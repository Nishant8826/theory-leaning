# 🟢 Node.js – Complete Revision Guide

Welcome to the Node.js Mastery consolidated Master Revision Guide. This guide aggregates all key concepts, commands, configurations, analogies, best practices, and interview questions to allow you to revise the entire module in under 30 minutes from a single file. By examining these concepts from first principles, you can refresh your knowledge of V8 engine execution, event loop phases, core module designs, performance scaling, and production architecture.

---

## 📌 Module Navigation
- [01. Introduction to Node.js](#01-introduction-to-nodejs)
- [02. Node.js Environment Setup](#02-nodejs-environment-setup)
- [03. JavaScript Fundamentals for Node.js](#03-javascript-fundamentals-for-nodejs)
- [04. Runtime vs Framework](#04-runtime-vs-framework)
- [05. V8 Engine](#05-v8-engine)
- [06. Event Loop Basics](#06-event-loop-basics)
- [07. npm](#07-npm)
- [08. npx](#08-npx)
- [09. Modules](#09-modules)
- [10. CommonJS](#10-commonjs)
- [11. ES Modules](#11-es-modules)
- [12. File System Module](#12-file-system-module)
- [13. Path Module](#13-path-module)
- [14. OS Module](#14-os-module)
- [15. Events Module](#15-events-module)
- [16. Buffers](#16-buffers)
- [17. Streams Basics](#17-streams-basics)
- [18. Callbacks](#18-callbacks)
- [19. Promises](#19-promises)
- [20. Async/Await](#20-asyncawait)
- [21. HTTP Module](#21-http-module)
- [22. Creating Web Servers](#22-creating-web-servers)
- [23. REST APIs](#23-rest-apis)
- [24. Express.js](#24-expressjs)
- [25. Middleware](#25-middleware)
- [26. Routing](#26-routing)
- [27. MVC Architecture](#27-mvc-architecture)
- [28. Environment Variables](#28-environment-variables)
- [29. Validation](#29-validation)
- [30. Error Handling](#30-error-handling)
- [31. Logging](#31-logging)
- [32. Authentication](#32-authentication)
- [33. Authorization](#33-authorization)
- [34. JWT](#34-jwt)
- [35. Cookies](#35-cookies)
- [36. Sessions](#36-sessions)
- [37. MongoDB](#37-mongodb)
- [38. Mongoose](#38-mongoose)
- [39. PostgreSQL](#39-postgresql)
- [40. ORM Concepts](#40-orm-concepts)
- [40a. Sequelize ORM](#40a-sequelize-orm)
- [41. Redis](#41-redis)
- [42. Caching](#42-caching)
- [43. Rate Limiting](#43-rate-limiting)
- [44. File Uploads](#44-file-uploads)
- [45. Email Services](#45-email-services)
- [45a. Payment Gateways (Razorpay and Stripe)](#45a-payment-gateways-razorpay-and-stripe)
- [45b. Payment Gateways (Real-Time Scenarios)](#45b-payment-gateways-real-time-scenarios)
- [46. Event Loop Deep Dive](#46-event-loop-deep-dive)
- [47. Streams Deep Dive](#47-streams-deep-dive)
- [48. Worker Threads](#48-worker-threads)
- [49. Cluster Module](#49-cluster-module)
- [50. Child Processes](#50-child-processes)
- [51. Memory Management](#51-memory-management)
- [52. Garbage Collection](#52-garbage-collection)
- [53. Performance Optimization](#53-performance-optimization)
- [54. Node.js Internals](#54-nodejs-internals)
- [55. Security Fundamentals](#55-security-fundamentals)
- [56. OWASP Top Risks](#56-owasp-top-risks)
- [57. Helmet](#57-helmet)
- [58. CORS](#58-cors)
- [59. CSRF](#59-csrf)
- [60. XSS](#60-xss)
- [61. SQL Injection](#61-sql-injection)
- [62. NoSQL Injection](#62-nosql-injection)
- [63. Testing Fundamentals](#63-testing-fundamentals)
- [64. Unit Testing](#64-unit-testing)
- [65. Integration Testing](#65-integration-testing)
- [66. Jest](#66-jest)
- [67. Supertest](#67-supertest)
- [68. Swagger/OpenAPI](#68-swaggeropenapi)
- [69. Microservices](#69-microservices)
- [70. Event-Driven Architecture](#70-event-driven-architecture)
- [71. RabbitMQ](#71-rabbitmq)
- [72. Kafka](#72-kafka)
- [73. Distributed Systems](#73-distributed-systems)
- [74. Scaling Node.js](#74-scaling-nodejs)
- [75. Docker](#75-docker)
- [76. Kubernetes](#76-kubernetes)
- [77. CI/CD](#77-cicd)
- [78. GitHub Actions](#78-github-actions)
- [79. AWS Deployment](#79-aws-deployment)
- [80. Nginx](#80-nginx)
- [81. Reverse Proxy](#81-reverse-proxy)
- [82. Load Balancing](#82-load-balancing)
- [83. Observability](#83-observability)
- [84. Monitoring](#84-monitoring)
- [85. Logging Pipelines](#85-logging-pipelines)
- [86. Distributed Tracing](#86-distributed-tracing)
- [87. Production Architecture](#87-production-architecture)
- [88. System Design for Node.js](#88-system-design-for-nodejs)

---

## 01. Introduction to Node.js
🔗 **Full Lesson:** [01_Introduction_to_NodeJS.md](./01_Introduction_to_NodeJS.md)

* **Why It Exists**: Before Node.js, JavaScript was browser-bound, and traditional web servers (like Apache) allocated a dedicated thread per connection, leading to heavy memory usage and context-switching overhead under heavy database/network I/O loads.
* **Key Concepts**:
  - *Google V8 Engine*: Compiles JavaScript directly into optimized machine code outside the browser.
  - *Libuv Library*: A multi-platform C library that manages the system event loop and a pool of background threads to handle non-blocking asynchronous operations.
  - *CPU-Bound vs. I/O-Bound*: Highly optimized for I/O-bound tasks where threads idle waiting for data, but can block the single main execution thread during heavy computation.

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
> Never block the event loop with synchronous calls (e.g. `fs.readFileSync`) in request handlers, as this halts execution for all other client requests.

---

## 02. Node.js Environment Setup
🔗 **Full Lesson:** [02_NodeJS_Environment_Setup.md](./02_NodeJS_Environment_Setup.md)

* **Why It Exists**: Installing Node.js globally using direct installers leads to version conflicts, write-access permission errors (forcing the usage of `sudo npm install`), and environment drift across developer systems and production.
* **Key Concepts**:
  - *Node Version Managers*: Tools (like NVM or FNM) that dynamically modify the system's `PATH` variable to redirect `node` and `npm` executions to isolated local directories.
  - *Engine Locking*: Enforcing node/npm engine requirements inside the application configuration file to abort execution on wrong runtimes.
  - *Deterministic Configuration*: Utilizing strict npm policies like exact-save dependency locking to shield build runs from buggy packages.

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

* **Why It Exists**: Core JavaScript behaviors—like scopes, lexical environments, execution contexts, and closures—govern how memory is managed, variable namespaces are resolved, and context states behave on server instances.
* **Key Concepts**:
  - *Execution Context & Call Stack*: Runtimes initialize code in a Global Execution Context and manage active functions on a LIFO (Last In, First Out) Call Stack.
  - *Closures & Memory Leaks*: Closures preserve access to outer variables even after parent execution contexts clear. Storing a closure reference in a global cache or array prevents V8 from garbage collecting the referenced variables.
  - *Context Bindings (`this`)*: The global context `this` references `module.exports` in Node.js modules. Standard functions bind context dynamically while arrow functions preserve lexical context boundaries.

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

* **Why It Exists**: Conflating a runtime environment (like Node.js) with code frameworks (like Express) leads to weak troubleshooting, as developers fail to diagnose whether a network bug lies in routing abstractions or underlying OS socket streams.
* **Key Concepts**:
  - *Runtime Environment*: Integrates an execution engine (like V8) and wraps low-level system calls (filesystem, TCP, cryptographic cards) to run language code on the server.
  - *Web Framework*: An application layer built on top of runtime APIs that simplifies development by introducing MVC structuring, validation helpers, and routing patterns.
  - *Alternative Runtimes*: Systems like Deno (Rust/V8, secure sandbox, ESM) and Bun (Zig/JavaScriptCore, fast startup, built-in bundler) run JS files using different design tradeoffs.

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

* **Why It Exists**: JavaScript is dynamically typed and executed on the fly. Google's V8 engine JIT-compiles JS into native machine code, managing execution pipelines and dynamic property mappings to reach execution speeds comparable to static languages.
* **Key Concepts**:
  - *JIT Compilation Pipeline*: Ignition interpreter compiles code to bytecode, monitoring hot paths. TurboFan compiler then extracts hot code to generate optimized machine instructions.
  - *Hidden Classes & Inline Caches*: V8 dynamically associates objects with internal Shapes (Hidden Classes). Inline Cache (IC) bypasses class lookups by saving the offset address of accessed properties.
  - *V8 Heap Structure*: Divides dynamic allocation memory into New Space (scavenger GC), Old Space (mark-sweep GC), Large Object Space, and Code Space (TurboFan targets).

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

* **Why It Exists**: Node.js operates on a single main execution thread. It handles high concurrency by offloading I/O blocking tasks to the operating system or Libuv's thread pool and scheduling callbacks via the Event Loop.
* **Key Concepts**:
  - *Execution Queues*: Tasks are split into high-priority Microtasks (`process.nextTick`, Promises) and standard Macrotasks (timers, network, FS I/O).
  - *Loop Phases*: The event loop executes in phases: Timers (setTimeout), I/O Pending, Idle/Prepare, Poll (waiting/checking network), Check (setImmediate), and Close.
  - *Microtask Exhaustion*: Microtask queues execute immediately when the stack clears. Recursive `process.nextTick` calls will drain resource ticks and starve macrotasks.

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

* **Why It Exists**: Managing external libraries requires strict version controls, dependency resolution, and integrity checks to avoid supply chain hacks and broken code builds when patch updates are released.
* **Key Concepts**:
  - *Semantic Versioning (SemVer)*: Formatted as `MAJOR.MINOR.PATCH`. Operators like Caret (`^`) allow minor/patch updates, Tilde (`~`) limits to patches, and exact matching locks changes completely.
  - *Integrity Locking*: `package-lock.json` maps exact versions and includes SHA-512 cryptographic subresource hashes to guarantee identical package codes across deployments.
  - *Dependency Classification*: Separating dependencies (production requirements) from devDependencies (development testing/builders) reduces production build sizes.

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

* **Why It Exists**: Installing package CLI binaries globally causes version conflicts, while adding one-off binaries to local dependencies bloats the project file sizes and PATH environments.
* **Key Concepts**:
  - *Ephemeral Execution*: npx fetches the requested package CLI to a temporary cache, executes the binary command, and deletes it right after execution.
  - *Local Path Scanning*: Before requesting remote registries, npx scans the local directory's `node_modules/.bin` to execute local dependency packages directly.
  - *Direct Remote Calling*: Executes command blocks from raw HTTP source URLs or specific versions of packages without permanent installations.

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

* **Why It Exists**: Browsers share the global namespace, creating context name collisions. Node.js implements modules to isolate variables and functions inside files, enabling clean modular programming.
* **Key Concepts**:
  - *The Module Wrapper*: Node.js wraps code modules in a hidden IIFE function before compilation to inject parameters (`exports`, `require`, `module`, `__filename`, `__dirname`).
  - *Private Scopes*: Variables declared inside module code remain private to that file unless assigned explicitly to `module.exports`.
  - *Circular Dependencies*: Requiring file A from B and B from A causes V8 to supply an incomplete export object to resolve the loops, leading to unexpected `undefined` parameters.

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

* **Why It Exists**: Created to implement a synchronous module system for server-side Javascript environments, where module dependencies are loaded locally from file paths on disk.
* **Key Concepts**:
  - *Synchronous Loading*: Resolves and loads dependencies instantly in sequence. This blocks code execution, making it unsuitable for client-side browsers.
  - *Caching Mechanisms*: Cache modules by path in `require.cache`. Multiple `require` calls to the same file return the exact same instance.
  - *Dynamic Importing*: Because require behaves as a standard function, you can call it inside conditionals or loops during runtime.

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

* **Why It Exists**: Standardized ECMAScript module syntax designed to load modules asynchronously, support static analysis, and enable tree-shaking optimizations.
* **Key Concepts**:
  - *Static Resolution*: Import/export mappings are analysed at compile time. This prevents calling imports conditionally or inside loop scopes.
  - *Asynchronous Parsing*: Executed in three isolated steps: Construction (resolving files), Instantiation (mapping variables), and Evaluation (running code blocks).
  - *Path Resolving*: Paths require absolute filenames with extensions (e.g. `./db.js`) as they must support remote URL resolving.

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

* **Why It Exists**: Provides programmatic access to the host machine's filesystem, wrapping OS-level file actions into standard JavaScript APIs.
* **Key Concepts**:
  - *API Variants*: Provides synchronous (blocking), callback (async), and promise-based async utilities.
  - *Thread-pool Offloading*: Asynchronous filesystem calls are offloaded to Libuv background threads, freeing the main thread for event processing.
  - *Buffer Limits*: Standard file reads allocate the entire file into a V8 memory buffer, which will crash the engine on large files (use Streams instead).

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

* **Why It Exists**: Resolving file paths using manual string concat fails across operating systems because Windows uses backslashes (`\`) while POSIX/Linux systems use forward slashes (`/`).
* **Key Concepts**:
  - *Platform Abstraction*: Automatically uses system-specific delimiters (slashes) depending on where the node runtime is executing.
  - *path.join vs path.resolve*: `path.join` concatenates path parts. `path.resolve` compiles an absolute path resolving from the execution directory (`process.cwd()`).
  - *Parsing utilities*: Includes functions to parse paths into structures containing directories, extensions, root, and file names.

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

* **Why It Exists**: System deployment and infrastructure management require access to host hardware stats like memory limits, cpu architectures, and network interface ports.
* **Key Concepts**:
  - *Hardware Diagnostics*: Exposes real-time CPU metrics, operating system versioning, system uptime, and memory capacities.
  - *Network Interfaces*: Exposes local IP assignments, MAC addresses, and network routing configurations.
  - *Cluster Core Matching*: Used to fetch available logical processor cores (`os.cpus().length`) to scale process clusters.

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

* **Why It Exists**: Complex backend flows require decoupled publisher-subscriber patterns to react to process activities asynchronously.
* **Key Concepts**:
  - *EventEmitter Class*: Establishes an observer structure where modules register listener callbacks that execute when matching event tags are emitted.
  - *Synchronous Execution*: Event listeners are executed synchronously in the order they are registered in the current event loop execution tick.
  - *Reference Retaining*: Lingering listeners retain references to parent variables, causing closures to leak memory if not removed with `.off()`.

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

* **Why It Exists**: JavaScript was not originally designed to handle binary data streams. Buffers allow Node.js to handle raw binary data payloads (like file streams and TCP packets) by allocating raw memory blocks outside the V8 heap.
* **Key Concepts**:
  - *Fixed-Size Allocations*: Once allocated, buffer sizes cannot be dynamically resized, requiring careful prediction of expected stream size.
  - *Clean vs Unsafe Allocation*: `Buffer.alloc()` zero-fills allocated memory for safety, whereas `Buffer.allocUnsafe()` is faster but leaves pre-existing data in the raw memory, posing security leak threats.
  - *V8 Heap Independence*: Allocations occur in raw C++ system memory rather than inside the V8 garbage-collector monitored heap, optimizing high-performance applications.

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

* **Why It Exists**: Loading very large files (e.g. 4GB databases or videos) entirely into memory will exceed V8 heap limits and crash Node.js. Streams resolve this by loading and processing files chunk-by-chunk.
* **Key Concepts**:
  - *Stream Architectures*: Classified into Readable (source), Writable (destination), Duplex (bi-directional like sockets), and Transform (mutator like zlib compressions).
  - *Backpressure Control*: A mechanism that pauses reading pipes if the writing stream is slower than the incoming chunk speed, preventing memory spikes.
  - *Event-Driven Handling*: Emits life-cycle triggers like `'data'`, `'end'`, `'drain'`, and `'error'` to orchestrate chunk streams.

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

* **Why It Exists**: Allows code blocks to execute immediately after asynchronous system tasks complete without blocking the single main execution thread.
* **Key Concepts**:
  - *Delegation Pattern*: Handed to async functions as arguments to run once offloaded Libuv/OS tasks report completions.
  - *Error-First Conventions*: Node.js callbacks accept error variables as their first parameter (`err`) and data payloads as the second (`data`).
  - *Callback Hell*: Deeply nested asynchronous callbacks make code hard to read, maintain, and dry-run (leading to Promise abstractions).

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

* **Why It Exists**: Replaces nested callbacks with clean, chainable asynchronous objects that handle operational failures and successes uniformly.
* **Key Concepts**:
  - *Promise States*: Transition from `pending` to either `fulfilled` (via `resolve()`) or `rejected` (via `reject()`). Once resolved, state is immutable.
  - *Microtask Queue*: Promise callbacks execute inside V8's microtask queue, which has execution priority over standard macrotask queues (like timers).
  - *Promise Chaining*: Replaces nested structures with sequential `.then()` flows, routing all intermediate exceptions to a single trailing `.catch()` block.

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

* **Why It Exists**: Simplifies Promise tracking by allowing asynchronous operations to be written in a flat, readable style resembling synchronous code.
* **Key Concepts**:
  - *Syntax Sugar*: Functions declared as `async` automatically return a Promise. The `await` keyword pauses execution context until the target promise resolves.
  - *Event Loop Preservation*: Pausing inside an async function only yields control back to the Event Loop, allowing other events to execute.
  - *Exception Control*: Allows standard `try/catch` syntax to handle asynchronous exceptions, simplifying error routing.

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

* **Why It Exists**: Serves as the low-level foundation for network servers in Node.js, parsing TCP streams into standard HTTP requests and responses.
* **Key Concepts**:
  - *Network Bridge*: Directs TCP sockets into Node's parser, exposing headers, paths, and methods to the runtime environment.
  - *IncomingMessage (`req`)*: Acts as a readable stream of incoming network request chunks, capturing headers, verbs, and query strings.
  - *ServerResponse (`res`)*: A writable stream used to send response headers, set status codes, and write content payloads back to clients.

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

* **Why It Exists**: Enables serving API responses or website assets by analyzing incoming URL structures and routing them to appropriate data handlers.
* **Key Concepts**:
  - *Request Routing*: Matching the incoming request URL and method (e.g. GET `/api/users`) to execute distinct logic.
  - *Body Buffer Stream*: In raw servers, requests containing body data (like POST) must be read asynchronously in chunks from the readable stream.
  - *Header Management*: Setting proper Content-Length, Content-Type, and CORS headers to ensure browsers parse payloads correctly.

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

* **Why It Exists**: Establishes a stateless, standardized interface pattern using uniform HTTP methods and status codes for API communication.
* **Key Concepts**:
  - *Stateless Architecture*: Each HTTP request must contain all context and tokens required to process it, without depending on server-side session states.
  - *HTTP Resource Verbs*: Utilizes HTTP verbs to map resource actions: GET (retrieve), POST (create), PUT (replace), PATCH (update parts), and DELETE (remove).
  - *Status Code Standards*: Uses status codes to return structural results: 200/201 (success), 400 (bad input), 401 (no authentication), 403 (unauthorized), 404 (missing), 500 (internal failure).

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

## 24. ExpressJS
🔗 **Full Lesson:** [24_ExpressJS.md](./24_ExpressJS.md)

* **Why It Exists**: Replaces low-level Node HTTP boilerplate with a simple, high-performance middleware chain and routing engine.
* **Key Concepts**:
  - *Middleware Pipeline*: Processes incoming requests sequentially through an array of functions before returning a response.
  - *Response Abstractions*: Simplifies tasks with helper APIs like `res.json()`, `res.status()`, and `res.sendFile()`.
  - *Route Param Parsing*: Automatically parses parameters from route segments (e.g. `/users/:id` maps parameter to `req.params.id`).

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

* **Why It Exists**: Runs code sequentially during the request-response cycle to execute validations, authentication, logging, or data mutations before reaching controllers.
* **Key Concepts**:
  - *The Middleware Signature*: A function accepting `req`, `res`, and `next` arguments. Calling `next()` forwards control down the chain.
  - *Types of Middleware*: Classified into Application-level (`app.use`), Router-level, Built-in (e.g. `express.static`), Third-party (e.g. `cors`), and Error-handling.
  - *Execution Sequence*: Order matters. Middleware declared first executes first. Global parsers must sit above routes.

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

* **Why It Exists**: Cleanly structure application codebases by isolating path endpoints and request verbs into modular files rather than keeping them in a single file.
* **Key Concepts**:
  - *express.Router*: A mini-application instance capable of executing middleware and routing functions, mounted dynamically onto parent applications.
  - *Parameter Matching*: Supports path patterns (wildcards, regex, colon variables) to parse variables dynamically.
  - *Router Mounting*: Groups related endpoints (e.g. `/api/v1/users`) into dedicated sub-routers to maintain a clean project structure.

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

* **Why It Exists**: Divides applications into Model (data and storage logic), View (output structure), and Controller (orchestration logic) to keep codebase layers clean, testable, and maintainable.
* **Key Concepts**:
  - *Model Layer*: Enforces schema rules, executes database queries, and manages data states.
  - *Controller Layer*: Intercepts requests, validates inputs, invokes models, and determines which view to output.
  - *View Layer*: Formats the response representation (returning JSON structures in modern REST APIs, or server-side HTML template engines).

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

* **Why It Exists**: Storing database passwords, API credentials, and runtime secrets in code leads to security breaches and credential leaks. Environment variables keep configuration data decoupled from source files.
* **Key Concepts**:
  - *process.env*: The Node.js object mapping current system shell environment variables inside runtime memory.
  - *dotenv Library*: Reads local `.env` configuration files during application bootstrap and writes key-value pairs into `process.env`.
  - *Configuration Management*: Allows loading different credentials (dev, staging, prod) dynamically based on the execution context.

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

* **Why It Exists**: Server systems cannot trust client inputs. Validation blocks invalid, malicious, or malformed data schemas at the API boundary, keeping database systems clean and secure.
* **Key Concepts**:
  - *Request Sanitization*: Strips illegal characters, scripts, or undefined object keys from payloads before parsing.
  - *Schema Validation*: Validates bodies, URL parameters, and headers against strict structural definitions using validator libraries (e.g. Zod or Joi).
  - *Boundary Defense*: Catching validation errors at request pipelines protects database layers from parsing failures.

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

* **Why It Exists**: Uncaught runtime errors crash the single Node thread, taking down the entire server. Structuring exception rules ensures stability, logs debug data, and maps errors to clear status codes.
* **Key Concepts**:
  - *Error Middeleware Signature*: Express maps errors to middleware functions containing 4 arguments: `(err, req, res, next)`.
  - *Error Categorization*: Splits failures into Operational (predictable issues like invalid credentials) and Programmer errors (unhandled system bugs).
  - *Crash Management*: Real-world servers should log programmer errors and perform a graceful shutdown while process managers (like PM2) spin up replacement instances.

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

* **Why It Exists**: Writing stdout messages using standard `console.log()` in production is slow (runs synchronously, blocking the main thread) and outputs unstructured text that cannot be parsed by log collectors.
* **Key Concepts**:
  - *Structured Log Outputs*: Formatting logs as single-line JSON structures to facilitate machine parsing and indexing.
  - *Log Severity Levels*: Categorizing events by severity: debug, info, warn, and error, to filter out verbose traffic in production.
  - *Asynchronous Shaving*: Buffering outputs and writing log payloads using non-blocking filesystems to prevent event loop bottlenecks.

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

* **Why It Exists**: Confirms the identity of a client attempting to access server routes, establishing a secure trust boundary before parsing requests.
* **Key Concepts**:
  - *Cryptographic Salt Hashing*: Salting introduces random strings to password fields before hashing, rendering rainbow-table lookup strategies useless.
  - *Argon2/Bcrypt Standards*: Algorithms designed with high processing costs to slow down calculations and mitigate brute-force attempts.
  - *Token/Session Mapping*: Binding authenticated request streams to either temporary signed payloads (JWT) or database reference IDs (sessions).

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

* **Why It Exists**: Restricts authenticated identities from reaching specific routes or files based on their access rights, roles, or attributes.
* **Key Concepts**:
  - *Role-Based Access Control (RBAC)*: Defining fixed roles (e.g. admin, user, editor) and checking if active requests carry matching tags.
  - *Attribute-Based Access Control (ABAC)*: Fine-grained access control inspecting resource ownership (e.g. checking if `requestingUser.id === document.ownerId`).
  - *Access Middleware Hooks*: Intercepting requests inside early pipeline stages to evaluate authorization flags and return HTTP 403 Forbidden on check failures.

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

* **Why It Exists**: Provides a stateless, cryptographically signed token mechanism that allows servers to authorize requests without querying database session tables.
* **Key Concepts**:
  - *JWT Architecture*: Formatted in three base64 segments: Header (signing algorithm), Payload (user claims), and Signature (verifies integrity).
  - *Stateless Validation*: The server verifies the token signature using a local secret key. If valid, the payload claims are trusted without database queries.
  - *Expiry Guarding*: Enforcing short lifespans (e.g., 15 minutes) on tokens and utilizing refresh token flows to renew keys.

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
  // Verifies signature integrity and expiration
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

* **Why It Exists**: Enables HTTP servers to write small key-value strings to client browsers, which are automatically sent back in the headers of all subsequent requests.
* **Key Concepts**:
  - *HttpOnly Protection*: Prevents client-side scripts (like `document.cookie`) from reading the cookie, mitigating token theft via Cross-Site Scripting (XSS).
  - *Secure Protocol Constraint*: Restricts cookies to be transmitted only over TLS/HTTPS encrypted connections, preventing interception.
  - *SameSite Context Rules*: Restricts when cookies are sent on cross-site requests, mitigating Cross-Site Request Forgery (CSRF).

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

* **Why It Exists**: Implements a stateful server-managed authentication system by storing session payloads on the server and referencing them via a random session ID cookie.
* **Key Concepts**:
  - *Stateful Control*: User variables (auth status, shopping carts) are stored in server memory (e.g. Redis). The client only gets a cryptographically signed session ID.
  - *Access Revocation*: Session states can be instantly deleted on the server, immediately terminating client access (a key advantage over stateless JWTs).
  - *Central Store Scaling*: Storing session states in local RAM breaks load balancing. Production clusters require storing sessions in shared, fast memory stores like Redis.

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

* **Why It Exists**: A document-oriented NoSQL database that structures data in flexible JSON-like BSON files, allowing fast horizontal scaling and dynamic schema changes.
* **Key Concepts**:
  - *Document Store model*: Organizations map schemas directly to nested JSON fields (subdocuments, arrays), reducing the need for complex, slow SQL joins.
  - *Horizontal Sharding*: Scales write-heavy databases by partitioning data ranges across multiple database shards.
  - *Index Configurations*: B-Tree indexes speed up lookups, but slow down writes as indexes must be rebuilt on each document insert.

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

* **Why It Exists**: Establishes a Schema-based Object Document Mapper (ODM) on top of MongoDB, enforcing type casting, validations, and query hooks.
* **Key Concepts**:
  - *Strict Schema Mapping*: Sanitizes incoming document fields, rejecting properties not explicitly declared inside the schema definition.
  - *Active Record Hooks*: Invoking middleware hooks (e.g. hashing passwords inside the `'save'` hook before writing to database collections).
  - *Virtuals & Populate*: Simulates data relations (virtual joins) by linking document IDs and populating referenced structures during query execution.

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

* **Why It Exists**: A highly reliable, ACID-compliant Relational Database Management System (RDBMS) designed to guarantee transactional integrity and support complex data analysis.
* **Key Concepts**:
  - *Relational Integrity*: Table schemas enforce rigid fields, data types, and foreign key relations to protect data structure rules.
  - *ACID Compliance*: Ensures transactions are Atomic, Consistent, Isolated, and Durable, preventing data corruption during failures.
  - *Query Optimizations*: Utilizes query planners, explain scopes, and indexing (B-Tree, GIN) to optimize query paths over large datasets.

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

* **Why It Exists**: Abstracts database communication behind object-oriented APIs, letting developers query relational tables or document structures using language methods instead of writing SQL strings.
* **Key Concepts**:
  - *Data Mapping Patterns*: Active Record pattern (models define fields and carry query methods) vs. Data Mapper pattern (entities are thin, repositories query data).
  - *Schema Sync & Migrations*: Managing database changes programmatically using migration files to track modifications in version control.
  - *The N+1 Query Problem*: An optimization issue where querying parent records executes separate database requests for each child record, bloating network latency.

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

* **Why It Exists**: A promise-based Node.js ORM implementing the Active Record pattern for SQL databases, wrapping schemas, relations, and transactional logic.
* **Key Concepts**:
  - *Model Associations*: Declaring table relations using Active Record helpers: `hasMany`, `belongsTo`, and `belongsToMany`.
  - *Managed Transactions*: Wrapping database queries in transaction hooks to automatically roll back changes if intermediate errors occur.
  - *Migration Scaffolding*: Modifying table structures sequentially using version-controlled up/down script files.

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

* **Why It Exists**: Storing and fetching data from disk-based databases slows down routes. Redis provides an in-memory key-value store to serve cached queries and session data in sub-milliseconds.
* **Key Concepts**:
  - *In-Memory Architecture*: Holds datasets in server RAM, periodically writing snapshots to disk asynchronously to prevent data loss.
  - *Data Types*: Supports keys mapped to Strings, Hashes (objects), Lists (queues), and Sets (unique listings).
  - *TTL Expiry*: Attaches Time-To-Live (TTL) timestamps to keys to automatically purge stale cache entries.

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

* **Why It Exists**: Prevents database scaling bottlenecks and speeds up response times by saving processed query results in high-speed, temporary cache memory.
* **Key Concepts**:
  - *Cache-Aside Pattern*: The application checks the cache layer first. On a cache miss, it queries the database, writes the result to the cache, and returns it.
  - *Cache Invalidation*: Updating or deleting cached data immediately when database records are modified to prevent returning stale data to users.
  - *Cache Stampede / Herd Effect*: An issue where multiple concurrent requests query the database simultaneously when a cache key expires, degrading database performance.

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

* **Why It Exists**: Protects web APIs from brute-force attempts, scrapers, and denial-of-service (DDoS) resource starvation by restricting client request frequency.
* **Key Concepts**:
  - *Token Bucket / Sliding Window*: Algorithms that track request frequencies inside sliding windows to throttle excessive client requests.
  - *Redis Tracking*: Using client IP addresses as key flags in Redis and incrementing counters to block clients exceeding limits.
  - *Throttling Responses*: Returning HTTP status code `429 Too Many Requests` along with standard `Retry-After` headers once limits are reached.

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

* **Why It Exists**: Web servers require secure mechanisms to accept, parse, validate, and store file payloads (e.g. PDFs, images) uploaded by users.
* **Key Concepts**:
  - *multipart/form-data encoding*: The standard HTTP encoding format for files, requiring specialized parsers to read file binary streams.
  - *Disk vs Memory Storage*: Multer can write files to a temporary disk location or buffer them directly in RAM to stream to cloud storage buckets.
  - *Validation Filtering*: Checking file size limits and MIME types at the route boundary to reject execute-permissions files (e.g. `.exe`, `.sh`).

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

// app.post('/profile/avatar', uploader.single('avatar'), controller);
```

> [!WARNING]
> Do not store user-uploaded files on local server disks in load-balanced clusters, as other server nodes will not be able to access those files. Stream uploads directly to a centralized object store (like AWS S3).

---

## 45. Email Services
🔗 **Full Lesson:** [45_Email_Services.md](./45_Email_Services.md)

* **Why It Exists**: Enables web applications to send automated transactional notifications (such as registration confirmations or password resets) to users.
* **Key Concepts**:
  - *SMTP Transport vs. Web APIs*: Sending emails via direct SMTP configurations (using Nodemailer) vs. calling transactional email API providers (SendGrid, Mailgun).
  - *HTML Templating*: Compiling responsive HTML email templates programmatically using template engines (Handlebars, EJS) to support personalized variables.
  - *Asynchronous Queuing*: Offloading mailing tasks to background queues to prevent email delivery latency from blocking HTTP requests.

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

* **Why It Exists**: Securely processing credit cards directly on application servers requires strict, expensive PCI-DSS certifications. Payment gateways collect sensitive card details directly from user browsers, keeping backend servers out of PCI scope.
* **Key Concepts**:
  - *Card Tokenization*: Card details are processed on the gateway's secure network. The backend only receives a secure token to execute the transaction.
  - *Client-Server Coordination*: Orchestrating payment flows: backend sets up payment details, client completes payment via gateway UI, and backend verifies success.
  - *Webhook Verification*: Gateways emit async HTTP POST callbacks to confirm payment success. The backend must cryptographically verify webhook signatures to prevent fraud.

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

* **Why It Exists**: Real-world e-commerce transactions require handling edge cases like network timeouts, checkout cancellations, refunds, database crashes, and webhook failures.
* **Key Concepts**:
  - *Payment Idempotency*: Utilizing idempotency keys in API requests to prevent double-charging users during network retries.
  - *checkout-timers*: Reserving stock temporarily while the payment is processed. If the checkout fails or expires, the reserved inventory is automatically released.
  - *Webhook Idempotency*: Design database webhook handlers to identify and ignore duplicate events from payment gateways.

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

* **Why It Exists**: Failure to understand how the event loop scheduling transitions between I/O poll, timers, and check phases can lead to race conditions, microtask starvation, and severe performance bottlenecks in high-concurrency systems.
* **Key Concepts**:
  - *Six Loop Phases*: Libuv iterates through distinct phases in a Tick: Timers (setTimeout/setInterval), Pending (deferred system errors), Idle/Prepare (internals), Poll (fetch I/O events, block if idle), Check (setImmediate), and Close (socket cleanup).
  - *Microtask Boundaries*: Microtasks (`process.nextTick` and resolved Promise callbacks) execute immediately after the current phase operation finishes, before moving to the next loop phase.
  - *Deterministic Scheduling*: In the global scope, `setImmediate` vs `setTimeout(..., 0)` is non-deterministic. However, within an I/O callback (Poll phase), `setImmediate` always executes first as the loop transitions directly to the Check phase.

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

* **Why It Exists**: High-throughput pipelines require understanding stream internals. If you do not manage backpressure, a fast data source can overwhelm a slow data destination, causing the application to accumulate data in memory buffers, resulting in memory leaks and crashes.
* **Key Concepts**:
  - *highWaterMark*: Defines the maximum internal buffer size before backpressure is triggered (default 16KB for standard streams, 64KB for file streams, or 16 items in objectMode).
  - *Backpressure Control*: When a writable stream's buffer fills, `.write(chunk)` returns `false`. The readable source must pause sending data until the writable destination emits the `drain` event.
  - *Custom Stream Types*: Custom streams are built by extending core classes and overriding private methods: `_read` (Readable), `_write` (Writable), or `_transform` (Transform).

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

* **Why It Exists**: Executing heavy calculations (like password hashing, image resizing, or CPU-bound loops) on the main execution thread blocks the event loop, freezing all other client requests. Spawning worker threads yields non-blocking parallel processing.
* **Key Concepts**:
  - *V8 Heap Isolation*: Each worker thread runs its own isolated V8 engine instance (private heap and call stack), bypassing single-threaded runtime CPU limits.
  - *Shared Memory Space*: Workers can share memory zones directly using `SharedArrayBuffer` structures, bypassing serialization delays over Inter-Process Communication (IPC).
  - *Atomics Operations*: Because shared memory is vulnerable to race conditions, the `Atomics` object provides non-interruptible memory-access APIs (like `Atomics.add` or `Atomics.wait`) to prevent data corruption.

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

* **Why It Exists**: Node.js defaults to running on a single CPU core, leaving other physical CPU cores idle. Clustering spawns replica workers under a single port to distribute workloads, maximizing server hardware throughput.
* **Key Concepts**:
  - *Master-Worker Orchestration*: The Primary (Master) process binds to the port, spawns workers, and routes incoming TCP connections, while Worker processes execute the application code.
  - *Routing Modes*: In Round-Robin mode (Linux default), the Primary accepts connections and hands them off to idle workers. In Shared Socket mode (Windows default), workers compete to accept connections directly, which can lead to load imbalance.
  - *Graceful Recovery*: The primary process can monitor worker exit events and immediately execute `cluster.fork()` to spin up replacements, ensuring high availability.

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

* **Why It Exists**: Spawning child processes allows Node.js to execute system binaries, run shell scripts, or run calculations written in other languages without blocking the main event loop.
* **Key Concepts**:
  - *Process Execution Methods*: `exec` runs commands in a shell and buffers output. `execFile` executes binaries directly without shell overhead. `spawn` spawns processes and streams output. `fork` runs Node.js modules with a built-in IPC channel.
  - *Buffer Limits*: `exec` and `execFile` buffer the entire stdout/stderr payload with a default limit of 1MB. Exceeding this limit immediately terminates the child process with a `maxBuffer exceeded` error.
  - *Command Injection Vulnerability*: Using shell-spawning methods like `exec` with unvalidated user input allows attackers to append shell control operators and run unauthorized terminal commands.

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

* **Why It Exists**: Although JavaScript manages memory automatically, backend applications that run indefinitely must optimize allocations to avoid memory leaks, which cause heap exhaustion and process crashes in production.
* **Key Concepts**:
  - *Stack vs Heap*: The Stack stores fast, local primitive values and function execution stack frames. The Heap stores complex references (objects, arrays, and closures) and is managed by the Garbage Collector.
  - *Memory Metrics*: `process.memoryUsage()` tracks heapTotal (allocated V8 heap), heapUsed (active JS objects), and rss (Resident Set Size: total physical memory used by the process).
  - *Retention Leaks*: Occur when references to short-lived variables are retained by long-lived global objects (such as unevicted caches, forgotten event listeners, or uncleared intervals), preventing garbage collection.

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

* **Why It Exists**: High-performance backend services must write GC-friendly code. Creating too many temporary objects forces the garbage collector to run frequently, causing Stop-The-World pauses that block the main thread and spike API latency.
* **Key Concepts**:
  - *Generational Heap*: Based on the hypothesis that most objects die young, the heap is split into the New Space (young, short-lived objects) and the Old Space (long-lived objects promoted from New Space).
  - *Minor GC (Scavenger)*: Manages New Space using Cheney's copying algorithm, dividing it into From-Space and To-Space. Reachable objects are copied to To-Space and compacted, then spaces are flipped. It runs in 1-5ms.
  - *Major GC (Mark-Sweep-Compact)*: Manages Old Space. It marks reachable objects, sweeps dead objects into a free list, and compacts memory. It can cause Stop-The-World pauses of 50-500ms.

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

* **Why It Exists**: Resolving performance bottlenecks (CPU blocking, DB queries, JSON serialization) is critical to prevent server timeouts and keep infrastructure costs low under heavy user load.
* **Key Concepts**:
  - *Benchmark-Profile-Optimize*: The required workflow for optimization. Never guess; measure the baseline, profile execution metrics, refactor the bottleneck, and run load tests to verify.
  - *JSON Serialization Latency*: Native `JSON.stringify` runs synchronously and inspects objects dynamically, which is slow for large arrays. Compiled schema serializations perform up to 2x faster.
  - *Diagnostic Tools*: Clinic.js provides Doctor (diagnoses bottlenecks), Flame (generates execution flamegraphs), and Bubbleprof (tracks async latency).

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

* **Why It Exists**: Deep familiarity with the internal runtime architecture—such as C++ bindings and the Libuv thread pool—enables developers to resolve low-level performance issues and debug system-level failures.
* **Key Concepts**:
  - *Architectural Layers*: Built using the JS Core Library (API surface), C++ Bindings (glue layer linking JS to C++), V8 Engine (JS compilation), and Libuv (Event Loop and thread pool).
  - *Libuv Thread Pool*: Handles blocking operations (FS access, DNS lookups, crypto) using an internal thread pool. The default size is 4, which can cause starvation when running concurrent blocking tasks.
  - *Environment Configuration*: The thread pool size must be adjusted by setting the `UV_THREADPOOL_SIZE` environment variable at the system level before Node.js starts initializing.

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

* **Why It Exists**: Securing Node.js applications requires defensive design. Hardcoded secrets, processes running with excessive permissions, or slow connection handlers make servers vulnerable to data leaks and attacks.
* **Key Concepts**:
  - *Principle of Least Privilege*: A process must run with the lowest permissions necessary. Never run Node.js applications as the system root user, as a compromise would yield full host control.
  - *Payload Size Constraints*: Restricting request sizes on body parsers limits memory usage and prevents Denial of Service (DoS) attacks from large payloads.
  - *Timeout Settings*: Setting connection timeouts on HTTP socket handles protects servers against Slowloris attacks that exhaust available sockets.

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

* **Why It Exists**: Writing secure code requires understanding how common vulnerabilities—such as broken access control, cryptographic failures, and injection attacks—manifest in Node.js, allowing you to mitigate them.
* **Key Concepts**:
  - *Broken Access Control*: Occurs when APIs return records without verifying user ownership (Insecure Direct Object References - IDOR). Mitigation requires validating resource access rights in every controller.
  - *NoSQL Injection*: Occurs when MongoDB queries accept unvalidated object values (e.g. `{ "$ne": "" }`), permitting attackers to bypass database password checks.
  - *Information Leakage*: Exposing database connection strings or detailed execution stack traces in production HTTP responses leaks system details to attackers.

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

* **Why It Exists**: Express exposes frameworks details (such as `X-Powered-By: Express`), allowing attackers to target your specific stack. Helmet sets secure HTTP response headers to defend against clickjacking, script injection, and MIME-sniffing.
* **Key Concepts**:
  - *Content Security Policy (CSP)*: Restricts resource source URLs (scripts, images, CSS) to prevent execution of unauthorized scripts and inline XSS payloads.
  - *Clickjacking Defense*: Sets `X-Frame-Options` to `DENY` or `SAMEORIGIN` to block browsers from embedding your pages inside malicious `<iframe>` wrappers.
  - *MIME Sniffing Prevention*: Sets `X-Content-Type-Options: nosniff`, forcing browsers to strictly adhere to the declared MIME type rather than parsing file content (defends against script uploads disguised as images).

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

* **Why It Exists**: To prevent cross-origin script executions from stealing data, browsers implement the Same-Origin Policy (SOP). CORS defines safe access headers, letting authorized frontend origins consume backend APIs.
* **Key Concepts**:
  - *Preflight OPTIONS Requests*: For write verbs (PUT, DELETE) or custom authorization headers, browsers emit a preflight `OPTIONS` query to verify CORS permissions before sending the actual request.
  - *Same-Origin Definition*: Same-origin requires matching protocols, domain names, and port configurations. Any variation triggers CORS validation.
  - *Credential Constraints*: When cross-origin API calls require authentication cookies (`credentials: true`), the wildcard origin `*` is forbidden. The server must return explicit origin whitelist match headers.

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

* **Why It Exists**: Browsers automatically append cookies to HTTP requests matching target domains. Attackers can exploit this by hosting forms that submit requests to your API, forcing actions under the user's logged-in session.
* **Key Concepts**:
  - *Cross-Site Request Forgery*: Exploits cookie auto-attachment by sending requests (e.g. password resets or bank transfers) from malicious domains on behalf of authenticated users.
  - *SameSite Cookie Flags*: Setting `sameSite: 'lax'` or `sameSite: 'strict'` tells browsers to withhold session cookies on cross-origin subrequests, blocking CSRF at the browser level.
  - *Synchronizer Token Pattern*: The server issues a random token, which is stored in a cookie. For state-changing requests, the client must return this token in a custom header (e.g. `X-CSRF-Token`). The server compares the two values.

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

* **Why It Exists**: Exposing inputs without sanitization lets attackers store executable scripts (Stored XSS) or reflect them via queries (Reflected XSS), running code inside user browsers to steal cookies and log keystrokes.
* **Key Concepts**:
  - *HTML Escaping*: Translates characters into entities (e.g., `<` to `&lt;`, `>` to `&gt;`) to render inputs as literal strings, neutralizing execution.
  - *HttpOnly Cookies*: Setting the `HttpOnly` flag on cookies blocks client-side JavaScript access (`document.cookie`), protecting session tokens from XSS theft.
  - *Content Security Policy*: Enables defining strict script source whitelists and blocking inline scripts to prevent injected script execution.

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


