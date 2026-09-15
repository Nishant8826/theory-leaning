# 10 — Offline Lead Attribution

## 📌 1. Bridging Physical & Digital Worlds

A significant portion of enterprise revenue originates from physical, non-digital channels: trade shows, outbound sales reps, inbound phone calls, direct mail, billboards, and walk-in meetings. 

A world-class Lead Management System treats offline touchpoints as **first-class citizens**, mapping them seamlessly into the universal **Source $\rightarrow$ Medium $\rightarrow$ Campaign** attribution taxonomy.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              OFFLINE ATTRIBUTION CHANNELS                              │
├─────────────────┬─────────────────┬────────────────────┬───────────────────────────────┤
│ 1. Dynamic QR   │ 2. Call         │ 3. Field Sales Rep │ 4. In-Person Trade Shows      │
│    Codes        │    Tracking DNI │    Direct Entry    │    & Badge Scanners           │
├─────────────────┼─────────────────┼────────────────────┼───────────────────────────────┤
│ Print posters,  │ Unique virtual  │ Sales rep creates  │ Conference badge scan or      │
│ billboards, and │ phone numbers   │ lead manually via  │ business card OCR scanner     │
│ flyers with     │ per campaign    │ LMS Mobile App     │ synced via batch ingestion    │
│ embedded UTMs.  │ (Twilio/Exotel).│ during outreach.   │ pipeline.                     │
└─────────────────┴─────────────────┴────────────────────┴───────────────────────────────┘
```

---

## 📱 2. QR Code Attribution Architecture

QR codes provide a direct bridge from physical collateral to our digital attribution pipeline:

```
┌─────────────────────────┐
│     Physical Asset      │
│ (e.g., Billboard Banner)│
│  "Scan for 20% Discount"│
└────────────┬────────────┘
             │
             ▼ 1. User Scans QR with Phone Camera
┌──────────────────────────────────────────────────────────┐
│             LMS Short-Link & Redirect Service            │
│   https://link.acme.com/qr/delhi-expo-2026               │
└────────────────────────────┬─────────────────────────────┘
                             │
                             ▼ 2. Server Logs Scan Event & Redirects with Clean UTMs
┌──────────────────────────────────────────────────────────┐
│              Target Landing Page Destination             │
│   https://acme.com/offer?                                │
│     utm_source=trade_show                                │
│     &utm_medium=qr_code                                  │
│     &utm_campaign=delhi_tech_expo_2026                   │
│     &utm_content=booth_a4_standee                        │
│     &scan_id=scan_98a7sd8f7a9sd                          │
└────────────────────────────┬─────────────────────────────┘
                             │
                             ▼ 3. User Submits Lead Form
┌──────────────────────────────────────────────────────────┐
│                    Universal LMS Database                │
│    Lead created with full physical event attribution!    │
└──────────────────────────────────────────────────────────┘
```

### Dynamic QR Code Generator Schema
```json
{
  "_id": "qr_campaign_9812",
  "tenantId": "tenant_acme_corp",
  "campaignId": "camp_delhi_expo_2026",
  "shortCode": "delhi-expo-2026",
  "destinationUrl": "https://acme.com/offer",
  "attribution": {
    "source": "trade_show",
    "medium": "qr_code",
    "campaign": "delhi_tech_expo_2026",
    "content": "booth_a4_standee"
  },
  "totalScans": 1420,
  "uniqueScans": 1104,
  "leadsGenerated": 182,
  "isActive": true
}
```

---

## 📞 3. Telephony & Call Tracking Attribution (Twilio / Exotel / Plivo)

When prospective buyers call a sales hotline, how does the system know which billboard, TV ad, or Google ad prompted the call?

We implement **Dynamic Number Insertion (DNI)** and **Campaign Virtual Hotlines**:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                          INBOUND CALL ATTRIBUTION PIPELINE                             │
├────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                        │
│  Marketing Channel: Newspaper Ad in Tech Weekly                                       │
│  Assigned Phone Number: +1 (800) 555-0144 (Virtual Twilio Number)                      │
│                                                                                        │
│  1. Prospect dials +1 (800) 555-0144                                                   │
│  2. Twilio receives call and posts webhook to LMS: `POST /api/v1/webhooks/telephony`   │
│  3. LMS Telephony Adapter:                                                             │
│     ├── Looks up assigned campaign for +1 (800) 555-0144                               │
│     └── Maps: source = "print_media", medium = "phone", campaign = "tech_weekly_q2"    │
│  4. LMS searches existing leads by Caller Phone (`+14155552671`):                      │
│     ├── Found: Appends `LeadTouchpoint` (Call duration: 4m 30s)                        │
│     └── Not Found: Spawns new Lead assigned to Inbound Sales Queue                     │
│  5. Twilio connects call to Sales Rep's desk phone / WebRTC Softphone                  │
│                                                                                        │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 👔 4. Outbound Sales Rep & Manual Lead Attribution

When a sales representative meets a client or conducts cold outbound prospecting, they manually input the lead via the LMS CRM interface.

### Strict Governance in UI
To prevent sales reps from typing arbitrary strings (`"met at lunch"`, `"friend"`), the LMS UI presents **governed dropdowns**:

```json
{
  "tenantId": "tenant_acme_corp",
  "source": "sales_team",
  "medium": "offline",
  "campaign": "outbound_banking_q3",
  "leadOwnerId": "user_rep_rajesh_sharma",
  "fullName": "Vikram Malhotra",
  "email": "vikram.m@hdfcbank.com",
  "phone": "+919820012345",
  "customFields": {
    "meetingLocation": "Mumbai Corporate HQ",
    "opportunitySize": 100000
  },
  "firstTouch": {
    "source": "sales_team",
    "medium": "offline",
    "campaign": "outbound_banking_q3",
    "timestamp": "2026-06-15T09:30:00Z"
  }
}
```

---

Previous : [09_Website_UTM_Tracking.md](./09_Website_UTM_Tracking.md) | Index: [00_Index.md](../00_Index.md) | Next: [11_Lead_Normalization_and_Deduplication.md](./11_Lead_Normalization_and_Deduplication.md)
