# Scaling, Load Balancing, and Monitoring

---

### 2. What
- **Auto Scaling Groups (ASG):** AWS infrastructure that automatically increases or decreases the number of your running EC2 servers based on website traffic.
- **Elastic Load Balancer (ELB):** A traffic router. It sits in front of your servers and distributes incoming user traffic evenly across them so no single server is overwhelmed.
- **CloudWatch:** AWS's native monitoring service. It tracks CPU usage, memory, and aggregates logs.

---

### 3. Why
If you build a Node.js API on a single EC2 instance and your app goes viral, your single server will hit 100% CPU utilization and crash. If you implement an Auto Scaling Group, AWS will automatically launch 10 identical servers to handle the traffic. You must use a Load Balancer to evenly split the traffic among those 10 servers.

---

### 4. How
1. Create an **AMI (Amazon Machine Image)**: Take a blueprint snapshot of your perfectly configured Ubuntu server.
2. Provide that blueprint to the Auto Scaling Group. 
3. Attach the ASG to the Load Balancer.

---

### 5. Implementation

**CloudWatch Alerts via CLI**

```bash
# 1. Create a CloudWatch Alarm that triggers when CPU > 80%
aws cloudwatch put-metric-alarm \
    --alarm-name "High-CPU-Alarm" \
    --metric-name CPUUtilization \
    --namespace AWS/EC2 \
    --statistic Average \
    --period 300 \
    --threshold 80 \
    --comparison-operator GreaterThanThreshold \
    --dimensions Name=AutoScalingGroupName,Value=MyNodeASG \
    --evaluation-periods 2
    
# This alarm tells the Auto Scaling Group to launch more instances!
```

---

### 6. Steps (Designing a Scalable Architecture)
1. Set up an Ubuntu EC2 server, install Node.js and PM2.
2. Snapshot the server into an AMI.
3. Create a **Target Group** and an **Application Load Balancer (ALB)**.
4. Create an **Auto Scaling Group**, telling it to use the new AMI, and set Minimum capacity to 1, Maximum capacity to 10.
5. Create a CloudWatch Alarm measuring CPU utilization. Make it trigger a "Scale Out" action.

---

### 7. Integration

🧠 **Think Like This:**
* **Frontend:** If using React on S3 + CloudFront, you never need scaling groups! S3 natively scales infinitely.
* **Backend:** EC2 Node.js apps must use ASGs. 
* **Database:** Connect all 10 scaled EC2 servers to the single RDS PostgreSQL database independently. 

---

### 8. Impact
📌 **Real-World Scenario:** A retail clothing website normally needs 2 EC2 servers to handle standard Monday traffic. On Black Friday, the CPU spikes. CloudWatch detects this, triggers the Auto Scaling Group, and AWS provisions 50 identical EC2 instances to handle checkout traffic. After the sale ends, AWS deletes the 48 extra servers, saving the company thousands of dollars over the weekend.

---

### 9. Interview Questions

Q1. Contrast scaling vertically versus scaling horizontally.
Answer: Vertically scaling means upgrading a single server with more RAM and CPU (e.g., shifting from `t2.micro` to `m5.large`). Horizontally scaling means keeping the original server but launching multiple identical clones to distribute the load.

Q2. What is an Auto Scaling Group (ASG)?
Answer: A logical collection of EC2 instances that share similar characteristics, which AWS automatically scales up or down based on predefined CloudWatch metrics like CPU utilization or network traffic.

Q3. What is an Elastic Load Balancer (ELB)?
Answer: A service that automatically distributes incoming application traffic securely across multiple targets, such as distinct EC2 instances in multiple Availability Zones, to achieve high fault tolerance.

Q4. What is Amazon CloudWatch?
Answer: A monitoring and observability service that collects monitoring and operational data in the form of logs, metrics, and events across all AWS resources.

Q5. If you possess an Auto Scaling Group but no Load Balancer, what is the architectural flaw?
Answer: The Auto Scaling Group will clone and launch the instances, but end users will not be able to interact with the new servers because there is no load balancer actively routing internet traffic to the newly created private IP addresses.

Q6. Why is selecting multiple Availability Zones critical when hooking up a Load Balancer?
Answer: Because if the Load Balancer routes traffic to 10 servers located in a single Availability Zone, a data center electrical fire will still take out the entire application. The Load Balancer should distribute traffic across servers spanning multiple AZs.

---

### 10. Summary
* Vertical scaling is upgrading hardware; Horizontal scaling aligns perfectly with AWS ASGs.
* ELBs securely act as traffic directors.
* CloudWatch is the monitoring brain that triggers scaling alerts securely.
* Combining ASG + ELB + CloudWatch results in an uncrashable backend.

---
Prev : [11_devops_codepipeline_docker_ecs.md](./11_devops_codepipeline_docker_ecs.md) | Next : [13_best_practices_security_cost.md](./13_best_practices_security_cost.md)
