# 📌 Content Delivery Network (CDN)

## 🧠 Concept Explanation (Story Format)

Your server is in Virginia, USA. A user in Mumbai, India loads your React app. The HTML, CSS, JavaScript, and all images travel across the Atlantic Ocean, through undersea cables, to reach India. That's 150ms+ just for network travel time.

Now imagine storing copies of your app's static files at 200+ locations worldwide (New York, London, Tokyo, Mumbai, Sydney...). When the Mumbai user requests a file, it's served from the Mumbai CDN server — just 5ms away!

That's a **CDN (Content Delivery Network)** — a globally distributed network of servers (called "edge servers" or "Points of Presence/PoP") that cache and serve your content close to users.

**AWS CloudFront** is the CDN we use. When you deploy to S3 and add CloudFront in front — your app is instantly global!

---

## 🏗️ Basic Design (Naive — No CDN)

```
User in Mumbai
      ↓ (150ms latency + 150ms back = 300ms per request)
Origin Server in Virginia (AWS us-east-1)
      ↓
All assets served from one location

Problems:
- High latency for global users
- Origin server bandwidth costs money for every file request
- Origin server overloaded (serving files AND running business logic)
- No redundancy — origin goes down, users can't load the app
```

---

## ⚡ Optimized Design

```
User in Mumbai
      ↓ (5ms — served from local edge server!)
CDN Edge Server in Mumbai
      ↓ (only on cache miss, once per cache period)
CloudFront Distribution → S3 Origin (Virginia)
                       → API Origin (Node.js)

User in London
      ↓ (3ms)
CDN Edge Server in London
      ↓ (cache hit! No origin request)

Edge server types:
- PoP (Point of Presence): ~400+ worldwide for CloudFront
- Regional Edge Cache: Mid-tier cache between PoP and origin
```

---

## 🔍 Key Components

### What CDN Caches

```
Static Assets (cache for days/months):
✅ React/Next.js build files (JS bundles)
✅ CSS stylesheets
✅ Images (profile photos, product images)
✅ Videos (transcoded segments)
✅ Fonts
✅ Favicons, manifest files
✅ Static HTML pages

Dynamic Content (can cache for seconds/minutes):
✅ API responses that change rarely (product catalog, public feed)
✅ Pre-rendered Next.js pages

Never cache:
❌ Authenticated API responses (user-specific data)
❌ Payment endpoints
❌ Real-time data (stock prices, live scores)
❌ User-specific content (my profile, my orders)
```

### Cache-Control Headers

```javascript
// Node.js Express — set caching headers
app.use(express.static('public', {
  maxAge: '1y',  // Static assets: cache for 1 year!
  etag: false    // Use Cache-Control instead of ETag
}));

// For API responses
app.get('/api/products', async (req, res) => {
  res.set({
    'Cache-Control': 'public, max-age=300, s-maxage=300', // 5 min for CDN, 5 min for browser
    'Vary': 'Accept-Encoding',  // Cache different versions for compressed vs uncompressed
    'ETag': generateEtag(products)  // Client can check if content changed
  });
  res.json(products);
});

// For authenticated endpoints (don't cache!)
app.get('/api/me', authenticate, (req, res) => {
  res.set('Cache-Control', 'private, no-store');  // Only browser, no CDN caching
  res.json(req.user);
});

// For real-time data
app.get('/api/live-scores', (req, res) => {
  res.set('Cache-Control', 'no-cache, no-store, must-revalidate');
  res.json(scores);
});
```

### AWS CloudFront Setup

```javascript
// Terraform (or AWS Console) for CloudFront configuration

// Cache behavior for static assets (S3 origin)
static_assets_behavior = {
  path_pattern: "/static/*",
  compress: true,
  cache_policy: {
    default_ttl: 86400,    // 24 hours default cache
    max_ttl: 31536000,     // 1 year max cache
    min_ttl: 0
  }
}

// Cache behavior for API (Node.js origin)
api_behavior = {
  path_pattern: "/api/*",
  allowed_methods: ["GET", "HEAD", "OPTIONS", "PUT", "PATCH", "POST", "DELETE"],
  cache_policy: {
    default_ttl: 0,        // Don't cache API by default
    max_ttl: 0
  },
  origin_request_policy: "forward_all_headers"  // Forward auth headers to origin
}

// Cache behavior for Next.js pages (S3 origin)
pages_behavior = {
  path_pattern: "/_next/*",
  compress: true,
  cache_policy: {
    default_ttl: 31536000,  // Cache Next.js assets forever (they have content hash in filename!)
    max_ttl: 31536000
  }
}
```

### Cache Invalidation

When you deploy a new version, how do users get the new files?

```javascript
// Strategy 1: Content-based cache busting (BEST)
// Next.js does this automatically!
// Old: /static/js/main.abc123.js → cached for 1 year
// New: /static/js/main.xyz789.js → new filename = instant cache miss
// Users always get the new version without any invalidation needed!

// Strategy 2: CloudFront Invalidation (manual, slower)
const cloudfront = new AWS.CloudFront();
await cloudfront.createInvalidation({
  DistributionId: process.env.CLOUDFRONT_DISTRIBUTION_ID,
  InvalidationBatch: {
    Paths: {
      Quantity: 1,
      Items: ['/index.html']  // Invalidate specific files
      // Items: ['/*']        // Invalidate ALL files (costs money, takes time)
    },
    CallerReference: Date.now().toString()
  }
}).promise();

// Strategy 3: Short TTL for frequently updated content
// Cache product catalog for 5 minutes instead of 1 day
// After 5 minutes, next request goes to origin automatically
```

### CDN for API Caching

```javascript
// Not just for static files — cache API responses too!

// Approach: Vary cache by query params
app.get('/api/products', async (req, res) => {
  const { category, page, sort } = req.query;
  const cacheKey = `products:${category}:${page}:${sort}`;
  
  // Check Redis first (for Node.js-level caching)
  const cached = await redis.get(cacheKey);
  if (cached) {
    res.set('X-Cache', 'HIT'); // Debug header
    return res.json(JSON.parse(cached));
  }
  
  const products = await db.getProducts({ category, page, sort });
  
  await redis.setex(cacheKey, 300, JSON.stringify(products));
  
  // Also allow CloudFront to cache this for 5 minutes
  res.set('Cache-Control', 'public, max-age=300, s-maxage=300');
  res.set('X-Cache', 'MISS');
  res.json(products);
});
```

---

## ⚖️ Trade-offs

| With CDN | Without CDN |
|----------|-------------|
| Fast globally (5-50ms) | Slow globally (100-300ms) |
| Reduced origin load | Origin handles all traffic |
| Cheap bandwidth | Expensive bandwidth |
| High availability | Origin = SPOF for static assets |
| Stale content risk | Always fresh |
| Cost for CDN service | No CDN cost |

---

## 📊 Scalability Discussion

### CDN Benefits by Numbers

```
Without CDN (server in Virginia):
  - Mumbai user: ~200ms latency per request
  - London user: ~80ms latency
  - NYC user: ~10ms latency
  - Server bandwidth cost: 100% from one location

With CloudFront:
  - Mumbai user: ~15ms (edge in Mumbai)
  - London user: ~8ms (edge in London)
  - NYC user: ~3ms (edge nearby)
  - Server bandwidth cost: only cache misses (~5-10% of requests)
  - 90-95% of traffic served from CDN without touching your server!

Bandwidth cost:
  - S3: $0.023/GB
  - CloudFront: $0.0085/GB (to internet) + reduced S3 requests
  - Plus: CloudFront provides DDoS protection!
```

### Next.js + CloudFront Setup

```javascript
// next.config.js
module.exports = {
  output: 'standalone',  // For Docker deployment
  
  // Configure CDN for assets
  assetPrefix: process.env.CLOUDFRONT_URL,  // https://d111111abcdef8.cloudfront.net
  
  // Configure image optimization
  images: {
    domains: ['your-s3-bucket.s3.amazonaws.com'],
    loader: 'cloudfront',  // Use CloudFront for Next/Image optimization
  }
};

// Images via CloudFront:
import Image from 'next/image';
function ProfilePhoto({ user }) {
  return (
    <Image
      src={user.avatarUrl}  // CloudFront URL
      alt={user.name}
      width={150}
      height={150}
      // Next.js automatically optimizes + serves via CDN
    />
  );
}
```

---

## 💼 Interview Questions (WITH SOLUTIONS)

### Q1: What is a CDN and why do we use it?

**Solution:**
A CDN is a globally distributed network of servers that caches and serves content close to users. Benefits:
1. **Reduced latency:** Content served from edge server near user (5-50ms vs 200ms)
2. **Reduced origin load:** 90%+ of requests served from CDN cache
3. **DDoS protection:** CDN absorbs traffic spikes, protects origin
4. **Global availability:** If origin is down, CDN can serve cached content
5. **Cost savings:** CDN bandwidth is cheaper than server bandwidth

AWS CloudFront is our CDN — integrate with S3 (static files) and EC2/Lambda (dynamic API with caching).

---

### Q2: How does CloudFront know which content to cache?

**Solution:**
CloudFront uses **cache behaviors** — rules that define how different URL patterns are handled:

1. **Cache-Control headers:** Origin (Node.js/S3) sends `Cache-Control: max-age=3600` → CloudFront caches for 1 hour
2. **Default TTL:** If origin sends no Cache-Control → use CloudFront default TTL
3. **Whitelist query strings:** Cache different versions based on `?lang=en` vs `?lang=fr`
4. **Whitelist headers:** Cache different versions based on `Accept-Language` header
5. **Cache keys:** By default, CloudFront caches by URL. Can customize to include query params, headers, cookies.

```
GET /api/products → cache key = /api/products → same response for everyone
GET /api/products?category=books → cache key = /api/products?category=books → different cache
GET /api/me (with Authorization header) → MUST NOT cache (user-specific!)
```

---

### Q3: What is the difference between a CDN's edge cache and a browser cache?

**Solution:**
| | Browser Cache | CDN Edge Cache |
|-|--------------|----------------|
| Location | User's browser | CDN server globally |
| Scope | One user | All users at that edge |
| Control | `Cache-Control: private` | `Cache-Control: s-maxage` |
| Invalidation | User clears cache | CDN invalidation API |
| Size | MB to GB | TB per edge location |

Example:
- Browser cache: Your profile photo is cached in YOUR browser. No one else sees it.
- CDN cache: A popular product image is cached at the Mumbai edge. ALL Mumbai users share this cache!

Use `public, max-age=60, s-maxage=3600` to:
- Browser caches for 60 seconds
- CDN caches for 1 hour (all users)

---

### Q4: How do you handle cache invalidation in a CDN?

**Solution:**
1. **Content-based filenames (best):** Include file hash in filename.
   - `main.abc123.js` → `main.xyz789.js` (new hash on every build)
   - Old filename → cached forever. New filename → immediate miss.
   - Next.js, Webpack do this automatically!

2. **Short TTL for frequently changing content:**
   - Product prices: `max-age=60` (refresh every minute)
   - News articles: `max-age=300` (refresh every 5 minutes)

3. **CloudFront Invalidation API (for emergencies):**
   - Remove specific files from all edge caches
   - Takes 2-10 minutes to propagate globally
   - First 1000 invalidation paths/month are free, then $0.005/path

4. **Versioned API paths:**
   - `/api/v1/products` → when you update product response format → `/api/v2/products`
   - Old path stays cached (old clients), new path starts fresh (new clients)

---

### Q5: When would you NOT want to use a CDN?

**Solution:**
Don't cache through CDN:
1. **User-specific authenticated data:** `GET /api/me` — different for every user
2. **Real-time data:** Live chat messages, live sports scores, stock prices
3. **POST/PUT/DELETE requests:** Mutating requests shouldn't be cached
4. **Security-sensitive data:** Tokens, passwords — never in cache
5. **Admin/internal APIs:** No external CDN for internal services
6. **Already fast data:** If origin is in same region and data is in Redis → CDN latency overhead may not be worth it

Practical example: Instagram
- CDN serves: photos, videos, JS, CSS (static files)
- Direct to server: Liking a post, posting a comment, your personalized feed API

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem 1: Design the CDN strategy for a Next.js e-commerce app

**Solution:**
```
CloudFront Distribution Setup:

1. Static Next.js Assets (/_next/static/*):
   → Origin: S3 bucket
   → Cache: 1 year (content hash in filename)
   → Compress: Yes (gzip/brotli)

2. Product Images (/images/*):
   → Origin: S3 bucket  
   → Cache: 7 days (product images change rarely)
   → Compress: Yes
   → Resize on-the-fly: CloudFront Function or Lambda@Edge

3. Product Catalog API (/api/products*):
   → Origin: Node.js on EC2/Lambda
   → Cache: 5 minutes (prices can change)
   → Vary by: query strings (category, page, sort)
   → No auth required → safe to cache publicly

4. User-Specific APIs (/api/cart, /api/orders, /api/me):
   → Origin: Node.js on EC2
   → Cache: NONE (user-specific!)
   → Forward: Authorization header to origin

5. Checkout (/api/payment*):
   → Origin: Node.js on EC2
   → Cache: NONE (financial data, always fresh)

Result:
- Product browsing: ~10ms globally (from CDN)
- Checkout: ~100ms (real-time, goes to origin)
- Images load instantly (cached at edge)
- Monthly bandwidth costs reduced by 80%+
```

---

### Problem 2: Your CDN is serving stale product prices (showing $100 when price is now $80). How do you fix it?

**Solution:**
```
Immediate fix:
1. CloudFront Invalidation:
   aws cloudfront create-invalidation \
     --distribution-id E1234567 \
     --paths "/api/products/*"
   → Takes 2-10 minutes, affects all edge servers

Better long-term solutions:

Option A: Shorter TTL
   Change: max-age=3600 → max-age=60
   Trade-off: More requests to origin (higher cost, slightly higher latency)

Option B: Surrogate keys / Cache tags (advanced CDN feature)
   When product 123 is updated → invalidate only the cache entries tagged "product:123"
   aws cloudfront create-invalidation --paths "/api/products/123" "/api/products?featured=true"

Option C: Skip CDN for pricing, use it only for non-price data
   - Cache product descriptions, images, reviews → CDN (stable data)
   - Fetch price separately from origin (always fresh) → combine in React
   
Option D: Use stale-while-revalidate
   Cache-Control: public, max-age=5, stale-while-revalidate=55
   → Serve stale content for up to 55 more seconds while fetching fresh data in background
   → User sees slightly stale data but no latency hit

For a shopping app, Option C is best:
   - Cache product info (name, description) for 1 hour
   - Fetch price from origin always (or short 30s cache)
   - Users never see wrong price, but still get fast product page loads
```

---

### Navigation
**Prev:** [18_Storage_Systems.md](18_Storage_Systems.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [20_Search_Design.md](20_Search_Design.md)
