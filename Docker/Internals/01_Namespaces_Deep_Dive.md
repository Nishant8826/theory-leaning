# 📌 Topic: Namespaces Deep Dive (Isolation)

## 🧠 Concept Explanation (Basic → Expert)
**Basic**: Namespaces are the "Walls" of a Docker container. They make a process think it's the only thing running on the computer. It has its own files, its own network, and its own list of other processes.
**Expert**: Namespaces are a **Linux Kernel Virtualization Primitive**. They provide **Resource Isolation** by wrapping a set of system resources in an abstraction that makes them appear unique to the process. Staff-level engineering requires understanding that Namespaces do NOT provide security (that's cgroups and Seccomp), they only provide **Visibility Isolation**. There are 7 primary types of namespaces: **PID** (Process IDs), **NET** (Networking), **MNT** (Mount points), **UTS** (Hostname), **IPC** (Inter-process communication), **USER** (User IDs), and **CGROUP** (cgroup hierarchy).

## 🏗️ Mental Model
- **The Apartment Building**: The Linux Kernel is the building. Each container is an apartment.
- **Namespaces**: The walls and the floor numbers. In Apartment 101, you have a kitchen and a bathroom. In Apartment 201, you *also* have a kitchen and a bathroom. You can't see into the other apartment, and you think your kitchen is the "only" kitchen.

## ⚡ Actual Behavior
- **PID 1**: Inside a container, your app is PID 1. On the host, that same app might be PID 5432. The PID namespace maps the host's 5432 to the container's 1.
- **Independent Networking**: A container can have its own IP address and its own `eth0` interface, completely separate from the host's `eth0`.

## 🔬 Internal Mechanics (The 7 Namespaces)
1. **PID (Process)**: Isolates the process ID space. Prevents a container from seeing or `kill`-ing processes in other containers.
2. **NET (Network)**: Isolates network devices, IP addresses, routing tables, and firewall rules.
3. **MNT (Mount)**: Isolates the list of mount points. A container has its own `/`, `/etc`, and `/var`.
4. **UTS (Hostname)**: Isolates the hostname and NIS domain name. Allows a container to have its own name (e.g., `web-server-1`).
5. **IPC (Inter-process Communication)**: Isolates System V IPC objects and POSIX message queues.
6. **USER (User ID)**: Maps a container's root (UID 0) to a non-privileged user on the host. (Essential for security).
7. **CGROUP**: Isolates the view of the cgroup hierarchy.

## 🔁 Execution Flow (Creating a Namespace)
1. Docker calls the `clone()` or `unshare()` system call with specific flags (e.g., `CLONE_NEWPID`).
2. The Kernel creates a new "Namespace Object."
3. The new process is "Pinned" to this namespace.
4. From now on, any kernel request (e.g., "List all processes") is filtered by the namespace object.
5. The process only sees what the namespace allows it to see.

## 🧠 Resource Behavior
- **Performance**: Namespaces have **Zero Performance Overhead**. It's just a pointer in the kernel's process structure.
- **Limits**: Namespaces do NOT limit resources (e.g., a process in a namespace can still use 100% of the host's CPU). That is the job of **cgroups**.

## 📐 ASCII Diagrams (REQUIRED)

```text
       LINUX KERNEL NAMESPACES
       
[ HOST OS ] (Real PID 500, 501, 502)
    |
    +----[ PID Namespace A ] ----> (Container sees PID 1, 2)
    |
    +----[ PID Namespace B ] ----> (Container sees PID 1, 2)
    |
    +----[ NET Namespace A ] ----> (Container sees IP 172.17.0.2)
```

## 🔍 Code (Exploring Namespaces)
```bash
# 1. Start a container
docker run -d --name test-ns alpine sleep 1000

# 2. Find the PID of the process on the HOST
PID=$(docker inspect -f '{{.State.Pid}}' test-ns)

# 3. List the namespaces for that PID
ls -l /proc/$PID/ns

# 4. 'Enter' a container's namespace from the host
# (This is how 'docker exec' works internally)
nsenter -t $PID -n ip addr show
```

## 💥 Production Failures
- **The "Zombie Reaper"**: You run an app as PID 1 that doesn't "reap" child processes. Over time, the container fills up with "Zombie" processes that can't be killed because they are in their own PID namespace.
  *Fix*: Use `tini` or `dumb-init` as your entrypoint.
- **Shared Networking**: You run two containers with `--network host`. Both try to bind to port 80. The second one fails because they are sharing the host's NET namespace.

## 🧪 Real-time Q&A
**Q: Are namespaces the same as Virtual Machines?**
**A**: **No.** A VM has its own Kernel and virtualized hardware. A container uses the **Host's Kernel**. Namespaces are just "Glasses" the kernel puts on the process to limit what it can see.

## ⚠️ Edge Cases
- **The 'Mount' Trap**: If you mount a host directory into a container, and then change the mount on the host, the container might not see the change because its MNT namespace "took a snapshot" of the mount table when it started.

## 🏢 Best Practices
- **Use User Namespaces**: Always map container root to a non-root host user.
- **Don't use `--pid=host`**: Unless you are running a debugging tool (like `htop`) that needs to see the whole system.
- **Namespace Awareness**: When writing monitoring tools, ensure they can "look into" other namespaces using the `/proc` filesystem.

## ⚖️ Trade-offs
| Feature | Virtual Machine | Namespace (Container) |
| :--- | :--- | :--- |
| **Isolation** | **Highest (Hardware)** | High (Logical) |
| **Speed** | Slow (Minutes) | **Instant (Milliseconds)**|
| **Overhead** | High (Full OS) | **Zero** |

## 💼 Interview Q&A
**Q: How does a Docker container achieve isolation from the host and other containers?**
**A**: Docker uses **Linux Namespaces** to provide isolation. When a container starts, Docker creates a set of namespaces (PID, NET, MNT, etc.) and attaches the container's processes to them. For example, the PID namespace ensures the container has its own process tree starting at PID 1, while the NET namespace provides it with its own virtual network stack. This ensures that the processes inside the container cannot see or interact with processes, files, or networks outside their assigned namespaces, creating the "Illusion" of a separate operating system.

## 🧩 Practice Problems
1. Use `nsenter` to run a command inside a container without using `docker exec`.
2. Compare the output of `ps aux` on your host and inside a running container.
3. Try to change the hostname of a container and verify that the host's hostname remains unchanged.

---
Prev: [05_Disaster_Recovery_Planning.md](../Reliability/05_Disaster_Recovery_Planning.md) | Index: [00_Index.md](../00_Index.md) | Next: [02_Cgroups_and_Resource_Control.md](./02_Cgroups_and_Resource_Control.md)
---
