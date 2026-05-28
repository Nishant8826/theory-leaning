# 47 – Python for DevOps Automation

> **Batch-43 | Python Automation for DevOps | 2026-05-28**
> Instructor: Cloud (Vikas) | IST

---

## Table of Contents

1. [Why Python for DevOps?](#1-why-python-for-devops)
2. [Python Basics for DevOps Engineers](#2-python-basics-for-devops-engineers)
3. [Python Modules & Dependency Management](#3-python-modules--dependency-management)
4. [Scripting vs Programming](#4-scripting-vs-programming)
5. [Boto3 – Python SDK for AWS](#5-boto3--python-sdk-for-aws)
6. [Hands-On Projects Walkthrough](#6-hands-on-projects-walkthrough)
7. [Visual Diagrams](#7-visual-diagrams)
8. [Scenario-Based Q&A](#8-scenario-based-qa)
9. [Interview Q&A](#9-interview-qa)
10. [Tech Stack Mapping](#10-tech-stack-mapping)
11. [Code / Practical Examples](#11-code--practical-examples)
12. [Navigation Footer](#navigation-footer)

---

## 1. Why Python for DevOps?

### What
Python is a **high-level, human-readable, interpreted programming language**. "High-level" means it's written closer to how humans speak, not how machines think. "Interpreted" means it runs **line-by-line**, unlike compiled languages (Java, C++) that must be entirely converted to machine code before running.

### Why

As a DevOps engineer, you don't write applications — you **automate infrastructure tasks**. Python is the go-to tool for this because:

| Reason | Detail |
|---|---|
| **Human-readable** | Code reads almost like plain English. Less time spent decoding syntax. |
| **Interpreted** | No compile step. Write a script, run it immediately. |
| **Massive library ecosystem** | Libraries for AWS (boto3), HTTP (requests), JSON, OS commands, scheduling — all ready to import. |
| **Cross-platform** | Runs on Linux, Mac, Windows without modification. |
| **Industry standard** | Used in DevOps, ML/AI, Data Science, Cybersecurity, and Cloud Automation. |
| **High salary** | One of the highest-paying scripting skills for cloud/DevOps roles. |

### How (Interpreted Language — Step by Step)
```
You write script.py
        │
        ▼
Python Interpreter reads line 1 → executes it immediately
        │
        ▼
Reads line 2 → executes it
        │
        ▼
... continues until end or hits an error
```

**Contrast with compiled language (Java):**
```
You write App.java
        │
        ▼
Compiler reads entire file → converts to bytecode (App.class)
        │
        ▼
JVM runs the bytecode
        (2-step process, slower feedback loop)
```

### Impact

| With Python | Without Python (manual) |
|---|---|
| Create 50 IAM users in 10 seconds | Click through AWS Console 50 times |
| Generate billing reports on schedule | Log in manually each day |
| Automate deployments via scripts | Run each command by hand |
| Error-prone tasks become repeatable | Human mistakes accumulate |

---

## 2. Python Basics for DevOps Engineers

### What
Key Python fundamentals every DevOps engineer needs to know — not to become a software developer, but to **read, write, and adapt automation scripts**.

### Current Version
- **Python 3.14** is the latest (as of 2026). Always use Python 3.x.
- **Python 2 is dead** — officially ended support in 2020. Never use it for new work.
- Check your version: `python3 --version`

### Python File Extension
All Python scripts use the `.py` extension.
- `deploy.py`, `create_user.py`, `billing_report.py`

### Core Concepts Used in DevOps Scripts

---

#### Variables
Store data that your script will use.

```python
username = "devops_user"
age = 25
is_active = True
```

---

#### User Input
Take input from the person running the script.

```python
name = input("Enter your name: ")
birth_year = int(input("Enter your birth year: "))
```

> `int()` converts string input to a number so you can do math with it.

---

#### Functions
A named, reusable block of code. Defined with `def`.

```python
def greet(name):
    print(f"Hello, {name}!")

greet("DevOps Engineer")   # Output: Hello, DevOps Engineer!
```

---

#### Loops
Repeat actions. Critical for automation (e.g., create 50 users in a loop).

```python
# for loop – repeat a fixed number of times
for i in range(5):
    print(f"Step {i}")

# while loop – repeat until condition is false
count = 10
while count > 0:
    print(count)
    count -= 1
```

---

#### Conditionals
Make decisions in your script.

```python
age = int(input("Enter age: "))
if age >= 18:
    print("Adult")
else:
    print("Minor")
```

---

#### How (Writing and Running a Python Script)

```bash
# 1. Create a script
nano my_script.py

# 2. Run it
python3 my_script.py

# 3. If it needs packages, install them first
pip install boto3
python3 my_script.py
```

### Impact

| Know Python Basics | Don't Know Python Basics |
|---|---|
| Read & modify existing automation scripts | Dependent on others for every change |
| Debug script errors quickly | Stuck on simple syntax issues |
| Adapt open-source DevOps tools | Use only out-of-the-box defaults |

---

## 3. Python Modules & Dependency Management

### What

A **module** is a pre-written Python file (a library) that adds extra capabilities to your script. Instead of writing everything from scratch, you `import` a module and use its built-in functions.

### Built-in Modules (No Installation Needed)

| Module | What it does | DevOps Use Case |
|---|---|---|
| `os` | Interact with the operating system | Run shell commands, read env variables, navigate directories |
| `sys` | Access Python runtime settings | Get command-line arguments, exit scripts with status codes |
| `time` | Work with time and delays | Add sleeps between operations, countdown timers |
| `json` | Parse and generate JSON | Read config files, process API responses |
| `datetime` | Work with dates and times | Timestamp log entries, calculate billing windows |
| `subprocess` | Run shell commands from Python | Trigger bash scripts, kubectl commands |

### Third-Party Modules (Need Installation)

| Module | What it does | Install |
|---|---|---|
| `boto3` | AWS SDK for Python — controls all AWS services | `pip install boto3` |
| `requests` | Make HTTP API calls | `pip install requests` |
| `paramiko` | SSH into remote servers | `pip install paramiko` |
| `kubernetes` | Control Kubernetes clusters | `pip install kubernetes` |
| `ansible` (runner) | Run Ansible playbooks from Python | `pip install ansible-runner` |

### How — Importing and Using Modules

```python
import time          # import the whole module
import os            # OS interactions
import json          # JSON handling
from datetime import datetime  # import just one thing from a module

# Using them:
time.sleep(3)                          # wait 3 seconds
current_dir = os.getcwd()              # get current directory
now = datetime.now().strftime("%Y-%m-%d")  # get today's date as string
```

---

### Dependency Management

#### The Problem
Different projects need different versions of the same library. If you install everything globally, projects break each other.

#### The Solution: `requirements.txt`

**Step 1 – Freeze current environment's packages into a file:**
```bash
pip freeze > requirements.txt
```

This creates a file like:
```
boto3==1.34.0
requests==2.31.0
paramiko==3.4.0
```

**Step 2 – Install dependencies on a new machine:**
```bash
pip install -r requirements.txt
```

> This is exactly like `npm install` with `package.json` in Node.js.

#### Best Practice: Virtual Environments
Isolate each project's dependencies so they don't conflict.

```bash
# Create a virtual environment
python3 -m venv venv

# Activate it (Linux/Mac)
source venv/bin/activate

# Activate it (Windows)
venv\Scripts\activate

# Now install packages — they stay isolated to this project
pip install boto3

# Deactivate when done
deactivate
```

### Impact

| With `requirements.txt` + venv | Without it |
|---|---|
| Any team member can reproduce your environment | "Works on my machine" syndrome |
| CI/CD pipelines install exact versions | Random version mismatches in production |
| Clean, isolated project dependencies | Package conflicts between projects |

---

## 4. Scripting vs Programming

### What

| | Scripting | Programming |
|---|---|---|
| **Goal** | Automate existing tasks/commands | Build full applications |
| **Audience** | The developer themselves / team | End users |
| **Complexity** | Single-purpose, short scripts | Multi-module, complex codebase |
| **Examples** | Cron job, deploy script, IAM cleanup | REST API, web app, mobile app |

### Why the Distinction Matters for DevOps

As a DevOps engineer, **most of your Python work is scripting** — not application development.

- Write a script to check if all EC2 instances are tagged correctly → **Scripting**
- Build a web dashboard to visualize cloud costs → **Programming** (usually done by devs)

### How

**A script** is typically:
- One `.py` file (sometimes a few)
- Runs start to finish and exits
- Triggered by a scheduler (cron) or CI/CD pipeline

**A program** is:
- Many files and modules
- Has a main loop or server that keeps running
- Handles user interaction

### Impact

Understanding this distinction stops you from over-engineering. A 30-line script that saves 2 hours of manual work daily is infinitely more valuable than a perfectly architected application that takes weeks to build.

---

## 5. Boto3 – Python SDK for AWS

### What
**Boto3** is the official **AWS SDK (Software Development Kit) for Python**. It's a Python library that lets you control every AWS service — EC2, S3, IAM, Lambda, RDS, CloudWatch — directly from Python code.

> Boto3 = "AWS Console, but in Python code."

### Why
- **Automation** – Create/delete resources programmatically without clicking the Console.
- **Integration** – Use AWS in CI/CD pipelines, scheduled scripts, and automation tools.
- **Scalability** – Loop through 1000 IAM users or S3 objects in seconds.
- **Consistency** – Same script runs identically every time.

### How (Setup — Step by Step)

**Step 1 – Install Boto3:**
```bash
pip install boto3
```

**Step 2 – Configure AWS credentials:**
```bash
aws configure
```
This prompts for:
```
AWS Access Key ID:     [your key]
AWS Secret Access Key: [your secret]
Default region name:   ap-south-1
Default output format: json
```

Credentials are stored in `~/.aws/credentials`. Boto3 reads them automatically.

**Step 3 – Use Boto3 in your script:**
```python
import boto3

# Create a client (for API calls)
iam = boto3.client('iam')

# Create a resource (higher-level, object-oriented interface)
s3 = boto3.resource('s3')
```

### `client` vs `resource`

| | `boto3.client()` | `boto3.resource()` |
|---|---|---|
| **Style** | Low-level API calls | High-level, object-oriented |
| **Returns** | Raw dictionaries (JSON) | Python objects with methods |
| **Best for** | IAM, billing, complex APIs | S3, EC2 (simpler operations) |

```python
# client example – returns raw dict
iam = boto3.client('iam')
response = iam.list_users()
users = response['Users']   # You navigate the dict manually

# resource example – returns objects
s3 = boto3.resource('s3')
bucket = s3.Bucket('my-bucket')   # bucket is an object with .upload_file(), .download_file(), etc.
```

### Impact

| With Boto3 | Without Boto3 (Manual Console) |
|---|---|
| Create 100 IAM users in a loop | Click "Create user" 100 times |
| Daily billing report emailed automatically | Log in and check manually every morning |
| S3 cleanup script deletes old files | Navigate folders and delete manually |
| Entire infra teardown on schedule | Miss resources, get unexpected bills |

---

## 6. Hands-On Projects Walkthrough

### Project 1: Calculate Age (`calculate.py`)

**What it does:** Takes the user's birth year as input, calculates their current age.

**Concepts used:** `input()`, `int()`, arithmetic, `print()`

**Why it matters:** Teaches input handling and type conversion — both critical in scripts that accept runtime parameters.

---

### Project 2: Countdown Timer

**What it does:** Counts down from a given number to 0, pausing 1 second between each step.

**Concepts used:** `import time`, `def` (function), `for` loop, `time.sleep()`

**Why it matters:** `time.sleep()` is used in real DevOps scripts to:
- Wait for an EC2 instance to start before connecting to it
- Pause between retries when an API call fails
- Add delays in deployment pipelines

---

### Project 3: AWS IAM Automation via Boto3

**What it does:** Full CRUD operations on IAM users.
- **Create** an IAM user
- **List** all IAM users
- **Update** (rename) a user
- **Delete** a user

**Why it matters:** IAM automation is one of the most common real-world DevOps tasks. Onboarding/offboarding employees, rotating credentials, auditing user lists — all scriptable with Boto3.

---

### Project 4: S3 File Upload

**What it does:** Uploads a local file (`hello.txt`) to an S3 bucket using `boto3.resource`.

**Why it matters:** Uploading build artifacts, logs, backups, and static assets to S3 is done in almost every CI/CD pipeline.

---

### Project 5: AWS Billing Report (7-Day Check)

**What it does:** Uses the AWS Cost Explorer API via Boto3 to pull billing data for the last 7 days and print a cost summary.

**Why it matters:** Cloud bills are unpredictable. A daily automated billing report emailed to the team catches cost spikes before they become a surprise at month-end.

---

## 7. Visual Diagrams

### How Python + Boto3 Connects to AWS

```
Your Machine (Python Script)
        │
        │  import boto3
        │  boto3.client('iam')
        │
        ▼
  ~/.aws/credentials
  (Access Key + Secret Key)
        │
        │  HTTPS API Calls
        ▼
  AWS API Endpoints
  ┌─────────────────────────────────────────┐
  │                                         │
  │  IAM API    S3 API    EC2 API    Cost   │
  │  /iam       /s3       /ec2       API    │
  │                                         │
  └─────────────────────────────────────────┘
        │
        ▼
  AWS Resources Created / Modified / Deleted
  (Users, Buckets, Instances, Reports)
```

---

### Python Module Import Flow

```
script.py
    │
    ├── import os          ← Built-in (no install needed)
    ├── import time        ← Built-in
    ├── import json        ← Built-in
    ├── import sys         ← Built-in
    │
    ├── import boto3       ← Third-party (pip install boto3)
    └── import requests    ← Third-party (pip install requests)

                ↓

pip install -r requirements.txt
    │
    ▼
boto3==1.34.0       ← installed to site-packages/
requests==2.31.0    ← installed to site-packages/
```

---

### DevOps Python Automation Flow

```
Trigger
  │
  ├── Manual:    python3 script.py
  ├── Scheduled: cron / EventBridge
  └── Pipeline:  Jenkins stage runs python3 script.py
        │
        ▼
  Python Script Runs
        │
        ├── reads .env / env variables (secrets)
        ├── imports modules (boto3, os, json)
        │
        ▼
  Boto3 makes AWS API calls
        │
        ├── IAM: create/list/delete users
        ├── S3: upload / download files
        ├── EC2: start / stop / describe instances
        └── Cost Explorer: pull billing data
        │
        ▼
  Output
        ├── Print to terminal
        ├── Write to log file
        ├── Send Slack/email notification
        └── Store result in S3 / DynamoDB
```

---

### Interpreted vs Compiled Execution

```
INTERPRETED (Python)                  COMPILED (Java)
────────────────────                  ───────────────
script.py                             App.java
    │                                     │
    ▼                                     ▼ (compile step)
Line 1 → execute                     javac App.java
    │                                     │
    ▼                                     ▼
Line 2 → execute                     App.class (bytecode)
    │                                     │
    ▼                                     ▼
Line 3 → execute                     java App (runs bytecode)

Faster feedback,                     Faster at runtime,
great for scripting                  but longer build cycle
```

---

### Python Virtual Environment Structure

```
my-devops-project/
├── venv/                    ← isolated Python environment
│   ├── bin/python3          ← project's own Python
│   ├── bin/pip              ← project's own pip
│   └── lib/site-packages/   ← packages installed here ONLY
│       ├── boto3/
│       └── requests/
│
├── scripts/
│   ├── create_user.py
│   └── billing_report.py
│
└── requirements.txt         ← pip freeze > requirements.txt
```

---

## 8. Scenario-Based Q&A

---

🔍 **Scenario 1:** Your manager asks you to onboard 30 new developers to AWS, each needing their own IAM user. Doing it manually in the Console would take 2 hours. How do you handle it?

✅ **Answer:** Write a Python + Boto3 script. Read the 30 usernames from a CSV file using Python's `csv` module, loop through them, and call `iam.create_user(UserName=name)` for each. Add them to a group with the right permissions using `iam.add_user_to_group()`. The entire operation takes 30 seconds instead of 2 hours, and the script is reusable every time you onboard new people.

---

🔍 **Scenario 2:** Your team's AWS bill unexpectedly doubled this month. No one noticed until the invoice arrived. How do you prevent this from happening again?

✅ **Answer:** Write a Python billing report script using Boto3's Cost Explorer client. Schedule it as a daily cron job (or AWS EventBridge + Lambda). The script checks the last 7 days of spend, compares it to the average, and sends a Slack/email alert if spend exceeds a threshold. You catch the spike on day 1, not day 30.

---

🔍 **Scenario 3:** You're setting up a CI/CD pipeline in Jenkins. After Terraform applies and an EC2 instance starts, your next step needs to SSH into it and run setup commands. But the instance isn't ready immediately. How do you handle this?

✅ **Answer:** Write a Python wait script using `import time` and `import boto3`. Poll the EC2 instance status every 10 seconds using `ec2.describe_instance_status()`. When the status shows `ok`, `time.sleep()` ends and your SSH step begins. This is far more reliable than a fixed `sleep 60` in a shell script.

---

🔍 **Scenario 4:** A junior engineer is setting up your project on their laptop. They run your Python script and immediately get `ModuleNotFoundError: No module named 'boto3'`. What went wrong and how do you fix it for the whole team permanently?

✅ **Answer:** The `requirements.txt` file is missing or wasn't used. Fix: run `pip freeze > requirements.txt` in your project root, commit it to Git. Add a README step: `pip install -r requirements.txt` before running any script. Better yet, add this install step as the first stage of your Jenkins pipeline so it always runs automatically.

---

🔍 **Scenario 5:** You need to upload 500 log files to S3 every night from an EC2 server. Doing it with the AWS CLI one by one is too slow. How do you automate bulk uploads?

✅ **Answer:** Write a Python script using `import os` and `boto3.resource('s3')`. Use `os.listdir()` to get all files in the log directory, loop through them, and call `bucket.upload_file(filename, key)` for each. Add a timestamp prefix to the S3 key so files are organized by date. Schedule with a cron job at midnight. 500 uploads, zero manual work.

---

🔍 **Scenario 6:** Your team uses Python scripts that require different versions of the same library across two projects. Project A needs `boto3==1.28`, Project B needs `boto3==1.34`. How do you manage this without conflict?

✅ **Answer:** Use a **virtual environment** (`python3 -m venv venv`) for each project. Each venv has its own isolated `pip` and `site-packages` folder. Project A's venv installs `boto3==1.28`, Project B's installs `boto3==1.34`. They never interfere. Each project has its own `requirements.txt` pinning its version.

---

## 9. Interview Q&A

---

**Q1. Why do DevOps engineers use Python instead of Bash for automation?**

**A:** Both are used, but Python offers several advantages over Bash for complex automation:
- Python handles errors more gracefully with `try/except`.
- Python natively parses JSON and YAML (API responses, config files) without external tools.
- Python has rich libraries (boto3, requests, kubernetes client) that would require many Bash workarounds.
- Python scripts are more readable and maintainable, especially for multi-step workflows.

Bash is great for quick one-liners and system-level tasks. Python is better for anything with logic, API calls, or data processing.

---

**Q2. What is Boto3 and how do you set it up?**

**A:** Boto3 is the official AWS SDK for Python. It lets you programmatically interact with any AWS service. Setup requires two steps:
1. `pip install boto3` — installs the library.
2. `aws configure` — sets up AWS credentials (`~/.aws/credentials`). Boto3 reads these automatically, so you never hardcode keys in your scripts.

---

**Q3. What is the difference between `boto3.client()` and `boto3.resource()`?**

**A:**
- `boto3.client()` is a **low-level** interface that maps directly to AWS API calls. It returns raw JSON-like dictionaries and gives you maximum control. Used for services with complex APIs like IAM and Cost Explorer.
- `boto3.resource()` is a **high-level**, object-oriented interface. It returns Python objects with methods like `.upload_file()` and `.delete()`. Simpler to use for S3 and EC2 operations.

---

**Q4. What is `pip freeze` and when do you use it?**

**A:** `pip freeze` lists all currently installed Python packages and their exact versions in `package==version` format. You redirect this output into a file: `pip freeze > requirements.txt`. You use it when you're done setting up a project's dependencies and want to "freeze" those versions so teammates or CI/CD pipelines can reproduce the exact environment with `pip install -r requirements.txt`.

---

**Q5. What is the difference between scripting and programming in a DevOps context?**

**A:** Scripting is writing short, single-purpose programs that **automate existing tasks** — like a shell command sequence or an API call loop. The audience is internal (the DevOps team). Programming is building **full applications** with users, UIs, and complex business logic. DevOps engineers primarily do scripting (deploy scripts, IAM scripts, monitoring scripts), not application development.

---

**Q6. What are Python virtual environments and why are they important in DevOps?**

**A:** A virtual environment (`venv`) is an isolated Python environment with its own pip and installed packages. It prevents dependency conflicts between projects that need different versions of the same library. In DevOps, CI/CD pipelines often create a fresh venv, install from `requirements.txt`, and run the scripts — ensuring a clean, reproducible environment every time regardless of what's installed globally on the build server.

---

**Q7. How would you securely pass AWS credentials to a Boto3 script in a CI/CD pipeline?**

**A:** Never hardcode credentials in the script. Options:
1. **IAM Roles** (best for EC2/ECS/Lambda) — assign an IAM role to the compute resource; Boto3 picks it up automatically via instance metadata. No keys needed.
2. **Environment variables** (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`) — injected by Jenkins/GitHub Actions secrets at runtime.
3. **AWS Secrets Manager / SSM Parameter Store** — fetch credentials at runtime using Boto3 itself (bootstrapped via IAM role).

Never use option: storing keys in `.env` files committed to Git.

---

**Q8. Name 5 real DevOps automation tasks you'd use Python + Boto3 for.**

**A:**
1. **IAM automation** — bulk create/delete/audit users and roles.
2. **EC2 management** — start/stop instances on schedule to save costs.
3. **S3 operations** — upload build artifacts, rotate old logs, sync buckets.
4. **Billing reports** — daily cost summaries sent to Slack/email.
5. **Auto-tagging** — scan all untagged resources and apply required tags for compliance.

---

**Q9. What modules would you use to build a Python script that SSHes into a server, runs a command, and saves the output to S3?**

**A:**
- `paramiko` — SSH client library for connecting to remote servers.
- `boto3` — to upload the output file to S3.
- `os` / `datetime` — to generate the output filename with a timestamp.
- `io` or built-in file ops — to write the command output to a local file first.

---

## 10. Tech Stack Mapping

### Python in the DevOps Tool Chain

| Stage | Tool | Python Role |
|---|---|---|
| **Infrastructure** | Terraform + AWS | Boto3 scripts validate infra, manage state |
| **CI/CD** | Jenkins | `sh 'python3 script.py'` in pipeline stages |
| **Configuration** | Ansible | Playbooks call Python scripts; Ansible itself is Python |
| **Monitoring** | CloudWatch + Lambda | Python Lambda functions process CW events |
| **Secrets** | AWS Secrets Manager | Boto3 fetches secrets at runtime |
| **Container** | Docker | Python scripts baked into Docker images |
| **Orchestration** | Kubernetes | `kubernetes` Python client automates pod management |

---

### Real Deployment Flow with Python Automation

```
Developer pushes code to GitHub
        │
        ▼
Jenkins Pipeline Triggered
        │
        ├── Stage 1: python3 -m venv venv && pip install -r requirements.txt
        │
        ├── Stage 2: python3 tests/pre_deploy_check.py
        │           (checks: EC2 healthy? S3 bucket exists? IAM role attached?)
        │
        ├── Stage 3: terraform apply (provision infra)
        │
        ├── Stage 4: python3 scripts/deploy.py
        │           (uploads build artifact to S3, triggers CodeDeploy)
        │
        └── Stage 5: python3 scripts/post_deploy_notify.py
                    (sends Slack message with deploy summary)
```

---

### Tech-Specific Python Usage

**Node.js / Express App on EC2:**
- Python script checks health endpoint after deploy: `requests.get("http://ec2-ip/health")`
- If unhealthy, script triggers rollback via Boto3 CodeDeploy API

**React / Next.js Frontend:**
- Python script uploads built static files to S3: `bucket.upload_file('out/', 'static/')`
- Invalidates CloudFront cache after upload via `cloudfront.create_invalidation()`

**MongoDB / PostgreSQL:**
- Python script runs database migrations before deploy
- Daily backup script dumps DB and uploads to S3 using `subprocess` + Boto3

**Redis (ElastiCache):**
- Python script flushes Redis cache after a major deployment

**AWS Lambda:**
- Lambda functions written in Python use Boto3 to interact with other AWS services
- Common: Lambda + EventBridge = scheduled Python automation (no EC2 needed)

---

## 11. Code / Practical Examples

### Example 1: Calculate Age (`calculate.py`)

```python
# calculate.py
# Demonstrates: input(), int(), arithmetic, print()

from datetime import datetime

def calculate_age(birth_year):
    current_year = datetime.now().year
    age = current_year - birth_year
    return age

# Get user input
birth_year_str = input("Enter your birth year: ")
birth_year = int(birth_year_str)   # convert string to integer

age = calculate_age(birth_year)
print(f"You are {age} years old.")
```

**Run:**
```bash
python3 calculate.py
# Enter your birth year: 1998
# You are 28 years old.
```

---

### Example 2: Countdown Timer

```python
# countdown.py
# Demonstrates: import time, def, for loop, time.sleep()

import time

def countdown(seconds):
    print(f"Starting countdown from {seconds}...")
    for i in range(seconds, 0, -1):
        print(f"{i}...")
        time.sleep(1)   # pause 1 second between each count
    print("🚀 Go!")

# Run the countdown
countdown(10)
```

**Real DevOps use of `time.sleep()`:**
```python
import time
import boto3

ec2 = boto3.client('ec2', region_name='ap-south-1')

# Start an instance
ec2.start_instances(InstanceIds=['i-0abc123456789'])
print("Instance starting... waiting 30 seconds")

time.sleep(30)  # wait for instance to boot before running next step

print("Proceeding with deployment...")
```

---

### Example 3: IAM Automation – Full CRUD

```python
# iam_automation.py
# Demonstrates: boto3.client, IAM CRUD operations

import boto3
import json

# Initialize IAM client
iam = boto3.client('iam', region_name='ap-south-1')

# ─── CREATE a user ────────────────────────────────────────
def create_user(username):
    try:
        response = iam.create_user(UserName=username)
        print(f"✅ Created user: {username}")
        return response['User']
    except iam.exceptions.EntityAlreadyExistsException:
        print(f"⚠️  User {username} already exists.")

# ─── LIST all users ───────────────────────────────────────
def list_users():
    response = iam.list_users()
    users = response['Users']
    print(f"\n📋 Total IAM Users: {len(users)}")
    for user in users:
        print(f"  - {user['UserName']} (created: {user['CreateDate'].strftime('%Y-%m-%d')})")
    return users

# ─── UPDATE (rename) a user ───────────────────────────────
def update_username(old_name, new_name):
    try:
        iam.update_user(UserName=old_name, NewUserName=new_name)
        print(f"✅ Renamed: {old_name} → {new_name}")
    except iam.exceptions.NoSuchEntityException:
        print(f"❌ User {old_name} not found.")

# ─── DELETE a user ────────────────────────────────────────
def delete_user(username):
    try:
        iam.delete_user(UserName=username)
        print(f"🗑️  Deleted user: {username}")
    except iam.exceptions.NoSuchEntityException:
        print(f"❌ User {username} not found.")

# ─── MAIN ─────────────────────────────────────────────────
if __name__ == "__main__":
    create_user("devops-test-user")
    list_users()
    update_username("devops-test-user", "devops-renamed-user")
    list_users()
    delete_user("devops-renamed-user")
```

---

### Example 4: S3 File Upload

```python
# s3_upload.py
# Demonstrates: boto3.resource, S3 file upload

import boto3
import os
from datetime import datetime

# Use resource (high-level, object-oriented)
s3 = boto3.resource('s3', region_name='ap-south-1')

def upload_file(local_file_path, bucket_name, s3_key=None):
    """Upload a local file to S3."""
    if s3_key is None:
        # Auto-generate key with timestamp prefix for organization
        timestamp = datetime.now().strftime("%Y/%m/%d")
        filename = os.path.basename(local_file_path)
        s3_key = f"uploads/{timestamp}/{filename}"

    bucket = s3.Bucket(bucket_name)
    bucket.upload_file(local_file_path, s3_key)
    print(f"✅ Uploaded: {local_file_path} → s3://{bucket_name}/{s3_key}")

# Create a test file
with open("hello.txt", "w") as f:
    f.write("Hello from Python + Boto3!")

# Upload it
upload_file("hello.txt", "my-devops-bucket-2026")
```

---

### Example 5: AWS Billing Report (7-Day Check)

```python
# billing_report.py
# Demonstrates: Cost Explorer API, datetime, json formatting

import boto3
import json
from datetime import datetime, timedelta

def get_billing_report(days=7):
    """Pull AWS costs for the last N days."""
    
    # Cost Explorer is only available in us-east-1
    ce = boto3.client('ce', region_name='us-east-1')

    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')

    response = ce.get_cost_and_usage(
        TimePeriod={
            'Start': start_date,
            'End': end_date
        },
        Granularity='DAILY',
        Metrics=['UnblendedCost']
    )

    print(f"\n💰 AWS Billing Report — Last {days} Days")
    print(f"   Period: {start_date} to {end_date}")
    print("-" * 45)

    total_cost = 0.0
    for result in response['ResultsByTime']:
        date = result['TimePeriod']['Start']
        cost = float(result['Total']['UnblendedCost']['Amount'])
        currency = result['Total']['UnblendedCost']['Unit']
        total_cost += cost
        print(f"  {date}: ${cost:.4f} {currency}")

    print("-" * 45)
    print(f"  TOTAL: ${total_cost:.4f} USD")

    # Alert if cost exceeds threshold
    if total_cost > 10.0:
        print(f"\n⚠️  ALERT: 7-day spend (${total_cost:.2f}) exceeds $10 threshold!")

get_billing_report(days=7)
```

---

### Example 6: Dockerfile for Python DevOps Script

```dockerfile
# Dockerfile – Python DevOps Automation Script

FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install dependencies first (layer cache optimization)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy scripts
COPY scripts/ ./scripts/

# AWS credentials passed as environment variables at runtime
# Never bake credentials into the image!
ENV AWS_DEFAULT_REGION=ap-south-1

# Run the billing report script as default command
CMD ["python3", "scripts/billing_report.py"]
```

```bash
# Build and run
docker build -t devops-python-tools .
docker run \
  -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
  -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
  devops-python-tools
```

---

### Example 7: Jenkins Pipeline with Python Automation

```groovy
// Jenkinsfile – Python-powered deployment pipeline
pipeline {
    agent any

    environment {
        AWS_ACCESS_KEY_ID     = credentials('aws-access-key')
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret-key')
        AWS_DEFAULT_REGION    = 'ap-south-1'
        S3_BUCKET             = 'myapp-artifacts-bucket'
    }

    stages {
        stage('Setup Python Environment') {
            steps {
                sh '''
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Pre-Deploy AWS Health Check') {
            steps {
                sh '''
                    source venv/bin/activate
                    python3 scripts/pre_deploy_check.py
                '''
            }
        }

        stage('Upload Artifact to S3') {
            steps {
                sh '''
                    source venv/bin/activate
                    python3 scripts/s3_upload.py \
                        --file dist/app.tar.gz \
                        --bucket $S3_BUCKET
                '''
            }
        }

        stage('Create IAM Deploy Role (if missing)') {
            steps {
                sh '''
                    source venv/bin/activate
                    python3 scripts/iam_setup.py
                '''
            }
        }

        stage('Post-Deploy Billing Alert') {
            steps {
                sh '''
                    source venv/bin/activate
                    python3 scripts/billing_report.py
                '''
            }
        }
    }

    post {
        always {
            sh 'rm -rf venv'  # clean up virtual environment
        }
    }
}
```

---

### Example 8: Bulk IAM User Creation from a List

```python
# bulk_iam_create.py
# Real-world scenario: onboard 30 new developers at once

import boto3

iam = boto3.client('iam', region_name='ap-south-1')

# List of new developers to onboard
new_users = [
    "alice.dev", "bob.dev", "charlie.dev",
    "diana.dev", "eve.dev", "frank.dev"
    # ... add all 30
]

DEVELOPER_GROUP = "developers-group"

created = []
failed = []

for username in new_users:
    try:
        # Create the user
        iam.create_user(UserName=username)

        # Add to developer group
        iam.add_user_to_group(
            GroupName=DEVELOPER_GROUP,
            UserName=username
        )

        # Tag the user for tracking
        iam.tag_user(
            UserName=username,
            Tags=[
                {'Key': 'Department', 'Value': 'Engineering'},
                {'Key': 'CreatedBy',  'Value': 'onboarding-script'}
            ]
        )

        created.append(username)
        print(f"✅ {username} created and added to {DEVELOPER_GROUP}")

    except Exception as e:
        failed.append(username)
        print(f"❌ Failed to create {username}: {str(e)}")

print(f"\n📊 Summary: {len(created)} created, {len(failed)} failed")
```

---

## Navigation Footer

← Previous: [`45_Ansible_Configuration_Management_&_Automation.md`](45_Ansible_Configuration_Management_&_Automation.md) | Next: [`47_Python_for_DevOps_Automation.md`](47_Python_for_DevOps_Automation.md) →