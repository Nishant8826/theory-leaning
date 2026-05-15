# Kubernetes Services

## Why This Exists
In the previous topics, we learned that Deployments create and replace Pods dynamically. This creates a big problem: **Pods are ephemeral, and their IP addresses change every time they are recreated.**

If your frontend app needs to talk to your backend app, and the backend Pods keep changing IPs, your frontend will break.

**Services** solve this. A Service provides a **stable IP address and DNS name** that sits in front of a set of Pods. It acts as a internal load balancer. Instead of talking to Pods directly, your frontend talks to the Service, and the Service forwards the request to an available Pod.

## Real World Analogy
Think of a Service as a **Customer Support Hotline**.
- Customers (Frontend) don't call individual support agents (Pods) on their personal cell phones.
- They call the main hotline number (Service IP).
- The switchboard operator routes the call to any available agent.
- Even if agents quit and are replaced by new ones, the hotline number never changes.

## Core Concepts
- **Service**: An abstract way to expose an application running on a set of Pods.
- **Labels & Selectors**: Services use label selectors to know which Pods to send traffic to.
- **Endpoint**: The actual IP and port of the Pods backing the service (managed automatically by Kubernetes).

### Service Types
1. **ClusterIP** (Default): Exposes the service on a cluster-internal IP. Good for communication *inside* the cluster (e.g., frontend to backend).
2. **NodePort**: Exposes the service on each Node's IP at a static port (30000-32767). Good for quick testing or on-premise clusters.
3. **LoadBalancer**: Creates an external load balancer in the cloud (AWS, GCP, Azure). Good for exposing apps to the internet.

## Architecture / Flow

```text
[ Client / Frontend Pod ]
       │
       ▼ (Hits stable DNS/IP)
[ Kubernetes Service ]
       │
       ▼ (Discovers pods via labels)
+------------------------------------------+
|  [ Pod 1 ]    [ Pod 2 ]    [ Pod 3 ]     |
|  label: app=backend                      |
+------------------------------------------+
```

## Practical Commands

```bash
# Expose a deployment as a ClusterIP service
kubectl expose deployment my-web --port=80 --target-port=80

# List all services
kubectl get svc

# Get detailed information about a service
kubectl describe svc my-web

# See the actual pod IPs connected to the service
kubectl get endpoints my-web
```

## Hands-On Exercise
Let's create a Service declaratively.

1. Create a file named `service.yaml`:
   ```yaml
   apiVersion: v1
   kind: Service
   metadata:
     name: my-backend-service
   spec:
     type: ClusterIP
     selector:
       app: my-backend-app
     ports:
       - protocol: TCP
         port: 80         # Port exposed by the service
         targetPort: 5000 # Port the container is listening on
   ```
2. Apply it:
   ```bash
   kubectl apply -f service.yaml
   ```

## Mini Project
**Task**: Expose your application to the outside world using `NodePort`.

1. Modify your `service.yaml`:
   ```yaml
   apiVersion: v1
   kind: Service
   metadata:
     name: my-public-service
   spec:
     type: NodePort
     selector:
       app: my-web-app
     ports:
       - port: 80
         targetPort: 80
         nodePort: 30001 # Must be between 30000-32767
   ```
2. Apply it.
3. Now you can access your application from outside the cluster by visiting `<Node-IP>:30001`.

## Real Production Usage
- **LoadBalancer in Cloud**: In production on AWS or GCP, you use `type: LoadBalancer`. Kubernetes will automatically talk to the cloud provider and provision a real Load Balancer (like AWS ALB) with a public IP.
- **DNS Resolution**: Kubernetes has a built-in DNS service. Pods can reach a service simply by using its name (e.g., `http://my-backend-service`).

## Common Mistakes
- **Port vs TargetPort confusion**: 
  - `port` is the port number on the Service itself (what other apps hit).
  - `targetPort` is the port number the container is actually listening on.
- **Selector Mismatch**: If the selector in the service doesn't match the labels on the pods, the service will have no endpoints, and traffic will fail.

## Debugging Guide
- **Service not routing traffic**: Run `kubectl get endpoints <service-name>`. If it says `<none>`, your service cannot find any pods with the specified labels. Check your label selectors!

## Best Practices
- **Use Service Names for communication**: Never hardcode Pod IPs. Use the service name (DNS) for internal communication.
- **Define named ports**: Instead of using numbers like `8080`, name the port in the Pod spec (e.g., `name: http`) and reference the name in the Service.

## Interview Questions
1. **What is a Service in Kubernetes?**
   *Answer*: A Service is an abstraction that defines a logical set of Pods and a policy by which to access them, providing a stable IP address and DNS name.
2. **What are the three main types of Kubernetes Services?**
   *Answer*: ClusterIP (internal), NodePort (external via node port), and LoadBalancer (external via cloud provider).

## Summary
Services are the glue that holds microservices together in Kubernetes. They solve the problem of ephemeral Pod IPs by providing stable endpoints and load balancing.

---
Prev: [02_deployments.md](./02_deployments.md) | Index: [Index](../00_index.md) | Next: [04_ingress.md](./04_ingress.md)
