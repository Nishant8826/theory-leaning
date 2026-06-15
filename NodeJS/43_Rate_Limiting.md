# Rate Limiting

## What You Will Learn
* The purpose of Rate Limiting in secure backend systems.
* Rate Limiting Algorithms (Fixed Window, Sliding Window, Token Bucket, Leaky Bucket).
* Configuring standard rate limit response headers.
* Building high-performance, Redis-backed rate limiting middleware in Express.

## Why This Matters
Exposing APIs without rate limits makes them vulnerable to brute-force login attacks, scraping, and Denial of Service (DDoS) attempts. An attacker can write a simple script that sends thousands of requests per second, exhausting server resources and crashing your application. Rate limiting blocks abusive clients at the request boundary, keeping your services stable and responsive for genuine users.

## Theory

### Rate Limiting Algorithms
1. **Fixed Window Counter**:
   * *Concept*: Divides time into fixed intervals (e.g. 1 minute). A counter tracks request volume per client within the active window.
   * *Pros*: Simple, fast lookup.
   * *Cons*: Traffic spikes can occur at the boundary of two windows, allowing double the allowed request volume within a short period.
2. **Sliding Window Counter**:
   * *Concept*: Tracks request timestamps dynamically using a sliding window. Resolves the boundary spike issue of the fixed window counter.
3. **Token Bucket**:
   * *Concept*: A bucket holds a maximum number of tokens. Every request consumes a token. Tokens are added back to the bucket at a constant rate.
   * *Pros*: Handles bursts of traffic while enforcing a constant limit.
4. **Leaky Bucket**:
   * *Concept*: Requests enter a queue. The queue processes and releases requests at a constant, steady rate.
   * *Pros*: Smooths out traffic spikes, keeping load predictable.

### Rate Limit Response Headers
Standard APIs communicate rate limit status using response headers:
* **`X-RateLimit-Limit`**: The maximum number of requests allowed within the time window.
* **`X-RateLimit-Remaining`**: The number of remaining requests allowed within the active window.
* **`X-RateLimit-Reset`**: The Unix epoch timestamp indicating when the rate limit counter resets.

When a client exceeds the limit, the server rejects the request with a **`429 Too Many Requests`** status code and returns a `Retry-After` header.

## Deep Dive

### Redis-Backed Rate Limiting
In distributed applications, in-memory rate limiting (storing counters in the Node.js process RAM) fails because requests are routed across multiple servers. Using **Redis** as a shared store allows all server instances to verify and update counters in a single location:
* **Atomic Operations**: Using atomic operations like `MULTI`, `INCR`, and `EXPIRE` ensures that rate limiting checks do not suffer from race conditions.

## Visual Explanation

### Sliding Window vs. Fixed Window Boundary Spike
```text
Limit: 100 requests per minute.

Fixed Window Counter (Spike Vulnerability):
Window A: [00:00 - 01:00] (User sends 100 requests at 00:59)
Window B: [01:00 - 02:00] (User sends 100 requests at 01:01)
  - Result: User executes 200 requests within a 2-second window! This bypasses the rate limit.

Sliding Window Counter (Smooth Enforcement):
Tracks request timestamps dynamically.
User sends request at 01:01 ── Checks window: [00:01 - 01:01] ── Active requests: 100 ──> Blocked!
```

## Real-World Example
Consider a login endpoint `/api/login`. You want to prevent brute-force attacks by limiting users to 5 login attempts per minute. You write rate-limiting middleware that uses the client's IP address and email as the key. If they exceed 5 attempts, the middleware returns a `429` status code and blocks further requests, protecting user accounts.

## Code Examples

### Redis Sliding Window Counter Rate Limiter Middleware

```javascript
// middleware/rateLimiter.js
const { redisClient } = require('../db/redisClient');
const AppError = require('../utils/AppError');

// Sliding Window Counter Rate Limiter Middleware
const rateLimiter = (maxRequests, windowSeconds) => {
  return async (req, res, next) => {
    // 1. Identify client using IP address
    const clientIp = req.ip || req.headers['x-forwarded-for'] || req.socket.remoteAddress;
    const clientKey = `rate:limit:${clientIp}:${req.route.path}`;

    try {
      const now = Date.now();
      const clearBefore = now - (windowSeconds * 1000);

      // Execute atomic multi transaction in Redis
      // zAdd: add active request timestamp
      // zRemRangeByScore: clear expired request timestamps
      // zCard: get active request count
      const [ , , activeRequestsCount ] = await redisClient.multi()
        .zAdd(clientKey, { score: now, value: now.toString() })
        .zRemRangeByScore(clientKey, 0, clearBefore)
        .zCard(clientKey)
        .expire(clientKey, windowSeconds) // Clean up key if idle
        .exec();

      const remaining = maxRequests - activeRequestsCount;

      // 2. Set standard Rate Limiting response headers
      res.setHeader('X-RateLimit-Limit', maxRequests);
      res.setHeader('X-RateLimit-Remaining', Math.max(0, remaining));
      res.setHeader('X-RateLimit-Reset', Math.ceil((now + (windowSeconds * 1000)) / 1000));

      // 3. Block client if they exceed limits
      if (activeRequestsCount > maxRequests) {
        res.setHeader('Retry-After', windowSeconds);
        return next(new AppError('Too Many Requests: Rate limit exceeded.', 429));
      }

      next();
    } catch (err) {
      console.error('Rate limiting error:', err.message);
      next(); // Fallback: allow requests if cache fails in production
    }
  };
};

module.exports = rateLimiter;
```

```javascript
// app.js
const express = require('express');
const { connectRedis } = require('./db/redisClient');
const rateLimiter = require('./middleware/rateLimiter');

const app = express();

// Apply rate limiting to secure endpoints
// Limits clients to 10 requests per minute
app.get('/api/resource', rateLimiter(10, 60), (req, res) => {
  res.json({ message: 'Request succeeded' });
});

app.use((err, req, res, next) => {
  res.status(err.statusCode || 500).json({ error: err.message });
});

app.listen(3000, async () => {
  await connectRedis();
  console.log('Rate limiter server running on port 3000');
});
```

## Best Practices
* **Use Shared Stores (Redis)**: Do not use in-memory rate limiting in production. Use a shared memory store like Redis to ensure limits are enforced consistently across all application servers.
* **Fallback Gracefully**: Ensure that rate limiting failures do not block requests. If Redis crashes, log the error and allow requests to bypass rate limiting, keeping the application online.
* **Determine Client IPs securely**: If your application is deployed behind a proxy (like Nginx, Cloudflare, or AWS ELB), configure `app.set('trust proxy', true)` in Express to read client IPs from the `X-Forwarded-For` header instead of the proxy server IP.

## Interview Questions

### Beginner
* **What is the purpose of rate limiting?**
  *Answer*: Rate limiting controls the volume of incoming requests to an API. It protects servers from brute-force login attacks, scraping, resource abuse, and Denial of Service (DDoS) attempts.

### Intermediate
* **Which HTTP status code is returned when a client exceeds their rate limit, and what headers should the response include?**
  *Answer*: The server returns a **`429 Too Many Requests`** status code. The response should include rate limit headers like `X-RateLimit-Limit` (max limit), `X-RateLimit-Remaining` (remaining requests), `X-RateLimit-Reset` (time until reset), and a `Retry-After` header telling the client how long to wait before retrying.

### Advanced
* **Why is in-memory rate limiting (using process RAM) an anti-pattern for scaled production architectures? How does Redis solve this?**
  *Answer*: In-memory rate limiting stores request counters in the local RAM of the server process. If you run multiple server instances behind a load balancer, each server will track counters independently, allowing clients to bypass limits by distributing requests across servers. 
  Additionally, counters are reset when a server restarts. Redis solves this by serving as a shared memory store, allowing all application instances to read and update rate limits in a single, centralized location.

### Senior Architect
* **How would you architecture a tiered rate-limiting framework at the API Gateway level to manage different tiers of clients (e.g. anonymous, standard, and enterprise tier clients)?**
  *Answer*: To build a tiered rate-limiting framework:
  1. **Enforce at Gateway**: Handle rate limiting at the API Gateway layer (using tools like Kong or AWS API Gateway) to block requests before they reach your application servers.
  2. **Authenticate Early**: Identify and authenticate clients early in the request pipeline to determine their subscription tier.
  3. **Read Tiers dynamically**: Retrieve the client's rate limits from a fast cache (like Redis) based on their subscription tier:
     - Anonymous users: Limit by IP address (e.g. 60 requests per minute).
     - Standard tier: Limit by API Key or User ID (e.g. 1,000 requests per minute).
     - Enterprise tier: High limits or dedicated capacity (e.g. 10,000 requests per minute).
  4. Use Redis sliding window counters to track request counts. If a client exceeds their tier limit, return a `429` status code and a `Retry-After` header, ensuring fair resource distribution across tiers.

---
Previous : [42_Caching.md] | Index : [00_index.md] | Next : [44_File_Uploads.md]
