# Performance Optimization

> 📌 **File:** 24_Performance_Optimization.md | **Level:** Full-Stack Dev → Networking Expert

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

#### Diagram Explanation (The Delivery Route)
Think of an API request like ordering an item for delivery:
- **Before Optimization:** You look up the warehouse address in a phone book (DNS), drive your truck to the warehouse to shake hands with the manager (TCP/TLS), and then request the package (HTTP). The warehouse packaging time is only 11% of the total trip!
- **After Optimization (CDN + Caching):** You build a mini-warehouse locally (CDN/Redis). The address is memorized (DNS cached), and the delivery driver has an open pre-approved connection (TCP reused). You cut out the geographical commute!

---

## Optimization by Layer

### 1. DNS Optimization
```javascript
// Node.js DNS caching (Node.js does NOT cache DNS by default!)
const CacheableLookup = require('cacheable-lookup');
const cacheable = new CacheableLookup({ maxTtl: 300 });

const http = require('http');
const https = require('https');
cacheable.install(http.globalAgent);
cacheable.install(https.globalAgent);
```

### 2. Connection Optimization (HTTP Keep-Alive)
```javascript
const https = require('https');

const keepAliveAgent = new https.Agent({
  keepAlive: true,
  maxSockets: 50,
  maxFreeSockets: 10,
  timeout: 60000
});

const axios = require('axios');
const apiClient = axios.create({
  baseURL: 'https://api.stripe.com',
  httpsAgent: keepAliveAgent
});
```

### 3. Compression (Express gzip)
```javascript
const compression = require('compression');
app.use(compression({
  threshold: 1024,
  level: 6
}));
```

### 4. Response Optimization (Pagination & Projection)
```javascript
app.get('/api/products', async (req, res) => {
  const { page = 1, limit = 20 } = req.query;
  const products = await Product.find({ isActive: true })
    .select({ name: 1, price: 1, image: 1 })
    .skip((page - 1) * limit)
    .limit(limit)
    .lean(); // Skip Mongoose heavy wrappers
  
  res.set('Cache-Control', 'public, max-age=60, s-maxage=300');
  res.json({ products, page, limit });
});
```

---

## Practice Exercises

### Exercise 1: Timing Audit
Use `curl -w` to measure your API's DNS, TCP, TLS, and TTFB times. Identify the biggest bottleneck and fix it.

### Exercise 2: Compression Verification
Verify compression headers on your endpoints. Compare payload size with and without gzip enabled.

---

## Interview Q&A

**Q1: How do you reduce Time to First Byte (TTFB)?**
> CDN (serve from edge), Redis cache (skip DB queries), connection keep-alive (skip TCP/TLS handshake), HTTP/2 (multiplex requests), database query optimization (indexes, projections), and compression.

**Q2: What is the difference between latency and throughput?**
> Latency = time for one request (ms). Throughput = requests processed per second. You can have high throughput with high latency (many parallel slow requests). Reducing latency usually improves throughput.

**Q3: How does HTTP/2 improve performance?**
> Multiplexes multiple requests over one TCP connection. Compresses headers (HPACK). Eliminates head-of-line blocking at HTTP level, reducing overhead and speeding up page loads.

**Q4: When should you use Redis cache vs CDN cache?**
> CDN: static assets, public API responses identical for all users. Redis: database query results, user-specific data, computed values, rate limiting counters.

**Q5: How do you handle the thundering herd problem?**
> When a cache key expires, hundreds of concurrent requests hit the DB. Solutions: cache lock (only first query runs, others wait), stale-while-revalidate (serve stale data while refreshing), and random TTL jitter.

---

Prev : [23 Debugging Network Issues](./23_Debugging_Network_Issues.md) | Index: [00 Index](./00_Index.md) | Next : [25 Network Monitoring And Observability](./25_Network_Monitoring_And_Observability.md)
