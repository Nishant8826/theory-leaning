# Query Operators

> 📌 **File:** 08_Query_Operators.md | **Level:** SQL Expert → MongoDB

---

## What is it?

MongoDB query operators are the building blocks of filter expressions — they replace SQL's `WHERE` clause syntax. Instead of `WHERE price > 100 AND stock > 0`, you write `{ price: { $gt: 100 }, stock: { $gt: 0 } }`. The operator vocabulary is different, but the logic is identical.

---

## SQL Parallel — Complete Operator Map

### Comparison Operators

```
┌────────────────────┬─────────────────────────┬────────────────────────────┐
│ SQL                │ MongoDB                 │ Example                    │
├────────────────────┼─────────────────────────┼────────────────────────────┤
│ = value            │ { field: value }        │ { age: 25 }               │
│ != / <>            │ { field: { $ne: v } }   │ { status: { $ne: "done" }}│
│ >                  │ { field: { $gt: v } }   │ { price: { $gt: 100 } }   │
│ >=                 │ { field: { $gte: v } }  │ { age: { $gte: 18 } }     │
│ <                  │ { field: { $lt: v } }   │ { stock: { $lt: 10 } }    │
│ <=                 │ { field: { $lte: v } }  │ { rating: { $lte: 3 } }   │
│ IN (a, b, c)       │ { field: { $in: [] } }  │ { brand: { $in: ["A","B"]}}│
│ NOT IN (a, b, c)   │ { field: { $nin: [] } } │ { status:{$nin:["x","y"]}}│
│ BETWEEN a AND b    │ { $gte: a, $lte: b }    │ { price:{$gte:10,$lte:50}}│
│ IS NULL            │ { field: null }          │ { discount: null }        │
│ IS NOT NULL         │ { field: { $ne: null } }│ { email: { $ne: null } }  │
└────────────────────┴─────────────────────────┴────────────────────────────┘
```

### Logical Operators

```
┌──────────────────────┬──────────────────────────────────────────────┐
│ SQL                  │ MongoDB                                      │
├──────────────────────┼──────────────────────────────────────────────┤
│ AND                  │ Implicit (multiple fields in same object)     │
│                      │ Explicit: { $and: [{...}, {...}] }           │
│ OR                   │ { $or: [{...}, {...}] }                      │
│ NOT                  │ { field: { $not: { $gt: 100 } } }           │
│ NOR (NOT OR)         │ { $nor: [{...}, {...}] }                     │
│ EXISTS (subquery)    │ { field: { $exists: true } }                │
└──────────────────────┴──────────────────────────────────────────────┘
```

### Element Operators

```
┌──────────────────────┬──────────────────────────────────────────────┐
│ SQL Concept          │ MongoDB                                      │
├──────────────────────┼──────────────────────────────────────────────┤
│ IS NULL / col exists │ { field: { $exists: true/false } }          │
│ TYPEOF / CAST        │ { field: { $type: "string" } }             │
│ (no equivalent)      │ { field: { $type: ["string", "number"] } } │
└──────────────────────┴──────────────────────────────────────────────┘
```

### Pattern Matching

```
┌────────────────────────┬──────────────────────────────────────────┐
│ SQL                    │ MongoDB                                  │
├────────────────────────┼──────────────────────────────────────────┤
│ LIKE '%value%'         │ { field: /value/i }                      │
│ LIKE 'value%'          │ { field: /^value/ }                      │
│ LIKE '%value'          │ { field: /value$/ }                      │
│ REGEXP / RLIKE         │ { field: { $regex: "pat", $options:"i" }}│
│ (no equivalent)        │ { $text: { $search: "keyword" } }       │
└────────────────────────┴──────────────────────────────────────────┘
```

---

## Why this is different from SQL (CRITICAL)

### 1. Array Queries Are First-Class

```javascript
// SQL has no native array querying (PostgreSQL has @> for arrays)
// MongoDB: Arrays are deeply integrated into the query engine

// Does array CONTAIN this value?
db.products.find({ tags: "electronics" })
// Matches: { tags: ["electronics", "sale"] }

// Does array contain ALL of these?
db.products.find({ tags: { $all: ["electronics", "sale"] } })

// Array has exactly N elements
db.products.find({ tags: { $size: 3 } })

// ANY array element matches complex condition
db.products.find({
  reviews: { $elemMatch: { rating: { $gte: 4 }, verified: true } }
})
// Different from: { "reviews.rating": { $gte: 4 }, "reviews.verified": true }
// $elemMatch ensures SAME element matches ALL conditions
```

### 2. Implicit AND vs Explicit AND

```javascript
// Implicit AND (most common — just add fields)
db.products.find({
  brand: "Dell",         // AND
  price: { $gt: 500 },  // AND
  stock: { $gt: 0 }     // AND
})

// Explicit $and (needed when same field appears twice)
db.products.find({
  $and: [
    { price: { $gt: 100 } },
    { price: { $lt: 500 } }
  ]
})
// Shorthand for same field:
db.products.find({ price: { $gt: 100, $lt: 500 } })

// ⚠️ GOTCHA: Duplicate keys in JSON objects — last one wins!
db.products.find({
  price: { $gt: 100 },
  price: { $lt: 500 }   // ❌ Overwrites the first price condition!
})
// You MUST use $and for two conditions on the same field with different operators
```

### 3. $expr for Field-to-Field Comparison

```sql
-- SQL: Compare two columns
SELECT * FROM products WHERE sale_price < original_price;
```

```javascript
// MongoDB: Need $expr for field-to-field comparison
db.products.find({
  $expr: {
    $lt: ["$salePrice", "$originalPrice"]
  }
})
// Without $expr, you can only compare a field to a literal value
```

---

## Syntax — All Operators

### Comparison

```javascript
// Equal
db.products.find({ brand: "Dell" })

// Not equal
db.products.find({ status: { $ne: "discontinued" } })

// Greater/Less than
db.products.find({ price: { $gt: 100, $lt: 500 } })
db.products.find({ stock: { $gte: 1 } })

// IN / NOT IN
db.products.find({ brand: { $in: ["Dell", "HP", "Lenovo"] } })
db.products.find({ category: { $nin: ["Discontinued", "Draft"] } })
```

### Logical

```javascript
// OR
db.products.find({
  $or: [
    { price: { $lt: 50 } },
    { "ratings.average": { $gte: 4.5 } }
  ]
})

// AND + OR combined (SQL: WHERE brand = 'Dell' AND (price < 500 OR stock > 100))
db.products.find({
  brand: "Dell",
  $or: [
    { price: { $lt: 500 } },
    { stock: { $gt: 100 } }
  ]
})

// NOR (neither condition is true)
db.products.find({
  $nor: [
    { status: "discontinued" },
    { stock: 0 }
  ]
})

// NOT
db.products.find({
  price: { $not: { $gt: 1000 } }  // price <= 1000 OR price doesn't exist
})
// ⚠️ $not also matches documents where the field doesn't exist!
// This is different from SQL where NOT (price > 1000) only returns rows where price exists
```

### Element

```javascript
// Field exists
db.products.find({ discount: { $exists: true } })   // Has discount field
db.products.find({ discount: { $exists: false } })  // No discount field

// Type checking
db.products.find({ price: { $type: "number" } })
db.products.find({ price: { $type: ["double", "decimal"] } })

// BSON type numbers
db.products.find({ price: { $type: 1 } })   // Double
db.products.find({ price: { $type: 19 } })  // Decimal128
```

### Array

```javascript
// Array contains value
db.products.find({ tags: "sale" })

// Array contains ALL values
db.products.find({ tags: { $all: ["sale", "featured"] } })

// Array size equals
db.products.find({ tags: { $size: 3 } })
// ⚠️ $size doesn't support ranges. For "size > 3", use:
db.products.find({ "tags.3": { $exists: true } })  // Has index 3 = at least 4 elements

// $elemMatch — single element matches all conditions
db.orders.find({
  items: {
    $elemMatch: {
      price: { $gte: 100 },
      quantity: { $gte: 2 }
    }
  }
})
// vs dot notation (ANY element matches each condition independently)
db.orders.find({
  "items.price": { $gte: 100 },     // Some element has price >= 100
  "items.quantity": { $gte: 2 }      // Some (possibly different) element has qty >= 2
})
```

### Evaluation

```javascript
// Regex
db.products.find({ name: { $regex: /^laptop/i } })
db.products.find({ name: { $regex: "laptop", $options: "i" } })

// Text search (requires text index)
db.products.createIndex({ name: "text", description: "text" })
db.products.find({ $text: { $search: "gaming laptop" } })
db.products.find({ $text: { $search: "\"gaming laptop\"" } })  // Exact phrase
db.products.find({ $text: { $search: "laptop -refurbished" } }) // Exclude term

// $expr — field-to-field comparison
db.products.find({
  $expr: { $gt: ["$stock", "$reorderLevel"] }
})

// $where — JavaScript expression (⚠️ AVOID — very slow, no index)
db.products.find({
  $where: function() { return this.price > this.cost * 2; }
})

// $mod — modulo
db.products.find({ stock: { $mod: [10, 0] } })  // Stock divisible by 10
```

---

## SQL vs MongoDB — Complex Query Side-by-Side

```sql
-- SQL: Complex query with subquery
SELECT *
FROM products
WHERE brand IN ('Dell', 'HP')
  AND price BETWEEN 500 AND 1500
  AND stock > 0
  AND (category = 'Laptops' OR category = 'Desktops')
  AND name LIKE '%Pro%'
  AND rating >= 4.0
ORDER BY price DESC
LIMIT 20;
```

```javascript
// MongoDB equivalent
db.products.find({
  brand: { $in: ["Dell", "HP"] },
  price: { $gte: 500, $lte: 1500 },
  stock: { $gt: 0 },
  $or: [
    { "category.name": "Laptops" },
    { "category.name": "Desktops" }
  ],
  name: { $regex: /Pro/i },
  "ratings.average": { $gte: 4.0 }
})
.sort({ price: -1 })
.limit(20)
```

---

## Node.js Using MongoDB Driver (REQUIRED)

```javascript
const { MongoClient, ObjectId } = require('mongodb');

async function queryOperatorExamples() {
  const client = new MongoClient('mongodb://localhost:27017');
  await client.connect();
  const db = client.db('ecommerce');
  const products = db.collection('products');

  // ──── Comparison ────
  const expensive = await products.find({ price: { $gte: 500 } }).toArray();

  // ──── Logical OR ────
  const deals = await products.find({
    $or: [
      { price: { $lt: 20 } },
      { "ratings.average": { $gte: 4.8 } }
    ]
  }).toArray();

  // ──── Array queries ────
  const tagged = await products.find({
    tags: { $all: ["electronics", "portable"] }
  }).toArray();

  // ──── Element queries ────
  const withDiscount = await products.find({
    discount: { $exists: true, $gt: 0 }
  }).toArray();

  // ──── Regex search ────
  const search = await products.find({
    name: { $regex: req.query.q, $options: 'i' }
  }).toArray();

  // ──── Complex combined query ────
  const filtered = await products.find({
    brand: { $in: ['Dell', 'HP', 'Lenovo'] },
    price: { $gte: 200, $lte: 1500 },
    stock: { $gt: 0 },
    'ratings.average': { $gte: 3.5 },
    tags: 'laptop',
    $or: [
      { 'specs.ram': { $in: ['16GB', '32GB'] } },
      { 'specs.storage': /ssd/i }
    ]
  })
  .sort({ 'ratings.average': -1, price: 1 })
  .limit(20)
  .toArray();

  // ──── Dynamic filter building (real-world pattern) ────
  function buildProductFilter(params) {
    const filter = {};
    if (params.brand) filter.brand = Array.isArray(params.brand)
      ? { $in: params.brand } : params.brand;
    if (params.minPrice || params.maxPrice) {
      filter.price = {};
      if (params.minPrice) filter.price.$gte = parseFloat(params.minPrice);
      if (params.maxPrice) filter.price.$lte = parseFloat(params.maxPrice);
    }
    if (params.inStock === 'true') filter.stock = { $gt: 0 };
    if (params.minRating) filter['ratings.average'] = { $gte: parseFloat(params.minRating) };
    if (params.search) filter.name = { $regex: params.search, $options: 'i' };
    if (params.tags) filter.tags = { $all: params.tags.split(',') };
    return filter;
  }

  await client.close();
}
```

---

## Real-World Scenario — Advanced Product Search

```javascript
// Express endpoint with full filter support
app.get('/api/products/search', async (req, res) => {
  const filter = {};
  const { q, category, brand, minPrice, maxPrice, minRating, tags, inStock } = req.query;

  // Text search OR regex
  if (q) {
    if (q.length < 3) {
      filter.name = { $regex: q, $options: 'i' };
    } else {
      filter.$text = { $search: q };
    }
  }
  if (category) filter['category.slug'] = category;
  if (brand) filter.brand = { $in: brand.split(',') };
  if (minPrice || maxPrice) {
    filter.price = {};
    if (minPrice) filter.price.$gte = parseFloat(minPrice);
    if (maxPrice) filter.price.$lte = parseFloat(maxPrice);
  }
  if (minRating) filter['ratings.average'] = { $gte: parseFloat(minRating) };
  if (tags) filter.tags = { $all: tags.split(',') };
  if (inStock === 'true') filter.stock = { $gt: 0 };

  const page = parseInt(req.query.page) || 1;
  const limit = Math.min(parseInt(req.query.limit) || 20, 100);

  const [results, total] = await Promise.all([
    db.collection('products')
      .find(filter)
      .sort({ 'ratings.average': -1, price: 1 })
      .skip((page - 1) * limit)
      .limit(limit)
      .toArray(),
    db.collection('products').countDocuments(filter)
  ]);

  res.json({ data: results, total, page, pages: Math.ceil(total / limit) });
});
```

---

## Performance Insight

```
┌────────────────────────────────────────────────────────────────┐
│  Operator         │ Index Usage               │ Performance    │
├───────────────────┼───────────────────────────┼────────────────┤
│  Equality (=)     │ ✅ Uses index             │ ⚡ Fastest     │
│  $in              │ ✅ Uses index             │ ⚡ Fast        │
│  $gt/$lt (range)  │ ✅ Uses index             │ ⚡ Fast        │
│  $or              │ ✅ Each branch can use idx│ ⚡ Good        │
│  $regex /^prefix/ │ ✅ Uses index (anchored)  │ ⚡ Fast        │
│  $regex /middle/  │ ❌ Full scan              │ 🐌 Slow       │
│  $text            │ ✅ Text index required    │ ⚡ Good        │
│  $ne / $nin       │ ⚠️ Poor selectivity       │ 🐌 Often slow │
│  $not             │ ⚠️ May not use index      │ 🐌 Variable   │
│  $exists: false   │ ❌ Scans sparse index     │ 🐌 Slow       │
│  $where           │ ❌ No index, JS execution │ 🐌 Very slow  │
│  $expr             │ ⚠️ Limited index support  │ 🐌 Usually slow│
│  $elemMatch       │ ✅ Uses multikey index    │ ⚡ Good        │
│  $size            │ ❌ No index               │ 🐌 Full scan  │
├───────────────────┴───────────────────────────┴────────────────┤
│  Rule: $eq > $in > $range > $regex(^) > $text > $or > rest   │
│  Design indexes around your most selective operators first.    │
└────────────────────────────────────────────────────────────────┘
```

---

## Common Mistakes (SQL Developers Make)

### ❌ Mistake 1: Using $regex Without Anchor

```javascript
// ❌ Full collection scan — like SQL's LIKE '%term%'
db.products.find({ name: { $regex: /laptop/ } })

// ✅ Use anchored regex when possible — like SQL's LIKE 'laptop%'
db.products.find({ name: { $regex: /^laptop/i } })
// Or use text index for general search
```

### ❌ Mistake 2: Confusing Dot Notation with $elemMatch

```javascript
// These are DIFFERENT:
// Dot notation: each condition can match DIFFERENT array elements
db.orders.find({ "items.price": { $gt: 100 }, "items.qty": { $gt: 5 } })
// Matches if ANY item has price>100 AND ANY item (possibly different) has qty>5

// $elemMatch: all conditions must match the SAME element
db.orders.find({ items: { $elemMatch: { price: { $gt: 100 }, qty: { $gt: 5 } } } })
// Matches only if a SINGLE item has BOTH price>100 AND qty>5
```

### ❌ Mistake 3: Using $ne for Existence Checks

```javascript
// ❌ $ne: null includes docs where field doesn't exist (confusing)
db.products.find({ discount: { $ne: null } })

// ✅ Be explicit
db.products.find({ discount: { $exists: true, $ne: null } })
```

---

## Practice Exercises

### Exercise 1: Query Translation

Convert these SQL queries to MongoDB:

```sql
1. SELECT * FROM products WHERE price NOT BETWEEN 100 AND 500;
2. SELECT * FROM orders WHERE status IN ('pending','processing') AND total > 50;
3. SELECT * FROM customers WHERE email LIKE '%@gmail.com';
4. SELECT * FROM products WHERE category IS NOT NULL AND stock > 0;
5. SELECT * FROM products WHERE (brand = 'Dell' AND price < 1000) OR (brand = 'Apple' AND price < 2000);
```

### Exercise 2: Array Query Challenge

Given products with a `reviews` array:
1. Find products with at least one 5-star review
2. Find products where ALL reviews are from verified buyers
3. Find products with more than 10 reviews
4. Find products where a verified buyer gave a rating above 4

### Exercise 3: Performance Optimization

You have this slow query. How would you optimize it?

```javascript
db.products.find({
  name: /gaming/i,
  price: { $gt: 100, $lt: 2000 },
  "category.name": "Electronics",
  tags: { $all: ["gaming", "rgb"] },
  stock: { $ne: 0 }
})
```

---

## Interview Q&A

**Q1: What's the difference between `$in` and `$or` for multiple value matching?**
> `$in` checks if a single field matches any value in an array — it uses a single index scan. `$or` can check different fields with different conditions — each branch uses its own index. For checking one field against multiple values, `$in` is more efficient. `$or` is needed when conditions span different fields.

**Q2: How do `$elemMatch` queries differ from dot notation array queries?**
> Dot notation conditions can be satisfied by different elements (`"items.price": {$gt:100}, "items.qty": {$gt:5}` — any item has price>100 AND any item has qty>5). `$elemMatch` requires a SINGLE element to satisfy ALL conditions. This distinction matters for arrays of objects.

**Q3: Why should you avoid `$where` in MongoDB?**
> `$where` executes JavaScript for every document — no index can be used, and it's orders of magnitude slower than native operators. It also poses a security risk (JavaScript injection). Use `$expr` for field comparisons instead.

**Q4: How does `$ne` interact with indexes?**
> `$ne` has poor index selectivity. If you query `{ status: { $ne: "deleted" } }` and 95% of documents are not deleted, the index scan covers 95% of documents — barely better than a full scan. Rewrite as positive matches: `{ status: { $in: ["active", "pending"] } }`.

**Q5: Can you combine `$text` search with other query operators?**
> Yes, but the `$text` query must be the first operator (it uses a text index). You can combine it with other filters: `{ $text: { $search: "laptop" }, price: { $gt: 100 } }`. However, you cannot use `$text` inside `$or` or `$elemMatch`, and you can only have ONE `$text` expression per query.
