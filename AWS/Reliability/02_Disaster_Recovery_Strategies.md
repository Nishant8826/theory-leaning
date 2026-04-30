# 🛡️ Disaster Recovery Strategies

## 📌 Topic Name
Disaster Recovery (DR): RTO, RPO, and Regional Failover

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Have a backup of your data in a different part of the country.
*   **Expert**: Disaster Recovery is the **Process of Restoring Service** after a catastrophic failure (e.g., an entire AWS region going offline). It is defined by two metrics: **RTO (Recovery Time Objective)**—how fast you need to be back up, and **RPO (Recovery Point Objective)**—how much data you can afford to lose. A Staff engineer chooses between four patterns: **Backup & Restore**, **Pilot Light**, **Warm Standby**, and **Multi-Site Active-Active**.

## 🏗️ Mental Model
Think of DR as **Backing up your House**.
- **Backup & Restore**: Taking a photo of your house and putting it in a safe. If the house burns down, you use the photo to build a new one from scratch (Slow, but cheap).
- **Pilot Light**: Keeping a small shed with a generator and some tools in another city. If the house burns down, you use the shed to quickly build a temporary house (Faster).
- **Warm Standby**: Keeping a small, identical house in another city. It's too small for everyone to live in, but it's ready. If the main house burns down, everyone moves in and you "expand" it (Fast).
- **Multi-Site (Active-Active)**: Having two full-sized identical houses in two different cities and people living in both. If one burns down, everyone just stays in the other one (Instant, but very expensive).

## ⚡ Actual Behavior
- **Backup & Restore**: RTO in hours, RPO in hours. Lowest cost.
- **Pilot Light**: RTO in tens of minutes, RPO in minutes. Data is replicated, but compute is off.
- **Warm Standby**: RTO in minutes, RPO in seconds. Compute is running at a small scale.
- **Active-Active**: RTO/RPO near zero. Traffic is served from both regions.

## 🔬 Internal Mechanics
1.  **Cross-Region Replication (CRR)**: S3 and RDS support automatic, asynchronous replication of data to another region.
2.  **Aurora Global Database**: Replicates data to up to 5 regions with <1 second latency using the storage layer, allowing for extremely low RPO.
3.  **Route 53 Health Checks**: Automatically redirects traffic from one region to another if the primary region's ALB stops responding.

## 🔁 Execution Flow (Pilot Light Failover)
1.  **Steady State**: Database is replicated to Region B. An AMI of the app server exists in Region B. No EC2s are running in B.
2.  **Disaster**: Region A goes offline.
3.  **Detect**: Route 53 health check fails.
4.  **Restore**:
    - Promote the RDS Read Replica in Region B to Primary.
    - Launch an ASG in Region B using the existing AMI.
5.  **Redirect**: Route 53 updates DNS to point to the new ALB in Region B.
6.  **Resolution**: Users are back online in < 30 minutes.

## 🧠 Resource Behavior
- **Global Tables (DynamoDB)**: Native Multi-Region, Multi-Active. You can write to any region, and it replicates to all others.
- **EBS Snapshots**: You must manually (or via DLM) copy snapshots to another region; they are not replicated automatically.

## 📐 ASCII Diagrams
```text
[ REGION A (Active) ] <---(Replication)---> [ REGION B (Standby) ]
        |                                           |
[ ROUTE 53 DNS ] -----------------------------------+
        |
    (If A Fails, Send to B)
```

## 🔍 Code / IaC (S3 Cross-Region Replication)
```hcl
resource "aws_s3_bucket_replication_configuration" "replication" {
  role   = aws_iam_role.replication_role.arn
  bucket = aws_s3_bucket.source.id

  rule {
    id     = "replicate-all"
    status = "Enabled"

    destination {
      bucket        = aws_s3_bucket.destination.arn
      storage_class = "STANDARD"
    }
  }
}
```

## 💥 Production Failures
1.  **The "Data Corruption" Replicator**: You have an Active-Active setup. A bug in your code starts deleting data in Region A. The deletion is immediately replicated to Region B. Now both regions are corrupted. **Solution**: Use **Point-in-Time Recovery (PITR)** and Versioning.
2.  **Out-of-Date AMIs**: You failover to Region B, but the AMI there is 6 months old and doesn't have the latest security patches or app code. The app crashes on launch. **Solution**: Automate AMI copying in your CI/CD pipeline.
3.  **Dependency Circularity**: Region B's failover process depends on a service that only exists in Region A. When A goes down, the "button" to failover to B doesn't work.

## 🧪 Real-time Q&A
*   **Q**: What is the difference between Multi-AZ and Multi-Region?
*   **A**: Multi-AZ protects against a single data center failure. Multi-Region protects against a total regional outage (e.g., an earthquake or a massive AWS backbone failure).
*   **Q**: Is Active-Active worth it?
*   **A**: Only for mission-critical applications where every second of downtime costs millions of dollars. It is extremely complex to manage data consistency (e.g., handling "split brain").

## ⚠️ Edge Cases
*   **Egress Costs**: Replicating terabytes of data between regions can be very expensive ($0.02 per GB).
*   **Regulatory Compliance**: Some data (like healthcare or financial records) cannot leave a specific country/region.

## 🏢 Best Practices
1.  **Define your RTO/RPO first**.
2.  **Automate the Failover**: Use a "Big Red Button" (Lambda or Step Function) to handle the promotion and DNS swap.
3.  **Practice "Game Days"**: Perform a full regional failover once a year to ensure your team and your code are ready.

## ⚖️ Trade-offs
*   **Backup & Restore**: Cheap, but high RTO (long downtime).
*   **Active-Active**: Zero RTO/RPO, but double the cost and extreme complexity.

## 💼 Interview Q&A
*   **Q**: How would you design a DR plan for a relational database with a 5-minute RPO?
*   **A**: I would use **Amazon RDS Cross-Region Read Replicas** or **Aurora Global Database**. This ensures that data is asynchronously replicated to the secondary region with less than 1 second of lag, well within the 5-minute RPO limit. For the failover, I would have a script that promotes the replica and updates the application's connection string.

## 🧩 Practice Problems
1.  Enable "Cross-Region Replication" for an S3 bucket and verify that a file uploaded to Region A appears in Region B.
2.  Calculate the annual cost of a "Warm Standby" architecture that uses 10% of the primary region's compute capacity.

---
Prev: [01_High_Availability_Principles.md](../Reliability/01_High_Availability_Principles.md) | Index: [Docker/00_Index.md](../00_Index.md) | Next: [03_Fault_Tolerance_Patterns.md](../Reliability/03_Fault_Tolerance_Patterns.md)
---
