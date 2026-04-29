# 📌 05 — Closures

## 🌟 Introduction

A **Closure** is when a function "remembers" the variables from its parent scope, even after the parent function has finished executing.

In simple terms: **Closure = Function + Lexical Environment**.

---

## 🏗️ The "Backpack" Metaphor

Imagine a student (the function) going home for the summer. Even though they left the school (the parent scope), they brought a **backpack** filled with books (variables). Whenever they need to study, they just look inside their backpack.

In JavaScript, every function carries a "backpack" of all the variables it had access to when it was created.

---

## 🔄 How it Works

When a function is defined inside another function, it gets a reference to the outer function's **Lexical Environment**.

```javascript
function outer() {
  let money = 100;
  
  return function inner() {
    money++; // inner() has access to money!
    console.log(money);
  };
}

const myWallet = outer(); // outer() is finished and its stack frame is gone.
myWallet(); // 101
myWallet(); // 102
```

---

## 📚 Why Use Closures?

### 1. Data Privacy (Encapsulation)
You can create "private" variables that cannot be accessed from the outside.

### 2. Maintaining State
Closures allow functions to "persist" data across multiple calls without using global variables.

---

## 📐 Visualizing the Closure (The "Backpack" Model)

```text
 ┌──────────────────────────────────────────────────────────┐
 │                      CALL STACK                          │
 ├──────────────────────────────────────────────────────────┤
 │ [ FEC: inner() ] ──▶  Looking for 'money'?               │
 │                      Check local... NO.                  │
 │                      Check "Backpack"... YES! (100)      │
 ├──────────────────────────────────────────────────────────┤
 │      (outer() context has been popped off/deleted)       │
 └──────────────────────────────────────────────────────────┘
           │
           ▼
 ┌──────────────────────────────────────────────────────────┐
 │                        THE HEAP                          │
 ├──────────────────────────────────────────────────────────┤
 │  [ CLOSURE (BACKPACK) ]                                  │
 │  { money: 101 }  <── Shared by all inner functions       │
 └──────────────────────────────────────────────────────────┘
```

---

## 🛠️ Real-World Troubleshooting (Q&A)

**P1: "Stale" Data in a Timer or Event Listener.**
> **Problem:** My `setInterval` is always printing the same old value of a variable, even though the variable changed outside.
> **Reason:** The closure "captured" the variable at the moment the timer was created. If you re-assign the variable (`myVar = newValue`), the old closure is still looking at the old reference or value.
> **Fix:** Use an object to store your data `{ value: 10 }` and mutate the property, or use the functional update pattern (common in React).

**P2: Memory Leaks in Large Single-Page Apps (SPAs).**
> **Problem:** The browser tab uses 2GB of RAM after 1 hour of use.
> **Reason:** You are adding closures (event listeners) to the `window` or `document` that reference large objects. Even when you "delete" the objects, the closures keep them alive.
> **Fix:** Always remove event listeners (`removeEventListener`) when a component or page is destroyed.

**P3: Unexpected Shared State between multiple functions.**
> **Problem:** I created two counters using the same `createCounter` function, but they are affecting each other.
> **Reason:** You likely defined a variable *outside* the `createCounter` function (in the global or parent scope). Both counters are now closing over the exact same variable.
> **Fix:** Ensure the variables you want to be "private" and "unique" are defined *inside* the parent function.

---

## 🔍 Code Walkthrough: The Loop Problem

This is a classic interview question:

```javascript
for (var i = 1; i <= 3; i++) {
  setTimeout(() => console.log(i), 1000);
}
// Output: 4, 4, 4
```

**Why?** `var` has function scope. By the time `setTimeout` runs (after 1 second), the loop is finished and `i` is 4. All three closures point to the **same** `i`.

**Fix with `let`:**
```javascript
for (let i = 1; i <= 3; i++) {
  setTimeout(() => console.log(i), 1000);
}
// Output: 1, 2, 3
```

---

## 🔬 Deep Technical Dive (V8 Internals)

### Escape Analysis
V8 performs "Escape Analysis" to decide where to store variables.
- If a variable **never escapes** its function (no closure), it stays on the **Stack** (super fast).
- If a variable **escapes** via a closure, V8 moves it to a **Context Object** on the **Heap** (slower but persistent).

---

## 💼 Interview Questions

**Q1: What is a Closure?**
> **Ans:** A closure is a function bundled together with references to its surrounding state (lexical environment). It gives you access to an outer function's scope from an inner function.

**Q2: What are the advantages of Closures?**
> **Ans:** Encapsulation (private variables), modularization, and maintaining state without polluting the global scope.

**Q3: Can closures cause performance issues?**
> **Ans:** Yes. They consume more memory because the captured variables cannot be garbage collected as long as the closure exists.

---

## ⚖️ Trade-offs

| Feature | Benefit | Cost |
| :--- | :--- | :--- |
| **Encapsulation** | Protects data from accidental mutation. | Harder to debug (variables are "hidden"). |
| **Persistent State** | No need for global variables. | Risk of memory leaks if not managed. |
| **Memory Management** | Variables live exactly as long as needed. | Higher memory usage (Heap instead of Stack). |

---

## 🔗 Navigation

**Prev:** [04_Scope_and_Lexical_Environment.md](04_Scope_and_Lexical_Environment.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [06_This_Keyword.md](06_This_Keyword.md)
