# SQL Vs NoSQL

> 📌 **File:** 19_SQL_Vs_NoSQL.md | **Level:** Beginner → MERN Developer

---

## What is it?
The strategic architectural decision between using a Relational SQL database (MySQL, PostgreSQL) versus a Non-Relational NoSQL schema-less document store (MongoDB, DynamoDB).

## MERN Parallel — You Already Know This!
- **MERN = NoSQL** (Agile, unstructured JSON, horizontal scaling)
- **PERN/SERN = SQL** (Strict, atomic relations, vertical scaling)

## Why does it matter?
Picking the wrong database for a system costs millions down the line. A financial banking app cannot use MongoDB (lacks rigid isolated atomicity by default). A rapidly evolving social media IoT data-pipe shouldn't use SQL (too rigid schema limits).

## How does it work?
SQL locks data structures into strict columns yielding 100% data fidelity. NoSQL dumps nested JSON variants into clusters yielding hyper-fast reads.

## Visual Diagram
```ascii
[ MongoDB / NoSQL ]                     [ MySQL / SQL ]
  Schema-less / Flexible                  Strict Schema required
  Scales Horizontally (Add servers)       Scales Vertically (Bigger RAM/CPU server)
  CAP Theorem: Values Partition/Avail.    CAP Theorem: Values Consistency
  Data stored as JSON/BSON Trees          Data stored in Normalized 2D Grids
```

## Syntax
```sql
-- MERN vs SQL — Database Philosophies

-- MongoDB Philosophy: Embed Data for fast fetch
{
  "_id": 1,
  "name": "Jane",
  "orders": [ { "id": 100, "total": 45 }, { "id": 101, "total": 90 } ]
}

-- SQL Philosophy: Maintain separate rigid definitions linked by keys
SELECT * FROM users u JOIN orders o ON u.id = o.user_id;

-- When you update Jane's data in SQL, it's perfect.
-- When you update Jane's data across 15 Mongo documents where she's embedded, it's chaos.
```

### Raw SQL vs ORM
- Not strictly applicable here as code, but philosophically an ORM acts as a translation layer trying to make Relational SQL "feel and behave" identical to NoSQL Mongoose objects.

### Real-World Scenario
**Scenario:** A tech startup must pick their tech stack.

**When to choose MongoDB:**
- Rapid agile prototyping where features change every week.
- You have mountains of unstructured data (Web scraping, Chat logs, IoT telemetry).
- You intend to build purely in Javascript using JSON across the whole stack.

**When to choose MySQL (SQL):**
- You are building e-commerce or financial systems tracking strict money.
- Entities are highly inter-relational (Permissions, Users, Products, Categories, Stock, Logs).
- Data integrity requires zero errors or orphaned records.

## Impact
Migrating from MongoDB to SQL halfway through a startup's life involves massive engineering rewrites of entire codebases, routing logic, and data conversion scripts. Architecture dictates destiny.

## Practice Exercises
- **Easy (Design)**: A system stores temperature strings collected every second from 20 devices. SQL or NoSQL?
- **Medium (Design)**: A hospital tracks patient pharmacy allotments matching FDA standards. SQL or NoSQL?
- **Hard (Design)**: A modern app mixes both! Suggest a polyglot architecture utilizing MongoDB for chat histories and MySQL for payment ledgers.

## Interview Q&A
1. **Core SQL:** What does Horizontal scaling vs Vertical scaling mean?
   *NoSQL Horizontal: Buying 5 cheap laptops to share the data shards. SQL Vertical: Buying 1 massive supercomputer server because relations must exist locally together.*
2. **MERN integration:** If MERN uses Mongo, why are SQL ORMs like Prisma built for Node?
   *Because JS is universally used, and developers demanded the strict safety of Postgres/MySQL seamlessly inside Next.js/Express architectures.*
3. **SQL vs MongoDB:** Which is faster?
   *Fetching a huge JSON nested object from Mongo is faster than performing 8 foreign key JOINS mathematically. Writing exact updates to perfect SQL structures is faster than patching huge JSON trees.*
4. **Scenario-based:** We need to add an `age` property, but only for active users.
   *Mongo allows you to inject `age` instantly without downtime. SQL requires `ALTER TABLE` forcing all inactive rows to inherit `age: NULL` locally.*
5. **Advanced/tricky:** Is NoSQL completely lacking schema?
   *Natively yes, but Mongoose applies application-level schema control on top. Mongoose is basically a strict straightjacket mapped onto flexible MongoDB.*

| Previous: [18_Normalization.md](./18_Normalization.md) | Next: [20_Final_Project.md](./20_Final_Project.md) |
