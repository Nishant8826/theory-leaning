# 33 – Docker Day 2: Container Operations, Port Mapping, Volumes & Management

---

## Table of Contents

1. [Docker Container Lifecycle – The Full Picture](#1-docker-container-lifecycle--the-full-picture)
2. [Port Mapping – Connecting the Outside World](#2-port-mapping--connecting-the-outside-world)
3. [Volume Mapping – Persisting Data Outside Containers](#3-volume-mapping--persisting-data-outside-containers)
4. [Running Modes – Detached vs Interactive](#4-running-modes--detached-vs-interactive)
5. [Container Naming & Management](#5-container-naming--management)
6. [NGINX – The Modern Web Server](#6-nginx--the-modern-web-server)
7. [Accessing Running Containers – docker exec](#7-accessing-running-containers--docker-exec)
8. [Container Monitoring – docker stats](#8-container-monitoring--docker-stats)
9. [Bulk Container Operations](#9-bulk-container-operations)
10. [Shell Types Inside Containers](#10-shell-types-inside-containers)
11. [Complete Docker Command Reference](#11-complete-docker-command-reference)
12. [Tech Stack Mapping](#12-tech-stack-mapping)
13. [Visual Diagrams](#13-visual-diagrams)
14. [Code & Practical Examples](#14-code--practical-examples)
15. [Scenario-Based Q&A](#15-scenario-based-qa)
16. [Interview Q&A](#16-interview-qa)

---

## 1. Docker Container Lifecycle – The Full Picture

### What
Every Docker container moves through a series of **states** during its life. Understanding these states and the commands that transition between them is the foundation of day-to-day Docker work.

> 💡 **Analogy:** Think of a container like a laptop. You can power it on (start), put it to sleep (pause), restart it, force-shut it down (kill), or throw it away (remove). Each state has a specific use case.

### The States

| State | Meaning | How to get there |
|-------|---------|-----------------|
| **Created** | Container exists but hasn't started | `docker create` |
| **Running** | Container is actively executing | `docker run` or `docker start` |
| **Paused** | All processes frozen, still in memory | `docker pause` |
| **Stopped/Exited** | Container stopped, but still exists on disk | `docker stop` or `docker kill` |
| **Removed** | Container is fully deleted | `docker rm` |

### Every Lifecycle Command Explained

#### `docker run` — Create AND Start (most common)
```bash
docker run nginx
# Creates a new container from the nginx image AND starts it immediately
# This is NOT the same as docker start — run always creates a NEW container
```

#### `docker start` — Start a Stopped Container
```bash
docker start my-nginx
# Restarts a container that previously stopped
# Does NOT create a new container — reuses the existing one
```

#### `docker stop` — Graceful Stop
```bash
docker stop my-nginx
# Sends SIGTERM signal — gives the container time to shut down cleanly
# Waits 10 seconds, then sends SIGKILL if still running
# Best practice: always try stop before kill
```

#### `docker restart` — Stop + Start
```bash
docker restart my-nginx
# Equivalent to: docker stop my-nginx && docker start my-nginx
# Useful after config changes
```

#### `docker pause` — Freeze (not stop)
```bash
docker pause my-nginx
# Freezes ALL processes inside the container using Linux cgroups
# Container stays in memory — resumes instantly
# Use case: temporarily free up CPU without losing container state
```

#### `docker unpause` — Resume Frozen Container
```bash
docker unpause my-nginx
# Resumes all frozen processes
# Picks up exactly where it left off
```

#### `docker kill` — Force Stop (Immediate)
```bash
docker kill my-nginx
# Sends SIGKILL immediately — no graceful shutdown
# Use only when docker stop doesn't work
# Risk: data corruption if container was writing files
```

#### `docker rm` — Delete Container
```bash
docker rm my-nginx           # Remove a stopped container
docker rm -f my-nginx        # Force remove even if running (combines kill + rm)
docker rm $(docker ps -aq)   # Remove ALL stopped containers
```

### Impact of Each Command

| Command | Container State After | Data in Container |
|---------|----------------------|-------------------|
| `stop` | Exited (saved on disk) | Preserved |
| `kill` | Exited (saved on disk) | Preserved (may corrupt if mid-write) |
| `pause` | Paused (in memory) | Preserved perfectly |
| `rm` | Gone forever | Lost ❌ |
| `rm -f` | Gone forever | Lost ❌ |

> ⚠️ **Key rule:** Never store important data inside a container's filesystem. When the container is removed, that data is gone forever. Use **volumes** for anything you want to keep.

---

## 2. Port Mapping – Connecting the Outside World

### What
A container runs in its own **isolated network**. By default, nothing outside the container — not even your browser on the same machine — can reach it. **Port mapping** creates a bridge between a port on your host machine and a port inside the container.

> 💡 **Analogy:** Your container is like an apartment in a building. The building (host machine) has public-facing door numbers (host ports). Port mapping is telling the building: "If someone knocks on door 8080, forward them to apartment 80 inside."

### Why
- Containers are network-isolated by default (security)
- Multiple containers can run the same internal port (e.g., multiple apps all using port 80 internally)
- You choose which host port to expose — no conflicts

### How – The `-p` Flag

```bash
docker run -p HOST_PORT:CONTAINER_PORT image_name
#               ↑              ↑
#     Port on your VM    Port inside container
```

#### Examples

```bash
# Map VM port 8080 to container's internal port 80
docker run -p 8080:80 nginx
# Access at: http://YOUR_VM_IP:8080

# Map VM port 3000 to container's port 3000 (Node.js app)
docker run -p 3000:3000 my-node-app

# Map VM port 9090 to Jenkins container's port 8080
docker run -p 9090:8080 jenkins/jenkins

# Multiple port mappings (e.g., HTTP + HTTPS)
docker run -p 80:80 -p 443:443 nginx

# Map to all interfaces (default) or specific IP
docker run -p 0.0.0.0:8080:80 nginx   # All interfaces
docker run -p 127.0.0.1:8080:80 nginx  # Localhost only (more secure)
```

### Running Multiple Containers on the Same Host

```bash
# Three NGINX containers on the same machine, different host ports
docker run -d -p 8081:80 --name nginx1 nginx
docker run -d -p 8082:80 --name nginx2 nginx
docker run -d -p 8083:80 --name nginx3 nginx

# All three use port 80 INTERNALLY
# Accessible on the host at 8081, 8082, 8083 respectively
```

### What Happens Without Port Mapping

```bash
docker run nginx
# NGINX starts and listens on port 80 INSIDE the container
# But nothing from outside can reach it
# No -p flag = no external access = container is isolated
```

### Firewall Consideration (GCP/AWS)
Port mapping alone isn't enough on cloud VMs. You also need to:
- **GCP:** Add Firewall Rule allowing the host port
- **AWS:** Add Inbound Rule in Security Group for the host port

### Impact

| Without Port Mapping | With Port Mapping |
|---------------------|-------------------|
| Container runs but is unreachable | Accessible from browser/external |
| No service is exposed | Service available on chosen port |
| Container is safely isolated | Controlled, deliberate exposure |

---

## 3. Volume Mapping – Persisting Data Outside Containers

### What
**Volumes** are the mechanism for storing data **outside** a container's filesystem, on the host machine (or cloud storage). Data in a volume **survives container deletion** — the container can be removed and recreated, and the data remains.

> 💡 **Analogy:** A container is like a hotel room. When you check out (container removed), the room is reset — your belongings are gone. A volume is like a storage unit outside the hotel. No matter how many times you check in and out, your belongings stay in the storage unit.

### Why – The Golden Rule
> ❌ **Never store important data inside a container**
> ✅ **Always use volumes for data that must persist**

Without volumes:
- Container deleted → all data gone (logs, uploads, database files)
- Container crashed → new container has no history
- Multiple containers can't share data

With volumes:
- Container lifecycle is separate from data lifecycle
- Upgrade a container (new image version) → data remains
- Multiple containers can mount the same volume

### How – The `-v` Flag

```bash
docker run -v HOST_PATH:CONTAINER_PATH image_name
#               ↑                ↑
#     Path on your host    Path inside container
```

#### Examples

```bash
# Mount host directory to NGINX html directory
docker run -d -p 8080:80 -v /home/ubuntu/mywebsite:/usr/share/nginx/html --name my-nginx nginx

# Now edit /home/ubuntu/mywebsite/index.html on the host
# Changes appear immediately in the container — no rebuild needed

# Mount a host directory for Jenkins data
docker run -d -p 8080:8080 -v /home/ubuntu/jenkins-data:/var/jenkins_home --name jenkins jenkins/jenkins

# Jenkins data (jobs, plugins, configs) saved in /home/ubuntu/jenkins-data
# Delete and recreate the container → all Jenkins data still there
```

### Named Volumes (Docker-Managed)

Instead of specifying a host path, let Docker manage the volume location:

```bash
# Create a named volume
docker volume create my-data

# Use it
docker run -d -v my-data:/var/lib/mysql mysql

# List volumes
docker volume ls

# Inspect where Docker stores it
docker volume inspect my-data
# Location: /var/lib/docker/volumes/my-data/_data
```

### Volume Types Comparison

| Type | Syntax | Managed by | Best For |
|------|--------|-----------|---------|
| **Bind Mount** | `-v /host/path:/container/path` | You | Development (edit files live) |
| **Named Volume** | `-v my-volume:/container/path` | Docker | Production data persistence |
| **tmpfs Mount** | `--tmpfs /container/path` | RAM | Temporary sensitive data |

### 6.1 NGINX with Custom Content – Step-by-Step Practical

#### What
A hands-on exercise to host a custom website using NGINX and Docker volumes.

#### Why
- Learn how to map host ports to container ports.
- Understand how Docker volumes enable "Live Reloading" without rebuilding images or restarting containers.
- Practice basic container management (run, stop, logs).

#### How – Step-by-Step

**Step 1: Create the Project Directory**
Create a folder on your Ubuntu host to store your website files.
```bash
mkdir -p /home/ubuntu/mysite
```

**Step 2: Create your HTML Content**
Create an `index.html` file. This is the entry point for your website.
```bash
echo "<h1>Hello from NGINX in Docker! 🐳</h1><p>Served via Volume Mapping</p>" > /home/ubuntu/mysite/index.html
```

**Step 3: Run the NGINX Container**
Deploy the container with both port and volume mapping.
```bash
docker run -d --name custom-nginx -p 8080:80 -v /home/ubuntu/mysite:/usr/share/nginx/html nginx
```

**Step 4: Verify and Access**
- **Check status:** `docker ps`
- **Access in browser:** `http://YOUR_VM_IP:8080` (or `localhost:8080` if local)

**Step 5: Test Live Updates**
Modify the file on the host machine and refresh your browser. You will see the changes immediately without restarting the container.
```bash
echo "<h1>Updated! No restart needed.</h1>" > /home/ubuntu/mysite/index.html
```

#### Troubleshooting: Fixing the 403 Forbidden Error
If your browser shows a "403 Forbidden" error, NGINX cannot find or read your file. Follow these steps:

1.  **Check if the file exists:** Ensure `index.html` is actually in the folder: `ls -l /home/ubuntu/mysite/index.html`.
2.  **Verify Permissions:** NGINX needs read permissions. Fix them with: `chmod -R 755 /home/ubuntu/mysite`.
3.  **Inspect Logs:** Check the container's error logs to see the specific reason: `docker logs custom-nginx`.
4.  **Path Mismatch:** If you are on Windows using PowerShell, use `${PWD}` instead of the Linux path: `-v ${PWD}/mysite:/usr/share/nginx/html`.

#### Impact
- **Speed:** Develop and test websites instantly without environment setup.
- **Isolation:** Your host machine stays clean (no NGINX installed locally).
- **Persistent Data:** Your website files stay safe on the host even if the container is deleted.

### Impact

| Storing Data in Container | Using Volumes |
|--------------------------|---------------|
| `docker rm` → data GONE ❌ | `docker rm` → data SAFE ✅ |
| Can't share between containers | Multiple containers share same data |
| Upgrade = lose data | Upgrade = keep data |
| No backup option | Back up the host path easily |

---

## 4. Running Modes – Detached vs Interactive

### What
When you start a container, you choose HOW to interact with it:
- **Foreground (default):** Container output appears in your terminal. Terminal is blocked.
- **Detached (`-d`):** Container runs in background. Terminal is free.
- **Interactive (`-it`):** Your terminal connects to the container's shell. You can type commands inside it.

---

### Detached Mode (`-d`)

#### What
The container runs silently in the background. You get your terminal back immediately after running the command.

```bash
docker run -d -p 8080:80 --name nginx-bg nginx
# Output: a1b2c3d4e5f6...  (just the container ID)
# Terminal is immediately free
# NGINX is running in background
```

#### Why Use It
- Web servers, databases, Jenkins — anything that should keep running
- You don't want your terminal blocked by container logs
- Production use case: always detached

#### Check What's Running
```bash
docker ps
# Shows all running containers, their ports, names, uptime
```

#### View Logs Without Attaching
```bash
docker logs nginx-bg           # Show all past logs
docker logs -f nginx-bg        # Follow logs in real time (like tail -f)
docker logs --tail 50 nginx-bg # Show last 50 lines only
```

---

### Interactive Mode (`-it`)

#### What
`-i` = keep STDIN open (receive your input)
`-t` = allocate a terminal (TTY — so you see output formatted properly)

Together: `-it` gives you a live shell inside the container.

```bash
# Start a new Ubuntu container and drop into bash shell
docker run -it ubuntu /bin/bash
# You're now INSIDE the container:
root@a1b2c3d4:/# ls
root@a1b2c3d4:/# apt update
root@a1b2c3d4:/# apt install python3 git -y
root@a1b2c3d4:/# python3 --version
# Type 'exit' to leave the container
```

#### When to Use Interactive Mode
- Debugging a container's internal state
- Installing packages or testing commands inside a specific image
- Exploring what files/directories exist in an image
- Running one-off commands in a specific environment

---

### The `--rm` Flag – Auto-Remove After Exit

```bash
docker run --rm ubuntu echo "Hello from inside Ubuntu"
# Container runs, prints "Hello from inside Ubuntu"
# Container is AUTOMATICALLY DELETED when it exits
# No orphaned stopped containers cluttering your system
```

Best combined with interactive mode for temporary sessions:
```bash
docker run --rm -it python:3.11 python
# Opens Python REPL inside Python 3.11 container
# Exit Python → container is immediately removed
```

---

### Running One-Off Commands

You can run a single command inside a container without an interactive shell:

```bash
# Print the date from an Alpine Linux container
docker run alpine date
# Output: Thu Apr 30 14:23:01 UTC 2026
# Container starts, runs 'date', exits, stays stopped

# Check Alpine's IP
docker run alpine ip addr

# Run Python script without installing Python locally
docker run python:3.11 python -c "print('Hello from Python container')"
```

---

## 5. Container Naming & Management

### What
By default, Docker assigns random funny names to containers (like `angry_einstein` or `jovial_curie`). The `--name` flag lets you give containers meaningful names for easy management.

### Why
- Easier to reference: `docker stop jenkins` vs `docker stop a3f8b2c1d9e4`
- Scripts and pipelines can reference by name reliably
- Clearer in `docker ps` output — you know what each container is

### How

```bash
# Create with a custom name
docker run -d --name jenkins -p 8080:8080 jenkins/jenkins
docker run -d --name my-nginx -p 80:80 nginx
docker run -d --name postgres-db -p 5432:5432 postgres

# Now reference by name
docker stop jenkins
docker start jenkins
docker logs jenkins
docker exec -it jenkins /bin/bash
docker rm -f jenkins
```

### Naming Conventions (Best Practice)

```
# For projects
app-name-service: shopping-cart-api, shopping-cart-db, shopping-cart-cache

# For environments
nginx-dev, nginx-qa, nginx-prod

# For teams
jenkins-master, jenkins-agent-1, jenkins-agent-2
```

### Listing Containers

```bash
docker ps           # Running containers only
docker ps -a        # ALL containers (running + stopped)
docker ps -q        # Only container IDs (quiet mode — useful for scripting)
docker ps -a | wc -l  # Count total containers (including header line)
```

### Force Remove Running Containers

```bash
docker rm -f container_name      # Force-removes even if running
docker rm -f $(docker ps -aq)    # Remove ALL containers (running + stopped)
```

---

## 6. NGINX – The Modern Web Server

### What
**NGINX** (pronounced "engine-x") is a high-performance web server, reverse proxy, and load balancer. It's the standard web server used in modern infrastructure.

> 💡 **Comparison:** Apache was the dominant web server for 20 years. NGINX was built to handle modern high-concurrency workloads — it handles 10,000 concurrent connections efficiently where Apache struggles. Tomcat is specifically a Java application server — useful only for Java apps.

### Why NGINX in Docker

```bash
# Official NGINX image is tiny (~186MB)
# Ready to serve static files with zero configuration
# Can be configured as:
#   - Static file server (HTML, CSS, JS)
#   - Reverse proxy (forward requests to Node.js, Spring Boot)
#   - Load balancer (distribute traffic across multiple backends)
#   - SSL terminator
```

### The Default NGINX Container

```bash
docker run -d -p 8080:80 --name nginx-test nginx

# What's inside the container:
# /usr/share/nginx/html/    ← Default web root (serve files from here)
# /etc/nginx/nginx.conf     ← Main NGINX config
# /etc/nginx/conf.d/        ← Site-specific configs
# /var/log/nginx/           ← Access and error logs
```

### Access Logs vs Container Logs

| Log Type | Location | What it shows | How to view |
|----------|----------|--------------|-------------|
| **Container logs** | Docker daemon | Application STDOUT/STDERR output | `docker logs my-nginx` |
| **NGINX access logs** | `/var/log/nginx/access.log` inside container | Every HTTP request (IP, URL, status code) | `docker exec my-nginx cat /var/log/nginx/access.log` |
| **NGINX error logs** | `/var/log/nginx/error.log` inside container | NGINX errors, config problems | `docker exec my-nginx cat /var/log/nginx/error.log` |

---

## 7. Accessing Running Containers – docker exec

### What
`docker exec` runs a command INSIDE an already-running container. It's the primary way to inspect, debug, or modify a container that's already up.

> 💡 **Difference from `docker run -it`:** `docker run` creates a NEW container. `docker exec` enters an EXISTING, running container.

### The Most Common Pattern

```bash
docker exec -it CONTAINER_NAME /bin/bash
# -i = interactive (keep stdin open)
# -t = terminal (allocate TTY)
# /bin/bash = the command to run (opens bash shell)
```

### Practical Examples

```bash
# Enter a running NGINX container
docker exec -it my-nginx /bin/bash

# Now you're inside NGINX container:
root@a1b2:/# ls /usr/share/nginx/html
root@a1b2:/# cat /etc/nginx/nginx.conf
root@a1b2:/# nginx -t   # Test nginx config
root@a1b2:/# exit

# Enter Jenkins container
docker exec -it jenkins /bin/bash

# Run a single command without entering interactive shell
docker exec my-nginx nginx -s reload      # Reload nginx config
docker exec my-nginx cat /etc/hosts       # Print hosts file
docker exec jenkins java -version         # Check Java version inside Jenkins
```

### What If There's No bash?

Some minimal images (like Alpine) don't have bash — only `sh`:

```bash
docker exec -it my-alpine-container /bin/sh
# Use sh instead of bash
```

---

## 8. Container Monitoring – docker stats

### What
`docker stats` shows **real-time resource usage** for all running containers — CPU, memory, network I/O, and disk I/O.

### Why
- Identify which container is consuming too much CPU or memory
- Debug performance issues without installing monitoring tools
- Quick health check of all running containers

### How

```bash
# Live stats for all running containers (updates every second)
docker stats

# Stats for specific container
docker stats my-nginx

# One-time snapshot (no live updates)
docker stats --no-stream

# Format output
docker stats --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"
```

### Reading the Stats Output

```
CONTAINER ID   NAME       CPU %   MEM USAGE / LIMIT    MEM %   NET I/O         BLOCK I/O
a1b2c3d4       my-nginx   0.00%   5.4MiB / 3.84GiB    0.14%   1.2kB / 648B    0B / 0B
b2c3d4e5       jenkins    2.50%   512MiB / 3.84GiB    13.0%   45kB / 12kB     8MB / 2MB
```

| Column | Meaning |
|--------|---------|
| `CPU %` | Percentage of host CPU being used |
| `MEM USAGE / LIMIT` | Current memory used / Maximum allowed |
| `MEM %` | Memory usage as percentage of limit |
| `NET I/O` | Network data received / sent |
| `BLOCK I/O` | Disk data read / written |

### Setting Resource Limits

```bash
# Limit container to 512MB RAM and 1 CPU
docker run -d --name limited-app --memory="512m" --cpus="1.0" -p 3000:3000 my-app

# Limit to 25% of one CPU
docker run -d --cpus="0.25" my-app
```

---

## 9. Bulk Container Operations

### What
When you need to create, manage, or destroy many containers at once, bash loops and Docker's quiet mode make this efficient.

### Why
- Testing container orchestration patterns
- Creating multiple instances for load testing
- Spinning up a development environment with many services
- Cleaning up after tests

### Bulk Creation with a Loop

```bash
# Create 10 NGINX containers in one command
for i in {1..10}; do
  docker run -d --name nginx-$i -p $((8080 + i)):80 nginx
done

# Creates: nginx-1 (port 8081), nginx-2 (8082), ... nginx-10 (8090)

# Create 30 containers (from class)
for i in $(seq 1 30); do
  docker run -d --name test-container-$i ubuntu sleep infinity
done

# Verify
docker ps | wc -l
```

### Bulk Remove All Containers

```bash
# Stop all running containers
docker stop $(docker ps -q)

# Remove all stopped containers
docker rm $(docker ps -aq)

# Force remove ALL (running + stopped) in one command
docker rm -f $(docker ps -aq)

# Count containers
docker ps -a | wc -l
```

### Docker System Cleanup

```bash
# Remove everything not in use (containers, images, networks, volumes)
docker system prune

# Also remove unused volumes
docker system prune --volumes

# See how much space Docker is using
docker system df
```

---

## 10. Shell Types Inside Containers

### What
When you enter a container with `docker exec -it container /bin/bash`, you're using a **shell** — a command interpreter. Different shells exist and different images include different ones.

### The Four Shell Types

| Shell | Full Name | Common in | Notes |
|-------|-----------|-----------|-------|
| **bash** | Bourne Again Shell | Ubuntu, Debian, most Linux | Default in most containers. Most feature-rich. |
| **sh** | Bourne Shell | Alpine, minimal images | Minimal — no color, limited features. Present everywhere. |
| **ksh** | Korn Shell | Enterprise Linux (AIX, older RHEL) | Rare in containers |
| **zsh** | Z Shell | macOS default, developer machines | Rare in containers unless explicitly installed |

### Practical Impact

```bash
# Ubuntu-based container → use bash
docker run -it ubuntu /bin/bash

# Alpine-based container → bash might not exist, use sh
docker run -it alpine /bin/sh

# If you try bash on Alpine and it fails:
docker exec -it my-alpine /bin/bash
# Error: OCI runtime exec failed: executable file not found in $PATH

# Fix:
docker exec -it my-alpine /bin/sh
```

### Checking What Shells Are Available

```bash
docker exec -it my-container cat /etc/shells
# Lists all installed shells
```

### Installing bash on Alpine (if needed)

```bash
docker exec -it alpine-container /bin/sh
# Inside container:
apk add --no-cache bash
exit

# Now bash works:
docker exec -it alpine-container /bin/bash
```

---

## 11. Complete Docker Command Reference

### Image Commands

```bash
docker pull nginx              # Download image from Docker Hub
docker images                  # List all local images
docker images -q               # List only image IDs
docker rmi nginx               # Remove an image
docker rmi -f nginx            # Force remove (even if containers use it)
docker rmi $(docker images -q) # Remove ALL images
docker image inspect nginx     # Detailed image metadata
docker history nginx           # Show image layers
```

### Container Run Commands

```bash
# Basic patterns
docker run nginx                           # Run in foreground
docker run -d nginx                        # Run in detached (background)
docker run -it ubuntu /bin/bash            # Interactive with shell
docker run --rm ubuntu echo "hi"           # Auto-remove after exit
docker run --name my-app nginx             # Custom name
docker run -p 8080:80 nginx               # Port mapping
docker run -v /host:/container nginx       # Volume mapping
docker run alpine date                     # Run single command

# Combined (common pattern)
docker run -d --name my-nginx -p 8080:80 -v /home/ubuntu/html:/usr/share/nginx/html --restart unless-stopped nginx
```

### Container Management Commands

```bash
docker ps                   # List running containers
docker ps -a                # List all containers (including stopped)
docker ps -q                # List running container IDs only
docker ps -aq               # List ALL container IDs
docker ps -a | wc -l        # Count all containers

docker start my-nginx       # Start stopped container
docker stop my-nginx        # Graceful stop (SIGTERM)
docker restart my-nginx     # Stop + start
docker pause my-nginx       # Freeze all processes
docker unpause my-nginx     # Resume frozen processes
docker kill my-nginx        # Force stop (SIGKILL)

docker rm my-nginx          # Remove stopped container
docker rm -f my-nginx       # Force remove running container
docker rm $(docker ps -aq)  # Remove all stopped containers
docker rm -f $(docker ps -aq) # Force remove ALL containers
```

### Inspection & Debugging

```bash
docker logs my-nginx              # View container stdout/stderr logs
docker logs -f my-nginx           # Follow logs in real time
docker logs --tail 100 my-nginx   # Last 100 lines

docker exec -it my-nginx /bin/bash  # Open interactive shell in container
docker exec my-nginx ls /etc        # Run single command in container

docker inspect my-nginx            # Full JSON metadata (IP, mounts, config)
docker stats                       # Real-time CPU/memory/network stats
docker stats --no-stream           # One-time stats snapshot
docker top my-nginx                # Processes running inside container
docker port my-nginx               # Show port mappings
```

### Volume Commands

```bash
docker volume create my-data      # Create named volume
docker volume ls                  # List all volumes
docker volume inspect my-data     # Detailed volume info
docker volume rm my-data          # Remove volume
docker volume prune               # Remove all unused volumes
```

### System Commands

```bash
docker system df           # Show Docker disk usage
docker system prune        # Remove all unused resources
docker info                # System-wide Docker info
docker version             # Docker version info
```

---

## 12. Tech Stack Mapping

### Docker in a Real DevOps Pipeline

```
Developer writes code
        │
        ▼
Git push to GitHub
        │
        ▼
Jenkins CI Pipeline:
  Stage 1: Clone code
  Stage 2: mvn clean package / npm build
  Stage 3: docker build -t app:v1.2 .
  Stage 4: docker push registry/app:v1.2
        │
        ▼
Container Registry (Docker Hub / AWS ECR / GCR)
        │
        ▼
Deployment (Docker run / Kubernetes / ECS)
  docker run -d -p 80:3000 -v /data:/app/data --name shopping-cart registry/shopping-cart:v1.2
```

### Common Docker Use Cases by Stack

| Application | Image | Port Mapping | Volume Mapping |
|-------------|-------|-------------|----------------|
| **NGINX** (static site) | `nginx` | `-p 80:80` | `-v /html:/usr/share/nginx/html` |
| **Jenkins** | `jenkins/jenkins` | `-p 8080:8080` | `-v /data:/var/jenkins_home` |
| **Node.js API** | `node:18` | `-p 3000:3000` | `-v /app:/usr/src/app` |
| **PostgreSQL** | `postgres:15` | `-p 5432:5432` | `-v pg-data:/var/lib/postgresql/data` |
| **MongoDB** | `mongo:6` | `-p 27017:27017` | `-v mongo-data:/data/db` |
| **Redis** | `redis:7` | `-p 6379:6379` | `-v redis-data:/data` |
| **Spring Boot** | `openjdk:21` | `-p 8080:8080` | `-v /logs:/app/logs` |
| **Python API** | `python:3.11` | `-p 5000:5000` | `-v /data:/app/data` |

---

## 13. Visual Diagrams

### Diagram 1: Container Lifecycle State Machine

```
                    docker run
  [Image] ────────────────────────────► [Running]
                                             │
                              ┌──────────────┼──────────────┐
                              │              │              │
                         docker pause  docker stop    docker kill
                              │              │              │
                              ▼              ▼              ▼
                          [Paused]      [Stopped/       [Stopped/
                              │          Exited]         Exited]
                              │              │              │
                        docker unpause       │              │
                              │         docker start        │
                              └──► [Running] ◄─────────────┘
                                       │
                                  docker rm -f
                                       │
                                       ▼
                                   [Deleted]
                                  (gone forever)
```

---

### Diagram 2: Port Mapping

```
OUTSIDE WORLD                   HOST MACHINE (VM)                 CONTAINER
─────────────                   ─────────────────                 ─────────
                                    Port 8080 ──────────────────► Port 80 (NGINX)
Browser                             Port 5432 ──────────────────► Port 5432 (Postgres)
http://IP:8080 ────────────────►    Port 8081 ──────────────────► Port 80 (NGINX 2)
                                    Port 3000 ──────────────────► Port 3000 (Node.js)
                                    (host ports)                  (container ports)

docker run -p 8080:80 nginx
              ↑    ↑
           HOST  CONTAINER
```

---

### Diagram 3: Volume Mapping

```
HOST MACHINE                              CONTAINER
────────────                              ─────────
/home/ubuntu/html/                        /usr/share/nginx/html/
  index.html        ◄── synchronized ───►   index.html
  style.css                                  style.css
  
[Edit file on host]  ← changes appear →  [Container serves updated file]
[Container deleted]   data still here    [New container, same data]

docker run -v /home/ubuntu/html:/usr/share/nginx/html nginx
              ↑ HOST PATH                  ↑ CONTAINER PATH
```

---

### Diagram 4: Detached vs Interactive Mode

```
FOREGROUND (default)              DETACHED (-d)              INTERACTIVE (-it)
────────────────────              ─────────────              ─────────────────
docker run nginx                  docker run -d nginx        docker run -it ubuntu bash

Terminal:                         Terminal:                  Terminal:
│ NGINX logs stream here...       │ a1b2c3d4e5f6            │ root@a1b2:/# ←── you type here
│ [4/May/2026 ...] GET /          │ (free immediately)       │ root@a1b2:/# ls
│ [4/May/2026 ...] GET /          │                          │ root@a1b2:/# apt install python3
│ (terminal is BLOCKED)           │ docker logs -f nginx     │ root@a1b2:/# exit
│                                 │ to see logs separately   │ (container stops)
│ Ctrl+C to stop
```

---

### Diagram 5: docker exec vs docker run

```
docker run -it ubuntu /bin/bash          docker exec -it my-container /bin/bash
──────────────────────────────           ─────────────────────────────────────
Creates a BRAND NEW container            Enters an EXISTING running container
     │                                              │
     ▼                                              ▼
New container ID: b2c3d4                  Same container: a1b2c3
New filesystem                            Same filesystem (your changes are there)
New environment                           Same environment
Exits when you exit bash                  Container keeps running when you exit
```

---

### Diagram 6: Bulk Container Loop

```
for i in {1..5}; do
  docker run -d --name nginx-$i -p $((8080+i)):80 nginx
done

Result:
┌────────────────┬──────────┬──────────────┐
│ Container Name │ Host Port│ Container Port│
├────────────────┼──────────┼──────────────┤
│ nginx-1        │ 8081     │ 80           │
│ nginx-2        │ 8082     │ 80           │
│ nginx-3        │ 8083     │ 80           │
│ nginx-4        │ 8084     │ 80           │
│ nginx-5        │ 8085     │ 80           │
└────────────────┴──────────┴──────────────┘
All 5 running simultaneously on same host
```

---

## 14. Code & Practical Examples

### Example 1: Complete NGINX Setup with Custom Content

```bash
#!/bin/bash
# Setup custom NGINX container with persistent content

# Step 1: Create directory structure on host
mkdir -p /home/ubuntu/mywebsite

# Step 2: Create a custom HTML page
cat > /home/ubuntu/mywebsite/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>My Docker NGINX Site</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
        h1 { color: #2ecc71; }
    </style>
</head>
<body>
    <h1>Hello from NGINX in Docker! 🐳</h1>
    <p>This content is served from a volume-mounted directory.</p>
    <p>Edit /home/ubuntu/mywebsite/index.html to change this page.</p>
</body>
</html>
EOF

# Step 3: Run NGINX with volume and port mapping
docker run -d --name my-nginx -p 8080:80 -v /home/ubuntu/mywebsite:/usr/share/nginx/html --restart unless-stopped nginx

# Step 4: Verify it's running
docker ps
echo "Access your site at: http://$(curl -s ifconfig.me):8080"

# Step 5: Watch the logs
docker logs -f my-nginx
```

---

### Example 2: Containerized Jenkins with Persistent Data

```bash
#!/bin/bash
# Run Jenkins with all data persisted to host

# Create persistent directory
mkdir -p /home/ubuntu/jenkins-data

# Set correct permissions (Jenkins runs as UID 1000)
chown -R 1000:1000 /home/ubuntu/jenkins-data

# Run Jenkins
docker run -d --name jenkins -p 8080:8080 -p 50000:50000 -v /home/ubuntu/jenkins-data:/var/jenkins_home --restart unless-stopped jenkins/jenkins:lts

# Port 8080 = Jenkins Web UI
# Port 50000 = Jenkins agent communication

# Get initial admin password
echo "Waiting for Jenkins to start..."
sleep 30
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

---

### Example 3: Running Multiple Services

```bash
#!/bin/bash
# Start a complete local development environment

# NGINX (web server / reverse proxy)
docker run -d --name nginx -p 80:80 -v /home/ubuntu/nginx-conf:/etc/nginx/conf.d nginx

# PostgreSQL database
docker run -d --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=mysecret -e POSTGRES_DB=myapp -v postgres-data:/var/lib/postgresql/data postgres:15

# Redis cache
docker run -d --name redis -p 6379:6379 -v redis-data:/data redis:7 redis-server --appendonly yes

# Node.js API
docker run -d --name api -p 3000:3000 -e DATABASE_URL=postgresql://postgres:mysecret@postgres:5432/myapp -e REDIS_URL=redis://redis:6379 my-node-api:latest

docker ps
echo "All services started!"
```

---

### Example 4: Cleanup Script

```bash
#!/bin/bash
# Complete Docker cleanup

echo "=== Current State ==="
docker ps -a
echo "Total containers: $(docker ps -a | wc -l)"
echo "Disk usage:"
docker system df

echo ""
echo "=== Stopping all running containers ==="
docker stop $(docker ps -q) 2>/dev/null || echo "No running containers"

echo "=== Removing all containers ==="
docker rm $(docker ps -aq) 2>/dev/null || echo "No containers to remove"

echo "=== Removing unused images ==="
docker image prune -f

echo "=== Removing unused volumes ==="
docker volume prune -f

echo ""
echo "=== After Cleanup ==="
docker system df
echo "Containers remaining: $(docker ps -a | wc -l)"
```

---

### Example 5: Basic Dockerfile for Node.js App

```dockerfile
# Dockerfile for a Node.js API
FROM node:22-alpine

# Set working directory inside container
WORKDIR /usr/src/app

# Copy dependency files first (for layer caching)
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy application code
COPY . .

# Expose the port your app runs on
EXPOSE 3000

# Command to start the application
CMD ["node", "server.js"]
```

Build and run:
```bash
# Build the image
docker build -t my-node-app:v1.0 .

# Run it with port and volume mapping
docker run -d --name node-api -p 3000:3000 -v /app/logs:/usr/src/app/logs my-node-app:v1.0
```

---

### Example 6: Jenkins Pipeline Using Docker

```groovy
// Jenkinsfile using Docker containers as build agents

pipeline {
    agent {
        docker {
            image 'maven:3.9-openjdk-21'   // Build inside Maven container
            args '-v /root/.m2:/root/.m2'    // Cache Maven dependencies
        }
    }

    stages {
        stage('Build') {
            steps {
                sh 'mvn clean package -DskipTests'
            }
        }

        stage('Test') {
            steps {
                sh 'mvn test'
            }
        }

        stage('Docker Build') {
            agent any   // Back to Jenkins agent for Docker commands
            steps {
                sh 'docker build -t shopping-cart:${BUILD_NUMBER} .'
                sh 'docker tag shopping-cart:${BUILD_NUMBER} shopping-cart:latest'
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    docker stop shopping-cart 2>/dev/null || true
                    docker rm shopping-cart 2>/dev/null || true
                    docker run -d --name shopping-cart -p 3000:3000 -v /app/data:/app/data --restart unless-stopped shopping-cart:${BUILD_NUMBER}
                '''
            }
        }
    }
}
```

---

## 15. Scenario-Based Q&A

---

🔍 **Scenario 1:** You ran `docker run nginx` and the NGINX container started, but you can't access it from your browser at `http://VM_IP`. What's wrong?

✅ **Answer:** Two possible issues. First — you didn't add port mapping. The container listens on port 80 **internally**, but without `-p 8080:80`, no external port is exposed. Fix: `docker run -d -p 8080:80 nginx`. Second — even with port mapping, your cloud VM's firewall may block port 8080. On GCP, add a firewall rule allowing TCP 8080. On AWS, add an inbound rule in the Security Group. Both must be done for external browser access to work.

---

🔍 **Scenario 2:** Your Jenkins container was running perfectly for 3 weeks. You deleted it and recreated it, and now all your jobs, plugins, and configurations are gone. How do you prevent this in the future?

✅ **Answer:** You stored Jenkins data inside the container — when the container was deleted, all data was lost. The fix going forward: always run Jenkins with a volume mount: `docker run -d --name jenkins -p 8080:8080 -v /home/ubuntu/jenkins-data:/var/jenkins_home jenkins/jenkins`. The `/var/jenkins_home` directory contains all Jenkins data. With this volume, you can delete and recreate the container as many times as you want — jobs, plugins, and configurations are stored in `/home/ubuntu/jenkins-data` on the host and persist forever.

---

🔍 **Scenario 3:** You have 5 different web applications and want to run them all on the same Ubuntu VM. How do you do this without port conflicts?

✅ **Answer:** Run each application in its own container with different host port mappings — all can use the same internal port (e.g., 80 or 3000) without conflict:
```bash
docker run -d -p 8081:80 --name app1 my-app1
docker run -d -p 8082:80 --name app2 my-app2
docker run -d -p 8083:3000 --name app3 my-node-app
docker run -d -p 8084:8080 --name app4 my-spring-app
docker run -d -p 8085:5000 --name app5 my-python-app
```
Each container is isolated, each uses its own network namespace, and the host port determines which app you reach externally.

---

🔍 **Scenario 4:** A container is consuming 90% CPU and slowing down your entire server. How do you identify and fix this?

✅ **Answer:** Run `docker stats` to identify the culprit — it shows real-time CPU/memory for all containers. Once identified: (1) If it's a bug, restart the container: `docker restart container-name`; (2) If it's expected high load, add resource limits to the container: `docker update --cpus="1.0" --memory="512m" container-name`; (3) If it's a runaway process, kill and recreate with limits: `docker rm -f container-name && docker run --cpus="0.5" --memory="256m" ...`; (4) Long-term: move that container to a dedicated slave agent so it doesn't impact other builds.

---

🔍 **Scenario 5:** You need to debug why a Node.js container isn't starting correctly. It starts and immediately exits. How do you investigate?

✅ **Answer:** The container exited because the process inside crashed or errored. Check the logs: `docker logs container-name`. The exit code tells you what happened: `docker inspect container-name --format='{{.State.ExitCode}}'`. Common causes visible in logs: missing environment variable, wrong file path, port already in use, startup script error. If you need to explore the container interactively, run a shell using the same image: `docker run -it --rm node:18 /bin/bash` and manually run your startup command to see the error in real time.

---

🔍 **Scenario 6:** Your team wants to test a deployment under load. They want to create 50 identical containers to simulate concurrent requests to a service. How do you do this efficiently?

✅ **Answer:** Use a bash loop:
```bash
for i in $(seq 1 50); do
  docker run -d --name load-test-$i -e TARGET_URL=http://your-service:3000 load-test-image
done
echo "Total containers: $(docker ps | grep load-test | wc -l)"
```
After testing, clean up with: `docker rm -f $(docker ps -aq --filter "name=load-test")`. This creates and removes all 50 containers in seconds — far faster than creating VMs or manually configuring individual processes.

---

## 16. Interview Q&A

---

**Q1. What is the difference between `docker run` and `docker start`?**

**A:** `docker run` creates a **brand new container** from an image and immediately starts it. Every `docker run` call creates a new container instance. `docker start` restarts a **previously stopped container** that already exists — it doesn't create anything new. The distinction matters because: `docker run nginx` always gives you a fresh container with a fresh filesystem state. `docker start my-nginx` resumes an existing container exactly where it stopped, preserving any changes made to its filesystem while it was running (though those changes are lost on `docker rm`).

---

**Q2. Explain port mapping in Docker. What does `-p 8080:80` mean?**

**A:** Docker containers run in isolated network namespaces — by default, nothing outside the container can reach them. Port mapping (`-p` flag) creates a rule that forwards traffic from a host port to a container port. `-p 8080:80` means: "Any traffic arriving at port 8080 on the host machine should be forwarded to port 80 inside the container." The format is always `HOST_PORT:CONTAINER_PORT`. You can map multiple ports (`-p 80:80 -p 443:443`) and run multiple containers on the same host using different host ports even if they all listen on the same internal port. Without port mapping, containers are completely network-isolated — which is secure by default.

---

**Q3. What is the purpose of Docker volumes and why shouldn't you store data inside a container?**

**A:** Docker containers have ephemeral (temporary) filesystems — when a container is removed with `docker rm`, everything written to its filesystem is permanently deleted. Volumes solve this by storing data on the host filesystem (or network storage) outside the container. The container mounts the volume and reads/writes to it, but the data's lifecycle is independent of the container. You should never store important data inside a container because: (1) `docker rm` deletes it permanently, (2) you can't upgrade to a new container version without losing data, (3) multiple containers can't share the same data. The best practice: containers are stateless, volumes are stateful.

---

**Q4. What is the difference between `-d` and `-it` flags in `docker run`?**

**A:** `-d` (detached mode) runs the container in the background — your terminal is immediately free and you don't see container output. Used for long-running services like web servers, databases, and Jenkins. `-it` (interactive + TTY) connects your terminal to the container's shell — you can type commands inside the container and see output in real time. `-i` keeps stdin open; `-t` allocates a virtual terminal. Used for debugging, exploring containers, or running interactive programs. They serve completely opposite purposes: `-d` is for production services you set and forget; `-it` is for hands-on container exploration.

---

**Q5. What is `docker exec` used for and how is it different from `docker run -it`?**

**A:** `docker exec` runs a command inside an **already running** container. `docker exec -it my-container /bin/bash` opens a shell in a container that's currently running something else (like NGINX). `docker run -it` creates a **new container** and starts it with an interactive shell. The key difference: `exec` enters an existing container without disrupting what's running in it; `run -it` always creates fresh. `exec` is used for debugging production containers (inspect logs, check files, run diagnostic commands), while `run -it` is used for exploring images or testing new containers.

---

**Q6. How would you monitor resource usage of Docker containers?**

**A:** `docker stats` shows real-time CPU percentage, memory usage (current/limit), memory percentage, network I/O, and block I/O for all running containers, updating every second. For a one-time snapshot: `docker stats --no-stream`. For custom formatting: `docker stats --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"`. If a container is consuming too much, set limits with `docker run --cpus="1.0" --memory="512m"` or update existing: `docker update --cpus="0.5" container-name`. For production monitoring, `docker stats` is good for quick checks — production environments use tools like Prometheus + Grafana, Datadog, or AWS CloudWatch for persistent metrics.

---

**Q7. What is the difference between `docker stop` and `docker kill`?**

**A:** `docker stop` sends the **SIGTERM** signal to the main process inside the container — this is a polite request to shut down. The container has 10 seconds (configurable with `--time`) to clean up (finish writes, close connections, flush buffers) before Docker sends SIGKILL to force-terminate it. `docker kill` sends **SIGKILL** immediately — no warning, no cleanup time. Use `docker stop` as the default — it allows graceful shutdown and prevents data corruption. Use `docker kill` only when `docker stop` doesn't work (process ignoring SIGTERM, hung container). In a Jenkins pipeline, always `docker stop` before `docker rm` for safety.

---

**Q8. Why is NGINX preferred over Apache for modern containerized deployments?**

**A:** NGINX handles concurrency fundamentally differently. Apache uses a process/thread per connection model — each connection spawns a new thread, consuming significant memory. Under high traffic (thousands of concurrent connections), Apache's memory usage explodes. NGINX uses an **event-driven, non-blocking** model — a small number of worker processes handle thousands of connections efficiently using an event loop. This means: NGINX uses dramatically less memory under load, has more predictable performance, and excels at serving static files and acting as a reverse proxy. In Docker, where memory efficiency matters and containers should be lightweight, NGINX is the standard choice. Apache and Tomcat are considered legacy for new projects.

---

**Q9. How do you create and manage multiple containers efficiently using bash?**

**A:** Use bash loops and Docker's quiet mode (`-q`): Create multiple containers: `for i in {1..10}; do docker run -d --name app-$i -p $((3000+i)):3000 my-app; done`. Stop all: `docker stop $(docker ps -q)`. Remove all: `docker rm $(docker ps -aq)`. Force remove all: `docker rm -f $(docker ps -aq)`. Count containers: `docker ps -a | wc -l`. Filter by name: `docker rm -f $(docker ps -aq --filter "name=app-")`. `docker ps -q` (quiet mode) returns only container IDs — these are passed to stop/rm via command substitution `$()`. This pattern is essential for test environments, CI cleanup scripts, and development environment management.

---

← Previous: [`32_Introduction_to_Docker_Containers_Images_&_Architecture`](32_Introduction_to_Docker_Containers_Images_&_Architecture) | Next: [`34_Dockerfiles_Custom_Images_Docker_Hub_&_Troubleshooting.md`](34_Dockerfiles_Custom_Images_Docker_Hub_&_Troubleshooting.md) →