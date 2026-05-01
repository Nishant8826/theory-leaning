# 📌 Topic: Event Loop Deep Dive (Microtasks vs Macrotasks)

## 🧠 Concept Explanation
While the basic Event Loop manages the flow of tasks, the "Deep Dive" involves understanding **Priority**. Not all tasks are created equal in the eyes of Node.js.

**The Hospital Triage Analogy (Deep Dive):**
Imagine a Hospital Emergency Room (The Event Loop).
*   **Macrotasks (Task Queue):** These are normal patients (setTimeout, I/O). They wait in the general waiting room and are seen in the order they arrived (per phase).
*   **Microtasks (Promise Queue):** These are "Critical Condition" patients who just arrived by ambulance (Promises). 
*   **NextTick (The Emergency Lane):** This is a patient who is already on the operating table and needs an immediate blood transfusion (`process.nextTick`).

**The Rule:** The doctor (The Main Thread) will **never** go back to the general waiting room (Macrotasks) until the operating table is clear AND all critical ambulance patients (Microtasks) have been stabilized. If new ambulances keep arriving, the people in the waiting room will wait forever (Starvation).

---

## 🏗️ Mental Model
The Event Loop is a series of "Phases," but between every single phase—and even after every single callback within those phases—Node.js checks the **Microtask Queue**. 

1.  **Macro-Step:** Finish one callback from a phase (e.g., one Timer).
2.  **Micro-Step:** Immediately drain the *entire* Microtask queue (Promises).
3.  **Next-Macro:** Move to the next callback or phase.

This is why Promises often feel "faster" than `setTimeout`—they literally cut in line.

---

## ⚡ Actual Behavior
The sequence of execution follows a very strict hierarchy:

1.  **Synchronous Code:** The code you wrote that isn't in a callback. It runs until the stack is empty.
2.  **`process.nextTick` Queue:** Drained immediately after the current operation. This is the "fastest" way to run code asynchronously.
3.  **Microtask Queue (Promises):** Drained immediately after the `nextTick` queue.
4.  **The Event Loop (Macrotasks):**
    *   **Timers:** `setTimeout` / `setInterval`.
    *   **Pending Callbacks:** System-level I/O errors.
    *   **Poll Phase:** New I/O, FS, HTTP.
    *   **Check Phase:** `setImmediate`.
    *   **Close Phase:** Socket closures.

*Note: After every single Macrotask in any phase, the Event Loop checks the Microtask queue again.*

---

## 🔬 Internal Mechanics (V8 + libuv + OS)
*   **V8's Role:** Microtasks (Promises) are actually managed by the **V8 Engine**, not by Libuv. V8 has its own internal queue for these.
*   **Libuv's Role:** Libuv manages the Macrotask phases (Timers, I/O, etc.) and handles the communication with the OS.
*   **The "Tick" Boundary:** The transition between "JavaScript execution" and "Event Loop Phase" is where the most Microtask processing happens.
*   **NextTick Implementation:** `process.nextTick` is a Node.js-specific optimization. It bypasses the V8 Microtask queue and uses a dedicated internal array for speed. This is why it always beats Promises.

---

## 🔁 Execution Flow
```javascript
import fs from 'node:fs';

setTimeout(() => console.log('Timer 1'), 0);
setImmediate(() => console.log('Immediate 1'));
fs.readFile(__filename, () => {
    console.log('I/O Callback');
    setTimeout(() => console.log('Timer 2'), 0);
    setImmediate(() => console.log('Immediate 2'));
    process.nextTick(() => console.log('nextTick inside I/O'));
});
Promise.resolve().then(() => console.log('Promise 1'));
process.nextTick(() => console.log('nextTick 1'));

/*
Expected Order:
1. nextTick 1 (Super Microtask)
2. Promise 1 (Microtask)
3. Timer 1 (Timer Phase)
4. Immediate 1 (Check Phase)
5. I/O Callback (Poll Phase)
6. nextTick inside I/O (Microtask drain)
7. Immediate 2 (Check Phase - runs BEFORE Timer 2 because we are in I/O)
8. Timer 2 (Timer Phase)
*/
```

---

## 🧠 Resource Behavior
*   **CPU:** Starvation can occur if Microtasks recursively schedule more Microtasks. The loop will never move to the next phase (e.g., Timers will never fire).
*   **Latency:** High Microtask volume increases "Event Loop Latency," making the server feel sluggish even if CPU % is low.

---

## 📐 ASCII Diagrams
```text
      +-----------------------------------------+
      |             CALL STACK                  |
      +--------------------+--------------------+
                           | (Empty)
                           v
      +--------------------+--------------------+
      |       MICROTASK QUEUE (Drained)         |
      |  1. process.nextTick  2. Promises       |
      +--------------------+--------------------+
                           |
      +--------------------+--------------------+
      |           EVENT LOOP PHASES             |
      | [Timers] -> [I/O] -> [Poll] -> [Check]  |
      +-----------------------------------------+
```

---

## 🔍 Code Example (Latest Node.js)
```javascript
// Demonstrating Microtask Starvation
function starve() {
    process.nextTick(starve); // Recursively add to nextTick queue
}

// This timer will NEVER fire because nextTick queue is never empty
setTimeout(() => {
    console.log("This will never run!");
}, 1000);

// starve(); // Uncomment to crash responsiveness
```

---

## 💥 Production Failures
*   **Starvation:** A complex promise chain that never yields back to the event loop, causing health checks (timers) to fail and the orchestrator (Kubernetes) to restart the pod.
*   **Order Dependency:** Relying on `setTimeout` to run before `setImmediate` (or vice versa) without understanding the phase logic.

---

## 🧪 Real-time Scenarios
*   **Database Hooks:** Using `process.nextTick` to ensure a "post-save" hook runs immediately after the current function but before the next event loop phase.
*   **UI Frameworks:** Batching multiple data updates into a single "render" call using Microtasks.

---

## ⚠️ Edge Cases
*   **Recursive `setImmediate`:** Unlike `nextTick`, recursive `setImmediate` calls won't starve the loop; they will be processed in the *next* iteration of the Check phase.
*   **Zero-latency Timers:** `setTimeout(fn, 0)` is actually `setTimeout(fn, 1)` in most environments, meaning it might miss the current tick.

---

## 🏢 Best Practices
1.  **Favor `setImmediate` for heavy work:** It allows I/O to be processed in between chunks.
2.  **Use `process.nextTick` sparingly:** Only for critical cleanup or state synchronization that *must* happen before the next phase.
3.  **Avoid deep Promise nesting:** Flatten chains to improve readability and predictability.

---

## ⚖️ Trade-offs
*   **Microtasks:** Faster execution, but high risk of starving I/O.
*   **Macrotasks:** Fairer to the system, but higher latency for the specific task.

---

## 💼 Interview Q&A
*   **Q:** What is the difference between `process.nextTick` and `setImmediate`?
*   **A:** `process.nextTick` fires immediately after the current operation (before the loop continues). `setImmediate` fires in the "Check" phase of the event loop.

---

## 🧩 Practice Problems
1.  Write a script that demonstrates that `setImmediate` runs before `setTimeout(..., 0)` when inside an `fs.readFile` callback.
2.  Create a "Microtask loop" that prevents a `setInterval` from logging more than once.

---
Prev: [../Basics/05_Basic_HTTP_Server.md](../Basics/05_Basic_HTTP_Server.md) | Index: [NodeJS/00_Index.md](../00_Index.md) | Next: [02_Async_Patterns_Promises_AsyncAwait.md](./02_Async_Patterns_Promises_AsyncAwait.md)
