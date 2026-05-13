# 39 – Kubernetes Advanced: Horizontal Pod Autoscaling (HPA) & Troubleshooting

---

## Table of Contents

1. [Horizontal Pod Autoscaling (HPA)](#1-horizontal-pod-autoscaling-hpa)
2. [Metrics Server – The Brain Behind HPA](#2-metrics-server--the-brain-behind-hpa)
3. [Setting Up HPA – Complete Walkthrough](#3-setting-up-hpa--complete-walkthrough)
4. [Load Testing HPA with BusyBox](#4-load-testing-hpa-with-busybox)
5. [HPA Scaling Behavior – Up & Down](#5-hpa-scaling-behavior--up--down)
6. [Kubernetes Troubleshooting – The 3-Step Rule](#6-kubernetes-troubleshooting--the-3-step-rule)
7. [The 10 Common Issues & Their Fixes](#7-the-10-common-issues--their-fixes)
8. [The 5 Commands Every DevOps Engineer Must Know](#8-the-5-commands-every-devops-engineer-must-know)
9. [RBAC – Role-Based Access Control Basics](#9-rbac--role-based-access-control-basics)
10. [Tech Stack Mapping](#10-tech-stack-mapping)
11. [Visual Diagrams](#11-visual-diagrams)
12. [Code & Practical Examples](#12-code--practical-examples)
13. [Scenario-Based Q&A](#13-scenario-based-qa)
14. [Interview Q&A](#14-interview-qa)

---

## 1. Horizontal Pod Autoscaling (HPA)

### What
**Horizontal Pod Autoscaling (HPA)** is a Kubernetes feature that **automatically increases or decreases the number of pod replicas** in a Deployment based on observed resource usage (CPU, memory, or custom metrics).

"Horizontal" means adding MORE pods (scaling out) — not making existing pods bigger (that's Vertical Pod Autoscaling, VPA).

> 💡 **Analogy:** Imagine a toll booth on a highway. At 2 AM, 1 booth handles all traffic easily. At 8 AM rush hour, 5 booths open automatically. At 10 AM when traffic dies, 4 booths close. HPA does the same for your application pods — opens more "booths" when traffic hits, closes them when it calms down.

### Why
Without HPA:
- You manually decide how many pods to run: `kubectl scale deployment/nginx --replicas=5`
- Too few pods → app is slow or crashes under load
- Too many pods → wasting money on idle servers
- Midnight traffic spike → nobody is awake to scale up

With HPA:
- Kubernetes watches CPU/memory every 15 seconds
- Automatically scales up when threshold exceeded
- Automatically scales down after load drops (with cooldown period)
- You sleep; Kubernetes handles it

### How HPA Calculates Scale

```
Desired Replicas = ceil(Current Replicas × (Current Metric / Target Metric))

Example:
  Current: 2 pods, each at 90% CPU
  Target:  50% CPU per pod
  
  Desired = ceil(2 × (90 / 50)) = ceil(3.6) = 4 pods

Kubernetes will scale from 2 → 4 pods to bring CPU back to ~50%
```

### Impact

| Without HPA | With HPA |
|-------------|---------|
| Manual scaling (miss spikes) | Automatic, instant response |
| Over-provision = wasted money | Right-sized at all times |
| Under-provision = downtime | Scales before users notice slowness |
| Someone must be on-call to scale | Kubernetes handles it 24/7 |
| App crashes at 3 AM | App scales up at 3 AM automatically |

---

## 2. Metrics Server – The Brain Behind HPA

### What
The **Metrics Server** is a Kubernetes cluster add-on that collects resource usage data (CPU and memory) from all nodes and pods every ~15 seconds and makes it available through the Kubernetes API.

HPA cannot work without Metrics Server — it has no data to base scaling decisions on.

### Why
Kubernetes doesn't natively collect resource metrics. The Metrics Server is the lightweight, in-cluster solution that provides this data. It's NOT for long-term storage or dashboards (use Prometheus + Grafana for that) — it just provides current resource usage for HPA decisions.

### Checking if Metrics Server is Installed

```bash
# Check if metrics API is available
kubectl get apiservices | grep metrics
# Should show: v1beta1.metrics.k8s.io   True

# Try to get node metrics
kubectl top nodes
# If this works, Metrics Server is running

# Try pod metrics
kubectl top pods
```

### Installing Metrics Server (if not present)

```bash
# GKE: Usually pre-installed — just verify with:
kubectl top nodes

# If not installed (or for non-GKE clusters):
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# Verify installation
kubectl get deployment metrics-server -n kube-system
kubectl get pods -n kube-system | grep metrics-server
```

### What Metrics Server Enables

```bash
# Once installed:
kubectl top nodes                    # CPU/memory per node
kubectl top pods                     # CPU/memory per pod
kubectl top pods --containers        # CPU/memory per container
kubectl get hpa                      # HPA can now show actual metrics
```

---

## 3. Setting Up HPA – Complete Walkthrough

### Step 1: Create Nginx Deployment with Resource Limits

> 🔑 **Critical:** HPA ONLY works on pods that have `resources.requests.cpu` set. Without requests defined, Kubernetes doesn't know what "50% CPU" means.

```yaml
# nginx-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 2          # Start with 2 pods
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx
        resources:
          requests:
            cpu: "250m"    # Guaranteed CPU: 250 millicores (0.25 CPU)
          limits:
            cpu: "500m"    # Maximum CPU: 500 millicores (0.5 CPU)
        ports:
        - containerPort: 80
```

```bash
kubectl apply -f nginx-deployment.yaml
kubectl get pods
kubectl describe deployment nginx-deployment
```

#### Understanding CPU Units

```
1 CPU (vCPU) = 1000 millicores

250m = 0.25 CPU = 25% of one CPU core
500m = 0.50 CPU = 50% of one CPU core
1000m = 1 CPU = 100% of one CPU core

requests: "250m"  ← Kubernetes GUARANTEES this much CPU
limits: "500m"    ← Kubernetes NEVER lets the container exceed this
```

---

### Step 2: Expose as LoadBalancer Service

```bash
kubectl expose deployment nginx-deployment \
  --type=LoadBalancer \
  --port=80 \
  --name=nginx-service

# Watch for external IP
kubectl get svc -w
# NAME            TYPE           CLUSTER-IP     EXTERNAL-IP   PORT(S)
# nginx-service   LoadBalancer   10.x.x.x       34.x.x.x      80:31xxx/TCP
```

---

### Step 3: Enable Metrics Server

```bash
# Verify metrics server is working
kubectl top nodes
kubectl top pods
```

---

### Step 4: Create the HPA

#### Method 1: kubectl autoscale (Imperative — Quick)

```bash
kubectl autoscale deployment nginx-deployment \
  --cpu-percent=50 \
  --min=2 \
  --max=5

# What this means:
# --cpu-percent=50  → Scale up when CPU exceeds 50% of requests
# --min=2           → Never go below 2 pods
# --max=5           → Never exceed 5 pods
```

#### Method 2: YAML (Declarative — Recommended)

```yaml
# hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: nginx-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: nginx-deployment
  minReplicas: 2
  maxReplicas: 5
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50    # Target: 50% of CPU requests
```

```bash
kubectl apply -f hpa.yaml
```

---

### Step 5: Verify HPA is Working

```bash
kubectl get hpa
# NAME               REFERENCE                    TARGETS    MINPODS  MAXPODS  REPLICAS  AGE
# nginx-deployment  Deployment/nginx-deployment   0%/50%     2        5        2         1m

# Columns explained:
# TARGETS:   Current CPU % / Target CPU %
# MINPODS:   Minimum replica count
# MAXPODS:   Maximum replica count
# REPLICAS:  Current actual replica count
```

---

## 4. Load Testing HPA with BusyBox

### What
**BusyBox** is a minimal Linux utility container used to generate HTTP load (simulate user traffic) to trigger HPA scaling.

### Why BusyBox for Load Testing?
- Tiny image (~1.5 MB) — starts instantly
- Has `wget` for making HTTP requests
- Can run infinite loops to hammer an endpoint
- `--rm` flag removes it after you exit — no cleanup needed

### The Load Test (from Class)

```bash
# Step 1: Launch a BusyBox container inside the cluster
kubectl run -it --rm \
  --image=busybox \
  load-generator \
  -- /bin/sh

# -it  = interactive + TTY (gives you a shell)
# --rm = auto-delete when you exit
# --image=busybox = the tiny utility container
# load-generator = name of this temporary pod
```

```bash
# Step 2: Inside BusyBox container, run infinite HTTP requests
while true; do wget -q -O- http://nginx-service; done

# while true  = loop forever
# wget        = make an HTTP request
# -q          = quiet mode (no progress output)
# -O-         = output response to stdout (don't save to file)
# http://nginx-service = calls the nginx service by DNS name
```

### Watching HPA React (in a second terminal)

```bash
# Terminal 2: Watch HPA status
kubectl get hpa -w
# NAME               TARGETS    REPLICAS
# nginx-deployment   2%/50%     2        ← before load
# nginx-deployment   11%/50%    2        ← load starting
# nginx-deployment   85%/50%    2        ← above threshold!
# nginx-deployment   85%/50%    4        ← scaled up to 4
# nginx-deployment   50%/50%    4        ← stabilizing

# Terminal 3: Watch pods being created
kubectl get pods -w
# nginx-deployment-xxx   1/1   Running   ← existing
# nginx-deployment-yyy   0/1   Pending   ← new pod starting
# nginx-deployment-yyy   1/1   Running   ← new pod ready
```

### The Cooling Period

```
Load stops (Ctrl+C in BusyBox terminal)
         │
         │ (Kubernetes waits 5 minutes before scaling down)
         │ This prevents "flapping" — rapidly scaling up/down/up/down
         ▼
kubectl get hpa -w
# TARGETS    REPLICAS
# 0%/50%     4        ← CPU dropped but still 4 pods (cooling)
# 0%/50%     4        ← still waiting (5 min default)
# 0%/50%     2        ← scaled back down to minimum ✅

# Scale-up: happens within 15-30 seconds
# Scale-down: waits 5 minutes (--stabilization-window-seconds=300)
```

### Class Observation

```
CPU reached 11% during load test (with --cpu-percent=2 threshold)
→ HPA triggered
→ Pods scaled from 2 to (up to) 5
→ After stopping load: 30-60 second cooling period observed
→ Pods scaled back to 2
```

> 💡 Note: Class used `--cpu-percent=2` (very low threshold) to make scaling easy to trigger in a demo. Production typically uses 50-70%.

---

## 5. HPA Scaling Behavior – Up & Down

### Scale-Up Behavior

```
Check interval: every 15 seconds
Scale-up condition: metric > target for 1+ check cycles
Scale-up speed: can double replicas per 15-second window
Maximum: bounded by spec.maxReplicas

Example timeline:
  t=0s:  CPU=80%, replicas=2 (above 50% threshold)
  t=15s: HPA detects: needs ceil(2 × 80/50) = 4 replicas
  t=15s: Scale to 4 pods requested
  t=30s: 2 new pods started and ready
  t=30s: CPU per pod drops to ~40% (distributed across 4)
```

### Scale-Down Behavior

```
Scale-down condition: metric < target for 5 minutes continuously
This prevents thrashing (rapidly scaling up and down)

Example timeline:
  t=0s:    Load stops. CPU=0%, replicas=4
  t=5min:  HPA confirms stable low CPU for 5 minutes
  t=5min:  Scale down to 2 pods
  
Why 5 minutes? Prevents this scenario:
  Traffic spike → scale up → traffic dips → scale down → traffic spike again
  (users would see poor performance during scale-down)
```

### HPA Configuration Options

```yaml
spec:
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 0       # Scale up immediately (default)
      policies:
      - type: Pods
        value: 2                           # Add max 2 pods per period
        periodSeconds: 15
    scaleDown:
      stabilizationWindowSeconds: 300     # Wait 5 min before scaling down (default)
      policies:
      - type: Percent
        value: 50                          # Remove max 50% of pods per period
        periodSeconds: 60
```

---

## 6. Kubernetes Troubleshooting – The 3-Step Rule

### The Golden Rule (Memorize This for Interviews)

```
Step 1: kubectl get pods -n <namespace>
        → What is the state? (Running/Pending/CrashLoopBackOff/Error)

Step 2: kubectl describe pod <pod-name> -n <namespace>
        → WHY is it in that state? (Events section at the bottom)

Step 3: kubectl logs <pod-name> --previous
        → WHAT did the application say before it crashed?
```

> 💡 **Interview tip from class:** "First I check pod status → then describe → then logs." This 3-step answer impresses interviewers because it shows systematic thinking, not random command-guessing.

### Why This Order Matters

```
get pods    → Gives you the SYMPTOM (CrashLoopBackOff)
describe    → Gives you the DIAGNOSIS (OOMKilled, ImagePullBackOff event)
logs        → Gives you the ROOT CAUSE (application error message)

Skipping describe: You'd see "CrashLoopBackOff" and guess at causes
Skipping logs: You'd know Kubernetes killed the pod but not WHY the app failed
```

---

## 7. The 10 Common Issues & Their Fixes

### Issue 1: Pod Not Starting (Pending/Unknown)

**What it looks like:**
```bash
kubectl get pods
# NAME          READY   STATUS    RESTARTS   AGE
# my-app-xxx    0/1     Pending   0          5m
```

**Diagnosis:**
```bash
kubectl describe pod my-app-xxx
# Look at Events section:
# Warning  FailedScheduling: 0/3 nodes available:
#   insufficient CPU (2 nodes), node selector not matched (1 node)
```

**Common Causes & Fixes:**

| Root Cause | Fix |
|-----------|-----|
| Insufficient CPU/RAM on nodes | Add more nodes or reduce resource requests |
| No nodes match nodeSelector | Check `kubectl get nodes --show-labels` |
| Taints on nodes | Add tolerations or remove taint |
| PVC not bound | See Issue 3 |

```bash
kubectl get events -n <namespace> --sort-by='.lastTimestamp'
kubectl describe node <node-name>  # Check Allocated resources
kubectl top nodes                   # Check current usage
```

---

### Issue 2: ImagePullBackOff

**What it looks like:**
```bash
kubectl get pods
# NAME      READY   STATUS             RESTARTS   AGE
# app-xxx   0/1     ImagePullBackOff   0          3m
```

**What it means:** Kubernetes cannot pull the container image.

**Diagnosis:**
```bash
kubectl describe pod app-xxx
# Events:
#   Warning  Failed: Failed to pull image "myapp:v2.0":
#   rpc error: 404 Not Found
```

**Common Causes & Fixes:**

| Root Cause | Fix |
|-----------|-----|
| Wrong image name/tag | Verify image exists: `docker pull image:tag` |
| Private registry, no secret | Create and reference imagePullSecret |
| Registry credentials expired | Recreate the pull secret |
| Typo in image name | Double-check in Deployment YAML |

```bash
# Check what image is being used
kubectl describe pod app-xxx | grep Image

# Check if pull secret exists
kubectl get secret -n <namespace>

# Create pull secret for Docker Hub
kubectl create secret docker-registry my-pull-secret \
  --docker-username=USER \
  --docker-password=PASSWORD \
  --docker-email=EMAIL
```

---

### Issue 3: PVC Not Bound

**What it looks like:**
```bash
kubectl get pvc
# NAME       STATUS    VOLUME   CAPACITY   ACCESS MODES
# my-pvc     Pending                                      ← Not bound!
```

**Diagnosis:**
```bash
kubectl describe pvc my-pvc
# Events:
#   Warning  ProvisioningFailed: no StorageClass found
#   OR
#   Warning  ProvisioningFailed: requested storage (100Gi) exceeds available
```

**Common Causes & Fixes:**

| Root Cause | Fix |
|-----------|-----|
| No StorageClass defined | Add `storageClassName` to PVC |
| Wrong StorageClass name | `kubectl get storageclass` → use correct name |
| Requested size exceeds available | Reduce storage request |
| Static PV capacity doesn't match | Check PV size matches or exceeds PVC request |

```bash
kubectl get storageclass           # Available storage classes
kubectl get pv                     # Available persistent volumes
kubectl describe pvc <name>        # Detailed error
```

---

### Issue 4: CrashLoopBackOff

**What it looks like:**
```bash
kubectl get pods
# NAME      READY   STATUS             RESTARTS   AGE
# app-xxx   0/1     CrashLoopBackOff   7          15m
```

**What it means:** Container keeps starting, crashing, and restarting in a loop. Kubernetes backs off exponentially (10s, 20s, 40s, 80s...) before each restart.

**Diagnosis (in order):**
```bash
# Most important: logs from the PREVIOUS (crashed) container
kubectl logs app-xxx --previous

# Check if liveness probe is failing
kubectl describe pod app-xxx
# Events: "Liveness probe failed: Get http://..."

# Check resource limits
kubectl describe pod app-xxx | grep -A5 Limits
```

**Common Causes:**

| Root Cause | Fix |
|-----------|-----|
| Application startup error | Check `kubectl logs --previous` for error message |
| OOMKilled (out of memory) | Increase memory limits or fix memory leak |
| Liveness probe failing | Fix probe path/port or increase initialDelaySeconds |
| Missing environment variable | Check ConfigMap/Secret references |
| Application can't connect to database | Fix service name or credentials |

---

### Issue 5: Service Not Accessible

**What it looks like:**
```bash
curl http://my-service   # Connection refused or no response
```

**Diagnosis:**
```bash
kubectl get svc my-service
kubectl get endpoints my-service
# NAME         ENDPOINTS
# my-service   <none>     ← THIS MEANS NO PODS MATCHED THE SELECTOR!

# OR
# my-service   10.0.0.5:80,10.0.0.6:80   ← Pods ARE connected
```

**The Endpoints Command is the Key:**
- `<none>` = Service selector labels don't match any pod labels → **label mismatch**
- IP addresses shown = routing works, issue is elsewhere (firewall, wrong port)

```bash
# Verify labels match
kubectl get pods --show-labels           # What labels do pods have?
kubectl describe svc my-service          # What selector does service use?

# Quick local test
kubectl port-forward svc/my-service 8080:80
curl http://localhost:8080

# Check NodePort from outside
kubectl get svc my-service -o jsonpath='{.spec.ports[0].nodePort}'
```

---

### Issue 6: ConfigMap Key Missing

**What it looks like:** App starts but crashes because an environment variable is undefined (`nil pointer`, `key not found`).

```bash
kubectl get configmap -n <namespace>
kubectl describe configmap my-config
# Look at Data section — is your key there?

# Check inside the pod
kubectl exec -it my-pod -- env | grep MY_KEY
kubectl exec -it my-pod -- printenv MY_KEY

# Check if configmap reference in deployment is correct
kubectl describe pod my-pod | grep -A5 "Environment"
```

---

### Issue 7: Node Not Ready

**What it looks like:**
```bash
kubectl get nodes
# NAME      STATUS     ROLES    AGE
# node-1    NotReady   worker   2h   ← Problem!
```

**Diagnosis:**
```bash
kubectl describe node node-1
# Conditions:
#   Ready  False  kubelet stopped posting node status

# Check kubelet status (SSH to the node)
systemctl status kubelet
journalctl -u kubelet -n 50   # Last 50 lines of kubelet logs

# Check resource pressure
kubectl describe node node-1 | grep -A10 "Conditions:"
# MemoryPressure: True  ← Node is running out of RAM
# DiskPressure: True    ← Node is running out of disk
```

**Common Causes:**

| Root Cause | Fix |
|-----------|-----|
| kubelet crashed | Restart: `systemctl restart kubelet` |
| Node out of memory | Free memory or add nodes |
| Node out of disk | Clean up or add disk |
| Network CNI plugin broken | Reinstall CNI plugin |
| Node unreachable | Check VM power state, SSH access |

---

### Issue 8: Pod Stuck in Pending (Scheduling Failed)

```bash
kubectl describe pod my-pod
# Events:
#   Warning  FailedScheduling: 0/3 nodes available:
#   3 Insufficient memory

# Solutions:
# 1. Add more nodes to cluster
# 2. Reduce resource requests in pod spec
# 3. Check for node taints preventing scheduling
kubectl get nodes -o json | jq '.items[].spec.taints'

# 4. Check nodeSelector
kubectl get nodes --show-labels
```

---

### Issue 9: RBAC Forbidden Error

**What it looks like:**
```bash
Error from server (Forbidden): pods is forbidden:
User "developer" cannot list resource "pods" in namespace "production"
```

**Diagnosis:**
```bash
# Check what a serviceaccount can do
kubectl auth can-i get pods \
  --as=system:serviceaccount:default:my-sa

# List role bindings in namespace
kubectl get rolebindings -n <namespace>
kubectl describe rolebinding <name> -n <namespace>

# Check cluster-level bindings
kubectl get clusterrolebindings | grep <user-or-sa>
```

**Fix:**
```bash
# Grant a serviceaccount pod-reading permission
kubectl create rolebinding allow-pods \
  --role=pod-reader \
  --serviceaccount=default:my-sa \
  -n production
```

---

### Issue 10: Ingress Not Working

```bash
kubectl get ingress -n <namespace>
kubectl describe ingress my-ingress -n <namespace>
# Check: backend service name/port, path rules, TLS config

# Is an ingress controller installed?
kubectl get ingressclass
kubectl get pods -n ingress-nginx   # For NGINX ingress

# Verify backend service works
kubectl get endpoints <backend-service>
```

---

## 8. The 5 Commands Every DevOps Engineer Must Know

These are the commands the instructor emphasized as must-know for freshers and interviews:

```bash
# 1: See ALL pods across ALL namespaces
kubectl get pods -A
# Use when: "I don't know where something is"

# 2: Get FULL details + events on any resource
kubectl describe pod <name>
# Use when: "A pod is failing and I need to know why"
# Golden rule: ALWAYS run this before asking for help

# 3: View logs from a CRASHED container
kubectl logs <name> --previous
# Use when: "Pod keeps restarting and I need to see the crash"
# --previous = logs from before the current restart

# 4: See a timeline of EVERYTHING that happened
kubectl get events --sort-by=lastTimestamp
# Use when: "Something just broke and I need to understand the sequence"

# 5: Restart a deployment without downtime
kubectl rollout restart deployment/<name>
# Use when: "Pods are stuck, config changed, or I just want a clean restart"
# Triggers a rolling restart — zero downtime ✅
```

### Why Each Is Essential

| Command | Why You Need It |
|---------|----------------|
| `get pods -A` | First thing in any debugging session — see the full picture |
| `describe pod` | 90% of answers are in the Events section here |
| `logs --previous` | The ONLY way to see what caused a crash (logs from current restart may be empty) |
| `get events --sort-by` | Understand sequence of events during an incident |
| `rollout restart` | Safe, zero-downtime fix for most common pod issues |

---

## 9. RBAC – Role-Based Access Control Basics

### What
**RBAC** in Kubernetes controls which users, services, and pods can perform which operations on which resources. It's the security layer that prevents developers from accidentally (or maliciously) deleting production resources.

### Core RBAC Objects

| Object | What it is |
|--------|-----------|
| **ServiceAccount** | Identity for a pod/application inside the cluster |
| **Role** | Set of allowed actions within ONE namespace |
| **ClusterRole** | Set of allowed actions across ALL namespaces |
| **RoleBinding** | Connects a user/SA to a Role (namespace-scoped) |
| **ClusterRoleBinding** | Connects a user/SA to a ClusterRole (cluster-wide) |

### Quick RBAC Setup

```bash
# Create a ServiceAccount for an application
kubectl create serviceaccount my-app -n default

# Create a Role (what it can do in this namespace)
kubectl create role pod-reader \
  --verb=get,list,watch \
  --resource=pods \
  -n production

# Bind the Role to the ServiceAccount
kubectl create rolebinding my-app-binding \
  --role=pod-reader \
  --serviceaccount=default:my-app \
  -n production

# Verify what the ServiceAccount can do
kubectl auth can-i list pods \
  --as=system:serviceaccount:default:my-app \
  -n production
```

---

## 10. Tech Stack Mapping

### HPA in a Real Production Pipeline

```
Production Cluster
│
├── NGINX Deployment (replicas: 2-10)
│     │ HPA: scale when CPU > 50%
│     │
│     ├── Metrics Server (monitors CPU/memory every 15s)
│     │
│     └── HPA Controller (reads metrics, adjusts replicas)
│
├── Node.js API Deployment (replicas: 3-20)
│     │ HPA: scale when CPU > 70% OR memory > 80%
│     │
│     └── Custom metrics HPA (requests-per-second from Prometheus)
│
└── Jenkins (replicas: 1, PVC for data persistence)
      │
      └── Jenkins Agent Pods (created on-demand by Kubernetes plugin)
```

### When Each HPA Threshold Makes Sense

| Service | CPU Threshold | Why |
|---------|-------------|-----|
| Web server (NGINX) | 50-60% | CPU-bound, straightforward |
| Node.js API | 60-70% | Node.js is single-threaded, scale earlier |
| Python ML service | 70-80% | Expected high CPU, scale later |
| Java Spring Boot | 60% | JVM overhead, conservative |
| Database (no HPA) | N/A | Use StatefulSet + vertical scaling instead |

### Jenkins Integration with K8s HPA

```groovy
// Jenkinsfile — deploy with HPA
stage('Deploy with HPA') {
    steps {
        sh """
            # Deploy the application
            kubectl apply -f k8s/deployment.yaml
            kubectl apply -f k8s/service.yaml

            # Apply HPA
            kubectl apply -f k8s/hpa.yaml

            # Verify HPA is active
            kubectl get hpa -n production

            # Wait for deployment
            kubectl rollout status deployment/my-app -n production
        """
    }
}
```

---

## 11. Visual Diagrams

### Diagram 1: HPA Architecture

```
                        METRICS SERVER
                        (collects every 15s)
                              │
                              │ CPU: 80% on pods
                              ▼
                        HPA CONTROLLER
                        (watches metrics)
                              │
                        CPU > 50%? YES!
                              │
                        Calculate: needs 4 pods
                              │
                              ▼
                        DEPLOYMENT (nginx-deployment)
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
          Pod 1 (80%)     Pod 2 (80%)     Pod 3 (NEW)     Pod 4 (NEW)
              │               │               │               │
              └───────────────┴───────────────┴───────────────┘
                              │
                          CPU: ~40% each (distributed)
                          HPA satisfied ✅
```

---

### Diagram 2: HPA Scale-Up vs Scale-Down Timeline

```
Time →
0m    5m    10m   15m   20m   25m   30m

Load test starts at t=2m:
CPU:     ─────╱‾‾‾‾‾‾‾‾‾‾╲──────────────────
         0%  11%          0%   0%    0%    0%

Pods:    ──────────╱‾‾‾‾‾‾‾‾╲───────────────
         2pods    4pods      2pods  (back to min)
                   │scale up │         │scale down
                  ~15s        │         5 min cooldown
                  response    └─────────┘

Scale UP:  Fast (15-30 seconds) — protects users
Scale DOWN: Slow (5 minutes) — prevents flapping
```

---

### Diagram 3: The 3-Step Troubleshooting Flow

```
Something is broken
        │
        ▼
STEP 1: kubectl get pods
  Pod status?
  ├── Running → problem is elsewhere (service? ingress?)
  ├── Pending → scheduling issue (resources? taint?)
  ├── CrashLoopBackOff → app keeps crashing → go to Step 2
  └── ImagePullBackOff → image problem → check image name/registry
        │
        ▼
STEP 2: kubectl describe pod <name>
  Read the Events section at the bottom
  ├── OOMKilled → increase memory limit
  ├── FailedScheduling → insufficient node resources
  ├── Failed to pull image → wrong image name
  ├── Liveness probe failed → fix probe or add initialDelay
  └── FailedMount → PVC not bound, check PV/PVC
        │
        ▼
STEP 3: kubectl logs <name> --previous
  Application error message → fix the bug/config
  ├── Connection refused → check service/database connection
  ├── Environment variable missing → check ConfigMap/Secret
  ├── Permission denied → check RBAC/file permissions
  └── Null pointer / panic → application code bug
```

---

### Diagram 4: BusyBox Load Test Flow

```
BusyBox Pod (inside cluster)
  while true; do wget http://nginx-service; done
              │
              │ HTTP requests (thousands per minute)
              ▼
  nginx-service (LoadBalancer → ClusterIP)
              │
              ├── nginx-pod-1 (CPU: 90% 😰)
              └── nginx-pod-2 (CPU: 90% 😰)
              
HPA detects: 90% > 50% threshold
              │
              ▼
  Scales to 4 pods
              │
              ├── nginx-pod-1 (CPU: 45% ✅)
              ├── nginx-pod-2 (CPU: 45% ✅)
              ├── nginx-pod-3 (CPU: 45% ✅) NEW
              └── nginx-pod-4 (CPU: 45% ✅) NEW
              
BusyBox stops → CPU drops to 0% → 5 min later → scales back to 2
```

---

### Diagram 5: Common Error States Flowchart

```
Pod Status
│
├── Pending
│     └── kubectl describe → Events
│           ├── "Insufficient CPU/memory" → Add nodes or reduce requests
│           ├── "No nodes matched selector" → Fix nodeSelector/labels
│           └── "Unbound PVC" → Fix PVC/StorageClass
│
├── CrashLoopBackOff
│     └── kubectl logs --previous
│           ├── OOMKilled → Increase memory limit
│           ├── App error → Fix bug
│           └── Config error → Fix ConfigMap/env vars
│
├── ImagePullBackOff
│     └── kubectl describe → Check image name/tag
│           ├── 404 Not Found → Wrong image name/tag
│           └── Unauthorized → Add imagePullSecret
│
└── Running but not accessible
      └── kubectl get endpoints SERVICE_NAME
            ├── <none> → Label mismatch between pod and service
            └── IP shown → Check port, firewall, ingress rules
```

---

## 12. Code & Practical Examples

### Example 1: Complete HPA Setup (All Files)

```yaml
# nginx-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 2
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.25-alpine
        ports:
        - containerPort: 80
        resources:
          requests:
            cpu: "250m"      # HPA requires this to be set!
            memory: "64Mi"
          limits:
            cpu: "500m"
            memory: "128Mi"
        readinessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 5
          periodSeconds: 5
        livenessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 10
          periodSeconds: 10
```

```yaml
# hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: nginx-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: nginx-deployment
  minReplicas: 2
  maxReplicas: 5
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300    # Wait 5 min before scale-down
    scaleUp:
      stabilizationWindowSeconds: 0      # Scale up immediately
```

```bash
# Deploy everything
kubectl apply -f nginx-deployment.yaml
kubectl expose deployment nginx-deployment --type=LoadBalancer --port=80 --name=nginx-service
kubectl apply -f hpa.yaml

# Verify
kubectl get pods
kubectl get svc
kubectl get hpa
kubectl top pods   # Needs metrics-server
```

---

### Example 2: Production-Grade HPA for Node.js API

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: node-api
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: node-api
  template:
    metadata:
      labels:
        app: node-api
    spec:
      containers:
      - name: api
        image: gcr.io/project/node-api:v1.5
        ports:
        - containerPort: 3000
        resources:
          requests:
            cpu: "200m"
            memory: "256Mi"
          limits:
            cpu: "500m"
            memory: "512Mi"
        readinessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 10
          periodSeconds: 5
          failureThreshold: 3
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: node-api-hpa
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: node-api
  minReplicas: 3
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 65
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 75
```

---

### Example 3: Troubleshooting Script

```bash
#!/bin/bash
# Kubernetes diagnostic script — run when something breaks

NAMESPACE=${1:-default}
POD=${2:-""}

echo "============================================"
echo " Kubernetes Diagnostic Report"
echo " Namespace: $NAMESPACE"
echo "============================================"

echo ""
echo "=== NODE STATUS ==="
kubectl get nodes -o wide

echo ""
echo "=== POD STATUS ==="
kubectl get pods -n $NAMESPACE -o wide

echo ""
echo "=== FAILING PODS ==="
kubectl get pods -n $NAMESPACE | grep -E "CrashLoop|Error|Pending|OOMKilled|ImagePull"

echo ""
echo "=== SERVICES & ENDPOINTS ==="
kubectl get svc -n $NAMESPACE
echo ""
echo "Endpoints (empty = label mismatch!):"
kubectl get endpoints -n $NAMESPACE

echo ""
echo "=== HPA STATUS ==="
kubectl get hpa -n $NAMESPACE 2>/dev/null || echo "No HPA found"

echo ""
echo "=== RECENT EVENTS (warnings) ==="
kubectl get events -n $NAMESPACE \
  --sort-by='.lastTimestamp' \
  --field-selector type=Warning \
  2>/dev/null | tail -20

echo ""
echo "=== RESOURCE USAGE ==="
kubectl top pods -n $NAMESPACE 2>/dev/null || echo "Metrics server not available"

# If a specific pod was provided
if [ -n "$POD" ]; then
  echo ""
  echo "=== DESCRIBE: $POD ==="
  kubectl describe pod $POD -n $NAMESPACE

  echo ""
  echo "=== LOGS (previous): $POD ==="
  kubectl logs $POD -n $NAMESPACE --previous 2>/dev/null || \
    echo "No previous logs (container hasn't crashed yet)"

  echo ""
  echo "=== LOGS (current): $POD ==="
  kubectl logs $POD -n $NAMESPACE --tail=50
fi

echo ""
echo "============================================"
echo " Run: kubectl describe pod <pod-name> -n $NAMESPACE"
echo " for detailed events on a specific pod"
echo "============================================"
```

---

### Example 4: Jenkins Pipeline with HPA Deploy

```groovy
pipeline {
    agent any

    environment {
        APP         = "node-api"
        NAMESPACE   = "production"
        IMAGE       = "gcr.io/${GCP_PROJECT}/${APP}:${BUILD_NUMBER}"
    }

    stages {

        stage('Build & Push') {
            steps {
                sh """
                    docker build -t ${IMAGE} .
                    gcloud auth configure-docker --quiet
                    docker push ${IMAGE}
                """
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh """
                    # Update image
                    kubectl set image deployment/${APP} \
                      ${APP}=${IMAGE} \
                      -n ${NAMESPACE}

                    # Apply HPA (idempotent — safe to re-run)
                    kubectl apply -f k8s/hpa.yaml -n ${NAMESPACE}

                    # Wait for rollout
                    kubectl rollout status deployment/${APP} \
                      -n ${NAMESPACE} --timeout=5m
                """
            }
        }

        stage('Verify') {
            steps {
                sh """
                    echo "=== Pod Status ==="
                    kubectl get pods -n ${NAMESPACE} -l app=${APP}

                    echo "=== HPA Status ==="
                    kubectl get hpa -n ${NAMESPACE}

                    echo "=== Resource Usage ==="
                    kubectl top pods -n ${NAMESPACE} -l app=${APP} || true
                """
            }
        }
    }

    post {
        failure {
            sh """
                echo "Deployment failed — rolling back"
                kubectl rollout undo deployment/${APP} -n ${NAMESPACE}
                kubectl get pods -n ${NAMESPACE} -l app=${APP}
            """
        }
    }
}
```

---

### Example 5: RBAC for Dev Team Access

```yaml
# dev-rbac.yaml — Give dev team read-only access to production

# Role: what they can do
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: dev-readonly
  namespace: production
rules:
- apiGroups: [""]
  resources: ["pods", "services", "endpoints", "configmaps"]
  verbs: ["get", "list", "watch"]
- apiGroups: [""]
  resources: ["pods/log"]
  verbs: ["get"]                   # Can read logs
- apiGroups: ["apps"]
  resources: ["deployments", "replicasets"]
  verbs: ["get", "list", "watch"]
- apiGroups: ["autoscaling"]
  resources: ["horizontalpodautoscalers"]
  verbs: ["get", "list", "watch"]  # Can see HPA but not modify
---
# RoleBinding: who gets this role
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: dev-readonly-binding
  namespace: production
subjects:
- kind: User
  name: developer@company.com
  apiGroup: rbac.authorization.k8s.io
- kind: ServiceAccount
  name: jenkins-sa
  namespace: jenkins
roleRef:
  kind: Role
  name: dev-readonly
  apiGroup: rbac.authorization.k8s.io
```

```bash
kubectl apply -f dev-rbac.yaml

# Verify developer can read pods
kubectl auth can-i list pods \
  --as=developer@company.com \
  -n production
# yes ✅

# Verify developer CANNOT delete pods
kubectl auth can-i delete pods \
  --as=developer@company.com \
  -n production
# no ✅
```

---

## 13. Scenario-Based Q&A

---

🔍 **Scenario 1:** Your Node.js API is getting crushed during a product launch — pods are at 90% CPU and users are seeing timeouts. The deployment has no HPA. What do you do immediately, and what do you set up afterward to prevent this?

✅ **Answer:** **Immediate fix:** `kubectl scale deployment/node-api --replicas=10 -n production` — manually add pods right now to handle the load. **After the incident:** Configure HPA properly. First, ensure the deployment has `resources.requests.cpu` set (HPA requires this). Then: `kubectl autoscale deployment node-api --cpu-percent=65 --min=3 --max=15 -n production`. Or preferably, create an `hpa.yaml` and commit it to Git so it's deployed automatically in future releases. Add Metrics Server if not installed. With HPA in place, the next launch scales automatically within 15-30 seconds of CPU exceeding the threshold.

---

🔍 **Scenario 2:** During an interview, you're asked to "walk through debugging a CrashLoopBackOff." What do you say?

✅ **Answer:** "My first step is always the 3-step debug flow: (1) `kubectl get pods` — confirm the state is CrashLoopBackOff and note how many restarts there are; (2) `kubectl describe pod POD_NAME` — I check the Events section at the bottom, looking for OOMKilled (memory limit hit), liveness probe failures, or missing environment variables; (3) `kubectl logs POD_NAME --previous` — this is the most important command for CrashLoopBackOff, because it shows the logs from BEFORE the restart. The current container's logs might be empty if it crashed immediately. Most causes: memory limit too low, missing configuration, database connection failure, or application startup error. Once I identify the root cause from the logs, I fix the deployment YAML — increase memory limits, add missing environment variables, or fix the application issue."

---

🔍 **Scenario 3:** You set up HPA with `--cpu-percent=50` but after the load test, HPA never scaled up. The BusyBox loop is running. What do you check?

✅ **Answer:** Three likely causes: (1) **Metrics Server not running** — `kubectl top pods` — if this errors, Metrics Server isn't installed. HPA needs it to get CPU data. Install it and retry; (2) **No resource requests defined** — `kubectl describe deployment nginx-deployment | grep -A3 Requests` — if `cpu` isn't listed under Requests, HPA has no baseline to calculate percentage against. Add `resources.requests.cpu: "250m"` to the deployment; (3) **BusyBox hitting wrong service** — verify the service name in the wget command matches the actual service: `kubectl get svc` — maybe the service is named differently. Also check: `kubectl get hpa` — if TARGETS shows `<unknown>/50%`, that's the Metrics Server issue.

---

🔍 **Scenario 4:** `kubectl get endpoints my-service` shows `<none>`. The service exists and pods are running. What's wrong?

✅ **Answer:** Label mismatch. The Service's `selector` doesn't match the pods' `labels`. Run: `kubectl describe svc my-service` — look at the Selector field (e.g., `app=myapp`). Then: `kubectl get pods --show-labels` — check if the running pods have exactly that label. Common mistake: Service selector is `app: my-app` but pods are labeled `app: myapp` (hyphen vs no-hyphen). Fix: either update the Service selector or the pod labels to match. Once labels match, endpoints populate automatically within seconds and traffic flows. This is the single most common Service issue.

---

🔍 **Scenario 5:** Your production database pod (StatefulSet) has status PVC Pending for 10 minutes and the app can't start. What do you do?

✅ **Answer:** Run `kubectl describe pvc mysql-storage-mysql-0 -n production` and read the Events. Three common causes: (1) **No StorageClass**: Events show "no StorageClass found" — `kubectl get storageclass` to see available classes. Add `storageClassName: standard` (or the correct name) to the PVC; (2) **Quota exceeded**: Events show "exceeded quota" — someone set a ResourceQuota on the namespace limiting storage. `kubectl describe resourcequota -n production` — either reduce PVC size or increase quota; (3) **Zone mismatch** (GKE): The PV is in zone A but the pod is being scheduled in zone B. Check node affinity and storage class topology. Most common in GKE: use `storageClassName: standard` which handles zone-aware provisioning.

---

🔍 **Scenario 6:** A junior developer accidentally deleted a deployment in production. Your monitoring shows the site is partially down. What's your incident response process?

✅ **Answer:** Immediate recovery (< 2 minutes): `kubectl apply -f k8s/deployment.yaml -n production` — the deployment is recreated from Git, idempotent, restores only what's missing. Watch recovery: `kubectl get pods -n production -w`. Communicate: post in incident Slack channel with ETA. Post-incident: (1) Add **RBAC controls** so junior devs don't have delete permissions in production (`kubectl auth can-i delete deployments --as=junior@company.com -n production` should return `no`); (2) This is why manifests must be in Git — recovery is seconds; (3) Document in post-mortem and share with L1/L2 teams. The whole resolution time: under 5 minutes with proper RBAC and GitOps in place.

---

## 14. Interview Q&A

---

**Q1. What is Horizontal Pod Autoscaling and how does it work?**

**A:** HPA (Horizontal Pod Autoscaling) automatically adjusts the number of pod replicas in a Deployment based on observed metrics — typically CPU or memory usage. It works through three components: the Metrics Server collects resource data from all pods every 15 seconds; the HPA Controller reads these metrics and compares them to the configured target; when the metric exceeds the target (e.g., CPU > 50%), HPA calculates the required replicas using the formula `ceil(currentReplicas × currentMetric/targetMetric)` and updates the Deployment's replica count. Scale-up is fast (15-30 seconds), scale-down has a 5-minute stabilization window to prevent flapping. Critical requirement: pods must have `resources.requests.cpu` defined — without it, HPA can't calculate CPU utilization percentage.

---

**Q2. What is CrashLoopBackOff and how do you debug it?**

**A:** CrashLoopBackOff means a container is repeatedly starting, crashing, and restarting. Kubernetes backs off exponentially (10s, 20s, 40s, 80s, max 5min) between restarts to avoid hammering a broken application. Debug steps: (1) `kubectl logs POD_NAME --previous` — the most important command: shows logs from the CRASHED container before the current restart (current logs may be empty); (2) `kubectl describe pod POD_NAME` — check Events for OOMKilled (memory limit exceeded), liveness probe failures, or missing ConfigMap/Secret references; (3) Check resource limits — if `kubectl describe pod` shows `OOMKilled`, the container needs more memory. Common root causes: application startup error, missing environment variable, out-of-memory, liveness probe too aggressive (failing before app fully starts — fix with higher `initialDelaySeconds`).

---

**Q3. What is the difference between a Pod being in "Pending" vs "CrashLoopBackOff"?**

**A:** Pending means the pod has been accepted by Kubernetes but hasn't started yet — typically a scheduling issue. The container hasn't started at all. Causes: insufficient CPU/RAM on any node, no nodes match the pod's nodeSelector, taints prevent scheduling, or a PVC hasn't bound yet. CrashLoopBackOff means the pod WAS scheduled and DID start, but the container process keeps exiting with an error code. The pod exists on a node, the image pulled successfully, but the application inside crashes immediately or soon after starting. The key distinction: Pending = Kubernetes can't START the pod; CrashLoopBackOff = Kubernetes is running the pod but the application inside keeps failing.

---

**Q4. How do you check why a Service isn't routing traffic to pods?**

**A:** `kubectl get endpoints SERVICE_NAME` is the key command. If it shows `<none>`, no pods are matching the Service's selector — this is a label mismatch and the most common cause. Compare: `kubectl describe svc SERVICE_NAME` shows the Selector (e.g., `app=myapp`), and `kubectl get pods --show-labels` shows actual pod labels. They must match exactly (case-sensitive, hyphen-sensitive). If endpoints show IP addresses but the service still isn't working: verify `targetPort` matches the container's `containerPort`, check NetworkPolicy isn't blocking traffic, confirm the application inside the pod is actually listening on that port with `kubectl exec -it POD_NAME -- netstat -tlnp`.

---

**Q5. What is the Metrics Server and why is it required for HPA?**

**A:** The Metrics Server is a Kubernetes cluster add-on that collects real-time CPU and memory usage from all nodes and pods, making this data available through the Kubernetes Metrics API (`metrics.k8s.io`). HPA requires Metrics Server because HPA needs current resource usage data to decide whether to scale. Without Metrics Server, `kubectl get hpa` shows `<unknown>/50%` for the TARGETS column — HPA can see the target but has no current data, so it doesn't scale. Verify with `kubectl top nodes` and `kubectl top pods` — if these work, Metrics Server is running. GKE typically ships with it; other clusters may need manual installation. Metrics Server is NOT for long-term storage — it only keeps the most recent metrics. Use Prometheus + Grafana for historical data and dashboards.

---

**Q6. Walk me through the commands you'd run when a pod is not starting.**

**A:** Systematic 3-step approach: (1) `kubectl get pods -n NAMESPACE` — identify the pod and its status (Pending? CrashLoopBackOff? ImagePullBackOff?); (2) `kubectl describe pod POD_NAME -n NAMESPACE` — read the Events section at the bottom, which shows the actual error (insufficient CPU, failed to pull image, PVC not bound, liveness probe failed, etc.); (3) Based on Events: if app-level issue, `kubectl logs POD_NAME --previous` to see crash output. If it's ImagePullBackOff: check image name/tag and registry credentials. If Pending: check `kubectl get nodes` for resource availability. If CrashLoopBackOff: `--previous` logs reveal the error. Additionally, `kubectl get events --sort-by=lastTimestamp` gives a timeline of everything that happened cluster-wide, useful for correlating issues.

---

**Q7. What is RBAC in Kubernetes and why is it important in production?**

**A:** RBAC (Role-Based Access Control) is Kubernetes's authorization system that controls who can perform which actions on which resources. Core objects: ServiceAccounts (identity for pods/apps), Roles (permissions within one namespace), ClusterRoles (cluster-wide permissions), RoleBindings (connects identity to role). It's critical in production because: without RBAC, any developer with cluster access could accidentally delete production deployments, view sensitive secrets, or modify security policies. With RBAC: developers get read-only access to production (can view pods and logs but not delete or modify), CI/CD service accounts get only the specific permissions they need (deploy to specific namespace, not all namespaces), and audit logs show who performed each action. The principle of least privilege: give each entity only what it needs, nothing more.

---

**Q8. What does `kubectl rollout restart deployment/NAME` do and when would you use it?**

**A:** `kubectl rollout restart` triggers a rolling restart of all pods in a deployment — one by one, with the new pod becoming ready before the old one terminates. Zero downtime. Use it when: pods are stuck in a bad state but the container isn't crashing (so CrashLoopBackOff fix methods don't apply), after updating a ConfigMap or Secret that the pod reads at startup (Kubernetes doesn't automatically restart pods when their ConfigMaps change), when you want a clean slate without changing the deployment configuration, or when debugging intermittent issues where a fresh pod start might resolve them. Unlike deleting pods manually (which also triggers recreation), `rollout restart` is controlled, auditable, records the restart in rollout history, and can be undone with `kubectl rollout undo`.

---

← Previous: [`38_Kubernetes_Microservices_Deployment_Monolithic_vs_Microservices_GKE_&_Real-World_E-Commerce_App.md`](38_Kubernetes_Microservices_Deployment_Monolithic_vs_Microservices_GKE_&_Real-World_E-Commerce_App.md) | Next: [`40_Kubernetes_ConfigMaps_Secrets_Ingress.md`](40_Kubernetes_ConfigMaps_Secrets_Ingress.md) →