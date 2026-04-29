# 📌 02 — Memory Management

## 🧠 Concept Explanation (Deep Technical Narrative)

JavaScript memory management is automatic — the developer doesn't call `malloc`/`free`. V8's garbage collector handles allocation and reclamation. But "automatic" doesn't mean "invisible" — understanding V8's memory model is essential for:
- Diagnosing memory leaks in production
- Optimizing allocation patterns to reduce GC pauses
- Understanding why certain code patterns are faster

V8's heap is divided into several **spaces**, each with different allocation strategies and GC behaviors:

| Space | Purpose | GC Type |
|-------|---------|---------|
| **New Space** (Young Generation) | Short-lived objects | Scavenge (minor GC) |
| **Old Space** | Long-lived objects | Mark-Compact (major GC) |
| **Code Space** | JIT-compiled bytecode/machine code | Mark-Compact |
| **Map Space** | Hidden classes (Maps/Shapes) | Mark-Compact |
| **Large Object Space** | Objects > 512KB | Individual, non-moved |

---

## 🔬 Internal Mechanics (Engine-Level — V8)

### New Space: Semi-Space Scavenger

New Space is split into two equal halves: **From-Space** and **To-Space**. Allocation is done by incrementing a pointer (a "bump pointer") into From-Space — extremely fast (comparable to stack allocation).

```
New Space Layout:
┌──────────────────────────────────────────────────────┐
│  FROM-SPACE                 │  TO-SPACE              │
│  ┌────────┬────────┬─────┐  │  ┌────────────────────┐│
│  │ obj A  │ obj B  │ ... │  │  │    (empty)         ││
│  └────────┴────────┴──┬──┘  │  └────────────────────┘│
│                        │    │                         │
│  Allocation pointer ───┘    │                         │
└──────────────────────────────────────────────────────┘
```

When From-Space fills, **Scavenge GC** runs:
1. Trace all live objects from roots (stack, globals, closures)
2. Copy live objects to To-Space (compacting them)
3. Update all pointers to new locations
4. Swap From-Space and To-Space
5. Dead objects in old From-Space are implicitly freed

Objects that survive **two scavenges** are **promoted to Old Space** — V8's heuristic for "this object is probably long-lived."

### Pointer Compression (V8 8.0+, Node.js 15+)

V8 compresses heap pointers from 64-bit to 32-bit by maintaining a "heap base" address. All heap pointers are stored as 32-bit offsets from the base. This:
- Reduces heap object size by ~40% for pointer-heavy objects
- Limits V8 heap to 4GB (base + 32-bit offset)
- Improves cache efficiency (more objects fit in L1/L2)

```
Without compression: each pointer = 8 bytes
With compression: each pointer = 4 bytes
JSObject with 4 properties: 80 bytes → 48 bytes (40% smaller)
```

### Write Barriers

When the GC moves objects (scavenging or compacting), all references must be updated. But V8 doesn't scan ALL old-space objects to find references to new-space objects on every minor GC — that would be too slow.

Instead, V8 uses a **write barrier**: every time old-space code writes a new-space pointer, V8 updates a **remembered set** that tracks which old-space slots contain new-space pointers. During scavenge, V8 only scans roots + the remembered set (not all of old-space).

```javascript
// This write triggers a write barrier in V8:
oldObject.child = newObject  // old → new pointer created
// V8's compiler inserts: RememberedSet.add(&oldObject.child)
```

Write barriers add small overhead to every object write in old-space — a necessary cost for generational GC correctness.

---

## 🔁 Execution Flow — Object Lifecycle

```
Allocation:
  new Foo()
    │
    ▼ V8: bump pointer in New Space From-Space
    
Young Object (New Space):
    │
    │ survives Scavenge 1 → still live at next minor GC
    │
    ▼ promoted after 2 survivors
    
Old Object (Old Space):
    │
    │ major GC cycle runs (incremental marking)
    │ object unreachable → not marked
    │
    ▼ swept (memory reclaimed)
    
Dead (freed):
    Memory slot returned to Old Space allocator
    (not immediately zeroed — next allocation overwrites)
```

---

## 🧠 Memory Behavior

```
V8 Heap Size Visualization (typical web app):

┌─────────────────────────────────────────────────────────────────┐
│ New Space: 1-8MB (small, frequent GC)                           │
│ ┌──────────┬──────────┐                                         │
│ │From-Space│ To-Space │                                         │
│ └──────────┴──────────┘                                         │
│                                                                 │
│ Old Space: 512MB+ (large, infrequent GC)                        │
│ ┌──────────────────────────────────────────────────────────┐   │
│ │  Long-lived objects, promoted closures, DOM nodes        │   │
│ └──────────────────────────────────────────────────────────┘   │
│                                                                 │
│ Code Space: varies (compiled JS code)                           │
│ Map Space: varies (hidden classes, ~fixed size per class)       │
│ Large Object Space: individual large allocations                │
└─────────────────────────────────────────────────────────────────┘

Node.js default heap limit: ~1.5GB (64-bit)
Browser: set by renderer process, typically 1-2GB
Increase: node --max-old-space-size=4096 (4GB)
```

---

## 📐 ASCII Diagram — Scavenge GC

```
BEFORE Scavenge:
FROM-SPACE: [A(live)] [B(dead)] [C(live)] [D(dead)] [E(live)]
TO-SPACE:   [empty                                           ]

AFTER Scavenge:
FROM-SPACE: [free (was A)] [free (was C)] [free (was E)]
TO-SPACE:   [A(copied)] [C(copied)] [E(copied)]

Pointers updated:
  Any reference to old-A's address → new-A's address in To-Space

THEN: swap from/to labels
New FROM-SPACE: [A] [C] [E]  (live, continue allocating here)
New TO-SPACE:   [empty]       (ready for next scavenge)

Objects surviving 2+ scavenges → PROMOTED to Old Space
```

---

## 🔍 Code Examples

### Example 1 — Allocation Rate Impact on GC

```javascript
// High allocation rate = frequent minor GC = GC pauses
function processList(items) {
  return items.map(item => ({  // Creates N new objects per call
    id: item.id,
    name: item.name.toUpperCase(),  // Creates N new strings
    processed: true
  }))
}

// Better: Reuse objects (object pooling)
class ObjectPool {
  constructor(factory, size = 100) {
    this.pool = Array.from({ length: size }, factory)
    this.index = 0
  }
  
  acquire() {
    return this.pool[this.index++ % this.pool.length]
  }
  
  release(obj) { /* reset obj properties */ }
}

// Or: mutate in place (if safe)
function processListInPlace(items) {
  for (const item of items) {
    item.name = item.name.toUpperCase()
    item.processed = true
  }
  return items
}
```

### Example 2 — Retained Size vs Shallow Size

```javascript
// Chrome DevTools terminology:
// Shallow size: memory occupied by the object itself (not what it references)
// Retained size: memory that would be freed if this object were GC'd
//                = object itself + exclusively referenced objects

const cache = new Map()
cache.set('key', {
  data: new Uint8Array(1024 * 1024),  // 1MB TypedArray
  metadata: { size: '1MB', compressed: false }
})

// cache shallow size: ~64 bytes (Map object header + internal slots)
// cache retained size: ~1MB + overhead (data array + metadata object)
// Because: cache → Map.entry → data array → only path to array
// If cache is GC'd, the 1MB array is also freed

// Important for leak detection:
// Objects with large retained size but small shallow size are
// often the ROOT of a leak (they hold many objects alive)
```

### Example 3 — String Interning and Memory

```javascript
// V8 interns (deduplicates) string literals and some computed strings
const s1 = 'hello'
const s2 = 'hello'
// s1 === s2 AND likely point to same heap string (interned)
// BUT: you cannot rely on this — it's an optimization

// Large string concatenation: allocates intermediate strings
let result = ''
for (let i = 0; i < 10000; i++) {
  result += 'x'  // Creates 10000 intermediate string objects!
  // V8 optimizes some of these away, but not all
}

// Better: array join (single allocation)
const parts = new Array(10000).fill('x')
result = parts.join('')  // ONE string allocation

// Template literals with complex interpolation:
const items = ['a', 'b', 'c']
const html = items.map(item => `<li>${item}</li>`).join('')  // Fewer allocs
```

### Example 4 — WeakRef and FinalizationRegistry

```javascript
// WeakRef: hold object without preventing GC
const cache = new Map()

class ResourceLoader {
  load(key) {
    const cached = cache.get(key)
    if (cached) {
      const value = cached.deref()  // null if GC'd
      if (value !== undefined) return value
    }
    
    const resource = this._loadExpensive(key)
    
    // WeakRef lets GC collect `resource` if memory pressure is high
    cache.set(key, new WeakRef(resource))
    
    // FinalizationRegistry: cleanup cache entry after GC
    registry.register(resource, key, resource)
    
    return resource
  }
  
  _loadExpensive(key) { /* ... */ }
}

const registry = new FinalizationRegistry(key => {
  cache.delete(key)
  console.log(`Cleaned up cache entry: ${key}`)
})

// Caveats:
// - FinalizationRegistry callback timing is non-deterministic
// - Not guaranteed to run (e.g., process termination)
// - Don't put critical cleanup logic here
// - Use for cache invalidation, logging, diagnostic purposes only
```

---

## 💥 Production Failures & Debugging

### Failure 1 — Memory Leak via Event Listener Accumulation

```javascript
// Node.js server: each request adds a 'data' listener to a stream
// without removing it when the request ends

http.createServer((req, res) => {
  const chunks = []
  
  // BUG: If this handler is called for an already-consumed stream,
  // the listener is added but never triggers, never removed
  req.on('data', chunk => chunks.push(chunk))
  req.on('end', () => {
    res.end(chunks.join(''))
  })
  
  // If req.on('error') is not handled: listener accumulates
  // Node.js emits MaxListenersExceededWarning at 10+ listeners
  
  // Fix: Always handle errors AND ensure cleanup
  req.on('error', (err) => {
    console.error(err)
    res.statusCode = 500
    res.end()
  })
}).listen(3000)
```

### Failure 2 — Old Space Pressure from Long-Lived Allocations

```javascript
// Production issue: in-memory session store leaking sessions
const sessions = {}

app.post('/login', (req, res) => {
  const sessionId = generateId()
  sessions[sessionId] = {
    user: req.body,
    createdAt: Date.now(),
    // sessions[sessionId] holds: user object, date, plus anything
    // stored during the session lifecycle
  }
  // NEVER expired! sessions grows unboundedly
})

// After 1 million logins: sessions object retains all user data
// V8 major GC runs more frequently, each run takes longer
// Node.js eventually OOMs or becomes very slow

// Fix: TTL-based expiry
setInterval(() => {
  const cutoff = Date.now() - 30 * 60 * 1000 // 30 min TTL
  Object.keys(sessions).forEach(key => {
    if (sessions[key].createdAt < cutoff) delete sessions[key]
  })
}, 60000) // Cleanup every minute
```

### Debugging Memory in Node.js

```bash
# 1. Heap snapshot at specific point
node -e "
const v8 = require('v8')
// ... run some code ...
v8.writeHeapSnapshot('./snapshot.heapsnapshot')
"

# 2. Memory usage tracking
node -e "
setInterval(() => {
  const mem = process.memoryUsage()
  console.log({
    rss: (mem.rss / 1024 / 1024).toFixed(1) + 'MB',      // Resident Set Size
    heapUsed: (mem.heapUsed / 1024 / 1024).toFixed(1) + 'MB',
    heapTotal: (mem.heapTotal / 1024 / 1024).toFixed(1) + 'MB',
    external: (mem.external / 1024 / 1024).toFixed(1) + 'MB'  // C++ objects
  })
}, 5000)
"

# 3. clinic.js for production profiling
npm install -g clinic
clinic heapprofile -- node app.js
```

---

## ⚠️ Edge Cases & Undefined Behaviors

### External Memory (C++ Objects via Native Addons)

```javascript
// Native addons (node-canvas, sharp, leveldb) allocate memory outside V8's heap
// This is tracked as `process.memoryUsage().external`
// V8's GC does NOT directly manage this memory

// If a native addon leaks C++ memory:
// - process.memoryUsage().heapUsed stays stable
// - process.memoryUsage().external grows
// - RSS grows

// The JS wrapper object has a `AdjustExternalMemory` call to hint V8
// about the external allocation size (so GC considers it for scheduling)
```

### ArrayBuffer Memory and GC Interaction

```javascript
// ArrayBuffer allocates its backing store in V8's ArrayBuffer allocator
// (not in the regular heap spaces)
const buf = new ArrayBuffer(100 * 1024 * 1024) // 100MB

// The JSArrayBuffer JS object is tiny (heap-tracked)
// The 100MB backing store is tracked separately
// process.memoryUsage().external shows the 100MB

// Transfer to Worker releases JS ownership:
const worker = new Worker('./worker.js')
worker.postMessage(buf, [buf]) // Transfer (zero-copy)
// buf.byteLength is now 0 in main thread
// Backing store moved to worker's C++ ArrayBuffer
```

---

## 🏢 Industry Best Practices

1. **Monitor `heapUsed` trend** — Growing `heapUsed` over time is a memory leak. Use monitoring tools (Datadog, New Relic) to alert on 80%+ heap utilization.

2. **Use object pools for hot-path objects** — Instead of creating and GCing thousands of objects per second, maintain a pool and reset objects for reuse.

3. **Avoid long-lived closures over large objects** — If you need a large dataset briefly, don't capture it in a closure that outlives the data's useful lifetime.

4. **Prefer `Buffer.allocUnsafe` over `Buffer.alloc` in Node.js for performance** — `allocUnsafe` skips zeroing; safe only if you fully initialize before reading.

5. **Set `--max-old-space-size` explicitly** — Don't rely on defaults. Production Node.js services should explicitly set heap limits based on container/pod memory limits.

---

## ⚖️ Trade-offs

| Strategy | Benefit | Cost |
|----------|---------|------|
| Object pooling | Reduces allocation rate, fewer GC pauses | Complexity, potential bugs if not reset |
| Generational GC | Fast for short-lived objects | Write barrier overhead |
| Pointer compression | Smaller heap, better cache performance | 4GB heap limit |
| WeakRef | Optional GC retention | Non-deterministic lifetime |
| External allocation (C++) | Bypasses V8 heap limits | Not managed by V8 GC |

---

## 💼 Interview Questions (With Solutions)

**Q1: What is the difference between Shallow Size and Retained Size in a heap snapshot?**

> Shallow size is the memory directly occupied by the object (its fields/slots). Retained size is the total memory that would be freed if that object were garbage collected — including all objects exclusively referenced by it (directly or transitively). For a Map object with 1000 entries pointing to 1MB objects each, the Map's shallow size might be 64 bytes but retained size is ~1GB. Retained size is the relevant metric for finding the root cause of memory leaks.

**Q2: Why do objects promoted to Old Space increase major GC frequency?**

> Major GC (Mark-Compact) must scan the entire Old Space, which grows over time. Each scan is proportional to the size of Old Space. More live objects in Old Space means more work per GC and more frequent GC to prevent OOM. Additionally, major GC causes significant GC pauses (though V8's incremental marking spreads this out). The goal is to minimize long-lived allocations and maximize object death in New Space (where scavenge is fast).

**Q3: What is a write barrier and why is it necessary for generational GC?**

> A write barrier is code inserted by the JIT compiler at every object write. When old-space code stores a pointer to a new-space object, the write barrier records this in a "remembered set." During minor GC (scavenge), V8 doesn't scan all of old-space to find references to new-space objects — that would be too slow. Instead, it only scans roots + the remembered set. Write barriers make this possible by tracking cross-generational pointers eagerly.

---

## 🧩 Practice Problems (With Solutions)

**Problem:** Write a function to detect whether V8 has promoted an object to Old Space:

```javascript
// Using V8's native syntax (development/testing only)
function isInOldSpace(obj) {
  // This requires --allow-natives-syntax flag
  // node --allow-natives-syntax
  return %GetHeapSpaceStatistics().some(space => 
    space.space_name === 'old_space' && /* complex check */
  )
}

// Practical approach: trigger promotion explicitly
function forcePromotion(obj) {
  // Run two minor GCs to promote to old space
  gc() // --expose-gc required
  gc()
  return obj
}

// Production approach: measure allocation count via PerformanceObserver
const obs = new PerformanceObserver((list) => {
  list.getEntries().forEach(entry => {
    if (entry.entryType === 'measure') {
      console.log(`GC: ${entry.name} took ${entry.duration}ms`)
    }
  })
})
obs.observe({ entryTypes: ['measure'] })
```

---

## 🔗 Navigation

**Prev:** [01_Deep_vs_Shallow_Copy.md](01_Deep_vs_Shallow_Copy.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [03_Garbage_Collection.md](03_Garbage_Collection.md)
