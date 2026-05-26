# 44 – Deploying 3-Tier Architecture on AWS using Terraform (IaC)

> **Batch-43 | Day 3 | Multi-Cloud with AWS + DevOps + AI | 2026-05-20**

---

## Table of Contents

1. [What is a 3-Tier Architecture?](#1-what-is-a-3-tier-architecture)
2. [Monolithic vs Microservice Architecture](#2-monolithic-vs-microservice-architecture)
3. [What is Terraform (IaC)?](#3-what-is-terraform-iac)
4. [Terraform Core Workflow](#4-terraform-core-workflow)
5. [Terraform File Structure](#5-terraform-file-structure)
6. [Errors Fixed During Session](#6-errors-fixed-during-session)
7. [Visual Diagrams](#7-visual-diagrams)
8. [Scenario-Based Q&A](#8-scenario-based-qa)
9. [Interview Q&A](#9-interview-qa)
10. [Tech Stack Mapping](#10-tech-stack-mapping)
11. [Code / Practical Examples](#11-code--practical-examples)
12. [Navigation Footer](#navigation-footer)

---

## 1. What is a 3-Tier Architecture?

### What
A **3-Tier Architecture** is a way to design and deploy software applications by splitting them into **three separate layers**, each with a distinct responsibility:

| Tier | Also Called | Responsibility |
|---|---|---|
| Tier 1 | **Web / Presentation Layer** | What the user sees (Frontend, UI) |
| Tier 2 | **Application / Logic Layer** | Business rules, API processing (Middleware) |
| Tier 3 | **Database / Data Layer** | Stores and retrieves data (DB) |

### Why
- **Separation of Concerns** – Each layer does one job. If the frontend breaks, the database is safe.
- **Scalability** – You can scale each tier independently. If your API gets 10x traffic, scale only Tier 2.
- **Security** – The database tier is never directly exposed to the internet. It only talks to the app layer.
- **Maintainability** – Teams can work on each layer without stepping on each other.

### How (Step-by-step)
1. A user opens a website (browser hits Tier 1 – Web Server / EC2 / S3 + CloudFront).
2. The Web Server passes the request to Tier 2 – Application Server (Node.js / Express running on EC2 or ECS).
3. The Application Server queries Tier 3 – Database (RDS / PostgreSQL / MongoDB).
4. Data flows back: DB → App Server → Web Server → User.

### Impact

| With 3-Tier | Without 3-Tier (Monolith) |
|---|---|
| Each tier scales independently | Scale everything or nothing |
| DB is private/secure | DB may be exposed |
| Easy fault isolation | One bug can crash everything |
| Slower initial setup | Faster to start, painful later |

---

## 2. Monolithic vs Microservice Architecture

### What

**Monolithic Architecture:**
Everything (UI, business logic, database calls) is bundled into a **single deployable unit**. One giant codebase, one deployment.

**Microservice Architecture:**
The application is broken into **many small, independent services**. Each service has its own codebase, its own database, and runs independently.

### Why

| Reason | Monolith | Microservice |
|---|---|---|
| Team size | Small teams | Large teams |
| Deployment speed | Fast (one deploy) | Slower (many deploys) |
| Scalability | Hard (scale all) | Easy (scale one service) |
| Fault tolerance | Low (one bug = full crash) | High (one service fails, rest run) |
| Complexity | Low initially | Higher, but manageable |

### How

**Monolith flow:**
```
User → Single App (UI + Logic + DB calls) → One Database
```

**Microservice flow:**
```
User → API Gateway → [Auth Service] → [Order Service] → [Payment Service]
                         ↓                  ↓                  ↓
                      Users DB          Orders DB          Payments DB
```

### Impact

- **Don't use Microservices** for a small startup — it's overkill and adds DevOps overhead.
- **Do use Microservices** when teams grow, traffic is high, and different components need different scaling.

---

## 3. What is Terraform (IaC)?

### What
**Terraform** is an open-source **Infrastructure as Code (IaC)** tool by HashiCorp. It lets you define your entire cloud infrastructure (servers, databases, networking, load balancers) in **code files** (`.tf` files) instead of clicking through the AWS Console manually.

> Think of it as: **"AWS Console, but in code form."**

### Why
- **Reproducibility** – Run the same code in Dev, Staging, and Production environments and get identical infrastructure.
- **Version Control** – Infrastructure changes are tracked in Git just like application code.
- **Speed** – Provision 40+ AWS resources with a single command instead of clicking for hours.
- **Disaster Recovery** – If infrastructure is destroyed, `terraform apply` rebuilds everything in minutes.
- **Collaboration** – Teams can review infrastructure changes via Pull Requests.

### How
Terraform talks to AWS (or any cloud provider) using **provider plugins**. You write what you *want* to exist (declarative style), and Terraform figures out *how* to create it.

```
Your .tf files → Terraform Engine → AWS API → AWS Resources Created
```

### Impact

| With Terraform | Without Terraform (Manual) |
|---|---|
| Infra is reproducible | Each environment may differ |
| Changes are tracked in Git | No audit trail |
| Full teardown in one command | Manual deletion = mistakes |
| Team collaboration via PRs | Single person controls infra |

---

## 4. Terraform Core Workflow

### The 5 Key Commands

---

### `terraform init`

**What:** Initializes the working directory. Downloads the required **provider plugins** (e.g., AWS provider) and **modules** referenced in your code.

**What it creates:**
- `.terraform/` folder – contains downloaded providers and modules
- `.terraform.lock.hcl` – locks provider versions

**Why:** You must run this first. Without it, Terraform doesn't know which cloud provider to talk to.

**Analogy:** Like `npm install` — sets up all dependencies before you can run the project.

```bash
terraform init
```

---

### `terraform plan`

**What:** A **dry run**. Terraform reads your `.tf` files, compares them against the current state (`.tfstate` file), and shows you *exactly* what it will create, change, or destroy — **without actually doing anything**.

**Why:** Prevents surprises. You can review the plan before applying. Great for catching mistakes.

**Output example:**
```
Plan: 12 to add, 0 to change, 0 to destroy.
```

**Analogy:** Like a blueprint review meeting before construction starts.

```bash
terraform plan
```

---

### `terraform apply`

**What:** **Executes** the plan and actually creates/modifies/destroys resources in AWS.

**Why:** This is the command that makes things real. Terraform sends API calls to AWS and provisions your infrastructure.

**What happens:**
1. Terraform shows the plan again.
2. Asks for confirmation: `Do you want to perform these actions? yes`
3. Provisions all resources in the correct order.
4. Updates the **state file** (`.tfstate`) with what was created.

```bash
terraform apply
# or skip confirmation prompt:
terraform apply -auto-approve
```

---

### `terraform destroy`

**What:** **Tears down all resources** that were created by your Terraform configuration.

**Why:** Useful for saving costs (destroy dev environments at night), cleanup after testing, or starting fresh.

**Warning:** This deletes everything. Use with caution in production.

```bash
terraform destroy
```

---

### `terraform refresh`

**What:** Syncs the **Terraform state file** with the **actual current state** of AWS resources.

**Why needed:** If someone manually changes something in AWS (outside Terraform), the state file becomes outdated. `refresh` updates it to reflect reality.

**Analogy:** Like clicking "Refresh" in your browser — it pulls the latest version of what actually exists.

```bash
terraform refresh
```

---

### Workflow Summary

```
terraform init → terraform plan → terraform apply → [use infra] → terraform destroy
                                         ↑
                              terraform refresh (when state drifts)
```

---

## 5. Terraform File Structure

In this session, ~40 AWS resources were created using **Terraform modules**. Here's the file structure and what each file does:

### Files Explained

---

### `main.tf` – The Root File

**What:** The entry point of your Terraform project. It **calls modules** (reusable blocks of infrastructure code).

**Why:** Instead of writing 400 lines of code in one file, you split logic into modules (networking, autoscaling, database) and call them here.

```hcl
# main.tf example
module "networking" {
  source    = "./modules/networking"
  namespace = var.namespace
  region    = var.region
}

module "autoscaling" {
  source   = "./modules/autoscaling"
  key_pair = var.key_pair
  vpc_id   = module.networking.vpc_id
}

module "database" {
  source     = "./modules/database"
  db_name    = var.db_name
  subnet_ids = module.networking.private_subnet_ids
}
```

---

### `variable.tf` – Variable Definitions

**What:** Declares all the **variables** your configuration uses — their names, types, descriptions, and optional default values.

**Why:** Keeps your code flexible and reusable. Instead of hardcoding `us-east-1` everywhere, you define it as a variable.

```hcl
# variable.tf
variable "namespace" {
  description = "Prefix for all resource names"
  type        = string
}

variable "region" {
  description = "AWS region to deploy into"
  type        = string
  default     = "us-east-1"
}

variable "key_pair" {
  description = "EC2 key pair name for SSH access"
  type        = string
}
```

---

### `terraform.tfvars` – Variable Values (Best Practice)

**What:** The file where you **assign actual values** to the variables defined in `variable.tf`.

**Why (Best Practice):**
- Keeps secrets and environment-specific values **out of the main code**.
- You can have multiple `.tfvars` files: `dev.tfvars`, `prod.tfvars`, `staging.tfvars`.
- Never commit sensitive `.tfvars` files to Git — add to `.gitignore`.

```hcl
# terraform.tfvars
namespace = "myapp-prod"
region    = "ap-south-1"
key_pair  = "my-ec2-key"
db_name   = "appdb"
```

---

### `output.tf` – Output Values

**What:** Defines what information Terraform should **print out after `apply`** completes.

**Why:** After creating 40 resources, you need to know key values like the Load Balancer DNS name and the encrypted DB password — without logging into the AWS Console.

```hcl
# output.tf
output "load_balancer_dns" {
  description = "DNS name to access the application"
  value       = module.networking.lb_dns_name
}

output "db_password_encrypted" {
  description = "Encrypted RDS password"
  value       = module.database.db_password
  sensitive   = true  # Hides value in terminal output
}
```

After `apply`, you'll see:
```
Outputs:
load_balancer_dns = "myapp-lb-123456.ap-south-1.elb.amazonaws.com"
db_password_encrypted = <sensitive>
```

---

### File Structure Summary

```
project/
├── main.tf              ← Calls modules, orchestrates everything
├── variable.tf          ← Declares variable names and types
├── terraform.tfvars     ← Assigns values to variables (env-specific)
├── output.tf            ← Prints key values after apply
├── .terraform/          ← Auto-created by `init` (providers/modules)
├── .terraform.lock.hcl  ← Provider version lock file
├── terraform.tfstate    ← Current state of AWS resources
└── modules/
    ├── networking/      ← VPC, subnets, security groups
    ├── autoscaling/     ← EC2 launch template, ASG, load balancer
    └── database/        ← RDS instance, subnet group
```

---

## 6. Errors Fixed During Session

### Error 1: Ubuntu AMI Version Mismatch

**What happened:** The Terraform config referenced an outdated Ubuntu AMI ID that no longer existed (or wasn't available in the selected region).

**Fix:** Updated the AMI to **Ubuntu 22.04 LTS** and used the correct AMI ID for the target region.

**Why this happens:** AMI IDs are **region-specific** and **change with new releases**. An AMI ID valid in `us-east-1` is completely different in `ap-south-1`.

**Best Practice:** Use a **data source** to always fetch the latest AMI dynamically:

```hcl
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical (Ubuntu's official AWS account)

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
}

resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id  # Always gets the latest
  instance_type = "t3.micro"
}
```

---

### Error 2: DB Instance Type – `t2.micro` → `t3.micro`

**What happened:** The RDS instance was configured as `t2.micro`, but AWS has **licensing restrictions** and deprecations on certain `t2` instance types for RDS in newer engine versions.

**Fix:** Changed to `t3.micro` — the current-generation equivalent.

**Why this matters:**
- `t3` instances are more cost-effective and have better baseline performance than `t2`.
- AWS is gradually retiring `t2` for many services.
- Always check the [AWS RDS supported instance types](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.DBInstanceClass.html) for your engine version.

```hcl
# Before (caused error):
instance_class = "db.t2.micro"

# After (fixed):
instance_class = "db.t3.micro"
```

---

## 7. Visual Diagrams

### 3-Tier Architecture on AWS

```
                          ┌──────────────────────────────────────────────┐
                          │                    AWS Cloud                  │
                          │                                              │
  User (Browser)          │  ┌─────────────────────────────────────┐    │
      │                   │  │            VPC (Virtual Network)     │    │
      │  HTTPS            │  │                                      │    │
      ▼                   │  │  ┌────────────────────────────────┐  │    │
  ┌────────┐              │  │  │    Public Subnet               │  │    │
  │Internet│──────────────┼──┼─▶│  ┌──────────────────────────┐ │  │    │
  │Gateway │              │  │  │  │  Application Load Balancer│ │  │    │
  └────────┘              │  │  │  └──────────┬───────────────┘ │  │    │
                          │  │  └─────────────┼────────────────-┘  │    │
                          │  │                │  (TIER 1 – Web)     │    │
                          │  │  ┌─────────────▼────────────────┐    │    │
                          │  │  │    Private Subnet (App)       │    │    │
                          │  │  │  ┌──────────────────────────┐ │    │    │
                          │  │  │  │  Auto Scaling Group       │ │    │    │
                          │  │  │  │  EC2 (Node.js / Express)  │ │    │    │
                          │  │  │  └──────────┬───────────────┘ │    │    │
                          │  │  └─────────────┼─────────────────┘    │    │
                          │  │                │  (TIER 2 – App)       │    │
                          │  │  ┌─────────────▼────────────────┐    │    │
                          │  │  │    Private Subnet (DB)        │    │    │
                          │  │  │  ┌──────────────────────────┐ │    │    │
                          │  │  │  │  RDS (PostgreSQL / MySQL) │ │    │    │
                          │  │  │  └──────────────────────────┘ │    │    │
                          │  │  └──────────────────────────────┘    │    │
                          │  │                (TIER 3 – DB)          │    │
                          │  └─────────────────────────────────────-┘    │
                          └──────────────────────────────────────────────┘
```

---

### Terraform Workflow

```
┌────────────────────────────────────────────────────────────┐
│                    Terraform Workflow                       │
└────────────────────────────────────────────────────────────┘

  .tf Files Written
        │
        ▼
  ┌─────────────┐
  │terraform    │  Downloads providers & modules
  │   init      │  Creates .terraform/ folder
  └──────┬──────┘
         │
         ▼
  ┌─────────────┐
  │terraform    │  Reads .tf files + state file
  │   plan      │  Shows: add/change/destroy
  └──────┬──────┘
         │
         ▼
  ┌─────────────┐
  │terraform    │  Calls AWS APIs
  │   apply     │  Creates actual resources
  └──────┬──────┘
         │                  ┌──────────────┐
         ├──────────────────▶ terraform    │ ← manual changes in AWS
         │                  │  refresh     │   drift detected
         │                  └──────────────┘
         ▼
  ┌─────────────┐
  │terraform    │  Deletes all resources
  │  destroy    │  Clean teardown
  └─────────────┘
```

---

### Terraform File Relationship Diagram

```
terraform.tfvars
  (actual values)
        │
        ▼
  variable.tf  ←──────────────────────────────┐
  (variable      │                             │
   declarations) │                             │
                 ▼                             │
              main.tf ─────── calls ──────▶ modules/
              (root file)                     ├── networking/
                 │                            ├── autoscaling/
                 │                            └── database/
                 ▼
              output.tf
              (prints DNS, passwords)
```

---

### Module Architecture (What ~40 Resources Look Like)

```
main.tf
 ├── module: networking
 │     ├── VPC
 │     ├── Public Subnets (2x AZ)
 │     ├── Private Subnets – App (2x AZ)
 │     ├── Private Subnets – DB (2x AZ)
 │     ├── Internet Gateway
 │     ├── NAT Gateway
 │     ├── Route Tables (public + private)
 │     └── Security Groups (ALB, EC2, RDS)
 │
 ├── module: autoscaling
 │     ├── EC2 Launch Template (Ubuntu 22.04)
 │     ├── Auto Scaling Group
 │     ├── Application Load Balancer
 │     ├── ALB Target Group
 │     └── ALB Listener (port 80/443)
 │
 └── module: database
       ├── RDS Instance (db.t3.micro)
       ├── DB Subnet Group
       ├── DB Parameter Group
       └── Secrets Manager (encrypted password)
```

---

## 8. Scenario-Based Q&A

---

🔍 **Scenario 1:** Your team just joined a new project. The dev environment was built manually in AWS six months ago. No one knows exactly what's deployed. How would Terraform help going forward?

✅ **Answer:** Going forward, write all new infrastructure as Terraform `.tf` files. Run `terraform import` to bring existing resources under Terraform's control. From now on, every change is code-reviewed in Git, reproducible, and documented. No more "who clicked what in the console" mystery.

---

🔍 **Scenario 2:** You ran `terraform apply` and created 40 resources. Your colleague logged into the AWS Console and manually changed a Security Group rule. Now `terraform plan` shows unexpected changes. Why?

✅ **Answer:** This is called **state drift**. The `.tfstate` file thinks the security group has the old rule, but AWS has the new one. Run `terraform refresh` to sync the state file with real AWS. Then decide: revert the manual change by running `terraform apply`, or update the `.tf` code to match what your colleague intended.

---

🔍 **Scenario 3:** You're deploying to three environments: Dev, Staging, Production — all in different AWS regions. How do you avoid duplicating Terraform code?

✅ **Answer:** Use separate `terraform.tfvars` files for each environment:
- `dev.tfvars` → region = `us-east-1`, instance_type = `t3.micro`
- `prod.tfvars` → region = `ap-south-1`, instance_type = `t3.large`

Then run: `terraform apply -var-file="prod.tfvars"`. Same code, different values. Never duplicate the modules.

---

🔍 **Scenario 4:** Your application suddenly gets 5x more traffic than usual during a product launch. Your 3-tier architecture has an Auto Scaling Group in Tier 2. What happens?

✅ **Answer:** The Auto Scaling Group detects high CPU (via CloudWatch alarm), automatically launches new EC2 instances in Tier 2 (app layer), and registers them with the Load Balancer. Tier 1 (ALB) distributes traffic across all instances. Tier 3 (RDS) handles the increased DB queries. When traffic drops, ASG scales in and terminates extra instances — saving cost. **This is the power of 3-tier scalability.**

---

🔍 **Scenario 5:** You're a junior DevOps engineer and someone asks you to destroy the dev environment every night and recreate it every morning to save costs. How do you do it?

✅ **Answer:** Schedule a CI/CD pipeline (Jenkins / GitHub Actions) that runs `terraform destroy -auto-approve` at 11 PM and `terraform apply -auto-approve` at 8 AM. Since everything is code, teardown and recreation takes ~10 minutes and is fully automated. No manual work.

---

🔍 **Scenario 6:** You try to run `terraform apply` and it fails with "AMI not found." What went wrong and how do you fix it?

✅ **Answer:** The AMI ID hardcoded in the config is invalid — either it was deprecated, or it's the wrong region. Fix: Use a `data "aws_ami"` block to dynamically fetch the latest Ubuntu 22.04 AMI for the current region (as shown in the Errors section). This future-proofs your code so it never breaks due to AMI expiry.

---

## 9. Interview Q&A

---

**Q1. What is Terraform and how is it different from the AWS Console?**

**A:** Terraform is an Infrastructure as Code (IaC) tool that lets you define AWS resources in `.tf` files. Unlike the AWS Console (a GUI), Terraform is code-based, version-controlled, reproducible, and automatable. The same Terraform code can create identical infrastructure in Dev, Staging, and Production — manually clicking the Console cannot guarantee that.

---

**Q2. Explain the `terraform init`, `plan`, `apply`, and `destroy` commands.**

**A:**
- `init` – Sets up the project: downloads provider plugins and modules. Must run first.
- `plan` – Dry run: shows what *will* happen without making any changes. Used for review.
- `apply` – Executes the plan and provisions actual AWS resources. Updates the state file.
- `destroy` – Tears down all resources managed by this configuration.

---

**Q3. What is the Terraform state file and why is it important?**

**A:** The `.tfstate` file is Terraform's record of what infrastructure currently exists in AWS. It maps your code to real-world resources. Without it, Terraform can't know what exists already. In teams, the state file is stored remotely (in S3 + DynamoDB for locking) so everyone shares the same source of truth.

---

**Q4. What is the difference between `variable.tf` and `terraform.tfvars`?**

**A:** `variable.tf` **declares** variables — their names, types, and descriptions (like a schema). `terraform.tfvars` **assigns values** to those variables (like the data). This separation allows you to have one codebase and multiple `.tfvars` files for different environments (dev, staging, prod).

---

**Q5. What is state drift in Terraform and how do you handle it?**

**A:** State drift happens when the actual AWS infrastructure is changed **outside of Terraform** (e.g., someone manually modifies a resource in the Console). The `.tfstate` file no longer matches reality. You handle it by running `terraform refresh` (to update the state) and then deciding whether to `apply` (revert to code) or update the code to match the manual change.

---

**Q6. What is a Terraform module and why do we use them?**

**A:** A module is a **reusable, self-contained block** of Terraform configuration. Instead of writing all 400+ lines in one file, you break logic into modules (networking, autoscaling, database) and call them from `main.tf`. This promotes DRY (Don't Repeat Yourself) principles, easier maintenance, and reusability across projects.

---

**Q7. Why should `terraform.tfvars` not be committed to Git?**

**A:** Because `terraform.tfvars` often contains sensitive values like database passwords, API keys, and environment-specific config. Committing these to a public (or even private) repo is a security risk. Best practice: add `.tfvars` to `.gitignore` and store sensitive values in a secrets manager (AWS Secrets Manager, HashiCorp Vault) or CI/CD environment variables.

---

**Q8. What is the difference between a Monolithic and Microservice architecture? When would you choose each?**

**A:**
- **Monolith** – Single deployable unit. All features in one codebase. Simple to start, hard to scale. Best for small teams and early-stage products.
- **Microservices** – Many independent services, each owning its domain and database. Complex to set up, but scales excellently and allows independent deployments. Best for large teams and high-traffic systems.

Choose Monolith to start fast. Migrate to Microservices when scaling pain begins.

---

**Q9. In a 3-tier AWS architecture, why is the database placed in a private subnet?**

**A:** The database should never be directly accessible from the internet. Placing it in a **private subnet** means it has no public IP and no route to the Internet Gateway. Only the Application Server (Tier 2, also in a private subnet) can reach it via internal VPC routing. This is a core security principle — minimize the attack surface.

---

**Q10. What happened when `db.t2.micro` was used and how was it fixed?**

**A:** AWS has deprecated or restricted `t2` instance types for newer RDS engine versions due to licensing constraints. The error indicated the instance class wasn't supported. The fix was to upgrade to `db.t3.micro` — the current-generation successor that offers the same free-tier eligibility with better performance and broader support.

---

## 10. Tech Stack Mapping

### Tools Used in This Architecture

| Layer | AWS Service | Purpose |
|---|---|---|
| DNS / CDN | Route 53, CloudFront | Domain routing, caching |
| Tier 1 – Frontend | S3 + CloudFront **or** EC2 behind ALB | Serve static/dynamic web content |
| Load Balancer | Application Load Balancer (ALB) | Distributes traffic to Tier 2 |
| Tier 2 – Backend | EC2 (Auto Scaling Group) | Runs Node.js / Express / Python APIs |
| Tier 3 – Database | RDS (PostgreSQL / MySQL) | Relational database, private subnet |
| Secrets | AWS Secrets Manager | Stores encrypted DB passwords |
| Networking | VPC, Subnets, Security Groups, NAT GW | Isolates tiers, controls traffic |
| IaC | Terraform | Provisions all of the above as code |
| CI/CD | Jenkins / GitHub Actions | Automates deploy pipeline |

---

### Real Deployment Flow (Node.js App on 3-Tier AWS)

```
Developer pushes code to GitHub
        │
        ▼
Jenkins Pipeline triggers
        │
        ├── terraform plan  (review infra changes)
        ├── terraform apply (provision/update infra)
        │
        ├── Build Docker image of Node.js app
        ├── Push image to ECR (Elastic Container Registry)
        │
        └── Rolling deploy to EC2 ASG via CodeDeploy
                  │
                  ▼
            ALB routes traffic to healthy EC2 instances
                  │
                  ▼
            Node.js app connects to RDS via private DNS
```

---

### Tech-Specific Notes

**Node.js App on EC2:**
- Environment variables (DB host, password) injected from AWS Secrets Manager or SSM Parameter Store
- App listens on port 3000; ALB forwards port 80/443 → 3000
- Process manager: PM2 or systemd for auto-restart

**React / Next.js Frontend:**
- Static builds deployed to S3 bucket
- Served via CloudFront CDN globally
- Next.js SSR: deploy on EC2 / ECS in Tier 1

**PostgreSQL / RDS:**
- Multi-AZ enabled for production (auto failover)
- Automated backups enabled
- Only accessible from App Security Group (no public access)

**Redis (ElastiCache):**
- Often added as a Tier 2.5 for session storage / caching
- Sits in private subnet, same as app tier

---

## 11. Code / Practical Examples

### Example 1: `main.tf` – Root Module Calling 3 Modules

```hcl
# main.tf

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # Store state remotely (team best practice)
  backend "s3" {
    bucket         = "my-terraform-state-bucket"
    key            = "prod/terraform.tfstate"
    region         = "ap-south-1"
    dynamodb_table = "terraform-state-lock"
  }
}

provider "aws" {
  region = var.region
}

module "networking" {
  source    = "./modules/networking"
  namespace = var.namespace
  region    = var.region
}

module "autoscaling" {
  source         = "./modules/autoscaling"
  key_pair       = var.key_pair
  vpc_id         = module.networking.vpc_id
  public_subnets = module.networking.public_subnet_ids
  app_subnets    = module.networking.app_subnet_ids
  alb_sg_id      = module.networking.alb_sg_id
  ec2_sg_id      = module.networking.ec2_sg_id
}

module "database" {
  source      = "./modules/database"
  db_name     = var.db_name
  db_username = var.db_username
  db_subnets  = module.networking.db_subnet_ids
  db_sg_id    = module.networking.db_sg_id
}
```

---

### Example 2: `variable.tf` + `terraform.tfvars`

```hcl
# variable.tf
variable "namespace" {
  description = "Prefix for naming all resources"
  type        = string
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = "ap-south-1"
}

variable "key_pair" {
  description = "Name of the EC2 SSH key pair"
  type        = string
}

variable "db_name" {
  description = "RDS database name"
  type        = string
}

variable "db_username" {
  description = "RDS master username"
  type        = string
}
```

```hcl
# terraform.tfvars  (DO NOT commit to Git)
namespace   = "myapp-prod"
region      = "ap-south-1"
key_pair    = "myapp-ec2-key"
db_name     = "myappdb"
db_username = "admin"
```

---

### Example 3: Dynamic AMI Data Source (Fix for AMI Error)

```hcl
# modules/autoscaling/main.tf

# Always fetch the latest Ubuntu 22.04 AMI
data "aws_ami" "ubuntu_22" {
  most_recent = true
  owners      = ["099720109477"] # Canonical official

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

resource "aws_launch_template" "app" {
  name_prefix   = "${var.namespace}-lt-"
  image_id      = data.aws_ami.ubuntu_22.id  # Dynamic, never stale
  instance_type = "t3.micro"
  key_name      = var.key_pair

  vpc_security_group_ids = [var.ec2_sg_id]

  user_data = base64encode(<<-EOF
    #!/bin/bash
    apt-get update -y
    apt-get install -y nodejs npm
    npm install -g pm2
  EOF
  )

  tag_specifications {
    resource_type = "instance"
    tags = {
      Name = "${var.namespace}-app-server"
    }
  }
}

resource "aws_autoscaling_group" "app" {
  name                = "${var.namespace}-asg"
  desired_capacity    = 2
  min_size            = 1
  max_size            = 4
  vpc_zone_identifier = var.app_subnets

  launch_template {
    id      = aws_launch_template.app.id
    version = "$Latest"
  }
}
```

---

### Example 4: RDS Module (with `db.t3.micro` fix)

```hcl
# modules/database/main.tf

resource "aws_db_subnet_group" "main" {
  name       = "${var.namespace}-db-subnet-group"
  subnet_ids = var.db_subnets
}

resource "random_password" "db" {
  length  = 16
  special = true
}

resource "aws_secretsmanager_secret" "db_password" {
  name = "${var.namespace}-db-password"
}

resource "aws_secretsmanager_secret_version" "db_password" {
  secret_id     = aws_secretsmanager_secret.db_password.id
  secret_string = random_password.db.result
}

resource "aws_db_instance" "main" {
  identifier             = "${var.namespace}-rds"
  engine                 = "postgres"
  engine_version         = "15"
  instance_class         = "db.t3.micro"  # Fixed: was db.t2.micro
  allocated_storage      = 20
  db_name                = var.db_name
  username               = var.db_username
  password               = random_password.db.result
  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [var.db_sg_id]
  skip_final_snapshot    = true
  multi_az               = false  # Set true for production

  tags = {
    Name = "${var.namespace}-database"
  }
}
```

---

### Example 5: `output.tf`

```hcl
# output.tf

output "alb_dns_name" {
  description = "Access the application at this URL"
  value       = module.autoscaling.alb_dns_name
}

output "rds_endpoint" {
  description = "RDS connection endpoint (internal use only)"
  value       = module.database.db_endpoint
}

output "db_password_secret_arn" {
  description = "ARN of the Secrets Manager secret holding the DB password"
  value       = module.database.secret_arn
  sensitive   = true
}
```

---

### Example 6: Jenkins Pipeline – Terraform + Deploy

```groovy
// Jenkinsfile
pipeline {
    agent any

    environment {
        AWS_ACCESS_KEY_ID     = credentials('aws-access-key')
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret-key')
        TF_VAR_FILE           = "prod.tfvars"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/org/infra-repo.git'
            }
        }

        stage('Terraform Init') {
            steps {
                sh 'terraform init'
            }
        }

        stage('Terraform Plan') {
            steps {
                sh "terraform plan -var-file=${TF_VAR_FILE} -out=tfplan"
            }
        }

        stage('Approval') {
            steps {
                input message: 'Review the plan. Approve to apply?'
            }
        }

        stage('Terraform Apply') {
            steps {
                sh 'terraform apply -auto-approve tfplan'
            }
        }

        stage('Deploy App') {
            steps {
                sh '''
                    # Build and push Docker image to ECR
                    aws ecr get-login-password --region ap-south-1 | \
                      docker login --username AWS --password-stdin $ECR_URI
                    docker build -t myapp:latest .
                    docker tag myapp:latest $ECR_URI/myapp:latest
                    docker push $ECR_URI/myapp:latest

                    # Trigger rolling update on EC2 ASG
                    aws deploy create-deployment \
                      --application-name myapp \
                      --deployment-group-name prod-asg \
                      --description "Deploy from Jenkins build $BUILD_NUMBER"
                '''
            }
        }
    }

    post {
        failure {
            echo 'Pipeline failed. Infrastructure may be in inconsistent state.'
        }
        success {
            echo 'Deployment successful!'
        }
    }
}
```

---

### Example 7: Dockerfile for Node.js App (Tier 2)

```dockerfile
# Dockerfile – Node.js Application Server (Tier 2)

FROM node:20-alpine

WORKDIR /app

# Copy dependency files first (layer caching optimization)
COPY package*.json ./
RUN npm ci --only=production

# Copy application source
COPY . .

# App listens on port 3000
EXPOSE 3000

# Health check for ALB
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD wget -qO- http://localhost:3000/health || exit 1

# Run with non-root user (security best practice)
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

CMD ["node", "server.js"]
```

---


← Previous: [`43_Terraform_Advanced_Commands_State_Management_MultiResource_Provisioning_&_PR_Workflow.md`](43_Terraform_Advanced_Commands_State_Management_MultiResource_Provisioning_&_PR_Workflow.md) | Next: [`45_Ansible_Configuration_Management_&_Automation.md`](45_Ansible_Configuration_Management_&_Automation.md) →