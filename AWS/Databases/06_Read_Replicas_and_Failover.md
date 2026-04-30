# 🔄 Read Replicas and Failover

## 📌 Topic Name
Database Scalability and Resilience: Replicas and Automatic Failover

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Replicas help with reads; Failover helps with uptime.
*   **Expert**: Read Replicas and Failover are two distinct mechanisms for **Horizontal Scaling** and **Availability**. Read Replicas use **Asynchronous Replication** to offload read traffic from the Primary. Failover is a **Control Plane Operation** that promotes a standby/replica to Primary during a failure. A Staff engineer designs "Read-Through" or "Write-Through" patterns to handle the inherent lag in distributed database clusters.

## 🏗️ Mental Model
Think of Read Replicas and Failover as a **Restaurant Chain**.
- **The Primary**: The main kitchen that takes all orders (Writes).
- **The Replicas**: The counter staff who can only hand out ready-made food (Reads). They might be a few seconds behind the kitchen.
- **Failover**: If the main kitchen catches fire, the counter staff in the next building (Standby) is immediately promoted to "Main Kitchen" so orders can continue.

## ⚡ Actual Behavior
- **RDS (Replicas)**: Uses the engine's native asynchronous replication (e.g., MySQL Binlogs). Max 15 replicas.
- **Aurora (Replicas)**: Uses a shared storage volume. Replicas see the same data as the Primary with <20ms lag.
- **DynamoDB (Global Tables)**: Multi-Region, Multi-Active replication. You can write to any region, and changes replicate to all other regions in ~1 second.

## 🔬 Internal Mechanics
1.  **Replication Lag**: The time between a write on the Primary and its visibility on a Replica. In RDS, this is impacted by network latency and the load on the replica's CPU/Disk.
2.  **Aurora Failover**: Aurora uses a "Priority" system (Tier 0 to Tier 15). When the Primary fails, Aurora promotes the replica with the highest priority (Tier 0). If all priorities are the same, it picks an arbitrary one.
3.  **DNS Updates**: AWS manages the "Endpoint" DNS. During failover, the TTL (Time-To-Live) is usually 1 second, but client-side caching can still cause 30-60 seconds of downtime.

## 🔁 Execution Flow (Aurora Failover)
1.  **Detection**: AWS health checks detect the Primary is unresponsive.
2.  **Election**: The storage layer and control plane pick a Read Replica to promote.
3.  **Promotion**: The chosen Replica is rebooted and its role changed to "Writer."
4.  **DNS Swap**: The "Cluster Endpoint" DNS CNAME is updated to point to the new Writer's IP.
5.  **Reconnection**: Applications reconnect to the same endpoint and resume operations.

## 🧠 Resource Behavior
- **Write-after-Read Consistency**: If your app writes to the Primary and immediately tries to read from a Replica, it might see the old value. **Solution**: Use a "Read-Through" cache or ensure critical reads go to the Primary endpoint.
- **Instance Sizing**: Replicas should generally be the same size as the Primary to prevent them from falling behind during replication.

## 📐 ASCII Diagrams
```text
      [ APP ] --- (Writes) ---> [ CLUSTER ENDPOINT ]
                                       |
                   +-------------------+-------------------+
                   | (Write)                               |
          [ PRIMARY (AZ-1) ]                    [ REPLICA (AZ-2) ]
          (Role: Writer)   ---(Async Repl)--->  (Role: Reader)
                   |                                       |
      +------------+---------------------------------------+------------+
      |               SHARED STORAGE LAYER (AURORA)                  |
      +--------------------------------------------------------------+
```

## 🔍 Code / IaC (Terraform)
```hcl
# Aurora Read Replica (Cluster Instance)
resource "aws_rds_cluster_instance" "replica" {
  count              = 2
  identifier         = "replica-${count.index}"
  cluster_identifier = aws_rds_cluster.main.id
  instance_class     = "db.r6g.large"
  promotion_tier     = 1 # Higher priority for failover
}

# RDS MySQL Read Replica
resource "aws_db_instance" "mysql_replica" {
  replicate_source_db = aws_db_instance.primary.identifier
  instance_class      = "db.t3.medium"
  # No multi-az needed for a simple read replica
}
```

## 💥 Production Failures
1.  **Replica Lag Death Spiral**: A high-volume write on the Primary (like a bulk data load) causes 30+ minutes of lag on the Replica. The replica's CPU spikes as it tries to replay the logs, making it even slower.
2.  **Failover to Underpowered Replica**: The Primary is an `r6g.4xlarge`, but the Replica is a `t3.medium`. Failover happens, and the new Primary immediately crashes under the production load.
3.  **Split Brain**: Rare in managed services, but can happen in custom setups where two nodes both think they are the "Primary." AWS RDS/Aurora prevents this via its central control plane and storage quorums.

## 🧪 Real-time Q&A
*   **Q**: Can I have a Read Replica in another region?
*   **A**: Yes (Cross-Region Replica). This is great for Disaster Recovery and low-latency local reads for global users.
*   **Q**: How do I monitor replication lag?
*   **A**: Use the `ReplicaLag` metric in CloudWatch.

## ⚠️ Edge Cases
*   **Read-Only Mode**: When a replica is promoted to primary, it first needs to "unlock" its storage to allow writes. This is why Aurora failover is so fast (it doesn't have to mount a new disk).
*   **Binlog Format**: In RDS MySQL, using `ROW` based binlogs is more reliable but creates more replication traffic than `STATEMENT` based binlogs.

## 🏢 Best Practices
1.  **Match Instance Sizes**: Keep your Read Replicas (at least the failover target) the same size as your Primary.
2.  **Use Aurora** if you need low-latency replicas (<100ms lag) and fast failover (<30s).
3.  **Connection Pooling**: Use **RDS Proxy** to handle the influx of connections during a failover event.

## ⚖️ Trade-offs
*   **Replicas**: Cost money and add complexity but provide horizontal read scaling and improved availability.

## 💼 Interview Q&A
*   **Q**: What is the difference between an RDS Multi-AZ Standby and a Read Replica?
*   **A**: A Standby is for High Availability; it is synchronously replicated, has no endpoint, and cannot be read from. A Read Replica is for Scalability; it is asynchronously replicated and has its own endpoint for read queries.

## 🧩 Practice Problems
1.  Simulate a high-load scenario on an RDS instance and measure the replication lag on its replica.
2.  Configure an Aurora cluster with two replicas and perform a "manual failover." Observe which replica is promoted based on tiers.

---
Prev: [05_Transactions_and_Consistency.md](../Databases/05_Transactions_and_Consistency.md) | Index: [Docker/00_Index.md](../00_Index.md) | Next: [01_ELB_ALB_NLB.md](../Networking/01_ELB_ALB_NLB.md)
---
