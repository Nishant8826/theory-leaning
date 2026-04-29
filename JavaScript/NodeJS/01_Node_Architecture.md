# 📌 01 — Node.js Architecture

## 🌟 Introduction

Many people think Node.js is a programming language. It’s not! Node.js is a **Runtime Environment** that allows you to run JavaScript on your computer or a server (outside the browser).

Its secret sauce? **"Single-threaded JavaScript with Multi-threaded I/O."**

Think of Node.js like a **Doctor's Office**:
-   **JavaScript (The Doctor):** There is only one doctor. He can only talk to one patient at a time.
-   **libuv (The Nurses):** There are many nurses. They handle the paperwork, blood tests, and X-rays (I/O tasks) in the background while the doctor sees the next patient.

---

## 🏗️ The Core Components

1.  **V8 Engine (Google):** The brain that converts your JavaScript into machine code that the computer understands.
2.  **libuv (C++ Library):** The engine room. It manages the **Event Loop** and the **Thread Pool**. It handles all the "waiting" (reading files, database calls, network requests).

---

## 🏗️ The libuv Thread Pool

By default, libuv has **4 Threads** (Workers). When you ask Node to do something heavy, it hands the task to one of these workers:
-   **File System (fs):** Reading or writing files.
-   **Crypto:** Hashing passwords.
-   **DNS:** Looking up website addresses.

**Network requests** (like `http.get`) are special—they don't even use the thread pool! They are handled directly by the Operating System for maximum speed.

---

## 🚀 The Event Loop (The Heart of Node)

The Event Loop is a continuous cycle that checks if there is any work to be done. It has different "buckets" (phases):

1.  **Timers:** Checks for `setTimeout` or `setInterval`.
2.  **I/O Callbacks:** Handles finished network or file tasks.
3.  **Poll:** Where the loop waits for new events.
4.  **Check:** Handles `setImmediate`.
5.  **Close:** Handles cleanup (like closing a database connection).

---

## 🔍 Code Walkthrough: Blocking vs Non-Blocking

```javascript
const fs = require('fs');

// ❌ BLOCKING (Synchronous)
// The "Doctor" stops everything and waits for the file to be read.
const data = fs.readFileSync('large-file.txt'); 
console.log('Finished reading!'); // This waits...
console.log('Next Task'); // This is blocked!

// ✅ NON-BLOCKING (Asynchronous)
// The "Doctor" hands the file to a "Nurse" (libuv) and moves to the next patient.
fs.readFile('large-file.txt', (err, data) => {
  console.log('Finished reading!'); // Runs LATER
});
console.log('Next Task'); // Runs IMMEDIATELY
```

---

## 📐 Visualizing the Architecture

```text
[   YOUR JAVASCRIPT CODE   ] (Main Thread)
            │
            ▼
[     NODE.JS BINDINGS     ] (Bridge)
            │
    ┌───────┴────────┐
    ▼                ▼
[ V8 ENGINE ]   [  LIBUV  ] (Event Loop + Thread Pool)
(The Brain)      (The Muscles)
```

---

## ⚡ Comparison Table

| Feature | Browser | Node.js |
| :--- | :--- | :--- |
| **Engine** | V8 (Chrome), SpiderMonkey (Firefox). | V8 (always). |
| **Global Object** | `window` | `global` |
| **DOM Access** | ✅ Yes. | ❌ No. |
| **File System** | ❌ No (Security). | ✅ Yes (Full access). |

---

## 🔬 Deep Technical Dive (V8 Internals)

### UV_THREADPOOL_SIZE
If you are doing a lot of file reading or password hashing, you might notice Node.js slows down. This is because all 4 default libuv threads are busy. You can increase the number of "Nurses" (threads) by setting an environment variable: `process.env.UV_THREADPOOL_SIZE = 8`. This tells libuv to hire 4 more workers to handle the load.

---

## 💼 Interview Questions

**Q1: Is Node.js truly single-threaded?**
> **Ans:** Yes and No. The **JavaScript execution** is single-threaded (one thing at a time). However, the **I/O operations** (files, network) are handled by libuv, which uses multiple threads and the Operating System in the background.

**Q2: What is the difference between `setImmediate` and `setTimeout(0)`?**
> **Ans:** `setTimeout(0)` goes into the **Timers** phase of the next loop. `setImmediate` is designed to run in the **Check** phase, which usually happens right after the I/O phase.

**Q3: Why is Node.js great for Chat Apps but bad for Video Editing?**
> **Ans:** Chat apps involve a lot of "Waiting" for data (I/O), which Node handles perfectly. Video editing involves "Heavy Math" (CPU), which would block the single JavaScript thread and freeze the entire server.

---

## ⚖️ Trade-offs

| Method | Benefit | Cost |
| :--- | :--- | :--- |
| **Single Process** | Very fast for I/O; low memory. | Can't use multiple CPU cores. |
| **Cluster Module** | Runs multiple copies of Node to use all CPU cores. | Each copy uses its own memory. |
| **Worker Threads**| Good for heavy math tasks in the background. | Complex to share data between threads. |

---

## 🔗 Navigation

**Prev:** [../Browser/09_Animation_and_Frame_Budget.md](../Browser/09_Animation_and_Frame_Budget.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [02_Event_Emitter.md](02_Event_Emitter.md)
