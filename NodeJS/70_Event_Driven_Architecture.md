# Event-Driven Architecture

## What You Will Learn
* The core concepts of Event-Driven Architecture (EDA).
* Distinguishing between Events, Commands, and Messages.
* The Publisher-Subscriber (Pub/Sub) pattern vs. Point-to-Point Message Queues.
* Designing Event Sourcing and CQRS (Command Query Responsibility Segregation).
* Navigating Eventual Consistency trade-offs in distributed systems.

## Why This Matters
Traditional APIs rely on synchronous, request-response communication (like REST). If Service A calls Service B, and Service B is down, the request fails. Event-Driven Architecture decouples services: they communicate by publishing events to a message broker. This allows services to continue running independently, improving system availability and scalability.

## Theory

### Event-Driven Principles
* **Decoupling**: Services do not know about each other's existences. They only publish events to, or consume events from, a central event broker, allowing you to add or modify services without changing existing ones.
* **Service Autonomy**: Services run independently, maintaining their own database states and processing tasks at their own speed.

### Events vs. Commands vs. Messages
* **Message**: The transport wrapper. A packet of data sent across the network containing headers and a body payload.
* **Command**: An instruction to perform a specific action (e.g. `CreateOrderCommand`). It has a single target receiver, is expected to execute immediately, and can fail.
* **Event**: A record of something that **has already occurred** in the system (e.g. `OrderCreatedEvent`). It is published to the broker, can have multiple subscribers, is immutable, and cannot be undone (only compensated).

## Deep Dive

### Pub/Sub vs. Message Queues
* **Point-to-Point Message Queues (e.g. Standard AMQP)**: A task is sent to a queue. Only **one consumer** processes the task (point-to-point). Once processed, the message is deleted. (Ideal for task distribution like sending emails).
* **Publisher-Subscriber (Pub/Sub)**: An event is published to a channel or topic. **Multiple subscribers** receive their own copy of the event simultaneously. (Ideal for broadcasting events like order notifications).

### Event Sourcing and CQRS
1. **Event Sourcing**: Instead of storing the current state of an object in a database table, the database stores the complete, sequential log of all state changes (events) that occurred on that object. You reconstruct the current state of the object by replaying the event log from the beginning.
2. **CQRS**: Separates write operations (Commands, which modify data) from read operations (Queries, which fetch data) into different models and databases. This allows you to optimize read databases (e.g., using Elasticsearch) and write databases independently.

## Visual Explanation

### Request-Response (Coupled) vs. Event-Driven (Decoupled)
```text
Request-Response (Coupled):
[ Client ] ──> [ Order Service ] ── HTTP POST ──> [ Payment Service ] (If down, checkout fails!)

Event-Driven (Decoupled):
[ Client ] ──> [ Order Service ] ──> Save Order (Pending)
                                          │
                                          ▼ (Publish: OrderCreated)
                                 [ Message Broker ]
                                   ├── Event ──> [ Payment Service ] (Charge card)
                                   └── Event ──> [ Email Service ]   (Send receipt)
```

## Real-World Example
Consider an e-commerce checkout. When a user buys a product, the Order Service saves a pending order and publishes an `OrderPlaced` event to Kafka. The Payment Service consumes this event to process the payment, the Inventory Service updates stock levels, and the Shipping Service schedules delivery. The Order Service does not wait for these services to finish, keeping checkout fast and responsive.

## Code Examples

### Simulating Pub/Sub and Event Queue Mechanics in Node.js

```javascript
// eda-demo.js
const { EventEmitter } = require('events');

// 1. Core Event Broker Simulation
class EventBroker extends EventEmitter {
  publish(eventType, eventData) {
    console.log(`[BROKER] Event Published: ${eventType} | Payload:`, eventData);
    this.emit(eventType, eventData);
  }

  subscribe(eventType, callback) {
    this.on(eventType, callback);
    console.log(`[BROKER] Service subscribed to topic: ${eventType}`);
  }
}

const broker = new EventBroker();

// 2. Event Consumers (Decoupled Services)
class InventoryService {
  constructor(eventBroker) {
    // Subscribe to OrderPlaced event
    eventBroker.subscribe('OrderPlaced', this.updateStock.bind(this));
  }

  updateStock(event) {
    console.log(`[INVENTORY-SERVICE] Reducing stock limits for items in Order: ${event.orderId}`);
  }
}

class EmailService {
  constructor(eventBroker) {
    eventBroker.subscribe('OrderPlaced', this.sendInvoice.bind(this));
  }

  sendInvoice(event) {
    console.log(`[EMAIL-SERVICE] Compiling and sending invoice for user ID: ${event.userId}`);
  }
}

// 3. Initialize Services
const inventory = new InventoryService(broker);
const email = new EmailService(broker);

// 4. Event Producer
class OrderService {
  constructor(eventBroker) {
    this.broker = eventBroker;
  }

  createOrder(userId, items) {
    const orderId = Math.floor(Math.random() * 10000);
    console.log(`\n[ORDER-SERVICE] Order ${orderId} saved locally in database.`);
    
    // Publish Event (describing something that HAS occurred)
    this.broker.publish('OrderPlaced', {
      orderId,
      userId,
      items,
      timestamp: new Date()
    });
  }
}

const orderService = new OrderService(broker);

// Execute Demo
orderService.createOrder(42, ['Laptop', 'Mouse']);
```

## Best Practices
* **Enforce Event Immutability**: Events represent historical facts. Never modify the payload of an event once it has been published.
* **Design for Eventual Consistency**: Accept that data takes time to replicate across services. Design user interfaces to handle eventual consistency (e.g. showing "Processing" status rather than assuming instant updates).
* **Write Small, Independent Event Payloads**: Include only the core identifiers and status changes in event payloads (e.g. Order ID, User ID, and Status). Let consumers query the publishing service's APIs if they need more details.

## Interview Questions

### Beginner
* **What is an Event in Event-Driven Architecture, and how does it differ from a Command?**
  *Answer*: An event represents a record of something that has already occurred in the system (e.g. `OrderCreated`). It is immutable, can have multiple subscribers, and cannot be rejected. A command is an instruction to perform a specific action (e.g. `CreateOrder`). It has a single target receiver, is expected to execute immediately, and can fail.

### Intermediate
* **What is the difference between point-to-point message queues and the publisher-subscriber (Pub/Sub) pattern?**
  *Answer*: Point-to-point queues deliver a message to exactly one consumer, who processes and deletes the message (ideal for task distribution like sending emails). Pub/Sub topics broadcast the message to all registered subscribers simultaneously, allowing multiple services to process the event independently.

### Advanced
* **What is Event Sourcing, and what are its main advantages and disadvantages?**
  *Answer*: Event Sourcing is a design pattern where the application stores the complete, sequential log of all state changes (events) that occurred on an object instead of saving its current state.
  * **Advantages**: Provides a perfect audit log of all changes, supports time-travel debugging (rebuilding state at any point in time), and makes write operations fast.
  * **Disadvantages**: Reading objects requires replaying the event log, which can be slow (mitigated by snapshots), and increases code complexity.

### Senior Architect
* **How would you architecture a high-volume system that handles Eventual Consistency across multiple microservices without violating domain boundaries? Discuss CQRS, read-model sync, and data synchronization.**
  *Answer*: To handle eventual consistency using CQRS and Event Sourcing:
  1. **Decouple Write/Read**: Separate the write database (optimized for transaction consistency, e.g. PostgreSQL) from the read databases (optimized for queries, e.g. Elasticsearch).
  2. **Publish State Events**: When the write service modifies data, it publishes a state change event (e.g. `UserUpdatedEvent`) to a message broker (like Kafka).
  3. **Sync Read Models**: A read model sync service consumes these events and updates the Elasticsearch query database asynchronously.
  4. **Manage Delay**: Because of network latency, the read database will lag slightly behind the write database. To manage this:
     - Use **Optimistic UI Updates**: Have the frontend update the UI instantly, assuming success.
     - Pass **version identifiers** in events to detect and reject out-of-order event delivery.
     - Configure clients to poll with backoff if a resource is queried immediately after updates.

---
Previous : [69_Microservices.md] | Index : [00_index.md] | Next : [71_RabbitMQ.md]
