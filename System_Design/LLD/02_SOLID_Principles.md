# 📌 SOLID Principles

## 🧠 Concept Explanation (Story Format)

You joined a startup. The codebase is a mess. Adding a new feature breaks 10 other things. A simple change requires modifying 15 files. Every developer is afraid to touch the code.

SOLID principles are 5 rules that, if followed, make your code easy to change, extend, and understand. They were coined by Robert C. Martin (Uncle Bob).

These principles apply directly to how you structure your Node.js services and JavaScript classes.

---

## 🔍 The 5 SOLID Principles

### S — Single Responsibility Principle (SRP)

**"A class should have only ONE reason to change."**

If a class handles authentication AND sends emails AND formats reports → changing email logic could break authentication!

```javascript
// ❌ VIOLATES SRP — UserService does TOO MUCH
class UserService {
  async register(userData) {
    // Creates user
    const user = await db.query('INSERT INTO users ...', [...]);
    
    // Sends email (different responsibility!)
    const emailHtml = `<h1>Welcome ${userData.name}!</h1>`;
    await nodemailer.sendMail({ to: userData.email, html: emailHtml });
    
    // Formats response (yet another responsibility!)
    return { id: user.id, name: user.name, createdAt: user.createdAt.toISOString() };
  }
  
  // Also does password management?
  async resetPassword(email) { /* ... */ }
  
  // Also does analytics?
  async trackUserSignup(userId) { /* ... */ }
}

// ✅ SRP — Each class has ONE responsibility
class UserRepository {
  async create(userData) {
    const result = await db.query('INSERT INTO users (name, email, password_hash) VALUES ($1, $2, $3) RETURNING *', 
                                  [userData.name, userData.email, userData.passwordHash]);
    return result.rows[0];
  }
  async findByEmail(email) { /* ... */ }
}

class EmailService {
  async sendWelcomeEmail(user) {
    await mailer.sendMail({
      to: user.email,
      subject: 'Welcome!',
      html: `<h1>Welcome, ${user.name}!</h1>`
    });
  }
}

class UserPresenter {
  format(user) {
    return { id: user.id, name: user.name, createdAt: user.createdAt.toISOString() };
  }
}

class UserService {
  constructor(userRepo, emailService, userPresenter) {
    this.userRepo = userRepo;
    this.emailService = emailService;
    this.userPresenter = userPresenter;
  }
  
  async register(userData) {
    const user = await this.userRepo.create(userData);
    await this.emailService.sendWelcomeEmail(user); // Each dependency has one job
    return this.userPresenter.format(user);
  }
}
```

---

### O — Open/Closed Principle (OCP)

**"Open for extension, closed for modification."**

Adding new behavior should NOT require changing existing code.

```javascript
// ❌ VIOLATES OCP — must modify existing code to add new payment method
class PaymentService {
  processPayment(type, amount, details) {
    if (type === 'stripe') {
      // Stripe logic
      return stripe.charges.create({ amount });
    } else if (type === 'paypal') {
      // PayPal logic
      return paypal.orders.create({ amount });
    } else if (type === 'crypto') {
      // ADDING CRYPTO: Must modify this function!
      return coinbase.createCharge({ amount });
    }
    throw new Error('Unknown payment type');
  }
}

// ✅ OCP — Adding new payment type: just add a new class, don't change existing code!
class PaymentProcessor {
  async process(amount, details) {
    throw new Error('Must implement process()');
  }
}

class StripeProcessor extends PaymentProcessor {
  async process(amount, details) {
    return stripe.charges.create({ amount: amount * 100, source: details.token });
  }
}

class PayPalProcessor extends PaymentProcessor {
  async process(amount, details) {
    return paypal.orders.create({ purchase_units: [{ amount: { value: amount.toString() } }] });
  }
}

// New payment: Just add new class! PaymentService doesn't change.
class CryptoProcessor extends PaymentProcessor {
  async process(amount, details) {
    return coinbase.createCharge({ local_price: { amount, currency: 'USD' } });
  }
}

class PaymentService {
  #processors = new Map();
  
  register(type, processor) {
    this.#processors.set(type, processor);
  }
  
  async processPayment(type, amount, details) {
    const processor = this.#processors.get(type);
    if (!processor) throw new Error(`Unknown payment type: ${type}`);
    return processor.process(amount, details);
  }
}

// Setup (open for extension, closed for modification)
const paymentService = new PaymentService();
paymentService.register('stripe', new StripeProcessor());
paymentService.register('paypal', new PayPalProcessor());
paymentService.register('crypto', new CryptoProcessor()); // Just register, no code change!
```

---

### L — Liskov Substitution Principle (LSP)

**"Subclasses must be substitutable for their parent class."**

If you use the parent class somewhere, replacing it with a subclass should NOT break anything.

```javascript
// ❌ VIOLATES LSP
class Rectangle {
  constructor(width, height) { this.width = width; this.height = height; }
  setWidth(width) { this.width = width; }
  setHeight(height) { this.height = height; }
  get area() { return this.width * this.height; }
}

class Square extends Rectangle {
  setWidth(width) {
    this.width = width;
    this.height = width; // Square must have equal sides!
  }
  setHeight(height) {
    this.width = height; // This BREAKS LSP!
    this.height = height;
  }
}

function testArea(rect) {
  rect.setWidth(5);
  rect.setHeight(10);
  console.log(rect.area); // Expected: 50
  // Square returns 100 (10*10)! LSP violated!
}

testArea(new Rectangle(0, 0)); // 50 ✅
testArea(new Square(0));        // 100 ❌ (unexpected!)

// ✅ Fix: Don't force incorrect inheritance
class Shape {
  get area() { throw new Error('Implement area'); }
}

class Rectangle extends Shape {
  constructor(width, height) { super(); this.width = width; this.height = height; }
  get area() { return this.width * this.height; }
}

class Square extends Shape {
  constructor(side) { super(); this.side = side; }
  get area() { return this.side ** 2; }
}
// Now they're completely independent — no LSP violation!
```

---

### I — Interface Segregation Principle (ISP)

**"Clients should not depend on interfaces they don't use."**

Don't force a class to implement methods it doesn't need.

```javascript
// ❌ VIOLATES ISP — Fat interface forces irrelevant methods
class DataProcessor {
  // ALL classes that extend this must implement ALL methods!
  readData() { throw new Error('Implement readData'); }
  writeData(data) { throw new Error('Implement writeData'); }
  deleteData(id) { throw new Error('Implement deleteData'); }
  exportToCSV() { throw new Error('Implement exportToCSV'); }
  generateReport() { throw new Error('Implement generateReport'); }
}

class ReadOnlyCache extends DataProcessor {
  readData() { return cache.get(key); }
  writeData() { throw new Error('ReadOnlyCache cannot write!'); } // FORCED to implement!
  deleteData() { throw new Error('ReadOnlyCache cannot delete!'); }
  exportToCSV() { throw new Error('Not applicable!'); }
  generateReport() { throw new Error('Not applicable!'); }
}

// ✅ ISP — Separate small interfaces (mixins/composition)
const Readable = (Base) => class extends Base {
  readData() { throw new Error('Implement readData'); }
};

const Writable = (Base) => class extends Base {
  writeData(data) { throw new Error('Implement writeData'); }
};

const Deletable = (Base) => class extends Base {
  deleteData(id) { throw new Error('Implement deleteData'); }
};

const Exportable = (Base) => class extends Base {
  exportToCSV() { throw new Error('Implement exportToCSV'); }
};

// ReadOnlyCache only gets what it needs
class ReadOnlyCache extends Readable(class {}) {
  readData() { return cache.get(key); }
}

// FullDataStore gets everything it needs
class FullDataStore extends Exportable(Deletable(Writable(Readable(class {})))) {
  readData() { return db.read(); }
  writeData(data) { return db.write(data); }
  deleteData(id) { return db.delete(id); }
  exportToCSV() { return converter.toCSV(db.readAll()); }
}
```

---

### D — Dependency Inversion Principle (DIP)

**"Depend on abstractions, not concretions."**

High-level modules should not depend on low-level modules. Both should depend on abstractions.

```javascript
// ❌ VIOLATES DIP — UserService is tightly coupled to MySQL
class UserService {
  constructor() {
    // Hard-coded dependency! Can't swap without changing UserService
    this.db = new MySQLDatabase({ host: 'localhost', db: 'myapp' });
  }
  
  async getUser(id) {
    return this.db.query(`SELECT * FROM users WHERE id = ${id}`);
  }
}

// Can't test without a real MySQL database!
// Can't switch to PostgreSQL without rewriting UserService!

// ✅ DIP — Depend on abstraction (interface), inject the implementation
class UserRepository { // Abstract interface
  async findById(id) { throw new Error('Implement findById'); }
  async save(user) { throw new Error('Implement save'); }
}

class PostgresUserRepository extends UserRepository {
  async findById(id) {
    const result = await pool.query('SELECT * FROM users WHERE id = $1', [id]);
    return result.rows[0];
  }
  async save(user) {
    await pool.query('INSERT INTO users ...', [...]);
  }
}

class MongoUserRepository extends UserRepository {
  async findById(id) {
    return db.collection('users').findOne({ _id: id });
  }
  async save(user) {
    await db.collection('users').insertOne(user);
  }
}

// In-memory repository for testing!
class InMemoryUserRepository extends UserRepository {
  #users = new Map();
  async findById(id) { return this.#users.get(id); }
  async save(user) { this.#users.set(user.id, user); return user; }
}

class UserService {
  constructor(userRepository) { // INJECT the dependency!
    this.userRepository = userRepository; // Depends on abstraction, not concretion
  }
  
  async getUser(id) {
    return this.userRepository.findById(id); // Works with ANY repository!
  }
}

// Production: Use PostgreSQL
const userService = new UserService(new PostgresUserRepository());

// Testing: Use in-memory (no DB needed!)
const testUserService = new UserService(new InMemoryUserRepository());
```

---

## 🔍 Design Patterns Used
- **Strategy Pattern:** OCP example (different payment processors)
- **Dependency Injection:** DIP example (inject repositories)
- **Decorator/Mixin Pattern:** ISP example (composable capabilities)

---

## ⚖️ Trade-offs

| With SOLID | Without SOLID |
|-----------|---------------|
| Easy to test | Hard to test (dependencies hardcoded) |
| Easy to extend | Modification ripples everywhere |
| More files/classes | Fewer files, but complex |
| Learning curve | Quick to write initially |

---

## 💼 Interview Questions (WITH SOLUTIONS)

### Q1: Explain the Single Responsibility Principle with a real example.

**Solution:**
SRP says a class should have only one reason to change.

Bad: `UserController` handles HTTP parsing, validation, database operations, email sending, and response formatting. If email provider changes → you modify the HTTP controller — wrong!

Good: Separate into `UserController` (HTTP), `UserService` (business logic), `UserRepository` (DB), `EmailService` (email). Each changes independently.

In Node.js: Keep your Express route handlers thin. Put business logic in service files. Put DB queries in repository files.

### Q2: How does Dependency Injection relate to the Dependency Inversion Principle?

**Solution:**
DIP says: depend on abstractions.
Dependency Injection is the MECHANISM to achieve DIP.

Instead of `class Service { constructor() { this.db = new MySQL(); } }` — you "inject" the dependency:
`class Service { constructor(dbRepository) { this.db = dbRepository; } }`

This makes code testable (inject mock), swappable (inject PostgreSQL vs MongoDB), and follows DIP.

In Node.js: Pass dependencies as constructor arguments. Use a DI container (like `awilix`) for large apps.

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem: Refactor a notification service to follow SOLID

**Solution:**
```javascript
// After SOLID refactoring:

// SRP: Each channel has one job
class EmailNotifier {
  async send(user, message) { await emailClient.send({ to: user.email, body: message }); }
}

class SMSNotifier {
  async send(user, message) { await smsClient.send({ to: user.phone, body: message }); }
}

class PushNotifier {
  async send(user, message) { await fcm.send({ token: user.fcmToken, notification: { body: message } }); }
}

// OCP: Add new notifier without changing NotificationService
class NotificationService {
  #notifiers = [];
  
  addNotifier(notifier) { this.#notifiers.push(notifier); return this; }
  
  async notify(user, message) {
    await Promise.allSettled(this.#notifiers.map(n => n.send(user, message)));
  }
}

// DIP: Depend on abstraction
const notificationService = new NotificationService()
  .addNotifier(new EmailNotifier())    // DI: inject concrete implementations
  .addNotifier(new SMSNotifier())
  .addNotifier(new PushNotifier());

await notificationService.notify(user, 'Your order has shipped!');
// Adding WhatsApp: create WhatsAppNotifier, addNotifier() — zero change to existing code!
```

---

### Navigation
**Prev:** [01_Object_Oriented_Design.md](01_Object_Oriented_Design.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [03_Design_Patterns_Overview.md](03_Design_Patterns_Overview.md)
