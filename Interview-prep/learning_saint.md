# Learning Saint: Full Stack Developer (Strong Backend + DevOps) Interview Prep Guide

This guide is a highly detailed, production-focused, and comprehensive interview preparation resource targeted at candidates with 3+ years of experience. It covers all core aspects of Backend Engineering, System Design, DevOps, Cloud Computing, and Real-Time Communication systems based on the Learning Saint job requirements.

---


# 1. Node.js Deep Dive

### ❓ Q1. Explain the Node.js Event Loop phases and how the Microtask Queue behaves.
<details>
<summary><b>👀 Show Answer</b></summary>

*   **Detailed Answer:**
    Node.js uses an event-driven, non-blocking I/O model powered by the V8 engine and the **libuv** C library. The Event Loop is composed of 6 main phases that execute in a loop:
    1.  **Timers:** Executes callbacks scheduled by `setTimeout()` and `setInterval()`.
    2.  **Pending Callbacks:** Executes I/O callbacks deferred from the previous loop iteration.
    3.  **Idle, Prepare:** Used internally by libuv.
    4.  **Poll:** Retrieves new I/O events. Node will block here if there are no pending timers/callbacks.
    5.  **Check:** Executes callbacks registered via `setImmediate()`.
    6.  **Close Callbacks:** Executes callbacks for closed connections (e.g., `socket.on('close', ...)`).
    
    **The Microtask Queue** consists of `process.nextTick()` callbacks and Promise resolve/reject callbacks. Crucially, the Microtask Queue is **not** a phase of the Event Loop. Instead, it is executed immediately after the current operation finishes, **between** phases of the event loop. `process.nextTick()` has a higher priority than promises.
*   **Real-world Example:**
    ```javascript
    setTimeout(() => console.log('Timeout'), 0);
    setImmediate(() => console.log('Immediate'));
    Promise.resolve().then(() => console.log('Promise'));
    process.nextTick(() => console.log('NextTick'));
    // Output Order: NextTick -> Promise -> Timeout -> Immediate
    ```
*   **Common Mistakes:**
    *   Assuming that `setTimeout(..., 0)` always executes before `setImmediate()`. In the main module, execution order depends on process performance and CPU load.
    *   Blocking the event loop with synchronous operations (like `fs.readFileSync`), which freezes all other concurrent user connections.
*   **Follow-up Interview Questions:**
    *   What happens if you recursively call `process.nextTick()`? (It starves the event loop, preventing it from proceeding to the next phase).
    *   How does the event loop offload heavy operations to the operating system? (Through the thread pool or OS-level async APIs like epoll/kqueue).

</details>

<hr/>

### ❓ Q2. When would you use Worker Threads vs. the Cluster Module in Node.js?
<details>
<summary><b>👀 Show Answer</b></summary>

*   **Detailed Answer:**
    *   **Cluster Module:** Spawns multiple identical instances of the Node.js process (each running on its own event loop and memory space) that share a single port. It uses round-robin load balancing. It is best for **scaling network-heavy I/O applications** to leverage multi-core CPUs.
    *   **Worker Threads (`worker_threads`):** Spawns light threads within the same process that share memory (using `SharedArrayBuffer`). It is designed for **heavy CPU-bound computational tasks** (e.g., image resizing, cryptography, data compression) to avoid blocking the main event loop thread.
*   **Real-world Example:**
    *   *Cluster:* Clustering an Express API server so 4 processes run on a 4-core server to handle HTTP requests.
    *   *Worker Threads:* Offloading bcrypt password hashing or PDF generation to a worker thread so the API remains responsive.
*   **Common Mistakes:**
    *   Using worker threads for network database requests (this adds thread communication overhead without performance benefits; database queries are asynchronous and handled by libuv's thread pool anyway).
    *   Spawning worker threads dynamically for every request without using a thread pool, which causes massive context-switching overhead.
*   **Follow-up Interview Questions:**
    *   How do Worker Threads communicate with the main thread? (Via `parentPort.postMessage` and `MessageChannel` message passing).
    *   How does the cluster module share the server TCP socket connection? (The master process binds to the port and hands off connections to workers).

</details>

<hr/>

### ❓ Q3. How do Streams & Buffers work, and how do you handle backpressure?
<details>
<summary><b>👀 Show Answer</b></summary>

*   **Detailed Answer:**
    *   **Buffer:** A raw memory allocation (RAM) outside the V8 heap, storing binary data.
    *   **Stream:** A mechanism to read or write data chunk-by-chunk. Types include: Readable, Writable, Duplex (TCP socket), and Transform (zlib, crypto).
    *   **Backpressure:** Occurs when a Readable stream produces data faster than the Writable stream can write it. If unhandled, chunks accumulate in memory, causing a memory leak or crash.
    
    To handle backpressure, Writable streams return `false` from `.write(chunk)` when their internal buffer exceeds `highWaterMark`. The Readable stream should then be paused via `.pause()`. Once the Writable stream clears its buffer, it fires the `'drain'` event, signaling the Readable stream to call `.resume()`. Utilizing `.pipe()` handles this lifecycle automatically.
*   **Real-world Example:**
    Streaming a 5GB video file from disk directly to an HTTP response using `pipe` or the modern `pipeline()` utility (which handles error cleaning):
    ```javascript
    const { pipeline } = require('stream');
    const fs = require('fs');

    app.get('/video', (req, res) => {
      pipeline(
        fs.createReadStream('large_file.mp4'),
        res,
        (err) => { if (err) console.error('Pipeline failed', err); }
      );
    });
    ```
*   **Common Mistakes:**
    *   Loading large files into memory using `fs.readFile()` instead of using streams.
    *   Failing to handle the error event on streams, which leads to unhandled exceptions and process crashes.
*   **Follow-up Interview Questions:**
    *   What is the default `highWaterMark` for streams? (16KB for object mode, 64KB for binary streams).
    *   How does `Transform` stream differ from a Duplex stream? (Transform outputs are computed directly from inputs, like gzip encryption).

</details>

<hr/>

### ❓ Q4. How do you diagnose and resolve Memory Leaks in Node.js?
<details>
<summary><b>👀 Show Answer</b></summary>

*   **Detailed Answer:**
    Memory leaks occur when the V8 garbage collector (GC) cannot reclaim memory because references to unused objects are still reachable.
    
    **Common causes in Node.js:**
    1.  **Global variables:** Unintentional variables attached to the global scope.
    2.  **Closures:** Inner functions keeping outer variables in scope long after execution.
    3.  **Dangling event listeners:** Registering listeners on persistent objects (like `process` or `ee.on(...)`) without removing them on cleanup.
    4.  **Caches:** Storing database query results in an unbounded local object.
    
    **Diagnostics Steps:**
    1.  Run Node with the inspection flag: `node --inspect index.js`.
    2.  Use Chrome DevTools (or tools like `clinic.js` / `heapdump`) to trigger Garbage Collection and take Heap Snapshots at different intervals under load.
    3.  Compare snapshots (using "Comparison" view) to identify which constructors are growing in count.
    4.  Trace the retainer tree to locate where the reference is held.
*   **Real-world Example:**
    A route handler appending user data to an external array for tracking:
    ```javascript
    const requestLog = []; // Leaks memory indefinitely
    app.get('/user', (req, res) => {
      requestLog.push(req.headers); 
      res.sendStatus(200);
    });
    ```
*   **Common Mistakes:**
    *   Confusing high memory usage with a leak (V8 might delay GC runs to optimize CPU performance).
    *   Adding local caching systems without a size limit (TTL/LRU).
*   **Follow-up Interview Questions:**
    *   How does V8's Garbage Collector work? (Uses a generational collector: Scavenge for young generation, Mark-Sweep-Compact for old generation).
    *   What is the default maximum memory limit for a Node.js process? (Depends on the version, typically ~1.4GB on 64-bit systems unless `--max-old-space-size` is adjusted).

</details>

<hr/>

### ❓ Q5. What are Async Hooks, and how can they be used for request tracking?
<details>
<summary><b>👀 Show Answer</b></summary>

*   **Detailed Answer:**
    The `async_hooks` module provides an API to track the lifetime of asynchronous resources created inside a Node.js application.
    
    For request tracking, we use **`AsyncLocalStorage`** (built on top of async hooks). It allows you to store state throughout the lifetime of a web request or any asynchronous execution chain, functioning like Thread-Local Storage (TLS) in multithreaded environments. This is extremely useful for tracing requests with a unique correlation ID across loggers, database calls, and helper utilities without passing the ID as a parameter to every single function.
*   **Real-world Example:**
    Setting a correlation ID in an Express middleware:
    ```javascript
    const { AsyncLocalStorage } = require('async_hooks');
    const asyncLocalStorage = new AsyncLocalStorage();

    app.use((req, res, next) => {
      const correlationId = req.headers['x-correlation-id'] || uuidv4();
      asyncLocalStorage.run({ correlationId }, () => {
        next();
      });
    });

    function logData(message) {
      const store = asyncLocalStorage.getStore();
      console.log(`[Request ID: ${store?.correlationId}] - ${message}`);
    }
    ```
*   **Common Mistakes:**
    *   Using custom async hooks in high-throughput production paths without measuring performance (can introduce CPU execution overhead on resource initialization).
    *   Losing context by accidentally escaping the async context boundaries (e.g., mixing async/await with older legacy callback libraries that lose execution contexts).
*   **Follow-up Interview Questions:**
    *   What are the performance implications of using `AsyncLocalStorage`? (Very low in modern Node.js versions, but custom low-level `async_hooks` tracking init/destroy hooks directly can hit throughput).
    *   How does it maintain context across timers and database connections? (Through libuv's wrapper contexts that propagate active execution details).

</details>

<hr/>

### ❓ Q6. Describe the Node.js Process Lifecycle and how to implement a Graceful Shutdown.
<details>
<summary><b>👀 Show Answer</b></summary>

*   **Detailed Answer:**
    The Node.js process lifecycle starts by initializing the execution stack, reading the entry file, and starting the event loop. The process stays alive as long as there are active event loop items (handles like open ports/sockets, and requests like database timers).
    
    A **Graceful Shutdown** is triggered by receiving OS signals (e.g., `SIGTERM` from Kubernetes, or `SIGINT` from Ctrl+C). It involves:
    1.  Stopping the server from accepting new incoming HTTP/WebSocket connections.
    2.  Allowing currently active requests to finish processing within a timeout period.
    3.  Closing database pools, Redis clients, and file handles.
    4.  Exiting the process cleanly with exit code `0`.
*   **Real-world Example:**
    ```javascript
    const server = app.listen(3000);

    process.on('SIGTERM', () => {
      console.log('SIGTERM signal received. Shutting down gracefully...');
      server.close(async () => {
        console.log('HTTP server closed.');
        try {
          await db.close(); // Close DB connections
          await redis.quit(); // Close Redis connections
          console.log('All resources released.');
          process.exit(0);
        } catch (err) {
          console.error('Error during cleanup', err);
          process.exit(1);
        }
      });
      
      // Force exit if shutdown takes too long (e.g., 10 seconds)
      setTimeout(() => {
        console.error('Forced shutdown due to timeout');
        process.exit(1);
      }, 10000);
    });
    ```
*   **Common Mistakes:**
    *   Immediately calling `process.exit(0)` on `SIGTERM`, which abruptly drops active customer requests.
    *   Forgetting to set a timeout for the shutdown process, which can cause the process to hang forever if a connection remains open.
*   **Follow-up Interview Questions:**
    *   What is the difference between `SIGINT`, `SIGTERM`, and `SIGKILL`? (SIGINT is interrupt, SIGTERM is request to terminate, SIGKILL is forced kill by OS which cannot be intercepted).
    *   What exit code indicates that a Node process terminated due to an uncaught exception? (Exit code 1).

</details>

<hr/>

### ❓ Q7. How do you implement robust Rate Limiting and API Security in Node.js?
<details>
<summary><b>👀 Show Answer</b></summary>

*   **Detailed Answer:**
    Securing a Node.js API requires protection layers at the application and infrastructure level:
    1.  **Rate Limiting:** Protects against DDoS and brute force. Use `express-rate-limit` for simple apps, and a Redis-backed rate limiter (like `rate-limiter-flexible`) for distributed systems to track IP request counts consistently across server instances.
    2.  **HTTP Headers Security:** Use the `helmet` middleware to set essential security headers (e.g., disabling `X-Powered-By`, configuring CSP, HSTS, X-Frame-Options).
    3.  **Input Validation:** Use schema validation libraries like `Zod` or `Joi` to sanitize and validate request bodies, query params, and headers.
    4.  **CORS:** Restrict origin domains via the `cors` middleware.
*   **Real-world Example:**
    Implementing a sliding-window rate limiter with Redis:
    ```javascript
    const { RateLimiterRedis } = require('rate-limiter-flexible');
    const Redis = require('ioredis');
    const redisClient = new Redis({ enableOfflineQueue: false });

    const rateLimiter = new RateLimiterRedis({
      storeClient: redisClient,
      keyPrefix: 'middleware',
      points: 100, // 100 requests
      duration: 60, // per 60 seconds
    });

    const rateLimitMiddleware = (req, res, next) => {
      rateLimiter.consume(req.ip)
        .then(() => next())
        .catch(() => res.status(429).send('Too Many Requests'));
    };
    ```
*   **Common Mistakes:**
    *   Using an in-memory rate limiter in production with multiple autoscaled application instances (the limits won't be synchronized).
    *   Relying on client-side validation alone.
*   **Follow-up Interview Questions:**
    *   How do you prevent SQL/NoSQL injection in a Node.js application? (Use Parameterized queries/ORMs like Mongoose/Sequelize and sanitize input keys).
    *   What are the benefits of using a sliding window algorithm vs. a fixed window for rate limiting? (Prevents traffic bursts at the boundary edge of a new window).

</details>

---


# 2. Database Engineering

### ❓ Q8. Compare MongoDB indexing types and when to use compound indexes.
<details>
<summary><b>👀 Show Answer</b></summary>

*   **Detailed Answer:**
    MongoDB uses indexes to optimize read queries. Types include:
    1.  **Single Field Index:** Created on a single document path.
    2.  **Compound Index:** Created on multiple fields. The order of fields in a compound index is critical. MongoDB searches from left to right.
    3.  **Multikey Index:** Created on fields containing array values, allowing MongoDB to index individual elements within the array.
    4.  **Text Index:** Supports text search queries on string content.
    5.  **Hashed Index:** Indexes hashes of field values, used for hash-based sharding.
    
    **Compound Index Rule (ESR - Equality, Sort, Range):**
    When designing a compound index, arrange fields in this order:
    1.  **Equality:** Fields matched with exact values (e.g., `{ status: "active" }`).
    2.  **Sort:** Fields used to order results (e.g., `{ createdAt: -1 }`).
    3.  **Range:** Fields matched with inequalities (e.g., `{ age: { $gt: 21 } }`).
*   **Real-world Example:**
    If you query: `db.users.find({ status: "active", age: { $gt: 30 } }).sort({ score: -1 })`
    The optimal index is: `{ status: 1, score: 1, age: 1 }` (Equality, Sort, Range).
*   **Common Mistakes:**
    *   Designing compound indexes in the wrong order (e.g., sorting on a range field first, which prevents index sorting).
    *   Creating too many indexes (which slows down insert, update, and delete write operations, as every index must be modified).
*   **Follow-up Interview Questions:**
    *   What is a covered query? (A query where all requested projection fields are part of the index itself, allowing MongoDB to bypass scanning the actual documents).
    *   What is the index overhead limit? (Indexes are stored in RAM; if indexes exceed cache size, MongoDB will swap to disk, degrading performance).

</details>

<hr/>

### ❓ Q9. How do you analyze MongoDB slow queries using Explain Plans and Aggregation?
<details>
<summary><b>👀 Show Answer</b></summary>

*   **Detailed Answer:**
    Slow queries can be identified using the database profiler or MongoDB Atlas alerts. To analyze:
    1.  Append `.explain("executionStats")` to your query.
    2.  Analyze the output JSON:
        *   **`stage`:** Look for `COLLSCAN` (Collection Scan, bad!) vs `IXSCAN` (Index Scan, good!).
        *   **`nReturned`:** Number of documents returned by the query.
        *   **`totalKeysExamined`:** Number of index keys checked. In an optimized query, this should match `nReturned`.
        *   **`totalDocsExamined`:** Number of physical documents loaded from disk. This should be minimal or 0 (if covered query).
    
    For the **Aggregation Pipeline**, we use the `$explain` stage. To optimize aggregations:
    *   Use `$match` and `$sort` stages at the very beginning of the pipeline to utilize indexes.
    *   Use `$project` or `$count` at the end to limit fields sent over the network.
*   **Real-world Example:**
    Analyzing a query without an index:
    ```javascript
    db.orders.find({ userId: "123" }).explain("executionStats");
    // Under executionStats:
    // "stage": "COLLSCAN"
    // "totalDocsExamined": 1000000
    // "nReturned": 5
    // FIX: db.orders.createIndex({ userId: 1 })
    ```
*   **Common Mistakes:**
    *   Running `.explain()` without passing `"executionStats"`, which only shows potential query planner paths without executing the stats collection.
    *   Placing `$match` stages after `$lookup` or `$unwind` stages in aggregation (which forces a full collection scan and joins on all un-filtered records).
*   **Follow-up Interview Questions:**
    *   What is the difference between `COLLSCAN` and `IXSCAN`? (COLLSCAN checks every document in the database; IXSCAN queries the sorted index tree).
    *   How do you optimize a query that has an in-memory sort warning? (Ensure the sort field is part of the index structure).

</details>

<hr/>

### ❓ Q10. Detail MongoDB Transactions, Replication, and Sharding scaling mechanics.
<details>
<summary><b>👀 Show Answer</b></summary>

*   **Detailed Answer:**
    *   **Transactions (ACID):** MongoDB supports multi-document ACID transactions across replica sets and sharded clusters. It uses a session object (`session.startTransaction()`) and requires a WiredTiger storage engine.
    *   **Replication (High Availability):** A **Replica Set** is a group of `mongod` processes that maintain the same data set. Consists of 1 Primary node (receives all writes) and multiple Secondary nodes (replicate primary's oplog). If the Primary dies, an election determines the new Primary.
    *   **Sharding (Horizontal Scaling):** Distributes data across multiple physical machines (shards). Key components:
        *   **Shard:** A physical replica set holding a subset of data.
        *   **Mongos:** Router query interface. Clients connect here.
        *   **Config Database:** Stores metadata configuration about shards.
        *   **Shard Key:** The field used to distribute data. Can be Range-based or Hash-based.
*   **Real-world Example:**
    Selecting a Shard Key: For a global chat app, sharding by `{ tenantId: 1, userId: 1 }` distributes users evenly across databases, avoiding hot shards.
*   **Common Mistakes:**
    *   Choosing a shard key with low cardinality (e.g., status field with 3 values), leading to massive unsplit chunks on a single shard.
    *   Performing multi-document transactions in high-throughput loops (adds locking overhead; schema design should ideally leverage nested documents instead of relations).
*   **Follow-up Interview Questions:**
    *   What is a "hot shard" issue? (When a shard key causes all write traffic to go to a single shard, rendering other shards idle).
    *   What are write concerns (e.g., `w: "majority"`) and read concerns in replica sets? (Write concern defines how many nodes must acknowledge a write before success; read concern defines transaction isolations).

</details>

<hr/>

### ❓ Q11. Compare SQL Joins, Indexing strategies (B-Tree/Hash), and Transaction Isolation Levels.
<details>
<summary><b>👀 Show Answer</b></summary>

*   **Detailed Answer:**
    *   **SQL Joins:**
        *   `INNER JOIN`: Returns matching rows in both tables.
        *   `LEFT JOIN`: Returns all rows from left table, with matching right table rows.
        *   `RIGHT JOIN`: Returns all rows from right table, with matching left table rows.
        *   `FULL JOIN`: Returns rows when there is a match in one of the tables.
    *   **Indexes:**
        *   **B-Tree Index:** Sorted tree structure. Supports equality, range searches, prefix matches, and sorts. (Used by default in PostgreSQL/MySQL).
        *   **Hash Index:** Hash table layout. Extremely fast ($O(1)$) for equality matching (`=`), but does not support range queries (`>`, `<`) or sorting.
    *   **Transaction Isolation Levels (ANSI SQL):**
        1.  **Read Uncommitted:** Can read uncommitted data (allows Dirty Reads).
        2.  **Read Committed:** Prevents Dirty Reads (only reads committed data). Non-repeatable reads can occur (data can change within transaction).
        3.  **Repeatable Read:** Prevents Non-repeatable reads. Phantom reads can occur (new rows can appear). (Default in MySQL InnoDB).
        4.  **Serializable:** Strict lock/ordering. Prevents all anomalies but severely reduces write concurrency. (Default in Postgres when requested).
*   **Real-world Example:**
    Handling bank ledger balances requires the `Serializable` isolation level to prevent concurrency anomalies.
*   **Common Mistakes:**
    *   Joining large unindexed tables (causes nested loop joins that scan millions of rows).
    *   Forgetting that PostgreSQL indexes are not automatically utilized if column data types in the query do not match index definitions.
*   **Follow-up Interview Questions:**
    *   What is a Dirty Read, a Non-repeatable Read, and a Phantom Read? (Dirty: reading uncommitted changes; Non-repeatable: value changes on re-read; Phantom: new rows appear on re-query).
    *   What is MVCC (Multi-Version Concurrency Control)? (A method where database engines keep multiple versions of rows to allow read operations without locking).

</details>

<hr/>

### ❓ Q12. How do you identify and resolve Deadlocks and optimize SQL Queries?
<details>
<summary><b>👀 Show Answer</b></summary>

*   **Detailed Answer:**
    *   **Deadlocks:** Occur when Transaction A locks Row 1 and wants Row 2, while Transaction B locks Row 2 and wants Row 1. The database detects this and terminates one transaction (rollback).
        *   *Resolution:* Acquire locks in the exact same order in all transaction code blocks. Keep transactions short. Use optimistic concurrency control.
    *   **Query Optimization Steps:**
        1.  Use `EXPLAIN ANALYZE <query>`.
        2.  Identify where costs are high (e.g., Seq Scan, Hash Join, Disk Spills).
        3.  Ensure columns used in `WHERE`, `JOIN` conditions, and `ORDER BY` are indexed.
        4.  Avoid `SELECT *` (causes excessive disk/network I/O; select only necessary columns).
        5.  Avoid functions on index columns (e.g., `WHERE YEAR(date_column) = 2026` invalidates the index; use `WHERE date_column >= '2026-01-01'`).
*   **Real-world Example:**
    Resolving deadlocks on stock inventories: Instead of updating rows randomly, sort item IDs in the API layer before executing database updates sequentially.
*   **Common Mistakes:**
    *   Assuming adding more indexes will always make the database faster (every index adds write time overhead).
    *   Not analyzing if the database is using an Index Scan vs a Bitmap Index Scan.
*   **Follow-up Interview Questions:**
    *   What is the difference between `EXPLAIN` and `EXPLAIN ANALYZE`? (Explain shows estimated execution plan cost; explain analyze actually runs the query and records exact timings).
    *   How do you resolve N+1 query problems in ORMs (like Hibernate/Prisma)? (Use eager fetching, join fetches, or select-in batching).

</details>

---

# 3. Redis Deep Dive

### ❓ Q13. Explain Caching Strategies (Cache-Aside, Write-Through) and Cache Invalidation.
<details>
<summary><b>👀 Show Answer</b></summary>

*   **Detailed Answer:**
    Caching boosts read speeds by storing computed data in an in-memory store like Redis.
    
    **Caching Patterns:**
    1.  **Cache-Aside (Lazy Loading):**
        *   App checks cache.
        *   *Hit:* Return data.
        *   *Miss:* Read from DB, write to cache, return.
        *   *Pros:* Cache only stores queried data; DB failures don't crash the app.
        *   *Cons:* Triple-call latency on cache miss.
    2.  **Write-Through:**
        *   App writes directly to cache; cache immediately writes to database.
        *   *Pros:* Data is always fresh in cache.
        *   *Cons:* Write latency is higher because it waits for both writes.
    3.  **Write-Behind (Write-Back):**
        *   App writes to cache; cache queues updates and writes to database asynchronously.
        *   *Pros:* Extremely fast writes.
        *   *Cons:* Risk of data loss if Redis crashes before writing to DB.
    
    **Cache Invalidation & Expiration:**
    *   **TTL (Time-To-Live):** Set key to expire automatically after a set duration.
    *   **Active Invalidation:** Explicitly deleting the Redis key on database updates.
    *   **Eviction Policies:** Under memory limits, Redis evicts keys based on settings like `volatile-lru` (Least Recently Used) or `allkeys-lfu` (Least Frequently Used).
*   **Real-world Example:**
    Using Cache-Aside with Active Invalidation for product details:
    ```javascript
    async function getProduct(id) {
      let cached = await redis.get(`product:${id}`);
      if (cached) return JSON.parse(cached);

      let product = await db.query('SELECT * FROM products WHERE id = ?', [id]);
      await redis.setex(`product:${id}`, 3600, JSON.stringify(product));
      return product;
    }
    ```
*   **Common Mistakes:**
    *   **Cache Stampede (Thundering Herd):** When a popular key expires, and thousands of concurrent requests miss the cache and hit the database at once. (Resolve by using locking or background re-warming).
    *   **Cache Penetration:** Querying keys that never exist in the database, overloading the DB. (Resolve by caching empty results or using a Bloom Filter).
*   **Follow-up Interview Questions:**
    *   What is Cache Avalanche and how do you prevent it? (When many cached keys expire at the same time, crashing the database; prevent by adding random jitter to TTLs).
    *   What eviction policy should you use for database session caches? (Typically `allkeys-lru`).

</details>

<hr/>

### ❓ Q14. Compare Redis Pub/Sub vs. Message Queues (RabbitMQ/Kafka) for Event-Driven Systems.
<details>
<summary><b>👀 Show Answer</b></summary>

*   **Detailed Answer:**
    *   **Redis Pub/Sub:** A lightweight, fire-and-forget broadcasting system. Publishers send messages to channels; active subscribers receive them instantly.
        *   *Pros:* Sub-millisecond latency, zero broker overhead.
        *   *Cons:* No message persistence. If a subscriber is offline, the message is lost forever.
    *   **Redis Streams:** A log-based data structure (introduced in Redis 5) that supports consumer groups, offsets, and persistence, acting like a lightweight Kafka.
    *   **RabbitMQ:** A traditional AMQP broker. It stores messages in queues and routes them via exchanges. Supports acknowledgments, routing keys, and guaranteed delivery.
    *   **Apache Kafka:** A distributed, commit-log broker. Messages are persisted to disk in partitioned topics. Consumers track their own offsets, allowing replay. Best for high-throughput event sourcing.
*   **Real-world Example:**
    *   *Redis Pub/Sub:* Distributing real-time chat messages to active WebSocket servers.
    *   *Kafka:* Storing user clickstream analytics events for offline batch processing.
*   **Common Mistakes:**
    *   Using Redis Pub/Sub for transactional business flows (like processing billing payments) where message loss is unacceptable.
    *   Ignoring message acknowledgement logic in RabbitMQ, causing messages to remain locked in queues.
*   **Follow-up Interview Questions:**
    *   What is the difference between Redis Pub/Sub and Redis Streams? (Streams support persistence, consumer groups, and acknowledging processed items; Pub/Sub is fire-and-forget).
    *   What is consumer group offset committing in Kafka? (Saving the consumer index progress to coordinate partition processing).

</details>

<hr/>

### ❓ Q15. How do you implement Distributed Locks and Rate Limiting using Redis?
<details>
<summary><b>👀 Show Answer</b></summary>

*   **Detailed Answer:**
    *   **Distributed Locks (Redlock Algorithm):**
        To coordinate tasks across multiple servers, you need a lock. In Redis, you set a key only if it doesn't exist (`NX`) with a lease timeout (`PX`).
        *   Command: `SET lock_key unique_token NX PX 30000` (expires in 30s).
        *   *Releasing:* Must be done via a Lua script to ensure atomicity. The script checks if the key value matches the thread's `unique_token` before deleting, preventing a thread from deleting a lock owned by another thread that took too long.
    *   **Rate Limiting:**
        Can be implemented using a **Token Bucket** or **Sliding Window Log** via Redis sorted sets (`ZADD`, `ZREMRANGEBYSCORE`).
*   **Real-world Example:**
    Lua script for safe Distributed Lock release:
    ```lua
    if redis.call("get", KEYS[1]) == ARGV[1] then
        return redis.call("del", KEYS[1])
    else
        return 0
    end
    ```
*   **Common Mistakes:**
    *   Releasing a distributed lock using a simple `DEL` command (without checking the token value), which can lead to releasing a lock that another process acquired after yours expired.
    *   Choosing a lock expiration time that is shorter than the execution time of the protected critical section.
*   **Follow-up Interview Questions:**
    *   What is the Redlock algorithm? (An algorithm proposed by Redis creator to acquire locks across multiple independent Redis master nodes to avoid single point of failure).
    *   How does a sliding window rate limiter work in Redis? (Uses Sorted Sets where keys are timestamps; counts items within the window range).

</details>

<hr/>

### ❓ Q16. Compare Redis Persistence Mechanisms: RDB vs. AOF.
<details>
<summary><b>👀 Show Answer</b></summary>

*   **Detailed Answer:**
    Redis is an in-memory database, but it offers persistence options to recover data after restarts:
    1.  **RDB (Redis Database Backup):**
        *   *How:* Takes point-in-time snapshots of the dataset at specified intervals (e.g., every 5 minutes if 100 keys changed). It forks a child process to write the DB to a binary file (`dump.rdb`).
        *   *Pros:* Extremely compact file size, fast restart times. Minimal impact on parent process performance.
        *   *Cons:* Risk of data loss (data written since the last snapshot is lost if Redis crashes).
    2.  **AOF (Append Only File):**
        *   *How:* Logs every write command received by the server to a log file (`appendonly.aof`). Commands are synced to disk using `fsync` policies (`always`, `everysec`, `no`).
        *   *Pros:* Durable (virtually zero data loss with `everysec`).
        *   *Cons:* File sizes are much larger than RDB, restarts are slower, and writing commands can impact performance depending on the `fsync` policy.
    
    In production, a hybrid model (both RDB and AOF enabled) is recommended.
*   **Real-world Example:**
    Tuning a production Redis instance: Configuring AOF with `appendfsync everysec` to balance performance and durability, and scheduled RDB snapshots for backup.
*   **Common Mistakes:**
    *   Using `appendfsync always` under high-throughput write loads (causes disk I/O bottlenecks).
    *   Forgetting to monitor disk space usage on the server, as AOF files will grow indefinitely until rewritten (`BGREWRITEAOF`).
*   **Follow-up Interview Questions:**
    *   What does `BGREWRITEAOF` do? (Instructs Redis to write a new, optimized version of the AOF log file in the background by analyzing the current in-memory state).
    *   How does the fork operation affect Redis memory footprint? (Uses OS copy-on-write; if many writes occur during fork, memory usage can double).

</details>

---

# 4. System Design

### ❓ Q17. Design a highly scalable URL Shortener (e.g., bit.ly).
<details>
<summary><b>👀 Show Answer</b></summary>

*   **High-Level Design (HLD):**
    ```text
     [Client] ---> [Load Balancer / API Gateway] 
                        |
            +-----------+-----------+
            |                       |
      [Write Service]         [Read Service]
            |                       |
     [Token Generator]          [Redis Cache]
            |                       |
            +-----------+-----------+
                        |
                  [NoSQL (MongoDB)]
    ```
    The system is split into write-heavy paths (generating short URLs) and read-heavy paths (redirecting). The **Read Service** is optimized for high throughput with a Redis cluster layer caching popular URLs, routing cache misses to a database (MongoDB). The **Write Service** communicates with a unique **Token Generator Service** to retrieve pre-allocated IDs.
*   **Low-Level Design (LLD) & Key Mechanics:**
    1.  **URL Encoding:** Base62 encoding (`[a-zA-Z0-9]`). A 7-character code provides $62^7 \approx 3.5$ trillion unique short URLs.
    2.  **Unique ID Generation:** A distributed coordinator like Apache ZooKeeper manages ID ranges for token generator instances. Each instance keeps a range in memory (e.g., 1 to 100,000) and increments it locally. This avoids central database auto-increment locks.
*   **Database Design:**
    A NoSQL collection (MongoDB) stores mappings since queries are simple key-value lookups.
    *   **Schema (`url_mappings`):**
        ```json
        {
          "_id": "Base62_ShortCode",
          "originalUrl": "https://example.com/very/long/url",
          "userId": "String_ObjectId",
          "createdAt": "ISODate"
        }
        ```
    *   **Index:** Unique index on `_id`.
*   **Scaling Strategy:**
    *   **Read Optimization:** 90% of traffic is reads. Redis cache eviction policy set to `volatile-lru`.
    *   **Horizontal Sharding:** Database sharded by the prefix of the hash of the short code to distribute load evenly.
*   **Bottlenecks & Security:**
    *   *Bottleneck:* Redis replication latency during sudden traffic spikes. Resolvable by adding local memory caches on read pods.
    *   *Security:* Restrict brute-force enumeration of short URLs by using a non-sequential, randomized hash seed for ID assignment. Validate original URLs against malware APIs (e.g., Google Safe Browsing).

</details>

<hr/>

### ❓ Q18. Design a Notification Service (Push, SMS, Email).
<details>
<summary><b>👀 Show Answer</b></summary>

*   **High-Level Design (HLD):**
    ```text
     [User Service / Event Trigger] ---> [API Gateway] ---> [Ingestion Workers]
                                                                  |
                                                           [RabbitMQ/Kafka]
                                                                  |
         +------------------------+-------------------------------+
         |                        |                               |
    [Push Workers]          [Email Workers]                 [SMS Workers]
         |                        |                               |
    [FCM/APNS]           [SES/SendGrid/Mailgun]          [Twilio/MessageBird]
    ```
*   **Low-Level Design (LLD) & Key Mechanics:**
    1.  **Priority Queues:** Notifications are grouped into High Priority (OTP, transaction receipts) and Low Priority (marketing campaigns).
    2.  **Idempotency Handler:** A database or cache table checks if a correlation ID has already been executed to prevent sending duplicate notifications if workers retry.
*   **Database Design (PostgreSQL):**
    *   `notifications` table:
        ```sql
        CREATE TABLE notifications (
            id UUID PRIMARY KEY,
            user_id VARCHAR(255) NOT NULL,
            type VARCHAR(50) NOT NULL, -- PUSH, SMS, EMAIL
            recipient VARCHAR(255) NOT NULL,
            content TEXT NOT NULL,
            status VARCHAR(50) DEFAULT 'PENDING',
            retry_count INT DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE INDEX idx_user_status ON notifications(user_id, status);
        ```
*   **Scaling Strategy:**
    *   Use **Rate Limiting** per integration channel (e.g., SMS carriers have strict TPS limits).
    *   Auto-scale worker pods in Kubernetes based on the consumer lag metric in Kafka/RabbitMQ.
*   **Bottlenecks & Security:**
    *   *Bottleneck:* Network latency of third-party SMS/Email gateways. Decoupled using async worker processes.
    *   *Security:* Implement strict data scrubbing in logs to avoid exposing OTPs or sensitive personal info. Secure API credentials of gateways.

</details>

<hr/>

### ❓ Q19. Design a Payment System (Double-Entry Bookkeeping, Idempotency).
<details>
<summary><b>👀 Show Answer</b></summary>

*   **High-Level Design (HLD):**
    ```text
     [Checkout UI] ---> [Payment Gateway Service] ---> [Idempotency Filter (Redis)]
                                    |
                        [Payment Executor Engine]
                                    |
            +-----------------------+-----------------------+
            |                                               |
     [Double-Entry Ledger]                       [External Gateways (Stripe)]
    ```
*   **Low-Level Design (LLD) & Key Mechanics:**
    1.  **Idempotency Keys:** Every request must submit a unique token. The server caches this token in Redis during execution. If the payment succeeds, the client receives the cached response on subsequent retries.
    2.  **Double-Entry Bookkeeping:** All money movements are logged as debits and credits across assets, liabilities, and equity accounts. The sum of debits must always equal the sum of credits. No balance can be updated directly without creating a ledger transaction row.
*   **Database Design (PostgreSQL):**
    *   `accounts` table:
        ```sql
        CREATE TABLE accounts (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            balance DECIMAL(15, 2) NOT NULL
        );
        ```
    *   `ledger_entries` table:
        ```sql
        CREATE TABLE ledger_entries (
            id UUID PRIMARY KEY,
            transaction_id UUID NOT NULL,
            account_id INT REFERENCES accounts(id),
            type VARCHAR(10) CHECK (type IN ('DEBIT', 'CREDIT')),
            amount DECIMAL(15, 2) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        ```
*   **Scaling Strategy:**
    *   Relational database shard-by-customer using PostgreSQL schemas or partitioned tables.
    *   Isolate the transaction log processing into high-throughput queue systems.
*   **Bottlenecks & Security:**
    *   *Bottleneck:* Database locking during ledger updates. Resolved by partitioning tables and batching ledger entries.
    *   *Security:* PCI-DSS compliance. Never store raw credit card credentials. Use tokenization (Stripe Elements) directly from the client.

</details>

<hr/>

### ❓ Q20. Design a Real-Time Chat Application.
<details>
<summary><b>👀 Show Answer</b></summary>

*   **High-Level Design (HLD):**
    ```text
     [Clients] <====WebSocket====> [WebSocket Servers] <---Pub/Sub (Redis)---> [Chat Service]
                                         |                                         |
                                  [Presence (Redis)]                       [Database (MongoDB)]
    ```
*   **Low-Level Design (LLD) & Key Mechanics:**
    1.  **Connection Management:** Load Balancer distributes WebSocket connections using sticky sessions (based on IP/headers).
    2.  **Message Delivery:** When Client A sends a message to Client B, the WebSocket server looks up B's active node in a Redis Presence mapping. If B is connected to Node 2, Node 1 publishes the message to Redis Pub/Sub, which routes it to Node 2 for delivery.
*   **Database Design:**
    MongoDB is used for chat history because of high write speed and schema flexibility.
    *   **`messages` collection:**
        ```json
        {
          "_id": "ObjectId",
          "chatId": "String_RoomId",
          "senderId": "String_UserId",
          "content": "String",
          "status": "DELIVERED / READ",
          "timestamp": "ISODate"
        }
        ```
    *   **Index:** Compound index on `{ chatId: 1, timestamp: -1 }`.
*   **Scaling Strategy:**
    *   Redis Cluster scales Pub/Sub throughput.
    *   MongoDB sharding using `chatId` as the shard key to keep single conversations on the same physical shard for fast read fetches.
*   **Bottlenecks & Security:**
    *   *Bottleneck:* Connection limits on WebSocket servers. Resolved by tuning Linux sysctl configs (`file-max` and `tcp` limits).
    *   *Security:* End-to-end encryption (E2EE) using Signal Protocol on client devices. Sanitizing HTML in the chat parser to prevent XSS.

</details>

<hr/>

### ❓ Q21. Design a Large Scale Video Calling Platform (WebRTC scale).
<details>
<summary><b>👀 Show Answer</b></summary>

*   **High-Level Design (HLD):**
    ```text
     [Client A] <===Signaling WebSocket===> [Signaling Service (Node.js)]
         |                                           |
     (WebRTC Media stream)                   (Room Coordination)
         |                                           |
         v                                           v
     [SFU Media Server (Kurento/Mediasoup)] <---> [Redis Cluster Store]
    ```
*   **Low-Level Design (LLD) & Key Mechanics:**
    1.  **Selective Forwarding Unit (SFU):** Instead of Peer-to-Peer (Mesh), which crashes user devices with high CPU during group calls, clients connect to an SFU server. The client sends 1 uplink stream (audio/video), and the SFU forwards it as separate downlink streams to other participants.
    2.  **Signaling Exchange:** Signaling service routes SDP (Session Description Protocol) offers, answers, and ICE candidates between participants.
*   **Database Design (Redis & PostgreSQL):**
    *   **Redis:** Dynamic state mapping. Store room active user IDs and their current SFU IP assignments.
    *   **PostgreSQL:** Historical metadata (users, calls logs, bills).
*   **Scaling Strategy:**
    *   Media servers are highly CPU-bound. Scale them horizontally by spawning SFU instances and deploying custom load balancing that assigns new rooms to SFUs with lowest CPU usage.
*   **Bottlenecks & Security:**
    *   *Bottleneck:* Network bandwidth on SFUs. Mitigated by using **Simulcast** (clients send video in 3 resolutions; the SFU sends lower quality to users with slow network links).
    *   *Security:* Enforce DTLS-SRTP encryption on media channels. Validate room tokens before allowing a client to join signaling channels.

</details>

<hr/>

### ❓ Q22. Design a Learning Management System (LMS) Platform (Course enrollment, Content delivery).
<details>
<summary><b>👀 Show Answer</b></summary>

*   **High-Level Design (HLD):**
    ```text
     [Client Browser] ---> [CloudFront CDN] ---> [ALB / API Gateway]
                                                      |
            +--------------------+--------------------+--------------------+
            |                    |                    |                    |
     [Auth Service]      [Course Service]     [Enrollment Service]  [Video Transcoding]
            |                    |                    |                    |
      [PostgreSQL]          [Redis Cache]       [Kafka Broker]          [AWS Elemental]
                                                      |                    |
                                              [Worker Consumers]        [AWS S3]
        
    ```
*   **Low-Level Design (LLD) & Key Mechanics:**
    1.  **Course Content Delivery:** Static materials (PDFs, metadata) and video chunks are cached at the edge via CloudFront.
    2.  **Enrollment Transaction:** Relational consistency is critical here. Using database transactions with pessimistic locking (`SELECT ... FOR UPDATE`) prevents users from bypassing enrollment slots limit.
*   **Database Design (PostgreSQL):**
    *   `courses` table:
        ```sql
        CREATE TABLE courses (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            slots_limit INT NOT NULL
        );
        ```
    *   `enrollments` table:
        ```sql
        CREATE TABLE enrollments (
            id SERIAL PRIMARY KEY,
            user_id INT NOT NULL,
            course_id INT REFERENCES courses(id),
            enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, course_id)
        );
        ```
*   **Scaling Strategy:**
    *   Decouple student progress analytics: When a user watches a video, write progress ticks asynchronously to Kafka, processing them with background workers to offload DB write stress.
*   **Bottlenecks & Security:**
    *   *Bottleneck:* Large video uploads. Resolved by direct-to-S3 signed URLs, offloading uploading tasks from the API server.
    *   *Security:* Restrict unauthorized video downloading by utilizing HLS (HTTP Live Streaming) segments signed with temporary keys.

</details>

<hr/>

### ❓ Q23. Design a Large Scale API Architecture.
<details>
<summary><b>👀 Show Answer</b></summary>

*   **High-Level Design (HLD):**
    ```text
     [Global DNS / Route 53] ---> [CloudFront CDN] ---> [Kong/Apisix API Gateway]
                                                               |
                                                   +-----------+-----------+
                                                   |                       |
                                             [Service Mesh]          [Auth (OIDC)]
                                                   |
                                    +--------------+--------------+
                                    |                             |
                            [Catalog Service]             [Order Service]
                                    |                             |
                              [Redis Cache]                   [Postgres]
    ```
*   **Low-Level Design (LLD) & Key Mechanics:**
    1.  **API Gateway Routing:** Handles global path-based routing, authentication verification, SSL termination, and client rate limiting.
    2.  **Service Mesh (Istio):** Manages internal service-to-service communication (mTLS, circuit breaking, distributed tracing injections).
*   **Database Design:**
    Each microservice owns its private database. No database queries cross microservice boundaries (Database-per-service pattern). Synchronization is achieved using CDC (Change Data Capture) or messaging queues (Kafka).
*   **Scaling Strategy:**
    *   Implement **Circuit Breakers** on external integrations.
    *   Cache dynamic API GET responses using HTTP caching headers (`Cache-Control: public, max-age=60`).
*   **Bottlenecks & Security:**
    *   *Bottleneck:* Single API Gateway failure. Mitigated by scaling the gateway layer behind an AWS Application Load Balancer across multi-AZs.
    *   *Security:* Implement OAuth 2.0 / OpenID Connect tokens, RBAC, WAF (Web Application Firewall) to filter SQL injections and common OWASP vulnerabilities.

</details>

---

# 5. Real-Time Communication

### ❓ Q24. Detail the WebRTC Connection Flow (Signaling, STUN/TURN, ICE Candidates).
<details>
<summary><b>👀 Show Answer</b></summary>

*   **Detailed Answer:**
    WebRTC is a peer-to-peer real-time media framework. However, two browser clients cannot connect directly due to NAT (Network Address Translation) and Firewalls. The connection setup requires a signaling layer and ICE servers:
    1.  **Signaling:** The exchange of media and network metadata. Peer A creates an **SDP Offer** (Session Description Protocol) defining its media formats and codecs. It sends it to Peer B via a Signaling Server (WebSockets/Socket.io). B responds with an **SDP Answer**.
    2.  **STUN (Session Traversal Utilities for NAT):** Peers call a STUN server to discover their public IP and port. STUN is fast and cheap, handling ~80% of connections.
    3.  **TURN (Traversal Using Relays around NAT):** If STUN fails (due to symmetric NAT/firewalls), the connection fallback is a TURN server, which acts as a media relay. All voice/video traffic flows through the TURN server. This is bandwidth-heavy and expensive.
    4.  **ICE (Interactive Connectivity Establishment):** A framework that gathers all possible connection paths (Host candidates, Server reflexive candidates from STUN, and Relay candidates from TURN) and test them in order of efficiency to establish the best peer path.
*   **Real-world Example:**
    A corporate video call where users behind strict office enterprise routers fail to connect directly via STUN. The system automatically routes their audio/video data packets through a CoTURN TURN server deployed on AWS.
*   **Common Mistakes:**
    *   Forgetting to add a TURN server configuration in the RTC Configuration (resulting in calls failing to connect when users are on cellular data or corporate networks).
    *   Assuming the Signaling server hosts the video stream (the signaling server only routes text-based metadata to coordinate connection setup).
*   **Follow-up Interview Questions:**
    *   What is the difference between SDP Offer and SDP Answer? (SDP Offer specifies what media/codecs the sender supports; SDP Answer is the receiver's response accepting or modifying those codecs).
    *   What protocols do WebRTC channels use? (SRTP for media streaming, SCTP for data channels).

</details>

<hr/>

### ❓ Q25. Compare Socket.io vs. WebSockets: Core differences and connection management.
<details>
<summary><b>👀 Show Answer</b></summary>

*   **Detailed Answer:**
    *   **WebSockets:**
        *   A native browser API providing full-duplex communication over a single TCP connection.
        *   Lightweight with low network overhead.
        *   Requires manual implementation of reconnection strategies, heartbeats, grouping (rooms), and fallback mechanisms.
    *   **Socket.io:**
        *   A wrapper library built on top of WebSockets and HTTP long-polling.
        *   Includes built-in auto-reconnection, heartbeats (ping/pong packets), auto-fallback (starts with HTTP polling and upgrades to WebSockets), and Room/Namespace support.
        *   *Downside:* Adds library overhead and is not compatible with native WebSocket clients.
*   **Real-world Example:**
    *   *Socket.io:* A real-time collaboration whiteboard where ease of room management, automatic reconnections, and backwards compatibility are critical.
    *   *WebSockets:* A financial ticker API where minimizing payload footprint and optimizing raw throughput are key.
*   **Common Mistakes:**
    *   Trying to connect a native WebSocket client (`new WebSocket('ws://...')`) directly to a Socket.io backend (they utilize incompatible handshaking protocols).
    *   Not configuring Ping/Pong intervals, leading to silent zombie connections that leak memory on the server.
*   **Follow-up Interview Questions:**
    *   How does Socket.io fall back to HTTP polling? (It sends regular HTTP GET/POST requests using Engine.io until the WebSocket upgrade handshake completes).
    *   How do you scale Socket.io across multiple servers? (By using a Redis Adapter to broadcast events across different WebSocket server instances).

</details>

<hr/>

### ❓ Q26. Explain Group Calling Architectures: SFU vs. MCU vs. Mesh.
<details>
<summary><b>👀 Show Answer</b></summary>

*   **Detailed Answer:**
    ```text
    1. Mesh (Peer-to-Peer)      2. MCU (Multi-point Control Unit)      3. SFU (Selective Forwarding Unit)
    
       [Peer A] <---> [Peer B]           [Peer A]   [Peer B]                [Peer A]   [Peer B]
          ^            ^                    \         /                        \         /
           \          /                      v       v                          v       v
             [Peer C]                         [ MCU ]                            [ SFU ]
                                             (Mixes stream)                     (Forwards stream)
                                                /     \                          /     \
                                               v       v                        v       v
                                            [Peer C] [Peer D]                [Peer C] [Peer D]
    ```
    1.  **Mesh (P2P):** Each peer connects directly to all other peers.
        *   *Pros:* Low server cost, low latency.
        *   *Cons:* Client CPU and bandwidth utilization scales quadratically $O(N^2)$. Fails for groups larger than 3-4 users.
    2.  **MCU (Multipoint Control Unit):** Peers send their media to a central server. The server decodes, resizes, blends all streams into a single composite video/audio track, encodes it, and sends one stream to each peer.
        *   *Pros:* Minimal bandwidth/CPU requirement on the client ($O(1)$).
        *   *Cons:* Extremely high CPU cost on the server (decoding/encoding is expensive), high infrastructure cost.
    3.  **SFU (Selective Forwarding Unit):** Peers send their media to a central server. The server does not decode; it forwards the streams as-is to all other peers.
        *   *Pros:* Low server CPU usage compared to MCU. Decoupled media control. Enables custom client layouts.
        *   *Cons:* Bandwidth scales linearly $O(N)$ on the client.
*   **Real-world Example:**
    Zoom and Microsoft Teams utilize an SFU-based architecture combined with Simulcast/SVC to scale large-scale group calling.
*   **Common Mistakes:**
    *   Selecting a Mesh (P2P) architecture for a virtual classroom system with 20+ users.
    *   Assuming SFUs require massive GPU power (SFUs perform routing at the network packet level without rendering or transcoding video).
*   **Follow-up Interview Questions:**
    *   What is Simulcast in WebRTC? (A technique where a client uploads three streams of different video qualities, and the SFU distributes the optimal quality matching each subscriber's network bandwidth).
    *   What is spatial audio? (Processing audio streams dynamically based on participant grid coordinate positions to mimic physical rooms).

</details>

<hr/>

### ❓ Q27. How do you scale Presence Systems for millions of concurrent users?
<details>
<summary><b>👀 Show Answer</b></summary>

*   **Detailed Answer:**
    A Presence System tracks who is online/offline and broadcasts state changes. In high-concurrency systems, publishing status updates on every user transition can trigger massive event storms.
    
    **Scaling Presence Architecture:**
    1.  **Storage:** Use Redis for fast state lookups. Store presence status using a hash mapping: `HSET presence:users userId "online"`. Set a TTL (e.g., 60s) on user activity keys.
    2.  **Heartbeats:** Active clients send regular ping signals every 30 seconds. A background worker sweeps Redis keys; if a user's heartbeat key has expired, their status is changed to "offline".
    3.  **Throttling Broadcasts:** Do not send status updates instantly. Queue changes in a buffer and batch them (e.g., once every 5 seconds) to client groups.
    4.  **Pub/Sub Distribution:** Use user friendship/room graphs to scope broadcasts. Clients only subscribe to status updates of their active contacts, rather than global channels.
*   **Real-world Example:**
    Slack handles presence by checking user status on load, then subscribing to presence events only for users visible on the current screen, saving bandwidth.
*   **Common Mistakes:**
    *   Writing presence states directly to SQL databases on every user click, which exhausts transaction limits.
    *   Broadcasting status updates to all online users globally, causing $O(N^2)$ network scaling.
*   **Follow-up Interview Questions:**
    *   How does Redis handle key expiration notify triggers? (Through Redis Keyspace Notifications, which publish events on expired keys).
    *   What is the benefit of a pull-based presence model vs a push-based model? (Pull model fetches presence on demand, saving message transmissions for inactive users).

</details>

---

# 6. React.js Deep Dive

### ❓ Q28. How does the Virtual DOM and the Reconciliation (Fiber) engine work in React?
<details>
<summary><b>👀 Show Answer</b></summary>

*   **Detailed Answer:**
    The **Virtual DOM (VDOM)** is a lightweight, in-memory representation of the real DOM elements.
    When a component's state or props change:
    1.  React builds a new VDOM tree.
    2.  It compares this new tree with the previous VDOM tree using a process called **Reconciliation**.
    3.  It calculates the minimum number of changes needed (diffing) and updates only those specific nodes in the real DOM.
    
    **React Fiber (introduced in v16):**
    The old reconciliation engine used a recursive stack-based approach that blocked the main thread until it scanned the entire tree (causing animation lag). **Fiber** is a complete rewrite. It breaks reconciliation work into small units of work (fibers) that can be paused, prioritized, and resumed. Fiber separates reconciliation into two phases:
    1.  **Render Phase (Asynchronous):** Traverses the fiber tree, calculates changes. Can be paused if higher priority work (like user typing) enters the queue.
    2.  **Commit Phase (Synchronous):** Writes calculated changes directly to the real DOM. It is synchronous to prevent rendering half-drawn UI.
*   **Real-world Example:**
    Using React DevTools Profiler to identify components re-rendering unnecessarily during typing inputs, and resolving it by separating the input state from heavy child trees.
*   **Common Mistakes:**
    *   Using array index keys in dynamic lists (`key={index}`). If items are sorted/inserted, React mapping breaks, causing incorrect states and performance lags. Use stable, unique IDs.
    *   Mutating state variables directly (e.g., `state.list.push(item)`) instead of using setter functions (e.g., `setState([...state.list, item])`). Direct mutations bypass reconciliation triggers.
*   **Follow-up Interview Questions:**
    *   What is the difference between a controlled and uncontrolled component in React? (Controlled has state-synchronized values via onChange; uncontrolled queries values via DOM refs).
    *   Why must hook declarations follow a static call order (no loops/conditionals)? (React matches hook states sequentially based on execution index).

</details>

<hr/>

### ❓ Q29. Compare Context API vs. Redux Toolkit and Zustand. How do you optimize rendering performance?
<details>
<summary><b>👀 Show Answer</b></summary>

*   **Detailed Answer:**
    *   **Context API:** Built-in React feature. Best for sharing global static data (e.g., theme, language, auth credentials). **Crucial Caveat:** It is not a state management tool. Any update to the context value forces *all* consumer components to re-render, regardless of whether they consume the specific field that changed.
    *   **Redux Toolkit (RTK):** Opinionated, boilerplate-reduced version of Redux. It uses a single store with selectors. Best for massive enterprise applications with complex transactional state flows.
    *   **Zustand:** A minimalist, fast global store built on hooks. No boilerplate, no context provider wrappers. Components subscribe to specific slices of state, preventing unnecessary renders.
    
    **Rendering Optimization Tools:**
    *   `React.memo`: Wraps presentational components to skip re-renders if props don't change references.
    *   `useMemo`: Memoizes expensive calculations across renders.
    *   `useCallback`: Memoizes inline function references to prevent child re-renders.
*   **Real-world Example:**
    In a dashboard app, changing user settings shouldn't re-render the stock chart component. Using Zustand selectors ensures the stock chart only listens to the stock array slice:
    ```javascript
    const stocks = useStockStore(state => state.stocks); // Chart only re-renders if stocks changes
    ```
*   **Common Mistakes:**
    *   Wrapping every single component and function in `React.memo`/`useCallback` (adds overhead of checking changes; use only for heavy components).
    *   Passing new inline object references in props (e.g., `style={{ color: 'red' }}`) to memoized components, which invalidates `React.memo` since references differ on every render.
*   **Follow-up Interview Questions:**
    *   How does React Query/TanStack Query change state management? (It handles server/network state cache automatically, reducing the need for global stores like Redux for API data).
    *   What is "prop drilling"? (Passing props down through components that don't need them just to reach a child).

</details>

---

# 7. JavaScript Advanced

### ❓ Q30. Explain Closures, Hoisting, and the JavaScript Event Loop.
<details>
<summary><b>👀 Show Answer</b></summary>

*   **Detailed Answer:**
    *   **Closures:** A function's lexical scope remains alive even after the outer function has finished executing. The inner function retains references to variables declared in its parent's lexical scope.
    *   **Hoisting:** JavaScript engine moves declarations (variable/function) to the top of their containing scope during compilation.
        *   `var` is hoisted and initialized with `undefined`.
        *   `let` and `const` are hoisted but remain uninitialized in the **Temporal Dead Zone (TDZ)**.
        *   Function declarations are fully hoisted (can be called before definition). Function expressions (e.g. `const foo = () => {}`) are hoisted according to their variable type (`let`/`const`).
    *   **Event Loop:** Coordinates call stack, Web APIs, Microtask Queue (Promises, `queueMicrotask`), and Macrotask Queue (`setTimeout`, I/O, UI render). The stack must be empty before the event loop pulls from the queues. **Microtasks have absolute priority over Macrotasks.**
*   **Real-world Example:**
    Creating private counters or currying configurations:
    ```javascript
    function makeApiKeyRequester(apiKey) {
      return function(endpoint) {
        return fetch(`${endpoint}?key=${apiKey}`); // Retains access to apiKey
      }
    }
    ```
*   **Common Mistakes:**
    *   Creating closures inside loop iterations using `var` instead of `let`, leading to all iterations referencing the final index value.
    *   Writing massive synchronous tasks that block the call stack, freezing the UI browser.
*   **Follow-up Interview Questions:**
    *   Explain the difference between `==` and `===`. (=== checks both value and type without performing implicit type coercion).
    *   What is the difference between `null` and `undefined`? (null represents intentional absence of value; undefined indicates a variable has been declared but not assigned a value).

</details>

<hr/>

### ❓ Q31. How does JavaScript handle Memory Management and Prototype inheritance?
<details>
<summary><b>👀 Show Answer</b></summary>

*   **Detailed Answer:**
    *   **Memory Management:** JS automatically allocates memory on creation and frees it using garbage collection (GC). CPython/Node uses a **Mark-and-Sweep** algorithm:
        1.  The GC defines a list of "roots" (global variables, call stack references).
        2.  It traverses the reference graph, marking all reachable objects.
        3.  Any unmarked, unreachable object is swept from memory.
    *   **Prototypal Inheritance:** In JS, objects inherit properties from other objects via a prototype chain. Every object has an internal link (`[[Prototype]]`, accessed via `Object.getPrototypeOf()` or `__proto__`). When a property lookup fails on an object, JS traverses the chain until it finds the property or hits `null`.
*   **Real-world Example:**
    Extending built-in prototypes is generally discouraged, but understanding it explains class extensions:
    ```javascript
    class Animal {
      speak() { return "Noise"; }
    }
    class Dog extends Animal {} // Dog.prototype.__proto__ === Animal.prototype
    ```
*   **Common Mistakes:**
    *   Dangling references in closures (retaining reference to huge objects in long-lived callback functions).
    *   Modifying native prototypes directly (e.g., `Array.prototype.foo = ...`), which can cause compatibility issues with other libraries.
*   **Follow-up Interview Questions:**
    *   What is the purpose of `Object.create(null)`? (Creates an object with no prototype chain, useful for clean dictionary mappings).
    *   How does the `this` keyword resolve in arrow functions vs normal functions? (Arrow functions resolve `this` lexically from their enclosing scope; normal functions resolve it dynamically based on how they are called).

</details>

---

# 8. Tailwind CSS

### ❓ Q32. How do you optimize Tailwind CSS for production, configure dark mode, and structure reusable components?
<details>
<summary><b>👀 Show Answer</b></summary>

*   **Detailed Answer:**
    *   **Optimization:** Tailwind CSS version 3 uses a Just-In-Time (JIT) compiler. It scans your source files (`html`, `js`, `jsx`, `tsx`) and generates CSS rules *only* for the utility classes you explicitly write. In production, this output is minified. Ensure the `content` array in `tailwind.config.js` points to all source file locations.
    *   **Dark Mode:** Configure it in `tailwind.config.js` using `darkMode: 'class'`. This triggers dark variants whenever the `dark` class is present on the root `<html>` or `<body>` element.
    *   **Reusable Components:**
        1.  In framework applications (React, Angular), wrap styles inside reusable component templates.
        2.  For repeated utility combinations, use Tailwind custom utility plugins or `@apply` syntax inside custom CSS layers (e.g., `@layer components`).
*   **Real-world Example:**
    Configuring dark mode toggle in React:
    ```javascript
    const toggleDarkMode = () => {
      document.documentElement.classList.toggle('dark');
    };
    ```
    Tailwind CSS styling:
    ```html
    <div class="bg-white text-black dark:bg-slate-900 dark:text-white">
      Dark mode card
    </div>
    ```
*   **Common Mistakes:**
    *   Using dynamic class string interpolations (e.g., `class={`bg-${color}-500`}`). Tailwind's scanner cannot compile partial string fragments; classes must be declared as complete static literals.
    *   Abusing the `@apply` directive to build massive traditional stylesheets, which defeats the utility-first design benefit and bloats the production bundle.
*   **Follow-up Interview Questions:**
    *   How do you configure custom theme colors and breakpoints in Tailwind? (Through the `theme.extend` section of `tailwind.config.js`).
    *   What are utility-first CSS benefits? (Saves writing custom CSS class names; style files don't grow with design iterations).

</details>

---

# 9. Authentication & Security

### ❓ Q33. Compare Session Cookies vs. JWT. How do you implement secure Refresh Token Rotation?
<details>
<summary><b>👀 Show Answer</b></summary>

*   **Detailed Answer:**
    *   **Session Cookies:** Stateful. The server stores a session record in a database (or Redis) and issues a random session ID in a secure cookie to the browser.
        *   *Pros:* Easy to revoke instantly.
        *   *Cons:* DB lookup on every API call, harder to scale horizontally.
    *   **JWT (JSON Web Token):** Stateless. A cryptographically signed token containing user payload.
        *   *Pros:* Decentralized validation (no DB check needed by target servers).
        *   *Cons:* Revocation is difficult until the token expires.
    
    **Secure Refresh Token Rotation Flow:**
    To achieve statelessness with high security, utilize both tokens:
    1.  **Access Token:** Short lifespan (e.g., 15 mins). Sent in HTTP headers.
    2.  **Refresh Token:** Long lifespan (e.g., 7 days). Stored in a secure `HttpOnly`, `Secure`, `SameSite=Strict` cookie.
    3.  **Rotation:** When the client requests a new Access Token using their Refresh Token:
        *   The server invalidates that specific Refresh Token.
        *   It issues a new Access Token *and* a brand-new Refresh Token.
        *   If the server receives a reuse request for an invalidated Refresh Token, it flags a potential breach, invalidates all active sessions for that user, and forces a re-login.
*   **Real-world Example:**
    Implementing Token Rotation in an authentication service using Redis to keep track of a blacklist/whitelist of active refresh tokens.
*   **Common Mistakes:**
    *   Storing Access or Refresh tokens in `localStorage` (exposed to XSS attacks that steal tokens via injected scripts).
    *   Not verifying the signing signature (`jwt.verify`) on the backend, allowing clients to forge arbitrary payloads.
*   **Follow-up Interview Questions:**
    *   What are the three parts of a JWT? (Header: algorithm type; Payload: claims/data; Signature: cryptographic verification).
    *   What are the HttpOnly, Secure, and SameSite cookie flags? (HttpOnly blocks JS access; Secure forces HTTPS; SameSite prevents CSRF).

</details>

<hr/>

### ❓ Q34. Explain OWASP Top 10 vulnerabilities (XSS, CSRF, SQLi, NoSQLi) and prevention.
<details>
<summary><b>👀 Show Answer</b></summary>

*   **Detailed Answer:**
    1.  **XSS (Cross-Site Scripting):** Malicious scripts are injected into trusted sites.
        *   *Type:* Stored, Reflected, DOM-based.
        *   *Prevention:* Sanitize inputs. Escape outputs (convert `<` to `&lt;`). Use Content Security Policy (CSP) headers.
    2.  **CSRF (Cross-Site Request Forgery):** Tricks logged-in browsers to perform actions on a different site automatically.
        *   *Prevention:* Use Anti-CSRF tokens. Set `SameSite=Lax` or `Strict` on cookies.
    3.  **SQL Injection (SQLi):** Inserting malicious SQL statements into inputs to manipulate queries.
        *   *Prevention:* Use parameterized queries (Prepared Statements). Never concatenate inputs directly into query strings.
    4.  **NoSQL Injection:** Injecting MongoDB operator queries (e.g., `{"$gt": ""}`).
        *   *Prevention:* Validate schemas using validation libraries (Zod, Joi) to ensure input fields are strings, not objects.
*   **Real-world Example:**
    NoSQL Injection vulnerability:
    ```javascript
    // Unsafe: if req.body.password is {"$ne": "random"}, query matches any non-empty password
    db.users.findOne({ username: req.body.username, password: req.body.password });
    
    // Safe: Sanitizing input data types using Zod
    const schema = z.object({
      username: z.string(),
      password: z.string()
    });
    ```
*   **Common Mistakes:**
    *   Relying on regex input validation filters instead of prepared statements.
    *   Using React's `dangerouslySetInnerHTML` parameter without sanitizing the input through a library like `DOMPurify`.
*   **Follow-up Interview Questions:**
    *   What does a Content Security Policy (CSP) header do? (Defines which domains the browser is allowed to load scripts and styles from, blocking inline scripts).
    *   What is an ORM's role in security? (ORMs implicitly parameterize database queries, mitigating SQL injections).

</details>

---

# 10. Docker Deep Dive

### ❓ Q35. Detail Docker Multi-stage Builds and secure networking topologies.
<details>
<summary><b>👀 Show Answer</b></summary>

*   **Detailed Answer:**
    *   **Docker Multi-stage Builds:** A Dockerfile optimization pattern. It defines multiple `FROM` blocks. You run the build process (pulling compilers, SDKs, devDependencies) in an initial stage, then copy *only* the compiled assets (e.g., the built Java jar or node build folder) into a lightweight, clean runtime environment stage (e.g., alpine).
        *   *Pros:* Reduces final image sizes by 80%, decreases attack surface by removing compilers and source code from production.
    *   **Docker Networking:**
        *   `Bridge` (default): Private internal network on the host. Containers communicate using DNS aliases.
        *   `Host`: Bypasses isolation, uses host network directly. Fastest but insecure.
        *   `Overlay`: Connects multiple Docker daemons (Swarm/K8s clusters), allowing cross-host container communication.
        *   `None`: Disables networking completely.
*   **Real-world Example:**
    Multi-stage build for a Node.js API:
    ```dockerfile
    # Stage 1: Build
    FROM node:18-alpine AS builder
    WORKDIR /app
    COPY package*.json ./
    RUN npm ci
    COPY . .
    RUN npm run build

    # Stage 2: Run
    FROM node:18-alpine AS runner
    WORKDIR /app
    COPY package*.json ./
    RUN npm ci --only=production
    COPY --from=builder /app/dist ./dist
    USER node
    EXPOSE 3000
    CMD ["node", "dist/index.js"]
    ```
*   **Common Mistakes:**
    *   Running containers as root (default). If a container is compromised, the attacker has root access to host kernels. Use `USER node` or custom non-root users.
    *   Including sensitive configuration files or secrets inside Docker images during build time. Secrets should be mounted at runtime as environment variables.
*   **Follow-up Interview Questions:**
    *   What is the difference between `CMD` and `ENTRYPOINT`? (ENTRYPOINT defines the executable that runs on startup; CMD specifies default arguments that can be overridden by the CLI).
    *   How do you optimize layer caching in Docker builds? (Copy package lists and run install steps *before* copying the remaining source code).

</details>

---

# 11. Kubernetes Deep Dive

### ❓ Q36. Explain Pods, Deployments, Services, and Ingress routing. How does HPA scale workloads?
<details>
<summary><b>👀 Show Answer</b></summary>

*   **Detailed Answer:**
    *   **Pod:** The smallest deployable unit in Kubernetes. Hosts one or more co-located containers sharing network namespaces, storage volumes, and local IP.
    *   **Deployment:** A controller that manages the state of Pods. It defines the replica count, container images, resource limits, and updates policies (e.g., Rolling Updates).
    *   **Service:** An abstract layer that defines a logical set of Pods and a policy to access them. Provides a stable IP address and DNS name, routing traffic to Pods using label selectors.
        *   *ClusterIP:* Internal communication only.
        *   *NodePort:* Exposes the service on a static port on each Node IP.
        *   *LoadBalancer:* Provisions an external load balancer (e.g., AWS NLB).
    *   **Ingress:** An API object that manages external access to services, acting as an application layer reverse proxy (layer 7). Handles routing paths, SSL termination, and host headers.
    *   **HPA (Horizontal Pod Autoscaler):** Scales pod replicas dynamically. It polls metrics APIs (CPU/Memory usage via Metrics Server or custom Prometheus metrics). If resource consumption exceeds a defined target percentage (e.g., CPU > 80%), the HPA requests the Deployment controller to increase the replica count.
*   **Real-world Example:**
    Deploying an HPA for a payment service:
    ```yaml
    apiVersion: autoscaling/v2
    kind: HorizontalPodAutoscaler
    metadata:
      name: payment-hpa
    spec:
      scaleTargetRef:
        apiVersion: apps/v1
        kind: Deployment
        name: payment-service
      minReplicas: 2
      maxReplicas: 10
      metrics:
      - type: Resource
        resource:
          name: cpu
          target:
            type: Utilization
            averageUtilization: 75
    ```
*   **Common Mistakes:**
    *   Deploying pods without configuring Resource Requests and Limits (resulting in pods scheduling randomly, leading to node resource exhaustion and OOM kills).
    *   Storing sensitive parameters (like passwords/database keys) inside basic ConfigMaps instead of encrypted Kubernetes Secrets.
*   **Follow-up Interview Questions:**
    *   What is the difference between a Liveness Probe and a Readiness Probe? (Liveness checks if a container has crashed and needs a restart; Readiness checks if the container is ready to receive network traffic).
    *   How does a Rolling Update work in Kubernetes? (It gradually replaces old pods with new ones, ensuring zero-downtime by checking readiness probes before dropping old pods).

</details>

---

# 12. AWS Deep Dive

### ❓ Q37. How do you design a high-availability architecture on AWS using EC2, ALB, ECS/EKS, and Route 53?
<details>
<summary><b>👀 Show Answer</b></summary>

*   **Detailed Answer:**
    A secure, highly available, multi-Availability Zone (AZ) architecture is designed as follows:
    1.  **Network Layer (VPC):** Create a VPC spanning two or more AZs. Build Public Subnets (hosting ALBs and NAT Gateways) and Private Subnets (hosting container nodes and database instances).
    2.  **DNS Routing (Route 53):** Routes client traffic to the ALB. Configured with Latency-based or Failover routing rules.
    3.  **Load Balancer (ALB):** Placed in public subnets. Binds SSL certificates, terminates TLS, and forwards traffic to the application layer.
    4.  **Compute Layer (ECS or EKS):** Deployed inside private subnets across multi-AZs. Nodes auto-scale based on load using Auto Scaling Groups. Container tasks are launched dynamically.
    5.  **Database Layer (RDS):** Deployed as Multi-AZ deployment. Active writes go to the Primary instance in AZ-A, which replicates data synchronously to a Standby instance in AZ-B. In case of primary failure, AWS automatically fails over to standby.
    6.  **CDN Layer (CloudFront):** Caches static assets (stored in S3) at global edge locations, reducing application layer load.
*   **Real-world Example:**
    Deploying a student catalog microservice where the client loads the index page from CloudFront, while dynamic course registrations go through Route 53 -> ALB -> EKS pods -> RDS PostgreSQL multi-AZ database.
*   **Common Mistakes:**
    *   Placing database instances in public subnets (exposes port 5432/3306 to the public internet, violating security compliance).
    *   Forgetting to configure a NAT Gateway for private subnets (pods inside private subnets won't be able to fetch external resources or install library patches).
*   **Follow-up Interview Questions:**
    *   What is the difference between IAM Roles and IAM Users? (IAM Users represent static accounts with credentials; IAM Roles are assumed temporarily by services or resources without using long-lived key credentials).
    *   What is S3 bucket versioning and object locking? (Versioning keeps historical file backups; object locking prevents deletions, protecting against ransomware).

</details>

---

# 13. Nginx & Linux

### ❓ Q38. Explain Nginx reverse proxying, load balancing, and Linux troubleshooting commands.
<details>
<summary><b>👀 Show Answer</b></summary>

*   **Detailed Answer:**
    *   **Nginx Reverse Proxy:** Nginx accepts client requests, intercepts them, and forwards them to backend upstream servers (Node.js, Go), shielding backend ports from the public internet.
    *   **Load Balancing Algorithms:**
        *   `Round-Robin` (default): Cycles requests sequentially.
        *   `Least-Conn`: Routes to the server with the fewest active connections.
        *   `IP-Hash`: Leverages client IP to route to the same upstream server (sticky sessions).
    *   **Linux Troubleshooting Toolbox:**
        *   `top` / `htop`: Real-time view of system processes, CPU, and Memory usage.
        *   `lsof -i :<port>`: Checks which process is listening on a specific port.
        *   `netstat -tuln` / `ss -tuln`: Lists all open ports and sockets.
        *   `journalctl -u <service>`: Inspects systemd logs.
        *   `df -h` / `du -sh *`: Identifies disk space utilization bottlenecks.
*   **Real-world Example:**
    Nginx upstream configuration with load balancing:
    ```nginx
    upstream backend_servers {
        least_conn;
        server backend1.example.com:3000 weight=3;
        server backend2.example.com:3000;
    }
    server {
        listen 80;
        location / {
            proxy_pass http://backend_servers;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
    ```
*   **Common Mistakes:**
    *   Forgetting to increase connection limits in Nginx configs (`worker_connections 1024` default is too low for high-traffic servers; increase to 10240 or more).
    *   Using blocking sync commands (like `grep` on 50GB log files) on active production servers; use `zgrep` or offload logs to ELK.
*   **Follow-up Interview Questions:**
    *   What is the difference between Nginx and Apache? (Nginx uses an asynchronous, event-driven architecture; Apache uses a thread-per-request model).
    *   What command would you use to trace system calls made by a process? (`strace -p <PID>`).

</details>

---

# 14. CI/CD

### ❓ Q39. Explain Blue-Green vs. Canary deployments. Detail a rollback strategy.
<details>
<summary><b>👀 Show Answer</b></summary>

*   **Detailed Answer:**
    *   **Blue-Green Deployment:** You maintain two identical production environments. Blue is active (handles live traffic); Green is idle (hosts the new code version). Once testing passes on Green, the Load Balancer switches router traffic from Blue to Green.
        *   *Pros:* Zero downtime, instant rollback (switch router back to Blue).
        *   *Cons:* Double infrastructure costs since two full environments run concurrently.
    *   **Canary Deployment:** You deploy the new code version to a small subset of instances (e.g., 5% of traffic). You monitor metrics (errors, latency). If metrics remain stable, you roll out the new version to the remaining 95% of servers.
        *   *Pros:* Low risk, tests actual production traffic.
        *   *Cons:* Complex routing setup, session stickiness issues.
    *   **Rollback Strategy:**
        *   *Automated:* If the error rate exceeds a threshold (e.g., >1% of HTTP 5xx errors for 3 minutes) on the new deployment, Prometheus triggers an alert that triggers a CI/CD job to redeploy the previous stable image tag.
        *   *Database migrations:* Always design databases with backward-compatible migrations (e.g., never delete columns or rename them in one step; follow the Expand/Contract phase pattern).
*   **Real-world Example:**
    A GitHub Actions workflow utilizing AWS ECS to perform a Canary deployment by modifying Task Definition weights on an AWS Application Load Balancer.
*   **Common Mistakes:**
    *   Deploying non-backward-compatible database changes simultaneously with application code, preventing a clean rollback.
    *   Failing to run automated integration smoke tests on Canary environments before routing user traffic.
*   **Follow-up Interview Questions:**
    *   What is the difference between Continuous Delivery and Continuous Deployment? (Continuous Delivery requires manual approval before deploying to prod; Continuous Deployment automates deployment to prod directly after testing passes).
    *   How do you configure a rollback in Kubernetes? (`kubectl rollout undo deployment/<deployment-name>`).

</details>

---

# 15. Microservices Architecture

### ❓ Q40. Detail the Saga Pattern and Circuit Breaker Pattern.
<details>
<summary><b>👀 Show Answer</b></summary>

*   **Detailed Answer:**
    *   **Saga Pattern (Distributed Transactions):**
        In microservices, transactions cannot span multiple databases. The Saga pattern coordinates a series of local transactions across services.
        1.  Each service executes a local transaction.
        2.  If any step fails, the Saga orchestrator (or event-bus listener) executes **compensating transactions** in reverse order to roll back state changes (e.g., if inventory allocation fails after card charging, the payment service compensation cancels the charge).
    *   **Circuit Breaker Pattern:**
        Prevents cascade failures across services by monitoring external call errors. States include:
        1.  **Closed:** Normal operation. Calls pass through.
        2.  **Open:** Error rate exceeds threshold (e.g., 50% failures). External calls fail instantly without hitting the target service, saving resources.
        3.  **Half-Open:** After a timeout, a limited number of test calls pass through. If they succeed, the circuit closes; if they fail, it re-opens.
*   **Real-world Example:**
    Implementing a Circuit Breaker on an e-commerce platform using a Node.js library (`opossum`) around a credit card verification microservice.
*   **Common Mistakes:**
    *   Designing synchronous cascading HTTP calls across microservices, which increases latency and amplifies failures (use event-driven pub/sub for decoupling).
    *   Implementing compensating transactions that are not idempotent.
*   **Follow-up Interview Questions:**
    *   What is Distributed Tracing? (Injecting correlation IDs in request headers—like W3C Trace Context—to track a request's journey across multiple microservice boundaries via Jaeger/Zipkin).
    *   What is Service Discovery? (A dynamic registry—like Consul or Eureka—where microservice instances register their IP/port locations to coordinate routing).

</details>

---

# 16. Production Scenarios (50+ Real Incidents)

Here is a catalog of 50 production incidents, their root causes, and concrete resolutions:

<details>
<summary><b>🚨 Incidents 1–10: CPU & Memory Issues</b></summary>

| # | Incident | Root Cause Analysis (RCA) | Resolution |
| :--- | :--- | :--- | :--- |
| 1 | **Node.js 100% CPU lockup** | Synchronous CPU-bound `JSON.parse` of a 200MB configuration file on the main thread. | Migrated parser logic to a Worker Thread. |
| 2 | **Node.js Pod OOMKilled** | Memory leak caused by growing global array cache with no TTL. | Replaced local cache with Redis `SETEX` TTL cache. |
| 3 | **Node.js process blocks on crypto** | Heavy synchronous `crypto.pbkdf2Sync` blocking the single thread. | Swapped to async `crypto.pbkdf2` callback/promise implementation. |
| 4 | **Slow PM2 reload/restarts** | PM2 scaling instances sequentially on slow storage nodes. | Configured PM2 cluster mode with dynamic reload thresholds. |
| 5 | **Node.js Promise Unhandled Rejections** | Crash on unhandled exceptions in async fetch handlers. | Added a global `unhandledRejection` handler and explicit try-catch blocks. |
| 6 | **Docker container thrashing** | Memory limits set too low, causing OS paging onto swap files. | Adjusted container requests/limits with 30% safety headroom. |
| 7 | **Memory Leak in Socket.io** | Disconnected user sockets not releasing listener hooks. | Added `socket.removeAllListeners()` during disconnect events. |
| 8 | **Memory leak in Axios clients** | Unused axios instances caching configurations and interceptors in loop scopes. | Reused singleton Axios clients or instantiated custom connection managers. |
| 9 | **Nginx worker connection limits** | File descriptor limit exceeded under peak network load. | Increased OS file limits (`ulimit -n`) and Nginx `worker_connections`. |
| 10 | **High event loop delay** | Large array iterations (nested loops) blocking event loop execution. | Optimized algorithms to $O(N)$ or chunked iterations using `setImmediate`. |

</details>

<details>
<summary><b>🚨 Incidents 11–20: Database & Caching Outages</b></summary>

| # | Incident | Root Cause Analysis (RCA) | Resolution |
| :--- | :--- | :--- | :--- |
| 11 | **Slow MongoDB Reads** | Collection scan on `orders` table due to missing index. | Created compound index on queried fields: `userId` + `status`. |
| 12 | **Postgres connection pool limit** | Autoscaled application instances exhausted active connections. | Deployed pgBouncer connection pool multiplexer. |
| 13 | **Redis OOM (Out of Memory)** | Cache eviction policy set to `noeviction` under memory limit. | Configured eviction policy to `allkeys-lru`. |
| 14 | **MongoDB Transaction Lock** | Long-running transaction holding write lock on user profiles. | Reduced transaction scope, optimizing execution queries. |
| 15 | **SQL Database Deadlock** | Parallel threads locking products in different order updates. | Sorted inventory item IDs programmatically before updating DB. |
| 16 | **Redis Cache Stampede** | Top-selling product cache expired; thousands of queries hit DB at once. | Implemented lock-aside with random background refresh. |
| 17 | **Postgres Disk Space Exhausted** | Write-Ahead Log (WAL) files growing due to replication lag. | Tuned replica sync timeouts and optimized auto-vacuum thresholds. |
| 18 | **MongoDB Hot Shard** | Monotonically increasing ID used as shard key, routing all writes to one shard. | Changed shard key to hashed compound key. |
| 19 | **Redis Timeout Exceptions** | High latency queries blocking single-threaded Redis execution loop (e.g., `KEYS *`). | Replaced blocking commands with cursor-based `SCAN`. |
| 20 | **SQL N+1 Query latency** | ORM lazy-loading related reviews on catalog rendering. | Configured eager join fetches in ORM definitions. |

</details>

<details>
<summary><b>🚨 Incidents 21–30: Real-Time & WebRTC Issues</b></summary>

| # | Incident | Root Cause Analysis (RCA) | Resolution |
| :--- | :--- | :--- | :--- |
| 21 | **WebRTC Call Drops (Office users)** | Firewalls blocking direct peer connections. STUN failed. | Configured TURN server on port 443 with TLS transport fallback. |
| 22 | **Socket.io connection drops** | Load balancer routing client pings to different servers. | Enabled Sticky Sessions (ip_hash) on the Nginx load balancer. |
| 23 | **WebRTC Audio/Video Desync** | CPU throttled on client devices, delaying track render loops. | Implemented dynamic audio/video layout down-scaling. |
| 24 | **Socket server memory leak** | Unsent messages pile up in memory buffers of slow-client sockets. | Tuned `maxHttpBufferSize` and added client-read timeout drops. |
| 25 | **WebRTC Screen Share fails** | Dynamic codec negotiation mismatch during desktop streams. | Forced VP8/H264 fallback profiles in SDP signaling offers. |
| 26 | **WebSocket server crash** | File descriptor limits reached during high user sessions. | Configured `/etc/security/limits.conf` for higher socket files. |
| 27 | **WebRTC SFU CPU spike** | 20-user group call using mesh routing model. | Migrated room connection layouts from Peer-to-Peer to SFU. |
| 28 | **Presence System latency** | Heartbeat updates triggering event loops on every tick. | Batch presence notifications using Redis sorted set throttles. |
| 29 | **Socket.io handshake fails** | HTTP CORS origin headers missing on initial polling requests. | Added explicit origin configs in the Socket.io server builder. |
| 30 | **WebRTC connection timeout** | ICE candidates took too long to gather on slow client links. | Implemented Trickle ICE protocol to send candidates immediately. |

</details>

<details>
<summary><b>🚨 Incidents 31–40: Kubernetes & DevOps Crashes</b></summary>

| # | Incident | Root Cause Analysis (RCA) | Resolution |
| :--- | :--- | :--- | :--- |
| 31 | **Kubernetes CrashLoopBackOff** | Environment secrets missing in ConfigMaps/Vault configurations. | Added secret mount validation to container startup scripts. |
| 32 | **K8s Pods eviction** | Node disk filled up with Docker container execution stdout logs. | Implemented Docker log rotation config and set log limits. |
| 33 | **Kubernetes service 503 errors** | Pods receiving traffic before initialization completed. | Configured dynamic readiness probe definitions. |
| 34 | **Deployments stuck** | Rolling update failed as new image failed liveness checks. | Rolled back using `kubectl rollout undo` and fixed the bug. |
| 35 | **Canary traffic bypass** | Ingress routing weight configurations misaligned in DNS rules. | Synced Nginx ingress annotations weights in deployment charts. |
| 36 | **GitHub Actions build failure** | Node modules caching issues in pipeline runners. | Cleared action caches and pinned dependency hashes in lockfile. |
| 37 | **Kubernetes HPA thrashing** | CPU target limit set too low, causing scale up/down oscillations. | Adjusted scale cooldown periods and raised CPU scale targets. |
| 38 | **Containers unable to resolve DNS** | CoreDNS deployment overloaded inside Kubernetes cluster. | Scaled CoreDNS replica counts and implemented local DNS caches. |
| 39 | **Secret Key Leaks** | AWS access keys committed to a public Git repository. | Rotated all leaked AWS credentials and integrated git-secrets. |
| 40 | **Helm Upgrade Timeout** | PVC (Persistent Volume Claim) failed to unbind from old node. | Forced volume unmounting and set dynamic reclaim parameters. |

</details>

<details>
<summary><b>🚨 Incidents 41–50: Cloud, Nginx & API Latency</b></summary>

| # | Incident | Root Cause Analysis (RCA) | Resolution |
| :--- | :--- | :--- | :--- |
| 41 | **AWS Bill Cost Spike** | Idle CloudFront logs and unattached EBS storage volumes. | Configured automatic garbage collection scripts for AWS. |
| 42 | **Nginx 502 Bad Gateway** | Node.js backend crashed under load and failed to restart. | Deployed PM2 process monitor and configured auto-restarts. |
| 43 | **AWS CloudFront 504 Gateway** | ALB target groups timed out during long-running API tasks. | Delegated heavy API processes to background tasks. |
| 44 | **API latency increases** | Cascading microservice failures due to third-party outages. | Implemented circuit breaker (Resilience4j) with fallback data. |
| 45 | **AWS Lambda execution timeouts** | DB connections exhausted on cold starts. | Configured Amazon RDS Proxy to handle pooling. |
| 46 | **Nginx SSL handshake failure** | Outdated cipher configurations on clients. | Updated TLS configs using modern secure Mozilla standards. |
| 47 | **Route53 DNS resolution drops** | TTL set too high during load balancer transitions. | Reduced Route53 target group record TTL values to 60 seconds. |
| 48 | **CloudFront cache bypass** | Query strings dynamically updating cache keys on static assets. | Standardized query params and restricted cache key definitions. |
| 49 | **AWS IAM Permission Denied** | ECS task execution roles missing KMS decrypter permissions. | Updated IAM policies to allow KMS decryption access. |
| 50 | **API gateway rate limit drops** | IP spoofing bypasses limits due to un-configured headers. | Configured trust proxy headers on upstream reverse gateways. |

</details>

---

# 17. Coding Round Preparation

Here are three common challenges encountered in backend coding rounds:

<details>
<summary><b>🟢 Easy: Reverse a String In-Place (JS)</b></summary>

*   **Problem:** Write a function that takes an array of characters and reverses it in-place.
*   **Solution:**
    ```javascript
    function reverseStringInPlace(strArray) {
      let left = 0;
      let right = strArray.length - 1;
      while (left < right) {
        let temp = strArray[left];
        strArray[left] = strArray[right];
        strArray[right] = temp;
        left++;
        right--;
      }
      return strArray;
    }
    ```
*   **Time Complexity:** $O(N)$
*   **Space Complexity:** $O(1)$

</details>

<details>
<summary><b>🟡 Medium: Group Objects by Key (JS/Node)</b></summary>

*   **Problem:** Write a utility function that groups an array of objects by a specific property key.
*   **Solution:**
    ```javascript
    function groupBy(array, key) {
      return array.reduce((result, currentValue) => {
        const groupKey = currentValue[key];
        if (!result[groupKey]) {
          result[groupKey] = [];
        }
        result[groupKey].push(currentValue);
        return result;
      }, {});
    }
    ```
*   **Time Complexity:** $O(N)$
*   **Space Complexity:** $O(N)$

</details>

<details>
<summary><b>🔴 Hard: Token Bucket Rate Limiter (Node.js/Redis)</b></summary>

*   **Problem:** Implement a thread-safe Token Bucket rate limiter in Node.js.
*   **Solution:**
    ```javascript
    class TokenBucketLimiter {
      constructor(capacity, fillRatePerSec) {
        this.capacity = capacity;
        this.fillRate = fillRatePerSec;
        this.tokens = capacity;
        this.lastRefill = Date.now();
      }

      allowRequest(tokensRequested = 1) {
        const now = Date.now();
        const elapsed = (now - this.lastRefill) / 1000;
        this.lastRefill = now;

        // Refill tokens based on elapsed time
        this.tokens = Math.min(this.capacity, this.tokens + (elapsed * this.fillRate));

        if (this.tokens >= tokensRequested) {
          this.tokens -= tokensRequested;
          return true;
        }
        return false;
      }
    }
    ```
*   **Time Complexity:** $O(1)$
*   **Space Complexity:** $O(1)$

</details>

---

# 18. Rapid Fire Round (100+ Q&As)

<details>
<summary><b>⚡ Expand 100+ Rapid Fire Q&As</b></summary>

| # | Question | Concise Answer |
| :--- | :--- | :--- |
| 1 | Is Node.js single-threaded? | Yes, the main execution thread is single-threaded, though libuv executes I/O tasks in threads. |
| 2 | What is PM2? | A production process manager for Node.js applications with a built-in load balancer. |
| 3 | What is libuv? | The multi-platform support library with a focus on asynchronous I/O that powers Node.js. |
| 4 | How does MongoDB handle ACID? | MongoDB handles ACID transactions across multiple documents and replica sets since version 4.0. |
| 5 | What is a database index? | A data structure (like B-Tree) that speeds up data retrieval operations on a table. |
| 6 | What is the difference between SQL and NoSQL? | SQL databases are relational and schema-strict; NoSQL is non-relational and schema-flexible. |
| 7 | What is Redis? | An in-memory key-value data store used as a database, cache, and message broker. |
| 8 | What is the default eviction policy in Redis? | `noeviction` (returns error when memory is full). |
| 9 | What does CORS stand for? | Cross-Origin Resource Sharing. |
| 10 | What is a JWT? | JSON Web Token, a stateless method of representing user authentication claims. |
| 11 | Where should you store JWTs? | In a secure, `HttpOnly`, `SameSite=Strict` cookie to prevent XSS theft. |
| 12 | What is Docker? | A platform to containerize applications, packaging code and dependencies together. |
| 13 | What is a Kubernetes Pod? | The smallest deployable computing unit, hosting one or more shared containers. |
| 14 | What is Ingress in Kubernetes? | An API object managing external HTTP routing access to services. |
| 15 | What is AWS EC2? | Elastic Compute Cloud, virtual servers in the Amazon cloud. |
| 16 | What is AWS S3? | Simple Storage Service, an object storage service for backups and static files. |
| 17 | What is an ALB on AWS? | Application Load Balancer, routes Layer 7 HTTP traffic across target paths. |
| 18 | What is Nginx? | A high-performance web server, reverse proxy, and load balancer. |
| 19 | What is CI/CD? | Continuous Integration and Continuous Delivery/Deployment automation pipeline. |
| 20 | What is a microservice? | An architectural pattern that structures an app as a collection of decoupled services. |
| 21 | What is the event loop? | Mechanism enabling Node to perform non-blocking I/O operations by offloading tasks to the OS. |
| 22 | What is a Promise in JS? | An object representing the eventual completion or failure of an asynchronous operation. |
| 23 | Explain `async/await` in JS. | Syntactic sugar built on top of Promises to write cleaner asynchronous code. |
| 24 | What is a closure in JS? | A function retaining references to its surrounding lexical state variables. |
| 25 | What is hosting in JS? | Compilation phase behavior moving declarations to the top of their scope. |
| 26 | What is React Virtual DOM? | A lightweight VDOM tree used to compute minimal real DOM updates via diffing. |
| 27 | What is React Fiber? | The rewrite of React's reconciliation engine, enabling pause/resume rendering tasks. |
| 28 | What is the purpose of `useEffect`? | Handles side effects (data fetching, DOM updates) in React functional components. |
| 29 | What is Redux? | A predictable state container for JavaScript apps using a single global store. |
| 30 | What is Tailwind CSS? | A utility-first CSS framework for rapid UI styling. |
| 31 | How does Tailwind JIT work? | Compiles styles dynamically in real-time by scanning files for written classes. |
| 32 | What is OAuth2? | An authorization framework enabling applications to obtain limited access to user accounts. |
| 33 | What is XSS? | Cross-Site Scripting, injecting malicious client-side scripts into web pages. |
| 34 | What is CSRF? | Cross-Site Request Forgery, forcing logged-in users to submit requests unknowingly. |
| 35 | How do you prevent SQL Injection? | Use parameterized prepared queries and sanitize inputs. |
| 36 | What is pgBouncer? | A connection pooler for PostgreSQL that minimizes connection overhead. |
| 37 | What is Redis Pub/Sub? | A lightweight messaging paradigm where publishers broadcast to channel listeners. |
| 38 | What is the Redlock algorithm? | A Redis algorithm to acquire distributed locks across multiple master nodes. |
| 39 | Compare Redis RDB vs AOF. | RDB takes periodic snapshots; AOF logs every write command for higher durability. |
| 40 | What is STUN in WebRTC? | Session Traversal Utilities for NAT, discovers a client's public IP address. |
| 41 | What is TURN in WebRTC? | Traversal Using Relays around NAT, acts as a fallback media relay server. |
| 42 | What is an SFU? | Selective Forwarding Unit, routes media streams without decoding them. |
| 43 | What is a MCU? | Multipoint Control Unit, decodes and mixes all media streams into one. |
| 44 | What is presence tracking? | Monitoring and broadcasting user online status changes. |
| 45 | Explain Blue-Green deployment. | Maintaining two identical environments to ensure instant routing switches. |
| 46 | Explain Canary deployment. | Deploying updates incrementally to a small subset of servers to monitor metrics. |
| 47 | What is a Circuit Breaker? | A pattern that stops API calls to failing services, preventing cascading crashes. |
| 48 | What is Saga pattern? | Coordinates distributed transactions using a sequence of compensating steps. |
| 49 | What is Kubernetes HPA? | Horizontal Pod Autoscaler, scales replica sets based on CPU/memory usage. |
| 50 | What is AWS Route 53? | A scalable Domain Name System (DNS) web service. |
| 51 | What is serverless (AWS Lambda)? | Compute service running code in response to events, managing resources automatically. |
| 52 | What is a Docker volume? | A persistent data storage mechanism mapping container files to host folders. |
| 53 | What is `setImmediate` in Node? | Schedules script execution in the Check phase of the Event Loop. |
| 54 | What is `process.nextTick`? | Runs callbacks immediately after the current operation, before event loop phases. |
| 55 | What is a Buffer in Node? | A block of memory outside the V8 heap for holding raw binary data. |
| 56 | What is a stream backpressure? | Queue congestion when reads exceed writes, resolved by pausing readable streams. |
| 57 | What is npm audit? | A command-line tool that scans Node.js projects for security vulnerabilities. |
| 58 | What is package-lock.json? | A lockfile that records the exact version of installed npm packages for reproducible builds. |
| 59 | What is a memory heap? | The area in memory where JavaScript objects and reference variables are allocated.
| 60 | What is a compound index? | A database index created on multiple columns of a table. |
| 61 | What is a covered query? | A query fully satisfied by index values without looking up database records. |
| 62 | What is MongoDB COLLSCAN? | Collection Scan, scanning every single document (indicates missing index). |
| 63 | Explain SQL JOIN. | Combines rows from two or more tables based on a related column. |
| 64 | What is MVCC? | Multi-Version Concurrency Control, allows non-locking database reads. |
| 65 | How do you detect SQL deadlocks? | The database engine automatically detects circular locks and aborts one. |
| 66 | What is SQL partitioning? | Splitting large tables horizontally into smaller, manageable tables. |
| 67 | What is Cache-Aside caching? | The application checks the cache, falling back to the database on a cache miss. |
| 68 | What is Cache Penetration? | Flooding cache requests for non-existent database keys (mitigated by Bloom filters). |
| 69 | What is Trickle ICE? | WebRTC protocol that transmits ICE candidates to peers as they are gathered. |
| 70 | What is DTLS-SRTP? | Encryption protocols securing WebRTC media channels. |
| 71 | What is a Helm Chart? | Package manager for Kubernetes, organizing resource templates. |
| 72 | What is Prometheus? | Open-source systems monitoring and alerting toolkit. |
| 73 | What is Grafana? | Visualization tool for metrics, creating real-time monitoring dashboards. |
| 74 | What is AWS IAM? | Identity and Access Management, controls user and service resource permissions. |
| 75 | What is AWS CloudFront? | Content Delivery Network (CDN) caching files at global edge locations. |
| 76 | What is `useMemo` in React? | Hook memoizing expensive calculations to skip redundant executions. |
| 77 | What is `useCallback`? | Hook memoizing inline function references to prevent child re-renders. |
| 78 | What is React Query caching? | Automated management of server state queries, reducing custom network logic. |
| 79 | What is the Temporal Dead Zone? | Time between `let`/`const` variable hoisting and its actual initialization line. |
| 80 | Explain CSS Grid vs Flexbox. | Flexbox is one-dimensional (row/column); Grid is two-dimensional (both). |
| 81 | What is OWASP? | Open Web Application Security Project, standardizing web security awareness. |
| 82 | Explain SameSite cookie attribute. | Restricts cookies from being sent in cross-site requests, mitigating CSRF. |
| 83 | What does `docker build --no-cache` do? | Forces rebuilding all layers from scratch, ignoring cached states. |
| 84 | What is Kubernetes Ingress Controller? | Deploys reverse proxy servers (like Nginx) to fulfill ingress rules. |
| 85 | What is StatefulSet in Kubernetes? | Manages stateful pods, maintaining stable IDs and persistent storage links. |
| 86 | What is AWS Auto Scaling? | Automatically adjusts compute resources dynamically matching active traffic load. |
| 87 | What is Nginx proxy_cache? | Direct caching of backend upstream responses inside Nginx folder paths. |
| 88 | What is Linux systemd? | System and service manager, initiating background services and boot environments. |
| 89 | What does `grep -r` do? | Recursively searches directories for files containing matching string patterns. |
| 90 | What is git-secrets? | Tool scanning commit strings to block commits containing sensitive tokens. |
| 91 | Explain REST API statelessness. | The server stores no client session context; requests must contain all credentials. |
| 92 | What is an API Gateway? | A gateway proxy managing authentication, rate limiting, and request routing. |
| 93 | What is Distributed Tracing correlation ID? | A unique transaction ID passed across microservices to group request logs. |
| 94 | What is a compensating transaction? | A transaction reversing database changes if a step in a Saga workflow fails. |
| 95 | What is a Kubernetes Service? | Logical abstraction mapping a stable network IP/DNS to active pods. |
| 96 | What is AWS Lambda cold start? | Init latency when a serverless function executes for the first time in a new environment. |
| 97 | How do you analyze slow SQL queries? | Run `EXPLAIN ANALYZE` and look for table scans or index misses. |
| 98 | What is the difference between `let` and `var`? | `let` is block-scoped and temporal-dead-zone bound; `var` is function-scoped. |
| 99 | What is a Docker Multi-stage build? | Pattern building images across stages, producing compact output containers. |
| 100 | What is dynamic import in JS? | Loading JS files asynchronously on-demand using `import()`. |
| 101 | What is a mock in unit testing? | An object mimicking the behavior of a real dependency for testing isolation. |

</details>

---

# 19. Final Revision Sheet (1-Day Revision Cheat Sheet)

Use this sheet as a quick reference check the day before your interview.

### 🚀 Key Architectures
*   **WebRTC Signaling:** SDP Offer/Answer over WebSockets. Media flows directly P2P or relayed through TURN.
*   **Double-Entry Ledger:** Balance updates must write credit and debit rows concurrently inside a SQL transaction block.
*   **Stateless Scaling:** Issue signed JWTs, validate dynamically, store refresh tokens in `HttpOnly` rotation cookies.

### 🛠️ Key Commands Cheat Sheet
*   `kubectl get pods -n <namespace>` — Lists active cluster pods.
*   `kubectl logs -f <pod-name>` — Streams container stdout logs.
*   `docker build -t app:latest .` — Compiles a Docker image.
*   `htop` — Real-time processor and RAM inspection.
*   `netstat -tlpn` — Lists active server sockets and listening ports.
*   `explain analyze <query>` — Executes and measures SQL query execution plans.

### 📝 Core Checklist
1.  **Event Loop:** Microtasks (Promises) run immediately after current tasks; Macrotasks (`setTimeout`) run next.
2.  **Thread Safety:** Use atomic classes, volatile flags, synchronized monitors, or ConcurrentHashMap locks.
3.  **Indexing Rule:** Compound indexes follow Equality -> Sort -> Range order.
4.  **K8s Probes:** Readiness probe controls traffic routing; Liveness probe controls pod restarts.

