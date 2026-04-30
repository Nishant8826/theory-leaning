# 📌 Topic: Multi-Stage Builds (Optimization)

## 🧠 Concept Explanation (Basic → Expert)
**Basic**: Multi-stage builds allow you to use one "big" image for building your code (with compilers and tools) and then copy the finished result to a "tiny" image for running it. This makes the final image much smaller.
**Expert**: Multi-stage builds are a **Build Pipeline Pattern** that allows you to define multiple `FROM` instructions in a single Dockerfile. Each `FROM` starts a new stage. You can "cherry-pick" specific artifacts (binaries, static files, compiled modules) from one stage to another using `COPY --from`. Staff-level engineering uses this to **Eliminate Attack Surface** (removing compilers/shell from production) and **Minimize Cold Start Latency** by reducing the image size from GBs to MBs.

## 🏗️ Mental Model
- **The Construction Site**: A building needs cranes, bulldozers, and scaffolding to be built. But you don't want the cranes and bulldozers to be inside the house when the family moves in. Multi-stage builds are the process of building the house and then moving only the furniture into the finished home.

## ⚡ Actual Behavior
- **Layer Discarding**: When the build finishes, Docker only keeps the layers from the **LAST** stage. All the layers from previous "build" stages are discarded (though they may stay in the build cache).
- **Parallelism**: BuildKit can run independent stages in parallel (e.g., building a Java backend and a React frontend simultaneously).

## 🔬 Internal Mechanics (Artifact Extraction)
1. **The Builder Stage**: Contains the full JDK, Node.js, or Go compiler. It clones the repo, installs dependencies, and runs the build command.
2. **The Result**: A static binary or a `dist` folder.
3. **The Runner Stage**: Starts with a minimal base (like `alpine` or `distroless`). It uses `COPY --from=builder /src/app /app` to pull only the compiled binary.
4. **Cleanup**: The builder's `node_modules` (1GB+), `.git` folder, and compiler tools are gone.

## 🔁 Execution Flow
1. Stage 1 (`AS build`): `npm install` -> `npm run build`.
2. Stage 2 (`AS test`): Runs unit tests against the build.
3. Stage 3 (`AS final`): Starts with Nginx.
4. `COPY --from=build /app/dist /usr/share/nginx/html`.
5. Docker exports ONLY Stage 3 as the final image.

## 🧠 Resource Behavior
- **Registry Costs**: Smaller images mean lower storage costs in ECR/Docker Hub.
- **Pull Speed**: An 800MB image takes minutes to pull on a slow network. A 40MB image takes seconds.

## 📐 ASCII Diagrams (REQUIRED)

```text
       MULTI-STAGE BUILD WORKFLOW
       
[ Stage 1: BUILDER ]         [ Stage 2: RUNNER ]
(node:18-heavy)              (node:18-alpine)
      |                            |
[ npm install ]                    |
[ npm build   ]                    |
      |                            |
      +----( COPY --from )---------+
      |                            |
[ Discarded Layers ]         [ Final Image (Small) ]
```

## 🔍 Code (Production Node/React Pattern)
```dockerfile
# STAGE 1: Build the React Frontend
FROM node:18-alpine AS build-frontend
WORKDIR /app/frontend
COPY frontend/package.json .
RUN npm install
COPY frontend/ .
RUN npm run build

# STAGE 2: Build the Node Backend
FROM node:18-alpine AS build-backend
WORKDIR /app/backend
COPY backend/package.json .
RUN npm install
COPY backend/ .
# (Optionally compile TypeScript here)

# STAGE 3: Final Production Image
FROM node:18-alpine
WORKDIR /app
# Copy backend code
COPY --from=build-backend /app/backend .
# Copy frontend static files into backend's public folder
COPY --from=build-frontend /app/frontend/dist ./public

EXPOSE 3000
CMD ["node", "index.js"]
```

## 💥 Production Failures
- **Missing Shared Libraries**: You build a C++ app in an Ubuntu builder and copy the binary to an Alpine runner. Alpine uses `musl` while Ubuntu uses `glibc`. The app fails to start with "File not found" or "Shared library error."
  *Fix*: Build on the same OS family as the runner.
- **Copying the Wrong Path**: You compile your app into `/app/build` but your `COPY --from` tries to pull from `/app/dist`. The build succeeds but the final image is empty/broken.

## 🧪 Real-time Q&A
**Q: Can I use more than two stages?**
**A**: Yes! Some complex pipelines have 5 or 6 stages: `base` -> `dependencies` -> `test` -> `build` -> `security-scan` -> `production`. BuildKit will manage the dependencies between them efficiently.

## ⚠️ Edge Cases
- **Debugging**: Because the production image doesn't have `bash`, `curl`, or `vim`, it is much harder to debug if something goes wrong. 
  *Fix*: Use `docker exec` with a sidecar or use a "debug" version of your image.

## 🏢 Best Practices
- **Name your stages**: Use `FROM image AS name` instead of referring to them by index (`--from=0`).
- **Use Distroless**: For maximum security, use Google's `distroless` images which contain *only* your app and its runtime dependencies (no shell, no package manager).
- **Stop at a specific stage**: Use `docker build --target build-step` to stop the build at a specific stage (useful for running tests in CI).

## ⚖️ Trade-offs
| Approach | Complexity | Security | Size |
| :--- | :--- | :--- | :--- |
| **Single Stage** | **Low** | Low | High |
| **Multi-Stage** | Medium | **High** | **Small** |

## 💼 Interview Q&A
**Q: Why are multi-stage builds considered a security best practice?**
**A**: They significantly reduce the "Attack Surface" of your container. In a single-stage build, your production container contains compilers (gcc), package managers (apt), and shell utilities (curl, wget) that an attacker could use to download malware or move laterally through your network. In a multi-stage build, those tools are left behind in the builder stage, and the final image contains only your application binary and the bare minimum libraries needed to run it.

## 🧩 Practice Problems
1. Take an existing "heavy" image you've built. Refactor it into a multi-stage build. Compare the size difference using `docker images`.
2. Try to build a Go or Rust application and copy the binary to a `scratch` image (the smallest possible image). Note the challenges with SSL certificates or timezone data.

---
Prev: [02_Layer_Caching_Strategies.md](./02_Layer_Caching_Strategies.md) | Index: [00_Index.md](../00_Index.md) | Next: [04_Multi_Arch_Images.md](./04_Multi_Arch_Images.md)
---
