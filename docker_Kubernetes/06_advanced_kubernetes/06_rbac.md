# Rbac

## Why This Exists
By default, if a developer has access to the cluster, they can accidentally delete the production database. RBAC (Role-Based Access Control) is the security framework that restricts what users, developers, and automated pipelines can do inside Kubernetes.

## Real World Analogy
Think of a **High-Security Laboratory**. 
*   **Subject (User/ServiceAccount):** The Scientist.
*   **Role:** The Security Badge level (e.g., "Level 2 Access - Allowed in Chemistry Lab, Denied from Vault").
*   **RoleBinding:** The action of the Security Office physically handing the Level 2 Badge to Bob the Scientist.

## Core Concepts
*   **Role:** Defines permissions (e.g., "Can read Pods") within one specific *Namespace*.
*   **ClusterRole:** Defines permissions globally across the *entire cluster*.
*   **RoleBinding:** Attaches a Role to a User, Group, or ServiceAccount.
*   **ServiceAccount:** An identity for pods/applications (not humans) to talk to the Kubernetes API.

## Architecture / Flow
1. You create a `ServiceAccount` for a CI/CD pipeline.
2. You create a `Role` with `rules: [apiGroups: "", resources: ["pods"], verbs: ["create", "update"]]`.
3. You create a `RoleBinding` connecting the `ServiceAccount` to the `Role`.
4. When the CI/CD pipeline tries to create a pod, the API server checks the RoleBinding and allows it. If it tries to delete a Secret, the API server denies it.

## Practical Commands
*   `kubectl create role pod-reader --verb=get --verb=list --resource=pods --namespace=dev`
*   `kubectl create rolebinding read-pods --role=pod-reader --user=alice --namespace=dev`
*   `kubectl auth can-i create deployments --as=alice` - Test what a user can do!

## Hands-On Exercise
Create a namespace called `staging`. Create a Role that only allows reading pods in `staging`. Bind it to a dummy ServiceAccount. Test the permissions using the `kubectl auth can-i` command to prove that the ServiceAccount can read pods, but cannot delete them.

## Mini Project
**"The Restricted Pipeline"**
Build a Kubernetes YAML file for a CI/CD ServiceAccount. Give it a Role that allows it to `apply` Deployments and Services in the `frontend` namespace, but explicitly exclude permissions to view or create `Secrets`.

## Real Production Usage
Security audits require strict RBAC. Developers typically have read-only access to production (to view logs and debug), while automated CI/CD pipelines have the write access to actually deploy the code.

## Common Mistakes
*   **God Mode for Everything:** Granting the `cluster-admin` (God mode) ClusterRole to Jenkins or GitHub Actions. If your Jenkins server gets hacked, the hacker instantly has total control to delete or mine Bitcoin on your entire Kubernetes cluster.

## Debugging Guide
*   **Pod crashing with `Forbidden` or `403` error?** This usually happens when an application inside a pod is trying to talk to the K8s API (like an ingress controller trying to read secrets). Ensure the pod has a `serviceAccountName` specified, and that account has the correct RoleBinding.

## Best Practices
*   **Principle of Least Privilege:** Do not use wildcards (`resources: ["*"]`). If an app only needs to read pods, specify exactly `["pods"]`. Deny everything by default.

## Interview Questions
*   **Q: What is the difference between a Role and a ClusterRole?**
    *   *A: A Role is scoped to a specific namespace (e.g., can only read pods in the `dev` namespace). A ClusterRole applies globally across all namespaces (e.g., can read pods in `dev`, `prod`, and `kube-system`), and is also required to grant access to cluster-scoped resources like Nodes.*

## Summary
RBAC is the invisible security fence inside Kubernetes. It prevents accidents, restricts the blast radius of hacked applications, and ensures strict governance over who controls your infrastructure.

---
Prev: [05_multi_cluster.md](./05_multi_cluster.md) | Index: [Index](../00_index.md) | Next: [07_disaster_recovery.md](./07_disaster_recovery.md)
