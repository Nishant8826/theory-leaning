# Kubernetes Networking

> 📌 **File:** 20_Kubernetes_Networking.md | **Level:** Full-Stack Dev → Networking Expert

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
```

---

## Kubernetes Networking Model

- Rule 1: Every Pod gets its own IP address.
- Rule 2: Pods can talk to any other Pod WITHOUT NAT.
- Rule 3: Nodes can talk to any Pod WITHOUT NAT.
- Rule 4: The IP a Pod sees for itself = the IP others see for it.

#### Diagram Explanation (The Highway System)
Kubernetes networking relies on a Container Network Interface (CNI):
- Imagine each Node (EC2 instance) is a local city. Inside that city, every Pod (app) gets its own street address (IP).
- Because of the CNI highway system, a pod in City 1 (Node 1) can send a data packet *directly* to a pod in City 2 (Node 2) without needing a complex post office or address translation (NAT).

---

## Services — Load Balancing & Discovery

Pods are ephemeral — their IPs change. K8s Services provide a stable IP and DNS name.

```yaml
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
```

### Service Types
- **ClusterIP (default):** Stable internal endpoint.
- **NodePort:** Access via Node IP + random port (30000-32767).
- **LoadBalancer:** Creates a cloud load balancer (ALB/NLB) automatically.
- **ExternalName:** Points to external service via CNAME.

---

## Ingress — External Traffic Routing

An Ingress manages external HTTP/S access to services (Layer 7 routing, like an ALB).

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  annotations:
    kubernetes.io/ingress.class: "alb"
    alb.ingress.kubernetes.io/scheme: "internet-facing"
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
```

---

## Network Policies (Firewall for Pods)

By default, all pods can talk to all pods. NetworkPolicies restrict traffic.

```yaml
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
              app: api
      ports:
        - protocol: TCP
          port: 27017
```

---

## Practice Exercises

### Exercise 1: Kubernetes Playground
Use Minikube or Katacoda to launch a deployment with 3 replicas of a node app. Expose them via a ClusterIP service.

### Exercise 2: Network Policy Verification
Apply a NetworkPolicy to allow access to a database Pod only from a specific app Pod. Verify that other Pods are blocked.

---

## Interview Q&A

**Q1: How does Kubernetes networking differ from Docker networking?**
> Docker: containers share a bridge network on one host. K8s: pods get real IPs across multiple nodes. K8s uses CNI plugins to create a flat network — any pod can reach any pod directly without NAT, even across nodes.

**Q2: What is a Kubernetes Service and why is it needed?**
> Pods are ephemeral — they get new IPs when they restart/scale. A Service provides a stable DNS name and IP that load-balances across matching Pods.

**Q3: What is an Ingress and how does it relate to ALB?**
> Ingress is a K8s resource defining HTTP routing rules (host/path → service). An Ingress Controller implements these rules. On AWS, the AWS Load Balancer Controller creates and configures ALBs automatically.

**Q4: How do you secure pod-to-pod communication?**
> NetworkPolicies act as firewalls for pods. By default, all pods can talk to all pods. You apply a deny-all baseline and explicitly allow needed connections.

**Q5: ECS Fargate vs EKS — when to use which?**
> ECS Fargate: simpler, less operational overhead, AWS-native, good for smaller teams and setups. EKS: more powerful, portable, standard Kubernetes API, better for complex microservices.

---

Prev : [19 Containers And Networking](./19_Containers_And_Networking.md) | Index: [00 Index](./00_Index.md) | Next : [21 Database Networking](./21_Database_Networking.md)
