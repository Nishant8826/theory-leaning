# Validation & Schema

> 📌 **File:** 16_Validation_And_Schema.md | **Level:** SQL Expert → MongoDB

---

## What is it?

MongoDB provides **JSON Schema validation** at the database level — think of it as `CREATE TABLE` constraints but defined as JSON rules. This adds the type safety and constraint enforcement that SQL developers expect, while keeping MongoDB's flexibility for schema evolution. You can also use Mongoose schemas for application-level validation.

---

## SQL Parallel — Think of it like this

```
SQL:                                     MongoDB:
NOT NULL                               → required + type check
CHECK (price > 0)                      → minimum: 0 in JSON Schema
UNIQUE                                 → Unique index
FOREIGN KEY                            → ❌ Not supported (application enforced)
DEFAULT value                          → ❌ Not supported at DB level (app/ODM)
VARCHAR(255)                           → maxLength: 255 in JSON Schema
ENUM ('a', 'b', 'c')                   → enum: ["a", "b", "c"]
CREATE TABLE ... (schema)              → db.createCollection({ validator })
ALTER TABLE ADD CONSTRAINT             → db.runCommand({ collMod, validator })
```

---

## Why this is different from SQL (CRITICAL)

### 1. Validation is Optional (Not Default)

```sql
-- SQL: Schema is MANDATORY. Every column has a type.
CREATE TABLE products (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,    -- Enforced by DB
  price DECIMAL(10,2) CHECK (price > 0)  -- Enforced by DB
);
-- INSERT with wrong type: ERROR. Always.
```

```javascript
// MongoDB: No validation by default
db.products.insertOne({ name: 42, price: "free" })  // ✅ Accepted!

// Add validation explicitly:
db.createCollection("products", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["name", "price"],
      properties: {
        name: { bsonType: "string" },
        price: { bsonType: "number", minimum: 0 }
      }
    }
  }
})
// NOW: db.products.insertOne({ name: 42, price: "free" })  → ERROR
```

### 2. Two Levels of Validation

```
┌────────────────────────────────────────────────────────────────┐
│  Level 1: MongoDB Server (JSON Schema Validator)              │
│  ├── Enforced by database engine                               │
│  ├── Cannot be bypassed by application code                   │
│  ├── Catches bad data from ANY client                          │
│  └── Limited: no defaults, no transforms, no virtuals         │
│                                                                │
│  Level 2: Mongoose/Application (Schema + Middleware)          │
│  ├── Enforced by application code                              │
│  ├── Can be bypassed (e.g., direct MongoDB driver calls)      │
│  ├── Rich: defaults, transforms, virtuals, middleware         │
│  └── Only works when data flows through Mongoose              │
│                                                                │
│  SQL comparison: Only Level 1 exists. All validation is       │
│  database-enforced. No need for application-level validation. │
│                                                                │
│  Recommendation: Use BOTH levels.                              │
│  Level 1 = safety net. Level 2 = business logic.              │
└────────────────────────────────────────────────────────────────┘
```

---

## MongoDB Server-Level Validation

### Creating a Collection with Validation

```javascript
db.createCollection("products", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["name", "price", "category", "stock"],
      properties: {
        name: {
          bsonType: "string",
          minLength: 1,
          maxLength: 500,
          description: "Product name - required string"
        },
        price: {
          bsonType: ["double", "decimal"],
          minimum: 0,
          description: "Price must be a non-negative number"
        },
        category: {
          bsonType: "object",
          required: ["name"],
          properties: {
            name: { bsonType: "string" },
            slug: { bsonType: "string" }
          }
        },
        stock: {
          bsonType: "int",
          minimum: 0,
          description: "Stock must be a non-negative integer"
        },
        status: {
          enum: ["active", "draft", "discontinued"],
          description: "Must be one of: active, draft, discontinued"
        },
        tags: {
          bsonType: "array",
          items: { bsonType: "string" },
          maxItems: 20,
          description: "Array of string tags, max 20"
        },
        specs: {
          bsonType: "object",
          additionalProperties: true  // Allow any fields in specs
        },
        createdAt: { bsonType: "date" },
        updatedAt: { bsonType: "date" }
      },
      additionalProperties: true  // Allow fields not listed above
    }
  },
  validationLevel: "strict",      // "strict" (default) or "moderate"
  validationAction: "error"        // "error" (default) or "warn"
})
```

### Modifying Validation on Existing Collection

```javascript
// SQL: ALTER TABLE products ADD CONSTRAINT ...

db.runCommand({
  collMod: "products",
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["name", "price"],
      properties: {
        name: { bsonType: "string", minLength: 1 },
        price: { bsonType: ["double", "decimal"], minimum: 0 },
        email: {
          bsonType: "string",
          pattern: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
        }
      }
    }
  },
  validationLevel: "moderate",    // Only validates inserts + updates to existing valid docs
  validationAction: "error"
})
```

### Validation Levels

```
┌──────────────────────────────────────────────────────────────┐
│  validationLevel   │ Behavior                                │
├────────────────────┼─────────────────────────────────────────┤
│  "strict" (default)│ ALL inserts AND updates are validated   │
│  "moderate"        │ Only validates:                          │
│                    │ - New inserts                            │
│                    │ - Updates to docs that ALREADY pass      │
│                    │ Skips validation for already-invalid docs│
│  "off"             │ No validation (effectively disabled)    │
├────────────────────┴─────────────────────────────────────────┤
│  Use "moderate" when adding validation to existing data      │
│  that might not all conform to the new rules yet.            │
│  Migrate invalid docs gradually, then switch to "strict".    │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│  validationAction  │ Behavior                                │
├────────────────────┼─────────────────────────────────────────┤
│  "error" (default) │ Rejects invalid documents (like SQL)    │
│  "warn"            │ Accepts document but logs a warning     │
│                    │ (useful for gradual rollout)             │
└──────────────────────────────────────────────────────────────┘
```

---

## Mongoose Schema Validation (Application Level)

```javascript
const mongoose = require('mongoose');

const productSchema = new mongoose.Schema({
  name: {
    type: String,
    required: [true, 'Product name is required'],
    trim: true,
    minlength: [1, 'Name cannot be empty'],
    maxlength: [500, 'Name too long']
  },
  slug: {
    type: String,
    unique: true,
    lowercase: true,
    index: true
  },
  price: {
    type: mongoose.Types.Decimal128,
    required: [true, 'Price is required'],
    validate: {
      validator: function(v) {
        return parseFloat(v.toString()) >= 0;
      },
      message: 'Price must be non-negative'
    }
  },
  category: {
    name: { type: String, required: true },
    slug: { type: String, required: true }
  },
  brand: {
    type: String,
    enum: {
      values: ['Dell', 'HP', 'Apple', 'Lenovo', 'Samsung', 'Other'],
      message: '{VALUE} is not a supported brand'
    }
  },
  stock: {
    type: Number,
    required: true,
    min: [0, 'Stock cannot be negative'],
    validate: {
      validator: Number.isInteger,
      message: 'Stock must be an integer'
    }
  },
  tags: {
    type: [String],
    validate: {
      validator: function(v) { return v.length <= 20; },
      message: 'Maximum 20 tags allowed'
    }
  },
  status: {
    type: String,
    enum: ['active', 'draft', 'discontinued'],
    default: 'draft'
  },
  specs: { type: Map, of: String },
  images: [{
    url: { type: String, required: true },
    alt: String,
    isPrimary: { type: Boolean, default: false }
  }],
  ratings: {
    average: { type: Number, default: 0, min: 0, max: 5 },
    count: { type: Number, default: 0, min: 0 }
  },
  isActive: { type: Boolean, default: true }
}, {
  timestamps: true,             // Adds createdAt, updatedAt automatically
  toJSON: { virtuals: true },   // Include virtuals in JSON output
  toObject: { virtuals: true }
});

// ──── Virtual Fields (computed, not stored) ────
productSchema.virtual('displayPrice').get(function() {
  return `$${parseFloat(this.price.toString()).toFixed(2)}`;
});

// ──── Pre-save Middleware ────
productSchema.pre('save', function(next) {
  if (this.isModified('name')) {
    this.slug = this.name.toLowerCase().replace(/[^a-z0-9]+/g, '-');
  }
  next();
});

// ──── Custom Instance Method ────
productSchema.methods.isLowStock = function() {
  return this.stock <= 10;
};

// ──── Custom Static Method ────
productSchema.statics.findByCategory = function(categorySlug) {
  return this.find({ 'category.slug': categorySlug, isActive: true });
};

// ──── Indexes ────
productSchema.index({ 'category.slug': 1, price: 1 });
productSchema.index({ tags: 1 });
productSchema.index({ name: 'text', 'category.name': 'text' });

const Product = mongoose.model('Product', productSchema);
```

### Using Mongoose Validation

```javascript
// Valid document
const laptop = new Product({
  name: 'Dell XPS 15',
  price: mongoose.Types.Decimal128.fromString('1299.99'),
  category: { name: 'Laptops', slug: 'laptops' },
  brand: 'Dell',
  stock: 45,
  tags: ['laptop', 'dell', 'professional']
});

await laptop.save(); // ✅ Passes validation

// Invalid document
try {
  const bad = new Product({
    name: '',              // Too short
    price: -50,            // Negative
    stock: 3.5,            // Not integer
    brand: 'Unknown',      // Not in enum
    tags: Array(25).fill('x') // Too many tags
  });
  await bad.save();
} catch (err) {
  console.log(err.errors);
  // {
  //   name: { message: 'Name cannot be empty' },
  //   price: { message: 'Price must be non-negative' },
  //   stock: { message: 'Stock must be an integer' },
  //   brand: { message: 'Unknown is not a supported brand' },
  //   tags: { message: 'Maximum 20 tags allowed' }
  // }
}
```

---

## SQL vs MongoDB — Validation Side-by-Side

```sql
-- SQL: Complete constraint definition
CREATE TABLE products (
  id SERIAL PRIMARY KEY,
  name VARCHAR(500) NOT NULL CHECK (LENGTH(name) > 0),
  price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
  stock INT NOT NULL DEFAULT 0 CHECK (stock >= 0),
  status VARCHAR(20) DEFAULT 'draft'
    CHECK (status IN ('active', 'draft', 'discontinued')),
  email VARCHAR(255) CHECK (email ~* '^[^@]+@[^@]+\.[^@]+$'),
  created_at TIMESTAMP DEFAULT NOW()
);

-- Any violation: INSERT fails with constraint error
```

```javascript
// MongoDB: JSON Schema validation (database level)
db.createCollection("products", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["name", "price", "stock"],
      properties: {
        name: { bsonType: "string", minLength: 1, maxLength: 500 },
        price: { bsonType: ["double", "decimal"], minimum: 0 },
        stock: { bsonType: "int", minimum: 0 },
        status: { enum: ["active", "draft", "discontinued"] },
        email: { bsonType: "string", pattern: "^[^@]+@[^@]+\\.[^@]+$" }
      }
    }
  }
})

// Note what's MISSING vs SQL:
// ❌ No DEFAULT values at DB level (use app/Mongoose)
// ❌ No FOREIGN KEY validation
// ❌ No AUTO_INCREMENT
// ❌ No cross-field validation (e.g., endDate > startDate)
//    → Use $expr in query-based validator or application code
```

---

## Node.js — Express API with Validation

```javascript
// Using Mongoose validation in Express
app.post('/api/products', async (req, res) => {
  try {
    const product = new Product(req.body);
    await product.validate(); // Explicit validation (optional — save() also validates)
    const saved = await product.save();
    res.status(201).json(saved);
  } catch (err) {
    if (err.name === 'ValidationError') {
      const errors = Object.values(err.errors).map(e => ({
        field: e.path,
        message: e.message,
        value: e.value
      }));
      return res.status(400).json({ errors });
    }
    if (err.code === 11000) { // Duplicate key (unique index)
      return res.status(409).json({ error: 'Duplicate value', field: Object.keys(err.keyPattern) });
    }
    res.status(500).json({ error: 'Internal server error' });
  }
});
```

---

## Real-World Scenario — Layered Validation Strategy

```javascript
// Layer 1: API input validation (express-validator / Joi / Zod)
const { body, validationResult } = require('express-validator');

app.post('/api/products',
  body('name').isString().trim().isLength({ min: 1, max: 500 }),
  body('price').isFloat({ min: 0 }),
  body('stock').isInt({ min: 0 }),
  body('status').optional().isIn(['active', 'draft', 'discontinued']),
  async (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    // Layer 2: Mongoose validates on save
    const product = new Product(req.body);
    const saved = await product.save(); // Mongoose validation runs here

    // Layer 3: MongoDB validates at write (if validator is set)
    // If Mongoose validation is bypassed (e.g., direct driver call),
    // MongoDB's JSON Schema catches it.

    res.status(201).json(saved);
  }
);
```

---

## Common Mistakes

### ❌ No Validation at All

```javascript
// "MongoDB is schema-less, we don't need validation"
// → 6 months later: chaos
{ name: "Laptop", price: 999 }
{ Name: "Mouse", cost: 29 }          // Different field names
{ name: true, price: "expensive" }   // Wrong types
// Good luck querying this consistently
```

### ❌ Only Mongoose Validation (No DB-Level)

```javascript
// Mongoose validates, but someone uses the native driver:
await db.collection('products').insertOne({ name: 42, price: "free" });
// Mongoose didn't see this — it bypasses Mongoose entirely
// DB-level validation would have caught it

// ✅ Use both: Mongoose for app logic + DB validator as safety net
```

### ❌ Over-Validating (Fighting MongoDB's Flexibility)

```javascript
// Don't try to make MongoDB behave exactly like SQL
// Allow some flexibility — that's the point
validator: {
  $jsonSchema: {
    additionalProperties: false  // ← Rejects ANY field not in the schema
  }
}
// This makes schema evolution painful. Use additionalProperties: true.
```

---

## Practice Exercises

### Exercise 1: Create validation rules for:
1. `customers` collection: email (required, pattern), firstName (required, string), age (optional, integer 13-120)
2. `orders` collection: items (required, array, min 1), total (required, number > 0), status (enum)

### Exercise 2: Migration
Add validation to an existing `products` collection that already has 10,000 documents. Some have incorrect types. Use `validationLevel: "moderate"` to avoid breaking existing data.

### Exercise 3: Layered Validation
Implement 3-layer validation for a user registration endpoint:
- Layer 1: express-validator on input
- Layer 2: Mongoose schema validation
- Layer 3: MongoDB server-level JSON Schema

---

## Interview Q&A

**Q1: How is MongoDB validation different from SQL constraints?**
> SQL constraints are mandatory, database-enforced, and block bad data at the storage level. MongoDB validation is optional, added via JSON Schema, and can be set to warn instead of error. SQL has foreign keys, defaults, and CHECK constraints built-in; MongoDB must implement these through application code or indexes.

**Q2: What's the difference between `validationLevel: "strict"` and `"moderate"`?**
> "strict" validates ALL inserts and updates. "moderate" only validates new inserts and updates to documents that already conform. Use "moderate" when adding validation to existing data that might not all pass, then migrate invalid documents and switch to "strict".

**Q3: Should you use Mongoose validation, MongoDB validation, or both?**
> Both. Mongoose provides rich application-level validation (defaults, transforms, middleware, virtuals). MongoDB server validation is a safety net that catches bad data from any client (scripts, admin tools, other services). Mongoose is your primary defense; MongoDB validator is your backup.

**Q4: Can MongoDB enforce foreign key constraints?**
> No. MongoDB has no foreign key constraints. Referential integrity must be enforced by application code, Mongoose middleware, or transactions. This is a fundamental difference from SQL and a conscious design choice — it enables horizontal scaling (sharding) without cross-shard constraint checks.

**Q5: How do you handle schema migration in MongoDB vs SQL?**
> SQL: `ALTER TABLE` — atomic, may lock table, requires downtime for large tables. MongoDB: No migration needed — old and new document shapes coexist. Use schemaVersion field, application normalizers, and gradual background migration. Zero downtime. Trade-off: application must handle multiple schema versions.
