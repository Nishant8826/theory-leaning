# 📌 04 — Callbacks, Promises, and Async/Await: The Microtask Mechanics

## 🧠 Concept Explanation

### Basic → Intermediate
JavaScript evolved from simple callbacks to Promises, and finally to Async/Await. All three patterns are used to handle asynchronous code, but they differ in how they are managed by the engine.

### Advanced → Expert
The distinction between **Macrotasks** (libuv tasks) and **Microtasks** (V8 tasks) is the most critical concept for high-performance Node.js. 

- **Callbacks**: Usually scheduled via libuv (Timers, I/O). They are Macrotasks.
- **Promises**: Handled by the V8 engine directly. They are Microtasks.
- **Async/Await**: Syntactic sugar for Generators + Promises. 

When a promise is resolved, its `.then()` callback is pushed to the **Microtask Queue**. This queue is processed **immediately** after the current synchronous execution and **before** the next libuv phase.

---

## 🏗️ Common Mental Model
"Async/Await makes code synchronous."
**Correction**: It makes the **syntax** look synchronous, but internally it **suspends** function execution, returns control to the event loop, and resumes once the awaited promise settles.

---

## ⚡ Actual Behavior: Task Interleaving
If you have a loop that resolves promises recursively, you can **starve** the Event Loop. Because Node.js (since v11) drains the entire microtask queue between every macrotask, a flood of promises will prevent the Timers and Poll phases from ever running.

---

## 🔬 Internal Mechanics (V8 + libuv + syscalls)

### V8 Promise Internals
A Promise in V8 is a `JSPromise` object. 
1. `pending`: The initial state.
2. `fulfilled`: Resolved.
3. `rejected`: Failed.

When `resolve()` is called, V8 creates a **PromiseReactionJob** and places it in the `MicrotaskQueue`.

### Async/Await Transformation
The V8 compiler transforms `async` functions into a state machine using **Generators**. An `await` is essentially a `yield`. The engine saves the local variables to the heap, exits the function, and uses the Promise's `.then()` to trigger the function's resumption.

---

## 📐 ASCII Diagrams

### Microtask vs Macrotask Priority
```text
  ┌───────────────────────────────────────────┐
  │         CALL STACK (Synchronous)          │
  └─────────────────────┬─────────────────────┘
                        │
                        ▼
  ┌───────────────────────────────────────────┐
  │           MICROTASK QUEUE (V8)            │ ◀─── Promises, process.nextTick
  │  (Executes until COMPLETELY empty)        │
  └─────────────────────┬─────────────────────┘
                        │
                        ▼
  ┌───────────────────────────────────────────┐
  │          MACROTASK QUEUE (libuv)          │ ◀─── setTimeout, I/O, setImmediate
  │  (Executes ONE task per iteration)        │
  └───────────────────────────────────────────┘
```

---

## 🔍 Code Example: The "Awaited" Execution
```javascript
async function staffLevelAsync() {
  console.log('1. Inside Async');
  
  // Every await creates a new Microtask
  await Promise.resolve(); 
  console.log('2. After first await');
  
  await Promise.resolve();
  console.log('3. After second await');
}

console.log('4. Start');
staffLevelAsync();
console.log('5. End');

// Order: 4 (Start) ──▶ 1 (Inside Async) ──▶ 5 (End) ──▶ 2 (Microtask 1) ──▶ 3 (Microtask 2)
```

---

## 💥 Production Failures & Debugging

### Scenario: Microtask Starvation
**Problem**: A developer uses a recursive Promise chain to process a massive dataset.
```javascript
function processData(i) {
  if (i > 1e6) return;
  Promise.resolve().then(() => {
    // Heavy work here...
    processData(i + 1); // Schedules a new Microtask
  });
}
```
**Impact**: The server stops responding to HTTP requests (`epoll` events are in the Macrotask queue). The process is busy emptying the Microtask queue that never ends.
**Fix**: Use `setImmediate` to move the next iteration to the Macrotask queue, allowing I/O to be processed.

---

## 🧪 Real-time Production Q&A

**Q: "I have an async function that does heavy math before the first `await`. Does it block?"**
**A**: **Yes.** The code in an `async` function runs synchronously **until it hits the first `await`**. If you have a `while(true)` before the first `await`, the event loop is blocked and the function never even returns the initial Promise to the caller.

---

## 🧪 Debugging Toolchain
- **`node --trace-warnings`**: Tracks unhandled promise rejections.
- **`async_hooks`**: Monitor the creation and resolution of every async resource.

---

## 🏢 Industry Best Practices
- **Never "fire and forget" Promises**: Always `await` or `.catch()` them. Unhandled rejections can crash the process in modern Node.js versions.
- **Avoid `process.nextTick`**: Unless you explicitly need to execute something *before* the next Microtask. It is almost always better to use `queueMicrotask` or `setImmediate`.

---

## 💼 Interview Questions
**Q: What is the difference between `await Promise.all()` and multiple sequential `await`s?**
**A**: Multiple sequential `await`s create a **Waterfall**. Each waits for the previous to finish. `Promise.all` executes the requests in **parallel** (at the libuv/OS level) and waits for the aggregation, significantly reducing total latency.

---

## 🧩 Practice Problems
1. Write a script that proves `process.nextTick` runs before `Promise.then`.
2. Refactor a callback-heavy code snippet into `async/await`. Explain the V8 memory impact of the transformation (Closure creation).

---

**Prev:** [03_Non_Blocking_IO.md](./03_Non_Blocking_IO.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [05_Error_Handling.md](./05_Error_Handling.md)
