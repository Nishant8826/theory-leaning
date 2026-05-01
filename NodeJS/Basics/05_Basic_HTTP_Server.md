# 📌 Topic: Basic HTTP Server Internals

## What
### 🧠 Concept Explanation
At its core, a Node.js HTTP server is a specialized **Event Emitter** that listens for network traffic and translates it into something JavaScript can understand.

**The Post Office Analogy (Deep Dive):**
Imagine a Post Office where one worker (the Main Thread) is responsible for handling all incoming mail.
*   **The Window (The Port):** The server "listens" at a specific window (e.g., Port 3000). If mail arrives at Port 80, this worker won't see it.
*   **The Envelope (The TCP Packet):** Data arrives in small chunks. The OS gathers these chunks and hands a complete "envelope" to Node.js.
*   **The Request (The Letter):** Inside the envelope is a letter written in a specific format (HTTP). Node.js reads the "Header" (who it's from, what they want) and the "Body" (the actual content).
*   **The Processing:** The worker looks at the letter, performs the requested task (maybe checking a database), and then writes a reply.
*   **The Response (The Return Mail):** The reply is sent back through the same window.

Because Node.js is non-blocking, the worker can handle a second person's letter while waiting for the database to return information for the first person's request.

---

### 🏗️ Mental Model
The `http` module is a high-level abstraction built on top of the `net` module (TCP). 
1.  **IncomingMessage (`req`):** This is a **Readable Stream**. It represents the data coming *from* the client. Since it's a stream, for large uploads, you don't get the whole body at once; you get it in "chunks."
2.  **ServerResponse (`res`):** This is a **Writable Stream**. It represents the data going *to* the client. You can "pipe" data into it (like a file stream) or "write" to it multiple times before finally "ending" it.

---

## Why
### 🏢 Best Practices
1.  **Always use `res.end()`:** Or use a framework like Express that does it for you.
2.  **Set Timeouts:** Use `server.setTimeout()` to prevent slow-loris attacks or hung connections.
3.  **Validate Content-Length:** To prevent large payload attacks.

---

### ⚖️ Trade-offs
*   **Pros:** Extremely fast, minimal overhead, full control over headers and streams.
*   **Cons:** Very verbose for complex routing, hard to maintain without a framework.

---

## How
### ⚡ Actual Behavior
When you run a server, the following happens for every single request:
1.  **Connection Establishment:** A client (like Chrome) initiates a connection. The OS handles the low-level handshake.
2.  **The 'request' Event:** Once the HTTP headers are fully parsed, the server emits a `'request'` event. This triggers your callback function.
3.  **Parsing:** The raw text `GET /index.html HTTP/1.1` is converted into the `req.method` and `req.url` properties.
4.  **Backpressure:** If the client is slow to receive data, Node.js pauses the stream to prevent memory from filling up with data that hasn't been sent yet. This is called "Backpressure management."
5.  **Termination:** The connection remains open (if using Keep-Alive) until either the client or the server explicitly closes it.

---

### 🔬 Internal Mechanics (V8 + libuv + OS)
*   **llhttp (The Parser):** HTTP parsing is complex and must be extremely fast. Node.js uses **llhttp**, a parser written in C (originally translated from TypeScript-like code), which is significantly faster than parsing strings in pure JavaScript.
*   **Sockets and File Descriptors:** In the eyes of the OS (especially Linux/macOS), every connection is a "File Descriptor." Node.js uses Libuv to monitor these descriptors. When data arrives, Libuv tells V8: "Hey, there's data ready on FD #12," and V8 runs the corresponding JS code.
*   **Zero-Copy (Optimizations):** In some cases, Node.js tries to move data directly from a file to a network socket without copying it into the "JavaScript space" (V8 Heap), which saves massive amounts of CPU and memory.
*   **Header Validation:** Node.js enforces strict limits on header sizes (usually 8KB-16KB) to prevent "Denial of Service" (DoS) attacks where a malicious client sends an infinite header.

---

### 🔁 Execution Flow
1.  `http.createServer()` creates a new `Server` instance.
2.  `.listen(3000)` tells the OS to start accepting connections.
3.  Client sends `GET / HTTP/1.1`.
4.  OS notifies Libuv -> Libuv notifies Node.js.
5.  llhttp parses the header.
6.  `request` callback is triggered with `req` and `res`.

---

### 🔍 Code Example (Latest Node.js)
```javascript
import http from 'node:http';

const server = http.createServer((req, res) => {
    // req: IncomingMessage (Readable Stream)
    // res: ServerResponse (Writable Stream)

    console.log(`Received ${req.method} request for ${req.url}`);

    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ message: "Hello from Low-Level Node.js" }));
});

server.listen(3000, () => {
    console.log("Server listening on http://localhost:3000");
});
```

---

## Impact
### 💥 Production Failures
*   **Memory Leaks via Requests:** If you attach a listener to `req` and never remove it, or if you keep a reference to `res` objects in a global array, memory will grow until the process crashes.
*   **Unfinished Responses:** Forgetting to call `res.end()` will keep the connection open until it times out, eventually exhausting the server's available sockets.

---

### 🧪 Real-time Scenarios
*   **Health Checks:** A simple `http` server in a microservice that just returns `200 OK` for a load balancer.
*   **Proxying:** Receiving a request and piping it directly to another server (e.g., a simple API gateway).

---

### ⚠️ Edge Cases
*   **Keep-Alive:** Modern browsers keep the TCP connection open for multiple HTTP requests. Node.js manages this automatically but it consumes a socket.
*   **Aborted Requests:** If the client closes the browser before the server finishes, you must handle the `close` event to stop expensive processing.

---

---

Prev: [04_Modules_CommonJS_ESM.md](./04_Modules_CommonJS_ESM.md) | Index: [NodeJS/00_Index.md](../00_Index.md) | Next: [../Intermediate/01_Event_Loop_Deep_Dive.md](../Intermediate/01_Event_Loop_Deep_Dive.md)
