# Network Monitoring & Observability

> 📌 **File:** 24_Network_Monitoring_And_Observability.md | **Level:** Full-Stack Dev → Networking Expert

---

## What is it?

Network monitoring is how you detect, diagnose, and resolve issues BEFORE users complain. Observability goes further — metrics, logs, and traces give you the ability to understand any system state from external outputs. You can't optimize what you can't measure.

---

## The Three Pillars of Observability

```
┌──────────────────────────────────────────────────────────────────┐
│  Pillar        │ What                    │ AWS Service           │
├────────────────┼─────────────────────────┼───────────────────────┤
│  Metrics       │ Numbers over time       │ CloudWatch Metrics    │
│                │ CPU, memory, latency,   │ + Grafana / Datadog   │
│                │ request count, errors   │                       │
│                │                         │                       │
│  Logs          │ Structured event records│ CloudWatch Logs       │
│                │ Request details, errors,│ + ELK / Loki          │
│                │ stack traces            │                       │
│                │                         │                       │
│  Traces        │ Request journey across  │ X-Ray                 │
│                │ services (distributed)  │ + Jaeger / Zipkin     │
├────────────────┴─────────────────────────┴───────────────────────┤
│                                                                  │
│  Metrics: "Something is wrong" (high error rate, slow responses)│
│  Logs: "What went wrong" (error details, stack trace)           │
│  Traces: "Where it went wrong" (which service, which query)    │
│  Together: Full picture for any production issue                │
└──────────────────────────────────────────────────────────────────┘
```

#### Diagram Explanation (The Hospital Vital Signs)
Observability conceptually is exactly like how a modern hospital monitors a patient:
- **Metrics (The Heart Monitor):** The steady beep-beep rhythm of raw numbers tracking over time. It visually tells you precisely *when* the patient's heart rate spikes out of nowhere ("Something is terribly wrong!").
- **Logs (The Doctor's Notepad):** The structured, chronological paragraphs of exactly what the patient ate, what medicine they took, and what they complained about ("Here is precisely *what* went wrong").
- **Traces (The MRI Scan):** Physically following a single illuminated drop of radioactive dye flow smoothly through the patient's entire vascular system across multiple organs ("Ah, it entered the API Gateway reliably, but it definitively got stuck deep inside the Redis database organ").

---

## Key Network Metrics to Monitor

```
┌──────────────────────────────────────────────────────────────────┐
│  Metric                     │ Why it Matters                    │
├─────────────────────────────┼───────────────────────────────────┤
│  Request latency (p50/p95/p99)│ User experience directly        │
│  Error rate (5xx %)          │ Application health               │
│  Request rate (req/sec)      │ Load / capacity planning         │
│  TCP connections (active)    │ Connection pool health           │
│  TCP connections (TIME_WAIT) │ Connection churn                  │
│  Bandwidth (bytes in/out)    │ Data transfer costs              │
│  DNS resolution time         │ DNS health                        │
│  TLS handshake time          │ Certificate / config issues      │
│  ALB target response time    │ Backend performance               │
│  ALB healthy targets         │ Service availability              │
│  NAT Gateway bytes processed │ Cost optimization                │
│  VPC Flow Logs (rejected)    │ Security / misconfiguration      │
│  Event loop lag              │ Node.js performance               │
│  Memory heap usage           │ Memory leak detection             │
│  DB connection pool usage    │ Pool exhaustion risk              │
└─────────────────────────────┴───────────────────────────────────┘
```

---

## Node.js Application Monitoring

```javascript
const express = require('express');
const client = require('prom-client');  // Prometheus metrics

const app = express();

// ──── Prometheus Metrics ────
const register = new client.Registry();
client.collectDefaultMetrics({ register }); // Node.js defaults

// Custom metrics
const httpRequestDuration = new client.Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests',
  labelNames: ['method', 'route', 'status'],
  buckets: [0.01, 0.05, 0.1, 0.5, 1, 2, 5, 10]
});
register.registerMetric(httpRequestDuration);

const httpRequestTotal = new client.Counter({
  name: 'http_requests_total',
  help: 'Total HTTP requests',
  labelNames: ['method', 'route', 'status']
});
register.registerMetric(httpRequestTotal);

const activeConnections = new client.Gauge({
  name: 'active_connections',
  help: 'Number of active connections'
});
register.registerMetric(activeConnections);

const dbPoolGauge = new client.Gauge({
  name: 'db_pool_connections',
  help: 'Database connection pool status',
  labelNames: ['db', 'state']
});
register.registerMetric(dbPoolGauge);

// ──── Metrics Middleware ────
app.use((req, res, next) => {
  const start = Date.now();
  activeConnections.inc();
  
  res.on('finish', () => {
    const duration = (Date.now() - start) / 1000;
    const route = req.route?.path || req.path;
    
    httpRequestDuration.observe(
      { method: req.method, route, status: res.statusCode },
      duration
    );
    httpRequestTotal.inc(
      { method: req.method, route, status: res.statusCode }
    );
    activeConnections.dec();
  });
  
  next();
});

// ──── Metrics Endpoint (Prometheus scrapes this) ────
app.get('/metrics', async (req, res) => {
  // Update DB pool metrics
  dbPoolGauge.set({ db: 'mongodb', state: 'active' }, 
    mongoose.connection.client.topology?.s?.pool?.currentCheckedOutCount || 0);
  dbPoolGauge.set({ db: 'mongodb', state: 'available' }, 
    mongoose.connection.client.topology?.s?.pool?.availableConnectionCount || 0);
  
  res.set('Content-Type', register.contentType);
  res.end(await register.metrics());
});

// ──── Structured Logging ────
function log(level, message, meta = {}) {
  console.log(JSON.stringify({
    timestamp: new Date().toISOString(),
    level,
    message,
    service: 'api-service',
    environment: process.env.NODE_ENV,
    ...meta
  }));
}

// Usage in request handler:
app.use((req, res, next) => {
  const requestId = req.headers['x-request-id'] || crypto.randomUUID();
  req.requestId = requestId;
  res.set('X-Request-ID', requestId);
  
  res.on('finish', () => {
    log('info', 'HTTP Request', {
      requestId,
      method: req.method,
      url: req.url,
      status: res.statusCode,
      duration: Date.now() - req.startTime,
      ip: req.ip,
      userAgent: req.headers['user-agent']?.substring(0, 80)
    });
  });
  
  req.startTime = Date.now();
  next();
});
```

---

## AWS CloudWatch Alarms

```
┌──────────────────────────────────────────────────────────────────┐
│  Critical Alarms (page on-call)                                 │
├─────────────────────────────────────────────────────────────────┤
│  ALB 5xx error rate > 5%         → Backend is failing          │
│  ALB healthy targets < 2         → Servers are down            │
│  ALB target response time > 5s   → Backend is slow             │
│  EC2 CPU > 80% for 5 min         → Scale up needed             │
│  RDS connections > 80% of max    → Pool exhaustion risk        │
│  RDS CPU > 80% for 5 min         → Query optimization needed  │
│  Redis memory > 80%              → Eviction starting           │
│                                                                 │
│  Warning Alarms (Slack notification)                            │
├─────────────────────────────────────────────────────────────────┤
│  ALB 4xx error rate > 10%        → Bad client requests         │
│  EC2 memory > 70%                → Memory leak possible        │
│  NAT Gateway bytes > threshold   → Cost alert                  │
│  Certificate expiry < 30 days    → Renewal needed              │
│  VPC Flow Logs rejections > N    → Possible attack / misconfig │
└──────────────────────────────────────────────────────────────────┘
```

### Setting Up CloudWatch Alarms (AWS CLI)

```bash
# ALB 5xx alarm
aws cloudwatch put-metric-alarm \
  --alarm-name "ALB-5xx-High" \
  --metric-name "HTTPCode_Target_5XX_Count" \
  --namespace "AWS/ApplicationELB" \
  --statistic Sum \
  --period 300 \
  --threshold 50 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 2 \
  --dimensions Name=LoadBalancer,Value=app/my-alb/xxxxx \
  --alarm-actions arn:aws:sns:us-east-1:123456789:alerts

# RDS CPU alarm
aws cloudwatch put-metric-alarm \
  --alarm-name "RDS-CPU-High" \
  --metric-name "CPUUtilization" \
  --namespace "AWS/RDS" \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 3 \
  --dimensions Name=DBInstanceIdentifier,Value=mydb \
  --alarm-actions arn:aws:sns:us-east-1:123456789:alerts
```

---

## Distributed Tracing

```javascript
// ──── Trace a request across services ────
// Request ID propagation — the simplest form of tracing

// API Gateway / ALB adds: X-Request-ID (or X-Amzn-Trace-Id)
// Your services PROPAGATE this ID through all calls

// Express middleware:
app.use((req, res, next) => {
  req.traceId = req.headers['x-amzn-trace-id'] || 
                req.headers['x-request-id'] || 
                crypto.randomUUID();
  
  // Pass to all downstream calls
  req.traceHeaders = {
    'X-Request-ID': req.traceId,
    'X-Amzn-Trace-Id': req.headers['x-amzn-trace-id']
  };
  
  next();
});

// When calling other services:
async function callUserService(userId, traceHeaders) {
  return axios.get(`${USER_SERVICE}/users/${userId}`, {
    headers: traceHeaders,  // Propagate trace ID!
    timeout: 5000
  });
}

// Now you can search logs by X-Request-ID across ALL services
// to see the complete journey of a single request.

// CloudWatch Logs Insights query:
// fields @timestamp, @message
// | filter @message like /request-id-here/
// | sort @timestamp asc
```

---

## VPC Flow Logs

```
VPC Flow Logs capture ALL network traffic metadata:

Format: version account-id interface-id srcaddr dstaddr 
        srcport dstport protocol packets bytes start end 
        action log-status

Example entries:
  2 123456789 eni-abc 10.0.1.10 10.0.20.5 49152 5432 6 10 840 
  1620000000 1620000060 ACCEPT OK
  → EC2 (10.0.1.10) connected to RDS (10.0.20.5:5432) ✅

  2 123456789 eni-abc 203.0.113.50 10.0.1.10 12345 22 6 5 300 
  1620000000 1620000060 REJECT OK
  → Someone tried SSH from 203.0.113.50 → REJECTED ❌
  (security group blocked it)

Useful queries:
  - Find rejected connections (security group / NACL issues)
  - Track top talkers (bandwidth analysis)
  - Detect port scanning attempts
  - Identify unexpected traffic patterns
```

---

## Health Check Dashboard

```javascript
// ──── Comprehensive Health Endpoint ────
app.get('/health/detailed', async (req, res) => {
  const checks = {};
  const start = Date.now();
  
  // MongoDB
  try {
    const mongoStart = Date.now();
    await mongoose.connection.db.admin().ping();
    checks.mongodb = { status: 'healthy', latency: Date.now() - mongoStart };
  } catch (err) {
    checks.mongodb = { status: 'unhealthy', error: err.message };
  }
  
  // Redis
  try {
    const redisStart = Date.now();
    await redis.ping();
    checks.redis = { status: 'healthy', latency: Date.now() - redisStart };
  } catch (err) {
    checks.redis = { status: 'unhealthy', error: err.message };
  }
  
  // External API
  try {
    const apiStart = Date.now();
    await axios.get('https://api.stripe.com/v1/', { timeout: 5000 });
    checks.stripe = { status: 'healthy', latency: Date.now() - apiStart };
  } catch (err) {
    checks.stripe = { status: 'degraded', error: err.message };
  }
  
  // System
  checks.system = {
    uptime: process.uptime(),
    memory: process.memoryUsage(),
    eventLoopLag: await measureEventLoopLag(),
    activeHandles: process._getActiveHandles().length,
    nodeVersion: process.version
  };
  
  const allHealthy = Object.values(checks)
    .filter(c => c.status)
    .every(c => c.status === 'healthy');
  
  res.status(allHealthy ? 200 : 503).json({
    status: allHealthy ? 'healthy' : 'degraded',
    totalLatency: Date.now() - start,
    checks,
    timestamp: new Date().toISOString()
  });
});

async function measureEventLoopLag() {
  return new Promise(resolve => {
    const start = process.hrtime.bigint();
    setImmediate(() => {
      resolve(Number(process.hrtime.bigint() - start) / 1e6); // ms
    });
  });
}
```

---

## Common Mistakes

### ❌ No Alerts — Finding Issues From User Complaints

```
❌ User emails: "Your site is down"
   You check: Oh, EC2 crashed 2 hours ago. Nobody noticed.
   
✅ CloudWatch Alarm → SNS → PagerDuty/Slack within 5 minutes
   Automatic notification when health check fails.
   Alert BEFORE users are affected.
```

### ❌ Logging Without Structure

```javascript
// ❌ Unstructured logs — impossible to search
console.log('Error: something went wrong for user 123');

// ✅ Structured JSON logs — queryable in CloudWatch Insights
console.log(JSON.stringify({
  level: 'error',
  message: 'Payment processing failed',
  userId: '123',
  orderId: '456',
  error: err.message,
  requestId: req.traceId,
  timestamp: new Date().toISOString()
}));
```

---

## Practice Exercises

### Exercise 1: Prometheus Metrics
Add Prometheus metrics to your Express app. Track request duration, error rate, and active connections. View metrics at `/metrics`.

### Exercise 2: CloudWatch Alarms
Set up alarms for: ALB 5xx > 10 per 5 minutes, EC2 CPU > 80%, RDS connections > 80% of max. Send to an SNS topic.

### Exercise 3: Distributed Tracing
Propagate X-Request-ID across two services. Search CloudWatch Logs by request ID to see the full request journey.

---

## Interview Q&A

**Q1: What are the three pillars of observability?**
> Metrics (numerical time-series data — CPU, latency, error rate), Logs (structured event records — request details, errors), Traces (request journey across services — which service, how long). Together they answer: what's wrong, what happened, and where it happened.

**Q2: How do you monitor a Node.js application in production?**
> Prometheus for metrics (request duration, error rate, event loop lag, memory). Structured JSON logs to CloudWatch Logs. Distributed tracing with X-Request-ID propagation. Health check endpoints for ALB. CloudWatch alarms for critical thresholds. Custom dashboards in Grafana/CloudWatch.

**Q3: What is distributed tracing and why is it important for microservices?**
> A single user request may touch 5-10 services. Distributed tracing assigns a trace ID at entry and propagates it through all services. When something fails, you search by trace ID to see every service touched, timing, and where the error occurred. Without it, debugging microservices is nearly impossible.

**Q4: What CloudWatch alarms would you set up for a production web app?**
> Critical: ALB 5xx rate, healthy target count, target response time, EC2 CPU, RDS CPU and connections, certificate expiry. Warning: 4xx rate, memory usage, NAT Gateway costs, disk usage. Use SNS for notifications and auto-scaling policies for automatic response.

**Q5: How do VPC Flow Logs help with security and debugging?**
> Flow Logs capture metadata for all VPC traffic (source, destination, port, action). For security: detect port scanning, unauthorized access attempts, data exfiltration. For debugging: verify security group rules are correct, identify rejected connections, track traffic patterns between services.


Prev : [23 VPC Architecture And Design](./23_VPC_Architecture_And_Design.md) | Index: [0 Index](./0_Index.md) | Next : [25 Deployment And Production Infrastructure](./25_Deployment_And_Production_Infrastructure.md)
