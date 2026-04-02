# Security: IAM, Security Groups & Roles

---

### 2. What
AWS operates on a "Shared Responsibility Model". AWS secures the physical buildings. *You* must secure the software.
- **IAM (Identity and Access Management):** The master control panel defining Who can do What.
- **IAM Policies:** Tiny JSON documents defining exact permissions (e.g., "Allow deleting S3 files").
- **IAM Roles:** Hats that servers can wear. You give an EC2 instance an IAM Role so it can securely access other AWS services without needing passwords.
- **Security Groups (SG):** A virtual firewall attached to an EC2 instance or RDS Database. It strictly controls which port numbers can receive traffic.

✅ **Simple Analogy:**
- **IAM Users:** Physical ID badges given to human employees allowing them into the building.
- **IAM Roles:** A special contractor badge given to a robot (EC2 instance) allowing it to automatically enter a specific storage room (S3) without human intervention.
- **Security Group:** The bouncer at the door of the club checking if you are allowed to enter via Port 80 (HTTP) or Port 22 (SSH).

---

### 3. Why
If you hardcode your AWS Admin password directly into your Node.js code, and you accidentally push that code to GitHub, hackers will scrape it in seconds and spin up $50,000 worth of Bitcoin mining servers on your account. You must explicitly use IAM Roles so passwords never physically exist in your source code.

---

### 4. How
When you create a new AWS Account, you login as the **Root User**. The very first thing you do is create an **IAM User** with Admin access, securely log out of Root, and never use the Root account again.

---

### 5. Implementation

**Configuring a Security Group via CLI**

If you spin up an Ubuntu EC2 instance, you cannot actually view the website until you open Port 80!

```bash
# 1. Create a new Security Group Firewall
aws ec2 create-security-group \
    --group-name MyWebServerFirewall \
    --description "Allow HTTP and SSH"

# This outputs a Group ID, e.g., sg-0123456789abcdef

# 2. Add an Inbound Rule to allow global web traffic (Port 80)
aws ec2 authorize-security-group-ingress \
    --group-id sg-0123456789abcdef \
    --protocol tcp --port 80 --cidr 0.0.0.0/0

# 3. Add an Inbound Rule to allow YOU to SSH into the terminal (Port 22)
# PRO TIP: Replace 0.0.0.0/0 with your personal IP address for max security!
aws ec2 authorize-security-group-ingress \
    --group-id sg-0123456789abcdef \
    --protocol tcp --port 22 --cidr 0.0.0.0/0
```

---

### 6. Steps (Securing EC2 to S3 access)
Never put IAM User API keys in an `.env` file on an EC2 instance. Follow this exact flow:
1. Create an **IAM Policy** that explicitly allows "S3 PutObject" (Uploading).
2. Create an **IAM Role**.
3. Attach the Policy to the Role.
4. Attach the Role to the Ubuntu EC2 instance.
5. Your Node.js code can now magically upload photos to S3 via the SDK using the Role's ambient credentials flawlessly.

---

### 7. Integration

🧠 **Think Like This:**
* **Frontend:** Your React static S3 bucket requires a special **Bucket Policy** explicitly setting "Public Read Access", otherwise all users trying to view your website will get a 403 Forbidden error!
* **Backend:** Your RDS PostgreSQL database requires a Security Group explicitly attached to it that strictly allows Port 5432 Inbound traffic ONLY originating from the Security Group attached to your Node.js EC2 instance!

---

### 8. Impact
📌 **Real-World Scenario:** Capital One suffered a massive data breach where 100 million credit card applications were stolen. Why? A hacker found a vulnerability in an EC2 web server. Because the EC2 server was assigned an overly broad **IAM Role** with excessive permissions, the hacker used the server as a proxy to legally download the entire customer S3 database. Sticking to the "Principle of Least Privilege" explicitly prevents this entirely.

---

### 9. Interview Questions

Q1. Contrast an IAM User with an IAM Role.
Answer: An IAM User has permanent credentials (like a password and access keys) and usually represents a human. An IAM Role does not have permanent credentials; it is temporarily assumed by trusted entities like EC2 instances or Lambda functions.

Q2. What is the Principle of Least Privilege?
Answer: A security discipline stating that a user, role, or service should explicitly only be granted the absolute minimum permissions strictly necessary to perform its specific authorized task.

Q3. What is an AWS Security Group?
Answer: A virtual firewall that controls inbound and outbound traffic at the instance level. It evaluates rules based on IP addresses, protocols, and port numbers.

Q4. If your Node.js app running on an EC2 instance cannot connect to your RDS MySQL database, what is the most likely culprit?
Answer: The Security Group attached to the RDS instance does not have an inbound rule allowing TCP Port 3306 traffic from the EC2 instance's IP address.

Q5. Are Security Groups stateful or stateless?
Answer: Security Groups are stateful. If you send a request from your instance, the response traffic for that request is automatically permitted back in, regardless of your inbound security group rules.

Q6. Why should you never use the AWS Root Account for daily operational tasks?
Answer: Because the Root Account has absolute unrestricted access to every resource and billing setting in the account. If compromised, the attacker can hijack the entire account permanently.

---

### 10. Summary
* Use IAM Users for humans, Identity Roles for machines.
* Security Groups act as instance-level firewalls controlling exact port traffic.
* S3 Buckets require specific Bucket Policies to become publicly readable.
* Always enforce the Principle of Least Privilege globally.

---
Prev : [06_networking_vpc_route53_cloudfront.md](./06_networking_vpc_route53_cloudfront.md) | Next : [08_working_with_aws_cli_ec2.md](./08_working_with_aws_cli_ec2.md)
