# HTTP/HTTPS Internals

> 📌 **File:** 03_HTTP_HTTPS_Internals.md | **Level:** Full-Stack Dev → Networking Expert

---

## What is it?

HTTP (Hypertext Transfer Protocol) is the application-layer protocol for the web. Every REST API endpoint, JSON payload, and page load is an HTTP transaction. HTTPS is HTTP running over TLS encryption. Understanding headers, methods, status codes, and HTTP/1.1 vs HTTP/2 vs HTTP/3 is critical for API design and performance.

---

## Map it to MY STACK (CRITICAL)

```
Browser (React) ──► HTTPS ──► CloudFront/ALB ──► HTTP ──► Node.js (Express)

CORS (browser restriction):
  Browser checks headers: Access-Control-Allow-Origin
  Managed in Express: app.use(cors())

HTTP Headers you must use:
  - Authorization: Bearer <JWT>   (Auth token)
  - Content-Type: application/json (JSON payload)
  - Cache-Control: max-age=3600    (Browser caching)
  - X-Request-ID: <UUID>           (Distributed tracing)
```

---

## HTTP Protocol Versions

```
┌──────────────────────────────────────────────────────────────────┐
│  HTTP Version History & Evolution                                │
├──────────────────────────────────────────────────────────────────┤
│  HTTP/1.1 (1997)                                                 │
│  ├── Simple text-based protocol                                  │
│  ├── Keep-Alive: Reuses single TCP connection for multiple reqs  │
│  └── Head-of-line blocking (requests must be processed in order) │
│                                                                  │
│  HTTP/2 (2015)                                                   │
│  ├── Binary-based (not text)                                     │
│  ├── Multiplexing: Multiple requests/responses over one TCP conn │
│  └── Header compression (HPACK)                                  │
│                                                                  │
│  HTTP/3 (2022)                                                   │
│  ├── Runs over UDP (using QUIC protocol)                         │
│  ├── Bypasses TCP handshakes, faster start                       │
│  └── Stream-level multiplexing (no TCP head-of-line blocking)    │
└──────────────────────────────────────────────────────────────────┘
```

#### Diagram Explanation (The Highway Traffic)
- **HTTP/1.1 (Single-lane road):** One car (request) must drive to the end and return before the next car can leave. If a slow truck (large image query) gets stuck, all traffic stops (`Head-of-Line Blocking`).
- **HTTP/2 (Multi-lane highway):** Multiple cars can drive side-by-side on the same road (TCP connection). But if the highway bridge collapses (TCP packet drop), all traffic on all lanes stops.
- **HTTP/3 (Flying cars over UDP):** Each request flies independently. If one car crashes, it has zero impact on the others. No bridge collapses, no traffic jams!

---

## Node.js Implementation

```javascript
const express = require('express');
const app = express();

// Parse JSON body (handles Content-Type: application/json)
app.use(express.json());

// ──── CORS Setup ────
app.use((req, res, next) => {
  res.setHeader('Access-Control-Allow-Origin', 'https://myapp.com');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  res.setHeader('Access-Control-Allow-Credentials', 'true');
  
  // Handle OPTIONS preflight request
  if (req.method === 'OPTIONS') {
    return res.sendStatus(200);
  }
  next();
});

// ──── Routes ────
app.get('/api/users/profile', (req, res) => {
  // Read custom header (X-Request-ID)
  const requestId = req.header('X-Request-ID');
  
  // Set cache control headers
  res.setHeader('Cache-Control', 'private, no-store, must-revalidate');
  res.setHeader('X-Response-Time', '5ms');
  
  res.json({
    id: 123,
    email: 'john@example.com',
    requestId
  });
});

app.listen(3000, () => console.log('HTTP Server listening on port 3000'));
```

---

## Commands & Diagnostics

```bash
# Inspect raw HTTP response headers
curl -I https://api.github.com

# Fetch and print headers + body
curl -v https://api.github.com/users/octocat

# Post JSON to API
curl -X POST https://api.myapp.com/api/login \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","password":"securePassword"}'

# Test OPTIONS preflight request (CORS test)
curl -X OPTIONS https://api.myapp.com/api/users \
  -H "Origin: https://another-origin.com" \
  -H "Access-Control-Request-Method: GET" -i
```

---

## Common Mistakes

### ❌ Caching Dynamic API Responses

```javascript
// ❌ Browser caches profile data. User logs out, another logs in:
// Browser shows OLD user profile!
app.get('/api/profile', (req, res) => {
  res.json(req.user); // Express default is no caching, but proxies might cache it!
});

// ✅ Explicitly disable caching for dynamic endpoints
app.get('/api/profile', (req, res) => {
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, private');
  res.json(req.user);
});
```

### ❌ Sending Large payloads without Compression

```javascript
// ❌ 500KB JSON response sent raw (slows down mobile networks)

// ✅ Enable Gzip/Brotli compression in Nginx or Express middleware
const compression = require('compression');
app.use(compression()); // Compress all responses > 1KB
```

---

## Practice Exercises

### Exercise 1: CORS Failure
Write an Express server that rejects calls from origins other than `localhost`. Create a local HTML page that attempts to fetch from it, and observe the CORS error in Chrome Console.

### Exercise 2: Timing Audit
Use `curl -v` on three different websites. Document: HTTP protocol version used (HTTP/1.1 vs HTTP/2 vs HTTP/3), response size, and timing headers.

### Exercise 3: Compression Test
Measure the size of a 1000-row JSON response in Chrome DevTools Network Tab with Gzip enabled vs disabled. Record the bandwidth savings.

---

## Interview Q&A

**Q1: What is a preflight request in CORS?**
> An HTTP OPTIONS request sent by the browser before the main request. It checks if the server allows the origin and method of the planned request. If the server approves, the browser sends the actual request (GET, POST).

**Q2: What is the difference between HTTP/1.1 and HTTP/2?**
> HTTP/1.1 is text-based and processes requests sequentially (head-of-line blocking). HTTP/2 is binary-based and introduces multiplexing (multiple concurrent requests over a single TCP connection) and header compression (HPACK).

**Q3: How does HTTP/3 improve page load times?**
> By running over UDP using the QUIC protocol. It reduces connection establishment time (combines TCP + TLS handshakes) and eliminates TCP head-of-line blocking (packet loss in one stream doesn't stall other streams).

**Q4: Explain the difference between `Cache-Control: no-cache` and `no-store`.**
> `no-cache` tells the browser it can cache the response but must validate it with the server (using ETag) before reusing it. `no-store` instructs the browser to never cache the response at all (necessary for private/sensitive data).

**Q5: What is HTTP Head-of-Line Blocking and how was it solved?**
> In HTTP/1.1, a TCP connection can only handle one request at a time. If a request is slow, all subsequent requests behind it are blocked. Solved in HTTP/2 by multiplexing, which allows sending multiple requests concurrently on the same connection.

---

Prev : [02 How The Internet Actually Works](./02_How_The_Internet_Actually_Works.md) | Index: [00 Index](./00_Index.md) | Next : [04 DNS Deep Dive](./04_DNS_Deep_Dive.md)
