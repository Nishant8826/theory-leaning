# 📌 Topic: Tmpfs Mounts and Data Security

🟢 **Simple Explanation (Beginner)**
-----------------------------------
Imagine you are writing a **Secret Code**. 
- If you write it in a **Notebook** (Volume/Bind Mount), it's saved on the paper even if you close the book.
- If you write it on a **Whiteboard** (Tmpfs), it is wiped clean the moment you leave the room.

**Tmpfs** stands for "Temporary Filesystem." It lives only in your computer's **RAM (Memory)**. It never touches your hard drive. This makes it incredibly fast and very secure for temporary secrets.

🟡 **Practical Usage**
-----------------------------------
### When to use Tmpfs?
1. **Secrets**: Storing passwords or API keys that shouldn't be written to disk.
2. **Speed**: Storing temporary session data or caches that need to be accessed thousands of times per second.
3. **Security**: Ensuring that no trace of the data is left on the server if the power goes out.

**How to use it:**
```powershell
# Mount /app/secrets into RAM
docker run -d --tmpfs /app/secrets nginx
```

**Note**: Tmpfs is only available on **Linux**. Docker Desktop on Mac/Windows supports it through the hidden Linux VM.

🔵 **Intermediate Understanding**
-----------------------------------
### Tmpfs vs. Volumes
| Feature | Volume | Tmpfs |
| :--- | :--- | :--- |
| **Storage** | Hard Drive / SSD | RAM (Memory) |
| **Persistence** | Yes (Stays after stop) | No (Gone after stop) |
| **Speed** | Fast | Instant (Lightning Fast) |
| **Sharing** | Can share between containers | Private to one container |

### Setting Limits
Because Tmpfs uses RAM, a malicious container could fill it up and crash your host!
**Best Practice**: Always set a size limit.
```bash
docker run -d --mount type=tmpfs,destination=/app/cache,tmpfs-size=100m nginx
```

🔴 **Internals (Advanced)**
-----------------------------------
### RAM Disk
Tmpfs is a standard Linux kernel feature. It creates a virtual partition in the memory pool. 
When you read/write to a tmpfs mount, there is **zero context switching** to the disk controller and **zero disk head movement**. 

### Memory Swapping
If your host starts running out of physical RAM, the Linux kernel might move parts of your "Tmpfs" data to the **Swap partition** on your hard drive.
**Staff Security Warning**: If this happens, your "secrets" are now written to the hard drive in the Swap file! To prevent this, you must disable swap on your production servers or use `mlock()`.

⚫ **Staff-Level Insights**
-----------------------------------
### Database "Work Mem"
Staff engineers often point their database's temporary working directory (like `tmpdir` in MySQL) to a Tmpfs mount. This makes complex `SORT` and `JOIN` operations significantly faster because the sorting happens entirely in RAM.

### PCI-DSS and Compliance
If you are handling Credit Card data, you are often forbidden from writing that data to a persistent disk. Tmpfs is a standard tool used to meet **Security Compliance** because it ensures the data is "volatile."

🏗️ **Mental Model**
Tmpfs is a **RAM-only Workspace**.

⚡ **Actual Behavior**
When the container stops, the Tmpfs mount is unmounted, and the memory is instantly freed for other processes. The data is unrecoverable.

🧠 **Resource Behavior**
- **Memory**: Tmpfs counts towards your container's **Memory Limit**. If you set a 512MB RAM limit and a 200MB Tmpfs, your app only has 312MB left for code!

💥 **Production Failures**
- **The "Memory Leak"**: An app keeps writing temporary files to `/tmp` (which is mapped to Tmpfs). It never deletes them. Eventually, the container hits its RAM limit and is killed by the OOM Killer.
- **Data Loss on Restart**: You accidentally put your actual database files in Tmpfs. The container restarts for an update, and your entire database is empty.

🏢 **Best Practices**
- Use Tmpfs for `/tmp` and `/var/run`.
- Always set `tmpfs-size`.
- Use Tmpfs for sensitive keys that are decrypted only at runtime.

🧪 **Debugging**
```bash
# See how much space is being used in Tmpfs inside a container
docker exec <id> df -h /app/secrets

# Check mount type
docker inspect <id> --format '{{ .Mounts }}'
```

💼 **Interview Q&A**
- **Q**: Why would you use a Tmpfs mount instead of a regular volume?
- **A**: For higher performance (RAM speed) and better security (data doesn't persist on disk).
- **Q**: Does Tmpfs work on Windows native containers?
- **A**: No. It is a Linux-specific kernel feature.

---
Prev: [20_Storage_Drivers_and_OverlayFS_Internals.md](20_Storage_Drivers_and_OverlayFS_Internals.md) | Index: [00_Index.md](../00_Index.md) | Next: [../Orchestration/22_Docker_Compose_Declarative_Containers.md](../Orchestration/22_Docker_Compose_Declarative_Containers.md)
---
