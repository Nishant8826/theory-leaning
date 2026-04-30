# 📌 Topic: Namespaces and cgroups (The Kernel Primitives)

## 🧠 Concept Explanation (Basic → Expert)
**Basic**: Namespaces are like putting a pair of virtual reality goggles on a process. It thinks it has its own private network, its own users, and its own process list. Cgroups are like a budget. They tell the process exactly how much CPU and RAM it is allowed to spend.
**Expert**: Docker is not a "technology"—it's a collection of Linux Kernel primitives. **Namespaces** provide **Isolation** (what a process can see), while **Control Groups (cgroups)** provide **Resource Accounting & Limits** (what a process can use). Together, they create the illusion of a standalone OS within a shared kernel environment.

## 🏗️ Mental Model
- **Namespaces (Isolation)**: A person in a room with opaque windows. They can see what's inside their room, but they have no idea there are other rooms in the same building.
- **Cgroups (Constraint)**: A person in a room with a limited air supply and a metered electricity bill. If they use too much, the power is cut off.

## ⚡ Actual Behavior
- **Namespace**: If you run `ps aux` inside a container, you only see PID 1 (your app). On the host, that same process might be PID 4592.
- **Cgroup**: If a container is limited to 512MB and it tries to allocate 513MB, the Kernel's OOM (Out Of Memory) Killer will instantly terminate it to protect the rest of the system.

## 🔬 Internal Mechanics (The Kernel Magic)
1. **Namespaces**:
   - `PID`: Isolates process IDs.
   - `NET`: Isolates network stacks (interfaces, IP addresses, routing tables).
   - `MNT`: Isolates mount points (each container has its own root `/`).
   - `UTS`: Isolates hostnames and domain names.
   - `IPC`: Isolates Inter-Process Communication (shared memory).
   - `USER`: Isolates User and Group IDs (allows root inside container to be non-root on host).
2. **Cgroups**:
   - `Memory`: Tracks and limits RAM usage.
   - `CPU`: Tracks and limits CPU shares and quotas.
   - `Blkio`: Limits Disk I/O.
   - `Devices`: Controls which hardware devices (GPU, USB) a container can access.

## 🔁 Execution Flow
1. `docker run --cpus 2 --memory 1g`
2. `runc` creates a new set of namespaces for the process.
3. `runc` creates a directory in `/sys/fs/cgroup/memory/docker/<id>` and writes `1073741824` into `memory.limit_in_bytes`.
4. The Kernel enforces these limits during execution.

## 🧠 Resource Behavior
- **CPU Throttling**: When a container exceeds its CPU quota, the kernel doesn't kill it; it just "throttles" its execution (CFS Quota), causing latency to increase.
- **Memory OOM**: When a container exceeds its memory limit, it is killed immediately.

## 📐 ASCII Diagrams (REQUIRED)

```text
       LINUX KERNEL ISOLATION
       
[ Container A ]      [ Container B ]      [ Host OS ]
      |                    |                    |
      v                    v                    v
+-------------------------------------------------------+
|                 LINUX KERNEL                          |
|  +----------------+  +----------------+  +---------+  |
|  | PID Namespace  |  | PID Namespace  |  | Root    |  |
|  | NET Namespace  |  | NET Namespace  |  | PID     |  |
|  | MNT Namespace  |  | MNT Namespace  |  | NS      |  |
|  +----------------+  +----------------+  +---------+  |
|                                                       |
|  +-------------------------------------------------+  |
|  |                 CGROUPS                         |  |
|  |  (Limit A: 1GB) | (Limit B: 2GB) | (Host: Free) |  |
|  +-------------------------------------------------+  |
+-------------------------------------------------------+
```

## 🔍 Code (Kernel Inspection)
```bash
# See cgroup memory limits for a running container
ID=$(docker ps -q --no-trunc | head -n 1)
cat /sys/fs/cgroup/memory/docker/$ID/memory.limit_in_bytes

# Verify Namespace isolation
# Inside container:
hostname # returns container ID
# Outside container:
hostname # returns host name
```

## 💥 Production Failures
- **The "Noisy Neighbor" (Cgroup v1 issue)**: In older kernels, some resources weren't perfectly isolated in cgroups (like page cache), leading to one container slowing down another.
- **PID Exhaustion**: If a container is allowed to fork unlimited processes, it can exhaust the host's PID limit (`/proc/sys/kernel/pid_max`), preventing the host from spawning new processes.
  *Fix*: Use `--pids-limit`.

## 🧪 Real-time Q&A
**Q: Can a process "break out" of a namespace?**
**A**: Theoretically, yes, if there's a kernel bug (vulnerability). This is why "Kernel Security" is synonymous with "Container Security." If an attacker can find a bug in the kernel's `MNT` namespace handling, they could potentially see the host's filesystem.

## ⚠️ Edge Cases
- **The `/proc` problem**: Some tools (like `top` or `free`) inside a container read from `/proc`, which is often NOT namespaced. This is why `free` inside a 512MB container might show 64GB (the total host RAM). 
  *Fix*: Use `lxcfs` or modern container-aware tools.

## 🏢 Best Practices
- **Always set memory limits**: Never run a container without `--memory`.
- **Use cgroup v2**: It provides much better resource isolation and management than v1.

## ⚖️ Trade-offs
| Feature | Benefit | Cost |
| :--- | :--- | :--- |
| **Namespaces**| Clean isolation | Minor syscall overhead |
| **Cgroups** | Performance predictability | Complexity in tuning limits |

## 💼 Interview Q&A
**Q: How does Docker limit memory usage?**
**A**: Docker uses the Linux Kernel's **Control Groups (cgroups)** subsystem. When you set a limit (e.g., `--memory 1g`), Docker writes this value to the cgroup filesystem (`/sys/fs/cgroup/memory/...`). The kernel then monitors every page allocation for the processes in that group. If the group tries to allocate more than its limit and cannot reclaim memory through swapping/cleaning, the kernel triggers the OOM Killer to stop the process.

## 🧩 Practice Problems
1. Create a container with a 10MB memory limit (`--memory 10m`). Use a tool like `stress` inside the container to exceed it and watch it get killed.
2. Inspect `/proc/self/ns` from both the host and a container and compare the inode numbers.

---
Prev: [02_Docker_Architecture.md](./02_Docker_Architecture.md) | Index: [00_Index.md](../00_Index.md) | Next: [04_Union_Filesystem.md](./04_Union_Filesystem.md)
---
