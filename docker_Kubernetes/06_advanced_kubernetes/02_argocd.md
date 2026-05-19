# Argocd

## Why This Exists
Applying Kubernetes YAMLs manually via `kubectl apply` from your laptop is dangerous and untraceable. If someone manually edits the cluster, the cluster "drifts" from the code saved in Git. ArgoCD solves this by continuously synchronizing your Git repository directly into your Kubernetes cluster.

## Real World Analogy
Think of a **Strict Art Curator**. 
The Git Repository is the **Official Blueprint Catalog**. The Kubernetes Cluster is the **Art Gallery**. 
ArgoCD is the Curator standing in the gallery holding the catalog. If a rogue employee tries to move a painting (manually change a pod), the Curator instantly notices the gallery no longer matches the blueprint, and forcefully moves the painting back. The gallery always perfectly matches the blueprint.

## Core Concepts
*   **Declarative Setup:** Everything about the app must be defined in files (YAML/Helm).
*   **Continuous Sync:** ArgoCD polls Git constantly to see if the files changed.
*   **Desired State vs Live State:** Git is the Desired state. The cluster is the Live state.
*   **Configuration Drift:** When a human manually alters the Live state so it no longer matches the Desired state.

## Architecture / Flow
1. Developer changes `replicas: 2` to `replicas: 5` and pushes the YAML to GitHub.
2. ArgoCD (running inside the cluster) polls GitHub and notices the commit.
3. ArgoCD compares Git (Desired) to the Cluster (Live) and marks the app as "OutOfSync".
4. ArgoCD automatically applies the new YAML to the cluster.
5. The cluster scales up to 5 replicas. The app is now "Synced".

## Practical Commands
*   *(ArgoCD is heavily UI-driven, but has a CLI)*
*   `argocd app create myapp --repo https://github.com/my/repo.git --path ./k8s --dest-server https://kubernetes.default.svc --dest-namespace default`
*   `argocd app sync myapp` - Force an immediate synchronization.

## Hands-On Exercise
Install ArgoCD on Minikube or a local cluster. Fork a public Git repository containing a simple Kubernetes Deployment. In the ArgoCD UI, create a new app pointing to your forked repo. Change the image tag in GitHub, commit it, and watch the ArgoCD UI magically update your cluster a few minutes later.

## Mini Project
**"The App of Apps"**
Create a master ArgoCD Application that points to a folder in Git. Inside that folder, put YAML files that define *other* ArgoCD Applications (like Prometheus, Nginx, and your web app). By syncing this one master app, ArgoCD will bootstrap your entire cluster from scratch!

## Real Production Usage
This is the gold standard for modern Kubernetes deployments. In secure enterprises, no human is ever given `kubectl` write access to Production. All changes *must* go through a GitHub Pull Request. When the PR merges, ArgoCD deploys it.

## Common Mistakes
*   **Manual Hotfixes:** Making a quick fix directly in the cluster using `kubectl edit deployment`. ArgoCD's self-healing feature will instantly detect this "drift" and overwrite your quick fix with whatever is currently in Git!
*   **Mixing Code and Config:** Putting your Node.js application code and your K8s YAML files in the exact same Git repository. Every time you commit code, ArgoCD unnecessarily re-checks the cluster.

## Debugging Guide
*   **App shows "OutOfSync" in the UI?** Click on the application and look at the "Diff" view. It will show a side-by-side comparison highlighting exactly which YAML lines in the cluster differ from your Git repository.

## Best Practices
*   **Two Repositories:** Separate your Application Code (e.g., Python/Java) from your Infrastructure Config (K8s YAMLs) into two different Git repositories. ArgoCD should only watch the config repo.

## Interview Questions
*   **Q: How does ArgoCD handle Configuration Drift?**
    *   *A: It continuously monitors the live cluster state. If it detects manual changes, it marks the application as "OutOfSync" and can be configured with "Automated Self-Healing" to instantly revert the cluster back to the state defined in Git.*

## Summary
ArgoCD enforces the reality that Git is the absolute single source of truth for your infrastructure, eliminating manual deployments and making disaster recovery as simple as creating a new cluster and pointing ArgoCD at your repo.

---
Prev: [01_istio.md](./01_istio.md) | Index: [Index](../00_index.md) | Next: [03_gitops.md](./03_gitops.md)
