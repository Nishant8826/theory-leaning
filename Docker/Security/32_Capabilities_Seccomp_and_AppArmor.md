# 📌 Topic: Capabilities, Seccomp, and AppArmor

🟢 **Simple Explanation (Beginner)**
-----------------------------------
Imagine you are a **Security Guard** at a high-tech building.
- **Capabilities**: Instead of giving someone the "Master Key" (Root), you give them a **Specific Keycard** that only opens the "Server Room" (Network settings) or the "Janitor Closet" (File permissions).
- **Seccomp**: You give them a **Restricted Radio**. They are only allowed to say 10 specific words. If they try to say "Open the safe," the radio shuts off.
- **AppArmor**: You give them a **Map**. They are allowed to walk in the hallway, but if they try to step into an office they aren't assigned to, an alarm goes off.

These three tools work together to make sure that even if a container is "Root," it can only do what it absolutely needs to do.

🟡 **Practical Usage**
-----------------------------------
### 1. Capabilities (Granting specific powers)
By default, Docker removes most "Root" powers. You can add or remove them manually.
```powershell
# Allow a container to change its own clock (usually not allowed!)
docker run --cap-add=SYS_TIME alpine date -s "12:00"

# Remove the ability to change file owners (even for root!)
docker run --cap-drop=CHOWN alpine chown node /etc/shadow
```

### 2. Seccomp (Restricting System Calls)
A standard container is allowed to make about 300 different requests (syscalls) to the kernel. You can provide a "Profile" to limit this.
```bash
docker run --security-opt seccomp=my-profile.json nginx
```

### 3. AppArmor (Restricting Files/Resources)
Docker comes with a default profile called `docker-default`. It prevents containers from doing dangerous things like mounting new hard drives.

🔵 **Intermediate Understanding**
-----------------------------------
### Linux Capabilities
Linux broke the "All-powerful Root" into ~40 smaller pieces called **Capabilities**.
- `CAP_NET_BIND_SERVICE`: Allow binding to ports < 1024.
- `CAP_SYS_ADMIN`: The "God mode" capability (Avoid this!).
- `CAP_CHOWN`: Change file ownership.

### Seccomp (Secure Computing Mode)
Seccomp acts as a **Firewall for Syscalls**. If a hacker manages to run code inside your container, they might try to call `ptrace` to take over another process. A good Seccomp profile will block `ptrace` entirely.

🔴 **Internals (Advanced)**
-----------------------------------
### BPF (Berkeley Packet Filter)
Seccomp uses **BPF** under the hood. When your app makes a syscall, the kernel runs a tiny BPF program that checks: "Is this syscall on the allowed list?" If no, the process is killed instantly.

### AppArmor vs. SELinux
- **AppArmor** (Ubuntu/Debian): Is "Path-based." You say: "This process cannot read `/etc/shadow`."
- **SELinux** (RedHat/CentOS): Is "Label-based." Every file and process has a label (e.g., `httpd_t`). You say: "Labels of type A cannot talk to labels of type B." (Much more powerful, but much harder to learn).

⚫ **Staff-Level Insights**
-----------------------------------
### Creating a Custom Seccomp Profile
Don't write a profile from scratch. 
**Staff Strategy**: Use a tool like **`strace`** to record every syscall your app actually uses during a test run, then create a profile that allows *only* those syscalls. This is called "Zero Trust Execution."

### The Danger of `--privileged`
When you run `--privileged`, Docker:
1. Adds **ALL** capabilities.
2. Disables **Seccomp**.
3. Disables **AppArmor**.
**Staff Rule**: Never use `--privileged` in production. If you need it, find the specific capability you are missing and use `--cap-add` instead.

🏗️ **Mental Model**
- **Capabilities**: **Privileges** (What I can do).
- **Seccomp**: **Language** (What I can say).
- **AppArmor**: **Territory** (Where I can go).

⚡ **Actual Behavior**
These are kernel-level features. If a container tries to violate a rule, the **Kernel** blocks the operation and logs an audit error in `/var/log/audit/audit.log`.

🧠 **Resource Behavior**
- **Performance**: Seccomp adds a few nanoseconds to every syscall. In high-performance apps, this can add up to 1-2% CPU overhead.

💥 **Production Failures**
- **"Operation Not Permitted"**: Your app tries to start but fails. You are root, the file is there, why can't it work? 
  - **Reason**: You are missing a **Capability** (like `CAP_NET_RAW` for pinging).
- **Silent App Crashes**: A Seccomp profile blocks a syscall your app only uses once a day (e.g., for log rotation). The app crashes randomly at midnight.

🏢 **Best Practices**
- Always **Drop All** capabilities and then add back only what you need.
  `docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE ...`
- Use the default Docker Seccomp profile unless you have a reason not to.

🧪 **Debugging**
```bash
# See which capabilities a process has
getpcaps <pid>

# Check if AppArmor is active for a container
docker inspect <id> --format '{{.AppArmorProfile}}'
```

💼 **Interview Q&A**
- **Q**: What does `--cap-drop=ALL` do?
- **A**: It removes all special Linux privileges from the root user inside the container, making it much more secure.
- **Q**: What is the difference between Seccomp and AppArmor?
- **A**: Seccomp restricts system calls (actions); AppArmor restricts access to system resources like files and networks (locations).

---
Prev: [31_Image_Scanning_and_Vulnerability_Management.md](31_Image_Scanning_and_Vulnerability_Management.md) | Index: [00_Index.md](../00_Index.md) | Next: [../Ops/33_Docker_in_Jenkins_Pipelines.md](../Ops/33_Docker_in_Jenkins_Pipelines.md)
---
