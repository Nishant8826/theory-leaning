# VPC Architecture & Design

> 📌 **File:** 23_VPC_Architecture_And_Design.md | **Level:** Full-Stack Dev → Networking Expert

---

## What is it?

A VPC (Virtual Private Cloud) is your isolated network in AWS — your own data center in the cloud. Every EC2, RDS, ElastiCache, and Lambda (in VPC mode) lives inside a VPC. Designing your VPC correctly determines security, availability, scalability, and cost of your entire infrastructure.

---

## Map it to MY STACK (CRITICAL)

```
Your laptop: connects via home router (192.168.1.x)
Your AWS: everything inside a VPC (10.0.x.x)

The VPC IS your infrastructure backbone.
Every networking concept we've covered converges here:
  - Subnetting (file 04) → VPC subnet design
  - Routing (file 10) → Route tables
  - NAT (file 10) → NAT Gateway
  - Security (file 12) → Security Groups, NACLs
  - Load Balancing (file 11) → ALB in public subnets
  - Database (file 22) → RDS in private subnets
```

---

## Production VPC Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│  VPC: 10.0.0.0/16 (us-east-1)                                      │
│                                                                      │
│  ┌────────── Availability Zone A ──────────┐  ┌────── AZ B ──────┐ │
│  │                                          │  │                   │ │
│  │  Public Subnet: 10.0.1.0/24             │  │ 10.0.2.0/24      │ │
│  │  ┌─────────┐  ┌────────────┐            │  │ ┌─────────┐     │ │
│  │  │  ALB    │  │NAT Gateway │            │  │ │  ALB    │     │ │
│  │  │ (node1) │  │            │            │  │ │ (node2) │     │ │
│  │  └─────────┘  └────────────┘            │  │ └─────────┘     │ │
│  │                                          │  │                   │ │
│  │  Private Subnet (App): 10.0.10.0/24     │  │ 10.0.11.0/24    │ │
│  │  ┌─────────┐  ┌─────────┐              │  │ ┌─────────┐     │ │
│  │  │  EC2    │  │  EC2    │              │  │ │  EC2    │     │ │
│  │  │ Node.js │  │ Node.js │              │  │ │ Node.js │     │ │
│  │  │ :3000   │  │ :3000   │              │  │ │ :3000   │     │ │
│  │  └─────────┘  └─────────┘              │  │ └─────────┘     │ │
│  │                                          │  │                   │ │
│  │  Private Subnet (Data): 10.0.20.0/24    │  │ 10.0.21.0/24    │ │
│  │  ┌─────────┐  ┌─────────┐              │  │ ┌─────────┐     │ │
│  │  │  RDS    │  │  Redis  │              │  │ │  RDS    │     │ │
│  │  │ Primary │  │ Primary │              │  │ │ Standby │     │ │
│  │  │ :5432   │  │ :6379   │              │  │ │ :5432   │     │ │
│  │  └─────────┘  └─────────┘              │  │ └─────────┘     │ │
│  │                                          │  │                   │ │
│  └──────────────────────────────────────────┘  └───────────────────┘ │
│                                                                      │
│  Route Tables:                                                       │
│  Public:  10.0.0.0/16 → local, 0.0.0.0/0 → IGW                   │
│  Private: 10.0.0.0/16 → local, 0.0.0.0/0 → NAT GW                │
│  Data:    10.0.0.0/16 → local (NO internet access)                 │
└──────────────────────────────────────────────────────────────────────┘
```

### Three-Tier Subnet Strategy

```
┌──────────────────────────────────────────────────────────────────┐
│  Tier       │ Subnet Type │ Internet  │ Contains               │
├─────────────┼─────────────┼───────────┼────────────────────────┤
│  Public     │ Public      │ In + Out  │ ALB, NAT GW, Bastion  │
│             │             │ (via IGW) │                        │
│             │             │           │                        │
│  App        │ Private     │ Out only  │ EC2 (Node.js),         │
│             │             │ (via NAT) │ ECS Tasks, Lambda      │
│             │             │           │                        │
│  Data       │ Isolated    │ None      │ RDS, ElastiCache,      │
│             │             │           │ DocumentDB             │
├─────────────┴─────────────┴───────────┴────────────────────────┤
│  Why 3 tiers:                                                   │
│  - Public: load balancer faces internet                        │
│  - App: servers need outbound (npm, APIs) but no inbound      │
│  - Data: databases need NO internet access at all              │
│  Each tier has its own route table and security group           │
└──────────────────────────────────────────────────────────────────┘
```

---

## Security Group Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  SG: sg-alb                                                    │
│  Inbound:  443 from 0.0.0.0/0 (HTTPS from internet)          │
│  Outbound: 3000 to sg-app                                      │
├─────────────────────────────────────────────────────────────────┤
│  SG: sg-app                                                    │
│  Inbound:  3000 from sg-alb (only from load balancer)         │
│  Inbound:  22 from sg-bastion (SSH from bastion only)         │
│  Outbound: 5432 to sg-data (PostgreSQL)                       │
│  Outbound: 6379 to sg-data (Redis)                            │
│  Outbound: 443 to 0.0.0.0/0 (external APIs, npm)             │
├─────────────────────────────────────────────────────────────────┤
│  SG: sg-data                                                   │
│  Inbound:  5432 from sg-app (PostgreSQL from app tier only)   │
│  Inbound:  6379 from sg-app (Redis from app tier only)        │
│  Outbound: None needed (data tier doesn't initiate connections)│
├─────────────────────────────────────────────────────────────────┤
│  SG: sg-bastion                                                │
│  Inbound:  22 from YOUR-IP/32 (SSH from your IP only)        │
│  Outbound: 22 to sg-app (SSH to app servers)                  │
│            5432 to sg-data (direct DB access for admin)        │
└─────────────────────────────────────────────────────────────────┘
```

---

## Multi-Region Architecture

```
Region: us-east-1 (Primary)              Region: eu-west-1 (DR / Low latency EU)
┌──────────────────────────┐              ┌──────────────────────────┐
│  VPC: 10.0.0.0/16        │              │  VPC: 10.1.0.0/16        │
│  ┌──────┐ ┌──────┐      │  VPC Peering │  ┌──────┐ ┌──────┐      │
│  │ ALB  │ │Node.js│     │◄────────────►│  │ ALB  │ │Node.js│     │
│  └──────┘ └──────┘      │  or Transit  │  └──────┘ └──────┘      │
│  ┌──────┐ ┌──────┐      │  Gateway     │  ┌──────┐ ┌──────┐      │
│  │ RDS  │ │Redis │      │              │  │ RDS  │ │Redis │      │
│  │Primary│ │      │      │              │  │Read  │ │      │      │
│  └──────┘ └──────┘      │              │  │Replica│ └──────┘      │
└──────────────────────────┘              └──────────────────────────┘
                │                                    │
                └──── Route 53 Latency-Based ────────┘
                      US users → us-east-1
                      EU users → eu-west-1

CIDR planning for multi-region:
  us-east-1: 10.0.0.0/16
  eu-west-1: 10.1.0.0/16
  ap-south-1: 10.2.0.0/16
  CIDRs MUST NOT overlap for VPC peering to work!
```

---

## VPC Endpoints (Saving Money + Security)

```
Without VPC Endpoint:
  EC2 → NAT Gateway → Internet → S3
  Cost: NAT Gateway data processing ($0.045/GB)
  Security: Traffic goes over the internet

With VPC Endpoint (Gateway):
  EC2 → VPC Endpoint → S3 (internal AWS network)
  Cost: FREE for S3 and DynamoDB gateway endpoints
  Security: Traffic stays within AWS network

┌──────────────────────────────────────────────────────────────────┐
│  Endpoint Type │ Services               │ Cost                  │
├────────────────┼────────────────────────┼───────────────────────┤
│  Gateway       │ S3, DynamoDB           │ FREE                  │
│  Interface     │ All other AWS services │ $0.01/hour + data    │
│                │ (SQS, SNS, ECR, Secrets│                       │
│                │  Manager, CloudWatch)  │                       │
├────────────────┴────────────────────────┴───────────────────────┤
│  Always create S3 and DynamoDB gateway endpoints.              │
│  They're free and save NAT Gateway costs.                       │
│  An app downloading 100GB/month from S3 via NAT = $4.50/month  │
│  saved with a free endpoint.                                     │
└──────────────────────────────────────────────────────────────────┘
```

---

## VPC Design Checklist

```
┌──────────────────────────────────────────────────────────────────┐
│  ✅ VPC Design Checklist                                        │
├──────────────────────────────────────────────────────────────────┤
│  □ CIDR block large enough (/16 for production)                 │
│  □ At least 2 AZs (high availability)                          │
│  □ Public subnets (ALB, NAT GW)                                │
│  □ Private app subnets (EC2, ECS)                               │
│  □ Private data subnets (RDS, ElastiCache)                     │
│  □ Internet Gateway attached                                    │
│  □ NAT Gateway in each AZ (for HA) or single (for cost)       │
│  □ Route tables per subnet tier                                 │
│  □ Security groups per tier (reference by SG ID)               │
│  □ VPC endpoints for S3 and DynamoDB (free!)                   │
│  □ VPC Flow Logs enabled (debugging, compliance)               │
│  □ DNS resolution enabled (enableDnsSupport)                   │
│  □ DNS hostnames enabled (enableDnsHostnames)                  │
│  □ Non-overlapping CIDRs for peering                           │
│  □ Tagging strategy for all resources                           │
└──────────────────────────────────────────────────────────────────┘
```

---

## Common Mistakes

### ❌ Single AZ Deployment

```
Everything in us-east-1a:
  ALB, EC2, RDS, Redis — all in one AZ
  
  us-east-1a goes down (it happens!):
  → EVERYTHING is down. Full outage.

✅ Multi-AZ:
  ALB: spans us-east-1a + 1b (automatic)
  EC2: ASG across 1a + 1b
  RDS: Multi-AZ (automatic failover)
  ElastiCache: Multi-AZ with automatic failover
  
  us-east-1a goes down:
  → ALB routes to 1b, RDS fails over, EVERYTHiNG continues
```

### ❌ VPC CIDR Too Small

```
❌ VPC: 10.0.0.0/24 (256 IPs total)
  4 subnets × 64 IPs = full. Can't add more subnets.
  Can't expand VPC CIDR easily.

✅ VPC: 10.0.0.0/16 (65,536 IPs)
  Room for hundreds of subnets
  Room for future services, VPC peering, additional AZs
```

### ❌ NAT Gateway in One AZ Only

```
NAT Gateway in us-east-1a only:
  If 1a goes down → private subnets in 1b lose internet access
  → npm install fails, external API calls fail

✅ NAT Gateway per AZ (costs more but resilient):
  us-east-1a private → NAT-1a → IGW
  us-east-1b private → NAT-1b → IGW
  
  For dev/staging: Single NAT is fine (save ~$32/month)
  For production: NAT per AZ
```

---

## Practice Exercises

### Exercise 1: VPC Design
Design a VPC for an app with: React frontend (S3 + CloudFront), Node.js API (3 instances), PostgreSQL (Multi-AZ), Redis, and a bastion host. Define all subnets, route tables, and security groups.

### Exercise 2: VPC Endpoint
Create an S3 VPC Gateway endpoint. Measure the cost savings if your app processes 50GB/month from S3.

### Exercise 3: Flow Logs
Enable VPC Flow Logs. Generate traffic and analyze the logs. Identify: accepted connections, rejected connections, and traffic patterns.

---

## Interview Q&A

**Q1: How would you design a VPC for a production application?**
> Three-tier design: public (ALB, NAT GW), private-app (EC2/ECS), private-data (RDS/Redis). Minimum 2 AZs. /16 CIDR. Security groups referencing by SG ID, not IP. VPC endpoints for S3. NAT Gateway per AZ for resilience. Flow Logs for monitoring.

**Q2: What is a VPC endpoint and when should you use one?**
> A VPC endpoint routes traffic to AWS services internally without going through NAT/internet. Gateway endpoints (S3, DynamoDB) are free — always create them. Interface endpoints cost money but keep traffic private and reduce NAT costs for services like SQS, ECR, Secrets Manager.

**Q3: How do you connect two VPCs?**
> VPC Peering: direct connection between two VPCs. Must have non-overlapping CIDRs. Routes added in both VPCs. Non-transitive. For many VPCs: Transit Gateway is a central hub. For cross-account or cross-region: both supported with peering and Transit Gateway.

**Q4: Why use multiple Availability Zones?**
> AZs are physically separate data centers. If one AZ has an outage (power, cooling, network), services in other AZs continue. Multi-AZ is required for production: ALB spans AZs, ASG launches in multiple AZs, RDS Multi-AZ provides automatic failover.

**Q5: What is the cost of a NAT Gateway and how do you reduce it?**
> ~$32/month + $0.045/GB data processing. Reduce by: S3/DynamoDB VPC endpoints (free, skip NAT for AWS traffic), caching (reduce outbound API calls), pulling Docker images from ECR via VPC endpoint, and using a single NAT Gateway in dev (save $32/month per extra AZ).
