# 📌 Object Oriented Design

## 🧠 Concept Explanation (Story Format)

Imagine you're building an Uber clone. You need to model real-world entities:
- A **Driver** with a name, car, and location
- A **Rider** with a name and payment method
- A **Ride** connecting a driver and rider with a price and status

Without OOP: You'd use raw objects, scattered functions, no clear structure. Adding a new feature means changing code everywhere.

With OOP: You create **classes** that model real-world entities. Each class has data (properties) and behavior (methods). Code is organized, reusable, and easy to extend.

---

## 🏗️ Basic Design (Without OOP)

```javascript
// ❌ Without OOP — scattered, hard to maintain
const users = [];

function createUser(name, email) {
  users.push({ name, email, createdAt: new Date() });
}

function getUserEmail(user) { return user.email; }
function greetUser(user) { return `Hello, ${user.name}!`; }

// Problem: No structure, no encapsulation, functions scattered everywhere
```

---

## ⚡ Optimized Design (With OOP)

```javascript
// ✅ With OOP — clean, organized, extensible
class User {
  #password; // Private field (encapsulation!)
  
  constructor(name, email, password) {
    this.id = crypto.randomUUID();
    this.name = name;
    this.email = email;
    this.#password = password; // Hidden — can't be accessed from outside
    this.createdAt = new Date();
  }
  
  get greeting() { return `Hello, ${this.name}!`; }
  
  async verifyPassword(input) {
    return bcrypt.compare(input, this.#password);
  }
  
  toJSON() {
    return { id: this.id, name: this.name, email: this.email }; // Never expose #password!
  }
}
```

---

## 🔍 Key OOP Concepts

### 1. Encapsulation

```javascript
class BankAccount {
  #balance; // Private — can't be accessed directly from outside
  #transactions = [];
  
  constructor(initialBalance) {
    if (initialBalance < 0) throw new Error('Initial balance cannot be negative');
    this.#balance = initialBalance;
  }
  
  // Controlled access via public methods
  get balance() { return this.#balance; }
  
  deposit(amount) {
    if (amount <= 0) throw new Error('Deposit amount must be positive');
    this.#balance += amount;
    this.#transactions.push({ type: 'deposit', amount, date: new Date() });
  }
  
  withdraw(amount) {
    if (amount <= 0) throw new Error('Amount must be positive');
    if (amount > this.#balance) throw new Error('Insufficient funds');
    this.#balance -= amount;
    this.#transactions.push({ type: 'withdrawal', amount, date: new Date() });
  }
  
  getStatement() { return [...this.#transactions]; } // Return copy, not original!
}

const account = new BankAccount(1000);
account.deposit(500);
account.withdraw(200);
console.log(account.balance); // 1300
// account.#balance = 999999; // ❌ ERROR! Private field — can't be accessed!
```

### 2. Inheritance

```javascript
class Vehicle {
  constructor(make, model, year) {
    this.make = make;
    this.model = model;
    this.year = year;
  }
  
  getInfo() {
    return `${this.year} ${this.make} ${this.model}`;
  }
  
  start() { return 'Vehicle started'; }
}

class Car extends Vehicle {
  constructor(make, model, year, doors) {
    super(make, model, year); // Call parent constructor
    this.doors = doors;
    this.type = 'car';
  }
  
  getInfo() {
    return `${super.getInfo()} (${this.doors} doors)`; // Extend parent method
  }
}

class ElectricCar extends Car {
  constructor(make, model, year, doors, batteryKWh) {
    super(make, model, year, doors);
    this.batteryKWh = batteryKWh;
    this.type = 'electric_car';
  }
  
  start() { return 'Electric motor engaged silently'; }
  
  get range() { return this.batteryKWh * 6; } // ~6 km per kWh
}

const tesla = new ElectricCar('Tesla', 'Model 3', 2024, 4, 75);
console.log(tesla.getInfo()); // "2024 Tesla Model 3 (4 doors)"
console.log(tesla.start());   // "Electric motor engaged silently"
console.log(tesla.range);     // 450
console.log(tesla instanceof Vehicle); // true — ElectricCar IS a Vehicle!
```

### 3. Polymorphism

```javascript
// Same interface, different behaviors
class Animal {
  speak() { throw new Error('Subclass must implement speak()'); }
  move() { return 'Moving...'; }
}

class Dog extends Animal {
  speak() { return 'Woof!'; }
  move() { return 'Running on four legs'; }
}

class Cat extends Animal {
  speak() { return 'Meow!'; }
  move() { return 'Padding silently'; }
}

class Bird extends Animal {
  speak() { return 'Tweet!'; }
  move() { return 'Flying'; }
}

// Polymorphism in action — same code works for all animals!
function makeAnimalSpeak(animal) {
  console.log(animal.speak()); // Different output depending on actual type!
}

const animals = [new Dog(), new Cat(), new Bird()];
animals.forEach(makeAnimalSpeak); // Woof! / Meow! / Tweet!
```

### 4. Abstraction

```javascript
// Abstract class — defines the contract, not the implementation
class PaymentProcessor {
  // Abstract methods — subclasses MUST implement these
  async charge(amount, currency, details) {
    throw new Error('charge() must be implemented by subclass');
  }
  
  async refund(transactionId, amount) {
    throw new Error('refund() must be implemented by subclass');
  }
  
  // Concrete method — shared behavior
  async processPayment(amount, currency, details) {
    console.log(`Processing ${currency} ${amount}...`);
    const result = await this.charge(amount, currency, details); // Calls subclass method
    await this.logTransaction(result);
    return result;
  }
  
  async logTransaction(result) {
    console.log(`Transaction ${result.id} logged`);
  }
}

class StripeProcessor extends PaymentProcessor {
  async charge(amount, currency, details) {
    const charge = await stripe.charges.create({
      amount: amount * 100, // Stripe uses cents
      currency,
      source: details.token
    });
    return { id: charge.id, status: 'success' };
  }
  
  async refund(transactionId, amount) {
    await stripe.refunds.create({ charge: transactionId, amount: amount * 100 });
    return { status: 'refunded' };
  }
}

class PayPalProcessor extends PaymentProcessor {
  async charge(amount, currency, details) {
    // PayPal-specific implementation
    const order = await paypal.orders.create({ amount, currency, payerId: details.payerId });
    return { id: order.id, status: 'success' };
  }
  
  async refund(transactionId, amount) {
    // PayPal refund logic
  }
}

// Usage — code doesn't know if it's Stripe or PayPal!
const processor = config.paymentGateway === 'stripe' ? new StripeProcessor() : new PayPalProcessor();
await processor.processPayment(99.99, 'USD', { token: 'tok_visa' });
```

---

## 🧱 Class Design (Complete Example — Ride Sharing)

```javascript
// Complete OOP design for Uber-like ride sharing

class Location {
  constructor(latitude, longitude) {
    this.latitude = latitude;
    this.longitude = longitude;
  }
  
  distanceTo(other) {
    // Haversine formula for GPS distance
    const R = 6371; // Earth radius in km
    const dLat = (other.latitude - this.latitude) * Math.PI / 180;
    const dLon = (other.longitude - this.longitude) * Math.PI / 180;
    const a = Math.sin(dLat/2)**2 +
              Math.cos(this.latitude * Math.PI/180) * 
              Math.cos(other.latitude * Math.PI/180) * 
              Math.sin(dLon/2)**2;
    return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
  }
  
  toString() { return `(${this.latitude}, ${this.longitude})`; }
}

class User {
  constructor(id, name, email, phone) {
    this.id = id;
    this.name = name;
    this.email = email;
    this.phone = phone;
    this.createdAt = new Date();
  }
}

class Driver extends User {
  constructor(id, name, email, phone, vehicle) {
    super(id, name, email, phone);
    this.vehicle = vehicle;
    this.rating = 5.0;
    this.totalRides = 0;
    this.currentLocation = null;
    this.isAvailable = false;
    this.status = 'offline'; // offline, available, on_ride
  }
  
  goOnline(location) {
    this.currentLocation = location;
    this.isAvailable = true;
    this.status = 'available';
  }
  
  goOffline() {
    this.isAvailable = false;
    this.status = 'offline';
  }
  
  updateLocation(location) {
    this.currentLocation = location;
  }
  
  acceptRide(ride) {
    if (!this.isAvailable) throw new Error('Driver not available');
    this.isAvailable = false;
    this.status = 'on_ride';
    ride.assignDriver(this);
  }
  
  completeRide(ride) {
    this.totalRides++;
    this.isAvailable = true;
    this.status = 'available';
    ride.complete();
  }
  
  updateRating(newRating) {
    this.rating = ((this.rating * this.totalRides) + newRating) / (this.totalRides + 1);
  }
}

class Rider extends User {
  constructor(id, name, email, phone, paymentMethod) {
    super(id, name, email, phone);
    this.paymentMethod = paymentMethod;
    this.rating = 5.0;
    this.totalRides = 0;
    this.activeRide = null;
  }
  
  requestRide(pickup, dropoff, rideType = 'standard') {
    if (this.activeRide) throw new Error('You already have an active ride');
    const ride = new Ride(this, pickup, dropoff, rideType);
    this.activeRide = ride;
    return ride;
  }
  
  cancelRide() {
    if (!this.activeRide) throw new Error('No active ride to cancel');
    if (this.activeRide.status === 'completed') throw new Error('Ride already completed');
    this.activeRide.cancel('rider_cancelled');
    this.activeRide = null;
  }
  
  rateDriver(driver, rating) {
    if (rating < 1 || rating > 5) throw new Error('Rating must be between 1 and 5');
    driver.updateRating(rating);
  }
}

class Ride {
  static #STATUS = Object.freeze({ PENDING: 'pending', ACCEPTED: 'accepted', IN_PROGRESS: 'in_progress', COMPLETED: 'completed', CANCELLED: 'cancelled' });
  
  constructor(rider, pickup, dropoff, rideType) {
    this.id = crypto.randomUUID();
    this.rider = rider;
    this.driver = null;
    this.pickup = pickup;
    this.dropoff = dropoff;
    this.rideType = rideType;
    this.status = Ride.#STATUS.PENDING;
    this.createdAt = new Date();
    this.startedAt = null;
    this.completedAt = null;
    this.fare = this.#calculateFare();
  }
  
  #calculateFare() {
    const distanceKm = this.pickup.distanceTo(this.dropoff);
    const baseFare = 2.0;
    const perKmRate = this.rideType === 'premium' ? 3.0 : 1.5;
    return +(baseFare + (distanceKm * perKmRate)).toFixed(2);
  }
  
  assignDriver(driver) {
    if (this.status !== Ride.#STATUS.PENDING) throw new Error('Can only assign driver to pending ride');
    this.driver = driver;
    this.status = Ride.#STATUS.ACCEPTED;
  }
  
  start() {
    if (this.status !== Ride.#STATUS.ACCEPTED) throw new Error('Ride must be accepted first');
    this.status = Ride.#STATUS.IN_PROGRESS;
    this.startedAt = new Date();
  }
  
  complete() {
    if (this.status !== Ride.#STATUS.IN_PROGRESS) throw new Error('Ride must be in progress');
    this.status = Ride.#STATUS.COMPLETED;
    this.completedAt = new Date();
    this.rider.activeRide = null;
    this.rider.totalRides++;
  }
  
  cancel(reason) {
    if ([Ride.#STATUS.COMPLETED, Ride.#STATUS.CANCELLED].includes(this.status)) {
      throw new Error('Cannot cancel completed or already cancelled ride');
    }
    this.status = Ride.#STATUS.CANCELLED;
    this.cancellationReason = reason;
    if (this.driver) {
      this.driver.isAvailable = true;
      this.driver.status = 'available';
    }
  }
  
  get duration() {
    if (!this.startedAt || !this.completedAt) return null;
    return Math.round((this.completedAt - this.startedAt) / 1000 / 60); // minutes
  }
}

// Usage:
const driver = new Driver('d1', 'Bob', 'bob@example.com', '+1234567890', { model: 'Toyota Camry', plate: 'XYZ123' });
const rider = new Rider('r1', 'Alice', 'alice@example.com', '+0987654321', { type: 'card', last4: '4242' });

driver.goOnline(new Location(40.7128, -74.0060));

const pickup = new Location(40.7589, -73.9851); // Times Square
const dropoff = new Location(40.6892, -74.0445); // Statue of Liberty

const ride = rider.requestRide(pickup, dropoff);
console.log(`Ride created: ${ride.id}, Fare: $${ride.fare}`);
// Distance: ~8.7km, Fare: $2 + (8.7 * 1.5) = ~$15

driver.acceptRide(ride);
ride.start();
driver.completeRide(ride);

rider.rateDriver(driver, 5);
console.log(`Driver rating: ${driver.rating}`); // Updated rating
```

---

## 🔍 Design Patterns Used

- **Factory Pattern:** `Ride.#calculateFare()` encapsulates fare calculation logic
- **Strategy Pattern:** Different fare strategies for different ride types
- **Observer Pattern:** Real-time location updates trigger notifications (can be extended)

---

## ⚖️ Trade-offs

| OOP | Functional |
|-----|------------|
| Clear entity modeling | Easy to compose |
| Encapsulation of state | Predictable (no side effects) |
| Inheritance for code reuse | Higher-order functions |
| Can get complex (deep hierarchies) | Simpler for stateless operations |

---

## 💼 Interview Questions (WITH SOLUTIONS)

### Q1: What are the four pillars of OOP?

**Solution:**
1. **Encapsulation:** Bundling data and methods together, hiding internal details. Private fields in JS (`#field`). Users interact through public methods only.
2. **Abstraction:** Exposing only necessary details, hiding complexity. `paymentProcessor.charge()` — you don't need to know how Stripe works internally.
3. **Inheritance:** Child classes inherit properties/methods from parent. `ElectricCar extends Car extends Vehicle`.
4. **Polymorphism:** Same interface, different implementations. `animal.speak()` returns different things for Dog, Cat, Bird.

### Q2: When would you use composition over inheritance?

**Solution:**
**Inheritance:** "IS-A" relationship. Dog IS-A Animal. ElectricCar IS-A Car.

**Composition:** "HAS-A" relationship. Car HAS-A Engine. User HAS-A PaymentMethod.

```javascript
// ❌ Inheritance for behaviors leads to rigid hierarchies
class FlyingSwimmingAnimal extends Animal { /* complex */ }

// ✅ Composition is more flexible
class Animal {
  constructor(name, behaviors) {
    this.name = name;
    this.behaviors = behaviors; // Inject behaviors!
  }
  move() { return this.behaviors.movement.move(); }
  speak() { return this.behaviors.vocal.speak(); }
}

const flyBehavior = { move: () => 'Flying' };
const swimBehavior = { move: () => 'Swimming' };
const duck = new Animal('Duck', { movement: { move: () => 'Flying and Swimming' } });
```

Rule: Favor composition for behaviors. Use inheritance for "IS-A" type relationships.

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem: Design a library management system using OOP

**Solution:**
```javascript
class Book {
  constructor(isbn, title, author, copies) {
    this.isbn = isbn;
    this.title = title;
    this.author = author;
    this.totalCopies = copies;
    this.availableCopies = copies;
  }
  get isAvailable() { return this.availableCopies > 0; }
  checkOut() {
    if (!this.isAvailable) throw new Error('No copies available');
    this.availableCopies--;
  }
  returnBook() { this.availableCopies = Math.min(this.totalCopies, this.availableCopies + 1); }
}

class Member {
  constructor(id, name, email) {
    this.id = id; this.name = name; this.email = email;
    this.borrowedBooks = [];
    this.maxBorrowLimit = 3;
  }
  borrow(book) {
    if (this.borrowedBooks.length >= this.maxBorrowLimit) throw new Error('Borrow limit reached');
    if (!book.isAvailable) throw new Error('Book not available');
    book.checkOut();
    this.borrowedBooks.push({ book, dueDate: new Date(Date.now() + 14 * 24 * 60 * 60 * 1000) });
  }
  return(book) {
    const idx = this.borrowedBooks.findIndex(b => b.book.isbn === book.isbn);
    if (idx === -1) throw new Error('Book not borrowed by this member');
    book.returnBook();
    this.borrowedBooks.splice(idx, 1);
  }
}

class Library {
  #catalog = new Map();
  #members = new Map();
  
  addBook(book) { this.#catalog.set(book.isbn, book); }
  registerMember(member) { this.#members.set(member.id, member); }
  searchByTitle(title) {
    return [...this.#catalog.values()].filter(b => b.title.toLowerCase().includes(title.toLowerCase()));
  }
  checkOut(memberId, isbn) {
    const member = this.#members.get(memberId);
    const book = this.#catalog.get(isbn);
    if (!member) throw new Error('Member not found');
    if (!book) throw new Error('Book not found');
    member.borrow(book);
  }
}
```

---

### Navigation
**Prev:** None | **Index:** [00_Index.md](../00_Index.md) | **Next:** [02_SOLID_Principles.md](02_SOLID_Principles.md)
