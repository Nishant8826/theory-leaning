# 📌 Creational Patterns

## 🧠 Concept Explanation (Story Format)

You're building a food delivery app. Every time a user places an order, you need to create an Order object. Sometimes it's a delivery order, sometimes pickup. Sometimes with loyalty discounts, sometimes with promo codes.

Without creational patterns: `new Order(userId, restaurantId, items, deliveryAddress, promoCode, loyaltyPoints, isScheduled, scheduledTime, paymentMethod, specialInstructions)` — complex constructors that are error-prone.

Creational patterns solve: **How do we create objects flexibly, correctly, and cleanly?**

---

## 🔍 Key Creational Patterns

### 1. Singleton Pattern

**Intent:** Ensure a class has only ONE instance, with global access.

**When to use:** Database connections, Redis clients, configuration managers, loggers.

```javascript
// Classic Singleton in JavaScript
class DatabasePool {
  static #instance = null;
  #pool;
  
  constructor() {
    if (DatabasePool.#instance) {
      return DatabasePool.#instance; // Return existing instance
    }
    
    this.#pool = new Pool({
      connectionString: process.env.DATABASE_URL,
      max: 20
    });
    
    DatabasePool.#instance = this;
  }
  
  static getInstance() {
    if (!DatabasePool.#instance) {
      new DatabasePool(); // Constructor sets #instance
    }
    return DatabasePool.#instance;
  }
  
  async query(sql, params) {
    return this.#pool.query(sql, params);
  }
  
  async end() {
    await this.#pool.end();
    DatabasePool.#instance = null; // Allow re-creation (for testing)
  }
}

// Usage — always the same instance!
const db1 = DatabasePool.getInstance();
const db2 = DatabasePool.getInstance();
console.log(db1 === db2); // true

// In Node.js, modules are cached — even simpler singleton:
// db.js
const { Pool } = require('pg');
const pool = new Pool({ connectionString: process.env.DATABASE_URL });
module.exports = pool; // Module is cached — same pool everywhere!
// Any require('./db') returns the SAME pool instance
```

**Singleton for Redis:**
```javascript
// redis.js — module-level singleton (Node.js pattern)
const Redis = require('ioredis');

let client = null;

function getRedisClient() {
  if (!client) {
    client = new Redis({
      host: process.env.REDIS_HOST,
      port: process.env.REDIS_PORT,
      retryStrategy: (times) => Math.min(times * 50, 2000)
    });
    
    client.on('error', (err) => console.error('Redis error:', err));
    client.on('connect', () => console.log('Redis connected'));
  }
  return client;
}

module.exports = { getRedisClient };
```

---

### 2. Factory Method Pattern

**Intent:** Define an interface for creating objects, but let subclasses decide which class to instantiate.

**When to use:** When you don't know upfront which class you'll need, or when you want to delegate creation.

```javascript
// Payment processor factory
class PaymentProcessor {
  async charge(amount, currency, details) { throw new Error('Implement charge'); }
  async refund(transactionId, amount) { throw new Error('Implement refund'); }
}

class StripeProcessor extends PaymentProcessor {
  async charge(amount, currency, details) {
    const charge = await stripe.charges.create({
      amount: Math.round(amount * 100),
      currency,
      payment_method: details.paymentMethodId,
      confirm: true
    });
    return { transactionId: charge.id, status: charge.status };
  }
  
  async refund(transactionId, amount) {
    await stripe.refunds.create({ charge: transactionId, amount: Math.round(amount * 100) });
    return { status: 'refunded' };
  }
}

class PayPalProcessor extends PaymentProcessor {
  async charge(amount, currency, details) {
    const order = await paypalClient.execute(new paypal.orders.OrdersCreateRequest(), {
      intent: 'CAPTURE',
      purchase_units: [{ amount: { value: amount.toString(), currency_code: currency } }]
    });
    return { transactionId: order.result.id, status: 'success' };
  }
  
  async refund(transactionId, amount) {
    await paypalClient.execute(new paypal.payments.CapturesRefundRequest(transactionId));
    return { status: 'refunded' };
  }
}

class RazorpayProcessor extends PaymentProcessor {
  async charge(amount, currency, details) {
    const order = await razorpay.orders.create({ amount: amount * 100, currency });
    return { transactionId: order.id, status: 'created' };
  }
  
  async refund(transactionId, amount) {
    await razorpay.payments.refund(transactionId, { amount: amount * 100 });
    return { status: 'refunded' };
  }
}

// Factory — creates the right processor
class PaymentProcessorFactory {
  static create(gateway) {
    const processors = {
      stripe: StripeProcessor,
      paypal: PayPalProcessor,
      razorpay: RazorpayProcessor
    };
    
    const ProcessorClass = processors[gateway];
    if (!ProcessorClass) throw new Error(`Unknown payment gateway: ${gateway}`);
    
    return new ProcessorClass();
  }
}

// Usage
const processor = PaymentProcessorFactory.create(user.preferredGateway);
const result = await processor.charge(99.99, 'USD', paymentDetails);
// Adding Stripe India: just add StripeIndiaProcessor, update processors map — no code change elsewhere!
```

---

### 3. Abstract Factory Pattern

**Intent:** Create families of related objects without specifying their concrete classes.

**When to use:** When you need to create multiple related objects that should work together.

```javascript
// Database family: each DB needs a connection AND a query builder
class DatabaseFactory {
  createConnection() { throw new Error('Implement'); }
  createQueryBuilder() { throw new Error('Implement'); }
  createMigrationRunner() { throw new Error('Implement'); }
}

class PostgresFactory extends DatabaseFactory {
  createConnection() { return new PostgresConnection(process.env.POSTGRES_URL); }
  createQueryBuilder() { return new PostgresQueryBuilder(); }
  createMigrationRunner() { return new PostgresMigrationRunner(); }
}

class MongoFactory extends DatabaseFactory {
  createConnection() { return new MongoConnection(process.env.MONGO_URL); }
  createQueryBuilder() { return new MongoQueryBuilder(); }
  createMigrationRunner() { return new MongoMigrationRunner(); }
}

// Application uses factory — doesn't care which DB!
class Application {
  constructor(dbFactory) {
    this.db = dbFactory.createConnection();
    this.queryBuilder = dbFactory.createQueryBuilder();
    this.migrationRunner = dbFactory.createMigrationRunner();
  }
  
  async initialize() {
    await this.db.connect();
    await this.migrationRunner.run();
  }
}

// Swap entire database family with one change!
const factory = process.env.DB_TYPE === 'postgres' ? new PostgresFactory() : new MongoFactory();
const app = new Application(factory);
await app.initialize();
```

---

### 4. Builder Pattern

**Intent:** Separate construction of complex objects from their representation. Build step by step.

**When to use:** Objects with many optional parameters, step-by-step construction needed.

```javascript
// Email builder — complex object with many optional parts
class Email {
  constructor(builder) {
    this.from = builder.from;
    this.to = builder.to;
    this.subject = builder.subject;
    this.text = builder.text;
    this.html = builder.html;
    this.cc = builder.cc;
    this.bcc = builder.bcc;
    this.attachments = builder.attachments;
    this.replyTo = builder.replyTo;
    this.priority = builder.priority || 'normal';
  }
}

class EmailBuilder {
  from(address) { this._from = address; return this; }
  to(address) { this._to = Array.isArray(address) ? address : [address]; return this; }
  subject(text) { this._subject = text; return this; }
  body(text) { this._text = text; return this; }
  htmlBody(html) { this._html = html; return this; }
  cc(address) { this._cc = address; return this; }
  bcc(address) { this._bcc = address; return this; }
  attach(filename, content) {
    this._attachments = this._attachments || [];
    this._attachments.push({ filename, content });
    return this;
  }
  replyTo(address) { this._replyTo = address; return this; }
  highPriority() { this._priority = 'high'; return this; }
  
  build() {
    if (!this._from) throw new Error('From address required');
    if (!this._to || !this._to.length) throw new Error('To address required');
    if (!this._subject) throw new Error('Subject required');
    
    return new Email({
      from: this._from,
      to: this._to,
      subject: this._subject,
      text: this._text,
      html: this._html,
      cc: this._cc,
      bcc: this._bcc,
      attachments: this._attachments,
      replyTo: this._replyTo,
      priority: this._priority
    });
  }
}

// Clean, readable construction!
const email = new EmailBuilder()
  .from('noreply@myapp.com')
  .to('alice@example.com')
  .subject('Your order has shipped!')
  .htmlBody('<h1>Great news!</h1><p>Your order is on its way.</p>')
  .attach('invoice.pdf', pdfBuffer)
  .highPriority()
  .build();

await mailer.send(email);

// Complex query builder for MongoDB
class MongoQueryBuilder {
  #collection;
  #filter = {};
  #projection = null;
  #sort = {};
  #limitValue = null;
  #skipValue = 0;
  #populateFields = [];
  
  from(collection) { this.#collection = collection; return this; }
  where(field, operator, value) {
    const ops = { '=': '$eq', '!=': '$ne', '>': '$gt', '<': '$lt', '>=': '$gte', '<=': '$lte', 'in': '$in' };
    this.#filter[field] = { [ops[operator] || '$eq']: value };
    return this;
  }
  select(...fields) { this.#projection = Object.fromEntries(fields.map(f => [f, 1])); return this; }
  orderBy(field, direction = 1) { this.#sort[field] = direction; return this; }
  limit(n) { this.#limitValue = n; return this; }
  skip(n) { this.#skipValue = n; return this; }
  
  async execute() {
    let query = this.#collection.find(this.#filter, this.#projection)
      .sort(this.#sort).skip(this.#skipValue);
    if (this.#limitValue) query = query.limit(this.#limitValue);
    return query.toArray();
  }
}

const users = await new MongoQueryBuilder()
  .from(db.collection('users'))
  .where('age', '>=', 18)
  .where('isActive', '=', true)
  .select('name', 'email', 'createdAt')
  .orderBy('createdAt', -1)
  .limit(20)
  .execute();
```

---

### 5. Prototype Pattern

**Intent:** Create objects by cloning an existing object (prototype).

**When to use:** Object creation is expensive, want to avoid subclassing, need configurable objects.

```javascript
class NotificationTemplate {
  constructor(type, subject, body, priority = 'normal') {
    this.type = type;
    this.subject = subject;
    this.body = body;
    this.priority = priority;
    this.attachments = [];
    this.metadata = {};
  }
  
  clone() {
    const cloned = new NotificationTemplate(this.type, this.subject, this.body, this.priority);
    cloned.attachments = [...this.attachments]; // Shallow copy
    cloned.metadata = { ...this.metadata };
    return cloned;
  }
  
  setSubject(subject) { this.subject = subject; return this; }
  setBody(body) { this.body = body; return this; }
}

// Template registry — pre-configured templates
const templates = {
  orderConfirmation: new NotificationTemplate(
    'email',
    'Order Confirmed! #{{orderId}}',
    '<h1>Thank you for your order!</h1>...',
    'high'
  ),
  passwordReset: new NotificationTemplate(
    'email',
    'Reset your password',
    '<p>Click here to reset: {{resetLink}}</p>',
    'high'
  ),
  weeklyDigest: new NotificationTemplate(
    'email',
    'Your weekly summary',
    '<h1>This week on MyApp...</h1>',
    'low'
  )
};

// Clone template and customize — no re-creating from scratch!
function sendOrderConfirmation(order) {
  const notification = templates.orderConfirmation.clone()
    .setSubject(`Order Confirmed! #${order.id}`)
    .setBody(`<h1>Order #${order.id} confirmed!</h1><p>Your items: ${order.items.join(', ')}</p>`);
  
  return mailer.send(notification);
}
```

---

## 🔍 Design Patterns Used
- **Singleton:** Database pool management
- **Factory:** Payment processor selection
- **Builder:** Complex object construction with fluent API

---

## ⚖️ Trade-offs

| Pattern | Pros | Cons |
|---------|------|------|
| Singleton | Single resource, easy global access | Hard to test, hidden dependency |
| Factory | Decouples creation from use | Extra abstraction layer |
| Abstract Factory | Groups related objects | Complex when many families |
| Builder | Readable, flexible construction | More code |
| Prototype | Fast cloning of complex objects | Deep vs shallow copy confusion |

---

## 💼 Interview Questions (WITH SOLUTIONS)

### Q1: Why is Singleton considered an anti-pattern sometimes?

**Solution:**
Singleton problems:
1. **Hidden dependency:** Functions secretly depend on global state — hard to see in signature
2. **Tight coupling:** Can't easily swap the implementation (e.g., for testing)
3. **Testing difficulty:** Can't easily mock the singleton (tests affect each other)
4. **Violation of SRP:** Often Singletons accumulate too many responsibilities

When Singleton IS appropriate:
- Genuinely shared resources (database pool, Redis connection)
- No state that changes per user/request
- Performance-critical (creating new pool per request = terrible)

Fix: Use dependency injection instead of global singleton access.

### Q2: What is the difference between Factory Method and Abstract Factory?

**Solution:**
- **Factory Method:** Creates ONE type of object. Uses inheritance — subclass decides which class to create.
  - `PaymentProcessorFactory.create(type)` → creates ONE processor

- **Abstract Factory:** Creates FAMILIES of related objects. Uses composition — factory creates multiple related objects.
  - `DatabaseFactory` → creates connection AND query builder AND migration runner (all must work together)

Use Factory Method for single object. Use Abstract Factory when you need multiple related objects that must be consistent (e.g., "use PostgreSQL everywhere" vs "use MongoDB everywhere").

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem: Design a notification system using Builder pattern

```javascript
class Notification {
  constructor(builder) {
    this.userId = builder.userId;
    this.type = builder.type;
    this.title = builder.title;
    this.body = builder.body;
    this.channels = builder.channels;
    this.data = builder.data;
    this.scheduledAt = builder.scheduledAt;
    this.expiresAt = builder.expiresAt;
  }
}

class NotificationBuilder {
  #userId; #type; #title; #body; #channels = []; #data = {}; #scheduledAt; #expiresAt;
  
  forUser(userId) { this.#userId = userId; return this; }
  ofType(type) { this.#type = type; return this; }
  withTitle(title) { this.#title = title; return this; }
  withBody(body) { this.#body = body; return this; }
  viaPush() { this.#channels.push('push'); return this; }
  viaEmail() { this.#channels.push('email'); return this; }
  viaSMS() { this.#channels.push('sms'); return this; }
  withData(data) { this.#data = data; return this; }
  scheduledFor(date) { this.#scheduledAt = date; return this; }
  expiresIn(seconds) { this.#expiresAt = new Date(Date.now() + seconds * 1000); return this; }
  
  build() {
    if (!this.#userId) throw new Error('User ID required');
    if (!this.#channels.length) throw new Error('At least one channel required');
    return new Notification({ userId: this.#userId, type: this.#type, title: this.#title, body: this.#body, channels: this.#channels, data: this.#data, scheduledAt: this.#scheduledAt, expiresAt: this.#expiresAt });
  }
}

// Clean, readable
const notification = new NotificationBuilder()
  .forUser(userId)
  .ofType('order_update')
  .withTitle('Your order shipped!')
  .withBody('Estimated delivery: Tomorrow')
  .viaPush()
  .viaEmail()
  .withData({ orderId: '123', trackingNumber: 'UPS12345' })
  .expiresIn(86400) // 24 hours
  .build();
```

---

### Navigation
**Prev:** [03_Design_Patterns_Overview.md](03_Design_Patterns_Overview.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [05_Structural_Patterns.md](05_Structural_Patterns.md)
