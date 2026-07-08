# Network Monitoring & Observability

> 📌 **File:** 25_Network_Monitoring_And_Observability.md | **Level:** Full-Stack Dev → Networking Expert

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
│  Logs          │ Structured event records│ CloudWatch Logs       │
│  Traces        │ Request journey across  │ X-Ray                 │
└────────────────┴─────────────────────────┴───────────────────────┘
```

- **Metrics:** "Something is wrong" (high error rate, slow responses).
- **Logs:** "What went wrong" (error details, stack trace).
- **Traces:** "Where it went wrong" (which service, which query).

#### Diagram Explanation (The Hospital Vital Signs)
Observability is like how a hospital monitors a patient:
- **Metrics (The Heart Monitor):** The steady beep-beep of numbers tracking over time. It tells you *when* the heart rate spikes ("Something is wrong").
- **Logs (The Doctor's Notepad):** Chronological paragraphs of exactly what the patient ate, drank, and complained about ("Here is *what* went wrong").
- **Traces (The MRI Scan):** Following a single drop of dye flow through the entire vascular system across organs ("Ah, it entered the API Gateway, but it got stuck in the Redis database organ").

---

## Key Network Metrics to Monitor

```
┌──────────────────────────────────────────────────────────────────┐
│  Metric                     │ Why it Matters                    │
├─────────────────────────────┼───────────────────────────────────┤
│  Request latency (p50/p95)  │ User experience directly        │
│  Error rate (5xx %)          │ Application health               │
│  TCP connections (active)    │ Connection pool health           │
│  ALB healthy targets         │ Service availability              │
│  NAT Gateway bytes processed │ Cost optimization                │
│  VPC Flow Logs (rejected)    │ Security / misconfiguration      │
└─────────────────────────────┴───────────────────────────────────┘
```

---

## Node.js Application Monitoring

```javascript
const express = require('express');
const client = require('prom-client'); // Prometheus metrics

const app = express();

const register = new client.Registry();
client.collectDefaultMetrics({ register });

const httpRequestDuration = new client.Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests',
  labelNames: ['method', 'route', 'status']
});
register.registerMetric(httpRequestDuration);

app.use((req, res, next) => {
  const start = Date.now();
  res.on('finish', () => {
    const duration = (Date.now() - start) / 1000;
    const route = req.route?.path || req.path;
    httpRequestDuration.observe(
      { method: req.method, route, status: res.statusCode },
      duration
    );
  });
  next();
});

app.get('/metrics', async (req, res) => {
  res.set('Content-Type', register.contentType);
  res.end(await register.metrics());
});
```

---

## Distributed Tracing

In a microservice architecture, propagate trace IDs down the call chain using headers:

```javascript
app.use((req, res, next) => {
  req.traceId = req.headers['x-request-id'] || crypto.randomUUID();
  req.traceHeaders = {
    'X-Request-ID': req.traceId
  };
  next();
});

async function callUserService(userId, traceHeaders) {
  return axios.get(`${USER_SERVICE}/users/${userId}`, {
    headers: traceHeaders, // Propagate trace ID!
    timeout: 5000
  });
}
```

---

## Practice Exercises

### Exercise 1: Prometheus Integration
Add Prometheus metrics to your Express app. Run load tests locally and verify the metric outputs.

### Exercise 2: Structured Logging
Format your application error logs as JSON objects. Verify that fields like `requestId`, `error`, and `timestamp` are parsed.

---

## Interview Q&A

**Q1: What are the three pillars of observability?**
> Metrics (numerical time-series data — CPU, latency, error rate), Logs (structured event records — request details, errors), Traces (request journey across services). Together they answer: what's wrong, what happened, and where it happened.

**Q2: How do you monitor a Node.js application in production?**
> Prometheus for metrics (request duration, error rate, event loop lag, memory). Structured JSON logs sent to CloudWatch Logs. Distributed tracing with X-Request-ID propagation. Health check endpoints for ALB.

**Q3: What is distributed tracing and why is it important for microservices?**
> A single user request may touch multiple services. Distributed tracing assigns a trace ID at entry and propagates it through all downstream API calls. When something fails, you search by trace ID to see every service touched, timing, and where the error occurred.

**Q4: What CloudWatch alarms would you set up for a production web app?**
> Critical alarms: ALB 5xx rate, healthy target count, target response time, EC2 CPU, RDS CPU and connections, and certificate expiry.

**Q5: How do VPC Flow Logs help with security and debugging?**
> Flow Logs capture metadata for all VPC traffic. For security: detect unauthorized access attempts and port scanning. For debugging: verify security group rules are correct and identify rejected connections.

---

Prev : [24 Performance Optimization](./24_Performance_Optimization.md) | Index: [00 Index](./00_Index.md) | Next : [26 Deployment And Production Infrastructure](./26_Deployment_And_Production_Infrastructure.md)
