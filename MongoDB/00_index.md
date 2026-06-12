# MongoDB Study Guide — Index

This index acts as a central hub and navigation control for the MongoDB developer study guide, tailored for SQL experts. Below is the direct navigation to all 22 topics, along with a quick revision summary of the concepts covered in each file.

---

## Table of Contents & Quick Revision

### 1. [01. Introduction & Setup](./01_Introduction_And_Setup.md)
* **Summary:** Overview of MongoDB, installation guide for local/Atlas, core CLI commands (`mongosh`), and setting up Node.js driver/Mongoose.
* **Key Concepts:** BSON storage, document databases, shell commands, and connection pooling settings.

### 2. [02. SQL vs MongoDB — Mental Model](./02_SQL_Vs_MongoDB_Mental_Model.md)
* **Summary:** The core paradigm shift from data-driven normalization to query-driven denormalization.
* **Key Concepts:** Query-driven schema design, data locality (performing fewer disk seeks by embedding), and two questions (read/write frequency) that decide schema structure.

### 3. [03. Databases, Collections & Documents](./03_Databases_Collections_Documents.md)
* **Summary:** Comparison of databases, collections, and documents to SQL databases, tables, and rows.
* **Key Concepts:** Implicit creation of databases/collections, polymorphic document structures, structure of `_id` and ObjectId, and 16MB document size limits.

### 4. [04. BSON & Data Types](./04_BSON_And_Data_Types.md)
* **Summary:** Exploration of Binary JSON (BSON), its rich data types, and differences from plain JSON.
* **Key Concepts:** Exact money precision using `Decimal128`, timestamp vs date, type queries using `$type`, and null vs missing fields.

### 5. [05. CRUD — Create](./05_CRUD_Create.md)
* **Summary:** Methods to insert documents, handling of uniqueness, and bulk writes.
* **Key Concepts:** `insertOne`, `insertMany`, `ordered: false` for independent failures, `upsert` options, and write concerns (`w: "majority"`).

### 6. [06. CRUD — Read](./06_CRUD_Read.md)
* **Summary:** Query filters, projection, sorting, and pagination mechanisms.
* **Key Concepts:** `find`, `findOne`, projection inclusion/exclusion rules, dot notation for nested fields, cursor iteration, and keyset-based pagination.

### 7. [07. CRUD — Update](./07_CRUD_Update.md)
* **Summary:** Field updates, modification of sub-documents/arrays, and atomic updates.
* **Key Concepts:** Update operators (`$set`, `$unset`, `$inc`, `$push`, `$pull`, `$addToSet`), array filtering (`arrayFilters`), and atomic updates using `findOneAndUpdate`.

### 8. [08. CRUD — Delete](./08_CRUD_Delete.md)
* **Summary:** Methods for document deletion, handling of orphaned references, and auto-delete indexes.
* **Key Concepts:** `deleteOne`, `deleteMany`, `drop` vs `deleteMany({})`, manual cascade deletions, soft-delete pattern, and TTL index auto-cleanup.

### 9. [09. Query Operators](./09_Query_Operators.md)
* **Summary:** In-depth guide to comparison, logical, element, and array query operators.
* **Key Concepts:** `$in`, `$or` vs `$in`, `$elemMatch` vs dot notation, regex searches, and field-to-field comparison with `$expr`.

### 10. [10. Projection & Pagination](./10_Projection_And_Pagination.md)
* **Summary:** Customizing returned fields, array slice selection, and high-performance pagination styles.
* **Key Concepts:** `$slice`, `$elemMatch` projection, offset-based vs cursor-based pagination, and covered queries.

### 11. [11. Indexes](./11_Indexes.md)
* **Summary:** Detailed indexing patterns, explain plan analysis, and performance tuning.
* **Key Concepts:** Multikey indexes, compound indexing with ESR rule (Equality, Sort, Range), unique/partial/sparse indexes, text and geospatial indexes, and reading explain plans.

### 12. [12. Aggregation Framework](./12_Aggregation_Framework.md)
* **Summary:** The pipeline-based reporting and data transformation engine of MongoDB.
* **Key Concepts:** Sequential stages (`$match`, `$group`, `$project`, `$sort`, `$limit`, `$unwind`), `$facet` for parallel streams, and the 100MB RAM limit per stage.

### 13. [13. $lookup & Relations](./13_Lookup_And_Relations.md)
* **Summary:** Joins in MongoDB, and modeling relationships.
* **Key Concepts:** `$lookup` syntax, pipeline lookup with let variables, 1:1, 1:N, and N:M relationships, and the performance cost of lookups.

### 14. [14. Embedding vs Referencing](./14_Embedding_Vs_Referencing.md)
* **Summary:** Decision framework for structuring related documents.
* **Key Concepts:** When to embed (data read together, bounded size) vs reference (unbounded array, shared volatile data), and hybrid patterns (cached snapshots).

### 15. [15. Schema Design Strategies](./15_Schema_Design_Strategies.md)
* **Summary:** Key architectural design patterns for production-grade document structures.
* **Key Concepts:** Attribute Pattern, Bucket Pattern (IoT/time-series), Computed Pattern (pre-computed values), Outlier Pattern, Schema Versioning Pattern, and Polymorphic Pattern.

### 16. [16. Transactions](./16_Transactions.md)
* **Summary:** Implementing ACID transactions across multiple documents and collections.
* **Key Concepts:** `session.startTransaction()`, Node.js callback API (`withTransaction`), transactional overhead, retry logic for transient errors, and sharded transaction limits.

### 17. [17. Validation & Schema](./17_Validation_And_Schema.md)
* **Summary:** Enforcing schema rules at the database level and application level.
* **Key Concepts:** Built-in JSON Schema validators (`$jsonSchema`), validation levels (`strict`/`moderate`), Mongoose schema validation, and middleware triggers.

### 18. [18. Mongoose Deep Dive](./18_Mongoose_Deep_Dive.md)
* **Summary:** Detailed guide to Mongoose features, connection settings, and performance helpers.
* **Key Concepts:** Virtual fields, virtual populate, pre/post save and query hooks, static and instance methods, population, and `.lean()` read optimizations.

### 19. [19. Performance Optimization](./19_Performance_Optimization.md)
* **Summary:** Best practices for writing fast database queries and optimizing schema performance.
* **Key Concepts:** Working set sizes, covered query optimization, bulk writes, query projection, secondary read preferences, and connection pool sizing.

### 20. [20. When to Use MongoDB vs SQL](./20_When_To_Use_MongoDB_Vs_SQL.md)
* **Summary:** Decision framework for when to choose MongoDB, SQL, or polyglot persistence.
* **Key Concepts:** Decision matrices, polyglot persistence architecture, total cost of ownership, and common database architectural mistakes.

### 21. [21. Real-World Architecture](./21_Real_World_Architecture.md)
* **Summary:** Production project structures, error handling patterns, auth integration, and WebSocket change streams.
* **Key Concepts:** Service layer pattern, custom ApiError handling, JWT authentication, real-time collection watching via Change Streams, and testing with in-memory Mongo database.

### 22. [22. Deployment & Scaling](./22_Deployment_And_Scaling.md)
* **Summary:** Hosting MongoDB in production, replica sets, sharding, and backups.
* **Key Concepts:** Local EC2 installation, security hardening checklist, PM2 & Nginx reverse proxy, Replica Set failover dynamics, sharding architecture, and TTL/backup policies.
