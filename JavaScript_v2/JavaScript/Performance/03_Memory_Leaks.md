# 📌 03 — Memory Leaks

## 🧠 Concept Explanation

A memory leak occurs when objects that are no longer needed remain reachable by the GC, preventing their collection. In JavaScript, leaks happen via unintentional references.

**Common leak sources:**
1. **Event listeners** not removed on component unmount
2. **Timers** (setInterval) referencing closures with large captured state
3. **Closures** capturing large objects unnecessarily
4. **Global variables** accumulating data
5. **DOM references** in JS while DOM nodes are removed from tree
6. **Caches** without eviction

## 🔬 Diagnosis Tools

### Chrome DevTools Memory Workflow

```
1. Baseline: Record heap snapshot before suspected leak
2. Trigger: Perform the action suspected to leak
3. After: Record second heap snapshot
4. Compare: Compare two snapshots ("Objects allocated between snapshots")
5. Identify: Look for objects with large "Retained Size" that shouldn't be there
6. Trace: Click object → Retainers panel shows who's keeping it alive
```

### Node.js Memory Monitoring

```javascript
const v8 = require('v8')

// Heap statistics
function logHeap(label) {
  const stats = v8.getHeapStatistics()
  console.log(`[${label}]`, {
    used: `${(stats.used_heap_size / 1024 / 1024).toFixed(1)}MB`,
    total: `${(stats.total_heap_size / 1024 / 1024).toFixed(1)}MB`,
    limit: `${(stats.heap_size_limit / 1024 / 1024).toFixed(1)}MB`
  })
}

// Detect leaks: take snapshots, compare
const inspector = require('inspector')
const session = new inspector.Session()
session.connect()

async function takeHeapSnapshot(filename) {
  const chunks = []
  session.on('HeapProfiler.addHeapSnapshotChunk', ({ params }) => {
    chunks.push(params.chunk)
  })
  
  await new Promise(resolve => session.post('HeapProfiler.takeHeapSnapshot', {}, resolve))
  
  require('fs').writeFileSync(filename, chunks.join(''))
  console.log(`Snapshot written to ${filename}`)
}

// Load in Chrome DevTools: Memory tab → Load profile
```

## 🔍 Code Examples

### Example 1 — Event Listener Leak

```javascript
// LEAK: Global event listener referencing large data
function initComponent() {
  const largeData = loadLargeDataset()  // 50MB
  
  // 'largeData' is captured in the closure!
  // Even if nothing else references largeData, the listener keeps it alive
  window.addEventListener('resize', () => {
    updateLayout(largeData)  // largeData captured
  })
  
  // Component is "destroyed" but window still holds the resize listener
  // largeData: 50MB retained forever
}

// Fix:
function initComponent() {
  const largeData = loadLargeDataset()
  
  const handler = () => updateLayout(largeData)
  window.addEventListener('resize', handler)
  
  // Return cleanup
  return () => window.removeEventListener('resize', handler)
}

const cleanup = initComponent()
// When component is destroyed:
cleanup()  // handler removed, largeData eligible for GC
```

### Example 2 — Timer Leak

```javascript
// LEAK: setInterval holding reference to large object
class MetricsCollector {
  constructor() {
    this.metrics = []  // Grows indefinitely
    
    // Timer holds reference to 'this' (via closure)
    // Even if MetricsCollector is "discarded", timer keeps it alive
    setInterval(() => {
      this.metrics.push(collectCurrentMetrics())
      // metrics grows: 1 entry/second × 86400 seconds = 86400 entries/day!
    }, 1000)
  }
}

// Fix:
class MetricsCollector {
  constructor() {
    this.metrics = []
    this._timer = setInterval(() => {
      this.metrics.push(collectCurrentMetrics())
      if (this.metrics.length > 1000) {
        this.metrics = this.metrics.slice(-500)  // Keep only recent 500
      }
    }, 1000)
  }
  
  destroy() {
    clearInterval(this._timer)  // Remove reference
    this.metrics = null
  }
}
```

### Example 3 — Detached DOM Node Leak

```javascript
// LEAK: Holding DOM references after removal from document
const removedNodes = []

document.querySelectorAll('.temporary').forEach(el => {
  removedNodes.push(el)  // Store reference
  el.remove()  // Remove from DOM
})

// el is removed from the document but NOT from memory!
// removedNodes keeps the entire el subtree alive (including event listeners!)

// Fix: Don't store references to DOM nodes you don't need
// Or: use WeakRef
const weakRefs = removedNodes.map(el => new WeakRef(el))
// Remove from removedNodes:
removedNodes.length = 0  // Now DOM nodes can be GC'd
```

### Example 4 — Cache Without Eviction

```javascript
// LEAK: Unbounded cache
const cache = new Map()

function getCachedUser(userId) {
  if (!cache.has(userId)) {
    cache.set(userId, fetchUser(userId))
  }
  return cache.get(userId)
}

// After 1 million unique users: cache has 1M entries, never freed

// Fix: LRU Cache with size limit
class LRUCache {
  constructor(maxSize = 1000) {
    this.maxSize = maxSize
    this.cache = new Map()  // Map maintains insertion order
  }
  
  get(key) {
    if (!this.cache.has(key)) return undefined
    const value = this.cache.get(key)
    this.cache.delete(key)
    this.cache.set(key, value)  // Move to end (most recently used)
    return value
  }
  
  set(key, value) {
    if (this.cache.has(key)) this.cache.delete(key)
    else if (this.cache.size >= this.maxSize) {
      this.cache.delete(this.cache.keys().next().value)  // Delete oldest
    }
    this.cache.set(key, value)
  }
}
```

## 💥 Production Failure — Express Route Handler Leak

```javascript
// Pattern: each request adds a listener that's never removed
app.get('/stream', (req, res) => {
  const stream = getDataStream()
  
  // 'data' listener captures res and stream
  stream.on('data', chunk => res.write(chunk))
  stream.on('end', () => res.end())
  
  // BUG: If client disconnects early:
  // stream is still live, 'data' handler still attached
  // stream is waiting for more data, holding res alive
  
  // Fix: Handle client disconnect
  req.on('close', () => {
    stream.destroy()  // This will remove listeners and allow GC
  })
})
```

## 🏢 Industry Best Practices

1. **Use `clinic heapprofile`** — Production-grade heap analysis.
2. **Set memory alerts** — Alert when heapUsed > 80% of max.
3. **Implement cleanup interfaces** — Every class that holds resources has `destroy()`.
4. **Use WeakMap/WeakSet for object associations** — Allow GC when key is unreachable.
5. **Bound all caches** — Never allow unbounded growth. Use LRU or TTL eviction.

## 💼 Interview Questions

**Q1: How do you identify a memory leak in a production Node.js application?**
> Steps: (1) Monitor `process.memoryUsage().heapUsed` over time — growing trend with no decrease = likely leak. (2) Take heap snapshots via `v8.writeHeapSnapshot()` or `--inspect` + Chrome DevTools at different times. (3) Compare snapshots: look for objects with large "Retained Size" that grew between snapshots. (4) Check "Retainers" panel: who's keeping these objects alive? (5) Common culprits: global arrays/maps growing without bounds, event listeners on long-lived objects, unclosed streams.

## 🔗 Navigation

**Prev:** [02_Reflow_and_Repaint.md](02_Reflow_and_Repaint.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [04_Lazy_Loading.md](04_Lazy_Loading.md)
