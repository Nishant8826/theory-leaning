# 🛠️ Project: Multi-Region DR Setup

## 📌 Topic Name
Project: Architecting for Regional Survival: Pilot Light with Aurora Global Database

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Set up a backup version of your entire application in a different part of the country for a total disaster.
*   **Expert**: This project implements a **Pilot Light Disaster Recovery Strategy**. It uses **Aurora Global Database** for near-zero RPO data replication and **Route 53 Failover Routing** for automated traffic redirection. The primary region (Active) runs the full stack, while the secondary region (Passive) has the data ready but the compute (ASGs) scaled down to zero to save costs.

## 🏗️ Architecture Overview
- **Primary (Region A)**: Fully functional ALB, ASG, and Aurora Primary Cluster.
- **Secondary (Region B)**: Aurora Global Read Replica. ASG is at `min=0`.
- **Data**: **S3 Cross-Region Replication** for static assets.
- **Traffic**: **Route 53** with a **Failover Routing Policy** and an **Active-Passive** health check.

## 📐 Architecture Diagram
```text
      [ USER ]
          |
   [ ROUTE 53 DNS ]
    /            \
[ REGION A ]      [ REGION B ]
(Active)          (Passive / Pilot Light)
[ ALB ]           [ ALB ]
[ ASG (3) ]       [ ASG (0) ]
[ AURORA PRI ] --(Repl)--> [ AURORA REPLICA ]
```

## 🔍 Implementation Steps (Terraform)
1.  **Global Data**: Create an `aws_rds_global_cluster`.
2.  **Primary**: Deploy an Aurora cluster in `us-east-1` attached to the global cluster.
3.  **Secondary**: Deploy an Aurora cluster in `us-west-2` attached to the same global cluster.
4.  **Compute**: Create identical VPCs and Launch Templates in both regions. Set ASG `desired_capacity = 0` in `us-west-2`.
5.  **Traffic**: Create two Route 53 A-records for the same name. Set one as Primary (with health check) and one as Secondary.

## 🔍 Code Snippet (Route 53 Failover)
```hcl
resource "aws_route53_record" "primary" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "api.myapp.com"
  type    = "A"
  
  failover_routing_policy {
    type = "PRIMARY"
  }

  set_identifier = "primary-region"
  health_check_id = aws_route53_health_check.primary_alb.id
  
  alias {
    name                   = aws_lb.primary_alb.dns_name
    zone_id                = aws_lb.primary_alb.zone_id
    evaluate_target_health = true
  }
}
```

## 💥 Production Considerations
1.  **Failover Automation**: Create a Lambda function that is triggered by the Route 53 health check failure. This Lambda should promote the Aurora replica and scale the secondary ASG from 0 to 3.
2.  **Testing**: Perform a "Game Day" where you simulate a regional outage by deleting the primary ALB. Verify that the system is back online in the secondary region within your RTO (e.g., 15 minutes).
3.  **Cost**: Remember that while you save on EC2 costs in the secondary region, you still pay for the RDS instances, S3 storage, and data transfer.

## 💼 Interview Walkthrough
- **Q**: Why choose "Pilot Light" over "Active-Active"?
- **A**: **Cost and Complexity**. Active-Active is extremely expensive because you pay for 100% of the resources in both regions. It also requires complex "Conflict Resolution" logic for the database. Pilot Light offers a great middle ground: low cost during normal operations, but a guaranteed recovery path (low RPO) during a major disaster.

## 🧩 Practice Problems
1.  Simulate a "Database Failover" in an Aurora Global cluster and measure the replication lag.
2.  Diagram the "Return to Primary" (Failback) process after a regional disaster is resolved.
