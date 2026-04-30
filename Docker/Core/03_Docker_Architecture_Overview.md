# 📌 Topic: Docker Architecture Overview

🟢 **Simple Explanation (Beginner)**
-----------------------------------
Docker isn't just one single program; it's a team working together.

Imagine a **Restaurant**:
1. **The Customer (Docker Client)**: You are the customer. You shout orders like "Make me a sandwich!" (`docker run`).
2. **The Waiter (Docker Daemon)**: The waiter takes your order and passes it to the kitchen. He manages the tables and the bill.
3. **The Chef (containerd)**: The chef knows *how* to cook. He manages the ingredients and the timing.
4. **The Stove (runc)**: The stove is the actual tool that applies heat to the food.

In Docker:
- You type commands in the **CLI**.
- The **Docker Daemon (`dockerd`)** manages images and networks.
- **containerd** manages the container lifecycle (start/stop).
- **runc** creates the container using Linux kernel features.

🟡 **Practical Usage**
-----------------------------------
When you install Docker Desktop, all these components are installed for you. You usually only interact with the Client.

**Check the components:**
```powershell
# See everything at once
docker info
```

**Common Architectures:**
- **Local Development**: Client and Daemon are on the same machine.
- **Remote Docker**: You can point your Client (on your laptop) to a Daemon running on a powerful AWS server.
  ```powershell
  # Example of connecting to a remote host
  docker -H ssh://user@remote-server ps
  ```

🔵 **Intermediate Understanding**
-----------------------------------
### The Components
1. **Docker CLI**: A thin wrapper that talks to the Daemon via a Unix Socket or TCP port (REST API).
2. **Docker Engine (dockerd)**: The core. It handles high-level logic:
   - Image building (`docker build`)
   - Network management
   - Volume management
   - Orchestration (Swarm)
3. **containerd**: A graduated CNCF project. It was once part of Docker but is now independent. It handles:
   - Image pushing/pulling
   - Managing container execution
4. **runc**: The "low-level" runtime. It follows the **OCI (Open Container Initiative)** spec. It interacts with the kernel.

### The "Shim"
When a container starts, a process called `containerd-shim` is created. 
**Why?** So that if the Docker Daemon or containerd restarts, your containers don't die! The shim keeps them alive.

🔴 **Internals (Advanced)**
-----------------------------------
### The Flow of a Request
```text
1. [CLI] "docker run" -> sends JSON via REST API to /var/run/docker.sock
2. [dockerd] authenticates, checks local images, pulls if needed.
3. [dockerd] calls [containerd] via gRPC.
4. [containerd] creates a "Bundle" (configs + rootfs).
5. [containerd] starts [containerd-shim].
6. [shim] calls [runc] to create the container.
7. [runc] sets up Namespaces/Cgroups and starts the app.
8. [runc] exits (it is a transient process).
9. [shim] stays alive to collect exit codes and handle logs.
```

### OCI (Open Container Initiative)
To prevent "Vendor Lock-in," the industry agreed on standards:
- **Image Spec**: How an image file should look.
- **Runtime Spec**: How to run a container (`runc` is the reference implementation).

⚫ **Staff-Level Insights**
-----------------------------------
### Decoupling and Reliability
By splitting Docker into `dockerd`, `containerd`, and `runc`, Docker achieved **High Availability**. You can upgrade your Docker Engine without killing your database container. This is called "Live Restore."

### Alternative Runtimes
You don't *have* to use `runc`. You can swap it for:
- **Kata Containers**: Uses a microVM for extra security.
- **gVisor**: A Google-built kernel sandbox.
- **Wasm**: To run WebAssembly modules in containers.

### Scaling the Daemon
At massive scale (thousands of containers), the Docker Daemon can become a "Single Point of Failure." Kubernetes actually bypasses `dockerd` and talks directly to `containerd` via the **CRI (Container Runtime Interface)**.

🏗️ **Mental Model**
Docker is a **Management Layer** on top of low-level Linux tools.

⚡ **Actual Behavior**
Even if you delete the `docker` binary while a container is running, the container process continues to run (if supervised by the shim).

🧠 **Resource Behavior**
- **Memory**: The Docker Daemon itself consumes about 100-200MB of RAM. 
- **Socket**: By default, it uses `/var/run/docker.sock`. Anyone who has access to this file effectively has **root access** to your machine.

💥 **Production Failures**
- **Docker Socket Exhaustion**: Too many API calls crashing the daemon.
- **Shim Leaks**: Occasionally, shims don't exit correctly, leaving "defunct" processes.

🏢 **Best Practices**
- **Don't expose the Docker Socket to the internet**. If you must use TCP, use TLS/SSL certificates.
- **Use `containerd` directly** if you are building an orchestration platform (like K8s).

🧪 **Debugging**
```bash
# See the logs of the daemon itself (Linux)
journalctl -u docker -f

# Check the containerd logs
journalctl -u containerd -f

# See the shim processes
ps aux | grep containerd-shim
```

💼 **Interview Q&A**
- **Q**: What is the difference between Docker Engine and containerd?
- **A**: Engine is the full user experience (CLI, API, Builds, Volumes). `containerd` is a subset focused purely on managing container execution and images.
- **Q**: What is OCI?
- **A**: The Open Container Initiative, which standardizes how containers should be built and run.

---
Prev: [02_Containers_vs_Virtual_Machines.md](02_Containers_vs_Virtual_Machines.md) | Index: [00_Index.md](../00_Index.md) | Next: [04_Installation_and_Setup_Windows_Linux_Mac.md](04_Installation_and_Setup_Windows_Linux_Mac.md)
---
