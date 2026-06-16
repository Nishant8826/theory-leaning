# HTTP Module

All Node.js web frameworks (Express, Fastify, Nest.js) are built on top of the native `http` module. If you only understand framework wrappers, you will struggle to debug low-level network issues like socket timeouts, header manipulation errors, or raw stream parsing errors in production.

### The HTTP Module and TCP Sockets
The `http` module sits on top of Node's native TCP network module (`net`). When you create an HTTP server, Node binds a TCP socket to a network port and listens for incoming data. When a client sends an HTTP request, Node parses the raw TCP text stream, builds `req` (an instance of `IncomingMessage`) and `res` (an instance of `ServerResponse`), and runs your connection handler callback.

### Stream-based Request and Response Lifecycle
* **`IncomingMessage` (req)**: A **Readable Stream**. It emits `data` events as HTTP request body bytes arrive from the network card, and an `end` event once the request body has been fully received.
* **`ServerResponse` (res)**: A **Writable Stream**. When you call `res.write(chunk)`, Node writes raw bytes directly to the underlying TCP socket. Calling `res.end()` completes the write cycle and closes the TCP connection (unless keep-alive is active).

## Deep Dive

### Resolving Request Headers
Request headers are parsed automatically by Node's C++ parser and exposed as a simple key-value object on `req.headers`. All header keys are converted to lowercase (e.g. `User-Agent` becomes `req.headers['user-agent']`). This standardizes header parsing and avoids cross-browser issues.

### Writing Response Headers
You write response status codes and headers using:
* **`res.writeHead(statusCode, headers)`**: Sends the status and headers to the client immediately. Once called, you can no longer modify headers.
* **`res.setHeader(name, value)`**: Queues headers in memory. They are written automatically when the first call to `res.write()` or `res.end()` is executed. This allows you to update headers dynamically during request processing.

## Visual Explanation

### Request-Response Stream Architecture
```text
  [ Client Browser ] ─── TCP Text stream (GET / HTTP/1.1) ───> [ Node.js TCP Socket ]
                                                                      │
                                                                      ▼ (C++ Parser)
                                                           [ http.IncomingMessage ]
                                                               (Readable Stream)
                                                                      │
                                                                      ▼ (Trigger Callback)
                                                           [ HTTP connection handler ]
                                                               (Your JavaScript Code)
                                                                      │
                                                                      ▼ (Write output)
                                                           [ http.ServerResponse ]
                                                               (Writable Stream)
                                                                      │
  [ Client Browser ] <─── TCP Bytes (HTTP/1.1 200 OK) <───────────────┘
```

## Real-World Example
Consider parsing an API key from incoming requests. In a raw HTTP server, you query the lowercased header mapping `req.headers['x-api-key']`. If the header is missing, you return a `401 Unauthorized` status using `res.writeHead(401)` and close the write stream with `res.end()`.

## Code Examples

### Native HTTP Server with Routing and Body Parsing

```javascript
// native-server.js
const http = require('http');
const url = require('url');

const server = http.createServer((req, res) => {
  // 1. Parse URL and Query parameters
  const parsedUrl = url.parse(req.url, true);
  const path = parsedUrl.pathname;
  const method = req.method.toUpperCase();

  console.log(`[REQUEST] ${method} ${path}`);

  // 2. Simple Routing Table
  if (path === '/api/info' && method === 'GET') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ status: 'active', platform: process.platform }));
    return;
  }

  if (path === '/api/data' && method === 'POST') {
    let body = '';
    
    // Parse incoming request body stream
    req.on('data', (chunk) => {
      body += chunk.toString();
    });

    req.on('end', () => {
      try {
        const payload = JSON.parse(body);
        res.writeHead(201, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ message: 'Data received', payload }));
      } catch (err) {
        res.writeHead(400, { 'Content-Type': 'text/plain' });
        res.end('Invalid JSON payload');
      }
    });
    return;
  }

  // 3. Fallback route for 404s
  res.writeHead(404, { 'Content-Type': 'text/plain' });
  res.end('Path not found');
});

const PORT = 3000;
server.listen(PORT, () => {
  console.log(`HTTP Server running on port ${PORT}`);
});
```

## Best Practices
* **Always End Responses**: Ensure your code path always calls `res.end()` (or sends a response). If a route fails to end the write stream, the client socket remains open indefinitely, leading to resource leaks.
* **Handle Stream Errors**: Attach error listeners to the `req` and `res` streams to prevent unhandled socket disconnect errors from crashing your process.
* **Keep Headers Lowercase**: When reading incoming headers, always query them using lowercase keys (`req.headers['authorization']`).

## Interview Questions

**Q:** What native Node.js module is used to create a web server?

> **Answer:**
> The native `http` module is used to create and manage web servers via its `http.createServer()` method.

**Q:** Why are HTTP request header keys accessed in lowercase inside Node.js?

> **Answer:**
> The HTTP specification declares headers to be case-insensitive. To simplify parsing and prevent developers from needing to handle variations (like `Content-Type` vs `content-type`), Node's internal parser automatically converts all incoming header keys to lowercase.

**Q:** Explain how incoming request body data is parsed in a raw HTTP server without frameworks, referencing streams.

> **Answer:**
> The `req` parameter passed to the `createServer` callback is an instance of `http.IncomingMessage`, which is a Readable Stream. Since request payloads (like large JSON payloads or file uploads) arrive in chunks, you must listen to the `'data'` event to accumulate the chunks into a buffer or string, and then parse the full payload once the `'end'` event fires:
> ```javascript
> let body = '';
> req.on('data', chunk => body += chunk.toString());
> req.on('end', () => {
> const data = JSON.parse(body);
> });
> ```

**Q:** In a high-throughput raw HTTP backend, what socket-level optimizations can you implement to maximize concurrent requests, and what are the trade-offs of toggling `keepAlive`?

> **Answer:**
> To optimize low-level network performance:
> 1. **Configure Keep-Alive**: Enable `keepAlive` on the HTTP Agent. This keeps TCP connections open across multiple requests, eliminating the CPU and latency overhead of setting up and tearing down TCP connections for each request.
> 2. **Set Socket Timeouts**: Configure socket timeouts (`server.keepAliveTimeout` and `server.headersTimeout`) to close idle sockets quickly, preventing slow-loris attacks and freeing up file descriptors.
> 3. **Tune Backlog Limit**: Adjust the socket connection queue size limit (using the `backlog` parameter in `server.listen(port, hostname, backlog)`) to handle larger bursts of connections.
> *Trade-off*: While keep-alive improves latency and throughput for active clients, holding sockets open consumes system memory and file descriptors. If there are many idle clients, this can exhaust server resources, requiring careful configuration of idle timeout thresholds.

---
Previous : [20_Async_Await.md](20_Async_Await.md) | Index : [00_index.md](00_index.md) | Next : [22_Creating_Web_Servers.md](22_Creating_Web_Servers.md)
