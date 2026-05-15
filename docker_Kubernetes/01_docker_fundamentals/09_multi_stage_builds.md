# Multi-Stage Builds

## Why This Exists
When building applications like React or Next.js, you need heavy tools (like Node.js, npm, and compiler tools) to build the production assets. However, once the assets are built (just static HTML, JS, and CSS), you don't need Node.js or `node_modules` anymore. You just need a web server like Nginx to serve them.

If you use a single Dockerfile, your final production image will contain all the build tools and source code, making it massive (hundreds of MBs or even GBs). This makes deployments slow and increases the security attack surface.

Multi-stage builds allow you to use multiple `FROM` statements in a single Dockerfile. You can use a heavy image for building and copy only the artifacts to a lightweight image for the final production container.

## Real World Analogy
Think of Multi-Stage builds like **Baking bread in a professional kitchen vs serving it in a cafe**.
- In the **Kitchen (Stage 1)**, you have heavy mixers, bags of flour, ovens, and trash. This is the build stage.
- Once the bread is baked, you don't take the mixer and the trash to the **Cafe (Stage 2)**. You only take the finished loaf of bread.

The customer (the production environment) only sees the bread, not the messy kitchen used to make it.

## Core Concepts
- **Stages**: Different sections of a Dockerfile, each starting with a `FROM` instruction.
- **`AS` keyword**: Used to name a stage (e.g., `FROM node:18 AS builder`).
- **`COPY --from`**: Copies files from a previous stage into the current stage.

## Architecture / Flow

```text
[Stage 1: Build]
- Uses heavy image (Node)
- Installs dependencies
- Generates build artifacts
        |
        | COPY --from=build
        v
[Stage 2: Production]
- Uses light image (Nginx)
- Copies ONLY artifacts
- Result: Small & secure image
```


## Practical Commands
No special commands are needed to run multi-stage builds. You just use the standard build command:
```bash
docker build -t my-app:prod .
```
Docker automatically handles the stages.

## Hands-On Exercise
Let's create a Dockerfile that builds a dummy static site.

1. Create a `Dockerfile`:
   ```dockerfile
   # Stage 1: Build stage
   FROM alpine AS builder
   WORKDIR /build
   # Simulate building something by creating a file
   RUN echo "Hello from the build stage" > output.txt

   # Stage 2: Final stage
   FROM alpine
   WORKDIR /app
   # Copy the file from the builder stage
   COPY --from=builder /build/output.txt .
   # Verify the file is there
   CMD ["cat", "output.txt"]
   ```
2. Build and run:
   ```bash
   docker build -t multi-stage-test .
   docker run --rm multi-stage-test
   ```
   You should see `Hello from the build stage`. Notice that the final image is extremely small because it doesn't contain any build artifacts other than the one file we copied.

## Mini Project
**Task**: Create a production Dockerfile for a React application.

1. Create a `Dockerfile` in your React project root:
   ```dockerfile
   # Stage 1: Build the React application
   FROM node:22-alpine AS build
   WORKDIR /app
   COPY package*.json ./
   RUN npm install
   COPY . .
   RUN npm run build

   # Stage 2: Serve the application with Nginx
   FROM nginx:alpine
   # Copy static files from build stage to Nginx html directory
   COPY --from=build /app/build /usr/share/nginx/html
   EXPOSE 80
   CMD ["nginx", "-g", "daemon off;"]
   ```

## Real Production Usage
This is the standard way to build frontend applications (React, Vue, Angular) and compiled languages (Go, Rust, Java) in production.
- **Go**: You use a Go image to compile the binary (heavy), and then copy the binary to a scratch (empty) image or a minimal alpine image (extremely light).
- **Security**: The final image doesn't contain package managers or shell tools (if using distroless images), making it very hard for hackers to exploit if they gain access.

## Common Mistakes
- **Not naming stages**: You can copy from stage index (e.g., `COPY --from=0`), but it makes the Dockerfile hard to read. Always name your stages using `AS`.
- **Including source code in the final stage**: Make sure you only copy the *build artifacts* (like the `build/` or `dist/` folder), not the `src/` folder.

## Debugging Guide
- **File not found during copy**:
  - Double check the paths in the `--from` stage. They are relative to the `WORKDIR` of that stage.
  - Verify that the previous stage actually generated the files.

## Best Practices
- **Use specific stages for specific jobs**: You can have more than two stages (e.g., Stage 1: Install, Stage 2: Test, Stage 3: Build, Stage 4: Serve).
- **Keep the final image as small as possible**: Use `alpine` or `distroless` for the final stage.

## Interview Questions
1. **Why do we use multi-stage builds?**
   *Answer*: To reduce the size of the final production image and improve security by excluding build tools and source code.
2. **How do you copy files from one stage to another in a Dockerfile?**
   *Answer*: Using the `COPY --from=<stage_name_or_index>` instruction.

## Summary
Multi-stage builds are a must-have skill for production Docker usage. They allow you to keep your development environment rich with tools while keeping your production images lean, fast, and secure.

---
Prev: [08_docker_compose.md](./08_docker_compose.md) | Index: [Index](../00_index.md) | Next: [10_image_optimization.md](./10_image_optimization.md)
