# Kubernetes Volumes & Persistent Storage

## Why This Exists
By default, containers are **ephemeral** (temporary). If a container crashes, Kubernetes restarts it, but all files created or modified inside the container are lost. If you are running a database like MySQL, this means your data is gone!

**Volumes** solve this problem by providing a way to store data outside the container's lifecycle. Kubernetes supports many types of volumes, from temporary local directories to cloud-based block storage (like AWS EBS or Google Persistent Disk).

## Real World Analogy
Think of a Volume like an **External Hard Drive (USB Flash Drive)**.
- Your laptop (Container) might break down, get lost, or be replaced.
- But if you save your important files on an external hard drive (Volume), you can just plug it into a new laptop and continue your work without losing anything.

## Core Concepts
Kubernetes uses a 3-part system for production storage:
1.  **PersistentVolume (PV)**: The actual piece of storage (disk) provisioned by the cluster administrator or automatically by a cloud provider.
2.  **PersistentVolumeClaim (PVC)**: A request for storage by a user. It is like a "ticket" that says "I need 5GB of storage with ReadWrite access."
3.  **StorageClass**: Defines the "type" of storage (e.g., slow HDD vs fast SSD). It allows Kubernetes to automatically create a PV when a PVC is requested.

## Architecture / Flow

```text
[ Cloud / Disk ] (AWS EBS / Local Disk)
       │
[ PersistentVolume (PV) ] (The actual 10GB disk)
       ▲
       │ (Binds to)
       │
[ PersistentVolumeClaim (PVC) ] (App's request: "I need 10GB")
       ▲
       │ (Mounts)
       │
[ Pod / Container ] (/var/lib/mysql)
```

## Practical Commands

```bash
# List all Persistent Volumes
kubectl get pv

# List all Claims (PVCs)
kubectl get pvc

# Check why a PVC is pending
kubectl describe pvc <pvc-name>
```

## Hands-On Exercise
Let's create a PersistentVolumeClaim and mount it in a Pod.

1. Create a PVC (`pvc.yaml`):
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
2. Apply it:
   ```bash
   kubectl apply -f pvc.yaml
   ```
3. Mount it in a Pod (`pod.yaml`):
   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     name: storage-pod
   spec:
     containers:
     - name: my-container
       image: alpine
       command: ["sh", "-c", "echo 'Hello from PVC' > /data/message.txt && sleep 3600"]
       volumeMounts:
       - name: my-storage
         mountPath: /data
     volumes:
     - name: my-storage
       persistentVolumeClaim:
         claimName: my-pvc
   ```

## Mini Project
**Task**: Set up a persistent MySQL database.

1. Create a PVC requesting 5GB.
2. Run a MySQL Deployment and mount the PVC at `/var/lib/mysql` (where MySQL stores its data).
3. Delete the Pod and watch Kubernetes create a new one. Verify that the data is still there!

## Real Production Usage
- **Dynamic Provisioning**: In the cloud (AWS, GCP, Azure), you rarely create PVs manually. You just create a PVC, and the cloud provider automatically creates an EBS volume or Persistent Disk and attaches it to your node.

## Common Mistakes
- **`emptyDir` for real data**: Using `emptyDir` as a volume. This volume is created when a Pod is assigned to a node, and is deleted when the Pod is removed. It is only for temporary cache data.
- **Wrong Access Mode**: Using `ReadWriteMany` on storage that only supports `ReadWriteOnce` (like standard AWS EBS).

## Debugging Guide
- **PVC is stuck in `Pending`**:
  - Run `kubectl describe pvc <name>`.
  - Common reason: No PV is available that matches the requested size, or the cloud provider failed to provision the disk.

## Best Practices
- **Always use PVCs**: Do not hardcode specific node paths (hostPath) unless necessary. PVCs make your app portable across different clusters.

## Interview Questions
1. **What is the difference between a PV and a PVC?**
   *Answer*: A PV is the actual storage resource (like a hard drive) created by the admin or cloud. A PVC is a request for storage by a developer. You can think of a PV as a "House" and a PVC as "Renting a House".
2. **What happens to data when a Pod is deleted if it uses a PVC?**
   *Answer*: The data survives. The PVC remains bound to the PV, and when a new Pod is created with the same PVC, it can access the data again.

## Summary
Volumes are critical for stateful applications like databases. By using PVs and PVCs, Kubernetes ensures that your data is safe even when containers are destroyed and recreated.

---
Prev: [06_secrets.md](./06_secrets.md) | Index: [Index](../00_index.md) | Next: [08_health_checks.md](./08_health_checks.md)
