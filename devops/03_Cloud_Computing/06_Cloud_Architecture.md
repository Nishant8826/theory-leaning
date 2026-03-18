# 🏗️ Architecture of Cloud Computing

---

## 📌 Overview

Cloud computing architecture describes **how the cloud is structured** — from what the user sees on their screen to the powerful servers running behind the scenes.

It has two main parts: **Frontend** and **Backend**.

---

## 📌 The Big Picture (Text-Based Diagram)

```
┌────────────────────────────────────────────────────────────────┐
│                    CLOUD COMPUTING ARCHITECTURE                 │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│   👤 USER (You)                                                │
│     │                                                          │
│     │  Uses browser, app, or CLI                               │
│     ▼                                                          │
│   ┌──────────────────────────────┐                             │
│   │        FRONTEND              │                             │
│   │  (What the user sees)        │                             │
│   │  - Web Browser               │                             │
│   │  - Mobile App                │                             │
│   │  - Desktop Application       │                             │
│   │  - Cloud Console (Dashboard) │                             │
│   └──────────────┬───────────────┘                             │
│                  │                                              │
│                  │  ← Internet (HTTPS/API calls) →             │
│                  │                                              │
│   ┌──────────────▼───────────────┐                             │
│   │         BACKEND              │                             │
│   │   (What runs behind          │                             │
│   │    the scenes)               │                             │
│   │                              │                             │
│   │   ┌───────────────────┐      │                             │
│   │   │  APPLICATION      │      │                             │
│   │   │  (Your code/app)  │      │                             │
│   │   └───────┬───────────┘      │                             │
│   │           │                  │                             │
│   │   ┌───────▼───────────┐      │                             │
│   │   │  MIDDLEWARE        │      │                             │
│   │   │  (Load Balancer,   │      │                             │
│   │   │   API Gateway)     │      │                             │
│   │   └───────┬───────────┘      │                             │
│   │           │                  │                             │
│   │   ┌───────▼───────────┐      │                             │
│   │   │  INFRASTRUCTURE    │      │                             │
│   │   │  - Servers (VMs)  │      │                             │
│   │   │  - Storage        │      │                             │
│   │   │  - Networking     │      │                             │
│   │   │  - Databases      │      │                             │
│   │   └───────────────────┘      │                             │
│   └──────────────────────────────┘                             │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

## 📌 Frontend (Client Side)

The **frontend** is everything the **user interacts with** to access cloud services.

### Components:

| Component | What It Is | Example |
|-----------|-----------|---------|
| **Web Browser** | You use Chrome/Firefox to access cloud services | Opening Gmail in Chrome |
| **Mobile App** | Apps on your phone that connect to cloud | Using Google Drive app |
| **Desktop App** | Software on your computer that uses cloud | VS Code with GitHub integration |
| **Cloud Console** | Dashboard where you manage cloud resources | AWS Console, Azure Portal |
| **CLI (Command Line)** | Terminal/command prompt to interact with cloud | Using `aws` or `gcloud` commands |

> **Simple way to remember:** Frontend = The **"face"** of cloud that you see and touch.

---

## 📌 Backend (Server Side)

The **backend** is everything that runs **behind the scenes** — the actual servers, storage, and networking that power the cloud.

### Three Main Backend Components:

---

### 1. 🖥️ Servers (Compute)

**What are servers?**
- Powerful computers that **process your requests**
- When you open a website, a server sends you that page
- In cloud, these are called **Virtual Machines (VMs)** — virtual computers running inside physical machines

**How it works:**
```
One Physical Server (Real Machine)
┌──────────────────────────────────────┐
│  ┌─────────┐ ┌─────────┐ ┌────────┐ │
│  │  VM 1   │ │  VM 2   │ │  VM 3  │ │
│  │(User A) │ │(User B) │ │(User C)│ │
│  └─────────┘ └─────────┘ └────────┘ │
│                                      │
│  Each VM acts like a separate        │
│  computer, but they all share        │
│  the same physical machine!          │
└──────────────────────────────────────┘
```

**Cloud Examples:**
- **AWS EC2** — Amazon's virtual servers
- **Azure Virtual Machines** — Microsoft's virtual servers
- **GCP Compute Engine** — Google's virtual servers

---

### 2. 💾 Storage

**What is cloud storage?**
- A place to **save files, images, videos, databases** on the cloud
- You don't need your own hard drives — cloud provider gives you storage space

**Types of Cloud Storage:**

| Type | What It Stores | Example |
|------|---------------|---------|
| **Object Storage** | Files, images, videos, backups | AWS S3, Google Cloud Storage |
| **Block Storage** | Hard drive for VMs (like C: drive) | AWS EBS, Azure Managed Disks |
| **File Storage** | Shared folders (like network drive) | AWS EFS, Azure Files |

**Example:**
> When you upload a photo to **Google Photos**, it's stored in Google's **object storage**. You can access it from any device because it's on the cloud!

---

### 3. 🌐 Networking

**What is cloud networking?**
- The **roads and highways** that connect everything together
- It makes sure data travels from the user to the server and back

**Key Networking Components:**

| Component | What It Does | Simple Analogy |
|-----------|-------------|---------------|
| **VPC (Virtual Private Cloud)** | Your own private network in the cloud | Your private room in a hotel |
| **Load Balancer** | Distributes traffic across multiple servers | Traffic police at a busy crossing |
| **CDN (Content Delivery Network)** | Puts copies of your content closer to users | Having food delivery kitchens in every city |
| **DNS (Domain Name System)** | Converts website names to IP addresses | Phone directory (name → number) |
| **Firewall** | Blocks unauthorized access | Security guard at the gate |

**How Networking Works (Simplified):**

```
User types "www.example.com"
        │
        ▼
   ┌─────────┐
   │   DNS   │ → Converts name to IP address (e.g., 52.86.143.12)
   └────┬────┘
        │
        ▼
   ┌──────────┐
   │ Firewall │ → Checks: Is this request safe?
   └────┬─────┘
        │
        ▼
   ┌───────────────┐
   │ Load Balancer │ → Sends request to the least busy server
   └───────┬───────┘
        │
        ▼
   ┌──────────┐
   │  Server  │ → Processes request, sends back the webpage
   └──────────┘
```

---

## 📌 How All Parts Work Together

Here's a **complete flow** of what happens when you use a cloud app:

### Example: You open Instagram

```
Step 1: You open Instagram app (FRONTEND)
           │
Step 2: App sends request over Internet
           │
Step 3: Request hits the LOAD BALANCER (NETWORKING)
           │
Step 4: Load Balancer sends it to an available SERVER (COMPUTE)
           │
Step 5: Server gets your photos from STORAGE
           │
Step 6: Server gets your profile from DATABASE
           │
Step 7: Server sends everything back through the Internet
           │
Step 8: Instagram app displays your feed (FRONTEND)
```

**Total time:** Less than 1 second! ⚡

---

## 📌 Layers of Cloud Architecture

```
┌────────────────────────────────────────────┐
│          LAYER 4: APPLICATION              │
│  (Your code: websites, apps, APIs)         │
├────────────────────────────────────────────┤
│          LAYER 3: PLATFORM                 │
│  (Runtime, frameworks, databases)          │
├────────────────────────────────────────────┤
│          LAYER 2: INFRASTRUCTURE           │
│  (VMs, storage, networking)                │
├────────────────────────────────────────────┤
│          LAYER 1: PHYSICAL HARDWARE        │
│  (Actual servers in data centers)          │
│  (Managed by cloud provider)              │
└────────────────────────────────────────────┘
```

---

## 🧠 Quick Revision (Interview Ready)

- **Cloud Architecture** has 2 main parts: **Frontend** (user interface) and **Backend** (servers, storage, networking)
- **Frontend** = Browser, mobile app, CLI, cloud console
- **Backend** has 3 key components:
  - **Servers (Compute)** — VMs that run your apps (e.g., AWS EC2)
  - **Storage** — Save files and data (e.g., AWS S3)
  - **Networking** — Connects everything (VPC, Load Balancer, CDN, DNS, Firewall)
- **Virtual Machines (VMs)** = Virtual computers running on shared physical hardware
- Everything is connected through the **internet** using **APIs and HTTPS**

---

> 📁 **Next:** [Deployment Models & Service Models →](./07_Deployment_and_Service_Models.md)
