# 📌 05 — Error Handling: Boundary Crossing and Crash Safety

## 🧠 Concept Explanation

### Basic → Intermediate
Errors in Node.js are either **Operational** (expected failures like "File Not Found") or **Programmer Errors** (bugs like `undefined is not a function`).

### Advanced → Expert
At a staff level, we care about **Error Propagation across Async Boundaries**. When an error occurs in a callback or a promise, the original stack trace is often lost. 

In Node.js, an uncaught error in a callback will trigger the `uncaughtException` event. If unhandled, the process **must** be restarted because it is in an undefined state (e.g., a database connection might be leaked or memory corrupted).

---

## 🏗️ Common Mental Model
"I can wrap my whole server in a try-catch."
**Correction**: Synchronous `try-catch` **cannot catch errors in callbacks**. Each callback starts a new execution context on the Call Stack.

---

## ⚡ Actual Behavior: The Stack Trace Cost
Every time an `Error` object is created, V8 captures a **Stack Trace**. This is a heavy operation (`Error.captureStackTrace`). In high-throughput systems, creating thousands of errors per second (even if caught) can become a CPU bottleneck.

---

## 🔬 Internal Mechanics (V8 + libuv + syscalls)

### V8 Stack Trace API
V8's `Error.stack` is a getter that triggers a C++ formatting routine. You can control the depth using `Error.stackTraceLimit`.

### The Async Boundary problem
When an async function `await`s, the engine saves the stack. In Node.js 12+, **Async Stack Traces** were introduced. V8 now stitches together the "current" stack with the "saved" stack of the suspended function, providing a logical trace even across event loop ticks.

---

## 📐 ASCII Diagrams

### Error Propagation in Async Flow
```text
  1. Main Script Starts
     │
     ▼
  2. Call fs.readFile(..., callback)
     (Stack is empty after this)
     │
     ▼
  3. libuv processes I/O
     │
     ▼
  4. Callback is Pushed to Stack
     ┌──────────────────────┐
     │ callback() {         │
     │   throw new Error(); │ ──▶ 5. WHERE DOES THIS GO?
     │ }                    │      (Not to Main Script)
     └──────────────────────┘
```

---

## 🔍 Code Example: Staff-Level Error Handling
```javascript
const logger = require('./logger');

// Centralized Error Handling Pattern
class AppError extends Error {
  constructor(message, statusCode, isOperational = true) {
    super(message);
    this.statusCode = statusCode;
    this.isOperational = isOperational;
    Error.captureStackTrace(this, this.constructor);
  }
}

process.on('uncaughtException', (error) => {
  logger.error('CRITICAL: Uncaught Exception', error);
  // ALWAYS exit after uncaughtException to avoid undefined state
  process.exit(1);
});

process.on('unhandledRejection', (reason, promise) => {
  // Rejections are often operational (e.g. timeout)
  logger.warn('Unhandled Rejection at:', promise, 'reason:', reason);
});
```

---

## 💥 Production Failures & Debugging

### Scenario: The Silent Database Timeout
**Problem**: The application starts "hanging." Users get timeouts, but there are no errors in the logs.
**Reason**: A database call is wrapped in a Promise that doesn't have a `.catch()` block. The promise is rejected, but it is "swallowed" silently (before Node 15) or triggers an unhandled rejection that isn't logged.
**Debug**: Use `node --trace-rejections` to identify where promises are failing without handlers.

---

## 🧪 Real-time Production Q&A

**Q: "Should I always use `try-catch` inside async functions?"**
**A**: **Yes**, but only if you intend to *handle* the error. If you are just logging and re-throwing, it's often cleaner to let the error bubble up to a global error-handling middleware (like in Express).

**Q: "Is it safe to continue after an `uncaughtException`?"**
**A**: **No.** Node.js is a single-threaded state machine. If an error is uncaught, you might have left an `EventEmitter` with a listener that will never fire, or a `Mutex` that is now locked forever. Restart the process via a process manager like **PM2** or **Kubernetes**.

---

## ⚠️ Edge Cases & Undefined Behaviors
- **Errors in `process.nextTick`**: These behave like synchronous errors and will crash the process if not caught, bypassing the libuv phases entirely.

---

## 🏢 Industry Best Practices
- **Distinguish Operational vs Programmer Errors**: Only retry operational errors (e.g. network blips).
- **Graceful Shutdown**: On `SIGTERM` or `uncaughtException`, stop accepting new connections, finish pending requests, and then exit.

---

## 💼 Interview Questions
**Q: What is the difference between `throw` and `process.emit('error')`?**
**A**: `throw` is a language-level keyword for the call stack. `process.emit('error')` (and EventEmitters in general) is a pattern for asynchronous error notification. If an EventEmitter emits an `'error'` and has no listener, it will throw an exception that crashes the process.

---

## 🧩 Practice Problems
1. Create a script that "leaks" an unhandled rejection. Find a way to detect it using `async_hooks`.
2. Write a function that modifies `Error.prepareStackTrace` to return errors as JSON objects instead of strings.

---

**Prev:** [04_Callbacks_Promises_Async.md](./04_Callbacks_Promises_Async.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [06_Environment_and_Config.md](./06_Environment_and_Config.md)
