# 🛠️ Project: Highly Available SQL Cluster

## 📌 Topic Name
Project: Deploying a Multi-AZ, Load-Balanced Relational Database Stack

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Set up a MySQL database that stays up even if a data center fails.
*   **Expert**: This project implements a **Traditional 3-Tier Web Architecture**. It focuses on **Stateful Availability** using **RDS Multi-AZ** and **Elastic Load Balancing**. It includes a private network topology with **NAT Gateways**, automated scaling via **ASGs**, and robust monitoring via **CloudWatch Alarms**.

## 🏗️ Architecture Overview
- **VPC**: 2 Public Subnets (for LBs), 2 Private Subnets (for Apps), 2 Data Subnets (for DBs).
- **Edge**: **ALB** in the public subnets.
- **App Tier**: **EC2 instances** in an **Auto Scaling Group** across 2 AZs.
- **Database Tier**: **Amazon RDS (PostgreSQL/MySQL)** in **Multi-AZ** configuration.
- **Security**: Security Groups layered to only allow traffic from the tier above.

## 📐 Architecture Diagram
```text
[ INTERNET ]
     |
 [  ALB  ] (Public Subnets)
     |
 [  ASG  ] (Private Subnets) --- [ NAT GATEWAY ] ---> [ INTERNET ]
     |
 [  RDS  ] (Data Subnets)
  (Primary in AZ1, Standby in AZ2)
```

## 🔍 Implementation Steps (Terraform)
1.  **VPC**: Create a VPC with 6 subnets across 2 AZs.
2.  **Network**: Deploy an IGW and two NAT Gateways (one per AZ).
3.  **Database**: Create an `aws_db_subnet_group` and an `aws_db_instance` with `multi_az = true`.
4.  **Compute**: Create a Launch Template for EC2 and an ASG with a Target Tracking scaling policy.
5.  **Traffic**: Create an ALB and a Listener that forwards traffic to the ASG's Target Group.

## 🔍 Code Snippet (Multi-AZ RDS)
```hcl
resource "aws_db_instance" "prod_db" {
  allocated_storage      = 100
  engine                 = "postgres"
  engine_version         = "14.7"
  instance_class         = "db.r6g.large"
  multi_az               = true # THE CORE OF THIS PROJECT
  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.db_sg.id]
  
  backup_retention_period = 7
  storage_encrypted       = true
}
```

## 💥 Production Considerations
1.  **Failover Time**: Expect a 60-120 second "blip" during an RDS failover. Ensure your application has **Retry Logic** in its DB connection pool.
2.  **Read Scaling**: If your app is read-heavy, add **Read Replicas** in both AZs to offload traffic from the Primary.
3.  **Patching**: Configure your **Maintenance Window** for a time of low traffic, as patching can occasionally trigger a failover.

## 💼 Interview Walkthrough
- **Q**: Why put the database in its own "Data Subnets"?
- **A**: For **Defense in Depth**. Even if an attacker compromises the web server in the private subnet, the database is still isolated. The database security group is configured to ONLY allow traffic on port 5432 from the app servers, and the NACLs provide an additional layer of protection at the subnet boundary.

## 🧩 Practice Problems
1.  Perform a "Reboot with Failover" on the RDS instance and measure how long the application is disconnected.
2.  Configure a CloudWatch Alarm to notify you if the "FreeStorageSpace" on the database falls below 10GB.

---
Prev: [01_Serverless_Web_App.md](../Projects/01_Serverless_Web_App.md) | Index: [Docker/00_Index.md](../00_Index.md) | Next: [03_Data_Processing_Pipeline.md](../Projects/03_Data_Processing_Pipeline.md)
---
