# Kubernetes

Docker packages your application, but running containers in production requires management. You need a system that monitors container health, automatically restarts crashed instances, load-balances client traffic, and scales resources dynamically. Kubernetes (K8s) is the industry-standard container orchestration platform. Understanding how to configure K8s YAML manifests ensures your Node.js services run reliably.

### Core Kubernetes Concepts
* **Pod**: The smallest deployable unit in Kubernetes, containing one or more tightly coupled containers sharing network and storage resources.
* **Deployment**: A controller that defines the desired state of Pods (e.g. "Run 3 replicas of the Node.js app container image") and manages rolling updates.
* **Service**: An abstraction that defines a logical set of Pods and a policy to load-balance traffic across them, providing a persistent network IP.
* **Ingress**: An API object that manages external HTTP/HTTPS access to services, handling SSL termination and path-based routing.

## Deep Dive

### Health Probes: Liveness vs. Readiness
Kubernetes monitors container health using Probes:
1. **Liveness Probe**: Checks if the container is running. If the liveness probe fails (e.g. the Node.js process is stuck in an infinite loop or has crashed), Kubernetes destroys the pod and spawns a new one.
2. **Readiness Probe**: Checks if the container is ready to accept user traffic. If the readiness probe fails (e.g. the application is still starting up or database pool connections dropped), Kubernetes removes the pod from the Service load-balancing pool, preventing users from receiving connection errors.

### Pod Lifecycle and the `preStop` Hook
When Kubernetes shuts down a pod (e.g., during rolling deployments):
1. The orchestrator updates the Service routing endpoints to stop sending traffic to the pod.
2. Network routing tables updates propagate asynchronously and can take a few seconds.
3. If K8s sends the `SIGTERM` signal to the container immediately, requests in transit will fail with connection drops.
4. **The Fix**: Configure a `preStop` hook script in the pod deployment configuration. This script runs a short sleep command (e.g. `sleep 10`) before sending the `SIGTERM` signal, allowing network routing changes to propagate and active requests to drain cleanly, supporting zero-downtime deployments.

## Visual Explanation

### Kubernetes Pod Shutdown Lifecycle and PreStop Hook
```text
  [ Rolling Update Initiated ]
               │
               ▼ (Asynchronous Network Event)
  [ Remove Pod from Service routing endpoints ] <──┐
               │                                   │ (Propagation delay: 5-10s)
               ▼                                   │
     [ Run preStop Hook: sleep 10 ] ───────────────┘
               │
               ▼ (Drains all active requests in transit)
     [ Send SIGTERM signal to Node.js process ]
               │
               ▼ (Node.js executes server.close() and exits)
  [ Container terminates cleanly (Zero downtime!) ]
```

## Real-World Example
Consider an Express API. You configure a Liveness Probe targeting `/health/live` and a Readiness Probe targeting `/health/ready`.
* `/health/live`: Returns `200 OK` instantly, indicating the process is alive.
* `/health/ready`: Queries the database and Redis clients. If the connection fails, it returns `503 Service Unavailable`, instructing Kubernetes to stop routing user requests to this pod until the database connection recovers.

## Code Examples

### Express Health Probes and Kubernetes Deployment Manifests

```javascript
// server.js (Express Application setup)
const express = require('express');
const mongoose = require('mongoose');

const app = express();

// 1. Liveness Probe Endpoint (Checks if process is responsive)
app.get('/health/live', (req, res) => {
  res.status(200).send('OK');
});

// 2. Readiness Probe Endpoint (Checks if database connection is active)
app.get('/health/ready', (req, res) => {
  const dbStatus = mongoose.connection.readyState;
  
  // connectionState: 1 = connected, 2 = connecting
  if (dbStatus === 1) {
    res.status(200).send('READY');
  } else {
    // Return 503 to instruct K8s to remove pod from Service endpoints pool
    res.status(503).send('NOT READY');
  }
});

app.listen(3000, () => console.log('App listening on port 3000'));
```

```yaml
# deployment.yaml (Kubernetes Deployment Manifest)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nodejs-api-deployment
  labels:
    app: nodejs-api
spec:
  replicas: 3 # Run 3 replicas of the container for high availability
  selector:
    matchLabels:
      app: nodejs-api
  template:
    metadata:
      labels:
        app: nodejs-api
    spec:
      containers:
      - name: nodejs-api-container
        image: myregistry.com/nodejs-api:v1.0.0
        ports:
        - containerPort: 3000
        
        # Inject environment configs from Kubernetes ConfigMap/Secrets
        env:
        - name: NODE_ENV
          value: "production"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: database-url

        # Configure Pod termination lifecycle
        lifecycle:
          preStop:
            exec:
              command: ["/bin/sh", "-c", "sleep 10"] # Wait for routing propagation

        # Health Probe Configurations
        livenessProbe:
          httpGet:
            path: /health/live
            port: 3000
          initialDelaySeconds: 15
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 3000
          initialDelaySeconds: 20
          periodSeconds: 5
```

## Best Practices
* **Separate Liveness and Readiness Probes**: Do not use the same endpoint for both probes. If your database experiences a temporary latency spike, a shared probe will cause Kubernetes to restart the container, worsening the issue. Use Readiness to pull the container out of rotation instead.
* **Configure Resources Limits**: Always define explicit `resources.limits` and `resources.requests` for CPU and Memory in your YAML files to prevent container memory hogging.
* **Graceful shutdowns**: Always handle the `SIGTERM` signal in your Node.js application to drain active requests when Kubernetes terminates a pod.

## Interview Questions

**Q:** What is a Pod in Kubernetes?

> **Answer:**
> A Pod is the smallest deployable unit in Kubernetes. It represents a single instance of a running process in your cluster and can contain one or more tightly coupled containers sharing network and storage resources.

**Q:** What is the difference between a Liveness Probe and a Readiness Probe?

> **Answer:**
> A Liveness Probe checks if the container is running. If it fails, Kubernetes kills and restarts the container. A Readiness Probe checks if the container is ready to accept network traffic. If it fails, Kubernetes pulls the container out of the Service load-balancing pool, preventing clients from receiving errors while the container recovers.

**Q:** Why is a `preStop` hook containing a `sleep` command necessary for achieving zero-downtime rolling updates in Kubernetes deployments?

> **Answer:**
> When a pod is deleted during updates, Kubernetes asynchronously updates the Service endpoints to stop routing traffic to the pod. However, this network routing update takes a few seconds to propagate across all cluster nodes.
> If Kubernetes sends a `SIGTERM` to the container immediately, the process stops accepting new requests while still receiving traffic in transit, causing connection errors. A `preStop` hook containing a `sleep 10` command pauses container shutdown, allowing routing updates to propagate and active requests to drain cleanly before `SIGTERM` is sent.

**Q:** How would you architecture a auto-scaling Kubernetes cluster for a high-concurrency Node.js WebSocket service? What scaling policies, Ingress configurations, and telemetry are required?

> **Answer:**
> To scale WebSockets in Kubernetes:
> 1. **Configure Ingress**: WebSockets are stateful, long-lived TCP connections. Use an Ingress controller (like Nginx Ingress) configured with **session affinity** (sticky sessions) if using HTTP fallback polling, or configure Layer 4 routing (TCP load balancing) to bypass HTTP parsing overhead.
> 2. **Tuning Termination Grace Period**: WebSocket connections can last for hours. Set a large `terminationGracePeriodSeconds` (e.g. 300 seconds) in your pod specifications to allow clients to disconnect slowly during deployments without being cut off.
> 3. **Auto-scaling Policies**: Standard CPU-based scaling fails for WebSockets because active connections consume memory (RAM) but minimal CPU. Configure the **Horizontal Pod Autoscaler (HPA)** to scale based on custom metrics like the active connection count or memory usage.
> 4. **Telemetry and Monitoring**: Instrument Node.js pods with Prometheus metrics tracking active socket counts, heap memory, and socket disconnect events to manage scale.

---
Previous : [75_Docker.md](75_Docker.md) | Index : [00_index.md](00_index.md) | Next : [77_CI_CD.md](77_CI_CD.md)
