# ☸️ Kubernetes Basics – Complete Revision Guide

Welcome to the Kubernetes Basics module revision sheet. This document aggregates all key concepts, commands, configurations, YAML files, analogies, production best practices, and interview-prep notes from every topic in this directory, allowing you to perform a complete revision from a single file.

---

## 📌 Module Navigation
- [01. Pods](#01-pods)
- [02. Deployments](#02-deployments)
- [03. Services](#03-services)
- [04. Ingress](#04-ingress)
- [05. ConfigMaps](#05-configmaps)
- [06. Secrets](#06-secrets)
- [07. Persistent Volumes & Storage](#07-persistent-volumes--storage)
- [08. Health Checks & Probes](#08-health-checks--probes)
- [09. Namespaces](#09-namespaces)
- [10. Local K8s: Minikube](#10-local-k8s-minikube)
- [11. Local K8s: KinD](#11-local-k8s-kind)

---

## 01. Pods
🔗 **Full Lesson:** [01_pods.md](./01_pods.md)

* **Why It Exists**: The smallest deployable unit in Kubernetes. K8s does not run containers directly; it wraps them in a Pod to provide a shared environment (Network IP, Port space, Storage volumes) for tightly-coupled containers.
* **Real-World Analogy**: **Shared Apartment**. Roommates (containers) live together, share the same street address (IP), plumbing (Network), and storage rooms (Volumes).
* **Sidecar Pattern**: Running a main app container alongside a helper helper-container (e.g., logging sidecar shipping logs from a shared volume).

### Key Commands:
```bash
kubectl run my-nginx --image=nginx:alpine                                 # Start a naked Pod imperatively (Not for production)
kubectl get pods                                                          # List all running pods in current namespace
kubectl describe pod secure-app                                           # Detailed config/state analysis & event logs
kubectl delete pod my-nginx                                               # Delete a specific pod
```

### Pod Manifest (`pod.yaml`):
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-web-app
  labels:
    app: web
spec:
  containers:
  - name: nginx-container
    image: nginx:alpine
    ports:
    - containerPort: 80
```

---

## 02. Deployments
🔗 **Full Lesson:** [02_deployments.md](./02_deployments.md)

* **Why It Exists**: Pods are mortal. If a naked Pod dies, it is gone forever. Deployments manage the lifecycle of Pods, guaranteeing the desired number of replicas, scaling, self-healing, rolling updates, and rollbacks.
* **Real-World Analogy**: **Shift Manager at a Fast Food restaurant**. If a worker (Pod) gets sick, the manager (Deployment) immediately hires a replacement (new Pod) to keep the shift running.

### Key Commands:
```bash
kubectl create deployment my-web --image=nginx:alpine                      # Create deployment imperatively
kubectl scale deployment my-web --replicas=5                              # Scale replicas up/down
kubectl rollout status deployment my-web                                  # Monitor update status
kubectl rollout undo deployment my-web                                    # Revert/Rollback to the previous deployment revision
```

### Deployment Manifest (`deployment.yaml`):
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx # Must match template label
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.14.2
        ports:
        - containerPort: 80
```

> [!WARNING]
> **Avoid `:latest` tags**: If your image tag is `:latest`, Kubernetes will not trigger a Rolling Update when you apply changes, because the tag name remains identical. Always tag with explicit versions or commit SHAs.

---

## 03. Services
🔗 **Full Lesson:** [03_services.md](./03_services.md)

* **Why It Exists**: Pod IPs change dynamically every time they are recreated. Services solve this by acting as a stable DNS name and internal load balancer in front of Pods.
* **Real-World Analogy**: **Customer Support Hotline**. Customers (internal frontend) call the main hotline number (Service IP). The switchboard operator routes calls to any available agent (Pods). Even if agents change, the hotline remains the same.
* **Service Types**:
  1. **ClusterIP**: Exposes service internally within the cluster. (Default).
  2. **NodePort**: Exposes the service on a static port (30000-32767) on all cluster Nodes.
  3. **LoadBalancer**: Provisions a cloud-provider external Load Balancer (AWS ALB, GCP ELB).

### Key Commands:
```bash
kubectl expose deployment my-web --port=80 --target-port=80                # Expose deployment internally as ClusterIP service
kubectl get svc && kubectl get endpoints my-web                           # List services and inspect backend pod IP bindings
```

### Service Manifest (`service.yaml`):
```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-backend-service
spec:
  type: ClusterIP
  selector:
    app: my-backend-app # Targets pods matching this label
  ports:
    - protocol: TCP
      port: 80         # Port exposed by the Service
      targetPort: 5000 # Port the container application is listening on
```

---

## 04. Ingress
🔗 **Full Lesson:** [04_ingress.md](./04_ingress.md)

* **Why It Exists**: Exposing 10 different Services via 10 cloud LoadBalancers is extremely expensive. Ingress acts as a single entry point (smart gateway) routing traffic to different services based on paths (path-based routing) or hostnames (host-based routing).
* **Real-World Analogy**: **Hospital Main Entrance Receptionist**. Directs visitors (traffic) to Radiology (Service A) or Pharmacy (Service B) based on their destination inquiry.

### Key Commands:
```bash
kubectl get ingress                                                       # List all ingress rules
kubectl describe ingress my-app-ingress                                   # Display routing maps
kubectl logs -n ingress-nginx <ingress-controller-pod>                    # View controller server logs to debug routing
```

### Ingress Manifest (`ingress.yaml`):
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-app-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: myportfolio.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: backend-service
            port:
              number: 80
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend-service
            port:
              number: 80
```

> [!IMPORTANT]
> **Controller Prerequisite**: Creating an Ingress resource merely defines routing rules. An **Ingress Controller** (like Nginx Ingress Controller or Traefik) must be installed in the cluster to read and execute these configurations.

---

## 05. ConfigMaps
🔗 **Full Lesson:** [05_configmaps.md](./05_configmaps.md)

* **Why It Exists**: Separates non-sensitive configurations (API URLs, database names, feature flags) from application code or container images, making applications portable across Dev, QA, and Prod namespaces without rebuilding images.
* **Real-World Analogy**: **Video Game Settings Menu**. The game disc (Docker Image) is identical, but you configure parameters like difficulty or audio output (ConfigMap) at runtime.

### Key Commands:
```bash
kubectl create configmap app-config --from-literal=COLOR=blue             # Create ConfigMap imperatively
kubectl get cm && kubectl describe cm app-config                          # List and show config keys
```

### ConfigMap Injected in Pod (`pod.yaml`):
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-app
spec:
  containers:
  - name: my-app-container
    image: alpine
    command: ["sh", "-c", "echo The DB URL is $DB_URL"]
    env:
    - name: DB_URL # Env var name inside container
      valueFrom:
        configMapKeyRef:
          name: app-settings # Name of ConfigMap
          key: DATABASE_URL   # ConfigMap key
```

---

## 06. Secrets
🔗 **Full Lesson:** [06_secrets.md](./06_secrets.md)

* **Why It Exists**: ConfigMaps store plain text, which is insecure for passwords, API tokens, database credentials, or TLS certificates. Secrets store sensitive information securely using Base64 encoding, node memory pinning, and access isolation.
* **Real-World Analogy**: **Hotel Room Safe**. AC temperature and TV channel guides are like ConfigMaps (visible to anyone in the room). Passports, cash, and jewelry go into the wall Safe (Secrets).

### Key Commands:
```bash
kubectl create secret generic db-pass --from-literal=password=secret123   # Create generic secret
kubectl get secret db-pass -o jsonpath="{.data.password}" | base64 --decode # Retrieve and decode secret value
```

### Secret Manifest (`secret.yaml`):
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-credentials
type: Opaque
data:
  username: YWRtaW4=        # "admin" in Base64
  password: c2VjcmV0MTIz    # "secret123" in Base64
```

> [!WARNING]
> **Base64 is NOT encryption**: Base64 values can be decoded instantly. Never push `secret.yaml` files to git. In production, use integration engines like **AWS Secrets Manager**, **Sealed Secrets**, or **HashiCorp Vault**.

---

## 07. Persistent Volumes & Storage
🔗 **Full Lesson:** [07_volumes.md](./07_volumes.md)

* **Why It Exists**: Containers are ephemeral. Storage systems decouple the volume lifecycle from the Pod lifecycle, ensuring database storage (like MySQL or Postgres) persists after a container crash.
* **Three-Part System**:
  1. **PersistentVolume (PV)**: Physical storage block provisioned by cluster admins or cloud drivers.
  2. **PersistentVolumeClaim (PVC)**: A developer's ticket/request for storage (e.g., "I need 5GB").
  3. **StorageClass**: Automates PV creation on-demand when a PVC requests it.

### PVC Manifest (`pvc.yaml`):
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
```

### Mount PVC in Pod:
```yaml
spec:
  containers:
  - name: my-container
    image: alpine
    volumeMounts:
    - name: my-storage
      mountPath: /data
  volumes:
  - name: my-storage
    persistentVolumeClaim:
      claimName: my-pvc
```

---

## 08. Health Checks & Probes
🔗 **Full Lesson:** [08_health_checks.md](./08_health_checks.md)

* **Why It Exists**: Enables self-healing automation. If a container hangs, stalls, or crashes, Kubernetes detects it and automatically executes corrective restarts or routing changes.
* **Probe Types**:
  1. **Liveness Probe**: Determines if the container is running. If it fails, K8s kills the container and creates a new one.
  2. **Readiness Probe**: Determines if the container is ready to handle network traffic. If it fails, the Pod's IP is removed from Services' load balancer endpoints.
  3. **Startup Probe**: Secures slow-booting applications, disabling liveness/readiness checks until it finishes starting.

### Probe Manifest (`health-pod.yaml`):
```yaml
spec:
  containers:
  - name: app-container
    image: nginx
    livenessProbe:
      httpGet:
        path: /
        port: 80
      initialDelaySeconds: 5
      periodSeconds: 10
    readinessProbe:
      httpGet:
        path: /
        port: 80
      initialDelaySeconds: 3
      periodSeconds: 5
```

---

## 09. Namespaces
🔗 **Full Lesson:** [09_namespaces.md](./09_namespaces.md)

* **Why It Exists**: Provides virtual partitioning within a single physical cluster, allowing resource, security, and project isolation across multiple teams.
* **Real-World Analogy**: **Operating System folders**. A file named `draft.docx` can coexist in `Work` and `Personal` without conflict.

### Key Commands:
```bash
kubectl get namespaces                                                    # List all namespaces
kubectl create namespace staging                                          # Create a namespace
kubectl get pods -n staging                                               # List resources in a specific namespace
kubectl config set-context --current --namespace=staging                  # Set default namespace context
```

### Resource Quotas (Cluster Protection):
Enforces resource limits inside a namespace:
```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-quota
  namespace: staging
spec:
  hard:
    requests.cpu: "1"
    requests.memory: 1Gi
    limits.cpu: "2"
    limits.memory: 2Gi
```

---

## 10. Local K8s: Minikube
🔗 **Full Lesson:** [10_minikube.md](./10_minikube.md)

* **Why It Exists**: Setting up physical multi-node cloud clusters is complex. Minikube provisions a single-node local Kubernetes cluster inside a VM or container on your computer.
* **Real-World Analogy**: **Flight Simulator**. Learn K8s commands locally without paying cloud fees.

### Key Commands:
```bash
minikube start --driver=docker                                            # Start local cluster using Docker driver
minikube status                                                           # View cluster state
minikube dashboard                                                        # Launch the Kubernetes UI dashboard in browser
minikube service hello-minikube                                           # Retrieve nodeport URL to connect to local services
minikube stop && minikube delete                                          # Stop cluster and delete resources
```

---

## 11. Local K8s: KinD
🔗 **Full Lesson:** [11_kind.md](./11_kind.md)

* **Why It Exists**: An alternative local cluster manager. Unlike Minikube which runs inside a virtual machine, KinD (Kubernetes in Docker) uses Docker containers *as* cluster nodes. This makes startup extremely fast, lightweight, and ideal for CI/CD test automation.
* **Real-World Analogy**: **Cardboard Boxes inside a Storage Unit**. Each container is a box representing a Master Node or a Worker Node inside Docker.

### Key Commands:
```bash
kind create cluster --config kind-config.yaml                             # Create multi-node cluster from config
kind get clusters && kind delete cluster                                  # List and delete clusters
kind load docker-image my-app:latest                                      # Load local Docker image into KinD cluster nodes
```

### Multi-Node KinD Config (`kind-config.yaml`):
```yaml
apiVersion: kind.x-k8s.io/v1alpha4
kind: Cluster
nodes:
- role: control-plane
- role: worker
- role: worker
```

> [!IMPORTANT]
> **Image Pull Gotcha**: KinD nodes run as isolated Docker containers. If your Pod tries to pull a local image from your laptop, it will fail with `ImagePullBackOff`. You **must** load the image manually using `kind load docker-image <image_name>`.

---
