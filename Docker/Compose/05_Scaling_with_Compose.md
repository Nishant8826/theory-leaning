# 📌 Topic: Scaling with Compose (Replicas and LB)

## 🧠 Concept Explanation (Basic → Expert)
**Basic**: Scaling with Compose means running multiple copies (replicas) of the same container to handle more traffic. You use the `--scale` flag to do this.
**Expert**: Scaling in Docker Compose is a **Horizontal Scaling Strategy** focused on the application layer. It requires the application to be **Stateless** (no data stored inside the container). Staff-level engineering involves managing the **Port Collision** problem (since multiple containers can't bind to the same host port) and implementing a **Load Balancer** (like Nginx or HAProxy) that can dynamically detect and route traffic to the new replicas. While Compose handles the creation of replicas, it does NOT provide an automatic load balancer; you must build one into your YAML.

## 🏗️ Mental Model
- **The Checkout Lane**: If one cashier (container) is too slow, you open 5 more lanes. But you need a manager (Load Balancer) at the entrance to tell people which lane to go to.

## ⚡ Actual Behavior
- **Port Mapping Limitation**: If your YAML has `ports: ["80:80"]`, you CANNOT scale that service. The second container will fail because port 80 is already taken on the host.
- **Internal DNS Load Balancing**: When you scale a service named `api`, Docker's internal DNS will return the IPs of ALL 5 replicas when another container looks up `http://api`.

## 🔬 Internal Mechanics (Round Robin DNS)
1. **The Request**: A frontend container pings `api`.
2. **The DNS Query**: Hits `127.0.0.11`.
3. **The Response**: Docker DNS returns 5 different A-records (IPs).
4. **The Selection**: Most clients (like `curl` or `fetch`) just pick the first IP in the list.
5. **The Rotation**: Docker DNS rotates the order of the list for every query (Round Robin), providing basic load balancing.

## 🔁 Execution Flow
1. `docker compose up --scale worker=5 -d`.
2. Compose checks the current count of `worker` containers.
3. It sees 1 and needs 5.
4. It creates 4 more containers with names like `project_worker_2`, `project_worker_3`, etc.
5. All 5 are joined to the same network.
6. The internal DNS is updated with the 4 new IPs.

## 🧠 Resource Behavior
- **CPU/RAM**: Scaling is linear. 5 replicas use 5x the RAM of 1 replica. 
- **Database Connections**: If each replica opens 10 connections to the DB, scaling to 10 replicas means the DB now has 100 open connections. Be careful not to overwhelm your database.

## 📐 ASCII Diagrams (REQUIRED)

```text
       SCALING ARCHITECTURE
       
[ Traffic ] --> [ Nginx (Load Balancer) ]
                       |
          +------------+------------+
          |            |            |
     [ API_1 ]    [ API_2 ]    [ API_3 ]  <-- Replicas
          |            |            |
          +------------+------------+
                       |
               [ SHARED REDIS ]
```

## 🔍 Code (Scaling with Nginx LB)
```yaml
services:
  lb:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    ports:
      - "80:80"
    depends_on:
      - web

  web:
    image: my-app:latest
    # NO port mapping here (avoids collision)
    deploy:
      replicas: 3
```

**nginx.conf snippet**:
```nginx
upstream myapp {
    server web:3000; # DNS 'web' returns all 3 IPs
}
server {
    listen 80;
    location / {
        proxy_pass http://myapp;
    }
}
```

## 💥 Production Failures
- **The "Stateful Scaling" Nightmare**: You scale your API to 3 replicas. A user logs into Replica 1. Their next request goes to Replica 2. Replica 2 says "Who are you?" and redirects them to the login page.
  *Fix*: Use a shared Session Store (Redis).
- **The "Zombie Replica"**: You run `docker compose up --scale web=2`. Later, you change the YAML to only 1 replica and run `docker compose up` again. Compose might leave the second container running unless you use the `--remove-orphans` flag.

## 🧪 Real-time Q&A
**Q: Can I scale my database?**
**A**: **No**, not with simple `--scale`. Databases are stateful. If you run 3 copies of Postgres on the same volume, they will corrupt each other's data instantly. Scaling databases requires complex patterns like Master-Slave replication or Sharding.

## ⚠️ Edge Cases
- **Docker Compose v3 vs v2 YAML**: The `deploy: replicas:` section only works with `docker stack deploy` (Swarm) or newer versions of `docker compose`. In older versions, you must use the CLI flag `--scale`.

## 🏢 Best Practices
- **Health Checks**: Always use health checks when scaling. If a replica is broken, the Load Balancer should stop sending traffic to it.
- **Use a Shared Cache**: Ensure all replicas use Redis for sessions and coordination.
- **Statelessness**: Ensure no local files are written inside the container (use S3 or Volumes).

## ⚖️ Trade-offs
| Strategy | Reliability | Performance | Complexity |
| :--- | :--- | :--- | :--- |
| **Single Instance**| Low | Low | **Low** |
| **Horizontal Scale**| **High** | **High** | High |

## 💼 Interview Q&A
**Q: How do you handle port collisions when scaling services with Docker Compose?**
**A**: When scaling a service horizontally, I remove the host port mapping (e.g., `80:80`) from the application containers. Instead, I only expose the internal port. I then introduce a **Load Balancer** service (like Nginx) in the same Compose project. The Load Balancer binds to the host's port 80 and uses Docker's internal DNS to route traffic to the application service name. Docker's internal DNS automatically handles the round-robin distribution of requests to the multiple underlying container IPs.

## 🧩 Practice Problems
1. Create a service and scale it to 5 replicas. Use `docker ps` to see their names.
2. Set up an Nginx load balancer and use a script to hit the load balancer 100 times. Log which container handles each request to verify load balancing is working.
3. Try to scale a service that has a hard-coded host port mapping and observe the error.

---
Prev: [04_Env_Config_and_Secrets.md](./04_Env_Config_and_Secrets.md) | Index: [00_Index.md](../00_Index.md) | Next: [01_Image_Registry_Architecture.md](../Registry/01_Image_Registry_Architecture.md)
---
