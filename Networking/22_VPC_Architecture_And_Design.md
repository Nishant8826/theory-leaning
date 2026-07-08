# VPC Architecture & Design

> 📌 **File:** 22_VPC_Architecture_And_Design.md | **Level:** Full-Stack Dev → Networking Expert

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
  - Subnetting (file 11) → VPC subnet design
  - Routing (file 12) → Route tables
  - NAT (file 12) → NAT Gateway
  - Security (file 16) → Security Groups, NACLs
  - Load Balancing (file 13) → ALB in public subnets
  - Database (file 21) → RDS in private subnets
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
│  │  └─────────┘  └────────────┘            │  │ └─────────┘     │ │
│  │                                          │  │                   │ │
│  │  Private Subnet (App): 10.0.10.0/24     │  │ 10.0.11.0/24    │ │
│  │  ┌─────────┐  ┌─────────┐              │  │ ┌─────────┐     │ │
│  │  │  EC2    │  │  EC2    │              │  │ │  EC2    │     │ │
│  │  └─────────┘  └─────────┘              │  │ └─────────┘     │ │
│  │                                          │  │                   │ │
│  │  Private Subnet (Data): 10.0.20.0/24    │  │ 10.0.21.0/24    │ │
│  │  ┌─────────┐  ┌─────────┐              │  │ ┌─────────┐     │ │
│  │  │  RDS    │  │  Redis  │              │  │ │  RDS    │     │ │
│  │  └─────────┘  └─────────┘              │  │ └─────────┘     │ │
│  └──────────────────────────────────────────┘  └───────────────────┘ │
└──────────────────────────────────────────────────────────────────────┘
```

#### Diagram Explanation (The Corporate Office Building)
Think of a secure VPC like designing a corporate office building:
- **The Lobby (Public Subnet):** This is the only room with physical doors directly to the outside street (Internet Gateway). The front desk receptionist (ALB) and the outgoing mailroom (NAT Gateway) work here.
- **The Cubicles (App Subnet - Private):** Employees (Node.js servers) sit here. They can send outgoing mail *out* to the internet by handing it to the mailroom (NAT), but no random person from the street can walk past the lobby straight into the cubicles.
- **The Vault (Data Subnet - Isolated):** The bank safe (Databases). It has zero doors or windows to the outside. Only authorized internal employees from the cubicles can badge in.

---

## Three-Tier Subnet Strategy

```
┌──────────────────────────────────────────────────────────────────┐
│  Tier       │ Subnet Type │ Internet  │ Contains               │
├─────────────┼─────────────┼───────────┼────────────────────────┤
│  Public     │ Public      │ In + Out  │ ALB, NAT GW, Bastion  │
│  App        │ Private     │ Out only  │ EC2 (Node.js), ECS     │
│  Data       │ Isolated    │ None      │ RDS, ElastiCache       │
└─────────────┴─────────────┴───────────┴────────────────────────┘
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
│  Outbound: 5432 to sg-data, 443 to 0.0.0.0/0                   │
├─────────────────────────────────────────────────────────────────┤
│  SG: sg-data                                                   │
│  Inbound:  5432 from sg-app (PostgreSQL from app tier only)   │
│  Outbound: None needed                                         │
└─────────────────────────────────────────────────────────────────┘
```

#### Diagram Explanation (The ID Badge System)
AWS Security Groups are identical to an electronic ID badge system on the doors between rooms:
Instead of trying to remember every employee's specific name (their temporary IP Address), you rely on group classifications: "Anyone wearing an 'App Tier' role badge (`sg-app`) is allowed to open the doorway directly into the Data Vault (`sg-data`)". If you hire and deploy 50 new Node.js server instances, you just hand them the 'App Tier' badge, and you never have to manually update the locks on the database itself!

---

## VPC Endpoints (Saving Money + Security)

- **Gateway Endpoints (S3, DynamoDB):** Route traffic internally, bypassing the internet. They are **FREE** and highly recommended to save NAT Gateway data processing fees.
- **Interface Endpoints (other AWS services):** Cost ~$0.01/hour plus data fees, but keep traffic private and bypass the internet.

---

## Practice Exercises

### Exercise 1: VPC Design Diagram
Design a VPC for an app with an ALB, Node.js API (3 instances), PostgreSQL (Multi-AZ), and Redis. List the subnets and route tables.

### Exercise 2: Flow Logs Analysis
Enable VPC Flow Logs in the AWS console. Generate traffic and analyze accepted and rejected packets to ensure security rules are working.

---

## Interview Q&A

**Q1: How would you design a VPC for a production application?**
> Three-tier design: public (ALB, NAT GW), private-app (EC2/ECS), private-data (RDS/Redis). Minimum 2 AZs. /16 CIDR. Security groups referencing by SG ID, not IP. VPC endpoints for S3. NAT Gateway per AZ for resilience. Flow Logs for monitoring.

**Q2: What is a VPC endpoint and when should you use one?**
> A VPC endpoint routes traffic to AWS services internally without going through NAT/internet. Gateway endpoints (S3, DynamoDB) are free — always create them. Interface endpoints cost money but keep traffic private and reduce NAT costs for services like SQS, ECR, Secrets Manager.

**Q3: How do you connect two VPCs?**
> VPC Peering: direct connection between two VPCs. Must have non-overlapping CIDRs. For many VPCs: Transit Gateway is a central hub.

**Q4: Why use multiple Availability Zones?**
> AZs are physically separate data centers. If one AZ has an outage, services in other AZs continue. Multi-AZ is required for production: ALB spans AZs, ASG launches in multiple AZs, RDS Multi-AZ provides automatic failover.

**Q5: What is the cost of a NAT Gateway and how do you reduce it?**
> ~$32/month + $0.045/GB data processing. Reduce by: S3/DynamoDB VPC endpoints (free, skip NAT for AWS traffic), caching (reduce outbound API calls), pulling Docker images from ECR via VPC endpoint.

---

Prev : [21 Database Networking](./21_Database_Networking.md) | Index: [00 Index](./00_Index.md) | Next : [23 Debugging Network Issues](./23_Debugging_Network_Issues.md)
