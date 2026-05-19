# Statefulsets

## Why This Exists
Standard Kubernetes `Deployments` are designed for stateless applications (like web servers). In a Deployment, pods are completely interchangeable and easily killed. But what about a Database? If you kill a database pod and replace it with a blank one, you lose data. StatefulSets exist to manage pods that need a persistent identity, a specific startup order, and their own dedicated storage.

## Real World Analogy
Think of a standard Deployment like **Fast Food Workers**. If cashier #3 goes on break, cashier #4 steps in. They are completely interchangeable.
Think of a StatefulSet like a **Corporate Board of Directors**. You have the CEO, the CFO, and the CTO. They are NOT interchangeable. The CFO has a specific locked filing cabinet (Persistent Storage) and a specific title (Network Identity). If the CFO leaves, the new person hired MUST take over that exact filing cabinet and title.

## Core Concepts
*   **Sticky Identity:** Pods get predictable names (e.g., `mysql-0`, `mysql-1`) instead of random hashes (e.g., `mysql-7b9x2`).
*   **Ordered Deployment:** `mysql-0` must fully start and be healthy *before* Kubernetes will even attempt to start `mysql-1`.
*   **PersistentVolumeClaim Templates:** Every pod gets its own separate hard drive. `mysql-0` gets drive A, `mysql-1` gets drive B.

## Architecture / Flow
1. Developer creates a StatefulSet requesting 3 replicas of a database.
2. K8s provisions a Persistent Volume (Disk) and attaches it to Node.
3. K8s starts Pod `db-0` and mounts the disk.
4. K8s waits for `db-0` to report "Ready".
5. K8s provisions a second disk, then starts `db-1`, and mounts the second disk.

## Practical Commands
*   `kubectl get statefulsets` (or `sts`)
*   `kubectl scale sts my-db --replicas=5` - Scales up sequentially.
*   `kubectl delete sts my-db` - Deletes the pods, but *intentionally leaves the data disks behind* to prevent accidental data loss.

## Hands-On Exercise
Deploy a StatefulSet of Nginx where each pod writes its own hostname (e.g., `web-0`, `web-1`) to an `index.html` file on a persistent volume. Delete the pod `web-0`, watch it recreate, and verify it still serves the same `web-0` index page.

## Mini Project
**"Replicated Database"**
Deploy a primary-replica Redis cluster. Use a StatefulSet. Configure the startup script so that `redis-0` knows it is the Primary, and `redis-1` and `redis-2` automatically configure themselves to replicate data from `redis-0` based on its predictable DNS name.

## Real Production Usage
StatefulSets are the backbone of running stateful systems like Kafka, Elasticsearch, Cassandra, MongoDB, or PostgreSQL inside Kubernetes. 

## Common Mistakes
*   **Using a Deployment for a Database:** Using a standard deployment with a shared volume means all replicas try to write to the exact same database files simultaneously, causing massive data corruption.
*   **Assuming Deletion cleans up Disks:** Deleting a StatefulSet does NOT delete the PersistentVolumeClaims. You must manually delete the PVCs if you want to destroy the data and stop paying for the cloud storage.

## Debugging Guide
*   **Pod stuck in Pending?** Look at `kubectl describe pod my-db-0`. Usually, it's stuck because the cloud provider failed to provision the requested Persistent Volume, or the volume is in a different Availability Zone than the node.
*   **Stuck Terminating?** If a node crashes, a StatefulSet pod might get stuck in "Terminating". K8s won't spin up a replacement until it is 100% sure the old pod is dead, to prevent "split-brain" data corruption.

## Best Practices
*   **Headless Services:** Always pair a StatefulSet with a "Headless Service" (ClusterIP: None). This allows other apps to look up the exact IP address of a specific pod (like `mysql-1.my-service`) rather than load-balancing randomly.

## Interview Questions
*   **Q: Why would you use a StatefulSet instead of a Deployment?**
    *   *A: When my application requires stable network identifiers (predictable names), ordered startup/teardown, or dedicated persistent storage for each individual replica.*

## Summary
While Kubernetes was originally built for stateless web apps, StatefulSets make it possible to run heavy, data-rich applications with the reliability and strict ordering that databases require.

---
Prev: [01_helm.md](./01_helm.md) | Index: [Index](../00_index.md) | Next: [03_jobs_cronjobs.md](./03_jobs_cronjobs.md)
