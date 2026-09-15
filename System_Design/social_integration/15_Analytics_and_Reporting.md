# 15 — Analytics & Reporting

## 📌 1. Revenue Attribution & The Multi-Touch Problem

In modern enterprise sales, a single buyer interacts with an average of **6 to 10 marketing touchpoints** before signing a contract. Relying strictly on single-touch attribution produces heavily biased business decisions:
* **First-Touch Bias**: Over-credits top-of-funnel social discovery (Instagram, TikTok) while ignoring the sales webinars that closed the deal.
* **Last-Touch Bias**: Over-credits branded Google Search and promotional emails while starving discovery channels of ad budget.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        TOUCHPOINT JOURNEY ATTRIBUTION WEIGHTING                        │
├────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                        │
│   Touchpoint 1          Touchpoint 2         Touchpoint 3          Touchpoint 4        │
│  [Instagram Ad]       [YouTube Explainer]   [LinkedIn Demo Ad]    [Email Newsletter]   │
│   (Discovery)            (Nurturing)          (Consideration)        (Conversion)      │
│        │                      │                    │                      │            │
│        ▼                      ▼                    ▼                      ▼            │
│  First-Touch (100%)          0%                   0%                     0%            │
│  Last-Touch (0%)             0%                   0%                    100%           │
│  Linear (25%)               25%                  25%                     25%           │
│  U-Shaped (40%)             10%                  10%                     40%           │
│  Time-Decay (10%)           15%                  30%                     45%           │
│                                                                                        │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🧮 2. Mathematical Definition of Attribution Models

### 1. Linear Attribution Model
Distributes equal credit across all $N$ registered touchpoints:
$$W_i = \frac{1}{N}$$

### 2. Time-Decay Model (Half-Life Formula)
Gives exponentially higher weighting to touchpoints closest in time to conversion (using a standard 7-day half-life $\lambda$):
$$W_i = 2^{-\frac{\Delta t_i}{\lambda}}$$
Where $\Delta t_i$ is the number of days prior to conversion. The weights are then normalized to sum to $1.0$.

### 3. Position-Based / U-Shaped Model
Assigns 40% credit to First-Touch, 40% to Last-Touch, and splits the remaining 20% evenly among the $N-2$ intermediate nurturing touches:
$$W_{\text{first}} = 0.40, \quad W_{\text{last}} = 0.40, \quad W_{\text{middle}} = \frac{0.20}{N - 2}$$

---

## 📈 3. Full-Funnel Conversion Pipeline

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                 REVENUE PIPELINE FUNNEL                                 │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  [ Total Ingested Leads ]  ──► 10,000 Leads (CPL: $15.00)                               │
│             │                                                                           │
│             ▼ (35% Conversion Rate)                                                     │
│  [ Marketing Qualified (MQL) ] ──► 3,500 MQLs                                           │
│             │                                                                           │
│             ▼ (25% Conversion Rate)                                                     │
│  [ Sales Qualified (SQL) ] ──► 875 SQLs                                                 │
│             │                                                                           │
│             ▼ (20% Conversion Rate)                                                     │
│  [ Active Opportunities / Deals ] ──► 175 Deals ($1.75M Pipeline)                       │
│             │                                                                           │
│             ▼ (40% Win Rate)                                                            │
│  [ Won Customers ] ──► 70 Paying Customers ($700,000 Realized ARR)                     │
│                                                                                         │
│  Key Metric: Blended Customer Acquisition Cost (CAC) = $2,142.85 per Won Customer       │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🏛️ 4. OLTP vs. OLAP Analytics Architecture

Executing complex multi-touch attribution queries across millions of `leadTouchpoints` on an active MongoDB transactional cluster causes CPU spikes and slow UI page loads.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              ANALYTICS TOPOLOGY AT SCALE                               │
├────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                        │
│  [ Application Server / Webhooks ]                                                     │
│                 │                                                                      │
│                 ▼ Write Path (<10ms)                                                   │
│  [ MongoDB Primary (OLTP) ] ──► (Operational CRM: Leads, Owners, Tasks)                │
│                 │                                                                      │
│                 ▼ Change Data Capture (MongoDB Change Streams / Debezium)              │
│  [ Apache Kafka / AWS Kinesis ]                                                        │
│                 │                                                                      │
│                 ▼ Micro-Batch Ingestion                                                │
│  [ ClickHouse / Snowflake (OLAP) ] ──► (Columnar Storage: Touchpoints, Ad Spend, ROI)  │
│                 │                                                                      │
│                 ▼ Sub-Second SQL Aggregations                                          │
│  [ Executive BI Dashboards (Metabase / Cube.js / React Charts) ]                       │
│                                                                                        │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### Scale Recommendation:
* **Stage 1 (Up to 250K Leads)**: Execute aggregations on a dedicated **MongoDB Read-Preference Secondary Replica** (`readPreference=secondaryPreferred`).
* **Stage 2 (1M+ Leads & Multi-Touch Attribution)**: Stream touchpoint events into **ClickHouse** (Columnar OLAP DB). Multi-touch attribution queries over 100M rows execute in under **80ms**.

---

Previous : [14_Campaign_Attribution.md](./14_Campaign_Attribution.md) | Index: [00_Index.md](../00_Index.md) | Next: [16_Security_and_OAuth.md](./16_Security_and_OAuth.md)
