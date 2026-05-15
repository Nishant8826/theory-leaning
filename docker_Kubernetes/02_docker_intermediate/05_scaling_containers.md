# Scaling Containers

## Why This Exists
A single container can only handle a certain amount of traffic. What happens when your app goes viral, or you have a massive Black Friday sale? 

If you only run one instance of your application, it becomes a **Single Point of Failure**. If it crashes, your site goes down. To handle high traffic and ensure high availability, you need to run multiple copies (replicas) of your container and distribute traffic among them.

## Real World Analogy
Think of scaling like **Opening more Checkout Lanes at a Grocery Store**.
- **Vertical Scaling**: Making a single cashier work faster or giving them a better computer. There is a limit to how fast they can go.
- **Horizontal Scaling**: Opening 5 more checkout lanes. This is how Docker scales. You don't make the container bigger; you just run more of them.

## Core Concepts
- **Vertical Scaling**: Increasing CPU/RAM of an existing container/server.
- **Horizontal Scaling**: Adding more instances of the container.
- **Replicas**: Identical running copies of a container.
- **Load Balancer**: A tool (like Nginx) that sits in front and distributes traffic to the replicas.

## Architecture / Flow

```text
       [ Internet Traffic ]
                │
                ▼
      +-------------------+
      |   Load Balancer   | (Nginx / AWS ALB)
      +-------------------+
                │
      ┌─────────┴─────────┐
      ▼                   ▼
[ App Replica 1 ]   [ App Replica 2 ]   [ App Replica 3 ]
```

## Practical Commands

Using Docker Compose is the easiest way to scale containers locally.

```bash
# Scale the 'web' service to 3 instances
docker compose up -d --scale web=3

# Scale down to 1 instance
docker compose up -d --scale web=1
```

## Hands-On Exercise
Let's see Docker Compose scale a service.

1. Create a `docker-compose.yml`:
   ```yaml
   version: '3.8'
   services:
     web:
       image: nginx:alpine
       ports:
         - "8080:80" # This will cause a conflict if we scale!
   ```
2. If you try to run `docker compose up --scale web=3`, it will **fail** because all 3 containers will try to bind to host port `8080`.
3. To fix this, remove the host port mapping:
   ```yaml
   version: '3.8'
   services:
     web:
       image: nginx:alpine
       expose:
         - "80" # Expose inside network, let Load Balancer handle public port
   ```

## Mini Project
**Task**: Set up a load balancer and scale a backend service.

1. Create a `docker-compose.yml`:
   ```yaml
   version: '3.8'
   services:
     app:
       image: nginxdemos/hello:plain # Displays container hostname
     
     lb:
       image: nginx:alpine
       ports:
         - "80:80"
       volumes:
         - ./nginx.conf:/etc/nginx/nginx.conf:ro
       depends_on:
         - app
   ```
2. Create `nginx.conf` to load balance to the service name `app`:
   ```nginx
   events {}
   http {
       upstream backend {
           server app:80; # Docker DNS resolves this to all replicas
       }
       server {
           listen 80;
           location / {
               proxy_pass http://backend;
           }
       }
   }
   ```
3. Run and scale:
   ```bash
   docker compose up -d --scale app=3
   ```
4. Visit `localhost` and refresh. You will see different container IDs, proving traffic is being balanced!

## Real Production Usage
While Docker Compose can scale containers on a single machine, it cannot scale across multiple servers. In production, we use **Orchestrators**:
- **Docker Swarm**: Built into Docker, good for small-to-medium setups.
- **Kubernetes (K8s)**: The industry standard for large-scale container orchestration across server clusters.
- **AWS ECS / ECS Fargate**: Managed container services by AWS.

## Common Mistakes
- **Port Conflicts**: Trying to scale a service that has a hardcoded host port (e.g., `"80:80"`).
- **Stateful Apps**: If your app stores user sessions in its local memory, scaling will break your app (User logs in on Instance 1, next click goes to Instance 2 where they are not logged in).

## Debugging Guide
- **Traffic only going to one container**: Ensure your load balancer is not caching DNS resolutions indefinitely. Docker's embedded DNS load balances by default, but some proxies need configuration to respect it.

## Best Practices
- **Make apps stateless**: Store sessions in Redis and uploads in S3, not on the container's local disk.
- **Use Health Checks**: Ensure the load balancer only sends traffic to containers that are actually ready.

## Interview Questions
1. **How do you handle user sessions when scaling web containers horizontally?**
   *Answer*: You should not store sessions in the container's memory. Instead, use a centralized session store like **Redis**, or use JWT tokens that don't require server-side session state.
2. **What is the issue with port mapping when scaling with Docker Compose?**
   *Answer*: You cannot bind multiple containers to the same host port. You should omit the host port and use a reverse proxy/load balancer to route traffic.

## Summary
Scaling is the superpower of containerization. By keeping your applications stateless and utilizing Docker Compose or Kubernetes, you can handle massive traffic spikes effortlessly.

---
Prev: [04_monitoring.md](./04_monitoring.md) | Index: [Index](../00_index.md) | Next: [06_cicd_github_actions.md](./06_cicd_github_actions.md)
