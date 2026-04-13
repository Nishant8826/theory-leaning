# Load Balancing

> 📌 **File:** 11_Load_Balancing.md | **Level:** Full-Stack Dev → Networking Expert

---

## What is it?

A load balancer distributes incoming traffic across multiple servers so no single server gets overwhelmed. It's how you scale from 1 Node.js instance to 10, handle thousands of concurrent users, and achieve zero-downtime deployments. In AWS, you'll primarily use ALB (Application Load Balancer).

---

## Map it to MY STACK (CRITICAL)

```
Without load balancer:
  Users ─────────────► Single EC2 (Node.js)
                        │
                        └── 1000 req/sec → CPU at 100% → crashes

With load balancer:
  Users ──► ALB ─┬──► EC2 #1 (Node.js) ← 333 req/sec each
                 ├──► EC2 #2 (Node.js)
                 └──► EC2 #3 (Node.js)
                      All share MongoDB / Redis via connection pools
```

### AWS Load Balancer Types

```
┌────────────────────────────────────────────────────────────────────┐
│  Type        │ Layer │ Protocol    │ Use Case                     │
├──────────────┼───────┼─────────────┼──────────────────────────────┤
│  ALB         │ 7     │ HTTP/HTTPS  │ REST APIs, WebSocket,        │
│              │       │ WebSocket   │ Next.js, path-based routing  │
│              │       │             │ ← YOUR PRIMARY CHOICE        │
├──────────────┼───────┼─────────────┼──────────────────────────────┤
│  NLB         │ 4     │ TCP/UDP     │ MongoDB proxy, Redis proxy,  │
│              │       │ TLS         │ gaming, gRPC, extreme perf   │
├──────────────┼───────┼─────────────┼──────────────────────────────┤
│  CLB         │ 4/7   │ HTTP/TCP    │ ❌ Legacy — don't use       │
├──────────────┼───────┼─────────────┼──────────────────────────────┤
│  GWLB        │ 3     │ IP          │ Firewall appliances (rare)   │
└──────────────┴───────┴─────────────┴──────────────────────────────┘
```

---

## How does it actually work?

### ALB Request Flow

```
User: GET https://api.myapp.com/api/products

1. DNS: api.myapp.com → ALB DNS → ALB IP (multiple IPs, one per AZ)
2. TCP: Browser → ALB (TLS terminated here)
3. ALB checks listener rules:
   Rule 1: Host=api.myapp.com, Path=/api/* → Target Group "api-servers"
   Rule 2: Host=admin.myapp.com, Path=/*  → Target Group "admin-servers"
   Default: → Target Group "default-servers"
4. ALB picks a healthy target from the group:
   - Round-robin (default)
   - Least outstanding requests
5. ALB forwards: HTTP request → EC2 #2 (10.0.1.11:3000)
6. Node.js processes, responds to ALB
7. ALB sends response back to user

Headers ALB adds:
  X-Forwarded-For: 203.0.113.50 (client's real IP)
  X-Forwarded-Proto: https (original protocol)
  X-Forwarded-Port: 443
```

### Health Checks

```
ALB checks each target every 30 seconds:

  ALB → GET /health HTTP/1.1 → EC2 #1
  
  EC2 #1 responds: 200 OK → ✅ Healthy (keep sending traffic)
  EC2 #2 responds: 500 Error → ❌ Unhealthy (stop sending traffic)
  EC2 #3 no response → ❌ Unhealthy (timeout, crashed)

Health check config:
  Path: /health (your Express health endpoint)
  Interval: 30s (how often to check)
  Timeout: 5s (how long to wait for response)
  Healthy threshold: 2 (consecutive successes to mark healthy)
  Unhealthy threshold: 3 (consecutive failures to mark unhealthy)
  Matcher: 200 (expected HTTP status code)
```

### Load Balancing Algorithms

```
┌──────────────────────────────────────────────────────────────────┐
│  Algorithm                   │ How it Works                     │
├──────────────────────────────┼──────────────────────────────────┤
│  Round Robin (ALB default)   │ 1→2→3→1→2→3 (equal rotation)   │
│  Least Outstanding Requests  │ Send to the server with fewest  │
│  (ALB option)                │ in-progress requests             │
│  IP Hash                     │ Same client IP → same server    │
│  Weighted                    │ Server 1: 70%, Server 2: 30%    │
│  Random                      │ Random server each time         │
├──────────────────────────────┴──────────────────────────────────┤
│  For your Node.js app:                                          │
│  - Stateless APIs: Round Robin (simplest, works great)         │
│  - Slow DB queries: Least Outstanding (prevents pileup)        │
│  - WebSocket: ALB sticky sessions (same client → same server) │
│  - Blue/green deploy: Weighted (shift traffic gradually)       │
└──────────────────────────────────────────────────────────────────┘
```

---

## Visual Diagram — ALB Architecture

```
                    Internet
                       │
                 ┌─────┴─────┐
                 │    ALB     │  HTTPS listener (:443)
                 │            │  TLS terminated here
                 │  Rules:    │  
                 │  /api/* → TG1│
                 │  /ws/*  → TG2│  (sticky sessions)
                 │  /*     → TG3│
                 └──┬──┬──┬──┘
                    │  │  │
         ┌──────────┘  │  └──────────┐
         │             │             │
    ┌────▼────┐   ┌────▼────┐   ┌────▼────┐
    │ EC2 #1  │   │ EC2 #2  │   │ EC2 #3  │
    │ Node.js │   │ Node.js │   │ Node.js │
    │ :3000   │   │ :3000   │   │ :3000   │
    └────┬────┘   └────┬────┘   └────┬────┘
         │             │             │
         └──────┬──────┴──────┬──────┘
                │             │
         ┌──────▼──┐   ┌─────▼──┐
         │MongoDB  │   │ Redis  │
         │(Atlas)  │   │(Elasti)│
         └─────────┘   └────────┘
```

---

## Node.js Implementation

```javascript
// ──── Health Check Endpoint (REQUIRED for ALB) ────
app.get('/health', async (req, res) => {
  try {
    // Check database connectivity
    await mongoose.connection.db.admin().ping();
    
    // Check Redis connectivity
    await redis.ping();
    
    res.status(200).json({
      status: 'healthy',
      uptime: process.uptime(),
      timestamp: new Date().toISOString(),
      memory: process.memoryUsage(),
      connections: {
        mongodb: mongoose.connection.readyState === 1 ? 'connected' : 'disconnected',
        redis: redis.status === 'ready' ? 'connected' : 'disconnected'
      }
    });
  } catch (err) {
    res.status(503).json({
      status: 'unhealthy',
      error: err.message
    });
  }
});

// ──── Get Real Client IP Behind ALB ────
app.set('trust proxy', true);  // Trust X-Forwarded-For from ALB

app.use((req, res, next) => {
  // req.ip now returns the REAL client IP, not ALB's IP
  console.log(`Client IP: ${req.ip}`);
  console.log(`Full chain: ${req.headers['x-forwarded-for']}`);
  console.log(`Protocol: ${req.headers['x-forwarded-proto']}`);
  next();
});

// ──── Graceful Shutdown (for zero-downtime deploys) ────
let isShuttingDown = false;

process.on('SIGTERM', () => {
  console.log('SIGTERM received — starting graceful shutdown');
  isShuttingDown = true;
  
  // Stop accepting new connections
  server.close(async () => {
    console.log('HTTP server closed');
    
    // Close database connections
    await mongoose.connection.close();
    await redis.quit();
    
    console.log('All connections closed — exiting');
    process.exit(0);
  });
  
  // Force exit after 30s (ALB will stop sending traffic)
  setTimeout(() => {
    console.error('Forced shutdown after 30s');
    process.exit(1);
  }, 30000);
});

// Health check returns 503 during shutdown
app.get('/health', (req, res, next) => {
  if (isShuttingDown) {
    return res.status(503).json({ status: 'shutting_down' });
  }
  next();
});

// ──── WebSocket with ALB Sticky Sessions ────
const io = require('socket.io')(server, {
  cors: { origin: '*' },
  // ALB sticky sessions ensure same client hits same server
  // But if server restarts, client reconnects to different server
  // Solution: Use Redis adapter for Socket.IO
  adapter: require('@socket.io/redis-adapter').createAdapter(pubClient, subClient)
});
// Now WebSocket events are shared across all Node.js instances!
```

---

## Sticky Sessions (Session Affinity)

```
Problem: Stateful WebSocket connections

Without sticky sessions:
  Connect → Server 1 ✅
  Reconnect → Server 2 (different!) → state lost ❌

With ALB sticky sessions:
  Connect → Server 1 ✅ (ALB sets AWSALB cookie)
  Reconnect → Server 1 ✅ (ALB reads cookie, routes to same target)

When to use sticky sessions:
  ✅ WebSocket / Socket.IO (with Redis adapter as backup)
  ✅ Server-side sessions without Redis (not recommended)
  ❌ Stateless REST APIs (don't need it)
  ❌ JWT authentication (don't need it — token carries state)
  
Problem with sticky sessions:
  - Uneven load (popular users stick to one server)
  - Server restart = lost sessions
  - Scale-in = lost sessions
  → Better: Store state in Redis (truly stateless servers)
```

---

## Zero-Downtime Deployment

```
Rolling deployment with ALB:

Step 1: Deploy new code to EC2 #3
  ALB health check → EC2 #3 fails → traffic stops going to #3

Step 2: EC2 #3 starts with new code
  ALB health check → EC2 #3 passes → traffic resumes

Step 3: Repeat for EC2 #2, then EC2 #1

  Time 0: [v1] [v1] [v1]  ← all old version
  Time 1: [v1] [v1] [v2]  ← #3 updated, passes health check
  Time 2: [v1] [v2] [v2]  ← #2 updated
  Time 3: [v2] [v2] [v2]  ← all new version ✅ zero downtime

Key requirements:
  1. Health check endpoint (/health)
  2. Graceful shutdown (SIGTERM handler)
  3. Backward-compatible API changes (v1 and v2 run simultaneously)
  4. Connection draining (ALB waits for in-flight requests)
```

---

## Performance Insight

```
┌──────────────────────────────────────────────────────────────────┐
│  Load Balancer Performance Impact                                │
├──────────────────┬───────────────────────────────────────────────┤
│  ALB latency     │ +1-5ms per request (HTTP parsing)             │
│  NLB latency     │ +<0.1ms per request (TCP passthrough)        │
│  ALB connections │ Thousands concurrent                          │
│  NLB connections │ Millions concurrent                           │
│  ALB cost        │ ~$16/mo + $0.008/LCU-hour                   │
│  NLB cost        │ ~$16/mo + $0.006/NLCU-hour                  │
├──────────────────┴───────────────────────────────────────────────┤
│                                                                  │
│  ALB Idle Timeout (default: 60s):                               │
│  If no data flows for 60s, ALB CLOSES the connection.           │
│  Must be: ALB timeout > Node.js keep-alive timeout              │
│  Set: Node.js keepAliveTimeout = 65000 (65s > ALB's 60s)       │
│                                                                  │
│  Connection Draining (default: 300s):                            │
│  When removing a target, ALB waits 300s for in-flight requests. │
│  Reduce to 30s for faster deployments.                          │
└──────────────────────────────────────────────────────────────────┘
```

---

## Common Mistakes

### ❌ No Health Check Endpoint

```javascript
// ALB can't determine if your server is healthy
// → sends traffic to crashed servers → 502 errors

// ✅ Always have a health check
app.get('/health', (req, res) => res.status(200).json({ status: 'ok' }));
```

### ❌ Keep-Alive Timeout Mismatch

```javascript
// ALB idle timeout: 60s (default)
// Node.js keepAliveTimeout: 5s (old Node.js default)
// → ALB keeps connection, Node.js closes it → 502!

server.keepAliveTimeout = 65000;  // 65s > ALB's 60s
server.headersTimeout = 66000;    // Slightly more
```

### ❌ Not Trusting Proxy Headers

```javascript
// ❌ req.ip returns ALB's internal IP (10.0.x.x)
console.log(req.ip); // 10.0.1.50 (wrong!)

// ✅ Trust ALB's X-Forwarded-For header
app.set('trust proxy', true);
console.log(req.ip); // 203.0.113.50 (correct client IP!)
```

---

## Practice Exercises

### Exercise 1: Health Check
Create a health check endpoint that verifies MongoDB and Redis connections. Return 200 if both are healthy, 503 if either is down.

### Exercise 2: Graceful Shutdown
Implement SIGTERM handling that: stops accepting new connections, waits for in-flight requests to complete (30s max), closes DB connections, then exits.

### Exercise 3: Load Test
Use `wrk` or `autocannon` to load test your API with 100 concurrent connections. Monitor which EC2 instances receive traffic.

---

## Interview Q&A

**Q1: What is the difference between ALB and NLB?**
> ALB (Layer 7) understands HTTP — can route by URL path, hostname, headers. Adds 1-5ms latency. Supports WebSocket upgrade. NLB (Layer 4) sees only TCP/UDP — routes by port, ultra-low latency (<0.1ms), handles millions of connections. Use ALB for web apps, NLB for databases/gaming.

**Q2: How do you achieve zero-downtime deployments with a load balancer?**
> Rolling deploys: update one instance at a time while others handle traffic. ALB health checks detect when an instance is down (during deploy) and stop routing to it. Connection draining waits for in-flight requests. Graceful shutdown (SIGTERM handler) in Node.js completes pending work.

**Q3: What are sticky sessions and when should you use them?**
> Sticky sessions route the same client to the same server (via cookie). Needed for WebSocket connections without shared state. Problem: uneven load distribution, lost sessions on server restart. Better approach: store session state in Redis and keep servers stateless.

**Q4: How does ALB health checking work?**
> ALB sends HTTP requests to a health check path on each target at a configured interval. If a target fails N consecutive checks (unhealthy threshold), ALB stops routing traffic to it. When it passes M consecutive checks (healthy threshold), traffic resumes. Critical for reliability.

**Q5: How do you handle the ALB idle timeout problem?**
> ALB closes TCP connections after 60 seconds of inactivity. If Node.js closes first (default keepAliveTimeout was 5s), ALB sends requests to a closed connection → 502 error. Fix: set Node.js `keepAliveTimeout` > ALB idle timeout (e.g., 65s > 60s).
