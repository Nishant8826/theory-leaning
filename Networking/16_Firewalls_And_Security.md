# Firewalls & Security

> 📌 **File:** 16_Firewalls_And_Security.md | **Level:** Full-Stack Dev → Networking Expert

---

## What is it?

Network security is about controlling what traffic is allowed in and out of your servers. You need to know Security Groups (AWS host firewalls), NACLs (AWS subnet firewalls), and WAF (Layer 7 web application firewalls for DDoS and SQL injection). In your app, Helmet secures HTTP headers, and rate limiters prevent API abuse.

---

## Map it to MY STACK (CRITICAL)

```
┌──────────────────────────────────────────────────────────────────┐
│  Security Layer │ Level        │ How it Works                    │
├─────────────────┼──────────────┼─────────────────────────────────┤
│  AWS WAF        │ Layer 7      │ Inspects HTTP headers, body     │
│                 │ (Application)│ Blocks SQLi, XSS, bots, DDoS     │
│                 │              │                                 │
│  Security Group │ Layer 4      │ Stateful host firewall          │
│  (sg-xxx)       │ (TCP/UDP)    │ References SG IDs (no IPs!)     │
│                 │              │                                 │
│  NACL           │ Layer 3      │ Stateless subnet firewall       │
│  (acl-xxx)      │ (IP/Port)    │ Explicit Allow/Deny by IP block │
│                 │              │                                 │
│  Helmet.js      │ Express      │ Sets secure HTTP headers        │
│  (app level)    │ (Code)       │ CSP, HSTS, X-Frame-Options      │
│                 │              │                                 │
│  Rate Limiter   │ Express      │ Throttles requests by IP        │
│  (app level)    │ (Code/Redis) │ Redis-backed sliding window     │
└─────────────────┴──────────────┴─────────────────────────────────┘
```

---

## AWS Firewalls — Security Groups vs NACLs

```
Security Group (Stateful, Host Level):
  You connect: Client IP → port 443 → EC2
  Security Group ALLOWS port 443 inbound.
  Response (outbound) is AUTOMATICALLY allowed.

NACL (Stateless, Subnet Level):
  You connect: Client IP → port 443 → Subnet
  NACL must ALLOW port 443 inbound.
  AND NACL must ALLOW ephemeral ports (1024-65535) outbound!
```

#### Diagram Explanation (The Club Security vs The Border Patrol)
- **Security Groups (The Club Bouncer):** Stateful. The bouncer checks your invite (Inbound Rule) on the way in. If you are allowed inside, you are automatically allowed to leave without being questioned on the way out (`Stateful`).
- **NACLs (The Border Patrol Checkpoint):** Stateless. A checkpoint at the subnet border. They inspect every single packet going *in*, and they inspect every packet going *out* entirely separately (`Stateless`).

---

## App Security Code (Express)

### 1. Helmet — Securing Headers

```javascript
const express = require('express');
const helmet = require('helmet');

const app = express();

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'", "https://apis.google.com"],
      styleSrc: ["'self'", "https://fonts.googleapis.com", "'unsafe-inline'"],
      imgSrc: ["'self'", "data:", "https://images.unsplash.com"],
      connectSrc: ["'self'", "https://api.stripe.com"],
      fontSrc: ["'self'", "https://fonts.gstatic.com"],
      objectSrc: ["'none'"],
      upgradeInsecureRequests: []
    }
  },
  strictTransportSecurity: {
    maxAge: 31536000,          // 1 year
    includeSubDomains: true,
    preload: true
  },
  frameguard: { action: 'deny' },
  noSniff: true,
  xssFilter: true
}));
```

### 2. Redis-Backed Rate Limiter (Sliding Window)

```javascript
const Redis = require('ioredis');
const redis = new Redis(process.env.REDIS_URL);

const rateLimiter = (options) => {
  const { windowMs = 15 * 60 * 1000, max = 100 } = options;
  
  return async (req, res, next) => {
    const ip = req.ip;
    const key = `ratelimit:${ip}`;
    const now = Date.now();
    const windowStart = now - windowMs;
    
    try {
      const multi = redis.multi();
      multi.zremrangebyscore(key, 0, windowStart);
      multi.zcard(key);
      multi.zadd(key, now, now);
      multi.expire(key, Math.ceil(windowMs / 1000));
      
      const results = await multi.exec();
      const requestCount = results[1][1];
      
      res.set('X-RateLimit-Limit', max);
      res.set('X-RateLimit-Remaining', Math.max(0, max - requestCount));
      res.set('X-RateLimit-Reset', new Date(now + windowMs).toISOString());
      
      if (requestCount >= max) {
        return res.status(429).json({ error: 'Too many requests' });
      }
      next();
    } catch (err) {
      console.error('Rate limiter error:', err);
      next(); // Fail open in production
    }
  };
};

app.use('/api/', rateLimiter({ windowMs: 15 * 60 * 1000, max: 100 }));
```

---

## DDoS Mitigation

- **Layer 3/4 (Volumetric):** Handled by AWS Shield (Standard is free, enabled on Route 53 and CloudFront).
- **Layer 7 (HTTP Flood, Application):** Handled by AWS WAF (Web Application Firewall) + CloudFront.
  - **WAF Rules:** Rate-based rules, geo-blocking, bot control, and payload inspection for SQLi/XSS.

---

## CORS — Cross-Origin Resource Sharing

CORS is a browser security mechanism, NOT a server security mechanism! It prevents malicious websites from reading your API responses.

### Express CORS Implementation

```javascript
const cors = require('cors');

const whitelist = ['https://myapp.com', 'https://admin.myapp.com'];

const corsOptions = {
  origin: (origin, callback) => {
    if (!origin) return callback(null, true);
    if (whitelist.indexOf(origin) !== -1) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  },
  credentials: true
};

app.use(cors(corsOptions));
```

---

## Practice Exercises

### Exercise 1: Helmet Audit
Apply Helmet to an Express app. Use Chrome DevTools (Network tab) to inspect the headers before and after. Identify new headers added.

### Exercise 2: Sliding Window Limiter
Implement the Redis sliding window rate limiter in Express. Use `autocannon` to hit the server at 150 requests/sec. Verify 429 status code returns.

---

## Interview Q&A

**Q1: What is the difference between Security Groups and NACLs?**
> Security Groups are stateful host-level firewalls (apply to instances, allow rules only, reference SG IDs). NACLs are stateless subnet-level firewalls (apply to subnets, allow and deny rules evaluated in order, reference IP blocks).

**Q2: How does a stateful firewall work?**
> It tracks connection state. If inbound traffic is allowed, outbound response is automatically allowed without explicit rules. Security Groups are stateful; NACLs are stateless and need explicit outbound rules for ephemeral ports.

**Q3: How do you protect an API from DDoS attacks?**
> Layered defense: AWS Shield (L3/4 protection), AWS WAF (L7 rate limits, geo-blocking, bot control), CloudFront (caching, DDoS absorption), and application-level Redis rate limiters. Keep databases private.

**Q4: Explain CORS. Is it a server security tool?**
> No, CORS is a browser security mechanism that prevents a site on origin A from reading responses from origin B. The server defines policies (`Access-Control-Allow-Origin`); the browser enforces them. Non-browser clients (curl, mobile apps) ignore CORS.

**Q5: Why reference Security Groups by ID instead of IP?**
> IPs in cloud environments are dynamic (auto-scaling, restarts). Referencing by SG ID says "allow traffic from any instance belonging to this group". It is dynamic, self-updating, and avoids hardcoded IPs.

---

Prev : [15 CDN And Caching](./15_CDN_And_Caching.md) | Index: [00 Index](./00_Index.md) | Next : [17 API Gateways](./17_API_Gateways.md)
