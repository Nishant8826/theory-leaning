# 📌 Storage Systems

## 🧠 Concept Explanation (Story Format)

You're Instagram. Every day, 100 million photos are uploaded. Each photo is 5MB. That's 500TB of data per day.

You can't store all that in PostgreSQL or MongoDB. You need specialized storage systems for different types of data.

Think about your own house:
- Important documents (passport, birth certificate) → a safe (database)
- Everyday files (work documents) → filing cabinet (file system)
- Old clothes and boxes → attic/storage unit (cold storage)
- Books you reference daily → on your desk (cache)

Different data has different access patterns and requires different storage.

---

## 🏗️ Basic Design (Naive)

```
Everything in MongoDB:
- User data in MongoDB
- Profile photos in MongoDB (as base64 strings!) ← TERRIBLE
- Posts in MongoDB
- Logs in MongoDB

Problems:
- MongoDB not designed for large binary files
- DB gets huge, slow, expensive
- Can't serve images globally fast
- No CDN integration
```

---

## ⚡ Optimized Design

```
RIGHT TOOL FOR RIGHT DATA:

Structured Data (users, orders) → PostgreSQL (RDS)
Document Data (posts, comments) → MongoDB (Atlas/EC2)
File Storage (images, videos)  → AWS S3
Cache (hot data, sessions)     → Redis (ElastiCache)
Search Index (full-text)       → Elasticsearch
Time-Series (logs, metrics)    → CloudWatch / InfluxDB
Archive (old data, backups)    → S3 Glacier
Message Queue (async jobs)     → SQS / Redis Bull
```

---

## 🔍 Key Components

### 1. Object Storage (AWS S3)

Best for: Images, videos, documents, backups, static website files.

```javascript
const AWS = require('aws-sdk');
const multer = require('multer');
const s3 = new AWS.S3({ region: 'us-east-1' });

// Upload to S3 directly from Node.js
const upload = multer({ storage: multer.memoryStorage() });

app.post('/upload-photo', upload.single('photo'), async (req, res) => {
  const { originalname, buffer, mimetype } = req.file;
  const key = `photos/${req.user.id}/${Date.now()}-${originalname}`;
  
  const params = {
    Bucket: process.env.S3_BUCKET_NAME,
    Key: key,
    Body: buffer,
    ContentType: mimetype,
    // Optional: make publicly readable
    // ACL: 'public-read'  
  };
  
  const result = await s3.upload(params).promise();
  
  // Store S3 URL in database, not the file!
  await db.query(
    'UPDATE users SET avatar_url = $1 WHERE id = $2',
    [result.Location, req.user.id]
  );
  
  res.json({ url: result.Location });
});

// Generate pre-signed URL for secure, time-limited access
const getSignedUrl = (key, expirySeconds = 3600) => {
  return s3.getSignedUrl('getObject', {
    Bucket: process.env.S3_BUCKET_NAME,
    Key: key,
    Expires: expirySeconds  // URL expires in 1 hour
  });
};

// Upload directly from browser (bypass your server for large files!)
app.get('/upload-url', async (req, res) => {
  const key = `uploads/${req.user.id}/${Date.now()}-${req.query.filename}`;
  const uploadUrl = s3.getSignedUrl('putObject', {
    Bucket: process.env.S3_BUCKET_NAME,
    Key: key,
    Expires: 300,  // 5 minutes to upload
    ContentType: req.query.contentType
  });
  res.json({ uploadUrl, key });
});
// Frontend uploads directly to S3 using the signed URL!
// Your server never sees the file bytes → much faster + cheaper
```

**S3 Storage Classes (Cost Optimization):**
```
S3 Standard:         Frequently accessed data (hot)    → Most expensive
S3 Intelligent-Tier: Unknown access patterns           → Auto-moves between tiers
S3 Standard-IA:      Infrequent access (> 1/month)    → 40% cheaper
S3 Glacier:          Archive (accessed < 1/year)       → 70% cheaper (retrieval: minutes-hours)
S3 Glacier Deep:     Long-term archive (7+ years)      → Cheapest (retrieval: hours-days)
```

### 2. Block Storage (AWS EBS)

Best for: Database data files, OS disks, anything that needs low-latency I/O.

```
EBS = Virtual hard disk for your EC2 instance
- Used by: PostgreSQL, MongoDB when self-hosted on EC2
- Types:
  gp3: General purpose SSD (most common, 3000 IOPS baseline)
  io2: High performance SSD (100,000+ IOPS, for databases)
  st1: Throughput-optimized HDD (big data, sequential reads)
  sc1: Cold HDD (archiving, lowest cost)

You don't interact with EBS in code — it's transparent storage for your EC2.
```

### 3. File Storage (AWS EFS)

Best for: Shared file system across multiple EC2 instances.

```javascript
// When do you need EFS vs S3?
// EFS: Multiple servers need to read/write the same files simultaneously
//      like NFS (network file system)
// Example: Multiple Node.js servers that process uploaded files
//         EFS lets all of them access the same uploaded files

// S3: Object storage — better for most use cases
// Just store file in S3, store URL in DB → no need for EFS

// EFS use case: Legacy apps that use local file system paths
// or when you need POSIX file semantics
```

### 4. In-Memory Storage (Redis)

Best for: Caching, sessions, real-time data, leaderboards, queues.

```javascript
// Already covered in Caching chapter, but here's a summary:
const redis = require('ioredis');
const client = new redis(process.env.REDIS_URL);

// Different data structures for different use cases:
await client.set('key', 'value', 'EX', 3600);           // Simple cache
await client.hset('user:123', { name: 'Alice' });        // User object
await client.zadd('leaderboard', 5000, 'alice');         // Sorted ranking
await client.sadd('online_users', 'alice', 'bob');       // Set of online users
await client.lpush('notifications:123', JSON.stringify(notif)); // Queue/list
await client.geoadd('drivers', lng, lat, driverId);      // Geospatial data
```

### 5. Time-Series Storage

Best for: Metrics, IoT data, logs, anything with timestamps.

```javascript
// AWS CloudWatch (managed time-series for metrics)
const cloudwatch = new AWS.CloudWatch();

// Record custom metrics
await cloudwatch.putMetricData({
  Namespace: 'MyApp/Performance',
  MetricData: [{
    MetricName: 'ApiLatency',
    Value: responseTime,
    Unit: 'Milliseconds',
    Dimensions: [{ Name: 'Endpoint', Value: '/api/posts' }]
  }]
}).promise();

// For IoT or high-frequency data → InfluxDB or AWS Timestream
// Time-series DBs are optimized for:
// - High write throughput (millions of data points/sec)
// - Efficient range queries by timestamp
// - Automatic data compression over time
// - Automatic deletion of old data (retention policies)
```

### 6. Search Storage (Elasticsearch)

Best for: Full-text search, log analysis, complex queries.

```javascript
const { Client } = require('@elastic/elasticsearch');
const client = new Client({ node: process.env.ELASTICSEARCH_URL });

// Index a document (like a post)
await client.index({
  index: 'posts',
  id: post.id,
  document: {
    title: post.title,
    content: post.content,
    userId: post.userId,
    tags: post.tags,
    createdAt: post.createdAt
  }
});

// Full-text search with ranking
const results = await client.search({
  index: 'posts',
  query: {
    multi_match: {
      query: 'node.js redis caching',
      fields: ['title^2', 'content'],  // Title matches count double
      fuzziness: 'AUTO'  // Handle typos
    }
  },
  from: 0, size: 20  // Pagination
});
```

---

## ⚖️ Trade-offs

| Storage Type | Best For | Not For | Cost |
|-------------|---------|---------|------|
| S3 | Large files, backups | Fast random reads | Very cheap |
| PostgreSQL | Structured data, ACID | Schema-less data | Medium |
| MongoDB | Flexible documents | Complex joins | Medium |
| Redis | Hot data, caching | Large data | Expensive per GB |
| Elasticsearch | Search, logs | ACID transactions | Medium-High |
| EBS | Database storage, OS | Cross-instance sharing | Medium |
| Glacier | Archive, compliance | Frequent access | Very cheap |

---

## 📊 Scalability Discussion

### Data Tiering (Cost Optimization)

```
HOT TIER (frequently accessed — last 30 days):
  → Redis: Most accessed data (sub-millisecond)
  → PostgreSQL/MongoDB: Active records
  → S3 Standard: Active media files

WARM TIER (sometimes accessed — 30 days to 1 year):
  → PostgreSQL/MongoDB: Less active records (indexed, archived columns)
  → S3 Standard-IA: Less accessed files (e.g., old photos)

COLD TIER (rarely accessed — 1-7 years):
  → PostgreSQL archival tables: Old transactions
  → S3 Glacier: Old media, compliance data

DEEP COLD (compliance archive — 7+ years):
  → S3 Glacier Deep Archive: Tax records, legal documents

Automated lifecycle: S3 Lifecycle rules automatically move files between tiers:
S3 Standard → S3 IA (after 30 days) → Glacier (after 90 days) → Deep Archive (after 365 days)
This can reduce storage costs by 70-90%!
```

### Node.js Storage Decision Flow

```javascript
// Decision tree in your code:
async function storeData(data, type) {
  switch(type) {
    case 'user_session':
      return redis.setex(`session:${data.id}`, 3600, JSON.stringify(data));
    
    case 'profile_photo':
      const key = `photos/${data.userId}/${Date.now()}.jpg`;
      await s3.upload({ Bucket: process.env.BUCKET, Key: key, Body: data.buffer }).promise();
      return `https://cdn.myapp.com/${key}`; // CloudFront URL
    
    case 'user_data':
      return primaryDB.query('INSERT INTO users...', [...]);
    
    case 'post':
      return mongoDB.collection('posts').insertOne(data);
    
    case 'search_index':
      return elasticsearch.index({ index: 'posts', document: data });
    
    case 'app_metric':
      return cloudwatch.putMetricData({ ... });
  }
}
```

---

## 💼 Interview Questions (WITH SOLUTIONS)

### Q1: How would you store 1 million profile photos in your system?

**Solution:**
**NEVER store photos in your database** (as binary blobs or base64 strings):
- Bloats your DB → slow queries
- DB not optimized for binary data
- No CDN integration
- Expensive to replicate

**Correct approach:**
1. Upload photo → Node.js API → AWS S3 (using multipart upload for large files)
2. Store the S3 key/URL in your PostgreSQL/MongoDB
3. Serve via CloudFront CDN (S3 bucket as origin)
4. For thumbnails: S3 upload triggers Lambda → generates thumbnails → stores in S3

```javascript
// Complete photo upload flow
app.post('/upload-avatar', upload.single('photo'), async (req, res) => {
  // 1. Upload original to S3
  const originalKey = `avatars/original/${req.user.id}.jpg`;
  await s3.putObject({ Bucket: BUCKET, Key: originalKey, Body: req.file.buffer }).promise();
  
  // 2. Generate thumbnail (or let Lambda do it)
  const thumbnailKey = `avatars/thumbnail/${req.user.id}.jpg`;
  const thumbnail = await sharp(req.file.buffer).resize(150, 150).jpeg({ quality: 80 }).toBuffer();
  await s3.putObject({ Bucket: BUCKET, Key: thumbnailKey, Body: thumbnail }).promise();
  
  // 3. Store S3 URL in DB (not the photo!)
  const avatarUrl = `https://cdn.myapp.com/${thumbnailKey}`;
  await db.query('UPDATE users SET avatar_url = $1 WHERE id = $2', [avatarUrl, req.user.id]);
  
  res.json({ avatarUrl });
});
```

---

### Q2: What is the difference between S3, EBS, and EFS?

**Solution:**
| | S3 | EBS | EFS |
|-|----|----|-----|
| Type | Object storage | Block storage | File storage |
| Access | HTTP (REST API) | Mount as disk (EC2) | Mount as NFS (multiple EC2) |
| Sharing | Via URLs | Single EC2 only | Multiple EC2 simultaneously |
| Latency | ~50-200ms | <1ms | ~1-10ms |
| Scalability | Unlimited | Up to 64TB | Unlimited |
| Use case | Images, files, backups | Database storage, OS disk | Shared file system |
| Cost | Very cheap | Medium | Higher |

For our Node.js app:
- Profile photos → **S3** (accessible globally via URL)
- PostgreSQL data files → **EBS** (fast disk I/O)
- Shared config/assets across servers → **EFS** (rarely needed) or better: S3

---

### Q3: When would you use Redis vs a traditional database?

**Solution:**
Redis when:
- Data needs to be accessed in < 1ms (user sessions, hot cache)
- Data fits in memory (Redis is memory-bound)
- Data expires (session tokens, rate limit counters)
- Need specific data structures: sorted sets for leaderboards, pub/sub for real-time
- Atomic operations needed: INCR, DECR for counters

Database (PostgreSQL/MongoDB) when:
- Data must persist permanently (survive server restart)
- Data is too large for memory
- Need ACID guarantees
- Need complex queries (joins, aggregations)
- Data doesn't expire

**Common pattern:** Redis as cache in front of DB.
- Redis: recent/hot data (fast, temporary)
- DB: all data (slow, permanent)

---

### Q4: How do you handle a multi-TB database that's growing too fast?

**Solution:**
**Step 1: Audit what you're storing**
- Are you storing logs in the DB? Move to CloudWatch/Elasticsearch
- Are you storing large binary data in DB? Move to S3
- Are you storing derived/computed data? Can it be recalculated?

**Step 2: Data lifecycle management**
- Archive old data: Move records older than 2 years to archive tables
- Compress: Enable PostgreSQL compression for text columns
- Normalize: Are you storing duplicate data? Reference instead

**Step 3: Partition the table**
```sql
-- Time-based partitioning
CREATE TABLE events PARTITION BY RANGE (created_at);
-- Old partitions can be archived to S3 and dropped!
```

**Step 4: Move cold data to S3 + Athena**
- Export old records to S3 as Parquet files
- Query them with AWS Athena (SQL on S3!) when needed
- Cost: S3 + Athena query = tiny fraction of DB cost

**Step 5: Shard the database**
- Split data across multiple DB servers
- Each shard has a fraction of the data

---

### Q5: How do you design storage for a video streaming service like YouTube?

**Solution:**
```
Upload flow:
1. User uploads raw video → S3 (direct multipart upload, up to 5TB)
2. S3 triggers Lambda/SQS → Video processing queue
3. Worker: Transcodes to multiple resolutions (720p, 1080p, 4K)
   - Use AWS Elastic Transcoder or MediaConvert
4. Store transcoded segments in S3 (HLS format — small chunks)
5. Update MongoDB: video record with status + S3 keys

Streaming flow:
1. User clicks play → API returns CloudFront URL for video manifest (m3u8 file)
2. Video player (HLS.js) fetches manifest → fetches chunks from CloudFront edge
3. Adaptive bitrate: Player switches quality based on user's bandwidth
4. CloudFront caches popular videos at edge → most users never hit your S3!

Storage hierarchy:
- Hot (< 30 days old): CloudFront + S3 Standard (served from edge)
- Warm (30 days - 1 year): S3 Standard-IA + CloudFront (cached on demand)
- Cold (> 1 year): S3 Glacier (user must request → restored in hours)
- Metadata: MongoDB (video info, tags, views)
- Search: Elasticsearch (title, description, tags indexed)
- Analytics: S3 + Athena (viewing history, click-through data)
```

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem 1: Design the storage architecture for a Google Drive-like app

**Solution:**
```javascript
// Storage design:

// 1. File Storage: AWS S3 with folder structure
// s3://drive-files/user/{userId}/folder/{folderId}/{fileId}

// 2. Metadata: PostgreSQL
// files table: id, user_id, name, size, mime_type, s3_key, parent_folder_id, is_deleted, created_at
// folders table: id, user_id, name, parent_id, created_at
// shares table: file_id, shared_with_user_id, permission (view/edit), expires_at

// 3. Thumbnails: Lambda generates, stored in S3
// s3://drive-thumbnails/{fileId}/thumb.jpg

// 4. Cache (Redis): Recent file metadata, folder tree for active users
// 5. Search: Elasticsearch for file name + content search

// Upload flow (direct S3, server not in the path):
app.get('/upload-url', authenticate, async (req, res) => {
  const fileId = uuid();
  const key = `user/${req.user.id}/${fileId}/${req.query.filename}`;
  
  // Insert placeholder in DB
  await db.query('INSERT INTO files (id, user_id, name, s3_key, status) VALUES ($1, $2, $3, $4, $5)',
    [fileId, req.user.id, req.query.filename, key, 'uploading']);
  
  // Generate pre-signed URL for direct S3 upload
  const uploadUrl = s3.getSignedUrl('putObject', {
    Bucket: 'drive-files', Key: key, Expires: 600,
    ContentLength: req.query.size  // Prevent oversized uploads
  });
  
  res.json({ uploadUrl, fileId });
});

// S3 Event triggers Lambda → update file status to 'ready' in DB
// S3 Event triggers another Lambda → generate thumbnail if image/video

// Share a file:
app.post('/files/:id/share', authenticate, async (req, res) => {
  const { shareWithEmail, permission, expiresIn } = req.body;
  const user = await db.query('SELECT id FROM users WHERE email = $1', [shareWithEmail]);
  
  await db.query(
    'INSERT INTO shares (file_id, shared_with_user_id, permission, expires_at) VALUES ($1, $2, $3, $4)',
    [req.params.id, user.rows[0].id, permission, new Date(Date.now() + expiresIn)]
  );
  
  // Generate shareable link (short URL via URL shortener)
  // Send email notification
});
```

---

### Problem 2: How do you reduce S3 storage costs for a social media app with billions of photos?

**Solution:**
```
1. Compression at upload time:
   - Use Sharp.js to compress images before S3
   - JPEG quality 80% saves 60% space with minimal visual loss
   - WebP format: 30% smaller than JPEG

2. Multiple resolutions (don't serve 4K to phone):
   - thumbnail: 150x150 (profile pictures, grids)
   - medium: 800x600 (feed view)
   - original: full size (when user views full-screen)
   - Only generate what's needed, lazily

3. S3 Lifecycle policies:
   - Move originals to S3-IA after 30 days (people rarely re-view old photos)
   - Move to Glacier after 1 year
   - Delete very old photos from active storage (compliance permitting)

4. Content deduplication:
   - Hash each photo (MD5/SHA256)
   - If hash exists in DB → same photo → just store reference, not new copy
   - Users often share same memes/images

5. Lazy thumbnail generation:
   - Don't generate all sizes at upload
   - Generate on first request, cache in CloudFront

6. S3 Intelligent-Tiering:
   - Let AWS automatically move objects between tiers based on access patterns
   - Set it and forget it

Estimated savings:
- Compression: -60%
- Lifecycle tiering: -50% of remaining
- Deduplication: -20% of remaining
- Total: Can reduce storage costs by 80%+
```

---

### Navigation
**Prev:** [17_Monolith_vs_Microservices.md](17_Monolith_vs_Microservices.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [19_Content_Delivery_Network.md](19_Content_Delivery_Network.md)
