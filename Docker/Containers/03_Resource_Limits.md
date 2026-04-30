# 📌 Topic: Resource Limits (CPU and Memory)

## 🧠 Concept Explanation (Basic → Expert)
**Basic**: Resource limits are like a speed governor on a car. They ensure that one container doesn't "hog" all the power of the server, leaving nothing for others.
**Expert**: Resource management in Docker is a implementation of **Kernel Control Groups (cgroups)**. It involves two strategies: **Hard Limits** (Enforcement) and **Soft Limits** (Prioritization). Staff-level engineering requires understanding the difference between **CPU Shares** (relative weight) and **CPU Quotas** (absolute time), and how the **OOM Killer** decides which container to execute when the host runs out of RAM.

## 🏗️ Mental Model
- **Memory Limit**: A hard ceiling. If you hit it, you are instantly kicked out of the building.
- **CPU Limit (Quota)**: A stopwatch. You are allowed to work for exactly 10 minutes every hour. Once your time is up, you must freeze until the next hour starts.
- **CPU Shares (Soft)**: A priority queue. If the building is empty, you can use all the desks. If the building is full, you are only guaranteed your specific assigned desk.

## ⚡ Actual Behavior
- **Memory (OOM)**: When a process tries to allocate memory beyond its `--memory` limit, the kernel returns a `null` or triggers a page fault. If the process doesn't handle it, it is killed.
- **CPU (Throttling)**: When a process uses its full `--cpus` quota, the kernel "throttles" it. The process is removed from the CPU scheduler until the next time period (default 100ms).

## 🔬 Internal Mechanics (CFS and OOM)
1. **CFS (Completely Fair Scheduler)**: Docker uses `cpu.cfs_period_us` (usually 100,000µs) and `cpu.cfs_quota_us`. If you set `--cpus 0.5`, Docker sets the quota to 50,000µs.
2. **OOM Score**: Every process has an `oom_score` (0 to 1000). The higher the score, the more likely it is to be killed. Docker containers usually have higher scores than host system processes.
3. **Swap**: By default, Docker allows containers to use swap space if the host has it enabled. You can limit this with `--memory-swap`.

## 🔁 Execution Flow
1. `docker run --memory 512m --cpus 1`
2. Docker writes `536870912` to `memory.limit_in_bytes`.
3. Docker writes `100000` to `cpu.cfs_quota_us`.
4. Kernel monitors every memory allocation and context switch.

## 🧠 Resource Behavior
- **Latency**: CPU Throttling is the #1 cause of "Random P99 Latency Spikes" in microservices.
- **Stability**: Memory limits prevent a memory leak in one app from crashing the entire server.

## 📐 ASCII Diagrams (REQUIRED)

```text
       RESOURCE LIMIT ENFORCEMENT
       
[ CPU QUOTA ]                  [ MEMORY LIMIT ]
  (Throttling)                   (Termination)
      |                              |
[########### ] 80% used        [##########  ] 90% used
[############] 100% used       [############] 100% used
      |                              |
( Wait for next )              ( KERNEL KILL! )
(   interval    )              (  OOMKilled   )
```

## 🔍 Code (Applying Limits)
```bash
# 1. Hard memory limit + No Swap
docker run -d --memory 512m --memory-swap 512m nginx

# 2. Hard CPU Quota (1.5 Cores)
docker run -d --cpus 1.5 nginx

# 3. CPU Shares (Priority)
# This container gets 2x the CPU of a default container (1024) during contention
docker run -d --cpu-shares 2048 nginx

# 4. Check usage
docker stats
```

## 💥 Production Failures
- **The "Invisible Throttling"**: Your app's CPU usage in `docker stats` shows 50%, but the app is slow. 
  *Reason*: You have a bursty app. It hits 100% for 10ms, gets throttled for the rest of the 100ms window, then resumes. `docker stats` averages this out to 50% over a second, hiding the performance hit.
- **OOM Kill Loop**: A Java app is configured with an Xmx (Heap) of 1GB, but the Docker limit is 512MB. The app starts, tries to allocate its heap, and is instantly killed by Docker. It restarts and dies again forever.

## 🧪 Real-time Q&A
**Q: Should I set CPU limits?**
**A**: It depends. Hard limits (`--cpus`) are great for **Predictability** but can waste resources if the host is idle. Soft limits (`--cpu-shares`) are better for **Efficiency** but can lead to "Noisy Neighbor" issues where one container slows down another during peak load.

## ⚠️ Edge Cases
- **Java/Node in Containers**: Older versions of JVM (<8u131) and Node.js don't realize they are in a container and try to use all the host's RAM/CPU, leading to OOM crashes.
  *Fix*: Use modern versions or specify heap size manually.

## 🏢 Best Practices
- **Always set memory limits**: At least as a safety net.
- **Prefer CPU Shares for Internal Apps**: Let them use idle capacity.
- **Use CPU Quotas for Public APIs**: Ensure consistent response times.
- **Monitoring**: Alert when `container_cpu_cfs_throttled_seconds_total` starts increasing.

## ⚖️ Trade-offs
| Strategy | Advantage | Disadvantage |
| :--- | :--- | :--- |
| **No Limits** | Max Performance | Zero Safety |
| **Hard Quotas**| Predictable Latency | Wasted Idle Capacity |
| **Soft Shares** | High Resource ROI | Latency Jitter |

## 💼 Interview Q&A
**Q: What is the difference between CPU Shares and CPU Quotas in Docker?**
**A**: **CPU Quotas** (`--cpus`) set an absolute hard limit on the amount of CPU time a container can use within a specific period (e.g., 50ms per 100ms window), regardless of whether the host is busy or idle. **CPU Shares** (`--cpu-shares`) are relative weights. They only matter when the host's CPU is at 100% utilization. If two containers are fighting for CPU, a container with 2048 shares will get twice as much time as one with 1024. If the host is mostly idle, a container with low shares can still use 100% of the CPU.

## 🧩 Practice Problems
1. Run a container with `--memory 50m`. Use a script to allocate a 100MB array. Verify it gets OOMKilled using `docker inspect`.
2. Run a CPU-heavy container with `--cpus 0.5`. Use `top` on the host to see that it never exceeds 50% of a single core.

---
Prev: [02_Process_Model_PID1.md](./02_Process_Model_PID1.md) | Index: [00_Index.md](../00_Index.md) | Next: [04_Logging_and_STDOUT.md](./04_Logging_and_STDOUT.md)
---
