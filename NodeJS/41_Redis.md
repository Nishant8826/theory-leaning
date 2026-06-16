# Redis

Disk-based databases (like PostgreSQL or MongoDB) have query latency and limited write throughput. Redis runs entirely in-memory, keeping query latency under 1-2 milliseconds. Knowing how to leverage Redis for caching, session management, and rate limiting is key to building fast, scalable backend systems.

### What is Redis?
**Redis (Remote Dictionary Server)** is an open-source, in-memory key-value data structure store. It is used as a database, cache, message broker, and streaming engine. Because it keeps all data in RAM, read and write operations are extremely fast.

### Core Redis Data Structures
Unlike simple key-value caches that only support text strings, Redis supports several data structures:
* **Strings**: The most basic key-value type (binary-safe strings up to 512MB).
* **Hashes**: Maps between string fields and string values, ideal for representing objects (e.g. `user:101 -> name: "Bob", role: "admin"`).
* **Lists**: Lists of strings sorted by insertion order. Useful for building message queues.
* **Sets**: Unordered collections of unique strings. Ideal for tracking unique events or tags.
* **Sorted Sets (ZSET)**: Non-repeating collections of strings, where every member is associated with a numeric score. The members are kept sorted by their scores, making them ideal for high-performance leaderboards.

## Deep Dive

### Node.js Redis Connection Management
To interact with Redis, Node.js applications use clients like `redis` (official client) or `ioredis` (a robust, feature-rich alternative).
* **Single Connection**: Because Redis is single-threaded, a single TCP connection is often sufficient to handle thousands of operations per second.
* **Non-blocking Execution**: In Node.js, calls to the Redis client are asynchronous. Node passes commands down the TCP socket, and handles responses via the event loop as they arrive from Redis.

## Visual Explanation

### Caching Strategy with Redis (Read-Aside)
```text
  [ Client Request: GET /api/users/42 ]
                   │
                   ▼
     [ Check Cache: GET user:42 ] ── Redis lookup ──> [ Found in Redis? ]
                                                            ├── YES ──> Return user JSON (Cache Hit - 1ms)
                                                            │
                                                            └── NO  ──> [ Cache Miss ]
                                                                             │
                                                                             ▼ (Fetch from DB)
                                                                    [ PostgreSQL / MongoDB ]
                                                                             │
                                                                             ▼ (Save back to cache)
                                                                    [ SETEX user:42 3600 ]
                                                                             │
                                                                             ▼
                                                                    [ Return response ]
```

## Real-World Example
Consider a rate-limiting system. You want to restrict users to 100 requests per minute. You store a Redis string key containing the user's IP address and a numeric value representing their request count. Every time the user sends a request, you run the `INCR` command in Redis and set an expiration time of 60 seconds. If the counter exceeds 100, you reject the request instantly, protecting your servers from overload.

## Code Examples

### Redis Client Configuration and Core Data Structures Demo

```javascript
// db/redisClient.js
// Dependency required: npm install redis
const { createClient } = require('redis');

const REDIS_URL = process.env.REDIS_URL || 'redis://localhost:6379';

const redisClient = createClient({ url: REDIS_URL });

redisClient.on('connect', () => console.log('Successfully connected to Redis.'));
redisClient.on('error', (err) => console.error('Redis client error:', err.message));

// Initialize connection once during startup
const connectRedis = async () => {
  if (!redisClient.isOpen) {
    await redisClient.connect();
  }
  return redisClient;
};

module.exports = { redisClient, connectRedis };
```

```javascript
// redis-data-types.js
const { connectRedis, redisClient } = require('./db/redisClient');

async function runRedisDemo() {
  await connectRedis();

  try {
    // 1. STRINGS (Basic Key-Value with Expiration)
    // Set a key with a Time-to-Live (TTL) of 10 seconds
    await redisClient.set('cache:key:user_1', 'Alice', { EX: 10 });
    const userVal = await redisClient.get('cache:key:user_1');
    console.log('GET String Value:', userVal); // 'Alice'

    // 2. HASHES (Storing Objects)
    const userHashKey = 'user:profile:101';
    await redisClient.hSet(userHashKey, {
      name: 'Bob',
      role: 'admin',
      loginCount: '12'
    });
    
    // Set field expiration if using Redis 7.4+, or read entire hash
    const profile = await redisClient.hGetAll(userHashKey);
    console.log('GET Hash Object:', profile);
    /* Output: { name: 'Bob', role: 'admin', loginCount: '12' } */

    // 3. LISTS (Queue mechanics: Left Push, Right Pop)
    const queueKey = 'tasks:queue';
    await redisClient.lPush(queueKey, 'task_id_1');
    await redisClient.lPush(queueKey, 'task_id_2');
    
    // Pop task from the end of the queue
    const nextTask = await redisClient.rPop(queueKey);
    console.log('Dequeued Task:', nextTask); // 'task_id_1'

    // 4. SORTED SETS (Leaderboards)
    const leaderboardKey = 'leaderboard:players';
    await redisClient.zAdd(leaderboardKey, [
      { score: 250, value: 'player_alex' },
      { score: 500, value: 'player_sarah' },
      { score: 100, value: 'player_john' }
    ]);

    // Query top players in descending order
    const topPlayers = await redisClient.zRangeWithScores(leaderboardKey, 0, -1, {
      REV: true
    });
    console.log('Sorted Leaderboard (Top Scores):', topPlayers);

    // Clean up demo keys
    await redisClient.del(['cache:key:user_1', userHashKey, queueKey, leaderboardKey]);
    console.log('Demo cleanup completed.');

  } catch (err) {
    console.error('Error during Redis operations:', err.message);
  } finally {
    await redisClient.disconnect();
  }
}
runRedisDemo();
```

## Best Practices
* **Always Set TTLs on Caches**: Always configure a Time-To-Live (TTL) expiration using `EXPIRE` or `set(key, value, { EX })` on all cache entries to prevent stale data from lingering and to manage memory usage.
* **Use Namespace Colon Formatting**: Organize your Redis keys using colons to create namespaces (e.g. `user:101:profile` or `order:5005:status`) for easier management and querying.
* **Monitor Memory Consumption**: Redis stores all data in memory. Monitor Redis memory limits and configure eviction policies (like `allkeys-lru` - Least Recently Used) to prevent Out of Memory errors.

## Interview Questions

**Q:** What is Redis and why is it faster than standard databases like PostgreSQL or MongoDB?

> **Answer:**
> Redis is an in-memory key-value data structure store. It is faster because it holds all data in RAM, eliminating disk write and read latency, which keeps operations under 1-2 milliseconds.

**Q:** Name three data structures supported by Redis and describe a real-world use case for each.

> **Answer:**
> 1. **Strings**: Storing standard user session tokens or cached JSON outputs with an expiration time.
> 2. **Hashes**: Storing structured objects, like a user profile containing fields for name, role, and email.
> 3. **Lists**: Building simple message queues using Left-Push (`lPush`) and Right-Pop (`rPop`) operations.

**Q:** Explain the difference between Redis RDB (Redis Database) and AOF (Append Only File) persistence mechanisms. What are the performance trade-offs?

> **Answer:**
> Redis provides two persistence options:

**Q:** RDB

> **Answer:**
> * *Pros*: Highly optimized for fast restarts; minimal impact on write performance.
> * *Cons*: If Redis crashes, data written since the last snapshot is lost.

**Q:** AOF

> **Answer:**
> * *Pros*: Highly durable; minimal data loss if Redis crashes.
> * *Cons*: Slower write performance due to continuous disk writes, and generates larger log files.
> * *Trade-off*: High-performance caching layers often disable persistence entirely. Hybrid configurations use both RDB and AOF to balance speed and durability.

**Q:** How would you architecture a distributed locking mechanism using Redis (Redlock algorithm) to prevent race conditions when updating inventory in a scaled multi-instance Node.js cluster?

> **Answer:**
> To implement a distributed lock using Redis:
> 1. Define a unique lock key (e.g. `lock:inventory:product_id`).
> 2. Attempt to acquire the lock using the atomic `SET` command with options:
> ```javascript
> const acquired = await redisClient.set(lockKey, uniqueToken, {
> NX: true, // Only set the key if it does not already exist
> PX: 5000  // Set a millisecond expiration (5 seconds) to prevent deadlocks
> });
> ```
> 3. If `acquired === 'OK'`, the server holds the lock and can safely update the inventory database.
> 4. If the server fails to acquire the lock, implement a retry back-off loop before attempting again.
> 5. Once the database update is complete, release the lock by deleting the key. To do this safely, run a Lua script to verify that the value stored in the lock matches the server's `uniqueToken` before deleting it, preventing the server from accidentally deleting a lock held by another process if the operation took longer than the TTL.

---
Previous : [40_ORM_Concepts.md](40_ORM_Concepts.md) | Index : [00_index.md](00_index.md) | Next : [42_Caching.md](42_Caching.md)
