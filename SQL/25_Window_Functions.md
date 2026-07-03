# Window Functions (Analytic Functions)

> 📌 **File:** `25_Window_Functions.md` | **Level:** Advanced → MERN Developer

---

## What is it?

A **Window Function** performs calculations across a set of table rows that are related to the current row. 

Unlike standard aggregate functions (`SUM`, `COUNT`, `AVG`), which collapse their grouped rows into a single summary row, **window functions do not collapse your rows**. Each row retains its individual identity in the final output, but gains access to calculations made across the "window" of related rows.

Window functions are defined using the `OVER` clause:
```sql
SELECT employee_name, department, salary,
       SUM(salary) OVER(PARTITION BY department) AS department_total
FROM employees;
```

---

## MERN Parallel — You Already Know This!

If you wanted to calculate a running total or a department-wise ranking in a MongoDB/Node.js application, you would typically have to:
1. Load all documents into Node.js.
2. Loop over the documents in JavaScript and maintain aggregate counters (like `let runningTotal = 0;`).
3. Push the results back into a new array.

SQL does all of this directly inside the database query engine in a single step using the `OVER` clause.

---

## Why does it matter?

* **Preserves Row Details:** You can display individual transaction details (like date, amount, user) alongside group summaries (like total monthly sales) in the same row.
* **Simplifies Complex Calculations:** You can compute running totals, moving averages, and month-over-month differences without executing slow self-joins.
* **Allows Advanced Rankings:** Easily find the "top 3 highest-earning employees in each department" or assign ranks to items based on sales scores.

---

## How does it work?

The behavior of a window function is controlled by three components inside the `OVER()` clause:

1. **`PARTITION BY` (Optional):** Splits the table rows into groups (e.g., partition by department). The calculation resets for each group. If omitted, the entire table is treated as one partition.
2. **`ORDER BY` (Optional):** Defines the order of rows inside each partition. This is crucial for calculating sequential items like running totals or rankings.
3. **`ROWS / RANGE` Frame (Optional):** Defines a subset of rows within the partition (e.g., *"the current row and the two preceding rows"*).

---

### 📊 Common Window Functions & Examples

Suppose we have a `products` table:

| id | name | category | price |
| :--- | :--- | :--- | :--- |
| 1 | iPhone | Tech | 1000 |
| 2 | Macbook | Tech | 2000 |
| 3 | iPad | Tech | 1000 |
| 4 | Shirt | Apparel | 50 |
| 5 | Jeans | Apparel | 80 |

---

### 1. Ranking Functions (`ROW_NUMBER`, `RANK`, `DENSE_RANK`)

These functions assign a sequential number to rows within their partitions.

```sql
SELECT name, category, price,
       ROW_NUMBER() OVER(PARTITION BY category ORDER BY price DESC) AS row_num,
       RANK() OVER(PARTITION BY category ORDER BY price DESC) AS rnk,
       DENSE_RANK() OVER(PARTITION BY category ORDER BY price DESC) AS dense_rnk
FROM products;
```

#### Result Output:
| name | category | price | row_num | rnk | dense_rnk | Explanation |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Macbook | Tech | 2000 | 1 | 1 | 1 | Highest Tech product. |
| iPhone | Tech | 1000 | 2 | 2 | 2 | Tie for 2nd place. |
| iPad | Tech | 1000 | 3 | 2 | 2 | Tie for 2nd place. |
| Jeans | Apparel | 80 | 1 | 1 | 1 | Highest Apparel product. |
| Shirt | Apparel | 50 | 2 | 2 | 2 | Lowest Apparel product. |

##### 🔍 Understanding the differences on ties (iPhone vs iPad):
* **`ROW_NUMBER()`:** Never duplicate values. Assigns sequential `2` and `3`.
* **`RANK()`:** Assigns duplicate rank `2` to both, then **skips** the next number. The next item would get rank `4`.
* **`DENSE_RANK()`:** Assigns duplicate rank `2` to both, but **does not skip** the next number. The next item gets rank `3`.

---

### 2. Value Lag and Lead (`LAG` and `LEAD`)

These allow you to fetch data from preceding (`LAG`) or succeeding (`LEAD`) rows relative to the current row. This is perfect for calculating trends like **Month-over-Month growth**.

#### Example: Compare current product price to the next cheaper product in Tech
```sql
SELECT name, price,
       LAG(price, 1) OVER(ORDER BY price DESC) AS previous_higher_price,
       LEAD(price, 1) OVER(ORDER BY price DESC) AS next_lower_price
FROM products
WHERE category = 'Tech';
```

#### Result Output:
| name | price | previous_higher_price | next_lower_price |
| :--- | :--- | :--- | :--- |
| Macbook | 2000 | `NULL` | 1000 |
| iPhone | 1000 | 2000 | 1000 |
| iPad | 1000 | 1000 | `NULL` |

---

### 3. Running Totals (Cumulative Sum)

If you use standard aggregate functions with `OVER(ORDER BY ...)`, they act as cumulative/running operators.

#### Example: Running Total of Product Prices
```sql
SELECT name, price,
       SUM(price) OVER(ORDER BY id) AS running_total
FROM products;
```

#### Result Output:
| name | price | running_total | Calculation |
| :--- | :--- | :--- | :--- |
| iPhone | 1000 | 1000 | $1000$ |
| Macbook | 2000 | 3000 | $1000 + 2000$ |
| iPad | 1000 | 4000 | $3000 + 1000$ |
| Shirt | 50 | 4050 | $4000 + 50$ |
| Jeans | 80 | 4130 | $4050 + 80$ |

---

## Common Pitfalls & Gotchas

### ⚠️ Gotcha #1: You cannot filter Window Functions in a `WHERE` clause!
If you try to run:
```sql
-- ❌ This will throw a syntax error!
SELECT name, ROW_NUMBER() OVER(ORDER BY price DESC) AS rnk 
FROM products 
WHERE ROW_NUMBER() OVER(ORDER BY price DESC) = 1;
```
* **Why?** In SQL's execution phase, the `WHERE` clause runs **before** the window function runs. You cannot filter by a column that has not been calculated yet.
* **✔️ The Solution (Use a CTE):**
  ```sql
  WITH RankedProducts AS (
      SELECT name, price, ROW_NUMBER() OVER(ORDER BY price DESC) AS rnk 
      FROM products
  )
  SELECT * FROM RankedProducts WHERE rnk = 1;
  ```

### ⚠️ Gotcha #2: Performance Cost
Window functions require sorting data on the fly. If you run a window query over millions of rows without appropriate indexes on the `PARTITION BY` and `ORDER BY` columns, your query will slow down significantly.
