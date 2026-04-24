# 📌 Design Patterns Overview

## 🧠 Concept Explanation (Story Format)

You're designing a house. You don't invent doors from scratch — you use a standard door design because it works, everyone understands it, and it fits into your wall properly.

Design patterns are the same — proven, reusable solutions to common software design problems. When a developer says "use the Observer pattern here," everyone on the team immediately understands the approach.

The famous "Gang of Four" book (1994) documented 23 design patterns, grouped into three categories.

---

## 🔍 Three Categories of Design Patterns

```
┌─────────────────────────────────────────────────────────────┐
│                    DESIGN PATTERNS                           │
├─────────────────┬─────────────────┬─────────────────────────┤
│   CREATIONAL    │   STRUCTURAL    │      BEHAVIORAL          │
├─────────────────┼─────────────────┼─────────────────────────┤
│ How objects     │ How objects     │ How objects              │
│ are created     │ are composed    │ communicate              │
├─────────────────┼─────────────────┼─────────────────────────┤
│ Singleton       │ Adapter         │ Observer                 │
│ Factory         │ Decorator       │ Strategy                 │
│ Abstract Factory│ Facade          │ Command                  │
│ Builder         │ Proxy           │ Iterator                 │
│ Prototype       │ Composite       │ Template Method          │
│                 │ Bridge          │ State                    │
│                 │ Flyweight       │ Chain of Responsibility  │
└─────────────────┴─────────────────┴─────────────────────────┘
```

---

## 🏗️ Most Important Patterns for Your Stack

### Creational: How objects are created

**Singleton — One instance shared globally**
```javascript
// Redis client, DB connection pool — you want ONE, not many
class RedisClient {
  static #instance = null;
  
  static getInstance() {
    if (!RedisClient.#instance) {
      RedisClient.#instance = new Redis(process.env.REDIS_URL);
    }
    return RedisClient.#instance;
  }
}

const redis1 = RedisClient.getInstance();
const redis2 = RedisClient.getInstance();
console.log(redis1 === redis2); // true — same instance!
```

**Factory — Create objects without specifying exact class**
```javascript
// Create different logger types based on environment
class LoggerFactory {
  static create(type) {
    switch(type) {
      case 'console': return new ConsoleLogger();
      case 'file': return new FileLogger();
      case 'cloudwatch': return new CloudWatchLogger();
      default: throw new Error(`Unknown logger type: ${type}`);
    }
  }
}

const logger = LoggerFactory.create(process.env.LOGGER_TYPE || 'console');
logger.log('App started'); // Works regardless of type
```

**Builder — Construct complex objects step by step**
```javascript
class QueryBuilder {
  #table = '';
  #conditions = [];
  #orderBy = '';
  #limit = null;
  
  from(table) { this.#table = table; return this; } // Chaining!
  where(condition) { this.#conditions.push(condition); return this; }
  order(field, direction = 'ASC') { this.#orderBy = `ORDER BY ${field} ${direction}`; return this; }
  take(limit) { this.#limit = limit; return this; }
  
  build() {
    let query = `SELECT * FROM ${this.#table}`;
    if (this.#conditions.length) query += ` WHERE ${this.#conditions.join(' AND ')}`;
    if (this.#orderBy) query += ` ${this.#orderBy}`;
    if (this.#limit) query += ` LIMIT ${this.#limit}`;
    return query;
  }
}

const query = new QueryBuilder()
  .from('users')
  .where('age > 18')
  .where('active = true')
  .order('created_at', 'DESC')
  .take(20)
  .build();
// SELECT * FROM users WHERE age > 18 AND active = true ORDER BY created_at DESC LIMIT 20
```

---

### Structural: How objects are composed

**Adapter — Makes incompatible interfaces work together**
```javascript
// Your app uses a specific logger interface, but 3rd party uses a different one
class ThirdPartyLogger {
  writeLog(level, message, meta) { console[level](`[${level}]`, message, meta); }
}

class LoggerAdapter {
  constructor(thirdPartyLogger) {
    this.logger = thirdPartyLogger;
  }
  
  // Your interface: log(message, level)
  log(message, level = 'info') {
    this.logger.writeLog(level, message, {}); // Translate to their interface
  }
  
  error(message) { this.logger.writeLog('error', message, {}); }
}

const logger = new LoggerAdapter(new ThirdPartyLogger());
logger.log('Server started'); // Uses your interface, calls their implementation
```

**Decorator — Add behavior to objects without changing class**
```javascript
// Already seen in our Express middleware!
// But here's the explicit pattern:

function withRetry(fn, maxRetries = 3, delay = 1000) {
  return async function(...args) {
    let lastError;
    for (let attempt = 1; attempt <= maxRetries; attempt++) {
      try {
        return await fn(...args);
      } catch (error) {
        lastError = error;
        if (attempt < maxRetries) await new Promise(r => setTimeout(r, delay * attempt));
      }
    }
    throw lastError;
  };
}

function withLogging(fn, name) {
  return async function(...args) {
    console.log(`Calling ${name}...`);
    const result = await fn(...args);
    console.log(`${name} completed`);
    return result;
  };
}

// Decorate functions with new behaviors!
const sendEmailWithRetry = withRetry(sendEmail, 3);
const sendEmailWithLogging = withLogging(sendEmailWithRetry, 'sendEmail');
await sendEmailWithLogging('alice@example.com', 'Hello!');
// Logging + retry without changing sendEmail function!
```

**Facade — Simplify a complex system with a simple interface**
```javascript
// Complex system: Authentication requires checking DB, Redis, JWT, rate limiter...
class AuthFacade {
  constructor() {
    this.jwtService = new JWTService();
    this.userRepo = new UserRepository();
    this.redisClient = RedisClient.getInstance();
    this.rateLimiter = new RateLimiter(this.redisClient);
  }
  
  // Simple interface hiding all the complexity!
  async authenticate(token) {
    // Internally handles: rate limit check, JWT verify, user lookup, session check
    await this.rateLimiter.check(token);
    const payload = this.jwtService.verify(token);
    const user = await this.userRepo.findById(payload.userId);
    if (!user) throw new AuthError('User not found');
    const isValid = await this.redisClient.get(`session:${payload.userId}`);
    if (!isValid) throw new AuthError('Session expired');
    return user;
  }
  
  async login(email, password) { /* ... */ }
  async logout(userId) { /* ... */ }
}

// Client code is simple!
const authFacade = new AuthFacade();
const user = await authFacade.authenticate(token); // All complexity hidden!
```

---

### Behavioral: How objects communicate

**Observer — When one object changes, others are notified automatically**
```javascript
// Event system — the foundation of Node.js!
class EventEmitter {
  #listeners = {};
  
  on(event, callback) {
    if (!this.#listeners[event]) this.#listeners[event] = [];
    this.#listeners[event].push(callback);
    return () => this.off(event, callback); // Returns unsubscribe function
  }
  
  off(event, callback) {
    this.#listeners[event] = (this.#listeners[event] || []).filter(cb => cb !== callback);
  }
  
  emit(event, ...args) {
    (this.#listeners[event] || []).forEach(callback => callback(...args));
  }
}

class OrderService extends EventEmitter {
  async placeOrder(orderData) {
    const order = await db.createOrder(orderData);
    this.emit('order.placed', order); // Notify all subscribers!
    return order;
  }
}

// Subscribers register independently — no coupling!
orderService.on('order.placed', async (order) => {
  await emailService.sendConfirmation(order.userId);
});

orderService.on('order.placed', async (order) => {
  await inventoryService.reserve(order.items);
});

orderService.on('order.placed', async (order) => {
  await analyticsService.track('purchase', order);
});
```

**Strategy — Switch algorithms at runtime**
```javascript
// Different sorting strategies for feed
class FeedStrategy {
  sort(posts) { throw new Error('Implement sort'); }
}

class ChronologicalStrategy extends FeedStrategy {
  sort(posts) { return [...posts].sort((a, b) => b.createdAt - a.createdAt); }
}

class PopularityStrategy extends FeedStrategy {
  sort(posts) { return [...posts].sort((a, b) => b.likesCount - a.likesCount); }
}

class PersonalizedStrategy extends FeedStrategy {
  constructor(userPreferences) { super(); this.prefs = userPreferences; }
  sort(posts) {
    return [...posts].sort((a, b) => {
      const scoreA = a.likesCount + (this.prefs.includes(a.category) ? 100 : 0);
      const scoreB = b.likesCount + (this.prefs.includes(b.category) ? 100 : 0);
      return scoreB - scoreA;
    });
  }
}

class Feed {
  constructor(strategy) { this.strategy = strategy; }
  setStrategy(strategy) { this.strategy = strategy; }
  getItems(posts) { return this.strategy.sort(posts); }
}

// Switch strategy at runtime!
const feed = new Feed(new ChronologicalStrategy());
feed.setStrategy(new PopularityStrategy()); // User changed sorting preference
feed.getItems(posts);
```

---

## ⚖️ Trade-offs

| Pattern | When to Use | Caution |
|---------|------------|---------|
| Singleton | Shared resource (DB, Redis) | Hard to test, global state |
| Factory | Create objects polymorphically | Can over-complicate simple creation |
| Observer | Event handling, loose coupling | Too many listeners = hard to trace |
| Strategy | Interchangeable algorithms | Overkill for simple conditionals |
| Decorator | Add behavior without subclassing | Chain too long = confusing |

---

## 💼 Interview Questions (WITH SOLUTIONS)

### Q1: What are the three categories of design patterns?

**Solution:**
1. **Creational:** Deal with object creation — how objects are instantiated. Examples: Singleton, Factory, Builder. Solve: "How do I create this object flexibly?"
2. **Structural:** Deal with object composition — how objects fit together. Examples: Adapter, Decorator, Facade. Solve: "How do I make these incompatible things work together?"
3. **Behavioral:** Deal with object communication — how objects interact. Examples: Observer, Strategy, Command. Solve: "How do objects talk to each other?"

### Q2: Give an example of the Observer pattern in Node.js

**Solution:**
Node.js EventEmitter IS the Observer pattern!

```javascript
const EventEmitter = require('events');
const orderEmitter = new EventEmitter();

// Subscribers (observers)
orderEmitter.on('orderPlaced', (order) => emailService.send(order));
orderEmitter.on('orderPlaced', (order) => analytics.track(order));
orderEmitter.on('orderPlaced', (order) => inventory.reserve(order));

// Publisher (subject) — doesn't know about subscribers!
function placeOrder(data) {
  const order = db.create(data);
  orderEmitter.emit('orderPlaced', order); // All subscribers notified!
  return order;
}
```

Socket.IO is also Observer: `socket.on('message', handler)` = subscribe, `io.emit('message', data)` = notify.

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem: Which patterns do you use in a React + Node.js app?

**Solution:**
```
Frontend (React):
- Observer: React Context + useReducer (state changes notify components)
- Strategy: Different render strategies (list view vs grid view)
- Decorator: HOCs (Higher Order Components) add behavior to components
- Facade: Custom hooks (useAuth, useCart) hide complex state logic

Backend (Node.js):
- Singleton: DB pool, Redis client
- Factory: Creating different payment processors
- Builder: Query builders, email template builders
- Observer: EventEmitter for async events
- Strategy: Different caching strategies, different sorting algorithms
- Adapter: Wrapping third-party APIs to your interface
- Facade: Service layer hiding repository complexity
- Middleware chain: Chain of Responsibility pattern (Express middleware)
```

---

### Navigation
**Prev:** [02_SOLID_Principles.md](02_SOLID_Principles.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [04_Creational_Patterns.md](04_Creational_Patterns.md)
