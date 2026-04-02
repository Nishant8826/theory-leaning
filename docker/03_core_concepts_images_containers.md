# Core Concepts: Images & Containers

---

### What
- **Docker Image:** A read-only template containing instructions for building a Docker container. It includes the OS files, the runtime (like Node.js), application code, and third-party dependencies. Once made, an image cannot be changed.
- **Docker Container:** A runnable instance of an image. You can start, stop, move, or delete a container. You can think of an Image as the generic Class, inside OOP programming, and a Container as the instantiated Object.
- **Image Layers:** Docker images are built like an onion, layer by layer. If an image is 1GB, and you change 1 line of your JS code and rebuild, Docker doesn't rebuild 1GB—it only rebuilds the tiny 1KB layer with your code!

---

### Why
By keeping Images read-only, Docker ensures absolute consistency. If I pull Image `v1.2`, I guarantee it is identical to your `v1.2`. 
By building images in layers, building and downloading updates takes literally seconds because Docker uses heavily optimized caching mechanisms.

---

### How
When you start a container, Docker grabs the read-only Image layers and stacks them up. It then magically adds a **thin read-write layer** exactly on top.
When a user uploads a photo to your Node.js app inside a container, the photo belongs to the thin "read-write" layer. 
*Warning:* If the container is deleted, that thin layer is completely destroyed!

---

### Implementation

You don't configure layers in application code, but you interact with them via the terminal.

```bash
# Pull an Image (Notice how it downloads in chunks? Those are LAYERS!)
docker pull nginx
# Output:
# 3b4173d100c8: Pull complete (Base OS Layer)
# a645e7f1dc21: Pull complete (Nginx software Layer)

# Look at downloaded Images
docker images

# Run a container IN DETACHED MODE (-d) and name it
docker run -d --name my_webserver nginx

# Look at running containers
docker ps

# Stop the container
docker stop my_webserver

# Completely delete the running instance (Image remains safe on your HDD)
docker rm my_webserver
```

---

### Steps
1. Fetch an image (`docker pull [image_name]`).
2. Run it (`docker run [image_name]`).
3. Check status (`docker ps` - think "process status").
4. If you need to debug a stopped container, `docker logs [container_id]`.
5. Remove unused containers (`docker rm -f [container_id]`) and images (`docker rmi [image_name]`) to save disk space.

---

### Integration

* **React/Next.js/Node.js:** You will build custom Docker Images for your specific frontends and backends. A Node.js backend Image might consist of: Base OS layer -> Node installation layer -> `package.json/npm install` layer -> Your backend code layer.
* **Full-stack apps:** You will spin up **Three** completely separate Containers from **Three** different Images (React Image, Node Image, MongoDB Image) and network them together.

---

### Impact
Image layer caching speeds up Continuous Integration (CI/CD) pipelines remarkably. If a developer only changes CSS and pushes to GitHub, the CI pipeline recognizes that the heavy `npm install` layer hasn't changed. It uses the cached `node_modules` instantly, only rebuilding the tiny CSS layer in 1.4 seconds.

---

### Interview Questions
1. **What is the exact relationship between an Image and a Container?**
   *Answer: An image is a read-only, immutable template. A container is a live, running instance of that template possessing an active read-write layer and network bindings.*
2. **Explain Docker Image Layers and Caching.**
   *Answer: Images are built via sequential instructions. Each instruction creates a layer. If a layer hasn't changed, Docker securely re-uses it from the cache on subsequent builds, saving massive amounts of time and bandwidth.*
3. **What happens to data written inside a container if the container is destroyed?**
   *Answer: It is permanently lost, because data is written to the ephemeral read-write layer attached to that specific container instance.*

---

### Summary
* Images are read-only generic blueprints.
* Containers are actual running apps.
* Images are built in cached layers for extreme speed.
* Never store permanent data inside a generic container instance.

---
Prev : [02_docker_architecture.md](./02_docker_architecture.md) | Next : [04_volumes_and_bind_mounts.md](./04_volumes_and_bind_mounts.md)
