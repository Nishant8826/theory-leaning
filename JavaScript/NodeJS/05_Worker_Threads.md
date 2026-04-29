# 📌 05 — Worker Threads

## 🌟 Introduction

In the **Cluster Module**, we created separate *processes* to use more CPU cores. But processes are heavy and don't share memory.

**Worker Threads** allow you to run multiple threads within the **same process**. They are much lighter and can share memory efficiently.

Think of it like a **Chef's Assistant**:
-   **Cluster:** You open 4 separate restaurants. They don't share a pantry.
-   **Worker Threads:** You have 1 restaurant, but you hire 4 assistants to work in the same kitchen. They all share the same pantry (Memory).

---

## 🏗️ When to Use Worker Threads?

You should use Worker Threads for **CPU-Intensive tasks** that would normally freeze your server:
1.  **Image Processing:** Resizing or applying filters.
2.  **Encryption/Decryption:** Hashing passwords or generating keys.
3.  **Complex Math:** Calculating high-level statistics or physics.
4.  **Parsing:** Processing a massive 500MB JSON or CSV file.

---

## 🚀 Worker Threads vs. Cluster

| Feature | Cluster | Worker Threads |
| :--- | :--- | :--- |
| **Process** | Multiple separate processes. | One process, multiple threads. |
| **Memory** | Isolated (No sharing). | Can share memory (`SharedArrayBuffer`). |
| **Startup** | Slow (Heavy). | Fast (Lightweight). |
| **Use Case** | Scaling Web Servers (I/O). | Heavy Computation (CPU). |

---

## 🔍 Code Walkthrough: Heavy Math Worker

```javascript
// main.js
const { Worker } = require('worker_threads');

function runHeavyTask(n) {
  return new Promise((resolve, reject) => {
    // Create a new worker thread
    const worker = new Worker('./worker.js', { workerData: n });

    worker.on('message', resolve); // Get the result
    worker.on('error', reject);
    worker.on('exit', (code) => {
      if (code !== 0) reject(new Error(`Worker stopped with code ${code}`));
    });
  });
}

runHeavyTask(40).then(result => console.log(`Result: ${result}`));
console.log("I'm not blocked! I can still handle other tasks.");

// worker.js
const { parentPort, workerData } = require('worker_threads');

// A heavy function that would normally freeze the server
function slowFibonacci(n) {
  if (n <= 1) return n;
  return slowFibonacci(n - 1) + slowFibonacci(n - 2);
}

const result = slowFibonacci(workerData);
parentPort.postMessage(result); // Send result back to main thread
```

---

## 🏗️ Shared Memory (SharedArrayBuffer)

This is the "Superpower" of Worker Threads. They can both look at the exact same piece of memory at the same time. This means you can pass 100MB of data between threads **instantly** without copying it.

---

## 📐 Visualizing the Thread Model

```text
[   MAIN THREAD   ] (Handles HTTP, DB, UI)
        │
        ├─▶ [ Worker Thread 1 ] (Math/Hashing)
        ├─▶ [ Worker Thread 2 ] (Image Filtering)
        └─▶ [ Worker Thread 3 ] (JSON Parsing)
```

---

## 🔬 Deep Technical Dive (V8 Internals)

### Isolate Isolation
Even though they are in the same process, each Worker Thread runs in its own **V8 Isolate**. This means they have their own call stack and their own garbage collector. They only share memory if you explicitly tell them to using a `SharedArrayBuffer`. This keeps them safe—one worker crashing won't necessarily corrupt the variables of the main thread.

---

## 💼 Interview Questions

**Q1: Why not just use `setTimeout` for heavy tasks?**
> **Ans:** `setTimeout` only delays a task; it still runs on the **Main Thread**. If the task takes 5 seconds of CPU time, it will freeze your server for 5 seconds. Worker Threads move the task to a **different thread** entirely.

**Q2: What is a `SharedArrayBuffer`?**
> **Ans:** It is a special type of memory that can be accessed by multiple threads at the same time. It allows for "Zero-Copy" communication, meaning you don't waste time copying data back and forth between threads.

**Q3: Can a Worker Thread touch the `process` object?**
> **Ans:** Yes, but some parts of it are limited. They cannot change things like the current working directory or environment variables that would affect other threads.

---

## ⚖️ Trade-offs

| Method | Benefit | Cost |
| :--- | :--- | :--- |
| **Main Thread** | No overhead; easy to write. | Freezes on heavy math. |
| **Worker Threads** | Keeps server responsive; fast sharing. | Higher complexity; thread management overhead. |
| **Child Process** | Total isolation (cannot crash main). | Very slow communication; high memory usage. |

---

## 🔗 Navigation

**Prev:** [04_Cluster_Module.md](04_Cluster_Module.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [06_Middleware_Design.md](06_Middleware_Design.md)
