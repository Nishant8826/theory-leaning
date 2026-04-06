# 🎯 System Design: AWS IAM (Like Identity & Access Management Platform)
> **Level:** Beginner-Friendly | **Format:** What → Why → How → Impact
> **Stack:** Next.js + Node.js + MySQL + MongoDB (Polyglot) + Redis + CDN

---

## 1. 📋 REQUIREMENTS

### 🧠 Think of it like this
> Imagine a massive hospital. The front desk checks your ID and gives you a visitor badge (Authentication). Your badge's RFID chip opens the cafeteria, but flashes red at the surgical room (Authorization). IAM is this security system — for the entire cloud.

---

### ✅ Functional Requirements (FR)

| # | Requirement | What | Why | How | Impact if Missing |
|:--|:-----------|:-----|:----|:----|:-----------------|
| FR1 | **Create Users** | Admins create individual user accounts | Every person/service needs a unique identity | POST API → MySQL `users` table with hashed password | No way to identify who is doing what |
| FR2 | **Create Groups** | Group users logically (e.g., `Developers`, `HR`) | Assign permissions to 100 people in one click instead of 100 times | MySQL `groups` table with many-to-many mapping | Admin manually manages every user = slow & error-prone |
| FR3 | **Assign Users to Groups** | Add/remove users from groups | Inheritance of permissions — join `Developers` group, get all dev permissions | MySQL join table `group_memberships` | Can't batch-manage permissions |
| FR4 | **Create Roles** | Temporary permissions assumed by services | An EC2 server or Lambda function needs database access — but it's not a human | MongoDB role document with trust policy | Services can't access anything, or they have permanent keys (insecure) |
| FR5 | **Attach/Detach Policies** | Define Allow/Deny rules and attach to users/groups/roles | Granular control — DevOps can deploy but not delete prod DB | MongoDB JSON policy documents | Everyone has full access = security nightmare |
| FR6 | **Authentication (Login)** | Validate user credentials securely | Prove "you are who you say you are" | bcrypt password comparison + JWT token generation | Anyone can pretend to be anyone |
| FR7 | **Authorization (Access Control)** | Evaluate every API request against policies | Prove "you are allowed to do this" | Policy Engine evaluates merged policies | Any user can do any action = catastrophic |
| FR8 | **Generate Access Keys** | Programmatic access for bots/tools (Terraform, Jenkins) | Humans use passwords, machines use access keys | Key pair generation (Access Key ID + Secret Key) | No programmatic automation possible |
| FR9 | **Audit Logs** | Record "who did what, when, from where" | Compliance, forensics, and debugging | Async event → MongoDB audit collection | No accountability, can't investigate breaches |

### ⚙️ Non-Functional Requirements (NFR)

| # | Requirement | What | Why | Real-World Example | Impact if Missing |
|:--|:-----------|:-----|:----|:-------------------|:-----------------|
| NFR1 | **High Availability (99.99%)** | IAM must never go down | If IAM is down, the ENTIRE cloud platform is inaccessible | AWS had an IAM outage in 2017 — no one could access any service | Total platform outage |
| NFR2 | **Low Latency (<100ms)** | Every API call first passes through IAM check | Billions of authorization checks per day | A 500ms IAM check on every S3 read would make the whole cloud unusable | All services become slow |
| NFR3 | **Strong Security** | Withstand brute-force, token theft, privilege escalation | IAM IS the security system — if it's compromised, everything is | MFA, key rotation, encryption at rest + in transit | Single breach = entire cloud exposed |
| NFR4 | **Scalability** | Millions of users, billions of access checks/day | Every microservice, user, and bot checks IAM on every action | Netflix has thousands of microservices all hitting IAM constantly | System crumbles under load |
| NFR5 | **Fault Tolerance** | Redundancy across multiple geographic regions | A data center fire shouldn't take down global IAM | Multi-AZ, multi-region replication | Single region failure = global outage |
| NFR6 | **Auditability** | Tamper-proof logs of every security decision | Regulatory compliance (SOC2, GDPR, HIPAA) | Auditors need proof of access controls | Compliance failures = legal penalties |

---

## 2. 📊 SCALE & CONSTRAINTS

### 🧠 Think of it like this
> IAM is unique — it's not user-facing like Instagram. It's infrastructure-facing. Every single API call across the entire cloud platform hits IAM. If AWS handles 1 billion API calls/day, IAM handles 1 billion authorization checks/day.

---

### Traffic Estimation

| Metric | Calculation | Result |
|:-------|:-----------|:-------|
| **Total cloud users** | All AWS accounts, IAM users, roles | **~500M identities** |
| **Auth checks per day** | Every API call = 1 IAM check | **~10B checks/day** |
| **Auth check RPS (normal)** | 10B ÷ 86,400 | **~115,000 RPS** |
| **Auth check RPS (peak, 3x)** | 115K × 3 | **~350,000 RPS** |
| **Login requests per day** | ~5M human logins + ~50M token refreshes | **~55M/day** |
| **Policy updates per day** | Admin actions (create/modify policies) | **~500K/day** |

### Storage Estimation

| Data Type | Size per Unit | Total Volume |
|:----------|:-------------|:-------------|
| **User records** | ~2KB | 500M × 2KB = **~1 TB** |
| **Policy documents** | ~5KB avg (JSON) | 100M policies × 5KB = **~500 GB** |
| **Group memberships** | ~100 bytes | 2B mappings × 100B = **~200 GB** |
| **Audit logs** | ~500 bytes per log | 10B/day × 500B = **~5 TB/day** (cold storage with archival) |

### Scaling Journey

| Stage | Identities | Infra Needed |
|:------|:-----------|:-------------|
| **Startup SaaS** | 100 – 1K | Single server, 1 MySQL DB, basic JWT |
| **Mid Company** | 1K – 100K | Load balanced services, Redis cache, read replicas |
| **Enterprise** | 100K – 10M | Microservices on K8s, sharded DB, multi-AZ |
| **Cloud Platform (AWS-scale)** | 10M – 500M | Multi-region, dedicated policy engine cluster, Kafka audit pipeline |

---

## 3. 💰 BUDGET & COSTING

### 🧠 Think of it like this
> IAM is a cost CENTER, not a revenue generator — but it protects billions of dollars of infrastructure. Skimping on IAM is like removing locks from a bank to save on hardware.

---

| Component | Startup (1K users) | Mid Scale (1M users) | Large Scale (500M identities) |
|:----------|:-------------------|:---------------------|:------------------------------|
| **Compute (Node.js Services)** | 1 EC2 (~$20/mo) | 10 EKS pods (~$400/mo) | 500+ containers (~$25K/mo) |
| **MySQL (Users/Groups)** | Small RDS (~$15/mo) | Multi-AZ Master + 3 replicas (~$500/mo) | Sharded cluster (~$15K/mo) |
| **MongoDB (Policies/Logs)** | Atlas free tier ($0) | Dedicated cluster (~$300/mo) | Sharded multi-region (~$10K/mo) |
| **Redis Cache** | Micro (~$15/mo) | Cluster (~$300/mo) | Multi-AZ cluster (~$8K/mo) |
| **Message Queue (Kafka)** | Not needed | Basic (~$100/mo) | Multi-broker cluster (~$5K/mo) |
| **Total** | **~$55/mo** | **~$1,600/mo** | **~$65K+/mo** |

**💡 Key Reasoning:**
- **Startup:** Use managed services (RDS, Redis Cloud) — don't hire a DBA for 100 users.
- **Mid Scale:** Invest heavily in Redis — every millisecond in IAM check latency multiplies across EVERY API call in your platform.
- **Large Scale:** Audit log storage dominates. Use S3 + Glacier for cold storage archival — 90% of audit logs are read during investigations, not daily.

---

## 4. 🏗️ HIGH LEVEL DESIGN (HLD)

### 🧠 Think of it like this
> IAM has two doors: the **front door** (Authentication — "Who are you?") and the **inner doors** (Authorization — "Are you allowed here?"). Every person and every robot must pass through both doors for every single action.

---

### Why Next.js for IAM Dashboard?

| Rendering Mode | What | When to Use in IAM | Benefit |
|:---------------|:-----|:-------------------|:--------|
| **SSR (Server-Side Rendering)** | HTML generated on server per request | IAM Dashboard pages (user list, policy editor) | Secure — sensitive data never exposed in client JS bundles |
| **SSG (Static Site Generation)** | HTML generated at build time | Documentation, help pages, error pages | Fast load, cached at CDN, zero server cost |
| **CSR (Client-Side Rendering)** | JavaScript renders in browser | Interactive policy builder, real-time audit log viewer | Rich interactivity for complex JSON editing |

**Why Not Pure React?** → IAM dashboards benefit from SSR because sensitive data (user lists, policy details) should be rendered server-side and sent as HTML — not fetched client-side where it could be intercepted by browser extensions.

---

### Polyglot Persistence — Which Database for Which Service?

| Service | Database | Why This Choice |
|:--------|:---------|:---------------|
| **User Service** | MySQL | ACID compliance — if you delete a user, all group memberships must delete atomically |
| **Group Service** | MySQL | Many-to-many relationships (users ↔ groups) — JOINs are essential |
| **Policy Service** | MongoDB | Policies are deeply nested JSON (Actions arrays, Resource wildcards, Conditions). SQL can't handle dynamic schemas well |
| **Auth Service** | MySQL + Redis | MySQL stores credentials, Redis stores active sessions for instant validation |
| **Policy Engine** | Redis (primary) + MongoDB (fallback) | Must respond in <10ms — cached compiled policies in Redis |
| **Audit Service** | MongoDB | High-write-volume append-only logs with flexible schema |
| **Role Service** | MongoDB | Roles contain trust policies (JSON) + attached permission policies (JSON references) |

---

### Service-Level Architecture Diagram

```text
                    ┌───────────────────────────┐
                    │  Admin Dashboard (Next.js) │
                    │  or CLI / SDK / Terraform  │
                    └─────────────┬─────────────┘
                                  │
                                  ▼
                    ┌───────────────────────────┐
                    │  CDN (CloudFront)          │ ← Static assets (JS, CSS, docs)
                    └─────────────┬─────────────┘
                                  │
                                  ▼
                    ┌───────────────────────────┐
                    │  Load Balancer (Nginx/ALB) │ ← Distributes traffic
                    └─────────────┬─────────────┘
                                  │
                                  ▼
                    ┌───────────────────────────┐
                    │  API Gateway               │ ← TLS, Rate Limiting, Routing
                    └─────────────┬─────────────┘
                                  │
         ┌────────────┬───────────┼───────────┬────────────┐
         ▼            ▼           ▼           ▼            ▼
   ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
   │   Auth   │ │   User   │ │  Policy  │ │   Role   │ │  Audit   │
   │ Service  │ │ Service  │ │  Engine  │ │ Service  │ │ Service  │
   └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘
        │            │            │            │            │
        ▼            ▼            ▼            ▼            ▼
   ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
   │  Redis  │ │  MySQL   │ │  Redis  │ │ MongoDB │ │ MongoDB │
   │(Session)│ │(Users,   │ │(Cached  │ │(Roles,  │ │(Audit   │
   │         │ │ Groups)  │ │Policies)│ │Policies)│ │  Logs)  │
   └─────────┘ └─────────┘ └─────────┘ └─────────┘ └────┬────┘
                                                          │
                                                   ┌──────▼──────┐
                                                   │ Kafka Queue │ ← Async log ingestion
                                                   └─────────────┘
```

---

### Step-by-Step Flow: User Tries to Read a Database

```text
1. User/Service sends API request: GET /databases/prod-db
   → Request includes JWT token in Authorization header
2. API Gateway receives request
3. Gateway verifies JWT signature (is token valid and not expired?)
4. Gateway extracts user_id from JWT payload
5. Gateway forwards request to Policy Engine with:
   → user_id, action: "db:Read", resource: "arn:aws:db:::prod-db"
6. Policy Engine checks Redis cache for user's compiled policies
   → Cache HIT? Use cached result (0.5ms)
   → Cache MISS? Query MySQL for user's groups → MongoDB for all attached policies → Cache result
7. Policy Engine merges all policies and evaluates:
   → Any explicit DENY for db:Read? → DENY (Deny always wins)
   → Any explicit ALLOW for db:Read? → ALLOW
   → Neither? → Default DENY
8. If ALLOW → Request proceeds to Database Service → Returns data
   If DENY → Returns HTTP 403 Forbidden immediately
9. Audit Service logs the decision asynchronously via Kafka:
   → {user, action, resource, decision, timestamp, IP}
```

---

## 5. 🔧 LOW LEVEL DESIGN (LLD)

### 🧠 Think of it like this
> HLD is the floor plan of the building. LLD is the wiring diagram — where every switch, pipe, and wire goes. This is where we define exactly what data looks like and how services communicate.

---

### MySQL Tables (CREATE TABLE with indexes & foreign keys)

```sql
-- ========== USERS TABLE ==========
CREATE TABLE users (
    user_id       CHAR(36) PRIMARY KEY,        -- UUID
    username      VARCHAR(64) UNIQUE NOT NULL,
    email         VARCHAR(128) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,        -- bcrypt hashed
    mfa_enabled   BOOLEAN DEFAULT FALSE,
    mfa_secret    VARCHAR(128),                 -- TOTP secret (encrypted)
    status        ENUM('active', 'inactive', 'suspended') DEFAULT 'active',
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_status ON users(status);
```

```sql
-- ========== GROUPS TABLE ==========
CREATE TABLE groups (
    group_id    CHAR(36) PRIMARY KEY,
    group_name  VARCHAR(128) UNIQUE NOT NULL,
    description TEXT,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_groups_name ON groups(group_name);
```

```sql
-- ========== GROUP MEMBERSHIPS (Join Table) ==========
CREATE TABLE group_memberships (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    user_id     CHAR(36) NOT NULL,
    group_id    CHAR(36) NOT NULL,
    added_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, group_id),                -- Prevent duplicate memberships
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (group_id) REFERENCES groups(group_id) ON DELETE CASCADE
);

CREATE INDEX idx_gm_user ON group_memberships(user_id);
CREATE INDEX idx_gm_group ON group_memberships(group_id);
```

```sql
-- ========== ACCESS KEYS TABLE ==========
CREATE TABLE access_keys (
    access_key_id   CHAR(20) PRIMARY KEY,       -- e.g., "AKIAIOSFODNN7EXAMPLE"
    secret_key_hash VARCHAR(255) NOT NULL,       -- Hashed, never stored plain
    user_id         CHAR(36) NOT NULL,
    status          ENUM('active', 'inactive') DEFAULT 'active',
    last_used_at    TIMESTAMP,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE INDEX idx_ak_user ON access_keys(user_id);
```

---

### MongoDB Collections (Example JSON Documents)

**Policies Collection:**
```json
{
  "_id": ObjectId("..."),
  "policy_id": "pol_s3_readonly",
  "policy_name": "S3-Read-Only",
  "description": "Allows read and list access to all S3 buckets",
  "version": "2024-01-01",
  "statement": [
    {
      "sid": "AllowS3Read",
      "effect": "Allow",
      "action": ["s3:GetObject", "s3:ListBucket"],
      "resource": "arn:aws:s3:::*"
    },
    {
      "sid": "DenyS3Delete",
      "effect": "Deny",
      "action": ["s3:DeleteObject", "s3:DeleteBucket"],
      "resource": "*"
    }
  ],
  "attached_to": {
    "users": ["uuid-alice", "uuid-bob"],
    "groups": ["group-developers"],
    "roles": ["role-lambda-exec"]
  },
  "created_at": "2024-06-15T10:00:00Z",
  "updated_at": "2024-06-15T10:00:00Z"
}
```

**Roles Collection:**
```json
{
  "_id": ObjectId("..."),
  "role_id": "role-lambda-exec",
  "role_name": "LambdaExecutionRole",
  "description": "Role assumed by Lambda functions to access DynamoDB",
  "trust_policy": {
    "statement": [{
      "effect": "Allow",
      "principal": { "service": "lambda.amazonaws.com" },
      "action": "sts:AssumeRole"
    }]
  },
  "attached_policies": ["pol_dynamodb_readwrite", "pol_cloudwatch_logs"],
  "max_session_duration": 3600,
  "created_at": "2024-06-15T10:00:00Z"
}
```

**Audit Logs Collection:**
```json
{
  "_id": ObjectId("..."),
  "event_id": "evt_abc123",
  "timestamp": "2024-06-15T10:05:00Z",
  "user_id": "uuid-alice",
  "action": "s3:DeleteObject",
  "resource": "arn:aws:s3:::prod-backup/db-dump.sql",
  "decision": "Deny",
  "reason": "Explicit Deny in policy pol_s3_readonly",
  "source_ip": "192.168.1.100",
  "user_agent": "aws-cli/2.0"
}
```

---

### API Design (RESTful Endpoints)

| Method | Path | Description | Auth Required |
|:-------|:-----|:-----------|:-------------|
| `POST` | `/api/v1/auth/login` | Authenticate user, return JWT | ❌ |
| `POST` | `/api/v1/auth/mfa/verify` | Verify MFA TOTP code | ✅ (partial) |
| `POST` | `/api/v1/users` | Create a new IAM user | ✅ (Admin) |
| `GET` | `/api/v1/users` | List all users | ✅ (Admin) |
| `DELETE` | `/api/v1/users/:userId` | Delete a user | ✅ (Admin) |
| `POST` | `/api/v1/groups` | Create a group | ✅ (Admin) |
| `POST` | `/api/v1/groups/:groupId/members` | Add user to group | ✅ (Admin) |
| `DELETE` | `/api/v1/groups/:groupId/members/:userId` | Remove user from group | ✅ (Admin) |
| `POST` | `/api/v1/policies` | Create a JSON policy | ✅ (Admin) |
| `PUT` | `/api/v1/policies/:policyId/attach` | Attach policy to user/group/role | ✅ (Admin) |
| `POST` | `/api/v1/roles` | Create a role | ✅ (Admin) |
| `POST` | `/api/v1/authz/evaluate` | Internal: Evaluate permission (used by all services) | ✅ (Service-to-service) |
| `POST` | `/api/v1/access-keys` | Generate access key pair | ✅ |
| `GET` | `/api/v1/audit/logs?user=&action=&from=&to=` | Query audit logs | ✅ (Admin) |

---

### Core Algorithm: Policy Evaluation Engine

```text
┌──────────────────────────────────────────────────────────┐
│               POLICY ENGINE — EVALUATION FLOW            │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Input: { user_id, action, resource }                    │
│          ↓                                               │
│  Step 1: Check Redis for cached compiled policy          │
│          → Key: "policy:{user_id}"                       │
│          → HIT? Skip to Step 4                           │
│          ↓ MISS                                          │
│  Step 2: Fetch user's groups from MySQL                  │
│          → SELECT group_id FROM group_memberships        │
│            WHERE user_id = ?                             │
│          ↓                                               │
│  Step 3: Fetch ALL attached policies from MongoDB        │
│          → User's direct policies                        │
│          → Group policies (for each group)               │
│          → Role policies (if assuming a role)            │
│          → Cache compiled result in Redis (TTL: 5 min)   │
│          ↓                                               │
│  Step 4: EVALUATE against requested action + resource    │
│          │                                               │
│          ├── Any EXPLICIT DENY matching action+resource? │
│          │   → YES → Return DENY (Deny ALWAYS wins)      │
│          │                                               │
│          ├── Any EXPLICIT ALLOW matching action+resource?│
│          │   → YES → Return ALLOW                        │
│          │                                               │
│          └── Neither?                                    │
│              → Return DEFAULT DENY                       │
│          ↓                                               │
│  Step 5: Emit audit event → Kafka → MongoDB              │
│                                                          │
│  TOTAL TIME TARGET: < 10ms                               │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

**Key Rule: Deny ALWAYS beats Allow.**
Even if a user has 10 policies that say `Allow s3:*`, if ONE policy says `Deny s3:DeleteObject`, the delete is **always denied**.

```javascript
// Policy Engine — Node.js Implementation
const evaluatePolicy = async (userId, action, resource) => {
    // Step 1: Check Redis cache
    const cacheKey = `policy:${userId}`;
    let policies = await redis.get(cacheKey);

    if (!policies) {
        // Step 2: Fetch user's groups from MySQL
        const groups = await db.query(
            'SELECT group_id FROM group_memberships WHERE user_id = ?', [userId]
        );

        // Step 3: Fetch all policies from MongoDB
        const userPolicies = await Policy.find({ 'attached_to.users': userId });
        const groupPolicies = await Policy.find({
            'attached_to.groups': { $in: groups.map(g => g.group_id) }
        });

        policies = [...userPolicies, ...groupPolicies];

        // Cache for 5 minutes
        await redis.setex(cacheKey, 300, JSON.stringify(policies));
    } else {
        policies = JSON.parse(policies);
    }

    // Step 4: Evaluate — Deny wins over Allow
    let decision = 'DEFAULT_DENY';

    for (const policy of policies) {
        for (const stmt of policy.statement) {
            if (matchesAction(stmt.action, action) && matchesResource(stmt.resource, resource)) {
                if (stmt.effect === 'Deny') return 'DENY';    // Explicit Deny — STOP immediately
                if (stmt.effect === 'Allow') decision = 'ALLOW';
            }
        }
    }

    return decision === 'ALLOW' ? 'ALLOW' : 'DENY';
};
```

---

## 6. 📈 SCALABILITY DESIGN

### 🧠 Think of it like this
> IAM is like airport security. At a tiny airport, 1 guard is enough. At a mega-airport (500M passengers/year), you need 100 security lanes running in parallel — but every single passenger must still be checked.

---

### Horizontal Scaling

```text
All services run in Docker containers managed by Kubernetes (EKS):

┌──────────────────────────────────────────────┐
│  Kubernetes Cluster                          │
│  ┌────────┐ ┌────────┐ ┌────────┐           │
│  │Auth x5 │ │User x3 │ │Policy  │           │
│  │Pods    │ │Pods    │ │Engine  │           │
│  │        │ │        │ │x20 Pods│ ← MOST    │
│  └────────┘ └────────┘ └────────┘   SCALED  │
│  ┌────────┐ ┌────────┐                      │
│  │Role x3 │ │Audit x5│                      │
│  │Pods    │ │Workers │                      │
│  └────────┘ └────────┘                      │
└──────────────────────────────────────────────┘
```

Policy Engine gets the most replicas because EVERY API call across the platform hits it.

### Caching (Redis)

| Data | Cache Duration (TTL) | Why |
|:-----|:--------------------|:----|
| Compiled user policies | 5 minutes | Policies rarely change; caching saves 99% of DB reads |
| Active JWT sessions | Token lifetime (1-24h) | Instant session validation without DB hit |
| User → Group mappings | 10 minutes | Group membership changes are infrequent |
| Rate limit counters | 1 minute sliding window | Track API calls per user for throttling |

### CDN Usage with Next.js

- Next.js dashboard static assets (JS bundles, CSS, fonts) served from CDN edge
- SSG documentation/help pages cached globally — zero server load
- **Security note:** Sensitive IAM data is NEVER cached on CDN — only static UI assets

### Database Scaling

| Strategy | MySQL | MongoDB |
|:---------|:------|:--------|
| **Replication** | Master (writes) + 5 Read Replicas (auth checks) | Primary + Secondary Replica Sets |
| **Partitioning** | Partition `audit_summary` by date range | Built-in sharding on `user_id` or `policy_id` |
| **Read/Write Split** | 99% reads (auth checks) → replicas, 1% writes (user creation) → master | Reads from secondaries for audit queries |

### Scaling Comparison Table (0 → 500M Identities)

| Identities | Policy Engine | MySQL | MongoDB | Redis | Special |
|:-----------|:-------------|:------|:--------|:------|:--------|
| **1K** | 1 instance | 1 DB | 1 instance | 1 node | Nothing special |
| **100K** | 5 pods + LB | Master + 2 replicas | Replica set | 3-node cluster | Add caching |
| **10M** | 20 pods (auto-scale) | Sharded (2 shards) + replicas | 3-shard cluster | 6-node cluster | Kafka for audit |
| **100M** | 50+ pods | Sharded (4 shards) | 10-shard cluster | Multi-AZ cluster | Multi-region |
| **500M** | 200+ pods (multi-region) | Sharded + partitioned | 50+ shards | Global cluster | Dedicated policy cache layer |

---

## 7. 🛡️ RELIABILITY & FAULT TOLERANCE

### 🧠 Think of it like this
> If the bank's vault lock breaks, you don't leave the vault open. You have backup locks, backup guards, and an alarm system. IAM is the vault lock of the cloud.

---

### What Happens If...

| Failure Scenario | Impact | Solution |
|:-----------------|:-------|:---------|
| **Policy Engine crashes** | ALL services get 503 — nothing works | Run 20+ replicas + Kubernetes auto-restart. LB routes to healthy pods. If ALL fail, **fail-closed** (deny everything) |
| **Redis cache goes down** | Policy checks take 50ms instead of 0.5ms | Redis Sentinel auto-promotes replica. App falls back to MySQL + MongoDB directly |
| **MySQL master crashes** | Can't create new users/groups, but auth checks still work (from Redis cache + replicas) | RDS Multi-AZ: automatic failover to standby in <60 seconds |
| **MongoDB goes down** | Can't fetch policies on cache miss | Replica set auto-promotes secondary. Cached policies in Redis continue to serve |
| **Kafka goes down** | Audit logs stop recording | Buffer audit events in-memory/local disk. Replay when Kafka recovers. Never block auth decisions for audit |
| **Entire region goes down** | Regional users affected | Multi-region deployment with DNS failover (Route 53) |

### Retry & Fallback Strategies

```text
Auth Check Request → Policy Engine
    ↓ Fails?
    → Retry (3 times with exponential backoff: 50ms, 200ms, 800ms)
    ↓ Still fails?
    → Fall back to stale Redis cache (last known policies)
    ↓ No cache?
    → FAIL CLOSED: Return DENY (security > availability for IAM)
```

**⚠️ Critical Design Decision: Fail CLOSED vs Fail OPEN**
- **Fail CLOSED (DENY ALL):** If we can't determine permissions, deny everything. Users are locked out temporarily, but no unauthorized access occurs.
- **Fail OPEN (ALLOW ALL):** If we can't check, let everyone through. Keeps services running but creates a massive security hole.
- **IAM must ALWAYS fail CLOSED.** Security is more important than availability for an access control system.

### Idempotency

| Operation | Problem Without Idempotency | Solution |
|:----------|:---------------------------|:---------|
| **Create User** | Network retry → duplicate user created | Check `username` UNIQUE constraint. Return existing user on conflict |
| **Attach Policy** | Retry → policy attached twice | Upsert pattern — attach is idempotent by design |
| **Audit Log Write** | Retry → duplicate log entries | Include `event_id` (UUID) — deduplicate on insert |

### Circuit Breaker Pattern

```text
CLOSED (Normal)           OPEN (Tripped!)           HALF-OPEN (Testing)
    │                         │                          │
All requests pass        All requests → DENY         Let 1 request through
to Policy Engine         immediately (fail-closed)        │
    │                    (don't overwhelm broken svc)     ↓
    ↓                         ↓                      If success → CLOSED
If failures > 5 in      After 30s timeout            If fail → OPEN
10 seconds → OPEN        → HALF-OPEN
```

---

## 8. 🔌 FLEXIBILITY & EXTENSIBILITY

### 🧠 Think of it like this
> A well-designed security system lets you add new camera types, new badge readers, and new alarm zones without rewiring the whole building.

---

### Adding Notifications (Async, Event-Driven)

```text
Admin detaches policy from user
    ↓
Policy Service emits event → Kafka topic: "policy.changes"
    ↓
Multiple consumers:
    ├── Cache Invalidator: Deletes user's Redis policy cache IMMEDIATELY
    ├── Notification Worker: Emails admin "Policy X removed from User Y"
    └── Compliance Logger: Creates compliance audit record
```

### Multi-Language (i18n)

- IAM Dashboard supports multiple languages via Next.js i18n routing
- Error messages returned by API are i18n-ready: `{ "code": "ACCESS_DENIED", "message_key": "error.access.denied" }` — frontend translates
- Audit logs always stored in English (canonical format)

### SEO Improvements using Next.js

- IAM Dashboard is internal, so SEO is less critical — BUT:
- Public documentation pages use SSG for fast, SEO-friendly rendering
- API reference docs use `getStaticProps` with MDX for structured content

### Domain-Specific Extensions

| Feature | Architecture Approach |
|:--------|:---------------------|
| **Service Control Policies (SCP)** | Organization-level policies in MongoDB, evaluated BEFORE user policies |
| **Permission Boundaries** | Additional policy layer that caps maximum permissions a user CAN have |
| **Temporary Credentials (STS)** | Separate Token Service that issues short-lived tokens when assuming roles |
| **Cross-Account Access** | Trust policies in Roles that allow external account IDs to assume the role |
| **Attribute-Based Access Control (ABAC)** | Policy conditions that check request attributes (IP, time, tags) |

---

## 9. 🛠️ DEV-FRIENDLY PRACTICES

### 🧠 Think of it like this
> The best security system is useless if the engineers maintaining it can't understand or update it safely.

---

### Project Structure

```text
iam-platform/
├── frontend/                        (Next.js Dashboard)
│   ├── pages/
│   │   ├── index.js                 (Dashboard Home — SSR)
│   │   ├── users/index.js           (User List — SSR)
│   │   ├── policies/editor.js       (Policy JSON Editor — CSR)
│   │   ├── audit/logs.js            (Audit Log Viewer — CSR)
│   │   └── docs/[...slug].js        (Documentation — SSG)
│   ├── components/
│   │   ├── PolicyBuilder.js          (Visual policy creator)
│   │   ├── UserTable.js
│   │   └── AuditTimeline.js
│   └── next.config.js
│
├── services/                        (Node.js Microservices)
│   ├── auth-service/
│   │   ├── routes/authRoutes.js
│   │   ├── controllers/authController.js
│   │   ├── services/jwtService.js
│   │   └── server.js
│   ├── user-service/
│   │   ├── routes/userRoutes.js
│   │   ├── controllers/userController.js
│   │   ├── models/User.js            (Sequelize — MySQL)
│   │   └── server.js
│   ├── policy-engine/
│   │   ├── engine/evaluator.js        (Core algorithm)
│   │   ├── engine/policyMerger.js
│   │   ├── cache/redisCache.js
│   │   └── server.js
│   ├── audit-service/
│   │   ├── consumers/kafkaConsumer.js
│   │   ├── models/AuditLog.js         (Mongoose — MongoDB)
│   │   └── server.js
│   └── role-service/
│       └── ...
│
├── shared/                          (Shared Libraries)
│   ├── middleware/
│   │   ├── authMiddleware.js
│   │   └── rateLimiter.js
│   ├── utils/
│   └── config/
│
├── docker-compose.yml
├── k8s/                             (Kubernetes manifests)
└── README.md
```

### CI/CD Pipeline

```text
Developer pushes code
        ↓
┌─────────────────────────────┐
│   GitHub Actions CI         │
├─────────────────────────────┤
│ 1. Lint (ESLint)            │
│ 2. Unit Tests (Jest)        │
│ 3. Security Scan (Snyk)     │ ← Extra for IAM!
│ 4. Integration Tests        │
│ 5. Policy Engine Benchmark  │ ← Must stay < 10ms
│ 6. Build Docker images      │
│ 7. Push to ECR              │
└───────────┬─────────────────┘
            ↓
┌─────────────────────────────┐
│   CD (Deploy)               │
├─────────────────────────────┤
│ Staging → Auto Deploy       │
│ Security Review → Manual    │ ← IAM changes need review
│ Production → Canary Deploy  │
│ (1% traffic → monitor →    │
│  roll out to 100%)          │
└─────────────────────────────┘
```

### Logging & Monitoring

| Tool | Purpose | What It Monitors |
|:-----|:--------|:----------------|
| **Winston** (Node.js) | Structured JSON logs | API errors, auth decisions, request latency |
| **Prometheus** | Metrics collection | Policy eval latency (p50, p95, p99), cache hit rate, auth failures/sec |
| **Grafana** | Dashboard visualization | Real-time graphs of all metrics |
| **ELK Stack** | Log aggregation | Search audit logs, debug auth failures |
| **PagerDuty** | Alerting | Alert if: auth failure rate > 10%, eval latency > 100ms, or cache hit rate < 90% |

**🚨 Critical Alerts:**
- 10+ `403 Forbidden` from same API key in 5 seconds → Possible brute-force → Slack/PagerDuty alert
- Policy Engine p99 latency > 50ms → Cache may be failing → Investigate Redis
- Cache hit rate drops below 80% → Cache eviction storm or misconfiguration

---

## 10. 📝 FINAL NOTES (BEGINNER FRIENDLY)

### Summary Table

| Section | Key Lesson |
|:--------|:-----------|
| **Requirements** | IAM has two jobs: Authentication (who are you?) and Authorization (what can you do?) |
| **Scale** | IAM is checked on EVERY API call — it must be the fastest service in the system |
| **Budget** | Redis caching is the best ROI investment — saves millions of DB reads per day |
| **HLD** | Polyglot: MySQL for identity (ACID), MongoDB for policies (JSON), Redis for speed |
| **LLD** | Policies are nested JSON → MongoDB. The evaluation algorithm must handle Deny > Allow > Default Deny |
| **Scalability** | Policy Engine needs the most replicas because it handles every single request |
| **Reliability** | IAM must FAIL CLOSED (deny all) — never fail open (allow all) |
| **Extensibility** | Event-driven architecture lets you add SCPs, ABAC, and STS without rewriting core |
| **Dev Practices** | Security scans in CI/CD + canary deployments for IAM changes |

### Key Takeaways

1. **Default Deny:** If no policy explicitly allows an action, it is denied. This is the golden rule of IAM.
2. **Deny Always Wins:** Even 100 Allow policies can't override 1 Deny policy. Security is conservative by design.
3. **Cache is Critical:** Policy evaluation must be <10ms. Redis caching gets you there. Without cache, you'd query MySQL + MongoDB on every single API call across the platform.
4. **Fail Closed:** If IAM can't determine permissions, deny everything. Security > Availability.
5. **Audit Everything:** Every allow, every deny, every login — logged asynchronously. You WILL need these logs during a security incident.
6. **Separate Identity from Permissions:** Users/Groups in MySQL (relational, ACID). Policies in MongoDB (flexible JSON). Don't force one DB to do both jobs.

### Common Mistakes Beginners Make

| ❌ Mistake | Why It's Wrong | ✅ Correct Approach |
|:-----------|:--------------|:-------------------|
| Storing policies in SQL tables | Policies are deeply nested JSON with variable structure; SQL requires rigid schemas | Store policies in MongoDB; query nested Action arrays natively |
| Checking permissions client-side | Client code can be modified by attackers | Always check on backend (Policy Engine server-side) |
| Caching policies forever | Admin removes access but user keeps working for hours | TTL of 5 min + immediate cache invalidation on policy change |
| No audit logging | Can't investigate breaches or prove compliance | Log EVERY decision (allow AND deny) asynchronously |
| Storing passwords in plain text | One DB breach exposes all credentials | Always hash with bcrypt (salt rounds ≥ 10) |
| Fail OPEN on errors | If Policy Engine is down, everyone has full access | Fail CLOSED — deny all when uncertain |
| Single Policy Engine instance | Single point of failure — one crash = entire platform locked | 20+ replicas with auto-scaling and health checks |
| Synchronous audit logging | Audit write blocks the auth response, adding 50ms+ latency | Async via Kafka — audit never slows down auth decisions |

---

## 11. 🎤 SCENARIO-BASED Q&A

### Q1: A Junior Developer tries to delete a Production database. Walk through what happens.
**Answer:** (1) Developer's CLI sends `DELETE /storage/prod-backup` with their JWT token. (2) API Gateway verifies JWT → extracts `user_id`. (3) Request forwarded to Policy Engine: `{ user: junior-dev, action: s3:DeleteObject, resource: arn:s3:::prod-backup }`. (4) Policy Engine checks Redis → cache miss. (5) Queries MySQL: user belongs to `Junior-Developers` group. (6) Queries MongoDB: `Junior-Developers` group has policy `S3-Read-Only` which only allows `s3:GetObject` and `s3:ListBucket`. No explicit Allow for `s3:DeleteObject`. (7) Decision Matrix: No Allow found → **Default DENY**. (8) Returns `403 Forbidden`. (9) Audit Service logs: "User junior-dev attempted unauthorized DeleteObject on prod-backup at 10:05 AM from IP 192.168.1.50." Crisis averted! 🛡️

### Q2: An admin revokes a user's access, but the user continues accessing resources for 5 minutes. Why?
**Answer:** This is the **cache invalidation problem**. The user's compiled policies were cached in Redis with a 5-minute TTL. The revocation updated MongoDB, but Redis still had the old "Allow" policies. **Solution:** When a policy is changed, the Policy Service must emit an event to Kafka. A Cache Invalidator consumer immediately deletes the user's Redis cache key (`DEL policy:{userId}`). The next auth check will miss cache, fetch fresh policies from MongoDB, and the revocation takes effect immediately. This is why event-driven architecture matters — you can't just rely on TTL expiry for security-critical changes.

### Q3: If Amazon has a massive sale day, authorization checks increase 10x. How does your system handle this?
**Answer:** (1) **Auto-scaling:** Kubernetes Horizontal Pod Autoscaler (HPA) detects increased CPU/request count on Policy Engine pods → automatically scales from 20 → 200 pods. (2) **Redis absorbs the load:** With a 95%+ cache hit rate, most checks never touch MySQL/MongoDB. Redis Cluster handles 1M+ reads/sec. (3) **Pre-warming:** Before known events (Prime Day), pre-load commonly accessed policies into Redis. (4) **Read replicas:** MySQL read replicas handle the 1% cache misses that need DB queries. (5) **Rate limiting:** API Gateway throttles individual users/services that exceed their quota, preventing one service from starving others.

### Q4: Why did you choose to mix MySQL and MongoDB instead of using just one database?
**Answer:** **MySQL** is perfect for identity data — users, groups, and memberships are inherently relational. "User A is in Group B which has Policy C" requires JOINs, which MySQL handles efficiently. ACID transactions ensure that when you delete a user, all their group memberships are atomically removed. **MongoDB** is perfect for policies — they are deeply nested JSON documents with variable structure (some policies have 2 statements, some have 50; some have Conditions blocks, some don't). Storing this in SQL would require either: (a) a generic `json_blob` column (wastes SQL's relational strengths) or (b) 10+ normalized tables (EAV anti-pattern, slow queries). MongoDB stores and queries nested JSON natively. This is **Polyglot Persistence** — use the best tool for each data shape.

### Q5: How would you write a Node.js algorithm to resolve conflicts between a group policy that Allows read and a user policy that Denies read?
**Answer:** The algorithm follows AWS's real evaluation logic: (1) Collect ALL policies attached to the user (directly + through groups + through roles). (2) Flatten all statements into a single list. (3) For the requested action, first scan for any **Explicit Deny** — if found, immediately return DENY (no further evaluation). (4) Then scan for any **Explicit Allow** — if found, mark as ALLOW. (5) If no Allow found, return **Default DENY**. The key insight: Deny is checked FIRST and wins unconditionally. This means a user policy with `Deny: s3:Read` will override even 10 group policies with `Allow: s3:*`. This is by design — it's always safer to deny than to accidentally allow.

### Q6: What happens if a hacker steals a JWT token? How do we mitigate this?
**Answer:** (1) **Short expiry:** JWTs expire in 1 hour, limiting the attack window. (2) **Session tracking:** Store session IDs in Redis. Admin can "kill" a session by deleting the Redis key — next API call with that JWT fails validation. (3) **IP binding:** Optionally bind JWT to origin IP. If the token is used from a different IP, flag and invalidate. (4) **MFA enforcement:** Even with a stolen JWT, sensitive actions (policy changes, user deletion) require re-authentication with MFA. (5) **Audit alerts:** If the same JWT is used from two different IPs simultaneously, trigger an automatic session invalidation and alert. (6) **Access key rotation:** For programmatic keys, enforce 90-day rotation and alert on keys older than threshold.

### Q7: The Policy Engine is a single point of failure. If it goes down, nobody can do anything. How do we prevent this?
**Answer:** (1) **Redundancy:** Run 20+ Policy Engine pods across multiple Availability Zones. Kubernetes restarts crashed pods within seconds. (2) **Load Balancer health checks:** ALB pings each pod every 10 seconds. Unhealthy pods are removed from rotation immediately. (3) **Graceful degradation:** If Policy Engine latency exceeds threshold, Circuit Breaker trips → requests fail-closed (DENY ALL) instead of hanging. (4) **Multi-region:** Deploy Policy Engine in 3+ AWS regions. If an entire region fails, DNS failover (Route 53) redirects traffic to another region. (5) **Cached fallback:** Even if all Policy Engine pods restart simultaneously, Redis still holds cached policies. A lightweight "cache-only evaluator" can serve from Redis during recovery — slightly stale but functional. (6) **Chaos engineering:** Regularly kill Policy Engine pods in staging to verify recovery mechanisms work.

### Q8: How do you handle millions of policies being evaluated for a single user who belongs to 15 groups?
**Answer:** Without optimization, checking a user in 15 groups with 5 policies each = 75 policy documents × 10 statements each = 750 statement evaluations per request. At 100K RPS, that's 75M statement evaluations/second — too slow. **Optimization:** (1) **Pre-compile at write time:** When a policy is attached/detached, compute the user's "effective policy" (merged result of all policies) and store it as a single Redis hash map: `{ "s3:Read": "Allow", "s3:Delete": "Deny", "ec2:*": "Allow" }`. (2) **Evaluation becomes O(1):** Look up `action` in hash map → instant. (3) **Invalidate on change:** Any policy/group membership change triggers recompilation for affected users. (4) **Lazy compilation:** Only compile when the user makes their next request (cache miss) — don't eagerly recompile for users who haven't logged in for months.

---

> **🎓 Study Tip:** IAM is unique because security is MORE important than availability. In most systems, we prioritize uptime. In IAM, we prioritize correctness — it's better for everyone to be locked out for 30 seconds than for one unauthorized user to access production data.
