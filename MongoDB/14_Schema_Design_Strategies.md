# Schema Design Strategies

> 📌 **File:** 14_Schema_Design_Strategies.md | **Level:** SQL Expert → MongoDB

---

## What is it?

Schema design in MongoDB is driven by **application access patterns**, not by data normalization rules. In SQL, you follow 1NF → 2NF → 3NF and let the query planner figure out performance. In MongoDB, YOU design the schema to match your queries — and getting it wrong can't be fixed with a better index.

---

## SQL Parallel — Think of it like this

```
SQL Design Process:
  1. Identify entities
  2. Normalize to 3NF
  3. Add indexes for performance
  4. Done — schema rarely changes

MongoDB Design Process:
  1. List ALL application queries (access patterns)
  2. Identify read/write ratio for each
  3. Design documents to serve the most common queries
  4. Choose embed vs reference for each relationship
  5. Add indexes
  6. Iterate as access patterns evolve
```

---

## The Six Foundational Patterns

### Pattern 1: Attribute Pattern

**Problem:** Products with varied attributes (one has "ram", another has "horsepower").

```javascript
// ❌ SQL approach: EAV table or sparse columns
// products: id | name | price | color | size | ram | storage | fuel_type | ...
// Most columns NULL for most products

// ❌ MongoDB anti-pattern: Many optional top-level fields
{ name: "Laptop", ram: "16GB", storage: "512GB" }
{ name: "Car", horsepower: "200", fuelType: "gasoline" }

// ✅ Attribute Pattern: Uniform array of key-value pairs
{
  name: "Laptop",
  price: 999,
  attributes: [
    { key: "ram", value: "16GB", unit: "gigabytes" },
    { key: "storage", value: "512", unit: "gigabytes" },
    { key: "cpu", value: "i7-12700H", unit: null }
  ]
}

// Index: { "attributes.key": 1, "attributes.value": 1 }
// Query: db.products.find({ attributes: { $elemMatch: { key: "ram", value: "16GB" } } })
```

### Pattern 2: Bucket Pattern

**Problem:** Time-series data with millions of small documents (IoT, logs, metrics).

```javascript
// ❌ One document per measurement (too many documents)
{ sensorId: "temp-1", value: 22.5, timestamp: ISODate("2024-01-01T00:00:00") }
{ sensorId: "temp-1", value: 22.6, timestamp: ISODate("2024-01-01T00:01:00") }
// 1 million readings = 1 million documents = massive index overhead

// ✅ Bucket Pattern: Group measurements into time buckets
{
  sensorId: "temp-1",
  date: ISODate("2024-01-01"),          // One document per day
  measurements: [
    { time: ISODate("...T00:00:00"), value: 22.5 },
    { time: ISODate("...T00:01:00"), value: 22.6 },
    // ... 1440 readings per day
  ],
  stats: {                                // Pre-computed
    min: 20.1, max: 28.3, avg: 23.7, count: 1440
  }
}
// 365 documents per year vs 525,600 documents
// Index on { sensorId: 1, date: -1 } — much smaller
```

### Pattern 3: Computed Pattern

**Problem:** Expensive aggregations run on every read.

```javascript
// ❌ Calculate on every request
// db.reviews.aggregate([{ $match: { productId } }, { $group: { avg, count } }])
// Slow when product has 50,000 reviews

// ✅ Computed Pattern: Pre-compute and store
{
  _id: ObjectId("..."),
  name: "Laptop",
  price: 999,
  ratings: {
    average: 4.5,           // Updated on each review
    count: 1523,
    distribution: { 5: 800, 4: 400, 3: 200, 2: 80, 1: 43 }
  }
}

// On new review:
db.products.updateOne(
  { _id: productId },
  {
    $inc: {
      "ratings.count": 1,
      [`ratings.distribution.${review.rating}`]: 1
    },
    $set: {
      "ratings.average": newAverage  // Recalculate
    }
  }
)
```

### Pattern 4: Outlier Pattern

**Problem:** Most documents are small, but a few are enormous.

```javascript
// Most products have 10-100 reviews (embed fine)
// Some products have 50,000+ reviews (exceeds 16MB)

// ✅ Outlier Pattern: Embed up to a limit, overflow to separate collection
{
  _id: ObjectId("..."),
  name: "Popular Widget",
  reviews: [/* first 100 reviews */],
  hasOverflow: true,                // Flag
  reviewCount: 50000
}

// Overflow stored separately:
// product_reviews: { productId: ObjectId("..."), reviews: [/* next batch */] }

// Read logic:
async function getReviews(productId, page) {
  const product = await products.findOne({ _id: productId });
  if (!product.hasOverflow || page === 1) {
    return product.reviews.slice(0, 10);
  }
  // Fetch from overflow collection for later pages
  return await productReviews.findOne({ productId })
    .then(doc => doc.reviews.slice((page-1)*10, page*10));
}
```

### Pattern 5: Schema Versioning Pattern

**Problem:** Schema evolves over time. Old documents have different shapes.

```javascript
// ✅ Add a version field to every document
{ schemaVersion: 1, name: "John", address: "123 Main St" }

// After schema change:
{ schemaVersion: 2, name: "John", address: { street: "123 Main", city: "NYC", state: "NY" } }

// Application handles both versions:
function normalizeCustomer(doc) {
  if (doc.schemaVersion === 1) {
    return { ...doc, address: { street: doc.address } };
  }
  return doc;
}

// Gradual migration with background job:
db.customers.find({ schemaVersion: { $lt: 2 } }).forEach(doc => {
  db.customers.updateOne({ _id: doc._id }, {
    $set: {
      schemaVersion: 2,
      address: { street: doc.address, city: "Unknown" }
    }
  });
});
```

### Pattern 6: Polymorphic Pattern

**Problem:** Different entity types in the same collection (SQL: table-per-type inheritance).

```javascript
// SQL: products, electronics, clothing, books tables with inheritance
// MongoDB: Single collection with type discriminator

db.products.insertMany([
  {
    type: "electronics",
    name: "Laptop",
    price: 999,
    specs: { ram: "16GB", storage: "512GB" },
    warranty: { months: 24 }
  },
  {
    type: "clothing",
    name: "T-Shirt",
    price: 29,
    sizes: ["S", "M", "L"],
    material: "Cotton"
  },
  {
    type: "book",
    name: "MongoDB Guide",
    price: 49,
    author: "Jane Doe",
    pages: 450,
    isbn: "978-0-123456-78-9"
  }
])

// Query by type:
db.products.find({ type: "electronics" })

// Partial index per type:
db.products.createIndex(
  { "specs.ram": 1 },
  { partialFilterExpression: { type: "electronics" } }
)
```

---

## E-Commerce Schema Design (Complete)

```javascript
// ═══ PRODUCTS ═══
{
  _id: ObjectId("..."),
  sku: "LAPTOP-DELL-001",
  name: "Dell XPS 15",
  slug: "dell-xps-15",
  description: "Professional laptop...",
  price: NumberDecimal("1299.99"),
  compareAtPrice: NumberDecimal("1499.99"),
  
  // Embedded: category info (read together, rarely changes)
  category: {
    _id: ObjectId("..."),
    name: "Laptops",
    path: "Electronics > Computers > Laptops"
  },
  
  brand: "Dell",
  
  // Embedded: bounded array
  images: [
    { url: "/img/xps15-front.jpg", alt: "Front view", isPrimary: true },
    { url: "/img/xps15-side.jpg", alt: "Side view", isPrimary: false }
  ],
  
  // Attribute pattern for flexible specs
  specs: [
    { key: "RAM", value: "16GB" },
    { key: "Storage", value: "512GB SSD" },
    { key: "Display", value: "15.6\" OLED" }
  ],
  
  // Computed pattern for ratings
  ratings: { average: 4.6, count: 342 },
  
  // Subset pattern: only recent reviews
  recentReviews: [
    { userId: ObjectId("..."), name: "John", rating: 5, text: "Amazing!", date: ISODate("...") }
  ],
  
  // Inventory
  stock: 45,
  lowStockThreshold: 10,
  
  // SEO
  seo: { title: "Dell XPS 15 Laptop", description: "...", keywords: ["dell", "laptop"] },

  tags: ["laptop", "dell", "professional", "oled"],
  isActive: true,
  createdAt: ISODate("..."),
  updatedAt: ISODate("...")
}

// Indexes:
// { sku: 1 } unique
// { slug: 1 } unique
// { "category._id": 1, price: 1 }
// { tags: 1 }
// { name: "text", description: "text" }
// { isActive: 1, stock: 1 } partial

// ═══ ORDERS ═══
{
  _id: ObjectId("..."),
  orderNumber: "ORD-2024-001234",
  
  // Extended reference: customer snapshot
  customerId: ObjectId("..."),
  customer: { name: "John Doe", email: "john@example.com" },
  
  // Embedded items with product snapshots
  items: [
    {
      productId: ObjectId("..."),
      sku: "LAPTOP-DELL-001",
      name: "Dell XPS 15",
      price: NumberDecimal("1299.99"),
      quantity: 1,
      subtotal: NumberDecimal("1299.99")
    }
  ],
  
  // Embedded address (snapshot at time of order)
  shippingAddress: {
    name: "John Doe",
    street: "123 Main St",
    city: "New York",
    state: "NY",
    zip: "10001"
  },
  
  payment: {
    method: "credit_card",
    last4: "4242",
    chargeId: "ch_xxx"
  },
  
  subtotal: NumberDecimal("1299.99"),
  tax: NumberDecimal("115.37"),
  shipping: NumberDecimal("0.00"),
  total: NumberDecimal("1415.36"),
  
  status: "shipped",
  statusHistory: [
    { status: "pending", timestamp: ISODate("...") },
    { status: "confirmed", timestamp: ISODate("...") },
    { status: "shipped", timestamp: ISODate("..."), trackingNumber: "1Z..." }
  ],
  
  createdAt: ISODate("..."),
  updatedAt: ISODate("...")
}

// Indexes:
// { orderNumber: 1 } unique
// { customerId: 1, createdAt: -1 }
// { status: 1, createdAt: -1 }
// { createdAt: 1 } for reporting

// ═══ CUSTOMERS ═══
{
  _id: ObjectId("..."),
  email: "john@example.com",
  password: "$2b$10$hashedpassword",
  
  profile: {
    firstName: "John",
    lastName: "Doe",
    phone: "+1-555-0123",
    avatar: "/img/avatars/john.jpg"
  },
  
  // Embedded: bounded (max 5)
  addresses: [
    { label: "Home", street: "123 Main", city: "NYC", state: "NY", zip: "10001", isDefault: true }
  ],
  
  // Computed
  orderStats: {
    totalOrders: 12,
    totalSpent: NumberDecimal("4523.87"),
    lastOrderDate: ISODate("...")
  },
  
  preferences: { newsletter: true, theme: "dark" },
  
  roles: ["customer"],
  isActive: true,
  createdAt: ISODate("..."),
  updatedAt: ISODate("...")
}

// Indexes:
// { email: 1 } unique
// { "profile.lastName": 1, "profile.firstName": 1 }
```

---

## Anti-Patterns

### ❌ God Document (Too Much Embedding)

```javascript
// Everything in one document — user + orders + reviews + activity + settings
{
  name: "John",
  orders: [/* 5000 orders with items */],
  reviews: [/* 500 reviews */],
  activityLog: [/* 100,000 events */],
  // Document = 50MB → ERROR
}
```

### ❌ Fully Normalized (SQL in MongoDB)

```javascript
// 10 collections that all reference each other
// Every read requires 3-5 $lookups
// This is just a slow SQL database
```

### ❌ Massive Arrays

```javascript
// Rule of thumb:
// < 100 items → embed confidently
// 100-1000 → embed with $slice/$push limits
// 1000+ → separate collection
// 10000+ → definitely separate collection
```

---

## Practice Exercises

### Exercise 1: Design from Access Patterns

Given these access patterns for a social media app:
1. Show user profile with follower/following counts
2. Show user's feed (posts from followed users, sorted by time)
3. Show a post with like count, comment count, and top 3 comments
4. Show all comments on a post (paginated)
5. Check if current user has liked a post

Design the collections and document shapes.

### Exercise 2: Schema Review

Review this schema and identify problems:
```javascript
// users: { name, email, allPosts: [...], allComments: [...], allLikes: [...] }
// products: { name, reviewerId, categoryId, warehouseId }
// orders: { userId, productIds: [...] }
```

---

## Interview Q&A

**Q1: How do you approach schema design in MongoDB?**
> Start with access patterns (queries), not entities. List the top 10 most frequent queries. Design documents to serve each query with minimal reads. Choose embed vs reference for each relationship based on read/write ratio, cardinality, and data volatility. Iterate as patterns evolve.

**Q2: What is the Bucket Pattern and when would you use it?**
> Group large numbers of similar small documents into fewer "bucket" documents. Used for time-series data (IoT, metrics, logs). Instead of 1M sensor readings = 1M documents, bucket by hour/day = thousands of documents. Reduces index size, improves query performance, pre-computes statistics.

**Q3: How do you handle schema migration in MongoDB?**
> Add a `schemaVersion` field. Application code handles multiple versions with normalizer functions. Run background migration scripts to convert old documents gradually. No downtime needed — old and new shapes coexist. Very different from SQL's `ALTER TABLE` which is atomic but blocking.

**Q4: What is the Polymorphic Pattern?**
> Store different entity types in the same collection with a type discriminator field. Like SQL table-per-hierarchy inheritance. Simplifies queries across types while allowing type-specific fields. Use partial indexes for type-specific fields.

**Q5: How do you handle many-to-many relationships in MongoDB?**
> Options: (1) Array of ObjectIds on one or both sides. (2) Junction collection (like SQL). (3) Embed denormalized data on one or both sides. Choice depends on array size and query patterns. For small M:N (user enrolled in courses), array of IDs works. For large M:N (users ↔ products liked), use a junction collection with compound index.
