# 📌 05 — Worker Threads (Node.js)

## 🧠 Concept Explanation

Worker Threads differ from Cluster: Cluster creates **separate processes** (high isolation, separate heap, no shared memory). Worker Threads create **threads within the same process** (lower overhead, optional shared memory via SharedArrayBuffer).

Use Worker Threads for CPU-bound work that needs shared memory or lower startup overhead. Use Cluster for network-facing servers that need process isolation.

## 🔬 Key Differences from Cluster

| Feature | Cluster | Worker Threads |
|---------|---------|----------------|
| Type | Separate OS processes | OS threads, same process |
| Memory | Separate heaps | Separate heaps (opt-in sharing) |
| Startup | ~50-200ms | ~5-20ms |
| Communication | IPC (socket) | postMessage or SharedArrayBuffer |
| Shared State | No (use Redis) | SharedArrayBuffer + Atomics |
| Crash isolation | Yes (worker crash ≠ primary crash) | No (thread crash = process crash) |

## 🔍 Code Examples

### Example 1 — CPU-Bound Task Offloading

```javascript
// main.js
const { Worker } = require('worker_threads')

function runWorker(data) {
  return new Promise((resolve, reject) => {
    const worker = new Worker('./worker.js', {
      workerData: data,
      // resourceLimits for production safety:
      resourceLimits: {
        maxOldGenerationSizeMb: 256,  // Limit worker heap
        maxYoungGenerationSizeMb: 64,
        stackSizeMb: 4
      }
    })
    
    worker.on('message', resolve)
    worker.on('error', reject)
    worker.on('exit', code => {
      if (code !== 0) reject(new Error(`Worker exited with code ${code}`))
    })
  })
}

// worker.js
const { workerData, parentPort } = require('worker_threads')

function fibonacci(n) {
  if (n <= 1) return n
  return fibonacci(n - 1) + fibonacci(n - 2)  // CPU-intensive
}

const result = fibonacci(workerData.n)
parentPort.postMessage(result)
```

### Example 2 — Shared Buffer for Image Processing

```javascript
// main.js: Process image in worker, get result back without copying
const { Worker } = require('worker_threads')
const { createCanvas } = require('canvas')

async function applyFilterInWorker(imageBuffer) {
  // Create shared buffer (no copy on postMessage)
  const sharedBuffer = new SharedArrayBuffer(imageBuffer.byteLength)
  new Uint8Array(sharedBuffer).set(new Uint8Array(imageBuffer))
  
  const width = 800, height = 600  // Known dimensions
  
  await new Promise((resolve, reject) => {
    const worker = new Worker('./filter-worker.js')
    worker.postMessage({ sharedBuffer, width, height })
    worker.on('message', () => { resolve(); worker.terminate() })
    worker.on('error', reject)
  })
  
  // Workers modified sharedBuffer in place
  return Buffer.from(sharedBuffer)
}

// filter-worker.js
const { parentPort } = require('worker_threads')
parentPort.on('message', ({ sharedBuffer, width, height }) => {
  const pixels = new Uint8Array(sharedBuffer)
  
  // Apply grayscale filter in-place
  for (let i = 0; i < pixels.length; i += 4) {
    const avg = (pixels[i] + pixels[i+1] + pixels[i+2]) / 3
    pixels[i] = pixels[i+1] = pixels[i+2] = avg
  }
  
  parentPort.postMessage('done')  // Signal completion (data already in sharedBuffer)
})
```

## 💥 Production Failure

```javascript
// Worker thread crash propagates to main process
const { Worker } = require('worker_threads')

const worker = new Worker('./bad-worker.js')
// bad-worker.js: throw new Error('crash!') with no try/catch

// Unlike cluster workers: unhandled exception in Worker Thread
// DOES kill the entire process unless handled!

// Fix: always handle worker errors
worker.on('error', (err) => {
  console.error('Worker crashed:', err)
  // Don't let it propagate as uncaughtException
})
```

## 🏢 Industry Best Practices

1. **Use resourceLimits** — Prevent runaway workers from OOM-killing your process.
2. **Pool worker threads** — Creation overhead: ~5-20ms. Worth pooling for frequent tasks.
3. **Prefer `transferList`** — For large ArrayBuffers, always transfer rather than clone.
4. **Handle worker errors** — An unhandled error in a worker throws in the parent.
5. **Use `worker_threads` for CPU work** — PDF generation, image processing, complex calculations.

## 🔗 Navigation

**Prev:** [04_Cluster_Module.md](04_Cluster_Module.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [06_Middleware_Design.md](06_Middleware_Design.md)
