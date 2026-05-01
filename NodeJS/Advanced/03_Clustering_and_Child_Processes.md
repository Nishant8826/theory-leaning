# 📌 Topic: Clustering and Child Processes

## What
### 🧠 Concept Explanation
Node.js is famously single-threaded, meaning it can only use one CPU core for JavaScript execution. On a modern server with 16 or 32 cores, a standard Node.js app leaves 90% of the hardware sitting idle. **Clustering** is the solution that allows Node.js to scale horizontally across a single machine.

**The Supermarket Analogy (Deep Dive):**
Imagine a massive supermarket (Your Server).
*   **The Single Process:** Initially, there is only **one cashier** (The Main Thread). No matter how many customers (Requests) arrive, they must all wait in one line. If one customer has a massive, complicated order (CPU-heavy task), the whole store grinds to a halt.
*   **Clustering (The Expansion):** The manager (The Primary Process) decides to open **8 checkout lanes**. 
    *   Each lane has its own cashier (Worker Process) and its own cash register (V8 Instance).
    *   The cashiers don't talk to each other; they are completely focused on their own line.
    *   **The Front Door (The Port):** To the customers outside, there is still only one front door (e.g., Port 3000). 
*   **The Greeter (The Load Balancer):** The manager stands at the door. As customers walk in, the manager says, "You go to Lane 1, you go to Lane 2." This ensures the work is distributed evenly.

---

### 🏗️ Mental Model
Think of Clustering as **Process Duplication**.
*   **Shared Nothing:** Unlike threads, processes share **no memory**. A variable defined in Worker 1 is invisible to Worker 2.
*   **The Master-Slave Relationship:** The Primary process is the "parent." It doesn't handle HTTP requests itself; its only job is to spawn workers and restart them if they die.
*   **The IPC Pipe:** Since they don't share memory, workers talk to the primary through a specialized "Inter-Process Communication" (IPC) channel—essentially a private chat room where they send JSON messages.

---

## Why
### 🏢 Best Practices
1.  **Use PM2:** In production, don't write your own cluster logic. Use PM2 (`pm2 start app.js -i max`), which handles restarts, logging, and monitoring.
2.  **Statelessness:** Ensure your workers are completely stateless.
3.  **Match CPU Cores:** Don't fork more workers than you have cores; it causes context-switching overhead.

---

### ⚖️ Trade-offs
*   **Pros:** Better performance, fault tolerance, utilizes multi-core hardware.
*   **Cons:** Higher memory usage, complex communication, shared state requires external DB (Redis).

---

## How
### ⚡ Actual Behavior
When you use the `cluster` module:
1.  **Bootstrapping:** The Primary process executes your code. It sees `cluster.isPrimary` is true.
2.  **Forking:** It calls `cluster.fork()`. This literally spawns a brand-new OS process that runs the *exact same file*.
3.  **Worker Execution:** The new process (the child) sees `cluster.isPrimary` is false. It skips the fork logic and starts the web server.
4.  **The Magic Port Sharing:** Normally, two apps can't listen to Port 3000. But Node.js handles this specially. When a worker calls `.listen(3000)`, it actually tells the Primary: "Hey, let me know when someone connects to 3000." The Primary accepts the connection and "hands off" the socket to the worker.

---

### 🔬 Internal Mechanics (V8 + libuv + OS)
*   **OS `fork()`:** On Unix-based systems, `cluster.fork()` is implemented using the `fork()` system call. This is incredibly efficient because it uses **Copy-on-Write (COW)**. The child process doesn't actually copy the parent's memory until it tries to change something.
*   **Round-Robin Scheduling:** By default, the Primary process uses a Round-Robin algorithm to distribute connections. It keeps a list of workers and hands the next connection to the next worker in line.
*   **Handle Passing:** Node.js uses a technique called "Handle Passing." It sends the raw file descriptor (the ID of the network connection) across the IPC pipe. The worker's Libuv then picks up that ID and starts talking to the client.
*   **Shared Port Implementation:** On Windows, the Primary process doesn't do the load balancing; it passes the listening socket to all workers, and the OS itself decides which worker gets the connection. On Linux, Node.js does the balancing manually for better control.

---

### 🔁 Execution Flow
1.  Primary starts.
2.  Primary calls `cluster.fork()` for each CPU core.
3.  Workers start and execute the same `app.js` but follow the "else" block of `cluster.isPrimary`.
4.  Worker calls `.listen(3000)`.
5.  Node.js intercepts this call and registers the worker with the Primary.

---

### 🔍 Code Example (Latest Node.js)
```javascript
import cluster from 'node:cluster';
import http from 'node:http';
import { availableParallelism } from 'node:os';
import process from 'node:process';

if (cluster.isPrimary) {
  const numCPUs = availableParallelism();
  console.log(`Primary ${process.pid} is running. Forking ${numCPUs} workers...`);

  for (let i = 0; i < numCPUs; i++) {
    cluster.fork();
  }

  cluster.on('exit', (worker, code, signal) => {
    console.log(`Worker ${worker.process.pid} died. Restarting...`);
    cluster.fork(); // Auto-restart!
  });
} else {
  // Workers can share any TCP connection
  http.createServer((req, res) => {
    res.writeHead(200);
    res.end(`Hello from Worker ${process.pid}`);
  }).listen(8000);

  console.log(`Worker ${process.pid} started`);
}
```

---

## Impact
### 💥 Production Failures
*   **Zombie Processes:** If the Primary dies but workers keep running, or if workers die and aren't restarted, your capacity drops.
*   **State Issues:** Since memory isn't shared, you can't store sessions in a local variable. You **must** use a shared store like Redis.

---

### 🧪 Real-time Scenarios
*   **High-Traffic APIs:** Using all 32 cores of a massive AWS EC2 instance to handle 50k requests per second.
*   **Graceful Reloads:** Restarting workers one by one so the app never goes offline during a deployment.

---

### ⚠️ Edge Cases
*   **Sticky Sessions:** If you use WebSockets, you need the client to stay with the *same* worker. Cluster's default load balancing can break this. (Solution: Use a specialized load balancer like Nginx or a library like `sticky-session`).
*   **Primary Blocking:** If the Primary process does heavy work, it will slow down the connection handoff for *all* workers.

---

---

Prev: [02_Buffer_and_Binary_Data.md](./02_Buffer_and_Binary_Data.md) | Index: [NodeJS/00_Index.md](../00_Index.md) | Next: [04_Worker_Threads.md](./04_Worker_Threads.md)
