# 📌 08 — Event Loop

## 🌟 Introduction

JavaScript is **single-threaded**, meaning it can only do one thing at a time. So how can we fetch data from a server, wait for a timer, and handle clicks all at once?

The answer is the **Event Loop**. It is the "Traffic Controller" that allows JavaScript to perform non-blocking operations by offloading tasks to the browser (or Node.js) and then handling the results when they are ready.

---

## 🏗️ The 3 Main Components

To understand the Event Loop, you must understand these three parts:

1.  **Call Stack:** Where your code is currently running (The "Now").
2.  **Web APIs / Node APIs:** Where "waiting" happens (e.g., `setTimeout`, `fetch`, DOM events).
3.  **Callback Queue (Task Queue):** Where finished tasks wait to be put back on the Call Stack.

---

## 🔄 How the Loop Works

The Event Loop has one simple job: **Monitor the Call Stack and the Callback Queue.**

-   If the **Call Stack is empty**, the Event Loop takes the first task from the **Callback Queue** and pushes it onto the stack to be executed.
-   This cycle repeats forever.

---

## ⚡ Microtasks vs. Macrotasks (The "VIP" Line)

Not all tasks are equal. JavaScript uses two different queues:

### 1. Microtask Queue (VIP Priority)
-   Includes: **Promises** (`.then`, `.catch`, `async/await`), `queueMicrotask`.
-   **Priority:** Extremely high. The Event Loop will **empty the entire Microtask Queue** before moving to any Macrotasks.

### 2. Macrotask Queue (Normal Priority)
-   Includes: `setTimeout`, `setInterval`, `setImmediate`, I/O, UI Rendering.

---

## 📐 Visualizing the Event Loop (The "Track" Model)

```text
 ┌──────────────────────────────────────────────────────────┐
 │                      THE CALL STACK                      │
 │   [ console.log ] ◀── Current Execution                  │
 └─────────────┬────────────────────────────────────────────┘
               │
               │ (Stack Empty?)
               ▼
 ┌──────────────────────────────────────────────────────────┐
 │                      THE EVENT LOOP                      │
 │    Check Microtask Queue... ──▶ Check Macrotask Queue    │
 └──────┬───────────────────────────────┬───────────────────┘
        │                               │
        ▼                               ▼
 ┌──────────────┐                ┌──────────────┐
 │ MICROTASK Q  │                │ MACROTASK Q  │
 │ [ Promise 1 ]│                │ [ Timeout 1 ]│
 │ [ Promise 2 ]│                │ [ Timeout 2 ]│
 └──────────────┘                └──────────────┘
 (EMPTY ENTIRELY)                (ONE AT A TIME)
```

---

## 🛠️ Real-World Troubleshooting (Q&A)

**P1: "The UI is frozen while my loop runs."**
> **Problem:** You have a massive `for` loop (e.g., processing 10 million records). The page is unresponsive, and clicks don't work.
> **Reason:** You have blocked the **Call Stack**. The Event Loop cannot check the Callback Queue or the Render Pipeline as long as the stack is not empty.
> **Fix:** Break the heavy loop into chunks using `setTimeout(0)` or `requestIdleCallback`. This "yields" control back to the Event Loop between chunks.

**P2: "Random" execution order of `setTimeout` and `Promise`.**
> **Problem:** You expected `setTimeout(..., 0)` to run before a `Promise.then()`, but it ran after.
> **Reason:** You forgot the **VIP Rule**. Even if `setTimeout` was called first, the Event Loop *always* prioritizes the Microtask Queue. It will finish all promises before it even looks at a timeout.
> **Fix:** Never rely on `setTimeout(0)` for critical ordering if promises are involved.

**P3: "Memory Leak" from growing Microtask Queue.**
> **Problem:** The app gets slower and slower over time.
> **Reason:** You have a recursive promise (a microtask that creates another microtask). This is called **Microtask Starvation**. The Macrotask Queue (which handles GC and Rendering) never gets a turn, so memory usage balloons and the UI lags.
> **Fix:** Avoid infinite promise chains. Use `setTimeout` if you need a truly "long" background process.

---

## 🔍 Code Walkthrough: Predicting Output

```javascript
console.log("Start");

setTimeout(() => {
  console.log("Timeout");
}, 0);

Promise.resolve().then(() => {
  console.log("Promise");
});

console.log("End");
```

### Execution Flow:
1.  **Logs "Start"**.
2.  `setTimeout` $\rightarrow$ Moves to **Macrotask Queue**.
3.  `Promise.resolve().then` $\rightarrow$ Moves to **Microtask Queue**.
4.  **Logs "End"**.
5.  Event Loop checks **Microtask Queue** $\rightarrow$ **Logs "Promise"**.
6.  Event Loop checks **Macrotask Queue** $\rightarrow$ **Logs "Timeout"**.

**Final Output:** `Start`, `End`, `Promise`, `Timeout`.

---

## 🔬 Deep Technical Dive (V8 Internals)

### Starvation
If a microtask keeps adding more microtasks (like a recursive promise chain), the Event Loop will stay stuck in the Microtask Queue forever. This will **starve** the Macrotask Queue and the UI, making the page completely unresponsive.

---

## 💼 Interview Questions

**Q1: Why is `setTimeout(..., 0)` not actually 0 milliseconds?**
> **Ans:** Even if the timer is 0ms, the callback must go through the Macrotask Queue. It has to wait for the Call Stack to be empty and for all currently pending Microtasks to finish.

**Q2: What happens if the Event Loop is blocked?**
> **Ans:** If a synchronous task takes too long, the Event Loop cannot check the queues. This means clicks, animations, and timers will all be frozen until that task finishes.

---

## ⚖️ Trade-offs

| Feature | Benefit | Cost |
| :--- | :--- | :--- |
| **Non-blocking I/O** | App stays responsive while waiting for data. | Complex code flow. |
| **Microtask Priority** | Important async updates happen immediately. | Risk of "starvation". |
| **Single-threaded** | No "Race Conditions" or threading bugs. | Cannot perform heavy computation. |

---

## 🔗 Navigation

**Prev:** [07_Prototype_and_Inheritance.md](07_Prototype_and_Inheritance.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [09_Promises.md](09_Promises.md)
