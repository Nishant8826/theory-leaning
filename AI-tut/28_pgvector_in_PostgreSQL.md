# Chapter 28: pgvector in PostgreSQL

**Estimated Reading Time**: 25 minutes  
**Difficulty**: Advanced  
**Prerequisites**: Chapters 1–27.  
**Learning Objectives**:
1. Configure and enable the `pgvector` extension in PostgreSQL.
2. Write SQL table schemas containing vector columns.
3. Construct HNSW indexes on vector columns in SQL.
4. Set up and query `pgvector` programmatically in TypeScript.

---

## Introduction

As a MERN stack developer, you know PostgreSQL. Setting up a dedicated vector database (like Pinecone) introduces operational overhead, new pricing models, and data synchronization challenges.

**pgvector** is an open-source extension for PostgreSQL. It allows you to store vectors in standard Postgres tables and perform vector searches alongside relational SQL queries, keeping your stack simple and ACID-compliant.

In this chapter, we configure a Postgres schema with `pgvector` and write a TypeScript search service.

---

## Theory: Schemas, Operators, and Index configurations

### 1. Vector Column Types
pgvector adds a custom `vector` type. You specify the dimensions when declaring the column:
```sql
CREATE TABLE items (
  id SERIAL PRIMARY KEY,
  embedding vector(1536) -- OpenAI embedding size
);
```

### 2. Operators for Similarity Search
pgvector adds three distance operators to SQL:
* `<=>`: Cosine Distance
* `<->`: Euclidean (L2) Distance
* `<#>`: Negative Inner Product
* To calculate similarity from distance: `1 - (embedding <=> query_vector)`

### 3. HNSW Index Configuration in SQL
To index vector columns, we use the HNSW access method:
```sql
CREATE INDEX ON items 
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);
```
* `m`: Maximum connections per node in the graph.
* `ef_construction`: Size of the dynamic candidate list evaluated during index construction.

---

## Real-World Analogy: Storing Image Metadata

Imagine managing a catalog of paintings:
* **Relational data**: Storing the painter's name, the date painted, and the price.
* **Vector data**: Storing a 3D color histogram vector representing the dominant colors.
* **Traditional Approach**: You store metadata in SQL, and color vectors in a separate database. To find "paintings by Picasso that are mostly blue", you query both databases and merge the results.
* **pgvector Approach**: You store everything in a single Postgres table. You find PICASSO paintings that are blue using a single SQL query.

---

## Architecture Diagram: Unified SQL Query Execution

This diagram shows how Postgres optimizes metadata filtering and HNSW vector searches within a single query plan.

```mermaid
graph TD
    SQL[Query: SELECT * FROM items WHERE category = 'A' ORDER BY embedding <=> vec LIMIT 5] --> Plan[Query Optimizer]
    Plan -->|B-Tree index| Filter[Filter: category = 'A']
    Plan -->|HNSW index| Sort[Sort by Cosine Distance]
    Filter & Sort --> Merge[Combined Results]
```

---

## Code Example: pgvector Integration (TypeScript)

Let's write a TypeScript script that connects to a PostgreSQL database, enables the `vector` extension, creates a table, inserts mock embeddings, and queries them.

First, install the client package:
```bash
npm install pg dotenv
npm install --save-dev @types/pg
```

Create `pgvector_integration.ts`:

```typescript
import { Client } from "pg";
import dotenv from "dotenv";

dotenv.config();

const client = new Client({
  connectionString: process.env.DATABASE_URL || "postgresql://postgres:postgres@localhost:5432/postgres"
});

// Converts a TS number array into pgvector syntax: '[0.1,0.2,0.3]'
function toPgVector(arr: number[]): string {
  return `[${arr.join(",")}]`;
}

async function runPgVectorDemo() {
  await client.connect();
  console.log("Connected to PostgreSQL database.");

  try {
    // 1. Enable extension
    await client.query("CREATE EXTENSION IF NOT EXISTS vector;");
    console.log("pgvector extension active.");

    await client.query("DROP TABLE IF EXISTS search_index;");

    // 2. Create Table
    await client.query(`
      CREATE TABLE search_index (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        category TEXT NOT NULL,
        embedding vector(3)
      );
    `);

    // 3. Create HNSW Index
    await client.query(`
      CREATE INDEX ON search_index 
      USING hnsw (embedding vector_cosine_ops)
      WITH (m = 16, ef_construction = 64);
    `);
    console.log("HNSW index successfully built.");

    // 4. Insert Mock Data
    const items = [
      { title: "React State Management", category: "frontend", vec: [0.95, 0.05, 0.01] },
      { title: "PostgreSQL Database Joins", category: "backend", vec: [0.02, 0.99, 0.05] },
      { title: "Docker Network Port Mappings", category: "devops", vec: [0.05, 0.90, 0.20] }
    ];

    for (const item of items) {
      await client.query(
        "INSERT INTO search_index (title, category, embedding) VALUES ($1, $2, $3);",
        [item.title, item.category, toPgVector(item.vec)]
      );
    }
    console.log("Inserted mock items.");

    // 5. Query using Cosine Distance (<=> operator)
    const queryVector = [0.92, 0.08, 0.02];
    console.log(`\nQuerying for closest vector to: [${queryVector.join(",")}]...`);

    const result = await client.query(`
      SELECT title, category,
             (1 - (embedding <=> $1)) as similarity
      FROM search_index
      ORDER BY embedding <=> $1
      LIMIT 2;
    `, [toPgVector(queryVector)]);

    console.log("\nResults (Ordered by Cosine Similarity):");
    result.rows.forEach((row, idx) => {
      console.log(`${idx + 1}. Title: "${row.title}" | Similarity: ${parseFloat(row.similarity).toFixed(4)}`);
    });

  } catch (error: any) {
    console.error("Database operation failed:", error.message);
  } finally {
    await client.end();
    console.log("Connection closed.");
  }
}

// Run
runPgVectorDemo();
```

Run this file:
```bash
npx tsx pgvector_integration.ts
```

---

## Best Practices, Production & Security Considerations

### 1. Prevent SQL Injection in Vector Inputs
Never write raw strings like `ORDER BY embedding <=> '[${array}]'`.
* **Production Rule**: Always pass vector strings as parameterized arguments (`$1`) to SQL queries, as shown in the code example.

---

## Common Mistakes

1. **Mismatching dimensions**: Attempting to insert a 4D vector into a column defined as `vector(3)`. Postgres will reject the write and throw a type error.

---

## Exercises & Mini Project

### Exercise 1: L2 Operator query
Modify the SQL query in the code example to use Euclidean distance (`<->` operator) and update the calculations to sort by distance ascending.

### Mini Project: Document Search API
Build an Express API with `POST /api/docs` (inserts text and generates embedding using OpenAI) and `POST /api/search` (accepts a search query, generates embedding, and queries pgvector).

---

## Interview Questions

1. **Q**: Why is `pgvector` preferred over standalone vector databases for early-stage applications?
   * **A**: It allows you to store metadata and embeddings in the same database, ensures ACID compliance, and simplifies queries by allowing relational joins (`JOIN` tables) and vector search in a single SQL statement.
2. **Q**: What pgvector SQL operator is used to run Cosine Distance searches?
   * **A**: The `<=>` operator computes cosine distance. Similarity is computed as `1 - (embedding <=> query_vector)`.

---

## Navigation

**Prev:** [Chapter 27: Vector Databases Overview](file:///d:/learning/theory/AI-tut/27_Vector_Databases_Overview.md) | **Index:** [Course Overview](file:///d:/learning/theory/AI-tut/README.md) | **Next:** [Chapter 29: AI Agent Blueprints 1](file:///d:/learning/theory/AI-tut/29_AI_Agent_Blueprints_1.md)
