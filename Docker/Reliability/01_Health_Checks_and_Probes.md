# 📌 Topic: Health Checks and Probes (Self-Healing)

## 🧠 Concept Explanation (Basic → Expert)
**Basic**: Health Checks are like a doctor's checkup for your container. The orchestrator (Docker/K8s) periodically asks, "Are you okay?" If the container doesn't answer or says "No," the orchestrator kills it and starts a fresh one.
**Expert**: Health Checks are the foundation of **Self-Healing Infrastructure**. Staff-level engineering requires distinguishing between **Liveness Probes** (Is the process alive or dead-locked?), **Readiness Probes** (Is the app ready to handle traffic?), and **Startup Probes** (Has the app finished its slow initialization?). A poorly configured health check can lead to the **Death Spiral**—where a slow-responding app is killed repeatedly, never getting enough time to actually start up and handle load.

## 🏗️ Mental Model
- **Liveness**: "Are you breathing?" If no, I'll try to resuscitate you (Restart).
- **Readiness**: "Are you ready to see patients?" If no, I'll tell the receptionist (Load Balancer) to stop sending people to your room, but I won't kill you.
- **Startup**: "Are you still getting dressed?" I'll wait longer before I start asking if you're breathing.

## ⚡ Actual Behavior
- **Automatic Recovery**: If your app enters a "Deadlock" (CPU is at 100% but it's not responding to requests), the health check will fail, and Docker will automatically restart the container.
- **Zero-Downtime Deployment**: During an update, the Load Balancer won't send traffic to the NEW container until its **Readiness Probe** passes. This prevents users from hitting an app that is still "Booting up."

## 🔬 Internal Mechanics (The Probe Types)
1. **HTTP Probe**: The orchestrator sends a `GET /health` request. A `200 OK` is a pass; anything else is a fail.
2. **TCP Socket Probe**: The orchestrator tries to open a connection on a port (e.g., 3306). If the port is open, it passes.
3. **Exec Probe**: The orchestrator runs a command INSIDE the container (e.g., `pg_isready`). If the command returns exit code 0, it passes.

## 🔁 Execution Flow
1. Container starts.
2. **Initial Delay**: Orchestrator waits 30 seconds for the app to boot.
3. **First Probe**: Orchestrator runs `curl localhost:8080/health`.
4. **Failure**: App returns `503 Service Unavailable` because the DB is still connecting.
5. **Readiness Check**: Load Balancer removes the container from the pool.
6. **Retry**: 10 seconds later, Probe runs again. Returns `200 OK`.
7. **Success**: Load Balancer adds container back to the pool.

## 🧠 Resource Behavior
- **CPU**: Complex health checks (e.g., running a heavy DB query every 2 seconds) can consume significant CPU and add load to the very system they are trying to monitor.
- **Network**: Frequent probes across thousands of containers create a constant "Background Hum" of network traffic.

## 📐 ASCII Diagrams (REQUIRED)

```text
       SELF-HEALING PROBE CYCLE
       
[ Orchestrator ] --( 1: Check )--> [ Container ]
       ^                                |
       |                        ( 2: App Logic )
       |                                |
( 4: Action ) <--( 3: Status )----------+
       |
+------+------+-----------------+
|             |                 |
[ RESTART ]  [ REMOVE FROM LB ] [ DO NOTHING ]
(Liveness)   (Readiness)        (Healthy)
```

## 🔍 Code (Docker Compose Healthcheck)
```yaml
services:
  db:
    image: postgres:15
    healthcheck:
      # Check if postgres is ready to accept connections
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s

  api:
    image: my-node-app
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

## 💥 Production Failures
- **The "Shallow" Health Check**: Your health check only checks if the web server is running. It doesn't check the DB connection. The web server is UP, but every request fails because the DB is DOWN. The Load Balancer keeps sending traffic to a broken app.
  *Fix*: Implement a "Deep" health check that verifies all critical dependencies (DB, Redis, API).
- **The "Panic" Restart**: Your DB is slow. All 10 API containers fail their health checks at the same time. Docker restarts all 10 containers simultaneously. Now you have 0 containers online and the DB is even more overwhelmed by 10 new startup connections.
  *Fix*: Set a long `timeout` and `retries` to allow for temporary slow-downs.

## 🧪 Real-time Q&A
**Q: Should my health check query the Database?**
**A**: **Yes, but carefully.** Don't run a complex `SELECT COUNT(*)` every 5 seconds. Run a simple `SELECT 1`. If your app can't talk to the DB, it's not "Ready" and shouldn't be receiving traffic.

## ⚠️ Edge Cases
- **Zombie Processes**: A process can be "Running" (PID exists) but completely frozen due to a kernel bug or resource deadlock. Only an **External Probe** (HTTP/TCP) can detect this; a simple process check will show it as "Healthy."

## 🏢 Best Practices
- **Use separate endpoints**: `/health/live` (cheap) and `/health/ready` (checks DB/Redis).
- **Don't be too aggressive**: A 1-second interval is usually overkill and creates unnecessary load.
- **Log health failures**: When a check fails, log the *reason* (e.g., "Redis connection timed out") so you can debug it later.

## ⚖️ Trade-offs
| Check Type | Accuracy | Performance Impact |
| :--- | :--- | :--- |
| **TCP Port** | Low | **Lowest** |
| **HTTP Endpoint**| Medium | Medium |
| **Deep Script** | **Highest** | High |

## 💼 Interview Q&A
**Q: What is the difference between a Liveness probe and a Readiness probe?**
**A**: A **Liveness probe** determines if the container is still running. If it fails, the orchestrator kills and restarts the container. Use this to catch deadlocks. A **Readiness probe** determines if the container is ready to handle requests. If it fails, the orchestrator removes the container from the Load Balancer's rotation but does **NOT** kill it. Use this for apps that are temporarily busy, performing a large migration, or waiting for a dependency like a database to become available.

## 🧩 Practice Problems
1. Create a Node.js app with a `/health` endpoint that returns a 500 error if a file `REPAIR_MODE` exists.
2. Deploy it with a Docker healthcheck and see it go from "healthy" to "unhealthy" when you `touch REPAIR_MODE`.
3. Observe how Docker stops showing the "healthy" status in `docker ps`.

---
Prev: [05_Kernel_Tuning_for_High_Throughput.md](../Performance/05_Kernel_Tuning_for_High_Throughput.md) | Index: [00_Index.md](../00_Index.md) | Next: [02_Circuit_Breakers_and_Retries.md](./02_Circuit_Breakers_and_Retries.md)
---
