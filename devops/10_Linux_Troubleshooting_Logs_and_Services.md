# 🐧 Linux Commands & Concepts (Intermediate - Part 4)

> **File:** `10_Linux_Troubleshooting_Logs_and_Services.md`  
> **Topic:** Troubleshooting, Boot Process, Logs, Services, Disk & System Debugging  
> **Level:** 🟡 Intermediate  
> **Prerequisites:** [09_Linux_VI_Editor_and_Package_Management.md](./09_Linux_VI_Editor_and_Package_Management.md)

---

## 📌 Introduction

In the world of **DevOps**, troubleshooting is your superpower. Imagine this: It’s a busy Monday morning, and your company’s e-commerce website goes down. Customers can’t place orders, and every minute of downtime costs thousands of dollars. As a DevOps Engineer, you are the first person called to fix it.

Is the server out of memory? Is the disk full? Did a recent update crash the service? To answer these questions, you need to know exactly where to look and which commands to run. This guide will walk you through the essential tools for Linux troubleshooting, boot processes, and system debugging—tools that separate a beginner from a senior professional.

---

## 📚 Table of Contents
1. [🌐 Website Troubleshooting Basics](#-website-troubleshooting-basics)
2. [🖥️ Linux Boot Process Deep Dive](#-linux-boot-process-deep-dive)
3. [📊 System Troubleshooting Commands](#-system-troubleshooting-commands)
4. [📁 Log Management & Debugging](#-log-management--debugging)
5. [⚙️ Service & Process Management](#-service--process-management)
6. [💽 Disk & Storage Troubleshooting](#-disk--storage-troubleshooting)
7. [🔐 File Permissions (Troubleshooting Perspective)](#-file-permissions-troubleshooting-perspective)
8. [🏋️ Practice Tasks](#-practice-tasks)
9. [🎤 Interview Questions](#-interview-questions)
10. [📝 Summary](#-summary)

---

## 🌐 Website Troubleshooting Basics

Before you even touch the server terminal, you often start from the **Browser**.

### 1. Browser Inspect (Network Tab)
If a site isn't loading, right-click anywhere on the page and select **Inspect** (or press `F12`), then go to the **Network** tab. Refresh the page to see every request made by your browser.

*   **Red Rows:** Indicate failed requests.
*   **Time Column:** Shows if a backend API is taking too long to respond.

### 2. HTTP Status Codes (The Secret Language)
Status codes tell you *whose* fault it is:
*   **1xx (Informational):** Request received, continuing process.
*   **2xx (Success):** Everything is fine (e.g., `200 OK`).
*   **3xx (Redirection):** The resource moved (e.g., `301 Moved Permanently`).
*   **4xx (Client Error):** YOUR fault (Browsers/Users).
    *   `403 Forbidden`: You don't have permission.
    *   `404 Not Found`: The URL is wrong or the file is missing.
*   **5xx (Server Error):** THE SERVER'S fault (DevOps/Backend).
    *   `500 Internal Server Error`: The code crashed.
    *   `502 Bad Gateway`: The proxy (Nginx) can't reach the backend.
    *   `503 Service Unavailable`: The server is overloaded.

**Real-World Scenario:** If a user says "I can't log in," and you see a `500 error` in the Network tab, you know you need to check the **Application Logs** on the server.

---

## 🖥️ Linux Boot Process Deep Dive

To fix a server that won't start, you must understand how it wakes up.

### The 6 Stages of Booting
1.  **BIOS/UEFI (Basic Input/Output System):** Performs a Power-On Self-Test (POST) to ensure the hardware components (RAM, CPU, Hard Drive) are functioning correctly. It’s like a person waking up and checking if their hands and legs work. After the POST, it looks for the bootable drive.
2.  **MBR/GPT (Master Boot Record / GUID Partition Table):** This is the very first sector of the bootable drive. It contains information about how the disk is partitioned and holds the primary bootloader execution code. It points the system to where the GRUB bootloader is located.
3.  **Bootloader (GRUB - Grand Unified Bootloader):** The boot menu you sometimes see when starting a computer. It finds the Operating System and asks, "Which OS or Linux kernel version do you want to load?" It then loads the selected kernel into RAM.
4.  **Kernel:** The absolute heart of Linux. It takes over from GRUB, initializes the hardware (CPU, RAM, Disk), mounts the root file system as read-only initially, and wakes up the first system process (`init` or `systemd`).
5.  **Init (systemd):** The very first process to run in Linux, which means it always gets PID 1 (Process ID 1). It is responsible for starting up all other background services, managing daemons (Nginx, Database, SSH), and mounting the file systems as read-write.
6.  **Runlevel / Target:** This final stage determines the state the system will boot into. It decides if you get a graphical user interface (GUI / Desktop) or just a command-line Terminal (CLI). For servers, this is typically set to multi-user, text-only mode to save resources.

### 🪟 Windows Boot Process (For Comparison)
Understanding the Windows boot process is also helpful, especially in mixed environments. Here is how Windows wakes up:
1.  **BIOS/UEFI & POST:** Just like Linux, it starts with a Power-On Self-Test (POST) to check hardware components.
2.  **Bootmgr (Windows Boot Manager):** The BIOS/UEFI reads the boot sector (MBR/GPT) which launches `Bootmgr`. `Bootmgr` reads the **BCD** (Boot Configuration Data) to find the OS.
3.  **Winload:** `Bootmgr` executes `winload.exe` (or `winload.efi`), which acts like the later stages of GRUB. It loads the Windows Kernel and core drivers into memory.
4.  **NTOSKRNL (Windows Kernel):** The Windows Kernel (`ntoskrnl.exe`) takes over, initializes hardware, and starts the system processes.
5.  **SMSS (Session Manager):** The kernel starts `smss.exe` (Session Manager Subsystem), which sets up the environment and starts core subsystems like `csrss.exe` and `wininit.exe`.
6.  **Winlogon & GUI:** Finally, `winlogon.exe` and `lsass.exe` (security) are started. This presents the Windows login screen and loads the user desktop (GUI).

### 📜 The `dmesg` Command
`dmesg` (Display Message) shows the kernel's log buffer. Use it to see hardware errors or boot issues.
```bash
dmesg | less
# Search for errors during boot
dmesg | grep -i error
```
**Analogy:** If your car doesn't start, `dmesg` is like looking under the hood to see if a wire is disconnected.

---

## 📊 System Troubleshooting Commands

When the system feels "slow," use these tools to find the bottleneck.

### 1. Hardware Overview
*   `lsblk`: List all disk partitions (check if a drive is mounted).
*   `lshw`: List all hardware (CPU, Motherboard, etc.).
*   `cat /proc/cpuinfo`: Detailed info about your processor.

### 2. Resource Checks
*   `free -h`: Check RAM usage in "human-readable" format (GB/MB).
*   `df -h`: Check Disk Space. If `/` is **100% full**, the system will crash!
*   `top`: The "Task Manager" of Linux. Shows real-time CPU/RAM usage.
*   `htop`: A much better, colorful version of `top` (you might need to install it).

**Real Debugging Scenario:**
*   **High CPU?** Check `top`. Find the process ID (PID) using the most %CPU.
*   **Everything is slow?** Check `free -h`. If `available` is near 0, the system is swapping, which is very slow.

---

## 📁 Log Management & Debugging

Logs are the "Black Box" of a server. They record everything that happens.

### Where are logs?
Almost all logs live in: `/var/log/`
*   `/var/log/syslog` (Debian/Ubuntu) or `/var/log/messages` (RHEL/CentOS): General system logs.
*   `/var/log/auth.log`: Security and login attempts.
*   `/var/log/nginx/error.log`: Why your website is down.

### ⚠️ How to view logs?
**NEVER use `vi` or `nano` to just check logs.** If a log file is 5GB, an editor will try to load it into RAM and crash your server!
*   `cat`: Best for small files.
*   `less`: Best for large files. You can scroll and search (`/word`).
*   `tail -f /var/log/syslog`: **Crucial!** It follows the log in real-time as new lines are added.

---

## ⚙️ Service & Process Management

In DevOps, we manage "Services" (long-running apps like Nginx or Docker).

### Using `systemctl`
*   `systemctl status nginx`: Is it running or failed?
*   `systemctl start nginx`: Turn it on.
*   `systemctl stop nginx`: Turn it off.
*   `systemctl restart nginx`: Stop then Start (cleans up stuck processes).
*   `systemctl enable nginx`: Make sure it starts automatically when the server reboots.

### Managing Processes
*   `ps -ef`: List every running process on the system.
*   `kill -15 <PID>`: **Graceful Kill**. Asks the app to "Please save your work and close."
*   `kill -9 <PID>`: **Force Kill**. Literally kills the process instantly. Use only as a last resort!

---

## 💽 Disk & Storage Troubleshooting

"Disk Full" is the most common reason for production outages.

1.  **Find which disk is full:** `df -h`
2.  **Find which FOLDER is taking space:** `du -sh /var/log/*` (Disk Usage)
3.  **Cleanup Strategy:**
    *   Delete old logs (like `.log.1` or `.gz` files).
    *   Clear temporary files in `/tmp`.
    *   **Automation:** Use `logrotate` to automatically compress and delete old logs.

---

## 🔐 File Permissions (Troubleshooting Perspective)

If you get a **"Permission Denied"** error, it's a permission issue.

Run `ls -l` to see permissions:
`-rwxr-xr--  1 root root`

*   **R** (Read), **W** (Write), **X** (Execute).
*   **Owner** (first 3), **Group** (next 3), **Others** (last 3).

**Fixing it:**
*   `chmod 755 script.sh`: Makes it executable for you.
*   `chown user:group file`: Changes who owns the file.

---

## 🏋️ Practice Tasks

Perform these steps to become comfortable with troubleshooting:

1.  **Resource Check:** Open your terminal and run `free -h` and `df -h`. Identify if any partition is more than 80% full.
2.  **Live Log Monitoring:** Run `sudo tail -f /var/log/auth.log` in one terminal. In another, try {to try to} SSH into your server with a wrong password. Watch the log update in real-time!
3.  **Process Hunt:** Find the PID of your browser or any app using `ps -ef | grep <app_name>`.
4.  **Service Restart:** Check the status of the `systemd-journald` service using `systemctl status`. Restart it and check the status again.
5.  **Permissions:** Create a file `test.txt`. Remove all permissions using `chmod 000 test.txt`. Try to read it using `cat`. Then fix it using `chmod 644 test.txt`.

---

## 🎤 Interview Questions

1.  **Q: What is the difference between `kill -9` and `kill -15`?**
    *   **A:** `kill -15` (SIGTERM) is a graceful termination signal allowing the process to clean up. `kill -9` (SIGKILL) is an immediate force-kill that doesn't allow any cleanup.

2.  **Q: Where would you look if your web server stops responding?**
    *   **A:** First, check the service status with `systemctl status nginx/apache`. Then check the logs in `/var/log/nginx/error.log`. Finally, check system resources using `df -h` and `free -h`.

3.  **Q: What does a 502 Bad Gateway error usually mean?**
    *   **A:** It means your web proxy (like Nginx) cannot communicate with the backend application service (like Gunicorn or Node.js).

4.  **Q: How do you check which process is consuming the most CPU?**
    *   **A:** Use the `top` or `htop` command and sort by `%CPU`.

5.  **Q: What is the purpose of the `dmesg` command?**
    *   **A:** It displays the kernel messages, helping to debug hardware issues, driver problems, or boot errors.

6.  **Q: If a disk is 100% full, but you can't find large files, what could be the issue?**
    *   **A:** Deleted files might still be "held open" by a running process. You can find these using `lsof | grep deleted`.

7.  **Q: Describe the Linux boot process in simple steps.**
    *   **A:** BIOS/UEFI -> Bootloader (GRUB) -> Kernel -> Init (systemd) -> Targets/Runlevels.

8.  **Q: What is the difference between `top` and `htop`?**
    *   **A:** `top` is the default basic monitor. `htop` is an interactive, color-coded, and more user-friendly version that allows sorting and searching easily.

9.  **Q: How do you make a service start automatically on boot?**
    *   **A:** Use `systemctl enable <service_name>`.

10. **Q: Why should you avoid using `vi` to open a 10GB log file?**
    *   **A:** Editors like `vi` load the entire file into RAM, which can cause the system to run out of memory and crash. Use `less` or `tail` instead.

---

## 📝 Summary

| Command | Use Case |
| :--- | :--- |
| `df -h` | Check Disk Space (Human readable) |
| `free -h` | Check RAM usage |
| `top` / `htop` | Monitor system processes and CPU usage |
| `tail -f` | Watch log files update in real-time |
| `systemctl` | Manage system services (start, stop, status) |
| `dmesg` | View kernel and boot-time hardware logs |
| `ps -ef` | Snapshot of all running processes |
| `chmod` / `chown` | Fix permission and ownership issues |

**Congratulations!** You now have a solid foundation in Linux troubleshooting. Keep practicing! 🚀

---
Prev : [09_Linux_VI_Editor_and_Package_Management.md](09_Linux_VI_Editor_and_Package_Management.md) | Next : [11_AWS_Basics_and_Cloud_Introduction.md](11_AWS_Basics_and_Cloud_Introduction.md)
---
