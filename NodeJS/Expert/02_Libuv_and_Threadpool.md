# 📌 Topic: Libuv and the Threadpool

## What
### 🧠 Concept Explanation
Libuv is the **Dispatcher** of the Node.js universe.
**Analogy:** 
- **The Main Thread:** The CEO who handles all decisions.
- **Asynchronous OS Calls (epoll/kqueue):** The CEO's smartphone. They can check thousands of emails (network sockets) at once without doing any work themselves.
- **The Threadpool (Libuv):** The CEO's 4 interns (Default size is 4). If the CEO needs to do something heavy that their phone can't do (like heavy math, crypto, or file compression), they hand it to an intern. If all 4 interns are busy, the next heavy task has to wait until an intern is free.

---

### 🏗️ Mental Model
Libuv provides two ways to do things asynchronously:
1.  **Native Async (Non-blocking):** Used for Networking. It leverages OS-level notification systems (like `epoll`). It does **not** use threads.
2.  **Threadpool (Blocking):** Used for File I/O, DNS, and some Crypto/Zlib tasks. It uses a fixed-size pool of background threads to handle blocking operations.

---

## Why
### 🏢 Best Practices
1.  **Increase `UV_THREADPOOL_SIZE`:** If you are doing heavy file I/O or crypto, set it to the number of logical cores on your server (up to 128).
2.  **Use `dns.resolve()` instead of `dns.lookup()`:** `resolve` uses networking (native async) and doesn't block the threadpool.
3.  **Offload to Worker Threads:** For truly heavy CPU work that isn't handled by Libuv (like JSON parsing or complex logic), use Worker Threads instead.

---

### ⚖️ Trade-offs
*   **Native Async:** Zero thread overhead, highly scalable, but only works for certain types of I/O (Networking).
*   **Threadpool:** Simple and robust, but limited by a fixed number of workers.

---

## How
### ⚡ Actual Behavior
*   **Default Threads:** Libuv has 4 background threads by default.
*   **CPU-Bound Blocking:** If you have 10 files to read, and the threadpool is size 4, the first 4 will start immediately, and the next 6 will wait.
*   **Networking is special:** Networking does NOT use the threadpool. You can have 10,000 open sockets and only 4 threads, and they won't interfere with each other.

---

### 🔬 Internal Mechanics (V8 + libuv + OS)
*   **uv_loop_t:** The main struct that represents the event loop.
*   **uv_work_t:** The request structure for offloading tasks to the threadpool.
*   **Internal Queue:** Libuv maintains a queue of tasks. When a thread in the pool is idle, it pulls the next task from the queue.

---

### 🔁 Execution Flow
1.  Node.js calls `crypto.pbkdf2()`.
2.  A `uv_work_t` request is created.
3.  The request is pushed to the threadpool queue.
4.  One of the 4 libuv threads picks up the work.
5.  Thread completes work and signals the main loop.
6.  The main loop executes the callback in the next tick.

---

### 🔍 Code Example (Latest Node.js - Testing Pool Size)
```javascript
import crypto from 'node:crypto';
import { performance } from 'node:perf_hooks';

// Default threadpool is 4. Running 5 heavy crypto tasks will show a bottleneck.
// Try changing this: process.env.UV_THREADPOOL_SIZE = 8;
const start = performance.now();

for (let i = 0; i < 5; i++) {
  crypto.pbkdf2('pass', 'salt', 100000, 64, 'sha512', () => {
    console.log(`Task ${i+1} done at ${Math.round(performance.now() - start)}ms`);
  });
}

/*
Typical Output (Default size 4):
Task 1 done at 100ms
Task 2 done at 102ms
Task 3 done at 105ms
Task 4 done at 110ms
Task 5 done at 205ms  <-- Notice the jump! It had to wait for T1-T4 to finish.
*/
```

---

## Impact
### 💥 Production Failures
*   **Threadpool Starvation:** Doing too many `fs.readFile` or `crypto` operations at once, causing other critical tasks (like DNS lookups) to hang.
*   **Blocking DNS:** Node's `dns.lookup()` uses the threadpool. If the pool is full, your app won't be able to resolve any new domain names (like for a DB or an external API).

---

### 🧪 Real-time Scenarios
*   **Image Upload Server:** Processing many images simultaneously using `sharp` (which uses the threadpool).
*   **Encryption Service:** A service that generates thousands of secure tokens using `crypto`.

---

### ⚠️ Edge Cases
*   **Changing Pool Size:** `UV_THREADPOOL_SIZE` must be set **before** the first call to an asynchronous function. Setting it halfway through your script has no effect.
*   **Maximum Size:** The limit is 1024 threads, but setting it that high is usually a bad idea due to OS overhead.

---

---

Prev: [01_V8_Engine_Internals.md](./01_V8_Engine_Internals.md) | Index: [NodeJS/00_Index.md](../00_Index.md) | Next: [03_Garbage_Collection.md](./03_Garbage_Collection.md)
