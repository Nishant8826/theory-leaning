# 💰 Cost Model and Billing

## 📌 Topic Name
AWS Economics: Understanding the Physics of Cloud Spend

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: You pay for what you use. Turn things off to save money.
*   **Expert**: AWS cost is a three-dimensional vector: **Compute (Execution)**, **Storage (State)**, and **Networking (Movement)**. A Staff engineer doesn't just look at the total bill; they look at **Unit Economics** (e.g., cost per request). Understanding the nuances of "Data Transfer Out" vs "Inter-AZ Transfer" is what separates a senior engineer from a principal.

## 🏗️ Mental Model
Think of AWS Billing as a **Utility Bill (Electricity + Water)**.
- **Compute**: The lightbulbs (On-Demand, Spot, Savings Plans).
- **Storage**: The fridge (S3, EBS, RDS). Even if you don't eat the food, you pay for the cold air keeping it fresh.
- **Networking**: The delivery truck. Moving things *inside* the warehouse is cheap; shipping *outside* is expensive.

## ⚡ Actual Behavior
AWS uses a **Usage-Based Billing Model**. Usage is tracked in near-real-time by every service and aggregated into the **Cost and Usage Report (CUR)**.
- **Granularity**: Most compute is billed by the second (with a 60-second minimum).
- **Commitments**: You can trade "flexibility" for "price" using Savings Plans (SP) or Reserved Instances (RI).

## 🔬 Internal Mechanics
1.  **Data Transfer Pricing**:
    *   **Inbound**: Free (mostly). AWS wants your data.
    *   **Outbound to Internet**: Expensive ($0.05 - $0.09 per GB).
    *   **Inter-AZ**: $0.01 per GB.
    *   **Inter-Region**: $0.02 per GB.
2.  **Savings Plans vs. RIs**: Savings Plans are the modern standard. You commit to a $/hr spend (e.g., $10/hr) and AWS gives you a 30-70% discount. It applies automatically across instance families and regions (Compute SP).
3.  **Spot Instances**: Excess capacity sold at up to 90% discount. AWS can take them back with a 2-minute warning.

## 🔁 Execution Flow (Billing Cycle)
1.  **Resource Usage**: EC2 instance runs for 3600 seconds.
2.  **Metering**: Service sends "3600 seconds of m5.large" to the billing engine.
3.  **Pricing Engine**: Applies active Savings Plans, then Tiered Pricing (S3 gets cheaper as you store more), then Taxes.
4.  **Consolidated Billing**: Pushes the line item to the Management Account.

## 🧠 Resource Behavior
- **Orphaned Resources**: Deleting an EC2 instance does NOT delete its EBS volume or its Elastic IP. These continue to incur costs.
- **NAT Gateway**: You are billed per hour *and* per GB processed. This is often the #1 surprise cost in VPCs.

## 📐 ASCII Diagrams
```text
[ COST DRIVERS ]
       |
+------+------+------+
|   COMPUTE   |   STORAGE   |   NETWORKING   |
| (On-Demand) |  (GP3/IO2)  |  (Internet Out)|
|   (Spot)    |  (S3 tiers) |  (Inter-AZ)    |
|   (Lambda)  |  (Glacier)  |  (NAT Gateway) |
+------+------+------+------+----------------+
       |
[ BILLING DASHBOARD / CUR ]
```

## 🔍 Code / IaC (Terraform)
```hcl
# Using Budgets to prevent cost explosions
resource "aws_budgets_budget" "monthly_limit" {
  name              = "monthly-budget"
  budget_type       = "COST"
  limit_amount      = "1000"
  limit_unit        = "USD"
  time_period_start = "2023-01-01_00:00"
  time_unit         = "MONTHLY"

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 80
    threshold_type             = "PERCENTAGE"
    notification_type          = "ACTUAL"
    subscriber_email_addresses = ["admin@example.com"]
  }
}
```

## 💥 Production Failures
1.  **The "NAT Gateway Trap"**: A high-throughput service in a private subnet pulls 100TB from S3 via the NAT Gateway instead of a VPC Endpoint. Cost: $4,500 for the data transfer alone.
2.  **Snapshot Bloat**: Taking daily EBS snapshots and never deleting them. Over a year, the storage cost can exceed the compute cost.
3.  **Cross-Region Replication**: Accidentally enabling S3 replication for a bucket with petabytes of data, leading to a massive "Data Transfer Inter-Region" bill.

## 🧪 Real-time Q&A
*   **Q**: What is the most expensive part of AWS?
*   **A**: Usually **Data Transfer Out** or **Unmanaged NAT Gateways**.
*   **Q**: Does a stopped EC2 instance cost money?
*   **A**: The compute (CPU/RAM) stops billing, but you still pay for the EBS storage and any assigned Elastic IPs.

## ⚠️ Edge Cases
*   **Data Transfer between S3 and EC2**: Free if in the same region, but ONLY if you use private IPs or VPC Endpoints. If you use the public S3 endpoint, you might pay.
*   **Free Tier Limits**: "Free" doesn't mean "Unlimited." If you exceed 750 hours of t2.micro, you pay.

## 🏢 Best Practices
1.  **VPC Endpoints**: Always use them for S3 and DynamoDB.
2.  **Spot for Stateless**: Use Spot instances for CI/CD, batch processing, and stateless web tiers.
3.  **Compute Savings Plans**: The most flexible way to save on EC2, Fargate, and Lambda.

## ⚖️ Trade-offs
*   **On-Demand vs. Savings Plans**: On-demand is 100% flexible but 30%+ more expensive.
*   **GP2 vs. GP3**: GP3 is almost always cheaper and faster, as you can tune IOPS independently of size.

## 💼 Interview Q&A
*   **Q**: How would you architecture a high-traffic app to minimize data transfer costs?
*   **A**: 1. Use CloudFront (caching at edge). 2. Keep chatty services in the same AZ (risky) or minimize cross-AZ talk. 3. Use VPC Endpoints. 4. Compress data (Gzip/Brotli) before sending it over the wire.

## 🧩 Practice Problems
1.  Analyze a sample AWS bill (CUR) and identify the top 3 cost drivers.
2.  Calculate the cost difference between running 10 instances on On-Demand vs. 1-year Savings Plan vs. Spot.
