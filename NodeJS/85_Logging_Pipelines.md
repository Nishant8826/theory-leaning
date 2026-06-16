# Logging Pipelines

Logging is your primary tool for forensic debugging in production. If your application logs are unstructured plain text, searching through millions of lines during an incident is virtually impossible. Standard tools like `console.log` run synchronously under the hood when writing to terminals or files, severely blocking the Event Loop. Production systems require structured, asynchronous JSON logs shipped automatically to a centralized dashboard.

### Structured vs. Unstructured Logging
* **Unstructured Logging**: Human-readable text strings.
  * *Example*: `[INFO] 2026-06-15 10:15:30 User Alice logged in from 192.168.1.1`
  * *Drawback*: Parsing these logs requires complex regular expressions which break if the log format changes slightly.
* **Structured Logging**: Formatting log events as structured JSON objects.
  * *Example*: `{"time":1773663330000,"level":"info","msg":"User logged in","userId":"Alice","ip":"192.168.1.1"}`
  * *Benefit*: Instantly queryable by log search engines (e.g., Elasticsearch, Loki) without custom parsers.

### Log Levels
Logs are classified by severity to allow filtering:
1. **Fatal**: Severe errors causing immediate application shutdown (e.g., database connection loss).
2. **Error**: Operations that failed but did not crash the system (e.g., payment transaction failure).
3. **Warn**: Unexpected events that don't stop the flow (e.g., deprecated API usage, high disk usage warning).
4. **Info**: Regular operational events (e.g., server started, user checked out).
5. **Debug**: Fine-grained informational events useful for local troubleshooting.
6. **Trace**: Extremely detailed logs (e.g., raw SQL query dumps, memory profiles).

---

## Deep Dive

### The Performance Cost of Console.Log
In Node.js, `console.log` is blocking. When writing to a terminal or a redirected file, V8 serializes the arguments and writes them to stdout using synchronous system writes (`fs.writeSync`). This blocks the single execution thread, causing Event Loop delays and bottlenecking requests.

### High-Performance Logging with Pino
Pino is an extremely fast JSON logger for Node.js. It achieves low overhead by:
1. **JSON Serialization**: Using fast string concatenation instead of slow `JSON.stringify`.
2. **Asynchronous Logging**: Writing logs to memory buffers and flushing them to stdout in chunks, rather than writing synchronously on every log invocation.

```javascript
// Enable non-blocking asynchronous logging in Pino
import pino from 'pino';
const logger = pino(pino.destination({ sync: false }));
```

---

## Visual Explanation

### Modern Logging Pipeline Architecture
Instead of having Node.js write to files or make network requests to log aggregators, the containerized standard is to write logs directly to `stdout`. A separate, lightweight daemon collects and ships those logs.

```text
 [ Express App ] ──> Logs JSON to stdout (non-blocking)
      │
      ▼ (Container Runtime redirects stdout to log files)
 [ Host Log File (/var/log/pods/...) ]
      │
      ▼ (Lightweight Collector watches file changes)
 [ Log Shipper (Fluentbit / Vector) ] ── (Batches & Compresses) ──┐
                                                                 │
                                                                 ▼
                                                    [ Loki / Elasticsearch ]
                                                                 │
                                                                 ▼
                                                     [ Grafana / Kibana ]
```

---

## Real-World Example
In a checkout service handling 10,000 requests per minute, tracing a user's failure across microservices is difficult. To solve this, a unique `Correlation ID` (or `Request ID`) is generated at the gateway and attached to the request headers. Every log statement inside the checkout, payment, and inventory services logs this ID. If checkout fails, querying the ID in Grafana Loki reconstructs the exact timeline of operations across all microservices.

---

## Code Examples

### Setting up Structured, Asynchronous Logging with Express and Pino
First, install the logging libraries:
```bash
npm install pino pino-http express
```

Create `logger.js` to manage the Pino instance:

```javascript
// logger.js
import pino from 'pino';

// Initialize Pino with configuration
const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  // Format log timestamps to ISO strings
  timestamp: pino.stdTimeFunctions.isoTime,
  // Redact sensitive payload keys to avoid logging private information
  redact: {
    paths: ['req.headers.authorization', 'req.body.password', 'req.body.creditCard'],
    censor: '[REDACTED]'
  },
  // Customize log level outputs in production vs development
  formatters: {
    level: (label) => {
      return { level: label.toUpperCase() };
    },
  },
}, pino.destination({
  // Enable async log flushing to avoid blocking the Event Loop
  sync: false,
  minLength: 4096 // Buffer up to 4KB of log text before flushing
}));

// Gracefully flush logs to stdout on process exit
process.on('exit', () => logger.flush());

export default logger;
```

Create the application script `app.js` using `pino-http` to generate request contexts:

```javascript
// app.js
import express from 'express';
import { pinoHttp } from 'pino-http';
import { randomUUID } from 'crypto';
import logger from './logger.js';

const app = express();
app.use(express.json());

// Integrate pino-http middleware
app.use(pinoHttp({
  logger,
  // Generate a unique Correlation ID for every request if not sent by client
  genReqId: (req) => {
    return req.headers['x-correlation-id'] || randomUUID();
  },
  // Custom serializer to reduce verbose log outputs
  serializers: {
    req(req) {
      return {
        id: req.id,
        method: req.method,
        url: req.url,
      };
    },
    res(res) {
      return {
        statusCode: res.statusCode,
      };
    }
  }
}));

app.post('/api/checkout', (req, res) => {
  // Access the request-scoped logger configured with the request ID
  const reqLogger = req.log;

  reqLogger.info({ userId: req.body.userId }, 'Processing checkout request');

  if (!req.body.cart || req.body.cart.length === 0) {
    reqLogger.warn('Attempted checkout with an empty cart');
    return res.status(400).json({ error: 'Cart is empty' });
  }

  // Simulate payment processing
  try {
    reqLogger.info('Authorizing payment transaction');
    // Simulate transaction execution
    res.json({ success: true, transactionId: randomUUID() });
  } catch (error) {
    reqLogger.error({ err: error }, 'Checkout payment failed');
    res.status(500).json({ error: 'Payment failed' });
  }
});

app.listen(3000, () => {
  logger.info('API Gateway server listening on port 3000');
});
```

---

## Best Practices
* **Never Log Secrets**: Redact fields like `password`, `token`, `secret`, and `creditCard` at the logger configuration boundary to prevent PII (Personally Identifiable Information) data exposure in logging databases.
* **Log to Stdout**: Do not configure Node.js to write directly to files in containerized systems (Docker/Kubernetes). Let the container runtime capture `stdout` and leverage specialized logging sidecars to forward them.
* **Generate Request IDs**: Inject a correlation ID at the HTTP gateway level and pass it down via headers to all internal services, logging the ID in every microservice trace.
* **Configure Asynchronous Flush**: Under high traffic, configure pino's buffer to prevent Event Loop blockage. Make sure to call `logger.flush()` on exit signals (`SIGINT`, `SIGTERM`) to avoid losing buffered logs during restarts.

---

## Interview Questions

**Q:** Why is `console.log` discouraged in production Node.js applications?

> **Answer:**
> `console.log` is a synchronous operation when output is redirected to files or pipe terminals. This blocks the main thread, delaying event loop cycles and dropping application performance. Additionally, it outputs unstructured string text which is difficult to query in production log tools.

**Q:** What is a structured log, and what are its advantages?

> **Answer:**
> A structured log is a log entry formatted as a standardized machine-readable data object, typically JSON, rather than a raw text string. This allows log collectors and indexers (like Elasticsearch or Loki) to instantly parse, index, search, and aggregate logs by specific fields (like `userId`, `statusCode`, or `latency`) without requiring complex regex patterns.

**Q:** How can you implement request-scoped logging to track all actions under a single HTTP request in Node.js?

> **Answer:**
> You can use **AsyncLocalStorage** (part of the `async_hooks` module) or libraries built on top of it, such as `pino-http`. At the request entry point, you generate a unique Correlation ID and attach it to a logger instance inside an async storage context. All subsequent asynchronous operations invoked under that request scope can retrieve the active logger context, logging the correlation ID automatically without needing to pass the logger variable through every function parameter.

**Q:** Describe the architecture of a centralized logging system for a Node.js microservice fleet handling thousands of requests per second. How do you prevent log storage bottlenecks and system resource contention?

> **Answer:**
> To handle high volume logging efficiently:
> 1. **Non-Blocking Output**: Node.js instances log in JSON format directly to `stdout` asynchronously using `pino` with output buffers enabled to prevent blocking the Event Loop.
> 2. **Decoupled Collection**: A local log shipper (like **Fluentbit** or **Vector**) runs as a daemonset on the host, scraping container stdout log files, parsing the JSON metadata, and batching logs in memory.
> 3. **Message Queue Buffer**: In extremely high-throughput systems, the log shippers forward events to a message queue like **Apache Kafka** instead of writing directly to the database. This acts as a buffer and prevents DB overload.
> 4. **Indexing Database**: Log indexing consumers pull data from Kafka and ingest it into clustered search databases like **Elasticsearch / OpenSearch** or log-aggregators like **Grafana Loki** (which index metadata labels, rather than full raw text, reducing disk footprint).
> 5. **Retention Policies**: Configure strict index retention periods (e.g., delete debug logs after 7 days, info logs after 30 days) and archive raw files to cold storage (e.g., AWS S3) for long-term compliance.

---
Previous : [84_Monitoring.md](84_Monitoring.md) | Index : [00_index.md](00_index.md) | Next : [86_Distributed_Tracing.md](86_Distributed_Tracing.md)
