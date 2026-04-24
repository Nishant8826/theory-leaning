# 📌 Behavioral Patterns

## 🧠 Concept Explanation (Story Format)

Your app needs to notify users when their order ships. But you don't know upfront which users care about which notifications, or via which channel. You also need to switch between different pricing strategies based on user type.

Behavioral patterns handle HOW objects communicate and HOW responsibilities are distributed among them. They're the glue that makes your system responsive, flexible, and extensible.

---

## 🔍 Key Behavioral Patterns

### 1. Observer Pattern

**Intent:** Define a one-to-many dependency so that when one object changes state, all dependents are notified automatically.

**Real-world use:** Node.js EventEmitter, Socket.IO events, React state updates, Redux store.

```javascript
// Custom EventEmitter (Observer pattern implementation)
class EventBus {
  #listeners = new Map();
  #onceListeners = new Map();
  
  on(event, callback) {
    if (!this.#listeners.has(event)) this.#listeners.set(event, []);
    this.#listeners.get(event).push(callback);
    
    // Return unsubscribe function!
    return () => {
      const list = this.#listeners.get(event);
      const idx = list.indexOf(callback);
      if (idx !== -1) list.splice(idx, 1);
    };
  }
  
  once(event, callback) {
    const wrapper = (...args) => {
      callback(...args);
      this.off(event, wrapper);
    };
    return this.on(event, wrapper);
  }
  
  off(event, callback) {
    const list = this.#listeners.get(event) || [];
    this.#listeners.set(event, list.filter(cb => cb !== callback));
  }
  
  emit(event, ...args) {
    (this.#listeners.get(event) || []).forEach(cb => {
      try { cb(...args); }
      catch (e) { console.error(`Error in listener for ${event}:`, e); }
    });
  }
}

// Application usage
const orderBus = new EventBus();

// Subscribers don't know about each other!
const unsubEmail = orderBus.on('order.placed', async (order) => {
  await emailService.sendConfirmation(order.userId, order.id);
});

const unsubInventory = orderBus.on('order.placed', async (order) => {
  await inventoryService.reserveItems(order.items);
});

const unsubAnalytics = orderBus.on('order.placed', async (order) => {
  await analytics.trackPurchase({ orderId: order.id, amount: order.total });
});

// Publisher — doesn't know who's listening!
async function placeOrder(data) {
  const order = await db.createOrder(data);
  orderBus.emit('order.placed', order); // Notifies ALL subscribers
  return order;
}

// React-style Observer with store
class Store {
  #state;
  #subscribers = [];
  
  constructor(initialState) { this.#state = initialState; }
  
  getState() { return this.#state; }
  
  setState(updater) {
    this.#state = typeof updater === 'function' ? updater(this.#state) : { ...this.#state, ...updater };
    this.#subscribers.forEach(fn => fn(this.#state));
  }
  
  subscribe(fn) {
    this.#subscribers.push(fn);
    return () => { this.#subscribers = this.#subscribers.filter(s => s !== fn); };
  }
}

const cartStore = new Store({ items: [], total: 0 });

// Components subscribe to state changes
cartStore.subscribe((state) => {
  document.getElementById('cart-count').textContent = state.items.length;
});

cartStore.setState(state => ({
  items: [...state.items, newItem],
  total: state.total + newItem.price
}));
// All subscribers notified automatically!
```

---

### 2. Strategy Pattern

**Intent:** Define a family of algorithms, put each in a class, and make them interchangeable.

```javascript
// Sorting strategies for product catalog
class SortStrategy {
  sort(items) { throw new Error('Implement sort'); }
}

class PriceAscendingStrategy extends SortStrategy {
  sort(items) { return [...items].sort((a, b) => a.price - b.price); }
}

class PriceDescendingStrategy extends SortStrategy {
  sort(items) { return [...items].sort((a, b) => b.price - a.price); }
}

class PopularityStrategy extends SortStrategy {
  sort(items) { return [...items].sort((a, b) => b.salesCount - a.salesCount); }
}

class RelevanceStrategy extends SortStrategy {
  constructor(searchQuery) { super(); this.query = searchQuery.toLowerCase(); }
  sort(items) {
    return [...items].sort((a, b) => {
      const scoreA = a.name.toLowerCase().includes(this.query) ? 2 : a.description.includes(this.query) ? 1 : 0;
      const scoreB = b.name.toLowerCase().includes(this.query) ? 2 : b.description.includes(this.query) ? 1 : 0;
      return scoreB - scoreA;
    });
  }
}

class ProductCatalog {
  #strategy;
  
  constructor(strategy = new PriceAscendingStrategy()) {
    this.#strategy = strategy;
  }
  
  setStrategy(strategy) { this.#strategy = strategy; }
  
  getProducts(items) { return this.#strategy.sort(items); }
}

// In your API
app.get('/products', async (req, res) => {
  const products = await db.getProducts();
  const catalog = new ProductCatalog();
  
  // Switch strategy based on query param
  const strategies = {
    price_asc: new PriceAscendingStrategy(),
    price_desc: new PriceDescendingStrategy(),
    popular: new PopularityStrategy(),
    relevant: new RelevanceStrategy(req.query.q || '')
  };
  
  catalog.setStrategy(strategies[req.query.sort] || new PriceAscendingStrategy());
  
  res.json(catalog.getProducts(products));
});

// Compression strategy
class Compressor {
  compress(data) { throw new Error('Implement compress'); }
  decompress(data) { throw new Error('Implement decompress'); }
}

class GzipCompressor extends Compressor {
  compress(data) { return zlib.gzipSync(data); }
  decompress(data) { return zlib.gunzipSync(data); }
}

class BrotliCompressor extends Compressor {
  compress(data) { return zlib.brotliCompressSync(data); }
  decompress(data) { return zlib.brotliDecompressSync(data); }
}

class StorageService {
  #compressor;
  
  constructor(compressor) { this.#compressor = compressor; }
  
  setCompressor(compressor) { this.#compressor = compressor; }
  
  async save(key, data) {
    const compressed = this.#compressor.compress(Buffer.from(JSON.stringify(data)));
    await s3.putObject({ Key: key, Body: compressed }).promise();
  }
  
  async load(key) {
    const result = await s3.getObject({ Key: key }).promise();
    const decompressed = this.#compressor.decompress(result.Body);
    return JSON.parse(decompressed.toString());
  }
}
```

---

### 3. Command Pattern

**Intent:** Encapsulate a request as an object, allowing parameterization, queuing, and undo operations.

```javascript
// Command interface
class Command {
  async execute() { throw new Error('Implement execute'); }
  async undo() { throw new Error('Implement undo'); }
}

// Concrete commands
class AddToCartCommand extends Command {
  constructor(cart, product, quantity = 1) {
    super();
    this.cart = cart;
    this.product = product;
    this.quantity = quantity;
  }
  
  async execute() {
    this.cart.addItem(this.product, this.quantity);
    return { added: this.product.name, quantity: this.quantity };
  }
  
  async undo() {
    this.cart.removeItem(this.product.id, this.quantity);
    return { removed: this.product.name };
  }
}

class ApplyDiscountCommand extends Command {
  constructor(cart, discountCode) {
    super();
    this.cart = cart;
    this.discountCode = discountCode;
    this.previousDiscount = null;
  }
  
  async execute() {
    this.previousDiscount = this.cart.discount;
    const discount = await discountService.validate(this.discountCode);
    this.cart.applyDiscount(discount);
    return { discount: discount.percentage };
  }
  
  async undo() {
    this.cart.discount = this.previousDiscount;
    return { discount: 'removed' };
  }
}

// Command invoker with history (enables undo/redo!)
class CommandManager {
  #history = [];
  #undoneHistory = [];
  
  async execute(command) {
    const result = await command.execute();
    this.#history.push(command);
    this.#undoneHistory = []; // Clear redo history when new command executed
    return result;
  }
  
  async undo() {
    const command = this.#history.pop();
    if (!command) throw new Error('Nothing to undo');
    const result = await command.undo();
    this.#undoneHistory.push(command);
    return result;
  }
  
  async redo() {
    const command = this.#undoneHistory.pop();
    if (!command) throw new Error('Nothing to redo');
    const result = await command.execute();
    this.#history.push(command);
    return result;
  }
  
  get canUndo() { return this.#history.length > 0; }
  get canRedo() { return this.#undoneHistory.length > 0; }
}

// Usage with undo/redo
const manager = new CommandManager();
await manager.execute(new AddToCartCommand(cart, product1, 2));
await manager.execute(new AddToCartCommand(cart, product2, 1));
await manager.execute(new ApplyDiscountCommand(cart, 'SAVE20'));

await manager.undo(); // Removes discount
await manager.undo(); // Removes product2

// Command queue for async processing
class CommandQueue {
  #queue = [];
  #isProcessing = false;
  
  enqueue(command) {
    this.#queue.push(command);
    if (!this.#isProcessing) this.#process();
  }
  
  async #process() {
    this.#isProcessing = true;
    while (this.#queue.length) {
      const command = this.#queue.shift();
      try { await command.execute(); }
      catch (e) { console.error('Command failed:', e); }
    }
    this.#isProcessing = false;
  }
}
```

---

### 4. Template Method Pattern

**Intent:** Define the skeleton of an algorithm, deferring some steps to subclasses.

```javascript
// Data processing pipeline template
class DataPipeline {
  // Template method — defines the algorithm skeleton
  async process(data) {
    const cleaned = await this.clean(data);          // Subclass implements
    const validated = await this.validate(cleaned);   // Subclass implements
    const transformed = await this.transform(validated); // Subclass implements
    await this.load(transformed);                     // Subclass implements
    await this.notify();                              // Common step — optional override
    return transformed;
  }
  
  async clean(data) { throw new Error('Implement clean'); }
  async validate(data) { throw new Error('Implement validate'); }
  async transform(data) { throw new Error('Implement transform'); }
  async load(data) { throw new Error('Implement load'); }
  
  // Optional hook — subclasses CAN override but don't have to
  async notify() {
    console.log('Pipeline completed');
  }
}

class UserImportPipeline extends DataPipeline {
  async clean(users) {
    return users.map(u => ({
      ...u,
      email: u.email?.toLowerCase().trim(),
      name: u.name?.trim()
    })).filter(u => u.email && u.name);
  }
  
  async validate(users) {
    return users.filter(u => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(u.email));
  }
  
  async transform(users) {
    return Promise.all(users.map(async u => ({
      ...u,
      passwordHash: await bcrypt.hash(generateTempPassword(), 10),
      createdAt: new Date()
    })));
  }
  
  async load(users) {
    await db.query(
      'INSERT INTO users (name, email, password_hash) SELECT * FROM UNNEST($1::text[], $2::text[], $3::text[]) ON CONFLICT DO NOTHING',
      [users.map(u => u.name), users.map(u => u.email), users.map(u => u.passwordHash)]
    );
  }
  
  async notify() {
    await emailService.sendBatchImportReport(this.result);
  }
}

class ProductImportPipeline extends DataPipeline {
  async clean(products) { /* product-specific cleaning */ }
  async validate(products) { /* product-specific validation */ }
  async transform(products) { /* product-specific transformation */ }
  async load(products) { /* bulk insert into products table */ }
}

// Usage
const pipeline = new UserImportPipeline();
await pipeline.process(csvData);
```

---

### 5. State Pattern

**Intent:** Allow an object to change its behavior when its internal state changes.

```javascript
// Order state machine
class OrderState {
  constructor(order) { this.order = order; }
  
  // Define allowed transitions — subclasses override what's allowed
  confirm() { throw new Error(`Cannot confirm order in ${this.constructor.name} state`); }
  cancel() { throw new Error(`Cannot cancel order in ${this.constructor.name} state`); }
  ship() { throw new Error(`Cannot ship order in ${this.constructor.name} state`); }
  deliver() { throw new Error(`Cannot deliver order in ${this.constructor.name} state`); }
  
  toString() { return this.constructor.name; }
}

class PendingState extends OrderState {
  confirm() {
    this.order.setState(new ConfirmedState(this.order));
    return 'Order confirmed';
  }
  cancel() {
    this.order.setState(new CancelledState(this.order));
    return 'Order cancelled';
  }
}

class ConfirmedState extends OrderState {
  ship() {
    this.order.setState(new ShippedState(this.order));
    return 'Order shipped';
  }
  cancel() {
    // Can cancel confirmed but need refund
    this.order.refund();
    this.order.setState(new CancelledState(this.order));
    return 'Order cancelled (refund initiated)';
  }
}

class ShippedState extends OrderState {
  deliver() {
    this.order.setState(new DeliveredState(this.order));
    return 'Order delivered';
  }
  // Cannot cancel once shipped!
}

class DeliveredState extends OrderState {
  // Terminal state — nothing more to do
}

class CancelledState extends OrderState {
  // Terminal state — cannot reactivate
}

class Order {
  #state;
  #history = [];
  
  constructor(id, userId) {
    this.id = id;
    this.userId = userId;
    this.#state = new PendingState(this);
  }
  
  setState(newState) {
    this.#history.push({ from: this.#state.toString(), to: newState.toString(), at: new Date() });
    this.#state = newState;
  }
  
  confirm() { return this.#state.confirm(); }
  cancel() { return this.#state.cancel(); }
  ship() { return this.#state.ship(); }
  deliver() { return this.#state.deliver(); }
  
  get status() { return this.#state.toString(); }
  get history() { return [...this.#history]; }
  
  refund() { /* initiate refund logic */ }
}

// Usage
const order = new Order('123', 'user_456');
console.log(order.status); // PendingState

order.confirm();
console.log(order.status); // ConfirmedState

order.ship();
console.log(order.status); // ShippedState

try {
  order.cancel(); // ❌ Throws — can't cancel shipped order
} catch (e) {
  console.error(e.message);
}

order.deliver();
console.log(order.status); // DeliveredState
```

---

## ⚖️ Trade-offs

| Pattern | Purpose | Best For |
|---------|---------|---------|
| Observer | Event notification | Loose coupling, fan-out |
| Strategy | Interchangeable algorithms | Sorting, pricing, auth |
| Command | Encapsulate requests | Undo/redo, queuing, logging |
| Template Method | Algorithm skeleton | ETL pipelines, import/export |
| State | State-dependent behavior | Order status, auth flow |

---

## 💼 Interview Questions (WITH SOLUTIONS)

### Q1: How is Observer different from Pub/Sub?

**Solution:**
- **Observer:** Subscribers (observers) know about the subject. Direct reference. Usually synchronous. Same process.
- **Pub/Sub:** Publishers and subscribers don't know each other. Mediated by a message broker (Redis, SQS, RabbitMQ). Asynchronous. Can be across services/processes.

Observer = EventEmitter in same Node.js process.
Pub/Sub = SNS topic with SQS subscriptions across microservices.

### Q2: When would you use the Command pattern?

**Solution:**
Use Command when you need:
1. **Undo/Redo:** Each command knows how to undo itself
2. **Queuing/Scheduling:** Commands can be queued for later execution
3. **Logging:** Record which commands were executed and when
4. **Transactions:** Execute a series of commands atomically (rollback on failure)

Real examples: Text editor undo/redo, shopping cart operations, database migrations (up/down commands), form wizards.

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem: Implement a user notification system using Observer pattern

```javascript
class NotificationSystem extends EventBus {
  async notifyUserCreated(user) {
    this.emit('user.created', user);
  }
  
  async notifyOrderPlaced(order) {
    this.emit('order.placed', order);
  }
}

const notifications = new NotificationSystem();

// Each subscriber handles their own responsibility
notifications.on('user.created', async (user) => {
  await sendWelcomeEmail(user.email, user.name);
});

notifications.on('user.created', async (user) => {
  await slackNotify(`🎉 New user: ${user.name} (${user.email})`);
});

notifications.on('order.placed', async (order) => {
  await sendOrderConfirmation(order.userId, order.id);
});

notifications.on('order.placed', async (order) => {
  await reserveInventory(order.items);
});

// Usage in routes
app.post('/users', async (req, res) => {
  const user = await userService.create(req.body);
  await notifications.notifyUserCreated(user);
  res.status(201).json(user);
});
```

---

### Navigation
**Prev:** [05_Structural_Patterns.md](05_Structural_Patterns.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [07_Database_Design.md](07_Database_Design.md)
