# 📌 Topic: Container Forensics and Recovery

🟢 **Simple Explanation (Beginner)**
-----------------------------------
Imagine a **Crime Scene**. 
- A container has crashed or was hacked. 
- You need to find out **exactly what happened** inside, even if the container is gone.

**Container Forensics** is like being a digital CSI. You look at the "fingerprints" (logs), the "corpse" (crashed container state), and the "blood spatters" (modified files) to reconstruct the story of the disaster.

🟡 **Practical Usage**
-----------------------------------
### 1. Extracting Files from a "Dead" Container
If a container won't start, you can't `exec` into it. 
**The Solution**: Use `docker cp`.
```powershell
# Copy the config file out of a crashed container to investigate
docker cp <crashed_id>:/app/config.json ./config_dump.json
```

### 2. Seeing every file change
```powershell
# See everything the app changed on the filesystem since it started
docker diff <container_id>
```
- `A`: Added file.
- `C`: Changed file.
- `D`: Deleted file.

### 3. Turning a container into an Image
If you want to study a "hacked" container safely on your laptop:
```powershell
docker commit <hacked_id> hacker-investigation:v1
docker save hacker-investigation:v1 > forensic_image.tar
```

🔵 **Intermediate Understanding**
-----------------------------------
### Export vs. Save
- **`docker save`**: Saves the **Image** (including all its history and layers). Best for moving images between servers.
- **`docker export`**: Saves the **Running Container's Filesystem** (it flattens all layers into one). Best for creating a "snapshot" of a specific container's files.

### Inspecting the Writable Layer
Every change a container makes is stored in a specific folder on the host (The "UpperDir").
A forensic engineer can look at this folder directly to see deleted files or hidden scripts.

🔴 **Internals (Advanced)**
-----------------------------------
### Checkpoint and Restore (CRIU)
Did you know you can "Freeze" a container and "Unfreeze" it on a different server?
This uses **CRIU** (Checkpoint/Restore in Userspace). 
1. It dumps the entire **RAM** of the app to a file.
2. You move the file to a new server.
3. The app resumes exactly where it was, with all its variables and connections intact.
*Note: This is still an experimental feature in Docker.*

### The Audit Log
On Linux, the `auditd` system can record every time a container tries to access a sensitive file (like `/etc/shadow`). Even if the hacker deletes the logs *inside* the container, the host's audit log will have the record.

⚫ **Staff-Level Insights**
-----------------------------------
### Post-Mortem Analysis
When a production incident happens, a Staff Engineer doesn't just fix it; they write a **Post-Mortem**.
- They use **`docker inspect`** to see exactly when the OOM killer struck.
- They use **`docker logs --since`** to correlate the crash with other events in the system.
- They check the **Host Kernel logs** (`dmesg`) for hardware or kernel failures.

### The "Immutable" Proof
In a legal investigation, you must prove the data wasn't tampered with.
**Staff Strategy**: Calculate the **SHA256 hash** of the forensic `.tar` file and record it in a secure log immediately after capture.

🏗️ **Mental Model**
Container Forensics is **Digital Autopsy**.

⚡ **Actual Behavior**
Most data is stored in the **OverlayFS layers**. Even if a hacker runs `rm -rf /`, the original image files are still safe in the "Lower" layers.

🧠 **Resource Behavior**
- **Disk**: Saving/Exporting a container uses a lot of disk space (as big as the container's files).

💥 **Production Failures**
- **The "Overwritten Clues"**: You restarted the container with `--rm`. The old container was deleted instantly, and all the "clues" (files in the writable layer) are gone forever.
  - **Staff Rule**: Never use `--rm` for critical production services.
- **The "Full RAM" Dump**: Trying to checkpoint a container with 32GB of RAM will freeze the server while it writes 32GB to the disk.

🏢 **Best Practices**
- Always use **External Logging** so you don't lose logs when the container dies.
- Use **Read-Only** filesystems (Chapter 29) to make forensics easier (any file in `docker diff` is suspicious!).
- Keep a "Forensic Toolbox" image ready with tools like `tcpdump`, `strace`, and `lsof`.

🧪 **Debugging**
```bash
# Export a container to see its full filesystem
docker export <id> -o container_fs.tar
tar -tvf container_fs.tar | head -n 20
```

💼 **Interview Q&A**
- **Q**: How do you see which files have been modified inside a container?
- **A**: Using the `docker diff` command.
- **Q**: What is the difference between `docker save` and `docker export`?
- **A**: `save` preserves image layers and history; `export` takes a snapshot of the container's current state and flattens it into a single layer.

---
Prev: [51_Docker_Plugins_and_Contexts.md](../Ops/51_Docker_Plugins_and_Contexts.md) | Index: [00_Index.md](../00_Index.md) | Next: DONE
---
