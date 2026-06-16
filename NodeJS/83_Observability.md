# Observability

In a distributed Node.js microservice architecture, troubleshooting failures becomes extremely complex. Standard tools like local log files are insufficient because a single user request might cross five different network boundaries. Observability allows you to infer the internal state of your system by analyzing its external outputs (telemetry data), allowing you to pinpoint performance bottlenecks and locate silent failures in real-time.

### Monitoring vs. Observability
* **Monitoring**: Focuses on the *known-unknowns*. It asks: *"Is the CPU usage above 80%?"* or *"Is the HTTP 500 error rate high?"* It alerts you when pre-defined thresholds are crossed.
* **Observability**: Focuses on the *unknown-unknowns*. It asks: *"Why is request latency spiking specifically for user accounts created in June when they try to check out?"* It provides the rich context needed to debug complex, non-obvious issues without deploying new code.

### The Three Pillars (M.E.L.T.)
1. **Metrics**: Aggregatable numeric data measuring system health over time (e.g., CPU load, request count, garbage collection pause duration). Highly efficient to store; best for alerts.
2. **Logs**: Structured, timestamped text records of discrete events (e.g., a query failed, user logged in). Essential for detailed debugging.
3. **Traces**: Represent the end-to-end journey of a request as it flows through a distributed system. A trace is made of multiple **Spans** (individual units of work).

### Black-Box vs. White-Box Monitoring
* **Black-Box**: Inspecting the system from the outside. Example: Ping tests, port scanning, checking if public HTTP routes return 200 OK.
* **White-Box**: Inspecting the system internals using internal exposure. Example: Querying the Node.js process heap memory usage, Event Loop latency, or database connection pool health.

---

## Deep Dive

### OpenTelemetry (OTel)
OpenTelemetry is a vendor-neutral, open-source standard for gathering telemetry data. It combines API definitions and SDK implementations to collect metrics, logs, and traces.

* **API**: Defines data types and how telemetry data is written. Code written using the OTel API is decoupled from the backend storage.
* **SDK**: Implements the API and handles the actual processing, buffering, and exporting of the telemetry data to backends like Jaeger, Prometheus, or Datadog.

#### Instrumentation Paradigms
* **Auto-Instrumentation**: OTel can dynamically intercept and patch Node.js core modules (`http`, `https`) and popular libraries (Express, Mongoose, PostgreSQL, Redis) at runtime. It creates spans and logs metadata automatically.
* **Manual Instrumentation**: Custom code written by developers using the OTel API to measure specific business processes or custom application logic.

---

## Visual Explanation

### Distributed Request Tracing and Span Hierarchy
When a client hits an API Gateway, a `Trace ID` is generated. This ID is passed to downstream services via HTTP headers (e.g., `W3C Trace Context`), stitching the entire request flow into a single logical timeline.

```text
Trace ID: 4bf92f3577b34da6a3ce929d0e0e4736

[Span A: API Gateway (Parent)] ─────────────────────────────────────────────────────────┐
    │                                                                                   │
    ├── [Span B: User Auth Service (Child)] ──────────────┐                            │
    │                                                     │                             │
    └── [Span C: Checkout Service (Child)] ───────────────┼─────────────────────────────┘
             │                                            │
             └── [Span D: SQL DB Update (Grandchild)] ────┘
```

---

## Real-World Example
A customer reports that checking out takes over 8 seconds. In a traditional setup, you would have to grep separate log files across three services. 
With Observability, you search for the checkout request's Trace ID in a visualization tool (e.g., Jaeger). The trace reveals that while the API Gateway and Auth Service took 10ms, the Checkout Service was stalled for 7.8 seconds waiting for an unindexed PostgreSQL query (`Span D: SQL DB Update`). You instantly know where to fix the code.

---

## Code Examples

### Setting up OpenTelemetry Auto-Instrumentation in Node.js
To instrument an app, you initialize OpenTelemetry *before* importing any other dependencies.

First, install the required OTel packages:
```bash
npm install @opentelemetry/api @opentelemetry/sdk-node @opentelemetry/auto-instrumentations-node @opentelemetry/exporter-trace-otlp-proto
```

Create an initialization script `instrumentation.js`:

```javascript
// instrumentation.js
import { NodeSDK } from '@opentelemetry/sdk-node';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-proto';
import { diag, DiagConsoleLogger, DiagLogLevel } from '@opentelemetry/api';

// Optional: Enable OTel internal diagnostic logging for troubleshooting
diag.setLogger(new DiagConsoleLogger(), DiagLogLevel.INFO);

// Configure the trace exporter to send data to an OTel Collector or Jaeger endpoint
const traceExporter = new OTLPTraceExporter({
  url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT || 'http://localhost:4318/v1/traces',
});

const sdk = new NodeSDK({
  traceExporter,
  instrumentations: [
    getNodeAutoInstrumentations({
      // Auto-configure common database, http, and Express packages
      '@opentelemetry/instrumentation-fs': { enabled: false }, // Avoid massive log spam from FS reads
    }),
  ],
  serviceName: 'checkout-service',
});

// Start the SDK and register clean shutdown triggers
sdk.start();
console.log('OpenTelemetry SDK initialized successfully');

process.on('SIGTERM', () => {
  sdk.shutdown()
    .then(() => console.log('OTel SDK shut down successfully'))
    .catch((err) => console.error('Error shutting down OTel SDK', err))
    .finally(() => process.exit(0));
});
```

To run your application with this instrumentation:
```bash
node --import ./instrumentation.js server.js
```

---

## Best Practices
* **Load Instrumentation First**: Always run OpenTelemetry setup scripts using `node --import` (or `require` as the absolute first line in CommonJS). If libraries like `pg` or `express` are imported before OTel, auto-instrumentation will fail to patch them.
* **Keep FS Spans Disabled**: Turn off filesystem auto-instrumentation (`instrumentation-fs`) in web apps. It generates thousands of low-value spans for every module file import, creating performance overhead and trace storage bloat.
* **Pass Context Downstream**: Ensure all outbound HTTP client requests (e.g. using `axios` or `fetch`) pass standard context headers (`traceparent`). The OTel HTTP auto-instrumentation library handles this automatically.
* **Avoid High Cardinality in Metrics**: Do not include highly unique values (like user IDs, email addresses, or timestamps) as labels/attributes in metrics. This can lead to database explosion inside monitoring metrics backends like Prometheus.

---

## Interview Questions

**Q:** What is the difference between a Trace and a Span in observability?

> **Answer:**
> A trace represents the entire end-to-end execution path of a transaction or request as it moves through a system. A span represents a single, named unit of work within that trace (e.g., an HTTP request handler execution, a database query, or a function execution). A trace is composed of a tree of nested spans.

**Q:** Why should you use structured JSON logging instead of plain text logs in production Node.js applications?

> **Answer:**
> Plain text logs are difficult for log management systems (like Elasticsearch or Grafana Loki) to parse and query dynamically. Structured JSON logs format each log entry as a clean JSON object, making it easy to index, filter, and aggregate log data by specific parameters (e.g., HTTP status code, request duration, error levels, or trace IDs) across millions of entries.

**Q:** What is context propagation in distributed tracing, and how does Node.js implement it under the hood?

> **Answer:**
> Context propagation is the process of passing trace metadata (like Trace ID and parent Span ID) across service boundaries (e.g. via HTTP headers or message queue envelopes). In Node.js, since executions are asynchronous and callback-based, OpenTelemetry relies on **AsyncLocalStorage** from the `async_hooks` module to maintain and propagate trace context across asynchronous boundaries (promises, callbacks, timers) without manually threading trace variables through every function call.

**Q:** How would you architecture a low-overhead telemetry collection pipeline for a fleet of high-throughput Node.js microservices?

> **Answer:**
> To minimize the CPU and memory overhead on the production Node.js servers:
> 1. **Local Agent / Collector Daemon**: Deploy an **OpenTelemetry Collector** as a sidecar container (in Kubernetes) or a local daemon on each virtual machine host.
> 2. **Fast Internal Protocols**: Configure the Node.js application's OTel SDK to export metrics and traces over **gRPC or HTTP/protobuf** (`otlp`) pointing directly to the local collector daemon.
> 3. **Batching and Buffering**: Configure OTel SDK exports to run asynchronously with a batch processor, buffering spans in memory and flushing them at set intervals or batch sizes, rather than sending a network request per span.
> 4. **Dynamic Sampling**: Implement trace sampling policies (e.g. 1% of successful requests and 100% of failed requests) at the SDK or collector level to reduce storage and network load without losing critical debug context.

---
Previous : [82_Load_Balancing.md](82_Load_Balancing.md) | Index : [00_index.md](00_index.md) | Next : [84_Monitoring.md](84_Monitoring.md)
