# 📌 Topic: Union Filesystem (OverlayFS)

## 🧠 Concept Explanation (Basic → Expert)
**Basic**: Imagine a stack of transparent glass plates. You draw something on the bottom plate, something else on the middle plate, and something else on the top plate. When you look from the top, you see the combined image. That's how Docker layers work.
**Expert**: Docker uses **Union Mounts** (specifically **OverlayFS** in modern versions) to create a single, unified view of multiple directories. This is what allows Docker to have "Layers." Each instruction in a Dockerfile creates a read-only layer. When a container runs, Docker adds a thin, writable "Container Layer" on top. This ensures that the original image is never modified and that multiple containers can share the same base image layers efficiently using **Copy-on-Write (CoW)** mechanics.

## 🏗️ Mental Model
- **Image Layers (Read-Only)**: The pages of a book. You can read them, but you can't change the printed text.
- **Container Layer (Read-Write)**: A piece of tracing paper placed over a page. You can write your own notes on the tracing paper. To anyone looking, your notes appear to be on the page, but the book remains pristine.

## ⚡ Actual Behavior
- **Adding a file**: When you create a new file, it is written only to the top "Writable" layer.
- **Deleting a file**: When you "delete" an image file in a container, Docker creates a **whiteout** file in the writable layer that hides the file in the lower layer. The original file still exists on disk in the image layer!
- **Modifying a file**: Docker uses **Copy-on-Write**. It copies the file from the read-only layer to the writable layer first, then modifies it there.

## 🔬 Internal Mechanics (OverlayFS)
OverlayFS uses three main directories:
1. **LowerDir**: The read-only image layers.
2. **UpperDir**: The writable container layer (where changes go).
3. **Merged**: The unified view that you see inside the container.
4. **WorkDir**: An internal directory used by the kernel to manage atomic transitions.

## 🔁 Execution Flow (Modifying `/etc/hosts`)
1. App requests to write to `/etc/hosts`.
2. Kernel checks if `/etc/hosts` exists in `UpperDir`.
3. If not, kernel looks in `LowerDir`.
4. Kernel finds it in `LowerDir`, copies it to `UpperDir` (Copy-on-Write).
5. The write operation is performed on the copy in `UpperDir`.

## 🧠 Resource Behavior
- **Disk Space Efficiency**: 100 containers running the same 1GB image only consume 1GB of disk space + the tiny amount of unique data in their writable layers.
- **Performance Overhead**: The first time you write to a large file in a lower layer, there is a latency spike as the kernel must perform the physical copy operation (CoW).

## 📐 ASCII Diagrams (REQUIRED)

```text
       OVERLAYFS LAYER STACK
       
[ Merged View (What you see) ]
      ^
      |
+--------------------------+
|  Writable Layer (Upper)  |  <-- Your changes
+--------------------------+
|  Image Layer 3 (Lower)   |  <-- /app/dist
+--------------------------+
|  Image Layer 2 (Lower)   |  <-- node_modules
+--------------------------+
|  Image Layer 1 (Lower)   |  <-- OS (Alpine)
+--------------------------+
```

## 🔍 Code (Inspecting Mounts)
```bash
# Find the OverlayFS mount points for a container
docker inspect <container_id> --format '{{.GraphDriver.Data}}'

# View the directories on the host
# You will see LowerDir, UpperDir, and Merged paths in /var/lib/docker/overlay2/...
```

## 💥 Production Failures
- **The "Large File Copy-on-Write" Hang**: A developer modifies a 2GB database file inside a container layer. The container freezes for 30 seconds as the kernel copies that 2GB file from the read-only layer to the writable layer.
  *Fix*: Use **Volumes** for large, high-churn data.
- **Disk Exhaustion via Whiteouts**: Deleting files in a Dockerfile `RUN` command doesn't actually free space in the image; it just adds a whiteout. 
  *Fix*: Clean up temp files in the same `RUN` command (`apt-get install ... && rm -rf ...`).

## 🧪 Real-time Q&A
**Q: If I run 1,000 containers from the same image, does it use 1,000x the RAM for the filesystem?**
**A**: No. The kernel is smart. It maps the read-only layers into memory once (Page Cache) and shares them across all processes. Only the unique writable pages consume additional RAM.

## ⚠️ Edge Cases
- **Inodes**: Every layer and every file consumes an inode. If you have too many layers or millions of small files, you can run out of inodes on the host disk even if you have plenty of gigabytes left.

## 🏢 Best Practices
- **Minimize Layers**: Group related commands in a single `RUN`.
- **Use Multi-stage Builds**: This discards the heavy build-tool layers and only keeps the final artifact layer.
- **Clean up in the same layer**: Always delete cache/temp files in the same `RUN` instruction where they were created.

## ⚖️ Trade-offs
| Storage Driver | Performance | Stability |
| :--- | :--- | :--- |
| **Overlay2** | **High** | **Standard** |
| **Btrfs** | Medium | High |
| **ZFS** | Medium | Highest |

## 💼 Interview Q&A
**Q: Explain "Copy-on-Write" (CoW) in the context of Docker.**
**A**: CoW is an optimization strategy where the system only copies a resource when a modification is attempted. In Docker, all image layers are immutable (read-only). When a container needs to modify a file that exists in an image layer, the storage driver copies that file from the read-only layer up to the container's writable layer. All subsequent reads and writes happen on this copy. This allows multiple containers to share the same underlying image data safely and efficiently.

## 🧩 Practice Problems
1. Use `docker history <image>` to see the size of each layer. Find a layer that "adds" 0 bytes but performs a command.
2. Create a container, add a file, and then find where that file physically lives on your host's filesystem using `docker inspect`.

---
Prev: [03_Namespaces_and_cgroups.md](./03_Namespaces_and_cgroups.md) | Index: [00_Index.md](../00_Index.md) | Next: [05_Container_Runtime_runc_containerd_OCI.md](./05_Container_Runtime_runc_containerd_OCI.md)
---
