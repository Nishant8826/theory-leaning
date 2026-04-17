# 🚦 The Linux Boot Process: The Morning Routine

What happens between the time you press the power button and the time you see the login screen? It's like waking up in the morning.

## 🌅 Step-by-Step Awakening
1.  **BIOS/UEFI (The Alarm):** Check if the hardware (RAM, Disk) is okay.
2.  **GRUB (The Choice):** Where you pick which version of Linux to load.
3.  **Kernel (The Brain):** The "Boss" loads into memory and starts managing hardware.
4.  **Init (systemd) (The Manager):** The very first process (`PID 1`) that starts all other programs (WiFi, Keyboard, Web Server).

---

## 💡 Real-World DevOps Use Case
Why should you care? If a server doesn't "come back to life" after a reboot, you need to know *where* it stopped.
*   **Case 1:** It stops at BIOS? There is a hardware problem.
*   **Case 2:** It stops at the Kernel? A software update might have broken the core.

---

## ✍️ Hands-on Task
1. Look at your processes by typing `ps -p 1`.
2. See what is listed under the "COMMAND" column. It should either be `/sbin/init` or `systemd`. This is the "Grandfather" of every other process on your computer!

---
Prev: [07_file_permissions.md](07_file_permissions.md) | Index: [00_index.md](00_index.md) | Next: [08_process_management.md](08_process_management.md)
---
