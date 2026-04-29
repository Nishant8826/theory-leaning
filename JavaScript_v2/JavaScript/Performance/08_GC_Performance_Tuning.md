# 📌 08 — GC Performance Tuning

## 🧠 Concept Explanation

(See also Advanced/03_Garbage_Collection.md for GC internals)

GC performance tuning focuses on reducing GC pause frequency and duration. Key strategies: reduce allocation rate, ensure objects die young (in New Space), and set appropriate heap limits.

## 🔍 Code Examples

### Measuring GC Impact

```javascript
const { PerformanceObserver } = require('perf_hooks')

// Track GC events
const obs = new PerformanceObserver((list) => {
  list.getEntries().forEach(entry => {
    if (entry.entryType === 'gc') {
      const gcTypes = { 1: 'scavenge', 2: 'mark-compact', 4: 'incremental', 8: 'weak-callbacks' }
      console.log(`GC [${gcTypes[entry.detail?.kind] || 'unknown'}] ${entry.duration.toFixed(2)}ms`)
      
      if (entry.duration > 50) {
        console.error(`Long GC pause: ${entry.duration.toFixed(1)}ms`)
        sendAlert('gc_pause', { duration: entry.duration })
      }
    }
  })
})
obs.observe({ entryTypes: ['gc'] })
```

### Object Pool Pattern (Reduce Allocation Rate)

```javascript
class VectorPool {
  constructor(poolSize = 1000) {
    this.pool = Array.from({ length: poolSize }, () => ({ x: 0, y: 0, z: 0 }))
    this.index = 0
  }
  
  acquire(x = 0, y = 0, z = 0) {
    const obj = this.pool[this.index++ % this.pool.length]
    obj.x = x; obj.y = y; obj.z = z
    return obj
  }
  // No release needed — circular pool overwrites old entries
}

const pool = new VectorPool()

// Physics engine hot loop:
for (let i = 0; i < particles.length; i++) {
  const velocity = pool.acquire(vx, vy, vz)  // Reused object, no GC pressure
  applyPhysics(particles[i], velocity)
}
```

### Allocation Rate Monitoring

```javascript
let lastHeapUsed = process.memoryUsage().heapUsed

setInterval(() => {
  const { heapUsed } = process.memoryUsage()
  const allocRate = (heapUsed - lastHeapUsed) / 1024 / 1024  // MB/sec
  lastHeapUsed = heapUsed
  
  if (Math.abs(allocRate) > 50) {  // >50MB/sec allocation
    console.warn(`High allocation rate: ${allocRate.toFixed(1)}MB/sec`)
  }
}, 1000)
```

## 🏢 Industry Best Practices

1. **Set heap limit** — `--max-old-space-size=512` for 512MB. OOM at known limit vs unpredictable crash.
2. **Profile before tuning** — Use `--heap-prof` to see where allocations come from.
3. **Prefer stack allocation** — Primitives and small value objects that don't escape are stack-allocated.
4. **Reduce string creation** — String concatenation in loops creates many short-lived strings.
5. **Use `Buffer.allocUnsafe`** — Skip zero-fill for performance-critical buffer creation.

## 💼 Interview Questions

**Q1: How does the `--max-old-space-size` flag affect GC behavior?**
> It sets the maximum old generation heap size. V8 scales its major GC frequency to try to stay under this limit. A larger limit: fewer, longer major GCs. A smaller limit: more frequent, shorter major GCs. In containerized environments, set this to 70-80% of the container's memory limit to leave room for other allocations (external memory, native modules, stack). Without this setting, V8 may try to use all available system RAM before GCing, causing OOM kills in containers.

## 🔗 Navigation

**Prev:** [07_Event_Loop_Blocking_UI.md](07_Event_Loop_Blocking_UI.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [../Interview/01_JS_Interview_Core.md](../Interview/01_JS_Interview_Core.md)
