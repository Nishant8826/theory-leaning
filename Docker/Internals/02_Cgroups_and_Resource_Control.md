# 📌 Topic: Cgroups and Resource Control (V1 vs V2)

## 🧠 Concept Explanation (Basic → Expert)
**Basic**: Cgroups (Control Groups) are the "Brakes" of a Docker container. They make sure one container doesn't eat all the CPU or RAM on your computer, leaving nothing for the others.
**Expert**: Cgroups are a **Linux Kernel Resource Management** system. They handle **Metering**, **Limiting**, and **Prioritizing** resources (CPU, Memory, Disk I/O, Network). Staff-level engineering requires understanding the transition from **Cgroups V1** (Multiple hierarchies, complex to manage) to **Cgroups V2** (Unified hierarchy, better controller coordination). Cgroups V2 is essential for modern features like **Rootless Docker** and improved **OOM (Out Of Memory)** handling.

## 🏗️ Mental Model
- **Namespaces**: The walls of your apartment (Isolation).
- **Cgroups**: The utility meters and breakers for your apartment. If you use too much electricity (CPU) or water (RAM), the breaker trips (OOM Kill) or your flow is restricted (Throttling).

## ⚡ Actual Behavior
- **Throttling (CPU)**: If you set a limit of 0.5 CPU, the kernel will physically stop your process from running once it uses its "Quota" for a given time period. The app feels "Slow" but doesn't crash.
- **OOM Killing (RAM)**: RAM cannot be "Throttled" (you can't give an app half a byte). If an app exceeds its RAM limit, the kernel has no choice but to kill it instantly.

## 🔬 Internal Mechanics (The Controllers)
1. **CPU Controller**: Uses **CFS (Completely Fair Scheduler)**. It defines a `period` (usually 100ms) and a `quota` (how much of that 100ms the container can use).
2. **Memory Controller**: Tracks pages of memory used. Includes **RSS** (Real RAM) and **Cache**.
3. **PIDs Controller**: Limits the total number of processes/threads. Prevents "Fork Bombs."
4. **IO Controller**: Limits Disk Read/Write speed (IOPS/bps).

## 🔁 Execution Flow (The OOM Kill)
1. App allocates a large array.
2. Kernel Memory Controller: "Total used: 512MB. Limit: 512MB."
3. App requests 1 more byte.
4. Memory Controller: "Limit Exceeded!"
5. Kernel: Calls the **OOM Killer** function.
6. OOM Killer: Finds the process with the highest "OOM Score" (usually the container process).
7. Kernel: Sends `SIGKILL` to the process.
8. Docker: Logs "OOM Killed" and restarts the container if configured.

## 🧠 Resource Behavior
- **Soft Limits (`--memory-reservation`)**: Allows a container to use more RAM if the host has plenty, but forces it back down to the limit if the host gets crowded.
- **Hard Limits (`--memory`)**: A strict ceiling. Never exceeded.

## 📐 ASCII Diagrams (REQUIRED)

```text
       CGROUPS V1 vs V2
       
      [ CGROUPS V1 ]                [ CGROUPS V2 ]
    +----------------+            +-------------------+
    | /sys/fs/cgroup |            |  /sys/fs/cgroup   |
    |  /cpu          |            |  /my-container    |
    |  /memory       |            |    /cpu.max       |
    |  /pids         |            |    /memory.max    |
    +----------------+            +-------------------+
    (Separate Trees)              (Unified Hierarchy)
```

## 🔍 Code (Checking Cgroup Version)
```bash
# 1. Check if your host is using Cgroups V2
stat -fc %T /sys/fs/cgroup
# Output: 'cgroup2fs' means V2. 'tmpfs' usually means V1.

# 2. View limits for a running container
docker run -d --name limit-test --cpu-shares 512 --memory 128m alpine sleep 1000
CDIR=$(docker inspect -f '{{.Id}}' limit-test)

# V2 Path:
cat /sys/fs/cgroup/system.slice/docker-$CDIR.scope/memory.max
```

## 💥 Production Failures
- **The "Java/Node RAM Ignorance"**: Older versions of Java/Node didn't know they were in a container. They saw 64GB of RAM on the host and tried to allocate a 32GB heap, even though the Docker limit was 1GB. The container crashed instantly.
  *Fix*: Use modern versions of runtimes that are "Cgroup Aware" (`-XX:+UseContainerSupport`).
- **CPU Throttling Latency**: You set a 0.1 CPU limit. Your app needs to do 50ms of work. The kernel gives it 10ms, then stops it for 90ms, then gives it 10ms. A 50ms task now takes 500ms.
  *Fix*: Set "Requests" (guaranteed) but allow "Bursting" to higher limits.

## 🧪 Real-time Q&A
**Q: Why move to Cgroups V2?**
**A**: V2 provides a much cleaner API and fixes a major bug in V1 where a container could use 100% of the disk I/O and starve the rest of the system. V2 also allows **Rootless Docker** to manage resources safely, which was nearly impossible in V1.

## ⚠️ Edge Cases
- **Swap**: By default, Docker might allow containers to use "Swap" (slow disk RAM). If you want strict performance, you must disable swap or set `--memory-swap` to match `--memory`.

## 🏢 Best Practices
- **Always set PIDs limits**: `--pids-limit 100` prevents an attacker from crashing your whole server with a simple script.
- **Monitor Throttling**: Use `container_cpu_cfs_throttled_seconds_total` in Prometheus to see if your CPU limits are too tight.
- **Prefer V2**: If you are setting up a new server, use a modern OS (Ubuntu 22.04+, RHEL 9+) that defaults to Cgroups V2.

## ⚖️ Trade-offs
| Limit Type | App Impact | Host Impact |
| :--- | :--- | :--- |
| **No Limits** | Fast | **Dangerous (Crashes Host)**|
| **Hard Limits** | **Risk of OOM** | Safe |
| **Soft Limits** | Flexible | Medium Risk |

## 💼 Interview Q&A
**Q: What is the difference between CPU 'Shares' and CPU 'Limits' in Docker?**
**A**: **CPU Shares** (`--cpu-shares`) is a weighted, relative value. If the host is idle, a container with shares can use 100% of the CPU. It only restricts the container when the host is under contention. **CPU Limits** (`--cpus`) is an absolute "Hard" limit. If you set a limit of 0.5, the container will never use more than 50% of a single core, even if the rest of the server is completely idle. Use Shares for flexible workloads and Limits for consistent, predictable performance.

## 🧩 Practice Problems
1. Run a container with `--memory 50m`. Try to run a command that uses 100MB of RAM and watch the OOM Kill in `docker inspect`.
2. Compare the `/sys/fs/cgroup` directory on a V1 host vs a V2 host.
3. Use `docker stats` to watch the "CPU %" of a container as you change its `--cpus` limit.

---
Prev: [01_Namespaces_Deep_Dive.md](./01_Namespaces_Deep_Dive.md) | Index: [00_Index.md](../00_Index.md) | Next: [03_OverlayFS_and_Storage_Drivers.md](./03_OverlayFS_and_Storage_Drivers.md)
---
