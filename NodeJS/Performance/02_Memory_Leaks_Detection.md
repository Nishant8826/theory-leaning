# 📌 02 — Memory Leaks Detection: Finding Hidden RAM Hogs

## 🧠 Concept Explanation

### Basic → Intermediate
A memory leak occurs when a program allocates memory but fails to release it back to the operating system. In Node.js, this usually means an object is still reachable from the "Root" (Global object or active Stack) even though it is no longer needed.

### Advanced → Expert
At a staff level, memory leaks are usually caused by **Retained Closures** or **Forgotten Subscriptions**.
1. **Global Variables**: Attaching data to `global` or a module-level variable that grows forever.
2. **Closures**: An inner function that references a large variable from the outer scope, preventing that variable from being GC'd as long as the inner function exists.
3. **Event Listeners**: Adding `.on('data', ...)` to a long-lived emitter (like a database connection) inside a request handler and never calling `.removeListener()`.
4. **Timers**: A `setInterval` that keeps running in the background, referencing objects that should have been deleted.

---

## 🏗️ Common Mental Model
"V8 will clean it up eventually."
**Correction**: V8's Garbage Collector can only clean up objects that are **unreachable**. If you have a single reference to a 1GB object in a global array, V8 **must** keep it in memory.

---

## ⚡ Actual Behavior: The "Shallow" vs "Retained" Size
- **Shallow Size**: The memory taken by the object itself (e.g. just the keys and basic properties).
- **Retained Size**: The total memory that would be freed if this object were deleted (including all other objects it exclusively points to).
When debugging leaks, always look at the **Retained Size**.

---

## 🔬 Internal Mechanics (V8 Heap)

### The Dominator Tree
V8 builds a graph of objects. An object A "dominates" object B if every path from the Root to B goes through A. If A is deleted, B is guaranteed to be collected.

### WeakRef and FinalizationRegistry
Modern Node.js (v14.6+) provides `WeakRef`, which allows you to hold a reference to an object without preventing it from being GC'd. This is useful for building caches that don't leak memory.

---

## 📐 ASCII Diagrams

### How a Closure Leaks Memory
```text
  function outer() {
    const hugeData = new Array(1000000); // 1. Allocated
    
    return function inner() {
      // 2. inner() is returned and stored in a Global variable
      // 3. inner() "captures" hugeData in its closure
      console.log(hugeData.length);
    };
  }
  
  global.leak = outer(); // 4. hugeData is now trapped forever!
```

---

## 🔍 Code Example: The Event Listener Leak
```javascript
const EventEmitter = require('events');
const db = new EventEmitter(); // Long-lived

function handleRequest(req, res) {
  const bigData = { id: 1, content: '...' };
  
  // ❌ LEAK: Every request adds a new listener to 'db'
  // The listener closure captures 'bigData' and 'res'
  db.on('update', () => {
    console.log('Update for', bigData.id);
  });
  
  res.send('Done');
}
```

---

## 💥 Production Failures & Debugging

### Scenario: The Slowly Growing RSS
**Problem**: The process starts at 100MB RAM. Every day it grows by 100MB. After 10 days, it crashes.
**Reason**: A small leak in a high-frequency path (e.g. adding one string to a global log array on every request).
**Debug**: 
1. Take a Heap Snapshot at Start.
2. Take a Heap Snapshot after 1 hour.
3. Use the **Comparison** view in Chrome DevTools to see which objects were created but not deleted between the two snapshots.

---

## 🧪 Real-time Production Q&A

**Q: "I see thousands of '(string)' objects in my heap snapshot. Is that the leak?"**
**A**: **Probably not directly.** Strings are the most common primitive. Look at what is **holding** those strings. Look for a "Distance" from root and see which custom class or closure is the parent.

---

## 🧪 Debugging Toolchain
- **`heapdump`**: Generate snapshots programmatically.
- **`memwatch-next`**: Emits an event when it detects a "leak-like" pattern in memory growth.

---

## 🏢 Industry Best Practices
- **Avoid Module-Level State**: Store request-specific data inside the request lifecycle, not in file-level variables.
- **Use `once()` for Listeners**: If you only need to react to an event once, use `.once()` to ensure the listener is auto-removed.

---

## 💼 Interview Questions
**Q: How does a "Detached DOM Node" leak happen in the browser, and what is the Node.js equivalent?**
**A**: In a browser, it's a DOM node removed from the page but still referenced in JS. In Node.js, the equivalent is an **Open Handle** (like an unclosed Socket or File Descriptor) that is still referenced by an object, preventing the object and the handle's buffer from being freed.

---

## 🧩 Practice Problems
1. Write a script that deliberately leaks memory via a closure. Use a heap snapshot to identify the variable name being leaked.
2. Compare the memory usage of a regular `Map` vs a `WeakMap` when the keys are deleted.

---

**Prev:** [01_Profiling_and_Analysis.md](./01_Profiling_and_Analysis.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [03_Event_Loop_Lag_Monitoring.md](./03_Event_Loop_Lag_Monitoring.md)
