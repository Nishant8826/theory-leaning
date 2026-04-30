# 📌 Topic: Exec, Logs, and Inspecting State

🟢 **Simple Explanation (Beginner)**
-----------------------------------
Imagine a container is a **Locked Room**.
1. **Logs**: Looking through the **Window**. You can see what's happening and hear what the people inside are saying, but you can't touch anything.
2. **Exec**: Opening the door and **Walking In**. You can move things around, fix the furniture, and talk to people directly.
3. **Inspect**: Reading the **Blueprints**. You see how big the room is, what the IP address is, and where the vents are.

🟡 **Practical Usage**
-----------------------------------
### 1. `docker logs` (The Window)
```powershell
# See everything the app has printed so far
docker logs <container_id>

# Follow the logs in real-time (Live)
docker logs -f <container_id>

# See the last 20 lines only
docker logs --tail 20 <container_id>
```

### 2. `docker exec` (The Door)
```powershell
# Run a single command inside a running container
docker exec <container_id> ls /app

# Get a full interactive shell inside
docker exec -it <container_id> bash
```

### 3. `docker inspect` (The Blueprints)
```powershell
# Get a massive JSON with all settings
docker inspect <container_id>

# Extract just the IP address (using formatting)
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <container_id>
```

🔵 **Intermediate Understanding**
-----------------------------------
### Where do logs go?
By default, Docker captures everything the app prints to `STDOUT` (Standard Output) and `STDERR` (Standard Error) and saves it to a **JSON file** on the host.

### The Lifecycle of `exec`
Commands run with `exec` only live as long as the command itself. If you `exec bash`, the session ends when you type `exit`. It does **not** restart the container or affect the main app.

🔴 **Internals (Advanced)**
-----------------------------------
### Log Drivers
Docker can be configured to send logs to different places:
- `json-file` (Default)
- `syslog` (Linux system log)
- `awslogs` (CloudWatch)
- `fluentd` (Log aggregator)

### How `exec` works in the Kernel
When you run `docker exec`:
1. The Docker Daemon tells the Kernel to start a new process.
2. The Kernel "joins" that new process to the **same Namespaces** (Network, PID, Mount) as the running container.
3. It feels like you are "inside," but you are just a process sharing the same "blinders."

⚫ **Staff-Level Insights**
-----------------------------------
### Logging Bottlenecks
Writing huge amounts of logs to `json-file` can slow down your app because of **Disk I/O**.
**Staff Solution**: Configure **Log Rotation** in `daemon.json` so you don't fill up the disk:
```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

### Inspecting "Dead" Containers
Even if a container has crashed (`Exited`), you can still `inspect` it and see its `logs`. This is the only way to find out *why* it died.

🏗️ **Mental Model**
- `logs` = Read-only history.
- `exec` = Real-time interaction.
- `inspect` = Metadata/Configuration.

⚡ **Actual Behavior**
`docker logs` doesn't talk to the container; it reads a file on your hard drive. 
`docker exec` talks to the Docker Engine, which talks to `containerd`.

🧠 **Resource Behavior**
- **Exec**: Each `exec` session creates a new process on the host, consuming a small amount of RAM.
- **Logs**: Reading logs consumes Disk I/O.

💥 **Production Failures**
- **"Log File Too Large"**: A container runs for a year, the log file becomes 50GB, and the server crashes.
- **"No Shell Available"**: You try to `exec -it ... bash` but it fails because the image was built with `alpine` (which uses `sh`) or `distroless` (which has NO shell).

🏢 **Best Practices**
- Always log to `STDOUT/STDERR` in your app code. Do NOT log to a file inside the container.
- Use `docker stats` alongside `inspect` to see real-time resource usage.

🧪 **Debugging**
```bash
# Debugging a networking issue:
docker inspect <id> | grep IPAddress

# See the last 5 minutes of logs
docker logs --since 5m <id>
```

💼 **Interview Q&A**
- **Q**: Where does Docker store container logs by default?
- **A**: In JSON files on the host, usually under `/var/lib/docker/containers/<id>/<id>-json.log`.
- **Q**: Can you `exec` into a stopped container?
- **A**: No. The container must be running to join its namespaces.

---
Prev: [12_Interactive_vs_Detached_Modes.md](12_Interactive_vs_Detached_Modes.md) | Index: [00_Index.md](../00_Index.md) | Next: [14_Resource_Limits_CPU_and_Memory.md](14_Resource_Limits_CPU_and_Memory.md)
---
