# Disaster Recovery

## Why This Exists
Servers catch on fire. Ransomware encrypts hard drives. A tired engineer accidentally runs `kubectl delete namespace prod`. Disaster Recovery (DR) is your premeditated plan and toolset to restore the entire cluster and its data when the worst-case scenario happens.

## Real World Analogy
Think of a **Fire Evacuation Plan and an Offsite Safe**. 
You don't wait for the office building to catch fire to figure out where the exits are. And you don't keep your only copy of your passport inside the building. 
DR is practicing the fire drill (testing the restore process) and keeping your crucial backups in an offsite safe (Cloud Storage) so you can rebuild your life if the building burns down.

## Core Concepts
*   **RTO (Recovery Time Objective):** How fast must we be back online? (e.g., 1 hour).
*   **RPO (Recovery Point Objective):** How much data are we allowed to lose? (e.g., 15 minutes).
*   **Velero:** The industry-standard open-source tool for backing up and restoring K8s clusters.
*   **etcd Backups:** Taking a raw snapshot of the Kubernetes Master database.

## Architecture / Flow
1. **Backup:** Velero agent runs inside K8s -> Takes a snapshot of all K8s YAMLs and Physical Hard Drives (Persistent Volumes) -> Uploads them to an external AWS S3 bucket.
2. **Disaster:** The cluster is completely deleted by a hacker.
3. **Restore:** Spin up a brand new empty cluster -> Install Velero -> Point Velero to the S3 bucket -> Run `velero restore` -> All deployments and data magically reappear.

## Practical Commands
*   `velero backup create prod-backup --include-namespaces prod`
*   `velero restore create --from-backup prod-backup`
*   `ETCDCTL_API=3 etcdctl snapshot save snapshot.db` (For raw control plane backups).

## Hands-On Exercise
Install Velero locally (you can use Minio to act as a fake S3 bucket). Deploy a simple Nginx pod. Take a backup using Velero CLI. Delete the Nginx pod manually. Run a Velero restore command and watch the pod magically reappear.

## Mini Project
**"The Automated etcd Backup"**
Write a Kubernetes `CronJob` YAML. Every 12 hours, this job spins up a container, connects to the Kubernetes API, runs the `etcdctl snapshot save` command, and securely uploads the resulting database file to an AWS S3 bucket.

## Real Production Usage
High-performing SRE teams run automated "Game Days". They intentionally delete a staging cluster and time exactly how long it takes their automated DR scripts to rebuild it from GitOps repos and Velero volume backups, ensuring they meet their RTO SLA.

## Common Mistakes
*   **The Untested Backup:** Backing up data every day but never testing the restore process. A backup is absolutely useless if you find out during a crisis at 3 AM that the restore script has been broken for 6 months.

## Debugging Guide
*   **Volume restore failed on a new cluster?** Ensure the new cluster is in the exact same cloud availability zone as the old one. AWS cannot magically attach a hard drive stored in `us-east-1a` to a server running in `us-east-1b`.

## Best Practices
*   **Decouple State:** The best disaster recovery is a completely stateless cluster. Keep databases *outside* of Kubernetes (e.g., use AWS RDS). If your cluster is 100% stateless, Disaster Recovery is simply running Terraform to get a new cluster and letting ArgoCD deploy the apps.

## Interview Questions
*   **Q: Define RTO and RPO.**
    *   *A: RTO (Recovery Time Objective) is the maximum acceptable downtime (e.g., we must be back online in 2 hours). RPO (Recovery Point Objective) is the maximum acceptable data loss (e.g., we back up every 15 mins, so the worst-case is losing 15 mins of customer data).*

## Summary
Disaster Recovery in Kubernetes shifts operations from "trying to fix broken servers" to "completely destroying and recreating environments" from secure offsite backups.

---
Prev: [06_rbac.md](./06_rbac.md) | Index: [Index](../00_index.md) | Next: [08_cost_optimization.md](./08_cost_optimization.md)
