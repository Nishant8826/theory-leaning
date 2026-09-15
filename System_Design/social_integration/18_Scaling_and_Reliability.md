# 18 — Scaling & Reliability

## 📌 1. Scaling Milestones (10K ──► 1M ──► 100M+ Leads)

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              SYSTEM SCALE EVOLUTION ROADMAP                            │
├────────────────────┬────────────────────────────┬──────────────────────────────────────┤
│ Scale Tier         │ Architecture & Data Layer  │ Bottlenecks & Mitigations            │
├────────────────────┼────────────────────────────┼──────────────────────────────────────┤
│ **Stage 1**        │ Single Express Monolith    │ Node.js event loop blocks on I/O.    │
│ (10K - 100K Leads) │ MongoDB Atlas 3-node RS    │ • Add Redis BullMQ queue buffer.     │
│                    │ Redis single instance      │ • Add compound indexes on tenantId.  │
├────────────────────┼────────────────────────────┼──────────────────────────────────────┤
│ **Stage 2**        │ Modular Services on K8s    │ MongoDB CPU spikes on report aggreg. │
│ (1M - 10M Leads)   │ Dedicated Ingestion Workers│ • Route analytics to Read Replicas.  │
│                    │ Redis Cluster (Sentinel)   │ • Auto-scale workers via KEDA/HPA.   │
├────────────────────┼────────────────────────────┼──────────────────────────────────────┤
│ **Stage 3**        │ Event-Driven Microservices │ Sharding limits & cross-shard joins. │
│ (100M+ Leads)      │ MongoDB Sharded Cluster    │ • Shard by `{ tenantId, _id }`.      │
│                    │ ClickHouse Columnar OLAP   │ • Stream CDC via Kafka to ClickHouse.│
└────────────────────┴────────────────────────────┴──────────────────────────────────────┘
```

---

## ⚡ 2. Resiliency: Circuit Breakers & Backpressure

When downstream third-party APIs (such as the Meta Graph API) degrade or fail, naive systems hang and exhaust connection pools. We integrate the **Circuit Breaker Pattern** (via Opossum):

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              CIRCUIT BREAKER STATE TRANSITIONS                         │
├────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                        │
│          ┌───────────────────────────┐                                                 │
│          │       CLOSED STATE        │ ◄── Normal Operations (Graph API healthy)       │
│          └─────────────┬─────────────┘                                                 │
│                        │                                                               │
│                        ▼ (Failures > 50% over 10s window)                              │
│          ┌───────────────────────────┐                                                 │
│          │        OPEN STATE         │ ◄── Fast-Fail without calling Meta Graph API    │
│          │                           │     Jobs sent directly to BullMQ Delayed Queue  │
│          └─────────────┬─────────────┘                                                 │
│                        │                                                               │
│                        ▼ (After 60s cooldown timer)                                    │
│          ┌───────────────────────────┐                                                 │
│          │      HALF-OPEN STATE      │ ◄── Probe 5 test requests                       │
│          └───────────────────────────┘     ├── All Pass ──► Return to CLOSED           │
│                                            └── Any Fail ──► Return to OPEN             │
│                                                                                        │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🛡️ 3. Failure Scenario & Disaster Recovery Matrix

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                               FAILURE MODES & MITIGATIONS                               │
├───────────────────────┬──────────────────────────────┬──────────────────────────────────┤
│ Failure Scenario      │ Direct System Impact         │ Architectural Recovery Strategy  │
├───────────────────────┼──────────────────────────────┼──────────────────────────────────┤
│ **Meta API Down**     │ Cannot fetch lead details    │ Circuit breaker trips; jobs      │
│ (HTTP 500 / 503)      │ from `leadgen_id`.           │ delayed in BullMQ with backoff.  │
├───────────────────────┼──────────────────────────────┼──────────────────────────────────┤
│ **MongoDB Replica**   │ Primary node re-election for │ Ingestion Gateway buffers in     │
│ **Failover**          │ ~10-15 seconds.              │ Redis without dropping webhooks. │
├───────────────────────┼──────────────────────────────┼──────────────────────────────────┤
│ **OAuth Token**       │ Graph API returns 400 with   │ Worker flags tenant integration  │
│ **Revoked / Expired** │ error code 190.              │ degraded; moves jobs to DLQ.     │
├───────────────────────┼──────────────────────────────┼──────────────────────────────────┤
│ **Viral Ad Webhook**  │ Influx of 10,000 reqs/sec    │ Redis `SETNX` drops duplicates;  │
│ **Storm**             │ hitting edge gateway.        │ K8s HPA scales ingestion workers.│
├───────────────────────┼──────────────────────────────┼──────────────────────────────────┤
│ **Partial CSV Batch** │ 100 invalid emails in a      │ Worker processes line-by-line in │
│ **Failure**           │ 50,000 row CSV upload.       │ transaction; exports error CSV.  │
└───────────────────────┴──────────────────────────────┴──────────────────────────────────┘
```

---

## 📈 4. Kubernetes Autoscaling via KEDA (Queue-Depth Driven)

Instead of scaling workers based on CPU (which is a lagging indicator for I/O-bound workers), we scale worker pods based on **BullMQ Queue Depth**:

```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: lead-ingestion-worker-scaler
spec:
  scaleTargetRef:
    name: lead-ingestion-worker-deployment
  minReplicaCount: 2
  maxReplicaCount: 50
  triggers:
    - type: redis
      metadata:
        address: redis-cluster:6379
        listName: bull:lead-ingestion-queue:wait
        listLength: "50" # Scale out 1 pod per 50 pending leads
```

---

Previous : [17_Webhooks_and_Event_Processing.md](./17_Webhooks_and_Event_Processing.md) | Index: [00_Index.md](../00_Index.md) | Next: [19_Implementation_Guide.md](./19_Implementation_Guide.md)
