# 📂 The Linux Filesystem Hierarchy

In Windows, you have `C:\` and `D:\`. In Linux, everything starts from a single point: **The Root (/)**.

## 🌳 The Root Tree Analogy
Imagine a huge tree. The Root is the ground (`/`). Every folder branches out from there.

| Folder | Purpose | Real-Life Analogy |
| :--- | :--- | :--- |
| `/` | **Root** | The base of the whole tree. |
| `/root` | **Home of the Boss** | The private office of the System Administrator. |
| `/home` | **User Bedrooms** | Where normal users (like you) store their files (Documents, Photos). |
| `/etc` | **Settings/Switchboard** | Where all configuration files live (like the system's "Settings" menu). |
| `/bin` | **Essential Tools** | Contains basic commands like `ls` and `cp` (Your basic toolkit). |
| `/var` | **Variable Data** | Where logs and databases live (Things that change constantly). |
| `/tmp` | **Trash/Scrapbook** | Temporary files that are deleted when you restart. |
| `/usr` | **User Apps** | Where user-installed programs live. |

---

## 🛠️ Why does this matter in DevOps?
*   **Logs:** When an app crashes, a DevOps engineer immediately looks into `/var/log`.
*   **Configs:** When we need to change how a web server (like Nginx) works, we go to `/etc/nginx`.
*   **Permissions:** You shouldn't store your personal photos in `/bin`! Knowing where things go keeps the system safe.

---

## ✍️ Hands-on Task
1. Open your terminal.
2. Type `cd /` to go to the Root.
3. Type `ls` to see all the folders mentioned above.
4. Go to the "Bedroom" by typing `cd /home`.

---
Prev: [02_linux_architecture_shell.md](02_linux_architecture_shell.md) | Index: [00_index.md](00_index.md) | Next: [04_basic_commands.md](04_basic_commands.md)
---
