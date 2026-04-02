# ☁️ AWS EC2, AMI, EBS & Load Balancers — Deep Dive

## 📚 Table of Contents
1. [📌 Introduction](#1--introduction)
2. [💻 EC2 (Elastic Compute Cloud) — Deep Dive](#2--ec2-elastic-compute-cloud--deep-dive)
3. [🖼️ AMI (Amazon Machine Image)](#3-️-ami-amazon-machine-image)
4. [💾 EBS (Elastic Block Storage)](#4--ebs-elastic-block-storage)
5. [⚖️ Load Balancers (ELB)](#5-️-load-balancers-elb)
6. [📈 Auto Scaling — Quick Introduction](#6--auto-scaling--quick-introduction)
7. [🛠️ Practical Tips & Tools](#7-️-practical-tips--tools)
8. [📝 Assignment & Practice Tasks](#8--assignment--practice-tasks)
9. [🌍 Real-World Scenario: Putting It All Together](#9--real-world-scenario-putting-it-all-together)
10. [🎤 Interview Questions & Answers](#10--interview-questions--answers)
11. [🚫 Common Mistakes Beginners Make](#11--common-mistakes-beginners-make)
12. [✅ DevOps Best Practices](#12--devops-best-practices)
13. [📝 Quick Revision Summary](#13--quick-revision-summary)

---

## 1. 📌 Introduction

Welcome back! 🚀 In this session we go **deep** into the core building blocks of AWS infrastructure:

- **EC2** — Your virtual servers in the cloud (this time we look at instance options, recovery, and protection).
- **AMI** — Pre-baked server templates that save you hours of setup.
- **EBS** — The hard drives attached to your cloud servers.
- **Load Balancers** — The traffic cops that distribute user requests across multiple servers.

By the end of this guide you will understand how these four services work **together** to run production-grade applications. Let's dive in! 💪

---

## 2. 💻 EC2 (Elastic Compute Cloud) — Deep Dive

### 2.1 What is EC2?

EC2 = **Elastic Compute Cloud**. It is a service that lets you rent virtual servers (called **instances**) on Amazon's hardware. You choose the operating system, the CPU/RAM size, and the region — and AWS spins up a ready-to-use server in seconds.

### 2.2 Why Do We Need EC2?

| Without EC2 (Traditional) | With EC2 (Cloud) |
|:---|:---|
| Buy physical hardware ($$$$) | Rent by the second (₹₹) |
| Wait weeks for delivery | Launch in < 60 seconds |
| Hire a team to maintain servers | AWS handles hardware maintenance |
| Hard to scale up during traffic spikes | Scale up/down instantly |

### 2.3 EC2 Homepage & AWS Global View

When you open the **EC2 Dashboard** in the AWS Console you see an overview of:
- Running instances
- Security Groups
- Key Pairs
- Elastic IPs
- Volumes (EBS)

> 💡 **Tip:** Click **"AWS Global View"** (top-right corner) to see all your resources running across **every** AWS region at once. Super useful when you forget which region you launched something in!

### 2.4 Instance Types — Picking the Right Size

An **Instance Type** defines how much CPU, RAM, storage, and network speed your server gets. Think of it like choosing a car — a hatchback for city errands vs. a truck for heavy cargo.

| Instance Family | Use Case | Example |
|:---|:---|:---|
| `t2` / `t3` (General Purpose) | Small apps, dev/test environments | `t2.micro` (1 CPU, 1 GB RAM) |
| `m5` / `m6i` (General Purpose) | Production web apps, databases | `m5.xlarge` (4 CPU, 16 GB RAM) |
| `c5` / `c6i` (Compute Optimized) | Heavy computation, video encoding | `c5.4xlarge` (16 CPU, 32 GB RAM) |
| `r5` / `r6i` (Memory Optimized) | In-memory databases (Redis, SAP) | `r5.2xlarge` (8 CPU, 64 GB RAM) |
| `g4` / `p4` (GPU) | Machine Learning, graphics rendering | `p4d.24xlarge` (8 GPUs!) |

> **Example from class:** A server with **16 CPU, 32 GB RAM** would be something like the `c5.4xlarge` instance type — a compute-optimized powerhouse.

**Real-World Analogy:** 🏠  
Instance types are like apartments.  
- `t2.micro` = a studio apartment (cheap, good for one person).  
- `m5.xlarge` = a 3-bedroom flat (balanced for a family).  
- `c5.4xlarge` = a penthouse (expensive, powerful, for serious workloads).

### 2.5 Important EC2 Instance Options

These are settings you configure when launching or managing an EC2 instance:

#### 🔄 Auto-Recovery
- **What:** If the underlying physical hardware fails, AWS automatically **migrates** your instance to healthy hardware.
- **Why:** Keeps your application running without manual intervention.
- **How:** Enable it via the EC2 console → Instance Settings → Auto-Recovery. AWS uses health checks to detect hardware issues.
- **Impact:** Zero-downtime recovery from hardware failures. Your IP address and data stay the same.

#### 🔌 Shutdown Behavior
- **What:** Tells AWS what to do when you (or your OS) issues a `shutdown` command.
- Two options:
  - **Stop** (default) — The instance pauses. You can restart it later. (Data on EBS is preserved.)
  - **Terminate** — The instance is **permanently deleted**. Gone forever. 💀
- **Why it matters:** Imagine accidentally running `sudo shutdown` on a production server configured to **Terminate**. Disaster!

> ⚠️ **WARNING:** Always double-check the shutdown behavior before launching critical instances. The default for most AMIs is "Stop", but always verify.

#### 🐻‍❄️ Hibernate Mode
- **What:** Saves the **entire contents of RAM** to disk (EBS), then stops the instance. When you start it again, everything loads back into RAM — your applications resume exactly where they left off.
- **Why:** Useful for applications with long startup times. Instead of cold-booting (5-10 minutes to warm up caches), you hibernate and resume in seconds.
- **How:** 
  1. EBS root volume must be **encrypted**.
  2. EBS root volume must be **large enough** to hold the RAM contents.
  3. Instance RAM must be less than **150 GB**.

**Real-World Analogy:** 💻  
- **Stop** = Shutting down your laptop (you lose everything in RAM, apps close).  
- **Hibernate** = Closing your laptop lid (everything freezes, opens exactly where you left off).

#### 🛡️ Termination Protection
- **What:** A safety lock that **prevents** anyone from accidentally deleting (terminating) your instance.
- **Why:** In a production environment, one accidental click on "Terminate" could take down your entire website.
- **How:** Enable it during launch or via Instance Settings → Change Termination Protection → Enable.
- **Impact:** Even if someone clicks "Terminate", AWS will say: *"Nope! Termination protection is ON."*

**Real-World Analogy:** 🔒  
It's like the safety lock on a paper shredder. Even if you put documents in, it won't shred until you unlock it.

### 2.6 EC2 Concept Flow — ASCII Diagram

```
┌──────────────────────────────────────────────────────────┐
│                    EC2 INSTANCE LIFECYCLE                 │
│                                                          │
│   [ Launch ]                                             │
│       │                                                  │
│       ▼                                                  │
│   [ Running ] ◄────────────────────────┐                 │
│       │           │           │        │                 │
│       ▼           ▼           ▼        │                 │
│   [ Stop ]   [ Hibernate ] [ Reboot ]  │                 │
│       │           │                    │                 │
│       ▼           ▼                    │                 │
│   [ Stopped ] [ Stopped ]             │                 │
│       │           │                    │                 │
│       ▼           ▼                    │                 │
│   [ Start ] ──────┘────────────────────┘                 │
│                                                          │
│   [ Terminate ] ──► 💀 GONE FOREVER                      │
│   (Unless Termination Protection is ON)                  │
└──────────────────────────────────────────────────────────┘
```

---

## 3. 🖼️ AMI (Amazon Machine Image)

### 3.1 What is an AMI?

An **AMI (Amazon Machine Image)** is a **pre-configured template** used to launch EC2 instances. It contains:
- The **Operating System** (Ubuntu, Amazon Linux, Windows, etc.)
- **Pre-installed software** (NGINX, Docker, Node.js, etc.)
- **Application configurations** (config files, environment variables)
- **Data** on attached storage volumes

### 3.2 Why Do We Need AMIs?

Imagine this scenario:

> **Without AMI:** Your company needs to deploy 200 servers for a product launch. You manually log into each server, install Ubuntu, install NGINX, configure firewalls, copy application code, set environment variables... **200 times.** That could take **weeks**, and one typo on server #147 causes a bug that takes days to find. 😱

> **With AMI:** You set up ONE perfect server, create an AMI called `"Krishna-AMI"`, and use it to launch 200 identical clones in **minutes.** Every server is guaranteed to be identical. 🎯

### 3.3 How AMIs Work — Step by Step

```
Step 1: Launch a base EC2 instance (e.g., Ubuntu 22.04)
            │
            ▼
Step 2: SSH into it and install everything you need
        ┌─────────────────────────────────┐
        │  sudo apt update                │
        │  sudo apt install nginx -y      │
        │  # Copy your app code           │
        │  # Configure firewalls          │
        │  # Set environment variables    │
        └─────────────────────────────────┘
            │
            ▼
Step 3: Go to EC2 Console → Select Instance → Actions → Image → Create Image
            │
            ▼
Step 4: AWS creates your AMI (e.g., "Krishna-AMI")
        ┌─────────────────────────────────────────┐
        │  AMI ID: ami-0abc123def456                │
        │  Name:   Krishna-AMI                      │
        │  OS:     Ubuntu 22.04                     │
        │  Software: NGINX, Node.js, App Code       │
        └─────────────────────────────────────────┘
            │
            ▼
Step 5: Launch 1, 10, or 200 instances from this AMI
        ┌──────┐  ┌──────┐  ┌──────┐       ┌──────┐
        │ EC2  │  │ EC2  │  │ EC2  │  ...  │ EC2  │
        │  #1  │  │  #2  │  │  #3  │       │ #200 │
        └──────┘  └──────┘  └──────┘       └──────┘
        All IDENTICAL — same OS, same software, same config!
```

### 3.4 AMI Types

| AMI Source | Description |
|:---|:---|
| **Amazon Quick Start AMIs** | Pre-built by AWS (Ubuntu, Amazon Linux, Windows). Ready to use out of the box. |
| **AWS Marketplace AMIs** | Built by third-party vendors (e.g., WordPress pre-installed, Jenkins pre-configured). Some are free, some are paid. |
| **Community AMIs** | Shared publicly by other AWS users. Use with caution — verify trust! |
| **My AMIs (Custom AMIs)** | Created by YOU from your own configured instances. This is what "Krishna AMI" is! |

### 3.5 AWS Marketplace

The **AWS Marketplace** is like an **app store** for servers. Instead of manually installing complex software, you can find ready-made AMIs with software already installed and configured:

- WordPress blog (ready to use)
- Jenkins CI/CD server
- Machine Learning environments (with TensorFlow/PyTorch pre-installed)
- Security tools, monitoring tools, etc.

Some are **free**, some charge a **license fee** on top of your EC2 costs.

### 3.6 Real-World Scenario: The "Golden AMI" Strategy

**Company:** A fintech startup with 50 microservices.

**Problem:** Every month, the security team releases OS patches. Updating 50+ servers manually is risky and slow.

**Solution:**
1. The DevOps team creates a **"Golden AMI"** every month with the latest OS patches, security agents, and monitoring tools.
2. All development teams are **required** to build their apps on top of this Golden AMI.
3. Old servers are gradually replaced with new ones launched from the updated Golden AMI.

**Result:** Consistent, secure, and auditable infrastructure across the entire company. ✅

**Real-World Analogy:** 🍪  
An AMI is a **cookie cutter**. Instead of hand-shaping 200 cookies (servers) individually, you press the cutter once and stamp out perfect, identical cookies every time.

---

## 4. 💾 EBS (Elastic Block Storage)

### 4.1 What is EBS?

**EBS (Elastic Block Storage)** is the **hard drive** for your EC2 instance. Just like your laptop has an SSD or HDD where you store your operating system, files, and applications — EBS is the cloud equivalent.

When you launch an EC2 instance, it comes with a **root EBS volume** (like the C: drive on Windows). You can also attach **additional volumes** (like adding a D: drive or E: drive).

### 4.2 Why Do We Need EBS?

- **Persistence:** Unlike instance storage (which is lost when you stop/terminate), EBS data **survives** even when you stop an instance.
- **Backups:** You can take **snapshots** (point-in-time backups) of your entire volume.
- **Flexibility:** You can increase the size, change the type (SSD → HDD), and even detach a volume from one instance and attach it to another.

### 4.3 SSD vs HDD — Choosing the Right Volume Type

| Feature | SSD (Solid State Drive) | HDD (Hard Disk Drive) |
|:---|:---|:---|
| Speed | ⚡ Very fast | 🐢 Slower |
| Cost | 💰 More expensive | 💵 Cheaper |
| Best For | Databases, boot volumes, apps that need fast I/O | Log storage, backups, large sequential reads |
| AWS Types | `gp3` (General Purpose SSD), `io2` (Provisioned IOPS SSD) | `st1` (Throughput HDD), `sc1` (Cold HDD) |

**Real-World Analogy:** 🏎️ vs 🚌  
- **SSD** = Sports car. Fast, responsive, premium.  
- **HDD** = City bus. Slower, but carries a LOT of data cheaply.

### 4.4 EBS Volume Types — Detailed

| Volume Type | Code | Use Case | Max IOPS | Max Size |
|:---|:---|:---|:---|:---|
| General Purpose SSD | `gp3` / `gp2` | Most workloads, boot volumes | 16,000 | 16 TB |
| Provisioned IOPS SSD | `io2` / `io1` | Critical databases (Oracle, SQL Server) | 64,000 | 16 TB |
| Throughput Optimized HDD | `st1` | Big data, data warehouses, log processing | 500 | 16 TB |
| Cold HDD | `sc1` | Infrequently accessed data, archives | 250 | 16 TB |

> 💡 **Tip for beginners:** When in doubt, use `gp3`. It's the default, and it covers 90% of use cases.

### 4.5 Key EBS Concepts

#### 📦 Volume
A **volume** is a single block storage device (a virtual hard drive). You can think of it as:
- `C:` drive on Windows
- `/dev/sda1` on Linux

Every EC2 instance has at least ONE volume (the root volume where the OS lives).

#### 📸 Snapshot
A **snapshot** is a **point-in-time backup** of an EBS volume. It captures the exact state of the data at the moment the snapshot is taken.

**Why snapshots are powerful:**
- **Disaster Recovery:** If your volume gets corrupted, restore from a snapshot.
- **Migration:** Create a snapshot in Mumbai, copy it to the US region, and create a volume there.
- **AMI Creation:** Snapshots are the building blocks of AMIs!

### 4.6 The EBS Concept Flow

This is one of the **most important** diagrams to understand:

```
┌─────────────────────────────────────────────────────────────────┐
│                       EBS CONCEPT FLOW                          │
│                                                                 │
│   ┌──────────┐         ┌──────────────┐         ┌──────────┐   │
│   │  VOLUME  │ ──────► │   SNAPSHOT    │ ──────► │  VOLUME  │   │
│   │ (C: Drive)│  Backup │ (Photo of    │ Restore │ (New     │   │
│   │          │         │  your drive)  │         │  C: Drive)│  │
│   └──────────┘         └──────┬───────┘         └──────────┘   │
│                               │                                 │
│                               │ Can also create                 │
│                               ▼                                 │
│                        ┌──────────────┐                         │
│                        │     AMI      │                         │
│                        │ (Full server │                         │
│                        │  template)   │                         │
│                        └──────────────┘                         │
│                               │                                 │
│                               ▼                                 │
│                    Launch new EC2 instances!                     │
└─────────────────────────────────────────────────────────────────┘

Summary:
  Volume  →  Snapshot (backup)
  Snapshot →  New Volume (restore)
  Snapshot →  AMI (create server template)
```

### 4.7 How to Create an EBS Snapshot — Step by Step

1. Go to **EC2 Dashboard** → **Volumes** (left sidebar).
2. Select the volume you want to back up.
3. Click **Actions** → **Create Snapshot**.
4. Give it a description like `"Production-DB-Backup-2026-04-02"`.
5. Click **Create Snapshot**.
6. Done! 🎉 You can now find your snapshot under **Snapshots** in the left sidebar.

### 4.8 Real-World Scenario: The Midnight Database Disaster

**Problem:** At 2 AM, a junior developer accidentally runs `DROP DATABASE production;` and deletes every customer record. 😰

**Solution:** The DevOps team had configured **automated nightly EBS snapshots**. They:
1. Go to Snapshots → find the one from 11 PM (3 hours ago).
2. Create a new volume from that snapshot.
3. Attach the new volume to the database server.
4. Restore the database from the backup volume.

**Result:** Only 3 hours of data lost instead of everything. Crisis averted! 🛡️

**Real-World Analogy:** 📸  
- A **Volume** is your phone.  
- A **Snapshot** is a photo of all the data on your phone at this exact moment.  
- If your phone breaks tomorrow, you use the photo (snapshot) to set up a brand new phone with all your data.

---

## 5. ⚖️ Load Balancers (ELB)

### 5.1 What is a Load Balancer?

A **Load Balancer** sits between the user and your servers. Its job is to **distribute incoming traffic** across multiple EC2 instances so that no single server gets overwhelmed.

AWS calls their load balancing service **ELB (Elastic Load Balancing)**.

### 5.2 Why Do We Need Load Balancers?

| Without Load Balancer | With Load Balancer |
|:---|:---|
| 1 server handles ALL traffic | Traffic is spread across multiple servers |
| If the server crashes → **entire site goes down** | If one server crashes → others keep serving |
| Users hit the server directly (security risk) | Users hit the LB; servers are hidden (secure) |
| Cannot scale easily | Seamlessly adds/removes servers |

**Real-World Analogy:** 🏦  
Imagine a bank with ONE teller window. 100 customers are waiting in line — it takes forever, and if that teller goes on break, nobody gets served.

Now imagine the bank has 5 teller windows and a **receptionist at the door** who directs each customer to the least busy window. That receptionist is the **Load Balancer**.

### 5.3 How a Load Balancer Works

```
                    ┌──────────────┐
                    │   USERS      │
                    │  (Millions!) │
                    └──────┬───────┘
                           │
                           ▼
                ┌──────────────────────┐
                │    LOAD BALANCER     │
                │  (Single entry point │
                │   www.myapp.com)     │
                └───┬──────┬──────┬───┘
                    │      │      │
          ┌─────────┘      │      └─────────┐
          ▼                ▼                ▼
    ┌──────────┐    ┌──────────┐    ┌──────────┐
    │ Server 1 │    │ Server 2 │    │ Server 3 │
    │  (Healthy│    │ (Healthy)│    │ (CRASHED) │
    │   ✅)    │    │   ✅     │    │   ❌      │
    └──────────┘    └──────────┘    └──────────┘
                                         │
                        ❌ LB stops sending traffic here
                           (Health Check detected failure)
```

**Key mechanism — Health Checks:**  
The Load Balancer constantly pings each server (e.g., sends an HTTP request to `/health`). If a server doesn't respond correctly, the LB marks it as **unhealthy** and stops sending traffic to it. When the server recovers, traffic resumes automatically.

### 5.4 Types of AWS Load Balancers

AWS provides **four** types of load balancers:

| Type | Abbreviation | Layer | Best For |
|:---|:---|:---|:---|
| **Application Load Balancer** | ALB | Layer 7 (HTTP/HTTPS) | Web applications, microservices, REST APIs |
| **Network Load Balancer** | NLB | Layer 4 (TCP/UDP) | Gaming servers, IoT, ultra-low latency apps |
| **Gateway Load Balancer** | GWLB | Layer 3 (IP) | Firewalls, intrusion detection, network appliances |
| **Classic Load Balancer** | CLB | Layer 4 & 7 | ⚠️ **LEGACY — Do not use for new projects** |

#### 🔵 ALB (Application Load Balancer) — Most Common

- Works at **Layer 7** (HTTP/HTTPS level — understands URLs, headers, cookies).
- Can route traffic based on **URL path**:
  - `www.myapp.com/api/*` → Backend server group
  - `www.myapp.com/images/*` → Media server group
  - `www.myapp.com/admin/*` → Admin server group
- Supports **WebSockets** and **HTTP/2**.
- **Best for:** Most web applications. This is probably what you'll use 80% of the time.

#### 🟢 NLB (Network Load Balancer) — High Performance

- Works at **Layer 4** (TCP/UDP level — faster because it doesn't inspect HTTP content).
- Can handle **millions of requests per second** with ultra-low latency.
- Assigns a **static IP** (or Elastic IP) to the load balancer.
- **Best for:** Real-time multiplayer games, financial trading platforms, IoT data streams.

#### 🟡 Gateway Load Balancer (GWLB) — Specialized

- Routes traffic through **third-party virtual appliances** (firewalls, deep packet inspection).
- Used by companies that need all traffic to pass through a security appliance before reaching the application.
- **Best for:** Network security, compliance-heavy industries (banking, healthcare).

#### 🔴 Classic Load Balancer (CLB) — Legacy

- The **original** AWS load balancer (launched in 2009).
- Supports both Layer 4 and Layer 7 but with **fewer features** than ALB/NLB.
- AWS recommends **migrating** to ALB or NLB.
- **Do NOT use for new projects.**

### 5.5 Choosing the Right Load Balancer

```
Do you need HTTP/HTTPS routing (URL paths, headers)?
    │
    ├── YES → Use ALB (Application Load Balancer)
    │
    └── NO
         │
         ├── Do you need ultra-low latency or static IP?
         │       │
         │       ├── YES → Use NLB (Network Load Balancer)
         │       │
         │       └── NO → Use ALB (it's the safest default)
         │
         └── Do you need to route through firewalls/security appliances?
                 │
                 └── YES → Use GWLB (Gateway Load Balancer)
```

### 5.6 Real-World Scenario: E-Commerce Flash Sale

**Company:** An e-commerce platform having a 24-hour flash sale.

**Normal traffic:** 1,000 requests/second → 2 servers handle it fine.

**Flash sale traffic:** 50,000 requests/second → 2 servers would **melt**.

**Solution with Load Balancer + Auto Scaling:**
1. **ALB** distributes traffic across all available servers.
2. **Auto Scaling** detects CPU usage > 70% and spins up 20 more servers from a pre-built **AMI**.
3. ALB automatically adds the new servers to the pool.
4. After the sale, traffic drops → Auto Scaling **terminates** the extra servers.
5. You only pay for the servers during peak hours. 💰

---

## 6. 📈 Auto Scaling — Quick Introduction

### 6.1 What is Auto Scaling?

**Auto Scaling** automatically adjusts the **number of EC2 instances** based on real-time demand. More traffic = more servers. Less traffic = fewer servers.

### 6.2 Why Do We Need It?

Without Auto Scaling, you either:
- **Over-provision:** Run 20 servers 24/7 "just in case" → waste money. 💸
- **Under-provision:** Run 2 servers and pray traffic doesn't spike → risk downtime. 😰

Auto Scaling gives you the **right number of servers at the right time**.

### 6.3 How It Works (Simplified)

```
┌─────────────────────────────────────────────────────────┐
│                    AUTO SCALING GROUP                    │
│                                                         │
│   Minimum: 2 instances  (always running, even at 3 AM)  │
│   Desired: 4 instances  (normal business hours)         │
│   Maximum: 20 instances (Black Friday / flash sale)     │
│                                                         │
│   ┌────────────────────────────────────┐                │
│   │  SCALING POLICY (based on rules)   │                │
│   │                                    │                │
│   │  IF CPU > 70% → Add 2 instances    │                │
│   │  IF CPU < 30% → Remove 1 instance  │                │
│   └────────────────────────────────────┘                │
│                                                         │
│   Uses AMI to launch new identical instances            │
│   Load Balancer automatically discovers new instances   │
└─────────────────────────────────────────────────────────┘
```

### 6.4 Real-World Analogy

🚕 **Uber's Driver Model:**
- During morning rush hour → More drivers are online (scale up).
- At 3 AM → Fewer drivers needed (scale down).
- You don't keep 10,000 drivers idle at 3 AM just because the morning rush needs them. Auto Scaling does this for servers.

---

## 7. 🛠️ Practical Tips & Tools

### 7.1 Always Use the Correct Region 🌍

> ⚠️ **IMPORTANT:** Always set your AWS Console region to **Mumbai (ap-south-1)** if you're in India. If you accidentally launch instances in `us-east-1` (Virginia), your app will be slow for Indian users AND you might forget about those resources running up your bill.

**How to check:** Look at the **top-right corner** of the AWS Console — it shows your current region.

### 7.2 Delete Unused Resources 🗑️

AWS charges you for resources **even when they're idle**. After every practice session:
- ✅ Terminate EC2 instances you no longer need.
- ✅ Delete unattached EBS volumes.
- ✅ Release unused Elastic IPs.
- ✅ Deregister old AMIs and delete their underlying snapshots.

### 7.3 Elastic IP Cost Warning ⚠️

An **Elastic IP** is a static, permanent public IP address. Here's the tricky part:

| Elastic IP Status | Cost |
|:---|:---|
| Attached to a **running** instance | ✅ **FREE** |
| **Not attached** to any instance | ❌ **$0.005/hour ≈ $3.60/month** |
| Attached to a **stopped** instance | ❌ **$0.005/hour** (still charges!) |

> 💡 AWS charges for unused Elastic IPs to discourage IP hoarding. If you're not using it, **release it immediately**.

### 7.4 Useful Tools

| Tool | Purpose |
|:---|:---|
| **MobaXterm** | SSH client for connecting to Linux EC2 instances. Better than PuTTY — has built-in SFTP, tabs, and a nice GUI. |
| **FileZilla** | FTP/SFTP client for transferring files between your computer and EC2 instances. Drag and drop files easily. |
| **AWS CLI** | Command-line tool to manage AWS resources from your terminal. Essential for automation. |
| **PuTTY** | Alternative SSH client (Windows). Requires `.ppk` key format instead of `.pem`. |

---

## 8. 📝 Assignment & Practice Tasks

### Linux Commands Assignment
- Learn **5 new Linux commands** and be prepared to demonstrate them.
- Goal by end of the course: Master **50+ commands**.
- Be ready for **5-minute presentations** explaining what each command does.

### Hands-On Practice
- [ ] Launch an EC2 instance with Ubuntu in the Mumbai region.
- [ ] SSH into it using MobaXterm and install NGINX.
- [ ] Create a custom AMI from your configured instance.
- [ ] Launch 2 new instances from your AMI.
- [ ] Create an EBS snapshot of your root volume.
- [ ] Create an Application Load Balancer and register your instances as targets.
- [ ] Test: Stop one instance and verify the LB routes around it.
- [ ] **🚨 CLEAN UP:** Terminate all instances, delete volumes, release Elastic IPs, deregister AMI, delete snapshots.

---

## 9. 🌍 Real-World Scenario: Putting It All Together

### Scenario: Deploying a Production Web Application

**Company:** "QuickCart" — an online grocery delivery app serving 500,000 daily users across India.

**Architecture:**

```
┌──────────────────────────────────────────────────────────────────┐
│                     QUICKCART PRODUCTION SETUP                   │
│                                                                  │
│                        [ Users across India ]                    │
│                               │                                  │
│                               ▼                                  │
│                    ┌─────────────────────┐                       │
│                    │   ALB (Application  │                       │
│                    │   Load Balancer)    │                       │
│                    └────┬─────┬─────┬───┘                       │
│                         │     │     │                            │
│              ┌──────────┘     │     └──────────┐                │
│              ▼                ▼                ▼                 │
│     ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│     │   EC2 #1    │ │   EC2 #2    │ │   EC2 #3    │            │
│     │ (from AMI)  │ │ (from AMI)  │ │ (from AMI)  │            │
│     │             │ │             │ │             │             │
│     │ ┌─────────┐ │ │ ┌─────────┐ │ │ ┌─────────┐ │            │
│     │ │ EBS Vol │ │ │ │ EBS Vol │ │ │ │ EBS Vol │ │            │
│     │ │  (gp3)  │ │ │ │  (gp3)  │ │ │ │  (gp3)  │ │            │
│     │ └─────────┘ │ │ └─────────┘ │ │ └─────────┘ │            │
│     └─────────────┘ └─────────────┘ └─────────────┘            │
│              │              │              │                     │
│              └──────────────┼──────────────┘                    │
│                             ▼                                    │
│                    ┌─────────────────┐                           │
│                    │  Auto Scaling   │                           │
│                    │  Group          │                           │
│                    │  Min: 3         │                           │
│                    │  Max: 15        │                           │
│                    │  Uses: QuickCart │                           │
│                    │  Golden AMI     │                           │
│                    └─────────────────┘                           │
│                                                                  │
│        📸 Nightly EBS Snapshots for Disaster Recovery            │
└──────────────────────────────────────────────────────────────────┘
```

**How each service plays a role:**

| Service | Role in QuickCart |
|:---|:---|
| **EC2** | Runs the application servers (Node.js backend) |
| **AMI** | "QuickCart Golden AMI" — Ubuntu + Node.js + app code + monitoring agent pre-installed |
| **EBS** | Stores OS, application logs, and temporary data on each server |
| **ALB** | Distributes user traffic evenly; routes `/api` to backend, `/static` to CDN |
| **Auto Scaling** | Scales from 3 to 15 servers during peak lunch/dinner ordering hours |
| **Snapshots** | Nightly backups of database volumes for disaster recovery |

---

## 10. 🎤 Interview Questions & Answers

### Q1: What is EC2 and why is it important?
> **A:** EC2 (Elastic Compute Cloud) is AWS's virtual server service. It lets you rent computing power in the cloud by the second. It's important because it eliminates the need to buy physical hardware — you can launch, scale, and terminate servers instantly, paying only for what you use.

### Q2: What is an AMI? How is it different from a Snapshot?
> **A:** An AMI (Amazon Machine Image) is a complete template that includes the OS, software, and configuration to launch an EC2 instance. A Snapshot is a point-in-time backup of a single EBS volume. An AMI can be *created from* a snapshot, but an AMI also contains launch permissions and block device mappings that a snapshot doesn't have.

### Q3: What is EBS? What happens to EBS data when you terminate an EC2 instance?
> **A:** EBS (Elastic Block Storage) provides persistent block-level storage volumes for EC2 instances. By default, the **root EBS volume is deleted** when the instance is terminated (the "Delete on Termination" flag is ON). Additional volumes are **NOT** deleted by default. You should always take snapshots of important data before terminating.

### Q4: What is the difference between "Stop" and "Terminate" an EC2 instance?
> **A:** **Stop** pauses the instance — you can start it again later, and the EBS data is preserved (but you still pay for the EBS volume). **Terminate** permanently deletes the instance and (by default) its root volume. Terminated instances cannot be recovered.

### Q5: What is EC2 Hibernate? When would you use it?
> **A:** Hibernate saves the contents of RAM to the encrypted root EBS volume, then stops the instance. When restarted, everything loads back into memory and the application resumes exactly where it left off. Useful for applications with long initialization times (10+ minute warm-up periods for caches, indexes, or ML models).

### Q6: What are the types of AWS Load Balancers? Which one would you use for a web app?
> **A:** AWS has four types: ALB (Layer 7, HTTP/HTTPS), NLB (Layer 4, TCP/UDP), GWLB (Layer 3, for network appliances), and CLB (legacy — deprecated). For a typical web application, I would use an **ALB** because it supports path-based routing, host-based routing, WebSockets, and integrates with AWS services like WAF and Cognito.

### Q7: What is Termination Protection? Why should you enable it?
> **A:** Termination Protection is a safety feature that prevents an EC2 instance from being accidentally terminated. When enabled, any attempt to terminate the instance (via console, CLI, or API) will be blocked until protection is explicitly disabled. It's critical for production servers to prevent accidental deletion.

### Q8: What is the difference between SSD and HDD EBS volumes?
> **A:** SSD volumes (`gp3`, `io2`) offer fast, random I/O — ideal for databases and boot volumes. HDD volumes (`st1`, `sc1`) offer cheaper, sequential throughput — ideal for log processing, big data, and archival storage. SSDs cost more but are significantly faster.

### Q9: How do you back up an EBS volume?
> **A:** By creating an **EBS Snapshot**. A snapshot is a point-in-time copy of the volume stored in S3 (managed by AWS). Snapshots are incremental — only the data that changed since the last snapshot is saved, reducing storage costs. You can also automate snapshots using **Amazon Data Lifecycle Manager (DLM)**.

### Q10: How does a Load Balancer know if a server is healthy?
> **A:** Through **Health Checks**. The Load Balancer periodically sends a request (e.g., HTTP GET on `/health`) to each registered instance. If the instance returns a successful response (e.g., HTTP 200), it's marked **healthy**. If it fails to respond or returns an error after a configurable number of attempts, it's marked **unhealthy**, and the LB stops routing traffic to it.

### Q11: What is the difference between ALB and NLB?
> **A:** ALB operates at Layer 7 (HTTP/HTTPS) and can make routing decisions based on URL path, hostname, HTTP headers, and query strings. NLB operates at Layer 4 (TCP/UDP), doesn't inspect packet content, and is optimized for extreme performance (millions of requests/second) with ultra-low latency. ALB is used for web apps; NLB is used for gaming, IoT, or financial trading platforms.

### Q12: Can you move an EBS volume from one Availability Zone to another?
> **A:** Not directly. EBS volumes are locked to a specific Availability Zone. To move, you: (1) Create a snapshot of the volume, (2) Create a new volume from that snapshot in the target AZ. To move across **regions**, you copy the snapshot to the other region first, then create a volume there.

### Q13: What happens if you don't release an unused Elastic IP?
> **A:** AWS charges approximately **$0.005 per hour** (~$3.60/month) for Elastic IPs that are allocated but not associated with a running instance. This is to discourage IP address hoarding, since IPv4 addresses are a limited resource.

### Q14: What is the EBS Concept Flow? (Volume → Snapshot → Volume/AMI)
> **A:** You start with an EBS **Volume** (your data). You create a **Snapshot** (a backup/photo of that data). From that Snapshot, you can either create a new **Volume** (to restore or migrate data) or create an **AMI** (to launch identical EC2 instances). This flow is the backbone of AWS disaster recovery and scaling strategies.

### Q15: How does Auto Scaling work with AMIs and Load Balancers?
> **A:** Auto Scaling uses a **Launch Template** (which references an AMI) to spin up new EC2 instances when demand increases. These new instances are automatically registered with the **Load Balancer**, which starts distributing traffic to them. When demand decreases, Auto Scaling terminates extra instances and the LB removes them from the pool. This creates a self-healing, cost-efficient, and highly available architecture.

---

## 11. 🚫 Common Mistakes Beginners Make

### EC2 Mistakes
1. **🔴 Choosing the wrong instance type** — Picking a `c5.4xlarge` for a blog that gets 10 visitors/day. Use `t2.micro` or `t3.micro` for learning/testing.
2. **🔴 Losing the `.pem` key file** — If you lose it, you cannot SSH into your instance. Store it in a secure location (password manager, encrypted folder).
3. **🔴 Leaving all ports open (0.0.0.0/0)** — Only open the ports you need (22 for SSH, 80 for HTTP, 443 for HTTPS). Never open all traffic to all IPs.
4. **🔴 Setting shutdown behavior to "Terminate"** — One accidental `shutdown` command and your production server is gone forever.
5. **🔴 Forgetting to enable Termination Protection** on production instances.

### AMI Mistakes
6. **🔴 Hardcoding secrets in AMIs** — NEVER bake API keys, passwords, or database credentials into an AMI. Use AWS Secrets Manager or environment variables at boot time.
7. **🔴 Never updating your AMI** — An AMI created 6 months ago has 6 months of unpatched security vulnerabilities.

### EBS Mistakes
8. **🔴 Not taking regular snapshots** — If your volume fails and you have no snapshot, that data is gone forever.
9. **🔴 Leaving old EBS volumes unattached** — You're still paying for them even though nothing is using them. Clean up!
10. **🔴 Using HDD volumes for databases** — Databases need fast random I/O. Always use SSD (`gp3` or `io2`).

### Load Balancer Mistakes
11. **🔴 Not configuring Health Checks** — Without health checks, the LB blindly sends traffic to dead servers, causing errors for users.
12. **🔴 Mismatched Security Groups** — The Load Balancer's security group must allow inbound HTTP/HTTPS, AND the EC2 instances' security group must allow traffic FROM the Load Balancer.
13. **🔴 Using Classic Load Balancer for new projects** — CLB is legacy. Always use ALB or NLB.

### General AWS Mistakes
14. **🔴 Forgetting to delete practice resources** — After every lab session, terminate everything. One forgotten `m5.xlarge` costs ~$140/month.
15. **🔴 Not monitoring the AWS Free Tier usage** — Use the AWS Billing Dashboard and set up **billing alerts** to get notified before you get a surprise bill.

---

## 12. ✅ DevOps Best Practices

### Infrastructure
- 🟢 **Use Infrastructure as Code (IaC):** Manage all your EC2 instances, EBS volumes, and Load Balancers via Terraform or AWS CloudFormation — not by clicking around the console.
- 🟢 **Tag everything:** Add tags like `Environment: Production`, `Team: Backend`, `Owner: krishna@company.com` to every resource. This makes billing, auditing, and cleanup easy.
- 🟢 **Use Launch Templates over Launch Configurations:** Launch Templates support versioning, are more flexible, and are the recommended approach for Auto Scaling Groups.

### Security
- 🟢 **Enable Termination Protection** on all production EC2 instances.
- 🟢 **Encrypt EBS volumes at rest:** Enable encryption on all volumes, especially those containing customer data or credentials.
- 🟢 **Restrict Security Groups:** Principle of least privilege — only open the ports you absolutely need, only to the IPs that need access.
- 🟢 **Use IAM Roles for EC2** instead of storing Access Keys on the instance. Roles provide temporary, auto-rotating credentials.

### Cost Management
- 🟢 **Use Reserved Instances / Savings Plans** for predictable workloads (up to 72% cheaper than On-Demand).
- 🟢 **Use Spot Instances** for batch processing, CI/CD runners, and non-critical workloads (up to 90% cheaper).
- 🟢 **Set up billing alerts** and AWS Budgets to catch unexpected charges early.
- 🟢 **Right-size your instances:** Monitor CPU/memory usage with CloudWatch. If your `m5.xlarge` is at 10% CPU, downgrade to `t3.medium`.

### Reliability
- 🟢 **Deploy across multiple Availability Zones (AZs):** If one AZ goes down, your app stays alive in the others.
- 🟢 **Automate snapshots** using Amazon Data Lifecycle Manager (DLM) — don't rely on manual backups.
- 🟢 **Use Auto Scaling** with proper min/max/desired settings so your app handles traffic spikes gracefully.
- 🟢 **Implement the Golden AMI strategy:** Monthly updated AMIs with the latest patches, security agents, and monitoring tools.

### Monitoring & Logging
- 🟢 **Enable CloudWatch monitoring** for every EC2 instance (CPU, memory, disk, network).
- 🟢 **Set up CloudWatch Alarms** for critical thresholds (CPU > 80%, disk > 90%).
- 🟢 **Centralize logs** using CloudWatch Logs or ELK Stack.
- 🟢 **Enable VPC Flow Logs** to track network traffic for security analysis.

---

## 13. 📝 Quick Revision Summary

| Concept | What It Is | Key Takeaway |
|:---|:---|:---|
| **EC2** | Virtual servers in the cloud | Rent by the second. Choose instance type wisely. |
| **Instance Type** | CPU/RAM/storage configuration | `t2.micro` for learning, `m5/c5` for production. |
| **Auto-Recovery** | Automatic hardware failure recovery | Instance migrates to healthy hardware automatically. |
| **Shutdown Behavior** | What happens on `shutdown` command | "Stop" = pause. "Terminate" = delete forever. ⚠️ |
| **Hibernate** | Save RAM to disk, resume later | Like closing your laptop lid. Needs encrypted EBS. |
| **Termination Protection** | Safety lock against accidental deletion | ALWAYS enable on production instances. |
| **AMI** | Server template / blueprint | Create once, launch hundreds of identical servers. |
| **Golden AMI** | Monthly-patched company AMI | Best practice for consistent, secure infrastructure. |
| **AWS Marketplace** | App store for server software | Find pre-built AMIs (WordPress, Jenkins, etc.). |
| **EBS** | Virtual hard drive for EC2 | Persistent storage. Use `gp3` SSD by default. |
| **EBS Snapshot** | Point-in-time backup of a volume | Incremental. Can create new volumes or AMIs from it. |
| **Volume → Snapshot → Volume/AMI** | The EBS concept flow | Core of AWS backup, migration, and scaling strategy. |
| **ALB** | Application Load Balancer (Layer 7) | Best for web apps. Supports URL path routing. |
| **NLB** | Network Load Balancer (Layer 4) | Best for ultra-low latency (gaming, trading). |
| **GWLB** | Gateway Load Balancer (Layer 3) | For network security appliances. |
| **CLB** | Classic Load Balancer | ⚠️ Legacy — don't use for new projects. |
| **Health Checks** | LB pings servers to check if alive | Critical! Without it, LB sends traffic to dead servers. |
| **Auto Scaling** | Automatically adjusts server count | Right number of servers at the right time. Saves money. |
| **Elastic IP** | Static public IP address | Free when attached to running instance. Charged if unused! |
| **MobaXterm** | SSH client for Linux EC2 | Better than PuTTY — has SFTP, tabs, GUI. |
| **FileZilla** | File transfer tool (SFTP) | Drag-and-drop files to/from EC2 instances. |

---

← Prev: [13_ELB_and_EC2.md](13_ELB_and_EC2.md) | Next: [15_AWS_S3_and_Storage.md](15_AWS_S3_and_Storage.md) →
