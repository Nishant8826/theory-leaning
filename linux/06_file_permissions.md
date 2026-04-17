# 🔐 File Permissions: The Lock & Key

In Linux, every file and folder has its own "security guard." This ensures only the right people can see or change its content.

## 🛡️ The Three Power Permissions
1.  **Read (r):** You can look at the content.
2.  **Write (w):** You can change or delete the content.
3.  **Execute (x):** You can run the file (like a script or program).

---

## 🔢 Understanding the Numbers (Octal)
You'll often see numbers like `755` or `644`. Here's what they mean:
*   **4** = Read
*   **2** = Write
*   **1** = Execute
*   **Total = 7 (Read + Write + Execute)**
*   **Total = 6 (Read + Write)**
*   **Total = 5 (Read + Execute)**

### The Order Matters:
A permission like `755` means:
*   **User (Boss):** 7 (Full access)
*   **Group (Team):** 5 (Read/Execute)
*   **Others (World):** 5 (Read/Execute)

---

## 🛠️ Changing Permissions (Commands)
*   **`chmod` (Change Mode):** Change permissions.
    *   *Example:* `chmod 777 file.txt` (Everyone can do anything!)
    *   *Example:* `chmod a+x script.sh` (Make the script runnable).
*   **`chown` (Change Owner):** Change who "owns" the file.
    *   *Example:* `sudo chown mary file.txt` (Mary is now the boss of this file).

---

## 💡 Real-World scenario
You have a "database config" file containing a password. Only the "app" should read it. No one else should even see it. You would use `chmod 400 password.txt` to keep it safe!

---

## ✍️ Hands-on Task
1. Create a file called `private.txt`.
2. Type `ls -l` to see its current permissions (the `rw-r--r--` part).
3. Change it so only you can read it: `chmod 400 private.txt`.
4. Try to list it again. It now says `r--------`.


### 💡 Dev Tip
*   `chmod +x` is often the key to fixing deployment issues when executing Node.js processes or shell scripts on AWS EC2.

## 🧠 Core Concepts Summary
*   **What:** A stringent 3-tier access system (Read/Write/Execute) applied to every single file and folder individually.
*   **Why:** Prevents unauthorized personnel or malicious bots from altering vital configuration files or reading sensitive environment variables.
*   **How:** We assign numeric (octal) or symbolic blocks (e.g., `chmod 755 app.js` or `chown john:devs index.html`) defining privileges for the owner, the group, and everyone else.
*   **Impact:** Enforces a rigid web-security model, directly stopping unauthorized script executions from disrupting live production apps.

---
Prev: [05_user_management.md](05_user_management.md) | Index: [00_index.md](00_index.md) | Next: [07_linux_boot_process.md](07_linux_boot_process.md)
---
