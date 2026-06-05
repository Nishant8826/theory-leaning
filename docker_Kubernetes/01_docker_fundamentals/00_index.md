# 🐳 Docker Fundamentals – Complete Revision Guide

Welcome to the Docker Fundamentals module revision sheet. This document aggregates all key concepts, commands, syntax configurations, analogies, production best practices, and interview-prep notes from every topic in this directory, allowing you to perform a complete revision from a single file.

---

## 📌 Module Navigation
- [01. Docker Basics](#01-docker-basics)
- [02. Images vs Containers](#02-images-vs-containers)
- [03. Dockerfile In-Depth](#03-dockerfile-in-depth)
- [04. Volumes & Data Persistence](#04-volumes--data-persistence)
- [05. Docker Networks](#05-docker-networks)
- [06. Port Forwarding](#06-port-forwarding)
- [07. Environment Variables](#07-environment-variables)
- [08. Docker Compose](#08-docker-compose)
- [09. Multi-Stage Builds](#09-multi-stage-builds)
- [10. Image Optimization](#10-image-optimization)
- [11. Container Debugging](#11-container-debugging)
- [12. Container Security](#12-container-security)

---

## 01. Docker Basics
🔗 **Full Lesson:** [01_docker_basics.md](./01_docker_basics.md)

* **Why It Exists**: Eliminates the "it works on my machine" problem by packaging code and *all its dependencies* into a single, standardized, self-contained unit.
* **Real-World Analogy**: Standardized freight **shipping containers**. Ships, trucks, and cranes don't care what is inside; they are built to load/unload a standard size box.
* **Architecture Parts**:
  * **Client**: CLI tool used to interact with Docker (e.g., `docker build`).
  * **Daemon (`dockerd`)**: Background host service managing images, containers, networks, and volumes.
  * **Image**: Read-only static template/blueprint.
  * **Container**: Active, running isolated instance of an image.
  * **Registry**: Storage and distribution hub for images (e.g., Docker Hub, AWS ECR).

### Key Commands:
```bash
docker pull node:22-alpine                                     # Pull image from Docker Hub
docker run -d --name my-app -p 8080:80 nginx:latest            # Run container in detached mode
docker ps                                                      # List running containers
docker ps -a                                                   # List all containers (including stopped)
docker stop my-app && docker rm my-app                         # Stop and delete container
docker images                                                  # List local images
docker rmi nginx:latest                                        # Delete local image
```

---

## 02. Images vs Containers
🔗 **Full Lesson:** [02_images_vs_containers.md](./02_images_vs_containers.md)

* **Real-World Analogy**: 
  * **OOP**: Image = `Class` (Blueprint) | Container = `Object` (Instance).
  * **Baking**: Image = `Recipe` (Read-only) | Container = `Cake` (Eatable, multiple cakes from 1 recipe).
* **Architecture Difference**:
  * **Image**: Made of immutable, read-only layers. Once built, it cannot be modified.
  * **Container**: Active instance that adds a thin **Read-Write layer** on top of the image's read-only layers. Any runtime changes (writing files, installations) occur in this temporary writable layer. If the container is deleted, the writable layer is destroyed, but the base image remains untouched.

### Key Gotcha: `run` vs `start`
* `docker run`: Creates a **new** container instance from an image and starts it.
* `docker start`: Restarts an **existing, stopped** container instance, preserving previous configurations in its writable layer.

---

## 03. Dockerfile In-Depth
🔗 **Full Lesson:** [03_dockerfile.md](./03_dockerfile.md)

* **Why It Exists**: A blueprint script to automate image building.
* **Core Instructions**:
  * `FROM`: Base parent image (e.g., `node:22-alpine`).
  * `WORKDIR`: Sets the working directory inside the container for subsequent instructions.
  * `COPY <src> <dest>`: Copies files from the host machine (build context) to the container.
  * `RUN`: Executes shell commands *during the build process* and commits results to a new image layer.
  * `ENV`: Sets persistent environment variables at runtime.
  * `EXPOSE`: Documents the ports the application listens on (informational only).
  * `CMD`: Specifies the default command executed *when the container starts*.

### Key Commands:
```bash
docker build -t my-app:v1 .                             # Build image from Dockerfile in current dir
docker build -f Dockerfile.dev -t my-app:dev .          # Build using a specific custom Dockerfile
```

> [!IMPORTANT]
> **Build Context (`.` at the end)**: Specifies the directory sent to the Docker daemon. Any files copied via `COPY` must be within this build context directory.
> **RUN vs CMD**: `RUN` executes during image build (static snapshot). `CMD` executes when the container spins up (runtime entrypoint).

---

## 04. Volumes & Data Persistence
🔗 **Full Lesson:** [04_volumes.md](./04_volumes.md)

* **Why It Exists**: Containers are ephemeral. If you delete a database container without a volume, all data is lost. Volumes map container paths to host directories to decouple data lifecycle from container lifecycle.
* **Real-World Analogy**: Container = **Rental Car** (temporary glovebox space) | Volume = **Suitcase** (you take your data with you when returning the car).
* **Persistence Types**:
  * **Named Volumes**: Completely managed by Docker (stored in `/var/lib/docker/volumes/`). **Best for production databases** (PostgreSQL, MongoDB).
  * **Bind Mounts**: Maps a specific, absolute path on the host directory to the container. **Best for local development** (reflecting live code updates/hot reloading).
  * **Tmpfs Mounts**: Volatile, in-memory storage. Never written to disk (good for temporary security keys).

### Key Commands:
```bash
docker volume create db-data                                       # Create a named volume
docker run -d --name database -v db-data:/data/db mongo:latest     # Run using named volume
docker run -d --name app -v $(pwd)/src:/app/src node:22-alpine     # Bind mount for development
docker volume ls && docker volume inspect db-data                  # List and detail volumes
docker volume prune                                                # Delete all unused volumes
```

---

## 05. Docker Networks
🔗 **Full Lesson:** [05_networks.md](./05_networks.md)

* **Why It Exists**: Secure communication between containers. By default, containers are isolated and cannot reach each other by name unless connected to the same custom network.
* **Real-World Analogy**: A private **Office LAN phone system**. Putting containers on the same custom network assigns them internal extensions to call each other directly by name.
* **Network Drivers**:
  * **Bridge**: Default virtual network driver on a single host. **Custom Bridge Networks** support automatic DNS resolution by container name.
  * **Host**: Removes isolation between container and host network namespace (shares host IP/ports directly).
  * **Overlay**: Connects multiple Docker daemons together (for multi-node Docker Swarm orchestration).
  * **None**: Disables all network access.

### Key Commands:
```bash
docker network create app-net                                      # Create custom bridge network
docker run -d --name database --network app-net mongo:latest       # Run database inside network
docker run -d --name backend --network app-net -p 8080:8080 app    # Run app, reaches database via connection string: 'mongodb://database:27017'
docker network inspect app-net                                     # Check connected containers and IPs
```

> [!WARNING]
> Containers on the default `bridge` network cannot resolve each other by container name. You **must** create a custom network to leverage built-in DNS service discovery.

---

## 06. Port Forwarding
🔗 **Full Lesson:** [06_ports.md](./06_ports.md)

* **Why It Exists**: Containers run in private network namespaces. To allow outside systems (or the host browser) to reach a containerized app, you must map a host port to the container port.
* **Real-World Analogy**: Host = **Office Building Address** | Container = **Specific Office Room**. Port forwarding directs traffic arriving at the main entrance door to the correct internal office desk.
* **Syntax**: `-p <HostPort>:<ContainerPort>` (Host-to-Container).

### Key Commands:
```bash
docker run -d -p 8080:80 nginx:latest                         # Maps host port 8080 to container port 80
docker run -d -p 127.0.0.1:3000:3000 node-app:latest          # Restricts host access to localhost interface only
docker run -d -P nginx:latest                                 # Maps exposed ports to random high ports
docker port <container_name>                                  # Inspect active port mappings
```

---

## 07. Environment Variables
🔗 **Full Lesson:** [07_environment_variables.md](./07_environment_variables.md)

* **Why It Exists**: Keeps images **configuration-agnostic**. Instead of building different images for Dev, Staging, and Prod, you build one image and inject credentials, ports, and API keys at runtime.
* **Real-World Analogy**: **Universal Remote**. The hardware/code is identical, but it operates differently depending on the code parameters programmed in at startup.
* **Build Args vs. Env Vars**:
  * **`ARG`**: Build-time variables. Used in the Dockerfile only while building (e.g., passing node version). Not accessible in running containers.
  * **`ENV`**: Persistent runtime variables. Visible inside the container environment.

### Key Commands:
```bash
docker run -e DB_HOST=mongo -e DB_PORT=27017 my-app:latest     # Inject single environment variables
docker run --env-file .env my-app:latest                       # Load variables from local .env file
docker exec -it my-app env                                     # Print environment variables inside container
```

---

## 08. Docker Compose
🔗 **Full Lesson:** [08_docker_compose.md](./08_docker_compose.md)

* **Why It Exists**: Simplifies the management of multi-container applications (e.g., frontend + backend + database + cache). Instead of running dozens of verbose CLI commands, you define the entire stack in a single YAML file.
* **Real-World Analogy**: **Orchestra Conductor**. The YAML file acts as the musical sheet, directing all services on when to start, how to interact, and what volume/network to share.

### Key Commands:
```bash
docker compose up -d                                           # Start stack in background (creates network, volumes, containers)
docker compose down                                            # Stop and destroy stack (cleans up resources)
docker compose logs -f <service_name>                          # Follow logs for a specific container service
docker compose ps                                              # View status of running stack services
docker compose up --build                                      # Force rebuild of Dockerfile images before startup
```

### Gotcha: `depends_on`
The `depends_on` instruction controls container **startup order** (e.g., starting database container before application container). It does **not** wait for the database application to be ready to accept connections. Your application code must implement connection retry logic.

---

## 09. Multi-Stage Builds
🔗 **Full Lesson:** [09_multi_stage_builds.md](./09_multi_stage_builds.md)

* **Why It Exists**: Frontend apps (React, Next.js) require heavy build dependencies (Node, NPM, compilers). However, their final output is simple static files served by Nginx. Multi-stage builds compile code in a heavy environment, then copy only the compiled output into a lightweight production container.
* **Real-World Analogy**: **Kitchen (Stage 1)** has heavy mixers, ovens, flour bags. The **Cafe counter (Stage 2)** only receives the baked bread. You don't bring the mixer and garbage to the serving area.

### Production Example (React App Dockerfile):
```dockerfile
# Stage 1: Build compilation
FROM node:22-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Final lightweight image
FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

---

## 10. Image Optimization
🔗 **Full Lesson:** [10_image_optimization.md](./10_image_optimization.md)

* **Why It Exists**: Smaller images result in faster build times, faster deployment downloads, lower network/storage cloud costs, and a significantly smaller security attack surface.
* **Optimization Strategies**:
  1. **Minimal Base Image**: Choose `alpine` or Google’s `distroless` over full distributions (e.g., Ubuntu).
  2. **Optimize Cache Order**: Copy dependency manifests (`package.json`) and run installs *before* copying the rest of the code files.
  3. **Minimize Layers**: Combine consecutive commands (e.g., `RUN apt-get update && apt-get install -y && rm -rf /var/lib/apt/lists/*` to clean up temporary caches in the same layer).
  4. **Exclude Files**: Write a `.dockerignore` file to block folders like `node_modules`, `.git`, or logs from entering the build context.

### Layer Analysis Commands:
```bash
docker history my-app:latest                                   # Check size contribution of each build layer
docker system prune -a --volumes                               # Full cleanup of builder cache and unused images
```

---

## 11. Container Debugging
🔗 **Full Lesson:** [11_container_debugging.md](./11_container_debugging.md)

* **Real-World Analogy**: Modern cars have computer covers blocking mechanical access. You must plug in diagnostic tools (CLI commands) to retrieve error logs.
* **Common Trap: `localhost`**: Inside a container, `localhost` (or `127.0.0.1`) references the container itself. Connecting to host database systems requires using the host IP or establishing a unified Docker network.

### Debugging Commands:
```bash
docker logs -f --tail 100 <container>                          # Follow logs showing only last 100 lines
docker inspect <container> | grep ExitCode                     # Extract exit codes from stopped containers
docker exec -it <container> sh                                 # Launch interactive shell inside running container
docker stats                                                   # Real-time CPU, memory, and networking stats
docker top <container>                                         # Show running processes inside container
docker cp <container>:/app/logs.txt ./local-logs.txt           # Copy log files from container to host filesystem
```

---

## 12. Container Security
🔗 **Full Lesson:** [12_container_security.md](./12_container_security.md)

* **Why It Exists**: Containers share the host kernel. If a container is compromised and runs as `root`, an attacker can escape the container and compromise the entire host server.
* **Security Pillars**:
  1. **Least Privilege**: Never run application processes as root inside the container. Use `USER node` or `--user 1000`.
  2. **Image Scans**: Scan code dependencies and image packages for vulnerabilities during CI/CD checks.
  3. **Read-Only Filesystem**: Lock down container filesystems using `--read-only` to prevent malware installation.
  4. **Secret Protection**: Pass API keys at runtime via environment variables; never bake keys into image layers using `ENV` in a Dockerfile.

### Security Commands:
```bash
docker scout quickview node:22                                 # Scan image for CVE vulnerabilities
docker run --read-only alpine touch /tmp/test                 # Test container with read-only constraint
docker run --user 1000 alpine whoami                           # Force container to execute as non-root user UID
```

### Safe production Dockerfile permissions:
```dockerfile
FROM node:22-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY --chown=node:node . .                                     # Changes ownership of source files to node user
USER node                                                      # Switches to node user context
CMD ["node", "app.js"]
```

---
