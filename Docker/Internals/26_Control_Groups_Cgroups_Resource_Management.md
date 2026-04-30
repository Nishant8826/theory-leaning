# 📌 Topic: Control Groups (Cgroups): Resource Management

🟢 **Simple Explanation (Beginner)**
-----------------------------------
While **Namespaces** decide what a container can **SEE**, **Cgroups** decide what a container can **USE**.

Imagine a **Kindergarten Class**.
- **Namespaces**: The kids are in different rooms so they can't see each other (Isolation).
- **Cgroups**: Each room only gets 2 boxes of crayons and 1 gallon of juice. No matter how much they scream, they can't have more (Resource Limits).

If one container (kid) starts using too much memory (juice), Cgroups step in and say "No more!" and might even kick the container out (OOM Kill).

🟡 **Practical Usage**
-----------------------------------
You set these limits when you run the container.
```powershell
# Limit to 10% CPU and 100MB RAM
docker run -d --cpus=".1" --memory="100m" nginx
```

### Checking the limits
On a Linux host, you can find the actual files that control these limits:
```bash
# Go to the memory cgroup for docker
cd /sys/fs/cgroup/memory/docker/<container_id>
cat memory.limit_in_bytes
```
If you change the number in this file, the container's limit changes **instantly** without a restart!

🔵 **Intermediate Understanding**
-----------------------------------
### Cgroup v1 vs. Cgroup v2
- **v1 (Older)**: Resources are separate. You have a folder for Memory, a folder for CPU, a folder for Disk I/O.
- **v2 (Modern)**: Everything is unified in one hierarchy. It is much more efficient and handles things like "IO pressure" better. 
- *Docker and Kubernetes have recently moved almost entirely to Cgroup v2.*

### What can Cgroups control?
1. **Memory**: RAM usage and Swap.
2. **CPU**: How many "shares" of the processor it gets.
3. **PIDs**: How many processes a container can start (prevents "Fork Bombs").
4. **Network**: Traffic priority.
5. **Block I/O**: Read/Write speed to the hard drive.

🔴 **Internals (Advanced)**
-----------------------------------
### The CFS Scheduler
For CPU limits, Cgroups use the **Completely Fair Scheduler (CFS)**.
- It defines a **Period** (usually 100ms).
- If you set `--cpus="0.5"`, Cgroups gives the container a **Quota** of 50ms.
- Once the container uses its 50ms, it is **Throttled** (suspended) until the next period starts.

### The Memory Controller
When a process requests memory (using `malloc`), the kernel checks the Cgroup counter. 
- If `counter + request > limit`, the kernel tries to reclaim memory from the cache.
- If it still can't find room, it triggers the **OOM Killer**.

### ASCII Diagram: Cgroup Hierarchy
```text
/sys/fs/cgroup/
├── cpu/
│   └── docker/
│       ├── container_A/ (cpu.shares=512)
│       └── container_B/ (cpu.shares=1024) <-- Gets 2x more CPU
├── memory/
│   └── docker/
│       ├── container_A/ (memory.limit=1G)
│       └── container_B/ (memory.limit=2G)
```

⚫ **Staff-Level Insights**
-----------------------------------
### Detecting Throttling
Sometimes your app is slow, but `docker stats` says CPU is only at 20%. 
**Staff Secret**: Check the **Throttling metrics**. Your app might be hitting its limit for a tiny fraction of a second and getting paused, even if the "average" usage looks low.
```bash
cat /sys/fs/cgroup/cpu/docker/<id>/cpu.stat
# Look for nr_throttled and throttled_time
```

### The "Fork Bomb" Defense
A malicious container can crash your whole server by running `while(true) fork();`. This fills the host's process table.
**Staff Protection**: Always set a **PID Limit** in production.
`docker run --pids-limit 100 ...`

🏗️ **Mental Model**
Cgroups are **Resource Meters and Fences**.

⚡ **Actual Behavior**
Cgroups are enforced at the **Kernel Level**. There is no way for a process to "bypass" them because the kernel itself handles the accounting.

🧠 **Resource Behavior**
- **Overhead**: Minimal. Accounting for memory/CPU usage adds about 1% overhead to the kernel.

💥 **Production Failures**
- **Disk I/O Starvation**: One container is doing a massive database backup, making the hard drive so busy that other containers can't read their logs.
  - **Fix**: Use `--device-read-bps` to limit I/O.
- **System-Wide OOM**: If you don't limit your containers, and the host runs out of RAM, the kernel might kill a **Critical System Process** (like SSH or Docker itself) instead of the greedy container.

🏢 **Best Practices**
- **Always set memory limits.**
- Use Cgroup v2 if possible (requires a modern Linux kernel like 5.8+).
- Set a **PID Limit** to prevent malicious code from crashing the host.

🧪 **Debugging**
```bash
# Check if your app is being throttled
docker inspect <id> --format '{{.State.Health}}' # If configured

# Direct kernel check
cat /sys/fs/cgroup/cpu,cpuacct/docker/<id>/cpuacct.usage
```

💼 **Interview Q&A**
- **Q**: What is the difference between Namespaces and Cgroups?
- **A**: Namespaces provide isolation (what you see); Cgroups provide resource limiting (what you use).
- **Q**: Can you change a container's memory limit while it is running?
- **A**: Yes, using the `docker update --memory ...` command, which modifies the cgroup files on the fly.

---
Prev: [25_Linux_Namespaces_The_Isolation_Engine.md](25_Linux_Namespaces_The_Isolation_Engine.md) | Index: [00_Index.md](../00_Index.md) | Next: [27_Docker_Engine_to_containerd_to_runc_Flow.md](27_Docker_Engine_to_containerd_to_runc_Flow.md)
---
