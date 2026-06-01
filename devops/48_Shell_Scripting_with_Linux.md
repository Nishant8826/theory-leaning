# 48 – Shell Scripting with Linux (Bash)

> **Batch-43 | Shell Scripting for DevOps | Linux Automation**

---

## Table of Contents

1. [Shell Architecture](#1-shell-architecture)
2. [Types of Shells](#2-types-of-shells)
3. [What is a Shell Script?](#3-what-is-a-shell-script)
4. [Shebang (`#!/bin/bash`)](#4-shebang-binbash)
5. [File Permissions & `chmod`](#5-file-permissions--chmod)
6. [Variables & Command Substitution](#6-variables--command-substitution)
7. [Operators – AND (`&&`) and OR (`||`)](#7-operators--and--and-or-)
8. [Functions in Bash](#8-functions-in-bash)
9. [Loops & Sleep](#9-loops--sleep)
10. [Arithmetic in Bash](#10-arithmetic-in-bash)
11. [Cron vs Sleep](#11-cron-vs-sleep)
12. [If-Else Conditions](#12-if-else-conditions)
13. [Practical Scripts from Session](#13-practical-scripts-from-session)
14. [Visual Diagrams](#14-visual-diagrams)
15. [Scenario-Based Q&A](#15-scenario-based-qa)
16. [Interview Q&A](#16-interview-qa)
17. [Tech Stack Mapping](#17-tech-stack-mapping)
18. [Code / Practical Examples](#18-code--practical-examples)
19. [Navigation Footer](#navigation-footer)

---

## 1. Shell Architecture

### What
The **shell architecture** describes how a user's commands travel through layers to eventually reach the hardware.

```
User → Terminal → Shell → Kernel (OS) → Hardware
```

Each layer has a distinct job:

| Layer | What it is | Role |
|---|---|---|
| **Hardware** | Physical components (CPU, RAM, Disk, Network) | Executes actual operations |
| **Kernel** | Core of the OS; inner layer | Manages hardware resources (memory, CPU scheduling, I/O) |
| **Shell** | Upper layer connected to the terminal | Translates human commands into system calls for the kernel |
| **Terminal** | The window you type into | Interface between you and the shell |
| **User** | You | Types commands |

### Why
Without the shell, you'd need to write machine code (binary / assembly) to talk to the kernel. The shell gives you a human-readable way to control the entire operating system.

### How (Step-by-Step — What Happens When You Type `ls`)

```
1. You type:  ls -l
2. Terminal sends the input to the Shell (Bash)
3. Shell parses "ls" → finds it at /bin/ls
4. Shell makes a system call to the Kernel: "run /bin/ls with flag -l"
5. Kernel tells hardware to read the directory from disk
6. Disk sends data back to Kernel → Kernel to Shell → Shell prints to Terminal
7. You see the file listing
```

### Impact

| With a Shell | Without a Shell |
|---|---|
| Type `rm file.txt` to delete a file | Write raw system calls in C or assembly |
| Automate 1000 operations in a script | Run every operation manually |
| Chain commands, add logic, schedule tasks | No automation possible at OS level |

---

## 2. Types of Shells

### What
A shell is a program that reads your commands and executes them. There are **8 main types** of shells in Linux:

| Shell | Full Name | Key Characteristic |
|---|---|---|
| **Bash** | Bourne Again Shell | Most widely used; default on Ubuntu/Amazon Linux |
| **ZSH** | Z Shell | Bash superset; used in macOS; better autocomplete |
| **SH** | Bourne Shell | Original Unix shell; minimal, portable |
| **CSH** | C Shell | Syntax similar to C language |
| **TSH / TCSH** | TENEX C Shell | Improved CSH with history and editing |
| **KSH** | Korn Shell | Combines SH and CSH features |
| **Dash** | Debian Almquist Shell | Minimal, fast; used for system scripts in Debian |
| **Fish** | Friendly Interactive Shell | User-friendly, colorful; not POSIX-compliant |

### Why Bash (99% Industry Use)?
- Default shell on nearly all Linux distributions (Ubuntu, CentOS, Amazon Linux, RHEL)
- POSIX compliant — scripts work across different Unix-like systems
- Massive community support and documentation
- Supports everything: variables, loops, functions, arrays, conditionals

### How to Check Your Current Shell
```bash
echo $SHELL          # shows your default shell path
echo $0              # shows currently running shell
cat /etc/shells      # lists all installed shells on the system
chsh -s /bin/zsh     # change default shell to ZSH (requires re-login)
```

---

## 3. What is a Shell Script?

### What
A **shell script** is a plain text file containing a **set of Linux commands written in order**, saved with a `.sh` extension, and executed **sequentially** (one by one, top to bottom).

> Think of it as a **recipe**: each line is a step, executed in order, to achieve a result.

### Why
- **Automation** — Replace repetitive manual commands with a single script run
- **Consistency** — Same script produces same result every time (no human error)
- **Speed** — 50 commands run in seconds instead of minutes of manual typing
- **Scheduling** — Scripts can be scheduled (cron) to run without any human presence

### How (Creating and Running a Script)

```bash
# Step 1: Create the file
nano my_script.sh

# Step 2: Write commands inside (with shebang at top)
#!/bin/bash
echo "Hello, DevOps!"
pwd
ls -l

# Step 3: Save and exit (Ctrl+O, Enter, Ctrl+X in nano)

# Step 4: Make it executable
chmod +x my_script.sh

# Step 5: Run it
./my_script.sh

# Alternative: run without chmod using bash directly
bash my_script.sh
```

### Impact

| With Shell Scripts | Without Shell Scripts |
|---|---|
| Server health check in 1 command | SSH into server, run 10 commands manually |
| New server setup automated (30 min → 2 min) | Click through setup manually every time |
| Log cleanup scheduled nightly | Remember to do it manually, sometimes forget |
| Consistent deployments | Steps missed, environments differ |

---

## 4. Shebang (`#!/bin/bash`)

### What
The **shebang** (also called hashbang) is the very first line of a shell script:

```bash
#!/bin/bash
```

It tells the operating system **which interpreter to use** to run this script.

- `#!` — the shebang characters (OS recognizes this as a special directive)
- `/bin/bash` — the full path to the Bash interpreter

### Why
- Without a shebang, the OS uses the **current user's default shell** — which may not be Bash
- If someone runs your script in a ZSH or Dash environment, it might behave differently or fail
- The shebang guarantees your script **always runs with Bash**, regardless of environment

### How
```bash
#!/bin/bash           # use Bash (most common in DevOps)
#!/bin/sh             # use POSIX sh (more portable but fewer features)
#!/usr/bin/env bash   # find bash wherever it's installed (best for portability)
#!/usr/bin/python3    # use Python (yes, shebang works for Python scripts too!)
```

> The `#!` looks like a comment to the shell, but the **operating system reads it first** before handing the file to any shell. It's not a comment — it's an OS instruction.

### Impact

| With Shebang | Without Shebang |
|---|---|
| Script always runs with Bash | Runs with whatever shell the user happens to have |
| Predictable behavior across systems | Different output on different machines |
| Can run as `./script.sh` directly | Must always run as `bash script.sh` |

---

## 5. File Permissions & `chmod`

### What
In Linux, every file has **permissions** that control who can read, write, or execute it. A shell script file needs **execute permission** before it can be run directly.

### Understanding Permissions

```bash
ls -l my_script.sh
# -rw-r--r-- 1 ubuntu ubuntu 245 May 28 10:00 my_script.sh
#  ↑↑↑↑↑↑↑↑↑
#  │││││││││
#  ││││││└└└── Other:  r-- = read only
#  │││└└└──── Group:  r-- = read only
#  └└└──────── Owner:  rw- = read + write (no execute yet)
```

Permission characters:
- `r` = read (4)
- `w` = write (2)
- `x` = execute (1)
- `-` = no permission (0)

### How to Add Execute Permission

```bash
# Add execute permission for owner only (recommended)
chmod +x my_script.sh
# Result: -rwxr--r--

# Numeric method — owner: read+write+execute (7), group: read (4), other: read (4)
chmod 744 my_script.sh

# Run the script
./my_script.sh
```

### Why NEVER Use `chmod 777` in Production

`chmod 777` gives **everyone** (owner + group + all others) read + write + execute permission.

```
777 = rwxrwxrwx
       ↑↑↑ ↑↑↑ ↑↑↑
       Owner  Group  Others
       ALL    ALL    ALL  ← DANGEROUS
```

**Security risks:**
- Any user on the system can modify your script
- An attacker who gains any access can alter and execute your scripts
- A modified script with root privileges = full system compromise

### Production Best Practices

| Scenario | Permission | Command |
|---|---|---|
| Owner runs only | `700` | `chmod 700 script.sh` |
| Owner + group runs | `750` | `chmod 750 script.sh` |
| Owner runs + group reads | `740` | `chmod 740 script.sh` |
| **NEVER in production** | `777` | ❌ Do not use |

---

## 6. Variables & Command Substitution

### What
**Variables** store values (text, numbers, command output) that your script can reuse. You declare them, then reference them with a `$` prefix.

### How — Declaring and Using Variables

```bash
#!/bin/bash

# Declare a variable (no spaces around =)
name="DevOps Engineer"
version=3
environment="production"

# Use the variable with $
echo "Hello, $name"
echo "Version: $version"
echo "Deploying to: $environment"
```

**Rules:**
- No spaces around `=` (`name = "value"` is WRONG, `name="value"` is correct)
- Reference with `$name` or `${name}` (curly braces avoid ambiguity)
- Use **double quotes** `"$name"` to preserve spaces in values

### Command Substitution

**Command substitution** captures the **output of a command** and stores it in a variable.

```bash
# Syntax: $(command)  ← modern, preferred
# Old syntax: `command`  ← backticks (works but avoid)

current_user=$(whoami)         # runs 'whoami', stores the output
current_date=$(date +%Y-%m-%d) # stores today's date
server_ip=$(hostname -I)       # stores server's IP address
disk_usage=$(df -h / | tail -1) # stores the root disk usage line

echo "Logged in as: $current_user"
echo "Date: $current_date"
echo "Server IP: $server_ip"
```

### Special Variables

| Variable | Meaning |
|---|---|
| `$0` | Name of the script itself |
| `$1`, `$2`, ... | Arguments passed to the script |
| `$#` | Number of arguments passed |
| `$?` | Exit code of last command (0 = success, non-0 = error) |
| `$$` | PID (Process ID) of the script |
| `$USER` | Current logged-in username |
| `$HOME` | Home directory path |
| `$PWD` | Current working directory |

```bash
# Example: script called with arguments
# ./deploy.sh myapp production

app_name=$1      # myapp
env=$2           # production
echo "Deploying $app_name to $env environment"
```

---

## 7. Operators – AND (`&&`) and OR (`||`)

### What
Bash operators let you **chain commands** and control what runs based on whether the previous command succeeded or failed.

### AND (`&&`) — "Only if previous succeeded"

```bash
command1 && command2
```
`command2` runs **only if** `command1` exits with code `0` (success).

```bash
# Real example: Only deploy if tests pass
npm test && npm run deploy

# Only create a folder if it doesn't exist
mkdir /app/logs && echo "Logs directory created"

# Only restart service if config file updated successfully
cp nginx.conf /etc/nginx/ && systemctl restart nginx
```

### OR (`||`) — "Run this if previous FAILED"

```bash
command1 || command2
```
`command2` runs **only if** `command1` exits with a non-zero code (failure).

```bash
# If directory creation fails, print an error
mkdir /app/logs || echo "ERROR: Could not create logs directory"

# If service fails to start, send an alert
systemctl start myapp || echo "Service failed to start" | mail -s "ALERT" admin@company.com
```

### Combining Both

```bash
# Run all three, but stop at first failure
apt-get update && apt-get install -y nginx && systemctl start nginx
```

### Impact

| With `&&` / `||` | Without them |
|---|---|
| Deploy only if build succeeds | Deploy even after failed build |
| Alert only when something fails | Alert every time regardless |
| Safe command chaining | Blind sequential execution |

---

## 8. Functions in Bash

### What
A **function** is a named, reusable block of commands. You define it once and call it by name as many times as needed.

### Why
- Avoid repeating the same commands in multiple places
- Break complex scripts into readable, named sections
- Pass arguments to functions for flexible behavior

### How — Syntax

```bash
#!/bin/bash

# Define a function
function_name() {
    # commands go here
    echo "Inside the function"
}

# Call the function
function_name
```

### With Arguments

```bash
#!/bin/bash

greet_user() {
    local username=$1         # $1 = first argument passed to function
    echo "Hello, $username! Welcome to the server."
}

check_service() {
    local service=$1
    if systemctl is-active --quiet "$service"; then
        echo "✅ $service is running"
    else
        echo "❌ $service is NOT running"
    fi
}

# Call functions
greet_user "Alice"
greet_user "Bob"
check_service "nginx"
check_service "docker"
```

> `local` makes a variable **local to the function** — it won't interfere with variables outside it.

---

## 9. Loops & Sleep

### For Loop

Repeats a block of commands a specific number of times (or over a list).

```bash
#!/bin/bash

# Loop 5 times
for i in 1 2 3 4 5; do
    echo "Iteration: $i"
done

# Using seq (generates a sequence)
for i in $(seq 1 5); do
    echo "Count: $i"
done

# Loop with range syntax
for i in {1..5}; do
    echo "Step $i"
done

# Loop over a list of servers
for server in web1 web2 web3; do
    echo "Checking $server..."
    ping -c 1 $server
done
```

### While Loop

Repeats as long as a condition is true.

```bash
#!/bin/bash

count=1
while [ $count -le 5 ]; do
    echo "Count: $count"
    count=$((count + 1))
done
```

### `sleep` — Pause Between Iterations

```bash
#!/bin/bash

# Monitor process list every 30 seconds, 3 times
for i in 1 2 3; do
    echo "=== Check $i at $(date) ==="
    ps aux | grep nginx
    sleep 30    # wait 30 seconds before next iteration
done
```

### Why `sleep` Matters in DevOps

- Wait for an EC2 instance to boot before SSH-ing in
- Retry a failed API call after a delay
- Throttle monitoring loops to avoid hammering the system

---

## 10. Arithmetic in Bash

### What
Bash can do basic math using the `$((...))` syntax (called arithmetic expansion).

### How

```bash
#!/bin/bash

# Declare number variables
a=10
b=3

# Arithmetic operations
sum=$((a + b))
diff=$((a - b))
product=$((a * b))
quotient=$((a / b))     # integer division only (no decimals)
remainder=$((a % b))    # modulo

echo "Sum:       $sum"       # 13
echo "Diff:      $diff"      # 7
echo "Product:   $product"   # 30
echo "Quotient:  $quotient"  # 3
echo "Remainder: $remainder" # 1
```

> For **decimal arithmetic**, use `bc` (basic calculator):
```bash
result=$(echo "scale=2; 10 / 3" | bc)
echo $result   # 3.33
```

### DevOps Use Cases for Arithmetic

```bash
# Calculate disk usage percentage alert threshold
used=$(df / | tail -1 | awk '{print $5}' | tr -d '%')
if [ $used -gt 80 ]; then
    echo "⚠️ Disk usage critical: ${used}%"
fi

# Count failed log lines
error_count=$(grep -c "ERROR" /var/log/app.log)
echo "Errors today: $error_count"
```

---

## 11. Cron vs Sleep

### What

Both `cron` and `sleep` deal with **time** in automation, but they work very differently.

| | `cron` | `sleep` |
|---|---|---|
| **Type** | System-level scheduler | In-script pause/delay |
| **Scope** | Runs independently of any script | Only works inside a running script |
| **Precision** | Specific time (e.g., every day at 2 AM) | Relative delay (wait X seconds) |
| **Persistence** | Runs forever on schedule | Stops when script exits |
| **Config location** | `crontab -e` | Inside `.sh` script |

### Cron — Scheduled Tasks

Cron runs commands on a schedule. Edit with `crontab -e`.

```
# Cron syntax:
# ┌──── minute (0-59)
# │  ┌──── hour (0-23)
# │  │  ┌──── day of month (1-31)
# │  │  │  ┌──── month (1-12)
# │  │  │  │  ┌──── day of week (0=Sun, 6=Sat)
# │  │  │  │  │
# *  *  *  *  *  command

# Examples:
0 2 * * *    /scripts/backup.sh           # Every day at 2:00 AM
*/5 * * * *  /scripts/health_check.sh     # Every 5 minutes
0 0 * * 0    /scripts/weekly_report.sh    # Every Sunday at midnight
30 8 1 * *   /scripts/billing_report.sh   # 1st of every month at 8:30 AM
```

### Sleep — In-Script Delays

```bash
#!/bin/bash

# sleep units: s=seconds, m=minutes, h=hours, d=days
sleep 30        # wait 30 seconds
sleep 5m        # wait 5 minutes
sleep 2h        # wait 2 hours

# Example: retry loop with sleep
for attempt in 1 2 3; do
    if curl -s http://myapp/health | grep -q "ok"; then
        echo "App is healthy!"
        break
    else
        echo "Attempt $attempt failed. Retrying in 10 seconds..."
        sleep 10
    fi
done
```

### When to Use Which

| Use Case | Use |
|---|---|
| Run backup every night at 3 AM | `cron` |
| Wait 30 seconds after starting a service | `sleep` |
| Send weekly billing report every Monday | `cron` |
| Retry a failed API call 3 times with a delay | `sleep` in a loop |
| Clean old logs every Sunday | `cron` |
| Monitor disk every 60 seconds indefinitely | `cron` (not `sleep` in infinite loop) |

---

## 12. If-Else Conditions

### What
`if-else` lets your script make **decisions** based on conditions — run different commands depending on what's true.

### Syntax

```bash
#!/bin/bash

if [ condition ]; then
    # commands if condition is TRUE
elif [ another_condition ]; then
    # commands if second condition is TRUE
else
    # commands if ALL conditions are FALSE
fi
```

### Comparison Operators

**Numeric comparisons:**

| Operator | Meaning |
|---|---|
| `-eq` | equal to |
| `-ne` | not equal to |
| `-gt` | greater than |
| `-lt` | less than |
| `-ge` | greater than or equal |
| `-le` | less than or equal |

**String comparisons:**

| Operator | Meaning |
|---|---|
| `=` | strings are equal |
| `!=` | strings are not equal |
| `-z` | string is empty |
| `-n` | string is not empty |

**File checks:**

| Operator | Meaning |
|---|---|
| `-f` | file exists and is a regular file |
| `-d` | directory exists |
| `-e` | path exists (file or directory) |
| `-r` | file is readable |
| `-x` | file is executable |

### Examples

```bash
#!/bin/bash

# Numeric if-else
disk_usage=$(df / | tail -1 | awk '{print $5}' | tr -d '%')
if [ $disk_usage -gt 90 ]; then
    echo "🔴 CRITICAL: Disk at ${disk_usage}%"
elif [ $disk_usage -gt 75 ]; then
    echo "🟡 WARNING: Disk at ${disk_usage}%"
else
    echo "🟢 OK: Disk at ${disk_usage}%"
fi

# File check
if [ -f "/etc/nginx/nginx.conf" ]; then
    echo "Nginx config found"
else
    echo "ERROR: Nginx config missing!"
    exit 1
fi

# String check
environment=$1
if [ "$environment" = "production" ]; then
    echo "Deploying to PRODUCTION — double-checking..."
elif [ "$environment" = "staging" ]; then
    echo "Deploying to staging..."
else
    echo "Unknown environment: $environment"
    exit 1
fi
```

---

## 13. Practical Scripts from Session

### Script 1 – Basic System Info

```bash
#!/bin/bash
# Shows current directory, files, disk, and memory

echo "=== Current Directory ==="
pwd

echo "=== Files in Directory ==="
ls -l

echo "=== Disk Usage ==="
df -h

echo "=== Memory Usage ==="
free -h

echo "=== Creating a test file ==="
touch test_file.txt
echo "test_file.txt created."
```

---

### Script 2 – Variables & Command Substitution

```bash
#!/bin/bash
# Demonstrates variable declaration and command substitution

app_name="MyDevOpsApp"
version="2.1.0"
current_user=$(whoami)
hostname_val=$(hostname)
current_date=$(date '+%Y-%m-%d %H:%M:%S')

echo "Application: $app_name"
echo "Version:     $version"
echo "Deployed by: $current_user"
echo "Server:      $hostname_val"
echo "Timestamp:   $current_date"
```

---

### Script 3 – System Health Monitoring Report

```bash
#!/bin/bash
# System health report: hostname, IP, processes, memory, disk

echo "============================================"
echo "        SYSTEM HEALTH REPORT               "
echo "============================================"
echo "Hostname:    $(hostname)"
echo "IP Address:  $(hostname -I)"
echo "Date/Time:   $(date)"
echo ""
echo "--- Top Processes ---"
ps aux --sort=-%cpu | head -6

echo ""
echo "--- Memory Usage ---"
free -h

echo ""
echo "--- Disk Usage ---"
df -H

echo "============================================"
```

---

### Script 4 – Colorful Monitoring Report

```bash
#!/bin/bash
# Color-coded system health report

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'   # No Color (resets to default)

echo -e "${CYAN}============================================${NC}"
echo -e "${GREEN}        SYSTEM HEALTH REPORT               ${NC}"
echo -e "${CYAN}============================================${NC}"

echo -e "${YELLOW}Hostname:${NC}   $(hostname)"
echo -e "${YELLOW}IP Address:${NC} $(hostname -I)"
echo -e "${YELLOW}Date/Time:${NC}  $(date)"

echo -e "\n${BLUE}--- Top Processes ---${NC}"
ps aux --sort=-%cpu | head -6

echo -e "\n${BLUE}--- Memory Usage ---${NC}"
free -h

echo -e "\n${BLUE}--- Disk Usage ---${NC}"
df -H

# Disk alert
disk_pct=$(df / | tail -1 | awk '{print $5}' | tr -d '%')
if [ $disk_pct -gt 80 ]; then
    echo -e "\n${RED}⚠️  WARNING: Disk usage at ${disk_pct}%!${NC}"
fi

echo -e "${CYAN}============================================${NC}"
```

---

### Script 5 – Loop + Sleep (Process Monitor)

```bash
#!/bin/bash
# Runs PS command every 30 seconds, 3 times

echo "Starting process monitor (3 checks, 30s apart)..."

for i in 1 2 3; do
    echo ""
    echo "=== Check $i of 3 | $(date '+%H:%M:%S') ==="
    ps aux --sort=-%cpu | head -10
    
    if [ $i -lt 3 ]; then
        echo "Next check in 30 seconds..."
        sleep 30
    fi
done

echo ""
echo "Monitoring complete."
```

---

### Script 6 – Arithmetic Operations

```bash
#!/bin/bash
# Demonstrates arithmetic using $((...))

echo "Enter first number:"
read a

echo "Enter second number:"
read b

sum=$((a + b))
diff=$((a - b))
product=$((a * b))

echo "-------------------"
echo "$a + $b = $sum"
echo "$a - $b = $diff"
echo "$a × $b = $product"

# Guard against division by zero
if [ $b -ne 0 ]; then
    quotient=$((a / b))
    echo "$a ÷ $b = $quotient"
else
    echo "Cannot divide by zero."
fi
```

---

## 14. Visual Diagrams

### Shell Architecture Diagram

```
┌──────────────────────────────────────────────────────┐
│                     USER                            │
│              (types commands)                       │
└─────────────────────┬────────────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────────────┐
│                   TERMINAL                          │
│        (bash, xterm, PuTTY, iTerm, VS Code)        │
│         displays output ← sends input →            │
└─────────────────────┬────────────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────────────┐
│                    SHELL                            │
│              (Bash, ZSH, SH, etc.)                 │
│  • Interprets commands                              │
│  • Handles variables, loops, functions              │
│  • Makes system calls to Kernel                    │
└─────────────────────┬────────────────────────────────┘
                      │  system calls
                      ▼
┌──────────────────────────────────────────────────────┐
│                    KERNEL                           │
│          (Core OS — innermost layer)               │
│  • Manages CPU, Memory, File I/O, Networking       │
│  • Talks directly to hardware drivers              │
└─────────────────────┬────────────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────────────┐
│                   HARDWARE                          │
│         (CPU, RAM, SSD, NIC, GPU...)               │
└──────────────────────────────────────────────────────┘
```

---

### Shell Script Execution Flow

```
script.sh (text file)
        │
        │ chmod +x   (make executable)
        │
        ▼
./script.sh  (executed)
        │
        │ OS reads line 1: #!/bin/bash
        │ → "use /bin/bash to run this"
        │
        ▼
Bash Interpreter reads line 2
        │ → executes command
        │ → captures output
        │ → moves to line 3
        ▼
Bash reads line 3
        │ → executes command
        │ → ...
        ▼
Script ends (exit code 0 = success)
```

---

### Cron vs Sleep Decision Flow

```
Need time-based automation?
           │
           ▼
    Is it recurring on a schedule?
    (every night, every 5 minutes, every Monday)
           │
     ┌─────┴──────┐
    YES            NO
     │              │
     ▼              ▼
  Use CRON        Is it a delay WITHIN a script?
  crontab -e      (wait after a command, retry loop)
                       │
                 ┌─────┴──────┐
                YES            NO
                 │              │
                 ▼              ▼
             Use SLEEP      Reconsider if
             sleep 30       automation is needed
```

---

### File Permission Structure

```
Permission String:  - r w x r - x r - -
                    │ │ │ │ │ │ │ │ │ │
                    │ └─┬─┘ └─┬─┘ └─┬─┘
                    │  Owner  Group Other
                    │
                    └── File type: - = regular file
                                   d = directory
                                   l = symlink

Numeric:            Owner: rwx = 4+2+1 = 7
                    Group: r-x = 4+0+1 = 5
                    Other: r-- = 4+0+0 = 4
                    chmod 754 file.sh
```

---

### DevOps Shell Scripting Ecosystem

```
Shell Scripts in DevOps
         │
         ├── System Monitoring
         │       └── health_check.sh → cron → CloudWatch / Slack alert
         │
         ├── Log Management
         │       └── log_rotate.sh → cron → compress old logs → upload to S3
         │
         ├── Deployment
         │       └── deploy.sh → Jenkins pipeline stage → restart service
         │
         ├── User Management
         │       └── create_users.sh → loop over list → useradd + permissions
         │
         ├── Backup
         │       └── backup.sh → cron → dump DB → tar + gzip → S3 upload
         │
         └── Process Management
                 └── watchdog.sh → cron every 5 min → check service → restart if down
```

---

## 15. Scenario-Based Q&A

---

🔍 **Scenario 1:** You manage 20 EC2 servers. Every morning you need to check disk usage on all of them. Doing it manually via SSH takes 45 minutes. How do you automate it?

✅ **Answer:** Write a shell script `disk_check.sh` that loops over a list of server IPs, SSHes into each one, and runs `df -H`. Use `ssh -i key.pem user@$server "df -H"` inside the loop. Schedule it with cron at 8 AM daily (`0 8 * * * /scripts/disk_check.sh >> /var/log/disk_report.log`). One script, zero manual effort, logged output you can review.

---

🔍 **Scenario 2:** Your Jenkins deploy script starts the application but the app takes 15 seconds to be ready. The next pipeline step tries to hit the app's health endpoint immediately and fails. What do you do?

✅ **Answer:** Add a `sleep 15` after the start command in your shell script to give the app time to initialize. Or better — write a retry loop: check the health endpoint every 5 seconds, up to 10 attempts, and only proceed when it returns `200 OK`. This is more reliable than a fixed sleep.

---

🔍 **Scenario 3:** A junior engineer in your team accidentally ran `chmod 777` on all scripts in `/scripts/prod/`. What's the risk and how do you fix it?

✅ **Answer:** `chmod 777` gives every user on the system read, write, and execute access. Anyone who gains shell access (even a low-privilege user or a compromised service account) can now modify and run your production scripts — potentially injecting malicious commands. Fix immediately: `chmod 750 /scripts/prod/*.sh` to give owner full access, group read+execute, and strip all other access. Audit who modified scripts using `stat` and check git diff if scripts are version-controlled.

---

🔍 **Scenario 4:** You're asked to write a deployment script that only deploys if the current environment is "production" or "staging", and rejects any other value with an error message.

✅ **Answer:** Use an if-elif-else block in the script:
```bash
env=$1
if [ "$env" = "production" ]; then
    echo "Deploying to production..."
    # deploy commands
elif [ "$env" = "staging" ]; then
    echo "Deploying to staging..."
    # deploy commands
else
    echo "ERROR: Unknown environment '$env'. Use 'production' or 'staging'."
    exit 1
fi
```
The `exit 1` stops the script and signals failure to Jenkins so the pipeline halts.

---

🔍 **Scenario 5:** You need a script that automatically restarts the Nginx web server if it goes down, checks every 5 minutes, and sends an alert when it restarts. How do you build this?

✅ **Answer:**
```bash
#!/bin/bash
if ! systemctl is-active --quiet nginx; then
    systemctl restart nginx
    echo "Nginx was down. Restarted at $(date)" | \
      mail -s "ALERT: Nginx Restarted" admin@company.com
fi
```
Save as `/scripts/nginx_watchdog.sh`, `chmod 750`, add to cron: `*/5 * * * * /scripts/nginx_watchdog.sh`. Now Nginx self-heals every 5 minutes.

---

🔍 **Scenario 6:** Your team has a script that creates AWS resources. It uses hardcoded values like `us-east-1` and `t3.micro` throughout the file. You need to make it flexible for different environments.

✅ **Answer:** Replace all hardcoded values with variables declared at the top of the script (or read from environment variables / arguments):
```bash
REGION=${1:-"us-east-1"}
INSTANCE_TYPE=${2:-"t3.micro"}
ENVIRONMENT=${3:-"dev"}
```
Now calling `./provision.sh ap-south-1 t3.large production` overrides the defaults. The script becomes reusable for every environment without editing code.

---

## 16. Interview Q&A

---

**Q1. What is a shell and how is it different from the kernel?**

**A:** The kernel is the core of the OS — it manages hardware (CPU, RAM, I/O) and runs in a privileged mode. Users cannot interact with the kernel directly. The shell is the outer layer that sits between the user and the kernel. It takes human-readable commands from the terminal, interprets them, and passes them to the kernel as system calls. Think of it as: Kernel = engine of a car; Shell = steering wheel and dashboard.

---

**Q2. What is a shebang and why is it important?**

**A:** A shebang (`#!/bin/bash`) is the first line of a shell script. It tells the operating system which interpreter to use to execute the script. Without it, the OS uses the current user's default shell, which may not be Bash — causing unpredictable behavior. The shebang guarantees the script always runs with the intended interpreter, regardless of who runs it or what shell they use.

---

**Q3. What is the difference between `cron` and `sleep` in shell scripts?**

**A:** `cron` is a system-level scheduler that runs scripts at specific times (e.g., every night at 2 AM) completely independently. It runs whether or not any script is currently running. `sleep` is an in-script command that pauses execution for a specified duration before the next line runs — it only works while the script is actively running. Use `cron` for recurring scheduled tasks; use `sleep` for delays and retries within a script.

---

**Q4. Why should you never use `chmod 777` in production?**

**A:** `chmod 777` grants read, write, and execute permission to ALL users (owner, group, and everyone else). In production, this means any user on the system — or any process running as any user — can modify and execute your script. If a script has elevated privileges (runs as root or has sudo), an attacker or compromised service can inject malicious commands. Production best practice is `chmod 700` (owner only) or `chmod 750` (owner + group).

---

**Q5. What is command substitution in bash and how do you use it?**

**A:** Command substitution captures the output of a command and assigns it to a variable. Syntax: `variable=$(command)`. For example: `current_date=$(date +%Y-%m-%d)` runs the `date` command and stores its output in `current_date`. You can then use `$current_date` anywhere in the script. It's used in DevOps scripts to dynamically capture server hostname, IP address, disk usage percentages, active process counts, etc.

---

**Q6. How do you use if-else conditions in bash? Give a real-world example.**

**A:** Bash if-else syntax uses `[ condition ]` brackets and the keywords `then`, `elif`, `else`, `fi`:
```bash
disk=$(df / | tail -1 | awk '{print $5}' | tr -d '%')
if [ $disk -gt 90 ]; then
    echo "CRITICAL: Disk at ${disk}%"
elif [ $disk -gt 75 ]; then
    echo "WARNING: Disk at ${disk}%"
else
    echo "OK: Disk at ${disk}%"
fi
```
Real-world use: health check scripts, environment validation in deploy pipelines, service availability checks.

---

**Q7. What is the difference between `&&` and `||` in bash?**

**A:** `&&` (AND) runs the next command **only if the previous command succeeded** (exit code 0). Example: `npm test && npm run deploy` — deploys only if tests pass. `||` (OR) runs the next command **only if the previous command failed** (non-zero exit code). Example: `systemctl start app || echo "Start failed"` — prints an error only if start fails. Together they allow conditional command chaining without writing full if-else blocks.

---

**Q8. How do you pass arguments to a shell script and use them inside?**

**A:** Arguments are passed on the command line: `./script.sh arg1 arg2`. Inside the script, they're accessed via positional parameters: `$1` (first argument), `$2` (second), etc. `$#` gives the count of arguments and `$0` is the script name itself. Example:
```bash
./deploy.sh myapp production
# Inside script:
app=$1     # myapp
env=$2     # production
echo "Deploying $app to $env"
```

---

**Q9. What Linux commands are typically used in a server monitoring script?**

**A:**
- `hostname` / `hostname -I` — server name and IP
- `uptime` — how long the server has been running
- `ps aux` / `top` — active processes and CPU/memory usage
- `df -H` — disk space by filesystem
- `free -h` — RAM and swap usage
- `netstat -tuln` / `ss -tuln` — open ports and listening services
- `tail -n 50 /var/log/syslog` — recent system logs
- `who` / `last` — currently logged in users

---

**Q10. What shell scripting activities would you write on your DevOps resume?**

**A:** Based on the session's guidance for 5–10 LPA roles:
- Linux administration and user management automation
- System monitoring and health reporting scripts
- Process management (service watchdog, auto-restart)
- Log management (rotation, compression, archival to S3)
- Automated deployment scripts for application servers
- Disk, CPU, and memory threshold alerting scripts
- Cron-based scheduled maintenance tasks

---

## 17. Tech Stack Mapping

### Shell Scripts in the DevOps Tool Chain

| Tool / Service | Shell Script Role |
|---|---|
| **Jenkins** | `sh 'bash deploy.sh'` in pipeline stages |
| **EC2 (AWS)** | User data scripts at instance launch; SSH-based remote scripts |
| **S3 (AWS)** | Upload artifacts/logs; sync directories via AWS CLI in scripts |
| **Docker** | Entrypoint scripts; build automation |
| **Nginx / Apache** | Config reload, vhost creation, SSL renewal scripts |
| **PostgreSQL / MongoDB** | Automated backup + compression + S3 upload scripts |
| **Node.js Apps** | Start/stop/restart scripts; environment setup before `npm start` |
| **Cron (Linux)** | Schedule all periodic DevOps maintenance tasks |
| **Slack / Email** | `curl` Slack webhook or `mail` command for alerts in scripts |

---

### Deployment Flow — Shell Scripts in a Node.js Stack

```
GitHub push → Jenkins webhook triggers pipeline
        │
        ├── Stage 1 (shell): ./scripts/setup.sh
        │   - apt-get update
        │   - install Node.js if missing
        │   - npm install
        │
        ├── Stage 2 (shell): ./scripts/test.sh
        │   - npm test
        │   - exit 1 if tests fail (stops pipeline)
        │
        ├── Stage 3 (shell): ./scripts/build.sh
        │   - npm run build
        │   - tar the build output
        │
        ├── Stage 4 (shell): ./scripts/deploy.sh
        │   - stop running process (pm2 stop app)
        │   - replace files with new build
        │   - pm2 start app --name "myapp"
        │   - sleep 10
        │   - curl health check
        │
        └── Stage 5 (shell): ./scripts/notify.sh
            - send Slack alert with deploy status
```

---

### Shell Monitoring Script → CloudWatch Metric

```
EC2 Server
    │
    ├── health_check.sh runs every 5 min (cron)
    │       - checks disk, memory, CPU, service status
    │       - if threshold exceeded: calls AWS CLI
    │
    │   aws cloudwatch put-metric-data \
    │     --metric-name DiskUsage \
    │     --value $disk_pct \
    │     --namespace CustomMetrics
    │
    └── CloudWatch triggers alarm if metric > 80%
            → SNS notification → Slack / Email
```

---

## 18. Code / Practical Examples

### Example 1: Full Server Setup Script (New EC2 Instance)

```bash
#!/bin/bash
# new_server_setup.sh
# Run once on a fresh Ubuntu EC2 to set up a Node.js app server

set -e   # Exit immediately if any command fails
set -o pipefail  # Catch errors in piped commands

echo "=== [1/6] Updating system packages ==="
apt-get update -y && apt-get upgrade -y

echo "=== [2/6] Installing Node.js 20 ==="
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt-get install -y nodejs

echo "=== [3/6] Installing PM2 (process manager) ==="
npm install -g pm2

echo "=== [4/6] Installing Nginx ==="
apt-get install -y nginx
systemctl enable nginx
systemctl start nginx

echo "=== [5/6] Configuring firewall ==="
ufw allow 22    # SSH
ufw allow 80    # HTTP
ufw allow 443   # HTTPS
ufw --force enable

echo "=== [6/6] Creating app directory ==="
mkdir -p /var/www/myapp
chown -R ubuntu:ubuntu /var/www/myapp

echo ""
echo "✅ Server setup complete!"
echo "Node.js: $(node --version)"
echo "npm: $(npm --version)"
echo "PM2: $(pm2 --version)"
```

---

### Example 2: Application Deployment Script

```bash
#!/bin/bash
# deploy.sh
# Usage: ./deploy.sh [staging|production]

set -e

ENVIRONMENT=${1:-"staging"}
APP_DIR="/var/www/myapp"
BACKUP_DIR="/var/backups/myapp"
APP_NAME="myapp"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Validate environment
if [ "$ENVIRONMENT" != "staging" ] && [ "$ENVIRONMENT" != "production" ]; then
    echo "ERROR: Environment must be 'staging' or 'production'"
    echo "Usage: ./deploy.sh [staging|production]"
    exit 1
fi

echo "🚀 Deploying to $ENVIRONMENT at $TIMESTAMP"

# Backup current version
echo "📦 Backing up current version..."
mkdir -p "$BACKUP_DIR"
if [ -d "$APP_DIR" ]; then
    tar -czf "$BACKUP_DIR/backup_$TIMESTAMP.tar.gz" -C "$APP_DIR" . && \
    echo "Backup saved: $BACKUP_DIR/backup_$TIMESTAMP.tar.gz"
fi

# Pull latest code
echo "⬇️  Pulling latest code..."
cd "$APP_DIR"
git pull origin main

# Install dependencies
echo "📥 Installing dependencies..."
npm ci --only=production

# Build (for Next.js / React apps)
echo "🔨 Building application..."
npm run build

# Restart application
echo "🔄 Restarting application..."
pm2 restart "$APP_NAME" 2>/dev/null || pm2 start npm --name "$APP_NAME" -- start

# Wait for app to be ready
echo "⏳ Waiting for app to start..."
sleep 10

# Health check
echo "🩺 Running health check..."
HEALTH=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/health)

if [ "$HEALTH" = "200" ]; then
    echo "✅ Deployment successful! App is healthy (HTTP $HEALTH)"
else
    echo "❌ Health check FAILED (HTTP $HEALTH). Rolling back..."
    LATEST_BACKUP=$(ls -t "$BACKUP_DIR"/*.tar.gz | head -1)
    tar -xzf "$LATEST_BACKUP" -C "$APP_DIR"
    pm2 restart "$APP_NAME"
    echo "🔙 Rollback complete."
    exit 1
fi
```

---

### Example 3: Log Cleanup Script with Cron

```bash
#!/bin/bash
# log_cleanup.sh
# Deletes log files older than 30 days and uploads archived logs to S3

LOG_DIR="/var/log/myapp"
ARCHIVE_DIR="/var/log/myapp/archive"
S3_BUCKET="s3://myapp-logs-archive"
DAYS_TO_KEEP=30

echo "=== Log Cleanup: $(date) ==="

# Create archive directory if it doesn't exist
mkdir -p "$ARCHIVE_DIR"

# Archive logs older than 30 days
echo "Archiving logs older than $DAYS_TO_KEEP days..."
find "$LOG_DIR" -name "*.log" -mtime +$DAYS_TO_KEEP -exec gzip {} \; -exec mv {}.gz "$ARCHIVE_DIR/" \;

# Upload archived logs to S3
echo "Uploading to S3..."
aws s3 sync "$ARCHIVE_DIR/" "$S3_BUCKET/$(date +%Y/%m)/" \
    --storage-class STANDARD_IA   # Infrequent Access = cheaper for cold storage

# Remove local archives after successful upload
if [ $? -eq 0 ]; then
    echo "Upload successful. Removing local archives..."
    rm -f "$ARCHIVE_DIR"/*.gz
    echo "✅ Cleanup done."
else
    echo "❌ S3 upload failed. Local archives retained."
    exit 1
fi
```

**Cron entry (runs every Sunday at 1 AM):**
```bash
0 1 * * 0 /scripts/log_cleanup.sh >> /var/log/log_cleanup.log 2>&1
```

---

### Example 4: Service Watchdog Script

```bash
#!/bin/bash
# watchdog.sh
# Checks if critical services are running; restarts if not; alerts on restart

SERVICES=("nginx" "node-app" "postgresql")
ALERT_EMAIL="devops@company.com"
SLACK_WEBHOOK="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
LOG_FILE="/var/log/watchdog.log"

send_alert() {
    local message=$1
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')

    # Log it
    echo "[$timestamp] $message" >> "$LOG_FILE"

    # Slack notification
    curl -s -X POST "$SLACK_WEBHOOK" \
        -H 'Content-type: application/json' \
        --data "{\"text\":\"🚨 WATCHDOG ALERT on $(hostname): $message\"}"
}

for service in "${SERVICES[@]}"; do
    if ! systemctl is-active --quiet "$service"; then
        echo "[$( date )] $service is DOWN. Attempting restart..."

        systemctl restart "$service"
        sleep 5

        if systemctl is-active --quiet "$service"; then
            send_alert "$service was DOWN and has been RESTARTED successfully."
        else
            send_alert "$service is DOWN and FAILED TO RESTART. Manual intervention needed!"
        fi
    fi
done
```

**Cron entry (every 5 minutes):**
```bash
*/5 * * * * /scripts/watchdog.sh
```

---

### Example 5: Dockerfile with Shell Script Entrypoint

```dockerfile
# Dockerfile – Node.js app with shell script entrypoint
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

# Copy and set permissions on entrypoint script
COPY scripts/docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

EXPOSE 3000

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["node", "server.js"]
```

```bash
#!/bin/sh
# docker-entrypoint.sh
# Runs before the main app starts inside the container

set -e

echo "=== Container starting up ==="
echo "Environment: $NODE_ENV"
echo "Database host: $DB_HOST"

# Wait for database to be ready before starting the app
echo "Waiting for database..."
until nc -z "$DB_HOST" 5432; do
    echo "Database not ready yet, retrying in 2s..."
    sleep 2
done
echo "✅ Database is ready!"

# Run database migrations
echo "Running migrations..."
npm run migrate

# Hand off to main process (node server.js)
echo "Starting application..."
exec "$@"
```

---

### Example 6: Jenkins Pipeline Using Shell Scripts

```groovy
// Jenkinsfile
pipeline {
    agent { label 'linux-agent' }

    environment {
        APP_ENV     = 'production'
        DEPLOY_DIR  = '/var/www/myapp'
        S3_BUCKET   = 'myapp-artifacts'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/org/myapp.git'
            }
        }

        stage('System Check') {
            steps {
                sh '''
                    echo "=== Build Environment ==="
                    node --version
                    npm --version
                    df -H
                    free -h
                '''
            }
        }

        stage('Install & Build') {
            steps {
                sh '''
                    npm ci
                    npm run build
                '''
            }
        }

        stage('Test') {
            steps {
                sh 'npm test'
            }
        }

        stage('Package & Upload to S3') {
            steps {
                sh '''
                    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
                    tar -czf app_${TIMESTAMP}.tar.gz dist/ package*.json
                    aws s3 cp app_${TIMESTAMP}.tar.gz s3://${S3_BUCKET}/builds/
                    echo "ARTIFACT=app_${TIMESTAMP}.tar.gz" > artifact.env
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh "chmod +x ./scripts/deploy.sh && ./scripts/deploy.sh $APP_ENV"
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                    sleep 15
                    STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/health)
                    if [ "$STATUS" != "200" ]; then
                        echo "Health check failed with HTTP $STATUS"
                        exit 1
                    fi
                    echo "✅ Health check passed (HTTP $STATUS)"
                '''
            }
        }
    }

    post {
        success {
            sh '''
                curl -s -X POST "$SLACK_WEBHOOK" \
                  --data "{\"text\":\"✅ Deploy to production succeeded — Build #${BUILD_NUMBER}\"}"
            '''
        }
        failure {
            sh '''
                curl -s -X POST "$SLACK_WEBHOOK" \
                  --data "{\"text\":\"❌ Deploy FAILED — Build #${BUILD_NUMBER}. Check Jenkins logs.\"}"
            '''
        }
    }
}
```

---

## Navigation Footer

← Previous: [`47_Python_for_DevOps_Automation.md`](47_Python_for_DevOps_Automation.md) | Next: [`49_Prompt_Engineering_for_DevOps_&_AI.md`](49_Prompt_Engineering_for_DevOps_&_AI.md) →