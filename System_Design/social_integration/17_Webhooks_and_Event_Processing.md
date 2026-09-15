# 17 — Webhooks & Event Processing

## 📌 1. Webhook Reliability Challenges

In distributed systems, webhooks operate over an unreliable network. Third-party ad networks (Meta, LinkedIn, Twilio) provide **at-least-once delivery guarantees**, which introduces four fundamental distributed systems challenges:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              WEBHOOK FAILURE MODES & HAZARDS                           │
├─────────────────┬─────────────────┬────────────────────┬───────────────────────────────┤
│ 1. Duplicate    │ 2. Out-of-Order │ 3. Network         │ 4. Poison Pill                │
│    Deliveries   │    Arrivals     │    Timeouts        │    Payloads                   │
├─────────────────┼─────────────────┼────────────────────┼───────────────────────────────┤
│ Meta sends the  │ An "Update"     │ If LMS takes >5s   │ A malformed payload crashes   │
│ same `leadgen`  │ webhook arrives │ to respond, Meta   │ the worker repeatedly,        │
│ webhook 3 times │ before the      │ flags endpoint as  │ blocking all other leads in   │
│ in 10 seconds.  │ "Create" event. │ down & retries.    │ the queue.                    │
└─────────────────┴─────────────────┴────────────────────┴───────────────────────────────┘
```

---

## 🔒 2. Idempotency Engine Architecture

To ensure that processing the same webhook multiple times produces the exact same state without creating duplicate leads, we implement a **Redis Distributed Idempotency Guard**:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                           REDIS IDEMPOTENCY EXECUTION FLOW                             │
├────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                        │
│  Inbound Webhook Event (Platform: "facebook", ID: "leadgen_109823487123984")           │
│         │                                                                              │
│         ▼                                                                              │
│  [ Generate Idempotency Key ] ──► `idempotency:webhook:facebook:leadgen_109823487123984`│
│         │                                                                              │
│         ▼                                                                              │
│  [ Redis SET key "processing" NX EX 86400 ]                                            │
│         │                                                                              │
│         ├──► Key Already Exists? ──► Log "Duplicate Event Dropped" ──► Return 200 OK   │
│         │                                                                              │
│         └──► Key Acquired Successfully ──► Proceed to Enqueue & Process                │
│                                                                                        │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### TypeScript Redis Idempotency Guard
```typescript
import Redis from 'ioredis';

const redis = new Redis(process.env.REDIS_URL!);

export async function acquireWebhookLock(
  platform: string,
  eventId: string,
  ttlSeconds: number = 86400 // 24-hour deduplication window
): Promise<boolean> {
  const key = `idempotency:webhook:${platform}:${eventId}`;
  // SET key value NX (only if Not eXists) EX (expiry in seconds)
  const result = await redis.set(key, 'locked', 'EX', ttlSeconds, 'NX');
  return result === 'OK';
}
```

---

## 🔁 3. Retry Policies & Dead-Letter Queue (DLQ)

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              RETRY & DLQ STATE MACHINE                                 │
├────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                        │
│  [ Incoming Webhook Job ]                                                              │
│            │                                                                           │
│            ▼                                                                           │
│  [ Worker Execution ] ──► Success ──► Complete Job                                     │
│            │                                                                           │
│            ▼ (Transient Error: Graph API 503 / DB Connection Timeout)                  │
│  [ Exponential Backoff Retries ]                                                       │
│    • Attempt 1: 5 seconds delay                                                        │
│    • Attempt 2: 30 seconds delay                                                       │
│    • Attempt 3: 5 minutes delay                                                        │
│    • Attempt 4: 30 minutes delay                                                       │
│            │                                                                           │
│            ▼ (Max 5 Attempts Exhausted OR Unrecoverable 400 Bad Request)               │
│  [ Dead-Letter Queue (DLQ) ]                                                           │
│  • Preserves raw payload, stack trace, and timestamps for 14 days                      │
│  • Triggers PagerDuty / Slack Alert to On-Call Engineer                                │
│                                                                                        │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## ⏳ 4. Out-of-Order Event Sequencing

In high-concurrency environments, an `update_lead` webhook may reach the LMS worker before the initial `create_lead` webhook has finished writing to MongoDB.

### Resolution: Version Clocks & Monotonic Timestamps
1. Every event envelope carries the provider's `created_time` (Unix millisecond timestamp).
2. When updating a lead, the MongoDB query uses conditional updates:
```javascript
// Only update if incoming event timestamp is strictly newer than current state
await Lead.updateOne(
  { 
    _id: leadId, 
    lastEventTimestamp: { $lt: incomingEventTimestamp } 
  },
  { 
    $set: { 
      status: incomingStatus,
      lastEventTimestamp: incomingEventTimestamp 
    } 
  }
);
```

---

Previous : [16_Security_and_OAuth.md](./16_Security_and_OAuth.md) | Index: [00_Index.md](../00_Index.md) | Next: [18_Scaling_and_Reliability.md](./18_Scaling_and_Reliability.md)
