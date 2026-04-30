# 📌 Topic: GitOps Principles (ArgoCD / Flux)

## 🧠 Concept Explanation (Basic → Expert)
**Basic**: GitOps is a way to manage your infrastructure where Git is the "single source of truth." If you want to change your deployment (e.g., scale to 5 replicas), you don't run a command; you update a YAML file in Git. A "Sync" tool sees the change and updates the cluster automatically.
**Expert**: GitOps is the implementation of **Declarative Continuous Delivery**. It uses a **Pull-based Model** rather than a push-based one. Tools like **ArgoCD** or **Flux** run inside your cluster and constantly "watch" a Git repository. When the Git state differs from the Cluster state, the tool **Reconciles** them. Staff-level engineering requires mastering **Automated Drift Detection**, **Rollback via Git Revert**, and **Multi-environment Management** using tools like Kustomize or Helm.

## 🏗️ Mental Model
- **Traditional CD (Push)**: You are a delivery driver. You take the package (Image) and drive it to the house (Cluster). If the house is locked or you get lost, the delivery fails.
- **GitOps (Pull)**: The house (Cluster) has a smart robot (ArgoCD) that watches your shop's website (Git). When the robot sees a new product, it goes and gets it itself. The house is always in sync with the shop.

## ⚡ Actual Behavior
- **No Direct Access**: Developers don't need `kubectl` or `docker` access to the production servers. They only need access to Git. This is a massive security win.
- **Drift Correction**: If someone manually changes a container setting using the CLI, GitOps will detect the change and "Overwrite" it with the correct setting from Git within minutes.

## 🔬 Internal Mechanics (The Reconciler)
1. **The Watcher**: Pulls the Git repo every 30-60 seconds.
2. **The Diff**: Compares the YAML in Git with the live objects in the cluster API.
3. **The Synchronization**: Issues `apply` commands to the cluster to match the Git state.
4. **The Health Check**: Monitors the objects to ensure they are "Healthy" and "Synced."

## 🔁 Execution Flow (Deploying an Update)
1. Developer pushes code. CI builds image `v2` and pushes to registry.
2. **CI Pipeline**: Automatically updates the `deployment.yaml` in the "Config Repo" to use `v2`.
3. **ArgoCD**: Detects the change in the Config Repo.
4. **ArgoCD**: Pulls the new YAML and applies it to the cluster.
5. **Cluster**: Pulls image `v2` and performs a rolling update.

## 🧠 Resource Behavior
- **CPU/Network**: GitOps controllers use a small amount of resources to constantly poll Git and the Cluster API.
- **Security**: Reduces the attack surface by eliminating the need for long-lived "Admin" tokens in your CI/CD system (Jenkins).

## 📐 ASCII Diagrams (REQUIRED)

```text
       GITOPS WORKFLOW (PULL MODEL)
       
[ App Code ] -> [ CI Build ] -> [ Image Registry ]
                                       |
[ Git Config Repo ] <---( Update Tag )-+
      |
      +----( Watch )-----+
                         v
                  [ ArgoCD Controller ]
                         |
                  ( Reconcile / Apply )
                         v
                  [ Production Cluster ]
```

## 🔍 Code (ArgoCD Application Definition)
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app-prod
spec:
  project: default
  source:
    repoURL: 'https://github.com/myorg/gitops-config'
    targetRevision: HEAD
    path: overlays/production
  destination:
    server: 'https://kubernetes.default.svc'
    namespace: my-app
  syncPolicy:
    automated:
      prune: true      # Delete resources not in Git
      selfHeal: true   # Correct manual changes automatically
```

## 💥 Production Failures
- **The "Sync Loop"**: You have a resource that changes itself (like a Horizontal Pod Autoscaler). ArgoCD sees the change, thinks it's "Drift," and reverts it. The HPA changes it back. This goes on forever.
  *Fix*: Use `ignoreDifferences` in the ArgoCD config.
- **Git Repo Outage**: If GitHub is down, you cannot deploy or fix your infrastructure, even in an emergency.
  *Fix*: Have a manual "Break Glass" procedure to bypass GitOps if necessary.

## 🧪 Real-time Q&A
**Q: Can I use GitOps with Docker Compose?**
**A**: Not natively. GitOps is primarily a Kubernetes/Swarm concept because it requires an "Internal Controller" to watch and reconcile. However, you can simulate it with a script that runs `git pull && docker compose up -d` on a cron job (this is essentially "Poor Man's GitOps").

## ⚠️ Edge Cases
- **Secret Management**: You can't put plaintext secrets in Git. 
  *Fix*: Use **Sealed Secrets** (encrypted in Git, decrypted in cluster) or an **External Secrets Operator** that pulls from HashiCorp Vault.

## 🏢 Best Practices
- **Separate Repos**: Keep your "App Code" (Java/Node) in one repo and your "Infrastructure Config" (YAML/Terraform) in another.
- **No Manual Changes**: Lock down cluster access so only the GitOps controller can make changes.
- **Prune Resources**: Enable "Prune" so that deleting a file in Git also deletes the resource in the cluster.

## ⚖️ Trade-offs
| Feature | Traditional CD (Push) | GitOps (Pull) |
| :--- | :--- | :--- |
| **Security** | Low (Credentials in CI)| **High (Internal)** |
| **Audit Trail** | Medium (Logs) | **Highest (Git History)**|
| **Setup Effort** | **Low** | High |
| **Drift Detection**| None | **Automatic** |

## 💼 Interview Q&A
**Q: What is "Configuration Drift" and how does GitOps solve it?**
**A**: Configuration Drift occurs when the state of the production environment deviates from the documented or desired state—usually due to manual, emergency "hotfixes" made by engineers using the CLI. GitOps solves this by having a **Reconciliation Loop**. The GitOps controller constantly compares the live cluster state against the "Desired State" in Git. If it finds a discrepancy (the "Drift"), it automatically overwrites the manual changes with the state defined in Git, ensuring the environment remains consistent, predictable, and fully auditable.

## 🧩 Practice Problems
1. Set up a simple "Local GitOps" script that pulls a repo and runs `docker compose up`.
2. Research the difference between **ArgoCD** (Push/Pull hybrid with UI) and **Flux** (Pure GitOps).
3. Try to "break" a GitOps deployment by manually deleting a container and watch it come back to life.

---
Prev: [04_Infrastructure_as_Code_Terraform.md](./04_Infrastructure_as_Code_Terraform.md) | Index: [00_Index.md](../00_Index.md) | Next: [01_Horizontal_Scaling.md](../Scaling/01_Horizontal_Scaling.md)
---
