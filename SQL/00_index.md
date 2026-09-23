# SQL Curriculum Index & Complete Revision Guide

> 📌 **File:** `00_index.md` | **Level:** Complete Course Directory & Revision Guide

Welcome to the SQL learning path! This curriculum is tailored specifically for **MERN Stack Developers** transitioning from NoSQL (MongoDB/Mongoose) to Relational Databases (MySQL/Sequelize/mysql2).

---

## 🗺️ Syllabus Directory & Chapter Map

Use this directory to jump directly to any topic or tutorial file.

| File / Link | Level | Key Topics Covered |
| :--- | :--- | :--- |
| 🚀 **[01. Introduction & Setup](./01_Introduction_And_Setup.md)** | Beginner | MySQL architecture, InnoDB Buffer Pool, Express connection pools with `mysql2`. |
| 🗣️ **[02. What Is SQL?](./02_What_Is_SQL.md)** | Beginner | 6-stage query execution pipeline, DDL/DML/DQL/DCL/TCL sublanguages, MQL vs SQL. |
| 🏗️ **[03. Databases & Tables](./03_Databases_And_Tables.md)** | Beginner | Primary Key strategies (Auto-Increment vs UUIDv7 B+Tree clustering), Foreign Keys & Cascades. |
| 🗃️ **[04. Data Types](./04_Data_Types.md)** | Beginner | Exact `DECIMAL` vs IEEE 754 `FLOAT`, `VARCHAR` vs off-page `TEXT`, `JSON` virtual columns, Collations. |
| 🔨 **[05. Create, Drop & Alter](./05_Create_Drop_Alter.md)** | Intermediate | Online DDL algorithms (`INSTANT`, `INPLACE`, `COPY`), Metadata Locks (MDL), `gh-ost` migrations. |
| 📝 **[06. Insert, Update & Delete](./06_Insert_Update_Delete.md)** | Intermediate | Bulk insert tuning, `ON DUPLICATE KEY UPDATE` vs `REPLACE INTO`, soft deletes & unique indexes. |
| 🔍 **[07. SELECT Basics](./07_Select_Basics.md)** | Intermediate | 8-step SQL logical query processing order, alias scope, `DISTINCT` memory overhead, `CASE WHEN`. |
| 🎯 **[08. WHERE Clause & Filters](./08_Where_Clause_And_Filters.md)** | Intermediate | Three-Valued Logic (3VL), SARGability rules (preventing index-killing queries), pattern matching. |
| 🔢 **[09. Sorting & Limiting](./09_Sorting_And_Limiting.md)** | Intermediate | Filesort mechanics vs Index sorting, multi-column Keyset (Cursor) pagination with tuples. |
| 📊 **[10. Aggregate Functions](./10_Aggregate_Functions.md)** | Intermediate | InnoDB `COUNT(*)` MVCC mechanics, `GROUP_CONCAT` buffer sizing, empty-set aggregation rules. |
| 📂 **[11. GROUP BY & HAVING](./11_Group_By_And_Having.md)** | Intermediate | `ONLY_FULL_GROUP_BY` SQL mode, `WITH ROLLUP` multidimensional subtotals, Hash vs Streaming grouping. |
| 🤝 **[12. Joins](./12_Joins.md)** | Advanced | Physical join algorithms (Index Nested Loop, Hash Join in MySQL 8), driving table optimization, `ON` vs `WHERE`. |
| 🪆 **[13. Subqueries](./13_Subqueries.md)** | Advanced | Semi-join transformations (Materialization, FirstMatch), the dangerous `NOT IN` with `NULL`s trap, `EXISTS`. |
| 🖼️ **[14. Views](./14_Views.md)** | Advanced | View algorithms (`MERGE` vs `TEMPTABLE`), `WITH CHECK OPTION`, security definers, materialized views. |
| ⚡ **[15. Indexes](./15_Indexes.md)** | Advanced | B+Tree 16KB page fan-out math, Covering Indexes, Index Condition Pushdown (ICP), `EXPLAIN` hierarchy. |
| 🔐 **[16. Transactions](./16_Transactions.md)** | Advanced | Deep ACID mechanics (Undo/Redo/WAL), concurrency anomalies, InnoDB locks (Record/Gap/Next-Key), deadlocks. |
| 📦 **[17. Stored Procedures](./17_Stored_Procedures.md)** | Advanced | Procedures vs UDFs, `SQLEXCEPTION` handlers, cursors, dynamic SQL (`PREPARE`/`EXECUTE`). |
| ⚡ **[18. Triggers](./18_Triggers.md)** | Advanced | Execution order (`PRECEDES`/`FOLLOWS`), mutating table limits, Triggers vs Transactional Outbox / CDC. |
| 📐 **[19. Normalization](./19_Normalization.md)** | Expert | Functional dependencies ($X \rightarrow Y$), 1NF to 3NF, Boyce-Codd (BCNF), strategic denormalization. |
| ⚖️ **[20. SQL vs. NoSQL](./20_SQL_Vs_NoSQL.md)** | Expert | CAP Theorem vs PACELC Theorem, ACID vs BASE models, enterprise Polyglot Persistence design. |
| 🛒 **[21. Final Project](./21_Final_Project.md)** | Expert | Complete normalized production database schema and Express API for an e-commerce platform. |
| 🌐 **[22. Deployment On EC2](./22_Deployment_On_EC2.md)** | Expert | Production PM2, Nginx reverse proxy, SSL/Certbot, AWS RDS Multi-AZ, Read Replicas, PITR backups. |
| 🔀 **[23. Database Sharding & Partitioning](./23_Sharding_And_Partitioning.md)** | Expert | Range/List/Hash/Subpartitioning, partition pruning in `EXPLAIN`, consistent hashing, 2PC vs Saga pattern. |
| 🪵 **[24. CTEs & Recursive Queries](./24_CTEs_And_Recursive_Queries.md)** | Advanced | Multi-CTE chaining, recursive CTE tree traversal (org charts, breadcrumbs, BOM), cycle detection. |
| 🪟 **[25. Window Functions](./25_Window_Functions.md)** | Advanced | `OVER()` anatomy, ranking (`ROW_NUMBER`, `RANK`, `DENSE_RANK`), `LAG`/`LEAD`, sliding window frames, Top-N. |

---

## 🧠 Comprehensive Study & Revision Notes (All Chapters)

This revision guide is designed for high-density, fast review, focusing on exact SQL syntax, under-the-hood database engine behavior, and NoSQL (MERN) comparisons.

---

### 🚀 [01. Introduction & Setup](./01_Introduction_And_Setup.md)
* **Core Paradigm Shift:** Relational databases require strict schema planning before insertion. MongoDB allows schema-less dynamic JSON.
* **Server Architecture:** 3 Layers: (1) Connection/Thread Manager, (2) SQL Core (Parser $\rightarrow$ Preprocessor $\rightarrow$ Cost-Based Optimizer $\rightarrow$ Executor), (3) Pluggable Storage Engine (InnoDB).
* **InnoDB Buffer Pool:** Dedicated RAM cache (`innodb_buffer_pool_size`) holding table data & index pages. Sized to $70\%-80\%$ of total server memory in production.
* **Connection Pooling:** In Express, use `mysql2.createPool()`. Optimal pool size: $(\text{CPU Cores} \times 2) + \text{Disk Spindles}$.

---

### 🗣️ [02. What Is SQL?](./02_What_Is_SQL.md)
* **Sublanguages:**
  * **DDL:** `CREATE`, `ALTER`, `DROP`, `TRUNCATE`.
  * **DML:** `INSERT`, `UPDATE`, `DELETE`.
  * **DQL:** `SELECT`.
  * **DCL:** `GRANT`, `REVOKE` (User security & permissions).
  * **TCL:** `COMMIT`, `ROLLBACK`, `SAVEPOINT`.
* **6-Stage Execution Pipeline:** Query $\rightarrow$ Parser (AST) $\rightarrow$ Preprocessor (Catalog/Perms) $\rightarrow$ Rewriter $\rightarrow$ Cost-Based Optimizer (CBO evaluates I/O + CPU cost) $\rightarrow$ Executor $\rightarrow$ InnoDB Storage Engine.

---

### 🏗️ [03. Databases & Tables](./03_Databases_And_Tables.md)
* **Primary Key Strategies:**
  * `BIGINT AUTO_INCREMENT`: Sequential, compact (8 bytes), prevents B+Tree page splits, but reveals business volume.
  * `UUIDv4` (Random): Causes massive B+Tree page splits and cache thrashing due to random disk writes.
  * `UUIDv7` (Ordered): 128-bit timestamp-prefixed UUID. Ideal for globally unique, distributed, sequential clustering.
* **Referential Integrity Actions (`ON DELETE / ON UPDATE`):**
  * `RESTRICT` / `NO ACTION`: Blocks parent modification if child rows exist (Default).
  * `CASCADE`: Deletes/updates child rows automatically.
  * `SET NULL`: Sets child foreign key to `NULL`.

---

### 🗃️ [04. Data Types](./04_Data_Types.md)
* **Money & Math:** Always use `DECIMAL(P, S)`. Never use `FLOAT`/`DOUBLE` for currency because binary floating-point (IEEE 754) introduces rounding bugs (`0.1 + 0.2 = 0.30000000000000004`).
* **Strings & Off-Page Storage:** `CHAR` is fixed-size; `VARCHAR` uses 1-2 length bytes. Large `TEXT`/`BLOB` columns are pushed to **Overflow Pages**, causing extra disk seeks.
* **JSON & Virtual Columns:** Index JSON fields using Generated Virtual Columns (`attributes->>'$.brand'`).
* **Charsets & Collations:** Always use `utf8mb4` with `utf8mb4_0900_ai_ci` (case/accent insensitive) or `utf8mb4_bin` (exact binary match).

---

### 🔨 [05. Create, Drop & Alter](./05_Create_Drop_Alter.md)
* **Online DDL (MySQL 8.0):**
  * `ALGORITHM = INSTANT`: Metadata-only modification in 0ms (no table rebuild).
  * `ALGORITHM = INPLACE`: Rebuilds storage file while allowing concurrent reads/writes.
  * `ALGORITHM = COPY`: Legacy; locks table and copies all rows to temp table.
* **Metadata Lock (MDL) Trap:** A long-running `SELECT` blocks an `ALTER TABLE`, which queues and blocks all subsequent incoming API queries, crashing the server. Use `gh-ost` or `pt-online-schema-change` for zero-downtime migrations.
* **DELETE vs TRUNCATE vs DROP:** `DELETE` is DML (row-by-row, rollbackable); `TRUNCATE` is DDL (resets auto-increment, wipes data pages instantly, non-rollbackable); `DROP` deletes structure + data permanently.

---

### 📝 [06. Insert, Update & Delete](./06_Insert_Update_Delete.md)
* **Bulk Inserts:** Batch multi-row inserts (`INSERT INTO ... VALUES (), (), ()`) in chunks of $500-1000$ to avoid round-trip latency and Redo log flushing overhead.
* **Multi-Table DML:** Perform correlated `UPDATE t1 JOIN t2 ON ... SET ...` and `DELETE t1 FROM t1 JOIN t2 ON ...` in a single atomic SQL statement.
* **Production Batch Deletions:** Never execute unbounded `DELETE FROM logs WHERE created_at < NOW()`; run chunked loops (`DELETE ... LIMIT 5000; SELECT SLEEP(0.05);`) to prevent long transaction lock escalation and replication lag.
* **UPSERT:** Use `INSERT ... ON DUPLICATE KEY UPDATE` (in-place modification). Avoid `REPLACE INTO` (executes `DELETE` + `INSERT`, which breaks auto-increment IDs, triggers, and foreign keys).
* **Soft Deletes:** Add `deleted_at TIMESTAMP NULL`. Fix duplicate key bugs on deleted accounts using a virtual generated column: `active_email = IF(deleted_at IS NULL, email, NULL)`.
* **Optimistic Concurrency:** Use a `version` integer column (`WHERE id = ? AND version = ?`) to prevent lost updates without locking rows.

---

### 🔍 [07. SELECT Basics](./07_Select_Basics.md)
* **8-Step Logical Execution Order:**
  `FROM & JOIN` (1) $\rightarrow$ `WHERE` (2) $\rightarrow$ `GROUP BY` (3) $\rightarrow$ `HAVING` (4) $\rightarrow$ `SELECT` (5) $\rightarrow$ `DISTINCT` (6) $\rightarrow$ `ORDER BY` (7) $\rightarrow$ `LIMIT/OFFSET` (8).
* **Alias Scope:** Aliases created in `SELECT` cannot be evaluated in `WHERE` because `WHERE` runs first.
* **DISTINCT Overhead:** Generates temporary sorting tables in memory/disk (`Using temporary; Using filesort`).

---

### 🎯 [08. Where Clause & Filters](./08_Where_Clause_And_Filters.md)
* **Three-Valued Logic (3VL):** Boolean outcomes evaluate to `TRUE`, `FALSE`, or `UNKNOWN` (represented by `NULL`). Comparisons like `WHERE col = NULL` evaluate to `UNKNOWN` and return 0 rows. Use `IS NULL`.
* **SARGability (Search Argument Able):**
  * ❌ *Non-SARGable:* `WHERE YEAR(created_at) = 2024` or `WHERE string_col = 123` (forces full table scan).
  * ✔️ *SARGable:* `WHERE created_at >= '2024-01-01' AND created_at < '2025-01-01'`.
* **Collation Mismatch Index-Killers:** Comparing columns or literals across differing collations (`utf8mb4_general_ci` vs `utf8mb4_unicode_ci`) causes hidden coercion functions that completely disable B+Tree index lookups.
* **Non-Deterministic Short-Circuiting:** SQL optimizer does not guarantee left-to-right evaluation order; use `NULLIF()` or `CASE WHEN` to safely prevent division-by-zero errors.
* **Boolean Full-Text Search:** Inverted index querying with operators (`+`, `-`, `*`, `""`, `~`, `><`).

---

### 🔢 [09. Sorting & Limiting](./09_Sorting_And_Limiting.md)
* **Filesort Mechanics:** If no matching index exists, MySQL allocates `sort_buffer_size` in RAM and runs QuickSort/MergeSort. If buffer overflows, it spills temporary files to disk.
* **The `ORDER BY RAND() LIMIT 1` Trap:** Full table scan + generating random floats for every row + full filesort ($O(N \log N)$). Replace with $O(1)$ indexed mathematical random primary key seek (`WHERE id >= FLOOR(RAND() * @max_id)`).
* **Offset vs Keyset (Cursor) Pagination:**
  * `LIMIT 10 OFFSET 50000`: Scans and discards 50,000 rows (slow $O(N)$).
  * `WHERE (created_at, id) < (?, ?) ORDER BY created_at DESC, id DESC LIMIT 10`: Jumps directly to B+Tree leaf page in $O(\log N)$ with zero drift.

---

### 📊 [10. Aggregate Functions](./10_Aggregate_Functions.md)
* **InnoDB `COUNT(*)`:** Cannot use static metadata row counts due to MVCC (every transaction sees a different snapshot of visible rows). It must scan the smallest secondary index tree.
* **`GROUP_CONCAT`:** Concatenates values into strings. Increase `group_concat_max_len` to avoid default 1024-byte truncation.
* **Empty Set Handling:** `COUNT` on empty set returns `0`; `SUM`, `AVG`, `MIN`, `MAX` return `NULL` (defend with `COALESCE(SUM(...), 0)`).

---

### 📂 [11. GROUP BY & HAVING](./11_Group_By_And_Having.md)
* **`ONLY_FULL_GROUP_BY`:** Every non-aggregated column in `SELECT` must be declared in `GROUP BY` to guarantee deterministic output. Use `ANY_VALUE()` if an arbitrary value is acceptable.
* **`WITH ROLLUP`:** Computes multi-level subtotals and grand totals in a single database pass. Use `GROUPING()` to identify summary rows.
* **Grouping Engines:** Index Streaming Aggregation (fast index traversal) vs Hash Aggregation (in-memory temp table).

---

### 🤝 [12. Joins](./12_Joins.md)
* **Physical Join Algorithms:**
  * **Index Nested Loop (INLJ):** Loops outer rows against inner B+Tree index ($O(M \log N)$).
  * **Batched Key Access (BKA) + MRR:** Buffers outer keys and sorts by clustered disk address for 10x faster sequential page reads.
  * **Hash Join (MySQL 8.0.18+):** In-memory hash table on smaller table probed by larger table ($O(M + N)$); gracefully spills hash partitions to disk chunks when exceeding `join_buffer_size`.
* **Join Elimination:** Optimizer automatically drops unused `LEFT JOIN`s on unique key tables from the execution plan.
* **Dimensional Modeling:** Star Schema (flat de-normalized dimensions for fast OLAP) vs Snowflake Schema (normalized sub-dimensions).
* **`ON` vs `WHERE` in `LEFT JOIN`:** Placing right-table filter conditions in `WHERE` silently converts `LEFT JOIN` into an `INNER JOIN`. Keep right-table filters in the `ON` clause.

---

### 🪆 [13. Subqueries](./13_Subqueries.md)
* **Modern `LATERAL` Derived Tables (MySQL 8.0.14+):** Enables correlated subqueries in the `FROM` clause for high-performance Top-N per user/category calculations.
* **Semi-Join Transformations:** MySQL un-nests `WHERE id IN (SELECT ...)` into FirstMatch, Materialization, or LooseScan.
* **The `NOT IN` with `NULL` Trap:** If the subquery contains a single `NULL`, `NOT IN` evaluates to `UNKNOWN` for all rows and returns an empty set. Always use **`NOT EXISTS`** instead.

---

### 🖼️ [14. Views](./14_Views.md)
* **View Algorithms:**
  * `ALGORITHM = MERGE`: Inlines view SQL into outer query, pushing filters down to base table indexes.
  * `ALGORITHM = TEMPTABLE`: Materializes view into a temporary table (used for `GROUP BY`, `DISTINCT`, `UNION`).
* **`WITH CHECK OPTION`:** Rejects updates/inserts that would cause a row to disappear from the view.
* **Security:** `SQL SECURITY DEFINER` (creator permissions) vs `INVOKER` (caller permissions).

---

### ⚡ [15. Indexes](./15_Indexes.md)
* **B+Tree Fan-Out Math:** A 16KB page with 14-byte pointers has a fan-out of $\approx 1,170$. A 3-level tree indexes over **136 million rows** in just **3 page reads**.
* **Index Selectivity Math ($S = \text{Cardinality} / N$):** If an index matches $>20-30\%$ of table rows, the CBO intentionally skips the index and chooses a fast sequential table scan.
* **Composite Index Range Termination Rule:** Multi-column index `(A, B, C)` cannot use column `C` for index filtering if column `B` uses a range operator (`>`, `<`, `BETWEEN`, `LIKE 'x%'`).
* **Covering Index (`Using index`):** Secondary index containing all requested columns, eliminating the slow secondary Clustered Index bookmark lookup.
* **Loose Index Scan (`Using index for group-by`):** Jumps directly across B+Tree sub-branches to evaluate `DISTINCT` / `GROUP BY` without scanning matching rows.
* **Index Condition Pushdown (ICP):** Evaluates `WHERE` predicates at the storage engine index layer before reading table rows.
* **`EXPLAIN ANALYZE`:** Shows real execution runtime, row counts, iteration loops, and Volcano iterator steps.

---

### 🔐 [16. Transactions](./16_Transactions.md)
* **Transaction Types & Architectures:**
  * **Explicit vs Implicit:** `START TRANSACTION` / `COMMIT` vs `@@autocommit = 1`.
  * **Read-Only Optimization (`START TRANSACTION READ ONLY`):** Skips allocating `DB_TRX_ID` and Undo Log memory to drastically reduce CPU contention on read replicas.
  * **Chained Transactions (`COMMIT AND CHAIN`):** Commits and immediately starts a new transaction with 0ms roundtrip.
  * **Savepoints:** Partial rollback to checkpoints (`SAVEPOINT`, `ROLLBACK TO SAVEPOINT`).
  * **Distributed / XA Transactions:** Two-Phase Commit (2PC) coordinated via `XA START`, `XA PREPARE`, `XA COMMIT`.
  * **Compensating Transactions (Sagas):** Forward/compensating APIs in distributed microservices.
* **The Silent Implicit Commit Trap:** DDL (`ALTER TABLE`, `CREATE TABLE`, `TRUNCATE`) and security statements auto-commit active transactions, permanently preventing `ROLLBACK`.
* **InnoDB Lock Hierarchy:** Shared (`S`), Exclusive (`X`), Intention Locks (`IS`/`IX` for $O(1)$ table conflict checks), Record Locks, Gap Locks, Next-Key Locks, and AUTO-INC locks.
* **InnoDB MVCC Hidden Columns:** Every clustered record contains `DB_TRX_ID` (last modifying transaction ID), `DB_ROLL_PTR` (7-byte pointer to Undo Log historical versions), and `DB_ROW_ID`.
* **Read View Structure:** `[trx_ids: min_trx_id, max_trx_id]` snapshot visibility rules.
* **Snapshot Read vs Current Locking Read:** Plain `SELECT` reads historical undo views; `SELECT ... FOR UPDATE`, `UPDATE`, and `DELETE` perform locking reads on the newest physical data.
* **ACID Mechanics:** Undo Log (Atomicity + MVCC snapshots), Redo Log + WAL (Durability & fast sequential crash recovery), Lock Manager (Isolation).
* **Isolation Levels & Anomalies:** `READ UNCOMMITTED` (Dirty Reads), `READ COMMITTED` (Non-Repeatable Reads), `REPEATABLE READ` (Next-Key Locking prevents Phantoms), `SERIALIZABLE`.
* **Write Skew Anomaly:** Two concurrent transactions read overlapping state and perform non-overlapping writes (prevented by `SELECT ... FOR UPDATE` or Serializable).
* **Two-Phase Locking (2PL):** Growing phase (acquire locks) $\rightarrow$ Shrinking phase (release locks at `COMMIT`/`ROLLBACK`).

---

### 📦 [17. Stored Procedures](./17_Stored_Procedures.md)
* **Procedures vs UDFs:** Functions return a single scalar and run inside `SELECT`. Procedures are called via `CALL`, manage transactions, and accept `IN`/`OUT`/`INOUT` parameters.
* **Error Handling:** `DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK; RESIGNAL; END;`.
* **Dynamic SQL:** `PREPARE stmt FROM @sql; EXECUTE stmt USING @param; DEALLOCATE PREPARE stmt;`.

---

### ⚡ [18. Triggers](./18_Triggers.md)
* **Execution Ordering:** Control order of multiple triggers using `PRECEDES` or `FOLLOWS`.
* **Limitations:** Triggers cannot start/commit transactions or mutate the invoking table.
* **Microservices Architecture:** Prefer the **Transactional Outbox Pattern** and **Change Data Capture (CDC / Debezium)** over heavy database triggers.

---

### 📐 [19. Normalization](./19_Normalization.md)
* **Functional Dependencies & Armstrong's Axioms:** Reflexivity, Augmentation, Transitivity, Union, Decomposition, Pseudotransitivity.
* **Normal Forms:**
  * **1NF:** Atomic scalar values (no arrays/JSON in cells).
  * **2NF:** 1NF + no partial functional dependencies on composite keys.
  * **3NF:** 2NF + no transitive dependencies ($A \rightarrow B \rightarrow C$).
  * **BCNF:** Stricter 3NF where every determinant $X$ in $X \rightarrow Y$ must be a Super Key.
* **Lossless Join vs Dependency Preservation:** 3NF always preserves dependencies; BCNF guarantees zero redundancy and lossless join but may split functional dependencies across tables.
* **Strategic Denormalization:** Used on read-heavy reporting columns (e.g. `order_total`), guarded by Redis caching or atomic triggers.

---

### ⚖️ [20. SQL vs. NoSQL](./20_SQL_Vs_NoSQL.md)
* **CAP vs PACELC Theorem:** If Partition ($P$), choose Availability ($A$) vs Consistency ($C$); Else ($E$), choose Latency ($L$) vs Consistency ($C$).
* **ACID vs BASE:** SQL enforces ACID; NoSQL uses BASE (Basically Available, Soft State, Eventual Consistency).
* **Polyglot Persistence:** MySQL (Financial ledger/Orders) + MongoDB (Dynamic Catalogs) + Redis (Sessions/Cache) + Elasticsearch (Search).

---

### 🛒 [21. Final Project](./21_Final_Project.md)
* **Production E-Commerce Schema:** Normalized schema covering Users, Roles, Categories, Products, Inventory, Orders, Order_Items, Payments, and Audit Logs.
* **Full-Stack Implementation:** Express API with `mysql2/promise`, row-level locking (`FOR UPDATE`), transactions, views, and error handling.

---

### 🌐 [22. Deployment On EC2](./22_Deployment_On_EC2.md)
* **Production Stack:** Ubuntu 22.04 LTS, Nginx reverse proxy, SSL/Certbot, PM2 process management cluster mode.
* **AWS RDS Database Architecture:** Multi-AZ high availability failover, Read Replicas for read scaling, VPC Security Groups, Parameter Groups, and automated Point-In-Time Recovery (PITR).

---

### 🔀 [23. Database Sharding & Partitioning](./23_Sharding_And_Partitioning.md)
* **Partitioning (Local Scaling):** Range, List, Hash, and Composite subpartitioning inside one server.
* **Partition Pruning:** The optimizer reads only the target partition file and skips all others (`EXPLAIN PARTITIONS`).
* **Sharding (Distributed Scaling):** Horizontal splitting across independent database servers.
* **Routing & Hashing:** Consistent Hashing Ring, Application-level routers, or Middleware proxies (Vitess / Citus).
* **Distributed IDs & Transactions:** UUIDv7, Twitter Snowflake IDs, Two-Phase Commit (2PC), and Saga Pattern.

---

### 🪵 [24. CTEs & Recursive Queries](./24_CTEs_And_Recursive_Queries.md)
* **Non-Recursive CTEs:** Modular top-down query chaining using `WITH cte1 AS (...), cte2 AS (...)` (optimizer inlines AST by default).
* **Recursive CTEs:** Traverses hierarchical trees and graphs in a single query:
  * **Anchor Member:** Base case query (e.g. Root categories `parent_id IS NULL`).
  * `UNION ALL`
  * **Recursive Member:** Joins the CTE back to the base table to fetch next depth level.
* **Hierarchical Modeling Tradeoffs:** Adjacency List (CTEs) vs Materialized Path vs Closure Table vs Nested Sets.
* **Graph Routing & Cycle Detection:** Shortest path traversal with path tracking strings and `cte_max_recursion_depth`.

---

### 🪟 [25. Window Functions](./25_Window_Functions.md)
* **Core Concept:** Computes aggregations across a partition of rows **without collapsing rows** (unlike `GROUP BY`).
* **Ranking:** `ROW_NUMBER()` (unique sequential), `RANK()` (ties with skips: 1, 2, 2, 4), `DENSE_RANK()` (ties without skips: 1, 2, 2, 3), `NTILE(n)`.
* **Navigation:** `LAG(col, 1)` (previous row) and `LEAD(col, 1)` (next row) for Month-over-Month (MoM) growth analytics.
* **Sliding Window Frames:** `ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING` (Moving averages), `RANGE` vs `ROWS` duplicate evaluation, and the `LAST_VALUE()` default frame trap.
* **Advanced Patterns:**
  * **Top-N per Group:** Using `DENSE_RANK()` in a CTE with `WHERE rank <= N`.
  * **Gaps & Islands Analysis:** Grouping consecutive login streaks using `(event_date - ROW_NUMBER() DAYS)` difference groupings.

---

