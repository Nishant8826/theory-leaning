# Window Functions (Analytic Functions)

> 📌 **File:** `25_Window_Functions.md` | **Level:** Advanced → MERN Developer

---

## What is it?

A **Window Function** (also known as an **Analytic Function**) performs calculations across a set of table rows that are related to the current row, **without collapsing the rows**.

To understand why this is a superpower, compare it to `GROUP BY`:
* **`GROUP BY`:** Takes 100 rows, groups them by department, and outputs **only 5 summary rows** (one per department). The individual employee rows are destroyed.
* **Window Function (`OVER`):** Keeps all **100 individual employee rows** intact, but appends a calculated summary column (like the department average salary or department sales rank) to every single row.

```sql
SELECT 
    employee_name, 
    department, 
    salary,
    -- Window Function: Appends department average without collapsing rows!
    AVG(salary) OVER(PARTITION BY department) AS dept_avg_salary
FROM employees;
```

---

## MERN Parallel — You Already Know This!

If you do data analysis in MongoDB or Node.js, you usually have to write multi-step loops:

| MongoDB (MERN) | SQL Window Function Equivalent | Description |
| :--- | :--- | :--- |
| MongoDB 5.0+ **`$setWindowFields`** stage | `OVER(PARTITION BY ... ORDER BY ...)` | Performs window-based calculations without reducing documents. |
| Fetch array in Node.js $\rightarrow$ loop with `let runningTotal = 0` | `SUM(amount) OVER(ORDER BY date)` | Calculates running totals directly inside the database engine. |
| Sort in Node.js $\rightarrow$ slice top 3 items per group in JS | `DENSE_RANK() OVER(...)` in CTE $\rightarrow$ `WHERE rnk <= 3` | Finds the Top $N$ records per category in one query. |
| Loop in Node.js checking `array[i - 1]` | `LAG(revenue, 1) OVER(ORDER BY month)` | Fetches previous record's value to calculate month-over-month growth. |

---

## Why does it matter?

* **Preserves Granular Row Detail:** You can display line-item order details alongside customer lifetime value and product category ranks on a single dashboard screen.
* **Solves the "Top N per Group" Problem:** Finding the top 3 best-selling products in every single category is notoriously difficult with standard `GROUP BY`, but takes 5 lines with `DENSE_RANK()`.
* **High-Speed Financial & Trend Analytics:** Compute running ledger balances, 7-day moving averages, and period-over-period percentage growth rates in pure SQL.
* **Eliminates Costly Self-Joins:** Before window functions, calculating running totals required joining a table to itself on `t1.id >= t2.id`, which resulted in an $O(N^2)$ Cartesian explosion. Window functions run in $O(N \log N)$ time.

---

## How does it work?

A Window Function is defined by the **`OVER()`** clause, which can contain up to three components:

```sql
FUNCTION() OVER (
    PARTITION BY group_column    -- 1. How to split the data into windows
    ORDER BY sort_column         -- 2. How to order rows inside each window
    ROWS BETWEEN ... AND ...     -- 3. The sliding frame of rows to include
)
```

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        WINDOW FUNCTION STRUCTURE                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Partition: Tech Department (PARTITION BY department)                  │
│   ┌────────────┬─────────┬──────────────┬────────────────────────────┐  │
│   │ Name       │ Salary  │ ORDER BY     │ Result: Dept Avg Salary    │  │
│   ├────────────┼─────────┼──────────────┼────────────────────────────┤  │
│   │ Alice      │ $120k   │ Highest (1)  │ $110k                      │  │
│   │ Bob        │ $100k   │ Lowest  (2)  │ $110k                      │  │
│   └────────────┴─────────┴──────────────┴────────────────────────────┘  │
│                                                                         │
│   Partition: Sales Department                                           │
│   ┌────────────┬─────────┬──────────────┬────────────────────────────┐  │
│   │ Charlie    │ $90k    │ Highest (1)  │ $80k                       │  │
│   │ David      │ $70k    │ Lowest  (2)  │ $80k                       │  │
│   └────────────┴─────────┴──────────────┴────────────────────────────┘  │
│                                                                         │
│   All 4 rows returned! No rows collapsed!                               │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Complete Taxonomy of Window Functions

---

### 1. Ranking Functions (`ROW_NUMBER`, `RANK`, `DENSE_RANK`, `NTILE`)

Used to order and rank rows within their partitions.

Suppose we have employee salaries:
* Alice: $\$100\text{k}$
* Bob: $\$80\text{k}$
* Charlie: $\$80\text{k}$ (Tie with Bob)
* David: $\$60\text{k}$

| Employee | Salary | `ROW_NUMBER()` | `RANK()` | `DENSE_RANK()` | `NTILE(2)` | Explanation |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Alice** | $\$100\text{k}$ | **1** | **1** | **1** | **1** (Top half) | Highest salary. |
| **Bob** | $\$80\text{k}$ | **2** | **2** | **2** | **1** (Top half) | Tie for 2nd. |
| **Charlie** | $\$80\text{k}$ | **3** | **2** | **2** | **2** (Bottom half) | Tie for 2nd. |
| **David** | $\$60\text{k}$ | **4** | **4** (Skips 3!) | **3** (No skip!) | **2** (Bottom half) | Notice `RANK` skipped 3, while `DENSE_RANK` did not. |

#### SQL Example:
```sql
SELECT 
    name, department, salary,
    ROW_NUMBER() OVER(PARTITION BY department ORDER BY salary DESC) AS seq_num,
    RANK() OVER(PARTITION BY department ORDER BY salary DESC) AS rank_with_skips,
    DENSE_RANK() OVER(PARTITION BY department ORDER BY salary DESC) AS dense_rank_no_skips,
    NTILE(4) OVER(ORDER BY salary DESC) AS salary_quartile
FROM employees;
```

---

### 2. Value / Navigation Functions (`LAG`, `LEAD`, `FIRST_VALUE`, `LAST_VALUE`)

Allows querying values from neighboring rows without self-joins:
* **`LAG(col, N, default)`:** Looks back $N$ rows before the current row.
* **`LEAD(col, N, default)`:** Looks ahead $N$ rows after the current row.
* **`FIRST_VALUE(col)`:** Returns the value from the first row of the window frame.
* **`LAST_VALUE(col)`:** Returns the value from the last row of the window frame.

#### Real-World Example: Month-over-Month (MoM) Growth Calculation
```sql
WITH MonthlySales AS (
    SELECT 
        DATE_FORMAT(order_date, '%Y-%m') AS sale_month,
        SUM(total_amount) AS current_month_revenue
    FROM orders
    GROUP BY sale_month
)
SELECT 
    sale_month,
    current_month_revenue,
    -- Get previous month's revenue
    LAG(current_month_revenue, 1, 0) OVER(ORDER BY sale_month ASC) AS previous_month_revenue,
    -- Calculate Growth Percentage: ((Current - Prev) / Prev) * 100
    ROUND(
        (current_month_revenue - LAG(current_month_revenue, 1, 0) OVER(ORDER BY sale_month ASC)) 
        / NULLIF(LAG(current_month_revenue, 1, 0) OVER(ORDER BY sale_month ASC), 0) * 100, 
        2
    ) AS mom_growth_percent
FROM MonthlySales;
```

---

### 3. Aggregate Window Functions & Sliding Frames

When standard aggregates (`SUM`, `AVG`, `COUNT`, `MIN`, `MAX`) are used with `OVER()`, they compute cumulative or windowed aggregates.

#### Understanding Sliding Window Frames (`ROWS BETWEEN`)
The frame specification controls exactly which surrounding rows are included in the math:

```sql
-- 1. Cumulative Running Total (From start of partition up to current row):
SUM(price) OVER (
    PARTITION BY category 
    ORDER BY id 
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
)

-- 2. 3-Day Moving Average (Previous row + Current row + Next row):
AVG(price) OVER (
    ORDER BY sale_date 
    ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
)

-- 3. Full Partition Total (Entire group):
SUM(price) OVER (
    PARTITION BY category 
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
)
```

```
Sliding Window Frame (3-Day Moving Average):
Row 1: [Row 1, Row 2] ───────────────▶ Average of 2 items
Row 2: [Row 1, Row 2, Row 3] ────────▶ Average of 3 items
Row 3: [Row 2, Row 3, Row 4] ────────▶ Average of 3 items
```

#### ⚠️ Gotcha: `RANGE` vs `ROWS` with Duplicate Values!
* **`ROWS`:** Operates on physical row count offsets. `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` adds values one physical line at a time.
* **`RANGE` (Default when `ORDER BY` is present):** Operates on logical values. If two rows have the **same value** in the `ORDER BY` column (a tie), `RANGE` evaluates all duplicate tied rows simultaneously!
  * *Result:* The running total will jump to the sum of all tied rows on the first duplicate, rather than incrementing line-by-line! Always use `ROWS` if you need strict row-by-row incremental running totals.

#### ⚠️ Gotcha: Why `LAST_VALUE()` Returns the Current Row!
```sql
-- ❌ BUG: Returns the current row's value, NOT the last value in the partition!
SELECT name, salary, LAST_VALUE(salary) OVER(ORDER BY salary) FROM employees;
```
* **Why the bug happens:** When `ORDER BY` is present, the default frame is `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`. The "last value" in a frame that ends at the *current row* is just the current row!
* ✔️ **The Solution:** Explicitly expand the frame to the end of the partition:
  ```sql
  LAST_VALUE(salary) OVER(ORDER BY salary ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
  ```

---

### 4. The Legendary "Gaps & Islands" Problem (FAANG Interview Classic)

**Problem:** Given a table of user login dates, find all consecutive login streaks (islands of consecutive days) and the length of each streak.

```sql
-- Sample table: user_logins (user_id, login_date)
WITH RankedLogins AS (
  -- Step 1: Remove multiple logins on same day & assign sequential row numbers
  SELECT DISTINCT 
    user_id, 
    login_date,
    ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY login_date ASC) AS seq
  FROM user_logins
),
GroupedIslands AS (
  -- Step 2: The Magic Math! (login_date - seq days) produces the EXACT same anchor date for consecutive days!
  SELECT 
    user_id, 
    login_date,
    DATE_SUB(login_date, INTERVAL seq DAY) AS streak_group
  FROM RankedLogins
)
-- Step 3: Group by the streak island to get start date, end date, and streak count!
SELECT 
  user_id,
  MIN(login_date) AS streak_start_date,
  MAX(login_date) AS streak_end_date,
  COUNT(*) AS consecutive_days_streak
FROM GroupedIslands
GROUP BY user_id, streak_group
HAVING COUNT(*) >= 3 -- Filter for streaks of 3+ consecutive days
ORDER BY user_id, streak_start_date;
```

---

### 5. Named Windows (`WINDOW` Clause)

If multiple window functions share the exact same `OVER(PARTITION BY ... ORDER BY ...)` definition, you can clean up your SQL using the `WINDOW` clause at the bottom:

```sql
SELECT 
    name, department, salary,
    ROW_NUMBER() OVER w AS row_num,
    RANK() OVER w AS rnk,
    AVG(salary) OVER w AS avg_sal
FROM employees
WINDOW w AS (PARTITION BY department ORDER BY salary DESC);
```

---

## The Famous "Top N per Group" Pattern

One of the most frequently asked problems in production and SQL interviews is: **"Find the Top 3 highest earning employees in EACH department."**

### ❌ The Common Mistake (Filtering in `WHERE`):
```sql
-- ❌ SYNTAX ERROR! You cannot use a window function directly in WHERE!
SELECT name, department, salary 
FROM employees 
WHERE DENSE_RANK() OVER(PARTITION BY department ORDER BY salary DESC) <= 3;
```
* **Why it fails:** SQL processes `WHERE` **before** window functions are calculated.

### ✔️ The Correct Solution (Wrap with CTE):
```sql
WITH RankedEmployees AS (
    SELECT 
        id, 
        name, 
        department, 
        salary,
        DENSE_RANK() OVER(PARTITION BY department ORDER BY salary DESC) AS rank_position
    FROM employees
)
SELECT id, name, department, salary, rank_position
FROM RankedEmployees
WHERE rank_position <= 3
ORDER BY department, rank_position;
```

---

## Visual Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     RUNNING TOTAL & LAG EXECUTION                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Date         Amount   Running Total (SUM OVER)   LAG(Amount, 1)        │
│  ──────────   ──────   ────────────────────────   ──────────────        │
│  2024-01-01   $100     $100                       NULL (No prev row)    │
│  2024-01-02   $200     $300 ($100 + $200)         $100                  │
│  2024-01-03   $150     $450 ($300 + $150)         $200                  │
│  2024-01-04   $300     $750 ($450 + $300)         $150                  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## MERN vs SQL — Side-by-Side Code

### MongoDB `$setWindowFields` vs SQL Window Function

```javascript
// ============================================
// MongoDB 5.0+ (MERN): $setWindowFields
// ============================================
const analytics = await Order.aggregate([
  {
    $setWindowFields: {
      partitionBy: '$department',
      sortBy: { salary: -1 },
      output: {
        departmentRank: {
          $denseRank: {}
        },
        runningTotal: {
          $sum: '$salary',
          window: { documents: ['unbounded', 'current'] }
        }
      }
    }
  }
]);
```

```sql
-- ============================================
-- MySQL: Window Functions
-- ============================================
SELECT 
  name, department, salary,
  DENSE_RANK() OVER(PARTITION BY department ORDER BY salary DESC) AS departmentRank,
  SUM(salary) OVER(PARTITION BY department ORDER BY salary DESC) AS runningTotal
FROM employees;
```

---

## Real-World Scenario + Full Stack Code

### Express.js Financial Analytics API with `mysql2/promise`

Below is an enterprise API route providing a comprehensive monthly financial report with cumulative revenue, MoM growth rates, and top performers.

```javascript
// server.js
const express = require('express');
const mysql = require('mysql2/promise');

const app = express();
app.use(express.json());

const pool = mysql.createPool({
  host: 'localhost',
  user: 'root',
  password: 'password',
  database: 'ecommerce',
  connectionLimit: 10
});

// GET /api/analytics/monthly-sales-growth
app.get('/api/analytics/monthly-sales-growth', async (req, res) => {
  const query = `
    WITH MonthlyAggregates AS (
      SELECT 
        DATE_FORMAT(order_date, '%Y-%m') AS month_key,
        COUNT(id) AS total_orders,
        SUM(total_amount) AS monthly_revenue
      FROM orders
      WHERE status = 'completed'
      GROUP BY month_key
    )
    SELECT 
      month_key,
      total_orders,
      monthly_revenue,
      -- 1. Cumulative Running Revenue (Year-to-Date style)
      SUM(monthly_revenue) OVER(ORDER BY month_key ASC) AS cumulative_revenue,
      -- 2. Previous Month Revenue via LAG
      LAG(monthly_revenue, 1, 0) OVER(ORDER BY month_key ASC) AS prev_month_revenue,
      -- 3. Percentage Growth Calculation
      ROUND(
        (monthly_revenue - LAG(monthly_revenue, 1, monthly_revenue) OVER(ORDER BY month_key ASC)) 
        / LAG(monthly_revenue, 1, monthly_revenue) OVER(ORDER BY month_key ASC) * 100, 
        2
      ) AS growth_percentage
    FROM MonthlyAggregates
    ORDER BY month_key DESC;
  `;

  try {
    const [results] = await pool.query(query);
    res.json({
      success: true,
      reportGeneratedAt: new Date(),
      data: results
    });
  } catch (err) {
    console.error('Analytics Query Error:', err);
    res.status(500).json({ error: 'Failed to generate financial analytics' });
  }
});

// GET /api/products/top-per-category — Returns Top 3 products in each category
app.get('/api/products/top-per-category', async (req, res) => {
  const query = `
    WITH CategorizedRankings AS (
      SELECT 
        p.id,
        p.name,
        c.name AS category_name,
        p.price,
        p.sales_count,
        DENSE_RANK() OVER(
          PARTITION BY p.category_id 
          ORDER BY p.sales_count DESC, p.price DESC
        ) AS popularity_rank
      FROM products p
      INNER JOIN categories c ON p.category_id = c.id
    )
    SELECT * 
    FROM CategorizedRankings 
    WHERE popularity_rank <= 3
    ORDER BY category_name, popularity_rank;
  `;

  try {
    const [rows] = await pool.query(query);
    res.json({ success: true, count: rows.length, topProducts: rows });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.listen(5000, () => console.log('Analytics Server listening on port 5000'));
```

---

## Impact

| Usage Mistake | What Happens |
| :--- | :--- |
| **Using Window Function in `WHERE` clause** | Query fails instantly with SQL syntax error (must wrap in CTE or derived subquery). |
| **Omitting `ORDER BY` in running totals** | Window defaults to `UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`, returning the static grand total instead of an incremental running sum. |
| **Using `RANK()` instead of `DENSE_RANK()` for pagination** | Missing ranks (e.g. ranks 1, 2, 2, 4) causes pagination gaps when fetching "Top 3". |
| **Computing running totals via JS loops in Node.js** | High network transfer overhead, heavy Node.js memory footprint, and slow response times on large tables. |

---

## Real-World Q&A

### ❓ Q1: When is a Window Function computed in SQL query execution order?
> **💡 Answer:** Window functions are executed **after** `FROM`, `JOIN`, `WHERE`, `GROUP BY`, and `HAVING`, but **before** `DISTINCT`, `ORDER BY`, and `LIMIT`. That is why window functions have access to aggregated groups, but cannot be filtered in `WHERE` or `HAVING` clauses.

### ❓ Q2: What is the default frame when `ORDER BY` is provided vs omitted inside `OVER()`?
> **💡 Answer:**
> * **When `ORDER BY` is present:** The default frame is `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` (computes cumulative running calculations).
> * **When `ORDER BY` is omitted:** The default frame is `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING` (computes the calculation across the entire partition).

### ❓ Q3: How do indexes affect Window Function performance?
> **💡 Answer:** If you have an index matching your window clause `(partition_column, order_column)`, MySQL reads rows directly in sorted partition order without performing an in-memory or disk `filesort` operation, resulting in dramatic $10\times$ to $100\times$ performance speedups.

---

## Interview Q&A

### ❓ Q1: What is the difference between `ROW_NUMBER()`, `RANK()`, and `DENSE_RANK()`?
> **💡 Answer:**
> * **`ROW_NUMBER()`:** Always generates unique, consecutive integer numbers ($1, 2, 3, 4$), regardless of tied values.
> * **`RANK()`:** Assigns identical rank numbers to tied values, but **skips** subsequent ranks ($1, 2, 2, 4$).
> * **`DENSE_RANK()`:** Assigns identical rank numbers to tied values, but **does not skip** subsequent ranks ($1, 2, 2, 3$).

### ❓ Q2: How do you calculate Month-over-Month (MoM) Growth in SQL?
> **💡 Answer:** First, aggregate sales by month inside a CTE. Then, in the outer query, use the `LAG(monthly_revenue, 1)` window function to retrieve the prior month's revenue and compute `((current - lag) / lag) * 100`.

### ❓ Q3: Why can't we use Window Functions directly inside a `WHERE` or `HAVING` clause?
> **💡 Answer:** Because of SQL's logical processing order. The database filters rows using `WHERE` and groups them using `HAVING` *before* evaluating window functions. To filter based on the result of a window function, you must calculate it inside a CTE or subquery first, and then filter the computed column in the outer query's `WHERE` clause.

---

| [← Previous Topic: CTEs & Recursive Queries](./24_CTEs_And_Recursive_Queries.md) | [Index](./00_index.md) | Next: — |
