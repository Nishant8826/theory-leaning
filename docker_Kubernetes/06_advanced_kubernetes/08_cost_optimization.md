# Cost Optimization

## Why This Exists
Kubernetes is incredibly powerful, but if left unconfigured, it is a money-burning machine. If you don't set limits, pods will consume massive amounts of CPU/RAM, forcing the cluster to automatically add more expensive EC2 servers. Cloud bills can spiral out of control overnight.

## Real World Analogy
Think of **Leaving the Lights On**. 
If you leave every light, TV, and AC unit on in your house while you go on vacation, your electric bill will be massive. 
Cost optimization is installing motion sensors that turn off lights when rooms are empty (Autoscaling) and swapping old bulbs for energy-efficient LEDs (Right-sizing pods).

## Core Concepts
*   **Requests & Limits:** Telling K8s exactly how much CPU/RAM a pod needs (Request) and the absolute maximum it is allowed to use (Limit).
*   **Cluster Autoscaler / Karpenter:** Automatically deletes empty servers (Nodes) to save money when traffic is low.
*   **Spot Instances:** Buying excess cloud compute capacity at a 70% discount, with the catch that the cloud provider can kill the server at any time.

## Architecture / Flow
1. Developer sets a pod Request to 1GB RAM.
2. At night, traffic drops. The Horizontal Pod Autoscaler scales the app from 10 pods down to 2 pods.
3. The Cluster Autoscaler notices that Node #3 is now completely empty.
4. The Cluster Autoscaler safely powers down Node #3.
5. You stop paying the hourly fee for that server.

## Practical Commands
*   `kubectl top pods` - See exactly how much CPU/RAM your apps are currently using.
*   `kubectl top nodes` - See how full your physical servers are.

## Hands-On Exercise
Deploy an Nginx pod without limits. Then deploy one with `resources: requests: memory: "64Mi"`. View the difference in how Kubernetes schedules them. Next, manually scale a deployment up to 50 replicas and watch `kubectl get nodes` to see if your cluster automatically adds new servers.

## Mini Project
**"The Weekend Shutdown"**
Install KEDA (Kubernetes Event-driven Autoscaling) or write a custom script. Configure it so that on Friday at 6:00 PM, all development namespaces are scaled down to exactly 0 replicas. On Monday at 8:00 AM, scale them back to 1. Watch your dev-environment AWS bill drop by 30%!

## Real Production Usage
Enterprise cost strategy relies heavily on **Spot Instances** for worker nodes. Because Kubernetes is designed to handle pods dying and restarting automatically, it is the perfect platform to run on cheap, unstable Spot Instances. If AWS reclaims the server, K8s just reschedules the pods onto a new one.

## Common Mistakes
*   **Requests == Limits:** Setting the Request and Limit to the exact same high number. This prevents Kubernetes from "overcommitting" resources, meaning you pay for RAM that is strictly reserved but not actually being used by the application.
*   **Zombie Clusters:** Spinning up a test EKS cluster, forgetting about it, and paying $70/month for the control plane plus EC2 costs for an empty cluster.

## Debugging Guide
*   **Pod stuck in `Pending`?** You probably asked for `requests: memory: "64Gi"` but no single node in your cluster is that large. K8s will refuse to schedule it because it can't find a server big enough to honor the guarantee.

## Best Practices
*   **Use Cost Visibility Tools:** Install tools like **Kubecost** or **Goldilocks**. They analyze your running pods over 30 days and provide recommendations: "You requested 4GB of RAM, but historically only use 500MB. Lower your requests to save $1,000/month."

## Interview Questions
*   **Q: What is the difference between a Resource Request and a Resource Limit?**
    *   *A: A Request is the minimum amount of compute K8s guarantees the pod will get, used for deciding which node to schedule it on. A Limit is the hard ceiling; if a pod exceeds its memory limit, the Linux kernel kills it (OOMKilled).*

## Summary
In the cloud, architectural efficiency is directly tied to financial efficiency. A well-architected Kubernetes cluster automatically shrinks its footprint—and its cost—when users are asleep.

---
Prev: [07_disaster_recovery.md](./07_disaster_recovery.md) | Index: [Index](../00_index.md) | Next: [09_large_scale_architecture.md](./09_large_scale_architecture.md)
