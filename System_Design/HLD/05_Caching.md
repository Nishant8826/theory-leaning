# 📌 Caching

## 🧠 Concept Explanation (Story Format)

You work at a library. Every time someone asks "Who wrote Harry Potter?", you walk to the back, search through thousands of books, find the answer, and come back. That's 5 minutes per question.

Smart move: Write the answer on a sticky note and stick it to the front desk. Next time someone asks → 2 seconds!

That sticky note is your **cache**. Redis is that sticky note, but for your Node.js app.

**Real world:** When you scroll Instagram, your feed is NOT fetched from the database every time. It's stored in Redis. When someone posts new content → Redis cache is updated. This is how Instagram serves 500 million daily users with reasonable hardware.

---

## 🏗️ Basic Design (Naive)

```
React App
    ↓ GET /api/feed
Node.js Server
    ↓ (every single request)
MongoDB → returns 50 posts
    ↓ (50ms - 200ms per request)
User gets feed

Problem: 1 million users refresh feed → 1M DB queries/minute!
```

---

## ⚡ Optimized Design

```
React App
    ↓ GET /api/feed?userId=123
Node.js Server
    ↓
[Redis Cache] ← Check cache first (~1ms)
    ↓ (MISS: data not in cache)
[MongoDB] ← Only query DB on cache miss (~50ms)
    ↓
Store result in Redis with TTL (Time-To-Live)
    ↓
Return data to user

Next request for same feed: Redis returns in 1ms!
```

---

## 🔍 Key Components

### Cache Hit vs Cache Miss

```
Cache HIT:  Request → Redis → Data found → Return (1ms) ✅
Cache MISS: Request → Redis → Not found → DB → Cache it → Return (50ms)

Hit Rate = (Cache Hits) / (Cache Hits + Cache Misses)
Target: > 80% hit rate for good performance
```

### Caching Strategies

**1. Cache-Aside (Lazy Loading) — Most Common**
```javascript
async function getUserProfile(userId) {
  const cacheKey = `user:${userId}`;
  
  // 1. Check cache
  const cached = await redis.get(cacheKey);
  if (cached) return JSON.parse(cached);
  
  // 2. Cache miss: fetch from DB
  const user = await db.query('SELECT * FROM users WHERE id = $1', [userId]);
  
  // 3. Store in cache
  await redis.setex(cacheKey, 3600, JSON.stringify(user.rows[0])); // 1hr TTL
  
  return user.rows[0];
}
```
**Pros:** Only caches what's actually needed. Cache failure doesn't break the app.
**Cons:** First request is always slow (cache miss).

---

**2. Write-Through Cache**
```javascript
async function updateUser(userId, data) {
  // Write to DB AND cache simultaneously
  await db.query('UPDATE users SET name=$1 WHERE id=$2', [data.name, userId]);
  await redis.setex(`user:${userId}`, 3600, JSON.stringify(data));
  // Cache is always in sync with DB
}
```
**Pros:** Cache is always fresh. No stale data.
**Cons:** Write operations are slightly slower (write to two places).

---

**3. Write-Behind (Write-Back) Cache**
```javascript
// Write to cache immediately, write to DB later (async)
async function updateUserAsync(userId, data) {
  await redis.setex(`user:${userId}`, 3600, JSON.stringify(data));
  // Put DB write in queue — process later
  await queue.add('updateUserInDB', { userId, data });
  // Super fast response to user!
}
```
**Pros:** Fastest write speed.
**Cons:** Risk of data loss if cache crashes before DB write.

---

**4. Read-Through Cache**
```javascript
// Cache sits between app and DB, handles everything
// Used by Redis as a service (less common in Node.js direct use)
```

---

### What to Cache (and What NOT to)

✅ **Cache these:**
- User profiles (change rarely)
- Product catalog (changes infrequently)
- Trending posts / Hot content
- Session data / JWT tokens
- Config values
- Aggregated counts (likes, views)

❌ **Don't cache these:**
- User's bank account balance (must be real-time accurate)
- Payment transaction status
- Anything that changes every second
- Large binary data (use S3 instead)
- Per-user real-time data (stock prices for a specific portfolio)

### Cache Eviction Policies

When Redis is full, how does it decide what to delete?

| Policy | Description | Use Case |
|--------|-------------|----------|
| **LRU** (Least Recently Used) | Remove least recently accessed | General purpose (default) |
| **LFU** (Least Frequently Used) | Remove least accessed overall | Popularity-based content |
| **TTL** (Time-To-Live) | Remove expired keys | Session data |
| **Random** | Remove random keys | When all data equally important |

```
# Redis configuration
maxmemory 256mb
maxmemory-policy allkeys-lru  # Use LRU when memory is full
```

---

## ⚖️ Trade-offs

| Cache | No Cache |
|-------|----------|
| Fast responses | Fresh data always |
| Reduced DB load | No stale data risk |
| Stale data risk | Higher DB load |
| Extra infrastructure | Simpler system |
| Cache invalidation complexity | — |

**Cache invalidation is one of the hardest problems in CS!**
> "There are only two hard things in CS: cache invalidation and naming things." — Phil Karlton

---

## 📊 Scalability Discussion

### Multi-Level Caching

```
Browser Cache (seconds)
    ↓ miss
CDN Cache / CloudFront (minutes-hours)
    ↓ miss
Application Cache / Redis (minutes-hours)
    ↓ miss
Database (source of truth)
```

### Redis Data Structures

Redis isn't just key-value! Use the right structure:

```javascript
// String: Simple values
await redis.set('totalUsers', '1000000');
await redis.incr('totalUsers'); // Atomic increment!

// Hash: Object storage (more memory efficient than JSON string)
await redis.hset('user:123', { name: 'Alice', email: 'alice@example.com' });
const user = await redis.hgetall('user:123');

// Set: Unique items (followers list)
await redis.sadd('followers:alice', 'bob', 'charlie');
const isFollowing = await redis.sismember('followers:alice', 'bob'); // true/false

// Sorted Set: Ranked data (leaderboard)
await redis.zadd('leaderboard', 5000, 'alice'); // score, member
await redis.zadd('leaderboard', 8000, 'bob');
const top10 = await redis.zrevrange('leaderboard', 0, 9, 'WITHSCORES');

// List: Message queues, activity feeds
await redis.lpush('notifications:user123', JSON.stringify({ type: 'like', from: 'bob' }));
const notifications = await redis.lrange('notifications:user123', 0, 19); // last 20
```

---

## 💼 Interview Questions (WITH SOLUTIONS)

### Q1: What is caching and what problem does it solve?

**Solution:**
Caching is storing the result of an expensive operation in fast storage (Redis/memory) so future requests for the same data are served faster without repeating the expensive operation. It solves:
- **Latency:** DB queries take 50-200ms, Redis takes <1ms
- **DB overload:** Cache absorbs 80-90% of read traffic
- **Scalability:** Allows serving millions of users with fewer DB instances

---

### Q2: How do you handle cache invalidation?

**Solution:**
Cache invalidation = deciding when to remove/update stale cache data.

**Strategies:**
1. **TTL (Time-Based):** Cache expires after N seconds automatically
   ```javascript
   redis.setex('productPrice:123', 300, price); // Auto-expires after 5 min
   ```
2. **Event-Based:** Delete cache when data changes
   ```javascript
   async function updateProduct(productId, data) {
     await db.update('products', data, { where: { id: productId } });
     await redis.del(`product:${productId}`); // Invalidate immediately
   }
   ```
3. **Cache Versioning:** Add version to key
   ```javascript
   const version = await redis.get('products:version');
   const cacheKey = `products:${version}:list`;
   ```
4. **Write-Through:** Always update cache when updating DB (never stale, but slower writes)

---

### Q3: What is a cache stampede and how do you prevent it?

**Solution:**
**Problem:** Many requests arrive at the same time, all get cache miss, all hit DB simultaneously → DB crashes.

**Solution 1: Cache locking (Mutex)**
```javascript
async function getWithLock(key, fetchFn, ttl) {
  const cached = await redis.get(key);
  if (cached) return JSON.parse(cached);
  
  const lockKey = `lock:${key}`;
  const lockAcquired = await redis.set(lockKey, '1', 'EX', 10, 'NX'); // NX = only if not exists
  
  if (!lockAcquired) {
    // Another request is rebuilding cache, wait briefly and retry
    await sleep(100);
    return getWithLock(key, fetchFn, ttl);
  }
  
  const data = await fetchFn();
  await redis.setex(key, ttl, JSON.stringify(data));
  await redis.del(lockKey);
  return data;
}
```

**Solution 2: Probabilistic Early Expiry**
```javascript
// Randomly refresh cache a bit before it expires
const ttl = await redis.ttl(key);
const randomRefreshChance = Math.random() < (1 / ttl);
if (randomRefreshChance) {
  // Proactively refresh before everyone rushes
}
```

---

### Q4: How would you implement a leaderboard using Redis?

**Solution:**
```javascript
// Redis Sorted Set is perfect for leaderboards!

// Add/update score
async function updateScore(userId, newScore) {
  await redis.zadd('game:leaderboard', newScore, userId);
}

// Get top 10 players
async function getTop10() {
  const results = await redis.zrevrange('game:leaderboard', 0, 9, 'WITHSCORES');
  // Returns: ['userId1', '9000', 'userId2', '8500', ...]
  const leaderboard = [];
  for (let i = 0; i < results.length; i += 2) {
    leaderboard.push({ userId: results[i], score: parseInt(results[i+1]) });
  }
  return leaderboard;
}

// Get a specific user's rank
async function getUserRank(userId) {
  const rank = await redis.zrevrank('game:leaderboard', userId);
  return rank + 1; // 0-indexed, so add 1
}
```

---

### Q5: Explain CDN caching vs server-side caching.

**Solution:**
| | CDN (CloudFront) | Server Cache (Redis) |
|-|-----------------|---------------------|
| **What** | Caches static files near user | Caches dynamic data near server |
| **Where** | Edge locations globally | Server's network |
| **Best for** | Images, JS, CSS, HTML | API responses, user sessions |
| **Managed by** | AWS CloudFront config | Your Node.js code |
| **Cost** | Very cheap per GB | Small memory cost |

For Instagram:
- Your profile photo → CloudFront (same for everyone)
- Your personalized feed → Redis (different per user)

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem 1: Design a caching strategy for a news website

**Solution:**
```
Homepage (trending articles): Cache 5 min in Redis
  - Changes frequently but 5 min stale is OK
  - Cache key: "homepage:trending"

Article content: Cache 1 hour in Redis + CloudFront
  - Articles rarely change after publishing
  - Cache key: "article:{articleId}:{version}"
  - Invalidate when article is edited

User preferences: Cache 30 min in Redis
  - Cache key: "user:prefs:{userId}"
  - Invalidate on preference update

Images/Photos: Cache indefinitely in CloudFront
  - Use content hash in filename for cache busting
  - article-{hash}.jpg → change filename when image changes

Comment counts: Cache 1 min with Redis (frequent writes)
  - Use Redis INCR for atomic increments (no race condition)
```

---

### Problem 2: Your Redis cache is consuming 8GB of 10GB memory. What do you do?

**Solution:**
1. **Audit:** `redis-cli --stat` and `redis-cli MEMORY DOCTOR` to find big keys
2. **Reduce TTLs:** Are some keys cached too long? Shorten TTL.
3. **Use better data types:** Store `HSET` (hash) instead of JSON strings — more memory efficient
4. **Eviction policy:** Set `maxmemory-policy allkeys-lru` — Redis auto-removes old keys
5. **Compress values:** Compress large JSON values before storing
6. **Scale Redis:** Use Redis Cluster (multiple nodes) or upgrade to larger instance in ElastiCache
7. **Two-tier cache:** Keep only hot data in Redis, less popular in a larger but slower memcache tier

---

### Navigation
**Prev:** [04_Load_Balancing.md](04_Load_Balancing.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [06_Database_Basics.md](06_Database_Basics.md)
