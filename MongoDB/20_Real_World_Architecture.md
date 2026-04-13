# Real-World Architecture

> 📌 **File:** 20_Real_World_Architecture.md | **Level:** SQL Expert → MongoDB

---

## What is it?

This chapter puts everything together into a production-ready backend architecture using MongoDB with Node.js/Express. It covers project structure, error handling, authentication, file uploads, real-time features, testing, and deployment patterns — the same patterns you'd use in a SQL-backed project, adapted for MongoDB.

---

## Production Project Structure

```
ecommerce-api/
├── src/
│   ├── config/
│   │   ├── db.js                  # MongoDB connection
│   │   ├── redis.js               # Redis connection
│   │   └── env.js                 # Environment validation
│   ├── models/
│   │   ├── Product.js             # Mongoose models
│   │   ├── Customer.js
│   │   ├── Order.js
│   │   └── Review.js
│   ├── routes/
│   │   ├── products.js
│   │   ├── customers.js
│   │   ├── orders.js
│   │   └── auth.js
│   ├── middleware/
│   │   ├── auth.js                # JWT authentication
│   │   ├── validate.js            # Input validation
│   │   ├── errorHandler.js        # Global error handler
│   │   └── rateLimiter.js         # Rate limiting
│   ├── services/
│   │   ├── productService.js      # Business logic
│   │   ├── orderService.js
│   │   └── emailService.js
│   ├── utils/
│   │   ├── ApiError.js            # Custom error class
│   │   ├── pagination.js          # Pagination helper
│   │   └── logger.js              # Winston/Pino logger
│   └── app.js                     # Express app setup
├── tests/
│   ├── unit/
│   ├── integration/
│   └── setup.js                   # Test DB setup
├── .env
├── .env.example
├── package.json
└── server.js                      # Entry point
```

---

## Database Connection (Production-Grade)

```javascript
// src/config/db.js
const mongoose = require('mongoose');
const logger = require('../utils/logger');

const connectDB = async () => {
  const options = {
    maxPoolSize: parseInt(process.env.MONGO_POOL_SIZE) || 10,
    minPoolSize: 2,
    serverSelectionTimeoutMS: 5000,
    socketTimeoutMS: 45000,
    retryWrites: true,
    w: 'majority',
    autoIndex: process.env.NODE_ENV !== 'production'
  };

  try {
    await mongoose.connect(process.env.MONGO_URI, options);
    logger.info(`MongoDB connected: ${mongoose.connection.host}`);
  } catch (err) {
    logger.error(`MongoDB connection failed: ${err.message}`);
    process.exit(1);
  }

  // Connection event handlers
  mongoose.connection.on('error', (err) => {
    logger.error(`MongoDB error: ${err.message}`);
  });

  mongoose.connection.on('disconnected', () => {
    logger.warn('MongoDB disconnected. Attempting reconnection...');
  });

  mongoose.connection.on('reconnected', () => {
    logger.info('MongoDB reconnected');
  });
};

// Graceful shutdown
const closeDB = async () => {
  await mongoose.connection.close();
  logger.info('MongoDB connection closed through app termination');
};

process.on('SIGINT', async () => { await closeDB(); process.exit(0); });
process.on('SIGTERM', async () => { await closeDB(); process.exit(0); });

module.exports = { connectDB, closeDB };
```

---

## Error Handling Pattern

```javascript
// src/utils/ApiError.js
class ApiError extends Error {
  constructor(statusCode, message, errors = []) {
    super(message);
    this.statusCode = statusCode;
    this.errors = errors;
    this.isOperational = true;
  }

  static badRequest(msg, errors) { return new ApiError(400, msg, errors); }
  static unauthorized(msg) { return new ApiError(401, msg || 'Unauthorized'); }
  static forbidden(msg) { return new ApiError(403, msg || 'Forbidden'); }
  static notFound(msg) { return new ApiError(404, msg || 'Not found'); }
  static conflict(msg) { return new ApiError(409, msg || 'Conflict'); }
  static internal(msg) { return new ApiError(500, msg || 'Internal server error'); }
}

// src/middleware/errorHandler.js
const errorHandler = (err, req, res, next) => {
  let error = { ...err, message: err.message };

  // Mongoose validation error → 400
  if (err.name === 'ValidationError') {
    const errors = Object.values(err.errors).map(e => ({
      field: e.path,
      message: e.message
    }));
    error = ApiError.badRequest('Validation failed', errors);
  }

  // Mongoose duplicate key → 409
  if (err.code === 11000) {
    const field = Object.keys(err.keyPattern)[0];
    error = ApiError.conflict(`Duplicate value for field: ${field}`);
  }

  // Mongoose bad ObjectId → 400
  if (err.name === 'CastError' && err.kind === 'ObjectId') {
    error = ApiError.badRequest(`Invalid ID: ${err.value}`);
  }

  // MongoDB connection error
  if (err.name === 'MongoServerError') {
    logger.error(`MongoDB error: ${err.message}`);
    error = ApiError.internal('Database error');
  }

  const statusCode = error.statusCode || 500;

  res.status(statusCode).json({
    success: false,
    message: error.message,
    errors: error.errors || [],
    ...(process.env.NODE_ENV === 'development' && { stack: err.stack })
  });
};
```

---

## Authentication with MongoDB

```javascript
// src/models/Customer.js (auth-related fields)
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');

const customerSchema = new mongoose.Schema({
  email: {
    type: String,
    required: true,
    unique: true,
    lowercase: true,
    trim: true,
    match: [/^\S+@\S+\.\S+$/, 'Invalid email']
  },
  password: {
    type: String,
    required: true,
    minlength: 8,
    select: false  // Never return password in queries by default
  },
  profile: {
    firstName: { type: String, required: true },
    lastName: { type: String, required: true }
  },
  roles: {
    type: [String],
    enum: ['customer', 'admin', 'vendor'],
    default: ['customer']
  },
  refreshTokens: [String],
  passwordResetToken: String,
  passwordResetExpires: Date,
  isActive: { type: Boolean, default: true },
  lastLogin: Date
}, { timestamps: true });

// Hash password before saving
customerSchema.pre('save', async function(next) {
  if (!this.isModified('password')) return next();
  this.password = await bcrypt.hash(this.password, 12);
  next();
});

// Compare password
customerSchema.methods.comparePassword = async function(candidatePassword) {
  return await bcrypt.compare(candidatePassword, this.password);
};

// Generate JWT
customerSchema.methods.generateAuthToken = function() {
  return jwt.sign(
    { id: this._id, email: this.email, roles: this.roles },
    process.env.JWT_SECRET,
    { expiresIn: process.env.JWT_EXPIRES_IN || '15m' }
  );
};

customerSchema.methods.generateRefreshToken = function() {
  return jwt.sign(
    { id: this._id },
    process.env.JWT_REFRESH_SECRET,
    { expiresIn: '7d' }
  );
};

// src/routes/auth.js
router.post('/register', async (req, res) => {
  const customer = await Customer.create(req.body);
  const token = customer.generateAuthToken();
  const refreshToken = customer.generateRefreshToken();

  // Store refresh token
  customer.refreshTokens.push(refreshToken);
  await customer.save();

  res.status(201).json({ token, refreshToken, customer: {
    id: customer._id,
    email: customer.email,
    name: `${customer.profile.firstName} ${customer.profile.lastName}`
  }});
});

router.post('/login', async (req, res) => {
  const { email, password } = req.body;

  const customer = await Customer.findOne({ email, isActive: true })
    .select('+password');

  if (!customer || !(await customer.comparePassword(password))) {
    throw ApiError.unauthorized('Invalid credentials');
  }

  customer.lastLogin = new Date();
  const token = customer.generateAuthToken();
  const refreshToken = customer.generateRefreshToken();
  customer.refreshTokens.push(refreshToken);
  await customer.save();

  res.json({ token, refreshToken });
});

// src/middleware/auth.js
const auth = async (req, res, next) => {
  const token = req.headers.authorization?.replace('Bearer ', '');
  if (!token) throw ApiError.unauthorized();

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = await Customer.findById(decoded.id).select('-password');
    if (!req.user || !req.user.isActive) throw ApiError.unauthorized();
    next();
  } catch (err) {
    throw ApiError.unauthorized('Invalid token');
  }
};

const authorize = (...roles) => (req, res, next) => {
  if (!roles.some(role => req.user.roles.includes(role))) {
    throw ApiError.forbidden('Insufficient permissions');
  }
  next();
};
```

---

## Service Layer Pattern

```javascript
// src/services/orderService.js
const Order = require('../models/Order');
const Product = require('../models/Product');
const Customer = require('../models/Customer');
const ApiError = require('../utils/ApiError');
const mongoose = require('mongoose');

class OrderService {
  async createOrder(customerId, orderData) {
    const session = await mongoose.startSession();

    try {
      let order;

      await session.withTransaction(async () => {
        // Validate and get products
        const productIds = orderData.items.map(i => i.productId);
        const products = await Product.find({ _id: { $in: productIds } })
          .session(session);

        // Build order items with price snapshots
        const items = [];
        for (const item of orderData.items) {
          const product = products.find(p => p._id.equals(item.productId));
          if (!product) throw ApiError.notFound(`Product ${item.productId} not found`);
          if (product.stock < item.quantity) {
            throw ApiError.badRequest(`Insufficient stock for ${product.name}`);
          }

          // Decrement stock
          await Product.updateOne(
            { _id: product._id, stock: { $gte: item.quantity } },
            { $inc: { stock: -item.quantity } },
            { session }
          );

          const price = parseFloat(product.price.toString());
          items.push({
            productId: product._id,
            name: product.name,
            price: product.price,
            quantity: item.quantity,
            subtotal: mongoose.Types.Decimal128.fromString(
              (price * item.quantity).toFixed(2)
            )
          });
        }

        const total = items.reduce(
          (sum, i) => sum + parseFloat(i.subtotal.toString()), 0
        );

        // Get customer snapshot
        const customer = await Customer.findById(customerId)
          .select('profile.firstName profile.lastName email')
          .session(session);

        order = await Order.create([{
          customerId,
          customer: {
            name: `${customer.profile.firstName} ${customer.profile.lastName}`,
            email: customer.email
          },
          items,
          total: mongoose.Types.Decimal128.fromString(total.toFixed(2)),
          shippingAddress: orderData.shippingAddress,
          status: 'pending'
        }], { session });

        order = order[0];

        // Update customer stats
        await Customer.updateOne(
          { _id: customerId },
          {
            $inc: { 'orderStats.totalOrders': 1, 'orderStats.totalSpent': total },
            $set: { 'orderStats.lastOrderDate': new Date() }
          },
          { session }
        );
      });

      return order;
    } finally {
      await session.endSession();
    }
  }

  async getOrders(customerId, { page = 1, limit = 20, status } = {}) {
    const filter = { customerId };
    if (status) filter.status = status;

    const [orders, total] = await Promise.all([
      Order.find(filter)
        .sort({ createdAt: -1 })
        .skip((page - 1) * limit)
        .limit(limit)
        .lean(),
      Order.countDocuments(filter)
    ]);

    return { orders, total, page, pages: Math.ceil(total / limit) };
  }

  async updateStatus(orderId, newStatus, userId) {
    const order = await Order.findOneAndUpdate(
      { _id: orderId },
      {
        $set: { status: newStatus, updatedAt: new Date() },
        $push: {
          statusHistory: {
            status: newStatus,
            changedBy: userId,
            timestamp: new Date()
          }
        }
      },
      { new: true, runValidators: true }
    );

    if (!order) throw ApiError.notFound('Order not found');
    return order;
  }
}

module.exports = new OrderService();
```

---

## Change Streams (Real-Time)

```javascript
// MongoDB's equivalent of PostgreSQL LISTEN/NOTIFY or triggers
// Watch for real-time changes on a collection

const pipeline = [
  { $match: {
    operationType: { $in: ['insert', 'update'] },
    'fullDocument.status': 'shipped'
  }}
];

const changeStream = db.collection('orders').watch(pipeline, {
  fullDocument: 'updateLookup'  // Include the full document on updates
});

changeStream.on('change', (change) => {
  console.log('Order shipped:', change.fullDocument._id);

  // Trigger notification to customer
  sendEmail(change.fullDocument.customer.email, {
    subject: 'Your order has shipped!',
    orderId: change.fullDocument._id
  });

  // Push real-time update via WebSocket
  io.to(`user:${change.fullDocument.customerId}`).emit('orderUpdate', {
    orderId: change.fullDocument._id,
    status: 'shipped'
  });
});

// WebSocket integration (Socket.IO)
const http = require('http');
const { Server } = require('socket.io');
const server = http.createServer(app);
const io = new Server(server);

io.on('connection', (socket) => {
  const userId = socket.handshake.auth.userId;
  socket.join(`user:${userId}`);

  socket.on('disconnect', () => {
    socket.leave(`user:${userId}`);
  });
});
```

---

## Testing with MongoDB

```javascript
// tests/setup.js
const { MongoMemoryServer } = require('mongodb-memory-server');
const mongoose = require('mongoose');

let mongoServer;

beforeAll(async () => {
  mongoServer = await MongoMemoryServer.create();
  await mongoose.connect(mongoServer.getUri());
});

afterEach(async () => {
  const collections = mongoose.connection.collections;
  for (const key in collections) {
    await collections[key].deleteMany({});
  }
});

afterAll(async () => {
  await mongoose.disconnect();
  await mongoServer.stop();
});

// tests/integration/product.test.js
const request = require('supertest');
const app = require('../../src/app');
const Product = require('../../src/models/Product');

describe('Products API', () => {
  describe('GET /api/products', () => {
    it('should return paginated products', async () => {
      // Seed test data
      await Product.create([
        { name: 'Laptop', price: 999, stock: 10,
          category: { name: 'Electronics', slug: 'electronics' } },
        { name: 'Mouse', price: 29, stock: 100,
          category: { name: 'Electronics', slug: 'electronics' } }
      ]);

      const res = await request(app)
        .get('/api/products?category=electronics&sort=-price')
        .expect(200);

      expect(res.body.data).toHaveLength(2);
      expect(res.body.data[0].name).toBe('Laptop');
      expect(res.body.pagination.total).toBe(2);
    });
  });

  describe('POST /api/products', () => {
    it('should reject invalid product', async () => {
      const res = await request(app)
        .post('/api/products')
        .send({ name: '', price: -5 })
        .set('Authorization', `Bearer ${adminToken}`)
        .expect(400);

      expect(res.body.errors).toBeDefined();
    });
  });
});
```

---

## Logging & Monitoring

```javascript
// src/utils/logger.js
const pino = require('pino');

const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  transport: process.env.NODE_ENV === 'development'
    ? { target: 'pino-pretty' }
    : undefined,
  serializers: {
    req: (req) => ({
      method: req.method,
      url: req.url,
      userId: req.user?.id
    }),
    err: pino.stdSerializers.err
  }
});

// Request logging middleware
app.use((req, res, next) => {
  const start = Date.now();
  res.on('finish', () => {
    logger.info({
      method: req.method,
      url: req.originalUrl,
      status: res.statusCode,
      duration: Date.now() - start,
      userId: req.user?.id
    });
  });
  next();
});

// MongoDB query logging (development)
if (process.env.NODE_ENV === 'development') {
  mongoose.set('debug', (collectionName, method, query, doc) => {
    logger.debug({ collection: collectionName, method, query });
  });
}
```

---

## Common Mistakes in Production

### ❌ No Connection Pool Tuning

```javascript
// Default pool size (100) is too high for most Node.js apps
// Each connection = ~1MB server memory
// 10-20 is usually sufficient for a single Node.js instance

mongoose.connect(uri, { maxPoolSize: 10 });
```

### ❌ No Health Check Endpoint

```javascript
// Always expose a health endpoint
app.get('/health', async (req, res) => {
  try {
    await mongoose.connection.db.admin().ping();
    res.json({
      status: 'OK',
      db: mongoose.connection.readyState === 1 ? 'connected' : 'disconnected',
      uptime: process.uptime()
    });
  } catch (err) {
    res.status(503).json({ status: 'ERROR', db: 'disconnected' });
  }
});
```

### ❌ No Graceful Shutdown

```javascript
// Always close connections on shutdown
process.on('SIGTERM', async () => {
  logger.info('SIGTERM received. Shutting down gracefully...');
  server.close(async () => {
    await mongoose.connection.close();
    await redis.quit();
    process.exit(0);
  });
  // Force shutdown after 10 seconds
  setTimeout(() => process.exit(1), 10000);
});
```

---

## Practice Exercises

### Exercise 1: Build a Complete API
Build a REST API for a blog platform with:
- User registration and JWT authentication
- CRUD for posts (with author info embedded)
- Comments (referenced, with pagination)
- Like/unlike (with count pre-computation)
- Tag-based search with text index

### Exercise 2: Add Real-Time
Add WebSocket support using Change Streams:
- Notify users when their post receives a comment
- Real-time feed updates when followed users post

### Exercise 3: Production Hardening
Add to your API:
- Rate limiting (express-rate-limit)
- Request validation (Joi/Zod)
- CORS configuration
- Helmet security headers
- Health check endpoint
- Graceful shutdown

---

## Interview Q&A

**Q1: How do you structure a production MongoDB + Node.js application?**
> Separate concerns: models (Mongoose schemas), routes (Express endpoints), services (business logic), middleware (auth, validation, errors), config (DB, env). Use connection pooling, proper error handling for Mongoose errors (ValidationError, CastError, 11000), and the service pattern to keep routes thin.

**Q2: How do you handle real-time features with MongoDB?**
> Change Streams — watch a collection for inserts, updates, and deletes. Combine with Socket.IO/WebSocket to push updates to connected clients. Requires a replica set. Alternative: poll the database (less efficient) or use a message queue (Kafka/RabbitMQ).

**Q3: How do you test MongoDB-backed applications?**
> Use `mongodb-memory-server` for in-memory MongoDB instances in tests. Each test suite gets a clean database. Test at integration level (HTTP requests → database), not just unit. Clear collections between tests. Mock external services but not the database.

**Q4: What's the difference between Mongoose's `select: false` and projection?**
> `select: false` in the schema means the field is NEVER returned in any query unless explicitly requested with `.select('+password')`. Projection on individual queries just controls that specific query. Use `select: false` for sensitive data (passwords, tokens) as a safety default.

**Q5: How do Change Streams compare to SQL triggers?**
> SQL triggers run inside the database engine (synchronous, same transaction). Change Streams run in the application (asynchronous, after the write commits). Change Streams are more flexible (any language, WebSocket integration) but don't guarantee processing (app can restart). SQL triggers guarantee execution but are limited to SQL operations.
