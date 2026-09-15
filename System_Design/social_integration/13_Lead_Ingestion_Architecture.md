# 13 — Lead Ingestion Architecture

## 📌 1. High-Throughput Ingestion Pipeline Overview

A robust Lead Ingestion Pipeline must handle heterogeneous workloads: from unpredictable viral traffic surges (5,000 leads in 60 seconds from a Super Bowl ad) to bulk background CSV uploads (500,000 legacy contacts) without degrading CRM response times.

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 END-TO-END INGESTION DATA FLOW                                   │
├──────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                  │
│   [ Inbound Sources ]                                                                            │
│   • Social Webhooks (Meta, LinkedIn)    • Website UTM Webforms    • Telephony (Twilio Calls)     │
│   • Public Ingestion API                • Bulk CSV Uploads        • Field Sales CRM Entry        │
│                    │                                                                             │
│                    ▼                                                                             │
│   ┌──────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                 1. INGESTION API GATEWAY                                 │   │
│   │   • Edge TLS & Rate Limiting               • HMAC / API Key / JWT Auth                   │   │
│   │   • Fast Schema Validation (Zod)           • Return 200 OK (<50ms)                       │   │
│   └─────────────────────────────────────────────┬────────────────────────────────────────────┘   │
│                                                 │                                                │
│                                                 ▼ Raw Job Packet                                 │
│   ┌──────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                 2. INGESTION QUEUE BUFFER                                │   │
│   │   • Redis / BullMQ (MERN Scale)            • AWS SQS / Apache Kafka (Enterprise Scale)   │   │
│   │   • Redis Distributed Lock Idempotency Guard (Key: `ingest:{tenantId}:{eventId}`)        │   │
│   └─────────────────────────────────────────────┬────────────────────────────────────────────┘   │
│                                                 │                                                │
│                                                 ▼ Dequeue Job                                    │
│   ┌──────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                 3. PIPELINE WORKER POOL                                  │   │
│   │                                                                                          │   │
│   │   [ Adapter Unpack ] ──► [ Normalizer ] ──► [ Deduplicator ] ──► [ Attribution Engine ]  │   │
│   │   Fetch platform PII     Clean Phone/Email    Email/Phone Match    Attach UTM & Touchpoint   │   │
│   └─────────────────────────────────────────────┬────────────────────────────────────────────┘   │
│                                                 │                                                │
│                                                 ▼ ACID Transaction                               │
│   ┌──────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                 4. STORAGE & EVENT DISPATCH                              │   │
│   │   • MongoDB Primary (`leads`, `leadTouchpoints`, `externalLeadMappings`)                 │   │
│   │   • Publish Event: `LeadCreated` / `LeadUpdated`                                         │   │
│   └─────────────────────────────────────────────┬────────────────────────────────────────────┘   │
│                                                 │                                                │
│                                                 ▼ Event Bus Subscribers                          │
│   ┌──────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                 5. DOWNSTREAM BUSINESS ACTIONS                           │   │
│   │   • Round-Robin Sales Assignment           • Slack / Email Sales Alert                   │   │
│   │   • Automated Email Drip Trigger           • External Webhook Dispatch                   │   │
│   └──────────────────────────────────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## ⚖️ 2. Synchronous vs. Asynchronous Ingestion

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              INGESTION MODE COMPARISON                                 │
├────────────────────────────┬─────────────────────────────┬─────────────────────────────┤
│ Architectural Dimension    │ Synchronous Ingestion       │ Asynchronous (Queued)       │
├────────────────────────────┼─────────────────────────────┼─────────────────────────────┤
│ Response Latency           │ 800ms - 2,500ms (Slow)      │ 20ms - 50ms (Ultra-Fast)    │
│ Webhook Timeout Risk       │ High (Meta drops after 5s)  │ Zero (200 OK sent instantly)│
│ Database Backpressure      │ Surges crash MongoDB CPU    │ Queue absorbs and buffers   │
│ Resilience to API Outages  │ Lost leads if DB restarts   │ Guaranteed at-least-once    │
│ Implementation Complexity  │ Minimal                     │ Requires Queue Worker infra │
│ Recommended Use Case       │ None (Never in Production)  │ **Universal Standard**      │
└────────────────────────────┴─────────────────────────────┴─────────────────────────────┘
```

---

## 📬 3. Message Broker Selection Matrix

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              MESSAGE BROKER EVALUATION                                 │
├───────────────────┬──────────────────────┬──────────────────────┬──────────────────────┤
│ Broker Technology │ Throughput Capacity  │ Operational Overhead │ Best Fit             │
├───────────────────┼──────────────────────┼──────────────────────┼──────────────────────┤
│ **Redis + BullMQ**│ 10,000 jobs/sec      │ Low (Shares Redis)   │ **MERN Stack Choice**│
│ **AWS SQS**       │ Near-infinite        │ Zero (Fully Managed) │ Cloud-Native Serverless│
│ **RabbitMQ**      │ 50,000 msgs/sec      │ Medium (Clustering)  │ Complex routing topologies│
│ **Apache Kafka**  │ 1,000,000+ msgs/sec  │ High (ZooKeeper/KRaft)│ Global Multi-Region BigData│
└───────────────────┴──────────────────────┴──────────────────────┴──────────────────────┘
```

### 💡 Staff Architect Recommendation for MERN Architecture
Deploy **Redis + BullMQ**. BullMQ provides native TypeScript interfaces, built-in exponential backoff retries, dead-letter queues, priority queues (e.g., paid ad leads processed before CSV batch imports), and parent-child dependency flows without the operational overhead of running a Kafka cluster.

---

## 💻 4. Resilient Ingestion Worker Implementation

```typescript
import { Worker, Job } from 'bullmq';
import { SocialAdapterFactory } from './SocialAdapterFactory';
import { LeadNormalizer } from './LeadNormalizer';
import { Lead } from '../models/Lead';
import { LeadTouchpoint } from '../models/LeadTouchpoint';
import { ExternalLeadMapping } from '../models/ExternalLeadMapping';

export const leadIngestionWorker = new Worker(
  'lead-ingestion-queue',
  async (job: Job) => {
    const { tenantId, platform, rawPayload, connectionConfig } = job.data;

    // 1. Resolve Platform Adapter
    const adapter = SocialAdapterFactory.getAdapter(platform);

    // 2. Fetch Additional Platform Data if needed (e.g. Meta Graph API)
    let leadData = rawPayload;
    if (adapter.platform === 'facebook' || adapter.platform === 'instagram') {
      leadData = await adapter.fetchLeadDetails(rawPayload.leadgen_id, connectionConfig.pageAccessToken);
    }

    // 3. Normalize into Canonical Domain Object
    const canonical = await adapter.normalizePayload(leadData, { tenantId });
    const validated = LeadNormalizer.normalize(canonical);

    // 4. Deduplication & Persistence within MongoDB Transaction
    const session = await Lead.startSession();
    session.startTransaction();

    try {
      // Deterministic Identity Match (Email or Phone within Tenant)
      let lead = await Lead.findOne({
        tenantId,
        $or: [
          ...(validated.email ? [{ email: validated.email }] : []),
          ...(validated.phoneNumber ? [{ phone: validated.phoneNumber }] : [])
        ]
      }).session(session);

      const touchpointData = {
        tenantId,
        source: validated.source,
        medium: validated.medium,
        campaignName: validated.campaignName,
        submittedAt: validated.submittedAt,
        rawPayload: validated.rawPayload
      };

      if (!lead) {
        // Create New Lead Record
        lead = new Lead({
          tenantId,
          fullName: validated.fullName,
          firstName: validated.firstName,
          lastName: validated.lastName,
          email: validated.email,
          phone: validated.phoneNumber,
          status: 'new',
          firstTouch: touchpointData,
          lastTouch: touchpointData,
          touchpointsCount: 1,
          customFields: validated.customFields
        });
        await lead.save({ session });
      } else {
        // Update Existing Lead Record
        lead.lastTouch = touchpointData;
        lead.touchpointsCount += 1;
        // Fill missing contact fields
        if (!lead.phone && validated.phoneNumber) lead.phone = validated.phoneNumber;
        if (!lead.email && validated.email) lead.email = validated.email;
        await lead.save({ session });
      }

      // 5. Append Immutable Touchpoint Record
      const touchpoint = new LeadTouchpoint({
        ...touchpointData,
        leadId: lead._id
      });
      await touchpoint.save({ session });

      // 6. Record External Mapping for O(1) Idempotency
      if (validated.externalLeadId) {
        await ExternalLeadMapping.updateOne(
          { tenantId, platform, externalLeadId: validated.externalLeadId },
          { $set: { internalLeadId: lead._id, createdAt: new Date() } },
          { upsert: true, session }
        );
      }

      await session.commitTransaction();

      // 7. Publish Event to Event Bus for downstream listeners
      await eventBus.publish('lead.ingested', { tenantId, leadId: lead._id, isNew: !lead.createdAt });
    } catch (error) {
      await session.abortTransaction();
      throw error; // Triggers BullMQ retry with backoff
    } finally {
      session.endSession();
    }
  },
  {
    connection: { host: process.env.REDIS_HOST, port: Number(process.env.REDIS_PORT) },
    concurrency: 10
  }
);
```

---

Previous : [12_Attribution_Data_Model.md](./12_Attribution_Data_Model.md) | Index: [00_Index.md](../00_Index.md) | Next: [14_Campaign_Attribution.md](./14_Campaign_Attribution.md)
