# Projection & Pagination

> 📌 **File:** 09_Projection_And_Pagination.md | **Level:** SQL Expert → MongoDB

---

## What is it?

Projection controls which fields are returned in query results (SQL's `SELECT column1, column2`). Pagination controls result windows (SQL's `LIMIT/OFFSET`). In MongoDB, both concepts exist but have important behavioral differences — especially around array projection and cursor-based pagination.

---

## SQL Parallel — Think of it like this

```
SQL:                                           MongoDB:
SELECT name, price FROM t                    → db.t.find({}, { name:1, price:1 })
SELECT * EXCEPT large_blob FROM t            → db.t.find({}, { large_blob: 0 })
SELECT * FROM t LIMIT 10                     → db.t.find().limit(10)
SELECT * FROM t LIMIT 10 OFFSET 20          → db.t.find().skip(20).limit(10)
SELECT * FROM t ORDER BY id LIMIT 10 OFFSET 0→ db.t.find().sort({_id:1}).limit(10)
```

---

## Projection

### Inclusion vs Exclusion

```javascript
// INCLUDE specific fields (whitelist)
db.products.find({}, { name: 1, price: 1, brand: 1 })
// Returns: { _id: ..., name: "Laptop", price: 999, brand: "Dell" }
// _id is ALWAYS included unless explicitly excluded

// EXCLUDE specific fields (blacklist)
db.products.find({}, { specs: 0, reviews: 0, description: 0 })
// Returns ALL fields EXCEPT specs, reviews, description

// Exclude _id
db.products.find({}, { name: 1, price: 1, _id: 0 })
// Returns: { name: "Laptop", price: 999 }

// ⚠️ RULE: Cannot mix inclusion and exclusion (except _id)
db.products.find({}, { name: 1, specs: 0 })  // ❌ ERROR!
// Either include what you want OR exclude what you don't — not both
```

### Nested Field Projection

```javascript
// Project nested fields with dot notation
db.products.find({}, {
  name: 1,
  "category.name": 1,     // Only category name, not slug
  "ratings.average": 1,   // Only average rating, not count
  "specs.ram": 1           // Only RAM from specs
})

// SQL equivalent requires JSON extraction:
// SELECT name, specs->>'ram' as ram FROM products;
```

### Array Projection Operators

```javascript
// $slice — return subset of array (no SQL equivalent)
db.products.find({}, {
  name: 1,
  reviews: { $slice: 5 }      // First 5 reviews
})
db.products.find({}, {
  reviews: { $slice: -3 }     // Last 3 reviews
})
db.products.find({}, {
  reviews: { $slice: [10, 5] } // Skip 10, return 5 (pagination within array)
})

// $elemMatch — return first matching array element
db.products.find(
  { "reviews.rating": { $gte: 5 } },
  { name: 1, reviews: { $elemMatch: { rating: { $gte: 5 } } } }
)
// Returns only the FIRST review with rating >= 5, not all of them

// $ (positional) — return matched array element
db.products.find(
  { "reviews.userId": ObjectId("...") },
  { name: 1, "reviews.$": 1 }
)
// Returns only the review that matched the query
```

---

## Pagination

### Offset-Based (skip/limit)

```javascript
// Page 1: skip 0, limit 10
db.products.find().sort({ createdAt: -1 }).skip(0).limit(10)

// Page 2: skip 10, limit 10
db.products.find().sort({ createdAt: -1 }).skip(10).limit(10)

// Page N:
const page = 5;
const pageSize = 20;
db.products.find()
  .sort({ createdAt: -1 })
  .skip((page - 1) * pageSize)
  .limit(pageSize)
```

**⚠️ Problem with large offsets:**
```
skip(0)       → Fast (start from beginning)
skip(100)     → Still OK
skip(10000)   → Slow (scans 10,000 docs to skip them)
skip(1000000) → Very slow (scans 1M docs)

SQL has the same problem:
OFFSET 1000000 LIMIT 10  → Also slow in SQL
```

### Cursor-Based Pagination (Keyset)

```javascript
// First page
const firstPage = await db.collection('products')
  .find({})
  .sort({ _id: 1 })
  .limit(20)
  .toArray();

// Get the last _id from results
const lastId = firstPage[firstPage.length - 1]._id;

// Next page — no skip needed!
const nextPage = await db.collection('products')
  .find({ _id: { $gt: lastId } })
  .sort({ _id: 1 })
  .limit(20)
  .toArray();

// For custom sort fields:
const lastPrice = firstPage[firstPage.length - 1].price;
const lastIdForTies = firstPage[firstPage.length - 1]._id;

const nextPage2 = await db.collection('products')
  .find({
    $or: [
      { price: { $gt: lastPrice } },
      { price: lastPrice, _id: { $gt: lastIdForTies } }
    ]
  })
  .sort({ price: 1, _id: 1 })
  .limit(20)
  .toArray();
```

```
┌─────────────────────────────────────────────────────────────────┐
│          Offset vs Cursor Pagination                            │
├───────────────────┬──────────────────┬──────────────────────────┤
│                   │  Offset (skip)   │  Cursor (keyset)         │
├───────────────────┼──────────────────┼──────────────────────────┤
│  Implementation   │  Simple          │  More complex            │
│  Deep pages       │  🐌 Slow         │  ⚡ Constant time        │
│  Random page jump │  ✅ Supported    │  ❌ Not practical        │
│  Total page count │  ✅ Easy         │  ❌ Expensive to compute │
│  Real-time inserts│  ⚠️ Duplicates   │  ✅ Consistent           │
│  Use case         │  Admin dashboards│  Infinite scroll, feeds  │
│  SQL equivalent   │  OFFSET/LIMIT    │  WHERE id > last_id      │
└───────────────────┴──────────────────┴──────────────────────────┘
```

---

## Node.js Using MongoDB Driver (REQUIRED)

```javascript
// Complete paginated API with projection
app.get('/api/products', async (req, res) => {
  const db = getDB();
  const {
    page = 1,
    limit = 20,
    fields,        // Comma-separated field names
    sort = '-createdAt',
    cursor         // For cursor-based pagination
  } = req.query;

  const pageNum = Math.max(1, parseInt(page));
  const limitNum = Math.min(Math.max(1, parseInt(limit)), 100);

  // Build projection from fields param
  let projection = {};
  if (fields) {
    fields.split(',').forEach(f => { projection[f.trim()] = 1; });
  } else {
    // Default: exclude heavy fields
    projection = { reviews: 0, description: 0 };
  }

  // Build sort object
  const sortObj = {};
  sort.split(',').forEach(field => {
    if (field.startsWith('-')) {
      sortObj[field.substring(1)] = -1;
    } else {
      sortObj[field] = 1;
    }
  });

  let filter = {};

  // Cursor-based pagination
  if (cursor) {
    const decoded = JSON.parse(Buffer.from(cursor, 'base64').toString());
    filter._id = { $gt: new ObjectId(decoded.lastId) };
  }

  const [data, total] = await Promise.all([
    db.collection('products')
      .find(filter)
      .project(projection)
      .sort(sortObj)
      .skip(cursor ? 0 : (pageNum - 1) * limitNum)
      .limit(limitNum)
      .toArray(),
    db.collection('products').countDocuments({})
  ]);

  // Generate next cursor
  let nextCursor = null;
  if (data.length === limitNum) {
    const lastDoc = data[data.length - 1];
    nextCursor = Buffer.from(JSON.stringify({ lastId: lastDoc._id })).toString('base64');
  }

  res.json({
    data,
    pagination: cursor
      ? { cursor: nextCursor, limit: limitNum, hasMore: data.length === limitNum }
      : { page: pageNum, limit: limitNum, total, pages: Math.ceil(total / limitNum) }
  });
});
```

---

## Real-World Scenario — Infinite Scroll Feed

```javascript
// API for infinite scroll (cursor-based)
app.get('/api/feed', async (req, res) => {
  const { cursor, limit = 20 } = req.query;
  const filter = { isActive: true };

  if (cursor) {
    // Cursor contains the createdAt + _id of the last seen item
    const { lastDate, lastId } = JSON.parse(
      Buffer.from(cursor, 'base64').toString()
    );
    filter.$or = [
      { createdAt: { $lt: new Date(lastDate) } },
      { createdAt: new Date(lastDate), _id: { $lt: new ObjectId(lastId) } }
    ];
  }

  const items = await db.collection('posts')
    .find(filter)
    .project({ title: 1, excerpt: 1, author: 1, createdAt: 1, thumbnail: 1 })
    .sort({ createdAt: -1, _id: -1 })
    .limit(parseInt(limit))
    .toArray();

  const nextCursor = items.length === parseInt(limit)
    ? Buffer.from(JSON.stringify({
        lastDate: items[items.length - 1].createdAt,
        lastId: items[items.length - 1]._id
      })).toString('base64')
    : null;

  res.json({ items, nextCursor, hasMore: !!nextCursor });
});
```

### React Infinite Scroll

```javascript
function Feed() {
  const [items, setItems] = useState([]);
  const [cursor, setCursor] = useState(null);
  const [hasMore, setHasMore] = useState(true);

  const loadMore = async () => {
    const url = cursor ? `/api/feed?cursor=${cursor}` : '/api/feed';
    const { data } = await axios.get(url);
    setItems(prev => [...prev, ...data.items]);
    setCursor(data.nextCursor);
    setHasMore(data.hasMore);
  };

  useEffect(() => { loadMore(); }, []);

  return (
    <InfiniteScroll loadMore={loadMore} hasMore={hasMore}>
      {items.map(item => <PostCard key={item._id} post={item} />)}
    </InfiniteScroll>
  );
}
```

---

## Performance Insight

```
┌─────────────────────────────────────────────────────────────────────┐
│  Projection Impact on Performance                                  │
├─────────────────────────┬───────────────────────────────────────────┤
│  Full document          │ Reads entire BSON from disk               │
│  Projected fields       │ Still reads full BSON, filters in memory  │
│  Projection on index    │ COVERED QUERY — reads only index, no disk│
├─────────────────────────┴───────────────────────────────────────────┤
│                                                                     │
│  Covered Query (the ultimate optimization):                         │
│  If ALL queried and projected fields are in an index,               │
│  MongoDB returns results from the index alone — never touches       │
│  the actual documents on disk.                                      │
│                                                                     │
│  db.products.createIndex({ brand: 1, price: 1, name: 1 })         │
│  db.products.find(                                                  │
│    { brand: "Dell" },                                               │
│    { brand: 1, price: 1, name: 1, _id: 0 }  // All in index       │
│  )                                                                  │
│  // explain() → stage: "IXSCAN", totalDocsExamined: 0 ← ZERO!     │
│                                                                     │
│  SQL equivalent: Index-only scan                                    │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Common Mistakes

### ❌ Sending Entire Documents to Frontend

```javascript
// ❌ Sends password hash, internal fields, large arrays
const user = await db.collection('users').findOne({ _id: userId });
res.json(user); // { password: '$2b$...', internalNotes: '...', allOrders: [...] }

// ✅ Project only what the client needs
const user = await db.collection('users').findOne(
  { _id: userId },
  { projection: { name: 1, email: 1, avatar: 1, createdAt: 1 } }
);
res.json(user);
```

### ❌ Using skip() for Deep Pagination

```javascript
// ❌ Page 5000 of results — extremely slow
db.products.find().skip(100000).limit(20)

// ✅ Use cursor-based pagination for infinite scroll / feeds
// ✅ Use offset for admin panels where deep pages are rare
```

---

## Practice Exercises

### Exercise 1: Projection

1. Find all products showing only name, price, and category name (exclude _id)
2. Find products showing the first 3 reviews only
3. Find a product and project only the review matching a specific userId

### Exercise 2: Pagination

1. Implement offset-based pagination for products sorted by price descending
2. Implement cursor-based pagination for an activity feed sorted by timestamp
3. Create an endpoint that supports both pagination styles via query param `?style=offset` or `?style=cursor`

---

## Interview Q&A

**Q1: What is a covered query?**
> A query where all fields in both the filter and projection exist in a single index. MongoDB satisfies the query entirely from the index without reading any documents from disk. This is the fastest possible query — equivalent to SQL's index-only scan.

**Q2: Why is skip-based pagination problematic at scale?**
> `skip(N)` must iterate through N documents before returning results. On page 10,000 (skip 200,000), MongoDB scans 200K entries. Cursor-based pagination uses an index-backed range query (`_id > lastId`), making every page equally fast regardless of depth.

**Q3: Can you mix field inclusion and exclusion in projection?**
> No, except for `_id`. You either include specific fields (`{ name: 1, price: 1 }`) or exclude specific fields (`{ reviews: 0, blob: 0 }`). Mixing (`{ name: 1, reviews: 0 }`) throws an error. `_id` is special — it can be excluded (`_id: 0`) with inclusion mode.

**Q4: How does `$slice` differ from `$elemMatch` in projection?**
> `$slice` returns N elements from an array by position (first 5, last 3, skip 10 take 5). `$elemMatch` returns the first element matching a condition. `$slice` is for pagination within arrays; `$elemMatch` is for finding a specific element.

**Q5: How do you handle total count efficiently with cursor-based pagination?**
> You typically don't. Cursor-based pagination returns `hasMore: true/false` instead of total count. Computing `countDocuments()` is expensive on large collections. Use `estimatedDocumentCount()` for approximate totals, or cache the count and refresh periodically.
