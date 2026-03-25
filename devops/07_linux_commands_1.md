# 🐧 Linux Commands & Concepts

> **File:** `07_linux_commands_1.md`  
> **Topic:** SSH Key Generation, Basic Linux Commands, System Info Commands & Important Concepts  
> **Level:** 🟢 Beginner Friendly

---

## 📌 Introduction

This file covers the **most important Linux commands** that every DevOps engineer (and even a developer) must know.

Think of Linux like the **cockpit of an airplane** — it gives you full control of the system through simple text commands. Once you know these commands, you can:

- Connect to remote servers securely (SSH)
- Create, move, copy, and delete files
- Monitor system performance
- Manage users and processes

Whether you're working on a local machine or a cloud server (like GCP, AWS, or Azure), these commands are your daily tools. Let's learn them step by step! 🚀

---

## 📚 Table of Contents

1. [SSH Key Generation and Authentication](#1-ssh-key-generation-and-authentication)
2. [Basic Linux Commands](#2-basic-linux-commands)
3. [System Information Commands](#3-system-information-commands)
4. [Important Concepts](#4-important-concepts)
5. [Practice Tasks](#5-practice-tasks)
6. [Interview Questions](#6-interview-questions)
7. [Summary](#7-summary)

---

## 1. 🔐 SSH Key Generation and Authentication

### What is SSH?

**SSH (Secure Shell)** is a way to **securely connect to another computer (or server) over the internet** — like a secret, encrypted tunnel.

> 🌍 **Real-life Example:**  
> Imagine you want to enter a high-security office building. Instead of showing an ID card (password), you have a **special digital badge** (SSH key). This badge is much harder to fake or steal.

---

### 🔑 Public Key vs Private Key — The Lock & Key Analogy

SSH uses a **pair of keys**: one public and one private.

| Key Type | What it is | Analogy |
|---|---|---|
| **Private Key** | Secret key — stays only on YOUR machine | 🗝️ Your physical house key |
| **Public Key** | Shareable key — put it on the server | 🔒 The lock on your house door |

- The **public key** is like a **lock** — you can give it to anyone (the server).
- The **private key** is like the **key to that lock** — only you should have it.

> ⚠️ **NEVER share your private key with anyone!**  
> If someone gets your private key, they can access all servers where your public key is added — just like someone stealing your house key can enter your home.

---

### 🛠️ How to Generate SSH Keys

```bash
ssh-keygen
```

Or generate a specific type (ED25519 is modern and recommended):

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

**What happens when you run this:**
1. It asks where to save the key (press Enter to use default location)
2. It asks for a passphrase (optional extra password — press Enter to skip)
3. It creates **two files** for you

---

### 📁 Where Are Keys Stored?

```
/root/.ssh/
├── id_ed25519        ← 🔴 Private Key (NEVER share this!)
└── id_ed25519.pub    ← 🟢 Public Key (safe to share)
```

```bash
# View your keys folder
ls ~/.ssh/

# View your public key (to copy to a server)
cat ~/.ssh/id_ed25519.pub
```

---

### ☁️ How Public Key is Used on a Server (GCP Example)

When you create a VM on Google Cloud Platform (GCP):

1. You generate your SSH key pair on your local machine
2. You copy your **public key** and paste it into **GCP → VM Metadata → SSH Keys**
3. GCP puts your public key inside the VM at `/home/username/.ssh/authorized_keys`
4. When you SSH into the VM, your machine uses the **private key** to prove your identity

```bash
# Connect to a GCP VM using SSH
ssh -i ~/.ssh/id_ed25519 username@<VM_EXTERNAL_IP>
```

> 🎯 **How it works behind the scenes:**  
> The server sends a random challenge → Your machine signs it with the **private key** → Server verifies it using the **public key** → Access granted! ✅

---

### 🔒 What is ED25519 Encryption?

**ED25519** is a modern encryption algorithm used to create SSH keys. Think of it as a **very complex mathematical lock** that is:

- 🚀 **Fast** — quick to generate and verify
- 🔐 **Very secure** — practically unbreakable with today's computers
- 📦 **Small** — the key is shorter but just as strong as older RSA keys

> 🧠 **Analogy:** Older locks (RSA) are like big, heavy padlocks. ED25519 is like a modern fingerprint-scan lock — smaller, faster, and much harder to break.

---

## 2. 📁 Basic Linux Commands

### 📌 `pwd` — Print Working Directory

**What it does:** Shows your current location in the file system.

```bash
pwd
# Output: /home/nishant/projects
```

> 🌍 **Real-life Example:** Like asking "Where am I right now?" on Google Maps. It shows your current address in the file system.

---

### 📌 `cd` — Change Directory

**What it does:** Moves you from one folder to another.

```bash
cd /home/nishant          # Go to specific path
cd Documents              # Go into Documents folder
cd ..                     # Go one folder back (like pressing Back)
cd ~                      # Go to your home directory
cd /                      # Go to the root (top-most) folder
```

> 🌍 **Real-life Example:** Like navigating between folders in Windows Explorer, but with keyboard instead of mouse.

---

### 📌 `mkdir` — Make Directory

**What it does:** Creates a new folder.

```bash
mkdir my_project                # Create a single folder
mkdir -p projects/app/logs      # Create nested folders in one shot
```

> `-p` flag means "create parent folders too if they don't exist"

> 🌍 **Real-life Example:** Like right-clicking → "New Folder" in Windows, but faster.

---

### 📌 `touch` — Create an Empty File

**What it does:** Creates a new empty file (or updates the timestamp of an existing file).

```bash
touch index.html
touch notes.txt config.json
```

> 🌍 **Real-life Example:** Like creating a new blank Word document without typing anything in it.

---

### 📌 `cp` — Copy

**What it does:** Copies a file or folder from one location to another.

```bash
cp file.txt backup.txt                    # Copy file
cp -r my_folder/ backup_folder/           # Copy entire folder (-r = recursive)
cp notes.txt /home/nishant/Documents/     # Copy to another location
```

> 🌍 **Real-life Example:** Like Ctrl+C and Ctrl+V — the original file stays, and a copy is made.

---

### 📌 `mv` — Move (or Rename)

**What it does:** Moves a file to another location, OR renames it.

```bash
mv old_name.txt new_name.txt             # Rename a file
mv report.txt /home/nishant/Documents/   # Move to another folder
mv my_folder/ /var/www/                  # Move entire directory
```

> 🌍 **Real-life Example:** Like Ctrl+X and Ctrl+V — the original is removed and placed at the new location.

---

### 📌 `rm` — Remove (Delete)

**What it does:** Deletes files or folders **permanently**.

```bash
rm file.txt                  # Delete a single file
rm -r my_folder/             # Delete a folder and all its contents
rm -rf old_project/          # Force delete without confirmation
```

> ⚠️ **WARNING: `rm` does NOT send files to Recycle Bin!**  
> Deleted files are **GONE FOREVER**. There is no undo.  
> **NEVER run:** `rm -rf /` (this will delete your entire system!)

> 🌍 **Real-life Example:** Like shredding important documents — once shredded, they cannot be recovered.

---

### 📌 `ls` — List

**What it does:** Shows all files and folders in the current directory.

```bash
ls            # Basic list
ls -l         # Detailed list (permissions, size, date)
ls -a         # Show hidden files (files starting with .)
ls -lh        # Detailed + human-readable file sizes
ls -la        # Detailed + hidden files
```

> 🌍 **Real-life Example:** Like opening a folder in Windows and seeing all its contents.

---

### 📌 `cat` — Concatenate / View File

**What it does:** Displays the contents of a file on the terminal.

```bash
cat notes.txt                        # View a file
cat file1.txt file2.txt              # View multiple files
cat file1.txt file2.txt > merged.txt # Merge two files into one
```

> 🌍 **Real-life Example:** Like opening a text file in Notepad to read it, but directly in the terminal.

---

### 📌 `vi` — Visual Editor (Text Editor in Terminal)

`vi` is a **powerful text editor** built into almost every Linux system. It works differently from editors like VS Code — you don't just type directly!

#### 🔄 Two Modes in vi

| Mode | What it is | How to enter |
|---|---|---|
| **Command Mode** | For navigating, saving, quitting | Default mode when vi opens |
| **Insert Mode** | For actually typing/editing text | Press `i` key |

#### 📖 Basic vi Usage

```bash
vi myfile.txt    # Open (or create) a file in vi
```

**Step-by-step:**

```
1. Run:  vi myfile.txt
2. You're in COMMAND MODE (you cannot type yet)
3. Press 'i' → Switches to INSERT MODE
4. Now type your content
5. Press 'Esc' → Returns to COMMAND MODE
6. Type ':wq' and press Enter → Save and Quit
7. Type ':q!' and press Enter → Quit WITHOUT saving
```

#### ⌨️ Common vi Commands

| Command | Action |
|---|---|
| `i` | Enter Insert mode (before cursor) |
| `Esc` | Exit Insert mode → back to Command mode |
| `:w` | Save the file |
| `:q` | Quit vi |
| `:wq` | Save and Quit |
| `:q!` | Quit without saving (force) |
| `dd` | Delete the current line |
| `yy` | Copy (yank) the current line |
| `p` | Paste below current line |
| `/word` | Search for a word |

> 🌍 **Real-life Example:** Imagine a text editor where you have two modes: "Reading Mode" (Command) and "Writing Mode" (Insert). You always start in Reading Mode and must switch to Writing Mode to type. It feels strange at first, but becomes very fast with practice!

---

## 3. 💻 System Information Commands

### 🤔 Why `-h` (Human-Readable)?

Many commands output sizes in **bytes** by default, which is hard to read.  
Adding `-h` flag converts them to **KB, MB, GB** — much easier to understand!

```
Without -h:  1073741824
With -h:     1.0G
```

---

### 📌 `hostname` — Show Machine Name

```bash
hostname
# Output: my-linux-server
```
> Tells you the name of your computer/server. Like a name tag for your machine.

---

### 📌 `hostname -I` — Show IP Address

```bash
hostname -I
# Output: 192.168.1.105
```
> Shows the **internal (private) IP address** of your machine — the address on your local network.

---

### 📌 `curl ifconfig.me` — Show Public IP Address

```bash
curl ifconfig.me
# Output: 103.21.244.0
```
> Shows your **public (external) IP address** — the one the internet sees.

> 🌍 **Analogy:** `hostname -I` = your home address within your apartment complex. `curl ifconfig.me` = the main gate address of the entire complex.

---

### 📌 `uname` — Unix Name / OS Information

```bash
uname         # Shows kernel name
# Output: Linux

uname -a      # Shows all system info
# Output: Linux my-server 5.15.0 #1 SMP x86_64 GNU/Linux
```

> `uname -a` = everything about your operating system: kernel name, hostname, version, architecture, etc.

---

### 📌 `who` — Show Logged-In Users

```bash
who
# Output:
# nishant  pts/0  2025-03-24 10:30 (192.168.1.10)
```
> Shows **who is currently logged into the system** — useful on shared servers.

---

### 📌 `w` — Show Who is Logged In + What They're Doing

```bash
w
# Output shows: user, login time, idle time, what command they're running
```
> Like `who` but with extra info — it also shows **what each user is currently doing**.

---

### 📌 `whoami` — Show Current User

```bash
whoami
# Output: nishant
```
> Tells you which user you are currently logged in as.

> 🌍 **Real-life Example:** Like asking "What is my username right now?" — very useful when switching between users.

---

### 📌 `uptime` — How Long System Has Been Running

```bash
uptime
# Output: 14:30:01 up 3 days, 2:15, 2 users, load average: 0.12, 0.08, 0.05
```

| Part | Meaning |
|---|---|
| `14:30:01` | Current time |
| `up 3 days, 2:15` | System running for 3 days and 2 hours 15 minutes |
| `2 users` | 2 users logged in |
| `load average` | CPU load in last 1, 5, 15 minutes |

> 🌍 **Real-life Example:** Like checking how long your laptop has been on since the last restart.

---

### 📌 `top` — Live Process Monitor

```bash
top
```
> Shows a **live, real-time view** of all running processes, CPU usage, memory usage.

> 🌍 **Real-life Example:** Like opening **Task Manager** in Windows. Press `q` to quit.

**Key columns in `top`:**
- `PID` — Process ID
- `%CPU` — How much CPU the process is using
- `%MEM` — How much memory
- `COMMAND` — The name of the program

---

### 📌 `free -h` — Show Memory (RAM) Usage

```bash
free -h
# Output:
#               total    used    free    shared
# Mem:           7.7G    3.2G    4.5G       128M
# Swap:          2.0G    0.0B    2.0G
```

> `-h` = human-readable (shows GB/MB instead of raw bytes).

> 🌍 **Real-life Example:** Like checking how much RAM is being used vs. available on your computer. **Swap** is virtual memory that uses disk space when RAM is full.

---

### 📌 `df -h` — Show Disk Space Usage

```bash
df -h
# Output:
# Filesystem      Size  Used Avail Use% Mounted on
# /dev/sda1        50G   18G   32G  36% /
```

> Shows how much **disk storage** is used and available on each partition.

> `-h` = human-readable sizes.

> 🌍 **Real-life Example:** Like checking how much space is left on your hard drive before downloading a large file.

---

### 📌 `history` — Show Command History

```bash
history
# Output:
#   1  ls
#   2  cd /var/log
#   3  cat error.log
#   498  ssh-keygen
#   499  history
```

> Shows the **last ~500 commands** you typed.

```bash
history | grep ssh       # Search history for commands with "ssh"
!3                       # Re-run command number 3 from history
!!                       # Re-run the last command
```

> 🌍 **Real-life Example:** Like browser history, but for your terminal commands.

---

## 4. 💡 Important Concepts

### 🧟 Zombie Process

#### What is it?

A **zombie process** is a process that has **finished running but is still listed in the process table** because its parent process hasn't acknowledged (collected) its exit status yet.

> 🧟 **Real-life Analogy:**  
> Imagine an employee (child process) finishes their work and submits a **completion report** to their manager (parent process). But the manager is too busy to read the report. Until the manager reads and acknowledges the report, the employee is stuck in a "done but not officially closed" state — that's a zombie!

#### Key Facts:

| Fact | Detail |
|---|---|
| State | Shows as `Z` (Zombie) in `top` or `ps` |
| Memory | Uses almost NO memory or CPU |
| Problem | If too many accumulate, they fill up the process table |
| Fix | Fix the parent process to properly collect exit status (using `wait()`) |

```bash
# See zombie processes
ps aux | grep 'Z'

# View all processes including zombies
top   # Look for 'zombie' count at the top
```

> ⚠️ Unlike a stuck/frozen process, you **cannot kill a zombie** with `kill -9`. You have to fix or kill the parent process.

---

### ✏️ vi Editor Modes (Recap)

The most confusing thing for beginners about `vi` is the **two-mode system**.

```
┌─────────────────────────────────────────────┐
│                                             │
│   COMMAND MODE          INSERT MODE         │
│   (Default)             (Typing mode)       │
│                                             │
│   Navigate, save,   ←→  Actually write      │
│   delete, copy          and edit text       │
│                                             │
│   Press 'i' to go →     Press 'Esc' to ←   │
│   to Insert Mode         return here        │
│                                             │
└─────────────────────────────────────────────┘
```

| Mode | You can... | You cannot... |
|---|---|---|
| **Command Mode** | Navigate, save (`:w`), quit (`:q`), delete line (`dd`) | Type letters as text |
| **Insert Mode** | Type and edit text freely | Run vi commands |

> ✅ **Golden Rule:** If you're confused, press `Esc` first. This always returns you to Command Mode and resets your state.

---

## 5. 🏋️ Practice Tasks

Try these tasks on a Linux terminal (or GCP VM) to solidify your learning:

### Task 1: SSH Key Setup
```bash
# 1. Generate an SSH key
ssh-keygen -t ed25519 -C "mytest@example.com"

# 2. View your keys
ls ~/.ssh/

# 3. Print your public key
cat ~/.ssh/id_ed25519.pub
```

---

### Task 2: File & Folder Operations
```bash
# 1. Go to your home directory
cd ~

# 2. Create a project structure
mkdir -p devops_practice/logs devops_practice/configs

# 3. Create some files
touch devops_practice/logs/app.log
touch devops_practice/configs/settings.txt

# 4. List the structure
ls -lR devops_practice/

# 5. Copy a file
cp devops_practice/configs/settings.txt devops_practice/configs/settings_backup.txt

# 6. Rename a file
mv devops_practice/configs/settings.txt devops_practice/configs/app_settings.txt

# 7. View what's in the directory now
ls -la devops_practice/configs/

# 8. Delete the backup file
rm devops_practice/configs/settings_backup.txt
```

---

### Task 3: System Information Check
```bash
# 1. Where am I?
pwd

# 2. Who am I?
whoami

# 3. What is my hostname and IP?
hostname
hostname -I

# 4. How long has the system been running?
uptime

# 5. How much RAM is free?
free -h

# 6. How much disk space is left?
df -h

# 7. What OS/kernel am I running?
uname -a

# 8. Who else is logged in?
who
```

---

### Task 4: vi Editor Practice
```bash
# 1. Open a new file in vi
vi my_first_vi_file.txt

# 2. Press 'i' to enter Insert Mode
# 3. Type:  Hello, this is my first vi file!
# 4. Press Esc to go back to Command Mode
# 5. Type :wq and press Enter to save and quit

# 6. Verify the file was saved
cat my_first_vi_file.txt

# 7. Re-open and edit it
vi my_first_vi_file.txt
# Press 'i', add a new line, press Esc
# Type :wq to save
```

---

### Task 5: Command History
```bash
# 1. View your command history
history

# 2. Search history for a specific command
history | grep mkdir

# 3. Re-run the last command
!!
```

---

## 6. 🎤 Interview Questions

### Q1. What is SSH and why is it used?
> **Answer:** SSH (Secure Shell) is a protocol used to **securely connect to a remote computer over the internet**. It encrypts all communication so no one can eavesdrop. It's used by DevOps engineers to access and manage cloud servers remotely.

---

### Q2. What is the difference between a public key and a private key?
> **Answer:** They work as a **pair**. The **public key** is like a lock — you put it on the server and it can be shared openly. The **private key** is the key to that lock — it stays only on your machine and must **never be shared**. Only someone with the correct private key can unlock (authenticate with) the server.

---

### Q3. What does `pwd` command do?
> **Answer:** `pwd` stands for **Print Working Directory**. It shows your **current location** in the file system. Example: `/home/nishant/projects`.

---

### Q4. What is the difference between `cp` and `mv`?
> **Answer:**  
> - `cp` = **Copy** — copies a file but the original remains (like Ctrl+C, Ctrl+V)  
> - `mv` = **Move** — moves the file to a new location, the original is removed (like Ctrl+X, Ctrl+V). `mv` is also used to **rename** files.

---

### Q5. What does `rm -rf` do and why is it dangerous?
> **Answer:** `rm -rf` **forcefully and recursively deletes** a file or directory and all its contents **permanently** — with no confirmation and no Recycle Bin. It's dangerous because there is **no undo**. Running `rm -rf /` would delete the entire file system.

---

### Q6. What is a zombie process?
> **Answer:** A zombie process is a process that has **finished executing** but still has an entry in the process table because its **parent process hasn't read its exit status** yet. It uses no resources but can cause issues if too many accumulate. It shows as status `Z` in `ps` or `top`.

---

### Q7. What are the two modes in the vi editor?
> **Answer:**  
> - **Command Mode** (default): Used for navigation, saving, deleting. You cannot type text directly.  
> - **Insert Mode**: Used for typing and editing text. Enter by pressing `i`, exit by pressing `Esc`.

---

### Q8. What is the difference between `hostname -I` and `curl ifconfig.me`?
> **Answer:**  
> - `hostname -I` = shows your **private/local IP** (visible only within your network)  
> - `curl ifconfig.me` = shows your **public IP** (the IP the internet sees)

---

### Q9. What does `free -h` and `df -h` show? What does `-h` mean?
> **Answer:**  
> - `free -h` shows **RAM (memory) usage** — total, used, and free  
> - `df -h` shows **disk space usage** on each partition  
> - `-h` stands for **human-readable** — it converts raw byte numbers to KB/MB/GB, making it much easier to read.

---

### Q10. What is ED25519 encryption?
> **Answer:** ED25519 is a **modern cryptographic algorithm** used to generate SSH keys. It creates keys that are **small, fast, and extremely secure**. It's recommended over older algorithms like RSA because it offers the same (or better) security with shorter key lengths and better performance.

---

## 7. 📝 Summary

Here's a quick recap of everything covered:

| Topic | Key Takeaway |
|---|---|
| **SSH Keys** | Public key = lock (on server). Private key = your key (never share!). |
| **ssh-keygen** | Generates a public/private key pair stored in `~/.ssh/` |
| **ED25519** | Modern, secure, fast encryption algorithm for SSH keys |
| **pwd** | Shows current directory location |
| **cd** | Navigate between directories |
| **mkdir** | Create new directories (use `-p` for nested) |
| **touch** | Create empty files |
| **cp** | Copy files/folders (original stays) |
| **mv** | Move or rename files/folders (original moves) |
| **rm** | Delete permanently — no undo! |
| **ls** | List contents of a directory |
| **cat** | View file contents |
| **vi** | Terminal text editor — has Command Mode and Insert Mode |
| **hostname** | Machine name; `-I` shows private IP |
| **curl ifconfig.me** | Shows public IP address |
| **uname -a** | Full OS and kernel information |
| **who / w / whoami** | Show logged-in users and current user |
| **uptime** | How long the system has been running |
| **top** | Live process/resource monitor (like Task Manager) |
| **free -h** | RAM usage in human-readable format |
| **df -h** | Disk space usage in human-readable format |
| **history** | List of recent commands |
| **Zombie Process** | Finished process not yet collected by parent; shows as `Z` |

---

> 💡 **Pro Tips:**
> - Always use `ls -lh` to view files with sizes in a readable format.
> - Use `history | grep <command>` to search for a previously used command.
> - When in doubt in `vi`, press `Esc` first!
> - Never run `rm -rf` without double-checking the path first.

---

← Previous: [06_linux/01_what_is_operating_system.md](06_linux/01_what_is_operating_system.md) | Next: [08_linux_commands_2](08_linux_commands_2.md)
