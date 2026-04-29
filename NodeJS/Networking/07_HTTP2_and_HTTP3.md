# 📌 07 — HTTP/2 and HTTP/3: Multiplexing and QUIC Internals

## 🧠 Concept Explanation

### Basic → Intermediate
HTTP/2 is an evolution of HTTP/1.1 that allows multiple requests to be sent over a single TCP connection simultaneously. HTTP/3 replaces TCP with **QUIC** (built on UDP) to solve the "Head-of-Line Blocking" problem.

### Advanced → Expert
At a systems level, HTTP/2 is a **Binary Protocol**.
1. **Binary Framing**: Data is split into small "Frames" (HEADERS, DATA, SETTINGS).
2. **Streams**: Each request/response is a logical "Stream" with a unique ID.
3. **Multiplexing**: Frames from different streams can be interleaved on the same connection.
4. **HPACK**: A specialized compression algorithm for headers to save bandwidth.

HTTP/3 (QUIC) takes this further by implementing congestion control and reliability **at the application layer** (using UDP), allowing individual streams to continue even if one packet for a different stream is lost.

---

## 🏗️ Common Mental Model
"HTTP/2 is always faster."
**Correction**: HTTP/2 can be **slower** than HTTP/1.1 on high-loss networks (like mobile data). Because it uses a single TCP connection, one lost packet blocks **all** streams (TCP Head-of-Line Blocking). This is exactly why HTTP/3 was created.

---

## ⚡ Actual Behavior: Server Push
HTTP/2 allows the server to "push" resources (like CSS/JS) to the client's cache before the client even parses the HTML and asks for them. In Node.js, this is handled via the `stream.pushStream()` API.

---

## 🔬 Internal Mechanics (libuv + nghttp2)

### The nghttp2 Library
Node.js uses the **nghttp2** C library to handle the complex state machine of HTTP/2 framing and HPACK.

### Flow Control (WINDOW_UPDATE)
HTTP/2 has its own flow control mechanism on top of TCP. The client can tell the server: "I can only handle 64KB more of Stream 5." This prevents a slow client from being overwhelmed by a fast server.

---

## 📐 ASCII Diagrams

### Multiplexing in HTTP/2
```text
  TCP CONNECTION
  ┌─────────────────────────────────────────────────────────────┐
  │ [H: Stream 1] [D: Stream 3] [H: Stream 5] [D: Stream 1] ... │
  └─────────────────────────────────────────────────────────────┘
     (Frames from different requests are interleaved)
```

---

## 🔍 Code Example: HTTP/2 Server in Node.js
```javascript
const http2 = require('http2');
const fs = require('fs');

const server = http2.createSecureServer({
  key: fs.readFileSync('key.pem'),
  cert: fs.readFileSync('cert.pem')
});

server.on('stream', (stream, headers) => {
  // Push a CSS file to the client automatically
  if (headers[':path'] === '/') {
    stream.pushStream({ ':path': '/style.css' }, (err, pushStream) => {
      if (!err) {
        pushStream.respond({ ':status': 200, 'content-type': 'text/css' });
        pushStream.end('body { background: #eee; }');
      }
    });
  }

  stream.respond({
    'content-type': 'text/html; charset=utf-8',
    ':status': 200
  });
  stream.end('<h1>Hello HTTP/2</h1>');
});

server.listen(8443);
```

---

## 💥 Production Failures & Debugging

### Scenario: The "HPACK Bomb" (Security)
**Problem**: The server CPU spikes to 100% when receiving a specific request.
**Reason**: An attacker sends headers that exploit the HPACK dynamic table, forcing the server to spend excessive CPU decompressing recursive or massive header values.
**Fix**: Tune `maxSettings` and `maxHeaderListSize` in your HTTP/2 server config.

### Scenario: Browser Connection Limits
**Problem**: I have 200 parallel requests, but only 100 are moving.
**Reason**: Browsers and servers have a `SETTINGS_MAX_CONCURRENT_STREAMS` limit (often 100). Even with multiplexing, you can hit this limit.
**Fix**: Increase the limit in the server config or use multiple connections (though this defeats the purpose of H2).

---

## 🧪 Real-time Production Q&A

**Q: "Is HTTP/3 ready for Node.js production?"**
**A**: **It's experimental.** While you can use it (via the `quic` module or libraries like `undici`), most production systems still use a reverse proxy like **Nginx** or **Cloudflare** to handle HTTP/3 and proxy to Node via HTTP/1.1 or H2.

---

## 🏢 Industry Best Practices
- **Disable Server Push if not needed**: It is difficult to get right and can actually waste bandwidth if the client already has the resource cached.
- **Header Compression**: Ensure you aren't sending massive, redundant cookies that bloat the HPACK table.

---

## 💼 Interview Questions
**Q: How does HTTP/3 solve Head-of-Line (HOL) blocking?**
**A**: HTTP/2 uses TCP, where a single lost packet stops the whole stream. HTTP/3 uses QUIC (UDP), which handles reliability per-stream. If a packet for Stream A is lost, Stream B continues uninterrupted.

---

## 🧩 Practice Problems
1. Use `nghttp2` CLI tools or Chrome DevTools to inspect the binary frames of a website using HTTP/2.
2. Implement a benchmark comparing the performance of loading 100 small images via HTTP/1.1 vs HTTP/2.

---

**Prev:** [06_TLS_SSL_Deep_Dive.md](./06_TLS_SSL_Deep_Dive.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [08_DNS_and_Connection_Lifecycle.md](./08_DNS_and_Connection_Lifecycle.md)
