# 📌 03 — Garbage Collection: Scavenge, Mark-Compact, and Orinoco

## 🧠 Concept Explanation

### Basic → Intermediate
Garbage Collection (GC) is the process of finding memory that is no longer being used by the application and making it available for reuse. V8 uses an automatic GC so developers don't have to call `free()`.

### Advanced → Expert
V8 uses a **Generational, Stop-the-world, Parallel, and Concurrent** collector (Project **Orinoco**). 
1. **Generational**: Objects are split into Young (New Space) and Old (Old Space).
2. **Stop-the-world**: The main thread pauses while GC runs (though V8 minimizes this).
3. **Parallel**: GC work is split across multiple threads.
4. **Concurrent**: GC work happens while the main thread is still running JS.

The logic is: **"Most objects die young."** 

---

## 🏗️ Common Mental Model
"GC runs when I have no more memory."
**Correction**: GC runs based on **heuristics**. It might run because the New Space is half-full, or because it predicts that running a cleanup now will be faster than waiting.

---

## ⚡ Actual Behavior: The Two Collectors
1. **Minor GC (Scavenger)**: Cleans the New Space. It is frequent and very fast. It uses a "Cheney's Algorithm" to move live objects from one semi-space to another.
2. **Major GC (Full Mark-Compact)**: Cleans the Old Space. It is less frequent and more expensive. It marks reachable objects, sweeps away the dead ones, and compacts the memory to prevent fragmentation.

---

## 🔬 Internal Mechanics (V8 + libuv + syscalls)

### Marking
V8 starts from "Roots" (Global object, Stack) and follows every pointer to find "Live" objects. Any memory not reached is "Dead."

### The Write Barrier
When you update an object in the Old Space to point to an object in the New Space, V8 must track this so the Minor GC doesn't accidentally delete the new object. This is handled by a "Write Barrier" in the compiled code.

---

## 📐 ASCII Diagrams

### Scavenge (Minor GC)
```text
  SEMI-SPACE A (From)             SEMI-SPACE B (To)
  ┌─────────────┐                 ┌─────────────┐
  │ [Live Obj] ─┼────────────────▶│ [Live Obj]  │
  │ [Dead Obj]  │                 │             │
  │ [Live Obj] ─┼────────────────▶│ [Live Obj]  │
  │ [Dead Obj]  │                 │             │
  └─────────────┘                 └─────────────┘
                                   (Flip Spaces)
```

---

## 🔍 Code Example: Triggering GC for Testing
```javascript
// Run with node --expose-gc app.js

function createLeakyData() {
  const data = new Array(1e6).fill('leak');
  return () => console.log(data.length);
}

console.log('Pre-GC:', process.memoryUsage().heapUsed);

global.gc(); // Manually trigger GC (Do NOT use in production!)

console.log('Post-GC:', process.memoryUsage().heapUsed);
```

---

## 💥 Production Failures & Debugging

### Scenario: The GC Death Spiral
**Problem**: Your server latency increases exponentially. CPU is at 100%.
**Reason**: The Heap is 95% full. Every time a new object is created, V8 triggers a Major GC to find space. It only finds a tiny bit of space, so it triggers GC again almost immediately. The process is now spending 90% of its time on GC rather than JS code.
**Debug**: Use `node --trace-gc`. Look for lines with `Mark-compact` taking hundreds of milliseconds.
**Fix**: Increase `--max-old-space-size` or fix the memory leak.

---

## 🧪 Real-time Production Q&A

**Q: "What are 'Incremental' and 'Concurrent' GC?"**
**A**: **Incremental** means the GC work is broken into tiny slices so the event loop isn't blocked for long. **Concurrent** means the work happens on a background thread while your JS is running. V8 uses both to keep "Stop-the-world" pauses under 1ms.

---

## 🧪 Debugging Toolchain
- **`--trace-gc`**: Log every GC event to stdout.
- **`clinic.js bubbleprof`**: Visualize how GC pauses delay your event loop.

---

## 🏢 Industry Best Practices
- **Prefer short-lived objects**: They are cleaned up by the fast Minor GC.
- **Don't touch the GC flags**: Unless you have a very specific workload (e.g. CLI tools vs long-running servers).

---

## 💼 Interview Questions
**Q: What is memory fragmentation and how does V8 solve it?**
**A**: Fragmentation is when free memory is split into tiny, non-contiguous holes. V8 solves this during the **Compact** phase of Major GC, where it moves live objects together in memory to create large contiguous blocks of free space.

---

## 🧩 Practice Problems
1. Use `--trace-gc` and identify the difference between a "Scavenge" and a "Mark-sweep" in the output.
2. Build a "Memory Pressure" test. Keep adding objects to a global array until the process crashes. Observe the GC behavior right before the crash.

---

**Prev:** [02_Memory_Management.md](./02_Memory_Management.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [04_Worker_Threads.md](./04_Worker_Threads.md)
