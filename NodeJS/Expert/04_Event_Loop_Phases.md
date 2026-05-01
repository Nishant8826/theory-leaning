# 📌 Topic: Event Loop Phases (Internal)

## What
### 🧠 Concept Explanation
If the Event Loop is a clock, the Phases are the **Ticks of the Second Hand**.
**Analogy:** Imagine a security guard patrolling a building. He follows a strict path:
1.  **Check the Timers:** Does anyone have an alarm set?
2.  **Check the Front Desk:** Are there any messages from the OS about networking or errors?
3.  **Check the Lobby:** Are there any new visitors (I/O) waiting to be processed?
4.  **Check the Security Desk:** Are there any "immediate" tasks waiting?
5.  **Check the Exit:** Is anyone leaving (socket close)?
He repeats this loop over and over, and he **must** finish one area before moving to the next.

---

### 🏗️ Mental Model
The Event Loop in Node.js (implemented by Libuv) consists of 7 distinct phases. Each phase has its own queue of callbacks. The loop moves through these phases sequentially.

---

## Why
### 🏢 Best Practices
1.  **Monitor Tick Frequency:** Use `perf_hooks` to measure the duration of each phase.
2.  **Avoid blocking in Poll:** Keep your I/O callbacks short.
3.  **Use `setImmediate` for cleanup:** To ensure it happens after I/O but before the next set of timers.

---

### ⚖️ Trade-offs
*   **Event Loop:** Efficiently handles I/O but vulnerable to CPU-bound blocking in any single phase.

---

## How
### ⚡ Actual Behavior
1.  **Timers:** Handles `setTimeout` and `setInterval`.
2.  **Pending Callbacks:** Executes I/O callbacks deferred from the previous loop (rarely used, mostly system errors).
3.  **Idle, Prepare:** Internal only.
4.  **Poll:** The most critical phase. Retrieves new I/O events.
5.  **Check:** Executes `setImmediate` callbacks.
6.  **Close Callbacks:** Executes close events (e.g., `socket.on('close', ...)`).

---

### 🔬 Internal Mechanics (V8 + libuv + OS)
*   **uv_run:** The C function that orchestrates the loop.
*   **The Poll Timeout:** If the event loop has nothing to do, it will "hang" in the Poll phase for a specific amount of time, waiting for I/O, rather than spinning the CPU at 100%.
*   **I/O Completion Ports:** On Windows, Libuv uses IOCP; on Linux, it uses `epoll` to wait for I/O events in the Poll phase.

---

### 🔁 Execution Flow
```text
1. Update loop 'now' time.
2. Are there any timers ready? (Timer Phase)
3. Run Pending I/O.
4. Run Idle/Prepare.
5. Calculate Poll Timeout and BLOCK. (Poll Phase)
6. Run Check. (setImmediate Phase)
7. Run Close.
8. Check if loop is 'alive' (any active handles/requests?). If yes, repeat.
```

---

### 🔍 Code Example (Latest Node.js - Phase Behavior)
```javascript
import fs from 'node:fs';

// Inside an I/O callback, setImmediate ALWAYS runs before setTimeout(0)
fs.readFile(__filename, () => {
    console.log('--- Inside I/O ---');

    setTimeout(() => {
        console.log('setTimeout');
    }, 0);

    setImmediate(() => {
        console.log('setImmediate');
    });
});

/*
EXPLANATION:
1. Poll phase finishes reading the file and runs the callback.
2. Next phase in the loop is 'Check' (setImmediate).
3. The loop then finishes and starts over, hitting the 'Timer' phase (setTimeout).
Output:
--- Inside I/O ---
setImmediate
setTimeout
*/
```

---

## Impact
### 💥 Production Failures
*   **Poll Phase Starvation:** A high volume of small I/O events that keeps the loop in the Poll phase forever, preventing Timers from ever firing.
*   **Infinite `nextTick`:** Remember, `process.nextTick` is NOT part of libuv; it's Node-specific and drains between *every* phase. It can starve the entire loop.

---

### 🧪 Real-time Scenarios
*   **Real-time Gaming:** Ensuring the loop stays under 16ms (60fps) to maintain smooth state updates.
*   **High-Frequency Logging:** Using `setImmediate` to batch logs so they are written in the Check phase rather than interrupting the main Poll logic.

---

### ⚠️ Edge Cases
*   **Empty Loop:** If there are no active timers, sockets, or file handles, the loop exits and the Node.js process ends.
*   **Ref vs Unref:** `timer.unref()` tells the loop: "Don't keep the process alive just for this timer."

---

---

Prev: [03_Garbage_Collection.md](./03_Garbage_Collection.md) | Index: [NodeJS/00_Index.md](../00_Index.md) | Next: [05_Memory_Leaks_Debugging.md](./05_Memory_Leaks_Debugging.md)
