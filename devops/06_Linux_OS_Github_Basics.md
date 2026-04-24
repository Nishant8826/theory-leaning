# 🖥️ Linux, OS & GitHub Basics

---

## 📌 1. What is an Operating System (OS)?

An **Operating System (OS)** is software that manages hardware resources and provides an interface for users and applications.

> **Analogy:** Customer (You) → Waiter (OS) → Kitchen (Hardware). The OS takes your order and tells the hardware what to do.

### Core Functions

| Function | What It Does |
|----------|-------------|
| **Resource Management** | Decides which app gets how much CPU/RAM |
| **File Management** | Tracks where files are stored |
| **Process Management** | Runs multiple apps simultaneously (multitasking) |
| **Security** | Ensures users can't access each other's data |
| **Interface** | GUI (Windows/Mac) or CLI (Linux terminal) |

### DevOps Perspective

- **Windows/Mac** → Writing code, meetings, local development
- **Linux** → Running servers, databases, deployment pipelines, containers

---

## 📌 2. What is Linux?

**Linux** is a free, open-source OS kernel created by **Linus Torvalds in 1991** as a free alternative to UNIX.

### Kernel vs Distribution

- **Kernel** = The core "brain" — manages hardware (CPU, memory, devices)
- **Distribution (Distro)** = Kernel + tools + package manager + desktop (optional)

> **Analogy:** Kernel = car engine. Distro = full car (seats, steering, AC). Same engine, different car brands.

| Distro | Best For | Package Manager |
|--------|----------|----------------|
| **Ubuntu** | Beginners, cloud servers | `apt` |
| **CentOS / Rocky Linux** | Enterprise servers | `yum` / `dnf` |
| **Debian** | Stability-focused servers | `apt` |
| **Red Hat (RHEL)** | Enterprise (paid support) | `yum` / `dnf` |
| **Alpine** | Docker containers (tiny ~5MB) | `apk` |

### Linux vs UNIX

| Feature | UNIX (1969) | Linux (1991) |
|---------|-------------|-------------|
| **Origin** | AT&T Bell Labs | Linus Torvalds / Community |
| **Cost** | Expensive licensing | Free / Open Source |
| **Portability** | Tied to specific hardware | Runs on everything (phones to clouds) |
| **Usage Today** | Banks, mainframes (legacy) | Modern internet, DevOps, startups |

> **Fun Fact:** macOS is UNIX-based — that's why Mac terminals look like Linux terminals!

### Why Linux Matters

- **90% of the world's servers** run Linux (including AWS, Google, Facebook)
- **Docker, Kubernetes, Jenkins, Terraform** — all built for Linux
- Learning Linux = essential for any DevOps career

---

## 📌 3. Open Source & Why Linux Dominates

### What is Open Source?

**Open Source** = Source code is publicly available for anyone to view, modify, and distribute.

> **Analogy:** Closed Source (Windows) = secret restaurant recipe. Open Source (Linux) = community potluck where everyone shares and improves the recipe.

| Feature | Open Source | Proprietary (Closed) |
|---------|-----------|---------------------|
| **Transparency** | You can read the code | Black box |
| **Bug Fixing** | Community fixes in hours | Wait for company's next update |
| **Cost** | Usually free | Paid licensing |
| **Vendor Lock-in** | None — switch freely | Locked to one company |

> **Note:** "Free" in open source = **Freedom** (free as in speech), not just $0 (free as in beer).

### Why Linux Dominates Servers

| Reason | Explanation |
|--------|------------|
| 🔒 **Security** | Strict permissions model, far fewer viruses than Windows |
| ⚡ **Efficiency** | Runs without GUI — a server needs only 512MB RAM (Windows needs 2–4GB) |
| 🛠️ **Stability** | Can run 500+ days without a reboot |
| 🐚 **CLI Power** | Everything scriptable — deploy 1000 servers with one script |
| 💰 **Free** | No licensing costs — saves thousands annually |

### Popular Open Source DevOps Tools

- **OS:** Linux (Ubuntu, Debian, CentOS)
- **Web Servers:** Apache, Nginx (powers 70% of internet)
- **Databases:** MySQL, PostgreSQL, MongoDB
- **DevOps:** Docker, Kubernetes, Jenkins, Terraform, Ansible

---

## 📌 4. Linux vs Windows

| Feature | Windows | Linux |
|---------|---------|-------|
| **Built For** | Desktop (GUI, ease of use) | Servers (CLI, automation) |
| **Command Line** | PowerShell / CMD | Bash / Zsh (industry standard) |
| **Cost** | $$$ (Licensing) | Free |
| **File Paths** | `C:\Users\Nishant` | `/home/nishant` |
| **Case Sensitivity** | `File.txt` = `file.txt` (SAME) | `File.txt` ≠ `file.txt` (DIFFERENT!) |
| **Updates** | Forced reboots required | Live patching, no reboot needed |
| **Resources** | Heavy (needs lots of RAM/CPU) | Lightweight (runs on minimal hardware) |
| **Separator** | Backslash `\` | Forward Slash `/` |
| **Drives** | `C:\`, `D:\`, `E:\` | Everything from single root `/` |

> **2 AM Scenario:** Windows Server says "I need to reboot for updates" (website goes down). Linux Server updates kernel while serving users (website stays up).

### DevOps Tip

Don't switch your laptop to Linux! Keep Windows and use **WSL**, **Docker**, or a **Cloud VM** to run Linux inside it.

---

## 📌 5. Linux File System

In Linux, everything starts from a single point: **The Root (`/`)**. No C: or D: drives.

### Directory Structure

| Folder | Purpose | Analogy |
|--------|---------|---------|
| `/` | Root — starting point of everything | Building foundation |
| `/bin` | Essential user commands (`ls`, `cp`, `cat`) | Basic tools |
| `/sbin` | System admin commands (`fdisk`, `reboot`) | Admin-only tools |
| `/etc` | Configuration files | Electrical switchboard (settings) |
| `/home` | User home directories (`/home/nishant`) | Your personal bedroom |
| `/root` | Root (admin) user's home | Landlord's private office |
| `/var` | Variable data (logs, caches, mail) | Garbage room + logbook |
| `/var/log` | System and application logs | CCTV recordings |
| `/tmp` | Temporary files (wiped on reboot) | Scratchpad |
| `/usr` | Installed programs and libraries | App store |
| `/dev` | Device files (hard drive, USB, keyboard) | Hardware connectors |
| `/proc` | Process/system info (virtual files) | Live health monitor |
| `/opt` | Optional/third-party software | Extension room |

### Key Concept: "Everything is a File"

In Linux, almost everything is represented as a file:
- `/dev/sda` → your hard drive
- `/proc/cpuinfo` → CPU information
- `/dev/null` → the "black hole" (discards data)

This means you can use the same tools (`cat`, `grep`, `ls`) to inspect anything.

---

## 📌 6. Users, Permissions & Shell Basics (NEW)

### Users in Linux

| User Type | Who | Home Directory | Power |
|-----------|-----|---------------|-------|
| **root** | Superuser / Admin | `/root` | Can do ANYTHING |
| **Regular user** | Normal user (e.g., `nishant`) | `/home/nishant` | Limited access |
| **Service user** | Apps like nginx, mysql | Varies | Runs specific services |

```
whoami          # Who am I?
sudo <command>  # Run as root (Super User DO)
su - root       # Switch to root user
```

### File Permissions

Every file has 3 permission types for 3 user groups:

```
-rwxr-xr--  1  nishant  devops  4096  Jan 10 10:00  script.sh
 │││ │││ │││
 │││ │││ └── Others: r-- (read only)
 │││ └───── Group:  r-x (read + execute)
 └──────── Owner:  rwx (read + write + execute)
```

| Symbol | Permission | Number |
|--------|-----------|--------|
| `r` | Read | 4 |
| `w` | Write | 2 |
| `x` | Execute | 1 |

```bash
chmod 755 script.sh    # Owner=rwx, Group=r-x, Others=r-x
chmod 644 config.txt   # Owner=rw-, Group=r--, Others=r--
chown nishant file.txt # Change file owner
```

### Shell Types

A **shell** is the program that interprets your commands.

| Shell | Description |
|-------|------------|
| **Bash** | Default on most Linux distros — industry standard |
| **Zsh** | Enhanced Bash with better autocomplete (default on macOS) |
| **sh** | Original basic shell — used in scripts for portability |

```bash
echo $SHELL    # See your current shell
cat /etc/shells # List all available shells
```

---

## 📌 7. Linux Commands Overview

### Navigation

| Command | Purpose | Example |
|---------|---------|---------|
| `pwd` | Print working directory | `pwd` → `/home/nishant` |
| `ls` | List files (`-la` for details + hidden) | `ls -la` |
| `cd` | Change directory | `cd /var/log` |

### File Operations

| Command | Purpose | Example |
|---------|---------|---------|
| `mkdir` | Create folder (`-p` for nested) | `mkdir -p app/logs` |
| `touch` | Create empty file | `touch error.log` |
| `cp` | Copy | `cp file.txt backup/` |
| `mv` | Move or rename | `mv old.txt new.txt` |
| `rm` | Delete (**⚠️ USE WITH CAUTION!**) | `rm -rf temp/` |

### Reading Files

| Command | Purpose | Example |
|---------|---------|---------|
| `cat` | See whole file | `cat config.yml` |
| `head` / `tail` | First/last 10 lines | `tail -20 error.log` |
| `grep` | Search text in file (**most used!**) | `grep "ERROR" app.log` |
| `less` | Scroll through large files | `less big_file.log` |

### System Info

| Command | Purpose | Example |
|---------|---------|---------|
| `top` / `htop` | Live CPU/RAM usage | `htop` |
| `df -h` | Disk space usage | `df -h` |
| `free -m` | Available RAM | `free -m` |
| `whoami` | Current username | `whoami` |
| `uname -a` | OS/kernel info | `uname -a` |

### Windows ↔ Linux Command Map

| Goal | Windows (CMD) | Linux (Bash) |
|------|--------------|-------------|
| List files | `dir` | `ls` |
| Clear screen | `cls` | `clear` |
| Copy file | `copy` | `cp` |
| Show IP | `ipconfig` | `ip a` or `ifconfig` |

### Keyboard Shortcuts (Must Know!)

| Shortcut | Action |
|----------|--------|
| **TAB** | Auto-complete filenames (saves hours!) |
| **↑ Arrow** | Previous command |
| **Ctrl + C** | Stop/kill running command |
| **Ctrl + L** | Clear screen |
| **Ctrl + R** | Search command history |

### Practice: Prepare a Log Directory

```bash
mkdir -p my_app/logs                            # Create nested folders
cd my_app/logs && pwd                           # Navigate and verify
touch error.log access.log                      # Create log files
echo "ERROR: DB connection failed at 12:00" >> error.log  # Add content
echo "ERROR: Password incorrect at 12:05" >> error.log
grep "12:05" error.log                          # Search specific error
```

> ⚠️ **Common Mistakes:** `rm -rf /` deletes ENTIRE system. Wrong case (`Document` vs `Documents`). Avoid spaces in filenames (use `my_file.txt`).

---

## 📌 8. Ways to Run Linux

You don't need to delete Windows. Multiple options:

| Method | Speed | Resource Usage | Best For |
|--------|-------|---------------|----------|
| **WSL** (Windows Subsystem for Linux) | Instant | Very Low | Daily Linux practice on Windows 10/11 |
| **Docker** (`docker run -it ubuntu`) | Instant (3 sec) | Extremely Low | Quick testing, microservices |
| **Virtual Machine** (VirtualBox/VMware) | Slow | High (needs lots of RAM) | Testing full OS features |
| **Cloud VM** (AWS/GCP/Azure) | Fast | Scalable | Production servers, 24/7 uptime |

### Creating a Linux VM on GCP (Free Tier)

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Navigate to **Compute Engine → VM Instances**
3. Click **Create Instance**:
   - Name: `my-linux-server`
   - Region: near you (e.g., `us-central1`)
   - Machine Type: **`e2-micro`** (free tier!)
   - Boot Disk: **Ubuntu 22.04 LTS**
4. Check **"Allow HTTP traffic"** under Firewall
5. Click **Create** → Wait ~1 minute
6. Click **SSH** button → you're inside a Linux server!

> ⚠️ **Always Stop/Delete** your instance when done practicing to avoid bills!

| Feature | Local VM (VirtualBox) | Cloud VM (GCP) |
|---------|----------------------|----------------|
| **External Access** | Hard to access from outside | Public IP, accessible worldwide |
| **Resources** | Uses your laptop's RAM/battery | Uses Google's data centers |
| **Uptime** | Stops when laptop closes | Runs 24/7 |

---

## 📌 9. Package Managers (NEW)

A **package manager** installs, updates, and removes software on Linux — like an app store for the terminal.

### apt (Ubuntu/Debian)

```bash
sudo apt update                  # Refresh package list
sudo apt install nginx           # Install a package
sudo apt remove nginx            # Remove a package
sudo apt upgrade                 # Upgrade all packages
```

### yum / dnf (CentOS/RHEL)

```bash
sudo yum update                  # Refresh + upgrade packages
sudo yum install httpd           # Install a package
sudo yum remove httpd            # Remove a package
```

| Feature | apt (Ubuntu/Debian) | yum/dnf (CentOS/RHEL) |
|---------|--------------------|-----------------------|
| **Config file** | `/etc/apt/sources.list` | `/etc/yum.repos.d/` |
| **Package format** | `.deb` | `.rpm` |
| **Update command** | `apt update && apt upgrade` | `yum update` |

> **DevOps Tip:** Always run `apt update` before `apt install` — otherwise you might install outdated versions!

---

## 📌 10. Git & GitHub Basics

### What is Git?

**Git** = A version control tool that tracks every change to your code. If you make a mistake, go back in time.

### What is GitHub?

**GitHub** = A cloud platform where you store Git repositories online for collaboration and backup.

> **Analogy:** Git = the "save game" system. GitHub = the cloud where everyone stores and shares their saves.

| Tool | Purpose | Location |
|------|---------|----------|
| **Git** | Tracks version history | Local (your PC) |
| **GitHub** | Stores/shares work online | Cloud (github.com) |

### Core Concepts

| Concept | What It Does | Command |
|---------|-------------|---------|
| **Repository (Repo)** | Project folder tracked by Git | `git init` |
| **Clone** | Copy a remote repo to your machine | `git clone <url>` |
| **Add** | Stage files for commit | `git add .` |
| **Commit** | Save a snapshot with a message | `git commit -m "fixed bug"` |
| **Push** | Send local commits to GitHub | `git push origin main` |
| **Pull** | Get latest changes from GitHub | `git pull origin main` |
| **Branch** | Parallel version of code | `git checkout -b feature` |

### Why DevOps Engineers Need Git/GitHub

1. **Collaboration** — 10 engineers work on the same script without conflicts
2. **Recovery** — accidentally deleted a file? `git checkout` restores it
3. **CI/CD** — push code → GitHub triggers automatic deployment
4. **Audit** — every change is tracked: who changed what, when, why

---

## 🔍 Scenario-Based Q&A

### Scenario 1: Choosing the Right OS for a Web Server
Budget is tight, need to host a high-traffic e-commerce site.

✅ **Answer:** Use **Linux (Ubuntu Server)**. It's free (no licensing), lightweight (less RAM needed), stable (years without reboot), and all DevOps tools (Docker, Nginx, K8s) are built for it. Saves thousands annually.

---

### Scenario 2: The Case-Sensitivity Trap
Code references `Config.json` but actual file on Linux server is `config.json`. App crashes.

✅ **Answer:** Linux is **case-sensitive**. Best practice: use all lowercase with underscores (`app_config.json`).

---

### Scenario 3: Lost Code Recovery
Junior dev deletes critical config file from production. No backup on server.

✅ **Answer:** Since team uses Git/GitHub, run `git checkout HEAD -- config/production.yml` to restore. Every version is preserved in Git history.

---

### Scenario 4: Quick Linux Environment Needed
Intern's Windows laptop can't handle VirtualBox.

✅ **Answer:** (1) **WSL** — Linux natively in Windows 10/11. (2) **Docker** — `docker run -it ubuntu` in 3 seconds. (3) **GCP Free Tier** — cloud VM, SSH from browser.

---

## 🎤 Interview Q&A

### Q1: What is an Operating System and why is it needed?
> **Answer:** An OS manages hardware resources (CPU, RAM, disk) and provides an interface for users/applications. It handles resource management, file systems, process scheduling, security, and user interface (GUI or CLI).

### Q2: Why is Linux preferred over Windows for servers?
> **Answer:** (1) **Free** — no licensing, (2) **Lightweight** — runs without GUI, minimal RAM, (3) **Stable** — years without reboot, (4) **Secure** — strict permissions, fewer viruses, (5) **Automation-friendly** — everything via CLI. 90% of cloud servers run Linux.

### Q3: What is the difference between the Linux Kernel and a Distribution?
> **Answer:** **Kernel** = core brain managing hardware. **Distro** = kernel + package manager + tools + optional desktop. Same kernel, different packaging (Ubuntu = beginner-friendly, CentOS = enterprise, Alpine = tiny containers).

### Q4: What is the difference between Git and GitHub?
> **Answer:** **Git** = local version control tool (tracks changes, branching, merging). **GitHub** = cloud platform for hosting Git repos (collaboration, PRs, CI/CD). Git is the engine; GitHub is the garage.

### Q5: What does "Everything is a file" mean in Linux?
> **Answer:** Everything is represented as a file — regular files, directories, devices (`/dev/sda` = hard drive), processes (`/proc/cpuinfo` = CPU info). Same tools (`cat`, `grep`) work on all of them.

### Q6: Explain the Linux file system hierarchy.
> **Answer:** Hierarchical tree from `/` (root). Key: `/etc` (config), `/home` (users), `/var/log` (logs), `/tmp` (temporary), `/bin` (commands), `/usr` (programs). Logs at `/var/log/syslog`, `/var/log/nginx/error.log`.

### Q7: VM vs Docker Container vs Cloud VM?
> **Answer:** **VM** = full OS with own kernel, heavy, slow to start. **Docker Container** = shares host kernel, lightweight, starts in seconds. **Cloud VM** = VM in remote data center (AWS/GCP), accessible via internet, runs 24/7.

### Q8: What is Open Source? Why important for DevOps?
> **Answer:** Source code publicly available to view/modify/distribute. Important because: most DevOps tools are open source (Docker, K8s, Jenkins), no vendor lock-in, community fixes bugs in hours, no licensing fees.

### Q9: What is the difference between `apt` and `yum`?
> **Answer:** Both are package managers. **apt** is used on Debian/Ubuntu (`.deb` packages), **yum/dnf** on CentOS/RHEL (`.rpm` packages). Same purpose, different Linux families.

### Q10: What are Linux file permissions? Explain `chmod 755`.
> **Answer:** Every file has read(4), write(2), execute(1) permissions for owner, group, and others. `chmod 755` = Owner gets rwx (7), Group gets r-x (5), Others get r-x (5). The file is readable/executable by all but only writable by the owner.

---

## 📝 Summary

| Concept | Key Takeaway |
|---------|-------------|
| **Operating System** | Middleman between you and hardware — manages resources, files, security |
| **Linux** | Free, open-source, stable — runs 90% of the world's servers |
| **Kernel vs Distro** | Kernel = engine; Distro = full car (Ubuntu, CentOS, Debian, Alpine) |
| **Open Source** | Free to use/modify/share — powers the entire DevOps ecosystem |
| **Linux vs Windows** | Linux = server king (CLI, free, lightweight). Windows = desktop king (GUI) |
| **File System** | Everything from `/` — no C:/D: drives. Everything is a file |
| **Permissions** | rwx for owner/group/others. `chmod` to change, `chown` to change owner |
| **Package Managers** | `apt` (Ubuntu) / `yum` (CentOS) — install/update/remove software |
| **Ways to Run Linux** | WSL (easiest), Docker (fastest), VM (full OS), Cloud (production) |
| **Git** | Local version control — tracks every code change ("time machine") |
| **GitHub** | Cloud platform for sharing/collaborating on Git repos |

---

← Previous: [05_DevOps_Basics_Tools_and_Roles.md](05_DevOps_Basics_Tools_and_Roles.md) | Next: [07_Linux_SSH_and_Basic_Commands.md](07_Linux_SSH_and_Basic_Commands.md) →
