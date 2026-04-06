# Linux Practical Session (Hands-on DevOps Basics)

## Introduction
This session provides a hands-on, practical deep-dive into the essential Linux commands and concepts every DevOps engineer needs to know. Mastering these commands is crucial because real-world DevOps isn't just about writing code; it's about keeping servers healthy, troubleshooting deployment failures, monitoring resources, and automating workflows. Knowing these topics inside out will significantly boost your confidence during interviews, where practical scenarios are frequently discussed, and more importantly, in production environments where quick thinking saves the day.

---

## Detailed Sections

### A. System Monitoring (Prince)

Monitoring the system is the first step in identifying and resolving issues before they impact the end user.

#### `vmstat`
- **What:** Virtual Memory Statistics. A command-line tool that reports information about processes, memory, paging, block IO, traps, and CPU activity.
- **Why:** Used to get a quick overview of why a system might be slow—is it a memory bottleneck or CPU?
- **How:** Run `vmstat 1` to get updates every 1 second.
- **Impact:** Helps quickly identify resource exhaustion in production.

#### `free -h`
- **What:** Displays the total amount of free and used physical and swap memory in the system. The `-h` flag makes it human-readable (e.g., Megabytes, Gigabytes).
- **Why:** To make sure your specific application (like a database or web server) is not running out of RAM. 
- **How:** Run `free -h`.
- **Impact:** Prevents Out-Of-Memory (OOM) errors, which can crash critical applications.

#### `top` / `htop`
- **What:** Interactive task managers that provide a dynamic, real-time view of running processes. `htop` is the prettier, more user-friendly version of `top`.
- **Why:** To find exactly which process or application is eating up your CPU or memory.
- **How:** Run `top` or `htop` (you may need to install `htop` first via package manager).
- **Impact:** Allows you to swiftly find and terminate rogue processes causing site outages.

#### `uptime`
- **What:** Tells you how long the system has been running, how many users are currently logged on, and the system load averages.
- **Why:** To check if a server unexpectedly rebooted recently and to measure the general load over the past 1, 5, and 15 minutes.
- **How:** Run `uptime`.
- **Impact:** Provides an instant health check—high load averages mean the server is struggling.

#### `ping`
- **What:** Sends ICMP ECHO_REQUEST packets to network hosts.
- **Why:** Used to check network connectivity between your server and another machine (like a database server or external API).
- **How:** Run `ping google.com`.
- **Impact:** Instantly verifies if a server is reachable, ruling out network down-time during troubleshooting.

---

### B. Basic Linux Commands (Rishabh)

These are the fundamental building blocks for navigating and interacting with any Linux environment.

#### `sudo`
- **What:** Superuser Do. Allows a permitted user to execute a command as the superuser (root) or another user.
- **Why:** For security reasons, you shouldn't log in as `root` directly. You use `sudo` only when elevated privileges are required, like installing packages.
- **How:** `sudo apt update`
- **Impact:** Protects the system from accidental, irreversible changes while allowing targeted administrative actions.

#### `pwd`
- **What:** Print Working Directory. Outputs the absolute path of the current directory you are in.
- **Why:** In terminal, you lack a graphical interface. You need to know exactly where you are to avoid running scripts or deleting files in the wrong place.
- **How:** `pwd`
- **Impact:** Prevents catastrophic errors like deleting files in `/var` when you thought you were in `/tmp`.

#### `ls`
- **What:** List directory contents.
- **Why:** To see what files and folders exist in the current location.
- **How:** `ls -la` (lists all files, including hidden ones, in a detailed format).
- **Impact:** Essential for verifying that a deployment copied the files correctly or checking if configuration files exist.

#### `cd`
- **What:** Change Directory.
- **Why:** To navigate around the server's file system (e.g., getting into application log folders).
- **How:** `cd /var/log`
- **Impact:** The main tool for moving into the working directories where actions need to be performed.

#### `mkdir`
- **What:** Make Directory.
- **Why:** To create new folders for organizing code, storing logs, or setting up new projects.
- **How:** `mkdir new_project`
- **Impact:** Keeps the server organized and is frequently used in automation scripts to set up environments.

#### `touch`
- **What:** Changes file timestamps. Often used to quickly create empty files.
- **Why:** Often used to create a blank configuration file or placeholder script before editing it.
- **How:** `touch config.yml`
- **Impact:** A fast way to initialize requirements during manual setup or automated deployments.

#### `chmod`
- **What:** Change Mode. Alters the read, write, and execute permissions of files and directories.
- **Why:** Security. For instance, ensuring a private SSH key (`.pem` file) is readable only by the owner.
- **How:** `chmod 400 key.pem` or `chmod +x script.sh` to make a script executable.
- **Impact:** Enforces proper security access, preventing unauthorized users from modifying or executing sensitive files.

---

### C. File Management (Sarang)

Managing, finding, and handling files efficiently is central to server administration.

#### `find`
- **What:** Searches for files in a directory hierarchy based on names, types, sizes, or timestamps.
- **Why:** To locate lost configuration files, massive log files, or specific scripts scattered across a server.
- **How:** `find / -name "nginx.conf"`
- **Impact:** Drastically speeds up troubleshooting by easily locating needed files in vast file systems.

#### `head` / `tail`
- **What:** Outputs the first part (`head`) or the last part (`tail`) of files.
- **Why:** You don't want to open a 5GB log file in an editor (it will freeze the terminal). Use `tail` to see the most recent errors.
- **How:** `tail -f /var/log/syslog` (`-f` follows the file, updating as new logs come in).
- **Impact:** Crucial for live-debugging a crashing application by watching errors occur in real-time.

#### `chown`
- **What:** Change File Owner and Group.
- **Why:** Often, an application like Nginx or Jenkins needs to own the folder it runs from, otherwise, it can't write logs or save data.
- **How:** `sudo chown -R ubuntu:ubuntu /app/directory`
- **Impact:** Solves common "Permission Denied" errors when deploying a new application.

#### `gzip`
- **What:** A tool for compressing and decompressing files.
- **Why:** To save disk space, especially for old logs or database backups, and to make file transfers faster over the network.
- **How:** `gzip backup.sql` (creates `backup.sql.gz`)
- **Impact:** Prevents server disks from filling up and hitting 100% usage, which causes servers to crash.

#### `mount` / `unmount`
- **What:** Attaches (mounts) or detaches (unmounts) external storage, like a new hard drive or USB, to a specific folder in the Linux filesystem.
- **Why:** When you attach a new disk to a server for extra storage, Linux won't use it until you physically 'mount' it to a folder.
- **How:** `sudo mount /dev/xvdf /data`
- **Impact:** Allows massive horizontal scaling of storage without disrupting the main operating system drive.

---

### D. Advanced & AWS Concepts (Mohit)

Understanding how Linux interacts with cloud concepts is critical for modern infrastructure.

#### `stress` (CPU testing)
- **What:** A tool designed to impose load on and stress test a computer system.
- **Why:** To test auto-scaling groups in AWS. You intentionally stress the CPU to 100% to see if AWS successfully launches a new backup server.
- **How:** `stress --cpu 4 --timeout 60`
- **Impact:** Ensures that your architecture correctly handles traffic spikes like Black Friday sales.

#### `lsblk`
- **What:** Lists information about all available or specified block devices (hard drives, flash drives).
- **Why:** Used to verify if a newly attached AWS EBS volume is actually recognized by the operating system.
- **How:** `lsblk`
- **Impact:** Essential first step for expanding server storage in the cloud.

#### EBS Volume Attach
- **What:** The AWS action of plugging an Elastic Block Store (hard drive) into an EC2 instance (server).
- **Why:** Applications grow. Databases need more storage. You attach EBS volumes to fulfill these requirements.
- **How:** Done via AWS Console/CLI. In Linux, verify changes with `lsblk`.
- **Impact:** Provides decoupled, persistent storage, ensuring data isn't lost if the instance terminates.

#### `mkfs.ext4`
- **What:** Make File System. Formats a raw hard drive into the ext4 file system.
- **Why:** A brand new EBS volume from AWS is totally blank. Before you can store files on it, it must be formatted.
- **How:** `sudo mkfs.ext4 /dev/xvdf`
- **Impact:** Prepares storage for use. Think of it like formatting a new USB stick before first use.

#### `tmux`
- **What:** Terminal Multiplexer. It lets you create multiple "windows" inside one terminal session and keeps them running even if your internet disconnects.
- **Why:** If you run a long database backup script and your SSH drops, you lose the progress. With `tmux`, the script continues safely in the background.
- **How:** Type `tmux` to start, then run your command. Reattach later with `tmux attach`.
- **Impact:** Safely manages long-running infrastructure tasks without fear of network interruptions.

---

### E. File Transfer & Process Management (Harsh)

Handling files between environments and controlling backend processes safely.

#### `scp` (Upload/Download)
- **What:** Secure Copy Protocol. Used to securely transfer files between your local machine and a remote server.
- **Why:** You built a new configuration file locally and need to push it strictly to the production server.
- **How:** `scp -i key.pem app.zip user@server_ip:/var/www/`
- **Impact:** A fast, secure alternative to setting up FTP servers, standard for quick manual transfers.

#### `nohup`
- **What:** "No Hang Up". Runs a command immune to hangups, meaning it ignores the disconnect signal if you log out.
- **Why:** Used to start a background application so it stays running indefinitely after you close your laptop.
- **How:** `nohup node server.js &`
- **Impact:** Creates quick, simple background services for small applications without writing complex systemd configurations.

#### `kill -9`
- **What:** Sends a SIGKILL signal to forcefully terminate a process immediately.
- **Why:** Sometimes, a broken application "hangs" and refuses to shut down via normal means. 
- **How:** First find the process ID (PID) via `top`, then run: `kill -9 1234`
- **Impact:** The ultimate "off switch" to kill runaway processes that are freezing up the server.

---

### F. Log Management (Shiv)

Keeping logs under control so they don't destroy the system.

#### Log Rotation
- **What:** The automated process of archiving old log files, compressing them, and creating new, empty ones.
- **Why Logs Need Rotation:** A busy web server can generate Gigabytes of logs a day. Without rotation, the disk reaches 100%, causing the whole application to crash beautifully.
- **Configuration Basics:** Linux uses `logrotate`. It's configured via `/etc/logrotate.conf` and rules in `/etc/logrotate.d/`. You define how daily/weekly the logs rotate, how many to keep, and if they should be compressed.
- **Nginx Example:** 
  You can set up `logrotate` for Nginx so it compresses logs daily and only keeps the last 14 days, deleting older ones automatically:
  ```text
  /var/log/nginx/*.log {
      daily
      missingok
      rotate 14
      compress
      delaycompress
      notifempty
      create 0640 www-data adm
      sharedscripts
      postrotate
          [ -s /run/nginx.pid ] && kill -USR1 `cat /run/nginx.pid`
      endscript
  }
  ```

---

## Real-World DevOps Use Cases

- **Troubleshooting Server Issues:** Checking why the website is down by SSH-ing into the server, looking at `htop` for spiked CPU, using `free -h` for memory, and `tail -f`ing the application logs to read the error.
- **Deploying Applications:** Using `scp` to send the new build artifact to the server, running `sudo chown` to ensure the web server has rights to read it, and restarting the service.
- **Monitoring Production Systems:** Writing bash scripts utilizing `vmstat` and `uptime` to alert the team when system load is uncharacteristically high before an actual outage occurs.
- **Managing Logs:** Setting up `logrotate` to prevent application logs from silently filling up the cloud VM disk space.

---

## Interview Preparation Section

Here are some common, beginner-friendly interview questions related to this session:

1. **What is the difference between `top` and `htop`?**
    - **Answer:** Both show running processes and system resources. However, `htop` offers a visually appealing, colorful interface, allows vertical/horizontal scrolling, and you can kill processes interactively without remembering the PID.

2. **What happens when the root partition (Disk) is 100% full?**
    - **Answer:** The system often crashes or becomes entirely unresponsive. Applications fail to write logs, databases can corrupt, and you usually cannot even log in via SSH or run basic commands.

3. **How do you securely transfer a file to a remote server?**
    - **Answer:** Using `scp` (Secure Copy Protocol) which encrypts the file transfer over SSH.

4. **What is the significance of the `chmod 777` command, and why is it dangerous?**
    - **Answer:** It grants Read, Write, and Execute permissions to *everyone* (Owner, Group, Public). It is a major security risk, allowing maliciously actors or bugs to alter or execute critical files. 

5. **What is log rotation?**
    - **Answer:** It’s an automated process that archives, compresses, and eventually deletes old log files, preventing them from growing infinitely and consuming all disk space.

6. **Why do we use the `nohup` command?**
    - **Answer:** It allows a process to continue running in the background even after you disconnect from your SSH terminal session. 

7. **How do you check memory usage in Linux?**
    - **Answer:** By using the `free -h` command to see available and used memory in human-readable sizes like MB or GB.

8. **If an AWS instance fails a status check, how might `uptime` help diagnose it?**
    - **Answer:** Looking at `uptime` allows you to see the load averages to determine if the server experienced massive CPU spikes, or if it had randomly rebooted just recently.

9. **You have a process hanging. How do you force-stop it?**
    - **Answer:** First find its PID (Process ID) using `top` or `ps`, and then execute `kill -9 <PID>` to send a forcefully terminate signal (SIGKILL).

10. **Explain the `sudo` command.**
    - **Answer:** "SuperUser Do" allows permitted users to run commands with the security privileges of the root user, ensuring elevated access is only used temporarily when needed.

11. **Why do we need to mount a disk?**
    - **Answer:** Linux requires hardware (like a new hard drive) to be mapped to a directory inside its virtual filesystem hierarchy before it can read or write files to it.

12. **How does `tmux` save DevOps engineers time?**
    - **Answer:** If your internet drops during a multi-hour network transfer or script execution, `tmux` prevents the session from dying, allowing you to re-attach exactly where you left off.

13. **What is the command to create an empty tracking file quickly?**
    - **Answer:** `touch filename.txt`

14. **How do you view live entries streaming into a log file?**
    - **Answer:** Use the command `tail -f /path/to/log`.

15. **What is the purpose of `mkfs.ext4`?**
    - **Answer:** It works like "formatting" a raw disk. It lays down the ext4 file system structure so the OS can start organizing files on newly attached hardware.

---

## Best Practices / Tips

1. **Never use `root` carelessly:** Always log in as a regular user and use `sudo` for administrative actions.
2. **Double check `rm -rf`:** Running remove recursive-force is dangerous. Always do an `ls` on the target path before running the delete command.
3. **Use Tab Completion:** Pressing the `Tab` key auto-completes folder and file names, reducing typos and speeding up navigation.
4. **Use `-h` where possible:** Always use human-readable flags (`free -h`, `df -h`, `ls -lh`) so you don’t have to manually calculate bytes.
5. **Alias long commands:** If you repeatedly type a long string like `kubectl get pods --namespace=production`, create an alias in your `~/.bashrc` to save time.
6. **Prioritize Log Rotation:** The minute you deploy an application, immediately set up log rotation. Don't wait until production crashes.
7. **Never trust memory; document everything:** Create markdown plays-books (like this one) for every server action you perform.
8. **Keep Private Keys Private:** A `.pem` file should always have `chmod 400` permissions. If it's more open, SSH typically refuses to use it anyway for security reasons.

---

### Navigation

- ⬅️ Previous: [14_AWS_EC2_AMI_EBS_LoadBalancer.md](./14_AWS_EC2_AMI_EBS_LoadBalancer.md)  
- ➡️ Next: [16.aws-s3-static-website-hosting.md](./16.aws-s3-static-website-hosting.md)  
