# 🔄 Process Management: The Task Manager of Linux

Every time you run a command or open an app, it becomes a "Process." Sometimes these processes misbehave, and you need to handle them.

## 🕒 What is a Process?
Imagine a kitchen. 
*   **Code:** The recipe.
*   **Process:** The actual act of cooking the meal.
Each process has a unique ID number called a **PID (Process ID)**.

---

## 🛠️ Managing Processes (Commands)
*   **`ps` (Process Status):** Show what's running right now.
    *   *Example:* `ps aux` (Shows *every* process on the system).
*   **`top`:** A live dashboard showing what's using the most CPU and RAM.
*   **`htop`:** A prettier, more intuitive version of `top` (you might need to install it).
*   **`kill`:** Stop a process that is stuck.
    *   *Example:* `kill 1234` (Stops the process with PID 1234).
    *   *Example:* `kill -9 1234` (Forcing a process to stop - use this only if it's really stuck).

## 🚀 Real-World DevOps Use Case
Your website is suddenly slow. You log into the server, run `top`, and see that a single process is taking up 99% of the CPU. You identify the PID and use `kill` to stop it. Website fixed!

---

## ✍️ Hands-on Task
1. Open your terminal and type `top`.
2. Look at the `CPU%` and `MEM%` columns.
3. To exit `top`, just press the letter `q` on your keyboard.
4. Try typing `ps ux` to see only your own running processes.

---
Previous: [07_file_permissions.md](07_file_permissions.md)  
Next: [09_system_monitoring.md](09_system_monitoring.md)
---
