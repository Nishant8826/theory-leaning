# 1. Scenario: Rogue Application Consuming All Memory

## 2. Real-world Context
You get an urgent alert on PagerDuty: The main frontend server is completely unresponsive. The CPU is maxed out. You manage to log in and need to identify what program is causing the lag, locate its precise process ID, and force it to stop immediately to restore service.

## 3. Objective
Identify resource-hogging background tasks and forcefully terminate them using Linux process management commands.

## 4. Step-by-step Solution

### Prerequisite: Setting up the Practice Environment
*To practice searching and killing a process without breaking a real system, let's start a harmless background process called `node` first:*

```bash
sudo useradd -m appuser || true
sudo bash -c 'cat <<EOF > /tmp/dummy_node
#!/bin/bash
while true; do sleep 60; done
EOF'
sudo chmod +x /tmp/dummy_node
sudo -u appuser bash -c "exec -a node /tmp/dummy_node &"
```
* **What:** Creates a fake process that masquerades under the name `node` and runs harmlessly in the background.
* **Why:** So that `top` and `ps aux | grep node` will actually find something for you to safely kill in the scenario.
* **How:** We write a tiny sleep loop into a file, make it executable, and run it as the `appuser` using the `exec -a node` trick to artificially set its process name to `node`.
* **Impact:** Provides a safe, isolated dummy process to practice fatal `kill -9` commands on without risking a real server.

**Step 1: Check real-time system metrics**
```bash
top
```
* **What:** Opens an interactive dashboard showing live CPU and Memory usage per process.
* **Why:** You need to instantly see what is currently running and draining resources.
* **How:** Type `top` and look at the `%CPU` and `%MEM` columns. Press `q` to quit out of it.
* **Impact:** Provides a bird's-eye view of server health, pinpointing the exact rogue program.

**Step 2: Search for the specific process details**
```bash
ps aux | grep node
```
* **What:** Lists all detailed running processes, then filters them to only show processes containing "node".
* **Why:** `top` is dynamic and moves fast. If you know a Node.js app is the culprit, `ps aux` freezes the output so you can safely grab its unique Process ID (PID).
* **How:** `ps` reports process status. `a` = all users, `u` = user readable format, `x` = commands not tied to a terminal. `grep` catches the exact keyword.
* **Impact:** You get the precise PID numbers needed to execute the termination.

**Step 3: Forcefully kill the process**
```bash
kill -9 14502
```
* **What:** Sends a SIGKILL signal directly to Process ID 14502, forcing the operating system to destroy it immediately via the kernel.
* **Why:** Sometimes a process is so frozen it can't shut itself down gracefully. You have to kill it by force.
* **How:** `kill` sends a signal. `-9` is the ultimate forceful signal. `14502` is the PID we found.
* **Impact:** Instantly frees up the CPU and Memory. The server becomes responsive again within seconds.

**Step 4: Verify the process is dead**
```bash
ps aux | grep 14502
```
* **What:** Checks if the PID still exists in the process list.
* **Why:** Zombie processes exist. You must verify the kill command actually worked.
* **How:** Same as step 2, but searching for the PID.
* **Impact:** Ensures the outage is actually resolved before notifying the engineering team.

## 6. Expected Output
```text
$ top
  PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
14502 appuser   20   0 1500432 900012   3052 R  99.9  85.2 201:10.22 node

$ ps aux | grep node
appuser  14502  99.9 85.2 1500432 900012 ?   R   10:00 201:10 node server.js

$ kill -9 14502
$ ps aux | grep 14502
admin    14560   0.0  0.0  12312   912 pts/1 S+  10:05   0:00 grep 14502
```

## 7. Tips / Best Practices
* **Graceful termination first:** Always try a regular `kill 14502` (which sends SIGTERM -15) before `kill -9` (SIGKILL). SIGTERM politely asks the app to save data and shutdown. SIGKILL kills it with no saving.
* **Using `htop`:** `htop` is a much prettier, colorized version of `top` that allows you to scroll easily and kill processes directly from the UI.

## 8. Interview Questions
1. **Q:** What is the difference between `kill -15` and `kill -9`?
   **A:** `kill -15` sends a SIGTERM, allowing the process to gracefully exit and clean up data. `kill -9` sends a SIGKILL, which forces the Linux kernel to abruptly drop the process, risking data corruption.
2. **Q:** What command would you use to list all processes running on the system?
   **A:** `ps aux` or `ps -ef`.
3. **Q:** How can you tell if a process is a "zombie"?
   **A:** In the `top` or `ps` output, the status column (S or STAT) will show a 'Z' for zombie processes.

---
[⬅️ Previous: 04_user_group_management](04_user_group_management.md) | [Next ➡️: 06_disk_management](06_disk_management.md)
