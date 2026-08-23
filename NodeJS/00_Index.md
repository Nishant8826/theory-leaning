# 🟢 Node.js – Complete Revision Guide

Welcome to the Node.js Mastery consolidated Master Revision Guide. This guide aggregates all key concepts, commands, configurations, analogies, best practices, and interview questions to allow you to revise the entire module in under 30 minutes from a single file. By examining these concepts from first principles, you can refresh your knowledge of V8 engine execution, event loop phases, core module designs, performance scaling, and production architecture.

---

## 📌 Module Navigation

* [01. Introduction to Node.js](#01-introduction-to-nodejs)
* [02. Node.js Environment Setup](#02-nodejs-environment-setup)
* [03. JavaScript Fundamentals for Node.js](#03-javascript-fundamentals-for-nodejs)
* [04. Runtime vs Framework](#04-runtime-vs-framework)
* [05. V8 Engine](#05-v8-engine)
* [06. Event Loop Basics](#06-event-loop-basics)
* [07. npm](#07-npm)
* [08. npx](#08-npx)
* [09. Modules](#09-modules)
* [10. CommonJS](#10-commonjs)
* [11. ES Modules](#11-es-modules)
* [12. File System Module](#12-file-system-module)
* [13. Path Module](#13-path-module)
* [14. OS Module](#14-os-module)
* [15. Events Module](#15-events-module)
* [16. Buffers](#16-buffers)
* [17. Streams Basics](#17-streams-basics)
* [18. Callbacks](#18-callbacks)
* [19. Promises](#19-promises)
* [20. Async/Await](#20-asyncawait)
* [21. HTTP Module](#21-http-module)
* [22. Creating Web Servers](#22-creating-web-servers)
* [23. REST APIs](#23-rest-apis)
* [24. Express.js](#24-expressjs)
* [25. Middleware](#25-middleware)
* [26. Routing](#26-routing)
* [27. MVC Architecture](#27-mvc-architecture)
* [28. Environment Variables](#28-environment-variables)
* [29. Validation](#29-validation)
* [30. Error Handling](#30-error-handling)
* [31. Logging](#31-logging)
* [32. Authentication](#32-authentication)
* [33. Authorization](#33-authorization)
* [34. JWT](#34-jwt)
* [35. Cookies](#35-cookies)
* [36. Sessions](#36-sessions)
* [37. MongoDB](#37-mongodb)
* [38. Mongoose](#38-mongoose)
* [39. PostgreSQL](#39-postgresql)
* [40. ORM Concepts](#40-orm-concepts)
* [40a. Sequelize ORM](#40a-sequelize-orm)
* [41. Redis](#41-redis)
* [42. Caching](#42-caching)
* [43. Rate Limiting](#43-rate-limiting)
* [44. File Uploads](#44-file-uploads)
* [45. Email Services](#45-email-services)
* [45a. Payment Gateways (Razorpay and Stripe)](#45a-payment-gateways-razorpay-and-stripe)
* [45b. Payment Gateways (Real-Time Scenarios)](#45b-payment-gateways-real-time-scenarios)
* [46. Event Loop Deep Dive](#46-event-loop-deep-dive)
* [47. Streams Deep Dive](#47-streams-deep-dive)
* [48. Worker Threads](#48-worker-threads)
* [49. Cluster Module](#49-cluster-module)
* [50. Child Processes](#50-child-processes)
* [51. Memory Management](#51-memory-management)
* [52. Garbage Collection](#52-garbage-collection)
* [53. Performance Optimization](#53-performance-optimization)
* [54. Node.js Internals](#54-nodejs-internals)
* [55. Security Fundamentals](#55-security-fundamentals)
* [56. OWASP Top Risks](#56-owasp-top-risks)
* [57. Helmet](#57-helmet)
* [58. CORS](#58-cors)
* [59. CSRF](#59-csrf)
* [60. XSS](#60-xss)
* [61. SQL Injection](#61-sql-injection)
* [62. NoSQL Injection](#62-nosql-injection)
* [63. Testing Fundamentals](#63-testing-fundamentals)
* [64. Unit Testing](#64-unit-testing)
* [65. Integration Testing](#65-integration-testing)
* [66. Jest](#66-jest)
* [67. Supertest](#67-supertest)
* [68. Swagger/OpenAPI](#68-swaggeropenapi)
* [69. Microservices](#69-microservices)
* [70. Event-Driven Architecture](#70-event-driven-architecture)
* [71. RabbitMQ](#71-rabbitmq)
* [72. Kafka](#72-kafka)
* [73. Distributed Systems](#73-distributed-systems)
* [74. Scaling Node.js](#74-scaling-nodejs)
* [75. Docker](#75-docker)
* [76. Kubernetes](#76-kubernetes)
* [77. CI/CD](#77-cicd)
* [78. GitHub Actions](#78-github-actions)
* [79. AWS Deployment](#79-aws-deployment)
* [80. Nginx](#80-nginx)
* [81. Reverse Proxy](#81-reverse-proxy)
* [82. Load Balancing](#82-load-balancing)
* [83. Observability](#83-observability)
* [84. Monitoring](#84-monitoring)
* [85. Logging Pipelines](#85-logging-pipelines)
* [86. Distributed Tracing](#86-distributed-tracing)
* [87. Production Architecture](#87-production-architecture)
* [88. System Design for Node.js](#88-system-design-for-nodejs)

---

## 01. Introduction to Node.js

🔗 **Full Lesson:** [01_Introduction_to_NodeJS.md](./01_Introduction_to_NodeJS.md)

* **What**: A JavaScript runtime built on Google Chrome's V8 engine that enables developers to execute JavaScript code on servers outside a web browser.
* **Why It Exists**: Before Node.js, JavaScript was restricted to running inside client-side browsers. Traditional web servers like Apache assigned a separate thread for every client connection, wasting excessive RAM context-switching and blocking on database/network I/O. Node.js resolves this by running a single-threaded runtime that handles thousands of connections concurrently using asynchronous, non-blocking I/O.
* **Key Concepts**:
  * **Google V8 Engine**: Compiles high-level JavaScript source code directly into optimized machine code at runtime.
  * **Libuv Library**: A multi-platform C library that handles the event loop, file system, thread pool, DNS lookups, and asynchronous networking.
  * **CPU-Bound vs. I/O-Bound**: Node.js is extremely efficient for I/O-bound tasks (e.g., database queries, network requests) but struggles with CPU-bound tasks (e.g., cryptography, image resizing) because heavy computations block the single main event loop thread.
  * **Least Privilege**: Protect runtime environments by running processes as non-root users to limit damage during compromise.

### Key Commands / Code Example:

```javascript
const fs = require('fs');

// Asynchronous Non-Blocking Read: hands off execution to Libuv and frees the main thread
fs.readFile('large_file.txt', 'utf8', (err, data) => {
  if (err) return console.error('Error:', err);
  console.log('File read finished');
});

console.log('Main thread continues immediately...');
```

> [!IMPORTANT]
> Never block the event loop with synchronous calls (e.g., `fs.readFileSync`) in request handlers, as this halts execution for all other client requests.

---

## 02. Node.js Environment Setup

🔗 **Full Lesson:** [02_NodeJS_Environment_Setup.md](./02_NodeJS_Environment_Setup.md)

* **What**: The software configuration and dependencies required to develop and execute Node.js applications, utilizing version managers and strict configuration parameters.
* **Why It Exists**: Installing Node.js globally using direct system installers leads to version conflicts, permission errors on Unix-based systems (forcing the usage of `sudo npm install`), and environment drift across developer systems, staging, and production environments.
* **Key Concepts**:
  * **Node Version Managers (NVM/FNM)**: Tools that download isolated Node.js binaries and dynamically modify the system's `PATH` variable to point to the active project runtime.
  * **Engine Locking**: Defining runtime constraints inside `package.json` to enforce execution under specific Node/npm versions.
  * **Strict Dependency Auditing**: Utilizing `.npmrc` settings like `save-exact=true` and `engine-strict=true` to prevent semantic version updates and runtime variation across pipelines.

### Key Commands / Code Example:

```json
// Configuration within package.json to restrict execution environment
{
  "name": "secure-production-app",
  "engines": {
    "node": ">=20.11.0 <21.0.0",
    "npm": ">=10.2.4"
  }
}
```
```ini
# Configurations to insert inside the project's .npmrc file
save-exact=true
engine-strict=true
```

> [!IMPORTANT]
> Always commit `package-lock.json` to version control and set `engine-strict=true` inside `.npmrc` to secure deployments against runtime and package-drift vulnerabilities.

---

## 03. JavaScript Fundamentals for Node.js

🔗 **Full Lesson:** [03_JavaScript_Fundamentals_for_NodeJS.md](./03_JavaScript_Fundamentals_for_NodeJS.md)

* **What**: The foundational JavaScript execution mechanisms, scoping principles, context rules, and memory lifecycle models that govern how Node.js manages execution states and variables.
* **Why It Exists**: Because Node.js runs asynchronous operations continuously, core JavaScript rules like closures and lexical scope determine how V8 retains memory references. A lack of understanding leads to massive memory leaks, variable scoping bugs, and binding failures.
* **Key Concepts**:
  * **Execution Context & Call Stack**: Runtimes initialize code in a Global Execution Context and manage active functions on a LIFO (Last In, First Out) Call Stack.
  * **Closures & Memory Retention**: Closures preserve access to outer variables even after parent execution contexts clear. Storing a closure reference in a global cache or array prevents V8 from garbage collecting the referenced variables.
  * **Context Bindings (`this`)**: The global context `this` references `module.exports` in Node.js modules. Standard functions bind context dynamically while arrow functions preserve lexical context boundaries.

### Key Commands / Code Example:

```javascript
// A closure-based middleware factory to encapsulate check logic
const checkRole = (requiredRole) => {
  // Inner function retains access to 'requiredRole' from its parent's lexical scope
  return (req, res, next) => {
    if (req.user && req.user.role === requiredRole) {
      next(); // authorized
    } else {
      res.status(403).json({ error: "Forbidden: Insufficient permissions" });
    }
  };
};

module.exports = checkRole;
```

> [!WARNING]
> Storing callback closures inside global structures (like arrays or event emitters) creates memory retention blocks that lead to heap exhaustion under heavy traffic.

---

## 04. Runtime vs Framework

🔗 **Full Lesson:** [04_Runtime_vs_Framework.md](./04_Runtime_vs_Framework.md)

* **What**: The technical distinction between a language execution environment (Node.js runtime) and a structured application wrapper (Express framework).
* **Why It Exists**: Developing backend applications requires understanding the roles of runtimes and frameworks. Mixing up the layers makes troubleshooting difficult, as developers must know whether an issue originates in the web routing library (framework) or the underlying operating system connection socket (runtime).
* **Key Concepts**:
  * **Runtime Environment**: Integrates an execution engine (like V8) and wraps low-level system calls (filesystem, TCP, cryptographic cards) to run language code on the server.
  * **Web Framework**: An application layer built on top of runtime APIs that simplifies development by introducing MVC structuring, validation helpers, and routing patterns.
  * **Alternative Runtimes**: Systems like Deno (Rust/V8, secure sandbox, ESM) and Bun (Zig/JavaScriptCore, fast startup, built-in bundler) run JS files using different design tradeoffs.

### Key Commands / Code Example:

```javascript
const http = require('http');

// Raw Node.js Runtime HTTP Server (zero dependency)
const server = http.createServer((req, res) => {
  if (req.url === '/health' && req.method === 'GET') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ status: 'OK' }));
  } else {
    res.writeHead(404);
    res.end('Not Found');
  }
});

server.listen(3000);
```

> [!NOTE]
> Structure your business logic independently of routing files (decoupling model/service layers from framework files) to enable migrations between web frameworks without rewrites.

---

## 05. V8 Engine

🔗 **Full Lesson:** [05_V8_Engine.md](./05_V8_Engine.md)

* **What**: Google Chrome's high-performance, open-source JavaScript and WebAssembly engine that JIT-compiles JavaScript directly to native machine code at runtime.
* **Why It Exists**: JavaScript is naturally dynamic and slower to run. The V8 engine compiles JavaScript directly into fast machine code on the fly, optimizing object property access to reach speeds near languages like C++ or Java.
* **Key Concepts**:
  * **JIT Compilation Pipeline**: Ignition interpreter compiles code to bytecode, monitoring hot paths. TurboFan compiler then extracts hot code to generate optimized machine instructions.
  * **Hidden Classes & Inline Caches**: V8 dynamically associates objects with internal Shapes (Hidden Classes). Inline Cache (IC) bypasses class lookups by saving the offset address of accessed properties.
  * **V8 Heap Structure**: Divides dynamic allocation memory into New Space (scavenger GC), Old Space (mark-sweep GC), Large Object Space, and Code Space (TurboFan targets).

### Key Commands / Code Example:

```javascript
// Optimization tip: Monomorphic execution path
function Point(x, y) {
  this.x = x;
  this.y = y;
}

// Accessing properties on instances with identical Shapes
const p1 = new Point(1, 2);
const p2 = new Point(3, 4);

function printCoordinates(p) {
  // Monomorphic call site: V8 optimizes offset access using inline caching
  console.log(p.x, p.y);
}
```

> [!WARNING]
> Dynamically adding, deleting, or reordering properties inside functions changes their Hidden Class (Shape), turning call sites megamorphic and forcing V8 to fall back to slow dictionary lookups.

---

## 06. Event Loop Basics

🔗 **Full Lesson:** [06_Event_Loop_Basics.md](./06_Event_Loop_Basics.md)

* **What**: The single-threaded execution manager inside Libuv that coordinates asynchronous operations in Node.js by resolving callbacks in structured phases.
* **Why It Exists**: Node.js runs on a single main thread. To handle thousands of requests at once without freezing, it offloads slow tasks (like reading files or network calls) to the operating system and uses the Event Loop to run their callbacks later.
* **Key Concepts**:
  * **Execution Queues**: Tasks are split into high-priority Microtasks (`process.nextTick`, Promises) and standard Macrotasks (timers, network, FS I/O).
  * **Loop Phases**: The event loop executes in phases: Timers (setTimeout), I/O Pending, Idle/Prepare, Poll (waiting/checking network), Check (setImmediate), and Close.
  * **Microtask Exhaustion**: Microtask queues execute immediately when the stack clears. Recursive `process.nextTick` calls will drain resource ticks and starve macrotasks.

### Key Commands / Code Example:

```javascript
console.log('Sync Start');

setTimeout(() => console.log('Macrotask: Timer'), 0);
setImmediate(() => console.log('Macrotask: Check'));

Promise.resolve().then(() => console.log('Microtask: Promise'));
process.nextTick(() => console.log('Microtask: nextTick'));

console.log('Sync End');
// Execution Order: Sync Start -> Sync End -> nextTick -> Promise -> Timer -> Check
```

> [!IMPORTANT]
> Ensure asynchronous interfaces are deterministic. Never mix synchronous outputs with async callbacks (e.g. returning cached objects synchronously but reading disk files asynchronously), as this causes execution race conditions.

---

## 07. npm

🔗 **Full Lesson:** [07_npm.md](./07_npm.md)

* **What**: Node Package Manager, the default CLI package installer and repository ecosystem used to resolve, lock, and audit external dependencies in Node.js projects.
* **Why It Exists**: Managing external packages requires strict version locks and safety checks. Without them, automatic updates can introduce bugs or security vulnerabilities into your project.
* **Key Concepts**:
  * **Semantic Versioning (SemVer)**: Formatted as `MAJOR.MINOR.PATCH`. Operators like Caret (`^`) allow minor/patch updates, Tilde (`~`) limits to patches, and exact matching locks changes completely.
  * **Integrity Locking**: `package-lock.json` maps exact versions and includes SHA-512 cryptographic subresource hashes to guarantee identical package codes across deployments.
  * **Dependency Classification**: Separating dependencies (production requirements) from devDependencies (development testing/builders) reduces production build sizes.

### Key Commands / Code Example:

```bash
# Audits dependencies for security vulnerabilities and prints a report
npm audit

# Runs security audit and automatically applies safe dependency updates
npm audit fix

# Installs dependencies exactly as resolved inside package-lock.json (for CI builds)
npm ci
```

> [!IMPORTANT]
> Never exclude `package-lock.json` from git. Always commit it to ensure dependency trees remain uniform across developer systems, CI builds, and production.

---

## 08. npx

🔗 **Full Lesson:** [08_npx.md](./08_npx.md)

* **What**: Node Package Execute, an npm-bundled runner utility used to execute CLI tools directly from the remote npm registry without local or global installations.
* **Why It Exists**: Installing command-line tools globally causes version conflicts, while installing them locally bloats your project. npx runs these tools directly from a temporary cache without permanently installing them.
* **Key Concepts**:
  * **Ephemeral Execution**: npx fetches the requested package CLI to a temporary cache, executes the binary command, and deletes it right after execution.
  * **Local Path Scanning**: Before requesting remote registries, npx scans the local directory's `node_modules/.bin` to execute local dependency packages directly.
  * **Direct Remote Calling**: Executes command blocks from raw HTTP source URLs or specific versions of packages without permanent installations.

### Key Commands / Code Example:

```bash
# Run the local or a temporary 'serve' package to serve static folders
npx serve -s build

# Scaffolds a new application using a specific version of a builder CLI
npx create-next-app@latest ./my-app --ts

# Run node scripts with specific packages without modifying project package.json
npx -p typescript tsc --version
```

> [!NOTE]
> Use npx to execute scaffolding commands (e.g. `create-react-app`) or one-off code formatters to avoid cluttering local dependency arrays and global system installations.

---

## 09. Modules

🔗 **Full Lesson:** [09_Modules.md](./09_Modules.md)

* **What**: The core architecture in Node.js used to isolate scopes, modularize functionality, and export variables safely without global namespace contamination.
* **Why It Exists**: In browsers, scripts share a single global space, causing variables to overwrite each other. Node.js uses modules to keep code in different files isolated and safe from namespace collisions.
* **Key Concepts**:
  * **The Module Wrapper**: Node.js wraps code modules in a hidden IIFE function before compilation to inject parameters (`exports`, `require`, `module`, `__filename`, `__dirname`).
  * **Private Scopes**: Variables declared inside module code remain private to that file unless assigned explicitly to `module.exports`.
  * **Circular Dependencies**: Requiring file A from B and B from A causes V8 to supply an incomplete export object to resolve the loops, leading to unexpected `undefined` parameters.

### Key Commands / Code Example:

```javascript
// The implicit module wrapper function injected by the Node.js compiler:
(function(exports, require, module, __filename, __dirname) {
  // Your module code is placed here
  const privateDbKey = '123456'; // remains private
  exports.getData = () => { return 'data'; }; // exposed
});
```

> [!NOTE]
> Because files are wrapped in functions, variables like `require`, `module`, and `__dirname` are dynamically injected parameters, rather than JavaScript global variables.

---

## 10. CommonJS

🔗 **Full Lesson:** [10_CommonJS.md](./10_CommonJS.md)

* **What**: The original synchronous module format used in Node.js, where dependencies are loaded sequentially from disk using `require()` and exported via `module.exports`.
* **Why It Exists**: Created as the original module system for Node.js on servers, allowing modules to be loaded synchronously directly from the local disk.
* **Key Concepts**:
  * **Synchronous Loading**: Resolves and loads dependencies instantly in sequence. This blocks code execution, making it unsuitable for client-side browsers.
  * **Caching Mechanisms**: Cache modules by path in `require.cache`. Multiple `require` calls to the same file return the exact same instance.
  * **Dynamic Importing**: Because require behaves as a standard function, you can call it inside conditionals or loops during runtime.

### Key Commands / Code Example:

```javascript
// Import syntax
const db = require('./database');

// Expose exports dynamically
module.exports = {
  connectDB: () => db.connect(),
  version: "1.0.0"
};
```

> [!WARNING]
> Objects returned by `require()` are shared by reference. Modifying properties on a required module changes that object across the entire runtime.

---

## 11. ES Modules

🔗 **Full Lesson:** [11_ES_Modules.md](./11_ES_Modules.md)

* **What**: The official standardized module system for JavaScript, loading modules asynchronously and statically resolving imports at compile time.
* **Why It Exists**: CommonJS cannot support asynchronous remote network loading or effective static code analysis like tree-shaking, which is essential for frontend compiling and modern universal JavaScript APIs.
* **Key Concepts**:
  * **Static Resolution**: Import/export mappings are analysed at compile time. This prevents calling imports conditionally or inside loop scopes.
  * **Asynchronous Parsing**: Executed in three isolated steps: Construction (resolving files), Instantiation (mapping variables), and Evaluation (running code blocks).
  * **Path Resolving**: Paths require absolute filenames with extensions (e.g. `./db.js`) as they must support remote URL resolving.

### Key Commands / Code Example:

```javascript
// Import and export ESM syntax
import { dbConnect } from './database.js';

export const init = () => dbConnect();

// Workaround to rebuild CommonJS globals in ES Modules:
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
```

> [!IMPORTANT]
> ES Modules do not inject `__dirname` or `__filename`. You must reconstruct these variables using `import.meta.url` and path helper utilities.

---

## 12. File System Module

🔗 **Full Lesson:** [12_File_System_Module.md](./12_File_System_Module.md)

* **What**: Node's built-in core module (`fs`) used to interact with the host operating system's files and directories.
* **Why It Exists**: Provides access to the computer's storage, wrapping low-level operating system file operations into easy-to-use JavaScript functions.
* **Key Concepts**:
  * **API Variants**: Provides synchronous (blocking), callback (async), and promise-based async utilities.
  * **Thread-pool Offloading**: Asynchronous filesystem calls are offloaded to Libuv background threads, freeing the main thread for event processing.
  * **Buffer Limits**: Standard file reads allocate the entire file into a V8 memory buffer, which will crash the engine on large files (use Streams instead).

### Key Commands / Code Example:

```javascript
const fs = require('fs').promises;

// Promise-based asynchronous file operations
async function logError(msg) {
  try {
    // Appends text to a file, creating it if missing
    await fs.writeFile('errors.log', `${msg}\n`, { flag: 'a' });
  } catch (err) {
    console.error('FS Write Error:', err);
  }
}
```

> [!IMPORTANT]
> Never use synchronous file operations (like `fs.writeFileSync`) in request handlers. They halt the main execution thread and block all incoming network connections.

---

## 13. Path Module

🔗 **Full Lesson:** [13_Path_Module.md](./13_Path_Module.md)

* **What**: Node's built-in utility module (`path`) that formats, joins, and resolves file paths consistently across Windows, macOS, and Linux.
* **Why It Exists**: Creating file paths by joining strings manually fails because Windows uses backslashes (\) while Mac and Linux use forward slashes (/). The Path module handles this difference automatically.
* **Key Concepts**:
  * **Platform Abstraction**: Automatically uses system-specific delimiters (slashes) depending on where the node runtime is executing.
  * **path.join vs path.resolve**: `path.join` concatenates path parts. `path.resolve` compiles an absolute path resolving from the execution directory (`process.cwd()`).
  * **Parsing utilities**: Includes functions to parse paths into structures containing directories, extensions, root, and file names.

### Key Commands / Code Example:

```javascript
const path = require('path');

// Join constructs paths relative to folder inputs
const dbConfigPath = path.join(__dirname, 'config', 'db.json');

// Resolve parses paths to absolute locations starting from current execution directory
const absolutePath = path.resolve('temp', 'logs');

// Parse breakdown
const parsed = path.parse(dbConfigPath); // returns { root, dir, base, ext, name }
```

> [!WARNING]
> `path.resolve` targets paths relative to `process.cwd()` (the directory where you ran the terminal command), which can vary and cause files to not be found. Use `path.join(__dirname, ...)` for safety.

---

## 14. OS Module

🔗 **Full Lesson:** [14_OS_Module.md](./14_OS_Module.md)

* **What**: Node's core built-in utility module (`os`) that provides diagnostic queries to retrieve information about the physical host hardware, system uptime, and CPU structures.
* **Why It Exists**: Managing servers and deployment requires reading the host system's hardware status, such as CPU details, free memory, and network settings.
* **Key Concepts**:
  * **Hardware Diagnostics**: Exposes real-time CPU metrics, operating system versioning, system uptime, and memory capacities.
  * **Network Interfaces**: Exposes local IP assignments, MAC addresses, and network routing configurations.
  * **Cluster Core Matching**: Used to fetch available logical processor cores (`os.cpus().length`) to scale process clusters.

### Key Commands / Code Example:

```javascript
const os = require('os');

// Diagnostic metrics
const totalCores = os.cpus().length; // returns number of logical cores
const freeMemBytes = os.freemem(); // returns current free RAM bytes
const sysPlatform = os.platform(); // returns 'win32', 'linux', or 'darwin'
const networkInfo = os.networkInterfaces(); // returns system network interfaces map
```

> [!IMPORTANT]
> Inside containerized runtimes (like Docker), `os.cpus()` and `os.totalmem()` report the overall host machine stats rather than container-specific limits. Read values from `/sys/fs/cgroup/` for accurate container limits.

---

## 15. Events Module

🔗 **Full Lesson:** [15_Events_Module.md](./15_Events_Module.md)

* **What**: Node's core messaging implementation (`events`) containing the `EventEmitter` class, which allows components to establish pub/sub communication channels.
* **Why It Exists**: Backend systems need a way for different parts of an application to communicate without being tightly linked together. The Events module allows parts of the code to listen and react to specific triggers.
* **Key Concepts**:
  * **EventEmitter Class**: Establishes an observer structure where modules register listener callbacks that execute when matching event tags are emitted.
  * **Synchronous Execution**: Event listeners are executed synchronously in the order they are registered in the current event loop execution tick.
  * **Reference Retaining**: Lingering listeners retain references to parent variables, causing closures to leak memory if not removed with `.off()`.

### Key Commands / Code Example:

```javascript
const EventEmitter = require('events');

class UserNotifier extends EventEmitter {
  signup(user) {
    this.emit('signup', user);
  }
}

const notifier = new UserNotifier();
notifier.on('signup', (user) => {
  console.log(`Sending activation mail to ${user.email}`);
});

notifier.signup({ email: 'test@example.com' });
```

> [!WARNING]
> If an EventEmitter throws an `'error'` event and there are no listeners registered for it, the Node.js process will crash. Always register a listener for `'error'` events.

---

## 16. Buffers

🔗 **Full Lesson:** [16_Buffers.md](./16_Buffers.md)

* **What**: A raw binary data storage structure in Node.js allocated outside the V8 heap in physical memory, used to handle raw TCP socket streams and file buffers directly.
* **Why It Exists**: Standard JavaScript was only designed to handle text, not raw binary data. Buffers allow Node.js to work with raw binary data (like files, images, or network packets) by storing it directly in the system's memory outside of JavaScript's normal memory pool (the V8 heap).
* **Key Concepts**:
  * **Fixed-Size Allocations**: Once allocated, buffer sizes cannot be dynamically resized, requiring careful prediction of expected stream size.
  * **Clean vs Unsafe Allocation**: `Buffer.alloc()` zero-fills allocated memory for safety, whereas `Buffer.allocUnsafe()` is faster but leaves pre-existing data in the raw memory, posing security leak threats.
  * **V8 Heap Independence**: Allocations occur in raw C++ system memory rather than inside the V8 garbage-collector monitored heap, optimizing high-performance applications.

### Key Commands / Code Example:

```javascript
// Safe zero-filled binary allocation (10 bytes)
const safeBuf = Buffer.alloc(10);

// Faster, unsafe allocation (contains dirty memory)
const rawBuf = Buffer.allocUnsafe(10);

// Convert standard strings to binary payloads and encode as hex
const textBuf = Buffer.from('NodeJS', 'utf8');
console.log(textBuf.toString('hex')); // Prints: 4e6f64654a53
```

> [!WARNING]
> Never use `Buffer.allocUnsafe()` to store user inputs without immediately overwriting the entire buffer length, otherwise residual system memory secrets can leak to clients.

---

## 17. Streams Basics

🔗 **Full Lesson:** [17_Streams_Basics.md](./17_Streams_Basics.md)

* **What**: An event-driven data streaming interface in Node.js that processes large datasets in small, sequential chunks, preventing memory saturation.
* **Why It Exists**: Reading massive files (like large databases or video files) all at once will fill the memory and crash the server. Streams fix this by loading and processing files in tiny, manageable pieces.
* **Key Concepts**:
  * **Stream Architectures**: Classified into Readable (source), Writable (destination), Duplex (bi-directional like sockets), and Transform (mutator like zlib compressions).
  * **Backpressure Control**: A mechanism that pauses reading pipes if the writing stream is slower than the incoming chunk speed, preventing memory spikes.
  * **Event-Driven Handling**: Emits life-cycle triggers like `'data'`, `'end'`, `'drain'`, and `'error'` to orchestrate chunk streams.

### Key Commands / Code Example:

```javascript
const fs = require('fs');

const src = fs.createReadStream('large_input.log');
const dest = fs.createWriteStream('processed_output.log');

// Connect streams using pipe which automatically handles backpressure flows
src.pipe(dest);

src.on('error', (err) => console.error('Read Stream Error:', err.message));
dest.on('error', (err) => console.error('Write Stream Error:', err.message));
```

> [!IMPORTANT]
> Always route `'error'` events on all piped streams. A standard `.pipe()` call does not forward errors, and an unhandled stream error will crash the application.

---

## 18. Callbacks

🔗 **Full Lesson:** [18_Callbacks.md](./18_Callbacks.md)

* **What**: A function passed as an argument to another function, which is executed asynchronously after a background operation completes.
* **Why It Exists**: Callbacks let Node.js run a specific block of code as soon as a slow background task (like reading a database) finishes, keeping the main thread free for other work.
* **Key Concepts**:
  * **Delegation Pattern**: Handed to async functions as arguments to run once offloaded Libuv/OS tasks report completions.
  * **Error-First Conventions**: Node.js callbacks accept error variables as their first parameter (`err`) and data payloads as the second (`data`).
  * **Callback Hell**: Deeply nested asynchronous callbacks make code hard to read, maintain, and dry-run (leading to Promise abstractions).

### Key Commands / Code Example:

```javascript
// Error-first asynchronous callback structure
function fetchConfig(fileName, callback) {
  require('fs').readFile(fileName, 'utf8', (err, data) => {
    if (err) {
      return callback(err); // Pass error upward
    }
    callback(null, JSON.parse(data)); // Pass success payload
  });
}

fetchConfig('config.json', (err, config) => {
  if (err) return console.error('Failed to load:', err.message);
  console.log('Active DB host:', config.dbHost);
});
```

> [!NOTE]
> Always check for the error argument first in callbacks before writing main payload logic, as executing calls on undefined parameters triggers runtime exceptions.

---

## 19. Promises

🔗 **Full Lesson:** [19_Promises.md](./19_Promises.md)

* **What**: A native JavaScript object representing the eventual completion (or failure) of an asynchronous operation and its resulting value.
* **Why It Exists**: Promises replace messy, deeply nested callbacks ("callback hell") with clean, chainable objects that make handling success and errors much easier.
* **Key Concepts**:
  * **Promise States**: Transition from `pending` to either `fulfilled` (via `resolve()`) or `rejected` (via `reject()`). Once resolved, state is immutable.
  * **Microtask Queue**: Promise callbacks execute inside V8's microtask queue, which has execution priority over standard macrotask queues (like timers).
  * **Promise Chaining**: Replaces nested structures with sequential `.then()` flows, routing all intermediate exceptions to a single trailing `.catch()` block.

### Key Commands / Code Example:

```javascript
const getPayload = (isValid) => {
  return new Promise((resolve, reject) => {
    if (!isValid) {
      return reject(new Error('Validation Failure'));
    }
    resolve({ status: 'Authorized' });
  });
};

getPayload(true)
  .then((res) => console.log('Response:', res))
  .catch((err) => console.error('Caught:', err.message));
```

> [!IMPORTANT]
> Uncaught Promise rejections will trigger exit signals in modern Node.js versions. Always catch promise chains or hook a global `unhandledRejection` handler to the process.

---

## 20. Async/Await

🔗 **Full Lesson:** [20_Async_Await.md](./20_Async_Await.md)

* **What**: Syntactic sugar built on top of JavaScript Promises that enables writing asynchronous execution paths using a flat, synchronous-looking code structure.
* **Why It Exists**: Simplifies writing asynchronous code by letting you write promise chains in a flat, sequential style that reads like normal synchronous code.
* **Key Concepts**:
  * **Syntax Sugar**: Functions declared as `async` automatically return a Promise. The `await` keyword pauses execution context until the target promise resolves.
  * **Event Loop Preservation**: Pausing inside an async function only yields control back to the Event Loop, allowing other events to execute.
  * **Exception Control**: Allows standard `try/catch` syntax to handle asynchronous exceptions, simplifying error routing.

### Key Commands / Code Example:

```javascript
const fs = require('fs').promises;

// Flattens asynchronous code and applies standard try/catch
async function loadUserData(userId) {
  try {
    const rawData = await fs.readFile(`./users/${userId}.json`, 'utf8');
    const user = JSON.parse(rawData);
    return user;
  } catch (err) {
    console.error(`Error loading user ${userId}:`, err.message);
    throw err; // rethrow after logging
  }
}
```

> [!IMPORTANT]
> Awaiting independent operations sequentially (e.g., `await getA(); await getB();`) slows down throughput. Use `Promise.all([getA(), getB()])` to run tasks in parallel.

---

## 21. HTTP Module

🔗 **Full Lesson:** [21_HTTP_Module.md](./21_HTTP_Module.md)

* **What**: A core Node.js module that wraps system TCP socket APIs, providing low-level HTTP parsing, server creation, and outgoing request capabilities.
* **Why It Exists**: Acts as the built-in foundation for web servers in Node.js, converting raw network socket data (TCP streams) into standard web request and response objects.
* **Key Concepts**:
  * **Network Bridge**: Directs TCP sockets into Node's parser, exposing headers, paths, and methods to the runtime environment.
  * **IncomingMessage (`req`)**: Acts as a readable stream of incoming network request chunks, capturing headers, verbs, and query strings.
  * **ServerResponse (`res`)**: A writable stream used to send response headers, set status codes, and write content payloads back to clients.

### Key Commands / Code Example:

```javascript
const http = require('http');

const server = http.createServer((req, res) => {
  // Set response headers and status codes
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('Hello from the Node.js core HTTP module');
});

// Bind to TCP port
server.listen(8080, () => {
  console.log('HTTP Server listening on port 8080');
});
```

> [!IMPORTANT]
> The core HTTP module provides no built-in path routing, body parsing, static file support, or security configuration. These must be implemented manually or via frameworks.

---

## 22. Creating Web Servers

🔗 **Full Lesson:** [22_Creating_Web_Servers.md](./22_Creating_Web_Servers.md)

* **What**: Network applications created in Node.js to listen on a designated TCP port, parse incoming HTTP requests, and stream back HTTP responses.
* **Why It Exists**: Allows you to serve dynamic web pages or API data by inspecting the client's requested URL and routing it to the correct handler function.
* **Key Concepts**:
  * **Request Routing**: Matching the incoming request URL and method (e.g. GET `/api/users`) to execute distinct logic.
  * **Body Buffer Stream**: In raw servers, requests containing body data (like POST) must be read asynchronously in chunks from the readable stream.
  * **Header Management**: Setting proper Content-Length, Content-Type, and CORS headers to ensure browsers parse payloads correctly.

### Key Commands / Code Example:

```javascript
const http = require('http');

const server = http.createServer((req, res) => {
  if (req.method === 'POST' && req.url === '/submit') {
    let body = '';
    
    // Read request body chunk stream
    req.on('data', chunk => { body += chunk; });
    
    req.on('end', () => {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ status: 'Success', received: body }));
    });
  } else {
    res.writeHead(404);
    res.end('Route Not Found');
  }
});
server.listen(3000);
```

> [!WARNING]
> Always restrict incoming request sizes in raw HTTP server handlers to prevent clients from sending infinitely large data payloads that crash server memory.

---

## 23. REST APIs

🔗 **Full Lesson:** [23_REST_APIs.md](./23_REST_APIs.md)

* **What**: Representational State Transfer APIs, an architectural style for designing web endpoints that standardizes stateless resource operations using HTTP verbs and JSON representations.
* **Why It Exists**: Standardizes how different systems talk to each other by using a consistent, stateless design with standard web actions (GET, POST, etc.) and response codes.
* **Key Concepts**:
  * **Stateless Architecture**: Each HTTP request must contain all context and tokens required to process it, without depending on server-side session states.
  * **HTTP Resource Verbs**: Utilizes HTTP verbs to map resource actions: GET (retrieve), POST (create), PUT (replace), PATCH (update parts), and DELETE (remove).
  * **Status Code Standards**: Uses status codes to return structural results: 200/201 (success), 400 (bad input), 401 (no authentication), 403 (unauthorized), 404 (missing), 500 (internal failure).

### Key Commands / Code Example:

```javascript
// Structural example of route resource actions mapping:
// GET    /api/v1/orders     ---> Retrieve list of orders (returns 200 OK)
// POST   /api/v1/orders     ---> Create new order (returns 201 Created)
// GET    /api/v1/orders/:id ---> Retrieve order detail (returns 200 OK or 404)
// PATCH  /api/v1/orders/:id ---> Update order details (returns 200 OK)
// DELETE /api/v1/orders/:id ---> Delete order (returns 204 No Content)
```

> [!IMPORTANT]
> REST API responses should always format output envelopes using standard formats (like JSON) and return correct HTTP status codes to help clients handle exceptions reliably.

---

## 24. Express.js

🔗 **Full Lesson:** [24_ExpressJS.md](./24_ExpressJS.md)

* **What**: A minimal and flexible Node.js web application framework that provides a robust suite of features for web and mobile applications.
* **Why It Exists**: Eliminates the complex boilerplate code needed to build servers using Node.js's built-in HTTP module, replacing it with an easy-to-use routing system.
* **Key Concepts**:
  * **Middleware Pipeline**: Processes incoming requests sequentially through an array of functions before returning a response.
  * **Response Abstractions**: Simplifies tasks with helper APIs like `res.json()`, `res.status()`, and `res.sendFile()`.
  * **Route Param Parsing**: Automatically parses parameters from route segments (e.g. `/users/:id` maps parameter to `req.params.id`).

### Key Commands / Code Example:

```javascript
const express = require('express');
const app = express();

// Global body parser middleware
app.use(express.json());

// Express route handling parameters
app.get('/api/users/:userId', (req, res) => {
  const { userId } = req.params;
  res.status(200).json({ id: userId, active: true });
});

app.listen(3000, () => console.log('Express active on port 3000'));
```

> [!WARNING]
> In Express 4.x, uncaught exceptions in asynchronous code blocks will hang the request or crash the process. You must wrap async handlers in try/catch and pass errors to `next(err)`.

---

## 25. Middleware

🔗 **Full Lesson:** [25_Middleware.md](./25_Middleware.md)

* **What**: Intermediary functions in the Express request-response lifecycle that intercept requests, run code, modify request/response objects, and call `next()`.
* **Why It Exists**: Allows you to run code (like verifying logins, checking inputs, or logging requests) in a sequence before your main route code processes the request.
* **Key Concepts**:
  * **The Middleware Signature**: A function accepting `req`, `res`, and `next` arguments. Calling `next()` forwards control down the chain.
  * **Types of Middleware**: Classified into Application-level (`app.use`), Router-level, Built-in (e.g. `express.static`), Third-party (e.g. `cors`), and Error-handling.
  * **Execution Sequence**: Order matters. Middleware declared first executes first. Global parsers must sit above routes.

### Key Commands / Code Example:

```javascript
const express = require('express');
const app = express();

// Custom Application-level middleware for request logging
const apiLogger = (req, res, next) => {
  console.log(`[LOG] ${new Date().toISOString()} - ${req.method} ${req.url}`);
  next(); // Pass execution context forward
};

app.use(apiLogger);

app.get('/data', (req, res) => res.send('Sensitive API Data'));
```

> [!IMPORTANT]
> If a middleware does not call `next()` or send a response (e.g., `res.send`), the request will hang indefinitely and leak server connection slots.

---

## 26. Routing

🔗 **Full Lesson:** [26_Routing.md](./26_Routing.md)

* **What**: The mechanism in Express used to map incoming request endpoints (method and URI path) to specific controller handler functions.
* **Why It Exists**: Keeps your server code organized by letting you split different web routes and endpoints into separate, clean files instead of cluttering a single file.
* **Key Concepts**:
  * **express.Router**: A mini-application instance capable of executing middleware and routing functions, mounted dynamically onto parent applications.
  * **Parameter Matching**: Supports path patterns (wildcards, regex, colon variables) to parse variables dynamically.
  * **Router Mounting**: Groups related endpoints (e.g. `/api/v1/users`) into dedicated sub-routers to maintain a clean project structure.

### Key Commands / Code Example:

```javascript
// routes/userRoutes.js
const express = require('express');
const router = express.Router();

// Define relative sub-paths
router.post('/login', (req, res) => res.json({ token: 'jwt' }));
router.get('/profile', (req, res) => res.json({ user: 'active' }));

module.exports = router;

// Mount in server.js
// const userRouter = require('./routes/userRoutes');
// app.use('/api/v1/users', userRouter);
```

> [!IMPORTANT]
> Define specific static routes (e.g. `/users/active`) before dynamic parameter paths (e.g. `/users/:id`) to prevent wildcards from intercepting and overriding requests.

---

## 27. MVC Architecture

🔗 **Full Lesson:** [27_MVC_Architecture.md](./27_MVC_Architecture.md)

* **What**: Model-View-Controller, an architectural design pattern that separates application logic into data management (Model), presentation representation (View), and routing logic (Controller).
* **Why It Exists**: Splits code into three logical layers. This separation keeps your codebase organized, clean, and easy to test.
* **Key Concepts**:
  * **Model Layer**: Enforces schema rules, executes database queries, and manages data states.
  * **Controller Layer**: Intercepts requests, validates inputs, invokes models, and determines which view to output.
  * **View Layer**: Formats the response representation (returning JSON structures in modern REST APIs, or server-side HTML template engines).

### Key Commands / Code Example:

```javascript
// controllers/productController.js
const Product = require('../models/productModel');

// Controller isolates business logic from server configuration
exports.getProductDetails = async (req, res, next) => {
  try {
    const product = await Product.findById(req.params.productId);
    if (!product) {
      return res.status(404).json({ error: 'Product not found' }); // View output representation
    }
    res.status(200).json(product);
  } catch (err) {
    next(err); // Route exceptions to error handling middleware
  }
};
```

> [!IMPORTANT]
> Keep controllers thin. Avoid writing raw SQL queries, data validations, or complex business algorithms directly inside controller files; delegate them to model schemas or helper service files.

---

## 28. Environment Variables

🔗 **Full Lesson:** [28_Environment_Variables.md](./28_Environment_Variables.md)

* **What**: System-level key-value variables loaded into application memory (`process.env`) to configure external integrations, ports, and credentials securely outside source code.
* **Why It Exists**: Hardcoding passwords and secret keys inside your source files is a massive security risk. Environment variables store these secrets safely outside of your code configuration.
* **Key Concepts**:
  * **process.env**: The Node.js object mapping current system shell environment variables inside runtime memory.
  * **dotenv Library**: Reads local `.env` configuration files during application bootstrap and writes key-value pairs into `process.env`.
  * **Configuration Management**: Allows loading different credentials (dev, staging, prod) dynamically based on the execution context.

### Key Commands / Code Example:

```javascript
// Server bootstrap configuration
require('dotenv').config();

// Access system variable configurations
const PORT = process.env.PORT || 3000;
const DB_URL = process.env.MONGO_URI;

if (!DB_URL) {
  console.error('Critical Error: MONGO_URI variable is undefined');
  process.exit(1); // abort server start
}
```

> [!WARNING]
> Never commit `.env` files containing actual production keys to git. Always add `.env` to your `.gitignore` and supply a `.env.example` file showing placeholder structures.

---

## 29. Validation

🔗 **Full Lesson:** [29_Validation.md](./29_Validation.md)

* **What**: The process of validating and sanitizing client request payloads (body, query, params) against a strict schema contract at the API boundary.
* **Why It Exists**: Web servers should never trust data sent by users. Validation checks and cleans client inputs at the entry point of your API to keep the database secure and error-free.
* **Key Concepts**:
  * **Request Sanitization**: Strips illegal characters, scripts, or undefined object keys from payloads before parsing.
  * **Schema Validation**: Validates bodies, URL parameters, and headers against strict structural definitions using validator libraries (e.g. Zod or Joi).
  * **Boundary Defense**: Catching validation errors at request pipelines protects database layers from parsing failures.

### Key Commands / Code Example:

```javascript
const { z } = require('zod');

// Schema validation contract
const registerUserSchema = z.object({
  email: z.string().email('Invalid email address format'),
  username: z.string().min(3, 'Username must be at least 3 characters long'),
  password: z.string().min(8, 'Password must be at least 8 characters long')
});

// Middleware parsing body schemas
const validateRegister = (req, res, next) => {
  const result = registerUserSchema.safeParse(req.body);
  if (!result.success) {
    return res.status(400).json({ errors: result.error.format() });
  }
  req.validatedBody = result.data;
  next();
};
```

> [!IMPORTANT]
> Always run strict data validations on the server. Client-side browser checks are easily bypassed using terminal utilities or API clients.

---

## 30. Error Handling

🔗 **Full Lesson:** [30_Error_Handling.md](./30_Error_Handling.md)

* **What**: The design patterns and middleware handlers used to intercept, log, and respond to runtime exceptions gracefully without crashing the Node.js process.
* **Why It Exists**: An unhandled crash will shut down the entire Node.js server. Proper error handling keeps the server running, logs errors for debugging, and returns clear, safe error messages to clients.
* **Key Concepts**:
  * **Error Middleware Signature**: Express maps errors to middleware functions containing 4 arguments: `(err, req, res, next)`.
  * **Error Categorization**: Splits failures into Operational (predictable issues like invalid credentials) and Programmer errors (unhandled system bugs).
  * **Crash Management**: Real-world servers should log programmer errors and perform a graceful shutdown while process managers (like PM2) spin up replacement instances.

### Key Commands / Code Example:

```javascript
// Custom operational error helper
class AppError extends Error {
  constructor(message, statusCode) {
    super(message);
    this.statusCode = statusCode;
    this.isOperational = true; // Mark as expected error
    Error.captureStackTrace(this, this.constructor);
  }
}

// Global Express Error Handler Middleware
app.use((err, req, res, next) => {
  const status = err.statusCode || 500;
  const message = err.message || 'Internal Server Error';
  
  res.status(status).json({
    success: false,
    error: {
      message,
      // Only attach stack trace during local development testing
      stack: process.env.NODE_ENV === 'development' ? err.stack : undefined
    }
  });
});
```

> [!IMPORTANT]
> Never expose raw stack traces (`err.stack`) to clients in production. Stack traces leak internal directory structures, library versions, and database schemas.

---

## 31. Logging

🔗 **Full Lesson:** [31_Logging.md](./31_Logging.md)

* **What**: A structured event-logging mechanism in Node.js that formats logs as JSON asynchronously, replacing slow blocking console writes.
* **Why It Exists**: Using `console.log()` in production slows down the server because it runs synchronously when writing to terminals or files. Structured logging formats logs as single-line JSON statements, allowing log shippers and dashboards to index and search queries instantly under heavy load.
* **Key Concepts**:
  * **Structured Log Outputs**: Formatting logs as single-line JSON structures to facilitate machine parsing and indexing.
  * **Log Severity Levels**: Categorizing events by severity: debug, info, warn, and error, to filter out verbose traffic in production.
  * **Asynchronous Shaving**: Buffering outputs and writing log payloads using non-blocking filesystems to prevent event loop bottlenecks.

### Key Commands / Code Example:

```javascript
const pino = require('pino');

// Highly optimized, JSON-structured asynchronous logger
const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  timestamp: pino.stdTimeFunctions.isoTime
});

logger.info({ userId: 101, action: 'order_create' }, 'Order processed successfully');
logger.error({ err: new Error('DB Connection Timeout') }, 'Database transaction failed');
```

> [!IMPORTANT]
> Never use `console.log()` in request pipelines. Use dedicated, asynchronous structured log libraries like Pino or Winston to keep application throughput high.

---

## 32. Authentication

🔗 **Full Lesson:** [32_Authentication.md](./32_Authentication.md)

* **What**: The security practice of verifying a user's identity using cryptographically salted password hashing algorithms (like Bcrypt or Argon2).
* **Why It Exists**: Verifies exactly who a user is (e.g. via passwords or tokens) before letting them access private features on the server.
* **Key Concepts**:
  * **Cryptographic Salt Hashing**: Salting introduces random strings to password fields before hashing, rendering rainbow-table lookup strategies useless.
  * **Argon2/Bcrypt Standards**: Algorithms designed with high processing costs to slow down calculations and mitigate brute-force attempts.
  * **Token/Session Mapping**: Binding authenticated request streams to either temporary signed payloads (JWT) or database reference IDs (sessions).

### Key Commands / Code Example:

```javascript
const bcrypt = require('bcrypt');

const hashPassword = async (plainPassword) => {
  const saltRounds = 12; // Computation cost factor
  const salt = await bcrypt.genSalt(saltRounds);
  return bcrypt.hash(plainPassword, salt);
};

const verifyPassword = async (plainPassword, hashedPassword) => {
  return bcrypt.compare(plainPassword, hashedPassword);
};
```

> [!IMPORTANT]
> Never store raw passwords or apply weak hashing algorithms (like MD5 or SHA-1) in database collections. Always hash credentials using bcrypt, scrypt, or Argon2.

---

## 33. Authorization

🔗 **Full Lesson:** [33_Authorization.md](./33_Authorization.md)

* **What**: The access control mechanism that checks authenticated user roles and permissions (RBAC or ABAC) to restrict access to secure endpoints.
* **Why It Exists**: Restricts what an identified user can do. It checks their roles or permissions to ensure a regular user cannot perform admin-only actions.
* **Key Concepts**:
  * **Role-Based Access Control (RBAC)**: Defining fixed roles (e.g. admin, user, editor) and checking if active requests carry matching tags.
  * **Attribute-Based Access Control (ABAC)**: Fine-grained access control inspecting resource ownership (e.g. checking if `requestingUser.id === document.ownerId`).
  * **Access Middleware Hooks**: Intercepting requests inside early pipeline stages to evaluate authorization flags and return HTTP 403 Forbidden on check failures.

### Key Commands / Code Example:

```javascript
// Middleware factory checking role clearance
const restrictToRoles = (...allowedRoles) => {
  return (req, res, next) => {
    // Rely on req.user populated by auth middleware
    if (!req.user || !allowedRoles.includes(req.user.role)) {
      return res.status(403).json({ error: 'Access denied: Insufficient privileges' });
    }
    next(); // role allowed, proceed
  };
};

// Usage: app.get('/admin', authenticate, restrictToRoles('admin'), adminController);
```

> [!IMPORTANT]
> Authorization modules must always execute after authentication modules, as role parsing requires accessing validated identities populated on the request object.

---

## 34. JWT

🔗 **Full Lesson:** [34_JWT.md](./34_JWT.md)

* **What**: JSON Web Token, an open standard (RFC 7519) that defines a compact, self-contained, and cryptographically signed payload for stateless authentication.
* **Why It Exists**: Provides a secure, signed token that the client carries with every request. This lets the server authorize the user instantly without checking a database session table.
* **Key Concepts**:
  * **JWT Creation Pipeline**: Header and Payload are Base64Url encoded first. The string `encodedHeader + "." + encodedPayload` is signed with a key via HMAC-SHA256. The resulting binary digest is Base64Url encoded to form the signature. Final format: `header.payload.signature`.
  * **`jwt.verify` Behind-the-Scenes**: Splits token by `.`, decodes header, reconstructs `unsignedData`, re-computes expected signature digest using secret key, compares signatures using **timing-safe comparison** (`crypto.timingSafeEqual`), decodes payload, and checks expiration (`exp`).
  * **Stateless Validation**: The server verifies the token signature using a local secret key (HS256) or public key (RS256). If valid, the payload claims are trusted without database queries.
  * **Expiry Guarding**: Enforcing short lifespans (e.g., 15 minutes) on access tokens and utilizing refresh token flows to renew keys.

### Key Commands / Code Example:

```javascript
const jwt = require('jsonwebtoken');

// Generate stateless token with 15 minute lifespan
const token = jwt.sign(
  { id: 'usr_101', role: 'editor' }, 
  process.env.JWT_SECRET, 
  { expiresIn: '15m' }
);

try {
  // jwt.verify re-computes signature using secret, does timing-safe comparison, & checks exp claim
  const payload = jwt.verify(token, process.env.JWT_SECRET);
  console.log('Decoded Claims:', payload);
} catch (err) {
  console.error('Invalid or Expired Token:', err.message);
}
```

> [!WARNING]
> JWT payloads are only base64Url encoded, NOT encrypted. Never store sensitive credentials (like passwords, keys, or private phone numbers) inside JWT claims.

---

## 35. Cookies

🔗 **Full Lesson:** [35_Cookies.md](./35_Cookies.md)

* **What**: Cryptographically signed client-side data containers automatically attached by browsers to outgoing requests, configured with security flags to protect sessions.
* **Why It Exists**: Allows the server to store tiny pieces of information (like a session ID) on the user's browser, which the browser automatically sends back with every future request.
* **Key Concepts**:
  * **HttpOnly Protection**: Prevents client-side scripts (like `document.cookie`) from reading the cookie, mitigating token theft via Cross-Site Scripting (XSS).
  * **Secure Protocol Constraint**: Restricts cookies to be transmitted only over TLS/HTTPS encrypted connections, preventing interception.
  * **SameSite Context Rules**: Restricts when cookies are sent on cross-site requests, mitigating Cross-Site Request Forgery (CSRF).

### Key Commands / Code Example:

```javascript
const express = require('express');
const app = express();

app.get('/login', (req, res) => {
  // Writing secure cookie payload in Express
  res.cookie('token', 'jwt_session_token_payload', {
    httpOnly: true, // Shields against XSS extractions
    secure: true,   // Transmit only over HTTPS connections
    sameSite: 'strict', // Blocks CSRF attempts
    maxAge: 900000 // Lifespan in milliseconds (15 mins)
  });
  res.send('Cookie written');
});
```

> [!IMPORTANT]
> Always set `HttpOnly` and `Secure` flags on authentication cookies to prevent access tokens from being stolen by malicious client-side JavaScript.

---

## 36. Sessions

🔗 **Full Lesson:** [36_Sessions.md](./36_Sessions.md)

* **What**: A stateful user tracking mechanism where session context is stored in a centralized server-side database (like Redis) and mapped to a signed client cookie ID.
* **Why It Exists**: Manages user logins securely by storing active login details directly on the server, while the client's browser only holds a random, temporary "session ID" cookie.
* **Key Concepts**:
  * **Stateful Control**: User variables (auth status, shopping carts) are stored in server memory (e.g. Redis). The client only gets a cryptographically signed session ID.
  * **Access Revocation**: Session states can be instantly deleted on the server, immediately terminating client access (a key advantage over stateless JWTs).
  * **Central Store Scaling**: Storing session states in local RAM breaks load balancing. Production clusters require storing sessions in shared, fast memory stores like Redis.

### Key Commands / Code Example:

```javascript
const session = require('express-session');
const RedisStore = require('connect-redis').default;
const redis = require('redis');

const redisClient = redis.createClient({ url: process.env.REDIS_URL });

// Configures stateful session manager backed by Redis
const sessionConfig = {
  store: new RedisStore({ client: redisClient }),
  secret: process.env.SESSION_SECRET,
  resave: false,
  saveUninitialized: false,
  cookie: {
    httpOnly: true,
    secure: true, // Requires HTTPS
    maxAge: 3600000 // 1 hour
  }
};
```

> [!IMPORTANT]
> Always configure a shared in-memory database (like Redis) for sessions in production. Using the default server memory store (`MemoryStore`) causes memory leaks and breaks session persistence behind load balancers.

---

## 37. MongoDB

🔗 **Full Lesson:** [37_MongoDB.md](./37_MongoDB.md)

* **What**: A flexible, document-based NoSQL database that represents data as dynamic BSON records, supporting horizontal scaling through sharding.
* **Why It Exists**: A flexible, document-based database that stores data as JSON-like records. This makes it easy to change database structures on the fly and scale out across multiple servers.
* **Key Concepts**:
  * **Document Store model**: Organizations map schemas directly to nested JSON fields (subdocuments, arrays), reducing the need for complex, slow SQL joins.
  * **Horizontal Sharding**: Scales write-heavy databases by partitioning data ranges across multiple database shards.
  * **Index Configurations**: B-Tree indexes speed up lookups, but slow down writes as indexes must be rebuilt on each document insert.

### Key Commands / Code Example:

```javascript
const { MongoClient } = require('mongodb');
const client = new MongoClient(process.env.MONGO_URI);

async function addProduct() {
  await client.connect();
  const db = client.db('ecom');
  const products = db.collection('products');
  
  // Insert flexible document structure with nested properties
  await products.insertOne({
    name: 'SSD Drive',
    attributes: { speed: '5000MB/s', capacity: '1TB' },
    tags: ['storage', 'pc-build']
  });
}
```

> [!IMPORTANT]
> MongoDB is schema-less by default. To prevent structural data pollution, enforce strict schema validations inside your code layer (e.g. using Mongoose) or configure MongoDB Schema Validation rules on collections.

---

## 38. Mongoose

🔗 **Full Lesson:** [38_Mongoose.md](./38_Mongoose.md)

* **What**: An Object Data Modeling (ODM) library for MongoDB that provides strict schema validation, type casting, and query hook middleware inside Node.js.
* **Why It Exists**: Adds structure and validation rules to MongoDB. It defines clear templates (schemas) inside your Node.js code to ensure only valid data is saved.
* **Key Concepts**:
  * **Strict Schema Mapping**: Sanitizes incoming document fields, rejecting properties not explicitly declared inside the schema definition.
  * **Active Record Hooks**: Invoking middleware hooks (e.g. hashing passwords inside the `'save'` hook before writing to database collections).
  * **Virtuals & Populate**: Simulates data relations (virtual joins) by linking document IDs and populating referenced structures during query execution.

### Key Commands / Code Example:

```javascript
const mongoose = require('mongoose');

// Schema declaration
const userSchema = new mongoose.Schema({
  email: { type: String, required: true, unique: true, lowercase: true },
  password: { type: String, required: true, select: false } // Hidden in queries by default
});

// Pre-save schema middleware hook
userSchema.pre('save', async function(next) {
  if (!this.isModified('password')) return next();
  this.password = await require('bcrypt').hash(this.password, 12);
  next();
});

const User = mongoose.model('User', userSchema);
```

> [!WARNING]
> Mongoose `.populate()` is an application-level abstraction that executes multiple query roundtrips to fetch linked documents, degrading performance under heavy read loads.

---

## 39. PostgreSQL

🔗 **Full Lesson:** [39_PostgreSQL.md](./39_PostgreSQL.md)

* **What**: A powerful, open-source object-relational SQL database focusing on structural integrity, ACID compliance, and query optimizations.
* **Why It Exists**: A reliable relational database that structures data in traditional tables. It guarantees strict rules (ACID compliance) so that transactions never corrupt your data.
* **Key Concepts**:
  * **Relational Integrity**: Table schemas enforce rigid fields, data types, and foreign key relations to protect data structure rules.
  * **ACID Compliance**: Ensures transactions are Atomic, Consistent, Isolated, and Durable, preventing data corruption during failures.
  * **Query Optimizations**: Utilizes query planners, explain scopes, and indexing (B-Tree, GIN) to optimize query paths over large datasets.

### Key Commands / Code Example:

```javascript
const { Pool } = require('pg');
const pool = new Pool({ connectionString: process.env.DATABASE_URL });

async function fetchUserById(userId) {
  // Parametric inputs protect execution scopes from SQL injection injections
  const query = 'SELECT id, email, role FROM users WHERE id = $1';
  const values = [userId];
  
  const res = await pool.query(query, values);
  return res.rows[0];
}
```

> [!IMPORTANT]
> Always use parameterized queries (`$1`, `$2`) or query builders when querying SQL tables. Raw string concatenation allows users to inject SQL commands and hijack databases.

---

## 40. ORM Concepts

🔗 **Full Lesson:** [40_ORM_Concepts.md](./40_ORM_Concepts.md)

* **What**: Object-Relational Mapping, a design pattern that translates database tables and relational rows into JavaScript objects, abstracting SQL syntax.
* **Why It Exists**: Allows developers to write database queries using regular JavaScript objects and methods, avoiding the need to write raw SQL strings inside their code.
* **Key Concepts**:
  * **Data Mapping Patterns**: Active Record pattern (models define fields and carry query methods) vs. Data Mapper pattern (entities are thin, repositories query data).
  * **Schema Sync & Migrations**: Managing database changes programmatically using migration files to track modifications in version control.
  * **The N+1 Query Problem**: An optimization issue where querying parent records executes separate database requests for each child record, bloating network latency.

### Key Commands / Code Example:

```javascript
// Structural example showing ORM abstractions vs SQL queries:
// Data Mapper Pattern:
// const users = await userRepository.find({ where: { status: 'active' } });
//
// Translates to database query:
// SELECT id, email, status FROM users WHERE status = 'active';
```

> [!IMPORTANT]
> Do not let ORMs mask execution costs. Regularly log and audit the queries generated by ORMs during database queries to identify and resolve N+1 performance bottlenecks.

---

## 40a. Sequelize ORM

🔗 **Full Lesson:** [40a_Sequelize_ORM.md](./40a_Sequelize_ORM.md)

* **What**: A widely-used promise-based Node.js ORM for relational databases (like PostgreSQL) that manages table models, migrations, and transactions.
* **Why It Exists**: A widely-used JavaScript library for relational databases (like PostgreSQL). It maps database tables directly to JavaScript classes, simplifying table relationships and updates.
* **Key Concepts**:
  * **Model Associations**: Declaring table relations using Active Record helpers: `hasMany`, `belongsTo`, and `belongsToMany`.
  * **Managed Transactions**: Wrapping database queries in transaction hooks to automatically roll back changes if intermediate errors occur.
  * **Migration Scaffolding**: Modifying table structures sequentially using version-controlled up/down script files.

### Key Commands / Code Example:

```javascript
const { Sequelize, DataTypes } = require('sequelize');
const sequelize = new Sequelize(process.env.DATABASE_URL);

const User = sequelize.define('User', {
  email: { type: DataTypes.STRING, allowNull: false, unique: true }
});

// Managed Transaction scope
async function createUser(emailData) {
  try {
    await sequelize.transaction(async (t) => {
      const newUser = await User.create({ email: emailData }, { transaction: t });
      return newUser;
    });
  } catch (err) {
    // sequelize rolls back transaction auto-handling errors
    console.error('Transaction Failed:', err.message);
  }
}
```

> [!IMPORTANT]
> Avoid using `sequelize.sync({ force: true })` in production, as it drops tables and deletes data on startup. Always use version-controlled CLI migrations instead.

---

## 41. Redis

🔗 **Full Lesson:** [41_Redis.md](./41_Redis.md)

* **What**: An open-source, in-memory key-value data structure store used as a high-speed database, cache, and session broker.
* **Why It Exists**: Reading from a standard disk database is slow. Redis stores data directly in the server's fast RAM, serving cached database results and login sessions almost instantly.
* **Key Concepts**:
  * **In-Memory Architecture**: Holds datasets in server RAM, periodically writing snapshots to disk asynchronously to prevent data loss.
  * **Data Types**: Supports keys mapped to Strings, Hashes (objects), Lists (queues), and Sets (unique listings).
  * **TTL Expiry**: Attaches Time-To-Live (TTL) timestamps to keys to automatically purge stale cache entries.

### Key Commands / Code Example:

```javascript
const redis = require('redis');
const client = redis.createClient({ url: process.env.REDIS_URL });

async function cacheProfile(userId, profileData) {
  await client.connect();
  
  // Set key value with TTL expiration of 3600 seconds (1 hour)
  await client.set(`user:${userId}`, JSON.stringify(profileData), { EX: 3600 });
  
  // Fetch key value
  const cachedVal = await client.get(`user:${userId}`);
  return JSON.parse(cachedVal);
}
```

> [!IMPORTANT]
> Configure Redis keys with explicit expiration timeouts (TTL) to avoid consuming all RAM and crashing the Redis server.

---

## 42. Caching

🔗 **Full Lesson:** [42_Caching.md](./42_Caching.md)

* **What**: The optimization strategy of storing copies of database query results in high-speed RAM (like Redis) to accelerate future API response times.
* **Why It Exists**: Speeds up response times and reduces server load by saving copies of database query results in temporary fast memory so they don't have to be calculated again.
* **Key Concepts**:
  * **Cache-Aside Pattern**: The application checks the cache layer first. On a cache miss, it queries the database, writes the result to the cache, and returns it.
  * **Cache Invalidation**: Updating or deleting cached data immediately when database records are modified to prevent returning stale data to users.
  * **Cache Stampede / Herd Effect**: An issue where multiple concurrent requests query the database simultaneously when a cache key expires, degrading database performance.

### Key Commands / Code Example:

```javascript
async function getCachedStats() {
  const cacheKey = 'site:analytics:stats';
  const cachedData = await redisClient.get(cacheKey);
  
  if (cachedData) {
    return JSON.parse(cachedData); // Cache Hit
  }
  
  // Cache Miss: Query SQL/Mongo
  const dbData = await DB.runAnalyticsQuery();
  
  // Write to cache with 5 minute expiration limit
  await redisClient.set(cacheKey, JSON.stringify(dbData), { EX: 300 });
  return dbData;
}
```

> [!WARNING]
> Cache invalidation is notoriously difficult. If database records are modified, you must instantly delete or update corresponding cache keys to avoid returning stale data.

---

## 43. Rate Limiting

🔗 **Full Lesson:** [43_Rate_Limiting.md](./43_Rate_Limiting.md)

* **What**: The security and resource-protection mechanism that limits the frequency of client requests over a specific time window to prevent API abuse.
* **Why It Exists**: Protects web APIs from being overwhelmed by spam, scrapers, or hackers by limiting how many requests a single user can send in a short timeframe.
* **Key Concepts**:
  * **Token Bucket / Sliding Window**: Algorithms that track request frequencies inside sliding windows to throttle excessive client requests.
  * **Redis Tracking**: Using client IP addresses as key flags in Redis and incrementing counters to block clients exceeding limits.
  * **Throttling Responses**: Returning HTTP status code `429 Too Many Requests` along with standard `Retry-After` headers once limits are reached.

### Key Commands / Code Example:

```javascript
const rateLimit = require('express-rate-limit');

// Configure rate limit rules
const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes window
  max: 100, // Limit each client IP to 100 requests per window
  standardHeaders: true, // Return rate limit info in headers
  legacyHeaders: false,
  message: 'Too many requests generated from this IP, please retry later.'
});

// Apply rate limiter middleware to sensitive routes
// app.use('/api/v1/auth', apiLimiter);
```

> [!IMPORTANT]
> When running APIs behind load balancers or reverse proxies (like Nginx), configure `app.set('trust proxy', 1)` in Express to ensure the rate limiter reads the client IP instead of the load balancer IP.

---

## 44. File Uploads

🔗 **Full Lesson:** [44_File_Uploads.md](./44_File_Uploads.md)

* **What**: The system mechanics and security policies involved in parsing, validating, and storing multi-part file payloads (via Multer) to local or cloud object stores.
* **Why It Exists**: Provides a safe way for servers to receive, check, and store files (like profile photos or PDFs) sent by clients without causing security risks.
* **Key Concepts**:
  * **multipart/form-data encoding**: The standard HTTP encoding format for files, requiring specialized parsers to read file binary streams.
  * **Disk vs Memory Storage**: Multer can write files to a temporary disk location or buffer them directly in RAM to stream to cloud storage buckets.
  * **Validation Filtering**: Checking file size limits and MIME types at the route boundary to reject execute-permissions files (e.g. `.exe`, `.sh`).

### Key Commands / Code Example:

```javascript
const multer = require('multer');

// Configure memory storage to buffer files for cloud upload
const uploader = multer({
  storage: multer.memoryStorage(),
  limits: { fileSize: 5 * 1024 * 1024 }, // Max file size limit: 5MB
  fileFilter: (req, file, cb) => {
    if (file.mimetype.startsWith('image/')) {
      cb(null, true);
    } else {
      cb(new Error('Format error: Only image uploads are permitted'), false);
    }
  }
});
```

> [!WARNING]
> Do not store user-uploaded files on local server disks in load-balanced clusters, as other server nodes will not be able to access those files. Stream uploads directly to a centralized object store (like AWS S3).

---

## 45. Email Services

🔗 **Full Lesson:** [45_Email_Services.md](./45_Email_Services.md)

* **What**: Transactional mail services in Node.js (via Nodemailer) used to compile templates and send emails asynchronously in background workers.
* **Why It Exists**: Allows servers to automatically send email alerts (like password resets or sign-up confirmations) to users when actions occur.
* **Key Concepts**:
  * **SMTP Transport vs. Web APIs**: Sending emails via direct SMTP configurations (using Nodemailer) vs. calling transactional email API providers (SendGrid, Mailgun).
  * **HTML Templating**: Compiling responsive HTML email templates programmatically using template engines (Handlebars, EJS) to support personalized variables.
  * **Asynchronous Queuing**: Offloading mailing tasks to background queues to prevent email delivery latency from blocking HTTP requests.

### Key Commands / Code Example:

```javascript
const nodemailer = require('nodemailer');

// Set SMTP transport relay
const transporter = nodemailer.createTransport({
  host: process.env.SMTP_HOST,
  port: parseInt(process.env.SMTP_PORT),
  auth: { user: process.env.SMTP_USER, pass: process.env.SMTP_PASS }
});

async function sendNotification(emailTarget, username) {
  const mailDetails = {
    from: '"Billing Division" <billing@ecom.com>',
    to: emailTarget,
    subject: 'Receipt: Transaction Completed',
    html: `<h3>Greetings ${username},</h3><p>Your payment has been finalized.</p>`
  };
  await transporter.sendMail(mailDetails);
}
```

> [!IMPORTANT]
> Never send emails synchronously inside request handlers. Offload mailing tasks to an asynchronous task runner or message queue (like BullMQ) to avoid slowing down API responses.

---

## 45a. Payment Gateways (Razorpay and Stripe)

🔗 **Full Lesson:** [45a_Payment_Gateways_Razorpay_and_Stripe.md](./45a_Payment_Gateways_Razorpay_and_Stripe.md)

* **What**: Integrations with secure credit card transaction platforms (like Stripe or Razorpay) to process payments using client-side tokenization and backend webhooks.
* **Why It Exists**: Handling credit cards directly on your server requires expensive, strict security audits. Payment gateways securely collect card details in the browser, keeping your server safe and out of scope.
* **Key Concepts**:
  * **Card Tokenization**: Card details are processed on the gateway's secure network. The backend only receives a secure token to execute the transaction.
  * **Client-Server Coordination**: Orchestrating payment flows: backend sets up payment details, client completes payment via gateway UI, and backend verifies success.
  * **Webhook Verification**: Gateways emit async HTTP POST callbacks to confirm payment success. The backend must cryptographically verify webhook signatures to prevent fraud.

### Key Commands / Code Example:

```javascript
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

// Create Stripe PaymentIntent with target billing currencies
async function initializeCheckoutIntent(orderId, totalAmountInCents) {
  const paymentIntent = await stripe.paymentIntents.create({
    amount: totalAmountInCents, // e.g. $10.00 is represented as 1000 cents
    currency: 'usd',
    metadata: { orderId },
    automatic_payment_methods: { enabled: true }
  });
  return paymentIntent.client_secret; // Send to client for secure checkout
}
```

> [!IMPORTANT]
> Always verify webhook signatures using raw request buffers. Attackers can forge HTTP request bodies to trigger fake checkout confirmations on your backend.

---

## 45b. Payment Gateways (Real-Time Scenarios)

🔗 **Full Lesson:** [45b_Payment_Gateways_real_time_scenerios.md](./45b_Payment_Gateways_real_time_scenerios.md)

* **What**: Advanced transactional handling patterns in payment processing to manage concurrency, idempotency, timeouts, and network drops.
* **Why It Exists**: Real-world payments have complex issues (like network failures or database crashes during a payment). The server must handle these edge cases to prevent charging users twice or losing orders.
* **Key Concepts**:
  * **Payment Idempotency**: Utilizing idempotency keys in API requests to prevent double-charging users during network retries.
  * **checkout-timers**: Reserving stock temporarily while the payment is processed. If the checkout fails or expires, the reserved inventory is automatically released.
  * **Webhook Idempotency**: Design database webhook handlers to identify and ignore duplicate events from payment gateways.

### Key Commands / Code Example:

```javascript
// Stripe charge creation using an Idempotency Key
async function processDirectCharge(customerId, amountVal, uniqueRequestToken) {
  const charge = await stripe.charges.create({
    amount: amountVal,
    currency: 'usd',
    customer: customerId
  }, {
    // Prevents double-charging if connection fails and the client retries the request
    idempotencyKey: `charge_token_${uniqueRequestToken}` 
  });
  return charge;
}
```

> [!IMPORTANT]
> Webhooks can arrive out of order or multiple times. Design database webhook operations to be idempotent, and record gateway transaction IDs to prevent duplicate status changes.

---

## 46. Event Loop Deep Dive

🔗 **Full Lesson:** [46_Event_Loop_Deep_Dive.md](./46_Event_Loop_Deep_Dive.md)

* **What**: A comprehensive analysis of the six asynchronous execution phases of the Libuv Event Loop and microtask execution boundaries in Node.js.
* **Why It Exists**: Not understanding the Event Loop phases can lead to bugs, frozen servers, or race conditions. Knowing its inner workings helps you write high-performance, concurrent applications.
* **Key Concepts**:
  * **Six Loop Phases**: Libuv iterates through distinct phases in a Tick: Timers (setTimeout/setInterval), Pending (deferred system errors), Idle/Prepare (internals), Poll (fetch I/O events, block if idle), Check (setImmediate), and Close (socket cleanup).
  * **Microtask Boundaries**: Microtasks (`process.nextTick` and resolved Promise callbacks) execute immediately after the current phase operation finishes, before moving to the next loop phase.
  * **Deterministic Scheduling**: In the global scope, `setImmediate` vs `setTimeout(..., 0)` is non-deterministic. However, within an I/O callback (Poll phase), `setImmediate` always executes first as the loop transitions directly to the Check phase.

### Key Commands / Code Example:

```javascript
const fs = require('fs');

fs.readFile(__filename, () => {
  // Executed in Poll phase: Check phase follows immediately
  setImmediate(() => {
    console.log('CHECK: setImmediate runs first inside I/O callback');
  });

  setTimeout(() => {
    console.log('TIMERS: setTimeout runs in the next loop iteration');
  }, 0);

  process.nextTick(() => {
    console.log('MICROTASK: process.nextTick executes before transition to Check phase');
  });
});
```

> [!IMPORTANT]
> Never call `process.nextTick` recursively, as it continuously fills the microtask queue, causing microtask starvation that freezes the event loop and starves I/O.

---

## 47. Streams Deep Dive

🔗 **Full Lesson:** [47_Streams_Deep_Dive.md](./47_Streams_Deep_Dive.md)

* **What**: Advanced management of Node.js stream buffers, exploring backpressure mechanics, `highWaterMark` thresholds, and custom stream class implementations.
* **Why It Exists**: If data comes in faster than the server can write it (backpressure), the memory will fill up and crash the app. Managing stream internals ensures data flows smoothly without overloading memory.
* **Key Concepts**:
  * **highWaterMark**: Defines the maximum internal buffer size before backpressure is triggered (default 16KB for standard streams, 64KB for file streams, or 16 items in objectMode).
  * **Backpressure Control**: When a writable stream's buffer fills, `.write(chunk)` returns `false`. The readable source must pause sending data until the writable destination emits the `drain` event.
  * **Custom Stream Types**: Custom streams are built by extending core classes and overriding private methods: `_read` (Readable), `_write` (Writable), or `_transform` (Transform).

### Key Commands / Code Example:

```javascript
const { Transform, pipeline } = require('stream');

// Custom transform stream that receives JS objects and outputs formatted lines
class SquareTransformStream extends Transform {
  constructor() {
    super({ writableObjectMode: true, readableObjectMode: false });
  }
  _transform(chunk, encoding, callback) {
    const squared = chunk * chunk;
    this.push(`Number: ${chunk} | Squared: ${squared}\n`);
    callback(); // Signals processing completion for the chunk
  }
}

// pipeline handles errors and automatically triggers stream cleanup
pipeline(sourceStream, new SquareTransformStream(), destStream, (err) => {
  if (err) console.error('Pipeline failed:', err.message);
});
```

> [!IMPORTANT]
> Always use `stream.pipeline` instead of raw `.pipe()` to stitch streams in production. `pipeline` correctly propagates errors and automatically destroys all intermediate streams if a failure occurs, preventing resource leaks.

---

## 48. Worker Threads

🔗 **Full Lesson:** [48_Worker_Threads.md](./48_Worker_Threads.md)

* **What**: Node's built-in multithreading module (`worker_threads`) that allows executing heavy CPU computations in parallel threads with isolated V8 instances.
* **Why It Exists**: Running heavy tasks (like image resizing or hashing passwords) on the main thread freezes the entire server. Worker threads let you run these heavy tasks in the background on other CPU cores.
* **Key Concepts**:
  * **V8 Heap Isolation**: Each worker thread runs its own isolated V8 engine instance (private heap and call stack), bypassing single-threaded runtime CPU limits.
  * **Shared Memory Space**: Workers can share memory zones directly using `SharedArrayBuffer` structures, bypassing serialization delays over Inter-Process Communication (IPC).
  * **Atomics Operations**: Because shared memory is vulnerable to race conditions, the `Atomics` object provides non-interruptible memory-access APIs (like `Atomics.add` or `Atomics.wait`) to prevent data corruption.

### Key Commands / Code Example:

```javascript
const { Worker, isMainThread, parentPort, workerData } = require('worker_threads');

if (isMainThread) {
  // Main thread: Spawn worker with parameters
  const worker = new Worker(__filename, { workerData: 40 });
  worker.on('message', (msg) => console.log('Result from worker:', msg.result));
} else {
  // Worker context: Perform CPU task and send results back
  const result = (function fib(n) { return n < 2 ? n : fib(n - 1) + fib(n - 2) })(workerData);
  parentPort.postMessage({ result });
  process.exit(0);
}
```

> [!WARNING]
> Spawning a worker thread introduces significant process allocation overhead (10-20ms). Never spawn workers on demand for single requests; deploy a worker thread pool (like Piscina) to keep active worker instances warm.

---

## 49. Cluster Module

🔗 **Full Lesson:** [49_Cluster_Module.md](./49_Cluster_Module.md)

* **What**: Node's built-in core module (`cluster`) that replicates the main process across all logical CPU cores to share incoming TCP socket connections.
* **Why It Exists**: By default, Node.js only uses one CPU core. The Cluster module lets you spin up copies of your server to run on all available CPU cores, sharing the network traffic to handle heavy workloads.
* **Key Concepts**:
  * **Master-Worker Orchestration**: The Primary (Master) process binds to the port, spawns workers, and routes incoming TCP connections, while Worker processes execute the application code.
  * **Routing Modes**: In Round-Robin mode (Linux default), the Primary accepts connections and hands them off to idle workers. In Shared Socket mode (Windows default), workers compete to accept connections directly, which can lead to load imbalance.
  * **Graceful Recovery**: The primary process can monitor worker exit events and immediately execute `cluster.fork()` to spin up replacements, ensuring high availability.

### Key Commands / Code Example:

```javascript
const cluster = require('cluster');
const http = require('http');
const numCPUs = require('os').cpus().length;

if (cluster.isPrimary) {
  // Primary process forks workers matching CPU core capacity
  for (let i = 0; i < numCPUs; i++) cluster.fork();

  cluster.on('exit', (worker) => {
    console.warn(`Worker ${worker.process.pid} died. Forking replacement...`);
    cluster.fork();
  });
} else {
  // Worker process creates HTTP server sharing port 3000
  http.createServer((req, res) => {
    res.writeHead(200);
    res.end(`Handled by worker process ${process.pid}`);
  }).listen(3000);
}
```

> [!IMPORTANT]
> Clustered worker processes are isolated and must be stateless. Never store session cookies or caching data in-memory inside workers; offload states to a shared database or Redis cache layer.

---

## 50. Child Processes

🔗 **Full Lesson:** [50_Child_Processes.md](./50_Child_Processes.md)

* **What**: Node's built-in core module (`child_process`) used to spawn, execute, and communicate with external system processes and command line binaries.
* **Why It Exists**: Allows Node.js to run system commands, execute shell scripts, or run code written in other languages (like Python or C++) as separate processes without freezing the server.
* **Key Concepts**:
  * **Process Execution Methods**: `exec` runs commands in a shell and buffers output. `execFile` executes binaries directly without shell overhead. `spawn` spawns processes and streams output. `fork` runs Node.js modules with a built-in IPC channel.
  * **Buffer Limits**: `exec` and `execFile` buffer the entire stdout/stderr payload with a default limit of 1MB. Exceeding this limit immediately terminates the child process with a `maxBuffer exceeded` error.
  * **Command Injection Vulnerability**: Using shell-spawning methods like `exec` with unvalidated user input allows attackers to append shell control operators and run unauthorized terminal commands.

### Key Commands / Code Example:

```javascript
const { spawn, fork } = require('child_process');

// 1. spawn: Streaming output safely
const child = spawn('ping', ['-n', '3', '127.0.0.1']);
child.stdout.on('data', (data) => console.log(`Output: ${data.toString()}`));

// 2. fork: Isolated Node process with IPC channel
const nodeChild = fork('task-worker.js');
nodeChild.send({ cmd: 'start' });
nodeChild.on('message', (msg) => console.log('Response from child:', msg));
```

> [!IMPORTANT]
> To defend against Command Injection, avoid `exec` when working with user inputs. Prefer `spawn` or `execFile`, which execute binaries directly and process inputs as an array of arguments, neutralizing shell operators.

---

## 51. Memory Management

🔗 **Full Lesson:** [51_Memory_Management.md](./51_Memory_Management.md)

* **What**: The memory management model inside the V8 engine, tracking call stack allocations, heap memory profiles, and identifying memory leaks.
* **Why It Exists**: Unlike frontend scripts, a backend server runs forever. Developers must monitor memory usage to prevent memory leaks, which slowly eat up the system's RAM and crash the server.
* **Key Concepts**:
  * **Stack vs Heap**: The Stack stores fast, local primitive values and function execution stack frames. The Heap stores complex references (objects, arrays, and closures) and is managed by the Garbage Collector.
  * **Memory Metrics**: `process.memoryUsage()` tracks heapTotal (allocated V8 heap), heapUsed (active JS objects), and rss (Resident Set Size: total physical memory used by the process).
  * **Retention Leaks**: Occur when references to short-lived variables are retained by long-lived global objects (such as unevicted caches, forgotten event listeners, or uncleared intervals), preventing garbage collection.

### Key Commands / Code Example:

```javascript
const express = require('express');
const app = express();

const unboundedCache = {};

app.get('/api/search', (req, res) => {
  const query = req.query.q || 'default';
  const heavyData = new Array(1000000).fill('PayloadData');

  // DANGER: Global cache has no size limit or eviction policy (Memory Leak)
  unboundedCache[query] = heavyData; 
  
  const usage = process.memoryUsage();
  console.log(`Heap Used: ${(usage.heapUsed / 1024 / 1024).toFixed(2)} MB`);
  res.json({ success: true });
});
```

> [!IMPORTANT]
> Never use plain JavaScript objects as unbounded caches in production. Always configure caching libraries with size constraints and TTL eviction policies, such as `lru-cache`.

---

## 52. Garbage Collection

🔗 **Full Lesson:** [52_Garbage_Collection.md](./52_Garbage_Collection.md)

* **What**: The automated memory reclamation algorithms inside the V8 engine, focusing on scavenger minor GC cycles and mark-sweep-compact major GC cycles.
* **Why It Exists**: Creating too many temporary objects forces JavaScript's garbage collector to run constantly. This freezes the server thread and slows down API responses, so writing clean memory code is critical.
* **Key Concepts**:
  * **Generational Heap**: Based on the hypothesis that most objects die young, the heap is split into the New Space (young, short-lived objects) and the Old Space (long-lived objects promoted from New Space).
  * **Minor GC (Scavenger)**: Manages New Space using Cheney's copying algorithm, dividing it into From-Space and To-Space. Reachable objects are copied to To-Space and compacted, then spaces are flipped. It runs in 1-5ms.
  * **Major GC (Mark-Sweep-Compact)**: Manages Old Space. It marks reachable objects, sweeps dead objects into a free list, and compacts memory. It can cause Stop-The-World pauses of 50-500ms.

### Key Commands / Code Example:

```bash
# 1. Trace all Garbage Collection activities in console
node --trace-gc server.js

# 2. Limit maximum heap space size of Old Space (e.g. to 400MB)
# Critical for container deployments (prevent OOM-killer crashes)
node --max-old-space-size=400 server.js
```
```javascript
// 3. Programmatically observe GC events using performance hooks
const { PerformanceObserver } = require('perf_hooks');
const obs = new PerformanceObserver((list) => {
  const entry = list.getEntries()[0];
  console.log(`[GC] Kind: ${entry.detail.kind} | Duration: ${entry.duration.toFixed(2)}ms`);
});
obs.observe({ entryTypes: ['gc'] });
```

> [!IMPORTANT]
> Always set the `--max-old-space-size` flag in containerized environments (like Docker on Kubernetes) to match the container's memory limit. If V8 heap allocations exceed the container limit, the OS kernel will kill the container.

---

## 53. Performance Optimization

🔗 **Full Lesson:** [53_Performance_Optimization.md](./53_Performance_Optimization.md)

* **What**: The systematic process of diagnosing, profiling, and optimizing Node.js backend speed, covering serialization latency and database query paths.
* **Why It Exists**: Finding and fixing slow operations (like bad database queries or slow calculations) is essential to keep web pages fast and lower hosting costs when traffic spikes.
* **Key Concepts**:
  * **Benchmark-Profile-Optimize**: The required workflow for optimization. Never guess; measure the baseline, profile execution metrics, refactor the bottleneck, and run load tests to verify.
  * **JSON Serialization Latency**: Native `JSON.stringify` runs synchronously and inspects objects dynamically, which is slow for large arrays. Compiled schema serializations perform up to 2x faster.
  * **Diagnostic Tools**: Clinic.js provides Doctor (diagnoses bottlenecks), Flame (generates execution flamegraphs), and Bubbleprof (tracks async latency).

### Key Commands / Code Example:

```javascript
const fastJson = require('fast-json-stringify');

// Compile serialization function ahead of time based on a JSON Schema
const stringifyProduct = fastJson({
  type: 'object',
  properties: {
    id: { type: 'integer' },
    name: { type: 'string' },
    price: { type: 'number' }
  }
});

const jsonString = stringifyProduct({ id: 101, name: 'Tablet', price: 299.99 });
```
```bash
# Benchmark application endpoints with 100 concurrent connections for 10 seconds
autocannon -c 100 -d 10 http://localhost:3000/api/products
```

> [!IMPORTANT]
> To optimize database query performance, always check slow queries using `.explain('executionStats')`. Create indexes for query filter fields to eliminate collection scans (`COLLSCAN`).

---

## 54. Node.js Internals

🔗 **Full Lesson:** [54_NodeJS_Internals.md](./54_NodeJS_Internals.md)

* **What**: The internal architecture of Node.js, detailing the C++ wrappers, V8 engine layer, and Libuv thread pool size configurations.
* **Why It Exists**: Knowing how Node.js is built internally (its C++ foundation and background thread pool) helps developers debug low-level issues, tune configurations, and optimize system speed.
* **Key Concepts**:
  * **Architectural Layers**: Built using the JS Core Library (API surface), C++ Bindings (glue layer linking JS to C++), V8 Engine (JS compilation), and Libuv (Event Loop and thread pool).
  * **Libuv Thread Pool**: Handles blocking operations (FS access, DNS lookups, crypto) using an internal thread pool. The default size is 4, which can cause starvation when running concurrent blocking tasks.
  * **Environment Configuration**: The thread pool size must be adjusted by setting the `UV_THREADPOOL_SIZE` environment variable at the system level before Node.js starts initializing.

### Key Commands / Code Example:

```bash
# Windows: Set thread pool size before launching Node
set UV_THREADPOOL_SIZE=16 && node server.js

# POSIX: Set thread pool size inline on startup
UV_THREADPOOL_SIZE=16 node server.js
```
```javascript
// Test PBKDF2 cryptography tasks that are offloaded to Libuv thread pool
const crypto = require('crypto');
const start = Date.now();

for (let i = 0; i < 8; i++) {
  crypto.pbkdf2('pass', 'salt', 100000, 64, 'sha512', () => {
    console.log(`Task completed in ${Date.now() - start}ms`);
  });
}
```

> [!IMPORTANT]
> Do not attempt to modify `process.env.UV_THREADPOOL_SIZE` inside your JavaScript code. Libuv initializes the thread pool during the runtime bootstrap phase before your script compiles, so changes made in JS are ignored.

---

## 55. Security Fundamentals

🔗 **Full Lesson:** [55_Security_Fundamentals.md](./55_Security_Fundamentals.md)

* **What**: The foundational principles of backend application security, centering on minimal privileges, payload constraints, and network timeouts.
* **Why It Exists**: Servers are constant targets for hackers. Understanding security basics—like hiding passwords, limiting permissions, and setting timeouts—protects your server from database leaks and attacks.
* **Key Concepts**:
  * **Principle of Least Privilege**: A process must run with the lowest permissions necessary. Never run Node.js applications as the system root user, as a compromise would yield full host control.
  * **Payload Size Constraints**: Restricting request sizes on body parsers limits memory usage and prevents Denial of Service (DoS) attacks from large payloads.
  * **Timeout Settings**: Setting connection timeouts on HTTP socket handles protects servers against Slowloris attacks that exhaust available sockets.

### Key Commands / Code Example:

```javascript
const express = require('express');
const http = require('http');
const app = express();

// 1. Enforce payload size limit (Max 10KB)
app.use(express.json({ limit: '10kb' }));

const server = http.createServer(app);

// 2. Configure HTTP socket timeouts to defend against Slowloris
server.headersTimeout = 5000;   // Timeout parsing headers (5s)
server.requestTimeout = 10000;  // Timeout parsing full request (10s)
server.keepAliveTimeout = 5000; // Timeout keeping idle socket open (5s)

server.listen(3000);
```

> [!IMPORTANT]
> Never hardcode API keys or credentials in your repository files. Inject them into environment variables at runtime, and scan your codebase using tools like GitGuardian or Trufflehog to detect credential leaks.

---

## 56. OWASP Top Risks

🔗 **Full Lesson:** [56_OWASP_Top_Risks.md](./56_OWASP_Top_Risks.md)

* **What**: The primary security flaws identified by the OWASP foundation, focusing on Broken Access Control, NoSQL Injection, and Information Leakage in Node.js.
* **Why It Exists**: Secure programming requires knowing how common web vulnerabilities (like injection attacks or access bypasses) work in Node.js, so you can write code that defends against them.
* **Key Concepts**:
  * **Broken Access Control**: Occurs when APIs return records without verifying user ownership (Insecure Direct Object References - IDOR). Mitigation requires validating resource access rights in every controller.
  * **NoSQL Injection**: Occurs when MongoDB queries accept unvalidated object values (e.g. `{ "$ne": "" }`), permitting attackers to bypass database password checks.
  * **Information Leakage**: Exposing database connection strings or detailed execution stack traces in production HTTP responses leaks system details to attackers.

### Key Commands / Code Example:

```javascript
const express = require('express');
const app = express();

// Secure login query: Cast parameter values to string explicitly
app.post('/api/login', (req, res) => {
  const username = String(req.body.username);
  const password = String(req.body.password);

  // MongoDB query is safe because operators like $ne are parsed as literal strings
  db.collection('users').findOne({ username, password }, (err, user) => {
    res.json({ success: !!user });
  });
});
```

> [!IMPORTANT]
> Never return raw error objects (`err.stack`) to clients in production environments. Implement a global error handler that logs the stack trace internally and returns generic error messages to the client.

---

## 57. Helmet

🔗 **Full Lesson:** [57_Helmet.md](./57_Helmet.md)

* **What**: A collection of security middleware libraries for Express that sets standard HTTP response headers to block browser-based attacks.
* **Why It Exists**: Express servers broadcast system details (like headers) that help hackers find exploits. Helmet secures these headers to protect your app from common browser-based attacks.
* **Key Concepts**:
  * **Content Security Policy (CSP)**: Restricts resource source URLs (scripts, images, CSS) to prevent execution of unauthorized scripts and inline XSS payloads.
  * **Clickjacking Defense**: Sets `X-Frame-Options` to `DENY` or `SAMEORIGIN` to block browsers from embedding your pages inside malicious `<iframe>` wrappers.
  * **MIME Sniffing Prevention**: Sets `X-Content-Type-Options: nosniff`, forcing browsers to strictly adhere to the declared MIME type rather than parsing file content (defends against script uploads disguised as images).

### Key Commands / Code Example:

```javascript
const express = require('express');
const helmet = require('helmet');
const app = express();

// 1. Basic Integration (sets 15 secure headers and strips X-Powered-By)
app.use(helmet());

// 2. Custom Content Security Policy
app.use(
  helmet.contentSecurityPolicy({
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'", 'https://apis.google.com'], // Allow trusted CDNs
      objectSrc: ["'none'"], // Disable plugins like Flash
      upgradeInsecureRequests: [] // Force HTTPS
    }
  })
);
```

> [!IMPORTANT]
> Load `helmet` middleware at the very top of your middleware chain before any static asset folders or routes to ensure all API responses are protected.

---

## 58. CORS

🔗 **Full Lesson:** [58_CORS.md](./58_CORS.md)

* **What**: Cross-Origin Resource Sharing, a browser-enforced security protocol that regulates cross-origin API calls using preflight checks and whitelist headers.
* **Why It Exists**: Web browsers block frontends from accessing APIs on different domains for safety. CORS headers allow you to safely white-list and permit your frontend app to query your backend server.
* **Key Concepts**:
  * **Preflight OPTIONS Requests**: For write verbs (PUT, DELETE) or custom authorization headers, browsers emit a preflight `OPTIONS` query to verify CORS permissions before sending the actual request.
  * **Same-Origin Definition**: Same-origin requires matching protocols, domain names, and port configurations. Any variation triggers CORS validation.
  * **Credential Constraints**: When cross-origin API calls require authentication cookies (`credentials: true`), the wildcard origin `*` is forbidden. The server must return explicit origin whitelist match headers.

### Key Commands / Code Example:

```javascript
const express = require('express');
const cors = require('cors');
const app = express();

const whitelist = ['https://my-app.com', 'http://localhost:3000'];

const corsOptions = {
  origin: (origin, callback) => {
    if (!origin || whitelist.includes(origin)) {
      callback(null, true);
    } else {
      callback(new Error('Blocked by CORS policy'));
    }
  },
  credentials: true, // Permit cookies to be sent across origins
  optionsSuccessStatus: 200 // Return 200 OK for OPTIONS preflights
};

app.use(cors(corsOptions));
```

> [!IMPORTANT]
> Setting `origin: '*'` alongside `credentials: true` in production is a severe security risk. Set up a dynamic whitelist array to validate origins and authorize only secure client interfaces.

---

## 59. CSRF

🔗 **Full Lesson:** [59_CSRF.md](./59_CSRF.md)

* **What**: Cross-Site Request Forgery, an attack vector that exploits cookie authentication flags to submit unauthorized transactions, mitigated by SameSite flags and tokens.
* **Why It Exists**: Browsers automatically send login cookies with web requests. Hackers can exploit this by tricks that submit requests to your server from malicious sites using a logged-in user's credentials.
* **Key Concepts**:
  * **Cross-Site Request Forgery**: Exploits cookie auto-attachment by sending requests (e.g. password resets or bank transfers) from malicious domains on behalf of authenticated users.
  * **SameSite Cookie Flags**: Setting `sameSite: 'lax'` or `sameSite: 'strict'` tells browsers to withhold session cookies on cross-origin subrequests, blocking CSRF at the browser level.
  * **Synchronizer Token Pattern**: The server issues a random token, which is stored in a cookie. For state-changing requests, the client must return this token in a custom header (e.g. `X-CSRF-Token`). The server compares the two values.

### Key Commands / Code Example:

```javascript
const crypto = require('crypto');

// Custom stateless Double-Submit Cookie CSRF Middleware
const csrfProtection = (req, res, next) => {
  if (['GET', 'HEAD', 'OPTIONS'].includes(req.method)) {
    // Generate token and save in client-accessible cookie on safe reads
    if (!req.cookies['csrf-token']) {
      const token = crypto.randomBytes(32).toString('hex');
      res.cookie('csrf-token', token, { sameSite: 'lax' });
    }
    return next();
  }

  // Validate state-changing operations
  const cookieToken = req.cookies['csrf-token'];
  const requestToken = req.headers['x-csrf-token'];

  if (!cookieToken || !requestToken || cookieToken !== requestToken) {
    return res.status(403).json({ error: 'Invalid or missing CSRF token' });
  }
  next();
};
```

> [!IMPORTANT]
> Never use GET requests to execute database writes or state-changing actions. CSRF middleware typically bypasses verification on GET requests, leaving those actions vulnerable.

---

## 60. XSS

🔗 **Full Lesson:** [60_XSS.md](./60_XSS.md)

* **What**: Cross-Site Scripting, an input vulnerability allowing attackers to execute scripts in client browsers, mitigated by HTML escaping, HttpOnly cookies, and CSPs.
* **Why It Exists**: Failing to clean user input allows hackers to inject malicious JavaScript code that runs inside other users' browsers to steal data or hijack sessions.
* **Key Concepts**:
  * **HTML Escaping**: Translates characters into entities (e.g., `<` to `&lt;`, `>` to `&gt;`) to render inputs as literal strings, neutralizing execution.
  * **HttpOnly Cookies**: Setting the `HttpOnly` flag on cookies blocks client-side JavaScript access (`document.cookie`), protecting session tokens from XSS theft.
  * **Content Security Policy**: Enables defining strict script source whitelists and blocking inline scripts to prevent injected script execution.

### Key Commands / Code Example:

```javascript
const express = require('express');
const xss = require('xss'); // Sanitization library
const app = express();

app.use(express.json());

// Middleware to recursively sanitize request inputs
const sanitizeBody = (req, res, next) => {
  const clean = (data) => {
    if (typeof data === 'string') return xss(data);
    if (typeof data === 'object' && data !== null) {
      for (const k in data) data[k] = clean(data[k]);
    }
    return data;
  };
  if (req.body) req.body = clean(req.body);
  next();
};

app.use(sanitizeBody);
```

> [!IMPORTANT]
> The `HttpOnly` flag protects session cookies from script access but does not fix the XSS vulnerability. Attackers can still run scripts in the browser to hijack the active session. Always combine `HttpOnly` with strict HTML escaping and CSP headers.

---

## 61. SQL Injection

🔗 **Full Lesson:** [61_SQL_Injection.md](./61_SQL_Injection.md)

* **What**: A database vulnerability where malicious SQL commands are executed by concatenating unvalidated inputs into SQL query strings.
* **Why It Exists**: Constructing SQL queries by joining strings directly lets attackers append their own SQL commands, which can compromise, delete, or steal the entire database.
* **Key Concepts**:
  * **String Concatenation**: The root cause of SQL injection. Combining variables directly inside SQL statements (e.g. `'SELECT * FROM users WHERE name = ' + input`) runs user input as executable database queries.
  * **Parameterized Queries**: A secure pattern where variables are sent as arguments separately from the SQL statement. The database engine treats them strictly as data, neutralizing any commands.
  * **Automated Scanners**: Tools (such as `sqlmap`) automate scanning input fields to identify and exploit SQL injection entry points.

### Key Commands / Code Example:

```javascript
const { Client } = require('pg');
const client = new Client();

// SECURE: Parameterized query using placeholders
async function getProfile(userId) {
  const query = 'SELECT id, username, email FROM users WHERE id = $1';
  const values = [userId]; // userId is treated strictly as data value
  const res = await client.query(query, values);
  return res.rows[0];
}
```

> [!IMPORTANT]
> Never construct SQL statements by joining strings. Always use parameterized inputs, or rely on ORMs that parameterize queries automatically.

---

## 62. NoSQL Injection

🔗 **Full Lesson:** [62_NoSQL_Injection.md](./62_NoSQL_Injection.md)

* **What**: A NoSQL database vulnerability where attackers inject MongoDB query operators (like `$gt` or `$ne`) inside JSON inputs to bypass logical checks.
* **Why It Exists**: Unlike SQL databases, NoSQL databases accept JSON objects as queries. If user inputs are passed directly into database query objects without sanitization, attackers can inject query operators to bypass authentication checks.
* **Key Concepts**:
  * **Operator Injection**: Injecting query properties (like `{ "$gt": "" }` or `{ "$ne": null }`) inside parameters to change the query's behavior.
  * **Type Sanitization**: Enforcing type validation on input variables (casting inputs to strings) to prevent objects from being parsed as query commands.
  * **Mongoose Schema Security**: Using strict ODM schemas to automatically ignore undeclared query keys and cast inputs to defined types.

### Key Commands / Code Example:

```javascript
const express = require('express');
const app = express();
app.use(express.json());

// SECURE: Enforce type conversion using standard casts
app.post('/api/auth', (req, res) => {
  const cleanUsername = String(req.body.username);
  const cleanPassword = String(req.body.password);

  // Database checks are safe because inputs are forced to literal strings
  db.collection('users').findOne({ 
    username: cleanUsername, 
    password: cleanPassword 
  }, (err, user) => {
    res.json({ success: !!user });
  });
});
```

> [!IMPORTANT]
> Express's built-in `express.json()` middleware parses objects. If a client sends `{"password": {"$ne": ""}}`, Express passes a query object to MongoDB. Always validate that inputs are strings, not objects, before querying.

---

## 63. Testing Fundamentals

🔗 **Full Lesson:** [63_Testing_Fundamentals.md](./63_Testing_Fundamentals.md)

* **What**: The methodology and practice of verifying backend application correctness, using test runners, assertion suites, and coverage reports.
* **Why It Exists**: Automated testing catches bugs early before they reach production. It acts as a safety net that lets you refactor code confidently without breaking existing features.
* **Key Concepts**:
  * **Test Pyramids**: Aligning test suites: Unit Tests (cheap, fast, mocks dependencies), Integration Tests (checks database/router integrations), and End-to-End Tests (verifies user flows).
  * **Code Coverage**: Metrics tracking test coverage across statements, branches, functions, and lines. Aim for 80%+ coverage on critical business logic.
  * **TDD Workflow**: Test-Driven Development loops: write a failing test first (Red), implement code to pass it (Green), and clean up the structure (Refactor).

### Key Commands / Code Example:

```bash
# Run tests and collect coverage metrics
jest --coverage

# Run tests in file-watching mode during active development
jest --watch
```

> [!IMPORTANT]
> Code coverage is only a diagnostic metric. Reaching 100% coverage does not mean the code is free of bugs; tests must evaluate logical edge cases and invalid inputs to be effective.

---

## 64. Unit Testing

🔗 **Full Lesson:** [64_Unit_Testing.md](./64_Unit_Testing.md)

* **What**: Testing isolated units of code (like individual functions or classes) in isolation by mocking external network and database dependencies.
* **Why It Exists**: Speeds up verification by isolating functions from external systems (like databases). If a test fails, you know the issue is in that specific function.
* **Key Concepts**:
  * **Isolation Design**: Mocking external services, network sockets, or filesystem calls to ensure tests evaluate only the target function logic.
  * **Test Doubles**: Using Stubs (returns mock outputs), Spies (tracks function execution variables), and Mocks (validates behavior interactions).
  * **Fast Execution**: Because unit tests run entirely in local memory without I/O calls, thousands of tests can run in under 5 seconds.

### Key Commands / Code Example:

```javascript
// calculator.js
const add = (a, b) => a + b;

// calculator.test.js
test('adds 2 + 3 to equal 5', () => {
  expect(add(2, 3)).toBe(5);
});
```

> [!NOTE]
> Keep unit tests completely free of I/O. Never connect to a live database or send network requests during unit tests; mock those operations instead.

---

## 65. Integration Testing

🔗 **Full Lesson:** [65_Integration_Testing.md](./65_Integration_Testing.md)

* **What**: Testing the interaction between multiple components or systems (like routing middleware, database drivers, and external APIs) together.
* **Why It Exists**: Unit tests mock database layers, which can hide integration bugs. Integration testing verifies that database clients, routing files, and logic modules work together correctly.
* **Key Concepts**:
  * **Boundary Testing**: Verifying interactions between API routing files, database drivers, and third-party integrations.
  * **Test Databases**: Spinning up isolated local databases (e.g. via Docker containers) to verify query logic against real database tables.
  * **State Lifecycle**: Resetting database tables and migrations before and after test suites run to prevent tests from leaking state to each other.

### Key Commands / Code Example:

```javascript
const request = require('supertest');
const app = require('../app');
const db = require('../db');

beforeAll(async () => await db.migrate());
afterAll(async () => await db.close());

test('POST /api/users creates a record in the database', async () => {
  const res = await request(app)
    .post('/api/users')
    .send({ email: 'test@mail.com', password: 'password123' });
    
  expect(res.status).toBe(201);
  expect(res.body.email).toBe('test@mail.com');
  
  // Query database directly to verify database write success
  const user = await db.findUserByEmail('test@mail.com');
  expect(user).toBeDefined();
});
```

> [!IMPORTANT]
> Never run integration tests against a live production database. Always target a dedicated local or containerized test database to prevent data deletion or contamination.

---

## 66. Jest

🔗 **Full Lesson:** [66_Jest.md](./66_Jest.md)

* **What**: A popular, feature-rich JavaScript testing framework that provides test runners, assertion APIs, mock setups, and coverage analytics.
* **Why It Exists**: Provides an all-in-one testing suite that handles test execution, assertions, mocking, and coverage reports, eliminating the need to combine multiple testing tools.
* **Key Concepts**:
  * **Zero Config Setup**: Works out of the box with built-in runners, mock wrappers, and assertions, reducing setup boilerplate.
  * **Snapshots**: Saves serialized copies of UI components or API responses to quickly identify unexpected changes in output format.
  * **Mock APIs**: Providing assertion mocks (such as `jest.fn()` or `jest.spyOn()`) to intercept imports and simulate dependencies.

### Key Commands / Code Example:

```javascript
// userService.test.js
const userService = require('./userService');
const db = require('./db');

// Mock the database dependency module
jest.mock('./db');

test('should return user profile from DB', async () => {
  const mockUser = { id: 1, name: 'Alice' };
  db.getUserById.mockResolvedValue(mockUser); // Configure mock behavior

  const user = await userService.fetchProfile(1);
  expect(user).toEqual(mockUser);
  expect(db.getUserById).toHaveBeenCalledWith(1); // Verify interaction
});
```

> [!NOTE]
> Clear mock states between tests using `jest.clearAllMocks()` or configure `clearMocks: true` in your Jest config to prevent mock call counters from leaking across tests.

---

## 67. Supertest

🔗 **Full Lesson:** [67_Supertest.md](./67_Supertest.md)

* **What**: An HTTP assertion library used in Node.js to test API endpoints by executing mock requests against Express applications without binding to network ports.
* **Why It Exists**: Allows you to test your Express API endpoints (routes, middleware, headers) in local memory, avoiding the need to spin up a live network server for testing.
* **Key Concepts**:
  * **In-Memory Testing**: Instantiates Express app handlers and executes mock requests directly inside Node's memory space, bypassing TCP handshake overhead.
  * **Declarative Assertions**: Chaining assertions directly (e.g. `.expect('Content-Type', /json/)` or `.expect(200)`) to verify routes and outputs.
  * **Status & Header Checks**: Easily tests middleware configurations by verifying status codes, cookies, and CORS headers.

### Key Commands / Code Example:

```javascript
const request = require('supertest');
const express = require('express');

const app = express();
app.get('/health', (req, res) => res.status(200).json({ status: 'OK' }));

test('GET /health returns JSON with status 200', async () => {
  await request(app)
    .get('/health')
    .expect('Content-Type', /json/) // Validate headers
    .expect(200) // Validate status code
    .then(response => {
      expect(response.body.status).toBe('OK'); // Validate body
    });
});
```

> [!IMPORTANT]
> When testing Express apps with Supertest, export the raw `app` instance from your app file instead of calling `app.listen(port)`. Supertest handles starting the server internally on ephemeral ports.

---

## 68. Swagger/OpenAPI

🔗 **Full Lesson:** [68_Swagger_OpenAPI.md](./68_Swagger_OpenAPI.md)

* **What**: A standard API design specification language used to describe, document, and visualize RESTful APIs using YAML or JSON configurations.
* **Why It Exists**: Standardizes how APIs are documented. It generates interactive documentation pages automatically, making it easy for frontend teams to understand and test API routes.
* **Key Concepts**:
  * **Interactive API Docs**: Generates web-based interfaces (Swagger UI) where developers can view parameters and test endpoints directly from the browser.
  * **Single Source of Truth**: Serves as the single reference for API endpoints, preventing documentation drift when backend code changes.
  * **Documentation Approaches**: Code-first (writing spec comments inside route files) vs. Design-first (defining YAML configuration files first and generating routes from it).

### Key Commands / Code Example:

```javascript
const express = require('express');
const swaggerUi = require('swagger-ui-express');
const YAML = require('yamljs');

const app = express();
// Load OpenAPI specification file
const swaggerDocument = YAML.load('./openapi.yaml');

// Serve interactive documentation on endpoint /api-docs
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDocument));
```

> [!NOTE]
> In large projects, choose a Design-First workflow. Define the `openapi.yaml` specification first, then use validation middleware (like `express-openapi-validator`) to automatically reject requests that do not match the API spec.

---

## 69. Microservices

🔗 **Full Lesson:** [69_Microservices.md](./69_Microservices.md)

* **What**: An architectural style where a single large application is split into a collection of small, independent, and stateless services.
* **Why It Exists**: Breaks down a complex system into independent, focused services. This allows individual teams to build, deploy, and scale specific components without affecting the rest of the application.
* **Key Concepts**:
  * **Domain-Driven Isolation**: Services manage their own boundaries and databases. A service must never write directly to another service's database tables.
  * **Service Boundaries**: Decoupling components so that a crash in one microservice (like the recommendation engine) does not bring down the main user service.
  * **Network Communication**: Services communicate via synchronous protocols (HTTP/gRPC) or asynchronous messaging (message brokers).

### Key Commands / Code Example:

```text
Monolithic Design:
[ Client ] ──> [ Unified API Instance (Auth, Products, Billing) ] ──> [ Shared DB ]

Microservice Design:
               ┌──> [ Auth Service ] ──────> [ Auth DB ]
[ Client ] ──> ├──> [ Product Service ] ───> [ Product DB ]
               └──> [ Billing Service ] ───> [ Billing DB ]
```

> [!WARNING]
> Microservices introduce network latency and distributed data issues. Do not adopt microservices prematurely; start with a modular monolith and split services out only when team size or scaling limits require it.

---

## 70. Event-Driven Architecture

🔗 **Full Lesson:** [70_Event_Driven_Architecture.md](./70_Event_Driven_Architecture.md)

* **What**: An architectural design pattern where decoupled services communicate and sync state asynchronously by emitting and consuming events.
* **Why It Exists**: Improves system resilience and performance. Instead of waiting for slow synchronous APIs, services publish events to a message queue and continue their work immediately.
* **Key Concepts**:
  * **Asynchronous Decoupling**: Services run independently. The publisher service emits events without knowing which consumer services will process them.
  * **Event Broker Envelopes**: Structuring events with unified metadata: unique event ID, event type (e.g. `order.created`), creation timestamp, and data payload.
  * **Eventual Consistency**: State modifications propagate across services via events. Data is not synchronized instantly, but eventually matches across the system.

### Key Commands / Code Example:

```javascript
// Generic event envelope design
const orderCreatedEvent = {
  metadata: {
    eventId: "evt_7834a9b2",
    eventType: "order.created",
    timestamp: "2026-06-27T17:23:00Z"
  },
  payload: {
    orderId: "ord_1092",
    userId: "usr_561",
    totalAmount: 149.99
  }
};
```

> [!IMPORTANT]
> Because events can fail mid-transit, design event consumers to be idempotent. Processing the same event multiple times must yield the same system state to prevent double-billing or duplicate records.

---

## 71. RabbitMQ

🔗 **Full Lesson:** [71_RabbitMQ.md](./71_RabbitMQ.md)

* **What**: An open-source message broker that facilitates async communications between services using AMQP standards, queues, and exchanges.
* **Why It Exists**: Acts as a reliable mail sorting office for services. It holds messages in secure queues until consumer services are ready to process them, helping handle spikes in traffic.
* **Key Concepts**:
  * **AMQP Routing**: Publishers send messages to Exchanges. Exchanges route them to Queues based on routing keys. Consumers poll or subscribe to Queues.
  * **Routing Topologies**: Direct (routes by exact key match), Fanout (broadcasts to all bound queues), and Topic (routes based on wildcard pattern matches).
  * **Message Durability**: Setting messages and queues to `durable` ensures they are saved to disk, preventing data loss if RabbitMQ restarts.

### Key Commands / Code Example:

```javascript
const amqp = require('amqplib');

async function publishNotification(routingKey, message) {
  const connection = await amqp.connect(process.env.RABBITMQ_URL);
  const channel = await connection.createChannel();
  
  const exchangeName = 'notification_events';
  await channel.assertExchange(exchangeName, 'topic', { durable: true });
  
  // Publish message with durability configuration
  channel.publish(
    exchangeName, 
    routingKey, 
    Buffer.from(JSON.stringify(message)),
    { persistent: true } // Persist message to disk
  );
  
  await channel.close();
  await connection.close();
}
```

> [!IMPORTANT]
> When building message consumers, set `noAck: false` and call `channel.ack(message)` only *after* the task finishes. This ensures RabbitMQ re-queues the message if the worker process crashes mid-task.

---

## 72. Kafka

🔗 **Full Lesson:** [72_Kafka.md](./72_Kafka.md)

* **What**: A high-throughput, distributed event streaming platform used to build real-time log pipelines and process data stream partitions.
* **Why It Exists**: Designed to handle massive event volumes (millions of events per second) by storing messages as an append-only commit log partitioned across servers.
* **Key Concepts**:
  * **Commit Log partitions**: Topics are split into distributed partitions. Messages are appended sequentially and preserved even after consumption.
  * **Consumer Groups**: Multiple consumers share message processing. Kafka routes each partition to a single group member to load-balance scale.
  * **Message Offsets**: Consumers track their read progress using numeric index pointers (offsets), allowing them to replay logs on recovery.

### Key Commands / Code Example:

```javascript
const { Kafka } = require('kafkajs');

const kafkaClient = new Kafka({
  clientId: 'billing-app',
  brokers: [process.env.KAFKA_BROKER_URL]
});

async function runProducer() {
  const producer = kafkaClient.producer();
  await producer.connect();
  
  // Write message payload to a partitioned topic
  await producer.send({
    topic: 'payment-events',
    messages: [
      { key: 'usr_561', value: JSON.stringify({ status: 'succeeded', amount: 99 }) }
    ]
  });
  await producer.disconnect();
}
```

> [!IMPORTANT]
> Kafka does not delete messages once consumed. Messages remain in partitions until cleanup policies (like time-based retention) remove them. This allows other services to replay past events.

---

## 73. Distributed Systems

🔗 **Full Lesson:** [73_Distributed_Systems.md](./73_Distributed_Systems.md)

* **What**: A collection of independent network nodes that communicate and coordinate actions via messages to achieve a unified system state.
* **Why It Exists**: Single-server applications eventually hit hardware scale limits. Distributed systems pool multiple machines together to handle infinite traffic and survive server crashes.
* **Key Concepts**:
  * **CAP Theorem**: A distributed system can only guarantee two out of three: Consistency (identical data reads), Availability (every read succeeds), or Partition Tolerance (survives network splits).
  * **Fallout Cascades**: One slow downstream service can consume all server sockets, triggering a domino effect that crashes the entire API gateway fleet.
  * **Distributed Sockets Control**: Implementing Circuit Breakers to fail fast and prevent crashes from spreading to healthy nodes.

### Key Commands / Code Example:

```text
CAP Theorem Options:
- CP (Consistency + Partition Tolerance): Reject requests if data consistency cannot be verified across nodes.
- AP (Availability + Partition Tolerance): Accept requests and return local data immediately, allowing temporary data drifts.
```

> [!IMPORTANT]
> In distributed microservices, network partitions are inevitable. Build services with an AP-first model (Availability + Partition Tolerance) using eventual consistency to ensure your APIs remain responsive during network drops.

---

## 74. Scaling Node.js

🔗 **Full Lesson:** [74_Scaling_NodeJS.md](./74_Scaling_NodeJS.md)

* **What**: The design methods of scaling Node.js applications horizontally and vertically using clusters, caches, and load-balancer routers.
* **Why It Exists**: Prevents servers from overloading. It details the two scaling paths: upgrading server hardware (vertical) or adding more server instances behind a load balancer (horizontal).
* **Key Concepts**:
  * **Vertical Scaling**: Upgrading single-server hardware (CPU cores, RAM) and using the Node `cluster` module to utilize all system resources.
  * **Horizontal Scaling**: Deploying multiple stateless Node.js server containers behind an Application Load Balancer (ALB) to distribute requests.
  * **Stateless Rules**: Eliminating local file storage, local sessions, and in-memory background tasks to enable server scaling and replacement.

### Key Commands / Code Example:

```text
Vertical Scaling (Scale Up):
Upgrade Server (2 Cores, 4GB RAM) ───> Upgrade Server (16 Cores, 32GB RAM)

Horizontal Scaling (Scale Out):
[ Load Balancer ] ──┬──> [ Node Server 1 ]
                    ├──> [ Node Server 2 ]
                    └──> [ Node Server 3 ] (Easily add more instances as traffic rises)
```

> [!IMPORTANT]
> Always build your backend stateless. Storing login sessions or file uploads locally on a server instance breaks load balancing, as subsequent client requests may route to other nodes.

---

## 75. Docker

🔗 **Full Lesson:** [75_Docker.md](./75_Docker.md)

* **What**: A containerization platform that packages applications and their environment dependencies into portable, isolated container images.
* **Why It Exists**: Eliminates the "works on my machine" bug by packaging Node.js, libraries, and files into a standard, isolated container that runs identically on any environment.
* **Key Concepts**:
  * **Container Isolation**: Porting applications inside isolated containers, ensuring clean runtimes independent of the host OS configuration.
  * **Docker Image Layers**: Built sequentially using directives in a `Dockerfile`. Reusing cache layers speeds up build pipeline times.
  * **Multi-Stage Builds**: Separating compile stages from runtime execution stages to exclude compilers and build dependencies, reducing the final image size.

### Key Commands / Code Example:

```dockerfile
# Multi-stage production Dockerfile for Node.js
# Stage 1: Build dependencies
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci

# Stage 2: Clean runtime environment
FROM node:20-alpine
WORKDIR /app
ENV NODE_ENV=production
COPY package*.json ./
RUN npm ci --only=production
COPY --from=builder /app/node_modules ./node_modules
COPY . .
USER node
EXPOSE 3000
CMD ["node", "server.js"]
```

> [!IMPORTANT]
> Always include a `USER node` directive in your production Dockerfiles. Running container processes as the default `root` user allows attackers to compromise the host system during a container escape.

---

## 76. Kubernetes

🔗 **Full Lesson:** [76_Kubernetes.md](./76_Kubernetes.md)

* **What**: An open-source container orchestration platform designed to automate deploying, scaling, and managing containerized applications across node clusters.
* **Why It Exists**: Managing hundreds of Docker containers manually is impossible. Kubernetes automates container deployment, scaling, healing (restarts), and networking across a cluster of servers.
* **Key Concepts**:
  * **Pods & Nodes**: A Pod is the smallest deployable unit (containing one or more containers). A Node is a physical or virtual machine running the Kubernetes node software.
  * **Service Discovery**: Exposes pod instances behind a stable virtual IP address to route traffic internally and balance connection loads.
  * **ConfigMaps & Secrets**: Injecting configuration settings and secret key variables dynamically into containers on boot, keeping credentials out of docker images.

### Key Commands / Code Example:

```yaml
# deployment.yaml configures a scalable Node.js container group
apiVersion: apps/v1
kind: Deployment
metadata:
  name: node-api-deployment
spec:
  replicas: 3 # Run 3 identical container instances
  selector:
    matchLabels:
      app: node-api
  template:
    metadata:
      labels:
        app: node-api
    spec:
      containers:
      - name: node-api
        image: myregistry.com/node-api:v1.0.0
        ports:
        - containerPort: 3000
        resources:
          limits:
            memory: "512Mi"
            cpu: "500m"
```

> [!IMPORTANT]
> Always define resource requests and limits (CPU and Memory) for your containers. Without limits, a single memory-leaking container can consume all Node RAM and freeze other services in your cluster.

---

## 77. CI/CD

🔗 **Full Lesson:** [77_CI_CD.md](./77_CI_CD.md)

* **What**: Continuous Integration and Continuous Deployment, software development pipelines designed to automate linting, testing, and building docker image containers dynamically.
* **Why It Exists**: Code manual checks and deployments lead to release bugs. CI/CD pipelines run tests automatically whenever code is pushed, and deploy updates to production without manual steps.
* **Key Concepts**:
  * **Continuous Integration (CI)**: Automatically fetching code updates, running code formatters/linters, and executing the test suites to catch bugs immediately.
  * **Continuous Delivery/Deployment (CD)**: Automatically building secure docker container images and deploying them to staging or production environments.
  * **Pipeline Isolation**: Running jobs inside clean, virtual runner containers to isolate build tasks and protect the main code repositories.

### Key Commands / Code Example:

```text
The CI/CD Automation Flow:
[ Local Code Change ] ──> [ Push to Git ] ──> [ CI Runner starts ]
                                                      │
                                                      ├──> Step 1: Run Linter / Formatter
                                                      ├──> Step 2: Run Unit & Integration Tests
                                                      ├──> Step 3: Compile Docker Image
                                                      └──> Step 4: Deploy to Kubernetes Cluster
```

> [!IMPORTANT]
> Configure your CI/CD pipelines to fail fast. Run fast code formatters and unit tests first, and execute slow integrations or container builds only when unit tests pass.

---

## 78. GitHub Actions

🔗 **Full Lesson:** [78_GitHub_Actions.md](./78_GitHub_Actions.md)

* **What**: A built-in CI/CD automation runner platform on GitHub that executes scripts, tests, and builds docker containers dynamically based on repository event triggers.
* **Why It Exists**: Integrates automation pipelines directly into your GitHub repository, running tests and deployments in response to pull requests and code merges.
* **Key Concepts**:
  * **Workflows & Jobs**: Workflows are YAML configuration files triggered by events (e.g. `push`). Jobs are collections of steps executed sequentially on runner machines.
  * **GitHub Secrets**: Environment variables encrypted and stored within GitHub settings, safely injected into runners at runtime (never committed to repository files).
  * **Action Modules**: Reusable pre-built code blocks (e.g. `actions/checkout`) that simplify setting up environments and dependencies.

### Key Commands / Code Example:

```yaml
# .github/workflows/ci.yml
name: Node.js CI
on:
  push:
    branches: [ main ]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout repository code
      uses: actions/checkout@v4
    - name: Install Node.js runtime
      uses: actions/setup-node@v4
      with:
        node-version: '20'
    - name: Clean install dependencies
      run: npm ci
    - name: Execute test suites
      run: npm test
```

> [!IMPORTANT]
> Pin action steps to explicit version tags or commit SHA hashes (e.g. `actions/checkout@v4.1.1`) to prevent third-party updates from breaking your pipeline or introducing malicious code.

---

## 79. AWS Deployment

🔗 **Full Lesson:** [79_AWS_Deployment.md](./79_AWS_Deployment.md)

* **What**: The hosting and orchestrating of Node.js applications in production using cloud solutions like ECS (Elastic Container Service) and EKS (Elastic Kubernetes Service).
* **Why It Exists**: Simplifies backend infrastructure by delegating hardware maintenance, auto-scaling, load balancing, and network routing to Amazon's cloud platforms.
* **Key Concepts**:
  * **AWS ECS / Fargate**: Runs docker containers without managing physical EC2 server nodes, eliminating server OS updates.
  * **EC2 Scaling Groups**: Automatically adjusts server instances based on metrics (like CPU or memory usage) to handle traffic spikes.
  * **AWS Secrets Manager**: A centralized service that stores database credentials and API keys securely, rotating passwords automatically.

### Key Commands / Code Example:

```text
Stateless AWS Architecture:
[ Client Request ] ──> [ ALB Load Balancer ] 
                             │
                             ├──> [ ECS Fargate Node.js Task 1 ] (Availability Zone A)
                             └──> [ ECS Fargate Node.js Task 2 ] (Availability Zone B)
                                         │
                             [ AWS Secrets Manager ] (Keys injected dynamically)
```

> [!NOTE]
> Always deploy your application containers inside AWS private subnets, exposing only your Application Load Balancer (ALB) to the public internet to protect backend resources from direct attacks.

---

## 80. Nginx

🔗 **Full Lesson:** [80_Nginx.md](./80_Nginx.md)

* **What**: A high-performance, open-source web server, load balancer, and reverse proxy designed to process massive concurrent HTTP connections.
* **Why It Exists**: Node.js can act as a web server, but it handles SSL certificates, static files, and connection limits slowly. Nginx acts as a high-speed shield in front of Node.js to manage these tasks efficiently.
* **Key Concepts**:
  * **Asynchronous Architecture**: Uses an event-driven, non-blocking architecture that allows a single worker process to handle tens of thousands of concurrent connections.
  * **Proxy Forwarding**: Accepting incoming client connections and proxying them to upstream Node.js application instances.
  * **Security Shielding**: Handling SSL/TLS termination, rate limiting, and blocking malicious requests before they reach Node.js.

### Key Commands / Code Example:

```nginx
# nginx.conf: Simple reverse proxy config
server {
    listen 80;
    server_name my-app.com;

    location / {
        proxy_pass http://localhost:3000; # Upstream Node.js application
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

> [!IMPORTANT]
> When proxying requests to Express apps, configure Nginx to forward client IP headers (`X-Real-IP`, `X-Forwarded-For`), and enable `app.set('trust proxy', 1)` in Express to ensure security checks read correct client IPs.

---

## 81. Reverse Proxy

🔗 **Full Lesson:** [81_Reverse_Proxy.md](./81_Reverse_Proxy.md)

* **What**: A proxy server sitting between client browsers and backends that accepts incoming network requests and routes them to upstream application servers.
* **Why It Exists**: Acts as a single entry point for your application. It hides your backend servers' real IP addresses and structures to protect them from direct attacks.
* **Key Concepts**:
  * **Architecture Shielding**: Client devices never connect directly to Node.js servers, hiding port configurations and server IPs.
  * **Static File Caching**: Serving static assets (CSS, JS, images) directly from Nginx disk space, keeping Node.js event loops focused on dynamic API routing.
  * **Header Injection**: Injecting security headers (CORS headers, client IPs, SSL status) before routing requests to upstream backends.

### Key Commands / Code Example:

```text
Request Path with Reverse Proxy:
[ Client Request ] ──> (Internet) ──> [ Nginx Reverse Proxy (Port 80/443) ]
                                                    │
                                                    ▼ (Internal Private Network)
                                      [ Node.js Application Server (Port 3000) ]
```

> [!NOTE]
> Configure your reverse proxy to compress responses using gzip or Brotli. This reduces network payload size and speeds up load times, saving Node.js CPU cycles.

---

## 82. Load Balancing

🔗 **Full Lesson:** [82_Load_Balancing.md](./82_Load_Balancing.md)

* **What**: The routing optimization strategy of distributing incoming client requests evenly across a pool of healthy backend application servers.
* **Why It Exists**: A single server eventually hits a limit on the number of requests it can handle. Load balancing pools multiple backend servers together to handle traffic spikes.
* **Key Concepts**:
  * **Routing Algorithms**: Distributing traffic using Round Robin (sequential routing), Least Connections (routes to idle nodes), or IP Hash (maps specific IPs to the same server).
  * **Active Health Checks**: Continually checking server health endpoints (e.g. GET `/health`). If a node crashes, the load balancer removes it and routes traffic to healthy nodes.
  * **SSL/TLS Offloading**: Performing SSL handshake encryption checks at the load balancer level, freeing Node.js servers from heavy cryptographic calculations.

### Key Commands / Code Example:

```nginx
# nginx.conf: Upstream Load Balancing pool configuration
upstream node_backend_cluster {
    server 10.0.0.101:3000; # Node Application 1
    server 10.0.0.102:3000; # Node Application 2
    server 10.0.0.103:3000; # Node Application 3
}

server {
    listen 80;
    location / {
        proxy_pass http://node_backend_cluster; # Round robin routing
    }
}
```

> [!IMPORTANT]
> Ensure the `/health` endpoint checked by the load balancer is fast and does not execute expensive database queries. A slow health check can cause the load balancer to report healthy nodes as down, triggering a cluster crash.

---

## 83. Observability

🔗 **Full Lesson:** [83_Observability.md](./83_Observability.md)

* **What**: The practice of understanding system health and performance using diagnostic outputs classified into Metrics, Logs, and Traces (M.E.L.T.).
* **Why It Exists**: Traditional server logs only show crash reports. Observability combines metrics, logs, and trace data to help you debug performance bottlenecks and network issues.
* **Key Concepts**:
  * **M.E.L.T. Pillars**: Metrics (numeric CPU, memory, request trends), Event Logs (JSON records of specific actions), and Traces (chronological request paths across servers).
  * **Active vs Reactive**: Moving from reactive monitoring (fixing bugs after users report crashes) to active analysis (identifying performance drifts and slow queries beforehand).
  * **OpenTelemetry Standard**: An open framework that standardizes collecting and exporting telemetry data to prevent lock-in to specific tracking tools.

### Key Commands / Code Example:

```text
The Pillars of Observability (M.E.L.T.):
1. Metrics: "CPU is at 88%. QPS is 1200." (Telemetry summaries)
2. Event Logs: "User 101 failed password check at 17:23:01." (Action details)
3. Traces: "Request GET /checkout took 4.2s. Payments API took 4.1s." (Execution maps)
```

> [!IMPORTANT]
> Standardize your telemetry configurations using OpenTelemetry APIs. This allows you to switch between analysis backends (Datadog, Dynatrace, New Relic) without modifying your application code.

---

## 84. Monitoring

🔗 **Full Lesson:** [84_Monitoring.md](./84_Monitoring.md)

* **What**: The real-time collection, visualization, and alerting of system performance metrics (like CPU, RAM usage, and request counts) using agents.
* **Why It Exists**: Alerts developers when servers overload or crash, allowing issues to be fixed before they affect users.
* **Key Concepts**:
  * **Golden Signals**: Critical API health metrics: Latency (response speed), Traffic (QPS), Errors (percentage of failed calls), and Saturation (system load).
  * **Data Collection Agents**: Using software agents (Prometheus, Datadog Agent) to collect system metrics periodically.
  * **Alerting Thresholds**: Setting up rules to send notifications (Slack, PagerDuty) if error rates or system metrics exceed safe limits.

### Key Commands / Code Example:

```javascript
const client = require('prom-client');

// Initialize Prometheus registry
const register = new client.Registry();
client.collectDefaultMetrics({ register });

// Define custom HTTP request counter
const httpRequestCounter = new client.Counter({
  name: 'http_requests_total',
  help: 'Total number of HTTP requests received',
  labelNames: ['method', 'route', 'status'],
});
register.registerMetric(httpRequestCounter);

// Usage inside middleware:
// httpRequestCounter.labels(req.method, req.path, res.statusCode).inc();
```

> [!IMPORTANT]
> Set alert rules based on symptoms that affect users (like high API error rates or slow response times), rather than raw CPU levels. High CPU usage is fine if the application is processing tasks successfully.

---

## 85. Logging Pipelines

🔗 **Full Lesson:** [85_Logging_Pipelines.md](./85_Logging_Pipelines.md)

* **What**: Log ingestion systems that collect, filter, buffer, and stream application JSON logs asynchronously to search engines (like Elasticsearch or Loki).
* **Why It Exists**: Storing log files on local disks eventually exhausts system storage and breaks container scaling. Logging pipelines ship logs to a secure, central search engine.
* **Key Concepts**:
  * **Log Collectors**: Lightweight agents (Fluentbit, Filebeat) that scan stdout files, parse JSON records, and ship them to database stores.
  * **Ingestion Buffering**: Using queues (Kafka, Redis) to protect log database indexing layers from overloading during traffic spikes.
  * **Log Analysis Engines**: Central search systems (Elasticsearch, Grafana Loki) that index fields to support dashboard visualizations.

### Key Commands / Code Example:

```text
JSON Logging Pipeline:
[ Node.js (App) ] ──> (writes JSON) ──> [ stdout log file ]
                                               │
                                       [ Fluentbit Collector ] (reads & ships)
                                               │
                                               ▼
                                       [ Ingest Queue (Kafka) ]
                                               │
                                               ▼
                                  [ Search Engine (Elasticsearch) ] <── [ Grafana Dashboard ]
```

> [!IMPORTANT]
> Never write logs directly to remote search engines from your Node.js application process. Network drops can lose log data, and write latency can block the main event loop thread. Write logs to `stdout` instead.

---

## 86. Distributed Tracing

🔗 **Full Lesson:** [86_Distributed_Tracing.md](./86_Distributed_Tracing.md)

* **What**: A debugging mechanism that maps and tracks the chronological path of requests across network boundaries in microservice architectures.
* **Why It Exists**: In microservices, troubleshooting a slow request is difficult. Distributed tracing maps the exact path of a request across all services and databases, helping isolate performance bottlenecks instantly.
* **Key Concepts**:
  * **Trace Context Propagation**: Injecting trace metadata (Trace ID, Parent Span ID) into outgoing headers and parsing them at the receiving service.
  * **W3C traceparent standard**: Standard HTTP header format `00-traceId-spanId-flags` to ensure compatibility between tracing tools.
  * **AsyncLocalStorage**: A built-in Node.js module used to store active trace contexts across asynchronous boundaries without passing variables through every function.

### Key Commands / Code Example:

```javascript
// Manual W3C Trace Context parsing middleware
function parseTraceContext(req) {
  const traceparent = req.headers['traceparent'];
  let traceId, parentSpanId;

  if (traceparent) {
    // format: version-traceId-spanId-flags
    const parts = traceparent.split('-');
    if (parts.length === 4) {
      traceId = parts[1];
      parentSpanId = parts[2];
    }
  }

  // Generate new IDs if missing (initialize root trace)
  const currentSpanId = require('crypto').randomBytes(8).toString('hex');
  traceId = traceId || require('crypto').randomBytes(16).toString('hex');

  return {
    traceId,
    parentSpanId,
    currentSpanId,
    traceparentHeader: `00-${traceId}-${currentSpanId}-01`
  };
}
```

> [!IMPORTANT]
> Always standardize on W3C `traceparent` headers. Avoid writing custom header formats (like `X-Trace-ID`) to ensure compatibility with API gateways, CDNs, and external platforms.

---

## 87. Production Architecture

🔗 **Full Lesson:** [87_Production_Architecture.md](./87_Production_Architecture.md)

* **What**: The design architecture of microservices, implementing multi-zone redundancy, stateless instances, and database replica routing.
* **Why It Exists**: Outlines how to deploy Node.js backends across multiple physical locations (Availability Zones) to prevent single hardware failures from taking down your application.
* **Key Concepts**:
  * **Multi-AZ Redundancy**: Deploying server instances across multiple physical data centers (Availability Zones) behind a load balancer to survive zone outages.
  * **Read/Write DB Splitting**: Directing write transactions to a Primary SQL database and routing read-only queries to a cluster of Read Replicas to scale database performance.
  * **Stateless Instances**: Ensuring server containers are completely stateless to support auto-scaling and dynamic node replacements.

### Key Commands / Code Example:

```javascript
// db-router.js: Direct database traffic based on write/read actions
const pg = require('pg');
const primaryPool = new pg.Pool({ host: process.env.DB_PRIMARY_HOST }); // Writes
const replicaPool = new pg.Pool({ host: process.env.DB_REPLICA_HOST }); // Reads

const db = {
  async write(queryText, params) {
    console.log('[DB] Routing write query to Primary SQL');
    return primaryPool.query(queryText, params);
  },
  async read(queryText, params) {
    console.log('[DB] Routing read query to Replica SQL Cluster');
    return replicaPool.query(queryText, params);
  }
};
```

> [!IMPORTANT]
> Always deploy your application instances across at least two Availability Zones (AZ) and automate failovers using managed load balancers to ensure continuous availability.

---

## 88. System Design for Node.js

🔗 **Full Lesson:** [88_System_Design_for_NodeJS.md](./88_System_Design_for_NodeJS.md)

* **What**: The ultimate engineering patterns for Node.js, implementing backpressure handles, circuit breakers, scale calculations, and asynchronous task brokers.
* **Why It Exists**: Focuses on designing backend systems that handle millions of requests, survive downstream service crashes, and prevent memory leaks.
* **Key Concepts**:
  * **Circuit Breaker Pattern**: Wrapping downstream service calls. If a service repeatedly fails, the breaker opens and returns a fallback immediately, protecting server resources.
  * **Exponential Backoff & Jitter**: Introducing exponential delay and random noise to query retries, preventing recovering databases from being overwhelmed.
  * **Throughput Calculations**: Calculating necessary server cluster sizes based on peak QPS, average response times, and V8 engine memory limits.

### Key Commands / Code Example:

```javascript
// circuit-breaker.js: Lightweight Circuit Breaker implementation
class CircuitBreaker {
  constructor(apiCall, options = {}) {
    this.apiCall = apiCall;
    this.failureThreshold = options.failureThreshold || 3;
    this.cooldownPeriod = options.cooldownPeriod || 5000;
    
    this.state = 'CLOSED'; // CLOSED, OPEN, HALF-OPEN
    this.failureCount = 0;
    this.nextAttemptTime = Date.now();
  }

  async execute(...args) {
    if (this.state === 'OPEN') {
      if (Date.now() > this.nextAttemptTime) {
        this.state = 'HALF-OPEN';
      } else {
        return { success: false, data: 'Fallback: downstream service down' };
      }
    }

    try {
      const response = await this.apiCall(...args);
      this.failureCount = 0;
      this.state = 'CLOSED';
      return response;
    } catch (err) {
      this.failureCount++;
      if (this.failureCount >= this.failureThreshold) {
        this.state = 'OPEN';
        this.nextAttemptTime = Date.now() + this.cooldownPeriod;
      }
      throw err;
    }
  }
}
```

> [!IMPORTANT]
> Always configure outbound timeouts on all downstream API and database connections. Without timeouts, hanging calls will exhaust connection sockets, crashing the API gateway.

---

Previous : [00_index.md](./00_index.md) | Index : [00_index.md](./00_index.md) | Next : [01_Introduction_to_NodeJS.md](./01_Introduction_to_NodeJS.md)

