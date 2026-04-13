# Aggregation Framework

> 📌 **File:** 11_Aggregation_Framework.md | **Level:** SQL Expert → MongoDB

---

## What is it?

The Aggregation Framework is MongoDB's equivalent of SQL's `GROUP BY`, `HAVING`, window functions, subqueries, and CTEs — combined into a **pipeline** of stages. Data flows through stages sequentially, each transforming the result for the next. Think of it as Unix pipes: `data | $match | $group | $sort | $project → result`.

---

## SQL Parallel — Think of it like this

```
SQL:                                    MongoDB Aggregation Stage:
WHERE                                 → $match
GROUP BY                              → $group
HAVING                                → $match (after $group)
SELECT (columns & computed)           → $project / $addFields
ORDER BY                              → $sort
LIMIT / OFFSET                        → $limit / $skip
COUNT / SUM / AVG / MIN / MAX         → $group accumulators
JOIN                                  → $lookup
UNION ALL                             → $unionWith
DISTINCT                              → $group with _id
CASE WHEN                             → $cond / $switch
Subquery / CTE                        → $facet / nested pipeline
CREATE TABLE AS SELECT                → $out / $merge
Window Functions (ROW_NUMBER, etc.)   → $setWindowFields
```

---

## Why this is different from SQL (CRITICAL)

### 1. Pipeline Architecture (Not Set-Based)

```
SQL processes everything at once (declarative):
  SELECT category, AVG(price) FROM products
  WHERE stock > 0 GROUP BY category HAVING AVG(price) > 100
  ORDER BY AVG(price) DESC LIMIT 5;
  
  → Query planner decides execution order

MongoDB processes sequentially (pipeline):
  db.products.aggregate([
    { $match: { stock: { $gt: 0 } } },        // Stage 1: Filter
    { $group: {                                  // Stage 2: Group
        _id: "$category.name",
        avgPrice: { $avg: "$price" }
    }},
    { $match: { avgPrice: { $gt: 100 } } },    // Stage 3: Having
    { $sort: { avgPrice: -1 } },                // Stage 4: Sort
    { $limit: 5 }                               // Stage 5: Limit
  ])
  
  → YOU control execution order (imperative)
```

### 2. Field References Use `$fieldName`

```javascript
// In aggregation, field references are prefixed with $
// This is different from find() queries

// find() — no $ prefix:
db.products.find({ price: { $gt: 100 } })

// aggregate() — $ prefix for field references:
{ $group: { _id: "$category.name", total: { $sum: "$price" } } }
//                ^                              ^
//                Field references use $
```

### 3. Can Transform Document Shape

```javascript
// SQL can only return columns that exist (or computed ones)
// MongoDB aggregation can completely reshape documents

db.products.aggregate([
  { $project: {
    productInfo: {
      title: { $toUpper: "$name" },
      displayPrice: { $concat: ["$", { $toString: "$price" }] }
    },
    isExpensive: { $gt: ["$price", 500] },
    tagCount: { $size: "$tags" }
  }}
])
// Creates entirely new document shapes
```

---

## Syntax — Common Stages

### $match (WHERE)

```javascript
// Always put $match as early as possible — it uses indexes
db.products.aggregate([
  { $match: {
    "category.name": "Electronics",
    price: { $gte: 100, $lte: 1000 },
    stock: { $gt: 0 }
  }}
])
// Uses the same query operators as find()
```

### $group (GROUP BY)

```javascript
// SQL: SELECT category, COUNT(*), AVG(price), SUM(price) FROM products GROUP BY category;
db.products.aggregate([
  { $group: {
    _id: "$category.name",          // GROUP BY field(s)
    count: { $sum: 1 },              // COUNT(*)
    avgPrice: { $avg: "$price" },    // AVG(price)
    totalRevenue: { $sum: "$price" },// SUM(price)
    minPrice: { $min: "$price" },    // MIN(price)
    maxPrice: { $max: "$price" },    // MAX(price)
    brands: { $addToSet: "$brand" }, // ARRAY_AGG(DISTINCT brand)
    products: { $push: "$name" }     // ARRAY_AGG(name)
  }}
])

// Group by multiple fields
db.orders.aggregate([
  { $group: {
    _id: {                          // GROUP BY category, brand
      category: "$category.name",
      brand: "$brand"
    },
    count: { $sum: 1 }
  }}
])

// Group ALL (no GROUP BY — aggregate entire collection)
db.products.aggregate([
  { $group: {
    _id: null,                     // GROUP BY nothing = entire collection
    totalProducts: { $sum: 1 },
    avgPrice: { $avg: "$price" }
  }}
])
```

### $project / $addFields (SELECT)

```javascript
// $project — include/exclude/compute fields
db.products.aggregate([
  { $project: {
    name: 1,
    price: 1,
    discountedPrice: { $multiply: ["$price", 0.9] },      // Computed
    priceRange: {                                           // CASE WHEN
      $switch: {
        branches: [
          { case: { $lt: ["$price", 50] }, then: "Budget" },
          { case: { $lt: ["$price", 200] }, then: "Mid-Range" },
          { case: { $lt: ["$price", 1000] }, then: "Premium" }
        ],
        default: "Luxury"
      }
    }
  }}
])

// $addFields — add new fields without removing existing ones
db.products.aggregate([
  { $addFields: {
    totalValue: { $multiply: ["$price", "$stock"] },
    hasReviews: { $gt: [{ $size: "$reviews" }, 0] }
  }}
])
```

### $sort, $limit, $skip

```javascript
db.products.aggregate([
  { $match: { stock: { $gt: 0 } } },
  { $sort: { price: -1 } },      // ORDER BY price DESC
  { $skip: 20 },                   // OFFSET 20
  { $limit: 10 }                   // LIMIT 10
])
```

### $unwind (Flatten Arrays)

```javascript
// $unwind creates one document per array element
// No direct SQL equivalent — closest is UNNEST / LATERAL JOIN

// Before $unwind:
{ name: "Laptop", tags: ["electronics", "computer", "portable"] }

// After { $unwind: "$tags" }:
{ name: "Laptop", tags: "electronics" }
{ name: "Laptop", tags: "computer" }
{ name: "Laptop", tags: "portable" }

// Use case: Count occurrences of each tag
db.products.aggregate([
  { $unwind: "$tags" },
  { $group: { _id: "$tags", count: { $sum: 1 } } },
  { $sort: { count: -1 } }
])
```

### $facet (Multiple Aggregations in Parallel)

```javascript
// SQL: Multiple queries in one request
// MongoDB: $facet runs multiple pipelines on the same data

db.products.aggregate([
  { $match: { "category.name": "Electronics" } },
  { $facet: {
    // Pipeline 1: Paginated results
    results: [
      { $sort: { price: -1 } },
      { $skip: 0 },
      { $limit: 10 },
      { $project: { name: 1, price: 1, brand: 1 } }
    ],
    // Pipeline 2: Total count
    totalCount: [
      { $count: "count" }
    ],
    // Pipeline 3: Price stats
    priceStats: [
      { $group: {
        _id: null,
        avg: { $avg: "$price" },
        min: { $min: "$price" },
        max: { $max: "$price" }
      }}
    ],
    // Pipeline 4: Brand distribution
    brands: [
      { $group: { _id: "$brand", count: { $sum: 1 } } },
      { $sort: { count: -1 } }
    ]
  }}
])
// Returns all four results in a single database call
```

---

## SQL vs MongoDB — Complex Aggregation Side-by-Side

```sql
-- SQL: Monthly revenue report with customer breakdown
SELECT 
  DATE_TRUNC('month', o.created_at) as month,
  COUNT(DISTINCT o.id) as order_count,
  COUNT(DISTINCT o.customer_id) as customer_count,
  SUM(o.total) as revenue,
  AVG(o.total) as avg_order_value
FROM orders o
WHERE o.created_at >= '2024-01-01'
  AND o.status = 'completed'
GROUP BY DATE_TRUNC('month', o.created_at)
HAVING SUM(o.total) > 10000
ORDER BY month DESC;
```

```javascript
// MongoDB equivalent
db.orders.aggregate([
  // WHERE
  { $match: {
    createdAt: { $gte: new Date("2024-01-01") },
    status: "completed"
  }},
  // GROUP BY month
  { $group: {
    _id: {
      year: { $year: "$createdAt" },
      month: { $month: "$createdAt" }
    },
    orderCount: { $sum: 1 },
    customerCount: { $addToSet: "$customerId" },
    revenue: { $sum: "$total" },
    avgOrderValue: { $avg: "$total" }
  }},
  // HAVING
  { $match: { revenue: { $gt: 10000 } } },
  // Fix customerCount (convert set to count)
  { $addFields: {
    customerCount: { $size: "$customerCount" }
  }},
  // ORDER BY
  { $sort: { "_id.year": -1, "_id.month": -1 } },
  // Reshape output
  { $project: {
    _id: 0,
    month: { $concat: [
      { $toString: "$_id.year" }, "-",
      { $toString: "$_id.month" }
    ]},
    orderCount: 1,
    customerCount: 1,
    revenue: 1,
    avgOrderValue: { $round: ["$avgOrderValue", 2] }
  }}
])
```

---

## Node.js Using MongoDB Driver (REQUIRED)

```javascript
// Dashboard analytics API
app.get('/api/analytics/dashboard', async (req, res) => {
  const db = getDB();
  const { startDate, endDate } = req.query;

  const results = await db.collection('orders').aggregate([
    // Filter by date range
    { $match: {
      status: 'completed',
      createdAt: {
        $gte: new Date(startDate || '2024-01-01'),
        $lte: new Date(endDate || new Date())
      }
    }},
    // Run multiple analyses in parallel
    { $facet: {
      // Revenue by month
      monthlyRevenue: [
        { $group: {
          _id: { $dateToString: { format: '%Y-%m', date: '$createdAt' } },
          revenue: { $sum: { $toDouble: '$total' } },
          orders: { $sum: 1 }
        }},
        { $sort: { _id: 1 } }
      ],
      // Top selling products
      topProducts: [
        { $unwind: '$items' },
        { $group: {
          _id: '$items.productId',
          name: { $first: '$items.name' },
          totalSold: { $sum: '$items.quantity' },
          revenue: { $sum: { $toDouble: '$items.subtotal' } }
        }},
        { $sort: { revenue: -1 } },
        { $limit: 10 }
      ],
      // Revenue by category
      categoryBreakdown: [
        { $unwind: '$items' },
        { $group: {
          _id: '$items.category',
          revenue: { $sum: { $toDouble: '$items.subtotal' } },
          count: { $sum: 1 }
        }},
        { $sort: { revenue: -1 } }
      ],
      // Overall stats
      totals: [
        { $group: {
          _id: null,
          totalRevenue: { $sum: { $toDouble: '$total' } },
          totalOrders: { $sum: 1 },
          avgOrderValue: { $avg: { $toDouble: '$total' } },
          uniqueCustomers: { $addToSet: '$customerId' }
        }},
        { $addFields: { uniqueCustomers: { $size: '$uniqueCustomers' } } }
      ]
    }}
  ]).toArray();

  res.json(results[0]);
});
```

---

## Performance Insight

```
┌──────────────────────────────────────────────────────────────────┐
│  Aggregation Stage    │ Index Usage    │ Memory Limit            │
├───────────────────────┼────────────────┼─────────────────────────┤
│  $match (first)       │ ✅ Uses index  │ N/A                     │
│  $match (later)       │ ❌ No index    │ N/A                     │
│  $sort (first)        │ ✅ Uses index  │ 100MB (in-memory)       │
│  $sort (later)        │ ❌ No index    │ 100MB limit             │
│  $group               │ ❌ No index    │ 100MB limit             │
│  $lookup              │ ✅ On foreign  │ 100MB per doc           │
│  $unwind              │ ❌ No index    │ N/A                     │
│  $facet               │ Varies         │ 100MB per sub-pipeline  │
├───────────────────────┴────────────────┴─────────────────────────┤
│                                                                  │
│  Key rules:                                                      │
│  1. Put $match FIRST — it's the only stage that uses indexes    │
│  2. $sort + $limit together = optimized (top-N)                 │
│  3. 100MB memory limit per stage — use { allowDiskUse: true }   │
│  4. $match → $sort at start = best performance                  │
│                                                                  │
│  db.products.aggregate([...], { allowDiskUse: true })           │
│  // Allows stages to spill to disk for large datasets            │
└──────────────────────────────────────────────────────────────────┘
```

---

## Common Mistakes

### ❌ Putting $match After $group

```javascript
// ❌ Full collection scan, then group, then filter
db.orders.aggregate([
  { $group: { _id: "$status", count: { $sum: 1 } } },
  { $match: { _id: "completed" } }
])

// ✅ Filter first, then group — uses index, processes fewer documents
db.orders.aggregate([
  { $match: { status: "completed" } },
  { $group: { _id: "$status", count: { $sum: 1 } } }
])
```

### ❌ Using $unwind on Large Arrays Without Limiting

```javascript
// ❌ 10K products × 100 reviews each = 1M intermediate documents
db.products.aggregate([
  { $unwind: "$reviews" },
  { $group: { _id: "$reviews.rating", count: { $sum: 1 } } }
])

// ✅ Match first to reduce documents, or use $slice to limit arrays
db.products.aggregate([
  { $match: { "category.name": "Electronics" } },
  { $unwind: "$reviews" },
  { $group: { _id: "$reviews.rating", count: { $sum: 1 } } }
])
```

---

## Practice Exercises

### Exercise 1: Convert SQL to Aggregation
```sql
SELECT brand, COUNT(*) as count, AVG(price) as avg_price
FROM products
WHERE stock > 0
GROUP BY brand
HAVING COUNT(*) > 5
ORDER BY avg_price DESC
LIMIT 10;
```

### Exercise 2: Build a Sales Report
Create an aggregation that produces:
- Total revenue per month for the last 12 months
- Top 5 customers by total spend
- Order count by status
- Average items per order

### Exercise 3: Product Analytics
Build an aggregation that returns for each product category:
- Number of products
- Average rating
- Price range (min, max)
- Most common tags (top 5)

---

## Interview Q&A

**Q1: How does $match differ from find()?**
> `$match` uses the same query syntax as `find()` but operates as a pipeline stage. When `$match` is the FIRST stage, it uses indexes. In later stages, it filters in memory. Always put `$match` first for performance.

**Q2: What is $facet and when should you use it?**
> `$facet` runs multiple aggregation pipelines on the same input data in a single database call. Use it for dashboard queries that need counts, averages, and paginated results simultaneously. Each sub-pipeline gets the same input but produces independent output.

**Q3: What is the 100MB memory limit and how do you handle it?**
> Each aggregation stage has a 100MB RAM limit. Exceeding it throws an error. Solutions: (1) Add `{ allowDiskUse: true }` to spill to disk. (2) Use `$match` early to reduce data. (3) Use `$project` to strip unnecessary fields.

**Q4: How does $unwind handle empty arrays and null values?**
> By default, `$unwind` removes documents with empty arrays or null/missing field. Use `preserveNullAndEmptyArrays: true` to keep them: `{ $unwind: { path: "$tags", preserveNullAndEmptyArrays: true } }`.

**Q5: Can aggregation pipelines use indexes?**
> Only `$match` and `$sort` when they are the FIRST stages (or immediately follow another `$match`). Later stages operate on intermediate results in memory. This is why pipeline ordering is crucial.
