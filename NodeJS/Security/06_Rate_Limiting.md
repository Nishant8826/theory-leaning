# 📌 Topic: Rate Limiting

## What
### 🧠 Concept Explanation
Rate limiting is a strategy used to control the amount of incoming and outgoing traffic to or from a network. It is the "Defense against the Flood," protecting your server from both malicious attacks (DDoS) and accidental overuse (the "Slashdot effect").

**The Nightclub Bouncer Analogy (Deep Dive):**
Imagine a popular nightclub (Your Node.js Server) with a limited capacity.
*   **The Bouncer (The Rate Limiter):** He stands at the door and controls who gets in and how fast.
*   **Fixed Window (The Hourly Pass):** The bouncer says, "We only let in 100 people per hour." At 10:00 PM, he starts counting. If 100 people arrive by 10:15, the door stays shut until 11:00 PM. 
    *   **The Problem:** At 10:59, 100 people enter. At 11:01, another 100 enter. For those two minutes, the club is dangerously overcrowded (200 people).
*   **Sliding Window (The Rolling Count):** The bouncer is smarter. He looks at his watch and counts how many people have entered in the *last 60 minutes*. Every time someone wants to enter, he calculates the "Rolling Sum." This is much fairer and prevents overcrowding.
*   **Token Bucket (The Arcade Coins):** Every guest is given a bucket. Every minute, a coin drops into the bucket. To enter the club, you must "pay" a coin. If you have a bucket full of coins (because you haven't visited in a while), you can "Burst" in with several friends at once.

---

### 🏗️ Mental Model
Think of Rate Limiting as **Cost Management for your CPU and Database**.
*   **Identification:** Who are we limiting? An IP address (Good for anonymous users), a User ID (Good for logged-in users), or an API Key (Good for business partners).
*   **Thresholds:** How much is "too much"? A health check might be allowed 1,000 times/min, while a password reset is only allowed 3 times/hour.
*   **The Penalty:** What happens when they cross the line? Usually, a `429 Too Many Requests` error, but sometimes you just "slow down" (Throttle) their requests instead of blocking them.

---

## Why
### 🏢 Best Practices
1.  **Limit by User ID:** Not just IP, as IPs can be easily spoofed or shared.
2.  **Use a Sliding Window:** It's fairer and prevents "Bursting" at the edge of the window.
3.  **Provide Feedback:** Always send the `Retry-After` header so the client knows when to stop.
4.  **Tiered Limiting:** Different limits for different endpoints (e.g., `/search` is expensive, `/health` is cheap).

---

### ⚖️ Trade-offs
*   **In-Memory:** Fast, zero latency, but resets on every app restart and doesn't work with multiple instances.
*   **Redis-Based:** Works across multiple servers, persists through restarts, but adds network latency (1-2ms) to every request.

---

## How
### ⚡ Actual Behavior
When a request hits a rate-limited Node.js route:
1.  **Identity Extraction:** Node.js looks at the request. If you are behind a proxy (like Nginx or Cloudflare), it looks at the `X-Forwarded-For` header to find the *real* user IP.
2.  **State Lookup:** It checks a "Counter." This count must be stored somewhere fast. 
    *   **In-Memory:** An object like `{ "1.2.3.4": 5 }`.
    *   **Distributed:** A call to Redis.
3.  **Decision:** 
    *   **Accept:** Increment the count and let the request through.
    *   **Reject:** Stop the request and send back headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, and most importantly, `Retry-After` (how many seconds until they can try again).

---

### 🔬 Internal Mechanics (V8 + libuv + OS)
*   **Redis Atomicity:** In a microservice environment, you have multiple Node.js instances. If two requests hit two different servers at the exact same microsecond, both might see the count as `99` and let the users in, totaling `101`. We use **Redis Lua scripts** or the `INCR` command to ensure the "Check-and-Increment" happens as a single, atomic operation that cannot be interrupted.
*   **Garbage Collection in RAM:** If you use in-memory limiting, you are storing an object for every unique IP address. If a botnet with 1 million IPs attacks you, your Node.js Heap will explode with these objects. You must use a "Least Recently Used" (LRU) cache that automatically deletes old IPs to save memory.
*   **Network Overhead:** Every rate-limit check is a "Round Trip" to Redis. If your Redis is in a different data center, you are adding 50ms of latency to *every* request. High-performance gateways often keep a "Local Cache" of the Redis data to avoid the network hop for common users.
*   **The 429 Payload:** Sending a 429 response is "Cheap" for Node.js. It doesn't involve the Database or complex business logic. It's just a small header and a tiny body, allowing a single Node.js process to reject tens of thousands of malicious requests per second without breaking a sweat.

---

### 🔁 Execution Flow
1.  Request arrives from IP `1.2.3.4`.
2.  Middleware checks Redis: `GET rate_limit:1.2.3.4`.
3.  If count > 100, return `429 Too Many Requests`.
4.  If count < 100, increment count and set expiry for the window.
5.  Call `next()` to proceed to the controller.

---

### 🔍 Code Example (Latest Node.js - Using `express-rate-limit`)
```javascript
import rateLimit from 'express-rate-limit';

const apiLimiter = rateLimit({
	windowMs: 15 * 60 * 1000, // 15 minutes
	max: 100, // Limit each IP to 100 requests per `window`
	standardHeaders: true, // Return rate limit info in the `RateLimit-*` headers
	legacyHeaders: false, // Disable the `X-RateLimit-*` headers
    message: "Too many accounts created from this IP, please try again after 15 minutes",
});

// Apply the rate limiting middleware to API calls only
app.use('/api/', apiLimiter);
```

---

## Impact
### 💥 Production Failures
*   **The "Proxy" Problem:** If your app is behind a load balancer (like Nginx), the `req.ip` will be the load balancer's IP, not the user's! You will rate-limit your own infrastructure. (Solution: Trust Proxy headers like `X-Forwarded-For`).
*   **Redis Downtime:** If your rate limiter depends on Redis and Redis goes down, your whole app might crash or let everyone in. (Solution: Use a "Fail-Open" strategy if security isn't the primary goal).

---

### 🧪 Real-time Scenarios
*   **Login Protection:** Limiting login attempts to 5 per minute to prevent "Brute Force" attacks.
*   **Public APIs:** Charging users more money for higher rate limits (e.g., 1000 req/min for Pro users).

---

### ⚠️ Edge Cases
*   **Shared IPs:** Multiple users in an office or a school sharing the same public IP address might accidentally block each other.
*   **Clock Drift:** If your Redis server and App server have different times, window resets might be unpredictable.

---

---

Prev: [05_Encryption_and_TLS.md](./05_Encryption_and_TLS.md) | Index: [NodeJS/00_Index.md](../00_Index.md) | Next: [../Performance/01_Event_Loop_Latency.md](../Performance/01_Event_Loop_Latency.md)
