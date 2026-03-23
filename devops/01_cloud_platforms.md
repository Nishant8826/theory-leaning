# 01 — Cloud Platforms & Introduction to AI

> A beginner-friendly, in-depth guide to **AWS, Azure, Google Cloud Platform**, and modern **Artificial Intelligence** concepts.

---

## Table of Contents

1. [Introduction to Cloud Platforms](#1-introduction-to-cloud-platforms)
2. [AWS (Amazon Web Services)](#2-aws-amazon-web-services)
3. [Microsoft Azure](#3-microsoft-azure)
4. [Google Cloud Platform (GCP)](#4-google-cloud-platform-gcp)
5. [Comparison — AWS vs Azure vs GCP](#5-comparison--aws-vs-azure-vs-gcp)
6. [Introduction to Artificial Intelligence](#6-introduction-to-artificial-intelligence)
7. [Real-World Use Cases](#7-real-world-use-cases)
8. [Summary](#8-summary)

---

## 1. Introduction to Cloud Platforms

### 1.1 What Is Cloud Computing?

Imagine you need a powerful computer to run your website, but buying one is expensive, and you only need it for a few hours a day. **Cloud computing** lets you *rent* that computer (and much more) over the internet — you pay only for what you use, just like an electricity bill.

> **In one line:** Cloud computing is using someone else's computers, storage, and software over the internet instead of owning them yourself.

**Simple analogy:**

| Without Cloud | With Cloud |
|---|---|
| Buying your own car | Using Uber / Ola |
| Building your own power plant | Using the electricity grid |
| Buying DVDs to watch movies | Using Netflix to stream movies |

### 1.2 Why Do Companies Use Cloud Platforms?

- **💰 Save Money** — No need to buy expensive servers. Pay only for what you use.
- **📈 Easy to Scale** — Need more power during a sale event? Add servers in minutes, remove them later.
- **🌍 Global Reach** — Deploy your app in data centers across the world so users everywhere get fast access.
- **🔒 Security** — Cloud providers invest billions in security — often more than any single company can afford.
- **⚡ Speed** — Launch new servers, databases, or AI models in seconds instead of weeks.
- **🛡️ Reliability** — Cloud providers guarantee 99.9 %+ uptime with backups across multiple locations.
- **🔧 Managed Services** — Let the cloud handle updates, patches, and maintenance so your team can focus on building products.

### 1.3 The Big Three Cloud Providers

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

| Provider | Full Name | Parent Company |
|---|---|---|
| **AWS** | Amazon Web Services | Amazon |
| **Azure** | Microsoft Azure | Microsoft |
| **GCP** | Google Cloud Platform | Google (Alphabet) |

All three offer similar categories of services (compute, storage, networking, databases, AI/ML, etc.), but each has unique strengths.

---

## 2. AWS (Amazon Web Services)

### 2.1 What Is AWS?

**AWS (Amazon Web Services)** is a cloud computing platform provided by **Amazon**. It was launched in **2006** and is currently the **largest** cloud provider in the world.

AWS offers **200+ services** — from renting virtual computers to running machine learning models, from storing files to sending emails.

> **Fun fact:** AWS was born because Amazon had excess computing capacity from running its own e-commerce site and decided to rent it out to others.

### 2.2 Why Do Companies Use AWS?

- **🏆 Market Leader** — Largest cloud provider with the most mature ecosystem.
- **🌐 Global Infrastructure** — 30+ geographic regions, 100+ availability zones worldwide.
- **🧩 Widest Service Selection** — 200+ fully featured services.
- **📚 Huge Community** — Largest community of users, tutorials, certifications, and third-party tools.
- **💼 Enterprise Ready** — Used by startups to Fortune 500 companies.
- **🆓 Free Tier** — Many services have a free tier so you can learn without spending money.

### 2.3 Key AWS Services

| Service | What It Does | Real-World Analogy |
|---|---|---|
| **EC2** (Elastic Compute Cloud) | Rent virtual computers | Renting a workspace in a co-working space |
| **S3** (Simple Storage Service) | Store files (images, videos, backups) | Google Drive / Dropbox but for apps |
| **IAM** (Identity & Access Management) | Control who can access what | Security guard + ID card system |
| **VPC** (Virtual Private Cloud) | Create your own private network | Building walls around your office floor |
| **RDS** | Managed databases | Hiring a DBA (database admin) for you |
| **Lambda** | Run code without managing servers | A vending machine — put money in, get result out |
| **CloudFront** | Deliver content fast globally (CDN) | Local branches of a library near your home |
| **Route 53** | Domain name system (DNS) | Phone book that maps names to addresses |

### 2.4 Real-World Companies Using AWS

| Company | How They Use AWS |
|---|---|
| **Netflix** | Streams all its video content using AWS (EC2, S3, CloudFront) |
| **Airbnb** | Hosts its entire platform on AWS |
| **Slack** | Uses AWS for messaging infrastructure |
| **NASA** | Uses AWS to store and process satellite imagery |
| **Samsung** | Uses AWS for its SmartThings IoT platform |
| **McDonald's** | Uses AWS for mobile ordering and analytics |

---

### 2.5 How Virtual Machines Are Created in AWS

#### What Is EC2?

**EC2 (Elastic Compute Cloud)** is AWS's service that lets you create **virtual machines** (VMs) in the cloud. Each VM is called an **EC2 instance**.

Think of it as renting a computer:
- You choose the operating system (Windows or Linux).
- You choose how powerful it should be (CPU, RAM).
- You turn it on, use it, and turn it off when you're done.
- You only pay for the time it was running.

#### Step-by-Step Concept of Launching an EC2 Instance

```
 ┌──────────────────────────────────────────────────────┐
 │          LAUNCHING AN EC2 INSTANCE                    │
 │                                                       │
 │  Step 1 ──▶  Choose an AMI (Operating System)        │
 │                (e.g., Ubuntu, Amazon Linux, Windows)  │
 │                                                       │
 │  Step 2 ──▶  Choose Instance Type (Size)             │
 │                (e.g., t2.micro = 1 CPU, 1 GB RAM)    │
 │                                                       │
 │  Step 3 ──▶  Configure Network (VPC & Subnet)        │
 │                (Which private network to use)         │
 │                                                       │
 │  Step 4 ──▶  Add Storage (EBS Volume)                │
 │                (e.g., 20 GB SSD hard disk)            │
 │                                                       │
 │  Step 5 ──▶  Set Security Group (Firewall Rules)     │
 │                (e.g., Allow SSH on port 22)           │
 │                                                       │
 │  Step 6 ──▶  Create / Select Key Pair                │
 │                (SSH key to log into the machine)      │
 │                                                       │
 │  Step 7 ──▶  Launch! 🚀                              │
 └──────────────────────────────────────────────────────┘
```

#### Components Involved

| Component | What It Is | Why It's Needed |
|---|---|---|
| **AMI** (Amazon Machine Image) | A pre-built template containing the OS and software | So AWS knows what operating system to install |
| **Instance Type** | Defines CPU, RAM, and network capacity (e.g., `t2.micro`, `m5.large`) | So you get the right amount of power for your workload |
| **Key Pair** | A pair of encryption keys (public + private) | So you can securely log into your VM via SSH |
| **Security Group** | A virtual firewall that controls inbound/outbound traffic | To protect your VM from unwanted access |
| **EBS Volume** | Elastic Block Store — the hard disk attached to your VM | To store your data, OS files, and applications |
| **VPC / Subnet** | The private network and sub-network where your VM lives | To isolate your resources and control network traffic |

---

### 2.6 Methods to Create VMs in AWS

There are **four main ways** to create an EC2 instance:

#### Method 1 — AWS Console (GUI)

The **AWS Management Console** is a web-based interface (like a website dashboard) where you can click through menus to create and manage resources.

**Best for:** Beginners, quick one-off tasks, learning.

**Steps:**
1. Log in to [console.aws.amazon.com](https://console.aws.amazon.com)
2. Search for **EC2** in the search bar
3. Click **"Launch Instance"**
4. Follow the wizard (choose AMI → Instance Type → Key Pair → Security Group → Launch)

> **Pros:** Easy, visual, no coding needed.
> **Cons:** Manual, slow, not repeatable — not ideal for creating 100 servers.

---

#### Method 2 — AWS CLI (Command Line Interface)

The **AWS CLI** is a tool you install on your computer that lets you manage AWS resources by typing commands in the terminal.

**Best for:** Automating tasks, scripting, faster than GUI.

**Installation:**
```bash
# Install AWS CLI (on Linux/macOS)
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Configure credentials
aws configure
# It will ask for: Access Key ID, Secret Key, Default Region, Output format
```

**Example — Launch an EC2 instance using CLI:**
```bash
aws ec2 run-instances \
  --image-id ami-0abcdef1234567890 \
  --instance-type t2.micro \
  --key-name my-key-pair \
  --security-group-ids sg-0123456789abcdef0 \
  --subnet-id subnet-0123456789abcdef0 \
  --count 1 \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=MyFirstServer}]'
```

**What this command does:**
- `--image-id` → Which OS image to use (Ubuntu, Amazon Linux, etc.)
- `--instance-type` → How powerful the machine should be
- `--key-name` → SSH key to log in
- `--security-group-ids` → Firewall rules
- `--count 1` → Create 1 instance
- `--tag-specifications` → Give the instance a name

---

#### Method 3 — Infrastructure as Code (Terraform / CloudFormation)

**Infrastructure as Code (IaC)** means you write your infrastructure in a file (like a recipe), and a tool reads that file and creates everything automatically.

##### AWS CloudFormation (AWS-native)

CloudFormation uses **YAML or JSON** templates:

```yaml
# cloudformation-ec2.yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: Create a simple EC2 instance

Resources:
  MyEC2Instance:
    Type: AWS::EC2::Instance
    Properties:
      ImageId: ami-0abcdef1234567890
      InstanceType: t2.micro
      KeyName: my-key-pair
      SecurityGroupIds:
        - sg-0123456789abcdef0
      Tags:
        - Key: Name
          Value: MyCloudFormationServer
```

```bash
# Deploy the stack
aws cloudformation create-stack \
  --stack-name my-first-stack \
  --template-body file://cloudformation-ec2.yaml
```

##### Terraform (Multi-cloud)

Terraform uses its own language called **HCL (HashiCorp Configuration Language)**:

```hcl
# main.tf
provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "my_server" {
  ami           = "ami-0abcdef1234567890"
  instance_type = "t2.micro"
  key_name      = "my-key-pair"

  tags = {
    Name = "MyTerraformServer"
  }
}
```

```bash
# Initialize Terraform
terraform init

# Preview what will be created
terraform plan

# Create the infrastructure
terraform apply
```

> **Why use IaC?**
> - Repeatable — run the same file to create identical environments.
> - Version controlled — store your infrastructure in Git.
> - Team-friendly — everyone uses the same configuration.
> - Terraform works across AWS, Azure, GCP, and more.

---

#### Method 4 — SDK / APIs

AWS provides **SDKs (Software Development Kits)** for many programming languages (Python, Java, Node.js, Go, etc.) so you can create and manage resources from your own applications.

**Example — Create an EC2 instance using Python (Boto3):**

```python
import boto3

# Create an EC2 client
ec2 = boto3.resource('ec2', region_name='us-east-1')

# Launch an instance
instances = ec2.create_instances(
    ImageId='ami-0abcdef1234567890',
    InstanceType='t2.micro',
    KeyName='my-key-pair',
    MinCount=1,
    MaxCount=1,
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {'Key': 'Name', 'Value': 'MyPythonServer'}
            ]
        }
    ]
)

print(f"Instance created: {instances[0].id}")
```

> **When to use SDKs?**
> - When you need to create resources as part of an application.
> - When you need complex logic (if/else, loops) around resource creation.
> - When building automation tools or custom dashboards.

---

#### Quick Comparison of All Methods

| Method | Best For | Learning Curve | Repeatability | Speed |
|---|---|---|---|---|
| **Console (GUI)** | Beginners, one-off tasks | ⭐ Easy | ❌ Low | 🐢 Slow |
| **CLI** | Scripting, quick automation | ⭐⭐ Medium | ✅ Good | 🐇 Fast |
| **IaC (Terraform / CFN)** | Production, team workflows | ⭐⭐⭐ Higher | ✅✅ Excellent | 🐇 Fast |
| **SDK / APIs** | App integration, complex logic | ⭐⭐⭐ Higher | ✅ Good | 🐇 Fast |

---

## 3. Microsoft Azure

### 3.1 What Is Azure?

**Microsoft Azure** is a cloud computing platform provided by **Microsoft**. Launched in **2010**, it is the **second-largest** cloud provider in the world.

Azure is especially popular among companies that already use Microsoft products like **Windows Server, Active Directory, Office 365, SQL Server**, and **.NET**.

> **Think of it this way:** If your company already lives in the Microsoft world, Azure is the natural extension of that world into the cloud.

### 3.2 Why Do Companies Use Azure?

- **🔗 Microsoft Integration** — Seamless integration with Windows, Office 365, Active Directory, Teams, SQL Server.
- **🏢 Enterprise Focus** — Strong hybrid cloud capabilities (connect on-premises data centers to the cloud).
- **🌍 Global Presence** — 60+ regions worldwide — more than any other cloud provider.
- **🔐 Compliance** — Meets 90+ compliance certifications (important for healthcare, finance, government).
- **🎓 Familiar Tools** — Developers who know .NET, C#, Visual Studio, and PowerShell feel at home.
- **💡 AI & ML** — Azure OpenAI Service gives access to GPT-4, DALL·E, and more.

### 3.3 Important Azure Services

| Service | What It Does | AWS Equivalent |
|---|---|---|
| **Azure Virtual Machines** | Rent virtual computers | EC2 |
| **Blob Storage** | Store unstructured data (files, images, videos) | S3 |
| **Azure Active Directory (Azure AD / Entra ID)** | Identity and access management | IAM |
| **Virtual Network (VNet)** | Private network for your resources | VPC |
| **Azure SQL Database** | Managed SQL database | RDS |
| **Azure Functions** | Run code without servers (serverless) | Lambda |
| **Azure DevOps** | CI/CD pipelines, repos, project management | CodePipeline + CodeBuild |
| **Azure Kubernetes Service (AKS)** | Managed Kubernetes | EKS |

---

### 3.4 How Virtual Machines Are Created in Azure

#### What Are Azure Virtual Machines?

Azure Virtual Machines (VMs) are on-demand, scalable computing resources offered by Microsoft Azure. Just like AWS EC2, you can create a VM, choose its size, install an operating system, and use it like a regular computer — all from the cloud.

#### Steps Involved in Creating an Azure VM

```
 ┌──────────────────────────────────────────────────────┐
 │        CREATING AN AZURE VIRTUAL MACHINE              │
 │                                                       │
 │  Step 1 ──▶  Choose a Resource Group                 │
 │                (A container to organize resources)    │
 │                                                       │
 │  Step 2 ──▶  Select a Region                         │
 │                (e.g., East US, West Europe, India)    │
 │                                                       │
 │  Step 3 ──▶  Choose an Image (OS)                    │
 │                (e.g., Ubuntu 22.04, Windows Server)   │
 │                                                       │
 │  Step 4 ──▶  Select VM Size                          │
 │                (e.g., Standard_B1s = 1 CPU, 1 GB RAM)│
 │                                                       │
 │  Step 5 ──▶  Configure Authentication                │
 │                (SSH key or username/password)          │
 │                                                       │
 │  Step 6 ──▶  Set Up Networking                       │
 │                (VNet, Subnet, Public IP, NSG)          │
 │                                                       │
 │  Step 7 ──▶  Configure Disks                         │
 │                (OS disk + optional data disks)         │
 │                                                       │
 │  Step 8 ──▶  Review & Create! 🚀                     │
 └──────────────────────────────────────────────────────┘
```

#### Components Involved

| Component | What It Is | Why It's Needed |
|---|---|---|
| **Resource Group** | A logical container that groups related Azure resources | Helps you organize, manage, and delete resources together |
| **Image** | Pre-built OS template (Ubuntu, CentOS, Windows Server) | Defines which operating system the VM will run |
| **VM Size** | Defines CPU, RAM, and disk capacity (e.g., `Standard_B1s`) | Determines the computing power of your VM |
| **Virtual Network (VNet)** | A private network in Azure for your resources | Isolates your resources and controls traffic |
| **Network Security Group (NSG)** | Firewall rules for inbound/outbound traffic | Protects the VM from unauthorized access |
| **Managed Disk** | The virtual hard drive attached to the VM | Stores the OS, applications, and data |
| **Public IP Address** | An internet-facing IP address | Allows you to connect to the VM from outside Azure |

---

### 3.5 Methods to Create VMs in Azure

#### Method 1 — Azure Portal (GUI)

The **Azure Portal** ([portal.azure.com](https://portal.azure.com)) is a web-based dashboard for managing Azure resources visually.

**Steps:**
1. Log in to the Azure Portal
2. Click **"Create a Resource"** → **"Virtual Machine"**
3. Fill in details: Resource Group, VM Name, Region, Image, Size
4. Configure authentication (SSH Key or Password)
5. Review and click **"Create"**

> **Pros:** Beginner-friendly, visual.
> **Cons:** Manual, not repeatable at scale.

---

#### Method 2 — Azure CLI

The **Azure CLI** (`az`) is a command-line tool for managing Azure resources.

**Installation:**
```bash
# Install Azure CLI (Linux)
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Login to Azure
az login
```

**Example — Create a VM using Azure CLI:**
```bash
# Create a resource group
az group create \
  --name MyResourceGroup \
  --location eastus

# Create a virtual machine
az vm create \
  --resource-group MyResourceGroup \
  --name MyAzureVM \
  --image Ubuntu2204 \
  --size Standard_B1s \
  --admin-username azureuser \
  --generate-ssh-keys \
  --public-ip-sku Standard
```

**What this command does:**
- `--resource-group` → Which group to put the VM in
- `--name` → Name of the VM
- `--image` → Operating system (Ubuntu 22.04)
- `--size` → How powerful the VM is
- `--generate-ssh-keys` → Automatically creates SSH keys for login

---

#### Method 3 — ARM Templates / Bicep

##### ARM Templates (JSON-based)

**Azure Resource Manager (ARM) Templates** are JSON files that define your infrastructure:

```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  "resources": [
    {
      "type": "Microsoft.Compute/virtualMachines",
      "apiVersion": "2023-03-01",
      "name": "MyArmVM",
      "location": "eastus",
      "properties": {
        "hardwareProfile": {
          "vmSize": "Standard_B1s"
        },
        "osProfile": {
          "computerName": "MyArmVM",
          "adminUsername": "azureuser"
        },
        "storageProfile": {
          "imageReference": {
            "publisher": "Canonical",
            "offer": "0001-com-ubuntu-server-jammy",
            "sku": "22_04-lts",
            "version": "latest"
          }
        }
      }
    }
  ]
}
```

##### Bicep (Simplified ARM)

**Bicep** is Microsoft's newer, simpler language for writing ARM templates:

```bicep
// main.bicep
resource myVM 'Microsoft.Compute/virtualMachines@2023-03-01' = {
  name: 'MyBicepVM'
  location: 'eastus'
  properties: {
    hardwareProfile: {
      vmSize: 'Standard_B1s'
    }
    osProfile: {
      computerName: 'MyBicepVM'
      adminUsername: 'azureuser'
    }
  }
}
```

```bash
# Deploy a Bicep template
az deployment group create \
  --resource-group MyResourceGroup \
  --template-file main.bicep
```

> **Why Bicep over ARM?** Bicep is cleaner, shorter, and easier to read while compiling down to the same ARM JSON.

---

#### Method 4 — Terraform

Terraform works with Azure just like it does with AWS — write HCL, run `terraform apply`.

```hcl
# main.tf
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "example" {
  name     = "MyResourceGroup"
  location = "East US"
}

resource "azurerm_virtual_machine" "example" {
  name                  = "MyTerraformVM"
  location              = azurerm_resource_group.example.location
  resource_group_name   = azurerm_resource_group.example.name
  vm_size               = "Standard_B1s"

  storage_os_disk {
    name              = "osdisk"
    caching           = "ReadWrite"
    create_option     = "FromImage"
  }

  storage_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts"
    version   = "latest"
  }

  os_profile {
    computer_name  = "hostname"
    admin_username = "azureuser"
  }

  os_profile_linux_config {
    disable_password_authentication = true
  }
}
```

```bash
terraform init
terraform plan
terraform apply
```

---

## 4. Google Cloud Platform (GCP)

### 4.1 What Is GCP?

**Google Cloud Platform (GCP)** is a suite of cloud computing services provided by **Google**. Launched in **2008**, GCP runs on the same infrastructure that Google uses internally for products like **Search, Gmail, YouTube, and Google Maps**.

> **Think of it this way:** GCP gives you access to the same powerful technology that runs Google's own products.

### 4.2 Why Do Companies Use GCP?

- **📊 Data & Analytics Leader** — BigQuery is one of the best tools for analyzing massive datasets.
- **🤖 AI / ML Powerhouse** — TensorFlow, Vertex AI, and pre-trained models from Google's AI research.
- **🌐 Google's Network** — One of the fastest and most reliable private networks on the planet.
- **💲 Cost-Effective** — Sustained-use discounts automatically reduce costs for long-running VMs.
- **☸️ Kubernetes Native** — GKE (Google Kubernetes Engine) is considered the best-managed Kubernetes service — Google invented Kubernetes!
- **🔓 Open Source Friendly** — Strong support for open-source tools and multi-cloud strategies.

### 4.3 Important GCP Services

| Service | What It Does | AWS Equivalent |
|---|---|---|
| **Compute Engine** | Rent virtual machines | EC2 |
| **Cloud Storage** | Store files and objects | S3 |
| **IAM** | Identity and access management | IAM |
| **VPC** | Virtual private cloud networking | VPC |
| **BigQuery** | Serverless data warehouse for analytics | Redshift / Athena |
| **Cloud Functions** | Run serverless code | Lambda |
| **GKE** | Managed Kubernetes | EKS |
| **Cloud Run** | Run containers without managing infrastructure | Fargate |
| **Vertex AI** | Build and deploy ML models | SageMaker |

---

### 4.4 How Virtual Machines Are Created in GCP

#### What Is Compute Engine?

**Compute Engine** is GCP's service for creating and managing virtual machines. It's the equivalent of AWS EC2 and Azure Virtual Machines.

You can create VMs running **Linux or Windows**, choose the machine type (CPU + RAM), attach disks, and connect them to networks.

#### Steps for Creating a VM in GCP

```
 ┌──────────────────────────────────────────────────────┐
 │       CREATING A GCP COMPUTE ENGINE VM                │
 │                                                       │
 │  Step 1 ──▶  Select a Project                        │
 │                (Logical grouping for resources)       │
 │                                                       │
 │  Step 2 ──▶  Choose a Region & Zone                  │
 │                (e.g., us-central1-a)                  │
 │                                                       │
 │  Step 3 ──▶  Choose a Machine Type                   │
 │                (e.g., e2-micro = 0.25 vCPU, 1 GB)    │
 │                                                       │
 │  Step 4 ──▶  Select a Boot Disk Image                │
 │                (e.g., Debian, Ubuntu, Windows)        │
 │                                                       │
 │  Step 5 ──▶  Configure Boot Disk Size & Type         │
 │                (e.g., 10 GB SSD or Standard)          │
 │                                                       │
 │  Step 6 ──▶  Set Up Networking                       │
 │                (VPC, Subnet, External IP, Firewall)   │
 │                                                       │
 │  Step 7 ──▶  Add SSH Keys (Optional)                 │
 │                                                       │
 │  Step 8 ──▶  Create! 🚀                              │
 └──────────────────────────────────────────────────────┘
```

#### Components Involved

| Component | What It Is | Why It's Needed |
|---|---|---|
| **Project** | A top-level container for all GCP resources | Organizes resources, billing, and permissions |
| **Machine Type** | Defines CPU and memory (e.g., `e2-micro`, `n2-standard-4`) | Determines how powerful the VM is |
| **Boot Disk Image** | OS template (Debian, Ubuntu, CentOS, Windows) | Defines the operating system |
| **Persistent Disk** | The virtual hard drive (SSD or HDD) | Stores OS, apps, and data — persists even if VM is deleted |
| **VPC Network** | Virtual Private Cloud network | Controls network communication between resources |
| **Firewall Rules** | Rules to allow/deny traffic | Protects the VM from unauthorized network access |
| **External IP** | Public IP address | Allows access to the VM from the internet |

---

### 4.5 Methods to Create VMs in GCP

#### Method 1 — Google Cloud Console (GUI)

The **Cloud Console** ([console.cloud.google.com](https://console.cloud.google.com)) is GCP's web-based dashboard.

**Steps:**
1. Log in to the Cloud Console
2. Navigate to **Compute Engine → VM Instances**
3. Click **"Create Instance"**
4. Fill in: Name, Region, Machine Type, Boot Disk, Networking
5. Click **"Create"**

---

#### Method 2 — gcloud CLI

`gcloud` is GCP's command-line tool.

**Installation:**
```bash
# Install Google Cloud SDK
curl https://sdk.cloud.google.com | bash

# Initialize and authenticate
gcloud init
gcloud auth login
```

**Example — Create a VM:**
```bash
gcloud compute instances create my-gcp-vm \
  --zone=us-central1-a \
  --machine-type=e2-micro \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud \
  --boot-disk-size=20GB \
  --boot-disk-type=pd-ssd \
  --tags=http-server,https-server
```

**What this command does:**
- `--zone` → Physical location of the VM
- `--machine-type` → CPU + RAM configuration
- `--image-family` → Operating system
- `--boot-disk-size` → Size of the hard drive
- `--tags` → Labels for applying firewall rules

---

#### Method 3 — Terraform

```hcl
# main.tf
provider "google" {
  project = "my-gcp-project-id"
  region  = "us-central1"
}

resource "google_compute_instance" "my_vm" {
  name         = "my-terraform-vm"
  machine_type = "e2-micro"
  zone         = "us-central1-a"

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2204-lts"
      size  = 20
      type  = "pd-ssd"
    }
  }

  network_interface {
    network = "default"

    access_config {
      // This gives the VM a public IP
    }
  }

  tags = ["http-server", "https-server"]
}
```

```bash
terraform init
terraform plan
terraform apply
```

---

#### Method 4 — Deployment Manager / APIs

##### Google Cloud Deployment Manager

Deployment Manager is GCP's native IaC tool that uses **YAML** config files:

```yaml
# vm-config.yaml
resources:
  - name: my-dm-vm
    type: compute.v1.instance
    properties:
      zone: us-central1-a
      machineType: zones/us-central1-a/machineTypes/e2-micro
      disks:
        - deviceName: boot
          type: PERSISTENT
          boot: true
          autoDelete: true
          initializeParams:
            sourceImage: projects/ubuntu-os-cloud/global/images/family/ubuntu-2204-lts
      networkInterfaces:
        - network: global/networks/default
          accessConfigs:
            - name: External NAT
              type: ONE_TO_ONE_NAT
```

```bash
# Deploy
gcloud deployment-manager deployments create my-vm-deployment \
  --config vm-config.yaml
```

##### REST API

You can also create VMs by making HTTP requests directly to GCP's REST API:

```bash
curl -X POST \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  "https://compute.googleapis.com/compute/v1/projects/MY_PROJECT/zones/us-central1-a/instances" \
  -d '{
    "name": "api-created-vm",
    "machineType": "zones/us-central1-a/machineTypes/e2-micro",
    "disks": [{
      "boot": true,
      "autoDelete": true,
      "initializeParams": {
        "sourceImage": "projects/ubuntu-os-cloud/global/images/family/ubuntu-2204-lts"
      }
    }],
    "networkInterfaces": [{
      "network": "global/networks/default",
      "accessConfigs": [{"type": "ONE_TO_ONE_NAT", "name": "External NAT"}]
    }]
  }'
```

---

## 5. Comparison — AWS vs Azure vs GCP

### Service-by-Service Comparison

| Feature | AWS | Azure | GCP |
|---|---|---|---|
| **Virtual Machines** | EC2 | Virtual Machines | Compute Engine |
| **Object Storage** | S3 | Blob Storage | Cloud Storage |
| **Block Storage** | EBS | Managed Disks | Persistent Disk |
| **Virtual Network** | VPC | VNet | VPC |
| **Identity & Access** | IAM | Azure AD / Entra ID | Cloud IAM |
| **Serverless Functions** | Lambda | Azure Functions | Cloud Functions |
| **Managed Kubernetes** | EKS | AKS | GKE |
| **Managed Database (SQL)** | RDS | Azure SQL | Cloud SQL |
| **Data Warehouse** | Redshift | Synapse Analytics | BigQuery |
| **CDN** | CloudFront | Azure CDN | Cloud CDN |
| **DNS** | Route 53 | Azure DNS | Cloud DNS |
| **AI/ML** | SageMaker | Azure ML / Azure OpenAI | Vertex AI |
| **IaC (Native)** | CloudFormation | ARM / Bicep | Deployment Manager |

### Pricing, Strengths & Adoption

| Aspect | AWS | Azure | GCP |
|---|---|---|---|
| **Pricing Model** | Pay-as-you-go + Reserved/Savings Plans | Pay-as-you-go + Reserved + Hybrid Benefit | Pay-as-you-go + Sustained/Committed Use |
| **Free Tier** | 12 months free + always-free services | 12 months free + always-free services | 90-day $300 credit + always-free services |
| **Biggest Strength** | Widest service selection, largest ecosystem | Microsoft integration, hybrid cloud | Data/AI/ML, Kubernetes, network speed |
| **Ideal For** | Startups, enterprises, any workload | Microsoft-centric orgs, hybrid setups | Data analytics, AI/ML, containers |
| **Market Share** | ~31 % | ~25 % | ~11 % |

### Companies Using Each Platform

| AWS | Azure | GCP |
|---|---|---|
| Netflix | Microsoft 365 / Teams | YouTube |
| Airbnb | LinkedIn | Spotify |
| Slack | Samsung | Snapchat |
| NASA | eBay | Twitter/X |
| McDonald's | Adobe | PayPal |
| Twitch | GE Healthcare | Target |

---

## 6. Real-World Use Cases

### 🎬 Netflix Using AWS

Netflix is one of the largest customers of AWS. Here's how they use it:

- **EC2 instances** — Run thousands of servers to encode, process, and stream video content.
- **S3** — Store petabytes of video files, images, and backups.
- **CloudFront (CDN)** — Deliver content to 200+ million users worldwide with low latency.
- **DynamoDB** — Store user preferences, viewing history, and recommendations.
- **Auto Scaling** — Automatically add more servers during peak hours (evenings, weekends) and remove them during off-peak times.

> **Result:** Netflix streams to 200+ million subscribers in 190+ countries with 99.99 % uptime.

---

### 🏢 Microsoft Services Using Azure

Microsoft uses Azure to power its own products and services:

- **Microsoft 365** (Word, Excel, PowerPoint Online) — Runs on Azure infrastructure.
- **Teams** — All video calls, chats, and file sharing use Azure.
- **LinkedIn** — After Microsoft acquired LinkedIn, it moved to Azure.
- **Xbox Cloud Gaming** — Uses Azure data centers to stream games to devices.
- **Bing Chat / Copilot** — Uses Azure OpenAI Service to power AI features.

> **Result:** Microsoft demonstrates that Azure can handle massive enterprise-scale workloads.

---

### 📺 YouTube Using GCP

YouTube is the world's largest video platform — and it runs entirely on GCP:

- **Compute Engine** — Processes and transcodes billions of videos.
- **Cloud Storage** — Stores over 800 million videos.
- **BigQuery** — Analyzes viewing patterns, ad performance, and creator analytics.
- **Cloud CDN** — Delivers video to 2+ billion monthly users with minimal buffering.
- **AI/ML** — Powers video recommendations, content moderation, auto-captions, and ad targeting.

> **Result:** YouTube serves 1 billion hours of video every day to users in 100+ countries.

---

## 7. Summary

### ☁️ Why Cloud Platforms Are Important

- Cloud computing has **transformed** how companies build and run software.
- Instead of buying expensive hardware, companies can **rent exactly what they need** from cloud providers.
- Cloud enables **faster innovation**, **global reach**, **better security**, and **cost savings**.
- Almost every modern application — from Netflix to Uber to ChatGPT — runs on cloud infrastructure.

### 🤔 When to Choose AWS vs Azure vs GCP

| Choose… | When… |
|---|---|
| **AWS** | You want the widest selection of services, the largest community, or you're a startup looking for the most mature ecosystem. |
| **Azure** | Your company already uses Microsoft products (Office 365, Active Directory, .NET) and wants seamless integration. |
| **GCP** | Your focus is on data analytics, machine learning, or Kubernetes — or you want Google-grade networking. |

> **Pro Tip:** Many large companies use **multi-cloud** strategies — running some workloads on AWS, some on Azure, and some on GCP — to avoid vendor lock-in and leverage each provider's strengths.

---
Previous: [00_Basics.md](00_Basics.md) Next: [02_Artificial_Intelligence.md](02_Artificial_Intelligence.md)
---
