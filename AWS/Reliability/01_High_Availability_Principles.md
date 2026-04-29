# 🛡️ High Availability Principles

## 📌 Topic Name
High Availability (HA): Multi-AZ, Redundancy, and Self-Healing

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Run your app in two different data centers so if one burns down, the other stays up.
*   **Expert**: High Availability is the **Elimination of Single Points of Failure (SPOF)**. It is a measure of how long a system remains functional during a failure. HA is achieved through **Redundancy** (running multiple copies), **Diversity** (placing copies in different AZs/Regions), and **Automated Failover**. A Staff engineer designs for "The Fallibility of Everything," ensuring that no single component (Database, Load Balancer, or Network Link) can bring down the entire system.

## 🏗️ Mental Model
Think of High Availability as a **Twin-Engine Airplane**.
- **Redundancy**: Having two engines.
- **Independence**: The fuel lines and electrical systems for the two engines are separate.
- **Failover**: If Engine 1 fails, Engine 2 can automatically handle the weight of the plane and keep it flying until it can land safely.

## ⚡ Actual Behavior
- **The "Three AZ" Rule**: For maximum HA, deploy across at least 3 Availability Zones. This ensures that even if one AZ fails, you still have 66% of your capacity and high availability (2 nodes) remaining.
- **SLA (Service Level Agreement)**: AWS services often have a 99.9% (3 nines) or 99.99% (4 nines) uptime guarantee. To reach 99.999% (5 nines), you almost always need a **Multi-Region** architecture.

## 🔬 Internal Mechanics
1.  **Health Checks**: The "Pulse" of HA. If the monitoring system doesn't receive a "Heartbeat," it assumes a failure.
2.  **Statelessness**: HA is significantly easier if the application doesn't store state locally. If Node A fails, Node B can immediately take over because the data is in a shared, highly available database (like Aurora).
3.  **Loose Coupling**: Using queues (SQS) between components. If the "Order Processor" fails, the "Order Receiver" keeps working, and the messages just wait in the queue.

## 🔁 Execution Flow (The HA Chain)
1.  **User**: Hits Route 53 (Global HA).
2.  **DNS**: Returns IPs for ALB nodes in 3 AZs.
3.  **ALB**: Distributes traffic to 6 EC2 instances (2 per AZ).
4.  **Database**: Primary is in AZ-1, Synchronous Standby is in AZ-2 (Multi-AZ).
5.  **Failure**: AZ-1 goes dark.
6.  **Response**: 
    - ASG detects 2 dead instances and launches new ones in AZ-2 and AZ-3.
    - RDS detects Primary is down and promotes Standby in AZ-2 to Primary.
    - ALB stops sending traffic to AZ-1.
7.  **Result**: System remains online with zero data loss.

## 🧠 Resource Behavior
- **Quorum**: In many distributed systems, a "Majority" (e.g., 2 out of 3) must agree for the system to remain functional.
- **RTO (Recovery Time Objective)**: How long it takes to recover (e.g., "Back in 5 minutes").
- **RPO (Recovery Point Objective)**: How much data you can afford to lose (e.g., "Last 1 minute of transactions").

## 📐 ASCII Diagrams
```text
      [ ROUTE 53 (Global) ]
               |
      [ ALB (Multi-AZ) ]
      /        |        \
[ AZ-1 ]    [ AZ-2 ]    [ AZ-3 ]
[ APP  ]    [ APP  ]    [ APP  ]
    \          |          /
    [ RDS PRIMARY / STANDBY ]
```

## 🔍 Code / IaC (Multi-AZ ASG)
```hcl
resource "aws_autoscaling_group" "ha_app" {
  # Spanning 3 AZs for High Availability
  vpc_zone_identifier = [
    aws_subnet.private_1a.id,
    aws_subnet.private_1b.id,
    aws_subnet.private_1c.id
  ]
  
  min_size         = 3 # At least one per AZ
  desired_capacity = 6 # Two per AZ
  max_size         = 12
  
  health_check_type = "ELB"
  # ...
}
```

## 💥 Production Failures
1.  **The "Single-AZ" Database**: You have 100 app servers in 3 AZs, but your database is only in AZ-1. AZ-1 fails, and even though your app servers are fine, they can't do anything because the database is dead.
2.  **The "Dependency" Outage**: Your app is highly available, but it calls an internal "Auth Service" that only runs in one AZ. When that AZ fails, your app can't authenticate users. **Staff Rule**: Your HA is only as good as your weakest dependency.
3.  **Poison Pill Message**: A malformed message in a queue causes the worker to crash. The message goes back to the queue and is picked up by another worker, which also crashes. This continues until the entire fleet is dead. **Solution**: Use Dead Letter Queues (DLQ).

## 🧪 Real-time Q&A
*   **Q**: What is the difference between Fault Tolerance and High Availability?
*   **A**: HA is about "Keeping it running" (maybe with a brief blip). Fault Tolerance is about "Zero interruption" (the user never knows anything happened). Fault Tolerance is much more expensive.
*   **Q**: Does Multi-AZ cost more?
*   **A**: Usually yes. You pay for more instances and for data transfer between AZs.

## ⚠️ Edge Cases
*   **Split Brain**: When two nodes both think they are the "Primary" and start writing different data to storage. Managed services like RDS prevent this.
*   **Soft Limits**: You try to scale out during an AZ failure, but you hit your EC2 Instance Quota for that region.

## 🏢 Best Practices
1.  **Design for "N+1" Redundancy**: Always have one more instance/node than you strictly need.
2.  **Automate Everything**: If a human has to "log in and fix it," it's not High Availability.
3.  **Test your Failover**: Regularly "kill" a database or an AZ to ensure the system recovers as expected.

## ⚖️ Trade-offs
*   **Multi-AZ**: High reliability, but higher cost and slight increase in network latency (inter-AZ).
*   **Single-AZ**: Lowest cost and lowest latency, but zero protection against a data center outage.

## 💼 Interview Q&A
*   **Q**: How do you design for "99.99%" availability on AWS?
*   **A**: 1. Deploy across **3 Availability Zones**. 2. Use a **Load Balancer** with health checks. 3. Use an **Auto Scaling Group**. 4. Use **Multi-AZ RDS** for the database. 5. Use **S3** for static assets. 6. Ensure all external dependencies are also highly available.

## 🧩 Practice Problems
1.  Configure an RDS instance for Multi-AZ and perform a manual failover. Observe the DNS change.
2.  Calculate the monthly downtime allowed for a "99.999%" SLA.
