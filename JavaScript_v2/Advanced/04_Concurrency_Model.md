# 📌 04 — Concurrency Model

## 🧠 Concept Explanation

JavaScript is single-threaded but not single-process. The **JS single-thread illusion** holds within one execution context (one JS thread), but actual parallelism is achieved through:

1. **Web Workers / Worker Threads** — True parallel JS execution in separate threads
2. **SharedArrayBuffer + Atomics** — Shared memory between threads
3. **The browser's multi-process architecture** — Compositor thread, network thread, etc.

Understanding the boundaries between these is essential for high-performance JavaScript.

## 🔬 Internal Mechanics

### Web Workers — Separate V8 Isolates

Each Worker runs in a separate **V8 Isolate** — a completely independent JS VM with its own heap, event loop, and microtask queue. There is NO shared memory by default.

Communication uses **postMessage + structured clone**:
`
Main Thread Isolate         Worker Isolate
┌──────────────────┐       ┌──────────────────┐
│  V8 Heap         │       │  V8 Heap         │
│  Event Loop      │       │  Event Loop      │
│       │postMessage│──────►│onmessage         │
│       │           │ clone │                  │
│  onmessage        │◄──────│postMessage       │
└──────────────────┘       └──────────────────┘
Message data is CLONED (structuredClone semantics)
`

### SharedArrayBuffer — True Shared Memory

SharedArrayBuffer (SAB) allows sharing a raw memory buffer between threads WITHOUT cloning:
`
Main Thread:    Worker:
sab = new SharedArrayBuffer(4)
view = new Int32Array(sab)    ──→  view = new Int32Array(sab)
view[0] = 42                        // Both see the SAME memory!
`

This enables real-time communication without serialization cost but introduces **data races**.

### Atomics — Lock-Free Synchronization

Atomics provides atomic operations on SharedArrayBuffer views:
`javascript
// Atomic read-modify-write (no data race)
Atomics.add(view, index, value)  // atomic increment
Atomics.compareExchange(view, index, expected, replacement)  // CAS

// Blocking wait (ONLY in workers, NOT main thread)
Atomics.wait(view, index, expected, timeout)
// Blocks the worker thread until view[index] !== expected

// Wake up waiting threads
Atomics.notify(view, index, count)
`

## 📐 ASCII Diagram — Thread Architecture

`
BROWSER PROCESS
┌──────────────────────────────────────────────────────────────┐
│  RENDERER PROCESS (one per tab)                               │
│  ┌─────────────────┐  ┌──────────────┐  ┌────────────────┐  │
│  │  Main Thread    │  │  Worker      │  │  Worker        │  │
│  │  (JS + Render)  │  │  Thread 1    │  │  Thread 2      │  │
│  │  V8 Isolate     │  │  V8 Isolate  │  │  V8 Isolate    │  │
│  └────────┬────────┘  └──────┬───────┘  └───────┬────────┘  │
│           │                  │                   │            │
│           └──────────────────┴───────────────────┘           │
│                              │                               │
│                    SharedArrayBuffer (SAB)                    │
│                    Shared memory across all threads           │
└──────────────────────────────────────────────────────────────┘
`

## 🔍 Code Examples

### Example 1 — Worker Thread (Node.js)

`javascript
// main.js
const { Worker, isMainThread, parentPort, workerData } = require('worker_threads')

if (isMainThread) {
  // Create worker with data
  const worker = new Worker(__filename, {
    workerData: { numbers: [1, 2, 3, 4, 5, 6, 7, 8] }
  })
  
  worker.on('message', result => {
    console.log('Sum from worker:', result)
  })
  
  worker.on('error', err => console.error('Worker error:', err))
} else {
  // Worker code
  const sum = workerData.numbers.reduce((a, b) => a + b, 0)
  parentPort.postMessage(sum)
}
`

### Example 2 — SharedArrayBuffer + Atomics (Producer-Consumer)

`javascript
// Shared ring buffer between main thread and worker
const BUFFER_SIZE = 1024
const sharedBuffer = new SharedArrayBuffer(
  4 +           // read pointer (Int32)
  4 +           // write pointer (Int32)
  BUFFER_SIZE   // data bytes (Uint8)
)

const control = new Int32Array(sharedBuffer, 0, 2)  // [readPtr, writePtr]
const data = new Uint8Array(sharedBuffer, 8, BUFFER_SIZE)

// Producer (main thread):
function write(byte) {
  const writePtr = Atomics.load(control, 1)
  const nextWrite = (writePtr + 1) % BUFFER_SIZE
  
  // Wait if buffer full
  while (nextWrite === Atomics.load(control, 0)) {
    // Spin-wait (bad for battery, use Atomics.wait in worker instead)
  }
  
  data[writePtr] = byte
  Atomics.store(control, 1, nextWrite)  // Atomic update of write pointer
  Atomics.notify(control, 1, 1)         // Wake consumer
}

// Consumer (worker thread):
function read() {
  const readPtr = Atomics.load(control, 0)
  
  // Block until data available
  while (readPtr === Atomics.load(control, 1)) {
    Atomics.wait(control, 0, readPtr)  // Block thread (workers only!)
  }
  
  const byte = data[readPtr]
  Atomics.store(control, 0, (readPtr + 1) % BUFFER_SIZE)
  return byte
}
`

### Example 3 — Race Condition Example

`javascript
// Data race without Atomics:
const sab = new SharedArrayBuffer(4)
const view = new Int32Array(sab)
view[0] = 0

// Main thread:
view[0]++  // Read 0, add 1, write 1 (NOT atomic)

// Worker (concurrent):
view[0]++  // May read 0 before main writes 1, ALSO writes 1
// Result: 1 instead of 2 — race condition!

// Fix with Atomics:
Atomics.add(view, 0, 1)  // Atomic increment — guaranteed correct
`

## 💥 Production Failure — Main Thread Blocking

`javascript
// Symptom: UI freezes during data processing

// WRONG: Heavy computation on main thread
function processLargeDataset(data) {
  return data
    .filter(item => complexFilter(item))
    .map(item => expensiveTransform(item))
    .sort((a, b) => complexComparison(a, b))
  // This may block main thread for 2-3 seconds → UI completely frozen
}

// CORRECT: Offload to Worker
function processLargeDatasetAsync(data) {
  return new Promise((resolve, reject) => {
    const worker = new Worker('./processor.js')
    worker.postMessage({ data })
    worker.on('message', resolve)
    worker.on('error', reject)
  })
}

// BETTER: Reuse worker pool (creating workers is expensive ~10-50ms)
class WorkerPool {
  constructor(size, scriptPath) {
    this.workers = Array.from({ length: size }, () => ({
      worker: new Worker(scriptPath),
      busy: false
    }))
  }
  
  async run(data) {
    const available = this.workers.find(w => !w.busy)
    if (!available) throw new Error('No workers available')
    
    available.busy = true
    return new Promise((resolve, reject) => {
      available.worker.once('message', result => {
        available.busy = false
        resolve(result)
      })
      available.worker.once('error', err => {
        available.busy = false
        reject(err)
      })
      available.worker.postMessage(data)
    })
  }
}
`

## ⚠️ Edge Cases

### COOP/COEP Headers Required for SharedArrayBuffer

`javascript
// SharedArrayBuffer requires cross-origin isolation due to Spectre:
// Response headers must include:
// Cross-Origin-Opener-Policy: same-origin
// Cross-Origin-Embedder-Policy: require-corp

// Check if available:
if (typeof SharedArrayBuffer === 'undefined') {
  console.log('SharedArrayBuffer not available: missing COOP/COEP headers')
}

if (!crossOriginIsolated) {
  console.log('Not cross-origin isolated')
}
`

## 🏢 Industry Best Practices

1. **Use Worker Threads for CPU-bound tasks** — Image processing, PDF generation, ML inference, crypto operations.
2. **Never block the main thread** — Any synchronous operation >16ms on main thread drops frames.
3. **Use WorkerPool** — Creating workers takes 10-50ms. Pool and reuse them.
4. **Use structured clone strategically** — Large data transferred via postMessage is cloned (slow). Use transferable objects (ArrayBuffer, ImageBitmap) for zero-copy transfer.
5. **Use SharedArrayBuffer + Atomics for high-frequency communication** — Avoids serialization cost of postMessage.

## ⚖️ Trade-offs

| Mechanism | Communication Cost | Shared State | Complexity |
|-----------|-------------------|--------------|------------|
| postMessage | Serialize/clone | No (copies) | Low |
| Transferable | Zero-copy | No (transferred) | Low |
| SharedArrayBuffer | Zero | Yes | High (race conditions) |
| Atomics | Zero | Synchronized | Very High |

## 💼 Interview Questions

**Q1: Why is Atomics.wait() forbidden on the main thread?**
> Atomics.wait() blocks the calling thread until a condition is met. If allowed on the main thread, it would freeze the UI completely — no user events, no rendering, no JavaScript execution until the wait completes. The spec explicitly forbids it on the main thread (it throws TypeError: Atomics.wait cannot be called in this context). Workers can use it because blocking a worker thread only affects that worker's computation, not the UI.

**Q2: How does V8 ensure SharedArrayBuffer access is safe across JIT compilation?**
> V8's TurboFan must not reorder or optimize away SharedArrayBuffer accesses that have Atomics semantics (because another thread might read/write between operations). V8 inserts **memory fences** (hardware barriers) around atomic operations to prevent CPU reordering. Non-atomic accesses to SAB are still subject to data races — the developer must use Atomics for synchronized access.

## 🧩 Practice Problem

Implement a thread-safe counter using SharedArrayBuffer:
`javascript
class SharedCounter {
  constructor() {
    this.sab = new SharedArrayBuffer(4)
    this.view = new Int32Array(this.sab)
  }
  
  increment() {
    return Atomics.add(this.view, 0, 1) + 1  // Returns old value + 1
  }
  
  decrement() {
    return Atomics.sub(this.view, 0, 1) - 1
  }
  
  get value() {
    return Atomics.load(this.view, 0)
  }
  
  reset() {
    Atomics.store(this.view, 0, 0)
  }
  
  // Get SAB for passing to workers
  get buffer() { return this.sab }
}
`

## 🔗 Navigation

**Prev:** [03_Garbage_Collection.md](03_Garbage_Collection.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [05_Debouncing_vs_Throttling.md](05_Debouncing_vs_Throttling.md)
