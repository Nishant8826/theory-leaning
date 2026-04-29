# 📌 06 — CORS

## 🧠 Concept Explanation

CORS (Cross-Origin Resource Sharing) is a browser security mechanism that restricts how web pages make requests to different origins. An **origin** is: `protocol + hostname + port`. Requests crossing origins are blocked by default unless the server explicitly allows them via CORS headers.

CORS applies ONLY in browser contexts — Node.js, curl, Postman: no CORS restrictions.

## 🔬 Internal Mechanics (Blink + Network Layer)

### Preflight Request Flow

```
For "complex" requests (non-simple methods like PUT/DELETE, or custom headers):

Browser → Server: OPTIONS /api/data
  Request headers:
    Origin: https://app.example.com
    Access-Control-Request-Method: POST
    Access-Control-Request-Headers: Content-Type, Authorization

Server → Browser: 200 OK
  Response headers:
    Access-Control-Allow-Origin: https://app.example.com
    Access-Control-Allow-Methods: GET, POST, PUT, DELETE
    Access-Control-Allow-Headers: Content-Type, Authorization
    Access-Control-Max-Age: 86400  (cache preflight for 24h)

Browser → Server: POST /api/data (actual request)
  Origin: https://app.example.com
  Content-Type: application/json
```

### Simple vs Non-Simple Requests

**Simple (no preflight):**
- Methods: GET, HEAD, POST
- Content-Type: text/plain, multipart/form-data, application/x-www-form-urlencoded
- No custom headers

**Non-simple (triggers preflight):**
- Methods: PUT, DELETE, PATCH, OPTIONS
- Content-Type: application/json
- Any custom header: Authorization, X-Custom-Header

## 📐 ASCII Diagram

```
Browser (https://app.example.com)
  │
  │ fetch('https://api.different.com/data')
  │
  ▼
[CORS check: different origin?]
  │ YES → Preflight OPTIONS (if non-simple)
  │       Check response headers
  │       Allow? → Send real request
  │       Deny?  → CORS error (blocked in browser, request never sent to server)
  │ NO (same origin) → Request passes through
```

## 🔍 Code Examples

### Example 1 — Express CORS Configuration

```javascript
// Minimal CORS setup (development — allows all origins)
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*')  // Any origin
  res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
  res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
  if (req.method === 'OPTIONS') return res.sendStatus(200)
  next()
})

// Production CORS (allowlist)
const allowedOrigins = ['https://app.example.com', 'https://admin.example.com']
app.use((req, res, next) => {
  const origin = req.headers.origin
  if (allowedOrigins.includes(origin)) {
    res.header('Access-Control-Allow-Origin', origin)  // Dynamic, not *
    res.header('Vary', 'Origin')  // Cache must vary by Origin header!
  }
  res.header('Access-Control-Allow-Credentials', 'true')  // Allow cookies
  if (req.method === 'OPTIONS') return res.sendStatus(200)
  next()
})
```

### Example 2 — Credentials and Cookies

```javascript
// Browser: must explicitly enable credentials
fetch('https://api.example.com/user', {
  credentials: 'include',  // Send cookies + Authorization headers
  // 'include': always send credentials
  // 'same-origin': only for same-origin (default)
  // 'omit': never send credentials
})

// Server: CANNOT use wildcard with credentials
// Access-Control-Allow-Origin: *           ← WRONG when credentials sent
// Access-Control-Allow-Origin: https://app.example.com  ← CORRECT
// Access-Control-Allow-Credentials: true   ← REQUIRED for cookies
```

### Example 3 — CORB (Cross-Origin Read Blocking)

```javascript
// CORB is a Blink-level protection (not same as CORS)
// Blocks cross-origin HTML/JSON/XML responses from reaching JS
// Even with proper CORS headers!

// Scenario: Malicious page tries to load private JSON via <script>:
// <script src="https://bank.com/api/balance"></script>
// CORB: bank.com responds with Content-Type: application/json
// Blink blocks the response from reaching the page script
// (attacker can't use bank's JSON as JS code)

// COEP (Cross-Origin Embedder Policy): opt-in for cross-origin isolation
// Required for SharedArrayBuffer + high-precision timers
// Response-headers: Cross-Origin-Embedder-Policy: require-corp
```

## 💥 Production Failures

### Failure — CORS Misconfiguration Allowing Any Origin

```javascript
// DANGEROUS: Reflecting any origin (not whitelisting)
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', req.headers.origin)  // Echo any origin!
  res.header('Access-Control-Allow-Credentials', 'true')
  next()
})
// This is effectively the same as wildcard (*) but also allows cookies
// Attack: attacker's origin gets credentials → CSRF via CORS
```

### Failure — Preflight Caching Issues

```javascript
// Access-Control-Max-Age: 0 → every request preflights (doubles request count!)
// This is the default if Max-Age not set in Chrome
// Fix: Set appropriate max age
res.header('Access-Control-Max-Age', '86400')  // Cache 24 hours
// WARNING: Cached preflight means header changes don't take effect for 24h
```

## 🏢 Industry Best Practices

1. **Whitelist specific origins** — Never use `*` in production with credentials.
2. **Set `Vary: Origin`** — Essential for reverse proxy/CDN caching correctness.
3. **Cache preflight** — Set `Access-Control-Max-Age` to reduce preflight overhead.
4. **Use cors npm package** — Battle-tested implementation for Express/Koa.
5. **Enable COEP + COOP** — Required for SharedArrayBuffer and precise performance timers.

## 💼 Interview Questions

**Q1: Why does CORS only apply in browsers?**
> CORS is enforced by the browser, not the server. Server-side code (curl, Node.js, etc.) directly makes TCP connections without going through a browser's Same-Origin Policy enforcement layer. CORS headers on the server tell the *browser* whether to allow the response to be read by cross-origin JS. The actual HTTP request is made regardless; the browser may block the *response* from being accessible to JS. Server-to-server calls bypass this entirely.

**Q2: Why can't you use `Access-Control-Allow-Origin: *` with credentials?**
> Using wildcard with credentials would allow any website to make authenticated requests to your API using the user's cookies. The browser enforces: if `Access-Control-Allow-Credentials: true`, then `Access-Control-Allow-Origin` must be a specific origin, not `*`. This prevents confused-deputy attacks where a malicious site sends the user's credentials to your API and reads the response.

## 🔗 Navigation

**Prev:** [05_Rendering_Pipeline.md](05_Rendering_Pipeline.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [07_Web_Workers.md](07_Web_Workers.md)
