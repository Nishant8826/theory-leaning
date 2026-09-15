# 05 — Facebook Lead Integration

## 📌 1. Overview & Meta Ecosystem Architecture

Facebook and Instagram both operate under the **Meta Developer Ecosystem**. While their user interfaces and brand demographics differ, their underlying programmatic infrastructure (Meta Graph API, Webhooks, Ad Managers, and OAuth authentication) is unified.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              SHARED META INTEGRATION LAYER                             │
├────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                        │
│     [ Facebook Feed Ad ]                           [ Instagram Story Ad ]              │
│     (Native Lead Form)                             (Native Lead Form)                  │
│              │                                              │                          │
│              └──────────────────────┬───────────────────────┘                          │
│                                     │                                                  │
│                                     ▼                                                  │
│                       [ Meta Graph Webhook Server ]                                    │
│                       (Event topic: "page/leadgen")                                    │
│                                     │                                                  │
│                                     ▼                                                  │
│                       [ LMS Meta Ingestion Gateway ]                                   │
│                       • Validates HMAC (App Secret)                                    │
│                       • Enqueues Job with { page_id, leadgen_id }                      │
│                                     │                                                  │
│                                     ▼                                                  │
│                       [ Meta Graph API Client Pool ]                                   │
│                       • Resolves Page Access Token for Tenant                          │
│                       • Executes GET /v19.0/{leadgen_id}                               │
│                                     │                                                  │
│                    ┌────────────────┴────────────────┐                                 │
│                    │                                 │                                 │
│                    ▼                                 ▼                                 │
│           [ Facebook Adapter ]             [ Instagram Adapter ]                       │
│           (source: "facebook")             (source: "instagram")                       │
│                    │                                 │                                 │
│                    └────────────────┬────────────────┘                                 │
│                                     │                                                  │
│                                     ▼                                                  │
│                    [ Universal LMS Normalizer & Attributor ]                           │
│                                                                                        │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔐 2. Meta OAuth 2.0 & Token Exchange Architecture

A standard failure mode in SaaS integrations is using short-lived user tokens that expire within 60 minutes. An enterprise LMS requires **never-expiring Page Access Tokens** generated through Meta's OAuth 2.0 token exchange flow:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        META OAUTH 2.0 LONG-LIVED TOKEN FLOW                            │
├────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                        │
│  1. Tenant Admin clicks "Connect Facebook" in LMS UI                                   │
│     └── Redirects to Meta OAuth Dialog with Scopes:                                    │
│         • `leads_retrieval`                                                            │
│         • `pages_manage_ads`                                                           │
│         • `pages_read_engagement`                                                      │
│         • `pages_show_list`                                                            │
│                                                                                        │
│  2. Meta returns Short-Lived User Access Token (Expiry: ~1-2 hours)                    │
│                                                                                        │
│  3. LMS Backend exchanges for Long-Lived User Access Token (Expiry: ~60 days)          │
│     └── GET /oauth/access_token?                                                       │
│         grant_type=fb_exchange_token&                                                  │
│         client_id={app_id}&                                                            │
│         client_secret={app_secret}&                                                    │
│         fb_exchange_token={short_lived_token}                                          │
│                                                                                        │
│  4. LMS queries User's Pages using Long-Lived Token                                    │
│     └── GET /me/accounts?access_token={long_lived_user_token}                          │
│                                                                                        │
│  5. Meta returns Page Objects with Permanent Page Access Tokens (No Expiry)            │
│                                                                                        │
│  6. LMS Backend subscribes Webhook to Page events                                      │
│     └── POST /{page_id}/subscribed_apps?                                              │
│         subscribed_fields=leadgen&                                                     │
│         access_token={page_access_token}                                               │
│                                                                                        │
│  7. Encrypt and store Page Access Token in MongoDB using AWS KMS                       │
│                                                                                        │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🏢 3. Multi-Tenant Page & Ad Account Mapping

In a multi-tenant B2B SaaS system, one corporate organization (Tenant) may manage multiple Facebook Pages, Ad Accounts, and Instagram Business Profiles.

### MongoDB `socialIntegrations` Document
```json
{
  "_id": "sec_int_fb_83921048",
  "tenantId": "tenant_acme_corp",
  "platform": "facebook",
  "status": "active",
  "metaAppId": "948201948201948",
  "pageAccounts": [
    {
      "pageId": "847291048201",
      "pageName": "Acme North America",
      "encryptedPageAccessToken": "enc_v1:98a7sd9f87as9d8f7as9d8f7...",
      "instagramActorId": "178414002938491",
      "isLeadgenSubscribed": true,
      "defaultCampaignId": "camp_us_general",
      "connectedAt": "2026-01-10T10:00:00Z"
    }
  ],
  "tokenHealth": {
    "isValid": true,
    "lastVerifiedAt": "2026-06-15T08:00:00Z"
  }
}
```

---

## ⚡ 4. Facebook Ingestion Pipeline Execution

```typescript
export class FacebookAdapter implements ISocialAdapter {
  readonly platform = "facebook";

  public verifyWebhookSignature(payload: any, signatureHeader: string, appSecret: string): boolean {
    const crypto = require("crypto");
    const hmac = crypto.createHmac("sha256", appSecret);
    const expected = `sha256=${hmac.update(JSON.stringify(payload)).digest("hex")}`;
    return crypto.timingSafeEqual(Buffer.from(signatureHeader), Buffer.from(expected));
  }

  public async fetchLeadDetails(leadgenId: string, pageAccessToken: string): Promise<any> {
    const response = await fetch(
      `https://graph.facebook.com/v19.0/${leadgenId}?fields=id,created_time,ad_id,ad_name,adset_name,campaign_name,form_id,field_data&access_token=${pageAccessToken}`
    );
    if (!response.ok) {
      const err = await response.json();
      throw new Error(`Meta Graph API Failure: ${JSON.stringify(err)}`);
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
      source: "facebook",
      medium: "paid_social",
      campaignName: rawLeadData.campaign_name || "facebook_lead_ad",
      externalLeadId: rawLeadData.id,
      externalFormId: rawLeadData.form_id,
      externalAdId: rawLeadData.ad_id,
      fullName: fieldMap.get("full_name") || `${fieldMap.get("first_name") || ""} ${fieldMap.get("last_name") || ""}`.trim(),
      email: fieldMap.get("email"),
      phoneNumber: fieldMap.get("phone_number"),
      customFields: {
        city: fieldMap.get("city"),
        jobTitle: fieldMap.get("job_title"),
        adName: rawLeadData.ad_name,
        adSetName: rawLeadData.adset_name
      },
      submittedAt: new Date(rawLeadData.created_time),
      rawPayload: rawLeadData
    };
  }
}
```

---

Previous : [04_Instagram_Lead_Integration.md](./04_Instagram_Lead_Integration.md) | Index: [00_Index.md](../00_Index.md) | Next: [06_LinkedIn_Lead_Integration.md](./06_LinkedIn_Lead_Integration.md)
