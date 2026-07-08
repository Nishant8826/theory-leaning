# API Gateways

> 📌 **File:** 17_API_Gateways.md | **Level:** Full-Stack Dev → Networking Expert

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

With API Gateway:
  React → API Gateway → /api/users → User Service
                       → /api/orders → Order Service
                       → /api/products → Product Service
  Gateway handles: auth, rate limiting, CORS, logging centrally
  Client only knows one URL
```

### AWS API Gateway Types

```
HTTP API (v2, cheaper):
  - REST APIs, simple proxy to Lambda or ALB. Low latency.
  - Pricing: $1.00/million requests + data transfer

REST API (v1, more features):
  - Full-featured: caching, request validation, API keys, usage plans, WAF integration.
  - Pricing: $3.50/million requests + data transfer + cache
```

---

## API Gateway Patterns

### Pattern 1: API Gateway + Lambda (Serverless)

```
React ──► API Gateway ──► Lambda ──► MongoDB Atlas / RDS
```

```javascript
exports.handler = async (event) => {
  const { httpMethod, path } = event;
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
```

### Pattern 3: Custom API Gateway with Express

```javascript
const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const rateLimit = require('express-rate-limit');
const jwt = require('jsonwebtoken');

const app = express();

app.use(rateLimit({ windowMs: 15 * 60 * 1000, max: 100 }));

const authMiddleware = (req, res, next) => {
  if (req.path.startsWith('/api/public/')) return next();
  const token = req.headers.authorization?.replace('Bearer ', '');
  if (!token) return res.status(401).json({ error: 'No token' });
  try {
    req.user = jwt.verify(token, process.env.JWT_SECRET);
    req.headers['x-user-id'] = req.user.id;
    next();
  } catch {
    res.status(401).json({ error: 'Invalid token' });
  }
};

app.use('/api/', authMiddleware);

app.use('/api/users', createProxyMiddleware({ target: 'http://user-service:3001', changeOrigin: true }));
app.use('/api/orders', createProxyMiddleware({ target: 'http://order-service:3002', changeOrigin: true }));
app.use('/api/products', createProxyMiddleware({ target: 'http://product-service:3003', changeOrigin: true }));

app.listen(8080);
```

---

## Visual Diagram — API Gateway Architecture

```
Mobile/Web Apps ──► CloudFront (CDN Edge)
                 ──► API Gateway (Auth, Rate limit)
                 ├──► User Service (Lambda)
                 ├──► Order Service (EC2)
                 └──► Product Service (Lambda)
```

#### Diagram Explanation (The Single Front Desk)
Imagine your microservice architecture as a hospital with specialized departments:
- **Without an API Gateway:** Every client has to figure out exactly which department to visit, pass a separate security check at every building (authentication), and locate the doctor's room.
- **With an API Gateway:** One centralized Front Desk handles check-in, authentication, rate limits, and routes patients to the correct internal department (`/api/users` vs `/api/orders`).

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
│  Lambda integration   │ ✅ Native            │ ✅ Supported        │
│  Max payload          │ 10MB                 │ Unlimited          │
│  Max timeout          │ 30s (REST), 29s(HTTP)│ 4000s              │
└──────────────────────┴──────────────────────┴─────────────────────┘
```

---

## Practice Exercises

### Exercise 1: API Gateway + Lambda
Create a simple CRUD API using API Gateway HTTP API + Lambda. Deploy with AWS CLI or Serverless Framework.

### Exercise 2: Custom Gateway
Build a custom API gateway with Express that proxies to 2 microservices with shared authentication and request logging.

---

## Interview Q&A

**Q1: What is an API Gateway and why use one?**
> A single entry point that handles cross-cutting concerns: authentication, rate limiting, CORS, logging, request routing, and response caching. Decouples clients from backend services. Clients know one URL; the gateway routes to the right service.

**Q2: API Gateway vs reverse proxy — what's the difference?**
> A reverse proxy (Nginx) forwards requests with minimal logic. An API Gateway adds intelligence: auth validation, rate limiting, request/response transformation, API versioning, analytics, and developer portal.

**Q3: When would you NOT use AWS API Gateway?**
> When you need: response times < 10ms (API GW adds 10-30ms), payloads > 10MB, requests longer than 29 seconds, WebSocket with complex routing, or cost optimization at high volume.

**Q4: How do you handle API versioning through a gateway?**
> Path-based: `/v1/users`, `/v2/users` → different target groups or Lambda versions. Header-based: `Accept-Version: 2`. Path-based is most common and CDN-friendly.

**Q5: What is the cold start problem with Lambda behind API Gateway?**
> First request to an idle Lambda takes 100-500ms to provision a container. Subsequent requests reuse the warm container (~1ms overhead). Solutions: provisioned concurrency (keeps containers warm), regular pings, or accept cold starts for non-critical paths.

---

Prev : [16 Firewalls And Security](./16_Firewalls_And_Security.md) | Index: [00 Index](./00_Index.md) | Next : [18 Microservices Networking](./18_Microservices_Networking.md)
