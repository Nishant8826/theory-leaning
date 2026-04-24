# 📌 Load Balancing

## 🧠 Concept Explanation (Story Format)

Think of a popular restaurant with 5 cashiers. A **manager** stands at the door and directs each customer to the cashier with the shortest queue. That manager is your **Load Balancer**.

Without the manager: Everyone rushes to Cashier #1. Cashier #1 is overwhelmed. Cashiers 2-5 are idle. Customers leave angry.

With the manager: Traffic is spread evenly. All cashiers are busy but not overwhelmed. Customers get served fast.

In our stack:
- **Customers** = HTTP requests from React app
- **Manager** = AWS Application Load Balancer (ALB)
- **Cashiers** = Node.js server instances on EC2

---

## 🏗️ Basic Design (Naive)

```
All React clients
       ↓
[Single Node.js Server on EC2]
       ↓
  [MongoDB]

Problems:
- One server = single point of failure
- Server can get overwhelmed
- Can't deploy without downtime
- Can't scale
```

---

## ⚡ Optimized Design

```
React (Next.js)
       ↓
[AWS CloudFront CDN]   ← Static assets served here
       ↓
[AWS ALB - Application Load Balancer]
       ↓ ↓ ↓
  [EC2 #1] [EC2 #2] [EC2 #3]   ← Node.js instances
  (Auto Scaling Group)
       ↓
  [ElastiCache Redis]
       ↓
  [RDS PostgreSQL]
```

**Benefits:**
- If EC2 #1 crashes → ALB routes to EC2 #2 and #3
- As traffic grows → Auto Scaling adds EC2 #4, #5
- No single point of failure

---

## 🔍 Key Components

### Load Balancing Algorithms

**1. Round Robin** (Default)
```
Request 1 → Server 1
Request 2 → Server 2
Request 3 → Server 3
Request 4 → Server 1  (cycles back)
```
Best when all servers are identical. Simple, even distribution.

**2. Least Connections**
```
Server 1: 50 connections
Server 2: 10 connections  ← Next request goes here
Server 3: 30 connections
```
Best when requests have different processing times. Prevents one server from being overloaded.

**3. IP Hash (Sticky Sessions)**
```
User A's IP → Always goes to Server 1
User B's IP → Always goes to Server 2
```
Use when you NEED the same user to hit the same server (legacy apps with in-memory sessions).

**4. Weighted Round Robin**
```
Server 1 (8 vCPU): weight 8 → gets 8/11 of traffic
Server 2 (2 vCPU): weight 3 → gets 3/11 of traffic
```
Use when servers have different capacities.

### Types of Load Balancers

| Type | Layer | Example | Use Case |
|------|-------|---------|----------|
| Layer 4 (Transport) | TCP/UDP | AWS NLB | Gaming, low latency |
| Layer 7 (Application) | HTTP/HTTPS | AWS ALB | Web apps, microservices |

**AWS ALB** (what we use):
- Routes by URL path: `/api/users` → Users Service, `/api/orders` → Orders Service
- Routes by HTTP headers, cookies
- Supports WebSockets (Socket.IO)
- Has built-in health checks

### Health Checks

```javascript
// Every Node.js server MUST have this endpoint
app.get('/health', async (req, res) => {
  try {
    // Check if DB is reachable
    await pool.query('SELECT 1');
    // Check if Redis is reachable
    await redisClient.ping();
    
    res.status(200).json({ 
      status: 'healthy',
      uptime: process.uptime(),
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    res.status(503).json({ status: 'unhealthy', error: error.message });
  }
});
```

ALB pings `/health` every 30 seconds. If a server returns non-200, ALB stops sending traffic to it.

---

## ⚖️ Trade-offs

| Feature | Benefit | Cost |
|---------|---------|------|
| More servers | Higher availability | More cost, more complexity |
| Sticky sessions | No session sharing needed | Uneven load distribution |
| Layer 7 LB | Smart routing | Slight overhead vs Layer 4 |
| Health checks | Auto-removes sick servers | Small performance overhead |

---

## 📊 Scalability Discussion

### AWS ALB Setup (Conceptual)

```
Target Group: "node-api-servers"
├── EC2 Instance 1 (Node.js) ← Port 3000
├── EC2 Instance 2 (Node.js) ← Port 3000
└── EC2 Instance 3 (Node.js) ← Port 3000

Health Check:
├── Path: /health
├── Interval: 30 seconds
├── Healthy threshold: 2 checks
└── Unhealthy threshold: 3 checks

Auto Scaling:
├── Min: 2 instances
├── Max: 10 instances
├── Scale up: CPU > 70% for 2 min
└── Scale down: CPU < 30% for 10 min
```

### Load Balancer for WebSockets (Socket.IO)

Socket.IO needs sticky sessions because WebSocket connections are persistent:

```javascript
// With AWS ALB, enable sticky sessions (session affinity)
// In your Socket.IO Node.js code, use Redis adapter for horizontal scaling:

const { createAdapter } = require('@socket.io/redis-adapter');
const { createClient } = require('redis');

const pubClient = createClient({ url: process.env.REDIS_URL });
const subClient = pubClient.duplicate();

io.adapter(createAdapter(pubClient, subClient));

// Now ANY server instance can broadcast to ANY connected client!
io.emit('newMessage', { text: 'Hello everyone!' });
```

---

## 💼 Interview Questions (WITH SOLUTIONS)

### Q1: What is a load balancer and why do we need it?

**Solution:**
A load balancer is a reverse proxy that distributes incoming network traffic across multiple backend servers. We need it because:
1. **High Availability:** If one server crashes, traffic routes to healthy servers
2. **Scalability:** Add/remove servers without changing client configuration
3. **Performance:** Spread load so no single server is overwhelmed
4. **Zero-downtime deployment:** Take servers offline one-by-one, update, bring back

---

### Q2: What is the difference between Layer 4 and Layer 7 load balancing?

**Solution:**
- **Layer 4 (Transport):** Operates on TCP/UDP. Routes based on IP and port. Very fast, but dumb — can't inspect HTTP content. AWS NLB. Use for gaming, IoT, ultra-low latency.
- **Layer 7 (Application):** Operates on HTTP. Can read headers, cookies, URLs. Can route `/api/users` to User Service and `/api/orders` to Order Service. AWS ALB. Use for web apps and microservices.

For our Node.js + React stack → **always use ALB (Layer 7)**.

---

### Q3: How do you handle WebSocket connections with a load balancer?

**Solution:**
WebSockets are stateful — once connected, the client is tied to a specific server. Two options:
1. **Sticky Sessions (IP Affinity):** ALB routes a user to the same server every time. Problem: if that server dies, connection is lost. Uneven load.
2. **Redis Pub/Sub Adapter (Better):** Each Socket.IO server uses Redis to share messages. Any server can send to any client. Use `@socket.io/redis-adapter`.

```javascript
// Setup Redis adapter for Socket.IO
io.adapter(createAdapter(pubClient, subClient));
// Now it doesn't matter which server handles the connection!
```

---

### Q4: What happens when a server fails health checks? Walk through the process.

**Solution:**
1. ALB sends `GET /health` every 30 seconds to each server
2. Server fails to respond (crashed) or returns 503
3. After 3 consecutive failures → ALB marks server as "unhealthy"
4. ALB stops routing new requests to that server
5. Auto Scaling sees unhealthy instance → terminates it → launches a new one
6. New instance passes health checks → ALB starts routing to it
7. Total downtime for users: ~0 seconds (ALB handled it transparently)

---

### Q5: How would you implement rate limiting at the load balancer level?

**Solution:**
- AWS ALB doesn't do rate limiting natively — use **AWS WAF** (Web Application Firewall) with ALB.
- Or implement at the API Gateway level (AWS API Gateway has built-in rate limiting).
- Or implement in Node.js middleware:

```javascript
const rateLimit = require('express-rate-limit');
const RedisStore = require('rate-limit-redis');

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // max 100 requests per window
  store: new RedisStore({
    client: redisClient,
    // Use Redis so all server instances share the same counter!
    // Without Redis, each server tracks independently → users get 100 * numServers requests
  }),
  message: 'Too many requests, please try again later.'
});

app.use('/api/', limiter);
```

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem 1: Design a load balancing strategy for a food delivery app with peak hours

**Solution:**
```
Off-peak (2 AM): Min 2 EC2 instances
Lunch rush (12-1 PM): Scale to 8 instances
Dinner rush (7-9 PM): Scale to 12 instances
Auto Scaling policy based on:
  - CPU > 60% → add 2 instances
  - Request latency P95 > 500ms → add 2 instances
  - CPU < 25% for 10 min → remove 1 instance

Scheduled scaling:
  - 11:30 AM: Pre-scale to 6 instances (predictive)
  - 6:30 PM: Pre-scale to 10 instances

Algorithm: Least Connections (order processing takes variable time)
Health Check: /health checks DB + payment service connectivity
```

---

### Problem 2: Your load balancer is itself a single point of failure. How do you fix it?

**Solution:**
- AWS ALB is internally redundant — AWS runs it across multiple Availability Zones
- For custom load balancers (nginx), use Active-Passive failover:
  - Two nginx instances, one active, one standby
  - Use **Keepalived** to monitor and promote standby if active fails
  - Or use DNS failover (Route 53 health checks)
- Even better: Use DNS load balancing with Route 53 + multiple ALBs in different regions (Global Load Balancing)

---

### Navigation
**Prev:** [03_Latency_vs_Throughput.md](03_Latency_vs_Throughput.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [05_Caching.md](05_Caching.md)
