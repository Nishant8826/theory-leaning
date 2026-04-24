# 🏗️ Case Study: URL Shortener (like bit.ly)

## 📋 Requirements

**Functional:**
- User pastes long URL → system returns short URL (e.g., `sho.rt/abc123`)
- User visits short URL → redirected to original URL
- Optional: Custom alias (`sho.rt/my-brand`)
- Optional: Analytics (click count, referrer, location)
- Optional: Expiry time for links

**Non-Functional:**
- 100M short URLs created per day
- 10 billion redirects per day (read:write ratio = 100:1)
- Redirect in < 10ms
- 99.99% availability
- Short URL must be unique

---

## 📊 Capacity Estimation

```
Writes: 100M URLs/day = ~1,157 writes/sec
Reads:  10B redirects/day = ~115,700 reads/sec (100:1 read:write)

Storage:
  Each URL record: ~500 bytes
  100M × 500 = 50GB new data per day
  1 year: 50GB × 365 = ~18TB

ID length:
  Base62 characters: [a-z A-Z 0-9] = 62 characters
  6 characters: 62^6 = 56.8 billion unique IDs
  → More than enough for many years!
```

---

## 🏗️ High Level Design

```
[Browser/App]
      ↓ POST /shorten
[AWS API Gateway]
      ↓
[Node.js URL Service] → [PostgreSQL + Redis]
                     → [S3 — Analytics events]

[Browser visits sho.rt/abc123]
      ↓
[AWS CloudFront + Lambda@Edge] ← Cache redirects at edge!
  OR
[AWS API Gateway + Node.js] → [Redis] → [PostgreSQL fallback]
      ↓
[302 Redirect to original URL]
```

---

## 🔑 Short URL ID Generation

### Approach 1: Random Base62 (Simple)

```javascript
const crypto = require('crypto');

function generateShortId(length = 7) {
  const BASE62 = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
  
  // Generate cryptographically secure random bytes
  const bytes = crypto.randomBytes(length);
  let id = '';
  
  for (let i = 0; i < length; i++) {
    id += BASE62[bytes[i] % 62];
  }
  
  return id;
}

// Check for collisions (rare but must handle)
async function generateUniqueShortId() {
  for (let attempt = 0; attempt < 5; attempt++) {
    const id = generateShortId(7); // 7 chars = 62^7 = 3.5 trillion possibilities
    
    const existing = await db.query('SELECT id FROM urls WHERE short_id = $1', [id]);
    if (existing.rows.length === 0) return id;
  }
  throw new Error('Failed to generate unique ID');
}
```

### Approach 2: Counter-Based with Base62 Encoding (Better at scale)

```javascript
// Use PostgreSQL sequence or Redis counter for globally unique IDs
// Then encode to base62

function toBase62(num) {
  const BASE62 = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
  if (num === 0) return BASE62[0];
  
  let result = '';
  while (num > 0) {
    result = BASE62[num % 62] + result;
    num = Math.floor(num / 62);
  }
  return result;
}

function fromBase62(str) {
  const BASE62 = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
  let result = 0;
  for (const char of str) {
    result = result * 62 + BASE62.indexOf(char);
  }
  return result;
}

// PostgreSQL sequence — globally unique, no collisions!
async function generateSequentialId() {
  const result = await db.query("SELECT nextval('url_id_seq') as id");
  return toBase62(parseInt(result.rows[0].id));
}

// With padding: ensure minimum length
const id = toBase62(12345).padStart(6, 'a'); // "aaaaDnh"
```

---

## 🗃️ Database Schema

```sql
-- Main URL table (PostgreSQL)
CREATE TABLE urls (
  id BIGSERIAL PRIMARY KEY,
  short_id VARCHAR(10) UNIQUE NOT NULL,  -- 'abc1234'
  original_url TEXT NOT NULL,
  custom_alias VARCHAR(50) UNIQUE,        -- Optional custom slug
  user_id UUID REFERENCES users(id),     -- NULL = anonymous
  title VARCHAR(200),                    -- Page title (fetched async)
  click_count BIGINT DEFAULT 0,          -- Denormalized for speed
  is_active BOOLEAN DEFAULT true,
  expires_at TIMESTAMP WITH TIME ZONE,   -- NULL = never expires
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_urls_short_id ON urls(short_id);
CREATE INDEX idx_urls_user_id ON urls(user_id) WHERE user_id IS NOT NULL;
CREATE INDEX idx_urls_expires ON urls(expires_at) WHERE expires_at IS NOT NULL;

-- Analytics table (high-write, consider time-partitioning)
CREATE TABLE url_clicks (
  id BIGSERIAL,
  short_id VARCHAR(10) NOT NULL,
  clicked_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  referrer VARCHAR(500),
  user_agent VARCHAR(500),
  ip_address INET,
  country VARCHAR(2),
  city VARCHAR(100)
) PARTITION BY RANGE (clicked_at);

-- Partitions for each month
CREATE TABLE url_clicks_2024_01 PARTITION OF url_clicks
  FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
```

---

## 💻 Node.js Implementation

```javascript
const express = require('express');
const { Pool } = require('pg');
const Redis = require('ioredis');
const crypto = require('crypto');

const app = express();
const db = new Pool({ connectionString: process.env.DATABASE_URL });
const redis = new Redis(process.env.REDIS_URL);

const BASE62 = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';

// --- URL Shortening ---

app.post('/api/shorten', async (req, res) => {
  const { originalUrl, customAlias, expiresIn } = req.body;
  
  // Validate URL
  try { new URL(originalUrl); } 
  catch { return res.status(400).json({ error: 'Invalid URL' }); }
  
  // Check if custom alias is taken
  if (customAlias) {
    const existing = await db.query('SELECT id FROM urls WHERE short_id = $1', [customAlias]);
    if (existing.rows.length > 0) return res.status(409).json({ error: 'Custom alias already taken' });
  }
  
  // Check if this exact URL was already shortened (deduplication)
  const urlHash = crypto.createHash('sha256').update(originalUrl).digest('hex');
  const duplicate = await db.query('SELECT short_id FROM urls WHERE url_hash = $1', [urlHash]);
  if (duplicate.rows.length > 0) {
    return res.json({ shortUrl: `${process.env.BASE_URL}/${duplicate.rows[0].short_id}` });
  }
  
  // Generate unique ID
  const shortId = customAlias || await generateUniqueShortId();
  
  const expiresAt = expiresIn 
    ? new Date(Date.now() + expiresIn * 1000) 
    : null;
  
  await db.query(
    'INSERT INTO urls (short_id, original_url, url_hash, user_id, expires_at) VALUES ($1, $2, $3, $4, $5)',
    [shortId, originalUrl, urlHash, req.user?.id, expiresAt]
  );
  
  // Pre-cache in Redis
  const cacheData = JSON.stringify({ url: originalUrl, expiresAt });
  if (expiresAt) {
    const ttl = Math.floor((expiresAt - Date.now()) / 1000);
    await redis.setex(`url:${shortId}`, ttl, cacheData);
  } else {
    await redis.setex(`url:${shortId}`, 86400, cacheData); // Cache 24 hours
  }
  
  res.status(201).json({
    shortUrl: `${process.env.BASE_URL}/${shortId}`,
    shortId,
    expiresAt
  });
});

// --- URL Redirect (CRITICAL PATH — must be fast!) ---

app.get('/:shortId', async (req, res) => {
  const { shortId } = req.params;
  
  // 1. Check Redis (< 1ms)
  const cached = await redis.get(`url:${shortId}`);
  
  if (cached) {
    const { url, expiresAt } = JSON.parse(cached);
    
    // Check expiry
    if (expiresAt && new Date(expiresAt) < new Date()) {
      return res.status(410).json({ error: 'This link has expired' });
    }
    
    // Track click asynchronously (don't slow down redirect!)
    trackClickAsync(shortId, req).catch(err => console.error('Analytics error:', err));
    
    return res.redirect(302, url);
  }
  
  // 2. Cache miss — check DB
  const result = await db.query(
    'SELECT original_url, expires_at, is_active FROM urls WHERE short_id = $1',
    [shortId]
  );
  
  if (!result.rows[0]) return res.status(404).send('Short URL not found');
  
  const { original_url, expires_at, is_active } = result.rows[0];
  
  if (!is_active) return res.status(410).send('This link has been deactivated');
  if (expires_at && new Date(expires_at) < new Date()) {
    return res.status(410).send('This link has expired');
  }
  
  // 3. Re-cache
  const ttl = expires_at 
    ? Math.floor((new Date(expires_at) - Date.now()) / 1000)
    : 86400;
  
  await redis.setex(`url:${shortId}`, Math.max(ttl, 1), JSON.stringify({ url: original_url, expiresAt: expires_at }));
  
  // Track click
  trackClickAsync(shortId, req).catch(() => {});
  
  return res.redirect(302, original_url);
});

// --- Async Analytics (fire and forget) ---
async function trackClickAsync(shortId, req) {
  const clickData = {
    shortId,
    referrer: req.headers.referer || null,
    userAgent: req.headers['user-agent'],
    ip: req.ip,
    clickedAt: new Date().toISOString()
  };
  
  // Batch analytics: Write to Redis queue, worker flushes to DB every minute
  await redis.lpush('analytics:clicks', JSON.stringify(clickData));
  
  // Atomic increment of click counter
  await redis.incr(`clicks:${shortId}`);
  
  // Periodically flush counter to DB (via scheduled job)
  // This avoids 115,700 DB writes/sec!
}

// --- Analytics worker (runs every 60 seconds) ---
setInterval(async () => {
  // Flush click events from Redis queue to DB
  const batchSize = 1000;
  const clicks = await redis.lrange('analytics:clicks', 0, batchSize - 1);
  
  if (clicks.length > 0) {
    await redis.ltrim('analytics:clicks', clicks.length, -1);
    
    const values = clicks.map(c => JSON.parse(c));
    await db.query(
      'INSERT INTO url_clicks (short_id, referrer, user_agent, ip_address, clicked_at) VALUES ' +
      values.map((_, i) => `($${i*5+1}, $${i*5+2}, $${i*5+3}, $${i*5+4}, $${i*5+5})`).join(','),
      values.flatMap(v => [v.shortId, v.referrer, v.userAgent, v.ip, v.clickedAt])
    );
  }
  
  // Flush click counts to DB
  const keys = await redis.keys('clicks:*');
  for (const key of keys) {
    const shortId = key.split(':')[1];
    const count = parseInt(await redis.getdel(key));
    if (count > 0) {
      await db.query('UPDATE urls SET click_count = click_count + $1 WHERE short_id = $2', [count, shortId]);
    }
  }
}, 60000);
```

---

## 🔒 Security Considerations

```javascript
// 1. Validate URLs — prevent redirect to malicious sites
const { URL } = require('url');

function isValidUrl(url) {
  try {
    const parsed = new URL(url);
    // Only allow http and https
    if (!['http:', 'https:'].includes(parsed.protocol)) return false;
    // Block private/local addresses (SSRF prevention)
    const hostname = parsed.hostname;
    if (hostname === 'localhost' || hostname.startsWith('127.') || hostname.startsWith('192.168.') || hostname.startsWith('10.')) {
      return false;
    }
    return true;
  } catch {
    return false;
  }
}

// 2. Safe redirect headers
res.setHeader('Referrer-Policy', 'no-referrer');
res.setHeader('X-Content-Type-Options', 'nosniff');

// 3. Check against Google Safe Browsing API for malicious URLs
// 4. Rate limit URL creation (prevent spam)
// 5. Custom alias validation (no offensive words)
```

---

## 📊 Analytics API

```javascript
app.get('/api/urls/:shortId/analytics', authenticate, async (req, res) => {
  const { shortId } = req.params;
  const { period = '30d' } = req.query;
  
  // Verify user owns this URL
  const url = await db.query('SELECT * FROM urls WHERE short_id = $1 AND user_id = $2', 
    [shortId, req.user.id]);
  if (!url.rows[0]) return res.status(404).json({ error: 'URL not found' });
  
  const days = parseInt(period.replace('d', ''));
  const since = new Date(Date.now() - days * 24 * 60 * 60 * 1000);
  
  const [totalClicks, clicksByDay, topReferrers, topCountries] = await Promise.all([
    db.query('SELECT COUNT(*) FROM url_clicks WHERE short_id = $1 AND clicked_at > $2', [shortId, since]),
    db.query('SELECT DATE(clicked_at) as date, COUNT(*) as clicks FROM url_clicks WHERE short_id = $1 AND clicked_at > $2 GROUP BY DATE(clicked_at) ORDER BY date', [shortId, since]),
    db.query('SELECT referrer, COUNT(*) as count FROM url_clicks WHERE short_id = $1 AND clicked_at > $2 GROUP BY referrer ORDER BY count DESC LIMIT 10', [shortId, since]),
    db.query('SELECT country, COUNT(*) as count FROM url_clicks WHERE short_id = $1 AND clicked_at > $2 GROUP BY country ORDER BY count DESC LIMIT 10', [shortId, since])
  ]);
  
  res.json({
    url: url.rows[0],
    analytics: {
      totalClicks: parseInt(totalClicks.rows[0].count),
      clicksByDay: clicksByDay.rows,
      topReferrers: topReferrers.rows,
      topCountries: topCountries.rows
    }
  });
});
```

---

## 🎯 Interview Discussion Points

### Key Design Decisions

1. **ID Generation Strategy:**
   - Random base62: Simple, no coordination needed, small collision risk
   - Sequential counter: No collisions, reveals creation order (privacy concern)
   - **Choice:** Random 7-char base62 — 3.5 trillion combinations, simple, no central coordinator

2. **Read Path Optimization (Most Important):**
   - Redis cache for all short URLs (99%+ cache hit rate)
   - CloudFront at edge for global low latency
   - 302 vs 301 redirect: 301 = permanent (browser caches, no analytics), 302 = temporary (always hits your server, enables analytics)

3. **Analytics at Scale:**
   - DON'T write to DB on every redirect (115,700 writes/sec would kill DB)
   - Redis counter + periodic flush to DB (every 60 seconds)
   - SQS queue for click events, Lambda consumer writes to analytics DB

4. **Database:**
   - PostgreSQL for URL data (ACID, unique constraints)
   - Redis for redirect cache (fast, scalable)
   - Time-series DB or partitioned table for analytics

### Scalability Path

```
Phase 1 (MVP): 
  Single Node.js + PostgreSQL + Redis → handles 100K users

Phase 2 (Growth):
  Load-balanced Node.js (ECS) + RDS PostgreSQL + ElastiCache Redis
  → 1M users

Phase 3 (Scale):
  Edge redirects with Lambda@Edge + CloudFront
  Database read replicas for analytics queries
  → 100M redirects/day

Phase 4 (Massive Scale):
  Cassandra/DynamoDB for URL storage (massive write throughput)
  Kafka for analytics events
  → 10B redirects/day
```

---

### Navigation
**Index:** [00_Index.md](00_Index.md) | **Next Case Study:** [02_Design_Instagram.md](02_Design_Instagram.md)
