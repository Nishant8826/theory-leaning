# 📊 System Monitoring: Checking the Server's Health

As a DevOps engineer, you are the doctor for your servers. You need tools to check if the server is feeling well or if it's "sick" (running out of space or memory).

## 🛠️ Monitoring Tools (Commands)
1.  **`df` (Disk Free):** Checks how much hard drive space is left.
    *   *Example:* `df -h` (The `-h` makes it "Human Readable" - 5 GB instead of a giant number of bytes).
2.  **`free`:** Checks how much RAM (Memory) is currently used.
    *   *Example:* `free -m` (Shows RAM in Megabytes).
3.  **`uptime`:** Tells you how long the server has been running without a reboot.
4.  **`du` (Disk Usage):** Shows which folders are taking up the most space.
    *   *Example:* `du -sh *` (Summarize the size of every folder in the current directory).

---

## 🚀 Real-World DevOps Usage
*   **Disk Check:** You get an alert that "Database is full." You use `df -h` to confirm the disk is at 100% capacity.
*   **Memory Check:** If your application crashes, you use `free -m` to see if the server ran out of memory (RAM).

---

## ✍️ Hands-on Task
1. Run `df -h` on your terminal. Look for the `/` (Root) line. How much space is left?
2. Run `free -m`. Check the "Available" column.
3. Type `uptime` to see if your computer has been awake for a long time!

---
Previous: [08_process_management.md](08_process_management.md) Next: [10_service_management.md](10_service_management.md)
---
