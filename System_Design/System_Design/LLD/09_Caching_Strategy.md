# 📌 Caching Strategy (LLD)

## 🧠 Concept Explanation (Story Format)

Your API gets 10,000 requests per second for "Show trending posts." Without caching, that's 10,000 database queries per second — your database crashes.

With caching: First request hits the database (50ms). Result stored in Redis. Next 9,999 requests? All served from Redis in 1ms. Database sees 1 query/5 minutes instead of 10,000/second.

---

## 🔍 Key Caching Patterns

### 1. Cache-Aside (Lazy Loading)

```javascript
class PostCache {
  constructor(redis, db) {
    this.redis = redis;
    this.db = db;
    this.TTL = 300; // 5 minutes
  }
  
  async getPost(postId) {
    const cacheKey = `post:${postId}`;
    
    // 1. Check cache
    const cached = await this.redis.get(cacheKey);
    if (cached) {
      return { ...JSON.parse(cached), _source: 'cache' };
    }
    
    // 2. Cache miss — fetch from DB
    const post = await this.db.query('SELECT * FROM posts WHERE id = $1', [postId]);
    if (!post.rows[0]) return null;
    
    // 3. Store in cache
    await this.redis.setex(cacheKey, this.TTL, JSON.stringify(post.rows[0]));
    
    return { ...post.rows[0], _source: 'database' };
  }
  
  async invalidatePost(postId) {
    await this.redis.del(`post:${postId}`);
  }
  
  // Batch get (reduces N+1 queries!)
  async getPosts(postIds) {
    // Pipeline all cache reads
    const pipeline = this.redis.pipeline();
    postIds.forEach(id => pipeline.get(`post:${id}`));
    const cacheResults = await pipeline.exec();
    
    // Identify misses
    const misses = postIds.filter((id, i) => !cacheResults[i][1]);
    
    // Fetch misses from DB
    let dbResults = [];
    if (misses.length > 0) {
      const result = await this.db.query('SELECT * FROM posts WHERE id = ANY($1)', [misses]);
      dbResults = result.rows;
      
      // Cache the fetched posts
      const setPipeline = this.redis.pipeline();
      dbResults.forEach(post => {
        setPipeline.setex(`post:${post.id}`, this.TTL, JSON.stringify(post));
      });
      await setPipeline.exec();
    }
    
    // Merge cache hits + DB results in original order
    const dbMap = Object.fromEntries(dbResults.map(p => [p.id, p]));
    return postIds.map((id, i) => {
      const cached = cacheResults[i][1];
      return cached ? JSON.parse(cached) : dbMap[id] || null;
    });
  }
}
```

### 2. Write-Through Cache

```javascript
class UserService {
  constructor(redis, db) {
    this.redis = redis;
    this.db = db;
  }
  
  async updateUser(userId, updates) {
    // 1. Update database
    const result = await this.db.query(
      'UPDATE users SET name = $1, bio = $2, updated_at = NOW() WHERE id = $3 RETURNING *',
      [updates.name, updates.bio, userId]
    );
    
    const updatedUser = result.rows[0];
    
    // 2. IMMEDIATELY update cache (write-through)
    await this.redis.setex(`user:${userId}`, 600, JSON.stringify(updatedUser));
    
    return updatedUser;
  }
  
  async createUser(userData) {
    const result = await this.db.query(
      'INSERT INTO users (name, email, password_hash) VALUES ($1, $2, $3) RETURNING *',
      [userData.name, userData.email, userData.passwordHash]
    );
    
    const user = result.rows[0];
    
    // Write to cache on creation too
    await this.redis.setex(`user:${user.id}`, 600, JSON.stringify(user));
    
    return user;
  }
}
```

### 3. Cache Stampede Prevention

```javascript
// Problem: Cache expires → 1000 requests all hit DB simultaneously!
// Solution: Mutex lock — only one request rebuilds the cache

class StampedePreventionCache {
  constructor(redis) {
    this.redis = redis;
  }
  
  async get(key, fetchFn, ttl = 300) {
    // Try cache first
    const cached = await this.redis.get(key);
    if (cached) return JSON.parse(cached);
    
    // Try to acquire lock (mutex)
    const lockKey = `lock:${key}`;
    const lockValue = crypto.randomUUID();
    const acquired = await this.redis.set(lockKey, lockValue, 'NX', 'EX', 30); // NX = only if not exists
    
    if (acquired) {
      // We have the lock — fetch and cache
      try {
        const data = await fetchFn();
        await this.redis.setex(key, ttl, JSON.stringify(data));
        return data;
      } finally {
        // Only release our lock (not someone else's)
        const currentLock = await this.redis.get(lockKey);
        if (currentLock === lockValue) await this.redis.del(lockKey);
      }
    } else {
      // Another process is fetching — wait and poll
      for (let i = 0; i < 10; i++) {
        await new Promise(r => setTimeout(r, 100)); // Wait 100ms
        const result = await this.redis.get(key);
        if (result) return JSON.parse(result);
      }
      
      // If still no cache after waiting — fetch directly (fallback)
      return fetchFn();
    }
  }
}

// Usage
const cache = new StampedePreventionCache(redis);
const trendingPosts = await cache.get(
  'trending:posts',
  () => db.query('SELECT * FROM posts ORDER BY score DESC LIMIT 20'),
  60 // 1 minute TTL
);
```

### 4. Cache Key Design

```javascript
// Structured cache keys — consistent, predictable, easy to invalidate

class CacheKeyBuilder {
  static user(userId) { return `user:${userId}`; }
  static userFeed(userId) { return `feed:user:${userId}`; }
  static post(postId) { return `post:${postId}`; }
  static postLikes(postId) { return `post:${postId}:likes`; }
  static trending(period = 'day') { return `trending:${period}`; }
  static search(query, page) { return `search:${Buffer.from(query).toString('base64')}:${page}`; }
  static rateLimit(userId, endpoint) { return `ratelimit:${userId}:${endpoint}`; }
  static session(sessionId) { return `session:${sessionId}`; }
  
  // Pattern-based invalidation
  static userPattern(userId) { return `*:user:${userId}:*`; }
}

// Invalidate all cache for a user
async function invalidateUserCache(userId) {
  const patterns = [
    CacheKeyBuilder.user(userId),
    CacheKeyBuilder.userFeed(userId),
    // Can't use KEYS * in production (blocks Redis!) — use SCAN instead
  ];
  
  const pipeline = redis.pipeline();
  patterns.forEach(key => pipeline.del(key));
  await pipeline.exec();
  
  // Scan for pattern-based deletion (production-safe)
  const stream = redis.scanStream({ match: `user:${userId}:*`, count: 100 });
  stream.on('data', (keys) => {
    if (keys.length) redis.del(...keys);
  });
}
```

### 5. TTL Strategy

```javascript
// Different TTLs for different data types
const TTL_CONFIG = {
  // User data — changes rarely, cache longer
  user_profile: 10 * 60,           // 10 minutes
  user_session: 24 * 60 * 60,      // 24 hours
  
  // Content — can change, cache shorter
  post: 5 * 60,                    // 5 minutes
  comment_list: 2 * 60,            // 2 minutes
  
  // Dynamic data — changes frequently
  trending_posts: 60,              // 1 minute
  live_scoreboard: 30,             // 30 seconds
  
  // Computed data — expensive to compute, cache longer
  user_recommendation: 30 * 60,   // 30 minutes
  
  // Rate limiting — precise windows
  rate_limit_minute: 60,
  rate_limit_hour: 3600,
};

// Jitter to prevent synchronized cache expiry
function ttlWithJitter(baseTtl, jitterPercent = 0.1) {
  const jitter = Math.random() * baseTtl * jitterPercent;
  return Math.floor(baseTtl + jitter);
  // Instead of all "user_profile" caches expiring at exactly same time →
  // They expire across 10 second window → smoother DB load
}

await redis.setex(key, ttlWithJitter(TTL_CONFIG.user_profile), JSON.stringify(data));
```

### 6. Redis Data Structures for Specific Use Cases

```javascript
// Sorted Set — Leaderboard / Top N
async function addScore(userId, score) {
  await redis.zadd('leaderboard', score, userId);
}

async function getTopUsers(count = 10) {
  // Get top N with scores, sorted desc
  const results = await redis.zrevrangebyscore('leaderboard', '+inf', '-inf', 'WITHSCORES', 'LIMIT', 0, count);
  // Returns: [userId1, score1, userId2, score2, ...]
  const leaderboard = [];
  for (let i = 0; i < results.length; i += 2) {
    leaderboard.push({ userId: results[i], score: parseFloat(results[i + 1]) });
  }
  return leaderboard;
}

// Set — User online status
async function setOnline(userId) {
  await redis.sadd('online_users', userId);
  await redis.expire('online_users', 300); // Auto-clean after 5 min inactivity
}

async function isOnline(userId) {
  return redis.sismember('online_users', userId);
}

async function getOnlineCount() {
  return redis.scard('online_users');
}

// HyperLogLog — Approximate unique count (very memory efficient!)
async function trackPageView(page, userId) {
  await redis.pfadd(`pageviews:${page}:${new Date().toDateString()}`, userId);
}

async function getUniqueViewers(page) {
  return redis.pfcount(`pageviews:${page}:${new Date().toDateString()}`);
  // 12KB memory for MILLIONS of unique users! (±0.81% error rate)
}

// Geo — Location-based queries
async function updateDriverLocation(driverId, lng, lat) {
  await redis.geoadd('drivers', lng, lat, driverId);
}

async function getNearbyDrivers(lng, lat, radiusKm = 5) {
  return redis.georadius('drivers', lng, lat, radiusKm, 'km', 'WITHCOORD', 'WITHDIST', 'COUNT', 10, 'ASC');
}
```

---

## ⚖️ Trade-offs

| Strategy | Best For | Drawback |
|---------|---------|---------|
| Cache-Aside | Read-heavy, intermittent misses | Cache miss latency |
| Write-Through | Write-heavy, consistency critical | Extra write latency |
| Write-Behind | Very high write throughput | Risk of data loss |
| Read-Through | Transparent caching | Complex to implement |

---

## 💼 Interview Questions (WITH SOLUTIONS)

### Q1: What is cache invalidation and why is it "hard"?

**Solution:**
Cache invalidation = removing or updating stale cache entries when the underlying data changes.

Why hard:
1. **Distributed caches:** Multiple cache servers — how do you invalidate ALL of them?
2. **Cascade invalidation:** Invalidating one object may need to invalidate others (user changes name → all their posts show wrong author name)
3. **Race conditions:** Cache invalidated → 1000 requests → all hit DB → cache updated multiple times
4. **TTL vs Event-based:** TTL is simple but can serve stale data. Event-based is accurate but complex.

Phil Karlton quote: "There are only two hard things in Computer Science: cache invalidation and naming things."

Common strategies:
- **TTL:** Let cache expire. Good for tolerating stale data.
- **Write-through:** Update cache on every write. Consistent but every write hits cache.
- **Event-based:** Listen for change events, invalidate specific keys. Precise but complex.

### Q2: How do you prevent cache stampede?

**Solution:**
Cache stampede: Cache for a popular item expires → many simultaneous requests → all hit DB simultaneously → DB overloaded.

Prevention strategies:
1. **Mutex lock:** Only one request fetches from DB. Others wait and use result.
2. **Probabilistic early expiration:** Randomly refresh cache before it expires: `if (Math.random() < staleness) refetch()`
3. **TTL Jitter:** Add random offset to TTL so caches don't all expire at same time
4. **Stale-while-revalidate:** Serve stale cache while one request refreshes in background
5. **Request coalescing:** Queue duplicate requests for the same cache key, serve one DB response to all

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem: Design a caching layer for a social media feed

```javascript
class FeedCache {
  constructor(redis, db) {
    this.redis = redis;
    this.db = db;
  }
  
  async getUserFeed(userId, { cursor, limit = 20 } = {}) {
    const cacheKey = `feed:${userId}:${cursor || 'latest'}:${limit}`;
    
    // Try cache (short TTL — feeds change frequently)
    const cached = await this.redis.get(cacheKey);
    if (cached) return JSON.parse(cached);
    
    // Build feed from following list
    const following = await this.redis.smembers(`user:${userId}:following`);
    
    const feed = await this.db.query(
      'SELECT posts.*, users.name as author_name FROM posts JOIN users ON posts.user_id = users.id WHERE posts.user_id = ANY($1) ORDER BY posts.created_at DESC LIMIT $2',
      [following, limit]
    );
    
    // Cache for 30 seconds (feeds need to be fresh-ish)
    await this.redis.setex(cacheKey, 30, JSON.stringify(feed.rows));
    
    return feed.rows;
  }
  
  // Fanout: When user posts, push to followers' feed caches
  async invalidateFollowerFeeds(userId) {
    const followers = await this.redis.smembers(`user:${userId}:followers`);
    
    if (followers.length > 1000) {
      // Big celebrity? Don't fanout — pull model instead (Twitter approach)
      return;
    }
    
    // Small accounts: fanout to all follower caches
    const pipeline = this.redis.pipeline();
    followers.forEach(followerId => {
      pipeline.del(`feed:${followerId}:latest:20`);
    });
    await pipeline.exec();
  }
}
```

---

### Navigation
**Prev:** [08_API_Design_LLD.md](08_API_Design_LLD.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [10_Concurrency_and_Async.md](10_Concurrency_and_Async.md)
