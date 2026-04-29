# 📌 02 — libuv Thread Pool Customization: Offloading the Work

## 🧠 Concept Explanation

### Basic → Intermediate
Node.js uses a "Thread Pool" provided by libuv to handle tasks that are blocking or expensive to perform on the main event loop (e.g. file I/O, DNS lookups, and certain cryptographic functions).

### Advanced → Expert
At a staff level, we must understand the **Limited Capacity** of this pool. 
By default, the libuv thread pool has only **4 threads**. These threads are shared across the entire Node.js process. If you have 4 threads busy calculating `bcrypt` hashes, a call to `fs.readFile()` will be queued and will not even start until one of the bcrypt hashes finishes.

You can increase the size of this pool using the `UV_THREADPOOL_SIZE` environment variable (up to 1024).

---

## 🏗️ Common Mental Model
"Everything asynchronous uses the thread pool."
**Correction**: **Network I/O** (HTTP, TCP, UDP) does **NOT** use the thread pool. It uses non-blocking OS primitives like `epoll` or `kqueue`. The thread pool is mainly for:
- `fs.*` (File system tasks)
- `dns.lookup()`
- `crypto.*` (pbkdf2, scrypt, etc.)
- `zlib.*` (Compression)

---

## ⚡ Actual Behavior: Thread Starvation
If you have a high-traffic app performing many file reads, the 4 default threads will become a bottleneck. This is called **Thread Pool Starvation**. Even if your CPU is only at 20%, your I/O requests will have high latency because they are stuck in the libuv queue.

---

## 🔬 Internal Mechanics (libuv)

### The Work Request (uv_work_t)
When a thread-pool-bound function is called:
1. Node.js creates a `uv_work_t` request.
2. The request is added to a global **Work Queue**.
3. One of the 4 idle threads picks up the request and executes the C++ code.
4. Once finished, the thread notifies the Event Loop to execute the JS callback.

---

## 📐 ASCII Diagrams

### libuv Thread Pool Queue
```text
  EVENT LOOP ──▶ [ WORK QUEUE ]
                       │
       ┌───────────────┼───────────────┬───────────────┐
       ▼               ▼               ▼               ▼
  [ THREAD 1 ]    [ THREAD 2 ]    [ THREAD 3 ]    [ THREAD 4 ]
  (Crypto)        (File I/O)      (Idle)          (DNS)
```

---

## 🔍 Code Example: Detecting Starvation
```javascript
const crypto = require('crypto');
const fs = require('fs');

const start = Date.now();

// Task 1: 4 Cryptographic operations (fills the pool)
for (let i = 0; i < 4; i++) {
  crypto.pbkdf2('pass', 'salt', 100000, 512, 'sha512', () => {
    console.log(`Crypto ${i} done: ${Date.now() - start}ms`);
  });
}

// Task 2: A simple file read (Stuck behind crypto)
fs.readFile(__filename, () => {
  console.log(`File read done: ${Date.now() - start}ms`);
});

// Result: All 5 tasks finish at almost the same time (approx 1s)
// even though the file read should only take 5ms.
```

---

## 💥 Production Failures & Debugging

### Scenario: The DNS Latency Spike
**Problem**: During a traffic burst, outgoing API calls to other services become very slow.
**Reason**: You are using `dns.lookup()` (the default). It uses the thread pool. If the pool is full of file I/O or crypto, DNS lookups are queued.
**Fix**: Increase `UV_THREADPOOL_SIZE=64` or use `dns.resolve()`, which does not use the thread pool.

### Scenario: The Cryptographic Bottleneck
**Problem**: You are using `bcrypt` to hash passwords. Login takes 1 second per user. If 10 users log in at once, the 10th user takes 3 seconds.
**Reason**: Bcrypt is using all 4 threads. The 5th to 10th users are waiting in the queue.
**Fix**: Increase the thread pool size to match the number of CPU cores, or use **Worker Threads** to handle bcrypt manually.

---

## 🧪 Real-time Production Q&A

**Q: "Should I set `UV_THREADPOOL_SIZE` to 1024?"**
**A**: **No.** Each thread has overhead (memory and context switching). Setting it too high can actually slow down the process. A good rule of thumb is to set it to **16 or 32** for most I/O-heavy applications.

---

## 🏢 Industry Best Practices
- **Set the variable at startup**: `UV_THREADPOOL_SIZE` must be set **before** the Node.js process starts (or at the very beginning of the main script before any I/O is performed).
- **Monitor I/O Latency**: If `fs` operations are slower than expected, check the thread pool usage.

---

## 💼 Interview Questions
**Q: Does `http.get()` use the libuv thread pool?**
**A**: **No.** It uses non-blocking sockets and the OS-level `epoll/kqueue` mechanism. The only part of an HTTP request that *might* use the thread pool is the **DNS resolution** if it uses `dns.lookup()`.

---

## 🧩 Practice Problems
1. Run the "Detecting Starvation" code example with `UV_THREADPOOL_SIZE=1` and then with `UV_THREADPOOL_SIZE=8`. Compare the timings.
2. Identify every core Node.js API that uses the libuv thread pool by reading the Node.js source code or documentation.

---

**Prev:** [01_V8_Ignition_TurboFan.md](./01_V8_Ignition_TurboFan.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [03_Memory_Layout_Smi_Doubles_Elements.md](./03_Memory_Layout_Smi_Doubles_Elements.md)
