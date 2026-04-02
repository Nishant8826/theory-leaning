# Working with AWS: CLI & EC2 Ubuntu Setup

---

### 2. What
To build things in AWS, you must communicate with their servers.
- **AWS Console:** The graphical user interface (GUI) website. Good for billing, terrible for speed.
- **AWS CLI (Command Line Interface):** A terminal tool you download. It allows you to create servers, upload files, and configure networking completely through code. 
- **SSH (Secure Shell):** The standard network protocol used to securely log into the terminal of a remote Linux computer (EC2 instance) across the internet.

✅ **Simple Analogy:**
- **AWS Console:** Walking into a restaurant and pointing at pictures on the menu.
- **AWS CLI:** Being the head chef and shouting exact commands at the kitchen staff to build the meal instantly.
- **SSH:** Teleporting your brain into a remote robot (EC2 server) in a different country, allowing you to use its hands.

---

### 3. Why
Cloud Engineers prefer the CLI over the UI because UIs change constantly. Buttons get moved every year. Terminal commands remain identical for decades. Furthermore, CLI commands can be saved into scripts to automate massive deployments instantly. Learning how to SSH into a raw Ubuntu instance is the core rite of passage for all backend developers.

---

### 4. How
1. Install the AWS CLI on your local MacOS/Windows laptop.
2. Go to the AWS Console, click IAM, and generate an **Access Key ID** and **Secret Access Key**.
3. Run `aws configure` in your terminal and paste those keys. Your computer is now permanently authenticated with AWS!

---

### 5. Implementation

**Deploying your first app on an Ubuntu EC2 Instance**

Assume you already generated your `MyUbuntuKey.pem` and used `aws ec2 run-instances` from Phase 2. AWS gave you a Public IP: `54.123.45.67`.

```bash
# 1. SSH into the raw blank Ubuntu server from your local laptop
# Note: "ubuntu" is the strictly default username for all Ubuntu AMIs.
ssh -i "MyUbuntuKey.pem" ubuntu@54.123.45.67

# --- YOU ARE NOW INSIDE THE REMOTE SERVER! ---

# 2. Update the Linux package manager securely
sudo apt-get update

# 3. Install Node.js natively
sudo apt-get install -y nodejs npm

# 4. Create a tiny quick Express app
mkdir my-api && cd my-api
npm init -y
npm install express
echo "const express = require('express'); const app = express(); app.get('/', (req, res) => res.send('Hello from AWS!')); app.listen(80, () => console.log('Live'));" > index.js

# 5. Run the app on Port 80 (Requires sudo to bind to low ports!)
sudo node index.js

# --- You can now visit http://54.123.45.67 in your browser! ---
```

---

### 6. Steps (Post-Deployment Best Practices)
1. **PM2:** Never run `node index.js` in production. When you close the SSH terminal session, the Node server will die. Instead, run `sudo npm install -g pm2`, and execute `pm2 start index.js`. PM2 keeps the server alive forever in the background!
2. **Reverse Proxy:** Industry standard dictates running your Node.js app on port `3000`, and installing **Nginx** to listen on Port `80` to safely proxy the traffic internally to Node.

---

### 7. Integration

🧠 **Think Like This:**
* The raw CLI gets you a blank Ubuntu server.
* SSH allows you to remotely control that blank server.
* Once inside, you treat that remote server exactly like you treat your local MacOS/Linux terminal. You install Git, clone your project repository directly onto the server, run `npm install`, and start the app!

---

### 8. Impact
📌 **Real-World Scenario:** By mastering the CLI, Senior Engineers can write a single 10-line bash script that generates 5 identical Ubuntu servers, installs Nginx, clones the GitHub repository, and starts the PM2 cluster simultaneously across 3 countries in under 60 seconds without ever touching a mouse.

---

### 9. Interview Questions

Q1. What is the AWS CLI?
Answer: The AWS Command Line Interface is a unified open-source tool that allows users to seamlessly interact securely with all AWS services programmatically via terminal commands.

Q2. What specific configuration command is required to authenticate your local computer with your AWS account?
Answer: You must run `aws configure`, which prompts you to input your IAM Access Key, Secret Access Key, default geographic region, and output format.

Q3. What is SSH and why is it used in AWS?
Answer: Secure Shell is a cryptographic network protocol used to operate network services securely over an unsecured network. It is primarily used to securely log into and execute commands on remote EC2 Linux instances.

Q4. When attempting to SSH into your freshly launched Ubuntu EC2 instance, your terminal simply times out and freezes. Why?
Answer: The most likely culprit is that the Security Group attached to the EC2 instance does not have an Inbound Rule allowing TCP Port 22 (SSH) traffic.

Q5. By default, what is the standard administrative username required when connecting to an official Ubuntu AMI on EC2?
Answer: The username is strictly exactly `ubuntu`.

Q6. Why should you use a process manager like PM2 instead of running `node server.js` directly via SSH?
Answer: If you run a standard Node process directly, it attaches exclusively to your current terminal session cleanly. When you disconnect the SSH session, the Linux kernel terminates the Node process. PM2 daemonizes the process, running it permanently in the background.

Q7. Why does binding an application to Port 80 usually require `sudo` privileges on a Linux EC2 instance?
Answer: On UNIX-based operating systems, all ports below 1024 are restricted "privileged ports" that explicitly require root administrative access to bind to for security reasons.

---

### 10. Summary
* The AWS CLI is a powerful programmatic tool replacing visual clicks.
* Use `aws configure` to securely link your computer to AWS.
* Use `ssh` combined with your `.pem` key to remotely log into Ubuntu EC2 servers.
* Install Node.js, clone your code, and utilize PM2 to keep the app alive permanently.

---
Prev : [07_security_iam_roles_policies.md](./07_security_iam_roles_policies.md) | Next : [09_hosting_react_nextjs_apps.md](./09_hosting_react_nextjs_apps.md)
