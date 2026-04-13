# Mongoose Deep Dive

> 📌 **File:** 17_Mongoose_Deep_Dive.md | **Level:** SQL Expert → MongoDB

---

## What is it?

Mongoose is an **ODM (Object Document Mapper)** for MongoDB — the MongoDB equivalent of Sequelize/Prisma for SQL. It adds schemas, validation, middleware (hooks), virtuals, population (lazy join), and a query builder on top of the native MongoDB driver. It's the de facto standard for Node.js + MongoDB applications.

---

## SQL Parallel — Think of it like this

```
SQL ORM (Sequelize/Prisma):               Mongoose:
Model.define('Product', { schema })      → new Schema({ schema })
Model.create({ data })                   → Model.create({ data }) / new Model().save()
Model.findAll({ where })                 → Model.find({ filter })
Model.findByPk(id)                       → Model.findById(id)
Model.update(values, { where })          → Model.updateOne(filter, update)
Model.destroy({ where })                 → Model.deleteOne(filter)
Model.findAll({ include: [Model2] })     → Model.find().populate('ref')
beforeCreate hook                        → pre('save') middleware
afterCreate hook                         → post('save') middleware
Migrations                               → ❌ Not needed (schema in code)
sequelize.sync()                         → ❌ Not needed (auto collection creation)
```

---

## Setup and Connection

```javascript
const mongoose = require('mongoose');

// Connection with options
async function connectDB() {
  await mongoose.connect(process.env.MONGO_URI, {
    // Connection pool
    maxPoolSize: 10,         // Default: 100. Adjust based on load.
    minPoolSize: 2,

    // Timeouts
    serverSelectionTimeoutMS: 5000,  // Fail fast if server is down
    socketTimeoutMS: 45000,

    // Write concern
    w: 'majority',
    retryWrites: true,

    // Indexes
    autoIndex: process.env.NODE_ENV !== 'production' // Don't auto-create indexes in prod
  });

  console.log(`✅ MongoDB connected: ${mongoose.connection.name}`);
}

// Connection events
mongoose.connection.on('error', (err) => console.error('MongoDB error:', err));
mongoose.connection.on('disconnected', () => console.warn('MongoDB disconnected'));

// Graceful shutdown
process.on('SIGINT', async () => {
  await mongoose.connection.close();
  process.exit(0);
});

module.exports = { connectDB };
```

---

## Schema Definition — Complete Example

```javascript
const mongoose = require('mongoose');
const { Schema } = mongoose;

// ═══════════ Product Schema ═══════════
const productSchema = new Schema({
  // ──── Basic Fields ────
  name: {
    type: String,
    required: [true, 'Product name is required'],
    trim: true,
    minlength: [2, 'Name must be at least 2 characters'],
    maxlength: [200, 'Name cannot exceed 200 characters'],
    index: true
  },

  slug: {
    type: String,
    unique: true,
    lowercase: true
  },

  description: {
    type: String,
    maxlength: 5000
  },

  // ──── Price with Decimal128 ────
  price: {
    type: Schema.Types.Decimal128,
    required: [true, 'Price is required'],
    validate: {
      validator: v => parseFloat(v.toString()) >= 0,
      message: 'Price must be non-negative'
    }
  },

  compareAtPrice: Schema.Types.Decimal128,

  // ──── Embedded Object (like SQL sub-table) ────
  category: {
    _id: { type: Schema.Types.ObjectId, ref: 'Category' },
    name: { type: String, required: true },
    slug: String
  },

  brand: {
    type: String,
    enum: {
      values: ['Dell', 'HP', 'Apple', 'Lenovo', 'Samsung', 'Sony', 'Nike', 'Other'],
      message: '{VALUE} is not supported'
    }
  },

  // ──── Array of Strings ────
  tags: {
    type: [String],
    validate: [v => v.length <= 20, 'Max 20 tags']
  },

  // ──── Array of Embedded Objects ────
  images: [{
    url: { type: String, required: true },
    alt: String,
    isPrimary: { type: Boolean, default: false }
  }],

  // ──── Flexible Key-Value (Map) ────
  specs: {
    type: Map,
    of: String
    // specs.set('ram', '16GB')
    // specs.get('ram') → '16GB'
  },

  // ──── Nested Object (Computed Pattern) ────
  ratings: {
    average: { type: Number, default: 0, min: 0, max: 5 },
    count: { type: Number, default: 0, min: 0 }
  },

  // ──── Inventory ────
  stock: {
    type: Number,
    required: true,
    min: [0, 'Stock cannot be negative'],
    validate: { validator: Number.isInteger, message: 'Stock must be integer' }
  },

  // ──── Status ────
  status: {
    type: String,
    enum: ['active', 'draft', 'discontinued'],
    default: 'draft'
  },

  isActive: { type: Boolean, default: true },
  deletedAt: Date  // Soft delete

}, {
  timestamps: true,                    // createdAt, updatedAt auto-managed
  toJSON: { virtuals: true, getters: true },
  toObject: { virtuals: true },
  collection: 'products'               // Explicit collection name
});
```

---

## Virtuals (Computed Properties — Not Stored)

```javascript
// SQL: Views / computed columns / application-level
// Mongoose: Virtual fields — computed on access, not stored in DB

productSchema.virtual('displayPrice').get(function() {
  return `$${parseFloat(this.price.toString()).toFixed(2)}`;
});

productSchema.virtual('isOnSale').get(function() {
  if (!this.compareAtPrice) return false;
  return parseFloat(this.price.toString()) < parseFloat(this.compareAtPrice.toString());
});

productSchema.virtual('isLowStock').get(function() {
  return this.stock <= 10;
});

// Virtual populate — "reverse $lookup"
productSchema.virtual('reviews', {
  ref: 'Review',
  localField: '_id',
  foreignField: 'productId'
});

// Usage:
const product = await Product.findById(id);
console.log(product.displayPrice);  // "$999.99"
console.log(product.isOnSale);      // true/false
console.log(product.isLowStock);    // true/false
```

---

## Middleware (Hooks) — Pre/Post

```javascript
// ──── Pre-save (like SQL triggers / Sequelize hooks) ────
productSchema.pre('save', function(next) {
  // Auto-generate slug from name
  if (this.isModified('name')) {
    this.slug = this.name
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-|-$/g, '');
  }
  next();
});

// ──── Pre-validate ────
productSchema.pre('validate', function(next) {
  if (this.tags) {
    this.tags = [...new Set(this.tags)]; // Remove duplicate tags
  }
  next();
});

// ──── Post-save ────
productSchema.post('save', function(doc) {
  console.log(`Product saved: ${doc.name} (${doc._id})`);
  // Could trigger: cache invalidation, webhook, search index update
});

// ──── Pre/Post for queries ────
productSchema.pre('find', function() {
  // Auto-exclude soft-deleted documents
  if (!this.getQuery().includeSoftDeleted) {
    this.where({ deletedAt: { $exists: false } });
  }
});

productSchema.pre('findOne', function() {
  this.where({ deletedAt: { $exists: false } });
});

// ──── Pre-remove ────
productSchema.pre('deleteOne', { document: true }, async function() {
  // Clean up related data (like SQL CASCADE)
  await mongoose.model('Review').deleteMany({ productId: this._id });
  console.log(`Cleaned up reviews for product ${this._id}`);
});
```

---

## Static Methods and Instance Methods

```javascript
// ──── Static Methods (on the Model — like class methods) ────
// SQL ORM: Product.findActive()

productSchema.statics.findByCategory = function(categorySlug, options = {}) {
  const { page = 1, limit = 20, sort = '-createdAt' } = options;
  return this.find({ 'category.slug': categorySlug, isActive: true })
    .sort(sort)
    .skip((page - 1) * limit)
    .limit(limit)
    .lean();
};

productSchema.statics.search = function(query, options = {}) {
  return this.find(
    { $text: { $search: query }, isActive: true },
    { score: { $meta: 'textScore' } }
  )
  .sort({ score: { $meta: 'textScore' } })
  .limit(options.limit || 20)
  .lean();
};

// Usage:
const laptops = await Product.findByCategory('laptops', { page: 2, limit: 10 });
const results = await Product.search('gaming laptop');

// ──── Instance Methods (on the document — like instance methods) ────
productSchema.methods.addReview = async function(userId, rating, text) {
  const Review = mongoose.model('Review');
  const review = await Review.create({
    productId: this._id,
    userId,
    rating,
    text
  });

  // Update computed ratings
  const stats = await Review.aggregate([
    { $match: { productId: this._id } },
    { $group: { _id: null, avg: { $avg: '$rating' }, count: { $sum: 1 } } }
  ]);

  this.ratings.average = Math.round(stats[0].avg * 10) / 10;
  this.ratings.count = stats[0].count;
  await this.save();

  return review;
};

productSchema.methods.softDelete = function() {
  this.deletedAt = new Date();
  this.isActive = false;
  return this.save();
};

// Usage:
const product = await Product.findById(id);
await product.addReview(userId, 5, 'Amazing product!');
await product.softDelete();
```

---

## Population (Mongoose's "JOIN")

```javascript
// ──── Schema with References ────
const orderSchema = new Schema({
  customerId: { type: Schema.Types.ObjectId, ref: 'Customer', required: true },
  items: [{
    productId: { type: Schema.Types.ObjectId, ref: 'Product', required: true },
    quantity: { type: Number, required: true, min: 1 },
    priceAtPurchase: Schema.Types.Decimal128
  }],
  total: Schema.Types.Decimal128,
  status: { type: String, enum: ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled'] }
}, { timestamps: true });

const Order = mongoose.model('Order', orderSchema);

// ──── Populate = LEFT JOIN equivalent ────

// Simple populate (like SQL: JOIN customers ON orders.customer_id = customers.id)
const order = await Order.findById(orderId)
  .populate('customerId')                      // Replaces ObjectId with full document
  .populate('items.productId');                // Nested populate

// Selective populate (like JOIN with specific columns)
const order = await Order.findById(orderId)
  .populate('customerId', 'name email')        // Only name and email
  .populate('items.productId', 'name price');  // Only name and price

// Populate with conditions
const order = await Order.findById(orderId)
  .populate({
    path: 'customerId',
    select: 'name email',
    match: { isActive: true }                  // Only populate if customer is active
  });

// Virtual populate (reverse lookup)
const product = await Product.findById(productId)
  .populate({
    path: 'reviews',                            // Virtual field
    select: 'rating text userId',
    options: { sort: { createdAt: -1 }, limit: 10 }
  });
```

### Population Performance Warning

```
┌─────────────────────────────────────────────────────────────────┐
│  ⚠️ populate() executes a SEPARATE QUERY for each reference    │
│                                                                 │
│  Order.find().populate('customerId')                            │
│  → Query 1: Find all orders                                    │
│  → Query 2: Find all customers with _id in [list of IDs]      │
│  = 2 queries minimum (N+1 if not batched)                      │
│                                                                 │
│  Order.find().populate('customerId').populate('items.productId')│
│  → Query 1: Find all orders                                    │
│  → Query 2: Find customers                                     │
│  → Query 3: Find products                                      │
│  = 3 queries (still better than N+1, but not a real JOIN)      │
│                                                                 │
│  For hot paths: Embed data instead of populating.               │
│  For cold paths (admin, reports): populate() is fine.           │
│                                                                 │
│  SQL comparison:                                                │
│  Sequelize's include/eager loading has the same N+1 issue       │
│  unless you use raw SQL or proper join configuration.           │
└─────────────────────────────────────────────────────────────────┘
```

---

## Query Building with Mongoose

```javascript
// Mongoose provides a fluent query builder (like Knex.js for SQL)

// Chained query
const products = await Product
  .find({ isActive: true })
  .where('price').gte(50).lte(500)
  .where('stock').gt(0)
  .where('category.slug').equals('electronics')
  .select('name price brand ratings')
  .sort('-ratings.average price')
  .skip(0)
  .limit(20)
  .lean()               // Return plain objects (5-10x faster)
  .exec();

// lean() comparison:
// Without lean(): Returns Mongoose Documents (with .save(), virtuals, etc.)
// With lean(): Returns plain JS objects (no methods, no change tracking)
// Use lean() for READ-ONLY operations (API responses)
// Don't use lean() if you need to call .save() afterward
```

---

## Express API with Mongoose

```javascript
const express = require('express');
const router = express.Router();
const Product = require('../models/Product');

// CREATE
router.post('/', async (req, res) => {
  try {
    const product = await Product.create(req.body);
    res.status(201).json(product);
  } catch (err) {
    if (err.name === 'ValidationError') {
      const errors = Object.values(err.errors).map(e => ({
        field: e.path, message: e.message
      }));
      return res.status(400).json({ errors });
    }
    if (err.code === 11000) {
      return res.status(409).json({ error: 'Duplicate key', fields: err.keyPattern });
    }
    res.status(500).json({ error: err.message });
  }
});

// READ (with pagination + filters)
router.get('/', async (req, res) => {
  const { page = 1, limit = 20, category, brand, minPrice, maxPrice, sort = '-createdAt' } = req.query;

  const filter = { isActive: true };
  if (category) filter['category.slug'] = category;
  if (brand) filter.brand = brand;
  if (minPrice || maxPrice) {
    filter.price = {};
    if (minPrice) filter.price.$gte = parseFloat(minPrice);
    if (maxPrice) filter.price.$lte = parseFloat(maxPrice);
  }

  const [products, total] = await Promise.all([
    Product.find(filter)
      .select('name price brand category ratings images slug')
      .sort(sort)
      .skip((page - 1) * limit)
      .limit(parseInt(limit))
      .lean(),
    Product.countDocuments(filter)
  ]);

  res.json({
    data: products,
    pagination: { page: +page, limit: +limit, total, pages: Math.ceil(total / limit) }
  });
});

// READ (by ID)
router.get('/:id', async (req, res) => {
  const product = await Product.findById(req.params.id).lean();
  if (!product) return res.status(404).json({ error: 'Not found' });
  res.json(product);
});

// UPDATE
router.patch('/:id', async (req, res) => {
  const product = await Product.findByIdAndUpdate(
    req.params.id,
    req.body,
    { new: true, runValidators: true }  // Return updated doc + run validation
  );
  if (!product) return res.status(404).json({ error: 'Not found' });
  res.json(product);
});

// DELETE (soft)
router.delete('/:id', async (req, res) => {
  const product = await Product.findById(req.params.id);
  if (!product) return res.status(404).json({ error: 'Not found' });
  await product.softDelete();
  res.json({ message: 'Product deleted' });
});

module.exports = router;
```

---

## Mongoose vs Native Driver — When to Use Which

```
┌──────────────────────────────────────────────────────────────┐
│  Use Mongoose when:                                         │
│  ├── Building CRUD APIs with consistent schemas              │
│  ├── Need validation, defaults, virtuals, middleware        │
│  ├── Team needs schema documentation in code                │
│  ├── Need populate (lazy joins)                              │
│  └── Rapid development with convention over configuration   │
│                                                             │
│  Use Native Driver when:                                    │
│  ├── Performance is critical (Mongoose adds ~10% overhead)  │
│  ├── Complex aggregation pipelines                           │
│  ├── Bulk operations (insertMany, bulkWrite)                │
│  ├── Change Streams                                          │
│  ├── Need full control over query construction              │
│  └── Working with dynamic/schema-less data                   │
│                                                             │
│  Common pattern: Use Mongoose for CRUD routes,              │
│  use native driver for analytics/aggregation.               │
└──────────────────────────────────────────────────────────────┘
```

---

## Practice Exercises

### Exercise 1: Build a Complete Model
Create a Mongoose model for `Customer` with:
- Required fields: email (unique, validated), firstName, lastName
- Optional: phone (regex validated), addresses array (max 5)
- Computed: fullName virtual
- Middleware: lowercase email on save
- Static: findByEmail
- Instance: addAddress

### Exercise 2: Population Chain
Given models: Order → Customer, Order → Product, Product → Category  
Build a query that returns an order with customer name, product names, and category names.

### Exercise 3: Lean vs Non-Lean Performance
Write a benchmark that queries 1000 products with and without `.lean()`. Measure the time difference.

---

## Interview Q&A

**Q1: What is the difference between Mongoose and the native MongoDB driver?**
> Mongoose adds schemas, validation, middleware, virtuals, population, and a query builder on top of the native driver. The native driver provides direct CRUD and aggregation access. Mongoose is ~10% slower due to overhead but significantly improves developer productivity and code maintainability.

**Q2: What does `.lean()` do and when should you use it?**
> `.lean()` returns plain JavaScript objects instead of Mongoose documents. It skips instantiating change tracking, getters, setters, virtuals, and methods. 5-10x faster for read-only operations. Use for API responses. Don't use when you need `.save()` or Mongoose document features.

**Q3: How does Mongoose `populate()` work internally?**
> It executes a separate query for each populated path — `find({ _id: { $in: [ids] } })`. NOT a database-level join. For 3 populated fields, that's 4 total queries. Mongoose batches IDs to avoid N+1, but it's still slower than embedding.

**Q4: What are Mongoose middleware (hooks) and how do they compare to SQL triggers?**
> Pre/post hooks on operations (save, validate, remove, find). Similar to SQL triggers but run in application code, not the database. Pre-save hooks are commonly used for hashing passwords, generating slugs, and validating data.

**Q5: Should you use `findByIdAndUpdate` or `findById` + `save`?**
> `findByIdAndUpdate` is faster (one DB operation) but skips middleware and some validators (unless `runValidators: true`). `findById` + `save` runs all middleware and validators but requires two DB operations. Use `findByIdAndUpdate` for simple updates; use `find` + `save` when middleware must run.
