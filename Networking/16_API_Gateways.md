# API Gateways

> 📌 **File:** 16_API_Gateways.md | **Level:** Full-Stack Dev → Networking Expert

---

## What is it?

An API Gateway is a single entry point for all client requests that handles cross-cutting concerns: authentication, rate limiting, request routing, response transformation, and monitoring. AWS API Gateway is the managed option; Nginx/Kong/Express can also serve as API gateways.

---

## Map it to MY STACK (CRITICAL)

```
Without API Gateway:
  React → /api/users → User Service (:3001)
  React → /api/orders → Order Service (:3002)
  React → /api/products → Product Service (:3003)
  Each service handles its own: auth, rate limiting, CORS, logging
  Client knows about every service ❌

With API Gateway:
  React → API Gateway → /api/users → User Service
                       → /api/orders → Order Service
                       → /api/products → Product Service
  Gateway handles: auth, rate limiting, CORS, logging centrally ✅
  Client only knows one URL ✅
```

### AWS API Gateway Types

```
┌────────────────────────────────────────────────────────────────────┐
│  Type            │ Protocol │ Use Case                            │
├──────────────────┼──────────┼─────────────────────────────────────┤
│  HTTP API        │ HTTP     │ REST APIs, simple proxy to Lambda  │
│  (v2, cheaper)   │          │ or ALB. Low latency. ← USE THIS   │
│                  │          │                                     │
│  REST API        │ HTTP     │ Full-featured: caching, request    │
│  (v1, more       │          │ validation, API keys, usage plans  │
│   features)      │          │ WAF integration. More expensive.   │
│                  │          │                                     │
│  WebSocket API   │ WS       │ Real-time: chat, notifications     │
│                  │          │ Routes by message content           │
├──────────────────┴──────────┴─────────────────────────────────────┤
│  Pricing:                                                         │
│  HTTP API: $1.00/million requests + data transfer                │
│  REST API: $3.50/million requests + data transfer + cache        │
│  For most apps: HTTP API is sufficient and 3.5x cheaper.        │
└────────────────────────────────────────────────────────────────────┘
```

---

## API Gateway Patterns

### Pattern 1: API Gateway + Lambda (Serverless)

```
React ──► API Gateway ──► Lambda ──► MongoDB Atlas / RDS
                                    
No EC2, no Nginx, no PM2, no scaling config.
API Gateway handles: routing, auth, throttling, CORS
Lambda handles: business logic
Scales automatically from 0 to thousands of concurrent requests.

Cost: Pay per request. Free tier: 1M requests/month.
Latency: +30-100ms (Lambda cold start)
```

```javascript
// Lambda handler (serverless Node.js)
exports.handler = async (event) => {
  const { httpMethod, path, body, headers } = event;
  
  if (httpMethod === 'GET' && path === '/api/products') {
    const products = await db.collection('products').find({}).toArray();
    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ products })
    };
  }
  
  return { statusCode: 404, body: 'Not found' };
};
```

### Pattern 2: API Gateway + ALB + EC2 (Traditional)

```
React ──► API Gateway ──► ALB ──► EC2 (Node.js)

API Gateway adds: auth, rate limiting, API keys, caching
ALB adds: load balancing, health checks
EC2 adds: your Express application

More control, lower latency (no cold start), higher base cost.
```

### Pattern 3: Custom API Gateway with Express

```javascript
const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const rateLimit = require('express-rate-limit');
const jwt = require('jsonwebtoken');

const app = express();

// ──── Cross-cutting: Rate Limiting ────
app.use(rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100
}));

// ──── Cross-cutting: Authentication ────
const authMiddleware = (req, res, next) => {
  // Skip auth for public endpoints
  if (req.path.startsWith('/api/public/')) return next();
  
  const token = req.headers.authorization?.replace('Bearer ', '');
  if (!token) return res.status(401).json({ error: 'No token' });
  
  try {
    req.user = jwt.verify(token, process.env.JWT_SECRET);
    // Forward user info to downstream services
    req.headers['x-user-id'] = req.user.id;
    req.headers['x-user-email'] = req.user.email;
    req.headers['x-user-roles'] = req.user.roles.join(',');
    next();
  } catch {
    res.status(401).json({ error: 'Invalid token' });
  }
};

app.use('/api/', authMiddleware);

// ──── Cross-cutting: Request Logging ────
app.use((req, res, next) => {
  const start = Date.now();
  res.on('finish', () => {
    console.log(JSON.stringify({
      method: req.method,
      path: req.path,
      status: res.statusCode,
      duration: Date.now() - start,
      userId: req.user?.id,
      ip: req.ip
    }));
  });
  next();
});

// ──── Route to Microservices ────
app.use('/api/users', createProxyMiddleware({
  target: 'http://user-service:3001',
  pathRewrite: { '^/api/users': '/users' },
  changeOrigin: true
}));

app.use('/api/orders', createProxyMiddleware({
  target: 'http://order-service:3002',
  pathRewrite: { '^/api/orders': '/orders' },
  changeOrigin: true
}));

app.use('/api/products', createProxyMiddleware({
  target: 'http://product-service:3003',
  pathRewrite: { '^/api/products': '/products' },
  changeOrigin: true
}));

app.listen(8080, () => console.log('API Gateway on :8080'));
```

---

## Visual Diagram — API Gateway Architecture

```
               Mobile App       React Web App       Third-party
                   │                 │                   │
                   └────────┬────────┘                   │
                            │                            │
                    ┌───────▼────────┐                   │
                    │  CloudFront    │◄──────────────────┘
                    │  (CDN + Edge)  │
                    └───────┬────────┘
                            │
                    ┌───────▼────────┐
                    │  API Gateway   │  ← auth, rate limit, throttle
                    │  (AWS or custom)│     CORS, API keys, logging
                    └───┬───┬───┬───┘
                        │   │   │
              ┌─────────┘   │   └─────────┐
              │             │             │
        ┌─────▼─────┐ ┌────▼────┐ ┌──────▼────┐
        │ User Svc  │ │Order Svc│ │Product Svc│
        │ (Lambda)  │ │ (EC2)   │ │ (Lambda)  │
        └─────┬─────┘ └────┬────┘ └──────┬────┘
              │            │              │
        ┌─────▼────┐ ┌────▼────┐ ┌───────▼───┐
        │PostgreSQL│ │MongoDB  │ │ElastiCache│
        └──────────┘ └─────────┘ └───────────┘
```

---

## API Gateway vs ALB — When to Use Which

```
┌────────────────────────────────────────────────────────────────────┐
│  Feature              │ API Gateway          │ ALB                 │
├───────────────────────┼──────────────────────┼─────────────────────┤
│  Auth (JWT/Cognito)   │ ✅ Built-in          │ ❌ App handles      │
│  Rate limiting        │ ✅ Built-in          │ ❌ App handles      │
│  API key management   │ ✅ Built-in          │ ❌ Not available    │
│  Request validation   │ ✅ Schema validation │ ❌ Not available    │
│  Response caching     │ ✅ Built-in          │ ❌ Not available    │
│  WebSocket            │ ✅ WebSocket API     │ ✅ HTTP upgrade     │
│  Lambda integration   │ ✅ Native            │ ✅ Supported        │
│  Cost (1M reqs/mo)    │ $1-3.50              │ ~$16 + LCU         │
│  Latency overhead     │ 10-30ms              │ 1-5ms              │
│  Max payload          │ 10MB                 │ Unlimited          │
│  Max timeout          │ 30s (REST), 29s(HTTP)│ 4000s              │
├───────────────────────┴──────────────────────┴─────────────────────┤
│  Use API Gateway: Serverless, need auth/rate-limit/API-keys      │
│  Use ALB: Long-running requests, large payloads, EC2 backend     │
│  Use Both: API Gateway → ALB → EC2 (full feature set)           │
└────────────────────────────────────────────────────────────────────┘
```

---

## API Gateway Latency Concern

```
┌──────────────────────────────────────────────────────────────────┐
│  API Gateway adds 10-30ms per request                           │
│                                                                  │
│  For most APIs (100-500ms total): 10ms is negligible (2-10%)   │
│  For ultra-low-latency APIs (<50ms): 10ms is significant (20%+)│
│                                                                  │
│  If latency matters more than managed features:                  │
│  Skip API Gateway → use ALB directly                            │
│  Implement auth/rate-limit in Express middleware                 │
│                                                                  │
│  Lambda cold start adds another 100-500ms (first request)       │
│  Provisioned concurrency fixes cold starts ($$$)                │
└──────────────────────────────────────────────────────────────────┘
```

---

## Common Mistakes

### ❌ Lambda + API Gateway Timeout Mismatch

```
API Gateway REST API max timeout: 29 seconds
Lambda max execution: 15 minutes

If your Lambda takes 35 seconds:
  Lambda: still running...
  API Gateway: 504 Gateway Timeout (at 29s)
  User: sees error
  Lambda: finishes, response has nowhere to go

Fix: Keep Lambda functions fast (< 10s for API responses)
For long tasks: return 202 Accepted immediately, process async with SQS
```

### ❌ Not Using Custom Domain

```
Default: https://abc123xyz.execute-api.us-east-1.amazonaws.com/prod/api/users

✅ Custom domain: https://api.myapp.com/users
Setup: Route 53 ALIAS record → API Gateway custom domain
Certificate: ACM (same region as API Gateway, or us-east-1 for edge)
```

---

## Practice Exercises

### Exercise 1: API Gateway + Lambda
Create a simple CRUD API using API Gateway HTTP API + Lambda. Deploy with AWS CLI or Serverless Framework.

### Exercise 2: Custom Gateway
Build a custom API gateway with Express that proxies to 2 microservices with shared authentication and request logging.

### Exercise 3: Rate Limiting
Configure API Gateway throttling: 100 requests/second steady, 200 burst. Test with `wrk` or `autocannon` and verify 429 responses.

---

## Interview Q&A

**Q1: What is an API Gateway and why use one?**
> A single entry point that handles cross-cutting concerns: authentication, rate limiting, CORS, logging, request routing, and response caching. Decouples clients from backend services. Clients know one URL; the gateway routes to the right service.

**Q2: API Gateway vs reverse proxy — what's the difference?**
> A reverse proxy (Nginx) forwards requests with minimal logic. An API Gateway adds intelligence: auth validation, rate limiting, request/response transformation, API versioning, analytics, and developer portal. An API Gateway IS a reverse proxy with added business logic.

**Q3: When would you NOT use AWS API Gateway?**
> When you need: response times < 10ms (API GW adds 10-30ms), payloads > 10MB, requests longer than 29 seconds, WebSocket with complex routing, or cost optimization at high volume (ALB can be cheaper). Use ALB directly with Express middleware instead.

**Q4: How do you handle API versioning through a gateway?**
> Path-based: `/v1/users`, `/v2/users` → different target groups or Lambda versions. Header-based: `Accept-Version: 2` → gateway routes accordingly. Query param: `?version=2`. Path-based is most common and CDN-friendly.

**Q5: What is the cold start problem with Lambda behind API Gateway?**
> First request to an idle Lambda takes 100-500ms to provision a container. Subsequent requests reuse the warm container (~1ms overhead). Solutions: provisioned concurrency (keeps containers warm, costs more), regular pings to keep warm, or accept cold starts for non-critical paths.


Prev : [15 WebSockets And Real Time](./15_WebSockets_And_Real_Time.md) | Index: [0 Index](./0_Index.md) | Next : [17 Microservices Networking](./17_Microservices_Networking.md)
