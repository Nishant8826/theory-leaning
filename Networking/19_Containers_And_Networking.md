# Containers & Networking

> 📌 **File:** 19_Containers_And_Networking.md | **Level:** Full-Stack Dev → Networking Expert

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

#### Diagram Explanation (The Apartment Building)
- **Localhost (The Studio Apartment):** Currently, your code and database all live in one single room (`localhost`). They talk to each other without resolving an address.
- **Docker Compose (The Apartment Building):** You moved your code and databases into their own separate apartments (`node-app`, `mongodb`), but they are all tightly contained in the same building (`app-network`). They call each other by name via the building intercom (Docker DNS).
- **ECS Production (The Master Planned Community):** In production, your code lives in one house (ECS Fargate), and your databases live in managed gated facilities (MongoDB Atlas, ElastiCache). They must use the public roads (VPC Networking) to securely communicate!

---

## Docker Networking Modes

- **bridge (default):** Private IPs on a virtual network. NAT to host. Used for most docker-compose developments.
- **host:** Container shares host's network. Performance-critical, no port isolation.
- **none:** Completely isolated container. Used for security-sensitive batch processing.
- **overlay:** Spans multiple Docker hosts. Used in Docker Swarm.
- **awsvpc (ECS only):** Direct VPC networking where each task gets its own ENI + VPC IP.

---

## Docker Compose — Full Stack Networking

```yaml
# docker-compose.yml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "3000:3000"
    environment:
      - MONGO_URI=mongodb://mongodb:27017/myapp    # Container DNS name!
      - REDIS_URL=redis://redis:6379
    depends_on:
      mongodb:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - app-network

  mongodb:
    image: mongo:7.0
    ports:
      - "27017:27017"
    volumes:
      - mongo-data:/data/db
    networks:
      - app-network
    healthcheck:
      test: echo 'db.runCommand("ping").ok' | mongosh --quiet
      interval: 30s
      timeout: 5s
      retries: 3

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

volumes:
  mongo-data:
  redis-data:

networks:
  app-network:
    driver: bridge
```

---

## AWS ECS Fargate — Production Container Networking

Fargate uses the `awsvpc` network mode. Each task gets its own Elastic Network Interface (ENI) with a real VPC IP address. This completely eliminates port conflicts and allows you to attach extremely specific firewall rules (Security Groups) directly to an individual container task.

---

## Practice Exercises

### Exercise 1: Docker Compose Setup
Create a `docker-compose.yml` with your Express API, MongoDB, and Redis. Verify containers can communicate by name.

### Exercise 2: Network Isolation
Create two Docker networks. Put the API on both, MongoDB on only one. Verify the API can reach MongoDB but another container on the second network cannot.

---

## Interview Q&A

**Q1: How does Docker networking work?**
> Docker creates a virtual bridge network. Each container gets a virtual Ethernet interface with a private IP. Docker runs a DNS server that resolves container names to IPs. Containers on the same network communicate directly.

**Q2: What networking mode does ECS Fargate use?**
> `awsvpc` — each task gets its own ENI with a real VPC IP address. This means tasks have direct VPC connectivity, can be targeted by security groups, and can access RDS/ElastiCache natively.

**Q3: How do containers discover each other?**
> Docker Compose: built-in DNS resolves service names. ECS: service discovery via AWS Cloud Map (DNS-based) or ALB. Kubernetes: kube-dns resolves service names. The pattern is always DNS-based.

**Q4: What is a multi-stage Docker build and why use it?**
> Separate stages for dependencies, building, and production. The final image only contains production code and deps — no dev tools, source code, or build cache, resulting in smaller, more secure images.

**Q5: How do you handle secrets in Docker containers?**
> Never hardcode in Dockerfiles or compose files. Inject via environment variables at runtime, using tools like AWS Secrets Manager (for ECS) or Kubernetes Secrets.

---

Prev : [18 Microservices Networking](./18_Microservices_Networking.md) | Index: [00 Index](./00_Index.md) | Next : [20 Kubernetes Networking](./20_Kubernetes_Networking.md)
