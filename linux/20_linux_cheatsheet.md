# 🗺️ The Ultimate Linux Cheatsheet

Bookmark this page! This is your "Cheat Code" for surviving inside the Linux terminal.

## 📂 Navigation & Files
| Command | Action |
| :--- | :--- |
| `pwd` | **Print Working Directory** (Outputs the full absolute path of your current location). |
| `cd ..` | **Go back one directory level** (Moves up to the parent folder).<br>`..`: Represents the parent directory. |
| `cd -` | **Go to previous directory** (Instantly toggle back to the last folder you were in).<br>`-`: Represents the previous working directory. |
| `ls -lh` | **List files with human-readable sizes** (e.g., 1K, 234M, 2G instead of raw bytes).<br>`-l`: Long listing format. `-h`: Human-readable sizes. |
| `ls -la` | **List ALL files in detailed format** (Shows hidden files, permissions, owner, and modification date).<br>`-l`: Long listing format. `-a`: Include hidden files (starting with '.'). |
| `mkdir -p a/b/c` | **Make nested directories at once** (Creates parent folders if they don't exist without throwing an error).<br>`-p`: Creates parent directories as needed. |
| `touch file` | **Create an empty file** (Or updates the modification timestamp if the file already exists). |
| `cp -r src dest` | **Copy directory recursively** (Copies a folder and everything inside it to a new destination).<br>`-r`: Recursive copy. |
| `mv old new` | **Move or Rename** (Moves a file/folder to a new location, or renames it if kept in the same directory). |
| `rmdir folder` | **Remove an empty directory** (Fails safely if the folder still contains files). |
| `rm -rf folder` | **FORCE Delete a directory and all its contents** (Bypasses prompts, deletes recursively. Use with extreme caution!).<br>`-r`: Recursive deletion. `-f`: Force deletion without prompts. |
| `file info.txt` | **Determine file type** (Looks at the file's contents, not just the extension, to tell you what it is). |
| `tree` | **Show directory structure as a tree** (Provides a visual hierarchy of all subfolders and files). |
| `ln -s file link` | **Create a symbolic link** (Creates a shortcut to a file or directory; deleting the shortcut keeps the original).<br>`-s`: Create soft (symbolic) link instead of hard link. |
| `stat file` | **Display file or file system status** (Shows detailed timestamps, size, blocks, and inode information). |

## 🛠️ System Information & Control
| Command | Action |
| :--- | :--- |
| `date` / `cal` | **Show current date/time** or display a text-based terminal calendar. |
| `uname -a` | **Show system info** (Prints detailed kernel version, system hostname, and architecture details).<br>`-a`: Print all system information. |
| `history` | **Show previously executed commands** (Great for remembering and reusing long commands you typed earlier). |
| `sudo !!` | **Run the last command with admin privileges** (Fixes "Permission denied" errors without retyping the entire command).<br>`!!`: Re-runs the last executed command. |
| `lscpu` | **Display CPU information** (Shows number of cores, threads, architecture, and clock speeds of your processor). |
| `lsblk` | **List block devices** (Displays a tree of connected hard drives, SSDs, partitions, and their mount points). |
| `systemctl status app` | **Check status of an application service** (Verify if a service is actively running, failed, or stopped).<br>`status`: Show service state. |
| `systemctl restart app` | **Restart a background service** (Useful for applying new configuration changes to web servers, databases, etc.).<br>`restart`: Stop then start the service. |
| `journalctl -xe` | **View system logs for debugging** (Jumps to the end of the central system log to diagnose recent crashes or start failures).<br>`-x`: Add explanatory messages. `-e`: Jump to the end of the log. |

## 📈 Monitoring & Performance
| Command | Action |
| :--- | :--- |
| `uptime` | **See system uptime** (Shows how long the server has been running since the last reboot, and system load averages). |
| `free -m` | **Check RAM usage** (Shows total, used, and free system memory and swap space in Megabytes).<br>`-m`: Display sizes in megabytes. |
| `df -h` | **Check disk space** (Displays total, used, and available space on all mounted drives in readable formats like GB).<br>`-h`: Print human-readable sizes (e.g., 1K 234M 2G). |
| `top` / `htop` | **Interactive Task Manager** (Live view of CPU, RAM usage, and active processes. `htop` is visually friendlier). |
| `vmstat 1` | **Monitor virtual memory & system performance** (Continuously reports CPU, memory, and IO statistics).<br>`1`: Updates every 1 second continuously. |
| `iostat -x 1` | **Monitor disk I/O activity** (Detailed statistics on hard drive utilization, read/write speeds).<br>`-x`: Display extended statistics. `1`: Updates every 1 second. |
| `dmesg --level=err` | **Show kernel hardware errors** (Useful for diagnosing newly attached USB drives or hardware failures).<br>`--level=err`: Filter messages to show only errors. |
| `sar -u 1 3` | **Collect and report system activity** (Advanced historical monitoring of CPU, memory, and network).<br>`-u`: Report CPU utilization. `1`: Interval (1s). `3`: Count (3 times). |

## 🔄 Process Management
| Command | Action |
| :--- | :--- |
| `jobs` | **List active background jobs** (Shows applications that you've paused or sent to the background in the current session). |
| `bg` | **Resume a paused process in the background** (Frees up your terminal while the task continues running silently). |
| `fg` | **Bring a background process to the foreground** (Allows you to interact with a background job again). |
| `ps aux` | **List all running processes** (Provides a static snapshot of every process running on the system with user details).<br>`a`: All with tty. `u`: User-oriented format. `x`: Processes without controlling ttys. |
| `killall app_name` | **Kill all processes with a specific name** (e.g., `killall node` terminates every running Node.js server). |
| `kill -9 PID` | **Kill a frozen application forcefully** (Instantly terminates the Process ID without waiting for it to cleanly shut down).<br>`-9`: Sends SIGKILL signal. |
| `nohup cmd &` | **Run a command immune to hangups** (Ensures the script/command keeps running even if you disconnect from SSH).<br>`&`: Runs the process in the background. |

## 🔍 Searching & Text
| Command | Action |
| :--- | :--- |
| `cat file` | **Print file contents to screen** (Dumps the entire file output sequentially onto your terminal). |
| `head -n 5 file` | **See first 5 lines** (Useful to quickly peek at the structure of a massive log or CSV file).<br>`-n 5`: Show the first 5 lines. |
| `tail -f file` | **Watch new lines in real-time** (Perfect for continuously monitoring application logs as they are being written).<br>`-f`: Output appended data as the file grows. |
| `less file` | **Scroll through a large file** (Lets you safely navigate up and down massive files using arrow keys without freezing the terminal). |
| `wc -l file` | **Count the total number of lines** (Helpful for finding out how many entries are in a text file or database export).<br>`-l`: Print the newline counts. |
| `echo "text" >> file` | **Append text to file** (Safely adds the new text to the very end without deleting existing contents).<br>`>>`: Append redirector. |
| `echo "text" > file` | **Write text to file** (Completely overwrites the file with the new text. Creates the file if it doesn't exist).<br>`>`: Overwrite redirector. |
| `grep "text" file` | **Search inside a file** (Prints all lines within the file that contain the exact requested text pattern). |
| `grep -r "text" dir` | **Search recursively in a directory** (Scans every file in a folder to find which ones contain the matching word).<br>`-r`: Read all files under each directory, recursively. |
| `find . -name "file"` | **Search for a file by name** (Scans the current directory downwards to locate exact or wildcard file names).<br>`.`: Start search traversing from current directory. `-name`: Base of file name matches shell pattern. |
| `find . -size +100M` | **Find exceptionally large files** (Locates files larger than 100 Megabytes to help clear disk space).<br>`-size +100M`: Match files greater than 100 Megabytes. |
| `sort file` | **Sort lines alphabetically/numerically** (Reorders the text file lines from A-Z or lowest to highest). |
| `uniq file` | **Omit sequentially repeated lines** (Filters out immediately duplicated entries from the text file). |
| `diff file1 file2` | **Compare two files side-by-side** (Highlights the exact lines that were added, removed, or changed between them). |
| `awk '{print $1}'` | **Print the first column of text** (Splits each line by spaces and selectively shows only the desired column).<br>`$1`: Represents the first field (column) of the current record. |
| `sed -i 's/old/new/g' file` | **Find and replace text globally** (Inline replaces every occurrence of "old" with "new" without opening the file manually).<br>`-i`: Edit files in place. `s/`: Substitute command. `/g`: Global replacement flag. |

## 🌐 Networking & SSH
| Command | Action |
| :--- | :--- |
| `ping site.com` | **Check network connectivity** (Sends continuous packets to a domain to see if it's online and measure response latency). |
| `ip addr` / `ifconfig` | **Show your Network Interfaces & IPs** (Find out your machine's local assigned private IP address). |
| `curl -I site.com` | **Check Website HTTP headers/status** (Quickly ping a site to see if it returns a 200 OK or 404/500 Error).<br>`-I`: Fetch the headers only. |
| `wget url` | **Download file from the internet directly** (Pulls an image, archive, or script straight to your current directory). |
| `ssh user@ip` | **Connect securely to a remote server** (Opens a remote terminal session as the specified user). |
| `scp file user@ip:/path` | **Secure copy a file to a server** (Transfers local files to remote machines seamlessly over SSH protocol). |
| `traceroute site.com` | **Trace network path to a host** (Maps out every router hop your connection takes to reach the destination server). |
| `dig domain.com` | **Check DNS records** (Queries nameservers to display exact A, TXT, or MX records associated with a domain). |
| `netstat -tulpn` | **List open ports and listening applications** (Shows exactly what background applications are taking up which server ports).<br>`-t`: TCP connections. `-u`: UDP connections. `-l`: Listening server sockets. `-p`: PID/Program name. `-n`: Numeric addresses. |
| `ss -tulpn` | **Get modern socket statistics** (The faster, modern alternative to `netstat` for tracking active connections and ports).<br>`-tulpn`: Equivalent meaning to netstat parameters but faster processing. |
| `nmap site.com` | **Network discovery and port scanning** (Audits security by scanning which ports are publicly exposed on the target IP). |
| `rsync -avz src dest` | **Fast, versatile remote/local file-copying** (Synchronizes folders by sending only the changed files, saving bandwidth).<br>`-a`: Archive mode (preserves permissions/times). `-v`: Verbose output. `-z`: Compress file data during the transfer. |

## 🔐 Permissions & Users
| Command | Action |
| :--- | :--- |
| `whoami` | **Show current logged-in user** (Confirms exactly who you are acting as inside the terminal). |
| `passwd` | **Change your account password** (Prompts you securely to update the logged-in user's authentication password). |
| `su - logname` | **Switch user** (Completely swaps your shell session over to another user account, loading their environment variables).<br>`-`: Start the shell as a login shell with an environment similar to a real login. |
| `useradd name` | **Create a new system user** (Generates a brand new user profile, allowing a new person to log in). |
| `userdel user` | **Delete a user account** (Removes a specified account completely to revoke system access). |
| `groupadd group` | **Create a new system group** (Establishes a new group which you can bulk-assign permissions to). |
| `usermod -aG group user`| **Add a user to a specific system group** (e.g., Adding a normal user to the `sudo` or `docker` group to grant privileges).<br>`-a`: Append the user to the supplemental group(s). `-G`: Specify the group list. |
| `chown user:group file` | **Change owner and group** (Transfers the official ownership rights of a file or folder to another specific user/group). |
| `chmod 755 file` | **Change file permissions** (Updates numeric read/write/execute rights for the file's owner, group, and public users).<br>`7`: Owner has full rights. `5`: Group has read/execute. `5`: Others have read/execute. |

## 📦 Archiving & Compression
| Command | Action |
| :--- | :--- |
| `zip -r zipfile.zip dir` | **Zip a folder securely** (Zips up an entire directory recursively into a widely-supported .zip format).<br>`-r`: Travel the directory structure recursively. |
| `unzip zipfile.zip` | **Unzip a zip file** (Extracts contents from a .zip file into the current directory). |
| `gzip file` | **Compress single file** (Directly replaces a standalone file with a `.gz` compressed version to save space). |
| `gunzip file.gz` | **Uncompress a `.gz` file** (Restores the heavily compressed file back to its original readable state). |
| `tar -czvf pkg.tar.gz dir` | **Compress a folder into an archive** (Groups multiple files into one .tar and significantly shrinks size via gzip).<br>`-c`: Create archive. `-z`: Filter through gzip. `-v`: Verbose output. `-f`: Use given archive file. |
| `tar -xzvf pkg.tar.gz` | **Extract a tar.gz archive** (Decompresses and unpacking the archive contents blindly into your current directory).<br>`-x`: Extract files from an archive. `-z`: Uncompress gzip. `-v`: Verbose output. `-f`: Specify target archive file. |

## ⚙️ Package Management
| Command | Action |
| :--- | :--- |
| `apt update` | **Refresh available package lists** (Debian/Ubuntu: Syncs the system with repositories to find the newest versions of software). |
| `apt install pkg` | **Install a software package** (Debian/Ubuntu: Downloads and installs the application along with all missing dependencies). |
| `apt remove pkg` | **Remove a software package** (Debian/Ubuntu: Uninstalls the software but generally keeps the configuration files intact). |
| `yum install pkg` | **Install package** (RHEL/CentOS/Amazon Linux: Fetches and installs the desired application). |
| `dpkg -i pkg.deb` | **Install a local DEB file** (Manually force installs an offline `.deb` package file for Ubuntu/Debian).<br>`-i`: Install the package. |
| `rpm -i pkg.rpm` | **Install a local RPM file** (Bypasses the repository to manually inject an offline `.rpm` installation file).<br>`-i`: Install package. |

## 💾 Disk Management
| Command | Action |
| :--- | :--- |
| `du -sh dir` | **Estimate heavy file space usage** (Summarizes the total disk space consumed by a specific folder in a human-readable format).<br>`-s`: Display only a total for each argument. `-h`: Print sizes in human readable format (e.g., 1K 234M 2G). |
| `fdisk -l` | **List all disk partition tables** (Exposes every hard drive attached to the system and their exact geometric partition sizes).<br>`-l`: List the partition tables for the specified devices. |
| `mount /dev/sda1 /mnt` | **Mount a file system** (Attaches a physical hard drive partition to a folder path so you can browse its files). |
| `umount /mnt` | **Unmount a file system** (Safely detaches the hard drive from the folder path, allowing physical removal). |

## 📝 Shortcuts & Variables
| Command | Action |
| :--- | :--- |
| `Ctrl + L` / `clear` | **Clear the terminal screen** (Wipes old output from your view, bringing the prompt fresh back to the top of the monitor). |
| `Ctrl + C` | **Terminate command execution** (Sends an interrupt signal to stop a freezing or infinitely looping command immediately). |
| `Ctrl + Z` | **Pause running command** (Suspends an active command and puts it in the background; you can resume it using `fg`). |
| `Ctrl + R` | **Reverse search terminal history** (Opens an interactive prompt where typing instantly matches your previously ran commands). |
| `alias name='cmd'` | **Create a shortcut command** (Assigns a long, complex command to a short easily-typable phrase for the current session). |
| `env` | **List all active environment variables** (Prints out everything currently exported, from PATH configurations to session details). |
| `export VAR="val"` | **Set an environment variable** (Stores data dynamically in memory that programs or scripts can read globally). |

## 🧠 Core Concepts Summary
*   **What:** A condensed quick-reference amalgamation of every imperative Linux command syntactically structured for fast retrieval.
*   **Why:** Retaining hundreds of exact command flags perfectly via human memory is unfeasible and unnecessary; references enable speed.
*   **How:** A modular layout grouping logic (Processes vs Networking vs Permissions) utilized actively by developers mid-development.
*   **Impact:** Empowers developers to bypass excessive web searching during crises and execute precise command flows instantly.

---
Prev: [19_advanced_commands.md](19_advanced_commands.md) | Index: [00_index.md](00_index.md) | Next: [21_linux_tips_2026.md](21_linux_tips_2026.md)
---
