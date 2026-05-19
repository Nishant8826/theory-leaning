# Monitoring

## Why This Exists
When you have 50 microservices running across 20 servers, you cannot just log into a server and type `top` to see if things are running. You need a centralized dashboard that constantly watches the system's heartbeat, records historical data, and alerts you *before* a small issue becomes a massive outage.

## Real World Analogy
Think of driving a car and looking at the **Dashboard**. 
You don't open the hood while driving on the highway to check the engine temperature. You look at the dials on your dashboard (**Grafana**) which are connected to sensors inside the engine (**Prometheus**). If the fuel gets dangerously low, a red light turns on and the car beeps at you (**Alertmanager**).

## Core Concepts
*   **Metrics:** Numbers measured over time (e.g., CPU %, Memory MBs, HTTP Error Rate, Active Users).
*   **Time-Series Database (Prometheus):** A specialized database designed purely to store metrics stamped with a specific time.
*   **Dashboards (Grafana):** The beautiful graphs, pie charts, and gauges that make raw metrics readable by humans.
*   **Alerting:** Rules that trigger notifications (Slack, PagerDuty, Email) when a metric crosses a dangerous threshold.

## Architecture / Flow
1. Your Application exposes a `/metrics` web endpoint showing its current stats.
2. **Prometheus** scrapes (pulls) data from that endpoint every 15 seconds and saves it to its database.
3. A Developer opens **Grafana** in their browser.
4. Grafana queries Prometheus and draws a graph showing CPU usage over the last 24 hours.
5. If Error Rate > 5%, Prometheus tells **Alertmanager**, which sends an automated Slack message to the engineering team.

## Practical Commands
*   `kubectl top pods` - Built-in command to see current CPU/Memory of pods (requires Metrics Server).
*   `kubectl top nodes` - See resource usage of your physical servers.
*   *(Monitoring is usually GUI-based, not CLI-based, so you spend most of your time in the Grafana UI).*

## Hands-On Exercise
Install the `kube-prometheus-stack` using Helm. Use `kubectl port-forward` to access the Grafana service on `localhost:3000`. Browse the default K8s dashboards and locate the graph showing the memory usage of your specific node.

## Mini Project
**"Custom App Metrics"**
Take a simple Node.js or Python API. Install a Prometheus client library. Create a custom metric called `items_purchased_total`. Every time someone hits the `/buy` endpoint, increment the counter. Connect Prometheus to it, and build a Grafana dashboard showing sales per minute!

## Real Production Usage
Companies have entire teams (Site Reliability Engineers / SREs) dedicated to this. They follow standards like "The RED Method" (Rate, Errors, Duration) to monitor every single microservice, ensuring they know about an outage before a customer even notices it.

## Common Mistakes
*   **Alert Fatigue:** Creating so many useless, minor alerts that developers start ignoring the alerting channel. Eventually, they ignore a critical database failure because they thought it was just another false alarm.
*   **Only Monitoring Infrastructure:** CPU and RAM graphs are nice, but if the CPU is 10%, yet every user is getting a "500 Internal Server Error", your app is still broken. You must monitor application-level metrics.

## Debugging Guide
*   **Grafana shows "No Data"?** Go to the Prometheus UI and check the "Targets" page. This will tell you if Prometheus is successfully reaching your app's `/metrics` endpoint, or if it's being blocked by a firewall or bad port configuration.

## Best Practices
*   **Monitor from the User's Perspective:** A high CPU isn't always bad (it just means the server is working hard). A high API response time (latency) is *always* bad because it directly frustrates the user. Measure what matters.
*   **Treat Dashboards as Code:** Export your Grafana dashboards as JSON files and save them in Git. If the cluster dies, you can recreate all your beautiful graphs instantly.

## Interview Questions
*   **Q: How does Prometheus collect metrics from applications?**
    *   *A: It uses a "Pull" model. Prometheus is configured with a list of targets, and it actively makes HTTP GET requests to their `/metrics` endpoints at regular intervals to scrape the data.*
*   **Q: What is the difference between Logging and Monitoring?**
    *   *A: Monitoring handles numbers/metrics over time (CPU went from 10% to 90%). Logging handles discrete events/text (User X failed to login at 2:00 PM).*

## Summary
A production system without monitoring is like flying an airplane blindfolded. Monitoring tools like Prometheus and Grafana turn an opaque cluster of servers into a transparent, measurable system where decisions are made based on data.

---
Prev: [05_autoscaling.md](./05_autoscaling.md) | Index: [Index](../00_index.md) | Next: [07_logging.md](./07_logging.md)
