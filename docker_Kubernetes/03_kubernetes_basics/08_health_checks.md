# Kubernetes Health Checks (Probes)

## Why This Exists
In a traditional server setup, if an application crashes or gets stuck in an infinite loop, a human administrator usually has to log in and restart it. 

Kubernetes is designed to be **self-healing**. To do this, it needs a way to know:
1.  Is the container still alive? (If not, restart it).
2.  Is the container ready to receive web traffic? (If not, don't send users to it yet).

**Probes** are health checks that Kubernetes runs periodically against your containers to answer these questions.

## Real World Analogy
Think of Health Checks like a **Pilot and a Co-Pilot checking on each other**.
- **Liveness Probe**: The Co-Pilot asks the Pilot every 5 minutes, *"Are you awake?"*. If the Pilot doesn't answer, the Co-Pilot takes over (Restarts the container).
- **Readiness Probe**: Before opening the airplane doors for passengers, the flight attendant asks the Pilot, *"Are you ready to take off?"*. If the Pilot says no (still loading fuel), passengers wait outside (No traffic sent to the Pod).

## Core Concepts
Kubernetes has 3 types of Probes:
1.  **Liveness Probe**: Determines if a container is running. If it fails, Kubernetes kills the container and creates a new one.
2.  **Readiness Probe**: Determines if a container is ready to respond to requests. If it fails, Kubernetes removes the Pod's IP from the Service's Load Balancer so no traffic reaches it.
3.  **Startup Probe**: Used for slow-starting applications. It disables liveness and readiness checks until the app is fully started up.

## Architecture / Flow

```text
[ Kubelet ] (Node Agent)
   │
   ├─► 1. Liveness Check? ──► [ Container ] (Success? Keep running. Fail? Kill & Restart)
   │
   └─► 2. Readiness Check? ─► [ Container ] (Success? Send traffic. Fail? Stop traffic)
```

## Practical Commands

```bash
# Describe pod to see probe results in the Events section
kubectl describe pod <pod-name>

# Check how many times a container has restarted due to liveness failure
kubectl get pods
```

## Hands-On Exercise
Let's create a Pod with both Liveness and Readiness probes.

1. Create a file named `health-pod.yaml`:
   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     name: health-check-demo
   spec:
     containers:
     - name: app-container
       image: nginx
       # Liveness probe checks if the container is alive
       livenessProbe:
         httpGet:
           path: /
           port: 80
         initialDelaySeconds: 5  # Wait 5 seconds before checking
         periodSeconds: 10       # Check every 10 seconds
       # Readiness probe checks if it's ready for traffic
       readinessProbe:
         httpGet:
           path: /
           port: 80
         initialDelaySeconds: 3
         periodSeconds: 5
   ```
2. Apply it:
   ```bash
   kubectl apply -f health-pod.yaml
   ```

## Mini Project
**Task**: Create a Pod with a failing liveness probe and watch it restart.

1. Create a Pod that points its liveness probe to a non-existent path like `/broken`.
2. Apply the Pod.
3. Run `kubectl get pods -w` and watch the `RESTARTS` count increase as Kubernetes kills and restarts it repeatedly.

## Real Production Usage
- **Zero-Downtime Deployments**: During a rolling update, Readiness Probes ensure that the old Pod is only destroyed *after* the new Pod is fully ready to take over traffic.

## Common Mistakes
- **Identical Liveness and Readiness Probes**: Using the exact same endpoint for both. If your database goes down, your app might fail the readiness probe (good, stop traffic), but if it also fails the liveness probe, Kubernetes will restart the container (bad, restarting won't fix the database issue).
- **Probes too aggressive**: Setting `periodSeconds: 1` and `failureThreshold: 1`. A tiny network glitch could cause your container to restart unnecessarily.

## Debugging Guide
- **Pod is running but receiving no traffic**: Check if the Readiness probe is failing. Run `kubectl describe pod` and look at the "Events" at the bottom.

## Best Practices
- **Create a dedicated health endpoint**: Create a simple `/health` or `/ready` endpoint in your code that returns HTTP 200 without doing heavy database queries.

## Interview Questions
1. **What is the difference between Liveness and Readiness probes?**
   *Answer*: Liveness probe decides when to **restart** a container. Readiness probe decides when to **send traffic** to a container.
2. **What is a Startup Probe used for?**
   *Answer*: It is used for applications that take a long time to start up. It prevents the liveness probe from killing the container before it finishes booting.

## Summary
Probes are the secret to Kubernetes' self-healing capabilities. By properly configuring them, you ensure your application is always available and stable without manual intervention.

---
Prev: [07_volumes.md](./07_volumes.md) | Index: [Index](../00_index.md) | Next: [09_namespaces.md](./09_namespaces.md)
