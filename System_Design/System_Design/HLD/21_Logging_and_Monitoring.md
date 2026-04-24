# 📌 Logging and Monitoring

## 🧠 Concept Explanation (Story Format)

It's 3 AM. Your app is down. Users are angry. Your boss is calling. You have NO idea what happened.

Without logging and monitoring: You're flying blind. You check code randomly. It takes hours to find the issue.

With logging and monitoring:
- Your phone buzzed at 2:58 AM (before users noticed) — "API latency P99 > 2000ms"
- You open your dashboard — see error rate spike at 2:55 AM
- You check distributed traces — see "Payment Service timeout"
- You check logs — "Database connection pool exhausted"
- You scale up the connection pool. 3:05 AM — problem solved. Users barely noticed.

This is why Netflix, Amazon, and every serious company invests heavily in observability.

---

## 🏗️ Basic Design (Naive)

```javascript
// ❌ Basic console.log — terrible for production
app.get('/api/users/:id', async (req, res) => {
  try {
    const user = await db.getUser(req.params.id);
    console.log('Got user:', user.id);  // Not searchable, no timestamps, no context
    res.json(user);
  } catch (error) {
    console.error('Error:', error.message);  // Where did this error come from? When? Which request?
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Problems:
// - No centralized log storage (logs lost when server restarts)
// - Can't search logs across multiple servers
// - No alerting
// - No performance metrics
// - No request tracing
```

---

## ⚡ Optimized Design (Observability Pillars)

```
The Three Pillars of Observability:

1. LOGS → What happened? (events, errors, debug info)
2. METRICS → How much/many/fast? (numbers over time)
3. TRACES → Where did time go? (request flow across services)

Architecture:
Node.js Apps
    ↓ (structured JSON logs)
CloudWatch Logs (AWS managed)
    ↓
CloudWatch Insights (search, analyze logs)
    ↓
CloudWatch Alarms → SNS → Slack/PagerDuty (alerts!)

Node.js Apps → CloudWatch Metrics (custom metrics)
    ↓
CloudWatch Dashboard (graphs, numbers)
    ↓
CloudWatch Alarms (if P99 > 2s → alert!)
```

---

## 🔍 Key Components

### Structured Logging with Winston

```javascript
const winston = require('winston');

// Create structured logger
const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()  // Output as JSON — searchable in CloudWatch!
  ),
  transports: [
    new winston.transports.Console(),
    // In production: also ship to CloudWatch or log aggregation service
  ]
});

// Middleware: Log every request
app.use((req, res, next) => {
  const requestId = req.headers['x-request-id'] || require('uuid').v4();
  req.requestId = requestId;
  
  const startTime = Date.now();
  
  res.on('finish', () => {
    logger.info('http_request', {
      requestId,
      method: req.method,
      path: req.path,
      statusCode: res.statusCode,
      duration: Date.now() - startTime,
      userId: req.user?.id,
      ip: req.ip,
      userAgent: req.headers['user-agent']
    });
  });
  
  next();
});

// Usage in services
class PostService {
  async createPost(userId, content) {
    logger.info('creating_post', { userId, contentLength: content.length });
    
    try {
      const post = await db.insertPost({ userId, content });
      logger.info('post_created', { postId: post.id, userId });
      return post;
    } catch (error) {
      logger.error('post_creation_failed', {
        userId,
        error: error.message,
        stack: error.stack,
        requestId: currentRequestId  // Tie log to request
      });
      throw error;
    }
  }
}

// Log Levels (use appropriately!):
// debug: Detailed debugging info (disable in production!)
// info: Normal operations ("User logged in", "Order created")
// warn: Unusual but not wrong ("Deprecated API endpoint used")
// error: Actual errors ("Database query failed", "Payment declined")
// fatal: System is broken ("Cannot connect to database on startup")
```

### Custom Metrics with CloudWatch

```javascript
const AWS = require('aws-sdk');
const cloudwatch = new AWS.CloudWatch({ region: 'us-east-1' });

// Helper to publish custom metrics
async function publishMetric(metricName, value, unit, dimensions = []) {
  await cloudwatch.putMetricData({
    Namespace: 'MyApp/API',
    MetricData: [{
      MetricName: metricName,
      Value: value,
      Unit: unit,
      Dimensions: dimensions,
      Timestamp: new Date()
    }]
  }).promise();
}

// Track API response times
app.use(async (req, res, next) => {
  const start = Date.now();
  res.on('finish', async () => {
    const duration = Date.now() - start;
    
    // Publish to CloudWatch (async, don't await to not slow down response)
    publishMetric('ApiLatency', duration, 'Milliseconds', [
      { Name: 'Endpoint', Value: req.path },
      { Name: 'Method', Value: req.method }
    ]).catch(err => logger.warn('Failed to publish metric', { err }));
    
    publishMetric('ApiRequests', 1, 'Count', [
      { Name: 'StatusCode', Value: res.statusCode.toString() }
    ]).catch(() => {});
  });
  next();
});

// Business metrics
async function onOrderPlaced(order) {
  await publishMetric('OrdersPlaced', 1, 'Count');
  await publishMetric('OrderRevenue', order.total, 'None');  // Track revenue
}

// Cache hit rate
async function getCached(key) {
  const value = await redis.get(key);
  await publishMetric('CacheHit', value ? 1 : 0, 'None');
  return value;
}
```

### Distributed Tracing with AWS X-Ray

```javascript
const AWSXRay = require('aws-xray-sdk');
const http = AWSXRay.captureHTTPs(require('http'));
const https = AWSXRay.captureHTTPs(require('https'));

// Capture PostgreSQL queries
const { Pool } = require('pg');
const pool = AWSXRay.capturePostgres(new Pool({ connectionString: process.env.DB_URL }));

// Capture Redis
const redis = AWSXRay.captureRedis(new Redis(process.env.REDIS_URL));

// Auto-instrument Express
app.use(AWSXRay.express.openSegment('user-service'));
app.use(router);
app.use(AWSXRay.express.closeSegment());

// Custom subsegments for your own code
app.get('/api/feed', async (req, res) => {
  const segment = AWSXRay.getSegment();
  
  // Trace Redis call
  const cacheSubsegment = segment.addNewSubsegment('redis_cache_check');
  const cached = await redis.get(`feed:${req.user.id}`);
  cacheSubsegment.close();
  
  if (cached) return res.json(JSON.parse(cached));
  
  // Trace DB call
  const dbSubsegment = segment.addNewSubsegment('db_query');
  const feed = await pool.query('SELECT * FROM posts WHERE ...', [...]);
  dbSubsegment.close();
  
  res.json(feed.rows);
});

// X-Ray shows you: For request X:
// - Total time: 245ms
// - Redis check: 2ms (MISS)
// - DB query: 200ms (slowest part!)
// - Response formatting: 43ms
// → Optimize the DB query!
```

### CloudWatch Alarms and Alerting

```javascript
// Set up alarms (typically done via Terraform/CloudFormation, but here's the concept):

/*
Alarm: HighApiErrorRate
  Metric: 5xx responses count
  Threshold: > 10 per minute for 3 consecutive periods
  Action: Notify "on-call" SNS topic → Slack + PagerDuty

Alarm: HighApiLatency
  Metric: ApiLatency P99
  Threshold: > 2000ms for 5 minutes
  Action: Notify on-call

Alarm: LowCacheHitRate
  Metric: CacheHit ratio
  Threshold: < 80% for 10 minutes
  Action: Notify team (non-urgent)

Alarm: DatabaseConnectionsHigh
  Metric: DatabaseConnections count
  Threshold: > 90% of max
  Action: Notify immediately (urgent!)
*/

// Slack notification via Lambda (triggered by SNS)
// lambda/notify-slack.js
exports.handler = async (event) => {
  const message = JSON.parse(event.Records[0].Sns.Message);
  
  await fetch(process.env.SLACK_WEBHOOK_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      text: `🚨 *ALERT: ${message.AlarmName}*\n${message.NewStateReason}\nRegion: ${message.Region}`
    })
  });
};
```

### Health Dashboard (Node.js Status Page)

```javascript
app.get('/status', async (req, res) => {
  const startTime = Date.now();
  const checks = {};
  
  // Database health
  try {
    await pool.query('SELECT 1');
    checks.database = { status: 'ok', latency: Date.now() - startTime };
  } catch (e) {
    checks.database = { status: 'error', message: e.message };
  }
  
  // Redis health
  try {
    const t = Date.now();
    await redis.ping();
    checks.redis = { status: 'ok', latency: Date.now() - t };
  } catch (e) {
    checks.redis = { status: 'error', message: e.message };
  }
  
  // Elasticsearch health
  try {
    const health = await elasticsearch.cluster.health();
    checks.elasticsearch = { status: health.status === 'green' ? 'ok' : 'degraded' };
  } catch (e) {
    checks.elasticsearch = { status: 'error' };
  }
  
  const overall = Object.values(checks).every(c => c.status === 'ok') ? 'ok' : 'degraded';
  
  res.status(overall === 'ok' ? 200 : 503).json({
    status: overall,
    uptime: process.uptime(),
    timestamp: new Date().toISOString(),
    checks
  });
});
```

---

## ⚖️ Trade-offs

| More Logging | Less Logging |
|-------------|-------------|
| Better debugging | Lower cost |
| Faster incident response | Lower storage |
| Better audit trail | Less noise |
| Higher storage cost | Harder debugging |
| Performance overhead | Miss incidents |

**Log storage cost tip:** Log at INFO level in production. Use DEBUG only during development. Ship logs to S3 Glacier after 30 days.

---

## 📊 Scalability Discussion

### Log Volume at Scale

```
100 servers × 1000 req/sec × 500 bytes/log = 50 MB/second of logs!
= 4.3 TB per day → Storage becomes expensive fast

Solutions:
1. Sampling: Only log 10% of successful requests (log 100% of errors)
2. Log levels: INFO in production, DEBUG only when debugging
3. Log retention: Keep 30 days in CloudWatch, archive to S3, delete after 1 year
4. Compression: CloudWatch compresses automatically
5. Structured logs: JSON logs are easier to query but slightly larger
```

---

## 💼 Interview Questions (WITH SOLUTIONS)

### Q1: What are the three pillars of observability?

**Solution:**
1. **Logs:** Timestamped, contextual records of events. What happened? Text-based. Used for debugging specific incidents.
   - Example: "ERROR: Payment declined for userId=123, orderId=456, reason=insufficient_funds"
   
2. **Metrics:** Numerical measurements over time. How many? How fast? How much?
   - Example: "API p99 latency = 450ms", "Error rate = 0.5%", "Cache hit rate = 92%"
   - Used for trending, alerting, capacity planning
   
3. **Traces:** End-to-end record of a request through multiple services. Where did time go?
   - Example: Request took 500ms → Redis 2ms → DB query 450ms → formatting 48ms
   - Used for performance optimization and identifying bottlenecks

All three together = complete observability. Logs tell you what, metrics tell you how much, traces tell you where.

---

### Q2: How do you structure logs to make them useful?

**Solution:**
**Always use structured JSON logs with these fields:**

```javascript
{
  "timestamp": "2024-01-15T10:30:45.123Z",
  "level": "error",
  "event": "payment_failed",        // Machine-readable event name
  "message": "Payment processing failed", // Human-readable
  "requestId": "req_abc123",         // Tie to HTTP request
  "userId": "user_456",              // Who
  "orderId": "order_789",            // What
  "error": "Stripe timeout",         // Why it failed
  "stack": "Error: ...\n at ...",    // Stack trace for errors
  "duration": 3500,                  // How long it took
  "service": "payment-service",      // Which microservice
  "version": "1.2.3"                 // Which deployment
}
```

**Why JSON?**
- CloudWatch Insights can query JSON fields: `filter level = "error" | stats count by event`
- Grep by specific fields: find all errors for a specific userId
- Easy to parse programmatically

**Correlation IDs:**
- Generate a unique `requestId` at API Gateway entry
- Pass it in headers to all downstream services
- Include in every log entry
- You can now trace ONE request across 10 microservices!

---

### Q3: What metrics should you track for a production Node.js API?

**Solution:**
**System metrics (auto-collected by CloudWatch for EC2):**
- CPU utilization (alert if > 80%)
- Memory utilization (alert if > 85%)
- Network I/O
- Disk I/O and usage

**Application metrics (custom):**
- Request rate (RPS per endpoint)
- Error rate (4xx and 5xx per endpoint)
- Response latency (P50, P95, P99 per endpoint)
- Active connections

**Business metrics:**
- User signups per hour
- Orders placed per hour
- Revenue per hour
- Conversion funnel drop-off rates

**Infrastructure metrics:**
- Database connections used/total (alert if > 80%)
- Redis memory used/total
- SQS queue depth (alert if messages pile up)
- Cache hit rate (alert if drops below 80%)

**Golden Signals (4 key metrics for any service):**
1. **Latency:** How long requests take
2. **Traffic:** How much demand
3. **Errors:** Rate of failed requests
4. **Saturation:** How "full" your service is (CPU, memory, queue depth)

---

### Q4: What is a distributed trace and why is it important for microservices?

**Solution:**
A distributed trace tracks a single request as it travels through multiple services. Each service adds a "span" to the trace (with start time, duration, metadata).

**Without distributed tracing:**
- User complains "checkout is slow"
- You have logs in 6 different services
- Can't correlate which logs belong to this user's request
- 2 hours to find the slow service

**With distributed tracing (AWS X-Ray):**
- Open trace for that request
- See: API Gateway (5ms) → Auth Service (3ms) → Order Service (10ms) → Payment Service (2500ms!) → Email Service (50ms)
- Immediately know: Payment Service is the bottleneck
- Click into Payment Service span → see: Stripe API call took 2500ms (timeout)
- Root cause in 5 minutes!

**Implementation:**
- Generate trace ID at entry point (API Gateway)
- Pass via `X-Amzn-Trace-Id` or `traceparent` header to all downstream services
- Each service creates a span and logs duration
- X-Ray assembles into visual flamegraph

---

### Q5: How do you set up alerting that doesn't create alert fatigue?

**Solution:**
Alert fatigue = too many false alerts → team starts ignoring alerts → real incidents missed.

**Rules for good alerting:**

1. **Alert on symptoms, not causes:**
   - ✅ "Users can't checkout" (symptom)
   - ❌ "CPU is at 75%" (cause — may not affect users at all)

2. **Set appropriate thresholds:**
   - Don't alert if P99 > 200ms (too sensitive, noisy)
   - Alert if P99 > 2000ms for 5+ minutes (actually affecting users)

3. **Severity levels:**
   - P1 (Critical): Pages on-call immediately — "Checkout is down"
   - P2 (High): Slack alert — "Error rate elevated at 2%"
   - P3 (Medium): Email daily digest — "Cache hit rate dropped to 78%"

4. **Runbooks for every alert:**
   - Each alert → link to runbook (what to check, how to fix)
   - Reduces panic, speeds up resolution

5. **Review and tune alerts:**
   - Monthly: Review false positive alerts
   - Remove or tune alerts that fired but required no action

6. **Alert on business metrics too:**
   - "Orders per minute dropped by 50%" → something is wrong!
   - Often catches issues before technical metrics do

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem 1: Your app was down for 30 minutes and you didn't know. Design an alerting system.

**Solution:**
```
Multi-layer alerting so you're notified within 2 minutes:

1. Uptime Monitoring (external perspective, catches total outages):
   - Use: AWS Route 53 Health Checks, or Pingdom, or Better Uptime
   - Ping /health endpoint from multiple regions every 30 seconds
   - If 3 consecutive failures → immediate alert
   - This is the "catch all" — detects total outages

2. Internal CloudWatch Alarms:
   - Error rate > 5% for 3 minutes → P1 alert
   - P99 latency > 5s for 3 minutes → P1 alert
   - Zero requests for 5 minutes (may indicate total failure) → P1 alert

3. Alert delivery:
   Alarm → SNS Topic → 
     → Lambda → Slack #incidents channel
     → Lambda → PagerDuty → on-call phone call
   
4. Escalation:
   - 0-5 min: Slack ping
   - 5-10 min: PagerDuty → on-call engineer phone call
   - 10-15 min: Escalate to team lead
   - 15+ min: Escalate to management

5. Status Page (so users know you know):
   - Statuspage.io or AWS Service Health
   - Auto-update when alarms fire
   - Tweet @yourstatus account

6. Post-mortem after every major incident:
   - What happened?
   - How long before detected?
   - How long to resolve?
   - What can we automate to detect/fix faster next time?
```

---

### Problem 2: Design logging for a financial transaction system

**Solution:**
```javascript
// Financial logs need: completeness, immutability, audit trail

const financialLogger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    // Primary: CloudWatch (searchable, alerts)
    new WinstonCloudWatch({ logGroupName: '/financial/transactions' }),
    // Backup: S3 for immutable audit trail
    new S3TransportStream({ bucket: 'financial-audit-logs', prefix: 'transactions' })
  ]
});

// Log every financial event
async function processPayment(orderId, userId, amount, method) {
  const txId = uuid();
  
  // Log: Payment initiated
  financialLogger.info('payment_initiated', {
    txId, orderId, userId,
    amount,  // Log the amount
    currency: 'USD',
    method,  // 'stripe', 'paypal'
    ip: req.ip,  // Log IP for fraud detection
    userAgent: req.headers['user-agent'],
    timestamp: new Date().toISOString()
  });
  
  try {
    const charge = await stripe.charges.create({ amount: amount * 100, currency: 'usd' });
    
    // Log: Payment succeeded
    financialLogger.info('payment_succeeded', {
      txId, orderId, userId, amount,
      stripeChargeId: charge.id,
      last4: charge.payment_method_details?.card?.last4
    });
    
    return charge;
  } catch (error) {
    // Log: Payment failed (MUST log this!)
    financialLogger.error('payment_failed', {
      txId, orderId, userId, amount,
      error: error.message,
      errorCode: error.code,  // Stripe error codes
      stripeDeclineCode: error.decline_code
    });
    throw error;
  }
}

// Audit log: Never delete financial logs
// Retention: 7 years minimum (legal requirement!)
// Access: Restricted to finance team + security
// Encryption: All logs encrypted at rest (CloudWatch + S3 with KMS)
// Compliance: PCI DSS requires audit trail for all card transactions
```

---

### Navigation
**Prev:** [20_Search_Design.md](20_Search_Design.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [22_Security_Basics.md](22_Security_Basics.md)
