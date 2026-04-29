# 📉 Spot Instances

## 📌 Topic Name
EC2 Spot Instances: Harnessing Excess Capacity for Massive Savings

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Use spare AWS capacity at a huge discount, but AWS can take it back anytime.
*   **Expert**: Spot Instances are a **Free-Market Auction for Spare Compute Capacity**. AWS prices fluctuate based on supply and demand in each AZ for each instance type. A Staff engineer uses Spot for **Stateless, Fault-Tolerant, or Time-Insensitive** workloads. The key to success with Spot is **Instance Diversification**—not being tied to a single instance type or AZ.

## 🏗️ Mental Model
Think of Spot as **Standby Flying**.
- **On-Demand**: A confirmed ticket. You pay full price, and the seat is yours.
- **Spot**: A standby ticket. You pay 10% of the price, but if a full-paying passenger (On-Demand user) shows up, you get kicked off the plane.

## ⚡ Actual Behavior
- **Price**: Can be up to 90% cheaper than On-Demand.
- **Interruption**: When AWS needs the capacity back, it sends a **2-minute warning** via the Instance Metadata Service (IMDS) and EventBridge.
- **Capacity Pools**: Every instance type in every AZ is a separate pool. `m5.large` in `us-east-1a` might be interrupted, while `m5.large` in `us-east-1b` is available.

## 🔬 Internal Mechanics
1.  **Spot Price Algorithm**: AWS no longer uses a literal bidding system. The price is determined by long-term supply/demand trends.
2.  **Interruption Signaling**: The `instance-action` field in IMDS changes from `null` to a JSON object containing the termination time.
3.  **Spot Fleet/ASG Integration**: ASG can manage a mix of On-Demand and Spot instances, automatically falling back to On-Demand if Spot is unavailable.

## 🔁 Execution Flow (Handling Interruption)
1.  **Poll**: Application or agent polls `http://169.254.169.254/latest/meta-data/spot/instance-action`.
2.  **Warning**: Field changes -> "You have 120 seconds."
3.  **Drain**: App stops accepting new connections, flushes logs to S3, and saves any state.
4.  **Terminate**: AWS reclaims the instance.

## 🧠 Resource Behavior
- **Persistence**: EBS volumes are NOT deleted on interruption (if configured correctly), but they are detached.
- **Allocation Strategy**: 
    - **Capacity Optimized**: Picks pools with the lowest risk of interruption. (Best for reliability)
    - **Lowest Price**: Picks the cheapest pool. (Best for cost)

## 📐 ASCII Diagrams
```text
[ AWS Capacity Pool ]
|-------------------|
| [ On-Demand ]     | <--- High Priority
| [ On-Demand ]     |
| [ Reserved ]      |
| [ ... ]           |
| [ SPOT (Free) ]   | <--- Low Priority (Your Instance)
|-------------------|
          |
    (Demand Spikes)
          |
[ Warning: 2 Mins ] --> [ App Drains ] --> [ Reclaimed ]
```

## 🔍 Code / IaC (Terraform)
```hcl
# ASG with a mix of Spot and On-Demand
resource "aws_autoscaling_group" "mixed_asg" {
  mixed_instances_policy {
    instances_distribution {
      on_demand_base_capacity                  = 1 # Always keep 1 OD instance
      on_demand_percentage_above_base_capacity = 0 # Everything else is Spot
      spot_allocation_strategy                 = "capacity-optimized"
    }

    launch_template {
      launch_template_specification {
        launch_template_id = aws_launch_template.app_lt.id
      }
      # Diversification: List multiple instance types
      override { instance_type = "m5.large" }
      override { instance_type = "m5d.large" }
      override { instance_type = "m4.large" }
    }
  }
}
```

## 💥 Production Failures
1.  **The "Single Pool" Mistake**: Using only one instance type (e.g., `c5.large`) in one AZ. If that pool is reclaimed, your entire service goes dark.
2.  **Ignoring the Warning**: App doesn't listen for the 2-minute warning. Transactions are cut mid-flight, leading to data corruption or "502 Bad Gateway" errors.
3.  **Stateful App on Spot**: Running a database on Spot without replication. The instance is reclaimed, and the DB goes offline for several minutes until a new one starts.

## 🧪 Real-time Q&A
*   **Q**: How often do interruptions happen?
*   **A**: Less than 5% of the time on average, but it depends on the pool. Use the **Spot Instance Advisor** to see the interruption frequency.
*   **Q**: Can I "bid" higher to stay online?
*   **A**: No. The "bid" is now just a maximum price you are willing to pay. If the market price exceeds your bid OR if AWS needs the physical capacity, you are interrupted regardless.

## ⚠️ Edge Cases
*   **Spot Blocks**: (Deprecated) Used to guarantee 1-6 hours of capacity. No longer available for new customers.
*   **Hibernate**: You can configure Spot to hibernate instead of terminate, saving the RAM state to EBS.

## 🏢 Best Practices
1.  **Be Flexible**: Use at least 2-3 AZs and 5+ instance types.
2.  **Handle Interruptions**: Use an agent or EventBridge to trigger a graceful shutdown.
3.  **Stateless only**: Perfect for Spark/Hadoop, CI/CD, and stateless web servers.

## ⚖️ Trade-offs
*   **Spot**: Massive cost savings but requires architectural resilience.
*   **On-Demand**: Predictable but expensive.

## 💼 Interview Q&A
*   **Q**: How do you make a web application "Spot-ready"?
*   **A**: 1. Ensure the app is stateless (state in Redis/DB). 2. Use an ASG with multiple instance types and AZs. 3. Implement a script that listens for the interruption signal and tells the Load Balancer to stop sending traffic to the instance before it dies.

## 🧩 Practice Problems
1.  Use the AWS CLI to find the current Spot price for `t3.large` in `us-east-1a`.
2.  Write a simple shell script that runs on an instance and logs a message to CloudWatch when a Spot interruption warning is detected.
