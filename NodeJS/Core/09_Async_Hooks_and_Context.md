# 📌 09 — Async Hooks and Context: Tracking Async Lifecycles

## 🧠 Concept Explanation

### Basic → Intermediate
Async operations in Node.js are fragmented. When you make a database call and get a result in a callback, there is no built-in way to know which original HTTP request triggered that database call. `AsyncLocalStorage` provides a way to store data (like a Request ID) that follows the execution flow across async boundaries.

### Advanced → Expert
At the system level, this is built on top of **Async Hooks**. An Async Hook is a core API that provides callbacks for every stage of an "Async Resource" (a Timeout, a Promise, a Socket, etc.).
The lifecycle stages are:
1. `init`: Called when the resource is created.
2. `before`: Called just before the callback is executed.
3. `after`: Called just after the callback finishes.
4. `destroy`: Called when the resource is cleaned up.

---

## 🏗️ Common Mental Model
"AsyncLocalStorage is like a global variable."
**Correction**: It is more like **Thread-Local Storage (TLS)** in multi-threaded languages, but adapted for the single-threaded asynchronous nature of Node.js.

---

## ⚡ Actual Behavior: Context Propagation
When a new async resource is created (e.g. `fs.readFile`), Node.js captures the "current" context. When the callback for that file read is eventually executed, Node.js restores that captured context, making it available within the callback.

---

## 🔬 Internal Mechanics (V8 + libuv + syscalls)

### Execution Context vs Async Context
V8 manages the **Execution Context** (Stack). Node.js manages the **Async Context** (Async Hooks). 
Every time a callback is called from libuv, Node.js's C++ layer looks up the associated `asyncId` and triggers the `before` hooks.

### Performance Overhead
Using `AsyncHooks` directly has a significant performance cost (approx 10-20% drop in throughput) because it forces Node.js to track every single async handle and execute JS callbacks for every lifecycle event. `AsyncLocalStorage` is more optimized but still carries some overhead.

---

## 📐 ASCII Diagrams

### Context Propagation Flow
```text
  HTTP REQUEST (Req ID: 123)
     │
     ▼
  [ AsyncLocalStorage.run(123, ...) ]
     │
     ├─▶ DB.query() ──▶ [init Hook: capture 123]
     │                      │
     │                      ▼
     │              [ libuv waiting ]
     │                      │
     │                      ▼
     └─▶ Callback ◀─── [before Hook: restore 123]
           │
           ▼
        console.log(als.getStore()) // Outputs: 123
```

---

## 🔍 Code Example: Distributed Tracing with ALS
```javascript
const { AsyncLocalStorage } = require('async_hooks');
const { v4: uuid } = require('uuid');

const storage = new AsyncLocalStorage();

function log(msg) {
  const id = storage.getStore();
  console.log(`[Request ID: ${id || 'N/A'}] ${msg}`);
}

// Middleware simulation
function handleRequest(req) {
  const requestId = uuid();
  
  storage.run(requestId, () => {
    log('Starting work');
    
    // Even after a timeout, the ID is preserved
    setTimeout(() => {
      log('Work complete');
    }, 100);
  });
}

handleRequest();
```

---

## 💥 Production Failures & Debugging

### Scenario: The "Context Loss" Bug
**Problem**: Suddenly, all your logs show `Request ID: undefined` after a specific database call.
**Reason**: You are using a library (e.g. an old Redis client) that doesn't properly preserve the async context because it uses a custom internal pool or a non-standard callback mechanism.
**Debug**: Check if the library is compliant with `AsyncResource`.
**Fix**: Manually wrap the callback in `storage.bind()` or use `AsyncResource` to link the new task to the current ID.

---

## 🧪 Real-time Production Q&A

**Q: "Is it safe to use AsyncLocalStorage in production for high-volume apps?"**
**A**: **Yes, in Node 14.8+**. The performance impact was significantly reduced by moving much of the logic to C++. However, avoid storing large objects in the store; store only small primitives (IDs, metadata).

---

## 🧪 Debugging Toolchain
- **`node --trace-event-categories node.async_hooks`**: Generate a trace file that can be viewed in Chrome DevTools (`chrome://tracing`) to see the entire async dependency tree.

---

## 🏢 Industry Best Practices
- **Use ALS for Tracing**: It is the standard way to implement correlation IDs in microservices.
- **Don't use ALS for shared state**: Avoid using it as a way to pass variables between functions; use explicit arguments where possible to keep code readable.

---

## 💼 Interview Questions
**Q: How does `AsyncLocalStorage` differ from a regular global object?**
**A**: A global object is shared by all concurrent requests. `AsyncLocalStorage` provides a unique storage "bucket" per request flow, ensuring that concurrent requests don't leak data into each other.

---

## 🧩 Practice Problems
1. Implement a simple "Request Timer" using `async_hooks` that records the time between `init` and `destroy` for every network socket.
2. Create a logger that automatically appends the current user's ID to every log line without passing the user object through every function.

---

**Prev:** [08_Timers_Internals.md](./08_Timers_Internals.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [../Runtime/01_V8_Integration.md](../Runtime/01_V8_Integration.md)
