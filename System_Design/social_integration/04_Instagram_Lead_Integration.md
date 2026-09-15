# 04 — Instagram Lead Integration

## 📌 1. Overview & Capture Mechanisms

Instagram is a primary top-of-funnel customer acquisition channel. In an enterprise Lead Management System, Instagram leads are captured through four distinct mechanisms:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                             INSTAGRAM LEAD CAPTURE MODES                               │
├─────────────────┬─────────────────┬────────────────────┬───────────────────────────────┤
│ 1. Instant Lead │ 2. Click-to-DM  │ 3. Bio / Story     │ 4. Direct Messenger           │
│    Generation   │    Ads (CTD)    │    Link In Bio     │    Automation (Chatbot)       │
├─────────────────┼─────────────────┼────────────────────┼───────────────────────────────┤
│ Native in-app   │ User clicks ad  │ User clicks link   │ User sends DM or replies to a │
│ Instant Form    │ and initiates a │ in bio / story ->  │ story with a trigger keyword  │
│ pre-filled from │ direct chat on  │ visits landing     │ -> chatbot collects contact   │
│ profile data.   │ Instagram DM.   │ page with UTMs.    │ details in-chat.              │
└─────────────────┴─────────────────┴────────────────────┴───────────────────────────────┘
```

> [!NOTE]
> **API Verification Notice**: Instagram's developer ecosystem operates under the **Meta Graph API** (Instagram Graph API & Messenger Platform). Platform permissions, webhook topics (`leadgen`, `messages`), and API rate limits evolve frequently. Always verify against Meta's latest official developer documentation prior to production rollout.

---

## 🏗️ 2. Native Instant Form (Lead Gen) Architecture

When a user submits a native Instagram Lead Ad form, Instagram does not transmit the user's PII (Name, Email, Phone) directly in the webhook payload for security and privacy reasons. Instead, Meta transmits a lightweight **Notification Event** containing an `external_lead_id` (or `leadgen_id`).

```
┌──────────────┐          ┌────────────────┐          ┌────────────────┐          ┌──────────────┐
│  Instagram   │          │  LMS Webhook   │          │ Ingestion      │          │  Meta Graph  │
│  Lead Ad     │          │  Gateway       │          │ Worker         │          │  API         │
└──────┬───────┘          └───────┬────────┘          └───────┬────────┘          └──────┬───────┘
       │                          │                           │                          │
       │ 1. Form Submitted        │                           │                          │
       ├─────────────────────────►│                           │                          │
       │                          │ 2. Verify HMAC SHA-256    │                          │
       │                          │ 3. Enqueue Job (BullMQ)   │                          │
       │ 4. 200 OK (<50ms)        │                           │                          │
       │◄─────────────────────────┤                           │                          │
       │                          │                           │ 5. Pull Next Event       │
       │                          │                           ├─────────────────────────►│
       │                          │                           │                          │
       │                          │                           │ 6. GET /v19.0/{lead_id}  │
       │                          │                           │    (Page Access Token)   │
       │                          │                           ├─────────────────────────►│
       │                          │                           │                          │
       │                          │                           │ 7. Return Full PII & Ad  │
       │                          │                           │◄─────────────────────────┤
       │                          │                           │                          │
       │                          │                           │ 8. Normalize & Attrib    │
       │                          │                           │ 9. Save to MongoDB       │
       │                          │                           │                          │
```

---

## 📦 3. Data Capture: Platform Data vs. Internal Attribution

To maintain architectural purity, we strictly segregate **Platform-Supplied Data** (external metadata) from **Internal LMS Attribution Data** (canonical domain values).

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                           DATA SEGREGATION ARCHITECTURE                                │
├────────────────────────────────────────┬───────────────────────────────────────────────┤
│ External Meta / Instagram Payload      │ Internal LMS Canonical Domain Object          │
├────────────────────────────────────────┼───────────────────────────────────────────────┤
│ • `leadgen_id`: "109823487123984"      │ • `tenantId`: "tenant_acme_corp"              │
│ • `page_id`: "847291048201"            │ • `leadId`: "lead_65f3a9b1c8e"                │
│ • `form_id`: "48291048123"             │ • `source`: "instagram"                       │
│ • `ad_id`: "23849102839401"            │ • `medium`: "paid_social"                     │
│ • `adset_id`: "23849102839111"         │ • `campaign`: "summer_sale_2026"              │
│ • `campaign_id`: "120384910283"        │ • `channel`: "Paid Social"                    │
│ • `created_time`: 1718449200           │ • `name`: "Alex Rivera"                       │
│ • `field_data`: [                      │ • `email`: "alex.rivera@example.com"          │
│     { "name": "full_name", ... },      │ • `phone`: "+14155552671" (E.164)             │
│     { "name": "email", ... },          │ • `externalIdentities`: [                     │
│     { "name": "phone_number", ... }    │     { "platform": "instagram",                │
│   ]                                    │       "externalLeadId": "109823487123984",    │
│                                        │       "adId": "23849102839401" }              │
│                                        │   ]                                           │
└────────────────────────────────────────┴───────────────────────────────────────────────┘
```

---

## 💻 4. Instagram Webhook Payload Structure

### 1. Inbound Webhook Notification from Meta
```json
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
            "ad_id": "23849102839401",
            "form_id": "48291048123",
            "leadgen_id": "109823487123984",
            "created_time": 1718449200,
            "page_id": "847291048201",
            "adgroup_id": "23849102839111"
          }
        }
      ]
    }
  ]
}
```

### 2. Meta Graph API Lead Retrieval (`GET /v19.0/{leadgen_id}`)
```json
{
  "created_time": "2026-06-15T11:00:00+0000",
  "id": "109823487123984",
  "ad_id": "23849102839401",
  "ad_name": "Instagram Story Video 01",
  "adset_name": "Tech Enthusiasts 25-40",
  "campaign_name": "Summer Sale 2026",
  "form_id": "48291048123",
  "field_data": [
    {
      "name": "full_name",
      "values": ["Alex Rivera"]
    },
    {
      "name": "email",
      "values": ["alex.rivera@example.com"]
    },
    {
      "name": "phone_number",
      "values": ["+14155552671"]
    },
    {
      "name": "company_size",
      "values": ["50-100"]
    }
  ]
}
```

---

## 🛠️ 5. Instagram Lead Adapter Implementation

```typescript
export class InstagramAdapter implements ISocialAdapter {
  readonly platform = "instagram";

  public verifyWebhookSignature(payload: any, signatureHeader: string, appSecret: string): boolean {
    const crypto = require("crypto");
    const hmac = crypto.createHmac("sha256", appSecret);
    const expectedSignature = `sha256=${hmac.update(JSON.stringify(payload)).digest("hex")}`;
    return crypto.timingSafeEqual(Buffer.from(signatureHeader), Buffer.from(expectedSignature));
  }

  public async fetchLeadDetails(leadgenId: string, pageAccessToken: string): Promise<any> {
    const url = `https://graph.facebook.com/v19.0/${leadgenId}?access_token=${pageAccessToken}`;
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Meta Graph API Error: ${response.statusText}`);
    }
    return response.json();
  }

  public async normalizePayload(rawLeadData: any, context: { tenantId: string }): Promise<CanonicalLeadPayload> {
    const fieldMap = new Map<string, string>();
    rawLeadData.field_data?.forEach((field: { name: string; values: string[] }) => {
      fieldMap.set(field.name.toLowerCase(), field.values[0]);
    });

    return {
      tenantId: context.tenantId,
      source: "instagram",
      medium: "paid_social",
      campaignName: rawLeadData.campaign_name || "instagram_lead_ad",
      externalLeadId: rawLeadData.id,
      externalFormId: rawLeadData.form_id,
      externalAdId: rawLeadData.ad_id,
      fullName: fieldMap.get("full_name") || fieldMap.get("name"),
      email: fieldMap.get("email"),
      phoneNumber: fieldMap.get("phone_number") || fieldMap.get("phone"),
      customFields: {
        companySize: fieldMap.get("company_size"),
        adSetName: rawLeadData.adset_name,
        adName: rawLeadData.ad_name
      },
      submittedAt: new Date(rawLeadData.created_time),
      rawPayload: rawLeadData
    };
  }
}
```

---

Previous : [03_Social_Media_Lead_Architecture.md](./03_Social_Media_Lead_Architecture.md) | Index: [00_Index.md](../00_Index.md) | Next: [05_Facebook_Lead_Integration.md](./05_Facebook_Lead_Integration.md)
