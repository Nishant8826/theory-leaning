# 🗄️ RDS Internals

## 📌 Topic Name
Amazon RDS: The Managed Relational Database Service

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: AWS manages your MySQL/Postgres/SQL Server database. No need to patch the OS.
*   **Expert**: RDS is a **Managed Database Automation Layer** built on top of EC2 and EBS. It provides an abstraction for high availability (Multi-AZ), automated backups, and software patching. Internally, RDS uses **Synchronous Block-Level Replication** for its Multi-AZ feature and asynchronous replication for Read Replicas.

## 🏗️ Mental Model
Think of RDS as an **Automated Car Mechanic**.
- **The Database Engine**: The car's engine (MySQL/PG).
- **RDS Service**: The mechanic who automatically changes the oil (Patching), backs up the car's data (Snapshots), and gives you a loaner car if yours breaks (Failover).

## ⚡ Actual Behavior
- **Multi-AZ**: When enabled, RDS creates a "Standby" instance in a different AZ. Every write to the "Primary" is synchronously replicated to the "Standby" at the storage level.
- **Backups**: RDS takes a full daily snapshot and continuously uploads transaction logs to S3, allowing for **Point-in-Time Recovery (PITR)** down to the second.

## 🔬 Internal Mechanics
1.  **Block-Level Replication**: Unlike MySQL's native "Binlog" replication, RDS Multi-AZ replicates raw disk blocks. This ensures that the Standby is a perfect physical clone of the Primary.
2.  **DNS Failover**: When the Primary fails, RDS updates the DNS CNAME of your database endpoint to point to the Standby's IP address. This typically takes 60-120 seconds.
3.  **The "Maintenance Window"**: A weekly time slot where RDS can apply OS or DB patches. You can postpone some patches, but critical security ones are mandatory.

## 🔁 Execution Flow (Write Operation in Multi-AZ)
1.  **App**: Sends `INSERT` to RDS Endpoint.
2.  **Primary**: Receives write, writes to local EBS.
3.  **Sync**: The block change is sent over the AWS network to the Standby AZ.
4.  **Standby**: Writes to its own EBS and sends an `ACK`.
5.  **Primary**: Returns success to the Application.

## 🧠 Resource Behavior
- **Storage Autoscaling**: RDS can automatically increase its EBS volume size if it's running out of space, preventing database downtime due to "Disk Full" errors.
- **Instance Types**: RDS uses standard EC2 instance families (e.g., `db.m5`, `db.r6g`).

## 📐 ASCII Diagrams
```text
      [ APPLICATION ]
             |
      [ RDS ENDPOINT ] (DNS CNAME)
             |
    +--------V--------+
    |  AZ-1 (PRIMARY) | <---(Sync Replication)---> |  AZ-2 (STANDBY) |
    |  [ DB Instance ]|                            |  [ DB Instance ]|
    |  [ EBS Volume  ]|                            |  [ EBS Volume  ]|
    +-----------------+                            +-----------------+
```

## 🔍 Code / IaC (Terraform)
```hcl
resource "aws_db_instance" "prod_db" {
  allocated_storage    = 100
  engine               = "postgres"
  engine_version       = "14.7"
  instance_class       = "db.r6g.large" # Graviton memory-optimized
  multi_az             = true
  db_name              = "mydb"
  username             = "admin"
  password             = var.db_password
  skip_final_snapshot  = false
  
  # Enabling Storage Autoscaling
  max_allocated_storage = 1000
}
```

## 💥 Production Failures
1.  **Replication Lag on Read Replicas**: High write volume on the Primary causes the asynchronous binlog replication to fall behind. Applications reading from the replica see "old" data, leading to confusing bugs.
2.  **Storage Full Crash**: If you don't enable storage autoscaling and the EBS volume hits 100%, the database will freeze and likely corrupt its logs, making recovery difficult.
3.  **The DNS TTL Issue**: During a failover, your application might have cached the old IP of the Primary. Even though RDS updated DNS, the app keeps trying to talk to a dead server. **Solution**: Use small JVM/OS DNS TTLs.

## 🧪 Real-time Q&A
*   **Q**: Can I access the underlying EC2 instance of RDS?
*   **A**: No. RDS is a "closed" service. If you need OS access, use **RDS Custom** or run your own DB on EC2.
*   **Q**: Does Multi-AZ improve read performance?
*   **A**: No. The Standby is "passive" and cannot be read from. For read performance, you need **Read Replicas**.

## ⚠️ Edge Cases
*   **Free Storage Limit**: RDS needs at least 10% free space to perform maintenance operations. If it's too full, patches will fail.
*   **Snapshot Performance**: Taking a snapshot on a Single-AZ instance causes a brief I/O suspension (milliseconds to seconds). In Multi-AZ, the snapshot is taken from the Standby, so the Primary is unaffected.

## 🏢 Best Practices
1.  **Use Multi-AZ** for all production databases.
2.  **Performance Insights**: Enable this to see exactly which SQL queries are causing load.
3.  **Secrets Manager**: Don't hardcode passwords; use Secrets Manager with automatic rotation.

## ⚖️ Trade-offs
*   **RDS vs. EC2**: Higher cost and less control vs. significant reduction in operational burden.
*   **Multi-AZ vs. Read Replicas**: High Availability (Sync) vs. Scalability (Async).

## 💼 Interview Q&A
*   **Q**: How does RDS handle a failure of the Primary instance?
*   **A**: It detects the failure (via health checks), promotes the Standby to Primary by making its storage "writable," and then updates the DNS record of the DB endpoint. The whole process is automated and usually finishes in under 2 minutes.

## 🧩 Practice Problems
1.  Enable "Performance Insights" and identify the "Top SQL" by load in a test RDS instance.
2.  Perform a manual failover (Reboot with Failover) and measure how long it takes for your application to reconnect.

---
Prev: [06_Storage_Performance.md](../Storage/06_Storage_Performance.md) | Index: [Docker/00_Index.md](../00_Index.md) | Next: [02_Aurora_Architecture.md](../Databases/02_Aurora_Architecture.md)
---
