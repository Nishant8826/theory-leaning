# Writing Dockerfiles Step-by-Step

---

### What
A **Dockerfile** is a simple text file (`.txt` extension is usually omitted, it's just named `Dockerfile`). It contains a sequential list of instructions on exactly how Docker should build your custom Image. You can consider it the "recipe" for your application environment.

---

### Why
Without a Dockerfile, you would have to manually open a pristine Linux container, manually install Node.js, manually copy your code, and manually start your server, which defeats the point of automation. A Dockerfile automates this entire building process so you or anyone on your team can generate an identical image with one command.

---

### How
Dockerfiles read from top to bottom. Common instructions include:
- `FROM`: Starts the recipe by grabbing a base OS image (like Ubuntu or Alpine Linux).
- `WORKDIR`: Creates and moves into a folder inside the container.
- `COPY`: Copies files from your physical computer *into* the container.
- `RUN`: Executes terminal commands inside the container during the *build* phase (e.g., `npm install`).
- `CMD / ENTRYPOINT`: The command the container runs when it finally *turns on* (e.g., `node server.js`).

---

### Implementation

Let's write a standard Dockerfile for a Node.js Express backend. Note that order is incredibly important for layer caching!

```dockerfile
# File: Dockerfile

# 1. Base Image - Start with an incredibly lightweight Linux OS pre-installed with Node 18
FROM node:18-alpine

# 2. Set the Working Directory inside the container
WORKDIR /usr/src/app

# 3. Copy ONLY package.json first! (Crucial for layer caching)
COPY package*.json ./

# 4. Install dependencies
# (Docker caches the result of this step. It won't run again unless package.json changes)
RUN npm install

# 5. Copy the rest of your application code into the container
COPY . .

# 6. Expose the port your server listens on (informational)
EXPOSE 8080

# 7. Start the application! (This happens when the container starts, not when it builds)
CMD ["node", "index.js"]
```

---

### Steps
1. Place a file named exactly `Dockerfile` (no extension) in the root of your Node.js project.
2. Open your terminal in the same folder.
3. **Build the image**, giving it a tag/name:
   `docker build -t my-custom-backend .`
   *(The `.` tells Docker to look in the current folder for the Dockerfile).*
4. Once built, run it!:
   `docker run -p 8080:8080 my-custom-backend`

---

### Integration

* **React/Next.js/Node.js:** Regardless of the Javascript framework, the Dockerfile looks largely identical. You simply change the `CMD` to `npm start` or `npm run dev`.
* **Layer Caching:** Notice why we copy `package.json` separate from all other code (`COPY . .`) in Step 3? If we copied everything at once, any change to a single HTML file would invalidate the cache, forcing Docker to wait 3 minutes running `npm install` again. By isolating `package.json`, Docker uses the 0-second cache as long as you didn't add new packages!

---

### Impact
The `Dockerfile` is ultimate infrastructure-as-code documentation. Any new developer joining your company doesn't need a massive "Readme" file on how to download specific C++ logic tools or Python versions; they simply run `docker build` and the Dockerfile handles the complex setup sequentially.

---

### Interview Questions
1. **Explain the difference between `RUN` and `CMD` inside a Dockerfile.**
   *Answer: `RUN` executes a command during the Image build process (like installing packages). `CMD` specifies the default command that executes only when the Container actually starts (like turning on the web server).*
2. **Why do we copy `package.json` and run `npm install` before copying the rest of the application code?**
   *Answer: To leverage Docker's layer caching. Application code changes frequently, while dependencies change rarely. Isolating the dependency installation ensures Docker reuses the cached node_modules layer, drastically reducing build times.*
3. **What is `alpine` (e.g., node:18-alpine)?**
   *Answer: Alpine is a hyper-minimalist Linux distribution heavily favored in Docker. It reduces image sizes from roughly 1GB down to roughly 50MB, saving bandwidth and improving security.*

---

### Summary
* A Dockerfile acts as a sequential recipe for building your Image.
* Read from top to bottom, each instruction creates a new cached Layer.
* Order your commands from least-frequently-changed (`npm install`) to most-frequently-changed (`Source Code`).
* Build with `docker build`, then instantiate with `docker run`.

---
Prev : [05_working_with_docker_commands.md](./05_working_with_docker_commands.md) | Next : [07_docker_compose_basics.md](./07_docker_compose_basics.md)
