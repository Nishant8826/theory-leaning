# 📌 Topic: Build Pipelines

## What
### 🧠 Concept Explanation
A Build Pipeline is the automated sequence of steps that transforms raw source code into a deployable software product. In Node.js, this often involves "Transpilation" (converting TS to JS), "Bundling," and "Containerization."

**The Manufacturing Blueprint Analogy (Deep Dive):**
Imagine you are building high-end custom furniture.
*   **The Raw Code (The Lumber):** You have raw wood and a set of instructions. This is the code in your Git repo.
*   **The Build Stage (The Workshop):**
    *   **Transpilation (Babel/TSC):** You use a machine to sand down the rough edges of the wood. You're turning "Raw Wood" (Modern JS/TypeScript) into "Finished Planks" (Node-compatible JS).
    *   **Bundling (Webpack/Esbuild):** You glue the planks together to form a chair. You combine 100 small files into 1 or 2 large, efficient files.
    *   **Artifact (The Finished Chair):** The chair is now ready. It's solid, it's painted, and it has a version number (`v1.0.0`) stamped on the bottom. 
*   **The Registry (The Warehouse):** You put the chair in a box (A Docker Image) and store it in a temperature-controlled warehouse. 
*   **Deployment (The Living Room):** When a customer buys it, you don't "build" the chair again in their house. You just move the box from the warehouse to their room. This ensures the chair they saw in the showroom is the *exact* one they get.

---

### 🏗️ Mental Model
Think of Build Pipelines as **The Forge of Immutability**.
1.  **Code is Volatile:** It changes every minute.
2.  **Artifacts are Frozen:** Once a build is complete, that version (e.g., `image:v42`) can never be changed. If you find a typo, you don't "edit" v42; you build a new `v43`.
3.  **Consistency is King:** The build environment must be isolated. If it works in the pipeline, it *must* work in production because the artifact is identical.

---

## Why
### 🏢 Best Practices
1.  **Build Once, Deploy Everywhere:** The same Docker image should go to Dev, Staging, and Prod.
2.  **Semantic Versioning:** Follow SemVer strictly.
3.  **Keep it Fast:** A build pipeline should take less than 5-10 minutes. If it's longer, developers will stop checking their code.

---

### ⚖️ Trade-offs
*   **Docker Images:** Very reliable, easy to scale, but large and complex to manage.
*   **Zip Artifacts:** Small and fast, but rely on the destination server having the right version of Node installed.

---

## How
### ⚡ Actual Behavior
In a Node.js build pipeline:
1.  **Environment Cleaning:** The builder (Jenkins, GitHub Action, etc.) starts with a completely empty filesystem. It "Clones" the code and runs `npm ci`.
2.  **Static Analysis:** Tools like `ESLint` and `SonarQube` read the code without running it, looking for patterns that lead to bugs or security holes.
3.  **Transpilation:** For TypeScript apps, `tsc` runs. This is often the slowest step. It checks for type errors and generates the `.js` and `.d.ts` files in a `dist` or `build` folder.
4.  **Containerization:** A `Dockerfile` is used to create an "Image." This image contains the Node.js runtime, your `dist` folder, and only the production `node_modules`. This image is a self-contained "Planet" that can run on any server in the world.

---

### 🔬 Internal Mechanics (V8 + libuv + OS)
*   **Tree Shaking and Dead Code Elimination:** Modern build tools (like `esbuild` or `Rollup`) analyze the "Dependency Graph" of your code. If you import a library like `lodash` but only use one function, the build tool will "shake" the tree until only that one function is left, discarding the rest of the library. This drastically reduces the V8 memory footprint at runtime.
*   **Source Maps:** Because the build process "Minifies" and "Munges" your code (e.g., renaming `function calculateUserBalance` to `function a`), debugging in production would be impossible. The build generates a `.map` file—a dictionary that links the ugly production code back to your beautiful source code.
*   **The NPM Pruning Process:** When building a production artifact, we run `npm prune --production`. This tells the OS to delete all `devDependencies` (like test runners and linters), which can often reduce the `node_modules` size by 70-80%.
*   **Layered Caching (Docker):** Docker builds are "Layered." Each command in a Dockerfile (like `COPY` or `RUN`) creates a new layer. If you haven't changed your `package.json`, the OS will reuse the "Cached Layer" for `npm install`, making subsequent builds take seconds instead of minutes.
*   **V8 Bytecode Pre-compilation:** Some advanced pipelines (like those for AWS Lambda) actually "Pre-warm" the V8 bytecode. They run the code once during the build so that V8 can generate and cache the optimized machine code, eliminating "Cold Start" latency for the end user.

---

### 🔁 Execution Flow
1.  **Code Check:** Ensure `package-lock.json` is present.
2.  **Lint:** Check for code style errors.
3.  **Build:** Run `npm run build` to generate the `dist` or `build` folder.
4.  **Dockerize:** Create a `Dockerfile` and run `docker build -t myapp:1.0.0 .`.
5.  **Push:** Upload the image to a Registry (Docker Hub, ECR).
6.  **Archive:** Store the `dist` folder in Jenkins or S3 for fallback.

---

### 🔍 Code Example (Latest Node.js - Multi-stage Dockerfile)
```dockerfile
# Stage 1: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Production
FROM node:20-alpine
WORKDIR /app
# Only copy the production dependencies and the build folder
COPY --from=builder /app/package*.json ./
RUN npm ci --omit=dev
COPY --from=builder /app/dist ./dist

EXPOSE 3000
CMD ["node", "dist/app.js"]
```

---

## Impact
### 💥 Production Failures
*   **Large Images:** Creating a 1GB Docker image for a 10MB app, causing deployments to take 10 minutes instead of 30 seconds. (Solution: Use `alpine` images and multi-stage builds).
*   **Building in Production:** Running `npm install` on your production server. If the npm registry is down, you can't scale or restart. Always build the artifact *before* deployment.

---

### 🧪 Real-time Scenarios
*   **Rolling Back:** Traffic is failing. You simply tell Kubernetes to use the previous artifact version `myapp:1.0.1` instead of `1.0.2`. It takes seconds.
*   **Preview Environments:** Building a unique URL for every Pull Request so the product manager can test the feature before it's merged.

---

### ⚠️ Edge Cases
*   **Non-deterministic Builds:** A build that gives different results on different machines (e.g., because it uses the current timestamp in the file hash). This makes debugging impossible.
*   **Dependency Hijacking:** An attacker releases a malicious version of a package your build uses. (Solution: Use `package-lock.json` and `npm audit`).

---

---

Prev: [01_NodeJS_in_Jenkins.md](./01_NodeJS_in_Jenkins.md) | Index: [NodeJS/00_Index.md](../00_Index.md) | Next: [03_Test_Automation.md](./03_Test_Automation.md)
