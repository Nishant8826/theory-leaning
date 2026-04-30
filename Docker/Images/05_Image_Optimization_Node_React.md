# 📌 Topic: Image Optimization (Node.js & React)

## 🧠 Concept Explanation (Basic → Expert)
**Basic**: Images for Node and React can become huge (over 1GB) because of `node_modules`. Optimization is about making them small and secure.
**Expert**: Optimized Node/React images require a **Tri-Stage Architecture**: 
1. **Dependency Stage**: Installing `devDependencies` for building/testing.
2. **Build Stage**: Compiling TypeScript/Sass and creating the production bundle.
3. **Runtime Stage**: Using a minimal base (Alpine/Distroless) and copying ONLY the production files. 
Staff-level optimization also includes **Layer Cache Optimization** (copying `package.json` first), **Removing Sensitive Data** (`.npmrc`), and **Production-only pruning** (`npm prune --production`).

## 🏗️ Mental Model
- **The Backpack**: When you go hiking, you don't take your whole wardrobe. You only take the clothes you'll wear and the food you'll eat. An optimized image is a perfectly packed backpack for a production "hike."

## ⚡ Actual Behavior
- **The `node_modules` Bloat**: A standard `npm install` for a React app can easily add 500MB to your image. Most of these are build tools (Webpack, Babel) that are useless once the `dist` folder is created.
- **Multi-Stage Magic**: By using multi-stage builds, you can reduce a React image from 800MB to 20MB (just the Nginx server and the static HTML/JS).

## 🔬 Internal Mechanics (The Pruning)
1. `npm install` installs everything (`dependencies` + `devDependencies`).
2. After building the app, `npm prune --production` deletes the `devDependencies` (test runners, linters, types).
3. The remaining `node_modules` are significantly smaller and safer (less code = less attack surface).

## 🔁 Execution Flow
1. **Base**: Define Node version and Alpine base.
2. **Deps**: Copy `package.json`, install ALL dependencies (including dev).
3. **Build**: Copy source code, run `npm build`.
4. **Final (React)**: Copy only the `/dist` folder into an `nginx:alpine` image.
5. **Final (Node)**: Copy only production `node_modules` and compiled JS into a fresh `node:alpine` image.

## 🧠 Resource Behavior
- **Memory**: Smaller images start faster and use less "Page Cache" memory on the host.
- **Disk**: 100 microservices x 1GB = 100GB. Optimized: 100 x 50MB = 5GB. Huge savings in cloud storage costs.

## 📐 ASCII Diagrams (REQUIRED)

```text
       NODE/REACT OPTIMIZATION FLOW
       
[ BUILDER STAGE ]                  [ RUNNER STAGE ]
- Full Node OS                     - Alpine / Nginx
- npm, git, gcc                    - No shell / tools
- 1GB node_modules                 - 20MB Static files
- Secret .npmrc                    - Clean env
       |                                  |
[ npm run build ] --(COPY --from)--> [ /app/dist ]
```

## 🔍 Code (Production Dockerfile for Node/React)
```dockerfile
# --- Stage 1: Install Dependencies ---
FROM node:18-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

# --- Stage 2: Build the Application ---
FROM node:18-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build
# Prune devDependencies for Node backend
RUN npm prune --production

# --- Stage 3: Final Production Image (Node Backend) ---
FROM node:18-alpine AS runner
WORKDIR /app
ENV NODE_ENV production
# Create non-root user
RUN addgroup -S nodeapp && adduser -S nodeapp -G nodeapp
# Copy only production modules and build output
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
USER nodeapp
CMD ["node", "dist/main.js"]

# --- ALTERNATIVE Stage 3: Final Image (React Frontend) ---
# FROM nginx:alpine
# COPY --from=builder /app/dist /usr/share/nginx/html
# EXPOSE 80
# CMD ["nginx", "-g", "daemon off;"]
```

## 💥 Production Failures
- **The "Missing Dependency" Crash**: You run `npm prune --production` but your app uses a library at runtime that you accidentally listed in `devDependencies`. The image builds, but the app crashes in production with `module not found`.
- **The "Root User" Vulnerability**: Leaving the default `root` user in a Node image. If your app has a directory traversal bug, the attacker can overwrite system files.
  *Fix*: Use `USER node`.

## 🧪 Real-time Q&A
**Q: Should I use `npm install` or `npm ci`?**
**A**: In Docker, ALWAYS use `npm ci`. It is faster, more reliable, and strictly follows the `package-lock.json`. It also deletes existing `node_modules` before starting, ensuring a clean build.

## ⚠️ Edge Cases
- **Native Modules**: Libraries like `bcrypt` or `sharp` need to be compiled for the specific OS. If you build in a Debian builder and copy to an Alpine runner, the app will crash.
  *Fix*: Ensure both stages use the same base image (e.g., both use `alpine`).

## 🏢 Best Practices
- **Use `.dockerignore`**: Exclude `node_modules` and `dist` from being copied from your laptop (they should be built *inside* Docker).
- **Environment Variables**: Set `NODE_ENV=production`. Many libraries (like Express) optimize themselves when this is set.
- **Avoid `latest` tags**: Use specific versions (`node:18.16.0-alpine`) to ensure your builds are reproducible.

## ⚖️ Trade-offs
| Strategy | Complexity | Security | Size |
| :--- | :--- | :--- | :--- |
| **Standard Build** | **Low** | Low | High |
| **Multi-Stage** | Medium | **High** | **Small** |
| **Distroless** | High | **Highest** | **Smallest** |

## 💼 Interview Q&A
**Q: How do you handle secrets (like a private NPM token) during a Docker build?**
**A**: I use **BuildKit Secret Mounts**. I never use `ARG` or `ENV` because those are baked into the image history. Instead, I use `RUN --mount=type=secret,id=npmrc,target=/root/.npmrc npm install`. This makes the secret available to the `npm install` command but ensures it is never saved in any image layer.

## 🧩 Practice Problems
1. Build a basic React image. Check the size. Refactor it into a multi-stage build with an Nginx runner. Check the size again.
2. Verify that `USER node` is working by running `docker exec -it <id> whoami` inside your container.

---
Prev: [04_Multi_Arch_Images.md](./04_Multi_Arch_Images.md) | Index: [00_Index.md](../00_Index.md) | Next: [06_Base_Images_and_Security.md](./06_Base_Images_and_Security.md)
---
