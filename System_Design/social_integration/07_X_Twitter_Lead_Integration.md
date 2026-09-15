# 07 — X / Twitter Lead Integration

## 📌 1. Overview & Architectural Realities

Unlike Meta and LinkedIn—which offer native in-app "Instant Lead Generation Forms"—lead acquisition on **X (formerly Twitter)** predominantly operates via **traffic redirection and tracking links**.

While X provides direct messaging automation and developer APIs (X Developer API v2), enterprise LMS design for X centers around **Attribution-Driven Landing Page Conversion** and **X Click ID (`twclid`) Tracking**.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              X / TWITTER LEAD ACQUISITION MODES                        │
├──────────────────────────────┬───────────────────────────────┬─────────────────────────┤
│ 1. Sponsored Web Ads         │ 2. Organic Posts & Bio Links  │ 3. Direct Message (DM)  │
├──────────────────────────────┼───────────────────────────────┼─────────────────────────┤
│ Promoted Tweet with CTA card │ Pinned tweet or Bio link with │ Automated DM chat flow  │
│ appending UTMs + `twclid` -> │ tracking shortlink -> Landing │ capturing lead email in │
│ High-conversion Landing Page.│ Page form submission.         │ conversation (Chatbot). │
└──────────────────────────────┴───────────────────────────────┴─────────────────────────┘
```

> [!NOTE]
> **API Verification Notice**: X's developer tiers, endpoint access (API v2 / Account Activity API), and webhook pricing models change periodically. Always verify against the official X Developer Portal before designing direct API-based webhook ingestion.

---

## 🔗 2. Attribution-Driven Web Traffic Pipeline

The core mechanism for attributing leads from X relies on disciplined UTM parameters and click token capture:

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│   X Sponsored   │       │ LMS Client SDK  │       │  Lead Submit    │       │ Universal LMS   │
│   Post / Tweet  │       │ on Landing Page │       │  Web Form       │       │ Ingestion API   │
└────────┬────────┘       └────────┬────────┘       └────────┬────────┘       └────────┬────────┘
         │                         │                         │                         │
         │ 1. Click Ad             │                         │                         │
         │ (utm_source=twitter_x   │                         │                         │
         │ &twclid=1928301)        │                         │                         │
         ├────────────────────────►│                         │                         │
         │                         │ 2. Extracts UTMs &      │                         │
         │                         │    `twclid` to Cookie   │                         │
         │                         │    & LocalStorage       │                         │
         │                         │                         │                         │
         │                         │ 3. User Fills Form      │                         │
         │                         ├────────────────────────►│                         │
         │                         │                         │ 4. POST /api/v1/leads   │
         │                         │                         │    (with UTM + twclid)  │
         │                         │                         ├────────────────────────►│
         │                         │                         │                         │
         │                         │                         │                         │ 5. Attribution  │
         │                         │                         │                         │    Engine Logs  │
         │                         │                         │                         │    Touchpoint   │
```

---

## 📦 3. Normalized Payload for X-Generated Leads

When the website lead form submits data originating from X, the client-side tracking script attaches attribution metadata:

```json
{
  "tenantId": "tenant_acme_corp",
  "source": "twitter_x",
  "medium": "paid_social",
  "campaign": "developer_ai_tool_launch",
  "content": "infographic_card_v2",
  "term": "ai_agents_devops",
  "name": "Jordan Smith",
  "email": "jordan.smith@devops.io",
  "phone": "+12065550199",
  "clickId": {
    "type": "twclid",
    "value": "1782910482019482"
  },
  "landingPage": "https://example.com/products/ai-agent?utm_source=twitter_x&utm_medium=paid_social&utm_campaign=developer_ai_tool_launch&twclid=1782910482019482",
  "referrer": "https://t.co/98ad8s7d6"
}
```

---

## 🤖 4. Direct Message (DM) Ingestion via X API v2 (Optional Advanced Mode)

For organizations running conversational lead generation on X, an automated bot interacts with prospective customers over DM.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              X DIRECT MESSAGE INGESTION                                │
├────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                        │
│  1. Prospect sends DM: "Interested in Enterprise Pricing"                              │
│  2. X Webhook (Account Activity API) sends CRC challenge and event payload             │
│  3. LMS Chatbot Worker executes conversational prompt:                                 │
│     └── "Thanks for reaching out! What is your corporate email address?"               │
│  4. User replies: "jordan@devops.io"                                                   │
│  5. LMS Regex & Verification engine extracts contact details                           │
│  6. Ingestion Gateway creates Canonical Lead:                                          │
│     └── source: "twitter_x", medium: "direct_message", campaign: "dm_inbound"          │
│                                                                                        │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

Previous : [06_LinkedIn_Lead_Integration.md](./06_LinkedIn_Lead_Integration.md) | Index: [00_Index.md](../00_Index.md) | Next: [08_YouTube_Lead_Integration.md](./08_YouTube_Lead_Integration.md)
