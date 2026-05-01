# 📌 Topic: Event Loop Basics

## What
### 🧠 Concept Explanation
The Event Loop is the **engine room** of Node.js. It is what allows Node.js to be "non-blocking" despite being single-threaded.

**The Waitstaff Analogy (Deep Dive):**
Imagine a busy café with only **one waiter** (the main thread).
*   **The Waiter (Event Loop):** Their job is to take orders and deliver food. They never stand still.
*   **The Orders (Requests):** Customers place orders (HTTP requests, database calls).
*   **The Kitchen (OS / Libuv):** When you order a complex dish (Reading a file), the waiter writes it down and gives it to the kitchen.
*   **The Crucial Moment:** The waiter **does not wait** at the kitchen door for the food to be ready. They immediately go back to the tables to take more orders.
*   **The Bell (The Callback Queue):** When the kitchen finishes the dish, they ring a bell. The waiter finishes their current task (taking an order) and then checks the "finished dish" area to deliver the food.

This allows the café to serve 100 people with only one waiter, provided the waiter never gets stuck in a long conversation with a single customer (blocking the thread).

---

### 🏗️ Mental Model
The Event Loop is essentially a **semi-infinite loop** that waits for events and then dispatches them to handler functions. It follows a very specific "schedule" of phases. It only checks for "ready" tasks when the Call Stack is empty.

1.  **Call Stack:** Where your current JS code runs.
2.  **Task Queues:** Where callbacks wait for their turn.
3.  **The Loop:** The bridge that moves tasks from the Queue to the Stack.

---

## Why
### 🏢 Best Practices
1.  **Don't starve the loop:** If you have a task that takes >10ms, it's starting to impact latency.
2.  **Use `setImmediate` for "yielding":** If you have a long array to process, process 100 items, then `setImmediate` to process the next 100.
3.  **Monitor Lag:** Use `perf_hooks` to monitor the time between ticks.

---

### ⚖️ Trade-offs
*   **Pros:** Incredible efficiency for I/O-bound applications.
*   **Cons:** One unhandled "blocking" line of code can bring down the entire system's responsiveness.

---

## How
### ⚡ Actual Behavior
The Event Loop isn't just one big pile of tasks; it's a series of **highly organized queues**. When the Call Stack is empty, Node.js enters the loop and processes these queues in order:

1.  **Timers Phase:** Handles `setTimeout` and `setInterval` callbacks whose time has expired.
2.  **Pending Callbacks Phase:** Executes I/O callbacks deferred from the previous loop iteration (rarely used by developers directly).
3.  **Idle/Prepare Phase:** Internal use only.
4.  **Poll Phase:** This is where the magic happens. Node.js waits for new I/O events (new connections, file reads). If the queue is empty, it might block here briefly to wait for events.
5.  **Check Phase:** Specifically for `setImmediate()` callbacks.
6.  **Close Callbacks Phase:** Handles "close" events, like `socket.on('close')`.

**Crucial Exception:** `process.nextTick()` and **Promises (Microtasks)** are processed **between every single phase** and even during the current execution. They are the "emergency lanes" that get priority over everything else.

---

### 🔬 Internal Mechanics (V8 + libuv + OS)
*   **Libuv's `uv_run`:** This C function runs in a `while` loop. As long as there are "active handles" (like an open server) or "active requests" (like a pending file read), the loop keeps running.
*   **The "Tick":** Every full rotation of the loop is one "Tick." Node.js monitors "Event Loop Lag" by measuring how long a single tick takes. If a tick takes 100ms, your server is effectively "lagging" because it can't respond to new events during that time.
*   **OS Polling:** Libuv doesn't "ask" the OS if a file is ready over and over. It uses **Event Demultiplexing**. It tells the OS: "Let me know when something happens on these 500 connections," and the OS wakes Node.js up only when there is actual work to do. This is why Node.js is so power-efficient.

---

### 🔁 Execution Flow
```text
1. Start Script
2. Run Synchronous Code (Top-to-bottom)
3. Process process.nextTick() queue
4. Process Microtask Queue (Promises)
5. Enter Event Loop Phases:
   a. Timers (setTimeout)
   b. Pending Callbacks (I/O)
   c. Idle/Prepare
   d. Poll (Retrieve new I/O events)
   e. Check (setImmediate)
   f. Close Callbacks
```

---

### 🔍 Code Example (Latest Node.js)
```javascript
console.log("1. Synchronous");

setTimeout(() => {
    console.log("4. Timer (Macrotask)");
}, 0);

Promise.resolve().then(() => {
    console.log("3. Promise (Microtask)");
});

process.nextTick(() => {
    console.log("2. nextTick (Super Microtask)");
});

/*
Output Logic:
1. "Synchronous" runs first (Call Stack).
2. "nextTick" runs immediately after the current operation.
3. "Promise" runs after nextTick but before any Macrotasks.
4. "Timer" runs in the next phase of the loop.
*/
```

---

## Impact
### 💥 Production Failures
*   **The "Heavy Loop" Freeze:** `while(true) {}` will prevent the Event Loop from ever checking the Task Queue. The server will not respond to any new requests.
*   **DNS Blocking:** Some legacy Node.js DNS lookups are synchronous and can block the entire loop if the DNS server is slow.

---

### 🧪 Real-time Scenarios
*   **Logging:** Writing logs asynchronously ensures that the main request processing logic isn't slowed down by disk latency.
*   **Database Queries:** While waiting for PostgreSQL to return 1000 rows, the Event Loop is free to handle 50 other incoming HTTP requests.

---

### ⚠️ Edge Cases
*   **Timer Precision:** `setTimeout(..., 0)` does not mean 0ms. It depends on the loop's current phase and CPU load. It's usually ~1-4ms.
*   **`setImmediate` vs `setTimeout`:** Within an I/O cycle, `setImmediate` is guaranteed to run before `setTimeout`.

---

---

Prev: [02_JavaScript_Execution_Model.md](./02_JavaScript_Execution_Model.md) | Index: [NodeJS/00_Index.md](../00_Index.md) | Next: [04_Modules_CommonJS_ESM.md](./04_Modules_CommonJS_ESM.md)
