# 📈 Caching Strategies

## 📌 Topic Name
Distributed Caching: ElastiCache (Redis/Memcached) and DAX

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Store frequently accessed data in memory so you don't have to go to the slow database every time.
*   **Expert**: Caching is a **Performance and Cost Optimization Strategy** that reduces database load and provides microsecond latency. It involves choosing the right engine (**Redis** for data structures and persistence, **Memcached** for simplicity and multi-threading) and the right pattern (**Lazy Loading** vs. **Write-Through**). A Staff engineer uses caching to solve "Hot Key" issues in DynamoDB (via **DAX**) and to handle session state in distributed web tiers.

## 🏗️ Mental Model
Think of Caching as a **Chef's Mise en Place**.
- **The Database**: The pantry (Huge, organized, but far away).
- **The Cache**: The small bowls on the counter (Right in front of you, very fast to grab, but small).
- **Cache Hit**: The ingredient is in the bowl.
- **Cache Miss**: You have to walk to the pantry (Latency!).

## ⚡ Actual Behavior
- **Latency**: <1ms (In-memory) vs. 5-10ms (SSD-based DB).
- **Throughput**: Millions of requests per second per node.
- **Eviction**: When the cache is full, it automatically deletes old data (usually **LRU** - Least Recently Used).

## 🔬 Internal Mechanics
1.  **Lazy Loading (Cache-Aside)**:
    - App checks Cache.
    - If Miss, App reads from DB.
    - App writes result back to Cache.
    - (Pros: Only requested data is cached. Cons: Cache miss penalty on first read).
2.  **Write-Through**:
    - App writes to Cache.
    - Cache (or App) updates the DB.
    - (Pros: Data is always fresh. Cons: Write penalty).
3.  **DynamoDB Accelerator (DAX)**: A managed, write-through cache that sits *in front* of DynamoDB. It’s API-compatible, meaning you don't have to change your code logic; you just change the client.

## 🔁 Execution Flow (Lazy Loading)
1.  **Request**: `GET /user/123`.
2.  **Cache Check**: `redis.get("user:123")` -> `null` (Miss).
3.  **Database**: `SELECT * FROM users WHERE id=123` -> `{name: "Alice"}`.
4.  **Populate**: `redis.setex("user:123", 3600, "{name: 'Alice'}")` (Set with 1 hour TTL).
5.  **Response**: Return User to client.
6.  **Next Request**: `redis.get("user:123")` -> `Hit!` (returns instantly).

## 🧠 Resource Behavior
- **Redis Clusters**: Supports **Pub/Sub**, **Sorted Sets**, and **High Availability** (via Replication Groups and Multi-AZ).
- **Memcached**: Purely a key-value store. It is multi-threaded, meaning it can handle more concurrent requests on a single large instance than the single-threaded Redis.

## 📐 ASCII Diagrams
```text
[ APP ] ----(1) Check Cache----> [ ElastiCache ]
  |                                  |
  | (2) If Miss, Call DB             | (3) Return Result
  |                                  |
[ RDS / DYNAMODB ] <-----------------+
```

## 🔍 Code / IaC (ElastiCache Redis)
```hcl
resource "aws_elasticache_replication_group" "redis" {
  replication_group_id          = "prod-redis"
  replication_group_description = "Redis for sessions"
  node_type                     = "cache.t4g.micro"
  num_cache_clusters            = 2 # 1 Primary + 1 Replica
  port                          = 6379
  parameter_group_name          = "default.redis7"
  automatic_failover_enabled    = true
  multi_az_enabled              = true
  
  subnet_group_name = aws_elasticache_subnet_group.main.name
}
```

## 💥 Production Failures
1.  **Cache Stampede (Thundering Herd)**: A high-traffic key (e.g., "HomePageData") expires. 1,000 simultaneous requests see a "Cache Miss" and all hit the database at the same time, crashing it. **Solution**: Use random TTLs or background "soft" refreshes.
2.  **Dirty Reads**: You update the database but forget to update (or invalidate) the cache. Users see old data for the duration of the TTL.
3.  **Out of Memory (OOM)**: The cache fills up, and the eviction policy is set to "No Eviction." The cache starts rejecting new writes, breaking the application.

## 🧪 Real-time Q&A
*   **Q**: When should I use Redis vs. Memcached?
*   **A**: Use **Redis** 99% of the time (Data structures, Persistence, HA). Use **Memcached** only if you have a massive, simple key-value workload that needs to scale vertically across many CPU cores.
*   **Q**: What is a "TTL"?
*   **A**: Time To Live. The amount of time an object stays in the cache before being automatically deleted.

## ⚠️ Edge Cases
*   **Local Caching**: Using an in-memory map inside your Lambda/App. Very fast (zero network hop) but "cold" on every new instance and impossible to synchronize across a fleet.
*   **Warm-up**: After a cache reboot or flush, the database will be hit hard until the cache is "warm" again.

## 🏢 Best Practices
1.  **Use TTLs on everything**.
2.  **Monitor "Cache Hit Ratio"**: If it’s < 80%, your cache might be too small or your TTLs too short.
3.  **Choose a High-Entropy Key**: Ensure keys are distributed evenly across the cache cluster nodes.

## ⚖️ Trade-offs
*   **Caching**: Drastically improves speed and reduces DB cost, but adds significant complexity to data consistency and troubleshooting.

## 💼 Interview Q&A
*   **Q**: How do you prevent a "Cache Stampede"?
*   **A**: 1. Use **Locking**: The first request to see a miss takes a "lock" on the key while it fetches from the DB; other requests wait. 2. **Pre-fetching**: A background worker refreshes the cache *before* it expires. 3. **Jitter**: Set random TTLs (e.g., 60s + rand(0,10)) so multiple keys don't expire at the exact same time.

## 🧩 Practice Problems
1.  Implement a "Rate Limiter" using Redis `INCR` and `EXPIRE`.
2.  Compare the latency of a DynamoDB `GetItem` call with and without DAX enabled.

---
Prev: [03_Predictive_Scaling.md](../Scaling/03_Predictive_Scaling.md) | Index: [Docker/00_Index.md](../00_Index.md) | Next: [05_SQS_SNS_Deep_Dive.md](../Scaling/05_SQS_SNS_Deep_Dive.md)
---
