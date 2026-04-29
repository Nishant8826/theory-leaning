# 📊 Controller Metrics

## 📌 Topic Name
Jenkins Observability: Controller Metrics and JMX

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Keeping an eye on how much CPU and RAM the Jenkins server is using so it doesn't crash.
*   **Expert**: The Jenkins Controller is a highly concurrent, memory-intensive Java application. Standard OS-level metrics (CPU/RAM) are insufficient for diagnosing performance degradation. A Staff engineer relies on **JMX (Java Management Extensions)** and the **Metrics Plugin** (Dropwizard) to expose internal JVM telemetry. This includes Garbage Collection (GC) pauses, Executor Queue Depth, HTTP active requests, and CPS engine heap utilization. These metrics must be scraped via Prometheus and visualized in Grafana to establish baselines and trigger proactive alerts before an OutOfMemoryError (OOM) occurs.

## 🏗️ Mental Model
Think of observing Jenkins like **Monitoring a Car Engine**.
- **OS Metrics (The Dashboard)**: Speedometer and Fuel Gauge. Tells you the car is moving and has gas.
- **JMX Metrics (The OBD-II Scanner)**: Plugs directly into the engine's computer. Tells you the exact fuel injection timing, the temperature of cylinder 3, and the transmission fluid pressure.
- If the car is shuddering, the speedometer won't tell you why. You need the deep engine metrics.

## ⚡ Actual Behavior
- **The Metrics Plugin**: Acts as a registry. Jenkins core and plugins register their internal counters (e.g., `jenkins.queue.size.value`) with this plugin.
- **Prometheus Exporter**: The Prometheus plugin creates a `/prometheus` HTTP endpoint. A Prometheus server scrapes this endpoint every 15 seconds, translating the Dropwizard metrics into time-series data.

## 🔬 Internal Mechanics (Jenkins core + OS + networking)
1.  **JVM Heap Regions**: Metrics expose Eden Space, Survivor Space, and Tenured (Old) Gen. Monitoring the Old Gen growth rate is critical; if it hits 100% and a Full GC cannot clear it, the JVM crashes.
2.  **Thread States**: Jenkins exposes the number of threads in `RUNNABLE`, `BLOCKED`, and `WAITING` states. A sudden spike in `BLOCKED` threads usually indicates a deadlock in a plugin or massive disk I/O contention.
3.  **HTTP Active Requests**: Tracks how many users/API calls are hitting the Jetty web server. Spikes here correlate with SCM Polling storms or DDOS attacks.

## 🔁 Execution Flow (Metrics Scraping)
1.  **Metric Generation**: Jenkins Queue adds an item. Code calls `queueCounter.inc()`.
2.  **Scrape Interval**: Every 15s, Prometheus sends `HTTP GET /prometheus` to Jenkins.
3.  **Translation**: Plugin iterates through all Dropwizard metrics, formats them as plaintext Prometheus format.
4.  **Ingestion**: Prometheus stores the time-series data.
5.  **Alerting**: PromQL query `jenkins_queue_size > 100` evaluates to true.
6.  **Action**: Alertmanager pages the DevOps team via PagerDuty.

## 🧠 Resource Behavior (CPU, memory, IO, threads)
- **Observer Effect**: The act of scraping metrics consumes CPU. Scraping 10,000 metrics every 1 second will severely degrade Jenkins web performance. 15-30 second intervals are standard.
- **GC Pauses**: If the JVM executes a Full GC, the entire Jenkins application (including the `/prometheus` endpoint) freezes. Prometheus will record a "Target Down" or timeout error.

## 📐 ASCII Diagrams (MANDATORY)
```text
[ JENKINS CONTROLLER JVM ]
    |
    |-- [ Metrics Plugin ] (Aggregates internal counters)
    |-- [ Prometheus Plugin ] (Exposes /prometheus HTTP endpoint)
           ^
           | (HTTP GET every 15s)
           |
[ PROMETHEUS SERVER ] ---> (Stores Time-Series Data)
           |
           v
[ GRAFANA DASHBOARD ] ---> [ ALERTMANAGER ] ---> (PagerDuty)
(Visualizes Heap, Queue, Threads)
```

## 🔍 Code (Jenkinsfile / Groovy / CLI / YAML)
```yaml
# PromQL Queries for Grafana Alerts

# Alert if the Queue has been backed up for more than 5 minutes
# Indicates a lack of agents or a stuck scheduler
jenkins_queue_size_value > 50 
  for: 5m

# Alert if JVM Old Generation heap is over 90%
# Indicates an impending OutOfMemoryError crash
jvm_memory_pool_bytes_used{pool="G1 Old Gen"} / jvm_memory_pool_bytes_max{pool="G1 Old Gen"} > 0.90

# Alert if Jenkins is experiencing long "Stop-The-World" Garbage Collection pauses
rate(jvm_gc_collection_seconds_sum[5m]) > 1.0
```

## 💥 Production Failures
1.  **The Silent OOM**: Jenkins crashes. The OS metrics show memory was at 50% just before the crash. The team is confused. Without JMX metrics, they didn't see that the *JVM Heap* was at 100%, even though the OS had plenty of RAM left over.
2.  **Thread Exhaustion**: The Jenkins UI stops loading for everyone. CPU is low, RAM is low. Metrics show 500 Jetty threads in the `BLOCKED` state. Investigation reveals a bad plugin is trying to write to a locked file on a slow NFS mount.
3.  **Queue Blindness**: Developers complain builds are taking forever. The Jenkins UI looks fine. Metrics show that while the Controller is healthy, the `jenkins.queue.pending` metric has been hovering at 200 for hours because the Kubernetes cluster is out of IP addresses and cannot spawn new agents.

## 🧪 Real-time Q&A
*   **Q**: Can I see these metrics without Prometheus?
*   **A**: Yes, the Metrics Plugin provides a `/metrics/<token>/ping` and `/metrics/<token>/healthcheck` JSON endpoint you can hit directly with `curl` or browser.
*   **Q**: What is a "Health Check" metric in Jenkins?
*   **A**: Plugins can register boolean health checks. For example, "Can I write to disk?" or "Is the database reachable?" If any check returns false, the `/healthcheck` endpoint returns an HTTP 500, which can be used by an AWS Load Balancer to failover.

## ⚠️ Edge Cases
*   **Plugin Metric Leaks**: Poorly written plugins might register a new metric tag for every single build number (e.g., `build_duration{id="1"}`, `build_duration{id="2"}`). This is called **Cardinality Explosion** and will instantly crash your Prometheus server by generating millions of unique time series.

## 🏢 Best Practices
1.  **Monitor the Queue**: The most critical business metric is Queue Depth and Queue Wait Time. It directly translates to developer frustration.
2.  **Alert on GC Pauses**: Alert if GC pauses exceed 2 seconds. A JVM spending all its time doing Garbage Collection is not doing any actual CI/CD work.
3.  **Four Golden Signals**: Always monitor Latency, Traffic, Errors, and Saturation for the Jenkins web UI.

## ⚖️ Trade-offs
*   **Pull (Prometheus) vs Push (Datadog/StatsD)**: Prometheus pulls metrics via HTTP, which fails if Jenkins freezes (GC pause). Push agents send metrics asynchronously, which can be more resilient to application lockups but require managing sidecar agents.

## 💼 Interview Q&A
*   **Q**: Your Jenkins server crashed with an `OutOfMemoryError`. How would you use metrics to determine if the crash was caused by a sudden spike (like a user loading a 1GB file) or a slow memory leak over several weeks?
*   **A**: I would look at the Grafana dashboard for JVM Heap utilization, specifically the "Old Gen" memory pool, over a 30-day window. If the graph looks like a "sawtooth" that resets to a baseline, but that baseline slowly creeps upward week over week until it hits 100%, it's a slow memory leak (often caused by lingering Jenkins objects in the CPS engine). If the baseline was flat at 30%, and it spiked vertically to 100% in 2 minutes, it was an acute event, like a massive XML payload or a giant Groovy string allocation.

## 🧩 Practice Problems
1.  Install the Metrics Plugin. Go to `<jenkins_url>/metrics/currentUser/metrics` in your browser and inspect the raw JSON output of the JVM counters.
2.  Write a PromQL query that calculates the percentage of Jenkins HTTP requests that return a 5xx Error code.
