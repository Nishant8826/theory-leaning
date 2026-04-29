# 📌 02 — Memory Management: Heap, Stack, and Off-Heap Layouts

## 🧠 Concept Explanation

### Basic → Intermediate
Memory in Node.js is divided into the **Stack** (for primitives and local pointers) and the **Heap** (for objects and closures). V8 automatically manages the Heap using Garbage Collection.

### Advanced → Expert
At a staff level, we must understand the **V8 Heap Segmentation**. The heap is not a single block of memory; it is divided into distinct spaces:
1. **New Space (Young Generation)**: Where most objects are first allocated. It is small (typically 1MB-8MB) and optimized for fast allocation/cleanup.
2. **Old Space (Old Generation)**: Where objects that survived the New Space are promoted. This is where most long-lived data resides.
3. **Large Object Space**: For objects larger than the size of a "page" in other spaces. These are never moved during GC to avoid expensive copies.
4. **Code Space**: Where the JIT compiler stores the executable machine code.
5. **Map Space**: Stores the Hidden Classes (Shapes) of objects.

---

## 🏗️ Common Mental Model
"Everything in JavaScript is an object."
**Correction**: Primitives (numbers, booleans) are often stored "inline" on the **Stack** or inside the object itself (Smis - Small Integers) to avoid heap allocation overhead.

---

## ⚡ Actual Behavior: Off-Heap Memory
Node.js often works with data that is **NOT** in the V8 Heap. 
- **Buffers**: Allocated in the C++ layer using `malloc` or `calloc`. This memory is managed by Node.js, not V8.
- **Native Addons**: Can allocate arbitrary memory on the system heap.
This is why your process memory (RSS) might be 2GB while your JS Heap is only 200MB.

---

## 🔬 Internal Mechanics (V8 + libuv + syscalls)

### Semi-space allocation
The **New Space** is divided into two semi-spaces. Only one is used for allocation. When it's full, GC copies surviving objects to the other semi-space and flips them. This is called **Scavenging**.

### Memory Limits and RSS
- **RSS (Resident Set Size)**: The total memory the process occupies in RAM.
- **Heap Total**: Total size of the V8 Heap.
- **Heap Used**: Actual data in the Heap.

---

## 📐 ASCII Diagrams

### The V8 Heap Layout
```text
  ┌─────────────────────────────────────────────────────────────┐
  │                    PROCESS MEMORY (RSS)                     │
  │  ┌───────────────────────────────────────────────────────┐  │
  │  │                  V8 HEAP                             │  │
  │  │  ┌────────────┐  ┌────────────┐  ┌─────────────────┐ │  │
  │  │  │ NEW SPACE  │  │ OLD SPACE  │  │ LARGE OBJ SPACE │ │  │
  │  │  └────────────┘  └────────────┘  └─────────────────┘ │  │
  │  │  ┌────────────┐  ┌────────────┐                      │  │
  │  │  │ CODE SPACE │  │ MAP SPACE  │                      │  │
  │  │  └────────────┘  └────────────┘                      │  │
  │  └───────────────────────────────────────────────────────┘  │
  │  ┌───────────────────────────────────────────────────────┐  │
  │  │               OFF-HEAP / NATIVE                      │  │
  │  │  (Buffers, C++ Objects, Thread Pool, libuv handles)  │  │
  │  └───────────────────────────────────────────────────────┘  │
  └─────────────────────────────────────────────────────────────┘
```

---

## 🔍 Code Example: Monitoring Memory Segments
```javascript
const v8 = require('v8');

function printMemory() {
  const heapSpace = v8.getHeapSpaceStatistics();
  const memoryUsage = process.memoryUsage();
  
  console.log('--- Memory Snapshot ---');
  console.log(`RSS: ${Math.round(memoryUsage.rss / 1024 / 1024)} MB`);
  console.log(`External (Off-Heap): ${Math.round(memoryUsage.external / 1024 / 1024)} MB`);
  
  heapSpace.forEach(space => {
    console.log(`${space.space_name}: ${Math.round(space.space_used_size / 1024 / 1024)} MB / ${Math.round(space.space_size / 1024 / 1024)} MB`);
  });
}

setInterval(printMemory, 5000).unref();
```

---

## 💥 Production Failures & Debugging

### Scenario: The Buffer Leak (Off-Heap)
**Problem**: The process RSS keeps growing until the OS kills the process (OOM Killer), but the V8 Heap stays constant at 100MB.
**Reason**: You are creating `Buffer` objects in a loop but they are pinned by a global reference or a leak in a native C++ addon. V8 doesn't "see" this as heap pressure, so it doesn't trigger GC aggressively.
**Debug**: Use `process.memoryUsage().external`.
**Fix**: Ensure Buffers are nullified or their size is accounted for in your design.

---

## 🧪 Real-time Production Q&A

**Q: "What is a 'Zombie' object in V8?"**
**A**: It's an object that is no longer reachable by your code but hasn't been collected yet because the GC hasn't run. This is normal. A "leak" is when the object *remains* reachable by mistake (e.g. in a global array).

---

## 🧪 Debugging Toolchain
- **`node --inspect`**: Connect Chrome DevTools and take a **Heap Snapshot**.
- **`heapdump`**: Generate snapshots programmatically when memory hits a threshold.

---

## 🏢 Industry Best Practices
- **Avoid Global Variables**: They are the root of most memory leaks.
- **Use WeakMap/WeakSet**: For metadata that should be collected if the key object is no longer used elsewhere.

---

## 💼 Interview Questions
**Q: Why does Node.js have a memory limit?**
**A**: To ensure predictable GC pauses. A massive 64GB heap would take many seconds to clean, blocking the event loop and causing massive latency spikes. 

---

## 🧩 Practice Problems
1. Write a script that deliberately causes a "Heap OOM" and another that causes an "RSS OOM" (using Buffers). Compare the error messages.
2. Use `v8.getHeapSnapshot()` and explore the generated `.heapsnapshot` file in Chrome DevTools. Find the "path to root" for a specific variable.

---

**Prev:** [01_V8_Integration.md](./01_V8_Integration.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [03_Garbage_Collection.md](./03_Garbage_Collection.md)
