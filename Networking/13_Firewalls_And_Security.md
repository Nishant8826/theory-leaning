# Firewalls & Security

> 📌 **File:** 13_Firewalls_And_Security.md | **Level:** Full-Stack Dev → Networking Expert

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
  (It remembers the connection state)

NACL (Stateless, Subnet Level):
  You connect: Client IP → port 443 → Subnet
  NACL must ALLOW port 443 inbound.
  AND NACL must ALLOW ephemeral ports (1024-65535) outbound!
  (It has no memory. Every packet is checked separately)

┌──────────────────────────────────────────────────────────────────┐
│  Feature              │ Security Group       │ NACL              │
├───────────────────────┼──────────────────────┼───────────────────┤
│  Level                │ Instance / Host      │ Subnet            │
│  State                │ Stateful             │ Stateless         │
│  Rules                │ Allow only (default  │ Allow and Deny    │
│                       │ deny-all)            │ (eval in order)   │
│  Target               │ Refer by SG ID or IP │ Refer by IP CIDR  │
│  Evaluation           │ All rules evaluated  │ Rules in order    │
│                       │ (no ordering)        │ (100, 200, etc)   │
├───────────────────────┴──────────────────────┴───────────────────┤
│  Rule of thumb:                                                 │
│  Use Security Groups for 95% of controls (reference by SG ID).  │
│  Use NACLs only for broad IP blocking (e.g. block a subnet/IP).  │
└──────────────────────────────────────────────────────────────────┘
```

#### Diagram Explanation (The Club Security vs The Border Patrol)
- **Security Groups (The Club Bouncer):** Stateful. The bouncer checks your invite (Inbound Rule) on the way in. If you are allowed inside, you are automatically allowed to leave without being physically stopped and re-questioned on the way out (`Stateful`).
- **NACLs (The Border Patrol Checkpoint):** Stateless. A checkpoint at the subnet border. They inspect every single packet going *in*, and they inspect every packet going *out* entirely separately (`Stateless`). If you forget to add a rule allowing people to leave (Outbound Ephemeral Ports), they are locked inside the country forever!

---

## App Security Code (Express)

### 1. Helmet — Securing Headers

```javascript
const express = require('express');
const helmet = require('helmet');

const app = express();

// ──── Configure Helmet ────
app.use(helmet({
  // Content Security Policy (CSP) — what resources can load
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
  // Strict-Transport-Security (HSTS) — force HTTPS
  strictTransportSecurity: {
    maxAge: 31536000,          // 1 year
    includeSubDomains: true,
    preload: true
  },
  // Prevent clickjacking
  frameguard: { action: 'deny' },
  // Prevent MIME type sniffing
  noSniff: true,
  // XSS protection for older browsers
  xssFilter: true
}));
```

### 2. Redis-Backed Rate Limiter (Sliding Window)

```javascript
const Redis = require('ioredis');
const redis = new Redis(process.env.REDIS_URL);

// ──── Sliding Window Rate Limiter ────
const rateLimiter = (options) => {
  const { windowMs = 15 * 60 * 1000, max = 100 } = options;
  
  return async (req, res, next) => {
    const ip = req.ip;
    const key = `ratelimit:${ip}`;
    const now = Date.now();
    const windowStart = now - windowMs;
    
    try {
      const multi = redis.multi();
      
      // 1. Remove requests older than window start
      multi.zRemRangeByScore(key, 0, windowStart);
      // 2. Count requests in current window
      multi.zCard(key);
      // 3. Add current request timestamp
      multi.zAdd(key, now, now);
      // 4. Set expiry on key (keep Redis clean)
      multi.expire(key, Math.ceil(windowMs / 1000));
      
      const results = await multi.exec();
      const requestCount = results[1][1]; // Result of zCard
      
      res.set('X-RateLimit-Limit', max);
      res.set('X-RateLimit-Remaining', Math.max(0, max - requestCount));
      res.set('X-RateLimit-Reset', new Date(now + windowMs).toISOString());
      
      if (requestCount >= max) {
        return res.status(429).json({
          error: 'Too many requests, please try again later.'
        });
      }
      
      next();
    } catch (err) {
      console.error('Rate limiter error:', err);
      next(); // Fail open in production so rate limiter outage doesn't block users
    }
  };
};

app.use('/api/', rateLimiter({ windowMs: 15 * 60 * 1000, max: 100 }));
```

---

## DDoS Mitigation

```
DDoS: Distributed Denial of Service (overwhelming your servers)

Mitigation Strategy:
┌──────────────────────────────────────────────────────────────────┐
│  Layer 3/4 (Syn Flood, Volumetric)                               │
│  └── Handled by AWS Shield (Standard is free, enabled on Route 53│
│      and CloudFront). Absorbs gigabit floods at edge.            │
│                                                                  │
│  Layer 7 (HTTP Flood, Application)                               │
│  └── Handled by AWS WAF (Web Application Firewall) + CloudFront. │
│                                                                  │
│  WAF Rules:                                                      │
│  1. Rate-based rule: Block IP if requests > 2000 per 5 minutes   │
│  2. Geo-blocking: Block traffic from regions you don't serve     │
│  3. Bot control: Inspect headers/behavior, challenge with CAPTCHA│
│  4. SQLi/XSS: Inspect payloads for database injection strings    │
│                                                                  │
│  Application Level (Node.js)                                     │
│  └── Node.js is bad at handling DDoS. High CPU overhead.         │
│      Use WAF and CDN to block malicious traffic BEFORE it hits   │
│      your Node.js servers.                                       │
└──────────────────────────────────────────────────────────────────┘
```

#### Diagram Explanation (The Water Filtration System)
DDoS protection is visually exactly like running a water filtration system for your company:
- **AWS Shield (The Coarse Grate):** Located way out at the edge of the river. It catches massive logs, rocks, and giant debris (Volumetric layer 3/4 traffic) easily.
- **AWS WAF (The Fine Filter):** Sits at the building entrance. It inspects the water molecule-by-molecule to filter out fine sand, toxic chemicals, and parasites (Layer 7 HTTP floods, SQL injection strings) before the water goes into your drinking system.
- **Node.js (The Drinking Faucet):** If you try to dump raw, unfiltered river water directly into your faucet, the faucet instantly clogs. You must rely on Shield and WAF to deliver clean, purified HTTP requests to your Node.js code!

---

## CORS — Cross-Origin Resource Sharing

```
CORS is a browser security mechanism, NOT a server security mechanism!
It prevents malicious websites from reading your API responses.

Scenario:
  User logged into mybank.com (has active session cookie)
  User visits evil-site.com
  evil-site.com runs: fetch('https://mybank.com/api/transfer')
  Browser intercepts this check via CORS.

Preflight Request (CORS check):
  OPTIONS /api/transfer HTTP/1.1
  Origin: https://evil-site.com
  Access-Control-Request-Method: POST

Server Response:
  Access-Control-Allow-Origin: https://mybank.com  (only allow mybank.com)
  
Browser blocks request because Origin doesn't match Allow-Origin!
CORS does not stop evil-site from SENDING the request (writes can still
happen!). It stops the browser from allowing evil-site to READ response.
```

### Express CORS Implementation

```javascript
const cors = require('cors');

const whitelist = ['https://myapp.com', 'https://admin.myapp.com'];

const corsOptions = {
  origin: (origin, callback) => {
    // Allow requests with no origin (like mobile apps, curl)
    if (!origin) return callback(null, true);
    
    if (whitelist.indexOf(origin) !== -1) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  },
  credentials: true,                  // Allow cookies/auth headers
  optionsSuccessStatus: 200            // IE10 compatibility
};

app.use(cors(corsOptions));
```

---

## Common Mistakes

### ❌ Exposing database ports to 0.0.0.0/0

```
❌ Security Group Rule: Inbound PostgreSQL (5432) from 0.0.0.0/0
   → Anyone can connect and attempt brute force authentication

✅ Reference Security Group by ID
   Inbound 5432 from sg-app (only instances wearing the sg-app badge)
```

### ❌ Inbound SSH open to the world (Port 22)

```
❌ Inbound Port 22 from 0.0.0.0/0
   → Thousands of automated bots will brute-force SSH logins

✅ Inbound Port 22 from YOUR-IP/32 only
   Or use AWS Systems Manager (SSM) Session Manager (no open ports needed!)
```

---

## Practice Exercises

### Exercise 1: Helmet Audit
Apply Helmet to an Express app. Use Chrome DevTools (Network tab) to inspect the headers before and after. Identify new headers added.

### Exercise 2: Sliding Window Limiter
Implement the Redis sliding window rate limiter in Express. Use `autocannon` to hit the server at 150 requests/sec. Verify 429 status code returns.

### Exercise 3: Security Group Setup
Create an AWS Security Group configuration for ALB and EC2. The EC2 instances must only accept traffic from the ALB Security Group ID.

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

Prev : [12 Load Balancing](./12_Load_Balancing.md) | Index: [00 Index](./00_Index.md) | Next : [14 Proxies And Reverse Proxies](./14_Proxies_And_Reverse_Proxies.md)
