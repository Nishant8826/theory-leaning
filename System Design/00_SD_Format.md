# 📐 System Design Document — Standard Format & Prompt Template

> **Purpose:** Use this template/prompt to generate any system design document in a consistent,
> beginner-friendly, interview-ready format.

---

## 🧑‍🏫 How to Use This Template

Copy the prompt below and replace `[SYSTEM NAME]` and `[EXAMPLE: Like XYZ]` with the system you
want to design. Feed it to an AI or follow it manually to produce a complete document.

---

## ✅ THE PROMPT

```
You are a Senior System Design Architect and Mentor.

Create a complete beginner-friendly system design for a "[SYSTEM NAME]" ([EXAMPLE: Like XYZ]).

Your explanation must be simple, structured, and easy to understand for beginners. Avoid jargon where possible and explain everything clearly using:

👉 What (what it is)
👉 Why (why it is needed)
👉 How (how it works)
👉 Impact (what happens if we do/do not use it)

Follow this exact sequence:

========================
1. REQUIREMENTS
========================
- Functional Requirements (FR)
- Non-Functional Requirements (NFR)
Explain each with real-world examples.

========================
2. SCALE & CONSTRAINTS
========================
- Start from 0 users → scale to 500 million users
- Estimate:
  - Traffic (RPS)
  - Storage
  - Peak vs normal load

========================
3. BUDGET & COSTING
========================
- Cost considerations for:
  - Startup (low budget)
  - Mid scale
  - Large scale (500M users)
- Include cloud cost thinking (not exact pricing, but reasoning)

========================
4. HIGH LEVEL DESIGN (HLD)
========================
Explain architecture using:
- Services (e.g., User Service, Core Service, etc.)

Tech Stack:
- Frontend: Next.js (for SEO, SSR, SSG)
- Backend: Node.js + Express
- Database: MySQL (for ACID/relational) + MongoDB (for flexible/catalog data) — Polyglot Persistence
- Cache: Redis
- Cloud components: CDN, Load Balancer, API Gateway

👉 Also explain:
- Why Next.js is used (SEO, SSR benefits)
- Difference between SSR, SSG, CSR in this system
- Which Database for Which Service? (Polyglot Persistence table)
  - MySQL = ACID, relational, financial, transactional data
  - MongoDB = flexible schema, catalog, content, nested docs

👉 Provide:
1. Service-level architecture diagram (ASCII diagram)
2. Step-by-step flow (primary user action flow)

========================
5. LOW LEVEL DESIGN (LLD)
========================
- Database design:
  - MySQL tables (with CREATE TABLE SQL, indexes, foreign keys)
  - MongoDB collections (with example JSON documents)
- APIs (basic endpoints with method, path, description)
- Core algorithm (the key concurrency/logic problem of the system)

👉 Include:
1. Component-level diagram (ASCII)
2. Key algorithms with step-by-step explanation

========================
6. SCALABILITY DESIGN
========================
Explain:
- Horizontal scaling
- Caching (Redis)
- CDN usage with Next.js
- Database scaling:
  - MySQL: Replication + Partitioning
  - MongoDB: Sharding + Replica Sets
- Scaling comparison table (0 → 500M users)

========================
7. RELIABILITY & FAULT TOLERANCE
========================
- What happens if:
  - A critical service fails
  - A server crashes
- Retry & fallback strategies
- Idempotency where needed
- Circuit breaker pattern

========================
8. FLEXIBILITY & EXTENSIBILITY
========================
- How to add new features:
  - Notifications (async, event-driven)
  - Multi-language (i18n)
  - SEO improvements using Next.js
  - Other domain-specific extensions

========================
9. DEV-FRIENDLY PRACTICES
========================
- Project structure (Next.js + Node.js)
- CI/CD pipeline (ASCII diagram)
- Logging & monitoring (structured logs, Prometheus, Grafana)

========================
10. FINAL NOTES (BEGINNER FRIENDLY)
========================
- Summary table (section → key lesson)
- Key takeaways (numbered list)
- Common mistakes beginners make (table: mistake → why wrong → correct approach)

========================
11. SCENARIO-BASED Q&A
========================
Provide 7+ interview-style questions with detailed answers:
- Cover concurrency, scaling, failure, SEO, extensibility
- Each answer should include the reasoning, not just a one-liner

========================

OUTPUT FORMAT RULES:
- Write everything in Markdown format
- All diagrams must be ASCII (no images)
- Use tables where possible for comparison
- Every section must have:
  - 🧠 "Think of it like this" analogy header
  - Clear What / Why / How structure
  - Real-world examples
- Keep explanations simple and beginner-friendly
- Use analogies and emojis to make it engaging
- Header format:
  # 🎯 System Design: [System Name] (Like [Real World App])
  > **Level:** Beginner-Friendly | **Format:** What → Why → How → Impact
  > **Stack:** Next.js + Node.js + MySQL + MongoDB (Polyglot) + Redis + CDN
```

---
