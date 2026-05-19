# Production Debugging

## Why This Exists
Even with perfect code and perfect CI/CD pipelines, things break in production. Networks partition, cloud disks fill up, and users submit corrupted data. Because Kubernetes abstracts so much away, you need a highly systematic approach to peel back the layers and find the root cause of failures in a complex, distributed environment.

## Real World Analogy
Think of a **Medical Diagnosis**. 
You don't just randomly perform surgery on a patient complaining of pain. You check their vital signs (Monitoring/Grafana), ask for their medical history (Logging/Kibana), perform specific localized tests (Networking/DNS checks), and only after systematically ruling out possibilities do you prescribe a treatment.

## Core Concepts
*   **Pod Statuses:** Understanding what `Pending`, `CrashLoopBackOff`, and `ImagePullBackOff` actually mean.
*   **K8s Events:** A temporary chronological log of everything the K8s control plane is doing (e.g., "Failed to attach volume", "Scaled up replica set").
*   **OOMKilled (Out of Memory):** The silent killer where Linux terminates a container because it exceeded its memory limit.

## Architecture / Flow
A systematic debugging flow:
1. **Symptom:** "The website is returning 502 Bad Gateway."
2. **Dashboards:** Check Grafana. Is CPU spiking? Is the database reachable?
3. **Cluster State:** `kubectl get pods`. Are any pods crashing?
4. **Inspect:** `kubectl describe pod <name>` to check for K8s events and volume errors.
5. **Logs:** `kubectl logs <name>` to check for application-level stack traces.
6. **Network:** Use a temporary busybox pod to `curl` the service internally.
7. **Fix:** Update the Deployment YAML and apply.

## Practical Commands
*   `kubectl describe pod <pod-name>` - The holy grail of debugging. Shows limits, volumes, and recent events.
*   `kubectl get events --sort-by='.metadata.creationTimestamp'` - See a timeline of recent cluster errors.
*   `kubectl exec -it <pod-name> -- /bin/sh` - SSH directly into a running container to check files or test network connectivity.
*   `kubectl get pod <name> -o yaml` - See the raw generated YAML to check if defaults were applied incorrectly.

## Hands-On Exercise
Deploy a pod but deliberately misspell the image name (e.g., `image: nginxxxx:latest`). Run `kubectl get pods` and see the `ErrImagePull` status. Run `kubectl describe pod` and look at the `Events` section at the very bottom to read the exact error message from the container runtime.

## Mini Project
**"Chaos Engineering"**
Write a bash script that does something terrible: deletes a random service, changes a random deployment's image to a broken one, or applies a NetworkPolicy that blocks all traffic. Have a friend run the script on your cluster. Practice using only `kubectl` to find and fix the issue they caused.

## Real Production Usage
In major tech companies, when a critical system goes down, an "Incident Commander" opens a War Room. SREs (Site Reliability Engineers) jump in, instantly pull up monitoring dashboards, search centralized logs, and use `kubectl exec` to rapidly diagnose the system while following strict "Runbooks" (pre-written troubleshooting guides).

## Common Mistakes
*   **Restarting Immediately:** If a pod is failing, junior developers often delete it hoping a fresh one fixes it. If you delete it, you lose the logs and the context of *why* it failed. Always investigate before restarting.
*   **Assuming it's a Code Issue:** Often, apps crash not because of bad code, but because of bad infrastructure (e.g., the K8s Node ran out of disk space, or a security group blocked a port).

## Debugging Guide
*   **`Pending` Status:** The Pod hasn't even started. Usually means your cluster doesn't have enough CPU/RAM to fit the pod, or it's waiting for a Persistent Volume to be created.
*   **`CrashLoopBackOff` Status:** The app starts, hits a fatal error, and crashes immediately. K8s tries restarting it on a loop. Run `kubectl logs <pod-name> -p` to see the error.
*   **Can't reach the Database?** Run `kubectl exec` into your web pod, install `ping` or `telnet`, and manually try to reach the database pod's IP to prove if it's a network routing issue or an app code issue.

## Best Practices
*   **Liveness & Readiness Probes:** Always configure these. They tell Kubernetes exactly how to test if your app is frozen or still booting up, allowing K8s to automatically restart frozen apps or pause traffic to apps that aren't ready.
*   **Write Runbooks:** For every alert you configure, write a document explaining exactly what commands to run to debug it at 3:00 AM.

## Interview Questions
*   **Q: Walk me through how you would debug an application that is randomly crashing every few hours.**
    *   *A: 1. Check `kubectl get events` for `OOMKilled` (memory leaks are common). 2. Check centralized logging for application stack traces right before the crash time. 3. Check Grafana for CPU/Memory spikes correlating with the crash times.*

## Summary
Production debugging is the ultimate test of your Kubernetes knowledge. It requires combining your understanding of containers, networking, storage, and application architecture into a systematic process of elimination.

---
Prev: [07_logging.md](./07_logging.md) | Index: [Index](../00_index.md) | Next: [Index](../00_index.md)
