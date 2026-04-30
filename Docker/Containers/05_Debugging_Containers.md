# 📌 Topic: Debugging Containers (The Staff Toolchain)

## 🧠 Concept Explanation (Basic → Expert)
**Basic**: When a container is broken, you use `docker logs` to see the error or `docker exec` to go inside and look around.
**Expert**: Production debugging involves **Observability** and **Sidecar Investigation**. In a hardened environment (Distroless/No-Shell), `docker exec` won't work. Staff-level engineers use `docker inspect` to analyze metadata, `docker events` to track state changes, and **Ephemeral Debug Containers** that share the target container's namespaces (Network/PID) to run diagnostic tools (`tcpdump`, `strace`, `lsof`) without modifying the original image.

## 🏗️ Mental Model
- **The Surgeon**: You don't open the patient up (Modify image) to see what's wrong. You use an X-ray (docker inspect) or an Endoscope (sidecar container) to look inside without causing trauma.

## ⚡ Actual Behavior
- **`docker logs --tail 100 -f`**: The first line of defense.
- **`docker inspect`**: Returns the entire JSON configuration (Env vars, IP addresses, Mount points, Health status).
- **`docker top`**: Shows the processes running *inside* the container from the perspective of the host.

## 🔬 Internal Mechanics (Namespace Sharing)
The most powerful debugging technique is joining the namespace of a running container.
1. Every container has its own Network and PID namespace.
2. You can start a *second* container with `--network container:<target_id>`.
3. Now, the second container sees the same `localhost`, the same open ports, and the same network traffic as the first one.

## 🔁 Execution Flow (Debugging a "Silent" failure)
1. `docker ps`: Is it running?
2. `docker logs`: Did it crash?
3. `docker inspect`: Are the environment variables correct?
4. `docker stats`: Is it hitting a memory limit (OOM)?
5. `docker exec`: (If shell exists) check config files.
6. **Namespace Join**: (If no shell) Run a net-shoot container to check connectivity.

## 🧠 Resource Behavior
- **Sidecar Overhead**: Debugging containers consume host resources. Be careful when running `tcpdump` on a high-traffic production container, as it can saturate the CPU.

## 📐 ASCII Diagrams (REQUIRED)

```text
       SIDECAR DEBUGGING PATTERN
       
+-----------------------+       +-----------------------+
|  Target Container     |       |   Debug Container     |
|  (Node.js / No Shell) |       |   (Alpine / Tools)    |
|                       |       |                       |
| [ NET Namespace ] <-------+------- [ Join NET NS ]    |
| [ PID Namespace ] <-------+------- [ Join PID NS ]    |
|                       |       |                       |
+-----------------------+       +-----------------------+
                                |  $ tcpdump -i eth0    |
                                |  $ ps aux             |
                                +-----------------------+
```

## 🔍 Code (Advanced Debugging CLI)
```bash
# 1. Debug Networking in a Distroless container
# Run 'nicolaka/netshoot' sharing the network stack of 'myapp'
docker run --rm -it --network container:myapp nicolaka/netshoot

# 2. See the diff between image and current container state
# (What files were modified/added?)
docker diff my-container

# 3. Analyze why a container is slow (Host level)
PID=$(docker inspect -f '{{.State.Pid}}' my-container)
sudo strace -p $PID

# 4. Check events (Real-time lifecycle)
docker events --filter 'container=myapp'
```

## 💥 Production Failures
- **The "Heisenbug"**: An app only fails under heavy load. You try to `docker exec` and run tools, but the very act of running those tools changes the CPU timing and the bug disappears.
  *Fix*: Use passive monitoring (Prometheus/X-Ray) instead of interactive debugging.
- **"Connection Refused" but Service is Up**: The app is listening on `127.0.0.1` inside the container instead of `0.0.0.0`. It works for internal health checks but fails for the external Load Balancer.

## 🧪 Real-time Q&A
**Q: How do I debug a container that crashes immediately upon start?**
**A**: Use `docker logs <id>` (the logs persist after exit). If the logs are empty, use `docker run --rm -it <image> /bin/sh` to override the ENTRYPOINT and manually run the app to see the error.

## ⚠️ Edge Cases
- **Kernel-level hangs**: If a container is in a `D` state (Uninterruptible Sleep), even `docker kill -9` might fail. This usually indicates a hardware or filesystem driver issue (NFS hang).

## 🏢 Best Practices
- **Log to STDOUT**: Never hide logs in files.
- **Include Healthchecks**: Let Docker/Kubernetes tell you when a container is "Limping."
- **Keep a "Debug Toolkit" Image**: Have an image with `curl`, `dig`, `tcpdump`, `jq`, and `lsof` ready to go in your registry.

## ⚖️ Trade-offs
| Tool | Depth | Risk |
| :--- | :--- | :--- |
| **docker logs** | Surface | **Zero** |
| **docker exec** | Deep | Medium (Modifies state) |
| **Sidecar** | **Deepest**| Low (Namespace only) |

## 💼 Interview Q&A
**Q: If a container has no shell (e.g., Distroless), how can you troubleshoot network connectivity issues?**
**A**: I use the **Namespace Joining** pattern. I run a temporary "troubleshooting" container (like `netshoot`) and use the `--network container:<target_id>` flag. This allows the debug container to see the exact network environment of the target container, allowing me to use `tcpdump`, `nslookup`, or `curl` to diagnose the issue without needing a shell in the original container.

## 🧩 Practice Problems
1. Run a container in the background. Use `docker diff` to see what happens when you create a file inside it.
2. Try to `strace` a running container from the host.
3. Use a sidecar container to see the open ports of a running Nginx container.

---
Prev: [04_Logging_and_STDOUT.md](./04_Logging_and_STDOUT.md) | Index: [00_Index.md](../00_Index.md) | Next: [06_Rootless_Containers.md](./06_Rootless_Containers.md)
---
