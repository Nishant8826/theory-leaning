# 📊 Tracing and APM

## 📌 Topic Name
OpenTelemetry: Distributed Tracing and APM in Jenkins

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Tracking a build visually to see exactly which steps took the most time, and identifying if a slow database or a slow API is causing the delay.
*   **Expert**: Traditional Jenkins metrics (CPU, Queue Depth) indicate *that* there is a problem, but not *where* in the pipeline the latency occurs. A Staff engineer implements **Application Performance Monitoring (APM)** using the **OpenTelemetry (OTel)** plugin. This instruments Jenkins to emit Distributed Traces (Spans). A pipeline execution becomes a distributed trace, and every `stage` and `step` becomes a child span. By exporting these to Jaeger, Honeycomb, or Datadog, you can visualize the exact critical path of a build, identify hidden bottlenecks (e.g., a slow S3 upload), and correlate pipeline execution with the performance of external backend services.

## 🏗️ Mental Model
Think of OpenTelemetry as a **GPS Tracker on a Package**.
- **Without APM**: You mail a package. 5 days later, it arrives. You know it took 5 days, but you have no idea if it got stuck in the warehouse, on the truck, or at the sorting facility.
- **With APM (Tracing)**: You attach a GPS tracker. You review the map: "Warehouse (1 day) -> Truck (3 days) -> Sorting (1 day)".
- **In Jenkins**: The package is the Pipeline. The stages are the transit points. Tracing tells you that your 20-minute build spent 18 minutes running `npm install` and 2 minutes running tests.

## ⚡ Actual Behavior
- **Span Generation**: The Jenkins OTel plugin automatically wraps the pipeline execution engine. When a stage starts, it creates a "Span" with a start time. When it ends, it closes the span.
- **Context Propagation**: OTel is powerful because it can pass the `TraceID` across boundaries. If Jenkins calls a microservice via `sh 'curl api.internal'`, it can inject the `TraceID` header. If the microservice is also instrumented with OTel, you get a single unified trace showing Jenkins calling the API, and the API querying the database!

## 🔬 Internal Mechanics (Jenkins core + OS + networking)
1.  **OTLP (OpenTelemetry Protocol)**: Jenkins exports trace data using OTLP over gRPC or HTTP to an OpenTelemetry Collector running as a sidecar or central service.
2.  **Spans and Attributes**: A Jenkins trace contains metadata (Attributes) like `jenkins.job.name`, `jenkins.build.number`, `error=true`, and the node label.
3.  **Flame Graphs**: APM tools render these nested spans as Gantt charts/Flame graphs, making parallel stage execution and blocking IO operations visually obvious.

## 🔁 Execution Flow (Pipeline Tracing)
1.  **Start Build**: Jenkins generates a `TraceID` (e.g., `a1b2c3d4`). Creates root span: `Build #42`.
2.  **Stage ('Checkout')**: Creates child span. Records start time. Runs Git clone. Records end time (5s).
3.  **Stage ('Test')**: Creates child span.
4.  **Parallel Execution**: Spawns two child spans (`Unit`, `Integration`) simultaneously.
5.  **Failure**: `Integration` step fails. Span is marked `error=true`.
6.  **Export**: The OTel plugin asynchronously sends the completed trace JSON via gRPC to the Datadog Agent or Jaeger Collector.

## 🧠 Resource Behavior (CPU, memory, IO, threads)
- **gRPC Overhead**: Sending thousands of spans per minute requires network bandwidth. Using a local OTel Collector (on the same host/network) buffers this data and reduces latency impact on the Jenkins JVM.
- **Storage Costs**: Traces are massive JSON documents. Storing 100% of traces for every Jenkins build will cost a fortune in Datadog/Splunk. **Tail-based sampling** (only keeping traces of failed or unusually slow builds) is critical.

## 📐 ASCII Diagrams (MANDATORY)
```text
[ JENKINS PIPELINE EXECUTION ]
|
+-- [ Stage: Checkout ] (5s)
|
+-- [ Stage: Parallel Tests ] (45s)
|      |
|      +-- [ Unit Tests ] (10s)
|      |
|      +-- [ Integration Tests ] (45s) <--- (Critical Path Bottleneck)
|              |
|              +-- [ sh 'curl api.dev.corp' ] (Injects TraceID: 123)
|
+-- [ Stage: Deploy ] (10s)

(Unified Trace visualized in Datadog/Jaeger)
[ JENKINS: Integration Tests ] -------------------------------->
      |
      +-- [ API DEV: GET /users ] (OTel Context Propagation) -->
                |
                +-- [ DB: SELECT * ] ------------------------> (Slow Query!)
```

## 🔍 Code (Jenkinsfile / Groovy / CLI / YAML)
```yaml
# JCasC Configuration for OpenTelemetry Plugin
unclassified:
  openTelemetry:
    authentication: "noAuthentication"
    endpoint: "http://otel-collector.monitoring.svc.cluster.local:4317" # gRPC endpoint
    exportOtelConfigurationAsEnvironmentVariables: true
    observabilityBackends:
      - jaeger:
          jaegerBaseUrl: "https://jaeger.corp.com"
          name: "Jaeger"
```

## 💥 Production Failures
1.  **The Invisible Bottleneck**: A build takes 40 minutes. The logs just show tests running. Without APM, engineers spend weeks optimizing the code. OTel tracing reveals that 30 minutes of the build is spent *waiting in the Jenkins queue* for an executor. The code is fine; the infrastructure is lacking.
2.  **Collector Saturation**: Jenkins is configured to send traces directly to a SaaS APM provider over the public internet. The internet connection drops. The Jenkins OTel plugin buffers traces in JVM memory until the heap hits 100% and crashes Jenkins. **Solution**: Always send to a local OTel Collector that handles disk-buffering and retries.

## 🧪 Real-time Q&A
*   **Q**: Can OTel track script execution inside a Shared Library?
*   **A**: Yes, the plugin intercepts pipeline step execution. If your shared library calls `sh` or `sleep`, those will appear as child spans. You can also manually create custom spans in Groovy using the OpenTelemetry API.
*   **Q**: How is this different from Blue Ocean?
*   **A**: Blue Ocean is a UI that reads the pipeline AST from Jenkins' local disk. It cannot correlate Jenkins events with external systems (like a database query). OTel exports the data to enterprise monitoring tools.

## ⚠️ Edge Cases
*   **Clock Skew**: If the Jenkins Controller's NTP clock is 5 seconds out of sync with the Agent's clock, the distributed trace will look broken (e.g., a child step appearing to finish *before* the parent stage started). NTP synchronization is strictly required for tracing.

## 🏢 Best Practices
1.  **Use an OTel Collector**: Never point Jenkins directly at a SaaS provider (Datadog/NewRelic). Point Jenkins at an OpenTelemetry Collector deployed in your infrastructure. Let the collector handle API keys, batching, and sampling.
2.  **Correlate Logs and Traces**: Ensure the Jenkins Log Aggregation injects the `TraceID` into the JSON logs. This allows you to click a slow span in Jaeger and instantly see the Jenkins logs for that exact step.
3.  **Trace External Calls**: If your pipeline deploys to Kubernetes, pass the `TraceID` into the K8s deployment annotations so you can trace the lifecycle from "Code Merge" all the way to "Pod Running".

## ⚖️ Trade-offs
*   **Visibility vs Complexity**: APM provides incredible, granular visibility into pipeline performance, but requires maintaining a complex distributed tracing infrastructure and managing high data-ingestion costs.

## 💼 Interview Q&A
*   **Q**: Developers complain a specific pipeline is "slow." You look at the history, and indeed, it grew from 5 minutes to 25 minutes over the last month. How would you use OpenTelemetry to diagnose this without reading 10,000 lines of logs?
*   **A**: I would open our APM tool (e.g., Datadog or Jaeger) and look at a recent trace (Flame Graph) for this pipeline. The trace visually breaks down the execution time of every stage and step. I would look for the longest horizontal span on the critical path. It might reveal that the `npm install` span grew from 1 minute to 20 minutes, indicating a cache failure or network issue, instantly narrowing down the root cause without touching the raw logs.

## 🧩 Practice Problems
1.  Research "OpenTelemetry Context Propagation". Understand how the `traceparent` HTTP header allows Jenkins to link its trace with a downstream API service.
2.  Identify the difference between a Trace, a Span, and a Span Attribute.
