# CRUD — Read

> 📌 **File:** 05_CRUD_Read.md | **Level:** SQL Expert → MongoDB

---

## What is it?

Read operations retrieve documents from collections. MongoDB's `find()` is the equivalent of SQL's `SELECT`. The key difference: MongoDB queries use JSON-based filter objects instead of SQL string syntax, and results can include deeply nested data that would require JOINs in SQL.

---

## SQL Parallel — Think of it like this

```
SQL:                                  MongoDB:
SELECT * FROM t                    →  db.t.find()
SELECT * FROM t WHERE x = 1       →  db.t.find({ x: 1 })
SELECT a, b FROM t                 →  db.t.find({}, { a: 1, b: 1 })
SELECT * FROM t WHERE x > 5       →  db.t.find({ x: { $gt: 5 } })
SELECT * FROM t LIMIT 1           →  db.t.findOne({})
SELECT * FROM t ORDER BY x ASC    →  db.t.find().sort({ x: 1 })
SELECT * FROM t LIMIT 10 OFFSET 20→  db.t.find().skip(20).limit(10)
SELECT COUNT(*) FROM t             →  db.t.countDocuments()
SELECT DISTINCT(x) FROM t         →  db.t.distinct('x')
```

---

## Why this is different from SQL (CRITICAL)

### 1. Queries Return Cursors, Not Result Sets

```javascript
// SQL: SELECT * returns all rows into memory
// MongoDB: find() returns a CURSOR — an iterator

const cursor = db.products.find({});
// Nothing loaded yet. cursor is lazy.

// Option 1: Iterate
while (await cursor.hasNext()) {
  const doc = await cursor.next();
  console.log(doc);
}

// Option 2: Convert to array (loads all into memory)
const all = await cursor.toArray(); // ⚠️ Don't do this for large collections

// Option 3: forEach
await cursor.forEach(doc => console.log(doc));

// SQL developers: This is like a database cursor in SQL, not a result set.
```

### 2. Querying Nested Fields is Natural

```javascript
// SQL: Requires JOINs or JSON extraction operators
// SELECT * FROM products WHERE category->>'name' = 'Electronics';

// MongoDB: Dot notation for nested fields — first-class feature
db.products.find({ "category.name": "Electronics" })
db.products.find({ "specs.ram": "16GB" })
db.products.find({ "address.city": "New York" })

// Array element queries — also natural
db.products.find({ tags: "portable" })        // Array contains "portable"
db.products.find({ "tags.0": "computer" })    // First element is "computer"
```

### 3. No JOINs in find()

```javascript
// You CANNOT do this:
// db.orders.find() JOIN db.customers ...

// You either:
// 1. Embed the data (best for MongoDB)
// 2. Use $lookup in aggregation (expensive)
// 3. Do multiple queries in application code
```

---

## Syntax

### Basic find()

```javascript
// SELECT * FROM products;
db.products.find()

// SELECT * FROM products WHERE brand = 'Dell';
db.products.find({ brand: "Dell" })

// SELECT * FROM products WHERE price > 100;
db.products.find({ price: { $gt: 100 } })

// SELECT * FROM products WHERE brand = 'Dell' AND price > 500;
db.products.find({ brand: "Dell", price: { $gt: 500 } })

// SELECT * FROM products WHERE brand = 'Dell' OR brand = 'HP';
db.products.find({ $or: [{ brand: "Dell" }, { brand: "HP" }] })

// SELECT * FROM products WHERE brand IN ('Dell', 'HP', 'Lenovo');
db.products.find({ brand: { $in: ["Dell", "HP", "Lenovo"] } })

// SELECT * FROM products WHERE price BETWEEN 100 AND 500;
db.products.find({ price: { $gte: 100, $lte: 500 } })

// SELECT * FROM products WHERE name LIKE '%laptop%';
db.products.find({ name: /laptop/i })
db.products.find({ name: { $regex: "laptop", $options: "i" } })
```

### findOne()

```javascript
// SELECT * FROM products WHERE _id = 1 LIMIT 1;
db.products.findOne({ _id: ObjectId("...") })

// Returns a single document (or null)
// NOT a cursor — direct document
```

### Projection (SELECT specific fields)

```javascript
// SELECT name, price FROM products;
db.products.find({}, { name: 1, price: 1 })
// Returns: { _id: ..., name: "Laptop", price: 999 }
// Note: _id is ALWAYS included unless explicitly excluded

// SELECT name, price FROM products (without _id);
db.products.find({}, { name: 1, price: 1, _id: 0 })
// Returns: { name: "Laptop", price: 999 }

// Exclude specific fields
db.products.find({}, { specs: 0, tags: 0 })
// Returns all fields EXCEPT specs and tags

// ⚠️ Cannot mix inclusion and exclusion (except _id)
// db.products.find({}, { name: 1, specs: 0 })  // ERROR!
```

### Sorting

```javascript
// SELECT * FROM products ORDER BY price ASC;
db.products.find().sort({ price: 1 })

// SELECT * FROM products ORDER BY price DESC;
db.products.find().sort({ price: -1 })

// SELECT * FROM products ORDER BY category ASC, price DESC;
db.products.find().sort({ "category.name": 1, price: -1 })
```

### Limiting and Skipping

```javascript
// SELECT * FROM products LIMIT 10;
db.products.find().limit(10)

// SELECT * FROM products LIMIT 10 OFFSET 20;
db.products.find().skip(20).limit(10)

// Method chaining (order doesn't matter — MongoDB always applies: sort → skip → limit)
db.products.find({ brand: "Dell" })
  .sort({ price: -1 })
  .skip(0)
  .limit(10)
```

### Counting

```javascript
// SELECT COUNT(*) FROM products;
db.products.countDocuments()                    // Exact count (reads collection)
db.products.estimatedDocumentCount()            // Fast approximate (uses metadata)

// SELECT COUNT(*) FROM products WHERE price > 100;
db.products.countDocuments({ price: { $gt: 100 } })
```

### Distinct

```javascript
// SELECT DISTINCT brand FROM products;
db.products.distinct("brand")
// Returns: ["Dell", "HP", "Logitech", ...]

// SELECT DISTINCT brand FROM products WHERE price > 500;
db.products.distinct("brand", { price: { $gt: 500 } })
```

---

## SQL vs MongoDB — Side-by-Side

```sql
-- SQL: Complex query with multiple conditions
SELECT p.name, p.price, c.name as category_name
FROM products p
JOIN categories c ON p.category_id = c.id
WHERE p.price BETWEEN 50 AND 500
  AND c.name = 'Electronics'
  AND p.stock > 0
ORDER BY p.price DESC
LIMIT 10 OFFSET 20;
```

```javascript
// MongoDB: Single collection query (data embedded)
db.products.find(
  {
    price: { $gte: 50, $lte: 500 },
    "category.name": "Electronics",
    stock: { $gt: 0 }
  },
  { name: 1, price: 1, "category.name": 1 }
)
.sort({ price: -1 })
.skip(20)
.limit(10)
```

---

## Node.js Using MongoDB Driver (REQUIRED)

```javascript
const { MongoClient, ObjectId } = require('mongodb');

async function readOperations() {
  const client = new MongoClient('mongodb://localhost:27017');
  await client.connect();
  const db = client.db('ecommerce');
  const products = db.collection('products');

  // ──────────── Find All ────────────
  const allProducts = await products.find({}).toArray();
  console.log('Total products:', allProducts.length);

  // ──────────── Find with Filter ────────────
  const electronics = await products.find({
    "category.name": "Electronics"
  }).toArray();

  // ──────────── Find One by ID ────────────
  const product = await products.findOne({
    _id: new ObjectId("65a1b2c3d4e5f6a7b8c9d0e1")
  });

  // ──────────── Complex Query ────────────
  const results = await products.find({
    price: { $gte: 50, $lte: 1000 },
    stock: { $gt: 0 },
    "ratings.average": { $gte: 4.0 },
    tags: { $in: ["computer", "gaming"] }       // Array intersection
  })
  .project({ name: 1, price: 1, "ratings.average": 1 })
  .sort({ "ratings.average": -1, price: 1 })
  .skip(0)
  .limit(20)
  .toArray();

  // ──────────── Cursor Iteration (memory-efficient) ────────────
  const cursor = products.find({ stock: { $gt: 0 } });
  for await (const doc of cursor) {
    // Process one document at a time — no array in memory
    console.log(doc.name, doc.stock);
  }

  // ──────────── Count ────────────
  const total = await products.countDocuments();
  const inStock = await products.countDocuments({ stock: { $gt: 0 } });
  const estimated = await products.estimatedDocumentCount();

  // ──────────── Distinct ────────────
  const brands = await products.distinct('brand');
  const activeCategories = await products.distinct('category.name', { stock: { $gt: 0 } });

  // ──────────── Check if Document Exists ────────────
  const exists = await products.findOne(
    { email: "john@example.com" },
    { projection: { _id: 1 } }  // Only fetch _id for efficiency
  );
  if (exists) console.log('Customer exists');

  await client.close();
}
```

### Express API — Product Search

```javascript
// GET /api/products?category=Electronics&minPrice=50&maxPrice=500&sort=price&order=desc&page=1&limit=10
app.get('/api/products', async (req, res) => {
  const {
    category, minPrice, maxPrice, brand, search,
    sort = 'createdAt', order = 'desc',
    page = 1, limit = 10
  } = req.query;

  // Build filter dynamically
  const filter = {};
  if (category) filter['category.name'] = category;
  if (brand) filter.brand = brand;
  if (minPrice || maxPrice) {
    filter.price = {};
    if (minPrice) filter.price.$gte = parseFloat(minPrice);
    if (maxPrice) filter.price.$lte = parseFloat(maxPrice);
  }
  if (search) filter.name = { $regex: search, $options: 'i' };

  const skip = (parseInt(page) - 1) * parseInt(limit);
  const sortObj = { [sort]: order === 'asc' ? 1 : -1 };

  const db = getDB();
  const [products, total] = await Promise.all([
    db.collection('products')
      .find(filter)
      .sort(sortObj)
      .skip(skip)
      .limit(parseInt(limit))
      .toArray(),
    db.collection('products').countDocuments(filter)
  ]);

  res.json({
    data: products,
    pagination: {
      page: parseInt(page),
      limit: parseInt(limit),
      total,
      pages: Math.ceil(total / parseInt(limit))
    }
  });
});
```

---

## ORM / ODM Comparison

```javascript
// ──── Sequelize (SQL) ────
const products = await Product.findAll({
  where: {
    price: { [Op.between]: [50, 500] },
    stock: { [Op.gt]: 0 }
  },
  include: [{ model: Category, where: { name: 'Electronics' } }],
  order: [['price', 'DESC']],
  limit: 10,
  offset: 20
});
// Generates: SELECT ... JOIN ... WHERE ... ORDER BY ... LIMIT ... OFFSET ...

// ──── Mongoose (MongoDB) ────
const products = await Product.find({
  price: { $gte: 50, $lte: 500 },
  stock: { $gt: 0 },
  'category.name': 'Electronics'
})
.select('name price category.name')
.sort({ price: -1 })
.skip(20)
.limit(10)
.lean();  // ← Returns plain objects instead of Mongoose documents (faster)

// Key differences:
// - Sequelize: include[] for JOINs. Complex eager/lazy loading.
// - Mongoose: No includes needed (data is embedded). .lean() for performance.
// - Mongoose .lean(): Skips Mongoose document instantiation. 5-10x faster for reads.
```

---

## Real-World Scenario — Product Search API

### React Frontend

```javascript
// React component using the search API
function ProductSearch() {
  const [products, setProducts] = useState([]);
  const [filters, setFilters] = useState({
    category: '', search: '', minPrice: '', maxPrice: '', page: 1
  });

  useEffect(() => {
    const params = new URLSearchParams(
      Object.entries(filters).filter(([_, v]) => v)
    );
    fetch(`/api/products?${params}`)
      .then(res => res.json())
      .then(data => setProducts(data.data));
  }, [filters]);

  return (
    <div>
      <input
        placeholder="Search products..."
        onChange={e => setFilters({ ...filters, search: e.target.value, page: 1 })}
      />
      {products.map(p => (
        <div key={p._id}>
          <h3>{p.name}</h3>
          <p>${parseFloat(p.price.toString()).toFixed(2)}</p>
        </div>
      ))}
    </div>
  );
}
```

---

## Performance Insight

### Query Performance Comparison

```
┌─────────────────────────────────────────────────────────────┐
│  Operation                  │ Without Index │ With Index    │
├─────────────────────────────┼───────────────┼───────────────┤
│  Find by _id                │ <1ms (hashed) │ <1ms          │
│  Find by indexed field      │ Full scan     │ <1ms          │
│  Find by unindexed field    │ Full scan     │ Full scan     │
│  Regex (anchored: /^lap/)   │ Full scan     │ Index scan    │
│  Regex (unanchored: /lap/)  │ Full scan     │ Full scan     │
│  Sort (indexed field)       │ In-memory     │ Index order   │
│  Sort (unindexed field)     │ In-memory     │ In-memory     │
├─────────────────────────────┴───────────────┴───────────────┤
│  ⚠️ In-memory sort has a 100MB limit. Exceeding it = error.│
│  Always index fields you sort on.                           │
└─────────────────────────────────────────────────────────────┘
```

### Explain Plan (= SQL EXPLAIN ANALYZE)

```javascript
// Check how MongoDB executes your query
db.products.find({ price: { $gt: 100 } }).explain("executionStats")

// Key fields to check:
// executionStats.executionTimeMillis  — total time
// executionStats.totalDocsExamined    — documents scanned (like rows_examined)
// executionStats.totalKeysExamined    — index entries checked
// winningPlan.stage                   — COLLSCAN (bad) vs IXSCAN (good)

// Rule: If totalDocsExamined >> nReturned, you need a better index.
```

---

## Common Mistakes (SQL Developers Make)

### ❌ Mistake 1: Using `.toArray()` on Large Collections

```javascript
// ❌ Loads millions of documents into memory
const all = await db.collection('logs').find({}).toArray();

// ✅ Use cursor iteration
for await (const doc of db.collection('logs').find({})) {
  process(doc);
}

// ✅ Or use pagination
const page = await db.collection('logs')
  .find({})
  .skip(offset)
  .limit(pageSize)
  .toArray();
```

### ❌ Mistake 2: Not Using Projection

```javascript
// ❌ Fetching entire documents when you only need name and price
const products = await db.collection('products').find({}).toArray();
// Each document might be 10KB with specs, reviews, etc.

// ✅ Only fetch what you need
const products = await db.collection('products')
  .find({}, { projection: { name: 1, price: 1 } })
  .toArray();
// Each document is now ~100 bytes
```

### ❌ Mistake 3: Skip/Limit for Deep Pagination

```javascript
// ❌ skip(100000) is slow — MongoDB must iterate through 100K docs
db.products.find().skip(100000).limit(10)

// ✅ Cursor-based pagination (keyset pagination)
// First page:
db.products.find().sort({ _id: 1 }).limit(10)

// Subsequent pages (use last document's _id):
db.products.find({ _id: { $gt: lastId } }).sort({ _id: 1 }).limit(10)
```

---

## Practice Exercises

### Exercise 1: Query Translation

Convert these SQL queries to MongoDB:

```sql
1. SELECT * FROM products WHERE brand = 'Dell' AND stock > 0;
2. SELECT name, price FROM products WHERE price < 100 ORDER BY price ASC LIMIT 5;
3. SELECT * FROM customers WHERE address_city IN ('NYC', 'LA', 'Chicago');
4. SELECT COUNT(*) FROM orders WHERE status = 'shipped' AND total > 100;
5. SELECT DISTINCT category FROM products WHERE price > 50;
```

### Exercise 2: Nested Query Challenge

Write MongoDB queries for:
1. Find products where specs.ram is "16GB" and specs.storage contains "SSD"
2. Find customers whose address is in state "NY" or "CA"
3. Find orders where any item has quantity > 5

### Exercise 3: Build a Search API

Create a GET `/api/products/search` endpoint that supports:
- Text search in product name
- Category filter
- Price range
- Brand filter
- Sort by price or rating
- Pagination with total count

---

## Interview Q&A

**Q1: What's the difference between `find()` and `findOne()`?**
> `find()` returns a cursor (lazy iterator). `findOne()` returns a single document or null. Use `findOne` for ID lookups. Use `find` for everything else. `findOne` is NOT `find().limit(1)` — it doesn't return a cursor at all.

**Q2: How do you query nested fields in MongoDB?**
> Use dot notation: `db.products.find({ "specs.ram": "16GB" })`. This works for any depth of nesting: `"a.b.c.d"`. For arrays, `{ tags: "value" }` checks if any element matches. For specific positions, `{ "tags.0": "value" }` checks the first element.

**Q3: Why is `skip()` with large offsets slow?**
> `skip(N)` iterates through N documents before returning results. On page 10,000 of a paginated list, MongoDB scans 100,000+ documents just to skip them. Solution: use cursor-based pagination with `{ _id: { $gt: lastSeenId } }` which uses the index directly.

**Q4: What is `lean()` in Mongoose and when should you use it?**
> `lean()` skips creating Mongoose document instances (with getters, setters, virtuals, save methods) and returns plain JavaScript objects. 5-10x faster for read-only operations. Use it for API responses. Don't use it if you need to call `.save()` or use Mongoose middleware.

**Q5: How do you check if a query uses an index?**
> Use `.explain("executionStats")`. Look for `winningPlan.stage: "IXSCAN"` (good, index scan) vs `"COLLSCAN"` (bad, full collection scan). Check `totalDocsExamined` vs `nReturned` — if ratio is high, the index isn't selective enough.
