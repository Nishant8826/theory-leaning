# 42 – Terraform & Infrastructure as Code (IaC)

> **Session Date:** May 18, 2026
> **Category:** DevOps / Cloud Infrastructure
> **Tools Covered:** Terraform, Ansible, AWS CLI, IAM, EC2, HCL

---

## Table of Contents

1. [What is Infrastructure as Code (IaC)?](#1-what-is-infrastructure-as-code-iac)
2. [What is Terraform?](#2-what-is-terraform)
3. [Terraform vs Ansible](#3-terraform-vs-ansible)
4. [Terraform Workflow & Commands](#4-terraform-workflow--commands)
5. [HCL – HashiCorp Configuration Language](#5-hcl--hashicorp-configuration-language)
6. [Hands-On Lab Walkthrough](#6-hands-on-lab-walkthrough)
7. [Visual Diagrams](#7-visual-diagrams)
8. [Scenario-Based Q&A](#8-scenario-based-qa)
9. [Interview Q&A](#9-interview-qa)
10. [Tech Stack Mapping](#10-tech-stack-mapping)
11. [Code / Practical Examples](#11-code--practical-examples)

---

## 1. What is Infrastructure as Code (IaC)?

### What
IaC means writing **code to define, provision, and manage infrastructure** — instead of clicking through dashboards or running manual commands. Think of it as a blueprint for your servers, networks, databases, and cloud resources — stored as text files.

### Why
- Manual infrastructure setup is slow, error-prone, and impossible to reproduce exactly
- **40% of deployment errors** come from manual activities — IaC eliminates most of them
- Code can be version-controlled on GitHub, reviewed, tested, and rolled back
- Teams can spin up identical environments (dev, staging, prod) with a single command

### How
1. You write configuration files describing what infrastructure you want
2. A tool reads those files and talks to cloud provider APIs (AWS, Azure, GCP)
3. The cloud provider creates the resources
4. The state of infrastructure is tracked in a **state file**

### Impact

| With IaC | Without IaC |
|---|---|
| Consistent environments every time | "Works on my machine" problems |
| Infra tracked in Git | No history of what changed |
| Automated, fast provisioning | Slow, click-heavy process |
| Easy disaster recovery | Manual recreation after failure |
| Reduced human error | 40%+ error rate from manual steps |

---

## 2. What is Terraform?

### What
Terraform is an open-source **Infrastructure as Code tool** created by **HashiCorp in 2014**. It lets you define cloud resources in configuration files and provision them automatically. It supports **6,546+ providers** including AWS, Azure, GCP, Kubernetes, GitHub, and more.

### Why
- Cloud infrastructures are complex — dozens of services need to work together
- Terraform gives you a single tool to manage infra across multiple cloud providers
- It maintains a **state file** so it knows what exists and what needs to change
- Supports **immutable infrastructure** — instead of patching, it destroys and recreates

### How
1. Write `.tf` files using HCL (HashiCorp Configuration Language)
2. Run `terraform init` → downloads required provider plugins
3. Run `terraform plan` → previews what will be created/changed/destroyed
4. Run `terraform apply` → actually creates the resources
5. Terraform records everything in `terraform.tfstate`
6. Run `terraform destroy` → removes all resources defined in your config

### Impact

| Scenario | Impact |
|---|---|
| Using Terraform | Infra is reproducible, auditable, fast |
| Not using Terraform | Manual errors, inconsistency, slow recovery |
| Terraform with GitHub | Full change history, PR reviews for infra |
| Terraform destroy | Clean teardown, no orphaned resources |

---

## 3. Terraform vs Ansible

### What
Both are automation tools — but they solve **different problems** in the DevOps lifecycle.

### Why Both Exist
- **Terraform** is great at talking to cloud APIs to create resources
- **Ansible** is great at SSH-ing into servers and configuring them after creation
- They complement each other — use Terraform to create the server, Ansible to configure it

### Detailed Comparison

| Feature | Terraform | Ansible |
|---|---|---|
| **Purpose** | Infrastructure Provisioning | Configuration Management |
| **Language** | HCL (HashiCorp Config Language) | YAML (Playbooks) |
| **Infrastructure style** | Immutable (destroys & recreates) | Mutable (in-place modifications) |
| **State Management** | Yes — tracks state in `.tfstate` | No state file |
| **Agentless?** | Yes | Yes (uses SSH) |
| **Created by** | HashiCorp (2014) | Red Hat (2012) |
| **Best for** | Creating EC2, VPCs, S3, RDS | Installing Python, patching OS, managing users |
| **Cloud provider support** | 6,546+ providers | Wide but less cloud-focused |

### Best Practice Combination
```
Terraform → Create EC2 instance
Ansible   → Install Python, configure app, manage users on that EC2
```

### Impact
- **Using both together:** Fully automated pipeline from raw cloud to configured server
- **Terraform alone:** Infrastructure is created but not configured
- **Ansible alone:** No automated way to provision the underlying servers

---

## 4. Terraform Workflow & Commands

### What
Terraform follows a clear **4-step workflow** for managing infrastructure lifecycle.

### The Core Commands

#### `terraform init`
- **What:** Downloads and installs the required **provider plugins** (e.g., AWS provider)
- **When:** Run once after writing your first `.tf` file or when adding a new provider
- **Creates:** `.terraform/` directory with downloaded plugins

#### `terraform plan`
- **What:** Previews changes — shows what will be **created, modified, or destroyed**
- **When:** Always run before apply — acts as a "dry run"
- **Output:** Color-coded diff (`+` green = create, `~` yellow = modify, `-` red = destroy)

#### `terraform apply`
- **What:** **Actually creates/modifies** the infrastructure described in your `.tf` files
- **When:** After reviewing the plan output and you're confident
- **Asks:** Prompts for confirmation (`yes`) before proceeding
- **Creates:** Updates `terraform.tfstate` with real resource IDs

#### `terraform destroy`
- **What:** **Removes all resources** defined in your configuration
- **When:** When you're done with an environment (e.g., after a lab)
- **Why important:** Prevents surprise AWS bills from forgotten resources

### Workflow Diagram
```
Write .tf Files
      ↓
terraform init      ← Downloads AWS/Azure/GCP provider plugins
      ↓
terraform plan      ← Shows preview: what will be created/changed/destroyed
      ↓
terraform apply     ← Creates real resources in the cloud
      ↓
[Resources Running]
      ↓
terraform destroy   ← Tears everything down cleanly
```

---

## 5. HCL – HashiCorp Configuration Language

### What
HCL is the language Terraform uses to describe infrastructure. It's designed to be:
- **Human-friendly** — readable like English sentences
- **Machine-friendly** — parseable by tools and automations

### Basic HCL Structure
```hcl
# This is a comment

# Block type "resource" of type "aws_instance" named "my_server"
resource "aws_instance" "my_server" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"

  tags = {
    Name = "MyFirstServer"
  }
}
```

### Key Concepts

| Concept | Description | Example |
|---|---|---|
| **Block** | A container for configuration | `resource { }`, `provider { }` |
| **Argument** | Key-value pair inside a block | `instance_type = "t3.micro"` |
| **Provider** | Plugin to talk to a cloud | `provider "aws" { }` |
| **Resource** | A piece of infra to create | EC2 instance, S3 bucket |
| **Variable** | Reusable input value | `var.region` |
| **Output** | Value exported after apply | Public IP of EC2 |

---

## 6. Hands-On Lab Walkthrough

### Setup Steps Performed

#### Step 1: Install Terraform
```
Downloaded terraform binary (31.9 MB)
Placed in C:\bin folder
Added C:\bin to system PATH environment variable
```

#### Step 2: Install & Configure AWS CLI
```bash
aws configure
# Prompts for:
# AWS Access Key ID
# AWS Secret Access Key
# Default region (e.g., us-east-1)
# Output format (json)
```

#### Step 3: Create IAM User
```
IAM User: Terraform43
Permissions: Administrator Access
Generated: Access Key ID + Secret Access Key
```

#### Step 4: Clone & Run Terraform
```bash
git clone <terraform-repo>
cd terraform-repo

terraform init    # Downloads AWS provider
terraform plan    # Preview: 1 EC2 instance to be created
terraform apply   # Type "yes" to confirm
# EC2 instance created!

terraform destroy # Clean up all resources
```

#### Troubleshooting Encountered
- **Issue:** T2 micro instance type not eligible for free tier in some regions
- **Fix:** Switched to `t3.micro` which is free-tier eligible
- **Lesson:** Always check the instance type eligibility for your AWS account type

---

## 7. Visual Diagrams

### Terraform Architecture Overview
```
┌─────────────────────────────────────────────┐
│             Developer's Machine              │
│                                             │
│  ┌──────────┐    ┌──────────────────────┐  │
│  │  .tf     │    │   terraform.tfstate  │  │
│  │  files   │    │   (tracks what       │  │
│  │  (HCL)   │    │    exists in cloud)  │  │
│  └────┬─────┘    └──────────────────────┘  │
│       │                                     │
│  ┌────▼─────────────────┐                  │
│  │   Terraform CLI      │                  │
│  │  init / plan /       │                  │
│  │  apply / destroy     │                  │
│  └────┬─────────────────┘                  │
└───────┼──────────────────────────────────── ┘
        │ HTTPS API calls
        ▼
┌───────────────────────────────────────────────┐
│              Cloud Provider APIs               │
│                                               │
│   ┌──────┐   ┌──────┐   ┌──────┐   ┌──────┐ │
│   │  AWS │   │Azure │   │ GCP  │   │ 6500+│ │
│   │  EC2 │   │  VM  │   │Compu │   │others│ │
│   │  S3  │   │      │   │  te  │   │      │ │
│   └──────┘   └──────┘   └──────┘   └──────┘ │
└───────────────────────────────────────────────┘
```

### Terraform vs Ansible in a Pipeline
```
Developer pushes code
        │
        ▼
┌───────────────────┐
│    Terraform      │   ← "Build the house"
│                   │
│  • Create VPC     │
│  • Create EC2     │
│  • Create RDS     │
│  • Create S3      │
└────────┬──────────┘
         │ Infrastructure ready
         ▼
┌───────────────────┐
│     Ansible       │   ← "Furnish the house"
│                   │
│  • Install Python │
│  • Install Nginx  │
│  • Create users   │
│  • Patch OS       │
│  • Deploy app     │
└───────────────────┘
         │
         ▼
   App Running! 🚀
```

### Terraform State Lifecycle
```
terraform apply                terraform apply (again, after change)
      │                                   │
      ▼                                   ▼
Creates resource         ┌─── Reads tfstate ────┐
      │                  │                       │
      ▼                  ▼                       ▼
Updates tfstate     What exists?          What do I want?
      │                  │                       │
      ▼                  └──── Computes DIFF ────┘
Resource running               │
                               ▼
                      Only changes the DIFF
                      (not everything)
```

### IaC Error Reduction
```
Manual Deployments          IaC (Terraform)
─────────────────          ───────────────
Click Console               Write Code
Click Again                 Review in PR
Forget a step         →     Run terraform plan
Wrong region                Run terraform apply
Wrong size                  ✅ Consistent every time
Wrong security group
     │
     ▼
40% error rate              ~0% config error rate
```

---

## 8. Scenario-Based Q&A

---

🔍 **Scenario 1:** Your team manually created 50 EC2 instances for a project. The project ended, but no one knows which instances to delete. The AWS bill is huge.

✅ **Answer:** With Terraform, all resources are tracked in `terraform.tfstate` and defined in code. Running `terraform destroy` would cleanly remove all 50 instances with zero guesswork. Cost goes to $0 immediately. Manual infra leaves "orphaned resources" that bleed money silently.

---

🔍 **Scenario 2:** A new developer joins the team and needs an exact copy of the production environment to test a feature. It takes a week manually. How can this be fixed?

✅ **Answer:** With Terraform, the entire environment is in `.tf` files in GitHub. The new developer clones the repo, sets their AWS credentials, runs `terraform apply`, and has a **perfect replica** of production in minutes. This is the power of IaC — infrastructure is reproducible on demand.

---

🔍 **Scenario 3:** You're asked: "Should we use Terraform or Ansible to install Node.js on our servers?"

✅ **Answer:** **Ansible** — Terraform is for provisioning infrastructure (creating the servers), while Ansible is for configuration management (installing software on servers). You'd use Terraform to create the EC2 instances, then Ansible to SSH in and install Node.js.

---

🔍 **Scenario 4:** You made a small change to your Terraform config (changed instance type from t3.micro to t3.small). What happens when you run `terraform apply`?

✅ **Answer:** Because Terraform uses **immutable infrastructure**, it will **destroy the old t3.micro instance and create a new t3.small instance**. It doesn't modify the existing instance in-place. This is different from Ansible which would modify in-place. Run `terraform plan` first to see this clearly before applying.

---

🔍 **Scenario 5:** Your company's AWS infrastructure has no documentation. A senior engineer who set everything up manually just quit. How can you prevent this in future?

✅ **Answer:** Adopt IaC with Terraform. All infrastructure is written as code in `.tf` files, stored in GitHub. The code **is** the documentation — it shows exactly what exists, why, and how. New engineers can read it, and `terraform plan` shows the current vs desired state.

---

🔍 **Scenario 6:** You ran `terraform apply` and accidentally created resources in the wrong AWS region. How do you fix it fast?

✅ **Answer:** Run `terraform destroy` to remove all the resources in the wrong region. Update the `region` in your provider config, then run `terraform apply` again. Because everything is code, this takes minutes instead of hours of manual cleanup.

---

## 9. Interview Q&A

---

**Q1: What is Terraform and why is it used?**

**A:** Terraform is an open-source Infrastructure as Code (IaC) tool by HashiCorp (2014). It allows teams to define cloud infrastructure using HCL configuration files and provision it automatically via provider APIs. It's used because it eliminates manual errors (which cause 40% of deployment failures), enables consistent reproducible environments, version-controls infrastructure, and works across 6,500+ providers including AWS, Azure, and GCP.

---

**Q2: What is the difference between Terraform and Ansible?**

**A:** Terraform is for **infrastructure provisioning** — creating servers, networks, databases from scratch using HCL. It uses immutable infrastructure (destroys and recreates on changes) and tracks state. Ansible is for **configuration management** — installing software, managing users, patching — on already-existing servers using YAML playbooks. It modifies in-place (mutable). Best practice: use Terraform to create EC2 instances, Ansible to configure them.

---

**Q3: Explain the Terraform workflow — what happens when you run each command?**

**A:**
- `terraform init` — Downloads required provider plugins (e.g., AWS) into `.terraform/` directory
- `terraform plan` — Reads current state (`.tfstate`) and desired state (`.tf` files), computes a diff, shows what will be created/changed/destroyed — no real changes
- `terraform apply` — Executes the plan, calls cloud APIs to create real resources, updates `.tfstate`
- `terraform destroy` — Removes all resources tracked in the state file

---

**Q4: What is `terraform.tfstate` and why is it important?**

**A:** It's a JSON file that Terraform uses to **track the real-world state of resources** it created. It maps your HCL configuration to actual cloud resource IDs (e.g., EC2 instance ID). Without it, Terraform doesn't know what already exists and would try to create everything from scratch. It should be stored remotely (S3 + DynamoDB for locking) in team environments to avoid conflicts.

---

**Q5: What is immutable infrastructure and why does Terraform use it?**

**A:** Immutable infrastructure means you **never modify a running resource** — instead, you destroy it and create a new one with the desired configuration. Terraform uses this approach because it eliminates configuration drift (servers gradually diverging from their intended state), makes changes predictable, and ensures every environment is created from the same clean template. The tradeoff is brief downtime during replacement, addressed by blue-green deployments.

---

**Q6: What is HCL and how is it different from YAML or JSON?**

**A:** HCL (HashiCorp Configuration Language) is a domain-specific language designed to be both human-readable and machine-parseable. Unlike YAML (used by Ansible/Kubernetes), HCL supports expressions, functions, loops, and references natively — making it more powerful for infrastructure logic. Unlike JSON, it supports comments and is less verbose. It uses blocks (`resource "aws_instance" "name" { }`) to organize configuration hierarchically.

---

**Q7: How would you set up Terraform for an AWS project from scratch?**

**A:**
1. Install Terraform binary and add to system PATH
2. Install AWS CLI and run `aws configure` with IAM credentials
3. Create IAM user with appropriate permissions and generate access keys
4. Write `main.tf` with provider and resource blocks
5. Run `terraform init` to download AWS provider
6. Run `terraform plan` to preview resources
7. Run `terraform apply` to create infrastructure
8. Store `terraform.tfstate` remotely (S3 bucket with DynamoDB locking for teams)

---

**Q8: What are Terraform providers and why do they matter?**

**A:** Providers are **plugins** that allow Terraform to interact with specific cloud services or APIs. Each provider (AWS, Azure, GCP, Kubernetes, GitHub, etc.) exposes a set of resources you can manage. Terraform supports 6,546+ providers. When you run `terraform init`, it downloads the specified provider plugin. Without the correct provider, Terraform has no way to talk to that cloud service.

---

**Q9: Why is IaC preferred over manual infrastructure management in production?**

**A:** IaC solves several critical problems: (1) **Reproducibility** — spin up identical environments in minutes; (2) **Version control** — track every infra change in Git with commit history; (3) **Error reduction** — eliminates the 40% of errors caused by manual activities; (4) **Speed** — `terraform apply` in seconds vs hours of clicking; (5) **Disaster recovery** — rebuild everything from code if infra is lost; (6) **Cost control** — `terraform destroy` ensures clean teardown with no forgotten resources.

---

## 10. Tech Stack Mapping

### Where Terraform Fits in the DevOps Pipeline

```
Developer → GitHub → CI/CD Pipeline → Terraform → Cloud Infrastructure → App Deployment
```

### Real-World Usage by Stack

#### Node.js / Next.js Apps on AWS
```
Terraform provisions:
  ├── EC2 instances (app servers)
  ├── RDS (PostgreSQL database)
  ├── ElastiCache (Redis for sessions/caching)
  ├── S3 (static assets for Next.js)
  ├── CloudFront (CDN for S3)
  ├── ALB (Application Load Balancer)
  └── VPC, Subnets, Security Groups

Then: Ansible or Docker deploys Node.js/Next.js app onto EC2
```

#### MongoDB Deployments
```
Terraform provisions:
  ├── EC2 instances for MongoDB cluster
  ├── EBS volumes for persistent storage
  ├── VPC with private subnets
  └── Security groups (port 27017)

Ansible: Installs MongoDB, configures replica set
```

#### Jenkins CI/CD Integration
```
Jenkins Pipeline:
  Stage 1: Checkout code from GitHub
  Stage 2: Run terraform init + terraform plan
  Stage 3: Await approval (manual gate)
  Stage 4: Run terraform apply
  Stage 5: Deploy application onto provisioned infra
  Stage 6: Run smoke tests
```

#### AWS Services Terraform Commonly Manages

| AWS Service | Terraform Resource | Use Case |
|---|---|---|
| EC2 | `aws_instance` | App servers |
| S3 | `aws_s3_bucket` | Static files, state backend |
| RDS | `aws_db_instance` | PostgreSQL, MySQL |
| ElastiCache | `aws_elasticache_cluster` | Redis for Socket.IO |
| Lambda | `aws_lambda_function` | Serverless functions |
| IAM | `aws_iam_role` | Permissions |
| VPC | `aws_vpc` | Network isolation |
| ALB | `aws_lb` | Load balancing |

#### WebSockets / Socket.IO
```
Terraform provisions:
  ├── EC2 instances with sticky sessions enabled on ALB
  ├── Security groups opening port 443 (WSS)
  └── ElastiCache Redis (for Socket.IO adapter - multi-server pub/sub)
```

---

## 11. Code / Practical Examples

### Example 1: Basic Terraform for Node.js EC2

**`provider.tf`**
```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
  # Credentials from: aws configure (or env vars)
}
```

**`main.tf`**
```hcl
# Security Group — allow SSH and HTTP
resource "aws_security_group" "node_app_sg" {
  name        = "node-app-sg"
  description = "Allow SSH and HTTP traffic"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 3000
    to_port     = 3000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# EC2 Instance for Node.js App
resource "aws_instance" "node_server" {
  ami                    = "ami-0c55b159cbfafe1f0"  # Amazon Linux 2
  instance_type          = "t3.micro"               # Free tier eligible
  vpc_security_group_ids = [aws_security_group.node_app_sg.id]

  # Install Node.js on startup
  user_data = <<-EOF
    #!/bin/bash
    curl -sL https://rpm.nodesource.com/setup_18.x | bash -
    yum install -y nodejs git
    echo "Node.js installed" > /var/log/node-install.log
  EOF

  tags = {
    Name        = "NodeJS-App-Server"
    Environment = "dev"
    ManagedBy   = "Terraform"
  }
}

# Output the public IP
output "server_ip" {
  value       = aws_instance.node_server.public_ip
  description = "Public IP of the Node.js server"
}
```

**`variables.tf`**
```hcl
variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "dev"
}
```

---

### Example 2: Remote State Backend (Team Setup)

```hcl
# backend.tf — store tfstate in S3 instead of local machine
terraform {
  backend "s3" {
    bucket         = "my-terraform-state-bucket"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-lock"   # Prevents concurrent applies
    encrypt        = true
  }
}
```

---

### Example 3: Terraform for Full Node.js Stack

```hcl
# S3 bucket for Next.js static assets
resource "aws_s3_bucket" "nextjs_assets" {
  bucket = "my-nextjs-app-assets"

  tags = {
    Name = "NextJS Static Assets"
  }
}

resource "aws_s3_bucket_public_access_block" "nextjs_public" {
  bucket                  = aws_s3_bucket.nextjs_assets.id
  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

# ElastiCache Redis for Socket.IO sessions
resource "aws_elasticache_cluster" "redis" {
  cluster_id           = "socketio-redis"
  engine               = "redis"
  node_type            = "cache.t3.micro"
  num_cache_nodes      = 1
  parameter_group_name = "default.redis7"
  port                 = 6379
}

# Output Redis endpoint for app config
output "redis_endpoint" {
  value = aws_elasticache_cluster.redis.cache_nodes[0].address
}
```

---

### Example 4: Jenkins Pipeline with Terraform

```groovy
// Jenkinsfile
pipeline {
    agent any

    environment {
        AWS_ACCESS_KEY_ID     = credentials('aws-access-key')
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret-key')
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
                sh 'terraform plan -out=tfplan'
                // Archive plan for review
                archiveArtifacts artifacts: 'tfplan'
            }
        }

        stage('Approval') {
            steps {
                // Manual gate — someone must approve before apply
                input message: 'Review plan above. Apply infrastructure changes?',
                      ok: 'Apply'
            }
        }

        stage('Terraform Apply') {
            steps {
                sh 'terraform apply tfplan'
            }
        }

        stage('Deploy App') {
            steps {
                // Get EC2 IP from Terraform output
                script {
                    def serverIp = sh(
                        script: 'terraform output -raw server_ip',
                        returnStdout: true
                    ).trim()
                    echo "Deploying to: ${serverIp}"
                    // Deploy Node.js app via Ansible or Docker
                    sh "ansible-playbook -i ${serverIp}, deploy.yml"
                }
            }
        }
    }

    post {
        failure {
            echo 'Pipeline failed! Infrastructure may need cleanup.'
        }
    }
}
```

---

### Example 5: Dockerfile for Node.js App (Deployed on Terraform-Provisioned EC2)

```dockerfile
# Dockerfile
FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci --only=production

# Copy source code
COPY . .

# Build Next.js app (if applicable)
RUN npm run build

EXPOSE 3000

# Run the app
CMD ["node", "server.js"]
```

```bash
# Deployment commands on EC2 (via Ansible or SSH)
docker pull myapp:latest
docker stop myapp-container || true
docker rm myapp-container || true
docker run -d \
  --name myapp-container \
  --restart unless-stopped \
  -p 3000:3000 \
  -e NODE_ENV=production \
  -e REDIS_URL=redis://$(terraform output -raw redis_endpoint):6379 \
  myapp:latest
```

---

### Example 6: Ansible Playbook (Works After Terraform Creates EC2)

```yaml
# deploy.yml — run after Terraform creates the server
---
- name: Configure Node.js Server
  hosts: all
  become: yes

  tasks:
    - name: Install Node.js
      shell: |
        curl -sL https://rpm.nodesource.com/setup_18.x | bash -
        yum install -y nodejs

    - name: Install PM2 (process manager)
      npm:
        name: pm2
        global: yes

    - name: Clone application
      git:
        repo: "https://github.com/org/myapp.git"
        dest: /var/app

    - name: Install app dependencies
      npm:
        path: /var/app

    - name: Start app with PM2
      shell: pm2 start /var/app/server.js --name myapp
```

---

### Complete Deployment Flow

```
1. Developer writes Terraform code
         ↓
2. Push to GitHub (infra as code, version controlled)
         ↓
3. Jenkins picks up the change (CI/CD trigger)
         ↓
4. terraform init → terraform plan → (human approval) → terraform apply
         ↓
5. EC2, RDS, Redis, S3 provisioned on AWS
         ↓
6. Ansible playbook runs: installs Node.js, PM2, clones app
         ↓
7. Docker container starts: Node.js/Next.js app live
         ↓
8. Health check passes → deployment complete 🚀
```

---

### Quick Reference: Terraform Commands Cheat Sheet

```bash
# Initialize project (download providers)
terraform init

# Preview changes (dry run)
terraform plan

# Preview and save plan to file
terraform plan -out=myplan.tfplan

# Apply changes
terraform apply

# Apply saved plan (no confirmation prompt)
terraform apply myplan.tfplan

# Destroy all resources
terraform destroy

# Show current state
terraform show

# List resources in state
terraform state list

# Get output values
terraform output
terraform output -raw server_ip

# Format .tf files
terraform fmt

# Validate syntax
terraform validate

# Refresh state (sync with real world)
terraform refresh
```

---

## Additional Notes

- **Terraform Certification:** HashiCorp offers official Terraform Associate certification ($70, sometimes $20–30 during sales)
- **Free Tier Tip:** Always use `t3.micro` (not T2) for free-tier eligibility in newer AWS accounts
- **State File Security:** Never commit `terraform.tfstate` to GitHub — it contains sensitive data (IPs, credentials references). Use `.gitignore`
- **Cost Discipline:** Always run `terraform destroy` after labs to avoid surprise AWS bills

---

← Previous: [`41_Grafana_Deep_Dive_Dashboards_Alerting_User_Management_&_Real_World_Monitoring`](41_Grafana_Deep_Dive_Dashboards_Alerting_User_Management_&_Real_World_Monitoring) | Next: [`43_Terraform_Advanced_Commands_State_Management_MultiResource_Provisioning_&_PR_Workflow.md`](43_Terraform_Advanced_Commands_State_Management_MultiResource_Provisioning_&_PR_Workflow.md) →