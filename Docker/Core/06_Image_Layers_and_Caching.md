# 📌 Topic: Image Layers and Caching (Internals)

## 🧠 Concept Explanation (Basic → Expert)
**Basic**: Docker images are built in steps. If you don't change a step, Docker reuses the result from the last time you built it. This makes builds fast.
**Expert**: Docker images are an ordered stack of **Immutable, Content-Addressable Layers**. Each instruction in a Dockerfile (`RUN`, `COPY`, `ADD`) that modifies the filesystem creates a new layer. Docker uses **SHA256 digests** of the layer content to identify them. If the digest matches a cached layer on the host, Docker skips the execution. Staff-level engineering focuses on **Cache Invalidation Optimization**—structuring the Dockerfile so that frequently changing parts (like source code) are at the bottom, while stable parts (like OS updates and dependencies) are at the top.

## 🏗️ Mental Model
- **Content-Addressable**: If two different people build a layer containing the exact same `package.json`, they will both get the exact same SHA256 ID. Docker doesn't need to know *how* it was built, only *what* is inside.
- **The "Cache Chain"**: If Layer 2 changes, every layer above it (3, 4, 5) MUST be rebuilt, even if their contents didn't change.

## ⚡ Actual Behavior
- **COPY/ADD Cache**: Docker calculates a checksum of the files being copied. If even 1 bit changes in your `src/`, the cache for that `COPY` command (and everything after it) is invalidated.
- **RUN Cache**: Docker simply looks at the string of the command. It does **NOT** know if the external world changed. If you run `RUN apt-get update`, Docker will use the cache from 6 months ago unless you force a rebuild or the command string itself changes.

## 🔬 Internal Mechanics (The Manifest)
An image is not just a pile of layers; it's a **Manifest JSON** file.
1. **Config**: Defines the environment variables, entrypoint, and user.
2. **Layers**: A list of SHA256 digests of the compressed tarballs that make up the filesystem.
3. **Storage**: Layers are stored in `/var/lib/docker/overlay2` and deduplicated. If 10 images use `alpine:latest`, that layer is stored only once on your disk.

## 🔁 Execution Flow
1. `docker build` starts.
2. Docker checks the first instruction.
3. It generates a "Build Context" (the files in your folder).
4. It compares the current instruction and the files involved against existing layer IDs.
5. If a match is found: "Using cache."
6. If no match: Executes the command, creates a new layer, and generates a new ID.
7. ALL subsequent instructions now lose their cache.

## 🧠 Resource Behavior
- **Build Speed**: Optimized caching can reduce build times from 10 minutes to 10 seconds.
- **Disk Usage**: Bloated layers (e.g., leaving `.git` or `node_modules` from a build stage) increase image size and slow down `docker pull` operations across the network.

## 📐 ASCII Diagrams (REQUIRED)

```text
       DOCKERFILE CACHE INVALIDATION
       
[ Dockerfile ]          [ Cache Status ]
-----------------------------------------
FROM node:18-alpine     | (CACHED)
WORKDIR /app            | (CACHED)
COPY package.json .     | (CACHED - package.json unchanged)
RUN npm install         | (CACHED - expensive step skipped!)
COPY . .                | (INVALIDATED - src/index.js changed)
RUN npm run build       | (REBUILT)
CMD ["node", "app.js"]  | (REBUILT)
```

## 🔍 Code (Optimized Node.js Pattern)
```dockerfile
# BAD: Any change in code invalidates npm install
COPY . .
RUN npm install

# GOOD: npm install is only rebuilt if package.json changes
COPY package.json package-lock.json ./
RUN npm install
COPY . .
```

## 💥 Production Failures
- **The "Stale Package" Bug**: You add a new dependency to `package.json`, but because you structured your Dockerfile poorly, Docker uses an old `node_modules` layer from the cache.
- **Security Vulnerabilities in Cache**: You have `RUN apt-get update && apt-get install -y openssl`. Because this is cached, your image never gets the latest security patches unless you use `--no-cache` or change the Dockerfile.

## 🧪 Real-time Q&A
**Q: Does `RUN apt-get update` check for new packages every time?**
**A**: No. Docker only checks if the string `RUN apt-get update` has been seen before. It has no idea if the Ubuntu servers have new updates. To force an update, you can add a build-arg like `RUN apt-get update && apt-get install -y ... # BUILD_DATE=2023-10-01`.

## ⚠️ Edge Cases
- **Layer Limits**: While there is a technical limit of 127 layers in the OverlayFS driver, you should practically aim for as few as possible to improve performance, though "squashing" layers is less necessary in modern Docker than it used to be.

## 🏢 Best Practices
- **Order Matters**: Put the most stable instructions at the top.
- **Specific `COPY`**: Don't `COPY . .` early. Only copy the specific files needed for the next step (like `package.json`).
- **Clean up in the same layer**: If you download a 100MB file, use it, and delete it in the same `RUN` command, it never becomes part of the image. If you delete it in a *different* `RUN` command, it still exists in the previous layer!

## ⚖️ Trade-offs
| Strategy | Build Speed | Image Size |
| :--- | :--- | :--- |
| **Many Small Layers**| High (Granular Cache)| Large (Metadata overhead) |
| **Few Large Layers** | Low (Big Rebuilds) | **Small** |
| **Multi-Stage** | **High** | **Smallest** |

## 💼 Interview Q&A
**Q: How does Docker deduplicate image layers?**
**A**: Docker uses **Content-Addressable Storage**. When a layer is created, Docker calculates a SHA256 hash of its content. This hash is the layer's ID. If you pull two different images that both happen to use the exact same Debian base layer, Docker sees that it already has a layer with that SHA256 ID on disk and simply points both images to the same physical data.

## 🧩 Practice Problems
1. Build an image, change a comment in your code, and rebuild. Observe which layers are cached.
2. Run `docker inspect <image>` and look at the `RootFS.Layers` section. Match these IDs to the layers shown in `docker history`.

---
Prev: [05_Container_Runtime_runc_containerd_OCI.md](./05_Container_Runtime_runc_containerd_OCI.md) | Index: [00_Index.md](../00_Index.md) | Next: [07_BuildKit_Internals.md](./07_BuildKit_Internals.md)
---
