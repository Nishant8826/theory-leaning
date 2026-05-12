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

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
V8 is Google's open-source, high-performance JavaScript and WebAssembly engine, written in C++. It is used in Chrome and Node.js. Its primary role is to compile JavaScript source code directly into native machine code. It does this using **Just-In-Time (JIT) Compilation**, a hybrid approach that provides fast startup times and highly optimized execution.

**The V8 Pipeline (How it works):**
1. **Ignition (Interpreter):** V8 parses the JavaScript and converts it into a lightweight, intermediate **Bytecode**. Ignition immediately interprets this bytecode, ensuring the application boots up incredibly fast without waiting for heavy compilation.
2. **Profiling:** While Ignition runs the bytecode, it acts as a monitor, looking for "hot" code (functions that are executed repeatedly).
3. **TurboFan (Optimizing Compiler):** Once code is identified as "hot", V8 passes it to TurboFan. TurboFan aggressively compiles the bytecode into pure **Native Machine Code** (CPU-specific 1s and 0s). The next time that code runs, it bypasses the interpreter completely and executes the lightning-fast machine code.
4. **Deoptimization:** If TurboFan's assumptions about the code break (e.g., a function suddenly receives a `String` instead of a `Number`), V8 discards the machine code and deoptimizes back down to the Ignition interpreter to handle the data safely.

> 💡 **Interviewer Focus:**
- Emphasize JIT compilation (the balance between fast startup via Ignition and peak performance via TurboFan).
- Mention the transition from Bytecode to Native Machine Code based on "hot" paths.
- Mention that Deoptimization acts as the failsafe for dynamic types.

</details>

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

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
npm (Node Package Manager) is the default package manager for Node.js. It consists of a command-line client (`npm`) and an online database of public and private packages (the npm registry). It is used to install, share, and manage dependencies in a Node.js project, typically tracked within a `package.json` file.

> 💡 **Interviewer Focus:**
- Emphasize its dual role as a CLI tool and an online registry.
- Mention dependency management via `package.json` and `package-lock.json`.

</details>

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

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
- **`require` (CommonJS):** Synchronous, dynamically loaded at runtime. You can conditionally require modules inside functions.
- **`import` (ES Modules):** Asynchronous, statically analyzed at parse time. Must be declared at the top level (unless using dynamic `import()`), enabling tree-shaking (dead code elimination).

**Advantages & Disadvantages:**
- **`require`:**
  - *Advantage:* Simple to use, allows dynamic/conditional loading anywhere in the code.
  - *Disadvantage:* Synchronous nature can block execution if used outside of application startup. Harder to statically analyze for tree-shaking.
- **`import`:**
  - *Advantage:* Highly optimized. Static analysis allows for excellent dead-code elimination (tree-shaking). Asynchronous nature handles large dependency trees better.
  - *Disadvantage:* More strict. Cannot be conditionally loaded in standard form (must use top-level declaration or `await import()`).

**When to use which one?**
- Use **`import` (ESM)** for all modern, new projects (Node.js 14+ natively supports it). It is the ECMAScript standard, provides better tooling support (tree-shaking), and unifies syntax between frontend (React/Vue) and backend (Node.js).
- Use **`require` (CommonJS)** when working with legacy Node.js codebases, when you absolutely need to load a module conditionally at runtime, or when a specific older npm package does not support ESM.

> 💡 **Interviewer Focus:**
- Static vs dynamic analysis.
- Note that ES modules are the modern standard, but CommonJS is still widely prevalent in legacy Node.js.

</details>

<hr/>

### ❓ Q7. **What is `package.json` and what does it contain?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
`package.json` is the **manifest file** for any Node.js project. *(A manifest file is simply a central document that describes the project, its identity, and exactly what external resources or libraries it needs to run—similar to a shipping invoice or a table of contents).* 

It holds metadata relevant to the project and is used to manage dependencies, scripts, versions, and project details.
Key fields include:
- `name` & `version`: Project identity.
- `dependencies`: Libraries needed in production.
- `devDependencies`: Libraries needed only for local development and testing.
- `scripts`: Custom CLI commands (e.g., `start`, `test`).

</details>

<hr/>

### ❓ Q8. **What is the `fs` module?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
The `fs` (File System) module is a built-in Node.js module used to interact with the file system. It provides functions to read, create, update, delete, and rename files and directories. It offers both synchronous (`readFileSync`) and asynchronous (`readFile` / `promises.readFile`) APIs.

> 💡 **Interviewer Focus:**
- Recommend using the asynchronous methods or the Promise-based API (`fs.promises`) to avoid blocking the event loop.

</details>

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

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
Core modules are built-in modules provided by Node.js, meaning they don't require external installation via npm.
Examples include:
- `http`: To create HTTP servers.
- `fs`: To interact with the file system.
- `path`: To manipulate file paths safely across OS.
- `crypto`: For cryptographic operations.
- `os`: To get operating system information.

> 💡 **Interviewer Focus:**
- Ensure the candidate knows they don't need npm for these and are accessed natively via `require('module_name')` or `node:module_name`.

</details>

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

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
In Node.js, errors are typically handled via:
1. **Error-First Callbacks:** Standard pattern where the first argument of the callback is reserved for an error object (`cb(err, data)`).
2. **Promises & Async/Await:** Handled using `.catch()` blocks or `try...catch` blocks within `async` functions.
3. **Event Emitters:** Using `.on('error', cb)` for streams or custom emitters.
4. **Global Error Middlewares:** In frameworks like Express, centralized error-handling middleware (`app.use((err, req, res, next) => {...})`) acts as a catch-all for errors thrown during request processing.

> 💡 **Interviewer Focus:**
- Emphasize that unhandled promise rejections or uncaught exceptions will crash a Node process.
- Discuss `try...catch` as the modern standard.
- Mention the importance of a centralized/global error middleware in web frameworks.

</details>

<hr/>

### ❓ Q13. **What is the purpose of the `path` module?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
The `path` module provides utilities for working with file and directory paths. It is crucial because different operating systems use different path delimiters (e.g., Windows uses `\`, while Unix/Linux uses `/`). The `path` module normalizes this.
Key methods:
- `path.join()`: Safely concatenates paths.
- `path.resolve()`: Resolves a sequence of paths to an absolute path.

> 💡 **Interviewer Focus:**
- Highlight cross-platform compatibility (avoiding manual string concatenation for paths).

</details>

<hr/>

### ❓ Q14. **What is the `events` module?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
The `events` module is a core, built-in module in Node.js that provides a way to work with events. It contains the `EventEmitter` class, which allows objects to emit named events that cause previously registered listeners (callbacks) to be executed. 

Because Node.js is fundamentally built around an **event-driven architecture**, almost all of its core APIs (like `fs`, `http`, and `stream`) inherit from the `EventEmitter` class under the hood.

**Example Usage:**
```javascript
const EventEmitter = require('events');
const myEmitter = new EventEmitter();

// 1. Register a listener (subscriber)
myEmitter.on('userLoggedIn', (username) => {
  console.log(`Welcome back, ${username}!`);
});

// 2. Emit the event (publisher)
myEmitter.emit('userLoggedIn', 'Alice'); 
// Output: Welcome back, Alice!
```

> 💡 **Interviewer Focus:**
- Highlight that `EventEmitter` is the basis for many core modules like `fs` and `http`.
- It implements the Publisher/Subscriber (Pub/Sub) or Observer design pattern.

</details>

<hr/>

### ❓ Q15. **What are streams in Node.js?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
Streams are a way to handle reading/writing files, network communications, or any kind of end-to-end information exchange in a highly efficient way. Instead of reading a massive file into memory all at once (which could crash your server), streams read data piece by piece (chunk by chunk), processing it over time.

There are four fundamental stream types in Node.js:
1. **Readable:** Streams from which data can be read (e.g., `fs.createReadStream()`, `process.stdin`, HTTP responses).
2. **Writable:** Streams to which data can be written (e.g., `fs.createWriteStream()`, `process.stdout`, HTTP requests).
3. **Duplex:** Streams that are both Readable and Writable (e.g., a TCP network socket like `net.Socket`).
4. **Transform:** A special type of Duplex stream where the output is computed based on the input (e.g., `zlib.createGzip()` for data compression).

**Understanding Transform Streams (The Factory Analogy):**
Think of a Transform stream like a machine on a factory assembly line. 
- The **Readable** stream is the conveyor belt bringing *raw materials* (like a raw text file).
- The **Transform** stream is the machine in the middle that mathematically modifies the materials (like compressing the text).
- The **Writable** stream is the outgoing belt taking the *finished product* away (saving the zipped file).

```javascript
const fs = require('fs');
const zlib = require('zlib');

const rawFile = fs.createReadStream('file.txt'); // Readable
const zipMachine = zlib.createGzip();            // Transform
const zippedFile = fs.createWriteStream('file.gz'); // Writable

// Connect the assembly line using .pipe()
rawFile.pipe(zipMachine).pipe(zippedFile);
```

> 💡 **Interviewer Focus:**
- Emphasize memory efficiency: Streams prevent memory bloat by processing large amounts of data in small chunks.
- Be ready to name an example for each stream type, especially the compression example for Transform streams.

</details>

<hr/>

### ❓ Q16. **Explain the concept of callbacks in Node.js.**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
A callback is a function passed as an argument to another function, which is then invoked inside the outer function to complete some kind of routine or action. In Node.js, callbacks are heavily used to manage asynchronous operations, allowing the single-threaded event loop to continue running while waiting for I/O operations (like reading a file) to finish.

**Example (Error-First Callback):**
```javascript
const fs = require('fs');

// The anonymous function (err, data) => {...} is the callback
fs.readFile('example.txt', 'utf8', (err, data) => {
  if (err) {
    console.error('Error reading file:', err);
    return;
  }
  console.log('File content:', data);
});

console.log('This prints first, while the file is being read in the background.');
```

> 💡 **Interviewer Focus:**
- Understand the difference between sync and async execution.
- Recognize the standard "error-first callback" pattern.

</details>

<hr/>

### ❓ Q17. **What is the difference between `setImmediate` and `setTimeout`?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
Both are used to schedule code to run asynchronously, but they operate in different phases of the Node.js Event Loop.

1. **`setTimeout(callback, 0)`**: Schedules a script to run *after* a minimum threshold in milliseconds has elapsed. This is processed in the **Timers phase** of the event loop.
2. **`setImmediate(callback)`**: Schedules a script to run *immediately after* the current I/O polling phase completes. This is processed in the **Check phase** of the event loop.

**The Tricky Part (Execution Order):**
If you call both from the main module (the top level of your script), the execution order is **non-deterministic** (it depends on the performance of the process).
```javascript
setTimeout(() => console.log('timeout'), 0);
setImmediate(() => console.log('immediate'));
// Output could be either 'timeout' then 'immediate', OR 'immediate' then 'timeout'.
```

However, if you move them inside an **I/O callback** (like reading a file), `setImmediate` will **always** execute first. This is because the Check phase (where `setImmediate` runs) strictly follows the I/O Polling phase.
```javascript
const fs = require('fs');
fs.readFile(__filename, () => {
  setTimeout(() => console.log('timeout'), 0);
  setImmediate(() => console.log('immediate'));
});
// Output is ALWAYS: 
// 1. immediate
// 2. timeout
```

> 💡 **Interviewer Focus:**
- Event Loop phases (Timers phase vs Check phase).
- Explaining why the execution order is deterministic *only* inside an I/O cycle.

</details>

<hr/>

### ❓ Q18. **What are the global objects in Node.js?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
- `__dirname`: Absolute path to the directory containing the currently executing file.
- `__filename`: Absolute path to the currently executing file.
- `process`: Information about the current Node.js process.
- `Buffer`: Used to handle binary data.

> 💡 **Interviewer Focus:**
- Mentioning that `__dirname` and `__filename` are not available natively in ESM.

</details>

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

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
Middleware functions are functions that have access to the request object (`req`), the response object (`res`), and the next middleware function in the application’s request-response cycle (usually denoted by `next`). They can execute code, modify the request/response objects, end the response cycle, or call `next()` to pass control to the subsequent middleware.

> 💡 **Interviewer Focus:**
- Common use cases: authentication, logging, body parsing (e.g., JSON), and error handling.

</details>

<hr/>

### ❓ Q21. **How do you read command-line arguments in Node.js?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
Command-line arguments can be read using the `process.argv` array. 
- `process.argv[0]`: The absolute path to the Node.js executable.
- `process.argv[1]`: The path to the JavaScript file being executed.
- `process.argv[2]` and onwards: The actual arguments passed by the user.
*Libraries like `yargs` or `commander` are often used to parse complex arguments.*

> 💡 **Interviewer Focus:**
- Knowing that the first two indices are reserved for paths.

</details>

<hr/>

### ❓ Q22. **How do you parse JSON in Node.js?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
You can parse JSON strings into JavaScript objects using `JSON.parse()`. Conversely, `JSON.stringify()` converts JavaScript objects into JSON strings. In Express, you use the `express.json()` middleware to parse incoming JSON payload in requests.

> 💡 **Interviewer Focus:**
- Differentiate between standard JS methods and Express middleware.

</details>

<hr/>

### ❓ Q23. **What are environment variables and how do you use them in Node.js?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
Environment variables are dynamic values outside the application that affect its behavior. In Node.js, they are accessed via `process.env`. They are crucial for storing sensitive information (like API keys) and configuring different environments (development vs production).

> 💡 **Interviewer Focus:**
- Security implications of hardcoding secrets.
- Using `NODE_ENV`.

</details>

<hr/>

### ❓ Q24. **What is a REPL in Node.js?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
REPL stands for **Read, Eval, Print, Loop**. It is an interactive shell (or console) provided by Node.js. It reads user input, evaluates the JavaScript code, prints the result to the console, and loops back to wait for the next input. It's excellent for quick debugging and testing small JS snippets.

**Practical Example:**
To try it yourself, open your terminal (command prompt) and type:
```bash
node
```
You will see a `>` prompt. Now you can type JavaScript directly:
```javascript
> const name = "Alice";
undefined
> "Hello " + name;
'Hello Alice'
> Math.random();
0.841578...
```
To exit the REPL, type `.exit` or press `Ctrl + C` twice.

> 💡 **Interviewer Focus:**
- Understanding what each letter stands for.
- Mentioning how to enter and exit the REPL.

</details>

<hr/>

### ❓ Q25. **How do you update npm packages?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
To update packages:
- `npm outdated`: Check which packages have newer versions.
- `npm update`: Safely update packages within semantic versioning ranges.
- `npm install package_name@latest`: Forcefully update a specific package to latest.

> 💡 **Interviewer Focus:**
- Knowing the difference between safe updates vs major version upgrades.

</details>

<hr/>

### ❓ Q26. **What is the purpose of `package-lock.json`?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
It is automatically generated and describes the exact dependency tree that was installed. It guarantees that anyone who clones the project and runs `npm install` gets the exact same versions of all dependencies and sub-dependencies.

> 💡 **Interviewer Focus:**
- Emphasize reproducible builds across environments.

</details>

<hr/>

### ❓ Q27. **What is `process.nextTick()`?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
`process.nextTick()` adds a callback to the next tick queue. This queue is fully drained after the current operation completes, regardless of the event loop phase. It allows you to defer execution of a function until after the current synchronous code runs, but before any asynchronous I/O events.

> 💡 **Interviewer Focus:**
- Differentiate between `nextTick` and `setImmediate`.

</details>

<hr/>

### ❓ Q28. **What is an EventEmitter memory leak?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
A memory leak occurs if you add too many listeners (by default > 10) to a single event using `on()`. Node.js warns about this. It usually happens if listeners are added inside a loop or request handler without being removed using `removeListener()`.

> 💡 **Interviewer Focus:**
- Using `once()` or properly removing listeners.

</details>

<hr/>

### ❓ Q29. **What does non-blocking I/O mean?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
Non-blocking I/O means that the Node.js execution thread does not stop and wait for a slow I/O operation to complete. Instead, Node.js offloads the operation, registers a callback, and moves on. When the operation finishes, the callback is pushed to the event loop.

> 💡 **Interviewer Focus:**
- It allows a single thread to handle thousands of concurrent requests.

</details>

<hr/>

### ❓ Q30. **How does Node.js handle concurrency despite being single-threaded?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
Node.js handles concurrency through its **event-driven, non-blocking I/O architecture**, primarily powered by the Event Loop and the Libuv library. 

Here is a detailed breakdown of how it works:

1. **The Single Thread (Event Loop):** The main Node.js process runs on a single thread. This thread is extremely fast because it *only* executes JavaScript application logic (like routing, formatting data, or math). It **never waits** for slow operations.
2. **Asynchronous I/O Delegation:** When the main thread encounters a slow I/O operation (like a database query, reading a file, or making an API call), it doesn't sit idle waiting for the result. Instead, it delegates the task and immediately moves on to process the next incoming user request.
3. **Libuv & The Background Workers:** The delegation goes to **Libuv** (a C++ library). Libuv handles the task in the background in two main ways:
   - **OS Async Interfaces:** For network requests (like HTTP calls or database queries), Libuv uses the operating system's native async capabilities (like `epoll` on Linux). These use *zero* extra threads.
   - **The Thread Pool:** For operations that the OS cannot handle asynchronously (like heavy File System (fs) operations, Cryptography, or DNS lookups), Libuv offloads the work to a hidden **Thread Pool** (default size of 4 threads).
4. **The Callback Queue:** Once the background task finishes (e.g., the database returns the data), Libuv pushes the associated callback function into the Event Queue. 
5. **Closing the Loop:** The Event Loop constantly monitors this queue. When the main thread is free, it picks up the callback from the queue and executes it, returning the data to the user.

> 💡 **Interviewer Focus:**
- Clearly distinguish between the single-threaded Event Loop (which runs JS) and the multi-threaded Libuv Thread Pool (which runs C++ background tasks).
- Mention that network I/O usually relies on OS features, not the thread pool.

</details>

<hr/>

### ❓ Q31. **What is a Buffer in Node.js and why is it used?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
A Buffer is a globally available class in Node.js used to handle raw binary data (like images, zip files, or network packets). Since JavaScript historically had no mechanism for reading or manipulating streams of binary data, the Buffer class was introduced. It allocates raw memory outside the V8 heap.

**The Relationship between Buffers and Streams:**
- **A Stream** is the *process* of moving data from point A to point B continuously over time.
- **A Buffer** is the actual *container* holding a small chunk of that data at any given moment.

**Analogy:**
Imagine filling a swimming pool with a water hose. The continuous flow of water is the **Stream**. If you hold a small bucket under the hose to catch some water before pouring it into the pool, that bucket is the **Buffer**. 

When Node.js downloads a massive 1GB video, it doesn't load 1GB into memory at once. It *streams* the data, catching small chunks of it into **Buffers**, processing them, and then clearing the buffers to make room for the next chunk.

</details>

<hr/>

### ❓ Q32. **How do you handle file uploads in Node.js?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
File uploads are usually handled by using multipart form data. Since Express cannot parse `multipart/form-data` out of the box, libraries like **Multer** or **Busboy** are used as middleware. They parse the incoming stream of file data, save it to a temporary directory, and attach metadata to the `req.file` object for further processing.

> 💡 **Interviewer Focus:**
- Mention `multipart/form-data` and a library like Multer.

</details>

<hr/>

### ❓ Q33. **What are promises and how are they used in Node.js?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
A Promise is an object that returns some value in future either it will be resolved or rejected. It avoids "callback hell" by allowing developers to chain asynchronous operations sequentially using `.then()`, and centrally handle errors using `.catch()`.

> 💡 **Interviewer Focus:**
- Three states: Pending, Fulfilled, Rejected.
- Immutability of resolved promises.

</details>

<hr/>

### ❓ Q34. **What is the `cluster` module?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
By default, a Node.js application runs on a single thread. This means that if you run your app on an 8-core server, it will naturally only use 1 core, wasting the other 7.

The `cluster` module solves this. It allows you to easily create multiple child processes (called **workers**) that run simultaneously and share the same server port. 

**How it works (Primary / Worker Architecture):**
- **Primary (Master) Process:** Its only job is to spawn Worker processes (usually one for each CPU core) and act as a Load Balancer, distributing incoming network requests to the workers using a Round-Robin algorithm.
- **Worker Processes:** These actually execute your application code and handle the HTTP requests.

**Example:**
```javascript
const cluster = require('cluster');
const os = require('os');
const http = require('http');

if (cluster.isPrimary) {
  // Primary process spawns workers based on CPU cores
  const numCPUs = os.cpus().length;
  for (let i = 0; i < numCPUs; i++) {
    cluster.fork();
  }
} else {
  // Worker processes run the actual server
  http.createServer((req, res) => {
    res.end('Hello World');
  }).listen(3000);
}
```

> 💡 **Interviewer Focus:**
- Explain the Primary Load Balancer vs Worker application logic.
- Mention that in modern production environments, developers rarely write this manual code. Instead, they use Process Managers like **PM2** (`pm2 start app.js -i max`) or Kubernetes to handle clustering automatically.

</details>

<hr/>

### ❓ Q35. **How do you implement authentication in Express?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
Authentication is typically implemented using Passport.js or custom middleware. For stateless authentication, JWT (JSON Web Tokens) are used. The user logs in, receives a token, and sends it in the Authorization header of subsequent requests. Middleware verifies the token before allowing access to protected routes.

> 💡 **Interviewer Focus:**
- Difference between stateful (sessions) and stateless (JWT).

</details>

<hr/>

### ❓ Q36. **What is a session and how is it managed?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
A session is a way to persist data (like user identity) across multiple HTTP requests, since HTTP itself is **stateless**.

**Traditional Sessions (Stateful):**
Sessions are managed by creating a unique **Session ID** (a random string) for the user upon login. 
1. The server saves this ID in a server-side database (like Redis) alongside the user's data.
2. The server sends the ID to the client's browser as a Cookie.
3. On every subsequent request, the browser sends the Cookie, and the server does a database lookup to see who the ID belongs to. The server has to *remember* the state.

**How does this compare to JWT (JSON Web Tokens)?**
JWT does **NOT** use Session IDs. JWTs are **Stateless**.
1. The server mathematically signs the user's data into a token and sends it to the client.
2. The server does NOT save the token in a database.
3. When the client sends the token back, the server just verifies the mathematical signature. It doesn't need to look up a session in a database because the token *itself* carries the user's identity.

> 💡 **Interviewer Focus:**
- Why Redis is the preferred session store for traditional sessions (speed and TTL).
- Explaining the difference between Stateful (Session IDs) and Stateless (JWT) authentication.

</details>

<hr/>

### ❓ Q37. **What is JWT and how is it used for authentication?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
JSON Web Token (JWT) is an open standard used for securely transmitting information between parties as a JSON object. It is stateless, meaning the server does not need to store session data in a database.

**The Structure of a JWT:**
A JWT is a string separated by dots into three parts (`xxxxx.yyyyy.zzzzz`):
1. **Header:** Contains the token type (JWT) and the signing algorithm being used (e.g., HMAC SHA256).
2. **Payload:** Contains the *Claims* (the actual data, like `userId`, `role`, and expiration time `exp`). **Note:** This part is only Base64 encoded, *not encrypted*, so never put raw passwords or highly sensitive data here!
3. **Signature:** Created by taking the encoded Header, encoded Payload, and a secret key known *only* to the server, and running them through the algorithm. This ensures the token hasn't been tampered with.

**How it is used in Authentication:**
1. **Login:** The user provides credentials (username/password).
2. **Token Generation:** The server verifies credentials, generates a JWT signed with its Secret Key, and sends it to the client.
3. **Storage & Usage:** The client stores the JWT and attaches it to the `Authorization: Bearer <token>` header of every subsequent API request.
4. **Validation:** The server receives the request, mathematically verifies the JWT's signature using its Secret Key, and grants access if valid.

> 💡 **Interviewer Focus:**
- Emphasize the three parts: Header, Payload, Signature.
- Highlight that the Payload is readable by anyone (Base64), so it shouldn't contain sensitive secrets. The Signature is what prevents tampering.

</details>

<hr/>

### ❓ Q38. **Explain CORS and how to enable it in Node.js.**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
CORS (Cross-Origin Resource Sharing) is a security mechanism enforced by web browsers. It blocks web pages from making API requests to a different domain than the one that served the web page. To allow these requests in Node.js, the server must explicitly respond with specific headers (`Access-Control-Allow-Origin`). This is usually done easily in Express by using the `cors` middleware package.

> 💡 **Interviewer Focus:**
- Emphasize that CORS is a **browser** security feature, not a server security feature (curl requests don't care about CORS).

</details>

<hr/>

### ❓ Q39. **What is a RESTful API?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
REST (Representational State Transfer) is an architectural style for designing APIs. A RESTful API:
- Uses standard HTTP methods (`GET`, `POST`, `PUT`, `DELETE`).
- Relies on stateless communication (no client context stored on the server).
- Operates on resource URIs (e.g., `/users/123`).
- Uses standard data formats like JSON.

> 💡 **Interviewer Focus:**
- Statelessness and semantic use of HTTP methods are key identifiers.

</details>

<hr/>

### ❓ Q40. **What is Mongoose and how do you connect it?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
Mongoose is an Object Data Modeling (ODM) library for MongoDB and Node.js. It provides schema validation and relationship mapping. You connect using `mongoose.connect("mongodb://localhost/myapp")`.

> 💡 **Interviewer Focus:**
- Emphasize schema validation which native MongoDB lacks.

</details>

<hr/>

### ❓ Q41. **What is database connection pooling?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
Connection pooling is a technique used to maintain a "pool" of active, ready-to-use database connections in memory. 

**The Problem without Pooling:**
Every time a user makes a request that requires database data, the server has to:
1. Open a TCP connection.
2. Perform authentication (Handshake).
3. Execute the query.
4. Close the connection.
This process is extremely slow and resource-intensive. Under high traffic, the database will crash from trying to open and close thousands of connections simultaneously.

**The Solution (Connection Pooling):**
Instead of opening and closing connections per request, the app opens a set number of connections (e.g., 10) when the server starts and keeps them open in a "pool".
- When a request needs database access, it **borrows** an active connection from the pool.
- It executes the query instantly (no handshake needed).
- It **returns** the connection back to the pool for the next request to use.

If all 10 connections are currently being used, the 11th request will wait in a brief queue until one is returned.

> 💡 **Interviewer Focus:**
- Emphasize the massive reduction in latency by eliminating TCP handshake overhead.
- Mention that this prevents the database from crashing under high concurrency.

</details>

<hr/>

### ❓ Q42. **What are environment-specific configurations?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
These are settings that change based on where the code is running (e.g., local dev, staging, production). In Node.js, `NODE_ENV` is used to determine the environment, allowing the app to switch database URIs, logging levels, or API keys accordingly.

> 💡 **Interviewer Focus:**
- `dotenv` package usage.

</details>

<hr/>

### ❓ Q43. **What is the `crypto` module?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
The `crypto` module is a core Node.js module providing cryptographic functionality (OpenSSL wrappers). It is used for hashing passwords, creating random tokens, encrypting sensitive data, and verifying digital signatures.

> 💡 **Interviewer Focus:**
- Modern libraries like `bcrypt` or `argon2` are preferred for passwords over raw `crypto`.

</details>

<hr/>

### ❓ Q44. **How do you implement logging in a Node.js application?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
`console.log` is synchronous and lacks features for production. To implement proper logging, use specialized libraries like **Winston**, **Pino**, or **Morgan** (for HTTP requests). These libraries support:
- Log levels (info, warn, error, debug).
- Formatting (JSON output for log aggregators).
- Multiple transports (saving to a file, database, or sending to Datadog/CloudWatch).

> 💡 **Interviewer Focus:**
- Explain why `console.log` is bad in production (blocks the thread, difficult to search).

</details>

<hr/>

### ❓ Q45. **What is the difference between SQL and NoSQL databases in the context of Node.js?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
SQL databases (PostgreSQL, MySQL) are relational, use structured schemas, and are ideal for complex queries. NoSQL databases (MongoDB) are non-relational, document-oriented, flexible, and map perfectly to JavaScript/JSON objects, making them highly popular in the Node ecosystem (MERN stack).

> 💡 **Interviewer Focus:**
- Emphasize JSON compatibility with NoSQL.

</details>

<hr/>

### ❓ Q46. **How do you write unit tests in Node.js?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
Unit tests are written using frameworks like **Jest** or **Mocha/Chai**. You write small blocks of code (`describe`, `it`) invoking specific functions with mock data and `expect` the output to match a specific result. Mocking libraries isolate functions by faking DB/API calls.

> 💡 **Interviewer Focus:**
- Emphasize isolation (mocking dependencies).

</details>

<hr/>

### ❓ Q47. **What is the purpose of a reverse proxy like Nginx with Node.js?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
While Node.js is incredibly fast at executing application logic, it is **not** designed to be a direct, public-facing web server. A reverse proxy (like Nginx or HAProxy) sits in front of the Node.js application, intercepts all incoming traffic from the public internet, and then forwards only the safe, legitimate requests to Node.js.

Key responsibilities of a Reverse Proxy:
1. **SSL/TLS Termination:** Encrypting and decrypting HTTPS traffic is highly CPU-intensive. Nginx handles this natively in C, offloading the heavy cryptography work so Node's single thread can focus purely on business logic.
2. **Load Balancing:** If you are running 4 Node.js instances (e.g., via PM2 or Docker), Nginx can evenly distribute incoming traffic among them.
3. **Serving Static Assets:** Node.js is relatively slow at reading and serving static files (like images, CSS, JS). Nginx is highly optimized to serve these directly from the disk without ever waking up the Node.js process.
4. **Security & Connection Management:** Nginx absorbs slow clients and basic DDoS attacks (like Slowloris), ensuring that Node.js only ever deals with healthy, fast connections.

> 💡 **Interviewer Focus:**
- Emphasize **SSL Termination** and **Static File Serving** as the two primary ways Nginx prevents Node.js from wasting its single thread on non-application tasks.

</details>

<hr/>

### ❓ Q48. **How do you handle routing in Express.js?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
Express uses the `express.Router()` object to handle modular routing. You can create route handlers for specific HTTP methods and URL paths.
```javascript
const router = express.Router();
router.get('/users', (req, res) => res.send('Users list'));
app.use('/api', router); // Mounts the router at /api
```
This keeps the codebase clean by splitting routes into separate files.

> 💡 **Interviewer Focus:**
- Organizing code logically into modular controllers and routers.

</details>

<hr/>

### ❓ Q49. **What is semantic versioning in npm?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
Semantic Versioning (SemVer) is a standardized versioning system used in npm: `MAJOR.MINOR.PATCH` (e.g., `1.4.2`).
- **MAJOR:** Incompatible API changes (breaking changes).
- **MINOR:** Adds functionality in a backwards-compatible manner.
- **PATCH:** Backwards-compatible bug fixes.
Prefixes like `^` (allows minor/patch updates) or `~` (allows patch updates only) control auto-update limits.

> 💡 **Interviewer Focus:**
- Explaining the difference between `^` and `~` in `package.json`.

</details>

<hr/>

### ❓ Q50. **How do you prevent SQL injection in Node.js?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
SQL injection occurs when malicious SQL statements are inserted into entry fields for execution. It is prevented by **never concatenating raw user input** into SQL queries. 

Instead, you must use **Parameterized Queries** (also known as Prepared Statements) or rely on ORMs/Query Builders that automatically sanitize inputs.

**❌ The Bad Way (Vulnerable to Injection):**
If a user inputs `admin'; DROP TABLE users; --` as the username, the database will literally execute the `DROP TABLE` command and delete everything!
```javascript
const username = req.body.username;
// NEVER DO THIS
db.query(`SELECT * FROM users WHERE username = '${username}'`);
```

**✅ The Good Way (Parameterized Queries):**
Using libraries like `pg` (PostgreSQL) or `mysql2`, you use placeholders (`$1` or `?`). The database driver securely escapes the input before executing the query, ensuring the input is treated strictly as data, not as executable SQL code.
```javascript
const username = req.body.username;
// The $1 placeholder is safely replaced by the value in the array
db.query('SELECT * FROM users WHERE username = $1', [username]);
```

Alternatively, using an ORM like **Sequelize** or **Prisma** automatically handles this escaping for you.

> 💡 **Interviewer Focus:**
- The cardinal rule: NEVER concatenate strings or use template literals to build SQL queries.
- Explain *why* placeholders work (they force the database to treat input as literal text, preventing it from being parsed as SQL syntax).

</details>

<hr/>

### ❓ Q51. **How do you prevent Cross-Site Scripting (XSS)?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
XSS is prevented by sanitizing user input before storing it and escaping output before rendering it in the browser. In Node.js, libraries like `xss-filters` or `DOMPurify` can be used. Helmet.js can also help by setting strict Content Security Policy (CSP) headers.

> 💡 **Interviewer Focus:**
- Input sanitization and CSP headers.

</details>

<hr/>

### ❓ Q52. **What is the `util` module used for?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
The `util` module provides utility functions for debugging and formatting. `util.promisify()` is highly used to convert older callback-based functions into modern Promise-based functions. `util.inspect()` is useful for deeply formatting objects for debugging.

> 💡 **Interviewer Focus:**
- `util.promisify` is the most common use case.

</details>

<hr/>

### ❓ Q53. **How do you handle file downloads in Express?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
Use the `res.download(path, [filename])` method in Express. It automatically sets the appropriate headers (like `Content-Disposition`) to prompt the browser to download the file rather than displaying it.

> 💡 **Interviewer Focus:**
- `res.download` vs `res.sendFile`.

</details>

<hr/>

### ❓ Q54. **How do you profile a Node.js application?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
You profile an app to find CPU/memory bottlenecks using `node --inspect` to connect Chrome DevTools for heap snapshots. Clinic.js is a suite of tools (Doctor, Bubbleprof, Flame) to visualize bottlenecks like Flame Graphs.

> 💡 **Interviewer Focus:**
- Ask them to describe reading a flame graph.

</details>

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

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
- **Loading:** CJS (`require`) is synchronous and blocking. ESM (`import`) is asynchronous and loads modules in parallel.
- **Resolution:** CJS resolves paths at runtime (dynamic). ESM resolves modules statically at parse time.
- **`this` Keyword:** In CJS, top-level `this` is `module.exports`. In ESM, it is `undefined`.
- **Top-level await:** Only supported natively in ESM.

> 💡 **Interviewer Focus:**
- Understanding the strict static nature of ESM which allows static analysis tools to work properly.

</details>

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

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
Microservices architecture is an approach to software development where a large application is built as a collection of small, independent, and loosely coupled services. Each service is responsible for a specific business capability (e.g., User Auth, Payment Processing, Catalog Management) and communicates with other services over a network.

**Why Node.js is a Perfect Fit for Microservices:**
1. **Lightweight and Fast:** Node.js has a small memory footprint and fast startup times. This makes it ideal for containerization (Docker) and auto-scaling in cloud environments.
2. **High I/O Performance:** Microservices involve a lot of network communication (I/O). Node.js's non-blocking, event-driven architecture handles thousands of concurrent network requests efficiently on a single thread.
3. **JSON Native:** Microservices typically communicate using JSON. Since Node.js uses JavaScript, parsing and generating JSON requires zero translation overhead.
4. **Massive Ecosystem:** The npm registry provides ready-to-use libraries for almost any microservice need (API gateways, message brokers, service discovery).

**Core Components of a Node.js Microservices Ecosystem:**
- **API Gateway:** The single entry point for clients. It routes requests to appropriate services, handles authentication, rate limiting, and SSL termination (e.g., using Express or specialized tools like Kong).
- **Communication Protocols:**
  - **Synchronous:** REST APIs (using Express/Fastify) or gRPC (for high-performance, strongly-typed internal communication).
  - **Asynchronous (Event-Driven):** Message brokers like **RabbitMQ**, **Apache Kafka**, or **Redis** are used to decouple services. For example, when an order is placed, the Order Service emits an event, and the Inventory Service listens to update stock.
- **Database per Service:** Each microservice should own its data. For example, the User Service uses MongoDB, while the Payment Service uses PostgreSQL. This prevents tight coupling at the database level.

**Common Challenges & Solutions:**
- **Data Consistency:** Since databases are distributed, maintaining consistency is hard. Solution: Use the **Saga Pattern** or Event Sourcing instead of distributed transactions (2PC).
- **Service Discovery:** Services need to know where others are located. Solution: Use tools like Consul, Eureka, or native Kubernetes DNS.
- **Distributed Tracing:** Debugging across multiple services is difficult. Solution: Implement Correlation IDs and use tools like **OpenTelemetry** and **Jaeger** (see Q63).

> 💡 **Interviewer Focus:**
- Emphasize the shift from monolithic to distributed systems.
- Contrast Synchronous (REST/gRPC) vs Asynchronous (Message Queues) communication.
- Mention that Node.js excels because microservices are I/O-bound (network calls), which fits the Event Loop perfectly.
- Be prepared to discuss "Database per Service" and how it prevents services from stepping on each other's toes.

</details>

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
Since Node.js runs on a single thread, heavy CPU-intensive tasks can block the Event Loop, making the application unresponsive. To solve this, Node.js provides the `child_process` module, which allows you to spawn new processes (sub-processes) to run tasks in parallel, execute system commands, or run other scripts without blocking the main thread.

There are 4 primary methods to create child processes:

### 1. `spawn()`
- **What it does:** Launches a new process with a given command.
- **How it works:** It streams the output (`stdout` and `stderr`). Data is processed in chunks as it arrives.
- **Best for:** Long-running processes, processing large amounts of data (like video encoding or streaming logs), or when you need to interact with the process in real-time.
- **Example:**
```javascript
const { spawn } = require('child_process');
const ls = spawn('ls', ['-lh', '/usr']);

ls.stdout.on('data', (data) => {
  console.log(`Stdout chunk: ${data}`);
});
```

### 2. `exec()`
- **What it does:** Spawns a shell and runs a command within that shell.
- **How it works:** It **buffers** the entire output and passes it to a callback function when the process finishes. It has a default buffer limit of 1024KB (if exceeded, it crashes).
- **Best for:** Running quick shell commands where you expect small amounts of output and want to use shell syntax (like pipes `|` or redirects `>`).
- **Example:**
```javascript
const { exec } = require('child_process');

exec('cat *.js | wc -l', (error, stdout, stderr) => {
  if (error) console.error(`error: ${error.message}`);
  console.log(`Total lines: ${stdout}`);
});
```

### 3. `execFile()`
- **What it does:** Similar to `exec()`, but it executes the specified file directly without spawning a shell.
- **How it works:** It also buffers the output. Since it doesn't use a shell, it doesn't support shell syntax (like pipes), making it slightly faster and **much more secure** against shell injection attacks.
- **Best for:** Running executable files or scripts (like a Python script or a binary) where security is a priority.
- **Example:**
```javascript
const { execFile } = require('child_process');

execFile('node', ['--version'], (error, stdout, stderr) => {
  console.log(`Node version: ${stdout}`);
});
```

### 4. `fork()`
- **What it does:** A specialized case of `spawn()` designed specifically to run Node.js modules.
- **How it works:** It spawns a new Node.js process and establishes a built-in **Inter-Process Communication (IPC)** channel, allowing the parent and child to send JSON messages to each other.
- **Best for:** Offloading CPU-heavy JavaScript tasks (like complex math or heavy data processing) to a separate process.
- **Example:**
```javascript
// Parent.js
const { fork } = require('child_process');
const child = fork('child.js');

child.on('message', (msg) => console.log('From child:', msg));
child.send({ start: true });

// Child.js
process.on('message', (msg) => {
  if (msg.start) process.send({ result: 42 });
});
```

> 💡 **Interviewer Focus:**
- **Streaming vs Buffering:** `spawn` streams (efficient memory), `exec`/`execFile` buffer (simple but limited memory).
- **Shell vs No Shell:** `exec` uses a shell (supports pipes, risky), `execFile` does not (secure, no pipes).
- **IPC:** `fork` is the only one with built-in message passing.
- Mention **Worker Threads** (introduced in Node 10) as the modern alternative for running CPU-intensive JS tasks in *threads* rather than full *processes* (lighter memory footprint).

</details>

<hr/>

### ❓ Q63. **How do you handle distributed tracing in a microservices ecosystem?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
In a microservices ecosystem, a single user request might travel through 5 different Node.js services. Distributed tracing tracks this path. 
When a request hits the API Gateway, a unique `correlation ID` (or trace ID) is generated and attached to the HTTP headers. As the request is passed from service to service, this ID is forwarded and logged. Tools like **OpenTelemetry**, **Jaeger**, or **Zipkin** are used to aggregate these logs and visually trace the request's journey.

> 💡 **Interviewer Focus:**
- The importance of passing the Correlation ID via headers.

</details>

<hr/>

### ❓ Q64. **Explain the concept of continuous integration and continuous deployment (CI/CD) for Node.js.**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
CI/CD automates the software release process.
- **Continuous Integration (CI):** Every time code is pushed, automated servers (like GitHub Actions, Jenkins) install dependencies, run linting, and execute unit tests to ensure nothing broke.
- **Continuous Deployment (CD):** Once CI passes, the code is automatically packaged (often Dockerized) and deployed to staging or production environments (like AWS ECS or Kubernetes).

> 💡 **Interviewer Focus:**
- Ensuring tests run strictly before any deployment occurs.

</details>

<hr/>

### ❓ Q65. **What is Docker and how is it used with Node.js?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
Docker is a platform for containerizing applications. It packages the Node.js app, its dependencies, and the runtime into a single portable image. This ensures the app runs exactly the same on any machine, eliminating "it works on my machine" issues.

> 💡 **Interviewer Focus:**
- Standardizing deployment across environments.

</details>

<hr/>

### ❓ Q66. **How do you structure a large Node.js application?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
A common approach is the Layered (or N-Tier) Architecture:
1. **Controllers/Routes:** Handles HTTP requests/responses.
2. **Service Layer:** Contains business logic, decoupled from HTTP.
3. **Data Access Layer:** Handles database queries.

> 💡 **Interviewer Focus:**
- Emphasize Separation of Concerns.

</details>

<hr/>

### ❓ Q67. **How do you implement rate limiting and throttling?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
Rate limiting restricts the number of requests a user (or IP) can make in a given timeframe to prevent abuse.
- **Implementation:** Often implemented using Redis and a library like `express-rate-limit`. A Token Bucket or Sliding Window Log algorithm is used.
- **Throttling:** Slows down the response artificially when limits are approached, instead of outright blocking them immediately.

> 💡 **Interviewer Focus:**
- Why Redis is necessary in a multi-instance (cluster) deployment (shared state).

</details>

<hr/>

### ❓ Q68. **What is GraphQL and how does it differ from REST?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
GraphQL is a query language for APIs and a runtime for fulfilling those queries with your existing data. It was developed by Facebook to solve common inefficiencies in RESTful APIs.

Here is a detailed comparison of how they differ:

### 1. Endpoints
- **REST:** Uses multiple endpoints for different resources. E.g., `GET /users/1` to get a user, and `GET /users/1/posts` to get their posts.
- **GraphQL:** Uses a **single endpoint** (usually `/graphql`). All requests (read, write, etc.) go to this single URL.

### 2. Data Fetching (The Core Difference)
REST often suffers from two major problems that GraphQL solves:
- **Over-fetching:** REST returns the entire resource object, even if you only need a small part. E.g., getting a user's name might return their address, phone number, and history. GraphQL allows the client to request *exactly* the fields it needs.
- **Under-fetching:** A single REST request might not give you enough data, forcing you to make multiple requests (waterfall requests). GraphQL allows you to fetch deeply nested related data in a single query.

### 3. Request Examples
**REST:**
You might hit `/api/users/1` and get:
```json
{
  "id": 1,
  "name": "Alice",
  "email": "alice@example.com",
  "posts": ["post1", "post2"] // or you might need another request to /api/users/1/posts
}
```

**GraphQL:**
You send a query describing exactly what you want:
```graphql
query {
  user(id: 1) {
    name
    posts {
      title
    }
  }
}
```
And you get exactly that shape back:
```json
{
  "data": {
    "user": {
      "name": "Alice",
      "posts": [
        { "title": "My first post" }
      ]
    }
  }
}
```

### 4. Operations
- **REST:** Relies on semantic HTTP methods (`GET`, `POST`, `PUT`, `DELETE`).
- **GraphQL:** Uses three main operation types:
  - **Query:** For reading data (equivalent to `GET`).
  - **Mutation:** For writing/modifying data (equivalent to `POST`/`PUT`/`DELETE`).
  - **Subscription:** For real-time updates (uses WebSockets).

### 5. Schema & Typing
- **REST:** Typically doesn't enforce a schema unless using tools like OpenAPI/Swagger.
- **GraphQL:** Is strictly typed. You must define a **Schema** using Schema Definition Language (SDL) that dictates what queries are possible and what data types they return.

> 💡 **Interviewer Focus:**
- Clearly explain **Over-fetching** and **Under-fetching**.
- Mention that GraphQL shifts the power to the **client** (the client decides the shape of the response), whereas REST keeps the power with the **server** (the server dictates the response).
- Be ready to discuss trade-offs: REST is easier to cache at the HTTP level (since URLs are unique), while GraphQL caching is more complex because it uses a single endpoint and POST requests.

</details>

<hr/>

### ❓ Q69. **What is Apollo Server?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
Apollo Server is a community-driven, open-source GraphQL server that works with many Node.js HTTP frameworks (like Express). It helps easily build a GraphQL API by defining type definitions (schema) and resolvers.

> 💡 **Interviewer Focus:**
- The relationship between schemas and resolvers.

</details>

<hr/>

### ❓ Q70. **What is the difference between Server-Side Rendering (SSR) and Client-Side Rendering (CSR)?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
- **CSR:** The server sends bare-bones HTML and a large JS bundle. The browser renders the UI. (Slower initial load, fast later interactions).
- **SSR:** Node.js executes the JS and sends fully populated HTML. (Fast initial load, great for SEO).

> 💡 **Interviewer Focus:**
- SEO implications and Time to First Byte (TTFB).

</details>

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

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
The npm registry is open, leading to risks like:
- **Typosquatting:** Malicious packages with names similar to popular ones (e.g., `react-domm`).
- **Post-Install Scripts:** Packages can run arbitrary code on your server immediately upon `npm install`.
- **Dependency Hijacking:** An attacker takes over a legitimate package and pushes a malicious update.
Mitigation: Use `npm audit`, lockfiles, and enterprise artifact registries.

> 💡 **Interviewer Focus:**
- Awareness of supply-chain attacks in the Node ecosystem.

</details>

<hr/>

### ❓ Q73. **How do you implement OAuth2 in Node.js?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
Implementing OAuth2 in Node.js allows users to log in using external providers like Google, GitHub, or Facebook. The industry standard for handling this in Node.js is **Passport.js**.

Here is a detailed breakdown of the flow and a code example using the **Google Strategy**:

### 1. The OAuth2 Flow (Authorization Code Grant)
1.  **Redirect:** The user clicks "Login with Google". Your Node app redirects them to Google's consent screen.
2.  **Consent:** The user logs in and grants permission to your app.
3.  **Callback:** Google redirects the user back to your app with a temporary **Authorization Code** in the URL.
4.  **Exchange:** Your Node server securely sends this code back to Google (along with your `Client Secret`) in exchange for an **Access Token** and user profile data.
5.  **Session:** You save the user to your database and create a session or JWT.

### 2. Implementation with Code (Passport.js)

```javascript
const express = require('express');
const passport = require('passport');
const GoogleStrategy = require('passport-google-oauth20').Strategy;

const app = express();

// 1. Configure Passport with Google Strategy
passport.use(new GoogleStrategy({
    clientID: process.env.GOOGLE_CLIENT_ID,
    clientSecret: process.env.GOOGLE_CLIENT_SECRET,
    callbackURL: "http://localhost:3000/auth/google/callback"
  },
  async (accessToken, refreshToken, profile, done) => {
    try {
      // Find or create user in your database using profile.id
      // const user = await User.findOrCreate({ googleId: profile.id });
      return done(null, profile);
    } catch (err) {
      return done(err, null);
    }
  }
));

// 2. Initialize Passport
app.use(passport.initialize());

// 3. Define Routes

// Route to start authentication (Redirects to Google)
app.get('/auth/google',
  passport.authenticate('google', { scope: ['profile', 'email'] })
);

// Callback route (Google redirects here)
app.get('/auth/google/callback', 
  passport.authenticate('google', { failureRedirect: '/login' }),
  (req, res) => {
    // Successful authentication, redirect to dashboard.
    res.redirect('/dashboard');
  }
);

app.listen(3000, () => console.log('Server running on port 3000'));
```

### 💡 Key Security Considerations:
*   **Never expose the Client Secret** to the frontend or git. Use environment variables.
*   **CSRF Protection:** Use the `state` parameter (Passport handles this automatically) to prevent Cross-Site Request Forgery attacks.
*   **Token Storage:** Store the Access Token securely. If you only need to authenticate the user, you don't even need to store the token; just create a session for the user in your app.

> 💡 **Interviewer Focus:**
*   Never expose client secrets to the frontend; the token exchange must happen securely on the Node.js backend.
*   Understanding the difference between the **Authorization Code** (frontend) and the **Access Token** (backend).

</details>

<hr/>

### ❓ Q74. **What is an API Gateway?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
An **API Gateway** is a server that acts as a single entry point for all clients (web apps, mobile apps, third-party services) to access your backend microservices. Instead of clients calling dozens of different microservices directly, they make requests to the API Gateway, which then routes the request to the appropriate service.

Here is a detailed breakdown and code example:

### 1. Key Responsibilities
*   **Request Routing:** Forwards requests to the correct microservice based on the URL.
*   **Cross-Cutting Concerns:** Handles Authentication, Rate Limiting, SSL Termination, and CORS in one place.
*   **Protocol Translation:** Can translate between HTTP and gRPC or message queues.

### 2. Implementation with Code (Simple Gateway in Node.js)
While tools like Kong or AWS API Gateway are used in production, you can build a simple API Gateway in Node.js using `express` and `http-proxy`:

```javascript
const express = require('express');
const httpProxy = require('http-proxy');
const proxy = httpProxy.createProxyServer({});

const app = express();

// 1. Centralized Authentication Middleware
const authMiddleware = (req, res, next) => {
  const token = req.headers['authorization'];
  if (!token) {
    return res.status(401).json({ error: 'Unauthorized' });
  }
  // Verify token...
  next();
};

// 2. Routing to Microservices
const SERVICES = {
  user: 'http://localhost:3001',
  order: 'http://localhost:3002',
};

// Route to User Service
app.use('/api/users', authMiddleware, (req, res) => {
  proxy.web(req, res, { target: SERVICES.user });
});

// Route to Order Service
app.use('/api/orders', authMiddleware, (req, res) => {
  proxy.web(req, res, { target: SERVICES.order });
});

app.listen(3000, () => console.log('API Gateway running on port 3000'));
```

### 3. Benefits
*   **Reduces Client Complexity:** Clients only need to know one URL.
*   **Improves Security:** Microservices are not exposed to the public internet.
*   **Performance:** Can handle caching and SSL offloading.

> 💡 **Interviewer Focus:**
*   Centralizes security policies and reduces client complexity.
*   Mentioning that while Node can do this, dedicated tools like Kong are preferred for massive scale.

</details>

<hr/>

### ❓ Q75. **How do you handle webhooks in Node.js?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
Webhooks are HTTP POST requests sent by external services (like Stripe) when an event occurs. In Node.js, you expose a specific endpoint to receive these requests. Crucially, you must verify the webhook signature (using crypto) to ensure it came from the trusted provider.

> 💡 **Interviewer Focus:**
- Verifying webhook signatures to prevent spoofing.

</details>

<hr/>

### ❓ Q76. **What is the `assert` module?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
The `assert` module provides a set of assertion functions for verifying invariants. If the condition is false, it throws an `AssertionError`. It is primarily used for internal testing and writing basic unit tests without external libraries.

> 💡 **Interviewer Focus:**
- Simple test validation.

</details>

<hr/>

### ❓ Q77. **How do you handle distributed locks in Node.js?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
In a distributed system, standard memory locks fail. We use Redis. The service sets a key with `NX` (Not eXists) and `PX` (expiration time to prevent deadlocks if the app crashes). For high reliability, the Redlock algorithm is used.

> 💡 **Interviewer Focus:**
- The importance of TTL to prevent infinite deadlocks.

</details>

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

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
The `require` function operates in 5 steps:
1. **Resolution:** Finds the absolute path of the file based on the passed string.
2. **Loading:** Determines the file type (.js, .json, .node) and loads the content.
3. **Wrapping:** Wraps the loaded code in an Immediately Invoked Function Expression (IIFE) that injects `exports, require, module, __filename, __dirname`. This gives the module its private scope.
4. **Evaluation:** The V8 engine executes the code.
5. **Caching:** The exported result is cached in `require.cache`. Subsequent `require` calls for the same file return the cached object instantly without re-executing.

> 💡 **Interviewer Focus:**
- Crucial to mention the IIFE wrapper and the aggressive caching mechanism.

</details>

<hr/>

### ❓ Q82. **Design an API rate limiter from scratch.**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
Designing an API rate limiter from scratch is a common system design question. It protects your infrastructure from DoS attacks, prevents resource abuse, and controls costs.

Here is a detailed guide and implementation:

### 1. Common Algorithms
*   **Fixed Window:** Counts requests in a fixed time window (e.g., 1 minute). Simple to implement but allows a burst of traffic at the edge of the window.
*   **Sliding Window:** Smooths out the burst by looking at the exact timestamp of requests.
*   **Token Bucket:** Refills tokens at a constant rate. Requests consume tokens. Allows for some burstiness while maintaining a steady rate.

### 2. The Distributed Race Condition Problem
If you have multiple Node.js instances, storing the request count in local memory won't work. You must use a centralized store like **Redis**.
However, if two requests hit different Node instances at the exact same time, both might read the count as `9`, and both might increment it to `10`, allowing 11 requests instead of 10.
*   **The Solution:** Use Redis atomic operations or **Lua scripts** to ensure the "Read-Modify-Write" cycle happens atomically.

### 3. Implementation with Code (Fixed Window using Redis)
Here is how you can implement a Fixed Window rate limiter in Node.js using Redis:

```javascript
const express = require('express');
const { createClient } = require('redis');

const app = express();
const redisClient = createClient();

redisClient.on('error', (err) => console.log('Redis Client Error', err));

async function startApp() {
  await redisClient.connect();

  // Rate Limiter Middleware
  const rateLimiter = async (req, res, next) => {
    const ip = req.ip; // Use IP address as the identifier
    const key = `rate_limit:${ip}`;
    const limit = 10; // Max 10 requests
    const windowSize = 60; // 60 seconds

    try {
      // 1. Atomically increment the count
      const currentCount = await redisClient.incr(key);

      // 2. If it's the first request in the window, set the expiry
      if (currentCount === 1) {
        await redisClient.expire(key, windowSize);
      }

      // 3. Check if limit exceeded
      if (currentCount > limit) {
        return res.status(429).json({
          error: 'Too Many Requests',
          message: `Limit exceeded. Try again in ${windowSize} seconds.`
        });
      }

      next();
    } catch (error) {
      console.error(error);
      next(); // Fail open or closed depending on business logic
    }
  };

  app.use(rateLimiter);

  app.get('/', (req, res) => {
    res.send('Request successful!');
  });

  app.listen(3000, () => console.log('Server running on port 3000'));
}

startApp();
```

### 4. Production Grade: Using Lua Scripts
To make the above code completely race-condition free (since the `expire` call happens after `incr`), you should use a Lua script executed directly inside Redis:

```lua
-- Lua script for rate limiting
local current = redis.call('INCR', KEYS[1])
if current == 1 then
    redis.call('EXPIRE', KEYS[1], ARGV[1])
end
return current
```
In Node.js, you execute this using `redisClient.eval()`.

> 💡 **Interviewer Focus:**
*   **Redis** as the centralized counter for distributed systems.
*   Understanding of **Race Conditions** and how to solve them (Lua scripts or Redis transactions).
*   Knowledge of different algorithms (Token Bucket vs Fixed Window).

</details>

<hr/>

### ❓ Q83. **What is the `worker_threads` module?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
True parallelism is achieved using `worker_threads`. Unlike `cluster` (memory-isolated processes), worker threads share the same process but have their own V8 instance and Event Loop. Essential for heavy CPU tasks like image processing or AI.

> 💡 **Interviewer Focus:**
- Differentiate between Concurrency (Event loop) and Parallelism (Worker Threads).

</details>

<hr/>

### ❓ Q84. **How do you design a scalable file storage system?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
Separate metadata from binary blobs. Node.js receives the stream and pipes it to Object Storage (S3). Metadata is saved in a DB. For downloads, Node.js generates a Pre-Signed URL, offloading the heavy downloading work directly to the CDN or S3.

> 💡 **Interviewer Focus:**
- Piping streams directly and using Pre-Signed URLs.

</details>

<hr/>

### ❓ Q85. **What is an ORM vs Query Builder?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
An ORM (like TypeORM or Prisma) maps database tables to classes/objects, allowing you to interact with the database using object-oriented paradigms. A Query Builder (like Knex.js) provides a fluent programmatic interface to write SQL queries without writing raw strings.

> 💡 **Interviewer Focus:**
- Abstraction level differences.

</details>

<hr/>

### ❓ Q86. **How do you optimize a Node.js app startup time?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
1. **Lazy Loading:** Using `require()` dynamically inside functions.
2. **V8 Snapshots:** Compiling the initial state into a V8 snapshot binary to avoid re-parsing JS files.
3. **Reducing Bloat:** Removing unused npm packages.

> 💡 **Interviewer Focus:**
- V8 Snapshots as an advanced optimization technique.

</details>

<hr/>

### ❓ Q87. **Design a notification system (Push, Email, SMS) with guaranteed delivery.**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
Designing a notification system that handles Push, Email, and SMS with **guaranteed delivery** requires a decoupled, event-driven architecture to handle spikes in traffic and third-party API failures.

Here is a comprehensive system design and implementation strategy:

### 1. High-Level Architecture
*   **The API Server:** Receives notification requests (e.g., `POST /notify`) from other services. It does *not* send the notification directly. Instead, it validates the request and pushes it to a Message Queue.
*   **The Message Queue:** (RabbitMQ, Kafka, or Bull in Node.js) Stores the messages persistently. If a worker crashes, the message is not lost.
*   **The Notification Workers:** Dedicated Node.js processes that pull messages from the queue and call third-party APIs (like SendGrid for email, Twilio for SMS, or Firebase for Push).

### 2. Ensuring Guaranteed Delivery (The Interviewer's Focus)
*   **At-Least-Once Delivery:** We acknowledge the message from the queue *only after* the third-party API successfully responds.
*   **Retries with Exponential Backoff:** If the third-party API is down, the worker puts the message back in the queue with a delay that increases with each failure (e.g., wait 1s, then 5s, then 20s).
*   **Idempotency:** Each notification should have a unique `notificationId`. If a worker crashes after sending the SMS but before acknowledging the queue, the retried message won't result in a duplicate SMS (if the third-party API supports idempotency keys).
*   **Dead Letter Queue (DLQ):** If a message fails after `N` retries (e.g., 5 times), it is moved to a special queue called a DLQ for manual inspection or alerting.

### 3. Node.js Implementation Example (using `Bull` and Redis)
`Bull` is the most popular, premium library in Node.js for handling background jobs and queues.

```javascript
const Queue = require('bull');

// 1. Create the Notification Queue
const notificationQueue = new Queue('notifications', 'redis://127.0.0.1:6379');

// --- PRODUCER (API Server) ---
async function sendNotification(userId, type, message) {
  // Add job to queue with retry configuration
  await notificationQueue.add({
    userId,
    type,
    message
  }, {
    attempts: 5, // Retry 5 times
    backoff: {
      type: 'exponential', // Wait longer between each retry
      delay: 2000 // Start with 2 seconds
    }
  });
}

// --- WORKER (Notification Service) ---
notificationQueue.process(async (job) => {
  const { type, message, userId } = job.data;
  
  try {
    if (type === 'EMAIL') {
      await sendEmailAPI(userId, message);
    } else if (type === 'SMS') {
      await sendSMSAPI(userId, message);
    }
    // If successful, job is completed automatically
  } catch (error) {
    console.error(`Failed to send ${type} for job ${job.id}. Attempt ${job.attemptsMade}`);
    // Throwing an error tells Bull to retry based on our configuration
    throw error; 
  }
});

// Handle jobs that failed all retry attempts (Moved to DLQ concept)
notificationQueue.on('failed', (job, err) => {
  if (job.attemptsMade >= job.opts.attempts) {
    console.log(`Job ${job.id} permanently failed. Moving to DLQ manual review.`);
    // Here you would save to a 'dead_letters' database table
  }
});

// Mock API calls
async function sendSMSAPI(user, msg) { /* Call Twilio */ }
async function sendEmailAPI(user, msg) { /* Call SendGrid */ }
```

> 💡 **Interviewer Focus:**
*   **Message Queues:** Why we need them (decoupling and handling spikes).
*   **Exponential Backoff:** To avoid spamming a failing third-party API.
*   **Idempotency:** How to prevent sending the same notification twice on retry.

</details>

<hr/>

### ❓ Q88. **How do you handle database migrations in a CI/CD pipeline without downtime?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
To migrate schemas without downtime, you must use the **Expand and Contract pattern**:
1. **Expand:** Add the new column/table. Update the Node.js code to write to both the old and new columns, but only read from the old.
2. **Migrate:** Run a background script to backfill historical data from the old column to the new one.
3. **Transition:** Update the Node.js code to read from the new column.
4. **Contract:** Once everything is stable, remove the old column.
This ensures that running instances of the old code during the deployment don't break.

> 💡 **Interviewer Focus:**
- The concept of decoupling the database migration from the code deployment.

</details>

<hr/>

### ❓ Q89. **Explain the implementation of a reverse proxy in Node.js.**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
While Nginx is preferred, you can build a reverse proxy in Node.js using `http-proxy` or native `stream` piping.
The Node server listens on port 80. When a request hits, the server looks at the host header, creates a new HTTP client request to the internal microservice, and seamlessly `.pipe()`s the incoming `req` stream to the proxy request, and `.pipe()`s the proxy `res` stream back to the client. This handles large payloads efficiently without buffering them in memory.

> 💡 **Interviewer Focus:**
- The critical role of `streams` (`pipe`) in proxying to prevent memory bloat.

</details>

<hr/>

### ❓ Q90. **Design a distributed caching strategy for a microservices architecture.**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
Designing a distributed caching strategy for microservices involves managing data consistency across multiple independent services. The industry standard is using **Redis** with the **Cache-Aside** pattern.

Here is a comprehensive design and implementation:

### 1. Caching Strategies
*   **Cache-Aside (Lazy Loading):** The application is responsible for reading and writing to the cache. This is the most common pattern.
    *   *Read:* App checks cache. If found, returns data. If not found, reads from DB, writes to cache, and returns.
    *   *Write:* App writes to DB, then invalidates (deletes) the cache key.
*   **Write-Through:** App writes to the cache, and the cache synchronously writes to the DB. (Harder to implement with Redis as a standalone cache).

### 2. Handling Invalidation in Microservices
The biggest challenge is when Service A updates data that Service B has cached.
*   **The Solution:** Use an event-driven approach. When Service A updates the database, it publishes an event (e.g., `user.updated`) to a message broker like Kafka or RabbitMQ. Service B listens to this event and deletes the corresponding key from its Redis cache.

### 3. Implementation with Code (Cache-Aside with Redis)
Here is how you implement the Cache-Aside pattern in Node.js using the `redis` library:

```javascript
const express = require('express');
const { createClient } = require('redis');

const app = express();
const redisClient = createClient();

redisClient.on('error', (err) => console.log('Redis Client Error', err));

async function startApp() {
  await redisClient.connect();

  // Simulated Database Call
  async function getUserFromDB(userId) {
    console.log(`fetching user ${userId} from Database...`);
    return { id: userId, name: 'John Doe', role: 'Admin' };
  }

  // API Endpoint using Cache-Aside
  app.get('/user/:id', async (req, res) => {
    const userId = req.params.id;
    const cacheKey = `user:${userId}`;

    try {
      // 1. Check Cache
      const cachedData = await redisClient.get(cacheKey);
      
      if (cachedData) {
        console.log('Cache Hit!');
        return res.json(JSON.parse(cachedData));
      }

      console.log('Cache Miss!');
      // 2. Fetch from DB on miss
      const user = await getUserFromDB(userId);

      // 3. Save to Cache with a TTL (Time-To-Live) of 1 hour (3600 seconds)
      await redisClient.set(cacheKey, JSON.stringify(user), {
        EX: 3600
      });

      return res.json(user);
    } catch (error) {
      console.error(error);
      return res.status(500).json({ error: 'Server Error' });
    }
  });

  // Endpoint to simulate update and invalidation
  app.post('/user/:id/update', async (req, res) => {
    const userId = req.params.id;
    const cacheKey = `user:${userId}`;

    // 1. Update DB (Simulated)
    console.log(`Updating user ${userId} in Database...`);
    
    // 2. Invalidate Cache (Delete Key)
    await redisClient.del(cacheKey);
    console.log(`Cache key ${cacheKey} invalidated.`);

    return res.json({ success: true, message: 'User updated and cache cleared' });
  });

  app.listen(3000, () => console.log('Server running on port 3000'));
}

startApp();
```

### 4. Advanced Considerations
*   **Cache Penetration:** If a requested key doesn't exist in the DB, requests will always hit the DB. *Solution:* Cache the "null" or empty result with a short TTL.
*   **Cache Avalanche:** If all keys expire at the exact same time, the DB will be flooded. *Solution:* Add a random jitter to the TTL (e.g., 3600 + random(0, 300)).

> 💡 **Interviewer Focus:**
*   **Cache-Aside** is the go-to answer for web apps.
*   Always mention setting a **TTL** (Time-To-Live) to prevent stale data.
*   Be ready to explain **Cache Invalidation** in a distributed system (Pub/Sub or message events).

</details>

<hr/>

### ❓ Q91. **How would you monitor and alert on Node.js application health in a large-scale deployment?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
Monitoring a large-scale Node.js deployment requires observing both the **Application level** (HTTP requests, event loop lag) and the **Infrastructure level** (CPU, Memory).

Here is a comprehensive strategy for monitoring and alerting:

### 1. The RED Metrics Pattern
For web services, we focus on the RED pattern:
*   **Rate:** The number of requests per second.
*   **Errors:** The number of failed requests.
*   **Duration:** The time it takes to process requests (specifically looking at the 95th and 99th percentiles, not just the average).

### 2. Node.js Specific Metrics
Because Node.js is single-threaded, you must monitor:
*   **Event Loop Lag:** If the event loop is blocked, your app cannot handle new requests.
*   **Memory Usage (Heap):** To detect memory leaks.
*   **Active Handles:** To see if connections (like database clients) are not being closed.

### 3. Implementation with Code (Prometheus & Express)
The standard open-source stack is **Prometheus** (to collect data) and **Grafana** (to visualize it). In Node.js, we use the `prom-client` library.

```javascript
const express = require('express');
const client = require('prom-client'); // Prometheus client

const app = express();

// 1. Collect default metrics (CPU, Memory, Event Loop Lag)
const collectDefaultMetrics = client.collectDefaultMetrics;
collectDefaultMetrics({ timeout: 5000 });

// 2. Create custom metrics
const httpRequestDurationMicroseconds = new client.Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route', 'code'],
  buckets: [0.1, 0.3, 0.5, 0.7, 1, 3, 5] // buckets in seconds
});

// 3. Middleware to measure request duration
app.use((req, res, next) => {
  const end = httpRequestDurationMicroseconds.startTimer();
  res.on('finish', () => {
    end({ method: req.method, route: req.path, code: res.statusCode });
  });
  next();
});

// 4. Expose the /metrics endpoint for Prometheus to scrape
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', client.register.contentType);
  res.end(await client.register.metrics());
});

// 5. Basic Health Check Endpoint
app.get('/health', (req, res) => {
  res.status(200).json({ status: 'UP', timestamp: new Date() });
});

app.listen(3000, () => console.log('Server running with monitoring!'));
```

### 4. Alerting Strategy
Data without alerts is useless. You should set up alerts in **Prometheus AlertManager** or **Grafana** to trigger notifications (like PagerDuty or Slack) when:
*   **Error Rate:** > 1% of total requests for 5 minutes.
*   **Latency (p95):** > 500ms for 5 minutes.
*   **Event Loop Lag:** > 100ms (indicates CPU-heavy blocking code).
*   **Memory Usage:** > 80% of the container limit (prevents OOM kills).

> 💡 **Interviewer Focus:**
*   Mentioning **Event Loop Lag** shows you understand Node.js specifics.
*   Using **p95/p99 latency** instead of "average latency" shows senior-level understanding.
*   Differentiating between a simple `/health` endpoint and a full `/metrics` scrape.

</details>

<hr/>

### ❓ Q92. **Design an idempotent API. Why is it important?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
An idempotent API is an API where calling it once has the exact same effect as calling it 100 times. It prevents catastrophic bugs like duplicate credit card charges if a client's network drops and they automatically retry a `POST` request.
Design: The client generates a unique UUID (Idempotency Key) and sends it in the header. The Node.js server checks Redis to see if that key was processed. If yes, it returns the cached successful response. If no, it processes the payment and saves the key.

> 💡 **Interviewer Focus:**
- It is a fundamental requirement for payment gateways and distributed retries.

</details>

<hr/>

### ❓ Q93. **Explain the consensus algorithm (like Raft) and how you might use it in a Node distributed system.**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
A consensus algorithm like Raft ensures that a cluster of distributed nodes agrees on a single source of truth, even if some nodes crash.
If you build a distributed stateful Node.js application, Raft handles **Leader Election** (picking one Node instance to coordinate writes) and **Log Replication** (ensuring all follower instances receive the data securely). It guarantees strong consistency across a cluster, serving as the backbone for systems like etcd or ZooKeeper.

> 💡 **Interviewer Focus:**
- Demonstrating knowledge of distributed systems beyond basic stateless REST APIs.

</details>

<hr/>

### ❓ Q94. **How do you handle eventual consistency in distributed systems?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
In microservices, you cannot use traditional ACID database transactions across multiple databases. Instead, you accept eventual consistency using the **Saga Pattern**.
If Service A successfully processes an order but Service B fails to process payment, Service B publishes a failure event. Service A listens to this and executes a **Compensating Transaction** (e.g., changing the order status to "Cancelled" and returning inventory).

> 💡 **Interviewer Focus:**
- The concept of Compensating Transactions instead of ACID rollbacks.

</details>

<hr/>

### ❓ Q95. **Design a real-time collaborative text editor (like Google Docs) using Node.js.**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
Designing a real-time collaborative text editor (like Google Docs) is a classic system design question. The main challenge is not the real-time communication, but **concurrency control**—how to handle multiple users editing the exact same character at the exact same time without messing up the document.

Here is a comprehensive system design:

### 1. The Core Algorithms (The most important part)
To prevent conflicts and ensure all users see the exact same document, you must use one of two algorithms:

*   **Operational Transformation (OT):**
    *   This is the algorithm used by Google Docs.
    *   It is **server-centric**. When a user types, the client sends the *operation* (e.g., `Insert("X" at index 5)`) to the server.
    *   If another user simultaneously sent an operation, the server **transforms** the incoming operation so it makes sense in the new context.
    *   *Example:* If User A inserts at index 5 and User B deletes at index 5 at the same time, the server decides the order and updates both clients so they end up with the same text.
*   **Conflict-free Replicated Data Types (CRDTs):**
    *   This is a newer approach used by tools like Figma and libraries like `Yjs`.
    *   It is **distributed**. The data structures themselves are designed mathematically so that no matter what order edits arrive in, they will always merge to the exact same state without needing a central server to decide.

### 2. System Architecture
*   **WebSockets (Socket.io):** Used for bi-directional, low-latency communication. HTTP requests are too slow and heavy for keystroke-level updates.
*   **Node.js Server:** Acts as the OT server or the relay for CRDT operations. Node's event-driven nature makes it perfect for handling thousands of concurrent WebSocket connections.
*   **In-Memory Store (Redis):** Active documents are kept in Redis. Disk I/O is too slow for every keystroke. Redis ensures that if the Node server crashes, another server can pick up the document state instantly.
*   **Persistent Database:** Periodically (or on document close), the document state is flushed from Redis to a database like MongoDB or PostgreSQL for long-term storage.

### 3. Scalability Considerations
*   **Pub/Sub with Redis:** If you have 10,000 users, they won't all fit on one Node.js server. You will need multiple servers. When User A types on Server 1, Server 1 uses Redis Pub/Sub to broadcast the edit to Server 2, which then sends it to User B.
*   **Sticky Sessions:** Ensure that all users editing the *same* document are routed to the *same* Node.js server if using OT, to make transformation calculations easier.

> 💡 **Interviewer Focus:**
*   **OT vs CRDT:** You *must* mention these terms. OT is harder to implement but better for text. CRDT is easier to scale but uses more memory.
*   **WebSockets:** Why HTTP is not suitable.
*   **Redis:** For managing shared state across multiple Node instances.

</details>

<hr/>

### ❓ Q96. **How would you trace a performance issue across multiple microservices?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
When a request is slow in a microservices architecture, you need to know which service caused the delay. This requires **Distributed Tracing**.

### 🛑 The Problem in Microservices
In a monolith, tracing a request is easy because everything happens on one server. In microservices, a single request might touch 5 different services (API Gateway ➡️ Auth ➡️ Order ➡️ Inventory ➡️ Payment). If the request is slow, finding which service caused the delay by looking at raw logs is nearly impossible.

### 🔑 Core Concepts of Distributed Tracing
Distributed Tracing solves this by tracking the request's path across all services:
*   **Trace:** The entire journey of a request from start to finish.
*   **Span:** A single unit of work within that journey (e.g., a DB query in one service). A Trace is made up of many Spans.
*   **Trace ID:** A unique ID generated at the start and passed in HTTP headers (e.g., `x-trace-id`) to every downstream service.

### 📦 The Package Tracking Analogy
Think of the **Trace ID** as a package **Tracking Number**. The **Spans** are the stops the package makes (Left Warehouse ➡️ Sorting Facility). The tracking details show you exactly where the package was delayed.

### 🛠️ The Implementation: OpenTelemetry & Jaeger
In Node.js, you implement this using **OpenTelemetry** (to generate and pass Trace IDs) and **Jaeger** or **Zipkin** (to visualize the data). Jaeger provides a "waterfall" graph showing the time spent in each service.

### ❓ Can I use Morgan for this? (Common Follow-up)
**Yes, but with limitations. Morgan handles *Logging*, not *Tracing*.**
*   **What Morgan can do:** You can configure Morgan to log the `Trace ID` in each service. Searching this ID in a centralized log system (like ELK) shows logs from all services.
*   **What Morgan cannot do:** It cannot create visual waterfall graphs or measure network latency between services.

### 💡 Summary for Interviews:
*   Use **Morgan** for HTTP request logging (finding *what* happened in a service).
*   Use **OpenTelemetry + Jaeger** for distributed tracing (finding *where* the request got delayed).

> 💡 **Interviewer Focus:**
*   Differentiating between a **Trace ID** (the whole journey) and a **Span** (one specific service's work).
*   Understanding that Morgan is for local logging, while OpenTelemetry is for distributed tracing across services.

</details>

<hr/>

### ❓ Q97. **Explain the concept of CQRS and Event Sourcing in Node.js applications.**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
- **Event Sourcing:** Instead of storing the current state of an object in a database, you store a sequence of immutable events (e.g., `AccountCreated`, `MoneyDeposited`, `MoneyWithdrawn`). To get the current balance, you fold (reduce) the events.
- **CQRS (Command Query Responsibility Segregation):** Separates the write model (Commands) from the read model (Queries). Node.js listens to the event stream and updates a highly optimized, read-only MongoDB projection, allowing blazing fast UI queries without impacting the write database.

> 💡 **Interviewer Focus:**
- Mentioning that it provides an incredible audit log natively.

</details>

<hr/>

### ❓ Q98. **Design a scalable web scraper.**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
### 🌐 What is a Web Scraper?
A **Web Scraper** (or web crawler) is an automated script that extracts data from websites. Instead of a human manually copying and pasting information, a scraper downloads the raw HTML of a page, parses it to find specific data (like prices or names), and saves it to a database.

### 🏗️ Designing a Scalable Web Scraper
Designing a scalable web scraper involves handling millions of pages while dealing with anti-bot protections, rate limits, and high resource consumption (especially memory).

Here is a comprehensive system design:

### 1. High-Level Architecture
A distributed architecture is required to scale horizontally.
*   **The Scheduler (Master):** Maintains the list of URLs to be scraped, prioritizes them, and ensures we don't hit the same domain too fast (Politeness policy). It pushes URLs to a message queue.
*   **The Message Queue:** (Redis or RabbitMQ) Acts as a buffer and distributes URL tasks to worker nodes.
*   **The Scraper Workers:** (Node.js instances) Pull URLs from the queue, fetch the content, parse it, and save the data.
*   **Storage:** Raw HTML might be stored in an S3 bucket (Data Lake), while structured data goes to MongoDB or PostgreSQL.

### 2. Handling Dynamic Content (SPA)
*   **Static Pages:** Use `axios` or `got` to fetch HTML and `cheerio` to parse it. This is extremely fast and low-resource.
*   **Dynamic Pages (React/Vue/Angular):** Use **Puppeteer** or **Playwright**. Since these spin up real Chromium instances, they consume massive amounts of RAM.
    *   *Optimization:* Disable images, CSS, and fonts in Puppeteer to save bandwidth and memory.
    *   *Optimization:* Use a pool of browser instances rather than opening a new browser for every page.

### 3. Evading Anti-Bot Detection (The Interviewer's Favorite)
Scraping at scale will trigger security systems like Cloudflare. To mitigate this:
*   **Proxy Rotation:** Route requests through a pool of thousands of rotating proxies (Residential proxies are best as they look like real users).
*   **Header Spoofing:** Rotate `User-Agent` strings and accept-language headers to mimic different browsers. Use libraries like `puppeteer-extra-plugin-stealth` to hide Puppeteer fingerprints.
*   **Request Throttling:** Implement random delays (jitter) between requests to avoid looking like a bot.
*   **CAPTCHA Handling:** Integrate with third-party solving services (like 2Captcha) or use AI models to solve simple captchas.

### 4. Node.js Implementation Tips
*   **Concurrency Control:** Do not use `Promise.all()` on thousands of URLs at once; it will crash the server. Use `p-limit` or a worker pool to limit concurrent requests.
*   **Memory Management:** Headless browsers leak memory. Kill and restart browser instances after a certain number of requests.

> 💡 **Interviewer Focus:**
*   **Politeness:** How do you ensure you don't DDoS the target site? (Rate limiting per domain).
*   **Cost vs Speed:** Using Cheerio where possible and Puppeteer only when necessary.
*   **Anti-Bot Mitigation:** Proxy rotation and stealth plugins.

</details>

<hr/>

### ❓ Q99. **How would you implement dynamic module loading without restarting the application?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
Dynamic module loading is dangerous but possible by invalidating the `require.cache`. 
```javascript
delete require.cache[require.resolve('./myModule.js')];
const updatedModule = require('./myModule.js');
```
In a production app, you can expose an admin endpoint that triggers this. However, it can cause severe memory leaks because old closures might still hold references to the old module, preventing garbage collection.

> 💡 **Interviewer Focus:**
- Explicitly warning the interviewer about the severe memory leak risks associated with this.

</details>

<hr/>

### ❓ Q100. **Design a scalable pub/sub messaging system.**

<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
Designing a scalable Pub/Sub (Publish/Subscribe) messaging system involves decoupling the senders (producers) from the receivers (consumers). When discussing *massive scale* (millions of events per second), the industry standard is **Apache Kafka** or **AWS Kinesis**. For smaller scale or complex routing, **RabbitMQ** or **Redis Pub/Sub** might be used.

Here is a detailed breakdown of how a system like Kafka achieves massive scalability:

### 1. Core Architecture Components
*   **Producers:** Applications (like Node.js services) that generate and send messages.
*   **Brokers:** The servers that form the cluster. They receive messages, store them, and serve them to consumers.
*   **Topics:** A specific feed or category to which messages are published.
*   **Partitions:** Topics are split into partitions. This is the **key to scalability**. Each partition is an ordered, immutable sequence of records that is continually appended to.

### 2. How it Scales (The Secret Sauce)
*   **Horizontal Scaling via Partitioning:** A single topic can be split across many partitions located on different brokers. This allows multiple consumers to read from the same topic simultaneously, increasing throughput.
*   **Consumer Groups:** Consumers are grouped together to share the load of reading a topic. If a topic has 4 partitions and a consumer group has 4 instances, each instance reads from exactly one partition. If a consumer crashes, the system automatically rebalances the partitions to the remaining consumers.
*   **Sequential I/O:** Kafka writes messages to the end of the log (sequential write), which is extremely fast even on traditional hard drives, avoiding the overhead of random disk seeks.

### 3. Message Guarantees & Reliability
*   **Durability:** Messages are written to disk and replicated across multiple brokers.
*   **Offsets:** Consumers keep track of where they are in the log using an "offset". This allows them to resume reading if they crash.
*   **Delivery Guarantees:** You can configure the system for *At-most-once*, *At-least-once* (most common), or *Exactly-once* delivery.

### 4. Node.js Implementation Example (using `kafkajs`)
```javascript
const { Kafka } = require('kafkajs');

const kafka = new Kafka({
  clientId: 'my-app',
  brokers: ['localhost:9092']
});

// Producer Example
const produce = async () => {
  const producer = kafka.producer();
  await producer.connect();
  await producer.send({
    topic: 'user-signups',
    messages: [{ value: JSON.stringify({ userId: 123, email: 'test@example.com' }) }],
  });
};

// Consumer Example
const consume = async () => {
  const consumer = kafka.consumer({ groupId: 'email-service-group' });
  await consumer.connect();
  await consumer.subscribe({ topic: 'user-signups', fromBeginning: true });
  await consumer.run({
    eachMessage: async ({ topic, partition, message }) => {
      const data = JSON.parse(message.value.toString());
      console.log(`Sending welcome email to ${data.email}`);
    },
  });
};
```

### 5. Kafka vs RabbitMQ (A Common Follow-up)
*   **Use Kafka for:** High throughput, log aggregation, event sourcing, and when consumers need to replay past messages (replayability).
*   **Use RabbitMQ for:** Complex routing (e.g., topic exchange with wildcards), high reliability per message, and when messages should be deleted immediately after consumption.

> 💡 **Interviewer Focus:**
*   Emphasize **Partitioning** as the mechanism for horizontal scaling.
*   Mention **Consumer Groups** and how they handle load balancing and fault tolerance.
*   Explain the difference between message queuing (RabbitMQ) and log-based pub/sub (Kafka).

</details>

<hr/>

---

### 🧭 Navigation

| ⬅️ Previous | 🏠 Index | ➡️ Next |
| :--- | :---: | ---: |
| [⬅️ JavaScript](./01_Javascript.md) | [Home](./00_Index.md) | 🚫 *None* |
