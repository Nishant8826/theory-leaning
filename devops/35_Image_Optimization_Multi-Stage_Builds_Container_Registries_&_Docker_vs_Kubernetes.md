# 35 – Docker Day 4: Image Optimization, Multi-Stage Builds, Container Registries & Docker vs Kubernetes

---

## Table of Contents

1. [Why Docker Image Optimization Matters](#1-why-docker-image-optimization-matters)
2. [Base Image Selection – The First Big Decision](#2-base-image-selection--the-first-big-decision)
3. [Dockerfile Best Practices for Smaller Images](#3-dockerfile-best-practices-for-smaller-images)
4. [Multi-Stage Dockerfiles – The Gold Standard](#4-multi-stage-dockerfiles--the-gold-standard)
5. [Container Registries – Beyond Docker Hub](#5-container-registries--beyond-docker-hub)
6. [Pushing to Google Container Registry (GCR)](#6-pushing-to-google-container-registry-gcr)
7. [Pushing to AWS ECR](#7-pushing-to-aws-ecr)
8. [Pushing to Azure Container Registry (ACR)](#8-pushing-to-azure-container-registry-acr)
9. [Docker Compose vs Kubernetes – When to Use What](#9-docker-compose-vs-kubernetes--when-to-use-what)
10. [Tech Stack Mapping](#10-tech-stack-mapping)
11. [Visual Diagrams](#11-visual-diagrams)
12. [Code & Practical Examples](#12-code--practical-examples)
13. [Scenario-Based Q&A](#13-scenario-based-qa)
14. [Interview Q&A](#14-interview-qa)

---

## 1. Why Docker Image Optimization Matters

### What
Docker image optimization is the practice of making your Docker images as **small, fast, and secure** as possible — without sacrificing functionality. An optimized image contains only what's absolutely necessary to run the application.

> 💡 **Analogy:** Imagine packing for a weekend trip. A bloated image is like packing every piece of clothing you own "just in case." An optimized image is a perfectly packed carry-on — everything you need, nothing you don't. The carry-on boards faster, costs less to check, and is easier to move around.

### Why It Matters — The Business Case

| Problem with Bloated Images | Cost |
|----------------------------|------|
| 1.14 GB image vs 188 MB image | 6x more storage cost in ECR/GCR/ACR |
| Large image = slow `docker pull` | CI/CD pipeline takes longer |
| Full OS + dev tools in production | Larger attack surface for vulnerabilities |
| More layers = more cache misses | Slower builds in Jenkins/GitHub Actions |
| High memory usage | More expensive cloud instances needed |

### The Real Numbers from Class

```
Bloated Image:
  Base: Ubuntu (~1.14 GB) + Python manually installed
  Total: ~1.2 GB+

Optimized Image:
  Base: python:3.11-slim (~188 MB)
  Total: ~200–250 MB

Savings: ~1 GB per image
         × 50 deployments/day
         × 10 microservices
         = Significant storage and bandwidth savings
```

### Benefits of Optimization

```
1. Reduced Storage Costs
   → Less data stored in ECR/GCR/Docker Hub
   → Lower S3/Cloud Storage bills

2. Faster CI/CD Pipelines
   → Faster docker pull on every deployment
   → Faster docker push in build pipelines
   → Faster container startup

3. Better Security
   → Fewer packages = fewer CVEs (known vulnerabilities)
   → No build tools in production (compilers can be exploited)
   → Smaller attack surface

4. Lower Memory Errors
   → Lean images use less RAM
   → More containers per node
   → Cost savings on Kubernetes clusters

5. Quicker Container Startup
   → Kubernetes pod startup faster
   → Faster auto-scaling response
```

---

## 2. Base Image Selection – The First Big Decision

### What
The `FROM` instruction is the single most impactful optimization decision. Your base image sets the floor for your final image size — everything you add builds on top of it.

### Why — The Size Difference Is Dramatic

| Base Image | Approximate Size | Use Case |
|-----------|-----------------|---------|
| `ubuntu:22.04` | ~77 MB (base) → ~1.14 GB after packages | ❌ Avoid for production |
| `debian:12` | ~117 MB | General Linux base |
| `debian:12-slim` | ~75 MB | Slimmed Debian — good choice |
| `alpine:3.18` | ~7 MB | Smallest common Linux — great for production |
| `python:3.11` | ~920 MB | Full Python (Debian-based) |
| `python:3.11-slim` | ~188 MB | Slim Python — recommended |
| `python:3.11-alpine` | ~48 MB | Smallest Python — best size |
| `node:18` | ~991 MB | Full Node.js |
| `node:18-slim` | ~245 MB | Slim Node.js |
| `node:18-alpine` | ~112 MB | Smallest Node.js — recommended |
| `openjdk:21-slim` | ~417 MB | Slim Java — good for Spring Boot |
| `nginx:alpine` | ~41 MB | NGINX on Alpine — excellent |
| `scratch` | 0 MB | For compiled static binaries only |

### The Three Image Variants Explained

#### Full Images (e.g., `python:3.11`)
- Based on full Debian
- Includes: compilers, build tools, package managers, debug utilities
- **When to use:** Never in production — only as build stages

#### Slim Images (e.g., `python:3.11-slim`)
- Based on Debian but strips non-essential packages
- Removes: documentation, locale files, some utilities
- **When to use:** Production runtime when you need some system libraries
- **Tradeoff:** Some packages that need compilation might fail

#### Alpine Images (e.g., `python:3.11-alpine`)
- Based on Alpine Linux — uses `musl libc` instead of `glibc`
- Extremely small (~5-50 MB base)
- **When to use:** Production when compatibility is verified
- **Tradeoff:** Some Python packages that rely on glibc behave differently, `pip install` may need `apk add build-base` for compiled packages
- **Package manager:** `apk` instead of `apt`

### Practical Comparison from Class

```bash
# Bloated Dockerfile (what NOT to do)
FROM ubuntu:22.04
RUN apt-get update && apt-get install -y python3 python3-pip
# Final image: ~1.14 GB 😱

# Optimized Dockerfile (what TO do)
FROM python:3.11-slim
# Final image: ~188 MB ✅ (83% smaller!)
```

### How to Check Available Tags

```bash
# Search Docker Hub for all tags of an image
# https://hub.docker.com/_/python/tags
# https://hub.docker.com/_/node/tags

# Check local image sizes
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
```

---

## 3. Dockerfile Best Practices for Smaller Images

### Practice 1: Combine RUN Commands (Reduce Layers)

Each `RUN` instruction creates a new image layer. Even if you delete files in a later `RUN`, the original layer (with those files) still exists — the image size doesn't decrease.

```dockerfile
# ❌ BAD — Creates 4 separate layers, files from update are still in layer 1
RUN apt-get update
RUN apt-get install -y curl wget
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*

# ✅ GOOD — One layer, files cleaned in the SAME RUN = actually smaller
RUN apt-get update && apt-get install -y --no-install-recommends curl wget && apt-get clean && rm -rf /var/lib/apt/lists/*
```

### Practice 2: Use `--no-install-recommends`

```dockerfile
# Without flag — installs package + all recommended packages (bloated)
RUN apt-get install -y curl

# With flag — installs only what's strictly required (leaner)
RUN apt-get install -y --no-install-recommends curl
```

### Practice 3: Use `COPY` Instead of `ADD`

```dockerfile
# ❌ ADD can download from URLs — creates unpredictable dependencies
ADD https://example.com/script.sh /app/

# ✅ COPY is explicit — only copies local files
COPY script.sh /app/
```

`ADD` has hidden behavior (auto-extracting archives, URL downloads) that can introduce unexpected files into your image. Use `COPY` for explicit, predictable behavior.

### Practice 4: Use `.dockerignore`

Just like `.gitignore` for Git, `.dockerignore` tells Docker which files NOT to include in the build context. This speeds up build time and prevents accidentally including sensitive files.

```
# .dockerignore
node_modules/
.git/
*.log
.env
.env.*
dist/
build/
__pycache__/
*.pyc
.DS_Store
README.md
tests/
docs/
coverage/
```

### Practice 5: Set a WORKDIR

```dockerfile
# ❌ BAD — No WORKDIR, files land in root /
COPY . /
RUN python server.py  # Where is it?!

# ✅ GOOD — Organized, predictable, easier to troubleshoot
WORKDIR /app
COPY . .
CMD ["python", "server.py"]
```

### Practice 6: Copy Dependencies Before Code

```dockerfile
# ❌ SLOW — Code change invalidates npm install cache
COPY . .
RUN npm install

# ✅ FAST — npm install cached unless package.json changes
COPY package*.json ./
RUN npm install
COPY . .           # Only this layer rebuilds when code changes
```

### Practice 7: Use Specific Version Tags

```dockerfile
# ❌ BAD — "latest" can change, breaking your build
FROM node:latest

# ✅ GOOD — Pinned version = reproducible builds
FROM node:18.20.2-alpine3.19
```

### Practice 8: Run as Non-Root User

```dockerfile
# Security best practice — don't run as root inside containers
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

# Verify
# docker run my-image whoami
# → appuser (not root)
```

### Summary Table

| Practice | Layer Impact | Size Impact | Security Impact |
|----------|-------------|------------|-----------------|
| Slim/Alpine base | N/A | ⬇️ Major | ✅ Better |
| Combine RUN with `&&` | ⬇️ Fewer | ⬇️ Smaller | ✅ Cleaner |
| `--no-install-recommends` | ⬇️ Fewer files | ⬇️ Smaller | ✅ Fewer packages |
| `.dockerignore` | N/A | ⬇️ Build context | ✅ No secrets leaked |
| `COPY` over `ADD` | N/A | N/A | ✅ Predictable |
| Dependency-first COPY | ✅ Cache hits | ⬇️ Build time | N/A |
| Non-root USER | N/A | N/A | ✅✅ Critical |

---

## 4. Multi-Stage Dockerfiles – The Gold Standard

### What
A **multi-stage Dockerfile** uses multiple `FROM` statements in a single file, creating separate build stages. Each stage can have a different base image. The key power: you can **copy artifacts from one stage to the next**, leaving behind everything else — including build tools, dev dependencies, and compilation files.

> 💡 **Analogy:** Imagine building a house. You use heavy construction equipment (cranes, concrete mixers, scaffolding) during construction. When the house is finished, you don't leave all that equipment inside. You remove it, and the residents move in. Multi-stage builds do the same: heavy build tools exist only in the build stage, the final image has only the finished "house" — the running application.

### Why Multi-Stage?

Without multi-stage, you face a dilemma:
- Include build tools → **large, insecure production image**
- Don't include build tools → **can't compile your application**

Multi-stage solves this by having TWO separate environments:
- **Build Stage:** Has all tools needed to compile/build (large, temporary)
- **Runtime Stage:** Has only what's needed to run (small, production-ready)

### How Multi-Stage Works

```dockerfile
# ═══ STAGE 1: BUILD ═══════════════════════════════════════
# Named "builder" — can be referenced by later stages
FROM node:18 AS builder

WORKDIR /app

# Install ALL dependencies (including dev)
COPY package*.json ./
RUN npm ci                   # Installs 500MB of node_modules

COPY . .
RUN npm run build            # Produces /app/dist/ (compiled output)

# node_modules = 500MB, source = 50MB, dist = 5MB
# Total builder stage: ~650MB (but we don't ship this!)

# ═══ STAGE 2: RUNTIME ═════════════════════════════════════
# Fresh start — only what we need to RUN
FROM node:18-alpine AS runtime

WORKDIR /app

# Install only production dependencies
COPY package*.json ./
RUN npm ci --only=production   # Much smaller, no dev tools

# Copy ONLY the compiled output from builder stage
COPY --from=builder /app/dist ./dist

# No node_modules from builder, no source code, no dev tools
# Total runtime image: ~150MB ✅

EXPOSE 3000
CMD ["node", "dist/server.js"]
```

### What `COPY --from=builder` Does

```
COPY --from=STAGE_NAME  SOURCE_IN_THAT_STAGE  DEST_IN_THIS_STAGE

COPY --from=builder /app/dist ./dist
         ↑               ↑          ↑
   "from the stage   "copy this   "put it here in
    named builder"    directory"   this stage"
```

Only the files you explicitly copy make it to the final image. Everything else in the build stage is discarded.

### Multi-Stage for Different Languages

#### Python (Compile Requirements + Run)

```dockerfile
# Stage 1: Build — compile Python wheels
FROM python:3.11 AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime — slim Python with pre-compiled packages
FROM python:3.11-slim AS runtime

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH=/root/.local/bin:$PATH
CMD ["python", "app.py"]
```

#### Java Spring Boot

```dockerfile
# Stage 1: Build the JAR
FROM maven:3.9-openjdk-21 AS builder

WORKDIR /app
COPY pom.xml .
RUN mvn dependency:resolve   # Cache dependencies

COPY src ./src
RUN mvn clean package -DskipTests

# Stage 2: Runtime — just the JDK and the JAR
FROM openjdk:21-slim AS runtime

WORKDIR /app
COPY --from=builder /app/target/*.jar app.jar

EXPOSE 8080
CMD ["java", "-jar", "app.jar"]
```

#### Go (Static Binary — Smallest Possible)

```dockerfile
# Stage 1: Build — full Go toolchain
FROM golang:1.22 AS builder

WORKDIR /app
COPY go.* ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 go build -o main .

# Stage 2: Runtime — literally nothing (scratch)
FROM scratch AS runtime

COPY --from=builder /app/main /main
EXPOSE 8080
CMD ["/main"]
# Final image: ~10MB! (just the static binary)
```

### Size Comparison: Single Stage vs Multi-Stage

```
Node.js Application

Single Stage (FROM node:18):
  base image:    991 MB
  node_modules:  +500 MB (all dev + prod)
  source code:   +50 MB
  build output:  +10 MB
  Total: ~1.55 GB 😱

Multi-Stage (builder=node:18, runtime=node:18-alpine):
  runtime base:  112 MB (alpine)
  prod only deps: +100 MB
  dist only:     +5 MB
  Total: ~217 MB ✅ (86% smaller!)
```

---

## 5. Container Registries – Beyond Docker Hub

### What
A **container registry** is a storage and distribution system for Docker images. It's where images live between being built and being deployed. Different cloud providers have their own registries optimized for their ecosystems.

### Why Multiple Registries Exist

| Scenario | Best Registry |
|----------|--------------|
| Open source / learning | Docker Hub |
| Deploying to AWS (ECS, EKS, Lambda) | AWS ECR |
| Deploying to GCP (GKE, Cloud Run) | Google GCR / Artifact Registry |
| Deploying to Azure (AKS, Container Apps) | Azure ACR |
| Enterprise (any cloud) | All have private registry options |
| Self-hosted | Harbor, Nexus, GitLab Registry |

### Why Not Just Use Docker Hub for Everything?

| Issue | Docker Hub | Cloud Registries (ECR/GCR/ACR) |
|-------|-----------|-------------------------------|
| **Pull rate limits** | 100 pulls/6h (free) | Unlimited within the cloud |
| **Network speed** | External internet | Internal network (fast, free) |
| **Security/Private** | Limited free private repos | Built-in IAM integration |
| **Scanning** | Limited | Built-in vulnerability scanning |
| **Cost at scale** | Gets expensive | Included in cloud pricing |
| **Latency** | Higher (external) | Low (same region) |

---

## 6. Pushing to Google Container Registry (GCR)

### What
GCR (now evolving into Artifact Registry) is Google Cloud's managed container image registry. Images stored in GCR are in the same network as GKE clusters — fast pulls, no egress costs.

### Step-by-Step GCR Push

#### Step 1: Authenticate with Google Cloud
```bash
# Login to your Google account
gcloud auth login
# Opens browser for authentication

# Verify which account is logged in
gcloud auth list
```

#### Step 2: Set Your GCP Project
```bash
# List your projects
gcloud projects list

# Set the active project
gcloud config set project YOUR_PROJECT_ID
# Example: gcloud config set project my-devops-project-123456

# Verify
gcloud config get-value project
```

#### Step 3: Configure Docker to Use GCR
```bash
# This allows Docker to authenticate with GCR using gcloud credentials
gcloud auth configure-docker

# For specific regional registries:
gcloud auth configure-docker us-central1-docker.pkg.dev
```

#### Step 4: Build Your Image
```bash
docker build -t my-app .
```

#### Step 5: Tag for GCR

GCR image names follow this format:
```
gcr.io/PROJECT_ID/IMAGE_NAME:TAG
```

```bash
# For GCR (Container Registry):
docker tag my-app gcr.io/your-project-id/my-app:latest
docker tag my-app gcr.io/your-project-id/my-app:v1.0

# For Artifact Registry (newer GCP registry):
docker tag my-app us-central1-docker.pkg.dev/your-project-id/your-repo/my-app:latest
```

#### Step 6: Push to GCR
```bash
docker push gcr.io/your-project-id/my-app:latest
docker push gcr.io/your-project-id/my-app:v1.0
```

#### Step 7: Verify in GCP Console
```
GCP Console → Container Registry (or Artifact Registry) → your-project → images
```

#### Step 8: Pull and Test
```bash
# Pull from GCR on any authenticated machine
docker pull gcr.io/your-project-id/my-app:latest
docker run -d -p 3000:3000 gcr.io/your-project-id/my-app:latest
```

### GCR Regional Registries

| Hostname | Region |
|----------|--------|
| `gcr.io` | US (multi-region) |
| `us.gcr.io` | United States |
| `eu.gcr.io` | European Union |
| `asia.gcr.io` | Asia |

---

## 7. Pushing to AWS ECR

### What
Amazon Elastic Container Registry (ECR) is AWS's managed container registry, deeply integrated with ECS, EKS, Lambda, and CodePipeline.

### Step-by-Step ECR Push

#### Step 1: Create ECR Repository in AWS Console
```
AWS Console → ECR → Create repository
  Name: my-app
  Visibility: Private
  Scan on push: Enable (free vulnerability scanning!)
  → Create
```

Or via CLI:
```bash
aws ecr create-repository --repository-name my-app --region us-east-1
```

#### Step 2: Authenticate Docker with ECR
```bash
# Get login token and pipe to docker login
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# Token is valid for 12 hours
```

#### Step 3: Tag for ECR

ECR image names follow:
```
ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/REPO_NAME:TAG
```

```bash
# Get your account ID
aws sts get-caller-identity --query Account --output text

# Tag
docker tag my-app:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/my-app:latest

docker tag my-app:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/my-app:v1.0
```

#### Step 4: Push to ECR
```bash
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/my-app:latest
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/my-app:v1.0
```

#### Step 5: Verify
```
AWS Console → ECR → my-app → Images
```

---

## 8. Pushing to Azure Container Registry (ACR)

### What
Azure Container Registry (ACR) is Microsoft's managed container registry, integrated with AKS, Azure Container Apps, and Azure DevOps.

### Step-by-Step ACR Push

#### Step 1: Create ACR in Azure Portal
```
Azure Portal → Container Registries → Create
  Registry name: mycompanyregistry  (must be globally unique)
  Resource group: my-rg
  Location: East US
  SKU: Basic (learning) / Standard (production)
  → Create
```

Or via CLI:
```bash
az group create --name my-rg --location eastus

az acr create --resource-group my-rg --name mycompanyregistry --sku Basic
```

#### Step 2: Login to ACR
```bash
az acr login --name mycompanyregistry
# Login Succeeded ✅
```

#### Step 3: Tag for ACR

ACR image names follow:
```
REGISTRY_NAME.azurecr.io/IMAGE_NAME:TAG
```

```bash
docker tag my-app mycompanyregistry.azurecr.io/my-app:latest
docker tag my-app mycompanyregistry.azurecr.io/my-app:v1.0
```

#### Step 4: Push
```bash
docker push mycompanyregistry.azurecr.io/my-app:latest
```

#### Step 5: Verify
```bash
az acr repository list --name mycompanyregistry --output table
az acr repository show-tags --name mycompanyregistry --repository my-app
```

---

## 9. Docker Compose vs Kubernetes – When to Use What

### What They Are

| | Docker Compose | Kubernetes |
|--|----------------|-----------|
| **What** | Tool to define and run multi-container applications using a YAML file | Container orchestration platform for managing containers at scale |
| **Scale** | Single machine | Multiple machines (clusters) |
| **Learning curve** | Easy | Steep |
| **Setup time** | Minutes | Hours/Days |

### Detailed Comparison

| Feature | Docker Compose | Kubernetes |
|---------|---------------|-----------|
| **Multi-container apps** | ✅ Yes | ✅ Yes |
| **Single machine** | ✅ Best use case | ⚠️ Overkill |
| **Multiple nodes/machines** | ❌ No | ✅ Built for this |
| **Auto-scaling** | ❌ Manual | ✅ Horizontal Pod Autoscaler |
| **Self-healing** | ❌ No | ✅ Restarts failed pods automatically |
| **Zero-downtime deploys** | ❌ No | ✅ Rolling updates |
| **Load balancing** | ⚠️ Basic | ✅ Advanced |
| **Service discovery** | ✅ By service name | ✅ DNS-based |
| **Health checks** | ✅ Basic | ✅ Liveness + Readiness probes |
| **Rollbacks** | ❌ Manual | ✅ `kubectl rollout undo` |
| **Multi-cloud/region** | ❌ No | ✅ Yes |
| **Monitoring** | ❌ Basic | ✅ Prometheus, Grafana integration |
| **Secret management** | ✅ Basic env vars | ✅ Kubernetes Secrets + Vault |
| **Production ready** | ⚠️ Dev/staging only | ✅ Industry standard |
| **Industry standard** | Dev/QA environments | Production everywhere |

### When to Use Each

```
Docker Compose:
  ✅ Local development environment
  ✅ Running multiple services on a single server
  ✅ Simple staging environments
  ✅ Development team testing
  ✅ When you have 1 machine and < 10 containers
  ❌ NOT for production at scale

Kubernetes:
  ✅ Production workloads
  ✅ Microservices architecture
  ✅ High availability requirements
  ✅ Auto-scaling needs
  ✅ Multi-team, multi-service environments
  ✅ When containers need to run across multiple machines
  ✅ When you need zero-downtime deployments
```

### The Journey from Docker to Kubernetes

```
Development:      Docker (build + run locally)
                         │
                         ▼
Testing/Staging:  Docker Compose (run all services together)
                         │
                         ▼
Production:       Kubernetes (orchestrate at scale)
```

---

## 10. Tech Stack Mapping

### Optimized Docker Images in a Full DevOps Pipeline

```
Developer writes application code
          │ git push
          ▼
GitHub Repository
  ├── src/
  ├── Dockerfile          ← Multi-stage, slim base
  ├── .dockerignore       ← Excludes node_modules, .git, .env
  └── Jenkinsfile
          │
          ▼
Jenkins CI Pipeline:
  Stage 1: git clone
  Stage 2: docker build (multi-stage — only runtime stage shipped)
  Stage 3: docker tag for ECR/GCR/ACR
  Stage 4: docker push to registry
  Stage 5: Deploy (Kubernetes / ECS pull from registry)
          │
          ▼
Container Registry (ECR / GCR / ACR)
  → Image: 150MB (was 1.5GB)
  → Pull time: 5 seconds (was 60 seconds)
  → Vulnerability scan: 0 critical CVEs
          │
          ▼
Production Kubernetes Cluster
  → Fast pod startup
  → More pods per node (efficient resources)
  → Secure runtime (no build tools exposed)
```

### Real Application Stack with Optimized Images

| Service | Bloated Image | Optimized Image | Savings |
|---------|--------------|-----------------|---------|
| Node.js API | `node:18` = 991 MB | `node:18-alpine` = 112 MB | 88% |
| Python ML service | `ubuntu` + python = 1.14 GB | `python:3.11-slim` = 188 MB | 84% |
| React frontend | `node:18` = 991 MB | Multi-stage → `nginx:alpine` = 41 MB | 96% |
| Spring Boot API | `openjdk:21` = 470 MB | Multi-stage → `openjdk:21-slim` = 417 MB | 11% |
| PostgreSQL | Standard: 376 MB | `postgres:16-alpine` = 234 MB | 38% |

---

## 11. Visual Diagrams

### Diagram 1: Single Stage vs Multi-Stage Build

```
SINGLE STAGE                            MULTI-STAGE
─────────────                           ────────────

FROM node:18 (991MB)                    ┌─────────────────────────────┐
  ↓                                     │  STAGE 1: BUILD             │
Install all packages                    │  FROM node:18 (991MB)       │
  ↓                                     │  npm install (+ dev deps)   │
Copy all code                           │  npm run build              │
  ↓                                     │  → /dist output             │
Build                                   └───────────────┬─────────────┘
  ↓                                                     │ COPY --from=builder
FINAL IMAGE: ~1.5 GB ❌                                 ↓ /dist only
                                        ┌─────────────────────────────┐
                                        │  STAGE 2: RUNTIME           │
                                        │  FROM node:18-alpine (112MB)│
                                        │  npm install --only=prod    │
                                        │  COPY /dist from builder    │
                                        └─────────────────────────────┘
                                        FINAL IMAGE: ~217 MB ✅
                                        (86% smaller!)
```

---

### Diagram 2: Layer Optimization – Combining RUN Commands

```
BAD — 4 layers, files never truly deleted:
──────────────────────────────────────────
Layer 1: apt-get update  → adds 50MB of package lists
Layer 2: apt-get install → adds 200MB of packages
Layer 3: apt-get clean   → appears to clean, but Layer 1 still has the data
Layer 4: rm -rf ...      → same issue

Total: 250MB (can't reclaim Layer 1 data even though "cleaned")

GOOD — 1 layer, actually clean:
────────────────────────────────
Layer 1: apt-get update && apt-get install && apt-get clean && rm -rf
         → Everything done in ONE layer
         → No intermediate bloat
         → Files actually removed from this layer

Total: ~80MB (only what you need) ✅
```

---

### Diagram 3: Base Image Size Hierarchy

```
                    SIZE (approximate)
scratch             ████ 0 MB        ← Static binary only
alpine:3.18         ████ 7 MB        ← Smallest full Linux
nginx:alpine        ████████ 41 MB   ← NGINX on Alpine
node:18-alpine      █████████████ 112 MB   ← Node.js on Alpine
python:3.11-slim    ████████████████ 188 MB ← Slim Debian + Python
node:18-slim        ███████████████████ 245 MB
openjdk:21-slim     ████████████████████████ 417 MB
debian:12           ███████████████████████████ ~620 MB
python:3.11         ████████████████████████████████ 920 MB
node:18             █████████████████████████████████ 991 MB
ubuntu:22.04 + pkg  ████████████████████████████████████ 1.14+ GB ❌
```

---

### Diagram 4: Container Registry Ecosystem

```
                    ┌──────────────────┐
                    │   Docker Build   │
                    │ docker build .   │
                    └────────┬─────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │  Docker Hub  │ │  AWS ECR     │ │  GCR / GAR   │
    │ hub.docker   │ │ ACCOUNT.dkr  │ │ gcr.io/      │
    │ .com         │ │ .ecr.REGION  │ │ PROJECT/     │
    │              │ │ .amazonaws   │ │ IMAGE        │
    │ Public repos │ │ .com/REPO    │ │              │
    │ Free tier    │ │ IAM-secured  │ │ gcloud auth  │
    │              │ │              │ │              │
    └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
           │                │                │
           └────────────────┴────────────────┘
                            │
                   ┌────────▼────────┐
                   │   Kubernetes /  │
                   │   ECS / Cloud   │
                   │   Run          │
                   │ (docker pull)   │
                   └─────────────────┘

    Also: Azure ACR → azurecr.io/REGISTRY/IMAGE
```

---

### Diagram 5: Docker Compose vs Kubernetes

```
DOCKER COMPOSE                         KUBERNETES
──────────────                         ──────────
Single machine                         Multiple machines (cluster)
      │                                      │
  service A ──┐                      Node 1: Pod A, Pod B
  service B ──┤ one server           Node 2: Pod C, Pod D
  service C ──┘                      Node 3: Pod E, Pod F

Manual scaling                        Auto-scaling
  docker-compose scale web=3            kubectl scale --replicas=10
  (manual, one machine)                 (auto, across all nodes)

If container crashes:                 If pod crashes:
  Stays dead until you restart          Kubernetes auto-restarts it
                                        in < 30 seconds

Zero-downtime deploy:                 Zero-downtime deploy:
  Not built-in                          kubectl rollout update
  Must script manually                  Rolling update built-in

Good for:                             Good for:
  Dev, staging, single-server           Production, scale, HA
  Simple setups                         Microservices at scale
```

---

### Diagram 6: Multi-Stage Python Build Flow

```
Stage 1 "builder":           Stage 2 "runtime":
FROM python:3.11             FROM python:3.11-slim
   │                              │
   │ pip install                  │ COPY --from=builder /root/.local
   │ (compiles packages)          │ (pre-compiled wheels only)
   │                              │
   │ /root/.local ─────────────►  │ COPY app.py
   │ (compiled wheels)            │
   │                              │ CMD ["python", "app.py"]
   │                              │
   │ ~920 MB (discarded)          │ ~230 MB ✅
```

---

## 12. Code & Practical Examples

### Example 1: Bloated vs Optimized Dockerfile (Python) — From Class

```dockerfile
# ═══════════════════════════════════════════
# BLOATED VERSION — DO NOT USE IN PRODUCTION
# ═══════════════════════════════════════════
FROM ubuntu:22.04

RUN apt-get update
RUN apt-get install -y python3 python3-pip curl wget git
RUN apt-get install -y build-essential
# Installing build-essential adds compilers not needed at runtime
# Using Ubuntu base: ~1.14 GB before we add anything
# Final size: ~1.3+ GB 😱

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . /app
WORKDIR /app
CMD ["python3", "app.py"]

# ═══════════════════════════════════════════
# OPTIMIZED VERSION — USE THIS IN PRODUCTION
# ═══════════════════════════════════════════
FROM python:3.11-slim

# Single RUN = single layer + cleanup in same layer
RUN apt-get update && apt-get install -y --no-install-recommends curl && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy dependencies first (layer cache optimization)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
# Final size: ~220 MB ✅ (83% smaller!)

CMD ["python", "app.py"]
```

Build and compare:
```bash
docker build -f Dockerfile.bloated -t my-app:bloated .
docker build -f Dockerfile.optimized -t my-app:optimized .
docker images | grep my-app
# my-app   bloated      1.31GB
# my-app   optimized    218MB
```

---

### Example 2: Multi-Stage Node.js from Class

```dockerfile
# Two-stage Dockerfile for Node.js application

# ════ Stage 1: Prepare the Application ════════════════════
FROM node:18 AS builder

LABEL stage="builder"

WORKDIR /app

# Install all dependencies (including dev)
COPY package*.json ./
RUN npm ci

# Copy source and build
COPY . .
RUN npm run build
# This produces /app/dist/ — compiled, optimized output

# ════ Stage 2: Run the Application ═════════════════════════
FROM node:18-alpine AS runtime

LABEL stage="runtime"
LABEL maintainer="devops@company.com"
LABEL version="1.0.0"

WORKDIR /app

# Only production dependencies
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

# Copy only compiled output from builder
COPY --from=builder /app/dist ./dist

# Security: run as non-root
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=3s --retries=3 CMD wget -qO- http://localhost:3000/health || exit 1

CMD ["node", "dist/server.js"]
```

---

### Example 3: Multi-Stage Spring Boot

```dockerfile
# ════ Stage 1: Maven Build ══════════════════════════════════
FROM maven:3.9-openjdk-21-slim AS builder

WORKDIR /app

# Cache Maven dependencies (only re-downloads if pom.xml changes)
COPY pom.xml .
RUN mvn dependency:go-offline -B

# Copy source and build JAR
COPY src ./src
RUN mvn clean package -DskipTests -B

# ════ Stage 2: Runtime ══════════════════════════════════════
FROM openjdk:21-slim AS runtime

WORKDIR /app

# Create non-root user
RUN addgroup --system appgroup && adduser --system --group appuser
USER appuser

# Copy only the JAR from builder
COPY --from=builder /app/target/*.jar app.jar

EXPOSE 8080

# JVM tuning for containers
ENV JAVA_OPTS="-Xms256m -Xmx512m -XX:+UseContainerSupport"

HEALTHCHECK --interval=30s --timeout=10s --retries=3 CMD curl -f http://localhost:8080/actuator/health || exit 1

CMD ["sh", "-c", "java $JAVA_OPTS -jar app.jar"]
```

---

### Example 4: Jenkins Pipeline – Build Optimized Image and Push to ECR + GCR

```groovy
pipeline {
    agent any

    environment {
        AWS_ACCOUNT_ID    = credentials('aws-account-id')
        AWS_REGION        = 'us-east-1'
        GCP_PROJECT_ID    = credentials('gcp-project-id')
        ECR_REPO          = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/my-app"
        GCR_REPO          = "gcr.io/${GCP_PROJECT_ID}/my-app"
        IMAGE_TAG         = "${BUILD_NUMBER}"
    }

    stages {

        stage('Clone') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/yourname/my-app.git'
            }
        }

        stage('Docker Build (Multi-Stage)') {
            steps {
                sh """
                    docker build --target runtime -t my-app:${IMAGE_TAG} -t my-app:latest .
                    docker images my-app
                """
            }
        }

        stage('Push to AWS ECR') {
            steps {
                sh """
                    # Authenticate
                    aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REPO}

                    # Tag and push
                    docker tag my-app:${IMAGE_TAG} ${ECR_REPO}:${IMAGE_TAG}
                    docker tag my-app:${IMAGE_TAG} ${ECR_REPO}:latest
                    docker push ${ECR_REPO}:${IMAGE_TAG}
                    docker push ${ECR_REPO}:latest
                """
            }
        }

        stage('Push to GCR') {
            steps {
                sh """
                    # Authenticate (assumes gcloud is installed and configured)
                    gcloud auth configure-docker --quiet

                    # Tag and push
                    docker tag my-app:${IMAGE_TAG} ${GCR_REPO}:${IMAGE_TAG}
                    docker tag my-app:${IMAGE_TAG} ${GCR_REPO}:latest
                    docker push ${GCR_REPO}:${IMAGE_TAG}
                    docker push ${GCR_REPO}:latest
                """
            }
        }

        stage('Cleanup Local Images') {
            steps {
                sh """
                    docker rmi my-app:${IMAGE_TAG} || true
                    docker rmi my-app:latest || true
                    docker image prune -f
                """
            }
        }
    }

    post {
        success {
            echo "✅ Image ${IMAGE_TAG} pushed to ECR and GCR!"
        }
        failure {
            echo "❌ Build/push failed — check logs"
        }
    }
}
```

---

### Example 5: React/Next.js Multi-Stage (Static → NGINX)

```dockerfile
# ════ Stage 1: Build React/Next.js app ═════════════════════
FROM node:18-alpine AS builder

WORKDIR /app

# Cache dependencies
COPY package*.json ./
RUN npm ci

COPY . .

# Build for production
RUN npm run build
# Next.js produces: /app/.next/ and /app/out/ (static export)

# ════ Stage 2: Serve with NGINX (41 MB!) ═══════════════════
FROM nginx:alpine AS runtime

# Remove default NGINX site
RUN rm -rf /usr/share/nginx/html/*

# Copy built static files from builder
COPY --from=builder /app/out /usr/share/nginx/html

# Custom NGINX config for SPA routing
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

# Final image: ~50 MB (was ~1 GB with Node.js base!)
```

`nginx.conf` for SPA:
```nginx
server {
    listen 80;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    gzip on;
    gzip_types text/html text/css application/javascript;
}
```

---

### Example 6: .dockerignore for Node.js Projects

```
# .dockerignore — always create this file!

# Dependencies (built inside container)
node_modules/
npm-debug.log
yarn-error.log

# Git history (not needed in container)
.git/
.gitignore

# Environment files (NEVER in container)
.env
.env.*
.env.local
.env.production

# Build output (rebuilt inside container)
dist/
build/
.next/
out/

# Test files (not needed in production image)
tests/
__tests__/
*.test.js
*.spec.js
coverage/

# Documentation
README.md
docs/
*.md

# IDE files
.vscode/
.idea/
*.swp
.DS_Store

# Docker files themselves
Dockerfile*
docker-compose*
.dockerignore
```

---

## 13. Scenario-Based Q&A

---

🔍 **Scenario 1:** Your Jenkins CI/CD pipeline takes 18 minutes per run because `docker pull` downloads a 1.4 GB image every time. Your manager wants it under 5 minutes. What do you do?

✅ **Answer:** Optimize the Docker image in two steps: (1) Switch the base image — from `FROM ubuntu:22.04` to `FROM python:3.11-slim` or `FROM node:18-alpine` depending on the runtime. This alone can cut image size by 80-85%; (2) Implement a multi-stage Dockerfile — keep all build tools in a builder stage, copy only the compiled artifact to a slim runtime stage. A 1.4 GB image typically becomes 150-250 MB. Docker pull of 200 MB completes in ~10-20 seconds even on a slow connection. Total pipeline time should drop from 18 minutes to under 4 minutes — and subsequent builds are faster due to layer caching.

---

🔍 **Scenario 2:** A security audit found 47 critical CVEs (known vulnerabilities) in your production Docker images. Most come from packages you don't use. How do you address this?

✅ **Answer:** The root cause is using a bloated base image — full Ubuntu or Debian images include hundreds of packages, each a potential vulnerability. The fix: (1) Switch to `slim` or `alpine` base images — Alpine has ~10% of the packages of Ubuntu, dramatically fewer CVEs; (2) Use multi-stage builds — your build tools (compilers, npm, pip) never appear in the final runtime image, eliminating entire vulnerability categories; (3) Combine and clean RUN commands — don't leave package manager caches in layers; (4) Enable `--no-install-recommends` for apt. Enable ECR's "Scan on push" or GCR's Container Analysis for automatic CVE scanning on every push. After optimization, expect CVE count to drop from 47 to 3-5 or even zero.

---

🔍 **Scenario 3:** Your company has three deployment targets: AWS (ECS), GCP (Cloud Run), and Azure (Container Apps). The DevOps team pushes images manually to each registry. This takes an hour per release. How do you automate this?

✅ **Answer:** Create a single Jenkins pipeline with parallel push stages using `parallel {}` in the Jenkinsfile. Build the image once, tag it three ways, then push to all three registries in parallel:
```groovy
stage('Push to Registries') {
    parallel {
        stage('ECR') { steps { sh 'docker push ${ECR_REPO}:${TAG}' } }
        stage('GCR') { steps { sh 'docker push ${GCR_REPO}:${TAG}' } }
        stage('ACR') { steps { sh 'docker push ${ACR_REPO}:${TAG}' } }
    }
}
```
All three pushes happen simultaneously. Store cloud credentials securely in Jenkins Credentials Store. This reduces multi-registry deployment from 1 hour to 5-10 minutes.

---

🔍 **Scenario 4:** A developer on your team is using `FROM ubuntu:22.04` as the base for a Python application, then manually installing Python 3.11 with `apt-get`. The resulting image is 1.14 GB. How do you explain the better approach?

✅ **Answer:** Show them the direct comparison:
```dockerfile
# Their approach: Ubuntu + manual Python = 1.14 GB
FROM ubuntu:22.04
RUN apt-get update && apt-get install -y python3.11 python3-pip

# Better: Official Python slim = 188 MB (83% smaller!)
FROM python:3.11-slim
```
The official `python:3.11-slim` image IS Ubuntu/Debian but already has Python installed and pre-configured, without the overhead of installing it manually. It's also maintained by the Python Docker community — always up-to-date and secure. The manual approach also risks getting a slightly different Python version or missing configuration that `FROM python:3.11-slim` handles correctly.

---

🔍 **Scenario 5:** Your team's `docker build` takes 15 minutes because `npm install` (which downloads 500MB) runs on every single build, even for a one-line code change. How do you fix this with layer caching?

✅ **Answer:** Reorder the Dockerfile to copy `package.json` and run `npm install` BEFORE copying the application code:
```dockerfile
# SLOW — code change = npm install runs every time
COPY . .
RUN npm install

# FAST — npm install runs only when package.json changes
COPY package*.json ./
RUN npm install       # Cached unless package.json changes ✅
COPY . .              # Only this layer rebuilds for code changes
```
Docker caches each layer. Since `package.json` rarely changes (only when adding/removing dependencies), `npm install` runs from cache 95%+ of the time. Build time drops from 15 minutes to 30-60 seconds for typical code changes.

---

🔍 **Scenario 6:** Your startup is moving from a single server (managed with Docker Compose) to multiple servers because you're expecting a traffic spike. Your manager asks if you should just run Docker Compose on more servers manually. What do you recommend?

✅ **Answer:** Recommend migrating to **Kubernetes**. Running Docker Compose on multiple servers manually has critical problems: you'd have to manually SSH into each server to deploy, no automatic load balancing between servers, if a container crashes it stays dead until you fix it manually, no automatic scaling when traffic spikes, and no coordination between servers. Kubernetes solves all of this: single command deployment across all nodes (`kubectl apply`), automatic load balancing and service discovery, self-healing (crashed pods restart automatically in < 30 seconds), Horizontal Pod Autoscaler handles traffic spikes, and rolling updates for zero-downtime deployments. The transition is worth the learning curve at production scale.

---

## 14. Interview Q&A

---

**Q1. What is Docker image optimization and what are its main benefits?**

**A:** Docker image optimization is the practice of reducing image size, build time, and attack surface while maintaining full functionality. Main benefits: (1) **Storage cost reduction** — smaller images cost less to store in ECR/GCR/ACR and less to transfer; (2) **Faster deployments** — smaller images pull faster, speeding up CI/CD pipelines and container startup; (3) **Security improvement** — fewer packages means fewer CVEs (known vulnerabilities); every package removed is one less attack vector; (4) **Resource efficiency** — lean containers use less memory, allowing more pods per node in Kubernetes; (5) **Faster builds** — proper layer ordering enables aggressive caching. The primary techniques are: slim/alpine base images, multi-stage builds, combining RUN commands, and proper `.dockerignore` usage.

---

**Q2. What is a multi-stage Dockerfile and when would you use it?**

**A:** A multi-stage Dockerfile uses multiple `FROM` statements in one file, creating separate build phases. Files can be selectively copied between stages using `COPY --from=STAGE_NAME`. The classic pattern: a "builder" stage with a full image (Maven, Node.js with dev dependencies) compiles the application, and a "runtime" stage with a slim image copies only the compiled output. Everything in the builder stage — compilers, dev tools, test libraries — is discarded. Use it when: your application needs compilation (Java, TypeScript, Go, Rust), your language has separate dev and prod dependencies (Node.js), you want to serve a frontend with NGINX instead of Node.js, or any time the build environment should be different from the runtime environment — which is almost always in production.

---

**Q3. What is the difference between `alpine`, `slim`, and full Docker base images?**

**A:** Three variants exist for most official images: **Full** (e.g., `python:3.11`, `node:18`) is based on full Debian — includes compilers, build tools, documentation. ~900MB-1GB+. For build stages only. **Slim** (e.g., `python:3.11-slim`, `node:18-slim`) is stripped Debian — removes documentation, locale files, non-essential utilities. ~200-250MB. Good production choice for most apps. **Alpine** (e.g., `python:3.11-alpine`, `node:18-alpine`) is based on Alpine Linux with musl libc instead of glibc. ~50-120MB. Smallest option but some Python packages that need glibc require extra setup (`apk add build-base`). Best choice when you verify compatibility. Alpine also uses `apk` package manager instead of `apt`. The recommendation: use Alpine if compatibility is confirmed, otherwise use Slim.

---

**Q4. How does layer caching work in Docker and how do you optimize for it?**

**A:** Every Dockerfile instruction creates a layer. Docker caches each layer and reuses cached layers if neither the instruction NOR any previous layer has changed. When a layer changes, all layers after it must rebuild. The optimization rule: **put things that change rarely near the top, things that change often near the bottom**. Practical application for Node.js:
```
# Cached most builds (package.json rarely changes):
COPY package*.json ./
RUN npm install

# Only this rebuilds when code changes:
COPY . .
```
This pattern means a typical code change (no new dependencies) rebuilds only the last COPY layer — taking seconds instead of minutes. The same principle applies to all runtimes: copy `pom.xml` before `src/` for Maven, copy `requirements.txt` before application code for Python.

---

**Q5. How do you push a Docker image to Google Container Registry (GCR)?**

**A:** Four-step process: (1) Authenticate: `gcloud auth login` then `gcloud auth configure-docker`; (2) Set your project: `gcloud config set project YOUR_PROJECT_ID`; (3) Tag with GCR format: `docker tag local-image gcr.io/PROJECT_ID/IMAGE_NAME:TAG`; (4) Push: `docker push gcr.io/PROJECT_ID/IMAGE_NAME:TAG`. The GCR image name format is `gcr.io/PROJECT_ID/IMAGE_NAME:TAG`. For regional registries, use `us.gcr.io`, `eu.gcr.io`, or `asia.gcr.io`. For the newer Artifact Registry: `REGION-docker.pkg.dev/PROJECT_ID/REPO/IMAGE:TAG`. In Jenkins, use a service account key stored in credentials and `gcloud auth activate-service-account --key-file=KEY_FILE` for non-interactive authentication.

---

**Q6. What are the key differences between Docker Compose and Kubernetes?**

**A:** Docker Compose manages multiple containers on a **single machine** using a YAML file — simple, fast to set up, great for development and single-server setups. Kubernetes is a full **container orchestration platform** for managing containers across **multiple machines** (a cluster). Key Kubernetes advantages: automatic self-healing (restarts failed containers), horizontal auto-scaling based on CPU/memory, zero-downtime rolling deployments, multi-node load balancing, built-in service discovery, multi-cloud and multi-region support. Compose is appropriate for local development, simple staging, or single-server deployments. Kubernetes is the industry standard for production workloads with high-availability requirements. The path: Docker locally → Compose for staging → Kubernetes for production.

---

**Q7. Why should you use `COPY` instead of `ADD` in Dockerfiles?**

**A:** Both copy files into an image, but `ADD` has extra behaviors that can cause issues: it auto-extracts tar archives (potentially adding unexpected files) and can download from URLs (creating external dependencies at build time, security risk). `COPY` is explicit — it only copies local files. The Docker documentation itself recommends `COPY` unless you specifically need `ADD`'s archive extraction feature. In practice: use `COPY` for copying files and directories. Use `ADD` only when you intentionally need to auto-extract a local tar archive — never for URL downloads (use `RUN curl` instead, which is explicit and traceable in the build log).

---

**Q8. What is the `--no-install-recommends` flag and why does it matter?**

**A:** When you run `apt-get install -y package`, Debian/Ubuntu installs the package AND all its "recommended" packages — these are optional packages the maintainer thinks you might want. Many recommended packages are unnecessary in a Docker container (documentation, GUI tools, optional utilities). The `--no-install-recommends` flag skips recommended packages: `apt-get install -y --no-install-recommends curl`. This typically saves 20-50 MB per install command. Combined with `apt-get clean && rm -rf /var/lib/apt/lists/*` in the same RUN layer, it keeps the image as lean as possible. This matters at scale: 10 microservices each saving 50 MB = 500 MB of unnecessary storage and transfer costs eliminated.

---

**Q9. How do you handle credentials securely when pushing to multiple container registries in a Jenkins pipeline?**

**A:** Never hardcode credentials in Jenkinsfiles or environment variables in plain text. Use Jenkins Credentials Store: (1) For AWS ECR — store an IAM user's access key and secret as "AWS Credentials" type in Jenkins, reference with `withCredentials([aws(...)])`; (2) For GCP GCR — store a service account JSON key as a "Secret File," use `gcloud auth activate-service-account --key-file=$KEY_FILE`; (3) For Azure ACR — store service principal credentials as username/password. In the pipeline, credentials appear as `****` in logs. Additionally: use IAM roles instead of user credentials where possible (Jenkins EC2 instance role for ECR access needs no stored credentials), rotate credentials regularly, and scope permissions minimally — the Jenkins service account should only have push access to specific repositories, not admin access to the entire registry.

---


← Previous: [`34_Dockerfiles_Custom_Images_Docker_Hub_&_Troubleshooting.md`](34_Dockerfiles_Custom_Images_Docker_Hub_&_Troubleshooting.md) | Next: [`36_KubernetesIntroduction_Architecture_Clusters_Namespaces_&_kubectl.md`](36_KubernetesIntroduction_Architecture_Clusters_Namespaces_&_kubectl.md) →