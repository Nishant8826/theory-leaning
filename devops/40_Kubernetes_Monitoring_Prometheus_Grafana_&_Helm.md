# 40 – Kubernetes Monitoring: Prometheus, Grafana & Helm

---

## Table of Contents

1. [Why Monitoring is Non-Negotiable](#1-why-monitoring-is-non-negotiable)
2. [The Monitoring Tools Landscape](#2-the-monitoring-tools-landscape)
3. [Helm – The Kubernetes Package Manager](#3-helm--the-kubernetes-package-manager)
4. [Prometheus – The Metrics Database](#4-prometheus--the-metrics-database)
5. [Grafana – The Visualization Layer](#5-grafana--the-visualization-layer)
6. [Node Exporter & Kube State Metrics](#6-node-exporter--kube-state-metrics)
7. [The Full Monitoring Architecture](#7-the-full-monitoring-architecture)
8. [Step-by-Step Setup on GKE](#8-step-by-step-setup-on-gke)
9. [PromQL – Querying Prometheus](#9-promql--querying-prometheus)
10. [Grafana Dashboards & Alerts](#10-grafana-dashboards--alerts)
11. [Tech Stack Mapping](#11-tech-stack-mapping)
12. [Visual Diagrams](#12-visual-diagrams)
13. [Code & Practical Examples](#13-code--practical-examples)
14. [Scenario-Based Q&A](#14-scenario-based-qa)
15. [Interview Q&A](#15-interview-qa)

---

## 1. Why Monitoring is Non-Negotiable

### What
Monitoring is the practice of **continuously collecting, storing, and analyzing metrics** from your infrastructure and applications to understand their health, performance, and behavior in real time.

> 💡 **Analogy:** Monitoring a Kubernetes cluster is like a hospital's patient monitoring system. Without it, a doctor has to walk to each patient room and check vitals manually. With it, every patient's heart rate, blood pressure, and oxygen levels show on a central screen — and an alarm fires the moment something is abnormal. You don't wait for the patient to collapse; you act when the trend starts.

### Why

#### What Monitoring Tracks
```
Infrastructure Level:
  - CPU usage per node and pod
  - Memory consumption
  - Disk I/O and available space
  - Network throughput
  
Application Level:
  - Request latency (how slow is the API?)
  - Error rate (how many 5xx responses?)
  - Throughput (requests per second)
  - Pod restart count (is something crashing?)
  
Business Level:
  - Transaction success rate
  - Active users
  - Feature-specific metrics
```

#### The Three Monitoring Goals

| Goal | Without Monitoring | With Monitoring |
|------|-------------------|----------------|
| **Reactive** | Find out something broke when users complain | Get alerted within 30 seconds of a failure |
| **Proactive** | Disk fills up → system crashes → data lost | Alert at 80% disk → fix before crash |
| **Historical** | "Was it slow last Tuesday?" — no idea | Query exact latency for any past timestamp |

### Impact

| Without Monitoring | With Monitoring |
|-------------------|----------------|
| Outages discovered by angry users | Alerts fire before users notice |
| "It worked yesterday" with no data | "CPU spiked at 3:47 AM, here's the graph" |
| Disk fills silently → pod crash → data lost | Alert at 80% → action taken |
| Can't prove SLA compliance | Metrics prove 99.9% uptime |
| Blind deployment → hope it works | Know exactly what changed and its impact |
| Post-mortems are guesswork | Post-mortems have precise timelines |

### The DevOps Reality (from class)

> "Setting up this monitoring infrastructure represents 90% of DevOps work. Once set up, L1/L2 teams handle day-to-day monitoring and alerting. Most production outages are caused by human error, bad deployments, or poor monitoring — not platform failures. Kubernetes clusters themselves achieve 95-99.9% uptime."

---

## 2. The Monitoring Tools Landscape

### What
Multiple tools exist for monitoring. Understanding the landscape helps you choose the right tool and explain your choices in interviews.

### The Major Tools

#### Prometheus + Grafana ✅ (Industry Standard for Kubernetes)
- **Market share:** Used by ~90% of companies running Kubernetes
- **Prometheus:** Open-source metrics collection and storage (time-series database)
- **Grafana:** Open-source visualization and dashboarding
- **Why it dominates:** Native Kubernetes integration, free/open-source, massive community, scales well, PromQL is powerful

#### ELK Stack (Elasticsearch + Logstash + Kibana)
- **Elasticsearch:** Search and analytics engine (stores logs)
- **Logstash:** Log pipeline (collects, transforms, ships logs)
- **Kibana:** Visualization (like Grafana but for logs)
- **Best for:** Log analytics, full-text search in logs
- **Downside:** 3 separate components to maintain and scale — operationally complex. Resource-heavy.
- **In Kubernetes:** Often use EFK (replace Logstash with Fluentd — lighter weight)

#### Datadog (Commercial)
- **What:** SaaS monitoring platform — you send metrics to Datadog's cloud
- **Why:** Everything in one platform (metrics, logs, traces, APM), easy to set up
- **Cost:** Expensive at scale (~$23/host/month)
- **Best for:** Startups and enterprises that want managed monitoring without the ops overhead

#### Other Tools

| Tool | Best For | Notes |
|------|---------|-------|
| **Nagios** | Legacy infrastructure monitoring | Old but still used in enterprises |
| **Zabbix** | Enterprise on-premise monitoring | Free, complex setup |
| **AppDynamics** | Application performance monitoring (APM) | Cisco product, enterprise-grade |
| **Splunk** | Log management and security analytics | Very expensive, industry standard in finance/security |
| **New Relic** | APM + infrastructure monitoring | SaaS, similar to Datadog |

### Why Prometheus + Grafana Wins in Kubernetes

```
✅ Free and open-source
✅ Native Kubernetes integration (auto-discovers pods, services)
✅ Time-series database optimized for metrics
✅ Powerful query language (PromQL)
✅ Grafana has hundreds of pre-built dashboards
✅ AlertManager for routing alerts to Slack/PagerDuty/email
✅ Deployed inside the cluster — no data leaves
✅ CNCF project — long-term support guaranteed
```

---

## 3. Helm – The Kubernetes Package Manager

### What
**Helm** is the **package manager for Kubernetes** — it simplifies deploying complex applications (like Prometheus + Grafana + Node Exporter + kube-state-metrics) to Kubernetes with a single command instead of managing dozens of separate YAML files.

> 💡 **Analogy:**
> - **Linux without package manager:** Download nginx source code, compile it, manually configure systemd, manage dependencies yourself — hours of work
> - **Linux with APT:** `apt install nginx` → done in 30 seconds
>
> - **Kubernetes without Helm:** Write 20+ YAML files for Deployments, Services, ConfigMaps, RBAC, CRDs for Prometheus stack — days of work
> - **Kubernetes with Helm:** `helm install prometheus prometheus-community/kube-prometheus-stack` → done in 5 minutes

### Why Helm

```
Without Helm (installing Prometheus manually):
  - prometheus-deployment.yaml
  - prometheus-service.yaml
  - prometheus-configmap.yaml
  - prometheus-rbac.yaml
  - grafana-deployment.yaml
  - grafana-service.yaml
  - grafana-configmap.yaml
  - grafana-secret.yaml
  - node-exporter-daemonset.yaml
  - node-exporter-service.yaml
  - kube-state-metrics-deployment.yaml
  - alertmanager-deployment.yaml
  - ... (20+ more files)
  All need to be individually created, versioned, and maintained

With Helm:
  helm install prometheus prometheus-community/kube-prometheus-stack
  → Installs everything above in one command
  → Pre-configured, tested, production-ready
  → Upgrade: helm upgrade prometheus ...
  → Rollback: helm rollback prometheus 1
```

### Key Helm Terminology

| Term | Explanation | Analogy |
|------|-------------|---------|
| **Chart** | A Helm package — a collection of Kubernetes YAML templates | Like a .deb/.rpm package |
| **Release** | A deployed instance of a chart in a cluster | Like an installed application |
| **Repository** | A collection of charts (like Docker Hub for images) | Like APT/YUM repository |
| **Values** | Configuration parameters that customize a chart | Like configuration flags in apt |
| **Helm Hub / Artifact Hub** | The central registry for Helm charts | Like npmjs.com for Node.js |

### Helm Maintainers
- Maintained by **CNCF** (Cloud Native Computing Foundation)
- Major contributors: **Microsoft**, **Google**, **Bitnami**
- This backing ensures long-term stability and enterprise trust

### Core Helm Commands

```bash
# Add a chart repository
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts

# Update repository (like apt update)
helm repo update

# Search for available charts
helm search repo prometheus

# Install a chart (creates a release)
helm install RELEASE_NAME CHART_NAME

# List installed releases
helm list

# Upgrade an existing release
helm upgrade RELEASE_NAME CHART_NAME

# Rollback to previous version
helm rollback RELEASE_NAME REVISION_NUMBER

# Uninstall a release
helm uninstall RELEASE_NAME

# Get release status
helm status RELEASE_NAME

# See what a chart would deploy (dry run)
helm install --dry-run --debug RELEASE_NAME CHART_NAME

# Download chart values to customize
helm show values prometheus-community/kube-prometheus-stack > values.yaml
```

---

## 4. Prometheus – The Metrics Database

### What
**Prometheus** is an open-source **time-series database** specifically designed for storing metrics (numbers over time). It uses a **pull model** — instead of applications pushing metrics to Prometheus, Prometheus regularly goes out and "scrapes" (pulls) metrics from configured endpoints.

> 💡 **Analogy:** Prometheus is like a health inspector who regularly visits every restaurant (pod/node) on a schedule, checks specific measurements (temperature, hygiene score, headcount), and records them with a timestamp. The inspector doesn't wait for restaurants to report — they proactively go collect data.

### Why Prometheus

```
Traditional monitoring (push model):
  App → sends metrics → monitoring server
  Problem: If app is struggling, it might not send metrics
  Problem: Monitoring server gets overwhelmed with inbound connections

Prometheus (pull model):
  Prometheus → scrapes → /metrics endpoint on app
  Advantage: Prometheus controls the rate of data collection
  Advantage: If an app disappears, Prometheus detects it (no scrape = alert)
  Advantage: Apps just need to expose a /metrics HTTP endpoint
```

### How Prometheus Works

```
Step 1: Prometheus is configured with "scrape configs"
        → "Scrape every pod in namespace X on port 9090/metrics"
        → "Scrape every node via node-exporter on port 9100/metrics"

Step 2: Every 15 seconds (default), Prometheus calls each /metrics endpoint
        GET http://pod-ip:9090/metrics
        
Step 3: The response is a text format:
        # HELP http_requests_total Total HTTP requests
        # TYPE http_requests_total counter
        http_requests_total{method="GET",status="200"} 1234
        http_requests_total{method="POST",status="500"} 5
        
Step 4: Prometheus stores this as time-series data in its TSDB (Time Series Database)
        Key: http_requests_total{method="GET",status="200"}
        Values: [t=1000: 1234] [t=1015: 1256] [t=1030: 1289] ...

Step 5: AlertManager watches for rules:
        IF http_requests_total{status="500"} > 100 → fire alert → Slack/email
```

### Prometheus Storage Format

```
Time-Series: metric_name{label1="value1", label2="value2"} = float64

Examples:
  cpu_usage_percent{node="node-1", pod="api-xxx"} = 45.2
  memory_bytes_used{namespace="production"} = 2147483648
  http_requests_total{method="GET", status_code="200"} = 58234
  pod_restart_count{pod="payment-service-xxx"} = 3
  
Each data point: (timestamp, float64 value)
Data stored compressed on disk
Default retention: 15 days (configurable)
```

### Prometheus Components

| Component | Role |
|-----------|------|
| **Prometheus Server** | Scrapes, stores, and queries metrics |
| **AlertManager** | Routes alerts to Slack, PagerDuty, email |
| **Pushgateway** | For short-lived jobs that can't be scraped |
| **Node Exporter** | Exposes Linux host metrics (CPU, memory, disk) |
| **Kube State Metrics** | Exposes Kubernetes object state as metrics |

---

## 5. Grafana – The Visualization Layer

### What
**Grafana** is an open-source **data visualization and dashboarding platform**. It connects to data sources (like Prometheus) and displays the data as beautiful, interactive graphs, charts, and alerts.

> 💡 **Analogy:** Prometheus is like a hospital's medical data system — it stores all patient measurements as raw numbers. Grafana is the doctor's dashboard — it turns those numbers into clear graphs, trends, and color-coded alerts that a doctor (or DevOps engineer) can understand at a glance.

### Why Grafana (Not Just Prometheus's Built-in UI)

```
Prometheus UI:
  - Basic query interface
  - Simple graphs
  - No dashboards
  - No team collaboration features

Grafana:
  - Beautiful, customizable dashboards
  - Multiple panels per dashboard
  - Team collaboration (share dashboards)
  - Multiple data sources (Prometheus + Loki + CloudWatch all in one)
  - Pre-built community dashboards (hundreds available)
  - Alerting with notification channels
  - Role-based access (viewer, editor, admin)
```

### How Grafana Works

```
Step 1: Grafana connects to Prometheus as a "Data Source"
        URL: http://prometheus-operated:9090  (in-cluster DNS)

Step 2: You create a Panel with a PromQL query:
        rate(http_requests_total[5m])  ← requests per second over 5 minutes

Step 3: Grafana runs the query against Prometheus every 30 seconds

Step 4: Prometheus returns time-series data points

Step 5: Grafana renders this as a line graph, gauge, bar chart, etc.

Step 6: Multiple panels grouped into a Dashboard
        Dashboard: "Kubernetes Cluster Overview"
          - Panel: CPU usage per node (line chart)
          - Panel: Memory usage (gauge)
          - Panel: Pod restart count (bar chart)
          - Panel: HTTP error rate (stat panel)
```

### Pre-Built Dashboards
Grafana has a community library at **grafana.com/grafana/dashboards** with thousands of pre-built dashboards. Import by Dashboard ID:

| Dashboard | ID | What it Shows |
|-----------|-----|--------------|
| Kubernetes Cluster Overview | 7249 | Nodes, pods, namespaces overview |
| Node Exporter Full | 1860 | Detailed host metrics (CPU, disk, network) |
| Kubernetes Pod Monitoring | 6336 | Per-pod CPU, memory, restarts |
| NGINX Ingress Controller | 9614 | Request rates, errors, latency |
| Spring Boot Statistics | 12685 | JVM, HTTP, database metrics |
| Node.js Application | 11159 | Event loop lag, heap, requests |

### Access Details (from Class)
```
URL:      http://GRAFANA_EXTERNAL_IP:3000
Username: admin
Password: prom-operator  ← retrieved from Kubernetes secret
```

---

## 6. Node Exporter & Kube State Metrics

### Node Exporter

#### What
**Node Exporter** is a Prometheus exporter that runs on every Kubernetes node (as a DaemonSet — one pod per node). It exposes Linux host-level metrics via an HTTP endpoint at `:9100/metrics`.

#### What It Exposes
```
node_cpu_seconds_total          ← CPU usage by mode (user, system, idle)
node_memory_MemAvailable_bytes  ← Available RAM
node_filesystem_avail_bytes     ← Available disk space
node_network_receive_bytes_total ← Network ingress
node_load1                      ← 1-minute load average
node_disk_io_now                ← Current disk I/O operations
```

#### Why It's a DaemonSet
A DaemonSet ensures exactly ONE pod runs on EVERY node. Node Exporter needs to run on every node because each node has different hardware metrics.

---

### Kube State Metrics

#### What
**Kube State Metrics (KSM)** is a service that talks to the Kubernetes API server and exposes the current state of Kubernetes objects as Prometheus metrics.

#### What It Exposes
```
kube_pod_status_phase                    ← Is a pod Running/Pending/Failed?
kube_deployment_status_replicas_ready    ← How many deployment replicas are ready?
kube_node_status_condition               ← Is a node Ready?
kube_pod_container_resource_limits       ← What are the resource limits?
kube_hpa_status_current_replicas         ← How many HPA replicas currently?
kube_persistentvolumeclaim_status_phase  ← Is PVC bound?
```

#### Node Exporter vs Kube State Metrics

| | Node Exporter | Kube State Metrics |
|--|--------------|-------------------|
| **What it monitors** | Physical node/host | Kubernetes objects |
| **Metrics type** | Infrastructure (CPU, RAM, disk) | Cluster state (pod status, deployment health) |
| **Data source** | Linux kernel | Kubernetes API |
| **Runs as** | DaemonSet (one per node) | Single Deployment |
| **Example metric** | Node CPU = 45% | Deployment ready replicas = 2/3 |

Together, Node Exporter + KSM + Prometheus gives you complete visibility into both the infrastructure AND the Kubernetes layer.

---

## 7. The Full Monitoring Architecture

### How All Components Connect

```
KUBERNETES CLUSTER (monitoring namespace)
│
├── Prometheus Server (Deployment)
│     │ Every 15s: scrapes metrics from:
│     ├────────────────────────────────────────
│     │ ← Node Exporter (port 9100 on each node)
│     │   Infrastructure: CPU, RAM, disk, network
│     │
│     ├── Kube State Metrics (port 8080)
│     │   K8s state: pod status, deployment health
│     │
│     ├── App pods with /metrics endpoint
│     │   Application: request rate, errors, latency
│     │
│     └── Prometheus itself (self-monitoring)
│
├── AlertManager (receives alerts from Prometheus)
│     └── Routes to: Slack, PagerDuty, Email, Webhooks
│
├── Grafana (Deployment, port 3000)
│     │ Queries Prometheus for data (PromQL)
│     └── Serves dashboards to DevOps engineers
│
└── Persistent Volumes (for Prometheus & Grafana data)
      └── Data survives pod restarts ✅
```

### Data Flow

```
Physical Node
    │
    │ CPU/memory/disk stats from Linux kernel
    ▼
Node Exporter pod (port 9100)
    │
    │ GET /metrics (every 15s)
    ▼
Prometheus Server (stores as time-series)
    │
    │ PromQL query: node_cpu_seconds_total
    ▼
Grafana (renders as graph)
    │
    │ HTTP (browser)
    ▼
DevOps Engineer sees: "Node-2 CPU is at 80%"
    │
    │ (if alert rule configured)
    ▼
AlertManager → Slack: "⚠️ Node-2 CPU > 75% for 5 minutes"
```

---

## 8. Step-by-Step Setup on GKE

### Prerequisites
- GKE cluster running (3 nodes, 2 CPU, 8 GB RAM per node — per class)
- kubectl configured and connected
- Helm installed

### Step 1: Install Helm

```bash
# On Linux / Cloud Shell (one-liner)
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Verify
helm version
# version.BuildInfo{Version:"v3.x.x", ...}
```

### Step 2: Create Monitoring Namespace

```bash
# Isolation best practice — keep monitoring separate
kubectl create namespace monitoring

# Verify
kubectl get ns
```

### Step 3: Add Prometheus Community Helm Repository

```bash
# Add the repository
helm repo add prometheus-community \
  https://prometheus-community.github.io/helm-charts

# Update to get latest chart versions (like apt update)
helm repo update

# Verify repository added
helm repo list
# NAME                    URL
# prometheus-community    https://prometheus-community.github.io/helm-charts

# Search available charts
helm search repo prometheus-community
```

### Step 4: Install kube-prometheus-stack

The `kube-prometheus-stack` is the all-in-one chart that installs:
- Prometheus Operator
- Prometheus Server
- AlertManager
- Node Exporter (DaemonSet on every node)
- Kube State Metrics
- Grafana
- Pre-built dashboards
- Pre-configured alerts

```bash
# Install the full monitoring stack
helm install prometheus \
  prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace

# This takes 2-3 minutes — watch pods starting:
kubectl get pods -n monitoring -w

# Expected pods when complete:
# alertmanager-prometheus-kube-prometheus-alertmanager-0   2/2   Running
# prometheus-grafana-xxxxx                                  3/3   Running
# prometheus-kube-prometheus-operator-xxxxx                 1/1   Running
# prometheus-kube-state-metrics-xxxxx                       1/1   Running
# prometheus-prometheus-kube-prometheus-prometheus-0        2/2   Running
# prometheus-prometheus-node-exporter-xxxxx (×3 nodes)     1/1   Running
```

### Step 5: Expose Grafana as LoadBalancer

```bash
# By default, Grafana is ClusterIP (internal only)
# Expose it to the internet:
kubectl patch svc prometheus-grafana \
  -n monitoring \
  -p '{"spec": {"type": "LoadBalancer"}}'

# Watch for external IP to be assigned
kubectl get svc prometheus-grafana -n monitoring -w
# NAME                  TYPE           CLUSTER-IP    EXTERNAL-IP   PORT(S)
# prometheus-grafana    LoadBalancer   10.x.x.x      34.x.x.x      80:xxxxx/TCP
```

### Step 6: Get Grafana Admin Password

```bash
# The password is stored in a Kubernetes secret
kubectl get secret \
  prometheus-grafana \
  -n monitoring \
  -o jsonpath="{.data.admin-password}" | base64 --decode ; echo

# OR using the class approach (password was "prom-operator"):
kubectl get secret \
  prometheus-grafana \
  -n monitoring \
  -o yaml
# Look for admin-password field (base64 encoded)
```

### Step 7: Access Grafana

```bash
# Get external IP
GRAFANA_IP=$(kubectl get svc prometheus-grafana -n monitoring \
  -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

echo "Grafana URL: http://$GRAFANA_IP"
# Username: admin
# Password: prom-operator (or from secret)
```

### Step 8: Verify Prometheus is Collecting Metrics

```bash
# Port-forward Prometheus for local access
kubectl port-forward svc/prometheus-kube-prometheus-prometheus \
  9090:9090 \
  -n monitoring

# Open: http://localhost:9090
# Go to: Status → Targets (should show all scrape targets as UP)
```

### Complete Helm Monitoring Setup Script

```bash
#!/bin/bash
# One-script setup for Prometheus + Grafana on GKE

# Prerequisites check
command -v kubectl >/dev/null || { echo "kubectl required"; exit 1; }
command -v helm >/dev/null || {
  echo "Installing Helm..."
  curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
}

# Setup monitoring namespace
kubectl create namespace monitoring --dry-run=client -o yaml | kubectl apply -f -

# Add and update repo
helm repo add prometheus-community \
  https://prometheus-community.github.io/helm-charts
helm repo update

# Install kube-prometheus-stack
helm install prometheus \
  prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --wait  # Wait until all pods are ready before returning

# Expose Grafana
kubectl patch svc prometheus-grafana \
  -n monitoring \
  -p '{"spec": {"type": "LoadBalancer"}}'

# Wait for external IP
echo "Waiting for Grafana external IP..."
until kubectl get svc prometheus-grafana -n monitoring \
  -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null | grep -q .; do
  sleep 5
done

GRAFANA_IP=$(kubectl get svc prometheus-grafana -n monitoring \
  -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

GRAFANA_PASS=$(kubectl get secret prometheus-grafana -n monitoring \
  -o jsonpath="{.data.admin-password}" | base64 --decode)

echo ""
echo "✅ Monitoring stack deployed!"
echo "   Grafana URL:      http://$GRAFANA_IP"
echo "   Username:         admin"
echo "   Password:         $GRAFANA_PASS"
```

---

## 9. PromQL – Querying Prometheus

### What
**PromQL** (Prometheus Query Language) is the query language used to retrieve and transform metrics stored in Prometheus. You use it in Grafana panels, Prometheus UI, and alert rules.

### Basic PromQL Concepts

#### Instant Vector (current value)
```promql
# Current CPU usage across all containers
container_cpu_usage_seconds_total

# Filter to specific namespace
container_cpu_usage_seconds_total{namespace="production"}

# Filter to specific pod
container_cpu_usage_seconds_total{pod="my-app-xxx"}
```

#### Range Vector (values over time window)
```promql
# CPU usage over the last 5 minutes
container_cpu_usage_seconds_total[5m]
```

#### Functions (most important)
```promql
# Rate: per-second rate over time window (for counters)
rate(http_requests_total[5m])
# = how many HTTP requests per second, averaged over last 5 min

# Increase: total increase over time window
increase(http_requests_total[1h])
# = how many requests in the last hour

# Sum: aggregate across all labels
sum(rate(http_requests_total[5m]))

# Sum by label: group results
sum(rate(http_requests_total[5m])) by (namespace)

# Average
avg(container_memory_usage_bytes) by (pod)

# Max
max(node_cpu_seconds_total{mode="user"}) by (node)
```

### Essential PromQL Queries for DevOps

```promql
# === NODE METRICS ===

# CPU usage % per node
100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# Available memory per node (GB)
node_memory_MemAvailable_bytes / 1024 / 1024 / 1024

# Disk usage % per node
(1 - node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"}) * 100

# === POD METRICS ===

# CPU usage per pod (millicores)
rate(container_cpu_usage_seconds_total{container!=""}[5m]) * 1000

# Memory usage per pod (MB)
container_memory_usage_bytes{container!=""} / 1024 / 1024

# Pod restart count
kube_pod_container_status_restarts_total

# === APPLICATION METRICS ===

# HTTP request rate per second
rate(http_requests_total[5m])

# HTTP error rate (5xx)
rate(http_requests_total{status=~"5.."}[5m])

# 95th percentile request latency
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# === CLUSTER HEALTH ===

# Number of pods not running
kube_pod_status_phase{phase!="Running"} == 1

# Deployment replicas not ready
kube_deployment_status_replicas_ready < kube_deployment_spec_replicas

# HPA current replicas
kube_horizontalpodautoscaler_status_current_replicas
```

---

## 10. Grafana Dashboards & Alerts

### Importing Pre-Built Dashboards

```
Grafana UI:
  Left Sidebar → Dashboards → Import
  
  Option 1: Enter Dashboard ID (from grafana.com/dashboards)
    ID: 1860   ← Node Exporter Full
    Click: Load → Select Prometheus data source → Import
    
  Option 2: Upload JSON file
    Download JSON from grafana.com → Upload → Import
```

### Creating a Custom Dashboard

```
Grafana UI:
  Dashboards → New Dashboard → Add Panel

  Panel Editor:
    Title: "Production Pod CPU Usage"
    
    Query (PromQL):
      rate(container_cpu_usage_seconds_total{
        namespace="production",
        container!=""
      }[5m]) * 1000
      
    Visualization: Time series (line graph)
    Unit: millicores
    
    Save Panel → Save Dashboard
```

### Setting Up Prometheus Alerts

Alerts are defined in Prometheus as rules in YAML. When a condition is met for a duration, AlertManager fires the alert.

```yaml
# custom-alerts.yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: custom-alerts
  namespace: monitoring
spec:
  groups:
  - name: cluster-alerts
    rules:
    
    # Alert when pod keeps restarting
    - alert: PodCrashLooping
      expr: rate(kube_pod_container_status_restarts_total[15m]) * 60 * 15 > 0
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "Pod {{ $labels.pod }} is crash-looping"
        description: "Pod {{ $labels.pod }} in namespace {{ $labels.namespace }} is restarting"

    # Alert when node CPU is high
    - alert: NodeHighCPU
      expr: |
        100 - (avg by(instance) 
          (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
      for: 10m
      labels:
        severity: critical
      annotations:
        summary: "High CPU on {{ $labels.instance }}"
        description: "Node {{ $labels.instance }} CPU > 80% for 10 minutes"

    # Alert when disk is almost full
    - alert: NodeDiskAlmostFull
      expr: |
        (1 - node_filesystem_avail_bytes{mountpoint="/"} / 
          node_filesystem_size_bytes{mountpoint="/"}) * 100 > 85
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "Disk almost full on {{ $labels.instance }}"

    # Alert when a deployment has unavailable replicas
    - alert: DeploymentUnavailable
      expr: kube_deployment_status_replicas_unavailable > 0
      for: 5m
      labels:
        severity: critical
      annotations:
        summary: "Deployment {{ $labels.deployment }} has unavailable replicas"
```

```bash
kubectl apply -f custom-alerts.yaml
```

### Configuring AlertManager for Slack

```yaml
# alertmanager-config.yaml
apiVersion: monitoring.coreos.com/v1alpha1
kind: AlertmanagerConfig
metadata:
  name: slack-config
  namespace: monitoring
spec:
  route:
    receiver: slack-notifications
    groupWait: 30s
    groupInterval: 5m
    repeatInterval: 12h
  receivers:
  - name: slack-notifications
    slackConfigs:
    - apiURL:
        name: slack-webhook-secret
        key: webhookURL
      channel: '#devops-alerts'
      title: '{{ range .Alerts }}{{ .Annotations.summary }}{{ end }}'
      text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'
      sendResolved: true
```

---

## 11. Tech Stack Mapping

### Complete Monitoring Architecture for a Real Application

```
User Traffic
     │
     ▼
React/Next.js Frontend (Pods)
  Metrics: page load time, JS errors
     │
     ▼
Node.js API (Pods)
  Metrics: request rate, error rate, latency
  Custom metrics via prom-client library
     │
     ├── PostgreSQL (StatefulSet)
     │   Metrics: query time, connections, cache hit ratio
     │   via: postgres-exporter
     │
     ├── Redis (StatefulSet)
     │   Metrics: memory usage, hit rate, connections
     │   via: redis-exporter
     │
     └── AWS S3 (external)
         Metrics: via CloudWatch + cloudwatch-exporter
         
ALL → scraped by Prometheus → visualized in Grafana
```

### Monitoring Per Technology

| Technology | How to Instrument | Prometheus Exporter |
|-----------|------------------|-------------------|
| **Node.js** | `prom-client` npm package | Built into app |
| **Spring Boot** | `spring-boot-actuator + micrometer` | Built into app |
| **PostgreSQL** | — | `postgres-exporter` |
| **MongoDB** | — | `mongodb-exporter` |
| **Redis** | — | `redis-exporter` |
| **NGINX** | — | `nginx-vts-exporter` |
| **Kubernetes nodes** | — | `node-exporter` (in kube-prometheus-stack) |
| **K8s objects** | — | `kube-state-metrics` (in kube-prometheus-stack) |
| **AWS services** | CloudWatch → | `cloudwatch-exporter` |

---

## 12. Visual Diagrams

### Diagram 1: Full Monitoring Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                  KUBERNETES CLUSTER                           │
│                  namespace: monitoring                        │
│                                                               │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │                  PROMETHEUS                             │  │
│  │            (Time-Series Database)                       │  │
│  │                                                         │  │
│  │  Scrapes every 15 seconds from:                        │  │
│  │  ┌──────────────┐  ┌─────────────────┐                 │  │
│  │  │ Node Exporter│  │ Kube State      │                 │  │
│  │  │ (each node)  │  │ Metrics         │                 │  │
│  │  │ CPU,RAM,disk │  │ pod/deploy state│                 │  │
│  │  └──────────────┘  └─────────────────┘                 │  │
│  │  ┌────────────────────────────────────┐                 │  │
│  │  │    App Pods (/metrics endpoints)   │                 │  │
│  │  │  Node.js, Spring Boot, Python, etc.│                 │  │
│  │  └────────────────────────────────────┘                 │  │
│  └──────────────────────────┬──────────────────────────────┘  │
│                             │ PromQL queries                   │
│  ┌──────────────────────────▼──────────────────────────────┐  │
│  │                    GRAFANA                              │  │
│  │              (port 3000, LoadBalancer)                  │  │
│  │                                                         │  │
│  │  Dashboard 1: Cluster Overview                          │  │
│  │  Dashboard 2: Node Exporter Full                        │  │
│  │  Dashboard 3: Application Metrics                       │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │              ALERTMANAGER                               │  │
│  │  Receives alerts from Prometheus                        │  │
│  │  Routes to: Slack /#devops-alerts                       │  │
│  │             PagerDuty (on-call)                         │  │
│  │             Email (team@company.com)                    │  │
│  └─────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────┘
```

---

### Diagram 2: Helm Chart Analogy

```
LINUX (APT)                            KUBERNETES (HELM)
────────────                           ─────────────────
Repository: apt.ubuntu.com             Repository: prometheus-community.github.io

apt update                             helm repo update
apt install nginx                      helm install prometheus kube-prometheus-stack
apt list --installed                   helm list
apt upgrade nginx                      helm upgrade prometheus ...
apt remove nginx                       helm uninstall prometheus
apt show nginx                         helm show chart kube-prometheus-stack

Package (.deb)                         Chart (folder of YAML templates)
Installed program                      Helm Release (running in cluster)

One command → installs nginx with      One command → installs Prometheus +
all dependencies configured            Grafana + Node Exporter + Alertmanager
```

---

### Diagram 3: Prometheus Scrape Flow

```
t=0s                    t=15s                   t=30s
 │                        │                       │
 ├─► GET /metrics         ├─► GET /metrics         ├─► GET /metrics
 │   node-exporter        │   node-exporter        │   node-exporter
 │   (all 3 nodes)        │   (all 3 nodes)        │   (all 3 nodes)
 │                        │                        │
 │   Response:            │   Response:             │   Response:
 │   cpu=0.43             │   cpu=0.61              │   cpu=0.58
 │   memory=0.72          │   memory=0.73           │   memory=0.74
 │                        │                        │
 ▼                        ▼                        ▼
Stored in TSDB          Stored in TSDB           Stored in TSDB
  [(t=0, 0.43),          [(t=15, 0.61),           [(t=30, 0.58),
   (t=0, 0.72)]          (t=15, 0.73)]             (t=30, 0.74)]

Grafana asks: "Show me CPU for last 30 seconds"
Prometheus returns all 3 data points → Grafana draws the line graph
```

---

### Diagram 4: Node Exporter vs Kube State Metrics

```
NODE EXPORTER (one per node)            KUBE STATE METRICS (one deployment)
────────────────────────────            ─────────────────────────────────────
Talks to: Linux Kernel                  Talks to: Kubernetes API Server

Reports:                                Reports:
  CPU usage %                             Pod status (Running/Pending/Failed)
  Memory available bytes                  Deployment ready replicas
  Disk I/O                               Node conditions
  Network packets in/out                 HPA current replicas
  Load average                           PVC binding status

Example metric:                         Example metric:
  node_cpu_seconds_total{               kube_pod_status_phase{
    mode="user"                           namespace="production",
  } = 2345.67                             pod="api-xxx",
                                          phase="Running"
"How hard is the physical           } = 1
 hardware working?"
                                    "What is the state of my
                                     Kubernetes objects?"
```

---

### Diagram 5: Alert Flow

```
Prometheus Rule:
  "IF CPU > 80% for 10 minutes → fire NodeHighCPU alert"
                │
                │ condition met
                ▼
        PROMETHEUS fires alert
                │
                ▼
        ALERTMANAGER receives it
                │
          ┌─────┴──────┐
          ▼            ▼
      Slack         PagerDuty
  /#devops-alerts   (on-call)
  
  "⚠️ ALERT: NodeHighCPU
   Node: node-2.us-central1
   CPU: 87% for 12 minutes
   Dashboard: http://grafana.../..."
```

---

## 13. Code & Practical Examples

### Example 1: Custom Helm Values for kube-prometheus-stack

```yaml
# custom-values.yaml
# Override defaults in kube-prometheus-stack

grafana:
  adminPassword: "YourSecurePassword123"
  service:
    type: LoadBalancer
    port: 3000
  persistence:
    enabled: true
    size: 10Gi
    storageClassName: standard

prometheus:
  prometheusSpec:
    retention: 30d            # Keep 30 days of metrics
    storageSpec:
      volumeClaimTemplate:
        spec:
          storageClassName: standard
          resources:
            requests:
              storage: 50Gi  # Disk for metrics storage
    additionalScrapeConfigs:
    - job_name: 'my-node-app'
      static_configs:
      - targets: ['node-api-service:3001']  # Scrape custom app

alertmanager:
  config:
    global:
      slack_api_url: 'https://hooks.slack.com/services/XXX/YYY/ZZZ'
    route:
      receiver: 'slack-notifications'
    receivers:
    - name: 'slack-notifications'
      slack_configs:
      - channel: '#alerts'
        title: 'Kubernetes Alert'

nodeExporter:
  enabled: true    # Install on all nodes (default: true)

kubeStateMetrics:
  enabled: true    # Monitor K8s object state (default: true)
```

```bash
# Install with custom values
helm install prometheus \
  prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  -f custom-values.yaml
```

---

### Example 2: Adding Custom Metrics to a Node.js App

```javascript
// metrics.js — Add Prometheus metrics to Node.js
const client = require('prom-client');

// Auto-collect default Node.js metrics (event loop, memory, CPU)
client.collectDefaultMetrics({ timeout: 5000 });

// Custom counter: count HTTP requests
const httpRequestsTotal = new client.Counter({
  name: 'http_requests_total',
  help: 'Total number of HTTP requests',
  labelNames: ['method', 'route', 'status_code']
});

// Custom histogram: track request duration
const httpRequestDuration = new client.Histogram({
  name: 'http_request_duration_seconds',
  help: 'HTTP request duration in seconds',
  labelNames: ['method', 'route'],
  buckets: [0.01, 0.05, 0.1, 0.3, 0.5, 1, 2, 5]
});

// Gauge: current active connections
const activeConnections = new client.Gauge({
  name: 'active_connections',
  help: 'Number of active connections'
});

module.exports = {
  httpRequestsTotal,
  httpRequestDuration,
  activeConnections,
  register: client.register
};
```

```javascript
// server.js — Express app with metrics endpoint
const express = require('express');
const metrics = require('./metrics');

const app = express();

// Middleware: track all requests
app.use((req, res, next) => {
  const end = metrics.httpRequestDuration.startTimer({
    method: req.method,
    route: req.path
  });
  
  res.on('finish', () => {
    metrics.httpRequestsTotal.labels(
      req.method,
      req.path,
      res.statusCode.toString()
    ).inc();
    end();
  });
  next();
});

// Metrics endpoint — Prometheus scrapes this
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', metrics.register.contentType);
  res.end(await metrics.register.metrics());
});

// Your app routes
app.get('/api/products', (req, res) => {
  res.json({ products: [] });
});
```

---

### Example 3: ServiceMonitor – Tell Prometheus to Scrape Your App

```yaml
# servicemonitor.yaml
# Tells Prometheus to scrape your Node.js app's /metrics endpoint

apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: node-api-monitor
  namespace: monitoring            # Must be in monitoring namespace
  labels:
    release: prometheus            # Must match Prometheus's serviceMonitorSelector
spec:
  namespaceSelector:
    matchNames:
    - production                   # Scrape services in 'production' namespace
  selector:
    matchLabels:
      app: node-api                # Select the node-api service
  endpoints:
  - port: metrics                  # Port name in the Service
    path: /metrics
    interval: 15s                  # Scrape every 15 seconds
```

```yaml
# The Service needs a named port for the ServiceMonitor to reference:
apiVersion: v1
kind: Service
metadata:
  name: node-api-service
  namespace: production
  labels:
    app: node-api
spec:
  selector:
    app: node-api
  ports:
  - name: http
    port: 3000
    targetPort: 3000
  - name: metrics          # Named port referenced by ServiceMonitor
    port: 3001
    targetPort: 3001
```

---

### Example 4: Jenkins Pipeline – Deploy App + Set Up Monitoring

```groovy
pipeline {
    agent any

    environment {
        APP           = "node-api"
        NAMESPACE     = "production"
        MON_NAMESPACE = "monitoring"
    }

    stages {

        stage('Deploy Application') {
            steps {
                sh """
                    kubectl apply -f k8s/deployment.yaml -n ${NAMESPACE}
                    kubectl apply -f k8s/service.yaml -n ${NAMESPACE}
                    kubectl rollout status deployment/${APP} -n ${NAMESPACE}
                """
            }
        }

        stage('Apply Monitoring Config') {
            steps {
                sh """
                    # ServiceMonitor tells Prometheus to scrape the app
                    kubectl apply -f k8s/servicemonitor.yaml -n ${MON_NAMESPACE}

                    # Custom alert rules
                    kubectl apply -f k8s/alerts.yaml -n ${MON_NAMESPACE}

                    echo "✅ Monitoring configured for ${APP}"
                """
            }
        }

        stage('Verify Metrics') {
            steps {
                sh """
                    # Port-forward Prometheus to verify scraping
                    kubectl port-forward svc/prometheus-kube-prometheus-prometheus \
                      9090:9090 -n ${MON_NAMESPACE} &
                    PF_PID=$!
                    sleep 5

                    # Check if our app's metrics endpoint is being scraped
                    curl -s http://localhost:9090/api/v1/targets | \
                      python3 -c "
                    import json, sys
                    data = json.load(sys.stdin)
                    targets = data['data']['activeTargets']
                    app_targets = [t for t in targets if '${APP}' in str(t)]
                    print(f'Found {len(app_targets)} target(s) for ${APP}')
                    for t in app_targets:
                      print(f'  Health: {t[\"health\"]}')
                    "
                    kill $PF_PID
                """
            }
        }
    }
}
```

---

## 14. Scenario-Based Q&A

---

🔍 **Scenario 1:** At 2 AM, your Node.js API starts returning 503 errors. Users are affected. You have Prometheus + Grafana monitoring. Walk through your investigation.

✅ **Answer:** (1) Open Grafana → Application dashboard → look at the HTTP error rate panel: `rate(http_requests_total{status=~"5.."}[5m])` — you see errors spiked at 2:03 AM; (2) Check the request rate panel — requests are normal, not a traffic spike; (3) Check pod restart count panel — you see `payment-service` had 3 restarts in 5 minutes; (4) Switch to the Node panel — Node-2 shows memory at 95%; (5) Root cause: payment-service pods are OOMKilled on Node-2. Memory limit is too low for current load; (6) Immediate fix: `kubectl set resources deployment/payment-service --limits=memory=512Mi -n production`; (7) Alert rule to add: alert when pod restarts > 2 in 15 minutes. The entire investigation took 3 minutes because of monitoring.

---

🔍 **Scenario 2:** Your manager asks "Why are we spending time setting up Prometheus and Grafana? Can't we just use `kubectl get pods` to monitor the cluster?"

✅ **Answer:** `kubectl get pods` shows current state — it only tells you what's running RIGHT NOW. It can't tell you what was happening at 3 AM when the slowness occurred, whether CPU was trending upward over the past week, which specific pod started consuming excessive memory before it crashed, or whether your 99.9% uptime SLA is actually being met. Prometheus stores time-series data — you can query exactly what happened at any past timestamp. Grafana visualizes trends, correlations, and anomalies that are invisible in text output. AlertManager tells you about problems BEFORE users notice. `kubectl get pods` is like looking out the window to check weather; Prometheus + Grafana is a full weather station with historical data and storm predictions.

---

🔍 **Scenario 3:** After installing kube-prometheus-stack with Helm, you run `kubectl get pods -n monitoring` and see one pod stuck in `Pending`. How do you troubleshoot?

✅ **Answer:** Run `kubectl describe pod <pending-pod> -n monitoring` and check the Events section. Common causes: (1) **Insufficient resources** — Events show "Insufficient memory/CPU" → your nodes (2 CPU, 4GB each) may not have enough headroom after other workloads. Prometheus needs ~500MB RAM minimum. Solution: use 8GB RAM nodes (as in class config) or reduce Prometheus resource requests in values.yaml; (2) **PVC not bound** — if Prometheus persistence is enabled but no StorageClass exists → `kubectl get pvc -n monitoring` → check status; (3) **Node affinity** — check if the chart has nodeSelector that doesn't match any nodes. Run `helm get values prometheus -n monitoring` to see the configuration.

---

🔍 **Scenario 4:** You deploy a new Node.js microservice. Your team wants it monitored in Grafana automatically. What do you set up?

✅ **Answer:** Three steps: (1) **Instrument the app** — add `prom-client` npm package, expose a `/metrics` endpoint returning Prometheus-format metrics (request count, duration, errors, custom business metrics); (2) **Create a ServiceMonitor** — a Kubernetes object telling Prometheus to scrape your service's `/metrics` endpoint every 15 seconds. Apply it to the monitoring namespace with the right selector labels; (3) **Import or create a Grafana dashboard** — either import a community Node.js dashboard (e.g., ID: 11159) or create a custom one with PromQL queries for your specific metrics. The kube-prometheus-stack Prometheus Operator automatically discovers ServiceMonitor objects and starts scraping — no manual Prometheus config needed.

---

🔍 **Scenario 5:** Disk space on your Prometheus PV is filling up rapidly. You have 30 days of retention configured. What are your options?

✅ **Answer:** Three approaches: (1) **Increase PV size** — if the storage class supports online expansion: `kubectl edit pvc prometheus-db-prometheus-0 -n monitoring` and increase the storage size. GCP's standard StorageClass supports this; (2) **Reduce retention** — update Helm values: `prometheus.prometheusSpec.retention: 15d` and `helm upgrade prometheus prometheus-community/kube-prometheus-stack -n monitoring -f values.yaml`; (3) **Add remote storage** — configure Prometheus to write to AWS Thanos or Cortex for long-term storage, keeping only recent data locally; (4) **Reduce scrape frequency** — change interval from 15s to 30s for non-critical metrics. Most important: this is why you set up monitoring for your monitoring — alert when Prometheus PV disk usage exceeds 70%.

---

🔍 **Scenario 6:** An interviewer asks you to describe the Prometheus + Grafana monitoring stack and how it works. How do you answer clearly and confidently?

✅ **Answer:** "Prometheus is an open-source time-series database that periodically scrapes metrics from configured endpoints — it pulls data rather than waiting for apps to push it. It stores metrics as key-value pairs with timestamps. Node Exporter is deployed as a DaemonSet to expose Linux host metrics from every node — CPU, memory, disk. Kube State Metrics exposes Kubernetes object state like pod status and deployment health. All this flows into Prometheus, which stores it and evaluates alerting rules via AlertManager. Grafana connects to Prometheus as a data source and visualizes the metrics using PromQL queries on customizable dashboards. The whole stack is deployed to Kubernetes using Helm — specifically the `kube-prometheus-stack` chart — which sets everything up with pre-built dashboards and alerts in a single command. In production, you'd expose Grafana via a LoadBalancer and configure AlertManager to send notifications to Slack or PagerDuty when thresholds are breached."

---

## 15. Interview Q&A

---

**Q1. What is Helm and why is it used in Kubernetes?**

**A:** Helm is the package manager for Kubernetes — it simplifies deploying complex applications by packaging all required Kubernetes resources (Deployments, Services, ConfigMaps, RBAC, etc.) into a single reusable unit called a **chart**. Instead of managing 20+ individual YAML files for a monitoring stack, one command — `helm install prometheus prometheus-community/kube-prometheus-stack` — deploys Prometheus, Grafana, AlertManager, Node Exporter, and Kube State Metrics, all pre-configured. Helm also handles upgrades (`helm upgrade`), rollbacks (`helm rollback`), and configuration through values files. It's maintained by CNCF with contributions from Microsoft, Google, and Bitnami. The analogy: Helm is to Kubernetes what APT/YUM is to Linux — you don't compile nginx from source; you `apt install nginx`. You don't write 20 YAML files for Prometheus; you `helm install prometheus ...`.

---

**Q2. What is Prometheus and how does it differ from traditional monitoring tools like Nagios?**

**A:** Prometheus is an open-source time-series database built specifically for cloud-native environments. Key differences from Nagios: (1) **Pull vs Push**: Prometheus actively scrapes metrics from targets every 15 seconds; Nagios relies on agents pushing data or running checks. Pull is more resilient — if a service disappears, Prometheus immediately knows (no scrape = alert); (2) **Native Kubernetes integration**: Prometheus auto-discovers Kubernetes pods and services via ServiceMonitors; Nagios needs manual configuration; (3) **Time-series storage**: Prometheus stores metrics as (timestamp, float64 value) optimized for metric queries; Nagios stores discrete check results; (4) **Query language**: Prometheus has PromQL for complex queries and aggregations; Nagios has limited query capabilities; (5) **Scalability**: Prometheus handles millions of time series natively.

---

**Q3. What is the difference between Node Exporter and Kube State Metrics?**

**A:** Both are Prometheus exporters that collect data from different layers. Node Exporter is a DaemonSet (runs on every node) that talks to the Linux kernel and exposes hardware/OS metrics: CPU usage percentage, available memory bytes, disk I/O, network throughput, and load average. It answers "How hard is my hardware working?" Kube State Metrics is a single Deployment that talks to the Kubernetes API server and exposes the state of Kubernetes objects: pod status phases (Running/Pending/Failed), deployment ready replica counts, node conditions, PVC binding status, and HPA replica counts. It answers "What is the state of my Kubernetes workloads?" Together they provide complete observability — Node Exporter for infrastructure health, Kube State Metrics for application/workload health.

---

**Q4. What is PromQL and can you give a real example?**

**A:** PromQL (Prometheus Query Language) is the functional query language for retrieving and transforming time-series data from Prometheus. It supports filtering, aggregation, rate calculations, and mathematical operations. A real example: `rate(http_requests_total{status=~"5..",namespace="production"}[5m])` — this calculates the per-second rate of HTTP 5xx errors in the production namespace over the last 5 minutes. If this rate exceeds a threshold (e.g., > 10 errors/second), it would trigger a PagerDuty alert. Another example: `100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)` calculates CPU usage percentage per node by subtracting idle time from 100%. PromQL is used in Grafana panel queries, Prometheus alert rules, and the Prometheus UI.

---

**Q5. Why does Prometheus use a "pull" model instead of "push"?**

**A:** In a pull model, Prometheus decides when to collect data — it calls each target's `/metrics` endpoint on its schedule. This has several advantages in Kubernetes: (1) **Failure detection**: if a pod stops responding to scrapes, Prometheus immediately knows it's gone and can fire an alert — in a push model, you'd wait for a timeout; (2) **Central control**: the scrape interval, retries, and timeout are controlled centrally in Prometheus configuration, not distributed across thousands of applications; (3) **No agent overhead**: applications just need an HTTP endpoint — no persistent connection or complex agent; (4) **Rate limiting**: Prometheus controls how often it collects, preventing data storms during incidents; (5) **Service discovery**: Prometheus can discover new pods/services in Kubernetes and start scraping them automatically without any application-side configuration. The trade-off: short-lived jobs that complete before Prometheus scrapes use a Pushgateway.

---

**Q6. How do you set up alerting in Prometheus + AlertManager?**

**A:** Three components: (1) **PrometheusRule**: defines the alert condition in PromQL: `alert: HighCPU, expr: node_cpu_usage > 0.8, for: 10m` — this fires if CPU exceeds 80% for 10 continuous minutes; the `for` clause prevents alerts on brief spikes; (2) **AlertManager**: receives fired alerts from Prometheus and routes them to configured receivers based on labels — send `severity: critical` to PagerDuty, `severity: warning` to Slack; (3) **Receiver configuration**: defines where alerts go — Slack webhook URL, PagerDuty API key, email SMTP server. The flow: Prometheus evaluates rules every 15 seconds → condition met for `for` duration → alert sent to AlertManager → AlertManager deduplicates, groups, and routes → Slack/PagerDuty/email receives notification. With `kube-prometheus-stack`, many alerts come pre-configured (pod crashing, node not ready, high CPU, etc.).

---

**Q7. What persistence is required for Prometheus and Grafana, and why?**

**A:** Both need PersistentVolumes to survive pod restarts. Prometheus stores its time-series database on disk — without a PV, every pod restart loses all historical metrics, which defeats the purpose of monitoring. The PV size depends on retention period and number of metrics: a busy cluster with 30-day retention might need 50-100GB. Grafana stores its dashboards, data source configurations, user accounts, and alert rules in an SQLite or PostgreSQL database — without persistence, every restart resets to default (losing all custom dashboards). In `kube-prometheus-stack`, persistence is configured in values.yaml: `prometheus.prometheusSpec.storageSpec.volumeClaimTemplate.spec.resources.requests.storage: 50Gi` and `grafana.persistence.enabled: true, size: 10Gi`. The storage class must support ReadWriteOnce access mode (standard on GKE/EKS/AKS).

---

**Q8. How would you monitor a Node.js application with Prometheus?**

**A:** Four steps: (1) **Install prom-client**: `npm install prom-client` — the official Prometheus client for Node.js; (2) **Add metrics to the app**: create Counters (http_requests_total, errors_total), Histograms (request_duration_seconds), and Gauges (active_connections). Call `client.collectDefaultMetrics()` for Node.js runtime metrics (event loop lag, heap usage, GC); (3) **Expose /metrics endpoint**: add a route that returns `register.metrics()` with content type `register.contentType` — Prometheus scrapes this endpoint; (4) **Create a ServiceMonitor**: a Kubernetes CRD that tells the Prometheus Operator to scrape your service's metrics port every 15 seconds. The Prometheus Operator automatically discovers new ServiceMonitors and updates Prometheus configuration. After this setup, you can query `rate(http_requests_total[5m])` in Grafana to see request throughput, or `histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))` for P95 latency.

---

← Previous: [`39_Kubernetes_Advanced_Horizontal_Pod_Autoscaling_(HPA)_&_Troubleshooting.md`](39_Kubernetes_Advanced_Horizontal_Pod_Autoscaling_(HPA)_&_Troubleshooting.md) | Next: [`40_Kubernetes_Monitoring_Prometheus_Grafana_&_Helm.md`](40_Kubernetes_Monitoring_Prometheus_Grafana_&_Helm.md) →