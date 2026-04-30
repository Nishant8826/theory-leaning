# 📌 Topic: Docker Security Best Practices

🟢 **Simple Explanation (Beginner)**
-----------------------------------
Imagine you are building a **Bank Vault**.
- You don't leave the front door open.
- You don't give the janitor the key to the main safe.
- You check everyone who comes in and out.

In Docker, "Security" is about making sure that if a hacker breaks into your app, they are trapped in a small, empty "box" (the container) and can't get out to control your whole computer.

🟡 **Practical Usage**
-----------------------------------
### 1. The "Root" Rule
By default, Docker runs your app as `root`. This is like giving your app a loaded gun.
**Best Practice**: Create a normal user.
```dockerfile
FROM node:18-alpine
# ... build app ...
USER node
CMD ["node", "app.js"]
```

### 2. The "Read-Only" Rule
If your app doesn't need to write files, lock the door!
```bash
docker run --read-only nginx
```
*Note: This might break some apps that expect to write to `/tmp`. Use a Tmpfs for those specific folders.*

### 3. Scanning for Holes
Docker has built-in tools to check if your images have known bugs.
```bash
docker scan my-image:latest
```

🔵 **Intermediate Understanding**
-----------------------------------
### Attack Surface
Every tool you install in your image (like `curl`, `git`, `vim`) is a tool a hacker can use. 
**The Goal**: Use **Minimal Base Images** (like `alpine` or `distroless`) that contain almost nothing but your app.

### Secrets Management
Never put passwords in your Dockerfile or Environment variables if you can avoid it. 
- **Bad**: `ENV DB_PASS=password123`
- **Good**: Use **Docker Secrets** (Swarm) or a **Secrets Volume** (Kubernetes) that mounts the password as a file.

🔴 **Internals (Advanced)**
-----------------------------------
### The Docker Socket Vulnerability
The file `/var/run/docker.sock` is the "Master Key."
- If a container has this file mounted, it can talk to the Docker Engine.
- It can then start a new container that has access to your **entire hard drive**.
- **Rule**: NEVER mount the Docker socket inside a container unless you are building a tool like Portainer or Jenkins and you fully trust it.

### Content Trust
How do you know the `nginx` image you pulled is actually from Nginx and not a hacker?
**Docker Content Trust (DCT)** uses digital signatures. If the signature doesn't match, Docker won't pull the image.
```bash
export DOCKER_CONTENT_TRUST=1
docker pull nginx
```

⚫ **Staff-Level Insights**
-----------------------------------
### Supply Chain Security (SBOM)
A Staff Engineer doesn't just care about their code; they care about the **300 libraries** their code uses.
**The Solution**: Generate a **Software Bill of Materials (SBOM)** for every image. This is a list of every package inside. If a new "Log4j" style bug is found, you can search your SBOMs and find which apps are at risk in seconds.
```bash
docker sbom my-image:latest
```

### Immutable Infrastructure
In production, you should disable `exec`. If you find yourself having to `exec` into a production container to fix something, your deployment process is broken. 

🏗️ **Mental Model**
Security is **Defense in Depth**. One layer (Namespaces) might fail, so you have another (Cgroups), and another (Read-only), and another (Non-root).

⚡ **Actual Behavior**
Docker uses **AppArmor** or **SELinux** (on Linux) to provide high-level security profiles that limit what a container can do even if it has root access.

🧠 **Resource Behavior**
- **Performance**: Security scanning takes time during the build. Security profiles (AppArmor) have near-zero impact on runtime performance.

💥 **Production Failures**
- **The "Privileged" Escape**: A developer runs a container with `--privileged`. The container can now see every hard drive and device on the host. A hacker breaks in and encrypts the host's hard drive (Ransomware).
- **Environment Leak**: A developer puts a Cloud API Key in an `ENV` variable. A hacker uses `docker inspect` to steal the key and spends $50,000 on the company's AWS account.

🏢 **Best Practices**
- Run as a **non-root user**.
- Use **official, verified images**.
- **Scan** images in your CI/CD pipeline.
- Keep the **Docker Host** (the server) patched and updated.

🧪 **Debugging**
```bash
# Check if you are currently root inside a container
docker exec <id> whoami

# Check if a container has too many privileges
docker inspect <id> --format '{{.HostConfig.Privileged}}'
```

💼 **Interview Q&A**
- **Q**: Is it safe to run a container as root?
- **A**: No, because if the container is compromised, the hacker has root access to the container and a better chance of escaping to the host.
- **Q**: What is a "Minimal Base Image"?
- **A**: An image that contains only the absolute minimum required to run the application, reducing the attack surface.

---
Prev: [../Internals/28_The_Copy_on_Write_CoW_Mechanism.md](../Internals/28_The_Copy_on_Write_CoW_Mechanism.md) | Index: [00_Index.md](../00_Index.md) | Next: [30_Rootless_Docker_Running_without_Sudo.md](30_Rootless_Docker_Running_without_Sudo.md)
---
