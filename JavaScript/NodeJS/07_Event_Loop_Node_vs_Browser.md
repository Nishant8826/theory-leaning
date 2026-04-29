# 📌 07 — Event Loop: Node.js vs Browser

## 🌟 Introduction

Both the Browser and Node.js use an **Event Loop** to handle asynchronous tasks. However, they aren't exactly the same.

Think of it like two different **Race Tracks**:
-   **The Browser Track:** Optimized for **Spectators** (Users). It focuses on smooth animations and reacting to clicks.
-   **The Node.js Track:** Optimized for **Freight** (Data). It focuses on handling thousands of file reads and network requests as fast as possible.

---

## 🏗️ The Key Differences

| Feature | Browser | Node.js |
| :--- | :--- | :--- |
| **Engine Room** | Handled by the Browser (Web APIs). | Handled by **libuv** (C++). |
| **Phases** | Simple: Tasks & Microtasks. | Complex: 6 specific phases (Timers, I/O, etc). |
| **Special VIP** | None. | **`process.nextTick`** (Runs before anything else). |
| **Animations** | `requestAnimationFrame` (rAF). | Not available. |
| **Immediate** | Not available. | **`setImmediate`**. |

---

## 🏗️ The "VIP" Queue: `process.nextTick`

Node.js has a special queue called `nextTick`. It is like a **VIP Pass** at a club.

If you call `process.nextTick()`, Node will finish what it's doing and then immediately run that function **before moving to the next phase of the loop**.

> [!WARNING]
> **Danger:** If you recursively call `nextTick`, the Event Loop will get stuck in a loop and never move on to handle I/O or Timers. This is called **Event Loop Starvation**.

---

## 🚀 `setImmediate` vs `setTimeout(0)`

This is the most common interview question in Node.js.

-   **Inside an I/O callback** (like `fs.readFile`): `setImmediate` **ALWAYS** runs first.
-   **Outside an I/O callback**: The order is random! It depends on how fast your computer's clock is at that exact millisecond.

---

## 🔍 Code Walkthrough: The Race

```javascript
// Node.js Code
console.log('1. Start');

setTimeout(() => console.log('5. Timeout'), 0);
setImmediate(() => console.log('6. Immediate'));

process.nextTick(() => console.log('2. NextTick'));

Promise.resolve().then(() => console.log('3. Promise'));

console.log('4. End');

// Result: 1, 4, 2, 3, 5/6 (5 and 6 might swap)
```

**Why this order?**
1.  **Sync Code (1, 4):** Always first.
2.  **nextTick (2):** The highest priority "VIP" queue.
3.  **Promises (3):** The regular microtask queue.
4.  **Timers/Check (5, 6):** The actual event loop phases.

---

## 📐 Visualizing the Two Loops

**Browser Loop:**
`Sync Code` ➔ `All Microtasks` ➔ `Render UI` ➔ `Next Task`

**Node.js Loop:**
`Sync Code` ➔ `nextTick` ➔ `Microtasks` ➔ `Phases (Timers ➔ I/O ➔ Poll ➔ Check ➔ Close)`

---

## 🔬 Deep Technical Dive (V8 Internals)

### libuv Integration
In the browser, the event loop is part of the HTML spec. In Node, it's a separate C++ library called **libuv**. Because libuv is independent of V8, it can be updated or changed without changing the JavaScript engine. This is why Node.js can have very different timing behaviors than Chrome, even though they both use the same V8 engine.

---

## 💼 Interview Questions

**Q1: What is the difference between Microtasks and Macrotasks?**
> **Ans:** Microtasks (Promises, nextTick) are high priority and run immediately after the current task. Macrotasks (setTimeout, setImmediate, I/O) are lower priority and run in specific phases of the loop.

**Q2: When should you use `process.nextTick`?**
> **Ans:** Use it when you need to ensure a piece of code runs **after** the current function finishes but **before** the event loop continues (e.g., for error handling or cleanup).

**Q3: Can `setImmediate` block the event loop?**
> **Ans:** No. Unlike `nextTick`, `setImmediate` is a phase in the loop. Even if you have many `setImmediate` calls, Node will eventually move to the next phase, preventing starvation.

---

## ⚖️ Trade-offs

| Method | Benefit | Cost |
| :--- | :--- | :--- |
| **`process.nextTick`** | Runs as soon as possible. | Can block the event loop (Starvation). |
| **`setImmediate`** | Safe and predictable. | Runs slightly later than nextTick. |
| **`setTimeout(0)`** | Cross-platform (works in browser). | Not guaranteed to be "immediate" (has ~1-4ms delay). |

---

## 🔗 Navigation

**Prev:** [06_Middleware_Design.md](06_Middleware_Design.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [08_Backpressure_Deep_Dive.md](08_Backpressure_Deep_Dive.md)
