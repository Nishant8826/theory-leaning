# 📈 Auto Scaling Groups (ASG)

## 📌 Topic Name
Auto Scaling Groups: Orchestrating Fleet Elasticity

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: ASG automatically adds or removes EC2 instances based on traffic.
*   **Expert**: An ASG is a **Declarative Fleet Manager**. It maintains a "Desired Capacity" of instances across multiple AZs. It is an event-driven system that reacts to **CloudWatch Alarms** or **Predictive Machine Learning** to adjust the fleet size. It also handles self-healing by replacing unhealthy instances automatically.

## 🏗️ Mental Model
Think of ASG as a **Thermostat**.
- **Set Point**: Desired Capacity (e.g., 5 instances).
- **Sensor**: CloudWatch Metrics (e.g., CPU > 70%).
- **Actuator**: EC2 `RunInstances` / `TerminateInstances` APIs.

## ⚡ Actual Behavior
ASG doesn't "watch" your instances directly. It receives signals.
- **Health Checks**: Can be EC2-based (is the VM alive?) or ELB-based (is the app returning 200 OK?).
- **Scaling Policies**:
    - **Target Tracking**: "Keep CPU at 50%." (Recommended)
    - **Step Scaling**: "If CPU > 70%, add 2. If CPU > 90%, add 5."
    - **Scheduled**: "Scale up at 9 AM Monday."

## 🔬 Internal Mechanics
1.  **AZ Rebalancing**: If one AZ has 3 instances and another has 1, ASG will try to rebalance them to ensure high availability.
2.  **Cooldown Period**: A safety delay after a scaling action to allow the new instances to warm up and the metrics to stabilize, preventing "thrashing" (rapidly scaling up and down).
3.  **Lifecycle Hooks**: Allows you to pause the launch or termination process. Useful for downloading code before service starts or draining logs before a server is killed.

## 🔁 Execution Flow (Scale Up)
1.  **Metric Breach**: CloudWatch Alarm fires (e.g., CPU > 70% for 3 minutes).
2.  **ASG Trigger**: ASG receives the alarm signal.
3.  **Launch Phase**: ASG calls `RunInstances` in the AZ with the fewest instances.
4.  **Health Grace Period**: ASG waits (e.g., 300s) for the instance to boot and app to start.
5.  **ELB Registration**: Instance is added to the Load Balancer Target Group.

## 🧠 Resource Behavior
- **Termination Policy**: By default, ASG protects instances in AZs with the fewest instances and then picks the one with the oldest Launch Configuration.
- **Instance Refresh**: A feature that allows you to roll out a new AMI across the whole fleet in a controlled manner (Canary/Blue-Green).

## 📐 ASCII Diagrams
```text
[ CloudWatch Alarm ] --- (Trigger) ---> [ Auto Scaling Group ]
                                              |
      +---------------------------------------+---------------------------------------+
      |                                       |                                       |
  [ AZ-1 ]                                 [ AZ-2 ]                                [ AZ-3 ]
  - EC2 (Running)                          - EC2 (Running)                         - EC2 (New!)
  - EC2 (Running)                          - EC2 (Running)
```

## 🔍 Code / IaC (Terraform)
```hcl
resource "aws_autoscaling_group" "app_asg" {
  desired_capacity    = 2
  max_size            = 5
  min_size            = 1
  vpc_zone_identifier = [aws_subnet.private_a.id, aws_subnet.private_b.id]

  launch_template {
    id      = aws_launch_template.app_lt.id
    version = "$Latest"
  }

  target_group_arns = [aws_lb_target_group.app_tg.arn]
  health_check_type = "ELB" # Use ELB health instead of just EC2
}

# Target Tracking Scaling Policy
resource "aws_autoscaling_policy" "cpu_scaling" {
  name                   = "cpu-target-tracking"
  autoscaling_group_name = aws_autoscaling_group.app_asg.name
  policy_type            = "TargetTrackingScaling"
  target_tracking_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ASGAverageCPUUtilization"
    }
    target_value = 50.0
  }
}
```

## 💥 Production Failures
1.  **Scaling Loop (Thrashing)**: Metric for scaling up is too sensitive, but the scale-down metric is too aggressive. The fleet constantly grows and shrinks, causing instability.
2.  **Launch Failure Overload**: The ASG tries to launch instances, but they fail (e.g., bad AMI or lack of capacity). ASG keeps trying indefinitely, which can lead to high "failed launch" logs and API throttling.
3.  **Zombie Instances**: ELB health check is failing, so ASG terminates the instance. A new one starts, fails again, and is terminated. This "death spiral" continues until you hit your bill limit.

## 🧪 Real-time Q&A
*   **Q**: Why should I use ELB health checks instead of EC2 health checks?
*   **A**: Because an EC2 instance can be "running" while the web server process (Nginx/Node) has crashed. ELB checks the app layer.
*   **Q**: What is a "Cooldown"?
*   **A**: It's the "wait time" to see if the previous scaling action fixed the problem before doing another one.

## ⚠️ Edge Cases
*   **Suspended Processes**: You can manually "suspend" ASG processes (like HealthCheck or ReplaceUnhealthy) for debugging. Don't forget to resume them!
*   **Subnet Capacity**: If your subnet has no more free IPs, ASG will fail to launch instances.

## 🏢 Best Practices
1.  **Use Launch Templates**: Launch Configurations are deprecated.
2.  **Termination Protection**: Enable for sensitive instances if needed, but rarely used in ASGs.
3.  **Multi-AZ**: Always span at least 2, ideally 3 AZs.

## ⚖️ Trade-offs
- **Warm Pools vs. Cost**: Keeping "pre-initialized" instances ready (Warm Pools) reduces scale-up time but costs more than cold starts.

## 💼 Interview Q&A
*   **Q**: How would you handle a stateful application in an ASG?
*   **A**: Use **Lifecycle Hooks** to ensure data is synced (e.g., to S3 or a DB) before the instance is terminated, and use **Instance Protection** to prevent the ASG from killing a specific instance that is currently processing a critical task.

## 🧩 Practice Problems
1.  Configure an ASG to use a "Spot-first" strategy, falling back to On-Demand only if Spot capacity is unavailable.
2.  Create a lifecycle hook that sends a Slack notification whenever an instance is about to be terminated.

---
Prev: [01_EC2_Internals.md](../Compute/01_EC2_Internals.md) | Index: [Docker/00_Index.md](../00_Index.md) | Next: [03_Lambda_Internals.md](../Compute/03_Lambda_Internals.md)
---
