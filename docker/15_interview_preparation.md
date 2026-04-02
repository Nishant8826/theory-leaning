# Interview Preparation: Docker & DevOps

---

### What
Docker is an incredibly common topic in almost all modern Software Engineering and DevOps interviews. Understanding both the basic definitions and the complex systemic networking concepts is essential.

---

### 1. Fundamentals

**Q: Explain the difference between virtualization (VMs) and containerization (Docker).**
*Answer:* Virtual Machines rely on a hypervisor to virtualize completely isolated hardware and install a full, heavy Guest OS for every machine. Docker virtualizes the OS itself, allowing lightweight containers to share the host's OS kernel directly, drastically reducing startup times and memory usage.

**Q: What is the difference between a Docker Image and a Docker Container?**
*Answer:* A Docker Image is an immutable, read-only file consisting of stacked instructions/layers (OS, tools, code). A Container is a live, running instance of an Image that attaches a temporary read-write layer and a network interface.

**Q: What is a Docker Volume?**
*Answer:* Since the internal filesystem of a container is ephemeral (destroyed upon deletion), a Docker Volume is a persistent storage location safely managed on the physical host machine, allowing databases to retain their data across container restarts.

---

### 2. Scenario-Based Questions

**Scenario 1: You joined a team working on a huge React+Node app. Every time you change one line of code, Docker takes 4 minutes to rebuild the container. How do you fix this?**
*Answer:* I would restructure the `Dockerfile` to leverage layer caching. I would move `COPY package.json` and `RUN npm install` to the very top, before `COPY . .`. This way, Docker re-uses the massive `node_modules` cache unless the dependencies specifically change. Furthermore, I would utilize Bind Mounts (`-v "$(pwd):/app"`) in development so the local code syncs into the container instantly without needing a rebuild.

**Scenario 2: The frontend container (running React) cannot connect to the backend API container in Docker Compose.**
*Answer:* I would ensure they are both on the same custom Docker Network inside `docker-compose.yml`. I would also verify that the frontend is calling the correct DNS name. Wait! Because React executes in the *user's physical browser*, not inside the internal network, React must fetch from `localhost:[published_port]`, not the internal `http://backend:5000` DNS.

**Scenario 3: Your CI/CD pipeline pushes an image to production, but it is 1.5GB and causes downtime while downloading.**
*Answer:* I would implement a **Multi-Stage Build**. I would compile the application in `STAGE 1 (Builder)`, and then copy strictly the final production artifacts (`/dist` or `/build` folder) into a pristine, minimalist `node:alpine` or `nginx:alpine` image for `STAGE 2`. This easily drops the image size under 100MB by abandoning compilers and devDependencies.

---

### 3. Practical Knowledge Checks

**Q: What does the `-p 8080:80` flag mean exactly?**
*Answer:* It maps Port 8080 on the external Host Machine to Port 80 inside the internal Docker container.

**Q: Why use `user node` locally instead of running as `root` in a Dockerfile?**
*Answer:* The Principle of Least Privilege. Running Node.js as the root user means that if a hacker finds an arbitrary execution bug in a malicious npm package, they possess administrative access to the container sand-box.

**Q: What happens when you run `docker-compose down -v`?**
*Answer:* It forcefully stops and removes all containers, networks, and explicitly removes the attached Volumes, actively wiping any database persistence you may have generated.

---

### Conclusion
Docker is the cornerstone of modern cloud architecture. 
If you understand **Layer Caching**, **Volumes vs Bind Mounts**, and **Internal Compose Networking**, you will ace your interviews.

Good luck!

---
Prev : [14_debugging_and_best_practices.md](./14_debugging_and_best_practices.md) | Next : None (End of Guide)
