# 📌 Project: Full-Stack MERN Deployment with Nginx Reverse Proxy

## 🏗️ Project Overview
In this staff-level project, we will deploy a production-grade MERN (MongoDB, Express, React, Node) application. We won't just run `docker-compose up`; we will implement **Production Hardening**, **Layer 7 Routing**, **Non-Root Execution**, and **Health-Dependent Orchestration**. This project demonstrates the integration of Images, Networking, Storage, and Security modules.

## 📐 Architecture Diagram

```text
                     [ INTERNET ]
                          |
                  [ NGINX PROXY ] (L7)
                          |
          +---------------+---------------+
          | ( /api )                      | ( / )
          v                               v
    [ NODE.JS API ] <-----------> [ REACT FRONTEND ]
    ( Replicas: 3 )               ( Static / Distroless )
          |
    +-----+-----+
    |           |
[ MONGODB ]  [ REDIS ]
 (Volume)     (Cache)
```

## 🛠️ Step 1: The Optimized Dockerfiles

### 1.1 Backend (Node.js) - Security & Speed
We use a **Multi-stage build** and run as a **Non-root user**.
```dockerfile
# Stage 1: Build
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Stage 2: Production Runtime
FROM node:18-alpine
RUN apk add --no-cache tini
WORKDIR /app
# Copy only the necessary files from builder
COPY --from=builder /app/node_modules ./node_modules
COPY . .

# Security: Run as non-root user
USER node
EXPOSE 3000
ENTRYPOINT ["/sbin/tini", "--"]
CMD ["node", "server.js"]
```

### 1.2 Frontend (React) - Minimal Footprint
We compile the React app and serve it using a hardened Nginx image.
```dockerfile
# Stage 1: Build
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Serve with Nginx
FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## ⛓️ Step 2: The Orchestration (docker-compose.yml)
We implement **Healthchecks**, **Resource Limits**, and **Network Isolation**.
```yaml
version: '3.8'

services:
  nginx:
    image: my-nginx-proxy
    ports:
      - "80:80"
    depends_on:
      api:
        condition: service_healthy
    networks:
      - frontend

  api:
    build: ./backend
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
    environment:
      - MONGO_URI=mongodb://db:27017/prod
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 10s
    networks:
      - frontend
      - backend

  db:
    image: mongodb:6
    volumes:
      - mongo-data:/data/db
    networks:
      - backend

networks:
  frontend:
  backend:
    internal: true # Security: DB has no access to the outside world

volumes:
  mongo-data:
```

## 💥 Production Failures & Fixes
- **Failure**: The API starts but fails to connect to MongoDB because MongoDB is still initializing. The API crashes and enters a restart loop.
  *Fix*: Use `depends_on` with `condition: service_healthy` and implement a retry-loop in the Node.js connection logic.
- **Failure**: A hacker exploits a vulnerability in the React app. Because Nginx was running as `root`, they manage to read the host's `/etc/shadow`.
  *Fix*: Use an unprivileged Nginx image (`nginxinc/nginx-unprivileged`) and drop all capabilities.

## 💼 Interview Q&A
**Q: Why use two separate Docker networks (Frontend and Backend) in this project?**
**A**: This is the principle of **Micro-segmentation**. The `frontend` network allows the Nginx proxy to talk to the Node.js API. The `backend` network allows the API to talk to the Database. Crucially, the Database is **not** on the `frontend` network. This ensures that even if the Nginx proxy is compromised, the attacker has no direct network path to the Database, significantly reducing the "Blast Radius" of a breach.

## 🧪 Lab Exercise
1. Build and deploy the stack using `docker-compose up -d`.
2. Use `docker stats` to verify that the 3 API replicas are sharing the load.
3. Manually stop the `db` container and verify that the `api` healthcheck fails and Nginx stops routing traffic to it.

---
Prev: [05_Linux_Capabilities_Matrix.md](../Internals/05_Linux_Capabilities_Matrix.md) | Index: [00_Index.md](../00_Index.md) | Next: [02_RealTime_SocketIO_Cluster.md](./02_RealTime_SocketIO_Cluster.md)
---
