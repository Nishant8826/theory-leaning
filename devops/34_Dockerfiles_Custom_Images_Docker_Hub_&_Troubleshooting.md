# 34 – Dockerfiles, Custom Images, Docker Hub & Troubleshooting

---

## Table of Contents

1. [What is a Dockerfile?](#1-what-is-a-dockerfile)
2. [Dockerfile Instructions – Every Command Explained](#2-dockerfile-instructions--every-command-explained)
3. [The 5-Stage Dockerfile Structure](#3-the-5-stage-dockerfile-structure)
4. [Building a Custom Docker Image](#4-building-a-custom-docker-image)
5. [Image Tagging – Naming Your Image Properly](#5-image-tagging--naming-your-image-properly)
6. [Docker Hub – Pushing & Pulling Images](#6-docker-hub--pushing--pulling-images)
7. [Creating Images from Running Containers – docker commit](#7-creating-images-from-running-containers--docker-commit)
8. [Backup & Offline Storage – docker save & docker load](#8-backup--offline-storage--docker-save--docker-load)
9. [Troubleshooting Containers – The Three Commands](#9-troubleshooting-containers--the-three-commands)
10. [Cleanup Operations](#10-cleanup-operations)
11. [Tech Stack Mapping](#11-tech-stack-mapping)
12. [Visual Diagrams](#12-visual-diagrams)
13. [Code & Practical Examples](#13-code--practical-examples)
14. [Scenario-Based Q&A](#14-scenario-based-qa)
15. [Interview Q&A](#15-interview-qa)

---

## 1. What is a Dockerfile?

### What
A **Dockerfile** is a plain text file (no extension) containing a sequence of instructions that tells Docker how to **build a custom Docker image**. It's the recipe for creating your application's container.

> 💡 **Analogy:** Think of a Docker image like a cake. A Dockerfile is the recipe — it lists every ingredient (base OS, software, files) and every step (install this, copy that, run this command). Anyone with the recipe can bake the exact same cake, anywhere in the world, every time.

### Why
Without a Dockerfile:
- You'd manually install everything inside a running container every time
- No reproducibility — "works on my machine" problem returns
- No version control for your environment
- Can't automate image creation in CI/CD

With a Dockerfile:
- **Reproducible:** Same image built on any machine, any time
- **Version controlled:** Lives in your Git repo with your code
- **Automated:** Jenkins/GitHub Actions can build it automatically
- **Documented:** Every dependency and config step is explicitly written
- **Shareable:** Anyone on the team or the world can build the same image

### How
You write a Dockerfile → run `docker build` → Docker executes each instruction **in order**, creating a **layer** for each instruction → the final result is a **Docker image** you can run as many containers from as you want.

### Impact

| Without Dockerfile | With Dockerfile |
|-------------------|-----------------|
| Manual setup every time | Automated, one-command build |
| Inconsistent environments | Identical everywhere |
| "It worked yesterday" problems | Version-pinned, repeatable |
| No CI/CD automation possible | Builds automatically in pipelines |
| Knowledge in people's heads | Knowledge in code |

---

## 2. Dockerfile Instructions – Every Command Explained

### `FROM` – The Base Image

```dockerfile
FROM ubuntu:22.04
```

- **What:** Defines the starting point — the base OS or runtime your image builds on
- **Why:** You don't build from nothing. You start from an existing image (OS, language runtime) and add on top
- **Rule:** Every Dockerfile MUST start with `FROM` (except multi-stage builds)

```dockerfile
# Common base images
FROM ubuntu:22.04        # Full Ubuntu OS
FROM debian:12-slim      # Minimal Debian (smaller)
FROM alpine:3.18         # Tiny Linux (~5MB) — smallest common base
FROM python:3.11-slim    # Python with slim Debian
FROM node:22-alpine      # Node.js on Alpine
FROM openjdk:21-slim     # Java 21
FROM nginx:latest        # NGINX web server
FROM scratch             # Literally nothing (for static binaries)
```

---

### `MAINTAINER` – Metadata (Legacy)

```dockerfile
MAINTAINER John Doe <john@example.com>
```

- **What:** Adds author/contact information to the image metadata
- **Status:** Deprecated — use `LABEL` instead
- **Modern equivalent:**

```dockerfile
LABEL maintainer="John Doe <john@example.com>"
LABEL version="1.0"
LABEL description="Shopping cart application"
```

---

### `RUN` – Execute Commands at Build Time

```dockerfile
RUN apt-get update
RUN apt-get install -y nginx python3 git curl
```

- **What:** Executes a shell command **during the image build process**
- **When it runs:** At BUILD time — when you run `docker build`
- **Creates a new layer:** Each `RUN` instruction adds a layer to the image
- **Important:** Changes made by `RUN` are baked into the image permanently

```dockerfile
# Bad practice (multiple RUN = multiple layers = larger image)
RUN apt-get update
RUN apt-get install -y nginx
RUN apt-get install -y python3

# Good practice (chain commands with && to create ONE layer)
RUN apt-get update && apt-get install -y nginx python3 git && apt-get clean && rm -rf /var/lib/apt/lists/*
```

> ⚠️ **`RUN` vs `CMD`:** `RUN` runs at **build time** (baked into image). `CMD` runs at **container start time** (when you do `docker run`).

---

### `CMD` – Default Command at Container Start

```dockerfile
CMD ["echo", "Container is running!"]
CMD ["nginx", "-g", "daemon off;"]
CMD ["python3", "app.py"]
CMD ["java", "-jar", "app.jar"]
```

- **What:** Defines the default command that runs when a container starts
- **When it runs:** At RUNTIME — every time you do `docker run`
- **Can be overridden:** `docker run my-image /bin/bash` replaces the CMD
- **Only one CMD:** If you write multiple `CMD` lines, only the last one is used

```dockerfile
# Two formats:
CMD ["nginx", "-g", "daemon off;"]   # Exec format (recommended)
CMD nginx -g "daemon off;"           # Shell format (runs in /bin/sh -c)
```

> 💡 **Deep Dive: Why `daemon off;`?**
>
> In the command `CMD ["nginx", "-g", "daemon off;"]`:
> - **`nginx`**: Starts the Nginx web server.
> - **`-g`**: Allows you to pass "global" configuration directives to Nginx.
> - **`daemon off;`**: This tells Nginx to run in the **foreground**.
>
> **Why is this required in Docker?**
> A Docker container lives only as long as its **main process** (PID 1) is running.
> - By default, Nginx runs as a background "daemon". If it runs in the background, the initial start command finishes immediately, and Docker thinks the task is done, so it **stops the container**.
> - By setting `daemon off;`, Nginx stays in the foreground, keeping the process active. As long as Nginx is active, the container stays running.

---

### `ENTRYPOINT` – Fixed Command (Can't Override Without --entrypoint)

```dockerfile
ENTRYPOINT ["python3", "app.py"]
```

- **What:** Like CMD but the command is always executed — it can't be overridden by `docker run` arguments
- **When to use:** When your container has one specific purpose and always runs the same program

---

### `COPY` – Copy Files Into the Image

```dockerfile
COPY index.html /usr/share/nginx/html/
COPY . /app/
COPY package*.json /usr/src/app/
```

- **What:** Copies files/directories from your **local machine** into the image at build time
- **Source:** Relative to the build context (where your Dockerfile is)
- **Destination:** Path inside the image

---

### `ADD` – Like COPY but With Superpowers

```dockerfile
ADD app.tar.gz /usr/src/app/        # Auto-extracts tar archives
ADD https://example.com/file.zip /  # Download from URL
```

- **What:** Like COPY but also auto-extracts compressed archives and can download from URLs
- **Best practice:** Use `COPY` unless you specifically need `ADD`'s extra features

---

### `WORKDIR` – Set Working Directory

```dockerfile
WORKDIR /app
RUN npm install    # Runs inside /app
COPY . .           # Copies to /app
```

- **What:** Sets the working directory for all subsequent instructions
- **Why:** Avoids using absolute paths everywhere; keeps things organized

---

### `EXPOSE` – Document the Port

```dockerfile
EXPOSE 3000
EXPOSE 8080
```

- **What:** Documents which port the container application listens on
- **Important:** This does NOT actually publish the port — it's documentation
- **Actual port publishing:** Still requires `-p` flag in `docker run`

---

### `ENV` – Set Environment Variables

```dockerfile
ENV NODE_ENV=production
ENV PORT=3000
ENV DATABASE_URL=postgresql://localhost:5432/mydb
```

- **What:** Sets environment variables that are available both at build time and runtime
- **Why:** Configures the application without hardcoding values in code

---

### `ARG` – Build-Time Variables

```dockerfile
ARG APP_VERSION=1.0.0
RUN echo "Building version $APP_VERSION"
```

- **What:** Like ENV but only available during the build, not at runtime
- **Pass at build time:** `docker build --build-arg APP_VERSION=2.0.0 .`

---

### Complete Instruction Reference

| Instruction | When it runs | Purpose |
|-------------|-------------|---------|
| `FROM` | Build | Set base image |
| `LABEL` | Build | Add metadata |
| `MAINTAINER` | Build | Author info (deprecated) |
| `RUN` | Build | Execute shell commands |
| `COPY` | Build | Copy local files into image |
| `ADD` | Build | Copy files + extract + download |
| `WORKDIR` | Build | Set working directory |
| `ENV` | Build + Runtime | Set environment variables |
| `ARG` | Build only | Build-time variables |
| `EXPOSE` | Documentation | Document the port |
| `CMD` | Runtime | Default start command (overridable) |
| `ENTRYPOINT` | Runtime | Fixed start command |
| `VOLUME` | Runtime | Mount point for external storage |
| `USER` | Build + Runtime | Set user to run as |

---

## 3. The 5-Stage Dockerfile Structure

The class taught a clear 5-stage mental model for writing any Dockerfile:

```
Stage 1: Base Image Selection
         → FROM ubuntu:22.04

Stage 2: Maintainer / Metadata
         → MAINTAINER / LABEL

Stage 3: OS-Level Package Updates
         → RUN apt-get update

Stage 4: Software Installation
         → RUN apt-get install -y nginx python3

Stage 5: Application Command / Completion
         → CMD ["echo", "Image ready!"]
            OR CMD ["nginx", "-g", "daemon off;"]
```

### The First Dockerfile from Class

```dockerfile
# Stage 1: Base Image
FROM ubuntu:22.04

# Stage 2: Metadata
MAINTAINER DevOps Team <devops@company.com>

# Stage 3: OS Update
RUN apt-get update

# Stage 4: Install Software
RUN apt-get install -y nginx python3 git curl

# Stage 5: Completion message / start command
CMD ["echo", "Docker image is ready!"]
```

---

## 4. Building a Custom Docker Image

### What
`docker build` reads your Dockerfile and executes each instruction to produce a custom image stored locally.

### The Build Command

```bash
docker build -t imagename .
#             ↑            ↑
#        image name     build context
#        (tag)          (current directory)
```

- `-t` = tag (name) for the image
- `.` = build context — the directory Docker looks in for the Dockerfile and any files referenced in it

### Step-by-Step Build Process

```bash
# Step 1: Create your project directory
mkdir my-docker-project
cd my-docker-project

# Step 2: Create your Dockerfile
nano Dockerfile
# (write your Dockerfile instructions)

# Step 3: Build the image
docker build -t my-first-image .

# Step 4: Verify it was created
docker images
# Shows: my-first-image   latest   a1b2c3d4   2 minutes ago   123MB

# Step 5: Run a container from your image
docker run my-first-image
# Or interactive:
docker run -it my-first-image /bin/bash
```

### What Happens During `docker build`

```
Step 1/5 : FROM ubuntu:22.04
 ---> 1a2b3c4d5e6f   (pulls ubuntu:22.04 if not cached)

Step 2/5 : MAINTAINER DevOps Team
 ---> Running in a1b2c3d4e5f6
 ---> 2b3c4d5e6f7a   (new layer created)

Step 3/5 : RUN apt-get update
 ---> Running in b2c3d4e5f6a7
Get:1 http://archive.ubuntu.com... (downloads package lists)
 ---> 3c4d5e6f7a8b   (new layer with updated package lists)

Step 4/5 : RUN apt-get install -y nginx python3 git curl
 ---> Running in c3d4e5f6a7b8
(installs packages...)
 ---> 4d5e6f7a8b9c   (new layer with installed packages)

Step 5/5 : CMD ["echo", "Docker image is ready!"]
 ---> 5e6f7a8b9c0d

Successfully built 5e6f7a8b9c0d
Successfully tagged my-first-image:latest
```

### The Build Context

The `.` in `docker build -t name .` tells Docker: "The build context is the current directory." Docker sends ALL files in this directory to the Docker daemon for the build.

> ⚠️ **Use `.dockerignore`** to exclude files you don't want sent:
```
# .dockerignore
node_modules/
.git/
*.log
.env
dist/
```

### Docker Layer Caching – Speed Up Builds

Docker caches each layer. If an instruction hasn't changed since the last build, Docker reuses the cached layer instead of re-running it.

```dockerfile
# SLOW: apt-get update runs every build because code changes
FROM ubuntu:22.04
COPY . /app         # Code changes = cache miss = all below re-runs
RUN apt-get update  # Re-runs unnecessarily every time

# FAST: Package installation is cached unless Dockerfile changes
FROM ubuntu:22.04
RUN apt-get update && apt-get install -y nginx  # Cached ✅
COPY . /app         # Code changes only invalidate THIS layer and below
```

**Rule:** Put things that change RARELY (package installs) near the top. Put things that change FREQUENTLY (your code) near the bottom.

---

## 5. Image Tagging – Naming Your Image Properly

### What
**Tagging** is the process of giving your Docker image a proper name that includes your Docker Hub username, the image name, and a version. This is required before pushing to Docker Hub.

### Why
- Docker Hub identifies images by `username/imagename:version`
- Without a username prefix, Docker doesn't know which account to push to
- Tags let you track versions (v1.0, v1.1, latest)

### How – The Tag Command

```bash
docker tag SOURCE_IMAGE TARGET_IMAGE

# Full format:
docker tag LOCAL_IMAGE_NAME_OR_ID DOCKERHUB_USERNAME/IMAGE_NAME:TAG

# Examples:
docker tag my-first-image johndoe/my-first-image:latest
docker tag my-first-image johndoe/my-first-image:v1.0
docker tag a1b2c3d4e5f6 johndoe/shopping-cart:v2.1

# After tagging, docker images shows both:
# my-first-image              latest   a1b2c3d4   (original)
# johndoe/my-first-image      latest   a1b2c3d4   (same image, new name)
# johndoe/my-first-image      v1.0     a1b2c3d4   (same image, version tag)
```

### Version Tags – Best Practices

```bash
# Always tag with a specific version AND latest
docker tag my-app johndoe/my-app:1.0.0
docker tag my-app johndoe/my-app:latest

# After a new version:
docker tag my-app johndoe/my-app:1.1.0
docker tag my-app johndoe/my-app:latest   # latest now points to 1.1.0
```

> 💡 **`latest` tag:** It's just a convention — Docker doesn't automatically update it. You must manually tag each new version as `latest` if you want that behavior.

---

## 6. Docker Hub – Pushing & Pulling Images

### What
**Docker Hub** (hub.docker.com) is the default public container registry — a cloud storage for Docker images. It's like GitHub but for Docker images.

### Why
- Share your images with teammates or the world
- Store images for deployment — your server pulls the image instead of building it
- Maintain a history of image versions
- Public images: free | Private images: limited free, paid for more

### The Complete Push Workflow

#### Step 1: Login to Docker Hub

```bash
docker login
# Enter your Docker Hub username
# Enter your Docker Hub password
# Login Succeeded ✅
```

#### Step 2: Tag Your Image with Your Username

```bash
docker tag my-first-image yourusername/my-first-image:latest
```

#### Step 3: Push to Docker Hub

```bash
docker push yourusername/my-first-image:latest

# Output:
# The push refers to repository [docker.io/yourusername/my-first-image]
# a1b2c3d: Pushing  123.4MB/456.7MB
# latest: digest: sha256:abc123... size: 1234
```

#### Step 4: Verify on Docker Hub
```
Go to: https://hub.docker.com/r/yourusername/my-first-image
```

### The Pull Workflow (Testing / Deployment)

```bash
# Pull the image on any machine
docker pull yourusername/my-first-image:latest

# Run it
docker run yourusername/my-first-image:latest

# Or run someone else's class image to test
docker pull classmate_username/their-image:latest
docker run classmate_username/their-image:latest
```

### Docker Hub vs Other Registries

| Registry | Who uses it | URL |
|----------|------------|-----|
| **Docker Hub** | Public projects, beginners | hub.docker.com |
| **AWS ECR** | AWS-deployed applications | ACCOUNT.dkr.ecr.REGION.amazonaws.com |
| **GCR (Google)** | GCP applications | gcr.io/PROJECT/IMAGE |
| **GitHub Container Registry** | GitHub-hosted projects | ghcr.io/USER/IMAGE |
| **Private Registry** | Enterprise (self-hosted) | your.registry.company.com |

### Pushing to AWS ECR (Production Pattern)

```bash
# Authenticate to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# Tag for ECR
docker tag my-app:latest ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/my-app:latest

# Push to ECR
docker push ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/my-app:latest
```

---

## 7. Creating Images from Running Containers – docker commit

### What
`docker commit` creates a new Docker image from the **current state** of a running or stopped container — capturing all changes made to the filesystem since the container started.

> 💡 **Analogy:** Imagine you're working on a document. `docker commit` is like saving a snapshot of the document at this exact moment — all your edits are preserved in the snapshot.

### Why
- You made manual changes inside a container and want to save that state as a reusable image
- Quickly "save your work" without writing a Dockerfile
- Create a checkpoint image before making risky changes

### How

```bash
# Step 1: Start a container and make changes
docker run -it ubuntu /bin/bash

# Inside the container, install things:
apt-get update
apt-get install -y nginx python3 git
echo "Custom setup complete"
exit   # Exit without stopping (or Ctrl+P, Ctrl+Q to detach)

# Step 2: Find the container ID
docker ps -a
# CONTAINER ID: a1b2c3d4e5f6

# Step 3: Commit to a new image
docker commit a1b2c3d4e5f6 my-custom-ubuntu

# With a commit message and author:
docker commit --message "Added nginx, python3, git" --author "John Doe" a1b2c3d4e5f6 my-custom-ubuntu:v1.0

# Step 4: Verify
docker images
# my-custom-ubuntu   v1.0   b2c3d4e5f6a7   Just now   234MB

# Step 5: Run from committed image
docker run -it my-custom-ubuntu:v1.0 /bin/bash
# python3 and git are already there ✅
```

### `docker commit` vs Dockerfile

| `docker commit` | Dockerfile |
|----------------|-----------|
| Manual process — you did it by hand | Automated — instructions are code |
| Hard to reproduce exactly | 100% reproducible |
| No version history of what was done | Every step is documented |
| Quick and easy for one-off saves | Requires writing the file |
| Not suitable for CI/CD | The standard for CI/CD |
| Use for: quick prototyping, exploration | Use for: everything in production |

> 💡 **Best practice:** Use `docker commit` to explore and figure out what steps you need. Then write those steps into a proper Dockerfile.

---

## 8. Backup & Offline Storage – docker save & docker load

### What
`docker save` exports a Docker image as a `.tar` file (compressed archive) that can be stored on disk, transferred via USB, uploaded to S3, or loaded on a machine without internet access.

### Why — Real-World Use Cases
- **Restricted environments:** Production servers that can't access Docker Hub (security policy)
- **Air-gapped systems:** Banks, military, government — no internet at all
- **Backup strategy:** Store images in S3 before major deployments
- **Transfer to offline machines:** Move images without a registry
- **Quarterly housekeeping:** Archive old image versions before cleanup

### Commands

#### Save Image to tar File

```bash
# Save single image
docker save my-app:latest > my-app.tar

# Save with explicit output flag
docker save -o my-app.tar my-app:latest

# Save multiple images into one tar
docker save -o images-backup.tar my-app:latest nginx:latest postgres:15

# Compress while saving (smaller file)
docker save my-app:latest | gzip > my-app.tar.gz
```

#### Load Image from tar File

```bash
# Load from tar file
docker load < my-app.tar

# Load with input flag
docker load -i my-app.tar

# Load compressed
docker load < my-app.tar.gz

# Verify it loaded
docker images
# my-app   latest   a1b2c3d4   (loaded from tar)
```

#### The Complete Backup/Restore Workflow

```bash
# === BACKUP (on source machine) ===
# Build or pull your image
docker build -t shopping-cart:v1.0 .

# Save to tar
docker save -o shopping-cart-v1.0.tar shopping-cart:v1.0
ls -lh shopping-cart-v1.0.tar
# -rw-r--r-- 1 ubuntu ubuntu 487M May 4 14:23 shopping-cart-v1.0.tar

# Upload to S3 for safekeeping
aws s3 cp shopping-cart-v1.0.tar s3://my-company-backups/docker/

# === RESTORE (on target machine with no internet) ===
# Download from S3
aws s3 cp s3://my-company-backups/docker/shopping-cart-v1.0.tar .

# Load the image
docker load -i shopping-cart-v1.0.tar

# Run it
docker run -d -p 3000:3000 shopping-cart:v1.0
```

### `docker export` / `docker import` – For Containers (Not Images)

```bash
# Export a running container's filesystem (not the image)
docker export my-container > container-backup.tar

# Import back as a new image
cat container-backup.tar | docker import - my-restored-image:latest
```

| Command | Works with | Includes image history/layers |
|---------|-----------|------------------------------|
| `docker save` | Images | ✅ Yes (full image with all layers) |
| `docker export` | Containers | ❌ No (just filesystem snapshot) |
| `docker load` | Restores `save` output | ✅ Yes |
| `docker import` | Restores `export` output | ❌ No layers |

---

## 9. Troubleshooting Containers – The Three Commands

### What
When something goes wrong with a container, three commands cover 95% of all investigation needs.

> 💡 **Troubleshooting order:** Always start with `docker logs` → then `docker inspect` → then `docker stats`.

---

### Command 1: `docker logs` – What Did the App Say?

**What:** Shows the STDOUT and STDERR output from the container's main process — everything the application printed since it started.

```bash
# Show all logs
docker logs my-container

# Follow logs in real time (like tail -f)
docker logs -f my-container

# Show last 50 lines
docker logs --tail 50 my-container

# Show logs with timestamps
docker logs -t my-container

# Show logs since a specific time
docker logs --since 2026-05-04T14:00:00 my-container
docker logs --since 1h my-container   # Last 1 hour
```

**When to use:** Application not behaving correctly, container exiting unexpectedly, checking for startup errors.

---

### Command 2: `docker inspect` – Deep Container Metadata

**What:** Returns complete JSON metadata about a container or image — IP address, port bindings, volume mounts, environment variables, current state, network settings, restart count.

```bash
# Full inspect output (very long JSON)
docker inspect my-container

# Get just the IP address
docker inspect my-container --format='{{.NetworkSettings.IPAddress}}'

# Get the container's state
docker inspect my-container --format='{{.State.Status}}'
docker inspect my-container --format='{{.State.ExitCode}}'
docker inspect my-container --format='{{.State.Error}}'

# Get all environment variables
docker inspect my-container --format='{{.Config.Env}}'

# Get volume mounts
docker inspect my-container --format='{{json .Mounts}}' | python3 -m json.tool

# Get port bindings
docker inspect my-container --format='{{json .NetworkSettings.Ports}}' | python3 -m json.tool
```

**Useful inspect fields:**

| Field | What it shows |
|-------|--------------|
| `.State.Status` | running, exited, paused |
| `.State.ExitCode` | 0=success, non-zero=error |
| `.State.Error` | Error message if crashed |
| `.NetworkSettings.IPAddress` | Container's internal IP |
| `.NetworkSettings.Ports` | Port mappings |
| `.Mounts` | Volume mount details |
| `.Config.Env` | Environment variables |
| `.Config.Image` | Which image it's running |
| `.HostConfig.Memory` | Memory limit |

**When to use:** Container has wrong IP, volumes not mounting, ports not binding, container crashed with no log output.

---

### Command 3: `docker stats` – Resource Consumption

**What:** Real-time CPU, memory, network, and disk I/O usage for all running containers.

```bash
# Live stats for all containers
docker stats

# Stats for specific container
docker stats my-container

# One-time snapshot (no live updates)
docker stats --no-stream

# Custom format
docker stats --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}"
```

**When to use:** Container is slow, server running hot, investigating memory leaks, capacity planning.

---

### Troubleshooting Decision Tree

```
Container not working?
         │
         ▼
Is it running?
├── NO → docker ps -a → docker logs container_name (see why it exited)
│                     → docker inspect container_name (check ExitCode and Error)
│
└── YES → What's the symptom?
          │
          ├── Application errors → docker logs -f my-container
          │
          ├── Can't connect to it → docker inspect my-container
          │                        (check IP, port bindings, network)
          │
          ├── Slow / high CPU → docker stats
          │
          └── Data not persisting → docker inspect my-container
                                    (check .Mounts section)
```

---

## 10. Cleanup Operations

### What
Over time, Docker accumulates unused images, stopped containers, unused networks, and orphaned volumes. Cleanup commands reclaim this disk space.

> ⚠️ **CRITICAL WARNING:** Never run cleanup commands in production without manager approval. Deleted data CANNOT be recovered. Always confirm what will be deleted before running prune commands.

### Check Disk Usage First

```bash
docker system df

# Output:
# TYPE            TOTAL     ACTIVE    SIZE      RECLAIMABLE
# Images          15        3         4.2GB     3.1GB (73%)
# Containers      8         2         124MB     89MB (71%)
# Local Volumes   5         2         2.3GB     890MB (38%)
# Build Cache     0         0         0B        0B
```

### The Cleanup Commands

#### Clean Everything Unused at Once

```bash
# Remove: stopped containers + unused networks + dangling images
docker system prune

# ALSO remove unused volumes (more aggressive)
docker system prune --volumes

# Skip confirmation prompt (for scripts)
docker system prune -f
```

#### Clean Specific Things

```bash
# Remove only stopped containers
docker container prune

# Remove all images not used by any container
docker image prune -a

# Remove only dangling images (untagged/orphaned layers)
docker image prune

# Remove unused volumes only
docker volume prune

# Remove unused networks only
docker network prune
```

#### Manual Targeted Cleanup

```bash
# Remove specific stopped container
docker rm container_name

# Force remove running container
docker rm -f container_name

# Remove all stopped containers
docker rm $(docker ps -aq)

# Remove specific image
docker rmi image_name:tag

# Force remove image (even if container uses it)
docker rmi -f image_name

# Remove all images
docker rmi $(docker images -q)
```

### Quarterly Housekeeping Checklist (Real-World)

```
1. Check disk usage:        docker system df
2. Review what's running:   docker ps
3. List all images:         docker images
4. Identify old/unused images (check creation date and last used)
5. Check with team: "Is anyone using image X?"
6. Get manager approval for cleanup
7. Remove unused containers: docker container prune
8. Remove unused images:     docker image prune -a
9. Remove unused volumes:    docker volume prune
10. Verify disk recovered:   docker system df
11. Document what was cleaned and when
```

### Production-Safe Cleanup Pattern

```bash
# SAFE: Only remove containers/images not tagged 'latest' or 'production'
# First, see what would be removed (dry run mentality)
docker images --filter "dangling=true"
docker ps -a --filter "status=exited"

# SAFER: Remove only containers that exited more than 24 hours ago
docker ps -a --filter "status=exited" --filter "since=24h"

# Remove a specific old image by name and tag (targeted)
docker rmi myapp:v1.0  # Only removes v1.0, keeps v2.0 and latest
```

---

## 11. Tech Stack Mapping

### Dockerfile in a Complete DevOps Pipeline

```
Developer writes code
        │
        ▼
Dockerfile in the same Git repo:
  my-project/
  ├── src/
  ├── Dockerfile       ← Defines how to containerize the app
  ├── .dockerignore
  └── Jenkinsfile      ← Calls docker build + push
        │
        ▼
Jenkins CI Pipeline:
  Stage 1: Git clone
  Stage 2: mvn package / npm build
  Stage 3: docker build -t app:${BUILD_NUMBER} .
  Stage 4: docker tag app:${BUILD_NUMBER} youraccount/app:${BUILD_NUMBER}
  Stage 5: docker push youraccount/app:${BUILD_NUMBER}
        │
        ▼
Docker Hub / AWS ECR (Image Registry)
        │
        ▼
Production Server pulls and runs:
  docker pull youraccount/app:${BUILD_NUMBER}
  docker run -d -p 80:3000 youraccount/app:${BUILD_NUMBER}
```

### Dockerfiles by Application Type

| App Type | Base Image | Key Instructions | Start Command |
|----------|-----------|-----------------|--------------|
| **Node.js API** | `node:22-alpine` | `COPY package*.json`, `RUN npm ci`, `COPY . .` | `CMD ["node", "server.js"]` |
| **React/Next.js** | `node:22-alpine` (build), `nginx:alpine` (serve) | Multi-stage build | `CMD ["nginx", "-g", "daemon off;"]` |
| **Spring Boot** | `openjdk:21-slim` | `COPY *.jar app.jar` | `CMD ["java", "-jar", "app.jar"]` |
| **Python Flask** | `python:3.11-slim` | `COPY requirements.txt`, `RUN pip install` | `CMD ["python", "app.py"]` |
| **Static HTML** | `nginx:alpine` | `COPY html/ /usr/share/nginx/html/` | (NGINX starts by default) |

---

## 12. Visual Diagrams

### Diagram 1: Dockerfile → Image → Container Flow

```
Dockerfile                 Image                  Container
──────────                 ─────                  ─────────
FROM ubuntu:22.04    ──►   Layer 1: Ubuntu    ──► Running process
RUN apt-get update   ──►   Layer 2: pkg lists     with its own:
RUN apt-get install  ──►   Layer 3: nginx,py3     • Filesystem
COPY . /app          ──►   Layer 4: your code     • Network
CMD ["python3","app"]──►   Layer 5: CMD config    • Process space

docker build -t myapp .    docker images           docker run myapp
(builds the image)         (see the image)         (starts container)
```

---

### Diagram 2: Image Layers (How Docker Stores Images)

```
┌─────────────────────────────────────┐
│  Container Write Layer              │  ← Unique per container (temporary)
│  (your runtime changes)             │
├─────────────────────────────────────┤
│  Layer 5: CMD ["node", "server.js"] │  ← Your Dockerfile
├─────────────────────────────────────┤
│  Layer 4: COPY . /app               │  ← Your Dockerfile
├─────────────────────────────────────┤
│  Layer 3: RUN npm install           │  ← Your Dockerfile
├─────────────────────────────────────┤
│  Layer 2: COPY package.json /app    │  ← Your Dockerfile
├─────────────────────────────────────┤
│  Layer 1: node:22-alpine (base)     │  ← FROM
└─────────────────────────────────────┘

Each layer is cached. Change Layer 4 → Layers 1-3 reused from cache ✅
                                      → Layers 4-5 rebuilt from scratch
```

---

### Diagram 3: Docker Hub Push/Pull Workflow

```
Developer Machine              Docker Hub                  Production Server
──────────────────             ──────────                  ─────────────────
docker build .      ─────►    (builds locally)
docker tag app      
yourusername/app:v1 ─────►
docker push         ─────────────────────────────────────►  hub.docker.com
yourusername/app:v1              stored safely              yourusername/app:v1

                                                            docker pull
                                                            yourusername/app:v1
                                                            docker run -d -p 80:3000
                                                            yourusername/app:v1
```

---

### Diagram 4: docker commit vs Dockerfile Workflow

```
DOCKER COMMIT (Quick & Dirty)          DOCKERFILE (Proper Way)
─────────────────────────────          ─────────────────────────
docker run -it ubuntu bash             Write Dockerfile:
> apt install nginx python3              FROM ubuntu:22.04
> echo "custom content" > file          RUN apt-get install...
> exit                                  COPY . /app
                                        CMD [...]
docker commit a1b2c3 my-image
                                       docker build -t my-image .
Use for: exploring, prototyping        Use for: everything else
❌ Not reproducible                    ✅ Fully reproducible
❌ No history of what was done         ✅ Every step documented
```

---

### Diagram 5: docker save / docker load – Offline Image Transfer

```
Machine WITH internet              Machine WITHOUT internet
(or production machine)            (air-gapped / restricted)

docker pull nginx:latest           
docker save nginx:latest           
  > nginx.tar               ──────► USB / S3 / SFTP ──────► docker load -i nginx.tar
                                                              docker images
                                                              nginx   latest   ✅
```

---

### Diagram 6: Troubleshooting Command Selection

```
Something's wrong with a container
              │
     ┌────────┴──────────┐
     ▼                   ▼
Container exited?    Container running but broken?
     │                   │
     ▼                   ├── App errors?      → docker logs -f container
docker logs container    │
docker inspect container ├── Network/IP?     → docker inspect container
(check ExitCode, Error)  │
                         └── Slow/CPU?       → docker stats
```

---

## 13. Code & Practical Examples

### Example 1: Complete Dockerfile – Ubuntu with Nginx & Python

```dockerfile
# The exact Dockerfile from class, explained line by line

# Stage 1: Base Image — Start from Ubuntu 22.04 LTS
FROM ubuntu:22.04

# Stage 2: Metadata
MAINTAINER DevOps Student <student@devops.com>

# Stage 3: Update OS package lists
# apt-get update refreshes the list of available packages
RUN apt-get update

# Stage 4: Install required software
# -y flag answers "yes" to all prompts automatically (non-interactive)
RUN apt-get install -y nginx python3 git curl wget

# Stage 5: Completion — this command runs when container starts
CMD ["echo", "✅ Custom Docker image is ready!"]
```

```bash
# Build it
docker build -t my-ubuntu-custom .

# Verify
docker images | grep my-ubuntu-custom

# Run it (should print the echo message and exit)
docker run my-ubuntu-custom

# Enter it interactively (nginx and python3 are installed)
docker run -it my-ubuntu-custom /bin/bash
```

---

### Example 2: Production-Grade Node.js Dockerfile

```dockerfile
# Multi-stage build for a production Node.js API

# ── Stage 1: Build Stage ──────────────────────────────────
FROM node:22-alpine AS builder

WORKDIR /app

# Copy package files first (layer caching optimization)
COPY package*.json ./

# Install ALL dependencies (including dev)
RUN npm ci

# Copy source code
COPY . .

# Build the application (if using TypeScript or bundler)
RUN npm run build

# ── Stage 2: Production Stage ────────────────────────────
FROM node:22-alpine AS production

LABEL maintainer="devops@company.com"
LABEL version="1.0.0"
LABEL description="Shopping Cart Node.js API"

# Set working directory
WORKDIR /app

# Set production environment
ENV NODE_ENV=production
ENV PORT=3000

# Copy only production dependencies
COPY package*.json ./
RUN npm ci --only=production

# Copy built application from build stage
COPY --from=builder /app/dist ./dist

# Create non-root user (security best practice)
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

# Document the port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1

# Start the application
CMD ["node", "dist/server.js"]
```

---

### Example 3: Next.js Production Dockerfile

```dockerfile
FROM node:22-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci

FROM node:22-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
ENV NEXT_TELEMETRY_DISABLED 1
RUN npm run build

FROM node:22-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED 1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs
EXPOSE 3000
ENV PORT 3000

CMD ["node", "server.js"]
```

---

### Example 4: Jenkins Pipeline – Build, Tag, Push to Docker Hub

```groovy
pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds')
        IMAGE_NAME             = 'yourusername/shopping-cart'
        IMAGE_TAG              = "${BUILD_NUMBER}"
    }

    stages {

        stage('Clone') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/yourname/shopping-cart.git'
            }
        }

        stage('Build App') {
            steps {
                sh 'mvn clean package -DskipTests'
            }
        }

        stage('Docker Build') {
            steps {
                sh """
                    docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                    docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest
                """
            }
        }

        stage('Docker Login') {
            steps {
                sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
            }
        }

        stage('Docker Push') {
            steps {
                sh """
                    docker push ${IMAGE_NAME}:${IMAGE_TAG}
                    docker push ${IMAGE_NAME}:latest
                """
            }
        }

        stage('Deploy') {
            steps {
                sh """
                    docker stop shopping-cart 2>/dev/null || true
                    docker rm shopping-cart 2>/dev/null || true
                    docker run -d \
                      --name shopping-cart \
                      -p 3000:3000 \
                      --restart unless-stopped \
                      ${IMAGE_NAME}:${IMAGE_TAG}
                """
            }
        }

        stage('Cleanup Local Images') {
            steps {
                sh """
                    docker rmi ${IMAGE_NAME}:${IMAGE_TAG} || true
                    docker image prune -f
                """
            }
        }
    }

    post {
        success {
            echo "✅ Image ${IMAGE_NAME}:${IMAGE_TAG} deployed!"
        }
        failure {
            echo "❌ Pipeline failed. Check logs above."
        }
    }
}
```

---

### Example 5: Backup Script for Docker Images

```bash
#!/bin/bash
# Quarterly Docker image backup script

BACKUP_DIR="/backups/docker-images"
S3_BUCKET="s3://company-backups/docker"
DATE=$(date +%Y-%m-%d)

mkdir -p $BACKUP_DIR

echo "=== Docker Disk Usage Before Backup ==="
docker system df

echo ""
echo "=== Images to Backup ==="
docker images --format "{{.Repository}}:{{.Tag}}"

# Save each production image
for IMAGE in shopping-cart:latest api-gateway:latest nginx:latest; do
    echo "Saving: $IMAGE"
    FILENAME="${IMAGE//[:\/]/-}-${DATE}.tar"
    docker save $IMAGE > "$BACKUP_DIR/$FILENAME"
    echo "Saved: $BACKUP_DIR/$FILENAME ($(ls -lh $BACKUP_DIR/$FILENAME | awk '{print $5}'))"

    # Upload to S3
    aws s3 cp "$BACKUP_DIR/$FILENAME" "$S3_BUCKET/$FILENAME"
    echo "Uploaded to: $S3_BUCKET/$FILENAME"
done

echo ""
echo "=== Backup Complete ==="
ls -lh $BACKUP_DIR/
```

---

### Example 6: Python Flask Dockerfile

```dockerfile
FROM python:3.11-slim

LABEL maintainer="devops@company.com"

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home appuser
USER appuser

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_ENV=production

HEALTHCHECK CMD curl -f http://localhost:5000/health || exit 1

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]
```

---

### Practical: Create Dockerfile, Build Custom Nginx Image, Tag & Push to Docker Hub

#### What
This practical covers the full lifecycle of a custom Docker image: from writing the "recipe" (Dockerfile) using a base OS (Ubuntu), building the binary artifact (Image), naming it for the cloud (Tagging), and finally publishing it to a global registry (Pushing).

#### Why
Using a base OS like Ubuntu allows you to fully customize your environment. However, you must explicitly install and configure services like Nginx. Sharing these images on **Docker Hub** ensures that your team can pull the exact same configuration you've built.

#### Step-by-Step Guidance

**Step 1: Create Your Project Workspace**
```bash
mkdir custom-ubuntu-nginx
cd custom-ubuntu-nginx
```

**Step 2: Create the Dockerfile**
Create a file named `Dockerfile` and add the following content:
```dockerfile
FROM ubuntu
MAINTAINER rnishant428@gmail.com

RUN apt-get update
RUN apt-get install nginx -y

CMD ["echo", "Image created"]
```

**Step 3: Build Your Custom Image**
```bash
docker build -t my-ubuntu-nginx .
```
*   `docker build`: The command to create an image.
*   `-t`: Tags the image with a local name.
*   `.`: The build context (current directory).

**Step 4: Verify the Local Image**
```bash
docker images
# You should see 'my-ubuntu-nginx' in the list
```

**Step 5: Run the Container**
```bash
docker run my-ubuntu-nginx
# Output: Image created
```
*Note: The container exits immediately after printing the message because the CMD finished.*

**Step 6: Login to Docker Hub**
```bash
docker login
```

**Step 7: Tag Your Image for Docker Hub**
```bash
docker tag my-ubuntu-nginx rnishant428/my-ubuntu-nginx:v1.0
docker tag my-ubuntu-nginx rnishant428/my-ubuntu-nginx:latest
```

**Step 8: Push to Docker Hub**
```bash
docker push rnishant428/my-ubuntu-nginx:latest
```

---

### HW Assignment: Fix the Nginx Container

**The Problem:**
You successfully pushed your image. However, when you run it:
`docker run -d --name my-nginx -p 80:80 rnishant428/my-ubuntu-nginx:latest`

1.  The container starts and **immediately stops** (status: Exited).
2.  You cannot access the Nginx web page at `localhost:80`.
3.  `docker logs my-nginx` only shows "Image created".

**Your Task:**
Troubleshoot and fix the Dockerfile so the container **stays running** and **serves the Nginx web page**.

#### Troubleshooting & Fix Guidance (How to Solve)

1.  **Step 1: Understand why it stopped**
    Docker containers stay alive only as long as their main process (the `CMD`) is running. In our case, the `echo` command finishes in milliseconds, so the container shuts down.

2.  **Step 2: Identify the fix**
    To keep the container running, the `CMD` must start a long-running process. Since we installed Nginx, we should tell Nginx to start in the **foreground**.

3.  **Step 3: Update the Dockerfile**
    Modify the last line of your Dockerfile:
    ```dockerfile
    FROM ubuntu
    MAINTAINER rnishant428@gmail.com
    RUN apt-get update
    RUN apt-get install nginx -y
    
    # FIX: Start nginx in the foreground
    CMD ["nginx", "-g", "daemon off;"]
    ```

4.  **Step 4: Rebuild, Retag, and Rerun**
    ```bash
    # Rebuild
    docker build -t rnishant428/my-ubuntu-nginx:fixed .
    
    # Run in background
    docker run -d --name my-web-fixed -p 80:80 rnishant428/my-ubuntu-nginx:fixed
    
    # Verify it's running
    docker ps
    ```
    *Now visit `localhost:80` and you will see the Ubuntu Nginx welcome page!*

---

### Practical: Create, Build & Run a Jenkins Docker Image

#### What
This practical involves creating a customized Jenkins environment. We start with the official Jenkins Long Term Support (LTS) image and add specific system tools needed for our automation pipelines.

#### Why
In a real DevOps setup, a "naked" Jenkins installation is rarely enough. You often need to:
1.  **Pre-install tools**: Like Python, Maven, or Docker CLI inside the Jenkins container.
2.  **Security**: Switch between `root` (for installation) and `jenkins` user (for running) to follow the Principle of Least Privilege.
3.  **Persistence**: Prepare the image for volume mounting so your jobs aren't lost.

#### The Jenkins Dockerfile
Create a new directory `my-jenkins-setup` and save this as `Dockerfile`:

```dockerfile
# Stage 1: Base Image
FROM jenkins/jenkins:lts

# Stage 2: Metadata
LABEL maintainer="rnishant428@gmail.com"

# Stage 3: Installation (Requires Root)
USER root
RUN apt-get update && apt-get install -y python3 python3-pip git curl

# Stage 4: Revert to Jenkins User (Security Best Practice)
USER jenkins

# Stage 5: Documentation
# 8080: Web UI | 50000: Agent communication
EXPOSE 8080
EXPOSE 50000
```

#### Step-by-Step Guidance

**Step 1: Create Workspace**
```bash
mkdir jenkins-custom && cd jenkins-custom
touch Dockerfile
```

**Step 2: Build the Image**
```bash
docker build -t my-custom-jenkins:v1 .
```
*   The `USER root` command allowed us to install python3 and git during this build phase.

**Step 3: Run the Jenkins Container**
```bash
docker run -d \
  --name jenkins-server \
  -p 8080:8080 \
  -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  my-custom-jenkins:v1
```
*   `-p 8080:8080`: Maps the Jenkins Web Dashboard to your host.
*   `-p 50000:50000`: Used for connecting Jenkins build agents.
*   `-v jenkins_home...`: Ensures your configurations/jobs survive container restarts.

**Step 4: Access Jenkins**
1.  Open `http://localhost:8080`.
2.  To get the initial admin password, run:
    ```bash
    docker exec jenkins-server cat /var/jenkins_home/secrets/initialAdminPassword
    ```

---

## 14. Scenario-Based Q&A

---

🔍 **Scenario 1:** Your company's production servers have no internet access due to security policy. Your new application is containerized. How do you get the Docker image onto the production server?

✅ **Answer:** Use `docker save` and `docker load`. On a machine with internet access: `docker pull` or `docker build` the image, then `docker save my-app:latest > my-app.tar`. Transfer the tar file to production via S3 (`aws s3 cp`), SFTP, or approved file transfer. On the production server: `docker load -i my-app.tar`. The image is now available locally without any internet access. This is the standard approach for air-gapped environments — build and save on a CI server that has internet, transfer the artifact to restricted environments.

---

🔍 **Scenario 2:** A container starts but immediately exits. You run `docker ps` and the container isn't there. How do you investigate?

✅ **Answer:** The container exited (either successfully or with an error). Use `docker ps -a` to see stopped containers. Find your container and check two things: (1) `docker logs container_name` — see what the application printed before exiting. Look for error messages; (2) `docker inspect container_name --format='{{.State.ExitCode}}'` — an exit code of 0 means it completed normally (your CMD just ran and finished), non-zero means it crashed. For processes that should keep running (web servers), make sure the process runs in the foreground — `nginx -g "daemon off;"` not just `nginx`.

---

🔍 **Scenario 3:** Your team member pushed a Docker image to Docker Hub. You need to use it. How do you get it and run it?

✅ **Answer:** `docker pull teammatename/imagename:tag` downloads the image to your local machine. Then `docker run teammatename/imagename:tag` runs it. If you need specific port mapping or volumes: `docker run -d -p 8080:80 -v /data:/app/data teammatename/imagename:tag`. You can also run it directly without explicitly pulling — `docker run` will auto-pull if the image isn't local. Check available tags on `hub.docker.com/r/teammatename/imagename` to ensure you're using the right version.

---

🔍 **Scenario 4:** After several months of active Docker usage, your Jenkins server's disk is at 95% capacity. How do you safely reclaim space?

✅ **Answer:** Follow the safe cleanup process: (1) `docker system df` — understand what's consuming space; (2) Check with the team: "Are there any images/containers we must keep?"; (3) Get manager approval; (4) Remove safely: `docker container prune` (only stopped containers), `docker image prune -a` (only images not used by any running container), `docker volume prune` (only volumes not mounted by any container); (5) Verify: `docker system df` again; (6) If more space is needed: `docker system prune --volumes`. Never use force-all cleanup commands without verification — you could delete images that are needed for rollback.

---

🔍 **Scenario 5:** You're experimenting with a new software setup inside an Ubuntu container. After 2 hours of trial and error, you've got everything working perfectly. You don't want to lose this work. What do you do?

✅ **Answer:** Use `docker commit`. While the container is still running (or after stopping it): `docker commit container_id my-working-setup:v1`. This takes a snapshot of the container's current filesystem state and saves it as a new image. Then push it to Docker Hub for safety: `docker tag my-working-setup:v1 yourusername/my-working-setup:v1` → `docker push yourusername/my-working-setup:v1`. Long-term, translate your manual steps into a proper Dockerfile so the setup is reproducible and version-controlled — `docker commit` is a safety net, not a workflow.

---

🔍 **Scenario 6:** You're onboarding a new developer. They need a full development environment: Node.js 18, MongoDB, Redis, and NGINX, all running locally. How do you set this up using Docker without installing anything natively?

✅ **Answer:** Create individual containers for each service using the appropriate images with correct port and volume mappings:
```bash
docker run -d --name mongo -p 27017:27017 -v mongo-data:/data/db mongo:6
docker run -d --name redis -p 6379:6379 -v redis-data:/data redis:7
docker run -d --name nginx -p 80:80 -v ./nginx.conf:/etc/nginx/conf.d/default.conf nginx
docker run -d --name api -p 3000:3000 -v .:/app -w /app node:22-alpine node server.js
```
The developer's machine stays clean — no native installs needed. Each service is isolated, versioned, and identical to what runs in production. This is also a great introduction to Docker Compose, which would manage all these services from a single file.

---

## 15. Interview Q&A

---

**Q1. What is a Dockerfile and what are its most important instructions?**

**A:** A Dockerfile is a plain text file containing sequential instructions that Docker executes to build a custom image. The most important instructions: `FROM` (mandatory — sets the base image everything builds on), `RUN` (executes commands at build time — installs packages, sets up the environment), `COPY` (copies files from the host into the image), `CMD` (sets the default command that runs when a container starts — can be overridden), `WORKDIR` (sets the working directory for subsequent instructions), `ENV` (sets environment variables), and `EXPOSE` (documents which port the application uses). The key distinction: `RUN` executes at build time and its result is baked into the image. `CMD` executes at runtime when the container starts.

---

**Q2. What is the difference between `CMD` and `ENTRYPOINT`?**

**A:** Both define what runs when a container starts, but they behave differently when you pass arguments to `docker run`. `CMD` is the default command — it can be completely replaced by anything you put after the image name: `docker run my-image /bin/bash` ignores the `CMD` entirely. `ENTRYPOINT` is the fixed executable — it always runs, and anything after the image name in `docker run` is passed as arguments to it: `docker run my-image --port 3000` passes `--port 3000` to the ENTRYPOINT command. Common pattern: use ENTRYPOINT for the main executable, CMD for default arguments that can be overridden.

---

**Q3. How do Docker image layers work and why do they matter for build performance?**

**A:** Each instruction in a Dockerfile creates a new layer — a filesystem snapshot of changes made by that instruction. Layers are cached: if a layer's instruction hasn't changed since the last build, Docker reuses the cached version instead of re-running it. This dramatically speeds up builds. The practical implication: order your Dockerfile so things that change rarely (base image, package installs) come early — they'll be cached. Things that change frequently (your application code) come late — only those layers rebuild. The classic optimization: `COPY package.json .` → `RUN npm install` → `COPY . .` — dependencies are cached as long as package.json doesn't change, even if your application code changes constantly.

---

**Q4. How do you push a Docker image to Docker Hub? Walk through the steps.**

**A:** Four steps: (1) `docker login` — authenticate with Docker Hub credentials; (2) `docker tag local-image yourusername/imagename:tag` — the image must be named with your Docker Hub username prefix for Docker to know which account to push to; (3) `docker push yourusername/imagename:tag` — uploads the image layers to Docker Hub; (4) Verify at `hub.docker.com/r/yourusername/imagename`. Always push with both a specific version tag and `latest` if it's your current stable version. In a Jenkins pipeline, use the Credentials plugin to store Docker Hub credentials securely and `docker login --password-stdin` to avoid the password appearing in logs.

---

**Q5. What is `docker save` and when would you use it in production?**

**A:** `docker save` exports a Docker image as a `.tar` archive file: `docker save my-app:latest > my-app.tar`. It's used when: (1) Production servers have no internet access — you build the image on a CI server, save it as tar, transfer it via S3 or SFTP, and load it with `docker load -i my-app.tar`; (2) Backup strategy — save important image versions before major deployments or quarterly housekeeping; (3) Air-gapped environments — banks, government, military systems with no external internet; (4) Transferring images between registries without a common network path. Important: `docker save` preserves image layers and history. `docker export` (for containers) does not.

---

**Q6. What is `docker commit` and when is it appropriate to use?**

**A:** `docker commit` creates a new image from a running or stopped container's current state: `docker commit container_id new-image-name:tag`. It's appropriate for: quickly saving manual changes you've made inside a container for experimentation, creating a checkpoint before making risky modifications, and prototyping a setup to figure out what commands are needed. However, it should NOT be the standard workflow for production images because: the process isn't reproducible (you can't see exactly what was done), there's no version history of changes, it can't be automated in CI/CD, and the resulting image has undefined provenance. Use it for exploration, then translate the steps into a proper Dockerfile.

---

**Q7. What are the three main Docker troubleshooting commands and when do you use each?**

**A:** (1) `docker logs container_name` — shows everything the application printed to stdout/stderr. Use when the container is behaving unexpectedly, exiting immediately, or throwing application errors. Use `-f` to follow logs in real time. (2) `docker inspect container_name` — returns complete JSON metadata: IP address, port bindings, volume mounts, environment variables, exit code, error messages. Use when you can't connect to a container (wrong IP/port), volumes aren't mounting, or a container crashed with no log output. The `--format` flag extracts specific fields. (3) `docker stats` — real-time CPU, memory, network, and disk I/O per container. Use when a container is slow, a server is overloaded, or you're investigating memory leaks. Start with logs, then inspect for infrastructure issues, then stats for resource problems.

---

**Q8. Why should you never run `docker system prune` in production without approval, and what's the safe approach?**

**A:** `docker system prune` removes stopped containers, unused networks, and dangling images. With `--volumes`, it also removes unused volumes — this can delete database data, log files, and application data stored in volumes. The removal is immediate and permanent — no recycle bin, no recovery. In production: (1) always run `docker system df` first to understand what will be affected and how much space is at stake; (2) get explicit manager/team approval; (3) prefer targeted cleanup over broad prune — `docker rm specific-container`, `docker rmi specific-image`; (4) schedule during maintenance windows; (5) ensure backups exist for any volumes you're about to prune. Production databases stored in Docker volumes can be permanently lost in seconds with a mistyped prune command.

---

**Q9. What is the difference between `docker save`/`docker load` and `docker export`/`docker import`?**

**A:** `docker save` and `docker load` work with **images** and preserve complete image history (all layers, metadata, tags). The restored image is identical to the original — you can push it to a registry, inspect its history, and use it exactly as before. `docker export` and `docker import` work with **containers** — they export the container's current filesystem as a flat archive with no layer history or metadata. The imported result is a new image with a single layer and no history. Use `save/load` when you need to transfer or backup a complete image with full fidelity. Use `export/import` when you only need a filesystem snapshot, or want to flatten an image's layers (reduces size but loses history).

---

← Previous: [`33_Container_Operations_Port_Mapping_Volumes_&_Management.md`](33_Container_Operations_Port_Mapping_Volumes_&_Management.md) | Next: [`35_Image_Optimization_Multi-Stage_Builds_Container_Registries_&_Docker_vs_Kubernetes.md`](35_Image_Optimization_Multi-Stage_Builds_Container_Registries_&_Docker_vs_Kubernetes.md) →