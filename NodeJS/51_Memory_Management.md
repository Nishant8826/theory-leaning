# Memory Management

## What You Will Learn
* How V8 allocates memory across the Stack and the Heap.
* Analyzing memory footprints using `process.memoryUsage()`.
* The difference between RSS, Heap Total, Heap Used, and External memory.
* Identifying and resolving common memory leak patterns in Node.js.

## Why This Matters
JavaScript handles memory management automatically using a garbage collector. However, in long-running backend servers, memory leaks (retaining references to objects that are no longer needed) will slowly consume available RAM. Over time, memory usage increases until the V8 engine runs out of memory, causing the application to crash in production.

## Theory

### Stack vs. Heap Memory Allocation
V8 divides memory into two main structures:
* **Stack**: A fast, LIFO (Last In, First Out) memory space managed directly by the CPU. It stores local primitive variables (numbers, booleans, undefined) and function execution stack frames. Memory is reclaimed automatically when the function returns and clears from the call stack.
* **Heap**: A large, unstructured memory space used to store reference types (objects, arrays, functions, and buffers). Allocation and cleanup are managed dynamically by V8's Garbage Collector.

### Analyzing Memory: `process.memoryUsage()`
To monitor memory consumption, use the native `process.memoryUsage()` API. It returns an object containing:
1. **`rss` (Resident Set Size)**: The total physical memory allocated to the Node.js process by the operating system (includes the V8 heap, C++ code space, and all loaded native modules/bindings).
2. **`heapTotal`**: The total memory allocated by V8 for JavaScript objects.
3. **`heapUsed`**: The actual memory currently occupied by JavaScript objects. A steadily increasing `heapUsed` over time indicates a memory leak.
4. **`external`**: Memory used by C++ objects bound to JavaScript (like buffers allocated outside the V8 heap).
5. **`arrayBuffers`**: Memory allocated for SharedArrayBuffers and TypedArrays.

## Deep Dive

### Common Memory Leak Vectors in Node.js
Memory leaks occur when objects are no longer needed but remain reachable from the root object (the global scope), preventing the garbage collector from reclaiming their memory.

1. **Accidental Global Variables**: Declaring variables without `var`, `let`, or `const` binds them to the global object, meaning they are never garbage collected:
   ```javascript
   function leak() {
     leakedData = new Array(1000000); // Binds to global.leakedData!
   }
   ```
2. **Forgotten Event Listeners**: Registering event listeners on long-lived global objects (like `process` or database connection pools) without removing them when the request finishes:
   ```javascript
   process.on('configUpdate', () => { ... }); // Never garbage collected!
   ```
3. **Uncleared Intervals/Timeouts**: Callbacks inside `setInterval` or `setTimeout` hold references to variables in their parent scopes via closures. If the interval is not cleared, the closed-over variables cannot be garbage collected.
4. **Unbounded Caches**: Storing data (like user profiles or API responses) in a simple JavaScript object cache without setting expiration times or maximum size limits. As users increase, the cache grows until the server runs out of memory.

## Visual Explanation

### V8 Memory Footprint (Resident Set Size Layout)
```text
+-----------------------------------------------------------------------------+
| Resident Set Size (RSS) - Total OS Process Memory                           |
|                                                                             |
|  +-----------------------------------------------------------------------+  |
|  | V8 Heap Memory                                                        |  |
|  |   ├── heapTotal (Allocated space)                                     |  |
|  |   └── heapUsed  (Active JS Objects, Arrays, Closures)                 |  |
|  +-----------------------------------------------------------------------+  |
|                                                                             |
|  +--------------------------------------+  +-----------------------------+  |
|  | External Memory (C++ Buffers, Slabs) |  | C++ Code / Native Bindings  |  |
|  +--------------------------------------+  +-----------------------------+  |
+-----------------------------------------------------------------------------+
```

## Real-World Example
Consider an Express route handler that logs request analytics to a local array. If you push metadata to a global array on every request, the array grows indefinitely. Under heavy load, the heap memory will slowly rise (as shown in `heapUsed`) until V8 exhausts its limit (~1.4GB on 64-bit systems by default) and crashes with an `Out of Memory` error.

## Code Examples

### Tracking Memory Footprints and Simulating a Leak

```javascript
// memory-leak-demo.js
const express = require('express');
const app = express();

// A global cache that grows indefinitely (Memory Leak Vector)
const unboundedCache = {};

// Helper to log current memory footprint
const logMemoryUsage = (tag) => {
  const mem = process.memoryUsage();
  const toMB = (bytes) => (bytes / 1024 / 1024).toFixed(2);
  console.log(`[${tag}] RSS: ${toMB(mem.rss)}MB | Heap Used: ${toMB(mem.heapUsed)}MB | External: ${toMB(mem.external)}MB`);
};

app.get('/api/search', (req, res) => {
  const searchTerm = req.query.q || 'default';
  
  // Simulate fetching a heavy database record (1MB payload)
  const heavyDataPayload = new Array(1000000).fill('UserDataString');

  // Cache results to make subsequent searches fast
  // DANGER: No eviction policy (no size limit, no TTL expiration)
  unboundedCache[searchTerm] = heavyDataPayload;

  logMemoryUsage('SEARCH-REQUEST');
  res.json({ status: 'success', term: searchTerm });
});

app.get('/api/gc', (req, res) => {
  // Expose garbage collector in Node using flag: node --expose-gc script.js
  if (global.gc) {
    console.log('\n--- Running Manual Garbage Collection ---');
    global.gc();
    logMemoryUsage('AFTER-GC');
    res.send('Garbage Collection triggered.');
  } else {
    res.send('Garbage collection not exposed. Run node with --expose-gc');
  }
});

app.listen(3000, () => {
  logMemoryUsage('SERVER-START');
  console.log('Memory monitoring server running on port 3000');
});
```

## Best Practices
* **Enforce Strict Mode**: Always run JavaScript in strict mode (`"use strict";`) or use TypeScript to prevent accidental global variables.
* **Always Clear Schedulers and Listeners**: Always call `clearInterval()` or `clearTimeout()` and remove event listeners when they are no longer needed.
* **Set Cache Limits**: Use mature caching libraries with built-in eviction policies (like Least Recently Used - LRU) and TTL expirations (like `lru-cache`) instead of plain JavaScript objects.
* **Use Streams for Heavy Data**: Use streams to process heavy files or database queries in chunks, keeping the V8 heap memory footprint low.

## Interview Questions

### Beginner
* **What is the difference between the Stack and the Heap in V8 memory allocation?**
  *Answer*: The Stack stores fast, local primitive values and function execution stack frames that are managed automatically by the CPU and reclaimed when functions return. The Heap stores complex reference objects (objects, arrays, functions) whose memory is allocated dynamically and cleaned up by V8's Garbage Collector.

### Intermediate
* **What is the difference between `heapUsed` and `rss` in `process.memoryUsage()`?**
  *Answer*: `heapUsed` represents the actual memory currently occupied by JavaScript objects within the V8 heap. `rss` (Resident Set Size) represents the total physical memory allocated to the Node.js process by the operating system, which includes the V8 heap, C++ execution code space, and all loaded native modules/bindings.

### Advanced
* **Explain how a memory leak can occur via a closure in a Node.js route handler. How do you resolve it?**
  *Answer*: A memory leak occurs when a child function (closure) references variables from its parent scope (such as request/response payloads or database connections), and the child function remains registered on a long-lived global object (like a global event emitter or interval). 
  Because the global object retains a reference to the child function, and the child function retains a reference to the parent scope, the parent variables cannot be garbage collected. You resolve this by unregistering the event listener or clearing the interval when the request finishes.

### Senior Architect
* **How would you debug a production Node.js memory leak that causes containers to restart every few hours? Walk through tools, profiling techniques, and analysis.**
  *Answer*: To debug a production memory leak:
  1. **Monitor Metrics**: Trace memory metrics in your dashboards (e.g. Prometheus). A saw-tooth memory chart (memory rises steadily, drops slightly during GC, and rises again until crash) confirms a memory leak.
  2. **Expose Debugger**: Run the Node.js process with the `--inspect` flag, or trigger diagnostic heap snapshots dynamically using the native `v8` module:
     ```javascript
     const v8 = require('v8');
     v8.writeHeapSnapshot(); // Generates a heap snapshot file
     ```
  3. **Compare Snapshots**: Take multiple heap snapshots under simulated load (e.g. after 100 requests, 1,000 requests, and 10,000 requests).
  4. **Analyze in Chrome DevTools**: Load the snapshots into Chrome DevTools Memory panel and perform a **Comparison** analysis:
     - Sort by the number of allocated objects (Delta).
     - Identify which constructors are growing in count (often strings, arrays, or system closure objects).
     - Inspect the **Retainers** tree path of the growing objects to identify which global variable, cache mapping, or event listener is holding the reference, and fix the leak in the code.

---
Previous : [50_Child_Processes.md] | Index : [00_index.md] | Next : [52_Garbage_Collection.md]
