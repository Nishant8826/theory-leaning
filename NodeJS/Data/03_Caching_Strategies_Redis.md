# 📌 03 — Caching Strategies (Redis): Latency vs Consistency

## 🧠 Concept Explanation

### Basic → Intermediate
Caching is the process of storing copies of data in a high-speed storage layer (usually RAM) to handle future requests faster. Redis is the most popular in-memory data store for Node.js.

### Advanced → Expert
At a staff level, caching is a trade-off between **Performance** and **Consistency**. 
1. **Cache-Aside (Lazy Loading)**: App checks cache ──▶ miss ──▶ load from DB ──▶ update cache. Most common.
2. **Write-Through**: App writes to cache ──▶ cache updates DB. Consistent, but slower writes.
3. **Write-Behind (Write-Back)**: App writes to cache ──▶ app continues ──▶ cache updates DB eventually. Extremely fast, but risk of data loss.

The "Cache Invalidation" problem is the hardest part: **"There are two hard things in computer science: cache invalidation and naming things."**

---

## 🏗️ Common Mental Model
"I'll just cache everything for 1 hour."
**Correction**: Not all data is equal. Some data (User Profile) can be stale for a minute, while other data (Stock Inventory) must be highly consistent. Use different TTLs (Time To Live) and invalidation patterns for different data types.

---

## ⚡ Actual Behavior: Cache Stampede
When a popular cache key expires, thousands of concurrent requests might all see a "miss" and hit the database simultaneously to re-populate the cache. This can crash your database.
**Fix**: Use **Mutual Exclusion (Mutex)** or **Soft Expiration** (where the first request to see an expired key returns the stale data but triggers an async refresh).

---

## 🔬 Internal Mechanics (Redis Data Structures)

### Beyond Key-Value
Redis is a **Data Structure Server**.
- **Hashes**: Perfect for storing user objects.
- **Sorted Sets (ZSETs)**: Ideal for leaderboards or priority queues.
- **Bitmaps**: For massive analytics (e.g. "Unique users today").
- **Pub/Sub**: For real-time messaging between Node.js instances.

---

## 📐 ASCII Diagrams

### Cache-Aside Pattern
```text
  1. GET /user/123
     │
     ▼
  2. [ REDIS.GET(123) ] ─── Found? ───▶ [ RETURN DATA ]
     │                                     ▲
     └─ No (Miss)                          │
        │                                  │
        ▼                                  │
  3. [ DB.QUERY(123) ] ──▶ 4. [ REDIS.SET(123) ]
```

---

## 🔍 Code Example: Smart Cache with TTL
```javascript
const Redis = require('ioredis');
const redis = new Redis();

async function getUser(id) {
  const cacheKey = `user:${id}`;
  
  // 1. Try Cache
  const cached = await redis.get(cacheKey);
  if (cached) return JSON.parse(cached);
  
  // 2. Try DB
  const user = await db.users.findById(id);
  
  // 3. Update Cache with TTL (30 minutes)
  if (user) {
    await redis.set(cacheKey, JSON.stringify(user), 'EX', 1800);
  }
  
  return user;
}
```

---

## 💥 Production Failures & Debugging

### Scenario: The Cache Inconsistency
**Problem**: A user updates their profile, but the site still shows the old name.
**Reason**: You updated the database but forgot to delete the Redis key. Or, the cache has a 24-hour TTL and no invalidation logic.
**Fix**: Use the **Cache-Aside** pattern and always delete the key after a DB update.

### Scenario: Redis OOM (Maxmemory Policy)
**Problem**: Redis is using 100% of its RAM and starts throwing errors.
**Reason**: You are storing more data than fits in memory.
**Fix**: Configure a `maxmemory-policy`. Use `allkeys-lru` (Least Recently Used) so Redis automatically deletes old data to make room for new data.

---

## 🧪 Real-time Production Q&A

**Q: "Should I cache the database result or the final API JSON?"**
**A**: **Cache the Database result**. This allows you to reuse the cache for different API endpoints or internal logic. Only cache the final API JSON (Edge Caching) if the endpoint is extremely high traffic and the payload is identical for all users.

---

## 🏢 Industry Best Practices
- **Namespace your keys**: Use `v1:user:123` so you can clear versions of your data easily.
- **Avoid "KEYS *"**: Never use the `KEYS` command in production; it is $O(N)$ and blocks the single-threaded Redis process. Use `SCAN` instead.

---

## 💼 Interview Questions
**Q: What is a "Hot Key" problem in Redis?**
**A**: A Hot Key is a single key that is requested millions of times per second (e.g. a celebrity's profile). Even with Redis's speed, a single key can hit the network limit of the Redis node. Solution: Use **Local In-Memory Cache** (in Node.js) as a first layer for extremely hot keys.

---

## 🧩 Practice Problems
1. Implement a "Global Rate Limiter" using Redis `INCR` and `EXPIRE`.
2. Build a "Search Autocomplete" using Redis Sorted Sets (`ZSET`).

---

**Prev:** [02_ORM_vs_Query_Builder.md](./02_ORM_vs_Query_Builder.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [04_Consistency_vs_Availability.md](./04_Consistency_vs_Availability.md)
