# SQL Curriculum Index & Complete Revision Guide

> 📌 **File:** `00_index.md` | **Level:** Complete Course Directory & Revision Guide

Welcome to the SQL learning path! This curriculum is tailored specifically for **MERN Stack Developers** transitioning from NoSQL (MongoDB/Mongoose) to Relational Databases (MySQL/Sequelize/mysql2).

---

## 🗺️ Syllabus Directory & Chapter Map

Use this directory to jump directly to any topic or tutorial file.

| File / Link | Level | Key Topics Covered |
| :--- | :--- | :--- |
| 🚀 **[01. Introduction & Setup](./01_Introduction_And_Setup.md)** | Beginner | Installing MySQL & Workbench, setting up Express connection pools with `mysql2`. |
| 🗣️ **[02. What Is SQL?](./02_What_Is_SQL.md)** | Beginner | DDL, DML, DQL sublanguages; SQL syntax vs MQL (MongoDB Query Language). |
| 🏗️ **[03. Databases & Tables](./03_Databases_And_Tables.md)** | Beginner | `CREATE TABLE` syntax, Constraints (Primary Keys, Foreign Keys, Unique, Default). |
| 🗃️ **[04. Data Types](./04_Data_Types.md)** | Beginner | Integer/string sizes, exact `DECIMAL` vs floating `FLOAT`, `DATETIME` vs `TIMESTAMP`. |
| 🔨 **[05. Create, Drop & Alter](./05_Create_Drop_Alter.md)** | Intermediate | Modifying table structures on disk, `ALTER TABLE`, `TRUNCATE` vs `DROP`. |
| 📝 **[06. Insert, Update & Delete](./06_Insert_Update_Delete.md)** | Intermediate | Mutating table rows, `affectedRows` vs `changedRows`, soft deletes, safety precautions. |
| 🔍 **[07. SELECT Basics](./07_Select_Basics.md)** | Intermediate | Column projection, aliases (`AS`), calculated values, inline `CASE WHEN` logic. |
| 🎯 **[08. WHERE Clause & Filters](./08_Where_Clause_And_Filters.md)** | Intermediate | Row filtering, logical operators, `IN`, `BETWEEN`, `LIKE` wildcards, handling `NULL`s. |
| 🔢 **[09. Sorting & Limiting](./09_Sorting_And_Limiting.md)** | Intermediate | Ordering query rows (`ORDER BY`), Offset-based vs Cursor-based Pagination logic. |
| 📊 **[10. Aggregate Functions](./10_Aggregate_Functions.md)** | Intermediate | Data math: `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`, dealing with `NULL` aggregates. |
| 📂 **[11. GROUP BY & HAVING](./11_Group_By_And_Having.md)** | Intermediate | Collapsing rows into category summaries, filtering aggregate results via `HAVING`. |
| 🤝 **[12. Joins](./12_Joins.md)** | Advanced | Combining tables: `INNER`, `LEFT` (preserves unmatched), `RIGHT`, `CROSS` Joins. |
| 🪆 **[13. Subqueries](./13_Subqueries.md)** | Advanced | Nesting queries inside SELECT/WHERE/FROM, `EXISTS` vs `IN`, Correlated queries. |
| 🖼️ **[14. Views](./14_Views.md)** | Advanced | Virtual database tables (`CREATE VIEW`), security abstraction, materialized views. |
| ⚡ **[15. Indexes](./15_Indexes.md)** | Advanced | B-Tree indexing, index types, `EXPLAIN` query analyzer, Leftmost Prefix rule. |
| 🔐 **[16. Transactions](./16_Transactions.md)** | Advanced | ACID compliance, concurrency safety, row locking (`FOR UPDATE`), rollbacks. |
| 📦 **[17. Stored Procedures](./17_Stored_Procedures.md)** | Advanced | Storing and executing compiled SQL blocks on the server (`CREATE PROCEDURE`). |
| ⚡ **[18. Triggers](./18_Triggers.md)** | Advanced | Automating data changes via event hooks (`BEFORE/AFTER INSERT/UPDATE/DELETE`). |
| 📐 **[19. Normalization](./19_Normalization.md)** | Expert | Relational layout standards: 1NF, 2NF, 3NF, BCNF, avoiding database anomalies. |
| ⚖️ **[20. SQL vs. NoSQL](./20_SQL_Vs_NoSQL.md)** | Expert | CAP Theorem, vertical vs horizontal scaling, Polyglot Persistence implementation. |
| 🛒 **[21. Final Project](./21_Final_Project.md)** | Expert | Structuring a complete normalized production database for an e-commerce API. |
| 🌐 **[22. Deployment On EC2](./22_Deployment_On_EC2.md)** | Expert | Setting up PM2, Nginx reverse proxies, SSL/Certbot, AWS RDS, and daily backups. |

---

## 🧠 Comprehensive Study & Revision Notes (All Chapters)

This revision guide is designed for high-density, fast review, focusing on exact SQL syntax, under-the-hood database engine behavior, and NoSQL (MERN) comparisons.

---

### 🚀 [01. Introduction & Setup](./01_Introduction_And_Setup.md)
* **Core Paradigm Shift:** Relational databases require you to plan and declare your tables and columns (strict schema) *before* writing any data. In NoSQL (MongoDB), you write first and let schemas evolve dynamically.
* **Connection Pooling:** In Express/Node.js, never create a single client connection per request (this causes crash bottlenecks). Always create a connection pool, which manages a queue of reusable database connections.
* **Node.js (mysql2/promise) Cheatsheet:**
  ```js
  const mysql = require('mysql2/promise');
  const db = mysql.createPool({
    host: 'localhost',
    user: 'root',
    password: 'password',
    database: 'ecommerce',
    connectionLimit: 10,
    waitForConnections: true,
    queueLimit: 0
  });
  ```
* **Gotcha:** Always release connections back to the pool when using raw transactions, otherwise you cause connection leaks that freeze the application.

---

### 🗣️ [02. What Is SQL?](./02_What_Is_SQL.md)
* **Core Idea:** SQL is an English-sentence-like language used to communicate with relational engines, divided into operational subcategories.
* **Sublanguages:**
  * **DDL (Data Definition):** Controls schemas (`CREATE`, `ALTER`, `DROP`, `TRUNCATE`).
  * **DML (Data Manipulation):** Controls records (`INSERT`, `UPDATE`, `DELETE`).
  * **DQL (Data Query):** Retrieves records (`SELECT`).
  * **TCL (Transaction Control):** Controls transactions (`COMMIT`, `ROLLBACK`, `SAVEPOINT`).
  * **DCL (Data Control):** Controls security (`GRANT`, `REVOKE`).
* **Declarative vs Imperative:** SQL is declarative (you state *what* you want: `SELECT * FROM users WHERE age > 18`). MongoDB Query Language (MQL) is imperative/object-based (you write JSON queries describing *how* to find matching documents: `db.users.find({ age: { $gt: 18 } })`).

---

### 🏗️ [03. Databases & Tables](./03_Databases_And_Tables.md)
* **Key Constraints:**
  * `PRIMARY KEY`: Unique, non-null, and physically orders the table data (only 1 per table).
  * `FOREIGN KEY`: Points to a primary key in another table to guarantee referential integrity.
  * `NOT NULL`, `UNIQUE`, `DEFAULT`, `CHECK` (e.g., `CHECK (price >= 0)`).
* **Referential Integrity Actions (ON DELETE/UPDATE):**
  * `CASCADE`: If parent is deleted/updated, automatically delete/update child rows.
  * `SET NULL`: If parent is deleted, set the child's foreign key column to `NULL`.
  * `RESTRICT` / `NO ACTION`: Blocks you from deleting or updating a parent row (e.g., Category) if it is still being used by any child rows (e.g., Products). (Default behavior).
* **SQL Example:**
  ```sql
  CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category_id INT,
    price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
  );
  ```

---

### 🗃️ [04. Data Types](./04_Data_Types.md)
* **Key Data Types:**

| Category | SQL Type | Storage Size | Best For | Tips & Examples |
| :--- | :--- | :--- | :--- | :--- |
| **Strings** | `CHAR(N)` | Fixed $N$ characters | Fixed-size text | ISO codes (e.g. `'IN'`, `'US'`), statuses. (Faster) |
| | `VARCHAR(N)` | Variable length | Dynamic-size text | Names, emails, passwords. (Saves space) |
| **Integers** | `TINYINT` | 1 byte | Tiny numbers | Age, status flags, boolean `0/1` values. |
| | `INT` | 4 bytes | Standard IDs | General ID columns, counts (-2.14 Billion to 2.14 Billion range). |
| | `BIGINT` | 8 bytes | Large IDs | Transctions, logs, high-scale tables. |
| | `UNSIGNED` | *Modifier* | Positive numbers | Append to double positive range (e.g. `INT UNSIGNED`). |
| **Decimals** | `DECIMAL(P,S)`| Exact numeric | Money & Currency | **Always use for money** (e.g., `DECIMAL(10,2)`). |
| | `FLOAT / DOUBLE`| Approximate numeric| Science & Math | **Never use for money!** (Approximations cause rounding bugs). |
| **Time** | `DATETIME` | 8 bytes | Fixed timestamps | Historical dates, booking dates (1000–9999). Timezone-static. |
| | `TIMESTAMP` | 4 bytes | System times | `created_at`, `updated_at` (1970–2038). Converts automatically to user timezone. |

---

### 🔨 [05. Create, Drop & Alter](./05_Create_Drop_Alter.md)
* **Alter Syntax:**
  ```sql
  ALTER TABLE users ADD COLUMN age INT NOT NULL DEFAULT 18;
  ALTER TABLE users DROP COLUMN phone;
  ALTER TABLE users MODIFY COLUMN name VARCHAR(200) NOT NULL;
  ```
* **DDL Production Alert:** Modifying columns on large tables (using `ALTER TABLE`) locks the table, blocking incoming database updates and freezing your application.
* **DELETE vs. TRUNCATE vs. DROP:**

| Feature | `DELETE` | `TRUNCATE` | `DROP` |
| :--- | :--- | :--- | :--- |
| **What it does** | Deletes specific rows (using `WHERE`). | Deletes all rows (empties the table). | Deletes the **entire table** (data & structure). |
| **Table Structure** | Kept intact. | Kept intact. | **Destroyed** (gone from database). |
| **Reset Auto-Increment?**| ❌ No. | ✅ Yes (resets back to 1). | N/A (table is deleted). |
| **Speed** | 🐢 Slow (deletes row-by-row). | ⚡ Blazing Fast (wipes storage directly). | ⚡ Fast (wipes table files from disk). |
| **Can Undo (Rollback)?** | ✅ Yes (can be rolled back). | ❌ No (cannot be undone). | ❌ No (cannot be undone). |
| **Sublanguage Type** | **DML** (Data Manipulation). | **DDL** (Data Definition). | **DDL** (Data Definition). |

---

### 📝 [06. Insert, Update & Delete](./06_Insert_Update_Delete.md)
* **Parameterized Inputs:** Never concatenate input variables directly into queries (e.g., `'WHERE id = ' + req.body.id`). Always use `?` syntax. This separates code execution from parameter data, neutralizing **SQL Injection** attacks.
* **Safety Rules:** Running an `UPDATE` or `DELETE` query without a `WHERE` clause modifies **every single row** in the table.
* **Advanced Commands:**
  * `INSERT IGNORE`: Inserts row, but silently drops it without throwing an error if a duplicate key constraint is triggered.
  * `INSERT INTO ... ON DUPLICATE KEY UPDATE`: If record exists, updates defined columns; otherwise, inserts new record (equivalent to MongoDB upsert).
* **Affected vs Changed:**
  * `affectedRows` counts matched query rows.
  * `changedRows` counts rows where values were actually altered (e.g. updating stock to the same value results in `changedRows: 0`).

---

### 🔍 [07. SELECT Basics](./07_Select_Basics.md)
* **Projection Efficiency:** Avoid `SELECT *`. Select only required fields (`SELECT name, price`) to minimize RAM consumption, index usage, and network transmission sizes.
* **Inline Conditionals (CASE WHEN):**
  ```sql
  SELECT name, price,
    CASE 
      WHEN price > 50000 THEN 'Premium'
      WHEN price > 10000 THEN 'Standard'
      ELSE 'Budget'
    END AS tier
  FROM products;
  ```
* **Unique Rows:** `SELECT DISTINCT city FROM customers;` retrieves only non-duplicate list items.

---

### 🎯 [08. WHERE Clause & Filters](./08_Where_Clause_And_Filters.md)
* **Three-Valued Logic:** SQL evaluations result in `TRUE`, `FALSE`, or `NULL` (unknown).
* **NULL Comparisons:** Since `NULL` represents missing data, any comparison like `WHERE phone = NULL` evaluates to `NULL` (unknown) and returns 0 results. You **must** use `IS NULL` or `IS NOT NULL`.
* **Pattern Matching:**
  * `LIKE 'a%'`: Matches strings starting with 'a' (can use regular B-Tree indexes).
  * `LIKE '%a%'`: Matches strings containing 'a' (violates index prefixing, forcing slow table scans).
  * `_` matches exactly one character; `%` matches zero or more characters.
* **Operators:** `IN ('Delhi', 'Mumbai')` (list matching) and `BETWEEN 10 AND 50` (inclusive range).

---

### 🔢 [09. Sorting & Limiting](./09_Sorting_And_Limiting.md)
* **Multiple Sorting:** `ORDER BY category_id ASC, price DESC`.
* **Offset-Based Pagination:**
  ```sql
  SELECT * FROM products ORDER BY id LIMIT 10 OFFSET 50000;
  ```
  * **Critical Performance Issue:** MySQL must read through and discard the first 50,000 rows before returning 10. Large offset pagination causes massive disk-read delays.
* **Cursor-Based Pagination (Keyset):**
  ```sql
  SELECT * FROM products WHERE id > last_seen_id ORDER BY id LIMIT 10;
  ```
  * **Why it's faster:** Uses the index on `id` to jump directly to the target block in $O(\log N)$ time, skipping previous records entirely.

---

### 📊 [10. Aggregate Functions](./10_Aggregate_Functions.md)
* **Core Aggregates:** `COUNT()`, `SUM()`, `AVG()`, `MIN()`, `MAX()`.
* **Aggregate NULL Handling:** All aggregate functions (except `COUNT(*)`) ignore `NULL` values. For example, `AVG(bonus)` is calculated as `SUM(bonus) / COUNT(rows_with_non_null_bonus)`.
* **COUNT(*) vs COUNT(column):**
  * `COUNT(*)` counts total rows in the result set (including rows with `NULL`s).
  * `COUNT(phone)` counts only rows where the `phone` value is not `NULL`.
* **MERN Parallel:** Equivalent to MongoDB `$group` operators (`$sum`, `$avg`, etc.).

---

### 📂 [11. GROUP BY & HAVING](./11_Group_By_And_Having.md)
* **WHERE vs HAVING:**
  * `WHERE` filters rows **before** aggregation and grouping occur. It cannot evaluate aggregate functions.
  * `HAVING` filters the computed groups **after** aggregation has occurred.
* **Rule of Thumb:** Use `WHERE` to filter raw data; use `HAVING` to filter aggregated totals.
* **Written Syntax Order (How you type it):**
  `SELECT` → `FROM` → `JOIN` → `WHERE` → `GROUP BY` → `HAVING` → `ORDER BY` → `LIMIT`
* **Logical Execution Order (How MySQL runs it under the hood):**
  1. `FROM` & `JOIN` (Loads the table data)
  2. `WHERE` (Filters raw rows before grouping; cannot use aggregate functions or SELECT aliases)
  3. `GROUP BY` (Groups matching rows together)
  4. `HAVING` (Filters aggregated groups; can use aggregate functions)
  5. `SELECT` (Selects columns and calculates aliases like `AS total`)
  6. `DISTINCT` (Filters duplicate rows)
  7. `ORDER BY` (Sorts final result rows)
  8. `LIMIT` & `OFFSET` (Limits output rows)
* **Example:**
  ```sql
  SELECT category_id, COUNT(*) AS prod_count
  FROM products
  WHERE status = 'published'
  GROUP BY category_id
  HAVING prod_count > 5;
  ```

---

### 🤝 [12. Joins](./12_Joins.md)
* **Core Joins:**
  * **INNER JOIN:** Returns records with matching keys in both tables.
  * **LEFT JOIN:** Returns all records from the left table, and matching records from the right table. If no match, right columns return `NULL`.
  * **RIGHT JOIN:** Returns all records from the right table, and matching records from the left table.
  * **CROSS JOIN:** Returns the Cartesian product (combines every left row with every right row).
* **N+1 Query Problem:** Occurs when an application retrieves a list of parent rows (1 query), then loops through each row to query its child records (N queries). Solved by executing a single `JOIN` query:
  ```sql
  SELECT o.id, o.total, c.name 
  FROM orders o 
  INNER JOIN customers c ON o.customer_id = c.id;
  ```

---

### 🪆 [13. Subqueries](./13_Subqueries.md)
* **Derived Tables Requirement:** Any subquery placed in the `FROM` clause must be given an alias, or SQL throws a syntax error:
  ```sql
  SELECT * FROM (SELECT id, price FROM products) AS sub_table;
  ```
* **Correlated vs Non-Correlated:**
  * **Non-Correlated:** Independent subquery that runs once.
  * **Correlated:** Subquery references the outer query's fields, forcing it to run once for every single row evaluated by the outer query (slow!).
* **EXISTS vs IN:**
  * `IN` evaluates the entire subquery result list first.
  * `EXISTS` is a boolean indicator. It stops searching disk sectors as soon as it finds the first matching record, making it highly efficient.

---

### 🖼️ [14. Views](./14_Views.md)
* **Core Concept:** A View is a **saved SELECT query query blueprint** that you can treat like a normal table. It takes up zero disk space (it stores only the query text, not the actual table rows). When you query a view, MySQL runs the saved query live under the hood to get the freshest data.
* **Benefits:**
  * **Security:** Allows you to hide sensitive columns (e.g. expose a `public_users` view that excludes the `password_hash` column).
  * **Simplicity:** Saves you from writing long, painful multi-table `JOIN` queries repeatedly. You save the query once in a view, then simply call `SELECT * FROM my_view;`.
* **Updatable Views:** A view can only handle updates/inserts if it references a single table, contains no grouping (`GROUP BY`), distinct markers (`DISTINCT`), or aggregate functions.
* **Materialized Views:** Unlike other RDBMS engines, MySQL does not support Materialized Views (physically cached results) natively. They must be simulated via trigger updates or scheduled insert scripts.

---

### ⚡ [15. Indexes](./15_Indexes.md)
* **B-Tree Structure:** Sorts keys in a tree pattern, enabling lookup times of $O(\log N)$ instead of $O(N)$ full table scans.
* **Key Index Types:**
  * **Clustered:** Physically sorts data rows on disk. Only one per table (automatically created on the `PRIMARY KEY`).
  * **Unique:** Enforces that all values in the column are distinct while indexing them (e.g. unique email checks).
  * **Single-Column:** Standard index created on a single field to speed up filters.
  * **Composite (Compound):** Built on multiple columns. Subject to the **Leftmost Prefix Rule** (an index on `(A, B)` only works if your query filters by column `A` or `A AND B`; it does not work for column `B` alone).
  * **Full-Text (`FULLTEXT`):** Designed for fast keyword matching in large text blocks using `MATCH() ... AGAINST()`.
  * **Prefix (Partial):** Indexes only the first $N$ characters of a long string/text column to save memory space.
  * **Spatial:** Indexes geographic coordinate fields (`POINT`, `POLYGON`) using geometry-optimized R-Trees.
* **Verification:** Prefix queries with `EXPLAIN` (e.g. `EXPLAIN SELECT * ...`).
  * Avoid `type = ALL` (full scan) and `key = NULL`.
  * Look for `type = const/eq_ref/ref` indicating index usage.

---

### 🔐 [16. Transactions](./16_Transactions.md)
* **ACID Properties Under-The-Hood:**
  * **Atomicity ("All-or-Nothing"):** A transaction executes as one indivisible unit.
    * *How it works:* Uses the **Undo Log**. Before modifying any row, MySQL logs the reverse action (e.g. logging a `DELETE` for an `INSERT`, or the old value for an `UPDATE`). On rollback, MySQL executes the Undo Log backwards to revert all changes.
  * **Consistency ("Constraint Enforcement"):** The database must move from one valid state to another, strictly enforcing all constraints.
    * *How it works:* Enforced by database engine validation rules (like `NOT NULL`, `UNIQUE`, `FOREIGN KEY`, and check constraints like `CHECK (wallet_balance >= 0)`). If any rule is violated during execution, MySQL instantly aborts the query and rolls back the transaction.
  * **Isolation ("Concurrency Control"):** Concurrent transactions must not interfere with each other's execution.
    * *How it works:* Uses **MVCC (Multi-Version Concurrency Control)** and **Locks**. With MVCC, when Transaction A updates a row, Transaction B can read the original version of that row from the **Undo Log** without waiting (non-blocking reads). Row locks (`FOR UPDATE`) serialize access when transactions explicitly try to edit the same record at the same time.
  * **Durability ("Crash Survival"):** Committed data is guaranteed to survive power outages or server crashes.
    * *How it works:* Uses the **Redo Log** (Write-Ahead Logging). Writing updates directly to random sectors on disk is slow. On `COMMIT`, MySQL writes sequentially to the **Redo Log** on disk (which is fast). If the server crashes, on reboot MySQL replays the Redo Log to apply any committed changes that hadn't yet been flushed to main data tables.
* **Locks:** `SELECT ... FOR UPDATE` locks selected rows, preventing concurrent transactions from editing/reading them until commit.
* **Isolation Levels:** `READ UNCOMMITTED` (allows dirty reads), `READ COMMITTED` (prevents dirty reads, allows non-repeatable reads), `REPEATABLE READ` (default; prevents non-repeatable reads), `SERIALIZABLE` (slowest; full locking).

---

### 📦 [17. Stored Procedures](./17_Stored_Procedures.md)
* **Core Concept:** Code blocks stored on the database server. Helps reduce network latency by running multi-step code on the database itself rather than over the network.
* **Parameter Modes:**
  * `IN`: Input arguments (read-only).
  * `OUT`: Output arguments (return parameters).
  * `INOUT`: Read-write arguments.
* **Stored Procedure vs. View:**
  * **View:** Virtual table, read-only selection, no parameters, can be used in JOIN queries.
  * **Stored Procedure:** Compiled logic block, runs DML modifications, takes parameters, handles loops/variables/transactions, called via `CALL`.

---

### ⚡ [18. Triggers](./18_Triggers.md)
* **Event Listeners:** SQL blocks triggered automatically on `BEFORE` or `AFTER` execution of an `INSERT`, `UPDATE`, or `DELETE` statement.
* **Row Modifiers:** Use `NEW` (inspect/modify values about to be inserted) and `OLD` (retrieve values being updated or deleted).
* **Example:**
  ```sql
  CREATE TRIGGER check_discount BEFORE INSERT ON products
  FOR EACH ROW
  BEGIN
    IF NEW.price > 100000 THEN
      SET NEW.price = NEW.price * 0.90; -- Auto 10% discount
    END IF;
  END;
  ```
* **Gotchas:** Triggers cannot execute transactions (`COMMIT` or `ROLLBACK`) internally, and cannot read/write to the table that triggered them (causes mutating table errors).

---

### 📐 [19. Normalization](./19_Normalization.md)
* **Normal Forms Guide:**
  * **1NF (Atomic):** Cell values must contain only single, scalar values (no arrays, lists, or JSON).
  * **2NF (No Partial Key Dependency):** Must be in 1NF, and all non-key columns must depend on the *entire* primary key (only applies if primary key is composite/multi-column).
  * **3NF (No Transitive Dependency):** Must be in 2NF, and all non-key columns must depend *only* on the primary key, not on other non-key columns. ("No column depends on a column that is not the key").
* **Anomalies:** Redundant databases suffer from **Insert** anomalies (cannot add data), **Update** anomalies (inconsistent edits), and **Delete** anomalies (accidental loss of secondary data).

---

### ⚖️ [20. SQL vs. NoSQL](./20_SQL_Vs_NoSQL.md)
* **Comparison Matrix:**
  * **SQL (MySQL):** Relational tables, strict schemas, supports joins, vertically scalable, guaranteed ACID safety. Best for financial ledgers, transactional ordering, and structured logic.
  * **NoSQL (MongoDB):** Flexible JSON documents, dynamic schemas, horizontal scaling (sharding), fast read access (embedded documents). Best for analytics logs, real-time chats, and catalogs.
* **CAP Theorem:** Any distributed system can guarantee at most two of: **C**onsistency, **A**vailability, and **P**artition Tolerance.
  * MySQL prioritizes **Consistency** (CP).
  * MongoDB prioritizes **Consistency** but shifts depending on write/read concerns.

---

### 🛒 [21. Final Project](./21_Final_Project.md)
* **Relational Schema Design:** Building a normalized e-commerce database structure.
* **Implementation checklist:**
  * Define tables with primary and foreign key constraints.
  * Implement indexing on search columns and foreign keys.
  * Construct views for order search summaries.
  * Build stored procedures wrapping transactions to deduct stock and place orders securely.
  * Enforce audit logging via triggers.

---

### 🌐 [22. Deployment On EC2](./22_Deployment_On_EC2.md)
* **Production Stack Setup:**
  * **Nginx:** Reverse proxy server directing external client requests to internal APIs and enforcing SSL (Certbot).
  * **PM2:** Keeps the Express.js API running in the background and handles crash restarts.
  * **AWS RDS:** Managed relational database hosting that takes care of replica scaling, automatic security patches, and daily backups.
* **Database Backup Script:**
  ```bash
  mysqldump -u root -p ecommerce_db > /backups/backup_$(date +%F).sql
  ```
  * Scheduled to run automatically using system `cron` utility jobs.
