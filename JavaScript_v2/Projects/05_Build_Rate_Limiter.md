# 📌 Project 05 — Build Rate Limiter

## 🎯 Goal

Implement multiple rate limiting algorithms: Token Bucket, Sliding Window, Fixed Window. These are essential for API protection in production.

## ✅ Complete Solutions

### Token Bucket

```javascript
class TokenBucketRateLimiter {
  constructor({ capacity, refillRate, refillIntervalMs = 1000 }) {
    this.capacity = capacity
    this.tokens = capacity
    this.refillRate = refillRate
    this.lastRefill = Date.now()
  }
  
  _refill() {
    const now = Date.now()
    const elapsed = now - this.lastRefill
    const tokensToAdd = Math.floor(elapsed / 1000) * this.refillRate
    this.tokens = Math.min(this.capacity, this.tokens + tokensToAdd)
    if (tokensToAdd > 0) this.lastRefill = now
  }
  
  consume(tokens = 1) {
    this._refill()
    if (this.tokens >= tokens) {
      this.tokens -= tokens
      return true
    }
    return false
  }
  
  getRetryAfterMs() {
    const tokensNeeded = 1 - this.tokens
    return Math.ceil(tokensNeeded / this.refillRate * 1000)
  }
}
```

### Sliding Window

```javascript
class SlidingWindowRateLimiter {
  constructor({ windowMs, maxRequests }) {
    this.windowMs = windowMs
    this.maxRequests = maxRequests
    this.requests = new Map()  // clientId → timestamp[]
  }
  
  allow(clientId) {
    const now = Date.now()
    const windowStart = now - this.windowMs
    
    // Get/init client's request timestamps
    let timestamps = this.requests.get(clientId) || []
    
    // Remove expired timestamps
    timestamps = timestamps.filter(ts => ts > windowStart)
    
    if (timestamps.length >= this.maxRequests) {
      this.requests.set(clientId, timestamps)
      return { allowed: false, remaining: 0, retryAfter: timestamps[0] + this.windowMs - now }
    }
    
    timestamps.push(now)
    this.requests.set(clientId, timestamps)
    
    return { allowed: true, remaining: this.maxRequests - timestamps.length, retryAfter: 0 }
  }
  
  cleanup() {
    const now = Date.now()
    for (const [clientId, timestamps] of this.requests.entries()) {
      const valid = timestamps.filter(ts => ts > now - this.windowMs)
      if (valid.length === 0) this.requests.delete(clientId)
      else this.requests.set(clientId, valid)
    }
  }
}
```

## 🔗 Navigation

**Prev:** [04_Build_React_Like_State.md](04_Build_React_Like_State.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [06_Real_Time_Chat.md](06_Real_Time_Chat.md)
