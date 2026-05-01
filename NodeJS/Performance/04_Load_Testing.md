# 📌 Topic: Load Testing

## 🧠 Concept Explanation
Load Testing is the practice of simulating high levels of traffic to your application to understand how it behaves under pressure. It's about finding the "Breaking Point" before your users do.

**The Bridge Stress-Test Analogy (Deep Dive):**
Imagine you have just built a new bridge over a river.
*   **Normal Day:** 10 cars a minute drive across. The bridge is silent and steady. This is your "Baseline."
*   **The Load Test (The Heavy Convoy):** You hire 1,000 heavy-duty trucks to drive across the bridge at the exact same time.
    *   **Latency (The Sway):** As the trucks get onto the bridge, it starts to sway. This is your "Response Time." If it sways too much, users get scared (Frustration).
    *   **Throughput (The Flow):** You want to see how many trucks can cross per hour. If the line of trucks backs up to the highway, your "Throughput" has hit its limit.
    *   **The Breaking Point (The Collapse):** At what point does a bolt snap? At what point does the concrete crack? You want to know that at truck #950, the bridge becomes unsafe. This is your **Saturation Point**.

---

## 🏗️ Mental Model
Think of Load Testing as a **Dialogue between your App and its Resources**.
*   **Requests Per Second (RPS):** How many "questions" can your app answer per second?
*   **Latency Percentiles (The Tail):** Don't look at the average! 
    *   **P50 (Median):** What the "average" user feels.
    *   **P99:** What the unluckiest 1% of users feel. This is where you find the real bugs.
*   **Saturation:** The point where adding more CPU or RAM doesn't help because another resource (like the DB connection pool) is full.

---

## ⚡ Actual Behavior
When you run a load test on Node.js:
1.  **The JIT Warm-up:** For the first few thousand requests, V8 is "Learning." It's compiling JS into machine code. Your latency will be high and erratic. Once it's "Warm," latency drops and stabilizes.
2.  **Event Loop Lag:** As concurrency increases, the Event Loop takes longer to finish a full rotation. You'll see "Lag" increase, meaning tasks are sitting in the queue longer before they even start.
3.  **Socket Exhaustion:** If your test is too aggressive, you might run out of local ports or "File Descriptors." Your OS will start throwing `EMFILE` errors, not because Node.js is slow, but because the OS can't open any more "pipes."
4.  **Database Bottleneck:** Often, you'll find that Node.js is only at 20% CPU, but the database is at 100%. Node.js is just waiting for the DB to answer. Adding more Node.js servers here will actually make the problem *worse*.

---

## 🔬 Internal Mechanics (V8 + libuv + OS)
*   **TCP Backlog (SOMAXCONN):** When a request arrives, it sits in a "Pending" queue in the OS kernel before Node.js calls `accept()`. If you send 10,000 requests in 1ms, this queue fills up instantly. Any further requests are "Dropped" by the OS, and the user gets a "Connection Refused" error without Node.js ever seeing the request.
*   **V8 Scavenging:** High throughput means high object creation. You'll see the V8 "Scavenger" GC running every few milliseconds. This is normal, but if it takes too long, it will add "Jitter" to your P99 latency.
*   **Context Switching:** If you have 1,000 concurrent "Users" in your test, the OS has to manage 1,000 different TCP sockets. The CPU spends a significant amount of its time just switching its focus from one socket to another. This "Management Overhead" is why a single process can eventually reach a limit even if the code is fast.
*   **The "Knee" in the Curve:** Performance is usually linear (double the users, double the RPS) until you hit the "Knee." After this point, throughput flattens and latency goes "Vertical." Your load test's main goal is to find exactly where this "Knee" is.

---

## 🔁 Execution Flow
1.  **Baseline:** Measure app idling (CPU/RAM).
2.  **Ramp-up:** Gradually increase concurrent users from 1 to 500.
3.  **Peak:** Hold high load for 5-10 minutes.
4.  **Ramp-down:** Observe how long it takes for the app to recover (e.g., does memory drop back down?).
5.  **Analyze:** Find the P99 latency and the point where errors started appearing.

---

## 🧠 Resource Behavior
*   **CPU:** Usually hits 100% first in Node.js apps.
*   **Memory:** Should stay stable. A steady climb indicates a leak.
*   **Disk:** High if you are logging every request during the test.

---

## 📐 ASCII Diagrams
```text
PERFORMANCE CURVE
Latency
  ^         / (Breaking Point / Knee)
  |        /
  |       /
  | _____/
  +------------> RPS
     (Linear)
```

---

## 🔍 Code Example (Latest Node.js - Using Autocannon)
```bash
# Install
npm install -g autocannon

# Run a test: 100 concurrent connections for 10 seconds
autocannon -c 100 -d 10 http://localhost:3000

# Results will show:
# Req/Sec: How many total requests per second
# Bytes/Sec: Throughput
# Latency: P50, P90, P99
```

---

## 💥 Production Failures
*   **Testing against Production:** Running a load test against your live site and accidentally taking it down for real users. (Solution: Use a Staging environment).
*   **Ignoring the Network:** Testing from your laptop to a server across the country. Your results will measure the internet's speed, not your server's speed. (Solution: Run the test from the same data center).

---

## 🧪 Real-time Scenarios
*   **Black Friday Sale:** Simulating 10x normal traffic to ensure the checkout service can handle the spike.
*   **New Feature Launch:** Checking if a new complex query slows down the whole API.

---

## ⚠️ Edge Cases
*   **Statelessness:** If your app uses sessions, the load tester must support "Cookie Persistence," otherwise every request will look like a new user.
*   **Caching:** If you test the same URL over and over, you are just testing your cache. Use randomized parameters to test the real DB logic.

---

## 🏢 Best Practices
1.  **Monitor the Server:** Use `top` or `htop` on the server while the test is running.
2.  **Test the Full Stack:** Don't just test a "Hello World" endpoint; test real flows (Login -> Search -> Purchase).
3.  **Automate:** Run a small load test as part of your CI/CD pipeline to catch performance regressions.

---

## ⚖️ Trade-offs
*   **Autocannon:** Very fast, easy to use, but limited to HTTP.
*   **k6:** Scriptable in JS, handles multiple protocols (WebSockets, gRPC), gives beautiful reports, but more complex to set up.

---

## 💼 Interview Q&A
*   **Q:** What is "P99 Latency" and why is it important?
*   **A:** It means 99% of requests were faster than this value. It's important because it represents the "worst case" experience for your users. A fast average doesn't matter if 1 in 100 users waits 10 seconds.

---

## 🧩 Practice Problems
1.  Run `autocannon` on a simple Node.js server and note the RPS. Then add a 10ms `while` loop block and see how much the RPS drops.
2.  Write a `k6` script that performs a GET request with a random ID between 1 and 1000.

---
Prev: [03_Caching_Strategies.md](./03_Caching_Strategies.md) | Index: [NodeJS/00_Index.md](../00_Index.md) | Next: [05_Scaling_NodeJS.md](./05_Scaling_NodeJS.md)
