# Common Table Expressions (CTEs) & Recursive Queries

> 📌 **File:** `24_CTEs_And_Recursive_Queries.md` | **Level:** Advanced → MERN Developer

---

## What is it?

A **Common Table Expression (CTE)** is a temporary, named result set that exists only during the execution of a single SQL statement (`SELECT`, `INSERT`, `UPDATE`, or `DELETE`). 

Think of a CTE as a **clean, readable, top-level variable in SQL** that stores intermediate query results.

```sql
WITH HighEarners AS (
    SELECT id, name, department_id, salary 
    FROM employees 
    WHERE salary > 100000
)
SELECT * FROM HighEarners WHERE department_id = 5;
```

When taken to the advanced level, **Recursive CTEs** allow a query to reference *itself*, enabling you to traverse complex hierarchical trees (like org charts, nested category trees, and bill of materials) and graphs (like social connections) that were previously impossible in standard SQL without writing complex stored procedure loops.

---

## MERN Parallel — You Already Know This!

If you build aggregation pipelines in MongoDB or traverse graphs with `$graphLookup`, CTEs map directly to your mental model:

| MongoDB (MERN) | SQL CTE Equivalent | Purpose |
| :--- | :--- | :--- |
| Aggregation Pipeline Stage 1 (`$match`) | `WITH filtered_data AS (SELECT ...)` | Isolates and filters intermediate datasets. |
| Aggregation Pipeline Stage 2 (`$group`) | `, grouped_data AS (SELECT ... FROM filtered_data)` | Chains sequential calculations step-by-step. |
| **`$graphLookup`** stage | **`WITH RECURSIVE`** | Recursively traverses parent-child document relationships. |
| JavaScript `while` / `for` loop in Node.js | SQL Recursive Query Engine | Traverses tree depths inside the database engine without sending data back and forth to Node.js. |

---

## Why does it matter?

* **Kills Nested Subquery "Callback Hell":** In traditional SQL, complex subqueries are nested inside out, forcing you to read from the deepest parenthesis outward. CTEs let you write modular queries from top to bottom.
* **Reusable Intermediate Datasets:** If a subquery needs to be joined multiple times within the same query, a CTE lets you define it once rather than duplicating subquery text.
* **Native Tree & Graph Traversal:** In applications like e-commerce category breadcrumbs (`Electronics > Computers > Laptops > Gaming Laptops`) or comment threads (Reddit/HN style nested replies), Recursive CTEs fetch entire nested trees in a single database query.
* **Massive Performance Boost over Node.js Loops:** Fetching a 10-level hierarchy via recursive SQL takes $\approx 2\text{ms}$ in a single query, compared to making 10 sequential API-to-database network round-trips in Node.js.

---

## How does it work?

---

### 1. Non-Recursive CTEs (Chaining & Modularity)

You can define multiple CTEs in a single query by separating them with commas. Each subsequent CTE can reference any CTE defined before it!

```sql
WITH 
  MonthlySales AS (
    -- CTE 1: Aggregate monthly totals
    SELECT 
      DATE_FORMAT(order_date, '%Y-%m') AS sale_month,
      SUM(total_amount) AS revenue
    FROM orders
    GROUP BY sale_month
  ),
  AverageRevenue AS (
    -- CTE 2: Calculate average of the monthly totals from CTE 1
    SELECT AVG(revenue) AS avg_monthly_revenue
    FROM MonthlySales
  )
-- Main Query: Compare monthly sales to overall average
SELECT 
  ms.sale_month,
  ms.revenue,
  ar.avg_monthly_revenue,
  (ms.revenue - ar.avg_monthly_revenue) AS variance
FROM MonthlySales ms
CROSS JOIN AverageRevenue ar
ORDER BY ms.sale_month DESC;
```

#### Under-the-Hood: CTE Inlining vs Materialization
* **Inlining (Query Rewrite):** In MySQL 8.0, the optimizer often merges non-recursive CTEs directly into the main query AST (Abstract Syntax Tree), applying index filters seamlessly.
* **Materialization:** If a CTE is referenced multiple times, the query optimizer may materialize the CTE into an internal in-memory temporary table to avoid re-executing the subquery calculation.

---

### 🔄 2. Recursive CTEs (Tree & Graph Traversal)

A Recursive CTE is declared using `WITH RECURSIVE` and consists of three core components:

```sql
WITH RECURSIVE CTE_Name AS (
    -- 1. ANCHOR MEMBER (Base Case): Executes once to get the starting row(s)
    SELECT initial_columns FROM table WHERE parent_id IS NULL

    UNION ALL

    -- 2. RECURSIVE MEMBER (Recursive Step): Joins the CTE back to the base table
    SELECT child_columns FROM table JOIN CTE_Name ON table.parent_id = CTE_Name.id
)
-- 3. TERMINATION: Recursion automatically terminates when the recursive member returns 0 rows!
SELECT * FROM CTE_Name;
```

#### The Internal Execution Cycle Step-by-Step:

```
Step 1: Execute ANCHOR query ──▶ Produces R0 (Base Rows, e.g. Root Level 1)
                                      │
Step 2: Execute RECURSIVE query using R0 ──▶ Produces R1 (Level 2 Children)
                                      │
Step 3: Execute RECURSIVE query using R1 ──▶ Produces R2 (Level 3 Children)
                                      │
Step 4: Execute RECURSIVE query using R2 ──▶ Produces R3 (Empty Set Ø)
                                      │
Step 5: Engine unions all sets [R0 ∪ R1 ∪ R2] and returns final output to client!
```

---

## Real-World Practical Use Cases

### Use Case 1: E-Commerce Category Breadcrumbs & Ancestry Tree

Suppose we have a hierarchical `categories` table:

| id | name | parent_id |
| :--- | :--- | :--- |
| 1 | Electronics | NULL |
| 2 | Computers | 1 |
| 3 | Laptops | 2 |
| 4 | Gaming Laptops | 3 |

#### Query: Build Full Breadcrumb Path for Every Category
```sql
WITH RECURSIVE CategoryPath AS (
    -- Anchor: Start with root categories (parent_id IS NULL)
    SELECT 
        id, 
        name, 
        parent_id, 
        1 AS depth, 
        CAST(name AS CHAR(1000)) AS breadcrumb
    FROM categories
    WHERE parent_id IS NULL

    UNION ALL

    -- Recursive Step: Join child categories to parent path
    SELECT 
        c.id, 
        c.name, 
        c.parent_id, 
        cp.depth + 1, 
        CONCAT(cp.breadcrumb, ' > ', c.name)
    FROM categories c
    INNER JOIN CategoryPath cp ON c.parent_id = cp.id
)
SELECT id, name, depth, breadcrumb 
FROM CategoryPath 
ORDER BY breadcrumb;
```

#### Query Result:
| id | name | depth | breadcrumb |
| :--- | :--- | :--- | :--- |
| 1 | Electronics | 1 | Electronics |
| 2 | Computers | 2 | Electronics > Computers |
| 3 | Laptops | 3 | Electronics > Computers > Laptops |
| 4 | Gaming Laptops | 4 | Electronics > Computers > Laptops > Gaming Laptops |

---

### Use Case 2: Bill of Materials (BOM) & Inventory Assembly

In manufacturing and gaming inventory, an assembled item (e.g., a "Bicycle") is made of sub-components (Frame, Wheels), which are made of raw materials (Steel, Rubber).

```sql
WITH RECURSIVE ComponentExplosion AS (
    -- Anchor: The finished product
    SELECT 
        assembly_id, 
        component_id, 
        quantity,
        1 AS level
    FROM bill_of_materials
    WHERE assembly_id = 'BICYCLE'

    UNION ALL

    -- Recursive Member: Sub-components
    SELECT 
        bom.assembly_id, 
        bom.component_id, 
        bom.quantity * ce.quantity, -- Multiplies component quantities down the tree
        ce.level + 1
    FROM bill_of_materials bom
    INNER JOIN ComponentExplosion ce ON bom.assembly_id = ce.component_id
)
SELECT * FROM ComponentExplosion;
```

---

## Preventing Infinite Loops & Cycle Detection

If your data contains circular references (e.g. Employee A manages Employee B, and Employee B manages Employee A):
* A recursive CTE will loop infinitely until memory is exhausted or the database hits its recursion safety limit.

### Safety Guards in MySQL:

1. **System Recursion Limit:**
   MySQL enforces a safeguard variable `cte_max_recursion_depth` (default is 1000 iterations). If a query exceeds this, it terminates with an error:
   ```sql
   SET SESSION cte_max_recursion_depth = 500; -- Configurable limit
   ```

2. **Cycle Detection using Path Tracking:**
   You can track visited IDs in a string and stop recursion if an ID is encountered twice:
   ```sql
   WITH RECURSIVE OrgGraph AS (
       SELECT id, manager_id, name, CAST(id AS CHAR(200)) AS path
       FROM employees WHERE manager_id IS NULL
       
       UNION ALL
       
       SELECT e.id, e.manager_id, e.name, CONCAT(og.path, ',', e.id)
       FROM employees e
       INNER JOIN OrgGraph og ON e.manager_id = og.id
       WHERE og.path NOT LIKE CONCAT('%', e.id, '%') -- Stops circular recursion!
   )
   SELECT * FROM OrgGraph;
   ```

---

## 🧭 Graph Traversal & Shortest Path (Flight / Network Routing)

Beyond simple trees, Recursive CTEs can solve graph shortest-path problems (Dijkstra-style traversal directly in SQL):

```sql
-- Schema: Directed Flights between Airports with cost
-- flights (origin VARCHAR(3), destination VARCHAR(3), cost INT)

WITH RECURSIVE FlightPaths AS (
    -- 1. Anchor: Direct flights departing from 'DEL' (Delhi)
    SELECT 
        origin, 
        destination, 
        cost AS total_cost, 
        1 AS stops, 
        CAST(CONCAT(origin, ' -> ', destination) AS CHAR(500)) AS route,
        CAST(CONCAT(',', origin, ',', destination, ',') AS CHAR(500)) AS visited
    FROM flights
    WHERE origin = 'DEL'

    UNION ALL

    -- 2. Recursive Member: Connect connecting flights avoiding circular loops
    SELECT 
        fp.origin, 
        f.destination, 
        fp.total_cost + f.cost, 
        fp.stops + 1, 
        CONCAT(fp.route, ' -> ', f.destination),
        CONCAT(fp.visited, f.destination, ',')
    FROM FlightPaths fp
    INNER JOIN flights f ON fp.destination = f.origin
    WHERE fp.visited NOT LIKE CONCAT('%,', f.destination, ',%') -- Loop Prevention Guard
      AND fp.stops < 4 -- Max 4 hops
)
-- Find the cheapest route to London ('LHR')
SELECT route, stops, total_cost 
FROM FlightPaths 
WHERE destination = 'LHR' 
ORDER BY total_cost ASC 
LIMIT 1;
```

---

## 🏛️ System Design Comparison: 4 Ways to Model Hierarchies in SQL

In technical architecture interviews, you will often be asked: *"What are the tradeoffs of modeling hierarchical trees in relational databases?"*

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 HIERARCHICAL DATA MODELING TRADEOFF MATRIX                                  │
├────────────────────┬────────────────────┬──────────────────┬─────────────────┬──────────────────────────────┤
│ Strategy           │ Read Tree Speed    │ Insert/Move Cost │ Storage Size    │ Ideal Use Case               │
├────────────────────┼────────────────────┼──────────────────┼─────────────────┼──────────────────────────────┤
│ 1. Adjacency List  │ Fast with CTE      │ 🟢 O(1) Fast     │ 🟢 Minimal      │ Default choice for most apps │
│    (`parent_id`)   │ (Recursive scan)   │ (Change 1 ID)    │ (1 column)      │ (Org charts, file systems)   │
├────────────────────┼────────────────────┼──────────────────┼─────────────────┼──────────────────────────────┤
│ 2. Materialized    │ 🟢 O(1) Fast       │ 🟡 Moderate      │ 🟡 Moderate     │ E-commerce category paths    │
│    Path (`/1/4/9`) │ (`LIKE '/1/4/%'`)  │ (Update strings) │ (String column) │ & breadcrumbs                │
├────────────────────┼────────────────────┼──────────────────┼─────────────────┼──────────────────────────────┤
│ 3. Closure Table   │ 🟢 O(1) Ultra-Fast │ 🔴 Heavy         │ 🔴 High         │ Read-heavy deep graphs       │
│    (Bridge Table)  │ (Direct JOIN)      │ (Insert N pairs) │ (O(N²) rows)    │ (Tag hierarchies, permissions)│
├────────────────────┼────────────────────┼──────────────────┼─────────────────┼──────────────────────────────┤
│ 4. Nested Sets     │ 🟢 O(1) Fast Range │ 🔴 Terrible      │ 🟢 Minimal      │ Static, read-only catalogs   │
│    (`lft`, `rgt`)  │ (`BETWEEN l & r`)  │ (Re-indexes all) │ (2 integers)    │ that NEVER change            │
└────────────────────┴────────────────────┴──────────────────┴─────────────────┴──────────────────────────────┘
```

---

## Visual Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    RECURSIVE CTE TREE TRAVERSAL FLOW                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   [Level 1: CEO (id: 1, manager_id: NULL)]    ◀── ANCHOR MEMBER         │
│             │                                                           │
│             ├──▶ [Level 2: VP Eng (id: 2, manager_id: 1)] ◀── PASS 1    │
│             │          │                                                │
│             │          └──▶ [Level 3: Lead (id: 4, mgr: 2)] ◀── PASS 2  │
│             │                     │                                     │
│             │                     └──▶ [Level 4: Dev (id: 6)] ◀── PASS 3│
│             │                                                           │
│             └──▶ [Level 2: VP Sales (id: 3, manager_id: 1)] ◀── PASS 1  │
│                        │                                                │
│                        └──▶ [Level 3: Rep (id: 5, mgr: 3)] ◀── PASS 2   │
│                                                                         │
│   When PASS 4 produces 0 children ──▶ STOP & RETURN COMPLETE TREE       │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## MERN vs SQL — Side-by-Side Code

### MongoDB `$graphLookup` vs SQL Recursive CTE

```javascript
// ============================================
// MongoDB (MERN): $graphLookup Aggregation
// ============================================
const categoryTree = await Category.aggregate([
  { $match: { name: 'Electronics' } },
  {
    $graphLookup: {
      from: 'categories',
      startWith: '$_id',
      connectFromField: '_id',
      connectToField: 'parentId',
      as: 'allSubcategories',
      maxDepth: 5,
      depthField: 'depthLevel'
    }
  }
]);
```

```sql
-- ============================================
-- MySQL: Recursive CTE
-- ============================================
WITH RECURSIVE CategoryTree AS (
  SELECT id, name, parent_id, 0 AS depthLevel
  FROM categories
  WHERE name = 'Electronics'
  
  UNION ALL
  
  SELECT c.id, c.name, c.parent_id, ct.depthLevel + 1
  FROM categories c
  INNER JOIN CategoryTree ct ON c.parent_id = ct.id
  WHERE ct.depthLevel < 5
)
SELECT * FROM CategoryTree;
```

---

## ORM Equivalent (Sequelize / Prisma)

Standard ORM query builders (like Sequelize `.findAll()` or Prisma `findMany`) cannot express recursive loops natively without sending multiple SQL queries. In production, you execute Recursive CTEs using raw queries:

```javascript
// Sequelize Raw Recursive CTE Query
const [categories] = await sequelize.query(`
  WITH RECURSIVE SubTree AS (
    SELECT id, name, parent_id FROM categories WHERE id = :rootId
    UNION ALL
    SELECT c.id, c.name, c.parent_id 
    FROM categories c 
    INNER JOIN SubTree st ON c.parent_id = st.id
  )
  SELECT * FROM SubTree;
`, {
  replacements: { rootId: req.params.id },
  type: sequelize.QueryTypes.SELECT
});
```

---

## Real-World Scenario + Full Stack Code

### Express.js Hierarchical Category Tree API (`mysql2/promise`)

Below is a complete Express endpoint that fetches an entire category sub-tree and formats it into a nested JSON structure in Node.js:

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

// Helper: Convert flat recursive SQL rows into a nested JSON Tree
function buildNestedTree(items, rootParentId = null) {
  const map = {};
  const tree = [];

  items.forEach(item => {
    map[item.id] = { ...item, children: [] };
  });

  items.forEach(item => {
    if (item.parent_id === rootParentId || item.parent_id === null) {
      tree.push(map[item.id]);
    } else if (map[item.parent_id]) {
      map[item.parent_id].children.push(map[item.id]);
    }
  });

  return tree;
}

// GET /api/categories/:id/tree — Returns category and all nested children
app.get('/api/categories/:id/tree', async (req, res) => {
  const rootCategoryId = parseInt(req.params.id, 10);

  const query = `
    WITH RECURSIVE CategoryBranch AS (
      -- 1. Anchor: Start with the requested category
      SELECT id, name, parent_id, slug, 0 AS depth
      FROM categories
      WHERE id = ?

      UNION ALL

      -- 2. Recursive Member: Fetch all children at any depth
      SELECT c.id, c.name, c.parent_id, c.slug, cb.depth + 1
      FROM categories c
      INNER JOIN CategoryBranch cb ON c.parent_id = cb.id
    )
    SELECT * FROM CategoryBranch ORDER BY depth ASC, name ASC;
  `;

  try {
    const [rows] = await pool.query(query, [rootCategoryId]);

    if (rows.length === 0) {
      return res.status(404).json({ error: 'Category not found' });
    }

    // Convert SQL flat relational rows to nested JSON
    const nestedResult = buildNestedTree(rows, rows[0].parent_id);

    res.json({
      success: true,
      totalCount: rows.length,
      data: nestedResult
    });
  } catch (err) {
    console.error('CTE Query Error:', err);
    res.status(500).json({ error: 'Database query failed' });
  }
});

app.listen(5000, () => console.log('Category Tree API running on port 5000'));
```

---

## Impact

| Implementation Choice | What Happens |
| :--- | :--- |
| **Writing nested subqueries instead of CTEs** | Unreadable "SQL spaghetti", hard to debug, difficult to maintain in production. |
| **Recursive query without a cycle detection guard** | Endless loop freezing database connections until `cte_max_recursion_depth` triggers an error. |
| **Using `UNION` instead of `UNION ALL` in Recursive CTEs** | Slow execution because the engine runs duplicate-elimination hashing on every single recursion step. |
| **Traversing trees using Node.js loops ($N$ queries)** | Catastrophic N+1 network latency delays (10 DB roundtrips vs 1 CTE roundtrip). |

---

## Real-World Q&A

### ❓ Q1: Is a CTE temporary table stored on disk?
> **💡 Answer:** In MySQL 8.0, CTEs are typically computed in-memory. If a CTE is non-recursive and simple, the optimizer inlines it directly into the outer query without creating any temporary table. If intermediate results exceed `tmp_table_size` or contain blobs, the database temporarily spills rows to internal memory or temporary disk files, and automatically drops them immediately when query execution finishes.

### ❓ Q2: What is the difference between `UNION` and `UNION ALL` in recursive CTEs?
> **💡 Answer:** `UNION ALL` preserves all rows without running duplicate-checking algorithms. `UNION` removes duplicate rows at every recursion pass, which incurs a heavy performance penalty. In 99% of recursive hierarchies (like trees), relationships are strictly hierarchical with no duplicate child IDs, so `UNION ALL` is standard best practice.

### ❓ Q3: Can I use a CTE with `UPDATE` or `DELETE` statements?
> **💡 Answer:** Yes! In MySQL 8.0+, you can use CTEs with DML operations:
> ```sql
> WITH ExpiredUsers AS (
>   SELECT id FROM users WHERE last_login < DATE_SUB(NOW(), INTERVAL 2 YEAR)
> )
> DELETE u FROM users u 
> INNER JOIN ExpiredUsers eu ON u.id = eu.id;
> ```

---

## Interview Q&A

### ❓ Q1: What is a Common Table Expression (CTE) and how does it differ from a Database View?
> **💡 Answer:** 
> * A **CTE** is temporary and exists only for the duration of a single query. It is not saved in the database catalog.
> * A **View** is a permanent database object (a saved query definition) stored in the database schema that can be reused across different queries and sessions.

### ❓ Q2: Explain the structure of a Recursive CTE. What are the essential components?
> **💡 Answer:** A Recursive CTE consists of:
> 1. An **Anchor Member:** The initial `SELECT` that provides the base result set (e.g., finding the root parent where `parent_id IS NULL`).
> 2. A **Set Operator:** `UNION ALL` (or `UNION`).
> 3. A **Recursive Member:** A `SELECT` that references the CTE name itself, joining it to the source table to find the next generation of children.
> 4. A **Termination Condition:** When the recursive member produces an empty result set, the engine halts execution.

### ❓ Q3: How do you handle circular reference traps in recursive queries?
> **💡 Answer:** 
> 1. Set the session variable `cte_max_recursion_depth` to a reasonable threshold to prevent infinite runaway queries.
> 2. Track visited nodes in a string column (e.g. `CONCAT(path, ',', id)`) and add a `WHERE path NOT LIKE CONCAT('%', id, '%')` filter in the recursive member.

### ❓ Q4: How does the query optimizer treat CTEs vs Temporary Tables or Subqueries? What is an "Optimization Barrier / Fence"?
> **💡 Answer:** In older versions of engines like PostgreSQL (<12), CTEs acted as rigid **optimization fences / barriers**, meaning the database materialized the CTE independently in memory before outer WHERE filters could be pushed down into it (preventing index usage). In modern MySQL (8.0+) and PostgreSQL (12+), non-recursive CTEs are **inlined by default** — the optimizer merges the CTE into the main query tree, allowing predicate pushdown and index usage just like standard derived tables.

### ❓ Q5: You are designing an e-commerce category tree with 1,000,000 product categories and fast read requirements. Which schema design pattern would you choose?
> **💡 Answer:** If reads dominate and category paths rarely move, a **Materialized Path** (storing `/1/4/19/` in a column with a prefix index) or **Closure Table** (a separate ancestor-descendant bridge table) provides $O(1)$ direct retrieval without recursion overhead. If categories frequently change parent hierarchies, an **Adjacency List** (`parent_id`) with a **Recursive CTE** provides the optimal balance between $O(1)$ fast writes and sub-millisecond recursive reads.

---

| [← Previous Topic: Database Sharding & Partitioning](./23_Sharding_And_Partitioning.md) | [Index](./00_index.md) | [Next: Window Functions →](./25_Window_Functions.md) |

