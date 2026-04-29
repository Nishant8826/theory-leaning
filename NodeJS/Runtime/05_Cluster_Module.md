# 📌 05 — Cluster Module: Multi-Process Throughput

## 🧠 Concept Explanation

### Basic → Intermediate
The Cluster module allows you to create multiple instances of your Node.js application, each running on its own CPU core. Since Node.js is single-threaded (in terms of JS execution), clustering is the primary way to scale horizontally on a single machine.

### Advanced → Expert
At the system level, the Cluster module uses a **Master/Worker process model**.
- **Master Process**: Orchestrates the workers. It doesn't actually handle requests; it just manages the workers' lifecycles.
- **Worker Processes**: Independent OS processes that share the same server port.

Communication between Master and Workers happens via **IPC (Inter-Process Communication)** using a built-in pipe.

---

## 🏗️ Common Mental Model
"The Cluster module balances the load between CPUs."
**Correction**: The Cluster module balances **TCP connections**. It doesn't know about the CPU load of individual workers. By default, it uses a **Round-Robin** strategy to distribute connections.

---

## ⚡ Actual Behavior: Port Sharing
How can multiple processes listen on the same port (e.g. 8080)?
1. The **Master** process creates the server socket.
2. It then **hands off** the socket handle to the workers.
3. In modern Linux, this can also be handled by the kernel using the `SO_REUSEPORT` socket option.

---

## 🔬 Internal Mechanics (V8 + libuv + syscalls)

### IPC and the 'message' event
IPC in Node.js uses Unix Domain Sockets (on Linux/macOS) or Named Pipes (on Windows). When you `send()` a message, it is serialized to a string/buffer and transmitted via a syscall (`write()`).

### Round-Robin Strategy
The Master process accepts the connection in its own event loop and then sends the file descriptor of the new connection to a worker via IPC. The worker then handles the request.

---

## 📐 ASCII Diagrams

### Cluster Architecture
```text
      ┌───────────────────────────┐
      │      MASTER PROCESS       │
      │  (Port 8080, Load Balancer)│
      └──────────────┬────────────┘
                     │
         ┌───────────┴───────────┐
         │ (IPC Channel)         │
         ▼                       ▼
  ┌──────────────┐        ┌──────────────┐
  │   WORKER 1   │        │   WORKER 2   │
  │ (Event Loop) │        │ (Event Loop) │
  └──────────────┘        └──────────────┘
```

---

## 🔍 Code Example: Basic Cluster Implementation
```javascript
const cluster = require('cluster');
const http = require('http');
const numCPUs = require('os').cpus().length;

if (cluster.isMaster) {
  console.log(`Master ${process.pid} is running`);

  // Fork workers for each CPU core
  for (let i = 0; i < numCPUs; i++) {
    cluster.fork();
  }

  cluster.on('exit', (worker, code, signal) => {
    console.log(`Worker ${worker.process.pid} died. Respawning...`);
    cluster.fork(); // Resilience: Auto-respawn
  });
} else {
  // Workers can share any TCP connection
  http.createServer((req, res) => {
    res.writeHead(200);
    res.end('Hello from Cluster!\n');
  }).listen(8080);

  console.log(`Worker ${process.pid} started`);
}
```

---

## 💥 Production Failures & Debugging

### Scenario: The Sticky Session Problem
**Problem**: You are using Socket.io or a stateful API. A user logs in, but their next request fails because it is routed to a different worker that doesn't have their session.
**Reason**: Cluster's Round-Robin strategy doesn't guarantee that the same IP will go to the same worker.
**Fix**: Use an external store like **Redis** for sessions, or a load balancer that supports "Sticky Sessions" based on IP hash.

### Scenario: High Latency due to IPC overhead
**Problem**: You are sending massive data objects between Master and Workers via `process.send()`.
**Reason**: Every message must be serialized to JSON, piped through a socket, and de-serialized. This can block the event loop of both processes.
**Fix**: Use **Shared Memory** (Worker Threads) if you need to share large data sets.

---

## 🧪 Real-time Production Q&A

**Q: "Should I use the Cluster module if I am running in Kubernetes?"**
**A**: **Usually No.** Kubernetes scales by adding more Pods (containers). Each Pod should ideally be small and single-process to allow the K8s scheduler to do its job effectively. If you have a 16-core node, K8s will run multiple Pods on it anyway. Use Clustering only if your container is specifically allocated multiple cores.

---

## 🧪 Debugging Toolchain
- **`pm2`**: The industry standard for managing clusters. It handles auto-restarts, zero-downtime reloads, and monitoring out of the box.

---

## 🏢 Industry Best Practices
- **Graceful Shutdown**: When a worker needs to stop, call `server.close()` to stop accepting new connections, but finish existing ones before calling `process.exit()`.
- **Statelessness**: Never store important data in the memory of a cluster worker.

---

## 💼 Interview Questions
**Q: How does the Master process detect that a worker has died?**
**A**: The Master process monitors the OS child process signals (like `SIGCHLD`). Libuv provides a `uv_signal_t` handle to catch these events.

---

## 🧩 Practice Problems
1. Build a custom load balancer in the Master process that uses a "Least Connections" strategy instead of Round-Robin.
2. Experiment with the `SCHED_NONE` cluster policy. Observe how the OS kernel handles connection distribution when Node's internal load balancer is disabled.

---

**Prev:** [04_Worker_Threads.md](./04_Worker_Threads.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [06_Process_Model.md](./06_Process_Model.md)
