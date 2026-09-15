# 📚 System Design Course — Master Index

> Built for developers with JavaScript, Node.js, React, MongoDB, PostgreSQL, Redis, and AWS experience.
> All examples use this stack. Beginner-to-advanced learning path.

---

## 📂 HLD — High Level Design

Covers the big-picture architecture decisions every system designer must know.

| # | Topic | Description |
|---|-------|-------------|
| [01](HLD/01_Introduction_System_Design.md) | Introduction to System Design | Goals, terminology, interview strategy |
| [02](HLD/02_Scalability_Basics.md) | Scalability Basics | Vertical vs horizontal scaling, stateless design |
| [03](HLD/03_Latency_vs_Throughput.md) | Latency vs Throughput | Performance metrics, async processing |
| [04](HLD/04_Load_Balancing.md) | Load Balancing | Algorithms, health checks, L7 vs L4 |
| [05](HLD/05_Caching.md) | Caching | Cache-Aside, Write-Through, eviction (Redis) |
| [06](HLD/06_Database_Basics.md) | Database Basics | ACID, connection pooling, schema design |
| [07](HLD/07_SQL_vs_NoSQL.md) | SQL vs NoSQL | PostgreSQL vs MongoDB selection criteria |
| [08](HLD/08_Indexing_and_Partitioning.md) | Indexing and Partitioning | B-trees, GIN indexes, range partitioning |
| [09](HLD/09_Replication_and_Sharding.md) | Replication and Sharding | Consistent hashing, read replicas |
| [10](HLD/10_CAP_Theorem.md) | CAP Theorem | CP vs AP trade-offs, PACELC |
| [11](HLD/11_Consistency_Models.md) | Consistency Models | Eventual to strong consistency spectrum |
| [12](HLD/12_API_Design.md) | API Design | REST principles, versioning, error handling |
| [13](HLD/13_Rate_Limiting.md) | Rate Limiting | Token Bucket, Sliding Window (Redis) |
| [14](HLD/14_Message_Queues.md) | Message Queues | SQS, Bull, fan-out, DLQ patterns |
| [15](HLD/15_Event_Driven_Architecture.md) | Event-Driven Architecture | Pub/Sub, Event Sourcing, Saga pattern |
| [16](HLD/16_Microservices.md) | Microservices | Service communication, Circuit Breaker |
| [17](HLD/17_Monolith_vs_Microservices.md) | Monolith vs Microservices | Decision framework, strangler fig migration |
| [18](HLD/18_Storage_Systems.md) | Storage Systems | S3, EBS, data tiering, choosing storage |
| [19](HLD/19_Content_Delivery_Network.md) | CDN | CloudFront, cache-control, invalidation |
| [20](HLD/20_Search_Design.md) | Search Design | Elasticsearch, inverted index, autocomplete |
| [21](HLD/21_Logging_and_Monitoring.md) | Logging and Monitoring | Logs, Metrics, Traces — AWS X-Ray/CloudWatch |
| [22](HLD/22_Security_Basics.md) | Security Basics | OWASP Top 10, bcrypt, CORS, Helmet.js |
| [23](HLD/23_Authentication_and_Authorization.md) | Authentication & Authorization | JWT, OAuth, RBAC, 2FA |

---

## 📂 LLD — Low Level Design

Covers object-oriented design, design patterns, and implementation-level decisions.

| # | Topic | Description |
|---|-------|-------------|
| [01](LLD/01_Object_Oriented_Design.md) | Object Oriented Design | Classes, encapsulation, inheritance, polymorphism |
| [02](LLD/02_SOLID_Principles.md) | SOLID Principles | SRP, OCP, LSP, ISP, DIP with Node.js examples |
| [03](LLD/03_Design_Patterns_Overview.md) | Design Patterns Overview | Creational, Structural, Behavioral categories |
| [04](LLD/04_Creational_Patterns.md) | Creational Patterns | Singleton, Factory, Builder, Prototype |
| [05](LLD/05_Structural_Patterns.md) | Structural Patterns | Adapter, Decorator, Facade, Proxy, Composite |
| [06](LLD/06_Behavioral_Patterns.md) | Behavioral Patterns | Observer, Strategy, Command, Template, State |
| [07](LLD/07_Database_Design.md) | Database Design | Normalization, relationships, indexes, transactions |
| [08](LLD/08_API_Design_LLD.md) | API Design (LLD) | Validation (Zod), response format, error handling |
| [09](LLD/09_Caching_Strategy.md) | Caching Strategy (LLD) | Cache-Aside, stampede prevention, Redis data structures |
| [10](LLD/10_Concurrency_and_Async.md) | Concurrency & Async | Promise.all, p-limit, generators, worker threads |

---

## 🏗️ System Design Case Studies

Full end-to-end design for 11 real-world systems. Each includes requirements, capacity estimation, architecture diagram, core implementation code, database schema, and interview discussion points.

| # | System | Key Topics Covered |
|---|--------|--------------------|
| [01](01_Design_URL_Shortener.md) | URL Shortener (bit.ly) | Base62 encoding, redirect performance, analytics at scale |
| [02](02_Design_Instagram.md) | Instagram | Photo pipeline, feed fanout, like counter optimization |
| [03](03_Design_WhatsApp.md) | WhatsApp | WebSocket scaling, offline delivery, E2E encryption |
| [04](04_Design_Uber.md) | Uber | Redis Geospatial, 1M location writes/sec, surge pricing |
| [05](05_Design_Netflix.md) | Netflix | HLS streaming, CDN strategy, recommendation systems |
| [06](06_Design_Twitter.md) | Twitter | Celebrity problem, timeline pre-computation, trending |
| [07](07_Design_Dropbox.md) | Dropbox | Block-based storage, delta sync, deduplication |
| [08](08_Design_Google_Drive.md) | Google Drive | OT for collaboration, permission cascading, resumable uploads |
| [09](09_Design_Auth_Access_Refresh_Token.md) | Access & Refresh Token System | JWT, Rotation (RTR), Reuse Detection, Axios Interceptor Queue, Redis Blacklist |
| [10](10_Design_Role_Based_Access_Control_RBAC.md) | Role-Based Access Control (RBAC) | Granular Permissions, Redis Cache, ABAC Ownership Policy, React UI Gating |
| [11](11_MFA_System_Design_MERN_Ecommerce.md) | Multi-Factor Authentication (MFA) | TOTP (RFC 6238), WebAuthn/Passkeys, SMS/Email OTP, Step-Up Auth, Trusted Devices, Redis State Machine |

---

## 📱 Social Integration & Universal Lead Attribution System Design

Comprehensive 19-part master architecture guide for Lead Management Systems (LMS) with multi-channel attribution (Instagram, Facebook, LinkedIn, X, YouTube, Google Ads, Offline QR, Sales Team).

| # | Topic | Key Concepts Covered |
|---|-------|----------------------|
| [01](social_integration/01_Lead_Attribution_Fundamentals.md) | Lead Attribution Fundamentals | Lead definitions, Source/Medium/Campaign taxonomy, Multi-touch journeys |
| [02](social_integration/02_Source_Medium_Campaign_Model.md) | Source, Medium & Campaign Data Model | Governed taxonomy, enums vs DB dictionary, click IDs, normalization |
| [03](social_integration/03_Social_Media_Lead_Architecture.md) | Social Media Lead Architecture | Adapter/Strategy/Factory patterns, ingestion gateway, modular monolith |
| [04](social_integration/04_Instagram_Lead_Integration.md) | Instagram Lead Integration | Meta Graph API, instant forms, DM automation, webhook subscriptions |
| [05](social_integration/05_Facebook_Lead_Integration.md) | Facebook Lead Integration | Page access tokens, long-lived token exchange, multi-tenant mapping |
| [06](social_integration/06_LinkedIn_Lead_Integration.md) | LinkedIn Lead Integration | Lead Gen Forms, URN data mapping, OAuth refresh rotation, rate limiting |
| [07](social_integration/07_X_Twitter_Lead_Integration.md) | X / Twitter Lead Integration | Tracking links, twclid capture, landing page attribution, CAPI sync |
| [08](social_integration/08_YouTube_Lead_Integration.md) | YouTube Lead Integration | Video descriptions, timestamps, pinned comments, TV-to-web cross-device |
| [09](social_integration/09_Website_UTM_Tracking.md) | Website & UTM Tracking | Client SDK, 1st-party cookie persistence, dual-slot first/last touch, SPAs |
| [10](social_integration/10_Offline_Lead_Attribution.md) | Offline Lead Attribution | Dynamic QR codes, Dynamic Number Insertion (DNI), telephony webhooks |
| [11](social_integration/11_Lead_Normalization_and_Deduplication.md) | Normalization & Deduplication | E.164 phone parsing, RFC 5322 email, deterministic identity matching |
| [12](social_integration/12_Attribution_Data_Model.md) | Attribution Data Model (MongoDB) | `leads`, `leadTouchpoints`, `externalLeadMappings`, compound indexes |
| [13](social_integration/13_Lead_Ingestion_Architecture.md) | Lead Ingestion Architecture | BullMQ queue buffer, async worker pipelines, distributed idempotency |
| [14](social_integration/14_Campaign_Attribution.md) | Campaign Attribution | Multi-tier campaign hierarchy, CAC/ROAS queries, attribution windows |
| [15](social_integration/15_Analytics_and_Reporting.md) | Analytics & Reporting | First-touch, Last-touch, U-Shaped, Time-Decay models, OLTP vs OLAP |
| [16](social_integration/16_Security_and_OAuth.md) | Security & OAuth | AES-256-GCM envelope encryption (KMS), HMAC verification, RBAC |
| [17](social_integration/17_Webhooks_and_Event_Processing.md) | Webhooks & Event Processing | Idempotency locks (`SETNX`), DLQ state machines, out-of-order sequencing |
| [18](social_integration/18_Scaling_and_Reliability.md) | Scaling & Reliability | 10K to 100M+ scale tiers, circuit breakers, KEDA queue autoscaling |
| [19](social_integration/19_Implementation_Guide.md) | Complete Implementation Guide | MERN architecture, REST APIs, 6 data flows, 18 pitfalls, reference diagram |

---

## 🛠️ Tech Stack Reference

All examples in this course use:

| Layer | Technology |
|-------|-----------|
| Runtime | Node.js (JavaScript) |
| Web Framework | Express.js |
| SQL Database | PostgreSQL (`pg` library) |
| NoSQL Database | MongoDB (`mongoose`) |
| Cache | Redis (`ioredis`) |
| Message Queue | AWS SQS + Bull (Redis) |
| File Storage | AWS S3 |
| CDN | AWS CloudFront |
| Compute | AWS EC2 / ECS / Lambda |
| Search | Elasticsearch |
| Real-time | Socket.IO |
| Validation | Zod / Joi |
| Authentication | JWT + bcrypt |
| Monitoring | AWS CloudWatch + X-Ray + Winston |

---

## 🎓 Learning Path

```
Beginners → Start with HLD 01-07 (core concepts)
Intermediate → HLD 08-17 (distributed systems)
Advanced → HLD 18-23 + Case Studies
LLD → After HLD, for interview practice on object-oriented design
```

---

## 📋 Interview Checklists

### Before System Design Interview:
- [ ] Practice estimating: QPS, Storage, Bandwidth
- [ ] Know when to use SQL vs NoSQL
- [ ] Know when to add a cache, and what to cache
- [ ] Understand fan-out (push vs pull for feeds)
- [ ] Explain CAP theorem trade-offs for your design
- [ ] Know how to scale: Load balancers, replicas, sharding
- [ ] Security: Rate limiting, auth, HTTPS

### During Interview:
1. Clarify requirements (5 min)
2. Estimate scale (5 min)
3. High-level design (15 min)
4. Deep dive on interesting components (20 min)
5. Address bottlenecks and scaling (10 min)
6. Security and monitoring (5 min)
