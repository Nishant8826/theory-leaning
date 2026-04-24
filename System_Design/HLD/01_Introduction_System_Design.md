# 📌 Introduction to System Design

## 🧠 Concept Explanation (Story Format)

Imagine you just built a cool Instagram-like photo sharing app using React + Node.js. It's working perfectly for your 10 friends. But suddenly, 1 million people want to use it!

What happens?
- Your single Node.js server **crashes** under load
- Your MongoDB instance **runs out of memory**
- Users in Tokyo get **slow responses** because your server is in Ohio
- Your app goes **down** when you deploy a new version

**This is exactly why System Design exists.**

System Design is the art of planning how your application will work **at scale**. It answers questions like:
- How do we handle 10 million users?
- What if our database server dies?
- How do we serve images fast to users in Japan?
- How do we deploy without downtime?

---

## 🏗️ Basic Design (Naive)

When you first build an app, it usually looks like this:

```
[React Frontend]
      ↓
[Node.js Server]
      ↓
[MongoDB Database]
```

**Problems with this:**
- One server handles EVERYTHING (auth, business logic, file storage)
- One database = single point of failure
- If the server goes down → app is dead
- Can't scale individual parts independently

---

## ⚡ Optimized Design

A production-ready system looks like this:

```
[React / Next.js Frontend]
        ↓
   [AWS CloudFront CDN]        ← Serves static files globally fast
        ↓
   [AWS API Gateway]           ← Manages traffic, routes requests
        ↓
   [Load Balancer]             ← Distributes traffic to multiple servers
      ↙    ↘
[Node.js]  [Node.js]          ← Multiple server instances
      ↓         ↓
   [Redis Cache]               ← Fast in-memory data store
      ↓
[MongoDB]  [PostgreSQL]        ← Persistent storage
      ↓
   [AWS S3]                    ← Object storage for images/videos
```

---

## 🔍 Key Components

### 1. Frontend (React / Next.js)
- The user interface your users see
- Makes API calls to the backend
- Deployed on Vercel or AWS S3 + CloudFront

### 2. API Gateway (AWS API Gateway)
- Entry point for all client requests
- Handles authentication tokens, rate limiting
- Routes requests to the right microservice

### 3. Node.js Backend
- Business logic lives here
- Processes requests, talks to database
- Can run multiple instances behind a load balancer

### 4. Redis Cache
- Stores frequently accessed data in memory
- Example: Store user sessions, trending posts count
- 100x faster than reading from database

### 5. Database (MongoDB / PostgreSQL)
- **MongoDB** → For flexible, document-based data (posts, comments)
- **PostgreSQL** → For structured, relational data (users, transactions)

### 6. AWS S3
- Stores files, images, videos
- Cheap, durable, infinitely scalable

---

## ⚖️ Trade-offs

| Simple Design | Scaled Design |
|--------------|---------------|
| Easy to build | Complex to build and maintain |
| Cheap to run | More expensive (multiple servers) |
| Hard to scale | Easy to scale individual parts |
| Single point of failure | Highly available |

---

## 📊 Scalability Discussion

**Vertical Scaling (Scale Up):**
- Make your single server bigger (more RAM, more CPU)
- Simple but has limits — you can't add RAM forever
- Example: Upgrade EC2 from t2.micro to c5.4xlarge

**Horizontal Scaling (Scale Out):**
- Add more servers
- Use a Load Balancer to distribute traffic
- This is what companies like Instagram and Netflix do

---

## 💼 Interview Questions (WITH SOLUTIONS)

### Q1: What is the difference between HLD and LLD?

**Solution:**
- **HLD (High Level Design):** The big picture. Which services do we use? How do components talk to each other? Example: "We'll use Redis for caching and PostgreSQL for storage."
- **LLD (Low Level Design):** The details. What classes do we write? What are the API schemas? What database schema do we use?
- Think of HLD as the **architect's blueprint** and LLD as the **engineer's implementation plan**.

---

### Q2: Why do we need a Load Balancer?

**Solution:**
- Without a load balancer, all traffic goes to one server. When it crashes → app is down.
- A load balancer sits in front of multiple Node.js servers. It distributes incoming requests.
- AWS offers **ALB (Application Load Balancer)** — we can use it with Node.js servers on EC2.
- If one server crashes, the load balancer routes traffic to the healthy ones automatically.

---

### Q3: What is the role of Redis in a system?

**Solution:**
- Redis is an in-memory key-value store. It's **blazingly fast** (microseconds vs milliseconds for DB).
- Common uses:
  - **Session storage:** Store JWT tokens or user sessions
  - **Caching:** Cache popular posts or user profiles
  - **Rate limiting:** Count API calls per user
  - **Pub/Sub:** Real-time notifications
- In Node.js, we use the `ioredis` library to connect to Redis.

---

### Q4: How do you ensure your app doesn't go down during deployment?

**Solution:**
- Use **Rolling Deployment:** Update servers one by one, not all at once
- Use **Blue-Green Deployment:** Run two identical environments (Blue=live, Green=new). Switch traffic when Green is ready.
- With AWS, use **Elastic Beanstalk** or **ECS** for zero-downtime deployments
- Use **health checks** so the load balancer knows which servers are ready

---

### Q5: A startup says "We'll design for scale from day one." Is this a good idea?

**Solution:**
- **No, usually not.** This is called **over-engineering**.
- First, validate your product. Build the simplest thing that works.
- Start with a monolith (single Node.js app + MongoDB). It's easy to build and deploy.
- Only add complexity (microservices, caching, queues) when you actually hit scaling problems.
- Famous quote: *"Premature optimization is the root of all evil"* — Donald Knuth

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem 1: Your e-commerce site is getting 100x more traffic during a sale. What do you do?

**Solution:**
1. **Pre-scale:** Add more Node.js instances on EC2 before the sale starts (AWS Auto Scaling)
2. **Cache product pages:** Use Redis to cache product listings so DB isn't hammered
3. **Use a CDN:** Static assets (images, CSS) served from CloudFront, not your server
4. **Queue purchases:** Use a message queue (like AWS SQS) to handle order processing asynchronously
5. **Read replicas:** Add PostgreSQL read replicas so read traffic doesn't slow down writes

---

### Problem 2: Your Node.js app is slow. How do you diagnose and fix it?

**Solution:**
1. **Add monitoring:** Use AWS CloudWatch or tools like New Relic to find bottlenecks
2. **Check database queries:** Slow queries with missing indexes are the #1 cause
3. **Add Redis caching:** Cache results of expensive DB queries
4. **Profile your Node.js code:** Use `clinic.js` or Node's built-in profiler
5. **Check network latency:** Is your database in a different region than your server?

---

### Problem 3: Draw the system architecture for a simple blog app that needs to handle 1 million users.

**Solution:**
```
Users (React)
    ↓
CloudFront CDN (static assets)
    ↓
AWS API Gateway
    ↓
ALB (Load Balancer)
    ↙      ↘
Node.js   Node.js   (EC2 Auto Scaling Group)
    ↓
Redis (session + post caching)
    ↓
PostgreSQL (RDS) ← Primary
    ↓
PostgreSQL Read Replica (for read-heavy queries)
    ↓
S3 (image storage)
```

---

### Navigation
**Prev:** None | **Index:** [00_Index.md](../00_Index.md) | **Next:** [02_Scalability_Basics.md](02_Scalability_Basics.md)
