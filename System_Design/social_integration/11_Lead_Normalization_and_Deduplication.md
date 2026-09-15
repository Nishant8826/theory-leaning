# 11 — Lead Normalization & Deduplication

## 📌 1. The Multi-Platform Data Fragmentation Challenge

When aggregating leads across Instagram, Facebook, LinkedIn, Google Ads, and manual CSV imports, incoming payloads are completely non-uniform:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        RAW PLATFORM PAYLOAD INCONSISTENCY                              │
├─────────────────────┬──────────────────────┬────────────────────┬──────────────────────┤
│ Instagram           │ Facebook             │ LinkedIn           │ Website Webform      │
├─────────────────────┼──────────────────────┼────────────────────┼──────────────────────┤
│ `first_name`: "Alex"│ `full_name`: "Alex R"│ `firstName`: "Alex"│ `name`: "Alex Rivera"│
│ `last_name`: "R"    │ `email`: "ALEX@G.COM"│ `lastName`: "Rivera│ `work_email`: "alex" │
│ `phone`: "4155552671│ `phone_number`:      │ `work_email`:      │ `tel`: "(415)5552671"│
│                     │ "+1 (415) 555-2671"  │ "alex@enterprise"  │                      │
└─────────────────────┴──────────────────────┴────────────────────┴──────────────────────┘
```

Without a rigorous **Normalization and Deduplication Engine**, the CRM quickly degrades with duplicate contacts, corrupted names, un-callable phone numbers, and misallocated sales commissions.

---

## 🧹 2. The Normalization Engine Pipeline

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                             LEAD NORMALIZATION PIPELINE                                 │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  [ Raw Ingestion Payload ]                                                              │
│              │                                                                          │
│              ▼ 1. Email Normalization                                                   │
│  • Strip leading/trailing whitespaces                                                   │
│  • Convert to lowercase (`ALEX.R@GMAIL.COM` ──► `alex.r@gmail.com`)                     │
│  • Validate RFC 5322 regex syntax                                                       │
│              │                                                                          │
│              ▼ 2. Phone Normalization (Google libphonenumber)                           │
│  • Detect country calling code (default to Tenant's default country if omitted)         │
│  • Strip parentheses, dashes, spaces: `(415) 555-2671`                                  │
│  • Convert to international standard **E.164**: `+14155552671`                          │
│              │                                                                          │
│              ▼ 3. Name Sanitization & Parsing                                           │
│  • Capitalize First Letters: `alex rivera` ──► `Alex Rivera`                            │
│  • If only `full_name` provided: parse into `firstName = Alex`, `lastName = Rivera`     │
│  • If `firstName` & `lastName` provided: concatenate to `fullName`                      │
│              │                                                                          │
│              ▼ 4. Attribution & UTM Sanitization                                        │
│  • Slugs converted to lowercase snake_case (`Paid Social` ──► `paid_social`)             │
│  • Match against Governed Sources Dictionary                                            │
│              │                                                                          │
│              ▼ 5. Legal Consent & GDPR/TCPA Validation                                  │
│  • Timestamp consent opt-in, IP address, and privacy policy version                     │
│              │                                                                          │
│  [ Pristine CanonicalLead Object ]                                                      │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔍 3. Deduplication Architecture: Identity Signals & Matching

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              IDENTITY SIGNAL HIERARCHY                                 │
├─────────────────┬─────────────────┬────────────────────┬───────────────────────────────┤
│ Tier 1 (Master) │ Tier 2 (Primary)│ Tier 3 (Secondary) │ Tier 4 (Fuzzy Match)          │
├─────────────────┼─────────────────┼────────────────────┼───────────────────────────────┤
│ Tenant ID +     │ Tenant ID +     │ Tenant ID +        │ Tenant ID +                   │
│ Normalized      │ Normalized      │ Platform Identity  │ (Soundex / Levenshtein Name + │
│ E.164 Phone     │ Email Address   │ (`externalLeadId`) │ Company / Postal Code)        │
└─────────────────┴─────────────────┴────────────────────┴───────────────────────────────┘
```

### Exact Matching vs. Fuzzy Matching
1. **Exact Matching (Deterministic)**: 
   ```typescript
   // MongoDB Compound Query (Indexed)
   const existingLead = await Lead.findOne({
     tenantId: context.tenantId,
     $or: [
       { email: canonical.email },
       { phone: canonical.phoneNumber }
     ]
   });
   ```
2. **Fuzzy Matching (Probabilistic)**:
   * Used when email/phone is missing or typos exist (e.g. `alex.riviera@corp.com` vs `alex.rivera@corp.com`).
   * Algorithms: **Jaro-Winkler distance** (similarity $> 0.88$) and **Double Metaphone / Soundex** for names.
   * **Rule**: Probabilistic matches are NEVER merged automatically in production. Instead, they trigger a "Potential Duplicate" flag for manual sales review to avoid destructive data corruption.

---

## 🔀 4. Merge Strategies & Conflict Resolution Rules

When an incoming lead matches an existing contact in the database, the system executes the following deterministic merge logic:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        DEDUPLICATION MERGE DECISION MATRIX                             │
├─────────────────────────┬──────────────────────────────────────────────────────────────┤
│ Field Category          │ Conflict Resolution Action                                   │
├─────────────────────────┼──────────────────────────────────────────────────────────────┤
│ **First-Touch**         │ **IMMUTABLE**: Retain original acquisition source & campaign.│
│ **Last-Touch**          │ **OVERWRITE**: Update with current interaction metadata.     │
│ **Touchpoints Stream**  │ **APPEND**: Push new `LeadTouchpoint` record to history.     │
│ **Missing Core Data**   │ **FILL GAPS**: If existing lead had no phone, populate it.   │
│ **Assigned Lead Owner** │ **PRESERVE**: Do NOT change assigned sales rep automatically.│
│ **Lifecycle Stage**     │ **ADVANCE ONLY**: Prospect ──► MQL, but never regress Won ──►│
│ **External Identities** │ **APPEND**: Add `{ platform: "linkedin", id: "..." }`.       │
└─────────────────────────┴──────────────────────────────────────────────────────────────┘
```

---

## 💻 5. Canonical Normalizer Implementation

```typescript
import { parsePhoneNumber, CountryCode } from 'libphonenumber-js';

export class LeadNormalizer {
  public static normalize(raw: any, defaultCountry: CountryCode = 'US'): CanonicalLeadPayload {
    // 1. Email Normalization
    let cleanEmail: string | undefined = undefined;
    if (raw.email) {
      cleanEmail = raw.email.trim().toLowerCase();
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(cleanEmail)) {
        cleanEmail = undefined; // Flag invalid email
      }
    }

    // 2. Phone Normalization (E.164)
    let cleanPhone: string | undefined = undefined;
    if (raw.phoneNumber || raw.phone) {
      try {
        const parsed = parsePhoneNumber(raw.phoneNumber || raw.phone, defaultCountry);
        if (parsed && parsed.isValid()) {
          cleanPhone = parsed.format('E.164'); // e.g. +14155552671
        }
      } catch (err) {
        cleanPhone = raw.phoneNumber || raw.phone; // Fallback to raw if unparseable
      }
    }

    // 3. Name Normalization
    let fullName = (raw.fullName || raw.name || '').trim();
    let firstName = raw.firstName || '';
    let lastName = raw.lastName || '';

    if (fullName && (!firstName || !lastName)) {
      const parts = fullName.split(/\s+/);
      firstName = parts[0] || '';
      lastName = parts.slice(1).join(' ') || '';
    } else if (firstName && !fullName) {
      fullName = `${firstName} ${lastName}`.trim();
    }

    return {
      tenantId: raw.tenantId,
      source: (raw.source || 'website').toLowerCase().trim(),
      medium: (raw.medium || 'direct').toLowerCase().trim(),
      campaignName: (raw.campaignName || raw.campaign || 'unspecified').toLowerCase().trim(),
      externalLeadId: raw.externalLeadId || '',
      fullName,
      firstName,
      lastName,
      email: cleanEmail,
      phoneNumber: cleanPhone,
      customFields: raw.customFields || {},
      submittedAt: raw.submittedAt ? new Date(raw.submittedAt) : new Date(),
      rawPayload: raw.rawPayload || raw
    };
  }
}
```

---

## ⚠️ 6. Critical Risks of Incorrect Lead Merging

1. **Cross-Tenant Data Leakage**: In a multi-tenant SaaS, merging by email without filtering by `tenantId` allows Tenant A's salesperson to view Tenant B's confidential enterprise leads.
2. **Shared Family / Corporate Landlines**: Merging solely on a shared phone number (`+18005550100`) could combine two completely different corporate executives into one record.
3. **Sales Commission Disputes**: Overwriting a lead's original owner during an automated webform submission causes internal sales friction and misaligned incentives.

---

Previous : [10_Offline_Lead_Attribution.md](./10_Offline_Lead_Attribution.md) | Index: [00_Index.md](../00_Index.md) | Next: [12_Attribution_Data_Model.md](./12_Attribution_Data_Model.md)
