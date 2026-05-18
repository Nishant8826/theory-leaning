# Kubernetes Namespaces

## Why This Exists
Imagine you are a large company with 50 different developer teams all sharing a single Kubernetes cluster. If everyone creates Pods and Services in the same place, it will quickly become a mess. Names will conflict, and one team might accidentally delete another team's database!

**Namespaces** solve this by providing virtual partitions within a single physical cluster. They allow you to divide cluster resources between multiple users, teams, or projects.

## Real World Analogy
Think of a Namespace like **Folders on your computer** or **Apartments in a building**.
- Without folders, all your files (Work, Photos, Music) are dumped on the Desktop. It's a mess.
- With folders (Namespaces), you separate your files. A file named `resume.txt` can exist in both the `Work` folder and the `Personal` folder without conflict.

## Core Concepts
- **`default`**: The default namespace where your resources go if you don't specify one.
- **`kube-system`**: The namespace for objects created by the Kubernetes system itself (like DNS and dashboard).
- **Custom Namespace**: A namespace you create for your specific team or application (e.g., `frontend-team`, `staging`).
- **ResourceQuotas**: Limits on how much CPU, memory, or many Pods a namespace can use.

## Architecture / Flow

```text
[ Physical Kubernetes Cluster ]
       │
       ├─► [ Namespace: Default ] ──► [ App A Pods ]
       │
       ├─► [ Namespace: Finance ] ──► [ App B Pods ]
       │
       └─► [ Namespace: HR ] ───────► [ App C Pods ]
```

## Practical Commands

```bash
# List all namespaces
kubectl get namespaces

# Create a new namespace
kubectl create namespace my-team

# View pods in a specific namespace
kubectl get pods -n my-team

# Set your current default namespace so you don't have to type -n every time
kubectl config set-context --current --namespace=my-team
```

## Hands-On Exercise
Let's create a namespace and deploy a Pod inside it.

1. Create a namespace:
   ```bash
   kubectl create namespace development
   ```
2. Create a Pod in that namespace (`pod.yaml`):
   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     name: dev-pod
     namespace: development  # Specify the namespace here!
   spec:
     containers:
     - name: nginx
       image: nginx:alpine
   ```
3. Apply and check:
   ```bash
   kubectl apply -f pod.yaml
   kubectl get pods -n development
   ```

## Mini Project
**Task**: Set up a Resource Quota to limit a namespace's memory.

1. Create a file `quota.yaml`:
   ```yaml
   apiVersion: v1
   kind: ResourceQuota
   metadata:
     name: memory-limit
     namespace: development
   spec:
     hard:
       requests.memory: 1Gi
       limits.memory: 2Gi
   ```
2. Apply it: `kubectl apply -f quota.yaml`.
3. Now, the `development` team cannot use more than 2GB of RAM in total!

## Real Production Usage
- **Environment Separation**: Many companies use namespaces to separate `dev`, `qa`, and `prod` environments within the same cluster to save money on cloud costs.
- **Soft Multi-tenancy**: Allowing different client applications to run in the same cluster securely.

## Common Mistakes
- **Forgetting the `-n` flag**: Running `kubectl get pods` and thinking your app is gone, when it is just running in a different namespace.
- **Assuming full security**: Namespaces provide logical isolation, not physical or network isolation. Pods in different namespaces can still talk to each other by default unless you use **NetworkPolicies**.

## Debugging Guide
- **"Resource not found"**: Always check if you are looking in the correct namespace using `kubectl get <resource> -n <namespace>`.

## Best Practices
- **Use Namespaces for Teams**: Assign a namespace to each team or large application stack.
- **Apply Quotas**: Always apply ResourceQuotas to prevent one team's runaway application from crashing the whole cluster.

## Interview Questions
1. **What is a Namespace in Kubernetes?**
   *Answer*: It is a virtual partition in a cluster that allows you to isolate resources, prevent naming conflicts, and apply resource limits for different teams or projects.
2. **How do you view Pods in all namespaces at once?**
   *Answer*: Using the command `kubectl get pods -A` or `kubectl get pods --all-namespaces`.

## Summary
Namespaces are the key to organizing large clusters. They keep your resources tidy, prevent conflicts, and allow you to control resource usage across teams.

---
Prev: [08_health_checks.md](./08_health_checks.md) | Index: [Index](../00_index.md) | Next: [10_minikube.md](./10_minikube.md)
