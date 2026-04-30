# 📌 Topic: Docker Engine to containerd to runc Flow

🟢 **Simple Explanation (Beginner)**
-----------------------------------
Imagine you want to **Launch a Rocket**.
1. **The President (Docker Engine)**: Gives the order "Launch!"
2. **Mission Control (containerd)**: Prepares the rocket, checks the fuel, and manages the countdown.
3. **The Launchpad (runc)**: The physical machinery that actually pushes the rocket into the sky.

In the early days, Docker did everything. Now, it is split into specialized tools so that each part can be improved without breaking the others.

🟡 **Practical Usage**
-----------------------------------
You can actually see these processes running on your Linux host.
```bash
ps -ef | grep -E "dockerd|containerd|shim|runc"
```

### Why does this split matter?
If the **Docker Daemon (`dockerd`)** crashes or needs an update, your containers keep running because **containerd** and the **shim** are still holding them up. This is called "Live Restore."

🔵 **Intermediate Understanding**
-----------------------------------
### The Components
1. **dockerd**: High-level features (Builds, API, Secrets, Networking).
2. **containerd**: Low-level lifecycle (Pulling images, starting/stopping containers). It is used by both Docker and Kubernetes.
3. **containerd-shim**: A "bodyguard" for each container. It handles the input/output and keeps the container alive if the main daemon restarts.
4. **runc**: The actual tool that talks to the Linux Kernel to create namespaces and cgroups.

🔴 **Internals (Advanced)**
-----------------------------------
### The Execution Chain
1. **Docker CLI** sends a REST request to `dockerd`.
2. **dockerd** converts this into a **gRPC** call to `containerd`.
3. **containerd** creates a "Container Bundle" (a folder with `config.json` and the root filesystem).
4. **containerd** calls `containerd-shim`.
5. **containerd-shim** calls `runc create`.
6. **runc** creates the namespaces, sets the cgroups, and runs the app.
7. **runc** exits immediately after the app starts.
8. **containerd-shim** stays alive to collect the app's logs and exit code.

### The OCI Standard
`runc` is an **OCI (Open Container Initiative)** compliant runtime. This means you could theoretically replace `runc` with something else (like `kata-runtime` for VMs) and `containerd` wouldn't even notice.

### ASCII Diagram: The Handover
```text
[ USER ] --(CLI)--> [ dockerd ]
                       |
                   (gRPC API)
                       |
                       v
                 [ containerd ]
                       |
               (Executes Shim)
                       |
                       v
              [ containerd-shim ] --(calls)--> [ runc ]
                       |                         |
               (Stays Alive) <-----------(Starts App & Exits)
                       |
                       v
                [ YOUR APP ]
```

⚫ **Staff-Level Insights**
-----------------------------------
### Kubernetes vs. Docker
Kubernetes used to talk to Docker, which talked to containerd, which talked to runc.
**Staff Change**: K8s now uses the **CRI (Container Runtime Interface)** to talk **directly to containerd**, skipping `dockerd` entirely. This reduces RAM usage and complexity.

### Debugging with `ctr` and `crictl`
If Docker is broken, you can still manage your containers using the low-level tools:
- `ctr`: The CLI for `containerd`.
- `crictl`: The CLI for Kubernetes runtimes.
- `runc list`: See containers from the kernel's perspective.

🏗️ **Mental Model**
It's a **Relay Race**. Each runner passes the baton to the next and then steps aside (or stays as a bodyguard).

⚡ **Actual Behavior**
The communication between `dockerd` and `containerd` happens over a Unix Socket (`/run/containerd/containerd.sock`).

🧠 **Resource Behavior**
- **Memory**: Each `containerd-shim` uses about 2-3MB of RAM. If you have 1000 containers, that's 2-3GB of RAM just for shims!

💥 **Production Failures**
- **Shim Leak**: Sometimes, if a container crashes violently, the `containerd-shim` doesn't exit. You'll see a process using 100% CPU that you can't kill easily.
- **Socket Permission Denied**: If the permissions on the `containerd.sock` are wrong, Docker will report "Cannot connect to the Docker daemon."

🏢 **Best Practices**
- Enable **"Live Restore"** in `/etc/docker/daemon.json` to keep containers running during Docker updates.
```json
{
  "live-restore": true
}
```

🧪 **Debugging**
```bash
# Check the status of containerd
systemctl status containerd

# Use the low-level tool to see images
sudo ctr -n moby images list
```

💼 **Interview Q&A**
- **Q**: Why does runc exit after starting the container?
- **A**: Because its only job is to set up the kernel environment (Namespaces/Cgroups) and "exec" the app. It doesn't need to stay running.
- **Q**: What is the purpose of the containerd-shim?
- **A**: It decouples the container from the Docker daemon, allowing the daemon to restart without stopping the containers.

---
Prev: [26_Control_Groups_Cgroups_Resource_Management.md](26_Control_Groups_Cgroups_Resource_Management.md) | Index: [00_Index.md](../00_Index.md) | Next: [28_The_Copy_on_Write_CoW_Mechanism.md](28_The_Copy_on_Write_CoW_Mechanism.md)
---
