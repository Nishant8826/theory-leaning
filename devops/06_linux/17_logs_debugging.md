# 🔎 Logs & Debugging: Finding the Culprit

If a server is a black box, the "Logs" are its diary. They record everything that happens—the good, the bad, and the ugly.

## 📂 Where are the Diary Entries?
Almost all logs live in one place: `/var/log`.

| File | What it tells you |
| :--- | :--- |
| `/var/log/syslog` | **General system events** |
| `/var/log/auth.log` | **Security/Logins** (Who entered the building?) |
| `/var/log/apache2/error.log` | **Web server errors** |
| `/var/log/kern.log` | **Kernel issues** |

---

## 🛠️ Debugging Tools (Commands)
1.  **`tail`:** Look at the *last* few lines of a file (the most recent events).
    *   *Example:* `tail -f /var/log/syslog` (Shows lines as they happen in "Real-Time").
2.  **`less`:** Open a big file and scroll through it effortlessly.
3.  **`grep`:** Search for a specific word (like "CRITICAL") in a log file.
4.  **`journalctl`:** The modern way to read "systemd" logs.
    *   *Example:* `journalctl -u nginx` (Shows logs only for the Nginx service).

## 🚀 Real-World DevOps Use Case
A website is showing "Internal Server Error." 
1. You run `tail -f /var/log/apache2/error.log`. 
2. You refresh the site. 
3. You see the exact line of code that is failing in your terminal. Fixed!

---

## ✍️ Hands-on Task
1. Check the general logs on your system: `sudo tail -n 20 /var/log/syslog`.
2. Look through the login history: `sudo tail /var/log/auth.log`.
3. Try giving a wrong command and seeing if it gets recorded anywhere!

---
Previous: [16_linux_boot_process.md](16_linux_boot_process.md)  
Next: [18_http_status_codes.md](18_http_status_codes.md)
---
