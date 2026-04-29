# 📌 01 — HTTP Server Internals: From TCP Stream to JS Objects

## 🧠 Concept Explanation

### Basic → Intermediate
The `http` module is built on top of the `net` module. It parses raw TCP streams into high-level JavaScript objects: `IncomingMessage` (Request) and `ServerResponse`.

### Advanced → Expert
At a staff level, we must understand the **Parsing Pipeline**. Node.js uses a highly optimized C parser called **llhttp** (replacing the older `http_parser`). 
1. **TCP Connection**: libuv accepts a new connection on a socket.
2. **Buffering**: Data arrives in chunks (Node.js Buffers).
3. **llhttp State Machine**: The C++ parser scans the buffer for headers, methods, and paths. 
4. **JS Objects Creation**: Once enough data is parsed, Node.js creates the `req` and `res` objects and emits the `'request'` event.

The critical performance factor here is the **Header Overhead**. Every header must be converted from a raw byte stream into a V8 String. Large numbers of headers or very large header values can block the event loop due to this conversion cost.

---

## 🏗️ Common Mental Model
"Express is my server."
**Correction**: Express is just a layer of middleware. The **real** server is `http.Server`. Every byte you send goes through the `http` module's internal stream management.

---

## ⚡ Actual Behavior: Keep-Alive
By default, Node.js HTTP/1.1 servers use **Persistent Connections (Keep-Alive)**. This means a single TCP connection can be reused for multiple HTTP requests. This significantly reduces the latency of the TCP/TLS handshake for repeat clients.

---

## 🔬 Internal Mechanics (V8 + libuv + syscalls)

### llhttp integration
The `llhttp` parser is a finite state machine generated from TypeScript-like descriptions into C. It is designed to be **Zero-Copy** as much as possible, referencing the original memory of the buffer instead of creating new strings until absolutely necessary.

### writev() syscall
When you call `res.end()`, Node.js might use the `writev` syscall to send multiple buffers (Headers + Body) in a single kernel transition, reducing the number of context switches.

---

## 📐 ASCII Diagrams

### The Request Lifecycle
```text
  1. NIC receives Packets ──▶ 2. Kernel Buffers ──▶ 3. libuv uv_read_start
                                                        │
     ┌──────────────────────────────────────────────────┘
     ▼
  4. Node.js C++ Binding (llhttp) ──▶ 5. Create 'req' / 'res' (JS)
                                               │
     ┌─────────────────────────────────────────┘
     ▼
  6. Express / App Logic (JS) ──▶ 7. res.write() ──▶ 8. writev() syscall
                                                        │
     ┌──────────────────────────────────────────────────┘
     ▼
  9. Kernel sends data to NIC
```

---

## 🔍 Code Example: Low-level HTTP Optimization
```javascript
const http = require('http');

// Optimizing for high-throughput
const server = http.createServer((req, res) => {
  // 1. Avoid large headers to reduce V8 string conversion cost
  // 2. Use streams for large bodies to keep RSS low
  req.pipe(process.stdout);
  
  res.writeHead(200, {
    'Content-Type': 'text/plain',
    'Connection': 'keep-alive'
  });
  
  res.end('Hello Internals');
});

// Configure internal limits to prevent DoS
server.maxHeadersCount = 100;
server.headersTimeout = 60000; // 60s
server.requestTimeout = 300000; // 5m

server.listen(8080);
```

---

## 💥 Production Failures & Debugging

### Scenario: The "Hanging" Request
**Problem**: Users report that the site "freezes" indefinitely.
**Reason**: You have a request where you never call `res.end()` (e.g. an error path that forgot to send a response). The TCP connection stays open and the client waits forever.
**Debug**: Use `server.getConnections()` to monitor active connections. Use `lsof` to see open sockets.
**Fix**: Always ensure every path in your code ends with a response or a timeout handler.

### Scenario: Slow Header Parsing (Slowloris Attack)
**Problem**: CPU is low, but the server stops accepting new connections.
**Reason**: An attacker is sending headers very slowly (1 byte every few seconds). Node.js's `llhttp` is waiting for the end of the headers, occupying a socket and internal handle.
**Fix**: Tune `server.headersTimeout` and `server.requestTimeout`.

---

## 🧪 Real-time Production Q&A

**Q: "Is it faster to send one large `res.end(bigBuffer)` or multiple `res.write(chunk)`?"**
**A**: One large `res.end()` is generally faster because it reduces the number of `write()` syscalls and V8 boundary crossings. However, for memory efficiency with large data, `res.write()` (streaming) is better.

---

## 🧪 Debugging Toolchain
- **`curl -v`**: Inspect raw headers and connection behavior.
- **`tcpdump` / `Wireshark`**: See the raw packets on the wire to debug TLS or TCP issues.

---

## 🏢 Industry Best Practices
- **Use a Reverse Proxy (Nginx/Envoy)**: Don't expose Node.js directly to the internet. Let Nginx handle slow clients, SSL termination, and buffering.
- **Limit Header Sizes**: Prevent memory attacks by limiting `maxHeaderSize`.

---

## 💼 Interview Questions
**Q: What is the purpose of the `res.flushHeaders()` method?**
**A**: It allows you to send the HTTP headers to the client immediately without waiting for the body content. This is useful for performance as it allows the browser to start downloading assets (CSS/JS) while the server is still generating the HTML.

---

## 🧩 Practice Problems
1. Implement a simple HTTP server using the `net` module (TCP) instead of the `http` module. Manually parse the GET request and send a raw HTTP response.
2. Monitor the `server.on('clientError')` event. What triggers it most frequently in your production environment?

---

**Prev:** [../Runtime/09_Process_Signals_and_Lifecycle.md](../Runtime/09_Process_Signals_and_Lifecycle.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [02_Express_Internals.md](./02_Express_Internals.md)
