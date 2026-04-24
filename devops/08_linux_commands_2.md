# 🐧 Linux Commands & Concepts (Intermediate - Part 2)

> **Level:** 🟡 Intermediate  
> **Prerequisites:** [07_linux_commands_1.md](./07_linux_commands_1.md)  
> **Topics:** System Monitoring · Process Management · TAR · Shell Scripting · Permissions · User & Group Management

---

## 📌 Introduction

Welcome back! 🎉

In Part 1, you learned the **basics of Linux** — how to navigate files, SSH into servers, and use common commands.

In **Part 2**, we go deeper into the topics that **DevOps engineers use every single day on production servers**:

- 👀 Watching what's happening on a server in real-time
- 🛑 Managing and killing stuck processes
- 📦 Compressing and archiving log files
- 🤖 Automating tasks with shell scripts
- 🔐 Controlling who can read, write, or execute files
- 👤 Managing users and groups on a multi-user server

> 💡 **Think of yourself as a server admin.** Your job is to keep the server healthy, secure, and running smoothly. These commands are your toolbox.

---

## 📚 Table of Contents

| # | Section | Emoji |
|---|---------|-------|
| 1 | [System Monitoring Commands](#-system-monitoring-commands) | 💻 |
| 2 | [Process Management](#-process-management) | ⚙️ |
| 3 | [File Compression (TAR)](#-file-compression-tar) | 📦 |
| 4 | [Shell Scripting](#-shell-scripting) | 🧾 |
| 5 | [File Permissions](#-file-permissions) | 🔐 |
| 6 | [User Management](#-user-management) | 👤 |
| 7 | [Group Management](#-group-management) | 👥 |
| 8 | [Advanced User Management](#-advanced-user-management) | 🔒 |
| 9 | [Practice Tasks](#-practice-tasks) | 🏋️ |
| 10 | [Interview Questions](#-interview-questions) | 🎤 |
| 11 | [Summary](#-summary) | 📝 |

---

## 💻 System Monitoring Commands

> 🏥 **Real-life analogy:** Just like a doctor monitors a patient's heartbeat, blood pressure, and temperature — a DevOps engineer monitors a server's CPU, memory, and disk usage. These commands are your **stethoscope**.

---

### 🔹 `top` — Real-Time System Dashboard

```bash
top
```

**What it does:**
Gives you a **live, auto-refreshing view** of your system — what processes are running, how much CPU and memory they're using.

**Key output fields:**

```
top - 10:30:01 up 3 days,  2:15,  2 users,  load average: 0.25, 0.40, 0.38
Tasks: 198 total,   1 running, 197 sleeping,   0 stopped,   0 zombie
%Cpu(s):  5.5 us,  2.1 sy,  0.0 ni, 91.8 id,  0.4 wa
MiB Mem :   7951.2 total,   1234.5 free,   4200.1 used,   2516.6 buff/cache
```

| Field | Meaning |
|-------|---------|
| `up 3 days` | Server has been running for 3 days without restart |
| `load average` | How busy the CPU is (1m, 5m, 15m average) |
| `us` | CPU used by user programs |
| `id` | CPU that is idle (free) |
| `wa` | CPU waiting for disk/network (high = disk issue) |
| `MiB Mem` | Total, free, and used RAM |

**How to use it:**
- Press `q` to quit
- Press `k` to kill a process (enter the PID)
- Press `M` to sort by memory usage
- Press `P` to sort by CPU usage

**🔴 Real-world DevOps example:**
> A user reports the app is slow. You SSH into the server and run `top`. You see **Java** is using 98% CPU. You note its PID and investigate further.

---

### 🔹 `htop` — Colored, Interactive Version of top

```bash
htop
```

**What it does:**
Same as `top` but with **colors, mouse support, and easier navigation**.

> 💡 You may need to install it first: `sudo apt install htop`

**Why DevOps engineers prefer it:**
- Easier to read
- You can use arrow keys to scroll through processes
- Press `F9` to send a signal (kill) to a process
- Press `F6` to sort by a column

---

### 🔹 `uptime` — How Long Has the Server Been Running?

```bash
uptime
```

**Sample output:**
```
10:30:01 up 3 days,  2:15,  2 users,  load average: 0.25, 0.40, 0.38
```

**What it tells you:**
- How long the server has been running
- How many users are logged in
- **Load average** — a server with 1 CPU should have load < 1.0 (ideally)

**🔴 Real-world DevOps example:**
> After a server restart, you run `uptime` to confirm the server has been up and stable. A load average much higher than the number of CPUs means the server is **overloaded**.

---

### 🔹 `free -h` — How Much Memory (RAM) is Available?

```bash
free -h
```

**Sample output:**
```
              total        used        free      shared  buff/cache   available
Mem:           7.8G        4.1G        1.2G        120M        2.5G        3.3G
Swap:          2.0G        0.5G        1.5G
```

| Column | Meaning |
|--------|---------|
| `total` | Total RAM installed |
| `used` | RAM currently in use |
| `free` | RAM completely unused |
| `buff/cache` | RAM used by OS for caching (can be freed) |
| `available` | RAM actually available for new programs |
| **Swap** | Disk space used as backup RAM (slow!) |

> ⚠️ **Warning:** High swap usage means your server is **out of RAM** and using disk as memory. This makes everything very slow. Time to upgrade RAM or optimize the app.

**🔴 Real-world DevOps example:**
> App is throwing `OutOfMemoryError`. You run `free -h` and find only 200MB available. You check which process is eating RAM using `top`.

---

### 🔹 `ps -aef` and `ps aux` — List All Processes

```bash
ps -aef
ps aux
```

**What it does:**
Shows a **snapshot** (not live) of all currently running processes.

**Sample output of `ps aux`:**
```
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.1  51820  3584 ?        Ss   Mar20   0:04 /sbin/init
www-data  1234  1.2  2.4 512000 98304 ?        S    09:00   5:21 nginx: worker
ubuntu    5678  0.0  0.1  21472  4096 pts/0    S+   10:25   0:00 bash
```

| Column | Meaning |
|--------|---------|
| `USER` | Who started this process |
| `PID` | Process ID (unique number) |
| `%CPU` | CPU being used |
| `%MEM` | Memory being used |
| `COMMAND` | What program is running |

**Difference between `-aef` and `aux`:**
- Both show all processes — `aux` shows a bit more detail (memory %)
- In practice, DevOps engineers use both interchangeably

---

### 🔹 `df -h` — Disk Space Usage

```bash
df -h
```

**Sample output:**
```
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        50G   38G   10G  80% /
tmpfs           3.9G     0  3.9G   0% /dev/shm
/dev/sdb1       200G   50G  150G  25% /data
```

| Column | Meaning |
|--------|---------|
| `Size` | Total disk size |
| `Used` | How much is used |
| `Avail` | How much is free |
| `Use%` | Percentage used |
| `Mounted on` | Where this disk is attached |

> ⚠️ **Warning:** If `Use%` reaches **100%**, your server will **crash**. Set up monitoring alerts at 80%.

**🔴 Real-world DevOps example:**
> Log files have filled up the disk. You run `df -h` and see `/` is at 100%. You need to find and remove old logs immediately.

---

### 🔹 `du -sh` — How Big is This Folder?

```bash
du -sh /var/log
du -sh *          # Show size of everything in current folder
```

**What it does:**  
Shows the **disk usage of a specific directory or file**.

- `-s` = summary (show total, not each sub-file)
- `-h` = human readable (MB, GB)

**🔴 Real-world DevOps example:**
> Disk is almost full. You run `du -sh /var/log/*` to find out which log file is huge. You find `app.log` is 40GB and archive it.

---

### 🔹 `ping` — Is This Server Reachable?

```bash
ping google.com
ping 192.168.1.10
```

**What it does:**
Sends small packets to a server and checks if they come back. Used to test **network connectivity**.

**Sample output:**
```
PING google.com (142.250.67.46): 56 data bytes
64 bytes from 142.250.67.46: icmp_seq=0 ttl=118 time=12.3 ms
64 bytes from 142.250.67.46: icmp_seq=1 ttl=118 time=11.8 ms
```

- `time=12.3 ms` = how fast the reply came back (lower = better)
- Press `Ctrl+C` to stop

**🔴 Real-world DevOps example:**
> App can't connect to the database. You `ping` the database server IP. If ping fails, it's a network issue. If it succeeds, the problem is in the app or database config.

---

### 🔹 `who`, `w`, `last` — Who is Logged In?

```bash
who       # Who is currently logged in
w         # Who is logged in + what they're doing
last      # Login history
```

**`who` output:**
```
ubuntu   pts/0        2026-03-25 09:15 (192.168.1.50)
devops   pts/1        2026-03-25 10:00 (10.0.0.5)
```

**`w` output (more detail):**
```
USER     TTY      FROM             LOGIN@   IDLE WHAT
ubuntu   pts/0    192.168.1.50     09:15    0.00s w
devops   pts/1    10.0.0.5         10:00    2:30  vim app.conf
```

**`last` output:**
```
ubuntu   pts/0   192.168.1.50    Tue Mar 25 09:15   still logged in
root     tty1                    Mon Mar 24 22:00 - 22:05 (00:05)
```

**🔴 Real-world DevOps example (Security!):**
> Someone made unauthorized changes to the server. You run `last` to see who logged in recently. You check timestamps against the time of the incident.

---

## ⚙️ Process Management

> 🎭 **Real-life analogy:** Think of processes like apps running on your phone. If one app freezes, you force-stop it. On Linux, processes work the same way — and you have more control over them.

---

### 🔹 Finding a Specific Process

```bash
ps -aef | grep nginx
ps aux | grep java
```

**What this does:**
- `ps -aef` lists ALL processes
- `|` (pipe) sends that list to `grep`
- `grep nginx` filters only lines containing "nginx"

**Sample output:**
```
root      1234  0.0  0.1  52312  2048 ?  Ss  09:00  0:00 nginx: master process
www-data  1235  0.0  0.2  52312  4096 ?  S   09:00  0:01 nginx: worker process
ubuntu    5001  0.0  0.0  14220   984 pts/0  S+  10:30  0:00 grep --color=auto nginx
```

> 💡 The last line with `grep` in the command is your search command itself — you can ignore it.

**Getting just the PID:**
```bash
pgrep nginx          # Returns only the process IDs
pidof nginx          # Same thing
```

---

### 🔹 Killing a Process

```bash
kill <PID>           # Graceful stop (ask nicely)
kill -9 <PID>        # Force kill (terminate immediately)
killall nginx        # Kill all processes named "nginx"
pkill java           # Kill by name (partial match ok)
```

| Signal | Number | Meaning |
|--------|--------|---------|
| SIGTERM | 15 (default) | "Please stop cleanly" |
| SIGKILL | 9 | "Stop RIGHT NOW, no cleanup" |

> ⚠️ **Prefer `kill` (SIGTERM) over `kill -9` (SIGKILL).** Force kill doesn't let the app save data or close files properly. Only use `-9` if the process is completely frozen.

---

### 🔹 Step-by-Step Production Troubleshooting Scenario

**🔴 Scenario:** "The server is slow, users are complaining!"

**Step 1: Check load and uptime**
```bash
uptime
# If load average >> number of CPUs, something is wrong
```

**Step 2: Find what's eating CPU**
```bash
top
# Press P to sort by CPU
# Note the PID of the high-CPU process
```

**Step 3: Investigate the process**
```bash
ps -aef | grep <PID>
# Check what user it belongs to and what command started it
```

**Step 4: Check memory**
```bash
free -h
# Is swap being used heavily? That means RAM is exhausted.
```

**Step 5: Check disk**
```bash
df -h
# Is disk full? Full disk can slow down everything.
```

**Step 6: Take action**
```bash
# If it's a stuck process:
kill <PID>

# If the service needs a restart:
sudo systemctl restart nginx
sudo systemctl restart your-app
```

---

### 🔹 OOM — Out Of Memory Killer

**What is OOM?**  
When your Linux server runs out of RAM and swap space, the **OOM Killer** (Out Of Memory Killer) activates automatically. It **picks a process and kills it** to free up memory.

**How to check if OOM killed something:**
```bash
sudo dmesg | grep -i "oom"
sudo grep -i "out of memory" /var/log/syslog
```

**Sample OOM message:**
```
Out of memory: Kill process 4521 (java) score 892 or sacrifice child
Killed process 4521 (java) total-vm:3145728kB, anon-rss:2097152kB
```

> ⚠️ **OOM is a serious alert.** It means your server doesn't have enough memory for all running applications. You need to either:
> - Add more RAM
> - Reduce memory usage (optimize your app)
> - Add more swap space (temporary fix)

---

## 📦 File Compression (TAR)

> 📬 **Real-life analogy:** TAR is like packing multiple items into a single box and then shrinking that box (compression). On Linux, we archive + compress files to save space and transfer them easily.

---

### 🔹 What is TAR?

**TAR = Tape Archive**

Originally used to back up data to magnetic tapes. Today, we use it to:
- Bundle multiple files into one
- Compress log files to save disk space
- Package application files for deployment
- Create backups

---

### 🔹 `tar cvf` — Create an Archive

```bash
tar cvf archive.tar /path/to/folder
```

**Flags explained:**
| Flag | Meaning |
|------|---------|
| `c` | **C**reate a new archive |
| `v` | **V**erbose — show files being added |
| `f` | **F**ile — specify the archive filename |

**Example — Archive logs folder:**
```bash
tar cvf logs_backup.tar /var/log/app/
```

**Create a COMPRESSED archive (with gzip):**
```bash
tar cvzf logs_backup.tar.gz /var/log/app/
```
- Adding `z` = compress with **gzip** (makes the file much smaller)
- `.tar.gz` is the standard extension for compressed archives

---

### 🔹 `tar xvf` — Extract an Archive

```bash
tar xvf archive.tar
```

**Flags explained:**
| Flag | Meaning |
|------|---------|
| `x` | E**x**tract files from archive |
| `v` | **V**erbose — show files being extracted |
| `f` | **F**ile — specify archive filename |

**Extract a gzip-compressed archive:**
```bash
tar xvzf logs_backup.tar.gz
```

**Extract to a specific folder:**
```bash
tar xvzf logs_backup.tar.gz -C /tmp/restored/
```

---

### 🔹 Quick TAR Reference

```bash
# View contents without extracting
tar tvf archive.tar.gz

# Create compressed archive
tar cvzf backup.tar.gz /var/log/

# Extract compressed archive
tar xvzf backup.tar.gz

# Extract to specific directory
tar xvzf backup.tar.gz -C /home/ubuntu/restore/
```

**🔴 Real-world DevOps examples:**

> **Log Rotation:** App logs grow 500MB/day. Every night, a cron job runs:
> ```bash
> tar cvzf /backups/app_logs_$(date +%Y%m%d).tar.gz /var/log/app/
> ```
> This compresses logs (~80% smaller) and moves them to a backup location.

> **Deployment:** Deploying a new version of an app:
> ```bash
> tar cvzf app_v2.1.tar.gz ./dist/
> scp app_v2.1.tar.gz ubuntu@prod-server:/opt/app/
> ssh ubuntu@prod-server "tar xvzf /opt/app/app_v2.1.tar.gz -C /opt/app/"
> ```

---

## 🧾 Shell Scripting

> 🤖 **Real-life analogy:** A shell script is like a **recipe**. Instead of performing each step manually every time, you write down all the steps once and run the recipe whenever you need it.

---

### 🔹 What is Shell Scripting?

A **shell script** is a plain text file containing a series of Linux commands. When you run the script, Linux executes those commands one by one — automatically.

**Why DevOps engineers use shell scripts:**
- 🔁 **Automation** — Run repetitive tasks without manual effort
- ⏰ **Scheduling** — Run with cron jobs at specific times
- 🚨 **Monitoring** — Check server health and send alerts
- 🚀 **Deployment** — Deploy applications automatically
- 🧹 **Maintenance** — Clean old files, rotate logs, backup data

---

### 🔹 The Shebang Line `#!/bin/bash`

Every shell script should start with:

```bash
#!/bin/bash
```

**What is a shebang?**
- `#!` = "shebang" (sharp + bang)
- `/bin/bash` = tells Linux to use the **Bash shell** to run this script
- Without it, Linux might use a different shell and your script might fail

Think of it as saying: *"Hey Linux, use the Bash program to interpret this file."*

---

### 🔹 Creating and Running a Shell Script

**Step 1: Create the file**
```bash
nano server_check.sh
```

**Step 2: Write your script**
```bash
#!/bin/bash

echo "============================="
echo "  SERVER HEALTH CHECK REPORT "
echo "============================="
echo ""

echo "📅 Date and Time:"
date
echo ""

echo "⏱️ Server Uptime:"
uptime
echo ""

echo "💾 Memory Usage:"
free -h
echo ""

echo "💿 Disk Usage:"
df -h
echo ""

echo "============================="
echo "  Report Complete!"
echo "============================="
```

**Step 3: Save and exit**
- In nano: `Ctrl+O` (save), `Ctrl+X` (exit)

**Step 4: Give execute permission**
```bash
chmod +x server_check.sh
```

**Step 5: Run the script**
```bash
./server_check.sh
```

**Sample output:**
```
=============================
  SERVER HEALTH CHECK REPORT 
=============================

📅 Date and Time:
Tue Mar 25 10:30:01 IST 2026

⏱️ Server Uptime:
 10:30:01 up 3 days,  2:15,  2 users,  load average: 0.25, 0.40, 0.38

💾 Memory Usage:
              total        used        free      shared  buff/cache   available
Mem:           7.8G        4.1G        1.2G        120M        2.5G        3.3G

💿 Disk Usage:
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        50G   38G   10G  80% /

=============================
  Report Complete!
=============================
```

---

### 🔹 Useful Script Additions

**Add variables:**
```bash
#!/bin/bash
SERVER_NAME="prod-web-01"
echo "Checking server: $SERVER_NAME"
```

**Add a warning if disk is high:**
```bash
#!/bin/bash
DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | tr -d '%')

if [ $DISK_USAGE -gt 80 ]; then
    echo "⚠️ WARNING: Disk usage is at ${DISK_USAGE}%! Take action!"
else
    echo "✅ Disk usage is fine: ${DISK_USAGE}%"
fi
```

**🔴 Real-world DevOps usage:**
> This script runs every hour via a cron job on all production servers. If disk goes above 80%, it sends an alert to Slack or email.

---

## 🔐 File Permissions

> 🏠 **Real-life analogy:** Think of a house. The **owner** (you) can do anything — enter, renovate, sell. Your **family** (group) may be allowed inside but not renovate. **Strangers** (others) can only look through the window (read-only), OR are completely blocked.

---

### 🔹 Understanding Permission Basics

When you run `ls -l`, you see:

```bash
ls -l
```

```
-rwxr-xr-- 1 ubuntu devops 4096 Mar 25 10:00 server_check.sh
drwxr-xr-x 2 ubuntu devops 4096 Mar 25 09:00 logs/
```

**Breaking down `-rwxr-xr--`:**

```
- rwx r-x r--
│ │   │   │
│ │   │   └── Others (everyone else)
│ │   └────── Group members
│ └────────── Owner (user)
└──────────── Type (- = file, d = directory)
```

**Permission characters:**
| Symbol | Meaning | Number value |
|--------|---------|-------------|
| `r` | Read | 4 |
| `w` | Write | 2 |
| `x` | Execute | 1 |
| `-` | No permission | 0 |

---

### 🔹 Numeric (Octal) Permissions

Each permission group (Owner, Group, Others) is represented as a number:

```
rwx = 4+2+1 = 7  (full permissions)
r-x = 4+0+1 = 5  (read + execute)
r-- = 4+0+0 = 4  (read only)
--- = 0+0+0 = 0  (no permissions)
```

**Common permission numbers:**

| Number | Meaning | Use case |
|--------|---------|----------|
| `755` | Owner: all, Group+Others: read+execute | Web files, scripts |
| `644` | Owner: read+write, Group+Others: read | Config files |
| `600` | Owner: read+write only | SSH private keys |
| `777` | Everyone: full permissions | **⚠️ DANGEROUS** |
| `400` | Owner: read only | Super sensitive files |

---

### 🔹 `chmod` — Change Permissions

```bash
# Using numbers (recommended)
chmod 755 server_check.sh
chmod 644 config.conf
chmod 600 ~/.ssh/id_rsa

# Using symbols
chmod +x script.sh        # Add execute for everyone
chmod -w file.txt         # Remove write permission
chmod u+x script.sh       # Add execute for owner (u=user/owner)
chmod g-w file.txt        # Remove write from group (g=group)
chmod o-r secret.txt      # Remove read from others (o=others)
```

**`chmod +x` specifically:**
```bash
chmod +x script.sh
```
This makes the file **executable** — meaning you can run it as a program.

> 💡 You MUST do this after creating a `.sh` script, otherwise Linux won't run it.

---

### 🔹 Why `777` is DANGEROUS ⚠️

`chmod 777 file.sh` means:
- **Everyone** on the system can read, write, AND execute it
- A hacker or malicious user who gains any access to the server can:
  - Read your config files (steal database passwords!)
  - Modify your scripts (inject malicious code!)
  - Execute dangerous commands

**Best practice:**
```bash
# ✅ Good - only owner can modify, others can read
chmod 644 config.conf

# ✅ Good - script executable by owner, readable by group
chmod 754 deploy.sh

# ❌ Bad - everyone has full control
chmod 777 anything.sh
```

---

### 🔹 `ls -l` — Viewing File Permissions

```bash
ls -l
ls -la    # Include hidden files (starting with .)
```

Sample output:
```
total 32
-rwxr-xr-- 1 ubuntu devops  1024 Mar 25 10:00 server_check.sh
-rw-r--r-- 1 ubuntu devops   512 Mar 25 09:00 config.conf
drwxr-xr-x 2 ubuntu devops  4096 Mar 24 15:00 logs/
-rw------- 1 ubuntu ubuntu  1679 Mar 20 08:00 .ssh/id_rsa
```

| Field | Value | Meaning |
|-------|-------|---------|
| Permissions | `-rwxr-xr--` | See above |
| Links | `1` | Number of hard links |
| Owner | `ubuntu` | File owner username |
| Group | `devops` | File group |
| Size | `1024` | File size in bytes |
| Date | `Mar 25 10:00` | Last modified |
| Name | `server_check.sh` | File name |

---

## 👤 User Management

> 🏢 **Real-life analogy:** In a company, different employees have different access levels. The receptionist can see the lobby, an engineer can access the server room, and only the CTO has master keys. Linux user management works the same way.

---

### 🔹 `adduser` — Create a New User

```bash
sudo adduser john
```

This will:
1. Create a new user named `john`
2. Create a home directory `/home/john`
3. Ask you to set a password
4. Ask for optional info (Full Name, Phone, etc.)

**For scripting (non-interactive):**
```bash
sudo useradd -m -s /bin/bash john     # Create user with home dir and bash shell
sudo passwd john                       # Set password separately
```

---

### 🔹 `passwd` — Change User Password

```bash
sudo passwd john        # Change john's password (as admin)
passwd                  # Change YOUR OWN password
```

You'll be prompted to enter the new password twice.

---

### 🔹 `deluser` — Delete a User

```bash
sudo deluser john               # Delete user but keep home directory
sudo deluser --remove-home john # Delete user AND their home directory
```

> ⚠️ **Warning:** Deleting with `--remove-home` permanently removes all files in `/home/john`. Make sure to backup important data first!

---

### 🔹 `su` — Switch User

```bash
su john           # Switch to user john (needs john's password)
su -              # Switch to root (needs root password)
sudo su -         # Switch to root (using sudo — needs YOUR password)
```

**`-` flag:**
Using `su -` loads the target user's full environment (PATH, home directory, etc.). Always use `su -` instead of just `su`.

---

### 🔹 `exit` — Go Back to Previous User

```bash
exit
```

After running `su john`, type `exit` to return to your original user.

---

### 🔹 Real-World Example — Multi-User Server Setup

```bash
# Step 1: Create users for team members
sudo adduser alice
sudo adduser bob
sudo adduser carol

# Step 2: Set passwords
sudo passwd alice   # Set Alice's password
sudo passwd bob     # Set Bob's password

# Step 3: Give them sudo access (if senior devops)
sudo usermod -aG sudo alice

# Step 4: Switch to alice to test
su - alice
whoami        # Should show "alice"
exit          # Back to your user
```

**🔴 Real-world DevOps scenario:**
> A new developer joins your team. You create their account, add them to the `devops` group (for shared project access), and give them their credentials. They can now SSH into the server with their own account — no password sharing!

---

## 👥 Group Management

> 🏷️ **Real-life analogy:** Groups are like **access cards** in an office. Instead of individually granting every person access to every room, you give everyone in the "Engineering" team the Engineering access card. When a new engineer joins, you just give them the card.

---

### 🔹 `addgroup` — Create a New Group

```bash
sudo addgroup devops
sudo addgroup developers
sudo addgroup qa-team
```

This creates a group that users can be added to.

---

### 🔹 `usermod -aG` — Add User to a Group

```bash
sudo usermod -aG devops alice
sudo usermod -aG devops bob
```

**Breaking it down:**
- `usermod` = modify a user account
- `-a` = **Append** (add without removing existing groups) ← VERY IMPORTANT!
- `-G` = specify the **Group** to add
- `devops` = group name
- `alice` = username

> ⚠️ **Critical:** ALWAYS use `-aG` together, never just `-G`. Using `-G` alone **REPLACES** all existing groups, which can lock a user out of sudo!

**To apply group changes, user must log out and log back in:**
```bash
# Or use this without logging out:
newgrp devops
```

---

### 🔹 `getent group` — See Group Members

```bash
getent group devops       # Show members of 'devops' group
getent group              # List ALL groups on the system
groups alice              # Show which groups alice belongs to
id alice                  # Show user ID and group memberships
```

**Sample output:**
```
devops:x:1002:alice,bob,carol
```
Format: `groupname:password:GID:members`

---

### 🔹 `delgroup` — Delete a Group

```bash
sudo delgroup old-team
```

> 💡 You can only delete a group if it's not the primary group of any user.

---

### 🔹 Real-World DevOps Access Control Example

```bash
# Create groups for different teams
sudo addgroup backend-devs
sudo addgroup frontend-devs
sudo addgroup devops-team

# Add engineers to groups
sudo usermod -aG backend-devs alice
sudo usermod -aG backend-devs bob
sudo usermod -aG frontend-devs carol
sudo usermod -aG devops-team david
sudo usermod -aG devops-team emma

# Give devops-team sudo access
sudo usermod -aG sudo david
sudo usermod -aG sudo emma

# Verify
getent group backend-devs
getent group devops-team
```

Now:
- Alice and Bob can work with backend files
- Carol works with frontend files
- David and Emma (DevOps) have admin access

**Set folder permissions for a group:**
```bash
sudo chown -R :backend-devs /opt/backend/
sudo chmod -R 770 /opt/backend/
# Now: owner has full access, backend-devs group has full access, others have NO access
```

---

## 🔒 Advanced User Management

---

### 🔹 `chage` — Password and Account Expiry Settings

**What is `chage`?**  
`chage` (CHange AGE) controls when a user's **password expires** and when their **account expires**.

```bash
sudo chage -l john          # View current expiry settings for john
sudo chage john             # Interactive mode to set all options
```

**Sample `chage -l` output:**
```
Last password change                    : Mar 01, 2026
Password expires                        : Jun 01, 2026
Password inactive                       : never
Account expires                         : never
Minimum number of days between password change : 0
Maximum number of days between password change : 90
Number of days of warning before password expires : 7
```

**Setting expiry with flags:**
```bash
# Password must be changed every 90 days
sudo chage -M 90 john

# Warn user 7 days before password expires
sudo chage -W 7 john

# Account expires on a specific date
sudo chage -E 2026-12-31 john

# Force user to change password on next login
sudo chage -d 0 john
```

> **🔴 Real-world scenario:** A contractor is hired until June 30th. You set their account to expire on that date. After June 30th, they automatically cannot log in — no manual action needed.

---

### 🔹 `/etc/passwd` — User Account Information

```bash
cat /etc/passwd
```

**Sample line:**
```
john:x:1001:1001:John Dev,,,:/home/john:/bin/bash
```

| Field | Value | Meaning |
|-------|-------|---------|
| Username | `john` | Login name |
| Password | `x` | Password is in `/etc/shadow` |
| UID | `1001` | User ID number |
| GID | `1001` | Primary group ID |
| GECOS | `John Dev,,,` | Full name / info |
| Home | `/home/john` | Home directory |
| Shell | `/bin/bash` | Default shell |

> 💡 **Important UIDs:**
> - `0` = root (superuser)
> - `1-999` = system users (services like nginx, mysql)
> - `1000+` = regular human users

---

### 🔹 `/etc/group` — Group Information

```bash
cat /etc/group
```

**Sample lines:**
```
sudo:x:27:ubuntu,david
devops:x:1002:alice,bob,carol
```

Format: `group_name:password:GID:members`

---

### 🔹 `/etc/shadow` — Encrypted Passwords

```bash
sudo cat /etc/shadow
```

**Sample line:**
```
john:$6$salt$hashedpassword...:19200:0:90:7:::
```

> 🔒 **Security note:** 
> - This file is **readable only by root** (mode 640 or 000)
> - Passwords are stored as **cryptographic hashes** (not plain text)
> - Even if someone reads this file, they can't easily recover the password
> - This is why it's separate from `/etc/passwd` (which is readable by all)

**Never directly edit these files** — use `adduser`, `passwd`, `chage` etc. instead.

---

## 🏋️ Practice Tasks

### Task 1: Monitor Your Server 🖥️

**Objective:** Get a complete picture of server health.

```bash
# 1. Check how long the server has been running
uptime

# 2. See the top 5 CPU-consuming processes
top -b -n 1 | head -20

# 3. Check available memory
free -h

# 4. Check disk usage on all drives
df -h

# 5. Find which folder is using the most space
sudo du -sh /var/* | sort -rh | head -5

# 6. See who is currently logged in
w
```

**✅ Success criteria:** You can explain every line of output.

---

### Task 2: Find and Manage Processes ⚙️

**Objective:** Practice finding and controlling processes.

```bash
# 1. List all running processes
ps aux

# 2. Find the bash processes
ps aux | grep bash

# 3. Find the PID of your terminal session
echo $$

# 4. Start a background process (sleep for 1000 seconds)
sleep 1000 &

# 5. Find it
ps aux | grep sleep

# 6. Get its PID and kill it gracefully
kill <PID>

# 7. Verify it's gone
ps aux | grep sleep
```

---

### Task 3: Work with TAR Archives 📦

**Objective:** Create and extract compressed archives.

```bash
# 1. Create a test directory with some files
mkdir ~/test_archive
echo "Hello World" > ~/test_archive/file1.txt
echo "DevOps Learning" > ~/test_archive/file2.txt
echo "Linux is awesome" > ~/test_archive/file3.txt

# 2. Create a compressed archive
tar cvzf ~/my_backup.tar.gz ~/test_archive/

# 3. View contents without extracting
tar tvzf ~/my_backup.tar.gz

# 4. Delete the original directory
rm -rf ~/test_archive/

# 5. Extract the archive
tar xvzf ~/my_backup.tar.gz -C ~/

# 6. Verify files are restored
ls ~/test_archive/
cat ~/test_archive/file1.txt
```

---

### Task 4: Write a Shell Script 🧾

**Objective:** Create your first monitoring shell script.

```bash
# 1. Create the script file
nano ~/health_check.sh
```

**Paste this content:**
```bash
#!/bin/bash

echo "============================================"
echo "  🖥️  SERVER HEALTH CHECK - $(hostname)"
echo "  📅  $(date)"
echo "============================================"

echo ""
echo "🕐 UPTIME:"
uptime

echo ""
echo "💾 MEMORY:"
free -h

echo ""
echo "💿 DISK:"
df -h | grep -v tmpfs

echo ""
echo "🔝 TOP 5 CPU PROCESSES:"
ps aux --sort=-%cpu | head -6

echo ""
echo "============================================"
echo "  ✅ Health check complete!"
echo "============================================"
```

```bash
# 2. Save and make executable
chmod +x ~/health_check.sh

# 3. Run it!
./~/health_check.sh

# 4. Run it and save output to a file
./~/health_check.sh > /tmp/health_report.txt
cat /tmp/health_report.txt
```

---

### Task 5: Practice File Permissions 🔐

**Objective:** Understand and set file permissions.

```bash
# 1. Create test files
touch test_public.txt test_private.txt test_script.sh

# 2. Check current permissions
ls -l

# 3. Make script executable
chmod +x test_script.sh

# 4. Make private file readable only by owner
chmod 600 test_private.txt

# 5. Set public file to standard permissions
chmod 644 test_public.txt

# 6. Verify all permissions
ls -l

# 7. Try to understand each permission string
# For each file, explain: who can read, write, execute?
```

---

### Task 6: Create Users and Groups 👤👥

**Objective:** Practice user and group management.

```bash
# 1. Create two new users
sudo adduser devuser1
sudo adduser devuser2

# 2. Create a group
sudo addgroup dev-team

# 3. Add both users to the group
sudo usermod -aG dev-team devuser1
sudo usermod -aG dev-team devuser2

# 4. Verify group membership
getent group dev-team

# 5. Check user details
id devuser1
id devuser2

# 6. Switch to devuser1 and verify
su - devuser1
whoami
groups
exit

# 7. Set password expiry for devuser1 (90 days)
sudo chage -M 90 devuser1

# 8. Check expiry settings
sudo chage -l devuser1

# 9. Cleanup (delete the test users)
sudo deluser --remove-home devuser1
sudo deluser --remove-home devuser2
sudo delgroup dev-team
```

---

## 🎤 Interview Questions

---

### Q1: What does load average mean in the `uptime` or `top` output?

**Answer:**
Load average shows the average number of processes waiting to use the CPU over 1, 5, and 15 minutes. 

- For a **1 CPU system**: load average of `1.0` means 100% utilized; above 1.0 means processes are waiting (overloaded)
- For a **4 CPU system**: load average of `4.0` means all CPUs are at 100%
- Rule of thumb: **load average should not regularly exceed the number of CPU cores**

---

### Q2: What is the difference between `free` memory and `available` memory in `free -h`?

**Answer:**
- **Free**: RAM that is completely unused
- **Available**: RAM that is actually available for new programs (includes memory that's currently used for cache, which the OS can reclaim instantly)

The **`available`** number is what matters when asking "do I have enough memory?" because Linux actively uses free RAM as disk cache for performance.

---

### Q3: What is the difference between `kill` and `kill -9`?

**Answer:**
- `kill <PID>` sends SIGTERM (signal 15) — politely asks the process to stop. The process can catch this signal and clean up gracefully (save data, close files).
- `kill -9 <PID>` sends SIGKILL — immediately forces the OS to terminate the process. The process has no chance to clean up.

**Best practice:** Always try `kill` first. Only use `kill -9` if the process ignores `kill` and is completely frozen.

---

### Q4: What is the OOM Killer and when does it activate?

**Answer:**
OOM Killer (Out Of Memory Killer) is a Linux kernel mechanism. When the system runs out of both RAM and swap space, the kernel must free memory. The OOM Killer selects a process (usually the one using the most memory) and kills it.

You can check if OOM killed something with:
```bash
dmesg | grep -i oom
grep "out of memory" /var/log/syslog
```

---

### Q5: Explain the difference between `tar cvf` and `tar cvzf`

**Answer:**
- `tar cvf archive.tar files/` — Creates a TAR archive **without compression**. The file is just bundled, not compressed.
- `tar cvzf archive.tar.gz files/` — Creates a TAR archive **with gzip compression**. The resulting file is much smaller. The `z` flag enables gzip compression.

In production, we almost always use `cvzf`/`xvzf` because disk space matters.

---

### Q6: What is a shebang line? Why is it important?

**Answer:**
The shebang `#!/bin/bash` is the first line of a shell script. It tells the operating system which interpreter to use when running the script.

Without it, Linux doesn't know which shell to use. The script might:
- Use a different shell (sh instead of bash), which behaves differently
- Fail entirely if the system can't determine the interpreter

Always include `#!/bin/bash` as the very first line of bash scripts.

---

### Q7: What is the difference between `chmod 755` and `chmod 777`?

**Answer:**
- `chmod 755`: Owner has full access (rwx=7). Group and Others have read+execute (r-x=5). Others **cannot write/modify** the file.
- `chmod 777`: **Everyone** (owner, group, others) has full read, write, and execute permissions.

`777` is dangerous because any user on the system can modify or delete the file. In a web server context, this means a hacker who compromises any account can modify your scripts. Always use the minimum permissions needed.

---

### Q8: What does `-aG` mean in `usermod -aG sudo john`?

**Answer:**
- `-a` = **Append** — add the user to the specified group without removing them from their current groups
- `-G` = **Groups** — specify the group(s) to add

**CRITICAL:** If you use just `-G` (without `-a`), it replaces all current groups! This could remove a user from the `sudo` group, locking them out. Always use `-aG` together to safely add users to additional groups.

---

### Q9: What is the difference between `/etc/passwd` and `/etc/shadow`?

**Answer:**
- `/etc/passwd`: Contains basic user information (username, UID, GID, home directory, shell). **Readable by all users.** Where the password field shows `x`, it means the actual password is in `/etc/shadow`.
- `/etc/shadow`: Contains encrypted (hashed) passwords and password policy information (expiry, etc.). **Only readable by root.** This file is separate for security — if passwd were readable by everyone with password hashes, attackers could attempt to crack them.

---

### Q10: How would you troubleshoot a server that is responding slowly?

**Answer:**
Systematic approach:
1. `uptime` — Check load average (is it too high for the number of CPUs?)
2. `top` — Identify which process is consuming high CPU (press P to sort by CPU)
3. `free -h` — Check if the system is low on memory or using swap heavily
4. `df -h` — Check if any disk is full (full disk can cause severe slowdowns)
5. `ps aux | grep <process-name>` — Investigate the specific process
6. `dmesg | grep oom` — Check if OOM killer has been active
7. Take action: kill the problematic process, restart the service, or scale up resources

---

### Q11: How do you set a file so only the owner can read and write it, but nobody else can access it?

**Answer:**
```bash
chmod 600 filename
```
- Owner: `rw-` (6 = 4+2)
- Group: `---` (0)
- Others: `---` (0)

This is the correct permission for sensitive files like SSH private keys (`~/.ssh/id_rsa`) and configuration files with passwords.

---

### Q12: A contractor's access needs to be revoked automatically on December 31st. How do you do this?

**Answer:**
```bash
sudo chage -E 2026-12-31 contractor_username
```

This sets the account expiry date. After December 31st, the user will be unable to log in, even if they have the correct password. You can verify the setting with:
```bash
sudo chage -l contractor_username
```

---

## 📝 Summary

### Complete Command Reference Table

| Category | Command | What It Does |
|----------|---------|-------------|
| **Monitoring** | `top` | Live process and resource monitor |
| **Monitoring** | `htop` | Colored, interactive version of top |
| **Monitoring** | `uptime` | Server run time + load average |
| **Monitoring** | `free -h` | RAM usage (total, used, available) |
| **Monitoring** | `ps aux` | Snapshot of all running processes |
| **Monitoring** | `ps -aef` | Same as above, slightly different format |
| **Monitoring** | `df -h` | Disk space usage for all filesystems |
| **Monitoring** | `du -sh` | Size of a specific folder |
| **Monitoring** | `ping` | Test network connectivity |
| **Monitoring** | `who` | Who is currently logged in |
| **Monitoring** | `w` | Logged-in users + what they're doing |
| **Monitoring** | `last` | Login history |
| **Processes** | `ps aux \| grep` | Filter process list |
| **Processes** | `kill <PID>` | Gracefully stop a process |
| **Processes** | `kill -9 <PID>` | Force kill a process |
| **Processes** | `pkill <name>` | Kill by process name |
| **TAR** | `tar cvzf` | Create compressed archive |
| **TAR** | `tar xvzf` | Extract compressed archive |
| **TAR** | `tar tvzf` | List archive contents |
| **Scripts** | `#!/bin/bash` | Shebang — declare bash interpreter |
| **Scripts** | `chmod +x file.sh` | Make script executable |
| **Scripts** | `./script.sh` | Run a script |
| **Permissions** | `chmod 755` | Set numeric permissions |
| **Permissions** | `chmod +x` | Add execute permission |
| **Permissions** | `ls -l` | View file permissions |
| **Users** | `sudo adduser` | Create new user |
| **Users** | `sudo passwd` | Set/change user password |
| **Users** | `sudo deluser` | Delete a user |
| **Users** | `su -` | Switch to another user |
| **Groups** | `sudo addgroup` | Create new group |
| **Groups** | `sudo usermod -aG` | Add user to group (safely) |
| **Groups** | `getent group` | View group membership |
| **Groups** | `sudo delgroup` | Delete a group |
| **Advanced** | `sudo chage -l` | View password/account expiry |
| **Advanced** | `sudo chage -M` | Set max password age |
| **Advanced** | `sudo chage -E` | Set account expiry date |
| **Config Files** | `/etc/passwd` | User account information |
| **Config Files** | `/etc/group` | Group information |
| **Config Files** | `/etc/shadow` | Encrypted passwords (root only) |

---

### Key Takeaways 🎯

| Concept | Remember |
|---------|---------|
| **Load Average** | Should be ≤ number of CPU cores |
| **Memory** | Watch `available`, not just `free` |
| **Disk** | Alert at 80%, act before 100% |
| **kill vs kill -9** | Always try graceful kill first |
| **chmod 777** | NEVER use in production |
| **usermod -aG** | Always use `-a` with `-G` |
| **Shebang** | Always start scripts with `#!/bin/bash` |
| **chmod +x** | Required before running a script |
| **/etc/shadow** | Never edit manually |

---

> 🚀 **Next Steps:**  
> Practice these commands on a test server or local VM. The goal is to build **muscle memory** — you should be able to run these commands without thinking about them when a production issue strikes at 2am!

---
Prev : [07_linux_commands_1.md](07_linux_commands_1.md) | Next : [09_linux_commands_3.md](09_linux_commands_3.md)
---
