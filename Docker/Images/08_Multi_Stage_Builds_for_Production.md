# 📌 Topic: Multi-Stage Builds for Production

🟢 **Simple Explanation (Beginner)**
-----------------------------------
Imagine you are building a wooden chair.
1. You go to a **Workshop** full of saws, drills, and sawdust.
2. Once the chair is finished, you move it to your **Living Room**.
3. You don't bring the saws, drills, and sawdust into the living room; you just bring the finished chair.

**Multi-Stage builds** do exactly this. 
- **Stage 1 (Build)**: Use a heavy image with all the compilers and tools (the Workshop).
- **Stage 2 (Final)**: Copy only the finished "app" to a tiny, clean image (the Living Room).

This keeps your production images small, fast, and secure.

🟡 **Practical Usage**
-----------------------------------
**Example: A React App**
Without multi-stage, you'd ship `npm`, `webpack`, and your source code. With multi-stage, you only ship the HTML/CSS/JS.

```dockerfile
# STAGE 1: Build Stage
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build # This creates the 'dist' folder

# STAGE 2: Production Stage
FROM nginx:alpine
# Copy ONLY the built files from the 'builder' stage
COPY --from=builder /app/dist /usr/share/nginx/html
# Nginx image is already set up to serve files
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

🔵 **Intermediate Understanding**
-----------------------------------
### The `AS` Keyword
The `AS <name>` allows you to name a stage. You can then use `--from=<name>` to pull files from it.

### Why does this matter?
- **Security**: Compilers and package managers (`npm`, `pip`, `gcc`) are tools that hackers can use if they break into your container. If they aren't there, the hacker is stuck.
- **Size**: A Go build image might be 800MB, but the resulting binary is only 15MB. Why ship 800MB?
- **Efficiency**: Only the final stage is saved as your image. All previous stages are discarded.

🔴 **Internals (Advanced)**
-----------------------------------
### BuildKit Parallelism
With the modern **BuildKit** engine, Docker doesn't run stages one-by-one linearly. If Stage A and Stage B don't depend on each other, BuildKit runs them **at the same time** (Parallel Building).

### File Ownership
When you `COPY --from`, the files are owned by `root` by default in the new stage. If your app needs to run as a non-root user, you must use:
`COPY --chown=node:node --from=builder /app/dist .`

⚫ **Staff-Level Insights**
-----------------------------------
### Shared Base Images
In large companies, Staff Engineers create a "Base Image" for the whole company that includes security patches, then developers use it in their multi-stage builds.

### Testing in Multi-Stage
You can add a "Test" stage that runs your unit tests. If the tests fail, the build stops, and the final image is never created.
```dockerfile
FROM builder AS tester
RUN npm test

FROM nginx:alpine
COPY --from=builder /app/dist ...
```

### Distroless Images
For maximum security, use Google's **Distroless** images as your final stage. They contain **zero** shell, zero package manager—only your app and its runtime (e.g., just the Python interpreter).

🏗️ **Mental Model**
Multi-stage is a **Pipeline**. Input -> Process -> Extract -> Final Output.

⚡ **Actual Behavior**
Docker creates temporary images for each stage. Only the final `FROM` instruction defines what ends up in your `docker images` list.

🧠 **Resource Behavior**
- **Build Cache**: Each stage has its own cache. If you change a file in the "Build" stage, the "Production" stage will still use its cache for the `COPY --from` step *unless* the specific files you are copying have changed.

💥 **Production Failures**
- **Missing Shared Libraries**: In languages like C++ or Python, you might copy the binary but forget the `.so` (Shared Object) files it needs to run. The container will start but immediately crash with "File not found."
- **Fix**: Use `ldd` to check dependencies before copying.

🏢 **Best Practices**
- Use **Alpine** or **Distroless** for the final stage.
- Name your stages clearly (`builder`, `tester`, `runner`).
- Always use `COPY --chown` if running as non-root.

🧪 **Debugging**
```bash
# Build only up to a specific stage (to debug tests, for example)
docker build --target builder -t debug-image .
```

💼 **Interview Q&A**
- **Q**: What are the two main benefits of multi-stage builds?
- **A**: 1. Smaller image size. 2. Improved security (less attack surface).
- **Q**: How do you copy files from one stage to another?
- **A**: Using the `COPY --from=<stage_name>` instruction.

---
Prev: [07_Layer_Caching_and_Optimization.md](07_Layer_Caching_and_Optimization.md) | Index: [00_Index.md](../00_Index.md) | Next: [09_BuildKit_The_Modern_Build_Engine.md](09_BuildKit_The_Modern_Build_Engine.md)
---
