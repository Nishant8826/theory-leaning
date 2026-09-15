# 14 — Campaign Attribution

## 📌 1. Campaign Modeling & Multi-Tier Hierarchy

In digital marketing and revenue operations, campaigns are rarely monolithic. Enterprise advertising structures follow a **4-Tier Hierarchy**:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              CAMPAIGN TAXONOMY HIERARCHY                               │
├────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                        │
│  [ Level 1: Master Campaign ] ──► e.g. "Global_AI_Summit_2026" (Budget: $200,000)      │
│         │                                                                              │
│         ├────────► [ Level 2: Ad Set / Channel Group ] (e.g. LinkedIn Sponsored InMail)│
│         │                 │                                                            │
│         │                 ├────────► [ Level 3: Ad / Creative ] (e.g. Video_Testimonial)│
│         │                 │                 │                                          │
│         │                 │                 └────────► [ Level 4: Tracking URL / CTA ] │
│         │                 │                            https://acme.com/summit?utm=... │
│         │                 │                                                            │
│         └────────► [ Level 2: Ad Set / Channel Group ] (e.g. Google Search Brand Ads)  │
│                           │                                                            │
│                           └────────► [ Level 3: Ad / Creative ] (e.g. Search_Copy_A)   │
│                                             │                                          │
│                                             └────────► [ Level 4: Tracking URL / CTA ] │
│                                                        https://acme.com/summit?utm=... │
│                                                                                        │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🗄️ 2. Campaign MongoDB Schema (`leadCampaigns`)

```json
{
  "_id": { "$oid": "65f3d001c8e1234567890001" },
  "tenantId": "tenant_acme_corp",
  "name": "Global AI Summit 2026",
  "code": "ai_summit_2026",
  "status": "active",
  "budget": {
    "allocated": 200000,
    "currency": "USD",
    "spentToDate": 84500
  },
  "schedule": {
    "startDate": { "$date": "2026-05-01T00:00:00Z" },
    "endDate": { "$date": "2026-07-31T23:59:59Z" }
  },
  "channels": [
    {
      "source": "linkedin",
      "medium": "paid_social",
      "targetAudience": "CTOs, VPs of Engineering",
      "utmParams": {
        "utm_source": "linkedin",
        "utm_medium": "paid_social",
        "utm_campaign": "ai_summit_2026"
      }
    },
    {
      "source": "google",
      "medium": "cpc",
      "targetAudience": "Keywords: enterprise ai platform",
      "utmParams": {
        "utm_source": "google",
        "utm_medium": "cpc",
        "utm_campaign": "ai_summit_2026"
      }
    }
  ],
  "metrics": {
    "totalLeadsGenerated": 1450,
    "mqlCount": 620,
    "sqlCount": 210,
    "dealsClosed": 42,
    "totalRevenueAttributed": 1250000
  },
  "createdAt": { "$date": "2026-04-15T08:00:00Z" }
}
```

---

## 📊 3. Answering Core Business Questions with Aggregations

### Question 1: "What is the Customer Acquisition Cost (CAC) and ROI for Campaign X?"
```javascript
// MongoDB Aggregation Pipeline
db.leadCampaigns.aggregate([
  { $match: { tenantId: "tenant_acme_corp", code: "ai_summit_2026" } },
  {
    $project: {
      name: 1,
      spent: "$budget.spentToDate",
      dealsClosed: "$metrics.dealsClosed",
      revenue: "$metrics.totalRevenueAttributed",
      cac: {
        $cond: [
          { $gt: ["$metrics.dealsClosed", 0] },
          { $divide: ["$budget.spentToDate", "$metrics.dealsClosed"] },
          0
        ]
      },
      roas: {
        $cond: [
          { $gt: ["$budget.spentToDate", 0] },
          { $divide: ["$metrics.totalRevenueAttributed", "$budget.spentToDate"] },
          0
        ]
      }
    }
  }
]);
```

### Result:
```json
{
  "name": "Global AI Summit 2026",
  "spent": 84500,
  "dealsClosed": 42,
  "revenue": 1250000,
  "cac": 2011.90,
  "roas": 14.79
}
```

---

## ⏳ 4. Attribution Windows & Lookback Logic

An **Attribution Window** defines the maximum allowable elapsed time between an ad interaction (click or impression) and lead creation for attribution credit to be awarded.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          STANDARD ATTRIBUTION WINDOWS                       │
├───────────────────────┬──────────────────────┬──────────────────────────────┤
│ Window Type           │ Lookback Duration    │ Use Case                     │
├───────────────────────┼──────────────────────┼──────────────────────────────┤
│ **Click-Through**     │ 7 to 30 Days         │ Standard Web and Ad Clicks   │
│ **View-Through**      │ 24 Hours (1 Day)     │ Video / Display Impressions  │
│ **Session Lifetime**  │ 30 Minutes           │ Active Web Browsing Session  │
│ **B2B Pipeline**      │ 90 to 180 Days       │ Complex Enterprise Sales     │
└───────────────────────┴──────────────────────┴──────────────────────────────┘
```

When processing an incoming touchpoint, if the time delta between initial ad click and lead conversion exceeds the tenant's configured Lookback Window (e.g. $> 30\text{ days}$), the Attribution Engine assigns credit to `source: "organic"` or `source: "direct"`.

---

Previous : [13_Lead_Ingestion_Architecture.md](./13_Lead_Ingestion_Architecture.md) | Index: [00_Index.md](../00_Index.md) | Next: [15_Analytics_and_Reporting.md](./15_Analytics_and_Reporting.md)
