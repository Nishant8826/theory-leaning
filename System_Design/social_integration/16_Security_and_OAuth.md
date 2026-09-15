# 16 — Security & OAuth

## 📌 1. Enterprise Security Baseline

A Lead Management System stores sensitive Personally Identifiable Information (PII) and holds OAuth credentials granting direct read/write access to corporate ad accounts and social media pages. A single credential leak could compromise marketing campaigns or violate global privacy laws (GDPR, CCPA, SOC 2).

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              DEFENSE-IN-DEPTH SECURITY MODEL                           │
├───────────────────┬───────────────────┬────────────────────┬───────────────────────────┤
│ 1. Transport      │ 2. Edge & Webhook │ 3. Token Security  │ 4. Multi-Tenant Data      │
│    Security (TLS) │    Validation     │    & Encryption    │    Isolation (RBAC)       │
├───────────────────┼───────────────────┼────────────────────┼───────────────────────────┤
│ Mandatory TLS 1.3 │ Cryptographic     │ AES-256-GCM        │ Strict `tenantId`         │
│ across all API &  │ HMAC SHA-256      │ Envelope           │ partitioning on all DB    │
│ webhook endpoints.│ verification.     │ Encryption w/ KMS. │ queries and cache keys.   │
└───────────────────┴───────────────────┴────────────────────┴───────────────────────────┘
```

---

## 🔐 2. OAuth Token Security & Envelope Encryption

### Why Plaintext Token Storage is Catastrophic
Storing third-party access tokens in plaintext in MongoDB means any internal database backup leak, SQL/NoSQL injection, or unauthorized employee read allows an attacker to hijack the client's Facebook Page or LinkedIn Ad Account.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                          AES-256-GCM ENVELOPE ENCRYPTION ARCHITECTURE                  │
├────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                        │
│  [ Plaintext Token: "EAABw...page_token" ]                                             │
│                     │                                                                  │
│                     ▼                                                                  │
│  [ AWS KMS (Key Management Service) ] ──► Generates unique Data Encryption Key (DEK)   │
│                     │                                                                  │
│                     ▼                                                                  │
│  [ AES-256-GCM Local Cipher ]                                                         │
│  • Encrypts Token with DEK                                                             │
│  • Produces: `ciphertext`, `initializationVector` (IV), and `authTag`                  │
│                     │                                                                  │
│                     ▼                                                                  │
│  [ MongoDB `socialIntegrations` Record ]                                               │
│  Stores: `{ encryptedToken, encryptedDEK, iv, authTag, keyVersion: 1 }`                │
│                                                                                        │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### Production Token Encryption Utility
```typescript
import crypto from 'crypto';

const ALGORITHM = 'aes-256-gcm';
const MASTER_KEY = Buffer.from(process.env.ENCRYPTION_MASTER_KEY_HEX!, 'hex'); // 32 bytes

export interface EncryptedData {
  ciphertext: string;
  iv: string;
  authTag: string;
}

export function encryptSecret(plainText: string): EncryptedData {
  const iv = crypto.randomBytes(12); // Recommended 96-bit IV for GCM
  const cipher = crypto.createCipheriv(ALGORITHM, MASTER_KEY, iv);
  
  let encrypted = cipher.update(plainText, 'utf8', 'hex');
  encrypted += cipher.final('hex');
  const authTag = cipher.getAuthTag().toString('hex');

  return {
    ciphertext: encrypted,
    iv: iv.toString('hex'),
    authTag
  };
}

export function decryptSecret(data: EncryptedData): string {
  const decipher = crypto.createDecipheriv(
    ALGORITHM,
    MASTER_KEY,
    Buffer.from(data.iv, 'hex')
  );
  decipher.setAuthTag(Buffer.from(data.authTag, 'hex'));

  let decrypted = decipher.update(data.ciphertext, 'hex', 'utf8');
  decrypted += decipher.final('utf8');
  return decrypted;
}
```

---

## 🛡️ 3. Webhook Signature Verification (HMAC-SHA256)

Every webhook incoming from Meta, LinkedIn, or Twitter must undergo cryptographic signature verification before reading payload contents:

```typescript
export function verifyMetaSignature(
  rawBodyBuffer: Buffer,
  signatureHeader: string,
  appSecret: string
): boolean {
  if (!signatureHeader || !signatureHeader.startsWith('sha256=')) {
    return false;
  }
  
  const signatureHash = signatureHeader.replace('sha256=', '');
  const hmac = crypto.createHmac('sha256', appSecret);
  hmac.update(rawBodyBuffer);
  const expectedHash = hmac.digest('hex');

  // Timing-safe comparison prevents side-channel timing attacks
  return crypto.timingSafeEqual(
    Buffer.from(signatureHash, 'hex'),
    Buffer.from(expectedHash, 'hex')
  );
}
```

---

## 🏢 4. Multi-Tenant Isolation & Role-Based Access Control (RBAC)

In a multi-tenant SaaS, every request is injected with the authenticated `tenantId` extracted from the verified JWT.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          RBAC ROLE PERMISSION MATRIX                        │
├────────────────────┬───────────┬─────────────┬─────────────┬────────────────┤
│ Role               │ View Leads│ Edit Leads  │ Manage OAuth│ View Analytics │
├────────────────────┼───────────┼─────────────┼─────────────┼────────────────┤
│ **Super Admin**    │ All       │ All         │ Yes         │ Yes (Company)  │
│ **Sales Manager**  │ Team Only │ Team Only   │ No          │ Yes (Team)     │
│ **Sales Rep**      │ Owned Only│ Owned Only  │ No          │ No             │
│ **API Integration**│ Ingest    │ Append Only │ No          │ No             │
└────────────────────┴───────────┴─────────────┴─────────────┴────────────────┘
```

### Express Tenant Enforcement Middleware
```typescript
export function enforceTenantContext(req: any, res: any, next: any) {
  const tenantId = req.user?.tenantId;
  if (!tenantId) {
    return res.status(403).json({ error: 'Tenant context required' });
  }
  
  // Attach tenant context to query filters automatically
  req.tenantFilter = { tenantId };
  next();
}
```

---

Previous : [15_Analytics_and_Reporting.md](./15_Analytics_and_Reporting.md) | Index: [00_Index.md](../00_Index.md) | Next: [17_Webhooks_and_Event_Processing.md](./17_Webhooks_and_Event_Processing.md)
