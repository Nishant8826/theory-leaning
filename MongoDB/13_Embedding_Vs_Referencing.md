# Embedding vs Referencing

> 📌 **File:** 13_Embedding_Vs_Referencing.md | **Level:** SQL Expert → MongoDB

---

## What is it?

This is the **single most important schema design decision** in MongoDB. Every relationship between entities must be modeled as either **embedded** (data inside the document) or **referenced** (data in a separate collection with an ID link). SQL only has one option — normalized tables with foreign keys. MongoDB gives you the choice, and choosing wrong has severe consequences.

---

## SQL Parallel — Think of it like this

```
SQL World:    EVERYTHING is referenced (normalized)
              orders → order_items → products → categories
              Every relationship = foreign key + JOIN

MongoDB World: You CHOOSE for each relationship:
              Embed (fast reads, data duplication)
              Reference (normalized, needs $lookup or extra query)
```

---

## The Decision Framework

```
┌──────────────────────────────────────────────────────────────────────┐
│                    EMBED vs REFERENCE Decision Tree                 │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Is the data ALWAYS read together?                                  │
│  ├── YES → EMBED                                                    │
│  └── NO  → How often is it read together?                          │
│            ├── Frequently → Consider EMBED (with size check)        │
│            └── Rarely → REFERENCE                                   │
│                                                                      │
│  Can the related data grow UNBOUNDED?                               │
│  ├── YES (unlimited comments/orders/logs) → REFERENCE              │
│  └── NO  (max 5 addresses, 3 sizes) → EMBED                       │
│                                                                      │
│  Does the related data change INDEPENDENTLY?                        │
│  ├── YES (product price changes affect all orders) → REFERENCE     │
│  └── NO  (order captures price at time of purchase) → EMBED        │
│                                                                      │
│  Is the related data SHARED across many documents?                  │
│  ├── YES (category used by 1000 products) → REFERENCE              │
│  └── NO  (shipping address for one order) → EMBED                  │
│                                                                      │
│  Will the document exceed 16MB?                                     │
│  ├── POSSIBLE → REFERENCE                                           │
│  └── NO → EMBED is fine                                             │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Visual Comparison

```
EMBEDDING (Denormalized):
┌─────────────────────────────────────────┐
│  Order Document                         │
│  ┌───────────────────────────────────┐  │
│  │ _id: ObjectId()                   │  │
│  │ customer: {                       │  │  ← Customer data INSIDE order
│  │   name: "John",                   │  │
│  │   email: "john@example.com"       │  │
│  │ }                                 │  │
│  │ items: [                          │  │  ← Items INSIDE order
│  │   { name: "Laptop", price: 999 }, │  │
│  │   { name: "Mouse", price: 29 }    │  │
│  │ ]                                 │  │
│  │ shippingAddress: {                │  │  ← Address INSIDE order
│  │   street: "123 Main", city: "NYC" │  │
│  │ }                                 │  │
│  │ total: 1028                       │  │
│  └───────────────────────────────────┘  │
│  ONE read = ALL data. ZERO joins.       │
└─────────────────────────────────────────┘

REFERENCING (Normalized):
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ orders       │     │ customers    │     │ products     │
│──────────────│     │──────────────│     │──────────────│
│ _id          │     │ _id          │     │ _id          │
│ customerId ──┼────►│ name         │     │ name         │
│ items: [     │     │ email        │     │ price        │
│  {productId}─┼────►│ address      │     │              │
│ ]            │     │              │     │              │
│ total        │     │              │     │              │
└──────────────┘     └──────────────┘     └──────────────┘
THREE collections. Need $lookup or multiple queries.
```

---

## When to Embed

### ✅ Rule 1: Data Read Together → Embed

```javascript
// Product with its specifications — always shown together
{
  _id: ObjectId("..."),
  name: "MacBook Pro",
  price: 2499,
  specs: {
    cpu: "M3 Pro",
    ram: "18GB",
    storage: "512GB SSD",
    display: "14.2-inch Liquid Retina XDR"
  }
}
// The product page ALWAYS shows specs. Embed.
```

### ✅ Rule 2: Data Belongs To Only One Parent → Embed

```javascript
// Order's shipping address — belongs only to this order
{
  _id: ObjectId("..."),
  shippingAddress: {
    street: "123 Main St",
    city: "New York",
    state: "NY",
    zip: "10001"
  }
}
// Each order has exactly one shipping address. Embed.
```

### ✅ Rule 3: Bounded Array (1:Few) → Embed

```javascript
// User with addresses (max 5-10)
{
  _id: ObjectId("..."),
  name: "John",
  addresses: [
    { label: "Home", street: "123 Main", city: "NYC" },
    { label: "Work", street: "456 Office", city: "NYC" }
  ]
}
// Small, bounded array. Embed.
```

### ✅ Rule 4: Data is a Snapshot (Point-in-Time) → Embed

```javascript
// Order captures product info at time of purchase
{
  _id: ObjectId("..."),
  items: [
    {
      productId: ObjectId("..."),  // Reference for tracing
      name: "Laptop",              // Snapshot — won't change
      price: 999.99,               // Price AT time of order
      quantity: 1
    }
  ]
}
// Even if product price changes later, this order is frozen.
```

---

## When to Reference

### ✅ Rule 1: Unbounded Growth → Reference

```javascript
// ❌ BAD: User with all orders embedded (could be thousands)
{
  name: "John",
  orders: [
    { total: 99.99, items: [...] },  // Order 1
    { total: 49.99, items: [...] },  // Order 2
    // ... 10,000 more orders
    // Document exceeds 16MB!
  ]
}

// ✅ GOOD: Separate orders collection with reference
// users collection:
{ _id: ObjectId("user1"), name: "John" }

// orders collection:
{ _id: ObjectId("..."), userId: ObjectId("user1"), total: 99.99 }
{ _id: ObjectId("..."), userId: ObjectId("user1"), total: 49.99 }
// Index: { userId: 1, createdAt: -1 }
```

### ✅ Rule 2: Frequently Updated Shared Data → Reference

```javascript
// ❌ BAD: Product category name embedded in 5000 products
// If category name changes, you must update 5000 documents
{
  name: "Laptop",
  category: { name: "Electonics" }  // Typo in 5000 documents!
}

// ✅ GOOD: Reference the category + cache the name
{
  name: "Laptop",
  categoryId: ObjectId("cat1"),
  categoryName: "Electronics"  // Denormalized cache — update periodically
}
// Or accept stale data and update via background job
```

### ✅ Rule 3: Many-to-Many → Reference

```javascript
// Students enrolled in courses (M:N)
// students collection:
{
  _id: ObjectId("..."),
  name: "Alice",
  enrolledCourseIds: [ObjectId("c1"), ObjectId("c2")]
}

// courses collection:
{
  _id: ObjectId("c1"),
  name: "MongoDB 101",
  enrolledStudentIds: [ObjectId("s1"), ObjectId("s2")]
}
// Both sides keep references. Or use one side only + query.
```

### ✅ Rule 4: Data Accessed Independently → Reference

```javascript
// Blog comments — sometimes viewed without the blog post
// (e.g., "recent comments" widget, moderation dashboard)

// posts collection:
{ _id: ObjectId("..."), title: "My Post", body: "..." }

// comments collection:
{
  _id: ObjectId("..."),
  postId: ObjectId("..."),
  userId: ObjectId("..."),
  text: "Great post!",
  createdAt: new Date()
}
// Comments can be queried independently for moderation
```

---

## Hybrid Pattern — The Best of Both Worlds

```javascript
// Store a reference AND a denormalized subset

// orders collection:
{
  _id: ObjectId("..."),
  customerId: ObjectId("user1"),    // Reference (for joins when needed)
  customer: {                        // Embedded snapshot (for display)
    name: "John Doe",
    email: "john@example.com"
  },
  items: [
    {
      productId: ObjectId("p1"),    // Reference
      name: "Laptop",               // Snapshot
      price: 999.99,                // Snapshot (price at time of order)
      image: "/img/laptop.jpg"      // Snapshot
    }
  ]
}

// Benefits:
// - Read: No $lookup needed (embedded snapshot)
// - Write: Can trace back to original (reference)
// - Update: Run background job to sync denormalized fields
```

---

## Real-World Patterns

### Pattern 1: Extended Reference

```javascript
// Instead of full embed OR bare reference, store "just enough"
{
  authorId: ObjectId("..."),           // Full reference
  author: {                             // Partial embed (display fields only)
    name: "John Doe",
    avatar: "/img/john.jpg"
  }
}
// You can display the author without $lookup
// For full profile, query authors collection
```

### Pattern 2: Subset Pattern

```javascript
// Embed only the most recent/relevant items
{
  _id: ObjectId("..."),
  name: "Gaming Laptop",
  recentReviews: [                     // Last 10 reviews embedded
    { user: "Alice", rating: 5, date: ISODate("...") },
    { user: "Bob", rating: 4, date: ISODate("...") }
  ],
  totalReviews: 1523                   // Count for display
}

// Full reviews in separate collection
// reviews: { productId: ObjectId("..."), user: "...", rating: 5, ... }
```

### Pattern 3: Computed Pattern

```javascript
// Pre-compute aggregated values
{
  _id: ObjectId("..."),
  name: "Gaming Laptop",
  ratings: {
    average: 4.5,                      // Pre-computed
    count: 1523,                       // Pre-computed
    distribution: {                     // Pre-computed
      "5": 800, "4": 400, "3": 200, "2": 80, "1": 43
    }
  }
}
// Updated on each new review with $inc and recalculation
// Avoids aggregating 1523 reviews on every product page load
```

---

## Node.js Implementation

```javascript
// Embedding on creation
app.post('/api/orders', async (req, res) => {
  const { customerId, items } = req.body;
  const db = getDB();

  // Fetch customer for snapshot
  const customer = await db.collection('customers').findOne(
    { _id: new ObjectId(customerId) },
    { projection: { name: 1, email: 1 } }
  );

  // Fetch products for snapshots
  const productIds = items.map(i => new ObjectId(i.productId));
  const products = await db.collection('products')
    .find({ _id: { $in: productIds } })
    .project({ name: 1, price: 1, image: 1 })
    .toArray();

  // Build order with embedded snapshots
  const orderItems = items.map(item => {
    const product = products.find(p => p._id.equals(new ObjectId(item.productId)));
    return {
      productId: product._id,
      name: product.name,           // Snapshot
      price: product.price,         // Snapshot
      image: product.image,         // Snapshot
      quantity: item.quantity
    };
  });

  const order = {
    customerId: new ObjectId(customerId),
    customer: { name: customer.name, email: customer.email }, // Snapshot
    items: orderItems,
    total: orderItems.reduce((sum, i) => sum + parseFloat(i.price.toString()) * i.quantity, 0),
    status: 'pending',
    createdAt: new Date()
  };

  const result = await db.collection('orders').insertOne(order);
  res.status(201).json({ orderId: result.insertedId });
});

// Background job to sync denormalized data
async function syncCustomerNames() {
  const db = getDB();
  const customers = db.collection('customers');
  const orders = db.collection('orders');

  const cursor = customers.find({}).project({ _id: 1, name: 1, email: 1 });

  for await (const customer of cursor) {
    await orders.updateMany(
      { customerId: customer._id },
      { $set: {
        'customer.name': customer.name,
        'customer.email': customer.email
      }}
    );
  }
}
```

---

## Performance Comparison

```
┌──────────────────────────────────────────────────────────────┐
│  Scenario              │ Embedded      │ Referenced          │
├────────────────────────┼───────────────┼─────────────────────┤
│  Read (single entity)  │ ⚡⚡ 1 read    │ 🐌 N+1 reads        │
│  Read (list)           │ ⚡⚡ 1 query   │ 🐌 1 + N queries     │
│  Write (create)        │ ⚡ 1 write     │ ⚡ 1 write           │
│  Update (parent)       │ ⚡ 1 update    │ ⚡ 1 update          │
│  Update (child)        │ ⚡ 1 update    │ ⚡ 1 update          │
│  Update (shared data)  │ 🐌 N updates  │ ⚡ 1 update          │
│  Storage               │ ⚠️ Duplication│ ⚡ No duplication    │
│  Document growth       │ ⚠️ Can grow   │ ⚡ Stable size       │
│  Consistency           │ ⚠️ App manages│ ⚡ Single source     │
├────────────────────────┴───────────────┴─────────────────────┤
│  Rule: Reads > Writes? → Embed                              │
│        Writes > Reads? → Reference                           │
│        Both frequent?  → Hybrid (reference + cached embed)   │
└──────────────────────────────────────────────────────────────┘
```

---

## Common Mistakes

### ❌ Embedding Unbounded Arrays

```javascript
// ❌ User with all activity logs embedded
{ name: "John", activityLog: [ /* 500,000 entries */ ] }
// Document will exceed 16MB. Application will crash.

// ✅ Separate collection with TTL
// activityLogs: { userId: ObjectId("..."), action: "login", timestamp: ... }
```

### ❌ Over-Normalizing (SQL Habit)

```javascript
// ❌ SQL-style normalization in MongoDB
db.users        // { _id, name }
db.emails       // { _id, userId, email }
db.phones       // { _id, userId, phone }
db.preferences  // { _id, userId, theme, lang }

// ✅ Embed all of it
db.users  // { _id, name, email, phone, preferences: { theme, lang } }
```

### ❌ Duplicating Without a Sync Strategy

```javascript
// Embedded customer name in orders — great for reads
// But if customer changes their name, old orders show old name
// Is this acceptable? Usually yes for orders (historical record)
// If not, implement a sync mechanism
```

---

## Practice Exercises

### Exercise 1: Schema Design Decision

For each scenario, decide: Embed or Reference? Justify your answer.

1. **Product ↔ Reviews** (products can have 10,000+ reviews)
2. **User ↔ Settings** (one settings object per user)
3. **Blog Post ↔ Author** (author info needed on every post display)
4. **Order ↔ Line Items** (max 50 items per order)
5. **Chat Room ↔ Messages** (millions of messages)

### Exercise 2: Hybrid Pattern

Design a schema for a social media post that:
- Shows author name and avatar (without extra query)
- Shows like count and comment count
- Shows the 3 most recent comments with commenter names
- Links to full comment list in separate collection

### Exercise 3: Migration

You have a fully normalized MongoDB schema (SQL-style). Redesign it for MongoDB. The current schema:
- `users` (id, name, email)
- `posts` (id, user_id, title, body)
- `comments` (id, post_id, user_id, text)
- `likes` (id, post_id, user_id)

Primary query: "Show a post with author info, comment count, like count, and latest 5 comments."

---

## Interview Q&A

**Q1: When would you embed vs reference in MongoDB?**
> Embed when: data is read together, bounded in size, owned by the parent, accessed as a unit. Reference when: data grows unboundedly, is shared across documents, changes independently, or is accessed separately. Most real-world schemas use a hybrid of both.

**Q2: What is the 16MB document size limit and how does it affect schema design?**
> Every BSON document has a 16MB max. This forces you to reference data that could grow unboundedly (comments, logs, events). Calculate: if an embedded array could exceed ~10,000 items, switch to referencing. This limit is intentional — it prevents pathological document sizes that would hurt performance.

**Q3: How do you handle data consistency with embedded/denormalized data?**
> Accept eventual consistency for non-critical data (category names cached in products). Use Change Streams for near-real-time sync. Run periodic background jobs for batch sync. For critical data, use multi-document transactions. For historical snapshots (order prices), consistency isn't needed — the snapshot IS the correct value.

**Q4: What is the Subset Pattern?**
> Embed only a subset of related data (e.g., last 10 reviews) in the parent document, with the full dataset in a separate collection. This gives fast reads for the common case while supporting pagination/search over the full dataset.

**Q5: If you need to JOIN three collections frequently, should you use MongoDB?**
> Probably not for that specific workload. Frequent multi-collection joins are a signal that the data is inherently relational. Options: (1) Redesign to embed more data. (2) Use $lookup for occasional queries. (3) Use SQL for that component (polyglot persistence). MongoDB shines when most reads are single-document.
