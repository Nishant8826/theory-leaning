# 37 – Kubernetes Day 2: Pods, Deployments, Services, ReplicaSets, StatefulSets & Persistent Volumes

---

## Table of Contents

1. [Kubernetes Architecture – Deep Dive](#1-kubernetes-architecture--deep-dive)
2. [Pods – The Smallest Unit](#2-pods--the-smallest-unit)
3. [Services – Stable Communication Between Pods](#3-services--stable-communication-between-pods)
4. [Deployments – Managing Pod Lifecycle](#4-deployments--managing-pod-lifecycle)
5. [ReplicaSets – Guaranteeing Pod Count](#5-replicasets--guaranteeing-pod-count)
6. [StatefulSets – Pods with Unique Identities](#6-statefulsets--pods-with-unique-identities)
7. [Persistent Volumes & Claims (PV/PVC)](#7-persistent-volumes--claims-pvpvc)
8. [Auto-Healing in Practice](#8-auto-healing-in-practice)
9. [Exposing Applications – kubectl expose](#9-exposing-applications--kubectl-expose)
10. [Essential kubectl Commands](#10-essential-kubectl-commands)
11. [Tech Stack Mapping](#11-tech-stack-mapping)
12. [Visual Diagrams](#12-visual-diagrams)
13. [Code & Practical Examples](#13-code--practical-examples)
14. [Scenario-Based Q&A](#14-scenario-based-qa)
15. [Interview Q&A](#15-interview-qa)

---

## 1. Kubernetes Architecture – Deep Dive

### What
Kubernetes has a two-tier architecture: a **Control Plane** (master node) that makes all decisions, and **Worker Nodes** that do all the actual work. Every single piece of communication inside the cluster flows through the **API Server** — it is the central hub for everything.

> 💡 **Analogy:** The Control Plane is a company's head office — strategy, scheduling, decision-making happen here. Worker Nodes are the branch offices — actual work happens here. The API Server is the company's switchboard — every call, internal or external, goes through it.

---

### Control Plane Components

#### API Server (`kube-apiserver`)
- **What:** The ONLY entry point into the cluster — all requests (from kubectl, other components, CI/CD tools) go through it
- **What it does:** Authenticates requests, validates them, stores results in etcd, notifies other components
- **Think of it as:** The reception desk of a hotel — every guest, every staff member, every delivery goes through reception

#### etcd
- **What:** A distributed key-value database — the cluster's single source of truth
- **Stores:** Every piece of cluster state — what pods exist, which node they're on, what configs are set, what secrets exist
- **Critical:** If etcd is lost without backup, the cluster loses ALL knowledge of its state
- **Think of it as:** The hotel's central reservation system — if it crashes with no backup, no one knows which rooms are booked

#### Scheduler (`kube-scheduler`)
- **What:** Watches for newly created pods that have no node assigned, then decides which node they should run on
- **How it decides:** Available CPU/RAM on each node, pod resource requests, affinity/anti-affinity rules, taints and tolerations
- **Think of it as:** A hotel manager assigning arriving guests to available rooms based on their preferences and room availability

#### Controller Manager (`kube-controller-manager`)
- **What:** Runs multiple controllers in background loops, each watching for a specific condition and acting on it
- **Key controllers:**
  - **Node Controller:** Notices when nodes go down, marks them as unavailable
  - **Replication Controller:** Ensures the correct number of pods is always running
  - **Deployment Controller:** Manages rolling updates and rollbacks
- **Think of it as:** The hotel's maintenance department — constantly checking that everything is as it should be, fixing things when they're not

#### Cloud Controller Manager
- **What:** Integrates Kubernetes with the cloud provider's API (GCP, AWS, Azure)
- **Handles:** Creating cloud load balancers, managing cloud storage volumes, node lifecycle in the cloud

---

### Worker Node Components

#### Kubelet
- The agent running on every worker node
- Receives pod specifications from the API server
- Ensures containers described in those specs are running and healthy
- Reports node and pod status back to the master every few seconds

#### kube-proxy
- Handles **network communication** on each node
- Maintains network rules that allow pods to communicate with each other and with the outside world
- When a Service receives traffic on port 80, kube-proxy routes it to the correct pod
- **Think of it as:** The hotel's internal telephone operator — routes calls to the right room

#### Container Runtime
- The actual engine that starts and stops containers
- Kubernetes supports: Docker, containerd, CRI-O
- kubelet tells the container runtime what to run — the runtime does the actual work

---

### Full Communication Flow

```
kubectl run nginx --image=nginx

1. kubectl → reads kubeconfig → finds API server address
2. kubectl → HTTPS request → API Server (with auth token)
3. API Server → authenticates, authorizes
4. API Server → writes pod spec to etcd: "pending pod: nginx"
5. Scheduler → sees unscheduled pod in etcd
6. Scheduler → evaluates nodes → picks Node-2 (most available)
7. Scheduler → writes to etcd: "assign nginx to Node-2"
8. Kubelet on Node-2 → sees the assignment
9. Kubelet → tells container runtime: "start nginx container"
10. Container runtime → pulls nginx image → starts container
11. Kubelet → reports to API Server: "Pod running on Node-2"
12. API Server → updates etcd: "nginx pod: Running on Node-2"
13. kubectl → shows: pod/nginx created ✅
```

---

## 2. Pods – The Smallest Unit

### What
A **Pod** is the smallest deployable unit in Kubernetes. It's a wrapper around one or more containers that share:
- The same network IP address
- The same storage volumes
- The same lifecycle (they start and stop together)

> 💡 **Analogy:** A pod is like a shipping container on a cargo ship. The container holds one or more items (containers/apps). The items inside share the same space and are moved together. The ship (node) carries many containers (pods).

### Why
Kubernetes doesn't schedule individual containers directly — it schedules Pods. This abstraction allows:
- Grouping tightly related containers (e.g., an app + a logging sidecar) as one unit
- Giving them a single shared IP (they talk via `localhost`)
- Managing them as one atomic unit for scheduling and scaling

### Important Pod Facts

```
- Each Pod gets a unique IP address within the cluster
- Pod IPs are EPHEMERAL — when a pod is deleted and recreated, it gets a NEW IP
- This is why Services exist (stable endpoint regardless of pod IP changes)
- In practice: one container per pod (best practice for most cases)
- Pods are NOT self-healing — Deployments are what restart failed pods
```

### Creating a Pod

```bash
# Imperative (quick, not recommended for production)
kubectl run nginx --image=nginx:1.16

# Declarative (YAML — recommended)
kubectl apply -f pod.yaml
```

### Pod Lifecycle States

| State | Meaning |
|-------|---------|
| **Pending** | Pod accepted but containers not yet created (scheduling or image pull) |
| **Running** | At least one container is running |
| **Succeeded** | All containers exited successfully (code 0) |
| **Failed** | At least one container exited with non-zero code |
| **CrashLoopBackOff** | Container keeps crashing and restarting — something is wrong |
| **ImagePullBackOff** | Cannot pull the container image (wrong name, no access) |
| **Unknown** | Pod state cannot be determined (node communication issue) |

### Investigating a Pod

```bash
kubectl describe pod nginx   # Full details, events, errors
kubectl logs nginx           # Application output
kubectl logs -f nginx        # Follow logs live
kubectl exec -it nginx -- /bin/bash  # Shell into it
```

### Impact

| Running Containers Directly (Docker) | Using Pods (Kubernetes) |
|--------------------------------------|------------------------|
| No automatic restart | Deployment restarts failed pods |
| Single machine only | Spread across many nodes |
| No coordination between containers | Tightly coupled containers share network/storage |
| No health-based routing | Traffic only to healthy pods |

---

## 3. Services – Stable Communication Between Pods

### What
A **Service** is a Kubernetes object that provides a **stable network endpoint** for a set of pods. While pod IPs change every time a pod is recreated, a Service's IP and DNS name stay constant forever.

> 💡 **Analogy:** Pods are like employees who might change desks (IPs) every day. A Service is like the department's phone number — it never changes, even when employees move around. Calling the department number always connects you to whoever is available.

### Why Services Are Critical

```
Without Services:
  Pod A (IP: 10.0.1.5) calls Pod B at 10.0.1.8
  Pod B crashes → recreated → gets IP: 10.0.1.15
  Pod A still tries 10.0.1.8 → Connection refused ❌

With Services:
  Pod A calls "backend-service" (stable DNS name or ClusterIP)
  Service routes to whatever pod is currently running "backend"
  Pod B crashes → recreated → Service automatically finds new pod
  Pod A calls "backend-service" → still works ✅
```

### The Four Service Types

#### 1. ClusterIP (Default)
- **What:** Internal IP only — pods within the cluster can reach it, nothing outside
- **Use case:** Backend services, databases — things that should NOT be internet-facing
- **DNS name:** `service-name.namespace.svc.cluster.local`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: backend-svc
spec:
  type: ClusterIP    # Default — don't need to specify
  selector:
    app: backend
  ports:
  - port: 80
    targetPort: 3000
```

#### 2. NodePort
- **What:** Exposes the service on a specific port on EVERY node's external IP
- **Port range:** 30000–32767
- **Use case:** Development/testing, direct node access, not for production
- **Access:** `http://NODE_EXTERNAL_IP:30080`

```yaml
spec:
  type: NodePort
  ports:
  - port: 80
    targetPort: 3000
    nodePort: 30080    # Optional — auto-assigned if not specified
```

#### 3. LoadBalancer ✅ (Used in Class)
- **What:** Creates an external cloud load balancer (GCP/AWS/Azure) with a public IP
- **Use case:** Production internet-facing services
- **How:** Kubernetes talks to cloud provider API → provisions a real load balancer → assigns external IP
- **Access:** `http://EXTERNAL_IP`

```yaml
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 80
```

#### 4. ExternalName
- **What:** Maps a service name to an external DNS name
- **Use case:** Integrating external services (databases, APIs) into cluster service discovery

---

### How Services Find Pods — Label Selectors

Services don't target pods by name — they use **labels**. Any pod with matching labels automatically becomes part of the service.

```yaml
# Pod has label: app=nginx
metadata:
  labels:
    app: nginx

# Service selects pods with label: app=nginx
spec:
  selector:
    app: nginx
```

When a new pod is created with `app: nginx`, the service **automatically** starts routing traffic to it. When a pod is deleted, the service automatically stops routing to it. No manual configuration needed.

### Impact

| Without Services | With Services |
|-----------------|---------------|
| Pod-to-pod: hardcoded IPs that change | Stable DNS name forever |
| App breaks when pod restarts | App keeps working transparently |
| Manual load balancing between pods | Automatic round-robin distribution |
| No internet access | LoadBalancer type exposes publicly |

---

## 4. Deployments – Managing Pod Lifecycle

### What
A **Deployment** is a higher-level Kubernetes object that manages a set of identical pods and ensures the **desired state** is always maintained. It's what makes Kubernetes truly self-healing.

> 💡 **Analogy:** Imagine you're running a coffee shop with 3 baristas (pods). A Deployment is like a staffing manager who says: "There must ALWAYS be exactly 3 baristas working." If one calls in sick (pod crashes), the manager immediately hires a replacement. You never have fewer than 3.

### Why Not Just Create Pods Directly?

```
Problem with standalone pods:
  kubectl run nginx --image=nginx   (creates a Pod)
  Pod crashes
  → Pod stays dead — nothing recreates it ❌

Solution with a Deployment:
  kubectl create deployment nginx --image=nginx
  Pod crashes
  → Deployment controller detects: desired=1, actual=0
  → Automatically creates a new pod ✅
  → This is auto-healing
```

### What a Deployment Manages

```
Deployment
    │
    ├── Manages → ReplicaSet
    │                │
    │                ├── Pod 1 (replica)
    │                ├── Pod 2 (replica)
    │                └── Pod 3 (replica)
    │
    ├── Rolling Updates (zero downtime)
    ├── Rollbacks (revert to previous version)
    └── Scaling (add/remove replicas)
```

### Creating a Deployment

```bash
# Imperative
kubectl create deployment nginx --image=nginx:1.16 --replicas=3

# Declarative (preferred)
kubectl apply -f deployment.yaml
```

### Rolling Updates with Deployments

```bash
# Update the image version
kubectl set image deployment/nginx nginx=nginx:1.17

# What happens:
# 1. New ReplicaSet created for nginx:1.17
# 2. New pod (nginx:1.17) started → waits for Ready
# 3. Old pod (nginx:1.16) terminated
# 4. Repeat for all replicas
# Result: Zero downtime ✅

# Check rollout status
kubectl rollout status deployment/nginx

# View rollout history
kubectl rollout history deployment/nginx

# Rollback to previous version
kubectl rollout undo deployment/nginx
```

### Deployment vs Pod

| Pod | Deployment |
|-----|-----------|
| Runs containers | Manages pods |
| No self-healing | Auto-restarts failed pods |
| Manual scaling | Easy scaling: `--replicas=5` |
| No rolling updates | Built-in rolling updates |
| Use for: one-off tasks | Use for: all long-running apps |

---

## 5. ReplicaSets – Guaranteeing Pod Count

### What
A **ReplicaSet** ensures that a specified number of pod replicas are always running at any given time. It's the component that actually enforces the pod count.

> 💡 **Analogy:** A ReplicaSet is like a franchise rule: "There must always be exactly 3 open McDonald's locations in this city." If one closes, another must open immediately.

### Why
- Single pods provide no redundancy — one crash = full outage
- With 3 replicas across different nodes: one node dies, 2 replicas keep serving traffic

### Relationship: Deployment → ReplicaSet → Pods

```
You create/update a Deployment
         │
         ▼
Deployment creates a ReplicaSet
         │
         ▼
ReplicaSet creates and maintains Pods

When you update a Deployment (new image):
  Old Deployment → Old ReplicaSet (scaled to 0 — kept for rollback)
  New Deployment → New ReplicaSet (scaled to desired replicas)
```

### Rarely Create ReplicaSets Directly

```bash
# You almost never create ReplicaSets directly
# Create Deployments instead — they manage ReplicaSets for you

# But you can inspect them:
kubectl get replicasets
kubectl get rs  # shorthand
kubectl describe rs REPLICASET_NAME
```

### Self-Healing Demo (from Class)

```bash
# Create a deployment with 3 replicas
kubectl create deployment nginx --image=nginx:1.16 --replicas=3

# See 3 pods running
kubectl get pods
# nginx-abc1   Running
# nginx-def2   Running
# nginx-ghi3   Running

# Delete one pod manually
kubectl delete pod nginx-abc1

# Watch Kubernetes immediately create a replacement
kubectl get pods -w
# nginx-def2   Running   (still there)
# nginx-ghi3   Running   (still there)
# nginx-jkl4   Running   ← NEW pod automatically created ✅

# The ReplicaSet detected: desired=3, actual=2 → created new pod
```

---

## 6. StatefulSets – Pods with Unique Identities

### What
A **StatefulSet** manages pods that need **stable, unique identities** — each pod gets a predictable name, a dedicated persistent storage, and a stable network identity that persists across pod restarts.

> 💡 **Netflix Subscription Analogy (from class):** Think of Netflix plans — Basic, Standard, Premium. They all run the same Netflix application but each has different capabilities. You can't swap a Premium user onto a Basic pod just because Basic has available capacity. Each user has a specific, unique relationship with their pod. That's StatefulSet thinking — pods aren't interchangeable.

> 💡 **Banking Passbook Analogy (from class):** Different-colored passbooks in a bank represent different account types. A savings account holder can't be randomly assigned to a current account service. Each pod serves a specific identity.

### Deployment vs StatefulSet

| Feature | Deployment | StatefulSet |
|---------|-----------|-------------|
| **Pod names** | Random (nginx-x7k2p) | Ordered & stable (nginx-0, nginx-1, nginx-2) |
| **Pod identity** | Interchangeable | Unique — nginx-0 is always nginx-0 |
| **Storage** | Shared or none | Each pod gets its OWN persistent storage |
| **Startup order** | All at once | Sequential (0 first, then 1, then 2) |
| **Shutdown order** | Any order | Reverse order (2 first, then 1, then 0) |
| **DNS** | Service-based | Each pod has its own DNS name |
| **Use case** | Stateless apps (APIs, web servers) | Stateful apps (databases, message queues) |

### When to Use StatefulSet

```
Use StatefulSet for:
  ✅ Databases (MySQL, PostgreSQL, MongoDB replica sets)
  ✅ Message queues (Kafka, RabbitMQ)
  ✅ Distributed caches (Redis Cluster)
  ✅ Any app where each instance has unique identity/data

Use Deployment for:
  ✅ Web servers (NGINX, Apache)
  ✅ REST APIs (Node.js, Spring Boot)
  ✅ Worker processes
  ✅ Any app where instances are interchangeable
```

### StatefulSet Pod Naming

```bash
# Deployment creates pods with random names:
kubectl get pods
# shopping-cart-7d4f9b2c1-x7k2p   Running  ← random suffix
# shopping-cart-7d4f9b2c1-m3n8q   Running  ← random suffix

# StatefulSet creates pods with ordered, stable names:
kubectl get pods
# mysql-0   Running   ← always mysql-0 (primary)
# mysql-1   Running   ← always mysql-1 (replica)
# mysql-2   Running   ← always mysql-2 (replica)
# If mysql-1 crashes → recreated as mysql-1 (same name, same storage)
```

---

## 7. Persistent Volumes & Claims (PV/PVC)

### What
- **Persistent Volume (PV):** A piece of actual storage (disk, NFS, cloud storage) provisioned in the cluster
- **Persistent Volume Claim (PVC):** A request by a pod to USE a certain amount of that storage

> 💡 **Netflix Resume Feature Analogy (from class):** Imagine Netflix stores every movie/show on persistent volumes (the actual storage). Your user account (PVC) is a claim that says "I need access to this content and the ability to track where I stopped." When you log in on a new device, your claim (PVC) finds the right persistent volume (storage) and gives you exactly where you left off — your progress is persistent across devices and sessions.

### Why
Containers are ephemeral — when a pod is deleted, everything inside it is deleted too, including any data written to the container's filesystem. This is catastrophic for databases.

```
Without PV/PVC:
  MySQL pod stores data in container filesystem
  Pod crashes → recreated → ALL DATABASE DATA GONE ❌

With PV/PVC:
  MySQL pod mounts a PVC
  PVC is bound to a PV (actual disk storage)
  Pod crashes → recreated → mounts same PVC → data still there ✅
```

### How PV/PVC Works

```
Step 1: Admin creates a PersistentVolume (PV)
        → "Here is 50GB of SSD storage available in the cluster"

Step 2: Developer creates a PersistentVolumeClaim (PVC)
        → "I need 10GB of storage for my database"

Step 3: Kubernetes binds the PVC to a suitable PV
        → PV is 50GB, PVC needs 10GB → bound ✅

Step 4: Pod mounts the PVC
        → Data written to the PV — persists forever
        → Pod can be deleted, recreated — data remains
```

### Storage Classes (Dynamic Provisioning)

In cloud environments, you don't manually create PVs. **StorageClasses** automatically provision storage when a PVC is created:

```yaml
# PVC requests storage — cloud creates it automatically
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mysql-storage
spec:
  storageClassName: standard   # GCP's default SSD
  accessModes:
  - ReadWriteOnce              # One pod at a time
  resources:
    requests:
      storage: 20Gi
```

### Access Modes

| Mode | Meaning | Use Case |
|------|---------|---------|
| `ReadWriteOnce (RWO)` | One pod can read/write | Databases |
| `ReadOnlyMany (ROX)` | Many pods can read | Static content |
| `ReadWriteMany (RWX)` | Many pods can read/write | Shared file systems (NFS) |

---

## 8. Auto-Healing in Practice

### What
Auto-healing is Kubernetes automatically detecting and recovering from pod failures without human intervention. It's one of Kubernetes' most powerful and important features.

### How It Works – Step by Step

```
1. Deployment says: "I want 3 nginx pods running"
   Kubernetes stores this as "desired state" in etcd

2. Pod nginx-2 crashes (out of memory, bug, etc.)
   Container runtime reports to kubelet: "container stopped"

3. Kubelet reports to API Server: "Pod nginx-2 is not running"

4. Controller Manager checks:
   Desired: 3 pods
   Actual:  2 pods
   → MISMATCH — action needed!

5. Controller Manager instructs Scheduler to schedule a new pod

6. Scheduler picks a healthy node

7. Kubelet on that node creates a new container

8. New pod starts: nginx-4 (new name, same app)

Total time: 10-30 seconds
Human involvement: ZERO
```

### Demonstrating Auto-Healing (from Class)

```bash
# 1. Create deployment
kubectl create deployment nginx --image=nginx:1.16 --replicas=3

# 2. See 3 pods
kubectl get pods
# nginx-xxx1  Running
# nginx-xxx2  Running
# nginx-xxx3  Running

# 3. Delete a pod (simulating a crash)
kubectl delete pod nginx-xxx1

# 4. Immediately watch what happens
kubectl get pods -w
# nginx-xxx2  Running   (unchanged)
# nginx-xxx3  Running   (unchanged)
# nginx-xxx4  Pending   ← NEW pod being created
# nginx-xxx4  Running   ← AUTO-HEALED ✅

# Note: you deleted nginx-xxx1, a brand new pod nginx-xxx4 appeared
# The ReplicaSet detected the shortfall and self-healed
```

### What Auto-Healing Does NOT Cover

```
Auto-healing DOES handle:
  ✅ Container crash (OOM, segfault, bug)
  ✅ Node failure (pod moved to another node)
  ✅ Accidental pod deletion
  ✅ CrashLoopBackOff (retries with backoff)

Auto-healing does NOT handle:
  ❌ Bad application code (keeps crashing — CrashLoopBackOff infinitely)
  ❌ Wrong docker image (ImagePullBackOff — needs human fix)
  ❌ Data corruption inside the application
  ❌ Configuration errors in the deployment itself
```

---

## 9. Exposing Applications – kubectl expose

### What
`kubectl expose` creates a **Service** for a pod or deployment, making it accessible over the network — either internally (ClusterIP) or externally (LoadBalancer).

### Why
Pods aren't accessible outside the cluster by default. To allow traffic in (from users, other services), you must create a Service.

### How – kubectl expose from Class

```bash
# Expose a deployment as a LoadBalancer (external access)
kubectl expose deployment nginx \
  --type=LoadBalancer \
  --port=80 \
  --target-port=80 \
  --name=nginx-svc

# Watch for the external IP to be assigned
kubectl get svc -w
# NAME        TYPE           CLUSTER-IP     EXTERNAL-IP      PORT(S)
# nginx-svc   LoadBalancer   10.96.0.1      <pending>        80:31234/TCP
# nginx-svc   LoadBalancer   10.96.0.1      34.x.x.x ✅      80:31234/TCP

# Access at: http://34.x.x.x
```

### Expose via UI (GCP Console)

```
GKE Console → Workloads → Select your deployment
→ Actions → Expose
→ Port: 80, Target Port: 80
→ Service type: Load Balancer
→ Expose ✅
```

### The Port Mapping

```
External User
     │
     │  port: 80 (what user calls)
     ▼
LoadBalancer Service (External IP: 34.x.x.x)
     │
     │  targetPort: 80 (what container listens on)
     ▼
Pod (Container: NGINX listening on 80)
```

---

## 10. Essential kubectl Commands

### Pod Commands

```bash
# Create (imperative — quick testing)
kubectl run nginx --image=nginx:1.16

# List pods
kubectl get pods
kubectl get pods -o wide     # With node and IP info
kubectl get pods -w          # Watch in real time
kubectl get pods -A          # All namespaces

# Details
kubectl describe pod PODNAME  # Full info, events
kubectl logs PODNAME           # App output
kubectl logs -f PODNAME        # Follow live
kubectl logs --previous PODNAME # Previous container logs (after crash)

# Interact
kubectl exec -it PODNAME -- /bin/bash  # Shell access

# Delete
kubectl delete pod PODNAME
kubectl delete pod PODNAME --grace-period=0  # Force delete
```

### Deployment Commands

```bash
kubectl get deployment          # List all deployments
kubectl get deploy              # Shorthand

kubectl describe deployment NAME  # Full details

kubectl create deployment nginx --image=nginx:1.16 --replicas=3

kubectl scale deployment nginx --replicas=5  # Scale up/down

kubectl set image deployment/nginx nginx=nginx:1.17  # Rolling update

kubectl rollout status deployment/nginx  # Watch rollout progress
kubectl rollout history deployment/nginx  # See all versions
kubectl rollout undo deployment/nginx     # Rollback
kubectl rollout undo deployment/nginx --to-revision=2  # Rollback to specific version

kubectl delete deployment nginx
```

### Service Commands

```bash
kubectl get svc           # List services
kubectl get services      # Same

kubectl describe svc NAME  # Full details including endpoints

kubectl expose deployment nginx \
  --type=LoadBalancer \
  --port=80

kubectl delete svc NAME
```

### Node Commands

```bash
kubectl get nodes          # List nodes
kubectl get nodes -o wide  # With IPs, OS, kernel version
kubectl describe node NAME  # Full node info
kubectl top node           # CPU/memory usage per node (metrics-server needed)
```

### Quick Reference

| Command | What it does |
|---------|-------------|
| `kubectl get pods` | List pods |
| `kubectl get svc` | List services |
| `kubectl get deployment` | List deployments |
| `kubectl get rs` | List ReplicaSets |
| `kubectl get all` | List all resources |
| `kubectl get all -A` | All resources, all namespaces |
| `kubectl describe pod NAME` | Detailed pod info + events |
| `kubectl delete pod NAME` | Delete a pod |
| `kubectl logs NAME` | View pod logs |
| `kubectl exec -it NAME -- bash` | Shell into pod |

---

## 11. Tech Stack Mapping

### Complete Application Architecture on Kubernetes

```
User Request
     │
     ▼
DNS → LoadBalancer Service (External IP)
     │
     ▼
NGINX Ingress Controller (routing rules)
     │
     ├── /api/* → Backend Service (ClusterIP)
     │                │
     │                ├── Pod: Node.js API (Deployment, 3 replicas)
     │                └── Pod: Node.js API (Deployment, 3 replicas)
     │
     ├── /* → Frontend Service (ClusterIP)
     │            │
     │            └── Pod: React/Next.js (Deployment, 2 replicas)
     │
     └── Database Service (ClusterIP, headless for StatefulSet)
              │
              ├── Pod: MySQL-0 (StatefulSet, Primary) ─── PVC: mysql-0-pvc
              ├── Pod: MySQL-1 (StatefulSet, Replica) ─── PVC: mysql-1-pvc
              └── Pod: MySQL-2 (StatefulSet, Replica) ─── PVC: mysql-2-pvc
```

### Workload Types by Service

| Service | Kubernetes Object | Why |
|---------|------------------|-----|
| React / Next.js frontend | Deployment | Stateless, interchangeable pods |
| Node.js REST API | Deployment | Stateless, can scale horizontally |
| Python ML service | Deployment | Stateless workers |
| MongoDB / MySQL / PostgreSQL | StatefulSet | Unique identity per replica, persistent data |
| Redis (single) | Deployment + PVC | Stateless app, but needs storage |
| Redis Cluster | StatefulSet | Each node has identity |
| Message queue (Kafka) | StatefulSet | Order and identity matter |
| Batch job (data processing) | Job / CronJob | Runs once or on schedule |

---

## 12. Visual Diagrams

### Diagram 1: Kubernetes Object Hierarchy

```
CLUSTER
│
├── NAMESPACE: production
│     │
│     ├── DEPLOYMENT: shopping-cart
│     │     │
│     │     └── REPLICASET: shopping-cart-abc
│     │           │
│     │           ├── POD: shopping-cart-abc-x7k2p  → Container: node-api
│     │           ├── POD: shopping-cart-abc-m3n8q  → Container: node-api
│     │           └── POD: shopping-cart-abc-p9r4t  → Container: node-api
│     │
│     ├── SERVICE: shopping-cart-svc (LoadBalancer → routes to pods above)
│     │
│     ├── STATEFULSET: mysql
│     │     ├── POD: mysql-0 → PVC: mysql-0-pvc → PV: 20GB disk
│     │     ├── POD: mysql-1 → PVC: mysql-1-pvc → PV: 20GB disk
│     │     └── POD: mysql-2 → PVC: mysql-2-pvc → PV: 20GB disk
│     │
│     └── SERVICE: mysql-svc (ClusterIP — internal only)
│
└── NAMESPACE: monitoring
      └── DEPLOYMENT: grafana
```

---

### Diagram 2: Why Services Are Essential

```
WITHOUT SERVICE (pods communicate by IP)          WITH SERVICE
───────────────────────────────────────           ────────────
  Pod A (10.0.1.5) → talks to → Pod B (10.0.1.8)  Pod A → "backend-svc"
                                                              │
  Pod B crashes!                                             │
  Pod B' recreated at 10.0.1.15                    Service selector: app=backend
                                                             │
  Pod A still calls 10.0.1.8 → ❌ BROKEN           ├── Pod B' (10.0.1.15) ✅
                                                    └── Pod C  (10.0.1.22) ✅
                                                   
                                                   Service IP NEVER changes
                                                   Pod IPs change — irrelevant
```

---

### Diagram 3: Deployment vs StatefulSet

```
DEPLOYMENT (interchangeable pods)           STATEFULSET (unique pods)
──────────────────────────────              ──────────────────────────────
Pod names: random suffixes                  Pod names: ordered, stable
  web-7d4f9b-x7k2p                           db-0  (Primary)
  web-7d4f9b-m3n8q                           db-1  (Replica 1)
  web-7d4f9b-p9r4t                           db-2  (Replica 2)

All pods are identical                      Each pod has unique role/data
Any pod can serve any request               db-0 is PRIMARY — not interchangeable

Pod dies → new random name                  Pod dies → same name on restart
                                            db-1 dies → db-1 recreated
                                            Same storage, same identity

Use for: APIs, web servers                  Use for: databases, Kafka, Redis Cluster
```

---

### Diagram 4: PV/PVC Netflix Analogy

```
PERSISTENT VOLUMES (Netflix Library)          USER PVCs (Your Account)
────────────────────────────────              ──────────────────────────
PV: "All Netflix movies" (100TB)              PVC: "User John's streaming claim"
PV: "4K content library" (50TB)               PVC: "User Jane's HD claim"
PV: "Downloads library" (20TB)                PVC: "User Bob's basic claim"

                    Kubernetes binds PVC to appropriate PV

Result: When John logs in on new device:
  → PVC still bound to same PV
  → Resume exactly where he stopped
  → Data persists across device changes, pod restarts
```

---

### Diagram 5: Auto-Healing Flow

```
t=0:  Desired: 3 pods    Actual: 3 pods   ✅ All good
      [Pod-1] [Pod-2] [Pod-3]

t=5s: Pod-2 crashes!
      Desired: 3 pods    Actual: 2 pods   ⚠️ Mismatch!
      [Pod-1]         [Pod-3]

t=6s: Controller Manager detects mismatch
      → Sends scheduling request for 1 new pod

t=8s: Scheduler picks Node-2 (has capacity)
      → Assigns new pod to Node-2

t=12s: Kubelet on Node-2 starts container
       [Pod-1]  [Pod-4]  [Pod-3]

t=20s: New pod passes health check
       Desired: 3 pods    Actual: 3 pods   ✅ Healed!

Human involvement: 0 seconds
```

---

### Diagram 6: Service Types

```
ClusterIP (internal only):
  Pod A → ClusterIP:80 → Pod B  (stays inside cluster)

NodePort (via node's external IP):
  Internet → NodeIP:30080 → Service → Pod  (node must be accessible)

LoadBalancer (cloud-provisioned, production):
  Internet → EXTERNAL_IP:80 → Cloud LB → Service → Pod 1
                                                  → Pod 2
                                                  → Pod 3
  (cloud automatically provisions real load balancer)
```

---

## 13. Code & Practical Examples

### Example 1: Complete Pod YAML

```yaml
# nginx-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
  namespace: default
  labels:
    app: nginx
    version: "1.16"
    environment: dev
spec:
  containers:
  - name: nginx
    image: nginx:1.16         # Specific version from class
    ports:
    - containerPort: 80
    resources:
      requests:
        memory: "64Mi"
        cpu: "100m"           # 100 millicores = 0.1 CPU
      limits:
        memory: "128Mi"
        cpu: "200m"
    livenessProbe:            # Restart if this fails
      httpGet:
        path: /
        port: 80
      initialDelaySeconds: 10
      periodSeconds: 10
    readinessProbe:           # Only send traffic when this passes
      httpGet:
        path: /
        port: 80
      initialDelaySeconds: 5
      periodSeconds: 5
  restartPolicy: Always
```

```bash
kubectl apply -f nginx-pod.yaml
kubectl get pods
kubectl describe pod nginx-pod
kubectl logs nginx-pod
```

---

### Example 2: Deployment + Service (Full Stack)

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  namespace: default
  labels:
    app: nginx
spec:
  replicas: 3                 # 3 identical pods
  selector:
    matchLabels:
      app: nginx              # manages pods with this label
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1             # One extra pod during update
      maxUnavailable: 0       # Never reduce below 3 during update
  template:
    metadata:
      labels:
        app: nginx            # MUST match selector above
    spec:
      containers:
      - name: nginx
        image: nginx:1.16
        ports:
        - containerPort: 80
        resources:
          requests:
            memory: "64Mi"
            cpu: "100m"
          limits:
            memory: "128Mi"
            cpu: "200m"
---
# service.yaml (in same file, separated by ---)
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
  namespace: default
spec:
  type: LoadBalancer
  selector:
    app: nginx               # Routes traffic to pods with this label
  ports:
  - protocol: TCP
    port: 80                 # External port
    targetPort: 80           # Pod's container port
```

```bash
kubectl apply -f deployment.yaml
kubectl get deployment nginx-deployment
kubectl get pods -l app=nginx
kubectl get svc nginx-service
# Wait for EXTERNAL-IP to appear (2-3 minutes for cloud LB)
kubectl get svc -w
```

---

### Example 3: StatefulSet for MySQL

```yaml
# mysql-statefulset.yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: mysql
  namespace: production
spec:
  serviceName: "mysql"         # Headless service name (required)
  replicas: 3
  selector:
    matchLabels:
      app: mysql
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
      - name: mysql
        image: mysql:8.0
        ports:
        - containerPort: 3306
        env:
        - name: MYSQL_ROOT_PASSWORD
          valueFrom:
            secretKeyRef:
              name: mysql-secret
              key: root-password
        volumeMounts:
        - name: mysql-storage       # references the volumeClaimTemplate below
          mountPath: /var/lib/mysql
  volumeClaimTemplates:            # Each pod gets its OWN PVC automatically
  - metadata:
      name: mysql-storage
    spec:
      accessModes: ["ReadWriteOnce"]
      storageClassName: standard
      resources:
        requests:
          storage: 20Gi
# Result: mysql-0 gets mysql-storage-mysql-0 PVC (20Gi)
#         mysql-1 gets mysql-storage-mysql-1 PVC (20Gi)
#         mysql-2 gets mysql-storage-mysql-2 PVC (20Gi)
---
# Headless service for StatefulSet (required for DNS)
apiVersion: v1
kind: Service
metadata:
  name: mysql
  namespace: production
spec:
  clusterIP: None             # Headless — no load balancing, direct pod DNS
  selector:
    app: mysql
  ports:
  - port: 3306
# Pod DNS: mysql-0.mysql.production.svc.cluster.local
#          mysql-1.mysql.production.svc.cluster.local
```

---

### Example 4: PersistentVolumeClaim for Node.js App

```yaml
# pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: app-storage
  namespace: production
spec:
  accessModes:
  - ReadWriteOnce
  storageClassName: standard
  resources:
    requests:
      storage: 10Gi
---
# deployment using PVC
apiVersion: apps/v1
kind: Deployment
metadata:
  name: node-api
  namespace: production
spec:
  replicas: 1                  # ReadWriteOnce → only 1 pod can mount
  selector:
    matchLabels:
      app: node-api
  template:
    metadata:
      labels:
        app: node-api
    spec:
      containers:
      - name: node-api
        image: gcr.io/your-project/node-api:latest
        volumeMounts:
        - mountPath: /app/uploads    # Where app writes files
          name: app-data
      volumes:
      - name: app-data
        persistentVolumeClaim:
          claimName: app-storage     # References the PVC above
```

---

### Example 5: Jenkins Pipeline – Full K8s Deploy

```groovy
pipeline {
    agent any

    environment {
        IMAGE       = "gcr.io/${GCP_PROJECT}/shopping-cart:${BUILD_NUMBER}"
        NAMESPACE   = "production"
        APP         = "shopping-cart"
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

        stage('Update Deployment Image') {
            steps {
                sh """
                    # Get GKE credentials
                    gcloud container clusters get-credentials my-cluster \
                      --zone us-central1-a

                    # Update the image in the deployment
                    kubectl set image deployment/${APP} \
                      ${APP}=${IMAGE} \
                      -n ${NAMESPACE}

                    # Wait for rollout to complete
                    kubectl rollout status deployment/${APP} \
                      -n ${NAMESPACE} \
                      --timeout=5m
                """
            }
        }

        stage('Verify') {
            steps {
                sh """
                    kubectl get pods -n ${NAMESPACE} -l app=${APP}
                    kubectl get svc -n ${NAMESPACE} -l app=${APP}
                """
            }
        }
    }

    post {
        failure {
            sh """
                kubectl rollout undo deployment/${APP} -n ${NAMESPACE}
                echo "❌ Deployment failed — rolled back"
            """
        }
        success {
            echo "✅ Deployed ${IMAGE} to ${NAMESPACE}"
        }
    }
}
```

---

### Example 6: kubectl Auto-Healing Demo Script

```bash
#!/bin/bash
# Demonstrate Kubernetes auto-healing

echo "=== Creating Deployment with 3 replicas ==="
kubectl create deployment demo --image=nginx:1.16 --replicas=3

echo "Waiting for pods to start..."
kubectl wait --for=condition=ready pod -l app=demo --timeout=60s

echo ""
echo "=== Current pods ==="
kubectl get pods -l app=demo

# Get name of first pod
POD=$(kubectl get pods -l app=demo -o jsonpath='{.items[0].metadata.name}')

echo ""
echo "=== Deleting pod: $POD (simulating crash) ==="
kubectl delete pod $POD

echo ""
echo "=== Watch Kubernetes auto-heal (Ctrl+C to stop) ==="
kubectl get pods -l app=demo -w
# You'll see: old pod terminating, new pod creating, new pod running
# All within 10-20 seconds — completely automatic
```

---

## 14. Scenario-Based Q&A

---

🔍 **Scenario 1:** You deployed v2.0 of your API. Pods are starting but immediately returning 500 errors. Users are affected. What do you do in the next 30 seconds?

✅ **Answer:** Immediate rollback: `kubectl rollout undo deployment/shopping-cart -n production`. Kubernetes reverts to the previous ReplicaSet (v1.9 pods), replacing v2.0 pods gracefully — zero additional downtime. The command completes in seconds. Then investigate: `kubectl logs -l app=shopping-cart --previous -n production` to see the error in the v2.0 pods. Fix the bug, push v2.1. Kubernetes keeps the old ReplicaSet (v1.9) available specifically for this purpose — it doesn't delete it when you deploy, it just scales it to 0. Rollback is instantaneous because v1.9 is already there, just dormant.

---

🔍 **Scenario 2:** Your Node.js API pods keep getting OOM-killed (out of memory). You have 5 pods and CPU/traffic is fine, but memory keeps climbing. What Kubernetes concepts help you here?

✅ **Answer:** Two approaches: (1) **Auto-healing** is already working — pods restart automatically after OOM kill. But the root cause is a memory leak. (2) Set proper **resource limits** in the deployment: `limits.memory: "512Mi"` ensures pods are killed before they starve the entire node. (3) Add a **liveness probe** that checks a `/health` endpoint — if the app becomes unresponsive before OOM, Kubernetes restarts it proactively. (4) Use **HPA** with memory metrics to scale out before any single pod gets too loaded. Long-term fix: debug the memory leak in the application code. Kubernetes doesn't fix bad code — it manages the impact of it.

---

🔍 **Scenario 3:** Your company runs a PostgreSQL database in Kubernetes. Another team deleted a pod and when it restarted, all the database data was gone. Why did this happen and how do you prevent it?

✅ **Answer:** The database was running in a **Deployment** (or standalone pod) without a **PersistentVolumeClaim**. When the pod was deleted, the container filesystem was destroyed — including all PostgreSQL data. Fix: (1) Switch from Deployment to **StatefulSet** — the correct Kubernetes object for databases; (2) Add a **PersistentVolumeClaim** with `volumeClaimTemplates` in the StatefulSet — each pod gets dedicated persistent storage that survives pod restarts and deletions; (3) Enable regular **database backups** to S3/GCS regardless of PV (PVs aren't backup — they're just persistent storage). With StatefulSet + PVC, deleting `mysql-0` recreates it as `mysql-0` and mounts the same PVC with all data intact.

---

🔍 **Scenario 4:** You have a Node.js API running as a Deployment with 3 pods. A developer asks: "How do other services in the cluster call this API?" What do you tell them?

✅ **Answer:** Use the **Service's DNS name**, not the pod IPs. Create a ClusterIP Service for the deployment. Inside the cluster, the service is reachable at `api-service.namespace.svc.cluster.local` (or just `api-service` from within the same namespace). Example in Node.js: `const response = await fetch('http://api-service/users')`. The Service automatically load-balances across all 3 pods using round-robin. If a pod restarts and gets a new IP, nothing in the calling service needs to change — the Service DNS name never changes. Never hardcode pod IPs in your application code.

---

🔍 **Scenario 5:** Your application needs to handle a sudden 10x traffic spike during a product launch. You have auto-scaling configured. Walk through exactly what happens.

✅ **Answer:** With HPA configured: (1) Traffic spike hits → CPU on existing 3 pods climbs to 85% (threshold: 70%); (2) HPA detects this within 15 seconds; (3) HPA calculates: needs `ceil(3 × 85/70) = 4` pods to bring CPU to target; (4) HPA requests Deployment to scale to 4 pods; (5) Scheduler picks available nodes; (6) New pods start, pass readiness probes; (7) Service automatically includes new pods in rotation; (8) CPU drops to acceptable levels; (9) Traffic subsides → HPA scales back down after 5-minute cooldown. From a user perspective: zero impact, no downtime, automatic. Without HPA, pods would be CPU-throttled, requests would time out, and you'd wake someone up to manually scale at 3 AM.

---

🔍 **Scenario 6:** A team member deleted a deployment in the production namespace accidentally with `kubectl delete deployment shopping-cart`. What do you do?

✅ **Answer:** If you have a GitOps workflow with your manifests in Git: `kubectl apply -f k8s/deployment.yaml -n production` — the deployment is recreated within seconds. If you don't have manifests in Git (this is why you should): `kubectl create deployment shopping-cart --image=registry/shopping-cart:v1.5 --replicas=3 -n production` — but you need to know the last working image version. This scenario highlights why **Infrastructure-as-Code** matters: your YAML manifests in Git are the source of truth, and recovery is a single `kubectl apply` command. Also: implement RBAC to prevent junior team members from having delete permissions on production namespaces.

---

## 15. Interview Q&A

---

**Q1. What is a Pod in Kubernetes and why is it not recommended to run pods directly without a Deployment?**

**A:** A Pod is the smallest deployable unit in Kubernetes — a wrapper around one or more containers sharing network and storage. Running pods directly (without a Deployment) has a critical limitation: when a standalone pod crashes, it stays dead — nothing recreates it. A Deployment adds a management layer: it watches for pods that disappear and automatically recreates them (self-healing). Deployments also enable rolling updates (swap old pods for new without downtime), rollbacks (revert to previous version with one command), and easy scaling (`kubectl scale`). In practice, you almost never create standalone pods in production — you always create Deployments (or StatefulSets for stateful apps) and let them manage pods.

---

**Q2. Why are Kubernetes Services necessary? Can't pods just communicate directly?**

**A:** Pod IPs are ephemeral — every time a pod is deleted and recreated (crash, rolling update, node failure), it gets a completely new IP address. If Pod A communicates with Pod B by IP address and Pod B restarts, Pod A's hardcoded IP is now invalid — communication breaks. Services solve this with a stable, unchanging endpoint. A Service has a permanent ClusterIP and DNS name (e.g., `backend-service`). It uses label selectors to find current pods — when pods come and go, the Service automatically routes to whatever's running. Services also load-balance across multiple replicas. Additionally, LoadBalancer type Services provision external cloud load balancers, giving your application a stable public IP that never changes regardless of what happens to the underlying pods.

---

**Q3. What is the difference between a Deployment and a StatefulSet?**

**A:** A Deployment manages **stateless, interchangeable pods** — all replicas are identical, they can be created/deleted in any order, and if one crashes it's replaced by a new pod with a random name. Used for APIs, web servers, worker processes. A StatefulSet manages **stateful pods with unique identities** — pods have stable, ordered names (db-0, db-1, db-2) that persist across restarts, each pod has its own dedicated persistent storage (via volumeClaimTemplates), pods start in order (0 first) and stop in reverse order, and each pod has a stable DNS name. Used for databases (MySQL, PostgreSQL), message queues (Kafka), and distributed caches (Redis Cluster). The key distinction: if you swap two Deployment pods, nothing breaks. If you swap two StatefulSet pods (e.g., database primary and replica), things break catastrophically.

---

**Q4. Explain Kubernetes auto-healing. Is it the same as self-healing?**

**A:** They're the same concept. Kubernetes auto-healing (self-healing) means the system automatically detects and recovers from pod failures without human intervention. It works through the desired-state model: you declare "I want 3 replicas running" in a Deployment, and the ReplicaSet controller continuously compares desired state (3) with actual state. When a pod crashes, actual drops to 2 — the controller detects the mismatch and immediately schedules a new pod. The entire recovery typically takes 10-30 seconds. Important nuance: auto-healing restarts pods, but if the application itself has a bug causing immediate crash, it enters CrashLoopBackOff — Kubernetes keeps restarting but with exponential backoff delays. Auto-healing handles infrastructure failures; application bugs require developer intervention.

---

**Q5. What are Persistent Volumes and Persistent Volume Claims? Why are they needed?**

**A:** Containers have ephemeral storage — when a container is deleted, any data written to its filesystem is permanently lost. This is catastrophic for databases. Persistent Volumes (PV) are actual storage resources in the cluster — a piece of SSD disk, NFS share, or cloud storage. Persistent Volume Claims (PVC) are requests by pods to use storage — "I need 20GB of ReadWriteOnce storage." Kubernetes binds PVCs to appropriate PVs. The pod mounts the PVC, writes data to it — and that data exists on the PV independently of the pod's lifecycle. Delete and recreate the pod: it remounts the same PVC and all data is there. In cloud environments, StorageClasses enable dynamic provisioning — creating a PVC automatically provisions a cloud disk without needing a pre-existing PV.

---

**Q6. What is the difference between the four Kubernetes Service types?**

**A:** (1) **ClusterIP** (default): internal-only IP — pods within the cluster communicate using it, nothing outside can reach it. Used for databases and backend services. (2) **NodePort**: exposes the service on a port (30000-32767) on every node's external IP. Used for development/testing. (3) **LoadBalancer**: creates a cloud provider load balancer with an external public IP. Used for production internet-facing services — the one we used in class with `kubectl expose --type=LoadBalancer`. (4) **ExternalName**: maps a service to an external DNS name for integrating external services. For production workloads, LoadBalancer for external services and ClusterIP for internal service-to-service communication is the standard pattern.

---

**Q7. What happens when you run `kubectl delete pod` on a pod that belongs to a Deployment?**

**A:** The pod is immediately terminated. However, the Deployment's ReplicaSet detects the shortfall: desired count is 3, actual count is 2. Within seconds, it schedules a new pod. The new pod has a different name (random suffix), potentially runs on a different node, gets a new IP address — but is otherwise identical to the deleted pod (same image, same config). From the application's perspective: briefly one fewer replica serving traffic, then back to full count. This is actually how you can safely test auto-healing in production — deleting a pod is safe because Kubernetes immediately replaces it. If you want to permanently reduce replicas, scale the Deployment: `kubectl scale deployment/nginx --replicas=2`.

---

**Q8. How does a Kubernetes rolling update work and what makes it zero-downtime?**

**A:** When you update a Deployment (new image version), Kubernetes performs a rolling update rather than replacing all pods at once. With default settings (`maxSurge: 1, maxUnavailable: 0`): (1) Create one new pod with the new version; (2) Wait for it to pass readiness probe (confirm it's serving traffic); (3) Terminate one old pod; (4) Repeat until all pods are new version. At every point, at least the original number of pods is serving traffic — zero downtime. If the new pods fail readiness probes, the rollout pauses — the broken version never gets full traffic. You can monitor progress with `kubectl rollout status` and revert instantly with `kubectl rollout undo`. This is only possible because Kubernetes maintains multiple ReplicaSets — the old one is scaled to 0 but kept for rollback, the new one scales up.

---


← Previous: [`36_KubernetesIntroduction_Architecture_Clusters_Namespaces_&_kubectl.md`](36_KubernetesIntroduction_Architecture_Clusters_Namespaces_&_kubectl.md) | Next: [`38_Kubernetes_Microservices_Deployment_Monolithic_vs_Microservices_GKE_&_Real-World_E-Commerce_App.md`](38_Kubernetes_Microservices_Deployment_Monolithic_vs_Microservices_GKE_&_Real-World_E-Commerce_App.md) →