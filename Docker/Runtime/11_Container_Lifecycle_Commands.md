# 📌 Topic: Container Lifecycle Commands

🟢 **Simple Explanation (Beginner)**
-----------------------------------
A container has a **Life Story**.
1. **Born (Create)**: The container is created from an image but hasn't started yet.
2. **Growing (Start/Run)**: The app inside is running and doing work.
3. **Sleeping (Pause)**: The app stops moving, but it remembers everything.
4. **Napping (Stop)**: The app is closed, but the container "box" still exists.
5. **Death (Remove)**: The box is thrown away. All data inside is gone.

In Docker, we use specific commands to move through this story.

🟡 **Practical Usage**
-----------------------------------
### The Big 4 Commands
1. `docker run`: Create + Start (The most common).
2. `docker stop`: Ask nicely to shut down.
3. `docker start`: Wake up a stopped container.
4. `docker rm`: Delete the container.

**Example Flow:**
```powershell
# 1. Start a container
docker run --name my-web -d nginx

# 2. Stop it
docker stop my-web

# 3. See that it still exists (but is exited)
docker ps -a

# 4. Remove it
docker rm my-web
```

### Useful Flags
- `-d`: Detached mode (runs in the background).
- `--name`: Give it a friendly name instead of a random one like `agitated_hopper`.
- `--rm`: Automatically delete the container when it stops (Great for one-off tasks!).

🔵 **Intermediate Understanding**
-----------------------------------
### Pause vs. Stop
- **Pause**: Freezes the process using the **CPU Scheduler**. The memory (RAM) is still occupied. The app doesn't know it was paused.
- **Stop**: Sends a `SIGTERM` signal to the app. The app can save its work and close gracefully. The RAM is released.

### The Init Process (PID 1)
Inside every container, the first process started is **PID 1**. 
- If PID 1 dies, the container dies.
- PID 1 is responsible for cleaning up "zombie" child processes.

🔴 **Internals (Advanced)**
-----------------------------------
### Signals: SIGTERM vs SIGKILL
When you run `docker stop`:
1. Docker sends `SIGTERM` (Signal 15) to PID 1.
2. Docker waits for a **Grace Period** (default 10 seconds).
3. If the app is still running, Docker sends `SIGKILL` (Signal 9), which forces the kernel to kill it instantly.

### Container State Machine
```text
[ Image ] --(run)--> [ Running ] --(pause)--> [ Paused ]
     ^                  |      <--(unpause)--     |
     |                (stop)                      |
     |                  v                         |
     |----(rm)---- [ Exited ] <-------------------|
```

⚫ **Staff-Level Insights**
-----------------------------------
### Handling "Graceful Shutdown"
In production, you don't want to lose active user requests. 
**Staff Rule**: Ensure your Node.js/Go app catches `SIGTERM` and finishes processing current requests before exiting.

**Node.js Example:**
```javascript
process.on('SIGTERM', () => {
  server.close(() => {
    console.log('Processed all requests. Closing now.');
    process.exit(0);
  });
});
```

### The "PID 1" Problem
Many apps aren't designed to be PID 1. They don't handle signals correctly.
**Staff Fix**: Use `tini`. It's a tiny init binary that handles signals and passes them to your app.
```dockerfile
# Add Tini
RUN apk add --no-cache tini
ENTRYPOINT ["/sbin/tini", "--"]
CMD ["node", "app.js"]
```

🏗️ **Mental Model**
A container is a **Controlled Process**.

⚡ **Actual Behavior**
`docker run` is actually `docker create` + `docker start`.

🧠 **Resource Behavior**
- **Stopped Containers**: They take up **Disk Space** (because of the read-write layer) but **Zero CPU/RAM**.

💥 **Production Failures**
- **"Container is already in use"**: You try to `docker run --name my-app` but it fails because an old, stopped container with that name still exists.
  - **Fix**: `docker rm -f my-app` or use `--rm`.
- **The "Infinite Restart" Loop**: Your app crashes immediately on start. Docker (if configured with `--restart always`) will keep trying to start it, eating up your logs and CPU.

🏢 **Best Practices**
- Always name your containers.
- Use `--rm` for temporary debugging containers.
- Set a custom stop timeout for heavy apps: `docker stop -t 30 my-heavy-db`.

🧪 **Debugging**
```bash
# See why a container exited (Check Exit Code)
docker ps -a

# Exit Code 137: Means it was SIGKILLed (usually OOM - Out of Memory)
# Exit Code 0: Clean exit
# Exit Code 1: App crash
```

💼 **Interview Q&A**
- **Q**: What happens when you run `docker stop`?
- **A**: Docker sends a `SIGTERM`, waits 10 seconds, then sends a `SIGKILL`.
- **Q**: How do you keep a container running forever?
- **A**: It must have a foreground process. If the main process finishes, the container stops.

---
Prev: [../Images/10_Multi_Arch_Images_Buildx.md](../Images/10_Multi_Arch_Images_Buildx.md) | Index: [00_Index.md](../00_Index.md) | Next: [12_Interactive_vs_Detached_Modes.md](12_Interactive_vs_Detached_Modes.md)
---
