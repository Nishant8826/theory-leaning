# 📌 Case Study 03 — Handling a 100x Traffic Spike

## 🛠️ The Scenario
A news website is mentioned on a popular social media platform. Traffic spikes from 100 users to 10,000 users in 2 minutes.

**Impact**:
- The servers hit 100% CPU.
- Response times go from 50ms to 30 seconds.
- Most users see "504 Gateway Timeout".
- The database connection pool is exhausted.

---

## 🔍 Step 1: Immediate Triage (The "Emergency Brake")
The system is in a **Cascading Failure**. Even if we add more servers now, they will take 5 minutes to boot, and the existing servers are already dead.

**Action**: Implement **Load Shedding** at the API Gateway.
We configure the load balancer to immediately reject 50% of traffic with a `503 Service Unavailable` error. This "sheds" the load and allows the remaining 50% of users to actually have a working site, rather than everyone having a broken site.

---

## 🧪 Step 2: Scale Out (Horizontal Scaling)
We trigger the Auto-Scaling Group to add 10 new instances. 

**The Problem**: The new instances are stuck in "Pending" because they are downloading a large 2GB Docker image and running a slow `npm install` (Technical Debt).

---

## 🔬 Step 3: Identify the Root Bottleneck
While waiting for servers, we look at the logs. The CPU is high, but the database is also slow. 
The bottleneck is the **Session Store**. We are using a single small Redis instance for sessions, and it has hit its network throughput limit.

---

## 💡 Step 4: Short-term Fix (Bypass the Bottleneck)
We disable session-tracking for "Guest" users. Since 90% of the traffic is anonymous readers, we only check for sessions if a user is trying to comment or login.

```javascript
// ✅ EMERGENCY BYPASS
app.use((req, res, next) => {
  if (req.path === '/article') {
    // Skip session lookup for read-only pages
    return next();
  }
  sessionMiddleware(req, res, next);
});
```

---

## ⚡ Step 5: Long-term Architecture Fixes
After the spike subsides, we perform a post-mortem and implement:

1. **Pre-baked Images**: We move away from `npm install` during boot. We now use pre-built Docker images that start in < 20 seconds.
2. **Read-through Caching**: We add a CDN (Cloudflare) to cache the article pages. The traffic won't even hit our servers next time.
3. **Database Read Replicas**: We split the traffic so that article reads go to 3 Read Replicas, while only writes go to the Primary.

---

## 📈 Results of the Fixes
We simulate another 100x spike using `k6`.
- **Latency**: Stays under 200ms.
- **Cache Hit Ratio**: 95% at the CDN.
- **Server Load**: Only 20% increase in CPU.

---

## 🏢 Lessons Learned
1. **The Gateway is your Shield**: Use it to shed load before your servers crash.
2. **Speed is everything in Scaling**: If your server takes 5 minutes to start, your auto-scaling is useless during a spike.
3. **Cache as far away from the server as possible**: The CDN is the best defense against traffic spikes.

---

**Next:** [04_Microservices_Failure_Chain.md](./04_Microservices_Failure_Chain.md)
