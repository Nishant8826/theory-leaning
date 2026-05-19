# Autoscaling

## Why This Exists
Web traffic isn't constant. If you buy enough servers for your absolute maximum peak traffic (like Black Friday), you waste thousands of dollars 364 days a year. If you only buy enough for average traffic, your site crashes on Black Friday. Autoscaling dynamically adds and removes resources exactly when needed.

## Real World Analogy
Think of a **Grocery Store Checkout**:
*   **Horizontal Pod Autoscaler (HPA):** The manager sees a long line forming, so they open 3 more checkout registers (adding more Pods).
*   **Vertical Pod Autoscaler (VPA):** A customer has a massive, heavy cart that one cashier can't handle. They swap in a stronger cashier (increasing CPU/RAM for an existing Pod).
*   **Cluster Autoscaler:** The store is completely packed, and every register is open. The manager calls the construction crew to instantly build an extension to the building (adding more physical servers/nodes).

## Core Concepts
*   **HPA (Horizontal Pod Autoscaler):** Scales the *number* of Pods in a Deployment up or down based on metrics like CPU utilization.
*   **Metrics Server:** A vital K8s component that collects resource usage data from all nodes/pods so the HPA knows when to trigger a scale.
*   **Scale to Zero:** Some advanced autoscalers (like KEDA) can scale your app down to 0 pods if there is no traffic, costing you exactly $0.

## Architecture / Flow
1. **Metrics Server** continuously monitors CPU usage.
2. The HPA is configured to keep average CPU at 50%.
3. A traffic spike hits. Average CPU jumps to 85%.
4. The HPA notices this and updates the Deployment from 2 replicas to 5 replicas.
5. Kubernetes spins up the 3 new Pods.
6. The traffic is now spread across 5 Pods, bringing the average CPU back down to 50%.

## Practical Commands
*   `kubectl autoscale deployment my-app --cpu-percent=50 --min=1 --max=10` - Creates an HPA instantly.
*   `kubectl get hpa` - See the current status, current replica count, and metric targets.
*   `kubectl describe hpa my-app` - View the exact math and events K8s used to decide to scale up or down.

## Hands-On Exercise
Deploy an Nginx pod and set its CPU `requests` to 100m. Create an HPA for it. Then, run a temporary `busybox` pod and use a loop to send continuous thousands of `wget` requests to Nginx. Watch `kubectl get hpa -w` to see the replicas automatically increase!

## Mini Project
**"Queue-Based Scaling"**
Look into KEDA (Kubernetes Event-driven Autoscaling). Instead of scaling based on CPU, configure an autoscaler that watches a RabbitMQ or SQS message queue. If the queue hits 1,000 pending messages, it should scale up the worker pods to process them faster.

## Real Production Usage
This is the ultimate promise of Cloud Computing: "Pay only for what you use." E-commerce sites scale up dramatically during the day and scale down to 1 or 2 pods at 3:00 AM when users are asleep, saving massive amounts of money.

## Common Mistakes
*   **Missing CPU Requests:** The HPA calculates scaling as a percentage. If you don't define a CPU `request` in your Deployment YAML, Kubernetes doesn't know what "100%" is, and the HPA will simply show `<unknown>` and refuse to work.
*   **Scaling Thrashing:** Setting thresholds too tightly so the cluster scales up, then immediately scales down, then scales up again in an infinite loop.

## Debugging Guide
*   **HPA says `<unknown>/50%`?** The Metrics Server is either not installed in your cluster, or the pod doesn't have resource requests defined.
*   **Pods scaling but staying in `Pending`?** Your HPA did its job, but your physical cluster ran out of space. You need a Cluster Autoscaler to add more physical Nodes.

## Best Practices
*   **Always set a sane `max` limit:** If your app has a bug that causes infinite CPU loops, or if you get hit by a DDOS attack, you do NOT want your HPA to scale up to 10,000 pods and give you a $50,000 cloud bill.
*   **Scale up fast, scale down slow:** You want to react instantly to a traffic spike, but you want to wait a few minutes before scaling down just in case the spike comes back.

## Interview Questions
*   **Q: What is the difference between Horizontal Scaling and Vertical Scaling?**
    *   *A: Horizontal adds MORE instances (from 2 servers to 5 servers). Vertical makes existing instances BIGGER (from 2GB RAM to 8GB RAM).*
*   **Q: Why might an HPA fail to scale a deployment even if CPU is at 100%?**
    *   *A: It might have reached its configured `max` replica limit, or the underlying nodes might be full (requiring Cluster Autoscaler).*

## Summary
Autoscaling turns Kubernetes from a static container host into a living, breathing, elastic platform that reacts to the real-time demands of your users while optimizing your cloud bill.

---
Prev: [04_networking.md](./04_networking.md) | Index: [Index](../00_index.md) | Next: [06_monitoring.md](./06_monitoring.md)
