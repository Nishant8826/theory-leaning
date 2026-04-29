# 📌 09 — Connection Pooling: HTTP Agents and Socket Reuse

## 🧠 Concept Explanation

### Basic → Intermediate
Connection Pooling is a technique used to keep multiple network connections open so they can be reused for future requests. This avoids the overhead of establishing a new TCP/TLS connection for every single HTTP request.

### Advanced → Expert
In Node.js, connection pooling is managed by the **`http.Agent`** class. 
1. When you make a request, the Agent checks its internal "Free Sockets" pool.
2. If a socket is available for the given host/port, it is reused.
3. If not, and the pool isn't full, it creates a new socket.
4. If the pool is full, the request is queued.

At a staff level, tuning the `maxSockets` and `keepAlive` properties is critical for high-throughput microservices.

---

## 🏗️ Common Mental Model
"Node.js handles all connections automatically."
**Correction**: The **Global Agent** has `keepAlive: false` by default in older Node.js versions. This means every request to the same server still performs a full TCP/TLS handshake. Modern Node.js (v18+) has better defaults, but custom agents are still required for advanced tuning.

---

## ⚡ Actual Behavior: Socket Persistence
When `keepAlive` is enabled, the socket stays in the `ESTABLISHED` state even after the request is finished. It remains in the Agent's pool until it is reused or the `keepAliveMsecs` (idle timeout) is reached.

---

## 🔬 Internal Mechanics (libuv + http.Agent)

### The Socket Queue
The Agent maintains several internal objects:
- `sockets`: Active sockets currently in use.
- `freeSockets`: Idle sockets waiting to be reused.
- `requests`: Queued requests waiting for a free socket.

### Socket Timeout
If a socket in the `freeSockets` pool is not reused within the `keepAliveMsecs` window, the Agent calls `socket.destroy()` to release the OS resources.

---

## 📐 ASCII Diagrams

### Agent Pool Management
```text
  INCOMING REQUESTS ──▶ [ HTTP AGENT ]
                          │
       ┌──────────────────┴──────────────────┐
       ▼                                     ▼
 [ FREE SOCKETS ]                     [ ACTIVE SOCKETS ]
 (Reuse if match)                     (Currently sending data)
       │                                     ▲
       └─────────── (Request Done) ──────────┘
```

---

## 🔍 Code Example: Custom Agent for High Throughput
```javascript
const http = require('http');

// Custom Agent for a high-traffic microservice
const agent = new http.Agent({
  keepAlive: true,
  keepAliveMsecs: 1000,
  maxSockets: 100,      // Max concurrent connections per host
  maxFreeSockets: 10,   // Max idle connections to keep open
  timeout: 60000        // Socket timeout
});

const options = {
  hostname: 'my-microservice.com',
  port: 80,
  path: '/api',
  method: 'GET',
  agent: agent // Use the custom agent
};

const req = http.request(options, (res) => {
  res.on('data', () => {}); // Drain stream
});

req.end();
```

---

## 💥 Production Failures & Debugging

### Scenario: The "Request Queue" Latency
**Problem**: Your app is using low CPU and memory, but request latency is very high (seconds).
**Reason**: You hit the `maxSockets` limit (default was 5 in older Node.js). New requests are sitting in the Agent's internal `requests` queue, waiting for a socket to become free.
**Debug**: Inspect `agent.requests` object in the debugger.
**Fix**: Increase `maxSockets`.

### Scenario: Socket Hangup during Deployments
**Problem**: When you deploy a new version of a service, the calling service sees many `ECONNRESET` or "Socket hang up" errors.
**Reason**: The calling service has many `freeSockets` open. When the target service restarts, it kills those connections. The calling service tries to use a dead socket before it realizes it's gone.
**Fix**: Implement **Retries** for idempotent requests and ensure your target service handles graceful shutdown.

---

## 🧪 Real-time Production Q&A

**Q: "Should I use one global agent for everything?"**
**A**: **No.** If you have one host that is slow, it might exhaust the pool and prevent requests to other, faster hosts. Create separate agents for different external services to isolate their performance characteristics.

---

## 🧪 Debugging Toolchain
- **`netstat`**: Check the number of `ESTABLISHED` connections to your target host.
- **`process.stdout.write(JSON.stringify(agent.getCurrentStatus()))`**: Custom debugging to see pool usage.

---

## 🏢 Industry Best Practices
- **Enable `keepAlive`**: This is the single most important performance optimization for Node.js networking.
- **Set realistic timeouts**: Don't let a socket sit idle for too long, as it consumes kernel memory and can be closed by intermediate firewalls/LB.

---

## 💼 Interview Questions
**Q: What is the difference between `maxSockets` and `maxFreeSockets`?**
**A**: `maxSockets` is the total number of connections allowed per host (active + idle). `maxFreeSockets` is the maximum number of *idle* connections the agent will keep open in the background for future reuse.

---

## 🧩 Practice Problems
1. Create a script that hits a local server 100 times. Compare the time taken with `keepAlive: true` vs `keepAlive: false`. Use `tcpdump` to count the number of handshakes.
2. Build a "Circuit Breaker" that monitors the `agent.requests` queue and fails fast if the queue becomes too large.

---

**Prev:** [08_DNS_and_Connection_Lifecycle.md](./08_DNS_and_Connection_Lifecycle.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [../Architecture/01_Monolith_vs_Microservices.md](../Architecture/01_Monolith_vs_Microservices.md)
