# 📌 04 — Cluster Module

## 🌟 Introduction

Most modern computers have 4, 8, or even 16 CPU cores. However, by default, Node.js runs on only **one single core**. This means if you have an 8-core server, you are wasting 87% of your hardware's power!

The **Cluster Module** allows you to create multiple copies of your app (called **Workers**) that all run at the same time and share the same server port.

Think of it like a **Restaurant Expansion**:
-   **Standard Node.js:** 1 chef in a tiny kitchen. He can only cook one meal at a time.
-   **Cluster Module:** 8 chefs in 8 kitchens, but they all share the same front door. They can handle 8x more customers!

---

## 🏗️ How it Works

1.  **Primary (Master) Process:** The manager. It doesn't handle requests. Its only job is to "spawn" workers and restart them if they crash.
2.  **Worker Processes:** The actual app. Each worker runs on its own CPU core.

---

## 🚀 Why Use Clustering?

1.  **High Performance:** Use 100% of your server's CPU power.
2.  **Reliability:** If one worker crashes due to a bug, the other workers keep handling requests. The user never sees an error.
3.  **Zero-Downtime Updates:** You can restart workers one by one to update your code without ever stopping the server.

---

## 🔍 Code Walkthrough: Basic Cluster

```javascript
const cluster = require('cluster');
const http = require('http');
const os = require('os');

if (cluster.isPrimary) {
  // 1. We are the MANAGER. Count the CPUs.
  const numCPUs = os.cpus().length;
  console.log(`Primary ${process.pid} is running. Forking ${numCPUs} workers...`);

  // 2. Create one worker for every CPU core
  for (let i = 0; i < numCPUs; i++) {
    cluster.fork();
  }

  // 3. If a worker dies, start a new one immediately!
  cluster.on('exit', (worker) => {
    console.log(`Worker ${worker.process.pid} died. Starting a replacement...`);
    cluster.fork();
  });

} else {
  // 4. We are a WORKER. We handle actual requests.
  http.createServer((req, res) => {
    res.writeHead(200);
    res.end(`Hello from Worker ${process.pid}\n`);
  }).listen(8000);
}
```

---

## 📐 Visualizing the Cluster

```text
       [ INCOMING REQUESTS ]
                 │
                 ▼
        [ PRIMARY PROCESS ] (Load Balancer)
         /       |       \
        ▼        ▼        ▼
    [Worker 1] [Worker 2] [Worker 3] (on different CPU cores)
```

---

## ⚠️ The Golden Rule: No Shared Memory

Because each worker is a **separate process**, they do **not** share variables.

-   If you set `let count = 0` in your code, every worker has its own `count`.
-   If Worker 1 increments its count, Worker 2 stays at 0.

**The Solution:** Use an external database or **Redis** if you need to share data (like sessions or a cache) between workers.

---

## 🔬 Deep Technical Dive (V8 Internals)

### Round-Robin Scheduling
How does the Primary process decide which worker gets the next request? On most systems (Windows/Mac), Node.js uses **Round-Robin**. It simply goes in a circle: Worker 1, then 2, then 3, then 1 again. On Linux, the operating system kernel handles this distribution automatically for even better performance.

---

## 💼 Interview Questions

**Q1: What is the difference between Cluster and Worker Threads?**
> **Ans:** **Cluster** creates separate *processes* (isolated memory, good for scaling web servers). **Worker Threads** create separate *threads* within the same process (shared memory, good for heavy math/CPU tasks).

**Q2: How many workers should you create?**
> **Ans:** Generally, you should create one worker for every physical CPU core on your machine (using `os.cpus().length`). Creating more can actually slow things down because the CPU has to waste time switching between them.

**Q3: Can workers share a port?**
> **Ans:** Yes! This is the magic of the Cluster module. Even though they are separate processes, Node.js handles the magic of allowing them to all "listen" on port 80 or 3000 at the same time.

---

## ⚖️ Trade-offs

| Feature | Single Instance | Cluster |
| :--- | :--- | :--- |
| **CPU Usage** | 1 Core. | All Cores. |
| **Fault Tolerance** | Zero (If it crashes, site is down). | High (If one dies, others stay up). |
| **Complexity** | Simple. | Medium (Requires Redis for shared data). |
| **Memory** | Low. | Higher (Each worker uses its own RAM). |

---

## 🔗 Navigation

**Prev:** [03_Streams.md](03_Streams.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [05_Worker_Threads.md](05_Worker_Threads.md)
