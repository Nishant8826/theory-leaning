# 📌 04 — Cluster Module

## 🧠 Concept Explanation

Node.js runs on a single CPU core by default. The Cluster module allows creating child processes (workers) that share the same server port, enabling multi-core utilization. The primary process manages workers; workers handle actual HTTP requests.

OS-level load balancing (Linux): The kernel distributes incoming connections to worker processes via SO_REUSEPORT. On macOS/Windows: libuv distributes connections via a round-robin algorithm in the primary process.

## 🔍 Code Examples

### Example 1 — Production Cluster Setup

```javascript
const cluster = require('cluster')
const http = require('http')
const os = require('os')
const process = require('process')

const numCPUs = os.cpus().length

if (cluster.isPrimary) {
  console.log(`Primary ${process.pid}: forking ${numCPUs} workers`)
  
  const workers = new Map()
  
  for (let i = 0; i < numCPUs; i++) {
    const worker = cluster.fork()
    workers.set(worker.id, worker)
  }
  
  // Graceful restart worker
  cluster.on('exit', (worker, code, signal) => {
    console.warn(`Worker ${worker.process.pid} died (${signal || code})`)
    workers.delete(worker.id)
    
    if (code !== 0) {  // Abnormal exit
      const newWorker = cluster.fork()
      workers.set(newWorker.id, newWorker)
    }
  })
  
  // Graceful shutdown
  process.on('SIGTERM', () => {
    console.log('Primary: shutting down workers')
    for (const worker of workers.values()) {
      worker.send({ type: 'SHUTDOWN' })
    }
    setTimeout(() => process.exit(0), 30000)
  })
  
} else {
  const server = http.createServer(app)
  server.listen(3000)
  
  process.on('message', (msg) => {
    if (msg.type === 'SHUTDOWN') {
      server.close(() => {
        process.exit(0)
      })
    }
  })
  
  console.log(`Worker ${process.pid} started`)
}
```

### Example 2 — Sticky Sessions (For WebSockets with Cluster)

```javascript
// Problem: WebSocket connections need to go to the SAME worker
// (Round-robin distributes to different workers — breaks stateful connections)

// Solution: nginx/haproxy sticky sessions based on IP hash
// OR: Redis session store that all workers share

// Node.js cluster-level sticky sessions (not built-in, use `sticky-cluster` or `socket.io-redis`):
const sticky = require('sticky-cluster')  // npm package

sticky((callback) => {
  const io = require('socket.io')
  const server = http.createServer(app)
  io.attach(server)
  callback(server)
}, {
  concurrency: numCPUs,  // Number of worker processes
  port: 3000,
  debug: true
})
```

## 💥 Production Failure — Shared State Assumption

```javascript
// WRONG: Workers DO NOT share memory
// Each cluster worker is a separate process with its own heap

// In-memory cache is NOT shared:
const cache = {}  // Each worker has its own cache!

app.get('/data', (req, res) => {
  if (cache[req.params.id]) return res.json(cache[req.params.id])
  // Cache hit on Worker 1 ≠ cache hit on Worker 2
  // 4 workers = 4 separate caches = 4x Redis load
})

// Fix: Use Redis for shared state across workers
const redis = require('ioredis')
const client = new redis()

app.get('/data', async (req, res) => {
  const cached = await client.get(req.params.id)
  if (cached) return res.json(JSON.parse(cached))
  // Same Redis: shared across all workers
})
```

## 🏢 Industry Best Practices

1. **Fork one worker per CPU core** — `os.cpus().length` workers is the guideline.
2. **Implement graceful shutdown** — SIGTERM → stop accepting, drain existing, exit.
3. **Monitor worker crashes** — Alert and restart workers on abnormal exits.
4. **Avoid shared in-process state** — Use Redis/Memcached for shared state.
5. **Consider PM2** — Production process manager with built-in cluster, logging, monitoring.

## 💼 Interview Questions

**Q1: How does the Cluster module distribute connections?**
> On Linux with `SO_REUSEPORT` (default since Node.js 10): the OS kernel distributes incoming connections across all workers that are bound to the same port — at the kernel level, before Node.js involvement. On Windows/macOS or when `cluster.schedulingPolicy = cluster.SCHED_RR`: the primary process accepts connections and passes the socket handle to a worker via IPC, round-robin style. The Linux kernel-level approach has lower latency.

## 🔗 Navigation

**Prev:** [03_Streams.md](03_Streams.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [05_Worker_Threads.md](05_Worker_Threads.md)
