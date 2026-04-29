# 📌 07 — Web Workers

## 🧠 Concept Explanation

Web Workers enable true parallel execution in the browser by running JavaScript in background threads. Each worker is a separate OS thread with its own V8 Isolate, event loop, and heap — completely isolated from the main thread.

**Types:**
- **Dedicated Workers** — One-to-one with creating page
- **Shared Workers** — Shared across multiple pages/tabs from same origin
- **Service Workers** — Network proxy (covered in 04_Service_Workers.md)

## 🔬 Internal Mechanics

### Worker Creation Cost

Creating a Worker is expensive (~10-50ms):
1. OS thread creation
2. New V8 Isolate initialization
3. New event loop setup
4. Worker script download + parse + evaluate

**Always pool workers!** Don't create a new worker per task.

### postMessage and Structured Clone

Default data transfer uses structured clone (serialization copy):
```
Main Thread → [serialize data] → [copy bytes] → Worker → [deserialize]
              ↑ CPU cost for large objects       ↑ CPU cost
```

Transferables (zero-copy):
```
Main Thread → [transfer ownership] → Worker
              No copy — pointer moved
              Original detached (ArrayBuffer.byteLength = 0)
```

### Memory Isolation

Workers have completely separate heaps:
- Variables in worker don't affect main thread
- GC in worker is independent of main thread GC
- Large allocations in worker don't show in main thread's process.memoryUsage().heapUsed... but DO show in OS-level RSS

## 📐 ASCII Diagram

```
Main Thread (V8 Isolate A)         Worker (V8 Isolate B)
┌─────────────────────────┐        ┌─────────────────────────┐
│  DOM access             │        │  No DOM access           │
│  Event Loop             │        │  Own Event Loop          │
│  V8 Heap                │        │  Own V8 Heap             │
│  Global: window         │        │  Global: self (WorkerGS) │
└──────────┬──────────────┘        └────────────┬────────────┘
           │ postMessage(data)                   │
           │ ────────────────────────────────►  │
           │ (structured clone or transfer)      │ onmessage
           │                                    │
           │◄──────────────────────────────────  │
           │ onmessage                           │ postMessage(result)
```

## 🔍 Code Examples

### Example 1 — Worker Pool Pattern

```javascript
// worker-pool.js (main thread)
class WorkerPool {
  constructor(workerScript, poolSize = navigator.hardwareConcurrency || 4) {
    this.workers = []
    this.taskQueue = []
    this.nextTaskId = 0
    this.pendingTasks = new Map()
    
    for (let i = 0; i < poolSize; i++) {
      const worker = new Worker(workerScript)
      worker.onmessage = ({ data }) => {
        const { taskId, result, error } = data
        const { resolve, reject } = this.pendingTasks.get(taskId)
        this.pendingTasks.delete(taskId)
        worker._busy = false
        if (error) reject(new Error(error))
        else resolve(result)
        this._processQueue()
      }
      worker._busy = false
      this.workers.push(worker)
    }
  }
  
  run(data) {
    return new Promise((resolve, reject) => {
      const taskId = ++this.nextTaskId
      this.pendingTasks.set(taskId, { resolve, reject })
      
      const available = this.workers.find(w => !w._busy)
      if (available) {
        available._busy = true
        available.postMessage({ taskId, data })
      } else {
        this.taskQueue.push({ taskId, data })
      }
    })
  }
  
  _processQueue() {
    if (!this.taskQueue.length) return
    const available = this.workers.find(w => !w._busy)
    if (!available) return
    const { taskId, data } = this.taskQueue.shift()
    available._busy = true
    available.postMessage({ taskId, data })
  }
  
  terminate() {
    this.workers.forEach(w => w.terminate())
  }
}

// worker.js (worker script)
self.onmessage = ({ data: { taskId, data } }) => {
  try {
    const result = heavyComputation(data)
    self.postMessage({ taskId, result })
  } catch(e) {
    self.postMessage({ taskId, error: e.message })
  }
}
```

### Example 2 — Transfer Large Data (Zero-Copy)

```javascript
// Process large image data in worker without cloning
async function processImage(imageData) {
  const worker = new Worker('./image-processor.js')
  
  // Create transferable buffer from canvas ImageData
  const buffer = imageData.data.buffer.slice(0)  // ArrayBuffer
  
  return new Promise((resolve, reject) => {
    worker.onmessage = ({ data }) => {
      // Receive processed buffer back
      const processedData = new Uint8ClampedArray(data.buffer)
      resolve(new ImageData(processedData, imageData.width, imageData.height))
      worker.terminate()
    }
    
    // Transfer: zero copy! buffer.byteLength = 0 after this
    worker.postMessage({ buffer, width: imageData.width }, [buffer])
  })
}

// image-processor.js
self.onmessage = ({ data: { buffer, width } }) => {
  const pixels = new Uint8ClampedArray(buffer)
  
  // Invert colors in-place
  for (let i = 0; i < pixels.length; i += 4) {
    pixels[i]     = 255 - pixels[i]     // R
    pixels[i + 1] = 255 - pixels[i + 1] // G
    pixels[i + 2] = 255 - pixels[i + 2] // B
    // Alpha unchanged
  }
  
  // Transfer processed buffer back (zero-copy)
  self.postMessage({ buffer: pixels.buffer }, [pixels.buffer])
}
```

### Example 3 — Shared Workers (Cross-Tab State)

```javascript
// shared-worker.js
const connections = []
let sharedState = { count: 0 }

self.onconnect = ({ ports }) => {
  const port = ports[0]
  connections.push(port)
  
  port.onmessage = ({ data }) => {
    switch(data.type) {
      case 'INCREMENT':
        sharedState.count++
        broadcast({ type: 'STATE_UPDATE', state: sharedState })
        break
      case 'GET_STATE':
        port.postMessage({ type: 'STATE_UPDATE', state: sharedState })
        break
    }
  }
  
  port.start()
  port.postMessage({ type: 'STATE_UPDATE', state: sharedState })
}

function broadcast(message) {
  connections.forEach(p => p.postMessage(message))
}

// Main thread (any tab):
const worker = new SharedWorker('./shared-worker.js')
worker.port.start()
worker.port.onmessage = ({ data }) => {
  if (data.type === 'STATE_UPDATE') {
    updateUI(data.state)
  }
}
worker.port.postMessage({ type: 'INCREMENT' })
```

## 💥 Production Failures

### Failure — Worker Not Terminated (Memory Leak)

```javascript
// Anti-pattern: creating workers without terminating them
async function processEachItem(items) {
  for (const item of items) {
    const worker = new Worker('./processor.js')  // New worker per item!
    await new Promise(resolve => {
      worker.onmessage = ({ data }) => { resolve(data); /* MISSING: worker.terminate() */ }
      worker.postMessage(item)
    })
    // Worker continues running after task! Memory leak.
    // 1000 items = 1000 zombie workers
  }
}

// Fix: Always terminate or use a pool
```

### Failure — Serialization Bottleneck

```javascript
// Posting large objects without measuring serialization cost
const hugeDataset = generateMillionRecords()  // 100MB object graph

worker.postMessage(hugeDataset)
// Structured clone of 100MB object: 500ms-2s blocking main thread!
// The clone happens synchronously in the main thread

// Fix: Design data transfer carefully
// - Use ArrayBuffer/TypedArray for numeric data (fast serialization)
// - Transfer instead of clone when possible
// - Stream data in chunks via multiple postMessage calls
```

## ⚠️ Edge Cases

### Workers Cannot Use DOM APIs

```javascript
// Inside a worker:
document.getElementById('app')  // ReferenceError: document is not defined
window.location                 // ReferenceError: window is not defined
fetch('/api/data')              // WORKS! fetch is available in workers
console.log('test')             // WORKS!
performance.now()               // WORKS!
crypto.getRandomValues(...)     // WORKS!
importScripts('./lib.js')       // WORKS! (classic workers only)
```

### Worker Error Handling

```javascript
const worker = new Worker('./heavy.js')
worker.onerror = (errorEvent) => {
  console.error('Worker error:', errorEvent.message, errorEvent.filename, errorEvent.lineno)
  // errorEvent.preventDefault() - prevent default error in console
}

// Unhandled rejections in workers (Chrome 70+):
worker.onmessageerror = (event) => {
  console.error('Message deserialization error:', event)
}
```

## 🏢 Industry Best Practices

1. **Pool workers** — Creation overhead is significant. Pool based on `navigator.hardwareConcurrency`.
2. **Transfer large buffers** — Never clone large ArrayBuffers. Use transfer list.
3. **Terminate when done** — `worker.terminate()` or `self.close()` inside worker.
4. **Chunk large data** — Don't serialize millions of records at once. Stream in chunks.
5. **Use module workers** — `new Worker('./w.js', { type: 'module' })` for ESM in workers.

## 💼 Interview Questions

**Q1: Why can't Web Workers access the DOM?**
> The DOM is not thread-safe. Allowing concurrent access to the DOM from multiple threads would require complex locking and could cause race conditions in the rendering pipeline. The browser's design decision: workers are completely isolated from the DOM, communicating only via message passing. This keeps the threading model simple and deterministic. If workers need DOM-like operations, they use OffscreenCanvas or postMessage results back to the main thread.

**Q2: What is the difference between postMessage clone and transfer?**
> Clone (default): the data is serialized using structured clone, memory is copied, and a new independent copy is created in the destination thread. Expensive for large data (~1MB/ms for serialization). Transfer: the underlying memory ownership is moved from source to destination. No copying — the ArrayBuffer's backing store pointer is simply moved. The source object becomes detached (byteLength = 0). Zero-copy but destructive.

## 🔗 Navigation

**Prev:** [06_CORS.md](06_CORS.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [08_Intersection_Observer_and_Performance.md](08_Intersection_Observer_and_Performance.md)
