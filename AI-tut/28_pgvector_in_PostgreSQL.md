# 🤖 pgvector in PostgreSQL: SQL Vectors, Cosine Distance, and HNSW Indexing

## 📌 Overview

As a web developer, PostgreSQL is likely already your favorite relational database. 

What if you could turn your existing PostgreSQL database into a **high-performance vector database** with a single command?

With **pgvector**, you can!

`pgvector` is an open-source extension for PostgreSQL that adds native **Vector data types**, mathematical **distance operators** (like Cosine Distance `<=>`), and **HNSW indexing** right inside standard SQL tables. You can join relational user profiles, order histories, and vector embeddings in a single SQL query!

```mermaid
flowchart TD
    subgraph PostgreSQL_Database["PostgreSQL 16+ with pgvector"]
        direction TB
        Table["Table: documents <br> • id: UUID <br> • user_id: UUID (Relational FK) <br> • title: VARCHAR(255) <br> • content: TEXT <br> • embedding: VECTOR(1536) ⭐"]
        Index["Index: HNSW (vector_cosine_ops) <br> Accelerated sub-10ms queries"]
        Table --- Index
    end

    SQLQuery["SQL: SELECT title, content, 1 - (embedding <=> $1) AS similarity <br> FROM documents <br> WHERE user_id = $2 <br> ORDER BY embedding <=> $1 LIMIT 3;"]
    
    SQLQuery --> PostgreSQL_Database
    PostgreSQL_Database --> Result["Returns Top 3 Semantically Relevant Rows!"]

    style PostgreSQL_Database fill:#e1f5fe,stroke:#0288d1,stroke-width:2px
    style Table fill:#fff9c4,stroke:#fbc02d,stroke-width:2px
    style SQLQuery fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    style Result fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
```

---

## 🎯 Why This Matters

1. **Zero New Infrastructure**: No need to pay for or manage a separate vector database like Pinecone. Use your existing PostgreSQL database on Supabase, Neon, AWS RDS, or Docker.
2. **Relational Joins + Vector Search**: Combine standard SQL `JOIN`, `WHERE`, and `GROUP BY` clauses with vector similarity in a single query.
3. **100% ACID Compliance**: Vector updates are wrapped inside database transactions, preventing data corruption.

---

## 🧠 Prerequisites

- [05_Embeddings_and_Vector_Search.md](./05_Embeddings_and_Vector_Search.md): Understanding 1536-dimensional vectors and cosine similarity.
- [27_Vector_Databases_Overview.md](./27_Vector_Databases_Overview.md): Understanding HNSW indexes.
- Basic SQL syntax (`SELECT`, `INSERT`, `ORDER BY`).

---

## 🔍 Deep Dive

### 1. The 3 Distance Operators in pgvector

pgvector introduces 3 custom mathematical SQL operators:

| Operator | Metric | SQL Operator | Best For |
|---|---|---|---|
| **Cosine Distance** | $1 - \text{Cosine Similarity}$ | `<=>` | **Text & language embeddings (Standard in GenAI)** ⭐ |
| **Euclidean (L2) Distance** | $\sqrt{\sum (a_i - b_i)^2}$ | `<->` | Image coordinates, physical spatial distances |
| **Negative Dot Product** | $-(\vec{A} \cdot \vec{B})$ | `<#>` | Normalized unit vectors for maximum math speed |

> [!NOTE]
> Distance is the **opposite of similarity**. 
> - A distance of `0.0` means identical vectors (100% match).
> - To get Cosine Similarity from Cosine Distance: $\text{Similarity} = 1 - (\text{embedding} \Leftrightarrow \text{query\_vector})$.

---

### 2. Creating an HNSW Index in SQL

To make searches blazing fast across millions of rows, create an **HNSW index** with `vector_cosine_ops`:

```sql
-- Enable the extension (run once per database)
CREATE EXTENSION IF NOT EXISTS vector;

-- Create the documents table
CREATE TABLE IF NOT EXISTS knowledge_articles (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    category VARCHAR(50),
    embedding vector(1536) -- Matches OpenAI text-embedding-3-small dimensions!
);

-- Create HNSW Index for ultra-fast Cosine Distance queries
CREATE INDEX ON knowledge_articles 
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);
```

- **`m`** (Default: 16): Maximum number of connections per node in the graph. (Higher = more accurate, more RAM).
- **`ef_construction`** (Default: 64): Size of the dynamic candidate list during index build.

---

### 3. The Power of Hybrid SQL Queries

You can filter by regular SQL columns AND vector distance simultaneously:

```sql
SELECT 
    title, 
    content, 
    1 - (embedding <=> '[0.012, -0.045, ...]'::vector) AS similarity_score
FROM knowledge_articles
WHERE category = 'Billing' AND created_at >= '2026-01-01'
ORDER BY embedding <=> '[0.012, -0.045, ...]'::vector
LIMIT 3;
```

---

## 💡 Simple Example: The Unified Supermarket

- **Without pgvector**: You buy groceries at the supermarket (Postgres), but have to drive 5 miles to a separate electronics store (Pinecone) for batteries, and manually keep two receipts synchronized.
- **With pgvector**: The supermarket adds an electronics aisle! You buy everything in one single cart with a single checkout receipt!

---

## 🏗️ Real-World Example: Multi-Tenant SaaS RAG API

In a multi-tenant Node.js app:
```typescript
const sql = `
  SELECT id, title, content, 1 - (embedding <=> $1::vector) AS score
  FROM internal_documents
  WHERE tenant_id = $2 AND is_archived = false
  ORDER BY embedding <=> $1::vector
  LIMIT 5;
`;
const rows = await db.query(sql, [JSON.stringify(queryVector), userTenantId]);
```
PostgreSQL executes the relational security filter `tenant_id = $2` and the vector distance calculation in a single query execution plan!

---

## ⚠️ Common Mistakes & Pitfalls

1. ❌ **Dimension Mismatch**:
   - *Error*: Defining column as `vector(1536)` but trying to insert a vector of length `768`. PostgreSQL will immediately throw a runtime error.
2. ❌ **Sorting by `DESC` instead of `ASC` for Distance**:
   - *Trap*: `ORDER BY embedding <=> query ASC` puts the closest match (smallest distance) at the top. If you write `DESC`, you retrieve the least relevant documents!

---

## 🔥 Important Points to Remember

- `pgvector` adds native vector search directly into PostgreSQL.
- `<=>` calculates Cosine Distance (0.0 = exact match).
- Similarity score = `1 - (embedding <=> query_vector)`.
- Use HNSW indexes (`USING hnsw (embedding vector_cosine_ops)`) for sub-10ms search.
- Enables unified relational SQL queries with vector search.

---

## 💻 Code / Commands / Configuration

Here is a complete TypeScript script demonstrating how to insert and query vectors in PostgreSQL using `pg` (node-postgres):

```typescript
// pgvector_query_demo.ts
// 1. Run: npm install pg dotenv @types/pg
// 2. Run: npx ts-node pgvector_query_demo.ts

import { Client } from "pg";
import * as dotenv from "dotenv";

dotenv.config();

async function runPgVectorDemo() {
  const client = new Client({
    connectionString: process.env.DATABASE_URL || "postgresql://postgres:postgres@localhost:5432/mydb",
  });

  try {
    await client.connect();
    console.log("🐘 Connected to PostgreSQL!");

    // 1. Enable extension & create table
    await client.query("CREATE EXTENSION IF NOT EXISTS vector;");
    await client.query(`
      CREATE TABLE IF NOT EXISTS demo_kb (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        embedding vector(3) -- 3-dimensional vector for demonstration
      );
    `);

    // 2. Insert sample records with 3D vectors
    await client.query(`
      INSERT INTO demo_kb (title, content, embedding) VALUES
      ('Refund Policy', 'Full refunds within 30 days of purchase.', '[0.95, 0.10, 0.05]'),
      ('Shipping Policy', 'Standard shipping takes 3-5 business days.', '[0.10, 0.90, 0.20]'),
      ('Security Guide', 'Passwords must be at least 16 characters.', '[0.05, 0.15, 0.95]')
      ON CONFLICT DO NOTHING;
    `);

    // 3. Mock Query Vector (looking for refund information)
    const userQueryVector = [0.92, 0.12, 0.08];
    console.log("🔍 Executing Cosine Distance Query for Vector:", userQueryVector);

    // 4. Query using <=> Cosine Distance Operator
    const querySql = `
      SELECT 
        id, 
        title, 
        content,
        1 - (embedding <=> $1::vector) AS similarity_score
      FROM demo_kb
      ORDER BY embedding <=> $1::vector ASC
      LIMIT 2;
    `;

    const res = await client.query(querySql, [JSON.stringify(userQueryVector)]);

    console.log("\n🏆 Query Results Ranked by Cosine Similarity:");
    res.rows.forEach((row, i) => {
      console.log(`\n#${i + 1} Title: ${row.title}`);
      console.log(`Similarity: ${(parseFloat(row.similarity_score) * 100).toFixed(2)}%`);
      console.log(`Content: "${row.content}"`);
    });
  } catch (err) {
    console.error("Postgres Error (Check DATABASE_URL connection):", err);
  } finally {
    await client.end();
  }
}

runPgVectorDemo();
```

---

## 🎤 Interview Perspective

* **Q: How does pgvector's HNSW index differ from its IVFFlat index in terms of performance and operational maintenance?**
  * **Answer**: 
    - **HNSW** builds a hierarchical graph that can be populated incrementally with zero training step, delivers higher recall, and performs faster query search ($O(\log N)$), but requires more memory (RAM) and takes longer to build.
    - **IVFFlat** partitions the vector space into lists/centroids and requires a pre-training step on an existing dataset (`CREATE INDEX ... WITH (lists = 100)`). If vector distribution shifts significantly after bulk inserts, IVFFlat indexes must be re-indexed to maintain recall.
* **Q: How do you format and sanitize vector parameters when executing queries from Node.js with `pg`?**
  * **Answer**: In Node.js, float arrays (e.g. `number[]`) are serialized as a stringified array format `[0.123, 0.456, ...]` and passed as parameterized values `$1::vector` to prevent SQL injection and let PostgreSQL cast the parameter to the native vector type.

---

## 🧩 Connection With Previous Concepts

- **Previous Lesson ([27_Vector_Databases_Overview.md](./27_Vector_Databases_Overview.md))**: Compared vector database providers.
- **Next Lesson ([29_AI_Agent_Blueprints_1.md](./29_AI_Agent_Blueprints_1.md))**: We will start building complete, end-to-end production **Agent Blueprints**—starting with an Autonomous Customer Support Agent!

---

Previous : [27_Vector_Databases_Overview.md](./27_Vector_Databases_Overview.md) | Index: [00_Index.md](./00_Index.md) | Next: [29_AI_Agent_Blueprints_1.md](./29_AI_Agent_Blueprints_1.md)
