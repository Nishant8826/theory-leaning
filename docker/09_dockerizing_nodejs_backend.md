# Dockerizing a Node.js & TypeScript Backend

---

### What
"Dockerizing" simply means taking an existing project and writing a robust `Dockerfile` for it so it can be packaged. In this section, we focus on Dockerizing a modern Node.js application built with TypeScript.

---

### Why
Using TypeScript introduces a completely new step: compilation. Your Node.js server cannot read `.ts` files naturally; they must be compiled to `.js` files using the `tsc` compiler before running. The Dockerfile must account for this build step!

---

### How
1. We start from a Node.js base image.
2. We copy our `package.json` and install dependencies.
3. We copy the raw `.ts` source code files.
4. We explicitly run a terminal command `npm run build` inside Docker to compile TypeScript into `/dist/` javascript files.
5. We set the `CMD` to run the compiled Javascript file `/dist/index.js`, not the TypeScript file.

---

### Implementation

Here is an effective Dockerfile for a TypeScript Node.js backend.

```dockerfile
# File: Dockerfile

# Start with a lightweight OS containing Node 18
FROM node:18-alpine

# Set working directory
WORKDIR /usr/src/app

# Copy dependency configs
COPY package*.json ./
COPY tsconfig.json ./

# Install ALL dependencies (including TypeScript plugins inside DevDependencies)
RUN npm install

# Copy all the raw .ts source code located in /src
COPY ./src ./src

# EXECUTE the TypeScript compiler (turns .ts into .js inside a /dist folder)
RUN npm run build 

# Expose port (Documentation only)
EXPOSE 4000

# Notice we run the compiled JS file, NOT the TS file!
CMD ["node", "dist/index.js"]
```

---

### Steps
1. Ensure your `package.json` has a build script: `"build": "tsc"`.
2. Ensure your `tsconfig.json` specifies `"outDir": "./dist"`.
3. Drop the Dockerfile above into the project.
4. Run `docker build -t ts-backend .`

---

### Integration

* **React/Next.js/Node.js:** Node.js backend logic in Docker translates highly into production environments perfectly. Be careful not to use massive Node frameworks (like `node:18`) without the `-alpine` suffix in production, otherwise your TypeScript backend Image could exceed 1.2GBs entirely unnecessarily. 
* **.dockerignore:** Very important! Create a `.dockerignore` file and add `node_modules`. If you don't do this, Docker will copy your massive physically installed Windows modules into the Linux environment, causing severe C++ binding crashes! Let Docker fetch its own modules via `RUN npm install`.

---

### Impact
Dockerizing TypeScript provides absolute guarantee that if the compilation succeeds locally on your Mac, it will absolutely compile and run on an AWS Linux server without TS versioning conflicts or missing configuration structures. 

---

### Interview Questions
1. **When Dockerizing a TypeScript application, what extra `RUN` step is practically always required?**
   *Answer: You must invoke a build step (like `RUN npm run build`) to execute the `tsc` compiler, transpiling the TypeScript `.ts` code into standard Node.js executable `.js` code.*
2. **Why is creating a `.dockerignore` file containing `node_modules` critical?**
   *Answer: It prevents you from overriding Linux container native binaries with potentially incompatible Host-OS binaries (like Windows C++ bindings), and significantly speeds up compilation by preventing transferring hundreds of megabytes from the host machine.*

---

### Summary
* TypeScript must be compiled inside the Docker build phase.
* Copy `tsconfig.json` early alongside package managers.
* `CMD` must trigger the resulting `.js` artifact inside the output directory.
* Never copy `node_modules` manually into a container.

---
Prev : [08_docker_compose_full_stack.md](./08_docker_compose_full_stack.md) | Next : [10_dockerizing_react_and_nextjs.md](./10_dockerizing_react_and_nextjs.md)
