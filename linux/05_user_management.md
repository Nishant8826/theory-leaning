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
            *   > **⚠️ Common Error:** `Permission denied (publickey)` when trying to login with a `.pem` key (e.g., `ssh -i mykey.pem mary@<server_ip>`).
            *   > **Why this happens:** In cloud servers (like AWS), newly created users do not automatically receive SSH keys. Mary's `~/.ssh/authorized_keys` file is missing, so the server rejects the connection.
            *   > **The Solution (Copy the key):** You must copy the existing SSH keys to the new user's home directory.
            *   >   1. Log in to the server normally using your default user (e.g., `ubuntu` or `ec2-user`).
            *   >   2. Switch to the root user: `sudo -i`
            *   >   3. Create the `.ssh` directory for Mary: `mkdir -p /home/mary/.ssh`
            *   >   4. Copy the authorized keys from the default user to Mary's directory (replace `ubuntu` with `ec2-user` if needed):
            *   >      `cp /home/ubuntu/.ssh/authorized_keys /home/mary/.ssh/`
            *   >   5. Fix the ownership and permissions so SSH will accept it securely:
            *   >      *   `chown -R mary:mary /home/mary/.ssh` (Makes `mary` the actual owner, instead of `root`)
            *   >      *   `chmod 700 /home/mary/.ssh` (Secures the folder: ONLY `mary` can enter/read it)
            *   >      *   `chmod 600 /home/mary/.ssh/authorized_keys` (Secures the key file: ONLY `mary` can read/write it)
            *   >   6. Done! Now, `ssh -i linux-practicles.pem mary@<server_ip>` will connect successfully.
*   **`passwd`:** Set or change a user's password.
    *   *Example:* `sudo passwd mary` (You will be prompted to type her new password twice).
    *   *What it does:* It securely hashes (encrypts) the password and stores it in the `/etc/shadow` file. Without a password or an SSH key, Mary cannot log in at all.
*   **`userdel`:** Remove a user account.
    *   *Example:* `sudo userdel -r mary` (The `-r` removes her home directory too).

## 👥 Groups (The Teams)
Instead of giving permissions to 50 people one by one, we put them in a group.
*   **Team Analogy:** Group "DevOps" can access the server, group "Marketing" cannot.
*   **`groupadd`:** Create an empty, new group.
    *   *Example:* `sudo groupadd devops`
    *   *What it does:* Creates a new team label inside the `/etc/group` file. Right now, the team is empty.
*   **`usermod`:** Modify existing user properties (like adding them to groups).
    *   *Example:* `sudo usermod -aG devops mary`
    *   *What the flags mean:*
        *   **`-a` (Append):** CRITICAL FLAG. It means "add to this group *without* removing them from their other groups." If you forget the `-a`, Mary will be ripped out of every other team she is currently in!
        *   **`-G` (Groups):** Tells the command we are modifying the user's supplementary (secondary) groups.

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
