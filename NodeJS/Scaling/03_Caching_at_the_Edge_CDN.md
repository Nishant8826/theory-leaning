# 📌 03 — Caching at the Edge (CDN): Global Latency Reduction

## 🧠 Concept Explanation

### Basic → Intermediate
A Content Delivery Network (CDN) is a distributed network of servers (Edge Locations) that deliver content to users based on their geographic location. It stores static assets like images, CSS, and JS files closer to the user to reduce latency.

### Advanced → Expert
At a staff level, we use the CDN to cache **Dynamic Content** using the `Cache-Control` and `Surrogate-Control` headers.
1. **Edge Locations**: Servers located in cities around the world.
2. **Time to Live (TTL)**: How long the CDN should keep a copy of the data.
3. **Invalidation (Purging)**: Telling the CDN to delete a cached file because the data has changed.

The goal is to move the "Read" load away from your Node.js servers entirely for frequently accessed data.

---

## 🏗️ Common Mental Model
"CDNs are only for images and videos."
**Correction**: Modern CDNs (Cloudflare, Fastly, Akamai) can cache **API JSON responses**. If your `/api/top-products` is the same for all users, caching it at the edge for 1 minute can reduce your server load by 99%.

---

## ⚡ Actual Behavior: The "Vary" Header
Caching becomes complex when the response depends on a header (e.g. `Accept-Language` or `Authorization`). The `Vary` header tells the CDN: "Only serve this cached copy if these specific headers match the original request."

---

## 🔬 Internal Mechanics (Networking + HTTP)

### Shared vs Private Cache
- **`public`**: The response can be cached by CDNs and browsers.
- **`private`**: The response contains user-specific data and should **only** be cached by the user's browser, never by a shared CDN.

### stale-while-revalidate
A powerful `Cache-Control` directive. It tells the CDN: "Serve the stale (old) data immediately, but in the background, fetch a fresh copy from the origin server for the next user." This provides 0ms latency for the user while keeping the cache fresh.

---

## 📐 ASCII Diagrams

### CDN Edge Caching
```text
  USER (London) ──▶ [ EDGE: London ] ──(Miss)─▶ [ ORIGIN: New York ]
                                                    │
  USER (London) ◀── [ EDGE: London ] ◀──(Cache)─────┘
                          │
                          ▼ (Next User in London)
  USER 2 (London) ──▶ [ EDGE: London ] ──▶ (HIT - 10ms)
```

---

## 🔍 Code Example: Setting Cache Headers in Express
```javascript
app.get('/api/products', (req, res) => {
  const products = getProducts();
  
  // 1. Cache for 1 hour at the CDN
  // 2. Allow serving stale data for up to 10 mins while revalidating
  res.set('Cache-Control', 'public, max-age=3600, stale-while-revalidate=600');
  
  res.json(products);
});

// For user-specific data: NEVER CACHE AT EDGE
app.get('/api/me', (req, res) => {
  res.set('Cache-Control', 'private, no-cache');
  res.json(req.user);
});
```

---

## 💥 Production Failures & Debugging

### Scenario: The "Private Data Leak"
**Problem**: User A logs in and sees User B's profile information.
**Reason**: You set `Cache-Control: public` on a user-specific API. The CDN cached User B's response and served it to User A.
**Fix**: Always use `private` or `no-store` for any endpoint that requires authentication.

### Scenario: The "Eternal" Cache
**Problem**: You updated an image on your server, but users are still seeing the old version.
**Reason**: The image has a `max-age` of 1 year and you haven't triggered a "Purge" on the CDN.
**Fix**: Use **Content Hashing** in filenames (e.g. `logo.a1b2c3.png`). When the content changes, the filename changes, bypassing the old cache automatically.

---

## 🧪 Real-time Production Q&A

**Q: "Should we use Cloudflare Workers or Lambda@Edge?"**
**A**: **Yes, for high-performance logic.** These allow you to run small snippets of code (like A/B testing or Header modification) directly at the edge location, avoiding the trip to your origin server entirely.

---

## 🏢 Industry Best Practices
- **Content Hashing**: For all static assets.
- **Normalize Headers**: Ensure your CDN ignores irrelevant query parameters (like UTM tracking tags) to increase the **Cache Hit Ratio**.

---

## 💼 Interview Questions
**Q: What is the "Thundering Herd" problem in CDNs?**
**A**: It's when a cache key expires and multiple edge locations all request the data from the origin server at the same time. Modern CDNs use **Request Collapsing** to ensure only one request goes to the origin for that specific key.

---

## 🧩 Practice Problems
1. Use `curl -I` to inspect the `CF-Cache-Status` or `X-Cache` headers of a popular website.
2. Implement `stale-while-revalidate` in an Express app and observe the behavior using the Network tab in Chrome.

---

**Prev:** [02_Load_Balancing_Strategies.md](./02_Load_Balancing_Strategies.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [04_Database_Sharding_and_Partitioning.md](./04_Database_Sharding_and_Partitioning.md)
