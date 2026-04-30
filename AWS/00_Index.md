# ☁️ Staff-Level AWS & Distributed Systems Curriculum

## 📚 Module Overview
This module covers 13 distinct domains:
1.  **Core Infrastructure**: VPCs, SDN, and Global Backbone.
2.  **Compute**: Nitro-powered EC2, Firecracker MicroVMs (Lambda), and Container Orchestration.
3.  **Storage**: S3 durability, EBS IOPS, and EFS consistency.
4.  **Databases**: Aurora quorum-based storage and DynamoDB partitioning.
5.  **Networking**: ALB/NLB internals, Route53 DNS, and Global Accelerators.
6.  **Security**: IAM Evaluation Logic, KMS Envelope Encryption, and Zero Trust.
7.  **Observability**: Distributed tracing (X-Ray) and high-resolution CloudWatch metrics.
8.  **DevOps**: IaC best practices and immutable deployment strategies.
9.  **Scaling & Reliability**: Event-driven architectures and Chaos Engineering.
10. **Internals Deep Dive**: The engineering secrets of Nitro, S3, and DynamoDB.

---

## 📂 Curriculum Map

### 🏗️ [Core](./Core/)
- [01 AWS Global Infrastructure](./Core/01_AWS_Global_Infrastructure.md)
- [02 Regions, AZs, and Edge Locations](./Core/02_Regions_AZs_Edge.md)
- [03 VPC Deep Dive](./Core/03_VPC_Deep_Dive.md)
- [04 Subnets and Routing](./Core/04_Subnets_Routing.md)
- [05 Security Groups vs NACLs](./Core/05_Security_Groups_vs_NACLs.md)
- [06 IAM Deep Dive](./Core/06_IAM_Deep_Dive.md)
- [07 Resource Tagging Strategy](./Core/07_Resource_Tagging_Strategy.md)
- [08 Service Quotas and Limits](./Core/08_Service_Quotas_and_Limits.md)
- [09 Cost Model and Billing](./Core/09_Cost_Model_and_Billing.md)

### 💻 [Compute](./Compute/)
- [01 EC2 Internals](./Compute/01_EC2_Internals.md)
- [02 Auto Scaling Groups](./Compute/02_Auto_Scaling_Groups.md)
- [03 Lambda Internals](./Compute/03_Lambda_Internals.md)
- [04 ECS vs EKS](./Compute/04_ECS_vs_EKS.md)
- [05 Fargate Deep Dive](./Compute/05_Fargate_Deep_Dive.md)
- [06 Bootstrapping and UserData](./Compute/06_Bootstrapping_and_UserData.md)
- [07 Instance Types and Performance](./Compute/07_Instance_Types_and_Performance.md)
- [08 Spot Instances](./Compute/08_Spot_Instances.md)

### 📦 [Storage](./Storage/)
- [01 S3 Internals](./Storage/01_S3_Internals.md)
- [02 S3 Consistency Model](./Storage/02_S3_Consistency_Model.md)
- [03 EBS vs EFS](./Storage/03_EBS_vs_EFS.md)
- [04 Glacier and Archival](./Storage/04_Glacier_and_Archival.md)
- [05 Data Lifecycle Policies](./Storage/05_Data_Lifecycle_Policies.md)
- [06 Storage Performance](./Storage/06_Storage_Performance.md)

### 🗄️ [Databases](./Databases/)
- [01 RDS Internals](./Databases/01_RDS_Internals.md)
- [02 Aurora Architecture](./Databases/02_Aurora_Architecture.md)
- [03 DynamoDB Internals](./Databases/03_DynamoDB_Internals.md)
- [04 Partitioning and Hot Keys](./Databases/04_Partitioning_and_Hot_Keys.md)
- [05 Transactions and Consistency](./Databases/05_Transactions_and_Consistency.md)
- [06 Read Replicas and Failover](./Databases/06_Read_Replicas_and_Failover.md)

### 🌐 [Networking](./Networking/)
- [01 ELB/ALB/NLB Internals](./Networking/01_ELB_ALB_NLB.md)
- [02 DNS and Route53](./Networking/02_DNS_Route53.md)
- [03 CDN and CloudFront](./Networking/03_CDN_CloudFront.md)
- [04 API Gateway Internals](./Networking/04_API_Gateway_Internals.md)
- [05 VPC Peering and PrivateLink](./Networking/05_VPC_Peering_and_PrivateLink.md)
- [06 NAT Gateway and Internet Access](./Networking/06_NAT_Gateway_and_Internet.md)
- [07 Hybrid Connectivity (VPN/DirectConnect)](./Networking/07_Hybrid_Connectivity_VPN_DirectConnect.md)
- [08 Connection Lifecycle](./Networking/08_Connection_Lifecycle.md)

### 🔐 [Security](./Security/)
- [01 IAM Policies Deep Dive](./Security/01_IAM_Policies_Deep_Dive.md)
- [02 KMS Internals](./Security/02_KMS_Internals.md)
- [03 Secrets Manager vs SSM](./Security/03_Secrets_Manager_vs_SSM.md)
- [04 Network Security](./Security/04_Network_Security.md)
- [05 Zero Trust on AWS](./Security/05_Zero_Trust_on_AWS.md)
- [06 Compliance and Auditing](./Security/06_Compliance_and_Auditing.md)

### 📊 [Observability](./Observability/)
- [01 CloudWatch Internals](./Observability/01_CloudWatch_Internals.md)
- [02 Distributed Tracing with X-Ray](./Observability/02_Distributed_Tracing_XRay.md)
- [03 Logging Strategies](./Observability/03_Logging_Strategies.md)
- [04 Alerting and SLOs](./Observability/04_Alerting_and_SLOs.md)

### 🚀 [DevOps](./DevOps/)
- [01 CI/CD Pipelines](./DevOps/01_CI_CD_Pipelines.md)
- [02 CloudFormation vs Terraform](./DevOps/02_CloudFormation_vs_Terraform.md)
- [03 Infrastructure as Code Best Practices](./DevOps/03_Infrastructure_as_Code.md)
- [04 Blue-Green and Canary Deployments](./DevOps/04_Blue_Green_and_Canary.md)
- [05 Deployment Failures and Rollbacks](./DevOps/05_Deployment_Failures.md)

### 📈 [Scaling](./Scaling/)
- [01 Vertical vs Horizontal Scaling](./Scaling/01_Vertical_vs_Horizontal.md)
- [02 Auto Scaling Groups Deep Dive](./Scaling/02_Auto_Scaling_Groups_Deep_Dive.md)
- [03 Predictive Scaling](./Scaling/03_Predictive_Scaling.md)
- [04 Caching Strategies](./Scaling/04_Caching_Strategies.md)
- [05 SQS and SNS Deep Dive](./Scaling/05_SQS_SNS_Deep_Dive.md)
- [06 Event-Driven Architecture](./Scaling/06_Event_Driven_Architecture.md)

### ⚡ [Performance](./Performance/)
- [01 Compute Performance Optimization](./Performance/01_Compute_Performance_Optimization.md)
- [02 Database Query Tuning](./Performance/02_Database_Query_Tuning.md)
- [03 Networking Latency Reduction](./Performance/03_Networking_Latency_Reduction.md)
- [04 Cost vs Performance Tradeoffs](./Performance/04_Cost_vs_Performance_Tradeoffs.md)

### 🛡️ [Reliability](./Reliability/)
- [01 High Availability Principles](./Reliability/01_High_Availability_Principles.md)
- [02 Disaster Recovery Strategies](./Reliability/02_Disaster_Recovery_Strategies.md)
- [03 Fault Tolerance Patterns](./Reliability/03_Fault_Tolerance_Patterns.md)
- [04 Chaos Engineering](./Reliability/04_Chaos_Engineering.md)
- [05 Incident Response](./Reliability/05_Incident_Response.md)

### 🔬 [Internals](./Internals/)
- [01 The Nitro System](./Internals/01_The_Nitro_System.md)
- [02 Firecracker MicroVMs](./Internals/02_Firecracker_MicroVMs.md)
- [03 S3 Bit Rot and Durability](./Internals/03_S3_Bit_Rot_and_Durability.md)
- [04 DynamoDB Paxos and Partitioning](./Internals/04_DynamoDB_Paxos_and_Partitioning.md)
- [05 Eventual Consistency in AWS](./Internals/05_Eventual_Consistency.md)

### 🏗️ [Projects](./Projects/)
- [01 Serverless Web App](./Projects/01_Serverless_Web_App.md)
- [02 Highly Available SQL Cluster](./Projects/02_Highly_Available_SQL_Cluster.md)
- [03 Data Processing Pipeline](./Projects/03_Data_Processing_Pipeline.md)
- [04 Multi-Region DR Setup](./Projects/04_Multi_Region_DR_Setup.md)
- [05 Build an Observability Platform](./Projects/05_Build_Observability_Platform.md)

---
**Prev: None | Index: [00_Index.md](./00_Index.md) | Next: [01_AWS_Global_Infrastructure.md](./Core/01_AWS_Global_Infrastructure.md)**
