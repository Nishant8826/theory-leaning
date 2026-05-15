# Docker Logging

## Why This Exists
When running applications in traditional servers, you usually write logs to a file (like `/var/log/app.log`). However, in Docker, containers are ephemeral. If a container crashes and is deleted, all the log files inside it are lost forever.

Docker solves this by capturing everything your application prints to `stdout` (standard output) and `stderr` (standard error). It then passes these logs to a **Logging Driver**. Understanding how to view, manage, and rotate these logs is crucial for debugging and preventing your server's hard drive from filling up.

## Real World Analogy
Think of Docker logs like **Security Camera Footage** for a building.
- If the camera stores footage on a hard drive *inside* the building, and the building burns down (container crashes), the footage is lost.
- Docker acts like a system that automatically streams the footage to a secure off-site server (Logging Driver), so you can see what happened even after the building is gone.

## Core Concepts
- **`stdout` / `stderr`**: Standard output and standard error. The rule in Docker is: **Applications should log directly to the console, not to files.**
- **Logging Drivers**: Plugins that handle where logs go (e.g., `json-file`, `syslog`, `fluentd`, `awslogs`).
- **Log Rotation**: The practice of limiting log file sizes and deleting old logs to save disk space.

## Architecture / Flow

```text
[ Application ]
       │
       ▼ (Console.log / Print)
[ stdout / stderr ]
       │
       ▼ (Captured by)
[ Docker Daemon ]
       │
       ▼ (Sent to)
[ Logging Driver ] (Default: json-file)
       │
       ▼
[ Local Disk / Cloud Storage ]
```

## Practical Commands

```bash
# View logs of a running container
docker logs my-app

# Follow logs in real-time (like tail -f)
docker logs -f my-app

# View only the last 100 lines
docker logs --tail 100 my-app

# View logs since a specific time
docker logs --since 10m my-app
```

## Hands-On Exercise
By default, Docker keeps logs forever. Let's run a container with **Log Rotation** configured so it doesn't eat up all disk space.

1. Run a container with log limits:
   ```bash
   docker run -d --name limited-logger \
     --log-driver json-file \
     --log-opt max-size=10m \
     --log-opt max-file=3 \
     alpine sh -c "while true; do echo 'Logging data...'; sleep 1; done"
   ```
2. This ensures the log file will never exceed 10MB, and Docker will only keep a maximum of 3 log files (older ones get deleted).

## Mini Project
**Task**: Configure log rotation globally in Docker Compose.

1. Create a `docker-compose.yml`:
   ```yaml
   version: '3.8'
   services:
     web:
       image: nginx:alpine
       ports:
         - "80:80"
       logging:
         driver: "json-file"
         options:
           max-size: "200k"
           max-file: "10"
   ```
2. Run `docker compose up -d`. If you generate traffic to this Nginx server, the logs will automatically rotate once the file reaches 200KB.

## Real Production Usage
In production, reading logs with `docker logs` on individual servers doesn't scale. Companies use **Centralized Logging**:
- **ELK Stack**: Elasticsearch (Store), Logstash (Process), Kibana (Visualize).
- **Grafana Loki**: A lightweight log aggregation system.
- **CloudWatch / Stackdriver**: Native logging solutions for AWS and GCP.
You configure Docker's logging driver to ship logs directly to these services.

## Common Mistakes
- **Not setting log limits**: Leaving the default settings can result in a single container generating gigabytes of logs, filling up the host OS disk, and crashing the entire server.
- **Logging to files inside containers**: If your app writes to `/app/logs/output.log` inside the container, `docker logs` will show nothing, and the container will grow in size.

## Debugging Guide
- **Where are logs stored physically?**
  On Linux, by default, they are at: `/var/lib/docker/containers/<container-id>/<container-id>-json.log`. You need root access to view them.
- **`docker logs` is slow**: If a container has been running for months without rotation, reading logs can take minutes. Use `--tail` or `--since` to speed it up.

## Best Practices
- **Log in JSON format**: If your application logs in JSON, centralized log analyzers can easily parse and search through the data.
- **Always use log rotation**: Set default log rotation in `/etc/docker/daemon.json` so all containers use it by default.

## Interview Questions
1. **How do you view logs of a container that has already been stopped and removed?**
   *Answer*: You cannot view them using `docker logs` if the container is removed. You must use a centralized logging system or have volume-mounted the log directory.
2. **Where should a containerized application write its logs?**
   *Answer*: To `stdout` and `stderr`. Docker captures these automatically.

## Summary
Docker logging is simple if you follow the golden rule: **Log to stdout**. By configuring proper logging drivers and log rotation, you ensure that your applications are debuggable and your servers stay healthy.

---
Prev: [02_redis_mysql_mongodb_containers.md](./02_redis_mysql_mongodb_containers.md) | Index: [Index](../00_index.md) | Next: [04_monitoring.md](./04_monitoring.md)
