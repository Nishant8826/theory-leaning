# 📌 05 — Benchmarking: Measuring RPS and Latency Correctly

## 🧠 Concept Explanation

### Basic → Intermediate
Benchmarking is the practice of running a performance test on your application to determine how many Requests Per Second (RPS) it can handle and what the Latency (response time) is under load.

### Advanced → Expert
At a staff level, benchmarking is about **Simulating Reality**. 
1. **RPS (Throughput)**: The total volume of work.
2. **Latency (p95, p99)**: The user experience. Focus on the "Tail Latency" (the slowest 1% of users).
3. **The Microbenchmark Trap**: Benchmarking a single function (like `a + b`) is often useless because V8 will optimize it away in a way that doesn't happen in real code.

The most important rule: **Only benchmark in a "Cold" environment (No other apps running) and after "Warming Up" the JIT compiler.**

---

## 🏗️ Common Mental Model
"My app handles 10,000 requests per second in my benchmark!"
**Correction**: That might be true for a "Hello World" endpoint. But real endpoints involve database calls, auth, and complex logic. A real-world benchmark must include these dependencies to be meaningful.

---

## ⚡ Actual Behavior: JIT Warming
When you first start a Node.js process, it is slow because V8 is interpreting code. After a few thousand requests, TurboFan optimizes the "Hot" paths. If you benchmark too early, you are measuring the interpreter speed, not the actual production speed.

---

## 🔬 Internal Mechanics (Networking + OS)

### Latency vs Throughput
You can have high throughput but high latency (e.g. processing 1000 requests at once but each takes 1 second). Conversely, you can have low latency but low throughput. In Node.js, we often trade a bit of latency for much higher throughput.

---

## 📐 ASCII Diagrams

### The Throughput/Latency Curve
```text
  Latency
     ▲
     │             / (Congestion / Queueing)
     │            /
     │      _____/
     │_____/
     └────────────────▶ Throughput (RPS)
```

---

## 🔍 Code Example: Benchmarking with Autocannon
```bash
# Install autocannon
npm install -g autocannon

# Run a 10-second benchmark with 100 concurrent connections
autocannon -c 100 -d 10 http://localhost:3000

# Results will show:
# Req/Sec: The throughput
# Latency: The average, p95, and p99 response times
```

---

## 💥 Production Failures & Debugging

### Scenario: The Coordinated Omission Problem
**Problem**: Your benchmark tool reports a p99 of 100ms, but your real-world users are reporting 5 seconds.
**Reason**: Most benchmarking tools stop sending requests when the server is "busy." If the server hangs for 5 seconds, the tool waits, and then only measures the *next* request. This "omits" the 5-second delay from the results.
**Fix**: Use a tool like **wrk2** or **autocannon** with a fixed request rate (`-r` flag) to ensure the tool keeps sending requests even when the server is slow.

### Scenario: Localhost Benchmarking
**Problem**: You benchmark a Node.js app on your laptop. It handles 50k RPS. You deploy to AWS and it only handles 5k RPS.
**Reason**: Localhost bypasses the real networking stack. In production, you have TCP overhead, firewalls, and context switching between the container and the host.
**Fix**: Always benchmark in an environment that matches production (CPU/RAM/Network).

---

## 🧪 Real-time Production Q&A

**Q: "Should I use `ab` (Apache Benchmark)?"**
**A**: **No.** `ab` is old and uses a single-threaded model that can't saturate a modern Node.js server. Use **Autocannon** (written in Node) or **wrk** (C) for multi-core, high-concurrency testing.

---

## 🏢 Industry Best Practices
- **Warm up for 30s**: Before starting the actual measurement.
- **Isolate the database**: If you want to benchmark the Node.js logic, use a "Mock" database to ensure you aren't just benchmarking the DB speed.

---

## 💼 Interview Questions
**Q: What is the difference between p95 and p99 latency?**
**A**: p95 means 95% of users had a response time faster than X. p99 means 99% of users were faster than Y. The difference between p95 and p99 often reveals "Edge Case" performance issues, like GC pauses or lock contention.

---

## 🧩 Practice Problems
1. Run a benchmark on an Express app with and without Gzip compression. Observe the trade-off between CPU usage and network throughput.
2. Compare the throughput of an Express app vs a Fastify app using `autocannon`.

---

**Prev:** [04_I_O_Optimization_Techniques.md](./04_I_O_Optimization_Techniques.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [../Security/01_OWASP_Top_10_in_NodeJS.md](../Security/01_OWASP_Top_10_in_NodeJS.md)
