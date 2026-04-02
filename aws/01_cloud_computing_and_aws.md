# Cloud Computing & Introduction to AWS

---

### 2. What
**Cloud Computing** means using the internet to rent computers, storage, and databases from massive tech companies (like Amazon, Google, or Microsoft) instead of buying physical machines for your own house or office. 

**Amazon Web Services (AWS)** is the world's largest cloud provider. Netflix, Twitch, and Airbnb all run on AWS.

**Types of Cloud:**
- **Public Cloud:** Like a massive apartment building (AWS). Everyone rents their own isolated space, but you share the main building's water and power.
- **Private Cloud:** Like owning a private mansion. You own the physical servers completely.
- **Hybrid Cloud:** Connecting your private mansion to the public apartment building. Used by banks for high security + high scale.

**Service Models:**
- **IaaS (Infrastructure as a Service):** Renting the raw hardware.
- **PaaS (Platform as a Service):** Renting the platform. You upload code, they handle the OS setup.
- **SaaS (Software as a Service):** Renting the final product (e.g., Gmail, Slack).

✅ **Simple Analogy:**
Think of transportation:
- *On-Premise:* Buying your own car. You pay for gas, maintenance, and insurance.
- *IaaS:* Leasing a car. You drive it, but they own it.
- *PaaS:* Calling a Taxi. You just tell them the destination (code).
- *SaaS:* Taking a bus. Pre-set route, zero driving, you just ride.

---

### 3. Why
Before AWS, starting a tech company meant buying $50,000 worth of servers. If your app failed, you lost $50,000. If your app went globally viral overnight, your servers crashed. AWS introduced the **Pay-As-You-Go** model. You only pay for the exact seconds your computer is turned on. When you go viral, AWS automatically clones your server infinitely.

---

### 4. How
Instead of calling Dell to order a server and waiting 2 weeks, you open the AWS CLI (Command Line Interface), type a command, and within 30 seconds, a brand new Linux computer is booted up in a data center in London, ready for you to use.

---

### 5. Implementation

**Mini Exercise: IaaS vs PaaS logic in AWS**
While we will dive deep visually later, this is the mental model for accessing AWS:

```bash
# Using IaaS (AWS EC2 - Raw Server)
# You have to provide the exact Ubuntu image, size, and networking config manually.
aws ec2 run-instances --image-id ami-0abcdef12345 --count 1 --instance-type t2.micro --key-name MyKeyPair

# Using PaaS (AWS Elastic Beanstalk - Platform)
# You just tell AWS to create a Node.js environment. It handles the EC2 setup for you!
eb create my-node-env
```

---

### 6. Steps (Beginning your Journey)
1. **Understand your goal:** Are you building a website? You need Compute. Storing files? You need Storage.
2. **Shift your mindset:** Treat servers like cattle, not pets. If a server is acting buggy, you don't spend 5 hours fixing it. You destroy it and launch a brand new identical one in 10 seconds.
3. **Learn the CLI:** The web UI changes constantly. Terminal commands remain stable for decades.

---

### 7. Integration

🧠 **Think Like This:**
If you are building a React frontend and Node.js backend:
* **React:** Just static files. It does not need a heavy "IaaS" computer.
* **Node.js:** A live running script. It requires a dedicated "IaaS" Linux server or a "PaaS" environment to stay awake 24/7.

---

### 8. Impact
📌 **Real-World Scenario:** When Disney+ launched, 10 million people signed up on day one. Because they built their infrastructure on Cloud Computing, their systems auto-scaled to meet the insane demand magically, rather than crashing permanently. 

---

### 9. Interview Questions

Q1. Explain the difference between CapEx and OpEx in cloud computing.
Answer: CapEx (Capital Expenditure) is buying physical servers upfront. OpEx (Operational Expenditure) is the cloud model where you pay for compute by the hour as an ongoing operating cost.

Q2. What are the three main types of cloud deployments?
Answer: Public Cloud (shared resources via internet), Private Cloud (dedicated internal infrastructure), and Hybrid Cloud (a bridge between public and private).

Q3. Differentiate between IaaS, PaaS, and SaaS.
Answer: IaaS provides raw virtual hardware (like EC2). PaaS provides a managed code environment (like Elastic Beanstalk). SaaS provides a fully finished software product (like Gmail).

Q4. What is the primary financial advantage of using AWS?
Answer: The Pay-As-You-Go pricing model, which eliminates upfront hardware costs and allows businesses to scale costs precisely alongside user traffic.

Q5. If you only have raw code and don't want to manage Linux updates, which service model should you choose?
Answer: PaaS (Platform as a Service), because the cloud provider handles the underlying operating system and security patches automatically.

Q6. Why is AWS considered highly elastic?
Answer: Because it allows you to automatically provision thousands of servers when demand spikes, and instantly terminate them when demand drops, ensuring you only pay for what you use.

---

### 10. Summary
* Cloud computing replaces buying hardware with renting it over the internet.
* AWS is the leading cloud provider utilizing a Pay-As-You-Go model.
* IaaS gives you control; PaaS gives you convenience.
* Elasticity ensures your app survives viral traffic spikes.

---
Prev : [Start] | Next : [02_aws_global_infrastructure.md](./02_aws_global_infrastructure.md)
