# Kubernetes Deployments

## Why This Exists
In the previous topic, we learned that Pods are the smallest unit in Kubernetes. However, you should almost never create Pods directly. Why? Because Pods are mortal. If a Pod crashes or the node it is running on dies, that Pod is gone forever.

**Deployments** exist to solve this. A Deployment is a higher-level object that manages Pods. You tell a Deployment: "I want 3 replicas of my web app running at all times." The Deployment ensures that happens. If a Pod dies, it automatically creates a new one. It also handles seamless updates (Rolling Updates) when you release a new version of your app.

## Real World Analogy
Think of a Deployment as the **Manager of a Fast Food Shift**.
- The Pods are the workers on the line.
- If a worker gets sick and leaves (Pod crashes), the Manager (Deployment) immediately calls in a replacement worker to keep the line moving.
- If the company introduces a new uniform (New App Version), the Manager doesn't send everyone home at once. They have workers change one by one (Rolling Update) so the store never closes.

## Core Concepts
- **Deployment**: The object that manages the desired state of your application.
- **ReplicaSet**: A background object used by the Deployment to ensure the exact number of Pods are running.
- **Rolling Update**: Updating Pods a few at a time so there is zero downtime.
- **Rollback**: Reverting to a previous working version if the new version has bugs.

## Architecture / Flow

```text
[ Deployment ]
       │
       ▼ (Manages)
[ ReplicaSet ]
       │
       ▼ (Ensures replicas)
+------------------------------------------+
|  [ Pod 1 ]    [ Pod 2 ]    [ Pod 3 ]     |
+------------------------------------------+
```

## Practical Commands

```bash
# Create a deployment imperatively
kubectl create deployment my-web --image=nginx:alpine

# Scale the deployment to 5 replicas
kubectl scale deployment my-web --replicas=5

# View rollout status
kubectl rollout status deployment my-web

# Rollback to the previous version
kubectl rollout undo deployment my-web
```

## Hands-On Exercise
Let's create a Deployment declaratively.

1. Create a file named `deployment.yaml`:
   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: nginx-deployment
   spec:
     replicas: 3
     selector:
       matchLabels:
         app: nginx
     template:
       metadata:
         labels:
           app: nginx
       spec:
         containers:
         - name: nginx
           image: nginx:1.14.2
           ports:
           - containerPort: 80
   ```
2. Apply it:
   ```bash
   kubectl apply -f deployment.yaml
   ```
3. Check the status:
   ```bash
   kubectl get deployments
   kubectl get pods # You should see 3 pods
   ```

## Mini Project
**Task**: Perform a Zero-Downtime Rolling Update and a Rollback.

1. Open your `deployment.yaml` and change the image from `nginx:1.14.2` to `nginx:latest`.
2. Apply the change:
   ```bash
   kubectl apply -f deployment.yaml
   ```
3. Watch the rollout in real-time:
   ```bash
   kubectl get pods -w
   ```
   *You will see new pods being created and old pods being terminated one by one.*
4. Oh no! `latest` broke the app! Let's roll back:
   ```bash
   kubectl rollout undo deployment nginx-deployment
   ```
5. Kubernetes will revert the pods back to `nginx:1.14.2`.

## Real Production Usage
- **Deployment Strategy**: Kubernetes supports `RollingUpdate` (default) and `Recreate` (kills all old pods first, causes downtime but good for apps that can't run two versions at once like databases).
- **CI/CD Integration**: In real life, your GitHub Actions pipeline will update the image in the Deployment YAML and run `kubectl apply` to deploy new code.

## Common Mistakes
- **Forgetting Selectors**: The `matchLabels` in the `selector` must match the `labels` in the `template`. If they don't, the Deployment won't know which Pods to manage.
- **Using `:latest` tag**: If you use `:latest`, Kubernetes won't trigger a rolling update if the image changes because the tag name didn't change. Always use specific versions or commit SHAs.

## Debugging Guide
- **Deployment stuck**: Run `kubectl describe deployment <name>`. Check the `Events` section at the bottom. It usually reveals if there are issues pulling the image or if resources are insufficient.

## Best Practices
- **Use specific tags**: Never use `latest` in production.
- **Set resource requests and limits**: Tell Kubernetes how much CPU and RAM your app needs so it can schedule efficiently.

## Interview Questions
1. **What is the difference between a Pod and a Deployment?**
   *Answer*: A Pod represents a single instance of a running process. A Deployment manages Pods, handling scaling, self-healing, and zero-downtime updates.
2. **How do you achieve zero-downtime updates in Kubernetes?**
   *Answer*: By using a Deployment with the `RollingUpdate` strategy, which replaces old Pods with new ones incrementally.

## Summary
Deployments are the workhorse of Kubernetes. They give your application self-healing capabilities and allow you to scale up or update your application with zero downtime.

---
Prev: [01_pods.md](./01_pods.md) | Index: [Index](../00_index.md) | Next: [03_services.md](./03_services.md)
