# 📌 02 — API Gateway Pattern: The Single Entry Point

## 🧠 Concept Explanation

### Basic → Intermediate
An API Gateway is a server that acts as an entry point for all clients. It routes requests to the appropriate microservice, handles authentication, and can perform load balancing.

### Advanced → Expert
At a staff level, the API Gateway is the **Edge Controller**. 
1. **Request Routing**: Translating external public URLs to internal private service endpoints.
2. **Cross-Cutting Concerns**: Offloading Auth, Rate Limiting, CORS, and SSL termination from the microservices.
3. **Payload Transformation**: Converting between external formats (JSON) and internal formats (gRPC/Protobuf).
4. **Aggregation**: Combining data from multiple services into a single response to reduce client-side round trips.

---

## 🏗️ Common Mental Model
"The Gateway is just a proxy."
**Correction**: It is a **Smart Proxy**. It often maintains state (for rate limiting) and performs logical decisions (dynamic routing based on headers or user identity).

---

## ⚡ Actual Behavior: Single Point of Failure (SPOF)
If your API Gateway goes down, your **entire system** is unreachable. This is why gateways must be highly available (running in multiple AZs) and stateless.

---

## 🔬 Internal Mechanics (Networking + Performance)

### Backpressure at the Edge
The Gateway is the first line of defense against traffic spikes. It must implement **Backpressure**—telling clients to slow down (HTTP 429) rather than overwhelming internal services and causing a cascading failure.

### The Cost of the "Extra Hop"
Every request going through the gateway adds at least **1 extra network hop** and **2 extra serialization/deserialization cycles**. This adds 10-50ms of latency that wouldn't exist in a direct-to-service model.

---

## 📐 ASCII Diagrams

### API Gateway Layout
```text
  CLIENTS (Web, Mobile)
     │
     ▼ (Public Internet)
  ┌────────────────────────┐
  │      API GATEWAY       │ ◀─── Auth, Rate Limit, Logging
  └──────────┬─────────────┘
             │
     ┌───────┼───────┐ (Private Network)
     ▼       ▼       ▼
  [ Svc A ] [ Svc B ] [ Svc C ]
```

---

## 🔍 Code Example: Simple Proxy with Rate Limiting
```javascript
const express = require('express');
const proxy = require('express-http-proxy');
const rateLimit = require('express-rate-limit');

const app = express();

// 1. Rate Limiter (Edge Defense)
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100 // 100 requests per window per IP
});

app.use(limiter);

// 2. Auth Offloading
app.use((req, res, next) => {
  const token = req.headers['authorization'];
  if (validateToken(token)) return next();
  res.status(401).send('Unauthorized');
});

// 3. Dynamic Routing
app.use('/users', proxy('http://user-service:3001'));
app.use('/posts', proxy('http://post-service:3002'));

app.listen(80);
```

---

## 💥 Production Failures & Debugging

### Scenario: The Gateway Timeout
**Problem**: The gateway returns 504 Gateway Timeout, but the internal service logs show that the request was processed successfully.
**Reason**: The gateway's `timeout` setting is shorter than the internal service's processing time. The gateway gave up, but the service kept working.
**Fix**: Synchronize timeouts across the stack (Gateway timeout > Service timeout).

### Scenario: The "Header Bloat"
**Problem**: Requests start failing with 431 Request Header Fields Too Large.
**Reason**: Each service in the chain adds its own headers (Request-ID, Auth-Metadata, Tracing-ID). By the time it hits the 5th service, the headers exceed the buffer limit.
**Fix**: Prune unnecessary headers at the Gateway or increase the `maxHeaderSize` in internal Node.js processes.

---

## 🧪 Real-time Production Q&A

**Q: "Should we build our own gateway in Node.js or use Kong/AWS Gateway?"**
**A**: **Use an established tool (Kong, Envoy, AWS/GCP Gateway)** for standard routing and security. Build a **Custom Node.js Gateway (BFF)** only when you need complex data aggregation or business-specific logic that standard proxies can't handle.

---

## 🏢 Industry Best Practices
- **Service Discovery**: Integrate the gateway with a service registry (Consul/K8s DNS) so it doesn't need hardcoded IPs.
- **Circuit Breaking**: The gateway should stop calling a service that is repeatedly failing to prevent overwhelming it.

---

## 💼 Interview Questions
**Q: What is a "BFF" (Backend for Frontend)?**
**A**: A BFF is a specific type of API Gateway tailored to one specific client type (e.g. one for Mobile, one for Web). This allows the Mobile BFF to send smaller, optimized payloads, while the Web BFF can send more detailed data.

---

## 🧩 Practice Problems
1. Implement a simple round-robin load balancer in Node.js that routes requests to three different backend ports.
2. Build a "Request Aggregator" route that calls two different APIs in parallel and merges their JSON responses.

---

**Prev:** [01_Monolith_vs_Microservices.md](./01_Monolith_vs_Microservices.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [03_Event_Driven_Architecture.md](./03_Event_Driven_Architecture.md)
