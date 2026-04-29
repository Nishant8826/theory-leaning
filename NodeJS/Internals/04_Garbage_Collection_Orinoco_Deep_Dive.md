# 📌 04 — Garbage Collection: Project Orinoco Deep Dive

## 🧠 Concept Explanation

### Basic → Intermediate
Garbage Collection (GC) is the process of reclaiming memory that is no longer being used by the application. In V8, this happens automatically so developers don't have to manually manage memory.

### Advanced → Expert
At a staff level, we must understand **Project Orinoco**—the initiative to move GC work off the main thread to reduce "Stop-the-World" pauses.
1. **Parallelism**: Multiple threads doing the same GC task at once.
2. **Concurrency**: GC working in the background while the main JS thread is still running.
3. **Incrementality**: Breaking a large GC task into smaller chunks.

V8 uses a **Generational Strategy**:
- **Young Generation (Scavenge)**: Fast, frequent, handles short-lived objects (most objects die young).
- **Old Generation (Mark-Compact)**: Slower, handles long-lived objects.

---

## 🏗️ Common Mental Model
"GC stops my app from running."
**Correction**: In modern V8, the "Stop-the-World" pause is minimized. **Marking** (finding live objects) happens **Concurrently** in the background. Only the final **Sweeping** and **Compacting** (moving objects to defragment memory) require a short pause.

---

## ⚡ Actual Behavior: The "Write Barrier"
When GC is running concurrently in the background, your JS code might update an object's reference (e.g. `obj.a = b`). V8 uses a **Write Barrier** to notify the GC that the object graph has changed, ensuring that the background thread doesn't accidentally delete an object that is still alive.

---

## 🔬 Internal Mechanics (V8 GC)

### Minor GC (Scavenger)
Uses the **Cheney's Algorithm**. The Young Generation is split into two semi-spaces: **From-Space** and **To-Space**. 
1. New objects are allocated in From-Space.
2. When From-Space is full, live objects are copied to To-Space.
3. The spaces are swapped.
4. Objects that survive two scavenges are "promoted" to the Old Generation.

---

## 📐 ASCII Diagrams

### Concurrent Marking
```text
  MAIN THREAD:  [ JS ] [ JS ] [ JS ] [ PAUSE ] [ JS ]
                   │      │      │       │
  GC THREADS:      └──[ MARKING ]────────┴──[ SWEEP ]
                      (Background)        (Stop-the-world)
```

---

## 🔍 Code Example: Monitoring GC Events
```javascript
const { PerformanceObserver } = require('perf_hooks');

// Observe Garbage Collection events
const obs = new PerformanceObserver((list) => {
  const entry = list.getEntries()[0];
  console.log(`GC Event: ${entry.name}`);
  console.log(`Type: ${entry.kind}`);
  console.log(`Duration: ${entry.duration}ms`);
});

obs.observe({ entryTypes: ['gc'] });

// Trigger some GC activity
let data = [];
for (let i = 0; i < 1000000; i++) {
  data.push({ i });
  if (i % 100000 === 0) data = []; // Make objects unreachable
}
```

---

## 💥 Production Failures & Debugging

### Scenario: The "Major GC" Latency Spike
**Problem**: Every few minutes, the p99 latency of your app spikes from 50ms to 500ms.
**Reason**: The Old Generation is full, and V8 is performing a full **Mark-Compact** cycle. Even with concurrency, a large heap (e.g. 4GB) requires a significant pause to compact memory.
**Fix**: Tune `--max-old-space-size` or use multiple smaller Node.js processes instead of one giant one.

### Scenario: High Allocation Rate
**Problem**: The CPU is at 80% even though there is zero traffic.
**Reason**: Your code is creating and discarding thousands of small objects in a loop (e.g. inside a logger or a parser). The Scavenger GC is running constantly to clean up the mess.
**Fix**: Reuse objects where possible or use **Object Pools**.

---

## 🧪 Real-time Production Q&A

**Q: "Should I call `global.gc()` manually?"**
**A**: **Almost never.** Calling GC manually blocks the event loop and interferes with V8's sophisticated internal scheduling. Only use it for debugging or in specific background worker tasks that you know are finished.

---

## 🧪 Debugging Toolchain
- **`node --trace-gc`**: Log every GC event to the console.
- **`node --trace-gc-verbose`**: Detailed breakdown of heap spaces.

---

## 🏢 Industry Best Practices
- **Prefer short-lived objects**: They are cleaned up very efficiently by the Scavenger.
- **Avoid large "God" objects**: Objects that stay alive forever in the Old Generation increase the cost of every Mark-Compact cycle.

---

## 💼 Interview Questions
**Q: What is "Fragmentation" in the heap and how does V8 solve it?**
**A**: Fragmentation is when free memory is split into small, non-contiguous holes. V8 solves this during the **Mark-Compact** phase by moving live objects together (compacting) to create large blocks of free space.

---

## 🧩 Practice Problems
1. Use `--trace-gc` and identify the difference in duration between a `Scavenge` and a `Mark-sweep`.
2. Write a script that fills the heap until it triggers a full GC. Measure how the Event Loop Lag increases during that time.

---

**Prev:** [03_Memory_Layout_Smi_Doubles_Elements.md](./03_Memory_Layout_Smi_Doubles_Elements.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [05_The_C_Boundary_NAPI_Internals.md](./05_The_C_Boundary_NAPI_Internals.md)
