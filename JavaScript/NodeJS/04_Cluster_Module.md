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

## 🚀 Code Walkthrough: Express Server Cluster

While the basic example uses the built-in `http` module, in the real world, you are likely using **Express**. The cluster logic remains exactly the same!

```javascript
const cluster = require('cluster');
const os = require('os');
const express = require('express');

if (cluster.isPrimary) {
  // Primary process: Spawn workers
  const numCPUs = os.cpus().length;
  console.log(`Primary ${process.pid} is running. Forking ${numCPUs} workers...`);

  for (let i = 0; i < numCPUs; i++) {
    cluster.fork();
  }

  cluster.on('exit', (worker, code, signal) => {
    console.log(`Worker ${worker.process.pid} died. Starting a new one...`);
    cluster.fork();
  });
} else {
  // Worker process: Run the Express app
  const app = express();

  app.get('/', (req, res) => {
    res.send(`Hello from Express! Handled by Worker ${process.pid}`);
  });

  // Simulate a CPU-heavy task to see load balancing
  app.get('/heavy', (req, res) => {
    let total = 0;
    for (let i = 0; i < 50000000; i++) {
      total++;
    }
    res.send(`Heavy task finished by Worker ${process.pid}. Total: ${total}`);
  });

  app.listen(3000, () => {
    console.log(`Worker ${process.pid} listening on port 3000`);
  });
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

---

## 🧠 Deep Dive: Process vs. Thread (The Confusion Killer)

This is the most common point of confusion. Let's break it down once and for all.

### 1. What is a Process? (Used by **Cluster**)
A **Process** is a completely independent "container" for a program. 
- **Isolation:** It has its own private memory (RAM). Process A cannot touch Process B's variables.
- **Independence:** If Process A crashes, Process B keeps running perfectly.
- **Overhead:** High. Starting a new process is like starting a whole new factory. It takes more RAM and time.
- **Analogy:** **Two different Restaurants.** They have different kitchens, different staff, and different bank accounts. They don't share anything.

### 2. What is a Thread? (Used by **Worker Threads**)
A **Thread** is a smaller execution unit *inside* a process.
- **Shared Memory:** Multiple threads in the same process **share the same RAM**. This is fast but dangerous (one thread could accidentally overwrite another's data).
- **Dependence:** If the main process crashes, all its threads die instantly.
- **Overhead:** Low. Starting a thread is like hiring one more cook in an existing kitchen. It's fast and uses very little extra RAM.
- **Analogy:** **Two Chefs in the SAME Restaurant.** They share the same fridge, the same stove, and the same ingredients. They have to communicate carefully so they don't bump into each other!

### Summary Table

| Feature | Process (Cluster) | Thread (Worker Thread) |
| :--- | :--- | :--- |
| **Memory** | **Isolated.** Each has its own. | **Shared.** They use the same memory. |
| **Crashing** | If one dies, others live. | If process dies, all threads die. |
| **Communication** | Slow (IPC). Like sending an email. | Fast. Like talking across the table. |
| **Resource Cost** | High (Heavyweight). | Low (Lightweight). |
| **Best For** | Scaling web servers (I/O). | Heavy data processing (CPU). |

---

---

## 🌍 Connecting to Hardware: Cores vs. Threads

To truly master performance, you need to understand how your code interacts with the physical CPU chip inside your computer.

### 1. Physical Cores vs. Logical Cores
-   **Physical Cores:** These are the actual "brains" on the CPU chip. If you have a 4-core CPU, you have 4 physical processing units.
-   **Logical Cores (Threads/Hyper-Threading):** Modern CPUs (Intel/AMD) use a trick called **Hyper-Threading**. It allows one physical core to act like two. So, a 4-core CPU will often show up in your OS as **8 Logical Processors**.
-   **How to check in Node:** `os.cpus().length` returns the number of **Logical Cores**.

> **💡 The Best Analogy: The 2-Handed Chef**
> - **A Physical Core** is like a **Chef**.
> - **A Logical Thread** is like one of the **Chef's hands**.
> 
> If a Chef (Core) has two hands (Threads), they can chop vegetables with the left hand while stirring a pot with the right. They are only **one person**, but they can handle **two tasks** at the exact same time. 
> 
> If the Chef is waiting for the oven to beep (waiting for data from the hard drive), they don't just stand there; they use their other hand to keep working on something else. This is why we spawn workers based on **Logical Cores (Hands)**, not just Physical Cores (Chefs)!

### 2. Parallelism vs. Concurrency
-   **Parallelism (True Speed):** When you have 4 Cluster Workers running on 4 different cores, they are doing work at the **exact same millisecond**. This is what you want for maximum performance.
-   **Concurrency (The Illusion):** If you create 50 Workers on a 4-core machine, the CPU has to "juggle" them. It runs Worker 1 for a tiny bit, then switches to Worker 2. This is called **Context Switching**. If you do this too much, your server actually slows down because the CPU spends more time "juggling" than "cooking."

### 3. The Node.js Internal Thread Pool (Libuv)
Even when you run a "Single-Instance" Node app, it isn't truly single-threaded!
-   **The Main Thread:** Where your JavaScript code and the Event Loop live.
-   **The Libuv Thread Pool:** Node.js has a hidden pool of **4 default threads** used for heavy tasks that the OS can't do easily (like `fs` file operations, `crypto`, and `zlib` compression).
-   **Difference:** These internal threads are managed by Node.js automatically. **Worker Threads** and **Cluster Workers** are threads/processes managed by **YOU**.

---

## 💼 Interview Questions

**Q1: What is the difference between Cluster and Worker Threads?**
> **Ans:** 
> - **Cluster:** Creates separate **OS processes**. Each worker has its own memory space, V8 instance, and Event Loop. They communicate via IPC (Inter-Process Communication). Best for scaling **I/O bound** tasks (like web servers) across multiple CPU cores.
> - **Worker Threads:** Creates separate **threads** within the *same* process. They share the same memory space (though they can also use `SharedArrayBuffer` for efficiency) and are much "lighter" than clusters. Best for **CPU-bound** tasks (like heavy encryption, image processing, or complex math).

**Q2: How many workers should you create?**
> **Ans:** The industry standard is to create **one worker for every physical CPU core** (`os.cpus().length`). 
> - **Why not more?** If you create more workers than cores, the CPU has to "context switch" (pause one worker to let another run). This switching takes time and actually reduces performance.
> - **Pro Tip:** In production, some engineers leave 1 core free for the OS and the Primary process to ensure the system stays responsive under extreme load.

**Q3: How can multiple workers share the same port without a "Port in Use" error?**
> **Ans:** This is handled by the **Primary process**. 
> 1. The Primary process actually creates the server socket and listens on the port.
> 2. When a request comes in, the Primary process decides which worker should handle it.
> 3. It then "hands over" the connection handle to the chosen worker via **IPC**. 
> 4. To the outside world, it looks like one server; internally, it's a coordinated team.

**Q4: If a worker crashes, does the whole server go down?**
> **Ans:** No. This is one of the biggest benefits of clustering. Since each worker is an independent process, if one crashes (e.g., due to an uncaught exception), the others continue to function. The Primary process can listen for the `exit` event and immediately `fork()` a new worker to replace the dead one, providing **high availability**.

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
