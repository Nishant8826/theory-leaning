# Jobs Cronjobs

## Why This Exists
Not every piece of software is a web server that needs to run 24/7. Sometimes you need a script to run once, do some math or a database migration, and then shut down. A `Job` handles tasks that run to completion. A `CronJob` is a Job that runs on a specific time schedule.

## Real World Analogy
*   **Deployment:** A **Store Cashier**. They stand at the register all day waiting for customers. If they leave, you replace them.
*   **Job:** A **Plumber**. You call them, they fix the specific pipe, and as soon as it's fixed, they leave.
*   **CronJob:** A **Night Security Guard**. They arrive exactly at 2 AM every night, walk a specific patrol route, and go home at 3 AM.

## Core Concepts
*   **Run to Completion:** Unlike a Deployment which restarts a pod if it stops, a Job *wants* the pod to stop successfully (exit code 0).
*   **Parallel Executions:** A Job can be configured to spin up 5 pods at once to process a queue of work faster.
*   **Cron Syntax:** The scheduling mechanism (e.g., `* * * * *` for every minute) used by CronJobs.

## Architecture / Flow
1. Developer applies a CronJob manifest set to run at midnight.
2. At exactly 12:00 AM, the CronJob controller creates a **Job** object.
3. The Job object creates a **Pod**.
4. The Pod runs its script (e.g., backing up a database).
5. The script finishes successfully. The Pod's status changes to `Completed`. It stops consuming CPU/RAM.

## Practical Commands
*   `kubectl create job my-job --image=busybox -- echo "Hello"` - Quick way to test a job.
*   `kubectl get jobs`
*   `kubectl get cronjobs` (or `cj`)
*   `kubectl create job --from=cronjob/my-cronjob manual-run` - Instantly trigger a CronJob right now, ignoring the schedule.

## Hands-On Exercise
Write a Job YAML that spins up a container, sleeps for 10 seconds, prints "Work Done", and exits. Watch the pod status change from `Running` to `Completed` using `kubectl get pods -w`.

## Mini Project
**"The Daily Scraper"**
Create a CronJob that runs every 5 minutes. The container should run a simple Python script that makes an HTTP GET request to a public API (like a weather API), logs the result to the console, and exits. 

## Real Production Usage
*   **Database Migrations:** Running a Job to update database schemas before a new version of an app is deployed.
*   **Backups:** CronJobs that trigger a database dump and upload it to an S3 bucket every night at 3 AM.
*   **Batch Processing:** Generating weekly PDF reports for users.

## Common Mistakes
*   **Wrong Restart Policy:** Pods in a Job MUST have `restartPolicy: OnFailure` or `Never`. If you set it to `Always` (the default for deployments), K8s will endlessly restart your completed script.
*   **Messing up Cron Syntax:** Accidentally setting `* * * * *` (every minute) instead of `0 0 * * *` (every day at midnight) and destroying your database with backup requests.

## Debugging Guide
*   **Job failed?** Do a `kubectl get pods`, find the pod that has status `Error`, and run `kubectl logs <pod-name>` to see what the script choked on.
*   **Job hanging?** Set an `activeDeadlineSeconds` in your Job YAML. If the script gets stuck in an infinite loop, K8s will automatically kill it after the deadline.

## Best Practices
*   **Idempotency:** Make sure your scripts are safe to run twice. If a node crashes in the middle of a Job, Kubernetes might start the Job over again on a new node.
*   **Cleanup:** By default, completed Jobs and their Pods stay in the cluster so you can read their logs. Use `ttlSecondsAfterFinished` to have K8s automatically delete them after a few hours to keep your cluster clean.

## Interview Questions
*   **Q: What happens if the script inside a Job crashes (returns a non-zero exit code)?**
    *   *A: The Job controller will recognize the failure and start a new Pod to try again, up to a limit defined by the `backoffLimit` (default is 6 retries).*

## Summary
Jobs and CronJobs allow Kubernetes to be more than just a host for web servers; they turn the cluster into a powerful, distributed task-runner and batch-processing engine.

---
Prev: [02_statefulsets.md](./02_statefulsets.md) | Index: [Index](../00_index.md) | Next: [04_networking.md](./04_networking.md)
