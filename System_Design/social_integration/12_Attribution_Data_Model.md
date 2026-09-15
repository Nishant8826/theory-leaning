# 12 — Attribution Data Model (MongoDB)

## 📌 1. Database Architecture & Schema Design Philosophy

Our MongoDB schema design is optimized for **high-throughput asynchronous ingestion** (write-heavy) and **sub-50ms CRM dashboard queries** (read-heavy).

We apply a **Hybrid Normalized-Denormalized Model**:
* **Denormalized Snapshots** (`firstTouch` & `lastTouch`) are embedded directly inside the parent `leads` collection for instant OLTP list queries (`GET /api/v1/leads`).
* **Normalized Event Stream** (`leadTouchpoints`) is stored in an append-only time-series collection to power granular multi-touch attribution analytics and timeline views without bloating the main `leads` document.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              MONGODB COLLECTION TOPOLOGY                               │
├────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                        │
│   ┌───────────────────────────┐                     ┌──────────────────────────────┐   │
│   │        leadSources        │                     │        leadCampaigns         │   │
│   │ (Governed Source Catalog) │                     │  (Budgets, UTMs & Targets)   │   │
│   └─────────────┬─────────────┘                     └──────────────┬───────────────┘   │
│                 │                                                  │                   │
│                 └─────────────────────────┬────────────────────────┘                   │
│                                           │                                            │
│                                           ▼                                            │
│                     ┌───────────────────────────────────────────┐                      │
│                     │                   leads                   │                      │
│                     │  (Canonical Profile + Fast Snapshots)     │                      │
│                     │  • _id, tenantId, email, phone, status    │                      │
│                     │  • firstTouch (Snapshot Object)           │                      │
│                     │  • lastTouch (Snapshot Object)            │                      │
│                     │  • externalIdentities []                  │                      │
│                     └─────────────────────┬─────────────────────┘                      │
│                                           │ 1:N                                        │
│                                           ▼                                            │
│                     ┌───────────────────────────────────────────┐                      │
│                     │              leadTouchpoints              │                      │
│                     │   (Immutable Time-Series Event Log)       │                      │
│                     │   • _id, tenantId, leadId, timestamp      │                      │
│                     │   • source, medium, campaign, UTMs, CAPI  │                      │
│                     └───────────────────────────────────────────┘                      │
│                                                                                        │
│   ┌───────────────────────────┐                     ┌──────────────────────────────┐   │
│   │    socialIntegrations     │                     │     externalLeadMappings     │   │
│   │(OAuth Tokens & Page Confs)│                     │(O(1) Webhook Deduplication)  │   │
│   └───────────────────────────┘                     └──────────────────────────────┘   │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🗄️ 2. Detailed Collection Schemas

### 1. `leads` Collection (The Canonical Entity)
```json
{
  "_id": { "$oid": "65f3a9b1c8e123456789abcd" },
  "tenantId": "tenant_acme_corp",
  "fullName": "Alex Rivera",
  "firstName": "Alex",
  "lastName": "Rivera",
  "email": "alex.rivera@enterprise.com",
  "phone": "+14155552671",
  "status": "new",
  "lifecycleStage": "marketing_qualified",
  "leadScore": 75,
  "assignedOwnerId": { "$oid": "65f3a9b1c8e1234567890001" },
  
  "firstTouch": {
    "source": "instagram",
    "medium": "paid_social",
    "campaignId": { "$oid": "65f3a9b1c8e1234567890010" },
    "campaignName": "summer_sale_2026",
    "content": "story_video_v1",
    "term": "crm_tools",
    "clickId": "fbclid_IwAR28301982039",
    "landingPage": "https://acme.com/features",
    "referrer": "https://l.instagram.com/",
    "timestamp": { "$date": "2026-06-01T10:15:30Z" }
  },

  "lastTouch": {
    "source": "google",
    "medium": "cpc",
    "campaignId": { "$oid": "65f3a9b1c8e1234567890020" },
    "campaignName": "brand_search_us",
    "content": "text_ad_top",
    "clickId": "gclid_EAIaIQobChMI892",
    "landingPage": "https://acme.com/demo",
    "referrer": "https://www.google.com/",
    "timestamp": { "$date": "2026-06-15T14:22:10Z" }
  },

  "touchpointsCount": 4,

  "externalIdentities": [
    {
      "platform": "instagram",
      "externalLeadId": "109823487123984",
      "externalUserId": "ig_user_849201",
      "pageId": "847291048201",
      "connectedAt": { "$date": "2026-06-01T10:15:30Z" }
    },
    {
      "platform": "linkedin",
      "externalLeadId": "urn:li:leadGenFormResponse:109283746",
      "connectedAt": { "$date": "2026-06-10T11:00:00Z" }
    }
  ],

  "consent": {
    "isOptedIn": true,
    "consentType": "gdpr_explicit",
    "privacyPolicyVersion": "2026.1",
    "optedInAt": { "$date": "2026-06-01T10:15:30Z" },
    "ipAddress": "198.51.100.42"
  },

  "customFields": {
    "companySize": "50-200",
    "estimatedBudget": 50000,
    "industry": "Fintech"
  },

  "createdAt": { "$date": "2026-06-01T10:15:30Z" },
  "updatedAt": { "$date": "2026-06-15T14:22:10Z" }
}
```

---

### 2. `leadTouchpoints` Collection (Immutable Event Stream)
```json
{
  "_id": { "$oid": "65f3b110c8e1234567890001" },
  "tenantId": "tenant_acme_corp",
  "leadId": { "$oid": "65f3a9b1c8e123456789abcd" },
  "anonymousId": "anon_98f4a1c2-3e81-4b72-a982-129849102834",
  "eventType": "form_submission",
  "source": "instagram",
  "medium": "paid_social",
  "campaignName": "summer_sale_2026",
  "campaignId": { "$oid": "65f3a9b1c8e1234567890010" },
  "content": "story_video_v1",
  "term": "crm_tools",
  "clickId": "fbclid_IwAR28301982039",
  "landingPage": "https://acme.com/features",
  "referrer": "https://l.instagram.com/",
  "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X)...",
  "ipAddress": "198.51.100.42",
  "submittedAt": { "$date": "2026-06-01T10:15:30Z" },
  "rawPayload": {
    "leadgen_id": "109823487123984",
    "form_id": "48291048123"
  }
}
```

---

### 3. `externalLeadMappings` Collection (O(1) Deduplication)
```json
{
  "_id": { "$oid": "65f3c001c8e1234567890001" },
  "tenantId": "tenant_acme_corp",
  "platform": "facebook",
  "externalLeadId": "109823487123984",
  "internalLeadId": { "$oid": "65f3a9b1c8e123456789abcd" },
  "createdAt": { "$date": "2026-06-01T10:15:30Z" }
}
```

---

## ⚡ 3. Indexing Strategy & Sharding Architecture

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              COMPOUND INDEX SPECIFICATION                              │
├─────────────────────┬──────────────────────────────────────────┬───────────────────────┤
│ Collection          │ Key Index Fields                         │ Query Optimization    │
├─────────────────────┼──────────────────────────────────────────┼───────────────────────┤
│ `leads`             │ `{ tenantId: 1, email: 1 }` (Sparse)     │ Exact Deduplication   │
│ `leads`             │ `{ tenantId: 1, phone: 1 }` (Sparse)     │ Exact Deduplication   │
│ `leads`             │ `{ tenantId: 1, status: 1, createdAt: -1}`│ CRM Inbox Lists       │
│ `leads`             │ `{ tenantId: 1, "firstTouch.source": 1 }`│ Attribution Rollups   │
│ `leadTouchpoints`   │ `{ tenantId: 1, leadId: 1, timestamp: 1}`│ Lead Timeline View    │
│ `leadTouchpoints`   │ `{ tenantId: 1, source: 1, timestamp: 1}`│ Analytics Aggregations│
│ `externalLeadMappings`│ `{ tenantId: 1, platform: 1, externalLeadId: 1 }` (UNIQUE) │ Webhook Idempotency │
└─────────────────────┴──────────────────────────────────────────┴───────────────────────┘
```

### MongoDB Sharding Key Recommendation
In an enterprise multi-tenant system scaling to 100M+ leads, shard collections using a **Hashed Compound Shard Key**:
* Shard Key: `{ tenantId: 1, _id: "hashed" }`
* **Why**: Guarantees that all queries for a specific tenant route directly to the target shard without expensive scatter-gather operations across the cluster.

---

Previous : [11_Lead_Normalization_and_Deduplication.md](./11_Lead_Normalization_and_Deduplication.md) | Index: [00_Index.md](../00_Index.md) | Next: [13_Lead_Ingestion_Architecture.md](./13_Lead_Ingestion_Architecture.md)
