# 45 – Ansible: Configuration Management & Automation

> **Batch-43 | Day 41 | Ansible | 2026-05-26**

---

## Table of Contents

1. [What is Ansible?](#1-what-is-ansible)
2. [Ansible vs Other Config Management Tools](#2-ansible-vs-other-config-management-tools)
3. [Ansible Architecture Components](#3-ansible-architecture-components)
4. [How Ansible Works – Agentless + SSH](#4-how-ansible-works--agentless--ssh)
5. [Ansible Playbooks & YAML](#5-ansible-playbooks--yaml)
6. [Hands-On Lab – 9 Steps Walkthrough](#6-hands-on-lab--9-steps-walkthrough)
7. [Visual Diagrams](#7-visual-diagrams)
8. [Scenario-Based Q&A](#8-scenario-based-qa)
9. [Interview Q&A](#9-interview-qa)
10. [Tech Stack Mapping](#10-tech-stack-mapping)
11. [Code / Practical Examples](#11-code--practical-examples)
12. [Navigation Footer](#navigation-footer)

---

## 1. What is Ansible?

### What
**Ansible** is an open-source **Configuration Management** and **IT Automation** tool. It lets you automate repetitive tasks across many servers — like installing software, applying patches, restarting services, managing users, or running backups — all from a single machine, using simple code written in **YAML**.

> Think of Ansible as a **remote control for your entire server fleet.** You write what you want done, and Ansible goes and does it on 1 machine or 1000 machines simultaneously.

**Created:** 2012 by Michael DeHaan | **Acquired by:** Red Hat (2015) | **Currently:** Most widely used automation tool in the DevOps world.

### Why
Without Ansible (manual world):
- You SSH into each server one by one.
- You run the same commands on 50 servers — manually, error-prone, time-consuming.
- A junior engineer might miss a step on server #34.
- No audit trail of what was done.

With Ansible:
- Write a **Playbook** once.
- Run it against 50 servers simultaneously.
- Every server gets the exact same config.
- The Playbook itself is the documentation.

### How (High Level)
1. Install Ansible **only on the Master machine** (your laptop or a dedicated server).
2. Define your target machines in an **Inventory file** (their IP addresses).
3. Write a **Playbook** (YAML file) describing what tasks to run.
4. Run the Playbook → Ansible SSHes into each target machine and executes the tasks.
5. Results are reported back to the master.

### Impact

| With Ansible | Without Ansible |
|---|---|
| 50 servers configured in 5 minutes | 50 servers = hours of manual SSH |
| Consistent, reproducible configs | Servers drift — each one slightly different |
| Playbooks = self-documenting | No audit trail |
| Idempotent — safe to re-run | Manual scripts can break on re-run |
| No agent software needed on targets | Agent-based tools add overhead |

---

## 2. Ansible vs Other Config Management Tools

### What
There are several tools in the **Configuration Management** category. Ansible is the newest and most beginner-friendly.

| Tool | Created | Language | Agent Required? | Status |
|---|---|---|---|---|
| **CFEngine** | 1993 | C | Yes | Mostly outdated |
| **Puppet** | 2005 | Ruby / DSL | Yes | Still used, declining |
| **Chef** | 2009 | Ruby DSL | Yes | Still used, declining |
| **Ansible** | 2012 | YAML | **No (agentless)** | **Most popular today** |
| **SaltStack** | 2011 | YAML/Python | Optional | Niche use |

### Why Ansible Won
1. **Agentless** — No software to install on target machines. Huge operational advantage.
2. **YAML** — Human-readable. Even non-programmers can read and write Playbooks.
3. **Low barrier to entry** — Get started in under an hour vs days for Chef/Puppet.
4. **Push-based** — Master pushes tasks to targets (vs Chef/Puppet where agents pull).
5. **Large community** — Thousands of pre-built roles on Ansible Galaxy.

### Agent-Based vs Agentless

```
AGENT-BASED (Chef / Puppet):
  Master ──────────── Agent (installed on each target) ──── Executes tasks
              Needs: Agent install, certificate management, port open, agent updates

AGENTLESS (Ansible):
  Master ─── SSH ──── Target (just needs SSH + Python)
              Needs: Nothing extra — SSH already exists on every Linux server
```

---

## 3. Ansible Architecture Components

### Ansible Master

**What:** The machine where Ansible software is installed. This is the **control node** — the only machine that needs Ansible.

**What it contains:**
- Ansible software + Python dependencies
- Inventory / Host file (list of target IPs)
- Playbooks (YAML files with tasks)
- SSH private key (to authenticate to targets)

**Analogy:** The **conductor of an orchestra** — gives instructions to all musicians (target machines) but doesn't play an instrument itself.

---

### Target Machines (Managed Nodes)

**What:** The servers, VMs, or containers that Ansible manages and runs tasks on.

**Requirements (very minimal):**
- SSH server running
- Python installed (usually pre-installed on all Linux distros)
- That's it — no Ansible software needed

**In the lab:** 3 Docker containers — 1 Master + 2 Targets (Target 1, Target 2)

---

### Inventory / Host File

**What:** A simple text file on the Master that lists the **IP addresses or hostnames** of all target machines. Ansible reads this file to know *where* to run tasks.

**Why:** Without this, Ansible doesn't know which machines to connect to.

```ini
# /etc/ansible/hosts  (default location)

# Ungrouped hosts
192.168.1.10
192.168.1.11

# Grouped hosts
[webservers]
192.168.1.10
192.168.1.11

[databases]
192.168.1.20
192.168.1.21

[all:vars]
ansible_user=root
ansible_ssh_private_key_file=/root/.ssh/id_rsa
```

---

### Playbook

**What:** A **YAML file** containing an ordered list of **tasks** to execute on target machines. This is where you write your automation logic.

**Why:** Playbooks are the heart of Ansible. They define *what* to do, *where* to do it, and *in what order*.

**Analogy:** Like a **recipe** — a step-by-step list of instructions. The master chef (Ansible) follows the recipe on each target kitchen (server).

```yaml
# install_nginx.yml
- name: Install Nginx on web servers
  hosts: webservers          # Which targets to run on
  become: yes                # Run as root (sudo)
  tasks:
    - name: Install Nginx
      apt:
        name: nginx
        state: present
    - name: Start Nginx service
      service:
        name: nginx
        state: started
```

---

### CMDB (Configuration Management Database)

**What:** A database that stores **logs of all configuration activity** — what was changed, when, on which machine, by whom.

**Why:** Provides an audit trail. In large organizations, compliance requires knowing exactly what changed on which server and when.

**In Ansible context:** Ansible Tower / AWX (the enterprise UI for Ansible) has built-in CMDB-like logging. Standalone Ansible logs can be sent to ELK stack, Splunk, etc.

---

## 4. How Ansible Works – Agentless + SSH

### The Agentless Advantage

**What:** "Agentless" means Ansible does **not require any software to be pre-installed** on target machines. It uses **SSH** (Secure Shell) — which is already present on virtually every Linux server — to connect and run tasks.

**Why this matters:**
- No agent = no agent updates to manage
- No agent = no extra ports to open (just SSH port 22)
- No agent = no agent crashes to troubleshoot
- Works on any machine you can SSH into

### SSH Key-Based Authentication

**What:** Instead of typing a password every time, Ansible uses **SSH key pairs** for passwordless authentication.

**How it works:**
1. On the Master, generate an SSH key pair: `ssh-keygen`
   - Creates: `~/.ssh/id_rsa` (private key — stays on master, never share)
   - Creates: `~/.ssh/id_rsa.pub` (public key — copy to targets)
2. Copy the public key to each target: `ssh-copy-id root@<target-ip>`
   - This appends the public key to `~/.ssh/authorized_keys` on the target
3. Now Ansible can SSH in without a password — it proves identity using the private key

**Analogy:** The private key is your **house key**. The public key is your **lock**. You put the lock (public key) on every target machine. Your key (private key) opens all of them.

```
Master                          Target Machine
  │                                    │
  │  Has: id_rsa (private key)         │  Has: authorized_keys
  │                                    │       (contains master's public key)
  │                                    │
  │ ──── SSH connection attempt ──────▶│
  │      "Here's my public key"        │
  │                                    │  Checks: "Is this public key in
  │                                    │           my authorized_keys?"
  │ ◀──── Authentication success ──────│  YES → Allow connection
```

---

## 5. Ansible Playbooks & YAML

### YAML Basics for Ansible

**What:** YAML (Yet Another Markup Language) is the language used to write Playbooks. It's designed to be human-readable.

**Key YAML rules:**
- Uses **indentation** (spaces, never tabs) to define structure
- Lists use `-` (dash)
- Key-value pairs use `:` (colon)
- Strings don't need quotes (usually)

```yaml
# Basic YAML structure
name: John          # Key: Value
age: 30

hobbies:            # Key: List
  - reading
  - coding

address:            # Key: Nested object
  city: Mumbai
  country: India
```

### Playbook Structure Explained

```yaml
---                           # YAML document start (optional)
- name: My First Playbook     # Play name (human description)
  hosts: webservers           # Which inventory group to target
  become: yes                 # Escalate to root/sudo
  vars:                       # Variables for this play
    http_port: 80
  tasks:                      # List of tasks to run in order
    - name: Task description  # Human-readable task name
      module_name:            # Ansible module to use
        parameter1: value1    # Module parameters
        parameter2: value2
```

### Common Ansible Modules

| Module | What it does | Example use |
|---|---|---|
| `apt` / `yum` | Install/remove packages | Install Nginx, Python |
| `service` | Start/stop/restart services | Start Nginx service |
| `copy` | Copy files to targets | Deploy config files |
| `template` | Copy files with variable substitution | Deploy nginx.conf with vars |
| `user` | Create/manage users | Add deploy user |
| `file` | Create directories/set permissions | Create `/var/app` dir |
| `command` / `shell` | Run arbitrary commands | Run custom scripts |
| `git` | Clone git repositories | Deploy app code |
| `docker_container` | Manage Docker containers | Start/stop containers |
| `ping` | Test connectivity | Verify targets are reachable |

---

## 6. Hands-On Lab – 9 Steps Walkthrough

### Lab Setup
- **1 VM** = Ansible Master (Ubuntu)
- **3 Docker containers** = Target 1, Target 2 (Ubuntu containers with SSH)

---

### Step 1: Create the Master VM and Target Containers

```bash
# Launch Ubuntu VM as Ansible Master (EC2 or local VM)
# Then create Docker containers as targets

docker run -d --name target1 \
  -p 2221:22 \
  ubuntu:22.04 \
  /bin/bash -c "apt-get update && apt-get install -y openssh-server && service ssh start && tail -f /dev/null"

docker run -d --name target2 \
  -p 2222:22 \
  ubuntu:22.04 \
  /bin/bash -c "apt-get update && apt-get install -y openssh-server && service ssh start && tail -f /dev/null"
```

---

### Step 2: Install Ansible + Dependencies on Master

```bash
# On the Ansible Master VM
apt-get update -y
apt-get install -y python3 python3-pip vim iputils-ping openssh-client

# Install Ansible
pip3 install ansible
# OR via apt:
apt-get install -y ansible

# Verify
ansible --version
```

---

### Step 3: Configure SSH on Target Machines (Permit Root Login)

By default, SSH on Ubuntu doesn't allow root login with a password. For the lab, we enable it:

```bash
# On each Target container:
apt-get install -y openssh-server vim

# Edit SSH config
vim /etc/ssh/sshd_config
```

Change these two lines in `/etc/ssh/sshd_config`:
```
PermitRootLogin yes          # Allow root to log in
PasswordAuthentication yes   # Allow password login (for initial key copy)
```

```bash
# Restart SSH service
service ssh restart
# OR
systemctl restart sshd

# Set root password (needed for ssh-copy-id)
passwd root
# Enter password: root123 (or any password)
```

---

### Step 4: Generate SSH Keys on Master and Copy to Targets

```bash
# On Master: Generate SSH key pair (press Enter for all prompts)
ssh-keygen -t rsa -b 4096

# This creates:
# ~/.ssh/id_rsa        (private key - NEVER share this)
# ~/.ssh/id_rsa.pub    (public key - copy to targets)

# Copy public key to Target 1
ssh-copy-id root@<target1-ip>
# Enter target's root password when prompted

# Copy public key to Target 2
ssh-copy-id root@<target2-ip>

# Test passwordless SSH
ssh root@<target1-ip>   # Should connect without password
```

**What `ssh-copy-id` does under the hood:**
```bash
# It essentially runs this on the target:
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

---

### Step 5: Add Target IPs to Inventory / Host File

```bash
# On Master, edit the Ansible hosts file
vim /etc/ansible/hosts
```

```ini
# /etc/ansible/hosts

[webservers]
192.168.1.10   # Target 1 IP
192.168.1.11   # Target 2 IP

[webservers:vars]
ansible_user=root
ansible_ssh_private_key_file=/root/.ssh/id_rsa
```

```bash
# Test connectivity to all hosts
ansible all -m ping

# Expected output:
# 192.168.1.10 | SUCCESS => { "ping": "pong" }
# 192.168.1.11 | SUCCESS => { "ping": "pong" }
```

---

### Step 6: Write a Playbook to Install Nginx on Target 1

```bash
# On Master
vim install_nginx.yml
```

```yaml
---
- name: Install and start Nginx on Target 1
  hosts: 192.168.1.10   # or use group name: webservers
  become: yes

  tasks:
    - name: Update apt cache
      apt:
        update_cache: yes

    - name: Install Nginx
      apt:
        name: nginx
        state: present

    - name: Ensure Nginx is started and enabled
      service:
        name: nginx
        state: started
        enabled: yes

    - name: Verify Nginx is running
      command: systemctl status nginx
      register: nginx_status

    - name: Print Nginx status
      debug:
        var: nginx_status.stdout_lines
```

---

### Step 7: Run the Playbook

```bash
ansible-playbook install_nginx.yml

# Expected output:
# PLAY [Install and start Nginx on Target 1] ***
# TASK [Update apt cache] *** ok
# TASK [Install Nginx] *** changed
# TASK [Ensure Nginx is started and enabled] *** changed
# PLAY RECAP:
# 192.168.1.10 : ok=4 changed=2 unreachable=0 failed=0
```

**Output fields explained:**
- `ok` – Task ran, no change needed (already correct state)
- `changed` – Task ran and made a change
- `unreachable` – Couldn't connect to host
- `failed` – Task ran but errored

---

### Step 8: Verify on Target 1

```bash
# SSH into Target 1 and verify
ssh root@<target1-ip>
systemctl status nginx     # Should show "active (running)"
curl http://localhost      # Should return Nginx welcome page
```

---

### Step 9: Homework – Repeat for Target 2

Apply the same Nginx installation to Target 2 by:
1. Ensuring SSH key is copied to Target 2 (Step 4 for Target 2)
2. Adding Target 2 IP to the inventory
3. Updating the playbook `hosts` to target Target 2 (or the whole `webservers` group)
4. Running `ansible-playbook install_nginx.yml` again

---

## 7. Visual Diagrams

### Ansible Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Ansible Master                              │
│                                                                     │
│  ┌─────────────┐   ┌──────────────┐   ┌──────────────────────────┐ │
│  │  Inventory  │   │  Playbooks   │   │    SSH Private Key       │ │
│  │  Host File  │   │  (YAML files)│   │    (~/.ssh/id_rsa)       │ │
│  │             │   │              │   │                          │ │
│  │ [webservers]│   │ install_     │   │  Used to authenticate    │ │
│  │ 10.0.0.1   │   │ nginx.yml    │   │  to all targets          │ │
│  │ 10.0.0.2   │   │ backup.yml   │   │                          │ │
│  └─────────────┘   └──────────────┘   └──────────────────────────┘ │
└────────────────────────────┬────────────────────────────────────────┘
                             │
               Ansible reads inventory + playbook
                             │
              ┌──────────────┴──────────────┐
              │         SSH (Port 22)        │
              │    (No agent needed!)        │
              └──────────────┬──────────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
         ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│   Target 1      │ │   Target 2      │ │   Target N      │
│  10.0.0.1       │ │  10.0.0.2       │ │  10.0.0.N       │
│                 │ │                 │ │                 │
│ ✓ SSH server    │ │ ✓ SSH server    │ │ ✓ SSH server    │
│ ✓ Python        │ │ ✓ Python        │ │ ✓ Python        │
│ ✗ No Ansible!   │ │ ✗ No Ansible!   │ │ ✗ No Ansible!   │
│                 │ │                 │ │                 │
│ authorized_keys:│ │ authorized_keys:│ │ authorized_keys:│
│ [master pubkey] │ │ [master pubkey] │ │ [master pubkey] │
└─────────────────┘ └─────────────────┘ └─────────────────┘
       │                   │                   │
       ▼                   ▼                   ▼
  CMDB / Logs ◀──────── Results ────────────────┘
  (What changed, when, where)
```

---

### SSH Key Setup Flow

```
MASTER                              TARGET
  │                                   │
  │  1. ssh-keygen                    │
  │  Creates:                         │
  │  ├── id_rsa  (private) 🔑         │
  │  └── id_rsa.pub (public) 🔓       │
  │                                   │
  │  2. ssh-copy-id root@target-ip    │
  │  ────────── id_rsa.pub ──────────▶│ appended to
  │                                   │ ~/.ssh/authorized_keys
  │                                   │
  │  3. Ansible connects              │
  │  ────── SSH with id_rsa ─────────▶│ Checks authorized_keys
  │                                   │ ✅ Match found → Connected!
  │  4. Runs playbook tasks           │
  │  ────── apt install nginx ───────▶│ Executes task
  │  ◀──── Task result (ok/changed) ──│ Reports back
```

---

### Ansible Playbook Execution Flow

```
$ ansible-playbook install_nginx.yml
         │
         ▼
  Parse YAML Playbook
         │
         ▼
  Read Inventory File
  (get list of target IPs)
         │
         ▼
  For each target in parallel:
  ┌──────────────────────────────────┐
  │  SSH into target machine         │
  │          │                       │
  │          ▼                       │
  │  Execute Task 1: apt update      │
  │  ── ok / changed / failed ──▶    │
  │          │                       │
  │          ▼                       │
  │  Execute Task 2: install nginx   │
  │  ── ok / changed / failed ──▶    │
  │          │                       │
  │          ▼                       │
  │  Execute Task 3: start service   │
  │  ── ok / changed / failed ──▶    │
  └──────────────────────────────────┘
         │
         ▼
  PLAY RECAP:
  Target1: ok=3 changed=2 unreachable=0 failed=0
  Target2: ok=3 changed=2 unreachable=0 failed=0
```

---

### Ansible vs Agent-Based Tools

```
CHEF / PUPPET (Agent-Based):
─────────────────────────────
  Chef Server ─────────────────────────────────┐
                                               │  Pull (agents check in)
  ┌──────────────┐  ┌──────────────┐  ┌───────▼──────┐
  │ Target 1     │  │ Target 2     │  │  Target 3    │
  │ Chef Agent ✓ │  │ Chef Agent ✓ │  │ Chef Agent ✓ │
  │ (installed)  │  │ (installed)  │  │ (installed)  │
  └──────────────┘  └──────────────┘  └──────────────┘
  Problem: Must install & maintain agent on every machine

ANSIBLE (Agentless):
─────────────────────────────
  Ansible Master ──── SSH Push ─────────────────┐
                                               │
  ┌──────────────┐  ┌──────────────┐  ┌───────▼──────┐
  │ Target 1     │  │ Target 2     │  │  Target 3    │
  │ SSH + Python │  │ SSH + Python │  │ SSH + Python │
  │ (built-in)   │  │ (built-in)   │  │ (built-in)   │
  └──────────────┘  └──────────────┘  └──────────────┘
  Benefit: Zero installation overhead on targets
```

---

## 8. Scenario-Based Q&A

---

🔍 **Scenario 1:** Your company has 200 EC2 instances running Ubuntu. The security team just found a critical vulnerability in OpenSSL. You need to patch all 200 servers tonight. Without Ansible, this would take a team of 5 people all night. How does Ansible solve this?

✅ **Answer:** Write a single Playbook:
```yaml
- hosts: all
  become: yes
  tasks:
    - apt:
        name: openssl
        state: latest
        update_cache: yes
```
Run `ansible-playbook patch_openssl.yml`. Ansible SSHes into all 200 servers **in parallel** and applies the patch. Done in minutes. Every server gets identical treatment. You have a YAML file as the audit record of exactly what was done.

---

🔍 **Scenario 2:** Your team has 3 environments: Dev (5 servers), Staging (10 servers), Production (50 servers). All need Nginx installed but with different config files. How do you handle this with Ansible?

✅ **Answer:** Use separate **inventory groups** and **variables**:
- `inventory/dev.ini` — 5 Dev IPs
- `inventory/prod.ini` — 50 Prod IPs
- Use `templates/nginx.conf.j2` with variables like `{{ worker_processes }}`
- In `group_vars/dev.yml` set `worker_processes: 1`
- In `group_vars/prod.yml` set `worker_processes: 4`

Run `ansible-playbook -i inventory/dev.ini deploy.yml` for Dev and `ansible-playbook -i inventory/prod.ini deploy.yml` for Prod. Same playbook, different values — safe, consistent, and scalable.

---

🔍 **Scenario 3:** A new developer joins your team and accidentally runs a playbook that installs Nginx twice on the same server. Will it break anything?

✅ **Answer:** No — because Ansible is **idempotent**. The `apt` module checks if Nginx is already installed. If it is, it reports `ok` (no change). If it isn't, it installs it and reports `changed`. Running the same playbook 10 times produces the same result as running it once. This is a fundamental design principle of Ansible — safe to re-run.

---

🔍 **Scenario 4:** You set up SSH key-based auth for your Ansible Master, but when you run a playbook you get `Permission denied (publickey)`. What went wrong?

✅ **Answer:** Common causes:
1. You didn't run `ssh-copy-id` to the target — the public key isn't in the target's `authorized_keys`.
2. `PermitRootLogin` is still `no` in `/etc/ssh/sshd_config` on the target — SSH daemon won't allow root connections.
3. SSH service wasn't restarted after changing `sshd_config`.
4. Wrong username in the inventory (`ansible_user=ubuntu` but you're trying root).
Fix: Re-run `ssh-copy-id`, verify sshd_config settings, restart SSH, and test manually with `ssh root@<ip>` before running Ansible.

---

🔍 **Scenario 5:** Your manager asks: "Why are we using Ansible instead of just writing Bash scripts and running them with a for loop?" How do you answer?

✅ **Answer:** Bash scripts work, but Ansible is better because:
1. **Idempotency** — Bash `apt install nginx` always runs, even if nginx is installed. Ansible's `apt` module skips if already installed.
2. **Error handling** — Ansible stops and reports clearly when a task fails. A Bash for loop may silently fail on server #34.
3. **Parallel execution** — Ansible runs on all targets simultaneously. A Bash for loop is sequential.
4. **Readability** — YAML playbooks are self-documenting. Bash scripts need comments to be understood.
5. **Modules** — Ansible has 3000+ built-in modules for every task imaginable. No need to reinvent the wheel.

---

🔍 **Scenario 6:** You're a DevOps engineer and need to set up Ansible to manage 5 Docker containers as target machines on your laptop. What do you need on those containers?

✅ **Answer:** Each Docker container needs:
1. **SSH server** installed and running (`openssh-server`)
2. **Python 3** installed (Ansible uses Python to execute modules)
3. **Root login and password auth enabled** in `sshd_config` (at least initially, for `ssh-copy-id`)
4. A **root password** set (for the initial key exchange)

After copying the SSH public key, password auth can be disabled again for security. The containers don't need Ansible installed — that's the whole point of agentless.

---

## 9. Interview Q&A

---

**Q1. What is Ansible and what problem does it solve?**

**A:** Ansible is an open-source configuration management and automation tool. It solves the problem of managing repetitive tasks across many servers manually. Without Ansible, a DevOps engineer would need to SSH into each server individually to install software, apply patches, restart services, etc. With Ansible, you write a Playbook once and execute it against hundreds of servers simultaneously — saving time, ensuring consistency, and providing an audit trail.

---

**Q2. What does "agentless" mean in Ansible and why is it an advantage?**

**A:** Agentless means Ansible does **not require any software to be installed on the target machines**. It uses SSH (which is pre-installed on all Linux servers) to connect and execute tasks. The advantages are:
- Zero overhead — no agent to install, update, or troubleshoot on targets
- Works immediately on any SSH-accessible machine
- Fewer security concerns — no extra processes running on servers
- No port management (beyond SSH port 22)

---

**Q3. Explain the Ansible architecture components.**

**A:**
- **Ansible Master** — The control node where Ansible is installed. Contains playbooks, inventory, and SSH keys.
- **Target Machines (Managed Nodes)** — Servers that Ansible manages. Need only SSH + Python.
- **Inventory/Host File** — Lists IP addresses/hostnames of target machines, organized into groups.
- **Playbook** — YAML file containing ordered tasks to run on targets.
- **CMDB** — Stores configuration activity logs for audit and compliance.

---

**Q4. What is idempotency in Ansible and why does it matter?**

**A:** Idempotency means running the same playbook multiple times produces the same result — no duplicate actions, no breakage. For example, if a playbook installs Nginx and it's already installed, Ansible reports `ok` and skips — it doesn't install it again. This matters because:
- You can safely re-run playbooks without fear of side effects
- Playbooks become reliable "desired state" declarations
- Automation pipelines can run playbooks repeatedly (e.g., on every deploy) without issues

---

**Q5. What is an Ansible Playbook and how is it structured?**

**A:** A Playbook is a YAML file containing one or more "plays." Each play specifies:
- `hosts` — Which machines to target (from inventory)
- `become` — Whether to run as root/sudo
- `vars` — Variable definitions
- `tasks` — Ordered list of tasks, each using an Ansible module

Tasks are executed in order on all targeted machines, and each task uses a module (`apt`, `service`, `copy`, etc.) to perform a specific action.

---

**Q6. How does SSH key-based authentication work in Ansible?**

**A:**
1. On the Master, run `ssh-keygen` to create a key pair (private + public key).
2. Run `ssh-copy-id root@<target-ip>` to copy the public key to each target's `~/.ssh/authorized_keys`.
3. When Ansible connects to a target, it presents the private key as proof of identity.
4. The target checks its `authorized_keys` — if the matching public key is there, access is granted without a password.
5. In the inventory file, reference the private key with `ansible_ssh_private_key_file`.

---

**Q7. What is the difference between Ansible, Chef, and Puppet?**

**A:**

| | Ansible | Chef | Puppet |
|---|---|---|---|
| Agent required | No (agentless) | Yes | Yes |
| Language | YAML | Ruby DSL | Puppet DSL |
| Learning curve | Low | High | Medium-High |
| Push/Pull | Push | Pull | Pull |
| Popularity | Highest today | Declining | Declining |

Ansible is preferred today for its simplicity, agentless design, and YAML-based playbooks that anyone can read.

---

**Q8. What happens if an Ansible playbook task fails halfway through?**

**A:** By default, Ansible stops execution on the **failed host** and reports the error, but continues on other hosts that haven't failed. At the end, the PLAY RECAP shows `failed=1` for the affected host. You can handle failures with:
- `ignore_errors: yes` — Continue even if this task fails
- `failed_when` — Define custom failure conditions
- `block` / `rescue` / `always` — Ansible's try-catch equivalent
- `--limit` flag to re-run only on failed hosts after fixing the issue

---

**Q9. What is the Ansible inventory file and what can it contain?**

**A:** The inventory file (default: `/etc/ansible/hosts`) is a text file listing target machines. It can contain:
- Individual IP addresses or hostnames
- Groups of hosts in `[group_name]` sections
- Group variables in `[group_name:vars]` sections
- Nested groups with `[group_name:children]`
- Connection variables like `ansible_user`, `ansible_port`, `ansible_ssh_private_key_file`

It can be a static `.ini` or `.yaml` file, or a dynamic inventory script that queries AWS/GCP/Azure for live instance IPs.

---

## 10. Tech Stack Mapping

### Where Ansible Fits in DevOps

```
Developer Commits Code
        │
        ▼
   Jenkins Pipeline
        │
        ├──▶ Build Docker Image
        ├──▶ Run Tests
        ├──▶ Push to ECR
        │
        └──▶ ANSIBLE PLAYBOOK ◀── This is where Ansible comes in
                  │
                  ├── Configure EC2 instances (install Node.js, set env vars)
                  ├── Deploy Docker containers
                  ├── Configure Nginx reverse proxy
                  ├── Apply security patches
                  └── Restart services after deploy
```

---

### Ansible with AWS (EC2 + Dynamic Inventory)

| Use Case | How Ansible Helps |
|---|---|
| Provision new EC2 fleet | Playbook configures all new instances automatically |
| Patch 100 EC2s | One playbook run, all patched in parallel |
| Blue/Green deployment | Ansible switches Nginx upstream to new target group |
| Database backup | Scheduled Ansible playbook triggers pg_dump on RDS |
| User management | Add/remove SSH users across all servers with one play |

**Dynamic Inventory for AWS:**
```bash
# Instead of static IPs, Ansible queries AWS for running EC2s
ansible-playbook -i aws_ec2.yaml deploy.yml

# aws_ec2.yaml (dynamic inventory plugin config):
# plugin: aws_ec2
# regions: ap-south-1
# filters:
#   tag:Environment: production
```

---

### Ansible in a Node.js / React Deployment Pipeline

```
FULL DEPLOYMENT FLOW:

1. Jenkins builds Node.js app Docker image
2. Jenkins pushes image to AWS ECR
3. Jenkins calls: ansible-playbook deploy_app.yml

ANSIBLE PLAYBOOK (deploy_app.yml) does:
  ├── SSH into all app servers (EC2 ASG)
  ├── Pull latest Docker image from ECR
  ├── Stop old container
  ├── Start new container (port 3000)
  ├── Update Nginx config (reverse proxy to port 3000)
  └── Reload Nginx
```

---

### Ansible with Redis / MongoDB / PostgreSQL

| Database | Ansible Use |
|---|---|
| **PostgreSQL (RDS)** | Configure pg_hba.conf, create databases/users, run migrations |
| **MongoDB** | Install mongod, configure replication, create admin users |
| **Redis** | Install redis-server, configure maxmemory, set up sentinel |

---

## 11. Code / Practical Examples

### Example 1: Complete Lab Setup – Docker Containers as Targets

```bash
#!/bin/bash
# setup_lab.sh — Run on your laptop/VM

# Create a Docker network so containers can talk
docker network create ansible-lab

# Create Ansible Master container
docker run -d --name ansible-master \
  --network ansible-lab \
  -h ansible-master \
  ubuntu:22.04 \
  sleep infinity

# Create Target containers with SSH
for i in 1 2; do
  docker run -d --name target$i \
    --network ansible-lab \
    -h target$i \
    ubuntu:22.04 \
    bash -c "apt-get update -qq && \
             apt-get install -y openssh-server python3 && \
             echo 'root:root123' | chpasswd && \
             sed -i 's/#PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config && \
             sed -i 's/#PasswordAuthentication.*/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
             service ssh start && \
             tail -f /dev/null"
done

echo "✅ Lab created: ansible-master, target1, target2"
echo "Run: docker exec -it ansible-master bash"
```

---

### Example 2: Ansible Master Setup Script

```bash
#!/bin/bash
# run inside ansible-master container

# Install dependencies
apt-get update -y
apt-get install -y python3 python3-pip vim iputils-ping openssh-client sshpass

# Install Ansible
pip3 install ansible

# Verify
ansible --version

# Generate SSH key pair
ssh-keygen -t rsa -b 4096 -f /root/.ssh/id_rsa -N ""
echo "✅ SSH keys generated"

# Get target container IPs
TARGET1_IP=$(getent hosts target1 | awk '{ print $1 }')
TARGET2_IP=$(getent hosts target2 | awk '{ print $1 }')

# Copy SSH keys to targets (using sshpass for automation)
sshpass -p "root123" ssh-copy-id -o StrictHostKeyChecking=no root@$TARGET1_IP
sshpass -p "root123" ssh-copy-id -o StrictHostKeyChecking=no root@$TARGET2_IP

echo "✅ SSH keys copied to targets"

# Create inventory file
cat > /etc/ansible/hosts << EOF
[webservers]
$TARGET1_IP
$TARGET2_IP

[webservers:vars]
ansible_user=root
ansible_ssh_private_key_file=/root/.ssh/id_rsa
EOF

echo "✅ Inventory file created"
echo "Test with: ansible all -m ping"
```

---

### Example 3: Full Nginx Installation Playbook (Production-Grade)

```yaml
# install_nginx.yml
---
- name: Install and configure Nginx on web servers
  hosts: webservers
  become: yes
  vars:
    nginx_port: 80
    app_name: myapp

  tasks:
    - name: Update apt package cache
      apt:
        update_cache: yes
        cache_valid_time: 3600  # Only update if cache > 1 hour old

    - name: Install Nginx
      apt:
        name: nginx
        state: present           # present = install if not there

    - name: Create web root directory
      file:
        path: /var/www/{{ app_name }}
        state: directory
        mode: '0755'
        owner: www-data
        group: www-data

    - name: Deploy index.html
      copy:
        content: |
          <html>
            <body><h1>Hello from {{ inventory_hostname }}!</h1></body>
          </html>
        dest: /var/www/{{ app_name }}/index.html
        owner: www-data
        mode: '0644'

    - name: Configure Nginx virtual host
      copy:
        content: |
          server {
              listen {{ nginx_port }};
              root /var/www/{{ app_name }};
              index index.html;
              server_name _;
              location / {
                  try_files $uri $uri/ =404;
              }
          }
        dest: /etc/nginx/sites-available/{{ app_name }}

    - name: Enable site
      file:
        src: /etc/nginx/sites-available/{{ app_name }}
        dest: /etc/nginx/sites-enabled/{{ app_name }}
        state: link

    - name: Remove default site
      file:
        path: /etc/nginx/sites-enabled/default
        state: absent

    - name: Start and enable Nginx
      service:
        name: nginx
        state: started
        enabled: yes

    - name: Verify Nginx is responding
      uri:
        url: http://localhost:{{ nginx_port }}
        status_code: 200
      register: result

    - name: Print result
      debug:
        msg: "Nginx is up on {{ inventory_hostname }} – Status: {{ result.status }}"
```

```bash
# Run it
ansible-playbook install_nginx.yml

# Dry run (check mode — doesn't make changes)
ansible-playbook install_nginx.yml --check

# Verbose output
ansible-playbook install_nginx.yml -v
```

---

### Example 4: Node.js App Deployment Playbook

```yaml
# deploy_nodejs.yml
---
- name: Deploy Node.js Application
  hosts: appservers
  become: yes
  vars:
    app_dir: /opt/myapp
    app_port: 3000
    node_version: "20"

  tasks:
    - name: Install Node.js repository
      shell: |
        curl -fsSL https://deb.nodesource.com/setup_{{ node_version }}.x | bash -
      args:
        creates: /etc/apt/sources.list.d/nodesource.list

    - name: Install Node.js and npm
      apt:
        name:
          - nodejs
          - git
        state: present

    - name: Install PM2 globally
      npm:
        name: pm2
        global: yes
        state: present

    - name: Create app directory
      file:
        path: "{{ app_dir }}"
        state: directory
        mode: '0755'

    - name: Clone/update application code
      git:
        repo: "https://github.com/myorg/myapp.git"
        dest: "{{ app_dir }}"
        version: main
        force: yes

    - name: Install npm dependencies
      npm:
        path: "{{ app_dir }}"
        state: present

    - name: Copy environment file
      copy:
        src: files/.env.production
        dest: "{{ app_dir }}/.env"
        mode: '0600'

    - name: Start or restart app with PM2
      command: >
        pm2 startOrRestart {{ app_dir }}/ecosystem.config.js
        --env production
      environment:
        NODE_ENV: production

    - name: Save PM2 process list (survive reboot)
      command: pm2 save

    - name: Enable PM2 startup on boot
      command: pm2 startup systemd -u root --hp /root
```

---

### Example 5: Ansible Ad-Hoc Commands (Quick Tasks Without Playbook)

```bash
# Test connectivity to all hosts
ansible all -m ping

# Run a command on all webservers
ansible webservers -m command -a "uptime"

# Check disk space on all hosts
ansible all -m command -a "df -h"

# Install a package quickly (without writing a playbook)
ansible webservers -m apt -a "name=curl state=present" --become

# Restart a service
ansible webservers -m service -a "name=nginx state=restarted" --become

# Copy a file to all targets
ansible all -m copy -a "src=/local/file.txt dest=/tmp/file.txt"

# Check free memory on all machines
ansible all -m command -a "free -m"

# Gather facts about a target (OS, IP, CPU, memory, etc.)
ansible target1 -m setup
```

---

### Example 6: Jenkins Pipeline Integrating Ansible

```groovy
// Jenkinsfile
pipeline {
    agent any

    environment {
        ANSIBLE_HOST_KEY_CHECKING = 'False'
        ANSIBLE_PRIVATE_KEY = credentials('ansible-ssh-key')
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/org/app-repo.git'
            }
        }

        stage('Build') {
            steps {
                sh 'npm ci && npm run build'
            }
        }

        stage('Test') {
            steps {
                sh 'npm test'
            }
        }

        stage('Deploy with Ansible') {
            steps {
                sh """
                    ansible-playbook \
                      -i inventory/production.ini \
                      --private-key ${ANSIBLE_PRIVATE_KEY} \
                      playbooks/deploy_nodejs.yml \
                      --extra-vars "build_number=${BUILD_NUMBER}"
                """
            }
        }

        stage('Smoke Test') {
            steps {
                sh 'ansible webservers -m uri -a "url=http://{{ inventory_hostname }}:3000/health"'
            }
        }
    }

    post {
        failure {
            sh """
                ansible-playbook \
                  -i inventory/production.ini \
                  playbooks/rollback.yml
            """
        }
    }
}
```

---

### Example 7: Ansible Inventory with Multiple Environments

```ini
# inventory/production.ini

[web]
web1.prod.example.com
web2.prod.example.com
web3.prod.example.com

[app]
app1.prod.example.com ansible_port=22
app2.prod.example.com ansible_port=22

[db]
db1.prod.example.com

[prod:children]
web
app
db

[prod:vars]
ansible_user=deploy
ansible_ssh_private_key_file=/jenkins/.ssh/prod_key
env=production
```

```ini
# inventory/dev.ini

[web]
192.168.100.10

[app]
192.168.100.11

[dev:children]
web
app

[dev:vars]
ansible_user=root
ansible_ssh_private_key_file=/root/.ssh/id_rsa
env=development
```

```bash
# Run against dev
ansible-playbook -i inventory/dev.ini deploy.yml

# Run against prod
ansible-playbook -i inventory/production.ini deploy.yml
```

---

## Navigation Footer

← Previous: [`44_Deploying_3-Tier_Architecture_on_AWS_using_Terraform_(IaC).md`](44_Deploying_3-Tier_Architecture_on_AWS_using_Terraform_(IaC).md) | Next: [`46_Ansible_Playbooks_Roles_&_Tower.md`](46_Ansible_Playbooks_Roles_&_Tower.md) →