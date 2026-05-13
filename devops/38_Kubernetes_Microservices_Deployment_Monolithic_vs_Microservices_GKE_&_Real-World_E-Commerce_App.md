# 38 – Kubernetes Microservices Deployment: Monolithic vs Microservices, GKE & Real-World E-Commerce App

---

## Table of Contents

1. [Monolithic vs Microservices Architecture](#1-monolithic-vs-microservices-architecture)
2. [The Online Boutique – Real Microservices Application](#2-the-online-boutique--real-microservices-application)
3. [How Microservices Connect in Kubernetes](#3-how-microservices-connect-in-kubernetes)
4. [GKE Cluster Setup for Microservices](#4-gke-cluster-setup-for-microservices)
5. [Deploying the Full Application – Single Command](#5-deploying-the-full-application--single-command)
6. [Understanding the Kubernetes Manifest File](#6-understanding-the-kubernetes-manifest-file)
7. [Troubleshooting – Live Failure Scenarios from Class](#7-troubleshooting--live-failure-scenarios-from-class)
8. [Idempotent Deployments – Why kubectl apply is Safe](#8-idempotent-deployments--why-kubectl-apply-is-safe)
9. [Running Jenkins on Kubernetes](#9-running-jenkins-on-kubernetes)
10. [Resume Writing – How to Frame This Experience](#10-resume-writing--how-to-frame-this-experience)
11. [Tech Stack Mapping](#11-tech-stack-mapping)
12. [Visual Diagrams](#12-visual-diagrams)
13. [Code & Practical Examples](#13-code--practical-examples)
14. [Scenario-Based Q&A](#14-scenario-based-qa)
15. [Interview Q&A](#15-interview-qa)

---

## 1. Monolithic vs Microservices Architecture

### What

#### Monolithic Architecture
A **monolith** is an application where ALL features — user interface, business logic, database layer, cart, payments, recommendations — are bundled into **one single codebase**, built as **one deployable unit**, and managed by **one team**.

> 💡 **Analogy:** A monolith is like a Swiss Army knife. Everything is in one tool — scissors, knife, corkscrew. Very convenient when it's small. But if the corkscrew breaks, you have to return the entire knife. If you want to upgrade the scissors, you rebuild the whole tool.

#### Microservices Architecture
**Microservices** split each feature or domain into **independent, separately deployable services** that communicate with each other over a network (HTTP/gRPC).

> 💡 **Analogy:** Microservices are like a full kitchen with specialized appliances — a dedicated blender, a dedicated toaster, a dedicated coffee maker. If the toaster breaks, you still have coffee. Each appliance can be upgraded or replaced independently. Different chefs can work on different appliances at the same time.

---

### Why – The Business Reason for Microservices

#### Monolith Problems That Drove the Change

```
Startup stage: Monolith is FINE
  - Small team (5-10 devs)
  - Simple app, fast to build
  - One deployment = everything ships

Scale stage: Monolith becomes a NIGHTMARE
  - 200 developers all editing the same codebase
  - One feature change requires testing/redeploying everything
  - Checkout feature scales → entire app must scale (wasteful)
  - Bug in recommendations crashes payment service too
  - Different features need different tech stacks (Java vs Python vs Go)
  - Deploy: 4+ hours, high risk, all-hands event
```

#### Microservices Benefits

| Problem | Microservices Solution |
|---------|----------------------|
| One team owns everything | Each service has its own team |
| Any bug can crash everything | Bug in recommendations doesn't affect payments |
| Must scale everything together | Scale only the bottleneck (e.g., checkout) |
| Long deployment cycles | Each service deploys independently |
| One language for everything | Each service picks its own language |
| Hard to onboard new developers | Team owns small, understandable service |
| Difficult to troubleshoot | Logs/metrics per service, easy to isolate |

---

### How – The Architecture Shift

```
MONOLITH:
┌──────────────────────────────────────────────────────┐
│                    ONE APPLICATION                   │
│  Frontend + Cart + Payments + Catalog + Email + ...  │
│                                                      │
│  One codebase, one database, one deployment          │
│  One team, one tech stack, one scaling unit          │
└──────────────────────────────────────────────────────┘
  Deployed: shopping-cart.jar (500MB, 3 hour deploy)

MICROSERVICES:
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│ Frontend │  │  Cart    │  │ Payments │  │ Catalog  │
│  (Go)    │  │ (C#/.NET)│  │  (Node)  │  │  (Go)    │
└────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘
     │              │              │              │
     └──────────────┴──────────────┴──────────────┘
              Communicate via Kubernetes Services (gRPC/HTTP)
  
  Each service: own repo (or own folder), own Docker image,
  own deployment, own team, own language, independent scaling
```

### Impact

| | Monolith | Microservices |
|--|---------|--------------|
| **Team structure** | One large team | Multiple small teams |
| **Deploy frequency** | Weekly/Monthly (risky) | Multiple times per day |
| **Failure blast radius** | Entire app | One service |
| **Scaling** | Scale everything | Scale only what needs it |
| **Tech flexibility** | One language/framework | Best tool per service |
| **Startup speed** | Slow (large single app) | Fast (small services) |
| **Troubleshooting** | Complex, cross-cutting | Isolated per service |
| **Kubernetes fit** | ⚠️ Possible but wasteful | ✅ Perfect fit |

---

## 2. The Online Boutique – Real Microservices Application

### What
The **Online Boutique** (originally Google's `microservices-demo`) is a cloud-native e-commerce application built by Google to demonstrate microservices architecture on Kubernetes. It's a real, production-quality application used for training and demos.

**Repository:** `https://github.com/GoogleCloudPlatform/microservices-demo.git`
**Class Fork:** `https://github.com/DevSecOpsG/cd-k8`

### The 11 Microservices

| Service | Language | What It Does |
|---------|----------|-------------|
| **Frontend** | Go | The web UI — what users see and interact with |
| **Cart Service** | C# / .NET | Manages shopping cart state using Redis |
| **Product Catalog** | Go | Product listings, search, details |
| **Currency Service** | Node.js | Converts prices: USD → INR, JPY, CAD, EUR |
| **Payment Service** | Node.js | Processes credit card transactions |
| **Shipping Service** | Go | Calculates shipping costs and manages delivery |
| **Email Service** | Python | Sends order confirmation emails |
| **Checkout Service** | Go | Orchestrates the checkout flow (calls payment, shipping, email) |
| **Recommendation Service** | Python | AI-powered "you might also like" suggestions |
| **Ad Service** | Java | Serves contextual advertisements |
| **Load Generator** | Python/Locust | Simulates user traffic for testing |

> 💡 **Why different languages?** This is real microservices — each team picks the best tool for their job. The Currency Service team picked Node.js for its JSON handling. The Email Service team picked Python for its email libraries. The Frontend team picked Go for its performance. Kubernetes doesn't care what language each service uses — it just runs the Docker container.

### Internal Communication

All services communicate through Kubernetes Services using **gRPC** (Google Remote Procedure Call) — a high-performance binary protocol. The Frontend calls the Cart Service, which calls the Product Catalog, etc.

```
User Browser
     │ HTTP
     ▼
Frontend (Go)
     │ gRPC
     ├── Product Catalog Service (Go)
     ├── Cart Service (C#) ──── Redis (in-memory DB)
     ├── Currency Service (Node.js)
     └── Checkout Service (Go)
              │ gRPC
              ├── Payment Service (Node.js)
              ├── Shipping Service (Go)
              └── Email Service (Python)
```

---

## 3. How Microservices Connect in Kubernetes

### The Role of Match Labels

In the Kubernetes manifests, **labels** are the glue that connects services to their pods and services to each other.

```yaml
# Cart Service Deployment
metadata:
  labels:
    app: cartservice       ← "I am the cart service"

# Cart Service (Kubernetes Service)
spec:
  selector:
    app: cartservice       ← "Route traffic to pods labeled 'cartservice'"
```

When the Frontend calls `cartservice:7070`, Kubernetes's Service finds all pods labeled `app: cartservice` and routes the request to one of them. This is how 11 different services know how to find each other.

### Service Discovery in Kubernetes

```bash
# Inside the Frontend container, calling Cart Service:
grpc.Dial("cartservice:7070")
# Kubernetes DNS resolves "cartservice" to the ClusterIP of the cartservice Service
# Which then routes to a running cartservice pod

# No IP addresses hardcoded — service names only
# If Cart Service pod restarts with new IP → doesn't matter
# Service name "cartservice" always works
```

### The Load Balancer for External Access

Line 816 in the manifest creates the **frontend-external** Service with type `LoadBalancer`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: frontend-external
spec:
  type: LoadBalancer     # ← Creates a GCP external load balancer
  selector:
    app: frontend
  ports:
  - port: 80
    targetPort: 8080
```

This is the ONLY service exposed to the internet. All internal services use ClusterIP (invisible from outside). This is a security best practice — minimize the public attack surface.

---

## 4. GKE Cluster Setup for Microservices

### Why Different Configuration Than Standard?

The microservices demo runs 11+ services simultaneously. Standard 2 CPU / 4 GB RAM nodes would run out of memory.

### Class Configuration

```
Cluster: online-boutique-cluster
Location: us-central1-a (or nearest region)
Nodes: 1-3 (limited by GCP free tier quota)
Per node:
  - CPU: 2 vCPUs (1 core)
  - RAM: 8 GB (doubled from standard 4 GB)
  - Disk: 30 GB SSD
```

### Step 1: Create GKE Cluster

```bash
# Via gcloud CLI
gcloud container clusters create online-boutique \
  --zone us-central1-a \
  --num-nodes 3 \
  --machine-type e2-standard-2 \
  --disk-size 30 \
  --disk-type pd-ssd

# e2-standard-2 = 2 vCPU, 8 GB RAM — matches class config
```

### Step 2: Connect to the Cluster

```bash
# Get credentials (writes to ~/.kube/config)
gcloud container clusters get-credentials online-boutique \
  --zone us-central1-a

# Verify connection
kubectl get nodes
# Should show your nodes as Ready
kubectl cluster-info
```

---

## 5. Deploying the Full Application – Single Command

### What Makes This "Single-Click"

The entire 11-service application — every Deployment, every Service, every ConfigMap — is defined in ONE file: `kubernetes-manifests.yaml`. One `kubectl apply` deploys everything.

### The Full Deployment Process (from Class)

```bash
# Step 1: Clone the repository
git clone https://github.com/DevSecOpsG/cd-k8.git
# Original Google repo:
# git clone https://github.com/GoogleCloudPlatform/microservices-demo.git

# Step 2: Navigate to project
cd cd-k8
# or
cd microservices-demo

# Step 3: Deploy EVERYTHING with one command
kubectl apply -f ./release/kubernetes-manifests.yaml

# What happens:
# Kubernetes reads the YAML file
# Creates 11 Deployments (one per service)
# Creates 11 Services (one per service)
# Creates 1 ConfigMap (Redis config)
# Pulls Docker images from Google's Container Registry
# Starts all pods across nodes
# Connects services via labels

# Step 4: Watch pods starting up
kubectl get pods -w
# You'll see: Pending → ContainerCreating → Running for each service

# Step 5: Get the external IP of the frontend
kubectl get service frontend-external | awk '{print $4}'
# Output: 34.x.x.x  ← paste this in your browser
# Or wait and watch:
kubectl get svc -w

# Step 6: Open in browser
# http://34.x.x.x  → Online Boutique e-commerce site ✅
```

### What Gets Created

```bash
kubectl get all
# NAME                                    READY   STATUS
# pod/adservice-xxx                       1/1     Running
# pod/cartservice-xxx                     1/1     Running
# pod/checkoutservice-xxx                 1/1     Running
# pod/currencyservice-xxx                 1/1     Running
# pod/emailservice-xxx                    1/1     Running
# pod/frontend-xxx                        1/1     Running
# pod/loadgenerator-xxx                   1/1     Running
# pod/paymentservice-xxx                  1/1     Running
# pod/productcatalogservice-xxx           1/1     Running
# pod/recommendationservice-xxx           1/1     Running
# pod/redis-cart-xxx                      1/1     Running
# pod/shippingservice-xxx                 1/1     Running
#
# NAME                     TYPE           CLUSTER-IP    EXTERNAL-IP
# service/adservice         ClusterIP      10.x.x.x      <none>
# service/cartservice       ClusterIP      10.x.x.x      <none>
# service/frontend          ClusterIP      10.x.x.x      <none>
# service/frontend-external LoadBalancer   10.x.x.x      34.x.x.x  ← Public
# ...all others: ClusterIP (internal only)
```

### Checking Individual Service Details

```bash
# Check a specific pod
kubectl describe pod paymentservice-xxx

# Check logs for a service
kubectl logs -f paymentservice-xxx

# Get external IP with awk (from class)
kubectl get service frontend-external | awk '{print $4}'
# awk '{print $4}' extracts the 4th column (EXTERNAL-IP) from the output
```

---

## 6. Understanding the Kubernetes Manifest File

### What is `kubernetes-manifests.yaml`?

A single YAML file containing ALL Kubernetes resource definitions for all 11 services. Resources are separated by `---` (the YAML document separator).

### Structure of the File

```yaml
# ─── Service 1: adservice ──────────────────────────────────
apiVersion: apps/v1
kind: Deployment
metadata:
  name: adservice
spec:
  selector:
    matchLabels:
      app: adservice
  template:
    metadata:
      labels:
        app: adservice
    spec:
      containers:
      - name: server
        image: gcr.io/google-samples/microservices-demo/adservice:v0.8.0
        ports:
        - containerPort: 9555
        resources:
          requests:
            cpu: 200m
            memory: 180Mi
          limits:
            cpu: 300m
            memory: 300Mi
---
apiVersion: v1
kind: Service
metadata:
  name: adservice
spec:
  type: ClusterIP       # Internal only
  selector:
    app: adservice
  ports:
  - port: 9555
    targetPort: 9555
---
# ─── Service 2: cartservice ────────────────────────────────
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cartservice
...
# ─── (repeats for all 11 services) ────────────────────────
# ─── Line 816: The one public-facing service ───────────────
apiVersion: v1
kind: Service
metadata:
  name: frontend-external   # ← THE internet-facing service
spec:
  type: LoadBalancer        # ← Creates GCP external LB
  selector:
    app: frontend
  ports:
  - port: 80
    targetPort: 8080
```

### Key Principle: One Manifest, Many Services

The beauty of this approach:
- One file in Git → Source of truth for the entire application
- `kubectl apply -f kubernetes-manifests.yaml` → Deploy or update everything
- Change one service → Update the file → Re-apply → Only that service updates
- New team member → Clone repo → Apply manifest → Full app running in 5 minutes

---

## 7. Troubleshooting – Live Failure Scenarios from Class

### Scenario 1: Deleting a Single Pod (Email Service)

#### What happened

```bash
# Find the email service pod name
kubectl get pods | grep email
# emailservice-7d4f9b2c1-x7k2p   1/1   Running

# Manually delete the pod (simulating a crash)
kubectl delete pod emailservice-7d4f9b2c1-x7k2p
```

#### What Kubernetes did

```
t=0s:  emailservice pod deleted
t=2s:  ReplicaSet detects: desired=1, actual=0 → mismatch!
t=5s:  New pod scheduled: emailservice-7d4f9b2c1-NEW_ID (Pending)
t=10s: Container image pulled, container starting
t=15s: Pod is Running ✅
t=20s: Pod passes readiness probe → traffic routes to it

Impact: ~5-15 seconds of email service unavailability
User impact: If someone was checking out during those 15 seconds,
             their order confirmation email might be delayed.
             The checkout itself still completed (checkout calls
             email service asynchronously).
```

#### Key Learning
- Deleting a pod in a Deployment = **auto-healing kicks in immediately**
- A deployment with **multiple replicas** (e.g., 2) means zero downtime even during pod replacement
- Single replica → brief downtime (~15 seconds)
- This is why production has `replicas: 2` or higher for critical services

---

### Scenario 2: Deleting a Deployment (Payment Service)

#### What happened

```bash
# Delete the ENTIRE payment service deployment
kubectl delete deployment paymentservice

# What this does:
# - Deletes the Deployment object
# - Deletes the ReplicaSet
# - Deletes all payment service Pods
# - (Does NOT delete the Service object — that persists)
```

#### User Impact

```
User browses products → Works ✅ (product catalog still up)
User adds to cart → Works ✅ (cart service still up)
User proceeds to checkout → Clicks "Place Order"
  → Checkout service calls Payment service
  → RPC unavailable error: "payment service unavailable"
  → User sees error page ❌

What still worked:
  ✅ Browsing products
  ✅ Adding to cart
  ✅ Viewing recommendations
  ✅ Currency conversion
  ✅ Everything EXCEPT paying

This is the MICROSERVICES BENEFIT:
  In a monolith: payment bug = ENTIRE SITE DOWN
  In microservices: payment bug = ONLY PAYMENT FAILS
```

#### Recovery

```bash
# Redeploy using the same manifest — idempotent!
kubectl apply -f ./release/kubernetes-manifests.yaml

# What happens:
# Kubernetes reads the entire file
# Finds: paymentservice Deployment is MISSING → creates it
# All other services: ALREADY EXIST → no changes made
# Only the missing payment service is created

# Watch recovery:
kubectl get pods -w | grep payment
# paymentservice-xxx   0/1   ContainerCreating
# paymentservice-xxx   1/1   Running ✅

# Site is fully functional again
```

---

### Troubleshooting Commands Cheatsheet

```bash
# Find which pods are not Running
kubectl get pods | grep -v Running
kubectl get pods | grep -E "CrashLoop|Error|Pending|ImagePull"

# Get detailed info on a failing pod
kubectl describe pod FAILING_POD_NAME
# Look at: Events section at bottom → shows exactly what went wrong

# Check application logs
kubectl logs PODNAME
kubectl logs -f PODNAME           # Follow live
kubectl logs --previous PODNAME   # Logs from crashed container

# Check all events in the cluster
kubectl get events --sort-by='.lastTimestamp'

# Check resource usage
kubectl top pods
kubectl top nodes

# Check if service is routing to pods
kubectl describe svc paymentservice
# Look at Endpoints — if empty, no pods with matching labels exist
```

---

## 8. Idempotent Deployments – Why kubectl apply is Safe

### What
**Idempotent** means running the same operation multiple times produces the same result. `kubectl apply` is idempotent — run it once or 100 times, the result is the same desired state.

### Why This Matters

```bash
# Run 1: Nothing deployed yet
kubectl apply -f kubernetes-manifests.yaml
# Creates: 11 Deployments, 12 Services, 1 ConfigMap → all new

# Run 2: Some services deleted (payment was deleted)
kubectl apply -f kubernetes-manifests.yaml
# Creates: paymentservice (missing)
# Skips: all other existing services (unchanged)

# Run 3: Nothing changed since Run 2
kubectl apply -f kubernetes-manifests.yaml
# Skips: everything (all already in desired state)
# No errors, no duplicates, no harm done

# This is why kubectl apply is the standard in CI/CD
# Jenkins pipeline can run kubectl apply after every merge
# → Only changed services get updated, rest untouched
```

### How kubectl apply Knows What to Do

```
kubectl apply reads the YAML file
          │
          ├── For each resource in the file:
          │     ├── Does it exist in the cluster?
          │     │     ├── NO → Create it
          │     │     └── YES → Is it different from the file?
          │     │                 ├── YES → Update it
          │     │                 └── NO  → Do nothing
          │
          └── Result: Cluster matches the file exactly
```

---

## 9. Running Jenkins on Kubernetes

### What
Jenkins itself can run as a containerized application inside Kubernetes, just like any other service.

### Why Run Jenkins in K8s?
- Jenkins becomes highly available (K8s restarts it if it crashes)
- Jenkins agents can be Kubernetes pods (spin up dynamically for each build)
- Unified infrastructure — everything in one cluster

### The Command from Class

```bash
# Quick way to run Jenkins in Kubernetes
kubectl run jenkins --image=jenkins/jenkins:lts

# This creates a single Pod (not ideal for production)
# Better approach: use a Deployment for auto-healing
kubectl create deployment jenkins \
  --image=jenkins/jenkins:lts \
  --replicas=1
```

### Proper Jenkins on Kubernetes

```bash
# Step 1: Create namespace for Jenkins
kubectl create namespace jenkins

# Step 2: Deploy Jenkins with persistent storage
kubectl apply -f jenkins-deployment.yaml -n jenkins

# Step 3: Expose Jenkins
kubectl expose deployment jenkins \
  --type=LoadBalancer \
  --port=8080 \
  --target-port=8080 \
  -n jenkins

# Step 4: Get external IP
kubectl get svc -n jenkins -w

# Step 5: Get initial admin password
kubectl exec -it jenkins-pod-name -n jenkins -- \
  cat /var/jenkins_home/secrets/initialAdminPassword
```

---

## 10. Resume Writing – How to Frame This Experience

### What to Say vs What Not to Say

The instructor emphasized writing resume points that demonstrate **impact and decision-making**, not just commands.

### Strong Resume Points (Use These)

```
✅ "Migrated a monolithic e-commerce application to microservices 
    architecture on Kubernetes (GKE), resulting in independent 
    service deployments and improved fault isolation"

✅ "Designed and implemented single-click deployment pipeline using 
    kubectl apply with Kubernetes manifests, reducing deployment 
    time from 4 hours to 10 minutes"

✅ "Implemented CI/CD pipeline using Jenkins integrated with GKE, 
    enabling automated builds and deployments triggered by GitHub 
    push events"

✅ "Troubleshot P1 production incidents involving Kubernetes pod 
    failures and service disruptions, achieving resolution within 
    10 minutes using kubectl describe, logs, and events"

✅ "Created knowledge transfer documentation for L1/L2 support teams 
    covering Kubernetes operations, runbooks, and common error 
    resolutions"

✅ "Deployed Google's microservices demo (11 services, multiple 
    languages: Go, Python, Java, Node.js, C#) on GKE using 
    infrastructure-as-code approach"
```

### Weak Resume Points (Avoid These)

```
❌ "Used kubectl to deploy applications"
   (no impact, no scale, no context)

❌ "Worked on Kubernetes"
   (too vague)

❌ "Ran kubectl apply commands"
   (describes a task, not an achievement)
```

### The P1 Incident Framing

In interviews, use the STAR method (Situation, Task, Action, Result):

```
"During a production incident, the payment service deployment was 
accidentally deleted (Situation). I was responsible for restoring 
service within the SLA (Task). I immediately identified the missing 
deployment using kubectl get pods, confirmed the error was RPC 
unavailable via logs, and redeployed using the existing Kubernetes 
manifest (Action). The service was restored in 8 minutes with no 
data loss, and I documented the incident and added RBAC restrictions 
to prevent accidental deletions (Result)."
```

---

## 11. Tech Stack Mapping

### Online Boutique Full Stack on Kubernetes

```
Internet User
     │ HTTPS
     ▼
GCP Cloud Load Balancer (external IP: 34.x.x.x)
     │
     ▼
frontend-external Service (LoadBalancer, port 80)
     │
     ▼
Frontend Pod (Go, port 8080)
     │ gRPC (internal ClusterIP services)
     ├─────────────────────────────────────────────────────┐
     │                                                     │
     ▼                                                     ▼
Product Catalog Service          Cart Service (C#, port 7070)
(Go, port 3550)                         │
     │                              Redis (port 6379)
     ▼                                   
Recommendation Service
(Python, port 8080)
     │
     ├── Currency Service (Node.js, port 7000)
     │
     └── Checkout Service (Go, port 5050)
              │
              ├── Payment Service (Node.js, port 50051)
              ├── Shipping Service (Go, port 50051)
              └── Email Service (Python, port 8080)
```

### DevOps Pipeline for Microservices

```
Developer on team X (e.g., Payment Team)
  │ git push payment-service/
  ▼
GitHub → webhook → Jenkins
  │
  ▼
Jenkins Pipeline:
  Stage 1: Clone (only payment-service code)
  Stage 2: Build Docker image
  Stage 3: Push to GCR
  Stage 4: kubectl set image deployment/paymentservice
           paymentservice=gcr.io/project/payment:v1.5
  Stage 5: kubectl rollout status → wait for success
  │
  ▼
Only paymentservice pods updated (rolling update)
Other 10 services: UNTOUCHED, still serving traffic ✅
```

---

## 12. Visual Diagrams

### Diagram 1: Monolith vs Microservices

```
MONOLITH                                MICROSERVICES
────────                                ─────────────
┌──────────────────────────┐           ┌──────────┐ ┌──────────┐
│    EVERYTHING IN ONE     │           │ Frontend │ │  Cart    │
│                          │           │  (Go)    │ │ (C#)     │
│  Frontend                │           └────┬─────┘ └────┬─────┘
│  Cart                    │                │             │
│  Payments                │           ┌────▼─────┐ ┌────▼─────┐
│  Catalog                 │           │ Payments │ │ Catalog  │
│  Email                   │           │ (Node.js)│ │  (Go)    │
│  Shipping                │           └──────────┘ └──────────┘
│  Recommendations         │
│  Currency                │           ┌──────────┐ ┌──────────┐
│  Ads                     │           │  Email   │ │Recommend │
│                          │           │ (Python) │ │ (Python) │
│  ONE: team, repo,        │           └──────────┘ └──────────┘
│  deploy, language, DB    │
└──────────────────────────┘           Each: own team, own repo,
                                       own language, own deploy,
Bug in email = SITE DOWN               own database
Bug in email = EMAIL DOWN ONLY ✅
```

---

### Diagram 2: Service Communication via Labels

```
YAML:
  Deployment: paymentservice
    labels: app=paymentservice

  Service: paymentservice
    selector: app=paymentservice      ← finds pods with this label

  Checkout Deployment calls:
    grpc.Dial("paymentservice:50051") ← uses service name, not IP

K8s DNS resolves "paymentservice"
    → ClusterIP of paymentservice Service
    → Routes to pod labeled app=paymentservice
    → Pod IP: 10.x.x.x (doesn't matter, changes with pod restarts)

Result: Checkout → calls "paymentservice" → always works ✅
```

---

### Diagram 3: Single Manifest, 11 Services

```
kubernetes-manifests.yaml (one file)
│
├── --- Deployment: adservice
├── --- Service: adservice
├── --- Deployment: cartservice
├── --- Service: cartservice
├── --- Deployment: checkoutservice
├── --- Service: checkoutservice
├── --- Deployment: currencyservice
├── --- Service: currencyservice
├── --- Deployment: emailservice
├── --- Service: emailservice
├── --- Deployment: frontend
├── --- Service: frontend (ClusterIP, internal)
├── --- Service: frontend-external (LoadBalancer ← LINE 816, public!)
├── --- Deployment: paymentservice
├── --- Service: paymentservice
├── --- Deployment: productcatalogservice
├── --- Service: productcatalogservice
├── --- Deployment: recommendationservice
├── --- Service: recommendationservice
├── --- Deployment: shippingservice
├── --- Service: shippingservice
├── --- Deployment: redis-cart
└── --- Service: redis-cart

kubectl apply -f kubernetes-manifests.yaml
→ ALL of the above created in one command ✅
```

---

### Diagram 4: Microservices Failure Impact Comparison

```
MONOLITH (one bug = full outage):
Payment bug → 
  ❌ No browsing
  ❌ No search
  ❌ No cart
  ❌ No checkout
  ❌ No payments     ← the actual problem
  ❌ No emails
  ❌ No recommendations

MICROSERVICES (one bug = one service down):
Payment service deleted →
  ✅ Browsing works
  ✅ Search works
  ✅ Cart works
  ❌ Checkout fails  ← only because it calls payment
  ❌ No payments     ← the actual problem
  ✅ Emails work
  ✅ Recommendations work
  ✅ Currency works

Revenue impact: Much lower in microservices scenario
```

---

### Diagram 5: Idempotent kubectl apply

```
State 1: Fresh cluster                State 2: Payment deleted
All 11 services running               10 services running
                │                              │
                │ kubectl apply                │ kubectl apply
                │ kubernetes-manifests.yaml    │ kubernetes-manifests.yaml
                ▼                              ▼
All 11: already exist → SKIP          10: already exist → SKIP
Result: No changes                    paymentservice: missing → CREATE
                                      Result: payment restored ✅

State 3: Image updated in YAML
                │
                │ kubectl apply
                ▼
Changed service: rolling update
Other 10: same as file → SKIP
Result: only changed service updated ✅
```

---

### Diagram 6: Pod Deletion vs Deployment Deletion

```
DELETE POD:                            DELETE DEPLOYMENT:
kubectl delete pod emailservice-xxx    kubectl delete deployment paymentservice

ReplicaSet still exists                ReplicaSet ALSO deleted
ReplicaSet detects: 0/1 pods          Pods deleted
Creates new pod automatically         Service still exists (but no pods behind it)

Impact: 10-15 second gap              Impact: Permanent until redeployed
                                       Callers get: RPC unavailable error

Recovery: Automatic (10-15 sec)        Recovery: kubectl apply (manual)
```

---

## 13. Code & Practical Examples

### Example 1: Complete Deployment Steps (from Class)

```bash
#!/bin/bash
# Complete deployment script for Online Boutique on GKE

# === STEP 1: Create GKE Cluster ===
gcloud container clusters create online-boutique \
  --zone us-central1-a \
  --num-nodes 3 \
  --machine-type e2-standard-2 \
  --disk-size 30 \
  --disk-type pd-ssd

# === STEP 2: Connect to Cluster ===
gcloud container clusters get-credentials online-boutique \
  --zone us-central1-a

# Verify
kubectl get nodes

# === STEP 3: Clone Repository ===
git clone https://github.com/DevSecOpsG/cd-k8.git
# Or Google's original:
# git clone https://github.com/GoogleCloudPlatform/microservices-demo.git
cd cd-k8   # or microservices-demo

# === STEP 4: Deploy Everything ===
kubectl apply -f ./release/kubernetes-manifests.yaml

# === STEP 5: Watch Pods Start ===
kubectl get pods -w
# Wait until all pods show: Running 1/1

# === STEP 6: Get External IP ===
echo "Waiting for external IP..."
until kubectl get service frontend-external | awk '{print $4}' | grep -v EXTERNAL; do
  sleep 5
  echo "Still waiting..."
done

EXTERNAL_IP=$(kubectl get service frontend-external | awk '{print $4}')
echo "🎉 Application is live at: http://$EXTERNAL_IP"

# === STEP 7: Verify all services ===
kubectl get pods
kubectl get svc
kubectl get deployments
```

---

### Example 2: Single Service Manifest (Payment Service)

```yaml
# paymentservice deployment + service
apiVersion: apps/v1
kind: Deployment
metadata:
  name: paymentservice
spec:
  selector:
    matchLabels:
      app: paymentservice
  template:
    metadata:
      labels:
        app: paymentservice
    spec:
      serviceAccountName: default
      terminationGracePeriodSeconds: 5
      securityContext:
        fsGroup: 1000
        runAsGroup: 1000
        runAsNonRoot: true
        runAsUser: 1000
      containers:
      - name: server
        image: gcr.io/google-samples/microservices-demo/paymentservice:v0.8.0
        ports:
        - containerPort: 50051
        env:
        - name: PORT
          value: "50051"
        - name: DISABLE_PROFILER
          value: "1"
        readinessProbe:
          grpc:
            port: 50051
        livenessProbe:
          grpc:
            port: 50051
        resources:
          requests:
            cpu: 100m
            memory: 64Mi
          limits:
            cpu: 200m
            memory: 128Mi
---
apiVersion: v1
kind: Service
metadata:
  name: paymentservice
spec:
  type: ClusterIP         # Internal only — never expose payments publicly
  selector:
    app: paymentservice
  ports:
  - name: grpc
    port: 50051
    targetPort: 50051
```

---

### Example 3: Jenkins on Kubernetes (Production-Grade)

```yaml
# jenkins-on-k8s.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: jenkins
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: jenkins-pvc
  namespace: jenkins
spec:
  accessModes:
  - ReadWriteOnce
  storageClassName: standard
  resources:
    requests:
      storage: 20Gi
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: jenkins
  namespace: jenkins
spec:
  replicas: 1
  selector:
    matchLabels:
      app: jenkins
  template:
    metadata:
      labels:
        app: jenkins
    spec:
      securityContext:
        fsGroup: 1000
        runAsUser: 1000
      containers:
      - name: jenkins
        image: jenkins/jenkins:lts
        ports:
        - containerPort: 8080
          name: http
        - containerPort: 50000
          name: agent
        volumeMounts:
        - name: jenkins-home
          mountPath: /var/jenkins_home
        resources:
          requests:
            cpu: 500m
            memory: 1Gi
          limits:
            cpu: 1000m
            memory: 2Gi
      volumes:
      - name: jenkins-home
        persistentVolumeClaim:
          claimName: jenkins-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: jenkins
  namespace: jenkins
spec:
  type: LoadBalancer
  selector:
    app: jenkins
  ports:
  - name: http
    port: 8080
    targetPort: 8080
  - name: agent
    port: 50000
    targetPort: 50000
```

```bash
# Deploy
kubectl apply -f jenkins-on-k8s.yaml

# Get Jenkins URL
kubectl get svc -n jenkins -w

# Get initial admin password
kubectl exec -it -n jenkins \
  $(kubectl get pod -n jenkins -l app=jenkins -o jsonpath='{.items[0].metadata.name}') \
  -- cat /var/jenkins_home/secrets/initialAdminPassword
```

---

### Example 4: Jenkins Pipeline – Deploy to Microservices K8s

```groovy
// Jenkinsfile for a single microservice (e.g., payment service)
pipeline {
    agent any

    environment {
        SERVICE       = "paymentservice"
        GCR_IMAGE     = "gcr.io/${GCP_PROJECT}/${SERVICE}:${BUILD_NUMBER}"
        NAMESPACE     = "default"
        MANIFEST_FILE = "./release/kubernetes-manifests.yaml"
    }

    stages {

        stage('Clone') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/yourorg/microservices-demo.git'
            }
        }

        stage('Build Service Image') {
            steps {
                dir("src/${SERVICE}") {
                    sh """
                        docker build -t ${GCR_IMAGE} .
                        gcloud auth configure-docker --quiet
                        docker push ${GCR_IMAGE}
                    """
                }
            }
        }

        stage('Update Manifest') {
            steps {
                sh """
                    # Update just this service's image in the manifest
                    sed -i 's|gcr.io/google-samples/microservices-demo/${SERVICE}:.*|${GCR_IMAGE}|g' \
                      ${MANIFEST_FILE}
                """
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh """
                    gcloud container clusters get-credentials online-boutique \
                      --zone us-central1-a

                    # Apply — idempotent, only changed service updates
                    kubectl apply -f ${MANIFEST_FILE} -n ${NAMESPACE}

                    # Wait for this service's rollout
                    kubectl rollout status deployment/${SERVICE} \
                      -n ${NAMESPACE} --timeout=5m
                """
            }
        }

        stage('Verify') {
            steps {
                sh """
                    kubectl get pods -n ${NAMESPACE} -l app=${SERVICE}
                    kubectl logs -l app=${SERVICE} --tail=20
                """
            }
        }
    }

    post {
        failure {
            sh """
                kubectl rollout undo deployment/${SERVICE} -n ${NAMESPACE}
                echo "❌ Deploy failed — rolled back ${SERVICE}"
            """
        }
        success {
            echo "✅ ${SERVICE}:${BUILD_NUMBER} deployed successfully"
        }
    }
}
```

---

### Example 5: Troubleshooting Script

```bash
#!/bin/bash
# Production troubleshooting script for microservices on K8s

echo "=== CLUSTER HEALTH ==="
kubectl get nodes
echo ""

echo "=== POD STATUS (all) ==="
kubectl get pods -o wide
echo ""

echo "=== FAILING PODS ==="
kubectl get pods | grep -E "CrashLoop|Error|Pending|ImagePull|OOM"
echo ""

echo "=== SERVICES & ENDPOINTS ==="
kubectl get svc
echo ""

echo "=== RECENT EVENTS (errors) ==="
kubectl get events --sort-by='.lastTimestamp' | grep -i "warning\|error\|failed"
echo ""

echo "=== RESOURCE USAGE ==="
kubectl top pods 2>/dev/null || echo "metrics-server not installed"
echo ""

# Check a specific service
check_service() {
    local SVC=$1
    echo "=== Checking: $SVC ==="
    kubectl describe deployment $SVC | grep -A5 "Events:"
    echo "Logs (last 20 lines):"
    kubectl logs -l app=$SVC --tail=20
    echo ""
}

# Check all key services
for svc in frontend paymentservice cartservice productcatalogservice; do
    check_service $svc
done

echo "=== FRONTEND EXTERNAL IP ==="
kubectl get service frontend-external | awk '{print $4}'
```

---

## 14. Scenario-Based Q&A

---

🔍 **Scenario 1:** A junior developer asks: "Our app works fine. Why are we breaking it into 11 separate services? It's so much more complex." How do you explain the business justification?

✅ **Answer:** At small scale, microservices add complexity — that's true. The value appears at scale: (1) **Team independence** — when you have 5 separate teams working on 5 features, they're constantly blocking each other in a monolith. With microservices, the payment team deploys their changes without waiting for the catalog team to finish. (2) **Fault isolation** — last month when our recommendation service had a memory leak in the monolith, it crashed the entire site including payments. With microservices, a recommendations bug only takes down recommendations. (3) **Independent scaling** — during sales, we scale checkout 10x without scaling everything else (wasteful cost). Start with a monolith, migrate when team size and complexity demand it — Netflix, Uber, Amazon all made this journey.

---

🔍 **Scenario 2:** Your manager notices that after deleting and redeploying the payment service, it came back up in 3 minutes. They ask: "Can we make the payment service zero-downtime so customers are never affected during deployments?"

✅ **Answer:** Yes — two approaches: (1) **Multiple replicas:** Change the paymentservice Deployment to `replicas: 2` or `replicas: 3`. With 2+ pods running, Kubernetes performs a rolling update — one pod stays running while the new version starts. Users never see downtime. (2) **PodDisruptionBudget:** Add a PodDisruptionBudget requiring at least 1 pod always running during disruptions. For the accidental deletion scenario specifically: implement RBAC to prevent deletion of production deployments without approval, and use GitOps so deployments can only happen through the pipeline (not manual kubectl commands). Zero-downtime deployments are the standard in production — always run at least 2 replicas of any customer-facing service.

---

🔍 **Scenario 3:** You're asked to add a new microservice — a "Reviews Service" — to the existing Online Boutique. What's the process?

✅ **Answer:** Five steps: (1) **Build the service** — write the code (pick any language), create a Dockerfile, test locally; (2) **Push Docker image** to GCR: `docker build -t gcr.io/project/reviewsservice:v1.0 .` → `docker push`; (3) **Add to the manifest** — append a new Deployment and Service section to `kubernetes-manifests.yaml` with `app: reviewsservice` labels; (4) **Deploy** — `kubectl apply -f kubernetes-manifests.yaml`. Only the new Reviews service is created (existing services unchanged — idempotent); (5) **Connect** — in the Frontend code, call `reviewsservice:PORT` via the service name. The whole process doesn't touch any existing service — this is the microservices benefit.

---

🔍 **Scenario 4:** During a code review, a teammate proposes communicating between microservices using pod IPs directly (e.g., `http://10.48.0.5:3000`). What problem do you flag?

✅ **Answer:** Pod IPs are **ephemeral** — they change every time a pod is restarted, rescheduled to a different node, or when rolling updates happen. If the product catalog pod at `10.48.0.5` crashes and restarts, it gets a new IP like `10.48.0.8`. Any service hardcoding `10.48.0.5` would break. The correct approach is always using **Kubernetes Service names**: `http://productcatalogservice:3550`. Kubernetes DNS resolves the service name to the current ClusterIP, which then routes to healthy pods. Service names never change; pod IPs change constantly. This is the entire reason Kubernetes Services exist — stable discovery in a dynamic environment.

---

🔍 **Scenario 5:** Your monitoring alert fires: "Frontend is returning errors." You ssh to the cluster. Walk through your troubleshooting steps.

✅ **Answer:** Systematic approach: (1) `kubectl get pods` — check if any pods show `CrashLoopBackOff`, `Error`, or `Pending`; (2) `kubectl get events --sort-by='.lastTimestamp' | grep Warning` — look for recent warnings; (3) `kubectl logs -l app=frontend --tail=50` — check frontend logs for errors; (4) `kubectl describe pod <frontend-pod>` — check Events at bottom for scheduling issues, OOM kills; (5) Check downstream services: `kubectl get pods | grep -v Running` — is a service the frontend calls (checkout, catalog) down? (6) `kubectl top pods` — check CPU/memory for resource exhaustion; (7) `kubectl get svc frontend-external` — verify the external IP is still assigned. In the class scenario, you'd quickly find a downstream service (like payment) shows 0/0 pods — `kubectl apply -f kubernetes-manifests.yaml` restores it.

---

🔍 **Scenario 6:** Your company has a monolithic Spring Boot application. Your team lead assigns you to "migrate to microservices on Kubernetes." Where do you start?

✅ **Answer:** This is a common real-world task. Approach: (1) **Identify service boundaries** — map out the monolith's modules (user management, cart, orders, notifications). These become your microservices. (2) **Strangler Fig Pattern** — don't rewrite everything at once. Extract one service at a time (start with the least risky, e.g., email notifications). Route traffic to the new microservice, keep everything else in the monolith. (3) **Containerize** — write a Dockerfile for each new service; push to ECR/GCR. (4) **Kubernetes manifests** — write Deployment + Service YAML for each. (5) **Data** — each microservice should eventually own its data. Start with shared DB (easier), progressively separate (harder). (6) **CI/CD per service** — each service gets its own Jenkins pipeline. This is a 6-18 month project, not a weekend task. The Kubernetes part (deploying containers) is actually the easy part — the hard part is defining service boundaries.

---

## 15. Interview Q&A

---

**Q1. What is the difference between monolithic and microservices architecture? When would you recommend each?**

**A:** A monolith packages all functionality — UI, business logic, database access — into a single deployable unit. All features deploy together, share one codebase, and run in one process. Microservices split functionality into independent services that communicate over a network. Each service has its own codebase, deployment cycle, and often its own database. Choose monolith when: you're early-stage (< 10 developers), your domain is simple, or you need to move fast with few people — monoliths are simpler to develop and debug initially. Choose microservices when: you have multiple teams that would block each other in a shared codebase, you need different scaling for different components, you've experienced monolith-related incidents (one module crashing the whole app), or you want to use different technologies for different problems. Most successful microservices architectures started as monoliths.

---

**Q2. How does a single `kubectl apply -f kubernetes-manifests.yaml` deploy 11 services at once?**

**A:** A Kubernetes manifest YAML file can contain multiple resource definitions separated by `---`. When you run `kubectl apply -f file.yaml`, Kubernetes reads every resource definition in the file sequentially. For each resource, it checks whether it exists in the cluster — if not, it creates it; if it exists and the definition has changed, it updates it; if unchanged, it does nothing. So the single file containing 11 Deployments and 11 Services results in 22 resource creation/update operations from one command. This is the power of declarative, idempotent infrastructure-as-code — the file is the source of truth for the entire application state.

---

**Q3. What happened when the payment service deployment was deleted? Why did the rest of the app keep working?**

**A:** When the paymentservice Deployment was deleted, all payment pods stopped running. Other services (frontend, cart, catalog) continued working because they don't depend on payment for normal browsing — they're independent services. The failure was isolated: only when a user attempted checkout (which calls paymentservice) did they see an error — "RPC unavailable." This demonstrates microservices fault isolation: one service's failure doesn't cascade to others. In a monolith, payment code failing would crash the entire process. Recovery was simple: `kubectl apply -f kubernetes-manifests.yaml` — since apply is idempotent, it only recreated the missing paymentservice without touching working services.

---

**Q4. Why do microservices in Kubernetes communicate using service names instead of pod IPs?**

**A:** Pod IPs are ephemeral — they change every time a pod is restarted, rescheduled, or updated. In a system with rolling deployments and auto-healing, pods constantly get new IPs. Hardcoding pod IPs would mean every service needs to be reconfigured every time any other service restarts — impossible at scale. Kubernetes Services provide stable, permanent endpoints. A Service has a fixed ClusterIP that never changes, and a DNS name (e.g., `paymentservice`) that resolves to that ClusterIP. Any pod in the cluster can call `grpc.Dial("paymentservice:50051")` and always reach the current payment pods, regardless of how many times they've restarted and changed IPs. The Service uses label selectors to dynamically find current pods.

---

**Q5. What is the difference between deleting a pod versus deleting a deployment?**

**A:** Deleting a **Pod** is temporary — the pod's parent ReplicaSet (managed by the Deployment) immediately detects the shortfall and schedules a replacement. Within 10-30 seconds, a new pod with a new name is running. The Deployment still exists, the ReplicaSet still exists, only the pod instance is gone and recreated. Deleting a **Deployment** removes the Deployment object, its ReplicaSet, AND all its pods. Nothing recreates them automatically because the manager (Deployment) is gone. Recovery requires re-creating the Deployment (via `kubectl apply` or `kubectl create deployment`). In class, this was demonstrated: deleting the emailservice pod caused 15 seconds of disruption before auto-healing; deleting the paymentservice deployment caused permanent failure until manual redeployment.

---

**Q6. How would you set up CI/CD for a microservices application on Kubernetes?**

**A:** Each microservice gets its own Jenkins pipeline triggered by its subdirectory changes. Pipeline stages: (1) git clone the monorepo; (2) detect which service changed (or trigger per service repo); (3) `docker build` the service's Dockerfile in `src/SERVICE_NAME/`; (4) `docker push` to GCR/ECR with the build number as tag; (5) Update the image tag in the Kubernetes manifest; (6) `kubectl apply -f kubernetes-manifests.yaml` — idempotent, only the changed service updates; (7) `kubectl rollout status` — wait for successful rollout; (8) On failure: `kubectl rollout undo` automatically. The key benefit: each service team deploys independently. Changing the payment service doesn't require retesting and redeploying the catalog service. Each service can have its own deployment frequency.

---

**Q7. What does "idempotent" mean in the context of `kubectl apply`, and why does it matter for CI/CD?**

**A:** Idempotent means running the same operation multiple times produces the same result as running it once. `kubectl apply` is idempotent because: first run creates resources; subsequent runs with the same YAML either update changed resources or skip unchanged ones — it never creates duplicates or errors on existing resources. This matters enormously for CI/CD because pipelines run on every commit. `kubectl create` would fail on the second run with "AlreadyExists." With `kubectl apply`, the pipeline can run after every code push without risk — it simply brings the cluster to the desired state described in the YAML file, regardless of the current state. It also handles partial failures gracefully: if a deployment was accidentally deleted, re-running the pipeline restores it without affecting anything else.

---

**Q8. What are the benefits of using a single `kubernetes-manifests.yaml` file for all microservices versus separate files per service?**

**A:** Single file benefits: simpler to manage initially, one command deploys everything, easier for beginners, good for demos and small teams. Separate file benefits (preferred for real teams): each team owns their service's manifest, easier code review (PR for one service only changes one file), selective deployment (`kubectl apply -f paymentservice.yaml` without touching others), better Git history (changes clearly attributed per service). The best practice is **organized separate files in a `k8s/` directory**: `k8s/paymentservice.yaml`, `k8s/cartservice.yaml`, etc. Use `kubectl apply -f k8s/` to deploy all at once, or `kubectl apply -f k8s/paymentservice.yaml` for a single service. The Google demo uses one file for simplicity of demonstration, but production teams use separate files organized by service.

---

← Previous: [`37_Pods_Deployments_Services_ReplicaSets_StatefulSets_&_Persistent_Volumes.md`](37_Pods_Deployments_Services_ReplicaSets_StatefulSets_&_Persistent_Volumes.md) | Next: [`39_Kubernetes_Advanced_Horizontal_Pod_Autoscaling_(HPA)_&_Troubleshooting.md`](39_Kubernetes_Advanced_Horizontal_Pod_Autoscaling_(HPA)_&_Troubleshooting.md) →