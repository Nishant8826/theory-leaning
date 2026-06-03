# 51 – Multi-Cloud Comparison (AWS vs GCP vs Azure) & Azure DevOps

> **Batch-43 | 4th Link | Multi-Cloud with AWS + DevOps + AI | 8AM IST**
> Instructor: Vikas (CloudDevOpsHub)

---

## Table of Contents

1. [Why Multi-Cloud?](#1-why-multi-cloud)
2. [Multi-Cloud Services Comparison — Full Map](#2-multi-cloud-services-comparison--full-map)
3. [Service Deep-Dives (What / Why / How / Impact)](#3-service-deep-dives)
   - [Compute (EC2 / Compute Engine / Azure VM)](#31-compute)
   - [Object Storage (S3 / Cloud Storage / Blob Storage)](#32-object-storage)
   - [Managed Database (RDS / Cloud SQL / Azure SQL)](#33-managed-database)
   - [Identity Management (IAM / IAM / Entra ID)](#34-identity-management)
   - [Virtual Network (VPC / VPC / VNet)](#35-virtual-network)
   - [Kubernetes (EKS / GKE / AKS)](#36-kubernetes)
   - [Load Balancer (ELB/ALB/NLB / Cloud LB / Azure LB)](#37-load-balancer)
   - [Messaging & Queues (SQS / Pub-Sub / Service Bus)](#38-messaging--queues)
   - [Notifications (SNS / Event Grid / Service Bus Topics)](#39-notifications)
   - [Monitoring (CloudWatch / Cloud Monitoring / Azure Monitor)](#310-monitoring)
   - [Serverless (Lambda / Cloud Functions / Azure Functions)](#311-serverless)
4. [Azure Hierarchy — Landing Zone](#4-azure-hierarchy--landing-zone)
5. [Azure DevOps Components](#5-azure-devops-components)
6. [Self-Hosted vs Microsoft-Hosted Agents](#6-self-hosted-vs-microsoft-hosted-agents)
7. [Azure Web App (PaaS)](#7-azure-web-app-paas)
8. [Full CI/CD Flow — Azure DevOps + Node.js](#8-full-cicd-flow--azure-devops--nodejs)
9. [Visual Diagrams](#9-visual-diagrams)
10. [Scenario-Based Q&A](#10-scenario-based-qa)
11. [Interview Q&A](#11-interview-qa)
12. [Tech Stack Mapping](#12-tech-stack-mapping)
13. [Code / Practical Examples](#13-code--practical-examples)
14. [Navigation Footer](#navigation-footer)

---

## 1. Why Multi-Cloud?

### What
**Multi-cloud** means using services from more than one cloud provider (AWS + GCP, AWS + Azure, all three) within the same organization or project.

### Why It Matters
- **No vendor lock-in** — You're not dependent on one company's pricing, uptime, or product decisions
- **Best of breed** — Use GCP for AI/ML (Vertex AI, Gemini), AWS for compute scale, Azure for enterprise (Active Directory integration)
- **Compliance** — Some regulations require data in specific regions where only one provider has presence
- **Cost optimization** — Run workloads where pricing is most competitive
- **Redundancy** — If one cloud has an outage, workloads continue on another

### The Core Insight from This Session
> All three clouds offer the **same fundamental services** — just with different names and slight UX differences. If you understand one cloud well, learning the next is mostly a vocabulary exercise.

---

## 2. Multi-Cloud Services Comparison — Full Map

| Service Category | AWS | GCP | Azure |
|---|---|---|---|
| **Compute (VMs)** | EC2 | Compute Engine | Virtual Machine (Azure VM) |
| **Object Storage** | S3 | Cloud Storage | Blob Storage |
| **Managed Database** | RDS | Cloud SQL | Azure SQL Database |
| **Identity & Access** | IAM | Cloud IAM | Entra ID (Active Directory) |
| **Virtual Network** | VPC | VPC | VNet (Virtual Network) |
| **Kubernetes** | EKS | GKE | AKS |
| **Load Balancer** | ELB / ALB / NLB | Cloud Load Balancer | Azure Load Balancer |
| **Message Queue** | SQS | Pub/Sub | Azure Service Bus |
| **Notifications** | SNS | Event Grid | Service Bus Topics |
| **Monitoring** | CloudWatch | Cloud Monitoring | Azure Monitor |
| **Serverless** | Lambda | Cloud Functions | Azure Functions |
| **CI/CD** | CodePipeline | Cloud Build | Azure Pipelines |
| **Container Registry** | ECR | Artifact Registry | Azure Container Registry (ACR) |
| **DNS** | Route 53 | Cloud DNS | Azure DNS |
| **CDN** | CloudFront | Cloud CDN | Azure CDN |
| **Secret Management** | Secrets Manager | Secret Manager | Azure Key Vault |
| **Infrastructure as Code** | CloudFormation | Deployment Manager | ARM Templates / Bicep |

---

## 3. Service Deep-Dives

### 3.1 Compute

**What:** Virtual Machines — rented computers in the cloud. You choose CPU, RAM, OS, and the cloud provider runs the physical hardware.

| AWS EC2 | GCP Compute Engine | Azure VM |
|---|---|---|
| AMI (image) | Machine Image | VM Image |
| Instance Types (t3, m5, c6i) | Machine Types (n2, e2, c3) | VM Sizes (B, D, F series) |
| Security Groups | Firewall Rules | Network Security Groups (NSG) |
| Key Pairs (.pem) | SSH Keys | SSH Keys / Password |
| User Data script | Startup Script | Custom Script Extension |

**Why:** The foundation of cloud computing. Everything else runs on or alongside VMs.

**How — Launch an Azure VM:**
```
Azure Portal → Virtual Machines → Create
→ Select: Region, Image (Ubuntu 22.04), Size (B2s)
→ Authentication: SSH key or password
→ Networking: VNet, Subnet, NSG (open ports)
→ Review + Create → VM ready in ~2 minutes
```

**Impact:** Without VMs, you'd need physical servers — 6-week lead time, capital expense, physical maintenance.

---

### 3.2 Object Storage

**What:** Infinitely scalable storage for unstructured data — files, images, videos, logs, backups, static websites, build artifacts. No file system hierarchy, just buckets (containers) and objects (files) with keys.

| Feature | AWS S3 | GCP Cloud Storage | Azure Blob Storage |
|---|---|---|---|
| Container name | Bucket | Bucket | Container |
| Globally unique name | Yes (S3) | Yes | Yes (within storage account) |
| Static website hosting | Yes | Yes | Yes |
| Storage tiers | Standard, IA, Glacier | Standard, Nearline, Coldline, Archive | Hot, Cool, Archive |
| Lifecycle policies | Yes | Yes | Yes |
| Versioning | Yes | Yes | Yes |

> **Azure Blob vs Azure File Storage:**
> - **Blob Storage** — unstructured objects (images, PDFs, logs, artifacts). Accessed via HTTP/REST API or SDK. Cheaper.
> - **File Storage** — fully managed SMB file share. Can be mounted to VMs like a network drive (`Z:\`). Used when apps expect a traditional file system.

**Why:** Every app needs somewhere to store files that aren't in a database — profile pictures, uploaded documents, backups, deployment artifacts.

---

### 3.3 Managed Database

**What:** Platform-as-a-Service (PaaS) relational databases. The cloud provider manages the OS, DB engine installation, patching, backups, and failover. You just connect and query.

| Feature | AWS RDS | GCP Cloud SQL | Azure SQL Database |
|---|---|---|---|
| Supported engines | MySQL, PostgreSQL, Oracle, SQL Server, MariaDB | MySQL, PostgreSQL, SQL Server | SQL Server (native), MySQL, PostgreSQL |
| Multi-AZ (HA) | Yes | Yes (HA replicas) | Yes (zone-redundant) |
| Read replicas | Yes | Yes | Yes |
| Managed backups | Yes | Yes | Yes |
| Serverless option | Aurora Serverless | — | Azure SQL Serverless |

**Why:** Running your own database on a VM means you manage backups, patching, high availability, failover — all complex and risky. Managed DB handles all of it.

---

### 3.4 Identity Management

**What:** Controls **who** can do **what** on your cloud resources. Authentication (are you who you say?) + Authorization (are you allowed to do this?).

| Feature | AWS IAM | GCP Cloud IAM | Azure Entra ID |
|---|---|---|---|
| Human users | IAM Users | Google Accounts | Azure AD Users |
| Service identity | IAM Roles | Service Accounts | Managed Identities |
| Groups | IAM Groups | Google Groups | Security Groups |
| Policy language | JSON policies | IAM Roles (predefined + custom) | RBAC Roles + Policies |
| SSO capability | AWS SSO | Google Workspace | Entra ID (native SSO) |
| Enterprise identity | AWS Directory Service | Cloud Identity | **Entra ID is the industry standard** |

**Azure Entra ID (formerly Azure Active Directory):**
- This is where Azure shines — Entra ID is used by **millions of enterprises worldwide** for SSO and identity federation
- If your company uses Microsoft 365 (Outlook, Teams), you're already using Entra ID
- Single sign-on: one login gives access to Azure, M365, custom apps, and third-party SaaS tools
- This is a major reason enterprises choose Azure

---

### 3.5 Virtual Network

**What:** An isolated private network in the cloud where your resources live. Controls what talks to what, what's public vs private, and how traffic flows.

| Feature | AWS VPC | GCP VPC | Azure VNet |
|---|---|---|---|
| Subnets | Public + Private subnets per AZ | Subnets per region | Subnets per region |
| Route control | Route Tables | Routes | Route Tables |
| Internet access | Internet Gateway | Cloud Router | Internet Gateway |
| Private connectivity | AWS PrivateLink | Private Service Connect | Private Endpoints |
| Peering | VPC Peering | VPC Peering | VNet Peering |
| DNS | Route 53 (private zones) | Cloud DNS | Azure DNS |

---

### 3.6 Kubernetes

**What:** Managed Kubernetes control plane — the cloud provider runs and maintains the Kubernetes master nodes. You only manage worker nodes (or pay for fully managed node pools).

| Feature | AWS EKS | GCP GKE | Azure AKS |
|---|---|---|---|
| Control plane cost | $0.10/hr (~$73/month) | Free | Free |
| Managed node pools | Yes (Fargate) | Yes (Autopilot) | Yes |
| Autoscaling | Cluster Autoscaler | Cluster Autoscaler | Cluster Autoscaler |
| kubectl | Standard | Standard | Standard |
| Best for | AWS-native integrations | AI/ML workloads | Enterprise + Azure DevOps |

> **Key insight:** All three use the same `kubectl` commands and the same Kubernetes YAML manifests. A Deployment written for EKS works on GKE and AKS with zero changes (besides cloud-specific annotations for load balancers, storage classes, etc.).

---

### 3.7 Load Balancer

**What:** Distributes incoming traffic across multiple servers/pods/containers. Ensures no single instance is overwhelmed and provides failover.

| Type | AWS | GCP | Azure |
|---|---|---|---|
| **HTTP/HTTPS (Layer 7)** | ALB (Application LB) | Cloud HTTP(S) LB | Azure Application Gateway |
| **TCP/UDP (Layer 4)** | NLB (Network LB) | Cloud Network LB | Azure Load Balancer |
| **Classic** | ELB (deprecated) | — | — |
| **DNS-based** | Route 53 (GeoDNS) | Cloud DNS LB | Azure Traffic Manager |

**Layer 7 vs Layer 4:**
- **Layer 7 (HTTP/HTTPS):** Understands web traffic. Can route based on URL path (`/api` → one service), hostnames, headers. Used for web apps.
- **Layer 4 (TCP/UDP):** Handles raw network traffic. Faster, lower latency. Used for databases, game servers, anything non-HTTP.

---

### 3.8 Messaging & Queues

**What:** Message queues decouple services — one service puts a message in a queue, another service picks it up and processes it. They don't need to talk directly or be online at the same time.

> **Analogy:** Like leaving a voicemail. The sender doesn't need the receiver to be available right now. The message waits.

| Feature | AWS SQS | GCP Pub/Sub | Azure Service Bus |
|---|---|---|---|
| Model | Queue (point-to-point) | Publish/Subscribe | Queue + Topics |
| Message retention | Up to 14 days | 7 days (default) | Up to 14 days |
| FIFO support | Yes (FIFO queue) | Ordered topics | Yes |
| Dead-letter queue | Yes | Yes | Yes |
| Push delivery | No (poll only) | Yes | Yes |

**Why:** Without a queue, if Service B is slow or down, requests to Service A back up or fail. With a queue, Service A puts work in the queue and continues. Service B processes when ready.

**DevOps use cases:**
- Build pipeline events → queue → trigger deployment
- Log events → queue → aggregator → monitoring
- User signup → queue → send welcome email asynchronously

---

### 3.9 Notifications

**What:** Fan-out notification services that send alerts/events to multiple subscribers simultaneously — email, SMS, Slack, Lambda, queues.

| Feature | AWS SNS | GCP Event Grid | Azure Service Bus Topics |
|---|---|---|---|
| Fan-out | Yes (1 → many) | Yes (event-driven) | Yes (topics + subscriptions) |
| Targets | Lambda, SQS, HTTP, Email, SMS | Cloud Functions, HTTP, Pub/Sub | Functions, Queues, HTTP |
| Use case | Alerts, events, fan-out triggers | Event-driven microservices | Enterprise messaging |

**DevOps use cases:**
- CloudWatch alarm → SNS → Email to team + PagerDuty + Slack Lambda
- Deployment completed → SNS → multiple team channels notified simultaneously

---

### 3.10 Monitoring

**What:** Collects metrics (CPU, memory, request rate), logs (application output), and traces (request flow across services). Provides dashboards, alerting, and anomaly detection.

| Feature | AWS CloudWatch | GCP Cloud Monitoring | Azure Monitor |
|---|---|---|---|
| Metrics | Yes | Yes | Yes |
| Logs | CloudWatch Logs | Cloud Logging | Log Analytics |
| Dashboards | Yes | Yes | Yes |
| Alerts | CloudWatch Alarms | Alerting Policies | Alert Rules |
| Tracing | X-Ray (separate) | Cloud Trace | Application Insights |
| Custom metrics | Yes | Yes | Yes |

**Why:** Without monitoring, you find out about problems from angry users. With monitoring, you know before users do.

---

### 3.11 Serverless

**What:** Run code in response to events without managing any servers. You upload a function, define a trigger, and the cloud runs it on demand. Pay only when it executes.

| Feature | AWS Lambda | GCP Cloud Functions | Azure Functions |
|---|---|---|---|
| Max execution time | 15 minutes | 60 minutes | 230 seconds (Consumption) |
| Languages | Node.js, Python, Java, Go, Ruby, .NET | Node.js, Python, Go, Java, Ruby, PHP | C#, Java, Python, Node.js, PowerShell |
| Triggers | S3, API GW, SQS, EventBridge, etc. | HTTP, Pub/Sub, GCS, Firestore | HTTP, Timer, Blob, Service Bus, etc. |
| Cold start | Yes | Yes | Yes |
| Max memory | 10 GB | 32 GB | 1.5 GB (Consumption) |

**Why:** No server provisioning, patching, or scaling configuration. Ideal for event-driven tasks, API backends, automation scripts, scheduled jobs.

---

## 4. Azure Hierarchy — Landing Zone

### What
The **Azure Landing Zone** is the organizational hierarchy that structures all Azure resources in an enterprise. It defines how billing, access control, and governance are organized from top to bottom.

> Think of it as the **org chart for your cloud infrastructure.**

### The 5 Levels

```
Tenant (Root)
    └── Management Groups
            └── Subscriptions (Billing units)
                    └── Resource Groups
                            └── Resources
```

---

### Level 1: Tenant (Root)

**What:** The top-level container — represents your entire **organization** in Azure. Created when you sign up for Azure with a company email domain.

**Analogy:** The country — everything else is subdivisions within it.

```
Example: Tenant = "CloudDevOpsHub"
         Tenant ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
         All employees, subscriptions, and resources live here
```

---

### Level 2: Management Groups

**What:** Containers that group **multiple subscriptions** together for applying governance policies at scale.

**Why:** A large company might have 50 subscriptions (one per team, one per environment). You can apply a policy ("no VMs can be created in unapproved regions") at the Management Group level and it cascades to all subscriptions below.

```
Tenant: CloudDevOpsHub
    ├── Management Group: Production
    │       ├── Subscription: Prod-App-Team
    │       └── Subscription: Prod-Data-Team
    ├── Management Group: Development
    │       ├── Subscription: Dev-App-Team
    │       └── Subscription: Dev-Sandbox
    └── Management Group: Corporate
            └── Subscription: IT-Infrastructure
```

---

### Level 3: Subscriptions (Billing Units)

**What:** A subscription is the **billing and access boundary**. Every Azure resource belongs to a subscription. The invoice comes at the subscription level.

**Why:** Separate subscriptions per team/environment allows:
- Independent billing and cost tracking
- Clear budget limits per team
- Access isolation (Dev team can't touch Prod subscription)

**AWS Equivalent:** AWS Account
**GCP Equivalent:** GCP Project (billing is at project level)

```
Subscription: "Prod-App-Team"
├── Owner: CTO
├── Budget: $5,000/month
├── Region lock policy: only ap-south-1 allowed
└── All resources billed here
```

---

### Level 4: Resource Groups

**What:** A **logical container** that groups related Azure resources that share the same lifecycle (created together, deleted together) and the same application/environment.

**Why:**
- Delete a resource group = deletes all resources inside it (great for cleanup)
- Apply access control at group level (give a developer access to only the dev resource group)
- View all costs for one application in one place

**Best Practice:** One resource group per application per environment.

```
Resource Group: "myapp-prod-rg"
├── Azure VM (app server)
├── Azure SQL Database
├── Storage Account (Blob)
├── Azure App Service
└── Application Insights (monitoring)
```

---

### Level 5: Resources

The actual Azure services — VMs, databases, storage accounts, App Services, etc.

### Full Landing Zone Hierarchy

```
Tenant: CloudDevOpsHub (org root)
    │
    ├── Management Group: Production
    │       │
    │       └── Subscription: Prod-Billing
    │               │
    │               ├── Resource Group: webapp-prod-rg
    │               │       ├── Azure App Service (Node.js)
    │               │       ├── Azure SQL DB (PostgreSQL)
    │               │       └── Blob Storage (uploads)
    │               │
    │               └── Resource Group: infra-prod-rg
    │                       ├── Azure VNet
    │                       └── Azure Load Balancer
    │
    └── Management Group: Development
            │
            └── Subscription: Dev-Billing
                    │
                    └── Resource Group: webapp-dev-rg
                            ├── Azure App Service (Node.js dev)
                            └── Azure SQL DB (PostgreSQL dev)
```

**AWS Equivalent Comparison:**

| Azure | AWS |
|---|---|
| Tenant | AWS Organization |
| Management Group | OU (Organizational Unit) |
| Subscription | AWS Account |
| Resource Group | No direct equivalent (tags or CloudFormation stacks) |
| Resources | Resources |

---

## 5. Azure DevOps Components

### What
**Azure DevOps** is Microsoft's all-in-one DevOps platform. It includes everything a software team needs to plan, build, test, and deploy software.

> Think of it as: **Jira + GitHub + Jenkins + Confluence** — all in one platform, tightly integrated with Azure.

### The 5 Components

---

### Boards (≈ Jira)

**What:** Project management and task tracking tool.

**Work item hierarchy:**
```
Epic (large feature)
    └── User Story (feature broken down)
            └── Task (individual work item)
                    └── Bug (defect to fix)
```

**Features:**
- Kanban boards (drag cards across: To Do → In Progress → Done)
- Sprint planning
- Backlogs
- Burndown charts
- Link work items to code commits and pull requests

**Why:** Keeps development organized. Product manager creates stories, developers pick tasks, progress visible to all stakeholders.

---

### Repos (≈ GitHub)

**What:** Centralized Git repository hosting. Full Git support — clone, push, pull, branches, pull requests, code review.

**Features:**
- Unlimited private repositories
- Branch policies (require PR reviews before merging to main)
- Pull request templates
- Code search
- Integration with Boards (close a work item when PR merges)

**Why:** Centralized code storage with built-in access control using Entra ID — no need for a separate GitHub org. Especially useful in enterprises already using Microsoft tools.

---

### Pipelines (≈ Jenkins / GitHub Actions)

**What:** CI/CD automation — automatically build, test, and deploy code when developers push changes.

**Types:**
- **Build Pipeline** — compiles code, runs tests, creates artifacts
- **Release Pipeline** — deploys artifacts to environments

**Defined as YAML:**
```yaml
# azure-pipelines.yml
trigger:
  - main

pool:
  vmImage: 'ubuntu-latest'   # Microsoft-hosted agent

steps:
- task: NodeTool@0
  inputs:
    versionSpec: '20.x'

- script: npm ci && npm test
  displayName: 'Install and Test'
```

**Why:** Automated pipeline = every push is built, tested, and deployed consistently. No manual steps, no "works on my machine."

---

### Test Plans

**What:** Manual and automated test management. Define test cases, execute them, track results.

**Use case:** QA engineers write test cases in Test Plans, execute them against each release, track pass/fail.

---

### Wiki

**What:** Built-in documentation platform — write and organize team knowledge as markdown pages.

**Why:** Keeps docs alongside the code (in the same Azure DevOps project). Runbooks, architecture docs, onboarding guides, API documentation.

---

## 6. Self-Hosted vs Microsoft-Hosted Agents

### What
An **agent** is the machine that actually runs your pipeline jobs — the one that executes `npm install`, `docker build`, `kubectl apply`, etc.

Azure Pipelines offers two types:

---

### Microsoft-Hosted Agents

**What:** Azure provides and manages the build machine. A fresh VM is spun up for each pipeline run, your job runs, then the VM is discarded.

**Pros:**
- Zero setup — just use `pool: vmImage: 'ubuntu-latest'` in YAML
- Always has latest tools (Node.js, Docker, kubectl, etc.)
- No maintenance required

**Cons:**
- **Costs money** — Microsoft-hosted agents have free minutes (1,800 min/month free) but charge after that (~$0.008/minute)
- Slower startup (VM provisioning takes 1–2 minutes)
- No access to private network resources (your VMs, on-prem servers)
- Limited internet egress for private registries

**Best for:** Open-source projects, small teams within free tier limits.

---

### Self-Hosted Agents

**What:** You register your own machine (laptop, EC2, on-prem server) as an agent. Pipelines run on your machine.

**How to set up:**
```
1. Azure DevOps → Project Settings → Agent Pools → New Pool
2. Download agent software to your machine
3. Run configuration script (registers with Azure DevOps)
4. Agent is now available in pipelines

In pipeline YAML:
pool:
  name: 'MyLocalPool'   # your pool name
```

**Pros:**
- **Free** — no per-minute charges, you already own the machine
- Faster — no VM provisioning, dependencies already installed
- Access to private networks (can deploy to internal servers, private DBs)
- Custom tools pre-installed (specific Node version, internal certificates)

**Cons:**
- You maintain the machine (updates, security patches)
- If your machine is offline, pipeline fails
- Not scalable (one machine = one concurrent job)

**Best for:** Learning/development (save costs), enterprise setups with on-prem deployments, access to private resources.

---

### Side-by-Side

| | Microsoft-Hosted | Self-Hosted |
|---|---|---|
| **Setup** | Zero — works immediately | Requires installation + registration |
| **Cost** | Free tier + pay-as-you-go | Your infrastructure cost (or free on laptop) |
| **Startup time** | 1–2 min (VM provision) | Seconds (machine already running) |
| **Maintenance** | Azure handles it | You handle OS + tools |
| **Private network access** | No | Yes |
| **Best for** | Quick start, open source | Cost saving, private infra, enterprise |

---

## 7. Azure Web App (PaaS)

### What
**Azure Web App** is a fully managed Platform-as-a-Service (PaaS) for hosting web applications. You deploy your code (Node.js, Python, Java, .NET, PHP) and Azure handles the server, OS, scaling, SSL, and uptime.

> **Analogy:** If Azure VM is renting a house (you manage everything), Azure Web App is staying in a hotel (they manage everything, you just show up with your bags).

### Why

| Azure VM (IaaS) | Azure Web App (PaaS) |
|---|---|
| You manage OS, runtime, dependencies | Azure manages everything below your code |
| SSH in, configure Nginx, PM2, etc. | Just push code — it runs |
| Manual scaling | Auto-scaling built-in |
| You patch the OS | Azure patches automatically |
| Full control | Less control, but less work |

### Supported Runtimes
- Node.js (10, 12, 14, 16, 18, 20)
- Python (3.8, 3.9, 3.10, 3.11)
- Java (8, 11, 17, 21)
- .NET / .NET Core
- PHP
- Ruby
- Docker containers (custom runtime)

### How — Deploy a Node.js App to Azure Web App

```
1. Azure Portal → App Services → Create
2. Configure:
   - Subscription: your subscription
   - Resource Group: myapp-rg (create new)
   - Name: myapp-devops (becomes myapp-devops.azurewebsites.net)
   - Runtime: Node 20 LTS
   - Region: East US (or your nearest)
   - Plan: Free F1 (dev) or B1 (prod)
3. Review + Create
4. Deploy via Azure Pipelines (automatic on push)
```

### Impact

| With Azure Web App | Without (self-managed VM) |
|---|---|
| Deploy in minutes | Install Nginx, Node, PM2, configure SSL — hours |
| Scale with one click | Manual server provisioning |
| Built-in SSL certificates | Configure and renew manually |
| Built-in deployment slots (staging/prod swap) | Complex manual blue-green setup |

---

## 8. Full CI/CD Flow — Azure DevOps + Node.js

### The Complete Flow

```
Developer writes code on laptop
        │
        │  git push
        ▼
Azure Repos (Git)
        │
        │  push triggers pipeline
        ▼
Azure Pipelines
        │
        │  picks up the job
        ▼
Self-Hosted Agent (local machine / EC2)
        │
        ├── git pull (latest code)
        ├── npm ci (install dependencies)
        ├── npm test (run tests)
        ├── npm run build (compile/bundle)
        │
        │  deploy artifact
        ▼
Azure Web App (PaaS)
        │
        ▼
App live at: https://myapp.azurewebsites.net
```

### Why This Flow Works
1. **Azure Repos** — code is centralized and version-controlled
2. **Pipeline trigger** — no human needs to remember to deploy
3. **Self-hosted agent** — saves cost, faster, can access private resources
4. **Azure Web App** — handles hosting, SSL, scaling — no server management

---

## 9. Visual Diagrams

### Multi-Cloud Services Map

```
SERVICE CATEGORY          AWS              GCP               AZURE
─────────────────────────────────────────────────────────────────────
Compute (VMs)        │   EC2         │ Compute Engine  │ Virtual Machine
Object Storage       │   S3          │ Cloud Storage   │ Blob Storage
Managed DB           │   RDS         │ Cloud SQL       │ Azure SQL DB
Identity & Access    │   IAM         │ Cloud IAM       │ Entra ID (AAD)
Virtual Network      │   VPC         │ VPC             │ VNet
Kubernetes           │   EKS         │ GKE             │ AKS
Load Balancer        │   ALB/NLB     │ Cloud LB        │ Azure LB / App GW
Message Queue        │   SQS         │ Pub/Sub         │ Service Bus
Notifications        │   SNS         │ Event Grid      │ Service Bus Topics
Monitoring           │   CloudWatch  │ Cloud Monitoring│ Azure Monitor
Serverless           │   Lambda      │ Cloud Functions │ Azure Functions
─────────────────────────────────────────────────────────────────────
```

---

### Azure Landing Zone Hierarchy

```
┌─────────────────────────────────────────────────────────────────┐
│  TENANT  (Root — Organization level)                            │
│  e.g., CloudDevOpsHub.onmicrosoft.com                          │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  MANAGEMENT GROUP  (Governance layer)                     │ │
│  │  e.g., Production, Development, Corporate                 │ │
│  │                                                           │ │
│  │  ┌─────────────────────────────────────────────────────┐ │ │
│  │  │  SUBSCRIPTION  (Billing unit)                       │ │ │
│  │  │  e.g., Prod-App-Team ($5k/month budget)             │ │ │
│  │  │                                                     │ │ │
│  │  │  ┌───────────────────────────────────────────────┐ │ │ │
│  │  │  │  RESOURCE GROUP  (Logical container)          │ │ │ │
│  │  │  │  e.g., myapp-prod-rg                          │ │ │ │
│  │  │  │                                               │ │ │ │
│  │  │  │  ┌──────────────────────────────────────────┐│ │ │ │
│  │  │  │  │  RESOURCES                               ││ │ │ │
│  │  │  │  │  VM, DB, Storage, App Service, etc.      ││ │ │ │
│  │  │  │  └──────────────────────────────────────────┘│ │ │ │
│  │  │  └───────────────────────────────────────────────┘ │ │ │
│  │  └─────────────────────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

### Azure DevOps Components

```
AZURE DEVOPS (Project)
        │
        ├── 📋 BOARDS (≈ Jira)
        │       Epics → Stories → Tasks → Bugs
        │       Kanban, Sprints, Backlogs
        │
        ├── 📁 REPOS (≈ GitHub)
        │       Git repositories
        │       Branch policies, PRs, Code review
        │
        ├── ⚙️  PIPELINES (≈ Jenkins)
        │       CI Build pipelines (YAML)
        │       CD Release pipelines
        │       Runs on: Microsoft-Hosted OR Self-Hosted Agents
        │
        ├── 🧪 TEST PLANS
        │       Manual test cases
        │       Automated test results
        │
        └── 📖 WIKI
                Documentation pages (Markdown)
                Runbooks, architecture, onboarding
```

---

### Self-Hosted vs Microsoft-Hosted Agent

```
MICROSOFT-HOSTED:                      SELF-HOSTED:
─────────────────────────────────────────────────────────
Azure Pipelines triggers job           Azure Pipelines triggers job
         │                                      │
         ▼                                      ▼
Azure provisions fresh VM              Your machine picks up job
(ubuntu-latest, ~1-2 min)              (already running, instant)
         │                                      │
  [npm ci]                              [npm ci]
  [npm test]                            [npm test]
  [deploy]                              [deploy to private server]
         │                                      │
         ▼                                      ▼
VM destroyed (ephemeral)               Machine stays running
         │                                      │
    Costs: $$                              Costs: $0
```

---

### Full CI/CD Flow — Azure DevOps

```
Developer (VS Code + GitHub Copilot)
         │
         │  git push origin main
         ▼
Azure Repos
         │
         │  webhook → pipeline triggered
         ▼
Azure Pipelines
         │
    ┌────┴──────────────────────────────────┐
    │  Self-Hosted Agent (local/EC2)        │
    │                                       │
    │  Stage 1: Install                     │
    │    - npm ci                           │
    │                                       │
    │  Stage 2: Test                        │
    │    - npm test                         │
    │                                       │
    │  Stage 3: Build                       │
    │    - npm run build                    │
    │                                       │
    │  Stage 4: Deploy                      │
    │    - az webapp deploy                 │
    └───────────────────┬───────────────────┘
                        │
                        ▼
              Azure Web App (PaaS)
                        │
                        ▼
         https://myapp.azurewebsites.net ✅
```

---

## 10. Scenario-Based Q&A

---

🔍 **Scenario 1:** Your company uses AWS for compute but needs to integrate with Microsoft 365 (Outlook, Teams) for employee identity and SSO. Which Azure service handles this, and can you use it with AWS?

✅ **Answer:** **Azure Entra ID (Active Directory)** handles identity and SSO. Yes, you can use Entra ID with AWS — this is common in enterprises. Set up **AWS IAM Identity Center** (formerly SSO) to federate with Entra ID. Employees log in with their Microsoft credentials (Entra ID) and get access to AWS resources via assumed IAM roles. One login, two clouds.

---

🔍 **Scenario 2:** You're a DevOps engineer at a startup using Azure DevOps. Pipeline minutes are running out mid-month and it's causing CI/CD delays. Your manager wants a free solution. What do you do?

✅ **Answer:** Set up a **self-hosted agent** on your existing EC2 instance or even a developer's laptop. Register it with Azure DevOps Agent Pool. Update the pipeline YAML to use `pool: name: 'MyLocalPool'` instead of `vmImage: ubuntu-latest`. Pipeline runs are now free (you pay for the EC2 or nothing for a local machine). You also get faster builds since there's no VM provisioning delay.

---

🔍 **Scenario 3:** Your team has 5 different applications deployed on Azure. Every time you delete a resource, you accidentally delete something from the wrong app. How does the Azure hierarchy help prevent this?

✅ **Answer:** Organize each application in its own **Resource Group** (e.g., `webapp-prod-rg`, `dataservice-prod-rg`, `analytics-dev-rg`). Apply RBAC at the resource group level so each team only has access to their own group. Now deleting a resource group removes only that application's resources, and team members can't accidentally modify another app's infrastructure. Add Azure Locks (`CanNotDelete`) on production resource groups for extra safety.

---

🔍 **Scenario 4:** You're asked to design a multi-cloud architecture where the app runs on AWS EC2, stores files in both AWS S3 and Azure Blob Storage, and uses GCP Vertex AI for ML inference. The CTO asks if this is feasible. What's your answer?

✅ **Answer:** Yes, this is a standard multi-cloud pattern. Each cloud is being used for what it does best. The Python/Node.js app on EC2 uses the AWS SDK (boto3/aws-sdk) for S3, the Azure Storage SDK for Blob Storage, and the Google Cloud AI SDK for Vertex AI. They all communicate over HTTPS via their respective SDKs — no special infrastructure needed between clouds. Use environment variables to store each cloud's credentials, and ideally use respective secret managers (AWS Secrets Manager, Azure Key Vault, GCP Secret Manager) to avoid hardcoding.

---

🔍 **Scenario 5:** A new engineer on your team understands AWS well but is being asked to work on an Azure project. They're confused by Azure-specific terminology. How do you explain the mental model?

✅ **Answer:** Map it to what they know: "AWS Account = Azure Subscription (billing unit). AWS Organization + OU = Azure Tenant + Management Groups. CloudFormation Stack = Azure Resource Group (logical grouping). IAM = Entra ID. EC2 = Azure VM. S3 = Blob Storage. EKS = AKS. Lambda = Azure Functions. CloudWatch = Azure Monitor." Once the vocabulary clicks, the skills transfer directly — the concepts are identical, the names just differ.

---

🔍 **Scenario 6:** Your Azure pipeline deploys to an Azure Web App, but after deployment the app crashes with a missing environment variable error. How do you debug this?

✅ **Answer:** Azure Web App uses **Application Settings** (under Configuration) for environment variables — equivalent to `.env` files. Check: Azure Portal → App Service → Configuration → Application Settings. The variable may be set in your local `.env` but never added to App Service settings. Add it there (or via pipeline YAML using `AzureAppServiceSettings` task). Never commit `.env` files — use pipeline secrets and App Service configuration.

---

## 11. Interview Q&A

---

**Q1. How does the Azure organizational hierarchy differ from AWS?**

**A:** Azure uses a 5-level hierarchy: Tenant (org root) → Management Groups (governance) → Subscriptions (billing) → Resource Groups (logical containers) → Resources. AWS uses: AWS Organization → Organizational Units (OUs) → AWS Accounts (billing) → Resources. Key difference: Azure has Resource Groups as a first-class organizational layer — there's no direct AWS equivalent. AWS accounts are the billing boundary; Azure Subscriptions are. Azure Management Groups map to AWS OUs. Azure's Tenant (Entra ID) provides richer enterprise identity integration than AWS Organizations.

---

**Q2. What is the difference between Azure Blob Storage and Azure File Storage?**

**A:** Blob Storage stores unstructured objects (files, images, videos, logs, backups) accessed via REST API or SDK — similar to AWS S3. It's optimized for internet-facing access and cost-efficient at scale. File Storage provides a fully managed SMB network file share that can be mounted to Windows and Linux VMs like a network drive (e.g., `Z:\` on Windows or `/mnt/share` on Linux) — similar to AWS EFS. Use Blob for web apps, CI/CD artifacts, backups. Use File Storage when apps expect a traditional file system path (legacy apps, shared configuration directories).

---

**Q3. What is the difference between a self-hosted and Microsoft-hosted Azure Pipelines agent? When would you use each?**

**A:** A Microsoft-hosted agent is a fresh VM provisioned by Azure for each pipeline run — zero maintenance, costs per minute after the free tier, no private network access. A self-hosted agent is your own machine (laptop, EC2, on-prem server) registered with Azure DevOps — free to run (you own the hardware), faster startup, can access private networks, but you maintain it. Use Microsoft-hosted for public repos, simple builds, when you're within the free tier. Use self-hosted to save costs, access private infra (internal servers, private DBs), or when you need custom tools or specific hardware.

---

**Q4. What Azure service is equivalent to AWS Lambda and when would you choose Azure Functions over a VM?**

**A:** Azure Functions is equivalent to AWS Lambda. Choose Functions over a VM when: (1) the workload is event-driven (triggered by HTTP, timer, blob upload, Service Bus message) rather than continuously running, (2) the workload is short-duration (under a few minutes), (3) you want to avoid managing servers entirely, (4) you want to pay only for execution time. Use a VM when the workload runs continuously, needs more than 230 seconds, requires specific OS-level configuration, or needs consistent resources.

---

**Q5. How does Azure DevOps compare to a Jenkins + GitHub + Jira stack?**

**A:** Azure DevOps provides equivalent functionality to all three combined: Boards ≈ Jira (task tracking, sprints, epics), Repos ≈ GitHub (Git hosting, PRs, branch policies), Pipelines ≈ Jenkins (CI/CD automation via YAML). The key advantages of Azure DevOps: tight integration between all components (link a PR to a work item, trigger a pipeline from a commit), single sign-on via Entra ID, no separate tools to install/maintain. The key advantage of the separate-tools approach: more community support, more flexibility, not locked into Microsoft ecosystem.

---

**Q6. What is Azure Entra ID and why is it central to enterprise Azure deployments?**

**A:** Azure Entra ID (formerly Azure Active Directory) is Microsoft's cloud-based identity and access management service. It's central to enterprises because: (1) Most enterprise companies already use Microsoft 365 (Outlook, Teams, SharePoint) — Entra ID is already their identity provider, (2) it enables SSO across Azure, M365, and third-party SaaS apps with one login, (3) it supports MFA, conditional access, and Privileged Identity Management for security compliance, (4) it integrates with on-premises Active Directory for hybrid environments. Unlike AWS IAM (cloud-only), Entra ID bridges cloud and on-premises identity.

---

**Q7. What is a Resource Group in Azure and why is there no direct equivalent in AWS?**

**A:** A Resource Group is a logical container that groups Azure resources sharing the same lifecycle, environment, or application. You can apply RBAC, tags, policies, and budgets at the resource group level, and deleting a resource group deletes all resources inside it. AWS doesn't have a direct equivalent because AWS uses accounts as the primary isolation boundary — within an account, resources are organized via tags and managed via CloudFormation stacks. Azure's Resource Group is more explicit and enforced — every Azure resource must belong to exactly one Resource Group.

---

**Q8. Explain how messaging queues (SQS / Service Bus) help in a microservices deployment on Azure.**

**A:** In a microservices architecture, services need to communicate without tight coupling. Example: when a user uploads a resume to the ATS app, instead of the upload service directly calling the AI screening service (synchronous, fragile), it puts a message in Azure Service Bus. The AI screening service picks up messages from the queue at its own pace. Benefits: (1) if the AI service is slow/down, uploads still work — messages queue up, (2) you can scale the AI service independently based on queue depth, (3) failed screenings are retried automatically via dead-letter queue, (4) no data loss even during service restarts.

---

## 12. Tech Stack Mapping

### Multi-Cloud Tech Stack for a Full-Stack App

| Component | AWS Setup | Azure Setup | GCP Setup |
|---|---|---|---|
| **App Hosting** | EC2 + PM2 | Azure Web App | Compute Engine / Cloud Run |
| **Database** | RDS PostgreSQL | Azure DB for PostgreSQL | Cloud SQL PostgreSQL |
| **File Storage** | S3 | Blob Storage | Cloud Storage |
| **CDN** | CloudFront | Azure CDN | Cloud CDN |
| **DNS** | Route 53 | Azure DNS | Cloud DNS |
| **SSL** | ACM | App Service managed cert | Managed SSL |
| **Secrets** | Secrets Manager | Azure Key Vault | Secret Manager |
| **CI/CD** | CodePipeline + CodeBuild | Azure Pipelines | Cloud Build |
| **Container Registry** | ECR | Azure Container Registry | Artifact Registry |
| **Kubernetes** | EKS | AKS | GKE |
| **Monitoring** | CloudWatch | Azure Monitor + App Insights | Cloud Monitoring |
| **IAM** | IAM Roles | Entra ID + RBAC | Service Accounts |

---

### Azure DevOps Flow for Node.js App

```
Code pushed to Azure Repos (main branch)
         │
         ▼
Azure Pipeline triggered (azure-pipelines.yml)
         │
    ┌────┴─────────────────────────────────┐
    │  Self-Hosted Agent:                  │
    │                                      │
    │  - Node.js 20 pre-installed          │
    │  - npm ci (install deps)             │
    │  - npm test (Jest/Mocha)             │
    │  - npm run build                     │
    │  - az webapp deploy (deploy to PaaS) │
    └────────────────────┬─────────────────┘
                         │
                         ▼
              Azure Web App Service
              (myapp.azurewebsites.net)
                         │
                         ▼
                PostgreSQL on Azure SQL
                (Azure DB for PostgreSQL)
                         │
                         ▼
                Azure Blob Storage
                (user uploads, static assets)
```

---

### Tech Stack — ATS App (Multi-Cloud)

```
User → Azure Web App (Node.js / Python Streamlit)
         │
         ├── Azure Blob Storage (resume PDFs stored here)
         │
         ├── Azure SQL Database (candidate records)
         │
         └── GCP Gemini API (AI resume analysis)
                    │
              Returns: match %, feedback, keywords
```

---

## 13. Code / Practical Examples

### Example 1: Azure Pipelines YAML — Node.js App with Self-Hosted Agent

```yaml
# azure-pipelines.yml
# CI/CD pipeline for Node.js app deploying to Azure Web App

trigger:
  branches:
    include:
      - main
      - develop

pr:
  branches:
    include:
      - main

variables:
  nodeVersion: '20.x'
  webAppName: 'myapp-devops'              # Azure Web App name
  resourceGroup: 'myapp-prod-rg'
  azureSubscription: 'my-azure-service-connection'  # Service connection name

stages:
# ─── STAGE 1: BUILD & TEST ──────────────────────────────────────
- stage: Build
  displayName: 'Build and Test'
  jobs:
  - job: Build
    displayName: 'Build Job'
    pool:
      name: 'MyLocalPool'        # Self-hosted agent pool name
      # For Microsoft-hosted, replace above with:
      # vmImage: 'ubuntu-latest'

    steps:
    - task: NodeTool@0
      displayName: 'Install Node.js'
      inputs:
        versionSpec: $(nodeVersion)

    - script: |
        echo "Node version: $(node --version)"
        echo "npm version: $(npm --version)"
      displayName: 'Verify Node.js'

    - script: npm ci
      displayName: 'Install Dependencies'

    - script: npm test
      displayName: 'Run Tests'
      env:
        NODE_ENV: test

    - script: npm run build
      displayName: 'Build Application'

    - task: ArchiveFiles@2
      displayName: 'Archive build output'
      inputs:
        rootFolderOrFile: '$(System.DefaultWorkingDirectory)'
        includeRootFolder: false
        archiveType: 'zip'
        archiveFile: '$(Build.ArtifactStagingDirectory)/$(Build.BuildId).zip'
        replaceExistingArchive: true

    - publish: $(Build.ArtifactStagingDirectory)/$(Build.BuildId).zip
      displayName: 'Publish Artifact'
      artifact: drop

# ─── STAGE 2: DEPLOY ────────────────────────────────────────────
- stage: Deploy
  displayName: 'Deploy to Azure Web App'
  dependsOn: Build
  condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))

  jobs:
  - deployment: Deploy
    displayName: 'Deploy Job'
    environment: 'production'   # Requires approval if configured
    pool:
      name: 'MyLocalPool'

    strategy:
      runOnce:
        deploy:
          steps:
          - task: AzureWebApp@1
            displayName: 'Deploy to Azure Web App'
            inputs:
              azureSubscription: $(azureSubscription)
              appType: 'webAppLinux'
              appName: $(webAppName)
              package: '$(Pipeline.Workspace)/drop/$(Build.BuildId).zip'
              runtimeStack: 'NODE|20-lts'
              startUpCommand: 'npm start'
```

---

### Example 2: Azure Pipelines YAML — Python/Streamlit ATS App

```yaml
# azure-pipelines-ats.yml
# Pipeline for Python Streamlit ATS app

trigger:
  - main

pool:
  name: 'MyLocalPool'   # self-hosted (free)

variables:
  pythonVersion: '3.12'
  webAppName: 'ats-ai-app'

steps:
- task: UsePythonVersion@0
  displayName: 'Set Python version'
  inputs:
    versionSpec: $(pythonVersion)

- script: |
    python -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
  displayName: 'Install Dependencies'

- script: |
    source venv/bin/activate
    python -m pytest tests/ -v
  displayName: 'Run Tests'
  continueOnError: false

# Store Gemini API key as a pipeline secret variable
# In Azure DevOps: Pipeline → Variables → Add GOOGLE_API_KEY (secret)
- script: |
    mkdir -p .streamlit
    echo "GOOGLE_API_KEY = \"$GOOGLE_API_KEY\"" > .streamlit/secrets.toml
  displayName: 'Create Streamlit Secrets'
  env:
    GOOGLE_API_KEY: $(GOOGLE_API_KEY)    # pipeline secret variable

- task: AzureWebApp@1
  displayName: 'Deploy to Azure Web App'
  inputs:
    azureSubscription: 'my-azure-service-connection'
    appType: 'webAppLinux'
    appName: $(webAppName)
    package: '$(System.DefaultWorkingDirectory)'
    runtimeStack: 'PYTHON|3.12'
    startUpCommand: 'streamlit run app.py --server.port 8000 --server.address 0.0.0.0'
```

---

### Example 3: Self-Hosted Agent Setup Script

```bash
#!/bin/bash
# setup_azure_agent.sh
# Registers this machine as a self-hosted Azure DevOps agent

set -e

AGENT_VERSION="3.236.1"
AZURE_DEVOPS_URL="https://dev.azure.com/YOUR_ORG"
AGENT_POOL="MyLocalPool"
AGENT_NAME="$(hostname)-agent"

echo "=== Downloading Azure DevOps Agent ==="
mkdir -p ~/azure-agent && cd ~/azure-agent
curl -fsSL "https://vstsagentpackage.azureedge.net/agent/${AGENT_VERSION}/vsts-agent-linux-x64-${AGENT_VERSION}.tar.gz" \
     -o agent.tar.gz
tar -xzf agent.tar.gz
rm agent.tar.gz

echo "=== Configuring Agent ==="
echo "You'll need a Personal Access Token (PAT) from Azure DevOps:"
echo "  Azure DevOps → User Settings → Personal Access Tokens"
echo "  Scope: Agent Pools (Read & Manage)"
echo ""

./config.sh \
  --unattended \
  --url "$AZURE_DEVOPS_URL" \
  --auth pat \
  --token "$AZURE_DEVOPS_PAT" \    # export this env var before running
  --pool "$AGENT_POOL" \
  --agent "$AGENT_NAME" \
  --acceptTeeEula

echo "=== Installing as a Service (runs on boot) ==="
sudo ./svc.sh install
sudo ./svc.sh start

echo "✅ Agent '$AGENT_NAME' registered to pool '$AGENT_POOL'"
echo "   Check in Azure DevOps: Project Settings → Agent Pools"
```

---

### Example 4: Multi-Cloud SDK Usage — Node.js

```javascript
// multicloud-storage.js
// Uses AWS S3, Azure Blob, and GCP Storage from one Node.js app
// Demonstrates how multi-cloud SDK usage works in practice

const { S3Client, PutObjectCommand } = require('@aws-sdk/client-s3');
const { BlobServiceClient } = require('@azure/storage-blob');
const { Storage } = require('@google-cloud/storage');
const fs = require('fs');

// ─── AWS S3 Upload ─────────────────────────────────────────────
async function uploadToS3(filePath, bucketName, key) {
    const client = new S3Client({ region: process.env.AWS_REGION });
    const fileContent = fs.readFileSync(filePath);

    await client.send(new PutObjectCommand({
        Bucket: bucketName,
        Key: key,
        Body: fileContent,
        ServerSideEncryption: 'AES256'
    }));
    console.log(`✅ S3: Uploaded to s3://${bucketName}/${key}`);
}

// ─── Azure Blob Storage Upload ─────────────────────────────────
async function uploadToAzureBlob(filePath, containerName, blobName) {
    const connectionString = process.env.AZURE_STORAGE_CONNECTION_STRING;
    const client = BlobServiceClient.fromConnectionString(connectionString);
    const containerClient = client.getContainerClient(containerName);
    const blockBlobClient = containerClient.getBlockBlobClient(blobName);

    const fileContent = fs.readFileSync(filePath);
    await blockBlobClient.upload(fileContent, fileContent.length);
    console.log(`✅ Azure: Uploaded to ${containerName}/${blobName}`);
}

// ─── GCP Cloud Storage Upload ──────────────────────────────────
async function uploadToGCS(filePath, bucketName, destFileName) {
    const storage = new Storage(); // uses GOOGLE_APPLICATION_CREDENTIALS env var
    const bucket = storage.bucket(bucketName);
    await bucket.upload(filePath, { destination: destFileName });
    console.log(`✅ GCP: Uploaded to gs://${bucketName}/${destFileName}`);
}

// ─── Example Usage ─────────────────────────────────────────────
async function syncResumeToAllClouds(localPdfPath, candidateId) {
    const timestamp = new Date().toISOString().split('T')[0];
    const key = `resumes/${timestamp}/${candidateId}.pdf`;

    // Upload to all three clouds simultaneously
    await Promise.all([
        uploadToS3(localPdfPath, process.env.S3_BUCKET, key),
        uploadToAzureBlob(localPdfPath, 'resumes', key.replace(/\//g, '-')),
        uploadToGCS(localPdfPath, process.env.GCS_BUCKET, key)
    ]);

    console.log('✅ Resume synced to all three clouds');
}
```

---

### Example 5: Azure Resource Group Deployment via Azure CLI

```bash
#!/bin/bash
# deploy_azure_resources.sh
# Creates the full Azure resource hierarchy for the ATS app

TENANT_ID="your-tenant-id"
SUBSCRIPTION_ID="your-subscription-id"
RESOURCE_GROUP="ats-app-prod-rg"
LOCATION="eastus"
APP_NAME="ats-ai-app"
STORAGE_ACCOUNT="atsresumestorage"

echo "=== [1/5] Login to Azure ==="
az login --tenant $TENANT_ID
az account set --subscription $SUBSCRIPTION_ID

echo "=== [2/5] Create Resource Group ==="
az group create \
    --name $RESOURCE_GROUP \
    --location $LOCATION \
    --tags Environment=Production App=ATS Team=DevOps

echo "=== [3/5] Create Storage Account (Blob) ==="
az storage account create \
    --name $STORAGE_ACCOUNT \
    --resource-group $RESOURCE_GROUP \
    --location $LOCATION \
    --sku Standard_LRS \
    --kind StorageV2

# Create a container for resumes
az storage container create \
    --name resumes \
    --account-name $STORAGE_ACCOUNT \
    --public-access off

echo "=== [4/5] Create Azure Web App ==="
# Create App Service Plan
az appservice plan create \
    --name ats-app-plan \
    --resource-group $RESOURCE_GROUP \
    --sku B1 \
    --is-linux

# Create Web App with Python runtime
az webapp create \
    --name $APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --plan ats-app-plan \
    --runtime "PYTHON:3.12"

echo "=== [5/5] Set App Configuration (env vars) ==="
az webapp config appsettings set \
    --name $APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --settings \
        GOOGLE_API_KEY="@Microsoft.KeyVault(SecretUri=https://ats-keyvault.vault.azure.net/secrets/gemini-key/)" \
        AZURE_STORAGE_ACCOUNT="$STORAGE_ACCOUNT" \
        ENVIRONMENT="production"

echo ""
echo "✅ Azure resources deployed!"
echo "App URL: https://${APP_NAME}.azurewebsites.net"
```

---

### Example 6: Dockerfile for Azure Web App Deployment (Node.js)

```dockerfile
# Dockerfile – Node.js app for Azure Web App (Linux Container)

FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# ─────────────────────────────────────────────────────────────────
FROM node:20-alpine AS production

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

COPY --from=builder /app/dist ./dist

RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

# Azure Web App uses port 8080 by default for containers
# Set WEBSITES_PORT=3000 in App Service Configuration if using port 3000
EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD wget -qO- http://localhost:3000/health || exit 1

CMD ["node", "dist/server.js"]
```

```yaml
# azure-pipelines-docker.yml
# Build Docker image and push to Azure Container Registry

trigger:
  - main

pool:
  name: 'MyLocalPool'

variables:
  acrName: 'myappacr'
  imageName: 'nodejs-app'
  imageTag: $(Build.BuildId)

steps:
- task: Docker@2
  displayName: 'Build and Push to ACR'
  inputs:
    containerRegistry: 'my-acr-service-connection'
    repository: $(imageName)
    command: 'buildAndPush'
    Dockerfile: '**/Dockerfile'
    tags: |
      $(imageTag)
      latest

- task: AzureWebAppContainer@1
  displayName: 'Deploy Container to Azure Web App'
  inputs:
    azureSubscription: 'my-azure-service-connection'
    appName: 'myapp-devops'
    containers: '$(acrName).azurecr.io/$(imageName):$(imageTag)'
```

---

## Navigation Footer

**Previous:** `50_ATS_Project_Kubernetes_Concepts.md` (50_ATS_Project_Kubernetes_Concepts) | **Next:** `52_[Next_Topic_Name].md` (52_Next_Topic_Name)