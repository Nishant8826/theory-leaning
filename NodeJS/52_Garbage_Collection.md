# Garbage Collection

## What You Will Learn
* The Generational Hypothesis behind V8's memory reclaim strategies.
* How the **Scavenger** (Minor GC) collects memory in the Young Generation.
* How the **Mark-Sweep-Compact** (Major GC) collects memory in the Old Generation.
* Orinoco project optimizations: Incremental, Parallel, and Concurrent collection.
* Tuning GC performance using V8 CLI flags (`--trace-gc`, `--max-old-space-size`).

## Why This Matters
JavaScript abstracts memory management, but high-throughput servers cannot treat the Garbage Collector as a black box. If your application creates too many short-lived objects, the garbage collector will run frequently, causing "Stop-The-World" pauses that freeze the main thread. Understanding how V8 reclaims memory allows you to write GC-friendly code that keeps latency low.

## Theory

### The Generational Hypothesis
V8's garbage collection strategy is based on the **Generational Hypothesis**: most objects die shortly after allocation (e.g. variables inside function scopes are reclaimed immediately when the function returns). 

To optimize cleanup, V8 divides the heap into two generations:
1. **Young Generation (New Space)**: A small, high-speed buffer (typically 16-64MB) where all new objects are initially allocated.
2. **Old Generation (Old Space)**: A larger memory space where objects that survive multiple garbage collection runs in the Young Generation are promoted.

## Deep Dive

### The Two V8 Garbage Collectors
V8 utilizes two different collectors to manage these spaces:

#### 1. Minor GC: The Scavenger (Cheney's Copying Algorithm)
* **Goal**: Reclaim memory in the New Space.
* **Mechanism**: The New Space is divided into two equal semi-spaces: **From-Space** and **To-Space**.
  * New objects are written to the From-Space.
  * When the From-Space fills up, V8 runs the Scavenger.
  * It traces active object roots and copies surviving objects to the To-Space, keeping them contiguous to prevent fragmentation.
  * Any objects that survive multiple Scavenger runs are promoted to the Old Space.
  * The names of the spaces are flipped (From becomes To, and vice versa), and the memory is reclaimed.
* **Performance**: Extremely fast (takes 1-5ms) because it only copies surviving objects and ignores dead ones.

#### 2. Major GC: Mark-Sweep-Compact
* **Goal**: Reclaim memory in the Old Space.
* **Mechanism**:
  * **Marking**: V8 traverses the object reference tree starting from the roots (global variables, active execution frames) to identify and mark all reachable (active) objects.
  * **Sweeping**: V8 scans the heap and adds the memory addresses of unmarked (dead) objects to a "free list" to be reused for future allocations.
  * **Compacting**: V8 moves surviving objects to contiguous memory locations to fix memory fragmentation, keeping memory access fast.
* **Performance**: Slower (takes 50-500ms) because it must scan the entire heap, which can block the main thread.

### Orinoco Optimizations (Non-blocking GC)
To prevent long "Stop-The-World" pauses, the V8 team introduced the **Orinoco** garbage collector, which implements several optimization patterns:
* **Parallel Collection**: Multiple background threads assist the main thread during GC sweeps, reducing pause times.
* **Incremental Marking**: V8 splits the marking phase into small steps, running them in between JavaScript execution blocks to prevent long pauses.
* **Concurrent Sweeping**: Background threads sweep and compact memory while the main thread continues running JavaScript, eliminating pause latency.

## Visual Explanation

### Cheney's Scavenger Copying Algorithm (New Space)
```text
State 1: From-Space fills up
From-Space: [ Obj 1 (Active) ] [ Obj 2 (Dead) ] [ Obj 3 (Active) ]
To-Space:   [                ] [                ] [                ] (Empty)

State 2: Scavenger runs (Copy active objects)
From-Space: [ Obj 1 (Active) ] [ Obj 2 (Dead) ] [ Obj 3 (Active) ]
To-Space:   [ Obj 1 (Active) ] [ Obj 3 (Active) ] [                ] (Compacted)

State 3: Flip spaces & reclaim From-Space
New From-Space (Old To-Space):   [ Obj 1 (Active) ] [ Obj 3 (Active) ]
New To-Space (Old From-Space):   [                ] [                ] (Cleared & ready)
```

## Real-World Example
Suppose you run an API that processes large JSON arrays. If you write your processing logic using loops that create many temporary helper objects, you will trigger frequent Scavenger runs. If the objects survive because they are stored in arrays, they will be promoted to the Old Space, eventually triggering Major GC runs that freeze the server, causing latency spikes for clients.

## Code Examples

### Tracking Garbage Collection Cycles using CLI flags
You cannot force V8 to run garbage collection in standard JS code (unless running with specific flags). However, you can monitor GC behavior using V8 CLI flags:

```bash
# 1. Start your Node.js application and print detailed GC statistics to stdout
# Prints lines like: [14202:0x103008000] 10 ms: Scavenge 2.4 -> 1.2 MB
node --trace-gc app.js

# 2. Print GC statistics along with detailed heap space layouts
node --trace-gc-verbose app.js

# 3. Configure the maximum memory allocation limit of the V8 Old Space
# Useful for running Node.js in low-memory environments (like 512MB containers)
node --max-old-space-size=400 app.js
```

### Programmatically Monitoring GC Events using `perf_hooks`

```javascript
// monitor-gc.js
const { PerformanceObserver } = require('perf_hooks');

// Initialize observer for garbage collection events
const obs = new PerformanceObserver((list) => {
  const entry = list.getEntries()[0];
  console.log(`[GC EVENT] Type: ${entry.detail.kind} | Duration: ${entry.duration.toFixed(2)}ms`);
  
  // GC Kinds:
  // 1: Scavenge (Minor GC - Young Generation)
  // 2: Mark-Sweep-Compact (Major GC - Old Generation)
  // 4: Incremental Marking
});

// Subscribe to garbage collection performance metrics
obs.observe({ entryTypes: ['gc'] });

// Trigger allocations to force GC cycles
const objects = [];
console.log('Generating heap allocations...');
setInterval(() => {
  for (let i = 0; i < 10000; i++) {
    objects.push({ data: new Array(100).fill('leak-item') });
  }
  // Remove references to allow Scavenger to collect them
  if (objects.length > 500000) {
    objects.length = 0;
  }
}, 50);
```

## Best Practices
* **Tune `--max-old-space-size`**: Always set this flag in containerized environments (like Docker containers running under Kubernetes memory limits) to prevent V8 from allocating more memory than the container limit, which triggers OS OOM-killer crashes.
* **Reuse Object Instances**: Avoid creating unnecessary temporary objects in hot code paths. Reuse buffers or use object pools where appropriate to reduce GC pressure.
* **Limit Global variables**: Keep global scopes clean to ensure objects are marked as unreachable and garbage collected quickly.

## Interview Questions

### Beginner
* **What is Garbage Collection in JavaScript?**
  *Answer*: Garbage Collection is an automatic memory management process in the JavaScript engine (V8) that identifies and reclaims memory allocated to objects that are no longer referenced or reachable from the application roots.

### Intermediate
* **What is the Generational Hypothesis, and how does it affect V8's heap structure?**
  *Answer*: The Generational Hypothesis states that most objects die shortly after allocation. To optimize cleanup based on this rule, V8 divides the heap into two spaces: the Young Generation (New Space, for new, short-lived objects) and the Old Generation (Old Space, for long-lived objects promoted from the New Space).

### Advanced
* **Explain Cheney's Scavenger copying algorithm used in the V8 New Space.**
  *Answer*: Cheney's copying algorithm divides the New Space into two equal semi-spaces: From-Space and To-Space. 
  1. New objects are allocated in the From-Space.
  2. When the From-Space fills up, the Scavenger pauses execution to find active, reachable objects.
  3. It copies the active objects to the To-Space, compacting them to prevent memory fragmentation.
  4. Any objects that survive multiple Scavenger runs are promoted to the Old Space.
  5. The names of the semi-spaces are flipped, and the old From-Space is cleared, ready for new allocations.

### Senior Architect
* **Discuss how Orinoco optimizes V8 garbage collection to minimize Stop-The-World latency. Explain the difference between concurrent, parallel, and incremental garbage collection.**
  *Answer*: To minimize Stop-The-World latency, Orinoco implements several non-blocking collection patterns:
  * **Parallel Collection**: The main thread and multiple background worker threads perform GC tasks simultaneously. While this still pauses JavaScript execution (Stop-The-World), sharing the workload across multiple threads reduces the pause duration.
  * **Incremental Collection**: The main thread runs GC tasks in small, interleaved steps between JavaScript execution cycles. This does not reduce the total GC workload, but it breaks a single long pause into multiple short pauses, keeping the application responsive.
  * **Concurrent Collection**: Background helper threads perform the entire GC cycle (like marking or sweeping) while the main thread continues executing JavaScript. This is the most efficient pattern because it eliminates Stop-The-World pauses on the main thread entirely.

---
Previous : [51_Memory_Management.md] | Index : [00_index.md] | Next : [53_Performance_Optimization.md]
