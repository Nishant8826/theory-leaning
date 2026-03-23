# 🗺️ The Ultimate Linux Cheatsheet

Bookmark this page! This is your "Cheat Code" for surviving inside the Linux terminal.

## 📂 Navigation & Files
| Command | Action |
| :--- | :--- |
| `ls -la` | **List ALL files** (Even hidden ones). |
| `cd ..` | **Go back** one folder. |
| `pwd` | **Where am I?** (Show current path). |
| `mkdir -p a/b/c` | **Make nested folders** at once. |
| `rm -rf folder` | **FORCE Delete** a folder (Careful!). |

## 🛠️ System Control
| Command | Action |
| :--- | :--- |
| `sudo !!` | **Run the last command** but with admin power. |
| `systemctl restart app` | **Reboot an application**. |
| `top` / `htop` | **Show Task Manager**. |
| `kill -9 PID` | **Kill a frozen app**. |

## 🔍 Searching & Text
| Command | Action |
| :--- | :--- |
| `grep "text" file` | **Search inside file**. |
| `find . -name "file"` | **Search for file**. |
| `sed -i 's/a/b/g' file` | **Replace 'a' with 'b'** globally. |
| `head -n 5 file` | **See first 5 lines**. |
| `tail -f file` | **See new lines in real-time**. |

## 🌐 Networking & SSH
| Command | Action |
| :--- | :--- |
| `ip addr` | **Show My IP**. |
| `curl -I site.com` | **Check Website status**. |
| `ping site.com` | **Check connectivity**. |
| `ssh user@ip` | **Connect to remote server**. |

---

## ✍️ Quick Revision
If you need to find a log file that contains the word "Error," how do you do it? 
`grep "Error" /var/log/syslog`

---
Previous: [19_linux_day_to_day_tasks.md](19_linux_day_to_day_tasks.md)  
Next: [21_linux_tips_2026.md](21_linux_tips_2026.md)
---
