# 📌 Topic: Dockerfile Execution Model

## 🧠 Concept Explanation (Basic → Expert)
**Basic**: A Dockerfile is a list of commands. Docker runs them one by one to create an image. If it has already run a command before, it uses the cached result.
**Expert**: The Dockerfile is a **Declarative Manifest** that is compiled into a series of **Build Instructions**. Each instruction that modifies the filesystem (like `RUN`, `COPY`, `ADD`) creates a new layer. Instructions that modify metadata (like `ENV`, `EXPOSE`, `CMD`, `ENTRYPOINT`) update the image configuration JSON. Modern Docker (via BuildKit) treats the Dockerfile as a **Dependency Graph**, allowing for parallel execution and stage skipping. Staff-level engineering requires understanding that the order of instructions determines the efficiency of the cache and the final image size.

## 🏗️ Mental Model
- **Dockerfile**: A recipe for a cake.
- **Layers**: The individual sponge layers, frosting, and toppings. If you change the bottom sponge, you have to throw away the whole cake and start again.
- **Metadata**: The instructions on the cake box (serve cold, contains nuts).

## ⚡ Actual Behavior
When you run `docker build`:
1. The client sends the **Build Context** (files) to the daemon.
2. The daemon parses the Dockerfile.
3. For each command, the daemon checks the cache.
4. If not in cache, it creates a transient container, executes the command, commits the result as a new layer, and then destroys the transient container.

## 🔬 Internal Mechanics (The Build Context)
The **Build Context** is often the biggest bottleneck.
1. When you run `docker build .`, the CLI zips up *everything* in the current directory and sends it to the Docker Daemon.
2. If you have a 1GB `.git` folder or `node_modules`, it is sent every time, even if you don't use it.
3. BuildKit optimizes this by only sending the files that are actually referenced in `COPY` or `ADD` commands.

## 🔁 Execution Flow
1. `FROM`: Sets the base image layers.
2. `WORKDIR`: Creates the directory and sets the base path for subsequent commands.
3. `COPY/ADD`: Calculates file checksums and copies data.
4. `RUN`: Executes a shell command using `/bin/sh -c` (default).
5. `ENV/ARG`: Sets variables for build-time (ARG) and run-time (ENV).
6. `COMMIT`: Generates a layer ID and updates the manifest.

## 🧠 Resource Behavior
- **Disk IO**: Heavy during `COPY` and `RUN` commands (especially package installs).
- **Network**: Consumed during `FROM` (pulling base) and `RUN` (downloading packages).

## 📐 ASCII Diagrams (REQUIRED)

```text
       DOCKERFILE EXECUTION PIPELINE
       
[ Dockerfile ] -> [ Parser ] -> [ BuildKit Solver (DAG) ]
                                          |
          +-------------------------------+-----------------------+
          |                               |                       |
[ Cache Lookup ] --> [ Command Execution ] --> [ Snapshot Layer ] --> [ Manifest ]
          |                  |                       |
    (Using Cache)     (Transient Container)     (Content Hash)
```

## 🔍 Code (The "Staff-Level" Dockerfile)
```dockerfile
# syntax=docker/dockerfile:1
FROM node:18-alpine AS base

# Use a non-root user for security
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
WORKDIR /app

# Optimization: Copy only package files first
COPY package.json package-lock.json ./

# Use BuildKit cache mount to speed up install
RUN --mount=type=cache,target=/root/.npm \
    npm ci --only=production

# Copy rest of the code
COPY . .

# Final metadata
USER appuser
EXPOSE 3000
CMD ["node", "index.js"]
```

## 💥 Production Failures
- **The "Context Bomb"**: A developer runs `docker build .` from their home directory. Docker tries to send their entire `Documents`, `Downloads`, and `Pictures` folders (100GB+) to the daemon. The build hangs indefinitely.
  *Fix*: Use `.dockerignore`.
- **The "Layer Bloat"**: `RUN apt-get update`, `RUN apt-get install -y vim`, `RUN rm -rf /var/lib/apt/lists/*`. Because these are three separate layers, the 50MB of apt-get cache is permanently baked into Layer 2, even though you "deleted" it in Layer 3.
  *Fix*: Combine into one `RUN`.

## 🧪 Real-time Q&A
**Q: What is the difference between `ADD` and `COPY`?**
**A**: `COPY` is simple and preferred; it just copies files from your host. `ADD` is a "magic" command that can fetch files from URLs and automatically extract tarballs. Because `ADD`'s behavior is complex and less predictable, `COPY` is the best practice for 99% of use cases.

## ⚠️ Edge Cases
- **ARG vs ENV**: `ARG` variables are only available during the build. If you need a variable available when the container is *running*, you must use `ENV`. 
  *Warning*: Never put secrets (passwords) in `ARG` or `ENV`, as they are visible to anyone with `docker inspect`.

## 🏢 Best Practices
- **Use `.dockerignore`**: Exclude `.git`, `node_modules`, and logs.
- **Order by Fluctuation**: Stable layers (OS, Dependencies) at the top, volatile layers (Code, Config) at the bottom.
- **Small Base Images**: Use `alpine` or `distroless` to reduce attack surface and pull times.

## ⚖️ Trade-offs
| Decision | Pros | Cons |
| :--- | :--- | :--- |
| **Combine RUNs** | Smaller Image | Harder to debug intermediate steps |
| **Many COPYs** | Granular Caching | More metadata/layers |

## 💼 Interview Q&A
**Q: How can you reduce the size of a Docker image without changing the application code?**
**A**: 1. Use a smaller base image (like `alpine`). 2. Use multi-stage builds to discard build-time dependencies (compilers, git). 3. Combine multiple `RUN` commands into a single line to avoid creating intermediate layers with temporary files. 4. Ensure you are using a `.dockerignore` file to prevent copying unnecessary local files into the image.

## 🧩 Practice Problems
1. Create a Dockerfile for a Node.js app. Build it once. Change one line in `index.js` and build again. How many layers were cached?
2. Add a 1GB file to your directory. Build without `.dockerignore`. Observe the "Sending build context" time. Add the file to `.dockerignore` and observe the difference.

---
Prev: [09_System_Performance_Limits.md](../Core/09_System_Performance_Limits.md) | Index: [00_Index.md](../00_Index.md) | Next: [02_Layer_Caching_Strategies.md](./02_Layer_Caching_Strategies.md)
---
