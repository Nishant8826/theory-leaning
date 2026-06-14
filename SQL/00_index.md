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

---

### 🚀 [01. Introduction & Setup](./01_Introduction_And_Setup.md)
* **Core Idea:** Relational databases require strict schema definition *before* database writing, unlike document-based databases.
* **Connection Pooling:** Always use pools in Node.js instead of single client connections to avoid bottleneck delays under high API load.
* **Node Code Example:**
  ```js
  const mysql = require('mysql2/promise');
  const db = mysql.createPool({
    host: 'localhost', user: 'root', password: 'password', database: 'ecommerce', connectionLimit: 10
  });
  ```
* **MERN Parallel:** Creating a pool in `mysql2` is equivalent to `mongoose.connect()` (which wraps MongoDB's connection pooling mechanism under the hood).

---

### 🗣️ [02. What Is SQL?](./02_What_Is_SQL.md)
* **Core Idea:** SQL is an English-sentence-like language used to communicate with relational engines, divided into operational subcategories.
* **SQL Sublanguages:**
  * **DDL (Data Definition):** `CREATE`, `ALTER`, `DROP`, `TRUNCATE` (schema creation/alteration).
  * **DML (Data Manipulation):** `INSERT`, `UPDATE`, `DELETE` (data modifications).
  * **DQL (Data Query):** `SELECT` (reading data).
  * **TCL (Transaction Control):** `COMMIT`, `ROLLBACK`, `SAVEPOINT` (data transaction groups).
* **MERN Parallel:** SQL statements represent declarative logic (`SELECT * FROM users WHERE age >= 18`), whereas MongoDB relies on JS object-syntax query commands (`db.users.find({ age: { $gte: 18 } })`).

---

### 🏗️ [03. Databases & Tables](./03_Databases_And_Tables.md)
* **Core Idea:** Tables store data in fixed columns with explicit rule enforcement mechanisms called **constraints**.
* **Table Constraints:**
  * `PRIMARY KEY`: Unique, non-null column identifier (automatically indexed).
  * `FOREIGN KEY`: Enforces that a column value must match an identifier in a referenced table.
  * `NOT NULL`, `UNIQUE`, `DEFAULT`, `CHECK` (validates custom conditions like `CHECK (price > 0)`).
* **SQL Syntax Example:**
  ```sql
  CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    status VARCHAR(50) DEFAULT 'active'
  );
  ```

---

### 🗃️ [04. Data Types](./04_Data_Types.md)
* **Core Idea:** Choose exact data storage representations to conserve disk footprint and prevent math calculations errors.
* **Key Types:**
  * **Integers:** `TINYINT` (1 byte), `INT` (4 bytes), `BIGINT` (8 bytes). Use `UNSIGNED` to double positive ranges.
  * **Strings:** `CHAR(N)` (fixed-length), `VARCHAR(N)` (variable-length, saves bytes).
  * **Money:** **Always** use `DECIMAL(precision, scale)` (e.g., `DECIMAL(10,2)`). **Never** use floating-point types (`FLOAT`/`DOUBLE`) because binary representation errors cause rounding discrepancies.
  * **Dates:** `DATETIME` (no timezone translation, 1000–9999 range) vs `TIMESTAMP` (converts UTC to session local timezone, 1970–2038 range).

---

### 🔨 [05. Create, Drop & Alter](./05_Create_Drop_Alter.md)
* **Core Idea:** DDL operations update structures on disk. Be cautious in production: altering tables locks table operations.
* **Core Syntax:**
  ```sql
  ALTER TABLE users ADD COLUMN age INT NOT NULL;
  ALTER TABLE users DROP COLUMN old_col;
  ```
* **DROP vs. TRUNCATE:** `DROP` completely deletes both the data and the table schema from the database. `TRUNCATE` deletes all rows, resets indices (`AUTO_INCREMENT` goes back to 1), runs faster than `DELETE` (deallocates disk sectors directly), and cannot be rolled back.

---

### 📝 [06. Insert, Update & Delete](./06_Insert_Update_Delete.md)
* **Core Idea:** Mutating rows. Always use parameterized inputs to prevent injection attacks.
* **Core Code Examples:**
  ```sql
  INSERT INTO users (name, email) VALUES (?, ?);
  UPDATE users SET email = ? WHERE id = ?;
  DELETE FROM users WHERE id = ?;
  ```
* **Update/Delete Safety:** Failing to write a `WHERE` clause in `UPDATE` or `DELETE` executes the action against **every single row** in the table!
* **MERN Parallel:** Mongoose query results return `modifiedCount`. MySQL returns `affectedRows` (matched target rows) and `changedRows` (rows where values actually altered).

---

### 🔍 [07. SELECT Basics](./07_Select_Basics.md)
* **Core Idea:** Read column projection. Selecting specific columns (`SELECT name, price`) instead of wildcard `SELECT *` reduces bandwidth.
* **Core Syntax:**
  * **Aliases:** `SELECT price * stock AS total_value`
  * **Calculated Values:** `SELECT ROUND(price * 1.18, 2)`
  * **Conditional CASE WHEN:** Inline IF-ELSE logic inside queries:
    ```sql
    SELECT name,
      CASE 
        WHEN stock = 0 THEN 'Out of Stock'
        ELSE 'In Stock'
      END AS availability
    FROM products;
    ```

---

### 🎯 [08. WHERE Clause & Filters](./08_Where_Clause_And_Filters.md)
* **Core Idea:** Row filtering. SQL uses three-valued logical operators (`TRUE`, `FALSE`, and `NULL`).
* **Filtering Syntax:**
  * `AND`, `OR`, `NOT`, `IN` (list match), `BETWEEN a AND b` (inclusive range).
  * `LIKE 'iPhone%'` (prefix match, uses indexes) vs `LIKE '%Phone%'` (infix match, causes slow full-table scans).
  * **NULL Check:** Always use `IS NULL` or `IS NOT NULL`. SQL queries using `= NULL` fail silently because any comparison evaluating against `NULL` results in `NULL` (unknown).

---

### 🔢 [09. Sorting & Limiting](./09_Sorting_And_Limiting.md)
* **Core Idea:** Ordering records and implementing paginated offsets.
* **Sorting:** `ORDER BY price DESC, created_at ASC`
* **Offset Pagination:**
  * Uses `LIMIT limit OFFSET (page - 1) * limit`.
  * **Problem:** Large offsets (e.g. `OFFSET 100000`) force databases to read all previous rows and discard them, slowing query speeds.
* **Cursor Pagination (Keyset):**
  * Uses `WHERE id > last_seen_id ORDER BY id ASC LIMIT 10`.
  * Jumps directly to rows via index, ensuring $O(\log N)$ speed. Cannot jump directly to arbitrary pages.

---

### 📊 [10. Aggregate Functions](./10_Aggregate_Functions.md)
* **Core Idea:** Performing calculations on sets of database rows, collapsing them into single values.
* **Aggregates:** `COUNT(*)`, `SUM(col)`, `AVG(col)`, `MIN(col)`, `MAX(col)`.
* **Important Detail:** Aggregates ignore `NULL` values completely. For instance, `AVG(salary)` computes the average of only rows with actual numbers. `COUNT(*)` counts every row, while `COUNT(column)` ignores `NULL` records.
* **MERN Parallel:** Aggregate functions represent MongoDB’s pipeline operators like `$sum`, `$avg`, and `$count`.

---

### 📂 [11. GROUP BY & HAVING](./11_Group_By_And_Having.md)
* **Core Idea:** Grouping rows sharing attributes together for mathematical aggregations.
* **WHERE vs HAVING:**
  * `WHERE` filters database rows *before* they are grouped or aggregated.
  * `HAVING` filters the computed groups *after* the `GROUP BY` execution.
* **Syntax Example:**
  ```sql
  SELECT category_id, AVG(price) FROM products
  WHERE status = 'published'
  GROUP BY category_id
  HAVING AVG(price) > 500;
  ```

---

### 🤝 [12. Joins](./12_Joins.md)
* **Core Idea:** Relational databases normalize data by distributing it across multiple tables. JOIN queries bring them back together.
* **Join Types:**
  * **INNER JOIN:** Keeps only matching rows from both tables.
  * **LEFT JOIN:** Keeps all rows from the left table, putting `NULL` values in the right columns if no match exists.
  * **RIGHT JOIN:** Opposite of LEFT JOIN.
  * **CROSS JOIN:** Cartesian product (multiplies all rows together).
* **Syntax Example:**
  ```sql
  SELECT p.name, c.name AS category
  FROM products p
  INNER JOIN categories c ON p.category_id = c.id;
  ```

---

### 🪆 [13. Subqueries](./13_Subqueries.md)
* **Core Idea:** A nested query written inside an outer SQL statement.
* **Categories:**
  * **Scalar:** Returns a single value.
  * **Correlated:** Subquery references columns from the outer query, causing it to run once per outer row (slower, e.g. `p1.price > (SELECT AVG(price) FROM products p2 WHERE p2.category_id = p1.category_id)`).
  * **Non-Correlated:** Independent subquery that executes only once.
* **EXISTS vs. IN:** `EXISTS` checks only boolean presence (stops reading the disk as soon as it finds one match), making it faster than `IN` for subqueries on large datasets.

---

### 🖼️ [14. Views](./14_Views.md)
* **Core Idea:** A saved SELECT query that acts as a virtual table. Views contain no physical data on disk.
* **Usage:** Simplifies complex queries (hides long JOINs) and secures sensitive data by exposing only limited columns.
* **Core Syntax:**
  ```sql
  CREATE VIEW product_listings AS
  SELECT p.id, p.name, c.name AS category FROM products p JOIN categories c ON p.category_id = c.id;
  ```
* **Materialized Views:** Physical caches of view query data. MySQL does not support these natively, but you can simulate them by scheduling updates to physical tables.

---

### ⚡ [15. Indexes](./15_Indexes.md)
* **Core Idea:** Indexes are separate B-Tree data structures that make lookup speeds extremely fast ($O(\log N)$) instead of doing slow, linear table scans ($O(N)$).
* **Index Types:**
  * **Clustered:** Physical sorting of data rows on disk. Only one per table (the `PRIMARY KEY`).
  * **Non-Clustered:** Index structures that point back to data rows.
  * **Composite Index:** An index spanning multiple columns (`INDEX(a, b, c)`).
* **Leftmost Prefix Rule:** A composite index `(a, b, c)` only helps queries filtering by column combinations starting from the left: `(a)`, `(a,b)`, or `(a,b,c)`. It cannot optimize queries filtering only by `(b)` or `(c)`.
* **Execution Plan:** Prefix your query with `EXPLAIN` to verify if it uses indexes.

---

### 🔐 [16. Transactions](./16_Transactions.md)
* **Core Idea:** An all-or-nothing container grouping multiple database commands together to preserve integrity.
* **ACID Guarantees:**
  * **A**tomicity: All statements succeed, or everything is rolled back.
  * **C**onsistency: Valid database states are preserved.
  * **I**solation: Prevents concurrent operations from reading unfinished changes.
  * **D**urability: Writes committed changes to disk permanently.
* **Syntax & Concurrency Safety:**
  ```sql
  START TRANSACTION;
  -- FOR UPDATE locks matching rows so concurrent queries wait until commit
  SELECT stock FROM products WHERE id = 1 FOR UPDATE;
  UPDATE products SET stock = stock - 1 WHERE id = 1;
  COMMIT; -- Or ROLLBACK on error
  ```

---

### 📦 [17. Stored Procedures](./17_Stored_Procedures.md)
* **Core Idea:** Reusable, precompiled SQL blocks stored on the database server. Reduces network traffic by executing multiple steps on-db.
* **Syntax Example:**
  ```sql
  CREATE PROCEDURE GetProductStock(IN prod_id INT, OUT stock_count INT)
  BEGIN
    SELECT stock INTO stock_count FROM products WHERE id = prod_id;
  END;
  ```
* **Usage in Node.js:** Execute using `CALL` command: `CALL GetProductStock(?, @stock)`

---

### ⚡ [18. Triggers](./18_Triggers.md)
* **Core Idea:** Automatic database event listeners that execute SQL blocks on `INSERT`, `UPDATE`, or `DELETE`.
* **Key Keywords:** Use `NEW` (contains new row values) and `OLD` (contains previous row values) to inspect mutations.
* **Syntax Example:**
  ```sql
  CREATE TRIGGER log_price_change
  AFTER UPDATE ON products
  FOR EACH ROW
  BEGIN
    IF OLD.price <> NEW.price THEN
      INSERT INTO audit_log (product_id, old_val, new_val) VALUES (NEW.id, OLD.price, NEW.price);
    END IF;
  END;
  ```
* **MERN Parallel:** Equivalent to Mongoose database middleware hooks like `schema.pre('save')` or `schema.post('remove')`.

---

### 📐 [19. Normalization](./19_Normalization.md)
* **Core Idea:** Organizing schemas into distinct tables to eliminate redundant data storage and prevent database anomalies.
* **Anomalies:**
  * **Insert:** Cannot add records without adding unrelated values.
  * **Update:** Must edit duplicate entries in multiple rows.
  * **Delete:** Deleting a row accidentally clears unrelated records.
* **Normal Forms:**
  * **1NF:** Cell values must be atomic (no arrays/JSON lists).
  * **2NF:** 1NF + no partial key dependencies (attributes must depend on the *entire* composite primary key).
  * **3NF:** 2NF + no transitive dependencies (non-key columns must depend *only* on the primary key, not on other non-key columns).

---

### ⚖️ [20. SQL vs. NoSQL](./20_SQL_Vs_NoSQL.md)
* **Core Idea:** Choosing between strict schemas/transactions (SQL) and flexible document schemas (NoSQL).
* **Paradigms:**
  * **SQL (MySQL):** Relational tables, strict schema validation, complex joins, vertical scaling (bigger RAM/CPU), ACID compliance. Best for transactions and complex data structures.
  * **NoSQL (MongoDB):** JSON documents, dynamic schemas, horizontal scaling (sharding across servers), fast read lookups. Best for high-frequency logs and social feeds.
* **CAP Theorem:** You can only guarantee two out of the three: **C**onsistency, **A**vailability, and **P**artition tolerance.

---

### 🛒 [21. Final Project](./21_Final_Project.md)
* **Core Idea:** Structuring a complete normalized production database for an e-commerce API.
* **Real-world Practice:** Incorporates schemas with primary/foreign constraints, lookup views (`product_listing`), index tuning, stored procedures for orders, and ACID checkout transactions with atomic inventory checks.

---

### 🌐 [22. Deployment On EC2](./22_Deployment_On_EC2.md)
* **Core Idea:** Launching full-stack Node.js + MySQL projects to AWS cloud servers.
* **Stack Setup:**
  * **PM2:** Manages the Node.js API process (handles restarts and reboots).
  * **Nginx:** Acts as a reverse proxy, handling SSL certificate termination (Certbot/Let's Encrypt) and compression.
  * **AWS RDS:** Managed database engine ensuring automated backups, safety groups, and scaling.
  * **Backups:** Use `mysqldump` script automated via `cron` jobs:
    ```bash
    mysqldump -u user -pdb_password db_name > backup.sql
    ```
