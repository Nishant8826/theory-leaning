# 📌 Topic: Rootless Containers (Defense in Depth)

## 🧠 Concept Explanation (Basic → Expert)
**Basic**: Normally, the Docker Engine runs with "Root" (God) privileges on your computer. If a container is hacked, the hacker might get root on your whole computer. Rootless Docker allows you to run Docker as a normal user, so even if it's hacked, the damage is limited.
**Expert**: Rootless Containers are an architecture where both the **Docker Daemon** and the **Containers** run without `root` privileges. This is achieved by leveraging **User Namespaces** (`CLONE_NEWUSER`), which map a range of UIDs inside the container to a non-privileged range on the host. This significantly mitigates "Container Escape" vulnerabilities, as the process inside the container is technically unprivileged from the host kernel's perspective.

## 🏗️ Mental Model
- **Standard Docker**: A security guard who has the master key to the entire building. If someone steals the key, they can enter every office.
- **Rootless Docker**: A security guard who only has a key to one specific floor. If they lose the key, the rest of the building is still safe.

## ⚡ Actual Behavior
- **No Sudo**: You run `docker run` without `sudo`.
- **Restricted Ports**: You cannot bind a container to a privileged port (0-1023) like port 80 or 443 unless you explicitly configure the kernel to allow it for your user.
- **Host Protection**: If a process inside a rootless container successfully escapes the container, it still only has the privileges of the user who started Docker.

## 🔬 Internal Mechanics (UID Mapping)
1. **User Namespaces**: Map the container's `root` (UID 0) to a host user (e.g., UID 1001).
2. **SubUID/SubGID**: Files `/etc/subuid` and `/etc/subgid` define the range of IDs the user is allowed to "fake" inside the namespace (e.g., mapping 0-65535 inside to 100000-165535 outside).
3. **Slirp4netns**: Since a non-root user can't create network interfaces, Rootless Docker uses `slirp4netns` to provide a user-mode networking stack.

## 🔁 Execution Flow
1. User installs rootless-kit.
2. User starts `dockerd-rootless.sh`.
3. Daemon starts within a User Namespace.
4. When a container starts, `runc` uses the mapped UID range.
5. Filesystem access is managed via `fuse-overlayfs` (as a normal user can't perform standard overlay mounts).

## 🧠 Resource Behavior
- **Performance**: Networking is slightly slower due to `slirp4netns` overhead. Filesystem is slower due to `fuse-overlayfs`.
- **Memory**: Slightly higher overhead for the user-mode networking stack.

## 📐 ASCII Diagrams (REQUIRED)

```text
       ROOT vs ROOTLESS ARCHITECTURE
       
   [ STANDARD ]                    [ ROOTLESS ]
+-------------------+          +-----------------------+
|  Container (Root) |          |  Container (Mapped)   |
+-------------------+          +-----------------------+
|  Docker Daemon    |          |  Rootless Kit / Slirp |
|  (RUNS AS ROOT)   |          |  (RUNS AS USER)       |
+---------|---------+          +-----------|-----------+
          v                                v
+-------------------+          +-----------------------+
|  Host Kernel      |          |  Host Kernel          |
|  (Full Risk)      |          |  (Limited Risk)       |
+-------------------+          +-----------------------+
```

## 🔍 Code (Setup and Verification)
```bash
# 1. Install rootless support (Ubuntu example)
curl -fsSL https://get.docker.com/rootless | sh

# 2. Check current context
docker context ls

# 3. Verify ID mapping
docker run --rm alpine id
# Returns uid=0(root)

# On host, check the actual process:
ps -ef | grep sleep
# Shows UID 100000 (from subuid range)
```

## 💥 Production Failures
- **The "Port 80" Failure**: You try to start a web server on port 80 in rootless mode. It fails with `permission denied`.
  *Fix*: Use a port > 1024 or set `sysctl net.ipv4.ip_unprivileged_port_start=80`.
- **The "Ping" Failure**: Ping doesn't work inside some rootless containers because the `ICMP` socket requires root.
  *Fix*: Configure `net.ipv4.ping_group_range`.

## 🧪 Real-time Q&A
**Q: Is Rootless Docker ready for production?**
**A**: It depends on your needs. For high-performance databases or heavy I/O, the FUSE and Slirp overhead might be too high. For standard web APIs and CI/CD builders, it's a great security upgrade.

## ⚠️ Edge Cases
- **OverlayFS Support**: Some older Linux distributions don't allow non-root users to use OverlayFS, forcing Docker to use the very slow `vfs` storage driver.

## 🏢 Best Practices
- **Use for CI/CD**: Rootless Docker is perfect for build runners, preventing a malicious build script from compromising the build server.
- **Hardened SubUIDs**: Ensure `/etc/subuid` ranges don't overlap between different users.

## ⚖️ Trade-offs
| Feature | Root Docker | Rootless Docker |
| :--- | :--- | :--- |
| **Security** | Low | **High** |
| **Performance** | **High** | Medium |
| **Compatibility** | **Full** | Limited (Networking/Storage) |

## 💼 Interview Q&A
**Q: How does Rootless Docker protect the host system?**
**A**: Rootless Docker uses Linux **User Namespaces**. It maps the container's root user to a standard, unprivileged user on the host. Even if a process escapes the container's isolation, it only has the permissions of that unprivileged host user. It cannot modify system files, access other users' data, or perform administrative tasks on the host kernel, effectively neutering the impact of a container escape.

## 🧩 Practice Problems
1. Install Rootless Docker in a VM. Try to run an Nginx container on port 80.
2. Use `cat /etc/subuid` and calculate the range of IDs assigned to your user.
3. Compare the network latency of a Root vs Rootless container using `ping` or `curl`.

---
Prev: [05_Debugging_Containers.md](./05_Debugging_Containers.md) | Index: [00_Index.md](../00_Index.md) | Next: [01_Bridge_Network.md](../Networking/01_Bridge_Network.md)
---
