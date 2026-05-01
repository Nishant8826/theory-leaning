# 📌 Topic: Deploying Node.js to AWS EC2

## 🧠 Concept Explanation
Deploying to AWS EC2 (Elastic Compute Cloud) is the process of hosting your Node.js application on a virtual server in the Amazon cloud. It is the most "Raw" way to host in the cloud, giving you total control over the operating system, memory, and CPU.

**The Empty Apartment Analogy (Deep Dive):**
Imagine you are moving to a new city (The Cloud).
*   **Managed Hosting (Heroku/Vercel - The Hotel):** You check into a hotel. The room is furnished, the towels are clean, and there's a restaurant downstairs. You just show up and sleep.
    *   **The Catch:** It's expensive, and you can't paint the walls or change the furniture.
*   **AWS EC2 (The Empty Apartment):** You rent an empty space. 
    *   **The Setup:** You have to bring your own bed (Node.js), set up the Wi-Fi (Networking/VPC), and install the locks on the doors (Security Groups).
    *   **The Maintenance:** If a lightbulb breaks, you have to fix it. If the trash piles up (Log files), you have to take it out.
    *   **The Reward:** It's much cheaper for long-term stays, and you can customize it exactly how you want. You can turn the living room into a high-performance database or a massive file server.

---

## 🏗️ Mental Model
Think of EC2 as **Provisioning Virtual Hardware**.
1.  **The Instance (The Hardware):** Choosing the CPU/RAM combo (e.g., `t3.medium`).
2.  **The AMI (The Brain):** Choosing the OS (Ubuntu, Amazon Linux).
3.  **The Security Group (The Firewall):** Deciding who is allowed to talk to your server (e.g., "Only allow people on port 80").
4.  **The Lifecycle:** Unlike your laptop, an EC2 instance can be "Stopped" (paused) or "Terminated" (deleted forever).

---

## ⚡ Actual Behavior
When you deploy a Node.js app to EC2:
1.  **The SSH Tunnel:** You log in via a secure terminal. This is the only way to "talk" to the server's OS.
2.  **Process Persistence:** If you run `node app.js`, the app will die as soon as you close your terminal. You must use a "Process Manager" like **PM2**. PM2 acts as a 24/7 supervisor—if the app crashes, PM2 catches it and restarts it in milliseconds.
3.  **Port Mapping:** Node.js usually runs on port 3000 or 8080. However, the internet uses port 80 (HTTP) or 443 (HTTPS). You must either use a "Reverse Proxy" (Nginx) to bridge the gap or use AWS's Load Balancer.
4.  **Security Hardening:** By default, EC2 instances are targets for bots. Actual behavior involves changing default ports, disabling root login, and using SSH keys instead of passwords.

---

## 🔬 Internal Mechanics (V8 + libuv + OS)
*   **The Hypervisor (Nitro System):** Your "Server" isn't real. It's a slice of a much larger physical machine. AWS uses the Nitro Hypervisor to ensure that your Node.js process doesn't "leak" into another customer's space. This introduces a tiny amount of "Context Switching" overhead that you wouldn't see on a bare-metal server.
*   **EBS (Networked Storage):** On EC2, your "Hard Drive" is actually a separate server connected via a high-speed cable. When Node.js performs a `fs.readFile()`, the data travels over a specialized storage network. This means disk I/O is often slower than RAM but much more reliable (it survives if the EC2 instance crashes).
*   **The Linux Kernel and PM2:** PM2 uses the Linux `fork()` or `spawn()` system calls to create "Worker" processes. If you use PM2's "Cluster Mode," it uses the Node.js `cluster` module to distribute incoming TCP connections across all your CPU cores, bypassing the single-thread limit of V8.
*   **Entropy and Crypto:** Node.js uses `node:crypto` for things like JWT signing. In a virtual environment like EC2, the OS can sometimes "run out" of randomness (Entropy). AWS EC2 instances use specialized hardware (Nitro) to feed random numbers into the Linux `/dev/urandom` device, ensuring your encryption is always fast and secure.
*   **Elastic Network Interface (ENI):** Every EC2 has a virtual network card. When a request arrives, the OS kernel (Linux) handles the TCP handshake in the background before libuv "notifies" your Node.js code that a new connection is ready to be handled.

---

## 🔁 Execution Flow (Manual Deployment)
1.  Launch EC2 instance via AWS Console.
2.  Connect via SSH: `ssh -i key.pem ubuntu@1.2.3.4`.
3.  Update system: `sudo apt update && sudo apt upgrade`.
4.  Install Node.js via NVM.
5.  Clone repo: `git clone my-repo`.
6.  Install dependencies: `npm ci`.
7.  Start app with PM2: `pm2 start app.js`.
8.  Configure Security Group to allow traffic on port 80/443.

---

## 🧠 Resource Behavior
*   **Instance Types:** `t3.micro` (Burstable CPU, 1GB RAM) is good for small apps. `c5.large` (Compute Optimized) is better for high-traffic Node.js APIs.
*   **Disk:** AWS EBS (Elastic Block Store) provides persistent storage that is separate from the CPU.

---

## 📐 ASCII Diagrams
```text
[ USER ] --(HTTPS:443)--> [ SECURITY GROUP ] --(Port 3000)--> [ EC2 INSTANCE ]
                                                                     |
                                                               [ PM2 PROCESS ]
                                                               [ NODE.JS APP ]
```

---

## 🔍 Code Example (Latest Node.js - Using PM2 for Production)
```bash
# Install PM2 globally
npm install -g pm2

# Start the app in Cluster Mode (Utilize all CPUs)
pm2 start app.js -i max --name "my-api"

# Ensure PM2 starts on server reboot
pm2 startup
pm2 save

# View logs and monitoring
pm2 logs
pm2 monit
```

---

## 💥 Production Failures
*   **Forgetting to open Port 80:** Your app is running perfectly, but you can't see it in the browser because the Security Group is blocking traffic.
*   **Running as Root:** Running your Node app with `sudo`. If an attacker finds an RCE (Remote Code Execution) bug, they have full control over your entire server. (Solution: Use a non-privileged user).
*   **Disk Full with Logs:** PM2 logs grow forever and fill the disk. (Solution: Use `pm2-logrotate`).

---

## 🧪 Real-time Scenarios
*   **Single-Server MVP:** Getting a startup idea live in 10 minutes for $5/month.
*   **Legacy App Hosting:** Moving an old application that isn't Dockerized yet into the cloud.

---

## ⚠️ Edge Cases
*   **Instance Retirement:** Sometimes AWS needs to fix the underlying hardware and will force your instance to stop/restart. (Solution: Use an Auto-Scaling Group).
*   **In-Memory Storage:** If you save files to the EC2's local disk and the instance is terminated, those files are lost.

---

## 🏢 Best Practices
1.  **Use an Elastic Load Balancer (ELB):** Even for one instance. It handles SSL termination and makes scaling easier later.
2.  **Use Amazon Linux 2023:** It is optimized for AWS and has better security defaults.
3.  **Infrastructure as Code (IaC):** Use Terraform or CloudFormation instead of clicking buttons in the AWS Console.
4.  **Use Private Subnets:** Put your EC2 in a private subnet and only allow access through a Load Balancer or Bastion host.

---

## ⚖️ Trade-offs
*   **EC2:** Maximum control, cheap for steady load, but high management overhead (patches, security, scaling).
*   **Lambda (Serverless):** Zero management, scales to infinity, but "Cold Starts" and can be expensive for high-traffic steady loads.

---

## 💼 Interview Q&A
*   **Q:** What is a "Security Group" in AWS?
*   **A:** It acts as a virtual firewall for your EC2 instances to control incoming and outgoing traffic.

---

## 🧩 Practice Problems
1.  Launch a `t3.micro` instance and set up a Node.js server that is accessible via its Public IP.
2.  Write a simple `ecosystem.config.js` for PM2 that includes environment variables for `production`.

---
Prev: [../CI_CD/04_Deployment_Strategies.md](../CI_CD/04_Deployment_Strategies.md) | Index: [NodeJS/00_Index.md](../00_Index.md) | Next: [02_Serverless_Lambda.md](./02_Serverless_Lambda.md)
