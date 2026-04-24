# 📌 Database Design

## 🧠 Concept Explanation (Story Format)

You're building a Twitter clone. Badly designed tables = slow queries, duplicate data, data inconsistencies.

Good database design = fast queries even at millions of users, no data duplication, easy to extend.

Database design is about making the right choices upfront so you don't need to rewrite everything when you have 1 million users.

---

## 🔍 Key Concepts

### 1. Normalization (PostgreSQL)

**Goal:** Eliminate data duplication and ensure data integrity.

```sql
-- ❌ Bad design: Denormalized (data duplication)
CREATE TABLE orders_bad (
  id SERIAL PRIMARY KEY,
  user_name VARCHAR(100),  -- What if user changes name?
  user_email VARCHAR(100), -- Duplicated in every order!
  product_name VARCHAR(200),
  product_price DECIMAL(10,2), -- What if price changes?
  quantity INT,
  total_price DECIMAL(10,2)
);
-- Problem: If Alice changes email, must update ALL her orders!
-- Problem: If product price changes, what's the historical price?

-- ✅ Good design: Normalized (3NF)
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(100) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE products (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(200) NOT NULL,
  description TEXT,
  current_price DECIMAL(10,2) NOT NULL CHECK (current_price >= 0),
  stock_quantity INT NOT NULL DEFAULT 0 CHECK (stock_quantity >= 0),
  category_id UUID REFERENCES categories(id),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE orders (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id),
  status VARCHAR(50) NOT NULL DEFAULT 'pending',
  subtotal DECIMAL(10,2) NOT NULL,
  tax DECIMAL(10,2) NOT NULL DEFAULT 0,
  shipping_cost DECIMAL(10,2) NOT NULL DEFAULT 0,
  total DECIMAL(10,2) NOT NULL,
  shipping_address JSONB,  -- Snapshot of address at order time
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- order_items preserves price at time of purchase (important!)
CREATE TABLE order_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
  product_id UUID NOT NULL REFERENCES products(id),
  product_name VARCHAR(200) NOT NULL,  -- Snapshot (product name can change!)
  unit_price DECIMAL(10,2) NOT NULL,   -- Snapshot (price can change!)
  quantity INT NOT NULL CHECK (quantity > 0),
  subtotal DECIMAL(10,2) GENERATED ALWAYS AS (unit_price * quantity) STORED
);
```

### 2. Relationships and Foreign Keys

```sql
-- One-to-Many: User has many posts
CREATE TABLE posts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE, 
  -- ON DELETE CASCADE: when user deleted, their posts are also deleted
  title VARCHAR(200) NOT NULL,
  content TEXT NOT NULL,
  is_published BOOLEAN DEFAULT false,
  published_at TIMESTAMP WITH TIME ZONE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Many-to-Many: Users follow Users (self-referential!)
CREATE TABLE user_follows (
  follower_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  following_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  PRIMARY KEY (follower_id, following_id),  -- Composite PK prevents duplicates
  CHECK (follower_id != following_id)  -- Can't follow yourself!
);

-- Many-to-Many: Posts have many Tags
CREATE TABLE tags (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(50) UNIQUE NOT NULL,
  slug VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE post_tags (
  post_id UUID REFERENCES posts(id) ON DELETE CASCADE,
  tag_id UUID REFERENCES tags(id) ON DELETE CASCADE,
  PRIMARY KEY (post_id, tag_id)
);

-- One-to-One: User has one Profile
CREATE TABLE user_profiles (
  user_id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
  bio TEXT,
  avatar_url VARCHAR(500),
  website VARCHAR(200),
  location VARCHAR(100),
  follower_count INT DEFAULT 0,  -- Denormalized counter for performance!
  following_count INT DEFAULT 0
);
```

### 3. Indexes — Critical for Query Performance

```sql
-- Create indexes on frequently queried columns!
CREATE INDEX idx_posts_user_id ON posts(user_id);       -- "Show me all posts by user X"
CREATE INDEX idx_posts_published_at ON posts(published_at DESC); -- "Recent posts first"
CREATE INDEX idx_posts_is_published ON posts(is_published) WHERE is_published = true; -- Partial index!

-- Compound index for common query patterns
CREATE INDEX idx_posts_user_published ON posts(user_id, is_published, created_at DESC);
-- Supports: WHERE user_id = X AND is_published = true ORDER BY created_at DESC

-- Full-text search index (instead of Elasticsearch for simple cases)
CREATE INDEX idx_posts_search ON posts USING GIN(to_tsvector('english', title || ' ' || content));
-- Query: WHERE to_tsvector('english', title || ' ' || content) @@ to_tsquery('redis & caching')

-- JSONB index for querying JSON fields
ALTER TABLE users ADD COLUMN metadata JSONB DEFAULT '{}';
CREATE INDEX idx_users_metadata ON users USING GIN(metadata);
-- Query: WHERE metadata @> '{"plan": "premium"}' -- Uses index!

-- Analyze a slow query
EXPLAIN ANALYZE SELECT * FROM posts WHERE user_id = 'abc' AND is_published = true ORDER BY created_at DESC LIMIT 20;
-- Look for: Seq Scan (bad) vs Index Scan (good)
-- If Seq Scan: Add an index!
```

### 4. ACID Transactions

```sql
-- Transfer money between accounts — must be atomic!
BEGIN;
  UPDATE accounts SET balance = balance - 100 WHERE user_id = 'alice' AND balance >= 100;
  -- Check if update happened (balance was sufficient)
  UPDATE accounts SET balance = balance + 100 WHERE user_id = 'bob';
COMMIT;
-- If anything fails: ROLLBACK (both changes undone)
```

```javascript
// Node.js transactions with pg
async function transferFunds(fromUserId, toUserId, amount) {
  const client = await pool.connect();
  
  try {
    await client.query('BEGIN');
    
    // Deduct from sender (with row locking!)
    const deductResult = await client.query(
      'UPDATE accounts SET balance = balance - $1 WHERE user_id = $2 AND balance >= $1 RETURNING balance',
      [amount, fromUserId]
    );
    
    if (deductResult.rows.length === 0) {
      throw new Error('Insufficient funds or account not found');
    }
    
    // Add to receiver
    await client.query(
      'UPDATE accounts SET balance = balance + $1 WHERE user_id = $2',
      [amount, toUserId]
    );
    
    // Log transaction
    await client.query(
      'INSERT INTO transactions (from_user_id, to_user_id, amount, type) VALUES ($1, $2, $3, $4)',
      [fromUserId, toUserId, amount, 'transfer']
    );
    
    await client.query('COMMIT');
    return { success: true, newBalance: deductResult.rows[0].balance };
    
  } catch (error) {
    await client.query('ROLLBACK');
    throw error;
  } finally {
    client.release(); // ALWAYS release back to pool!
  }
}
```

### 5. MongoDB Schema Design

```javascript
// MongoDB: Embed vs Reference

// ❌ Too much embedding (document gets huge)
const order = {
  _id: ObjectId(),
  userId: ObjectId('user123'),
  items: [
    {
      product: { // Embedded entire product — terrible!
        _id: ObjectId(),
        name: 'Widget',
        price: 29.99,
        description: 'A really long description...',
        images: [...],  // Huge data duplicated in every order!
        reviews: [...]  // Impossible to maintain
      },
      quantity: 2
    }
  ]
};

// ✅ Reference for large/shared documents; Embed for small/owned
const orderSchema = new mongoose.Schema({
  userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true, index: true },
  status: { type: String, enum: ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled'], default: 'pending' },
  items: [{
    productId: { type: mongoose.Schema.Types.ObjectId, ref: 'Product' },
    // Snapshot the important fields at purchase time (product data can change!)
    productName: String,
    unitPrice: Number,
    quantity: { type: Number, min: 1 },
    subtotal: Number
  }],
  // Embed small, order-specific data that won't change
  shippingAddress: {  // Snapshot — address can change later
    street: String, city: String, state: String, zipCode: String, country: String
  },
  totals: {
    subtotal: Number, tax: Number, shipping: Number, total: Number
  },
  createdAt: { type: Date, default: Date.now },
  updatedAt: { type: Date, default: Date.now }
});

// Index for common queries
orderSchema.index({ userId: 1, createdAt: -1 }); // User's order history
orderSchema.index({ status: 1, createdAt: -1 });  // Admin: orders by status

const Order = mongoose.model('Order', orderSchema);

// Embedding rule:
// Embed: One-to-few (< 10 items), owned data, always retrieved together
// Reference: One-to-many (> 10), shared data, sometimes retrieved separately
```

---

## ⚖️ Trade-offs

| Normalized (SQL) | Denormalized (NoSQL) |
|-----------------|---------------------|
| No data duplication | Read performance |
| Easy updates | Need to maintain consistency |
| Complex joins for reads | No joins needed |
| Strong consistency | Eventual consistency possible |
| Harder to change schema | Flexible schema |

---

## 📊 Scalability Discussion

### Counter Problem

```javascript
// ❌ Slow: COUNT(*) every time
const likeCount = await db.query('SELECT COUNT(*) FROM post_likes WHERE post_id = $1', [postId]);

// ✅ Fast: Maintain a counter
// Use a counter column updated atomically
await db.query('UPDATE posts SET likes_count = likes_count + 1 WHERE id = $1', [postId]);

// For massive scale: Use Redis counter (atomic INCR)
await redis.incr(`post:${postId}:likes`);
// Periodically flush Redis counters to DB (write batching!)
```

---

## 💼 Interview Questions (WITH SOLUTIONS)

### Q1: What is database normalization and when would you denormalize?

**Solution:**
Normalization: Organizing data to reduce redundancy and improve data integrity. 1NF → 2NF → 3NF — each level eliminates more types of anomalies.

Denormalize when:
- Read performance is critical and joins are too slow
- Data doesn't change often (product category names)
- You need to snapshot historical values (product price at time of purchase)
- Reporting queries need pre-aggregated data

Common denormalizations:
- Counter columns: `posts.likes_count` (instead of `COUNT(*) FROM likes`)
- Category name on products (avoid join in product listing)
- User name on comments (avoid join when displaying comments)

### Q2: When do you use PostgreSQL vs MongoDB?

**Solution:**
**PostgreSQL:**
- Structured, relational data (orders, users, payments)
- ACID transactions required (financial data)
- Complex queries with multiple joins
- Strong consistency required
- Data schema is well-defined and stable

**MongoDB:**
- Semi-structured or varying data (product catalog with different attributes)
- Document-oriented data (posts with embedded comments)
- Rapid iteration (schema can change without migrations)
- Horizontal scaling from day 1 (built-in sharding)
- Denormalized read performance

For most apps: PostgreSQL for core user/order/payment data, MongoDB for content/activity data.

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem: Design the database schema for a Twitter-like app

```sql
-- Users
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  username VARCHAR(50) UNIQUE NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  display_name VARCHAR(100),
  bio TEXT,
  avatar_url VARCHAR(500),
  follower_count INT DEFAULT 0,    -- Denormalized counter
  following_count INT DEFAULT 0,
  tweet_count INT DEFAULT 0,
  is_verified BOOLEAN DEFAULT false,
  is_banned BOOLEAN DEFAULT false,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tweets
CREATE TABLE tweets (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  content VARCHAR(280) NOT NULL,
  reply_to_id UUID REFERENCES tweets(id) ON DELETE SET NULL,  -- Thread replies
  retweet_of_id UUID REFERENCES tweets(id) ON DELETE SET NULL, -- Retweets
  like_count INT DEFAULT 0,       -- Denormalized
  retweet_count INT DEFAULT 0,    -- Denormalized
  reply_count INT DEFAULT 0,      -- Denormalized
  is_deleted BOOLEAN DEFAULT false,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_tweets_user_id ON tweets(user_id, created_at DESC);
CREATE INDEX idx_tweets_reply_to ON tweets(reply_to_id) WHERE reply_to_id IS NOT NULL;

-- Follows
CREATE TABLE follows (
  follower_id UUID REFERENCES users(id) ON DELETE CASCADE,
  following_id UUID REFERENCES users(id) ON DELETE CASCADE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  PRIMARY KEY (follower_id, following_id),
  CHECK (follower_id != following_id)
);

-- Likes (many-to-many)
CREATE TABLE tweet_likes (
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  tweet_id UUID REFERENCES tweets(id) ON DELETE CASCADE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  PRIMARY KEY (user_id, tweet_id)
);

-- Hashtags
CREATE TABLE hashtags (id SERIAL PRIMARY KEY, name VARCHAR(100) UNIQUE NOT NULL);
CREATE TABLE tweet_hashtags (
  tweet_id UUID REFERENCES tweets(id) ON DELETE CASCADE,
  hashtag_id INT REFERENCES hashtags(id),
  PRIMARY KEY (tweet_id, hashtag_id)
);

CREATE INDEX idx_tweet_hashtags ON tweet_hashtags(hashtag_id, tweet_id);
```

---

### Navigation
**Prev:** [06_Behavioral_Patterns.md](06_Behavioral_Patterns.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [08_API_Design_LLD.md](08_API_Design_LLD.md)
