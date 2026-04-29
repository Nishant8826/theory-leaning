# 📌 02 — Load Balancing Strategies: Layer 4 vs Layer 7

## 🧠 Concept Explanation

### Basic → Intermediate
A Load Balancer (LB) is a device or software that distributes network traffic across a cluster of servers. It prevents any single server from becoming overwhelmed.

### Advanced → Expert
At a staff level, we must distinguish between **Layer 4** and **Layer 7** balancing.
1. **L4 (Transport Layer)**: Balances based on IP address and TCP/UDP port. It doesn't look at the HTTP content. It is extremely fast and low-latency.
2. **L7 (Application Layer)**: Balances based on HTTP headers, cookies, URLs, and query parameters. It is "smarter" but requires more CPU because it must decrypt TLS and parse the HTTP request.

Choosing between them is a trade-off between **Intelligence** and **Performance**.

---

## 🏗️ Common Mental Model
"The load balancer just picks a random server."
**Correction**: LBs use specific algorithms:
- **Round Robin**: Sequential distribution. Good if all servers are equal.
- **Least Connections**: Sends to the server with the fewest active requests. Best for requests with varying processing times.
- **IP Hash**: Ensures a user always hits the same server (Persistence).

---

## ⚡ Actual Behavior: Health Checks
A load balancer is only useful if it knows which servers are "healthy." It periodically sends a request to a `/health` endpoint on your Node.js app. If the app doesn't respond or returns a 5xx, the LB removes it from the pool.

---

## 🔬 Internal Mechanics (Networking)

### SSL Termination
The LB usually handles the expensive TLS/SSL handshake (**SSL Offloading**). It then communicates with the internal Node.js servers over plain HTTP. This saves Node.js CPU cycles.

### X-Forwarded-For
Since the LB "proxies" the request, the Node.js server sees the LB's IP as the source. To get the real user's IP, you must check the `X-Forwarded-For` header, which the LB adds.

---

## 📐 ASCII Diagrams

### L4 vs L7 Balancing
```text
  L4 BALANCING (Fast)        L7 BALANCING (Smart)
  [ IP:Port Only ]           [ Cookie / URL / Headers ]
         │                          │
         ▼                          ▼
  ┌────────────┐             ┌─────────────────────┐
  │   ROUTER   │             │   NGINX / ENVOY     │
  └────────────┘             └─────────────────────┘
         │                          │
    ┌────┴────┐                ┌────┴────┐
    ▼         ▼                ▼         ▼
 [Svc 1]   [Svc 2]          [/users]  [/posts]
```

---

## 🔍 Code Example: Health Check Endpoint
```javascript
const express = require('express');
const app = express();

app.get('/health', (req, res) => {
  // Check DB connection, disk space, etc.
  const isHealthy = checkSystemHealth();
  
  if (isHealthy) {
    res.status(200).send('OK');
  } else {
    // LB will see this and stop sending traffic
    res.status(503).send('Service Unavailable');
  }
});

app.listen(3000);
```

---

## 💥 Production Failures & Debugging

### Scenario: The "Zombie" Instance
**Problem**: Users are seeing 502 Bad Gateway errors, even though your auto-scaling says all servers are up.
**Reason**: One Node.js instance is in a "Deadlock" (Event Loop blocked). It's still "running" as a process, but it's not responding to the LB's health checks.
**Fix**: Ensure your health check includes a check of the **Event Loop Lag**. If lag is too high, fail the health check.

### Scenario: Header Size Limit at the LB
**Problem**: Large requests are failing at the LB, but never even reach the Node.js logs.
**Reason**: The LB (like Nginx or AWS ALB) has a default limit for HTTP header sizes (e.g. 8KB). If your JWT + Cookies exceed this, the LB rejects the request.
**Fix**: Increase the `large_client_header_buffers` (Nginx) or equivalent in your LB.

---

## 🧪 Real-time Production Q&A

**Q: "Should we use Nginx or a Cloud Load Balancer (ALB)?"**
**A**: **Use a Cloud LB (ALB/NLB)** for your public entry point. It handles scaling and DDoS protection better. Use **Nginx/Envoy** internally (Sidecar or Gateway) for fine-grained routing, retries, and service mesh features.

---

## 🏢 Industry Best Practices
- **Least Connections**: Use this as your default algorithm for Node.js, as request times can vary wildly.
- **Passive Health Checks**: Monitor real user traffic. If a server returns 5 consecutive 5xx errors to real users, remove it from the pool immediately.

---

## 💼 Interview Questions
**Q: What is "SSL Offloading" and why is it beneficial?**
**A**: It's the process of decrypting SSL/TLS traffic at the load balancer. It's beneficial because it centralizes certificate management and frees up CPU resources on the application servers, which can then focus purely on business logic.

---

## 🧩 Practice Problems
1. Configure an Nginx load balancer to distribute traffic between two Node.js apps using the `ip_hash` strategy.
2. Implement a `/health` check that fails if the available memory on the machine is less than 10%.

---

**Prev:** [01_Vertical_vs_Horizontal.md](./01_Vertical_vs_Horizontal.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [03_Caching_at_the_Edge_CDN.md](./03_Caching_at_the_Edge_CDN.md)
