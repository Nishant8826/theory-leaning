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


### 💡 Dev Tip
*   `df -h` is critical to prevent filled up disk space from logs, which can silently crash Node.js PM2 apps or databases operations.

## 🧠 Core Concepts Summary
*   **What:** Utilizing CLI instrumentation (`htop`, `df`, `free`) to visualize the CPU, Memory, and Disk usage health metrics.
*   **Why:** If CPU spikes to 100% or storage reaches 100% capacity, systems grind to a lethal halt; proactive monitoring prevents spontaneous server death.
*   **How:** Periodically inspecting the dashboard outputs or setting up automated alerts based on disk volume blocks (`df -h`).
*   **Impact:** Predicts scaling requirements before a major business release and avoids terrifying 3 AM production outages.

---
Prev: [13_http_status_codes.md](13_http_status_codes.md) | Index: [00_index.md](00_index.md) | Next: [15_ssh_key_management.md](15_ssh_key_management.md)
---
