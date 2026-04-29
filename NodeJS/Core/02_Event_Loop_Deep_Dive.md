# 📌 02 — Event Loop Deep Dive: The Heart of libuv

## 🧠 Concept Explanation

### Basic → Intermediate
The Event Loop is a continuous loop that picks up finished tasks and puts them onto the call stack. It allows Node.js to be asynchronous and non-blocking.

### Advanced → Expert
The Node.js Event Loop is a **multi-phase state machine** implemented in C within **libuv**. It is fundamentally different from the browser's event loop (HTML5 spec). While the browser focuses on a "Task Queue" and "Microtask Queue," Node.js has dedicated phases for specific types of handles and requests.

Each phase has a **FIFO queue** of callbacks. The loop enters a phase, executes its queue until it's empty or the maximum number of callbacks is reached, and then moves to the next phase.

---

## 🏗️ Common Mental Model
"The Event Loop is a circle."
**Correction**: It is a **sequential list of phases**. Once the last phase is reached, if there are still active handles (servers, timers, etc.), it restarts from the first phase.

---

## ⚡ Actual Behavior: The 6 Phases
1. **Timers**: Executes callbacks from `setTimeout()` and `setInterval()`.
2. **Pending Callbacks**: Executes I/O callbacks deferred from the previous loop iteration (e.g., TCP errors).
3. **Idle, Prepare**: Used internally by libuv only.
4. **Poll**: Retrieve new I/O events. This is where Node.js will block if there's nothing else to do.
5. **Check**: Executes `setImmediate()` callbacks.
6. **Close Callbacks**: Executes callbacks for closed handles (e.g., `socket.on('close', ...)`).

---

## 🔬 Internal Mechanics (libuv + Microtasks)

### The Microtask "Checkpoints"
In Node.js, **Microtasks** (Promises and `process.nextTick()`) are **NOT** part of the libuv phases. Instead, they are handled by the Node.js layer. 
- `process.nextTick()` has the highest priority.
- Promises (Resolved/Rejected) come after `nextTick`.

**Critical Change (Node 11+)**: Microtasks are now executed **between** every individual callback in the timers and check phases, matching browser behavior for consistency.

---

## 🔁 Execution Flow (The "Tick" Walkthrough)
1. **Sync Code Execution**: Main script runs.
2. **NextTick Queue**: All `process.nextTick` callbacks are drained.
3. **Microtask Queue**: All resolved Promises are drained.
4. **Enter libuv Loop**:
    - **Timers Phase**: Check if any timers are expired.
    - (Drain NextTick/Microtasks)
    - **Pending Phase**: Check for deferred I/O.
    - **Poll Phase**: Wait for I/O events (epoll/kqueue).
    - **Check Phase**: Execute `setImmediate`.
    - (Drain NextTick/Microtasks)
    - **Close Phase**: Clean up resources.

---

## 📐 ASCII Diagrams

### Detailed Event Loop Phases
```text
   ┌───────────────────────────┐
   │      START (MAIN)         │
   └─────────────┬─────────────┘
                 ▼
   ┌───────────────────────────┐      ┌───────────────────────────┐
   │     process.nextTick()    │ ───▶ │   Promise Microtasks      │
   └─────────────┬─────────────┘      └─────────────┬─────────────┘
                 ▼                                  │
   ┌────────────────────────────────────────────────▼─────────────┐
   │                    LIBUV EVENT LOOP                          │
   │                                                              │
   │  ┌───────────────┐      ┌───────────────┐      ┌──────────┐  │
   │  │   1. TIMERS   │ ───▶ │  2. PENDING   │ ───▶ │ 3. IDLE  │  │
   │  └──────┬────────┘      └───────────────┘      └─────┬────┘  │
   │         │                                            │       │
   │         ▼                                            ▼       │
   │  ┌───────────────┐      ┌───────────────┐      ┌──────────┐  │
   │  │   6. CLOSE    │ ◀─── │   5. CHECK    │ ◀─── │ 4. POLL  │  │
   │  └───────────────┘      └───────────────┘      └──────────┘  │
   │                                                              │
   └──────────────────────────────────────────────────────────────┘
```

---

## 🔍 Code Example: The Order of Operations
```javascript
const fs = require('fs');

console.log('1. Start');

setTimeout(() => console.log('2. Timer (11ms)'), 11);
setTimeout(() => console.log('3. Timer (0ms)'), 0);

setImmediate(() => console.log('4. Immediate'));

fs.readFile(__filename, () => {
  console.log('5. File Read (I/O Callback)');
  
  // Inside I/O, setImmediate ALWAYS runs before setTimeout(0)
  setTimeout(() => console.log('6. Nested Timer'), 0);
  setImmediate(() => console.log('7. Nested Immediate'));
  
  process.nextTick(() => console.log('8. NextTick inside I/O'));
});

Promise.resolve().then(() => console.log('9. Promise'));
process.nextTick(() => console.log('10. NextTick'));

console.log('11. End');

// Predicted Output: 1, 11, 10, 9, 3, 4 (or 4, 3), 5, 8, 7, 6
```

---

## 💥 Production Failures & Debugging

### Scenario: Event Loop Starvation (The "Synchronous Loop")
**Problem**: A developer adds a CPU-intensive data processing loop directly in an Express handler.
```javascript
app.get('/compute', (req, res) => {
  let i = 0;
  while(i < 1e9) i++; // Blocks the Event Loop for 2 seconds
  res.send('Done');
});
```
**Impact**: For 2 seconds, the server cannot accept new TCP connections, cannot heartbeat to Redis/DB, and cannot handle any other user requests.
**Debug**: Use `perf_hooks` to measure loop lag.

---

## 🧪 Real-time Production Q&A

**Q: "We see random latency spikes of 50ms. Our p99 is bad, but average latency is fine. Is this GC?"**
**A**: Not necessarily. Check the **Poll Phase**. If you have timers set to exactly 50ms, Node.js might be blocking in the Poll phase waiting for I/O, only waking up when the timer expires. This is called "Timer Jitter." Use `--trace-event-categories node.async_hooks` to see if the event loop is idling too long.

---

## ⚠️ Edge Cases & Undefined Behaviors
- **setTimeout(0) vs setImmediate**: In the main script, the order is non-deterministic. It depends on how fast the process starts. If the process is fast, the loop starts and the timer isn't ready (so Immediate wins). If it's slow, the timer is already expired (so Timer wins).

---

## 🏢 Industry Best Practices
- **Never block the loop**: Use `Worker Threads` for CPU-bound tasks.
- **Prefer setImmediate over process.nextTick**: `nextTick` can starve I/O if called recursively. `setImmediate` always yields to the loop.

---

## 💼 Interview Questions
**Q: How does Node.js decide when to exit the process?**
**A**: Node.js maintains a counter of **active handles** (servers, open sockets) and **active requests** (pending I/O). The event loop continues as long as this count is non-zero. You can manually remove a handle from this count using `handle.unref()`.

---

## 🧩 Practice Problems
1. Implement a function that measures "Event Loop Lag" in milliseconds using only `setImmediate` and `Date.now()`.
2. Predict the output of a script where a `process.nextTick` calls itself recursively 100 times. Does it block a `setTimeout(0)`? (Spoiler: Yes).

---

**Prev:** [01_Node_Architecture.md](./01_Node_Architecture.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [03_Non_Blocking_IO.md](./03_Non_Blocking_IO.md)
