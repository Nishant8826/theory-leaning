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

### S3 Storage Classes Architecture Diagram (ASCII)

```text
┌─────────────────────────────────────────────────────────────────────────────────┐
│                            AWS S3 STORAGE ARCHITECTURE                          │
│                                                                                 │
│  ┌──────────┐                                                                   │
│  │  Users / │    Upload     ┌───────────────────────────────────────────────┐   │
│  │  Apps /  │──────────────►│          S3 BUCKET: company-data             │   │
│  │  Servers │               │                                               │   │
│  └──────────┘               │  Default Storage Class: S3 STANDARD           │   │
│       ▲                     │  (all new uploads land here)                   │   │
│       │                     └───────────────┬───────────────────────────────┘   │
│       │ GET                                 │                                    │
│       │ (instant)                           │ Lifecycle Rules (automatic)         │
│       │                                     ▼                                    │
│       │            ┌────────────────────────────────────────────────────┐        │
│       │            │              LIFECYCLE TRANSITIONS                  │        │
│       │            │                                                    │        │
│       │            │  ┌──────────────────┐                              │        │
│       │            │  │  S3 STANDARD     │ ◄── Day 0: Upload lands here │        │
│       │            │  │  (Hot Data)      │     3 AZs, instant access    │        │
│       │            │  │  Cost: $$$$      │                              │        │
│       │            │  └────────┬─────────┘                              │        │
│       │            │           │ After 30 days                          │        │
│       │            │           ▼                                        │        │
│       │            │  ┌──────────────────┐                              │        │
│       │            │  │ STANDARD-IA      │  Infrequent but still needs  │        │
│       │            │  │ (Warm Data)      │  fast access when needed     │        │
│       │            │  │ Cost: $$$        │                              │        │
│       │            │  └────────┬─────────┘                              │        │
│       │            │           │ After 90 days                          │        │
│       │            │           ▼                                        │        │
│       │            │  ┌──────────────────┐                              │        │
│       │            │  │ GLACIER INSTANT  │  Archive but may need        │        │
│       │            │  │ (Cold Data)      │  millisecond retrieval       │        │
│       │            │  │ Cost: $$         │                              │        │
│       │            │  └────────┬─────────┘                              │        │
│       │            │           │ After 365 days                         │        │
│       │            │           ▼                                        │        │
│       │            │  ┌──────────────────┐                              │        │
│       │            │  │ GLACIER FLEXIBLE │  Deep archive, retrieval     │        │
│       │            │  │ (Frozen Data)    │  takes minutes to hours      │        │
│       │            │  │ Cost: $          │                              │        │
│       │            │  └────────┬─────────┘                              │        │
│       │            │           │ After 1825 days (5 years)              │        │
│       │            │           ▼                                        │        │
│       │            │  ┌──────────────────┐                              │        │
│       │            │  │ DEEP ARCHIVE     │  Cheapest, retrieval takes   │        │
│       │            │  │ (Ice Cold Data)  │  12-48 hours                 │        │
│       │            │  │ Cost: ¢          │                              │        │
│       │            │  └────────┬─────────┘                              │        │
│       │            │           │ After 2555 days (7 years)              │        │
│       │            │           ▼                                        │        │
│       │            │  ┌──────────────────┐                              │        │
│       │            │  │    🗑️ DELETE     │  Auto-removed per policy     │        │
│       │            │  │  (Expiration)    │                              │        │
│       │            │  └──────────────────┘                              │        │
│       │            └────────────────────────────────────────────────────┘        │
│       │                                                                          │
│       │            ┌────────────────────────────────────────────────────┐        │
│       │            │            SPECIAL STORAGE CLASSES                  │        │
│       │            │                                                    │        │
│       │            │  ┌──────────────────┐   ┌──────────────────────┐  │        │
│       │            │  │ INTELLIGENT-     │   │   ONE ZONE-IA        │  │        │
│       │            │  │ TIERING          │   │                      │  │        │
│       │            │  │                  │   │   Only 1 AZ          │  │        │
│       │            │  │  Auto-moves      │   │   1/3 cost of Std    │  │        │
│       │            │  │  between tiers   │   │   ⚠️ Data loss risk  │  │        │
│       │            │  │  based on access │   │   if AZ goes down    │  │        │
│       │            │  │  patterns        │   │                      │  │        │
│       │            │  │  (no manual      │   │   Best for:          │  │        │
│       │            │  │   intervention)  │   │   Recreatable data   │  │        │
│       │            │  └──────────────────┘   └──────────────────────┘  │        │
│       │            └────────────────────────────────────────────────────┘        │
│       │                                                                          │
│       │  ┌─────────────────────────────────────────────────────────────┐         │
│       └──│                   DATA REPLICATION                          │         │
│          │         ┌───────┐    ┌───────┐    ┌───────┐                │         │
│          │         │ AZ-1  │    │ AZ-2  │    │ AZ-3  │                │         │
│          │         │ Copy  │    │ Copy  │    │ Copy  │                │         │
│          │         └───────┘    └───────┘    └───────┘                │         │
│          │   (Except One Zone-IA which uses only 1 AZ)                │         │
│          └─────────────────────────────────────────────────────────────┘         │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### S3 Request Lifecycle — How a Request is Processed

This diagram shows what happens **step-by-step** when someone tries to access an object in S3 (e.g., a user's browser requests an image).

```text
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                     S3 REQUEST LIFECYCLE (GET Object)                                │
│                                                                                     │
│  STEP 1: DNS Resolution                                                             │
│  ┌──────────┐    "my-bucket.s3.amazonaws.com/logo.png"    ┌──────────┐              │
│  │  Client  │ ──────────────────────────────────────────► │   DNS    │              │
│  │ (Browser/│                                             │  Server  │              │
│  │  App/CLI)│ ◄── IP address of nearest S3 endpoint ──── │          │              │
│  └────┬─────┘                                             └──────────┘              │
│       │                                                                             │
│       │  HTTPS Request (GET /logo.png)                                              │
│       ▼                                                                             │
│  STEP 2: Request Hits S3 Endpoint                                                   │
│  ┌─────────────────────────────────────────────────────────────────────────┐         │
│  │                        AWS S3 ENDPOINT                                  │         │
│  │                                                                         │         │
│  │  ┌─────────────────────────────────────────────────────────────────┐   │         │
│  │  │ STEP 3: Authentication — "WHO are you?"                        │   │         │
│  │  │                                                                 │   │         │
│  │  │  ├── Anonymous request? (no credentials)                       │   │         │
│  │  │  │     → Treated as PUBLIC access                              │   │         │
│  │  │  │                                                             │   │         │
│  │  │  ├── AWS credentials provided? (Access Key / IAM Role / STS)  │   │         │
│  │  │  │     → Validate signature (AWS Signature V4)                │   │         │
│  │  │  │     → Invalid? ──► 403 Forbidden ❌ (STOP)                 │   │         │
│  │  │  │     → Valid? ──► Continue ▼                                 │   │         │
│  │  │  │                                                             │   │         │
│  │  │  └── Pre-signed URL?                                           │   │         │
│  │  │        → Check expiry + signature → Continue if valid ▼        │   │         │
│  │  └─────────────────────────────────────────────────────────────────┘   │         │
│  │                           │                                            │         │
│  │                           ▼                                            │         │
│  │  ┌─────────────────────────────────────────────────────────────────┐   │         │
│  │  │ STEP 4: Authorization — "Are you ALLOWED to do this?"          │   │         │
│  │  │                                                                 │   │         │
│  │  │  CHECK 1: Block Public Access                                  │   │         │
│  │  │  ┌─────────────────────────────────────────────────────┐       │   │         │
│  │  │  │ Is BPA ON + request is public? ──► 403 Denied ❌   │       │   │         │
│  │  │  │ BPA OFF or request is authenticated? ──► Continue ▼ │       │   │         │
│  │  │  └─────────────────────────────────────────────────────┘       │   │         │
│  │  │                           │                                     │   │         │
│  │  │  CHECK 2: Bucket Policy                                        │   │         │
│  │  │  ┌─────────────────────────────────────────────────────┐       │   │         │
│  │  │  │ Explicit DENY found? ──► 403 Denied ❌ (STOP)      │       │   │         │
│  │  │  │ Explicit ALLOW found? ──► Continue ▼                │       │   │         │
│  │  │  │ No match? ──► Check next ▼                          │       │   │         │
│  │  │  └─────────────────────────────────────────────────────┘       │   │         │
│  │  │                           │                                     │   │         │
│  │  │  CHECK 3: ACLs (if enabled)                                    │   │         │
│  │  │  ┌─────────────────────────────────────────────────────┐       │   │         │
│  │  │  │ ACL grants access? ──► Continue ▼                   │       │   │         │
│  │  │  │ No match? ──► Check next ▼                          │       │   │         │
│  │  │  └─────────────────────────────────────────────────────┘       │   │         │
│  │  │                           │                                     │   │         │
│  │  │  CHECK 4: IAM Policy (on the requester's user/role)            │   │         │
│  │  │  ┌─────────────────────────────────────────────────────┐       │   │         │
│  │  │  │ IAM DENY? ──► 403 Denied ❌ (STOP)                 │       │   │         │
│  │  │  │ IAM ALLOW? ──► ACCESS GRANTED ✅                    │       │   │         │
│  │  │  │ No match? ──► 403 Denied ❌ (default deny)          │       │   │         │
│  │  │  └─────────────────────────────────────────────────────┘       │   │         │
│  │  └─────────────────────────────────────────────────────────────────┘   │         │
│  │                           │                                            │         │
│  │                    ACCESS GRANTED ✅                                   │         │
│  │                           │                                            │         │
│  │                           ▼                                            │         │
│  │  ┌─────────────────────────────────────────────────────────────────┐   │         │
│  │  │ STEP 5: Object Lookup                                          │   │         │
│  │  │                                                                 │   │         │
│  │  │  S3 looks up the object key: "logo.png"                        │   │         │
│  │  │                                                                 │   │         │
│  │  │  ├── Object exists? ──► Continue ▼                             │   │         │
│  │  │  │                                                             │   │         │
│  │  │  ├── Object NOT found? ──► 404 Not Found ❌                    │   │         │
│  │  │  │                                                             │   │         │
│  │  │  └── Versioning enabled? ──► Fetch latest version              │   │         │
│  │  │       (or specific version if ?versionId=abc123 in URL)        │   │         │
│  │  └─────────────────────────────────────────────────────────────────┘   │         │
│  │                           │                                            │         │
│  │                           ▼                                            │         │
│  │  ┌─────────────────────────────────────────────────────────────────┐   │         │
│  │  │ STEP 6: Storage Class Retrieval                                 │   │         │
│  │  │                                                                 │   │         │
│  │  │  Which storage class is the object in?                         │   │         │
│  │  │                                                                 │   │         │
│  │  │  ┌──────────────────┐                                          │   │         │
│  │  │  │ S3 Standard      │──► Instant (milliseconds) ──► Return ✅ │   │         │
│  │  │  ├──────────────────┤                                          │   │         │
│  │  │  │ Standard-IA      │──► Instant (milliseconds) ──► Return ✅ │   │         │
│  │  │  ├──────────────────┤    (+ per-GB retrieval fee)              │   │         │
│  │  │  │ One Zone-IA      │──► Instant (milliseconds) ──► Return ✅ │   │         │
│  │  │  ├──────────────────┤    (+ per-GB retrieval fee)              │   │         │
│  │  │  │ Intelligent-Tier │──► Instant* (depends on current tier)    │   │         │
│  │  │  ├──────────────────┤                              ──► Return  │   │         │
│  │  │  │ Glacier Instant  │──► Instant (milliseconds) ──► Return ✅ │   │         │
│  │  │  ├──────────────────┤    (+ higher retrieval fee)              │   │         │
│  │  │  │ Glacier Flexible │──► ⏳ RESTORE REQUEST NEEDED             │   │         │
│  │  │  │                  │    Expedited: 1-5 min                    │   │         │
│  │  │  │                  │    Standard:  3-5 hours                  │   │         │
│  │  │  │                  │    Bulk:      5-12 hours                 │   │         │
│  │  │  │                  │    → 409 Error if not restored yet ❌    │   │         │
│  │  │  ├──────────────────┤                                          │   │         │
│  │  │  │ Deep Archive     │──► ⏳ RESTORE REQUEST NEEDED             │   │         │
│  │  │  │                  │    Standard:  12 hours                   │   │         │
│  │  │  │                  │    Bulk:      48 hours                   │   │         │
│  │  │  │                  │    → 409 Error if not restored yet ❌    │   │         │
│  │  │  └──────────────────┘                                          │   │         │
│  │  └─────────────────────────────────────────────────────────────────┘   │         │
│  │                           │                                            │         │
│  │                           ▼                                            │         │
│  │  ┌─────────────────────────────────────────────────────────────────┐   │         │
│  │  │ STEP 7: Decryption (if encrypted)                               │   │         │
│  │  │                                                                 │   │         │
│  │  │  ├── SSE-S3?  ──► AWS auto-decrypts (transparent)              │   │         │
│  │  │  ├── SSE-KMS? ──► KMS decrypts using key + logs to CloudTrail  │   │         │
│  │  │  └── DSSE-KMS?──► Double decryption via KMS                    │   │         │
│  │  └─────────────────────────────────────────────────────────────────┘   │         │
│  │                           │                                            │         │
│  │                           ▼                                            │         │
│  │  ┌─────────────────────────────────────────────────────────────────┐   │         │
│  │  │ STEP 8: Response Sent to Client                                 │   │         │
│  │  │                                                                 │   │         │
│  │  │  HTTP 200 OK                                                    │   │         │
│  │  │  Headers:                                                       │   │         │
│  │  │    Content-Type: image/png                                      │   │         │
│  │  │    Content-Length: 45678                                         │   │         │
│  │  │    ETag: "abc123def456"                                         │   │         │
│  │  │    x-amz-storage-class: STANDARD                                │   │         │
│  │  │    x-amz-server-side-encryption: aws:kms                        │   │         │
│  │  │  Body: [binary data of logo.png]                                │   │         │
│  │  └─────────────────────────────────────────────────────────────────┘   │         │
│  │                           │                                            │         │
│  │                           ▼                                            │         │
│  │  ┌─────────────────────────────────────────────────────────────────┐   │         │
│  │  │ STEP 9: Logging (background, after response)                    │   │         │
│  │  │                                                                 │   │         │
│  │  │  ├── Server Access Logging? ──► Write log to destination bucket │   │         │
│  │  │  ├── CloudTrail enabled?   ──► Record API event                 │   │         │
│  │  │  └── CloudWatch Metrics?   ──► Update request count & bytes     │   │         │
│  │  └─────────────────────────────────────────────────────────────────┘   │         │
│  └─────────────────────────────────────────────────────────────────────────┘         │
│                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────┐         │
│  │                        SUMMARY OF RESPONSE TIMES                       │         │
│  │                                                                         │         │
│  │  Standard / IA / Glacier Instant ──► Milliseconds (instant)            │         │
│  │  Intelligent-Tiering ──────────────► Milliseconds to Hours*            │         │
│  │  Glacier Flexible ─────────────────► 1 minute to 12 hours              │         │
│  │  Deep Archive ─────────────────────► 12 to 48 hours                    │         │
│  │                                                                         │         │
│  │  * If data is in archive tiers, a restore must complete first.         │         │
│  │    Direct GET on Glacier/Deep Archive WITHOUT prior restore = 409 ❌   │         │
│  └─────────────────────────────────────────────────────────────────────────┘         │
└─────────────────────────────────────────────────────────────────────────────────────┘
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

### 4.5 Block Public Access (BPA)

#### What
Block Public Access is a **bucket-level safety switch** that prevents your data from accidentally becoming public. It's an umbrella setting that overrides any ACL or Bucket Policy that tries to make objects public.

#### Why
Data breaches caused by **misconfigured public S3 buckets** are one of the most common cloud security incidents. Companies like Capital One, Twitch, and the US Department of Defense have suffered leaks because someone accidentally left a bucket open. BPA acts as a **master lock** that stops this.

#### How
1. Go to your bucket → **Permissions** tab.
2. Click **Edit** under **Block Public Access**.
3. You'll see **4 toggles** (all ON by default):

| Setting | What It Blocks |
| :--- | :--- |
| **BlockPublicAcls** | Blocks any new ACL that grants public access |
| **IgnorePublicAcls** | Ignores existing ACLs that grant public access |
| **BlockPublicPolicy** | Blocks any new bucket policy that grants public access |
| **RestrictPublicBuckets** | Restricts access to only AWS-authorized principals |

4. To make a bucket public (e.g., for static website hosting), you must **turn OFF all 4 toggles** first.

```text
┌──────────────────────────────────────────────────────────┐
│              BLOCK PUBLIC ACCESS (Default: ALL ON)       │
│                                                          │
│  ┌─────────────────┐    ┌─────────────────┐              │
│  │ BlockPublicAcls │ ON │IgnorePublicAcls │ ON           │
│  └─────────────────┘    └─────────────────┘              │
│  ┌───────────────────┐  ┌──────────────────────┐         │
│  │BlockPublicPolicy  │ON│RestrictPublicBuckets │ ON      │
│  └───────────────────┘  └──────────────────────┘         │
│                                                          │
│  Result: Even if ACL says "public" or policy says        │
│  "allow *", access is STILL BLOCKED ❌                   │
│                                                          │
│  To allow public access:                                 │
│  Turn OFF all 4 → THEN add ACL/Policy → Access works ✅ │
└──────────────────────────────────────────────────────────┘
```

#### Impact
- **Enabled (default)**: Bulletproof protection against accidental public exposure. Even a wrong IAM policy can't leak your data.
- **Disabled**: The bucket **can** be made public via ACLs or Bucket Policies. Required for static website hosting, but risky if misconfigured.

> 🛡️ **Best Practice**: Keep BPA enabled on ALL buckets by default. Only disable it on specific buckets that genuinely need public access (like static websites).

---

### 4.6 Access Control Lists (ACLs)

#### What
ACLs are the **oldest and simplest** way to control access to S3 buckets and objects. They define which AWS accounts or predefined groups (like "Everyone") can perform actions (read, write, full control) on a bucket or individual object.

#### Why
ACLs were S3's original access control mechanism (before Bucket Policies and IAM existed). They still exist for **backward compatibility**, but AWS now recommends **disabling them** in favor of Bucket Policies and IAM.

#### How
1. Go to your bucket → **Permissions** tab → **Object Ownership**.
2. Two modes:
   - **ACLs Disabled (Recommended)**: Bucket owner owns all objects. Access managed via policies only.
   - **ACLs Enabled**: Individual objects can have their own ACL permissions.

**ACL Permission Levels:**

| Permission | On Bucket | On Object |
| :--- | :--- | :--- |
| **READ** | List objects in the bucket | Read the object data |
| **WRITE** | Create/delete objects in the bucket | N/A (not applicable) |
| **READ_ACP** | Read the bucket's ACL | Read the object's ACL |
| **WRITE_ACP** | Modify the bucket's ACL | Modify the object's ACL |
| **FULL_CONTROL** | All of the above | All of the above |

**Predefined Groups (Grantees):**

| Group | Who Are They? |
| :--- | :--- |
| **Bucket Owner** | The AWS account that created the bucket |
| **Authenticated Users** | Any user with a valid AWS account (⚠️ NOT just your organization!) |
| **Everyone (Public)** | Anyone on the internet — no AWS account needed |
| **Log Delivery Group** | AWS service that writes S3 access logs |

```text
┌──────────────────────────────────────────────────────────────┐
│                     ACL vs BUCKET POLICY                     │
│                                                              │
│  ACLs (Legacy)                  Bucket Policies (Modern)     │
│  ┌────────────────────┐         ┌────────────────────────┐   │
│  │ Simple             │         │ Powerful               │   │
│  │ Per-object control │         │ JSON-based rules       │   │
│  │ Limited actions    │         │ Fine-grained actions   │   │
│  │ No conditions      │         │ IP, time, MFA conds   │   │
│  │ Hard to audit      │         │ Easy to read & audit   │   │
│  └────────────────────┘         └────────────────────────┘   │
│                                                              │
│  AWS Recommendation: DISABLE ACLs, use Bucket Policies ✅    │
└──────────────────────────────────────────────────────────────┘
```

#### Impact
- **ACLs Enabled**: Fine-grained per-object permissions, but harder to manage at scale. Risk of individual objects having unexpected access.
- **ACLs Disabled (Recommended)**: Centralized control through policies. Simpler, more secure, easier to audit.

> ⚠️ **Common Mistake**: Setting ACL to "Authenticated Users" thinking it means "only my team." It actually means **any person with any AWS account in the world** can access your data!

---

### 4.7 Bucket Policies

#### What
Bucket Policies are **JSON-based access control rules** attached directly to a bucket. They define who can do what on the bucket and its objects. Think of them as a **detailed rulebook** stuck on the front door of your bucket.

#### Why
Bucket Policies offer **much more control** than ACLs. You can grant access based on IP address, time of day, whether MFA was used, or restrict access to specific AWS services. They are the **recommended** way to manage S3 access.

#### How
1. Go to your bucket → **Permissions** tab → **Bucket Policy** → **Edit**.
2. Write or paste a JSON policy.
3. Save.

**Example: Make entire bucket publicly readable (for static website hosting):**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::my-website-bucket/*"
    }
  ]
}
```

**Anatomy of a Bucket Policy:**

```text
┌─────────────────────────────────────────────────────────┐
│                    BUCKET POLICY                        │
│                                                         │
│  "Effect"    →  Allow or Deny                           │
│  "Principal" →  WHO ("*" = everyone, specific ARN)      │
│  "Action"    →  WHAT (s3:GetObject, s3:PutObject, etc.) │
│  "Resource"  →  WHERE (bucket ARN + path)               │
│  "Condition" →  WHEN (IP range, MFA, SSL only, etc.)    │
└─────────────────────────────────────────────────────────┘

Example Conditions:
┌────────────────────┬──────────────────────────────────┐
│ Condition          │ Use Case                         │
├────────────────────┼──────────────────────────────────┤
│ IpAddress          │ Allow only from office IP range  │
│ SecureTransport    │ Enforce HTTPS only               │
│ MFA                │ Require MFA for delete actions   │
│ StringEquals       │ Restrict to specific prefixes    │
└────────────────────┴──────────────────────────────────┘
```

#### Impact
- **Using it**: Precise, auditable access control. You can allow CloudFront but block direct access, enforce HTTPS, restrict by IP.
- **Not using it**: You rely on ACLs (limited) or IAM only (doesn't cover cross-account or public access scenarios).

---

### 4.8 CORS (Cross-Origin Resource Sharing)

#### What
CORS is a **browser security configuration** that controls whether a web page from one domain (e.g., `myapp.com`) can request resources from your S3 bucket (e.g., `my-bucket.s3.amazonaws.com`). Without CORS, the browser blocks these cross-origin requests.

#### Why
Modern web apps often store images, fonts, or API data in S3 while the website itself runs on a different domain. Without CORS, the browser's **Same-Origin Policy** blocks the requests, and your images/fonts won't load.

#### How
1. Go to your bucket → **Permissions** tab → **Cross-origin resource sharing (CORS)**.
2. Add a JSON configuration:

```json
[
  {
    "AllowedHeaders": ["*"],
    "AllowedMethods": ["GET", "PUT"],
    "AllowedOrigins": ["https://myapp.com"],
    "ExposeHeaders": ["ETag"],
    "MaxAgeSeconds": 3000
  }
]
```

```text
 WITHOUT CORS                              WITH CORS

 ┌──────────┐    GET image.png    ┌─────┐   ┌──────────┐   GET image.png   ┌─────┐
 │ myapp.com│ ──────────────────► │ S3  │   │ myapp.com│ ────────────────► │ S3  │
 └──────────┘                    └─────┘   └──────────┘                   └─────┘
      │                             │           │                            │
      │  ❌ Browser BLOCKS response │           │  ✅ S3 sends CORS headers  │
      │  "No Access-Control-Allow   │           │  "Access-Control-Allow-    │
      │   -Origin header found"     │           │   Origin: myapp.com"       │
      ▼                             ▼           ▼                            ▼
  Page broken! 🔴                           Image loads! 🟢
```

#### Impact
- **Configured**: Your web app loads S3-hosted assets (images, fonts, JSON data) seamlessly across domains.
- **Not configured**: Users see broken images, missing fonts, and CORS errors in the browser console.

---

### 4.9 Server Access Logging

#### What
Server Access Logging records **every request** made to your S3 bucket — who accessed what, when, from which IP, and whether it succeeded or failed. The logs are stored in a **separate S3 bucket**.

#### Why
For **security auditing**, **compliance**, and **troubleshooting**. If someone accesses sensitive data or if costs spike unexpectedly, access logs tell you exactly what happened.

#### How
1. Create a **separate bucket** for storing logs (e.g., `my-app-access-logs`).
2. Go to your source bucket → **Properties** tab → **Server access logging**.
3. Enable it and specify the log destination bucket.
4. Optionally set a **prefix** (e.g., `logs/2026/`) to organize log files.

```text
┌─────────────────────┐         ┌────────────────────────────┐
│                     │  Logs   │                            │
│  Source Bucket      │────────►│  Log Destination Bucket    │
│  (prod-app-data)    │         │  (prod-app-access-logs)    │
│                     │         │                            │
│  Every GET, PUT,    │         │  Log Format:               │
│  DELETE request     │         │  [bucket-owner] [bucket]   │
│  is recorded        │         │  [time] [remote-ip]        │
│                     │         │  [requester] [operation]   │
│                     │         │  [key] [status-code]       │
│                     │         │  [bytes-sent]              │
└─────────────────────┘         └────────────────────────────┘
```

#### Impact
- **Enabled**: Full audit trail for security reviews. Identify unauthorized access, track costs, debug 403/404 errors.
- **Not enabled**: Blind spot — you have no idea who's accessing your data or why costs are rising.

> ⚠️ **Important**: Never store logs in the **same bucket** being logged. This creates an infinite loop (logging the log writes, which generates more logs).

---

### 4.10 Tags

#### What
Tags are **key-value pairs** (e.g., `Environment: Production`, `Team: Backend`) attached to your bucket for organization, cost tracking, and access control.

#### Why
When you have hundreds of S3 buckets across an organization, tags let you **categorize**, **filter**, and **allocate costs** by team, project, or environment.

#### How
1. Go to your bucket → **Properties** tab → **Tags**.
2. Add key-value pairs:

| Key | Value | Purpose |
| :--- | :--- | :--- |
| `Environment` | `Production` | Distinguish prod vs dev |
| `Team` | `Backend` | Track which team owns it |
| `Project` | `E-Commerce` | Group by project |
| `CostCenter` | `CC-1234` | AWS Cost Explorer billing |

#### Impact
- **Using it**: Clear ownership, accurate cost allocation in AWS billing, ability to create IAM policies that target specific tags.
- **Not using it**: Chaos — nobody knows who owns which bucket, and the monthly AWS bill is an unreadable mystery.

---

### 4.11 Transfer Acceleration

#### What
Transfer Acceleration speeds up **long-distance uploads** to S3 by routing data through Amazon's **CloudFront Edge Locations** (200+ worldwide). Instead of sending data straight across the internet, it enters Amazon's private backbone network at the nearest edge location.

#### Why
If your S3 bucket is in `us-east-1` but users upload from India or Australia, normal uploads travel over the public internet — slow and unreliable. Transfer Acceleration cuts upload time by **50-500%** for distant users.

#### How
1. Go to your bucket → **Properties** tab → **Transfer Acceleration**.
2. Enable it.
3. Use the accelerated endpoint: `my-bucket.s3-accelerate.amazonaws.com` instead of the normal endpoint.

```text
  NORMAL UPLOAD                    TRANSFER ACCELERATION

  ┌────────┐    Public Internet    ┌────────┐    Edge Location    AWS Backbone    ┌────────┐
  │  User  │ ───────────────────► │   S3   │    ┌──────────┐   ─────────────►   │   S3   │
  │ Mumbai │    ~800ms latency    │us-east │    │  Mumbai  │   Private, fast    │us-east │
  └────────┘                      └────────┘    │  Edge    │                    └────────┘
                                                └──────────┘
                                    ┌────────┐
                                    │  User  │ ──► Edge ──► Backbone ──► S3
                                    │ Mumbai │     ~50ms      ~100ms
                                    └────────┘
                                    Total: ~150ms (vs 800ms) ⚡
```

#### Impact
- **Enabled**: Dramatically faster uploads for geographically distant users. Better user experience.
- **Not enabled**: Users far from the bucket region experience slow, unreliable uploads.

---

### 4.12 Requester Pays

#### What
Normally the **bucket owner** pays for storage AND data transfer. With Requester Pays, the **person downloading** the data pays for the transfer costs.

#### Why
If you share large datasets (satellite imagery, genomics data, public research) with thousands of users, data transfer costs can be enormous. Requester Pays shifts the download cost to the consumer.

#### How
1. Go to your bucket → **Properties** tab → **Requester Pays**.
2. Enable it.
3. Now anyone downloading must include their AWS credentials and agrees to pay transfer costs.

#### Impact
- **Enabled**: You only pay for storage; downloaders pay for bandwidth. Great for shared/public datasets.
- **Not enabled**: You pay for every single download. One viral dataset could cost you thousands.

---

### Complete Bucket Configuration Summary

```text
┌──────────────────────────────────────────────────────────────────────────┐
│                    S3 BUCKET CONFIGURATION MAP                         │
│                                                                        │
│  ┌─── SECURITY ────────────────────────────────────────────────────┐   │
│  │                                                                 │   │
│  │  Block Public Access ── Master switch (ON by default)           │   │
│  │         │                                                       │   │
│  │         ├── ACLs ────── Legacy per-object permissions            │   │
│  │         │               (Recommended: DISABLE)                   │   │
│  │         │                                                       │   │
│  │         ├── Bucket Policy ── JSON rules (WHO/WHAT/WHERE/WHEN)   │   │
│  │         │                    (Recommended: USE THIS)            │   │
│  │         │                                                       │   │
│  │         ├── Encryption ── SSE-S3 │ SSE-KMS │ DSSE-KMS           │   │
│  │         │                                                       │   │
│  │         └── Object Lock ── WORM protection (Governance/Comply)  │   │
│  │                                                                 │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                        │
│  ┌─── DATA MANAGEMENT ────────────────────────────────────────────┐   │
│  │                                                                 │   │
│  │  Versioning ────── Keep all versions of objects                  │   │
│  │  Lifecycle Rules ── Auto-transition & auto-delete                │   │
│  │  Tags ───────────── Organize, track costs, control access       │   │
│  │  Replication ────── Copy to another bucket/region               │   │
│  │                                                                 │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                        │
│  ┌─── PERFORMANCE & ACCESS ───────────────────────────────────────┐   │
│  │                                                                 │   │
│  │  Transfer Acceleration ── Fast uploads via Edge Locations       │   │
│  │  CORS ────────────────── Allow cross-domain web requests        │   │
│  │  Static Website Hosting ── Serve HTML/CSS/JS directly           │   │
│  │  Requester Pays ──────── Downloaders pay transfer costs         │   │
│  │                                                                 │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                        │
│  ┌─── MONITORING ─────────────────────────────────────────────────┐   │
│  │                                                                 │   │
│  │  Server Access Logging ── Log every request to another bucket   │   │
│  │  CloudTrail ──────────── Log API calls (management events)      │   │
│  │  S3 Metrics ──────────── CloudWatch storage/request metrics     │   │
│  │                                                                 │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────────┘
```

### Access Control Decision Flow

```text
Request arrives at S3 bucket
        │
        ▼
┌───────────────────────┐
│ Block Public Access   │──── ON? ──── Is request public?
│ (Master Switch)       │                │
└───────────┬───────────┘           YES = ❌ DENIED
            │ (passes or                  │
            │  not public)           NO = Continue ▼
            ▼
┌───────────────────────┐
│ Bucket Policy         │──── Explicit DENY? ──── ❌ DENIED
│ (JSON Rules)          │
│                       │──── Explicit ALLOW? ─── Continue ▼
└───────────┬───────────┘
            │ (no explicit deny)
            ▼
┌───────────────────────┐
│ ACLs                  │──── ALLOW? ──── ✅ ACCESS GRANTED
│ (if enabled)          │
│                       │──── No match ── ❌ DENIED (default)
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ IAM Policy            │──── ALLOW? ──── ✅ ACCESS GRANTED
│ (User/Role level)     │
│                       │──── No match ── ❌ DENIED (default)
└───────────────────────┘

  RULE: Explicit DENY always wins over any ALLOW.
  DEFAULT: Everything is DENIED unless explicitly ALLOWED.
```

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
┌──────────────────────────────────────────────────────────────────────────────┐
│                              AWS CLOUD                                      │
│                                                                             │
│  ┌──────────┐                                                               │
│  │  Users   │      ┌───────────────────────────────────────────────────┐    │
│  │ (Browser)│─────►│            S3 Bucket: prod-app-data               │    │
│  └──────────┘      │                                                   │    │
│       │            │  ┌──────────────┐   ┌──────────────────────────┐  │    │
│       │ CORS       │  │  Objects     │   │  /images/                │  │    │
│       │ allowed    │  │  index.html  │   │  logo.png                │  │    │
│       │            │  │  style.css   │   │  banner.jpg              │  │    │
│                    │  │  app.js      │   │                          │  │    │
│                    │  └──────────────┘   └──────────────────────────┘  │    │
│                    │                                                   │    │
│                    │  Security:                                        │    │
│                    │  ├── Block Public Access: OFF (website bucket)    │    │
│                    │  ├── ACLs: DISABLED (using policies instead)      │    │
│                    │  ├── Bucket Policy: Allow public s3:GetObject     │    │
│                    │  ├── Encryption: SSE-KMS                          │    │
│                    │  └── Object Lock: Compliance Mode (7 years)       │    │
│                    │                                                   │    │
│                    │  Management:                                      │    │
│                    │  ├── Versioning: ENABLED                          │    │
│                    │  ├── Lifecycle: Standard → Glacier (90d) → Del    │    │
│                    │  ├── Tags: Env=Prod, Team=Backend                 │    │
│                    │  ├── Transfer Acceleration: ENABLED               │    │
│                    │  └── Server Access Logging → logs-bucket          │    │
│                    │                                                   │    │
│                    └───────────────────────────────────────────────────┘    │
│                              │                                              │
│                     ┌────────▼───────┐      ┌──────────────────────┐        │
│                     │  Replication   │      │  Access Logs Bucket  │        │
│                     │  across 3 AZs  │      │  (prod-app-logs)     │        │
│                     ├────┬────┬──────┤      │  Every request       │        │ 
│                     │AZ-1│AZ-2│AZ-3  │      │  recorded here       │        │
│                     └────┴────┴──────┘      └──────────────────────┘        │
└─────────────────────────────────────────────────────────────────────────────┘
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

🔍 **Scenario 7**: Your React app at `app.example.com` loads images from your S3 bucket, but users see broken images and the browser console shows CORS errors.
✅ **Answer**: Configure **CORS** on your S3 bucket to allow requests from `https://app.example.com`. Add `GET` to AllowedMethods and `https://app.example.com` to AllowedOrigins. The browser will then accept the cross-origin responses.

---

🔍 **Scenario 8**: Your company has 200+ S3 buckets, and the monthly AWS bill is $50,000. Management asks "Which team is using the most storage?"
✅ **Answer**: If **Tags** were used (e.g., `Team: Backend`, `Team: Frontend`), open **AWS Cost Explorer**, filter by S3 service, and group by the `Team` tag. You'll see cost breakdown per team. Without tags, you'd have to manually check each bucket — nearly impossible at scale.

---

🔍 **Scenario 9**: A junior developer set the ACL of a confidential HR document to "Authenticated Users" thinking it means only their team. Is the document safe?
✅ **Answer**: **No!** "Authenticated Users" means **any person in the world with an AWS account** — not just your organization. The document is essentially public to all 1 million+ AWS customers. Fix: Remove the ACL, disable ACLs on the bucket, and use a **Bucket Policy** with specific IAM ARNs instead.

---

🔍 **Scenario 10**: You notice suspicious access patterns on your S3 bucket — someone might be downloading data they shouldn't. How do you investigate?
✅ **Answer**: Enable **Server Access Logging** on the bucket (if not already enabled). Review the logs to see the requester's IP, the objects accessed, timestamps, and HTTP status codes. Cross-reference with **CloudTrail** for the IAM identity. Then tighten the **Bucket Policy** to restrict access.

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

### Q11: What is Block Public Access, and why is it important?
**A**: Block Public Access is a **master safety switch** with 4 settings that override ACLs and Bucket Policies to prevent accidental public exposure. It's enabled by default on all new buckets. It's important because many high-profile data breaches (Capital One, US DoD) happened due to misconfigured public buckets. BPA ensures that even if a developer writes a wrong policy, data stays private.

---

### Q12: What is the difference between ACLs and Bucket Policies? Which should you use?
**A**: ACLs are the **legacy** access control method — simple but limited (no conditions, hard to audit, per-object). Bucket Policies are **modern** JSON-based rules that support conditions (IP, MFA, HTTPS), are easier to audit, and apply at bucket level. **AWS recommends disabling ACLs** and using Bucket Policies for all access control.

---

### Q13: What is CORS, and when do you need to configure it on S3?
**A**: CORS (Cross-Origin Resource Sharing) controls whether a web page from one domain can access resources on your S3 bucket. You need it when your web app (e.g., `myapp.com`) fetches images, fonts, or data from S3 (a different origin). Without CORS, the browser blocks these requests due to the Same-Origin Policy.

---

### Q14: Explain the S3 access evaluation flow. What happens when a request hits your bucket?
**A**: S3 evaluates access in this order:
1. **Block Public Access** — If ON and request is public → DENIED
2. **Bucket Policy** — Check for explicit DENY (always wins) or ALLOW
3. **ACLs** (if enabled) — Check for ALLOW
4. **IAM Policies** — Check for ALLOW on the requester's role/user

Default is **DENY** — access is only granted if explicitly allowed AND not explicitly denied anywhere in the chain.

---

### Q15: What is the difference between Server Access Logging and CloudTrail for S3?
**A**:
- **Server Access Logging**: Records **every object-level request** (GET, PUT, DELETE) with details like IP, time, status code. Logs are delivered to another S3 bucket. Best for **detailed request analysis**.
- **CloudTrail**: Records **API-level management events** (CreateBucket, PutBucketPolicy, DeleteBucket). Best for **auditing configuration changes** and who made them.

Use **both** together for complete visibility.

---

← Previous: [`16_aws-s3-static-website-hosting.md`](16_aws-s3-static-website-hosting.md) | Next: [`18_TBD.md`](18_TBD.md) →
