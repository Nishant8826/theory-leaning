# 🏗️ AWS IAM System Design (Enterprise Level)

## 1. 📌 Introduction
### What is IAM?
IAM (Identity and Access Management) is the core security system of any cloud service. It acts as the grand "Security Checkpoint" that determines **who** is allowed into the system (Authentication) and **what** they are allowed to do once inside (Authorization).

### Why Companies Need IAM
Without IAM, any employee or software bug could accidentally delete production databases, read highly sensitive customer data, or launch thousands of expensive servers. IAM provides precise, granular control over every single action taken within a network.

### Real-World Analogy 🏢
Think of a massive hospital:
- **Authentication:** The front desk checks your ID and gives you a visitor badge (You proved who you are).
- **Authorization:** Your badge has an RFID chip. It opens the cafeteria door, but if you try to open the surgical operating room, the light flashes red and the door stays locked. (You don't have permission).

---

## 2. 🎯 Requirements

### ✅ Functional Requirements
- **Create users:** Admins can create individual user accounts.
- **Create groups:** Group users logically (e.g., `Developers`, `HR`).
- **Assign users to groups:** Easily grant multiple users the same permissions.
- **Create roles:** Temporary permissions meant to be assumed by services (e.g., automated scripts).
- **Attach/detach policies:** Define exact rules (Allow/Deny) and attach them to users, groups, or roles.
- **Authentication (login):** Validate user credentials securely.
- **Authorization (access control):** Evaluate every API request against attached policies.
- **Generate access keys:** Programmatic access for bots/tools like Terraform or Jenkins.
- **Audit logs:** Record "who did what, when, and from where" for compliance.

### ⚙️ Non-Functional Requirements
- **High availability (99.99%):** If IAM goes down, the entire cloud platform is inaccessible.
- **Low latency (<100ms):** Every single API call across the platform must first pass through an IAM check; it must be blazing fast.
- **Strong security:** Must withstand brutal attacks, prevent brute-forcing, and safeguard data.
- **Scalability:** Able to support millions of users and billions of access checks per day.
- **Fault tolerance:** Redundancy across multiple geographic regions.
- **Auditability:** Tamper-proof logs of every security decision.

---

## 3. 🏗️ High-Level Design (HLD)

To achieve low latency and high scalability, we use a distributed microservices architecture.

### Architecture Diagram

```text
       [ Next.js UI / CLI ]
                │
                ▼
       [ API Gateway (Nginx/Express) ]
                │
    ┌───────────┼────────────┬─────────────┐
    ▼           ▼            ▼             ▼
[ Auth ]    [ User ]     [ Policy ]    [ Audit ]
[Service]   [Service]    [ Engine ]    [Service]
    │           │            │             │
    ▼           ▼            ▼             ▼
[Redis ]    [ PostgreSQL DB ]        [ MongoDB ]
(Cache)     (Users, Groups)          (Logs)
```

### Components & Tech Stack
- **Frontend (Next.js / React.js):** Provides a high-performance, dynamic admin dashboard to manage users and policies visually.
- **Backend (Node.js + Express.js):** Microservices architecture. Node.js is excellent for highly concurrent, I/O-bound tasks like passing tokens and hitting databases.
- **API Gateway:** Routes incoming traffic, terminates SSL/TLS, and does initial rate-limiting.
- **Databases:** 
  - **SQL (PostgreSQL):** For highly relational data (Users, Groups, Mappings).
  - **NoSQL (MongoDB):** For massive, unstructured JSON data like Policies and Audit Logs.
- **Cache (Redis):** Stores active JWT sessions and frequently accessed policies to guarantee `<100ms` low-latency checks.
- **Auth Tokens (JWT):** Stateless JSON Web Tokens securely pass user identity between microservices without querying the DB every time.

---

## 4. 🔍 Low-Level Design (LLD)

### Data Models

**1. User (PostgreSQL)**
- `id` (UUID, Primary Key)
- `username` (String, Unique)
- `password_hash` (String, bcrypt)
- `mfa_enabled` (Boolean)

**2. Group (PostgreSQL)**
- `id` (UUID, Primary Key)
- `name` (String)

**3. GroupMembership (Join Table - PostgreSQL)**
- `user_id` (UUID)
- `group_id` (UUID)

**4. Policy (MongoDB)**
Because AWS IAM policies are deep JSON objects, MongoDB is the perfect choice for storing and querying them.

*Example JSON Policy:*
```json
{
  "Version": "2026-03-31",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:Read", "s3:List"],
      "Resource": "arn:aws:s3:::company-images/*"
    },
    {
      "Effect": "Deny",
      "Action": ["s3:Delete"],
      "Resource": "*"
    }
  ]
}
```

### Allow vs Deny Logic
The Policy Engine strictly follows this evaluation logic:
1. **Default Deny:** If an action isn't explicitly allowed, it's denied.
2. **Explicit Deny overrides ALLOW:** Even if the user has 10 Allow policies, but 1 Deny policy for an action, the result is ALWAYS **Deny**.

---

## 5. 🔐 Authentication Flow

1. **User Login:** The user opens the Next.js UI and submits `username` and `password`.
2. **Gateway:** API Gateway routes the request to the `Auth Service`.
3. **Password Validation:** `Auth Service` fetches the `password_hash` from PostgreSQL and compares it using `bcrypt`.
4. **Token Generation (JWT):** Upon success, the service generates a JWT signed with a secret key. The JWT payload contains the `user_id` and an expiration time.
5. **Session Handling:** The JWT is returned to the Client securely (HttpOnly Cookie) and the Session ID is cached in **Redis** for quick invalidation if the user logs out.

---

## 6. 🔑 Authorization Flow (CORE)

This is the most critical and highly-trafficked path in the system.

1. **Request:** User tries to read a database. The request hits the API Gateway with the JWT token in the header.
2. **Extract Identity:** API Gateway verifies the JWT signature. If valid, it extracts the `user_id` and forwards the request to the `Policy Engine`.
3. **Fetch Policies:** `Policy Engine` looks up Redis Cache for the user's policies. If not in cache, it queries PostgreSQL for the user's groups, then queries MongoDB for all attached JSON policies. (Then caches the result in Redis).
4. **Evaluate Rules:** The Engine merges all policies, evaluates the requested action (`db:Read`) against the rules.
5. **Decision:** If allowed, the request proceeds to the actual Database Service. If denied, it immediately returns an `HTTP 403 Forbidden`.
6. **Audit:** A message is sent to the `Audit Service` to log this event asynchronously.

---

## 7. ⚙️ API Design

RESTful endpoints built with Express.js:

- **`POST /api/v1/auth/login`**
  - **Body:** `{ "username": "...", "password": "..." }`
  - **Response:** `200 OK`, `Set-Cookie: jwt=token...`

- **`POST /api/v1/users`** (Create User)
  - **Body:** `{ "username": "alice", "email": "alice@company.com" }`
  - **Response:** `201 Created`

- **`POST /api/v1/groups/:groupId/users`** (Assign user to group)
  - **Body:** `{ "userId": "uuid-123" }`
  - **Response:** `200 OK`

- **`POST /api/v1/policies`** (Create JSON Policy)
  - **Body:** `{ "name": "S3ReadOnly", "document": { ...JSON... } }`
  - **Response:** `201 Created`

- **`POST /api/v1/authz/evaluate`** (Internal API used by other microservices)
  - **Body:** `{ "userId": "uuid", "action": "s3:Read", "resource": "arn:s3:::bucket" }`
  - **Response:** `{ "decision": "Allow" }` *(Must be under 10ms!)*

---

## 8. 🗄️ Database Design

### Why a Hybrid Database Strategy?
- **PostgreSQL:** IAM requires strict consistency for Identities. If we remove a user from a group, it must happen transactionally. SQL guarantees this via ACID compliance. Indexing on `username` allows instant lookups.
- **MongoDB:** Policies are highly nested JSON documents (Action arrays, Resource strings, Condition blocks). SQL struggles with dynamic schemas; NoSQL parses JSON natively and allows querying inside nested arrays.

### Relationships
- `User` ⟷ `Group` (Many-to-Many)
- `Group` ⟷ `Policy` (Many-to-Many via mappings)
- `User` ⟷ `Policy` (Many-to-Many via mappings)

---

## 9. 🚀 Scalability Design

To handle millions of users and high throughput:

1. **Horizontal Scaling:** Run multiple instances of Node.js `Auth Service` and `Policy Engine` in Docker containers managed by Kubernetes.
2. **Load Balancers:** Distribute incoming API Gateway traffic evenly across all Node.js containers.
3. **Caching (Redis Cluster):** Policy evaluation requires heavy compute. We cache the final parsed policy mapping for a user in Redis. Read speeds go from `~50ms` (DB) to `<1ms` (Redis).
4. **Read Replicas:** IAM is extremely read-heavy (99% Authorization checks, 1% Identity creation). We use Master PostgreSQL/MongoDB for Writes, and multiple Read Replicas distributed globally.
5. **Asynchronous Auditing:** Logging every action blocks the event loop. We push audit logs to a message queue (e.g., Kafka / RabbitMQ), and a background worker swallows them into MongoDB.

---

## 10. 🔒 Security Design

- **Encryption in Transit:** Strict TLS (HTTPS) on all API Gateway endpoints.
- **Encryption at Rest:** PostgreSQL and MongoDB disks are encrypted (AES-256).
- **Password Hashing:** Passwords are never stored in plaintext. We use `bcrypt` with a strong salt round so that even if the DB is stolen, passwords cannot be reversed.
- **MFA (Multi-Factor Auth):** Requires Time-based One Time Passwords (TOTP) to validate human identities.
- **Key Rotation:** Access keys (for bot accounts) enforce automatic rotation alerts every 90 days.
- **Principle of Least Privilege:** Users start with **Zero** permissions by default until a policy explicitly grants access.

---

## 11. 📊 Logging & Monitoring

- **Audit Logs:** Every successful and failed authorization attempt is logged in MongoDB (Who, What, When, IP Address).
- **Monitoring (ELK Stack):** Elasticsearch, Logstash, and Kibana are used to visualize traffic.
- **Alerts:** If the system detects 10 `HTTP 403 Forbidden` errors from the same API key within 5 seconds, an alert is sent via Slack/PagerDuty to DevOps (possible brute-force or misconfigured script).

---

## 12. 💰 Budget Estimation

*Rough Monthly Costs (AWS Pricing)*

**Startup (Small Scale - 100s of users)**
- Single EC2 instance for Node.js: ~$10
- Managed PostgreSQL (Small): ~$15
- Managed MongoDB Atlas: ~$15
- Redis (Micro): ~$15
- **Total:** ~$55/month

**Enterprise (Mid-Large Scale - Millions of users)**
- Auto-scaling EKS (Kubernetes) Node.js Clusters: ~$500+
- Multi-AZ PostgreSQL (Large): ~$300
- Sharded MongoDB cluster: ~$400
- Redis Cluster (High Availability): ~$200
- API Gateway & Load Balancers: ~$100
- **Total:** ~$1,500 - $3,000+/month

---

## 13. ⚠️ Challenges & Trade-offs

1. **Security vs Performance:** We must check permissions on *every* request. Hitting the database every time is secure but slow. To fix this, we trade some consistency for performance by using Redis caching.
2. **Cache Invalidation:** If an admin revokes a user's access, but that policy is cached in Redis for 5 minutes, the user maliciously still has access for 5 minutes!
   > *Solution:* When a policy updates, the backend must emit an event to immediately clear that specific user's Redis cache key.
3. **Complexity of JSON Policies:** Finding overlapping "Allows" and "Denies" across 20 different JSON files for one user requires a very optimized `Policy Engine` algorithm.

---

## 14. 🏋️ Real-World Scenario

**Scenario:** Junior Developer tries to delete a Production Storage Bucket.

1. Developer CLI sends: `DELETE /storage/prod-database-backup` with their JWT token.
2. API Gateway forwards JWT to `Policy Engine`.
3. `Policy Engine` inspects Redis. Cache miss.
4. Engine queries PostgreSQL: "User belongs to `Junior-Dev` group."
5. Engine queries MongoDB: Fetches JSON policy for `Junior-Dev`.
6. Engine evaluates policy: Finds `Effect: Allow, Action: s3:Read`, but no explicitly allowed `s3:Delete`.
7. **Decision Matrix:** Default = Deny. Result = DENY.
8. Engine returns `403 Forbidden`.
9. `Audit Service` logs: `User [Junior-Dev] attempted Unauthorized Delete on [prod-backup] at 10:05 AM`. Crisis averted! 🛡️

---

## 15. 🎤 Interview Questions

1. **IAM vs Identity Provider (IdP):** How is AWS IAM different from Okta or Google Auth?
2. **Handling High Load:** If Amazon has a big sale day, authorization checks 10x. How does your system scale instantly?
3. **The Cache Problem:** Explain exactly how you handle cache invalidation when a user's permissions are abruptly removed.
4. **Relational vs NoSQL:** Why did you choose to mix PostgreSQL and MongoDB instead of just using one?
5. **JSON Policy Parsing:** How would you write a Node.js algorithm to resolve conflicts between a group policy that Allows read, and a user policy that Denies read?
6. **JWT Security:** What happens if a hacker steals a JWT token? How do we mitigate this?
7. **Single Point of Failure:** If the Policy Engine goes down, nobody can do anything. How do we prevent this?
8. **Stateless vs Stateful:** Why are JWTs stateless, and why is that important for scaling our Express.js servers?

---

## 16. 📝 Summary

| Component | Responsibility | Key Takeaways |
| :--- | :--- | :--- |
| **User/Auth Service** | Verifies passwords, issues JWTs | Needs strong hashing (`bcrypt`) and secure token transport. |
| **Policy Engine** | Reads JSON, evaluates Allow/Deny | Must be ultra-fast using Redis caching. Default Deny rules! |
| **PostgreSQL DB** | Stores relational users/groups | Perfect for strict, ACID-compliant identity mapping. |
| **MongoDB**| Stores complex JSON policies | Easily schema-less, handles deeply nested permissions arrays. |
| **Redis Cache** | Caches identities & policies | Reduces DB load, heavily speeds up the critical <100ms path. |
| **Audit Service** | Logs all activity | Decoupled via async queues so it doesn't slow down the main system. |

---
*End of Design Document - Architecture Mastered!* 🏗️☁️
