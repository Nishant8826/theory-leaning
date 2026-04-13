# HTTP/HTTPS Internals

> 📌 **File:** 06_HTTP_HTTPS_Internals.md | **Level:** Full-Stack Dev → Networking Expert

---

## What is it?

HTTP (HyperText Transfer Protocol) is the application-layer protocol your entire stack runs on. Every `fetch()`, every API call, every page load, every S3 operation — all HTTP. HTTPS is HTTP encrypted with TLS. Understanding HTTP internals means understanding why your API is slow, why CORS errors happen, and how caching works.

---

## Map it to MY STACK (CRITICAL)

```
┌──────────────────────────────────────────────────────────────────────┐
│  Your Code                    │ HTTP Reality                        │
├───────────────────────────────┼─────────────────────────────────────┤
│  fetch('/api/users')          │ GET /api/users HTTP/1.1             │
│  axios.post('/api/orders', d) │ POST /api/orders HTTP/1.1 + body   │
│  res.json({...})              │ 200 OK + Content-Type: app/json    │
│  res.status(404)              │ 404 Not Found                       │
│  next/image (Next.js)         │ GET /image.webp + Accept: image/*  │
│  Express static middleware    │ GET /bundle.js + ETag caching       │
│  AWS S3 getObject             │ GET /bucket/key HTTP/1.1            │
│  CORS error in browser        │ OPTIONS preflight + Access-Control  │
│  Cookie auth                  │ Set-Cookie / Cookie headers         │
│  JWT auth                     │ Authorization: Bearer <token>       │
└───────────────────────────────┴─────────────────────────────────────┘
```

---

## How does it actually work?

### HTTP Request Anatomy

```
GET /api/products?category=electronics&limit=20 HTTP/1.1    ← Request line
Host: api.myapp.com                                          ← Required header
Accept: application/json                                      ← What client wants
Accept-Encoding: gzip, deflate, br                           ← Compression support
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...               ← JWT token
Cookie: sessionId=abc123; theme=dark                         ← Cookies
User-Agent: Mozilla/5.0 ... Chrome/120                       ← Browser info
Connection: keep-alive                                        ← Reuse TCP connection
Cache-Control: no-cache                                       ← Skip cache
X-Request-ID: uuid-1234                                       ← Custom correlation ID
                                                              ← Empty line (end of headers)
                                                              ← No body for GET
```

### HTTP Response Anatomy

```
HTTP/1.1 200 OK                                              ← Status line
Content-Type: application/json; charset=utf-8                ← Response type
Content-Length: 1523                                          ← Body size in bytes
Content-Encoding: gzip                                       ← Compressed
Cache-Control: public, max-age=300                           ← Cache for 5 min
ETag: "abc123def456"                                         ← Content fingerprint
X-Request-ID: uuid-1234                                      ← Echo correlation ID
X-Response-Time: 45ms                                        ← Server processing time
Set-Cookie: sessionId=xyz789; HttpOnly; Secure; SameSite=Lax← Set a cookie
Access-Control-Allow-Origin: https://myapp.com               ← CORS
Strict-Transport-Security: max-age=31536000                  ← Force HTTPS
                                                              ← Empty line
{"products": [{"id": 1, "name": "Laptop"}, ...]}           ← JSON body
```

### HTTP Methods in Your Stack

```
┌────────┬───────────────────────────────────────────────────────────┐
│ Method │ Your Usage                                                │
├────────┼───────────────────────────────────────────────────────────┤
│ GET    │ fetch('/api/products') — read data, no body              │
│ POST   │ fetch('/api/orders', {method:'POST', body}) — create     │
│ PUT    │ fetch('/api/products/1', {method:'PUT', body}) — replace │
│ PATCH  │ fetch('/api/products/1', {method:'PATCH', body}) — update│
│ DELETE │ fetch('/api/products/1', {method:'DELETE'}) — remove     │
│ OPTIONS│ Browser CORS preflight — automatic, you don't send this │
│ HEAD   │ curl -I — headers only, no body (check if resource exists)│
└────────┴───────────────────────────────────────────────────────────┘
```

### Status Codes You Must Know

```
┌──────┬───────────────────────────────────────────────────────────────┐
│ Code │ Meaning + When You See It                                     │
├──────┼───────────────────────────────────────────────────────────────┤
│ 200  │ OK — successful GET/PUT/PATCH                                 │
│ 201  │ Created — successful POST (new resource)                      │
│ 204  │ No Content — successful DELETE (no body returned)             │
│ 301  │ Moved Permanently — HTTP → HTTPS redirect, old URL           │
│ 302  │ Found (temporary redirect) — login redirects                  │
│ 304  │ Not Modified — cache is valid, use local copy (ETag match)   │
│ 400  │ Bad Request — validation error (malformed JSON, missing field)│
│ 401  │ Unauthorized — no/invalid JWT token                          │
│ 403  │ Forbidden — valid token but insufficient permissions          │
│ 404  │ Not Found — wrong URL or deleted resource                    │
│ 405  │ Method Not Allowed — POST to a GET-only endpoint             │
│ 409  │ Conflict — duplicate email, version conflict                  │
│ 413  │ Payload Too Large — file upload too big                      │
│ 429  │ Too Many Requests — rate limited                             │
│ 500  │ Internal Server Error — unhandled exception in Node.js       │
│ 502  │ Bad Gateway — Nginx/ALB can't reach your Node.js server     │
│ 503  │ Service Unavailable — server overloaded or in maintenance    │
│ 504  │ Gateway Timeout — your API took too long (ALB timeout)      │
└──────┴───────────────────────────────────────────────────────────────┘
```

---

## HTTP/1.1 vs HTTP/2 vs HTTP/3

```
┌──────────────────────────────────────────────────────────────────────┐
│  Feature            │ HTTP/1.1       │ HTTP/2          │ HTTP/3     │
├─────────────────────┼────────────────┼─────────────────┼────────────┤
│  Multiplexing       │ ❌ 1 req/conn  │ ✅ Many req/conn│ ✅ Yes     │
│  Header compression │ ❌ None        │ ✅ HPACK        │ ✅ QPACK   │
│  Server push        │ ❌ None        │ ✅ Supported    │ ❌ Removed │
│  Transport          │ TCP            │ TCP             │ QUIC (UDP) │
│  Head-of-line block │ ✅ Per conn    │ ⚠️ TCP level    │ ❌ None    │
│  Connection setup   │ TCP + TLS      │ TCP + TLS       │ 0-1 RTT   │
│  Browser support    │ All            │ All modern      │ ~95%       │
├─────────────────────┴────────────────┴─────────────────┴────────────┤
│                                                                      │
│  For YOUR React/Next.js app:                                        │
│  - Nginx/ALB serve HTTP/2 by default (if HTTPS enabled)             │
│  - Your Node.js talks HTTP/1.1 internally (fine over localhost/VPC) │
│  - CloudFront supports HTTP/3 (enabled in distribution settings)    │
│                                                                      │
│  HTTP/2 impact: Your React app loads 30-50% faster because         │
│  JS bundles, CSS, images are multiplexed over ONE connection        │
│  instead of opening 6 parallel connections (HTTP/1.1 limit).       │
└──────────────────────────────────────────────────────────────────────┘
```

### HTTP/1.1 vs HTTP/2 — Visual

```
HTTP/1.1 (6 connections max per domain):
Connection 1: ──[index.html]──────────────[idle]──────────────
Connection 2: ──[style.css]───────────────[idle]──────────────
Connection 3: ──[bundle.js]──────────────────────[idle]───────
Connection 4: ──[image1.jpg]─────────────────────────[idle]───
Connection 5: ──[image2.jpg]─────────────[idle]───────────────
Connection 6: ──[font.woff2]─────────────[idle]───────────────
Waiting:       ❌ image3.jpg (must wait for a free connection)

HTTP/2 (ONE connection, multiplexed):
Connection 1: ──[html][css][js][img1][img2][img3][font]───────
              All requests happen simultaneously on ONE TCP connection
              No waiting, no head-of-line blocking at HTTP level
```

---

## CORS — The Error Every Dev Hits

```javascript
// Browser error:
// Access to fetch at 'https://api.myapp.com' from origin 'https://myapp.com'
// has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header

// WHY: Same-Origin Policy prevents cross-origin requests by default
// React (localhost:3000) → API (localhost:8080) = DIFFERENT origin = blocked

// CORS flow:
// 1. Browser sends OPTIONS preflight (for POST/PUT/DELETE):
//    OPTIONS /api/orders
//    Origin: https://myapp.com
//    Access-Control-Request-Method: POST
//    Access-Control-Request-Headers: Content-Type, Authorization

// 2. Server responds with allowed origins:
//    Access-Control-Allow-Origin: https://myapp.com
//    Access-Control-Allow-Methods: GET, POST, PUT, DELETE
//    Access-Control-Allow-Headers: Content-Type, Authorization
//    Access-Control-Max-Age: 86400  (cache preflight for 24h)

// 3. Browser sends actual request (if preflight passed)

// Express CORS setup:
const cors = require('cors');

// ❌ Too permissive (allows everything)
app.use(cors());

// ✅ Production CORS
app.use(cors({
  origin: ['https://myapp.com', 'https://admin.myapp.com'],
  methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: true,  // Allow cookies
  maxAge: 86400       // Cache preflight for 24 hours
}));
```

---

## HTTP Caching

```
┌──────────────────────────────────────────────────────────────────┐
│  Header                │ What it does                            │
├────────────────────────┼────────────────────────────────────────┤
│  Cache-Control:        │                                         │
│    no-store            │ Never cache (sensitive data)            │
│    no-cache            │ Cache but revalidate every time         │
│    public, max-age=300 │ Cache for 5 min (CDN + browser)        │
│    private, max-age=60 │ Cache for 60s (browser only, not CDN)  │
│    immutable           │ Never changes (versioned JS bundles)   │
│                        │                                         │
│  ETag: "abc123"        │ Content fingerprint (like a hash)      │
│                        │ Browser sends If-None-Match: "abc123"  │
│                        │ Server returns 304 if unchanged        │
│                        │                                         │
│  Last-Modified: date   │ When content last changed              │
│                        │ Browser sends If-Modified-Since: date  │
│                        │ Server returns 304 if unchanged         │
└────────────────────────┴────────────────────────────────────────┘
```

### Caching Strategy for Your Stack

```javascript
// Static assets (Next.js build output) — immutable, long cache
app.use('/static', express.static('public', {
  maxAge: '1y',            // Cache for 1 year
  immutable: true,         // Never revalidate
  etag: false              // Not needed with immutable
}));
// URL: /static/bundle.abc123.js (hash in filename = cache busting)

// API responses — short cache or no cache
app.get('/api/products', (req, res) => {
  res.set('Cache-Control', 'public, max-age=60');  // CDN + browser: 60s
  res.set('Vary', 'Accept-Encoding');               // Different cache per encoding
  res.json(products);
});

// User-specific data — private cache only
app.get('/api/profile', auth, (req, res) => {
  res.set('Cache-Control', 'private, max-age=0');  // Don't cache in CDN
  res.json(req.user);
});

// Sensitive data — never cache
app.get('/api/payments', auth, (req, res) => {
  res.set('Cache-Control', 'no-store');  // Never cache anywhere
  res.json(payments);
});
```

---

## Node.js Implementation — Custom HTTP Insights

```javascript
const express = require('express');
const app = express();

// ──── Request/Response Timing Middleware ────
app.use((req, res, next) => {
  req.startTime = Date.now();
  
  // Log request details
  console.log(`→ ${req.method} ${req.url}`);
  console.log(`  Host: ${req.headers.host}`);
  console.log(`  Content-Type: ${req.headers['content-type'] || 'none'}`);
  console.log(`  Connection: ${req.headers.connection}`);
  console.log(`  Accept-Encoding: ${req.headers['accept-encoding']}`);
  
  // Capture response
  const originalEnd = res.end;
  res.end = function(...args) {
    const duration = Date.now() - req.startTime;
    res.set('X-Response-Time', `${duration}ms`);
    res.set('X-Request-ID', req.headers['x-request-id'] || crypto.randomUUID());
    console.log(`← ${res.statusCode} (${duration}ms, ${res.get('Content-Length') || '?'} bytes)\n`);
    originalEnd.apply(res, args);
  };
  
  next();
});

// ──── Compression ────
const compression = require('compression');
app.use(compression({
  threshold: 1024,        // Only compress responses > 1KB
  filter: (req, res) => { // Don't compress SSE or WebSocket
    if (req.headers['accept'] === 'text/event-stream') return false;
    return compression.filter(req, res);
  }
}));

// ──── Security Headers ────
app.use((req, res, next) => {
  res.set({
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'DENY',
    'X-XSS-Protection': '1; mode=block',
    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
    'Referrer-Policy': 'strict-origin-when-cross-origin'
  });
  next();
});

app.listen(3000);
```

---

## Commands & Debugging Tools

```bash
# Full HTTP request/response
curl -v https://api.myapp.com/api/health
# Shows: > (request), < (response), * (connection info)

# Only response headers
curl -I https://api.myapp.com/api/health

# Send POST with JSON
curl -X POST https://api.myapp.com/api/orders \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"productId": "123", "quantity": 1}'

# Check HTTP/2 support
curl --http2 -I https://api.myapp.com

# Check compression
curl -H "Accept-Encoding: gzip" -I https://api.myapp.com/api/products
# Look for: Content-Encoding: gzip

# Check caching headers
curl -I https://api.myapp.com/api/products
# Look for: Cache-Control, ETag, Last-Modified

# Test CORS preflight
curl -X OPTIONS https://api.myapp.com/api/products \
  -H "Origin: https://myapp.com" \
  -H "Access-Control-Request-Method: POST" -v
```

---

## Performance Insight

```
┌──────────────────────────────────────────────────────────────────┐
│  HTTP Optimization Checklist                                     │
├──────────────────────────────────────────────────────────────────┤
│  1. Enable HTTP/2 on Nginx/ALB (multiplexing)                  │
│  2. Enable gzip/brotli compression (60-80% size reduction)     │
│  3. Set Cache-Control headers (reduce requests)                 │
│  4. Use ETags for conditional requests (save bandwidth)         │
│  5. Keep-alive connections (avoid TCP handshake per request)    │
│  6. Minimize cookies (sent on EVERY request to that domain)    │
│  7. Use CDN for static assets (reduce latency)                  │
│  8. Batch API calls (reduce round trips)                        │
│  9. Use 204 for DELETE (no body = faster)                       │
│ 10. Prefetch/preconnect for known external APIs                 │
└──────────────────────────────────────────────────────────────────┘
```

---

## Common Mistakes

### ❌ Not Enabling Compression

```javascript
// Without compression: 500KB JSON response
// With gzip: ~100KB (80% reduction!)
// With brotli: ~80KB (84% reduction!)

// ✅ Always use compression middleware
const compression = require('compression');
app.use(compression());
```

### ❌ CORS Wildcard in Production

```javascript
// ❌ Allows ANY website to call your API
app.use(cors({ origin: '*' }));

// ✅ Whitelist your domains
app.use(cors({ origin: ['https://myapp.com'] }));
```

### ❌ Not Setting Proper Status Codes

```javascript
// ❌ Everything returns 200
app.post('/api/users', (req, res) => {
  res.json({ error: 'Email already exists' }); // 200 with error message
});

// ✅ Use proper status codes
app.post('/api/users', (req, res) => {
  res.status(409).json({ error: 'Email already exists' }); // 409 Conflict
});
```

---

## Interview Q&A

**Q1: What's the difference between HTTP/1.1 and HTTP/2?**
> HTTP/2 multiplexes multiple requests over a single TCP connection (vs 6 parallel connections in HTTP/1.1). It compresses headers with HPACK, supports server push, and uses binary framing. Result: 30-50% faster page loads for resource-heavy pages.

**Q2: How does HTTP caching work with ETags?**
> Server returns ETag (content hash) with response. Browser stores response + ETag. On next request, browser sends `If-None-Match: <etag>`. If content unchanged, server returns 304 (no body) — saves bandwidth. If changed, server returns 200 with new content and new ETag.

**Q3: Why do CORS errors only happen in browsers?**
> Same-Origin Policy is enforced by browsers, not servers. `curl`, Postman, and server-to-server requests don't check CORS. Browsers send an OPTIONS preflight for cross-origin requests; the server must respond with appropriate `Access-Control-*` headers.

**Q4: What causes a 502 Bad Gateway?**
> The reverse proxy (Nginx/ALB) cannot reach your backend (Node.js). Causes: Node.js crashed, wrong port, firewall blocking, health check failing. The proxy received the client's request but couldn't forward it.

**Q5: When would you use HTTP/3 over HTTP/2?**
> HTTP/3 uses QUIC (UDP) instead of TCP. It eliminates TCP head-of-line blocking, reduces connection setup time (0-RTT), and handles network switches better (WiFi→cellular). Best for mobile users with unstable connections. CloudFront supports it — enable in distribution settings.


Prev : [05 DNS Deep Dive](./05_DNS_Deep_Dive.md) | Index: [0 Index](./0_Index.md) | Next : [07 TCP Deep Dive](./07_TCP_Deep_Dive.md)
