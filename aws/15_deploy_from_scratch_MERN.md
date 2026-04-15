# 🚀 Complete Guide: Deploying a MERN Stack on AWS (Free Tier) Using the AWS Management Console

> **Audience:** Beginners who want to become job-ready cloud professionals.
> **Goal:** Deploy a production-grade MERN app on AWS using only the Console — step by step, with real-world best practices baked in.

---

## 📋 Table of Contents

1. [Prerequisites & AWS Account Setup](#1-prerequisites--aws-account-setup)
2. [IAM User Setup & Security Best Practices](#2-iam-user-setup--security-best-practices)
3. [Region Selection Strategy](#3-region-selection-strategy)
4. [Networking — VPC Deep Dive](#4-networking--vpc-deep-dive)
5. [Security Groups & NACLs](#5-security-groups--nacls)
6. [Compute Layer — EC2 Setup](#6-compute-layer--ec2-setup)
7. [Database Layer — MongoDB Deployment](#7-database-layer--mongodb-deployment)
8. [Deploying the MERN Application](#8-deploying-the-mern-application)
9. [Advanced Networking — VPC Peering](#9-advanced-networking--vpc-peering)
10. [Traffic Management — ALB, Route 53, HTTPS](#10-traffic-management--alb-route-53-https)
11. [Monitoring & Logging — CloudWatch](#11-monitoring--logging--cloudwatch)
12. [Cost Optimization (Mandatory)](#12-cost-optimization-mandatory)
13. [Industry Best Practices](#13-industry-best-practices)
14. [Scenario-Based Interview Q&A](#14-scenario-based-interview-qa)

---

## 1. Prerequisites & AWS Account Setup

### What
Before any deployment, you need a properly configured AWS account with billing safeguards in place.

### Why
An improperly set-up account without billing alerts or MFA can result in unexpected charges or a security breach within hours of creation.

### How — Step by Step

**Step 1.1 — Create Your AWS Account**
1. Visit [https://aws.amazon.com](https://aws.amazon.com) and click **Create an AWS Account**.
2. Enter your email address, set an account name (e.g., `mern-learning-account`), and set a strong root password.
3. Choose **Personal** account type.
4. Enter valid credit/debit card details — AWS Free Tier is free for 12 months within limits, but a card is required for identity verification.
5. Complete phone verification.
6. Select the **Basic (Free) Support Plan**.

**Step 1.2 — Enable MFA on Root Account (CRITICAL)**
1. Log into the AWS Console as root.
2. Click your account name in the top-right → **Security credentials**.
3. Under **Multi-factor authentication (MFA)**, click **Assign MFA device**.
4. Choose **Authenticator app** (use Google Authenticator or Authy on your phone).
5. Scan the QR code and enter two consecutive OTP codes to confirm.

> ⚠️ **NEVER use the root account for day-to-day tasks.** Root has unrestricted access to everything including billing. One compromised session = total account takeover.

**Step 1.3 — Set Up Billing Alerts**
1. From the top-right menu → **Account** → **Billing preferences**.
2. Enable **Receive AWS Free Tier usage alerts**.
3. Enable **Receive Billing Alerts**.
4. Go to **CloudWatch** → **Alarms** → **Create alarm**.
5. Select **Billing → Total Estimated Charge**.
6. Set threshold: `> $1` (triggers before any real charge).
7. Create an SNS topic, enter your email, and confirm the subscription.

### Impact if Misconfigured
- No MFA on root = single point of failure for entire account
- No billing alert = surprise charges discovered only on the monthly bill

---

## 2. IAM User Setup & Security Best Practices

### What
IAM (Identity and Access Management) lets you create users, groups, and roles with specific permissions. You'll create a non-root admin user for all console activities.

### Why
The principle of least privilege: give users only the permissions they need, nothing more. This limits the blast radius if credentials are compromised.

### How — Step by Step

**Step 2.1 — Create an Admin IAM User**
1. In the AWS Console, search for **IAM** and open it.
2. Click **Users** → **Create user**.
3. Username: `mern-admin`
4. Check **Provide user access to the AWS Management Console**.
5. Select **I want to create an IAM user**.
6. Set a custom password, uncheck "must create new password at next sign-in" for now.
7. Click **Next**.

**Step 2.2 — Attach Permissions**
1. On the permissions page, select **Attach policies directly**.
2. Search for and select **AdministratorAccess** (for learning purposes).

> 💡 **Industry Note:** In production, never assign `AdministratorAccess` to a regular user. Instead, create granular policies per role (e.g., EC2 admin, S3 read-only, etc.).

3. Click **Next** → **Create user**.
4. **Download or save the credentials** (Console sign-in URL, username, password).

**Step 2.3 — Enable MFA on IAM User**
1. Click the newly created user `mern-admin`.
2. Go to the **Security credentials** tab.
3. Under MFA, click **Assign MFA device** and repeat the authenticator app setup.

**Step 2.4 — Sign Out of Root and Sign In as IAM User**
1. Copy the Account sign-in URL (format: `https://ACCOUNT_ID.signin.aws.amazon.com/console`).
2. Open it in your browser, log in as `mern-admin`.
3. From this point forward, always use this IAM user — never root.

### IAM Best Practices Summary

| Practice | Reason |
|---|---|
| Never use root for daily tasks | Root cannot be restricted |
| Enable MFA on all users | Prevents credential theft |
| Use groups, not individual user policies | Easier permission management |
| Rotate access keys every 90 days | Reduces exposure window |
| Review unused permissions quarterly | Least privilege enforcement |

---

## 3. Region Selection Strategy

### What
AWS has 30+ geographic regions. You must choose where to deploy your resources.

### Why
- **Latency:** Users in India should use Mumbai (`ap-south-1`), not US East.
- **Data Residency:** Some countries legally require data to stay within their borders.
- **Cost:** Pricing varies by region (US East `us-east-1` is usually cheapest).
- **Service Availability:** Not all services are available in every region.

### How — Choosing Your Region

**Decision Criteria:**

| Factor | Recommended Region |
|---|---|
| Users primarily in India | `ap-south-1` (Mumbai) |
| Users primarily in USA | `us-east-1` (N. Virginia) |
| Users in Europe | `eu-west-1` (Ireland) |
| Lowest cost globally | `us-east-1` |
| Free Tier learning (any) | `us-east-1` or your nearest |

**Step 3.1 — Set Your Region**
1. In the AWS Console top-right, click the region dropdown (e.g., "N. Virginia").
2. Select your desired region — for this guide, we'll use **US East (N. Virginia) — us-east-1**.
3. Every resource you create will live in this region unless you explicitly change it.

> ⚠️ **Critical:** All networking resources (VPC, Subnets, EC2) must be in the same region. Accidentally creating resources in different regions is a common beginner mistake.

---

## 4. Networking — VPC Deep Dive

### Architecture Overview

```
+------------------------------------------------------------------+
|                        AWS Region: us-east-1                     |
|                                                                  |
|  +------------------------------------------------------------+  |
|  |                    VPC: 10.0.0.0/16                        |  |
|  |                                                            |  |
|  |   +------------------+      +------------------+          |  |
|  |   | Availability      |      | Availability      |         |  |
|  |   | Zone: us-east-1a  |      | Zone: us-east-1b  |         |  |
|  |   |                  |      |                  |          |  |
|  |   | +-------------+  |      | +-------------+  |          |  |
|  |   | | Public Sub  |  |      | | Public Sub  |  |          |  |
|  |   | | 10.0.1.0/24 |  |      | | 10.0.2.0/24 |  |          |  |
|  |   | | (EC2/React) |  |      | | (ALB Node2) |  |          |  |
|  |   | +-------------+  |      | +-------------+  |          |  |
|  |   |                  |      |                  |          |  |
|  |   | +-------------+  |      | +-------------+  |          |  |
|  |   | | Private Sub |  |      | | Private Sub |  |          |  |
|  |   | | 10.0.3.0/24 |  |      | | 10.0.4.0/24 |  |          |  |
|  |   | | (MongoDB)   |  |      | | (DB Replica)|  |          |  |
|  |   | +-------------+  |      | +-------------+  |          |  |
|  |   +------------------+      +------------------+          |  |
|  |                                                            |  |
|  |   Internet Gateway (IGW)    NAT Gateway (optional)        |  |
|  +------------------------------------------------------------+  |
+------------------------------------------------------------------+
                              |
                         [ Internet ]
                              |
                         [ User's Browser ]
```

### Traffic Flow Diagram

```
Internet User
     |
     v
[Internet Gateway (IGW)]
     |
     v
[Public Subnet — 10.0.1.0/24]
[EC2: Node.js/Express Backend]  <----  [EC2: React Frontend / S3+CloudFront]
     |
     | (internal traffic only — no public internet)
     v
[Private Subnet — 10.0.3.0/24]
[EC2: MongoDB]

NAT Gateway Flow (for outbound from private subnet):
[MongoDB EC2 in Private Subnet]
     |
     v
[NAT Gateway in Public Subnet]
     |
     v
[Internet Gateway]
     |
     v
[Internet (e.g., to download updates)]
```

---

### 4.1 — Create a VPC from Scratch

**What:** A Virtual Private Cloud is your own isolated network within AWS.

**Why:** Without a VPC, your resources would share a network with other AWS customers. VPC gives you full control over IP addressing, routing, and access.

**CIDR Block Planning — Why 10.0.0.0/16?**

| CIDR | Total IPs | Usable | Use Case |
|---|---|---|---|
| 10.0.0.0/16 | 65,536 | 65,531 | Large enterprise VPC |
| 10.0.0.0/24 | 256 | 251 | Single small subnet |
| 10.0.1.0/24 | 256 | 251 | One of our subnets |

We use `10.0.0.0/16` for the VPC so we have room to carve out many `/24` subnets (one per environment/tier).

> AWS reserves 5 IPs in every subnet: network address, VPC router, DNS, future use, broadcast.

**Step-by-Step:**
1. In the Console, search **VPC** and open the VPC Dashboard.
2. Click **Create VPC**.
3. Select **VPC only** (not "VPC and more" — we'll build manually to learn).
4. **Name tag:** `mern-vpc`
5. **IPv4 CIDR block:** `10.0.0.0/16`
6. **IPv6:** No IPv6 CIDR block (not needed for Free Tier learning).
7. **Tenancy:** Default (dedicated hardware costs significantly more).
8. Click **Create VPC**.

### 4.2 — Create Subnets

**What:** Subnets divide your VPC into smaller networks. Public subnets can reach the internet; private subnets cannot (directly).

**Why Multi-AZ?** If one Availability Zone goes down (power failure, cooling issue), your app stays alive in the other AZ. This is the foundation of high availability.

**Create Public Subnet 1 (AZ: us-east-1a)**
1. In VPC Dashboard → **Subnets** → **Create subnet**.
2. VPC: `mern-vpc`
3. Subnet name: `mern-public-subnet-1a`
4. Availability Zone: `us-east-1a`
5. IPv4 CIDR block: `10.0.1.0/24`
6. Click **Add new subnet** to add more in the same flow.

**Create Public Subnet 2 (AZ: us-east-1b)**
- Name: `mern-public-subnet-1b`
- AZ: `us-east-1b`
- CIDR: `10.0.2.0/24`

**Create Private Subnet 1 (AZ: us-east-1a)**
- Name: `mern-private-subnet-1a`
- AZ: `us-east-1a`
- CIDR: `10.0.3.0/24`

**Create Private Subnet 2 (AZ: us-east-1b)**
- Name: `mern-private-subnet-1b`
- AZ: `us-east-1b`
- CIDR: `10.0.4.0/24`

7. Click **Create subnet**.

**Enable Auto-assign Public IP on Public Subnets:**
1. Select `mern-public-subnet-1a` → **Actions** → **Edit subnet settings**.
2. Check **Enable auto-assign public IPv4 address**.
3. Save. Repeat for `mern-public-subnet-1b`.

> Do NOT enable auto-assign public IP on private subnets. Instances there should never have a public IP.

### 4.3 — Create Internet Gateway (IGW)

**What:** The IGW is the door between your VPC and the public internet.

**Why:** Without an IGW, nothing in your VPC can reach or be reached from the internet — not even your web server.

1. VPC Dashboard → **Internet gateways** → **Create internet gateway**.
2. Name: `mern-igw`
3. Click **Create internet gateway**.
4. After creation, click **Actions** → **Attach to VPC**.
5. Select `mern-vpc` → **Attach internet gateway**.

> One IGW per VPC. It is highly available by default — AWS manages redundancy for you.

### 4.4 — Create Route Tables

**What:** Route tables tell your subnet where to send traffic. Like a GPS for network packets.

**Why:** Public subnets need a route to the IGW. Private subnets should NOT have a route to the IGW (they use NAT if they need internet access at all).

**Public Route Table:**
1. VPC Dashboard → **Route tables** → **Create route table**.
2. Name: `mern-public-rt`
3. VPC: `mern-vpc`
4. Click **Create route table**.
5. Select `mern-public-rt` → **Routes** tab → **Edit routes** → **Add route**:
   - Destination: `0.0.0.0/0`
   - Target: `mern-igw` (Internet Gateway)
6. Save routes.
7. Click **Subnet associations** tab → **Edit subnet associations**.
8. Check `mern-public-subnet-1a` and `mern-public-subnet-1b` → Save.

**Private Route Table:**
1. Create another route table: `mern-private-rt`
2. VPC: `mern-vpc`
3. Do NOT add a `0.0.0.0/0` route to the IGW — this is what makes it private.
4. Associate with `mern-private-subnet-1a` and `mern-private-subnet-1b`.

### 4.5 — NAT Gateway (Optional — Cost Alert)

**What:** NAT Gateway allows instances in private subnets to reach the internet (for updates, package installs) without being reachable from the internet.

**Why:** Your MongoDB instance in the private subnet may need to download updates. NAT Gateway enables this outbound-only connection.

> 💰 **Cost Alert — NAT Gateway is NOT Free Tier eligible.**
> - NAT Gateway costs approximately **$0.045/hour** (~$32/month) + **$0.045 per GB** of data processed.
> - For learning/dev, skip NAT Gateway and instead use a Bastion Host to SSH into private instances for updates.

**FREE Alternative — Use EC2 Instance as NAT (t2.micro Free Tier):**

This is more complex to manage but completely free under Free Tier.

**Step 1: Launch the NAT Instance**
1. EC2 Dashboard → **Launch Instances**.
2. **Name:** `mern-nat-instance`
3. **AMI:** Ubuntu Server 24.04 LTS (Free Tier Eligible).
4. **Instance Type:** `t2.micro`
5. **Key Pair:** Select your `mern-keypair`.
6. **Network Settings:** 
   - **VPC:** `mern-vpc`
   - **Subnet:** `mern-public-subnet-1a` (Must be a public subnet).
   - **Auto-assign public IP:** Enable.
   - **Security Group:** Create new `mern-nat-sg`. 
     > 💡 **AWS Console Tip - Resolving Default Rules:** AWS usually auto-populates some default rules here. Update them to match exactly this:
     > - **Change Rule 1 (Default SSH `0.0.0.0/0`):** Change the Source from `Anywhere-IPv4` to **My IP**. This secures your server so only you can remote into it.
     > - **Change Rule 2 (Default Custom TCP):** Change the Type from `Custom TCP` to **All traffic**. Change the Source to **Custom**, and type exactly `10.0.0.0/16` into the box. This allows all traffic from your private subnet (like MongoDB) to route through this NAT.
7. Click **Launch Instance**.

**Step 2: Disable Source/Destination Check**
> **Why do this?** By default, AWS blocks an EC2 instance from sending or receiving traffic if it isn't the final destination. Since a NAT instance acts as a "middleman" router passing traffic from your private database out to the internet, we must disable this security check so it allows third-party traffic to pass through.
1. EC2 Dashboard → **Instances**.
2. Select your `mern-nat-instance`.
3. Click **Actions** → **Networking** → **Change source/destination check**.
4. Check **Stop** (Disable). 
5. Click **Save**.

**Step 3: Configure NAT Routing (Inside EC2)**
1. SSH into the instance: `ssh -i ~/Downloads/mern-keypair.pem ubuntu@<nat-instance-public-ip>`
2. Enable IP Forwarding in Linux:
   > **How this works:** Even though AWS allows the traffic through (Step 2), the Linux OS inside the EC2 will block it by default. We tell the Linux kernel it is allowed to route packets by appending `net.ipv4.ip_forward = 1` to its system configuration file, and `sysctl -p` applies the rule immediately.
   ```bash
   # Add the routing rule to the configuration file
   echo "net.ipv4.ip_forward = 1" | sudo tee -a /etc/sysctl.conf
   
   # Apply the change immediately
   sudo sysctl -p
   ```
3. Configure `iptables` (Ubuntu version):
   ```bash
   # Add the NAT masking rule (maps private IPs to this instance's public IP)
   sudo iptables -t nat -A POSTROUTING -o ens5 -s 10.0.0.0/16 -j MASQUERADE
   
   # Install persistent iptables to save the rule across server reboots
   # (Note: Press ENTER for "Yes" if a pink screen prompts you during install)
   sudo apt-get update
   sudo apt-get install -y iptables-persistent
   sudo netfilter-persistent save
   ```
4. Exit the SSH session.

**Step 4: Update Private Route Table**
1. VPC Dashboard → **Route Tables**.
2. Select `mern-private-rt`.
3. **Routes** tab → **Edit routes** → **Add route**:
   - **Destination:** `0.0.0.0/0`
   - **Target:** Instance → Select your `mern-nat-instance`.
4. Save changes.

**If you do create a NAT Gateway (paid):**
1. VPC Dashboard → **NAT gateways** → **Create NAT gateway**.
2. Name: `mern-nat-gw`
3. Subnet: `mern-public-subnet-1a` (NAT Gateway goes in the PUBLIC subnet).
4. Connectivity type: Public.
5. **Allocate Elastic IP** → click Allocate Elastic IP.
6. Click **Create NAT gateway**.
7. After it becomes Available, add a route in `mern-private-rt`:
   - Destination: `0.0.0.0/0`
   - Target: `mern-nat-gw`


---

## 5. Security Groups & NACLs

### The Critical Difference

```
Security Groups (SG):                Network ACLs (NACL):
+---------------------------+        +---------------------------+
| - Operates at instance    |        | - Operates at subnet      |
|   (ENI) level             |        |   level                   |
| - STATEFUL: return        |        | - STATELESS: must allow   |
|   traffic auto-allowed    |        |   inbound AND outbound    |
| - Only ALLOW rules        |        |   explicitly              |
| - Evaluated as a group    |        | - ALLOW and DENY rules    |
| - Default: deny all in    |        | - Rules evaluated in      |
|   (no inbound rules)      |        |   numbered order          |
+---------------------------+        +---------------------------+
```

**Analogy:**
- **Security Group** = Building door lock. If you unlock it from outside (inbound allowed), you can leave (return traffic automatically allowed).
- **NACL** = Building AND room locks. Even if you get through the building door, each room checks separately. Return traffic must also be explicitly unlocked.

### Port Reference for MERN Stack

| Port | Protocol | Service | Direction |
|---|---|---|---|
| 22 | TCP | SSH (admin access) | Inbound |
| 80 | TCP | HTTP (React app) | Inbound |
| 443 | TCP | HTTPS | Inbound |
| 3000 | TCP | React dev server | Inbound (dev only) |
| 5000 | TCP | Node.js/Express API | Inbound (from frontend SG) |
| 27017 | TCP | MongoDB | Inbound (from backend SG only) |
| 1024-65535 | TCP | Ephemeral ports (NACL only) | Outbound |

### 5.1 — Security Groups

**Create Security Group: Bastion Host SG**
1. EC2 Dashboard → **Security Groups** → **Create security group**.
2. Name: `mern-bastion-sg`
3. Description: `Allow SSH from admin IP only`
4. VPC: `mern-vpc`
5. Inbound rules:
   - Type: SSH | Port: 22 | Source: **My IP** (your current public IP — auto-populated)
6. Outbound rules: leave default (allow all outbound)
7. Create security group.

**Create Security Group: Backend (Node.js) SG**
1. Name: `mern-backend-sg`
2. Description: `Backend Node.js Express server`
3. VPC: `mern-vpc`
4. Inbound rules:
   - Type: SSH | Port: 22 | Source: `mern-bastion-sg` (security group ID, not CIDR)
   - Type: Custom TCP | Port: 5000 | Source: `0.0.0.0/0` (or restrict to frontend SG)
   - Type: HTTP | Port: 80 | Source: `0.0.0.0/0`
5. Create.

**Create Security Group: Database (MongoDB) SG**
1. Name: `mern-db-sg`
2. Description: `MongoDB private subnet only`
3. VPC: `mern-vpc`
4. Inbound rules:
   - Type: Custom TCP | Port: 27017 | Source: `mern-backend-sg` (ONLY the backend SG)
   - Type: SSH | Port: 22 | Source: `mern-bastion-sg`
5. **No inbound from the internet — MongoDB is never exposed publicly.**
6. Create.

**Create Security Group: Frontend SG (if hosting on EC2)**
1. Name: `mern-frontend-sg`
2. Description: `Frontend React application`
3. Inbound:
   - HTTP (80) from `0.0.0.0/0`
   - HTTPS (443) from `0.0.0.0/0`
   - SSH (22) from `mern-bastion-sg`
4. Create.

### 5.2 — Network ACLs (NACLs)

> For most setups, the default NACL (which allows all traffic) is fine when Security Groups are properly configured. NACLs are your second layer for subnet-wide rules.

**Blocking a Malicious IP Using NACLs:**

1. VPC Dashboard → **Network ACLs**.
2. Select the NACL associated with your public subnet.
3. Click **Inbound rules** → **Edit inbound rules**.
4. Add rule:
   - Rule number: `50` (lower numbers evaluated first)
   - Type: All traffic
   - Source: `<malicious-ip>/32`
   - Allow/Deny: **DENY**
5. Ensure a lower-numbered ALLOW rule exists for legitimate traffic (e.g., rule 100: allow all).
6. Save.

> NACL rules are evaluated in ascending numeric order. Rule 50 (DENY malicious IP) is checked before rule 100 (ALLOW all). First match wins.

**Why use NACL for IP blocking instead of Security Group?**
- Security Groups have no DENY rule — you can only control what's allowed.
- NACLs support explicit DENY — perfect for blocking bad actors.

### 5.3 — Bastion Host

**What:** A hardened EC2 instance in the public subnet that acts as the only SSH entry point into your private resources.

**Why:** MongoDB and other private instances should never have public IPs. You SSH into the Bastion first, then from Bastion you SSH into private instances. This creates a single, auditable entry point.

```
Your Laptop
    |
    | SSH (port 22)
    v
[Bastion Host — Public Subnet — Public IP]
    |
    | SSH (port 22, internal)
    v
[MongoDB EC2 — Private Subnet — Private IP only]
```

**Setup Step-by-Step:**

**Step 1: Launch the Bastion EC2**
1. EC2 Dashboard → **Launch Instances**.
2. **Name:** `mern-bastion-host`
3. **AMI:** Ubuntu Server 24.04 LTS (Free Tier Eligible).
4. **Instance Type:** `t2.micro`
5. **Key Pair:** Select your `mern-keypair`.
6. **Network Settings:** 
   - **VPC:** `mern-vpc`
   - **Subnet:** `mern-public-subnet-1a` (Must be public).
   - **Auto-assign public IP:** Enable.
   - **Security Group:** Select existing → `mern-bastion-sg`. 
7. Click **Launch Instance**.

**Step 2: Connect using SSH Agent Forwarding**
> **Why Agent Forwarding?** To SSH from the Bastion into your private MongoDB, the Bastion usually needs your secret `.pem` key file. But copying a master private key onto a server is a huge security risk! SSH Agent Forwarding magically passes your laptop's key authentication through the secure connection. This lets you log into the private database *without* ever uploading the key file to the Bastion.

Run these commands on your local laptop terminal:
```bash
# 1. Start the SSH agent (Required if you get "Could not open a connection" error)
# For Mac/Linux / Git Bash (Windows):
eval "$(ssh-agent -s)"

# OR For Windows PowerShell (Run as Administrator if the service is disabled):
# Start-Service ssh-agent

# 2. Add your key to your laptop's SSH agent
ssh-add ~/Downloads/mern-keypair.pem

# 2. SSH to bastion with agent forwarding (the -A flag does the magic!)
ssh -A ubuntu@<bastion-public-ip>

# 3. Now you are inside the Bastion! 
# Note: You will create the MongoDB instance in Section 7. Once created,
# you can SSH directly to its private IP from inside the Bastion like this:
ssh ubuntu@<mongodb-private-ip>
```

---

## 6. Compute Layer — EC2 Setup

### 6.1 — Create a Key Pair

**What:** An SSH key pair (public + private) for secure access to EC2 instances.

1. EC2 Dashboard → **Key Pairs** → **Create key pair**.
2. Name: `mern-keypair`
3. Key pair type: RSA
4. Private key file format: `.pem` (for Linux/Mac) or `.ppk` (for PuTTY on Windows)
5. Click **Create key pair** — the `.pem` file downloads automatically.
6. On your local machine:

```bash
chmod 400 ~/Downloads/mern-keypair.pem
```

> This file is your password. If lost, you cannot SSH into the instance. There is no "forgot key" option — you must terminate and replace the instance.

### 6.2 — Launch Backend EC2 (Node.js + Express)

**What:** An EC2 instance in the public subnet that runs your Node.js API server.

**Free Tier:** t2.micro (1 vCPU, 1GB RAM) — 750 hours/month free for 12 months.

1. EC2 Dashboard → **Instances** → **Launch instances**.
2. **Name:** `mern-backend`
3. **AMI:** Ubuntu Server 24.04 LTS (Free Tier eligible)
4. **Instance type:** `t2.micro` (Free Tier eligible)
5. **Key pair:** `mern-keypair`
6. **Network settings → Edit:**
   - VPC: `mern-vpc`
   - Subnet: `mern-public-subnet-1a`
   - Auto-assign public IP: Enable
   - Security group: Select existing → `mern-backend-sg`
7. **Storage:** 8 GB gp3 (Free Tier gives 30 GB total EBS — 8 GB per instance is fine)
8. **Advanced details → User data** (runs on first boot):

```bash
#!/bin/bash
# Update system
apt-get update -y

# Install Node.js 20 (LTS)
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt-get install -y nodejs

# Install PM2 globally
npm install -g pm2

# Install git
apt-get install -y git

# Create app directory
mkdir -p /var/www/backend
chown ubuntu:ubuntu /var/www/backend

echo "Backend setup complete" > /var/log/setup.log
```

9. Click **Launch instance**.

### 6.3 — Assign an Elastic IP to the Backend

**What:** A static public IPv4 address that you own until you explicitly release it.

**Why:** EC2 instances get a new public IP every time they restart. An Elastic IP stays the same, so your domain's DNS record doesn't break.

> 💰 **Cost Alert:**
> - **One Elastic IP attached to a running instance = FREE** (within Free Tier).
> - **Elastic IP NOT attached to a running instance = $0.005/hour charge.**
> - **Always release Elastic IPs if you stop your instance.**

1. EC2 Dashboard → **Elastic IPs** (under Network & Security) → **Allocate Elastic IP address**.
2. Keep defaults → **Allocate**.
3. Select the newly created EIP → **Actions** → **Associate Elastic IP address**.
4. Select your newly created `mern-backend` EC2 instance and its private IP.
5. Click **Associate**.

### 6.4 — Launch Frontend EC2 (Optional — React Build)

Same process, but:
- Name: `mern-frontend`
- SG: `mern-frontend-sg`
- Subnet: `mern-public-subnet-1b` (different AZ for diversity)
- User data:

```bash
#!/bin/bash
apt-get update -y
# Install Node.js so we can build the React app
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt-get install -y nodejs
# Install and Start Nginx
apt-get install -y nginx
systemctl enable nginx
systemctl start nginx
mkdir -p /var/www/frontend
```

> 💡 **Free Tier Alternative to EC2 for Frontend:** Host your React build on **S3 + CloudFront**.
> - S3: 5 GB storage + 20,000 GET requests/month free.
> - CloudFront: 1 TB data transfer + 10 million requests/month free.
> - No server to maintain, auto-scaling, global CDN.

### 6.5 — SSH Into Your EC2 Instance

Because we only allowed SSH from the Bastion Host in our Security Group (`mern-backend-sg`), you cannot SSH directly into the backend from your laptop!

```bash
# 1. SSH into your Bastion Host from your laptop (with SSH Agent Forwarding)
ssh -A ubuntu@<bastion-public-ip>

# 2. From INSIDE the Bastion, SSH to your backend EC2 using its PRIVATE IP
ssh ubuntu@<backend-private-ip>

# 3. Verify Node.js and PM2 are installed
node --version
npm --version
pm2 --version
```

### 6.6 — Instance Type Reference

| Instance | vCPU | RAM | Free Tier | Use Case |
|---|---|---|---|---|
| t2.micro | 1 | 1 GB | ✅ Yes | Learning, small apps |
| t3.micro | 2 | 1 GB | ✅ Yes (some regions) | Slightly better performance |
| t3.small | 2 | 2 GB | ❌ No | Production small app |
| t3.medium | 2 | 4 GB | ❌ No | Production medium app |

> ⚠️ Free Tier gives 750 hours/month combined across ALL t2.micro or t3.micro instances. Two t2.micro instances running 24/7 = 1,488 hours = charges apply after 750 hours.

---

## 7. Database Layer — MongoDB Deployment

### Option A: Self-Hosted MongoDB on EC2 (Free Tier Friendly)

**Pros:**
- Completely free within EC2 Free Tier limits
- Full control over configuration
- No data egress costs to an external service

**Cons:**
- You manage backups, updates, replication
- Single point of failure unless you set up replica sets
- Requires MongoDB administration knowledge

**Step 7.1 — Launch MongoDB EC2**
1. Launch a new EC2 instance:
   - Name: `mern-mongodb`
   - AMI: Ubuntu Server 24.04 LTS
   - Instance type: `t2.micro`
   - Key pair: `mern-keypair`
   - **Subnet: `mern-private-subnet-1a`** (CRITICAL — private subnet only)
   - Auto-assign public IP: **Disable** (private subnet, no public IP)
   - SG: `mern-db-sg`
   - Storage: 20 GB gp3 (keep total under 30 GB for Free Tier)
2. Launch.

**Step 7.2 — Install MongoDB via Bastion**
```bash
# SSH to Bastion first
ssh -A -i ~/Downloads/mern-keypair.pem ubuntu@<bastion-public-ip>

# From Bastion, SSH to MongoDB instance using private IP
ssh ubuntu@10.0.3.xxx

# Install MongoDB 7.0 Community on Ubuntu Linux
sudo apt-get install gnupg curl

curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | \
   sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg \
   --dearmor

echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

sudo apt-get update
sudo apt-get install -y mongodb-org

# Start and enable MongoDB
sudo systemctl start mongod
sudo systemctl enable mongod

# Verify
sudo systemctl status mongod
```

**Step 7.3 — Secure MongoDB**
```bash
# Connect to MongoDB shell
mongosh

# Switch to admin database
use admin

# Create admin user
db.createUser({
  user: "mernAdmin",
  pwd: "StrongPassword123!",
  roles: [{ role: "userAdminAnyDatabase", db: "admin" }]
})

# Create app-specific database user
use merndb
db.createUser({
  user: "mernAppUser",
  pwd: "AppPassword456!",
  roles: [{ role: "readWrite", db: "merndb" }]
})

exit
```

**Step 7.4 — Enable MongoDB Authentication**
```bash
# Open the configuration file using the vi editor
sudo vi /etc/mongod.conf

# 💡 vi Editor Quick Guide:
# 1. Press 'i' to enter Insert mode.
# 2. Make your changes (use arrow keys to navigate).
# 3. Press 'Esc' to exit Insert mode.
# 4. Type ':wq' and press Enter to save and quit.
```

```yaml
# In mongod.conf, find the security section:
security:
  authorization: enabled

# Also update the bindIp to allow only local and VPC CIDR:
net:
  port: 27017
  bindIp: 127.0.0.1,10.0.0.0/16
```

```bash
sudo systemctl restart mongod
```

> MongoDB should ONLY listen on its private IP, never on `0.0.0.0` (all interfaces). Combined with the Security Group that only allows port 27017 from `mern-backend-sg`, this gives you two layers of database protection.

---

### Option B: MongoDB Atlas Free Tier (Managed)

**Pros:**
- Managed backups, monitoring, auto-scaling
- Built-in replica set (3 nodes) even on free tier
- No server administration

**Cons:**
- Free tier (M0) limited to 512 MB storage
- Data leaves AWS — potential latency and data residency concerns
- Data transfer costs if regions don't match

**Setup:**
1. Go to [https://cloud.mongodb.com](https://cloud.mongodb.com) → Create free account.
2. Create a new project → Create a cluster → Select **M0 Free** tier.
3. Choose **AWS** and the **same region** as your EC2 (e.g., us-east-1).
4. Under **Network Access** → **Add IP Address**:
   - Add the private IP of your backend EC2: `10.0.1.xxx/32`
   - Or add the VPC CIDR: `10.0.0.0/16` (broader but still private)
5. Under **Database Access** → Create user with `readWrite` on your database.
6. Get your connection string from **Connect** → **Connect your application**.

**Connection String Format:**
```
mongodb+srv://mernAppUser:password@cluster0.xxxxx.mongodb.net/merndb?retryWrites=true&w=majority
```

---

## 8. Deploying the MERN Application

### 8.1 — Upload and Run the Backend

**Step 8.1.1 — Transfer Code to EC2 via Git**

*Note: Since our backend Security Group only allows SSH access from the Bastion Host, we cannot use SCP directly from our laptop. Instead, we will log into the backend and pull the code directly from GitHub!*

```bash
# 1. SSH into the Bastion Host from your laptop (with agent forwarding)
ssh -A ubuntu@<bastion-public-ip>

# 2. SSH from Bastion to the Backend EC2 using its Private IP
ssh ubuntu@<backend-private-ip>

# 3. Clone your repository directly into the backend
cd /var/www
git clone https://github.com/yourusername/mern-backend.git backend
cd backend
```

**Step 8.1.2 — Install Dependencies**
```bash
cd /var/www/backend
npm install --production
```

**Step 8.1.3 — Configure Environment Variables**
```bash
# Create .env file (NEVER commit this to Git)
nano /var/www/backend/.env
```

```env
PORT=5000
NODE_ENV=production
MONGODB_URI=mongodb://mernAppUser:AppPassword456!@10.0.3.xxx:27017/merndb
JWT_SECRET=your_very_long_random_secret_here
CORS_ORIGIN=http://your-frontend-domain.com
```

```bash
# Secure the .env file
chmod 600 /var/www/backend/.env
```

**Step 8.1.4 — Run Backend with PM2**
```bash
# Start the application
pm2 start server.js --name "mern-backend" --env production

# Verify it's running
pm2 status
pm2 logs mern-backend

# Auto-restart on server reboot
pm2 startup
# Copy and run the command PM2 prints
pm2 save
```

**PM2 Cheat Sheet:**

| Command | Purpose |
|---|---|
| `pm2 start app.js --name myapp` | Start app |
| `pm2 stop myapp` | Stop app |
| `pm2 restart myapp` | Restart app |
| `pm2 logs myapp` | View live logs |
| `pm2 monit` | Dashboard monitor |
| `pm2 delete myapp` | Remove from PM2 |

### 8.2 — Deploy React Frontend (Option A: Using the Frontend EC2)

If you chose to create the optional `mern-frontend` EC2 instance in Section 6.4, here is how you deploy to it using Git:

**Step 8.2.1 — Connect and Clone**
```bash
# 1. SSH into the Bastion Host from your laptop (with agent forwarding)
ssh -A ubuntu@<bastion-public-ip>

# 2. SSH from Bastion to the Frontend EC2 using its Private IP
ssh ubuntu@<frontend-private-ip>

# 3. Clone your frontend repository
cd /var/www
git clone https://github.com/yourusername/mern-frontend.git frontend
cd frontend
```

**Step 8.2.2 — Build and Serve via Nginx**
```bash
# Update API URL & Install/Build (Make sure this points to your Backend Public IP API!)
npm install
npm run build

# Because we installed NGINX in Section 6.4's user data script, 
# we just need to copy the built files to our web directory:
sudo cp -r build/* /var/www/frontend/

# 🚨 IMPORTANT: Tell Nginx to serve our frontend folder instead of the default "Welcome" page
sudo sed -i 's|root /var/www/html;|root /var/www/frontend;|g' /etc/nginx/sites-available/default

# (Optional but recommended): Fix React Router so direct links don't throw 404 errors
sudo sed -i 's|try_files $uri $uri/ =404;|try_files $uri $uri/ /index.html;|g' /etc/nginx/sites-available/default

# Reload Nginx to apply the changes
sudo systemctl restart nginx
```

### 8.3 — Deploy React Frontend (Option B: S3 + CloudFront — Recommended Free Option)

**Step 8.3.1 — Build React App Locally**
```bash
# In your local React project directory
# Update your API base URL to point to the backend EC2
# In src/config.js or .env.production:
REACT_APP_API_URL=http://<backend-public-ip>:5000

# Build the app
npm run build
# This creates a /build folder with static files
```

**Step 8.3.2 — Create an S3 Bucket for Static Hosting**
1. Open **S3** in the Console → **Create bucket**.
2. Bucket name: `mern-frontend-yourinitials-2024` (must be globally unique).
3. **Region:** us-east-1.
4. **Uncheck "Block all public access"** → confirm you understand.
5. Create bucket.

**Step 8.2.3 — Configure Static Website Hosting**
1. Click your bucket → **Properties** tab.
2. Scroll to **Static website hosting** → **Edit**.
3. Enable → Index document: `index.html` → Error document: `index.html` (for React Router).
4. Save.

**Step 8.2.4 — Add Bucket Policy for Public Read**
1. **Permissions** tab → **Bucket policy** → **Edit**.
2. Paste:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::mern-frontend-yourinitials-2024/*"
    }
  ]
}
```

3. Save.

**Step 8.2.5 — Upload Build Files**
1. Click **Objects** tab → **Upload**.
2. Upload ALL contents of your `build/` folder (not the folder itself, the contents).
3. Click **Upload**.

**Step 8.2.6 — Access Your Frontend**
- Your frontend is now live at the S3 static website endpoint shown in Properties.

**Step 8.2.7 — Add CloudFront for HTTPS and CDN (Recommended)**
1. Open **CloudFront** → **Create distribution**.
2. Origin domain: select your S3 bucket's static website endpoint.
3. **Viewer protocol policy:** Redirect HTTP to HTTPS.
4. Default root object: `index.html`
5. Create distribution (takes 10-15 minutes to deploy globally).
6. Your site is now available at `https://xxxx.cloudfront.net` with HTTPS and global CDN.

> 💰 **Free Tier:** CloudFront gives 1 TB data transfer and 10 million HTTP requests free per month.

### 8.3 — Connect Frontend to Backend

In your React app, update the API URL:
```javascript
// src/config/api.js
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';
export default API_BASE_URL;

// Usage in components
import API_BASE_URL from '../config/api';

const response = await fetch(`${API_BASE_URL}/api/users`);
```

**Configure CORS on Express Backend:**
```javascript
// In server.js or app.js
const cors = require('cors');

app.use(cors({
  origin: process.env.CORS_ORIGIN || 'http://localhost:3000',
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));
```

---

## 9. Advanced Networking — VPC Peering

### What
VPC Peering creates a private network connection between two VPCs. Traffic between them stays on AWS's private backbone — no internet involved.

### Why — Use Cases

```
Scenario: You have two VPCs:
- VPC-A (10.0.0.0/16): Your MERN app
- VPC-B (10.1.0.0/16): Your data analytics service

Without peering: Services communicate over the internet (slow, costly, insecure)
With peering: Direct private connection (fast, free, secure)
```

### VPC Peering Diagram

```
VPC-A (10.0.0.0/16)           VPC-B (10.1.0.0/16)
+-------------------+           +-------------------+
|                   |           |                   |
|  EC2 Backend      |<--------->|  Analytics EC2    |
|  10.0.1.50        |  Peering  |  10.1.1.100       |
|                   | Connection|                   |
+-------------------+           +-------------------+

Traffic: 10.0.1.50 → 10.1.1.100 (stays on AWS backbone)
```

### Important Limitations
- VPC peering is **NOT transitive**: If A peers with B, and B peers with C, A cannot reach C through B.
- CIDR ranges must NOT overlap: `10.0.0.0/16` and `10.0.0.0/16` cannot peer.

### How to Create VPC Peering

1. VPC Dashboard → **Peering connections** → **Create peering connection**.
2. Name: `mern-vpc-a-to-b`
3. **VPC ID (Requester):** Select `mern-vpc`
4. **VPC ID (Accepter):** Select the other VPC (or enter account ID + VPC ID for cross-account)
5. Click **Create peering connection**.
6. Go to **Peering connections** → select the new connection → **Actions** → **Accept request**.
7. **Update Route Tables in BOTH VPCs:**
   - In VPC-A's route table: Add route `10.1.0.0/16` → Target: Peering Connection
   - In VPC-B's route table: Add route `10.0.0.0/16` → Target: Peering Connection
8. **Update Security Groups:** Add inbound rules allowing traffic from the peer VPC's CIDR.

---

## 10. Traffic Management — ALB, Route 53, HTTPS

### Application Load Balancer (ALB)

**What:** Distributes incoming traffic across multiple EC2 instances, performs health checks, and routes based on URL path/hostname.

**Why:** If your backend EC2 crashes, the ALB detects the unhealthy instance and routes traffic to healthy ones. Enables zero-downtime deployments.

```
Internet
    |
    v
[ALB — Public Subnets — both AZs]
    |         |
    v         v
[EC2 B1]  [EC2 B2]   <-- Backend Target Group
```

> 💰 **Cost Alert:** ALB is NOT Free Tier eligible.
> - ~$0.008/LCU-hour + $0.016/hour for the ALB itself.
> - ~$14-20/month minimum.
> - For Free Tier learning: skip ALB and directly access EC2 via Elastic IP.

**Creating an ALB (when ready to pay):**
1. EC2 Dashboard → **Load Balancers** → **Create load balancer** → **Application Load Balancer**.
2. Name: `mern-alb`
3. Scheme: Internet-facing
4. VPC: `mern-vpc`
5. Subnets: Select BOTH public subnets (multi-AZ is required).
6. Security group: Create new SG allowing HTTP (80) and HTTPS (443) from `0.0.0.0/0`.
7. **Listeners:** HTTP:80 → Create target group.
8. **Target group:**
   - Type: Instances
   - Protocol: HTTP | Port: 5000 (your Node.js port)
   - Health check path: `/api/health` (create this endpoint in Express)
   - Register your backend EC2 instances.
9. Create ALB.

**Health Check Endpoint in Express:**
```javascript
app.get('/api/health', (req, res) => {
  res.status(200).json({ status: 'healthy', timestamp: new Date().toISOString() });
});
```

### Route 53 — Domain Setup

**What:** AWS's DNS service. Maps your domain name (e.g., `myapp.com`) to your server's IP.

**Free Tier:** Route 53 hosted zone costs **$0.50/month** (not free, but very cheap).

**Basic Setup:**
1. Open **Route 53** → **Hosted zones** → **Create hosted zone**.
2. Domain name: `yourapp.com`
3. Type: Public hosted zone.
4. Create.
5. You'll get 4 Name Server (NS) records — update these at your domain registrar.
6. Create an **A record:**
   - Name: `api.yourapp.com`
   - Type: A
   - Value: Your backend EC2 Elastic IP (or ALB DNS name as an Alias record)

### HTTPS with SSL/TLS

**Conceptual Flow:**
```
User → HTTPS request → ALB → SSL termination at ALB → HTTP to backend EC2
```

**AWS Certificate Manager (ACM) — Free SSL:**
1. Open **ACM** → **Request a certificate** → **Public certificate**.
2. Enter your domain: `yourapp.com` and `*.yourapp.com` (wildcard).
3. Validation method: DNS validation (ACM will give you CNAME records to add to Route 53).
4. AWS auto-adds these records if you use Route 53 → certificate is issued in minutes.
5. In ALB, add an HTTPS:443 listener using this ACM certificate.

> ACM certificates are **free** when used with ALB or CloudFront.

---

## 11. Monitoring & Logging — CloudWatch

### Free Tier Limits for CloudWatch

| Resource | Free Tier Limit |
|---|---|
| Metrics | 10 custom metrics + all basic EC2 metrics |
| Logs | 5 GB ingestion + 5 GB storage |
| Alarms | 10 alarms |
| Dashboards | 3 dashboards |

### 11.1 — Enable Detailed EC2 Monitoring

By default, EC2 sends metrics every 5 minutes (basic monitoring, free).
Detailed monitoring (1-minute intervals) costs $0.30/metric/month.

1. EC2 → Select your instance → **Actions** → **Monitor and troubleshoot** → **Manage detailed monitoring**.
2. For Free Tier: keep **basic monitoring** (every 5 minutes).

### 11.2 — Key EC2 Metrics to Watch

| Metric | Normal Range | Alert Threshold |
|---|---|---|
| CPUUtilization | < 80% | > 90% for 5 min |
| NetworkIn/Out | Varies | Sudden spike |
| StatusCheckFailed | 0 | > 0 |
| EBSReadOps/WriteOps | Varies | Very high sustained |

### 11.3 — Create a CloudWatch Alarm

1. CloudWatch → **Alarms** → **Create alarm**.
2. **Select metric** → EC2 → Per-Instance Metrics → `CPUUtilization` for your instance.
3. Period: 5 minutes | Statistic: Average.
4. Threshold: Greater than `80`.
5. **Actions:** Select or create an SNS topic → enter your email.
6. Alarm name: `mern-backend-high-cpu`
7. Create alarm.

### 11.4 — View PM2 Logs via CloudWatch

Install the CloudWatch agent on your EC2 to stream PM2 logs:
```bash
# Install CloudWatch agent
sudo yum install -y amazon-cloudwatch-agent

# Configure (simplified)
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-config-wizard
```

Or simply view logs directly on the instance:
```bash
# PM2 logs
pm2 logs mern-backend --lines 100

# System logs
sudo journalctl -u mongod -f

# Nginx access logs
sudo tail -f /var/log/nginx/access.log
```

### 11.5 — Debugging: Frontend Cannot Reach Backend

**Step-by-step debug checklist:**
```
1. Is the backend running?
   → ssh into backend EC2 → pm2 status → should show "online"

2. Is the correct port open?
   → curl http://localhost:5000/api/health (from backend EC2)
   → should return {"status":"healthy"}

3. Is Security Group allowing traffic?
   → Check mern-backend-sg inbound rules for port 5000

4. Is the API URL correct in the frontend?
   → Check REACT_APP_API_URL in React build
   → Check browser Network tab for the actual request URL

5. Is CORS configured?
   → Check browser Console for CORS errors
   → Check Express cors() middleware configuration

6. Is there a firewall on EC2?
   → sudo iptables -L (check for blocking rules)
```

---

## 12. Cost Optimization (Mandatory)

### Free Tier Limits — Complete Reference Table

| Service | Free Tier Offer | Duration | Watch Out For |
|---|---|---|---|
| EC2 t2.micro | 750 hours/month | 12 months | Running 2+ instances simultaneously |
| EBS Storage | 30 GB (gp2/gp3) | 12 months | Snapshots cost extra |
| S3 | 5 GB + 20K GET reqs | 12 months | Data transfer OUT costs |
| CloudFront | 1 TB transfer + 10M requests | 12 months | After 12 months, charges apply |
| RDS | 750 hours db.t2.micro + 20 GB | 12 months | Multi-AZ doubles cost |
| CloudWatch | 10 metrics, 5 GB logs | Always free | Detailed monitoring not free |
| Route 53 | — | Not free | $0.50/hosted zone/month |
| NAT Gateway | — | Not free | $0.045/hour + data |
| ALB | — | Not free | ~$16-20/month minimum |
| Elastic IP | 1 attached to running instance | Always free | Unattached EIPs charged |
| Data Transfer IN | Unlimited | Always free | |
| Data Transfer OUT | 100 GB/month | Always free (first year) | Exceeding = $0.09/GB |

### Common Mistakes That Cause Unexpected Charges

1. **Leaving Elastic IPs unattached** — Stop your instance to save hours, but the Elastic IP keeps charging if not released.
2. **Creating NAT Gateways and forgetting** — Charges accumulate hourly even with zero traffic.
3. **Keeping snapshots** — EBS snapshots count against your 30 GB free storage.
4. **Using t3.micro instead of t2.micro** — In some regions, t3.micro is not Free Tier eligible.
5. **Running multiple instances** — Two t2.micro instances running 24/7 = 1,488 hours (exceeds 750 free hours).
6. **Accidentally launching in wrong region** — Resources in non-primary regions may use different pricing.
7. **S3 data transfer OUT** — Reading from S3 to the internet costs after 100 GB.

### How to Shut Down Resources Properly

**To avoid ALL charges (for a break from learning):**
```
Order of operations:
1. Stop (not terminate) EC2 instances → saves state, loses public IP
2. Release any unattached Elastic IPs
3. Delete NAT Gateway (if created) → Release its Elastic IP too
4. Empty and delete S3 buckets (if not needed)
5. Delete CloudFront distributions (if not needed)
```

**Stop vs Terminate:**
- **Stop:** Instance pauses. EBS data preserved. No EC2 hourly charge. EBS storage still charged.
- **Terminate:** Instance and EBS deleted permanently. No charges at all.

### Set Up Budget Alerts

1. In the top-right menu → **Account** → search **Billing and Cost Management**.
2. Click **Budgets** → **Create budget**.
3. Use **Cost budget** template.
4. Budget amount: `$5` per month.
5. Alert: Send email when **actual cost** exceeds 80% of budget.
6. This gives you early warning before you hit the limit.

---

## 13. Industry Best Practices

### Architecture Comparison: Development vs Production

```
DEVELOPMENT (Free Tier Learning):
+------------------------------------------+
| Single EC2 t2.micro (backend + maybe db) |
| Single public subnet                      |
| No load balancer                          |
| Direct SSH access                         |
| MongoDB on same instance                  |
+------------------------------------------+

PRODUCTION (Industry Standard):
+------------------------------------------+
| Multi-AZ deployment                       |
| Public + Private subnets                  |
| ALB with health checks                    |
| MongoDB replica set (3 nodes)             |
| Bastion host for SSH                      |
| WAF for web application firewall          |
| Secrets Manager for credentials           |
| Auto Scaling Group for EC2                |
| CloudFront + S3 for frontend              |
| VPC Flow Logs for audit                   |
| AWS Backup for automated backups          |
+------------------------------------------+
```

### Security Hardening Checklist

- [ ] MFA enabled on all IAM users (especially root)
- [ ] No SSH from `0.0.0.0/0` — restrict to Bastion or specific IPs
- [ ] MongoDB only accessible from backend SG (not public internet)
- [ ] Environment variables stored in AWS Secrets Manager (not `.env` files in production)
- [ ] S3 buckets NOT publicly accessible unless intentional
- [ ] CloudTrail enabled for audit logging (Free Tier: 1 trail free)
- [ ] VPC Flow Logs enabled for network troubleshooting
- [ ] Regular key pair rotation

### Using AWS Secrets Manager for Credentials

Instead of `.env` files on EC2, production apps retrieve secrets programmatically:

```javascript
// In Node.js backend (production)
const { SecretsManagerClient, GetSecretValueCommand } = require('@aws-sdk/client-secrets-manager');

const client = new SecretsManagerClient({ region: 'us-east-1' });

async function getMongoUri() {
  const response = await client.send(new GetSecretValueCommand({
    SecretId: 'mern/prod/mongodb-uri'
  }));
  return response.SecretString;
}
```

> Secrets Manager costs $0.40/secret/month. An alternative (free) is **AWS Systems Manager Parameter Store** (standard parameters are free).

### Scalability Considerations

**Vertical Scaling:** Upgrade instance type (t2.micro → t3.medium). Simple but requires downtime.

**Horizontal Scaling:** Add more instances behind a Load Balancer. Requires stateless app design (sessions in Redis, not in-memory).

**Auto Scaling Group (ASG):**
- Automatically launch new EC2s when CPU exceeds threshold
- Automatically terminate excess EC2s when load drops
- Works with ALB to register/deregister targets

---

## 14. Scenario-Based Interview Q&A

---

**Q1: What happens if a NAT Gateway fails?**

**A:** Instances in private subnets lose outbound internet access. They cannot download packages, connect to external APIs, or reach MongoDB Atlas. Inbound traffic from the internet is not affected (it uses the Internet Gateway). Resolution: Create a new NAT Gateway or failover. Best practice: Deploy NAT Gateways in multiple AZs and have each AZ's private route table point to its own NAT Gateway. This prevents a single NAT failure from affecting all private subnets.

---

**Q2: How will you secure MongoDB in a private subnet?**

**A:** Multiple layers:
1. **Private subnet:** MongoDB EC2 has no public IP.
2. **Security Group:** Only allows port 27017 from the backend Security Group ID — not even other private IPs can connect unless they're in the backend SG.
3. **MongoDB authentication:** Enabled with strong passwords.
4. **bindIp restriction:** MongoDB only listens on its private IP and localhost, not `0.0.0.0`.
5. **Bastion Host:** Only SSH entry point — no direct SSH to MongoDB from the internet.
6. **Encryption at rest:** Enable EBS encryption for the MongoDB volume.
7. **Encryption in transit:** Use MongoDB TLS/SSL configuration.

---

**Q3: How do you debug if the frontend cannot reach the backend?**

**A:** Systematic approach:
1. Check if the backend process is running: `pm2 status`
2. Test locally on the backend EC2: `curl http://localhost:5000/api/health`
3. Check Security Group inbound rules for port 5000
4. Check the API URL in the React build (check browser Network tab)
5. Check for CORS errors in browser developer console
6. Verify CORS configuration in Express matches the frontend origin
7. Check if EC2 instance is in a running state and has its Elastic IP
8. Test from another machine: `curl http://<backend-ip>:5000/api/health`
9. Check PM2 logs: `pm2 logs mern-backend`

---

**Q4: How do you allow only your IP to SSH?**

**A:**
1. Find your public IP: visit `https://whatismyip.com`
2. Go to EC2 → Security Groups → `mern-bastion-sg` → Edit inbound rules.
3. For SSH rule (port 22): change Source from `0.0.0.0/0` to `YOUR-IP/32` (the `/32` means exactly that one IP).
4. For dynamic IPs (home internet): automate this with a script that updates the SG rule whenever your IP changes, or use AWS VPN/Client VPN for stable access.

---

**Q5: What is the difference between a Security Group and a NACL?**

**A:**

| Aspect | Security Group | NACL |
|---|---|---|
| Level | Instance (ENI) | Subnet |
| State | Stateful | Stateless |
| Rules | Allow only | Allow and Deny |
| Evaluation | All rules evaluated | Rules in order, first match wins |
| Return traffic | Auto-allowed | Must be explicitly allowed |
| Use case | Instance-level access control | Subnet-level, blocking bad IPs |

**Practical example:** You want to block IP `1.2.3.4` from accessing your entire public subnet. You cannot use a Security Group for this (no Deny rules). Use a NACL with rule `50: DENY ALL from 1.2.3.4/32`, placed before your ALLOW rules.

---

**Q6: Your MongoDB EC2 in the private subnet cannot download packages. What do you do?**

**A:** It needs outbound internet access. Options:
1. **Add a NAT Gateway** (paid): Place NAT in public subnet, add `0.0.0.0/0` route in private route table pointing to NAT Gateway.
2. **Use a NAT Instance** (free): A t2.micro EC2 with IP forwarding enabled acts as NAT.
3. **Use a Bastion as a proxy**: SSH in and use it to transfer packages manually.
4. **Use S3 VPC Endpoint** (free): If only AWS service access is needed, VPC endpoints allow private subnet resources to access S3 without internet.

---

**Q7: What happens if you terminate your EC2 instance instead of stopping it?**

**A:** All data on instance store volumes is permanently lost. EBS volumes may or may not be deleted depending on the "Delete on termination" setting (default: yes for root volume). You cannot recover a terminated instance — there is no "undo." The instance ID is gone forever. Always prefer Stop over Terminate unless you truly want to delete the instance and have backups of your data.

---

**Q8: How would you implement zero-downtime deployment for your Node.js backend?**

**A:**
1. Use an ALB with a Target Group.
2. Launch a NEW EC2 instance with the updated code.
3. Register the new instance with the Target Group.
4. Wait for health checks to pass on the new instance.
5. Deregister the OLD instance from the Target Group (ALB stops sending it new traffic).
6. Wait for in-flight requests to complete (connection draining — default 300 seconds).
7. Terminate the old instance.
This is a "blue-green" deployment pattern. PM2 also supports zero-downtime reload: `pm2 reload mern-backend`

---

**Q9: Your EC2 ran out of disk space. What do you do without data loss?**

**A:**
1. **SSH into the instance** and verify: `df -h`
2. **Modify the EBS volume** (no downtime needed): EC2 → Volumes → select volume → Actions → Modify Volume → increase size.
3. **Extend the partition and filesystem** (while instance is running):
```bash
sudo growpart /dev/xvda 1
sudo resize2fs /dev/xvda1  # for ext4
# OR
sudo xfs_growfs /  # for xfs (Amazon Linux 2023 default)
```
4. Verify with `df -h` again. No restart needed.

---

**Q10: How do you make your MERN app highly available?**

**A:**
1. **Frontend:** S3 + CloudFront (inherently highly available — no single point of failure).
2. **Backend:** 2+ EC2 instances in different AZs behind an ALB with health checks.
3. **Database:** MongoDB replica set (3 nodes across 3 AZs) OR MongoDB Atlas (built-in HA).
4. **Networking:** NAT Gateways in each AZ (not just one).
5. **Auto Scaling:** ASG to replace failed instances automatically.
This ensures that even if an entire AZ fails, the app continues serving traffic from the other AZ.

---

**Q11: When should you use a private subnet vs a public subnet?**

**A:**

| Resource | Subnet Type | Reason |
|---|---|---|
| Web Server (Nginx, React) | Public | Must be directly reachable from internet |
| Load Balancer | Public | Entry point from internet |
| Bastion Host | Public | Needs SSH from internet |
| Node.js API (behind ALB) | Private | Only ALB needs to reach it |
| MongoDB / any database | Private | Never directly internet-accessible |
| Redis cache | Private | Internal use only |
| Internal microservices | Private | No public access needed |

**Rule of thumb:** If a resource needs to RECEIVE connections from the internet, use a public subnet. Everything else goes private.

---

**Q12: How do you handle session management when you have multiple backend instances behind an ALB?**

**A:** Never store sessions in Node.js memory (in-process). With multiple instances, user A might authenticate on instance 1, but their next request goes to instance 2 — which has no session record.
Solution: **External session store.**
- **Redis (ElastiCache):** Most common production solution. Store sessions in Redis; all EC2 instances share the same session store.
- **JWT (stateless):** No session storage needed — the token itself carries user info. Preferred for APIs.
- **Sticky sessions on ALB:** Force ALB to route a user to the same instance (not recommended — defeats horizontal scaling).

---

**Q13: What is VPC Peering, and when would you use it?**

**A:** VPC Peering creates a direct, private network link between two VPCs. Traffic never leaves AWS's network. Use cases:
1. **Microservices across VPCs:** Service A in VPC-1 needs to call Service B in VPC-2.
2. **Cross-account access:** Your app VPC (account A) accessing a shared data lake VPC (account B).
3. **Dev/prod separation:** Dev team's VPC needs read access to production database VPC.

Limitations: Not transitive (A↔B and B↔C does not mean A↔C), CIDR ranges cannot overlap, maximum 125 peering connections per VPC.

Alternative for complex mesh networking: **AWS Transit Gateway** (paid service that acts as a hub for many VPCs).

---

**Q14: How would you block a specific country from accessing your application?**

**A:**
1. **AWS WAF (Web Application Firewall):** Create a geographic match condition → block requests from specific countries. WAF attaches to CloudFront or ALB.
2. **CloudFront geographic restriction:** If using CloudFront, enable built-in geo-restriction under the distribution → block specific countries.
3. NACLs alone are not practical for country blocking (would require blocking thousands of IP ranges manually).

WAF costs: ~$5/month for a web ACL + $1 per million requests.

---

**Q15: Your application is under a DDoS attack. What AWS services protect you?**

**A:**
1. **AWS Shield Standard** — Free, automatically protects all AWS resources against common layer 3/4 (network/transport) DDoS attacks like SYN floods and UDP reflection attacks.
2. **AWS Shield Advanced** — Paid ($3,000/month), for layer 7 (application) DDoS protection with 24/7 DDoS response team access.
3. **AWS WAF** — Block specific attack patterns (SQL injection, XSS, rate limiting per IP).
4. **CloudFront** — Absorbs volumetric attacks by distributing traffic globally across AWS's massive network.
5. **ALB with WAF** — Rate-limit requests per IP at the application layer.

For Free Tier learning: Shield Standard is automatically active. Pair with CloudFront to benefit from DDoS absorption.

---

## Appendix: Full Architecture Summary

```
FINAL MERN ARCHITECTURE (Free Tier Optimized):

Internet
    |
    v
[CloudFront Distribution]
    |              |
    v              v
[S3 Static]   [EC2 Backend t2.micro]
[React Build]  [Node.js + Express]  <-- Public Subnet 1a
                    |
                    | (private, port 27017, Security Group only)
                    v
              [EC2 MongoDB t2.micro]
              [Private Subnet 1a]
                    ^
                    |
              [Bastion t2.micro]
              [Public Subnet 1b]
                    ^
                    |
              [Your Laptop — SSH]

Supporting services:
- IAM: mern-admin user with MFA
- CloudWatch: CPU/status alarms, PM2 log streaming
- Billing: Budget alert at $5/month
- S3: React build static files
- CloudFront: HTTPS, global CDN, DDoS absorption (Shield Standard)

Security layers for MongoDB:
1. Private subnet (no public IP)
2. Security Group (port 27017 only from backend SG)
3. NACL (subnet-level, block bad IPs)
4. MongoDB auth (username/password)
5. bindIp (listen only on private IP)
6. EBS encryption (data at rest)
```

---

*This guide is designed for AWS Free Tier. Always monitor your Billing Dashboard and set budget alerts. Happy building! 🚀*