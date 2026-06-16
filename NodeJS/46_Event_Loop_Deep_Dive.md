# Event Loop Deep Dive

While the basic Event Loop model explains simple async operations, complex production applications (like websockets clusters or real-time trading engines) require a precise understanding of execution scheduling. Failing to understand how the loop transitions between I/O poll, timers, and check phases can lead to race conditions, microtask starvation, and performance bottlenecks.

### The Six Phases of the Libuv Event Loop
The Libuv event loop iterates over six distinct phases in a continuous cycle (a "Tick"):

```text
    ┌───────────────────────────┐
    │          START            │
    └─────────────┬─────────────┘
                  ▼
    ┌───────────────────────────┐
    │          Timers           │ <-- setTimeout() & setInterval()
    └─────────────┬─────────────┘
                  ▼
    ┌───────────────────────────┐
    │     Pending Callbacks     │ <-- TCP errors (like ECONNREFUSED)
    └─────────────┬─────────────┘
                  ▼
    ┌───────────────────────────┐
    │       Idle, Prepare       │ <-- Internal libuv optimization (skip)
    └─────────────┬─────────────┘
                  ▼
    ┌───────────────────────────┐
    │           Poll            │ <-- Fetch new I/O events; blocks if idle
    └─────────────┬─────────────┘
                  ▼
    ┌───────────────────────────┐
    │           Check           │ <-- setImmediate() callbacks
    └─────────────┬─────────────┘
                  ▼
    ┌───────────────────────────┐
    │      Close Callbacks      │ <-- socket.on('close', ...)
    └─────────────┬─────────────┘
                  ▼
    ┌───────────────────────────┐
    │   Check for active refs   │ ──(No refs?)──> [ Stop / Exit ]
    └─────────────┬─────────────┘
                  │ (Yes: Loop again)
                  └───────────────────────────────────────┐
                                                          ▼
                                                   [ Next Tick ]
```

1. **Timers**: Executes callbacks scheduled by `setTimeout` and `setInterval` whose threshold has passed.
2. **Pending Callbacks**: Executes I/O callbacks deferred from the previous loop iteration (e.g. system TCP socket errors).
3. **Idle, Prepare**: Used internally by Libuv for system operations.
4. **Poll**: Retrieves new I/O events (network connections, database queries, file inputs). If there are no immediate timers, the loop will block here to wait for incoming I/O events.
5. **Check**: Executes callbacks scheduled by `setImmediate()`.
6. **Close Callbacks**: Executes close events (e.g., `socket.on('close')`).

### Microtask Starvation
Microtasks (`process.nextTick` and resolved Promises) execute **immediately after the current phase operation finishes**, before the loop transitions to the next phase. If you continuously add callbacks to the microtask queue (especially `process.nextTick`), the Event Loop will remain stuck in the microtask phase forever. This prevents the loop from moving to the poll or timers phase, starving all other I/O operations and freezing the server.

## Deep Dive

### Deterministic Scheduling: `setTimeout(..., 0)` vs. `setImmediate()`
* **Main Script Execution**: When called in the main script, the execution order of `setTimeout(..., 0)` and `setImmediate()` is non-deterministic. If V8 bootstrap takes less than 1ms, the loop enters the Timers phase before the timeout timer has finished registering, executing `setImmediate` first. If it takes longer, `setTimeout` executes first.
* **Inside an I/O Cycle**: When called inside an I/O callback (such as `fs.readFile`), `setImmediate` **always** executes first. This is because the I/O callback runs in the Poll phase. Once the Poll phase completes, the loop transitions directly to the Check phase where `setImmediate` is scheduled, before wrapping around to the Timers phase in the next tick.

## Visual Explanation

### Microtask Queue Execution Boundaries
```text
Phase: Timers (setTimeout) ──> Executes Macrotask 1
                                       │
                                       ▼ (Call Stack clears)
                       [ DRAIN NEXTTICK QUEUE ]
                                       │
                                       ▼ (Empty?)
                       [ DRAIN PROMISE QUEUE ]
                                       │
                                       ▼ (Empty?)
Phase: Pending Callbacks ──> Executes Macrotask 2 ...
```

## Real-World Example
Consider an Express server that needs to process a large array of records without blocking user HTTP requests. Instead of processing the entire array in a single synchronous loop (which blocks the event loop), you can write a recursive helper that processes the array in small chunks, using `setImmediate()` to schedule the next chunk. This allows the event loop to run Poll and check phases between chunks, keeping the server responsive.

## Code Examples

### Tracing Execution Order inside an I/O Callback

```javascript
// event-loop-deep.js
const fs = require('fs');

console.log('1. Main Script Start');

// 1. Non-deterministic when run in the global scope
setTimeout(() => {
  console.log('TIMERS: setTimeout (Global Scope)');
}, 0);

setImmediate(() => {
  console.log('CHECK: setImmediate (Global Scope)');
});

// 2. Deterministic order when run inside an I/O callback
fs.readFile(__filename, () => {
  console.log('\n--- Entered I/O Callback (Poll Phase) ---');

  setTimeout(() => {
    // Executes in the next loop iteration (Timers Phase)
    console.log('TIMERS: setTimeout (Inside I/O)');
  }, 0);

  setImmediate(() => {
    // Executes in the current loop iteration (Check Phase - runs immediately after Poll)
    console.log('CHECK: setImmediate (Inside I/O)');
  });

  process.nextTick(() => {
    console.log('MICROTASK: process.nextTick (Inside I/O)');
  });

  Promise.resolve().then(() => {
    console.log('MICROTASK: Promise.then (Inside I/O)');
  });
});

console.log('2. Main Script End');
```

## Best Practices
* **Use `setImmediate` over `process.nextTick`**: Use `setImmediate()` to yield execution to the event loop. It executes in the Check phase and does not risk starving the event loop.
* **Avoid recursive nextTicks**: Never call `process.nextTick` recursively, as it starves the event loop of timers and I/O.
* **Break Up CPU Tasks**: Use `setImmediate` to break up heavy computational loops into smaller, asynchronous steps, allowing the event loop to process other client requests in between.

## Interview Questions

**Q:** What are the key phases of the Event Loop?

> **Answer:**
> The key phases of the Libuv event loop are: **Timers** (handles timeouts), **Pending Callbacks** (handles I/O errors), **Poll** (retrieves new I/O events), **Check** (handles `setImmediate` callbacks), and **Close Callbacks** (handles resource closures).

**Q:** Why does `setImmediate` always execute before `setTimeout(..., 0)` when called inside an I/O callback?

> **Answer:**
> I/O callbacks are processed in the **Poll phase** of the event loop. Once the Poll phase completes, the event loop transitions directly to the **Check phase** (where `setImmediate` callbacks are run) before wrapping around to the **Timers phase** (where `setTimeout` runs) in the next tick. Therefore, `setImmediate` always runs first.

**Q:** What is microtask starvation and how can it impact a high-concurrency Node.js application?

> **Answer:**
> Microtask starvation occurs when recursive or high-volume callbacks are continuously added to the microtask queue (e.g. `process.nextTick` or Promise chains). Because V8 drains the entire microtask queue before transitioning to the next phase of the event loop, the loop remains stuck in the microtask phase, starvation-blocking I/O events, timers, and connections. This causes API endpoints to hang and timeouts to occur.

**Q:** How would you debug a production Node.js process that is experiencing event loop delay (event loop blocking)? Discuss tools, performance metrics, and application code mitigations.

> **Answer:**
> 

**Q:** Detection Tools

> **Answer:**
> 1. Use the native `perf_hooks` module to measure loop delay: `monitorEventLoopDelay()`.
> 2. Collect CPU profiles using Node's diagnostic flags (`node --prof` or `--inspect`) to identify long-running synchronous functions.

**Q:** Key Metrics

> **Answer:**
> 

**Q:** Loop Delay

> **Answer:**
> 

**Q:** CPU Utilization

> **Answer:**
> 

**Q:** Code Mitigations

> **Answer:**
> - Offload heavy calculations to **Worker Threads** or background service queues.
> - Rewrite blocking synchronous calls (like `fs.readFileSync` or heavy JSON parsing) to use asynchronous equivalents.
> - Split large loops into chunks using `setImmediate` to yield execution back to the loop between iterations.

---
Previous : [20_Async_Await.md](20_Async_Await.md) | Index : [00_index.md](00_index.md) | Next : [47_Streams_Deep_Dive.md](47_Streams_Deep_Dive.md)
