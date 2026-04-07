# SQL Vs NoSQL

> 📌 **File:** `19_SQL_Vs_NoSQL.md` | **Level:** Beginner → MERN Developer

---

## What is it?

This is a comprehensive comparison between SQL databases (MySQL, PostgreSQL) and NoSQL databases (MongoDB). Now that you know both, this chapter helps you understand **when to choose which** — the most important architectural decision in any project.

There's no winner. Each is built for different use cases. The best developers know BOTH and choose wisely.

---

## MERN Parallel — You Already Know This!

You've lived in the MongoDB world. Now you can see both sides:

| Feature              | MongoDB (NoSQL)                    | MySQL (SQL)                        |
|----------------------|------------------------------------|------------------------------------|
| Data Model           | Documents (JSON/BSON)              | Tables (rows & columns)           |
| Schema               | Flexible / optional                | Strict / required                  |
| Relationships        | Embed or reference                 | Foreign keys + JOINs              |
| Query Language        | MQL (JavaScript-like)              | SQL (English-like)                |
| Scaling              | Horizontal (sharding)              | Vertical (bigger server)          |
| Transactions         | Limited (since v4.0)               | Full ACID since day 1             |
| Best For             | Rapid development, flexible data   | Complex queries, data integrity   |
| Driver               | `mongoose` / `mongodb`             | `mysql2` / `sequelize`            |

---

## Why does it matter?

- **Wrong database choice** can cost months of refactoring
- **Interviews** always ask "When would you use SQL vs NoSQL?"
- **Enterprise jobs** heavily lean toward SQL — your MongoDB experience is supplementary
- Many real-world apps use BOTH (polyglot persistence)
- Understanding trade-offs makes you a senior-level developer

---

## How does it work?

### Decision Framework

```
                        START HERE
                           │
                           ▼
                 ┌────────────────────┐
                 │ Do you need strict │
          Yes ◄──│ data relationships │──► No
          │      │ & transactions?    │      │
          │      └────────────────────┘      │
          ▼                                  ▼
    ┌──────────┐                    ┌────────────────┐
    │ SQL      │                    │ Does schema    │
    │ (MySQL)  │             Yes ◄──│ change often?  │──► No
    └──────────┘             │      └────────────────┘    │
                             ▼                            ▼
                    ┌────────────────┐           ┌────────────────┐
                    │ NoSQL          │           │ Either works!  │
                    │ (MongoDB)      │           │ Go with team's │
                    └────────────────┘           │ familiarity    │
                                                └────────────────┘
```

---

## Visual Diagram

### Side-by-Side Architecture

```
SQL Architecture:                    NoSQL Architecture:
┌──────────────────────┐            ┌──────────────────────┐
│     Application      │            │     Application      │
│     (Express)        │            │     (Express)        │
└──────────┬───────────┘            └──────────┬───────────┘
           │ mysql2                             │ mongoose
           ▼                                    ▼
┌──────────────────────┐            ┌──────────────────────┐
│  MySQL Server        │            │  MongoDB Server      │
│  ┌────────────────┐  │            │  ┌────────────────┐  │
│  │ Database        │  │            │  │ Database        │  │
│  │  ┌──────────┐  │  │            │  │  ┌──────────┐  │  │
│  │  │ Table     │  │  │            │  │  │Collection│  │  │
│  │  │ (rows)    │  │  │            │  │  │(documents│  │  │
│  │  └──────────┘  │  │            │  │  └──────────┘  │  │
│  │  ┌──────────┐  │  │            │  │  Documents can │  │
│  │  │ Table     │  │  │            │  │  be different  │  │
│  │  │ (JOINs)  │  │  │            │  │  shapes!       │  │
│  │  └──────────┘  │  │            │  └────────────────┘  │
│  └────────────────┘  │            └──────────────────────┘
│  Fixed schema        │            Flexible schema
│  ACID transactions   │            Horizontal scaling
│  Complex JOINs       │            Fast reads (embedded)
└──────────────────────┘            └──────────────────────┘
```

### Data Storage Comparison

```
Same data in SQL vs MongoDB:

SQL (3 normalized tables):           MongoDB (1 document):
                                     
customers:                           {
┌────┬─────────┐                       _id: ObjectId("..."),
│ id │ name    │                       name: "Nishant",
├────┼─────────┤                       email: "n@test.com",
│ 1  │ Nishant │                       orders: [
└────┴─────────┘                         {
orders:                                    date: "2024-01-15",
┌────┬─────┬────────┐                     total: 79999,
│ id │c_id │ total  │                     items: [
├────┼─────┼────────┤                       { name: "iPhone", qty: 1 }
│ 1  │  1  │ 79999  │                     ]
└────┴─────┴────────┘                    }
order_items:                           ]
┌─────┬────┬─────┬──────┐           }
│o_id │p_id│ qty │price │
├─────┼────┼─────┼──────┤           1 document = 1 read
│  1  │ 1  │  1  │79999 │           No JOINs needed
└─────┴────┴─────┴──────┘           But: data duplication risk
                                    
3 tables, needs JOINs
But: no data duplication
```

---

## Comprehensive Comparison

```
┌─────────────────────┬────────────────────────┬────────────────────────┐
│ Feature             │ SQL (MySQL)            │ NoSQL (MongoDB)        │
├─────────────────────┼────────────────────────┼────────────────────────┤
│ Data Structure      │ Tables (rows/columns)  │ Collections (documents)│
│ Schema              │ Fixed, predefined      │ Flexible, dynamic      │
│ Query Language      │ SQL (standardized)     │ MQL (MongoDB-specific) │
│ Relationships       │ JOINs (native)         │ $lookup / embed / ref  │
│ Transactions        │ Full ACID              │ Multi-doc since v4.0   │
│ Scaling Strategy    │ Vertical (scale up)    │ Horizontal (scale out) │
│ Data Integrity      │ Strong (constraints)   │ Application-enforced   │
│ Read Performance    │ Good (with indexes)    │ Excellent (embedded)   │
│ Write Performance   │ Good                   │ Excellent              │
│ Complex Queries     │ Excellent (SQL power)  │ Good (agg pipeline)    │
│ Rapid Prototyping   │ Slower (schema first)  │ Faster (no schema)     │
│ Data Duplication    │ Minimal (normalized)   │ Common (embedded)      │
│ Community/Jobs      │ Largest                │ Growing rapidly        │
│ Cost (cloud)        │ Moderate               │ Can be expensive       │
│ Backup/Recovery     │ Mature tools           │ Good tools             │
│ Learning Curve      │ Moderate               │ Lower (for JS devs)   │
│ ORM Support         │ Sequelize, Prisma      │ Mongoose               │
│ Hosting             │ AWS RDS, PlanetScale   │ MongoDB Atlas, AWS     │
├─────────────────────┼────────────────────────┼────────────────────────┤
│ BEST FOR:           │                        │                        │
│ E-commerce          │ ✅ Yes                  │ Partial                │
│ Banking/Finance     │ ✅ Yes                  │ ❌ No                   │
│ Social Media Feed   │ Partial                │ ✅ Yes                  │
│ CMS/Blog            │ ✅ Yes                  │ ✅ Yes                  │
│ IoT/Sensor Data     │ ❌ No                   │ ✅ Yes                  │
│ Analytics           │ ✅ Yes                  │ Partial                │
│ Chat/Real-time      │ Partial                │ ✅ Yes                  │
│ Inventory Mgmt      │ ✅ Yes                  │ ❌ No                   │
│ User Auth           │ ✅ Yes                  │ ✅ Yes                  │
└─────────────────────┴────────────────────────┴────────────────────────┘
```

---

## Code Comparison — Same Feature, Both Databases

```js
// ========== MongoDB / Mongoose ==========
// Schema
const productSchema = new Schema({
  name: { type: String, required: true },
  price: { type: Number, required: true },
  category: { type: Schema.Types.ObjectId, ref: 'Category' }
});

// CRUD
const product = await Product.create({ name: 'iPhone', price: 79999, category: catId });
const products = await Product.find({ price: { $gt: 10000 } }).populate('category');
await Product.updateOne({ _id: id }, { $set: { price: 69999 } });
await Product.deleteOne({ _id: id });

// Aggregation
const stats = await Product.aggregate([
  { $group: { _id: '$category', avg: { $avg: '$price' }, count: { $sum: 1 } } }
]);
```

```js
// ========== MySQL / mysql2 ==========
// Schema (CREATE TABLE)
await pool.query(`
  CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    category_id INT,
    FOREIGN KEY (category_id) REFERENCES categories(id)
  )
`);

// CRUD
const [result] = await pool.query(
  'INSERT INTO products (name, price, category_id) VALUES (?, ?, ?)',
  ['iPhone', 79999, catId]
);
const [products] = await pool.query(
  'SELECT p.*, c.name AS category FROM products p JOIN categories c ON p.category_id = c.id WHERE p.price > ?',
  [10000]
);
await pool.query('UPDATE products SET price = ? WHERE id = ?', [69999, id]);
await pool.query('DELETE FROM products WHERE id = ?', [id]);

// Aggregation
const [stats] = await pool.query(`
  SELECT category_id, ROUND(AVG(price), 2) AS avg, COUNT(*) AS count
  FROM products GROUP BY category_id
`);
```

---

## Real-World Scenario + Full Stack Code

### Scenario: When to use both — Polyglot Persistence

```
E-Commerce Application:
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│  MySQL (Primary Database):          MongoDB (Secondary):     │
│  ┌──────────────────────┐          ┌────────────────────┐   │
│  │ • User accounts      │          │ • Product reviews  │   │
│  │ • Orders & payments  │          │ • Chat messages    │   │
│  │ • Inventory          │          │ • Activity logs    │   │
│  │ • Product catalog    │          │ • User sessions    │   │
│  │ • Financial reports  │          │ • Search indexes   │   │
│  └──────────────────────┘          └────────────────────┘   │
│                                                              │
│  Why MySQL? Data integrity,        Why MongoDB? Flexible     │
│  complex queries, transactions     schema, high write speed, │
│  financial compliance              schema varies per review  │
└──────────────────────────────────────────────────────────────┘
```

```js
// Node.js — Polyglot persistence (using both)
const mysql = require('mysql2/promise');
const mongoose = require('mongoose');

// MySQL for structured, relational data
const sqlPool = mysql.createPool({
  host: 'localhost', user: 'root', password: 'root123', database: 'ecommerce'
});

// MongoDB for flexible, high-volume data
mongoose.connect('mongodb://localhost:27017/ecommerce_flexible');

// Product Review schema (MongoDB — flexible)
const reviewSchema = new mongoose.Schema({
  productId: Number,           // References MySQL products.id
  userId: Number,              // References MySQL customers.id
  rating: { type: Number, min: 1, max: 5 },
  title: String,
  body: String,
  pros: [String],              // Flexible arrays
  cons: [String],
  images: [String],            // Some reviews have images, some don't
  helpful: { yes: Number, no: Number },
  metadata: mongoose.Schema.Types.Mixed  // Any shape
}, { timestamps: true });
const Review = mongoose.model('Review', reviewSchema);

// API: Get product with reviews (data from both databases)
app.get('/api/products/:id', async (req, res) => {
  const productId = req.params.id;
  
  // Get product from MySQL (structured data)
  const [products] = await sqlPool.query(
    `SELECT p.*, c.name AS category FROM products p
     LEFT JOIN categories c ON p.category_id = c.id
     WHERE p.id = ?`,
    [productId]
  );
  
  if (products.length === 0) {
    return res.status(404).json({ error: 'Product not found' });
  }
  
  // Get reviews from MongoDB (flexible data)
  const reviews = await Review.find({ productId: parseInt(productId) })
    .sort({ createdAt: -1 })
    .limit(10);
  
  // Get review stats from MongoDB
  const stats = await Review.aggregate([
    { $match: { productId: parseInt(productId) } },
    { $group: {
      _id: null,
      avgRating: { $avg: '$rating' },
      totalReviews: { $sum: 1 },
      ratingBreakdown: {
        $push: '$rating'
      }
    }}
  ]);
  
  res.json({
    product: products[0],   // From MySQL
    reviews,                // From MongoDB
    reviewStats: stats[0]   // From MongoDB aggregation
  });
});

// API: Add review (MongoDB — flexible schema)
app.post('/api/products/:id/reviews', async (req, res) => {
  const review = await Review.create({
    productId: parseInt(req.params.id),
    userId: req.body.userId,
    rating: req.body.rating,
    title: req.body.title,
    body: req.body.body,
    pros: req.body.pros || [],
    cons: req.body.cons || [],
    images: req.body.images || [],
    metadata: req.body.metadata  // Any extra data the frontend sends
  });
  
  res.status(201).json(review);
});
```

```js
// React — Product page with data from both databases
function ProductPage({ productId }) {
  const [product, setProduct] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [stats, setStats] = useState(null);

  useEffect(() => {
    axios.get(`/api/products/${productId}`).then(({ data }) => {
      setProduct(data.product);      // From MySQL
      setReviews(data.reviews);      // From MongoDB
      setStats(data.reviewStats);    // From MongoDB
    });
  }, [productId]);

  if (!product) return <p>Loading...</p>;

  return (
    <div>
      <h1>{product.name}</h1>
      <p>₹{product.price} | Category: {product.category}</p>
      <p>Stock: {product.stock}</p>
      
      {stats && (
        <div>
          <h3>Reviews ({stats.totalReviews})</h3>
          <p>Average Rating: {'⭐'.repeat(Math.round(stats.avgRating))} ({stats.avgRating.toFixed(1)})</p>
        </div>
      )}
      
      {reviews.map(review => (
        <div key={review._id} style={{ borderBottom: '1px solid #ddd', padding: '12px 0' }}>
          <strong>{'⭐'.repeat(review.rating)}</strong>
          <h4>{review.title}</h4>
          <p>{review.body}</p>
          {review.pros.length > 0 && <p>👍 Pros: {review.pros.join(', ')}</p>}
          {review.cons.length > 0 && <p>👎 Cons: {review.cons.join(', ')}</p>}
        </div>
      ))}
    </div>
  );
}
```

**Output:**
```json
{
  "product": {
    "id": 1, "name": "iPhone 15", "price": "79999.00",
    "category": "Electronics", "stock": 50
  },
  "reviews": [
    {
      "_id": "65abc123...", "productId": 1, "rating": 5,
      "title": "Best phone ever!", "body": "Amazing camera...",
      "pros": ["Camera", "Battery", "Display"],
      "cons": ["Price", "No charger in box"],
      "images": ["photo1.jpg"], "createdAt": "2024-01-15T..."
    }
  ],
  "reviewStats": {
    "avgRating": 4.3, "totalReviews": 125
  }
}
```

---

## Impact

| If You Choose Wrong Database...          | What Happens                                    |
|------------------------------------------|-------------------------------------------------|
| MongoDB for financial transactions       | Data inconsistency, money lost, compliance fail  |
| MySQL for IoT sensor data (billions)     | Can't scale horizontally, performance collapse   |
| MongoDB for complex reporting            | Aggregation pipeline becomes nightmarish         |
| MySQL for rapidly changing schemas       | Endless ALTER TABLE migrations                   |
| Only know one database                   | Limited career options, wrong tool for half the jobs |

---

## Practice Exercises

### Easy
1. List 5 use cases best suited for SQL and 5 for NoSQL
2. Write the same CRUD operations in both MongoDB and MySQL
3. Compare the output format of a JOIN (SQL) vs populate (Mongoose)

### Medium
4. Design a chat application schema in both MongoDB and MySQL — compare complexity
5. Implement the same API endpoint using both databases and benchmark performance
6. Convert a MongoDB embedded document design to a normalized SQL schema

### Hard
7. Build an app using polyglot persistence: MySQL for users/orders, MongoDB for analytics/logs
8. Migrate a MongoDB collection to MySQL: transform embedded documents into normalized tables with data integrity preserved

---

## Interview Q&A

**Q1: When would you choose SQL over NoSQL?**
When you need: strong data integrity (foreign keys, constraints), complex multi-table queries (JOINs), ACID transactions (financial, e-commerce), structured and predictable data, complex reporting/analytics. SQL is the default choice for most business applications.

**Q2: When would you choose NoSQL over SQL?**
When you need: flexible/evolving schemas (CMS, IoT), horizontal scaling (millions of concurrent users), high write throughput (logs, social feeds), hierarchical/nested data (deeply nested documents), rapid prototyping without upfront schema design.

**Q3: What is polyglot persistence?**
Using multiple database types in a single application, choosing the best one for each use case. Example: MySQL for users/orders, MongoDB for product reviews/chat, Redis for caching/sessions, Elasticsearch for search. Complex to manage but optimal for large applications.

**Q4: Can you use JOINs in MongoDB?**
Yes, using `$lookup` in the aggregation pipeline, but it's less performant than SQL JOINs. MongoDB is designed for denormalized data where JOINs aren't needed. Mongoose's `populate()` sends separate queries (N+1 problem). If you find yourself needing many JOINs, a SQL database might be a better fit.

**Q5: "MongoDB is faster than MySQL." True or false?**
It depends on the use case. MongoDB is faster for simple reads of embedded documents (single document fetch vs multi-table JOIN). MySQL is faster for complex queries, aggregations, and filtered searches using indexes. Performance depends on: schema design, indexing, query patterns, data size, and access patterns. Neither is universally faster.

---

| [← Previous: Normalization](./18_Normalization.md) | [Next: Final Project →](./20_Final_Project.md) |
|---|---|
