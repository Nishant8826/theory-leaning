# 📌 Topic: Memory Leaks and Debugging

## What
### 🧠 Concept Explanation
A memory leak is like **Leaving the Taps Running in an Empty House**.
**Analogy:** Your application code (The House) uses water (Memory) to do things. Usually, when you're done, you turn off the tap (Garbage Collection). A memory leak happens when you forget to turn off a tap—maybe it's just a drip (a single variable) or a fire hose (a massive global array). Eventually, the house floods (Out of Memory), and the foundation (The OS) shuts down the water supply (Crashes the process).

---

### 🏗️ Mental Model
Memory leaks occur when an object is no longer needed but is still reachable from a **Root** (global variables, active closures, or the call stack).

---

## Why
### 🏢 Best Practices
1.  **Use WeakMaps:** If you need to associate data with an object, use `WeakMap`. It won't prevent the object from being garbage collected.
2.  **Bounded Caches:** Always use an LRU (Least Recently Used) cache with a `maxSize` limit.
3.  **Avoid Global State:** Pass variables through function arguments instead.

---

### ⚖️ Trade-offs
*   **Deep Profiling:** Finds exact leaks but significantly slows down the application and generates massive log files.
*   **Shallow Monitoring:** Fast and safe for production, but only tells you *that* there is a leak, not *where*.

---

## How
### ⚡ Actual Behavior
1.  **Memory Usage Growth:** `rss` (Resident Set Size) increases steadily over time without ever dropping back down.
2.  **Increased GC Activity:** The CPU spikes as V8 desperately tries to clear space in the Old Generation.
3.  **Fatal Error:** The process terminates with `FATAL ERROR: Ineffective mark-compact's near heap limit Allocation failed`.

---

### 🔬 Internal Mechanics (V8 + libuv + OS)
*   **The Retainer Tree:** A graph showing which objects are keeping a specific object alive.
*   **Heap Snapshots:** A JSON file containing every object in the V8 heap and the pointers between them.
*   **Allocation Tracking:** Recording every time an object is created and where it was created in the code.

---

### 🔁 Execution Flow (Debugging)
1.  **Detect:** Monitor memory metrics in production.
2.  **Reproduce:** Run a load test (using `autocannon`) locally.
3.  **Snapshot:** Take a Heap Snapshot at the start and after 1000 requests.
4.  **Compare:** Use Chrome DevTools to find objects that exist in the second snapshot but not the first.
5.  **Fix:** Remove the stale reference.

---

### 🔍 Code Example (Latest Node.js - Creating and Finding a Leak)
```javascript
import http from 'node:http';

// THE LEAK: Global array that never clears
const leakStore = [];

const server = http.createServer((req, res) => {
    // We attach some metadata to every request and "forget" to remove it
    const metadata = {
        time: new Date(),
        url: req.url,
        headers: req.headers,
        bigBuffer: Buffer.alloc(1024 * 10) // 10KB leak per request
    };

    leakStore.push(metadata);

    res.end('Logged');
});

server.listen(3000);

/*
DEBUGGING STEPS:
1. node --inspect app.js
2. Open Chrome DevTools -> Open dedicated DevTools for Node.
3. Tab: "Memory"
4. Take Heap Snapshot 1.
5. Run load: `npx autocannon -c 100 -d 10 http://localhost:3000`
6. Take Heap Snapshot 2.
7. Compare Snapshots -> Look for "metadata" or "Array".
*/
```

---

## Impact
### 💥 Production Failures
*   **Event Listener Accumulation:** Adding `socket.on('data', ...)` inside a request handler without ever calling `.removeListener()`. Each request adds a new function to the list, and functions are objects!
*   **Closure Leaks:**
    ```javascript
    function outer() {
      let largeData = Buffer.alloc(1000000);
      return function inner() {
        console.log("I'm alive");
      };
    }
    // largeData is kept in memory as long as 'inner' exists, even if not used.
    ```

---

### 🧪 Real-time Scenarios
*   **Caching Gone Wrong:** A local `const cache = {}` that grows with every unique user ID and never expires old entries.
*   **Streaming Failures:** Piping a huge file to a socket that has already closed, causing buffers to sit in memory.

---

### ⚠️ Edge Cases
*   **Native Module Leaks:** If a C++ addon leaks memory (using `malloc` without `free`), it won't show up in a V8 Heap Snapshot because it's outside V8. You need `valgrind` or `leaks` for this.
*   **String Interning:** V8 optimizes memory by reusing identical strings. This can sometimes hide leaks or make them look smaller than they are.

---

---

Prev: [04_Event_Loop_Phases.md](./04_Event_Loop_Phases.md) | Index: [NodeJS/00_Index.md](../00_Index.md) | Next: [06_Performance_Profiling.md](./06_Performance_Profiling.md)
