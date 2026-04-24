# 🏗️ Case Study: Instagram (Photo Sharing Platform)

## 📋 Requirements

**Functional:**
- Users can upload photos/videos
- Users can follow/unfollow other users
- Users see a feed of posts from people they follow
- Users can like and comment on posts
- Users can search for other users and hashtags
- Explore page shows trending/popular content
- Direct messaging (optional)
- Stories (24-hour disappearing content)

**Non-Functional:**
- 1 billion users, 100 million daily active
- 100 million photos uploaded per day
- 2 billion feed views per day
- High availability (99.99%)
- Post appears in followers' feeds within 5 seconds (eventual consistency OK)

---

## 📊 Capacity Estimation

```
Users: 100M DAU
Photos/day: 100M uploads
Photo size: 5MB average → 500TB storage per day!
  After compression (70%): 150TB/day
  1 year: ~55PB (55 Petabytes!)

Feed views: 2B/day = ~23,000 reads/sec
Uploads: 100M/day = ~1,157 uploads/sec
Likes: 5B/day = ~57,870 likes/sec

API calls: ~50,000 req/sec total
```

---

## 🏗️ High Level Architecture

```
Mobile App / Web Browser
           ↓
     [AWS CloudFront CDN]
     /         |          \
[API Gateway] [S3 Media]  [CloudFront = fast image delivery]
     ↓
[Load Balancer (ALB)]
     ↓
┌─────────────────────────────────────────────────────────┐
│                   MICROSERVICES                          │
│                                                         │
│ [User Service]    [Post Service]    [Feed Service]      │
│ [Follow Service]  [Media Service]   [Search Service]    │
│ [Notification Srv][Comment Service] [Story Service]     │
└─────────────────────────────────────────────────────────┘
     ↓
[PostgreSQL RDS] [MongoDB] [Redis ElastiCache] [Elasticsearch]
[S3 + Lambda]   [SQS/SNS]  [Kafka]
```

---

## 📸 Photo Upload Flow

```javascript
// Media Service

// Step 1: Get pre-signed S3 URL for direct upload
app.post('/api/media/upload-url', authenticate, async (req, res) => {
  const { contentType, fileSize } = req.body;
  
  // Validate
  const MAX_FILE_SIZE = 50 * 1024 * 1024; // 50MB
  const allowedTypes = ['image/jpeg', 'image/png', 'image/webp', 'video/mp4', 'video/quicktime'];
  
  if (fileSize > MAX_FILE_SIZE) return res.status(400).json({ error: 'File too large' });
  if (!allowedTypes.includes(contentType)) return res.status(400).json({ error: 'Invalid file type' });
  
  const mediaId = crypto.randomUUID();
  const key = `uploads/raw/${req.user.id}/${mediaId}`;
  
  // Create media record (pending status)
  await db.query(
    'INSERT INTO media (id, user_id, s3_key, status) VALUES ($1, $2, $3, $4)',
    [mediaId, req.user.id, key, 'pending']
  );
  
  // Generate pre-signed upload URL (5 min to upload)
  const uploadUrl = s3.getSignedUrl('putObject', {
    Bucket: process.env.S3_BUCKET,
    Key: key,
    ContentType: contentType,
    ContentLength: fileSize,
    Expires: 300
  });
  
  res.json({ uploadUrl, mediaId });
  // Client uploads directly to S3 — your server never handles the bytes!
});

// Step 2: After S3 upload, S3 Event → Lambda → Process media
// Lambda triggers on s3:ObjectCreated in uploads/raw/*

// Lambda function (media-processor)
exports.handler = async (event) => {
  const record = event.Records[0];
  const s3Key = record.s3.object.key;
  const mediaId = s3Key.split('/').pop();
  
  // Download from S3
  const original = await s3.getObject({ Bucket: process.env.S3_BUCKET, Key: s3Key }).promise();
  
  // Resize to multiple formats using Sharp
  const sizes = { thumbnail: 150, medium: 640, large: 1080, original: null };
  
  const processedKeys = {};
  for (const [size, width] of Object.entries(sizes)) {
    let buffer;
    if (width) {
      buffer = await sharp(original.Body)
        .resize(width, null, { withoutEnlargement: true })
        .jpeg({ quality: 80 })
        .toBuffer();
    } else {
      buffer = original.Body;
    }
    
    const processedKey = `media/${size}/${mediaId}.jpg`;
    await s3.putObject({
      Bucket: process.env.S3_BUCKET,
      Key: processedKey,
      Body: buffer,
      ContentType: 'image/jpeg',
      CacheControl: 'public, max-age=31536000' // Cache 1 year (immutable!)
    }).promise();
    
    processedKeys[size] = `${process.env.CDN_URL}/${processedKey}`;
  }
  
  // Update media record
  await db.query(
    'UPDATE media SET status = $1, thumbnail_url = $2, medium_url = $3, large_url = $4, original_url = $5 WHERE id = $6',
    ['ready', processedKeys.thumbnail, processedKeys.medium, processedKeys.large, processedKeys.original, mediaId]
  );
  
  // Delete raw upload (save storage)
  await s3.deleteObject({ Bucket: process.env.S3_BUCKET, Key: s3Key }).promise();
};

// Step 3: Create post
app.post('/api/posts', authenticate, async (req, res) => {
  const { mediaId, caption, location, tags } = req.body;
  
  // Verify media is ready and owned by user
  const media = await db.query('SELECT * FROM media WHERE id = $1 AND user_id = $2 AND status = $3',
    [mediaId, req.user.id, 'ready']);
  if (!media.rows[0]) return res.status(400).json({ error: 'Media not found or not ready' });
  
  // Create post
  const post = await db.query(
    'INSERT INTO posts (user_id, media_id, caption, location) VALUES ($1, $2, $3, $4) RETURNING *',
    [req.user.id, mediaId, caption, location]
  );
  
  // Extract and save hashtags
  const hashtags = (caption.match(/#[\w]+/g) || []).map(tag => tag.slice(1).toLowerCase());
  if (hashtags.length > 0) {
    await processHashtags(post.rows[0].id, hashtags);
  }
  
  // Trigger feed fanout (async)
  await sqs.sendMessage({
    QueueUrl: process.env.FEED_FANOUT_QUEUE,
    MessageBody: JSON.stringify({ postId: post.rows[0].id, userId: req.user.id })
  }).promise();
  
  res.status(201).json(post.rows[0]);
});
```

---

## 📰 Feed Generation (Critical Design Decision)

**The Instagram Feed Problem:**
- User A has 10 million followers
- User A posts → need to update 10 million feeds!
- Celebrity account: Selena Gomez has 400M followers!

### Push vs Pull vs Hybrid

```javascript
// PULL (fan-out on read) — Simple, used for celebrities
// User opens app → Query posts from everyone they follow
async function getFeedPull(userId, cursor, limit = 20) {
  // Get who user follows
  const following = await db.query(
    'SELECT following_id FROM follows WHERE follower_id = $1',
    [userId]
  );
  const followingIds = following.rows.map(r => r.following_id);
  
  // Get their recent posts
  return db.query(
    'SELECT posts.*, users.username, users.avatar_url FROM posts JOIN users ON posts.user_id = users.id WHERE posts.user_id = ANY($1) AND posts.created_at < $2 ORDER BY posts.created_at DESC LIMIT $3',
    [followingIds, cursor || new Date(), limit]
  );
}
// Problem: Following 500 people = 500 user IDs in WHERE clause, millions of rows scanned!

// PUSH (fan-out on write) — Fast reads, used for regular users
// User posts → push post ID to all followers' feed queues
async function fanOutToFollowers(postId, userId) {
  // Get all followers
  let offset = 0;
  const batchSize = 1000;
  
  while (true) {
    const followers = await db.query(
      'SELECT follower_id FROM follows WHERE following_id = $1 LIMIT $2 OFFSET $3',
      [userId, batchSize, offset]
    );
    
    if (followers.rows.length === 0) break;
    
    // Add post to each follower's feed cache
    const pipeline = redis.pipeline();
    followers.rows.forEach(({ follower_id }) => {
      pipeline.zadd(`feed:${follower_id}`, Date.now(), postId); // Sorted set by timestamp
      pipeline.zremrangebyrank(`feed:${follower_id}`, 0, -(500 + 1)); // Keep latest 500
    });
    await pipeline.exec();
    
    offset += batchSize;
    if (followers.rows.length < batchSize) break;
  }
}

// HYBRID — Best of both worlds (Instagram's actual approach)
async function getFeedHybrid(userId, cursor, limit = 20) {
  // 1. Get pre-computed feed from Redis (push model for normal users)
  const cachedPostIds = await redis.zrevrangebyscore(
    `feed:${userId}`, 
    cursor ? cursor : '+inf',
    '-inf',
    'WITHSCORES', 'LIMIT', 0, limit
  );
  
  let feedPostIds = [];
  for (let i = 0; i < cachedPostIds.length; i += 2) {
    feedPostIds.push(cachedPostIds[i]);
  }
  
  // 2. For celebrities (>1M followers), pull their posts at read time
  const celebrities = await redis.smembers(`user:${userId}:celebrity_following`);
  if (celebrities.length > 0) {
    const celebPosts = await db.query(
      'SELECT id, created_at FROM posts WHERE user_id = ANY($1) ORDER BY created_at DESC LIMIT $2',
      [celebrities, limit]
    );
    feedPostIds = [...feedPostIds, ...celebPosts.rows.map(p => p.id)];
    
    // Sort by timestamp
    feedPostIds.sort((a, b) => /* by timestamp */);
    feedPostIds = feedPostIds.slice(0, limit);
  }
  
  // 3. Fetch post details in one query
  return db.query(
    'SELECT posts.*, users.username, users.avatar_url FROM posts JOIN users ON posts.user_id = users.id WHERE posts.id = ANY($1)',
    [feedPostIds]
  );
}
```

---

## ❤️ Like and Comment System

```javascript
// Like Service — must handle 57,870 likes/sec!

// ❌ Don't write to DB on every like
app.post('/api/posts/:id/like', authenticate, async (req, res) => {
  const postId = req.params.id;
  const userId = req.user.id;
  
  // 1. Atomic add to Redis set (prevents duplicate likes)
  const added = await redis.sadd(`post:${postId}:likes`, userId);
  
  if (added === 0) {
    // Already liked → unlike
    await redis.srem(`post:${postId}:likes`, userId);
    return res.json({ liked: false });
  }
  
  // 2. Increment counter in Redis (atomic!)
  await redis.incr(`post:${postId}:like_count`);
  
  // 3. Write to DB asynchronously (queue it)
  await sqs.sendMessage({
    QueueUrl: process.env.LIKES_QUEUE,
    MessageBody: JSON.stringify({ postId, userId, action: 'like' })
  }).promise();
  
  res.json({ liked: true });
});

// Background worker: Batch write likes to DB
likesQueue.process(async (job) => {
  const { postId, userId, action } = job.data;
  
  if (action === 'like') {
    await db.query(
      'INSERT INTO post_likes (post_id, user_id) VALUES ($1, $2) ON CONFLICT DO NOTHING',
      [postId, userId]
    );
    await db.query('UPDATE posts SET likes_count = likes_count + 1 WHERE id = $1', [postId]);
  } else {
    await db.query('DELETE FROM post_likes WHERE post_id = $1 AND user_id = $2', [postId, userId]);
    await db.query('UPDATE posts SET likes_count = likes_count - 1 WHERE id = $1', [postId]);
  }
});

// Comment Service
app.post('/api/posts/:id/comments', authenticate, async (req, res) => {
  const { content } = req.body;
  
  const comment = await db.query(
    'INSERT INTO comments (post_id, user_id, content) VALUES ($1, $2, $3) RETURNING *',
    [req.params.id, req.user.id, content]
  );
  
  // Update comment count
  await db.query('UPDATE posts SET comments_count = comments_count + 1 WHERE id = $1', [req.params.id]);
  
  // Notify post owner
  await notificationQueue.add({
    type: 'comment',
    postId: req.params.id,
    commenterId: req.user.id,
    comment: content
  });
  
  res.status(201).json(comment.rows[0]);
});
```

---

## 🔍 Search Service

```javascript
// Elasticsearch for user and hashtag search

// Index user when created
userService.on('user.created', async (user) => {
  await elasticsearch.index({
    index: 'users',
    id: user.id,
    document: {
      username: user.username,
      displayName: user.displayName,
      bio: user.bio,
      followerCount: 0,
      isVerified: false
    }
  });
});

// Search endpoint
app.get('/api/search', async (req, res) => {
  const { q, type = 'all' } = req.query;
  
  const results = await elasticsearch.search({
    index: type === 'hashtags' ? 'hashtags' : 'users',
    query: {
      bool: {
        should: [
          { match_phrase_prefix: { username: q } },  // "john" → "john_doe"
          { match: { displayName: { query: q, fuzziness: 'AUTO' } } }
        ],
        minimum_should_match: 1
      }
    },
    sort: [{ followerCount: 'desc' }], // Popular accounts first
    size: 20
  });
  
  res.json(results.hits.hits.map(h => h._source));
});
```

---

## 🗄️ Database Schema

```sql
-- Users
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  username VARCHAR(30) UNIQUE NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255),
  display_name VARCHAR(100),
  bio VARCHAR(150),
  avatar_url VARCHAR(500),
  is_private BOOLEAN DEFAULT false,
  is_verified BOOLEAN DEFAULT false,
  follower_count INT DEFAULT 0,
  following_count INT DEFAULT 0,
  post_count INT DEFAULT 0,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Posts
CREATE TABLE posts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id),
  media_id UUID NOT NULL REFERENCES media(id),
  caption TEXT,
  location VARCHAR(100),
  likes_count INT DEFAULT 0,
  comments_count INT DEFAULT 0,
  is_deleted BOOLEAN DEFAULT false,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_posts_user_id ON posts(user_id, created_at DESC);
CREATE INDEX idx_posts_created_at ON posts(created_at DESC) WHERE is_deleted = false;

-- Follows (many-to-many)
CREATE TABLE follows (
  follower_id UUID REFERENCES users(id) ON DELETE CASCADE,
  following_id UUID REFERENCES users(id) ON DELETE CASCADE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  PRIMARY KEY (follower_id, following_id)
);

CREATE INDEX idx_follows_following ON follows(following_id, follower_id);

-- Comments
CREATE TABLE comments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  post_id UUID NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES users(id),
  content VARCHAR(2200) NOT NULL,
  likes_count INT DEFAULT 0,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_comments_post_id ON comments(post_id, created_at);
```

---

## 🎯 Interview Discussion Points

### Key Design Decisions

1. **Feed Architecture:** Hybrid push+pull. Regular users: fan-out to followers' Redis sorted sets. Celebrities (>1M followers): pull-on-read to avoid 1M Redis writes per post.

2. **Media Storage:** S3 + Lambda for processing, CloudFront for global delivery. Never store media in the database.

3. **Like/Counter System:** Redis atomic operations for real-time counts, async queue for persistent storage. Prevents 57,870 DB writes/sec.

4. **Feed Caching:** Each user's feed cached in Redis as sorted set (post IDs with timestamp score). App fetches full post details only for visible feed items.

5. **Consistency:** Feed is eventually consistent (slight delay is fine). Likes are eventually consistent. User profile data is strongly consistent (profile updates must be immediate).

### Scaling Challenges

```
Celebrity Problem: Beyoncé posts → fan out to 100M followers
Solution: Skip fan-out for users with >1M followers (celebrity threshold)
         Pull their posts at feed load time instead

Hot Partition Problem: Famous user's data all on one DB shard
Solution: Use user_id-based sharding, but add celeb-specific caching layer

Storage Problem: 55PB per year
Solution: Intelligent tiering (recent posts → S3 Standard, old → Glacier)
         Delete old Stories automatically (24h TTL in S3 lifecycle)
```

---

### Navigation
**Prev:** [01_Design_URL_Shortener.md](01_Design_URL_Shortener.md) | **Index:** [00_Index.md](00_Index.md) | **Next:** [03_Design_WhatsApp.md](03_Design_WhatsApp.md)
