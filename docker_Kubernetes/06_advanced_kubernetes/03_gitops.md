# Gitops

## Why This Exists
GitOps is the *philosophy* and set of practices that tools like ArgoCD implement. Historically, infrastructure changes were made via IT tickets, manual console clicks, or random bash scripts. GitOps dictates that Operations (infrastructure, deployments) must be managed exactly like Application Code: using Git, Pull Requests, and automated pipelines.

## Real World Analogy
Think of **Wikipedia vs Private Encyclopedias**. 
Before Wikipedia, encyclopedias were edited by a secret group of people behind closed doors (Manual Operations). 
With Wikipedia (GitOps), anyone can suggest an edit via a Pull Request. The history of every single change is recorded forever (Git History), the community reviews it (Code Review), and if a bad edit breaks a page, you can instantly hit "Undo" (Rollback).

## Core Concepts
*   **Declarative Infrastructure:** Everything must be written in code (YAML, Terraform). No clicking in UIs.
*   **Single Source of Truth:** If it's not in Git, it does not exist in the real world.
*   **Pull Requests for Operations:** The PR *is* the IT ticket.
*   **Automated Reconciliation:** A software agent continuously ensures the real world matches the Git repository.

## Architecture / Flow
1. Developer wants to add a new database.
2. Developer creates a Git branch and adds the `database.yaml` code.
3. Developer opens a Pull Request in GitHub.
4. Senior Engineers review the YAML and approve the PR.
5. The PR is merged into the `main` branch.
6. A software agent (like ArgoCD or Flux) notices the merge and automatically creates the database in the cluster.

## Practical Commands
*   *(GitOps isn't a tool, it's a workflow. The commands are standard Git commands).*
*   `git checkout -b fix-memory-leak`
*   `git commit -m "Increased pod memory limit to 2Gi"`
*   `git push origin fix-memory-leak`

## Hands-On Exercise
Simulate a GitOps failure. Manually delete a critical Deployment in your cluster using `kubectl delete`. If you have a GitOps tool running (like ArgoCD), watch how the cluster automatically recreates the Deployment within minutes because the Git repository says it *must* be there.

## Mini Project
**"The Automated PR Pipeline"**
Set up a GitOps pipeline that requires a successful CI test before a Pull Request can be merged. Write a GitHub Action that runs `kubeval` or `helm lint` on your YAML files. If the YAML has a syntax error, the PR gets blocked, preventing bad infrastructure from ever reaching the main branch.

## Real Production Usage
Enterprises use GitOps to achieve massive scale and pass compliance audits. When an auditor asks, "Who changed the firewall rules on October 12th?", you don't guess. You look at the Git commit history for the firewall code, see exactly who approved the Pull Request, and read their comments on *why* they changed it.

## Common Mistakes
*   **Committing Secrets to Git:** Because Git is the source of truth, people accidentally commit database passwords in plain text YAML. Hackers scan GitHub for this. You must use tools like `SealedSecrets` (which encrypts the secret in Git) or `ExternalSecrets` (which pulls from AWS Secrets Manager).

## Debugging Guide
*   **Deployment didn't happen?** Check the Git commit history on the `main` branch. If the commit wasn't successfully merged, the GitOps operator won't see it. The issue is in your Git workflow, not the cluster.

## Best Practices
*   **No SSH access:** Developers should never SSH into production servers or use `kubectl apply`. Remove their access. Force them to make changes via Git Pull Requests.
*   **Idempotency:** Your infrastructure code must be safe to run over and over again without causing errors.

## Interview Questions
*   **Q: What is the main difference between traditional CI/CD and GitOps?**
    *   *A: Traditional CI/CD uses a "Push" model, where the CI server (like Jenkins) reaches into the production cluster to push changes. GitOps uses a "Pull" model, where a highly secure agent sits inside the cluster and pulls changes from Git, preventing external tools from needing admin access to the cluster.*

## Summary
GitOps brings the best practices of software engineering (version control, peer review, transparent history) to infrastructure and operations, fundamentally changing how teams build and manage the cloud.

---
Prev: [02_argocd.md](./02_argocd.md) | Index: [Index](../00_index.md) | Next: [04_kafka_event_driven.md](./04_kafka_event_driven.md)
