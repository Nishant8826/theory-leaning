# 📌 Topic: Metrics and Monitoring

## What
### 🧠 Concept Explanation
Metrics are the numerical representation of your system's health and performance over time. While logs tell you *what* happened, metrics tell you *how much* is happening and how well the system is handling it.

**The Hospital Vital Signs Analogy (Deep Dive):**
Imagine a patient in the Intensive Care Unit (Your Production Server).
*   **The Log:** A nurse writes a note: "Patient complained of thirst at 2:00 PM." This is an **Event**.
*   **The Metric:** The heart rate monitor (The Vital Signs). It doesn't write a note for every heartbeat; it just shows a number: **72 BPM**.
    *   **Real-time:** You can look at the monitor and instantly know if the patient is stable.
    *   **Trends:** You can look at a chart from the last 24 hours to see if the heart rate is slowly increasing (A Memory Leak).
    *   **Alerts:** If the heart rate hits 0, the monitor screams. This is an **Alert**.
*   **The Metric Types:**
    *   **Counter (The Odometer):** Counts total requests. It only ever goes up.
    *   **Gauge (The Speedometer):** Shows current CPU usage. It goes up and down.
    *   **Histogram (The Delivery Stats):** Shows how many requests took <10ms, <100ms, etc.

---

### 🏗️ Mental Model
Think of Monitoring as a **Feedback Loop**.
1.  **Instrumentation:** You add code to your app to track specific numbers (e.g., `requests.inc()`).
2.  **Aggregation:** The monitoring system collects these numbers from all your servers.
3.  **Visualization:** You turn those numbers into beautiful, readable graphs (Grafana).
4.  **Alerting:** You define rules: "If the red line (Errors) goes above the blue line (Requests), send me a Slack message."

---

## Why
### 🏢 Best Practices
1.  **Monitor everything:** CPU, RAM, Event Loop Lag, GC Duration, and active handles.
2.  **Standardize Labels:** Use the same label names across all your microservices (e.g., `service_name`, `env`).
3.  **Set meaningful Alerts:** Don't alert on "CPU > 80%." Alert on "Error Rate > 5%" or "P99 Latency > 1s."

---

### ⚖️ Trade-offs
*   **Prometheus (Pull):** Easier to manage, auto-discovery works well.
*   **StatsD (Push):** Better for serverless (Lambda) where the process might not be alive for a scrape.

---

## How
### ⚡ Actual Behavior
In a Node.js monitoring setup:
1.  **The Registry:** The `prom-client` library maintains a "Registry" in the Node.js process memory. This is basically a fast, thread-safe object that holds all your current counters and gauges.
2.  **Zero-Latency Tracking:** When you increment a counter, you are just adding `1` to a number in RAM. This takes less than 1 nanosecond. It does **not** make a network call to the monitoring server.
3.  **The Scrape:** Every 15 seconds, the Prometheus server makes an HTTP request to your app at `GET /metrics`. Your app responds with a text-based list of all current numbers.
4.  **Labeling:** Metrics use "Labels" (e.g., `http_requests_total{method="POST", status="200"}`). This allows you to "Slice and Dice" the data later. You can view "Total Requests" or filter for only "POST requests that resulted in a 200."

---

### 🔬 Internal Mechanics (V8 + libuv + OS)
*   **System-Level Metrics:** `prom-client` hooks into Node.js internal C++ bindings to expose details you can't normally see:
    *   **Heap Statistics:** Total available, used, and "External" memory (memory used by C++ objects outside the V8 heap).
    *   **GC Statistics:** How many milliseconds the process spent paused for Garbage Collection in the last minute.
    *   **Event Loop Delay:** The delay between when a timer was scheduled and when it fired.
    *   **Active Handles/Requests:** The count of open TCP sockets, file handles, and pending asynchronous operations. 
*   **Histogram Buckets:** Histograms are expensive. To save memory, they don't store every single response time. They have "Buckets" (e.g., 0.1s, 0.5s, 1s). If a request takes 0.3s, it's counted in the "0.5s" bucket. Choosing the right buckets is critical for accurate P99 latency.
*   **The Scrape Cost:** Since the `/metrics` endpoint is an HTTP route, it's subject to the same event loop rules as your API. If your server is completely frozen by a CPU-heavy task, Prometheus won't be able to scrape it. This "Gap" in the graph is itself a powerful signal that the server is overwhelmed.
*   **Cardinality:** Each unique combination of labels creates a "Time Series" in the monitoring database. If you add `userId` as a label, and you have 1 million users, you have just created 1 million time series. This is "High Cardinality" and it is the #1 way to crash a monitoring system.

---

### 🔁 Execution Flow
1.  Application starts and initializes `prom-client`.
2.  Middleware increments a counter on every request: `requestCount.inc({ method: 'GET' })`.
3.  Prometheus server calls `GET /metrics`.
4.  App responds with a plain-text list of metrics: `http_requests_total{method="GET"} 4501`.
5.  Prometheus stores the number and timestamp.
6.  **Grafana** queries Prometheus and draws a line graph.

---

### 🔍 Code Example (Latest Node.js - Using `prom-client`)
```javascript
import client from 'prom-client';
import express from 'express';

const app = express();

// 1. Collect default metrics (CPU, RAM, Event Loop)
client.collectDefaultMetrics();

// 2. Custom metric for HTTP requests
const httpRequestDurationMicroseconds = new client.Histogram({
  name: 'http_request_duration_ms',
  help: 'Duration of HTTP requests in ms',
  labelNames: ['method', 'route', 'status_code'],
  buckets: [0.1, 5, 15, 50, 100, 500]
});

app.use((req, res, next) => {
  const end = httpRequestDurationMicroseconds.startTimer();
  res.on('finish', () => {
    end({ method: req.method, route: req.path, status_code: res.statusCode });
  });
  next();
});

// 3. Expose the metrics endpoint
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', client.register.contentType);
  res.end(await client.register.metrics());
});
```

---

## Impact
### 💥 Production Failures
*   **Metric Cardinality Explosion:** Adding a label that has thousands of unique values (like `userId` or `ipAddress`). Prometheus will crash trying to store a separate timeline for every single user. (Solution: Never use high-cardinality data as a label).
*   **Blocking on Metrics:** Doing a heavy database calculation inside the `/metrics` endpoint. The scraping process will time out or slow down the app.

---

### 🧪 Real-time Scenarios
*   **Detecting a Memory Leak:** Seeing the `nodejs_heap_size_used_bytes` graph go up steadily for 24 hours without dropping.
*   **Identifying "Error Spikes":** Seeing a sudden vertical line in your `error_count` graph after a new deployment, allowing you to Rollback immediately.

---

### ⚠️ Edge Cases
*   **Ghost Instances:** If a server crashes and doesn't shut down gracefully, Prometheus might still show its last reported values, making it look "stuck."
*   **Timeouts:** If the server is 100% CPU-busy, it might not respond to the scrape request, leading to "Gaps" in your monitoring data.

---

---

Prev: [01_Logging_Strategies.md](./01_Logging_Strategies.md) | Index: [NodeJS/00_Index.md](../00_Index.md) | Next: [03_Distributed_Tracing.md](./03_Distributed_Tracing.md)
