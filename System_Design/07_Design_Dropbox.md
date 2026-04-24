# 🏗️ Case Study: Dropbox (File Sync and Storage)

## 📋 Requirements

**Functional:**
- Users can upload files and folders
- Files sync automatically across all devices
- File sharing (with permissions: view/edit)
- File versioning (restore previous versions)
- Conflict resolution when multiple devices edit same file
- Offline mode (sync when back online)
- File search

**Non-Functional:**
- 500M registered users, 100M active
- 500PB of data stored (yes, petabytes!)
- File upload latency < 2 seconds for small files
- Sync changes across devices in < 30 seconds
- 99.99% availability

---

## 📊 Capacity Estimation

```
Files: 100M users × 200 files avg = 20 billion files
Storage: 500PB total (5MB avg file size)

Uploads: 100M users × 1 upload/day = ~1,157 uploads/sec
  Average file: 5MB → 5.8GB/sec upload bandwidth

Sync events: Much more frequent than uploads
  (Sync checks happen every 30 seconds per device)
  100M users × 3 devices = 300M devices
  300M / 30 = 10M sync checks/sec!
  → Sync service is the highest-traffic component

Block storage:
  Files chunked into 4MB blocks
  Only changed blocks are uploaded (delta sync)
  5MB file = 2 blocks
```

---

## 🏗️ High Level Architecture

```
[Desktop Client] ←→ [Mobile App] ←→ [Web Browser]
        ↓ (file chunks)         ↓ (API calls)
[AWS S3 Multipart Upload]  [CloudFront + ALB]
                                   ↓
        ┌──────────────────────────────────────────┐
        │           MICROSERVICES                  │
        │  [Upload Service]  [Sync Service]        │
        │  [File Service]    [Sharing Service]     │
        │  [Versioning Svc]  [Search Service]      │
        │  [Notification Svc][Auth Service]        │
        └──────────────────────────────────────────┘
                           ↓
        [PostgreSQL]  [Redis]  [S3]  [Kafka]  [Elasticsearch]
```

---

## 📁 Core Architecture Concepts

### Block-Based Storage (Key Design!)

```javascript
// Instead of storing whole files, Dropbox splits files into 4MB blocks
// Only changed blocks are uploaded → saves bandwidth!

class BlockService {
  BLOCK_SIZE = 4 * 1024 * 1024; // 4MB
  
  // Split file into blocks on CLIENT SIDE
  async splitFileIntoBlocks(fileBuffer) {
    const blocks = [];
    for (let i = 0; i < fileBuffer.length; i += this.BLOCK_SIZE) {
      const blockData = fileBuffer.slice(i, i + this.BLOCK_SIZE);
      const blockHash = crypto.createHash('sha256').update(blockData).digest('hex');
      blocks.push({ hash: blockHash, data: blockData, size: blockData.length });
    }
    return blocks;
  }
  
  // Server: Check which blocks already exist (don't re-upload!)
  async checkExistingBlocks(blockHashes) {
    const result = await db.query(
      'SELECT hash FROM blocks WHERE hash = ANY($1)',
      [blockHashes]
    );
    const existingHashes = new Set(result.rows.map(r => r.hash));
    return blockHashes.filter(hash => !existingHashes.has(hash)); // Missing blocks
  }
  
  // Upload only missing blocks
  async uploadBlock(blockHash, blockData) {
    // S3 key = block hash (content-addressed storage!)
    const s3Key = `blocks/${blockHash.slice(0, 2)}/${blockHash.slice(2, 4)}/${blockHash}`;
    
    // Check if already exists (global deduplication!)
    const exists = await s3.headObject({ Bucket: process.env.BLOCKS_BUCKET, Key: s3Key }).promise()
      .then(() => true).catch(() => false);
    
    if (!exists) {
      await s3.putObject({
        Bucket: process.env.BLOCKS_BUCKET,
        Key: s3Key,
        Body: blockData,
        ContentType: 'application/octet-stream',
        ServerSideEncryption: 'aws:kms'
      }).promise();
      
      // Record in DB
      await db.query(
        'INSERT INTO blocks (hash, s3_key, size, reference_count) VALUES ($1, $2, $3, 0) ON CONFLICT (hash) DO NOTHING',
        [blockHash, s3Key, blockData.length]
      );
    }
    
    // Increment reference count
    await db.query('UPDATE blocks SET reference_count = reference_count + 1 WHERE hash = $1', [blockHash]);
    
    return s3Key;
  }
}
```

### File Upload Flow

```javascript
// Upload API — client calls this to upload a file

app.post('/api/files/upload', authenticate, async (req, res) => {
  const { fileName, folderPath, blockHashes } = req.body;
  const userId = req.user.id;
  
  // 1. Verify user has storage quota
  const user = await db.query('SELECT storage_used, storage_quota FROM users WHERE id = $1', [userId]);
  const fileSize = blockHashes.reduce((acc, { size }) => acc + size, 0);
  
  if (user.rows[0].storage_used + fileSize > user.rows[0].storage_quota) {
    return res.status(413).json({ error: 'Storage quota exceeded' });
  }
  
  // 2. Check which blocks already exist (deduplification!)
  const allHashes = blockHashes.map(b => b.hash);
  const missingHashes = await blockService.checkExistingBlocks(allHashes);
  
  // 3. Tell client which blocks to upload
  if (missingHashes.length > 0) {
    // Generate pre-signed URLs for each missing block
    const uploadUrls = await Promise.all(missingHashes.map(async (hash) => {
      const s3Key = `blocks/${hash.slice(0, 2)}/${hash.slice(2, 4)}/${hash}`;
      const url = s3.getSignedUrl('putObject', {
        Bucket: process.env.BLOCKS_BUCKET, Key: s3Key,
        ContentType: 'application/octet-stream', Expires: 3600
      });
      return { hash, uploadUrl: url };
    }));
    
    return res.json({ needsUpload: uploadUrls }); // Client uploads these blocks directly to S3
  }
  
  // 4. All blocks exist — create/update file record
  const fileId = await createOrUpdateFile(userId, fileName, folderPath, blockHashes);
  
  // 5. Trigger sync notification to user's other devices
  await syncService.notifyDevices(userId, fileId, 'file_created');
  
  res.json({ fileId, status: 'complete' });
});

// Client workflow:
// 1. Split file into 4MB blocks
// 2. Compute SHA256 hash of each block
// 3. POST /api/files/upload with hashes → server returns missing block upload URLs
// 4. Upload missing blocks directly to S3
// 5. POST /api/files/upload again → server finalizes file
// Benefit: Only upload NEW or CHANGED blocks!

async function createOrUpdateFile(userId, fileName, folderPath, blockHashes) {
  const fileHash = crypto.createHash('sha256')
    .update(blockHashes.map(b => b.hash).join(''))
    .digest('hex');
  
  // Check if file exists
  const existing = await db.query(
    'SELECT id, current_version FROM files WHERE user_id = $1 AND folder_path = $2 AND name = $3',
    [userId, folderPath, fileName]
  );
  
  if (existing.rows[0]) {
    // Update existing file — create new version!
    const newVersion = existing.rows[0].current_version + 1;
    
    await db.query('BEGIN');
    
    // Archive current version
    await db.query(
      'INSERT INTO file_versions (file_id, version, block_hashes, created_at) SELECT id, current_version, current_blocks, updated_at FROM files WHERE id = $1',
      [existing.rows[0].id]
    );
    
    // Update file
    await db.query(
      'UPDATE files SET current_blocks = $1, file_hash = $2, current_version = $3, updated_at = NOW() WHERE id = $4',
      [JSON.stringify(blockHashes), fileHash, newVersion, existing.rows[0].id]
    );
    
    await db.query('COMMIT');
    return existing.rows[0].id;
  } else {
    // New file
    const result = await db.query(
      'INSERT INTO files (user_id, name, folder_path, current_blocks, file_hash, size) VALUES ($1, $2, $3, $4, $5, $6) RETURNING id',
      [userId, fileName, folderPath, JSON.stringify(blockHashes), fileHash, blockHashes.reduce((acc, b) => acc + b.size, 0)]
    );
    return result.rows[0].id;
  }
}
```

---

## 🔄 Sync Service (Most Complex)

```javascript
// Sync service: Detects changes and delivers to all devices

class SyncService {
  // Device polls for changes (every 30 seconds OR on reconnect)
  async getChanges(userId, deviceId, sinceTimestamp) {
    // Get all file changes since the device last synced
    const changes = await db.query(
      'SELECT files.*, "action" FROM file_events WHERE user_id = $1 AND created_at > $2 ORDER BY created_at ASC LIMIT 500',
      [userId, new Date(sinceTimestamp)]
    );
    
    // Don't send changes MADE BY this device (it already has them)
    return changes.rows.filter(c => c.device_id !== deviceId);
  }
  
  // Push notification to user's devices when a file changes
  async notifyDevices(userId, fileId, action) {
    // Get all active devices for this user
    const devices = await db.query(
      'SELECT device_id, push_token FROM user_devices WHERE user_id = $1 AND is_active = true',
      [userId]
    );
    
    // Record change event
    await db.query(
      'INSERT INTO file_events (user_id, file_id, action, created_at) VALUES ($1, $2, $3, NOW())',
      [userId, fileId, action]
    );
    
    // Notify devices via WebSocket (if connected) or push notification
    devices.rows.forEach(async (device) => {
      const socketId = await redis.hget('device:sockets', device.device_id);
      
      if (socketId) {
        // Device is connected via WebSocket — send real-time notification
        io.to(socketId).emit('file_changed', { fileId, action });
      } else {
        // Device offline — send push notification (on reconnect they'll poll for changes)
        await pushNotificationService.send(device.push_token, {
          title: 'Dropbox',
          body: `${action === 'created' ? 'New' : 'Updated'} file available`,
          data: { fileId, action }
        });
      }
    });
  }
}

// Conflict resolution
async function resolveConflict(userId, localFile, serverFile) {
  // Simple strategy: "Last write wins" with a copy of conflicting version
  // Dropbox creates "filename (User's conflicted copy 2024-01-15).ext"
  
  const conflictName = `${localFile.name.replace(/\.[^.]+$/, '')} (${localFile.owner}'s conflicted copy ${new Date().toDateString()})${localFile.extension}`;
  
  // Keep server version as-is, save local version as conflict copy
  await createOrUpdateFile(userId, conflictName, localFile.folderPath, localFile.blocks);
  
  return { conflictFile: conflictName };
}
```

---

## 📤 File Sharing

```javascript
app.post('/api/files/:fileId/share', authenticate, async (req, res) => {
  const { emails, permission = 'view' } = req.body; // permission: 'view' | 'edit'
  
  const file = await db.query('SELECT * FROM files WHERE id = $1 AND user_id = $2', 
    [req.params.fileId, req.user.id]);
  if (!file.rows[0]) return res.status(404).json({ error: 'File not found' });
  
  // Create share records
  const shares = await Promise.all(emails.map(async (email) => {
    const sharedUser = await db.query('SELECT id FROM users WHERE email = $1', [email]);
    
    if (sharedUser.rows[0]) {
      // Existing user — grant direct access
      await db.query(
        'INSERT INTO file_shares (file_id, shared_with_user_id, permission, created_by) VALUES ($1, $2, $3, $4) ON CONFLICT (file_id, shared_with_user_id) DO UPDATE SET permission = $3',
        [req.params.fileId, sharedUser.rows[0].id, permission, req.user.id]
      );
    } else {
      // New user — create invite link
      const inviteToken = crypto.randomBytes(32).toString('hex');
      await db.query(
        'INSERT INTO file_share_invites (file_id, email, permission, token, expires_at) VALUES ($1, $2, $3, $4, NOW() + INTERVAL \'7 days\')',
        [req.params.fileId, email, permission, inviteToken]
      );
      await emailService.sendShareInvitation(email, req.user.name, file.rows[0].name, inviteToken);
    }
  }));
  
  res.json({ message: 'Shared successfully' });
});

// Generate public sharing link
app.post('/api/files/:fileId/share-link', authenticate, async (req, res) => {
  const { permission = 'view', expiresIn } = req.body;
  
  const linkToken = crypto.randomBytes(32).toString('hex');
  const expiresAt = expiresIn ? new Date(Date.now() + expiresIn * 1000) : null;
  
  await db.query(
    'INSERT INTO share_links (file_id, token, permission, expires_at, created_by) VALUES ($1, $2, $3, $4, $5)',
    [req.params.fileId, linkToken, permission, expiresAt, req.user.id]
  );
  
  res.json({ shareLink: `${process.env.APP_URL}/shared/${linkToken}` });
});
```

---

## 📜 Version History

```javascript
// Versioning: Keep last N versions of each file

app.get('/api/files/:fileId/versions', authenticate, async (req, res) => {
  const versions = await db.query(
    'SELECT v.*, u.name as author_name FROM file_versions v JOIN users u ON v.author_id = u.id WHERE v.file_id = $1 ORDER BY v.version DESC LIMIT 30',
    [req.params.fileId]
  );
  
  res.json(versions.rows);
});

app.post('/api/files/:fileId/restore/:version', authenticate, async (req, res) => {
  const { fileId, version } = req.params;
  
  const targetVersion = await db.query(
    'SELECT * FROM file_versions WHERE file_id = $1 AND version = $2',
    [fileId, parseInt(version)]
  );
  
  if (!targetVersion.rows[0]) return res.status(404).json({ error: 'Version not found' });
  
  // Create new version with old blocks
  await db.query('BEGIN');
  
  // Archive current version
  await db.query(
    'INSERT INTO file_versions (file_id, version, block_hashes, author_id) SELECT id, current_version, current_blocks, $1 FROM files WHERE id = $2',
    [req.user.id, fileId]
  );
  
  // Restore target version
  await db.query(
    'UPDATE files SET current_blocks = $1, current_version = current_version + 1, updated_at = NOW() WHERE id = $2',
    [targetVersion.rows[0].block_hashes, fileId]
  );
  
  await db.query('COMMIT');
  
  // Notify devices of restore
  await syncService.notifyDevices(req.user.id, fileId, 'restored');
  
  res.json({ message: `File restored to version ${version}` });
});
```

---

## 🗄️ Database Schema

```sql
-- Files
CREATE TABLE files (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id),
  name VARCHAR(255) NOT NULL,
  folder_path VARCHAR(1000) NOT NULL DEFAULT '/',
  file_hash VARCHAR(64),
  current_blocks JSONB NOT NULL DEFAULT '[]',
  size BIGINT NOT NULL DEFAULT 0,
  current_version INT NOT NULL DEFAULT 1,
  is_deleted BOOLEAN DEFAULT false,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE UNIQUE INDEX idx_files_path ON files(user_id, folder_path, name) WHERE is_deleted = false;

-- Blocks (deduplicated!)
CREATE TABLE blocks (
  hash VARCHAR(64) PRIMARY KEY,
  s3_key VARCHAR(200) NOT NULL,
  size INT NOT NULL,
  reference_count INT DEFAULT 0
);

-- Versions
CREATE TABLE file_versions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  file_id UUID NOT NULL REFERENCES files(id),
  version INT NOT NULL,
  block_hashes JSONB NOT NULL,
  size BIGINT,
  author_id UUID REFERENCES users(id),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(file_id, version)
);

-- Sync events
CREATE TABLE file_events (
  id BIGSERIAL PRIMARY KEY,
  user_id UUID NOT NULL,
  file_id UUID REFERENCES files(id),
  device_id VARCHAR(100),
  action VARCHAR(30) NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
) PARTITION BY RANGE (created_at);
```

---

## 🎯 Interview Discussion Points

### Key Design Decisions

1. **Block-Based Storage:**
   - Files split into 4MB blocks
   - Content-addressed: Block hash = S3 key
   - Deduplication: If 1M users upload same file, only ONE copy in S3!
   - Delta sync: Only upload changed blocks when file updates

2. **Metadata vs Data Separation:**
   - Metadata (file names, paths, versions) → PostgreSQL
   - Block data → S3
   - Never mix them! DB for small, structured data. S3 for large blobs.

3. **Sync Architecture:**
   - Clients poll every 30s (simple, reliable)
   - WebSocket for instant notification when connected
   - Event log in DB: "What changed and when?"
   - Device syncs from where it last left off

4. **Conflict Resolution:**
   - Detection: Compare server and local file hashes before upload
   - Resolution: Create conflict copy (simple, user-visible, no data loss)
   - Alternative: Operational transforms (complex, used by Google Docs for real-time collaboration)

5. **Storage Optimization:**
   - Content deduplication (same block → one S3 object, multiple references)
   - Compression (gzip blocks before storage)
   - Tiering: Recent files in S3 Standard, old in S3 Glacier
   - Garbage collection: Decrement reference count when file deleted, delete block when count = 0

---

### Navigation
**Prev:** [06_Design_Twitter.md](06_Design_Twitter.md) | **Index:** [00_Index.md](00_Index.md) | **Next:** [08_Design_Google_Drive.md](08_Design_Google_Drive.md)
