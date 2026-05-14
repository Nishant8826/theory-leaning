# Port Forwarding

## Why This Exists
Containers run in their own isolated network namespace. This means if you run a web server inside a container on port 80, it is not accessible from outside the container by default. Not even from the host machine running the container!

To make a containerized application accessible to users or other systems outside the Docker host, you must explicitly map or "forward" ports from the host machine to the container.

## Real World Analogy
Think of the host machine as a **Large Office Building** and the container as a **Specific Office** inside it.
- The building has a main street address (the host's IP).
- The office inside has a room number (the container's port, e.g., 80).
- If someone from the outside world wants to visit that office, the building needs a **Receptionist** or a **Directory** that says: "To go to Office 80, go through Door 8080 on the main street."

Port forwarding is that directory. It maps `HostPort:ContainerPort`.

## Core Concepts
- **Publishing Ports (`-p`)**: Maps a port on the host to a port in the container.
- **Exposing Ports (`EXPOSE`)**: Documentation in the Dockerfile. It doesn't actually publish the port; it just tells users which ports the app listens on.
- **Random Port Mapping (`-P`)**: Maps all exposed ports to random high-numbered ports on the host.

## Architecture / Flow

```mermaid
graph LR
    A[Internet / User] -->|Port 8080| B(Host Machine)
    B -->|Forwards to| C(Container Port 80)
```

### Breakdown of the Flow:
1. **Traffic Arrives**: A user or external system sends a request to your host machine's IP address on a specific port (e.g., `8080`).
2. **Docker Proxy**: The Docker daemon has set up a rule (using iptables on Linux) to listen on that host port.
3. **Forwarding**: Docker forwards that traffic directly into the isolated network of the container, targeting the specific container port (e.g., `80`).
4. **Response**: The application inside the container processes the request and sends the response back through the same path.


## Practical Commands
```bash
# Map host port 8080 to container port 80
docker run -d -p 8080:80 nginx:latest

# Map host port 3000 to container port 3000
docker run -d -p 3000:3000 node-app:latest

# Bind to a specific interface (only accessible on localhost)
docker run -d -p 127.0.0.1:8080:80 nginx:latest

# Publish all exposed ports to random ports
docker run -d -P nginx:latest

# Check mapped ports for a running container
docker port <container_name_or_id>
```

## Hands-On Exercise
1. Run an Nginx container mapping port 8080 on the host to port 80 in the container:
   ```bash
   docker run -d --name my-web -p 8080:80 nginx:latest
   ```
2. Open your browser and go to `http://localhost:8080`. You should see the Nginx welcome page.
3. Now try to run another container on the same host port:
   ```bash
   docker run -d --name my-web2 -p 8080:80 nginx:latest
   ```
   *Note: This will fail with a "port is already allocated" error. You cannot bind two containers to the same host port.*
4. Fix it by using a different host port:
   ```bash
   docker run -d --name my-web2 -p 8081:80 nginx:latest
   ```

## Mini Project
**Task**: Run a Node.js app and a Redis server, but only expose the Node.js app to the outside world.

1. Create a custom network:
   ```bash
   docker network create my-app-net
   ```
2. Run Redis on the network (do NOT use `-p`):
   ```bash
   docker run -d --name cache --network my-app-net redis:alpine
   ```
   *Note: Redis is accessible on port 6379 ONLY inside the network.*
3. Run the Node app on the network and expose it to the host:
   ```bash
   docker run -d --name web-app --network my-app-net -p 80:3000 my-node-app
   ```
   *Result*: Users can access the app on port 80. The app can access Redis at `cache:6379`. Redis is secure from external access.

## Real Production Usage
- In production (like AWS or Kubernetes), you often don't map ports directly to host machines.
- Instead, you use a **Load Balancer** (like AWS ALB) or an **Ingress Controller** that receives traffic on port 80/443 and routes it to the correct container.

## Common Mistakes
- **Confusing the order**: It is always `HOST:CONTAINER`. If you do `80:8080` when your app runs on 8080, it won't work.
- **Port conflicts**: Trying to run multiple containers on the same host port.
- **Exposing everything**: Exposing database ports to the public internet is a huge security risk.

## Debugging Guide
- **Connection Refused**:
  - Verify the container is running.
  - Verify the app inside the container is actually listening on the port you think it is.
  - Check `docker port <container_name>` to see active mappings.

## Best Practices
- **Only publish what is necessary**: Keep internal services (databases, caches) internal.
- **Use specific interfaces**: If a service only needs to be accessed locally, bind it to `127.0.0.1:port`.

## Interview Questions
1. **What does `-p 8080:80` do in Docker?**
   *Answer*: It maps port 8080 on the host machine to port 80 inside the container.
2. **What is the difference between `EXPOSE` in a Dockerfile and the `-p` flag?**
   *Answer*: `EXPOSE` is documentation; it doesn't open ports. `-p` actually publishes the port and creates iptables rules on the host to forward traffic.

## Summary
Port forwarding bridges the gap between the isolated container network and the outside world. Always remember the order `HOST:CONTAINER` and only expose ports that are absolutely necessary for external access.

---
Prev: [05_networks.md](./05_networks.md) | Index: [Index](../00_index.md) | Next: [07_environment_variables.md](./07_environment_variables.md)
