# 🏗️ Case Study: Google Drive (Collaborative Document Storage)

## 📋 Requirements

**Functional:**
- Upload, store, and download files (any type)
- Real-time collaborative document editing (Docs, Sheets)
- Share files/folders with permissions (viewer, commenter, editor)
- File versioning with restore
- Full-text search across your files
- Comments and suggestions in documents
- Offline access (sync when back online)

**Non-Functional:**
- 2 billion+ users
- 15GB free storage per user (2 billion × 15GB = 30 exabytes!)
- Real-time collaboration: Changes appear in < 500ms for all editors
- 99.99% availability
- Works everywhere: Web, iOS, Android, Desktop

---

## 📊 Capacity Estimation

```
Storage: 2B users × 15GB quota = 30EB (exabytes!)
  → Google actually uses WAY more (Google One paid plans)
  → Most users don't use full quota (~3GB avg actual usage)
  → Effective: 2B × 3GB = 6 exabytes

Uploads: 
  1B active users × 5 uploads/day = 5B uploads/day
  Avg size: 500KB → 2.5PB/day

Real-time collaboration:
  Say 50M docs with active editors
  Each keystroke = 1 operation
  1M concurrent editors × 10 keystrokes/min = 167K ops/sec

Files: ~30 trillion files stored in Google Drive!
```

---

## 🏗️ High Level Architecture

```
[Browser/Mobile/Desktop]
         ↓
[CDN (CloudFront) for static + media]
         ↓
[API Gateway + Load Balancer]
         ↓
┌──────────────────────────────────────────────────────────┐
│                      MICROSERVICES                        │
│  [Upload Service]     [Storage Service]  [Auth Service]  │
│  [Collaboration Svc]  [Search Service]   [Share Service] │
│  [Convert Service]    [Versioning Svc]   [Index Service] │
└──────────────────────────────────────────────────────────┘
         ↓
[GCS/S3]  [Spanner/Postgres]  [Redis]  [Elasticsearch]
[Firestore for real-time]    [Kafka]   [BigTable]
```

---

## 📁 File Storage Architecture

```javascript
// Google Drive-style file storage with chunked upload

class DriveUploadService {
  CHUNK_SIZE = 5 * 1024 * 1024; // 5MB chunks
  
  // Initiate resumable upload session
  async initiateUpload(userId, metadata) {
    const uploadSession = {
      sessionId: uuidv4(),
      userId,
      fileName: metadata.fileName,
      fileSize: metadata.fileSize,
      contentType: metadata.contentType,
      parentFolderId: metadata.parentFolderId,
      totalChunks: Math.ceil(metadata.fileSize / this.CHUNK_SIZE),
      uploadedChunks: new Set(),
      createdAt: Date.now()
    };
    
    // Store session in Redis (expire after 24 hours)
    await redis.setex(
      `upload_session:${uploadSession.sessionId}`,
      86400,
      JSON.stringify(uploadSession)
    );
    
    return { sessionId: uploadSession.sessionId };
  }
  
  // Upload individual chunk
  async uploadChunk(sessionId, chunkNumber, chunkData) {
    const sessionData = await redis.get(`upload_session:${sessionId}`);
    if (!sessionData) throw new Error('Upload session expired or not found');
    
    const session = JSON.parse(sessionData);
    
    // Upload chunk to S3
    const chunkKey = `temp_chunks/${sessionId}/chunk_${String(chunkNumber).padStart(5, '0')}`;
    
    await s3.putObject({
      Bucket: process.env.CHUNKS_BUCKET,
      Key: chunkKey,
      Body: chunkData
    }).promise();
    
    // Track uploaded chunks
    session.uploadedChunks = [...new Set([...session.uploadedChunks, chunkNumber])];
    await redis.setex(`upload_session:${sessionId}`, 86400, JSON.stringify(session));
    
    // If all chunks uploaded → finalize
    if (session.uploadedChunks.length === session.totalChunks) {
      return await this.finalizeUpload(sessionId, session);
    }
    
    return { uploaded: session.uploadedChunks.length, total: session.totalChunks };
  }
  
  // Merge chunks and create file
  async finalizeUpload(sessionId, session) {
    // Merge chunks using S3 multipart upload
    const multipart = await s3.createMultipartUpload({
      Bucket: process.env.FILES_BUCKET,
      Key: `files/${session.userId}/${uuidv4()}`
    }).promise();
    
    const parts = await Promise.all(
      Array.from({ length: session.totalChunks }, (_, i) => i).map(async (i) => {
        const chunk = await s3.getObject({
          Bucket: process.env.CHUNKS_BUCKET,
          Key: `temp_chunks/${sessionId}/chunk_${String(i).padStart(5, '0')}`
        }).promise();
        
        const upload = await s3.uploadPart({
          Bucket: process.env.FILES_BUCKET,
          Key: multipart.Key,
          UploadId: multipart.UploadId,
          PartNumber: i + 1,
          Body: chunk.Body
        }).promise();
        
        return { PartNumber: i + 1, ETag: upload.ETag };
      })
    );
    
    await s3.completeMultipartUpload({
      Bucket: process.env.FILES_BUCKET,
      Key: multipart.Key,
      UploadId: multipart.UploadId,
      MultipartUpload: { Parts: parts }
    }).promise();
    
    // Create file metadata in DB
    const file = await db.query(
      'INSERT INTO drive_files (user_id, name, content_type, size, s3_key, parent_folder_id) VALUES ($1, $2, $3, $4, $5, $6) RETURNING *',
      [session.userId, session.fileName, session.contentType, session.fileSize, multipart.Key, session.parentFolderId]
    );
    
    // Clean up temp chunks
    await this.cleanupChunks(sessionId, session.totalChunks);
    await redis.del(`upload_session:${sessionId}`);
    
    // Trigger async tasks (thumbnail, text extraction for search)
    await kafkaProducer.send({
      topic: 'file-uploaded',
      messages: [{ value: JSON.stringify({ fileId: file.rows[0].id, s3Key: multipart.Key, contentType: session.contentType }) }]
    });
    
    return file.rows[0];
  }
}
```

---

## 🖊️ Real-Time Collaboration (Google Docs)

```javascript
// Operational Transformation (OT) — the algorithm behind real-time editing

// Basic concept: Transform concurrent operations so they can be applied in any order
// Example: 2 users editing "Hello" simultaneously
// User A: Insert " World" at position 5 → "Hello World"
// User B: Delete char at position 0 → "ello"
// Without OT: Applying B after A gives wrong result
// With OT: Transform A's operation to account for B's deletion → correct result

class OperationalTransform {
  // Operations
  static insert(position, text) { return { type: 'insert', position, text }; }
  static delete(position, length) { return { type: 'delete', position, length }; }
  
  // Transform operation A given that operation B has already been applied
  static transform(opA, opB) {
    if (opA.type === 'insert' && opB.type === 'insert') {
      if (opB.position <= opA.position) {
        // B inserted before A → A's position shifts right
        return { ...opA, position: opA.position + opB.text.length };
      }
      return opA; // B inserted after A → A unaffected
    }
    
    if (opA.type === 'insert' && opB.type === 'delete') {
      if (opB.position + opB.length <= opA.position) {
        // B deleted before A → A's position shifts left
        return { ...opA, position: opA.position - opB.length };
      } else if (opB.position >= opA.position) {
        return opA; // B deleted after A → A unaffected
      } else {
        // B deleted across A's position
        return { ...opA, position: opB.position };
      }
    }
    
    // (Handle more cases for production...)
    return opA;
  }
}

// Collaboration Service
class CollaborationService {
  // Client sends operations as they type
  async applyOperation(documentId, userId, operation, clientVersion) {
    const docKey = `doc:${documentId}`;
    
    // Acquire lock (only one operation at a time!)
    const lock = await redis.set(`lock:${docKey}`, userId, 'NX', 'EX', 5);
    if (!lock) {
      // Wait and retry
      await new Promise(r => setTimeout(r, 50));
      return this.applyOperation(documentId, userId, operation, clientVersion);
    }
    
    try {
      // Get current document state from Redis
      const docState = await redis.get(docKey);
      const { content, version, history } = JSON.parse(docState);
      
      // Transform operation against any operations applied since clientVersion
      let transformedOp = operation;
      const missedOps = history.slice(clientVersion);
      
      for (const missedOp of missedOps) {
        transformedOp = OperationalTransform.transform(transformedOp, missedOp);
      }
      
      // Apply transformed operation to document
      const newContent = this.applyOp(content, transformedOp);
      const newVersion = version + 1;
      
      const newState = {
        content: newContent,
        version: newVersion,
        history: [...history, transformedOp].slice(-100) // Keep last 100 ops
      };
      
      await redis.setex(docKey, 3600, JSON.stringify(newState));
      
      // Broadcast to all connected clients in this document
      io.to(`doc:${documentId}`).emit('operation', {
        operation: transformedOp,
        version: newVersion,
        userId
      });
      
      // Persist to DB (async, every 30 ops or 10 seconds)
      if (newVersion % 30 === 0) {
        await this.persistDocument(documentId, newContent, newVersion);
      }
      
      return { version: newVersion, operation: transformedOp };
      
    } finally {
      await redis.del(`lock:${docKey}`);
    }
  }
  
  applyOp(content, op) {
    if (op.type === 'insert') {
      return content.slice(0, op.position) + op.text + content.slice(op.position);
    } else if (op.type === 'delete') {
      return content.slice(0, op.position) + content.slice(op.position + op.length);
    }
    return content;
  }
  
  async persistDocument(documentId, content, version) {
    await db.query(
      'UPDATE documents SET content = $1, version = $2, updated_at = NOW() WHERE id = $3',
      [content, version, documentId]
    );
    
    // Create version snapshot every 100 versions
    if (version % 100 === 0) {
      await db.query(
        'INSERT INTO document_versions (document_id, version, content, created_at) VALUES ($1, $2, $3, NOW())',
        [documentId, version, content]
      );
    }
  }
}

// WebSocket handler for collaborative editing
io.on('connection', (socket) => {
  socket.on('join_document', async (documentId) => {
    socket.join(`doc:${documentId}`);
    
    // Track collaborator presence
    await redis.sadd(`doc:${documentId}:users`, socket.userId);
    await redis.expire(`doc:${documentId}:users`, 3600);
    
    // Notify others of new collaborator
    socket.to(`doc:${documentId}`).emit('collaborator_joined', { userId: socket.userId });
    
    // Send current document state
    const docState = await redis.get(`doc:${documentId}`);
    socket.emit('document_state', JSON.parse(docState));
  });
  
  socket.on('operation', async ({ documentId, operation, clientVersion }) => {
    await collaborationService.applyOperation(documentId, socket.userId, operation, clientVersion);
  });
  
  socket.on('cursor_position', ({ documentId, position }) => {
    socket.to(`doc:${documentId}`).emit('cursor_update', { userId: socket.userId, position });
  });
  
  socket.on('leave_document', async (documentId) => {
    socket.leave(`doc:${documentId}`);
    await redis.srem(`doc:${documentId}:users`, socket.userId);
    socket.to(`doc:${documentId}`).emit('collaborator_left', { userId: socket.userId });
  });
});
```

---

## 🔍 Search Service

```javascript
// Full-text search across all files
// Extract text from files, index in Elasticsearch

// Kafka consumer: processes uploaded files
kafkaConsumer.run({
  eachMessage: async ({ message }) => {
    const { fileId, s3Key, contentType } = JSON.parse(message.value.toString());
    
    let extractedText = '';
    
    // Extract text based on file type
    if (contentType === 'application/pdf') {
      const pdfBuffer = await s3.getObject({ Bucket: process.env.FILES_BUCKET, Key: s3Key }).promise();
      const pdfData = await pdfParse(pdfBuffer.Body);
      extractedText = pdfData.text;
    } else if (contentType.startsWith('text/')) {
      const textFile = await s3.getObject({ Bucket: process.env.FILES_BUCKET, Key: s3Key }).promise();
      extractedText = textFile.Body.toString('utf-8').slice(0, 100000); // Max 100KB of text
    }
    
    // Index in Elasticsearch
    await elasticsearch.index({
      index: 'drive_files',
      id: fileId,
      document: {
        name: fileName,
        content: extractedText,
        contentType,
        ownerId: userId,
        sharedWith: [], // Updated when file is shared
        size: fileSize,
        createdAt: new Date()
      }
    });
  }
});

app.get('/api/search', authenticate, async (req, res) => {
  const { q, type, page = 1, limit = 20 } = req.query;
  
  const results = await elasticsearch.search({
    index: 'drive_files',
    query: {
      bool: {
        must: [{
          multi_match: {
            query: q,
            fields: ['name^3', 'content'], // Name matches are 3x more important
            fuzziness: 'AUTO'
          }
        }],
        // IMPORTANT: Users only see their own files or files shared with them
        filter: [{
          bool: {
            should: [
              { term: { ownerId: req.user.id } },
              { term: { sharedWith: req.user.id } }
            ]
          }
        }]
      }
    },
    highlight: { fields: { content: {} } }, // Highlight matching text
    from: (page - 1) * limit,
    size: limit
  });
  
  res.json({
    results: results.hits.hits.map(h => ({ ...h._source, highlight: h.highlight })),
    total: results.hits.total.value
  });
});
```

---

## 🔒 Permission System

```javascript
// Hierarchical permissions: Folder permissions cascade to files

class PermissionService {
  async checkPermission(userId, resourceId, requiredPermission) {
    const cacheKey = `perm:${userId}:${resourceId}`;
    
    const cached = await redis.get(cacheKey);
    if (cached) {
      const perm = JSON.parse(cached);
      return this.hasRequiredPermission(perm, requiredPermission);
    }
    
    // Check direct permission on resource
    let permission = await db.query(
      'SELECT permission FROM file_shares WHERE resource_id = $1 AND user_id = $2',
      [resourceId, userId]
    );
    
    // Check if user is owner
    const resource = await db.query('SELECT user_id, parent_folder_id FROM drive_files WHERE id = $1', [resourceId]);
    
    if (resource.rows[0]?.user_id === userId) {
      const ownerPerm = { canView: true, canComment: true, canEdit: true, canShare: true, canDelete: true };
      await redis.setex(cacheKey, 300, JSON.stringify(ownerPerm));
      return true; // Owner has all permissions
    }
    
    // Check inherited permissions from parent folder
    if (!permission.rows[0] && resource.rows[0]?.parent_folder_id) {
      permission = await db.query(
        'SELECT permission FROM file_shares WHERE resource_id = $1 AND user_id = $2',
        [resource.rows[0].parent_folder_id, userId]
      );
    }
    
    if (!permission.rows[0]) {
      await redis.setex(cacheKey, 300, JSON.stringify(null));
      return false;
    }
    
    const userPerm = this.parsePermission(permission.rows[0].permission);
    await redis.setex(cacheKey, 300, JSON.stringify(userPerm));
    
    return this.hasRequiredPermission(userPerm, requiredPermission);
  }
  
  parsePermission(permLevel) {
    const permissions = {
      viewer: { canView: true, canComment: false, canEdit: false, canShare: false, canDelete: false },
      commenter: { canView: true, canComment: true, canEdit: false, canShare: false, canDelete: false },
      editor: { canView: true, canComment: true, canEdit: true, canShare: false, canDelete: false },
      owner: { canView: true, canComment: true, canEdit: true, canShare: true, canDelete: true }
    };
    return permissions[permLevel] || permissions.viewer;
  }
  
  hasRequiredPermission(userPerm, required) {
    if (!userPerm) return false;
    return userPerm[required] === true;
  }
  
  // When permission changes, invalidate cache
  async invalidatePermissionCache(userId, resourceId) {
    await redis.del(`perm:${userId}:${resourceId}`);
  }
}
```

---

## 🗄️ Database Schema

```sql
-- Drive files and folders
CREATE TABLE drive_files (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id),
  parent_folder_id UUID REFERENCES drive_files(id),
  name VARCHAR(255) NOT NULL,
  is_folder BOOLEAN DEFAULT false,
  content_type VARCHAR(100),
  size BIGINT DEFAULT 0,
  s3_key VARCHAR(500),
  current_version INT DEFAULT 1,
  is_trashed BOOLEAN DEFAULT false,
  is_starred BOOLEAN DEFAULT false,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  modified_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_files_parent ON drive_files(parent_folder_id) WHERE NOT is_trashed;
CREATE INDEX idx_files_user ON drive_files(user_id, modified_at DESC);

-- Sharing
CREATE TABLE file_shares (
  resource_id UUID NOT NULL REFERENCES drive_files(id) ON DELETE CASCADE,
  user_id UUID REFERENCES users(id),
  email VARCHAR(255),
  permission VARCHAR(20) NOT NULL CHECK (permission IN ('viewer', 'commenter', 'editor')),
  shared_by UUID REFERENCES users(id),
  shared_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(resource_id, user_id)
);

-- Documents (for collaborative editing)
CREATE TABLE documents (
  file_id UUID PRIMARY KEY REFERENCES drive_files(id),
  content TEXT DEFAULT '',
  version INT DEFAULT 1,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Document version snapshots
CREATE TABLE document_versions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  document_id UUID REFERENCES documents(file_id),
  version INT NOT NULL,
  content TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  created_by UUID REFERENCES users(id)
);
```

---

## 🎯 Interview Discussion Points

### Key Design Decisions

1. **Operational Transformation for Real-Time Collaboration:**
   - OT ensures concurrent edits converge to the same document state
   - Google Docs uses a version of OT; newer systems use CRDTs (Conflict-free Replicated Data Types)
   - Redis stores active document state (fast); PostgreSQL for persistence

2. **Hierarchical Storage:**
   - Drive is a tree (folders contain files and sub-folders)
   - Adjacency list model in DB (parent_folder_id reference)
   - For deep trees: Use materialized paths or nested sets for efficient subtree queries

3. **Permission Cascading:**
   - Permissions inherit from parent folder to children
   - User can have explicit override on specific file
   - Cache permissions in Redis (most files are read often)
   - Invalidate cache when permissions change

4. **Search Across 2B Users:**
   - Each user's files indexed with ownerId/sharedWith filter
   - Elasticsearch's document-level security enforces access control
   - Text extraction for PDF, DOCX, TXT makes content searchable

5. **Resumable Uploads:**
   - Large files chunked (5MB each)
   - Client tracks which chunks uploaded (survives network interruption)
   - Server stores partial progress in Redis (24h TTL)
   - Resume from last successful chunk on reconnect

---

### Navigation
**Prev:** [07_Design_Dropbox.md](07_Design_Dropbox.md) | **Index:** [00_Index.md](00_Index.md)
