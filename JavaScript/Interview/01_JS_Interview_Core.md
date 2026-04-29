# 📌 01 — JS Interview Core Concepts

## 🌟 Introduction

To ace a senior-level JavaScript interview, you need to go beyond knowing the syntax. You need to understand **how the engine (V8) works**.

This file summarizes the "Heavy Hitters"—the questions that separate juniors from seniors.

---

## 🏗️ 1. The Event Loop & Priority

Interviewers love asking "What is the output of this code?" with a mix of `setTimeout` and `Promises`.

**The Priority Order:**
1.  **Synchronous Code:** Runs immediately (Call Stack).
2.  **Microtasks:** `Promises`, `queueMicrotask`. (Runs after every piece of sync code).
3.  **Tasks (Macrotasks):** `setTimeout`, `setInterval`, `DOM Events`. (Runs only after the microtask queue is empty).

```javascript
console.log('1'); // Sync
setTimeout(() => console.log('2'), 0); // Task
Promise.resolve().then(() => console.log('3')); // Microtask
console.log('4'); // Sync

// Output: 1, 4, 3, 2
```

---

## 🏗️ 2. Closures (The Engine Perspective)

A **Closure** is when a function remembers its outer variables even after the outer function has finished.

**Engine Secret:** V8 doesn't just "remember" everything. It creates a **Context Object** on the Heap. If a variable is used inside a closure, it's moved from the Stack to this Heap object so it doesn't get deleted when the function returns.

---

## 🏗️ 3. `this` Binding (Call-time vs Definition-time)

The value of `this` is usually decided **when the function is called**, not when it is written.

| Call Type | `this` value |
| :--- | :--- |
| `obj.func()` | `this` is `obj`. |
| `func()` | `this` is `window` (or `undefined` in strict mode). |
| `func.call(otherObj)` | `this` is `otherObj`. |
| **Arrow Function** | `this` is inherited from where the function was **written**. |

---

## 🏗️ 4. The Prototype Chain

Every object has a "hidden link" to another object called its **Prototype**.

-   When you access `user.name`, V8 first looks at the `user` object.
-   If it’s not there, it follows the link to the prototype.
-   This continues until it reaches `Object.prototype` or finds the property.

---

## 🏗️ 5. Hoisting & The TDZ

-   **`var`:** Is hoisted and initialized as `undefined`. (You can use it before it’s declared).
-   **`let` / `const`:** Are hoisted but **not initialized**.
-   **Temporal Dead Zone (TDZ):** The "Danger Zone" from the start of the block until the variable is declared. Accessing it here throws a `ReferenceError`.

---

## 🚀 Rapid-Fire Interview Facts

1.  **`typeof null` is `"object"`:** This is a 30-year-old bug in JavaScript that was never fixed because it would break too many websites.
2.  **`0.1 + 0.2 !== 0.3`:** Computers use binary to store decimals. 0.1 and 0.2 can't be stored exactly, so you get `0.30000000000000004`.
3.  **`NaN === NaN` is `false`:** `NaN` is the only value in JS that is not equal to itself. Use `Number.isNaN()` instead.
4.  **`Map` vs `Object`:** Use `Map` for frequent additions/removals or when keys aren't strings. Use `Object` for simple data records.

---

## 📐 Visualizing the Event Loop Priority

| Step | Type | Example |
| :--- | :--- | :--- |
| **1** | Synchronous | `console.log`, `for` loops. |
| **2** | Microtask | `.then()`, `await`. |
| **3** | Animation | `requestAnimationFrame`. |
| **4** | Task | `setTimeout`. |

---

## 💼 Senior Level Tip: Memory Leaks

If asked about memory leaks, mention:
-   **Uncleared Timers:** `setInterval` running forever.
-   **Closures:** Holding onto large objects in a global variable.
-   **Forgotten DOM References:** Keeping a JS reference to a button that was removed from the HTML.
-   **WeakMap:** Use `WeakMap` to store metadata about objects so they can be garbage collected when no longer needed.

---

## 🔗 Navigation

**Prev:** [../Performance/08_GC_Performance_Tuning.md](../Performance/08_GC_Performance_Tuning.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [02_Tricky_Questions.md](02_Tricky_Questions.md)
