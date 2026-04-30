# 📌 Topic: Docker Architecture (Internal Workflow)

## 🧠 Concept Explanation (Basic → Expert)
**Basic**: Docker is like a client-server application. You (the client) give commands to a "Docker Engine" (the server), and it does the hard work of building images and running containers.
**Expert**: Docker follows a **Decoupled Architecture** based on the **OCI (Open Container Initiative)** standards. It consists of the **Docker CLI**, the **Docker Daemon (dockerd)**, **containerd**, **containerd-shim**, and **runc**. This transition from a monolithic daemon to a modular system allows for high stability (you can restart `dockerd` without killing running containers) and cross-platform compatibility.

## 🏗️ Mental Model
- **Docker CLI**: The remote control.
- **Docker Daemon (dockerd)**: The smart hub that translates commands into complex tasks.
- **containerd**: The warehouse manager who tracks all the boxes (containers) and inventory (images).
- **runc**: The actual worker who physically moves the box into its isolated space.

## ⚡ Actual Behavior
When you run `docker run alpine`:
1. The CLI sends a REST API request to `dockerd`.
2. `dockerd` calls `containerd` via gRPC.
3. `containerd` checks if the image exists; if not, it pulls it.
4. `containerd` creates a **bundle** and calls `runc`.
5. `runc` creates the container and then exits.
6. `containerd-shim` stays alive to monitor the container and prevent "zombie" processes.

## 🔬 Internal Mechanics (The Execution Chain)
1. **dockerd**: Handles high-level logic like image building (BuildKit), volume management, and networking.
2. **containerd**: An industry-standard container runtime. It manages the full container lifecycle: image transfer, execution, and storage.
3. **runc**: A lightweight, portable container runtime that implements the OCI specification. It is responsible for the actual kernel-level interaction (namespaces/cgroups).
4. **containerd-shim**: Acts as the parent of the container process. It allows `containerd` to exit or restart without affecting the container's stdin/stdout or its lifecycle.

## 🔁 Execution Flow (Step-by-Step)
1. `docker run` -> `dockerd` (API)
2. `dockerd` -> `containerd` (gRPC)
3. `containerd` -> `containerd-shim` (fork/exec)
4. `containerd-shim` -> `runc` (exec)
5. `runc` -> [Linux Kernel] (namespaces/cgroups)
6. `runc` exits; container PID 1 is now a child of `containerd-shim`.

## 🧠 Resource Behavior
- **Daemon Memory**: `dockerd` can consume significant RAM if managing thousands of containers or active builds.
- **Persistence**: Because of the shim, containers survive a `dockerd` crash or update (if "Live Restore" is enabled).

## 📐 ASCII Diagrams (REQUIRED)

```text
       DOCKER INTERNAL WORKFLOW
       
[ CLI ] --(REST)--> [ dockerd ]
                       |
                  (gRPC/HCS)
                       v
                [ containerd ] --(Pull)--> [ Image Store ]
                       |
                  (fork/exec)
                       v
              [ containerd-shim ]
                       |
                    (exec)
                       v
                    [ runc ] --(Exit)
                       |
                [ Linux Kernel ] <--- (Namespaces / Cgroups)
                       |
               [ CONTAINER PROCESS ]
```

## 🔍 Code (Inspecting the Chain)
```bash
# See the process hierarchy
ps auxf | grep -E "dockerd|containerd|shim"

# Check containerd status via its own CLI (ctr)
sudo ctr containers list

# Check runc directly
runc --version
```

## 💥 Production Failures
- **The "Zombie" Apocalypse**: If `containerd-shim` dies, the container's output has nowhere to go, and it might become an un-killable zombie process.
- **Daemon Hanging**: If `dockerd` is overwhelmed by API requests, it might stop responding. Running containers will keep running, but you won't be able to `stop` or `exec` into them until the daemon recovers.

## 🧪 Real-time Q&A
**Q: Why does Docker use containerd AND runc? Why not just one?**
**A**: Modularization. `containerd` handles "management" (image pulls, metadata). `runc` handles "execution" (talking to the kernel). This allows other tools (like Kubernetes/CRI-O) to use `runc` without needing the full Docker engine.

## ⚠️ Edge Cases
- **Windows Containers**: On Windows, Docker uses **HCS (Host Compute Service)** instead of `runc` to interface with the Windows kernel's Hyper-V isolation.

## 🏢 Best Practices
- **Enable Live Restore**: Set `"live-restore": true` in `/etc/docker/daemon.json` so containers keep running during Docker updates.
- **Limit API Exposure**: Never expose the Docker Unix Socket (`/var/run/docker.sock`) to untrusted containers; it's equivalent to giving them root on the host.

## ⚖️ Trade-offs
| Component | Responsibility | Lifespan |
| :--- | :--- | :--- |
| **dockerd** | Management / Build | Continuous |
| **containerd**| Lifecycle / Images | Continuous |
| **runc** | Execution | Transient (Exits) |
| **shim** | Monitoring | Per Container |

## 💼 Interview Q&A
**Q: What happens to your containers if the Docker Daemon (dockerd) is stopped?**
**A**: By default, they keep running as long as the host is up. The `containerd-shim` maintains the process. However, you won't be able to manage them via the CLI until the daemon is back. If "Live Restore" is NOT enabled, Docker might try to restart them when it comes back up, potentially causing a brief interruption.

## 🧩 Practice Problems
1. Locate `daemon.json` on your system. Enable `live-restore` and verify it by restarting the Docker service while a container is running.
2. Use `pstree -p` to visualize the relationship between `dockerd`, `containerd-shim`, and your application.

---
Prev: [01_Containerization_vs_VMs.md](./01_Containerization_vs_VMs.md) | Index: [00_Index.md](../00_Index.md) | Next: [03_Namespaces_and_cgroups.md](./03_Namespaces_and_cgroups.md)
---
