# Performance Optimization

> 📌 **File:** 21_Performance_Optimization.md | **Level:** Full-Stack Dev → Networking Expert

---

## What is it?

Network performance optimization is about reducing latency, increasing throughput, and minimizing wasted resources across every layer of your stack. The biggest wins come from reducing round trips, caching aggressively, and understanding where time is actually spent.

---

## The Performance Budget

```
User expectation: Page loads in < 2 seconds, API responds in < 200ms

Where time goes for a typical API call (cross-continent):
┌────────────────────────────────────────────────────────┐
│  DNS lookup          │  50ms  │ ▓▓▓                    │
│  TCP handshake       │  150ms │ ▓▓▓▓▓▓▓▓               │
│  TLS handshake       │  300ms │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓        │
│  HTTP request transit│  150ms │ ▓▓▓▓▓▓▓▓               │
│  Server processing   │  100ms │ ▓▓▓▓▓                  │
│  HTTP response transit│ 150ms │ ▓▓▓▓▓▓▓▓               │
│  Total               │  900ms │                        │
├────────────────────────────────────────────────────────┤
│  Network: 800ms (89%) — Server: 100ms (11%)           │
│  Your code is only 11% of the total time!              │
│  Optimizing your Node.js code alone won't fix this.   │
└────────────────────────────────────────────────────────┘

After optimization (CDN + keep-alive + cache):
┌────────────────────────────────────────────────────────┐
│  DNS (cached)        │  0ms   │                        │
│  TCP (reused)        │  0ms   │                        │
│  TLS (resumed)       │  0ms   │                        │
│  HTTP request        │  150ms │ ▓▓▓▓▓▓▓▓               │
│  Redis cache hit     │  2ms   │ ▓                      │
│  HTTP response       │  150ms │ ▓▓▓▓▓▓▓▓               │
│  Total               │  302ms │ 66% faster!           │
└────────────────────────────────────────────────────────┘
```

---

## Optimization by Layer

### 1. DNS Optimization

```javascript
// ──── Node.js DNS caching (Node.js does NOT cache DNS by default!) ────
const CacheableLookup = require('cacheable-lookup');
const cacheable = new CacheableLookup({ maxTtl: 300 }); // 5 min cache

// Apply globally
const http = require('http');
const https = require('https');
cacheable.install(http.globalAgent);
cacheable.install(https.globalAgent);

// Next.js frontend: dns-prefetch and preconnect
// In _document.js or layout.tsx:
// <link rel="dns-prefetch" href="https://api.myapp.com" />
// <link rel="preconnect" href="https://api.myapp.com" crossorigin />
// <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
```

### 2. Connection Optimization

```javascript
// ──── HTTP Keep-Alive (reuse TCP connections) ────
const http = require('http');
const https = require('https');

// Node.js outbound: reuse connections to external services
const keepAliveAgent = new https.Agent({
  keepAlive: true,
  maxSockets: 50,        // Max concurrent connections per host
  maxFreeSockets: 10,    // Keep 10 idle connections warm
  timeout: 60000,        // Socket timeout
  freeSocketTimeout: 30000  // Close idle sockets after 30s
});

// Use with axios
const axios = require('axios');
const apiClient = axios.create({
  baseURL: 'https://api.stripe.com',
  httpsAgent: keepAliveAgent,
  timeout: 10000
});

// Express inbound: align keep-alive with ALB
const server = http.createServer(app);
server.keepAliveTimeout = 65000;  // > ALB's 60s idle timeout
server.headersTimeout = 66000;
```

### 3. Compression

```javascript
// ──── Enable compression (60-80% size reduction) ────
const compression = require('compression');

app.use(compression({
  threshold: 1024,     // Only compress responses > 1KB
  level: 6,            // Compression level (1=fast, 9=best, 6=balanced)
  filter: (req, res) => {
    // Don't compress SSE streams
    if (req.headers['accept'] === 'text/event-stream') return false;
    return compression.filter(req, res);
  }
}));

// Verify compression:
// curl -H "Accept-Encoding: gzip" -I https://api.myapp.com/api/products
// Look for: Content-Encoding: gzip
//
// Uncompressed: 50KB JSON response
// gzip: ~10KB (80% reduction)
// brotli: ~8KB (84% reduction — even better, but more CPU)
```

### 4. HTTP/2 and Connection Multiplexing

```nginx
# Nginx: Enable HTTP/2 (single connection, multiple requests)
server {
    listen 443 ssl http2;           # Enable HTTP/2
    # ...
    
    # HTTP/2 push (preload critical resources)
    location / {
        http2_push /static/css/main.css;
        http2_push /static/js/bundle.js;
        proxy_pass http://node_api;
    }
}

# CloudFront: Enable HTTP/3 (QUIC — even faster)
# Settings → Distribution → Edit → HTTP/3: Enabled
```

### 5. Response Optimization

```javascript
// ──── Pagination — don't return 10,000 records ────
app.get('/api/products', async (req, res) => {
  const { page = 1, limit = 20, fields } = req.query;
  
  // Projection — only return needed fields
  const projection = fields 
    ? fields.split(',').reduce((acc, f) => ({ ...acc, [f.trim()]: 1 }), {})
    : { name: 1, price: 1, image: 1, rating: 1 }; // Default minimal fields
  
  const products = await Product.find({ isActive: true })
    .select(projection)
    .skip((page - 1) * limit)
    .limit(limit)
    .lean();                      // Skip Mongoose overhead for read-only
  
  // Set caching headers
  res.set('Cache-Control', 'public, max-age=60, s-maxage=300');
  
  res.json({ products, page, limit });
});

// Without optimization: 500KB response (all fields, all records)
// With optimization: 10KB response (needed fields, 20 records, cached)
```

### 6. Parallel Requests

```javascript
// ──── Backend: Parallel service calls ────
app.get('/api/dashboard', async (req, res) => {
  // ❌ Sequential (3000ms total)
  // const user = await getUser(req.userId);         // 1000ms
  // const orders = await getOrders(req.userId);     // 1000ms
  // const recommendations = await getRecs(req.userId); // 1000ms

  // ✅ Parallel (1000ms total — speed of slowest)
  const [user, orders, recommendations] = await Promise.all([
    getUser(req.userId),
    getOrders(req.userId),
    getRecs(req.userId)
  ]);

  res.json({ user, orders, recommendations });
});

// ──── Frontend: Parallel API calls in React ────
// ✅ Fire all requests in parallel
useEffect(() => {
  Promise.all([
    fetch('/api/user').then(r => r.json()),
    fetch('/api/orders').then(r => r.json()),
    fetch('/api/notifications').then(r => r.json())
  ]).then(([user, orders, notifications]) => {
    setData({ user, orders, notifications });
  });
}, []);
```

### 7. Redis Caching

```javascript
// ──── Cache expensive operations ────
async function getProductsWithCache(category) {
  const cacheKey = `products:${category}`;
  
  // Check Redis (< 1ms)
  const cached = await redis.get(cacheKey);
  if (cached) return JSON.parse(cached);
  
  // Cache miss — query MongoDB (~50-200ms)
  const products = await Product.find({ category, isActive: true })
    .sort({ rating: -1 })
    .limit(50)
    .lean();
  
  // Store in Redis (TTL: 5 minutes)
  await redis.set(cacheKey, JSON.stringify(products), 'EX', 300);
  
  return products;
}

// Cache hit: 1ms response
// Cache miss: 200ms response (but next 100 requests = 1ms each)
// If 100 req/min: 99% served from cache = avg 3ms instead of 200ms
```

---

## Frontend Performance

```javascript
// ──── Next.js Performance Optimizations ────

// 1. Static generation where possible
export async function getStaticProps() {
  const products = await fetch(`${API_URL}/api/products`).then(r => r.json());
  return {
    props: { products },
    revalidate: 60  // ISR: regenerate every 60 seconds
  };
}

// 2. Image optimization
import Image from 'next/image';
<Image
  src="/product.jpg"
  width={400}
  height={300}
  loading="lazy"       // Lazy load below-fold images
  placeholder="blur"   // Show blur while loading
  priority={false}     // Set true for above-fold (LCP) images
/>

// 3. Code splitting (automatic in Next.js)
import dynamic from 'next/dynamic';
const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <Spinner />,
  ssr: false  // Don't server-render this (only needed client-side)
});

// 4. Bundle analyzer
// next.config.js
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true'
});
module.exports = withBundleAnalyzer({ /* config */ });
// Run: ANALYZE=true npm run build
```

---

## Performance Monitoring

```javascript
// ──── Server-Side: Track key metrics ────
const metrics = {
  requests: 0,
  errors: 0,
  totalDuration: 0,
  p50: [],        // 50th percentile
  slowQueries: 0
};

app.use((req, res, next) => {
  const start = Date.now();
  
  res.on('finish', () => {
    const duration = Date.now() - start;
    metrics.requests++;
    metrics.totalDuration += duration;
    
    if (res.statusCode >= 500) metrics.errors++;
    if (duration > 1000) metrics.slowQueries++;
    
    // Track p50, p95, p99
    metrics.p50.push(duration);
    if (metrics.p50.length > 1000) metrics.p50.shift();
  });
  
  next();
});

app.get('/metrics', (req, res) => {
  const sorted = [...metrics.p50].sort((a, b) => a - b);
  res.json({
    totalRequests: metrics.requests,
    errorRate: `${((metrics.errors / metrics.requests) * 100).toFixed(2)}%`,
    avgDuration: `${(metrics.totalDuration / metrics.requests).toFixed(0)}ms`,
    p50: `${sorted[Math.floor(sorted.length * 0.5)]}ms`,
    p95: `${sorted[Math.floor(sorted.length * 0.95)]}ms`,
    p99: `${sorted[Math.floor(sorted.length * 0.99)]}ms`,
    slowQueries: metrics.slowQueries
  });
});
```

---

## Common Mistakes

### ❌ N+1 API Problem

```javascript
// Frontend makes N+1 requests:
// 1 request for product list
// N requests for each product's reviews
const products = await fetch('/api/products').then(r => r.json());
for (const p of products) {
  p.reviews = await fetch(`/api/products/${p.id}/reviews`).then(r => r.json());
}
// 20 products = 21 HTTP requests = 21 × RTT!

// ✅ Backend aggregation endpoint
app.get('/api/products-with-reviews', async (req, res) => {
  const products = await Product.aggregate([
    { $lookup: { from: 'reviews', localField: '_id', foreignField: 'productId', as: 'reviews' } },
    { $addFields: { reviewCount: { $size: '$reviews' }, reviews: { $slice: ['$reviews', 3] } } }
  ]);
  res.json(products);
});
// 1 request, 1 RTT, all data included
```

### ❌ Not Using CDN for Static Assets

```
Without CDN (everything from origin):
  index.html:    200ms (origin)
  bundle.js:     200ms (origin)
  styles.css:    200ms (origin)
  10 images:     200ms × 10 (origin)
  Total: ~2.6 seconds

With CDN (static from edge):
  index.html:    10ms (edge, short cache)
  bundle.js:     10ms (edge, immutable)
  styles.css:    10ms (edge, immutable)
  10 images:     10ms × 10 (edge)
  Total: ~130ms  — 20x faster!
```

---

## Practice Exercises

### Exercise 1: Timing Audit
Use `curl -w` to measure your API's DNS, TCP, TLS, and TTFB times. Identify the biggest bottleneck and fix it.

### Exercise 2: Compression Impact
Measure your API response size with and without gzip. Calculate the bandwidth savings for 10,000 requests/day.

### Exercise 3: Caching Impact
Add Redis caching to your slowest endpoint. Measure response time before and after. Calculate the hit rate after 1 hour.

---

## Interview Q&A

**Q1: How do you reduce Time to First Byte (TTFB)?**
> CDN (serve from edge), Redis cache (skip DB queries), connection keep-alive (skip TCP/TLS handshake), HTTP/2 (multiplex requests), database query optimization (indexes, projections), and compression (smaller response = faster transfer).

**Q2: What is the difference between latency and throughput?**
> Latency = time for one request (ms). Throughput = requests processed per second. You can have high throughput with high latency (many parallel slow requests). Reducing latency usually improves throughput. Use parallel requests, caching, and CDN to improve both.

**Q3: How does HTTP/2 improve performance?**
> Multiplexes multiple requests over one TCP connection (vs 6 parallel connections in HTTP/1.1). Compresses headers (HPACK). Eliminates head-of-line blocking at HTTP level. Result: fewer connections, less overhead, 30-50% faster page loads.

**Q4: When should you use Redis cache vs CDN cache?**
> CDN: static assets, public API responses identical for all users. Redis: database query results, user-specific data, computed values, rate limiting counters. CDN is globally distributed but public; Redis is server-side and private.

**Q5: How do you handle the thundering herd problem?**
> When a cache key expires, hundreds of concurrent requests hit the DB. Solutions: cache lock (only first request queries DB, others wait), stale-while-revalidate (serve stale data while refreshing in background), random TTL jitter (prevent simultaneous expiry), pre-warming before expiry.


Prev : [20 Debugging Network Issues](./20_Debugging_Network_Issues.md) | Index: [0 Index](./0_Index.md) | Next : [22 Database Networking](./22_Database_Networking.md)
