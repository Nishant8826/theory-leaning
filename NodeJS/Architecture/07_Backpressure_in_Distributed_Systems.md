# 📌 07 — Backpressure in Distributed Systems: Flow Control at Scale

## 🧠 Concept Explanation

### Basic → Intermediate
Backpressure is a signal sent from a consumer to a producer telling it to slow down because the consumer cannot keep up with the data rate.

### Advanced → Expert
In a distributed system, backpressure is the difference between a **controlled slowdown** and a **catastrophic crash**.
1. **Local Backpressure**: (Node.js Streams) A writable stream telling a readable stream to stop reading from the source.
2. **Distributed Backpressure**: A microservice returning `HTTP 429` or `503` to tell the API Gateway to stop sending requests.

Without backpressure, queues grow indefinitely, memory is exhausted, and latency spikes across the entire system.

---

## 🏗️ Common Mental Model
"I'll just add a bigger queue."
**Correction**: A bigger queue only **delays** the failure. If the producer is faster than the consumer indefinitely, the queue *will* eventually fill up. Backpressure is about **propagating the limit** back to the original source (the user or the ingress).

---

## ⚡ Actual Behavior: Load Shedding
When a system is overwhelmed and cannot apply backpressure effectively, it must perform **Load Shedding**. This means deliberately dropping new requests (giving them a fast 503 error) to preserve the health of the system for existing requests.

---

## 🔬 Internal Mechanics (Networking + Queues)

### TCP Receive Window
At the network level, TCP uses the **Receive Window** to signal backpressure. If the Node.js application is slow to call `socket.read()`, the kernel's receive buffer fills up, and the TCP window size advertised to the sender drops to zero.

### Circuit Breakers
A Circuit Breaker (like **Hystrix** or **Opossum**) detects when a downstream service is failing or slow. It "trips" the circuit and immediately returns an error for future calls, preventing the "slow-down" from propagating upwards.

---

## 📐 ASCII Diagrams

### Cascading Failure without Backpressure
```text
  [ USER ] ──▶ [ SERVICE A ] ──▶ [ SERVICE B (SLOW) ]
       │            │                 │
       │            ▼                 ▼
       │      (Queue grows)     (Internal Memory OOM)
       │            │                 │
       ▼            ▼                 ▼
  (Timeout)    (Crashes)         (Crashes)
```

---

## 🔍 Code Example: Circuit Breaker with Opossum
```javascript
const CircuitBreaker = require('opossum');

async function callDownstreamService() {
  // Simulate a network call
  return await httpClient.get('http://service-b/data');
}

const options = {
  timeout: 3000, // If name takes longer than 3s, trigger failure
  errorThresholdPercentage: 50, // Trip if 50% of requests fail
  resetTimeout: 30000 // After 30s, try again (half-open)
};

const breaker = new CircuitBreaker(callDownstreamService, options);

breaker.fallback(() => ({ error: 'Service B is currently unavailable' }));

app.get('/data', async (req, res) => {
  try {
    const result = await breaker.fire();
    res.json(result);
  } catch (err) {
    res.status(503).send('Service Unavailable');
  }
});
```

---

## 💥 Production Failures & Debugging

### Scenario: The Retry Storm
**Problem**: Service B is slightly slow. Service A has an aggressive retry policy (retry 3 times immediately).
**Impact**: The slight slowness in B causes A to quadruple the traffic to B. B now crashes completely under the load.
**Fix**: Use **Exponential Backoff** and **Jitter** for retries. Never retry immediately in a tight loop.

### Scenario: The Hidden Memory Leak (The queue is too big)
**Problem**: The server memory usage is 8GB, but the JS heap is only 500MB.
**Reason**: You are using a library that buffers data in native C++ memory without checking for backpressure. The "queue" is growing off-heap.
**Fix**: Use Node.js **Streams** correctly and always check the return value of `.write()`.

---

## 🧪 Real-time Production Q&A

**Q: "How do we implement backpressure in a REST API?"**
**A**: Use **Rate Limiting** and **Concurrency Limits**. If your Node.js process has > 100 active requests, start returning `503 Service Unavailable`. This tells the load balancer (and the user) that the service is full.

---

## 🏢 Industry Best Practices
- **Fail Fast**: Don't let requests hang for 30 seconds. Use short timeouts and return errors quickly.
- **Load Shedding**: It is better to serve 90% of users perfectly and 10% with a 503 than to serve 100% of users with 30s latency.

---

## 💼 Interview Questions
**Q: What is the difference between a Rate Limiter and a Circuit Breaker?**
**A**: A **Rate Limiter** protects a service from its *clients* (prevents too many requests). A **Circuit Breaker** protects a service from its *dependencies* (prevents waiting on a failing downstream service).

---

## 🧩 Practice Problems
1. Implement a simple "Load Shedder" middleware that checks the current event loop lag and returns 503 if lag is > 200ms.
2. Build a stream pipeline that reads a 10GB file and writes it to a slow network socket. Observe how `readable.pause()` and `readable.resume()` are called automatically.

---

**Prev:** [06_Stateful_vs_Stateless.md](./06_Stateful_vs_Stateless.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [../Data/01_Database_Connections.md](../Data/01_Database_Connections.md)
