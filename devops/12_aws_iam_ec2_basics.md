# ☁️ AWS IAM & EC2 Hands-on Guide

## 1. 📌 Introduction
Welcome to your first big step into the Cloud! 🚀 In this guide, we are going completely hands-on with two of the most important services in Amazon Web Services (AWS):
- **IAM (Identity and Access Management):** The "Security Guard" of your AWS account. It decides *who* can enter and *what* they can do.
- **EC2 (Elastic Compute Cloud):** A fancy name for "Virtual Computers in the Cloud". We will rent a computer from Amazon and run Windows on it!

By the end of this guide, you will know exactly how to manage users securely and launch your very own Windows server on the internet. Let's do this! 💪

## 2. 📚 Table of Contents
1. [📌 Introduction](#1--introduction)
2. [📚 Table of Contents](#2--table-of-contents)
3. [🔐 IAM (Identity and Access Management) Basics](#3--iam-identity-and-access-management-basics)
4. [👤 IAM Users, Groups & Best Practices](#4--iam-users-groups--best-practices)
5. [🤖 Service Accounts (Bot Users)](#5--service-accounts-bot-users)
6. [📜 IAM Policies & Roles](#6--iam-policies--roles)
7. [🔑 Authentication vs Authorization](#7--authentication-vs-authorization)
8. [🧾 Credential Reports & Security Best Practices](#8--credential-reports--security-best-practices)
9. [💻 EC2 (Elastic Compute Cloud) Introduction](#9--ec2-elastic-compute-cloud-introduction)
10. [🪟 Launching Windows Server on EC2](#10--launching-windows-server-on-ec2)
11. [🔐 Key Pairs & Secure Access](#11--key-pairs--secure-access)
12. [🖥️ Connecting to EC2 via RDP](#12-️-connecting-to-ec2-via-rdp)
13. [🌍 Region Concept (Important)](#13--region-concept-important)
14. [🏋️ Practice Tasks](#14-️-practice-tasks)
15. [🎤 Interview Questions](#15--interview-questions)
16. [📝 Summary](#16--summary)

---

## 3. 🔐 IAM (Identity and Access Management) Basics
### What is IAM?
IAM stands for **Identity and Access Management**. It is a free AWS service that helps you control who can access your AWS resources (like databases, servers, or files).

### Why is it important?
When you create an AWS account, you log in using your email address and password. This is called the **Root User**. The root user is like the CEO or the absolute owner of the entire company—they can do anything, including deleting the entire account or spending unlimited money! 💸

> ⚠️ **BEST PRACTICE:** NEVER use your Root account for daily tasks! Instead, use IAM to create separate "employee" accounts with limited powers.

### Real-World Analogy 🏢
Imagine AWS is a large office building.
- **Root User:** The building owner with the master key to every room.
- **IAM:** The security desk at the front door. They issue ID badges (Users) and decide who can enter the server room, who can only enter the cafeteria, and who isn't strictly allowed anywhere.

---

## 4. 👤 IAM Users, Groups & Best Practices

### What is an IAM User?
An IAM User is a digital identity with a specific name, password, and permissions. Just like you have a login for Netflix, an IAM User gives an engineer a login to your AWS account.

### What is an IAM Group?
A Group is simply a collection of IAM Users. 

**Scenario:** You have 5 new developers joining your team. Instead of giving permissions to each developer one by one, you:
1. Create a group called `DevOps-Team`.
2. Give the `DevOps-Team` group permission to use EC2 servers.
3. Add the 5 new developers to this group. 
*Boom!* They all automatically get the exact same permissions.

### Console Access & Account Alias
- **Console Access:** This means the user can log into the AWS Website (Management Console) using a username and password.
- **Account Alias:** AWS login URLs are usually long and ugly (e.g., `https://123456789012.signin.aws.amazon.com/console`). An Account Alias lets you create a friendly URL your team will actually remember! (e.g., `https://my-awesome-company.signin.aws.amazon.com/console`).

---

## 5. 🤖 Service Accounts (Bot Users)

### What is a Service Account?
Not everyone accessing your AWS account is a human! Sometimes, a script or an automation tool needs to talk to AWS. 
We call these **Service Accounts** (or Bot Accounts / Technical Users).

### Console Access? No!
Service accounts do **NOT** need to click around the AWS website. They don't have passwords. They communicate with AWS purely through code.

Instead of a username and password, Service Accounts use **Programmatic Access** via:
- **Access Key ID:** Think of this as the "bot username".
- **Secret Access Key:** Think of this as the "bot password".

### Used By:
- **Terraform / Ansible:** Tools that automate building servers.
- **Jenkins / GitHub Actions:** Tools that automatically deploy your code.
- **Python Scripts:** A script that automatically backups your database at midnight.

---

## 6. 📜 IAM Policies & Roles

### What is an IAM Policy?
A **Policy** is a plain JSON document that explicitly lists what actions are allowed or denied. 
*Example Policy logic:* "Allow this user to start an EC2 server, but DENY them from deleting it."

### What is an IAM Role?
A **Role** is similar to a user, but it is meant to be *assumable* temporarily. Roles do not have permanent passwords.

### The Real-World Difference
- **Policy:** The piece of paper (rulebook) that clearly states: "Can read files, cannot delete files."
- **Role:** A construction worker's "Hard Hat". 
  - An EC2 server can "put on the Hard Hat" (assume the role) to get temporary permission to read a database. When it takes the hat off, the permission is gone.

---

## 7. 🔑 Authentication vs Authorization

These two words sound similar but mean completely different things in security!

- **Authentication (AuthN):** *Who are you?*
  - Example: Showing your passport at the airport. Entering your username and password.
- **Authorization (AuthZ):** *What are you allowed to do?*
  - Example: Your boarding pass says you are in Economy class. You are *authenticated* to be on the plane, but you are not *authorized* to sit in First Class!

---

## 8. 🧾 Credential Reports & Security Best Practices

### What is a Credential Report?
A Credential Report is a downloadable Excel/CSV file from AWS. It lists every single IAM user in your account and tells you the status of their passwords and access keys.

### Why is Auditing Important?
In a real company, employees leave, or bot accounts are no longer needed. If you don't clean them up, hackers might find those old passwords and get into your AWS environment.

### Security Best Practices (The Golden Rules! ⭐)
1. **Never share the Root User password.**
2. **Enable MFA (Multi-Factor Authentication)** for all humans. It requires a code from your phone (like Google Authenticator) to log in.
3. **Delete inactive users.** If a developer quits, delete their IAM user immediately.
4. **Rotate Keys.** Change Service Account Access Keys every 90 days.

---

## 9. 💻 EC2 (Elastic Compute Cloud) Introduction

### What is EC2?
EC2 stands for **Elastic Compute Cloud**. It is AWS’s service for providing **Virtual Private Servers**. 

### Why do companies use it?
In the old days, companies had to buy physical hardware, wait weeks for it to be delivered, plug it in, and cool the room.
With EC2, you can rent a supercomputer in Germany, a web server in India, and a database in the USA—all with a few clicks! You pay only for the seconds you use it (Elastic). When you are done, you terminate it, and the billing stops instantly.

---

## 10. 🪟 Launching Windows Server on EC2

Let's get hands-on and launch a Windows computer in the cloud!

### Step-by-Step Guide
1. **Go to EC2 Dashboard:** Log into AWS and search for "EC2".
2. **Click "Launch Instance":** An instance is just a single virtual server.
3. **Name it:** E.g., `My-First-Windows-Server`.
4. **Choose an AMI (Amazon Machine Image):** This is the operating system. Select **Windows** -> **Windows Server 2025 Datacenter** (or 2022 if 2025 isn't available). Ensure it says "Free tier eligible".
5. **Instance Type:** Choose `t2.micro` or `t3.micro`. This determines the CPU and RAM. (Micro is free-tier!).
6. **Network/Security Group:** Allow **RDP (port 3389)** from "Anywhere" (0.0.0.0/0). *Note: In a real job, you would only allow your specific office IP!*
7. **Launch!** 🚀

---

## 11. 🔐 Key Pairs & Secure Access

Before AWS actually builds your server, it will ask for a **Key Pair**. 

### What is a Key Pair? (`.pem` file)
Because exposing passwords on the internet is dangerous, AWS uses cryptography. 
A key pair consists of two keys:
- **Public Key:** AWS puts this lock on your server.
- **Private Key (`.pem` file):** You download this to your personal laptop. It's the only key that can open the lock!

> ⚠️ **CRITICAL WARNING:** 
> You only get ONE chance to download the `.pem` file. If you lose it, you can NEVER log into that Windows server again! Guard it with your life.

---

## 12. 🖥️ Connecting to EC2 via RDP

Now that our Windows server is running in an Amazon data center, how do we see the screen?
Since it's Windows, we use **RDP (Remote Desktop Protocol)**.

### Steps to Connect:
1. Go to your EC2 instances list, select your Windows server, and click **Connect**.
2. Go to the **RDP Client** tab.
3. Click **Download Remote Desktop File**.
4. You need the Administrator password. Click **Get Password**.
5. Upload the `.pem` file you saved earlier and click **Decrypt Password**.
6. Open the downloaded RDP file, paste the decrypted password, and hit Connect!
7. 🎉 *Congratulations! You are now remotely controlling a Windows computer sitting in an Amazon data center!*

---

## 13. 🌍 Region Concept (Important)

### What is an AWS Region?
AWS has massive data centers all over the world. A Region is a physical geographical location in the world (e.g., `us-east-1` is in N. Virginia, USA; `ap-south-1` is in Mumbai, India).

### Why use the Mumbai region?
If your customers are in India, you should launch your EC2 servers in the Mumbai region (`ap-south-1`). Because the server is physically closer to the users, websites will load much faster (lower latency)!

### ⚠️ The Golden Rule of AWS Regions
- **IAM is GLOBAL.** When you create a user, they exist across the entire world simultaneously. You don't pick a region for IAM.
- **EC2 is REGIONAL.** If you launch a server in Mumbai, and then you change your AWS console view to London, your server disappears! (Don't panic, it's still in Mumbai, you just need to switch back).

---

## 14. 🏋️ Practice Tasks

*Want to be a true DevOps Engineer? Try completing these tasks without looking back at the guide!*

- [ ] Create an IAM Group called `Junior-Devs`.
- [ ] Create an IAM User named `Jane` and add her to the `Junior-Devs` group. Give her Console Access.
- [ ] Create a Service Account for "Jenkins" with Programmatic Access only. See if you can find the Access Key!
- [ ] Create an Account Alias to make your login URL pretty.
- [ ] Launch an EC2 Windows Server in a region closest to where you live.
- [ ] Decrypt the Windows password using your `.pem` key pair.
- [ ] Connect to the EC2 server using Remote Desktop (RDP).
- [ ] **Crucial Step:** When you are done practicing, **Terminate** (delete) the EC2 instance so AWS doesn't charge you money!

---

## 15. 🎤 Interview Questions

These are real questions asked in junior Cloud/DevOps interviews! Test yourself:

1. **Q: What is the difference between the Root user and an IAM user?**
   > **A:** The Root user has absolute, unrestricted access to the AWS account including billing and deleting the account. An IAM user is created by an administrator with specific, limited permissions for daily tasks.
2. **Q: Should developers use the Root user account for testing?**
   > **A:** Never! You should lock away the root account and use IAM users with least-privilege permissions.
3. **Q: What is the difference between Authentication and Authorization?**
   > **A:** Authentication verifies *who you are* (username/password). Authorization determines *what you are allowed to do* (IAM Policy).
4. **Q: What is an IAM Role and how does it differ from an IAM User?**
   > **A:** A User has permanent credentials (passwords/keys) meant for a long-term entity (like a human). A Role has temporary credentials and is meant to be assumed by AWS services (like an EC2 instance) to gain temporary permissions.
5. **Q: We have a Python script that needs to access an AWS database. Do we create a console password for it?**
   > **A:** No. We create a Service user with Programmatic Access using an Access Key ID and Secret Access Key.
6. **Q: What is a Policy?**
   > **A:** A JSON document that explicitly lists the allowed and denied permissions.
7. **Q: What is EC2?**
   > **A:** Elastic Compute Cloud. It is a service that provides scalable virtual servers in the cloud.
8. **Q: We launched an EC2 instance in `us-west-1`, but my colleague looking at `ap-south-1` cannot see it. Why?**
   > **A:** EC2 is a regional service. Servers only exist in the specific geographical region they were created in.
9. **Q: What happens if you lose your `.pem` key pair for an EC2 instance?**
   > **A:** You can no longer log in or decrypt the password for that specific instance. You must protect it carefully.
10. **Q: You need to ensure old employees who left 3 months ago don't still have AWS access. What tool helps you audit this easily?**
    > **A:** IAM Credential Report.

---

## 16. 📝 Summary

Here is your quick revision cheat sheet! 🔥

| Concept | Simple Definition | Key Detail |
| :--- | :--- | :--- |
| **IAM** | Identity & Access Management | Free service. Controls who/what accesses your AWS. **Global** scope. |
| **Root User** | The all-powerful account creator | Never use for daily tasks. Secure it with MFA! |
| **IAM User** | A human or bot account | Has a password for the console, or Keys for code. |
| **IAM Group** | A collection of users | Easiest way to manage permissions for a team. |
| **Policy** | The Rulebook (JSON) | Says exactly what is Allowed or Denied. |
| **Role** | Temporary "Hard Hat" | Assumed by services (like EC2) to get quick permissions without passwords. |
| **Service Account** | A bot user (Jenkins, Terraform) | Uses Access Key & Secret Key; no console access. |
| **AuthN vs AuthZ** | Authentication vs Authorization | AuthN = Who are you? AuthZ = What can you do? |
| **EC2** | Elastic Compute Cloud | Renting virtual servers. **Regional** scope. |
| **Region** | Physical world location | E.g., Mumbai, USA. Keep servers close to your users! |
| **Key Pair (.pem)**| Your super-secret server key | Never share it. Never lose it. Used to decrypt passwords. |
| **RDP** | Remote Desktop Protocol | The tool used to see the screen and control a Windows EC2 server. |

---
Prev : [11_aws_1.md](11_aws_1.md) | Next : [13_ELB_and_EC2.md](13_ELB_and_EC2.md)
---
