# CDN & Caching

> 📌 **File:** 14_CDN_And_Caching.md | **Level:** Full-Stack Dev → Networking Expert

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
│  (entry point)      │                    │            │ (must stay  │
│                     │                    │            │  fresh)     │
│                     │                    │            │             │
│  Images/fonts       │ CloudFront + S3    │ 30 days    │ Long cache  │
│                     │                    │            │             │
│  API: /products     │ CloudFront + Redis │ 60s        │ Short cache │
│  (public data)      │                    │            │             │
│                     │                    │            │             │
│  API: /profile      │ Redis only         │ 5 min      │ Private     │
│  (user-specific)    │                    │            │ (no CDN)    │
│                     │                    │            │             │
│  API: /checkout     │ NONE               │ 0          │ No cache    │
│  (transactions)     │                    │            │ (real-time) │
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
- **Redis (Working Memory):** For dynamic API endpoints, CloudFront has to ask the backend. Node.js then checks its own immediate working memory (Redis). If the database calculated this exact complex query 5 minutes ago, Redis literally remembers it and hands it back in 1ms!
- **Database (Deep Calculation):** If the data is totally new or specific strictly to a user's session (like a Checkout cart), the system bypasses all the caches completely down to the final database (`Cache MISS`), forcefully does the heavy calculation, and comprehensively sends the response back up the chain!

---

## How does it actually work?

### CloudFront — Request Flow

```
1. User in Mumbai: GET https://myapp.com/bundle.abc123.js

2. DNS: myapp.com → CloudFront → nearest edge (Mumbai POP)

3. Edge checks cache:
   Key: GET /bundle.abc123.js
   
   CACHE HIT:
     → Return immediately (< 10ms)
     → Header: X-Cache: Hit from cloudfront
   
   CACHE MISS:
     → Forward request to origin (S3 or ALB)
     → Receive response
     → Cache it at Mumbai edge
     → Return to user
     → Header: X-Cache: Miss from cloudfront

4. Next user in Mumbai requesting same file:
     → CACHE HIT (served from Mumbai edge)

CloudFront has 400+ edge locations worldwide.
Most cities get < 20ms latency to nearest edge.
```

### CloudFront Distribution Setup

```
Origin 1: S3 Bucket (static assets)
  Path pattern: /static/*, /_next/*, /images/*
  TTL: 86400s (1 day), immutable for hashed files
  
Origin 2: ALB (API)
  Path pattern: /api/*
  TTL: 0 (forward to origin every time, or respect Cache-Control)
  Forward headers: Authorization, Accept, Content-Type
  Forward cookies: None (API uses JWT, not cookies)
  
Origin 3: ALB (Server-Side Rendering)
  Path pattern: /* (default)
  TTL: 60s (HTML pages cached briefly)
  Forward cookies: All (session-based rendering)
```

---

## Multi-Layer Caching Strategy

```
┌──────────────────────────────────────────────────────────────────┐
│  Layer 1: Browser Cache (user's machine)                        │
│  ├── JS/CSS with hash: Cache-Control: max-age=31536000         │
│  ├── HTML: Cache-Control: no-cache (always revalidate)         │
│  └── API responses: varies by endpoint                          │
│                                                                  │
│  Layer 2: CDN Cache (CloudFront edge)                           │
│  ├── Static files: 1 year (same as browser)                     │
│  ├── Public API data: 60 seconds                                │
│  └── Private data: NOT cached (Cache-Control: private)         │
│                                                                  │
│  Layer 3: Application Cache (Redis)                             │
│  ├── Database query results: 5 minutes                          │
│  ├── Session data: 24 hours                                     │
│  ├── Computed aggregations: 15 minutes                          │
│  └── Rate limit counters: 15 minutes                            │
│                                                                  │
│  Layer 4: Database Cache (MongoDB WiredTiger / PG shared_buffers)│
│  └── Frequently accessed data stays in memory                   │
│                                                                  │
│  Closer to user = faster but harder to invalidate               │
│  Further from user = slower but always fresh                    │
└──────────────────────────────────────────────────────────────────┘
```

#### Diagram Explanation (The Caching Golden Rule)
This diagram perfectly visualizes the golden rule of caching: **"Closer to the user = Faster but drastically harder to invalidate."**
If you accidentally cache a broken javascript file on `Layer 1: Browser Cache`, you practically have no way of legally forcing the user to delete it off their computer. They will see a completely broken site for a full year until the TTL drops, unless you change the filename itself (Hashing: `bundle.abc.js` -> `bundle.xyz.js`). Conversely, if you cache bad logic deeply on `Layer 3: Redis`, you can manually run a 1-second `DEL` command from your terminal and instantly fix the bug globally. Always be incredibly careful with volatile CDN/Browser caches!

---

## Node.js Implementation

```javascript
const express = require('express');
const Redis = require('ioredis');

const app = express();
const redis = new Redis(process.env.REDIS_URL);

// ──── Static Asset Caching Headers ────
app.use('/static', express.static('public', {
  maxAge: '365d',
  immutable: true,
  etag: false
}));

// ──── Redis Cache Middleware ────
function cacheMiddleware(keyGenerator, ttlSeconds = 60) {
  return async (req, res, next) => {
    const key = typeof keyGenerator === 'function' 
      ? keyGenerator(req) 
      : `cache:${req.originalUrl}`;
    
    try {
      const cached = await redis.get(key);
      if (cached) {
        const data = JSON.parse(cached);
        res.set('X-Cache', 'HIT');
        res.set('X-Cache-TTL', await redis.ttl(key));
        return res.json(data);
      }
    } catch (err) {
      console.error('Cache read error:', err);
    }
    
    // Store original json method to intercept response
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

// ──── Cache Invalidation Helper ────
async function invalidateCache(patterns) {
  for (const pattern of patterns) {
    const keys = await redis.keys(pattern);
    if (keys.length > 0) {
      await redis.del(...keys);
      console.log(`Invalidated ${keys.length} cache keys: ${pattern}`);
    }
  }
}

// ──── Usage ────

// Public product list — cache for 60 seconds
app.get('/api/products', 
  cacheMiddleware(() => 'cache:products:list', 60),
  async (req, res) => {
    const products = await Product.find({ isActive: true }).lean();
    res.json({ products });
  }
);

// Individual product — cache for 5 minutes
app.get('/api/products/:id',
  cacheMiddleware(req => `cache:products:${req.params.id}`, 300),
  async (req, res) => {
    const product = await Product.findById(req.params.id).lean();
    if (!product) return res.status(404).json({ error: 'Not found' });
    res.json(product);
  }
);

// CDN-friendly headers for API responses
app.get('/api/products', (req, res, next) => {
  // Tell CloudFront to cache this response
  res.set('Cache-Control', 'public, max-age=60, s-maxage=300');
  // max-age: browser caches for 60s
  // s-maxage: CDN caches for 300s (overrides max-age for CDN)
  next();
});

// Update product — invalidate caches
app.put('/api/products/:id', async (req, res) => {
  const product = await Product.findByIdAndUpdate(req.params.id, req.body, { new: true });
  
  // Invalidate Redis cache
  await invalidateCache([
    `cache:products:${req.params.id}`,
    'cache:products:list'
  ]);
  
  // Invalidate CloudFront cache (optional — for critical updates)
  // aws cloudfront create-invalidation --distribution-id EXXXXX --paths "/api/products/*"
  
  res.json(product);
});

// User-specific data — NEVER cache in CDN
app.get('/api/profile', auth, (req, res) => {
  res.set('Cache-Control', 'private, no-store');  // No CDN, no browser cache
  res.json(req.user);
});
```

---

## Cache Invalidation Strategies

```
┌──────────────────────────────────────────────────────────────────┐
│  Strategy          │ How              │ When to Use              │
├────────────────────┼──────────────────┼──────────────────────────┤
│  TTL expiry        │ Cache auto-      │ Data changes infrequently│
│                    │ expires after N  │ Product listings, configs│
│                    │ seconds          │                          │
│                    │                  │                          │
│  Event-based       │ Invalidate on    │ Data changes by your app │
│  invalidation      │ write/update     │ Product update, new order│
│                    │                  │                          │
│  Cache-aside       │ Check cache first│ General purpose          │
│  (lazy loading)    │ then DB if miss  │ Most common pattern      │
│                    │                  │                          │
│  Write-through     │ Update cache AND │ Write-heavy, read-heavy  │
│                    │ DB on every write│ Real-time dashboards     │
│                    │                  │                          │
│  Cache versioning  │ Include version  │ When TTL is long         │
│  (hash in filename)│ in cache key     │ JS bundles, images       │
├────────────────────┴──────────────────┴──────────────────────────┤
│                                                                  │
│  "There are only two hard things in computer science:            │
│   cache invalidation and naming things." — Phil Karlton          │
│                                                                  │
│  Rule: Use TTL-based expiry when possible.                      │
│  Event-based invalidation adds complexity.                       │
└──────────────────────────────────────────────────────────────────┘
```

---

## Commands & Debugging Tools

```bash
# Check cache headers
curl -I https://myapp.com/api/products
# Look for:
#   Cache-Control: public, max-age=60, s-maxage=300
#   X-Cache: Hit from cloudfront  (CDN cache hit)
#   Age: 45  (seconds since cached)
#   ETag: "abc123"

# Check Redis cache
redis-cli GET "cache:products:list"
redis-cli TTL "cache:products:list"     # Remaining TTL in seconds
redis-cli KEYS "cache:products:*"        # All product cache keys
redis-cli DBSIZE                         # Total cached keys

# Invalidate CloudFront cache 
aws cloudfront create-invalidation \
  --distribution-id E1XXXXXX \
  --paths "/api/products/*" "/_next/*"

# Monitor cache hit rate
redis-cli INFO stats | grep -E "keyspace_hits|keyspace_misses"
# Hit rate = hits / (hits + misses)
# Target: > 80% hit rate
```

---

## Performance Insight

```
┌──────────────────────────────────────────────────────────────────┐
│  Impact of Each Cache Layer                                      │
├─────────────────────┬──────────┬─────────────────────────────────┤
│  Without caching    │ 500ms    │ DNS + TCP + TLS + API + DB     │
│  + Browser cache    │ 0ms      │ No request at all (local)      │
│  + CDN cache        │ 10ms     │ Served from edge (no origin)   │
│  + Redis cache      │ 50ms     │ Skip DB query (1ms Redis)      │
│  + DB query cache   │ 200ms    │ In-memory (no disk I/O)        │
├─────────────────────┴──────────┴─────────────────────────────────┤
│                                                                  │
│  Real scenario — Product page load:                             │
│  Without any caching: 800ms (every request hits DB)             │
│  With Redis: 200ms (skip 600ms DB query)                        │
│  With CDN + Redis: 15ms for static, 200ms for API              │
│  With all layers: 0ms cached, 200ms first load                  │
│                                                                  │
│  Cache invalidation cost:                                        │
│  Redis DEL: < 1ms                                                │
│  CloudFront invalidation: 60-300 seconds (async)                │
│  Browser cache: Can't invalidate! (only TTL expiry)             │
│  → Use hashed filenames for deployable assets (/bundle.abc.js) │
└──────────────────────────────────────────────────────────────────┘
```

---

## Common Mistakes

### ❌ Caching User-Specific Data in CDN

```javascript
// ❌ CDN caches /api/profile → ALL users see the SAME profile!
app.get('/api/profile', (req, res) => {
  res.set('Cache-Control', 'public, max-age=300');  // CDN caches this
  res.json(req.user);  // User A's data served to User B!
});

// ✅ Mark user-specific data as private
app.get('/api/profile', (req, res) => {
  res.set('Cache-Control', 'private, no-store');  // NEVER cache in CDN
  res.json(req.user);
});
```

### ❌ Not Invalidating After Updates

```javascript
// ❌ Update product but cache still serves old data for 5 minutes
app.put('/api/products/:id', async (req, res) => {
  await Product.findByIdAndUpdate(req.params.id, req.body);
  res.json({ success: true });
  // Cache still has old data!
});

// ✅ Invalidate cache on update
app.put('/api/products/:id', async (req, res) => {
  await Product.findByIdAndUpdate(req.params.id, req.body);
  await redis.del(`cache:products:${req.params.id}`);
  await redis.del('cache:products:list');
  res.json({ success: true });
});
```

---

## Practice Exercises

### Exercise 1: Redis Caching
Implement cache-aside pattern for your most expensive API endpoint. Measure response time before and after caching.

### Exercise 2: Cache Headers
Set appropriate Cache-Control headers for: static assets (1 year), public API (60s), private API (no cache). Verify with `curl -I`.

### Exercise 3: Hit Rate Monitoring
Add X-Cache-Status headers to your API responses. Monitor hit rate over 1 hour. Aim for > 80% on public endpoints.

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


Prev : [13 Proxies And Reverse Proxies](./13_Proxies_And_Reverse_Proxies.md) | Index: [0 Index](./0_Index.md) | Next : [15 WebSockets And Real Time](./15_WebSockets_And_Real_Time.md)
