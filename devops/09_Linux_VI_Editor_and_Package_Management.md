# 🐧 Linux Commands & Concepts (Intermediate - Part 3)

> **File:** `09_Linux_VI_Editor_and_Package_Management.md`  
> **Topic:** Linux Revision, Bandit Practice, SSH Connectivity, VI Editor Deep Dive, File Viewing Commands, Package Management  
> **Level:** 🟡 Intermediate  
> **Prerequisites:** [08_Linux_Monitoring_Scripting_and_Permissions.md](./08_Linux_Monitoring_Scripting_and_Permissions.md)  

---
## 📌 Introduction

Welcome to **Part 3** of our Linux journey! 🚀

By now, you've learned how to navigate the file system, manage processes, and even write basic automation scripts. In this guide, we are going to bridge the gap between being a "user" and being a **DevOps professional**.

We will cover how to practice your skills using real-world challenges (Bandit), how to jump between servers like a pro (SSH), how to edit configuration files efficiently (VI Editor), and how to manage software on your servers (Package Management).

> 💡 **DevOps Tip:** In a production environment, you rarely have a "Desktop" or a mouse. The terminal is your only interface. Mastering these commands is what makes you "senior" in the eyes of your team.

---

## 📚 Table of Contents

| # | Section | Emoji |
|---|---------|-------|
| 1 | [Linux Fundamentals Quick Revision](#-linux-fundamentals-quick-revision) | 🔁 |
| 2 | [Bandit Game (Hands-on Practice)](#-bandit-game-hands-on-practice) | 🎮 |
| 3 | [Server-to-Server Connectivity (SSH)](#-server-to-server-connectivity-ssh) | 🔐 |
| 4 | [VI Editor Deep Dive](#-vi-editor-deep-dive) | ✏️ |
| 5 | [File Viewing Commands](#-file-viewing-commands) | 📖 |
| 6 | [Package Management](#-package-management) | 📦 |
| 7 | [Practice Tasks](#-practice-tasks) | 🏋️ |
| 8 | [Interview Questions](#-interview-questions) | 🎤 |
| 9 | [Summary](#-summary) | 📝 |

---

## 🔁 Linux Fundamentals Quick Revision

Before we move forward, let's quickly refresh the core concepts.

### 🔹 What is Linux?
Linux is an **Open Source** operating system kernel. Unlike Windows, anyone can see the code, modify it, and share it. This makes it incredibly secure and flexible for servers.

### 🔹 Linux Architecture
1. **Kernel:** The "Brain" that talks to the hardware (CPU, RAM, Disk).
2. **Shell:** The "Translator" that takes your commands and gives them to the kernel (e.g., Bash, Zsh).
3. **User Space:** Where your applications (Nginx, Docker, Python) run.

### 🔹 File System Hierarchy
- `/` (Root): The starting point of everything.
- `/etc`: Configuration files (where the settings live).
- `/var/log`: System and application logs (for debugging).
- `/home`: Personal folders for users.
- `/root`: The home folder for the "Superuser" (Admin).

### 🔹 Basic Navigation
- `pwd`: Where am I? (Print Working Directory)
- `ls -ltr`: Show files, newest at the bottom.
- `cd ..`: Go one step back.
- `whoami`: Which user am I logged in as?

---

## 🎮 Bandit Game (Hands-on Practice)

Learning by reading is good, but learning by **doing** is better. 

### 🔹 What is Bandit?
[OverTheWire Bandit](https://overthewire.org/wargames/bandit/) is a "Capture The Flag" (CTF) game specifically designed for Linux beginners. You start at Level 0 and use Linux commands to find "passwords" to unlock the next level.

### 🔹 Why play it?
- It teaches you how to find files with weird names.
- It teaches you how to read hidden data.
- It builds "muscle memory" for the terminal.

### 🔹 How to connect?
Open your terminal and type:
```bash
ssh bandit0@bandit.labs.overthewire.org -p 2220
```
- **Username:** `bandit0`
- **Password:** `bandit0`
- **Port:** `2220` (Standard SSH is 22, but Bandit uses 2220).

**Your task in Level 0:** Find the file named `readme` and read its content using `cat`. That is the password for `bandit1`.

---

## 🔐 Server-to-Server Connectivity (SSH)

SSH (Secure Shell) is the industry standard for logging into remote servers securely.

### 🔹 Basic Connection
```bash
ssh username@server-ip
```

### 🔹 Server-to-Server (The DevOps Way)
In a real job, you might log into **Server A**, and from there, you need to log into **Server B** to fix a database.

**🔴 Real-world Scenario:**
1. You log into the **Bastion Server** (Jump Server) from your laptop.
2. From the Bastion, you SSH into the **Private App Server**.
3. This adds a layer of security because the App Server is not directly exposed to the internet.

### 🔹 What is a Bastion Host?
A **Bastion Host** (or Jump Box) is a special-purpose server on a network specifically designed and configured to withstand attacks. It acts as the "Entrance Gate" to your private network.

### 🔹 What is a Proxy Server?
A **Proxy Server** acts as an intermediary. When your server needs to download an update from the internet but isn't allowed to talk to the internet directly, it sends the request through a Proxy.

---

## ✏️ VI Editor Deep Dive

If you are a DevOps engineer, `vi` (or `vim`) is your best friend. You will use it to edit Nginx configs, environment variables, and scripts.

### 🔹 The Two Main Modes
1. **Command Mode (Default):** Used for navigation, deleting, and saving. You can't type text here.
2. **Insert Mode:** Used for typing text. Press `i` to enter this mode.

### 🔹 Essential Shortcuts 🚀

| Command | Action |
|---------|--------|
| `i` | Enter **Insert Mode** (Start typing) |
| `Esc` | Go back to **Command Mode** |
| `:w` | **W**rite (Save) |
| `:q` | **Q**uit |
| `:wq` | Save and Quit |
| `:q!` | Quit without saving (Force quit) |
| `dd` | Delete a whole line |
| `3dd` | Delete 3 lines |
| `u` | Undo last action |
| `:set nu` | Show line numbers |
| `/text` | Search for "text" in the file |

**🔴 Real-world Example:**
You need to change the port in `app.conf`. 
1. `vi app.conf`
2. Use arrows to find the line.
3. Press `i`, change the number.
4. Press `Esc`, then type `:wq` and hit Enter. Done!

---

## 📖 File Viewing Commands

In DevOps, we spend 80% of our time reading logs. Using `cat` for a 1GB log file will crash your terminal. Use the right tool for the job.

### 🔹 `cat` (Concatenate)
Best for small files. It dumps the whole content on the screen.
```bash
cat config.txt
```

### 🔹 `more` & `less`
Best for large files. They allow you to scroll through the file.
- `less` is better because it doesn't load the whole file into RAM at once.
- Press `Space` to scroll down, `b` to go up, and `q` to quit.

### 🔹 `head` & `tail`
- `head -n 10 file.txt`: Show the **first** 10 lines.
- `tail -n 10 file.txt`: Show the **last** 10 lines.

**🔴 Production Trick: `tail -f`**
This is the most used command by DevOps engineers. 
```bash
tail -f /var/log/nginx/access.log
```
The `-f` stands for **Follow**. It shows you the logs in **real-time** as they happen. If a user hits your website, you see the line pop up instantly!

---

## 📦 Package Management

How do you install tools like Docker, Git, or Java? You use a **Package Manager**.

### 🔹 Ubuntu/Debian (`apt`)
1. **Update the list of available software:**
   ```bash
   sudo apt update
   ```
2. **Upgrade all installed software:**
   ```bash
   sudo apt upgrade
   ```
3. **Install a new tool (e.g., Git):**
   ```bash
   sudo apt install git
   ```
4. **Remove a tool:**
   ```bash
   sudo apt remove git
   ```

### 🔹 RHEL/CentOS/Amazon Linux (`yum`)
On older RedHat-based systems, we use `yum`. On newer ones, we use `dnf`.
```bash
sudo yum install httpd
```

> 💡 **Why use a Package Manager?** It automatically handles **dependencies**. If Software A needs Software B to run, the package manager will install both for you.

---

## 🏋️ Practice Tasks

### Task 1: The Bandit Challenge
1. Connect to `bandit0` using the SSH command provided above.
2. Use `ls` to find the file.
3. Use `cat` to read it.
4. Use the password you found to log into `bandit1`.

### Task 2: VI Master
1. Create a file: `vi my_notes.txt`.
2. Press `i` and write "Learning Linux for DevOps".
3. Press `Esc` and type `:set nu` to see line numbers.
4. Undo your typing using `u`.
5. Save and quit using `:wq`.

### Task 3: Log Monitoring (Simulation)
1. Run `tail -f /var/log/syslog`. (You might need `sudo`).
2. Open a second terminal window and log in/out.
3. Watch the logs change in the first window.

---

## 🎤 Interview Questions

**Q1: What is the difference between `more` and `less`?**  
**A:** `less` is faster and more memory-efficient as it doesn't load the whole file. It also allows backward navigation, unlike the basic `more`.

**Q2: How do you watch a log file in real-time?**  
**A:** Using the command `tail -f <filename>`.

**Q3: How do you quit out of the VI editor without saving changes?**  
**A:** Press `Esc`, then type `:q!`.

**Q4: What is a Bastion Host?**  
**A:** A gateway server used to provide secure access to private network servers from an external network.

**Q5: What does `sudo apt update` do?**  
**A:** It refreshes the local database of available packages from the repositories so the system knows about the newest versions. It does NOT upgrade the software.

**Q6: How do you search for a word inside a file using VI?**  
**A:** In Command Mode, type `/` followed by the word (e.g., `/database`) and hit Enter.

---

## 📝 Summary

| Command | Purpose |
|---------|---------|
| `ssh` | Connect to remote servers |
| `vi` | Edit system configuration files |
| `tail -f` | Monitor logs in real-time |
| `less` | Read large files efficiently |
| `apt install` | Install new software/tools |
| `sudo` | Run commands with Admin (root) privileges |

---
Prev : [08_Linux_Monitoring_Scripting_and_Permissions.md](08_Linux_Monitoring_Scripting_and_Permissions.md) | Next : [10_Linux_Troubleshooting_Logs_and_Services.md](10_Linux_Troubleshooting_Logs_and_Services.md)
---
