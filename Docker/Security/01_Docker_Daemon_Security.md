# 📌 Topic: Docker Daemon Security (Hardening)

## 🧠 Concept Explanation (Basic → Expert)
**Basic**: The Docker Daemon is the "boss" of Docker on your computer. If a hacker gets control of the boss, they can control your whole computer. Hardening is about putting locks on the boss's door.
**Expert**: The Docker Daemon (`dockerd`) runs as a privileged process (`root`) and interacts directly with the Linux kernel (namespaces, cgroups). Staff-level engineering requires securing the **Daemon Attack Surface**. This involves moving away from the default insecure Unix socket to **TLS-encrypted TCP sockets**, implementing **User Namespaces** for UID remapping, enabling **Live Restore** for stability, and strictly controlling the `docker` group membership. A compromised daemon is equivalent to "Root on the Host," making its protection the most critical security task in the infrastructure.

## 🏗️ Mental Model
- **The Docker Daemon**: An all-powerful janitor who has the keys to every room in a building. 
- **Hardening**: Making sure the janitor only answers the phone (API) if the caller has a secret code (TLS Certificate) and ensuring that even if someone steals the janitor's keys, they can only open certain rooms (User Namespaces).

## ⚡ Actual Behavior
- **The Socket Problem**: By default, any user in the `docker` group can run *any* command as root. They can mount the host's `/etc/shadow` into a container and change your password.
- **The API Problem**: If you expose Docker on a network port (`2375`) without TLS, anyone on the internet can take over your server in 2 seconds.

## 🔬 Internal Mechanics (The Hardening Layers)
1. **TLS Authentication**: Uses Mutual TLS (mTLS). Both the client and the daemon must present certificates signed by a trusted CA.
2. **User Namespaces (`userns-remap`)**: Maps the container's `root` (UID 0) to a non-privileged user (e.g., UID 100000) on the host. If the container process escapes, it has NO power on the host.
3. **Authorization Plugins (AuthZ)**: Allows you to use tools like OPA (Open Policy Agent) to restrict specific Docker commands (e.g., "Developers can run containers, but they can't mount `/var/log`").

## 🔁 Execution Flow (Securing the Socket)
1. Remove `docker` group membership for non-admin users.
2. Generate CA, Server, and Client certificates.
3. Configure `daemon.json` to use `tlsverify`.
4. Restart Docker.
5. Client must now use `--tlsverify` and provide keys to talk to Docker.

## 🧠 Resource Behavior
- **CPU**: TLS encryption adds a negligible overhead to API calls.
- **Stability**: Using `live-restore` allows containers to keep running even if the Docker Daemon crashes or is being upgraded.

## 📐 ASCII Diagrams (REQUIRED)

```text
       DAEMON SECURITY ARCHITECTURE
       
[ Remote Client ] --( TCP:2376 + TLS )--> [ Docker Daemon ]
                                              |
          +-----------------------------------+-----------------------+
          |                                   |                       |
 [ User Namespace ]                  [ AuthZ Plugin ]        [ AppArmor / SecComp ]
 (UID Mapping)                       (Policy Check)          (Syscall Filtering)
          |                                   |                       |
   [ Container 0 ]                     [ Verified Cmd ]        [ Blocked Syscall ]
```

## 🔍 Code (Hardening the Daemon)
```json
// /etc/docker/daemon.json
{
  "icc": false,               // Disable inter-container communication by default
  "userns-remap": "default",  // Enable User Namespace remapping
  "live-restore": true,       // Keep containers running during daemon restart
  "no-new-privileges": true,  // Prevent processes from gaining more privileges (suid)
  "tlsverify": true,          // Enable TLS verification
  "tlscacert": "/etc/docker/ca.pem",
  "tlscert": "/etc/docker/server-cert.pem",
  "tlskey": "/etc/docker/server-key.pem"
}
```

## 💥 Production Failures
- **The "Exposed Socket" Ransomware**: A developer opens port 2375 to debug a remote server. A bot finds the port, runs a privileged container, mounts the host root, and encrypts the entire server disk for ransom.
- **Update Failure**: You enable `userns-remap` on a running system. Existing containers fail to start because they don't have permission to read their own volumes (which are owned by the old "real" root).
  *Fix*: You must manually `chown` volumes to the new mapped UID range.

## 🧪 Real-time Q&A
**Q: If I use Rootless Docker, do I still need to harden the daemon?**
**A**: Rootless Docker *is* the ultimate hardening. It runs the daemon itself as a non-root user. However, if you are forced to use standard Docker (for performance or feature reasons), then `userns-remap` and TLS are your best defenses.

## ⚠️ Edge Cases
- **Privileged Containers**: Using `--privileged` completely bypasses almost all daemon security measures. Never use it in production unless you are running specialized system tools (like a CNI plugin).

## 🏢 Best Practices
- **Restrict the Socket**: Only allow `root` and a very small group of trusted admins to access `/var/run/docker.sock`.
- **Audit Logs**: Enable `journald` logging for Docker to track every command executed against the API.
- **Regular Updates**: Most "Daemon Escapes" are fixed in newer versions. Stay current.

## ⚖️ Trade-offs
| Feature | Security Benefit | Complexity |
| :--- | :--- | :--- |
| **TLS** | Prevents remote takeover| High (Cert management) |
| **User NS** | Prevents host escape | High (Permission issues) |
| **ICC: False**| Limits Lateral Movement| Low |

## 💼 Interview Q&A
**Q: What is the risk of adding a user to the `docker` group on a Linux server?**
**A**: Adding a user to the `docker` group is effectively granting them **full root privileges** on the host. Since the Docker daemon runs as root, any user with access to the Docker socket can start a container, mount the host's root filesystem (`/`) into that container, and then modify any file on the host—including `/etc/shadow` or adding their own SSH key to `/root/.ssh/authorized_keys`. This allows for a trivial and immediate escalation to full root access on the physical/virtual server.

## 🧩 Practice Problems
1. Use `docker run -v /:/host alpine cat /host/etc/shadow` to see how easy it is to read host secrets with standard Docker.
2. Enable `userns-remap` and try the same command. Notice that it fails or returns an empty/protected file.
3. Generate a set of TLS certificates and configure your Docker daemon to only accept encrypted connections.

---
Prev: [05_Content_Trust_and_Signing.md](../Registry/05_Content_Trust_and_Signing.md) | Index: [00_Index.md](../00_Index.md) | Next: [02_Kernel_Capabilities_and_seccomp.md](./02_Kernel_Capabilities_and_seccomp.md)
---
