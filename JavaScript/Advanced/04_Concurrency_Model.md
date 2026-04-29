# 📌 04 — Concurrency Model

## 🌟 Introduction

JavaScript is **single-threaded**, which means it's like a **"One-Lane Road."** Only one car (task) can move at a time. However, modern computers have many cores, and browsers are complex.

The **Concurrency Model** is how JavaScript manages to do many things at once without crashing the "One-Lane Road."

---

## 🏗️ Concurrency vs. Parallelism

-   **Concurrency:** Handling multiple tasks at the same time by switching between them very fast (The Event Loop).
-   **Parallelism:** Actually running multiple tasks at the exact same time on different CPU cores (Web Workers).

---

## 👷‍♂️ Web Workers (The Assistants)

If you have a very "heavy" task (like processing a 4K image), doing it on the **Main Thread** will freeze the UI.

**Web Workers** allow you to run JavaScript in a separate thread.
-   They have **no access to the DOM** (they can't touch the UI).
-   They communicate with the Main Thread via **Messages**.

```text
MAIN THREAD (UI) <─── postMessage ───> WORKER THREAD (Math/Data)
   (Smooth UI)                           (Heavy Lifting)
```

---

## 📝 Communication: `postMessage`

Since Workers are in a separate "lane," they can't share variables directly. They have to send data back and forth.

### Main Script (`main.js`)
```javascript
const myWorker = new Worker('worker.js');

myWorker.postMessage([10, 20]); // Send data to worker

myWorker.onmessage = (e) => {
  console.log('Result from worker:', e.data); // Receive result
};
```

### Worker Script (`worker.js`)
```javascript
onmessage = (e) => {
  const [a, b] = e.data;
  const result = a + b; // Do heavy work
  postMessage(result); // Send result back
};
```

---

## 🤝 Shared Memory (`SharedArrayBuffer`)

For high-performance apps (like games), sending messages back and forth might be too slow. **SharedArrayBuffer** allows the Main Thread and the Worker to see and edit the **exact same spot in memory** (The "Shared Whiteboard").

> [!CAUTION]
> Shared memory is dangerous! If two threads try to change the same number at once, you get a **Race Condition**. To fix this, use **Atomics** to ensure only one thread edits at a time.

---

## 🔬 Deep Technical Dive (V8 Internals)

### Isolates
In V8, every thread (Main Thread and every Worker) is an **Isolate**. An Isolate is a completely independent version of the JS engine. It has its own Heap and its own Garbage Collector. This is why Workers are so stable — a crash in one Worker doesn't kill the main app.

---

## 💼 Interview Questions

**Q1: Is JavaScript multi-threaded?**
> **Ans:** The core JavaScript language is single-threaded. However, the **environment** (Browser/Node.js) is multi-threaded and provides APIs like Web Workers to run code in parallel.

**Q2: What are the limitations of Web Workers?**
> **Ans:** Workers cannot access the `window`, `document`, or any DOM elements. They are strictly for processing data and calculations.

**Q3: When should you use a Web Worker?**
> **Ans:** Use them for CPU-intensive tasks like image/video processing, large data sorting, complex mathematical calculations, or encryption.

---

## ⚖️ Trade-offs

| Feature | Benefit | Cost |
| :--- | :--- | :--- |
| **Main Thread** | Full access to UI/DOM. | Can be blocked easily by heavy code. |
| **Web Workers** | Keeps the UI smooth and responsive. | Creating a Worker has a small memory/startup overhead. |
| **postMessage** | Safe communication (no shared memory bugs). | Data is "copied" (cloned), which can be slow for huge datasets. |

---

## 🔗 Navigation

**Prev:** [03_Garbage_Collection.md](03_Garbage_Collection.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [05_Debouncing_vs_Throttling.md](05_Debouncing_vs_Throttling.md)
