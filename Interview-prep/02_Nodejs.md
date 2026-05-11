# 🚀 Interview Preparation - Node.js

> **Domain:** Web Development / Backend
> **Level:** Beginner to Expert
> **Target Role:** Software Engineer / Senior Engineer / Lead

---

## 🟢 Beginner Level

### ❓ Q1. **What is Node.js and how does it work?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
Node.js is an open-source, cross-platform runtime environment built on Chrome's V8 JavaScript engine. It allows developers to execute JavaScript code outside of a web browser. Node.js uses an event-driven, non-blocking I/O model, making it lightweight and highly efficient for data-intensive real-time applications that run across distributed devices.

> 💡 **Interviewer Focus:**
- Mention the V8 engine.
- Highlight the event-driven and non-blocking I/O model.
- Emphasize its use in server-side scripting and API development.

</details>

<hr/>

### ❓ Q2. **What is V8 engine?**
*(No answer provided. Discuss the JavaScript engine developed by Google used in Chrome and Node.js to compile JS to machine code.)*

<hr/>

### ❓ Q3. **Explain the difference between Node.js and browser JavaScript.**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
While both use JavaScript, they run in different environments. 
- **Browser JS:** Runs in the browser environment. It has access to the DOM (Document Object Model) and BOM (Browser Object Model) to manipulate web pages. It is restricted by CORS and cannot access the local file system directly.
- **Node.js:** Runs on the server. It lacks access to the DOM and BOM but has access to the underlying operating system, meaning it can read/write files, interact with databases, and handle network requests via core modules like `fs`, `http`, and `path`.

> 💡 **Interviewer Focus:**
- Contrast DOM/BOM availability with OS/file system access.

</details>

<hr/>

### ❓ Q4. **What is npm?**
*(No answer provided. Discuss Node Package Manager, package.json, and dependency management.)*

<hr/>

### ❓ Q5. **How do you import and export modules in Node.js?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
Node.js traditionally uses the CommonJS module system:
- **Exporting:** Assign functions or objects to `module.exports` or `exports`.
  ```javascript
  module.exports = { myFunction };
  ```
- **Importing:** Use the `require()` function.
  ```javascript
  const { myFunction } = require('./myModule');
  ```
With newer versions, Node.js also supports ES Modules (ESM) using `import` and `export` keywords (enabled via `.mjs` extension or `"type": "module"` in `package.json`).

> 💡 **Interviewer Focus:**
- Distinguish between CommonJS (`require`) and ES Modules (`import`).

</details>

<hr/>

### ❓ Q6. **What is the difference between `require` and `import`?**
*(No answer provided. Discuss CommonJS vs ES Modules, synchronous vs asynchronous loading.)*

<hr/>

### ❓ Q7. **What is `package.json` and what does it contain?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
`package.json` is the manifest file for any Node.js project. It holds metadata relevant to the project and is used to manage dependencies, scripts, versions, and project details.
Key fields include:
- `name` & `version`: Project identity.
- `dependencies`: Libraries needed in production.
- `devDependencies`: Libraries needed only for local development and testing.
- `scripts`: Custom CLI commands (e.g., `start`, `test`).

</details>

<hr/>

### ❓ Q8. **What is the `fs` module?**
*(No answer provided. Discuss file system operations.)*

<hr/>

### ❓ Q9. **Explain the difference between `readFile` and `readFileSync`.**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
- `fs.readFileSync()` is synchronous. It blocks the event loop until the file reading is completed. This should only be used during application startup, never during request handling.
- `fs.readFile()` is asynchronous. It reads the file in the background and executes a callback function once the data is available, allowing the event loop to continue processing other requests.

> 💡 **Interviewer Focus:**
- Strong emphasis on blocking vs. non-blocking code.

</details>

<hr/>

### ❓ Q10. **What are core modules in Node.js? Name a few.**
*(No answer provided. Mention fs, http, path, os, events.)*

<hr/>

### ❓ Q11. **What is an event emitter in Node.js?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
`EventEmitter` is a class in the `events` module that facilitates communication between objects in Node.js. It allows you to emit named events and register listeners (callbacks) that are called when those events occur.
```javascript
const EventEmitter = require('events');
const myEmitter = new EventEmitter();
myEmitter.on('event', () => console.log('Event occurred!'));
myEmitter.emit('event');
```

</details>

<hr/>

### ❓ Q12. **How do you handle errors in Node.js?**
*(No answer provided. Discuss try-catch, error-first callbacks, event emitters, and promise catch blocks.)*

<hr/>

### ❓ Q13. **What is the purpose of the `path` module?**
*(No answer provided. Discuss file path manipulation.)*

<hr/>

### ❓ Q14. **What are streams in Node.js?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
Streams are collections of data—just like arrays or strings. The difference is that streams might not be available all at once, and they don't have to fit in memory. This makes streams extremely powerful when working with large amounts of data, like reading a large file or streaming a video. 
Types of streams: Readable, Writable, Duplex, and Transform.

> 💡 **Interviewer Focus:**
- Mention memory efficiency.
- List the 4 types of streams.

</details>

<hr/>

### ❓ Q15. **What are the different types of streams?**
*(No answer provided. Mention Readable, Writable, Duplex, Transform.)*

<hr/>

### ❓ Q16. **Explain the concept of callbacks in Node.js.**
*(No answer provided. Discuss functions passed as arguments to execute after an async operation.)*

<hr/>

### ❓ Q17. **What is callback hell and how do you avoid it?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
Callback hell (or Pyramid of Doom) refers to heavily nested callbacks that make code difficult to read, maintain, and debug.
It can be avoided by:
1. Using Promises.
2. Using `async`/`await` (modern approach).
3. Modularizing code into separate functions.

</details>

<hr/>

### ❓ Q18. **What is the role of `__dirname` and `__filename`?**
*(No answer provided. Discuss absolute paths to the directory and file.)*

<hr/>

### ❓ Q19. **How do you create a simple HTTP server in Node.js?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
Using the core `http` module:
```javascript
const http = require('http');

const server = http.createServer((req, res) => {
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/plain');
  res.end('Hello World\n');
});

server.listen(3000, () => {
  console.log('Server running at port 3000');
});
```

</details>

<hr/>

### ❓ Q20. **What is middleware in the context of Express.js?**
*(No answer provided. Discuss functions that have access to req, res, and next.)*

<hr/>

### ❓ Q21. **How do you read command-line arguments in Node.js?**
*(No answer provided. Discuss process.argv.)*

<hr/>

### ❓ Q22. **What is the `process` object in Node.js?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
The `process` object is a global object that provides information about, and control over, the current Node.js process. It provides data like environment variables (`process.env`), command-line arguments (`process.argv`), and methods to exit the process (`process.exit()`).

</details>

<hr/>

### ❓ Q23. **What are environment variables and how do you use them?**
*(No answer provided. Discuss process.env and .env files.)*

<hr/>

### ❓ Q24. **What is a REPL in Node.js?**
*(No answer provided. Read, Eval, Print, Loop environment.)*

<hr/>

### ❓ Q25. **How do you update npm packages?**
*(No answer provided. Discuss npm update, npm outdated.)*

<hr/>

---

## 🟡 Intermediate Level

### ❓ Q26. **Explain the Node.js Event Loop.**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
The Event Loop is what allows Node.js to perform non-blocking I/O operations despite JavaScript being single-threaded. It offloads operations to the system kernel whenever possible. When operations complete, the kernel tells Node.js, and the corresponding callback is added to the event queue. The event loop continuously checks the call stack and the event queue, pushing callbacks from the queue to the stack when the stack is empty.

> 💡 **Interviewer Focus:**
- Single-threaded nature of JS.
- Offloading to the kernel (Libuv).
- Call stack, task queue, microtask queue.

</details>

<hr/>

### ❓ Q27. **What are the different phases of the Event Loop?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
The Event Loop has several phases, executed in order:
1. **Timers:** Executes callbacks scheduled by `setTimeout()` and `setInterval()`.
2. **Pending Callbacks:** Executes I/O callbacks deferred to the next loop iteration.
3. **Idle, Prepare:** Only used internally.
4. **Poll:** Retrieves new I/O events; executes I/O related callbacks.
5. **Check:** Executes `setImmediate()` callbacks.
6. **Close Callbacks:** Executes close callbacks (e.g., `socket.on('close', ...)`).

</details>

<hr/>

### ❓ Q28. **What is the difference between `process.nextTick()` and `setImmediate()`?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
- `process.nextTick()` fires immediately on the same phase. It resolves before the event loop continues to the next phase, putting it in the microtask queue.
- `setImmediate()` fires on the following iteration or 'tick' of the event loop, specifically in the **Check** phase.

> 💡 **Interviewer Focus:**
- `nextTick` is prioritized over `setImmediate` and Promises.

</details>

<hr/>

### ❓ Q29. **Explain the concept of non-blocking I/O in Node.js.**
*(No answer provided. Discuss how Node.js doesn't wait for I/O operations to finish.)*

<hr/>

### ❓ Q30. **How does Node.js handle concurrency despite being single-threaded?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
Node.js handles concurrency through its event-driven, non-blocking I/O architecture. While the JavaScript execution itself is single-threaded, the underlying C++ API and Libuv library provide a thread pool (default size 4) to handle heavy tasks like file system I/O, cryptography, and compression asynchronously. When these tasks finish, their callbacks are queued in the event loop.

</details>

<hr/>

### ❓ Q31. **What is a Buffer in Node.js and why is it used?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
A Buffer is a globally available class in Node.js used to handle raw binary data. Since JavaScript historically had no mechanism for reading or manipulating streams of binary data, the Buffer class was introduced. It allocates raw memory outside the V8 heap and is especially useful when working with file streams or network protocols.

</details>

<hr/>

### ❓ Q32. **How do you handle file uploads in Node.js?**
*(No answer provided. Mention Multer or handling multipart/form-data.)*

<hr/>

### ❓ Q33. **What are promises and how are they used in Node.js?**
*(No answer provided. Discuss object representing eventual completion or failure of an async operation.)*

<hr/>

### ❓ Q34. **Explain async/await and its advantages over promises.**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
`async`/`await` is syntactic sugar over Promises that makes asynchronous code look and behave a bit more like synchronous code. 
**Advantages:**
- Greatly improves code readability and maintainability.
- Avoids the `.then()` chain and nested callback structures.
- Makes error handling simpler by allowing the use of standard `try/catch` blocks.

</details>

<hr/>

### ❓ Q35. **What is the purpose of the `cluster` module?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
Because Node.js is single-threaded, a single instance runs on a single core. To take advantage of multi-core systems, the `cluster` module allows you to easily create child processes (workers) that run simultaneously and share the same server port. A master process dictates how the workers are spawned and managed.

</details>

<hr/>

### ❓ Q36. **How do you manage sessions in a Node.js application?**
*(No answer provided. Discuss express-session, Redis, or JWTs.)*

<hr/>

### ❓ Q37. **What is JWT and how is it used for authentication?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
JSON Web Token (JWT) is an open standard that defines a compact and self-contained way for securely transmitting information between parties as a JSON object.
In authentication: 
1. The user logs in.
2. The server generates a JWT and sends it to the client.
3. The client stores it and includes it in the `Authorization` header for subsequent requests.
4. The server validates the signature and grants access.

</details>

<hr/>

### ❓ Q38. **Explain CORS and how to enable it in Node.js.**
*(No answer provided. Discuss Cross-Origin Resource Sharing and the cors middleware.)*

<hr/>

### ❓ Q39. **What is a RESTful API?**
*(No answer provided. Discuss state transfer, statelessness, standard HTTP methods.)*

<hr/>

### ❓ Q40. **How do you connect to a MongoDB database using Mongoose?**
*(No answer provided. Discuss mongoose.connect().)*

<hr/>

### ❓ Q41. **What is connection pooling?**
*(No answer provided. Discuss reusing database connections to reduce overhead.)*

<hr/>

### ❓ Q42. **How do you handle uncaught exceptions in Node.js?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
You can listen for the `uncaughtException` event on the `process` object. However, doing so implies the application is in an undefined state. The best practice is to log the error, perform synchronous cleanup, and gracefully restart the process (e.g., using PM2).
```javascript
process.on('uncaughtException', (err) => {
  console.error('Uncaught Exception:', err);
  process.exit(1); 
});
```

</details>

<hr/>

### ❓ Q43. **What is the `crypto` module used for?**
*(No answer provided. Discuss hashing, HMAC, cipher, decipher, signing.)*

<hr/>

### ❓ Q44. **How do you implement logging in a Node.js application?**
*(No answer provided. Discuss Winston, Pino, or Morgan.)*

<hr/>

### ❓ Q45. **What are worker threads in Node.js?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
The `worker_threads` module enables the use of threads that execute JavaScript in parallel. Unlike the `cluster` module (which spawns new processes), worker threads share memory. They are extremely useful for performing CPU-intensive JavaScript operations (like image processing or complex math) without blocking the main event loop.

</details>

<hr/>

### ❓ Q46. **How do you write unit tests in Node.js?**
*(No answer provided. Discuss Jest, Mocha, Chai.)*

<hr/>

### ❓ Q47. **What is the purpose of a reverse proxy like Nginx with Node.js?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
Node.js is great at handling application logic, but it shouldn't be exposed directly to the public internet. A reverse proxy like Nginx is used for:
- Handling SSL/TLS termination.
- Load balancing across multiple Node.js instances.
- Serving static assets efficiently.
- Protecting against basic attacks (DDoS, slowloris).

</details>

<hr/>

### ❓ Q48. **How do you handle routing in Express.js?**
*(No answer provided. Discuss express.Router().)*

<hr/>

### ❓ Q49. **What is semantic versioning in npm?**
*(No answer provided. Discuss MAJOR.MINOR.PATCH.)*

<hr/>

### ❓ Q50. **How do you prevent SQL injection in Node.js?**
*(No answer provided. Discuss parameterized queries, ORMs, and escaping inputs.)*

<hr/>

---

## 🔴 Advanced Level

### ❓ Q51. **Deep dive into V8 engine optimization techniques.**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
The V8 engine compiles JavaScript directly to native machine code. Optimizations include:
- **Hidden Classes:** V8 creates hidden classes at runtime to optimize property access times. Objects with the same properties in the same order share a hidden class.
- **Inline Caching:** V8 caches the memory addresses of object properties.
- **TurboFan:** The optimizing compiler that re-compiles hot code (frequently executed code) into highly optimized machine code.

</details>

<hr/>

### ❓ Q52. **How does Node.js manage memory and garbage collection?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
Node.js (via V8) manages memory using a generational Garbage Collector. Memory is divided into:
- **New Space (Young Generation):** Where new objects are created. Managed by the Scavenger GC, which runs frequently and is very fast.
- **Old Space (Old Generation):** Objects that survive multiple GC cycles in the New Space are moved here. Managed by the Mark-Sweep and Mark-Compact algorithms, which run less frequently as they pause execution (stop-the-world).

</details>

<hr/>

### ❓ Q53. **Explain memory leaks in Node.js and how to detect them.**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
A memory leak occurs when objects are no longer needed but are still referenced, preventing the GC from freeing the memory.
**Causes:** Global variables, closures, event listeners not removed, and caching without bounds.
**Detection:** Use Node's built-in profiler (`--inspect`), Chrome DevTools (heap snapshots), or APM tools like New Relic/Datadog to monitor memory consumption trends and analyze heap dumps.

</details>

<hr/>

### ❓ Q54. **How do you profile a Node.js application for performance bottlenecks?**
*(No answer provided. Discuss clinic.js, Node inspector, flame graphs.)*

<hr/>

### ❓ Q55. **Explain the Libuv library and its role in Node.js.**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
Libuv is a multi-platform C library that provides support for asynchronous I/O based on event loops. It abstracts the underlying OS-specific non-blocking I/O mechanisms (like `epoll` on Linux, `kqueue` on macOS, `IOCP` on Windows). It also provides the thread pool used for tasks that cannot be non-blocking at the OS level (like file system operations and DNS lookups).

</details>

<hr/>

### ❓ Q56. **What is a thread pool in Libuv and how can you configure it?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
Libuv maintains a thread pool to offload heavy synchronous tasks (fs, crypto, zlib, dns). By default, this pool has 4 threads. If you have high I/O concurrency demands, tasks might queue up waiting for a free thread. You can configure the size by setting the `UV_THREADPOOL_SIZE` environment variable before the application starts.

</details>

<hr/>

### ❓ Q57. **How do you handle backpressure in streams?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
Backpressure occurs when data is being read faster than it can be written or processed. If ignored, it leads to massive memory spikes. Node.js handles backpressure natively via the `pipe()` method, which pauses the readable stream when the writable stream's internal buffer is full (returns `false`), and resumes it when the `drain` event is emitted.

</details>

<hr/>

### ❓ Q58. **What are the differences between CommonJS and ES Modules at runtime?**
*(No answer provided. Discuss dynamic vs static loading, synchronous vs asynchronous resolution.)*

<hr/>

### ❓ Q59. **How do you build a highly scalable real-time application using WebSockets?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
To build a scalable WebSocket app (e.g., using Socket.io):
1. **Multiple Instances:** Run multiple Node processes (Cluster or Kubernetes).
2. **Sticky Sessions:** If using Socket.io polling fallback, ensure requests from the same client hit the same server (via Load Balancer).
3. **Pub/Sub Adapter:** Use an in-memory datastore like Redis as a pub/sub message broker so that a message broadcasted from one server instance is propagated to clients connected to other instances.

</details>

<hr/>

### ❓ Q60. **Explain the microservices architecture using Node.js.**
*(No answer provided. Discuss independent deployment, domain-driven design, API Gateways.)*

<hr/>

### ❓ Q61. **How do you implement inter-process communication (IPC) in Node.js?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
IPC is necessary for the master process to communicate with child processes. In Node.js, when a process is spawned with an IPC channel (e.g., using `fork()`), you can use `process.send(message)` to send data and `process.on('message', callback)` to receive data.
```javascript
// Master
const worker = child_process.fork('worker.js');
worker.send({ hello: 'world' });

// Worker
process.on('message', (msg) => {
  console.log('Message from master:', msg);
});
```

</details>

<hr/>

### ❓ Q62. **What are child processes in Node.js? Explain `spawn`, `exec`, `execFile`, and `fork`.**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
- `spawn`: Starts a new process with a command. Best for large data as it uses streams.
- `exec`: Spawns a shell and runs a command, buffering the output. Best for small data payloads.
- `execFile`: Similar to `exec`, but executes the file directly without spawning a shell (more secure and faster).
- `fork`: A special case of `spawn` designed specifically to run Node.js modules. It establishes a built-in IPC channel for communication between parent and child.

</details>

<hr/>

### ❓ Q63. **How do you handle distributed tracing in a microservices ecosystem?**
*(No answer provided. Discuss OpenTelemetry, Jaeger, Zipkin, correlation IDs.)*

<hr/>

### ❓ Q64. **Explain the concept of continuous integration and continuous deployment (CI/CD) for Node.js.**
*(No answer provided. Discuss automated testing, Dockerizing, deployment pipelines.)*

<hr/>

### ❓ Q65. **How do you secure a Node.js application in production?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
- Use Helmet.js to set secure HTTP headers.
- Validate and sanitize input to prevent SQL/NoSQL injection and XSS.
- Implement rate limiting (e.g., `express-rate-limit`) to prevent brute force and DDoS.
- Use bcrypt/Argon2 for password hashing.
- Keep dependencies updated (use `npm audit`).
- Run Node.js as a non-root user.
- Use TLS/SSL (HTTPS).

</details>

<hr/>

### ❓ Q66. **What are the best practices for structuring a large Node.js application?**
*(No answer provided. Discuss layered architecture, controllers, services, repositories.)*

<hr/>

### ❓ Q67. **How do you implement rate limiting and throttling?**
*(No answer provided. Discuss Redis rate limiting, token bucket algorithm.)*

<hr/>

### ❓ Q68. **Explain GraphQL and how it compares to REST.**
*(No answer provided. Discuss over-fetching, under-fetching, single endpoint.)*

<hr/>

### ❓ Q69. **How do you optimize API latency in Node.js?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
- Add caching (Redis/Memcached) for database queries and HTTP responses.
- Optimize database queries (indexing, avoiding N+1 problem).
- Implement pagination.
- Compress responses using Gzip/Brotli.
- Use a CDN for static assets.
- Keep the event loop unblocked.

</details>

<hr/>

### ❓ Q70. **What is server-side rendering (SSR) vs client-side rendering (CSR)?**
*(No answer provided. Discuss Next.js vs React SPA, SEO implications.)*

<hr/>

### ❓ Q71. **How do you handle graceful shutdown in a Node.js application?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
When an application receives a termination signal (`SIGTERM` or `SIGINT`), it shouldn't abruptly close. 
1. Stop accepting new connections.
2. Finish processing ongoing requests.
3. Close database and external service connections cleanly.
4. Exit the process.
```javascript
process.on('SIGTERM', () => {
  server.close(() => {
    mongoose.connection.close(false, () => {
      process.exit(0);
    });
  });
});
```

</details>

<hr/>

### ❓ Q72. **What are the security risks associated with npm packages?**
*(No answer provided. Discuss typosquatting, malicious code execution post-install.)*

<hr/>

### ❓ Q73. **How do you implement OAuth2 in Node.js?**
*(No answer provided. Discuss Passport.js, access tokens, refresh tokens.)*

<hr/>

### ❓ Q74. **Explain the role of an API Gateway.**
*(No answer provided. Discuss routing, rate limiting, authentication offloading.)*

<hr/>

### ❓ Q75. **How do you use Redis for caching in Node.js?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
Redis is an in-memory data structure store. In Node.js, caching is typically implemented via middleware. When a request comes in:
1. Check if the requested data exists in Redis.
2. If yes (cache hit), return it immediately.
3. If no (cache miss), query the database, store the result in Redis with an expiration time (TTL), and return the data.

</details>

<hr/>

---

## 🟣 Expert Level

### ❓ Q76. **Design a concurrent job queue system in Node.js.**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
A robust job queue requires a message broker (like Redis or RabbitMQ) and worker processes.
1. **Producer:** The main Node.js API accepts a request and pushes a job object into Redis.
2. **Queue Management:** Use a library like BullMQ or Agenda to manage retries, concurrency, and delayed jobs.
3. **Consumers (Workers):** Separate Node.js processes constantly poll or listen to the queue. When a job appears, a worker takes it, executes the heavy processing, and updates the job status.

</details>

<hr/>

### ❓ Q77. **How would you architect a distributed locking mechanism using Redis and Node.js?**
*(No answer provided. Discuss Redlock algorithm, SETNX, TTL.)*

<hr/>

### ❓ Q78. **Explain how you would write a native C++ addon for Node.js using N-API.**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
N-API (Node-API) allows building native addons in C/C++ that are compiled once and work across multiple Node.js versions without recompilation. 
1. Write the C++ logic.
2. Use `<node_api.h>` to wrap C++ functions into JS-callable functions.
3. Define the module initialization.
4. Create a `binding.gyp` file to configure the build.
5. Use `node-gyp rebuild` to compile the module into a `.node` file, which is then `require()`d in JavaScript.

</details>

<hr/>

### ❓ Q79. **Design a highly available chat application handling millions of concurrent connections.**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
- **Connection Handling:** Use a fleet of Node.js WebSocket servers behind an HAProxy or AWS ALB load balancer.
- **State Management:** WebSockets are stateful. Use Redis Pub/Sub so instances can broadcast messages to users connected to other instances.
- **Scaling:** Automatically scale out server instances based on CPU and memory metrics.
- **Persistence:** Offload chat history to a fast, append-only database like Cassandra or DynamoDB via an asynchronous message queue (Kafka) to prevent blocking the WebSocket servers.

</details>

<hr/>

### ❓ Q80. **How would you handle a memory leak in a production environment with zero downtime?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
If a leak is detected in production:
1. **Mitigation:** Use PM2 to set a `--max-memory-restart` limit, ensuring the process gracefully restarts before crashing the server. Deploy multiple instances behind a load balancer so restarts don't drop traffic.
2. **Investigation:** Take heap snapshots (`v8.writeHeapSnapshot()`) dynamically. Use tools like Datadog or Node Clinic.
3. **Resolution:** Analyze the heap dumps locally to find retained sizes of objects (usually arrays, Maps, or unclosed event listeners), deploy the fix, and remove the PM2 memory restart limit.

</details>

<hr/>

### ❓ Q81. **Explain the inner workings of the `require` function and module caching.**
*(No answer provided. Discuss Resolution, Loading, Wrapping, Evaluation, and Caching phases.)*

<hr/>

### ❓ Q82. **Design an API rate limiter from scratch.**
*(No answer provided. Discuss sliding window log, token bucket, Redis lua scripts.)*

<hr/>

### ❓ Q83. **How do you achieve true parallelism in Node.js?**
*(No answer provided. Discuss worker_threads and shared array buffers.)*

<hr/>

### ❓ Q84. **Design a scalable file storage system similar to Amazon S3.**
*(No answer provided. Discuss chunking, metadata vs blob storage, CDNs, distributed hash tables.)*

<hr/>

### ❓ Q85. **Explain how you would implement a custom stream in Node.js.**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
You extend the stream classes from the `stream` module and implement specific methods.
- **Readable:** Extend `Readable`, implement `_read(size)`. Use `this.push(data)` to emit data.
- **Writable:** Extend `Writable`, implement `_write(chunk, encoding, callback)`.
- **Transform:** Extend `Transform`, implement `_transform(chunk, encoding, callback)`.

</details>

<hr/>

### ❓ Q86. **How would you optimize the startup time of a large Node.js application?**
*(No answer provided. Discuss lazy loading requires, snapshotting, reducing dependencies.)*

<hr/>

### ❓ Q87. **Design a notification system (Push, Email, SMS) with guaranteed delivery.**
*(No answer provided. Discuss DLQs, idempotency, retry mechanisms with exponential backoff.)*

<hr/>

### ❓ Q88. **How do you handle database migrations in a CI/CD pipeline without downtime?**
*(No answer provided. Discuss backward-compatible schema changes, expand-and-contract pattern.)*

<hr/>

### ❓ Q89. **Explain the implementation of a reverse proxy in Node.js.**
*(No answer provided. Discuss http-proxy module, streaming requests and responses.)*

<hr/>

### ❓ Q90. **Design a distributed caching strategy for a microservices architecture.**
*(No answer provided. Discuss cache invalidation, cache-aside, write-through, read-through.)*

<hr/>

### ❓ Q91. **How would you monitor and alert on Node.js application health in a large-scale deployment?**
*(No answer provided. Discuss RED metrics, Prometheus, Grafana, custom APM.)*

<hr/>

### ❓ Q92. **Design an idempotent API. Why is it important?**
*(No answer provided. Discuss idempotency keys, avoiding duplicate charges or actions.)*

<hr/>

### ❓ Q93. **Explain the consensus algorithm (like Raft) and how you might use it in a Node distributed system.**
*(No answer provided. Discuss leader election, log replication.)*

<hr/>

### ❓ Q94. **How do you handle eventual consistency in distributed systems?**
*(No answer provided. Discuss sagas, compensating transactions.)*

<hr/>

### ❓ Q95. **Design a real-time collaborative text editor (like Google Docs) using Node.js.**
*(No answer provided. Discuss Operational Transformation (OT) or CRDTs, WebSockets.)*

<hr/>

### ❓ Q96. **How would you trace a performance issue across multiple microservices?**
*(No answer provided. Discuss distributed tracing headers, OpenTelemetry.)*

<hr/>

### ❓ Q97. **Explain the concept of CQRS and Event Sourcing in Node.js applications.**
*(No answer provided. Discuss separating read/write models, event streams.)*

<hr/>

### ❓ Q98. **Design a scalable web scraper.**
*(No answer provided. Discuss puppeteer, rotating proxies, queues, un-blocking the event loop.)*

<hr/>

### ❓ Q99. **How would you implement dynamic module loading without restarting the application?**
*(No answer provided. Discuss require cache invalidation, though mention risks of memory leaks.)*

<hr/>

### ❓ Q100. **Design a scalable pub/sub messaging system.**
*(No answer provided. Discuss Kafka concepts, partitions, consumer groups.)*

<hr/>

---

### 🧭 Navigation

| ⬅️ Previous | 🏠 Index | ➡️ Next |
| :--- | :---: | ---: |
| [⬅️ JavaScript](./01_Javascript.md) | [Home](./00_Index.md) | 🚫 *None* |
