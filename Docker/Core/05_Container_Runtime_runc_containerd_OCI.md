# 📌 Topic: Container Runtime (containerd, runc, OCI)

## 🧠 Concept Explanation (Basic → Expert)
**Basic**: The container runtime is the engine that actually starts and stops your containers. While "Docker" is the brand, `containerd` and `runc` are the actual mechanical parts that do the work under the hood.
**Expert**: Modern containerization is governed by the **OCI (Open Container Initiative)** standards. The runtime is split into two categories: **High-level Runtimes** (like `containerd` or `CRI-O`) which handle image management, API, and storage; and **Low-level Runtimes** (like `runc`) which are transient tools that interface with the Linux Kernel to create namespaces and cgroups. Staff-level engineers must understand the **CRI (Container Runtime Interface)** used by Kubernetes and how it differs from the Docker Engine's management of `containerd`.

## 🏗️ Mental Model
- **OCI Spec**: The blueprint for a container. It says "A container must have these namespaces and these limits."
- **runc (Low-level)**: The builder who follows the blueprint to create the room and then leaves.
- **containerd (High-level)**: The landlord who manages the building, keeps the blueprints, and makes sure the builder (runc) does their job.

## ⚡ Actual Behavior
- **Independence**: You can stop the `containerd` service, and your containers will keep running because they are managed by `containerd-shim`.
- **Interchangeability**: You can swap `runc` for a more secure runtime like `gVisor (runsc)` or a VM-based runtime like `Kata Containers` by simply changing a configuration line in Docker/containerd.

## 🔬 Internal Mechanics (The OCI Bundle)
When you start a container:
1. `containerd` creates an **OCI Bundle** on disk.
2. This bundle consists of a `rootfs` directory (the extracted image) and a `config.json` file.
3. `config.json` contains the kernel-level instructions: "Enable PID namespace," "Limit RAM to 1GB," "Run `/bin/sh`."
4. `runc` reads this JSON, performs the `clone()` syscall, and starts the process.

## 🔁 Execution Flow
1. `containerd` receives a "Create Container" request.
2. It fetches and unpacks the image into a bundle.
3. It spawns a `containerd-shim` process.
4. The `shim` calls `runc create`.
5. `runc` initializes the namespaces/cgroups.
6. `shim` calls `runc start`.
7. `runc` execs the app process and then terminates.
8. The `shim` remains as the "Sub-reaper" for the app process.

## 🧠 Resource Behavior
- **Memory Footprint**: `containerd` is extremely efficient (written in Go), consuming ~20-50MB of RAM. `runc` consumes almost zero persistent RAM as it is a transient process.
- **Shim Overhead**: Every container has a `containerd-shim` process on the host, consuming ~2-3MB of RAM. 1,000 containers = 3GB of RAM just for shims.

## 📐 ASCII Diagrams (REQUIRED)

```text
       RUNTIME HIERARCHY
       
+-----------------------------+
|    Docker Engine (API)      |
+-------------|---------------+
              | (gRPC)
+-------------v---------------+
|        containerd           | <--- High-level (Images/CRI)
+-------------|---------------+
              | (fork)
+-------------v---------------+
|     containerd-shim         | <--- Monitoring / IO
+-------------|---------------+
              | (exec)
+-------------v---------------+
|          runc               | <--- Low-level (Kernel Setup)
+-------------|---------------+
              v
       [ Linux Kernel ]
```

## 🔍 Code (Manual Container Creation)
```bash
# You can create a container WITHOUT Docker using just runc
mkdir my-container && cd my-container
mkdir rootfs
# Export an image into the rootfs
docker export $(docker create alpine) | tar -C rootfs -xvf -

# Generate a spec
runc spec
# Edit config.json if needed, then run:
sudo runc run my-container-id
```

## 💥 Production Failures
- **The "Shim Leak"**: In older versions, a bug could cause `containerd-shim` processes to hang even after a container was killed, leading to memory and PID exhaustion on the host.
- **Version Mismatch**: Using a version of `runc` that is too old for the Host Kernel's features (like cgroup v2 support) can cause containers to fail to start with cryptic "Operation not permitted" errors.

## 🧪 Real-time Q&A
**Q: If I use Kubernetes, do I need Docker?**
**A**: No. Modern Kubernetes uses `containerd` or `CRI-O` directly via the **CRI (Container Runtime Interface)**. Docker is just a suite of tools built on top of `containerd`.

## ⚠️ Edge Cases
- **Privileged Containers**: When a container is "privileged," `runc` skips many of the namespace isolations, giving the container almost full access to the host's hardware. This is a massive security risk.

## 🏢 Best Practices
- **Update Runtimes Frequently**: Security vulnerabilities (like `CVE-2019-5736`) are often found in `runc`. Keep your host OS patched.
- **Use Alternative Runtimes for Untrusted Code**: If running code from users, consider `gVisor` which provides a secondary kernel-level sandbox.

## ⚖️ Trade-offs
| Runtime | Isolation Level | Performance |
| :--- | :--- | :--- |
| **runc** | Standard (Kernel) | **Near-Native** |
| **gVisor** | High (User-space Kernel) | Low (Syscall overhead) |
| **Kata** | **Highest (Micro-VM)** | Medium (Boot latency) |

## 💼 Interview Q&A
**Q: What is the role of `containerd-shim`?**
**A**: The shim serves three critical purposes: 1. It allows the runtime (`containerd`) to be restarted or upgraded without killing the containers. 2. It keeps the stdin/stdout/stderr open for the container even if `containerd` is down. 3. It acts as the "Sub-reaper," meaning if the container's PID 1 process spawns children and then exits, the shim ensures those children are properly reaped, preventing zombie processes on the host.

## 🧩 Practice Problems
1. Use `runc list` to see containers that `containerd` is currently managing.
2. Read the `config.json` generated by `runc spec` and try to identify where the `memory` limits are defined.

---
Prev: [04_Union_Filesystem.md](./04_Union_Filesystem.md) | Index: [00_Index.md](../00_Index.md) | Next: [06_Image_Layers_and_Caching.md](./06_Image_Layers_and_Caching.md)
---
