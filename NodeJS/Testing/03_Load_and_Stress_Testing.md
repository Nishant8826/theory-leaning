# 📌 03 — Load and Stress Testing: Finding the Breaking Point

## 🧠 Concept Explanation

### Basic → Intermediate
Load Testing measures how the system performs under an expected amount of traffic. Stress Testing pushes the system beyond its limits to see how it fails (Graceful vs Catastrophic).

### Advanced → Expert
At a staff level, load testing is about **Performance Regression Detection**.
1. **Saturation Point**: The point where adding more users doesn't increase throughput but significantly increases latency.
2. **Soak Testing**: Running a steady load for a long period (e.g. 24 hours) to find memory leaks or resource exhaustion that only appear over time.
3. **Spike Testing**: Suddenly increasing traffic by 10x to see how the auto-scaling and backpressure mechanisms react.

We use tools like **k6** (scriptable in JS) or **Gatling** because they provide a "Virtual User" model that simulates realistic browser behavior.

---

## 🏗️ Common Mental Model
"I'll just run a benchmark on one endpoint."
**Correction**: Load testing must simulate **User Journeys**. A user doesn't just hit `/api/search` 1000 times. They Login ──▶ Search ──▶ View Item ──▶ Add to Cart. Real-world bottlenecks often appear in the *transitions* between services.

---

## ⚡ Actual Behavior: The "Knee" in the Curve
Every system has a "knee" in its latency curve. Before this point, latency is stable. After this point, the event loop queue or the database thread pool becomes saturated, and latency grows exponentially. Load testing identifies this exact RPS value.

---

## 🔬 Internal Mechanics (Networking + OS)

### Ephemeral Port Exhaustion
During a high-intensity load test, the testing machine might run out of ports to open new connections to the server. This can make it look like the *server* is failing when it's actually the *load generator*.

---

## 📐 ASCII Diagrams

### Load vs Stress Testing
```text
  Throughput (RPS)
     ▲
     │       [ SATURATION ]
     │      ┌──────────────┐
     │     /               │ [ BREAKING POINT ]
     │    /                │ ──▶ CRASH
     │___/                 │
     └────────────────────────▶ Time / Load
       (Load Test)           (Stress Test)
```

---

## 🔍 Code Example: Load Test Script with k6
```javascript
import http from 'k6/http';
import { sleep, check } from 'k6';

// Define the test options
export const options = {
  stages: [
    { duration: '1m', target: 100 }, // Ramp up to 100 users
    { duration: '5m', target: 100 }, // Stay at 100 users
    { duration: '1m', target: 0 },   // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(99)<500'], // 99% of requests must be < 500ms
  },
};

export default function () {
  const res = http.get('http://localhost:3000/api/health');
  
  check(res, {
    'is status 200': (r) => r.status === 200,
  });
  
  sleep(1); // Think time: wait 1s between requests
}
```

---

## 💥 Production Failures & Debugging

### Scenario: The Database Bottleneck
**Problem**: During the load test, the Node.js CPU is only 20%, but latency is 10 seconds.
**Reason**: The database is at 100% CPU or has run out of connections.
**Fix**: Tune the database (indexes, query optimization) or implement a cache.

### Scenario: The "Cold" Cache Failure
**Problem**: The app handles the load test perfectly on Monday. On Tuesday morning, after a cache flush, it crashes under the same load.
**Reason**: The app was relying on the cache to hide slow database queries. Without the cache, the "Cold" performance is too low.
**Fix**: Load test with a **Cold Cache** to see your system's baseline performance.

---

## 🧪 Real-time Production Q&A

**Q: "Should I run load tests on my local machine?"**
**A**: **Only for initial scripts.** To get real results, run your load generator (k6) in the same cloud region as your server but on a **different instance**. Network latency between your house and AWS will invalidate your results.

---

## 🏢 Industry Best Practices
- **Monitor Everything**: While load testing, watch your Server CPU, Memory, DB CPU, and Event Loop Lag.
- **Automate in CI**: Run a small load test on every major release to ensure no performance regressions were introduced.

---

## 💼 Interview Questions
**Q: What is "Throughput" vs "Goodput"?**
**A**: **Throughput** is the total number of packets/requests sent. **Goodput** is the number of *successful* requests (e.g. status 200) that delivered meaningful data to the user. During a crash, throughput might be high (errors), but goodput is zero.

---

## 🧩 Practice Problems
1. Write a k6 script that performs a login and then uses the returned JWT to access a protected resource.
2. Identify the "Saturation Point" of a simple Node.js app by slowly increasing the number of virtual users until the p99 latency exceeds 1 second.

---

**Prev:** [02_Integration_Testing_Strategies.md](./02_Integration_Testing_Strategies.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [04_Contract_Testing.md](./04_Contract_Testing.md)
