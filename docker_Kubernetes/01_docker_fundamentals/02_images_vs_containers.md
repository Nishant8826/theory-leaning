# Images vs Containers

## Why This Exists
One of the most common confusions for beginners is understanding the difference between a Docker Image and a Docker Container. Understanding this distinction is crucial because it dictates how you build, share, and scale your applications.

If you don't understand this, you might end up trying to "edit" a running container and wondering why your changes disappear when it restarts, or you might create bloated images by mistake.

## Real World Analogy
Think of this relationship like **Object-Oriented Programming (OOP)** or **Baking**:

1. **OOP Analogy**:
   - **Docker Image** = The `Class`. It's the blueprint, the definition. It doesn't do anything on its own.
   - **Docker Container** = The `Object` (Instance). It's the actual running thing created from the class. You can create many objects from one class.

2. **Baking Analogy**:
   - **Docker Image** = The `Recipe`. It's read-only. You can't eat a recipe.
   - **Docker Container** = The `Cake`. It's what you actually eat (run). You can bake 10 cakes from the same recipe.

## Core Concepts
- **Docker Image**:
  - Read-only.
  - Composed of layers.
  - Stored in registries (like Docker Hub).
  - Created using a `Dockerfile`.
- **Docker Container**:
  - Statefull or Stateless (preferably stateless).
  - Has a read-write layer on top of the image layers.
  - Can be started, stopped, paused, and deleted.
  - Isolated from other containers and the host OS.

## Architecture / Flow

```text
+------------+
| Dockerfile |
+------------+
      |
      | docker build
      v
+------------------+
|   Docker Image   |
| (Read-Only Base) |
+------------------+
      |
      +---> docker run ---> [Container 1]
      |
      +---> docker run ---> [Container 2]
      |
      +---> docker run ---> [Container 3]
```

### Key Takeaways from the Diagram:
1. **One Blueprint, Many Instances**: You write a `Dockerfile` once, build it into a **Docker Image**, and from that single image, you can spin up 1, 10, or 100 identical **Containers**.
2. **Layered Architecture**: 
   - The **Image** is made of read-only layers.
   - When you run a **Container**, Docker adds a thin **Read-Write layer** on top. All changes made while the container is running (like creating files or installing packages) are stored in this read-write layer.
   - If the container is deleted, that read-write layer is destroyed, but the underlying image remains untouched.


## Practical Commands
```bash
# IMAGE COMMANDS
# --------------
# List images
docker images

# Pull image
docker pull redis:alpine

# Remove image
docker rmi redis:alpine

# CONTAINER COMMANDS
# ------------------
# Run a container (creates and starts)
docker run -d --name my-redis redis:alpine

# List running containers
docker ps

# List all containers
docker ps -a

# Stop container
docker stop my-redis

# Start a stopped container
docker start my-redis

# Remove container
docker rm my-redis
```

## Hands-On Exercise
1. Pull the `alpine` image (a very small Linux distro):
   ```bash
   docker pull alpine
   ```
2. Run a container that prints a message and exits:
   ```bash
   docker run alpine echo "Hello from Alpine"
   ```
3. Run `docker ps`. You won't see it because it stopped immediately.
4. Run `docker ps -a`. You will see the container with status `Exited (0)`.
5. Notice that the image `alpine` is still there (`docker images`), but the container instance has finished its job.

## Mini Project
**Task**: Create 3 different Nginx containers from the same image, serving on different ports.

1. Run Container 1 on port 8081:
   ```bash
   docker run -d --name web1 -p 8081:80 nginx:latest
   ```
2. Run Container 2 on port 8082:
   ```bash
   docker run -d --name web2 -p 8082:80 nginx:latest
   ```
3. Run Container 3 on port 8083:
   ```bash
   docker run -d --name web3 -p 8083:80 nginx:latest
   ```
4. Verify by visiting `localhost:8081`, `localhost:8082`, and `localhost:8083`.
5. Clean up:
   ```bash
   docker stop web1 web2 web3
   docker rm web1 web2 web3
   ```

## Real Production Usage
In production, you use the same image across all environments:
- **Dev**: Image built from commit `abc123` is tested locally.
- **Staging**: The exact same image `abc123` is deployed for QA.
- **Prod**: The exact same image `abc123` is deployed to customers.
This guarantees that if it worked in Staging, it WILL work in Prod. You never rebuild the image for different environments; you only change the environment variables.

## Common Mistakes
- **Confusing `run` and `start`**: `docker run` creates a NEW container from an image. `docker start` starts an EXISTING, stopped container. If you keep using `docker run`, you will create hundreds of orphaned containers.
- **Storing data in containers**: Containers are ephemeral. If you delete a container, any data written inside it (like a database) is lost forever. Use **Volumes** for persistent data.

## Debugging Guide
- **Container keeps exiting**: If you run a container and it immediately stops, it usually means the main process finished or crashed.
  - Check logs: `docker logs <id>`
  - Run interactively to see errors: `docker run -it <image_name> sh`

## Best Practices
- **Treat containers as cattle, not pets**: Don't try to fix a running container. If it's broken, delete it and spin up a new one from a corrected image.
- **Keep images immutable**: Once an image is built, it should never be modified. If you need changes, build a new image with a new version tag.

## Interview Questions
1. **Can you modify a Docker Image after it is built?**
   *Answer*: No, images are read-only. To make changes, you must modify the Dockerfile and build a new image.
2. **What happens to the data inside a container when it is stopped?**
   *Answer*: The data remains there. However, if the container is **removed** (`docker rm`), all data not stored in a volume is lost.

## Summary
Images are the static blueprints; containers are the dynamic, running instances. You build images once and run many containers from them. Never store persistent data directly in a container.

---
Prev: [01_docker_basics.md](./01_docker_basics.md) | Index: [Index](../00_index.md) | Next: [03_dockerfile.md](./03_dockerfile.md)
