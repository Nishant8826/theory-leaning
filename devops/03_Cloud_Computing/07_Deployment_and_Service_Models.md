# 📦 Deployment Models & Service Models

---

## Part 1: Deployment Models

Deployment models describe **WHERE** the cloud infrastructure is located and **WHO** can use it.

---

### 📌 1. Public Cloud

| Aspect | Details |
|--------|---------|
| **What** | Cloud resources shared among multiple companies/users |
| **Who manages** | Cloud provider (AWS, Azure, GCP) |
| **Who uses** | Anyone — open to the public |
| **Cost** | Low — pay-as-you-go |
| **Security** | Good, but shared environment |
| **Example** | Hosting your website on AWS |

> **Analogy:** Like a **co-working space**. You rent a desk, share the building, and someone else manages cleaning, electricity, and WiFi.

---

### 📌 2. Private Cloud

| Aspect | Details |
|--------|---------|
| **What** | Cloud used by ONE organization only |
| **Who manages** | The organization itself or a private provider |
| **Who uses** | Only that organization's employees |
| **Cost** | High — you maintain everything |
| **Security** | Highest — full control |
| **Example** | A bank running its own cloud for customer data |

> **Analogy:** Like **owning your own office building**. Only your employees can enter. You control everything.

---

### 📌 3. Hybrid Cloud

| Aspect | Details |
|--------|---------|
| **What** | Mix of public + private cloud |
| **Who manages** | Combination — some by you, some by provider |
| **Cost** | Medium |
| **Security** | Sensitive data stays private, rest goes public |
| **Example** | Hospital: Patient records on private, website on public |

> **Analogy:** Like having a **home office + co-working membership**. Sensitive work at home, meetings at co-working space.

---

### Deployment Models Comparison

```
┌──────────┬──────────────┬────────────────┐
│  PUBLIC  │   PRIVATE    │     HYBRID     │
├──────────┼──────────────┼────────────────┤
│ Shared   │ Dedicated    │ Mix of both    │
│ Low cost │ High cost    │ Medium cost    │
│ Less     │ Full         │ Balanced       │
│ control  │ control      │ control        │
│ AWS,     │ VMware,      │ AWS + On-prem  │
│ Azure    │ OpenStack    │ Azure + DC     │
└──────────┴──────────────┴────────────────┘
```

---

## Part 2: Service Models (IaaS, PaaS, SaaS)

Service models describe **WHAT** the cloud provider manages for you.

---

### The Pizza Analogy 🍕

```
Make at Home    Take & Bake     Pizza Delivery    Dine-In
(On-Premise)     (IaaS)           (PaaS)          (SaaS)

You do          They give        They make &      They do
EVERYTHING      dough, you       deliver the      EVERYTHING
yourself        bake it          pizza            for you
```

---

### 📌 1. IaaS (Infrastructure as a Service)

- **You get:** Servers (VMs), storage, networking
- **You manage:** OS, software, apps, data
- **Provider manages:** Physical hardware, virtualization
- **Examples:** AWS EC2, Azure VMs, GCP Compute Engine

> **Example:** You rent a VM on AWS. AWS gives you the machine. YOU install Ubuntu, Node.js, and deploy your website.

**Best for:** IT admins, DevOps engineers, companies wanting full control

---

### 📌 2. PaaS (Platform as a Service)

- **You get:** Everything in IaaS + OS + runtime + middleware
- **You manage:** Only your application code and data
- **Provider manages:** Servers, OS, runtime, scaling
- **Examples:** Heroku, AWS Elastic Beanstalk, Azure App Service, GCP App Engine

> **Example:** You push your Python code to Heroku. Heroku handles the server setup, Python installation, scaling — everything except your code.

**Best for:** Developers, startups, small teams wanting to focus on code

---

### 📌 3. SaaS (Software as a Service)

- **You get:** Complete, ready-to-use application
- **You manage:** Only your data within the app
- **Provider manages:** Everything!
- **Examples:** Gmail, Slack, Zoom, Google Docs, Salesforce, Netflix

> **Example:** You open Gmail. You don't install anything or manage servers. Google does everything. You just write emails. That's SaaS!

**Best for:** Everyone — regular users, businesses, students

---

### 📌 Who Manages What? (Visual)

```
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

---

### 📌 IaaS vs PaaS vs SaaS — Comparison Table

| Feature | IaaS | PaaS | SaaS |
|---------|------|------|------|
| **What you get** | Raw infrastructure | Platform to build apps | Ready-to-use software |
| **You manage** | OS, apps, data | Only apps and data | Only your data |
| **Provider manages** | Hardware, networking | Hardware + OS + runtime | Everything |
| **Control** | High | Medium | Low |
| **Skill needed** | High (DevOps) | Medium (Developer) | Low (Anyone) |
| **Example** | AWS EC2 | Heroku | Gmail, Zoom |
| **Pizza analogy** | Take & bake | Pizza delivery | Dine-in restaurant |

---

## 🧠 Quick Revision (Interview Ready)

**Deployment Models:**
- **Public** → Shared, cheap, AWS/Azure/GCP
- **Private** → Dedicated, expensive, full control
- **Hybrid** → Mix of both

**Service Models:**
- **IaaS** → Rent infrastructure, you manage OS + apps (EC2)
- **PaaS** → Rent platform, just push code (Heroku)
- **SaaS** → Use ready software (Gmail, Zoom)
- As you go IaaS → PaaS → SaaS: you manage **less**, provider manages **more**

---

> 📁 **Next:** [How Cloud Computing Works →](./08_How_Cloud_Works.md)
