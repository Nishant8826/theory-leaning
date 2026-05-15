# Docker Basics

## Why This Exists
As a full-stack developer, you've likely faced the "It works on my machine" problem. You build a React app with a Node.js backend, and everything works locally. But when you deploy it to a server, it fails because the server has a different Node.js version, missing system dependencies, or different environment configurations.

Docker exists to solve this exact problem. It packages your application and **all its dependencies** into a single, standardized unit called a container. This ensures that your app runs exactly the same way in development, staging, and production.

## Real World Analogy
Think of Docker like shipping containers in the freight industry.
Before standard shipping containers, cargo came in all shapes and sizes (bags of grain, barrels of oil, crates of electronics). Loading them onto ships was a nightmare because everything required special handling.

The shipping container revolutionized this. It doesn't matter what's inside (grain, oil, or electronics); the container is a standard size. Ships, cranes, and trucks are all designed to handle this standard container.

In this analogy:
- **Your Code** = The cargo
- **Docker Container** = The standard shipping container
- **The OS/Server** = The ship or truck

## Core Concepts
- **Docker Client**: The CLI tool you use to interact with Docker (e.g., running `docker build`).
- **Docker Daemon (dockerd)**: The background service running on your host OS that manages containers.
- **Docker Image**: A read-only template containing the application code, runtime, libraries, and environment variables. (The "blueprint").
- **Docker Container**: A running instance of an image. (The "actual building").
- **Docker Registry**: A place to store and share images (like Docker Hub or AWS ECR).

## Architecture / Flow

```text
[Developer]
    |
    | 1. Writes Code & Dockerfile
    v
[Docker Client]
    |
    | 2. Sends commands (build/run)
    v
[Docker Daemon] <-----> [Docker Registry] (3. Pulls if not local)
    |
    | 4. Creates
    v
[Docker Image]
    |
    | 5. Runs as
    v
[Docker Container]
```


## Practical Commands
Here are the absolute essential commands you need to know:

```bash
# Check Docker version
docker --version

# Pull an image from Docker Hub
docker pull node:22-alpine

# List local images
docker images

# Run a container from an image
docker run -d --name my-node-app -p 3000:3000 node:22-alpine

# List running containers
docker ps

# List all containers (including stopped ones)
docker ps -a

# Stop a running container
docker stop my-node-app

# Remove a container
docker rm my-node-app

# Remove an image
docker rmi node:22-alpine
```

## Hands-On Exercise
1. Pull the official Nginx image:
   ```bash
   docker pull nginx:latest
   ```
2. Run the Nginx container in detached mode, mapping port 8080 on your host to port 80 in the container:
   ```bash
   docker run -d --name my-nginx -p 8080:80 nginx:latest
   ```
3. Open your browser and go to `http://localhost:8080`. You should see the default Nginx welcome page.
4. Stop and remove the container:
   ```bash
   docker stop my-nginx
   docker rm my-nginx
   ```

## Mini Project
**Task**: Run a simple Node.js script inside a Docker container without creating a Dockerfile yet.

1. Create a file named `app.js` with this content:
   ```javascript
   console.log("Hello from inside the container!");
   console.log("Current Node version:", process.version);
   ```
2. Run this script using the official Node image, mounting your current directory into the container:
   ```bash
   # On Linux/Mac
   docker run --rm -v $(pwd):/app -w /app node:22-alpine node app.js

   # On Windows (PowerShell)
   docker run --rm -v ${PWD}:/app -w /app node:22-alpine node app.js
   ```
   *Explanation*: `--rm` removes the container after it finishes. `-v` mounts your local folder to `/app`. `-w` sets the working directory.

## Real Production Usage
In production, you never run manual `docker run` commands for your application.
- You use **Docker Compose** for multi-container apps on a single server.
- You use **Kubernetes** or **AWS ECS** for orchestrating containers across multiple servers.
- Images are automatically built and pushed to a registry (like AWS ECR) using CI/CD pipelines (like GitHub Actions).

## Common Mistakes
- **Running containers as root**: This is a security risk. Always use a non-root user in your production images.
- **Hardcoding environment variables**: Never bake secrets or API keys into your images. Use environment variables.
- **Large image sizes**: Using heavy base images like `ubuntu` instead of lightweight ones like `alpine` makes deployments slow.

## Debugging Guide
If a container fails to start or behave correctly:
1. **Check the logs**:
   ```bash
   docker logs <container_name_or_id>
   ```
2. **Inspect the container**: Get detailed JSON metadata about the container.
   ```bash
   docker inspect <container_name_or_id>
   ```
3. **Execute a shell inside the container**: (If it's running)
   ```bash
   docker exec -it <container_name_or_id> sh
   # or bash if available
   ```

## Best Practices
- **Use `.dockerignore`**: Just like `.gitignore`, prevent node_modules and logs from being copied into the image.
- **One process per container**: Don't run your Node app, Cron jobs, and Nginx all in one container. Separate them.
- **Use specific tags**: Never use `:latest` in production. Use specific versions like `node:18.16.0-alpine`.

## Interview Questions
1. **What is the difference between a container and a virtual machine?**
   *Answer*: VMs include a full operating system and a hypervisor, making them heavy and slow to start. Containers share the host OS kernel and are lightweight, starting in seconds.
2. **What does the `-p` flag do in `docker run`?**
   *Answer*: It publishes a container's port to the host. `8080:80` means traffic on host port 8080 is forwarded to container port 80.

## Summary
Docker solves the environment consistency problem by packaging code and dependencies together. Images are the blueprints, and containers are the running instances. Mastering these basics is the foundation for everything else in this course.

---
Prev: [Index](../00_index.md) | Index: [Index](../00_index.md) | Next: [02_images_vs_containers.md](./02_images_vs_containers.md)
