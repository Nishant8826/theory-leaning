# 📌 Topic: Resource Limits (CPU and Memory)

🟢 **Simple Explanation (Beginner)**
-----------------------------------
Imagine you are at a **Buffet**. 
- Without limits, one person could eat all the shrimp, leaving none for others.
- To prevent this, the waiter tells you: "You can only have **1 plate** of shrimp."

In Docker, if you run a "greedy" app, it might try to use all the RAM on your computer, causing your computer to freeze. Resource limits are "plates" that limit how much CPU and RAM a container can eat.

🟡 **Practical Usage**
-----------------------------------
### 1. Limiting Memory
```powershell
# Limit to 512 Megabytes
docker run -d --memory="512m" nginx
```

### 2. Limiting CPU
```powershell
# Limit to 0.5 CPU cores (50% of one core)
docker run -d --cpus="0.5" nginx
```

### 3. Monitoring Usage
```powershell
# See live usage of all containers
docker stats
```

🔵 **Intermediate Understanding**
-----------------------------------
### Hard Limits vs. Soft Limits
- **Hard Limit (`--memory`)**: If the container tries to use more than this, the kernel will kill it immediately (OOM).
- **Soft Limit (`--memory-reservation`)**: Docker allows the container to use more memory if the host has plenty, but forces it back down when the host is low on RAM.

### CPU Shares
CPU is handled differently than memory. CPU is "compressed." If a container is limited to 0.5 cores, it just runs slower. It doesn't crash.

🔴 **Internals (Advanced)**
-----------------------------------
### Control Groups (cgroups)
This is the Linux Kernel feature that makes limits possible.
- **cgroup v1**: The older version (separate hierarchies for memory, cpu).
- **cgroup v2**: The modern version (unified hierarchy).
When you set `--memory`, Docker writes that value into a file in the `/sys/fs/cgroup/` directory. The kernel reads that file to enforce the limit.

### The OOM Killer (Out of Memory)
If a container hits its hard memory limit, the Linux Kernel's **OOM Killer** is triggered.
1. It looks for the process using too much memory.
2. It sends a `SIGKILL`.
3. Docker detects this and sets the exit code to `137`.

⚫ **Staff-Level Insights**
-----------------------------------
### Java and Node.js Memory Issues
Old versions of Java and Node.js didn't "know" they were in a container. They would look at the **Host's RAM** (e.g., 64GB) instead of the **Container Limit** (e.g., 1GB) and try to allocate a massive heap, causing an instant crash.
**Staff Fix**: 
- For Java: Use `-XX:+UseContainerSupport`.
- For Node.js: Use `--max-old-space-size`.

### CPU Throttling
If you set `--cpus="0.5"`, the kernel uses "Quotas" and "Periods." It lets your app run for 50ms every 100ms. This can cause **Latency Spikes** in your API response times. 
**Staff Strategy**: Sometimes it's better to give more CPU but limit the number of threads.

🏗️ **Mental Model**
Resource limits are **Fences**. They keep the "animals" (containers) from eating each other's grass.

⚡ **Actual Behavior**
Memory is a **Hard Wall**. CPU is a **Governor**.

🧠 **Resource Behavior**
- **Memory Swap**: By default, if a container runs out of RAM, it might try to use the "Swap" (Hard Drive). This is extremely slow. Use `--memory-swap` to control this.

💥 **Production Failures**
- **The "Silent Crash" (Exit 137)**: Your app just disappears. You check `docker ps -a` and see `Exited (137)`. This is almost always an OOM issue.
- **CPU Starvation**: A non-limited container on your server starts an infinite loop, making your SSH connection and other containers unresponsive.

🏢 **Best Practices**
- **Always set limits** in production. Never leave them unlimited.
- Set memory limits slightly higher than your app's normal usage to account for occasional spikes.
- Use `docker stats` to benchmark your app's baseline usage before setting limits.

🧪 **Debugging**
```bash
# Check if your kernel supports cgroups v2
docker info | grep "Cgroup Version"

# Inspect the cgroup file directly (Linux)
cat /sys/fs/cgroup/memory/docker/<id>/memory.limit_in_bytes
```

💼 **Interview Q&A**
- **Q**: What happens when a container exceeds its memory limit?
- **A**: It is killed by the OOM Killer (Exit code 137).
- **Q**: What is the difference between `--cpus` and `--cpu-shares`?
- **A**: `--cpus` is a hard limit on total usage. `--cpu-shares` is a relative weight used only when the CPU is busy (contention).

---
Prev: [13_Exec_Logs_and_Inspecting_State.md](13_Exec_Logs_and_Inspecting_State.md) | Index: [00_Index.md](../00_Index.md) | Next: [../Networking/15_Docker_Network_Drivers_Bridge_Host_None.md](../Networking/15_Docker_Network_Drivers_Bridge_Host_None.md)
---
