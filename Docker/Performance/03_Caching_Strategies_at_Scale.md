# 📌 Topic: Caching Strategies at Scale (Redis and CDN)

## 🧠 Concept Explanation (Basic → Expert)
**Basic**: Caching is about saving a "copy" of slow data in a fast place. Redis is a fast "In-memory" database for your app. A CDN is a fast "Global" network for your static files.
**Expert**: At scale, caching is a **Multi-layered Data Hierarchy**. Staff-level engineering requires a "Cache-First" mindset to protect the primary database from being overwhelmed (the **Database Hammering** problem). This involves implementing **Cache-Aside**, **Write-Through**, and **Read-Through** patterns. You must also manage **Cache Invalidation** (the hardest problem in CS), ensuring that when data changes, the cache is updated or deleted across all global nodes simultaneously to prevent "Stale Data" bugs.

## 🏗️ Mental Model
- **Primary DB**: The central library. Huge collection, but slow to find a specific book.
- **Redis (L1/L2 Cache)**: A bookshelf in your office. Small collection, but you can reach it in seconds.
- **CDN (Edge Cache)**: A local bookstore in every city. They have the bestsellers (popular data) ready for immediate pickup so you don't have to wait for a delivery from the central library.

## ⚡ Actual Behavior
- **Latency Difference**: 
  - DB Query: 50ms - 200ms.
  - Redis Get: < 1ms.
  - CDN Edge: < 10ms.
- **Throughput**: One Redis container can handle 100,000+ requests per second, far exceeding what a traditional relational database (Postgres/MySQL) can handle.

## 🔬 Internal Mechanics (The Cache Layers)
1. **Application Cache**: In-memory (RAM) inside your Node.js/Go process. (Fastest, but reset on container restart).
2. **Distributed Cache (Redis)**: Shared by all container replicas. Persists across restarts.
3. **Database Cache**: The internal buffer pool of Postgres/MySQL.
4. **Edge Cache (CDN)**: Caching at the HTTP layer based on `Cache-Control` headers.

## 🔁 Execution Flow (Cache-Aside Pattern)
1. App receives request for `User:123`.
2. App checks Redis: `GET user:123`.
3. **Cache Hit**: Redis returns data. App returns to user. (Duration: 2ms).
4. **Cache Miss**: Redis returns `null`. 
5. App queries Postgres: `SELECT * FROM users WHERE id=123`.
6. App stores result in Redis: `SETEX user:123 3600 <data>`.
7. App returns to user. (Duration: 100ms).

## 🧠 Resource Behavior
- **Memory**: Redis stores EVERYTHING in RAM. If you don't set an **Eviction Policy** (like `allkeys-lru`), Redis will crash when the container hits its memory limit.
- **Network**: Heavy caching can saturate the internal "Back-tier" network between your App and Redis containers.

## 📐 ASCII Diagrams (REQUIRED)

```text
       SCALED CACHING ARCHITECTURE
       
[ USER ] --( 1 )--> [ CDN / EDGE ] --( Hit! )--> [ USER ]
      |                   |
 ( Miss! )           ( 2: Forward )
      |                   |
      v                   v
[ LOAD BALANCER ] --> [ APP CONTAINER ]
                             |
                   +---------+---------+
                   |                   |
             [ REDIS (L1) ]      [ DATABASE (L2) ]
              ( RAM - Fast )      ( Disk - Slow )
```

## 🔍 Code (Configuring Redis Eviction)
```bash
# redis.conf
# Limit memory to 2GB
maxmemory 2gb
# When full, remove the 'Least Recently Used' keys automatically
maxmemory-policy allkeys-lru

# Docker: Run with a memory limit
docker run -d --name cache --memory 2.5g redis redis-server /path/to/redis.conf
```

## 💥 Production Failures
- **The "Cache Avalanche"**: You set the same TTL (Time To Live) for 1 million keys. At exactly 12:00 PM, all 1 million keys expire. 1 million requests hit the Database at the same time. The DB crashes.
  *Fix*: Add a "Jitter" (Random noise) to your TTLs (e.g., 60 minutes + random 1-5 minutes).
- **The "Stale Data" Bug**: You update a user's profile in the DB but forget to delete the Redis key. The user keeps seeing their old profile for the next hour.

## 🧪 Real-time Q&A
**Q: Should I cache everything?**
**A**: **No.** Caching adds complexity. Only cache data that is: 1. **Frequently Read**. 2. **Slow to Calculate**. 3. **Static** (doesn't change every second). Caching a "Real-time Stock Ticker" is usually a bad idea.

## ⚠️ Edge Cases
- **Cache Penetration**: An attacker requests IDs that don't exist (e.g., `user:99999999`). Redis has a miss, and the request hits the DB. The attacker does this 1,000 times a second to crash the DB.
  *Fix*: Use a **Bloom Filter** or cache the "null" result for a short time.

## 🏢 Best Practices
- **Use Key Namespacing**: `user:profile:123` instead of just `123`.
- **Monitor Hit Ratio**: Aim for > 80%. If it's lower, you are caching the wrong things.
- **Fail Gracefully**: If Redis is down, your app should still work (just slower) by going directly to the DB.

## ⚖️ Trade-offs
| Caching Level | Latency | Data Freshness | Complexity |
| :--- | :--- | :--- | :--- |
| **None** | High | **Perfect** | **Low** |
| **App RAM** | **Lowest** | Poor | Medium |
| **Redis** | Low | Good | High |

## 💼 Interview Q&A
**Q: What is a "Cache Stampede" and how do you prevent it in a high-traffic system?**
**A**: A Cache Stampede (or Dog-piling) occurs when a popular cache key expires and multiple application servers all detect the miss simultaneously. They all then attempt to re-generate the data by hitting the database at the same time. To prevent this, I use **Locking/Mutexes**. The first container to detect the miss acquires a lock (using `SETNX` in Redis) and performs the DB query. All other containers see the lock and wait or return the "stale" version of the data until the first container updates the cache and releases the lock.

## 🧩 Practice Problems
1. Implement a "Cache-Aside" pattern in a simple Node/Express app using a Redis container.
2. Use `redis-cli monitor` to watch the commands hitting your Redis instance in real-time.
3. Simulate a "Cache Miss" storm and observe the spike in Database CPU usage.

---
Prev: [02_Network_Latency_Optimization.md](./02_Network_Latency_Optimization.md) | Index: [00_Index.md](../00_Index.md) | Next: [04_Cold_Start_Reduction.md](./04_Cold_Start_Reduction.md)
---
