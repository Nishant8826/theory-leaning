# 32 – Introduction to Docker: Containers, Images & Architecture

---

## Table of Contents

1. [The Problem Docker Solves – VMs vs Containers](#1-the-problem-docker-solves--vms-vs-containers)
2. [What is Docker?](#2-what-is-docker)
3. [Docker Architecture – The Three Parts](#3-docker-architecture--the-three-parts)
4. [Docker Hub – The Image Registry](#4-docker-hub--the-image-registry)
5. [The Docker Workflow – From Code to Container](#5-the-docker-workflow--from-code-to-container)
6. [Dockerfile – The Blueprint](#6-dockerfile--the-blueprint)
7. [Core Docker Commands](#7-core-docker-commands)
8. [Docker Installation on Ubuntu (GCP)](#8-docker-installation-on-ubuntu-gcp)
9. [Container Lifecycle – Why Containers Exit](#9-container-lifecycle--why-containers-exit)
10. [Image Sizes & Alpine Linux](#10-image-sizes--alpine-linux)
11. [Tech Stack Mapping](#11-tech-stack-mapping)
12. [Visual Diagrams](#12-visual-diagrams)
13. [Code & Practical Examples](#13-code--practical-examples)
14. [Scenario-Based Q&A](#14-scenario-based-qa)
15. [Interview Q&A](#15-interview-qa)

---

## 1. The Problem Docker Solves – VMs vs Containers

### What
Before Docker, the standard way to package and run applications was using **Virtual Machines (VMs)**. Docker replaces VMs for most use cases with something far lighter and faster — **containers**.

### The Classic Problem: "It Works on My Machine"

Imagine this scenario:
- Developer builds an app on their MacBook with Java 17, Maven 3.8, and specific environment variables
- The app is uploaded to a Linux production server with Java 11 and different configs
- The app breaks — "But it worked on my machine!"

This problem has plagued software development for decades. Docker eliminates it entirely.

### VMs vs Containers – The Core Difference

#### Virtual Machines
A VM runs an **entire operating system** on top of your physical hardware through a piece of software called a **Hypervisor** (VMware, VirtualBox, KVM).

```
Physical Hardware
      │
      ▼
Hypervisor (VMware / KVM)
      │
      ├── VM 1: Full OS (Ubuntu) + App A    ← 2.5GB+ each
      ├── VM 2: Full OS (Windows) + App B
      └── VM 3: Full OS (CentOS) + App C
```

#### Containers
A container shares the **host OS kernel** — it doesn't need its own OS. It only packages the application and its dependencies.

```
Physical Hardware
      │
      ▼
Host OS (Linux)
      │
      ▼
Docker Engine
      │
      ├── Container 1: App A + libs    ← ~100MB
      ├── Container 2: App B + libs    ← ~50MB
      └── Container 3: App C + libs    ← ~13MB
```

### Comparison Table

| Feature | Virtual Machine | Docker Container |
|---------|----------------|-----------------|
| **Size** | 2.5GB–20GB per VM | 13MB–500MB per image |
| **Startup time** | Minutes | Milliseconds |
| **OS overhead** | Full OS for each VM | Shares host kernel |
| **Portability** | Hard to move between environments | `docker push` / `docker pull` — instant |
| **Resource usage** | High (RAM, CPU for OS) | Minimal |
| **Isolation** | Strong (hardware-level) | Good (process-level) |
| **Best for** | Running different OS types | App packaging & deployment |
| **Collaboration** | Share 2.5GB+ OVF files | Share 100MB image from Docker Hub |

### Impact

| Without Docker (VMs) | With Docker |
|---------------------|------------|
| "It works on my machine" — broken in prod | Same container, same behavior everywhere |
| 2.5GB+ files to share environments | 119MB Ubuntu image from Hub |
| Minutes to spin up a new environment | Seconds to start a container |
| Dev, QA, Prod use different setups | Identical container across all environments |
| Microservices need separate VMs | Many containers on one host |

---

## 2. What is Docker?

### What
**Docker** is an open-source **containerization platform** that packages applications and all their dependencies into a standardized unit called a **container**. That container runs identically on any machine that has Docker installed — regardless of operating system, cloud provider, or hardware.

> 💡 **Analogy:** Think of Docker containers like **shipping containers** on cargo ships. Before standardized shipping containers, loading different cargo onto ships was slow, custom, and error-prone. Standardized containers can be loaded onto any ship, truck, or train — the contents don't change, only the transport. Docker does the same for software.

### Why Docker Exists
1. **Environment consistency:** Same container in dev, test, and production
2. **Microservices:** Each service runs in its own isolated container
3. **Speed:** Containers start in milliseconds
4. **Resource efficiency:** Run 10 containers where 1 VM would max out resources
5. **Developer collaboration:** Share exact environments via Docker Hub
6. **CI/CD integration:** Jenkins can build Docker images and deploy containers automatically

### Docker's Role in the DevOps World
Docker is the **packaging format** of modern DevOps:
- Code is written → packaged into a Docker image → deployed as a container
- Jenkins builds the image → pushes to Docker Hub/ECR → Kubernetes runs it in production
- Every major cloud (AWS, GCP, Azure) has first-class Docker support

---

## 3. Docker Architecture – The Three Parts

### What
Docker has three main components that work together. Understanding all three is essential for troubleshooting and interview questions.

---

### Part 1: Docker Client
- **What:** The CLI (command line interface) where YOU type Docker commands
- **How it works:** Accepts your commands (`docker run`, `docker build`) and sends them to the Docker Daemon via REST API
- **Where it runs:** Your local machine, or any server where you type Docker commands

```bash
# You type this on the Docker Client:
docker run ubuntu
# The client sends this instruction to the Daemon
```

---

### Part 2: Docker Daemon (`dockerd`)
- **What:** A background service (daemon process) running on your machine that does all the actual work
- **What it manages:** Images, containers, networks, volumes
- **How it works:** Listens for commands from the client, pulls images, creates/starts/stops containers

> 💡 **Analogy:** The Docker Client is like a waiter taking your order. The Docker Daemon is the kitchen that actually prepares the food.

Check if daemon is running:
```bash
sudo systemctl status docker
# Active: active (running) ✅
```

---

### Part 3: Docker Registry (Docker Hub)
- **What:** A cloud-based storage system for Docker images — like GitHub but for containers
- **Docker Hub:** The default public registry with 40+ million images
- **What's there:** Official images for Ubuntu, Nginx, MySQL, Node.js, Python, Redis, and millions more
- **Private registries:** AWS ECR, GCP Artifact Registry, self-hosted Harbor

```
docker pull ubuntu      → Downloads from Docker Hub
docker push myapp:v1    → Uploads to Docker Hub (requires login)
```

### How the Three Parts Work Together

```
YOU (Docker Client)
  │
  │ Type: docker run ubuntu
  │
  ▼
Docker Daemon
  │
  │ "Do I have ubuntu image locally?"
  │
  ├── YES → Create container from local image
  │
  └── NO → Pull from Docker Hub
              │
              ▼
          Docker Hub (Registry)
              │ ubuntu:latest image downloaded
              ▼
          Docker Daemon
              │ Creates container
              ▼
          Running Container ✅
```

---

## 4. Docker Hub – The Image Registry

### What
**Docker Hub** (hub.docker.com) is the world's largest container image registry — a central place to store, share, and discover Docker images. Think of it as "npm for containers" or "GitHub for Docker images."

### Why
- 40+ million images available for free
- Official images maintained by vendors (Ubuntu, MySQL, Nginx, Node.js)
- Community images for every tool imaginable
- Private repositories for company images (paid plans)

### Image Types

| Type | Who maintains it | Trust level | Example |
|------|-----------------|-------------|---------|
| **Official** | Docker Inc. + vendor | ⭐ Highest | `ubuntu`, `nginx`, `mysql` |
| **Verified Publisher** | Verified companies | ✅ High | `bitnami/wordpress` |
| **Community** | Individuals | ⚠️ Varies | `username/my-app` |

### Image Naming Convention

```
[registry/][username/]image-name[:tag]

Examples:
  ubuntu                       → Official ubuntu, latest tag
  ubuntu:22.04                 → Official ubuntu, version 22.04
  nginx:alpine                 → Nginx built on Alpine Linux
  yourname/shopping-cart:v1.2  → Your custom image, version 1.2
  123456.dkr.ecr.us-east-1.amazonaws.com/myapp:latest  → AWS ECR
```

### Docker Hub Commands

```bash
# Login to Docker Hub
docker login
# Enter: username and password

# Search for an image
docker search ubuntu

# Pull (download) an image
docker pull ubuntu
docker pull ubuntu:22.04
docker pull alpine:latest

# Push (upload) your image
docker push yourname/myapp:v1

# List local images
docker images
```

---

## 5. The Docker Workflow – From Code to Container

### What
The Docker workflow is a pipeline that takes your application code and transforms it into a running container. It has five stages, each building on the last.

### The Five-Stage Workflow

```
Stage 1: DOCKERFILE
   Write instructions (blueprint)
         │
         ▼
Stage 2: BUILD
   docker build → Creates IMAGE
         │
         ▼
Stage 3: PUSH
   docker push → Saves to REGISTRY (Docker Hub / ECR)
         │
         ▼
Stage 4: PULL
   docker pull → Downloads on any machine
         │
         ▼
Stage 5: RUN
   docker run → Creates running CONTAINER
```

---

### Stage 1: Dockerfile
The recipe. A text file with instructions for building an image. Covered in detail in Section 6.

### Stage 2: Build
```bash
docker build -t myapp:v1 .
# -t = tag/name the image
# . = build context (current directory, where Dockerfile is)
```

This reads the Dockerfile, executes each instruction, and produces an image.

### Stage 3: Push
```bash
docker login
docker push yourname/myapp:v1
# Image stored on Docker Hub (or ECR, GCR, etc.)
```

### Stage 4: Pull
```bash
# On any machine with Docker:
docker pull yourname/myapp:v1
# Downloads the image
```

### Stage 5: Run
```bash
docker run yourname/myapp:v1
# Creates a container from the image and runs it
```

---

## 6. Dockerfile – The Blueprint

### What
A **Dockerfile** is a plain text file containing a series of instructions that tell Docker how to build an image. Every line in a Dockerfile creates a new **layer** in the image.

> 💡 **Analogy:** A Dockerfile is like a recipe card. The recipe tells you: what base ingredients to start with (FROM), what to add (RUN/ADD/COPY), what temperature and time (CMD/ENTRYPOINT), and how to serve it (EXPOSE/CMD).

### Dockerfile Keywords – Every One Explained

| Keyword | Purpose | Example |
|---------|---------|---------|
| `FROM` | Base image to start from (required, always first) | `FROM ubuntu:22.04` |
| `RUN` | Execute commands during BUILD time | `RUN apt-get install -y java` |
| `CMD` | Default command when container STARTS (can be overridden) | `CMD ["java", "-jar", "app.jar"]` |
| `ENTRYPOINT` | Fixed command at startup (not easily overridden) | `ENTRYPOINT ["java", "-jar"]` |
| `ADD` | Copy files + can unpack .tar, fetch from URL | `ADD app.tar.gz /app/` |
| `COPY` | Copy files from host to image (simpler than ADD) | `COPY target/app.jar /app/app.jar` |
| `WORKDIR` | Set working directory inside the container | `WORKDIR /app` |
| `EXPOSE` | Document which port the app listens on | `EXPOSE 8080` |
| `ENV` | Set environment variables inside the container | `ENV JAVA_HOME=/usr/lib/jvm/java-21` |
| `MAINTAINER` | (Deprecated) Who maintains this image | `MAINTAINER john@company.com` |
| `LABEL` | Add metadata to the image | `LABEL version="1.0"` |
| `VOLUME` | Create a mount point for persistent data | `VOLUME ["/data"]` |
| `ARG` | Build-time variable (not in final image) | `ARG VERSION=1.0` |
| `USER` | Set which user runs subsequent commands | `USER appuser` |

### RUN vs CMD vs ENTRYPOINT – The Critical Distinction

```
RUN   → Executes during IMAGE BUILD (adds a layer to the image)
CMD   → Executes when CONTAINER STARTS (default command, replaceable)
ENTRYPOINT → Executes when CONTAINER STARTS (fixed command, not easily replaced)
```

```dockerfile
FROM ubuntu:22.04
RUN apt-get update && apt-get install -y curl   # ← BUILD time
CMD ["echo", "Hello from container"]            # ← RUN time (replaceable)
```

---

## 7. Core Docker Commands

### Image Commands

```bash
# Download an image from Docker Hub
docker pull ubuntu
docker pull ubuntu:22.04
docker pull alpine:latest

# List all local images
docker images
# Shows: REPOSITORY, TAG, IMAGE ID, CREATED, SIZE

# Remove an image
docker rmi ubuntu
docker rmi ubuntu:22.04

# Build an image from Dockerfile
docker build -t myapp:v1 .
docker build -t myapp:v1 -f Dockerfile.prod .  # specify Dockerfile name

# Tag an image
docker tag myapp:v1 yourname/myapp:v1

# Inspect image details
docker inspect ubuntu
```

---

### Container Commands

```bash
# Run a container (foreground, exits when done)
docker run ubuntu

# Run interactively with a terminal
docker run -it ubuntu bash
# -i = interactive, -t = terminal
# Now you're INSIDE the container → type commands → exit to leave

# Run in background (detached mode)
docker run -d nginx
# -d = detached (runs in background)

# Run with port mapping
docker run -d -p 8080:80 nginx
# -p host_port:container_port
# Access nginx at http://localhost:8080

# Run with a custom name
docker run --name my-ubuntu ubuntu

# Run and remove container when it exits
docker run --rm ubuntu echo "hello"

# Run hello-world (simplest test)
docker run hello-world
```

---

### Viewing Containers

```bash
# Show RUNNING containers only
docker ps

# Show ALL containers (running + stopped)
docker ps -a
# STATUS: Exited(0) = completed successfully
#         Up 2 hours = currently running

# Show container logs
docker logs container_name
docker logs -f container_name   # -f = follow (live logs)

# Get container details
docker inspect container_name
```

---

### Managing Running Containers

```bash
# Stop a running container (graceful)
docker stop container_name

# Kill a running container (immediate)
docker kill container_name

# Start a stopped container
docker start container_name

# Restart a container
docker restart container_name

# Execute a command in a running container
docker exec -it container_name bash
# Opens a shell INSIDE a running container

# Remove a stopped container
docker rm container_name

# Remove all stopped containers
docker container prune
```

---

### Quick Reference Table

| Command | What it does |
|---------|-------------|
| `docker pull ubuntu` | Download image from Hub |
| `docker images` | List local images |
| `docker run ubuntu` | Create + run container |
| `docker run -it ubuntu bash` | Interactive shell in container |
| `docker run -d -p 8080:80 nginx` | Background + port mapping |
| `docker ps` | Show running containers |
| `docker ps -a` | Show all containers |
| `docker stop name` | Stop container gracefully |
| `docker rm name` | Delete stopped container |
| `docker rmi image` | Delete image |
| `docker logs name` | View container logs |
| `docker exec -it name bash` | Shell into running container |

---

## 8. Docker Installation on Ubuntu (GCP)

### VM Setup
```
Cloud: Google Cloud Platform
OS: Ubuntu 24.04 LTS
Storage: 30 GB
CPU: 2 vCPUs
RAM: 4 GB
```

### Installation Method 1: Official Script (Used in Class — Easiest)

```bash
# Download and run the official Docker installation script
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Verify installation
docker --version
# Docker version 26.x.x

# Test with hello-world
sudo docker run hello-world
```

### Installation Method 2: apt (Manual — Recommended for Production)

```bash
# Step 1: Update packages
sudo apt-get update

# Step 2: Install prerequisites
sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Step 3: Add Docker's official GPG key
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
    sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Step 4: Set up the repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Step 5: Install Docker Engine
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io

# Step 6: Start and enable Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Step 7: Add current user to docker group (avoid sudo every time)
sudo usermod -aG docker $USER
newgrp docker   # Apply group change without logout

# Step 8: Verify
docker run hello-world
```

### After Installation — Check Everything Works

```bash
# Check Docker daemon is running
sudo systemctl status docker

# Check version
docker --version
docker info   # Detailed info about Docker installation

# Run hello-world
docker run hello-world

# Pull and check image sizes from class
docker pull ubuntu      # 119 MB
docker pull centos      # 301 MB
docker pull alpine      # 13.1 MB

# List downloaded images
docker images
```

---

## 9. Container Lifecycle – Why Containers Exit

### What
A container is not meant to run forever by default. It runs a process, and **when that process finishes, the container exits**. This is a feature, not a bug.

> 💡 **Analogy:** A container is like a function call, not a server. When you call a function, it runs, returns a value, and ends. You don't expect it to keep running after it's done.

### The Container Lifecycle

```
docker run → Container Created
                  │
                  ▼
             Process Starts
                  │
                  ▼
         Process completes / exits
                  │
                  ▼
           Container stops
           STATUS: Exited(0)    ← 0 = success
```

### Why `docker run ubuntu` Exits Immediately

```bash
docker run ubuntu
# Container starts → no process to run → immediately exits
# docker ps    → nothing (container exited)
# docker ps -a → shows Exited(0)
```

Ubuntu image has no default process. You need to give it something to do:

```bash
docker run ubuntu echo "Hello"
# Runs "echo Hello" → prints → exits immediately

docker run -it ubuntu bash
# Runs bash (interactive shell) → stays running while you're in it
# Type "exit" → shell exits → container exits
```

### Containers That Stay Running

Containers with **long-running processes** stay alive:

```bash
docker run -d nginx
# nginx is a web server → runs continuously → container stays up
# docker ps → shows running

docker run -d -p 8080:8080 myapp:v1
# App server listening on 8080 → runs continuously
```

### Exit Codes

| Exit Code | Meaning |
|-----------|---------|
| `0` | Process completed successfully |
| `1` | General error |
| `137` | Container was killed (OOM or docker kill) |
| `143` | Container received SIGTERM (docker stop) |

### Checking Exited Containers

```bash
docker ps -a
# CONTAINER ID   IMAGE     COMMAND       STATUS
# abc123         ubuntu    "bash"        Exited (0) 5 minutes ago
# def456         nginx     "nginx -g .." Up 2 hours
```

---

## 10. Image Sizes & Alpine Linux

### Image Sizes from Class

| Image | Size | What it is |
|-------|------|-----------|
| `alpine` | 13.1 MB | Minimal Linux, perfect for production containers |
| `ubuntu` | 119 MB | Full Ubuntu — familiar but larger |
| `centos` | 301 MB | CentOS Linux — even larger |
| Ubuntu VM | 2.5 GB+ | Full virtual machine image |

### What is Alpine Linux?

**Alpine Linux** is a security-focused, minimal Linux distribution designed specifically for containers and embedded systems. Its entire OS is ~5MB, and Docker image is ~13MB.

### Why Alpine for Production Containers?

| Reason | Detail |
|--------|--------|
| **Tiny size** | 13MB vs 119MB Ubuntu → faster pulls, less storage |
| **Security** | Fewer packages = fewer attack surfaces |
| **Speed** | Faster to download, push, pull in CI/CD |
| **Cost** | Less storage on registry and servers |
| **Production ready** | Used by official images (nginx:alpine, python:alpine) |

### Alpine-based Official Images

```bash
docker pull nginx:alpine          # 41MB vs nginx:latest 142MB
docker pull python:3.12-alpine    # 50MB vs python:3.12 1.01GB
docker pull node:20-alpine        # 182MB vs node:20 1.1GB
```

### Alpine Package Manager

Alpine uses `apk` instead of `apt`:

```dockerfile
# Ubuntu/Debian style:
RUN apt-get update && apt-get install -y curl

# Alpine style:
RUN apk update && apk add --no-cache curl
```

---

## 11. Tech Stack Mapping

### Docker in the DevOps Pipeline

```
Developer writes code (VS Code)
         │
         ▼
Git push to GitHub
         │
         ▼
Jenkins Pipeline:
  Stage 1: Clone from GitHub
  Stage 2: mvn clean package / npm build
  Stage 3: docker build -t myapp:v1 .
  Stage 4: docker push yourname/myapp:v1
         │
         ▼
Docker Hub / AWS ECR
(Image stored and versioned)
         │
         ▼
Production Environment:
  Kubernetes: kubectl apply deployment.yaml
  → Pulls image from ECR
  → Runs containers at scale
         │
         ▼
Users access the application
```

### Docker with Different Tech Stacks

| Application | Base Image | Key Considerations |
|------------|-----------|-------------------|
| **Node.js API** | `node:20-alpine` | npm install in Dockerfile, expose port 3000 |
| **Spring Boot (Java)** | `openjdk:21-alpine` | Copy JAR, run with java -jar |
| **React/Next.js** | `node:20-alpine` + `nginx:alpine` | Multi-stage build |
| **Python** | `python:3.12-alpine` | pip install -r requirements.txt |
| **MySQL** | `mysql:8.0` | Volume for data persistence |
| **Redis** | `redis:alpine` | Volume for data persistence |
| **Nginx** | `nginx:alpine` | Copy config and static files |

### Docker in AWS Ecosystem

| AWS Service | Docker Role |
|------------|------------|
| **ECS (Elastic Container Service)** | Run Docker containers on AWS (managed) |
| **EKS (Elastic Kubernetes Service)** | Run Docker containers with Kubernetes |
| **ECR (Elastic Container Registry)** | Private Docker Hub on AWS |
| **Fargate** | Serverless containers — no EC2 management |
| **App Runner** | Fully managed container deployment |
| **Lambda** | Can package functions as Docker images |

---

## 12. Visual Diagrams

### Diagram 1: VM vs Container Architecture

```
VIRTUAL MACHINES                    DOCKER CONTAINERS
────────────────                    ─────────────────

Physical Server                     Physical Server
      │                                   │
      ▼                                   ▼
Hypervisor (VMware/KVM)             Host OS (Linux)
      │                                   │
      ▼                                   ▼
┌──────────┬──────────┬──────────┐   Docker Engine
│  VM 1    │  VM 2    │  VM 3    │        │
│          │          │          │   ┌────┴────┬────────┬────────┐
│ Full OS  │ Full OS  │ Full OS  │   │ Cont.1  │ Cont.2 │ Cont.3 │
│ 2.5GB+   │ 2.5GB+   │ 2.5GB+   │   │         │        │        │
│ App A    │ App B    │ App C    │   │ App A   │ App B  │ App C  │
│          │          │          │   │ libs    │ libs   │ libs   │
│ Startup: │ Startup: │ Startup: │   │ ~100MB  │ ~50MB  │ ~13MB  │
│ Minutes  │ Minutes  │ Minutes  │   │ Start:  │ Start: │ Start: │
└──────────┴──────────┴──────────┘   │ Seconds │ Sec.   │ Sec.   │
                                     └─────────┴────────┴────────┘
```

---

### Diagram 2: Docker Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         YOUR MACHINE                            │
│                                                                 │
│  ┌──────────────────────┐         ┌────────────────────────┐   │
│  │    DOCKER CLIENT     │         │     DOCKER DAEMON      │   │
│  │                      │         │      (dockerd)         │   │
│  │  $ docker run nginx  │─────────►                        │   │
│  │  $ docker build .    │  REST   │  Manages:              │   │
│  │  $ docker push img   │   API   │  • Images              │   │
│  │  $ docker ps         │         │  • Containers          │   │
│  │                      │         │  • Networks            │   │
│  └──────────────────────┘         │  • Volumes             │   │
│                                   └──────────┬─────────────┘   │
└──────────────────────────────────────────────┼─────────────────┘
                                               │ Pull/Push images
                                               ▼
                              ┌────────────────────────────────┐
                              │         DOCKER HUB             │
                              │       (Registry)               │
                              │                                │
                              │  ubuntu:22.04  (119MB)         │
                              │  nginx:alpine  (41MB)          │
                              │  node:20-alpine (182MB)        │
                              │  40+ million images            │
                              └────────────────────────────────┘
```

---

### Diagram 3: Docker Workflow

```
Your Code + Dockerfile
         │
         │ docker build -t myapp:v1 .
         ▼
    ┌─────────┐
    │  IMAGE  │ ← Immutable snapshot (like a class definition)
    │ myapp:v1│
    └────┬────┘
         │
         ├──── docker push ────────────► Docker Hub / ECR
         │                               (stored, shared, versioned)
         │
         │ docker run myapp:v1
         ▼
    ┌─────────────┐
    │  CONTAINER  │ ← Running instance (like an object from a class)
    │  myapp:v1   │
    │  Port: 8080 │
    │  Status: Up │
    └─────────────┘
```

---

### Diagram 4: Dockerfile Layers

```
Dockerfile:                    Image Layers (cached):

FROM ubuntu:22.04    ──────►   Layer 1: ubuntu base (119MB)
RUN apt-get update   ──────►   Layer 2: package index
RUN apt-get install java ──►   Layer 3: Java installation
COPY app.jar /app/   ──────►   Layer 4: your JAR file
EXPOSE 8080          ──────►   Layer 5: metadata
CMD ["java","-jar",  ──────►   Layer 6: default command
     "/app/app.jar"]

Each layer is CACHED — rebuilding only re-runs changed layers
→ Faster builds on subsequent runs
```

---

### Diagram 5: Container Lifecycle

```
docker run ubuntu echo "hello"

   Created           Running           Exited
  ──────────        ─────────         ──────────
  Container    →    "hello"     →     Status:
  initialized       printed           Exited(0)
                                           │
                                    docker ps -a
                                    (still visible)
                                           │
                                    docker rm abc123
                                    (permanently deleted)

docker run -d nginx

   Created           Running           (stays running)
  ──────────        ─────────         ──────────────────
  Container    →    nginx web   →     Status: Up 2 hours
  initialized       server            docker ps (visible)
                    listening         
                    on port 80
```

---

### Diagram 6: Image Size Comparison

```
Image Sizes (to scale):

alpine    ██ 13.1 MB
ubuntu    ████████████████████████████████████████████ 119 MB
centos    ████████████████████████████████████████████████████████████████████████████████████████████████████████ 301 MB
Ubuntu VM ████████████████████... (2,500 MB+) would extend far off the page

Smaller = Faster pull/push = Less storage = Smaller attack surface
```

---

### Diagram 7: Port Mapping

```
docker run -d -p 8080:80 nginx

HOST MACHINE                    CONTAINER
─────────────                   ──────────
                                
  Port 8080  ──────────────────► Port 80 (nginx listens here)
  (your port)    port mapping    (container's internal port)
  
Browser: http://localhost:8080
→ Traffic forwarded to container port 80
→ nginx responds
→ You see the nginx welcome page
```

---

## 13. Code & Practical Examples

### Example 1: Dockerfile for a Java Spring Boot App

```dockerfile
# Stage: Base image
FROM openjdk:21-slim

# Maintainer info
LABEL maintainer="yourname@company.com"
LABEL version="1.0"

# Set working directory inside container
WORKDIR /app

# Copy the JAR file from build output to container
COPY target/shopping-cart.jar /app/shopping-cart.jar

# Document the port this app uses
EXPOSE 8080

# Command to run when container starts
CMD ["java", "-jar", "/app/shopping-cart.jar"]
```

Build and run:
```bash
# Build the image
docker build -t shopping-cart:v1 .

# Run it
docker run -d -p 8080:8080 --name my-shop shopping-cart:v1

# Check it's running
docker ps

# View logs
docker logs my-shop

# Access the app
curl http://localhost:8080/api/products
```

---

### Example 2: Dockerfile for a Node.js API

```dockerfile
# Use small Alpine-based Node.js image
FROM node:20-alpine

# Create app directory
WORKDIR /app

# Copy package files first (for layer caching)
COPY package.json package-lock.json ./

# Install dependencies
RUN npm ci --only=production

# Copy application code
COPY src/ ./src/

# Expose API port
EXPOSE 3000

# Start the API
CMD ["node", "src/index.js"]
```

---

### Example 3: Multi-Stage Dockerfile for React/Next.js

```dockerfile
# Stage 1: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Serve with Nginx (tiny production image)
FROM nginx:alpine AS production
COPY --from=builder /app/out /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

Result: Instead of 1.1GB Node.js image, final image is ~40MB nginx:alpine.

---

### Example 4: Jenkins Pipeline with Docker Build & Push

```groovy
pipeline {
    agent any

    environment {
        DOCKER_HUB_CREDS = credentials('dockerhub-credentials')
        IMAGE_NAME       = 'yourname/shopping-cart'
        IMAGE_TAG        = "${env.BUILD_NUMBER}"
    }

    stages {

        stage('Clone') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/yourname/shopping-cart.git'
            }
        }

        stage('Build JAR') {
            steps {
                sh 'mvn clean package -DskipTests'
            }
        }

        stage('Docker Build') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
                sh "docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest"
            }
        }

        stage('Docker Push') {
            steps {
                sh "echo ${DOCKER_HUB_CREDS_PSW} | docker login -u ${DOCKER_HUB_CREDS_USR} --password-stdin"
                sh "docker push ${IMAGE_NAME}:${IMAGE_TAG}"
                sh "docker push ${IMAGE_NAME}:latest"
            }
        }

        stage('Deploy') {
            steps {
                sh """
                    docker stop shopping-cart || true
                    docker rm shopping-cart || true
                    docker run -d \
                        --name shopping-cart \
                        -p 8080:8080 \
                        ${IMAGE_NAME}:${IMAGE_TAG}
                """
            }
        }
    }

    post {
        always {
            sh 'docker logout'
        }
        success {
            echo "✅ Image ${IMAGE_NAME}:${IMAGE_TAG} deployed successfully!"
        }
        failure {
            echo "❌ Build failed — check logs"
        }
    }
}
```

---

### Example 5: Practical Command Session (from class)

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Verify
docker --version

# Pull images
docker pull hello-world
docker pull ubuntu
docker pull centos
docker pull alpine

# Check sizes
docker images
# REPOSITORY   TAG       IMAGE ID       CREATED        SIZE
# ubuntu       latest    ba6acccedd29   6 months ago   119MB
# centos       latest    5d0da3dc9764   2 years ago    301MB
# alpine       latest    c059bfaa849c   3 months ago   13.1MB

# Run hello-world
docker run hello-world

# Run ubuntu interactively
docker run -it ubuntu bash
# Inside container:
# root@abc123:/# ls
# root@abc123:/# apt-get update
# root@abc123:/# exit

# See all containers (including exited)
docker ps -a
# CONTAINER ID   IMAGE         COMMAND    STATUS
# abc123         ubuntu        "bash"     Exited (0) 2 min ago
# def456         hello-world   "/hello"   Exited (0) 5 min ago
```

---

## 14. Scenario-Based Q&A

---

🔍 **Scenario 1:** A developer says "the application works perfectly on my laptop but crashes in production." This has been happening for months with every release. How does Docker solve this permanently?

✅ **Answer:** "Works on my machine" is an environment inconsistency problem — different OS, different Java version, different environment variables between the developer's laptop and production. Docker solves this by packaging the application AND its entire environment (OS libraries, runtime, configs) into a single container image. The developer builds the image locally, tests it, and pushes it to Docker Hub. Production pulls and runs the **exact same image** — byte for byte identical. There is no "my machine" vs "production" — there is only the container. The environment inconsistency disappears permanently.

---

🔍 **Scenario 2:** Your company runs 20 microservices. The operations team says provisioning a new VM for each service takes 3 days and the VMs sit idle 80% of the time. What do you propose?

✅ **Answer:** Move to Docker containers. Instead of one VM per service (20 VMs, mostly idle), run all 20 services as containers on a handful of powerful VMs. A single 8-CPU, 32GB RAM server can run 20+ containers simultaneously, each isolated from the others. New service deployment goes from "submit VM request, wait 3 days, configure OS" to "docker run myservice:v1" — taking seconds. For auto-scaling and orchestration of these containers, the next step is Kubernetes (covered in later sessions). Resource utilization goes from ~20% to 80%+.

---

🔍 **Scenario 3:** Your team's Jenkins pipeline takes 45 minutes because it downloads Node.js, npm packages, and build tools fresh every time. How does Docker fix this?

✅ **Answer:** Use a Docker image as the build environment in Jenkins. Instead of downloading everything fresh each run, build your pipeline inside a pre-built Docker image that already has Node.js, npm, and all build tools installed. In the Jenkinsfile: `agent { docker { image 'node:20-alpine' } }`. Jenkins pulls the image once (cached), and every subsequent build uses the cached image instantly. Additionally, Docker layer caching means `npm install` only re-runs when `package.json` changes — not on every build. Pipeline time drops from 45 minutes to under 10.

---

🔍 **Scenario 4:** You ran `docker run ubuntu` and the container exited immediately. Your colleague says Docker is broken. Is it?

✅ **Answer:** No — Docker is working correctly. This is expected behavior. The `ubuntu` image has no default process defined (`CMD` is empty or set to `bash`). When Docker starts the container, there's no process to run, so the container exits immediately with code 0 (success). To keep it running, give it a process: `docker run -it ubuntu bash` (interactive shell keeps it alive until you exit), or `docker run ubuntu sleep 3600` (sleeps for an hour). Containers are designed to run a process and exit when done — they're not VMs that sit idle.

---

🔍 **Scenario 5:** You need to choose between `ubuntu:22.04`, `debian:slim`, and `alpine:latest` as the base image for your production Node.js API. Which do you choose and why?

✅ **Answer:** Choose `node:20-alpine` (Alpine-based official Node.js image) for production. Alpine at 13.1MB vs Ubuntu at 119MB means: 10x smaller image → faster pulls in CI/CD → less storage cost on Docker Hub and AWS ECR → faster deployments → smaller attack surface (fewer packages = fewer vulnerabilities). Alpine uses `apk` instead of `apt`, so some packages have different names — but for Node.js APIs this is rarely an issue. Use Ubuntu only if you need specific Ubuntu-only packages that don't exist in Alpine's `apk` repository.

---

🔍 **Scenario 6:** Your manager asks you to explain the difference between a Docker image and a Docker container in a 30-second interview answer.

✅ **Answer:** "A Docker image is like a blueprint or a class definition — it's an immutable, read-only template that describes everything needed to run an application: the OS, runtime, libraries, and code. An image just sits there; it doesn't run or consume CPU. A container is a running instance created FROM an image — like an object created from a class. You can run multiple containers from the same image simultaneously, each isolated from the others. If the image is the recipe, the container is the meal being cooked. You build images once, run containers many times."

---

## 15. Interview Q&A

---

**Q1. What is Docker and why is it important in DevOps?**

**A:** Docker is an open-source containerization platform that packages applications and their dependencies into lightweight, portable containers. It's critical in DevOps for three reasons: (1) **Environment consistency** — the same container runs identically in dev, test, and production, eliminating "works on my machine" problems; (2) **Speed and efficiency** — containers start in milliseconds and are 10-20x smaller than VMs, enabling fast CI/CD pipelines; (3) **Microservices enablement** — different services can run in isolated containers on the same host with different runtimes. In a DevOps pipeline, Docker is typically the packaging format — Jenkins builds a Docker image, pushes it to ECR, and Kubernetes runs it in production.

---

**Q2. What is the difference between a Docker image and a Docker container?**

**A:** A Docker image is an immutable, read-only template — like a class definition or a recipe. It contains the OS layer, runtime, application code, and dependencies, but it's not running. It just exists as a stored file. A container is a running instance created from an image — like an object instantiated from a class. Containers have state, consume CPU and RAM, and have their own filesystem and network namespace. You can create many containers from the same image simultaneously, each isolated. Key commands: `docker build` creates an image; `docker run` creates a container from that image.

---

**Q3. Explain the Docker architecture — what are its three main components?**

**A:** Three components: (1) **Docker Client** — the CLI where you type commands (`docker run`, `docker build`). It communicates with the daemon via REST API. (2) **Docker Daemon (dockerd)** — a background process that does all the actual work: pulling images, creating containers, managing networks and volumes. It's the engine. (3) **Docker Registry (Docker Hub)** — a cloud storage for Docker images with 40+ million available images. When you run `docker pull ubuntu`, the client asks the daemon to download from the registry. When you run `docker push myapp:v1`, it goes the other way.

---

**Q4. What is a Dockerfile and what are the most important keywords?**

**A:** A Dockerfile is a text file with instructions for building a Docker image. Each instruction creates a layer. Most important keywords: `FROM` (base image — always required, always first), `RUN` (execute commands during build — installs packages, compiles code), `COPY`/`ADD` (bring files from host into the image), `WORKDIR` (set the working directory inside the container), `EXPOSE` (document which port the app uses), `CMD` (default command when container starts — can be overridden at `docker run`), `ENTRYPOINT` (fixed startup command — harder to override). The critical distinction: `RUN` happens at build time; `CMD`/`ENTRYPOINT` happen at container start time.

---

**Q5. Why do some Docker containers exit immediately after starting?**

**A:** A container runs until its main process exits. If there's no long-running process, the container exits immediately. `docker run ubuntu` starts the ubuntu container — but since no process is specified and ubuntu's default CMD is bash (which exits when there's no terminal), the container exits with code 0. This is correct behavior. Containers that stay running have long-running processes: `nginx` (web server), `java -jar app.jar` (Spring Boot), `node server.js` (Node.js API). To interact with ubuntu, provide a process: `docker run -it ubuntu bash` (the `-it` flags keep bash alive with an interactive terminal).

---

**Q6. What is the difference between `docker run`, `docker start`, and `docker exec`?**

**A:** Three distinct commands: `docker run` creates a BRAND NEW container from an image and starts it — this is the primary way to launch containers. `docker start` starts an EXISTING stopped container (one you've run before and stopped — it's in `docker ps -a`). `docker exec` runs a command INSIDE an already RUNNING container — most commonly `docker exec -it containername bash` to open a shell inside a running container for debugging. The pattern: `run` to create, `stop`/`start` to pause and resume, `exec` to get inside while running.

---

**Q7. Why should you use Alpine Linux as a base image for production containers?**

**A:** Alpine Linux Docker images are ~13MB vs ~119MB for Ubuntu. This matters because: (1) **Speed** — CI/CD pipelines pull images for every build; smaller = faster pipeline; (2) **Storage cost** — AWS ECR, Docker Hub charge by storage; 10x smaller = 10x cheaper; (3) **Security** — fewer installed packages means fewer vulnerabilities and a smaller attack surface; (4) **Network bandwidth** — deploying to multiple servers is faster with tiny images. The trade-off: Alpine uses `apk` not `apt`, and uses `musl libc` not `glibc`, which occasionally causes compatibility issues. For most Node.js, Python, and Go applications, Alpine works perfectly. Use `node:20-alpine`, `python:3.12-alpine`, `nginx:alpine` etc.

---

**Q8. How does Docker enable microservices architecture?**

**A:** Microservices require running multiple independent services, potentially with different languages, runtimes, and dependencies — which is impossible cleanly on a single server without containerization. Docker enables microservices by: (1) **Isolation** — each service runs in its own container with its own filesystem and dependencies (Service A uses Java 17, Service B uses Python 3.12, Service C uses Node.js 20 — no conflicts); (2) **Independent deployment** — update one service's container without touching others; (3) **Scalability** — scale individual services independently (`docker run` more instances of only the overloaded service); (4) **Consistency** — same container in dev and production. Docker is the packaging format; Kubernetes (covered next) is the orchestration layer that manages dozens of microservice containers at scale.

---

← Previous: [`31_Jenkins_Day-to-Day_Operations_Parameterized_Jobs_&_AWS_Core_Services.md`](31_Jenkins_Day-to-Day_Operations_Parameterized_Jobs_&_AWS_Core_Services.md) | Next: [`32_Introduction_to_Docker_Containers_Images_&_Architecture.md`](32_Introduction_to_Docker_Containers_Images_&_Architecture.md) →