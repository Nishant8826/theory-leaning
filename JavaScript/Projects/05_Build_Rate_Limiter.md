# 📌 Project 05 — Build a Rate Limiter

## 🌟 Introduction

If you have a popular API, you don't want a single user (or a bot) to send 1,000 requests per second and crash your server. You need a **Rate Limiter**.

Think of it like a **Nightclub Security Guard**:
-   The club has a **Capacity** (e.g., 100 people).
-   If the club is full, you have to wait outside.
-   When one person leaves, another can enter.

---

## 🏗️ 1. The Strategy: Token Bucket

The **Token Bucket** is the most popular algorithm for rate limiting.
1.  You have a bucket that can hold **N tokens**.
2.  Every time a user makes a request, they **take 1 token** from the bucket.
3.  If the bucket is empty, the request is **rejected** (Status 429: Too Many Requests).
4.  Every second, the bucket **refills** with a set number of tokens.

---

## 🏗️ 2. The Implementation

```javascript
class RateLimiter {
  constructor(maxTokens, refillRate) {
    this.maxTokens = maxTokens; // Max capacity
    this.refillRate = refillRate; // Tokens per second
    this.tokens = maxTokens; // Current tokens
    this.lastRefill = Date.now();
  }

  // Add tokens back based on how much time has passed
  refill() {
    const now = Date.now();
    const secondsPassed = (now - this.lastRefill) / 1000;
    const newTokens = secondsPassed * this.refillRate;

    this.tokens = Math.min(this.maxTokens, this.tokens + newTokens);
    this.lastRefill = now;
  }

  tryRequest() {
    this.refill();

    if (this.tokens >= 1) {
      this.tokens -= 1; // Take a token
      return true; // Request allowed
    }

    return false; // Request blocked
  }
}
```

---

## 🚀 3. Testing Your Limiter

```javascript
const limiter = new RateLimiter(5, 1); // 5 tokens max, refills 1 per second

// User sends 6 requests fast
for (let i = 1; i <= 6; i++) {
  console.log(`Request ${i}: ${limiter.tryRequest() ? "✅ OK" : "❌ BLOCKED"}`);
}

// Output:
// Request 1: ✅ OK
// Request 2: ✅ OK
// Request 3: ✅ OK
// Request 4: ✅ OK
// Request 5: ✅ OK
// Request 6: ❌ BLOCKED (Bucket empty!)
```

---

## 📐 Visualizing the Token Bucket

```text
 [ REFILL ] ──▶ (1 token/sec) ──▶ [ BUCKET ] (Max: 5)
                                     │
                                     ▼
 [ REQUEST ] ◀──(Take 1 token) ─── [ OK? ]
                                     │
                                     └─▶ NO TOKEN? ──▶ [ BLOCK ]
```

---

## 🔬 Deep Technical Dive (V8 Internals)

### Precision Timing
In the `refill()` method, we use `Date.now()`. On some systems, `Date.now()` might only be accurate to the nearest 1-10 milliseconds. For a high-speed rate limiter (handling 10,000 requests per second), this might not be precise enough. Professional rate limiters often use `performance.now()` or the `process.hrtime()` (in Node.js) to get **nanosecond** precision, ensuring that the "Refill" is perfectly smooth even at extreme speeds.

---

## 💼 Interview Tips

-   **What is Status Code 429?** It is the standard HTTP response for "Too Many Requests." You should always return this when the rate limit is hit.
-   **Where do you store tokens in production?** Not in a local variable! If you have 5 servers, each one would have its own limit. In production, we store the token count in **Redis** so all 5 servers can share the same "Bucket."
-   **What is a "Leaky Bucket"?** It's a similar algorithm where requests enter a bucket and "leak" out at a constant rate. It’s better for smoothing out "bursty" traffic.

---

## ⚖️ Trade-offs

| Algorithm | Benefit | Cost |
| :--- | :--- | :--- |
| **Token Bucket** | Allows "Bursts" of traffic (good for users). | Can be slightly unpredictable. |
| **Fixed Window** | Very simple to implement. | "Edge Case" where user sends many requests at the end of a minute and start of the next. |
| **Sliding Window** | Most accurate; no edge cases. | Very expensive to calculate in terms of memory. |

---

## 🔗 Navigation

**Prev:** [04_Build_React_Like_State.md](04_Build_React_Like_State.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [06_Real_Time_Chat.md](06_Real_Time_Chat.md)
