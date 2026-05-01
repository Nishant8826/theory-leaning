# 📌 Topic: Distributed Tracing

## What
### 🧠 Concept Explanation
Distributed Tracing is a method used to profile and monitor applications, especially those built using a microservices architecture. It allows you to see the "Full Story" of a request as it travels across different servers, databases, and third-party APIs.

**The GPS Package Tracker Analogy (Deep Dive):**
Imagine you order a custom pizza from a chain that has separate locations for Dough, Toppings, and Baking.
*   **Without Tracing (Individual Logs):** You have a camera at the Dough shop. It says "Dough ready at 5:00." You have a camera at the Topping shop. It says "Toppings added at 5:15." 
    *   **The Problem:** If the pizza takes 2 hours, which shop was slow? You have no way to link these two logs together because 1,000 pizzas were made that day.
*   **With Distributed Tracing (The GPS Tracker):** As soon as you place the order, the system attaches a **Trace ID** (a unique tracker) to your pizza.
    *   **The Journey:** You can see exactly when the dough was tossed (Span 1), how long it took to drive to the next shop (Network Latency), when the pepperoni was placed (Span 2), and how long it sat in the oven (Span 3).
    *   **The Root Cause:** If the pizza is late, you can see that the "Oven" stage took 90 minutes instead of 10. You don't just know it's late; you know *why* and *where*.

---

### 🏗️ Mental Model
Think of a Trace as a **Tree of Spans**.
*   **The Trace (The Tree):** The entire request/response lifecycle.
*   **The Span (The Branch):** A single unit of work. Every database query is a span. Every outgoing HTTP call is a span. Even a heavy CPU function can be a span.
*   **Context (The Sap):** For the tree to grow, "Context" (the Trace ID) must flow through every branch. If one branch doesn't get the Trace ID, it becomes a "disconnected" orphan and you lose visibility.

---

## Why
### 🏢 Best Practices
1.  **Use OpenTelemetry:** It is the industry standard and vendor-neutral.
2.  **Instrument at the Boundaries:** Focus on HTTP calls, DB queries, and Message Queues.
3.  **Add Metadata:** Add `userId`, `planType`, or `region` to spans as "Attributes" to help filter traces.
4.  **Sampling Policy:** Start with 1% and increase it if you need more data.

---

### ⚖️ Trade-offs
*   **Distributed Tracing:** Unbeatable for debugging microservices, but adds complexity and costs money/bandwidth to store the data.

---

## How
### ⚡ Actual Behavior
In a production Node.js environment:
1.  **Incoming Request:** Your API Gateway receives a request. It checks for a `traceparent` header. If missing, it creates a new `TraceID`.
2.  **Propagation:** As Node.js makes a call to the "User Service," the OpenTelemetry library automatically injects the `TraceID` into the outgoing HTTP headers.
3.  **Asynchronous Context:** Because Node.js is asynchronous, you might be handling 100 requests at the same time. Node.js must ensure that when an "Order DB Query" finishes, it knows which `TraceID` it belongs to.
4.  **Exporting:** Spans are not sent to the collector one by one (too much overhead). They are "Batched" in memory and sent every few seconds via a non-blocking background process.

---

### 🔬 Internal Mechanics (V8 + libuv + OS)
*   **`AsyncLocalStorage` (The Magic):** This is the core Node.js API that makes tracing possible. It works like a "Thread-Local Storage" but for asynchronous callbacks. It allows you to store a `TraceID` at the start of a request and access it anywhere in the code—even 50 levels deep in nested promises—without ever passing it as a function argument.
*   **Monkey Patching:** Most tracing libraries "Monkey Patch" (wrap) core Node.js modules like `http`, `https`, and `net`. When you call `http.get()`, you are actually calling a wrapped version that starts a span, attaches the Trace ID, and then calls the real `http.get()`.
*   **Sampling Algorithms:** Tracing every single request is expensive. 
    *   **Head-based Sampling:** The first service decides (e.g., 10% of traffic) to trace or not.
    *   **Tail-based Sampling:** All services trace everything, but a "Collector" only keeps the ones that were slow or had errors. This is much more powerful but harder to set up.
*   **Overhead:** Every span adds a few bytes to the heap and a few microseconds of CPU time. In an extreme case (e.g., creating 10,000 spans for a single request), this can lead to memory pressure and increased GC frequency. Professional tracing is designed to have `< 1%` performance impact.

---

### 🔁 Execution Flow
1.  **Gateway:** Receives a request. Generates `TraceID: 123`. Starts `Span: Gateway-Main`.
2.  **Gateway:** Calls Order Service. Adds `traceparent: 123` to the headers.
3.  **Order Service:** Receives request. Sees `TraceID: 123`. Starts `Span: Order-Process` as a child of `Gateway-Main`.
4.  **Order Service:** Queries DB. Starts `Span: DB-Query`.
5.  **Collector:** Receives all these spans and "stitches" them together into a timeline.

---

### 🔍 Code Example (Latest Node.js - OpenTelemetry)
```javascript
// instrumentation.js
import { NodeSDK } from '@opentelemetry/sdk-node';
import { HttpInstrumentation } from '@opentelemetry/instrumentation-http';
import { ExpressInstrumentation } from '@opentelemetry/instrumentation-express';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';

const sdk = new NodeSDK({
  traceExporter: new OTLPTraceExporter({ url: 'http://jaeger:4318/v1/traces' }),
  instrumentations: [new HttpInstrumentation(), new ExpressInstrumentation()],
});

sdk.start();
```

---

## Impact
### 💥 Production Failures
*   **Broken Context:** Forgetting to pass the trace header to a background worker or a message queue, causing the trace to "die" and a new, unrelated trace to start in the next service.
*   **Span Overload:** Creating a new span for every single variable assignment or small function, creating massive trace files that are impossible to read.

---

### 🧪 Real-time Scenarios
*   **Identifying "The Slow Service":** A user says the site is slow. You look at their trace and see that the "Inventory Service" took 90% of the total time.
*   **Debugging 500 Errors:** Seeing exactly which internal DB query failed in a chain of 10 microservice calls.

---

### ⚠️ Edge Cases
*   **Clock Skew:** If Service A and Service B have different system times, the spans might look like they overlap or happen in the wrong order. (Solution: Use NTP to sync clocks).
*   **Long-running spans:** If a span lasts 24 hours (e.g., a background job), it won't be visible in most tools until it finishes.

---

---

Prev: [02_Metrics_and_Monitoring.md](./02_Metrics_and_Monitoring.md) | Index: [NodeJS/00_Index.md](../00_Index.md) | Next: [04_Debugging_Production.md](./04_Debugging_Production.md)
