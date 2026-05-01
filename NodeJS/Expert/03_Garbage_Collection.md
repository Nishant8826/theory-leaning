# 📌 Topic: Garbage Collection (Orinoco)

## What
### 🧠 Concept Explanation
Garbage Collection is like a **Janitorial Staff in a Hotel**.
**Analogy:** 
- **Young Generation (The Lobby):** Guests (objects) arrive and leave quickly. The janitors (Scavenger GC) clean the lobby every few minutes because most people don't stay long.
- **Old Generation (The Rooms):** Guests who stay for a long time are moved to rooms. The janitors (Major GC) clean these rooms less often because it's a big, slow job.
- **Mark-Sweep-Compact:** The janitor walks through the rooms, marks who is still there, kicks out the ghosts, and then pushes all the remaining guests together so there are no empty gaps between rooms (Compaction).

---

### 🏗️ Mental Model
V8 uses a **Generational Garbage Collector**. It assumes that "most objects die young."
1.  **New Space (Young Generation):** Where new objects are allocated. Small (usually 1MB-64MB) and very fast to clean.
2.  **Old Space (Old Generation):** Where long-lived objects are moved. Large and more expensive to clean.

---

## Why
### 🏢 Best Practices
1.  **Don't create global variables:** They are roots and will never be collected.
2.  **Nullify references:** If you have a large object you no longer need, set it to `null`.
3.  **Use Streams:** To avoid loading huge datasets into the heap in the first place.

---

### ⚖️ Trade-offs
*   **Generational GC:** Very efficient for most JS patterns but adds complexity (write barriers) and uses more memory (semi-space) than simpler collectors.

---

## How
### ⚡ Actual Behavior
*   **Stop-the-world:** Historically, GC stopped everything. Modern V8 uses **Parallel**, **Incremental**, and **Concurrent** marking to avoid pausing the main thread for more than a few milliseconds.
*   **Weak Generational Hypothesis:** Objects that survive two "Scavenge" cycles are "promoted" to the Old Space.

---

### 🔬 Internal Mechanics (V8 + libuv + OS)
*   **Scavenge (Minor GC):** Uses "Semi-space" allocation. It copies live objects from one half of the New Space to the other, then clears the first half.
*   **Mark-Sweep-Compact (Major GC):** 
    1.  **Marking:** Traverse the heap from "roots" (global variables) to find all reachable objects.
    2.  **Sweeping:** Clear the memory of unreachable objects.
    3.  **Compacting:** Move objects together to prevent memory fragmentation.
*   **Write Barriers:** V8 uses these to track pointers from Old Space back to New Space so it doesn't accidentally delete young objects that are still being used by old ones.

---

### 🔁 Execution Flow
1.  App creates a new object. It goes into the "From-Space" of the New Generation.
2.  New Generation fills up.
3.  **Scavenge Cycle:** Live objects are copied to "To-Space".
4.  "From" and "To" spaces are swapped.
5.  If object survives another cycle, it is moved to the Old Generation.
6.  Old Generation reaches a threshold -> **Major GC** starts.

---

### 🔍 Code Example (Latest Node.js - Forcing GC for Testing)
```javascript
// Run with: node --expose-gc script.js
import { inspect } from 'node:util';

function getMemoryUsage() {
  const usage = process.memoryUsage();
  return `Heap Used: ${(usage.heapUsed / 1024 / 1024).toFixed(2)} MB`;
}

console.log('1. Initial:', getMemoryUsage());

let data = new Array(1000000).fill({ text: 'Heavy Object' });
console.log('2. After Allocation:', getMemoryUsage());

data = null; // Remove reference
console.log('3. Before GC:', getMemoryUsage());

if (global.gc) {
  global.gc(); // Force Garbage Collection
  console.log('4. After GC:', getMemoryUsage());
} else {
  console.log('GC not exposed. Use --expose-gc');
}
```

---

## Impact
### 💥 Production Failures
*   **Memory Leaks:** Keeping references to objects in a global array or closure, preventing the "Marking" phase from ever identifying them as garbage.
*   **Large Object Space (LOS):** Massive objects (like huge strings or buffers) go directly to a special space that is only cleaned during Major GC, causing performance issues.

---

### 🧪 Real-time Scenarios
*   **High-Volume APIs:** Thousands of short-lived objects (request/response metadata) are handled efficiently by the New Space Scavenger.
*   **Long-lived Caches:** In-memory caches reside in the Old Space and can cause slow "Stop-the-world" pauses if they grow too large.

---

### ⚠️ Edge Cases
*   **Closures:** A closure can keep a large parent scope alive in memory even if it only needs one tiny variable.
*   **Hidden Classes:** If you have millions of objects with different shapes, V8's metadata for those hidden classes can consume significant memory.

---

---

Prev: [02_Libuv_and_Threadpool.md](./02_Libuv_and_Threadpool.md) | Index: [NodeJS/00_Index.md](../00_Index.md) | Next: [04_Event_Loop_Phases.md](./04_Event_Loop_Phases.md)
