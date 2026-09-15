# 06 — LinkedIn Lead Integration

## 📌 1. Overview & B2B Lead Gen Dynamics

LinkedIn is the premier B2B lead acquisition network. Unlike consumer social networks, LinkedIn users provide high-fidelity professional data: verified corporate email addresses, company names, job titles, industry verticals, and seniority levels.

Capturing LinkedIn leads primarily occurs via **LinkedIn Lead Gen Forms** (sponsored in-feed cards and Message Ads).

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              LINKEDIN LEAD INGESTION PIPELINE                          │
├────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                        │
│   [ LinkedIn Member ]                                                                  │
│   Clicks "Download Enterprise Whitepaper"                                              │
│   (Form pre-filled with Work Email, Job Title, Company Size)                           │
│           │                                                                            │
│           ▼                                                                            │
│   [ LinkedIn Marketing Developer Platform ]                                            │
│   Generates `leadGenFormResponse` (URN: `urn:li:leadGenFormResponse:12345678`)         │
│           │                                                                            │
│           ▼                                                                            │
│   [ Lead Sync Webhook / Push Notification ]                                            │
│   Sends notification to LMS Ingestion Gateway                                          │
│           │                                                                            │
│           ▼                                                                            │
│   [ LMS LinkedIn Worker ]                                                              │
│   • Retrieves encrypted OAuth 2.0 Access Token for Organization                        │
│   • Calls LinkedIn Lead Sync API (`GET /v2/leadForms/...`)                             │
│   • Unpacks deeply nested JSON array responses                                         │
│           │                                                                            │
│           ▼                                                                            │
│   [ Canonical Normalizer ]                                                             │
│   Maps LinkedIn URNs to standard Lead and Attribution domain records                  │
│                                                                                        │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

> [!NOTE]
> **API Verification Notice**: LinkedIn's Developer Platform requires approved access to the **Lead Sync API** and **Community Management API**. OAuth access tokens last 60 days and require programmatic refresh token rotation. Always check the latest LinkedIn Developer Portal guidelines.

---

## 🔐 2. LinkedIn OAuth 2.0 & Scopes

Integrating a tenant's LinkedIn Campaign Manager requires specific OAuth 2.0 scopes:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          REQUIRED LINKEDIN OAUTH SCOPES                     │
├───────────────────────┬─────────────────────────────────────────────────────┤
│ Scope Name            │ Architectural Purpose                               │
├───────────────────────┼─────────────────────────────────────────────────────┤
│ `r_ads_leadgen`       │ Retrieve lead form responses and submitted PII.     │
│ `r_ads`               │ Read ad accounts, campaign names, and ad creatives. │
│ `r_organization_admin`│ Verify organization ownership and page roles.       │
│ `r_basicprofile`      │ Verify administrator credentials.                   │
└───────────────────────┴─────────────────────────────────────────────────────┘
```

### Token Lifecycle & Refresh Management
Unlike Meta's permanent page tokens, LinkedIn OAuth 2.0 issues:
* **Access Token**: Expires in **60 days**.
* **Refresh Token**: Expires in **365 days** (must be used to generate a new Access Token before expiry).

```typescript
// Background Token Health Monitor (Runs daily cron)
export async function refreshLinkedInTokens(integration: ILinkedInIntegration) {
  const isExpiringSoon = (integration.expiresAt.getTime() - Date.now()) < (7 * 24 * 60 * 60 * 1000); // 7 days
  if (isExpiringSoon) {
    const params = new URLSearchParams({
      grant_type: "refresh_token",
      refresh_token: decrypt(integration.encryptedRefreshToken),
      client_id: process.env.LINKEDIN_CLIENT_ID!,
      client_secret: process.env.LINKEDIN_CLIENT_SECRET!
    });
    const res = await fetch("https://www.linkedin.com/oauth/v2/accessToken", {
      method: "POST",
      body: params
    });
    const data = await res.json();
    await updateTenantToken(integration.tenantId, data.access_token, data.expires_in);
  }
}
```

---

## 📦 3. LinkedIn Data Model Differences & Canonical Mapping

LinkedIn formats lead form submissions as an array of question-answer pairs keyed by **LinkedIn URNs** (Uniform Resource Names).

### Raw LinkedIn Form Response Payload
```json
{
  "id": "urn:li:leadGenFormResponse:109283746",
  "leadType": "SPONSORED",
  "formUrn": "urn:li:leadGenForm:839201",
  "creativeUrn": "urn:li:sponsoredCreative:94820194",
  "campaignUrn": "urn:li:sponsoredCampaign:77482910",
  "submittedAt": 1718449200000,
  "formResponse": {
    "answers": [
      {
        "elementId": 1,
        "questionText": "First Name",
        "values": ["Samantha"]
      },
      {
        "elementId": 2,
        "questionText": "Last Name",
        "values": ["Chen"]
      },
      {
        "elementId": 3,
        "questionText": "Work Email",
        "values": ["samantha.chen@enterprisecloud.com"]
      },
      {
        "elementId": 4,
        "questionText": "Job Title",
        "values": ["VP of Engineering"]
      },
      {
        "elementId": 5,
        "questionText": "Company Name",
        "values": ["Enterprise Cloud Systems"]
      }
    ]
  }
}
```

### Transformation to Universal Canonical Schema
```typescript
export class LinkedInAdapter implements ISocialAdapter {
  readonly platform = "linkedin";

  public verifyWebhookSignature(payload: any, signature: string, secret: string): boolean {
    // LinkedIn HMAC-SHA256 signature verification
    const crypto = require("crypto");
    const hmac = crypto.createHmac("sha256", secret);
    const expected = hmac.update(JSON.stringify(payload)).digest("hex");
    return crypto.timingSafeEqual(Buffer.from(signature), Buffer.from(expected));
  }

  public async fetchLeadDetails(leadUrn: string, accessToken: string): Promise<any> {
    const res = await fetch(`https://api.linkedin.com/v2/leadForms/${encodeURIComponent(leadUrn)}`, {
      headers: { Authorization: `Bearer ${accessToken}` }
    });
    return res.json();
  }

  public async normalizePayload(raw: any, context: { tenantId: string }): Promise<CanonicalLeadPayload> {
    const answerMap = new Map<string, string>();
    raw.formResponse?.answers?.forEach((a: any) => {
      const key = a.questionText.toLowerCase().replace(/[^a-z0-9]/g, "_");
      answerMap.set(key, a.values[0]);
    });

    return {
      tenantId: context.tenantId,
      source: "linkedin",
      medium: "paid_social",
      campaignName: raw.campaignUrn || "linkedin_b2b_campaign",
      externalLeadId: raw.id,
      externalFormId: raw.formUrn,
      externalAdId: raw.creativeUrn,
      firstName: answerMap.get("first_name") || "",
      lastName: answerMap.get("last_name") || "",
      fullName: `${answerMap.get("first_name") || ""} ${answerMap.get("last_name") || ""}`.trim(),
      email: answerMap.get("work_email") || answerMap.get("email"),
      phoneNumber: answerMap.get("phone_number") || answerMap.get("work_phone"),
      customFields: {
        jobTitle: answerMap.get("job_title"),
        companyName: answerMap.get("company_name"),
        creativeUrn: raw.creativeUrn,
        campaignUrn: raw.campaignUrn
      },
      submittedAt: new Date(raw.submittedAt),
      rawPayload: raw
    };
  }
}
```

---

Previous : [05_Facebook_Lead_Integration.md](./05_Facebook_Lead_Integration.md) | Index: [00_Index.md](../00_Index.md) | Next: [07_X_Twitter_Lead_Integration.md](./07_X_Twitter_Lead_Integration.md)
