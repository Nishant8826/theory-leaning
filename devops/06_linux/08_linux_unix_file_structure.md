# 📂 Linux/UNIX File Structure

In Windows, you have `C:\` and `D:\`. In Linux, the world is simpler. Everything starts from a single point: **The Root (/)**.

## 🌳 The "Root" Tree
Imagine a tree where `/` is the ground. Every folder branches out from there.

| Folder | Purpose | Real-Life Analogy |
| :--- | :--- | :--- |
| `/` | **The Root** | The foundation of the whole building. |
| `/bin` | **User Binaries** | Your basic tools (like `ls`, `cp`). |
| `/etc` | **Configuration Files** | The building's electrical switchboard (Settings). |
| `/home` | **User Folders** | Your personal bedroom (where your docs live). |
| `/root` | **Admin Home** | The landlord's private office. |
| `/var` | **Variable Files** | The building's garbage and logs (things that change). |
| `/tmp` | **Temporary Files** | A scratchpad that gets wiped when you restart. |
| `/usr` | **User Programs** | Your installed apps (like Chrome or Python). |

## 🔍 Major Difference: Windows vs. Linux

| Feature | Windows | Linux |
| :--- | :--- | :--- |
| **Starting Point** | Multiple (`C:\`, `D:\`, `E:\`) | Single (`/`) |
| **Separator** | Backslash (`\`) | Forward Slash (`/`) |
| **Everything is a File?** | No | **YES!** Even your mouse is a file in Linux. |

## 🌍 Real-World Scenario: Debugging
A website is showing a "500 Internal Server Error". 
- In Windows, you look for a "Log Viewer" app.
- In Linux, you immediately go to `/var/log/nginx/error.log` to read the text file.

---
## ✍️ Hands-on Task
If you have a terminal open, type `cd /` and then `ls`. You will see all these folders like `etc`, `bin`, and `var`.

---
Prev: [07_linux_vs_unix.md](07_linux_vs_unix.md) | Next: [09_creating_linux_vm_docker_cloud.md](09_creating_linux_vm_docker_cloud.md)
