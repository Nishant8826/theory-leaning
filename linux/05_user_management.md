# 👤 User Management: Who's the Boss?

On a Linux server, many different people (and machines) work together. We need to control who can do what.

## 👑 The Root User (The Super Boss)
The most powerful user is called `root`. 
*   **Analogy:** The Root has the master key to every room and can delete anything. 
*   **Safety Tip:** Don't work as Root every day. You might accidentally delete the whole system with a single typo!

## 👦 Normal Users (The Office Workers)
These are users like `john` or `mary`. They can only touch their own files in `/home/john`.

---

## 🛠️ Managing Users (Commands)
*   **`useradd`:** Create a new user account.
    *   *Example:* `sudo useradd -m mary` (The `-m` creates a home directory for her).
    *   **How Mary logs in after you add her:**
        *   **Switching Users (Local):** If you are an administrator on the same machine, Mary can start working by typing `su - mary` (switch user) in the terminal.
        *   **Remote Login (SSH):** If the server is remote, Mary can log in from her own computer using `ssh mary@<server_ip_address>`.
*   **`passwd`:** Set or change a password. (Mary needs a password before she can log in!)
    *   *Example:* `sudo passwd mary`
*   **`userdel`:** Remove a user account.
    *   *Example:* `sudo userdel -r mary` (The `-r` removes her home directory too).

## 👥 Groups (The Teams)
Instead of giving permissions to 50 people one by one, we put them in a group.
*   **Team Analogy:** Group "DevOps" can access the server, group "Marketing" cannot.
*   **`groupadd`:** Create a new group.
    *   *Example:* `sudo groupadd devops`
*   **`usermod`:** Add a user to a group.
    *   *Example:* `sudo usermod -aG devops mary`

---

## 🚀 Real-World DevOps Use Case
When a new developer joins your company:
1. You create their user (`useradd`).
2. You add them to the `developer` group so they can access the codebase.
3. You never give them the `root` password for safety!

---

## ✍️ Hands-on Task
1. Check who is currently logged in by typing `whoami`.
2. Check your groups by typing `groups`.
3. Read the `/etc/passwd` file (using `cat /etc/passwd`) to see all the users on the system.

## 🧠 Core Concepts Summary
*   **What:** A multi-layered permissions architecture that dictates strictly who can access the machine and what actions they can perform.
*   **Why:** Running public-facing servers implies malicious access attempts. You must restrict privileges so a compromised web app doesn't grant hackers root system access.
*   **How:** Administrators execute commands like `useradd` and `usermod` to group individuals, selectively granting `sudo` execution rights.
*   **Impact:** Neutralizes insider threats and hacker escalations, ensuring that an attacker gaining entry as a "www-data" worker cannot delete the database.

---
Prev: [04_basic_commands.md](04_basic_commands.md) | Index: [00_index.md](00_index.md) | Next: [06_file_permissions.md](06_file_permissions.md)
---
