# Working with Docker: Core CLI Commands

---

### What
The Docker Command Line Interface (CLI) is how you interact with the Docker Engine. It's the daily tool developers use to fetch code, launch servers, read logs, and step inside containers to fix bugs that are happening in real-time.

---

### Why
Visual UI tools (like Docker Desktop GUI) are fine for beginners, but when an app crashes on an AWS Production Linux server at 3:00 AM, you won't have a visual UI. You must be deeply comfortable with the terminal commands to troubleshoot and control containers natively.

---

### How
The CLI verbs generally follow the pattern: `docker [object] [action]` (e.g., `docker container stop`). However, Docker provides shorter aliases for the most common commands (e.g., `docker stop`).

---

### Implementation

Here is your daily toolkit of commands organized by use-case.

```bash
# --- 1. RUNNING & MANAGING ---

# Run a container from an image. 
# -d (detached, runs in background) 
# -p (publish port HostPort:ContainerPort)
# --name (give it a human friendly name)
docker run -d -p 3000:8080 --name backend_api my_node_image

# List all ACTIVE containers running right now
docker ps

# List ALL containers (even stopped/crashed ones)
docker ps -a

# Stop an active container gracefully
docker stop backend_api

# Start it back up
docker start backend_api


# --- 2. DEBUGGING & LOGS ---

# See the console.log() outputs of a detached background container
docker logs backend_api

# "Follow" the logs in real time (like tail -f)
docker logs -f backend_api

# "EXEC" (Execute): Step INSIDE a running container to explore its files!
# -it means Interactive Terminal. /bin/sh is the shell environment inside the box.
docker exec -it backend_api /bin/sh
# (You are now inside the Linux container. Type 'ls' to see your code!)
# Type 'exit' to escape back to your Windows/Mac terminal.


# --- 3. CLEANING UP (Danger Zone) ---

# Delete a stopped container permanently
docker rm backend_api

# Delete a container that is currently running (Force)
docker rm -f backend_api

# Delete a downloaded blueprint Image
docker rmi my_node_image

# The "Nuclear Option": Deletes ALL stopped containers, unused networks, and dangling images.
# Great for freeing up gigabytes of disk space safely.
docker system prune -a
```

---

### Steps
1. Start an Nginx server in the background: `docker run -d -p 8080:80 --name test_site nginx`
2. Open your browser to `http://localhost:8080`.
3. Check the logs: `docker logs test_site`. You will see your browser's HTTP request recorded there.
4. Stop and delete it so it stops eating RAM: `docker rm -f test_site`.

---

### Integration

* **React/Next.js/Node.js:** If your backend acts strangely and returning HTTP 500s, you use `docker logs [container]` to read the exact Node.js stack trace error.
* **Full-stack apps:** If Next.js complains it "Cannot connect to Database", you can `docker exec -it my_next_app /bin/sh` and try pinging the database internally. This isolates whether it's a code issue or a Docker internal networking issue.

---

### Impact
Mastering `docker logs`, `docker ps`, and `docker exec` turns debugging from a guesswork nightmare into a surgical, 60-second fix.

---

### Interview Questions
1. **How do you gain terminal access to a running container?**
   *Answer: By using the `docker exec -it <container_name> /bin/bash` (or /bin/sh) command.*
2. **What does the `-p 8080:3000` flag actually do?**
   *Answer: It Maps/Forwards traffic hitting Port 8080 on the physical Host Machine directly into Port 3000 inside the isolated container.*
3. **If your server's disk space is 100% full due to Docker, what command fixes this?**
   *Answer: `docker system prune -a` removes all stopped containers, unused volumes, and dangling/unused images, safely freeing up gigabytes of space.*

---

### Summary
* `run -d` starts containers quietly in the background.
* `ps` shows what is running; `ps -a` shows what crashed.
* `logs` helps find bugs.
* `exec -it` lets you teleport inside the container to debug directly.
* `system prune` is your best friend for disk cleanup.

---
Prev : [04_volumes_and_bind_mounts.md](./04_volumes_and_bind_mounts.md) | Next : [06_writing_dockerfiles.md](./06_writing_dockerfiles.md)
