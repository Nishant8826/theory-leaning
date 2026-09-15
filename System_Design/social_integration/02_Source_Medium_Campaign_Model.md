# 02 — Source, Medium & Campaign Data Model

## 📌 1. Overview & Architectural Objective

To build an extensible Lead Management System (LMS), we must establish a **universal, channel-agnostic attribution schema**. The data model must satisfy two competing constraints:
1. **Strict Standardization**: Marketing and analytics teams require consistent, clean taxonomy (`source: "instagram"`, NOT `"Insta"`, `"IG"`, or `"instagram.com"`).
2. **Infinite Extensibility**: The system must accommodate new platforms (TikTok, WhatsApp, offline QR codes, AI chatbots) without requiring database schema migrations or core code refactoring.

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                           ATTRIBUTION ENTITY RELATIONSHIP MODEL                         │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ┌──────────────────────┐       1:N       ┌────────────────────────┐                    │
│  │     LeadSource       │─────────────────│      LeadCampaign      │                    │
│  │  (e.g., instagram)   │                 │ (e.g., summer_sale_26) │                    │
│  └──────────┬───────────┘                 └───────────┬────────────┘                    │
│             │                                         │                                 │
│             │ 1:N                                     │ 1:N                             │
│             ▼                                         ▼                                 │
│  ┌─────────────────────────────────────────────────────────────────┐                    │
│  │                          LeadTouchpoint                         │                    │
│  │ (Immutable interaction event with Source, Medium, Campaign, UTM)│                    │
│  └─────────────────────────────────┬───────────────────────────────┘                    │
│                                    │ N:1                                                │
│                                    ▼                                                    │
│  ┌─────────────────────────────────────────────────────────────────┐                    │
│  │                              Lead                               │                    │
│  │   (Canonical Profile: denormalized firstTouch & lastTouch)      │                    │
│  └─────────────────────────────────────────────────────────────────┘                    │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🏛️ 2. Controlled vs. Dynamic Attribution Fields

In enterprise systems design, attribution fields are divided into **governed entities** (system-validated) and **dynamic metadata** (free-form tracking parameters).

```
                      ┌──────────────────────────────────────┐
                      │      ATTRIBUTION ATTRIBUTES          │
                      └──────────────────┬───────────────────┘
                                         │
                 ┌───────────────────────┴───────────────────────┐
                 │                                               │
        ┌────────▼────────┐                             ┌────────▼────────┐
        │ Governed Fields │                             │ Dynamic Fields  │
        │ (Standardized)  │                             │ (Contextual)    │
        ├─────────────────┤                             ├─────────────────┤
        │ • Source        │                             │ • Content / Ad  │
        │ • Medium        │                             │ • Search Term   │
        │ • Channel       │                             │ • Landing Page  │
        │ • Campaign ID   │                             │ • Click IDs     │
        │ • Tenant ID     │                             │ • Referrer URL  │
        └─────────────────┘                             └─────────────────┘
```

### Taxonomy Classification Matrix

| Field Name | Type | Governance Level | Purpose & Examples |
| :--- | :--- | :--- | :--- |
| **`source`** | String (Slug) | Governed (Dictionary) | Identifies origin (`instagram`, `facebook`, `linkedin`, `google`, `offline_sales`). |
| **`medium`** | String (Slug) | Governed (Dictionary) | Identifies delivery mechanism (`paid_social`, `organic`, `cpc`, `email`, `qr_code`). |
| **`channel`** | String (Enum) | Governed (System Rollup) | High-level grouping (`Paid Social`, `Organic Search`, `Direct Sales`, `Events`). |
| **`campaign`** | String (Slug) | Governed / Managed | Business marketing campaign name (`summer_sale_2026`, `q3_cto_webinar`). |
| **`content`** | String | Dynamic (Sanitized) | Specific ad creative or CTA variant (`video_explainer_v1`, `hero_btn_blue`). |
| **`term`** | String | Dynamic (Sanitized) | Paid keyword or audience targeted (`crm_software_saas`, `fintech_leads`). |
| **`landing_page`** | String (URL) | Dynamic (Validated URL) | The exact entry URL where the visitor arrived (`https://example.com/demo?utm=...`). |
| **`referrer`** | String (URL) | Dynamic (Validated URL) | HTTP Referer header (`https://l.instagram.com/`, `https://www.google.com/`). |
| **`click_id`** | String | Dynamic (Platform ID) | Ad network tracking token (`fbclid`, `gclid`, `ttclid`, `li_fat_id`, `msclkid`). |
| **`external_lead_id`** | String | Platform-Specific ID | Native lead ID from platform (`fb_lead_gen_12345`, `li_lead_98765`). |

---

## 📋 3. Standardized Catalog of Sources and Mediums

### 1. Governed Sources Catalog
```json
[
  { "slug": "instagram", "displayName": "Instagram", "category": "social", "isDirectIntegration": true },
  { "slug": "facebook", "displayName": "Facebook", "category": "social", "isDirectIntegration": true },
  { "slug": "linkedin", "displayName": "LinkedIn", "category": "social", "isDirectIntegration": true },
  { "slug": "youtube", "displayName": "YouTube", "category": "video", "isDirectIntegration": false },
  { "slug": "twitter_x", "displayName": "X / Twitter", "category": "social", "isDirectIntegration": false },
  { "slug": "google", "displayName": "Google", "category": "search_engine", "isDirectIntegration": false },
  { "slug": "website", "displayName": "Direct Website", "category": "web", "isDirectIntegration": false },
  { "slug": "whatsapp", "displayName": "WhatsApp Business", "category": "messaging", "isDirectIntegration": true },
  { "slug": "sales_team", "displayName": "Sales Outbound", "category": "internal", "isDirectIntegration": false },
  { "slug": "trade_show", "displayName": "Trade Shows & Events", "category": "offline", "isDirectIntegration": false },
  { "slug": "customer_referral", "displayName": "Customer Referral", "category": "referral", "isDirectIntegration": false },
  { "slug": "csv_import", "displayName": "Bulk CSV Import", "category": "batch", "isDirectIntegration": false }
]
```

### 2. Governed Mediums Catalog
```json
[
  { "slug": "paid_social", "displayName": "Paid Social Ads", "defaultChannel": "Paid Social" },
  { "slug": "organic_social", "displayName": "Organic Social Posts / Bio", "defaultChannel": "Organic Social" },
  { "slug": "cpc", "displayName": "Cost-Per-Click Search / Display", "defaultChannel": "Paid Search" },
  { "slug": "organic", "displayName": "Organic Search Engine Traffic", "defaultChannel": "Organic Search" },
  { "slug": "email", "displayName": "Email Newsletter / Outreach", "defaultChannel": "Email Marketing" },
  { "slug": "direct", "displayName": "Direct URL / Untracked", "defaultChannel": "Direct" },
  { "slug": "qr_code", "displayName": "Physical QR Code", "defaultChannel": "Offline Marketing" },
  { "slug": "phone", "displayName": "Inbound / Outbound Phone Call", "defaultChannel": "Sales Outreach" },
  { "slug": "offline", "displayName": "In-Person / Physical Interaction", "defaultChannel": "Field Sales" },
  { "slug": "referral", "displayName": "Referral Link / Partner", "defaultChannel": "Partnerships" }
]
```

---

## 🔍 4. Architectural Debate: Hard-Coded Enums vs. Database-Driven Configuration

When designing the attribution governance layer, software architects face an important decision:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                               ARCHITECTURAL TRADE-OFF MATRIX                           │
├────────────────────────────┬─────────────────────────────┬─────────────────────────────┤
│ Dimension                  │ Option A: TypeScript Enums  │ Option B: DB-Driven Dict    │
├────────────────────────────┼─────────────────────────────┼─────────────────────────────┤
│ Speed of Adding Channels   │ Requires code deploy        │ Instant via Admin UI        │
│ Type-Safety in Backend     │ Compile-time validation     │ Runtime Zod schema / cache  │
│ Custom Tenant Channels     │ Impossible (Hardcoded)      │ Easy (Tenant-scoped sources)│
│ Maintenance Overhead       │ High across services        │ Low (Cached via Redis)      │
└────────────────────────────┴─────────────────────────────┴─────────────────────────────┘
```

### 💡 Staff Architect Recommendation: Hybrid Configuration Pattern
1. **Core Standard Defaults**: Define core universal slugs (`instagram`, `facebook`, `google`, `cpc`, `organic`, `email`) in a system enum to ensure type safety in business logic.
2. **Tenant-Configurable Dictionary in MongoDB**: Store all active sources and mediums in a `leadSources` and `leadMediums` collection.
3. **High-Performance In-Memory Cache**: Cache the governed dictionary in Redis (`SET tenant:123:sources`) with a 1-hour TTL. When an ingestion worker receives a lead, it validates against the Redis cache in < 1ms.

---

## 🧹 5. Normalization & Sanitization Rules for Attribution Parameters

Incoming attribution parameters are frequently distorted by ad networks, marketing agencies, and typos. The LMS Normalization Engine enforces the following sanitization pipeline:

```
Raw Input: "  https://example.com/demo?UTM_SOURCE=Instagram&utm_medium=Paid Social&utm_campaign=Summer%20Sale!  "
                                           │
                                           ▼
                             [ Lowercase Normalization ]
                                           │
                                           ▼
                             [ Slugification & Trim ]
                             ("Paid Social" -> "paid_social")
                             ("Summer Sale!" -> "summer_sale")
                                           │
                                           ▼
                             [ Alias Mapping Dictionary ]
                             ("insta", "ig", "instagram.com" -> "instagram")
                                           │
                                           ▼
Clean Output: {
  source: "instagram",
  medium: "paid_social",
  campaign: "summer_sale"
}
```

### Standardization Rules:
1. **Lowercase String Conversion**: All source, medium, and campaign identifiers are coerced to lowercase.
2. **Whitespace and Special Character Replacement**: Spaces, hyphens, and punctuation are converted to snake_case (`paid-social` -> `paid_social`).
3. **Alias Resolution**: Common vendor aliases are mapped to canonical identifiers:
   * `fb`, `facebook.com`, `m.facebook.com` $\rightarrow$ `facebook`
   * `ig`, `insta`, `l.instagram.com` $\rightarrow$ `instagram`
   * `tw`, `x.com`, `t.co` $\rightarrow$ `twitter_x`
   * `yt`, `youtube.com`, `youtu.be` $\rightarrow$ `youtube`
   * `linkedin.com`, `lnkd.in` $\rightarrow$ `linkedin`

---

## 🔗 6. Ad Click Identifiers (Click IDs) Architecture

Modern digital ad platforms append proprietary query parameters to landing page URLs. Capturing and storing these Click IDs is crucial for conversion reconciliation (Server-to-Server / CAPI):

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          MAJOR AD PLATFORM CLICK IDS                        │
├─────────────────┬────────────────────────────┬──────────────────────────────┤
│ Platform        │ Parameter Key              │ Purpose                      │
├─────────────────┼────────────────────────────┼──────────────────────────────┤
│ Google Ads      │ `gclid` / `wbraid` / `gbraid`│ Offline Conversion Import   │
│ Meta (FB / IG)  │ `fbclid`                   │ Meta Conversions API (CAPI)  │
│ LinkedIn        │ `li_fat_id`                │ LinkedIn Conversion API      │
│ TikTok          │ `ttclid`                   │ TikTok Events API            │
│ Microsoft / Bing│ `msclkid`                  │ Microsoft Advertising Sync   │
│ Twitter / X     │ `twclid`                   │ X Ads Conversion Tracking    │
└─────────────────┴────────────────────────────┴──────────────────────────────┘
```

When a visitor lands on a website, the LMS client tracking script extracts all matching Click IDs, persists them in browser storage, and attaches them to the `LeadTouchpoint` document upon form submission.

---

Previous : [01_Lead_Attribution_Fundamentals.md](./01_Lead_Attribution_Fundamentals.md) | Index: [00_Index.md](../00_Index.md) | Next: [03_Social_Media_Lead_Architecture.md](./03_Social_Media_Lead_Architecture.md)
