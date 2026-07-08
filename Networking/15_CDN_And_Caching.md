# CDN & Caching

> 📌 **File:** 15_CDN_And_Caching.md | **Level:** Full-Stack Dev → Networking Expert

---

## What is it?

A CDN (Content Delivery Network) caches your content at edge locations worldwide, serving users from the nearest point. When a user in Tokyo loads your React app hosted on US servers, the CDN serves the JS/CSS from a Tokyo edge server (~10ms) instead of crossing the Pacific (~200ms). AWS CloudFront is your CDN.

---

## Map it to MY STACK (CRITICAL)

```
┌──────────────────────────────────────────────────────────────────────┐
│  Content Type       │ Cache Where        │ TTL        │ Strategy    │
├─────────────────────┼────────────────────┼────────────┼─────────────┤
│  Next.js JS/CSS     │ CloudFront + S3    │ 1 year     │ Immutable   │
│  (hashed filenames) │                    │            │ (hash=bust) │
│                     │                    │            │             │
│  index.html         │ CloudFront         │ 5 min      │ Revalidate  │
│  (entry point)      │                    │            │             │
│                     │                    │            │             │
│  Images/fonts       │ CloudFront + S3    │ 30 days    │ Long cache  │
│                     │                    │            │             │
│  API: /products     │ CloudFront + Redis │ 60s        │ Short cache │
│                     │                    │            │             │
│  API: /profile      │ Redis only         │ 5 min      │ Private     │
│  (user-specific)    │                    │            │ (no CDN)    │
│                     │                    │            │             │
│  API: /checkout     │ NONE               │ 0          │ No cache    │
└─────────────────────┴────────────────────┴────────────┴─────────────┘
```

### Your Caching Architecture

```
                    User (Tokyo)
                        │
                   ┌────▼────┐
                   │CloudFront│  Edge server in Tokyo
                   │  (CDN)  │  
                   └────┬────┘
                         │
               ┌─────────┼─────────┐
               │         │         │
          Cache HIT  Cache MISS  Cache MISS
          (static)   (API)       (first time)
               │         │         │
          Return      ┌──▼──┐     │
          instantly   │ ALB │     │
                      └──┬──┘     │
                         │        │
                    ┌────▼────┐   │
                    │ Node.js │   │
                    └────┬────┘   │
                         │        │
               ┌─────────┼────┐   │
               │              │   │
          ┌────▼────┐   ┌────▼┐  │
          │  Redis  │   │Mongo│  │
          │ (cache) │   │ DB  │  │
          └─────────┘   └─────┘  │
                                 │
                            ┌────▼────┐
                            │   S3    │  Static assets origin
                            └─────────┘
```

#### Diagram Explanation (The Memory Game)
Caching is all about having different layers of memory. Think of it like taking a test:
- **CloudFront (Short-Term Memory / Open Book):** For static files, CloudFront instantly knows the answer. It doesn't even need to ask the brain. (Cache HIT)
- **Redis (Working Memory):** For dynamic API endpoints, CloudFront has to ask the backend. Node.js then checks its own immediate working memory (Redis). If the database calculated this exact complex query 5 minutes ago, Redis remembers it and hands it back in 1ms!
- **Database (Deep Calculation):** If the data is totally new or specific strictly to a user's session (like a Checkout cart), the system bypasses all the caches completely down to the final database (`Cache MISS`), does the heavy calculation, and sends the response back up the chain!

---

## How does it actually work?

### CloudFront — Request Flow

```
1. User in Mumbai: GET https://myapp.com/bundle.abc123.js
2. DNS: myapp.com → CloudFront → nearest edge (Mumbai POP)
3. Edge checks cache: Key: GET /bundle.abc123.js
   
   CACHE HIT:
     → Return immediately (< 10ms)
     → Header: X-Cache: Hit from cloudfront
   
   CACHE MISS:
     → Forward request to origin (S3 or ALB)
     → Receive response
     → Cache it at Mumbai edge
     → Return to user
```

---

## Multi-Layer Caching Strategy

```
┌──────────────────────────────────────────────────────────────────┐
│  Layer 1: Browser Cache (user's machine)                        │
│  ├── JS/CSS with hash: Cache-Control: max-age=31536000         │
│  └── HTML: Cache-Control: no-cache (always revalidate)         │
│                                                                  │
│  Layer 2: CDN Cache (CloudFront edge)                           │
│  ├── Static files: 1 year (same as browser)                     │
│  └── Public API data: 60 seconds                                │
│                                                                  │
│  Layer 3: Application Cache (Redis)                             │
│  ├── Database query results: 5 minutes                          │
│  └── Session data: 24 hours                                     │
│                                                                  │
│  Layer 4: Database Cache (MongoDB WiredTiger / PG shared_buffers)│
│  └── Frequently accessed data stays in memory                   │
└──────────────────────────────────────────────────────────────────┘
```

#### Diagram Explanation (The Caching Golden Rule)
This diagram visualizes the golden rule of caching: **"Closer to the user = Faster but drastically harder to invalidate."**
If you cache a broken javascript file in the browser, you cannot force the user to delete it off their computer. They will see a broken site for a full year until the TTL drops, unless you change the filename itself (Hashing: `bundle.abc.js` -> `bundle.xyz.js`). Conversely, if you cache bad logic on Redis, you can manually run a 1-second `DEL` command from your terminal and instantly fix the bug globally.

---

## Node.js Implementation

```javascript
const express = require('express');
const Redis = require('ioredis');

const app = express();
const redis = new Redis(process.env.REDIS_URL);

// Static Asset Caching Headers
app.use('/static', express.static('public', {
  maxAge: '365d',
  immutable: true,
  etag: false
}));

// Redis Cache Middleware
function cacheMiddleware(keyGenerator, ttlSeconds = 60) {
  return async (req, res, next) => {
    const key = typeof keyGenerator === 'function' 
      ? keyGenerator(req) 
      : `cache:${req.originalUrl}`;
    
    try {
      const cached = await redis.get(key);
      if (cached) {
        res.set('X-Cache', 'HIT');
        return res.json(JSON.parse(cached));
      }
    } catch (err) {
      console.error('Cache read error:', err);
    }
    
    const originalJson = res.json.bind(res);
    res.json = async (data) => {
      try {
        await redis.set(key, JSON.stringify(data), 'EX', ttlSeconds);
      } catch (err) {
        console.error('Cache write error:', err);
      }
      res.set('X-Cache', 'MISS');
      return originalJson(data);
    };
    next();
  };
}

// User-specific data — NEVER cache in CDN
app.get('/api/profile', auth, (req, res) => {
  res.set('Cache-Control', 'private, no-store');
  res.json(req.user);
});
```

---

## Practice Exercises

### Exercise 1: Redis Caching
Implement cache-aside pattern for your most expensive API endpoint. Measure response time before and after caching.

### Exercise 2: Cache Headers
Set appropriate Cache-Control headers for: static assets (1 year), public API (60s), private API (no cache). Verify with `curl -I`.

---

## Interview Q&A

**Q1: How does a CDN improve performance?**
> CDN caches content at edge locations near users. Static assets served from nearby edge (~10ms) instead of the origin server (~200ms cross-continent). Reduces origin load, improves Time to First Byte, and helps with DDoS absorption.

**Q2: What is cache invalidation and why is it hard?**
> Ensuring cached data stays consistent with the source. Hard because: caches exist at multiple layers (browser, CDN, Redis), propagation isn't instant (CloudFront takes 60-300s), and you can't purge browser caches remotely. Solutions: short TTLs, versioned URLs, event-based invalidation.

**Q3: When should you use Redis cache vs CDN cache?**
> CDN: static assets, public API responses (same for all users), geographic performance. Redis: user-specific data, database query results, session data, rate limit counters. Redis is private (server-side); CDN is public (shared across users).

**Q4: What is the thundering herd problem with caching?**
> When a popular cache key expires, hundreds of simultaneous requests hit the database before any can repopulate the cache. Solutions: cache lock (only one request queries DB), stale-while-revalidate (serve stale data while refreshing), pre-warming cache before expiry.

**Q5: How do you cache API responses correctly with CloudFront?**
> Set `Cache-Control: public, s-maxage=300` for cacheable responses. Use `Vary: Accept-Encoding` for compressed responses. Forward only needed headers (Authorization bypasses cache). Don't cache authenticated endpoints. Use `private, no-store` for user-specific data.

---

Prev : [14 Proxies And Reverse Proxies](./14_Proxies_And_Reverse_Proxies.md) | Index: [00 Index](./00_Index.md) | Next : [16 Firewalls And Security](./16_Firewalls_And_Security.md)
