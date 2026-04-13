# Kubernetes Networking

> 📌 **File:** 19_Kubernetes_Networking.md | **Level:** Full-Stack Dev → Networking Expert

---

## What is it?

Kubernetes (K8s) orchestrates containers at scale — managing deployment, scaling, and networking of containerized applications. K8s networking is more complex than Docker because it manages networking across multiple nodes, with its own DNS, load balancing, and network policies. AWS EKS is the managed Kubernetes service.

---

## Map it to MY STACK (CRITICAL)

```
Docker Compose (development):
  docker-compose up → 3 containers on ONE machine

ECS Fargate (production — simpler):
  Define task → AWS manages placement, networking, scaling
  Good for: small-medium teams, AWS-native shops

Kubernetes / EKS (production — powerful):
  Define pods, services, deployments → K8s manages EVERYTHING
  Good for: large teams, multi-cloud, complex microservices

┌──────────────────────────────────────────────────────────────────┐
│  When to use which:                                              │
│                                                                  │
│  1-5 services, AWS-only       → ECS Fargate (simpler)           │
│  5-50 services, complex       → EKS (more control)             │
│  Multi-cloud / hybrid         → Self-managed K8s               │
│  Solo dev / small team        → ECS or even plain EC2           │
│                                                                  │
│  K8s networking solves:                                          │
│  - Service discovery (DNS-based, automatic)                     │
│  - Load balancing (built-in, per-service)                       │
│  - Network isolation (NetworkPolicy)                             │
│  - Ingress routing (path/host-based, like ALB)                 │
│  - Secret management (Kubernetes Secrets)                       │
└──────────────────────────────────────────────────────────────────┘
```

---

## Kubernetes Networking Model

```
Rule 1: Every Pod gets its own IP address
Rule 2: Pods can talk to any other Pod WITHOUT NAT
Rule 3: Nodes can talk to any Pod WITHOUT NAT
Rule 4: The IP a Pod sees for itself = the IP others see for it

┌──────────────────────────────────────────────────────────────────┐
│  K8s Cluster                                                    │
│                                                                  │
│  Node 1 (EC2: 10.0.1.10)          Node 2 (EC2: 10.0.1.11)    │
│  ┌───────────────────────┐        ┌───────────────────────┐    │
│  │ Pod: api-abc (10.0.2.5)│       │ Pod: api-xyz (10.0.2.8)│   │
│  │ Container: node-app   │        │ Container: node-app   │    │
│  │ Port: 3000             │        │ Port: 3000             │    │
│  ├────────────────────────┤        ├────────────────────────┤    │
│  │ Pod: redis (10.0.2.6) │        │ Pod: mongo (10.0.2.9) │    │
│  │ Container: redis      │        │ Container: mongod     │    │
│  │ Port: 6379             │        │ Port: 27017           │    │
│  └───────────────────────┘        └───────────────────────┘    │
│                                                                  │
│  Pod 10.0.2.5 can reach Pod 10.0.2.9 directly — no NAT.       │
│  Even though they're on different nodes!                         │
│  (CNI plugin handles the cross-node networking)                 │
└──────────────────────────────────────────────────────────────────┘
```

---

## Services — Load Balancing & Discovery

```yaml
# Kubernetes Service = stable endpoint for a group of Pods
# Pods are ephemeral (restart, move, scale) — their IPs change.
# Services provide a STABLE DNS name and IP.

apiVersion: v1
kind: Service
metadata:
  name: api-service          # DNS name: api-service.default.svc.cluster.local
spec:
  selector:
    app: api                 # Route to all Pods with label app=api
  ports:
    - port: 80               # Service port (other pods use this)
      targetPort: 3000       # Container port (your Node.js listens here)
  type: ClusterIP            # Internal only (default)
```

### Service Types

```
┌────────────────────────────────────────────────────────────────────┐
│  Type          │ Access              │ Use Case                   │
├────────────────┼─────────────────────┼────────────────────────────┤
│  ClusterIP     │ Internal only       │ Service-to-service         │
│  (default)     │ api-service:80      │ communication              │
│                │                     │ Backend APIs, databases    │
│                │                     │                            │
│  NodePort      │ External via node   │ Development, testing       │
│                │ IP + random port    │ Not for production         │
│                │ (30000-32767)       │                            │
│                │                     │                            │
│  LoadBalancer  │ External via cloud  │ Production public access  │
│                │ load balancer       │ Creates an ALB/NLB        │
│                │                     │ automatically             │
│                │                     │                            │
│  ExternalName  │ DNS CNAME alias     │ Point to external service │
│                │                     │ (RDS, ElastiCache)        │
└────────────────┴─────────────────────┴────────────────────────────┘
```

### DNS in Kubernetes

```
Every Service gets a DNS name:

  <service>.<namespace>.svc.cluster.local

Examples:
  api-service.default.svc.cluster.local    → ClusterIP
  redis-service.default.svc.cluster.local  → ClusterIP
  
Shorthand (within same namespace):
  api-service       → works!
  redis-service     → works!

In your Node.js code:
  mongoose.connect('mongodb://mongo-service:27017/myapp');
  redis.connect('redis://redis-service:6379');
  
This is EXACTLY like Docker Compose naming — but across multiple nodes.
```

---

## Kubernetes Manifests for Your Stack

```yaml
# ──── Deployment: Node.js API ────
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-deployment
spec:
  replicas: 3                    # Run 3 instances
  selector:
    matchLabels:
      app: api
  template:
    metadata:
      labels:
        app: api
    spec:
      containers:
        - name: api
          image: 123456789.dkr.ecr.us-east-1.amazonaws.com/api:latest
          ports:
            - containerPort: 3000
          env:
            - name: MONGO_URI
              valueFrom:
                secretKeyRef:
                  name: db-secrets
                  key: mongo-uri
            - name: REDIS_URL
              value: "redis://redis-service:6379"
          resources:
            requests:
              memory: "256Mi"
              cpu: "250m"
            limits:
              memory: "512Mi"
              cpu: "500m"
          readinessProbe:         # K8s checks this before sending traffic
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 5
            periodSeconds: 10
          livenessProbe:          # K8s restarts pod if this fails
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 15
            periodSeconds: 20
---
# ──── Service: Internal Load Balancer ────
apiVersion: v1
kind: Service
metadata:
  name: api-service
spec:
  selector:
    app: api
  ports:
    - port: 80
      targetPort: 3000
  type: ClusterIP
---
# ──── Redis Deployment ────
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
        - name: redis
          image: redis:7-alpine
          ports:
            - containerPort: 6379
---
apiVersion: v1
kind: Service
metadata:
  name: redis-service
spec:
  selector:
    app: redis
  ports:
    - port: 6379
      targetPort: 6379
```

---

## Ingress — External Traffic Routing

```yaml
# Ingress = Layer 7 routing from internet to services
# Similar to: ALB with path-based routing + Nginx

apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  annotations:
    kubernetes.io/ingress.class: "alb"          # Use AWS ALB
    alb.ingress.kubernetes.io/scheme: "internet-facing"
    alb.ingress.kubernetes.io/certificate-arn: "arn:aws:acm:..."
    alb.ingress.kubernetes.io/listen-ports: '[{"HTTPS":443}]'
    alb.ingress.kubernetes.io/ssl-redirect: "443"
spec:
  rules:
    - host: api.myapp.com
      http:
        paths:
          - path: /api
            pathType: Prefix
            backend:
              service:
                name: api-service
                port:
                  number: 80
          - path: /
            pathType: Prefix
            backend:
              service:
                name: frontend-service
                port:
                  number: 80
    - host: admin.myapp.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: admin-service
                port:
                  number: 80
```

---

## Network Policies (Firewall for Pods)

```yaml
# Equivalent of Security Groups but for K8s Pods
# Default: ALL pods can talk to ALL pods (open network)
# NetworkPolicy restricts this

apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: db-network-policy
spec:
  podSelector:
    matchLabels:
      app: mongodb
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: api           # Only api pods can reach MongoDB
      ports:
        - protocol: TCP
          port: 27017

# Now: api pods → MongoDB ✅
#      any other pod → MongoDB ❌
```

---

## Commands & Debugging Tools

```bash
# Cluster info
kubectl cluster-info
kubectl get nodes -o wide

# Pods and Services
kubectl get pods -o wide                    # Shows Pod IPs
kubectl get services -o wide                # Shows Service IPs
kubectl get endpoints api-service           # Shows which Pods a Service routes to

# DNS debugging
kubectl exec -it <pod-name> -- nslookup api-service
kubectl exec -it <pod-name> -- nslookup redis-service

# Connectivity testing
kubectl exec -it <pod-name> -- curl http://api-service/health
kubectl exec -it <pod-name> -- nc -zv redis-service 6379

# Logs
kubectl logs <pod-name> --follow
kubectl logs -l app=api --all-containers    # All pods with label

# Describe (detailed info including events)
kubectl describe pod <pod-name>
kubectl describe service api-service

# Port forwarding (access service locally)
kubectl port-forward service/api-service 3000:80
# Now: curl http://localhost:3000/health hits the K8s service
```

---

## Common Mistakes

### ❌ Not Setting Resource Limits

```yaml
# ❌ No limits — one pod can consume all node memory and crash everything
containers:
  - name: api
    image: my-api

# ✅ Set requests (scheduling) and limits (hard cap)
containers:
  - name: api
    image: my-api
    resources:
      requests:
        memory: "256Mi"     # K8s schedules on nodes with this available
        cpu: "250m"
      limits:
        memory: "512Mi"     # Pod killed (OOMKilled) if exceeding this
        cpu: "500m"          # Pod throttled if exceeding this
```

### ❌ Not Using Readiness Probes

```yaml
# ❌ K8s sends traffic immediately — app might not be ready
# → 502 errors during startup

# ✅ Readiness probe — K8s waits until app is ready
readinessProbe:
  httpGet:
    path: /health
    port: 3000
  initialDelaySeconds: 5
  periodSeconds: 10
```

---

## Interview Q&A

**Q1: How does Kubernetes networking differ from Docker networking?**
> Docker: containers share a bridge network on one host. K8s: pods get real IPs across multiple nodes. K8s uses CNI plugins to create a flat network — any pod can reach any pod directly without NAT, even across nodes. K8s adds Services for stable endpoints and DNS-based discovery.

**Q2: What is a Kubernetes Service and why is it needed?**
> Pods are ephemeral — they get new IPs when they restart/scale. A Service provides a stable DNS name and IP that load-balances across matching Pods. ClusterIP for internal, LoadBalancer for external. It's the equivalent of an internal ALB.

**Q3: What is an Ingress and how does it relate to ALB?**
> Ingress is a K8s resource defining HTTP routing rules (host/path → service). An Ingress Controller implements these rules — on AWS, the ALB Ingress Controller creates and configures ALBs automatically based on Ingress definitions. It's declarative ALB management.

**Q4: How do you secure pod-to-pod communication?**
> NetworkPolicies act as firewalls for pods — restrict which pods can communicate on which ports. By default, all pods can talk to all pods. Apply deny-all baseline, then explicitly allow needed connections. Like Security Groups but for Kubernetes.

**Q5: ECS Fargate vs EKS — when to use which?**
> ECS Fargate: simpler, less operational overhead, AWS-native, good for < 10 services. EKS: more powerful, K8s ecosystem (Helm charts, operators), multi-cloud portable, better for complex microservices (> 10 services). ECS is AWS-only; K8s skills are transferable.


Prev : [18 Containers And Networking](./18_Containers_And_Networking.md) | Index: [0 Index](./0_Index.md) | Next : [20 Debugging Network Issues](./20_Debugging_Network_Issues.md)
