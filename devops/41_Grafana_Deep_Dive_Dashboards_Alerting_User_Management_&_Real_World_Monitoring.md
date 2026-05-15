# 41 – Grafana Deep Dive: Dashboards, Alerting, User Management & Real-World Monitoring

---

## Table of Contents

1. [Namespace Isolation for Monitoring](#1-namespace-isolation-for-monitoring)
2. [Grafana Configuration & User Management](#2-grafana-configuration--user-management)
3. [Data Sources – Connecting Grafana to Everything](#3-data-sources--connecting-grafana-to-everything)
4. [Scrape Interval & Timeout Settings](#4-scrape-interval--timeout-settings)
5. [Dashboard Management – 25,000+ Dashboards](#5-dashboard-management--25000-dashboards)
6. [The 5 Core Dashboard Types DevOps Must Know](#6-the-5-core-dashboard-types-devops-must-know)
7. [Troubleshooting – When Data Shows "NA"](#7-troubleshooting--when-data-shows-na)
8. [Grafana Alerting – Complete Setup](#8-grafana-alerting--complete-setup)
9. [Silence Periods – Suppressing Alerts During Maintenance](#9-silence-periods--suppressing-alerts-during-maintenance)
10. [Real-World Applications of Grafana](#10-real-world-applications-of-grafana)
11. [DevOps Role in Monitoring vs L1/L2 Teams](#11-devops-role-in-monitoring-vs-l1l2-teams)
12. [Tech Stack Mapping](#12-tech-stack-mapping)
13. [Visual Diagrams](#13-visual-diagrams)
14. [Code & Practical Examples](#14-code--practical-examples)
15. [Scenario-Based Q&A](#15-scenario-based-qa)
16. [Interview Q&A](#16-interview-qa)

---

## 1. Namespace Isolation for Monitoring

### What
Running monitoring tools (Prometheus, Grafana, AlertManager) in a **dedicated `monitoring` namespace** — completely separate from your application namespaces (`production`, `staging`, `development`).

### Why — The Critical Reason

> 💡 **Key principle:** If your application has a problem, monitoring should still work. If monitoring has a problem, your application should still work.

```
Without namespace isolation:
  monitoring + apps share the same namespace
  
  Scenario: Monitoring consumes all node CPU
  → Application pods get throttled
  → Users experience slowness
  → Monitoring caused the problem it was meant to prevent ❌

  Scenario: Someone accidentally deletes namespace
  → Both monitoring AND apps disappear together ❌

With namespace isolation (monitoring namespace):
  Monitoring namespace: prometheus, grafana, alertmanager
  Production namespace: your-api, your-frontend, your-db
  
  Monitoring pod issue → Apps unaffected ✅
  App pod issue → Monitoring unaffected ✅
  ResourceQuota per namespace → monitoring can't starve apps ✅
```

### Additional Isolation Benefits

| Benefit | Without Isolation | With Monitoring Namespace |
|---------|------------------|--------------------------|
| RBAC | Anyone with cluster access sees monitoring | Only DevOps team accesses monitoring namespace |
| Resource limits | Monitoring competes with apps | Separate quota for monitoring resources |
| `kubectl get pods` | Noisy — monitoring + app pods mixed | Clean — `-n production` shows only app pods |
| Accidental deletion risk | High — one `kubectl delete ns default` | Lower — separate namespaces, separate risks |
| Security | Prometheus can scrape credentials | Restricted by NetworkPolicy |

---

## 2. Grafana Configuration & User Management

### Accessing Grafana

```bash
# Get external IP
kubectl get svc prometheus-grafana -n monitoring

# Access at:
http://EXTERNAL_IP:3000

# Default credentials (change immediately in production!)
Username: admin
Password: prom-operator  ← retrieved from Kubernetes secret
```

### Changing the Theme

```
Grafana UI:
  Top right → Profile icon → Preferences
  → UI Theme: Default (Dark) / Light / System default
  
  Class used: Light (white) for better visibility during demo
  Production: Dark is easier on eyes for long monitoring sessions
```

### User Management

Grafana has its own user system — completely separate from Kubernetes users.

#### Creating a New User (Admin only)

```
Grafana UI:
  Left sidebar → Administration → Users → New user
  
  Fill in:
    Name: Aman Sharma
    Email: aman@company.com
    Username: aman
    Password: (set initial password)
    Role: Viewer / Editor / Admin
  
  Click: Create user
```

#### The Three Grafana Roles

| Role | What They Can Do |
|------|----------------|
| **Viewer** | View dashboards only — cannot edit, create, or delete | 
| **Editor** | Create and edit dashboards, manage data sources |
| **Admin** | Full control — manage users, organizations, system settings |

#### Real-World Role Assignment

```
DevOps Team Lead:          Admin    (manages infrastructure, users, alerts)
DevOps Engineers:          Editor   (create custom dashboards, modify alerts)
L1/L2 Support:             Viewer   (monitor dashboards, raise incidents)
Developers:                Viewer   (view application-level dashboards)
Management:                Viewer   (high-level business dashboards)
```

> 💡 From class: "Aman from the L2 team" gets **Viewer** role — they can see dashboards and monitor for problems, but cannot modify the monitoring configuration. This is the correct production security model.

### Organization Management

Grafana supports multiple **Organizations** within one instance — like having separate tenants. Each org has its own dashboards, users, and data sources. Used when:
- Multiple business units share one Grafana (but shouldn't see each other's data)
- Multi-tenant SaaS product monitoring

---

## 3. Data Sources – Connecting Grafana to Everything

### What
A **Data Source** in Grafana is a connection to an external system from which Grafana retrieves data for dashboards. Grafana is not a database — it's a visualization layer that connects to many different backends.

### Why Multiple Data Sources Matter

> 💡 **Grafana's power:** One dashboard can combine data from Prometheus (infrastructure), AWS CloudWatch (cloud services), PostgreSQL (business data), and Elasticsearch (logs) — all in one unified view.

### Supported Data Sources

| Data Source | Use Case |
|-------------|---------|
| **Prometheus** ✅ (primary for K8s) | Infrastructure and application metrics |
| **AWS CloudWatch** | AWS service metrics (EC2, RDS, Lambda) |
| **Azure Monitor** | Azure service metrics |
| **GCP Cloud Monitoring** | GCP service metrics |
| **Elasticsearch / OpenSearch** | Log analytics |
| **Loki** | Kubernetes log aggregation (Grafana's own log tool) |
| **PostgreSQL / MySQL** | Business metrics from databases |
| **InfluxDB** | Time-series data |
| **Jaeger / Zipkin** | Distributed tracing |
| **Google Sheets / Excel** | Simple tabular data for dashboards |

### How Prometheus Connects to Grafana

When `kube-prometheus-stack` is installed via Helm, Prometheus is automatically pre-configured as a data source in Grafana. No manual setup needed.

To verify:
```
Grafana → Connections → Data Sources
→ Prometheus (auto-configured)
   URL: http://prometheus-operated:9090   ← in-cluster DNS name, port 9090
   Access: Server (Grafana calls Prometheus internally)
   Status: ✅ Data source connected and labels found
```

### Manually Adding a Data Source

```
Grafana → Connections → Data Sources → Add new data source

Select: Prometheus
  URL: http://prometheus-operated.monitoring.svc:9090
  Scrape interval: 30s
  Query timeout: 60s
  HTTP Method: POST

Click: Save & Test
→ "Data source connected and labels found" ✅
```

### Adding AWS CloudWatch

```
Grafana → Data Sources → Add → CloudWatch
  Auth Provider: AWS SDK Default  (uses EC2 instance role)
  Default Region: us-east-1
  
  OR:
  Access Key ID: AKIA...
  Secret Access Key: ***
  
  Click: Save & Test
  → Now you can query AWS metrics in Grafana panels
```

---

## 4. Scrape Interval & Timeout Settings

### What
- **Scrape Interval:** How often Prometheus collects metrics from targets
- **Timeout:** How long Prometheus waits for a target to respond before marking the scrape as failed

### The Settings from Class

```
Scrape Interval: 30 seconds
Query Timeout:   60 seconds
```

### Choosing the Right Interval

| Interval | Use Case | Trade-off |
|----------|---------|-----------|
| **10s** | High-frequency trading, real-time critical systems | High storage consumption |
| **15s** | Default in most setups — good balance | — |
| **30s** | Class setting — slightly less granular | Less storage, acceptable for most cases |
| **60s** | Cost-sensitive environments | Misses brief spikes |

### Why the Timeout is Longer Than the Interval

If scrape interval = 30s and timeout = 30s:
- Prometheus calls target at t=0
- Target is slow → response at t=29s
- Next scrape fires at t=30s while previous is still pending
- Overlap causes issues

Setting timeout = 60s means:
- A slow scrape has up to 60 seconds to complete before being marked as failed
- Avoids false "target down" alerts from temporary slowness

### Where to Configure

In Grafana's data source settings:
```
Connections → Data Sources → Prometheus
  Scrape interval: 30s
  HTTP Method: POST
  Query timeout: 60s
```

In Prometheus configuration (via Helm values):
```yaml
prometheus:
  prometheusSpec:
    scrapeInterval: "30s"
    scrapeTimeout: "10s"    # Per-target timeout (different from query timeout)
    evaluationInterval: "30s"
```

---

## 5. Dashboard Management – 25,000+ Dashboards

### What
Grafana's official dashboard library at **grafana.com/grafana/dashboards** has over 25,000 community-contributed dashboards covering every technology imaginable. You don't need to build monitoring from scratch.

### Two Ways to Import a Dashboard

#### Method 1: Import by Dashboard ID (Fastest)

```
Grafana UI:
  Dashboards → New → Import
  
  Enter ID: 315
  Click: Load
  
  Select Data Source: Prometheus
  Click: Import
  
  → Dashboard loads immediately with all panels ✅
```

**Class used Dashboard ID: 315** — the Kubernetes cluster monitoring dashboard.

#### Method 2: Import via JSON File

```
1. Go to grafana.com/grafana/dashboards
2. Find the dashboard you want
3. Click: Download JSON
4. Save the file locally

Grafana UI:
  Dashboards → New → Import
  → Upload JSON file → Select file
  → Choose data source → Import
```

### Most Useful Dashboard IDs for Kubernetes DevOps

| Dashboard ID | Name | What It Shows |
|-------------|------|--------------|
| **315** | Kubernetes cluster monitoring | Overall cluster health |
| **1860** | Node Exporter Full | Detailed per-node metrics |
| **6336** | Kubernetes pod monitoring | Per-pod CPU, memory |
| **7249** | Kubernetes Cluster | Resources, capacity |
| **9614** | NGINX Ingress Controller | HTTP traffic, errors |
| **12685** | Spring Boot Statistics | JVM, HTTP metrics |
| **11159** | Node.js Application | Event loop, heap usage |
| **763** | Redis Dashboard | Cache metrics |
| **9628** | PostgreSQL Database | Query performance |
| **455** | MySQL Overview | Database metrics |

### Customizing a Dashboard

```
Grafana UI:
  Open any panel → Click title → Edit
  
  Panel title: "Cluster CPU Usage"
  
  Query: Change the PromQL query
    Before: node_cpu_seconds_total{mode="user"}
    After:  100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
  
  Visualization: Click "Visualization" dropdown
    Time series (line graph)
    Bar chart
    Gauge (circular meter)
    Stat (single number)
    Table
    Heatmap
  
  Display options:
    Unit: Percent (0-100)
    Thresholds: Green < 70%, Yellow 70-85%, Red > 85%
  
  Click: Apply → Save dashboard
```

### Saving and Sharing Dashboards

```
Grafana: Dashboard → Share → Export
  → Download JSON  (save to Git repo)
  → Link          (share with teammates)
  → Snapshot      (public read-only view)
```

> **Best practice:** Save all custom dashboard JSON files to your Git repository. This way, if Grafana's database is lost (pod restart without PV), dashboards can be restored in minutes.

---

## 6. The 5 Core Dashboard Types DevOps Must Know

From class: Focus on these 5 categories. Everything else is secondary.

### 1. Cluster Dashboard
**What it shows:** Overall health of the Kubernetes cluster

Key metrics:
```
- Total CPU usage / available
- Total memory usage / available
- Node count (ready vs not ready)
- Pod count across all namespaces
- Persistent volume usage
- API server request rate
```

### 2. Namespace Dashboard
**What it shows:** Resource consumption per namespace

Key metrics:
```
- CPU usage by namespace (which team is using the most?)
- Memory by namespace
- Pod count per namespace
- Resource quota utilization (are teams near their limits?)
- Network in/out per namespace
```

### 3. Workloads Dashboard
**What it shows:** Deployments, StatefulSets, DaemonSets health

Key metrics:
```
- Deployment ready replicas vs desired
- Pod restart count (is something crashing?)
- OOMKilled events
- CPU throttling (containers hitting CPU limits)
- HPA status and scaling events
```

### 4. Application Dashboard
**What it shows:** Custom application-level metrics (requires app instrumentation)

Key metrics:
```
- HTTP request rate (requests/second)
- HTTP error rate (% of 5xx responses)
- Request latency (P50, P95, P99)
- Active users / sessions
- Business metrics (orders per minute, etc.)
```

### 5. Networking Dashboard
**What it shows:** Cluster network traffic and connectivity

Key metrics:
```
- Network receive / transmit bytes per pod
- DNS query rate and latency
- Service request rate
- Ingress traffic and error rate
- Connection pool utilization
```

---

## 7. Troubleshooting – When Data Shows "NA"

### The Problem
You import a dashboard and panels show "No data" or "N/A" instead of metrics.

### Systematic Troubleshooting Steps

```
Step 1: Check data source connection
  Grafana → Connections → Data Sources → Prometheus
  Click: "Test" 
  → "Data source connected and labels found" ✅
  → "Connection refused" ❌ → Prometheus URL wrong or Prometheus down

Step 2: Check if the metric EXISTS in Prometheus
  Grafana → Explore tab
  Data source: Prometheus
  
  Type metric name in the query field:
    node_cpu_seconds_total
  
  Click: Run query
  → Data appears = metric exists, dashboard panel query is wrong
  → No data = metric doesn't exist (wrong exporter? wrong Prometheus config?)

Step 3: Check the panel's query
  Panel → Edit → Query
  
  Copy the PromQL query
  Go to: Explore tab
  Paste and run
  → See the actual error (label doesn't exist, wrong function, etc.)

Step 4: Check time range
  Dashboard top right: Time picker
  → Set to "Last 1 hour" or "Last 5 minutes"
  → Sometimes "Last 5 years" shows no recent data

Step 5: Check label names
  Dashboard was built for different label names
  Example: dashboard uses {job="kubernetes-nodes"}
           your setup has {job="node-exporter"}
  Fix: Edit panel query to match your label values
```

### Common "NA" Causes

| Cause | Symptom | Fix |
|-------|---------|-----|
| Wrong Prometheus URL | All panels empty | Fix data source URL |
| Missing exporter | Specific metrics empty | Install missing exporter (node-exporter, kube-state-metrics) |
| Wrong label in query | Some panels work, some don't | Edit panel query, use Explorer to find correct labels |
| Time range too narrow | "No data" for recent period | Prometheus needs time to collect data after install |
| Wrong metric name | Query shows error | Use Prometheus UI or Explorer to find correct metric name |

---

## 8. Grafana Alerting – Complete Setup

### What
Grafana Alerting allows you to define **rules** — when a metric crosses a threshold, Grafana fires an alert and sends a notification to configured contact points (Slack, Teams, PagerDuty, email, Jira).

> 💡 **Two alerting systems exist:** Prometheus AlertManager (rules in PrometheusRule YAML) and Grafana Alerting (rules in Grafana UI). Both work with the same `kube-prometheus-stack`. Use Grafana Alerting for flexibility; use PrometheusRule for GitOps/code-based management.

### Step 1: Configure a Contact Point

A **Contact Point** is where alerts get sent.

#### Email Contact Point

```
Grafana → Alerting → Contact Points → New Contact Point

Name: DevOps Email Alerts
Integration: Email

Addresses: devops@company.com; manager@company.com
Subject: [ALERT] {{ .GroupLabels.alertname }}
Message: {{ range .Alerts }}{{ .Annotations.description }}{{ end }}

Requirements:
  Grafana needs SMTP configuration in grafana.ini or Helm values:
  
  [smtp]
  enabled = true
  host = smtp.company.com:587
  user = alerts@company.com
  password = smtp_password
  from_address = grafana@company.com
```

#### Slack Contact Point

```
Grafana → Alerting → Contact Points → New Contact Point

Name: Slack DevOps Channel
Integration: Slack

Webhook URL: https://hooks.slack.com/services/T00000/B00000/XXXX
Channel: #devops-alerts    (or leave blank — webhook determines channel)
Title: [{{ .Status | toUpper }}] {{ .GroupLabels.alertname }}
Text: {{ range .Alerts }}{{ .Annotations.summary }}{{ end }}

Getting the webhook URL:
  Slack → Apps → Incoming Webhooks → Add to Slack
  Choose channel → Create → Copy webhook URL
```

#### Microsoft Teams Contact Point

```
Grafana → Alerting → Contact Points → New Contact Point

Name: Teams Alerts
Integration: Microsoft Teams

URL: https://company.webhook.office.com/webhookb2/XXX/IncomingWebhook/YYY/ZZZ

Getting webhook URL:
  Teams → Channel → ... → Connectors
  Incoming Webhook → Configure → Copy URL
```

#### PagerDuty Contact Point

```
Grafana → Alerting → Contact Points → New Contact Point

Name: PagerDuty On-Call
Integration: PagerDuty

API Key: (from PagerDuty Integrations → Add Integration → Prometheus)
Severity: critical

Use case: After-hours critical alerts that need immediate human response
```

### Step 2: Create an Alert Rule

```
Grafana → Alerting → Alert Rules → New Alert Rule

Step 1 - Query:
  Name: High CPU Usage
  Data source: Prometheus
  
  Query A:
    100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
  
  → This gives cluster-wide CPU %

Step 2 - Threshold:
  WHEN: last() OF query A
  IS ABOVE: 80   ← Fire alert when CPU > 80%
  
  OR use multi-threshold:
    > 60%  → Warning
    > 80%  → Critical

Step 3 - Details:
  Rule name: HighClusterCPU
  Folder: Infrastructure Alerts
  Evaluation group: every-1-minute
  Pending period: 5m   ← Must stay above threshold for 5 min before firing
                         (prevents false alerts from brief spikes)
  Labels:
    severity: critical
    team: devops

Step 4 - Annotations:
  Summary: Cluster CPU usage is {{ $values.A.Value | printf "%.1f" }}%
  Description: CPU has been above 80% for more than 5 minutes

Save
```

### Step 3: Configure Notification Policy

The **Notification Policy** determines which alerts go to which contact point.

```
Grafana → Alerting → Notification Policies

Default policy:
  Contact point: DevOps Email    ← Where ALL alerts go by default
  
Specific routing:
  + New nested policy
  Match labels: severity=critical
  Contact point: PagerDuty       ← Critical alerts → wake someone up
  
  + New nested policy  
  Match labels: severity=warning
  Contact point: Slack           ← Warnings → team channel
```

### Alert States

```
Normal → Pending → Firing → Resolved

Normal:  Metric is within acceptable range
Pending: Threshold exceeded, waiting for "Pending period" to confirm
Firing:  Threshold exceeded for the full pending period → notification sent
Resolved: Metric back within range → "Resolved" notification sent (optional)
```

---

## 9. Silence Periods – Suppressing Alerts During Maintenance

### What
A **Silence** is a time-bounded rule that suppresses (mutes) matching alerts so they don't send notifications. Used during planned maintenance to avoid alarm fatigue.

> 💡 **Analogy:** Before a surgeon performs an operation, the hospital sets the patient's blood pressure monitor to "silence mode" for the procedure — they know BP will be unusual. A Silence does the same for your infrastructure during maintenance.

### Why

```
Without Silences:
  Friday 10PM: "Redeploying payment service for v2.0"
  
  During deployment:
  - Pods restart → restart count alert fires → Slack spammed
  - Brief CPU spike → CPU alert fires
  - Temporary endpoint unavailability → availability alert fires
  
  Team receives 47 Slack messages during a 10-minute deployment
  → Alert fatigue → team starts ignoring alerts → DANGEROUS ❌

With Silence:
  Before deployment: Create silence for 30 minutes
  During deployment: Alerts still fire in Grafana UI
                    BUT notifications are suppressed
  After silence expires: Normal alerting resumes automatically ✅
```

### Creating a Silence

```
Grafana → Alerting → Silences → Add Silence

Duration: 
  Start: 2026-05-16 22:00
  End:   2026-05-16 22:30   ← 30 minute maintenance window

Matchers (which alerts to silence):
  namespace = production   ← Silence all production alerts
  
  OR more specific:
  alertname = HighCPU      ← Only silence this specific alert

Comment: Planned deployment of payment-service v2.0

Click: Submit → Silence active ✅
```

### Checking Active Silences

```bash
# Via Grafana UI:
Alerting → Silences → Active silences list

# Via AlertManager API:
curl http://alertmanager-service:9093/api/v2/silences

# Via kubectl (AlertManager pod):
kubectl exec -n monitoring alertmanager-xxx -- \
  curl localhost:9093/api/v2/silences
```

---

## 10. Real-World Applications of Grafana

### Domino's Pizza Example (from class)

> The instructor mentioned Domino's uses Grafana for **customer-facing displays** (order tracking screens) AND internal monitoring.

#### Customer-Facing: Order Tracking Dashboard
```
When you order pizza and see:
  "Order received" → "Being prepared" → "In oven" → "Out for delivery"
  
This status comes from their order management system. Grafana can visualize
this data in real time — showing how many orders are in each stage,
average preparation time, delivery efficiency, etc.
```

#### Internal Operations Dashboard
```
Domino's operations team might monitor:
  - Orders per minute per store
  - Average delivery time vs SLA
  - Failed payment transactions
  - Website/app error rate during peak hours
  - Inventory levels (ingredient tracking)
  - Driver GPS tracking metrics
```

### Other Real-World Grafana Use Cases

| Industry | Use Case |
|----------|---------|
| **E-commerce** | Order funnel metrics, cart abandonment rate, checkout success rate |
| **Banking** | Transaction volume, failed auth count, fraud detection metrics |
| **Healthcare** | Patient monitor data visualization, equipment uptime |
| **Gaming** | Player count per server, latency per region, matchmaking queue depth |
| **Logistics** | Package tracking status, delivery SLA compliance |
| **SaaS** | API response time per customer, feature usage analytics |

---

## 11. DevOps Role in Monitoring vs L1/L2 Teams

### The Division of Responsibility

```
DEVOPS ENGINEERS RESPONSIBILITY:
  ✅ Set up Prometheus + Grafana infrastructure
  ✅ Configure Helm deployment and values
  ✅ Connect data sources (Prometheus, CloudWatch, etc.)
  ✅ Import baseline dashboards
  ✅ Configure alerting rules and contact points
  ✅ Ensure PVs are configured (data persistence)
  ✅ Monitor the monitoring system itself (meta-monitoring)
  ✅ Troubleshoot Kubernetes issues flagged by L1/L2
  ✅ Integration verification (data flows correctly)
  ✅ Set up namespace isolation and RBAC

L1/L2 SUPPORT TEAM RESPONSIBILITY:
  ✅ Day-to-day monitoring of Grafana dashboards
  ✅ Acknowledge and investigate alerts
  ✅ Create custom dashboards for their team's needs (L2)
  ✅ First response to incidents
  ✅ Escalation to DevOps when Kubernetes issues found
  ✅ Document known issues and runbooks
  ❌ NOT responsible for infra setup or Helm management
```

### The Escalation Chain

```
Alert fires
    │
    ▼
L1 Support (first response)
  → Check dashboard
  → Identify affected service
  → Attempt standard fix (restart pod, etc.)
  → If fixed: document and close
    │
    │ If not fixed in 15-30 minutes
    ▼
L2 Support (deeper investigation)
  → Check logs, recent deployments
  → Compare with baseline dashboards
  → Attempt advanced fixes
    │
    │ If Kubernetes infrastructure issue
    ▼
DevOps Engineer
  → Kubernetes-level troubleshooting
  → Deployment rollbacks
  → Resource scaling
  → Infrastructure changes
```

---

## 12. Tech Stack Mapping

### Complete Monitoring Stack for Production

```
APPLICATION LAYER                    MONITORING LAYER
─────────────────                    ────────────────

React/Next.js (frontend)
  No built-in metrics needed         → Prometheus scrapes nginx-ingress metrics
  
Node.js API (backend)
  prom-client: request metrics ──────► ServiceMonitor → Prometheus
  
PostgreSQL                           
  postgres-exporter ─────────────────► Prometheus
  
Redis
  redis-exporter ────────────────────► Prometheus
  
AWS Services (RDS, Lambda, S3)
  cloudwatch-exporter ───────────────► Prometheus → Grafana CloudWatch datasource
  
Kubernetes Infrastructure
  node-exporter (DaemonSet) ─────────► Prometheus
  kube-state-metrics ────────────────► Prometheus

ALL DATA →  PROMETHEUS (time-series DB)
              │
              │ PromQL queries
              ▼
          GRAFANA (visualization)
              │
              ├── Dashboard: Cluster Overview (ID: 315)
              ├── Dashboard: Node Exporter Full (ID: 1860)  
              ├── Dashboard: Application Metrics (custom)
              ├── Dashboard: Business KPIs (custom)
              │
              │ Alerts
              ▼
          ALERTMANAGER
              ├── Slack: #devops-alerts (warnings)
              ├── PagerDuty: on-call engineer (critical)
              └── Jira: ticket auto-creation (P2/P3 issues)
```

### Grafana in a Jenkins Pipeline

```groovy
// After deploying, verify monitoring is working
stage('Verify Monitoring') {
    steps {
        sh '''
            # Verify Prometheus is scraping the new service
            kubectl port-forward svc/prometheus-kube-prometheus-prometheus \
              9090:9090 -n monitoring &
            sleep 5
            
            # Query Prometheus to confirm service metrics are being collected
            METRIC_COUNT=$(curl -s \
              "http://localhost:9090/api/v1/query?query=up{job='my-app'}" | \
              python3 -c "import json,sys; d=json.load(sys.stdin); print(len(d['data']['result']))")
            
            echo "Prometheus targets for my-app: $METRIC_COUNT"
            [ "$METRIC_COUNT" -gt "0" ] || { echo "ERROR: No metrics found"; exit 1; }
            
            kill %1  # Stop port-forward
        '''
    }
}
```

---

## 13. Visual Diagrams

### Diagram 1: Grafana Component Architecture

```
                    GRAFANA SERVER
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  ┌──────────────┐   ┌──────────────┐  ┌─────────────┐  │
│  │   Dashboards │   │  Alerting    │  │    Users    │  │
│  │              │   │              │  │             │  │
│  │  ID: 315     │   │  Rules       │  │  Admin      │  │
│  │  ID: 1860    │   │  Thresholds  │  │  Editor     │  │
│  │  Custom      │   │  Silences    │  │  Viewer     │  │
│  └──────┬───────┘   └──────┬───────┘  └─────────────┘  │
│         │ PromQL           │ Query                      │
│         │                  │                            │
│  ┌──────▼──────────────────▼──────────────────────────┐ │
│  │              Data Sources                          │ │
│  │  Prometheus │ CloudWatch │ PostgreSQL │ Loki │ ... │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
         │                    │
         │ Port 9090          │ Various APIs
         ▼                    ▼
   PROMETHEUS              AWS/Azure/GCP
   (in-cluster)            (external)
```

---

### Diagram 2: Alert Lifecycle

```
Metric: CPU = 85%
         │
         │ Threshold: > 80%
         ▼
    ┌──────────┐
    │  PENDING │  ← 0 to 5 minutes (pending period)
    └────┬─────┘  Still above threshold after 5 min?
         │ YES
         ▼
    ┌──────────┐
    │  FIRING  │  ← Alert is active, notifications sent
    └────┬─────┘
         │
    ┌────▼────────────────────┐
    │    ALERTMANAGER         │
    │                         │
    │  Route by label:        │
    │  severity=warning ──►   Slack
    │  severity=critical ──►  PagerDuty + Slack
    │  team=database ──────►  Database team channel
    └─────────────────────────┘
         │
         │ CPU drops to 60%
         ▼
    ┌───────────┐
    │ RESOLVED  │  ← Resolved notification sent
    └───────────┘
```

---

### Diagram 3: Grafana User Access Levels

```
                GRAFANA ORGANIZATION
                        │
           ┌────────────┼────────────┐
           ▼            ▼            ▼
       [Admin]      [Editor]      [Viewer]
           │            │            │
   Full control   Create/edit   View only
   Users          Dashboards    No changes
   Orgs           Data sources
   Settings       Alert rules
   
   Who gets what:
   DevOps Lead:  Admin   ─── Manages everything
   DevOps Eng:   Editor  ─── Creates dashboards
   L1/L2 Ops:   Viewer  ─── Monitors, reads alerts
   Developers:   Viewer  ─── See app dashboards
   Management:   Viewer  ─── See KPI dashboards
```

---

### Diagram 4: Dashboard Import Methods

```
METHOD 1: Dashboard ID (fastest)                METHOD 2: JSON File
─────────────────────────────                   ─────────────────────
grafana.com/grafana/dashboards                  grafana.com/grafana/dashboards
  Search: "kubernetes"                              Search: "kubernetes"
  Find dashboard                                    Find dashboard
  Copy ID: 315                                      Click: Download JSON
                                                    Save: kubernetes-315.json
Grafana UI:                                     
  Dashboards → Import                           Grafana UI:
  ID: 315                                         Dashboards → Import
  Load                                            Upload JSON file
  Select: Prometheus datasource                   Select: Prometheus datasource
  Import                                          Import
  ✅ Dashboard ready in 30 seconds                ✅ Dashboard ready
  
Good for: Quick setup                           Good for: Offline environments,
                                                version controlling dashboards
```

---

### Diagram 5: The 5 Core Dashboards

```
5 DASHBOARDS DEVOPS MUST HAVE
────────────────────────────────────────────────────────
Dashboard 1: CLUSTER          "Is the whole cluster healthy?"
  CPU, Memory, Nodes, Pod count

Dashboard 2: NAMESPACE        "Which team is using what?"
  Per-namespace CPU, memory, quotas

Dashboard 3: WORKLOADS        "Are my deployments healthy?"
  Ready replicas, restarts, OOMKills

Dashboard 4: APPLICATION      "Is my app performing well?"
  Request rate, errors, latency, business metrics

Dashboard 5: NETWORKING       "Is traffic flowing correctly?"
  In/Out bytes, DNS, ingress traffic
```

---

### Diagram 6: Silence During Maintenance

```
TIMELINE:
                    MAINTENANCE WINDOW
                    ┌─────────────────┐
                    │   SILENCE ON    │
─────────────────── │  Alerts still   │ ─────────────────
                    │ fire in Grafana │
ALERTS:             │  but NO Slack   │
  CPU spike ────────►   messages      ├──────────────────►
  Pod restart ──────►   sent          │
  Brief error ──────►                 │
                    └─────────────────┘
                         Silence expires
                         Normal alerting resumes

Team peace during deployment ✅
Alerts still visible in Grafana UI ✅
Alert history preserved ✅
```

---

## 14. Code & Practical Examples

### Example 1: Complete Grafana Helm Values with Alerting

```yaml
# grafana-values.yaml — Comprehensive Grafana configuration

grafana:
  adminPassword: "SecureAdminPassword123!"
  
  service:
    type: LoadBalancer
    port: 3000
  
  persistence:
    enabled: true
    size: 10Gi
    storageClassName: standard
  
  # SMTP for email alerts
  grafana.ini:
    smtp:
      enabled: true
      host: smtp.gmail.com:587
      user: alerts@company.com
      password: your_app_password
      from_address: grafana-alerts@company.com
      from_name: "Grafana Monitoring"
    
    auth:
      disable_login_form: false
    
    security:
      admin_user: admin
      admin_password: SecureAdminPassword123!
  
  # Pre-configure Slack notifier
  notifiers:
  - name: slack-devops
    type: slack
    settings:
      url: https://hooks.slack.com/services/XXX/YYY/ZZZ
      recipient: "#devops-alerts"
  
  # Auto-provision dashboards from ConfigMap
  dashboardProviders:
    dashboardproviders.yaml:
      apiVersion: 1
      providers:
      - name: 'default'
        orgId: 1
        folder: 'Kubernetes'
        type: file
        disableDeletion: false
        options:
          path: /var/lib/grafana/dashboards
  
  # Auto-import specific dashboards
  dashboards:
    default:
      node-exporter:
        gnetId: 1860        # Node Exporter Full
        revision: 36
        datasource: Prometheus
      kubernetes-cluster:
        gnetId: 7249        # Kubernetes Cluster
        revision: 1
        datasource: Prometheus
```

```bash
helm upgrade prometheus prometheus-community/kube-prometheus-stack \
  -n monitoring \
  -f grafana-values.yaml
```

---

### Example 2: Grafana Dashboard as Code (JSON ConfigMap)

```yaml
# custom-dashboard-configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: custom-k8s-dashboard
  namespace: monitoring
  labels:
    grafana_dashboard: "1"    # Grafana sidecar picks this up automatically
data:
  k8s-overview.json: |
    {
      "title": "K8s Production Overview",
      "uid": "k8s-prod-overview",
      "panels": [
        {
          "title": "Cluster CPU Usage %",
          "type": "timeseries",
          "targets": [
            {
              "expr": "100 - (avg(rate(node_cpu_seconds_total{mode=\"idle\"}[5m])) * 100)",
              "legendFormat": "CPU %"
            }
          ],
          "fieldConfig": {
            "defaults": {
              "unit": "percent",
              "thresholds": {
                "steps": [
                  {"value": 0, "color": "green"},
                  {"value": 70, "color": "yellow"},
                  {"value": 85, "color": "red"}
                ]
              }
            }
          }
        },
        {
          "title": "Pod Restart Count (Last Hour)",
          "type": "stat",
          "targets": [
            {
              "expr": "increase(kube_pod_container_status_restarts_total{namespace=\"production\"}[1h])",
              "legendFormat": "{{pod}}"
            }
          ]
        }
      ],
      "time": {"from": "now-1h", "to": "now"},
      "refresh": "30s"
    }
```

```bash
kubectl apply -f custom-dashboard-configmap.yaml
# Grafana sidecar auto-loads it within 30 seconds — no restart needed ✅
```

---

### Example 3: Prometheus Alert Rules YAML

```yaml
# production-alert-rules.yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: production-alerts
  namespace: monitoring
  labels:
    release: prometheus
spec:
  groups:

  - name: cpu-alerts
    rules:
    - alert: ClusterCPUWarning
      expr: |
        100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 60
      for: 5m
      labels:
        severity: warning
        team: devops
      annotations:
        summary: "Cluster CPU at {{ $value | printf \"%.1f\" }}% (warning threshold: 60%)"
        description: "Cluster CPU usage has exceeded 60% for 5 minutes."

    - alert: ClusterCPUCritical
      expr: |
        100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
      for: 10m
      labels:
        severity: critical
        team: devops
      annotations:
        summary: "CRITICAL: Cluster CPU at {{ $value | printf \"%.1f\" }}%"
        description: "Cluster CPU usage has exceeded 80% for 10 minutes. Immediate action required."

  - name: memory-alerts
    rules:
    - alert: NodeMemoryHigh
      expr: |
        (1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) * 100 > 85
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "Node {{ $labels.instance }} memory usage at {{ $value | printf \"%.1f\" }}%"

  - name: pod-alerts
    rules:
    - alert: PodCrashLooping
      expr: |
        rate(kube_pod_container_status_restarts_total[15m]) * 60 * 15 > 3
      for: 5m
      labels:
        severity: critical
      annotations:
        summary: "Pod {{ $labels.pod }} in namespace {{ $labels.namespace }} is crash-looping"
        description: "{{ $labels.pod }} has restarted more than 3 times in 15 minutes"

    - alert: DeploymentNotReady
      expr: |
        kube_deployment_status_replicas_ready < kube_deployment_spec_replicas
      for: 10m
      labels:
        severity: warning
      annotations:
        summary: "Deployment {{ $labels.deployment }} has unavailable replicas"

  - name: disk-alerts
    rules:
    - alert: NodeDiskAlmostFull
      expr: |
        (1 - node_filesystem_avail_bytes{mountpoint="/"} / 
             node_filesystem_size_bytes{mountpoint="/"}) * 100 > 85
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "Node {{ $labels.instance }} disk at {{ $value | printf \"%.1f\" }}%"
```

```bash
kubectl apply -f production-alert-rules.yaml
```

---

### Example 4: Key PromQL Queries for the 5 Dashboard Types

```promql
# === 1. CLUSTER DASHBOARD ===

# Overall cluster CPU %
100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# Overall cluster memory used %
(1 - sum(node_memory_MemAvailable_bytes) / sum(node_memory_MemTotal_bytes)) * 100

# Total running pods
count(kube_pod_status_phase{phase="Running"})

# Nodes not ready
count(kube_node_status_condition{condition="Ready",status!="true"})


# === 2. NAMESPACE DASHBOARD ===

# CPU usage by namespace
sum(rate(container_cpu_usage_seconds_total{container!=""}[5m])) by (namespace)

# Memory by namespace (MB)
sum(container_memory_usage_bytes{container!=""}) by (namespace) / 1024 / 1024

# Pod count per namespace
count(kube_pod_status_phase{phase="Running"}) by (namespace)


# === 3. WORKLOADS DASHBOARD ===

# Deployments with unavailable replicas
kube_deployment_status_replicas_unavailable > 0

# Pod restart count in last hour
sum(increase(kube_pod_container_status_restarts_total[1h])) by (pod, namespace)

# OOMKilled pods in last hour
sum(increase(kube_pod_container_status_last_terminated_reason{reason="OOMKilled"}[1h])) by (pod)

# CPU throttling %
rate(container_cpu_throttled_seconds_total[5m]) / rate(container_cpu_usage_seconds_total[5m]) * 100


# === 4. APPLICATION DASHBOARD ===

# HTTP requests per second
rate(http_requests_total[5m])

# HTTP error rate %
rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m]) * 100

# P95 request latency
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))


# === 5. NETWORKING DASHBOARD ===

# Network receive bytes per pod
rate(container_network_receive_bytes_total[5m])

# Network transmit bytes per pod
rate(container_network_transmit_bytes_total[5m])

# DNS query rate
rate(coredns_dns_requests_total[5m])
```

---

### Example 5: Grafana Silence via API (for automation)

```bash
#!/bin/bash
# Create a Grafana silence via API during deployment

GRAFANA_URL="http://grafana-external-ip:3000"
GRAFANA_USER="admin"
GRAFANA_PASS="prom-operator"
NAMESPACE="production"
SILENCE_DURATION_MINUTES=30

# Calculate end time
END_TIME=$(date -d "+${SILENCE_DURATION_MINUTES} minutes" -u +"%Y-%m-%dT%H:%M:%SZ")

# Create silence
curl -X POST "$GRAFANA_URL/api/alertmanager/grafana/api/v2/silences" \
  -u "$GRAFANA_USER:$GRAFANA_PASS" \
  -H "Content-Type: application/json" \
  -d '{
    "matchers": [
      {
        "name": "namespace",
        "value": "'"$NAMESPACE"'",
        "isRegex": false
      }
    ],
    "startsAt": "'"$(date -u +"%Y-%m-%dT%H:%M:%SZ")"'",
    "endsAt": "'"$END_TIME"'",
    "comment": "Automated silence during CI/CD deployment"
  }'

echo "Silence created for $NAMESPACE namespace for $SILENCE_DURATION_MINUTES minutes"
```

---

## 15. Scenario-Based Q&A

---

🔍 **Scenario 1:** A developer asks to see why the payment service is slow. They have Viewer role in Grafana. What dashboards can they use and what do they look at?

✅ **Answer:** With Viewer role, the developer can open any dashboard but cannot edit. Direct them to: (1) **Workloads dashboard** — check if payment-service pods have high CPU throttling or recent restarts; (2) **Application dashboard** — if payment-service exposes custom metrics, check P95 latency and error rate trends; (3) **Namespace dashboard** — check if production namespace is near resource quota limits (could cause all services to slow); (4) Use the Explorer tab (if Viewer has access) to run: `histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{service="payment"}[5m]))` — the 95th percentile response time. If they need to edit/create dashboards, they need Editor role — escalate to DevOps to change the role if justified.

---

🔍 **Scenario 2:** Your team has a planned maintenance window Saturday 2 AM for a Kubernetes upgrade. The upgrade will cause node restarts and brief pod disruptions. How do you prevent alert spam during the 2-hour window?

✅ **Answer:** Create a Silence before the maintenance window: Grafana → Alerting → Silences → New Silence. Set Start: Saturday 01:45 AM (15 min buffer), End: Saturday 04:00 AM (extra buffer). Add matcher: `severity=~(warning|critical)` to silence all severity levels. Comment: "Kubernetes upgrade - node rolling restart." Alternatively, create separate silences for specific alert names (NodeNotReady, PodCrashLooping) rather than all alerts, to keep unrelated alerts active. After the silence expires, all normal alerting automatically resumes. Alerts that fired during the window are still visible in Grafana's alert history for post-maintenance review.

---

🔍 **Scenario 3:** You imported Dashboard ID 315 but every panel shows "N/A." The previous dashboard you imported worked fine. What's your troubleshooting process?

✅ **Answer:** Systematic 4-step approach: (1) **Check time range** — top right of Grafana. Some dashboards default to "Last 5 minutes" which is too recent for Prometheus to have much data right after install. Try "Last 1 hour"; (2) **Check data source** — open a failing panel → Edit → Query. The query references a data source. Is it set to "Prometheus"? Is the Prometheus data source connected? (Connections → Test); (3) **Explorer check** — copy one query from the failing panel, go to Explore → Prometheus → paste the query → Run. Does it return data? If yes, the dashboard has wrong time range variables. If no data, the metric doesn't exist in your Prometheus; (4) **Label mismatch** — Dashboard 315 might use `{job="kubernetes-nodes"}` but your Node Exporter labels differently. Use the Prometheus UI to discover actual label values: `label_values(node_cpu_seconds_total, job)`.

---

🔍 **Scenario 4:** Your L1 team is getting hundreds of alerts at 3 AM during a traffic spike and eventually stops responding to them (alert fatigue). What do you fix in Grafana/AlertManager?

✅ **Answer:** Three fixes: (1) **Tune thresholds** — if CPU alert fires at 60% but the system handles 75% fine, raise the threshold to 75%. AlertManager groups repeated alerts, but fixing the root threshold is better; (2) **Increase pending period** — change alert rules from `for: 1m` to `for: 10m`. Brief spikes during traffic don't need alerts — sustained issues do; (3) **Routing by severity** — create notification policies: Warning alerts → Slack only (not PagerDuty), Critical alerts → PagerDuty + Slack. L1 team checks Slack in the morning; critical issues page the on-call. This prevents 3 AM wakeups for warnings; (4) **HPA** — the root cause is CPU spikes from traffic. Configure HPA so pods auto-scale, preventing the CPU spike entirely and eliminating the alert trigger.

---

🔍 **Scenario 5:** A new DevOps intern asks: "Why do we need Grafana when Prometheus already has a UI?" How do you explain the difference clearly?

✅ **Answer:** "Prometheus UI is like Excel with raw data — functional but basic. Grafana is like Power BI or Tableau — it turns that data into professional dashboards your whole team can understand. Prometheus UI: one query at a time, basic graphs, no dashboards, no sharing, no alerting UI. Grafana: multiple panels on one screen (cluster overview at a glance), beautiful visualizations (line charts, gauges, heatmaps), pre-built dashboards for everything (just import by ID), shared with your whole team, connects to multiple data sources (Prometheus + AWS CloudWatch + database all on one dashboard), alert management UI, and role-based access (L1 team gets view-only, DevOps gets edit access). In short: Prometheus is where the data lives; Grafana is how humans consume and act on that data."

---

🔍 **Scenario 6:** Management wants a dashboard showing business metrics: orders per minute, revenue per hour, and checkout success rate — alongside Kubernetes infrastructure metrics. Is this possible in Grafana?

✅ **Answer:** Yes, this is one of Grafana's strongest use cases — unified business + infrastructure dashboards. Setup: (1) **Business metrics**: Instrument the application with `prom-client` (Node.js) or Spring Actuator (Java). Expose custom metrics like `orders_total` (counter), `revenue_total` (counter), `checkout_attempts_total` and `checkout_success_total` (counters). Prometheus scrapes these via ServiceMonitor; (2) **Create unified dashboard** in Grafana with mixed panels: Panel 1: Orders per minute: `rate(orders_total[1m])`, Panel 2: Revenue per hour: `increase(revenue_total[1h])`, Panel 3: Checkout success rate: `rate(checkout_success_total[5m]) / rate(checkout_attempts_total[5m]) * 100`, Panel 4: API error rate: `rate(http_requests_total{status=~"5.."}[5m])`, Panel 5: Pod count; (3) Share with management as a "Business Overview" dashboard with Viewer role.

---

## 16. Interview Q&A

---

**Q1. How do you manage users and access control in Grafana?**

**A:** Grafana has a built-in user management system with three roles: Viewer (read-only, can see dashboards but not edit), Editor (can create and modify dashboards, add data sources), and Admin (full control — manage users, organizations, system settings). Users are created in Grafana Administration → Users. In production, the pattern is: DevOps leads get Admin, DevOps engineers get Editor, L1/L2 support and developers get Viewer. Grafana also supports LDAP/Active Directory integration for SSO and team-based permissions, and OAuth integration with GitHub, Google, or Azure AD — so users log in with their company credentials instead of managing a separate Grafana password. Organizations allow multi-tenancy within one Grafana instance.

---

**Q2. What is a Grafana Contact Point and how is it different from a Notification Policy?**

**A:** A Contact Point defines the destination and format of alert notifications — the WHERE and HOW. Examples: a Slack webhook URL + channel name, an email address + SMTP server, or a PagerDuty API key. A Notification Policy defines the routing rules — WHICH alerts go to WHICH contact point. The Notification Policy is like a sorting office: it looks at alert labels (severity=critical, team=database) and routes each alert to the appropriate Contact Point. Example: Notification Policy says "severity=critical → PagerDuty, severity=warning → Slack, team=database → database-team Slack channel." This separation allows one Contact Point (PagerDuty) to be used by multiple policies without duplicating the configuration.

---

**Q3. What are Silence periods in Grafana alerting and when would you use them?**

**A:** Silences temporarily suppress alert notifications for matching conditions during a specified time window. The alerts still fire and are visible in Grafana's alert history — only the notifications (Slack messages, PagerDuty pages) are suppressed. Use cases: planned maintenance windows (Kubernetes upgrades, deployments that cause brief disruptions), known issues being worked on (silence the alert while the fix is in progress), load testing (expected resource spikes shouldn't page the team), holiday periods (only critical alerts should wake someone up). Silences are time-bounded — they automatically expire and normal alerting resumes without manual intervention. Create via Grafana UI, AlertManager UI, or API for automation in CI/CD pipelines.

---

**Q4. How do you import a Grafana dashboard and what are the two methods?**

**A:** Two methods: (1) **Dashboard ID** — the simplest approach. Go to grafana.com/grafana/dashboards, find the dashboard, copy the numeric ID (e.g., 1860 for Node Exporter Full). In Grafana: Dashboards → Import → Enter ID → Load → Select Prometheus as data source → Import. Dashboard is ready in 30 seconds. (2) **JSON file** — download the dashboard JSON from grafana.com/grafana/dashboards. In Grafana: Dashboards → Import → Upload JSON file → Select data source → Import. The JSON method is preferred for production because: you can store dashboard JSON files in Git for version control, restore them if Grafana's database is lost, review changes in PRs, and deploy them automatically via ConfigMaps that Grafana's sidecar picks up without restart.

---

**Q5. Why should monitoring tools run in a separate Kubernetes namespace?**

**A:** Four reasons: (1) **Fault isolation** — if a monitoring pod consumes excessive resources, it shouldn't affect application pods. Namespace ResourceQuotas prevent monitoring from starving production; (2) **Security** — RBAC policies per namespace. L1 team gets read access to monitoring namespace; developers don't need access to monitoring infrastructure; (3) **Clarity** — `kubectl get pods -n production` shows only production pods, not 10+ monitoring pods mixed in; (4) **Lifecycle independence** — monitoring should survive application deployments and vice versa. If you accidentally delete the production namespace, monitoring keeps running, still collecting data, still firing alerts about the outage. Conversely, if Grafana needs a restart for config changes, applications are unaffected.

---

**Q6. What are the 5 core dashboard types a DevOps engineer should have in Grafana?**

**A:** (1) **Cluster dashboard** — overall health: total CPU/memory usage, node count, pod count across all namespaces, PV usage. Answers: "Is the cluster healthy?"; (2) **Namespace dashboard** — per-namespace resource consumption and quota utilization. Answers: "Which team is using the most resources?"; (3) **Workloads dashboard** — deployment health: ready replicas, pod restart counts, OOMKilled events, CPU throttling. Answers: "Are my applications running correctly?"; (4) **Application dashboard** — custom application metrics: request rate, error rate, P95 latency. Requires app instrumentation with prom-client. Answers: "Is my application performing well?"; (5) **Networking dashboard** — traffic flow: in/out bytes per pod, DNS query rate, ingress traffic, connection pool usage. Answers: "Is network communication healthy?" These five cover infrastructure, Kubernetes, application, and network — complete observability.

---

**Q7. How does Grafana connect to Prometheus, and what happens if the connection breaks?**

**A:** When installed via `kube-prometheus-stack` Helm chart, Prometheus is automatically pre-configured as a Grafana data source. The connection URL is the Kubernetes service DNS name: `http://prometheus-operated.monitoring.svc:9090` — this resolves to the Prometheus service within the cluster. If the connection breaks (Prometheus pod crashes, network issue), Grafana dashboards show "No data" or "N/A" instead of metrics. Troubleshoot by: going to Connections → Data Sources → Prometheus → clicking "Test" — this shows whether the connection is working and returns the specific error. Fix by checking `kubectl get pods -n monitoring | grep prometheus` — if the Prometheus pod is down, investigate with `kubectl describe pod` and `kubectl logs`.

---

**Q8. What is the DevOps engineer's responsibility in monitoring vs the L1/L2 support team?**

**A:** Clear division: DevOps sets up the infrastructure — installing Prometheus and Grafana via Helm, configuring namespaces, connecting data sources, importing baseline dashboards, setting up alerting rules and contact points, ensuring persistent volumes for data survival, and verifying the end-to-end data flow. DevOps also troubleshoots Kubernetes-level issues escalated from L1/L2 (pod scheduling, resource limits, RBAC). L1/L2 support handles day-to-day operations — monitoring dashboards, acknowledging and investigating alerts, first-level incident response, creating team-specific dashboards (L2 with Editor role), and documenting runbooks. DevOps focuses on "does the monitoring system work correctly" — L1/L2 focuses on "what is the monitoring system telling us." The goal is that DevOps builds the car and L1/L2 drives it daily.

---


← Previous: [`40_Kubernetes_Monitoring_Prometheus_Grafana_&_Helm.md`](40_Kubernetes_Monitoring_Prometheus_Grafana_&_Helm.md) | Next: [`42_Terraform_Infrastructure_as_Code.md`](42_Terraform_Infrastructure_as_Code.md) →