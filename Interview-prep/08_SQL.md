# 🚀 Interview Preparation - SQL

> **Domain:** Database Engineering / Backend Development  
> **Level:** Beginner to Expert  
> **Target Role:** Software Engineer / Senior Engineer / Database Engineer

---

## 🟢 Beginner Level

### ❓ Q1. **What is SQL and how does it differ from NoSQL databases?**

<details>
<summary><b>👀 Show Answer</b></summary>

* **SQL (Relational):** 
  - Uses structured, tabular schemas (rows and columns).
  - Enforces strict data integrity constraints via schemas and foreign keys.
  - Horizontally scales with difficulty; typically scales vertically (adding CPU/RAM).
  - Standardized querying language (SQL).
  - Examples: MySQL, PostgreSQL, SQLite, MS SQL Server.
* **NoSQL (Non-Relational):**
  - Document, key-value, wide-column, or graph formats.
  - Schema-less/dynamic schema.
  - Horizontally scales easily via sharding and clustering.
  - Query languages vary by system (e.g., MongoDB Query Language).
  - Examples: MongoDB, Redis, Cassandra, Neo4j.

> 💡 **Interviewer Focus:** Ensure candidate mentions schema stiffness vs flexibility, ACID compliance strengths in SQL, and vertical vs horizontal scaling constraints.

</details>

<hr/>

### ❓ Q2. **What are the different categories of SQL commands?**

<details>
<summary><b>👀 Show Answer</b></summary>

SQL commands are grouped into five main categories:
1. **DDL (Data Definition Language):** Defines database structure/schema.
   - Examples: `CREATE`, `ALTER`, `DROP`, `TRUNCATE`.
2. **DML (Data Manipulation Language):** Manipulates data within tables.
   - Examples: `INSERT`, `UPDATE`, `DELETE`, `SELECT` (sometimes grouped as DQL).
3. **DCL (Data Control Language):** Manages permissions and access controls.
   - Examples: `GRANT`, `REVOKE`.
4. **TCL (Transaction Control Language):** Manages database transactions.
   - Examples: `COMMIT`, `ROLLBACK`, `SAVEPOINT`.
5. **DQL (Data Query Language):** Specifically used for retrieving data.
   - Example: `SELECT`.

> 💡 **Interviewer Focus:** Watch for correct grouping of commands (e.g., `TRUNCATE` is DDL, not DML).

</details>

<hr/>

### ❓ Q3. **What is the difference between a Primary Key and a Foreign Key?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Primary Key:** 
  - Uniquely identifies each record in a table.
  - Cannot contain `NULL` values.
  - Only one primary key per table.
  - Automatically creates a clustered index.
- **Foreign Key:**
  - A field in one table that references the Primary Key of another table.
  - Helps enforce **Referential Integrity**.
  - Can contain `NULL` values (unless specified `NOT NULL`).
  - A table can have multiple foreign keys.

> 💡 **Interviewer Focus:** Referential integrity concept, cascading deletion effects, and indexing foreign keys.

</details>

<hr/>

### ❓ Q4. **What is the difference between CHAR and VARCHAR data types?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **`CHAR`:** 
  - Fixed-length string.
  - If the stored string is shorter than the defined length, it is right-padded with spaces to match the length.
  - Slightly faster because memory allocation is static.
  - Best for fields with uniform length (e.g., UUIDs, country codes like `US`, `IN`).
- **`VARCHAR`:**
  - Variable-length string.
  - Stores only the characters provided plus 1-2 bytes of length prefix metadata.
  - Saves disk space for variable inputs.
  - Slightly slower due to dynamic memory calculation.
  - Best for user inputs (e.g., names, emails).

> 💡 **Interviewer Focus:** Trade-off between storage efficiency (VARCHAR) and processing performance (CHAR).

</details>

<hr/>

### ❓ Q5. **What is a NULL value in SQL and how is it handled in comparisons?**

<details>
<summary><b>👀 Show Answer</b></summary>

A `NULL` value represents **unknown or missing data**.
- It is **not** equal to zero, an empty string, or another `NULL`.
- Any comparison with `NULL` using standard operators (`=`, `!=`, `<`, `>`) results in `UNKNOWN` (Three-valued logic).
- To check for nullability, you must use the `IS NULL` or `IS NOT NULL` operators.

```sql
-- ❌ Wrong comparison (returns empty set)
SELECT * FROM users WHERE middle_name = NULL;

--  Correct comparison
SELECT * FROM users WHERE middle_name IS NULL;
```

> 💡 **Interviewer Focus:** Understanding three-valued logic (`TRUE`, `FALSE`, `UNKNOWN`) and using functions like `COALESCE()` or `IFNULL()`.

</details>

<hr/>

### ❓ Q6. **What is the difference between WHERE and HAVING clauses?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **`WHERE`:** 
  - Filters rows **before** groups are formed and aggregate functions are calculated.
  - Cannot contain aggregate functions (like `SUM()`, `AVG()`, `COUNT()`).
  - Used on standard columns.
- **`HAVING`:**
  - Filters groups **after** the `GROUP BY` clause is applied.
  - Typically used with aggregate functions to filter summary results.

```sql
SELECT department_id, COUNT(*) 
FROM employees 
WHERE salary > 50000 -- Row filter
GROUP BY department_id 
HAVING COUNT(*) > 5; -- Aggregate group filter
```

> 💡 **Interviewer Focus:** SQL Query Execution Order (WHERE runs before GROUP BY, HAVING runs after).

</details>

<hr/>

### ❓ Q7. **What is the purpose of the GROUP BY clause?**

<details>
<summary><b>👀 Show Answer</b></summary>

The `GROUP BY` clause groups rows that have the same values in specified columns into summary rows (e.g., finding the total sales per region). It is used alongside aggregate functions like `COUNT()`, `MAX()`, `MIN()`, `SUM()`, and `AVG()`.

> 💡 **Interviewer Focus:** Point out that columns in the `SELECT` list that are not inside aggregate functions must be declared in the `GROUP BY` clause.

</details>

<hr/>

### ❓ Q8. **Explain the differences between DELETE, TRUNCATE, and DROP.**

<details>
<summary><b>👀 Show Answer</b></summary>

| Feature | `DELETE` | `TRUNCATE` | `DROP` |
| :--- | :--- | :--- | :--- |
| **Type** | DML (Data Manipulation) | DDL (Data Definition) | DDL (Data Definition) |
| **Speed** | Slow (logs row-by-row deletes) | Fast (deallocates data pages) | Immediate |
| **WHERE Clause**| Supported | Not Supported | Not Supported |
| **Rollback** | Possible (if in transaction) | Database specific | Not possible (usually) |
| **Identity Reset**| No | Yes (resets auto-increment) | N/A (deletes table) |
| **Locks** | Row-level locks | Table-level lock | Table-level lock |

> 💡 **Interviewer Focus:** Structural vs data actions, transactional safety, and transaction log impacts.

</details>

<hr/>

### ❓ Q9. **What are constraints in SQL? Name the common ones.**

<details>
<summary><b>👀 Show Answer</b></summary>

Constraints are rules applied to columns to limit the type of data that can be stored, ensuring data reliability and integrity.
- `NOT NULL`: Prevents storing `NULL` values.
- `UNIQUE`: Guarantees all values in a column are distinct.
- `PRIMARY KEY`: Combines `NOT NULL` and `UNIQUE`.
- `FOREIGN KEY`: References primary keys in other tables.
- `CHECK`: Ensures values satisfy a specific condition (e.g., `age >= 18`).
- `DEFAULT`: Provides a default value if none is specified.

> 💡 **Interviewer Focus:** How check constraints can implement basic business logic at the database layer.

</details>

<hr/>

### ❓ Q10. **What is the purpose of the IN and BETWEEN operators?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **`IN`**: Allows specifying multiple values in a `WHERE` clause, acting as shorthand for multiple `OR` statements.
- **`BETWEEN`**: Filters values within a inclusive range (numbers, text, or dates).

> 💡 **Interviewer Focus:** Knowing that `BETWEEN` is inclusive of boundary values.

</details>

<hr/>

### ❓ Q11. **Explain the difference between SQL Server, MySQL, and PostgreSQL syntax variations.**

<details>
<summary><b>👀 Show Answer</b></summary>

- **MySQL:** Optimized for web development. Uses backticks (`` ` ``) to quote identifiers, handles pagination via `LIMIT offset, limit` or `LIMIT count OFFSET offset`, and has custom string concatenation methods (`CONCAT`).
- **PostgreSQL:** Closely matches standard ANSI SQL. Uses double quotes (`"`) for identifiers, supports the string concatenation operator (`||`), has built-in array/JSONB columns, and supports recursive queries with standard syntax.
- **SQL Server (T-SQL):** Uses square brackets (`[]`) or double quotes for identifiers, implements pagination using `TOP` or `OFFSET FETCH` clauses, supports the `+` operator for string concatenation, and uses `CROSS APPLY` for table-valued functions.

```sql
-- MySQL pagination
SELECT * FROM users LIMIT 10 OFFSET 20;

-- SQL Server pagination
SELECT TOP 10 * FROM users; -- (Or OFFSET 20 ROWS FETCH NEXT 10 ROWS ONLY)
```

> 💡 **Interviewer Focus:** Awareness of syntax differences when writing cross-platform SQL queries or migrations.

</details>

<hr/>

### ❓ Q12. **How does the LIKE operator work, and what are wildcards?**

<details>
<summary><b>👀 Show Answer</b></summary>

The `LIKE` operator is used in a `WHERE` clause to search for a specified pattern in a column.
- **`%`**: Represents zero, one, or multiple characters.
- **`_`**: Represents a single character.

```sql
SELECT * FROM products WHERE name LIKE 'A%';   -- Starts with "A"
SELECT * FROM products WHERE name LIKE '_b%';  -- Has "b" in the second position
SELECT * FROM products WHERE name LIKE '%cat%';-- Contains "cat" anywhere
```

> 💡 **Interviewer Focus:** Point out that trailing wildcards (`LIKE 'A%'`) can utilize indexes (sargable), whereas leading wildcards (`LIKE '%A'`) prevent index seeks and force full table scans.

</details>

<hr/>

### ❓ Q13. **What is the difference between NULL and an empty string?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **`NULL`:** Represents the absence of a value or an unknown value. It occupies no space in terms of value storage (often marked by a bit in a NULL bitmap).
- **Empty String (`''`):** A value that exists and is known but contains no characters. It has a length of `0` and consumes memory for string metadata.
- *Note: In Oracle Database, an empty string is treated exactly as `NULL`.*

> 💡 **Interviewer Focus:** Checking nullability (`IS NULL`) vs checking empty values (`= ''`).

</details>

<hr/>

### ❓ Q14. **What does the AS keyword do in a SQL query?**

<details>
<summary><b>👀 Show Answer</b></summary>

The `AS` keyword is used to temporarily rename a column or a table with an **alias** for the duration of the query. It improves readability and is useful when joining tables or when columns are named via aggregates.

```sql
SELECT first_name AS fname, last_name AS lname 
FROM employees AS emp;
```

> 💡 **Interviewer Focus:** Essential when referencing subquery outputs or joining self-referential tables.

</details>

<hr/>

### ❓ Q15. **What is the default sorting order of the ORDER BY clause?**

<details>
<summary><b>👀 Show Answer</b></summary>

The default sorting order of `ORDER BY` is **ascending (`ASC`)**. To sort in descending order, you must explicitly append the `DESC` keyword.

> 💡 **Interviewer Focus:** Knowing how `NULL` values sort by default in different systems (e.g., PostgreSQL places `NULL`s last for `ASC`, while MySQL places them first). Explain using `NULLS FIRST` / `NULLS LAST` to control this explicitly.

</details>

<hr/>

### ❓ Q16. **How do you select distinct values from a table?**

<details>
<summary><b>👀 Show Answer</b></summary>

Use the `DISTINCT` keyword immediately after `SELECT` to eliminate duplicate rows from the query output.

```sql
SELECT DISTINCT country FROM customers;
```

> 💡 **Interviewer Focus:** Point out that `DISTINCT` operates on the *entire* tuple in the `SELECT` list, not just the first column, and forces a sorting or hashing step that has performance overhead.

</details>

<hr/>

### ❓ Q17. **What is the purpose of the LIMIT / TOP / ROWNUM clauses?**

<details>
<summary><b>👀 Show Answer</b></summary>

These clauses restrict the number of rows returned by a query, which is essential for pagination:
- **`LIMIT`** (PostgreSQL, MySQL, SQLite): `SELECT * FROM users LIMIT 10;`
- **`TOP`** (SQL Server): `SELECT TOP 10 * FROM users;`
- **`ROWNUM`** (Oracle): `SELECT * FROM users WHERE ROWNUM <= 10;`

> 💡 **Interviewer Focus:** Implementing consistent offset pagination and why keyset pagination is preferred for large datasets.

</details>

<hr/>

### ❓ Q18. **What is a database schema?**

<details>
<summary><b>👀 Show Answer</b></summary>

A database schema is the skeleton structure that represents the logical configuration of the entire database. It defines the tables, columns, constraints, relationships, indexes, views, and procedures. In some systems (like PostgreSQL), a schema acts as a namespace within a database.

> 💡 **Interviewer Focus:** Logical schema configuration vs physical database storage on disk.

</details>

<hr/>

### ❓ Q19. **What is the difference between a table and a view?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Table:** A physical database object that stores data values directly on disk.
- **View:** A virtual table defined by a SQL query. It does not store physical data; instead, it executes its query definition on the fly whenever referenced.

> 💡 **Interviewer Focus:** Security advantages of views (exposing a subset of columns to users without sharing access to the underlying table).

</details>

<hr/>

### ❓ Q20. **How do you insert multiple rows in a single INSERT statement?**

<details>
<summary><b>👀 Show Answer</b></summary>

You specify multiple value sets separated by commas within a single `INSERT` statement:

```sql
INSERT INTO users (name, email) VALUES 
('Alice', 'alice@test.com'),
('Bob', 'bob@test.com'),
('Charlie', 'charlie@test.com');
```

> 💡 **Interviewer Focus:** Performance benefits of batch inserts (fewer database roundtrips and transaction flushes) compared to executing individual insert loops.

</details>

<hr/>

### ❓ Q21. **What is referential integrity?**

<details>
<summary><b>👀 Show Answer</b></summary>

Referential integrity is a database state where all foreign key values are valid, meaning every foreign key matches an existing primary key in the referenced parent table. It prevents orphaned rows and keeps relationships consistent.

> 💡 **Interviewer Focus:** Enforcing integrity via foreign key constraints and cascade actions (`ON DELETE RESTRICT`, `ON DELETE CASCADE`).

</details>

<hr/>

### ❓ Q22. **What does the check constraint `CHECK (salary > 0)` do?**

<details>
<summary><b>👀 Show Answer</b></summary>

It prevents any insert or update operation from writing a row where the `salary` column is less than or equal to `0`. If violated, the database throws a constraint violation error and rolls back the operation.

> 💡 **Interviewer Focus:** Validating basic domain rules at the database level for consistency.

</details>

<hr/>

### ❓ Q23. **What is a composite primary key?**

<details>
<summary><b>👀 Show Answer</b></summary>

A primary key consisting of two or more columns. It guarantees that the *combination* of values across these columns is unique for every row, even if individual columns contain duplicates.

```sql
CREATE TABLE order_items (
  order_id INT,
  item_id INT,
  quantity INT,
  PRIMARY KEY (order_id, item_id)
);
```

> 💡 **Interviewer Focus:** When to use composite keys (e.g., junction tables resolving many-to-many relationships) vs auto-incrementing IDs.

</details>

<hr/>

### ❓ Q24. **How do you select records containing a specific pattern in the middle of a string?**

<details>
<summary><b>👀 Show Answer</b></summary>

Use the `LIKE` operator with the wildcard character `%` placed at both the beginning and the end of the search pattern.

```sql
SELECT * FROM users WHERE email LIKE '%@gmail%';
```

> 💡 **Interviewer Focus:** Understand that this query cannot perform an index seek and forces a full table scan; discuss using full-text indexing if pattern matching in the middle of strings is common.

</details>

<hr/>

### ❓ Q25. **What is the purpose of the CASE statement?**

<details>
<summary><b>👀 Show Answer</b></summary>

The `CASE` statement implements conditional logic in SQL queries (similar to `if-else` in programming). It evaluates expressions and returns values depending on conditions.

```sql
SELECT name, salary,
       CASE 
         WHEN salary > 100000 THEN 'High'
         WHEN salary > 50000 THEN 'Medium'
         ELSE 'Low'
       END as salary_tier
FROM employees;
```

> 💡 **Interviewer Focus:** Formatting query outputs dynamically at the database layer.

</details>

<hr/>

## 🟡 Intermediate Level

### ❓ Q26. **Explain the different types of JOINs in SQL.**

<details>
<summary><b>👀 Show Answer</b></summary>

JOINs combine rows from two or more tables based on a related column.
- **`INNER JOIN`:** Returns records that have matching values in both tables.
- **`LEFT (OUTER) JOIN`:** Returns all records from the left table, and matching records from the right table. Right values are `NULL` on mismatches.
- **`RIGHT (OUTER) JOIN`:** Returns all records from the right table, and matching records from the left table. Left values are `NULL` on mismatches.
- **`FULL (OUTER) JOIN`:** Returns all records when there is a match in either left or right table.
- **`CROSS JOIN`:** Returns the Cartesian product of both tables (combinations of all rows).
- **`SELF JOIN`:** A regular join where a table is joined with itself (useful for hierarchical structures).

> 💡 **Interviewer Focus:** Ask about performance characteristics (INNER is faster than OUTER) and how to handle `NULL` values generated by outer joins.

</details>

<hr/>

### ❓ Q27. **What is a Database Index and how does it speed up queries?**

<details>
<summary><b>👀 Show Answer</b></summary>

An index is a performance-tuning data structure (typically a **B-Tree** or **B+Tree**) created on columns to speed up data retrieval.
- Without an index, the database must perform a **Full Table Scan** (checking every row from disk).
- With an index, it searches the B-Tree in $O(\log N)$ time to locate the row address, then jumps directly to the record.
- **Trade-off:** Indexes speed up `SELECT` queries but slow down `INSERT`, `UPDATE`, and `DELETE` queries because the database must keep the index tree updated.

> 💡 **Interviewer Focus:** Understanding that indexes cost write performance and storage.

</details>

<hr/>

### ❓ Q28. **Explain the difference between a Clustered and a Non-Clustered index.**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Clustered Index:**
  - Physically re-orders and stores the actual data rows of the table in the leaf nodes of the index.
  - Only one clustered index per table.
  - Usually created automatically on the Primary Key.
- **Non-Clustered Index:**
  - Does not physically reorder the table data.
  - Contains index key values and a **row pointer** (RID or clustered index key) to the actual data location.
  - A table can have multiple non-clustered indexes.

> 💡 **Interviewer Focus:** How clustered indexes optimize range queries, and the overhead of index lookups (non-clustered index requires jumping to the actual table pages).

</details>

<hr/>

### ❓ Q29. **What is database normalization? Explain 1NF, 2NF, and 3NF.**

<details>
<summary><b>👀 Show Answer</b></summary>

Normalization is the process of structuring a relational database to minimize data redundancy and prevent update/insert anomalies.
- **First Normal Form (1NF):**
  - Atomic values only (no lists or groups in cells).
  - Columns must have unique names.
- **Second Normal Form (2NF):**
  - Must be in 1NF.
  - No partial dependency: non-key attributes must depend on the *entire* primary key (matters only when primary key is composite).
- **Third Normal Form (3NF):**
  - Must be in 2NF.
  - No transitive dependency: non-key attributes must not depend on other non-key attributes (must depend only on the primary key).

> 💡 **Interviewer Focus:** Practical evaluation of a messy table and showing how anomalies arise if rules are violated.

</details>

<hr/>

### ❓ Q30. **What is denormalization and when would you use it?**

<details>
<summary><b>👀 Show Answer</b></summary>

Denormalization is the process of intentionally adding redundant data to a database to optimize read performance.
- **When to use:** In read-heavy systems, reporting dashboards, or data warehouses where complex, multi-table JOINs slow down retrieval.
- **Trade-off:** Writes become slower and data consistency must be managed at the application layer or via database triggers.

> 💡 **Interviewer Focus:** Trade-off analysis. Make sure the candidate highlights the consistency risks denormalization introduces.

</details>

<hr/>

### ❓ Q31. **What is the difference between a Subquery and a Co-related Subquery?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Subquery (Independent):** 
  - Runs once, independent of the outer query. Its output is returned to the outer query.
  - Example: Finding employees whose salary is above the average salary.
- **Co-related Subquery:**
  - Relies on columns from the outer query.
  - Executes once for *every* candidate row evaluated by the outer query. Can be much slower.

```sql
-- Co-related query: references outer table 'e'
SELECT name, salary 
FROM employees e 
WHERE salary > (SELECT AVG(salary) FROM employees WHERE department_id = e.department_id);
```

> 💡 **Interviewer Focus:** Performance impact. Correlated queries act like nested loops ($O(N^2)$). Suggest rewriting them using JOINs or Window Functions.

</details>

<hr/>

### ❓ Q32. **Explain Window Functions in SQL. Give examples of RANK() vs DENSE_RANK().**

<details>
<summary><b>👀 Show Answer</b></summary>

Window functions perform calculations across a set of table rows related to the current row without merging them (unlike `GROUP BY`). They use the `OVER()` clause.
- **`ROW_NUMBER()`**: Assigns a unique sequential integer starting at 1.
- **`RANK()`**: Assigns sequential ranks but leaves gaps in rank numbering on ties (e.g., 1, 2, 2, 4).
- **`DENSE_RANK()`**: Assigns sequential ranks but does not leave gaps on ties (e.g., 1, 2, 2, 3).

```sql
SELECT employee_id, salary,
       RANK() OVER (ORDER BY salary DESC) as r,
       DENSE_RANK() OVER (ORDER BY salary DESC) as dr
FROM employees;
```

> 💡 **Interviewer Focus:** Using partition clauses (`PARTITION BY`) to calculate results within specific subgroups.

</details>

<hr/>

### ❓ Q33. **What is the difference between UNION and UNION ALL?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **`UNION`:** Combines the results of two queries, performs a sorting operation, and **removes duplicates**. It is slower due to deduplication overhead.
- **`UNION ALL`:** Combines results directly **without removing duplicates**. It is much faster because no sorting/distinct check is performed.

> 💡 **Interviewer Focus:** Performance differences. Use `UNION ALL` by default if you know the datasets are naturally distinct.

</details>

<hr/>

### ❓ Q34. **What is the difference between a View and a Materialized View?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **View:** 
  - A virtual table.
  - Does not store physical data; it runs the underlying query definition every time it is referenced.
- **Materialized View:**
  - A physical table that caches the query result on disk.
  - Speeds up complex queries dramatically but gets stale.
  - Requires refresh strategies (e.g., scheduled refresh, incremental updates).

> 💡 **Interviewer Focus:** Stale data handling and synchronization models.

</details>

<hr/>

### ❓ Q35. **What is a CTE (Common Table Expression)? Provide a basic use case.**

<details>
<summary><b>👀 Show Answer</b></summary>

A Common Table Expression (CTE) is a temporary result set defined using the `WITH` clause. It makes complex queries more readable compared to nested subqueries and can be referenced multiple times in the query.

```sql
WITH HighEarners AS (
  SELECT * FROM employees WHERE salary > 100000
)
SELECT department_id, COUNT(*) 
FROM HighEarners 
GROUP BY department_id;
```

> 💡 **Interviewer Focus:** Readability improvements, and using **Recursive CTEs** to query hierarchical graph data (like org charts or category trees).

</details>

<hr/>

### ❓ Q36. **Explain BCNF (Boyce-Codd Normal Form) and how it differs from 3NF.**

<details>
<summary><b>👀 Show Answer</b></summary>

BCNF is a stricter version of 3NF. A table is in BCNF if and only if for every non-trivial functional dependency $X \rightarrow Y$, the determinant $X$ is a **superkey**.
- **Difference from 3NF:** 3NF allows a dependency $X \rightarrow Y$ if $Y$ is a prime attribute (part of a candidate key) even if $X$ is not a superkey. BCNF eliminates this exception.
- BCNF addresses anomalies where candidate keys overlap.

> 💡 **Interviewer Focus:** Explaining BCNF's constraint: "Every determinant must be a candidate key."

</details>

<hr/>

### ❓ Q37. **What is a Self Join and when is it useful?**

<details>
<summary><b>👀 Show Answer</b></summary>

A Self Join is a regular join where a table is joined with itself. It requires aliasing the table at least twice in the query.
- **Use Case:** Querying hierarchical data stored in a single table, such as finding the manager's name for each employee in a self-referential table where `manager_id` references `employee_id`.

```sql
SELECT emp.name AS Employee, mgr.name AS Manager
FROM employees emp
LEFT JOIN employees mgr ON emp.manager_id = mgr.employee_id;
```

> 💡 **Interviewer Focus:** Using table aliases correctly to reference the same table at different hierarchy layers.

</details>

<hr/>

### ❓ Q38. **Explain the difference between NULLIF() and COALESCE() functions.**

<details>
<summary><b>👀 Show Answer</b></summary>

- **`COALESCE(val1, val2, ...)`**: Evaluates parameters in order and returns the **first non-null value** in the list.
- **`NULLIF(val1, val2)`**: Compares two values. If they are equal, it returns `NULL`; otherwise, it returns the first value (`val1`). Useful to prevent division-by-zero errors.

```sql
-- Prevent division by zero
SELECT total_sales / NULLIF(units_sold, 0) FROM product_metrics;
```

> 💡 **Interviewer Focus:** Handling data validation and fallback scenarios gracefully.

</details>

<hr/>

### ❓ Q39. **How do you find the second-highest salary from an Employee table?**

<details>
<summary><b>👀 Show Answer</b></summary>

Multiple options exist depending on vendor support:

```sql
-- Option A: Keyset Offset (Standard)
SELECT salary FROM employees 
ORDER BY salary DESC 
LIMIT 1 OFFSET 1;

-- Option B: Subquery (Highly Compatible)
SELECT MAX(salary) FROM employees 
WHERE salary < (SELECT MAX(salary) FROM employees);

-- Option C: Window Function (Optimal for ties)
WITH RankedSalaries AS (
  SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) as rnk
  FROM employees
)
SELECT DISTINCT salary FROM RankedSalaries WHERE rnk = 2;
```

> 💡 **Interviewer Focus:** Handling ties (multiple employees with the same highest salary) using `DENSE_RANK()`.

</details>

<hr/>

### ❓ Q40. **What is a database transaction and what are the ACID properties?**

<details>
<summary><b>👀 Show Answer</b></summary>

A **Transaction** is a logical unit of database work containing one or more SQL statements executed as a single block.
- **ACID Properties:**
  - **Atomicity:** All statements inside the transaction succeed, or all fail and are rolled back ("all or nothing").
  - **Consistency:** Ensures the database transitions from one valid state to another, enforcing all schema constraints.
  - **Isolation:** Concurrent transactions execute without interfering with each other's uncommitted data.
  - **Durability:** Once committed, transaction updates are permanent on disk and survive crashes.

> 💡 **Interviewer Focus:** Explaining how database locks and write-ahead logs implement these properties under the hood.

</details>

<hr/>

### ❓ Q41. **What is the difference between primary keys and unique keys regarding nullability?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Primary Key:** Must be unique and cannot contain any `NULL` values. Only one primary key is allowed per table.
- **Unique Key:** Enforces uniqueness across values but **allows NULL values** (either a single NULL in SQL Server, or multiple NULLs in PostgreSQL/MySQL, since NULL is treated as an unknown value and thus not equal to other NULLs).

> 💡 **Interviewer Focus:** Understanding standard differences in how database engines handle multiple NULL values in UNIQUE columns.

</details>

<hr/>

### ❓ Q42. **How does standard SQL handle string concatenation across different databases?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Standard SQL (ANSI):** Uses the double pipe operator `||` (e.g., `first_name || ' ' || last_name`). Supported by PostgreSQL, Oracle, and SQLite.
- **MySQL:** Uses `CONCAT(first_name, ' ', last_name)`.
- **SQL Server:** Uses the plus operator `+` (e.g., `first_name + ' ' + last_name`).

> 💡 **Interviewer Focus:** Cross-database compatibility issues when writing string interpolation queries.

</details>

<hr/>

### ❓ Q43. **What is an Upsert operation?**

<details>
<summary><b>👀 Show Answer</b></summary>

An **Upsert** is a database operation that inserts a row if it does not exist, or updates it if a uniqueness constraint conflict occurs.
- **PostgreSQL:** `INSERT INTO users (id, name) VALUES (1, 'Alice') ON CONFLICT (id) DO UPDATE SET name = 'Alice';`
- **MySQL:** `INSERT INTO users (id, name) VALUES (1, 'Alice') ON DUPLICATE KEY UPDATE name = 'Alice';`

> 💡 **Interviewer Focus:** Preventing primary key collisions in distributed applications and saving query roundtrips.

</details>

<hr/>

### ❓ Q44. **What is a composite index and why is column order important?**

<details>
<summary><b>👀 Show Answer</b></summary>

A composite index is an index on two or more columns (e.g., `(last_name, first_name)`).
- **Left-to-Right Prefix Rule:** The database can only use a composite index if the query filters include the left-most columns first.
- An index on `(A, B, C)` can speed up queries filtering on `(A)`, `(A, B)`, or `(A, B, C)`, but **cannot** speed up queries filtering solely on `(B)` or `(B, C)` because the index tree sorting keys start with `A`.

> 💡 **Interviewer Focus:** Explaining how to design composite indexes that support multiple queries while avoiding redundant index creations.

</details>

<hr/>

### ❓ Q45. **What are aggregate functions? Name five.**

<details>
<summary><b>👀 Show Answer</b></summary>

Aggregate functions perform a calculation on a set of values and return a single summarizing value. They ignore `NULL` values (except `COUNT(*)`).
1. `SUM()` - Calculates the total sum of numeric fields.
2. `AVG()` - Calculates the average value of numeric fields.
3. `COUNT()` - Returns the number of matching items.
4. `MAX()` - Returns the highest value in a column.
5. `MIN()` - Returns the lowest value in a column.

> 💡 **Interviewer Focus:** Understanding how grouping rules mandate that aggregate functions must run with a `GROUP BY` clause.

</details>

<hr/>

### ❓ Q46. **What is the purpose of foreign key cascade constraints?**

<details>
<summary><b>👀 Show Answer</b></summary>

They define what happens to child records when a referenced parent record is updated or deleted:
- **`ON DELETE CASCADE`:** If a parent row is deleted, all matching child rows are deleted automatically.
- **`ON DELETE SET NULL`:** If a parent row is deleted, the foreign key column in the child rows is set to `NULL`.
- **`ON DELETE RESTRICT` / `NO ACTION`:** Prevents deleting the parent row if any child rows reference it.

> 💡 **Interviewer Focus:** Preventing orphan database records and managing cascading delete performance costs.

</details>

<hr/>

### ❓ Q47. **What is the difference between cross joins and inner joins?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **`CROSS JOIN`:** Returns the Cartesian product of both tables. It matches every row of Table A with every row of Table B (e.g., $M \times N$ rows output). No join condition is specified.
- **`INNER JOIN`:** Matches rows between tables based on a specific join condition (e.g., `ON A.id = B.id`). Only returns rows that meet the criteria.

> 💡 **Interviewer Focus:** Performance impact of accidental CROSS JOIN queries on large tables.

</details>

<hr/>

### ❓ Q48. **How do you write a query to find duplicate records in a table?**

<details>
<summary><b>👀 Show Answer</b></summary>

To identify duplicate values in a column, group by that column and use the `HAVING` clause to filter out groups with a count greater than `1`:

```sql
SELECT email, COUNT(*) 
FROM users 
GROUP BY email 
HAVING COUNT(*) > 1;
```

> 💡 **Interviewer Focus:** Grouping column validation patterns.

</details>

<hr/>

### ❓ Q49. **What does the SQL command `TRUNCATE TABLE` do to the auto-increment counter?**

<details>
<summary><b>👀 Show Answer</b></summary>

Unlike `DELETE`, running `TRUNCATE` reset the auto-increment primary key identity counter back to its initial start value (usually `1` or `0`), because it deallocates the table's data pages entirely.

> 💡 **Interviewer Focus:** Understanding side-effects of `TRUNCATE` on table identity tracking.

</details>

<hr/>

### ❓ Q50. **What are temporary tables in SQL?**

<details>
<summary><b>👀 Show Answer</b></summary>

Temporary tables are short-lived tables that exist only for the duration of a client database session or transaction. They are automatically dropped when the session ends and are isolated from other concurrent user sessions.

```sql
CREATE TEMPORARY TABLE temp_orders AS 
SELECT * FROM orders WHERE order_date = CURRENT_DATE;
```

> 💡 **Interviewer Focus:** Storing intermediate calculation results in complex data processing pipelines.

</details>

<hr/>

## 🔴 Advanced Level

### ❓ Q51. **How do you identify and optimize a slow-running SQL query?**

<details>
<summary><b>👀 Show Answer</b></summary>

Query optimization follows a structured approach:
1. **Locate the Query:** Check Slow Query Logs or APM dashboards.
2. **Analyze the Execution Plan:** Prepend `EXPLAIN` (or `EXPLAIN ANALYZE` in PostgreSQL/MySQL) to inspect how the optimizer processes the query.
3. **Verify Indexing:** 
   - Look for `ALL` access (Full Table Scan) or missing keys.
   - Implement missing indexes on `WHERE`, `JOIN` conditions, and `ORDER BY` columns.
4. **Optimize SELECT list:** Avoid `SELECT *`. Retrieve only the columns required to optimize memory, network load, and leverage covering indexes.
5. **Rewrite Queries:** 
   - Avoid non-sargable queries (e.g., `WHERE YEAR(date) = 2026` does not use indexes; rewrite as `WHERE date >= '2026-01-01' AND date < '2027-01-01'`).
   - Replace slow co-related subqueries with `JOIN`s or window functions.
6. **Analyze Database Configuration:** Adjust pool sizes, buffer memory sizes, or execute maintenance routines (like `ANALYZE TABLE` or defragmentation).

> 💡 **Interviewer Focus:** Sargable vs non-sargable query patterns and reading `EXPLAIN` plan outputs.

</details>

<hr/>

### ❓ Q52. **Explain Transaction Isolation Levels and the read phenomena they prevent.**

<details>
<summary><b>👀 Show Answer</b></summary>

Relational databases support four standard isolation levels (defined by SQL-92) to balance concurrency against data consistency.
- **Read Phenomena:**
  - **Dirty Read:** Transaction A reads data modified by Transaction B before B commits. If B rolls back, A's data is invalid.
  - **Non-Repeatable Read:** Transaction A reads a row. Transaction B modifies that row and commits. Transaction A re-reads the row and sees different data.
  - **Phantom Read:** Transaction A queries a range of rows. Transaction B inserts new rows in that range and commits. Transaction A re-runs the query and sees "phantom" rows.

- **Isolation Levels and Protections:**

| Isolation Level | Dirty Reads | Non-Repeatable Reads | Phantom Reads | Mechanism |
| :--- | :---: | :---: | :---: | :--- |
| **Read Uncommitted**| Allowed | Allowed | Allowed | No locks. |
| **Read Committed** | Prevented | Allowed | Allowed | Read locks released immediately. |
| **Repeatable Read** | Prevented | Prevented | Allowed | Read locks held until commit. |
| **Serializable** | Prevented | Prevented | Prevented | Range/Key-range locks. |

*Note: In MySQL InnoDB, Repeatable Read also prevents Phantom Reads using Next-Key locking.*

> 💡 **Interviewer Focus:** Concurrency vs isolation trade-offs. Higher isolation levels reduce database performance due to lock contention.

</details>

<hr/>

### ❓ Q53. **What is the N+1 Query Problem in backend applications and how do you solve it?**

<details>
<summary><b>👀 Show Answer</b></summary>

The **N+1 Query Problem** occurs when an application executes 1 query to fetch parent records, followed by N queries to fetch associated child records for each parent.
- **Example:** Fetching 100 posts, then running 100 individual queries to fetch the author for each post.
- **Impact:** High latency due to 101 database roundtrips.
- **Solutions:**
  1. **SQL Layer:** Use an `INNER JOIN` or `LEFT JOIN` to fetch posts and authors in a single query.
  2. **ORM Layer:** Enable **Eager Loading** (e.g., `include` in Prisma/Sequelize, `relations` in TypeORM) to fetch everything in 1 or 2 queries using `IN (...)`.

> 💡 **Interviewer Focus:** Point out how ORMs can mask database inefficiencies and highlight the cost of network round-trips.

</details>

<hr/>

### ❓ Q54. **What is Pessimistic vs Optimistic Locking?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Pessimistic Locking:**
  - Assumes conflicts are highly likely.
  - Locks rows immediately upon reading (e.g., using `SELECT ... FOR UPDATE` in SQL) to prevent other transactions from modifying them until the lock is released (via commit/rollback).
  - Best for: Write-heavy systems with high concurrency contention (e.g., financial ledger balances).
- **Optimistic Locking:**
  - Assumes conflicts are rare.
  - Reads data without locking. When committing, it checks if the data was modified by another transaction since it was read.
  - Typically implemented using a `version` or `timestamp` column.
  - Best for: Read-heavy systems with low collision probability (e.g., wiki pages).

```sql
-- Optimistic lock commit check:
UPDATE products 
SET stock = 49, version = version + 1 
WHERE id = 101 AND version = 3; -- If version changed, update fails.
```

> 💡 **Interviewer Focus:** Trade-off analysis. Optimistic locking avoids database-level lock overhead but requires retry logic in application code on conflicts.

</details>

<hr/>

### ❓ Q55. **How do you prevent database deadlocks?**

<details>
<summary><b>👀 Show Answer</b></summary>

A deadlock occurs when Transaction 1 holds a lock that Transaction 2 needs, while Transaction 2 holds a lock that Transaction 1 needs. Both freeze indefinitely.
- **Prevention Strategies:**
  1. **Acquire locks in a consistent order:** Ensure all transaction logic updates resources in the exact same order (e.g., always lock `User` before `Wallet`).
  2. **Keep transactions small and fast:** Avoid long-running processing or network requests inside database transactions.
  3. **Use lower isolation levels** if consistency requirements permit.
  4. **Acquire row locks upfront:** Use explicit locks (`SELECT ... FOR UPDATE`) at the start of the transaction rather than upgrading lock states mid-transaction.
  5. **Set lock timeout parameters:** Configure database timeouts to fail fast rather than hanging indefinitely.

> 💡 **Interviewer Focus:** Consistent lock ordering as the primary defense against deadlocks.

</details>

<hr/>

### ❓ Q56. **What is a Stored Procedure and how does it differ from a User-Defined Function (UDF)?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Stored Procedure:**
  - Used to execute complex transactional logic.
  - Can return multiple output values or result sets.
  - Can call other procedures and perform write transactions (`COMMIT`/`ROLLBACK`).
  - Cannot be used directly inside standard `SELECT` or `WHERE` clauses.
- **User-Defined Function (UDF):**
  - Used for calculations or formatting values.
  - Must return a single value (or table).
  - Cannot perform write operations or transaction controls (must be read-only).
  - Can be used directly inside `SELECT` statements (e.g., `SELECT formatName(name) FROM users`).

> 💡 **Interviewer Focus:** When to use business logic in the database (procedures) vs in the application layer.

</details>

<hr/>

### ❓ Q57. **Explain database sharding vs partitioning.**

<details>
<summary><b>👀 Show Answer</b></summary>

Both split data to improve performance but operate at different architectural layers.
- **Partitioning (Vertical/Horizontal at Table Level):**
  - Split tables into smaller, manageable chunks *within a single database instance*.
  - Example: Splitting an `orders` table by year (2024 partitions, 2025 partitions).
  - Transparent to the application layer.
- **Sharding (Horizontal Partitioning across Instances):**
  - Distributes data across *multiple separate database servers/instances*.
  - Example: Users with IDs 1-1M reside on Server A, IDs 1M-2M reside on Server B.
  - Requires routing logic in the application layer or a proxy database middleware.

> 💡 **Interviewer Focus:** Infrastructure complexity scaling. Sharding requires resolving cross-shard joins and distributed transactions.

</details>

<hr/>

### ❓ Q58. **What is a Covering Index, and how does it prevent key lookups?**

<details>
<summary><b>👀 Show Answer</b></summary>

A **Covering Index** is a non-clustered index that contains all the columns referenced by a query (both in the `WHERE` filters and the `SELECT` list).
- If a query is covered by an index, the database optimizer retrieves all values directly from the index tree leaf nodes.
- It bypasses the secondary step of jumping to the main table pages on disk to fetch missing column values (known as a key/bookmark lookup).

```sql
-- Query:
SELECT username, email FROM users WHERE status = 'ACTIVE';

-- Covering Index:
CREATE INDEX idx_status_user_email ON users(status, username, email);
```

> 💡 **Interviewer Focus:** Designing optimal indexes to eliminate random read disk lookups.

</details>

<hr/>

### ❓ Q59. **What are database triggers, and what are their drawbacks?**

<details>
<summary><b>👀 Show Answer</b></summary>

A trigger is a database block of code that automatically fires in response to specific DML events (`INSERT`, `UPDATE`, `DELETE`) on a table.
- **Drawbacks:**
  - **Hidden Side Effects:** Logic is hidden from application code, making debugging difficult.
  - **Performance Cost:** They run inside the same transaction scope, increasing lock times and slows down writes.
  - **Maintenance Complexity:** Can lead to cascading updates across multiple tables that are difficult to trace.

> 💡 **Interviewer Focus:** Emphasize that triggers should be used sparingly, prioritizing application-layer validation or transactional services.

</details>

<hr/>

### ❓ Q60. **How do you handle recursive queries using CTEs?**

<details>
<summary><b>👀 Show Answer</b></summary>

Use the `WITH RECURSIVE` syntax. A recursive CTE consists of:
1. **Anchor Member:** An initial query returning the base row (e.g. root manager).
2. **Recursive Member:** A query referencing the CTE name itself, joined with the anchor/source table to walk the tree.
3. **Termination Condition:** Implicitly ends when the recursive member returns no rows.

```sql
WITH RECURSIVE OrgChart AS (
  -- Anchor
  SELECT id, manager_id, name, 1 as level 
  FROM employees WHERE manager_id IS NULL
  UNION ALL
  -- Recursive step
  SELECT e.id, e.manager_id, e.name, o.level + 1 
  FROM employees e
  INNER JOIN OrgChart o ON e.manager_id = o.id
)
SELECT * FROM OrgChart;
```

> 💡 **Interviewer Focus:** Querying hierarchical adjacency lists (trees or graphs) efficiently in relational tables.

</details>

<hr/>

### ❓ Q61. **What is the difference between clustered, non-clustered, and unique indexes?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Clustered Index:** Reorders physical data storage on disk based on key values. Maximum 1 per table.
- **Non-Clustered Index:** Maintains a separate index tree structure containing pointers to the data rows. Multiple allowed per table.
- **Unique Index:** A logical constraint enforced via an index structure (which can be clustered or non-clustered) that guarantees no duplicate values are inserted into the columns.

> 💡 **Interviewer Focus:** The physical storage architecture differences between indices.

</details>

<hr/>

### ❓ Q62. **Explain what an index merge scan is.**

<details>
<summary><b>👀 Show Answer</b></summary>

An **Index Merge Scan** occurs when the query optimizer uses multiple single-column indexes to satisfy a query that filters on multiple columns (e.g. `WHERE age = 30 AND status = 'ACTIVE'`).
- The database optimizer performs separate index seeks on `idx_age` and `idx_status`, retrieves the list of matching row pointers (RIDs/Pointers), and performs an intersection (AND) or union (OR) step on the keys before fetching data pages.
- **Optimization:** If this is a frequent query, it is often better to replace the individual indexes with a single **composite index** `(age, status)`.

> 💡 **Interviewer Focus:** Identifying query optimizer fallback designs and upgrading to composite indexes.

</details>

<hr/>

### ❓ Q63. **What is database federation?**

<details>
<summary><b>👀 Show Answer</b></summary>

Database Federation (or Federated Querying) is a architecture where an application queries multiple physically separate, heterogeneous database systems (e.g. joining PostgreSQL data with MySQL or S3 files) via a single unified query interface. It uses wrappers like **Foreign Data Wrappers (FDW)** in PostgreSQL.

> 💡 **Interviewer Focus:** Distributed data routing and network overhead limitations.

</details>

<hr/>

### ❓ Q64. **Explain index fragmentation and how to resolve it.**

<details>
<summary><b>👀 Show Answer</b></summary>

Index fragmentation occurs when data modifications (`INSERT`, `UPDATE`, `DELETE`) create empty gaps on index pages (Internal fragmentation) or cause pages to become out-of-order in physical memory (External fragmentation).
- **Impact:** Degrades performance of range scans because disk heads must jump around.
- **Resolutions:**
  - **Reorganize (Defragment):** Sorts pages and compacts them in-place (online operation, minimal locks).
  - **Rebuild:** Drops and recreates the index from scratch, defragmenting both internally and externally (locks table unless run with `ONLINE = ON`).

> 💡 **Interviewer Focus:** Index maintenance routines in large databases.

</details>

<hr/>

### ❓ Q65. **What is connection pooling and why is it important in high-traffic applications?**

<details>
<summary><b>👀 Show Answer</b></summary>

Connection pooling maintains a cache of active database connections that are shared and reused by application threads.
- **Why it is important:** Creating a new TCP connection to a database for every incoming request has high overhead (TCP handshakes, SSL negotiations, DB process allocation). Reusing connections from a pool (using tools like PgBouncer or HikariCP) drops latency from milliseconds to microseconds.

> 💡 **Interviewer Focus:** Tuning pool size metrics (calculating connection limit limits based on CPU and RAM capacities).

</details>

<hr/>

### ❓ Q66. **What is the difference between a write-ahead log (WAL) and a redo log?**

<details>
<summary><b>👀 Show Answer</b></summary>

They represent the same concept under different names across vendor dialects:
- **Write-Ahead Log (WAL)** (PostgreSQL standard term): An append-only log recording changes before they are committed to data pages.
- **Redo Log** (Oracle, MySQL InnoDB term): An identical transaction log recording page-level physical changes used to reconstruct committed writes on recovery.

> 💡 **Interviewer Focus:** Understanding the core durability mechanism common to relational databases.

</details>

<hr/>

### ❓ Q67. **How do you implement soft deletes at the database layer?**

<details>
<summary><b>👀 Show Answer</b></summary>

Soft deletes flag records as inactive rather than deleting them from disk:
1. Add a `deleted_at TIMESTAMP` or `is_deleted BOOLEAN` column.
2. Update application queries to filter `WHERE deleted_at IS NULL`.
3. **Gotcha:** Standard unique constraints (like `UNIQUE(username)`) break on soft-deletes since you cannot insert a duplicate username even if the original record was deleted.
4. **Fix:** Use a **Partial Index** to enforce uniqueness only on active rows: `CREATE UNIQUE INDEX idx_uniq_username ON users(username) WHERE deleted_at IS NULL;`

> 💡 **Interviewer Focus:** Partial indexes configuration to resolve uniqueness constraint collisions on soft-deleted rows.

</details>

<hr/>

### ❓ Q68. **Explain row-level security (RLS) in databases.**

<details>
<summary><b>👀 Show Answer</b></summary>

Row-Level Security (RLS) is a security feature (supported by PostgreSQL, SQL Server) that restricts which data rows a database user can retrieve or modify based on security policies.
- It attaches filters automatically to outgoing queries based on the database user session context (e.g. a tenant user query is automatically appended with `AND tenant_id = current_tenant()`).

> 💡 **Interviewer Focus:** Multi-tenant isolation enforcement at the database layer.

</details>

<hr/>

### ❓ Q69. **What are the differences between SQL Server's CROSS APPLY and INNER JOIN?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **`INNER JOIN`:** Evaluates two independent tables on a join condition. It cannot join a table with a table-valued function or correlated subquery that depends on columns from the left table.
- **`CROSS APPLY`:** Evaluates a table-valued function or correlated subquery for *every row* of the left table (similar to a foreach loop). It can pass parent columns down as parameters.

> 💡 **Interviewer Focus:** Joining parent tables with table-valued functions or custom functions.

</details>

<hr/>

### ❓ Q70. **What is a collation in SQL?**

<details>
<summary><b>👀 Show Answer</b></summary>

A Collation defines the rules for comparing and sorting character strings (case sensitivity, accent sensitivity, character sets, and locales).
- **Example:** `utf8mb4_unicode_ci` is a MySQL collation that is case-insensitive (`_ci`) and supports emojis.
- Changing collation changes alphabetical sorting sequences in `ORDER BY`.

> 💡 **Interviewer Focus:** Character sets, case sensitivity comparisons, and Unicode compatibility.

</details>

<hr/>

### ❓ Q71. **How do you choose between using an index scan vs an index seek?**

<details>
<summary><b>👀 Show Answer</b></summary>

This choice is made automatically by the database query optimizer:
- **Index Seek:** The optimizer traverses the index tree directly to retrieve a specific record or narrow range. Efficient for low-cardinality queries returning few rows.
- **Index Scan:** The database reads the *entire* index tree from start to finish. Chosen if the query retrieves a large percentage of table rows or if the columns filtered are not index prefixes.

> 💡 **Interviewer Focus:** How selectivity and statistics drive optimizer execution plans.

</details>

<hr/>

### ❓ Q72. **What does the keyword FORCE INDEX do in MySQL?**

<details>
<summary><b>👀 Show Answer</b></summary>

`FORCE INDEX` is a query hint that overrides the database optimizer's execution plan logic, forcing it to use a specified index even if the optimizer calculations suggested a full table scan or index scan was faster.

```sql
SELECT * FROM orders FORCE INDEX (idx_created_at) WHERE created_at = '2026-06-28';
```

> 💡 **Interviewer Focus:** When optimizer statistics are stale or incorrect, using hints as a temporary production hotfix.

</details>

<hr/>

### ❓ Q73. **How do you write a query to merge overlapping date ranges?**

<details>
<summary><b>👀 Show Answer</b></summary>

This is a classic "Island and Gaps" problem. You can solve it using Window Functions (`LAG` or `LEAD`) to calculate bounds:

```sql
WITH Bounds AS (
  SELECT start_date, end_date,
         -- Get the maximum end_date of all prior intervals
         MAX(end_date) OVER (ORDER BY start_date ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) as max_prev_end
  FROM room_bookings
),
Islands AS (
  SELECT start_date, end_date,
         -- Flag a new island start if there's no overlap
         CASE WHEN max_prev_end >= start_date THEN 0 ELSE 1 END as is_new_island
  FROM Bounds
),
Groups AS (
  SELECT start_date, end_date,
         -- Calculate running sum to group overlapping records
         SUM(is_new_island) OVER (ORDER BY start_date) as group_id
  FROM Islands
)
SELECT MIN(start_date) as merged_start, MAX(end_date) as merged_end
FROM Groups
GROUP BY group_id;
```

> 💡 **Interviewer Focus:** Intermediate state tracking using window aggregate frames.

</details>

<hr/>

### ❓ Q74. **What is the SQL standard syntax for transaction savepoints?**

<details>
<summary><b>👀 Show Answer</b></summary>

Savepoints allow rolling back a subset of statements within an active transaction without aborting the entire transaction.
- **Syntax:**
  - `SAVEPOINT my_savepoint;` (Creates a checkpoint)
  - `ROLLBACK TO SAVEPOINT my_savepoint;` (Rolls back changes since checkpoint)
  - `RELEASE SAVEPOINT my_savepoint;` (Discards savepoint context)

> 💡 **Interviewer Focus:** Implementing partial transaction recovery in complex application batch processes.

</details>

<hr/>

### ❓ Q75. **What is the difference between synthetic keys and natural keys?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Natural Key:** A column containing real-world identifiers that are naturally unique (e.g. Email, SSN, ISBN).
- **Synthetic Key:** An artificial, system-generated primary key (e.g. auto-incrementing `id`, UUID) created purely for database indexing and relationships.
- **Best Practice:** Default to synthetic keys because natural keys can change (e.g. users change emails), which breaks foreign key structures across tables.

> 💡 **Interviewer Focus:** Key mutability risks and database join efficiency (synthetic integers join faster than natural strings).

</details>

<hr/>

## 🟣 Expert Level

### ❓ Q76. **Explain Multi-Version Concurrency Control (MVCC) in modern relational engines.**

<details>
<summary><b>👀 Show Answer</b></summary>

Modern databases (like PostgreSQL and MySQL InnoDB) implement concurrency using **Multi-Version Concurrency Control (MVCC)** instead of acquiring read locks on everything.
- **Core Principle:** Readers do not block writers, and writers do not block readers.
- **How it works:**
  - When a transaction updates or deletes a row, the database does not overwrite the existing record in-place.
  - Instead, it creates a new version of the row on disk, marking each version with transaction IDs indicating when it was created and when it was deleted.
  - When another transaction reads the data, the database uses a **Snapshot** (Read View) of active transactions to determine which version of the row is visible to it.
  - Old, unreachable row versions are cleaned up asynchronously (e.g., PostgreSQL's **Vacuuming** process or MySQL's **Undo Log/Purge** threads).

> 💡 **Interviewer Focus:** Vacuuming overhead in PostgreSQL, bloat prevention, and undo log storage in MySQL InnoDB.

</details>

<hr/>

### ❓ Q77. **How do B-Trees compare to LSM Trees for relational and hybrid workloads?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **B-Trees (and B+Trees):**
  - Structure: Balanced tree on disk with nodes mapped to fixed-size pages.
  - Writes: Require random writes to disk pages, leading to **write amplification** and potential page splits.
  - Reads: Extremely fast for reads, range queries, and point lookups because data pages are contiguous and ordered.
  - Best for: Read-heavy relational workloads (Standard SQL).
- **Log-Structured Merge-Trees (LSM Trees):**
  - Structure: Writes are appended to an in-memory buffer (**MemTable**) and written sequentially to disk as immutable **SSTables**. SSTables are periodically merged and sorted via background **Compaction**.
  - Writes: Rapid, sequential writes.
  - Reads: Slower for reads since it may need to search multiple SSTables on disk to find the latest version of a row.
  - Best for: Write-heavy or time-series workloads (NoSQL databases like Cassandra, RocksDB).

> 💡 **Interviewer Focus:** Write amplification factors and point lookup trade-offs.

</details>

<hr/>

### ❓ Q78. **Explain the implementation of Distributed Transactions using the Two-Phase Commit (2PC) protocol.**

<details>
<summary><b>👀 Show Answer</b></summary>

When a transaction spans multiple physical database nodes, 2PC ensures all nodes either commit or abort the changes.
- **Participants:** A Coordinator node and multiple Participant nodes.
- **Phase 1: Prepare Phase**
  1. The Coordinator sends a `Prepare` message to all Participants.
  2. Each Participant runs the local transaction up to the point of committing, acquires locks, writes undo/redo logs, and checks if it *can* commit.
  3. Participants vote `Yes` (if prepared) or `No` (if failed/aborted).
- **Phase 2: Commit Phase**
  - **If all vote `Yes`:** The Coordinator logs a commit decision and sends `Commit` to all Participants. Participants execute the commit, release locks, and send an acknowledgment.
  - **If any vote `No`:** The Coordinator sends `Rollback` to all Participants. Participants roll back changes and release locks.
- **Drawbacks:**
  - **Blocking Protocol:** If the coordinator crashes mid-process, participants hang indefinitely holding locks (SPOF).
  - High latency due to network round-trips.

> 💡 **Interviewer Focus:** Understanding the failure modes of 2PC, coordinator recovery, and alternatives like Saga patterns.

</details>

<hr/>

### ❓ Q79. **How do you perform zero-downtime schema migrations on tables containing 100M+ rows?**

<details>
<summary><b>👀 Show Answer</b></summary>

Directly executing `ALTER TABLE` on huge tables can lock the table for hours, causing an outage.
- **Strategies:**
  - **Online Schema Change tools (e.g., `gh-ost`, `pt-online-schema-change`):**
     - Creates a duplicate ghost table with the new schema.
     - Slowly copies data from the old table to the new one in small chunks.
     - Uses database triggers (or parses replication logs) to sync real-time writes from the old table to the new table.
     - Performs a fast rename swap when synchronized.
  - **PostgreSQL Safe Migrations:**
     - Add columns with `NULL` or default values carefully (PostgreSQL 11+ does not write default values to disk instantly, avoiding writes).
     - Separate constraint validation into two steps: `ADD CONSTRAINT ... NOT VALID` followed by `VALIDATE CONSTRAINT` (which scans data without holding a write lock).
  - **Application-Layer Dual Writing:**
     - Add new columns to the schema.
     - Modify application code to write to both old and new columns.
     - Run a background script to backfill historical data.
     - Switch reads to the new column, then deprecate and drop the old column.

> 💡 **Interviewer Focus:** Lock levels (Exclusive vs Share locks) and preventing replica replication lag spikes during migrations.

</details>

<hr/>

### ❓ Q80. **Explain how Write-Ahead Logging (WAL) ensures Durability and Crash Recovery.**

<details>
<summary><b>👀 Show Answer</b></summary>

To prevent losing data on power loss or crashes, databases rely on **Write-Ahead Logging (WAL)**:
- Instead of writing modified data pages directly to random locations on disk immediately (which is slow), the database appends transaction changes sequentially to an append-only log file on disk (the WAL) first.
- The transaction is only considered committed once the WAL is flushed to non-volatile storage (`fsync`).
- Modified data pages in memory (buffer pool) are marked as dirty and written to disk later asynchronously (checkpointing).
- **Recovery:** On crash, the database reads the WAL from the last checkpoint:
  - **Redo:** Re-applies committed transactions whose data pages had not made it to disk.
  - **Undo:** Reverts uncommitted transactions that were active during the crash.

> 💡 **Interviewer Focus:** The role of `fsync` in performance vs safety and checkpointing frequency.

</details>

<hr/>

### ❓ Q81. **Explain the implementation of Read-After-Write Consistency in replica architectures.**

<details>
<summary><b>👀 Show Answer</b></summary>

In master-replica architectures, replication is asynchronous, leading to replication lag. If a user writes to the primary and reads from a replica immediately, they may see stale data.
- **Solutions:**
  - **Pin to primary:** Route reads to the primary database for a specific duration (e.g. 5-10 seconds) after the user executes a write operation.
  - **Replication verification:** Application checks the replica's Log Sequence Number (LSN) or transaction ID to verify it has processed the user's write transaction before reading.
  - **Session tokens:** Pass replication status tokens to clients, routing reads only to replicas matching or exceeding that transaction index.

> 💡 **Interviewer Focus:** Balancing read scalability against consistency requirements.

</details>

<hr/>

### ❓ Q82. **Explain phantom read prevention mechanisms under the hood in InnoDB.**

<details>
<summary><b>👀 Show Answer</b></summary>

In MySQL InnoDB, under the `REPEATABLE READ` isolation level, phantom reads are prevented using **Next-Key Locks**:
- InnoDB combines **Record Locks** (locking the specific indexed row) with **Gap Locks** (locking the empty spaces/gaps between index values).
- When a query scans a range (e.g. `WHERE age > 30`), InnoDB locks both the matching rows and the gaps between them. This prevents other concurrent transactions from inserting new rows within that index range until the transaction commits.

> 💡 **Interviewer Focus:** How Gap Locks work and why they can cause frequent deadlock anomalies.

</details>

<hr/>

### ❓ Q83. **How do you design a database schema for a high-concurrency ledger system to avoid hot-spotting?**

<details>
<summary><b>👀 Show Answer</b></summary>

Directly updating a single account balance row (e.g. `UPDATE accounts SET balance = balance + 10 WHERE id = 1`) locks that row. If thousands of requests hit the same account simultaneously, it creates a **write hot-spot** due to lock queue wait states.
- **Solution: Split Balance Pattern.**
  - Instead of a single row, store balances across multiple sub-account shard rows (e.g. 10 balance rows for a single account).
  - Incoming writes randomly update one of the 10 shards, reducing lock contention by 90%.
  - To read the balance, query the sum of all shards: `SELECT SUM(balance) FROM account_shards WHERE account_id = 1;`
  - Periodically run a background worker to consolidate shards.

> 💡 **Interviewer Focus:** Trade-off analysis: faster writes vs more expensive sum reads.

</details>

<hr/>

### ❓ Q84. **What is index selectivity, and how does a DB optimizer choose between index lookup vs table scan?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Index Selectivity:** The ratio of unique values in a column to the total number of records (Selectivity = Cardinality / Total Rows).
- High selectivity (close to 1, e.g. emails) makes indexes highly effective. Low selectivity (close to 0, e.g. gender) makes indexes useless.
- **Optimizer choice:** If selectivity is high and the query retrieves few rows, the optimizer uses an index seek. If the query retrieves a large percentage of the table (usually > 20%), the optimizer chooses a full table scan instead of random read index lookups to save disk head seeks.

> 💡 **Interviewer Focus:** Cardinality calculation, histogram statistics, and the threshold where table scans outperform index searches.

</details>

<hr/>

### ❓ Q85. **Explain the difference between optimistic concurrency control (OCC) and multi-version concurrency control (MVCC).**

<details>
<summary><b>👀 Show Answer</b></summary>

- **OCC (Optimistic Concurrency Control):** A transaction runs without acquiring locks. When committing, it checks if any other transaction modified the target data (validation phase). If a conflict is found, the transaction is aborted and must be retried by the application.
- **MVCC (Multi-Version Concurrency Control):** The database maintains multiple physical versions of rows. Readers see a snapshot version of the data matching their start transaction timestamp. Writes create new versions. It avoids aborts for readers and uses row-level write locks to handle write conflicts.

> 💡 **Interviewer Focus:** Contrasting OCC application-level retries with MVCC version management.

</details>

<hr/>

### ❓ Q86. **How does PostgreSQL handle write-amplification caused by heap-only tuples (HOT) updates?**

<details>
<summary><b>👀 Show Answer</b></summary>

In PostgreSQL, updating a row writes a new version of the row to disk (MVCC), which normally requires updating all indexes pointing to that row (causing write-amplification).
- **HOT (Heap-Only Tuples) Optimization:**
  - If the update does not modify any indexed columns, and there is enough free space on the same page, PostgreSQL writes the new row version to the same page.
  - It creates a local pointer chain on the page from the old row version to the new version.
  - Indexes continue pointing to the old row address, avoiding index write amplification entirely.

> 💡 **Interviewer Focus:** Tuning table fillfactor (e.g. setting to 80-90%) to preserve page space for HOT updates.

</details>

<hr/>

### ❓ Q87. **What is linearizability vs serializability?**

<details>
<summary><b>👀 Show Answer</b></summary>

They are consistency models addressing different dimensions:
- **Serializability:** A multi-transaction execution model. Enforces that the concurrent execution of multiple transactions yields the exact same state as if they had executed sequentially in some order. Addresses transaction operations interleaving.
- **Linearizability:** A single-operation, real-time read/write ordering model. Guarantees that once a write completes, all subsequent reads (in real-time) must return that write or a later write. Addresses distributed consensus and replication lag.

> 💡 **Interviewer Focus:** Concurrency control (database isolation) vs distributed system latency/consistency (linearizability).

</details>

<hr/>

### ❓ Q88. **Explain the concept of partition pruning in relational database engines.**

<details>
<summary><b>👀 Show Answer</b></summary>

Partition pruning is a query optimizer optimization for partitioned tables.
- If a table is partitioned horizontally by range (e.g. by `order_year`), and a query contains a filter `WHERE order_year = 2026`, the optimizer "prunes" (excludes) all other partitions (2024, 2025, etc.) from the execution plan.
- The query engine scans only the disk partitions containing 2026 data, saving disk I/O.

> 💡 **Interviewer Focus:** Writing queries containing sargable partition key expressions to enable pruning.

</details>

<hr/>

### ❓ Q89. **What is query compilation and parameterized query caching under the hood?**

<details>
<summary><b>👀 Show Answer</b></summary>

When a query is sent to a database:
1. **Parser & Lexer:** Validates syntax.
2. **Optimizer:** Compiles the query into an **execution plan** (calculating join paths and index selections). This compilation is CPU-heavy.
3. **Plan Cache:** Parameterized queries (using placeholders like `?` or `$1` instead of literal values) allow the database to compile the plan once and cache it. Subsequent queries reuse the pre-compiled plan from cache, saving CPU cycles.

> 💡 **Interviewer Focus:** Performance advantages of prepared statements and plan caching.

</details>

<hr/>

### ❓ Q90. **Explain how distributed databases achieve consensus using Paxos or Raft.**

<details>
<summary><b>👀 Show Answer</b></summary>

Distributed SQL databases (like CockroachDB or Spanner) replicate data across nodes using consensus algorithms:
- Data ranges are assigned to a consensus group (Raft group).
- Every write must be committed by a majority of nodes in the group.
- **Raft workflow:** A Leader node receives the write, writes it to its log, and broadcasts it to Follower nodes. Once a quorum (majority) of followers acknowledge writing it to their logs, the leader commits the transaction and sends confirmation to the client. This prevents data loss during node failures.

> 💡 **Interviewer Focus:** Quorum calculation ($Q = \lfloor N/2 \rfloor + 1$) and failover leader elections.

</details>

<hr/>

### ❓ Q91. **What is database row bloat, and how does it happen during high write/delete volume?**

<details>
<summary><b>👀 Show Answer</b></summary>

Row bloat (specifically in PostgreSQL MVCC) occurs when a high volume of `UPDATE` and `DELETE` queries create dead row versions (garbage) that have not been reclaimed.
- **Cause:** PostgreSQL does not delete rows instantly. Dead rows are cleaned up by the **Autovacuum** process.
- If Autovacuum is slow or blocked (e.g. by long-running transactions or active replication slots), dead rows accumulate on disk, increasing table size and slowing down sequential scans.

> 💡 **Interviewer Focus:** Autovacuum configuration tuning and long-running transaction prevention.

</details>

<hr/>

### ❓ Q92. **How does MySQL InnoDB handle page splitting and key sorting in indexes?**

<details>
<summary><b>👀 Show Answer</b></summary>

InnoDB indexes are B+Trees stored in 16KB pages.
- **Page splitting:** If a new row is inserted into a full index page (e.g. inserting a random UUID out of order), InnoDB splits the page into two pages, allocating 50% of the index keys to each page. This requires writing to disk and reorganizing tree pointers, leading to write amplification.
- **Optimization:** Using sequentially increasing keys (like `AUTO_INCREMENT` or ULIDs) ensures writes always append to the end of the last page, avoiding splits.

> 💡 **Interviewer Focus:** UUID primary key index performance degradation vs sequential keys.

</details>

<hr/>

### ❓ Q93. **Explain the difference between statement-based replication and row-based replication.**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Statement-Based Replication (SBR):** The primary logs the exact SQL statements (e.g. `UPDATE users SET status = 'ACTIVE' WHERE age > 30`) and replicas execute them.
  - Pros: Small log size.
  - Cons: Non-deterministic functions (like `NOW()`, `RAND()`, `UUID()`) cause data mismatch on replicas.
- **Row-Based Replication (RBR):** The primary logs the actual page-level row modifications. Replicas apply the changes directly.
  - Pros: Safe, deterministic, supports all query types.
  - Cons: High log volume (updating 1M rows generates 1M log records).

> 💡 **Interviewer Focus:** Data drift prevention vs write log network overhead.

</details>

<hr/>

### ❓ Q94. **Explain how databases handle lock upgrades and lock escalation.**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Lock Upgrade:** A single transaction upgrades a lock it already holds on a resource (e.g. upgrading a Shared Read Lock on a row to an Exclusive Write Lock because it wants to perform an update). This can cause deadlocks if two concurrent threads try to upgrade on the same row.
- **Lock Escalation:** The database engine automatically converts many fine-grained locks (e.g. 10,000 individual row locks) into a single coarse-grained lock (e.g. a single table lock) to save system memory.

> 💡 **Interviewer Focus:** Lock memory consumption thresholds and table concurrency issues.

</details>

<hr/>

### ❓ Q95. **What is doublewrite buffering in MySQL InnoDB and why is it used?**

<details>
<summary><b>👀 Show Answer</b></summary>

Doublewrite buffering is a crash-safety mechanism in InnoDB designed to prevent **torn page anomalies** (partial page writes caused by OS power failure while writing a 16KB InnoDB page to 4KB OS sectors).
- **How it works:** Before writing pages to data files, InnoDB writes them to a contiguous layout buffer (Doublewrite Buffer) on disk first.
- If a crash occurs during the subsequent write to the main data file, InnoDB recovers the uncorrupted page version from the Doublewrite Buffer and finishes the write.

> 💡 **Interviewer Focus:** Durability guarantees and disk write overhead.

</details>

<hr/>

### ❓ Q96. **How does PostgreSQL handle transaction wraparound?**

<details>
<summary><b>👀 Show Answer</b></summary>

PostgreSQL transaction IDs (TxID) are unsigned 32-bit integers, meaning there are $2^{32}$ (approx 4 billion) possible transaction values.
- **Wraparound problem:** Since IDs are finite, they eventually wrap around to `0`. If not managed, newer transactions appear older than historical ones, causing data invisibility.
- **Solution:** Autovacuum performs a "freeze" operation, rewriting old transaction headers to a special frozen TxID (`2`) which is treated as older than all other IDs.
- If the TxID counter approaches the limit without vacuuming, PostgreSQL stops accepting writes and shuts down to prevent data corruption.

> 💡 **Interviewer Focus:** Monitoring transaction age metrics (`age(datfrozenxid)`) to prevent write-outage failures.

</details>

<hr/>

### ❓ Q97. **Explain the concept of write skew in Serializable Snapshot Isolation (SSI).**

<details>
<summary><b>👀 Show Answer</b></summary>

Write Skew is a concurrency anomaly that can occur under Snapshot Isolation (which is weaker than strict Serializable).
- **Concept:** Two concurrent transactions (T1 and T2) read overlapping data, evaluate a precondition, and write to distinct tables/rows that are related.
- **Example:** A rule says "at least one doctor must be active". Doctors A and B are active.
  - T1 reads doctors active (2). T1 takes Doctor A off call (commits).
  - T2 reads doctors active (2). T2 takes Doctor B off call (commits).
  - Both commit successfully because they updated different rows, but the rule is violated (0 active doctors).
- **Solution:** Strict Serializable using SSI (which tracks read-write dependency graph cycles) or explicit locking (`SELECT FOR UPDATE`).

> 💡 **Interviewer Focus:** Understanding why standard row locks do not prevent write skew anomalies.

</details>

<hr/>

### ❓ Q98. **How does distributed sharding affect aggregation queries like GROUP BY and COUNT?**

<details>
<summary><b>👀 Show Answer</b></summary>

In sharded environments, data is scattered. An aggregation query like `SELECT category, COUNT(*) FROM products GROUP BY category` cannot run in a single step:
1. **Scatter:** The router (or coordinator) sends the query to all shards.
2. **Local Aggregation:** Each shard calculates its local count: `SELECT category, COUNT(*) FROM products GROUP BY category`.
3. **Gather:** The shards return results to the coordinator.
4. **Final Consolidation:** The coordinator aggregates the sub-counts from all shards (`SUM`) and applies the final `HAVING` or `ORDER BY` filters before returning the response.

> 💡 **Interviewer Focus:** Network overhead and memory consumption limits of coordinators during scatter-gather operations.

</details>

<hr/>

### ❓ Q99. **Explain database isolation levels from a formal mathematical perspective.**

<details>
<summary><b>👀 Show Answer</b></summary>

Formally, database transactions are evaluated using **Serialization Graphs (Dependency Graphs)**:
- Transactions are nodes, and conflicts (Read-after-Write, Write-after-Read, Write-after-Write) are directed edges.
- A history of concurrent execution is **Serializable** if and only if its serialization graph contains **no directed cycles**.
- Lower isolation levels permit specific types of cycles by omitting read or write lock constraints:
  - **Read Committed:** Allows cycles containing write-to-read dependencies across uncommitted transactions.
  - **Repeatable Read:** Guarantees no cycles in read-write dependencies, but permits cycles involving read-write dependencies of phantom ranges.

> 💡 **Interviewer Focus:** Mathematical formalization of serializability (conflict serializability vs view serializability).

</details>

<hr/>

### ❓ Q100. **How do columnar databases (like ClickHouse or BigQuery) differ from row-based engines regarding indexing?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Row-Based Databases (OLTP):**
  - Store entire rows contiguously on disk pages.
  - Indexing: Use B-Trees pointing to specific row addresses. Excellent for fast point lookups and updates.
- **Columnar Databases (OLAP):**
  - Store column values contiguously on disk (e.g. all values for `age` are together).
  - Indexing: B-Trees are not used. Instead, they rely on **sorting keys**, **sparse block indexes**, and **min/max indexes** per disk block, along with dictionary compression.
  - Excellent for scanning billions of rows to calculate aggregates across few columns. Point lookups and updates are slow.

> 💡 **Interviewer Focus:** Architectural differences between transaction-optimized (OLTP) and analytics-optimized (OLAP) database engines.

</details>

<hr/>

### 🧭 Navigation

| ⬅️ Previous | 🏠 Index | ➡️ Next |
| :--- | :---: | ---: |
| [⬅️ Khelo Tech Prep](./khelo_tech.md) | [Home](./00_Index.md) | [➡️ MongoDB](./09_MongoDB.md) |
