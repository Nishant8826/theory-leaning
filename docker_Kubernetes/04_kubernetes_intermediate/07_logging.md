# Logging

## Why This Exists
In Kubernetes, containers are ephemeral (temporary). If an app crashes, K8s deletes the dead pod and creates a new one. If you try to SSH in to read the error log file, the file is already gone! You need a system that constantly ships logs off the containers to a safe, searchable database before they are destroyed.

## Real World Analogy
Think of a **Court Stenographer**. 
Imagine 10 people talking at once in a chaotic courtroom (Microservices). If you don't write it down immediately, the words vanish into the air. The stenographer (Log Shipper) writes every single word down and stores it in a massive, searchable transcript archive (Log Database). Later, a lawyer can search the archive for "Objection" to find exactly what happened.

## Core Concepts
*   **Stdout / Stderr:** In K8s, apps shouldn't write to text files. They should print everything to standard output (console). K8s captures this automatically.
*   **Log Shipper (e.g., Fluentd, Promtail):** A tiny agent running on every physical server that grabs those console logs and forwards them to a database.
*   **Log Storage (e.g., Elasticsearch, Loki):** A database optimized for full-text search across billions of lines of text.
*   **Log Viewer (e.g., Kibana, Grafana):** The UI where developers type in search queries.

## Architecture / Flow
1. Node.js App runs `console.error("Database disconnected")`.
2. Kubernetes captures this and saves it to a temporary file on the physical Node.
3. **Fluentd** (running as a DaemonSet on that Node) reads the file.
4. Fluentd adds metadata (Pod Name, Namespace, Node IP) and ships it over the network to **Elasticsearch**.
5. A developer opens **Kibana**, searches for "Database disconnected", and finds the exact time and pod that caused the error.

## Practical Commands
*   `kubectl logs <pod-name>` - View recent logs for a specific pod.
*   `kubectl logs -f <pod-name>` - "Follow" the logs (streams them live to your terminal).
*   `kubectl logs -l app=my-web` - Grab the logs for *all* pods that have the label `app=my-web` combined together.
*   `kubectl logs <pod-name> -p` - View the logs of the *previous* crashed instance of this pod.

## Hands-On Exercise
Run a pod that loops and prints the current time and a random word every second. Use `kubectl logs -f` to watch it live. Delete the pod, then recreate it. Notice how the original logs are completely lost if you only rely on `kubectl logs`.

## Mini Project
**"Centralized Search"**
Use Helm to install the PLG stack (Promtail, Loki, Grafana) into a local cluster. Deploy a broken app that occasionally prints an error. Open Grafana, go to the "Explore" tab, and write a LogQL query to search the entire cluster for the word "error".

## Real Production Usage
When a user submits a support ticket at 2:04 PM saying "My payment failed", a developer opens Kibana and searches for `user_id: "12345"` between 2:00 PM and 2:05 PM. Centralized logging allows them to trace the user's journey across the API Gateway, the Orders Service, and the Payment Service to find exactly where it broke.

## Common Mistakes
*   **Logging Sensitive Data:** Accidentally printing passwords, API keys, or credit card numbers to `stdout`. Once it hits Elasticsearch, it's stored permanently and becomes a massive security/compliance violation.
*   **Multi-line Logs:** Java stack traces span 50 lines. If your log shipper isn't configured correctly, it will treat those 50 lines as 50 completely separate, disconnected logs, making them impossible to read in Kibana.

## Debugging Guide
*   **Logs aren't showing up in Kibana?** 
    1. Check if the app is actually printing to `stdout` (using `kubectl logs`).
    2. Check the logs of the Fluentd/Promtail DaemonSet pod on that specific node to see if it's failing to connect to the database.

## Best Practices
*   **Structured Logging (JSON):** Stop logging plain text like `User 54 logged in from 192.168.1.1`. Start logging JSON: `{"event": "login", "user": 54, "ip": "192.168.1.1"}`. JSON is infinitely easier for Elasticsearch to index, filter, and search.

## Interview Questions
*   **Q: What is the ELK or EFK stack?**
    *   *A: It stands for Elasticsearch (Database), Logstash/Fluentd (Shipper), and Kibana (UI). It is the industry standard suite for centralized logging.*
*   **Q: Why shouldn't a container write its logs to a local file like `/var/log/app.log`?**
    *   *A: Because containers are ephemeral. When the container dies, the file system is destroyed. Writing to `stdout` allows the container runtime to capture and forward the logs safely.*

## Summary
Centralized logging is your primary forensic tool. Without it, debugging a distributed microservice architecture is like trying to solve a crime where all the evidence burns up every 5 minutes.

---
Prev: [06_monitoring.md](./06_monitoring.md) | Index: [Index](../00_index.md) | Next: [08_production_debugging.md](./08_production_debugging.md)
