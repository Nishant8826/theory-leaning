# 📌 Topic: Linux Capabilities Matrix (Permissions)

## 🧠 Concept Explanation (Basic → Expert)
**Basic**: Linux Capabilities are like "Keys" to specific rooms in the OS. Instead of giving a container the "Master Key" (Root), you give it only the keys it needs, like the key to the "Network Room" or the "Time Room."
**Expert**: Capabilities divide the traditionally all-or-nothing **Root Privilege** into 40+ distinct units. By default, Docker grants 14 "Safe" capabilities (like `NET_BIND_SERVICE`) and denies dangerous ones (like `SYS_ADMIN` or `SYS_RAWIO`). Staff-level engineering requires a **Zero-Trust Privilege Model**. This means starting every container with `--cap-drop=ALL` and selectively adding back only the specific capabilities required by the application, drastically reducing the "Blast Radius" of a potential container escape.

## 🏗️ Mental Model
- **Root (Traditional)**: A god-like king. He can do anything, but if he's corrupted, the whole kingdom falls.
- **Capabilities**: A group of specialized professionals. One person can fix the pipes (Network), one can fix the clock (Time), but none of them can replace the king or destroy the kingdom.

## ⚡ Actual Behavior
- **Privilege Escalation**: Even if a hacker gains "Root" inside your container, if you've dropped `CAP_SYS_ADMIN`, they cannot mount the host filesystem or escape to the host.
- **Binding Ports**: An app needs `CAP_NET_BIND_SERVICE` to listen on port 80. Without it, even as root, the app will fail with "Permission Denied."

## 🔬 Internal Mechanics (The Matrix)
1. **Permitted**: The absolute maximum set of capabilities the process can ever have.
2. **Inheritable**: Capabilities that can be passed to child processes.
3. **Effective**: The set of capabilities currently being used by the kernel to perform permission checks.
4. **Ambient**: A set of capabilities that are preserved across an `execve` of a non-privileged program.

## 🔁 Execution Flow (Dropping Privileges)
1. Docker reads the `--cap-drop` flags from the command line.
2. Docker creates a "Bounding Set" for the container.
3. During `clone()`, the kernel ensures the new process can never gain a capability that isn't in its bounding set.
4. If the process tries to call `reboot()`, the kernel checks the `Effective` set for `CAP_SYS_BOOT`.
5. If missing, the call is blocked, regardless of the user's UID.

## 🧠 Resource Behavior
- **Security**: This is the primary defense against "Privilege Escalation" attacks. 
- **Compatibility**: Dropping too many capabilities can break standard tools. For example, `ping` won't work without `CAP_NET_RAW`.

## 📐 ASCII Diagrams (REQUIRED)

```text
       LINUX CAPABILITIES FILTER
       
[ ROOT PRIVILEGES ] 
       |
+------v------+
| CAP FILTER  | <-- ( --cap-drop=ALL )
+------|------+
       |
       +--- [ CAP_NET_BIND_SERVICE ]  (Allow)
       +--- [ CAP_SYS_ADMIN ]         (Block)
       +--- [ CAP_SYS_TIME ]          (Block)
       |
[ CONTAINER APP ] <-- Only has "Safe" keys
```

## 🔍 Code (Auditing Capabilities)
```bash
# 1. Start a container and see default capabilities
docker run --rm alpine capsh --print

# 2. Try to change the hostname (Requires CAP_SYS_ADMIN)
docker run --rm alpine hostname hacker-node
# This works by default because UTS namespace is isolated.

# 3. Try to change the CLOCK (Requires CAP_SYS_TIME - denied by default)
docker run --rm alpine date -s "2030-01-01"
# Result: 'date: can't set date: Operation not permitted'

# 4. Drop EVERYTHING and see it fail
docker run --rm --cap-drop=ALL alpine hostname test
# Result: 'hostname: sethostname: Operation not permitted'
```

## 💥 Production Failures
- **The "Ping" Mystery**: You follow a security guide and use `--cap-drop=ALL`. Suddenly, your health check scripts (which use `ping`) start failing. The app looks down, but it's actually just missing `CAP_NET_RAW`.
- **Nginx Startup Failure**: You run Nginx as a non-root user and drop all caps. Nginx fails to start because it can't bind to port 80.
  *Fix*: Add `--cap-add=NET_BIND_SERVICE` or use a port > 1024.

## 🧪 Real-time Q&A
**Q: What is the most dangerous capability?**
**A**: **CAP_SYS_ADMIN**. It is the "Swiss Army Knife" of capabilities. It allows mounting filesystems, configuring networks, changing cgroups, and many other things that can lead to a host escape. It is basically "Root-lite" and should **NEVER** be given to a production container.

## ⚠️ Edge Cases
- **Setuid Binaries**: Some programs (like `sudo`) rely on the "Setuid" bit to gain privileges. Dropping capabilities can break these programs even if they are run by root.
- **Kernel Version**: Newer kernels add new capabilities (like `CAP_BPF` or `CAP_CHECKPOINT_RESTORE`). Ensure your Docker version knows about these if you need them.

## 🏢 Best Practices
- **Audit your App**: Use `getpcaps <pid>` to see exactly what your app is using.
- **The Golden Rule**: `--cap-drop=ALL` first, then add only what breaks.
- **Combine with Seccomp**: Capabilities limit what you can *do*, Seccomp limits what you can *say* (syscalls). Use both for a "Defense in Depth."

## ⚖️ Trade-offs
| Security Setting | Security Level | Maintenance |
| :--- | :--- | :--- |
| **Default Caps** | Medium | **Easy** |
| **Cap-Add/Drop** | **High** | Medium |
| **Cap-Drop ALL** | **Highest** | High (Trial & Error)|

## 💼 Interview Q&A
**Q: Why would you use '--cap-drop=ALL' if the container is already running as a non-root user?**
**A**: Even as a non-root user, a process can potentially exploit a kernel vulnerability to escalate its privileges. If the container still has the default set of capabilities, an attacker who successfully gains root could then use those capabilities (like `CAP_CHOWN` or `CAP_FOWNER`) to modify sensitive files or further their attack. By dropping **all** capabilities, you ensure that even if the process is compromised and somehow gains root privileges, it still has **no power** to perform privileged kernel operations, providing a critical second layer of defense.

## 🧩 Practice Problems
1. List all capabilities currently held by your shell using `capsh --print`.
2. Find the minimum set of capabilities required to run a `tcpdump` inside a container.
3. Research the `CAP_NET_ADMIN` capability and list 3 dangerous things it allows a user to do.

---
Prev: [04_OCI_Spec_and_runc.md](./04_OCI_Spec_and_runc.md) | Index: [00_Index.md](../00_Index.md) | Next: [01_Docker_Node_React_Deployment.md](../Projects/01_Docker_Node_React_Deployment.md)
---
