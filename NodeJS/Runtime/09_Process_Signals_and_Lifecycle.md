# 📌 09 — Process Signals and Lifecycle: Graceful Termination and Docker Realities

## 🧠 Concept Explanation

### Basic → Intermediate
Every Node.js process has a lifecycle (Start ──▶ Run ──▶ Exit). You can interact with this lifecycle using **Signals** (like `SIGTERM` or `SIGINT`) which are asynchronous notifications sent to your process by the Operating System.

### Advanced → Expert
At a systems level, signals are **Software Interrupts**. 
- **SIGINT**: Sent when you press `Ctrl+C`.
- **SIGTERM**: The standard signal for "Please shutdown gracefully." Sent by Kubernetes or Docker.
- **SIGKILL**: (Signal 9) Immediate termination by the kernel. Your process **cannot** catch this or clean up.

In production (especially Docker), handling `SIGTERM` is mandatory. If you don't catch it, the kernel will wait (usually 10s) and then send `SIGKILL`, leading to data loss or database connection leaks.

---

## 🏗️ Common Mental Model
"The process stops as soon as I call `process.exit()`."
**Correction**: Calling `process.exit()` stops the **event loop** immediately, but it doesn't wait for pending I/O. For a clean exit, you must close all servers and wait for the loop to naturally become empty.

---

## ⚡ Actual Behavior: The "PID 1" Problem in Docker
In a container, if your Node.js app is the entrypoint (`ENTRYPOINT ["node", "app.js"]`), it runs as **PID 1**. On Linux, PID 1 has special behavior: it does **not** handle signals by default unless you explicitly write code to do so. This is why many Dockerized Node apps don't respond to `Ctrl+C` or take 10s to stop in K8s.

---

## 🔬 Internal Mechanics (V8 + libuv + syscalls)

### Signal Handling in libuv
Libuv uses a `uv_signal_t` handle. It uses a syscall (like `signalfd` on Linux) to integrate OS signals into the event loop. When a signal arrives, libuv wakes up and pushes the signal handler callback into the JS execution queue.

### BeforeExit vs Exit
- `beforeExit`: Emitted when the event loop is empty. You can perform async cleanup here (e.g. log one last message).
- `exit`: Emitted when the process is about to terminate. You **cannot** perform async tasks here; the loop is already dead.

---

## 📐 ASCII Diagrams

### The Graceful Shutdown Flow
```text
  1. SIGTERM Received ◀───────── (From K8s / OS)
     │
     ▼
  2. Stop Accepting Connections (server.close())
     │
     ▼
  3. Wait for Active Requests to finish
     │
     ▼
  4. Close DB Connections / Redis Pools
     │
     ▼
  5. Process exits naturally (Empty Event Loop)
```

---

## 🔍 Code Example: The "Perfect" Shutdown
```javascript
const http = require('http');
const server = http.createServer((req, res) => {
  setTimeout(() => res.end('Done'), 5000); // Long request
});

server.listen(8080);

const shutdown = (signal) => {
  console.log(`Received ${signal}. Starting graceful shutdown...`);
  
  // 1. Stop accepting new connections
  server.close(() => {
    console.log('HTTP server closed.');
    // 2. Close DB connections here
    process.exit(0);
  });

  // 3. Forced exit after 10s if graceful fails
  setTimeout(() => {
    console.error('Could not close connections in time, forcing exit');
    process.exit(1);
  }, 10000).unref();
};

process.on('SIGTERM', () => shutdown('SIGTERM'));
process.on('SIGINT', () => shutdown('SIGINT'));
```

---

## 💥 Production Failures & Debugging

### Scenario: The Database Connection Leak
**Problem**: After every deployment, your Database connection count spikes and takes hours to decrease.
**Reason**: Your app is being killed via `SIGKILL` because it doesn't handle `SIGTERM`. The DB server doesn't know the client is gone and keeps the connection open until its own timeout (which can be hours).
**Fix**: Catch `SIGTERM` and call `db.disconnect()`.

### Scenario: The PID 1 "Zombie" Process
**Problem**: In Docker, you see many `<defunct>` processes.
**Reason**: Node.js running as PID 1 is not "reaping" child processes that have finished.
**Fix**: Use a lightweight init system like **tini** or **dumb-init** in your Dockerfile.

---

## 🧪 Real-time Production Q&A

**Q: "Can I use `process.on('exit')` to save data to a file?"**
**A**: **No.** Saving to a file is an **asynchronous** operation. By the time the `exit` event fires, the event loop has stopped and libuv will not process any new file writes. You must do this in a signal handler or `beforeExit`.

---

## 🧪 Debugging Toolchain
- **`kill -l`**: List all available signals on your OS.
- **`docker kill --signal=SIGTERM <id>`**: Test your container's signal handling.

---

## 🏢 Industry Best Practices
- **Use an Init Process**: Always use `tini` in Docker to handle signals and reap zombies correctly.
- **Set a Timeout**: Never wait indefinitely for a graceful shutdown. If it takes > 30s, something is wrong; force the exit.

---

## 💼 Interview Questions
**Q: What is the difference between `SIGTERM` and `SIGKILL`?**
**A**: `SIGTERM` is a request to stop. The process can catch it and perform cleanup. `SIGKILL` is a command to the kernel to delete the process immediately. The process cannot catch or ignore `SIGKILL`.

---

## 🧩 Practice Problems
1. Write a script that spawns a child process and ensures that when the parent is killed, the child is also killed (preventing "Orphan" processes).
2. Create a Dockerfile for a Node.js app using `tini` and verify that `SIGTERM` is correctly received by the application.

---

**Prev:** [08_Diagnostics_Channel.md](./08_Diagnostics_Channel.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [../Networking/01_HTTP_Server_Internals.md](../Networking/01_HTTP_Server_Internals.md)
