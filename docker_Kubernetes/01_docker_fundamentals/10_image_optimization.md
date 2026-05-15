# Image Optimization

## Why This Exists
In production, image size matters.
- **Speed**: Smaller images download faster. When you deploy a new version, or when Kubernetes scales up your app, the new container starts faster if the image is small.
- **Cost**: Cloud providers charge for storage and data transfer. Smaller images reduce these costs.
- **Security**: Smaller images have fewer packages, which means fewer security vulnerabilities (CVEs).

Optimizing your images is not just about making them small; it's about making them secure and fast to build.

## Real World Analogy
Think of Image Optimization like **Packing for a backpacking trip vs packing for a car trip**.
- For a car trip, you can take heavy bags, extra shoes, and large bottles of shampoo.
- For a backpacking trip (Production), every gram counts. You take lightweight gear, transfer liquids to small bottles, and leave behind anything you don't absolutely need.

An optimized Docker image is the backpacking gear.

## Core Concepts
- **Base Image**: The starting point. Choose minimal ones like `alpine` or `distroless`.
- **Layers**: Every `RUN`, `COPY`, and `ADD` instruction creates a layer. Combine them to reduce overhead.
- **Cache**: Reusing layers from previous builds to speed up the current build.
- **.dockerignore**: Preventing unnecessary files from entering the image.

## Architecture / Flow

```text
[Standard Image] (1GB)
        |
        | 1. Use Alpine base
        v
[Alpine Image] (200MB)
        |
        | 2. Multi-stage build
        v
[Artifacts Only] (50MB)
        |
        | 3. Combine RUN commands
        v
[Optimized Image] (30MB)
```


## Practical Commands
```bash
# Check the size of your images
docker images

# Check the size of each layer in an image
docker history <image_name>

# Prune unused images and builders to free up space
docker system prune -a
```

## Hands-On Exercise
Let's compare the size of a standard Node image vs an Alpine Node image.

1. Pull both images:
   ```bash
   docker pull node:22
   docker pull node:22-alpine
   ```
2. Check their sizes:
   ```bash
   docker images | grep node
   ```
   *Observation*: Notice the massive difference. The standard image is likely around 900MB+, while the alpine image is around 100MB+.

## Mini Project
**Task**: Optimize a Dockerfile for a Node.js application.

**Before (Unoptimized)**:
```dockerfile
FROM node:18
WORKDIR /app
COPY . .
RUN npm install
CMD ["node", "app.js"]
```

**After (Optimized)**:
```dockerfile
FROM node:22-alpine
WORKDIR /app
# Copy only package files first to leverage cache
COPY package*.json ./
# Install only production dependencies
RUN npm ci --only=production
# Copy the rest of the code
COPY . .
# Use a non-root user for security
USER node
CMD ["node", "app.js"]
```

## Real Production Usage
- **Distroless Images**: Google provides "distroless" images that contain only your application and its runtime dependencies. They do not contain package managers, shells, or any other programs you would expect to find in a standard Linux distribution. This is the gold standard for security.
- **CI/CD Caching**: In GitHub Actions or AWS CodePipeline, you configure cache for Docker layers so that if your `package.json` didn't change, the `npm install` step is skipped, making builds take seconds instead of minutes.

## Common Mistakes
- **Installing devDependencies in production images**: Running `npm install` without `--only=production` includes test frameworks and build tools in the final image.
- **Not using `.dockerignore`**: Accidentally copying massive `node_modules` folders or secret files into the image.
- **Too many layers**: Having separate `RUN` commands for updating apt, installing a package, and cleaning up. Combine them!

## Debugging Guide
- **Why is my image so big?**
  - Run `docker history <image_name>` to see which layer is adding the most megabytes.
  - Check if you forgot to delete temporary files or cache files after installing packages.

## Best Practices
- **Use Alpine or Distroless as base images**.
- **Leverage Docker layer caching** by copying dependency files first.
- **Combine `RUN` commands** to avoid creating unnecessary layers.
- **Clean up package manager cache** in the same `RUN` command (e.g., `rm -rf /var/cache/apk/*`).

## Interview Questions
1. **How do you reduce the size of a Docker image?**
   *Answer*: Use smaller base images (like Alpine), use multi-stage builds, combine commands to reduce layers, use `.dockerignore`, and install only production dependencies.
2. **Why is it important to put `COPY package.json` before `COPY .`?**
   *Answer*: Because Docker caches layers. If `package.json` hasn't changed, Docker will reuse the cached layer for `npm install`, making the build much faster.

## Summary
Image optimization is about balance: making the image as small and secure as possible while keeping it functional. Always use Alpine bases, leverage caching, and clean up after yourself.

---
Prev: [09_multi_stage_builds.md](./09_multi_stage_builds.md) | Index: [Index](../00_index.md) | Next: [11_container_debugging.md](./11_container_debugging.md)
