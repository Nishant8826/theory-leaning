# 📌 Topic: Deployment Strategies

## What
### 🧠 Concept Explanation
Deployment is the process of moving your code from a developer's machine to the production environment where real users can access it. In modern Node.js engineering, deployment isn't just about "copying files"; it's about managing traffic and ensuring continuity.

**The Changing Tires on a Moving Car Analogy (Deep Dive):**
Imagine your application is a high-speed car on a highway (The Internet).
*   **Big Bang Deployment (The Stop & Go):** You force the car to stop on the shoulder, kick the passengers out, change all four tires, and then start the car again.
    *   **The Problem:** The passengers are angry because they were late (Downtime).
*   **Rolling Update (The Pit Crew):** You hire a world-class pit crew. As the car slows down slightly, you change the front-left tire, then the front-right, and so on.
    *   **The Result:** The car never stops, but for a few minutes, the car is running on a mix of old and new tires. This is **Version Coexistence**.
*   **Blue-Green (The Second Car):** You buy a completely identical second car with the new tires already installed. You drive the two cars side-by-side at 70 mph. You tell the passengers to jump from the old car (Blue) to the new car (Green) while they are moving.
    *   **The Result:** Zero downtime. If the new car has a engine failure, the passengers just jump back to the old car. This is **Instant Rollback**.
*   **Canary (The Scout):** You put the new tires on a small motorcycle and send it 1 mile ahead of the car. If the motorcycle doesn't crash, you put the tires on the main car.

---

### 🏗️ Mental Model
Think of Deployment as **Traffic Orchestration**.
1.  **Immutability:** You don't "update" a server. You delete the old server and create a new one from an image.
2.  **Statelessness:** For any deployment strategy to work, your Node.js app must be stateless. If you store user data in RAM, they will lose it when the server is replaced.
3.  **The "Liveness" vs. "Readiness" Distinction:**
    *   **Liveness:** Is the Node.js process running?
    *   **Readiness:** Is the Node.js app actually ready to handle a request (e.g., is the database connection open)?

---

## Why
### 🏢 Best Practices
1.  **Automate Rollbacks:** If the error rate exceeds 1% during a Canary deploy, the system should rollback automatically.
2.  **Separate DB Migrations:** Never do code changes and DB schema changes in the same atomic step.
3.  **Graceful Shutdown:** Listen for `SIGTERM` and close the server correctly.
4.  **Feature Flags:** Use flags (like LaunchDarkly) to turn features on/off without a full deployment.

---

### ⚖️ Trade-offs
*   **Rolling:** Resource efficient, but slow and hard to rollback quickly.
*   **Blue-Green:** Safe and fast rollback, but very expensive.
*   **Canary:** Safest for users, but most complex to set up and monitor.

---

## How
### ⚡ Actual Behavior
During a production deployment:
1.  **The New Instance:** A new Node.js process starts. It begins its "Warm-up" phase—connecting to Redis, warming up its internal caches, and allowing V8 to JIT-compile the code.
2.  **Health Verification:** The Load Balancer (or Kubernetes) repeatedly calls your `/readiness` endpoint. Your app must respond with `200 OK`. If it returns `503`, the deployment waits.
3.  **Traffic Shifting:** Once the new instance is "Ready," the Load Balancer starts sending it new TCP connections.
4.  **The Draining Phase:** The "Old" instance is told to stop accepting new requests (`SIGTERM`). However, it stays alive for 30-60 seconds to finish the requests it already had in progress. This is **Graceful Shutdown**.
5.  **Termination:** Once the old instance has "Drained" its event loop, it exits, and the OS reclaims the RAM.

---

### 🔬 Internal Mechanics (V8 + libuv + OS)
*   **The Load Balancer Handoff:** When you switch from Blue to Green, the Load Balancer doesn't "kill" the existing TCP sockets. It simply directs *new* `SYN` packets (the start of a TCP handshake) to the Green servers. Existing long-lived sockets (like a file upload or a WebSocket) will continue to talk to the Blue servers until they close.
*   **The `SIGTERM` Lifecycle:** When the OS wants to kill a Node.js process for a deployment, it sends a `SIGTERM`. Node.js doesn't die instantly. It triggers a `process.on('SIGTERM')` event. 
    *   Inside this event, you should call `server.close()`.
    *   This tells libuv to stop accepting new connections on the listen socket but keep the event loop running as long as there are active "Handles" (active requests).
*   **Memory Management during Coexistence:** During a Rolling Update, you might have 2x the normal number of processes running on the same hardware. If each Node.js process uses 1GB of RAM and your server has 1.5GB, the OS will start "Swapping" to disk, causing your P99 latency to explode.
*   **Service Discovery:** In a Horizontal Scaling environment, the "Green" servers must register their new IP addresses in a central registry (like Consul or Kubernetes CoreDNS). The Load Balancer watches this registry to know where to send the traffic. There is often a "Propagation Delay" of a few seconds where the system might try to send traffic to a server that isn't quite ready yet.

---

### 🔁 Execution Flow (Blue-Green)
1.  Environment **Blue** is live (v1.0.0).
2.  Deploy v1.1.0 to Environment **Green**.
3.  Run smoke tests on **Green**.
4.  Switch **Load Balancer** target from Blue to Green.
5.  Monitor Green for errors.
6.  If errors occur, switch back to Blue immediately.
7.  If Green is stable, decommission Blue.

---

### 🔍 Code Example (Latest Node.js - Readiness Check for K8s)
```javascript
import express from 'express';
const app = express();

let isReady = false;

// Simulated DB Connection
setTimeout(() => {
    isReady = true;
    console.log('Database connected. App is ready.');
}, 5000);

// Kubernetes will check this before sending traffic
app.get('/readiness', (req, res) => {
    if (isReady) {
        res.status(200).send('Ready');
    } else {
        res.status(503).send('Not Ready');
    }
});

app.listen(3000);
```

---

## Impact
### 💥 Production Failures
*   **Database Schema Mismatch:** You deploy v2 which needs a new DB column, but v1 is still running and doesn't know about it. (Solution: Use "Expand and Contract" DB migrations—add the column in one deploy, use it in the next).
*   **Session Loss:** If you use in-memory sessions, moving users to a new environment will log everyone out. (Solution: Use Redis).

---

### 🧪 Real-time Scenarios
*   **Major UI Overhaul:** Using Blue-Green to ensure that if the new UI is broken, you can flip back in milliseconds.
*   **Risk Mitigation:** Using Canary to test a new "Payment Logic" on only 1% of users before rolling it out to everyone.

---

### ⚠️ Edge Cases
*   **Hard-coded IPs:** If your frontend has the IP of the server hard-coded, Blue-Green will never work.
*   **Long-running Requests:** A file upload that takes 10 minutes might be cut off if the old server is terminated too quickly.

---

---

Prev: [03_Test_Automation.md](./03_Test_Automation.md) | Index: [NodeJS/00_Index.md](../00_Index.md) | Next: [../Cloud/01_Deploy_to_AWS_EC2.md](../Cloud/01_Deploy_to_AWS_EC2.md)
