# Khelo Tech & Strategy — Back-End Developer (Node.js) Interview Prep Guide

This guide is custom-tailored to the Job Description of **Khelo Tech & Strategy Pvt. Ltd.** for a **Back-End Developer (3 Years Experience)**. It covers JavaScript, Node.js, Express, databases (MySQL), microservices, system design, and preferred skills (React, AWS, Docker, Kubernetes). 

All answers are wrapped in `<details>` tags to enable active recall. Try to answer the question yourself before expanding the accordion!

---

## Table of Contents
1. [JavaScript & Node.js Core](#1-javascript--nodejs-core)
2. [RESTful APIs & Express.js](#2-restful-apis--expressjs)
3. [Database Engineering (MySQL)](#3-database-engineering-mysql)
4. [Microservices Architecture](#4-microservices-architecture)
5. [Cloud, DevOps & Containerization](#5-cloud-devops--containerization)
6. [Frontend Integration (React & Full-Stack)](#6-frontend-integration-react--full-stack)
7. [System Design & Scenario-Based (Gaming/Strategy Context)](#7-system-design--scenario-based-gamingstrategy-context)

---

## 1. JavaScript & Node.js Core

### ❓ Q1. What is Node.js, and how does it work under the hood?
<details>
<summary><b>👀 Show Answer</b></summary>

*   **Detailed Answer:**
    Node.js is an open-source, cross-platform, single-threaded JavaScript runtime environment built on Google Chrome's V8 JavaScript engine. It allows developers to execute JavaScript code on the server-side, outside a web browser.
    
    **Core Architectural Components:**
    1.  **V8 Engine:** A high-performance engine written in C++ that compiles JavaScript directly into native machine code before executing it.
    2.  **libuv:** A multi-platform C library that focuses on asynchronous I/O. It provides the event loop, thread pool, and file system/networking capabilities.
    3.  **C++ Bindings (Node.js API):** Wrappers that bridge JavaScript calls to low-level C++ implementations in V8 and libuv.

    **Key Characteristics:**
    *   **Single-Threaded:** Node.js executes JavaScript code on a single main thread, avoiding context-switching and complex synchronization overhead.
    *   **Non-Blocking I/O:** I/O operations (like reading files or network requests) are delegated to the operating system or libuv's thread pool, allowing the main thread to handle other tasks concurrently.
    *   **Event-Driven:** It uses the Observer pattern. When an asynchronous operation completes, it triggers a callback event to be processed by the event loop.

*   **Real-world Example:**
    In a traditional multi-threaded server (like Apache/PHP), each client request spawns a new thread. If the thread queries a database, it blocks and waits. If 10,000 users query at the same time, the server runs out of thread memory.
    In Node.js, the single thread receives the database query request, registers a callback, and moves on to accept the next user request. When the database returns data, the event loop schedules the callback to send the response back.

*   **Common Mistakes:**
    *   Thinking Node.js is a programming language or framework. It is a runtime environment.
    *   Assuming Node.js is completely single-threaded. JavaScript execution is single-threaded, but libuv runs a thread pool (default 4 threads) for heavy tasks, and the OS handles networking in its own threads.

*   **Follow-up Questions:**
    *   *Why is Node.js not suitable for CPU-intensive tasks?* Because CPU-intensive tasks block the single thread, preventing any other events or requests from being handled until the calculation finishes.
    *   *What is the difference between Node.js and a web browser runtime?* Both use V8 (in Chrome), but browsers provide Web APIs (DOM, fetch, window), while Node.js provides server-side APIs (fs, path, process, require).

</details>

<hr/>

### ❓ Q2. Is Node.js synchronous or asynchronous?
<details>
<summary><b>👀 Show Answer</b></summary>

*   **Detailed Answer:**
    Node.js is **both synchronous and asynchronous**, depending on how it executes code vs. how it handles I/O operations:
    
    1.  **Synchronous (JavaScript Execution):**
        *   JavaScript is run on a single main thread (the call stack).
        *   All synchronous code runs sequentially, line-by-line. If a function is blocking (e.g. CPU-heavy math calculations, large JSON serialization, or synchronous file operations like `fs.readFileSync`), it freezes execution and blocks other operations.
    2.  **Asynchronous (I/O Operations):**
        *   Node.js runtime delegates I/O actions (filesystem, database access, network calls, encryption) to the operating system or **libuv's internal thread pool**.
        *   Once delegated, the call stack is cleared, allowing Node.js to immediately accept other requests.
        *   When an asynchronous task completes, it places its callback/promise into the event loop queue, which eventually gets executed on the main thread.

*   **Real-world Example:**
    *   *Synchronous blocking behavior:*
        ```javascript
        const data = fs.readFileSync('file.txt'); // Blocks the entire server until read completes
        console.log(data);
        ```
    *   *Asynchronous non-blocking behavior:*
        ```javascript
        fs.readFile('file.txt', (err, data) => { // Does not block; read runs in background
          console.log(data);
        });
        ```

*   **Common Mistakes:**
    *   Believing Node.js runs asynchronous tasks in parallel on separate JavaScript execution threads. JavaScript always runs on a single main thread; parallel worker threads are only utilized via libuv C++ background tasks.
    *   Using synchronous methods (like `fs.writeFileSync` or `crypto.pbkdf2Sync`) inside web request-response loops in production APIs.

*   **Follow-up Questions:**
    *   *How does the Event Loop check for completed asynchronous tasks?* It polls libuv and system-level events at different phases of each loop iteration.
    *   *What are some examples of APIs in Node.js that are strictly synchronous?* Array operations (like `map`, `filter`), JSON operations (`JSON.stringify`, `JSON.parse`), and any function containing the `Sync` suffix (e.g. `fs.readFileSync`).

</details>

<hr/>

### ❓ Q3. How does the Node.js Event Loop work? Explain the execution phases and the behavior of the Microtask Queue.
<details>
<summary><b>👀 Show Answer</b></summary>

*   **Detailed Answer:**
    Node.js runs on a single-threaded execution model backed by the **V8 Engine** and **libuv** (which handles platform-specific asynchronous I/O and the background thread pool). The **Event Loop** is a continuous loop that orchestrates asynchronous operations across **6 main phases**:

    1.  **Timers:** Checks a min-heap structure containing registered timer thresholds. Executes expired callbacks scheduled by `setTimeout()` and `setInterval()`.
    2.  **Pending Callbacks:** Executes deferred system-level I/O callbacks from the previous loop iteration, such as specific TCP connection errors (`ECONNREFUSED`).
    3.  **Idle, Prepare:** Used internally by libuv for housekeeping operations and alignment hook routines. Developers' JavaScript code never executes in this phase.
    4.  **Poll:** The core phase that retrieves new I/O events. The loop behaves as follows:
        *   If the Poll queue contains active callbacks (e.g. database query replies, incoming network requests), it runs them synchronously until drained or a system safety limit is reached.
        *   If the Poll queue is empty and there are `setImmediate()` callbacks, it exits the Poll phase and goes to the Check phase.
        *   If the queue is empty and there are no `setImmediate()` callbacks, the loop calculates the wait time before any registered timer expires, and **blocks (waits)** in this phase to prevent 100% CPU utilization while idle.
    5.  **Check:** Executes callbacks registered via `setImmediate()`. This phase is designed to execute immediately after Poll I/O callbacks.
    6.  **Close Callbacks:** Executes close-event callbacks (e.g., `socket.on('close', ...)`), cleaning up handles and releasing system file descriptors.

    **Microtask Queue (process.nextTick & Promises):**
    The Microtask Queue is managed by Node.js/V8 and is **not** a part of the libuv event loop phases. It is split into `process.nextTick` callbacks (highest priority) and Promise resolution/rejections.
    *   **Execution Rule:** The microtask queues are completely drained **immediately after the current operation finishes**, before the event loop transitions to the next phase, and between individual callback executions within a phase.

*   **Real-world Example:**
    Consider the following code executed during an I/O callback:
    ```javascript
    fs.readFile('test.txt', () => {
      setTimeout(() => console.log('1. Timeout'), 0);
      setImmediate(() => console.log('2. Immediate'));
      process.nextTick(() => console.log('3. nextTick'));
      Promise.resolve().then(() => console.log('4. Promise'));
    });
    ```
    **Output Order:**
    1. `3. nextTick` (Executes immediately when the current I/O execution stack clears)
    2. `4. Promise` (Drains right after the nextTick queue finishes)
    3. `2. Immediate` (The loop transitions to the **Check** phase, executing `setImmediate` next)
    4. `1. Timeout` (The loop wraps up the cycle and starts the next iteration, executing the expired timer callback in the **Timers** phase)

*   **Common Mistakes:**
    *   Assuming `setTimeout(..., 0)` always executes before `setImmediate()`. Inside the main process, execution is non-deterministic, but inside an I/O callback, `setImmediate` is guaranteed to run first.
    *   Starving the event loop by calling recursive `process.nextTick()` chains. Since V8 must drain the microtask queue completely before passing to the next phase, recursive nextTicks will lock the loop indefinitely.

*   **Follow-up Questions:**
    *   *Why is Poll the longest-running phase?* Because Node.js blocks there waiting for network/socket/disk connections, keeping the process alive when idle.
    *   *What determines if the event loop should exit?* Libuv keeps a reference counter of active handles (ports, timers, socket descriptors) and active requests. When the count reaches 0, the event loop exits.

</details>

<hr/>

### ❓ Q4. Explain Streams and Buffers. How do you handle Backpressure in Node.js?
<details>
<summary><b>👀 Show Answer</b></summary>

*   **Detailed Answer:**
    *   **Buffer:** A temporary chunk of physical memory (RAM) allocated outside the V8 heap. It is used to represent and store a raw sequence of binary bytes.
    *   **Stream:** A mechanism for reading or writing data chunk-by-chunk sequentially, rather than loading the entire payload into memory. The four types of streams are `Readable`, `Writable`, `Duplex` (e.g., TCP sockets), and `Transform` (e.g., gzip compression).
    *   **Backpressure:** Occurs when a `Readable` stream produces data much faster than the matching `Writable` stream can consume it. If unhandled, chunks accumulate in system memory, leading to memory exhaustion and server crashes.

    **Handling Backpressure:**
    When writing data, if the Writable stream's internal buffer exceeds its limit (`highWaterMark`), `.write(chunk)` returns `false`. This signals the system to pause the Readable stream. Once the Writable stream drains its queue, it fires a `'drain'` event, telling the Readable stream to call `.resume()`. 
    
    Using `.pipe()` or `stream.pipeline()` handles this flow control automatically.

*   **Real-world Example:**
    Streaming a large log file from disk directly to an HTTP response safely:
    ```javascript
    const fs = require('fs');
    const { pipeline } = require('stream');

    app.get('/download-logs', (req, res) => {
      const source = fs.createReadStream('./massive-error-log.txt');
      
      // pipeline handles backpressure and cleans up descriptors on error/finish
      pipeline(source, res, (err) => {
        if (err) {
          console.error('Pipeline failed:', err);
          if (!res.headersSent) {
            res.status(500).send('Streaming error');
          }
        }
      });
    });
    ```

*   **Common Mistakes:**
    *   Using `fs.readFile()` to process file uploads or downloads. If a 1GB file is uploaded, it consumes 1GB of memory on the server. Multiple concurrent requests will quickly trigger an Out-Of-Memory (OOM) crash.
    *   Manually using `.pipe()` without registering error handlers on both the readable and writable streams, which causes unhandled exceptions to crash the process. Use `stream.pipeline` instead.

*   **Follow-up Questions:**
    *   *What is the default `highWaterMark` for binary and object streams?* By default, 64KB for binary streams, and 16 objects for object mode streams.
    *   *What is the difference between Duplex and Transform streams?* A Duplex stream has independent read and write channels (like a socket). A Transform stream is a Duplex stream where the output is dynamically computed from the input (like encrypting data as it passes through).

</details>

<hr/>

### ❓ Q5. When would you use Worker Threads vs. the Cluster Module in Node.js?
<details>
<summary><b>👀 Show Answer</b></summary>

*   **Detailed Answer:**
    Node.js provides two main concurrency tools for multi-core processors:
    
    *   **Cluster Module:**
        *   **Mechanics:** Spawns multiple physical instances of the same Node.js process (each running its own V8 engine, event loop, and memory heap). They share the same server port.
        *   **Use Case:** Scaling I/O-bound network applications. It is ideal for running an Express API across multiple cores to increase request-handling capacity.
        *   **Communication:** Inter-process communication (IPC) via message passing.
        
    *   **Worker Threads (`worker_threads`):**
        *   **Mechanics:** Spawns lightweight execution threads within the *same* process. All threads share the same process memory space, allowing them to pass array buffers efficiently without serialization overhead.
        *   **Use Case:** Offloading CPU-intensive calculations (e.g., cryptography, image compression, heavy math, PDF generation) from the event loop thread to prevent blocking client requests.
        *   **Communication:** Message passing via `MessageChannel` or shared memory using `SharedArrayBuffer`.

*   **Real-world Example:**
    *   **Cluster:** Spawning workers to handle web requests on an Express server:
        ```javascript
        const cluster = require('cluster');
        const os = require('os');

        if (cluster.isPrimary) {
          const numCPUs = os.cpus().length;
          for (let i = 0; i < numCPUs; i++) {
            cluster.fork();
          }
        } else {
          // Express app listening on port 3000
          app.listen(3000);
        }
        ```
    *   **Worker Threads:** Running a heavy password hashing function in a background worker:
        ```javascript
        const { Worker, isMainThread, parentPort, workerData } = require('worker_threads');

        if (isMainThread) {
          const worker = new Worker(__filename, { workerData: 'hashMePlease' });
          worker.on('message', (hash) => console.log('Hashed password:', hash));
        } else {
          const crypto = require('crypto');
          const result = crypto.scryptSync(workerData, 'salt', 64).toString('hex');
          parentPort.postMessage(result);
        }
        ```

*   **Common Mistakes:**
    *   Using Worker Threads for database queries or API calls. These tasks are already handled asynchronously by libuv under the hood; spawning workers introduces unnecessary thread-switching overhead.
    *   Spawning a new Worker Thread dynamically on every single HTTP request. Creating threads is expensive. Use a **Worker Pool** library instead to reuse threads.

*   **Follow-up Questions:**
    *   *How does the Cluster module load balance incoming connections?* On Windows, the master process hands off sockets to workers. On Unix-based systems, it uses a round-robin approach by default.
    *   *What are the risks of using `SharedArrayBuffer` in Worker Threads?* Race conditions. If multiple threads write to the same memory address simultaneously without synchronization (`Atomics`), data corruption occurs.

</details>

<hr/>

### ❓ Q6. How do you identify, trace, and prevent Memory Leaks in Node.js?
<details>
<summary><b>👀 Show Answer</b></summary>

*   **Detailed Answer:**
    A memory leak occurs when reference points to unused objects remain reachable in the application, preventing the V8 Garbage Collector (GC) from reclaiming memory.

    **Common Root Causes:**
    1.  **Global Variables:** Accidental assignment of values to variables on the global scope (`global.someCache = ...`).
    2.  **Closures:** Inner functions holding references to outer scope variables that are no longer needed.
    3.  **Dangling Event Listeners:** Registering event listeners on long-lived objects (e.g., `process.on('message')` or custom event emitters) without ever removing them when cleaning up.
    4.  **Uncapped In-Memory Caches:** Storing query responses in a plain JavaScript object without TTL expiration or item limits.

    **Detection & Tracing Workflow:**
    1.  **Monitor:** Use tools like AWS CloudWatch, PM2, or Prometheus/Grafana to track memory usage patterns. A slow, continuous upward trend under load is a classic leak.
    2.  **Inspect:** Start Node with the `--inspect` flag:
        ```bash
        node --inspect index.js
        ```
    3.  **Snapshot:** Open Chrome DevTools (`chrome://inspect`) and connect to the Node.js process. Take a **Heap Snapshot** when the server starts.
    4.  **Simulate Load:** Use benchmarking tools like `autocannon` or `wrk` to send thousands of concurrent requests to the endpoints.
    5.  **Compare:** Take a second heap snapshot and use the "Comparison" view to analyze which objects increased in count. Inspect the **Retainer Tree** to see what variables are holding onto those references.

*   **Real-world Example:**
    An endpoint appending user data to an external array on every request:
    ```javascript
    const activeSessions = []; // Leaks memory indefinitely

    app.get('/login', (req, res) => {
      activeSessions.push({ id: req.query.id, time: Date.now() });
      res.send('Logged In');
    });
    ```
    **Resolution:** Use a capped cache with TTL like `lru-cache`, or persist session mappings in a dedicated database like Redis.

*   **Common Mistakes:**
    *   Confusing elevated memory usage with a leak. Node.js may delay garbage collection until the heap is nearly full to conserve CPU cycles.
    *   Implementing custom in-memory caching mechanisms without size bounds.

*   **Follow-up Questions:**
    *   *How does V8's Generational GC work?* It splits memory into two regions: the *New Space* (short-lived, fast collection using Scavenge algorithm) and the *Old Space* (long-lived, collected using Mark-Sweep-Compact).
    *   *How can you force Garbage Collection manually for testing?* Start the application with `node --expose-gc index.js` and execute the `global.gc()` method.

</details>

---

## 2. RESTful APIs & Express.js

### ❓ Q7. How does the Express middleware execution flow work? How do you implement global error-handling for synchronous and asynchronous routes?
<details>
<summary><b>👀 Show Answer</b></summary>

*   **Detailed Answer:**
    Express middleware functions have access to the request (`req`), response (`res`), and the `next` function in the application's request-response cycle. Middlewares run sequentially in the order they are registered via `app.use()` or route definitions.
    
    If a middleware does not terminate the request (by sending a response), it **must** call `next()` to pass control to the subsequent middleware. Failing to call `next()` leaves the request hanging until client timeout.

    **Error-Handling Middleware:**
    An error-handling middleware is defined by providing exactly **4 arguments**: `(err, req, res, next)`. Express identifies it by its signature length. It must be declared *after* all other route handlers and regular middlewares.

    **Async Errors Handling:**
    *   In Express v4, errors thrown inside asynchronous functions (like database queries) are **not** automatically caught by Express. They result in an "Unhandled Promise Rejection" which can crash the server. You must explicitly catch the error and pass it to `next(err)`.
    *   In Express v5, errors thrown inside async handlers are automatically forwarded to the error middleware, but many production apps still run v4.

*   **Real-world Example:**
    Handling async errors clean and defining a global error middleware:
    ```javascript
    // Helper to wrap async route handlers
    const asyncHandler = (fn) => (req, res, next) => {
      Promise.resolve(fn(req, res, next)).catch(next);
    };

    // Async controller using the wrapper
    app.get('/user/:id', asyncHandler(async (req, res) => {
      const user = await db.findUserById(req.params.id);
      if (!user) {
        const err = new Error('User not found');
        err.statusCode = 404;
        throw err; // Caught by asyncHandler and passed to next(err)
      }
      res.json(user);
    }));

    // Global Error Middleware (MUST be registered last)
    app.use((err, req, res, next) => {
      const statusCode = err.statusCode || 500;
      console.error(`[Error] ${err.message}`, err.stack);
      res.status(statusCode).json({
        success: false,
        error: err.message || 'Internal Server Error'
      });
    });
    ```

*   **Common Mistakes:**
    *   Defining the global error handler middleware with only 3 parameters `(req, res, next)`. Express will treat it as a regular middleware, and it will not receive the error object.
    *   Forgetting to return after calling `next(err)`. The execution will continue in the current function block, potentially triggering double-response errors.

*   **Follow-up Questions:**
    *   *What happens if you call next('some string')?* Express skips all remaining routing and regular middlewares in the stack and jumps straight to the registered error-handling middleware.
    *   *How do you handle uncaught exceptions outside route handlers?* Listen to the process-level events:
        ```javascript
        process.on('uncaughtException', (err) => {
          console.error('Uncaught Exception:', err);
          process.exit(1); // Exit process immediately
        });
        ```

</details>

<hr/>

### ❓ Q8. What are the key architectural constraints of a RESTful API? How do you manage API Versioning in production?
<details>
<summary><b>👀 Show Answer</b></summary>

*   **Detailed Answer:**
    A REST (Representational State Transfer) API relies on **6 architectural constraints**:
    1.  **Client-Server:** Decoupling front-end concerns from back-end data storage.
    2.  **Stateless:** Each request from client to server must contain all the information necessary to understand and process the request. The server holds no session context.
    3.  **Cacheable:** Responses must explicitly define themselves as cacheable or non-cacheable to optimize network efficiency.
    4.  **Uniform Interface:** Simplifies architecture through uniform resource URI design, manipulation of resources through representations, self-descriptive messages, and HATEOAS.
    5.  **Layered System:** Clients cannot tell whether they are connected directly to the end server or intermediate nodes (like Load Balancers or CDNs).
    6.  **Code on Demand (Optional):** Servers can temporarily extend client functionality by transferring executable code (e.g., scripts).

    **API Versioning Strategies:**
    To introduce breaking updates without disrupting existing active clients:
    *   **URI Path Versioning (Recommended for clarity):** `https://api.khelotech.com/v1/users`
    *   **Header Versioning (Accept/Custom headers):** `Accept: application/vnd.khelotech.v2+json` or `X-API-Version: 2`
    *   **Query Parameter Versioning:** `https://api.khelotech.com/users?version=2`

*   **Real-world Example:**
    Implementing URI routing for versions in Express:
    ```javascript
    const express = require('express');
    const app = express();

    const v1Router = require('./routes/v1');
    const v2Router = require('./routes/v2');

    app.use('/api/v1', v1Router);
    app.use('/api/v2', v2Router);
    ```

*   **Common Mistakes:**
    *   Using HTTP POST for safe retrieving operations (which should be GET) or using GET requests to modify database states.
    *   Failing to return appropriate HTTP status codes (e.g., returning `200 OK` with a body payload containing `{ error: "Access Denied" }` instead of returning a proper `403 Forbidden`).

*   **Follow-up Questions:**
    *   *What is the difference between PUT and PATCH methods?* PUT replaces the entire target resource with the request payload. PATCH applies partial modifications to the resource.
    *   *What does Idempotency mean in REST?* An HTTP method is idempotent if executing it multiple times yields the same resource state. `GET`, `PUT`, `DELETE`, and `HEAD` are idempotent. `POST` is NOT idempotent.

</details>

<hr/>

### ❓ Q9. How do you implement robust JWT Authentication, Refresh Token Rotation, and secure Cookies?
<details>
<summary><b>👀 Show Answer</b></summary>

*   **Detailed Answer:**
    A secure authentication architecture separates credentials into two JWT tokens:
    1.  **Access Token:** Short-lived (e.g., 15 minutes). Sent in requests to authenticate access to protected API resources.
    2.  **Refresh Token:** Long-lived (e.g., 7 days). Used to request a new access token once it expires.

    **Secure Storage:**
    *   **Access Token:** Stored in client application memory (JavaScript state). Never save it in `localStorage` or `sessionStorage` as it is vulnerable to Cross-Site Scripting (XSS) attacks.
    *   **Refresh Token:** Sent from the server in an `httpOnly`, `secure` cookie with `sameSite: 'strict'`. This prevents JavaScript scripts from reading the cookie, shielding it from XSS.

    **Refresh Token Rotation (Security Best Practice):**
    To detect and prevent replay attacks if a refresh token is stolen:
    *   Every time a refresh token is used to get a new access token, the server invalidates that refresh token and issues a **new** one.
    *   The server maintains a database store of active refresh tokens.
    *   If a client requests a new access token using a *previously used/invalidated* refresh token, the server assumes malicious activity. It invalidates the entire family of refresh tokens associated with that user, forcing a re-login.

*   **Real-world Example:**
    Issuing tokens and cookies in Express:
    ```javascript
    const jwt = require('jsonwebtoken');

    app.post('/login', async (req, res) => {
      const user = await db.validateUser(req.body.email, req.body.password);
      
      const accessToken = jwt.sign({ userId: user.id }, process.env.ACCESS_SECRET, { expiresIn: '15m' });
      const refreshToken = jwt.sign({ userId: user.id }, process.env.REFRESH_SECRET, { expiresIn: '7d' });

      // Save refresh token to DB/Redis for active-session validation and tracking
      await redis.setex(`refresh_token:${user.id}:${refreshToken}`, 7 * 24 * 3600, 'active');

      // Send refresh token inside secure cookie
      res.cookie('refreshToken', refreshToken, {
        httpOnly: true,
        secure: true, // Requires HTTPS
        sameSite: 'strict',
        maxAge: 7 * 24 * 60 * 60 * 1000 // 7 days
      });

      res.json({ accessToken });
    });
    ```

*   **Common Mistakes:**
    *   Signing sensitive data like user passwords or PII (Personally Identifiable Information) inside the JWT payload. Anyone can decode the base64 payload of a JWT.
    *   Setting CORS `Access-Control-Allow-Origin: '*'` while trying to read secure credentials/cookies. For secure cookie transport, you must set specific origins and enable `credentials: true`.

*   **Follow-up Questions:**
    *   *What are the main claims in a JWT header and payload?* Header contains algorithm (`alg`) and type (`typ`). Payload contains registered claims like issuer (`iss`), expiration (`exp`), subject (`sub`), and custom claims (e.g., roles).
    *   *How do you handle instant user logout/token revocation since JWTs are stateless?* Maintain a Redis blacklist of revoked tokens with their remaining TTL, and check this cache during request auth checks.

</details>

---

## 3. Database Engineering (MySQL)

### ❓ Q10. How do you design, optimize, and choose indexes in MySQL? (B-Tree vs. Hash)
<details>
<summary><b>👀 Show Answer</b></summary>

*   **Detailed Answer:**
    An index speeds up search queries by avoiding slow Full Table Scans (`ALL` in MySQL).
    
    **Index Storage Structures in MySQL:**
    *   **B-Tree Index (Default in MySQL InnoDB):**
        *   **Mechanics:** Self-balancing search tree.
        *   **Best For:** Equality matches (`=`), Range queries (`>`, `<`, `BETWEEN`), prefix matches (`LIKE 'abc%'`), and sorting (`ORDER BY`).
    *   **Hash Index (Used mainly in Memory storage engine):**
        *   **Mechanics:** Uses hash tables mapping keys directly to row addresses.
        *   **Best For:** Pure equality matches (`=`).
        *   **Limitations:** Cannot perform range lookups or sort query operations.
    *   **Prefix Indexing (MySQL Specific):**
        *   **Mechanics:** Indexing only the first $N$ characters of a long string/VARCHAR column to save index space and RAM while maintaining fast lookup.

    **Compound Index Optimization (ESR Rule):**
    When combining fields in a compound index in MySQL, arrange fields in order of:
    1.  **E**quality: Fields searched for exact values (e.g., `WHERE status = 'ACTIVE'`).
    2.  **S**ort: Fields used to order query results (e.g., `ORDER BY score DESC`).
    3.  **R**ange: Fields queried with inequalities (e.g., `WHERE age > 18`).

*   **Real-world Example:**
    If you frequently execute:
    ```sql
    SELECT * FROM match_history 
    WHERE user_id = 9982 AND status = 'COMPLETED' 
    ORDER BY finished_at DESC;
    ```
    Creating a compound index:
    *   *Incorrect:* Index on `(finished_at, user_id, status)`
    *   *Correct (ESR):* Index on `(user_id, status, finished_at)` (Equality columns first, sorting last).

*   **Common Mistakes:**
    *   Adding indexes to columns with low selectivity (e.g., a "gender" column containing only 2 distinct values). The MySQL query optimizer will ignore the index and run a full table scan anyway.
    *   Creating too many indexes. Every write operation (insert, update, delete) requires updating the index trees, which slows down write performance.

*   **Follow-up Questions:**
    *   *What is a covering index in MySQL?* A query where all requested output fields are already part of the index structure itself, allowing the database to return results directly from the index (Index Only Scan) without executing a lookup on the clustered primary index table.
    *   *How does the InnoDB Buffer Pool affect index performance?* The Buffer Pool caches table and index data in RAM. If indexes do not fit within the Buffer Pool, performance drops significantly as MySQL has to swap data blocks to disk.

</details>

<hr/>

### ❓ Q11. How do you read and optimize MySQL queries using EXPLAIN plans?
<details>
<summary><b>👀 Show Answer</b></summary>

*   **Detailed Answer:**
    Explain plans show the execution pathway chosen by the MySQL query optimizer. To generate, prepend your query with `EXPLAIN` or `EXPLAIN ANALYZE <query>` (in MySQL 8.0+).

    **Key Columns to Analyze in MySQL `EXPLAIN`:**
    *   **`type` (Join Type):** Tells you how MySQL scans the table.
        *   *Bad:* `ALL` (Full table scan).
        *   *Good:* `const` (primary key/unique index lookup), `ref` (non-unique index match), `range` (index range scan, e.g. using `BETWEEN` or `>`).
    *   **`key`:** The actual index MySQL decided to use. If `NULL`, no index is used.
    *   **`rows`:** MySQL's estimate of the number of rows it needs to examine to execute the query.
    *   **`filtered`:** The estimated percentage of rows filtered by the query condition. A high value is better.
    *   **`Extra`:** Additional execution detail. Look out for:
        *   *Bad:* `Using filesort` (MySQL must sort the results in memory/disk temp files because there is no pre-sorted index).
        *   *Bad:* `Using temporary` (MySQL creates an internal temporary table to resolve the query).
        *   *Good:* `Using index` (Covering index is used; data retrieved directly from the index tree).

*   **Real-world Example (MySQL):**
    Running explanation on a slow query:
    ```sql
    EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'nishant@khelo.com';
    ```
    **Output fragment:**
    ```text
    -> Filter: (users.email = 'nishant@khelo.com')  (cost=50532 rows=498212)
        -> Table scan on users  (cost=50532 rows=498212) (actual time=0.04..120.2 ms)
    ```
    **Analysis:** The type of scan is `Table scan` (which is `ALL` in standard explain) and it examined all `498,212` rows in the database.
    **Resolution:** Add a unique index: `CREATE UNIQUE INDEX idx_email ON users(email);`.

*   **Common Mistakes:**
    *   Using raw `EXPLAIN` without `ANALYZE`. `EXPLAIN` only shows predicted execution paths based on old statistics. `EXPLAIN ANALYZE` actually runs the query, showing actual row scans and millisecond timings.
    *   Ignoring the `filesort` warning on high-throughput query structures.

*   **Follow-up Questions:**
    *   *What does "Using index condition pushdown (ICP)" mean in MySQL?* It is an optimization where MySQL pushes the filter conditions down to the storage engine (like InnoDB) to evaluate index fields directly before reading full table rows from disk.
    *   *What is the difference between EXPLAIN FORMAT=JSON and standard EXPLAIN?* JSON format output provides deeper internal metrics, including cost estimations and query block hierarchies.

</details>

<hr/>

### ❓ Q12. What are transaction Isolation Levels? How do you prevent Deadlocks in SQL databases?
<details>
<summary><b>👀 Show Answer</b></summary>

*   **Detailed Answer:**
    The **Isolation** property of ACID ensures concurrent transactions execute without data anomalies in MySQL. There are **4 standard isolation levels**:

    | Isolation Level | Dirty Reads | Non-Repeatable Reads | Phantom Reads |
    | :--- | :---: | :---: | :---: |
    | **Read Uncommitted** | Yes | Yes | Yes |
    | **Read Committed** | No | Yes | Yes |
    | **Repeatable Read** (MySQL default) | No | No | No (MySQL InnoDB avoids this via Next-Key locking) |
    | **Serializable** | No | No | No |

    *   **Dirty Read:** Reading uncommitted changes from another transaction.
    *   **Non-Repeatable Read:** Re-reading a row within a transaction returns a different value because another transaction updated it.
    *   **Phantom Read:** Re-running a query returns a new set of rows because another transaction inserted new records.

    **Deadlocks:**
    Occur when Transaction 1 holds a lock on Resource A and waits for Resource B, while Transaction 2 holds a lock on Resource B and waits for Resource A.

    **Deadlock Prevention Strategies:**
    1.  **Consistent Resource Access Order:** Ensure all transaction code blocks update tables/rows in the exact same sequence (e.g., sort item IDs alphabetically before locking them).
    2.  **Keep Transactions Short:** Minimize database locking durations. Do not call slow external APIs inside database transaction blocks.
    3.  **Use Optimistic Locking:** Utilize version check numbers (`UPDATE items SET stock = stock - 1 WHERE id = 1 AND version = 5`) instead of pessimistic write locks (`SELECT FOR UPDATE`).

*   **Real-world Example:**
    Handling transfer between two accounts safely:
    ```sql
    -- Transaction 1 (Transfer from Account 1 to 2)
    BEGIN;
    SELECT * FROM accounts WHERE id IN (1, 2) FOR UPDATE; 
    -- Sort IDs before locking. Always lock smaller ID first.
    -- Row 1 locked, then Row 2 locked.
    UPDATE accounts SET balance = balance - 100 WHERE id = 1;
    UPDATE accounts SET balance = balance + 100 WHERE id = 2;
    COMMIT;
    ```

*   **Common Mistakes:**
    *   Executing external API calls (e.g., sending emails or Stripe capture calls) inside a database transaction block. If the API lags, the database locks are held open, creating a performance bottleneck and increasing deadlock risk.
    *   Using high isolation levels (like `Serializable`) globally when lower, more performant isolation levels (like `Read Committed`) would suffice.

*   **Follow-up Questions:**
    *   *What is MVCC (Multi-Version Concurrency Control)?* A technique where database engines write updates to new versions of rows rather than overwriting existing records. This allows readers to access historical versions of data without acquiring locks.

</details>

---

## 4. Microservices Architecture

### ❓ Q13. Compare REST APIs, gRPC, and Message Brokers (RabbitMQ/Kafka) for inter-service communication.
<details>
<summary><b>👀 Show Answer</b></summary>

*   **Detailed Answer:**
    Microservices must communicate either synchronously (blocking) or asynchronously (non-blocking).

    | Communication Protocol | Type | Format | Latency / Throughput | Best Used For |
    | :--- | :--- | :--- | :--- | :--- |
    | **REST (HTTP/1.1)** | Synchronous | JSON (Text) | High Latency / Low throughput | Client-to-Backend interfaces, simple service links. |
    | **gRPC (HTTP/2)** | Synchronous | Protocol Buffers (Binary) | Very Low Latency / High throughput | Internal service-to-service communication. |
    | **RabbitMQ** | Asynchronous | Any (Binary/JSON) | Low Latency / Medium throughput | Message queues, task workers, routing, and transactional workflows. |
    | **Kafka** | Asynchronous | Any (Binary/JSON) | Medium Latency / Massive throughput | Event streaming, log aggregation, clickstream tracking. |

    *   **gRPC** uses **Protocol Buffers** which serialize/deserialize much faster than JSON text. It utilizes HTTP/2 to stream requests/responses concurrently over a single TCP connection.
    *   **RabbitMQ** acts as a message broker where messages are pushed to consumers instantly. It uses AMQP routing patterns (exchanges, queues) to manage delivery.
    *   **Kafka** is a distributed, append-only commit log topic. Consumers poll messages at their own pace, tracking their own offset locations, allowing them to replay messages.

*   **Real-world Example (gRPC definition):**
    Defining a service contract in a `.proto` file:
    ```protobuf
    syntax = "proto3";

    service UserService {
      rpc GetUserProfile (UserRequest) returns (UserResponse);
    }

    message UserRequest {
      string userId = 1;
    }

    message UserResponse {
      string name = 1;
      string email = 2;
      int32 experience = 3;
    }
    ```

*   **Common Mistakes:**
    *   Using synchronous REST calls across a long chain of microservices (e.g., Service A calls B, which calls C, which calls D). If one service in the chain lags or fails, the entire request chain breaks (known as Cascading Failure).
    *   Using Redis Pub/Sub for critical transactional tasks (e.g., payments processing) where data loss cannot be tolerated. Redis Pub/Sub is fire-and-forget; if the subscriber service goes offline, the message is lost. Use RabbitMQ or Kafka instead.

*   **Follow-up Questions:**
    *   *What is the Circuit Breaker Pattern?* A design pattern that stops requests to a failing service once errors cross a threshold. It immediately returns a fallback response, preventing resource exhaustion (e.g., using libraries like `opossum` in Node.js).
    *   *How does Kafka partition data?* Messages are distributed across partitions based on a hashing key (e.g., `userId`), ensuring all messages for a specific user land on the same partition and preserve execution order.

</details>

<hr/>

### ❓ Q14. How do you maintain data consistency across microservices? Explain the Saga Pattern.
<details>
<summary><b>👀 Show Answer</b></summary>

*   **Detailed Answer:**
    In a microservices architecture, each service owns its own database (Database-per-Service pattern). As a result, you cannot execute a distributed database transaction across multiple databases.
    
    To maintain eventual consistency, we use the **Saga Pattern**:
    *   A Saga is a sequence of local transactions.
    *   Each service executes a local transaction and publishes an event or message to trigger the next service's local transaction.
    *   If any transaction fails, the Saga runs a series of **Compensating Transactions** in reverse order to undo the changes made by the previous steps.

    **Saga Implementation Styles:**
    1.  **Choreography (Decentralized):**
        *   Each service listens to events published by other services and decides whether to execute a transaction.
        *   *Pros:* Simple to start, loose coupling.
        *   *Cons:* Hard to track when many services are involved; risk of cyclic dependencies.
    2.  **Orchestration (Centralized):**
        *   A central coordinator service (the Orchestrator) tells each participant service which transaction to execute next.
        *   *Pros:* Centralized flow visualization, easier to manage complex flows.
        *   *Cons:* Orchestrator can become a single point of failure and complex coordinator logic.

*   **Real-world Example (Orchestration Flow):**
    Creating an Order:
    ```text
    [Orchestrator] ---> (Create Order) ---> [Order Service] (Success)
    [Orchestrator] ---> (Reserve Credits) ---> [Payment Service] (Fails!)
    [Orchestrator] ---> (Cancel Order) ---> [Order Service] (Compensating Transaction)
    ```

*   **Common Mistakes:**
    *   Designing compensating transactions that cannot fail. Compensating transactions must be designed to be idempotent and retried until successful.
    *   Assuming the database state is isolated during a Saga. Since transactions commit step-by-step, users may see intermediate states (Dirty Reads). This must be handled at the application level.

*   **Follow-up Questions:**
    *   *What is the Outbox Pattern?* A pattern where event messages are saved directly into the service's database inside the same transaction as the business entity updates. A separate process reads this outbox table and publishes messages to the message queue, ensuring at-least-once delivery.
    *   *What is 2-Phase Commit (2PC)?* An older distributed transaction standard where a coordinator polls all participants to "prepare" before committing. It is slow and prone to blocking, which is why asynchronous Sagas are preferred.

</details>

---

## 5. Cloud, DevOps & Containerization

### ❓ Q15. Write a production-grade Dockerfile for a Node.js API. Explain why it is optimized.
<details>
<summary><b>👀 Show Answer</b></summary>

*   **Detailed Answer:**
    A production Dockerfile must:
    1.  Minimize image size to reduce build and deployment times.
    2.  Leverage caching layers by copying dependency manifests (`package.json`) before source code.
    3.  Run the application as a non-root user for security.
    4.  Implement **Multi-stage builds** to exclude dev dependencies from the final production container image.

*   **Production-Grade Dockerfile:**
    ```dockerfile
    # Stage 1: Build & Install Dependencies
    FROM node:20-alpine AS builder
    WORKDIR /usr/src/app
    
    # Copy manifests first to utilize docker cache layers
    COPY package*.json ./
    
    # Install all dependencies (including devDependencies for typescript/tests)
    RUN npm ci

    # Copy source code and build (e.g. compile TypeScript)
    COPY . .
    # RUN npm run build

    # Clean install only production dependencies
    RUN npm prune --production

    # Stage 2: Final minimal production environment
    FROM node:20-alpine AS runner
    WORKDIR /usr/src/app
    ENV NODE_ENV=production

    # Copy build artifacts and node_modules from build stage
    COPY --from=builder /usr/src/app/package*.json ./
    COPY --from=builder /usr/src/app/node_modules ./node_modules
    COPY --from=builder /usr/src/app/dist ./dist

    # Security: Run as a non-root user
    USER node

    EXPOSE 3000
    CMD ["node", "dist/index.js"]
    ```

*   **Why this is Optimized:**
    *   **`node:20-alpine`:** Alpine Linux is extremely small (~5MB), keeping the overall container footprint low.
    *   **Docker Layer Caching:** By copying `package.json` and running `npm ci` first, Docker skips reinstalling dependencies on subsequent builds unless dependencies change.
    *   **`USER node`:** Default Docker containers run as `root`. If an attacker exploits an RCE vulnerability in the Node app, they would get root access to the underlying container host. Changing to the `node` user mitigates this risk.
    *   **`npm prune --production`:** Removes tools like test frameworks and compilers, reducing image size.

*   **Follow-up Questions:**
    *   *What is the difference between `npm install` and `npm ci` inside a Dockerfile?* `npm ci` is designed for automated environments. It deletes the existing `node_modules` folder and installs the exact versions locked in `package-lock.json`. It is faster and more deterministic.
    *   *What should go into a `.dockerignore` file?* `node_modules`, `npm-debug.log`, `.git`, `.env`, and build folders like `dist` or `coverage`.

</details>

<hr/>

### ❓ Q16. Explain Kubernetes Core Components (Pods, Deployments, Services, HPA) and how to deploy a Node.js app.
<details>
<summary><b>👀 Show Answer</b></summary>

*   **Detailed Answer:**
    Kubernetes (K8s) automates the deployment, scaling, and management of containerized applications.

    **Core Components:**
    *   **Pod:** The smallest deployable execution unit in K8s, containing one or more containers sharing network and storage resources.
    *   **Deployment:** A controller that manages declarative state updates for Pods (e.g., scaling replicas up/down, handling rolling updates).
    *   **Service:** An abstraction layer that defines logical sets of Pods and policy rules to route network traffic to them, acting as an internal load balancer.
    *   **ConfigMap & Secret:** Components to store configuration settings (ConfigMaps) and sensitive details like API keys or certificates (Secrets) separately from container image code.
    *   **Horizontal Pod Autoscaler (HPA):** Dynamically scales the number of replica Pods in a deployment up or down based on metrics like CPU utilization or request rate.

*   **Real-world Example (Deployment YAML configuration):**
    ```yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: khelo-api-deployment
    spec:
      replicas: 3
      selector:
        matchLabels:
          app: khelo-api
      template:
        metadata:
          labels:
            app: khelo-api
        spec:
          containers:
          - name: api
            image: khelotech/api-service:v1.0.0
            ports:
            - containerPort: 3000
            resources:
              limits:
                cpu: "500m"
                memory: "512Mi"
              requests:
                cpu: "250m"
                memory: "256Mi"
            readinessProbe:
              httpGet:
                path: /healthz
                port: 3000
              initialDelaySeconds: 5
              periodSeconds: 10
    ```

*   **Common Mistakes:**
    *   Not setting resource requests and limits in the deployment YAML. K8s needs these limits to schedule container allocations properly. Without them, a single runaway Pod can consume all host memory, crashing other pods on the node.
    *   Using the `latest` image tag in production deployments. This makes it difficult to track what code version is currently deployed and can lead to unexpected version updates on pod restarts.

*   **Follow-up Questions:**
    *   *What is the difference between a Liveness Probe and a Readiness Probe?* A Liveness probe checks if a container is still running; if it fails, K8s restarts it. A Readiness probe checks if a container is ready to accept traffic; if it fails, K8s removes it from the service load balancer rotation.

</details>

---

## 6. Frontend Integration (React & Full-Stack)

### ❓ Q17. Compare Single Page Applications (SPA) vs. Server-Side Rendering (SSR). How do you configure CORS securely?
<details>
<summary><b>👀 Show Answer</b></summary>

*   **Detailed Answer:**
    *   **Single Page Application (SPA - e.g., React Create-React-App/Vite):**
        *   **Flow:** The browser downloads a minimal HTML wrapper file and a large JavaScript bundle. The JS executes in the browser, fetches data via APIs, and renders the UI dynamically on the client side.
        *   **Pros:** Fast page transitions, offloads rendering workload to the client.
        *   **Cons:** Poor initial load speed, poor SEO performance (web crawlers see empty HTML).
    *   **Server-Side Rendering (SSR - e.g., Next.js):**
        *   **Flow:** When a request hits the server, the server fetches API data, renders the complete HTML page, and sends the fully rendered page back to the browser. The browser then "hydrates" the page with JS listeners.
        *   **Pros:** Fast initial load, excellent SEO performance.
        *   **Cons:** Higher server-side load and overhead, longer Time to First Byte (TTFB).

    **CORS (Cross-Origin Resource Sharing):**
    By default, browsers enforce the Same-Origin Policy, blocking web apps on one domain (e.g. `khelo.com`) from reading API responses from another domain (e.g. `api.khelo.com`). CORS headers allow the server to whitelist specific origins.

*   **Real-world Example (Secure CORS in Express):**
    ```javascript
    const express = require('express');
    const cors = require('cors');
    const app = express();

    const whitelist = ['https://khelo.com', 'https://admin.khelo.com'];
    
    const corsOptions = {
      origin: function (origin, callback) {
        // Allow requests with no origin (like mobile apps or curl)
        if (!origin || whitelist.indexOf(origin) !== -1) {
          callback(null, true);
        } else {
          callback(new Error('Blocked by CORS'));
        }
      },
      credentials: true, // Allow sharing of cookies/auth headers
      optionsSuccessStatus: 200
    };

    app.use(cors(corsOptions));
    ```

*   **Common Mistakes:**
    *   Using `app.use(cors({ origin: '*' }))` in production endpoints that handle sensitive user data or require cookie authentication.
    *   Assuming CORS is a server security block. CORS is a browser-enforced security check; it does not block terminal requests (like `curl` or Postman).

*   **Follow-up Questions:**
    *   *What is a CORS preflight request?* An HTTP options request (`OPTIONS`) automatically sent by the browser before the actual request to verify if the server permits the cross-origin operation.
    *   *What is React Hydration?* The client-side process where React hooks into the pre-rendered HTML sent by the server and attaches event listeners, turning it into a fully interactive SPA.

</details>

---

## 7. System Design & Scenario-Based (Gaming/Strategy Context)

### ❓ Q18. Design a real-time, high-throughput gaming Leaderboard system.
<details>
<summary><b>👀 Show Answer</b></summary>

*   **System Architecture:**
    ```text
    [Game Server API] 
           | (Score Updates)
           v
    [Redis Sorted Set Cluster] <--- (Read Top Players) --- [API Gateway] <--- [Users]
           | 
           v (Async persistence)
     [Kafka/Worker] ---> [DB (MySQL)]
    ```

    **Key Mechanics:**
    1.  **Storage Engine:** Use **Redis Sorted Sets (ZSET)**. Redis stores values (player IDs) paired with floating-point scores, keeping them indexed in a skip-list structure.
    2.  **Time Complexity:** 
        *   Updating a score: `ZADD` is $O(\log N)$.
        *   Fetching top 100 players: `ZREVRANGE` is $O(\log N + M)$ where $M$ is the number of requested elements.
    3.  **Scalability:** A single Redis instance can easily handle over 50,000 writes/second. For massive scaling, partition/shard the leaderboard data by tournament IDs, region, or week blocks.

*   **Real-world Example (Implementation Code):**
    ```javascript
    const Redis = require('ioredis');
    const redis = new Redis();

    // Player wins a match and submits score
    async function updateScore(playerId, scoreIncrement) {
      // ZINCRBY increments score of player in sorted set 'weekly_leaderboard'
      await redis.zincrby('weekly_leaderboard', scoreIncrement, playerId);
    }

    // Client requests top 10 players
    async function getTopPlayers() {
      // Returns member names and scores, sorted highest to lowest
      const topPlayers = await redis.zrevrange('weekly_leaderboard', 0, 9, 'WITHSCORES');
      return topPlayers; // Format: ['player1', '1500', 'player2', '1420', ...]
    }
    ```

*   **Common Mistakes:**
    *   Updating and query-sorting leaderboard data inside a relational database table using `SELECT * FROM players ORDER BY score DESC LIMIT 10`. Under high traffic, this causes massive disk I/O bottlenecks and freezes the database.
    *   Failing to persist leaderboards. Keep Redis as the primary read/write layer, but stream score updates asynchronously to MySQL via message queues for permanent storage.

*   **Follow-up Questions:**
    *   *How do you get a player's rank?* Use `ZREVRANK weekly_leaderboard playerId` to get their 0-indexed position relative to all other players.
    *   *How do you handle tie breakers?* Append secondary values to the score (e.g. subtracting chronological timestamps from a base score value so the player who reached the score first ranks higher).

</details>

<hr/>

### ❓ Q19. Design a real-time Game Session Matchmaking Manager. How do you handle WebSockets and Sticky Sessions?
<details>
<summary><b>👀 Show Answer</b></summary>

*   **System Architecture:**
    ```text
                         [Load Balancer (Nginx/ALB)]
                                 | (Sticky Sessions)
            +--------------------+--------------------+
            |                                         |
     [WS Server Node 1]                        [WS Server Node 2]
            ^                                         ^
            |                  (Pub/Sub)              |
            +----------------< Redis >----------------+
                                 |
                        [Matchmaker Engine]
  ```

    **Key Mechanics:**
    1.  **State Management:** Matchmaking rooms, queues, and active game session nodes are stored in a fast **Redis Cluster** to keep them accessible across all servers.
    2.  **WebSocket Server Scaling:** WebSockets maintain long-lived stateful TCP connections. Scale the WS server layer horizontally behind an Application Load Balancer configured with **Sticky Sessions** (session affinity). This ensures reconnecting clients land on the same server holding their local connection context.
    3.  **Redis Pub/Sub Coordination:** When Server 1 needs to send a game update to Player B (who is connected to Server 2), Server 1 publishes the update to a Redis Pub/Sub channel. Server 2 receives it and forwards it to Player B's active WebSocket connection.

*   **Real-world Example (Redis-backed WebSocket Event distribution):**
    ```javascript
    const http = require('http');
    const { Server } = require('socket.io');
    const redisAdapter = require('@socket.io/redis-adapter');
    const Redis = require('ioredis');

    const pubClient = new Redis();
    const subClient = pubClient.duplicate();

    const server = http.createServer();
    const io = new Server(server, {
      cors: { origin: 'https://khelo.com' }
    });

    // Share connection states across servers automatically via Redis Adapter
    io.adapter(redisAdapter(pubClient, subClient));

    io.on('connection', (socket) => {
      const { roomId } = socket.handshake.query;
      socket.join(roomId);

      socket.on('game_action', (data) => {
        // Broadcasts to everyone in the room across all nodes
        io.to(roomId).emit('game_update', data);
      });
    });

    server.listen(3000);
    ```

*   **Common Mistakes:**
    *   Storing active player socket collections solely in application memory without an adapter. If Node restarts or scaling spawns a new server, players on different servers will be unable to communicate.
    *   Failing to set WebSocket connection timeouts or handle heartbeat check pings (`pingInterval` / `pingTimeout`), which leaves dead zombie connections open, consuming socket descriptors.

*   **Follow-up Questions:**
    *   *What is the file descriptor limit bottleneck?* Every TCP socket uses a file descriptor on Linux. By default, Linux limits this to 1024 per process. You must tune `/etc/security/limits.conf` (`nofile`) to scale WebSocket servers to tens of thousands of concurrent connections.
    *   *How do you handle horizontal autoscaling of WebSocket servers?* Use graceful shutdowns: stop accepting new connections, signal existing clients to reconnect (triggering client-side jittered reconnection loops), and wait for active clients to leave before shutting down the container.

</details>
