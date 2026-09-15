# 19 — Complete Implementation Guide

## 📌 1. Master System Blueprint & Tech Stack

This implementation guide consolidates the entire architectural blueprint for an enterprise-ready **Lead Management System (LMS)** with universal multi-channel lead attribution.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                 PRODUCTION TECH STACK                                  │
├───────────────────┬────────────────────────────────────────────────────────────────────┤
│ **Frontend**      │ React 18+ / Next.js (TypeScript, TailwindCSS, TanStack Query)      │
│ **Backend API**   │ Node.js 20+ LTS / Express.js (Modular Monolith, Strict TypeScript) │
│ **Database**      │ MongoDB 7.0+ (WiredTiger Engine, Replica Set / Sharded Cluster)    │
│ **Cache / Queue** │ Redis 7.2+ (BullMQ distributed job processing & idempotency locks) │
│ **Object Storage**│ AWS S3 (Encrypted CSV exports and raw payload cold-storage)        │
│ **Secrets / KMS** │ AWS KMS + Secrets Manager (Envelope Encryption for OAuth tokens)   │
│ **Monitoring**    │ OpenTelemetry + Prometheus + Grafana + Winston Structured Logs     │
└───────────────────┴────────────────────────────────────────────────────────────────────┘
```

---

## 📁 2. Clean Modular Directory Structure

```
src/
├── app.ts                         # Express app configuration & middleware pipeline
├── server.ts                      # Server bootstrap & graceful shutdown hooks
├── config/                        # Environment, Redis, MongoDB, and KMS configs
│   ├── database.ts
│   ├── redis.ts
│   └── security.ts
├── common/                        # Cross-cutting utilities & middleware
│   ├── middleware/
│   │   ├── auth.middleware.ts     # JWT validation & Tenant Context injector
│   │   ├── rbac.middleware.ts     # Role-based access control
│   │   └── rate-limiter.ts        # Redis-backed rate limiting
│   ├── errors/                    # Domain error classes
│   └── utils/
│       ├── encryption.util.ts     # AES-256-GCM envelope encryption helpers
│       ├── phone.util.ts          # E.164 phone normalizer (libphonenumber-js)
│       └── slugify.util.ts        # UTM & Campaign string sanitizers
├── modules/
│   ├── leads/                     # Core Lead Domain
│   │   ├── controllers/
│   │   ├── services/
│   │   ├── models/
│   │   │   ├── Lead.ts            # Canonical Lead Mongoose model
│   │   │   └── LeadTouchpoint.ts  # Time-series immutable touchpoints model
│   │   ├── routes/
│   │   └── dtos/
│   ├── attribution/               # Attribution & Taxonomy Engine
│   │   ├── services/
│   │   │   ├── AttributionService.ts
│   │   │   └── NormalizerService.ts
│   │   └── models/
│   │       ├── LeadSource.ts      # Governed Sources dictionary
│   │       └── LeadCampaign.ts    # Campaign definitions & UTM rules
│   ├── integrations/              # Social Media & Multi-Channel Adapters
│   │   ├── base/
│   │   │   ├── ISocialAdapter.ts
│   │   │   └── SocialAdapterFactory.ts
│   │   ├── adapters/
│   │   │   ├── MetaAdapter.ts     # Shared Meta Graph client
│   │   │   ├── InstagramAdapter.ts
│   │   │   ├── FacebookAdapter.ts
│   │   │   ├── LinkedInAdapter.ts
│   │   │   ├── TwitterAdapter.ts
│   │   │   └── TelephonyAdapter.ts
│   │   └── models/
│   │       ├── SocialIntegration.ts
│   │       └── ExternalLeadMapping.ts
│   ├── webhooks/                  # Inbound Webhook Gateway & Workers
│   │   ├── controllers/
│   │   │   └── WebhookController.ts
│   │   ├── queues/
│   │   │   └── ingestion.queue.ts # BullMQ queue initialization
│   │   └── workers/
│   │       └── ingestion.worker.ts# Asynchronous lead processor
│   └── analytics/                 # Reporting & Multi-Touch Attribution
│       ├── controllers/
│       └── services/
│           ├── MultiTouchEngine.ts# Linear, U-Shaped, Time-Decay calculations
│           └── FunnelReportService.ts
```

---

## 🌐 3. Complete REST API Specifications

### 1. Ingest Inbound Lead (`POST /api/v1/leads`)
* **Purpose**: General-purpose ingestion for website webforms, landing pages, mobile apps, and third-party partners.
```http
POST /api/v1/leads HTTP/1.1
Host: api.lms.acme.com
Authorization: Bearer <JWT_OR_API_KEY>
Content-Type: application/json

{
  "name": "Alex Rivera",
  "email": "alex.rivera@enterprise.com",
  "phone": "+14155552671",
  "source": "instagram",
  "medium": "paid_social",
  "campaign": "summer_sale_2026",
  "content": "video_explainer_v1",
  "term": "enterprise_crm",
  "clickId": "fbclid_IwAR28301982039",
  "landingPage": "https://acme.com/demo?utm_source=instagram...",
  "referrer": "https://l.instagram.com/",
  "customFields": {
    "companySize": "100-500",
    "industry": "Fintech"
  }
}
```

```http
HTTP/1.1 201 Created
Content-Type: application/json

{
  "success": true,
  "leadId": "65f3a9b1c8e123456789abcd",
  "isDuplicate": false,
  "status": "new",
  "firstTouch": {
    "source": "instagram",
    "medium": "paid_social",
    "campaign": "summer_sale_2026"
  }
}
```

---

### 2. Platform Webhook Ingestion Gateway (`POST /api/v1/webhooks/:platform`)
* **Purpose**: Ultra-fast edge endpoint for Meta, LinkedIn, X, and Twilio webhooks.
```http
POST /api/v1/webhooks/facebook HTTP/1.1
Host: api.lms.acme.com
X-Hub-Signature-256: sha256=d5b8e92a8f...
Content-Type: application/json

{
  "object": "page",
  "entry": [
    {
      "id": "847291048201",
      "time": 1718449200,
      "changes": [
        {
          "field": "leadgen",
          "value": {
            "leadgen_id": "109823487123984",
            "page_id": "847291048201",
            "form_id": "48291048123"
          }
        }
      ]
    }
  ]
}
```

```http
HTTP/1.1 200 OK
Content-Type: application/json

{ "received": true, "status": "enqueued" }
```

---

### 3. Connect Social Integration (`POST /api/v1/integrations/:platform/connect`)
* **Purpose**: Authenticate and persist long-lived OAuth tokens for a tenant.
```http
POST /api/v1/integrations/facebook/connect HTTP/1.1
Authorization: Bearer <TENANT_ADMIN_JWT>
Content-Type: application/json

{
  "authCode": "AQD8...temporary_meta_oauth_code",
  "redirectUri": "https://app.lms.acme.com/settings/integrations/meta/callback"
}
```

---

### 4. Attribution & Revenue Reporting (`GET /api/v1/attribution/report`)
* **Purpose**: Query multi-touch attribution reports across campaigns and channels.
```http
GET /api/v1/attribution/report?startDate=2026-01-01&endDate=2026-06-30&model=u_shaped HTTP/1.1
Authorization: Bearer <USER_JWT>
```

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "model": "u_shaped",
  "channels": [
    {
      "source": "instagram",
      "medium": "paid_social",
      "leadsAcquired": 1240,
      "dealsClosed": 38,
      "attributedRevenue": 380000,
      "totalAdSpend": 45000,
      "roas": 8.44
    },
    {
      "source": "google",
      "medium": "cpc",
      "leadsAcquired": 920,
      "dealsClosed": 45,
      "attributedRevenue": 450000,
      "totalAdSpend": 52000,
      "roas": 8.65
    }
  ]
}
```

---

## 🔄 4. Six End-to-End Ingestion Data Flows

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        UNIVERSAL LEAD INGESTION DATA FLOWS                             │
├────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                        │
│ 1. INSTAGRAM PAID AD:                                                                  │
│    Instagram Story Ad ──► Clicks Bio/Swipe Link ──► Landing Page with UTMs ──►         │
│    Client SDK captures UTMs to Cookie ──► Webform Submit ──► LMS Attributor            │
│                                                                                        │
│ 2. FACEBOOK NATIVE LEAD FORM:                                                          │
│    User fills Meta Form ──► Meta Webhook ──► LMS API Gateway (200 OK) ──►              │
│    BullMQ Worker ──► GET /v19.0/{leadgen_id} ──► Normalizer ──► Deduplicator ──► MongoDB│
│                                                                                        │
│ 3. LINKEDIN SPONSORED INMAIL:                                                          │
│    Member submits Form ──► LinkedIn Lead Sync Webhook ──► Worker fetches URN ──►      │
│    Normalizer maps URN answers ──► Deduplicator stitches Work Email ──► MongoDB        │
│                                                                                        │
│ 4. YOUTUBE VIDEO ATTRIBUTION:                                                          │
│    Viewer clicks Description Link ──► `utm_source=youtube&utm_content=vid_xyz` ──►     │
│    Landing Page persists First-Touch ──► Registration Form ──► Lead Created            │
│                                                                                        │
│ 5. OFFLINE POSTER QR CODE:                                                             │
│    Attendee scans Poster QR ──► Shortlink Redirect adds UTMs ──► Lead Form ──►         │
│    `source: "trade_show"`, `medium: "qr_code"`, `campaign: "delhi_expo_2026"`          │
│                                                                                        │
│ 6. FIELD SALES REP MANUAL ENTRY:                                                       │
│    Sales rep logs in CRM ──► Selects governed dropdowns ──► `source: "sales_team"`,    │
│    `medium: "offline"` ──► Saves Lead ──► Assigned directly to rep's active pipeline   │
│                                                                                        │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## ⚖️ 5. System Design Trade-Off Matrix

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              SYSTEM DESIGN TRADE-OFF ANALYSIS                          │
├────────────────────────────┬─────────────────────────────┬─────────────────────────────┤
│ Dimension                  │ Architectural Choice        │ Key Trade-Off Rationale     │
├────────────────────────────┼─────────────────────────────┼─────────────────────────────┤
│ **Database Engine**        │ MongoDB (with Sharding)     │ Flexible polymorphic custom │
│                            │                             │ fields; fast document writes│
├────────────────────────────┼─────────────────────────────┼─────────────────────────────┤
│ **Ingestion Paradigm**     │ Asynchronous via BullMQ     │ Prevents third-party webhook│
│                            │                             │ drops during DB load spikes.│
├────────────────────────────┼─────────────────────────────┼─────────────────────────────┤
│ **Attribution Strategy**   │ Dual Snapshot + Event Stream│ Fast OLTP reads; flexible   │
│                            │                             │ multi-touch OLAP analytics. │
├────────────────────────────┼─────────────────────────────┼─────────────────────────────┤
│ **Taxonomy Governance**    │ DB-Driven Cached in Redis   │ Infinite extensibility with │
│                            │                             │ sub-millisecond validation. │
├────────────────────────────┼─────────────────────────────┼─────────────────────────────┤
│ **Multi-Tenant Model**     │ Logical Sharded Isolation   │ Low infrastructure cost with│
│                            │                             │ strict compound key security│
└────────────────────────────┴─────────────────────────────┴─────────────────────────────┘
```

---

## 🚫 6. Top 18 Common Architectural Pitfalls to Avoid

```
❌ 1. Storing `source` as an unvalidated free-text string.
❌ 2. Overwriting the original acquisition source when a lead re-engages.
❌ 3. Hardcoding platform-specific fields (e.g., `fb_leadgen_id`) in the core Lead document.
❌ 4. Performing synchronous Meta Graph API HTTP calls inside the Webhook Gateway.
❌ 5. Storing OAuth access tokens in plaintext in MongoDB.
❌ 6. Omitting `tenantId` in compound unique indexes, causing cross-tenant collisions.
❌ 7. Merging leads based on probabilistic fuzzy names automatically without human review.
❌ 8. Failing to normalize phone numbers to E.164, preventing automated SMS/call triggers.
❌ 9. Relying solely on client-side third-party cookies for website attribution.
❌ 10. Querying unindexed MongoDB collections for real-time analytics dashboards.
❌ 11. Ignoring webhook HMAC signature validation.
❌ 12. Not implementing an idempotency cache for duplicate webhooks.
❌ 13. Lack of a Dead-Letter Queue (DLQ) for poison pill payloads.
❌ 14. Dropping leads when a third-party social API experiences temporary downtime.
❌ 15. Forgetting to handle Single Page Application (SPA) route changes in the website tracker.
❌ 16. Storing campaign names as mutable strings without immutable campaign ObjectId references.
❌ 17. Permitting sales reps to bypass governed attribution dropdowns during manual entry.
❌ 18. Running analytics queries directly on the primary OLTP database node at scale.
```

---

## 🏛️ 7. Final Reference Architecture Diagram

```
                                 ┌────────────────────────────────────────────────────────┐
                                 │                   LEAD INGESTION CHANNELS              │
                                 ├────────────────┬───────────────────┬───────────────────┤
                                 │ Social Webhooks│ Digital & Web UTM │ Offline & Direct  │
                                 │ • Instagram    │ • Google Ads / CPC│ • Dynamic QR Code │
                                 │ • Facebook     │ • SEO Organic     │ • Inbound Telephony│
                                 │ • LinkedIn     │ • Website Webforms│ • Field Sales Rep │
                                 │ • X / Twitter  │ • YouTube Video   │ • Trade Shows     │
                                 └────────┬───────┴─────────┬─────────┴─────────┬─────────┘
                                          │                 │                   │
                                          ▼                 ▼                   ▼
                                 ┌────────────────────────────────────────────────────────┐
                                 │              INGESTION GATEWAY & SECURITY              │
                                 │ • TLS 1.3 Termination  • HMAC Signature Verification   │
                                 │ • Rate Limiting        • Fast 200 OK (<50ms)           │
                                 └──────────────────────────┬─────────────────────────────┘
                                                            │
                                                            ▼
                                 ┌────────────────────────────────────────────────────────┐
                                 │               DISTRIBUTED QUEUE BUFFER                 │
                                 │ • Redis Cluster (BullMQ) • Idempotency Guard (`SETNX`) │
                                 └──────────────────────────┬─────────────────────────────┘
                                                            │
                                                            ▼ Async Workers
                                 ┌────────────────────────────────────────────────────────┐
                                 │               LEAD PROCESSING PIPELINE                 │
                                 │                                                        │
                                 │  [ Platform Adapters ] ──► Unpack Graph API PII        │
                                 │            │                                           │
                                 │            ▼                                           │
                                 │  [ Normalizer Engine ] ──► E.164 Phone & Clean Email   │
                                 │            │                                           │
                                 │            ▼                                           │
                                 │  [ Deduplicator ]      ──► Deterministic Identity Match│
                                 │            │                                           │
                                 │            ▼                                           │
                                 │  [ Attribution Engine] ──► Governed UTMs & Touchpoints │
                                 └──────────────────────────┬─────────────────────────────┘
                                                            │
                                                            ▼
                                 ┌────────────────────────────────────────────────────────┐
                                 │                  DATA PERSISTENCE LAYER                │
                                 │ • MongoDB Sharded Cluster (`leads`, `leadTouchpoints`) │
                                 │ • Envelope Encryption (AWS KMS + AES-256-GCM)          │
                                 └──────────────────────────┬─────────────────────────────┘
                                                            │
                                   ┌────────────────────────┴────────────────────────┐
                                   │                                                 │
                                   ▼ Real-Time Event Bus                             ▼ Change Data Capture
                        ┌───────────────────────┐                         ┌───────────────────────┐
                        │   OPERATIONAL CRM     │                         │   ANALYTICS & OLAP    │
                        │ • Sales Lead Routing  │                         │ • Kafka Stream        │
                        │ • Slack / Email Alerts│                         │ • ClickHouse OLAP     │
                        │ • Opportunity Pipeline│                         │ • Multi-Touch Reports │
                        └───────────────────────┘                         └───────────────────────┘
```

---

Previous : [18_Scaling_and_Reliability.md](./18_Scaling_and_Reliability.md) | Index: [00_Index.md](../00_Index.md) | Next: —
