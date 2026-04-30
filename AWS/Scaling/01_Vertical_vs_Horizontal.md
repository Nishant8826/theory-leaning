# 📈 Vertical vs. Horizontal Scaling

## 📌 Topic Name
Scaling Strategies: Size vs. Quantity

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Vertical scaling makes your server bigger; Horizontal scaling adds more servers.
*   **Expert**: Vertical scaling (**Scale Up**) involves increasing the compute, memory, or storage of a single instance. It is limited by hardware boundaries and typically requires downtime. Horizontal scaling (**Scale Out**) involves adding more nodes to a distributed system. It is the core of "Cloud Native" architecture, offering near-infinite scale and high availability, but requires the application to be **Stateless**.

## 🏗️ Mental Model
- **Vertical**: Getting a **Bigger Truck**. You can carry more weight, but if the truck breaks down, you can't deliver anything. Eventually, there is no bigger truck available on the market.
- **Horizontal**: Getting a **Fleet of Small Vans**. If one van breaks, the others keep moving. You can add 1,000 vans if you need to. But you need a "Dispatcher" (Load Balancer) to manage them.

## ⚡ Actual Behavior
- **Vertical**: Changing an `m5.large` to an `m5.4xlarge`. Requires a `Stop` and `Start` of the instance.
- **Horizontal**: Using an **Auto Scaling Group (ASG)** to increase the `DesiredCount` from 2 to 20. New instances are launched in parallel.
- **Managed Services**: 
    - RDS: Primarily Vertical (change instance type).
    - DynamoDB/Lambda/S3: Natively Horizontal (handled by AWS).

## 🔬 Internal Mechanics
1.  **Shared-Nothing Architecture**: For horizontal scaling to work, the application cannot store session data or state locally on the disk. State must be moved to an external database (RDS/DynamoDB) or cache (ElastiCache).
2.  **Graceful Shutdown**: When scaling in (removing nodes), the application must be able to finish current requests and save state before the instance is terminated.
3.  **Warm-up Time**: The time it takes for a new node to become ready (Booting OS + Starting App + Passing Health Checks).

## 🔁 Execution Flow (Scaling Out)
1.  **Detection**: CloudWatch Alarm fires: "Average CPU > 70%".
2.  **Trigger**: ASG receives the signal.
3.  **Launch**: ASG calls `RunInstances` API to create X new instances.
4.  **Register**: The new instances are automatically registered with the Target Group of the Load Balancer.
5.  **Traffic**: Once healthy, the Load Balancer begins sending requests to the new instances.

## 🧠 Resource Behavior
- **Vertical Limits**: The largest EC2 instance (`u-24tb1.metal`) has 24TB of RAM. If your DB needs 25TB, you MUST switch to a horizontal (sharded) architecture.
- **Scaling In**: AWS usually terminates the "Oldest" instance first or the one in the AZ with the most instances to maintain balance.

## 📐 ASCII Diagrams
```text
[ VERTICAL ]
[ Small Instance ] --(Change Type)--> [ HUGE INSTANCE ]
(Downtime required)

[ HORIZONTAL ]
[ Instance 1 ]       [ Instance 1 ] [ Instance 2 ] [ Instance 3 ]
[ Instance 2 ] ----> [ Instance 4 ] [ Instance 5 ] [ Instance 6 ]
(Zero downtime)
```

## 🔍 Code / IaC (Scaling Policy)
```hcl
# Horizontal Scaling Policy
resource "aws_autoscaling_policy" "cpu_target" {
  name                   = "target-tracking-cpu"
  autoscaling_group_name = aws_autoscaling_group.app_asg.name
  policy_type            = "TargetTrackingScaling"

  target_tracking_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ASGAverageCPUUtilization"
    }
    target_value = 50.0 # Keep CPU at 50%
  }
}
```

## 💥 Production Failures
1.  **The "Sticky Session" Trap**: You scale horizontally, but the Load Balancer is configured with "Sticky Sessions." All old users stay on Instance 1, which eventually crashes, while Instance 2-10 sit idle.
2.  **Database as the Bottleneck**: You scale your web tier to 1,000 instances, but they all connect to a single small RDS database. The database crashes under the connection load. **Solution**: Use Connection Pooling (RDS Proxy).
3.  **Local File Storage**: An app saves a user's uploaded image to the local `/tmp` folder. The user refreshes, hits a different instance (Scale out), and the image is "missing."

## 🧪 Real-time Q&A
*   **Q**: Can I vertically scale without downtime?
*   **A**: On some platforms yes, but on AWS EC2 it always requires a stop/start. Some RDS features allow for "Minimal Downtime" by using a standby.
*   **Q**: When is Vertical scaling better?
*   **A**: For legacy applications that are not "stateless" or for relational databases where sharding is too complex.

## ⚠️ Edge Cases
*   **Scale-In Protection**: You can mark specific instances in an ASG as "Protected" so they are never terminated during a scale-in event (useful for long-running jobs).
*   **Instance Refresh**: Automatically replacing all instances in an ASG with a new AMI, one by one, to ensure zero downtime.

## 🏢 Best Practices
1.  **Design for Horizontal First**: Always build stateless applications.
2.  **Target Tracking**: Use Target Tracking scaling policies instead of manual "Step" policies for a "set and forget" experience.
3.  **Instance Diversity**: Use multiple instance types in your ASG to avoid capacity issues in a single instance family.

## ⚖️ Trade-offs
*   **Vertical**: Simple, no code changes, but expensive and has a hard ceiling.
*   **Horizontal**: Highly resilient and infinite scale, but requires complex application design and a load balancer.

## 💼 Interview Q&A
*   **Q**: You have an application that is hitting its CPU limit. Should you make the instance bigger or add more instances?
*   **A**: If the application is **Stateless**, I would always prefer **Horizontal Scaling** as it provides better availability and cost-efficiency. If the application is **Legacy/Stateful**, I would scale **Vertically** as a short-term fix while planning a refactor to move the state out of the application tier.

## 🧩 Practice Problems
1.  Modify an ASG to use "Instance Refresh" and verify that a new AMI is deployed without dropping traffic.
2.  Compare the cost of 1 `m5.4xlarge` vs. 4 `m5.xlarge` instances.

---
Prev: [05_Deployment_Failures.md](../DevOps/05_Deployment_Failures.md) | Index: [Docker/00_Index.md](../00_Index.md) | Next: [02_Auto_Scaling_Groups_Deep_Dive.md](../Scaling/02_Auto_Scaling_Groups_Deep_Dive.md)
---
