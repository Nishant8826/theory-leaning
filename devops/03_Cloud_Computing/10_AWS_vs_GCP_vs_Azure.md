# 🏆 AWS vs GCP vs Azure — Simple Comparison

---

## 📌 The Big Three Cloud Providers

| | AWS | Azure | GCP |
|---|-----|-------|-----|
| **Full Name** | Amazon Web Services | Microsoft Azure | Google Cloud Platform |
| **By** | Amazon | Microsoft | Google |
| **Launched** | 2006 | 2010 | 2008 |
| **Market Share** | ~32% (Largest) | ~23% (Second) | ~10% (Third) |
| **Best For** | Everything (most services) | Microsoft/Enterprise | Data & AI/ML |

---

## 📌 Service-by-Service Comparison

| Category | AWS | Azure | GCP |
|----------|-----|-------|-----|
| **Virtual Servers** | EC2 | Virtual Machines | Compute Engine |
| **Serverless** | Lambda | Azure Functions | Cloud Functions |
| **Containers** | ECS / EKS | AKS | GKE |
| **Object Storage** | S3 | Blob Storage | Cloud Storage |
| **Block Storage** | EBS | Managed Disks | Persistent Disks |
| **SQL Database** | RDS | Azure SQL | Cloud SQL |
| **NoSQL Database** | DynamoDB | Cosmos DB | Firestore |
| **Data Warehouse** | Redshift | Synapse Analytics | BigQuery |
| **CDN** | CloudFront | Azure CDN | Cloud CDN |
| **DNS** | Route 53 | Azure DNS | Cloud DNS |
| **Load Balancer** | ALB / NLB | Azure Load Balancer | Cloud Load Balancing |
| **Identity (IAM)** | IAM | Azure AD / Entra ID | Cloud IAM |
| **Monitoring** | CloudWatch | Azure Monitor | Cloud Monitoring |
| **AI/ML** | SageMaker | Azure ML | Vertex AI |
| **Kubernetes** | EKS | AKS | GKE (Best!) |

---

## 📌 When to Use Which?

### ☁️ Choose **AWS** When:

- You want the **most services** (200+ services — more than anyone)
- You're a **startup** (AWS has great free tier & startup programs)
- You need **maximum flexibility** and options
- You want the **largest community** and most tutorials online
- You're preparing for **cloud certifications** (AWS certs are most popular)

> **Best for:** Startups, general-purpose cloud, e-commerce, media streaming
>
> **Who uses it:** Netflix, Airbnb, NASA, Samsung, Flipkart

---

### 🔷 Choose **Azure** When:

- Your company already uses **Microsoft products** (Windows, Office 365, Teams)
- You need **enterprise features** and corporate support
- You're building **hybrid cloud** (Azure has best hybrid tools with Azure Arc)
- Government or regulated industries (Azure has most **compliance certifications**)
- You use **.NET** or **Visual Studio** for development

> **Best for:** Enterprise/corporate, hybrid cloud, government, .NET developers
>
> **Who uses it:** Coca-Cola, BMW, HP, Indian Government portals

---

### 🟡 Choose **GCP** When:

- You're working with **big data and analytics** (BigQuery is amazing!)
- You need **AI and Machine Learning** tools (Google is the leader in AI)
- You're using **Kubernetes** (Google invented it, GKE is the best implementation)
- You want **simplicity** and clean pricing (GCP is known for simpler interface)
- You use **Google Workspace** (Gmail, Google Docs, etc.)

> **Best for:** Data analytics, AI/ML, Kubernetes, data engineering
>
> **Who uses it:** Spotify, Twitter, PayPal, HSBC, Snapchat

---

## 📌 Pricing Comparison (Approximate)

| Resource | AWS | Azure | GCP |
|----------|-----|-------|-----|
| Small VM (2 CPU, 4GB RAM) | ~$35/month | ~$35/month | ~$30/month |
| Object Storage (100 GB) | ~$2.30/month | ~$2.00/month | ~$2.00/month |
| Managed SQL DB (small) | ~$15/month | ~$15/month | ~$12/month |
| Free Tier | 12 months | 12 months | Always Free + 90-day trial |

> **Note:** GCP is often slightly cheaper. All three offer **free tiers** for beginners!

---

## 📌 Free Tier Comparison

| Feature | AWS Free Tier | Azure Free Tier | GCP Free Tier |
|---------|-------------|-----------------|---------------|
| **Duration** | 12 months | 12 months | Always free (some) + $300 credit |
| **VMs** | 750 hrs/month (t2.micro) | 750 hrs/month (B1S) | 1 f1-micro instance (always free) |
| **Storage** | 5 GB S3 | 5 GB Blob | 5 GB Cloud Storage |
| **Database** | 750 hrs RDS | 250 GB SQL | 1 GB Firestore |
| **Serverless** | 1M Lambda requests | 1M Function requests | 2M Cloud Function requests |

---

## 📌 Strengths & Weaknesses

### AWS

| ✅ Strengths | ❌ Weaknesses |
|-------------|-------------|
| Most services (200+) | Complex pricing (hard to predict bills) |
| Largest community | Can be overwhelming for beginners |
| Most mature platform | UI is not the prettiest |
| Best documentation | Cost can add up if not careful |

### Azure

| ✅ Strengths | ❌ Weaknesses |
|-------------|-------------|
| Best Microsoft integration | Sometimes confusing naming |
| Strong enterprise support | Steeper learning curve |
| Best hybrid cloud (Arc) | Outages have been frequent |
| Most compliance certs | Portal can be slow |

### GCP

| ✅ Strengths | ❌ Weaknesses |
|-------------|-------------|
| Best for AI/ML & Data | Fewer services than AWS/Azure |
| Cleanest interface | Smaller community |
| Best Kubernetes (GKE) | Less enterprise adoption |
| Simple pricing | Fewer regions than AWS/Azure |

---

## 📌 Decision Flowchart

```
START: Which cloud should I pick?
│
├── Are you a beginner learning cloud?
│   └── YES → Start with AWS (most tutorials and jobs)
│
├── Does your company use Microsoft products?
│   └── YES → Choose Azure
│
├── Are you working with AI/ML or Big Data?
│   └── YES → Choose GCP
│
├── Are you building a startup?
│   └── YES → AWS or GCP (best free tiers)
│
├── Do you need Kubernetes?
│   └── YES → GCP (best K8s support)
│
├── Do you need hybrid cloud?
│   └── YES → Azure (Azure Arc)
│
└── Not sure?
    └── Start with AWS → It's the safest choice
```

---

## 📌 Job Market Perspective

| Cloud | Job Demand | Average Salary (India) | Certifications |
|-------|-----------|----------------------|----------------|
| **AWS** | Highest (most demanded) | ₹8-25 LPA | Solutions Architect, DevOps Engineer |
| **Azure** | High (growing fast) | ₹7-22 LPA | AZ-900, AZ-104, AZ-400 |
| **GCP** | Growing (data/ML roles) | ₹8-24 LPA | Cloud Engineer, Data Engineer |

> **Advice for beginners:** Learn **AWS first** (most job opportunities), then add Azure or GCP based on your career path.

---

## 🧠 Quick Revision (Interview Ready)

- **AWS** = Largest, most services, best for startups & general use
- **Azure** = Best for Microsoft shops, enterprise, hybrid cloud
- **GCP** = Best for AI/ML, Big Data, Kubernetes
- All three offer **free tiers** — great for learning!
- **Market share:** AWS (~32%) > Azure (~23%) > GCP (~10%)
- **For jobs:** AWS is most in-demand, followed by Azure
- **Key services to know:**
  - Compute: EC2 / VMs / Compute Engine
  - Storage: S3 / Blob / Cloud Storage
  - Database: RDS / Azure SQL / Cloud SQL
  - Serverless: Lambda / Functions / Cloud Functions
- **Start with AWS** if you're unsure — it's the industry standard

---

> 📁 **Back to:** [README — Table of Contents →](./README.md)
