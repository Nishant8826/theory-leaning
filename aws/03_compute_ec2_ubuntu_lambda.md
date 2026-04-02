# Compute: EC2, Lambda, and Beanstalk

---

### 2. What
"Compute" is the brain power. It executes your Javascript or Python code.
- **EC2 (Elastic Compute Cloud):** A raw Virtual Machine. You rent an empty box, choose an OS (always choose Ubuntu!), and install everything yourself.
- **AWS Lambda:** Serverless compute. You don't get a server. You just paste your Javascript function into AWS, and it runs exactly when needed, scaling infinitely.
- **Elastic Beanstalk:** A PaaS wrapper around EC2. You upload a `.zip` of your Node.js code, and it builds the EC2 Ubuntu server for you automatically.

✅ **Simple Analogy:**
- **EC2:** Buying land and building a custom house. Full control, high effort.
- **Beanstalk:** Buying a pre-built house. You just move the furniture (code) in.
- **Lambda:** A hotel room rented by the exact millisecond you sleep in it. It vanishes when you leave.

---

### 3. Why
Picking the right compute service changes your entire DevOps workflow.
Using EC2 implies you are comfortable using the terminal, managing Linux security patches, and configuring Nginx. Using Lambda means zero server maintenance, but you have to rewrite your architecture into tiny "microservices". 

---

### 4. How
For production standard backends, we use **Linux EC2 instances**. Specifically, **Ubuntu**, because 99% of open-source guides, forums, and apt-get package managers are optimized for Ubuntu.

---

### 5. Implementation

**Launching an Ubuntu EC2 Instance via CLI**

```bash
# 1. We must find the standard Ubuntu Image ID (AMI) for our region.
# In us-east-1, Ubuntu 22.04 LTS might be ami-0c7217cdde317cfec (This changes frequently!)

# 2. Generate an SSH Key Pair so we can securely log into it natively
aws ec2 create-key-pair --key-name MyUbuntuKey --query 'KeyMaterial' --output text > MyUbuntuKey.pem

# 3. Secure the key locally (Linux/Mac requirement)
chmod 400 MyUbuntuKey.pem

# 4. Launch the Ubuntu Server! (t2.micro is entirely Free Tier eligible!)
aws ec2 run-instances \
    --image-id ami-0c7217cdde317cfec \
    --count 1 \
    --instance-type t2.micro \
    --key-name MyUbuntuKey

# The CLI will return a massive JSON block with your new Instance ID and Public IP address!
```

---

### 6. Steps (To Host a Backend)
1. Use the CLI to provision an Ubuntu `t2.micro` EC2 instance.
2. Ensure you have your `MyUbuntuKey.pem`.
3. You will SSH into the server via terminal (covered deeply in Phase 3).
4. Once inside Ubuntu, you install Node.js and run your code!

---

### 7. Integration

🧠 **Think Like This:**
* **Node.js (Backend):** You can run an entire Express.js API on a single $5/month Ubuntu EC2 instance smoothly. 
* **Lambda:** Instead of a long-running Node Express server, imagine writing just 1 function: `resizeImage()`. You upload it to Lambda. When a user uploads a photo, it fires, resizes it, and shuts down, costing $0.000001.

---

### 8. Impact
📌 **Real-World Scenario:** A traditional bank uses massive EC2 instances to process steady, predictable daily transactions cleanly because they want full control over the Linux kernel for compliance. A modern startup uses Lambda functions for user sign-ups because traffic is unpredictable and they want $0 bills during quiet nights.

---

### 9. Interview Questions

Q1. Contrast EC2 with AWS Lambda.
Answer: EC2 is an Infrastructure-as-a-Service virtual machine requiring manual OS maintenance and running continuously. AWS Lambda is a serverless function-as-a-service that executes code purely on-demand without any underlying server management.

Q2. What is an AMI?
Answer: Amazon Machine Image. It is a pre-configured template containing an operating system (like Ubuntu 22.04) and sometimes pre-installed software used to boot up an EC2 instance.

Q3. What does the term "Elastic" mean in Elastic Compute Cloud (EC2)?
Answer: It refers to the ability to easily resize compute capacity up or down (scaling) based dynamically on the immediate demands of your application.

Q4. Why is Ubuntu highly recommended for EC2 instances instead of Amazon Linux or Windows?
Answer: Ubuntu has massive global community support, almost all Node.js/Python tutorials are written for it, and the `apt` package manager resolves dependencies robustly for open-source stacks.

Q5. What is the fundamental pricing difference between EC2 and Lambda?
Answer: EC2 charges you by the hour for the entire time the server is turned on, regardless of whether it receives traffic. Lambda bills you per request and per millisecond of compute time used.

Q6. If a junior developer finds EC2 too difficult to configure manually for a Node.js app, what alternative AWS compute service should they use?
Answer: AWS Elastic Beanstalk. It automatically provisions the EC2 instances, load balancers, and scaling configurations while letting the developer simply upload their code.

Q7. What is a `.pem` file referenced during EC2 creation?
Answer: It is an RSA Private Key file used to securely authenticate and SSH into the Linux instance from your local terminal instead of using traditional passwords.

---

### 10. Summary
* EC2 = Raw Virtual Machines (Servers). Most apps run on Ubuntu Linux here.
* Lambda = Serverless functions. Code executes on-demand perfectly.
* Elastic Beanstalk = PaaS platform that manages EC2 automatically.
* Use the CLI to spin up instances with SSH `.pem` keys dynamically.

---
Prev : [02_aws_global_infrastructure.md](./02_aws_global_infrastructure.md) | Next : [04_storage_s3_ebs.md](./04_storage_s3_ebs.md)
