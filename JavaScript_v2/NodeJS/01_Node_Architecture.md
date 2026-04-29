# 📌 01 — Node.js Architecture

## 🧠 Concept Explanation

Node.js is a JavaScript runtime built on V8 with two additional layers that make it suitable for I/O-intensive server applications:
1. **libuv** — Cross-platform async I/O library providing the event loop, thread pool, and OS I/O primitives
2. **Node.js bindings** — C++ layer bridging V8 and libuv, implementing core modules (`fs`, `net`, `http`, etc.)

The fundamental design choice: **single-threaded JavaScript, multi-threaded I/O**. JS code runs on one thread, but all I/O operations are dispatched to the OS or libuv's thread pool.

## 🔬 Internal Mechanics (libuv)

### libuv Event Loop Phases

Node.js's event loop is more complex than the browser's — it has 6 distinct phases:

```
┌───────────────────────────────────────────────┐
│                    timers                     │ ← execute setTimeout/setInterval callbacks
├───────────────────────────────────────────────┤
│                 pending callbacks             │ ← I/O callbacks deferred to next iteration
├───────────────────────────────────────────────┤
│                   idle, prepare               │ ← internal use
├───────────────────────────────────────────────┤
│                      poll                    │ ← retrieve I/O events, execute callbacks
├───────────────────────────────────────────────┤
│                    check                     │ ← setImmediate callbacks
├───────────────────────────────────────────────┤
│                close callbacks               │ ← socket.on('close', ...) etc.
└───────────────────────────────────────────────┘
     ↑ After each phase: drain nextTick + promise queues ↑
```

### libuv Thread Pool

libuv maintains a **thread pool** (default size: 4, max: 1024) for:
- File system operations (`fs.readFile`, `fs.stat`, etc.)
- DNS resolution (`dns.lookup`)
- Crypto operations (`crypto.pbkdf2`, `crypto.randomBytes`)
- User code via `worker.runInAsyncScope` / `@napi-rs` native modules

Network I/O does NOT use the thread pool — it uses the OS's async I/O APIs (epoll on Linux, kqueue on macOS, IOCP on Windows).

```
JavaScript Thread:
  fn() → calls fs.readFile() → delegates to libuv

libuv Thread Pool (4 threads):
  Thread 1: [reading file A]
  Thread 2: [reading file B]
  Thread 3: [crypto hashing]
  Thread 4: [dns lookup]

When thread 1 completes:
  → callback added to poll phase queue
  → event loop (on JS thread) picks it up next poll iteration
  → JavaScript callback executed
```

### V8 + libuv Integration

V8 handles JavaScript execution. libuv handles I/O. They're integrated via:
- `uv_run()` is called in a loop by Node.js
- V8's microtask checkpoint is called between phases (nextTick + Promise queues)
- The "poll" phase blocks on I/O for up to the time until the next timer

## 📐 ASCII Diagram — Request Lifecycle

```
HTTP Request arrives → OS network stack → libuv (epoll/kqueue event)
                                               │
                                         poll phase: callback queued
                                               │
                              JS thread: http.IncomingMessage created
                                               │
                            Route handler executes (sync JS code)
                                               │
                              await db.query() → delegation to thread pool OR
                                               → native async I/O
                              JS thread: free (event loop continues)
                                               │
                         DB response: libuv callback → poll phase
                                               │
                              JS thread: route handler resumes
                              res.json() → OS write (non-blocking)
```

## 🔍 Code Examples

### Example 1 — Thread Pool Exhaustion

```javascript
// Problem: All 4 thread pool slots occupied → file reads queue up
const { stat } = require('fs/promises')

// This creates 8 concurrent file stat requests
// But only 4 thread pool slots → 4 wait for thread
const files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
await Promise.all(files.map(f => stat(f)))
// First 4 start immediately
// Next 4 queue until a slot opens

// Measure: thread pool starvation adds latency
// Fix: Increase pool size
process.env.UV_THREADPOOL_SIZE = '8'  // Set BEFORE any libuv calls!
// Must be set at startup, not after first use
// Or: use native async I/O where available (e.g., io_uring via libuv 1.45+)
```

### Example 2 — Event Loop Blocking Detection

```javascript
// Detect main thread blocking (long synchronous tasks)
const blocked = require('blocked-at')  // npm install blocked-at

blocked((time, stack) => {
  console.error(`Event loop blocked for ${time}ms`)
  console.error(stack.join('\n'))
}, { threshold: 50 })  // Alert if blocked > 50ms

// Alternative: manual measurement
let lastTick = Date.now()
setInterval(() => {
  const now = Date.now()
  const delta = now - lastTick
  if (delta > 100) {
    console.warn(`Event loop lag: ${delta}ms (expected ~10ms)`)
  }
  lastTick = now
}, 10)
```

### Example 3 — Cluster for Multi-Core Utilization

```javascript
const cluster = require('cluster')
const http = require('http')
const os = require('os')

if (cluster.isPrimary) {
  const numCPUs = os.cpus().length
  console.log(`Primary ${process.pid} is running`)
  
  // Fork workers
  for (let i = 0; i < numCPUs; i++) {
    cluster.fork()
  }
  
  cluster.on('exit', (worker, code, signal) => {
    console.log(`Worker ${worker.process.pid} died`)
    cluster.fork()  // Replace dead worker
  })
  
  // Primary can send messages to workers
  cluster.on('message', (worker, message) => {
    if (message.type === 'METRIC') {
      updateMetrics(message.data)
    }
  })
  
} else {
  // Worker process
  http.createServer((req, res) => {
    // Each worker has its own event loop
    // OS round-robins connections (on Linux: kernel-level load balancing)
    res.end(`Worker ${process.pid} handled this request`)
  }).listen(3000)
}
```

### Example 4 — Event Loop Monitoring in Production

```javascript
// Production-grade event loop monitoring
const { monitorEventLoopDelay } = require('perf_hooks')

const histogram = monitorEventLoopDelay({ resolution: 10 })  // 10ms sampling
histogram.enable()

// Periodic reporting
setInterval(() => {
  const metrics = {
    min: histogram.min / 1e6,   // ns to ms
    max: histogram.max / 1e6,
    mean: histogram.mean / 1e6,
    p50: histogram.percentile(50) / 1e6,
    p95: histogram.percentile(95) / 1e6,
    p99: histogram.percentile(99) / 1e6,
  }
  
  if (metrics.p99 > 100) {
    console.error('Event loop lag P99 > 100ms:', metrics)
    // Alert: Datadog, PagerDuty, etc.
  }
  
  histogram.reset()
}, 60000)
```

## 💥 Production Failures

### Failure 1 — Synchronous Crypto Blocking Node.js

```javascript
// crypto.pbkdf2Sync blocks the main thread!
app.post('/register', async (req, res) => {
  const hash = crypto.pbkdf2Sync(
    req.body.password,
    salt,
    100000,  // 100k iterations
    64,
    'sha512'
  )
  // This blocks the EVENT LOOP for ~100-500ms!
  // ALL other requests are queued during this time
  
  // Under load: 10 concurrent registrations × 200ms = 2 second stall
  
  await db.create({ hash: hash.toString('hex') })
  res.json({ success: true })
})

// Fix: Use async version (uses thread pool)
app.post('/register', async (req, res) => {
  const hash = await crypto.pbkdf2(password, salt, 100000, 64, 'sha512')  // Async!
  // Thread pool handles computation, JS thread stays free
  await db.create({ hash: hash.toString('hex') })
  res.json({ success: true })
})
```

### Failure 2 — Long JSON.parse Blocking Requests

```javascript
// Common Node.js API performance issue
app.get('/export', async (req, res) => {
  const rawData = await db.query('SELECT * FROM events')  // 50MB result
  
  // This runs synchronously on the main thread:
  const json = JSON.stringify(rawData)  // 50MB JSON stringify = 200-500ms block!
  res.setHeader('Content-Type', 'application/json')
  res.end(json)
  // During stringify: 0 other requests handled
})

// Fix: Stream the response
app.get('/export', async (req, res) => {
  res.setHeader('Content-Type', 'application/json')
  res.write('[')
  
  const cursor = db.queryCursor('SELECT * FROM events')
  let first = true
  
  for await (const row of cursor) {
    if (!first) res.write(',')
    res.write(JSON.stringify(row))  // Small chunk — short block
    first = false
    // Event loop gets control between chunks (async iteration)
  }
  
  res.end(']')
})
```

## ⚠️ Edge Cases

### libuv Thread Pool and DNS

```javascript
// dns.lookup uses thread pool (getaddrinfo, blocking system call)
// dns.resolve uses OS async (c-ares, non-blocking)
// They have different behaviors:

const dns = require('dns')

// Uses THREAD POOL - can exhaust UV_THREADPOOL_SIZE
dns.lookup('example.com', (err, address) => { ... })

// Uses c-ares (async, no thread pool)
dns.resolve4('example.com', (err, addresses) => { ... })

// In production: if thread pool is exhausted with file I/O,
// dns.lookup calls queue up → connection setup becomes slow
```

## 🏢 Industry Best Practices

1. **Never use synchronous I/O** in request handlers (`fs.readFileSync`, `crypto.pbkdf2Sync`).
2. **Set UV_THREADPOOL_SIZE** based on workload (default 4 is often too small for I/O-heavy apps).
3. **Use Cluster or Worker Threads** to utilize all CPU cores for CPU-bound work.
4. **Monitor event loop lag** — P99 > 100ms indicates blocking operations.
5. **Stream large responses** — Don't buffer large JSON responses in memory.
6. **Use `clinic.js`** — The definitive Node.js performance analysis tool.

## ⚖️ Trade-offs

| Approach | CPU Usage | Memory | Complexity | Use Case |
|----------|-----------|--------|------------|---------|
| Single process | 1 core | Low | Low | Dev, simple apps |
| Cluster | N cores | N×memory | Medium | HTTP servers |
| Worker Threads | N cores | Shared heap | High | CPU-bound tasks |
| Separate processes | N cores | N×memory | High | Isolation needed |

## 💼 Interview Questions

**Q1: Node.js is "single-threaded" — but file I/O is clearly not blocking. Explain.**
> Node.js is single-threaded for JavaScript execution, but libuv manages a thread pool (default 4 threads) for operations that require blocking OS calls (file I/O, DNS lookup, crypto). When `fs.readFile()` is called, Node.js passes the operation to libuv, which dispatches it to a thread pool thread. The main JavaScript thread is immediately free to handle other work. When the I/O completes, libuv queues a callback in the poll phase of the event loop. The callback executes on the JavaScript thread.

**Q2: What happens when the libuv thread pool is exhausted?**
> All new operations requiring thread pool threads (file I/O, DNS, crypto) queue up. They don't fail — they wait for a slot to open. This manifests as increased latency for those operations. Observable as: high P99 latency for file reads under load, slow DNS resolution. Diagnosis: `UV_THREADPOOL_SIZE=1 node app.js` makes it obvious. Fix: increase `UV_THREADPOOL_SIZE` (env var, must be set at process start) or reduce thread pool dependency (use streaming, native async APIs).

## 🔗 Navigation

**Prev:** [../Browser/09_Animation_and_Frame_Budget.md](../Browser/09_Animation_and_Frame_Budget.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [02_Event_Emitter.md](02_Event_Emitter.md)
