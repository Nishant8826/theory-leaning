# Worker Threads

Node.js is single-threaded, which means executing heavy calculations (like image resizing, PDF rendering, or cryptography) on the main thread blocks the event loop, freezing all other client requests. Using `worker_threads` allows you to spawn native OS threads running isolated V8 engines to run heavy computations in parallel, keeping your main server responsive.

### Worker Threads vs. Child Processes
* **Child Processes (e.g. `child_process`)**: Spawn completely new OS processes. Each process has its own isolated memory space, meaning data must be serialized and sent over slow Inter-Process Communication (IPC) channels.
* **Worker Threads (e.g. `worker_threads`)**: Spawn new threads *inside the same parent process*. Each thread has its own isolated V8 engine instance (heap and call stack), but they can share memory space directly using `SharedArrayBuffer` objects, eliminating data serialization overhead.

### Memory Sharing: `SharedArrayBuffer` and `Atomics`
* **`SharedArrayBuffer`**: A raw binary memory buffer that can be shared directly between threads. This allows multiple threads to read and write the same memory space, making data transfer extremely fast.
* **`Atomics`**: Because sharing memory exposes your application to race conditions (where two threads modify the same memory address simultaneously, corrupting data), Node.js provides the `Atomics` object. It ensures that read, write, and math operations on shared memory are executed atomically (they cannot be interrupted).

## Deep Dive

### Thread Communication: `MessagePort`
Threads communicate by sending messages through a **`MessageChannel`**, which contains two connected ports (`port1` and `port2`).
* When you call `port.postMessage(data)`, Node clones the data using the HTML structured clone algorithm and transmits it to the receiving port.
* For large payloads (like buffers or arrays), you can **transfer** the data instead of copying it. This passes ownership of the memory directly to the receiving thread, making the transfer fast and freeing up the sender's memory.

## Visual Explanation

### Worker Thread Concurrency Model
```text
  [ Main OS Process: Node.js ]
  ├── [ Main Thread: V8 Heap & Event Loop ]
  │         │
  │         ├── Instantiates (MessagePort communication) ──> parentPort
  │         ▼
  ├── [ Worker Thread 1: Isolated V8 Engine & Call Stack ]
  └── [ Worker Thread 2: Isolated V8 Engine & Call Stack ]
             │                                    │
             ▼                                    ▼
       [ Read / Write ] ─── Atomics lock ───> [ SharedArrayBuffer (Shared Memory) ]
```

## Real-World Example
Consider an API endpoint that generates cryptographic hashes (like password reset hashes) using complex algorithms. Executing these hashes on the main thread blocks requests. Instead, you spawn a worker thread to perform the hashing in the background, post the results back to the main thread, and return the response, keeping the API responsive under load.

## Code Examples

### Spawning Workers, Passing Messages, and Sharing Memory

```javascript
// main.js
const { Worker, isMainThread, parentPort, workerData } = require('worker_threads');
const path = require('path');

// 1. Define Worker Execution Block
if (!isMainThread) {
  // We are inside the Worker Thread context
  console.log(`[WORKER] Worker thread initialized with data: ${workerData}`);
  
  // Perform heavy CPU-bound task (Simulate calculating a Fibonacci sequence)
  const calculateFibonacci = (n) => {
    if (n < 2) return n;
    return calculateFibonacci(n - 1) + calculateFibonacci(n - 2);
  };

  const result = calculateFibonacci(workerData);
  
  // Send the calculated result back to the main thread
  parentPort.postMessage({ status: 'completed', result });
  process.exit(0); // Exit worker process safely
}

// 2. Define Main Thread Execution Block
else {
  console.log('1. Main thread started.');

  const runCpuTask = (numToCalculate) => {
    return new Promise((resolve, reject) => {
      // Spawn a new worker thread running this same file
      const worker = new Worker(__filename, {
        workerData: numToCalculate // Pass data to the worker
      });

      // Listen for messages from the worker
      worker.on('message', (message) => {
        resolve(message.result);
      });

      worker.on('error', (err) => {
        reject(err);
      });

      worker.on('exit', (code) => {
        if (code !== 0) {
          reject(new Error(`Worker stopped with exit code ${code}`));
        }
      });
    });
  };

  async function execute() {
    try {
      console.log('2. Spawning worker thread for Fibonacci calculation (this won\'t block)...');
      const fibResult = await runCpuTask(40); // 40 is high enough to block single thread
      console.log('3. Fibonacci result returned from worker:', fibResult);
    } catch (err) {
      console.error('Worker failed:', err.message);
    }
  }

  execute();
  console.log('4. Main thread continues processing other events (Not blocked!).');
}
```

## Best Practices
* **Do Not Spawn Workers per Request**: Spawning a worker thread takes ~10-20ms of CPU overhead. Never spawn a new worker thread for individual HTTP requests. Use a **Worker Pool** (like `piscina`) that keeps a set of warm workers active and reuses them.
* **Keep Workers Stateless**: Avoid storing state or caching data inside worker threads. Keep them focused strictly on executing tasks and returning results.
* **Use SharedArrayBuffer for Big Data**: If you need to share large arrays or image buffers between threads, pass them using `SharedArrayBuffer` to avoid data copying overhead.

## Interview Questions

**Q:** What is the purpose of the `worker_threads` module in Node.js?

> **Answer:**
> The `worker_threads` module allows Node.js to execute heavy CPU-bound JavaScript calculations concurrently on separate native threads, preventing them from blocking the main event loop.

**Q:** What is the difference between a Worker Thread and a Child Process?

> **Answer:**
> A child process runs in a completely separate operating system process with its own isolated memory, requiring slow serialization (IPC) to pass data. A worker thread runs inside the same parent process, running an isolated V8 instance but capable of sharing memory directly using `SharedArrayBuffer`, which is much faster.

**Q:** What are race conditions, and how does the `Atomics` object help you prevent them when sharing memory between threads?

> **Answer:**
> A race condition occurs when multiple threads attempt to read and write to the same shared memory address (`SharedArrayBuffer`) simultaneously, resulting in corrupted or unpredictable data. The `Atomics` object provides atomic execution operations (like `Atomics.add` or `Atomics.wait`). It guarantees that memory operations are completed entirely by one thread without interruption from other threads, preventing data corruption.

**Q:** How would you build a production-grade Worker Pool from scratch? Discuss worker initialization, task routing queues, and managing CPU throttling limits.

> **Answer:**
> To build a production-grade Worker Pool:
> 1. **Spawn Warm Workers**: Instantiate a fixed number of workers (typically matching the core count `os.cpus().length` to avoid CPU context-switching overhead) when the application starts, keeping them active ("warm").
> 2. **Implement Task Queue**: Maintain an array queue of pending CPU tasks in the parent process.
> 3. **Manage Worker States**: Track active and idle workers in a map. When a task is added:
> - If an idle worker is available, assign the task to it using `worker.postMessage()`.
> - If all workers are active, push the task to the queue.
> 4. **Handle Terminations**: Listen for worker crash events (`error` and `exit` events) and automatically spawn a new worker to replace the crashed one, keeping the pool capacity stable.
> 5. **Implement Timeouts**: Add execution timeouts to tasks to terminate and recreate workers that get stuck in infinite loops, protecting server resources.

---
Previous : [47_Streams_Deep_Dive.md](47_Streams_Deep_Dive.md) | Index : [00_index.md](00_index.md) | Next : [49_Cluster_Module.md](49_Cluster_Module.md)
