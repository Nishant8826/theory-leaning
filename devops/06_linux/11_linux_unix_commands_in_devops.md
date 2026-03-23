# ⌨️ Linux/UNIX Commands in DevOps

In DevOps, we don't use a mouse. We use commands. Here are the core categories of commands you'll use every day.

## 1. 🧭 Navigation (Where am I?)
- `pwd`: Print Working Directory.
- `ls`: List files.
- `cd`: Change directory.

## 2. 📂 File Operations (Doing stuff)
- `mkdir`: Create a folder.
- `touch`: Create a blank file.
- `cp`: Copy.
- `mv`: Move or Rename.
- `rm`: Remove (Delete). **USE WITH CAUTION!**

## 3. 🔍 Reading Files (Investigation)
- `cat`: See the whole file.
- `head` / `tail`: See the first or last 10 lines.
- `grep`: Search for text inside a file. (The most used tool!).

## 4. 🛠️ System Info (The Health Check)
- `top` / `htop`: See CPU/RAM usage.
- `df -h`: See how much disk space is left.
- `free -m`: See available RAM.

## 🔍 Comparison of Command Styles

| Goal | Windows (CMD) | Linux/UNIX (Bash) |
| :--- | :--- | :--- |
| **List Files** | `dir` | `ls` |
| **Clear Screen** | `cls` | `clear` |
| **Copy File** | `copy` | `cp` |
| **Show IP** | `ipconfig` | `ip a` or `ifconfig` |

## 🌍 Real-World Scenario: The Log Search
A developer says "The payment failed at 10:05 PM". 
You don't open the 5GB log file in Notepad. You type:
`grep "10:05" payment.log | grep "failed"`
Linux finds the exact line in **0.1 seconds**.

---
## 💡 Pro Tip
Always use `ls -la`. 
- `-l` shows details (size, date).
- `-a` shows hidden files (files starting with a dot `.`).

---
Prev: [10_create_linux_in_gcp.md](10_create_linux_in_gcp.md) | Next: [12_practice_linux_commands.md](12_practice_linux_commands.md)
