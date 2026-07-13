# ♾️ DevOps – Complete Revision Guide

Welcome to the DevOps Complete Revision Guide. This guide aggregates all key concepts, commands, configurations, best practices, and interview questions across all 57 lessons in this module. It is designed to allow you to revise the entire curriculum in under 30 minutes from a single file.

---

## 📌 Module Navigation

* [01. DevOps Basics](#01-devops-basics)
* [02. Cloud Platforms & Introduction to AI](#02-cloud-platforms-introduction-to-ai)
* [03. 🤖 03: Artificial Intelligence A Beginner's Guide](#03-artificial-intelligence-a-beginners-guide)
* [04. ☁️ Cloud Computing & Data Centers](#04-cloud-computing-data-centers)
* [05. 🛠️ Scripts, Docker & VM Setup Practical Reference](#05-scripts-docker-vm-setup-practical-reference)
* [06. DevOps Basics: Tools, Phases, and Roles](#06-devops-basics-tools-phases-and-roles)
* [07. 🖥️ Linux, OS and GitHub Basics](#07-linux-os-github-basics)
* [08. 🐧 Linux, SSH and Basic Commands](#08-linux-commands-concepts)
* [09. 🐧 Linux Monitoring, Scripting and Permissions](#09-linux-commands-concepts-intermediate-part-2)
* [10. 🐧 Linux, VI Editor and Package Management](#10-linux-commands-concepts-intermediate-part-3)
* [11. 🐧 Linux Troubleshooting, Logs and Services](#11-linux-commands-concepts-intermediate-part-4)
* [12. ☁️ AWS Basics and Cloud Introduction](#12-aws-fundamentals-part-1)
* [13. ☁️ AWS IAM & EC2 Hands-on Guide](#13-aws-iam-ec2-hands-on-guide)
* [14. ⚖️ Scaling, EC2, AMI & Load Balancers Essentials](#14-scaling-ec2-ami-load-balancers-essentials)
* [15. ☁️ AWS EC2, AMI, EBS & Load Balancers Deep Dive](#15-aws-ec2-ami-ebs-load-balancers-deep-dive)
* [16. 🐧 Linux Practical Session (Hands-on DevOps Basics)](#16-linux-practical-session-hands-on-devops-basics)
* [17. ☁️ AWS S3: Complete Guide and Static Website Hosting](#17-aws-s3-complete-guide-and-static-website-hosting)
* [18. S3 Storage Classes, Lifecycle Policies & RDS Introduction](#18-s3-storage-classes-lifecycle-policies-rds-introduction)
* [19. AWS RDS & Database Fundamentals](#19-aws-rds-database-fundamentals)
* [20. AWS RDS MySQL Setup & Management (Hands-On)](#20-aws-rds-mysql-setup-management-hands-on)
* [21. 🌐 AWS VPC & Networking Complete Beginner's Guide](#21-aws-vpc-networking-complete-beginners-guide)
* [22. VPC Networking NACL, CIDR, VPC Peering & Transit Gateway](#22-vpc-networking-nacl-cidr-vpc-peering-transit-gateway)
* [23. AWS CloudWatch Monitoring & Billing Management](#23-aws-cloudwatch-monitoring-billing-management)
* [24. AWS Lambda & Serverless Architecture](#24-aws-lambda-serverless-architecture)
* [25. Git & GitHub Fundamentals](#25-git-github-fundamentals)
* [26. Git & GitHub Deep Dive: Branching, PRs & Collaboration](#26-git-github-deep-dive-branching-prs-collaboration)
* [27. Introduction to CI/CD and Jenkins](#27-introduction-to-cicd-and-jenkins)
* [28. Jenkins Deep Dive: Users, RBAC, CI Pipelines & Local Setup](#28-jenkins-deep-dive-users-rbac-ci-pipelines-local-setup)
* [29. Java, Spring Boot, Maven & Jenkins Build Pipeline](#29-java-spring-boot-maven-jenkins-build-pipeline)
* [30. Jenkins Pipelines: Declarative, Scripted & CI Integration](#30-jenkins-pipelines-declarative-scripted-ci-integration)
* [31. Jenkins Master-Slave Architecture & Node Configuration](#31-jenkins-master-slave-architecture-node-configuration)
* [32. Jenkins Day-to-Day Operations, Parameterized Jobs & AWS Core Services](#32-jenkins-day-to-day-operations-parameterized-jobs-aws-core-services)
* [33. Introduction to Docker: Containers, Images & Architecture](#33-introduction-to-docker-containers-images-architecture)
* [34. Docker Day 2: Container Operations, Port Mapping, Volumes & Management](#34-docker-day-2-container-operations-port-mapping-volumes-management)
* [35. Dockerfiles, Custom Images, Docker Hub & Troubleshooting](#35-dockerfiles-custom-images-docker-hub-troubleshooting)
* [36. Docker Day 4: Image Optimization, Multi-Stage Builds, Container Registries & Docker vs Kubernetes](#36-docker-day-4-image-optimization-multi-stage-builds-container-registries-docker-vs-kubernetes)
* [37. Kubernetes: Introduction, Architecture, Clusters, Namespaces & kubectl](#37-kubernetes-introduction-architecture-clusters-namespaces-kubectl)
* [38. Kubernetes Day 2: Pods, Deployments, Services, ReplicaSets, StatefulSets & Persistent Volumes](#38-kubernetes-day-2-pods-deployments-services-replicasets-statefulsets-persistent-volumes)
* [39. Kubernetes Microservices Deployment: Monolithic vs Microservices, GKE & Real-World E-Commerce App](#39-kubernetes-microservices-deployment-monolithic-vs-microservices-gke-real-world-e-commerce-app)
* [40. Kubernetes Advanced: Horizontal Pod Autoscaling (HPA) & Troubleshooting](#40-kubernetes-advanced-horizontal-pod-autoscaling-hpa-troubleshooting)
* [41. Kubernetes Monitoring: Prometheus, Grafana & Helm](#41-kubernetes-monitoring-prometheus-grafana-helm)
* [42. Grafana Deep Dive: Dashboards, Alerting, User Management & Real-World Monitoring](#42-grafana-deep-dive-dashboards-alerting-user-management-real-world-monitoring)
* [43. Terraform & Infrastructure as Code (IaC)](#43-terraform-infrastructure-as-code-iac)
* [44. Terraform Day 2: IaC Commands, Code Structure & AWS Workflow](#44-terraform-day-2-iac-commands-code-structure-aws-workflow)
* [45. Deploying 3-Tier Architecture on AWS using Terraform (IaC)](#45-deploying-3-tier-architecture-on-aws-using-terraform-iac)
* [46. Ansible: Configuration Management & Automation](#46-ansible-configuration-management-automation)
* [47. Ansible Playbooks, Roles & Tower](#47-ansible-playbooks-roles-tower)
* [48. Python for DevOps Automation](#48-python-for-devops-automation)
* [49. Shell Scripting with Linux (Bash)](#49-shell-scripting-with-linux-bash)
* [50. Prompt Engineering for DevOps & AI](#50-prompt-engineering-for-devops-ai)
* [51. Multi-Cloud ATS App (AWS and GCP) & Kubernetes Concepts](#51-multi-cloud-ats-app-aws-and-gcp-kubernetes-concepts)
* [52. Multi-Cloud Comparison (AWS vs GCP vs Azure) & Azure DevOps](#52-multi-cloud-comparison-aws-vs-gcp-vs-azure-azure-devops)
* [53. Splunk (Log Analytics) & Docker Compose](#53-splunk-log-analytics-docker-compose)
* [54. Kafka on Kubernetes using Strimzi Operator](#54-kafka-on-kubernetes-using-strimzi-operator)
* [55. Complete CI/CD Pipeline: Jenkins, Docker & AWS (Node.js App)](#55-complete-cicd-pipeline-jenkins-docker-aws-nodejs-app)
* [56. DevSecOps: Jenkins, Trivy & SonarQube on AWS](#56-devsecops-jenkins-trivy-sonarqube-on-aws)
* [57. MLOps: FastAPI, Docker & AWS EKS (IT Career Prediction System)](#57-mlops-fastapi-docker-aws-eks-it-career-prediction-system)
* [99. Real-World DevOps Problems: Common & Rare (Remediation Playbook)](#99-real-world-devops-problems-common-rare-remediation-playbook)

---

## 01. DevOps Basics

🔗 **Full Lesson:** [01_DevOps_Basics.md](./01_DevOps_Basics.md)

* **What**: Introduction and foundational concepts of DevOps Basics.
* **Why It Exists**: In traditional software development, developers would write code and "throw it over the wall" to the operations team to deploy and manage. This often led to friction, slow releases, and manual errors.
* **Key Concepts**:
  * **What is DevOps?**
    * **Development:** Focuses on creating new features and fixing bugs.
    * **Operations:** Focuses on stability, security, and maintenance of the infrastructure.
    * **Faster Delivery:** Release features to customers multiple times a day instead of once every few months.
    * **Automation:** Reduce manual work and human error in testing, deployment, and infrastructure setup.
  * **Roles and Responsibilities in DevOps**
    * **Responsibilities:** Automating the software development lifecycle (SDLC), managing CI/CD pipelines, and ensuring smooth deployments.
    * **Skills:** Scripting (Python, Bash), CI/CD tools, Cloud knowledge (AWS/Azure/GCP), Linux.
    * **Tools:** Jenkins, GitLab CI, Git, Docker, Kubernetes, Terraform.
    * **Responsibilities:** Ensuring system uptime, performance, and reliability. They focus on "Service Level Objectives" (SLOs) and "Error Budgets."
  * **Tools and Technologies Used in DevOps**
    * **Tools:** Git (the standard), GitHub, GitLab, Bitbucket.
    * **Tools:** Jenkins, GitHub Actions, GitLab CI, CircleCI.
    * **Tools:** Docker, Podman.
    * **Tools:** Kubernetes (K8s), OpenShift.
  * **Clear DevOps Roadmap for Beginners**
    * **Fundamentals**: Learn Linux shell basics, networking (IP/DNS/HTTP), Git version control, and python/bash scripting.
    * **Advanced**: Master containerization (Docker), orchestration (Kubernetes), infrastructure as code (Terraform), and cloud fundamentals (AWS).
    * **Ops & Security**: Set up monitoring dashboards (Prometheus/Grafana) and security scanners (DevSecOps).

### Key Commands / Code Example:

```
┌─────────────────────────────────────────────────────────────────┐
│                    THE DEVOPS INFINITY LOOP                      │
│                                                                 │
│        PLAN ──► CODE ──► BUILD ──► TEST                         │
│          ▲                              │                       │
│          │        DEV SIDE              │                       │
│          │  ─────────────────────────   │                       │
│          │        OPS SIDE              │                       │
│          │                              ▼                       │
│       MONITOR ◄── OPERATE ◄── DEPLOY ◄── RELEASE               │
│                                                                 │
│   The cycle NEVER ends — continuous improvement!                │
└─────────────────────────────────────────────────────────────────┘
```

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## 02. Cloud Platforms & Introduction to AI

🔗 **Full Lesson:** [02_Cloud_Platforms_and_Introduction_to_AI.md](./02_Cloud_Platforms_and_Introduction_to_AI.md)

* **What**: Imagine you need a powerful computer to run your website, but buying one is expensive, and you only need it for a few hours a day. **Cloud computing** lets you *rent* that computer (and much more) over the internet — you pay only for what you use, just like an electricity bill.
* **Why It Exists**: Solves deployment speed, consistency, and reliability challenges of Cloud Platforms & Introduction to AI in production.
* **Key Concepts**:
  * **Introduction to Cloud Platforms**
    * **💰 Save Money** — No need to buy expensive servers. Pay only for what you use.
    * **📈 Easy to Scale** — Need more power during a sale event? Add servers in minutes, remove them later.
    * **🌍 Global Reach** — Deploy your app in data centers across the world so users everywhere get fast access.
    * **🔒 Security** — Cloud providers invest billions in security — often more than any single company can afford.
  * **AWS (Amazon Web Services)**
    * **🏆 Market Leader** — Largest cloud provider with the most mature ecosystem.
    * **🌐 Global Infrastructure** — 30+ geographic regions, 100+ availability zones worldwide.
    * **🧩 Widest Service Selection** — 200+ fully featured services.
    * **📚 Huge Community** — Largest community of users, tutorials, certifications, and third-party tools.
  * **Microsoft Azure**
    * **🔗 Microsoft Integration** — Seamless integration with Windows, Office 365, Active Directory, Teams, SQL Server.
    * **🏢 Enterprise Focus** — Strong hybrid cloud capabilities (connect on-premises data centers to the cloud).
    * **🌍 Global Presence** — 60+ regions worldwide — more than any other cloud provider.
    * **🔐 Compliance** — Meets 90+ compliance certifications (important for healthcare, finance, government).
  * **Google Cloud Platform (GCP)**
    * **📊 Data & Analytics Leader** — BigQuery is one of the best tools for analyzing massive datasets.
    * **🤖 AI / ML Powerhouse** — TensorFlow, Vertex AI, and pre-trained models from Google's AI research.
    * **🌐 Google's Network** — One of the fastest and most reliable private networks on the planet.
    * **💲 Cost-Effective** — Sustained-use discounts automatically reduce costs for long-running VMs.
  * **Comparison  AWS vs Azure vs GCP**
    * **Services**: AWS EC2/S3/VPC maps to Azure VMs/Blob/VNet and GCP Compute Engine/Cloud Storage/VPC.
    * **Ecosystems**: AWS has the largest market share (~31%); Azure has enterprise-grade Microsoft integration; GCP leads in AI/ML (Vertex AI), containers (GKE), and big data analysis.
  * **Real-World Use Cases**
    * **EC2 instances** — Run thousands of servers to encode, process, and stream video content.
    * **S3** — Store petabytes of video files, images, and backups.
    * **CloudFront (CDN)** — Deliver content to 200+ million users worldwide with low latency.
    * **DynamoDB** — Store user preferences, viewing history, and recommendations.

### Key Commands / Code Example:

```
┌─────────────────────────────────────────────────────────────────┐
│                    CLOUD COMPUTING MARKET                       │
│                                                                 │
│   ┌───────────┐    ┌───────────┐    ┌───────────┐              │
│   │           │    │           │    │           │              │
│   │    AWS    │    │   Azure   │    │    GCP    │              │
│   │  Amazon   │    │ Microsoft │    │  Google   │              │
│   │  ~31 %    │    │  ~25 %    │    │  ~11 %    │              │
│   │           │    │           │    │           │              │
│   └───────────┘    └───────────┘    └───────────┘              │
│                                                                 │
│   Launched: 2006    Launched: 2010    Launched: 2008            │
└─────────────────────────────────────────────────────────────────┘
```

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## <a id="03-artificial-intelligence-a-beginners-guide"></a>03. Artificial Intelligence A Beginner's Guide 🤖

🔗 **Full Lesson:** [03_Artificial_Intelligence.md](./03_Artificial_Intelligence.md)

* **What**: At its simplest, **Artificial Intelligence (AI)** is the science of making machines "smart." Instead of a human telling a computer exactly what to do step-by-step (traditional programming), we teach the computer to learn and make decisions on its own.
* **Why It Exists**: AI exists because many real-world problems are too complex for traditional rule-based programming. You can't write "if-else" rules for recognizing faces, understanding languages, or predicting weather.
* **Key Concepts**:
  * **Foundation of AI: The Basics**
    * **Analogy:** Traditional programming is like following a **recipe** (Step 1: Do this, Step 2: Do that). AI is like teaching a **child** (Show them 100 pictures of a cat, and eventually, they recognize a cat on their own).
    * **Netflix/YouTube:** Recommending your next favorite show.
    * **FaceID:** Your phone recognizing your face to unlock.
    * **Google Maps:** Predicting traffic and finding the fastest route.
  * **Prompt Engineering: Talking to AI**
    * **With prompt engineering:** AI gives focused, relevant, actionable answers
    * **Without prompt engineering:** AI gives generic, rambling responses that waste your time
    * **Writing:** "Help me draft a professional email to my manager about a server outage."
    * **Debugging:** "Explain why this Python code is giving me an Index Error."
  * **AI Co-Programmer Setup: Your Coding Buddy**:
    * **Pair Programmers**: Virtual coding partners that write boilerplate, find bugs, and explain complex code.
    * **Tools**: ChatGPT (brainstorming), Claude (reasoning/debugging), GitHub Copilot (real-time autocomplete), and Cursor (AI editor).
    * **Workflow**: Define the idea → Prompt AI → Review code for security/correctness → Refine.
    * **Verification**: Never blindly trust AI code; always check for hallucinations and security risks.
  * **History of AI: How We Got Here**:
    * **Turing Test (1950s)**: Alan Turing establishes the foundational question, "Can machines think?"
    * **Milestones**: IBM's Deep Blue beats Kasparov (1997); Neural Networks breakthrough in image recognition (2012); ChatGPT released (2022).
    * **Growth Factors**: Enabled by the convergence of massive internet data, powerful GPU hardware, and Transformer architecture (2017).
  * **AI vs. ML vs. DL vs. Generative AI**:
    * **Hierarchy**: AI is the broad concept (machines acting smart) → ML is data pattern recognition (spam filters) → DL is brain-like neural networks (FaceID) → GenAI creates new content (ChatGPT).
    * **Analogy**: ML is like a student learning to recognize grades (classification), while GenAI is a student writing a whole new story (generation).
    * **DevOps Applicability**: GenAI is the most immediately useful tier for DevOps engineers (generating scripts, IAC config templates, and documentation).
  * **How AI Works: Under the Hood**:
    * **The Big Three**: Data (millions of examples) → Training (finding patterns) → Model (the resulting brain).
    * **Neural Networks**: Thousands of interconnected node switches (neurons) whose connection strengths adjust as the AI learns.
    * **Limitation**: AI is only as good as its training data; biased data creates biased AI.
  * **Generative AI vs. Agentic AI & AI Agents**:
    * **Generative AI (The Author)**: Reactive content creation (e.g. ChatGPT writing code or essays). It has transformed content creation, coding, and learning.
    * **Agentic AI (The Manager)**: Proactive, multi-step autonomous task execution using external tools (APIs, browsers) to achieve high-level goals.
    * **AI Agents in DevOps**: Autonomous workflows transforming systems administration:
      * **Log Analysis**: Monitors logs 24/7, investigates causes of "Database Errors", and suggests or applies fixes.
      * **Deployment Helper**: Deploys applications to cloud provider instances and monitors for failures.
      * **Cost Optimization**: Identifies idle servers and triggers automatic shutdown or resizing requests.
      * **Auto-Remediation**: Auto-healing infrastructure and auto-scaling pods.
  * **AI Setup for 10x Productivity**:
    * **Daily Workflow**: Prioritize tasks (ChatGPT) → Write code (Cursor/Copilot) → Debug errors (Claude) → Research concepts (Perplexity AI).
    * **Tool Stack**: Combine Cursor, Perplexity, Claude, and ChatGPT for max efficiency.

### Key Commands / Code Example:

```
┌──────────────────────────────────────────────────────────┐
│              THE THREE LEVELS OF AI                       │
│                                                          │
│   ┌──────────────────────────────────────────────────┐   │
│   │           SUPER AI (Theoretical)                 │   │
│   │   Surpasses all human intelligence               │   │
│   │   ┌──────────────────────────────────────────┐   │   │
│   │   │      GENERAL AI (Not yet achieved)       │   │   │
│   │   │   Human-like intelligence across tasks   │   │   │
│   │   │   ┌──────────────────────────────────┐   │   │   │
│   │   │   │     NARROW AI (Today's AI) ✅    │   │   │   │
│   │   │   │   Good at ONE specific task      │   │   │   │
│   │   │   │   Siri, GPT, Recommendations     │   │   │   │
│   │   │   └──────────────────────────────────┘   │   │   │
│   │   └──────────────────────────────────────────┘   │   │
│   └──────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────┘
```

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## <a id="04-cloud-computing-data-centers"></a>04. Cloud Computing & Data Centers ☁️

🔗 **Full Lesson:** [04_Cloud_Computing_and_Data_Centers.md](./04_Cloud_Computing_and_Data_Centers.md)

* **What**:
  ```text
                  On-Premise    IaaS      PaaS      SaaS
  Applications    [  YOU  ]   [ YOU ]   [ YOU ]   [CLOUD]
  Data            [  YOU  ]   [ YOU ]   [ YOU ]   [CLOUD]
  Runtime         [  YOU  ]   [ YOU ]   [CLOUD]   [CLOUD]
  Middleware      [  YOU  ]   [ YOU ]   [CLOUD]   [CLOUD]
  OS              [  YOU  ]   [ YOU ]   [CLOUD]   [CLOUD]
  Virtualization  [  YOU  ]   [CLOUD]   [CLOUD]   [CLOUD]
  Servers         [  YOU  ]   [CLOUD]   [CLOUD]   [CLOUD]
  Storage         [  YOU  ]   [CLOUD]   [CLOUD]   [CLOUD]
  Networking      [  YOU  ]   [CLOUD]   [CLOUD]   [CLOUD]
  ```
* **Why It Exists**: Solves deployment speed, consistency, and reliability challenges of ☁️ Cloud Computing & Data Centers in production.
* **Key Concepts**:
  * **📌 1. What is a Data Center?**: Physical facility with servers, storage, and networking equipment (the physical hardware layer).
  * **📌 2. Problems with Data Centers**: High upfront capital, slow server scaling, high maintenance overhead, downtime risks, and geographic latency limits.
  * **📌 3. Why Cloud is Less Expensive**: Pay-as-you-go rental utility model (pay only for what you consume like an electricity bill).
  * **📌 4. What is Cloud Computing?**: On-demand self-service resource delivery over the internet with pooling, broad access, rapid elasticity, and measured pricing.
  * **📌 5. Types of Cloud (Deployment Models)**: Public (shared), Private (dedicated for compliance/security), and Hybrid (connected combination).
  * **📌 6. Benefits of Cloud Computing**: Cost efficiency, scalability, reliability, speed, and global reach.
    * **Vertical (Scale Up)**: Make server more powerful (add RAM (Random Access Memory) / CPU (Central Processing Unit)).
    * **Horizontal (Scale Out)**: Add more servers to share the load.
  * **📌 7. Cloud Architecture**: Split between user-facing Frontend and backend compute (EC2 VMs), storage (S3 objects, EBS disks), and VPC networking.
  * **📌 8. Service Models (IaaS, PaaS, SaaS)**:
    * **IaaS (Infrastructure as a Service)**: Rent raw VM infrastructure; manage OS, runtime, and apps (AWS EC2).
    * **PaaS (Platform as a Service)**: Rent development platform; manage only application code (Heroku).
    * **SaaS (Software as a Service)**: Access fully managed, ready-to-use software (Gmail, Zoom, Netflix).
  * **📌 9. How Cloud Computing Works**: Enabled by Virtualization (Hypervisors creating VMs on a physical host), API request routing, and orchestration.
  * **📌 10. Cloud Services Overview**: Categorized into compute, storage, databases, networking, and identity security (IAM).
  * **📌 11. AWS vs Azure vs GCP**:
    * **AWS**: Market leader, largest service catalog, best for startups and general jobs.
    * **Azure**: Best hybrid cloud (Arc) capabilities and seamless Microsoft enterprise integration.
    * **GCP**: Leader in AI/ML, data analytics, and Kubernetes (invented K8s, best engine via GKE).

### Key Commands / Code Example:

```
👤 USER → Browser / App / CLI
    │
    │ Internet (HTTPS / API)
    ▼
┌─────────────────────────────┐
│          BACKEND            │
│  ┌───────────────────────┐  │
│  │  APPLICATION (code)   │  │
│  ├───────────────────────┤  │
│  │  MIDDLEWARE            │  │
│  │  (Load Balancer, API) │  │
│  ├───────────────────────┤  │
│  │  INFRASTRUCTURE        │  │
│  │  Servers · Storage ·  │  │
│  │  Networking · DBs     │  │
│  └───────────────────────┘  │
└─────────────────────────────┘
```

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## <a id="05-scripts-docker-vm-setup-practical-reference"></a>05. Scripts, Docker & VM Setup Practical Reference 🛠️

🔗 **Full Lesson:** [05_Scripts_Docker_VM_Setup.md](./05_Scripts_Docker_VM_Setup.md)

* **What**: A shell script that automatically installs Docker Engine on a Linux machine using Docker's official installation script.
* **Why It Exists**: Docker is the foundation of modern containerized deployments. Instead of manually running multiple commands to install it, this script automates the entire process in two lines.
* **Key Concepts**:
  * **Docker Installation Script**
    * **With script:** Docker installed in ~2 minutes with zero manual steps
    * **Without script:** You'd need to manually add repositories, GPG keys, update package lists, and install — 10+ commands and easy to make mistakes
  * **GPG Keys & Security**: Asymmetric key pairs verifying package authenticity and integrity to prevent MITM attacks during installation.
  * **GNU Project ("GNU's Not Unix")**: Created the shell commands, compiler tools, and copyleft licensing (GPL) forming the software body of the GNU/Linux OS.
  * **Bourne Shell (sh)**: The original Unix command-line interpreter (1977); used in installer scripts for absolute portability across all Unix/Linux distros compared to `bash`.
  * **Running a Docker Container**
    * **With Docker:** One command to run a full Windows 11 React app — no Node.js installation, no npm setup, no build process
    * **Without Docker:** You'd need to clone the repo, install Node.js, install dependencies, configure the build, and start the server — 15+ minutes of setup
  * **GCP VM Creation Command**
    * **With CLI:** Create identical VMs in seconds, scriptable, repeatable, version-controllable
    * **With GUI:** Click through 8+ screens, manual, error-prone, can't be saved as code

### Key Commands / Code Example:

```bash
# Step 1: Download the official Docker installation script
curl -fsSL https://get.docker.com -o install-docker.sh

# Step 2: Run the installation script with sudo privileges
sudo sh install-docker.sh
```

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## 06. DevOps Basics: Tools, Phases, and Roles

🔗 **Full Lesson:** [06_DevOps_Basics_Tools_and_Roles.md](./06_DevOps_Basics_Tools_and_Roles.md)

* **What**: DevOps is like a bridge that connects two groups of people: the ones who build software (**Developers**) and the ones who make sure it runs smoothly for everyone (**Operations**).
* **Why It Exists**: Modern software development demands speed and reliability. Companies like Netflix deploy thousands of times per day, while traditional companies may deploy monthly.
* **Key Concepts**:
  * **Introduction**: Integrates Development and Operations to release updates faster, detect bugs earlier, and maintain 24/7 uptime.
  * **The Wall of Confusion Problem**: The traditional communication gap where developers focus on velocity ("It works on my machine!") while operations focuses on system stability, leading to finger-pointing.
  * **DevOps Phases (The Lifecycle)**
    * **With the lifecycle:** Issues are caught at every stage, each phase has automated quality gates
    * **Without the lifecycle:** Problems pile up and explode in production, leading to fire-fighting culture
  * **DevOps Tools**: Automated helper tools: Version Control (Git), CI/CD (Jenkins/GitHub Actions), Containerization (Docker), Orchestration (Kubernetes), and Monitoring (Prometheus/Grafana).
  * **Technologies Used in DevOps**: Consistent environments (Containers), automated deployment conveyor belts (Pipelines), on-demand compute/storage (Cloud), and automated tasks (Scripting).
  * **Roles and Responsibilities**: DevOps Engineers (build pipelines), Developers (build product code), QA Engineers (inspect bugs), and Operations (manage scale/uptime).
  * **Real-World Example: The DevOps Flow**: Developer commits code → GitHub triggers auto-test → Docker builds artifact → Pipeline pushes to AWS cloud → Feature goes live instantly.
  * **DevOps Best Practices**
    * **46x** more frequent deployments
    * **440x** faster lead time from commit to deploy
    * **170x** faster mean time to recovery from downtime
    * **5x** lower change failure rate

### Key Commands / Code Example:

```
┌──────────────────────────────────────────────────────────────────┐
│                    THE WALL OF CONFUSION                          │
│                                                                  │
│   DEVELOPERS                    OPERATIONS                       │
│   ┌──────────────┐    🧱🧱🧱    ┌──────────────┐                │
│   │ "It works on │    🧱🧱🧱    │ "The code is │                │
│   │  my machine!"│    🧱🧱🧱    │  broken!"    │                │
│   │              │    🧱🧱🧱    │              │                │
│   │ Goal: Ship   │    🧱🧱🧱    │ Goal: Keep   │                │
│   │ features fast│    🧱🧱🧱    │ things stable│                │
│   └──────────────┘    🧱🧱🧱    └──────────────┘                │
│                                                                  │
│   Result: Blame game, slow releases, unhappy customers          │
└──────────────────────────────────────────────────────────────────┘
```

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## <a id="07-linux-os-github-basics"></a>07. Linux, OS and GitHub Basics 🖥️

🔗 **Full Lesson:** [07_Linux_OS_and_GitHub_Basics.md](./07_Linux_OS_and_GitHub_Basics.md)

* **What**: Introduction and foundational concepts of 🖥️ Linux, OS and GitHub Basics.
* **Why It Exists**: Solves deployment speed, consistency, and reliability challenges of 🖥️ Linux, OS and GitHub Basics in production.
* **Key Concepts**:
  * **📌 1. What is an Operating System (OS)?**
    * **Definition**: Software that manages hardware resources and provides interfaces (GUI/CLI) for users and applications.
    * **Core Functions**: Resource management (CPU/RAM allocation), file management, process management (multitasking), and user security.
    * **Windows/Mac** → Writing code, meetings, local development
    * **Linux** → Running servers, databases, deployment pipelines, containers
  * **📌 2. What is Linux?**
    * **Definition**: A free, open-source operating system kernel created by Linus Torvalds in 1991 as an alternative to UNIX.
    * **Kernel** = The core "brain" — manages hardware (CPU, memory, devices)
    * **Distribution (Distro)** = Kernel + tools + package manager + desktop (optional) (e.g. Ubuntu, CentOS, Rocky Linux, Debian, Alpine)
    * **90% of the world's servers** run Linux (including AWS, Google, Facebook)
    * **Docker, Kubernetes, Jenkins, Terraform** — all built for Linux
  * **📌 3. Open Source & Why Linux Dominates**
    * **Open Source**: Publicly available source code allowing collaborative improvements, transparency, and no vendor lock-in.
    * **OS:** Linux (Ubuntu, Debian, CentOS)
    * **Web Servers:** Apache, Nginx (powers 70% of internet)
    * **Databases:** MySQL, PostgreSQL, MongoDB
    * **DevOps:** Docker, Kubernetes, Jenkins, Terraform, Ansible
    * **Server Domination**: Highly secure permissions, headless execution (runs on <512MB RAM), runs for years without rebooting, and is scriptable.
  * **📌 4. Linux vs Windows**
    * **Features**: Windows is GUI-first, case-insensitive, backslash-separated (`\`), and resource-heavy. Linux is CLI-first, case-sensitive (`file.txt` != `File.txt`), forward-slash-separated (`/`), and lightweight.
    * **Updates**: Windows requires forced reboots for updates, while Linux supports live patching without rebooting.
  * **📌 5. Linux File System**
    * **Root (`/`)**: Starts from a single root directory; no separate C: or D: drives.
    * **Structure**: `/bin` (essential user commands), `/etc` (configuration settings), `/var/log` (logs), and `/home` (user home directories).
    * **Paradigm**: "Everything is a file" (e.g. `/dev/sda` represents a hard drive, `/proc/cpuinfo` represents CPU details).
  * **📌 6. Users, Permissions & Shell Basics (NEW)**
    * **Users**: `root` (admin with absolute power), regular users, and service users (running background apps like Nginx).
    * **Permissions**: Configured via `chmod` and `chown` for Read (4 / `r`), Write (2 / `w`), and Execute (1 / `x`) split across Owner, Group, and Others.
    * **Shells**: Command interpreters: default standard `bash`, portable shell `sh`, and macOS-default `zsh`.
  * **📌 7. Linux Commands Overview**
    * **Common Commands**: Navigation (`pwd`, `ls`, `cd`), file management (`mkdir`, `touch`, `cp`, `mv`, `rm -rf`), and file reading (`cat`, `head`, `tail`, `grep`).
    * **Shortcuts**: `TAB` (autocomplete), `Ctrl+C` (terminate running process), `Ctrl+L` (clear screen), and `Ctrl+R` (reverse history search).
  * **📌 8. Ways to Run Linux**
    * **Methods**: WSL (very low resources on Windows), Docker (instant containers), VirtualBox (local VM environment), and Cloud VMs (GCP/AWS for 24/7 uptime).
    * **GCP Instance Config**: Machine Type: **`e2-micro`** (free tier!), Boot Disk: **Ubuntu 22.04 LTS**.
  * **📌 9. Package Managers (NEW)**
    * **Apt (Ubuntu/Debian)**: Installs `.deb` packages via `/etc/apt/sources.list`. Commands: `apt update`, `apt install`, `apt remove`.
    * **Yum/Dnf (CentOS/RHEL)**: Installs `.rpm` packages via `/etc/yum.repos.d/`. Commands: `yum update`, `yum install`.
  * **📌 10. Git & GitHub Basics**
    * **Git**: Local version control tracker (`git init`, `add`, `commit`, `branch`).
    * **GitHub**: Cloud hosting platform for collaboration and remote repository backup (`git push`, `pull`, `clone`).

### Key Commands / Code Example:

```
-rwxr-xr--  1  nishant  devops  4096  Jan 10 10:00  script.sh
 │││ │││ │││
 │││ │││ └── Others: r-- (read only)
 │││ └───── Group:  r-x (read + execute)
 └──────── Owner:  rwx (read + write + execute)
```

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## <a id="08-linux-commands-concepts"></a>08. Linux, SSH and Basic Commands 🐧

🔗 **Full Lesson:** [08_Linux_SSH_and_Basic_Commands.md](./08_Linux_SSH_and_Basic_Commands.md)

* **What**: Introduction and foundational concepts of 🐧 Linux, SSH and Basic Commands.
* **Why It Exists**: Many commands output sizes in **bytes** by default, which is hard to read. Adding `-h` flag converts them to **KB, MB, GB** — much easier to understand!
* **Key Concepts**:
  * **📌 Introduction**: Provides a starting point for the command-line interface ("cockpit of the airplane") for system navigation, file manipulation, and process control.
  * **🔐 SSH Key Generation and Authentication**
    * The **public key** is like a **lock** — you can give it to anyone (the server).
    * The **private key** is like the **key to that lock** — only you should have it.
    * 🚀 **Fast** — quick to generate and verify
    * 🔐 **Very secure** — practically unbreakable with today's computers
    * **Key Setup**: Keys are generated using `ssh-keygen -t ed25519` on the local machine and the public key is placed inside `/home/username/.ssh/authorized_keys` on the cloud host/server VM.
  * **📁 Basic Linux Commands**: Core tools for navigation (`pwd`, `cd`), directories/files (`mkdir -p`, `touch`), manipulation (`cp`, `mv`, `rm -rf`), listing (`ls -lah`), viewing (`cat`), and text editing (`vi`).
  * **💻 System Information Commands**: System resource inspect commands: memory status (`free -h`), disk usage (`df -h`), server uptime (`uptime`), process tree (`top`), and command logs (`history`).
  * **💡 Important Concepts**
    * **Zombie Processes**: Process that has finished execution but remains in the process table waiting for parental acknowledgement; cannot be killed with `kill -9`.
    * **vi Editor modes**: Dual modes: Command Mode (for navigating, saving `:w`, quitting `:q`) and Insert Mode (for typing/editing text via `i`).

### Key Commands / Code Example:

```bash
# View your keys folder
ls ~/.ssh/

# View your public key (to copy to a server)
cat ~/.ssh/id_ed25519.pub
```

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## <a id="09-linux-commands-concepts-intermediate-part-2"></a>09. Linux Monitoring, Scripting and Permissions 🐧

🔗 **Full Lesson:** [09_Linux_Monitoring_Scripting_and_Permissions.md](./09_Linux_Monitoring_Scripting_and_Permissions.md)

* **What**: Originally used to back up data to magnetic tapes. Today, we use it to:
- Bundle multiple files into one
- Compress log files to save disk space
- Package application files for deployment
- Create backups
* **Why It Exists**: Real-time server visibility, automation, and security permissions are the absolute backbone of system administration. DevOps engineers must know how to diagnose server performance bottlenecks, automate recurring tasks via shell scripts, package logs using archive tools, and enforce strict, secure file access bounds (preventing security holes like raw 777 permissions).
* **Key Concepts**:
  * **📌 Introduction**: Covers intermediate Linux tasks essential for DevOps engineers on live production environments: watching server state, process manipulation, shell scripting, and security permissions.
  * **💻 System Monitoring Commands**
    * **Load average** — a server with 1 CPU should have load < 1.0 (ideally)
    * **Tools**: Use `top` or `htop` for live metrics, `free -h` for memory, `df -h` for disk space, and `du -sh` for folder sizes.
  * **⚙️ Process Management**: Snapshot processes with `ps aux` or `ps -aef`. Terminate frozen/stuck processes using `kill <PID>` (SIGTERM 15) or `kill -9 <PID>` (SIGKILL 9). If the OS runs out of RAM, the **OOM Killer** dynamically force-stops memory-heavy applications.
  * **📦 File Compression (TAR)**
    * Adding `z` = compress with **gzip** (makes the file much smaller)
    * **Commands**: Bundle files using `tar cvf` and extract them with `tar xvf` (or `tar cvzf`/`tar xvzf` for compressed `.tar.gz` files).
  * **🧾 Shell Scripting**
    * 🔁 **Automation** — Run repetitive tasks without manual effort
    * ⏰ **Scheduling** — Run with cron jobs at specific times
    * 🚨 **Monitoring** — Check server health and send alerts
    * 🚀 **Deployment** — Deploy applications automatically
    * **Shebang**: Starts with `#!/bin/bash` to specify the Bash command interpreter. Make executable using `chmod +x script.sh`.
  * **🔐 File Permissions**
    * **Everyone** on the system can read, write, AND execute it
    * **Enforcement**: Set numerical permissions (Read=4, Write=2, Execute=1) like `600` for private SSH keys or `644` for configs. Modify with `chmod` and change owners with `chown`.
  * **👤 User Management**: Admin creation of human accounts with `adduser` / `useradd`, password management via `passwd`, account removal with `deluser --remove-home`, and switching user environments with `su - username`.
  * **👥 Group Management**
    * `-a` = **Append** (add without removing existing groups) ← VERY IMPORTANT!
    * `-G` = specify the **Group** to add
    * **Application**: Group access cards represent group identities. Create with `addgroup` and add users with `usermod -aG groupname username` to manage shared directory ownership.
  * **🔒 Advanced User Management**: Set account/password aging and expiry parameters using `chage` (e.g. `chage -M 90` for password rotation). Inspect user system mappings in `/etc/passwd`.

### Key Commands / Code Example:

```
top - 10:30:01 up 3 days,  2:15,  2 users,  load average: 0.25, 0.40, 0.38
Tasks: 198 total,   1 running, 197 sleeping,   0 stopped,   0 zombie
%Cpu(s):  5.5 us,  2.1 sy,  0.0 ni, 91.8 id,  0.4 wa
MiB Mem :   7951.2 total,   1234.5 free,   4200.1 used,   2516.6 buff/cache
```

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## <a id="10-linux-commands-concepts-intermediate-part-3"></a>10. Linux, VI Editor and Package Management 🐧

🔗 **Full Lesson:** [10_Linux_VI_Editor_and_Package_Management.md](./10_Linux_VI_Editor_and_Package_Management.md)

* **What**: Linux is an **Open Source** operating system kernel. Unlike Windows, anyone can see the code, modify it, and share it.
* **Why It Exists**: In modern production environments, server access is headless (no graphic desktop or mouse interface). DevOps engineers need to log in remotely and securely using SSH, edit server configuration files in place using terminal editors like VI/Vim, read files without causing system memory exhaustion, and use native package managers (apt, yum) to handle dependencies during software installations.
* **Key Concepts**:
  * **📌 Introduction**: Focuses on bridging the gap from simple local user usage to professional DevOps engineering tasks: connecting between servers, editing config files on headless systems, and installing software packages.
  * **🔁 Linux Fundamentals Quick Revision**: Quick summary of Linux open source kernel philosophy, its core architecture layers (Kernel, Shell, User Space), root/system configurations file hierarchies (`/etc`, `/var/log`), and basic navigations.
  * **🎮 Bandit Game (Hands-on Practice)**
    * **Username:** `bandit0`
    * **Password:** `bandit0`
    * **Port:** `2220` (Standard SSH is 22, but Bandit uses 2220).
    * **Purpose**: Gamified Capture-The-Flag platform to build muscle memory for finding weird files and reading hidden data in the command terminal.
  * **🔐 Server-to-Server Connectivity (SSH)**: The standard connection command `ssh username@server-ip`. Outlines secure jump paths from personal laptops through a public **Bastion Host** (Jump Box) into protected private application servers, and managing traffic via **Proxy Servers**.
  * **✏️ VI Editor Deep Dive**: Editing text files in headless terminals using two modes: Command Mode (for moving around, saving `:wq`, and deleting lines `dd`) and Insert Mode (press `i` to type).
  * **📖 File Viewing Commands**
    * `head -n 10 file.txt`: Show the **first** 10 lines.
    * `tail -n 10 file.txt`: Show the **last** 10 lines.
    * `tail -f /var/log/syslog`: **Crucial DevOps tool** to dynamically follow logs in real-time as events occur.
  * **📦 Package Management**: Utilizing automated managers like `apt` (Ubuntu/Debian) or `yum`/`dnf` (RedHat/CentOS) to install, update, and remove software while automatically resolving dependency trees.

### Key Commands / Code Example:

```bash
# Update local package index
sudo apt update

# Upgrade all installed software
sudo apt upgrade -y

# Install a package (e.g., git)
sudo apt install git -y

# Remove a package
sudo apt remove git -y

# RHEL/CentOS/Amazon Linux equivalent for installing httpd
sudo yum install httpd -y
```

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## <a id="11-linux-commands-concepts-intermediate-part-4"></a>11. Linux Troubleshooting, Logs and Services 🐧

🔗 **Full Lesson:** [11_Linux_Troubleshooting_Logs_and_Services.md](./11_Linux_Troubleshooting_Logs_and_Services.md)

* **What**: Introduction and foundational concepts of 🐧 Linux Troubleshooting, Logs and Services.
* **Why It Exists**: Production servers inevitably experience issues—whether due to disk space saturation, memory resource exhaustion, application daemon crashes, or network blocks. Understanding the core OS boot sequence (BIOS to systemd targets) and using diagnostic commands allows engineers to quickly trace the root cause of an outage, read system logs safely, and control background services.
* **Key Concepts**:
  * **📌 Introduction**: Outlines the importance of troubleshooting as a DevOps engineer's superpower, focusing on tracking down resource exhaustion, service failures, and debugging live site outages.
  * **🌐 Website Troubleshooting Basics**
    * **Red Rows:** Indicate failed requests.
    * **Time Column:** Shows if a backend API is taking too long to respond.
    * **1xx (Informational):** Request received, continuing process.
    * **2xx (Success):** Everything is fine (e.g., `200 OK`).
    * **Status Codes**: 4xx Client Errors (e.g. `403 Forbidden`, `404 Not Found`) and 5xx Server Errors (e.g. `500 Internal Error`, `502 Bad Gateway`, `503 Unavailable`).
  * **🖥️ Linux Boot Process Deep Dive**: The 6 key steps of OS boot: BIOS/UEFI (hardware POST check) → MBR/GPT partition sector → GRUB Bootloader → Kernel Initialization → Init Process (`systemd` with PID 1 starting background services) → Runlevel Target state. Features comparison to Windows boot stages (`Bootmgr`, `winload.exe`, `ntoskrnl.exe`, `smss.exe`).
  * **📊 System Troubleshooting Commands**
    * `df -h`: Check Disk Space. If `/` is **100% full**, the system will crash!
    * **High CPU?** Check `top`. Find the process ID (PID) using the most %CPU.
    * **Everything is slow?** Check `free -h`. If `available` is near 0, the system is swapping, which is very slow.
  * **📁 Log Management & Debugging**
    * `tail -f /var/log/syslog`: **Crucial!** It follows the log in real-time as new lines are added.
  * **⚙️ Service & Process Management**
    * `kill -15 <PID>`: **Graceful Kill**. Asks the app to "Please save your work and close."
    * `kill -9 <PID>`: **Force Kill**. Literally kills the process instantly. Use only as a last resort!
  * **💽 Disk & Storage Troubleshooting**
    * **Automation:** Use `logrotate` to automatically compress and delete old logs.
  * **🔐 File Permissions (Troubleshooting Perspective)**
    * **R** (Read), **W** (Write), **X** (Execute).
    * **Owner** (first 3), **Group** (next 3), **Others** (last 3).

### Key Commands / Code Example:

```bash
dmesg | less
# Search for errors during boot
dmesg | grep -i error
```

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## <a id="12-aws-fundamentals-part-1"></a>12. AWS (Amazon Web Services) Basics and Cloud Introduction ☁️

🔗 **Full Lesson:** [12_AWS_Basics_and_Cloud_Introduction.md](./12_AWS_Basics_and_Cloud_Introduction.md)

* **What**: Introduction and foundational concepts of ☁️ AWS Basics and Cloud Introduction.
* **Why It Exists**: Traditional physical server deployments required weeks of hardware shipping, heavy capital expense, manual cabling, and round-the-clock environmental maintenance. Cloud platforms like AWS remove this overhead, providing on-demand utility-style compute and storage resources globally with horizontal auto-scaling capabilities.
* **Key Concepts**:
  * **📌 Introduction**: Introducing AWS cloud capabilities. AWS acts as the playground of modern software deployment, replacing physical datacenters with virtual resource renting over the internet.
  * **️ What is AWS?**
    * **Traditional Way:** You buy an oven, rent a building, buy the furniture, and hire staff. If the shop fails, you are stuck with the expensive oven and a long lease.
    * **Cloud (AWS) Way:** You rent a fully equipped kitchen for $10 an hour. If you have many orders, you rent a second kitchen instantly. If no one buys pizza, you stop the rental and pay nothing.
    * **No upfront costs. No hidden fees. No commitments.**
  * **🏗️ Evolution of AWS**: Traces milestones from 2002 inception to the launch of SQS (Simple Queue Service - 2004), EC2 (Elastic Compute Cloud) / S3 (Simple Storage Service - 2006), VPC (Virtual Private Cloud - 2009), to today's catalog of 200+ managed services.
  * **🌍 Key Features of AWS**
    * **Region:** A physical location in the world (e.g., US-East-1 in Virginia).
    * **Availability Zone (AZ):** One or more data centers within a Region.
    * **Vertical Scaling:** Making your server "bigger" (more RAM/CPU).
    * **Horizontal Scaling:** Adding "more" servers (1 server becomes 10 during a sale).
  * **🏢 Traditional vs Cloud Infrastructure**
    * **Physical Storage** (Hard drives) → **S3** or **EBS (Elastic Block Store)**
    * **Physical Servers** (CPU/RAM) → **EC2**
    * **Networking** (Cables/Routers) → **VPC**
    * **Database Admin** → **RDS (Relational Database Service)**
  * **🧰 Core AWS Services Overview**: Overview of compute (EC2), storage (S3), network (VPC), identity database (IAM - Identity and Access Management), managed database (RDS), and logging dashboards (CloudWatch).
  * **🎯 Why Companies Use AWS (Real Industry Use Cases)**: Outlines cloud adoption motivations: Startup agility (Free Tier), Enterprise security rules (PCI-DSS - Payment Card Industry Data Security Standard compliance), E-Commerce spikes management (Prime Day auto-scaling), and Media latency optimizations (Netflix).

### Key Commands / Code Example:

```bash
# Review lesson files for specific commands and configurations of ️ AWS Fundamentals (Part 1)
```

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## <a id="13-aws-iam-ec2-hands-on-guide"></a>13. AWS IAM & EC2 Hands-on Guide ☁️

🔗 **Full Lesson:** [13_AWS_IAM_and_EC2_Basics.md](./13_AWS_IAM_and_EC2_Basics.md)

* **What**: IAM stands for **Identity and Access Management**. It is a free AWS service that helps you control who can access your AWS resources (like databases, servers, or files).
* **Why It Exists**: Restricting master root account access is a critical security rule. IAM provides identity protection using fine-grained permissions, roles, and programmatic access keys for automation bots. Simultaneously, EC2 allows developers to provision virtual compute nodes globally on-demand utilizing public/private keypairs instead of static insecure passwords.
* **Key Concepts**:
  * **📌 Introduction**
    * **IAM (Identity and Access Management):** The "Security Guard" of your AWS account. It decides *who* can enter and *what* they can do.
    * **EC2 (Elastic Compute Cloud):** A fancy name for "Virtual Computers in the Cloud". We will rent a computer from Amazon and run Windows on it!
  * **🔐 IAM Basics**
    * **Root User:** The building owner with the master key to every room.
    * **IAM:** The security desk at the front door. They issue ID badges (Users) and decide who can enter the server room, who can only enter the cafeteria, and who isn't strictly allowed anywhere.
  * **👤 IAM Users, Groups & Best Practices**
    * **Console Access:** This means the user can log into the AWS Website (Management Console) using a username and password.
    * **Account Alias:** AWS login URLs are usually long and ugly (e.g., `https://123456789012.signin.aws.amazon.com/console`). An Account Alias lets you create a friendly URL your team will actually remember! (e.g., `https://my-awesome-company.signin.aws.amazon.com/console`).
  * **🤖 Service Accounts (Bot Users)**
    * **Access Key ID:** Think of this as the "bot username".
    * **Secret Access Key:** Think of this as the "bot password".
    * **Terraform / Ansible:** Tools that automate building servers.
    * **Jenkins / GitHub Actions:** Tools that automatically deploy your code.
  * **📜 IAM Policies & Roles**
    * **Policy:** The piece of paper (rulebook) that clearly states: "Can read files, cannot delete files."
    * **Role:** A construction worker's "Hard Hat".
  * **🔑 Authentication vs Authorization**
    * **Authentication (AuthN):** *Who are you?*
    * **Authorization (AuthZ):** *What are you allowed to do?*
  * **🧾 Credential Reports & Security Best Practices**: Downloadable CSV audits tracking password/key ages across all users. Emphasizes security best practices: MFA (Multi-Factor Authentication) on all accounts, deleting stale user accounts, and rotating programmatic keys every 90 days.
  * **💻 EC2 Introduction**: Scalable virtual computing resources in the cloud that allow you to spin up and terminate virtual servers on demand with zero physical hardware management.
  * **🪟 Launching Windows Server on EC2**: Detailed hands-on walkthrough choosing an AMI (Amazon Machine Image - Windows Server Datacenter), choosing micro hardware (`t2.micro` / `t3.micro` free-tier eligible), and defining Security Groups (allowing RDP (Remote Desktop Protocol - tool used to see the screen and control a Windows EC2 server) port 3389).
  * **🔐 Key Pairs & Secure Access**
    * **Public Key:** AWS puts this lock on your server.
    * **Private Key (`.pem` file):** You download this to your personal laptop. It's the only key that can open the lock!
  * **🖥️ Connecting to EC2 via RDP**: Decrypting the Administrator password using the private `.pem` key, opening Windows Remote Desktop Connection client (RDP), and inputting credentials to access the remote Windows OS GUI.
  * **🌍 Region Concept (Important)**
    * **IAM is GLOBAL.** When you create a user, they exist across the entire world simultaneously. You don't pick a region for IAM.
    * **EC2 is REGIONAL.** If you launch a server in Mumbai, and then you change your AWS console view to London, your server disappears! (Don't panic, it's still in Mumbai, you just need to switch back).

### Key Commands / Code Example:

```bash
# Review lesson files for specific commands and configurations of ️ AWS IAM & EC2 Hands-on Guide
```

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## <a id="14-scaling-ec2-ami-load-balancers-essentials"></a>14. Scaling, EC2, AMI & Load Balancers Essentials ⚖️

🔗 **Full Lesson:** [14_ELB_and_EC2.md](./14_ELB_and_EC2.md)

* **What**: Introduction and foundational concepts of ⚖️ Scaling, EC2, AMI & Load Balancers Essentials.
* **Why It Exists**: Running a production application on a single server creates a single point of failure (SPOF - Single Point of Failure) and cannot scale dynamically. Load Balancers distribute traffic across multiple target nodes, while AMIs allow instant copying of server images, laying the foundation for high-availability architectures and horizontal auto-scaling.
* **Key Concepts**:
  * **Scaling & Elasticity**
    * **Horizontal Scaling (Scale Out / In):** Adding more machines (servers) to share the load.
    * **Vertical Scaling (Scale Up / Down):** Increasing the power (CPU, RAM) of an existing machine.
    * **Cost Efficiency:** Pay only for what you use.
    * **Reliability:** Prevents downtime during high traffic.
  * **EC2 (Elastic Compute Cloud)**: Rented virtual machines with customizable hardware sizing (instance types) and security parameters (Security Groups and key pairs).
  * **AMI (Amazon Machine Image)**: Blueprint templates containing pre-packaged OS configurations and dependencies to launch identical cloned servers rapidly.
  * **Load Balancer (ELB - Elastic Load Balancing)**
    * **High Availability:** If a server crashes, the ELB routes around it without the user noticing.
    * **Fault Tolerance & Seamless Scaling.**
  * **Practical Implementation Outline**: Step-by-step setup establishing target Linux EC2 nodes, installing web services (`nginx`), configuring custom default home pages, and opening Port 80.

### Key Commands / Code Example:

```text
Vertical Scaling              Horizontal Scaling
   [ Server ]                     [ Server ]
       |                         /    |    \
 [ BIG SERVER ]        [Server] [Server] [Server]
```

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## <a id="15-aws-ec2-ami-ebs-load-balancers-deep-dive"></a>15. AWS EC2, AMI, EBS & Load Balancers Deep Dive ☁️

🔗 **Full Lesson:** [15_AWS_EC2_AMI_EBS_LoadBalancer.md](./15_AWS_EC2_AMI_EBS_LoadBalancer.md)

* **What**: EC2 = **Elastic Compute Cloud**. It is a service that lets you rent virtual servers (called **instances**) on Amazon's hardware.
* **Why It Exists**: Going beyond basic virtual compute requires robust data persistence, network isolation, and strict cost controls. Deep knowledge of persistent EBS volumes, AMI backups, Layer-7 load routing (ALB - Application Load Balancer), and Auto Scaling groups enables engineers to prevent database dataloss, survive hardware failures, and avoid expensive cloud billing mistakes.
* **Key Concepts**:
  * **📌 Introduction**
    * **EC2** — Your virtual servers in the cloud (this time we look at instance options, recovery, and protection).
    * **AMI** — Pre-baked server templates that save you hours of setup.
    * **EBS** — The hard drives attached to your cloud servers.
    * **Load Balancers (ELB)** — The traffic cops that distribute user requests across multiple servers.
  * **💻 EC2 Deep Dive**
    * **What:** If the underlying physical hardware fails, AWS automatically migrates your instance to healthy hardware.
    * **Why:** Keeps your application running without manual intervention.
    * **How:** Enable it via the EC2 console → Instance Settings → Auto-Recovery. AWS uses health checks to detect hardware issues.
    * **Impact:** Zero-downtime recovery from hardware failures. Your IP address and data stay the same.
  * **🖼️ AMI**
    * The **Operating System** (Ubuntu, Amazon Linux, Windows, etc.)
    * **Pre-installed software** (NGINX, Docker, Node.js, etc.)
    * **Application configurations** (config files, environment variables)
    * **Data** on attached storage volumes
  * **💾 EBS (Elastic Block Store)**
    * **Persistence:** Unlike instance storage (which is lost when you stop/terminate), EBS data **survives** even when you stop an instance.
    * **Backups:** You can take **snapshots** (point-in-time backups) of your entire volume.
    * **Flexibility:** You can increase the size, change the type (SSD → HDD), and even detach a volume from one instance and attach it to another.
    * **SSD** = Sports car. Fast, responsive, premium.
  * **⚙️ Load Balancers (ELB)**
    * Works at **Layer 7** (HTTP/HTTPS level — understands URLs, headers, cookies).
    * Can route traffic based on **URL path**:
    * Supports **WebSockets** and **HTTP/2**.
    * **Best for:** Most web applications. This is probably what you'll use 80% of the time.
  * **📈 Auto Scaling  Quick Introduction**
    * **Over-provision:** Run 20 servers 24/7 "just in case" → waste money. 💸
    * **Under-provision:** Run 2 servers and pray traffic doesn't spike → risk downtime. 😰
  * **🛠️ Practical Tips & Tools**: Always verify the console region is set correctly (e.g. Mumbai). Clean up unused resources (EBS volumes, Elastic IPs, AMI snapshots) immediately to avoid background costs. Recommended client software tools include MobaXterm (for SSH/SFTP [Secure File Transfer Protocol]), FileZilla, and AWS CLI.
  * **🚫 Common Mistakes Beginners Make**:
    * **Security Mistakes**: Leaving all ports open (`0.0.0.0/0`), setting shutdown behavior to "Terminate" on production, or baking sensitive passwords and API keys into public AMIs.
    * **EBS Mistakes**: Not configuring regular snapshots or utilizing slow HDD volumes for highly active databases.
    * **Load Balancer Mistakes**: Blocked communications due to mismatched Security Groups, and forgetting to enable Health Checks.
    * **Billing Mistakes**: Forgetting to release unattached Elastic IPs, and not monitoring active resources against the AWS Free Tier.
  * **DevOps Best Practices**
    * 🟢 **Use Infrastructure as Code (IaC - Infrastructure as Code):** Manage all your EC2 instances, EBS volumes, and Load Balancers via Terraform or AWS CloudFormation — not by clicking around the console.
    * 🟢 **Tag everything:** Add tags like `Environment: Production`, `Team: Backend`, `Owner: krishna@company.com` to every resource. This makes billing, auditing, and cleanup easy.
    * 🟢 **Use Launch Templates over Launch Configurations:** Launch Templates support versioning, are more flexible, and are the recommended approach for Auto Scaling Groups.
    * 🟢 **Enable Termination Protection** on all production EC2 instances.

### Key Commands / Code Example:

```
┌──────────────────────────────────────────────────────────┐
│                    EC2 INSTANCE LIFECYCLE                 │
│                                                          │
│   [ Launch ]                                             │
│       │                                                  │
│       ▼                                                  │
│   [ Running ] ◄────────────────────────┐                 │
│       │           │           │        │                 │
│       ▼           ▼           ▼        │                 │
│   [ Stop ]   [ Hibernate ] [ Reboot ]  │                 │
│       │           │                    │                 │
│       ▼           ▼                    │                 │
│   [ Stopped ] [ Stopped ]             │                 │
│       │           │                    │                 │
│       ▼           ▼                    │                 │
│   [ Start ] ──────┘────────────────────┘                 │
│                                                          │
│   [ Terminate ] ──► 💀 GONE FOREVER                      │
│   (Unless Termination Protection is ON)                  │
└──────────────────────────────────────────────────────────┘
```

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## <a id="16-linux-practical-session-hands-on-devops-basics"></a>16. Linux Practical Session (Hands-on DevOps Basics) 🐧

🔗 **Full Lesson:** [16_Linux_Practical_Session.md](./16_Linux_Practical_Session.md)

* **What**: Introduction and foundational concepts of 🐧 Linux Practical Session (Hands-on DevOps Basics).
* **Why It Exists**: Hands-on scripting, terminal multiplexing (tmux), and background processing (nohup) prevent connection interruptions from aborting critical tasks. It is essential to master live resource check commands, permissions adjustments, secure file copies, and automatic log rotations to prevent servers from crashing due to disk exhaustion.
* **Key Concepts**:
  * **📌 Introduction**: Provides a hands-on, practical deep-dive into the essential Linux commands and concepts every DevOps engineer needs to know to keep servers healthy, troubleshoot deployment failures, and monitor resources.
  * **Detailed Sections**
    * **What:** Virtual Memory Statistics. A command-line tool that reports information about processes, memory, paging, block IO, traps, and CPU activity.
    * **Why:** Used to get a quick overview of why a system might be slow—is it a memory bottleneck or CPU?
    * **How:** Run `vmstat 1` to get updates every 1 second.
    * **Impact:** Helps quickly identify resource exhaustion in production.
  * **Real-World DevOps Use Cases**
    * **Troubleshooting Server Issues:** Checking why the website is down by SSH-ing into the server, looking at `htop` for spiked CPU, using `free -h` for memory, and `tail -f`ing the application logs to read the error.
    * **Deploying Applications:** Using `scp` to send the new build artifact to the server, running `sudo chown` to ensure the web server has rights to read it, and restarting the service.
    * **Monitoring Production Systems:** Writing bash scripts utilizing `vmstat` and `uptime` to alert the team when system load is uncharacteristically high before an actual outage occurs.
    * **Managing Logs:** Setting up `logrotate` to prevent application logs from silently filling up the cloud VM disk space.
  * **Best Practices / Tips**:
    * **Root Security**: Log in as a normal user and use `sudo` selectively rather than root commands carelessly.
    * **Tab Completion & Flags**: Speed up CLI navigation with Tab keys and use human-readable flags (`free -h`, `df -h`) to verify disk and memory.
    * **Safety Checks**: Double check all `rm -rf` targets by running `ls` first. Preserve SSH security by keeping private key permissions restricted (`chmod 400`).

### Key Commands / Code Example:

```bash
# Review lesson files for specific commands and configurations of 🐧 Linux Practical Session (Hands-on DevOps Basics)
```

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## <a id="17-aws-s3-complete-guide-and-static-website-hosting"></a>17. AWS S3: Complete Guide and Static Website Hosting ☁️

🔗 **Full Lesson:** [17_AWS_S3_Static_Website_Hosting.md](./17_AWS_S3_Static_Website_Hosting.md)

* **What**: AWS S3 is "Object Storage" in the cloud. Think of it as an **infinite Google Drive or Dropbox** for your code, images, videos, and backups.
* **Why It Exists**: Traditional block devices (like EBS volumes) must be attached to a server, have fixed capacities, and are expensive to scale for massive volumes of static media or log files. S3 solves this by offering an infinite, internet-accessible object store with 11 9's durability, serverless static web hosting, and automatic multi-AZ (Availability Zone) data replication.
* **Key Concepts**:
  * **Introduction to AWS S3**: Fully managed "Object Storage" in the cloud. Acts as an infinite drive for flat files, images, videos, and backups, reachable directly via internet HTTP/HTTPS endpoints.
  * **Key Concepts: Buckets and Objects**
    * A **Bucket** is like a root folder.
    * **Global Uniqueness**: S3 bucket names must be globally unique because each bucket name becomes part of a public URL ``` https://my-portfolio.s3.amazonaws.com ```, and just like domain names(DNS) on the internet, only one unique name can exist worldwide to avoid conflicts, ensure correct data routing, and maintain security and proper access across all AWS users.
    * **An Object** is the file (and any metadata).
    * **Total Size Limit**: A single object can be up to **5 TB**.
    * **Single Upload Limit**: A single `PUT` upload has a limit of 5 GB; larger files must use multipart uploads.
  * **Understanding Data Sizes (KB - Kilobyte, MB - Megabyte, GB - Gigabyte, TB - Terabyte)**: Measures of digital data sizes based on the binary power of two calculations ($2^{10} = 1,024$).
  * **Object Storage vs Traditional Storage**: Contrast between flat URL-accessible object store (S3) and hierarchical system-mounted block stores (EBS / local disks).
  * **Durability and Availability**
    * **What it means**: If you store 10,000,000 objects in S3, you might lose one object every 10,000 years. It is designed to never lose your data.
    * **Replication**: Files uploaded to S3 are automatically replicated across at least 3 distinct physical Availability Zones (AZs) inside the target Region.
  * **Pricing and Management**
    * **Pay-as-you-go**: You only pay for active storage volume (GB/month), API requests (PUT/GET), and data transfers out.
    * **Free Tier**: AWS offers 5GB of S3 storage for the first 12 months.
    * **Access Controls**: Set security using IAM policies, Bucket Policies, ACLs (Access Control Lists), and the "Block Public Access" default private block.
  * **Advanced Features**
    * **What**: Keeps multiple versions of an object in the same bucket.
    * **Why**: Protects against accidental deletion or overwrites. You can "roll back" to an older version.
    * **S3 Transfer Acceleration**: Uses Amazon CloudFront’s globally distributed edge locations to speed up long-distance uploads.
    * **AWS Snowball**: A physical "suitcase" full of hard drives sent to your office. You load your data (Petabytes) and mail it back to AWS because uploading over the internet would take years.
    * **Heavy Bucket Deletion**: AWS UI (User Interface) limits fail when attempting to delete buckets containing 100,000+ objects. Use AWS CLI commands like `aws s3 rb s3://bucket-name --force` to delete.
  * **Hands-on: Static Website Hosting**: Steps to host public websites (HTML/CSS/JS) serverlessly by uploading files, disabling "Block Public Access", writing a public-read bucket policy, and enabling static website hosting.
  * **Real-World Examples**: Storing application assets, portfolios, daily server logs, and database backups.
  * **Common Mistakes Beginners Make**
    * **Keeping Buckets Public**: Accidentally leaving sensitive data (customer info) open to the world.
    * **Not Enabling Versioning**: Deleting a critical file and realizing there is no "Undo" button.
    * **Ignoring Data Transfer Costs**: Thinking storage is the only cost (forgetting about the cost of users downloading files).
  * **DevOps Best Practices**
    * **Use Infrastructure as Code (IaC)**: Use Terraform or AWS CDK (Cloud Development Kit) to create buckets instead of clicking in the console.
    * **Enable Encryption**: Always enable SSE-S3 (Server-Side Encryption with Amazon S3-Managed Keys) for security.
    * **Lifecycle Policies**: Automatically move old files to "S3 Glacier" (cheaper storage) after 30 days.
    * **Least Privilege**: Grant users only the minimum access they need.

### Key Commands / Code Example:

```text
[ AWS CLOUD ]
      |
      +---- [ Bucket: "my-app-data" (Unique Name) ]
               |
               +--- [ Object: "logo.png" ]
               |--- [ Object: "video.mp4" ]
               |--- [ Object: "v2/script.js" ] (Folders are fake; they are part of the "key")
```

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## <a id="18-s3-storage-classes-lifecycle-policies-rds-introduction"></a>18. S3 Storage Classes, Lifecycle Policies & RDS Introduction

🔗 **Full Lesson:** [18_S3_Storage_Classes_Lifecycle_RDS.md](./18_S3_Storage_Classes_Lifecycle_RDS.md)

* **What**: S3 Storage Classes are **different tiers of storage** offered by AWS, each designed for a specific data access pattern. Think of them as choosing between a **filing cabinet on your desk** (fast access, expensive) vs. a **warehouse across town** (slow access, cheap).
* **Why It Exists**: Not all data is accessed equally. Your app's homepage images are loaded millions of times daily (**hot data**), while a 3-year-old audit report might never be opened again (**cold data**).
* **Key Concepts**:
  * **S3 Storage Classes Overview**
    * **Using it**: A company storing 100 TB of logs can save **up to 90% in storage costs** by moving old logs to Glacier Deep Archive.
    * **Not using it**: You pay **Standard prices for everything**, even data nobody touches — burning money every month.
  * **Deep Dive: Each Storage Class**
    * **Glacier Instant**: Medical records, news media archives (need quick access but rarely)
    * **Glacier Flexible**: Disaster recovery, yearly compliance audits
    * **Deep Archive**: Regulatory data (banking/healthcare records kept for 7+ years), historical research data
  * **S3 Lifecycle Management**
    * **Using it**: Set-and-forget cost optimization. Data flows to cheaper tiers automatically.
    * **Not using it**: Manual management overhead, accidental overspending, human errors (forgetting to move data), and compliance violations (forgetting to delete data on time).
    * You **cannot** transition directly from Standard to Deep Archive skipping Glacier (must follow the tier order or use specific allowed transitions).
    * **Minimum storage duration** charges apply — if you move an object out of Glacier before 90 days, you still pay for 90 days.
  * **S3 Bucket Configuration**
    * **Enabled**: You can recover from accidental deletes (just remove the "Delete Marker"), roll back to any previous version.
    * **Disabled**: One wrong upload, and the old file is gone forever.
    * **Using it**: Data at rest is protected. Compliance requirements met. Even AWS employees can't read your data.
    * **Not using it**: One data breach = lawsuits, fines, customer trust destroyed.
  * **Architecture Diagrams with draw.io**
    * **Using it**: Clear communication, faster onboarding of new team members, better documentation.
    * **Not using it**: Miscommunication, confusion about infrastructure, longer meetings explaining setups verbally.
  * **Amazon RDS (Relational Database Service)  Preview**
    * **Using it**: Automated backups, patching, scaling, and high availability. You focus on your app, not infrastructure.
    * **Not using it**: You manually install the database on EC2, handle all updates yourself, risk data loss if you misconfigure backups.
    * Days 0–90: **S3 Standard** (frequent access)
    * Day 90: Transition to **Glacier Instant Retrieval** (rare but quick access needed for audits)

### Key Commands / Code Example:

```text
Object uploaded
      │
      ▼
┌─────────────────────────┐
│  Frequent Access Tier   │  ◄── Default landing tier
│  (like S3 Standard)     │
└────────┬────────────────┘
         │ Not accessed for 30 days
         ▼
┌─────────────────────────┐
│  Infrequent Access Tier │  ◄── Automatic, no retrieval fee
│  (40% cheaper)          │
└────────┬────────────────┘
         │ Not accessed for 90 days
         ▼
┌─────────────────────────┐
│  Archive Instant Access │  ◄── Optional, auto-enabled
│  (68% cheaper)          │
└────────┬────────────────┘
         │ Not accessed for 180 days
         ▼
┌─────────────────────────┐
│  Deep Archive Access    │  ◄── Optional, auto-enabled
│  (95% cheaper)          │
└─────────────────────────┘

  * If the object is accessed again at any point,
    it automatically moves BACK to the Frequent Access tier.
```

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## <a id="19-aws-rds-database-fundamentals"></a>19. AWS RDS & Database Fundamentals

🔗 **Full Lesson:** [19_AWS_RDS_Database_Fundamentals.md](./19_AWS_RDS_Database_Fundamentals.md)

* **What**: A **database** is an organized collection of data stored electronically so it can be easily accessed, managed, and updated. Think of it as a **digital filing cabinet** — instead of paper folders in a drawer, you have structured data on a server that programs can read and write to in milliseconds.
* **Why It Exists**: Every modern business runs on data. Without databases:
- A hospital can't look up patient records quickly during emergencies
- An e-commerce site can't track inventory, orders, or customer info
- A bank can't process millions of transactions daily
* **Key Concepts**:
  * **Database Introduction & History**
    * **Data-driven decisions**: Companies using databases can analyze trends, predict demand, and make informed choices.
    * **Business automation**: Automated billing, inventory tracking, and customer management.
    * **Preventing business collapse**: Without databases, critical data lives in spreadsheets or physical files — one fire, one crash, and everything is gone.
  * **Database Types**
    * **Right choice**: Application performs well, scales efficiently, maintenance is manageable.
    * **Wrong choice**: Constant refactoring, performance bottlenecks, expensive migrations. Imagine forcing IoT sensor data into rigid SQL tables — millions of inserts per second would crush a traditional RDBMS.
  * **Relational vs Non-Relational Databases**
  * **Deep Dive: MySQL**
    * **Free and open source** — no licensing costs
    * **Massive community** — tutorials, Stack Overflow answers, plugins everywhere
    * **Cross-platform** — runs on Linux, Windows, and Mac
    * **Language support** — works seamlessly with PHP, Node.js, Python, Java, and more
  * **Deep Dive: Oracle Database**
    * **Extreme security** — encryption, auditing, data masking built-in
    * **Disaster recovery** — Oracle Data Guard provides automatic failover
    * **Handles petabytes** — designed for massive enterprise datasets
    * **ACID compliance** — guarantees data consistency (critical for banking)
  * **Deep Dive: MongoDB**
    * **No predefined schema required** — perfect when the business doesn't know the data structure in advance
    * **Dynamic column creation** — add new fields anytime without altering a "table"
    * **Horizontal scaling** — add more servers easily (sharding built-in)
    * **Developer-friendly** — JSON is the native format of JavaScript, making it ideal for modern web apps
  * **Deep Dive: Apache Cassandra**
    * **IoT and sensor data** — handles millions of writes per second from thousands of devices
    * **No single point of failure** — every node is equal (masterless architecture)
    * **Handles different data formats simultaneously** — ideal for heterogeneous data sources
    * **Geo-distributed** — data can be replicated across multiple data centers
  * **AWS RDS (Relational Database Service)**
    * **Using RDS**: Focus on building your app, not managing database infrastructure. Automated backups mean you never lose data. Multi-AZ means automatic failover.
    * **Not using it**: You spend 40-60% of your time on database administration — patching, backup scripts, failover configuration, monitoring setup — time that could be spent building features.
    * Enables **data-driven decision making** (analytics, reports)
    * Supports **business automation** (billing, inventory, CRM)

### Key Commands / Code Example:

```text
1970          1978          1995          1996          2009          Today
  │             │             │             │             │             │
  ▼             ▼             ▼             ▼             ▼             ▼
┌──────┐    ┌──────────┐  ┌──────────┐  ┌───────────┐  ┌──────────┐  ┌──────────┐
│Codd's│    │  Oracle  │  │  MySQL   │  │PostgreSQL │  │ MongoDB  │  │ Cloud    │
│Paper │    │  Founded │  │ Released │  │ Released  │  │ Released │  │ Managed  │
│(RDBMS│    │ (First   │  │ (Open    │  │ (Advanced │  │ (NoSQL   │  │ DBs      │
│Theory│    │  Commer- │  │  Source  │  │  Open     │  │  Era     │  │ (RDS,    │
│)     │    │  cial DB)│  │  RDBMS)  │  │  Source)  │  │  Begins) │  │ Aurora)  │
└──────┘    └──────────┘  └──────────┘  └───────────┘  └──────────┘  └──────────┘

              Enterprise      Community       Community       Flexible      Fully
              Grade            Driven          Driven          Schema        Managed
```

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## <a id="20-aws-rds-mysql-setup-management-hands-on"></a>20. AWS RDS MySQL Setup & Management (Hands-On)

🔗 **Full Lesson:** [20_AWS_RDS_MySQL_Setup_and_Management.md](./20_AWS_RDS_MySQL_Setup_and_Management.md)

* **What**: Introduction and foundational concepts of AWS RDS  MySQL Setup & Management (Hands-On).
* **Why It Exists**: Solves deployment speed, consistency, and reliability challenges of AWS RDS  MySQL Setup & Management (Hands-On) in production.
* **Key Concepts**:
  * **PostgreSQL  Quick Introduction**
    * **Open source and free** — no licensing fees, community-driven improvements
    * **35+ years of maturity** — one of the most stable and battle-tested databases
    * **Hybrid capability** — store traditional rows AND JSON documents in the same database
    * **Strong ACID compliance** — guarantees data integrity for financial, healthcare, and mission-critical systems
  * **Creating a MySQL Database on AWS RDS**
    * **No server management** — AWS manages the OS, database software, and security patching
    * **Production-ready defaults** — automated backups, encryption, and monitoring built-in
    * **Scalable** — start small (free tier) and scale vertically or horizontally as demand grows
    * **High availability** — Multi-AZ deployment ensures automatic failover during outages
  * **EC2 Jump Host  Connecting to a Private RDS instance**
    * **Security**: RDS databases should **never** be directly exposed to the internet — this prevents unauthorized access and attacks
    * **Controlled access**: Only users who can SSH into the Jump Host can reach the database
    * **Audit trail**: All database connections go through a single point, making monitoring easier
    * **Best practice**: In production environments, databases are always in private subnets
  * **Basic SQL Operations on MySQL**
    * SQL is the **universal language** for all relational databases (MySQL, PostgreSQL, Oracle, SQL Server)
    * Understanding basic SQL is essential for **any role** — developers, DevOps engineers, data analysts, QA engineers
    * **Practicing SQL**: Builds a foundational skill used across almost every technology stack and every company.
    * **Not practicing**: You'll struggle with debugging data issues, writing application queries, or even reading database-related documentation in any tech role.
  * **Database Backup Strategies**
    * **Data is the most valuable asset** — losing customer data can mean losing the business
    * **Regulatory compliance** — industries like finance and healthcare require mandatory backup retention
    * **Disaster recovery** — natural disasters, region outages, or ransomware can wipe out primary databases
    * **Human error protection** — developers accidentally running `DROP DATABASE` in production (it happens!)
  * **Encryption Using KMS Keys**
    * **Compliance**: Regulations like HIPAA, GDPR, PCI-DSS **require** encryption of sensitive data
    * **Data breach protection**: Even if someone steals the physical disk or intercepts network traffic, they can't read the data without the key
    * **Defense in depth**: Encryption is one layer of a multi-layered security strategy
    * **Using encryption**: Even if storage hardware is stolen, backups are leaked, or snapshots are shared — data remains unreadable without the KMS key. You remain compliant with regulations.
  * **Auto-Scaling for Storage**
    * **Prevents downtime**: If a database runs out of storage, it crashes — all write operations fail
    * **Eliminates manual monitoring**: No need to watch disk usage graphs at 2 AM
    * **Cost-efficient**: You pay only for the storage you actually use (scales up, never down)
    * **Scales up to 65,000 GB (64 TB)**: Enough for virtually any workload
  * **Multi-AZ Deployment for High Availability**
    * **Zero manual intervention during failures** — AWS handles failover automatically
    * **Protection from**: hardware failure, AZ outages, OS patching, and DB instance maintenance
    * **SLA compliance** — critical for applications requiring 99.95%+ uptime
    * **No data loss** — synchronous replication means standby always has the latest data
  * **Snapshots  Manual & Automated**
    * **Disaster recovery**: Restore the database to a known good state
    * **Before risky changes**: Take a snapshot before running `ALTER TABLE` or schema migrations
    * **Data migration**: Create a snapshot, share it with another AWS account, and restore it there
    * **Long-term archival**: Keep snapshots beyond the automated backup retention period
  * **Monitoring with CloudWatch**
    * **Proactive issue detection**: Spot problems before they affect users
    * **Capacity planning**: Know when to scale up before you run out of resources
    * **Troubleshooting**: Correlate slow application performance with database metrics
    * **Alerting**: Get notified (email, SMS, Slack) when metrics exceed thresholds
  * **Connection Options & Code Snippets**
    * **Using code snippets**: Developers can integrate the database in minutes rather than hours. Reduces configuration errors.
    * **Hardcoding passwords in code**: A major security risk. Always use environment variables, AWS Secrets Manager, or IAM authentication for credentials in production.
    * Free storage is less than **10% of allocated storage**
    * Low storage condition persists for at least **5 minutes**

### Key Commands / Code Example:

```text
┌──────────────────────────────────────────────────────────────────────────┐
│                     PostgreSQL — HYBRID DATABASE                         │
│                                                                          │
│   ┌─────────────────────────────┐   ┌─────────────────────────────┐      │
│   │      SQL (Relational)       │   │      NoSQL (Document)       │      │
│   │                             │   │                             │      │
│   │  CREATE TABLE users (       │   │  CREATE TABLE events (      │      │
│   │    id SERIAL PRIMARY KEY,   │   │    id SERIAL PRIMARY KEY,   │      │
│   │    name VARCHAR(100),       │   │    data JSONB               │      │
│   │    email VARCHAR(255)       │   │  );                         │      │
│   │  );                         │   │                             │      │
│   │                             │   │  INSERT INTO events         │      │
│   │  Structured, fixed schema   │   │  VALUES ('{"type":"click",  │      │
│   │  with rows & columns        │   │   "page":"/home"}');        │      │
│   │                             │   │                             │      │
│   │  Ideal for: Banking,        │   │  Ideal for: Logging,        │      │
│   │  Inventory, User accounts   │   │  Analytics, Flexible data   │      │
│   └─────────────────────────────┘   └─────────────────────────────┘      │
│                                                                          │
│            BOTH live in the SAME database engine ✅                       │
└──────────────────────────────────────────────────────────────────────────┘
```

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## <a id="21-aws-vpc-networking-complete-beginners-guide"></a>21. AWS VPC & Networking Complete Beginner's Guide 🌐

🔗 **Full Lesson:** [21_VPC_and_Networking.md](./21_VPC_and_Networking.md)

* **What**: A VPC is a **logically isolated section of the AWS cloud** where you can launch your resources (servers, databases, etc.) in a **virtual network that you fully control**.
* **Why It Exists**: Before VPCs, all AWS resources were on a shared, flat public network — like working in an open-plan office where anyone could walk up to your desk. That's obviously a security nightmare.
* **Key Concepts**:
  * **VPC  Virtual Private Cloud**
    * It's **your private network** inside AWS's massive network.
    * You decide the **IP address range**, the **subnets**, the **traffic rules**, and the **security**.
    * Your resources are **isolated** from other AWS customers
    * You have **full control** over your network configuration
  * **CIDR Notation & IP Sizing**
    * The **starting address** of a network
    * **How many addresses** exist in that network
    * **Choose VPC range**: `/16` → gives you 65,536 IPs — plenty to split into many subnets
    * **Choose subnet range**: `/24` → 256 IPs per subnet is comfortable for most use cases
  * **Subnets  Public & Private**
    * **Reception & Lobby** (Public Subnet): Anyone from outside can come here
    * **Server Room & HR** (Private Subnet): Only authorised staff can enter — visitors are not allowed
    * Lives in **one Availability Zone (AZ)** — a physical data center location
    * Has its own **route table** that controls traffic
  * **Internet Gateway (IGW)**
    * Allows **two-way communication** (traffic IN and OUT)
    * Is **free** to use
    * Is **managed by AWS** — you don't need to maintain it
  * **NAT Gateway**
    * Lives in a **public subnet** (so it has internet access)
    * Has an **Elastic IP** (static public address)
    * Lets private subnet resources **send outbound requests** to the internet
    * **Blocks all inbound connections** from the internet to private resources
  * **Elastic IP**
    * Can be **associated** with an EC2 instance or NAT Gateway
    * **Persists** when the instance is stopped/started
    * Can be **re-assigned** to a different instance if needed (useful during failures)
  * **VPC Endpoints**
    * Traffic stays **within AWS's private network** — never touches the public internet
    * **No NAT Gateway needed** for these services → saves money
    * **Better security** — no internet exposure
    * **Lower latency** — shorter path
  * **Route Tables**
    * **Signposts/GPS System**: Set of routing rules determining where network traffic is directed from subnets.
    * **Required Association**: Every subnet must be linked to a route table; default is the Main Route Table.
    * **Outbound Routing**: Public route tables route internet-bound traffic (`0.0.0.0/0`) to the Internet Gateway, while private tables direct it to a NAT Gateway or VPC Endpoint.
    * **Local Route**: The automatic route allowing all subnets within the VPC to communicate internally (cannot be deleted).
  * **IPv4 vs IPv6**
    * **IPv4** is like the old phone system with 10-digit numbers. When the population grew, they started running out of unique numbers.
    * **IPv6** is the new system with 20-digit numbers — enough for every device on Earth (and then some).
    * VPCs use **IPv4 by default** with private ranges (like 10.0.0.0/16)
    * You can optionally enable **IPv6** — AWS assigns a `/56` IPv6 block
  * **TCP vs UDP**
    * **Security Groups** have rules for both TCP and UDP ports
    * Understanding TCP vs UDP helps you write **correct security group rules**
  * **Egress-Only Internet Gateway**
    * **One-Way IPv6 Exit**: Stateful gateway that allows private subnet resources (with IPv6 addresses) to initiate outbound internet connections.
    * **Inbound Block**: Prevents the external public internet from initiating any direct inbound connections back to those private resources.
    * **Cost-Efficient**: Serves as the free, managed IPv6 counterpart to the expensive NAT Gateway.
  * **Practical Lab Walkthrough**
    * **Tier 1 (Web):** Public subnets for Load Balancers & Web Servers (Internet accessible)
    * **Tier 2 (App):** Private subnets for Application Servers (Outbound internet only via NAT Gateway)
    * **Tier 3 (Data):** Secure Private subnets for Databases (Strictly isolated, zero internet routing)
    * **What:** Creating the private, isolated virtual network boundary.

### Key Commands / Code Example:

```
Step 1: Choose your plot (IP address range) — e.g., 10.0.0.0/16
Step 2: Divide it into rooms (subnets) — public rooms and private rooms
Step 3: Install a main gate (Internet Gateway) for public access
Step 4: Set up a backdoor for deliveries (NAT Gateway) for private rooms
Step 5: Put up signposts (Route Tables) to direct traffic
Step 6: Add security guards (Security Groups & NACLs)
```

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## 22. VPC Networking NACL, CIDR, VPC Peering & Transit Gateway

🔗 **Full Lesson:** [22_NACL_CIDR_VPC_Peering_and_Transit_Gateway.md](./22_NACL_CIDR_VPC_Peering_and_Transit_Gateway.md)

* **What**: A **Network Access Control List (NACL)** is a security layer that works at the **subnet level** inside a VPC. It controls what traffic is allowed **in and out** of an entire subnet.
* **Why It Exists**: Security Groups protect individual EC2 instances — but what if 10 servers in a subnet are all being attacked by the same malicious IP? You'd have to update 10 Security Groups.
* **Key Concepts**:
  * **Network ACL (NACL)**
  * **CIDR Calculations**
  * **VPC Peering**
    * But route tables on **both sides** must be configured
  * **Transit Gateway**
    * **Setup 3 EC2 Instances (Ubuntu)**:
    * **Target Instance 1**: Subnet A, install a basic web server.
    * **Target Instance 2**: Subnet B, install a basic web server.
    * **Attacker Instance**: Any subnet, will act as the malicious IP.

### Key Commands / Code Example:

```
Inbound Rules Example:
┌─────────┬────────────┬──────────┬───────────┐
│ Rule #  │ Source IP  │ Protocol │ Action    │
├─────────┼────────────┼──────────┼───────────┤
│  100    │ 99.33.36.0 │  ALL     │  DENY     │
│  200    │ 0.0.0.0/0  │  HTTP    │  ALLOW    │
│  *      │ 0.0.0.0/0  │  ALL     │  DENY     │
└─────────┴────────────┴──────────┴───────────┘
Rule 100 is checked first → blocks 99.33.36.x before rule 200 even runs.
```

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## 23. AWS CloudWatch Monitoring & Billing Management

🔗 **Full Lesson:** [23_AWS_CloudWatch_Monitoring_and_Billing.md](./23_AWS_CloudWatch_Monitoring_and_Billing.md)

* **What**: AWS CloudWatch is AWS's built-in **observability and monitoring service**. Think of it as a CCTV system for your cloud infrastructure.
* **Why It Exists**: Without monitoring, you are flying blind. You won't know:
- Why your application is slow
- When a server is about to crash
- How much money you are burning
* **Key Concepts**:
  * **What is AWS CloudWatch?**
  * **EC2 Monitoring with CloudWatch**
    * **Enabled:** You can see trends, spot anomalies, and respond before a crash.
    * **Not enabled:** You are guessing when something goes wrong and have no historical data to debug with.
  * **CloudWatch Alarms**
    * Send a notification via **SNS**
    * Trigger an **Auto Scaling** action
    * Alarms trigger **continuously** as long as the breach persists — not just once.
    * A **single spike** that lasts less than the evaluation period will NOT trigger an alarm (by design — reduces false alerts).
  * **SNS  Simple Notification Service**
  * **CloudWatch Dashboards**
    * Create **one dashboard per project or environment** (e.g., `prod-web-servers`, `dev-databases`), not one per VM.
    * Use **different colors** for each instance on a combined graph to distinguish them easily.
    * Pin **alarm status widgets** alongside metric graphs so you see both the data and its health status.
    * **With dashboards:** Instant situational awareness for the whole team; faster incident response.
  * **AWS Billing Management & Budget Alerts**
    * Always check **Free Tier Usage** at the end of each lab.
    * Going over free tier limits = **you get charged** — no automatic warning unless you set it up.
  * **Monitoring Best Practices**
  * **Visual Diagrams**
    * **Metrics** – Time-series numerical data (e.g., CPU utilization, request count)
    * **Logs** – Text-based event records collected from applications and services
    * **Alarms** – Rules that watch metrics and trigger actions when thresholds are breached
    * **Dashboards** – Custom visual pages that display metrics and alarm status

### Key Commands / Code Example:

```
OK  ──────────────────────────────────►  (Everything is normal)
                  │
                  │  threshold crossed
                  ▼
ALARM  ──────────────────────────────►  (Notification triggered)
                  │
                  │  metric drops below threshold
                  ▼
OK  ──────────────────────────────────►  (Back to normal)

INSUFFICIENT_DATA = not enough data points yet to evaluate
```

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## 24. AWS Lambda & Serverless Architecture

🔗 **Full Lesson:** [24_AWS_Lambda_and_Serverless_Architecture.md](./24_AWS_Lambda_and_Serverless_Architecture.md)

* **What**: Serverless computing is a cloud model where **you write code and the cloud provider manages everything else** – servers, OS, scaling, patching, availability. You never "see" or manage a server.
* **Why It Exists**: Traditional approach: You rent a virtual machine (EC2), install software, manage uptime, pay 24/7. Serverless approach: You deploy a function, it runs *only when triggered*, and you pay *only for that run time*.
* **Key Concepts**:
  * **What is Serverless Computing?**
    * **With serverless:** Low cost, zero server management, infinite scalability.
    * **Without serverless:** You'd need a running server 24/7, manual scaling, higher ops overhead.
  * **AWS Lambda  Deep Dive**
    * ✅ **Used:** No servers to manage, automatic scaling, cost-efficient.
    * ❌ **Not used:** You'd need to run EC2 instances round the clock for event-driven tasks — wasteful and expensive.
  * **Project Architecture  Image Resizing**
  * **Key AWS Services Involved**
  * **Practical Implementation with Terraform**
  * **How Lambda Triggering Works**
  * **Visual Diagrams**

### Key Commands / Code Example:

```
1. Event occurs (e.g., file uploaded to S3)
        ↓
2. AWS detects the trigger
        ↓
3. Lambda spins up a compute container
        ↓
4. Your code runs inside it
        ↓
5. Output is produced (file saved, notification sent, etc.)
        ↓
6. Container is shut down
        ↓
7. You are billed for only the time your code ran
```

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## 25. Git & GitHub Fundamentals

🔗 **Full Lesson:** [25_Git_and_GitHub_Fundamentals.md](./25_Git_and_GitHub_Fundamentals.md)

* **What**: Version control is a system that **tracks and manages changes** to files over time. Think of it like Google Docs' version history — but far more powerful, built specifically for code.
* **Why It Exists**: Without version control:
- You'd manually save files like `project_v1.py`, `project_v2_final.py`, `project_v2_FINAL_REAL.py` 😅
- Two developers editing the same file would overwrite each other's work
- One bad change could destroy months of work with no way to recover
- There'd be no record of *who* changed *what* and *when*
* **Key Concepts**:
  * **What is Version Control?**
  * **Git  The Local Version Control Tool**
  * **GitHub  The Cloud Hosting Platform**
  * **Git vs GitHub  Side-by-Side Comparison**
  * **Market Landscape**
    * **99% of developers** use Git as their version control system
  * **The Git Workflow  Step by Step**
    * **Action:** Download the installer from [git-scm.com](https://git-scm.com/).
    * **Tip:** For Windows users, the installation includes **Git Bash**, a terminal that allows you to use Linux-like commands on Windows.
    * **Action:** Sign up for a free account at [github.com](https://github.com/).
    * **Role:** While Git tracks changes locally, GitHub acts as your "Cloud Garage" where you store and share your work.
  * **Core Git Commands Explained**
    * **What:** Initializes a brand new Git repository in the current folder
    * **What it creates:** A hidden `.git/` folder that stores all version history
    * **When to use:** Once, at the start of every new project
    * **What:** Moves files from *Untracked* → *Staged* (tells Git "include these in the next snapshot")
  * **First-Time Git Configuration**
  * **Visual Diagrams**
    * `git add` moves files to the **Staging Area** — it tells Git "I want to include these changes in my next snapshot." It does NOT save permanently.
    * `git commit` takes the staged changes and creates a **permanent snapshot** in the local repository with a unique ID and message.
    * `git commit` saves a snapshot to your **local** repository only — no internet required
    * `git push` uploads those local commits to the **remote** repository (e.g., GitHub)

### Key Commands / Code Example:

```
Git Hosting Market Share (2026 estimate)
─────────────────────────────────────────
GitHub     ████████████████████████████  70%
GitLab     ████████                      10%
Bitbucket  ████████                      10%
Others     ████████                      10%
```

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## 26. Git & GitHub Deep Dive: Branching, PRs & Collaboration

🔗 **Full Lesson:** [26_Git_and_GitHub_Deep_Dive_Branching_PRs_and_Collaboration.md](./26_Git_and_GitHub_Deep_Dive_Branching_PRs_and_Collaboration.md)

* **What**: Git is an **open-source, distributed version control system** operated primarily through the **CLI (Command Line Interface)**. "Distributed" means every developer has the **full copy** of the repository — history, branches, and all — on their own machine.
* **Why It Exists**: Centralized systems (like older SVN) had a single server. If that server went down, no one could work.
* **Key Concepts**:
  * **Git as a Distributed System**
  * **Essential Git Commands**
    * **What:** Downloads a full copy of a remote repository to your local machine
    * **When:** First time you want to start working on an existing project
    * **Creates:** A local folder with all files, branches, and history
    * **What:** Shows the current state of your working directory and staging area
  * **Fork vs Clone  Cloud vs Local**
  * **Branching Strategy**
  * **Pull Request (PR) Workflow**
    * Keep PRs **small and focused** — one feature or bug fix per PR
    * Write a **clear description** — what, why, and how to test
    * **Link the Jira/issue ticket** in the PR description
    * Respond to reviewer comments **within 24 hours**
  * **Merge Conflicts & Resolution**
    * Everything between `<<<<<<< HEAD` and `=======` is **your current version**
    * Everything between `=======` and `>>>>>>>` is the **incoming version**
    * You must **manually pick one** (or combine them), then delete the markers
    * Pull from main **before starting new work** and **regularly during development**
  * **GitHub Repository Settings & Features**
    * **Public:** Anyone on the internet can see the code (used for open source)
    * **Private:** Only invited collaborators can see it (used for company code)
    * **Read** – can view code
    * **Write** – can push branches
  * **Advanced Git Concepts**
    * **What:** Re-applies your commits on top of another branch's latest commits — creates a cleaner, linear history
    * **vs Merge:** Merge preserves the true history (including branch divergence); Rebase rewrites history to look linear
    * **Use with caution:** Never rebase commits that have already been pushed to a shared remote
    * **What:** Moves the current branch pointer backwards to an earlier commit
  * **DevOps Engineer's Role in GitHub**
  * **Visual Diagrams**
    * `git fetch` downloads the changes but does **not** merge them into your local branch. Your working directory stays untouched. You can inspect what changed before deciding to merge.
    * **Fork** is a cloud-to-cloud operation — it copies a repo from someone else's GitHub account to your GitHub account. No download happens.
    * **Clone** is a cloud-to-local operation — it downloads a repo from GitHub to your machine.
    * `git reset` moves the branch pointer backwards, **rewriting history**. It's dangerous on shared branches because it removes commits others may have already pulled.

### Key Commands / Code Example:

```bash
git status
# On branch main
# Changes not staged for commit:
#   modified: index.html
# Untracked files:
#   new-feature.py
```

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## 27. Introduction to CI/CD and Jenkins

🔗 **Full Lesson:** [27_Introduction_to_CICD_and_Jenkins.md](./27_Introduction_to_CICD_and_Jenkins.md)

* **What**: Think of it as an **automated assembly line for software** — code goes in one end, and a tested, packaged, deployable product comes out the other.
* **Why It Exists**: Before CI/CD existed, releasing software looked like this:
- Developers worked on separate code for weeks or months
- Code was manually merged at the end ("integration hell")
- A dedicated QA team manually tested everything
- Deployment was a stressful, all-hands event that could take days
- Bugs discovered late were expensive and slow to fix
* **Key Concepts**:
  * **What is CI/CD?**
  * **Continuous Integration (CI)  Deep Dive**
  * **The CI Pipeline  Step by Step**
    * **What happens:** A developer finishes a feature, commits, and pushes to GitHub (their feature branch or main)
    * **Trigger:** This event *automatically triggers* the entire CI pipeline
    * **Tool:** Git / GitHub
    * **What happens:** The CI tool (Jenkins) pulls the code and checks whether it compiles without errors
  * **Jenkins  The CI/CD Engine**
    * **Market Share:** 60–70% of CI/CD market
    * **Type:** Open-source (free)
    * **Language:** Written in Java
    * **Version in class:** 2.55.1
  * **Jenkins Setup  From Zero to Running**
    * **Why?** This is for **security**. It acts as a digital signature.
    * **How it works:** When you run `apt install`, Ubuntu uses this key to verify that the Jenkins software hasn't been modified or tampered with by hackers. If the signature doesn't match, your system will block the installation.
    * **Modern Standard:** We use `/etc/apt/keyrings/` to store the key, which is the current recommended practice for Debian-based systems like Ubuntu.
    * **Why?** It tells Ubuntu exactly **where to look** for Jenkins on the internet.
  * **Your First Jenkins Job**
    * Click **"New Item"** on Jenkins dashboard
    * Select **"Freestyle project"**
    * Scroll to **"Source Code Management"**
    * Select **Git**
  * **Key Commands Reference**
  * **Visual Diagrams**
    * A **Freestyle Project** is configured through Jenkins' web UI — you fill in forms to specify the source repo, build steps, and post-build actions. It's beginner-friendly but limited for complex workflows.
    * A **Pipeline** is defined as code in a file called `Jenkinsfile`, stored in the repository itself. It supports complex multi-stage workflows, conditional logic, parallel execution, and follows Infrastructure-as-Code principles.
    * **Continuous Delivery** means the pipeline automatically produces a release-ready artifact and deploys it to a staging environment. The final push to **production requires a manual approval**.
    * **Continuous Deployment** is fully automated — every change that passes all tests is automatically deployed all the way to **production** with no human intervention.
  * **🔧 How This Applies to My Tech Stack**

### Key Commands / Code Example:

```
Cloning repository https://github.com/yourname/hello-java.git
[hello-world-java] $ /bin/sh -xe /tmp/jenkins...
+ javac HelloWorld.java
+ java HelloWorld
Hello, World!
Finished: SUCCESS
```

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## 28. Jenkins Deep Dive: Users, RBAC, CI Pipelines & Local Setup

🔗 **Full Lesson:** [28_Jenkins_Deep_Dive_Users_RBAC_CI_Pipelines_and_Local_Setup.md](./28_Jenkins_Deep_Dive_Users_RBAC_CI_Pipelines_and_Local_Setup.md)

* **What**: Jenkins has a built-in **user management system** that lets you create individual accounts for every person who needs access to Jenkins. Each user can have their own login credentials and, through security settings, different levels of access.
* **Why It Exists**: In a real company, Jenkins is connected to your production pipelines. You cannot give everyone admin-level access:
- A **developer** should be able to trigger builds — not delete them
- An **L1 support** team member might only need to *view* build logs — not configure jobs
- An **admin** manages everything
* **Key Concepts**:
  * **Jenkins User Management & Security**
    * A **developer** should be able to trigger builds — not delete them
    * An **L1 support** team member might only need to *view* build logs — not configure jobs
    * An **admin** manages everything
  * **Role-Based Access Control (RBAC)**
  * **Continuous Integration  Automated Triggers**
  * **Java Application Build & Deployment in Jenkins**
  * **Jenkins Local Installation (WAR File Method)**
  * **Plugin Lifecycle Management**
  * **Real-Time DevOps Mindset**
  * **Visual Diagrams**
    * **Git Plugin** — connects Jenkins to GitHub/GitLab repositories
    * **Role-based Authorization Strategy** — enables RBAC for user permissions
    * **Pipeline** — enables writing pipelines as code in a Jenkinsfile
    * **Maven Integration** — supports building Java projects with Maven
  * **🔧 How This Applies to My Tech Stack**

### Key Commands / Code Example:

```
Step 1: Log in as admin
Step 2: Go to → Dashboard → Manage Jenkins → Users
Step 3: Click → "Create User"
Step 4: Fill in:
         - Username   (e.g., balaji)
         - Password
         - Full Name
         - Email
Step 5: Click → "Create User"
Step 6: Test in incognito window:
         - Open new incognito tab
         - Go to Jenkins URL
         - Log in with new credentials
         - Verify access works correctly
```

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## 29. Java, Spring Boot, Maven & Jenkins Build Pipeline

🔗 **Full Lesson:** [29_Java_Spring_Boot_Maven_and_Jenkins_Build_Pipeline.md](./29_Java_Spring_Boot_Maven_and_Jenkins_Build_Pipeline.md)

* **What**: Java is a **high-level, object-oriented, platform-independent programming language** created by Sun Microsystems in 1995 (now owned by Oracle). "High-level" means it uses human-readable syntax rather than machine code.
* **Why It Exists**: Java was designed around one core promise: **"Write Once, Run Anywhere" (WORA)**. Code written on a Windows machine should run identically on Linux, Mac, or any other platform — without modification.
* **Key Concepts**:
  * **Java Fundamentals**
  * **Java Compilation  How Code Becomes a Running App**
    * Jenkins stores the `.jar` as the **build artifact**
  * **Spring Boot Framework**
  * **Maven Build Tool**
    * Automatic dependency downloading from **Maven Central** (a massive public library registry)
    * **What:** Deletes the `target/` directory (all previously compiled files)
    * **Why:** Ensures your next build starts completely fresh — no leftover old files mixing with new
    * **When:** Always run before a full rebuild; prevents "dirty build" issues
  * **pom.xml  The Project Blueprint**
  * **Jenkins + Maven  Full Build Pipeline**
  * **Application Deployment & Port Configuration**
  * **Java's Platform Independence  Proven in Practice**
    * Build **once** in CI (on Linux Jenkins server)
    * Deploy the **same artifact** to any environment
  * **Visual Diagrams**
    * **JAR (Java Archive)** — A packaged Java application that is self-contained. For Spring Boot, the JAR includes an embedded web server (Tomcat), so you run it with `java -jar app.jar` directly. No external server needed.
    * **WAR (Web Application Archive)** — A packaged Java web application designed to be deployed *inside* an external Java web server (like Apache Tomcat or JBoss). The server must be installed and running separately.
    * **groupId/artifactId/version** — The project's unique identity (like a "name and address")
    * **packaging** — Output format: `jar` or `war`
  * **🔧 How This Applies to My Tech Stack**

### Key Commands / Code Example:

```
my-application/
├── pom.xml                          ← Maven config (dependencies, build)
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/example/app/
│   │   │       └── Application.java ← Main entry point
│   │   └── resources/
│   │       └── application.properties ← App config (port, DB, etc.)
└── target/                          ← Build output (created by Maven)
    └── shopping-cart.jar            ← The final deployable artifact
```

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## 30. Jenkins Pipelines: Declarative, Scripted & CI Integration

🔗 **Full Lesson:** [30_Jenkins_Pipelines_Declarative_Scripted_and_CI_Integration.md](./30_Jenkins_Pipelines_Declarative_Scripted_and_CI_Integration.md)

* **What**: A **Jenkins Pipeline** is a way to define your entire CI/CD build process as **code** — written in a file called a `Jenkinsfile`. Instead of clicking through forms in the Jenkins UI (Freestyle), you write the build steps as a script that Jenkins reads and executes.
* **Why It Exists**: Freestyle projects work for simple setups, but they have serious limitations in real teams:
* **Key Concepts**:
  * **Freestyle Jobs vs Pipelines  Why Upgrade?**
  * **Two Ways to Define a Pipeline**
    * **What:** You write the pipeline code directly inside the Jenkins job configuration UI
    * **Where it lives:** Inside Jenkins itself (not in your code repository)
    * **Good for:** Quick experiments, learning, demos
    * **Bad for:** Real projects — no version control, lost if Jenkins crashes
  * **Declarative vs Scripted Pipeline**
  * **Pipeline Syntax  Every Block Explained**
  * **Pipeline Syntax Generator**
  * **Building a Java Pipeline  Step by Step**
  * **Real Project Pipeline  Freestyle to Pipeline Migration**
    * Executes the built Spring Boot JAR file directly in the **foreground** using its absolute workspace path.
    * ⚠️ **Warning:** Because this command runs in the foreground without `nohup` or `&`, it will cause Jenkins to hang indefinitely waiting for the process to finish (which leads perfectly into the explanation in Section 8).
  * **Foreground vs Background Processes  The nohup Fix**
    * **`nohup`** = "No Hang Up" — tells the process to keep running even if the terminal/Jenkins session that started it closes
    * **`&`** = runs in background
  * **CI Configuration with Poll SCM**
  * **Key Jenkins Plugins Reference**
  * **Visual Diagrams**
    * **Declarative** starts with `pipeline {` and enforces a structured format. It's easier to read, produces clearer error messages, and is recommended for most use cases. The pipeline structure (agent, stages, post) is defined and predictable.
    * **Scripted** starts with `node {` and gives complete programmatic freedom — you can write arbitrary Groovy code anywhere. It's more powerful for complex custom logic but harder to maintain and debug.
    * **`pollSCM`** — Jenkins periodically checks the Git repository for new commits on a cron schedule. Simple to configure, works on private networks, but introduces polling delay and wastes resources checking when nothing changed.
    * **GitHub Webhook** — GitHub calls Jenkins immediately when a push event occurs. Real-time (sub-second trigger), no wasted polling, but requires Jenkins to be publicly reachable (or use a reverse proxy/tunnel).
  * **🔧 How This Applies to My Tech Stack**

### Key Commands / Code Example:

```
Jenkins Job → Configure → Pipeline → Definition: "Pipeline Script from SCM"
→ SCM: Git
→ Repository URL: https://github.com/yourname/your-repo.git
→ Branch: */main
→ Script Path: Jenkinsfile   ← the filename in your repo
```

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## 31. Jenkins Master-Slave Architecture & Node Configuration

🔗 **Full Lesson:** [31_Jenkins_Master_Slave_Architecture_and_Node_Configuration.md](./31_Jenkins_Master_Slave_Architecture_and_Node_Configuration.md)

* **What**: Introduction and foundational concepts of Jenkins Master-Slave Architecture & Node Configuration.
* **Why It Exists**: Imagine a single Jenkins server handling everything for a team of 50 developers:
- Every developer pushes code → Jenkins triggers a build
- 10 builds running simultaneously on one machine
- The machine's CPU, RAM, and disk are maxed out
- Builds slow down dramatically or fail entirely
- The master server becomes a bottleneck and single point of failure
- Different teams need different environments (Java vs Python vs Node.js) — one machine can't cleanly support all
* **Key Concepts**:
  * **Why Master-Slave? The Problem It Solves**
  * **Master-Slave Architecture  How It Works**
  * **Jenkins Internal File Structure**
  * **Jenkins Installation on Windows (MSI Method)**
  * **Setting Up a Slave Node  Step by Step**
  * **Connecting the Slave Using agent.jar**
  * **Assigning Jobs to Specific Nodes**
  * **Troubleshooting Offline Nodes**
    * If not yet started → **wait in a "pending" state** until the agent comes back online
    * If already running → **fail immediately** with a "connection lost" error
  * **Real-World Node Naming & Team Isolation**
  * **Assignment Configurations Reference**
    * **Status:** 2 Ubuntu VMs created in GCP (e.g., `jenkins-master` and `jenkins-slave`).
    * **Goal:** Orchestrate builds from the Master VM onto the Slave VM.
    * **Launch:** 1 Ubuntu VM (Master) and 1 CentOS VM (Slave).
    * **Key Difference:** Handling different package managers and OS hierarchies.
  * **Visual Diagrams**
    * **Package manager:** Ubuntu uses `apt` (`sudo apt install openjdk-21-jre -y`); CentOS uses `yum` or `dnf` (`sudo yum install java-21-openjdk -y`)
    * **Default paths:** Ubuntu stores Java at `/usr/lib/jvm/`; CentOS at `/usr/lib/jvm/java-21-openjdk/`
    * **Firewall tool:** Ubuntu uses `ufw`; CentOS uses `firewalld`
    * **Service management:** Both use `systemd` in modern versions
  * **🔧 How This Applies to My Tech Stack**

### Key Commands / Code Example:

```
Step 1: Developer pushes code to GitHub
Step 2: GitHub triggers Jenkins master (webhook) or master polls SCM
Step 3: Master receives trigger, looks up the job configuration
Step 4: Master checks which agents are available and match the job's requirements
Step 5: Master assigns the build to the best available agent
Step 6: Agent receives the assignment, pulls the code from GitHub
Step 7: Agent executes all pipeline stages (compile, test, package, deploy)
Step 8: Agent sends logs and result back to master in real time
Step 9: Master displays results in UI, sends notifications
Step 10: Agent workspace is cleaned up (optional)
```

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## 32. Jenkins Day-to-Day Operations, Parameterized Jobs & AWS Core Services

🔗 **Full Lesson:** [32_Jenkins_Day-to-Day_Operations_Parameterized_Jobs_and_AWS_Core_Services.md](./32_Jenkins_Day-to-Day_Operations_Parameterized_Jobs_and_AWS_Core_Services.md)

* **What**: Day-to-day Jenkins management means you're not just setting it up once — you're actively monitoring, troubleshooting, and maintaining it. This section covers the most common problems that appear in real jobs.
* **Why It Exists**: Solves deployment speed, consistency, and reliability challenges of Jenkins Day-to-Day Operations, Parameterized Jobs & AWS Core Services in production.
* **Key Concepts**:
  * **Jenkins Real-World Problems & Solutions**
  * **Jenkins Restart Methods**
    * **Graceful restart** waits for running builds to finish (preferred)
    * **Force restart** stops everything immediately (use only when Jenkins is stuck)
    * **System restart** restarts the underlying OS (last resort)
  * **Parameterized Jobs  One Job, Many Environments**
  * **Jenkins Credentials Management**
  * **Amazon Aurora  Enterprise Cloud Database**
    * The storage layer spans **6 copies across 3 Availability Zones** automatically
  * **Amazon CloudFront  CDN**
    * Content is cached at **edge locations** (400+ worldwide)
  * **AWS IAM Policies  Permissions as Code**
  * **Tech Stack Mapping**
  * **Visual Diagrams**
  * **Code & Practical Examples**

### Key Commands / Code Example:

```
Step 1: Click the failed build number (e.g., #7 ❌)
Step 2: Click "Console Output"
Step 3: Scroll to the bottom — look for "ERROR" or "FAILED"
Step 4: Read the lines ABOVE the error — context explains the cause
Step 5: Google the exact error message if needed
Step 6: Fix the root cause, re-run
```

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## 33. Introduction to Docker: Containers, Images & Architecture

🔗 **Full Lesson:** [33_Introduction_to_Docker_Containers_Images_and_Architecture.md](./33_Introduction_to_Docker_Containers_Images_and_Architecture.md)

* **What**: Before Docker, the standard way to package and run applications was using **Virtual Machines (VMs)**. Docker replaces VMs for most use cases with something far lighter and faster — **containers**.
* **Why It Exists**: 1. **Environment consistency:** Same container in dev, test, and production
2.
* **Key Concepts**:
  * **The Problem Docker Solves  VMs vs Containers**
    * **Heavyweight:** Each VM requires a complete Guest OS (e.g., a full 2GB+ Ubuntu or Windows installation) just to run an application.
    * **Strong Isolation:** Because each VM has its own kernel and OS, they are highly isolated from one another. A kernel crash or security breach in one VM typically won't affect others.
    * **Resource Intensive:** VMs consume significant RAM, CPU, and disk space just to keep the Guest OS running, meaning high overhead and fewer resources for the actual application.
    * **Slow Startup:** Booting a VM takes minutes because it has to perform a full OS boot sequence, just like a physical machine.
  * **What is Docker?**
  * **Docker Architecture  The Three Parts**
    * **What:** The CLI (command line interface) where YOU type Docker commands
    * **How it works:** Accepts your commands (`docker run`, `docker build`) and sends them to the Docker Daemon via REST API
    * **Where it runs:** Your local machine, or any server where you type Docker commands
    * **What:** A background service (daemon process) running on your machine that does all the actual work
  * **Docker Hub  The Image Registry**
  * **The Docker Workflow  From Code to Container**
  * **Dockerfile  The Blueprint**
  * **Core Docker Commands**
  * **Docker Installation on Ubuntu (GCP)**
  * **Container Lifecycle  Why Containers Exit**
  * **Image Sizes & Alpine Linux**
  * **Tech Stack Mapping**
  * **Visual Diagrams**
  * **Code & Practical Examples**

### Key Commands / Code Example:

```text
Physical Hardware
      │
      ▼
Hypervisor (VMware / KVM)
      │
      ├── VM 1: Full OS (Ubuntu) + App A    ← 2.5GB+ each
      ├── VM 2: Full OS (Windows) + App B
      └── VM 3: Full OS (CentOS) + App C
```

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## 34. Docker Day 2: Container Operations, Port Mapping, Volumes & Management

🔗 **Full Lesson:** [34_Container_Operations_Port_Mapping_Volumes_and_Management.md](./34_Container_Operations_Port_Mapping_Volumes_and_Management.md)

* **What**: Every Docker container moves through a series of **states** during its life. Understanding these states and the commands that transition between them is the foundation of day-to-day Docker work.
* **Why It Exists**: Solves deployment speed, consistency, and reliability challenges of Docker Day 2: Container Operations, Port Mapping, Volumes & Management in production.
* **Key Concepts**:
  * **Docker Container Lifecycle  The Full Picture**
  * **Port Mapping  Connecting the Outside World**
    * **GCP:** Add Firewall Rule allowing the host port
    * **AWS:** Add Inbound Rule in Security Group for the host port
  * **Volume Mapping  Persisting Data Outside Containers**
    * **Check status:** `docker ps`
    * **Access in browser:** `http://YOUR_VM_IP:8080` (or `localhost:8080` if local)
    * **Speed:** Develop and test websites instantly without environment setup.
    * **Isolation:** Your host machine stays clean (no NGINX installed locally).
  * **Running Modes  Detached vs Interactive**
    * **Foreground (default):** Container output appears in your terminal. Terminal is blocked.
    * **Detached (`-d`):** Container runs in background. Terminal is free.
    * **Interactive (`-it`):** Your terminal connects to the container's shell. You can type commands inside it.
  * **Container Naming & Management**
  * **NGINX  The Modern Web Server**
  * **Accessing Running Containers  docker exec**
  * **Container Monitoring  docker stats**
  * **Bulk Container Operations**
  * **Shell Types Inside Containers**
  * **Complete Docker Command Reference**
  * **Tech Stack Mapping**
  * **Visual Diagrams**
  * **Code & Practical Examples**

### Key Commands / Code Example:

```bash
docker stop my-nginx
# Sends SIGTERM signal — gives the container time to shut down cleanly
# Waits 10 seconds, then sends SIGKILL if still running
# Best practice: always try stop before kill
```

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## 35. Dockerfiles, Custom Images, Docker Hub & Troubleshooting

🔗 **Full Lesson:** [35_Dockerfiles_Custom_Images_Docker_Hub_and_Troubleshooting.md](./35_Dockerfiles_Custom_Images_Docker_Hub_and_Troubleshooting.md)

* **What**: A **Dockerfile** is a plain text file (no extension) containing a sequence of instructions that tells Docker how to **build a custom Docker image**. It's the recipe for creating your application's container.
* **Why It Exists**: Without a Dockerfile:
- You'd manually install everything inside a running container every time
- No reproducibility — "works on my machine" problem returns
- No version control for your environment
- Can't automate image creation in CI/CD
* **Key Concepts**:
  * **What is a Dockerfile?**
    * **Reproducible:** Same image built on any machine, any time
    * **Version controlled:** Lives in your Git repo with your code
    * **Automated:** Jenkins/GitHub Actions can build it automatically
    * **Documented:** Every dependency and config step is explicitly written
  * **Dockerfile Instructions  Every Command Explained**
    * **What:** Defines the starting point — the base OS or runtime your image builds on
    * **Why:** You don't build from nothing. You start from an existing image (OS, language runtime) and add on top
    * **Rule:** Every Dockerfile MUST start with `FROM` (except multi-stage builds)
    * **What:** Adds author/contact information to the image metadata
  * **The 5-Stage Dockerfile Structure**
  * **Building a Custom Docker Image**
  * **Image Tagging  Naming Your Image Properly**
  * **Docker Hub  Pushing & Pulling Images**
  * **Creating Images from Running Containers  docker commit**
  * **Backup & Offline Storage  docker save & docker load**
    * **Restricted environments:** Production servers that can't access Docker Hub (security policy)
    * **Air-gapped systems:** Banks, military, government — no internet at all
    * **Backup strategy:** Store images in S3 before major deployments
    * **Transfer to offline machines:** Move images without a registry
  * **Troubleshooting Containers  The Three Commands**
  * **Cleanup Operations**
  * **Tech Stack Mapping**
  * **Visual Diagrams**
  * **Code & Practical Examples**

### Key Commands / Code Example:

```dockerfile
# Common base images
FROM ubuntu:22.04        # Full Ubuntu OS
FROM debian:12-slim      # Minimal Debian (smaller)
FROM alpine:3.18         # Tiny Linux (~5MB) — smallest common base
FROM python:3.11-slim    # Python with slim Debian
FROM node:22-alpine      # Node.js on Alpine
FROM openjdk:21-slim     # Java 21
FROM nginx:latest        # NGINX web server
FROM scratch             # Literally nothing (for static binaries)
```

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## 36. Docker Day 4: Image Optimization, Multi-Stage Builds, Container Registries & Docker vs Kubernetes

🔗 **Full Lesson:** [36_Image_Optimization_Multi_Stage_Builds_Container_Registries_and_Docker_vs_Kubernetes.md](./36_Image_Optimization_Multi_Stage_Builds_Container_Registries_and_Docker_vs_Kubernetes.md)

* **What**: Docker image optimization is the practice of making your Docker images as **small, fast, and secure** as possible — without sacrificing functionality. An optimized image contains only what's absolutely necessary to run the application.
* **Why It Exists**: Solves deployment speed, consistency, and reliability challenges of Docker Day 4: Image Optimization, Multi-Stage Builds, Container Registries & Docker vs Kubernetes in production.
* **Key Concepts**:
  * **Why Docker Image Optimization Matters**
  * **Base Image Selection  The First Big Decision**
    * **When to use:** Never in production — only as build stages
    * **When to use:** Production runtime when you need some system libraries
    * **Tradeoff:** Some packages that need compilation might fail
    * **When to use:** Production when compatibility is verified
  * **Dockerfile Best Practices for Smaller Images**
  * **Multi-Stage Dockerfiles  The Gold Standard**
    * Include build tools → **large, insecure production image**
    * Don't include build tools → **can't compile your application**
    * **Build Stage:** Has all tools needed to compile/build (large, temporary)
    * **Runtime Stage:** Has only what's needed to run (small, production-ready)
  * **Container Registries  Beyond Docker Hub**
  * **Pushing to Google Container Registry (GCR)**
  * **Pushing to AWS ECR**
  * **Pushing to Azure Container Registry (ACR)**
  * **Docker Compose vs Kubernetes  When to Use What**
  * **Tech Stack Mapping**
  * **Visual Diagrams**
  * **Code & Practical Examples**

### Key Commands / Code Example:

```
Bloated Image:
  Base: Ubuntu (~1.14 GB) + Python manually installed
  Total: ~1.2 GB+

Optimized Image:
  Base: python:3.11-slim (~188 MB)
  Total: ~200–250 MB

Savings: ~1 GB per image
         × 50 deployments/day
         × 10 microservices
         = Significant storage and bandwidth savings
```

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## 37. Kubernetes: Introduction, Architecture, Clusters, Namespaces & kubectl

🔗 **Full Lesson:** [37_Kubernetes_Introduction_Architecture_Clusters_Namespaces_and_kubectl.md](./37_Kubernetes_Introduction_Architecture_Clusters_Namespaces_and_kubectl.md)

* **What**: Kubernetes (also written as **K8s** — because there are 8 letters between K and s) is an **open-source container orchestration platform** originally developed by Google, now maintained by CNCF (Cloud Native Computing Foundation).
* **Why It Exists**: Solves deployment speed, consistency, and reliability challenges of Kubernetes: Introduction, Architecture, Clusters, Namespaces & kubectl in production.
* **Key Concepts**:
  * **What is Kubernetes?**
    * Docker lets you **run** containers. But what if you have 100 containers across 10 servers?
    * You need something to **manage**, **restart on failure**, **scale**, and **distribute traffic** automatically.
    * Kubernetes is exactly that — a **manager / conductor** for your containers.
    * Kubernetes continuously **watches** the actual state and **reconciles** it with the desired state
  * **Core Definitions**
    * **What:** A **VM (Virtual Machine)** with software/applications installed. In Kubernetes, it has Docker (or another container runtime) installed.
    * **Types:**
    * **Master Node** — brain of the cluster, manages everything
    * **Worker Node** — does the actual work, runs your application containers
  * **Kubernetes Architecture**
  * **Kubernetes Features**
    * **What:** K8s automatically detects and fixes failed pods/containers.
    * **How:** The Controller Manager constantly checks if the actual pod count = desired count. If a pod dies → it creates a new one.
    * **Impact:** Zero manual intervention for minor failures.
    * **What:** Automatically increases/decreases the number of pods based on CPU/memory usage or traffic.
  * **Cluster Creation on GCP**
    * Platform: **Google Cloud Platform (GCP)** — Google Kubernetes Engine (GKE)
    * Cluster: **3 nodes** (1 per zone for high availability)
    * Node config: **30GB disk, 2 vCPUs, 4GB RAM** per node
    * Connection: **Cloud Shell** + `kubectl`
  * **Namespaces**
    * Isolate **dev / staging / production** in one cluster
    * Control **resource quotas** per team
    * Apply **RBAC** (Role-Based Access Control) per namespace
  * **kubectl Commands**
  * **kubectl create vs kubectl apply**
    * **`create`** = "Make this for the first time"
    * **`apply`** = "Make this happen — create if missing, update if existing"
  * **YAML in Kubernetes**
  * **Tech Stack Mapping**
  * **Practical / Code Examples**

### Key Commands / Code Example:

```
+------------------+       +------------------+       +------------------+
|   Worker Node 1  |       |   Worker Node 2  |       |   Worker Node 3  |
|  [Pod] [Pod]     |       |  [Pod] [Pod]     |       |  [Pod] [Pod]     |
|  Docker Runtime  |       |  Docker Runtime  |       |  Docker Runtime  |
|  Kubelet Agent   |       |  Kubelet Agent   |       |  Kubelet Agent   |
+------------------+       +------------------+       +------------------+
         |                          |                          |
         +------------+-------------+-------------------------+
                      |
             +--------+--------+
             |   Master Node   |
             |  (Control Plane)|
             +-----------------+
```

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## 38. Kubernetes Day 2: Pods, Deployments, Services, ReplicaSets, StatefulSets & Persistent Volumes

🔗 **Full Lesson:** [38_Pods_Deployments_Services_ReplicaSets_StatefulSets_and_Persistent_Volumes.md](./38_Pods_Deployments_Services_ReplicaSets_StatefulSets_and_Persistent_Volumes.md)

* **What**: Kubernetes has a two-tier architecture: a **Control Plane** (master node) that makes all decisions, and **Worker Nodes** that do all the actual work. Every single piece of communication inside the cluster flows through the **API Server** — it is the central hub for everything.
* **Why It Exists**: Kubernetes doesn't schedule individual containers directly — it schedules Pods. This abstraction allows:
- Grouping tightly related containers (e.g., an app + a logging sidecar) as one unit
- Giving them a single shared IP (they talk via `localhost`)
- Managing them as one atomic unit for scheduling and scaling
* **Key Concepts**:
  * **Kubernetes Architecture  Deep Dive**
    * **What:** The ONLY entry point into the cluster — all requests (from kubectl, other components, CI/CD tools) go through it
    * **What it does:** Authenticates requests, validates them, stores results in etcd, notifies other components
    * **Think of it as:** The reception desk of a hotel — every guest, every staff member, every delivery goes through reception
    * **What:** A distributed key-value database — the cluster's single source of truth
  * **Pods  The Smallest Unit**
  * **Services  Stable Communication Between Pods**
    * **What:** Internal IP only — pods within the cluster can reach it, nothing outside
    * **Use case:** Backend services, databases — things that should NOT be internet-facing
    * **DNS name:** `service-name.namespace.svc.cluster.local`
    * **What:** Exposes the service on a specific port on EVERY node's external IP
  * **Deployments  Managing Pod Lifecycle**
  * **ReplicaSets  Guaranteeing Pod Count**
  * **StatefulSets  Pods with Unique Identities**
  * **Persistent Volumes & Claims (PV/PVC)**
    * **Persistent Volume (PV):** A piece of actual storage (disk, NFS, cloud storage) provisioned in the cluster
    * **Persistent Volume Claim (PVC):** A request by a pod to USE a certain amount of that storage
  * **Auto-Healing in Practice**
  * **Exposing Applications  kubectl expose**
  * **Essential kubectl Commands**
  * **Tech Stack Mapping**
  * **Visual Diagrams**
  * **Code & Practical Examples**

### Key Commands / Code Example:

```
kubectl run nginx --image=nginx

1. kubectl → reads kubeconfig → finds API server address
2. kubectl → HTTPS request → API Server (with auth token)
3. API Server → authenticates, authorizes
4. API Server → writes pod spec to etcd: "pending pod: nginx"
5. Scheduler → sees unscheduled pod in etcd
6. Scheduler → evaluates nodes → picks Node-2 (most available)
7. Scheduler → writes to etcd: "assign nginx to Node-2"
8. Kubelet on Node-2 → sees the assignment
9. Kubelet → tells container runtime: "start nginx container"
10. Container runtime → pulls nginx image → starts container
11. Kubelet → reports to API Server: "Pod running on Node-2"
12. API Server → updates etcd: "nginx pod: Running on Node-2"
13. kubectl → shows: pod/nginx created ✅
```

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## 39. Kubernetes Microservices Deployment: Monolithic vs Microservices, GKE & Real-World E-Commerce App

🔗 **Full Lesson:** [39_Kubernetes_Microservices_Deployment_Monolithic_vs_Microservices_GKE_and_Real_World_E_Commerce_App.md](./39_Kubernetes_Microservices_Deployment_Monolithic_vs_Microservices_GKE_and_Real_World_E_Commerce_App.md)

* **What**: Introduction and foundational concepts of Kubernetes Microservices Deployment: Monolithic vs Microservices, GKE & Real-World E-Commerce App.
* **Why It Exists**: Solves deployment speed, consistency, and reliability challenges of Kubernetes Microservices Deployment: Monolithic vs Microservices, GKE & Real-World E-Commerce App in production.
* **Key Concepts**:
  * **Monolithic vs Microservices Architecture**
  * **The Online Boutique  Real Microservices Application**
  * **How Microservices Connect in Kubernetes**
  * **GKE Cluster Setup for Microservices**
  * **Deploying the Full Application  Single Command**
  * **Understanding the Kubernetes Manifest File**
    * Deleting a pod in a Deployment = **auto-healing kicks in immediately**
    * A deployment with **multiple replicas** (e.g., 2) means zero downtime even during pod replacement
  * **Idempotent Deployments  Why kubectl apply is Safe**
  * **Running Jenkins on Kubernetes**
  * **Resume Writing  How to Frame This Experience**
  * **Tech Stack Mapping**
  * **Visual Diagrams**
  * **Code & Practical Examples**

### Key Commands / Code Example:

```
Startup stage: Monolith is FINE
  - Small team (5-10 devs)
  - Simple app, fast to build
  - One deployment = everything ships

Scale stage: Monolith becomes a NIGHTMARE
  - 200 developers all editing the same codebase
  - One feature change requires testing/redeploying everything
  - Checkout feature scales → entire app must scale (wasteful)
  - Bug in recommendations crashes payment service too
  - Different features need different tech stacks (Java vs Python vs Go)
  - Deploy: 4+ hours, high risk, all-hands event
```

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## 40. Kubernetes Advanced: Horizontal Pod Autoscaling (HPA) & Troubleshooting

🔗 **Full Lesson:** [40_Kubernetes_Advanced_Horizontal_Pod_Autoscaling_and_Troubleshooting.md](./40_Kubernetes_Advanced_Horizontal_Pod_Autoscaling_and_Troubleshooting.md)

* **What**: "Horizontal" means adding MORE pods (scaling out) — not making existing pods bigger (that's Vertical Pod Autoscaling, VPA).
* **Why It Exists**: Without HPA:
- You manually decide how many pods to run: `kubectl scale deployment/nginx --replicas=5`
- Too few pods → app is slow or crashes under load
- Too many pods → wasting money on idle servers
- Midnight traffic spike → nobody is awake to scale up
* **Key Concepts**:
  * **Horizontal Pod Autoscaling (HPA)**
  * **Metrics Server  The Brain Behind HPA**
  * **Setting Up HPA  Complete Walkthrough**
  * **Load Testing HPA with BusyBox**
  * **HPA Scaling Behavior  Up & Down**
  * **Kubernetes Troubleshooting  The 3-Step Rule**
  * **The 10 Common Issues & Their Fixes**
    * `<none>` = Service selector labels don't match any pod labels → **label mismatch**
  * **The 5 Commands Every DevOps Engineer Must Know**
  * **RBAC  Role-Based Access Control Basics**
  * **Tech Stack Mapping**
  * **Visual Diagrams**
  * **Code & Practical Examples**

### Key Commands / Code Example:

```
Desired Replicas = ceil(Current Replicas × (Current Metric / Target Metric))

Example:
  Current: 2 pods, each at 90% CPU
  Target:  50% CPU per pod
  
  Desired = ceil(2 × (90 / 50)) = ceil(3.6) = 4 pods

Kubernetes will scale from 2 → 4 pods to bring CPU back to ~50%
```

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## 41. Kubernetes Monitoring: Prometheus, Grafana & Helm

🔗 **Full Lesson:** [41_Kubernetes_Monitoring_Prometheus_Grafana_and_Helm.md](./41_Kubernetes_Monitoring_Prometheus_Grafana_and_Helm.md)

* **What**: Monitoring is the practice of **continuously collecting, storing, and analyzing metrics** from your infrastructure and applications to understand their health, performance, and behavior in real time.
* **Why It Exists**: Solves deployment speed, consistency, and reliability challenges of Kubernetes Monitoring: Prometheus, Grafana & Helm in production.
* **Key Concepts**:
  * **Why Monitoring is Non-Negotiable**
  * **The Monitoring Tools Landscape**
    * **Market share:** Used by ~90% of companies running Kubernetes
    * **Prometheus:** Open-source metrics collection and storage (time-series database)
    * **Grafana:** Open-source visualization and dashboarding
    * **Why it dominates:** Native Kubernetes integration, free/open-source, massive community, scales well, PromQL is powerful
  * **Helm  The Kubernetes Package Manager**
    * Maintained by **CNCF** (Cloud Native Computing Foundation)
    * Major contributors: **Microsoft**, **Google**, **Bitnami**
  * **Prometheus  The Metrics Database**
  * **Grafana  The Visualization Layer**
  * **Node Exporter & Kube State Metrics**
  * **The Full Monitoring Architecture**
  * **Step-by-Step Setup on GKE**
  * **PromQL  Querying Prometheus**
  * **Grafana Dashboards & Alerts**
  * **Tech Stack Mapping**
  * **Visual Diagrams**
  * **Code & Practical Examples**

### Key Commands / Code Example:

```
Infrastructure Level:
  - CPU usage per node and pod
  - Memory consumption
  - Disk I/O and available space
  - Network throughput
  
Application Level:
  - Request latency (how slow is the API?)
  - Error rate (how many 5xx responses?)
  - Throughput (requests per second)
  - Pod restart count (is something crashing?)
  
Business Level:
  - Transaction success rate
  - Active users
  - Feature-specific metrics
```

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## 42. Grafana Deep Dive: Dashboards, Alerting, User Management & Real-World Monitoring

🔗 **Full Lesson:** [42_Grafana_Deep_Dive_Dashboards_Alerting_User_Management_and_Real_World_Monitoring.md](./42_Grafana_Deep_Dive_Dashboards_Alerting_User_Management_and_Real_World_Monitoring.md)

* **What**: Running monitoring tools (Prometheus, Grafana, AlertManager) in a **dedicated `monitoring` namespace** — completely separate from your application namespaces (`production`, `staging`, `development`).
* **Why It Exists**: ```
Without namespace isolation:
  monitoring + apps share the same namespace
  
  Scenario: Monitoring consumes all node CPU
  → Application pods get throttled
  → Users experience slowness
  → Monitoring caused the problem it was meant to prevent ❌
* **Key Concepts**:
  * **Namespace Isolation for Monitoring**
  * **Grafana Configuration & User Management**
  * **Data Sources  Connecting Grafana to Everything**
  * **Scrape Interval & Timeout Settings**
    * **Scrape Interval:** How often Prometheus collects metrics from targets
    * **Timeout:** How long Prometheus waits for a target to respond before marking the scrape as failed
  * **Dashboard Management  25,000+ Dashboards**
  * **The 5 Core Dashboard Types DevOps Must Know**
  * **Troubleshooting  When Data Shows "NA"**
  * **Grafana Alerting  Complete Setup**
  * **Silence Periods  Suppressing Alerts During Maintenance**
  * **Real-World Applications of Grafana**
  * **DevOps Role in Monitoring vs L1/L2 Teams**
  * **Tech Stack Mapping**
  * **Visual Diagrams**
  * **Code & Practical Examples**

### Key Commands / Code Example:

```
Without namespace isolation:
  monitoring + apps share the same namespace
  
  Scenario: Monitoring consumes all node CPU
  → Application pods get throttled
  → Users experience slowness
  → Monitoring caused the problem it was meant to prevent ❌

  Scenario: Someone accidentally deletes namespace
  → Both monitoring AND apps disappear together ❌

With namespace isolation (monitoring namespace):
  Monitoring namespace: prometheus, grafana, alertmanager
  Production namespace: your-api, your-frontend, your-db
  
  Monitoring pod issue → Apps unaffected ✅
  App pod issue → Monitoring unaffected ✅
  ResourceQuota per namespace → monitoring can't starve apps ✅
```

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## 43. Terraform & Infrastructure as Code (IaC)

🔗 **Full Lesson:** [43_Terraform_and_Infrastructure_as_Code.md](./43_Terraform_and_Infrastructure_as_Code.md)

* **What**: IaC means writing **code to define, provision, and manage infrastructure** — instead of clicking through dashboards or running manual commands. Think of it as a blueprint for your servers, networks, databases, and cloud resources — stored as text files.
* **Why It Exists**: Solves deployment speed, consistency, and reliability challenges of Terraform & Infrastructure as Code (IaC) in production.
* **Key Concepts**:
  * **What is Infrastructure as Code (IaC)?**
    * **40% of deployment errors** come from manual activities — IaC eliminates most of them
  * **What is Terraform?**
    * It maintains a **state file** so it knows what exists and what needs to change
    * Supports **immutable infrastructure** — instead of patching, it destroys and recreates
  * **Terraform vs Ansible**
    * **Terraform** is great at talking to cloud APIs to create resources
    * **Ansible** is great at SSH-ing into servers and configuring them after creation
    * **Using both together:** Fully automated pipeline from raw cloud to configured server
    * **Terraform alone:** Infrastructure is created but not configured
  * **Terraform Workflow & Commands**
    * **What:** Downloads and installs the required **provider plugins** (e.g., AWS provider)
    * **When:** Run once after writing your first `.tf` file or when adding a new provider
    * **Creates:** `.terraform/` directory with downloaded plugins
    * **What:** Previews changes — shows what will be **created, modified, or destroyed**
  * **HCL  HashiCorp Configuration Language**
    * **Human-friendly** — readable like English sentences
    * **Machine-friendly** — parseable by tools and automations
  * **Hands-On Lab Walkthrough**
    * **Issue:** T2 micro instance type not eligible for free tier in some regions
    * **Fix:** Switched to `t3.micro` which is free-tier eligible
    * **Lesson:** Always check the instance type eligibility for your AWS account type
  * **Visual Diagrams**
  * **Tech Stack Mapping**
  * **Code / Practical Examples**
  * **Additional Notes**
    * **Terraform Certification:** HashiCorp offers official Terraform Associate certification ($70, sometimes $20–30 during sales)
    * **Free Tier Tip:** Always use `t3.micro` (not T2) for free-tier eligibility in newer AWS accounts
    * **State File Security:** Never commit `terraform.tfstate` to GitHub — it contains sensitive data (IPs, credentials references). Use `.gitignore`
    * **Cost Discipline:** Always run `terraform destroy` after labs to avoid surprise AWS bills

### Key Commands / Code Example:

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

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## 44. Terraform Day 2: IaC Commands, Code Structure & AWS Workflow

🔗 **Full Lesson:** [44_Terraform_Advanced_Commands_State_Management_MultiResource_Provisioning_and_PR_Workflow.md](./44_Terraform_Advanced_Commands_State_Management_MultiResource_Provisioning_and_PR_Workflow.md)

* **What**: Introduction and foundational concepts of Terraform Day 2: IaC Commands, Code Structure & AWS Workflow.
* **Why It Exists**: Solves deployment speed, consistency, and reliability challenges of Terraform Day 2: IaC Commands, Code Structure & AWS Workflow in production.
* **Key Concepts**:
  * **Terraform vs Ansible  What's the Difference?**
    * You need **two different tools** for two different jobs:
    * **Terraform** = *Build the house* (spin up EC2, VPC, RDS)
    * **Ansible** = *Furnish the house* (install Nginx, copy config files, set up users)
  * **Terraform Code Structure**
    * Keeps code **modular** and **readable**
  * **Terraform CLI Commands**
    * **What:** Downloads provider plugins (e.g., AWS plugin)
    * **When:** Always run first, or when you add a new provider
    * **Creates:** `.terraform/` folder with downloaded plugins
    * **What:** Checks if your `.tf` files have correct syntax
  * **State File  The Brain of Terraform**
  * **Hands-On: EC2, IAM, S3 via Terraform**
  * **PR Workflow with Terraform**
  * **What Terraform Does NOT Do**
    * Terraform can **create** an Auto Scaling Group (ASG), but it does **not handle** the actual scaling logic
  * **Visual Diagrams**
  * **Tech Stack Mapping**
  * **Code / Practical Examples**

### Key Commands / Code Example:

```
project/
├── main.tf        ← Resources to create (EC2, S3, IAM, etc.)
├── provider.tf    ← Which cloud provider + region
└── variable.tf    ← Variables (reusable values)
```

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## 45. Deploying 3-Tier Architecture on AWS using Terraform (IaC)

🔗 **Full Lesson:** [45_Deploying_3_Tier_Architecture_on_AWS_using_Terraform.md](./45_Deploying_3_Tier_Architecture_on_AWS_using_Terraform.md)

* **What**: A **3-Tier Architecture** is a way to design and deploy software applications by splitting them into **three separate layers**, each with a distinct responsibility:
* **Why It Exists**: Solves deployment speed, consistency, and reliability challenges of Deploying 3-Tier Architecture on AWS using Terraform (IaC) in production.
* **Key Concepts**:
  * **What is a 3-Tier Architecture?**
    * **Separation of Concerns** – Each layer does one job. If the frontend breaks, the database is safe.
    * **Scalability** – You can scale each tier independently. If your API gets 10x traffic, scale only Tier 2.
    * **Security** – The database tier is never directly exposed to the internet. It only talks to the app layer.
    * **Maintainability** – Teams can work on each layer without stepping on each other.
  * **Monolithic vs Microservice Architecture**
    * **Don't use Microservices** for a small startup — it's overkill and adds DevOps overhead.
    * **Do use Microservices** when teams grow, traffic is high, and different components need different scaling.
  * **What is Terraform (IaC)?**
    * **Reproducibility** – Run the same code in Dev, Staging, and Production environments and get identical infrastructure.
    * **Version Control** – Infrastructure changes are tracked in Git just like application code.
    * **Speed** – Provision 40+ AWS resources with a single command instead of clicking for hours.
    * **Disaster Recovery** – If infrastructure is destroyed, `terraform apply` rebuilds everything in minutes.
  * **Terraform Core Workflow**
  * **Terraform File Structure**
    * Keeps secrets and environment-specific values **out of the main code**.
  * **Errors Fixed During Session**
  * **Visual Diagrams**
    * **Monolith** – Single deployable unit. All features in one codebase. Simple to start, hard to scale. Best for small teams and early-stage products.
    * **Microservices** – Many independent services, each owning its domain and database. Complex to set up, but scales excellently and allows independent deployments. Best for large teams and high-traffic systems.
  * **Tech Stack Mapping**
  * **Code / Practical Examples**

### Key Commands / Code Example:

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

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## 46. Ansible: Configuration Management & Automation

🔗 **Full Lesson:** [46_Ansible_Configuration_Management_and_Automation.md](./46_Ansible_Configuration_Management_and_Automation.md)

* **What**: Introduction and foundational concepts of Ansible: Configuration Management & Automation.
* **Why It Exists**: Without Ansible (manual world):
- You SSH into each server one by one. - You run the same commands on 50 servers — manually, error-prone, time-consuming.
* **Key Concepts**:
  * **What is Ansible?**
    * Write a **Playbook** once.
  * **Ansible vs Other Config Management Tools**
  * **Ansible Architecture Components**
  * **How Ansible Works  Agentless + SSH**
  * **Ansible Playbooks & YAML**
    * Uses **indentation** (spaces, never tabs) to define structure
  * **Hands-On Lab  9 Steps Walkthrough**
    * **1 VM** = Ansible Master (Ubuntu)
    * **3 Docker containers** = Target 1, Target 2 (Ubuntu containers with SSH)
  * **Visual Diagrams**
    * **Ansible Master** — The control node where Ansible is installed. Contains playbooks, inventory, and SSH keys.
    * **Target Machines (Managed Nodes)** — Servers that Ansible manages. Need only SSH + Python.
    * **Inventory/Host File** — Lists IP addresses/hostnames of target machines, organized into groups.
    * **Playbook** — YAML file containing ordered tasks to run on targets.
  * **Tech Stack Mapping**
  * **Code / Practical Examples**
  * **Navigation Footer**

### Key Commands / Code Example:

```
AGENT-BASED (Chef / Puppet):
  Master ──────────── Agent (installed on each target) ──── Executes tasks
              Needs: Agent install, certificate management, port open, agent updates

AGENTLESS (Ansible):
  Master ─── SSH ──── Target (just needs SSH + Python)
              Needs: Nothing extra — SSH already exists on every Linux server
```

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## 47. Ansible Playbooks, Roles & Tower

🔗 **Full Lesson:** [47_Ansible_Playbooks_Roles_and_Tower.md](./47_Ansible_Playbooks_Roles_and_Tower.md)

* **What**: Before running any Playbook, you should **verify that Ansible can actually reach all target machines** over SSH. The `ping` module is the simplest way to do this — it's like a health check before surgery.
* **Why It Exists**: Running a full Playbook against unreachable machines wastes time and leaves infrastructure in a **partial/inconsistent state** (some tasks ran, some didn't). A quick `ping` before every Playbook run confirms:
- SSH connectivity is working
- The correct key is being used
- The inventory IPs are reachable
- Python is available on the targets
* **Key Concepts**:
  * **Ansible Connectivity Check & Dry Run**
  * **Ansible Playbook Fundamentals**
    * **Repeatable** — run the same steps every time
    * **Version-controlled** — store in Git, review changes
    * **Self-documenting** — each task has a `name` field that reads like a sentence
    * **Idempotent** — safe to re-run without side effects
  * **YAML Basics for Ansible**
  * **Ansible Roles**
    * Roles are **reusable across projects** (write once, use everywhere)
    * Can be shared publicly on **Ansible Galaxy** (like npm for Ansible)
  * **Ansible Tower (Enterprise)**
  * **Visual Diagrams**
    * **Job Templates** — pre-defined playbook runs with locked inventory and credentials
    * **RBAC (Role-Based Access Control)** — developers get `Execute` permission on deployment templates only; they cannot modify them or see credentials
    * **Credentials stored in Tower vault** — developers trigger jobs without ever seeing SSH keys or AWS secrets
    * **Activity Stream** — full audit log of who ran what and when
  * **Tech Stack Mapping**
  * **Code / Practical Examples**
  * **Navigation Footer**

### Key Commands / Code Example:

```bash
# Ping all hosts in inventory
ansible all -m ping

# Ping only the 'webservers' group
ansible webservers -m ping

# Ping a single specific host
ansible 192.168.1.10 -m ping
```

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## 48. Python for DevOps Automation

🔗 **Full Lesson:** [48_Python_for_DevOps_Automation.md](./48_Python_for_DevOps_Automation.md)

* **What**: Python is a **high-level, human-readable, interpreted programming language**. "High-level" means it's written closer to how humans speak, not how machines think.
* **Why It Exists**: As a DevOps engineer, you don't write applications — you **automate infrastructure tasks**. Python is the go-to tool for this because:
* **Key Concepts**:
  * **Why Python for DevOps?**
  * **Python Basics for DevOps Engineers**
    * **Python 3.14** is the latest (as of 2026). Always use Python 3.x.
    * **Python 2 is dead** — officially ended support in 2020. Never use it for new work.
  * **Python Modules & Dependency Management**
  * **Scripting vs Programming**
    * Write a script to check if all EC2 instances are tagged correctly → **Scripting**
    * Build a web dashboard to visualize cloud costs → **Programming** (usually done by devs)
  * **Boto3  Python SDK for AWS**
    * **Automation** – Create/delete resources programmatically without clicking the Console.
    * **Integration** – Use AWS in CI/CD pipelines, scheduled scripts, and automation tools.
    * **Scalability** – Loop through 1000 IAM users or S3 objects in seconds.
    * **Consistency** – Same script runs identically every time.
  * **Hands-On Projects Walkthrough**
    * **Create** an IAM user
    * **List** all IAM users
    * **Update** (rename) a user
    * **Delete** a user
  * **Visual Diagrams**
    * `boto3.client()` is a **low-level** interface that maps directly to AWS API calls. It returns raw JSON-like dictionaries and gives you maximum control. Used for services with complex APIs like IAM and Cost Explorer.
    * `boto3.resource()` is a **high-level**, object-oriented interface. It returns Python objects with methods like `.upload_file()` and `.delete()`. Simpler to use for S3 and EC2 operations.
  * **Tech Stack Mapping**
  * **Code / Practical Examples**
  * **Navigation Footer**

### Key Commands / Code Example:

```
You write script.py
        │
        ▼
Python Interpreter reads line 1 → executes it immediately
        │
        ▼
Reads line 2 → executes it
        │
        ▼
... continues until end or hits an error
```

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## 49. Shell Scripting with Linux (Bash)

🔗 **Full Lesson:** [49_Shell_Scripting_with_Linux.md](./49_Shell_Scripting_with_Linux.md)

* **What**: The **shell architecture** describes how a user's commands travel through layers to eventually reach the hardware.
* **Why It Exists**: Without the shell, you'd need to write machine code (binary / assembly) to talk to the kernel. The shell gives you a human-readable way to control the entire operating system.
* **Key Concepts**:
  * **Shell Architecture**
  * **Types of Shells**
  * **What is a Shell Script?**
    * **Automation** — Replace repetitive manual commands with a single script run
    * **Consistency** — Same script produces same result every time (no human error)
    * **Speed** — 50 commands run in seconds instead of minutes of manual typing
    * **Scheduling** — Scripts can be scheduled (cron) to run without any human presence
  * **Shebang (`#!/bin/bash`)**
    * Without a shebang, the OS uses the **current user's default shell** — which may not be Bash
    * The shebang guarantees your script **always runs with Bash**, regardless of environment
  * **File Permissions & `chmod`**
  * **Variables & Command Substitution**
    * Use **double quotes** `"$name"` to preserve spaces in values
  * **Operators  AND (`&&`) and OR (`||`)**
  * **Functions in Bash**
  * **Loops & Sleep**
  * **Arithmetic in Bash**
  * **Cron vs Sleep**
  * **If-Else Conditions**
  * **Practical Scripts from Session**
  * **Visual Diagrams**
  * **Tech Stack Mapping**
  * **Code / Practical Examples**
  * **Navigation Footer**

### Key Commands / Code Example:

```
1. You type:  ls -l
2. Terminal sends the input to the Shell (Bash)
3. Shell parses "ls" → finds it at /bin/ls
4. Shell makes a system call to the Kernel: "run /bin/ls with flag -l"
5. Kernel tells hardware to read the directory from disk
6. Disk sends data back to Kernel → Kernel to Shell → Shell prints to Terminal
7. You see the file listing
```

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## 50. Prompt Engineering for DevOps & AI

🔗 **Full Lesson:** [50_Prompt_Engineering_for_DevOps_and_AI.md](./50_Prompt_Engineering_for_DevOps_and_AI.md)

* **What**: Most people think "AI = ChatGPT." That's like saying "the internet = Google." ChatGPT is just one **visible product** built on top of AI. The actual AI landscape is much broader.
* **Why It Exists**: As a DevOps engineer, you'll interact with AI at multiple levels:
- **Generative AI** — Write IaC, shell scripts, pipelines using Copilot / ChatGPT
- **Agentic AI** — Automate multi-step DevOps workflows
- **AI in cloud** — AWS Bedrock, GCP Vertex AI, Azure OpenAI for custom automation
* **Key Concepts**:
  * **The AI Landscape  More Than Just ChatGPT**
    * **Generative AI** — Write IaC, shell scripts, pipelines using Copilot / ChatGPT
    * **Agentic AI** — Automate multi-step DevOps workflows
    * **AI in cloud** — AWS Bedrock, GCP Vertex AI, Azure OpenAI for custom automation
  * **What is Prompt Engineering?**
  * **The CRAFT Model**
  * **Key Prompt Engineering Principles**
  * **Types of AI Explained**
  * **Agentic AI vs AI Agent**
  * **Tools Setup  VS Code + GitHub Copilot**
  * **Visual Diagrams**
    * **C:** "I'm running a Python 3.12 script on Ubuntu 22.04. Error: `ModuleNotFoundError: No module named 'boto3'`. I installed it with `pip install boto3`."
    * **R:** "You are a senior Python DevOps engineer."
    * **A:** "Diagnose why the error persists despite installation and give me the exact commands to fix it."
    * **F:** "Step-by-step numbered list."
  * **Tech Stack Mapping**
  * **Code / Practical Examples**
  * **Project Context**
  * **Code Style Rules**
  * **AWS Patterns**
  * **GCP Patterns**
  * **Security**
  * **Navigation Footer**

### Key Commands / Code Example:

```
AI (Artificial Intelligence)
    │
    ├── Machine Learning (ML)
    │       └── Deep Learning
    │               └── Neural Networks
    │
    ├── Computer Vision (image recognition)
    ├── Natural Language Processing (NLP)
    ├── Robotics
    │
    └── Generative AI  ← This is what ChatGPT, Claude, Gemini are
            └── Large Language Models (LLMs)
```

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## 51. Multi-Cloud ATS App (AWS and GCP) & Kubernetes Concepts

🔗 **Full Lesson:** [51_Multi_Cloud_ATS_App_AWS_and_GCP_and_Kubernetes_Concepts.md](./51_Multi_Cloud_ATS_App_AWS_and_GCP_and_Kubernetes_Concepts.md)

* **What**: An **ATS (Application Tracking System)** is software companies use to screen resumes. This project builds an **AI-powered ATS** that:
- Takes a Job Description (JD) and a resume (PDF) as input
- Uses **Google Gemini AI** to analyze how well the resume matches the JD
- Returns a **match percentage** and **feedback** for the candidate
* **Why It Exists**: Solves deployment speed, consistency, and reliability challenges of Multi-Cloud ATS App (AWS + GCP) & Kubernetes Concepts in production.
* **Key Concepts**:
  * **Project Overview  ATS Application**
    * Uses **Google Gemini AI** to analyze how well the resume matches the JD
    * Returns a **match percentage** and **feedback** for the candidate
  * **Architecture Explained**
    * **AWS** hosts and runs the application
    * **GCP** provides the AI brain (Gemini) via API call
    * **AWS EC2** is reliable, familiar, and cost-effective for running web apps
    * **GCP Gemini** is Google's most capable LLM — better at document analysis and structured feedback than most alternatives
  * **Step-by-Step Implementation**
  * **App Functionality**
  * **Kubernetes  Liveness Probe**
  * **Kubernetes  Readiness Probe**
  * **Liveness vs Readiness  Side-by-Side**
  * **Kubernetes  Affinity & Anti-Affinity**
    * **Affinity:** "I want to be NEAR this" (run on the same node or same zone as something)
    * **Anti-Affinity:** "I want to be FAR from this" (run on different nodes from something)
    * A web app and its Redis cache should be on the **same node** for low latency (avoid network hops)
    * All pods of a microservice should run in the **same availability zone** as its database
  * **Kubernetes  Taints & Tolerations**
    * **Taint** = A mark placed on a **node** that says "no ordinary pods allowed here"
    * **Toleration** = A permission placed on a **pod** that says "I'm allowed on tainted nodes"
    * **GPU nodes** — Only AI/ML workloads should run here (GPU is expensive)
    * **High-memory nodes** — Only memory-intensive databases
  * **Kubernetes  Ingress**
  * **Kubernetes  Network Policy**
    * The **frontend** should talk to the **backend API**
    * The **backend API** should talk to the **database**
    * The **frontend should NOT** talk directly to the **database**
    * **Ingress** (incoming traffic to a pod)
  * **Visual Diagrams**
  * **Tech Stack Mapping**
  * **Code / Practical Examples**
  * **Navigation Footer**

### Key Commands / Code Example:

```
User (Browser)
      │
      │ HTTP :8501
      ▼
AWS EC2 (Ubuntu T2 Large)
      │  Python + Streamlit app
      │  uploads JD + Resume PDF
      │
      │  API call (HTTPS)
      ▼
GCP Gemini API
      │  Processes: JD + Resume text
      │  Returns: match % + feedback
      ▼
AWS EC2 displays result
      │
      ▼
User sees AI screening output
```

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## 52. Multi-Cloud Comparison (AWS vs GCP vs Azure) & Azure DevOps

🔗 **Full Lesson:** [52_Multi_Cloud_Comparison_AWS_vs_GCP_vs_Azure_and_Azure_DevOps.md](./52_Multi_Cloud_Comparison_AWS_vs_GCP_vs_Azure_and_Azure_DevOps.md)

* **What**: Introduction and foundational concepts of Multi-Cloud Comparison (AWS vs GCP vs Azure) & Azure DevOps.
* **Why It Exists**: Solves deployment speed, consistency, and reliability challenges of Multi-Cloud Comparison (AWS vs GCP vs Azure) & Azure DevOps in production.
* **Key Concepts**:
  * **Why Multi-Cloud?**
    * **No vendor lock-in** — You're not dependent on one company's pricing, uptime, or product decisions
    * **Best of breed** — Use GCP for AI/ML (Vertex AI, Gemini), AWS for compute scale, Azure for enterprise (Active Directory integration)
    * **Compliance** — Some regulations require data in specific regions where only one provider has presence
    * **Cost optimization** — Run workloads where pricing is most competitive
  * **Multi-Cloud Services Comparison  Full Map**
  * **Service Deep-Dives**
    * This is where Azure shines — Entra ID is used by **millions of enterprises worldwide** for SSO and identity federation
    * **Layer 7 (HTTP/HTTPS):** Understands web traffic. Can route based on URL path (`/api` → one service), hostnames, headers. Used for web apps.
    * **Layer 4 (TCP/UDP):** Handles raw network traffic. Faster, lower latency. Used for databases, game servers, anything non-HTTP.
  * **Azure Hierarchy  Landing Zone**
  * **Azure DevOps Components**
    * **Build Pipeline** — compiles code, runs tests, creates artifacts
    * **Release Pipeline** — deploys artifacts to environments
  * **Self-Hosted vs Microsoft-Hosted Agents**
    * **Costs money** — Microsoft-hosted agents have free minutes (1,800 min/month free) but charge after that (~$0.008/minute)
    * **Free** — no per-minute charges, you already own the machine
  * **Azure Web App (PaaS)**
  * **Full CI/CD Flow  Azure DevOps + Node.js**
  * **Visual Diagrams**
  * **Tech Stack Mapping**
  * **Code / Practical Examples**
  * **Navigation Footer**

### Key Commands / Code Example:

```
Azure Portal → Virtual Machines → Create
→ Select: Region, Image (Ubuntu 22.04), Size (B2s)
→ Authentication: SSH key or password
→ Networking: VNet, Subnet, NSG (open ports)
→ Review + Create → VM ready in ~2 minutes
```

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## 53. Splunk (Log Analytics) & Docker Compose

🔗 **Full Lesson:** [53_Splunk_Log_Analytics_and_Docker_Compose.md](./53_Splunk_Log_Analytics_and_Docker_Compose.md)

* **What**: "Machine-generated data" means logs, metrics, events, and data that computers produce automatically:
- Web server access logs (`nginx.log`, `apache.log`)
- Application error logs (`app.log`, crash reports)
- Security events (failed logins, firewall blocks)
- Infrastructure metrics (CPU %, disk I/O, network traffic)
- Business events (orders placed, payments processed)
* **Why It Exists**: Without Splunk (or a similar tool), logs are:
- Scattered across dozens/hundreds of servers
- In different formats (some JSON, some plain text, some CSV)
- Accessible only by SSH-ing into each server individually
- Not searchable across systems
- Deleted when disk fills up
* **Key Concepts**:
  * **What is Splunk?**
  * **Splunk Architecture**
  * **Splunk Forwarders  Universal vs Heavy**
  * **Splunk Key Ports**
  * **Splunk Core Workflow  Collect  Index  Search  Alert**
    * **Forwarder monitoring** — watch log files, directories
    * **HEC** — apps push events via REST API
    * **Syslog** — network devices on port 514
    * **AWS/GCP/Azure integrations** — pull CloudTrail, VPC Flow Logs, etc.
  * **Splunk Alerts**
  * **Docker vs Docker Compose**
  * **Docker Swarm vs Kubernetes vs OpenShift**
    * **Managed by Red Hat, not cloud providers**
  * **Lab Walkthrough  Splunk on EC2 via Docker Compose**
  * **Visual Diagrams**
  * **Tech Stack Mapping**
  * **Code / Practical Examples**
  * **Navigation Footer**

### Key Commands / Code Example:

```
1. Logs are generated by your applications and infrastructure
2. Splunk Forwarders collect these logs from source machines
3. Logs are sent to the Splunk Indexer (stored + indexed)
4. You search, visualize, and alert on the indexed data
```

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## 54. Kafka on Kubernetes using Strimzi Operator

🔗 **Full Lesson:** [54_Kafka_on_Kubernetes_using_Strimzi_Operator.md](./54_Kafka_on_Kubernetes_using_Strimzi_Operator.md)

* **What**: Apache Kafka is a **distributed event streaming platform** — think of it as a high-speed, fault-tolerant pipe that lets applications send and receive millions (or trillions) of messages in real time.
* **Why It Exists**: Modern applications (e-commerce, ride-hailing, banking) generate massive amounts of data every second. Traditional message queues like RabbitMQ can handle ~50,000 messages/day.
* **Key Concepts**:
  * **What is Apache Kafka?**
  * **Kafka Core Components**
  * **Kafka vs RabbitMQ**
  * **Why Run Kafka on Kubernetes?**
    * **Auto-scaling:** K8s can automatically add/remove Kafka broker pods based on load.
    * **Self-healing:** If a broker pod crashes, K8s restarts it automatically.
    * **Containerization:** Kafka packaged in Docker images — consistent across dev, staging, prod.
    * **High Availability:** Spread pods across nodes/zones for fault tolerance.
  * **What is the Strimzi Operator?**
  * **KRaft Mode (ZooKeeper-less Kafka)**
  * **Architecture Diagram**
  * **Hands-On: Full Deployment Steps**
  * **Tech Stack Mapping**
    * **Broker** – A Kafka server that stores and serves messages.
    * **Topic** – A named stream of messages (like a folder).
    * **Partition** – A topic is split into partitions across brokers for parallelism and scalability.
    * **Producer** – Application that writes messages to a topic.
  * **Quick Reference: Essential Commands**
  * **Navigation Footer**

### Key Commands / Code Example:

```
Cluster
├── Broker 1  (Leader for Partition 0)
├── Broker 2  (Leader for Partition 1)
└── Broker 3  (Replica for Partition 0 & 1)
```

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## 55. Complete CI/CD Pipeline: Jenkins, Docker & AWS (Node.js App)

🔗 **Full Lesson:** [55_Complete_CICD_Pipeline_Jenkins_Docker_and_AWS_NodeJS_App.md](./55_Complete_CICD_Pipeline_Jenkins_Docker_and_AWS_NodeJS_App.md)

* **What**: These are three stages of modern software release automation:
* **Why It Exists**: Without CI/CD, releases are manual, slow, and error-prone. Developers would test locally, zip files, copy to servers, and hope it works.
* **Key Concepts**:
  * **Continuous Integration vs Delivery vs Deployment**
    * **CR = Change Request** — A ticket raised to describe what change is going to production
    * **CAB = Change Advisory Board** — A committee that reviews and approves the CR
    * This is **Continuous Delivery** — automated up to the gate, manual through it
  * **CI/CD Flow Overview**
  * **Declarative vs Scripted Pipelines**
    * **Structured, opinionated syntax** with defined blocks
    * **Full Groovy code** — maximum flexibility
    * **Declarative:** Building, testing, pushing — standard linear pipeline
    * **Scripted:** Complex deployments with conditions (if dev deploy here, if prod deploy there), dynamic container management
  * **Infrastructure Setup on AWS EC2**
  * **Jenkins Installation & Configuration**
  * **Docker Installation & Jenkins Integration**
  * **CI Pipeline  Build & Push Docker Image**
  * **CD Pipeline  Pull & Run Container**
  * **CI/CD Integration  Auto-Trigger CD after CI**
    * **Initial Build Overhead:** The first execution of the build pipeline may take longer to pull base Docker images and install npm packages. Subsequent builds benefit from cached layers and dependencies.
    * **Common Pipeline Failure Points:**
    * **Key Advice:** Practice the setup steps repeatedly and consult the build console output logs to pinpoint issues.
  * **Tech Stack Mapping**
    * Add **automated tests** stage (unit tests with Jest, integration tests) before building Docker image — fail fast
    * Use **semantic versioning** for image tags (`1.2.3`) instead of just `latest` or build number
    * Add **Docker image vulnerability scanning** (Trivy, Snyk) stage
    * Use **AWS ECR** (private) instead of Docker Hub
  * **Quick Reference Cheatsheet**
    * **Monitoring & Observability:** ELK, Prometheus, Grafana
    * **Infrastructure as Code (IaC) & Configuration Management:** Terraform, Ansible
    * **Containerization & Scripting:** Docker, Python, PowerShell
    * **Troubleshooting & Infrastructure Management**
  * **Navigation Footer**

### Key Commands / Code Example:

```
Continuous Delivery:
  Code Push → CI (build/test) → Artifact Ready → ⏸ Human Approval → Deploy to Prod

Continuous Deployment:
  Code Push → CI (build/test) → Artifact Ready → ✅ Auto Deploy to Prod
```

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## 56. DevSecOps: Jenkins, Trivy & SonarQube on AWS

🔗 **Full Lesson:** [56_DevSecOps_Jenkins_Trivy_SonarQube_on_AWS.md](./56_DevSecOps_Jenkins_Trivy_SonarQube_on_AWS.md)

* **What**: Introduction and foundational concepts of DevSecOps: Jenkins + Trivy + SonarQube on AWS.
* **Why It Exists**: Without SonarQube, a developer might write code that has a SQL injection vulnerability or a null pointer bug — and nobody notices until a customer reports it (or worse, a hacker exploits it). SonarQube catches these automatically before the code reaches production.
* **Key Concepts**:
  * **DevOps vs DevSecOps vs SRE**
    * **SRE** asks: "Is the system running reliably? What's the error rate? Is our SLO met?"
    * **DevSecOps** asks: "Is the code secure? Does the image have CVEs? Are there code smells?"
  * **Why DevSecOps?**
    * **Faster releases** — no security bottleneck at the end; checks are automated
    * **Vulnerability-free deployments** — images are scanned before they run
    * **Code quality gates** — bad code can't merge if SonarQube fails
    * **Reduced production failures** — cleaner code, safer images
  * **Core Tools Overview**
  * **SonarQube  Code Quality & Security Analysis**
    * **Bugs** — code that will likely cause errors at runtime
    * **Vulnerabilities** — security weaknesses (e.g., SQL injection risk, hardcoded passwords)
    * **Code Smells** — bad practices that make code hard to maintain
    * **Duplications** — copy-pasted code blocks
  * **Trivy  Container Image Vulnerability Scanner**
  * **Infrastructure Setup on AWS EC2**
  * **Software Installation**
  * **SonarQube Configuration**
  * **Jenkins Configuration & Integration**
  * **Full DevSecOps Pipeline**
  * **Three-Tier Application Deployment**
  * **Reading Pipeline Results**
  * **Tech Stack Mapping**
  * **Quick Reference Cheatsheet**
  * **Navigation Footer**

### Key Commands / Code Example:

```
Traditional DevOps:
  Code → Build → Test → Deploy → 🔥 Security issue found in production → Fix

DevSecOps (Shift Left):
  Code → 🔍 SAST → Build → 🔍 Image Scan → Test → Deploy → ✅ Already secure
```

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## 57. MLOps: FastAPI, Docker & AWS EKS (IT Career Prediction System)

🔗 **Full Lesson:** [57_MLOps_FastAPI_Docker_AWS_EKS_IT_Career_Prediction_System.md](./57_MLOps_FastAPI_Docker_AWS_EKS_IT_Career_Prediction_System.md)

* **What**: Introduction and foundational concepts of MLOps: FastAPI + Docker + AWS EKS (IT Career Prediction System).
* **Why It Exists**: Traditional DevOps pipelines don't account for:
- **Model training** — a step that doesn't exist in regular software
- **Data pipelines** — the model needs fresh, clean data
- **Model drift** — a model that was 95% accurate in January may be 70% accurate in December as real-world data changes
- **Experiment tracking** — data scientists run hundreds of experiments; we need to track which model performed best
* **Key Concepts**:
  * **DevOps vs MLOps**
    * **Model training** — a step that doesn't exist in regular software
    * **Data pipelines** — the model needs fresh, clean data
    * **Model drift** — a model that was 95% accurate in January may be 70% accurate in December as real-world data changes
    * **Experiment tracking** — data scientists run hundreds of experiments; we need to track which model performed best
  * **Project Overview: IT Career Upskilling Prediction**
  * **FastAPI  The ML Serving Layer**
  * **Python Virtual Environment**
  * **ML Model Training (train.py)**
  * **Dockerizing the ML Application**
  * **AWS IAM User & CLI Setup**
  * **kubectl, eksctl  Kubernetes CLI Tools**
  * **AWS EKS  Managed Kubernetes**
  * **Kubernetes Deployment Manifest**
  * **Full Architecture Diagram**
  * **Complete Step-by-Step Commands**
  * **Tech Stack Mapping**
  * **Cleanup & Cost Control**
  * **Quick Reference Cheatsheet**
  * **Navigation Footer**

### Key Commands / Code Example:

```
┌─────────────────────────────────────────────────────┐
│              IT Career Prediction System            │
│                                                     │
│  train.py ──► model.pkl (trained ML model)          │
│                  │                                  │
│  main.py ────────┤ FastAPI app loads model           │
│  (FastAPI)       │ serves predictions via REST API  │
│                  │                                  │
│  Dockerfile ─────► Docker Image (~3.3 GB)           │
│                  │                                  │
│  k8s-deploy.yml ─► EKS Cluster (2 pods)             │
│                      Public LoadBalancer IP         │
└─────────────────────────────────────────────────────┘
```

> [!IMPORTANT]
> Always verify configurations and test deployments in staging before promoting to production.

---

## 99. Real-World DevOps Problems: Common & Rare (Remediation Playbook)

🔗 **Full Playbook:** [99_Real_Devops_Problems.md](./99_Real_Devops_Problems.md)

* **What**: A production troubleshooting playbook listing common and rare DevOps failures (K8s OOMKilled, Docker space/inodes exhaustion, RDS Connection timeouts, Jenkins hangs, Terraform locks, Subnet IP exhaustion, Linux file descriptors exhaustion, DNS loops, KMS throttling, MLOps concept drift).
* **Why It Exists**: Real-world DevOps engineers spend 40-50% of their time troubleshooting incidents. This playbook provides step-by-step diagnostic tools, root cause analyses, command remediations, and architectural preventions.
* **Key Concepts**:
  * **Common Failures**: Step-by-step remediation for recurring cluster and VM issues.
  * **Rare & Complex Scenarios**: Exhaustive analysis of obscure production outages (subnet IP limit bounds, socket leaks, KMS throttling).
  * **Diagnostic Cheatsheet**: Quick-reference table mapping symptoms to commands.

### Key Commands / Code Example:

```bash
# Clean up all unused docker containers, networks, images, and volumes
docker system prune -a --volumes -f

# Force-unlock a hung Terraform state
terraform force-unlock <LOCK-ID>
```

> [!IMPORTANT]
> Never run destructive commands (like force-unlock or bulk prunes) in production without verifying network/cluster state and coordinate with team members first.

---

Previous : [00_index.md](./00_index.md) | Index : [00_index.md](./00_index.md) | Next : [01_DevOps_Basics.md](./01_DevOps_Basics.md)
