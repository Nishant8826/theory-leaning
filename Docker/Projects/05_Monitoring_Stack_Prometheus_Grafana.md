# 📌 Project: Full Observability Stack (Prometheus, Grafana, Loki)

## 🏗️ Project Overview
"If you can't measure it, you can't improve it." In this final project, we build a **Complete Observability Stack**. We will monitor our Docker containers at three levels: **Metrics** (numbers like CPU/RAM), **Logs** (text events), and **Tracing** (the path of a request through microservices). This project integrates Monitoring, Logging, and Performance modules into one unified dashboard.

## 📐 Architecture Diagram

```text
   [ CONTAINERS ] ----( Metrics )----> [ PROMETHEUS ]
         |                                   |
    ( Stdout Logs )                     ( Visualize )
         |                                   |
    [ PROMTAIL ] -----( Push )-------> [ LOKI ] <--- [ GRAFANA ]
         |                                              ^
    ( Tracing )                                         |
         |                                              |
    [ JAEGER ] -----------------------------------------+
```

## 🛠️ Step 1: Metrics Collection (Prometheus)
Prometheus "pulls" metrics from your containers every 15 seconds.
```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'docker-containers'
    static_configs:
      - targets: ['cadvisor:8080'] # cAdvisor extracts metrics from Docker

  - job_name: 'node-api'
    static_configs:
      - targets: ['api:3000']
```

## ⛓️ Step 2: Log Aggregation (Loki)
Instead of `docker logs`, which only works for one container, Loki collects logs from ALL containers into one searchable database.
```yaml
# promtail-config.yml
scrape_configs:
- job_name: system
  static_configs:
  - targets: [localhost]
    labels:
      job: docker-logs
      __path__: /var/lib/docker/containers/*/*.log
```

## ⛓️ Step 3: The Dashboard (Grafana)
Grafana connects to Prometheus and Loki to show you the "Big Picture."
1. **CPU/RAM Panels**: "Which container is eating all the memory?"
2. **Error Rate Panels**: "Did my 5xx errors spike after the last deployment?"
3. **Log Explorer**: "Show me all 'ERROR' logs for the 'Payments' service in the last 10 minutes."

## 🔬 Internal Mechanics (The "Golden Signals")
Staff-level engineers monitor the **Four Golden Signals**:
1. **Latency**: Time it takes to service a request.
2. **Traffic**: Demand placed on the system (Requests/sec).
3. **Errors**: The rate of requests that fail.
4. **Saturation**: How "full" your service is (e.g., CPU is at 95%).

## 💥 Production Failures & Fixes
- **Failure**: Prometheus fills up the disk with 1TB of metrics data.
  *Fix*: Set a **Retention Policy** (e.g., `--storage.tsdb.retention.time=15d`) and use **Downsampling**.
- **Failure**: Monitoring is slow. Grafana takes 30 seconds to load a dashboard.
  *Fix*: Use **Recording Rules** in Prometheus to pre-calculate complex queries.

## 💼 Interview Q&A
**Q: What is the difference between Logs, Metrics, and Tracing?**
**A**: **Metrics** are numerical data (integers/floats) over time; they are great for alerting (e.g., "CPU > 90%"). **Logs** are discrete text events; they are essential for debugging the *why* after an alert (e.g., "NullPointerException in user.js"). **Tracing** tracks a single request as it travels across multiple microservices; it is critical for finding bottlenecks in complex distributed systems (e.g., "The request spent 200ms in the Auth service and only 5ms in the API").

## 🧪 Lab Exercise
1. Deploy the stack using the provided `docker-compose.yml`.
2. Open Grafana (`localhost:3000`) and add Prometheus as a Data Source.
3. Create a Graph showing the RAM usage of your API container.
4. Intentionally crash your API and see the "Error Rate" spike on your dashboard.

---
Prev: [04_CI_CD_with_Jenkins_and_ECR.md](./04_CI_CD_with_Jenkins_and_ECR.md) | Index: [00_Index.md](../00_Index.md) | Next: [FINISH]
---
