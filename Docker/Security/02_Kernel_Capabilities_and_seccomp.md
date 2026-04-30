# 📌 Topic: Kernel Capabilities and Seccomp (Hardening)

## 🧠 Concept Explanation (Basic → Expert)
**Basic**: Kernel Capabilities and Seccomp are "security filters." Capabilities control what "Superpowers" a container has (like changing the clock). Seccomp controls what "Words" (System Calls) a container can say to the Linux Kernel.
**Expert**: This is the implementation of the **Principle of Least Privilege** at the syscall level. By default, a Docker container has a subset of the ~300 available Linux capabilities and is restricted by a default Seccomp profile that blocks dangerous syscalls (like `mount`, `reboot`, or `ptrace`). Staff-level engineering requires building **Custom Seccomp Profiles** for high-security apps and using **Capability Dropping** to remove everything except the bare essentials (like `NET_BIND_SERVICE`).

## 🏗️ Mental Model
- **Capabilities**: A tool belt. A plumber needs a wrench (Network) but doesn't need a chainsaw (Format Disk). We take the chainsaw away.
- **Seccomp**: A firewall for the Kernel's brain. The app can say "Open File" and "Write File," but if it says "Destroy System," the Kernel ignores it and kills the app.

## ⚡ Actual Behavior
- **Default Seccomp**: Docker blocks ~44 syscalls out of ~300. This is enough to stop most generic exploits.
- **Capabilities**: By default, Docker gives you things like `CHOWN` and `NET_RAW`, but denies `SYS_ADMIN` (the most dangerous superpower).

## 🔬 Internal Mechanics (The Syscall Filter)
1. **Capabilities**: Defined in `man 7 capabilities`. They break down the "All-or-nothing" root power into granular units.
2. **Seccomp (Secure Computing Mode)**: Uses a BPF (Berkeley Packet Filter) program to intercept every single syscall made by the container. If the syscall is not in the "Allow List," the kernel sends a `SIGSYS` or returns `EPERM`.
3. **The Filter**: When a container starts, `runc` loads the Seccomp JSON profile into the kernel's memory for that specific process tree.

## 🔁 Execution Flow
1. App in container calls `reboot()`.
2. Kernel Seccomp filter intercepts the call.
3. Profile says: `reboot` is BLOCKED.
4. Kernel kills the process or returns an error.
5. Container stays isolated; host stays up.

## 🧠 Resource Behavior
- **Performance**: Seccomp adds a very tiny overhead to every syscall (nanoseconds). It is usually unnoticeable.
- **Security**: This is the most effective defense against "Zero-day" kernel exploits. Even if a bug exists in the kernel's `mount` code, the container can't trigger it if the `mount` syscall is blocked by Seccomp.

## 📐 ASCII Diagrams (REQUIRED)

```text
       SYSCALL FILTERING LAYERS
       
[ App Code ] 
      |
 ( Syscall: 'reboot' )
      |
      v
+-----------------------+
|  Seccomp Filter (BPF) | <-- "Is reboot allowed?" -> NO!
+-----------------------+
      |
      v
[ Linux Kernel ]        <-- Never sees the request
```

## 🔍 Code (Dropping Capabilities)
```bash
# 1. Start a container and DROP all capabilities, then add back only what is needed
# This is the 'Gold Standard' for security
docker run --rm -it \
  --cap-drop=ALL \
  --cap-add=NET_BIND_SERVICE \
  alpine sh

# 2. Run with a custom Seccomp profile
docker run --rm -it \
  --security-opt seccomp=/path/to/my-profile.json \
  alpine sh

# 3. List current capabilities inside a container
# (Requires 'libcap' package)
capsh --print
```

## 💥 Production Failures
- **The "Ping" Failure**: You drop all capabilities, but your app needs to `ping` another service. `ping` requires `CAP_NET_RAW`. The app fails with "Operation not permitted."
- **Nginx Port 80**: You drop all capabilities. Nginx fails to start because it can't bind to port 80 (requires `CAP_NET_BIND_SERVICE`).

## 🧪 Real-time Q&A
**Q: Should I use `--privileged`?**
**A**: **NEVER** in production. `--privileged` adds all capabilities and disables all Seccomp filters. It gives the container full access to the host kernel and hardware. It is a massive security hole.

## ⚠️ Edge Cases
- **New Syscalls**: When the Linux kernel adds new syscalls (like `io_uring`), older Seccomp profiles might not know about them. Docker's default profile is updated regularly to handle this.

## 🏢 Best Practices
- **Drop ALL, then add**: Start with `--cap-drop=ALL` and only add what the app actually breaks without.
- **Use `no-new-privileges`**: Combine with `--security-opt=no-new-privileges` to prevent a process from ever gaining new capabilities (e.g., via a `setuid` binary).
- **Custom Profiles**: For high-value targets (databases/gateways), use tools like `strace` to find exactly which syscalls the app uses and block everything else.

## ⚖️ Trade-offs
| Security Level | Complexity | Protection |
| :--- | :--- | :--- |
| **Default** | **Low** | Medium |
| **Cap-Drop ALL** | Medium | **High** |
| **Custom Seccomp** | High | **Highest** |

## 💼 Interview Q&A
**Q: What is the difference between Linux Capabilities and Seccomp in Docker?**
**A**: **Capabilities** are high-level "superpowers" (e.g., the ability to change the system clock or open a raw network socket). They break down the power of `root` into smaller pieces. **Seccomp** is a low-level "syscall firewall." It works at the interface between the application and the kernel, allowing or blocking specific low-level functions (e.g., `execve`, `mount`, `mkdir`). You use Capabilities to limit what the process can *do* as a user, and Seccomp to limit how the process can *interact* with the kernel.

## 🧩 Practice Problems
1. Try to change the system time inside a container. Observe the failure.
2. Use `docker inspect` on a running container and look for the `CapAdd` and `CapDrop` sections.
3. Research the "Default Docker Seccomp Profile" on GitHub and see which syscalls it blocks.

---
Prev: [01_Docker_Daemon_Security.md](./01_Docker_Daemon_Security.md) | Index: [00_Index.md](../00_Index.md) | Next: [03_Scanning_Images_Trivy.md](./03_Scanning_Images_Trivy.md)
---
