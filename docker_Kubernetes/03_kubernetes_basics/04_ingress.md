# Kubernetes Ingress

## Why This Exists
In the previous topic, we learned that **Services** (like LoadBalancer or NodePort) allow external traffic to reach your Pods. However, if you have 10 different applications in your cluster, creating a cloud LoadBalancer for each one is **expensive** and hard to manage.

**Ingress** solves this. It acts as a single entry point (a smart router) for your cluster. It allows you to route traffic to different services based on the URL path (e.g., `myapp.com/api` goes to the backend service, while `myapp.com/` goes to the frontend service) or the hostname (e.g., `app1.com` vs `app2.com`). It also handles SSL termination.

## Real World Analogy
Think of Ingress as the **Front Door Receptionist at a massive hospital**.
- Patients (Traffic) don't enter through different doors for different departments.
- Everyone enters through the **Main Entrance** (Ingress).
- The Receptionist reads the sign or asks where you are going (URL Path) and directs you to the Radiology department (Service A) or the Pharmacy (Service B).

## Core Concepts
- **Ingress Resource**: A set of rules that define how traffic should be routed to services.
- **Ingress Controller**: The actual server that implements the rules (usually Nginx, Traefik, or HAProxy). **Note**: Kubernetes does not include an Ingress Controller by default; you must install one (like the Nginx Ingress Controller).
- **Host-based Routing**: Routing traffic based on domain names (e.g., `billing.example.com` vs `shop.example.com`).
- **Path-based Routing**: Routing traffic based on URL paths (e.g., `example.com/api` vs `example.com/docs`).

## Architecture / Flow

```text
[ Client ]
   │
   ▼ (Domain: myapp.com)
[ Load Balancer ] (Single IP for the whole cluster)
   │
   ▼
[ Ingress Controller ] (Nginx / Traefik)
   │
   ├─ If path is /api ──► [ Backend Service ] ──► [ Backend Pods ]
   │
   └─ If path is / ────► [ Frontend Service ] ──► [ Frontend Pods ]
```

## Practical Commands

```bash
# List all ingress resources
kubectl get ingress

# Get detailed information about an ingress
kubectl describe ingress my-ingress

# View logs of the Ingress Controller (to debug routing issues)
kubectl logs -n ingress-nginx <ingress-controller-pod-name>
```

## Hands-On Exercise
Let's create an Ingress resource with path-based routing.

1. Create a file named `ingress.yaml`:
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
2. Apply it:
   ```bash
   kubectl apply -f ingress.yaml
   ```

## Mini Project
**Task**: Set up a local Ingress using **Minikube** to test routing.

1. Enable the ingress controller in Minikube:
   ```bash
   minikube addons enable ingress
   ```
2. Apply a frontend and backend deployment and service.
3. Apply the `ingress.yaml` file from the Hands-On exercise above.
4. Add the domain to your local hosts file (`C:\Windows\System32\drivers\etc\hosts`):
   ```text
   <minikube-ip> myportfolio.com
   ```
5. Visit `myportfolio.com` and `myportfolio.com/api` in your browser to see traffic being routed to different pods!

## Real Production Usage
- **SSL/TLS Certificates**: In production, Ingress handles SSL certificates. You can use **Cert-Manager** to automatically provision and renew Let's Encrypt certificates for your Ingress.
- **WAF (Web Application Firewall)**: Many cloud providers integrate their WAF with the Ingress controller to protect against attacks.

## Common Mistakes
- **No Controller Installed**: Creating an Ingress resource and wondering why it doesn't work. Remember, the resource is just a set of rules. You need the **Ingress Controller** running to read and execute those rules.
- **Incorrect `pathType`**: Using `Prefix` or `Exact` incorrectly can cause requests to fail with 404 errors.

## Debugging Guide
- **Ingress has no Address/IP**: If `kubectl get ingress` shows an empty `ADDRESS` column for a long time, it means your Ingress Controller is not running or is misconfigured.

## Best Practices
- **Use Annotations**: Use annotations to customize Nginx behavior (like enabling CORS, rate limiting, or setting max body size).
- **Separate Ingress per App**: Don't put all rules in one giant file. Create an Ingress resource for each microservice stack.

## Interview Questions
1. **What is the difference between a Service and an Ingress?**
   *Answer*: A Service provides load balancing for a set of pods within the cluster. An Ingress sits in front of multiple services and handles smart HTTP/HTTPS routing, SSL termination, and path-based forwarding from the outside world.
2. **What is an Ingress Controller?**
   *Answer*: It is the actual application (like Nginx) that runs in the cluster, listens for Ingress resources, and executes the routing rules.

## Summary
Ingress is the standard way to expose multiple HTTP/HTTPS services to the outside world in Kubernetes. It saves costs by sharing a single Load Balancer and provides powerful routing capabilities.

---
Prev: [03_services.md](./03_services.md) | Index: [Index](../00_index.md) | Next: [05_configmaps.md](./05_configmaps.md)
