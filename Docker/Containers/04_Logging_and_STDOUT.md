# 📌 Topic: Logging and STDOUT (The JSON Driver)

## 🧠 Concept Explanation (Basic → Expert)
**Basic**: Docker captures everything your app prints to the screen (STDOUT/STDERR) and saves it so you can see it with `docker logs`.
**Expert**: Docker uses **Logging Drivers** to manage container output. The default is the **json-file driver**, which stores logs in local files on the host. For a senior engineer, logging is a **Performance and Stability concern**. If not configured correctly, logs can grow indefinitely, exhausting host disk space. Furthermore, the "Blocking" nature of standard I/O can slow down your application if the logging driver cannot keep up with the volume of messages.

## 🏗️ Mental Model
- **The Tape Recorder**: Every word your app says is recorded on a tape (Log file). If you don't set a limit, the tape will eventually fill up the entire room (The Hard Drive).

## ⚡ Actual Behavior
- **Non-persistent**: If you `docker rm` a container, its logs are deleted forever.
- **Blocking I/O**: If your app prints 1 million lines a second and the disk is slow, the app's `console.log` or `print` statements will actually wait for the disk to catch up, slowing down your business logic.

## 🔬 Internal Mechanics (The Log Pipeline)
1. App writes to `/proc/self/fd/1` (STDOUT).
2. The `containerd-shim` captures this data.
3. The Docker Daemon receives it and passes it to the configured **Logging Driver**.
4. The `json-file` driver appends the message (wrapped in JSON metadata) to a file in `/var/lib/docker/containers/<id>/<id>-json.log`.

## 🔁 Execution Flow
1. App: `console.log("Hello")`.
2. Kernel: Writes to pipe.
3. Docker: Reads pipe -> Wraps in JSON -> Writes to disk.
4. User: `docker logs` -> Docker reads the file and returns it.

## 🧠 Resource Behavior
- **Disk Space**: Without rotation, a noisy app can generate 100GB of logs in a day, crashing the entire host server.
- **CPU**: Parsing and writing JSON for every log line consumes daemon CPU cycles.

## 📐 ASCII Diagrams (REQUIRED)

```text
       DOCKER LOGGING PIPELINE
       
[ App Process ]
      |
 (STDOUT/ERR)
      v
[ containerd-shim ]
      |
[ Docker Daemon ] --(Logging Driver)--> [ /var/log/myapp.log ]
      |                                        |
      +----( json-file )-----------------------+
      |
      +----( awslogs / syslog / fluentd )----> [ Remote Service ]
```

## 🔍 Code (Configuring Log Rotation)
```json
// /etc/docker/daemon.json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```
*Effect: Each container keeps at most 3 log files of 10MB each. Older logs are deleted automatically.*

## 💥 Production Failures
- **The "Silent Disk Death"**: A debug flag is left on in production. A container generates 1GB of logs every hour. The host has 20GB free. On Sunday at 4 AM, the host disk hits 100%. SSH fails, Docker crashes, and the entire production environment goes dark.
- **Logging Latency**: A high-performance Java app is slow. Profiling shows it's spending 30% of its time waiting for `System.out.println`. 
  *Fix*: Use an asynchronous logging framework or use the `non-blocking` mode in the Docker logging driver.

## 🧪 Real-time Q&A
**Q: Should I log to a file inside the container?**
**A**: **NO.** Never. Logging to a file inside the container makes the logs hard to access, they disappear when the container is replaced, and they consume the container's writable layer space. Always log to **STDOUT/STDERR** and let Docker handle the transport.

## ⚠️ Edge Cases
- **Broken Pipes**: If the logging daemon (like Fluentd) crashes, and Docker is in "Blocking" mode, all your containers might freeze because they can't write their logs.

## 🏢 Best Practices
- **Use JSON Driver for Local**: But always with `max-size` and `max-file`.
- **Ship to Centralized Log Management**: In production (AWS), use the `awslogs` driver to send logs directly to CloudWatch.
- **Non-Blocking Mode**: For high-volume apps, use `"mode": "non-blocking"` to prevent logging from slowing down your app.

## ⚖️ Trade-offs
| Mode | Benefit | Risk |
| :--- | :--- | :--- |
| **Blocking (Default)**| Guaranteed Logs | App Performance hit |
| **Non-Blocking** | High Performance | Log messages might be dropped |

## 💼 Interview Q&A
**Q: How do you prevent Docker logs from consuming all disk space on a host?**
**A**: I configure **Log Rotation** in the Docker `daemon.json` file. By setting the `log-driver` to `json-file` and using `log-opts` such as `max-size` (e.g., 10m) and `max-file` (e.g., 3), I ensure that Docker only keeps a fixed amount of log data per container. Once the limit is reached, Docker automatically deletes the oldest log file when a new one is created.

## 🧩 Practice Problems
1. Create a "noisy" container that prints a number every millisecond. Watch the log file grow in `/var/lib/docker/containers/...`.
2. Apply log rotation in `daemon.json` and verify that only 3 files are kept.
3. Compare the application speed with and without `non-blocking` mode.

---
Prev: [03_Resource_Limits.md](./03_Resource_Limits.md) | Index: [00_Index.md](../00_Index.md) | Next: [05_Debugging_Containers.md](./05_Debugging_Containers.md)
---
