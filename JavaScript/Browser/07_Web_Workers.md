# 📌 07 — Web Workers

## 🌟 Introduction

JavaScript is normally **Single-Threaded**, meaning it can only do one thing at a time. If you run a heavy calculation, your website will freeze (jank) until it's finished.

**Web Workers** allow you to run JavaScript in the background on a **separate thread**. This means you can do heavy work without freezing the user interface.

Think of it like a **Restaurant**:
-   **Main Thread:** The waiter (takes orders, talks to customers, keeps the front of house smooth).
-   **Web Worker:** The chef (stays in the kitchen, does the heavy cooking, doesn't talk to customers).
-   The waiter sends an order to the chef, and the chef sends the finished meal back.

---

## 🏗️ How it Works: Communication

Since workers run in a separate room, they can't talk to the main thread directly. They use a system called **Message Passing**.

```javascript
// 📁 main.js
const worker = new Worker('worker.js');

// Send data to the worker
worker.postMessage({ num1: 10, num2: 20 });

// Receive result from the worker
worker.onmessage = (event) => {
  console.log('Result:', event.data);
};

// 📁 worker.js
self.onmessage = (event) => {
  const { num1, num2 } = event.data;
  const result = num1 + num2; // Heavy work here
  self.postMessage(result); // Send it back
};
```

---

## 🚀 When to Use Web Workers?

1.  **Image/Video Processing:** Filtering or resizing images.
2.  **Big Data:** Sorting or filtering thousands of rows in a table.
3.  **Complex Math:** Encryption, compression, or physics engines.
4.  **Parsing:** Processing large JSON files or logs.

---

## 🏗️ The Rules of Workers

To keep things safe and fast, workers have some limitations:
-   **No DOM Access:** They cannot touch `document` or `window`.
-   **No UI:** They cannot `alert()` or `prompt()`.
-   **Isolated Scope:** They have their own global object called `self`.

---

## 📐 Visualizing the Threads

```text
MAIN THREAD (UI)                 WORKER THREAD (Background)
   │                                     │
   │  (1) postMessage(data)              │
   │ ──────────────────────────────────▶ │
   │                                     │ (2) Heavy Work...
   │                                     │ (Doesn't freeze UI)
   │  (3) onmessage(result)              │
   │ ◀────────────────────────────────── │
   ▼                                     ▼
```

---

## ⚡ Comparison Table

| Feature | Main Thread | Web Worker |
| :--- | :--- | :--- |
| **Purpose** | UI, User Interaction, DOM. | Heavy computation, Data processing. |
| **DOM Access** | ✅ Yes. | ❌ No. |
| **Blocks UI?** | ✅ Yes (if task is long). | ❌ No. |
| **Communication** | Direct. | Message Passing (`postMessage`). |

---

## 🔬 Deep Technical Dive (V8 Internals)

### Structured Clone Algorithm
When you send an object to a worker using `postMessage`, JavaScript doesn't just pass a pointer. It **deep-copies** the object using the **Structured Clone Algorithm**. For massive objects, this "copying" process can actually slow down the main thread. To avoid this, you can use **Transferables** (like `ArrayBuffer`), which move the memory ownership from one thread to another without copying it (zero-copy).

---

## 💼 Interview Questions

**Q1: What is the main benefit of Web Workers?**
> **Ans:** They provide true parallelism in the browser, allowing heavy tasks to run in the background without blocking the main thread or freezing the user interface.

**Q2: Can a Web Worker access `localStorage`?**
> **Ans:** No. Web Workers do not have access to most browser APIs like `localStorage` or the DOM. They can, however, use `fetch()`, `IndexedDB`, and `WebSockets`.

**Q3: How do you stop a Web Worker?**
> **Ans:** From the main thread, you call `worker.terminate()`. From inside the worker itself, you call `self.close()`.

---

## ⚖️ Trade-offs

| Method | Benefit | Cost |
| :--- | :--- | :--- |
| **Web Worker** | High performance for heavy math. | Overhead of creating the thread (~20-40ms). |
| **Main Thread** | Easiest to write; full DOM access. | Risk of "Long Tasks" freezing the UI. |
| **Transferables** | Zero-copy performance for large data. | The original thread loses access to the data immediately. |

---

## 🔗 Navigation

**Prev:** [06_CORS.md](06_CORS.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [08_Intersection_Observer_and_Performance.md](08_Intersection_Observer_and_Performance.md)
