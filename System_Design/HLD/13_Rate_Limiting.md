# 📌 Rate Limiting

## 🧠 Concept Explanation (Story Format)

You built a Node.js API. One morning, a competitor's bot is sending 10,000 requests/second to your API. Your server crashes. Real users can't access your app.

Or: A user's account is being brute-forced — someone is trying 1,000 different passwords. Without rate limiting, they'll eventually succeed.

**Rate limiting** is the guard at the door: "You've had your 100 requests this minute. Come back later."

Twitter limits: 300 tweets per 3 hours. GitHub API: 5,000 requests/hour per user. AWS API Gateway: 10,000 RPS by default.

Rate limiting protects your system from:
- DDoS attacks
- API abuse
- Brute force attacks
- Cost overruns (Lambda, API calls)
- Ensuring fair usage across users

---

## 🏗️ Basic Design (Naive)

```javascript
// ❌ In-memory rate limiting — broken with multiple servers!
const requestCounts = {};

app.use((req, res, next) => {
  const ip = req.ip;
  requestCounts[ip] = (requestCounts[ip] || 0) + 1;
  
  if (requestCounts[ip] > 100) {
    return res.status(429).json({ error: 'Rate limit exceeded' });
  }
  next();
});

// Problem: Each Node.js server has its own counter!
// Server 1: User has sent 90 requests
// Server 2: User has sent 90 requests (different counter!)
// Total: 180 requests — but server thinks only 90!
```

---

## ⚡ Optimized Design

```
Rate Limiting Architecture:

User Request
      ↓
AWS API Gateway ← Global rate limit (first defense)
      ↓
[AWS WAF] ← Block IPs, countries
      ↓
ALB Load Balancer
      ↓
Node.js Server → [Redis] ← Shared counter for ALL servers!
                           Key: "ratelimit:{userId}:{window}"
                           Value: request count
                           TTL: window duration
```

---

## 🔍 Key Components

### Rate Limiting Algorithms

**1. Fixed Window Counter (Simplest)**
```javascript
// Count requests in a fixed time window (e.g., per minute)
async function fixedWindowRateLimit(userId, limit = 100, windowSeconds = 60) {
  const windowStart = Math.floor(Date.now() / 1000 / windowSeconds);
  const key = `ratelimit:${userId}:${windowStart}`;
  
  const count = await redis.incr(key);
  if (count === 1) {
    await redis.expire(key, windowSeconds); // Set TTL on first request
  }
  
  return count <= limit;
}

// Problem: "Boundary burst" attack
// Window resets at :00 every minute
// Attacker sends 100 requests at 0:59, 100 more at 1:01 → 200 requests in 2 seconds!
```

**2. Sliding Window Log (Most Accurate)**
```javascript
// Track timestamps of each request
async function slidingWindowRateLimit(userId, limit = 100, windowMs = 60000) {
  const now = Date.now();
  const windowStart = now - windowMs;
  const key = `ratelimit:log:${userId}`;
  
  // Remove old entries
  await redis.zremrangebyscore(key, 0, windowStart);
  
  // Count requests in window
  const count = await redis.zcard(key);
  
  if (count >= limit) {
    return false; // Rate limit exceeded
  }
  
  // Add current request
  await redis.zadd(key, now, `${now}-${Math.random()}`);
  await redis.expire(key, Math.ceil(windowMs / 1000));
  
  return true;
}

// Accurate but memory-intensive (stores every request timestamp)
```

**3. Sliding Window Counter (Best Balance)**
```javascript
// Approximate sliding window using two fixed windows
async function slidingWindowCounterRateLimit(userId, limit = 100, windowSeconds = 60) {
  const now = Math.floor(Date.now() / 1000);
  const currentWindow = Math.floor(now / windowSeconds);
  const previousWindow = currentWindow - 1;
  const elapsedInWindow = now % windowSeconds;
  
  const currentKey = `ratelimit:${userId}:${currentWindow}`;
  const previousKey = `ratelimit:${userId}:${previousWindow}`;
  
  const [currentCount, previousCount] = await Promise.all([
    redis.get(currentKey),
    redis.get(previousKey)
  ]);
  
  // Weighted count: current + (previous * remaining_fraction)
  const weightedCount = parseInt(currentCount || 0) + 
    parseInt(previousCount || 0) * (1 - elapsedInWindow / windowSeconds);
  
  if (weightedCount >= limit) {
    return false;
  }
  
  await redis.incr(currentKey);
  await redis.expire(currentKey, windowSeconds * 2);
  return true;
}
```

**4. Token Bucket (Bursty but Controlled)**
```javascript
// Tokens refill at constant rate, requests consume tokens
// Great for APIs that allow occasional bursts
async function tokenBucketRateLimit(userId, capacity = 100, refillRate = 10) {
  // refillRate: tokens per second
  const key = `tokenbucket:${userId}`;
  const now = Date.now() / 1000;
  
  const stored = await redis.hgetall(key);
  const lastRefill = parseFloat(stored.lastRefill) || now;
  const tokens = parseFloat(stored.tokens) || capacity;
  
  // Calculate tokens earned since last refill
  const elapsed = now - lastRefill;
  const newTokens = Math.min(capacity, tokens + elapsed * refillRate);
  
  if (newTokens < 1) {
    return false; // Not enough tokens
  }
  
  // Consume 1 token
  await redis.hset(key, { tokens: newTokens - 1, lastRefill: now });
  await redis.expire(key, Math.ceil(capacity / refillRate) + 1);
  return true;
}
// Benefit: User can burst 100 requests at once if they've been quiet
// Good for: APIs where occasional bursts are acceptable (like GitHub API)
```

**5. Leaky Bucket (Smooth Output)**
```javascript
// Requests queue up, processed at constant rate
// Prevents bursty traffic from hitting your servers
// Often implemented with a message queue (SQS/Bull)

const queue = require('bull');
const requestQueue = new queue('api-requests', redisConfig);

app.post('/heavy-endpoint', async (req, res) => {
  // Instead of processing immediately, queue the request
  const job = await requestQueue.add({ data: req.body, userId: req.user.id });
  res.status(202).json({ jobId: job.id, message: 'Request queued' });
});

// Worker processes at controlled rate (10 req/sec)
requestQueue.process(10, async (job) => {
  // Process job.data here
});
```

---

### Implementing Rate Limiting in Node.js

```javascript
const rateLimit = require('express-rate-limit');
const RedisStore = require('rate-limit-redis');
const { createClient } = require('redis');

const redisClient = createClient({ url: process.env.REDIS_URL });

// Different limits for different endpoints
const generalLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100,
  store: new RedisStore({ sendCommand: (...args) => redisClient.sendCommand(args) }),
  keyGenerator: (req) => req.user?.id || req.ip, // Rate limit per user, not per IP
  handler: (req, res) => {
    res.status(429).json({
      success: false,
      error: {
        code: 'RATE_LIMIT_EXCEEDED',
        message: 'Too many requests, please try again later',
        retryAfter: Math.ceil(req.rateLimit.resetTime / 1000)
      }
    });
  },
  standardHeaders: true,  // Add X-RateLimit-* headers
  legacyHeaders: false
});

const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5, // Only 5 login attempts per 15 minutes (brute force protection)
  store: new RedisStore({ sendCommand: (...args) => redisClient.sendCommand(args) }),
  skipSuccessfulRequests: true, // Don't count successful logins
});

// Apply different limits to different routes
app.use('/api/', generalLimiter);
app.use('/auth/login', authLimiter);

// Stricter limit for expensive operations
const uploadLimiter = rateLimit({ windowMs: 60 * 60 * 1000, max: 10 }); // 10 uploads/hour
app.use('/upload', uploadLimiter);
```

---

## ⚖️ Trade-offs

| Algorithm | Memory | Accuracy | Burst Handling | Complexity |
|-----------|--------|----------|----------------|------------|
| Fixed Window | Low | Medium | Allows boundary burst | Simple |
| Sliding Window Log | High | Exact | None | Medium |
| Sliding Window Counter | Low | Near-exact | None | Medium |
| Token Bucket | Low | Good | Yes (by design) | Medium |
| Leaky Bucket | Medium | Good | Smooths bursts | Higher |

---

## 📊 Scalability Discussion

### Multi-Tier Rate Limiting

```
Tier 1: AWS WAF (IP-level)
  → Block known malicious IPs
  → Block countries if needed
  → Limit: 10,000 req/min per IP (catches extreme DDoS)

Tier 2: AWS API Gateway
  → API key rate limits
  → Per-stage throttling
  → Limit: 1000 req/min per API key

Tier 3: Node.js + Redis (user-level)
  → Per-user, per-endpoint limits
  → Different limits for free vs paid users
  → Limit: 100 req/min for free, 1000 req/min for paid

Tier 4: Business logic
  → "You can only post 10 photos per day"
  → "You can only send 100 messages per hour"
```

### Response Headers

```javascript
// Always include rate limit info in headers
app.use('/api', (req, res, next) => {
  // These are automatically added by express-rate-limit with standardHeaders: true
  // X-RateLimit-Limit: 100
  // X-RateLimit-Remaining: 95
  // X-RateLimit-Reset: 1703000000
  // Retry-After: 30 (only on 429 responses)
  next();
});
```

---

## 💼 Interview Questions (WITH SOLUTIONS)

### Q1: What is rate limiting and why is it important?

**Solution:**
Rate limiting controls how many requests a user or IP can make to an API within a time window. It's important for:
1. **Protection from DDoS:** Limits damage from traffic floods
2. **Preventing abuse:** Stop bots from scraping your data at unlimited speed
3. **Fair resource distribution:** Ensure one heavy user doesn't starve others
4. **Cost control:** Limit Lambda invocations, database queries, and third-party API calls
5. **Security:** Prevent brute-force password attacks (5 attempts/15 min)
6. **Business rules:** Enforce tiered plans (free: 100 req/day, paid: 10,000 req/day)

---

### Q2: Why is in-memory rate limiting broken in a distributed system?

**Solution:**
In-memory rate limiting stores counters in each server's memory. With multiple servers:
- Server 1 sees 90 requests from User A
- Server 2 sees 90 requests from User A (different memory!)
- Total: 180 requests, but each server thinks only 90

The limit is effectively multiplied by the number of servers. A 100 req/min limit with 10 servers = effectively 1000 req/min.

**Fix:** Use Redis as a shared, centralized counter. All servers read/write to the same Redis counter for each user. Redis's atomic `INCR` ensures no race conditions.

---

### Q3: Explain the Token Bucket algorithm with a real example.

**Solution:**
Imagine a bucket that:
- Holds maximum 10 tokens
- Refills at 1 token/second
- Each request consumes 1 token

```
Scenario: User makes rapid requests
T=0: Bucket has 10 tokens (full)
T=0: User sends 10 requests → 10 tokens consumed → 0 left
T=0: User sends 11th request → REJECTED (0 tokens)
T=5: 5 seconds pass → 5 tokens refilled
T=5: User sends 5 requests → 5 tokens consumed → 0 left
T=5: 6th request → REJECTED

Use case: GitHub API allows 5000 requests/hour
→ Capacity: 5000 tokens
→ Refill rate: 5000/3600 ≈ 1.38 tokens/second
→ You can burst 5000 requests immediately, but then wait for refill
→ Alternatively, use 1.38 req/sec continuously all day
```

---

### Q4: How do you implement different rate limits for different user tiers?

**Solution:**
```javascript
// Middleware to get user's rate limit based on plan
const getRateLimit = (req, res, next) => {
  const plan = req.user?.plan || 'free';
  
  const limits = {
    free: { windowMs: 60 * 1000, max: 60 },      // 60 req/min
    pro: { windowMs: 60 * 1000, max: 600 },       // 600 req/min
    enterprise: { windowMs: 60 * 1000, max: 6000 } // 6000 req/min
  };
  
  const { windowMs, max } = limits[plan] || limits.free;
  
  // Dynamic rate limiter
  const limiter = rateLimit({
    windowMs,
    max,
    keyGenerator: (req) => `${plan}:${req.user.id}`,
    store: new RedisStore({ sendCommand: (...args) => redisClient.sendCommand(args) })
  });
  
  limiter(req, res, next);
};

app.use('/api', authenticateUser, getRateLimit);

// Also: Add rate limit info to user profile endpoint so they can see their usage
app.get('/api/me/usage', async (req, res) => {
  const key = `ratelimit:${req.user.plan}:${req.user.id}:*`;
  // Return current usage from Redis
});
```

---

### Q5: How does AWS API Gateway handle rate limiting?

**Solution:**
AWS API Gateway provides two levels of throttling:
1. **Account-level:** Default 10,000 RPS with burst of 5,000 across all APIs
2. **Stage-level:** Set limits per API stage (e.g., production vs staging)
3. **Method-level:** Different limits for different endpoints (POST /payments vs GET /products)

```
AWS Console/Terraform:
Usage Plan:
  - Throttle:
    - Rate: 1000 requests per second
    - Burst: 2000 requests (can briefly exceed rate limit)
  - Quota:
    - 100,000 requests per month per API key

API Keys:
  - Associate API keys with usage plans
  - Free tier: Plan A (100/min)
  - Paid tier: Plan B (1000/min)
```

Clients include API key in header: `x-api-key: your_api_key_here`

When exceeded: API Gateway returns 429 without hitting your Node.js server at all!

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem 1: Design rate limiting for a login endpoint to prevent brute force attacks

**Solution:**
```javascript
// Multi-layered protection:

// 1. Per-IP rate limit (block obvious bots)
const ipLoginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 20,                   // 20 attempts per IP
  keyGenerator: (req) => req.ip,
  skipSuccessfulRequests: true
});

// 2. Per-email rate limit (more targeted)
const emailLoginLimiter = async (req, res, next) => {
  const email = req.body.email?.toLowerCase();
  if (!email) return next();
  
  const key = `login:attempts:email:${email}`;
  const attempts = await redis.incr(key);
  
  if (attempts === 1) await redis.expire(key, 15 * 60); // 15 min window
  
  if (attempts > 10) {
    // After 10 failed attempts for this email → account lockout
    await redis.setex(`account:locked:${email}`, 30 * 60, '1'); // Lock 30 min
    return res.status(429).json({ error: 'Account temporarily locked. Try in 30 minutes.' });
  }
  
  next();
};

// 3. Progressive delays (honeypot)
const progressiveDelay = async (req, res, next) => {
  const attempts = await redis.get(`login:attempts:${req.body.email}`);
  if (attempts > 5) {
    const delay = Math.min(2000 * (attempts - 5), 30000); // Max 30s delay
    await new Promise(resolve => setTimeout(resolve, delay));
  }
  next();
};

app.post('/auth/login', ipLoginLimiter, emailLoginLimiter, progressiveDelay, loginController);

// 4. Reset attempts on successful login
async function onSuccessfulLogin(email) {
  await redis.del(`login:attempts:email:${email}`);
  await redis.del(`login:attempts:${req.ip}`);
}

// 5. CAPTCHA after 3 failed attempts (implement on frontend)
// 6. Alert user via email when account has >5 failed attempts
// 7. Optional: 2FA as additional layer
```

---

### Problem 2: Design a rate limiter for a public API with 3 tiers (free, pro, enterprise)

**Solution:**
```javascript
// Complete rate limiting service

class RateLimiter {
  constructor(redis) {
    this.redis = redis;
    this.tiers = {
      free: {
        requestsPerMinute: 60,
        requestsPerDay: 1000,
        requestsPerMonth: 10000
      },
      pro: {
        requestsPerMinute: 600,
        requestsPerDay: 50000,
        requestsPerMonth: 1000000
      },
      enterprise: {
        requestsPerMinute: 6000,
        requestsPerDay: 500000,
        requestsPerMonth: null // Unlimited
      }
    };
  }

  async checkLimit(apiKey, tier) {
    const limits = this.tiers[tier];
    const now = Date.now();
    
    const checks = await Promise.all([
      this.checkWindow(apiKey, 'minute', 60, limits.requestsPerMinute),
      this.checkWindow(apiKey, 'day', 86400, limits.requestsPerDay),
      limits.requestsPerMonth ? 
        this.checkWindow(apiKey, 'month', 2592000, limits.requestsPerMonth) : 
        { allowed: true }
    ]);
    
    const failed = checks.find(c => !c.allowed);
    if (failed) {
      return { allowed: false, window: failed.window, retryAfter: failed.retryAfter };
    }
    
    return { allowed: true };
  }

  async checkWindow(apiKey, window, windowSeconds, limit) {
    const windowKey = Math.floor(Date.now() / 1000 / windowSeconds);
    const key = `ratelimit:${apiKey}:${window}:${windowKey}`;
    
    const count = await this.redis.incr(key);
    if (count === 1) await this.redis.expire(key, windowSeconds);
    
    if (count > limit) {
      const ttl = await this.redis.ttl(key);
      return { allowed: false, window, retryAfter: ttl };
    }
    
    return { allowed: true, remaining: limit - count };
  }
}

// Middleware
const rateLimiter = new RateLimiter(redisClient);

app.use(async (req, res, next) => {
  const apiKey = req.headers['x-api-key'];
  if (!apiKey) return res.status(401).json({ error: 'API key required' });
  
  const { tier } = await apiKeyService.validate(apiKey);
  const result = await rateLimiter.checkLimit(apiKey, tier);
  
  if (!result.allowed) {
    res.setHeader('Retry-After', result.retryAfter);
    return res.status(429).json({ 
      error: `Rate limit exceeded for ${result.window} window`,
      retryAfter: result.retryAfter
    });
  }
  
  next();
});
```

---

### Navigation
**Prev:** [12_API_Design.md](12_API_Design.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [14_Message_Queues.md](14_Message_Queues.md)
