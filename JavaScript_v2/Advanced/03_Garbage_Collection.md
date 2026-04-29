# 📌 03 — Garbage Collection

## 🧠 Concept Explanation

V8 uses **Orinoco** — a mostly-parallel, mostly-concurrent, incremental garbage collector. The key word is "mostly": the GC still requires stop-the-world pauses, but it minimizes their duration by doing most work concurrently with JS execution.

V8's GC has two main cycles:
- **Minor GC (Scavenge):** Collects the Young Generation (New Space). Fast, frequent (~1ms pauses).
- **Major GC (Mark-Compact):** Collects the entire heap. Slow, infrequent (~50-100ms without concurrency).

## 🔬 Orinoco Phases

### 1. Incremental Marking
Instead of pausing JS entirely to mark all live objects, V8 does marking in small increments (1-5ms) interleaved with JS execution. Uses a tri-color marking:
- **White:** Not yet visited (potentially dead)
- **Gray:** Discovered but children not yet scanned
- **Black:** Fully scanned (definitely live)

Write barriers ensure correctness: if a black object gets a new pointer to a white object during incremental marking, the write barrier re-grays the black object.

### 2. Concurrent Marking (V8 6.0+)
Background threads do marking work concurrently with the main JS thread. Main thread only needs a brief pause at the end to finalize marking.

### 3. Parallel Scavenge
Minor GC uses multiple threads to copy live objects from From-Space to To-Space in parallel.

### 4. Concurrent Sweeping
After marking, dead memory is reclaimed by background threads while JS resumes.

## 📐 ASCII Diagram — Major GC Timeline

`
JS THREAD:  ████░░░░█████░░█████████░░░░░████████
GC THREAD:  ────████████████████████████─────────

████ = JS running
░░░░ = stop-the-world pause (very short with incremental/concurrent)
──── = GC concurrent work

Old approach: one long pause
New Orinoco: many tiny pauses + background work
`

## 🔍 GC Triggering

GC is triggered when:
- New Space allocation fails (From-Space is full) → Minor GC
- Old Space reaches a threshold (grows over time) → Major GC
- External memory hint (AdjustExternalMemory) indicates pressure
- Idle time: V8 schedules GC during idle periods (idle-time GC)

`javascript
// Force GC in Node.js (debugging only)
// node --expose-gc
global.gc()  // Triggers GC immediately

// Monitor GC activity
const v8 = require('v8')
v8.setFlagsFromString('--trace-gc')
// Logs: [GC_TYPE] [HEAP_BEFORE]->[HEAP_AFTER] [DURATION]ms
`

## 💥 Production Failure — GC Pause Causing Request Timeouts

`javascript
// Symptom: 99th percentile latency spikes every ~30 seconds (major GC)
// Tool: clinic.js heapprofile shows stop-the-world pauses

// Root cause: large object graphs being promoted to old space
// Fix: 
// 1. Reduce allocation rate in hot paths
// 2. Set appropriate heap limits: --max-old-space-size=512
// 3. Use --optimize-for-size for memory-constrained environments
// 4. Monitor with: node --trace-gc --trace-gc-verbose

// Measure GC overhead:
const start = process.hrtime.bigint()
// ... run workload ...
const end = process.hrtime.bigint()

// Check if GC dominated:
// node --perf-basic-prof app.js  → linux perf can show GC time
`

## 🔬 GC Performance Tuning Flags

`ash
# Expose GC for manual control (dev/test only)
node --expose-gc app.js

# Increase old space for memory-heavy apps  
node --max-old-space-size=4096 app.js

# Tune GC aggressiveness
node --gc-interval=100 app.js  # More frequent minor GC

# Log GC events
node --trace-gc app.js

# Optimize for low memory (more aggressive GC, smaller heap)
node --optimize-for-size app.js
`

## ⚠️ Edge Cases

### GC and Finalizers (FinalizationRegistry)
`javascript
// FinalizationRegistry callbacks are NOT guaranteed to run
// V8 may skip them during abrupt process termination
// Don't use for critical cleanup (use explicit cleanup patterns instead)
const registry = new FinalizationRegistry(value => {
  // value = the held value (NOT the object itself — it's been GC'd)
  console.log('Cleaned up:', value)
})

let obj = { data: 'important' }
registry.register(obj, 'cleanup-key', obj)  // 3rd arg = unregister token
obj = null  // Now eligible for GC
// At some future GC: 'Cleaned up: cleanup-key' may log
`

### WeakMap and GC Interaction
`javascript
// WeakMap keys are held weakly — don't prevent GC
const weakMap = new WeakMap()
let obj = {}
weakMap.set(obj, 'metadata')
obj = null  // obj can now be GC'd; entry in weakMap disappears too

// Regular Map: key reference prevents GC
const map = new Map()
let obj2 = {}
map.set(obj2, 'metadata')
obj2 = null  // obj2 CANNOT be GC'd — map.keys() still holds reference!
`

## 🏢 Industry Best Practices

1. **Profile before optimizing** — Use clinic heapprofile or Chrome DevTools before manually tuning GC.
2. **Reduce object lifespan** — Objects that die young (in New Space) are cheapest to collect.
3. **Avoid object shape changes in hot code** — Shape changes force IC invalidation and can trigger unexpected allocations.
4. **Set explicit heap limits** — Containerized Node.js apps should set --max-old-space-size to 75-80% of container memory limit.

## ⚖️ Trade-offs

| GC Strategy | Throughput | Pause Latency | Footprint |
|------------|-----------|---------------|-----------|
| Stop-the-World | High | High | Low |
| Incremental | Medium | Low | Medium |
| Concurrent | Medium | Very Low | High (GC threads) |
| Generational | High | Low for minor | Medium |

## 💼 Interview Questions

**Q1: What is the write barrier and why is it needed for concurrent GC?**
> The write barrier is compiler-inserted code that runs on every object property write in old space. It maintains the tri-color invariant: a black (fully marked) object must not point to a white (unmarked) object. If concurrent marking has already marked an object black but JS code then adds a pointer to a new (white) object, the write barrier re-grays the object so the GC re-scans it. Without write barriers, concurrent marking would incorrectly collect live objects.

**Q2: Why do V8 GC pauses correlate with your 99th percentile request latency?**
> Stop-the-world pauses suspend ALL JavaScript execution — including your request handlers. A 50ms major GC pause adds 50ms to any request that was in-flight during the GC. The 99th percentile catches these tail latency events because GC runs periodically and affects ~1% of requests during heavy GC pressure. Solutions: reduce heap size (less to mark), reduce allocation rate (less frequent GC), use --max-old-space-size to control GC frequency.

## 🧩 Practice Problem

Implement an allocation rate monitor:
`javascript
class AllocationMonitor {
  constructor(sampleIntervalMs = 1000) {
    this.samples = []
    setInterval(() => {
      const mem = process.memoryUsage()
      this.samples.push({ time: Date.now(), heapUsed: mem.heapUsed })
      if (this.samples.length > 60) this.samples.shift()
      
      if (this.samples.length > 1) {
        const prev = this.samples[this.samples.length - 2]
        const delta = mem.heapUsed - prev.heapUsed
        if (delta > 10 * 1024 * 1024) { // >10MB/sec
          console.warn(High allocation rate: MB/sec)
        }
      }
    }, sampleIntervalMs)
  }
}
`

## 🔗 Navigation

**Prev:** [02_Memory_Management.md](02_Memory_Management.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [04_Concurrency_Model.md](04_Concurrency_Model.md)
