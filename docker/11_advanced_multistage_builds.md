# Advanced: Multi-Stage Builds & .dockerignore

---

### What
- **Multi-Stage Builds:** A technique in Docker where you use *multiple* `FROM` commands in a single Dockerfile. You use one massive, heavy environment just to compile your code, and then you copy *only* the final compiled output into a tiny, pristine production container, leaving all the junk behind.
- **.dockerignore:** A file identical to `.gitignore` that tells Docker exactly which vast quantities of files it should fundamentally ignore during the heavy `COPY . .` command.

---

### Why
If you build a standard React single-page app, you require Node.js, `npm`, webpack, and a colossal `node_modules` folder (usually 600MB+) just to build the app. Your final static HTML/CSS files are only 5MB! If you ship the entire 600MB image to AWS, it costs significant cloud storage fees, drastically slows down load times, and creates massive security vulnerabilities (more libraries = more vectors to hack). Multi-stage solves this effortlessly by deleting the 600MB junk automatically.

---

### How
1. Initiate the **Builder Stage** using Node.js to `npm install` and `npm run build`.
2. Initiate the **Production Stage** using lightweight Nginx.
3. Use a specific Docker command: `COPY --from=builder` to pull the 5MB artifact over to Nginx.

---

### Implementation

A standard, highly-optimized Multi-Stage Dockerfile for a React UI:

```dockerfile
# ======= STAGE 1: BUILD ENVIRONMENT =======
FROM node:18-alpine AS builder

WORKDIR /app

# The '.' is relative to /app. The Docker daemon ignores anything in .dockerignore here!
COPY package*.json ./
RUN npm install
COPY . .

# Generates the minified, compiled /dist folder
RUN npm run build 


# ======= STAGE 2: PRODUCTION ENVIRONMENT =======
# Nginx is incredibly lean Web Server (often under 25MB)
FROM nginx:alpine

# Copy strictly the heavily optimized /dist artifact generated in STAGE 1!
# ALL previous folders, source code files, and node_modules from STAGE 1 are permanently deleted!
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80
# Nginx automatically spins up, serving the HTML files statically in microseconds.
CMD ["nginx", "-g", "daemon off;"]
```

And your absolute must-have `.dockerignore` file placement alongside it:

```text
# File: .dockerignore
node_modules
npm-debug.log
.git
.env
build/
dist/
Dockerfile
```

---

### Steps
1. Create a `.dockerignore` outlining heavy or sensitive development files.
2. Outline your Dockerfile to use an `AS builder` stage.
3. Identify precisely what output folder your framework compiler produces (`/dist`, `/build`, `/.next/standalone`).
4. Copy only that artifact path utilizing the `--from=builder` argument.

---

### Integration

* **React/Vue/Angular (Frontend):** This is the literal industry-standard gold rule. You completely forfeit the right to run arbitrary Node commands in a client-side frontend production container in return for an untouchably fast app.
* **TypeScript Backends:** This applies equally there! The builder stage invokes the `tsc` compiler. Stage 2 spins up a brand new pure Node environment and copies *only* the compiled `/dist/` Javascript files, completely eradicating the raw Type definitions and source maps.

---

### Impact
It shrinks image sizes by up to 95% (e.g., from 1.2 GB to 30 MB). Because hackers cannot exploit dev tools (like compilers) if those tools aren't even inside the server container, your security footprint hardens drastically.

---

### Interview Questions
1. **What is the central purpose of a Multi-Stage Docker build?**
   *Answer: To dramatically reduce the final Image footprint by isolating build-time dependencies into temporary intermediate layers and only shipping the finalized executable code layer to production.*
2. **If an image uses Multi-Stage Builds, can you run debugging compilation commands (like `npm run dev`) inside the resulting production container?**
   *Answer: No, because fundamentally the Node packages, dependencies, and internal source code necessary to accomplish compilation simply do not physically exist in the completed container filesystem.*
3. **What is exactly defined inside a `.dockerignore` file?**
   *Answer: Instructions indicating absolute paths, regular expressions, and configurations specifying folders the daemon must skip when executing arbitrary wide `COPY . .` commands, heavily utilized to prevent copying `node_modules` logic alongside source code.*

---

### Summary
* A `.dockerignore` file keeps local clutter out of your container builds.
* Multi-stage uses `AS builder` sequentially atop multiple `FROM` commands.
* We utilize `--from=builder` to extract compiled gold locally and disregard the structural scaffolding globally.

---
Prev : [10_dockerizing_react_and_nextjs.md](./10_dockerizing_react_and_nextjs.md) | Next : [12_advanced_networking_security.md](./12_advanced_networking_security.md)
