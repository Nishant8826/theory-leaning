# VPC Networking – NACL, CIDR, VPC Peering & Transit Gateway

---

## 1. Network ACL (NACL)

### 🔷 What is it?
A **Network Access Control List (NACL)** is a security layer that works at the **subnet level** inside a VPC. It controls what traffic is allowed **in and out** of an entire subnet.

### 🔷 Why does it exist?
Security Groups protect individual EC2 instances — but what if 10 servers in a subnet are all being attacked by the same malicious IP? You'd have to update 10 Security Groups. NACL lets you **block it once at the subnet level**.

### 🔷 How does it work?
1. You create a NACL and associate it with a subnet.
2. You define **inbound rules** (traffic coming in) and **outbound rules** (traffic going out).
3. Each rule has a **rule number** — lower number = higher priority.
4. Rules are evaluated **top to bottom** — first match wins.
5. There is always a default **DENY ALL** rule at the bottom (rule *).

```
Inbound Rules Example:
┌─────────┬────────────┬──────────┬───────────┐
│ Rule #  │ Source IP  │ Protocol │ Action    │
├─────────┼────────────┼──────────┼───────────┤
│  100    │ 99.33.36.0 │  ALL     │  DENY     │
│  200    │ 0.0.0.0/0  │  HTTP    │  ALLOW    │
│  *      │ 0.0.0.0/0  │  ALL     │  DENY     │
└─────────┴────────────┴──────────┴───────────┘
Rule 100 is checked first → blocks 99.33.36.x before rule 200 even runs.
```

### 🔷 Impact

| With NACL | Without NACL |
|---|---|
| Block malicious IPs at subnet level in one rule | Have to update every Security Group on every instance |
| Stateless — must define both inbound AND outbound rules | Security Groups are stateful (return traffic is auto-allowed) |
| Protects entire subnet | Only instance-level protection available |

---

### 🔁 NACL vs Security Group — Quick Comparison

```
┌────────────────────┬──────────────────────┬──────────────────────┐
│ Feature            │ NACL                 │ Security Group       │
├────────────────────┼──────────────────────┼──────────────────────┤
│ Level              │ Subnet               │ Instance (EC2)       │
│ Stateful?          │ No (stateless)       │ Yes (stateful)       │
│ Rules              │ Allow + Deny         │ Allow only           │
│ Rule Priority      │ Rule numbers         │ All rules evaluated  │
│ Default behavior   │ Deny all (*)         │ Deny all implicitly  │
└────────────────────┴──────────────────────┴──────────────────────┘
```

---

## 2. CIDR Calculations

### 🔷 What is it?
**CIDR (Classless Inter-Domain Routing)** is a way to define a range of IP addresses using a notation like `10.0.0.0/16`. The number after `/` tells how many bits are **fixed** (network part) — the rest are available for hosts.

### 🔷 Why does it exist?
To efficiently allocate IP address space — you get exactly as many IPs as you need, no more, no less.

### 🔷 How does it work?

**Formula:**
```
Total IPs = 2^(32 - CIDR value)
```

| CIDR | Total IPs | Usable IPs | Typical Use |
|---|---|---|---|
| /16 | 65,536 | 65,531 | Entire VPC |
| /24 | 256 | 251 | One Subnet |
| /32 | 1 | 1 | Single Host |

### 🔷 AWS Reserved IPs (for every subnet)
AWS always reserves **5 IPs** from each subnet:

```
For 10.0.0.0/24:
┌────────────┬───────────────────────────────┐
│ 10.0.0.0   │ Network address               │
│ 10.0.0.1   │ AWS VPC Router                │
│ 10.0.0.2   │ AWS DNS Server                │
│ 10.0.0.3   │ Reserved for future use       │
│ 10.0.0.255 │ Broadcast address             │
└────────────┴───────────────────────────────┘
Usable: 256 - 5 = 251 IPs
```

---

## 3. VPC Peering

### 🔷 What is it?
**VPC Peering** is a private network connection between **two VPCs** that lets them communicate using private IP addresses — without going over the public internet.

### 🔷 Why does it exist?
Sometimes two separate VPCs (maybe owned by different teams or accounts) need to talk to each other privately and securely. VPC Peering creates a **direct private tunnel** between them.

### 🔷 How does it work?

```
Step 1: VPC-A owner sends a Peering Request to VPC-B
Step 2: VPC-B owner accepts the request
Step 3: Both sides update their Route Tables to route traffic to each other
Step 4: Private communication is now possible
```

```
Architecture:

  Account A                    Account B
┌──────────┐                ┌──────────┐
│  VPC-A   │◄──── Peering ──►│  VPC-B   │
│10.0.0.0  │   Connection   │10.1.0.0  │
│  /16     │                │  /16     │
└──────────┘                └──────────┘
        Private IPs only, no internet
```

### 🔷 Key Rules of VPC Peering

**1. No Transitive Peering**
```
A ──peered──► B ──peered──► C

❌ A CANNOT talk to C through B
✅ A must create a SEPARATE peering with C
```

**2. No Overlapping IP Ranges**
```
VPC-A: 10.0.0.0/16  ──► ✅ Can peer
VPC-B: 10.1.0.0/16

VPC-A: 10.0.0.0/16  ──► ❌ Cannot peer (IPs overlap)
VPC-B: 10.0.0.0/16
```

**3. One-Way Request, Two-Way Setup**
- The connection itself is bidirectional once accepted
- But route tables on **both sides** must be configured

### 🔷 Impact

| With VPC Peering | Without VPC Peering |
|---|---|
| Private, secure communication between VPCs | Must go over public internet (less secure) |
| No data transfer cost for same-region | Exposes internal services publicly |
| Works cross-account and cross-region | Need VPNs or complex setups |

---

## 4. Transit Gateway

### 🔷 What is it?
A **Transit Gateway** is a central hub that connects **multiple VPCs** (and on-premises networks) together. Instead of creating peering between every pair of VPCs, everything connects to one central gateway.

### 🔷 Why does it exist?
VPC Peering works fine for 2–3 VPCs. But imagine 10 VPCs — you'd need up to **45 peering connections**. Transit Gateway solves this with a **hub-and-spoke model**.

### 🔷 How does it work?

```
Without Transit Gateway (Peering Mesh):

VPC-A ──── VPC-B
  │    ✕     │
VPC-C ──── VPC-D
(Many connections, hard to manage)

With Transit Gateway:

     VPC-A
       │
VPC-D──TGW──VPC-B
       │
     VPC-C
(One hub, everything connects here)
```

### 🔷 Impact

| Transit Gateway | VPC Peering (at scale) |
|---|---|
| One connection per VPC | N*(N-1)/2 connections needed |
| Supports transitive routing | No transitive routing |
| Centrally managed | Distributed, hard to manage |
| Slight added cost | Lower cost for small setups |

---

## 5. Scenario-Based Q&A

🔍 **Scenario 1:** Your company's app runs across 3 subnets. A hacker's IP `99.33.36.5` is flooding all your servers with requests. You want to block it immediately.

✅ **Answer:** Create a NACL rule with a low rule number (e.g., 100) that **DENY**s all traffic from `99.33.36.0/24`. Associate it with all 3 subnets. One rule blocks the attacker across all servers instantly — no need to touch individual Security Groups.

---

🔍 **Scenario 2:** An OTT platform (like Hotstar) wants to privately connect with 3 content provider VPCs to stream content without exposing anything to the internet.

✅ **Answer:** Set up **VPC Peering** between the OTT platform's VPC and each content provider's VPC. Ensure IP ranges don't overlap. Update route tables on both ends. Now all communication stays private.

---

🔍 **Scenario 3:** Your company has 8 VPCs across different teams. Managing peering between all of them is becoming a nightmare.

✅ **Answer:** Set up a **Transit Gateway**. Each VPC connects once to the TGW. All inter-VPC routing is handled centrally — much simpler to manage and scale.

---

🔍 **Scenario 4:** You tried to peer VPC "Mohit1" (`10.0.0.0/16`) with VPC "Mohit2" (`10.0.0.0/16`) but peering failed.

✅ **Answer:** Both VPCs have **overlapping CIDR ranges**. VPC Peering requires non-overlapping IP ranges. You'd need to recreate one VPC with a different CIDR (e.g., `10.1.0.0/16`) before peering.

---

🔍 **Scenario 5:** VPC-A is peered with VPC-B, and VPC-B is peered with VPC-C. A developer assumes VPC-A can reach VPC-C. Is he right?

✅ **Answer:** No. VPC Peering does **not support transitive routing**. VPC-A cannot reach VPC-C through VPC-B. A direct peering between VPC-A and VPC-C must be created, or use a **Transit Gateway**.

---

## 6. Interview Q&A

**Q1. What is the difference between a Security Group and a NACL?**

> Security Groups operate at the **instance level** and are **stateful** (return traffic is automatically allowed). NACLs operate at the **subnet level** and are **stateless** (you must explicitly allow both inbound and outbound traffic). NACLs also support DENY rules; Security Groups only support ALLOW rules.

---

**Q2. What does "stateless" mean in the context of NACLs?**

> It means the NACL doesn't remember previous connections. If you allow inbound HTTP traffic on port 80, you must also explicitly create an outbound rule to allow the response traffic back. Security Groups handle this automatically (stateful).

---

**Q3. Can VPC Peering work across different AWS accounts and regions?**

> Yes. VPC Peering supports **cross-account** and **cross-region** connections. The requesting account sends a peering request, and the accepting account must approve it. Both sides then need to update their route tables.

---

**Q4. What is transitive peering, and why doesn't VPC Peering support it?**

> Transitive peering would mean: if A is peered with B, and B is peered with C, then A can reach C through B. AWS does **not** allow this for security and architectural reasons. Each peering connection is isolated. Use **Transit Gateway** if transitive routing is needed.

---

**Q5. How many usable IPs are in a /24 subnet in AWS?**

> Total IPs = 2^(32-24) = 256. AWS reserves 5 IPs (network, router, DNS, reserved, broadcast). So **251 usable IPs**.

---

**Q6. What happens if two VPCs with overlapping CIDR ranges try to peer?**

> The peering connection will **fail**. AWS requires non-overlapping IP address ranges between peered VPCs so it can route traffic unambiguously.

---

**Q7. When would you choose Transit Gateway over VPC Peering?**

> When you have **many VPCs** (typically more than 3–4) that need to communicate. VPC Peering requires a connection between every pair — for N VPCs, that's N*(N-1)/2 connections. Transit Gateway uses a hub-and-spoke model, so each VPC needs only **one connection** to the gateway.

---

**Q8. What is the significance of rule numbers in a NACL?**

> Rule numbers define **priority**. Rules are evaluated in ascending order — the **lowest rule number is evaluated first**. The first matching rule is applied and evaluation stops. The default rule `*` (DENY ALL) is always last.

---

**Q9. You need to block a specific IP range from accessing your subnet. Which AWS service do you use and how?**

> Use a **NACL**. Add an inbound rule with a low rule number, set the source to the malicious IP/CIDR, and set the action to **DENY**. Associate the NACL with the target subnet.

---

**Q10. Can you peer two VPCs that belong to the same account?**

> Yes. VPC Peering works within the **same account**, across accounts, and across regions. The process is the same — send request, accept, update route tables.

---

**Q11. I ran `ipconfig` on my laptop and got `192.168.1.6`. Can I block this IP in an AWS NACL to stop my laptop from accessing AWS?**

> **No.** `192.168.x.x` is a **Private IP** assigned by your local WiFi router. It only exists inside your house/office network. When you connect to the internet, your home router uses NAT (Network Address Translation) to convert your private IP into a single **Public IP**. AWS only ever sees your Public IP. To block your laptop, you must search "What is my IP" on Google to find your true Public IP (e.g., `103.55.x.x`) and block *that* in the NACL.

---

## 7. 🧪 Hands-On Practicals — Real Industry Scenarios

> These practicals are based on **real industry problems and client requirements**.
> Each practical follows: **What → Why → How (Pre-requisites + Steps) → Impact**

### Practicals Table of Contents

| # | Practical | Concept |
|---|-----------|---------|
| 1 | Block a Malicious IP Range Attacking Production Subnets | NACL |
| 2 | Allow Only HTTPS Traffic to a Public Subnet via NACL | NACL |
| 3 | NACL Stateless Behavior — Troubleshoot a Broken Web App | NACL |
| 4 | NACL + Security Group Layered Defense | NACL + SG |
| 5 | Plan a VPC CIDR for a Multi-Tier Application | CIDR |
| 6 | Subnet Sizing — Calculate IPs for a Client's Infrastructure | CIDR |
| 7 | Avoid CIDR Overlap Before Peering — Planning Phase | CIDR + VPC Peering |
| 8 | Connect Two Team VPCs via VPC Peering (Same Account) | VPC Peering |
| 9 | Cross-Account VPC Peering for a Client Merger | VPC Peering |
| 10 | Prove That Transitive Peering Does NOT Work | VPC Peering |
| 11 | Replace a Peering Mesh with Transit Gateway | Transit Gateway |
| 12 | Hub-and-Spoke: Shared Services VPC via Transit Gateway | Transit Gateway |
| 13 | Full Scenario: Secure Multi-VPC Architecture for a FinTech Client | All Concepts |

---

### Practical 1: Block a Malicious IP Range Attacking Production Subnets

#### 🎯 What
Create a NACL rule to immediately block an IP range (`203.0.113.0/24`) that is flooding your production subnets with brute-force SSH and HTTP requests.

#### 🎯 Why (Industry Problem)
**Client Scenario:** A FinTech company's payment gateway servers (spread across 3 subnets) are under a distributed attack from IP range `203.0.113.0/24`. The SOC team has identified the source. Updating Security Groups on 15+ EC2 instances one-by-one is too slow — the attack is ongoing. They need an **instant subnet-level block**.

#### 🎯 Pre-requisites
- An existing VPC with at least 2 subnets (e.g., both public for easy testing).
- **Setup 3 EC2 Instances (Ubuntu)**:
  - **Target Instance 1**: Subnet A, install a basic web server.
  - **Target Instance 2**: Subnet B, install a basic web server.
  - **Attacker Instance**: Any subnet, will act as the malicious IP.
  *(To install a web server easily, add this to User Data when launching Target 1 & 2: `#!/bin/bash` then `apt update -y && apt install nginx -y` and `systemctl start nginx`)*
- Security Groups for Target 1 & 2 must allow **HTTP (80)** and **SSH (22)** from `0.0.0.0/0`.
- Note down the **Private IP or Public IP** of the "Attacker" instance (we will use this exact IP to block it).
- AWS Console access with VPC permissions.

#### 🎯 How (Step-by-Step)

**Step 0: Setup Environment (Completing Pre-requisites)**
```
1. Setup a VPC Manually (or use your Default VPC):
   - Go to AWS Console → VPC → Create VPC. Select "VPC only" (CIDR: 10.0.0.0/16).
   - Subnets → Create 2 Subnets in your VPC (e.g., 10.0.1.0/24 and 10.0.2.0/24).
   - Internet Gateways → Create an IGW and attach it to your VPC.
   - Route Tables → Edit the route table associated with your subnets. Add a route: `0.0.0.0/0` pointing to your IGW.
2. Go to EC2 → Launch Instances.
3. Launch Target 1 & Target 2:
   - Name: Target-1 (and later Target-2)
   - OS: Ubuntu (e.g., 24.04 LTS)
   - Network: Select your newly created VPC. Pick Subnet A (for Target 1) and Subnet B (for Target 2).
   - Auto-assign Public IP: Enable
   - Security Group: Create one allowing SSH (22) and HTTP (80) from Anywhere (0.0.0.0/0), and select it for both Target 1 and Target 2.
   - Advanced Details → User Data: Paste the script:
     #!/bin/bash
     apt update -y
     apt install nginx -y
     systemctl start nginx
     systemctl enable nginx
   - Launch!
4. Launch Attacker Instance:
   - Name: Attacker-Node
   - Setup exactly like above, but you can skip the User Data (no web server needed).
   - Once running, go to Instances → select Attacker-Node → Copy its Public IP (e.g., 54.12.34.56).
```

**Step 1: Identify the Default NACL (Just Observe)**
```
1. AWS Console → VPC → Network ACLs.
2. Find the NACL associated with your newly created VPC.
3. Click on the "Inbound Rules" and "Outbound Rules" tabs at the bottom.
Note: You will see it ALLOWS ALL traffic by default. We will NOT edit this default NACL. Best practice is to leave the default alone and create a custom one!
```

**Step 2: Create a Custom NACL**
```
1. Still in Network ACLs → Click the "Create network ACL" button.
2. Name: prod-block-nacl
3. VPC: Select your new VPC.
4. Click Create.
```

**Step 3: Add the DENY Rule for the Attacker IP Range (Inbound)**
```
Select prod-block-nacl → Inbound Rules → Edit
  Rule #: 50
  Type: All Traffic
  Source: <Your-Attacker-Instance-IP>/32    <-- Replace with the exact IP of the Attacker Server
  Action: DENY

  Rule #: 100
  Type: HTTP (80)
  Source: 0.0.0.0/0
  Action: ALLOW

  Rule #: 110
  Type: HTTPS (443)
  Source: 0.0.0.0/0
  Action: ALLOW

  Rule #: 120
  Type: SSH (22)
  Source: 0.0.0.0/0    <-- (Or use your Local Laptop IP /32 if you want strict security)
  Action: ALLOW
```

**Step 4: Add Outbound Rules (NACL is Stateless!)**
```
Outbound Rules → Edit
  Rule #: 100
  Type: Custom TCP
  Port Range: 1024-65535 (ephemeral ports for response traffic)
  Destination: 0.0.0.0/0
  Action: ALLOW
```

**Step 5: Associate the NACL with Target Subnets**
```
Subnet Associations tab → Edit → Select both Subnet A and Subnet B → Save
```

**Step 6: Verify the Block**
```bash
# 1. SSH into the ATTACKER Instance
ssh -i "your-key.pem" ec2-user@<attacker-instance-public-ip>

# 2. Try to hit Target 1 or Target 2 from the Attacker:
curl -v http://<target-1-ip>
# Expected: Connection timeout. The firewall blocks it at the subnet layer!

# 3. Disconnect from Attacker, and try from your LOCAL LAPTOP/another instance (which is NOT blocked):
curl -v http://<target-1-ip>
# Expected: 200 OK. The web server responds!
```

#### 🎯 Impact

| Before | After |
|--------|-------|
| Attack hits all 15 EC2 instances across 3 subnets | Blocked at subnet boundary — traffic never reaches any instance |
| SOC team updating 15 Security Groups manually | One NACL rule blocks the entire IP range instantly |
| Attack response time: 30+ minutes | Attack response time: < 2 minutes |

---

### Practical 2: Allow Only HTTPS Traffic to a Public Subnet via NACL

#### 🎯 What
Configure a custom NACL on a public subnet to allow **only HTTPS (port 443)** inbound traffic, blocking all other protocols including HTTP.

#### 🎯 Why (Industry Problem)
**Client Scenario:** A healthcare client (HIPAA compliance) requires that **all web traffic must be encrypted**. Their compliance auditor flagged that HTTP (port 80) is still accessible on their public-facing subnet. The client needs a network-level enforcement — not just application-level redirects.

#### 🎯 Pre-requisites
- Launch **1 EC2 instance** and paste the following into **User Data** to install Nginx and auto-configure a dummy SSL certificate for port 443 testing:
  ```bash
  #!/bin/bash
  apt update -y
  apt install nginx ssl-cert -y
  sed -i '/listen 80 default_server;/a \ \ \ \ listen 443 ssl default_server;\n    ssl_certificate /etc/ssl/certs/ssl-cert-snakeoil.pem;\n    ssl_certificate_key /etc/ssl/private/ssl-cert-snakeoil.key;' /etc/nginx/sites-available/default
  systemctl restart nginx
  ```
- Security Group must allow **HTTP (80)** and **HTTPS (443)** from `0.0.0.0/0`.
- An Elastic IP or public IP assigned to the instance.

#### 🎯 How (Step-by-Step)

**Step 1: Create a Strict NACL**
```
VPC → Network ACLs → Create Network ACL
  Name: https-only-nacl
  VPC: Select your VPC
```

**Step 2: Configure Inbound Rules**
```
Inbound Rules:
  Rule #100 → HTTPS (443)  → Source: 0.0.0.0/0 → ALLOW
  Rule #110 → SSH (22)     → Source: <your-ip>/32 → ALLOW
  Rule *    → All Traffic   → Source: 0.0.0.0/0 → DENY  (auto-created)
```
> ⚠️ Notice: There is NO rule for HTTP (port 80). It falls to the default DENY.

**Step 3: Configure Outbound Rules**
```
Outbound Rules:
  Rule #100 → Custom TCP → Port: 1024-65535 → Dest: 0.0.0.0/0 → ALLOW
  Rule *    → All Traffic → Dest: 0.0.0.0/0 → DENY
```

**Step 4: Associate with the Public Subnet**
```
Subnet Associations → Edit → Select public subnet → Save
```

**Step 5: Test**
```bash
# Test HTTP (should FAIL):
curl http://<ec2-public-ip>
# Expected: Connection timeout

# Test HTTPS (should WORK):
curl https://<ec2-public-ip>
# Expected: 200 OK (or SSL response)
```

#### 🎯 Impact

| Before | After |
|--------|-------|
| HTTP and HTTPS both accessible — compliance violation | Only HTTPS allowed — HIPAA compliant |
| Encryption enforcement depends on app config | Network-level enforcement — cannot be bypassed |
| Auditor flags the infrastructure | Passes compliance audit |

---

### Practical 3: NACL Stateless Behavior — Troubleshoot a Broken Web App

#### 🎯 What
Demonstrate and troubleshoot why a web application stops responding after applying a custom NACL with inbound ALLOW but **missing outbound rules** — proving NACL's stateless nature.

#### 🎯 Why (Industry Problem)
**Client Scenario:** A junior DevOps engineer at a SaaS startup applied a custom NACL to their production subnet. They added inbound rules for HTTP and SSH, but forgot to add outbound rules. All web applications immediately went down. The team is panicking — "Security Groups are fine, why is the app down?"

#### 🎯 Pre-requisites
- Launch **1 EC2 instance** with a web server (`apt update -y && apt install nginx -y; systemctl start nginx`).
- Security Group must allow **HTTP (80)** and **SSH (22)** from `0.0.0.0/0`.
- Verify the web app is accessible from your browser before starting.

#### 🎯 How (Step-by-Step)

**Step 1: Confirm the App Works with Default NACL**
```bash
curl http://<ec2-public-ip>
# Expected: 200 OK — app is working
```

**Step 2: Create a Custom NACL — Intentionally Missing Outbound Rules**
```
VPC → Create Network ACL → Name: broken-nacl

Inbound Rules:
  Rule #100 → HTTP (80) → Source: 0.0.0.0/0 → ALLOW
  Rule #110 → SSH (22)  → Source: 0.0.0.0/0 → ALLOW

Outbound Rules:
  (Leave ONLY the default * DENY ALL — don't add any ALLOW rules)
```

**Step 3: Associate with the Subnet**
```
Subnet Associations → Select the subnet → Save
```

**Step 4: Test — App Will Break**
```bash
curl http://<ec2-public-ip>
# Expected: Connection timeout!
# The request REACHES the server (inbound allowed)
# But the RESPONSE cannot leave (outbound denied)
```

**Step 5: Diagnose the Root Cause**
```
Key Insight:
┌──────────────────────────────────────────────────────┐
│ NACL is STATELESS                                    │
│                                                      │
│ Inbound ALLOW ≠ Outbound auto-ALLOW                 │
│ (Unlike Security Groups which ARE stateful)          │
│                                                      │
│ The HTTP request comes IN → allowed by rule 100      │
│ The HTTP response tries to go OUT → DENIED by rule * │
└──────────────────────────────────────────────────────┘
```

**Step 6: Fix It — Add Outbound Ephemeral Port Rule**
```
Outbound Rules → Edit:
  Rule #100 → Custom TCP → Port: 1024-65535 → Dest: 0.0.0.0/0 → ALLOW
```

**Step 7: Verify Fix**
```bash
curl http://<ec2-public-ip>
# Expected: 200 OK — app works again!
```

#### 🎯 Impact

| Learning | Real-World Effect |
|----------|-------------------|
| NACL is stateless — both directions must be explicitly configured | Prevents production outages from misconfigured NACLs |
| Security Groups are stateful — this mistake wouldn't happen with SG alone | Understanding the difference saves hours of debugging |
| Ephemeral ports (1024-65535) are needed for response traffic | Industry standard knowledge for network engineers |

---

### Practical 4: NACL + Security Group — Layered Defense (Defense-in-Depth)

#### 🎯 What
Build a **two-layer security model**: NACL blocks known bad IPs at the subnet level, while Security Groups allow only specific traffic at the instance level.

#### 🎯 Why (Industry Problem)
**Client Scenario:** An e-commerce company during a flash sale gets hit by bot traffic from a specific country's IP range. Meanwhile, their legitimate user traffic also increased. They need to:
1. Block the bot IP range at the subnet level (NACL)
2. Allow only required ports (80, 443) at the instance level (SG)
3. Allow SSH only from their office IP

#### 🎯 Pre-requisites
- VPC with public + private subnets
- **Launch 1 EC2 instance** in the public subnet. Install a web server (`apt update -y && apt install nginx -y; systemctl start nginx`).
- Know your office/home IP address (Search "What is my IP" online, append `/32` for the CIDR).
- **Setup 1 Attacker Instance**: Launch a separate EC2 instance in a different VPC (or simulate using another laptop). Note its Public IP.

#### 🎯 How (Step-by-Step)

**Step 1: Set Up the Security Group (Instance Level)**
```
EC2 → Security Groups → Create:
  Name: ecommerce-web-sg
  Inbound Rules:
    - HTTP (80)   → Source: 0.0.0.0/0
    - HTTPS (443) → Source: 0.0.0.0/0
    - SSH (22)    → Source: <office-ip>/32
  Outbound Rules:
    - All Traffic  → Destination: 0.0.0.0/0 (default)
```

**Step 2: Set Up the NACL (Subnet Level)**
```
VPC → Network ACLs → Create:
  Name: ecommerce-nacl

  Inbound Rules:
    Rule #50  → All Traffic → Source: 198.51.100.0/24 → DENY  ← Bot IP range
    Rule #60  → All Traffic → Source: 192.0.2.0/24    → DENY  ← Another bad range
    Rule #100 → HTTP (80)   → Source: 0.0.0.0/0       → ALLOW
    Rule #110 → HTTPS (443) → Source: 0.0.0.0/0       → ALLOW
    Rule #120 → SSH (22)    → Source: 0.0.0.0/0        → ALLOW

  Outbound Rules:
    Rule #100 → Custom TCP → Port: 1024-65535 → Dest: 0.0.0.0/0 → ALLOW
```

**Step 3: Associate NACL with the Public Subnet**

**Step 4: Test the Layered Defense**
```
Traffic Flow:

  Internet User
       │
       ▼
  ┌─ NACL Layer ──────────────────────────┐
  │  Is source IP in blocked range?       │
  │  YES → DROP (never reaches instance)  │
  │  NO  → Pass to Security Group         │
  └───────────────────────────────────────┘
       │
       ▼
  ┌─ Security Group Layer ───────────────┐
  │  Is the port allowed?               │
  │  YES → Allow to instance            │
  │  NO  → Drop silently                │
  └─────────────────────────────────────┘
       │
       ▼
  EC2 Instance (Web Server)
```

#### 🎯 Impact

| Layer | What It Catches |
|-------|----------------|
| NACL | Known malicious IP ranges — blocked before they hit any instance |
| Security Group | Unauthorized ports — only 80, 443, 22 from office |
| Combined | Defense-in-depth — even if one layer misconfigured, other catches |

---

### Practical 5: Plan a VPC CIDR for a Multi-Tier Application

#### 🎯 What
Design the IP addressing scheme (CIDR blocks) for a production VPC with Web, App, and Database tiers across 2 Availability Zones.

#### 🎯 Why (Industry Problem)
**Client Scenario:** A logistics company is migrating to AWS. They have a monolithic app being broken into microservices. They need a VPC that can support:
- 50 web servers (auto-scaling to 100)
- 30 application servers (auto-scaling to 60)
- 10 database servers (fixed)
- 2 Availability Zones for high availability
- Future growth of 3x

#### 🎯 Pre-requisites
- Understanding of CIDR notation
- A calculator or mental math for powers of 2
- Paper/notebook for diagramming

#### 🎯 How (Step-by-Step)

**Step 1: Calculate Total IP Requirement**
```
Tier          | Current | Max (Auto-Scale) | Future (3x) | Per AZ
──────────────|─────────|──────────────────|─────────────|────────
Web           | 50      | 100              | 300         | 150
App           | 30      | 60               | 180         | 90
Database      | 10      | 10               | 30          | 15
──────────────|─────────|──────────────────|─────────────|────────
Total per AZ  |         |                  |             | 255
Total         |         |                  |             | 510
```

**Step 2: Choose the VPC CIDR**
```
We need at least 510 IPs + buffer. Let's use /16 (65,536 IPs) for maximum flexibility.

VPC CIDR: 10.0.0.0/16
```

**Step 3: Design Subnet CIDRs**
```
┌─────────────────────────────────────────────────────────────┐
│                    VPC: 10.0.0.0/16                         │
│                                                             │
│  AZ-1 (ap-south-1a)           AZ-2 (ap-south-1b)          │
│  ┌───────────────────┐        ┌───────────────────┐        │
│  │ Web-1a            │        │ Web-1b            │        │
│  │ 10.0.1.0/24       │        │ 10.0.4.0/24       │        │
│  │ 251 usable IPs    │        │ 251 usable IPs    │        │
│  └───────────────────┘        └───────────────────┘        │
│  ┌───────────────────┐        ┌───────────────────┐        │
│  │ App-1a            │        │ App-1b            │        │
│  │ 10.0.2.0/24       │        │ 10.0.5.0/24       │        │
│  │ 251 usable IPs    │        │ 251 usable IPs    │        │
│  └───────────────────┘        └───────────────────┘        │
│  ┌───────────────────┐        ┌───────────────────┐        │
│  │ DB-1a             │        │ DB-1b             │        │
│  │ 10.0.3.0/28       │        │ 10.0.6.0/28       │        │
│  │ 11 usable IPs     │        │ 11 usable IPs     │        │
│  └───────────────────┘        └───────────────────┘        │
└─────────────────────────────────────────────────────────────┘
```

**Step 4: Verify no Overlaps and Create in AWS**
```
AWS Console → VPC → Create VPC:
  Name: logistics-prod-vpc
  CIDR: 10.0.0.0/16

Then create each subnet:
  VPC → Subnets → Create Subnet
  - Name: web-1a    | AZ: ap-south-1a | CIDR: 10.0.1.0/24
  - Name: app-1a    | AZ: ap-south-1a | CIDR: 10.0.2.0/24
  - Name: db-1a     | AZ: ap-south-1a | CIDR: 10.0.3.0/28
  - Name: web-1b    | AZ: ap-south-1b | CIDR: 10.0.4.0/24
  - Name: app-1b    | AZ: ap-south-1b | CIDR: 10.0.5.0/24
  - Name: db-1b     | AZ: ap-south-1b | CIDR: 10.0.6.0/28
```

#### 🎯 Impact

| Good Planning | Bad Planning |
|---------------|--------------|
| Room for 3x growth without re-architecting | Run out of IPs, must rebuild VPC |
| Non-overlapping CIDRs — ready for VPC Peering | Overlapping ranges block future peering |
| Subnets sized to tier needs — /28 for DB saves IP space | One-size-fits-all wastes thousands of IPs |
| AZ redundancy built in from day 1 | Single AZ = single point of failure |

---

### Practical 6: Subnet Sizing — Calculate IPs for a Client's Infrastructure

#### 🎯 What
Calculate the correct CIDR block for subnets based on actual client requirements. Practice converting requirements to CIDR notation.

#### 🎯 Why (Industry Problem)
**Client Scenario:** A gaming company is launching a new multiplayer game. They give you these requirements:
- **Game Servers Subnet:** Need exactly 500 IPs (game instances + auto-scaling buffer)
- **Admin Subnet:** Need 10 IPs (jump boxes, monitoring)
- **Database Subnet:** Need 20 IPs (RDS, ElastiCache)
- Must factor in AWS reserved IPs (5 per subnet)

#### 🎯 Pre-requisites
- CIDR formula: `Usable IPs = 2^(32 - prefix) - 5`
- A piece of paper or calculator

#### 🎯 How (Step-by-Step)

**Step 1: Calculate for Game Servers (Need 500 IPs)**
```
Need: 500 usable IPs
Formula: 2^(32 - prefix) - 5 ≥ 500
         2^(32 - prefix) ≥ 505

Try /23: 2^(32-23) = 2^9 = 512 → 512 - 5 = 507 usable ✅ (just enough)
Try /24: 2^(32-24) = 2^8 = 256 → 256 - 5 = 251 usable ❌ (not enough)

Answer: Use /23 (e.g., 10.0.0.0/23)
```

**Step 2: Calculate for Admin (Need 10 IPs)**
```
Need: 10 usable IPs
Try /28: 2^(32-28) = 2^4 = 16 → 16 - 5 = 11 usable ✅
Try /29: 2^(32-29) = 2^3 = 8  → 8 - 5  = 3 usable  ❌

Answer: Use /28 (e.g., 10.0.10.0/28)
```

**Step 3: Calculate for Database (Need 20 IPs)**
```
Need: 20 usable IPs
Try /27: 2^(32-27) = 2^5 = 32 → 32 - 5 = 27 usable ✅
Try /28: 2^(32-28) = 2^4 = 16 → 16 - 5 = 11 usable ❌

Answer: Use /27 (e.g., 10.0.20.0/27)
```

**Step 4: Summary Table**
```
┌──────────────────┬────────┬───────────┬────────────┬────────────┐
│ Subnet           │ CIDR   │ Total IPs │ Usable IPs │ Needed IPs │
├──────────────────┼────────┼───────────┼────────────┼────────────┤
│ Game Servers     │ /23    │ 512       │ 507        │ 500        │
│ Admin            │ /28    │ 16        │ 11         │ 10         │
│ Database         │ /27    │ 32        │ 27         │ 20         │
└──────────────────┴────────┴───────────┴────────────┴────────────┘
```

**Step 5: Create in AWS and Verify**
```
VPC → Subnets → Create each subnet
After creation, AWS Console will show "Available IPs" — verify it matches your calculations.
```

#### 🎯 Impact

| Correct Sizing | Over/Under Sizing |
|----------------|-------------------|
| Optimal IP usage — no waste, no shortage | Over-sizing wastes IPs, under-sizing causes launch failures |
| Clients get exactly what they need | Auto-scaling fails if subnet is exhausted |
| Shows DevOps maturity in architecture planning | Shows lack of planning — interview red flag |

---

### Practical 7: Avoid CIDR Overlap Before Peering — Planning Phase

#### 🎯 What
Before setting up VPC Peering, **audit existing VPC CIDR ranges** to ensure they don't overlap. Design new VPCs with unique ranges.

#### 🎯 Why (Industry Problem)
**Client Scenario:** A retail company acquires a smaller brand. Both companies independently built AWS infrastructure. The parent company's VPC uses `10.0.0.0/16` and the acquired company also uses `10.0.0.0/16`. They now want to connect the two VPCs for data sharing. **The peering request will fail.**

#### 🎯 Pre-requisites
- At least 2 VPCs to inspect (create 2 test VPCs if needed)
- Understanding of CIDR notation and overlap detection

#### 🎯 How (Step-by-Step)

**Step 1: Audit All Existing VPC CIDRs**
```bash
# AWS CLI — list all VPC CIDRs:
aws ec2 describe-vpcs --query "Vpcs[*].{VpcId:VpcId, CIDR:CidrBlock, Name:Tags[?Key=='Name'].Value|[0]}" --output table

# Expected Output:
# ┌──────────────┬───────────────┬───────────────┐
# │    VpcId     │    CIDR       │    Name       │
# ├──────────────┼───────────────┤───────────────┤
# │ vpc-0abc123  │ 10.0.0.0/16  │ parent-vpc    │
# │ vpc-0def456  │ 10.0.0.0/16  │ acquired-vpc  │  ← OVERLAP!
# └──────────────┴───────────────┴───────────────┘
```

**Step 2: Identify Overlapping Ranges**
```
Overlap Check:
  parent-vpc:   10.0.0.0   → 10.0.255.255  (/16 = 65,536 IPs)
  acquired-vpc: 10.0.0.0   → 10.0.255.255  (/16 = 65,536 IPs)

  Result: COMPLETE OVERLAP ❌ — peering impossible
```

**Step 3: Plan the Fix — Recreate One VPC with a New CIDR**
```
Strategy:
  - Keep parent-vpc as 10.0.0.0/16
  - Recreate acquired-vpc as 10.1.0.0/16

New Layout:
  parent-vpc:   10.0.0.0/16 (10.0.0.0 → 10.0.255.255)
  acquired-vpc: 10.1.0.0/16 (10.1.0.0 → 10.1.255.255)

  No overlap ✅ — peering possible
```

**Step 4: Create a CIDR Planning Document (Best Practice)**
```
┌──────────────────────────────────────────────────┐
│          Company CIDR Allocation Plan            │
├──────────────┬───────────────┬───────────────────┤
│ Team/Unit    │ VPC CIDR      │ Status            │
├──────────────┼───────────────┼───────────────────┤
│ Parent Prod  │ 10.0.0.0/16  │ Active            │
│ Parent Dev   │ 10.2.0.0/16  │ Active            │
│ Acquired Co. │ 10.1.0.0/16  │ Migrated          │
│ Future Use   │ 10.3.0.0/16  │ Reserved          │
│ Future Use   │ 10.4.0.0/16  │ Reserved          │
└──────────────┴───────────────┴───────────────────┘
```

#### 🎯 Impact

| With CIDR Planning | Without CIDR Planning |
|--------------------|----------------------|
| VPC Peering works first time | Peering fails — hours of debugging |
| Mergers & acquisitions are smooth | Forced to rebuild entire VPCs |
| Future-proof — reserved ranges available | Ad-hoc planning leads to conflicts |
| Industry best practice — documented allocation | Chaotic IP management |

---

### Practical 8: Connect Two Team VPCs via VPC Peering (Same Account)

#### 🎯 What
Set up VPC Peering between a **Development VPC** and a **Production VPC** within the same AWS account so dev team can access a shared database in prod.

#### 🎯 Why (Industry Problem)
**Client Scenario:** A media streaming company has separate VPCs for Dev and Prod. The Dev team needs read-only access to the production content catalog database for testing with real data structures (not the data itself, but the schema/metadata service). Currently, they dump data exports manually — slow and error-prone. VPC Peering would allow a direct, private, controlled connection.

#### 🎯 Pre-requisites
- 2 VPCs with **non-overlapping** CIDRs
  - Dev VPC: `10.0.0.0/16`
  - Prod VPC: `10.1.0.0/16`
- **Launch 1 EC2 Instance in each VPC**:
  - Dev Instance (e.g., 10.0.1.5)
  - Prod Instance (e.g., 10.1.1.10)
- Security Groups on both instances allowing traffic (like ICMP Ping or MySQL port 3306) from the peer VPC CIDR.

#### 🎯 How (Step-by-Step)

**Step 1: Create Two VPCs (if not existing)**
```
VPC → Create VPC:
  VPC 1: dev-vpc  | CIDR: 10.0.0.0/16
  VPC 2: prod-vpc | CIDR: 10.1.0.0/16

Create a subnet in each + launch an EC2 instance in each.
```

**Step 2: Create the Peering Connection**
```
VPC → Peering Connections → Create Peering Connection:
  Name: dev-to-prod-peering
  Requester VPC: dev-vpc (10.0.0.0/16)
  Accepter VPC: prod-vpc (10.1.0.0/16)
  Account: My account
  Region: This Region
  → Create Peering Connection
```

**Step 3: Accept the Peering Request**
```
VPC → Peering Connections → Select the pending request → Actions → Accept
Status should change to: Active ✅
```

**Step 4: Update Route Tables (BOTH VPCs)**
```
Dev VPC Route Table:
  Destination: 10.1.0.0/16 (prod VPC CIDR)
  Target: pcx-xxxxxxx (the peering connection ID)

Prod VPC Route Table:
  Destination: 10.0.0.0/16 (dev VPC CIDR)
  Target: pcx-xxxxxxx (the peering connection ID)
```

**Step 5: Update Security Groups**
```
Prod EC2 Security Group:
  Inbound: Allow TCP 3306 (MySQL) from 10.0.0.0/16 (dev VPC range)

Dev EC2 Security Group:
  Inbound: Allow ICMP (ping) from 10.1.0.0/16 (for testing)
```

**Step 6: Test Connectivity**
```bash
# From Dev EC2 instance:
ping <prod-ec2-private-ip>
# Expected: Replies from 10.1.x.x ✅

# Test database access:
mysql -h <prod-ec2-private-ip> -u readonly -p
# Expected: Connected to prod database ✅

# Verify NO public internet is used:
traceroute <prod-ec2-private-ip>
# Expected: Direct hop via VPC peering — no internet gateway
```

#### 🎯 Impact

| With VPC Peering | Without VPC Peering |
|------------------|---------------------|
| Private, encrypted communication | Data exported over internet — security risk |
| Low latency (same region, direct route) | Higher latency through internet |
| No data transfer cost (same region) | Data transfer costs apply |
| Access controlled by Security Groups + NACLs | Hard to control access |

---

### Practical 9: Cross-Account VPC Peering for a Client Merger

#### 🎯 What
Establish VPC Peering between two VPCs in **different AWS accounts** — simulating a company acquisition scenario.

#### 🎯 Why (Industry Problem)
**Client Scenario:** Company A (Account: 111111111111) acquires Company B (Account: 222222222222). Both companies need to share internal services (SSO, monitoring, logging) without exposing them to the internet. This requires **cross-account VPC Peering**.

#### 🎯 Pre-requisites
- 2 AWS accounts (or use AWS Organizations)
- VPC in Account A: `10.0.0.0/16`
- VPC in Account B: `172.16.0.0/16`
- **Launch 1 EC2 Instance in each VPC**:
  - Account A Instance (e.g., 10.0.1.5)
  - Account B Instance (e.g., 172.16.1.10)
- IAM permissions for VPC Peering in both accounts

#### 🎯 How (Step-by-Step)

**Step 1: From Account A — Send Peering Request**
```
VPC → Peering Connections → Create:
  Requester VPC: vpc-aaa (10.0.0.0/16) in Account A
  Accepter:
    Account: Another Account
    Account ID: 222222222222
    Region: Same region (or specify cross-region)
    VPC ID: vpc-bbb
  → Create
```

**Step 2: Log into Account B — Accept the Request**
```
VPC → Peering Connections → Select pending request → Actions → Accept
```

**Step 3: Update Route Tables in BOTH Accounts**
```
Account A Route Table:
  Dest: 172.16.0.0/16 → Target: pcx-xxxxxxx

Account B Route Table:
  Dest: 10.0.0.0/16 → Target: pcx-xxxxxxx
```

**Step 4: Update Security Groups in Both Accounts**
```
Account A SG: Allow inbound from 172.16.0.0/16 on required ports
Account B SG: Allow inbound from 10.0.0.0/16 on required ports
```

**Step 5: DNS Resolution Across Peering (Optional but Important)**
```
VPC → Peering Connection → Select → Actions → Edit DNS Settings
  ✅ Enable "Allow DNS resolution from the peer VPC"
  (This lets instances resolve each other's private DNS names)
```

**Step 6: Test**
```bash
# From Account A's EC2:
ping <account-b-ec2-private-ip>
nslookup <account-b-ec2-private-dns>
```

#### 🎯 Impact

| With Cross-Account Peering | Without It |
|---------------------------|------------|
| Secure private connectivity post-merger | Services exposed via public internet |
| Centralized monitoring across both companies | Separate, siloed monitoring |
| Shared SSO/auth services | Duplicate identity systems |
| No VPN hardware needed | Expensive VPN or Direct Connect required |

---

### Practical 10: Prove That Transitive Peering Does NOT Work

#### 🎯 What
Set up 3 VPCs (A, B, C), peer A↔B and B↔C, then **prove** that A **cannot** communicate with C through B.

#### 🎯 Why (Industry Problem)
**Client Scenario:** A DevOps lead at a consulting firm assumes that since the Staging VPC peers with the Shared Services VPC, and Shared Services peers with Production, then Staging can access Production. This is a **dangerous assumption** that could lead to security incidents or unexpected connectivity failures.

#### 🎯 Pre-requisites
- 3 VPCs with non-overlapping CIDRs:
  - VPC-A (Staging): `10.0.0.0/16`
  - VPC-B (Shared Services): `10.1.0.0/16`
  - VPC-C (Production): `10.2.0.0/16`
- **Launch 1 EC2 instance in each VPC**:
  - Make sure their Security Groups allow **ICMP - IPv4 (Ping)** and SSH from *all* the other VPC CIDR ranges so you can test freely.

#### 🎯 How (Step-by-Step)

**Step 1: Create 3 VPCs and Launch Instances**
```
VPC-A: 10.0.0.0/16 → EC2 in 10.0.1.x
VPC-B: 10.1.0.0/16 → EC2 in 10.1.1.x
VPC-C: 10.2.0.0/16 → EC2 in 10.2.1.x
```

**Step 2: Create Peering A ↔ B**
```
Create Peering: A-to-B → Accept
Route Table A: 10.1.0.0/16 → pcx-AB
Route Table B: 10.0.0.0/16 → pcx-AB
SG updates for A & B (allow ICMP from peer CIDR)
```

**Step 3: Create Peering B ↔ C**
```
Create Peering: B-to-C → Accept
Route Table B: 10.2.0.0/16 → pcx-BC
Route Table C: 10.1.0.0/16 → pcx-BC
SG updates for B & C (allow ICMP from peer CIDR)
```

**Step 4: Verify Direct Peers Work**
```bash
# From VPC-A EC2:
ping <vpc-b-ec2-private-ip>
# Result: ✅ SUCCESS — A can reach B

# From VPC-B EC2:
ping <vpc-c-ec2-private-ip>
# Result: ✅ SUCCESS — B can reach C
```

**Step 5: Attempt Transitive Communication (A → C)**
```bash
# From VPC-A EC2:
ping <vpc-c-ec2-private-ip>
# Result: ❌ TIMEOUT — A CANNOT reach C through B!
```

**Step 6: Understand Why**
```
Traffic Flow Attempt:
  VPC-A (10.0.1.5) → wants to reach → VPC-C (10.2.1.10)

  VPC-A's route table has NO route for 10.2.0.0/16
  Even if you added 10.2.0.0/16 → pcx-AB, the peering connection
  pcx-AB only connects A and B — it does NOT forward to C.

  AWS Design Decision:
  ┌─────────────────────────────────────────────────┐
  │  VPC Peering is POINT-TO-POINT.                 │
  │  No packet forwarding through a peered VPC.     │
  │  This is BY DESIGN for SECURITY reasons.        │
  │                                                 │
  │  Solution: Direct peering A↔C OR Transit Gateway│
  └─────────────────────────────────────────────────┘
```

**Step 7: Fix — Create Direct Peering A ↔ C (or use Transit Gateway)**
```
Create Peering: A-to-C → Accept
Route Table A: 10.2.0.0/16 → pcx-AC
Route Table C: 10.0.0.0/16 → pcx-AC

# Now test:
ping <vpc-c-ec2-private-ip>
# Result: ✅ SUCCESS
```

#### 🎯 Impact

| Learning | Industry Impact |
|----------|-----------------|
| VPC Peering is NOT transitive — proven hands-on | Prevents false security assumptions |
| Each peer acts as an isolated connection | Architects must plan connectivity explicitly |
| Transit Gateway solves this at scale | Key decision point: Peering vs TGW |

---

### Practical 11: Replace a Peering Mesh with Transit Gateway

#### 🎯 What
Take a scenario with 4 VPCs connected via a full peering mesh (6 connections) and **migrate** to a Transit Gateway (4 connections).

#### 🎯 Why (Industry Problem)
**Client Scenario:** A large bank has 4 departmental VPCs (Trading, Risk, Compliance, Operations). Originally connected via full peering mesh — **6 peering connections**. Every time a new VPC is added, they need to create peering with ALL existing VPCs. Managing route tables across all connections is becoming a major operational burden. They want a centralized hub.

```
Current Mesh (6 connections for 4 VPCs):
  Trading ──── Risk
    │    ╲  ╱    │
    │     ╳      │
    │    ╱  ╲    │
Compliance ── Operations

After Transit Gateway (4 connections):
    Trading
       │
Compliance─TGW─Risk
       │
   Operations
```

#### 🎯 Pre-requisites
- 4 VPCs with non-overlapping CIDRs:
  - Trading: `10.0.0.0/16`
  - Risk: `10.1.0.0/16`
  - Compliance: `10.2.0.0/16`
  - Operations: `10.3.0.0/16`
- **Launch 1 EC2 instance in each VPC** and ensure their Security Groups allow **All ICMP - IPv4** (ping).
- AWS account with Transit Gateway permissions

#### 🎯 How (Step-by-Step)

**Step 1: Create a Transit Gateway**
```
VPC → Transit Gateways → Create Transit Gateway:
  Name: bank-central-tgw
  ASN: 64512 (default)
  DNS Support: Enable
  VPN ECMP Support: Enable
  Default Route Table Association: Enable
  Default Route Table Propagation: Enable
  → Create
```

**Step 2: Create Transit Gateway Attachments (1 per VPC)**
```
VPC → Transit Gateway Attachments → Create:

  Attachment 1:
    TGW: bank-central-tgw
    Attachment Type: VPC
    VPC: Trading VPC
    Subnets: Select one subnet per AZ
    Name: tgw-trading

  Repeat for Risk, Compliance, Operations (4 total attachments)
```

**Step 3: Verify Transit Gateway Route Table**
```
VPC → Transit Gateway Route Tables → Select default route table
Routes tab should show:
  10.0.0.0/16 → tgw-trading    (propagated)
  10.1.0.0/16 → tgw-risk       (propagated)
  10.2.0.0/16 → tgw-compliance (propagated)
  10.3.0.0/16 → tgw-operations (propagated)
```

**Step 4: Update Each VPC Route Table**
```
For EACH VPC's route table, add routes to all OTHER VPCs via TGW:

Trading VPC Route Table:
  10.1.0.0/16 → tgw-xxxxxxx
  10.2.0.0/16 → tgw-xxxxxxx
  10.3.0.0/16 → tgw-xxxxxxx

(Or use a single supernet route: 10.0.0.0/8 → tgw-xxxxxxx)
```

**Step 5: Update Security Groups**
```
Each EC2's SG: Allow ICMP from 10.0.0.0/8 (all VPC ranges)
```

**Step 6: Test Transitive Routing (This NOW Works!)**
```bash
# From Trading EC2:
ping <risk-ec2-private-ip>        # ✅ Works
ping <compliance-ec2-private-ip>  # ✅ Works
ping <operations-ec2-private-ip>  # ✅ Works

# From ANY VPC to ANY other VPC:  # ✅ All work via Transit Gateway
```

**Step 7: Remove Old Peering Connections**
```
VPC → Peering Connections → Select each → Actions → Delete
Remove peering routes from all route tables
```

#### 🎯 Impact

| Metric | Peering Mesh (Before) | Transit Gateway (After) |
|--------|----------------------|------------------------|
| Connections | 6 (for 4 VPCs) | 4 (one per VPC) |
| Adding 1 new VPC | +4 new peering + routes | +1 attachment |
| Transitive routing | ❌ Not supported | ✅ Built-in |
| Route management | 12 route entries (2 per peer) | 4 route entries |
| Operational complexity | High | Low — centralized |
| Cost | Lower per-connection | Slightly higher (TGW hourly + data) |

---

### Practical 12: Hub-and-Spoke — Shared Services VPC via Transit Gateway

#### 🎯 What
Design and implement a **hub-and-spoke** architecture where a **Shared Services VPC** (containing DNS, monitoring, logging) is accessible to all spoke VPCs through a Transit Gateway.

#### 🎯 Why (Industry Problem)
**Client Scenario:** A multinational company has VPCs for each business unit (Marketing, Engineering, Sales, Finance). Each unit needs access to shared infrastructure:
- Centralized logging (ELK Stack)
- DNS resolver (Route 53 Resolver)
- Monitoring (Prometheus/Grafana)
- Security scanning (GuardDuty aggregation)

Instead of deploying these services in every VPC, they deploy once in a **Shared Services VPC** and connect via TGW.

#### 🎯 Pre-requisites
- Transit Gateway created
- 3+ VPCs (1 shared services + 2 spoke VPCs)
- **Launch EC2 instances**:
  - In Spoke VPCs (e.g., Marketing, Engineering).
  - In Shared Services VPC: Launch an instance and install dummy services to simulate apps (e.g., run a Python HTTP server on port 3000 to mock Grafana: `python3 -m http.server 3000`).

#### 🎯 How (Step-by-Step)

**Step 1: Design the Architecture**
```
Hub-and-Spoke Layout:

  Marketing VPC ─────┐
    10.1.0.0/16      │
                     │
  Engineering VPC ───┤
    10.2.0.0/16      │──── Transit Gateway ──── Shared Services VPC
                     │                          10.0.0.0/16
  Sales VPC ─────────┤                         (ELK, Grafana, DNS)
    10.3.0.0/16      │
                     │
  Finance VPC ───────┘
    10.4.0.0/16
```

**Step 2: Create the Shared Services VPC**
```
VPC: shared-services-vpc | CIDR: 10.0.0.0/16
Subnets:
  - monitoring-subnet: 10.0.1.0/24 (Grafana, Prometheus)
  - logging-subnet:    10.0.2.0/24 (ELK Stack)
  - dns-subnet:        10.0.3.0/24 (Route 53 Resolver)
```

**Step 3: Attach All VPCs to Transit Gateway**
```
Create TGW attachments for:
  - shared-services-vpc
  - marketing-vpc
  - engineering-vpc
  - sales-vpc
  - finance-vpc
```

**Step 4: Configure TGW Route Tables for Controlled Access**
```
Option A — All VPCs Can Talk to Shared Services Only (No Cross-Spoke):

  Create 2 TGW Route Tables:
    1. spoke-rt:
       - Route: 10.0.0.0/16 → shared-services attachment
       - Associate: marketing, engineering, sales, finance
       - (No routes to other spoke VPCs!)

    2. shared-services-rt:
       - Route: 10.1.0.0/16 → marketing attachment
       - Route: 10.2.0.0/16 → engineering attachment
       - Route: 10.3.0.0/16 → sales attachment
       - Route: 10.4.0.0/16 → finance attachment
       - Associate: shared-services VPC
```

**Step 5: Update VPC Route Tables**
```
Each spoke VPC route table:
  Dest: 10.0.0.0/16 → Target: tgw-xxxxxxx

Shared services route table:
  Dest: 10.0.0.0/8 → Target: tgw-xxxxxxx (supernet for all spokes)
```

**Step 6: Test**
```bash
# From Marketing EC2:
curl http://10.0.1.50:3000   # Grafana in shared services ✅
curl http://10.0.2.50:9200   # Elasticsearch in shared services ✅

# From Marketing EC2 trying to reach Engineering:
ping 10.2.1.10               # ❌ TIMEOUT — spoke-to-spoke blocked
```

#### 🎯 Impact

| Hub-and-Spoke | Duplicated Services |
|---------------|---------------------|
| One ELK stack serves all business units | 5 separate ELK setups — 5x cost |
| Centralized security monitoring | Fragmented visibility |
| Single pane of glass for dashboards | Multiple dashboards, inconsistent |
| Spoke isolation — Marketing can't reach Finance | No isolation between units |
| Cost: ~$300/month (TGW + shared infra) | Cost: ~$1,500/month (5x everything) |

---

### Practical 13: Full Scenario — Secure Multi-VPC Architecture for a FinTech Client

#### 🎯 What
Design and implement a **complete production architecture** combining ALL concepts: CIDR planning, VPC Peering, Transit Gateway, NACLs, and Security Groups — for a FinTech client's payment processing platform.

#### 🎯 Why (Industry Problem)
**Client Scenario:** A FinTech startup is launching a payment gateway. They need:
- **PCI-DSS compliance** (strict network segmentation)
- **Production VPC** for payment processing
- **Staging VPC** for testing
- **Shared Services VPC** for logging, monitoring, and security scanning
- Production ↔ Shared Services connectivity (via TGW)
- Staging ↔ Shared Services connectivity (via TGW)
- **NO direct path** between Production and Staging
- NACL rules to block known malicious IP ranges
- Security Groups for fine-grained instance access

#### 🎯 Pre-requisites
- AWS account with full VPC, EC2, TGW permissions
- Understanding of all previous practicals
- Time: 60-90 minutes

#### 🎯 How (Step-by-Step)

**Step 1: CIDR Planning (Practical 5 + 7)**
```
┌────────────────────────────────────────────────────────┐
│              CIDR Allocation Plan                      │
├──────────────────┬───────────────┬─────────────────────┤
│ VPC              │ CIDR          │ Purpose             │
├──────────────────┼───────────────┼─────────────────────┤
│ Production       │ 10.0.0.0/16  │ Payment processing  │
│ Staging          │ 10.1.0.0/16  │ Testing             │
│ Shared Services  │ 10.2.0.0/16  │ Logging/Monitoring  │
│ Reserved         │ 10.3.0.0/16  │ Future use          │
└──────────────────┴───────────────┴─────────────────────┘
No overlaps — all VPCs peerable ✅
```

**Step 2: Create All 3 VPCs with Subnets**
```
Production VPC (10.0.0.0/16):
  - pub-web:    10.0.1.0/24  (Web servers — public)
  - priv-app:   10.0.2.0/24  (App servers — private)
  - priv-db:    10.0.3.0/28  (Database — private, isolated)

Staging VPC (10.1.0.0/16):
  - pub-web:    10.1.1.0/24
  - priv-app:   10.1.2.0/24
  - priv-db:    10.1.3.0/28

Shared Services VPC (10.2.0.0/16):
  - monitoring: 10.2.1.0/24  (Grafana, Prometheus)
  - logging:    10.2.2.0/24  (ELK)
  - security:   10.2.3.0/24  (GuardDuty, Inspector)
```

**Step 3: Set Up Transit Gateway with Isolation (Practical 12)**
```
Create TGW: fintech-tgw

TGW Route Table — spoke-rt (associate: prod, staging):
  Route: 10.2.0.0/16 → shared-services attachment ONLY
  (Production and Staging CANNOT reach each other)

TGW Route Table — hub-rt (associate: shared-services):
  Route: 10.0.0.0/16 → prod attachment
  Route: 10.1.0.0/16 → staging attachment
```

**Step 4: Apply NACLs for PCI-DSS Compliance (Practical 1 + 2)**
```
Production Database Subnet NACL (strictest):
  Inbound:
    Rule #100: Allow TCP 3306 from 10.0.2.0/24 (app subnet only)
    Rule *:    DENY ALL

  Outbound:
    Rule #100: Allow TCP 1024-65535 to 10.0.2.0/24
    Rule *:    DENY ALL

Production Web Subnet NACL:
  Inbound:
    Rule #50:  DENY ALL from 198.51.100.0/24 (known bad range)
    Rule #60:  DENY ALL from 203.0.113.0/24  (known bad range)
    Rule #100: Allow HTTPS (443) from 0.0.0.0/0
    Rule *:    DENY ALL

  Outbound:
    Rule #100: Allow TCP 1024-65535 to 0.0.0.0/0
    Rule #110: Allow HTTPS (443) to 10.0.2.0/24 (to app tier)
    Rule *:    DENY ALL
```

**Step 5: Configure Security Groups (Practical 4)**
```
Web SG:
  Inbound: HTTPS (443) from 0.0.0.0/0
  Outbound: TCP 8080 to App SG

App SG:
  Inbound: TCP 8080 from Web SG
  Outbound: TCP 3306 to DB SG, HTTPS to 10.2.0.0/16 (shared services)

DB SG:
  Inbound: TCP 3306 from App SG ONLY
  Outbound: DENY ALL (except response traffic — stateful)
```

**Step 6: Verify the Architecture**
```
Test Matrix:
┌──────────────────────┬─────────────────────────────┬──────────┐
│ From                 │ To                          │ Expected │
├──────────────────────┼─────────────────────────────┼──────────┤
│ Internet             │ Prod Web (HTTPS)            │ ✅ Allow │
│ Internet             │ Prod Web (HTTP)             │ ❌ Block │
│ Prod Web             │ Prod App (8080)             │ ✅ Allow │
│ Prod App             │ Prod DB (3306)              │ ✅ Allow │
│ Prod Web             │ Prod DB (3306)              │ ❌ Block │
│ Prod App             │ Shared Services (Grafana)   │ ✅ Allow │
│ Staging App          │ Shared Services (ELK)       │ ✅ Allow │
│ Staging              │ Production (any)            │ ❌ Block │
│ Blocked IP range     │ Prod Web (any)              │ ❌ Block │
│ Internet             │ Prod DB (any)               │ ❌ Block │
└──────────────────────┴─────────────────────────────┴──────────┘
```

```bash
# Verification Commands (from respective EC2 instances):

# 1. Internet → Prod Web
curl https://<prod-web-public-ip>                    # ✅

# 2. Prod Web → Prod App
curl http://10.0.2.x:8080/health                     # ✅

# 3. Prod App → Prod DB
mysql -h 10.0.3.x -u app_user -p                     # ✅

# 4. Prod Web → Prod DB (SHOULD FAIL)
mysql -h 10.0.3.x -u app_user -p                     # ❌ Timeout

# 5. Prod → Shared Services
curl http://10.2.1.x:3000                             # ✅ Grafana

# 6. Staging → Production (SHOULD FAIL)
ping 10.0.1.x                                        # ❌ Timeout

# 7. Staging → Shared Services
curl http://10.2.2.x:9200                             # ✅ Elasticsearch
```

#### 🎯 Impact

| Aspect | Result |
|--------|--------|
| **PCI-DSS Compliance** | Database isolated — only app tier can access. NACL + SG double protection. |
| **Threat Mitigation** | Known malicious IPs blocked at NACL level before reaching any instance. |
| **Environment Isolation** | Staging CANNOT touch Production — TGW route table enforced. |
| **Centralized Operations** | Both envs send logs/metrics to Shared Services — single pane of glass. |
| **Scalability** | Adding a new env (e.g., DR) = 1 TGW attachment + routes. |
| **Cost Optimization** | Shared services deployed once, not per-environment. |

---

### 🧮 Quick Reference: CIDR Cheat Sheet

```
┌────────┬────────────────┬────────────┬──────────────────────────────┐
│ Prefix │ Total IPs      │ Usable IPs │ Use Case                     │
├────────┼────────────────┼────────────┼──────────────────────────────┤
│ /16    │ 65,536         │ 65,531     │ Large VPC                    │
│ /17    │ 32,768         │ 32,763     │ Medium VPC                   │
│ /18    │ 16,384         │ 16,379     │ Small VPC                    │
│ /19    │ 8,192          │ 8,187      │ Large subnet                 │
│ /20    │ 4,096          │ 4,091      │ Large subnet                 │
│ /21    │ 2,048          │ 2,043      │ Medium subnet                │
│ /22    │ 1,024          │ 1,019      │ Medium subnet                │
│ /23    │ 512            │ 507        │ Small-medium subnet          │
│ /24    │ 256            │ 251        │ Standard subnet              │
│ /25    │ 128            │ 123        │ Small subnet                 │
│ /26    │ 64             │ 59         │ Small subnet                 │
│ /27    │ 32             │ 27         │ Very small subnet            │
│ /28    │ 16             │ 11         │ Minimum recommended (AWS)    │
└────────┴────────────────┴────────────┴──────────────────────────────┘
```

---

### 🏁 Completion Checklist

Use this to track your practical completion:

- [ ] **Practical 1:** NACL — Block malicious IP range
- [ ] **Practical 2:** NACL — HTTPS-only enforcement
- [ ] **Practical 3:** NACL — Stateless troubleshooting
- [ ] **Practical 4:** NACL + SG — Layered defense
- [ ] **Practical 5:** CIDR — Multi-tier VPC planning
- [ ] **Practical 6:** CIDR — Subnet sizing calculations
- [ ] **Practical 7:** CIDR — Overlap detection before peering
- [ ] **Practical 8:** VPC Peering — Same account
- [ ] **Practical 9:** VPC Peering — Cross-account
- [ ] **Practical 10:** VPC Peering — Prove no transitive routing
- [ ] **Practical 11:** Transit Gateway — Replace peering mesh
- [ ] **Practical 12:** Transit Gateway — Hub-and-spoke shared services
- [ ] **Practical 13:** Full Scenario — FinTech multi-VPC architecture

---

> 💡 **Tip:** Start with Practicals 1-3 (NACL), then 5-6 (CIDR), then 8 & 10 (VPC Peering), and finally 11-12 (Transit Gateway). Practical 13 is the capstone — do it last.

---
Prev : [20_VPC_&_Networking.md](20_VPC_&_Networking.md) | Next : [22_aws_cloudwatch_monitoring_and_billing.md](22_aws_cloudwatch_monitoring_and_billing.md)
---
