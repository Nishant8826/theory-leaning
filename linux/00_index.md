# 00_index.md: Linux for the Real-World Developer

Organized into practical modules mapped to our tech stack workflows.

### 1. Linux Fundamentals
*File system, permissions, users, processes, networking basics*

*   [01_linux_overview.md](01_linux_overview.md) - The heart of the internet and why Linux is an industry superstar.
*   [02_linux_architecture_shell.md](02_linux_architecture_shell.md) - The 3 layers of Linux and the terminal waiter.
*   [03_filesystem_hierarchy.md](03_filesystem_hierarchy.md) - The root tree analogy and navigating critical system folders.
*   [04_basic_commands.md](04_basic_commands.md) - Core commands for navigating, managing, and viewing files.
*   [05_user_management.md](05_user_management.md) - Creating users, setting passwords, and granting root powers.
*   [06_file_permissions.md](06_file_permissions.md) - Understanding octal permissions and securing file operations.
*   [07_linux_boot_process.md](07_linux_boot_process.md) - The step-by-step journey from power button to login prompt.

### 2. Developer Workflow (Node.js / Python)
*Running Node apps (`npm`, `pm2`, `node`), Python environments (`venv`, `pip`), Environment variables (`.env`, export, dotenv), Logs and debugging (`tail`, `grep`, `journalctl`)*

*   [08_process_management.md](08_process_management.md) - Using `ps`, `top`, and `kill` to manage running processes.
*   [09_logs_debugging.md](09_logs_debugging.md) - Tailing `/var/log` events and finding bugs in real-time.
*   [10_linux_day_to_day_tasks.md](10_linux_day_to_day_tasks.md) - Common tasks you'll perform daily as a developer or sysadmin.

### 3. Frontend Deployment
*Build tools (`npm run build`), Serving static files (`nginx`, `serve`), Handling ports & processes*

*   [11_package_management.md](11_package_management.md) - Installing packages and dependencies for application serving.

### 4. Backend & APIs
*Running servers (Node.js, Express), Process managers (`pm2`, `systemd`), API testing via CLI (`curl`)*

*   [12_service_management.md](12_service_management.md) - Controlling background workers, PM2 equivalent concepts, and `systemctl`.
*   [13_http_status_codes.md](13_http_status_codes.md) - Knowing HTTP response mechanisms and tracking server errors analytically.

### 5. Databases
*MongoDB CLI basics, MySQL/PostgreSQL CLI usage, Redis CLI, Backup & restore commands*

*(Note: Essential database checks are mapped through system monitoring tips and advanced bash commands in the cheatsheet.)*

### 6. DevOps & AWS
*SSH into EC2, File transfer (`scp`, `rsync`), Managing services, Logs & monitoring, Working with S3 via CLI*

*   [14_system_monitoring.md](14_system_monitoring.md) - Checking server health and diagnosing disk space issues.
*   [15_ssh_key_management.md](15_ssh_key_management.md) - Logging securely into EC2 without using passwords.

### 7. Networking & Security
*Ports, firewalls (`ufw`, `iptables`), SSH config, Permissions & secrets handling*

*   [16_networking.md](16_networking.md) - Making computers talk efficiently, pinging hosts, and diagnosing port problems.

### 8. Automation & Scripting
*Bash scripting basics, Cron jobs, Automating deployments*

*   [17_vi_editor.md](17_vi_editor.md) - Handling text file edits strictly from inside the terminal.
*   [18_shell_scripting_basics.md](18_shell_scripting_basics.md) - Creating `.sh` magic to automate deploying builds flawlessly.

### 9. AI / API Workflows
*Calling APIs via curl, Handling JSON in CLI (`jq`), Testing LLM endpoints*

*   [19_advanced_commands.md](19_advanced_commands.md) - Finding items and structuring data output queries correctly.
*   [20_linux_cheatsheet.md](20_linux_cheatsheet.md) - Ultimate manual for advanced queries, grep text streams, and more.
*   [21_linux_tips_2026.md](21_linux_tips_2026.md) - Contemporary workflow adaptations for real-world modern environments.

### 10. Advanced Linux Mastery
*Reverse Proxies, Hardening Servers, Disk Partitions, and Mounts*

*   [22_web_servers_nginx.md](22_web_servers_nginx.md) - Mastering Nginx for Reverse Proxy and Load Balancing.
*   [23_storage_lvm_management.md](23_storage_lvm_management.md) - Disk management, formatting, and mounting AWS EBS volumes.
*   [24_security_firewalls.md](24_security_firewalls.md) - Hardening servers with UFW, Fail2ban, and secure SSH configs.

---
Prev: None | Index: [00_index.md](00_index.md) | Next: [01_linux_overview.md](01_linux_overview.md)
---
