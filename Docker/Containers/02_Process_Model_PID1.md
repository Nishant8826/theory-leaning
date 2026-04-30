# 📌 Topic: Process Model (PID 1 and Tini)

## 🧠 Concept Explanation (Basic → Expert)
**Basic**: The first process started in a container is called "PID 1". If this process dies, the whole container dies.
**Expert**: In Linux, **PID 1** (the init process) has two unique responsibilities: **Signal Forwarding** and **Zombie Reaping**. Most application runtimes (Node.js, Python, Java) are NOT designed to be init processes. They often ignore signals like `SIGTERM` or fail to adopt "orphaned" child processes, leading to system resource leaks. Staff-level engineering requires using an "Init-lite" like **Tini** or the `--init` flag to ensure the container behaves like a proper Linux system.

## 🏗️ Mental Model
- **The Captain (PID 1)**: The captain is responsible for the ship. If a sailor (child process) dies, the captain must record it. If a message (Signal) comes from the shore, the captain must tell the crew. If the captain leaves the ship, the ship sinks.
- **Tini**: A professional captain who knows how to manage a crew.
- **Node.js**: A great cook who was suddenly made captain. They know how to cook (run your app), but they don't know how to handle messages from the shore or what to do with dead sailors.

## ⚡ Actual Behavior
- **Signal Ignoring**: If you run `node app.js` as PID 1, and you `docker stop`, Node might ignore the `SIGTERM`. Docker then waits 10 seconds and `SIGKILL`s it.
- **Zombie Accumulation**: If your app spawns a subprocess (like `ffmpeg`) and that subprocess crashes, it becomes a "Zombie." A normal PID 1 would "reap" it. Node.js won't, and eventually, the host runs out of PIDs.

## 🔬 Internal Mechanics (The Init Responsibilities)
1. **Signal Proxying**: When the kernel sends a signal to a process group, it usually hits PID 1. PID 1 is expected to pass that signal to its children.
2. **Orphan Adoption**: When a process dies, its parent must "wait" on it to collect its exit code. If the parent dies first, the process is "orphaned" and adopted by PID 1. PID 1 must then "wait" on it.

## 🔁 Execution Flow
1. Docker starts the container.
2. **With Tini**: Tini starts as PID 1. It forks and execs your App as PID 2.
3. `SIGTERM` arrives at Tini (PID 1).
4. Tini forwards `SIGTERM` to the App (PID 2).
5. App shuts down.
6. Tini exits, and the container closes gracefully.

## 🧠 Resource Behavior
- **PID Space**: Without reaping, zombies consume slots in the kernel's process table. This can lead to a "Fork failure" on the entire host.

## 📐 ASCII Diagrams (REQUIRED)

```text
       WITHOUT INIT                    WITH INIT (TINI)
+-----------------------+       +-----------------------+
|  Container            |       |  Container            |
|  [ PID 1: Node.js ]   |       |  [ PID 1: Tini ]      |
|          |            |       |          |            |
|  (Ignores SIGTERM)    |       |  [ PID 2: Node.js ]   |
|  (Ignores Zombies)    |       |          |            |
+-----------------------+       |  (Forwards Signals)   |
                                |  (Reaps Zombies)      |
                                +-----------------------+
```

## 🔍 Code (Using Tini)
```dockerfile
# Option A: In the Dockerfile
RUN apk add --no-cache tini
ENTRYPOINT ["/sbin/tini", "--"]
CMD ["node", "app.js"]

# Option B: At Runtime (Docker 1.13+)
# docker run --init my-image
```

## 💥 Production Failures
- **The "Graceful Shutdown" Failure**: A database migration is running inside a container. You deploy a new version. `docker stop` sends `SIGTERM`. The app ignores it. 10 seconds later, `SIGKILL` hits. The migration is half-finished, the database is corrupted.
  *Fix*: Use an init process.
- **The "Zombie" Memory Leak**: A containerized cron job spawns shell scripts every minute. The scripts finish but stay as zombies. After 3 days, the host server crashes because it can't spawn any more processes.

## 🧪 Real-time Q&A
**Q: Do I need Tini if I use a shell script as my ENTRYPOINT?**
**A**: If you use `ENTRYPOINT ["/bin/sh", "run.sh"]`, the shell becomes PID 1. Standard shells like `sh` and `bash` do reap zombies but they **do not** forward signals to children unless you use `exec`. Always use `exec ./my-app` at the end of your shell scripts.

## ⚠️ Edge Cases
- **Shell vs Exec form**: 
  - `CMD node app.js` (Shell form): Runs as `/bin/sh -c "node app.js"`. The shell is PID 1.
  - `CMD ["node", "app.js"]` (Exec form): Runs `node app.js` directly as PID 1. **Always use Exec form.**

## 🏢 Best Practices
- **Always use an Init process**: Either `--init` at runtime or `tini` in the image.
- **Handle SIGTERM**: Even with Tini, your app must still listen for the signal to shut down gracefully.
- **Avoid Shell Wrappers**: If you must use a wrapper script, end it with `exec "$@"`.

## ⚖️ Trade-offs
| Init Method | Pros | Cons |
| :--- | :--- | :--- |
| **None** | Zero overhead | Zombie/Signal issues |
| **--init flag** | Easy, no image change | Requires runtime support |
| **Tini in Image** | Works everywhere | Adds 20KB to image |

## 💼 Interview Q&A
**Q: Why shouldn't you run a Node.js or Python application as PID 1 in a Docker container?**
**A**: Because these runtimes are not designed to act as init systems. They typically do not handle signal forwarding (meaning they might ignore `SIGTERM` from Docker) and they do not perform zombie process reaping. This can lead to containers that won't stop gracefully and hosts that run out of process IDs due to accumulated zombie processes. The solution is to use a dedicated init tool like `Tini`.

## 🧩 Practice Problems
1. Build a Node image without an init. Run it, try to `docker stop` it, and count how many seconds it takes.
2. Add `tini` or use `--init` and repeat. Observe the immediate shutdown.
3. Use a script to create a zombie process inside a container and verify if it gets reaped with and without Tini.

---
Prev: [01_Container_Lifecycle.md](./01_Container_Lifecycle.md) | Index: [00_Index.md](../00_Index.md) | Next: [03_Resource_Limits.md](./03_Resource_Limits.md)
---
