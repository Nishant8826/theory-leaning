# 📌 Topic: OCI Spec and runc (The Runtime)

## 🧠 Concept Explanation (Basic → Expert)
**Basic**: `runc` is the tiny program that actually starts the container. It's the "Engine" inside the engine. Docker doesn't start containers itself; it asks `containerd`, which then asks `runc` to do the heavy lifting.
**Expert**: `runc` is the reference implementation of the **OCI (Open Container Initiative) Runtime Specification**. It is a low-level CLI tool that takes an **OCI Bundle** (a folder with a `config.json` and a `rootfs`) and uses kernel features like `clone()`, `pivot_root()`, and `setns()` to create the container. Staff-level engineering requires understanding that the "Container" is not a single thing, but a series of kernel configurations standardized by the OCI so that any runtime (like `runc`, `kata-containers`, or `gVisor`) can run the same image.

## 🏗️ Mental Model
- **Docker**: The architect. He has the big blueprints and manages the whole site.
- **containerd**: The construction manager. He organizes the workers and the materials.
- **runc**: The individual worker with a hammer. He actually puts up the walls (namespaces) and installs the locks (cgroups). He does one job and then stays out of the way.

## ⚡ Actual Behavior
- **Portability**: Because `runc` follows the OCI spec, you can replace it with a different runtime like **Kata Containers** (which uses a tiny VM for better security) without changing your Dockerfile or your image.
- **Lifecycle**: `runc` is a "Short-lived" process. It starts the container, hands over the process to `containerd-shim`, and then exits. This is why Docker can restart without killing your containers.

## 🔬 Internal Mechanics (The Startup Steps)
1. **The Bundle**: `containerd` extracts the image into a folder and generates a `config.json`.
2. **The Create**: `runc create` creates the namespaces and cgroups but doesn't start the app yet.
3. **The Pivot**: `runc` calls `pivot_root` to change the container's `/` to the image's root folder.
4. **The Start**: `runc start` finally executes the `ENTRYPOINT` command.
5. **The Handover**: `runc` exits. The app process is now monitored by `containerd-shim`.

## 🔁 Execution Flow
1. `docker run ...`
2. Docker Daemon -> `containerd` (via gRPC).
3. `containerd` -> creates OCI bundle on disk.
4. `containerd` -> spawns `runc`.
5. `runc` -> sets up namespaces/cgroups.
6. `runc` -> starts the app process.
7. `runc` -> exits.
8. App process is now a child of the `containerd-shim`.

## 🧠 Resource Behavior
- **Memory**: `runc` uses very little memory (~10MB) because it only exists for a few seconds.
- **Dependencies**: `runc` depends on the host Linux kernel. It cannot run on Windows or Mac without a Linux VM.

## 📐 ASCII Diagrams (REQUIRED)

```text
       CONTAINER RUNTIME STACK
       
[  Docker CLI  ]
       |
[ Docker Daemon ] <--( REST API )
       |
[  containerd  ]  <--( gRPC )
       |
[ containerd-shim ] --( Spawns )--> [  runc  ]
       |                               |
       |                        ( Creates NS/CG )
       |                               |
       +------( Manages PID 1 )--------+
```

## 🔍 Code (Running a container with ONLY runc)
```bash
# 1. Create an OCI bundle
mkdir -p my-container/rootfs
docker export $(docker create alpine) | tar -C my-container/rootfs -xvf -

# 2. Generate the config
cd my-container
runc spec

# 3. Edit config.json if needed (e.g., change the command)

# 4. Run the container directly with runc (bypass Docker entirely)
sudo runc run my-container-id
```

## 💥 Production Failures
- **The "Shim Leak"**: In older versions, if the `containerd-shim` crashed, the container process would become an orphan. The container would keep running, but Docker would lose control of it (can't stop it, can't see logs).
- **Incompatible Runtimes**: You try to use a "Rootless" runtime on an old kernel that doesn't support User Namespaces. `runc` fails with an obscure "Permission Denied" error during the `clone()` syscall.

## 🧪 Real-time Q&A
**Q: Why is the OCI spec important?**
**A**: Before OCI, every tool (Docker, CoreOS Rocket, etc.) had its own image format and runtime. This split the community. OCI created a **Universal Standard**. Now, you can build an image with Docker and run it on Kubernetes (CRI-O), AWS Lambda, or even a specialized high-security runtime like gVisor.

## ⚠️ Edge Cases
- **Alternative Runtimes**: 
  - **gVisor (runsc)**: Intercepts syscalls for extra security.
  - **Kata (kata-runtime)**: Runs containers in a 100ms-boot VM.
  - **Firecracker**: Micro-VMs used by AWS Fargate.

## 🏢 Best Practices
- **Stay Updated**: `runc` is where most "Container Escape" vulnerabilities (like CVE-2019-5736) are found. Keeping your Docker engine updated is mostly about getting the latest `runc` security patches.
- **Use Shims**: Don't try to manage `runc` processes yourself; let `containerd` handle the complexity of process monitoring and log redirection.

## ⚖️ Trade-offs
| Runtime | Security | Speed | Overheads |
| :--- | :--- | :--- | :--- |
| **runc (Native)** | Medium | **Fastest** | **Zero** |
| **gVisor (Sandboxed)**| **High** | Medium | Medium |
| **Kata (VM)** | **Highest** | Slowest | High |

## 💼 Interview Q&A
**Q: What is the role of 'containerd' vs 'runc' in the Docker ecosystem?**
**A**: **containerd** is a high-level "Supervisor." It manages the lifecycle of images, volumes, and networks, and provides a gRPC API for the Docker daemon. **runc** is a low-level "Executor." It is a standalone tool that implements the OCI runtime spec to actually create and start the container using Linux kernel primitives. containerd calls runc to start a container and then monitors the process until it exits. This separation allows Docker to be more modular and allows for the use of alternative runtimes.

## 🧩 Practice Problems
1. Follow the "Code" section above to run a container using only the `runc` binary.
2. Use `ps auxf` on your host to see the process tree of a running Docker container. Note how the app is a child of a `shim`.
3. Research the "RunC Exploit" (CVE-2019-5736) and how it allowed a container to overwrite the host's `runc` binary.

---
Prev: [03_OverlayFS_and_Storage_Drivers.md](./03_OverlayFS_and_Storage_Drivers.md) | Index: [00_Index.md](../00_Index.md) | Next: [05_Linux_Capabilities_Matrix.md](./05_Linux_Capabilities_Matrix.md)
---
