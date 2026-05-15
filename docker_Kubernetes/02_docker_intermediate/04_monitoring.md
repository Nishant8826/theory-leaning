# Docker Monitoring

## Why This Exists
Running containers is great, but how do you know if they are healthy? Is your Node.js container using 100% CPU? Is your database container running out of memory? 

Without monitoring, you are flying blind. Monitoring allows you to track resource usage (CPU, Memory, Network, Disk I/O) in real-time, set up alerts, and understand when it's time to scale up or fix a memory leak.

## Real World Analogy
Think of container monitoring like the **Dashboard in a Car**.
- It tells you your speed (Network I/O), fuel level (Memory), and engine temperature (CPU).
- If the check engine light comes on (Alert), you know something is wrong before the car breaks down on the highway.

## Core Concepts
- **Metrics**: Data points collected over time (e.g., "Memory usage is 400MB").
- **`docker stats`**: The built-in, terminal-based monitoring tool.
- **cAdvisor**: A tool by Google that analyzes and exposes resource usage from running containers.
- **Prometheus**: A time-series database used to collect and store metrics.
- **Grafana**: A visualization tool used to create beautiful dashboards from metrics.

## Architecture / Flow

```text
[ Docker Containers ]
       │
       ▼ (Metrics exposed by)
[ cAdvisor ]
       │
       ▼ (Scraped by)
[ Prometheus ]
       │
       ▼ (Visualized by)
[ Grafana Dashboard ]
```

## Practical Commands

```bash
# View live resource usage for all running containers
docker stats

# View stats for a specific container
docker stats my-app

# View stats without a live stream (snapshot)
docker stats --no-stream
```

## Hands-On Exercise
Let's see how `docker stats` works.

1. Run a heavy process to see resource usage spike:
   ```bash
   docker run -d --name stressed-container alpine md5sum /dev/urandom
   ```
2. Run `docker stats` and observe the CPU usage for `stressed-container`. It should be near 100%.
3. Stop and remove the container:
   ```bash
   docker rm -f stressed-container
   ```

## Mini Project
**Task**: Set up a basic monitoring stack with Prometheus and Grafana.

1. Create a `docker-compose.yml`:
   ```yaml
   version: '3.8'
   services:
     app:
       image: nginx:alpine

     cadvisor:
       image: gcr.io/cadvisor/cadvisor:latest
       ports:
         - "8080:8080"
       volumes:
         - /:/rootfs:ro
         - /var/run:/var/run:ro
         - /sys:/sys:ro
         - /var/lib/docker/:/var/lib/docker:ro

     prometheus:
       image: prom/prometheus
       ports:
         - "9090:9090"

     grafana:
       image: grafana/grafana
       ports:
         - "3000:3000"
   ```
2. This setup allows cAdvisor to read Docker stats, Prometheus to collect them, and Grafana to display them on a web interface.

## Real Production Usage
In production, running your own monitoring stack can be complex. Many companies use managed solutions:
- **Datadog / New Relic**: Paid, full-featured monitoring platforms.
- **Managed Prometheus (AWS AMP)**: Scalable Prometheus managed by AWS.
Monitoring is usually tied to an **Alerting** system (like PagerDuty or Slack) to notify on-call engineers when a container fails.

## Common Mistakes
- **Not setting resource limits**: By default, a container can use all the RAM and CPU of the host machine. If one container has a memory leak, it can crash the entire server.
- **Ignoring OOMKilled**: Out of Memory (OOM) kills containers silently. If a container keeps restarting, check if it's hitting memory limits.

## Debugging Guide
- **Container keeps restarting**: Run `docker inspect <container_name>` and look for the `OOMKilled` field. If it's `true`, you need to allocate more memory to the container or fix a leak.

## Best Practices
- **Set resource limits**: Always specify CPU and Memory limits in your Docker Compose or run commands.
  ```yaml
  deploy:
    resources:
      limits:
        cpus: '0.50'
        memory: 512M
  ```

## Interview Questions
1. **What is `docker stats` used for?**
   *Answer*: It provides a live stream of resource usage statistics for running containers, including CPU, memory, network, and block I/O.
2. **What happens to a container when it exceeds its memory limit?**
   *Answer*: The Linux kernel will terminate the process with an Out of Memory (OOM) error, and the container will exit with code 137.

## Summary
Monitoring turns you from a reactive developer into a proactive one. By using tools like `docker stats` or the Prometheus/Grafana stack, you can ensure your containers are performant and reliable.

---
Prev: [03_logging.md](./03_logging.md) | Index: [Index](../00_index.md) | Next: [05_scaling_containers.md](./05_scaling_containers.md)
