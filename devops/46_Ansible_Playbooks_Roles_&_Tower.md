# 46 – Ansible Playbooks, Roles & Tower

> **Batch-43 | Ansible + DevOps | 2026-05-27**

---

## Table of Contents

1. [Ansible Connectivity Check & Dry Run](#1-ansible-connectivity-check--dry-run)
2. [Ansible Playbook Fundamentals](#2-ansible-playbook-fundamentals)
3. [YAML Basics for Ansible](#3-yaml-basics-for-ansible)
4. [Ansible Roles](#4-ansible-roles)
5. [Ansible Tower (Enterprise)](#5-ansible-tower-enterprise)
6. [Visual Diagrams](#6-visual-diagrams)
7. [Scenario-Based Q&A](#7-scenario-based-qa)
8. [Interview Q&A](#8-interview-qa)
9. [Tech Stack Mapping](#9-tech-stack-mapping)
10. [Code / Practical Examples](#10-code--practical-examples)
11. [Navigation Footer](#navigation-footer)

---

## 1. Ansible Connectivity Check & Dry Run

### What
Before running any Playbook, you should **verify that Ansible can actually reach all target machines** over SSH. The `ping` module is the simplest way to do this — it's like a health check before surgery.

```bash
ansible all -m ping
```

This is called an **ad hoc command** — a one-off Ansible instruction run directly from the terminal without writing a Playbook file.

### Why
Running a full Playbook against unreachable machines wastes time and leaves infrastructure in a **partial/inconsistent state** (some tasks ran, some didn't). A quick `ping` before every Playbook run confirms:
- SSH connectivity is working
- The correct key is being used
- The inventory IPs are reachable
- Python is available on the targets

### How
```bash
# Ping all hosts in inventory
ansible all -m ping

# Ping only the 'webservers' group
ansible webservers -m ping

# Ping a single specific host
ansible 192.168.1.10 -m ping
```

**Successful output:**
```
192.168.1.10 | SUCCESS => {
    "ansible_facts": { "discovered_interpreter_python": "/usr/bin/python3" },
    "changed": false,
    "ping": "pong"
}
```

**Failed output (unreachable):**
```
192.168.1.10 | UNREACHABLE! => {
    "changed": false,
    "msg": "Failed to connect to the host via ssh: ...",
    "unreachable": true
}
```

### Common "Unreachable" Errors and Fixes

| Error Cause | How to Fix |
|---|---|
| **Wrong IP in host file** | Check `/etc/ansible/hosts` — verify the IP is correct |
| **SSH service is down on target** | SSH into target manually; run `service ssh start` |
| **SSH key not copied** | Re-run `ssh-copy-id root@<target-ip>` |
| **Wrong file permissions on key** | Run `chmod 600 ~/.ssh/id_rsa` |
| **Port 22 blocked (firewall/SG)** | Open port 22 in AWS Security Group / UFW rules |
| **Wrong username** | Check `ansible_user` in inventory — must match the target user |
| **PasswordAuthentication disabled** | Set `PasswordAuthentication yes` in `/etc/ssh/sshd_config`, restart SSH |

### Impact

| With ping check first | Without ping check |
|---|---|
| Catch connectivity issues in seconds | Playbook runs, fails halfway |
| Clear, specific error to debug | Cryptic failure mid-execution |
| Infrastructure remains consistent | Partial state — some servers configured, others not |

---

## 2. Ansible Playbook Fundamentals

### What
A **Playbook** is the Ansible **code file** — written in YAML — that defines *what tasks to run, on which machines, in what order*. It is the core artifact of Ansible automation.

> If Ansible is the engine, the Playbook is the fuel.

A Playbook contains one or more **plays**. Each play targets a group of hosts and runs a list of tasks. Each task uses an Ansible **module** to perform a specific action.

### Why
Ad hoc commands (like `ansible all -m ping`) are good for one-off tasks. But for anything involving multiple steps — install software, configure it, start a service, deploy code — you need a Playbook. Playbooks are:
- **Repeatable** — run the same steps every time
- **Version-controlled** — store in Git, review changes
- **Self-documenting** — each task has a `name` field that reads like a sentence
- **Idempotent** — safe to re-run without side effects

### How (Playbook Structure)

```yaml
---                        # ← 3 dashes: marks the start of a YAML document
- name: Play description   # ← Human-readable name for this play
  hosts: webservers        # ← Which inventory group/IP to run on
  become: true             # ← Run tasks as root (sudo)

  tasks:                   # ← List of tasks to execute in order
    - name: Install Nginx  # ← Task name (shown in output)
      apt:                 # ← Ansible module name
        name: nginx        # ← Module parameter
        state: latest      # ← Desired state

    - name: Start Nginx
      service:
        name: nginx
        state: started
```

### The `become: true` Key

**What:** Tells Ansible to **escalate privileges** — run the task as the `root` user (like `sudo`).

**Why needed:** Installing packages, modifying system files, and managing services require root privileges. By default, Ansible runs as the connected user (e.g., `ubuntu`) which may not have permission.

```yaml
become: true          # at play level: ALL tasks run as root
# OR
- name: Install Nginx
  apt:
    name: nginx
  become: true        # at task level: only THIS task runs as root
```

### The `state` Parameter

This is one of the most important Ansible concepts — it defines the **desired state** you want, not the action:

| state value | What it does |
|---|---|
| `present` | Install if not installed (don't upgrade) |
| `latest` | Install or upgrade to latest version |
| `absent` | Uninstall / remove |
| `started` | Start the service if not running |
| `stopped` | Stop the service if running |
| `restarted` | Always restart the service |
| `enabled` | Enable service to start on boot |

### YAML Validator
Always validate your Playbook YAML before running:
- **Online:** [yamllint.com](https://www.yamllint.com) — paste your YAML to check for syntax errors
- **CLI:** `ansible-playbook --syntax-check install_nginx.yml`

### Impact

| With Playbooks | Without Playbooks (manual) |
|---|---|
| Multi-step tasks automated | Each step done manually per server |
| Consistent across all targets | Human error on each server |
| Stored in Git | No record of what was done |
| Re-run safely anytime | Re-running manual steps risks duplication |

---

## 3. YAML Basics for Ansible

### What
**YAML** (Yet Another Markup Language) is a human-readable data format used to write Ansible Playbooks. It is to Ansible what HTML is to web pages — the language you write your instructions in.

### Key YAML Rules

**Rule 1: Key-Value Pairs**
```yaml
name: nginx
state: latest
port: 80
enabled: true
```

**Rule 2: Indentation Replaces Brackets**
YAML uses **spaces** (never tabs) to define hierarchy. The number of spaces shows nesting level:
```yaml
# WRONG (tab indented):
service:
	name: nginx    ← TAB — will cause error

# RIGHT (space indented):
service:
  name: nginx    ← 2 spaces — correct
```

**Rule 3: Lists Use a Dash (`-`)**
```yaml
packages:
  - nginx
  - curl
  - git
```

**Rule 4: Start with Three Dashes**
```yaml
---                    # ← Marks start of YAML document
- name: My Playbook
  hosts: all
```

**Rule 5: Comments Use `#`**
```yaml
# This is a comment — ignored by Ansible
- name: Install Nginx  # inline comment
```

### YAML vs JSON (Same data, different format)

```yaml
# YAML (Ansible Playbook style)
name: John
age: 30
skills:
  - ansible
  - docker
```

```json
// JSON equivalent
{
  "name": "John",
  "age": 30,
  "skills": ["ansible", "docker"]
}
```

YAML is preferred for Ansible because it's **far more readable** and requires less typing.

### Common YAML Mistakes in Playbooks

```yaml
# MISTAKE 1: Mixing tabs and spaces
tasks:
	- name: bad task    ← TAB used = syntax error

# MISTAKE 2: Missing space after colon
name:nginx             ← no space = error
name: nginx            ← correct

# MISTAKE 3: Wrong indentation level
- name: Install Nginx
apt:                   ← should be indented under the task
  name: nginx

# CORRECT:
- name: Install Nginx
  apt:
    name: nginx
```

---

## 4. Ansible Roles

### What
An **Ansible Role** is a way to **organize and reuse** Playbook code. Instead of writing one giant Playbook file with hundreds of lines, you split your automation into **roles** — each role handles one concern (e.g., "install Java", "configure Nginx", "set up a database").

> A Role is to Ansible what a function/module is to programming — a reusable, self-contained unit of logic.

### Why
Without roles, as your Playbooks grow:
- One file becomes 500+ lines of YAML
- Hard to maintain, hard to test
- Can't share logic between projects
- Team members step on each other's code

With roles:
- Logic is split into small, focused files
- Roles are **reusable across projects** (write once, use everywhere)
- Can be shared publicly on **Ansible Galaxy** (like npm for Ansible)
- Easy to test each role independently

### How — Creating a Role

**Step 1: Use `ansible-galaxy init` to scaffold the role structure**

```bash
ansible-galaxy init rajivnginx
```

This command automatically creates the following folder structure:

```
rajivnginx/
├── README.md
├── defaults/
│   └── main.yml        ← Default variable values (lowest priority)
├── files/
│   └── (static files to copy to targets)
├── handlers/
│   └── main.yml        ← Handlers (tasks triggered by notify)
├── meta/
│   └── main.yml        ← Role metadata (author, dependencies)
├── tasks/
│   └── main.yml        ← THE MAIN TASKS FILE ← Most important
├── templates/
│   └── (Jinja2 template files, e.g. nginx.conf.j2)
├── tests/
│   ├── inventory
│   └── test.yml
└── vars/
    └── main.yml        ← Variable overrides (higher priority than defaults)
```

**Step 2: Write tasks in `tasks/main.yml`**

```yaml
# rajivnginx/tasks/main.yml
---
- name: Install Nginx
  apt:
    name: nginx
    state: latest

- name: Start Nginx service
  service:
    name: nginx
    state: started
    enabled: yes
```

**Step 3: Call the role from a Playbook**

```yaml
# site.yml (master playbook)
---
- name: Configure Web Servers
  hosts: webservers
  become: true
  roles:
    - rajivnginx       ← Calls the role by folder name
```

**Step 4: Run the playbook**

```bash
ansible-playbook site.yml
```

### Role Folders Explained

| Folder | Purpose | When to use |
|---|---|---|
| `tasks/` | The actual automation steps | Always — this is the core |
| `defaults/` | Default variable values | When your role has configurable options |
| `vars/` | Variable overrides | For values that shouldn't be changed by users |
| `handlers/` | Tasks triggered by `notify` | e.g., "restart nginx only if config changed" |
| `templates/` | Jinja2 config file templates | When config files need dynamic values |
| `files/` | Static files to copy to targets | Binary files, scripts, certs |
| `meta/` | Role dependencies | If this role requires other roles first |

### Ansible Galaxy — Role Marketplace

```bash
# Initialize a new role scaffold
ansible-galaxy init <role_name>

# Download a public role from Ansible Galaxy (like npm install)
ansible-galaxy install geerlingguy.nginx

# List installed roles
ansible-galaxy list

# Clone a roles repo from GitHub (as done in the session)
git clone https://github.com/DevSecOpsG/ansibleplaybookwithroles.git
cd ansibleplaybookwithroles

# Run a specific playbook from the repo
ansible-playbook openjdk11.yml
ansible-playbook maven.yml
```

### Handlers — A Special Role Feature

**What:** Handlers are tasks that run **only when triggered** by a `notify` directive. They run at the **end of a play**, not inline.

**Why:** Avoid unnecessary restarts. Restart Nginx only if its config file actually changed.

```yaml
# tasks/main.yml
- name: Copy Nginx config
  template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
  notify: Restart Nginx         # ← triggers the handler

# handlers/main.yml
- name: Restart Nginx
  service:
    name: nginx
    state: restarted
```

### Impact

| With Roles | Without Roles (single flat Playbook) |
|---|---|
| Reusable across multiple projects | Copy-paste code everywhere |
| Clean, organized structure | Monolithic YAML file |
| Easy to share via Ansible Galaxy | Can't easily share |
| Test each role independently | Must test the whole Playbook |

---

## 5. Ansible Tower (Enterprise)

### What
**Ansible Tower** (now called **Red Hat Ansible Automation Platform**) is the **web-based UI and enterprise wrapper** around Ansible. Instead of running `ansible-playbook` commands from a terminal, you manage, schedule, and audit Ansible runs through a graphical dashboard.

The open-source equivalent is **AWX** (free, community version of Tower).

### Why
Bare Ansible (CLI) is powerful but lacks:
- A visual dashboard for non-DevOps users
- Role-Based Access Control (RBAC) — who can run which playbook
- Scheduling — run a playbook every night at 2 AM automatically
- Centralized logging — see all playbook run history in one place
- API access — trigger playbooks from other systems (CI/CD, ServiceNow)

Tower provides all of this in a GUI.

### Who Uses It
Tower is used by roughly **10% of companies** (those with larger teams, compliance needs, or non-technical users who need to trigger automation). Most startups and small DevOps teams use plain CLI Ansible.

### Key Features

| Feature | What it does |
|---|---|
| **Projects** | Link to a Git repo containing your Playbooks |
| **Inventory** | GUI-based inventory management (instead of editing text files) |
| **Job Templates** | Define which Playbook runs on which inventory with which credentials |
| **Schedules** | Cron-like scheduling for playbook runs |
| **RBAC** | Control who can run, view, or edit what |
| **Notifications** | Slack/email alerts on success or failure |
| **REST API** | Trigger playbooks programmatically from Jenkins, Webhooks |
| **CMDB Logging** | Full audit log of every run — what ran, when, by whom, result |

### Tower vs CLI Ansible

```
CLI Ansible:
  DevOps Engineer → Terminal → ansible-playbook → Targets

Ansible Tower:
  DevOps Engineer ─────────┐
  Developer ───────────────┤→ Tower UI / API → ansible-playbook → Targets
  Manager (view only) ─────┘
  CI/CD Pipeline ──────────┘
       (RBAC controls who can do what)
```

### Impact

| With Tower | With CLI only |
|---|---|
| Visual history of all runs | Must grep logs manually |
| Non-engineers can trigger playbooks | Only engineers with SSH can run |
| Scheduled automation | Must set up cron jobs manually |
| RBAC — safe for large teams | Anyone with access can run anything |
| ~10% adoption (paid/complex) | 90% of teams start here |

---

## 6. Visual Diagrams

### Full Ansible Workflow — From Code to Execution

```
┌─────────────────────────────────────────────────────────────────┐
│                    ANSIBLE MASTER                               │
│                                                                 │
│  1. Inventory File          2. Playbook / Role                  │
│  ┌─────────────────┐        ┌────────────────────────────┐      │
│  │ [webservers]    │        │ ---                        │      │
│  │ 192.168.1.10    │        │ - hosts: webservers        │      │
│  │ 192.168.1.11    │        │   become: true             │      │
│  │                 │        │   roles:                   │      │
│  │ [dbservers]     │        │     - rajivnginx           │      │
│  │ 192.168.1.20    │        └────────────────────────────┘      │
│  └─────────────────┘                                            │
│          │                            │                         │
│          └──────────┬─────────────────┘                         │
│                     │                                           │
│             Ansible Engine                                      │
│          (reads inventory + playbook)                           │
└─────────────────────┬───────────────────────────────────────────┘
                      │
        ┌─────────────┴──────────────┐
        │      SSH (Port 22)         │
        │   (agentless - no install) │
        └─────────────┬──────────────┘
                      │
       ┌──────────────┼──────────────┐
       ▼              ▼              ▼
┌────────────┐ ┌────────────┐ ┌────────────┐
│ Target 1   │ │ Target 2   │ │ Target N   │
│ 192.168.   │ │ 192.168.   │ │ 192.168.   │
│   1.10     │ │   1.11     │ │   1.N      │
│            │ │            │ │            │
│ Tasks run: │ │ Tasks run: │ │ Tasks run: │
│ ✓ apt updt │ │ ✓ apt updt │ │ ✓ apt updt │
│ ✓ install  │ │ ✓ install  │ │ ✓ install  │
│ ✓ start svc│ │ ✓ start svc│ │ ✓ start svc│
└─────┬──────┘ └─────┬──────┘ └─────┬──────┘
      └──────────────┴──────────────┘
                      │
                      ▼
              PLAY RECAP shown on Master
              (ok, changed, failed, unreachable)
```

---

### Ansible Role Directory Structure

```
ansible-galaxy init rajivnginx
                    │
                    ▼
rajivnginx/
│
├── tasks/
│   └── main.yml  ◀──── THE MAIN FILE: list of tasks
│
├── handlers/
│   └── main.yml  ◀──── "Restart nginx" only if config changed
│
├── templates/
│   └── nginx.conf.j2  ◀──── Config files with {{ variables }}
│
├── files/
│   └── (static files: scripts, certs, etc.)
│
├── defaults/
│   └── main.yml  ◀──── Default values: nginx_port: 80
│
├── vars/
│   └── main.yml  ◀──── Hard overrides (higher priority)
│
├── meta/
│   └── main.yml  ◀──── Role author, dependencies
│
└── README.md     ◀──── Role documentation
```

---

### Playbook vs Role — When to Use Each

```
SIMPLE TASK (1-5 steps):
  Use a flat Playbook
  ┌──────────────────┐
  │ install_nginx.yml│
  │ - install nginx  │
  │ - start nginx    │
  └──────────────────┘

COMPLEX, REUSABLE AUTOMATION (5+ steps, used in multiple projects):
  Use a Role
  ┌──────────────────────────────────────┐
  │  site.yml (master playbook)          │
  │  roles:                              │
  │    - nginx_role  ─▶ tasks/main.yml   │
  │    - java_role   ─▶ tasks/main.yml   │
  │    - maven_role  ─▶ tasks/main.yml   │
  └──────────────────────────────────────┘
```

---

### Ansible Tower Architecture

```
┌──────────────────────────────────────────────────────┐
│                  Ansible Tower                       │
│                                                      │
│  ┌──────────┐  ┌──────────┐  ┌────────────────────┐  │
│  │  Job     │  │Inventory │  │  Projects          │  │
│  │Templates │  │Management│  │  (linked to Git)   │  │
│  └──────────┘  └──────────┘  └────────────────────┘  │
│                                                      │
│  ┌──────────┐  ┌──────────┐  ┌────────────────────┐  │
│  │ Schedule │  │  RBAC    │  │  Activity Stream   │  │
│  │ (cron)   │  │(who runs │  │  (audit log /CMDB) │  │
│  └──────────┘  │  what)   │  └────────────────────┘  │
│                └──────────┘                          │
│                                                      │
│  Users: DevOps ── Developer ── Manager ── CI/CD API  │
└──────────────────────────┬───────────────────────────┘
                           │ Runs Ansible Engine
                           │
         ┌─────────────────┴─────────────────┐
         │           SSH / WinRM             │
         ▼                                   ▼
   Target Linux Servers            Target Windows Servers
```

---

### Handler Flow (Notify Pattern)

```
Task: "Copy Nginx Config"
         │
         │  Did the config file change?
         │
    YES ─┴─ NO
     │          │
     │          │ (handler is NOT triggered)
     ▼
  notify: "Restart Nginx"
     │
     │  (handler queued, runs at END of play)
     ▼
Handler: service nginx restarted ✓
```

---

## 7. Scenario-Based Q&A

---

🔍 **Scenario 1:** You run `ansible-playbook deploy.yml` and get `UNREACHABLE!` for 3 out of 10 servers. The other 7 work fine. How do you diagnose and fix this?

✅ **Answer:** First, check the 3 failing hosts specifically:
```bash
ansible 192.168.1.13 -m ping -vvv   # -vvv gives verbose SSH debug output
```
Common causes and fixes:
1. Wrong IP in `/etc/ansible/hosts` → correct it
2. SSH service down on target → SSH in via console and run `service ssh start`
3. SSH key not copied to those 3 → re-run `ssh-copy-id root@<ip>`
4. Port 22 blocked → check AWS Security Group or `ufw status` on target

After fixing, re-run only the failed hosts:
```bash
ansible-playbook deploy.yml --limit "192.168.1.13,192.168.1.14,192.168.1.15"
```

---

🔍 **Scenario 2:** You have 3 different projects that all need Nginx installed and configured the same way. You're copying the same Playbook YAML into each project. Is there a better way?

✅ **Answer:** Yes — create an **Ansible Role** for Nginx:
```bash
ansible-galaxy init nginx_role
# Write tasks in nginx_role/tasks/main.yml
```
Then in each project's Playbook:
```yaml
roles:
  - nginx_role
```
Now the Nginx logic lives in one place. If you need to update the Nginx version, you change it in the role once — all 3 projects get the update. This is the DRY (Don't Repeat Yourself) principle applied to infrastructure code.

---

🔍 **Scenario 3:** A junior team member edits the Nginx config template and restarts Nginx manually on the server. Later, your Ansible playbook runs and overwrites their change. How can you use handlers to make this safer?

✅ **Answer:** Use a handler so Nginx only restarts when the template actually changes:
```yaml
# tasks/main.yml
- name: Deploy Nginx config
  template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
  notify: Restart Nginx

# handlers/main.yml
- name: Restart Nginx
  service:
    name: nginx
    state: restarted
```
If the config hasn't changed (same content), the task reports `ok` (not `changed`), the handler is **not triggered**, and Nginx is not restarted. Zero unnecessary downtime.

---

🔍 **Scenario 4:** Your company has 50 developers and a large DevOps team. Some developers need to trigger deployment playbooks but shouldn't be able to modify infrastructure or access credentials. How do you handle this?

✅ **Answer:** This is exactly the use case for **Ansible Tower**. You set up:
- **Job Templates** — pre-defined playbook runs with locked inventory and credentials
- **RBAC (Role-Based Access Control)** — developers get `Execute` permission on deployment templates only; they cannot modify them or see credentials
- **Credentials stored in Tower vault** — developers trigger jobs without ever seeing SSH keys or AWS secrets
- **Activity Stream** — full audit log of who ran what and when

Without Tower, you'd have to give developers SSH access to the Ansible master — a security risk.

---

🔍 **Scenario 5:** Your team uses a GitHub repo to store all Ansible Playbooks and Roles. A new DevOps engineer cloned the repo but doesn't know which Playbook installs what or what variables are available. How should the repo be structured?

✅ **Answer:** Follow the standard Ansible repo structure:
```
ansible-repo/
├── site.yml              ← Master playbook (calls all roles)
├── inventory/
│   ├── dev.ini
│   └── prod.ini
├── group_vars/
│   ├── webservers.yml    ← Variables for webserver group
│   └── all.yml           ← Variables for all hosts
├── roles/
│   ├── nginx/            ← ansible-galaxy init nginx
│   ├── openjdk11/        ← ansible-galaxy init openjdk11
│   └── maven/            ← ansible-galaxy init maven
└── README.md             ← Documents how to use the repo
```
Each Role has its own `README.md` (auto-generated by `ansible-galaxy init`) that documents variables, dependencies, and usage. The new engineer can run `ansible-playbook site.yml` and everything is handled.

---

🔍 **Scenario 6:** You wrote a Playbook and when you run it you get a YAML parse error. How do you debug it?

✅ **Answer:** Three approaches:
1. **Online validator:** Copy-paste the YAML into [yamllint.com](https://www.yamllint.com) — it shows the exact line and column of the error with a description.
2. **CLI syntax check:** `ansible-playbook --syntax-check myplaybook.yml` — Ansible parses without executing.
3. **Common culprits:** Look for tabs instead of spaces, missing space after `:`, wrong indentation level, or missing `---` at the top.

---

## 8. Interview Q&A

---

**Q1. What is a Playbook in Ansible and how is it different from an ad hoc command?**

**A:** A Playbook is a YAML file containing an ordered set of tasks to execute on target machines — it's the primary way to express complex, multi-step automation in Ansible. An ad hoc command (like `ansible all -m ping`) is a single, one-off command run directly from the terminal without a file. Ad hoc commands are for quick checks or one-time tasks. Playbooks are for repeatable, version-controlled automation.

---

**Q2. What does `become: true` do in a Playbook?**

**A:** `become: true` tells Ansible to escalate privileges and run the task as the `root` user — equivalent to `sudo`. It's needed for tasks that require system-level permissions, such as installing packages, modifying system configs, or managing services. It can be set at the play level (applies to all tasks) or at the individual task level (applies only to that task).

---

**Q3. What are Ansible Roles and why should you use them?**

**A:** Roles are a way to organize Ansible code into reusable, self-contained units. Instead of one large Playbook file, you split logic into roles (e.g., a "nginx" role, a "java" role). Each role has a standard directory structure (`tasks/`, `handlers/`, `templates/`, `defaults/`, etc.) created by `ansible-galaxy init`. Roles promote DRY principles, are shareable across projects, and can be published to Ansible Galaxy for community use.

---

**Q4. What does `ansible-galaxy init <role_name>` do?**

**A:** It generates a standard scaffold directory structure for a new Ansible Role. It creates folders for `tasks`, `handlers`, `templates`, `files`, `defaults`, `vars`, `meta`, and `tests`, each with a starter `main.yml` file. This ensures consistency across all roles and saves time setting up the structure manually. You then write your automation logic primarily in `tasks/main.yml`.

---

**Q5. What is the purpose of `handlers` in Ansible Roles?**

**A:** Handlers are special tasks that only run when explicitly triggered by a `notify` directive in another task. They run at the end of the play, not immediately. The key benefit: they prevent unnecessary actions. For example, if you have a task that updates an Nginx config, you notify a "Restart Nginx" handler. If the config didn't change (task reported `ok`), the handler is never triggered. If it did change (task reported `changed`), Nginx restarts exactly once at the end — no double-restarts even if multiple tasks notify the same handler.

---

**Q6. What are `defaults/` vs `vars/` in an Ansible Role?**

**A:** Both hold variable values, but with different priority levels:
- `defaults/main.yml` — **Lowest priority**. These are fallback values that users of the role are expected to override. Example: `nginx_port: 80`.
- `vars/main.yml` — **Higher priority**. These are "hard" values set by the role author that are not meant to be overridden by the user.

Variable priority order (low to high): `defaults` → `group_vars` → `host_vars` → `vars` → extra-vars (command line).

---

**Q7. What is Ansible Tower and when would a company use it?**

**A:** Ansible Tower (now Red Hat Ansible Automation Platform) is a web-based UI and enterprise management layer on top of Ansible. Companies use it when they need: RBAC (multiple teams with different permissions), a visual dashboard for non-DevOps users to trigger playbooks, scheduling, centralized audit logging, REST API integration with CI/CD or ITSM tools (like ServiceNow), and secure credential management. It's used by roughly 10% of companies — those with larger teams, compliance requirements, or non-technical users who need to trigger automation.

---

**Q8. What are the common causes of `UNREACHABLE` errors in Ansible and how do you fix them?**

**A:**
1. **Wrong IP in inventory** → Correct the IP in the hosts file
2. **SSH service not running on target** → Start SSH: `service ssh start`
3. **SSH key not copied to target** → Run `ssh-copy-id root@<target-ip>`
4. **Wrong key permissions** → Run `chmod 600 ~/.ssh/id_rsa`
5. **Port 22 blocked** → Open port 22 in firewall (AWS SG / UFW)
6. **Wrong username** → Check `ansible_user` in inventory

Debug with: `ansible all -m ping -vvv` for verbose SSH output showing exactly where the connection fails.

---

**Q9. What is the `state` parameter in Ansible modules and why is it important?**

**A:** The `state` parameter defines the **desired end state** you want, not an action. Ansible checks the current state and only acts if it doesn't match. For `apt`: `present` = ensure installed, `latest` = ensure latest version, `absent` = ensure removed. For `service`: `started` = ensure running, `stopped` = ensure stopped, `restarted` = always restart. This is what makes Ansible **idempotent** — you declare what you want, Ansible figures out whether action is needed.

---

## 9. Tech Stack Mapping

### Ansible in a Full DevOps Pipeline

```
Code Commit (GitHub)
       │
       ▼
Jenkins Pipeline
       │
       ├──▶ Checkout code
       ├──▶ Build (npm/mvn/docker)
       ├──▶ Test
       ├──▶ Push image to ECR
       │
       └──▶ ansible-playbook deploy.yml
                    │
    ┌───────────────┼───────────────┐
    ▼               ▼               ▼
EC2 Web         EC2 App         EC2 DB
 Servers        Servers         Servers
(Nginx role)  (Node.js role)  (Postgres role)
```

---

### Tool Integration Map

| Tool | How Ansible Integrates |
|---|---|
| **Node.js / Express** | Role installs Node.js, npm, PM2; deploys app code; starts service |
| **React / Next.js** | Role builds static assets, copies to Nginx web root, or configures SSR server |
| **MongoDB** | Role installs mongod, configures replica set, creates users/databases |
| **PostgreSQL** | Role installs postgres, runs `pg_hba.conf` template, creates DB and user |
| **Redis** | Role installs redis-server, configures `maxmemory`, sets up persistence |
| **Nginx** | Role installs Nginx, deploys virtual host config via template, enables site |
| **Docker** | `docker_container` module manages container lifecycle on target hosts |
| **AWS EC2** | Dynamic inventory plugin auto-discovers EC2 instances by tag |
| **Jenkins** | Jenkins `sh` step calls `ansible-playbook`; Tower's REST API can be triggered from Jenkins |
| **Java (JDK11)** | `openjdk11.yml` playbook / role (as demoed in session) |
| **Maven** | `maven.yml` playbook / role with interactive version prompt (as demoed) |

---

### Real Deployment Flow — Node.js App on AWS

```
Developer pushes to main branch
          │
          ▼
  Jenkins Pipeline starts
          │
          ├─ npm ci && npm run build
          ├─ docker build -t myapp .
          ├─ docker push ECR_URI/myapp:latest
          │
          └─ ansible-playbook -i inventory/prod.ini deploy_app.yml
                    │
                    └── Role: nodejs_app
                          tasks/main.yml:
                          1. docker login to ECR
                          2. docker pull latest image
                          3. docker stop old container
                          4. docker run new container (port 3000)
                          5. notify: Reload Nginx
                          handlers/main.yml:
                          - Reload Nginx upstream config
```

---

## 10. Code / Practical Examples

### Example 1: The Session's Sample Playbook (Nginx Install)

```yaml
# install_nginx.yml
---
- hosts: all
  become: true
  tasks:
    - name: install nginx
      apt:
        name: nginx
        state: latest

    - name: start nginx
      service:
        name: nginx
        state: started
```

```bash
# Validate syntax before running
ansible-playbook --syntax-check install_nginx.yml

# Dry run — shows what WOULD happen, no changes made
ansible-playbook install_nginx.yml --check

# Run it for real
ansible-playbook install_nginx.yml

# Run with verbose output (great for debugging)
ansible-playbook install_nginx.yml -v
```

---

### Example 2: Session Commands Explained — History Walkthrough

```bash
# 20: Initialize a new Ansible Role called 'rajivnginx'
ansible-galaxy init rajivnginx

# 21: List contents of current directory (see the role folder)
ls

# 22-23: Install 'tree' command and view role directory structure
apt install tree
tree rajivnginx
# Output shows all auto-generated folders and main.yml files

# 24: View command history
history

# 25-27: Clone and install Git, then clone the roles repo
apt install git
git clone https://github.com/DevSecOpsG/ansibleplaybookwithroles.git

# 28-29: List and navigate into the cloned repo
ls
cd ansibleplaybookwithroles/

# 30: See what playbooks are available in the repo
ls

# 31: Wrong command (missing hyphen) — typo
ansibleplaybook openjdk11.yml   # ← ERROR: command not found

# 32-33: Correct commands — run the Java and Maven playbooks
ansible-playbook openjdk11.yml
ansible-playbook maven.yml      # ← Prompts for Maven version interactively
```

---

### Example 3: Role — OpenJDK 11 Installation

```bash
# Create the role
ansible-galaxy init openjdk11
```

```yaml
# openjdk11/tasks/main.yml
---
- name: Update apt cache
  apt:
    update_cache: yes

- name: Install OpenJDK 11
  apt:
    name: openjdk-11-jdk
    state: present

- name: Set JAVA_HOME environment variable
  lineinfile:
    path: /etc/environment
    line: 'JAVA_HOME="/usr/lib/jvm/java-11-openjdk-amd64"'
    state: present

- name: Verify Java installation
  command: java -version
  register: java_version

- name: Print Java version
  debug:
    var: java_version.stderr_lines
```

```yaml
# openjdk11.yml (Playbook that calls the role)
---
- name: Install OpenJDK 11 on all app servers
  hosts: appservers
  become: true
  roles:
    - openjdk11
```

---

### Example 4: Role — Maven with Interactive Version Prompt

```yaml
# maven/defaults/main.yml
---
maven_version: "3.9.6"                  # Default — can be overridden
maven_install_dir: /opt/maven
maven_download_url: "https://downloads.apache.org/maven/maven-3/{{ maven_version }}/binaries/apache-maven-{{ maven_version }}-bin.tar.gz"
```

```yaml
# maven/tasks/main.yml
---
- name: Ensure Java is installed (Maven dependency)
  apt:
    name: openjdk-11-jdk
    state: present

- name: Create Maven install directory
  file:
    path: "{{ maven_install_dir }}"
    state: directory
    mode: '0755'

- name: Download Maven {{ maven_version }}
  get_url:
    url: "{{ maven_download_url }}"
    dest: "/tmp/apache-maven-{{ maven_version }}-bin.tar.gz"

- name: Extract Maven
  unarchive:
    src: "/tmp/apache-maven-{{ maven_version }}-bin.tar.gz"
    dest: "{{ maven_install_dir }}"
    remote_src: yes
    extra_opts: ["--strip-components=1"]

- name: Set Maven environment variables
  copy:
    content: |
      export MAVEN_HOME={{ maven_install_dir }}
      export PATH=$PATH:$MAVEN_HOME/bin
    dest: /etc/profile.d/maven.sh
    mode: '0755'

- name: Verify Maven installation
  command: "{{ maven_install_dir }}/bin/mvn -version"
  register: mvn_version

- name: Print Maven version
  debug:
    var: mvn_version.stdout_lines
```

```yaml
# maven.yml (Playbook with interactive version override)
---
- name: Install Maven
  hosts: appservers
  become: true
  vars_prompt:
    - name: maven_version
      prompt: "Enter Maven version to install (e.g. 3.9.6)"
      default: "3.9.6"
      private: no           # Show input (not a password)
  roles:
    - role: maven
      vars:
        maven_version: "{{ maven_version }}"
```

```bash
# Running this playbook prompts interactively:
ansible-playbook maven.yml
# Enter Maven version to install (e.g. 3.9.6) [3.9.6]: 3.8.8
```

---

### Example 5: Complete Role with Handlers and Templates — Nginx

```bash
ansible-galaxy init nginx_role
```

```yaml
# nginx_role/defaults/main.yml
---
nginx_port: 80
nginx_worker_processes: auto
app_name: myapp
```

```nginx
# nginx_role/templates/nginx.conf.j2
worker_processes {{ nginx_worker_processes }};

events {
    worker_connections 1024;
}

http {
    server {
        listen {{ nginx_port }};
        server_name _;
        root /var/www/{{ app_name }};
        index index.html;

        location / {
            try_files $uri $uri/ =404;
        }

        location /api/ {
            proxy_pass http://localhost:3000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
}
```

```yaml
# nginx_role/tasks/main.yml
---
- name: Install Nginx
  apt:
    name: nginx
    state: latest

- name: Deploy Nginx configuration from template
  template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
    validate: nginx -t -c %s    # Validate config before deploying
  notify: Reload Nginx           # Only reload if config changed

- name: Ensure web root exists
  file:
    path: "/var/www/{{ app_name }}"
    state: directory
    owner: www-data

- name: Start and enable Nginx
  service:
    name: nginx
    state: started
    enabled: yes
```

```yaml
# nginx_role/handlers/main.yml
---
- name: Reload Nginx
  service:
    name: nginx
    state: reloaded     # reloaded = apply config without dropping connections
```

```yaml
# site.yml — Master playbook calling the role
---
- name: Configure Web Servers
  hosts: webservers
  become: true
  vars:
    nginx_port: 8080          # Override the default port
    app_name: mywebapp
  roles:
    - nginx_role
```

---

### Example 6: Ad Hoc Commands Cheatsheet

```bash
# ─── CONNECTIVITY ─────────────────────────────────────────────
# Ping all hosts
ansible all -m ping

# Ping with verbose SSH debug output
ansible all -m ping -vvv

# ─── INFORMATION ──────────────────────────────────────────────
# Gather all facts about a host (OS, memory, CPU, IPs, etc.)
ansible 192.168.1.10 -m setup

# Check uptime on all servers
ansible all -m command -a "uptime"

# Check disk space
ansible all -m command -a "df -h"

# Check memory
ansible all -m command -a "free -m"

# ─── PACKAGE MANAGEMENT ───────────────────────────────────────
# Install a package
ansible webservers -m apt -a "name=curl state=present" --become

# Remove a package
ansible webservers -m apt -a "name=apache2 state=absent" --become

# Update all packages
ansible all -m apt -a "upgrade=dist update_cache=yes" --become

# ─── SERVICE MANAGEMENT ───────────────────────────────────────
# Restart a service
ansible webservers -m service -a "name=nginx state=restarted" --become

# Check service status
ansible webservers -m command -a "systemctl status nginx" --become

# ─── FILE OPERATIONS ──────────────────────────────────────────
# Copy a file to all hosts
ansible all -m copy -a "src=/local/app.conf dest=/etc/app.conf"

# Create a directory
ansible all -m file -a "path=/opt/myapp state=directory mode=0755" --become

# ─── TARGETED RUNS ────────────────────────────────────────────
# Run only on specific hosts (comma-separated)
ansible-playbook deploy.yml --limit "web1,web2"

# Run only on a group
ansible-playbook deploy.yml --limit "webservers"

# Dry run
ansible-playbook deploy.yml --check
```

---

### Example 7: Jenkins Pipeline — Using Ansible for Deployment

```groovy
// Jenkinsfile
pipeline {
    agent any

    environment {
        ANSIBLE_HOST_KEY_CHECKING = 'False'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/org/app-repo.git'
            }
        }

        stage('Build') {
            steps {
                sh 'npm ci && npm run build'
            }
        }

        stage('Connectivity Check') {
            steps {
                withCredentials([sshUserPrivateKey(
                    credentialsId: 'ansible-key',
                    keyFileVariable: 'SSH_KEY'
                )]) {
                    sh '''
                        ansible all \
                          -i inventory/prod.ini \
                          --private-key $SSH_KEY \
                          -m ping
                    '''
                }
            }
        }

        stage('Deploy with Ansible') {
            steps {
                withCredentials([sshUserPrivateKey(
                    credentialsId: 'ansible-key',
                    keyFileVariable: 'SSH_KEY'
                )]) {
                    sh '''
                        ansible-playbook \
                          -i inventory/prod.ini \
                          --private-key $SSH_KEY \
                          --extra-vars "build_number=${BUILD_NUMBER}" \
                          playbooks/deploy_app.yml
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "Deployment successful for build ${BUILD_NUMBER}"
        }
        failure {
            echo "Deployment failed — check Ansible output above"
        }
    }
}
```

---

### Example 8: Dockerfile for Ansible Master Container

```dockerfile
# Dockerfile.ansible-master
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    openssh-client \
    sshpass \
    git \
    vim \
    tree \
    iputils-ping \
    && pip3 install ansible \
    && apt-get clean

# Create working directory for playbooks
WORKDIR /ansible

# Generate SSH key at container start
CMD ["bash", "-c", \
     "ssh-keygen -t rsa -b 4096 -f /root/.ssh/id_rsa -N '' && \
      echo 'Ansible Master ready. Run: ansible --version' && \
      tail -f /dev/null"]
```

```bash
# Build and run
docker build -f Dockerfile.ansible-master -t ansible-master .
docker run -d --name ansible-master --network ansible-lab ansible-master

# Enter the container
docker exec -it ansible-master bash
ansible --version
```

---

## Navigation Footer

← Previous: [`46_Ansible_Playbooks_Roles_&_Tower.md`](46_Ansible_Playbooks_Roles_&_Tower.md) | Next: [`47_Python_for_DevOps_Automation.md`](47_Python_for_DevOps_Automation.md) →