# 📌 Topic: Debugging Production Incidents

🟢 **Simple Explanation (Beginner)**
-----------------------------------
Imagine you are a **Detective**. 
A "Crime" has happened (The Website is down).
1. **Secure the Scene**: Stop the bleeding (Restart the container).
2. **Look for Clues**: Read the logs, check the "Inspect" data.
3. **Check the Witnesses**: Ask the neighbor containers if they saw anything (Network tests).
4. **Solve the Case**: Find the root cause (e.g., The database was full).

Debugging in production is about moving fast but staying calm.

🟡 **Practical Usage**
-----------------------------------
### The "First Responder" Checklist
1. `docker ps`: Is the container actually running?
2. `docker logs --tail 100`: What was the last thing it said?
3. `docker stats`: Is it using 100% CPU or 100% RAM?
4. `docker inspect`: Are the environment variables and network settings correct?

### Entering the Container (The "Flashlight")
```powershell
docker exec -it <container_id> sh
# Test if the DB is reachable from here
ping database
# Check if the process is running inside
ps aux
```

🔵 **Intermediate Understanding**
-----------------------------------
### Exit Codes (The Death Certificate)
Check `docker ps -a` to see why a container died.
- **0**: Clean exit (The app finished its work).
- **1**: General error (The app crashed).
- **137**: **OOM Killed** (The container used too much memory).
- **139**: Segmentation Fault (Memory corruption in C/C++/Go).
- **143**: SIGTERM (Someone stopped it nicely).

### Network Connectivity
If Container A can't talk to Container B:
1. Are they on the same **Network**? (`docker network inspect`)
2. Is the app in Container B **listening** on the right port? (`netstat -tulpn`)
3. Is there a **Firewall** (iptables) blocking it?

🔴 **Internals (Advanced)**
-----------------------------------
### Strace: Watching System Calls
If an app is "stuck" and doesn't print any logs, you can use `strace` to see what it's asking the kernel.
```bash
# Trace a running process inside a container
# (Requires --cap-add=SYS_PTRACE)
strace -p <PID_OF_APP>
```
If you see it repeating `read(0, ...)` forever, it's stuck waiting for input.

### Inspecting the Host (The "Outside" View)
Sometimes the problem is not the container, but the host.
- `df -h`: Is the host's disk full? (Common cause of Docker failures).
- `dmesg | grep -i docker`: Are there any kernel-level errors related to Docker?

⚫ **Staff-Level Insights**
-----------------------------------
### The "Snapshot" Debugging
In production, you don't want to spend 1 hour debugging a live container. 
**Staff Strategy**: 
1. **Commit** the broken container to a new image: `docker commit <broken_id> investigation-image`.
2. **Push** that image to a private registry.
3. **Pull** it to your local machine to investigate while the production server is already running a fresh, healthy container.

### Core Dumps
If a Go or C++ app crashes, it can leave a "Core Dump" file. This is a snapshot of the RAM at the moment of death. Staff engineers use `gdb` to read these files and find the exact line of code that caused the crash.

🏗️ **Mental Model**
Debugging is **Scientific Investigation**. Hypothesis -> Test -> Result.

⚡ **Actual Behavior**
Most production issues are caused by **Resources** (Disk full, RAM full) or **Configuration** (Wrong DB password), not actual bugs in the code.

🧠 **Resource Behavior**
- **Disk I/O Wait**: If your server is slow, check `iostat`. High "iowait" means your hard drive can't keep up with the logs/database.

💥 **Production Failures**
- **The "Zombie" App**: The process is running, but it's not responding. It's in a "Deadlock."
  - **Fix**: `docker kill <id>` (Forceful).
- **The "DNS Ghost"**: A container moved servers, but the other containers still have the old IP cached.
  - **Fix**: Restart the dependent containers.

🏢 **Best Practices**
- **Always have a healthcheck.**
- Use **Structured Logging** (JSON) so you can search for "ERROR" in your log aggregator.
- Keep your images small so that restarting a container takes 1 second, not 1 minute.

🧪 **Debugging Tools**
- `top / htop`: Host resource usage.
- `lsof -i :8080`: See who is using a port.
- `tcpdump`: Capture actual network packets.
- `nslookup / dig`: Test DNS.

💼 **Interview Q&A**
- **Q**: How do you know if a container was killed because of memory?
- **A**: The exit code will be 137.
- **Q**: What is the first thing you check when a container is "Down"?
- **A**: `docker ps -a` to check the status and `docker logs` to see the error message.

---
Prev: [35_Monitoring_Docker_Stats_Prometheus_Grafana.md](35_Monitoring_Docker_Stats_Prometheus_Grafana.md) | Index: [00_Index.md](../00_Index.md) | Next: [../Scaling/37_Horizontal_Scaling_Strategies.md](../Scaling/37_Horizontal_Scaling_Strategies.md)
---
