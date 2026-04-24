# 📌 Scalability Basics

## 🧠 Concept Explanation (Story Format)

Think about Instagram in 2010 — it had 13 employees and 30 million users. How? They built their system to **scale**.

Scaling means: **your system can handle more load without breaking.**

You're running a Node.js API for a food delivery app. Right now, 100 users order food at the same time. Your server handles it fine. But on New Year's Eve, 50,000 users order at once. What happens?

Without scalability planning → your server dies, orders are lost, customers are angry.

With scalability planning → you spin up 20 more servers automatically, everyone gets their food.

---

## 🏗️ Basic Design (Naive)

```
All users → [Single Node.js Server] → [Single MongoDB]
```

**What breaks?**
- The server has limited CPU and RAM
- One slow query can block all other requests (Node.js is single-threaded!)
- You cannot update the server without downtime
- The database becomes a bottleneck under heavy reads/writes

---

## ⚡ Optimized Design

```
Users
  ↓
[AWS ALB - Load Balancer]
  ↙   ↓   ↘
[N1] [N2] [N3]   ← Node.js servers (Auto Scaling Group on EC2)
  ↓
[ElastiCache Redis]   ← Cache layer
  ↓
[RDS PostgreSQL Primary]  ←→  [Read Replica 1] [Read Replica 2]
  ↓
[S3 for static files]
```

---

## 🔍 Key Components

### Vertical Scaling (Scale Up)
- Upgrade your single machine: more CPU, more RAM, faster disk
- Example: Move from AWS `t2.micro` (1 vCPU, 1GB RAM) to `c5.4xlarge` (16 vCPU, 32GB RAM)
- **Limit:** You can't add RAM/CPU forever. Eventually you hit the max machine size.
- **When to use:** Quick fix, early stage, databases (databases are hard to run on multiple machines)

### Horizontal Scaling (Scale Out)
- Add more machines, all running the same code
- AWS Auto Scaling Group: automatically adds/removes EC2 instances based on CPU usage
- **Requirement:** Your app must be **stateless** — no user session stored in server memory!
  - Use Redis to store sessions instead of server memory
- **When to use:** Long-term, web servers, API servers

### Stateless vs Stateful

```javascript
// ❌ BAD: Stateful server (session in memory)
const sessions = {}; // stored on THIS server only
app.post('/login', (req, res) => {
  sessions[userId] = { loggedIn: true };
});

// ✅ GOOD: Stateless server (session in Redis)
const redis = require('ioredis');
const client = new redis();
app.post('/login', async (req, res) => {
  await client.set(`session:${userId}`, JSON.stringify({ loggedIn: true }), 'EX', 3600);
});
```

---

## ⚖️ Trade-offs

| Vertical Scaling | Horizontal Scaling |
|-----------------|-------------------|
| Simple — no code changes | Requires stateless app design |
| Has hard limits | Virtually unlimited |
| Single point of failure | Highly available |
| Cheaper initially | More complex (load balancer needed) |
| Good for databases | Good for API servers |

---

## 📊 Scalability Discussion

### Estimating Scale

Before designing, always estimate your scale:

```
Daily Active Users (DAU): 1 million
Requests per user per day: 10
Total requests/day: 10 million
Requests/second (avg): 10M / 86400s ≈ 115 req/sec
Peak (assume 3x avg): 345 req/sec

Node.js server handles ≈ 1000 req/sec (I/O bound)
→ We need at least 1 server, but 3 for reliability
```

### AWS Auto Scaling Setup
```
Min instances: 2 (always on for high availability)
Max instances: 10 (cap costs during viral spikes)
Scale up when: CPU > 70% for 3 minutes
Scale down when: CPU < 30% for 5 minutes
```

---

## 💼 Interview Questions (WITH SOLUTIONS)

### Q1: What is the difference between vertical and horizontal scaling?

**Solution:**
- **Vertical:** Bigger machine. Simple, no code changes, but limited and expensive at top-end. Good for databases.
- **Horizontal:** More machines. Requires stateless design and load balancer. Unlimited in theory. Good for API servers.
- In practice, most systems use **both**: databases scale vertically + read replicas, API servers scale horizontally.

---

### Q2: How do you make a Node.js app horizontally scalable?

**Solution:**
1. **No in-memory state:** Move sessions to Redis (`express-session` with `connect-redis`)
2. **No local file storage:** Upload files to S3, not the server's disk
3. **Externalize config:** Use environment variables, not hardcoded values
4. **Idempotent operations:** Same request → same result, even if processed twice
5. **Health check endpoint:** `GET /health` returns 200 so load balancer knows server is alive

```javascript
// Health check endpoint
app.get('/health', (req, res) => {
  res.status(200).json({ status: 'ok', uptime: process.uptime() });
});
```

---

### Q3: What is the "thundering herd" problem and how do you solve it?

**Solution:**
- **Problem:** Cache expires → thousands of requests hit DB at once → DB crashes
- **Solution 1:** Cache locking — only one request rebuilds cache, others wait
- **Solution 2:** Staggered TTLs — add random jitter to expiry times

```javascript
// Add jitter to TTL to prevent thundering herd
const baseTTL = 3600; // 1 hour
const jitter = Math.floor(Math.random() * 300); // 0-5 min random
await redis.set(key, value, 'EX', baseTTL + jitter);
```

---

### Q4: Your app receives a sudden 10x spike in traffic. Walk me through your response.

**Solution:**
1. **Immediate:** AWS Auto Scaling adds more EC2 instances automatically
2. **Check:** Is Redis cache working? Cached responses don't hit DB
3. **Check:** Is CloudFront serving static assets? Reduces Node.js load
4. **If DB is struggling:** Enable read replicas, route read traffic there
5. **If still struggling:** Enable request queuing — put requests in SQS, process async
6. **Post-mortem:** Set better auto-scaling policies, add more cache, optimize slow queries

---

### Q5: How do you test if your system is scalable?

**Solution:**
- **Load Testing:** Use tools like `k6`, `Artillery`, or `Apache JMeter`
- Simulate thousands of concurrent users
- Find the breaking point (when does response time degrade?)
- Example with Artillery:

```yaml
# artillery-config.yml
config:
  target: 'http://your-api.com'
  phases:
    - duration: 60
      arrivalRate: 100   # 100 users/sec for 60 seconds
scenarios:
  - flow:
      - get:
          url: '/api/posts'
```

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem 1: Design a system that can handle Black Friday traffic (100x normal load)

**Solution:**
1. **Predict:** Use historical data to know peak traffic time
2. **Pre-scale:** Increase min instances in Auto Scaling Group before Black Friday
3. **Cache aggressively:** Cache product catalog in Redis (data doesn't change often)
4. **Async checkout:** Put orders in SQS queue, process asynchronously
5. **Disable non-critical features:** Turn off recommendation engine, analytics
6. **Circuit breaker:** If payment service is down, queue the order and retry

---

### Problem 2: Your single MongoDB server is at 90% CPU. What do you do?

**Solution:**
1. **Short term:** Add Redis caching to reduce DB reads. Cache frequent queries.
2. **Medium term:** Add MongoDB read replicas. Route read queries to replicas.
3. **Long term:** Shard MongoDB. Split data across multiple servers by userId or region.
4. **Check:** Are there missing indexes? `db.collection.explain("executionStats")` to diagnose.
5. **Archive:** Move old data to cheaper storage (S3 + AWS Athena for querying).

---

### Problem 3: Explain how Instagram handles 1 billion users with limited servers

**Solution:**
- **CDN:** Photos/videos served from CloudFront edge locations near users
- **Caching:** Redis caches feeds, follower counts, popular posts
- **Sharding:** User data split across many DB servers by user_id
- **Async processing:** When you post a photo, fan-out to followers is done by background workers
- **Read replicas:** Most Instagram traffic is reads (scrolling feed), served by replicas
- **Horizontal scaling:** Thousands of identical API server instances behind load balancers

---

### Navigation
**Prev:** [01_Introduction_System_Design.md](01_Introduction_System_Design.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [03_Latency_vs_Throughput.md](03_Latency_vs_Throughput.md)
