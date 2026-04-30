# 📌 Topic: Container Lifecycle (Internal States)

## 🧠 Concept Explanation (Basic → Expert)
**Basic**: A container is like a lamp. You can turn it on (`start`), turn it off (`stop`), or throw it away (`rm`).
**Expert**: The Container Lifecycle is a state machine managed by the **Container Runtime**. It involves distinct phases: **Created**, **Running**, **Paused**, **Exited**, and **Dead**. Staff-level engineering requires understanding the transition signals (SIGTERM vs SIGKILL), the role of the `containerd-shim` in maintaining state during daemon restarts, and how the "Exited" state preserves the writable layer and logs until explicit removal.

## 🏗️ Mental Model
- **Created**: A car with the engine off, parked in a garage. All the seats are in place, but it's not moving.
- **Running**: The car is driving on the highway.
- **Paused**: The car is at a red light. The engine is still on, but it's not moving and not consuming "road time" (CPU).
- **Exited**: The car is parked and the engine is off.
- **Dead**: The car is in a scrap yard.

## ⚡ Actual Behavior
- **`stop`**: Sends `SIGTERM` to PID 1, waits 10 seconds (default), then sends `SIGKILL`.
- **`kill`**: Sends `SIGKILL` immediately. The process doesn't get a chance to save data or close connections.
- **`pause`**: Uses the `freezer` cgroup to suspend all processes in the container. Memory is preserved, but no CPU cycles are used.

## 🔬 Internal Mechanics (The State Machine)
1. **Created**: `containerd` has set up the OCI bundle and `runc` has initialized the namespaces, but the application entrypoint has not yet been executed.
2. **Running**: The `execve` syscall has been called, and the application is running as PID 1.
3. **Exited**: The PID 1 process has terminated. The container's filesystem (UpperDir) and logs remain on the host disk.
4. **Restarting**: If a `restart-policy` is set, Docker will move the container from Exited back to Running.

## 🔁 Execution Flow
1. `docker create`: `runc create`.
2. `docker start`: `runc start` -> `execve`.
3. `docker pause`: `SIGSTOP` or cgroup freezer.
4. `docker stop`: `SIGTERM` -> (wait) -> `SIGKILL`.
5. `docker rm`: Deletes the writable layer (UpperDir) and metadata.

## 🧠 Resource Behavior
- **Memory**: Paused containers still hold their RAM. Stopped containers release RAM but hold Disk space.
- **CPU**: Only Running containers consume CPU.

## 📐 ASCII Diagrams (REQUIRED)

```text
       CONTAINER STATE MACHINE
       
     [ docker create ]
            |
            v
       ( CREATED ) <-------+
            |              |
      [ docker start ]     | [ docker restart ]
            |              |
            v              |
       ( RUNNING ) --------+
       /    |    \
 [pause] [stop] [kill]
    |       |      |
(PAUSED) (EXITED) (DEAD)
            |
       [ docker rm ]
            |
        ( DELETED )
```

## 🔍 Code (State Inspection)
```bash
# 1. Create but don't start
docker create --name inactive alpine sleep 100
docker ps -a --filter name=inactive

# 2. Watch events during lifecycle
docker events &

# 3. Stop with custom timeout
docker stop --time 30 my-container

# 4. Inspect exit code
docker inspect my-container --format='{{.State.ExitCode}}'
```

## 💥 Production Failures
- **The "Unstoppable Container"**: Your app ignores `SIGTERM`. When you `docker stop`, it hangs for 10 seconds every time before being forcefully killed.
  *Fix*: Ensure your app handles signals correctly or use `STOPSIGNAL` in Dockerfile.
- **Disk Exhaustion (Exited Containers)**: You run thousands of short-lived containers but forget to `rm` them. Each one leaves behind a writable layer and logs until `/var/lib/docker` is full.
  *Fix*: Use `docker run --rm`.

## 🧪 Real-time Q&A
**Q: What is a "Dead" state?**
**A**: A container enters the "Dead" state when an error occurs during its removal (e.g., a resource is busy or a filesystem mount is stuck). It's a "Zombie" container that is neither running nor fully deleted. You often need to manually unmount its layers to fix it.

## ⚠️ Edge Cases
- **Zombie Processes**: if your PID 1 doesn't reap child processes, and those children exit, they stay as zombies. The container might stay "Running" but the host will slowly run out of PIDs.

## 🏢 Best Practices
- **Use `SIGTERM` handlers**: Always wrap your app (especially Node/Python) to handle signals and shut down gracefully.
- **Auto-Cleanup**: Use `--rm` for one-off tasks (like migrations or builds).
- **Prune Regularly**: Run `docker container prune` to clean up old exited containers.

## ⚖️ Trade-offs
| Command | Strategy | Risk |
| :--- | :--- | :--- |
| **stop** | Graceful | Slow (Wait time) |
| **kill** | Immediate | Data Loss / Corruption |
| **pause** | Suspend | Holds Memory |

## 💼 Interview Q&A
**Q: What happens when you run `docker stop` on a container?**
**A**: Docker sends a **SIGTERM** signal to the process running as PID 1 inside the container. It then starts a grace period (default 10 seconds). If the process terminates within this window, the container enters the "Exited" state. If the process is still running after the grace period, Docker sends a **SIGKILL** to forcefully terminate it. This ensures that applications have a chance to clean up resources, but also ensures the host can eventually reclaim control.

## 🧩 Practice Problems
1. Run a container, `pause` it, and try to `exec` into it. Observe what happens.
2. Write a simple Node.js script that traps `SIGTERM` and prints "Shutting down..." before exiting. Verify it works with `docker stop`.

---
Prev: [07_SBOM_and_Image_Signing.md](../Images/07_SBOM_and_Image_Signing.md) | Index: [00_Index.md](../00_Index.md) | Next: [02_Process_Model_PID1.md](./02_Process_Model_PID1.md)
---
