# 03 — Social Media Lead Architecture

## 📌 1. Architectural Mission Statement

The objective of this architecture is to build a **universal, plug-and-play integration framework** where any social network (Instagram, Facebook, LinkedIn, X, YouTube, TikTok) or inbound channel can be connected seamlessly. Adding a new channel must require **zero modifications** to the core Lead Management System (LMS) domain model, database schema, or business workflows.

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                            END-TO-END LEAD INGESTION ARCHITECTURE                                │
├──────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                  │
│   [ Instagram ]      [ Facebook ]      [ LinkedIn ]       [ X / Twitter ]      [ YouTube / Web ] │
│   Lead Gen Ads      Page Webhooks     Lead Sync API        Ad Tracking           UTM Webforms    │
│        │                 │                 │                    │                     │          │
│        └────────┬────────┴────────┬────────┴────────────┬───────┴─────────────┬───────┘          │
│                 │                 │                     │                     │                  │
│                 ▼                 ▼                     ▼                     ▼                  │
│   ┌──────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                 INTEGRATION LAYER (ADAPTERS)                             │   │
│   │   • Signature Verification (HMAC)          • OAuth Token Management & Refresh            │   │
│   │   • Payload Unpacking                      • Rate-Limit & Backoff Handling               │   │
│   └─────────────────────────────────────────────┬────────────────────────────────────────────┘   │
│                                                 │                                                │
│                                                 ▼ Standardized Raw Envelope                      │
│   ┌──────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                INGESTION GATEWAY & BUFFER                                │   │
│   │   • Fast 200 OK Response (<50ms)           • Immediate Enqueue to Redis / BullMQ / SQS   │   │
│   └─────────────────────────────────────────────┬────────────────────────────────────────────┘   │
│                                                 │                                                │
│                                                 ▼ Async Processing                               │
│   ┌──────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                LEAD PROCESSING PIPELINE (WORKER)                         │   │
│   │                                                                                          │   │
│   │   [ 1. Validation ] ──► [ 2. Normalization ] ──► [ 3. Deduplication ] ──► [ 4. Attribution] │   │
│   │   • Schema check        • Phone (E.164)          • Email/Phone Match      • Touchpoint log   │   │
│   │   • Security sanitize   • Slugify UTMs           • Conflict Resolution    • First/Last Touch │   │
│   └─────────────────────────────────────────────┬────────────────────────────────────────────┘   │
│                                                 │                                                │
│                                                 ▼ Clean Domain Objects                           │
│   ┌──────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                               PERSISTENCE & EVENT BROADCAST                              │   │
│   │   • MongoDB (Leads & Touchpoints)          • Event Bus (Kafka / Redis Streams)           │   │
│   │   • Sales Routing & Assignment             • Real-Time Webhooks & Notifications          │   │
│   └──────────────────────────────────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🧩 2. Core Architectural Design Patterns

To insulate core CRM logic from external platform quirks, we employ three classic enterprise design patterns:

### 1. The Adapter Pattern (`ISocialAdapter`)
Translates platform-specific, vendor-locked payloads into our internal `CanonicalLeadPayload`.

```typescript
// Core Canonical Interface
export interface CanonicalLeadPayload {
  tenantId: string;
  source: string;              // e.g. "instagram", "linkedin"
  medium: string;              // e.g. "paid_social"
  campaignName?: string;
  externalLeadId: string;      // Platform's unique lead identifier
  externalFormId?: string;
  externalAdId?: string;
  fullName?: string;
  firstName?: string;
  lastName?: string;
  email?: string;
  phoneNumber?: string;
  customFields: Record<string, any>;
  submittedAt: Date;
  rawPayload: Record<string, any>;
}

// Universal Adapter Contract
export interface ISocialAdapter {
  readonly platform: string;
  verifyWebhookSignature(payload: any, signature: string, secret: string): boolean;
  normalizePayload(rawEvent: any, connectionConfig: any): Promise<CanonicalLeadPayload>;
  fetchLeadDetails(externalLeadId: string, accessToken: string): Promise<any>;
}
```

### 2. The Strategy & Factory Pattern
Dynamically selects the appropriate adapter at runtime based on the incoming route parameter (`/api/v1/webhooks/:platform`).

```
                    ┌────────────────────────────┐
                    │    SocialAdapterFactory    │
                    └─────────────┬──────────────┘
                                  │
         ┌────────────────────────┼────────────────────────┐
         │                        │                        │
         ▼                        ▼                        ▼
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│  InstagramAdapter│    │ FacebookAdapter  │    │ LinkedInAdapter  │
└──────────────────┘    └──────────────────┘    └──────────────────┘
```

```typescript
export class SocialAdapterFactory {
  private static adapters: Map<string, ISocialAdapter> = new Map();

  public static register(platform: string, adapter: ISocialAdapter) {
    this.adapters.set(platform.toLowerCase(), adapter);
  }

  public static getAdapter(platform: string): ISocialAdapter {
    const adapter = this.adapters.get(platform.toLowerCase());
    if (!adapter) {
      throw new Error(`Unsupported social integration platform: ${platform}`);
    }
    return adapter;
  }
}
```

---

## ⚙️ 3. Component-by-Component Deep Dive

### 1. Integration Layer (Webhooks & Polling Workers)
* **Responsibility**: Authenticate incoming HTTP webhooks, decrypt tenant credentials, verify HMAC signatures, and unpack provider wrappers.
* **Resilience**: Acknowledges webhooks with HTTP `200 OK` within 50ms to prevent social platforms (Meta, LinkedIn) from flagging the endpoint as degraded and disabling webhook delivery.

### 2. Ingestion Queue (Redis / BullMQ / AWS SQS)
* **Responsibility**: Buffers sudden viral spikes (e.g., a Black Friday ad generating 5,000 leads in 2 minutes) without overwhelming downstream MongoDB clusters.
* **Idempotency Guard**: Rejects duplicate event IDs immediately at the queue boundary using Redis `SETNX`.

### 3. Lead Normalization Service
* **Responsibility**: Cleanses messy data into pristine canonical formats:
  * Phone numbers converted to strict international **E.164** format (e.g., `+14155552671`).
  * Names split into `firstName` and `lastName`.
  * Email addresses trimmed, stripped of invalid spaces, and lowercased.
  * Platform custom form questions mapped to standard CRM fields.

### 4. Deduplication Engine
* **Responsibility**: Inspects existing customer records using deterministic identity matching (Tenant ID + Normalized Email / Phone).
* **Action**: If an existing lead is identified, appends a new `LeadTouchpoint` rather than creating a duplicate contact record.

### 5. Attribution Engine
* **Responsibility**: Resolves `Source`, `Medium`, and `Campaign` against the governed dictionary, attaches UTM parameters and Click IDs, and calculates `firstTouch` and `lastTouch` metadata.

---

## 🏛️ 4. Microservice vs. Modular Monolith Architecture

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              TOPOLOGY TRADE-OFF ANALYSIS                               │
├────────────────────────────┬─────────────────────────────┬─────────────────────────────┤
│ Evaluation Criteria        │ Modular Monolith            │ Dedicated Ingestion Service │
├────────────────────────────┼─────────────────────────────┼─────────────────────────────┤
│ Deployment Complexity      │ Low (Single CI/CD Pipeline) │ Medium (Multi-service orch) │
│ Scaling Webhook Spikes     │ Monolith must scale out     │ Independent worker scaling  │
│ Blast Radius of API Bugs   │ Could impact sales CRM UI   │ Isolated to ingestion pipe  │
│ Team Velocity (< 15 Devs)  │ Extremely High              │ Higher network/ops friction │
│ Recommended Stage          │ Startups & Mid-Scale (MVP)  │ High-Volume Scale (1M+/day) │
└────────────────────────────┴─────────────────────────────┴─────────────────────────────┘
```

### 💡 Staff Architect Recommendation
Start with a **Modular Monolith** using strict boundary isolation (clean TypeScript modules inside `src/modules/integrations/` and `src/modules/leads/`). Communicate internally via an asynchronous event bus (BullMQ / Redis). When ingestion throughput exceeds 500 requests/second, extract the `integrations/` directory into a standalone serverless or containerized microservice without modifying domain business logic.

---

Previous : [02_Source_Medium_Campaign_Model.md](./02_Source_Medium_Campaign_Model.md) | Index: [00_Index.md](../00_Index.md) | Next: [04_Instagram_Lead_Integration.md](./04_Instagram_Lead_Integration.md)
