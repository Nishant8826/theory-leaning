# 36 — Kubernetes: Introduction, Architecture, Clusters, Namespaces & kubectl

> **Session:** Kubernetes Fundamentals (Batch 43 — CloudDevOpsHub with Vikas)
> **Covers:** Cluster creation on GCP, Namespace management, kubectl commands, Kubernetes features

---

## Table of Contents

1. [What is Kubernetes?](#1-what-is-kubernetes)
2. [Core Definitions](#2-core-definitions)
3. [Kubernetes Architecture](#3-kubernetes-architecture)
4. [Kubernetes Features](#4-kubernetes-features)
5. [Cluster Creation on GCP](#5-cluster-creation-on-gcp)
6. [Namespaces](#6-namespaces)
7. [kubectl Commands](#7-kubectl-commands)
8. [kubectl create vs kubectl apply](#8-kubectl-create-vs-kubectl-apply)
9. [YAML in Kubernetes](#9-yaml-in-kubernetes)
10. [Tech Stack Mapping](#10-tech-stack-mapping)
11. [Practical / Code Examples](#11-practical--code-examples)
12. [Scenario-Based Q&A](#12-scenario-based-qa)
13. [Interview Q&A](#13-interview-qa)

---

## 1. What is Kubernetes?

### What
Kubernetes (also written as **K8s** — because there are 8 letters between K and s) is an **open-source container orchestration platform** originally developed by Google, now maintained by CNCF (Cloud Native Computing Foundation).

It automates the **deployment, scaling, and management** of containerized applications.

### Why
- Docker lets you **run** containers. But what if you have 100 containers across 10 servers?
- You need something to **manage**, **restart on failure**, **scale**, and **distribute traffic** automatically.
- Kubernetes is exactly that — a **manager / conductor** for your containers.

### How
- You describe your desired state (e.g., "I want 3 replicas of my Node.js app running")
- Kubernetes continuously **watches** the actual state and **reconciles** it with the desired state
- If a pod crashes → it restarts it. If traffic spikes → it scales pods up.

### Impact

| Without Kubernetes | With Kubernetes |
|---|---|
| Manual container restarts | Auto self-healing |
| Manual scaling | Auto-scaling (HPA) |
| Uneven traffic distribution | Built-in load balancing |
| Hard to manage many servers | Unified control via master node |

---

## 2. Core Definitions

### Node
- **What:** A **VM (Virtual Machine)** with software/applications installed. In Kubernetes, it has Docker (or another container runtime) installed.
- **Types:**
  - **Master Node** — brain of the cluster, manages everything
  - **Worker Node** — does the actual work, runs your application containers
- **Why:** You need machines to run containers. Nodes are those machines.

```
+------------------+       +------------------+       +------------------+
|   Worker Node 1  |       |   Worker Node 2  |       |   Worker Node 3  |
|  [Pod] [Pod]     |       |  [Pod] [Pod]     |       |  [Pod] [Pod]     |
|  Docker Runtime  |       |  Docker Runtime  |       |  Docker Runtime  |
|  Kubelet Agent   |       |  Kubelet Agent   |       |  Kubelet Agent   |
+------------------+       +------------------+       +------------------+
         |                          |                          |
         +------------+-------------+-------------------------+
                      |
             +--------+--------+
             |   Master Node   |
             |  (Control Plane)|
             +-----------------+
```

---

### Cluster
- **What:** A **group of nodes** (VMs) managed by a single Master Node.
- **Ideal setup:** 2–3 worker nodes + 1 master node
- **Why:** Clustering gives you **high availability** and **distributed workloads**. If one node fails, others continue serving traffic.

```
CLUSTER
┌─────────────────────────────────────────────────────┐
│                                                     │
│   [Master Node]  ──manages──>  [Worker Node 1]      │
│                  ──manages──>  [Worker Node 2]      │
│                  ──manages──>  [Worker Node 3]      │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

### Container
- **What:** A **lightweight, portable, executable image** that contains your running application and all its dependencies.
- **Why:** Ensures the app runs the same everywhere — dev, staging, production.
- **Think of it as:** A sealed box with your app, code, runtime, libraries — all bundled.

---

### Pod
- **What:** The **smallest deployable unit** in Kubernetes. A Pod wraps one or more containers.
- **Why:** Kubernetes doesn't manage containers directly — it manages Pods.
- A Pod has its own IP address inside the cluster.

```
Pod
┌────────────────────────┐
│  Container (Node.js)   │
│  Container (Sidecar)   │  ← optional
│  Shared Network/Volume │
└────────────────────────┘
```

---

### kubectl
- **What:** The **command-line tool** used to communicate with and control a Kubernetes cluster.
- **Why:** Without it, you can't interact with the cluster from terminal/shell.
- **How:** It talks to the **API Server** (master node component) using the **kubeconfig** file for authentication.

---

### Kubelet
- **What:** An **agent** running on **every worker node**.
- **Why:** It is the link between the Master Node and Worker Node.
- **How:** 
  1. Master sends instructions (via API Server)
  2. Kubelet on the worker node **receives** those instructions
  3. Kubelet tells the container runtime (Docker) to **start/stop** containers
  4. Kubelet reports the **status** of the node back to the master

```
Master Node ──API Server──> Kubelet (on Worker) ──> Docker ──> Container
                                    ↑
                             Reports status back
```

---

### Namespace
- **What:** An **isolated virtual environment** within a cluster. Like a folder that groups related resources.
- **Why:** Separates teams/environments (dev, staging, prod) within the same physical cluster.
- **Default namespaces in K8s:** `default`, `kube-system`, `kube-public`, `kube-node-lease`

---

## 3. Kubernetes Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         MASTER NODE (Control Plane)                 │
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────┐  ┌──────────┐  │
│  │  API Server  │  │  Scheduler   │  │ Controller │  │   etcd   │  │
│  │  (Gateway)   │  │ (Assigns     │  │  Manager   │  │ (Config  │  │
│  │              │  │  pods→nodes) │  │            │  │  Store)  │  │
│  └──────┬───────┘  └──────────────┘  └────────────┘  └──────────┘  │
│         │                                                           │
└─────────┼───────────────────────────────────────────────────────────┘
          │  (via Kubelet)
          ↓
┌─────────────────────┐   ┌─────────────────────┐
│    Worker Node 1    │   │    Worker Node 2    │
│  ┌──────┐ ┌──────┐  │   │  ┌──────┐ ┌──────┐  │
│  │ Pod  │ │ Pod  │  │   │  │ Pod  │ │ Pod  │  │
│  └──────┘ └──────┘  │   │  └──────┘ └──────┘  │
│  Kubelet | Docker   │   │  Kubelet | Docker   │
└─────────────────────┘   └─────────────────────┘
```

### Master Node Components

| Component | Role |
|---|---|
| **API Server** | Entry point for all kubectl commands. Validates and processes requests. |
| **Scheduler** | Decides which worker node gets the new Pod based on resources available. |
| **Controller Manager** | Watches cluster state, ensures desired state matches actual state. |
| **etcd** | Distributed key-value store. Stores all cluster config and state data. |

### Worker Node Components

| Component | Role |
|---|---|
| **Kubelet** | Agent on every node. Executes commands from master. Reports status. |
| **Container Runtime** | Docker (or containerd). Actually runs the containers. |
| **kube-proxy** | Manages networking rules. Enables communication between pods and services. |

---

## 4. Kubernetes Features

### 4.1 Self-Healing
- **What:** K8s automatically detects and fixes failed pods/containers.
- **How:** The Controller Manager constantly checks if the actual pod count = desired count. If a pod dies → it creates a new one.
- **Impact:** Zero manual intervention for minor failures.

```
Desired State: 3 pods running
Actual State:  2 pods (1 crashed)
                ↓
K8s Auto-Creates 1 new pod → Back to 3 pods ✅
```

---

### 4.2 Auto-Scaling (HPA — Horizontal Pod Autoscaler)
- **What:** Automatically increases/decreases the number of pods based on CPU/memory usage or traffic.
- **Why:** Handles traffic spikes without manual intervention.
- **How:**
  1. You define a metric threshold (e.g., CPU > 70%)
  2. HPA monitors pod metrics
  3. When threshold crossed → HPA scales up pods
  4. When traffic drops → HPA scales down

```
Traffic Normal → 2 pods
Traffic Spike  → HPA triggers → 5 pods
Traffic Drops  → HPA triggers → 2 pods (scale down)
```

---

### 4.3 Automated Rollbacks
- **What:** If a new deployment causes failures, K8s automatically rolls back to the previous working version.
- **Why:** Prevents production downtime due to bad deployments.
- **How:** K8s keeps a rollout history. On failure detection, it reverts to the last stable ReplicaSet.

```
Deploy v2 → v2 fails health check
         → K8s detects failure
         → Rolls back to v1 automatically ✅
```

---

### 4.4 Load Balancing
- **What:** Distributes incoming traffic across multiple pods.
- **How:** Uses techniques like **round-robin** to evenly distribute requests.
- **Why:** No single pod gets overwhelmed. Ensures high availability.

```
User Request
     ↓
  [Service / Load Balancer]
   /       |        \
Pod 1    Pod 2    Pod 3
```

---

## 5. Cluster Creation on GCP

### Setup Done in Session
- Platform: **Google Cloud Platform (GCP)** — Google Kubernetes Engine (GKE)
- Cluster: **3 nodes** (1 per zone for high availability)
- Node config: **30GB disk, 2 vCPUs, 4GB RAM** per node
- Connection: **Cloud Shell** + `kubectl`

### Steps (GKE)
```bash
# Step 1: Create cluster in GCP Console or via gcloud CLI
gcloud container clusters create my-cluster \
  --num-nodes=3 \
  --disk-size=30 \
  --machine-type=e2-standard-2 \
  --region=us-central1

# Step 2: Get credentials (sets up kubeconfig)
gcloud container clusters get-credentials my-cluster --region=us-central1

# Step 3: Verify connection
kubectl cluster-info
kubectl get nodes
```

### kubeconfig File
- **What:** A config file (usually at `~/.kube/config`) that stores cluster connection details — server URL, credentials, context.
- **Why:** kubectl uses it to know **which cluster** to talk to and **how to authenticate**.
- **Analogy:** Like a saved password + server address book for your clusters.

---

## 6. Namespaces

### What
Namespaces are **virtual partitions** inside a Kubernetes cluster. They allow multiple teams or environments to share the same cluster without interfering with each other.

### Why
- Isolate **dev / staging / production** in one cluster
- Control **resource quotas** per team
- Apply **RBAC** (Role-Based Access Control) per namespace

### Default Namespaces

| Namespace | Purpose |
|---|---|
| `default` | Where your resources go if no namespace is specified |
| `kube-system` | Internal Kubernetes system components (DNS, scheduler, etc.) |
| `kube-public` | Publicly readable data, rarely used |
| `kube-node-lease` | Node heartbeat data for availability tracking |

### Namespace Architecture

```
CLUSTER
├── Namespace: default
│     ├── Pod: frontend
│     └── Pod: backend
├── Namespace: dev
│     ├── Pod: frontend-dev
│     └── Pod: backend-dev
└── Namespace: production
      ├── Pod: frontend-prod
      └── Pod: backend-prod
```

### Create Namespace — CLI
```bash
kubectl create namespace dev
kubectl create namespace production
```

### Create Namespace — YAML
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: dev
```
```bash
kubectl apply -f namespace.yaml
```

### Useful Namespace Commands
```bash
kubectl get ns                          # List all namespaces
kubectl get pods -n dev                 # List pods in 'dev' namespace
kubectl config set-context --current --namespace=dev  # Switch default namespace
```

---

## 7. kubectl Commands

### What
`kubectl` is the **CLI tool** to interact with your Kubernetes cluster. Every action — create, update, delete, inspect — goes through kubectl → API Server → cluster.

### Command Flow
```
You (terminal)
    ↓ kubectl command
  kubeconfig (auth)
    ↓
  API Server (Master Node)
    ↓
  Scheduler / Controller
    ↓
  Worker Node → Kubelet → Docker → Container
```

### Essential Commands

```bash
# Cluster Info
kubectl cluster-info                    # Show cluster endpoint info
kubectl config get-contexts             # Show all available contexts
kubectl config current-context          # Show active context

# Nodes
kubectl get nodes                       # List all worker nodes
kubectl describe node <node-name>       # Detailed info about a node

# Namespaces
kubectl get ns                          # List namespaces
kubectl create namespace <name>         # Create a namespace

# Pods
kubectl get pods                        # List pods in default namespace
kubectl get pods -n <namespace>         # List pods in specific namespace
kubectl get pods --all-namespaces       # List all pods across all namespaces
kubectl describe pod <pod-name>         # Detailed pod info
kubectl logs <pod-name>                 # View logs from a pod
kubectl exec -it <pod-name> -- bash     # SSH into a running pod

# Apply / Create
kubectl apply -f <file.yaml>            # Create or update resource from YAML
kubectl create -f <file.yaml>           # Create resource (fails if exists)
kubectl delete -f <file.yaml>           # Delete resource defined in YAML
kubectl delete pod <pod-name>           # Delete specific pod
```

---

## 8. kubectl create vs kubectl apply

### The Difference

| Feature | `kubectl create` | `kubectl apply` |
|---|---|---|
| **Use case** | First-time creation only | Create OR update |
| **If resource exists** | Throws error | Updates it |
| **Recommended for** | One-off object creation | CI/CD pipelines, repeated use |
| **Declarative?** | No (imperative) | Yes (declarative) |

### How to Remember
- **`create`** = "Make this for the first time"
- **`apply`** = "Make this happen — create if missing, update if existing"

```bash
# First time → both work
kubectl create -f deployment.yaml
kubectl apply -f deployment.yaml

# Second time with changes:
kubectl create -f deployment.yaml   # ❌ Error: already exists
kubectl apply -f deployment.yaml   # ✅ Updates the deployment
```

---

## 9. YAML in Kubernetes

### Why YAML
- Kubernetes resources are defined as YAML (or JSON) files
- YAML is human-readable and version-controllable (Git)
- Using `kubectl apply -f` with YAML files is the standard approach in production

### Basic Pod YAML
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-node-app
  namespace: dev
  labels:
    app: node-app
spec:
  containers:
    - name: node-container
      image: node:22-alpine
      ports:
        - containerPort: 3000
```

### Basic Deployment YAML (Production-style)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: node-app-deployment
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: node-app
  template:
    metadata:
      labels:
        app: node-app
    spec:
      containers:
        - name: node-app
          image: gcr.io/my-project/node-app:v1
          ports:
            - containerPort: 3000
          resources:
            requests:
              memory: "64Mi"
              cpu: "250m"
            limits:
              memory: "128Mi"
              cpu: "500m"
```

### YAML Key Fields Explained

| Field | Meaning |
|---|---|
| `apiVersion` | Which K8s API version to use (v1, apps/v1, etc.) |
| `kind` | Resource type: Pod, Deployment, Service, Namespace |
| `metadata` | Name, labels, namespace of the resource |
| `spec` | Actual desired configuration |
| `replicas` | How many pod copies to run |
| `selector` | How the Deployment finds its Pods (via labels) |
| `template` | Pod template used to create replicas |

---

## 10. Tech Stack Mapping

### Node.js / Next.js App on Kubernetes

```
Developer
  → Pushes code to GitHub
  → Jenkins pipeline triggers
  → Docker image built
  → Image pushed to GCP Artifact Registry
  → kubectl apply -f deployment.yaml
  → Kubernetes deploys pods across worker nodes
  → Service exposes app via Load Balancer
  → Users access app via public IP
```

### AWS Equivalent Services

| Kubernetes Concept | GCP Service | AWS Service |
|---|---|---|
| Cluster | GKE | EKS (Elastic Kubernetes Service) |
| Node | GCE VM | EC2 Instance |
| Container Registry | GCP Artifact Registry | ECR (Elastic Container Registry) |
| Load Balancer | GCP Load Balancer | AWS ALB / ELB |
| Persistent Storage | GCP Persistent Disk | EBS / EFS |

### Jenkins → Kubernetes Pipeline Flow

```
┌────────────────────────────────────────────────────────────┐
│                    Jenkins Pipeline                        │
│                                                            │
│  Stage 1: Checkout Code (Git)                              │
│  Stage 2: Build Docker Image                               │
│  Stage 3: Push to Container Registry (GCR / ECR)          │
│  Stage 4: kubectl apply -f k8s/deployment.yaml             │
│  Stage 5: Verify rollout (kubectl rollout status)          │
└────────────────────────────────────────────────────────────┘
```

---

## 11. Practical / Code Examples

### 11.1 Dockerfile for Node.js App
```dockerfile
# Stage 1: Build
FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Stage 2: Run
FROM node:22-alpine
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .
EXPOSE 3000
CMD ["node", "server.js"]
```

### 11.2 Kubernetes Service YAML (Expose App)
```yaml
apiVersion: v1
kind: Service
metadata:
  name: node-app-service
  namespace: production
spec:
  selector:
    app: node-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 3000
  type: LoadBalancer
```

### 11.3 HPA (Horizontal Pod Autoscaler) YAML
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: node-app-hpa
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: node-app-deployment
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

### 11.4 Jenkins Pipeline (Jenkinsfile)
```groovy
pipeline {
  agent any
  environment {
    IMAGE_NAME = "gcr.io/my-project/node-app"
    TAG = "${BUILD_NUMBER}"
  }
  stages {
    stage('Checkout') {
      steps { git 'https://github.com/myrepo/node-app.git' }
    }
    stage('Build Docker Image') {
      steps {
        sh "docker build -t ${IMAGE_NAME}:${TAG} ."
      }
    }
    stage('Push to Registry') {
      steps {
        sh "docker push ${IMAGE_NAME}:${TAG}"
      }
    }
    stage('Deploy to Kubernetes') {
      steps {
        sh "kubectl set image deployment/node-app-deployment node-app=${IMAGE_NAME}:${TAG} -n production"
        sh "kubectl rollout status deployment/node-app-deployment -n production"
      }
    }
  }
  post {
    failure {
      sh "kubectl rollout undo deployment/node-app-deployment -n production"
    }
  }
}
```

### 11.5 Full Deployment Steps (GCP)
```bash
# 1. Authenticate with GCP
gcloud auth login
gcloud config set project my-project-id

# 2. Configure Docker to use GCR
gcloud auth configure-docker

# 3. Build and push image
docker build -t gcr.io/my-project/node-app:v1 .
docker push gcr.io/my-project/node-app:v1

# 4. Create cluster and connect
gcloud container clusters create prod-cluster --num-nodes=3 --region=us-central1
gcloud container clusters get-credentials prod-cluster --region=us-central1

# 5. Deploy
kubectl create namespace production
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f hpa.yaml

# 6. Verify
kubectl get pods -n production
kubectl get svc -n production
```

---

## 12. Scenario-Based Q&A

🔍 **Scenario 1:** Your new v2 deployment is crashing all pods in production. Users are getting 500 errors.

✅ **Answer:** Kubernetes automated rollback kicks in. The Controller Manager detects that the new pods are failing their health checks (liveness/readiness probes). It automatically rolls back to the previous stable version (v1) using `kubectl rollout undo`. You can also manually trigger: `kubectl rollout undo deployment/node-app-deployment -n production`

---

🔍 **Scenario 2:** Your e-commerce app goes viral during a sale. Traffic is 10x normal load.

✅ **Answer:** HPA (Horizontal Pod Autoscaler) detects CPU utilization crossing 70%. It automatically spins up more pods (up to maxReplicas). The built-in Kubernetes Service load balancer distributes traffic using round-robin across all new pods. No manual intervention needed.

---

🔍 **Scenario 3:** You want dev, QA, and production teams to share one cluster but stay completely isolated.

✅ **Answer:** Create separate Namespaces: `dev`, `qa`, `production`. Apply ResourceQuotas per namespace to limit CPU/memory. Use RBAC to restrict which team can access which namespace. Each team deploys to their own namespace using `kubectl apply -f ... -n <namespace>`.

---

🔍 **Scenario 4:** A team member wants to connect to the cluster from their local laptop.

✅ **Answer:**
1. Install `kubectl` locally
2. Install `gcloud` CLI (for GCP) or `aws` CLI (for EKS)
3. Authenticate: `gcloud auth login`
4. Fetch credentials: `gcloud container clusters get-credentials prod-cluster --region=us-central1`
5. This populates `~/.kube/config` with the cluster context
6. Verify: `kubectl get nodes`

---

🔍 **Scenario 5:** A pod on worker node 2 crashes at 3 AM. No one is monitoring.

✅ **Answer:** Kubernetes self-healing handles it. The Controller Manager detects the pod count dropped below the desired replicas. It automatically creates a new pod (on the same or different node) to restore the desired state. No human action required.

---

🔍 **Scenario 6:** You update a deployment YAML file and run `kubectl create -f deployment.yaml`. It errors out.

✅ **Answer:** `kubectl create` fails if the resource already exists. You should use `kubectl apply -f deployment.yaml` instead, which creates if missing or updates if already present. `apply` is the correct command for day-2 operations and CI/CD pipelines.

---

## 13. Interview Q&A

**Q1. What is Kubernetes and why is it used?**

> Kubernetes is an open-source container orchestration platform that automates deployment, scaling, and management of containerized applications. It's used because manually managing containers across multiple servers is error-prone and unscalable. K8s provides self-healing, auto-scaling, load balancing, and declarative configuration.

---

**Q2. What is the difference between kubectl create and kubectl apply?**

> `kubectl create` is an imperative command used for first-time resource creation. It fails if the resource already exists. `kubectl apply` is declarative — it creates the resource if it doesn't exist or updates it if it does. `apply` is preferred in CI/CD pipelines because it's idempotent (safe to run multiple times).

---

**Q3. Explain the role of Kubelet in Kubernetes architecture.**

> Kubelet is an agent installed on every worker node. It acts as a bridge between the Master Node (Control Plane) and the worker node. It receives Pod specifications from the API Server, instructs the container runtime (e.g., Docker) to start/stop containers accordingly, and continuously reports the health and status of the node and its pods back to the master.

---

**Q4. Why is the kubeconfig file important and where is it located?**

> The kubeconfig file stores cluster connection details: the API server endpoint, authentication credentials (tokens/certs), and context information (which cluster/user/namespace to use). Without it, `kubectl` doesn't know which cluster to connect to or how to authenticate. It is located at `~/.kube/config` by default. The `KUBECONFIG` environment variable can override this path.

---

**Q5. What is a Namespace in Kubernetes? When would you use it?**

> A Namespace is a virtual partition within a cluster that provides isolation between groups of resources. You use Namespaces to separate environments (dev/staging/prod) within a single cluster, apply resource quotas per team, and implement RBAC security boundaries. Default namespaces include `default`, `kube-system`, `kube-public`, and `kube-node-lease`.

---

**Q6. Describe the communication flow when you run `kubectl` to create an NGINX pod.**

> 1. You run `kubectl apply -f pod.yaml`
> 2. kubectl reads `~/.kube/config` for auth details
> 3. kubectl sends the request to the **API Server** on the master node
> 4. API Server validates and stores the config in **etcd**
> 5. The **Scheduler** decides which worker node gets this pod
> 6. **Kubelet** on the chosen worker node receives the pod spec
> 7. Kubelet tells the container runtime (Docker) to pull the NGINX image
> 8. Container starts running inside a Pod on the worker node
> 9. Kubelet reports status back to the API Server

---

**Q7. What is HPA and how does it work?**

> HPA stands for Horizontal Pod Autoscaler. It automatically adjusts the number of pod replicas based on observed metrics (CPU, memory, custom metrics). You define min/max replicas and a threshold (e.g., CPU > 70%). When the threshold is crossed, HPA scales up pods. When load decreases, it scales them down. It requires the Metrics Server to be installed in the cluster.

---

**Q8. How would you isolate two teams sharing one Kubernetes cluster?**

> - Create separate Namespaces for each team (e.g., `team-alpha`, `team-beta`)
> - Apply **ResourceQuota** to each namespace to limit CPU/memory usage
> - Use **RBAC** (Role-Based Access Control) with Roles and RoleBindings to restrict each team to only their namespace
> - Apply **NetworkPolicies** to prevent cross-namespace pod communication if needed

---

**Q9. What happens if the Master Node fails?**

> If the master node goes down, the worker nodes continue running their existing pods (applications remain available). However, no new scheduling, scaling, or self-healing can happen until the master recovers. This is why production clusters use **multiple master nodes** (High Availability control plane) — typically 3 masters using etcd's consensus mechanism.

---

**Q10. What is etcd and why is it critical in Kubernetes?**

> etcd is a distributed key-value store used by Kubernetes as its **source of truth** for all cluster state and configuration data. It stores pod specs, node info, secrets, configmaps, and more. If etcd is lost without a backup, the entire cluster state is lost. This is why etcd backups are a critical part of Kubernetes disaster recovery planning.

---

← Previous: [`35_Image_Optimization_Multi-Stage_Builds_Container_Registries_&_Docker_vs_Kubernetes.md`](35_Image_Optimization_Multi-Stage_Builds_Container_Registries_&_Docker_vs_Kubernetes.md) | Next: [`37_Pods_Deployments_Services_ReplicaSets_StatefulSets_&_Persistent_Volumes.md`](37_Pods_Deployments_Services_ReplicaSets_StatefulSets_&_Persistent_Volumes.md) →
