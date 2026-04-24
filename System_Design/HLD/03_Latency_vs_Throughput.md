# 📌 Latency vs Throughput

## 🧠 Concept Explanation (Story Format)

Imagine you run a restaurant (your Node.js API server). Two things matter:

1. **How fast does a single customer get their food?** → This is **Latency**
2. **How many customers can you serve per hour?** → This is **Throughput**

A slow waiter (high latency) who serves 5 tables = bad.
A fast waiter (low latency) who serves 50 tables/hour = great throughput.

In system design, **you often have to choose** — optimizing for one can hurt the other.

**Real Example: Instagram Stories**
- Loading your feed: Low latency is critical (users leave if it takes >3 seconds)
- Processing video uploads: Throughput matters more (encode 1 million videos/day)

---

## 🏗️ Basic Design (Naive)

```
User → [Node.js Server] → [MongoDB]
         ↑
   Every request hits DB!
   Each query takes 50-200ms
   100 concurrent users = DB gets hammered
   Latency spikes under load
```

**Problems:**
- No caching → every request hits the DB (high latency)
- Single server → can't handle many requests at once (low throughput)
- Synchronous processing → slow tasks block other requests

---

## ⚡ Optimized Design

```
User Request
    ↓
[API Gateway]
    ↓
[Node.js Server]
    ↓
  [Redis Cache]  ← Try cache first (1-2ms response!)
    ↓ (cache miss)
[PostgreSQL/MongoDB]  ← Only if not in cache (50-200ms)

For heavy tasks:
[Node.js] → [AWS SQS Queue] → [Lambda Worker] → [DB]
   ↑                                               ↑
   Return 202 Accepted immediately              Process async
   (low latency!)                               (high throughput!)
```

---

## 🔍 Key Components

### Latency Numbers You Must Know

```
Operation                          Latency
-----------------------------------------
L1 cache reference                 0.5 ns
L2 cache reference                 7 ns
RAM access                         100 ns
Redis (in-memory cache)            ~1 ms
Same datacenter network roundtrip  ~0.5 ms
PostgreSQL query (with index)      1-10 ms
PostgreSQL query (without index)   100ms-10s
MongoDB query                      5-20 ms
S3 file fetch                      50-200 ms
Cross-region network               100-200 ms
```

### Throughput Concepts

**RPS (Requests Per Second):** How many requests your server can handle per second.

A typical Node.js server:
- Simple API (no DB): ~10,000 RPS
- API with Redis cache: ~2,000 RPS
- API with DB query: ~500 RPS

**Key insight:** Adding Redis cache can increase your effective throughput by **4x** by reducing DB calls.

---

## ⚖️ Trade-offs

| Optimize for Latency | Optimize for Throughput |
|---------------------|------------------------|
| Cache everything in Redis | Process in batches |
| Use CDN for static assets | Use async queues (SQS) |
| Minimize DB queries | Use bulk inserts |
| Return early (async processing) | Process multiple items at once |
| Pre-compute results | Pipeline operations |

**The tension:** 
- If you batch operations for throughput → users wait longer (higher latency)
- If you respond immediately for latency → you process fewer items efficiently (lower throughput)

---

## 📊 Scalability Discussion

### How to Measure

```javascript
// Measuring latency in Node.js
const start = Date.now();
const result = await db.query('SELECT * FROM users WHERE id = $1', [userId]);
const latency = Date.now() - start;
console.log(`Query latency: ${latency}ms`);

// Or use built-in performance API
const { performance } = require('perf_hooks');
const t0 = performance.now();
// ... operation ...
const t1 = performance.now();
console.log(`Operation took ${t1 - t0} ms`);
```

### P50, P95, P99 Latency

Don't just measure average latency — it lies!

```
If 99 users get 10ms response and 1 user gets 10 seconds:
Average = (99 * 10 + 10000) / 100 = 109ms  ← Looks fine!
P99 = 10,000ms  ← But 1% of users wait 10 SECONDS!
```

**Always measure:**
- **P50:** 50% of requests are faster than this (median)
- **P95:** 95% of requests are faster than this
- **P99:** 99% of requests are faster than this (your slowest users)

Use **AWS CloudWatch** to track P99 latency of your API Gateway.

---

## 💼 Interview Questions (WITH SOLUTIONS)

### Q1: What is the difference between latency and throughput?

**Solution:**
- **Latency:** Time for ONE request to complete. Measured in ms. User experience metric.
- **Throughput:** Number of requests processed per unit time. Measured in RPS (requests/sec). System capacity metric.
- Example: A highway with 8 lanes (high throughput) but a speed limit of 30mph (high latency) vs a single lane highway at 100mph (low throughput, low latency).
- In system design, optimize latency for real-time user-facing APIs, and throughput for background batch processing.

---

### Q2: How does Redis improve latency?

**Solution:**
- Redis stores data in RAM (not disk). RAM access is ~100,000x faster than disk.
- Instead of a 50ms PostgreSQL query, Redis returns data in <1ms.
- Implementation in Node.js:

```javascript
const redis = require('ioredis');
const client = new redis(process.env.REDIS_URL);

async function getUserProfile(userId) {
  // Try cache first
  const cached = await client.get(`user:${userId}`);
  if (cached) {
    return JSON.parse(cached); // ~1ms
  }
  
  // Cache miss: hit database
  const user = await db.query('SELECT * FROM users WHERE id = $1', [userId]);
  
  // Store in cache for 1 hour
  await client.setex(`user:${userId}`, 3600, JSON.stringify(user.rows[0]));
  
  return user.rows[0]; // ~50ms (only on cache miss)
}
```

---

### Q3: How do you use async processing to reduce latency?

**Solution:**
- Instead of doing slow work synchronously (making user wait), put work in a queue and return immediately.
- Example: User uploads a video. Instead of encoding it (which takes minutes), return "Upload successful!" and process it in background.

```javascript
// ✅ Async pattern with SQS
app.post('/upload-video', async (req, res) => {
  const videoKey = await uploadToS3(req.file); // Fast: just upload raw file
  
  // Put encoding task in queue
  await sqs.sendMessage({
    QueueUrl: process.env.VIDEO_QUEUE_URL,
    MessageBody: JSON.stringify({ videoKey, userId: req.user.id })
  }).promise();
  
  // Return immediately — low latency for user!
  res.status(202).json({ message: 'Video uploaded, processing started', videoKey });
});

// Background worker (Lambda or separate Node process)
async function processVideo(message) {
  const { videoKey, userId } = JSON.parse(message.Body);
  await encodeVideo(videoKey); // Takes 2-5 minutes, but user isn't waiting!
  await notifyUser(userId, 'Your video is ready!');
}
```

---

### Q4: Your API has P99 latency of 5 seconds. How do you fix it?

**Solution:**
1. **Find the slowest requests:** Check CloudWatch logs, sort by response time
2. **Check DB queries:** Use `EXPLAIN ANALYZE` in PostgreSQL to find missing indexes
3. **Check for N+1 queries:** Are you querying the DB in a loop?

```javascript
// ❌ N+1 Query - Very slow!
const posts = await Post.findAll(); // 1 query
for (const post of posts) {
  post.author = await User.findById(post.authorId); // N queries!
}

// ✅ Single join query - Fast!
const posts = await Post.findAll({ include: User }); // 1 query total
```

4. **Add indexes** on frequently queried columns
5. **Cache the slowest responses** in Redis
6. **Set timeouts** so slow requests fail fast instead of hanging

---

### Q5: Compare batch processing vs stream processing for throughput.

**Solution:**
- **Batch Processing:** Collect data, process all at once. High throughput, high latency.
  - Example: Process all transactions from the day, generate reports at midnight
  - Use: AWS Lambda triggered by schedule, or bulk MongoDB operations
- **Stream Processing:** Process data as it arrives. Lower latency, slightly lower throughput.
  - Example: Real-time fraud detection, live sports scores
  - Use: AWS Kinesis, Socket.IO, Redis Pub/Sub

For a payments system: use stream processing for fraud detection (low latency critical) but batch processing for monthly statements (throughput matters, not latency).

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem 1: Your checkout API takes 800ms. Product manager wants it under 200ms. How?

**Solution:**
1. **Profile:** Add timing logs at each step. Find which step is slow.
2. **Likely culprits:**
   - DB query without index: Add index on `product_id`, `user_id`
   - Calling external payment API synchronously: Make it async if possible
   - Multiple sequential DB queries: Parallelize with `Promise.all()`
   
```javascript
// ❌ Sequential (slow)
const user = await getUser(userId);       // 50ms
const cart = await getCart(userId);       // 50ms
const inventory = await checkInventory(); // 50ms
// Total: 150ms sequential

// ✅ Parallel (fast)
const [user, cart, inventory] = await Promise.all([
  getUser(userId),       // \
  getCart(userId),       //  All run simultaneously!
  checkInventory()       // /
]);
// Total: ~50ms (limited by slowest)
```

---

### Problem 2: Design a system that processes 1 million image uploads per day with fast user response

**Solution:**
```
User uploads image
    ↓
[Node.js API] → Upload raw image to S3 (fast, ~200ms)
    ↓
Return 202 Accepted to user (low latency!)
    ↓ (async)
S3 triggers Lambda
    ↓
Lambda resizes image, generates thumbnails
    ↓
Store thumbnails back in S3
    ↓
Update MongoDB record with thumbnail URLs
    ↓
Send push notification to user: "Image processed!"
```

- User gets response in ~300ms (low latency ✓)
- System processes 1M images/day using Lambda auto-scaling (high throughput ✓)

---

### Navigation
**Prev:** [02_Scalability_Basics.md](02_Scalability_Basics.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [04_Load_Balancing.md](04_Load_Balancing.md)
