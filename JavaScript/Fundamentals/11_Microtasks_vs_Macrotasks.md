# 📌 11 — Microtasks vs Macrotasks

## 🌟 Introduction

In the JavaScript Event Loop, not all asynchronous tasks are treated equally. They are divided into two main categories: **Microtasks** and **Macrotasks** (often just called "Tasks").

Understanding the priority of these two queues is the key to mastering JavaScript execution order.

---

## 🏗️ The Two Queues

### 1. The Microtask Queue (VIP Priority)
These tasks have the highest priority. After any synchronous code finishes, the Event Loop will look here first.
-   **Sources:** `Promise.then/catch/finally`, `async/await`, `queueMicrotask()`.
-   **Rule:** The Event Loop will not move to the next "Macrotask" until this queue is **completely empty**.

### 2. The Macrotask Queue (Standard Priority)
These are standard asynchronous tasks.
-   **Sources:** `setTimeout`, `setInterval`, `setImmediate`, I/O tasks, UI rendering, user events (click, scroll).
-   **Rule:** Only **one** Macrotask is executed per loop iteration.

---

## 📐 Visualizing the Queue Hierarchy

```text
  [  NOW (Synchronous)  ]
             │
             ▼
  [  VIP LINE (Microtasks) ]  <── EMPTY ENTIRE QUEUE
             │
             ▼
  [  UI RENDER (Painting)  ]  <── ONLY IF NECESSARY
             │
             ▼
  [  NORMAL LINE (Macrotasks) ] <── ONE TASK AT A TIME
```

---

## 🛠️ Real-World Troubleshooting (Q&A)

**P1: "Race conditions" between Timeout and Promise.**
> **Problem:** My code logic depends on a `setTimeout` running before a `Promise`, but it keeps happening the other way around.
> **Reason:** You are fighting the engine's built-in priority. Promises (Microtasks) will *always* win against Timeouts (Macrotasks).
> **Fix:** Don't rely on timing for critical logic. If you need a specific order, chain your promises or use `await` consistently.

**P2: High CPU usage but low traffic in Node.js.**
> **Problem:** My Node.js server is at 100% CPU.
> **Reason:** You might have **Microtask Starvation**. A recursive promise or a very tight loop of `queueMicrotask` is keeping the Event Loop busy in the VIP line, so it never gets a chance to handle I/O or other requests.
> **Fix:** Use `setImmediate()` instead of `process.nextTick()` or recursive promises if you want to break up heavy work and let the loop "breathe."

**P3: UI Stuttering (Jank) despite using `async`.**
> **Problem:** I'm doing heavy math in an `async` function, but the page still lags.
> **Reason:** Even though the function is `async`, the heavy math *inside* it is still synchronous. Only the parts after an `await` are asynchronous.
> **Fix:** Use `Web Workers` for heavy calculations, or use `await new Promise(r => setTimeout(r, 0))` periodically to yield control back to the UI renderer.

---

## 🔍 Code Walkthrough: The Priority Test

```javascript
console.log("1. Sync");

setTimeout(() => {
  console.log("2. Macrotask (Timeout)");
}, 0);

Promise.resolve().then(() => {
  console.log("3. Microtask (Promise)");
});

console.log("4. Sync");
```

**Final Output:** `1, 4, 3, 2`

---

## 🔬 Deep Technical Dive (V8 Internals)

### Checkpoint Draining
V8 drains the microtask queue at "Microtask Checkpoints". These checkpoints happen whenever the JS call stack becomes empty during task execution.

---

## 💼 Interview Questions

**Q1: Which runs first: `setTimeout` or `Promise.resolve()`?**
> **Ans:** `Promise.resolve().then()` runs first because it is a Microtask.

**Q2: Does `await` create a Microtask?**
> **Ans:** Yes. Everything after an `await` keyword is effectively wrapped in a `.then()` and scheduled as a Microtask.

---

## ⚖️ Trade-offs

| Feature | Benefit | Cost |
| :--- | :--- | :--- |
| **Microtasks** | Fast updates. | Risk of Starvation. |
| **Macrotasks** | Fair scheduling. | Slower (waits for loop). |

---

## 🔗 Navigation

**Prev:** [10_Async_Await.md](10_Async_Await.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [12_Execution_Order_Deep_Dive.md](12_Execution_Order_Deep_Dive.md)
