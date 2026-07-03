# Common Table Expressions (CTEs) & Recursive Queries

> 📌 **File:** `24_CTEs_And_Recursive_Queries.md` | **Level:** Advanced → MERN Developer

---

## What is it?

A **Common Table Expression (CTE)** is a temporary result set that you can name and reference within a single `SELECT`, `INSERT`, `UPDATE`, or `DELETE` query. 

Think of a CTE as a **temporary variable** that holds the result of a subquery. It exists only while that specific query is executing, and then it is immediately destroyed.

Standard CTEs are created using the `WITH` keyword:
```sql
WITH MyTemporaryTable AS (
    SELECT id, name, salary FROM employees WHERE salary > 50000
)
SELECT * FROM MyTemporaryTable; -- We query it just like a normal table!
```

---

## MERN Parallel — You Already Know This!

If you've written aggregation pipelines in MongoDB, you are already familiar with the mental model of CTEs:

| MongoDB Aggregation Stage (You Know) | SQL CTE Equivalent (You'll Learn) | Description |
| :--- | :--- | :--- |
| **Pipeline Stage 1:** `{ $match: { status: 'Active' } }` | `WITH active_users AS (SELECT ...)` | Creates a named, filtered, intermediate set of data. |
| **Pipeline Stage 2:** `{ $group: { _id: '$city', total: { $sum: '$sales' } } }` | `, city_sales AS (SELECT city, SUM(...) ...)` | Groups/aggregates that intermediate set, feeding it to the next step. |
| **Final Pipeline Output:** | `SELECT * FROM city_sales JOIN active_users ...` | Combines and filters the final result set. |

In MongoDB, you pass documents through stages from top to bottom. In SQL, CTEs allow you to do the exact same thing, flattening complex nested queries into sequential blocks.

---

## Why does it matter?

* **Eliminates Query "Callback Hell":** Standard subqueries force you to write nested code from the inside out (which is hard to read). CTEs let you write queries from top to bottom.
* **Avoids Code Duplication:** If you need to use the same subquery data multiple times in a query (e.g., joining it twice), you can define it once as a CTE and query it multiple times.
* **Enables Hierarchical Traversal:** Standard SQL cannot easily query self-referential trees (like parent/child categories, or employees and managers). **Recursive CTEs** allow you to traverse these loops easily.

---

## How does it work?

---

### 1. The Standard CTE (Improving Readability)

Imagine you want to find all departments where the total salary expense is greater than the company's average department salary expense.

#### ❌ The Hard-to-Read Way (Nested Subqueries)
```sql
SELECT department_id, SUM(salary) 
FROM employees 
GROUP BY department_id
HAVING SUM(salary) > (
    SELECT AVG(dept_sum) FROM (
        SELECT SUM(salary) AS dept_sum 
        FROM employees 
        GROUP BY department_id
    ) AS temp
);
```

#### ✔️ The Readable Way (Using CTEs)
You can define the intermediate calculations at the top:
```sql
WITH DepartmentSalaries AS (
    -- CTE 1: Calculate total salary per department
    SELECT department_id, SUM(salary) AS total_salary
    FROM employees
    GROUP BY department_id
),
CompanyAverage AS (
    -- CTE 2: Calculate average department salary using CTE 1
    SELECT AVG(total_salary) AS avg_salary
    FROM DepartmentSalaries
)
-- Main Query: Query the CTEs directly
SELECT * 
FROM DepartmentSalaries
WHERE total_salary > (SELECT avg_salary FROM CompanyAverage);
```

---

### 🔄 2. Recursive CTEs (Tree Traversal)

A **Recursive CTE** is a query that references itself. It is used to query hierarchical data (e.g., an organization chart where employees report to managers, who report to directors).

A recursive CTE has two parts:
1. **Anchor Member:** The starting point of the recursion (e.g., the CEO who has no manager).
2. **Recursive Member:** The query that joins the CTE back to the base table to fetch the next level down (e.g., employees who report to the current level).

#### Organization Tree Example
Suppose you have an `employees` table:

| id | name | manager_id |
| :--- | :--- | :--- |
| 1 | Alice (CEO) | NULL |
| 2 | Bob (Manager) | 1 |
| 3 | Charlie (Developer) | 2 |
| 4 | David (Developer) | 2 |

To build the org chart hierarchy:
```sql
WITH RECURSIVE OrgChart AS (
    -- 1. Anchor Member: Start with the CEO
    SELECT id, name, manager_id, 1 AS level
    FROM employees
    WHERE manager_id IS NULL
    
    UNION ALL
    
    -- 2. Recursive Member: Join employees to their managers in the OrgChart CTE
    SELECT e.id, e.name, e.manager_id, oc.level + 1
    FROM employees e
    JOIN OrgChart oc ON e.manager_id = oc.id
)
SELECT * FROM OrgChart;
```

##### How it executes step-by-step:
1. **Step 1 (Anchor):** Finds `Alice` (level 1).
2. **Step 2 (First Recursion):** Finds employees reporting to Alice $\rightarrow$ `Bob` (level 2).
3. **Step 3 (Second Recursion):** Finds employees reporting to Bob $\rightarrow$ `Charlie` and `David` (level 3).
4. **Step 4 (Third Recursion):** Finds employees reporting to Charlie or David $\rightarrow$ returns empty set. Recursion stops.

---

## Common Pitfalls & Gotchas

* **Infinite Loops in Recursion:** If your hierarchy data has a circular reference (e.g., Employee A reports to Employee B, who reports to Employee A), a recursive CTE will loop forever and freeze.
  * *Fix:* Use `LIMIT` or constraints in your table to prevent circular reporting relationships.
* **Performance Limitations:** In some SQL database engines (older versions), CTE results are not cached/materialized. If you query a CTE three times in your main query, the database might calculate the subquery three times. 
  * *Tip:* In PostgreSQL 12+, you can control this using `WITH cte_name AS MATERIALIZED (...)` to force caching.
* **Naming Collisions:** A CTE creates a temporary table namespace. Ensure your CTE name does not collide with actual table names in your database.
