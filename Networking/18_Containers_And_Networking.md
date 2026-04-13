# Containers & Networking

> 📌 **File:** 18_Containers_And_Networking.md | **Level:** Full-Stack Dev → Networking Expert

---

## What is it?

Docker containers package your Node.js app with its dependencies into an isolated environment. Container networking determines how containers talk to each other, to the host, and to the internet. Understanding this is essential when deploying with ECS, Docker Compose, or Kubernetes.

---

## Map it to MY STACK (CRITICAL)

```
Your local development:
  Node.js (:3000) → MongoDB (:27017) → Redis (:6379)
  All on localhost — networking is trivial.

Docker development:
  ┌────────────────────────────────────────┐
  │  Docker Network: app-network           │
  │                                        │
  │  ┌──────────┐  ┌─────────┐  ┌───────┐│
  │  │ node-app │  │ mongodb │  │ redis ││
  │  │ :3000    │  │ :27017  │  │ :6379 ││
  │  └──────────┘  └─────────┘  └───────┘│
  │                                        │
  │  Containers find each other by NAME    │
  │  node-app → mongodb:27017 (DNS-based)  │
  └────────────────────────────────────────┘

AWS ECS production:
  ┌────────────────────────────────────────┐
  │  ECS Cluster (Fargate)                │
  │                                        │
  │  Task: api-service                     │
  │  ┌──────────┐                         │
  │  │ node-app │ → MongoDB Atlas (external)│
  │  │ :3000    │ → ElastiCache Redis       │
  │  └──────────┘                         │
  │  Behind ALB, in VPC private subnet    │
  └────────────────────────────────────────┘
```

---

## Docker Networking Modes

```
┌──────────────────────────────────────────────────────────────────┐
│  Mode        │ How it Works               │ Use Case            │
├──────────────┼────────────────────────────┼─────────────────────┤
│  bridge      │ Default. Containers get    │ Most apps.          │
│  (default)   │ private IPs on a virtual   │ docker-compose.     │
│              │ network. NAT to host.      │ Dev environments.   │
│              │                            │                     │
│  host        │ Container shares host's    │ Performance-critical│
│              │ network. No isolation.     │ No port mapping.    │
│              │ Port conflicts possible.   │                     │
│              │                            │                     │
│  none        │ No networking. Completely  │ Batch processing,   │
│              │ isolated container.        │ security-sensitive. │
│              │                            │                     │
│  overlay     │ Spans multiple Docker      │ Docker Swarm,       │
│              │ hosts. Built-in DNS.       │ multi-host cluster. │
│              │                            │                     │
│  awsvpc      │ Each container gets its    │ AWS ECS Fargate.    │
│  (ECS only)  │ own ENI + VPC IP.         │ Native VPC          │
│              │ Direct VPC connectivity.   │ networking.         │
└──────────────┴────────────────────────────┴─────────────────────┘
```

---

## Docker Compose — Full Stack Networking

```yaml
# docker-compose.yml
version: '3.8'

services:
  # ──── Node.js API ────
  api:
    build: .
    ports:
      - "3000:3000"       # Host:Container — expose to localhost
    environment:
      - MONGO_URI=mongodb://mongodb:27017/myapp    # Container DNS name!
      - REDIS_URL=redis://redis:6379
      - NODE_ENV=development
    depends_on:
      mongodb:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - app-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 5s
      retries: 3

  # ──── MongoDB ────
  mongodb:
    image: mongo:7.0
    ports:
      - "27017:27017"     # Expose for local tools (Compass)
    volumes:
      - mongo-data:/data/db
    networks:
      - app-network
    healthcheck:
      test: echo 'db.runCommand("ping").ok' | mongosh --quiet
      interval: 30s
      timeout: 5s
      retries: 3

  # ──── Redis ────
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    networks:
      - app-network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 5s
      retries: 3

  # ──── Nginx Reverse Proxy ────
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      - api
    networks:
      - app-network

volumes:
  mongo-data:
  redis-data:

networks:
  app-network:
    driver: bridge
```

### How Docker DNS Works

```
Inside app-network:

Container "api" can reach:
  mongodb:27017    ← Docker DNS resolves "mongodb" to container IP
  redis:6379       ← Docker DNS resolves "redis" to container IP

Docker creates a virtual bridge network:
  172.18.0.1  — bridge gateway (Docker host)
  172.18.0.2  — api container
  172.18.0.3  — mongodb container
  172.18.0.4  — redis container
  172.18.0.5  — nginx container

Container name → IP resolution is automatic.
No need for IP addresses in your code!

// ✅ Works in Docker
mongoose.connect('mongodb://mongodb:27017/myapp');

// ❌ Hardcoded IP — breaks when containers restart
mongoose.connect('mongodb://172.18.0.3:27017/myapp');
```

---

## Dockerfile for Node.js

```dockerfile
# Dockerfile
FROM node:20-alpine AS base

# Install dependencies only when package files change
FROM base AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --only=production

# Build stage
FROM base AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production image
FROM base AS production
WORKDIR /app

# Non-root user (security)
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nodeapp -u 1001

# Copy only what's needed
COPY --from=deps /app/node_modules ./node_modules
COPY --from=build /app/dist ./dist
COPY --from=build /app/package.json ./

USER nodeapp

# Expose port (documentation — doesn't actually publish)
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD wget -qO- http://localhost:3000/health || exit 1

CMD ["node", "dist/server.js"]
```

---

## AWS ECS Fargate — Production Container Networking

```
┌──────────────────────────────────────────────────────────────────┐
│  ECS Fargate Networking (awsvpc mode)                           │
│                                                                  │
│  Each task gets its OWN elastic network interface (ENI)         │
│  with a PRIVATE IP in your VPC subnet.                          │
│                                                                  │
│  VPC: 10.0.0.0/16                                               │
│  ├── Private Subnet: 10.0.10.0/24                              │
│  │   ├── Task 1: 10.0.10.5  (api container)                    │
│  │   ├── Task 2: 10.0.10.6  (api container)                    │
│  │   └── Task 3: 10.0.10.7  (api container)                    │
│  │                                                               │
│  │   These IPs are REAL VPC IPs.                                │
│  │   Security groups attach directly to tasks.                  │
│  │   RDS/Redis security groups can reference ECS SG.           │
│  │                                                               │
│  Traffic flow:                                                   │
│  Internet → ALB → ECS Task (10.0.10.5:3000) → RDS/Redis       │
│                                                                  │
│  No port mapping. No NAT. Direct VPC networking.                │
│  This is why Fargate is simpler than EC2 for containers.       │
└──────────────────────────────────────────────────────────────────┘
```

### ECS Task Definition (Networking)

```json
{
  "family": "api-service",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "containerDefinitions": [
    {
      "name": "api",
      "image": "123456789.dkr.ecr.us-east-1.amazonaws.com/api:latest",
      "portMappings": [
        { "containerPort": 3000, "protocol": "tcp" }
      ],
      "environment": [
        { "name": "MONGO_URI", "value": "mongodb+srv://..." },
        { "name": "REDIS_URL", "value": "redis://my-cache.xxx.cache.amazonaws.com:6379" }
      ],
      "healthCheck": {
        "command": ["CMD-SHELL", "curl -f http://localhost:3000/health || exit 1"],
        "interval": 30,
        "timeout": 5,
        "retries": 3
      },
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/api-service",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

---

## Commands & Debugging Tools

```bash
# Docker networking
docker network ls                          # List networks
docker network inspect app-network         # Show network details + containers
docker exec -it api ping mongodb           # Test DNS resolution between containers
docker exec -it api nslookup mongodb       # DNS lookup inside container
docker exec -it api curl http://nginx:80   # HTTP call between containers

# See container IPs
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' api

# Port mapping
docker ps --format "table {{.Names}}\t{{.Ports}}"
# NAMES    PORTS
# api      0.0.0.0:3000->3000/tcp
# mongodb  0.0.0.0:27017->27017/tcp

# Logs
docker logs api --follow --tail 50

# Enter container shell
docker exec -it api sh
# Now you can debug networking from inside the container
```

---

## Common Mistakes

### ❌ Using `localhost` to Connect Between Containers

```javascript
// ❌ localhost refers to the SAME container, not the host
mongoose.connect('mongodb://localhost:27017/myapp');
// Works on your machine, FAILS in Docker!

// ✅ Use the service name (Docker DNS)
mongoose.connect('mongodb://mongodb:27017/myapp');
```

### ❌ Not Using Health Checks

```yaml
# ❌ No health check — Docker doesn't know if your app is working
services:
  api:
    image: my-api

# ✅ Health check — Docker restarts unhealthy containers
services:
  api:
    image: my-api
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 5s
      retries: 3
```

### ❌ Running as Root in Container

```dockerfile
# ❌ Container runs as root (security risk)
CMD ["node", "server.js"]

# ✅ Run as non-root user
RUN adduser -S nodeapp
USER nodeapp
CMD ["node", "server.js"]
```

---

## Practice Exercises

### Exercise 1: Docker Compose
Create a docker-compose.yml with your Express API, MongoDB, and Redis. Verify containers can communicate by name.

### Exercise 2: Network Isolation
Create two Docker networks. Put the API on both, MongoDB on only one. Verify the API can reach MongoDB but another container on the second network cannot.

### Exercise 3: ECS Deployment
Deploy your Dockerized app to ECS Fargate. Configure ALB, security groups, and verify connectivity to RDS/ElastiCache.

---

## Interview Q&A

**Q1: How does Docker networking work?**
> Docker creates a virtual bridge network. Each container gets a virtual Ethernet interface with a private IP. Docker runs a DNS server that resolves container names to IPs. Containers on the same network communicate directly; traffic to the host goes through NAT.

**Q2: What networking mode does ECS Fargate use?**
> `awsvpc` — each task gets its own ENI with a real VPC IP address. This means tasks have direct VPC connectivity, can be targeted by security groups, and can access RDS/ElastiCache natively. No port mapping or NAT needed.

**Q3: How do containers discover each other?**
> Docker Compose: built-in DNS resolves service names. ECS: service discovery via AWS Cloud Map (DNS-based) or ALB. Kubernetes: kube-dns resolves service names. The pattern is always DNS-based — use service names, not IPs.

**Q4: What is a multi-stage Docker build and why use it?**
> Separate stages for dependencies, building, and production. Final image only contains production code and deps — no dev tools, source code, or build cache. Results in smaller, more secure images (200MB vs 1GB+).

**Q5: How do you handle secrets in Docker containers?**
> Never in Dockerfiles or environment variables in docker-compose.yml (visible in logs). Use: AWS Secrets Manager (ECS integrates natively), Docker secrets (Swarm), or mounted volumes. ECS can inject secrets from Secrets Manager/SSM Parameter Store directly into container environment.


Prev : [17 Microservices Networking](./17_Microservices_Networking.md) | Index: [0 Index](./0_Index.md) | Next : [19 Kubernetes Networking](./19_Kubernetes_Networking.md)
