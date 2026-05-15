# Dockerfile In-Depth

## Why This Exists
In the previous topics, we used pre-built images like `nginx` and `node`. But as a full-stack developer, you need to containerize **your own** applications. You need a way to tell Docker how to build an image for your specific React, Next.js, or Node.js app.

A `Dockerfile` is a text document that contains all the commands a user could call on the command line to assemble an image. It automates the process of image creation.

## Real World Analogy
Think of a `Dockerfile` as a **Recipe** or an **Automated Installation Script**.
If you were setting up a new server manually, you would:
1. Install an OS (Ubuntu).
2. Install Node.js.
3. Copy your code.
4. Run `npm install`.
5. Run `npm start`.

A `Dockerfile` is just a list of these exact steps, written in a way that Docker understands, so it can do it for you automatically.

## Core Concepts
- **FROM**: Sets the base image (usually a lightweight OS or runtime).
- **WORKDIR**: Sets the working directory inside the container.
- **COPY**: Copies files from your host machine to the container.
- **RUN**: Executes commands during the build process (e.g., installing packages).
- **ENV**: Sets environment variables.
- **EXPOSE**: Informs Docker that the container listens on the specified network ports at runtime (documentation only).
- **CMD**: Specifies the command to run when the container starts.

## Architecture / Flow

```text
+-------------------------+
| Source Code & Dockerfile|
+-------------------------+
            |
            | 1. docker build
            v
+-------------------------+
| Docker Image            |
| (Static, Read-Only)     |
+-------------------------+
            |
            | 2. docker run
            v
+-------------------------+
| Running Container       |
| (Isolated Environment + |
|  Writable Layer)        |
|                         |
| -> Executes CMD         |
+-------------------------+
```


## Practical Commands
```bash
# Build an image from a Dockerfile in the current directory
docker build -t my-app:v1 .

# Build an image with a specific file name
docker build -f Dockerfile.dev -t my-app:dev .

# Run the newly built image
docker run -d -p 3000:3000 my-app:v1
```

## Hands-On Exercise
Let's containerize a simple Node.js application.

1. Create a directory and a file named `server.js`:
   ```javascript
   const http = require('http');
   const server = http.createServer((req, res) => {
       res.end('Hello from my custom Docker image!');
   });
   server.listen(3000, () => console.log('Server running on port 3000'));
   ```
2. Create a file named `Dockerfile` (no extension) in the same directory:
   ```dockerfile
   # Use official Node.js runtime as a parent image
   FROM node:22-alpine

   # Set the working directory
   WORKDIR /app

   # Copy the server file to the container
   COPY server.js .

   # Expose port 3000
   EXPOSE 3000

   # Run the app
   CMD ["node", "server.js"]
   ```
3. Build and run:
   ```bash
   docker build -t my-node-server .
   docker run -d -p 3000:3000 my-node-server
   ```
4. Visit `localhost:3000`.

## Mini Project
**Task**: Containerize a React application using multi-stage builds (we will cover this in detail later, but here is a taste).

1. Imagine you have a standard React app.
2. Create a `Dockerfile`:
   ```dockerfile
   # Stage 1: Build
   FROM node:22-alpine AS builder
   WORKDIR /app
   COPY package*.json ./
   RUN npm install
   COPY . .
   RUN npm run build

   # Stage 2: Serve
   FROM nginx:alpine
   COPY --from=builder /app/build /usr/share/nginx/html
   EXPOSE 80
   CMD ["nginx", "-g", "daemon off;"]
   ```
   *Note: This keeps the final image extremely small because it doesn't include Node.js or `node_modules`.*

## Real Production Usage
In production, Dockerfiles are the source of truth for your application's environment.
- They are stored in Git along with the source code.
- CI/CD pipelines use them to automatically build new images whenever code is pushed.
- We use **Caching** to make builds faster. Docker caches steps that haven't changed.

## Common Mistakes
- **Incorrect COPY order**: Copying all files *before* running `npm install` breaks the build cache every time a file changes, making builds slow.
- **Using heavy base images**: Using `FROM node:latest` results in a ~1GB image. `FROM node:alpine` results in ~100MB.
- **Hardcoding secrets**: Putting passwords or API keys in the Dockerfile.

## Debugging Guide
- **Build fails**: Look at the step where it failed. Usually, it's a typo in a command or a missing dependency.
- **To debug a failing build step**: You can run an interactive container of the *previous successful step* to see what's wrong.
  ```bash
  docker run -it <id_of_last_successful_layer> sh
  ```

## Best Practices
- **Leverage Build Cache**: Copy `package.json` first, run `npm install`, and THEN copy the rest of the code.
- **Use `.dockerignore`**: Exclude `node_modules`, `.git`, and build logs.
- **Minimize layers**: Combine `RUN` commands where appropriate (e.g., `RUN apt-get update && apt-get install -y ...`).

## Interview Questions
1. **What is the difference between `RUN` and `CMD` in a Dockerfile?**
   *Answer*: `RUN` executes commands *during the build process* and commits the results to the image. `CMD` specifies the default command to run *when the container starts*.
2. **How do you make your Docker builds faster?**
   *Answer*: By leveraging layer caching (copying dependencies first) and using a proper `.dockerignore` file.

## Summary
The Dockerfile is the automation script for creating images. By understanding its instructions and how caching works, you can create fast, efficient, and secure images for your applications.

---
Prev: [02_images_vs_containers.md](./02_images_vs_containers.md) | Index: [Index](../00_index.md) | Next: [04_volumes.md](./04_volumes.md)
