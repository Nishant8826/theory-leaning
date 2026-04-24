# 📌 Structural Patterns

## 🧠 Concept Explanation (Story Format)

You have a socket (your old app) and a plug (new third-party library) that don't fit each other. Instead of rewiring the house, you use an **adapter**. You want to add new features to your car without rebuilding the whole car — you add **accessories** (decorators). Complex systems hidden behind simple control panels — that's a **facade**.

Structural patterns deal with how classes and objects are composed to form larger structures. They help you build flexible, scalable code by changing the structure without changing individual classes.

---

## 🔍 Key Structural Patterns

### 1. Adapter Pattern

**Intent:** Convert one interface into another that clients expect. Makes incompatible interfaces work together.

```javascript
// Old payment interface your app uses
class OldPaymentInterface {
  makePayment(amount, cardNumber, expiry, cvv) { /* ... */ }
}

// New Stripe API has a completely different interface
class StripeAPI {
  createPaymentIntent(params) { /* { amount, currency, payment_method: { type, card: { number, exp_month, exp_year, cvc } } } */ }
}

// ❌ Without Adapter: Must change all your code to match Stripe
// ✅ With Adapter: Create adapter that translates your interface to Stripe's
class StripeAdapter {
  #stripeAPI;
  
  constructor(stripeAPI) {
    this.#stripeAPI = stripeAPI;
  }
  
  // OLD interface → Translates to Stripe interface internally
  async makePayment(amount, cardNumber, expiry, cvv) {
    const [expMonth, expYear] = expiry.split('/');
    
    // Translate to Stripe's format
    return this.#stripeAPI.createPaymentIntent({
      amount: Math.round(amount * 100), // Stripe uses cents
      currency: 'usd',
      payment_method: {
        type: 'card',
        card: {
          number: cardNumber,
          exp_month: parseInt(expMonth),
          exp_year: parseInt(`20${expYear}`),
          cvc: cvv
        }
      }
    });
  }
}

// Your code doesn't change — uses same interface
const payment = new StripeAdapter(new StripeAPI());
await payment.makePayment(99.99, '4242424242424242', '12/25', '123');

// Real-world use case: Adapting 3rd party loggers
class WinstonAdapter {
  #winston;
  
  constructor(winstonInstance) {
    this.#winston = winstonInstance;
  }
  
  // Your app uses: logger.log(level, message, context)
  log(level, message, context = {}) {
    // Winston uses: logger.log({ level, message, ...context })
    this.#winston.log({ level, message, ...context });
  }
  
  info(message, context) { this.log('info', message, context); }
  error(message, context) { this.log('error', message, context); }
}
```

---

### 2. Decorator Pattern

**Intent:** Attach additional responsibilities to an object dynamically. Decorators provide a flexible alternative to subclassing.

```javascript
// Base function
async function fetchUser(userId) {
  return db.query('SELECT * FROM users WHERE id = $1', [userId]);
}

// Decorators add behavior without modifying fetchUser!

// Caching decorator
function withCache(fn, options = {}) {
  const { ttl = 300, keyFn = (args) => JSON.stringify(args) } = options;
  
  return async function(...args) {
    const cacheKey = `cache:${fn.name}:${keyFn(args)}`;
    
    const cached = await redis.get(cacheKey);
    if (cached) {
      return { ...JSON.parse(cached), _fromCache: true };
    }
    
    const result = await fn.call(this, ...args);
    await redis.setex(cacheKey, ttl, JSON.stringify(result));
    
    return result;
  };
}

// Logging decorator
function withLogging(fn) {
  return async function(...args) {
    const start = Date.now();
    try {
      const result = await fn.call(this, ...args);
      console.log(`${fn.name} completed in ${Date.now() - start}ms`);
      return result;
    } catch (error) {
      console.error(`${fn.name} failed:`, error.message);
      throw error;
    }
  };
}

// Retry decorator
function withRetry(fn, { maxRetries = 3, delay = 1000 } = {}) {
  return async function(...args) {
    for (let attempt = 1; attempt <= maxRetries; attempt++) {
      try {
        return await fn.call(this, ...args);
      } catch (error) {
        if (attempt === maxRetries) throw error;
        await new Promise(r => setTimeout(r, delay * attempt));
      }
    }
  };
}

// Timeout decorator
function withTimeout(fn, timeoutMs = 5000) {
  return async function(...args) {
    return Promise.race([
      fn.call(this, ...args),
      new Promise((_, reject) => setTimeout(() => reject(new Error('Timeout')), timeoutMs))
    ]);
  };
}

// Stack decorators like middleware!
const getUser = withLogging(withCache(withRetry(withTimeout(fetchUser, 3000)), { ttl: 600 }));

const user = await getUser(123);
// → Logs, checks cache, retries on failure, times out after 3s

// Class-based decorator pattern
class APIService {
  async getData(endpoint) { return fetch(endpoint).then(r => r.json()); }
}

class CachedAPIService extends APIService {
  constructor(base, cache, ttl) {
    super();
    this.base = base;
    this.cache = cache;
    this.ttl = ttl;
  }
  
  async getData(endpoint) {
    const cacheKey = `api:${endpoint}`;
    const cached = await this.cache.get(cacheKey);
    if (cached) return JSON.parse(cached);
    
    const data = await this.base.getData(endpoint);
    await this.cache.setex(cacheKey, this.ttl, JSON.stringify(data));
    return data;
  }
}

class LoggedAPIService extends APIService {
  constructor(base) { super(); this.base = base; }
  
  async getData(endpoint) {
    console.log(`Fetching: ${endpoint}`);
    const data = await this.base.getData(endpoint);
    console.log(`Fetched ${endpoint}: ${JSON.stringify(data).length} bytes`);
    return data;
  }
}

// Layer decorators
const api = new LoggedAPIService(
  new CachedAPIService(
    new APIService(),
    redis, 300
  )
);
```

---

### 3. Facade Pattern

**Intent:** Provide a simple interface to a complex system. Hide complexity behind a unified API.

```javascript
// Complex order processing subsystem
class OrderFacade {
  constructor() {
    this.inventoryService = new InventoryService();
    this.pricingService = new PricingService();
    this.paymentService = new PaymentService();
    this.shippingService = new ShippingService();
    this.notificationService = new NotificationService();
    this.orderRepository = new OrderRepository();
  }
  
  // Simple interface hiding all the complexity!
  async placeOrder(userId, items, paymentDetails, shippingAddress) {
    // Check inventory (complex internally)
    await this.inventoryService.checkAvailability(items);
    
    // Calculate price with all discounts, taxes, shipping
    const { subtotal, tax, shippingCost, total } = 
      await this.pricingService.calculateTotal(items, userId, shippingAddress);
    
    // Create order record
    const order = await this.orderRepository.create({
      userId, items, subtotal, tax, shippingCost, total,
      shippingAddress, status: 'pending'
    });
    
    // Process payment
    const payment = await this.paymentService.charge(total, paymentDetails, order.id);
    
    // Reserve inventory
    await this.inventoryService.reserve(items, order.id);
    
    // Calculate and set shipping
    const shipping = await this.shippingService.createShipment(order.id, shippingAddress, items);
    
    // Update order status
    await this.orderRepository.update(order.id, {
      status: 'confirmed',
      paymentId: payment.id,
      shippingId: shipping.id,
      estimatedDelivery: shipping.estimatedDelivery
    });
    
    // Send notifications
    await this.notificationService.sendOrderConfirmation(userId, order);
    
    return { order, shipping, payment };
  }
  
  async cancelOrder(orderId, userId) {
    const order = await this.orderRepository.findById(orderId);
    if (order.userId !== userId) throw new Error('Unauthorized');
    
    await this.paymentService.refund(order.paymentId, order.total);
    await this.inventoryService.release(order.items, orderId);
    await this.shippingService.cancelShipment(order.shippingId);
    await this.orderRepository.update(orderId, { status: 'cancelled' });
    await this.notificationService.sendCancellationNotification(userId, order);
    
    return { status: 'cancelled' };
  }
}

// Client code is beautifully simple!
const orderFacade = new OrderFacade();
app.post('/orders', authenticate, async (req, res) => {
  const result = await orderFacade.placeOrder(
    req.user.id, req.body.items, req.body.payment, req.body.address
  );
  res.status(201).json(result);
});
```

---

### 4. Proxy Pattern

**Intent:** Provide a surrogate or placeholder for another object to control access to it.

```javascript
// Lazy loading proxy — only fetch data when needed
class UserProxy {
  #userId;
  #user = null;
  #db;
  
  constructor(userId, db) {
    this.#userId = userId;
    this.#db = db;
  }
  
  async getUser() {
    if (!this.#user) {
      this.#user = await this.#db.query('SELECT * FROM users WHERE id = $1', [this.#userId]);
    }
    return this.#user;
  }
  
  async getName() { return (await this.getUser()).name; }
  async getEmail() { return (await this.getUser()).email; }
}

// Protection proxy — control access based on permissions
class SecureDataProxy {
  #realData;
  #user;
  
  constructor(realData, user) {
    this.#realData = realData;
    this.#user = user;
  }
  
  async read(key) {
    if (!this.#user.permissions.includes('read')) throw new Error('Access denied: no read permission');
    return this.#realData.read(key);
  }
  
  async write(key, value) {
    if (!this.#user.permissions.includes('write')) throw new Error('Access denied: no write permission');
    return this.#realData.write(key, value);
  }
  
  async delete(key) {
    if (!this.#user.role !== 'admin') throw new Error('Access denied: admin only');
    return this.#realData.delete(key);
  }
}

// JavaScript Proxy object (built-in!)
function createValidatedObject(target, schema) {
  return new Proxy(target, {
    set(obj, prop, value) {
      if (schema[prop]) {
        const { type, min, max } = schema[prop];
        if (typeof value !== type) throw new TypeError(`${prop} must be of type ${type}`);
        if (min !== undefined && value < min) throw new RangeError(`${prop} must be >= ${min}`);
        if (max !== undefined && value > max) throw new RangeError(`${prop} must be <= ${max}`);
      }
      obj[prop] = value;
      return true;
    }
  });
}

const product = createValidatedObject({}, {
  price: { type: 'number', min: 0, max: 1000000 },
  stock: { type: 'number', min: 0 },
  name: { type: 'string' }
});

product.name = 'Widget';        // ✅
product.price = -10;            // ❌ Throws: price must be >= 0
product.stock = 100;            // ✅
```

---

### 5. Composite Pattern

**Intent:** Treat individual objects and compositions of objects uniformly.

```javascript
// UI component tree (like React DOM!)
class UIComponent {
  constructor(name) { this.name = name; this.children = []; }
  add(component) { this.children.push(component); return this; }
  render(depth = 0) { throw new Error('Implement render'); }
}

class Button extends UIComponent {
  constructor(label, onClick) {
    super(`button:${label}`);
    this.label = label;
    this.onClick = onClick;
  }
  render(depth = 0) { return `${' '.repeat(depth * 2)}<button>${this.label}</button>`; }
}

class Container extends UIComponent {
  constructor(id, className) { super(`container:${id}`); this.id = id; this.className = className; }
  render(depth = 0) {
    const prefix = ' '.repeat(depth * 2);
    const childrenHtml = this.children.map(c => c.render(depth + 1)).join('\n');
    return `${prefix}<div id="${this.id}" class="${this.className}">\n${childrenHtml}\n${prefix}</div>`;
  }
}

// Build tree of components — uniform treatment!
const modal = new Container('modal', 'modal-container')
  .add(new Container('modal-header', 'header')
    .add(new Button('Close', 'closeModal'))
  )
  .add(new Container('modal-body', 'body'))
  .add(new Container('modal-footer', 'footer')
    .add(new Button('Cancel', 'cancel'))
    .add(new Button('Confirm', 'confirm'))
  );

console.log(modal.render());
// Works for both leaf nodes (Button) and composite (Container) uniformly!
```

---

## ⚖️ Trade-offs

| Pattern | Purpose | Caution |
|---------|---------|---------|
| Adapter | Compatibility | Can hide bad design decisions |
| Decorator | Add behavior | Long decorator chains are confusing |
| Facade | Simplify | Can become a "God class" |
| Proxy | Control access | Extra indirection = slight overhead |
| Composite | Tree structures | Complex traversal |

---

## 💼 Interview Questions (WITH SOLUTIONS)

### Q1: What is the difference between Adapter and Facade?

**Solution:**
- **Adapter:** Makes TWO incompatible interfaces work together. Translates interface A to interface B. No simplification — same complexity, just translated.
- **Facade:** Simplifies a COMPLEX SUBSYSTEM into a simple interface. Combines multiple classes/APIs into one simple API.

Example: Adapter is like a UK-to-US power adapter (same power, different plug). Facade is like a TV remote (hides all the TV's complex electronics behind simple buttons).

### Q2: How does the Proxy pattern differ from the Decorator pattern?

**Solution:**
- **Proxy:** Controls ACCESS to an object. Typically same interface as the real object. Purpose: access control, lazy loading, caching.
- **Decorator:** Adds FUNCTIONALITY to an object. Wraps and extends behavior. Purpose: add logging, retry, metrics.

Practical difference: Proxy is transparent (client may not know it's a proxy). Decorator is intentional (client explicitly creates decorated version).

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem: Implement a middleware pipeline using the Decorator pattern

```javascript
// Express-like middleware pipeline
class Pipeline {
  #steps = [];
  
  use(middleware) { this.#steps.push(middleware); return this; }
  
  async execute(context) {
    let index = 0;
    const next = async () => {
      if (index < this.#steps.length) {
        const step = this.#steps[index++];
        await step(context, next);
      }
    };
    await next();
    return context;
  }
}

// Middleware functions (each is a decorator for the request)
const authMiddleware = async (ctx, next) => {
  const token = ctx.headers.authorization;
  ctx.user = await verifyToken(token);
  await next();
};

const logMiddleware = async (ctx, next) => {
  const start = Date.now();
  await next();
  console.log(`${ctx.method} ${ctx.path} - ${Date.now() - start}ms`);
};

const rateLimitMiddleware = async (ctx, next) => {
  const allowed = await checkRateLimit(ctx.user.id);
  if (!allowed) throw new Error('Rate limit exceeded');
  await next();
};

// Build pipeline
const pipeline = new Pipeline()
  .use(logMiddleware)
  .use(authMiddleware)
  .use(rateLimitMiddleware);

// Execute
await pipeline.execute({ headers: req.headers, method: 'GET', path: '/api/data' });
```

---

### Navigation
**Prev:** [04_Creational_Patterns.md](04_Creational_Patterns.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [06_Behavioral_Patterns.md](06_Behavioral_Patterns.md)
