## 1. Scaling & Elasticity

**What is it?**
Scaling means adjusting your computing resources to handle changing workloads. 
- **Horizontal Scaling (Scale Out / In):** Adding more machines (servers) to share the load.
- **Vertical Scaling (Scale Up / Down):** Increasing the power (CPU, RAM) of an existing machine.

**Why do we need it?**
Traffic fluctuates. You don't want to overpay for idle servers when traffic is low, and you don't want your website to crash due to a lack of resources when traffic spikes.

**How does it work?**
Systems monitor resource usage (like CPU utilization). When it exceeds a threshold, automatic triggers can launch new instances (Horizontal) from an AMI, or administrators can schedule upgrades to larger server sizes (Vertical).

**What is the impact?**
- **Cost Efficiency:** Pay only for what you use.
- **Reliability:** Prevents downtime during high traffic.

**Real-world Analogy:**
- *Horizontal*: A busy restaurant hires more waiters.
- *Vertical*: A busy restaurant trains 1 waiter to carry twice as many plates.

**Production-Level Example:**
Netflix uses Horizontal Scaling to provision thousands of servers during evening peak hours and shutting them down gracefully late at night.

**ASCII Diagram:**
```text
Vertical Scaling              Horizontal Scaling
   [ Server ]                     [ Server ]
       |                         /    |    \
 [ BIG SERVER ]        [Server] [Server] [Server] 
```

**Common Mistakes Beginners Make:**
- Relying entirely on Vertical Scaling, which eventually hits a hardware ceiling limit.
- Scaling out (horizontally) but forgetting to set up scaling *in*, leading to massive unexpected AWS bills.

---

## 2. EC2 (Elastic Compute Cloud)

**What is it?**
EC2 is a virtual server in AWS. It allows you to rent computing power in the cloud instead of buying physical hardware.

**Why do we need it?**
To run web applications, host databases, or process data without the upfront cost and maintenance of physical servers.

**How does it work?**
You select an Operating System, allocate hardware (RAM/CPU based on Instance Types like `t2.micro` or `m5.large`), and launch it. AWS reserves a slice of their massive physical servers just for you in seconds.

**What is the impact?**
Drastically reduces the time to market. Developers can instantly provision environments globally, tearing them down when finished.

**Real-world Analogy:**
Renting a car. You choose the car type (Instance Size), drive it to your destination (Compute), and return it when you're done, completely skipping maintenance and insurance (Server management).

**Production-Level Example:**
Hosting a backend Node.js API on an EC2 instance to serve mobile application requests.

**Common Mistakes Beginners Make:**
- Selecting instance types that are too large, wasting money.
- Losing the `.pem` / `.ppk` SSH keys, permanently losing secure access to their instance.
- Leaving all Ports (`0.0.0.0/0`) open in Security Groups, making the server a target for hackers.

---

## 3. AMI (Amazon Machine Image)

**What is it?**
An AMI is a pre-configured template (snapshot) used to create EC2 instances. It contains the Operating System setup, configurations, and pre-installed software.

**Why do we need it?**
If you need to horizontally scale to 10 servers, manually installing software on each one is slow and error-prone. AMIs allow you to duplicate a perfect server instantly.

**How does it work?**
Once you customize an EC2 instance with your app and dependencies, you create an AMI from it. In the future, every new server is launched specifically referencing this AMI ID, making them identical clones.

**What is the impact?**
Guarantees consistent environments (reducing "it works on my machine" bugs), dramatically speeds up boot times during auto-scaling, and serves as an excellent backup strategy.

**Real-world Analogy:**
A cookie cutter. Instead of shaping every cookie individually, you press the cutter to stamp out perfect, identical cookies.

**Production-Level Example:**
A company creates a "Golden AMI" every month containing the latest OS patches and security agents. All development teams are required to build on top of this Golden AMI.

**Common Mistakes Beginners Make:**
- Hardcoding sensitive data like passwords or API keys inside an AMI. Anyone who launches an instance from it can extract the secrets.
- Creating an AMI and never updating it, leading to future security vulnerabilities.

---

## 4. Load Balancer (ELB)

**What is it?**
A Load Balancer distributes incoming web traffic evenly across multiple server instances.

**Why do we need it?**
To ensure no single server is overwhelmed by request load, and to provide a single entry point (like `www.myapp.com`) for end-users, hiding the complex network of backend servers.

**How does it work?**
It sits between the user and your servers. Often using a Round Robin algorithm, it directs the first user to Server A, the next to Server B, and so on. Crucially, it uses "Health Checks" to constantly ensure a server is responsive before sending traffic.

**What is the impact?**
- **High Availability:** If a server crashes, the ELB routes around it without the user noticing.
- **Fault Tolerance & Seamless Scaling.**

**Real-world Analogy:**
A traffic cop at a busy intersection directing cars into multiple empty lanes so traffic flows smoothly.

**Production-Level Example:**
Using an Application Load Balancer to route traffic depending on the URL path: `/api/` goes to the backend server group, and `/images/` goes to a dedicated media server group.

**ASCII Diagram:**
```text
                  [User Request]
                        |
               [ Load Balancer ] 
               /        |        \
       [Server 1]   [Server 2]   [Server 3 (CRASHED)] 
                            (Traffic avoids Server 3 due to Health Checks)
```

**Common Mistakes Beginners Make:**
- Failing to configure Health Checks. If the Load Balancer blindly sends traffic to a dead instance, users will get errors.
- Placing the Load Balancer and the EC2 instances in misconfigured Security Groups so the Load Balancer is blocked from communicating with the servers.

---

## 5. Practical Implementation Outline

### Steps Performed
1. **Created EC2 Instances:** Launched Amazon Linux nodes.
2. **Connected & Secured:** Used SSH keys (via MobaXterm).
3. **App Installation:** `yum install nginx -y`
4. **Service Start:** `systemctl start nginx` && `systemctl enable nginx`
5. **Configuration:** Modified website content at `/usr/share/nginx/html/index.html`
6. **Troubleshooting Checked:** Verified Port 80 in Security Groups to allow public access.

---

## 6. Scenario-Based Problems

### Scenario 1: The E-Commerce Holiday Rush
**Problem:** Your store runs on a single large EC2 instance. Black Friday hits and traffic spikes 10x. Your site goes offline. 
**Solution:** A single server (Vertical scaling) creates a single point of failure. The ideal architecture places an **Application Load Balancer** in front of an Auto Scaling Group. As traffic builds, AWS spins up multiple new instances using a custom **AMI** to handle the load horizontally.

### Scenario 2: The Phantom 502 Error
**Problem:** Users occasionally get an error screen, but when they refresh, it works perfectly. You have 3 EC2 instances behind a Load Balancer.
**Solution:** One of your three servers has crashed or the application died. However, the Load Balancer is unaware because **Health Checks** were not configured properly. The Load Balancer keeps sending 1/3rd of the traffic to the dead server. Configuring a health check on `index.html` solves this immediately.

---

## 7. Interview Questions & Answers

### Q1: Can a running EC2 instance be vertically scaled?
**Answer:** No, vertical scaling requires the instance to be stopped first. Once stopped, the instance type can be modified (e.g., from `t2.micro` to `m5.large`), and then it can be restarted.

### Q2: What is the main difference between horizontal and vertical scaling?
**Answer:** Vertical scaling upgrades the resources of a single machine and has limits due to hardware maximums, causing brief downtime during the upgrade. Horizontal scaling adds completely new machines to distribute the load, offering virtually unlimited capacity without downtime.

### Q3: Why is Port 80 and 443 important in an EC2 Security Group?
**Answer:** Port 80 allows unencrypted HTTP traffic (web browsing), and Port 443 allows encrypted HTTPS traffic. Web servers require these open to receive requests from the public.

### Q4: If an EC2 instance crashes, what happens to the default root volume data?
**Answer:** By default, when an EC2 instance is terminated, its root Elastic Block Store (EBS) volume deletes with it. Critical data should be kept on external databases or independent EBS volumes.

### Q5: What is a Load Balancer Health Check?
**Answer:** A health check is an automated ping or request sent by the Load Balancer to an instance (like asking for an HTTP 200 OK from an `/index.html` page). If the instance doesn't respond correctly, the ELB marks it "Unhealthy" and stops sending traffic there.
