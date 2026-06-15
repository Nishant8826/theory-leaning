# Logging

## What You Will Learn
* Why `console.log` is an anti-pattern for production backend systems.
* Structuring logs using Log Levels (info, debug, warn, error, fatal).
* The benefits of structured JSON logs for logging pipelines.
* Comparing logging libraries (Winston vs. Pino).
* Building custom request logger middleware that tracks execution duration.

## Why This Matters
Logs are the eyes and ears of a production application. Using `console.log` blocks the event loop because writing to standard output (`stdout`) is a synchronous operation on most operating systems. Additionally, unstructured text logs are difficult to search or parse. Structured JSON logging keeps your applications fast and makes searching, filtering, and indexing logs in production tools easy.

## Theory

### Why `console.log` is Bad for Production
1. **Blocks the Event Loop**: When writing to a terminal (TTY) or a local file, `console.log` writes synchronously. This blocks the main thread, halting request processing.
2. **Lack of Metadata**: Standard output logs lack timestamps, process IDs, error levels, and request trace IDs.
3. **No Log Rotation**: Writing to standard output indefinitely will eventually exhaust the host's disk space unless managed by external log rotators.

### Structured Logging and Log Levels
Structured logging writes log entries as structured JSON objects instead of plain text strings. This format is easily parsed by log shippers (like Fluentd, Logstash, or vector) and stored in search databases (like Elasticsearch, Grafana Loki, or Datadog).

Logs are classified by **Log Levels** to manage volume:
* **fatal**: System crashes; the process must restart immediately.
* **error**: Critical issues (like database connection drops or unhandled exceptions).
* **warn**: Minor anomalies that do not stop execution (like deprecation warnings or slow queries).
* **info**: Standard informational events (like server startup or database sync).
* **debug**: Detailed trace logs used during development (like variable values or request payloads).
* **trace**: Extremely verbose telemetry data.

## Deep Dive

### Logging Libraries: Winston vs. Pino
* **Winston (Feature-Rich)**: A flexible, feature-rich logging library. It supports multiple transports, allowing you to route logs to different destinations (like files, databases, or third-party APIs) directly from your application code.
* **Pino (High-Performance)**: A highly optimized, fast logging library. Pino is designed to minimize CPU overhead. It writes logs to `stdout` as JSON using optimized string serialization, shifting routing and transport tasks to external processes (like log shippers) to keep the Node process fast.

## Visual Explanation

### Log Shipping Architecture
```text
  [ Node.js Process ] ── Writes structured JSON to stdout ──> [ OS stdout stream ]
                                                                      │
                                                                      ▼ (Non-blocking redirect)
                                                             [ Log Shipper Agent ]
                                                            (Fluentd / Vector / Loki)
                                                                      │
                                                                      ▼ (Batch send)
                                                             [ Search Database ]
                                                          (Elasticsearch / Grafana)
                                                                      │
  [ Ops / Dev Engineers ] <── Queries metrics / dashboards ───────────┘
```

## Real-World Example
Consider an API endpoint `/checkout`. When a payment fails, you log the event: `{ "level": "error", "message": "Payment failed", "userId": 42, "amount": 100 }`. Because this log is structured, developers can query Elasticsearch for all errors on the checkout endpoint for a specific user ID, rather than scanning plain text files manually.

## Code Examples

### Pino Logger Setup and Express Logger Middleware

```javascript
// utils/logger.js
const pino = require('pino');

// 1. Initialize Pino Logger
const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  // Format JSON logs with consistent properties
  base: {
    pid: process.pid,
    env: process.env.NODE_ENV || 'development'
  },
  // In development, format logs to be human-readable instead of raw JSON
  transport: process.env.NODE_ENV !== 'production' ? {
    target: 'pino-pretty',
    options: { colorize: true, translateTime: 'SYS:standard' }
  } : undefined
});

module.exports = logger;
```

```javascript
// app.js
const express = require('express');
const logger = require('./utils/logger');

const app = express();
app.use(express.json());

// 2. Custom Express Request Logger Middleware
app.use((req, res, next) => {
  const startTime = Date.now();
  
  // Attach the logger instance to the request object
  req.log = logger.child({ requestId: Math.random().toString(36).substring(7) });

  // Event fires once the response has been sent to the socket
  res.on('finish', () => {
    const duration = Date.now() - startTime;
    const logData = {
      method: req.method,
      url: req.url,
      statusCode: res.statusCode,
      duration: `${duration}ms`,
      userAgent: req.headers['user-agent']
    };

    if (res.statusCode >= 500) {
      req.log.error(logData, 'Request failed');
    } else if (res.statusCode >= 400) {
      req.log.warn(logData, 'Client validation issue');
    } else {
      req.log.info(logData, 'Request completed successfully');
    }
  });

  next();
});

// Sample Routes
app.get('/api/users', (req, res) => {
  req.log.debug({ query: req.query }, 'Executing search query...');
  res.json([{ id: 1, name: 'Alice' }]);
});

app.get('/api/error', (req, res) => {
  res.status(500).json({ error: 'Internal Server Error' });
});

app.listen(3000, () => {
  logger.info('Server successfully initialized on port 3000');
});
```

## Best Practices
* **Never use `console.log` in Production**: Use a production-grade logger library like Pino or Winston.
* **Log as Structured JSON**: Always output logs in JSON format in production.
* **Keep Transports out of the Node process**: Avoid writing logs directly to files, databases, or external APIs from inside your Node.js application, as this blocks execution. Write to `stdout` and let a log shipper handle routing.
* **Sanitize Secrets**: Strip sensitive data (like passwords, credit card numbers, or session tokens) before logging to prevent credential leaks.

## Interview Questions

### Beginner
* **Why should you avoid using `console.log` in production applications?**
  *Answer*: `console.log` writes to `stdout` synchronously, which blocks the single-threaded event loop and slows down request processing under load. Additionally, it lacks structured metadata (like timestamps and log levels) and is difficult to parse or search.

### Intermediate
* **What is structured logging and why is it preferred over plain text logs?**
  *Answer*: Structured logging writes log entries as structured JSON objects. This format is preferred because it allows log shippers and databases (like Elasticsearch or Loki) to index log properties dynamically, making searching, filtering, and metric aggregation in production dashboards easy.

### Advanced
* **Explain how Pino achieves higher performance than Winston.**
  *Answer*: Pino is designed with a "zero-overhead" philosophy. Instead of processing logs in memory, stringifying objects dynamically, or managing multiple transports inside the application thread, Pino converts JS objects to strings using highly optimized serialization schemas. It writes logs to `stdout` as a single stream, offloading formatting and routing tasks to external processes to keep the main application thread fast.

### Senior Architect
* **How would you design a distributed request tracing system across a microservices fleet, ensuring that a single API request can be traced across multiple services in log dashboards?**
  *Answer*: To trace requests across microservices:
  1. Generate a unique trace ID (e.g. using UUIDs) at the entry point of the network (like an API Gateway or the first receiving service) if one is not already present in the headers.
  2. Implement an Express middleware that checks the incoming headers for a correlation identifier (e.g. `X-Correlation-ID` or OpenTelemetry headers).
  3. Store this trace ID in a request context layer (such as **AsyncLocalStorage**).
  4. Configure your logger library to read this trace ID from the context and append it automatically to all logs generated during that request.
  5. When the service calls another microservice (via HTTP, gRPC, or message queues), forward the trace ID in the request headers, ensuring that all logs generated across the microservices fleet share the same trace ID for easy debugging.

---
Previous : [30_Error_Handling.md] | Index : [00_index.md] | Next : [32_Authentication.md]
