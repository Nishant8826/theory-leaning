# S3 Storage Classes, Lifecycle Policies & RDS Introduction

This note covers S3's seven storage classes, lifecycle management for automatic cost optimization, bucket configuration essentials (versioning, encryption, object lock), architecture diagramming with draw.io, and a preview of Amazon RDS.

---

## 1. S3 Storage Classes Overview

### What (Definition)
S3 Storage Classes are **different tiers of storage** offered by AWS, each designed for a specific data access pattern. Think of them as choosing between a **filing cabinet on your desk** (fast access, expensive) vs. a **warehouse across town** (slow access, cheap).

AWS offers **7 storage classes**:
1. S3 Standard
2. S3 Intelligent-Tiering
3. S3 Standard-IA (Infrequent Access)
4. S3 One Zone-IA
5. S3 Glacier Instant Retrieval
6. S3 Glacier Flexible Retrieval
7. S3 Glacier Deep Archive

### Why (Purpose / Need)
Not all data is accessed equally. Your app's homepage images are loaded millions of times daily (**hot data**), while a 3-year-old audit report might never be opened again (**cold data**). Paying premium storage prices for cold data is **wasteful**. Storage classes let you **match cost to usage**.

### How (Step-by-step Working)
1. When you upload an object to S3, you pick a storage class (default is **Standard**).
2. Each class has its own **pricing**, **retrieval time**, and **availability guarantees**.
3. You can change the class later manually or automatically via **Lifecycle Policies**.

### Impact (Real-world Importance)
- **Using it**: A company storing 100 TB of logs can save **up to 90% in storage costs** by moving old logs to Glacier Deep Archive.
- **Not using it**: You pay **Standard prices for everything**, even data nobody touches — burning money every month.

---

## 2. Deep Dive: Each Storage Class

### 2.1 S3 Standard

| Property | Detail |
| :--- | :--- |
| **Use Case** | Frequently accessed data (hot data) |
| **Availability Zones** | Data replicated across **3 AZs** |
| **Retrieval Time** | Instant (milliseconds) |
| **Durability** | 99.999999999% (11 nines) |
| **Availability** | 99.99% |
| **Cost** | Highest storage cost, lowest access cost |

**Best For**: Website assets, active application data, content distribution, gaming assets.

---

### 2.2 S3 Intelligent-Tiering

| Property | Detail |
| :--- | :--- |
| **Use Case** | Data with **unknown or changing** access patterns |
| **How it Works** | Automatically moves objects between tiers based on access patterns |
| **Availability Zones** | 3 AZs |
| **Monitoring Fee** | Small monthly per-object monitoring fee |
| **Retrieval Time** | Instant for frequent/infrequent tiers; minutes–hours for archive tiers |

**How Intelligent-Tiering Decides:**
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

**Best For**: Data lakes, analytics datasets, user-generated content where access patterns are unpredictable.

---

### 2.3 S3 One Zone-IA (Infrequent Access)

| Property | Detail |
| :--- | :--- |
| **Use Case** | Infrequently accessed data that can be **recreated** if lost |
| **Availability Zones** | **1 AZ only** (single point of failure) |
| **Cost** | About **one-third** the cost of S3 Standard |
| **Retrieval Time** | Instant (milliseconds) |
| **Risk** | If that AZ is destroyed, your data is **gone forever** |

**Best For**: Secondary backups, data you can regenerate (thumbnails, transcoded media), dev/test environments.

> ⚠️ **Warning**: Never store your **only copy** of critical data here. If the single AZ goes down (earthquake, fire, flood), you lose everything.

---

### 2.4 S3 Glacier Variants

| Property | Glacier Instant Retrieval | Glacier Flexible Retrieval | Glacier Deep Archive |
| :--- | :--- | :--- | :--- |
| **Use Case** | Archives accessed ~once per quarter | Archives accessed ~1-2 times per year | Archives accessed once every 2-5 years |
| **Retrieval Time** | Milliseconds | Minutes to 12 hours | 12 to 48 hours |
| **Cost (vs Standard)** | ~68% cheaper | ~90% cheaper | ~95% cheaper (**one-tenth** of Standard) |
| **Min Storage Duration** | 90 days | 90 days | 180 days |
| **AZs** | 3 AZs | 3 AZs | 3 AZs |

**Glacier Retrieval Speed Options (Flexible Retrieval):**

| Speed | Time | Cost |
| :--- | :--- | :--- |
| **Expedited** | 1-5 minutes | Most expensive |
| **Standard** | 3-5 hours | Moderate |
| **Bulk** | 5-12 hours | Cheapest |

**Best For**:
- **Glacier Instant**: Medical records, news media archives (need quick access but rarely)
- **Glacier Flexible**: Disaster recovery, yearly compliance audits
- **Deep Archive**: Regulatory data (banking/healthcare records kept for 7+ years), historical research data

---

### Complete Storage Class Comparison

```text
 HOT DATA ◄──────────────────────────────────────────────► COLD DATA
 (accessed constantly)                          (accessed almost never)

 ┌──────────┐  ┌──────────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐
 │ Standard │  │ Intelligent  │  │ One Zone │  │ Glacier  │  │ Deep Archive │
 │          │  │  Tiering     │  │   IA     │  │ Variants │  │              │
 │ 3 AZs    │  │ Auto-moves   │  │ 1 AZ     │  │ 3 AZs    │  │ 3 AZs        │
 │ $$$$     │  │ $$ - $$$$    │  │ $        │  │ $ - $$   │  │ ¢            │
 │ Instant  │  │ Instant*     │  │ Instant  │  │ Min-Hrs  │  │ 12-48 Hrs    │
 └──────────┘  └──────────────┘  └──────────┘  └──────────┘  └──────────────┘

 $$$$ = Most Expensive Storage     ¢ = Cheapest Storage
 * = Retrieval time depends on which internal tier the object is currently in
```

---

## 3. S3 Lifecycle Management

### What (Definition)
Lifecycle Management lets you create **rules** that automatically transition objects between storage classes or **delete** them after a specified number of days. Think of it as setting up an **autopilot for your data's journey from expensive to cheap storage and finally to deletion**.

### Why (Purpose / Need)
Imagine a bank that generates thousands of transaction records daily. Regulations require keeping them for years, but nobody queries 3-year-old records regularly. Without lifecycle rules, someone would manually move terabytes of data every month — **tedious, error-prone, and expensive**.

### How (Step-by-step Working)
1. Go to your S3 bucket → **Management** tab → **Lifecycle rules**.
2. Click **Create lifecycle rule**.
3. Define a **rule name** and scope (entire bucket or specific prefix/tag).
4. Set **transitions**: e.g., "After 90 days, move to Glacier Instant Retrieval."
5. Set **expiration**: e.g., "After 1500 days, permanently delete."
6. Save the rule. AWS handles everything automatically from now on.

### Impact (Real-world Importance)
- **Using it**: Set-and-forget cost optimization. Data flows to cheaper tiers automatically.
- **Not using it**: Manual management overhead, accidental overspending, human errors (forgetting to move data), and compliance violations (forgetting to delete data on time).

### Real-World Example: Banking Data Lifecycle

```text
 DAY 0                    DAY 90                  DAY 1000                DAY 1500
   │                        │                        │                       │
   ▼                        ▼                        ▼                       ▼
┌──────────────┐    ┌──────────────────────┐   ┌──────────────┐      ┌────────────┐
│  S3 Standard │───►│ Glacier Instant      │──►│ Glacier Deep │─────►│  DELETED   │
│              │    │ Retrieval            │   │ Archive      │      │            │
│ Active use   │    │ Rarely accessed      │   │ Compliance   │      │ Regulation │
│ by employees │    │ but may need quick   │   │ storage only │      │ period     │
│              │    │ access for audits    │   │              │      │ expired    │
└──────────────┘    └──────────────────────┘   └──────────────┘      └────────────┘

 Cost: $$$$           Cost: $$                  Cost: ¢               Cost: $0
```

### How to Create a Lifecycle Rule (Console Walkthrough)

| Step | Action | Detail |
| :--- | :--- | :--- |
| 1 | Open S3 Console | Navigate to the target bucket |
| 2 | Go to Management tab | Click **Lifecycle rules** |
| 3 | Create rule | Name it (e.g., `banking-data-lifecycle`) |
| 4 | Choose scope | Apply to entire bucket or filter by prefix (`logs/`, `transactions/`) |
| 5 | Add transition #1 | Move to **Glacier Instant Retrieval** after **90 days** |
| 6 | Add transition #2 | Move to **Glacier Deep Archive** after **1000 days** |
| 7 | Add expiration | **Delete** objects after **1500 days** |
| 8 | Review & save | Confirm and enable the rule |

### Important Lifecycle Rules Constraints
- You **cannot** transition directly from Standard to Deep Archive skipping Glacier (must follow the tier order or use specific allowed transitions).
- **Minimum storage duration** charges apply — if you move an object out of Glacier before 90 days, you still pay for 90 days.
- Lifecycle rules apply to **new and existing** objects in the bucket.

---

## 4. S3 Bucket Configuration

### 4.1 Versioning

#### What
Versioning keeps **every version** of every object you upload. When you re-upload a file with the same name, S3 doesn't overwrite it — it stores both the old and new versions.

#### Why
In production environments, accidental overwrite or deletion of a config file can bring an entire system down. Versioning acts as your **safety net**.

#### How
1. Open your bucket → **Properties** tab.
2. Click **Edit** under **Bucket Versioning**.
3. Select **Enable** → Save.
4. Now every upload creates a new version with a unique **Version ID**.

#### Impact
- **Enabled**: You can recover from accidental deletes (just remove the "Delete Marker"), roll back to any previous version.
- **Disabled**: One wrong upload, and the old file is gone forever.

```text
Upload "config.json" (v1) ──► Upload "config.json" (v2) ──► Delete "config.json"

    Without Versioning:
    config.json → OVERWRITTEN → GONE FOREVER ❌

    With Versioning:
    ┌─────────────────────────────────────────────┐
    │ Version ID: abc123  │ config.json (v1)      │ ✅ Still exists
    │ Version ID: def456  │ config.json (v2)      │ ✅ Still exists
    │ Version ID: ghi789  │ Delete Marker         │ ← Can be removed to restore
    └─────────────────────────────────────────────┘
```

> **Note**: Enabling versioning **increases storage costs** because every version takes up space. Combine with lifecycle rules to expire old versions automatically.

---

### 4.2 Encryption

#### What
S3 Encryption ensures your data is **scrambled** while stored on AWS servers, so even if someone gains physical access to the disk, they can't read your data.

#### Why
Compliance regulations (HIPAA, GDPR, PCI-DSS) **mandate** data encryption at rest. Even without regulations, it's a fundamental security best practice.

#### How (3 Options)

| Encryption Type | Full Name | Who Manages the Key? | When to Use |
| :--- | :--- | :--- | :--- |
| **SSE-S3** | Server-Side Encryption with S3-Managed Keys | **AWS** manages everything | Default, simplest option |
| **SSE-KMS** | Server-Side Encryption with AWS KMS | **You** control keys via KMS | When you need audit trails (who used the key, when) |
| **DSSE-KMS** | Dual-layer Server-Side Encryption with KMS | **You** control keys, data encrypted **twice** | Highest security requirements (government, military) |

```text
┌─────────────────────────────────────────────────────────────┐
│                    ENCRYPTION COMPARISON                    │
├─────────────┬──────────────┬──────────────┬─────────────────┤
│             │   SSE-S3     │   SSE-KMS    │   DSSE-KMS      │
├─────────────┼──────────────┼──────────────┼─────────────────┤
│ Complexity  │   Low        │   Medium     │   High          │
│ Key Control │   None       │   Full       │   Full          │
│ Audit Trail │   No         │   Yes (CT)   │   Yes (CT)      │
│ Encryption  │   Single     │   Single     │   Double        │
│ Cost        │   Free       │   KMS fees   │   KMS fees ×2   │
└─────────────┴──────────────┴──────────────┴─────────────────┘

CT = AWS CloudTrail logs every key usage
```

#### Impact
- **Using it**: Data at rest is protected. Compliance requirements met. Even AWS employees can't read your data.
- **Not using it**: One data breach = lawsuits, fines, customer trust destroyed.

---

### 4.3 Object Lock

#### What
Object Lock prevents objects from being **deleted or overwritten** for a defined period. Once locked, not even the root account can delete the data until the lock expires.

#### Why
Regulatory requirements (like SEC Rule 17a-4 for financial records) mandate that certain data be stored in a **WORM** (Write Once, Read Many) format — meaning once written, it cannot be changed or deleted.

#### How
1. Object Lock must be enabled **at bucket creation** (cannot be added later).
2. Choose a retention mode:
   - **Governance Mode**: Only users with special permissions can delete.
   - **Compliance Mode**: **Nobody** can delete, not even root — until retention period expires.
3. Set a **retention period** (e.g., 365 days).

#### Impact
- **Using it**: Guaranteed data immutability for compliance. Protection against ransomware (attackers can't delete backups).
- **Not using it**: A disgruntled employee or hacker could delete critical backups.

---

### 4.4 Bucket Naming Rules

| Rule | Detail |
| :--- | :--- |
| **Globally Unique** | No two buckets in the world can share a name |
| **3-63 characters** | Must be between 3 and 63 characters long |
| **Lowercase only** | No uppercase letters allowed |
| **No underscores** | Hyphens `-` are allowed, underscores `_` are not |
| **Cannot be changed** | Once created, the name is **permanent** |
| **Start with letter/number** | Cannot start with a hyphen |

> ⚠️ **Important**: Choose bucket names carefully! Since they can never be changed, many teams include the environment and project name: `prod-myapp-media-2026`

---

## 5. Architecture Diagrams with draw.io

### What (Definition)
**draw.io** (also called **diagrams.net**) is a free, open-source tool for creating professional architecture diagrams. It comes with built-in AWS icon libraries to draw cloud infrastructure visually.

### Why (Purpose / Need)
In DevOps, you constantly need to communicate your infrastructure to team members, managers, and clients. A well-drawn diagram **replaces pages of documentation** and makes complex systems understandable at a glance.

### How (Step-by-step Working)
1. Go to [draw.io](https://app.diagrams.net/) or install the VS Code extension.
2. Click **Create New Diagram** → Choose **Blank** or an **AWS template**.
3. On the left panel, search for **AWS** icons (S3, EC2, VPC, etc.).
4. Drag and drop components onto the canvas.
5. Connect them with arrows to show data flow.
6. Export as **PNG**, **SVG**, or **PDF**.

### Impact (Real-world Importance)
- **Using it**: Clear communication, faster onboarding of new team members, better documentation.
- **Not using it**: Miscommunication, confusion about infrastructure, longer meetings explaining setups verbally.

### Sample S3 Architecture Diagram (ASCII)

```text
┌──────────────────────────────────────────────────────────────────┐
│                        AWS CLOUD                                 │
│                                                                  │
│  ┌──────────┐      ┌────────────────────────────────────────┐    │
│  │  Users   │      │         S3 Bucket: prod-app-data       │    │
│  │ (Browser)│─────►│                                        │    │
│  └──────────┘      │  ┌──────────┐  ┌──────────────────┐    │    │
│                    │  │index.html│  │  /images/        │    │    │
│                    │  │style.css │  │  logo.png        │    │    │
│                    │  │app.js    │  │  banner.jpg      │    │    │
│                    │  └──────────┘  └──────────────────┘    │    │
│                    │                                        │    │
│                    │  Configuration:                        │    │
│                    │  ├── Versioning: ENABLED               │    │
│                    │  ├── Encryption: SSE-KMS               │    │
│                    │  ├── Object Lock: Compliance Mode      │    │
│                    │  └── Lifecycle: Standard → Glacier     │    │
│                    └────────────────────────────────────────┘    │
│                              │                                   │
│                     ┌────────▼───────┐                           │
│                     │  Replication   │                           │
│                     │  across 3 AZs  │                           │
│                     ├────┬────┬──────┤                           │
│                     │AZ-1│AZ-2│AZ-3  │                           │
│                     └────┴────┴──────┘                           │
└──────────────────────────────────────────────────────────────────┘
```

---

## 6. Amazon RDS (Relational Database Service) — Preview

### What (Definition)
Amazon RDS is a **managed relational database service** that makes it easy to set up, operate, and scale databases in the cloud. Instead of manually installing MySQL on an EC2 instance, RDS handles patches, backups, and scaling for you.

### Why (Purpose / Need)
Managing a database is hard — you need to handle installation, security patches, backups, replication, failover, and scaling. RDS takes over **all the heavy lifting** so developers can focus on writing queries, not managing servers.

### How (Step-by-step Working)
1. Go to AWS Console → **RDS** → **Create Database**.
2. Choose a database engine (MySQL, PostgreSQL, Oracle, SQL Server, MariaDB, or Aurora).
3. Select instance size (CPU, RAM) and storage type.
4. Configure networking (VPC, security groups).
5. Set credentials (master username and password).
6. AWS launches and manages the database for you.

### Impact (Real-world Importance)
- **Using it**: Automated backups, patching, scaling, and high availability. You focus on your app, not infrastructure.
- **Not using it**: You manually install the database on EC2, handle all updates yourself, risk data loss if you misconfigure backups.

### Supported Database Engines

| Engine | Key Strengths | Popularity |
| :--- | :--- | :--- |
| **MySQL** | Open-source, widely supported, huge community | ⭐ Most popular for beginners |
| **PostgreSQL** | Advanced features, complex queries, extensions | ⭐ Popular in startups |
| **Oracle** | Enterprise-grade, powerful, legacy systems | Common in banks/enterprises |
| **SQL Server** | Microsoft ecosystem, .NET integration | Common in Windows environments |
| **MariaDB** | MySQL fork, open-source, performance improvements | Growing adoption |
| **Aurora** | AWS proprietary, 5x faster than MySQL, auto-scaling | Best performance on AWS |

### ASCII Diagram: RDS vs Self-Managed DB

```text
┌──────────────────────────────────────────────────────────────────┐
│                     SELF-MANAGED (on EC2)                         │
│                                                                  │
│  YOU handle:  Installation │ Patching │ Backups │ Scaling │ HA   │
│               ──────────── │ ──────── │ ─────── │ ─────── │ ──   │
│                   😰           😰         😰        😰       😰  │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│                     AWS RDS (Managed)                             │
│                                                                  │
│  AWS handles: Installation │ Patching │ Backups │ Scaling │ HA   │
│               ──────────── │ ──────── │ ─────── │ ─────── │ ──   │
│                   ✅           ✅         ✅        ✅       ✅  │
│                                                                  │
│  YOU handle:  Schema design │ Queries │ App logic                │
│               ────────────── │ ─────── │ ─────────               │
│                   💻            💻         💻                    │
└──────────────────────────────────────────────────────────────────┘
```

### 5 Key Points About MySQL (Most Important to Learn)
1. **Open Source** — Free to use, massive community support, and abundantly available documentation.
2. **RDBMS** — Relational Database Management System; stores data in structured **tables** with rows and columns, linked by relationships (foreign keys).
3. **SQL Language** — Uses Structured Query Language for CRUD operations (`SELECT`, `INSERT`, `UPDATE`, `DELETE`).
4. **ACID Compliant** — Guarantees **Atomicity, Consistency, Isolation, Durability** ensuring reliable transactions (critical for banking, e-commerce).
5. **Replication & Scaling** — Supports **Master-Slave replication** for read scaling and high availability.

---

## 7. Scenario-Based Q&A

🔍 **Scenario 1**: Your company stores customer invoices. They're accessed frequently for the first 3 months, then rarely for 2 years, and must be deleted after 5 years per regulations.
✅ **Answer**: Create a lifecycle rule:
- Days 0–90: **S3 Standard** (frequent access)
- Day 90: Transition to **Glacier Instant Retrieval** (rare but quick access needed for audits)
- Day 730 (2 years): Transition to **Glacier Deep Archive** (cheapest, almost never accessed)
- Day 1825 (5 years): **Expiration** — auto-delete. This ensures compliance and minimizes cost.

---

🔍 **Scenario 2**: A developer accidentally uploaded a broken `config.json` to the production S3 bucket, and the application is crashing.
✅ **Answer**: If **Versioning is enabled**, go to the S3 bucket, toggle "Show Versions," find the previous working version of `config.json`, and restore it. This fix takes seconds. If versioning was NOT enabled, the old file is permanently gone, and you'd need a backup from elsewhere.

---

🔍 **Scenario 3**: Your startup stores user-uploaded profile pictures. Access patterns are unpredictable — some users are active, others abandoned their accounts years ago.
✅ **Answer**: Use **S3 Intelligent-Tiering**. It will automatically move rarely-accessed profile pictures to cheaper tiers and bring them back up instantly when accessed. No manual intervention or guessing required.

---

🔍 **Scenario 4**: You need to store 50 TB of thumbnail images that can be regenerated from the originals if lost. Budget is tight.
✅ **Answer**: Use **S3 One Zone-IA**. It costs about one-third of Standard, and since the thumbnails can be regenerated, losing them in a rare AZ failure is an acceptable risk.

---

🔍 **Scenario 5**: A government auditor demands that all financial records from 2020 must NOT be deletable under any circumstances for the next 7 years.
✅ **Answer**: Enable **Object Lock** in **Compliance Mode** with a 7-year retention period. Even the AWS root account cannot delete these records until the lock expires. This satisfies regulatory requirements like SEC 17a-4.

---

🔍 **Scenario 6**: Your team is confused about the infrastructure setup. Different team members describe it differently, leading to deployment errors.
✅ **Answer**: Create a clear **architecture diagram using draw.io** with AWS icons showing all services, their connections, and data flows. Share it in the team wiki. Update it whenever infrastructure changes.

---

## 8. Interview Questions & Answers

### Q1: How many S3 storage classes are there? Name them.
**A**: There are **7 storage classes**:
1. S3 Standard
2. S3 Intelligent-Tiering
3. S3 Standard-IA
4. S3 One Zone-IA
5. S3 Glacier Instant Retrieval
6. S3 Glacier Flexible Retrieval
7. S3 Glacier Deep Archive

---

### Q2: What is the difference between S3 Standard and One Zone-IA?
**A**: S3 Standard stores data across **3 Availability Zones** (high durability + availability) and is for frequently accessed data. One Zone-IA stores data in **only 1 AZ** (cheaper, about one-third the cost) but if that AZ goes down, the data is **lost permanently**. One Zone-IA is best for data that can be recreated.

---

### Q3: Explain S3 Lifecycle Policies with a real-world example.
**A**: Lifecycle policies automate data transitions between storage classes and handle deletion. **Example**: A hospital stores patient records in S3 Standard for active use. After 90 days, the lifecycle rule moves them to Glacier Instant Retrieval (cheaper, quick access for audits). After 7 years, records are automatically deleted per HIPAA guidelines. This eliminates manual data management entirely.

---

### Q4: What are the three encryption options in S3? When would you choose SSE-KMS over SSE-S3?
**A**: The three options are **SSE-S3**, **SSE-KMS**, and **DSSE-KMS**. You'd choose SSE-KMS over SSE-S3 when you need:
- **Key rotation control** (you decide when keys are rotated)
- **Audit trails** via CloudTrail (who accessed which key, when)
- **Granular permissions** (restrict specific users from decrypting)
SSE-S3 is simpler but gives you zero control over key management.

---

### Q5: What is Object Lock, and what's the difference between Governance and Compliance modes?
**A**: Object Lock prevents objects from being deleted or overwritten (WORM model).
- **Governance Mode**: Most users can't delete, but users with special IAM permissions (`s3:BypassGovernanceRetention`) can override the lock.
- **Compliance Mode**: **Nobody** can delete the data — not even the root account — until the retention period expires. It's irreversible.

---

### Q6: Can you change an S3 bucket's name after creation?
**A**: **No.** S3 bucket names are **permanent**. If you need a different name, you must create a new bucket with the desired name, copy all objects over, and delete the old bucket.

---

### Q7: What is Amazon RDS, and how is it different from installing MySQL on EC2?
**A**: RDS is a **managed database service** where AWS handles installation, patching, backups, scaling, and high availability. On EC2, you install MySQL yourself and manage everything manually. RDS saves significant operational overhead but costs slightly more. It's ideal for teams that want to focus on application development rather than database administration.

---

### Q8: What retrieval options does Glacier Flexible Retrieval offer, and when would you use each?
**A**: Three options:
- **Expedited** (1-5 minutes): Emergency access to archived data. Costs the most.
- **Standard** (3-5 hours): Normal retrieval for planned data access. Moderate cost.
- **Bulk** (5-12 hours): Large-scale retrieval of big datasets at the lowest cost.

**Use case**: If a legal team urgently needs a specific archived document for court → **Expedited**. If running a quarterly compliance audit → **Standard**. If migrating archived data to another system → **Bulk**.

---

### Q9: What is Intelligent-Tiering, and does it charge retrieval fees?
**A**: Intelligent-Tiering automatically moves objects between access tiers based on usage patterns. It charges a **small monthly monitoring fee per object** but does **NOT** charge retrieval fees when objects move between tiers. This makes it ideal for data with unpredictable access patterns — you get cost savings without the risk of retrieval fees.

---

### Q10: A client says "We need to keep financial records for 7 years but minimize costs." What S3 strategy would you recommend?
**A**: I'd recommend:
1. Store in **S3 Standard** for the first 90 days (active access)
2. Lifecycle rule to **Glacier Instant Retrieval** after 90 days (occasional audit access)
3. Lifecycle rule to **Glacier Deep Archive** after 1 year (cheapest storage, rarely accessed)
4. **Object Lock in Compliance Mode** with 7-year retention (prevents any deletion)
5. Automatic **expiration** after 2,555 days (7 years) to clean up

This strategy ensures regulatory compliance while minimizing storage costs by up to 95%.

---

← Previous: [`16_aws-s3-static-website-hosting.md`](16_aws-s3-static-website-hosting.md) | Next: [`18_TBD.md`](18_TBD.md) →
