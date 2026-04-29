# 📌 02 — Memory Management

## 🌟 Introduction

In low-level languages like C, developers have to manually manage memory (allocate and free it). In JavaScript, this is handled automatically by the engine (like V8) using a process called **Garbage Collection**.

Think of Memory Management like an **"Auto-Cleaning Kitchen"**:
1.  **Allocate:** You grab a plate (create a variable/object).
2.  **Use:** You eat from the plate.
3.  **Release:** A robot waiter (Garbage Collector) takes the plate away once you're done.

---

## 🏗️ Stack vs. Heap (Where is data stored?)

JavaScript uses two different types of memory to store data:

### 1. The Stack (Fast & Simple)
-   Stores **Static Data**: Primitives (numbers, strings).
-   Size is fixed.
-   Managed as **LIFO**.

### 2. The Heap (Large & Flexible)
-   Stores **Dynamic Data**: Objects, Arrays, and Functions.
-   Size is flexible.
-   Managed by the **Garbage Collector**.

---

## 📐 Visualizing the Pointer Relationship

```text
       [ THE STACK ]                        [ THE HEAP ]
       (Primitives)                         (Objects)
       
 ┌──────────────────────┐             ┌───────────────────────────┐
 │ userRef: 0x4A12B7 ───┼────────────▶│ {                         │
 ├──────────────────────┤             │   name: "Nishant",        │
 │ score: 100           │             │   skills: ["JS", "Go"]    │
 ├──────────────────────┤             │ }                         │
 │ isActive: true       │             └───────────────────────────┘
 └──────────────────────┘
 (The variable on the stack is just an address pointing to the heap)
```

---

## 🛠️ Real-World Troubleshooting (Q&A)

**P1: "Out of Memory" (OOM) crashes in Node.js.**
> **Problem:** My server crashes with `FATAL ERROR: Ineffective mark-compacts near heap limit`.
> **Reason:** Your app is filling up the **Heap** faster than the Garbage Collector can clean it. This is usually caused by a large cache (like a global object) that never clears.
> **Fix:** Monitor memory usage using `--inspect` and Chrome DevTools. Use `WeakMap` for caching if possible, or increase the heap limit using `--max-old-space-size=4096`.

**P2: Memory Leaks in Single-Page Applications (SPAs).**
> **Problem:** The browser tab uses more and more RAM as the user navigates between pages.
> **Reason:** You are adding **Event Listeners** to the `window` or `document` inside a component but forgetting to remove them when the component unmounts. The listener (and everything it references) is "leaked."
> **Fix:** Always clean up in `componentWillUnmount` or the `useEffect` return function: `window.removeEventListener(...)`.

**P3: "Detached" DOM Nodes.**
> **Problem:** Even after deleting a 1,000-row table from the UI, the memory is not freed.
> **Reason:** You have a variable in your JavaScript code that still points to one of the rows in that table. Even though the table is gone from the *screen*, it stays in the *Heap* because it's still "reachable."
> **Fix:** Set any variables that reference DOM elements to `null` once you remove them from the document.

---

## ⚠️ Memory Leaks (Common Causes)

1.  **Accidental Globals:** `window.x = data` stays forever.
2.  **Forgotten Timers:** `setInterval` keeps variables alive.
3.  **Closures:** Inner functions trapping outer variables.

---

## 🔬 Deep Technical Dive (V8 Internals)

### Generational Collection
V8 splits the Heap into two generations:
-   **New Space:** For short-lived objects.
-   **Old Space:** For objects that have survived multiple cleanup cycles.

---

## 💼 Interview Questions

**Q1: What is the difference between Stack and Heap memory?**
> **Ans:** The Stack is for static data (primitives) and is very fast. The Heap is for dynamic data (objects) and is managed by the Garbage Collector.

**Q2: What happens when the Heap is full?**
> **Ans:** If the Heap reaches its limit, the application will crash with an **"Out of Memory" (OOM)** error.

---

## 🔗 Navigation

**Prev:** [01_Deep_vs_Shallow_Copy.md](01_Deep_vs_Shallow_Copy.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [03_Garbage_Collection.md](03_Garbage_Collection.md)
