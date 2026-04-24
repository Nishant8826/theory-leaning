# 📌 Event-Driven Architecture

## 🧠 Concept Explanation (Story Format)

Traditional way (request-response): You call your friend and wait on the phone for them to answer and give you news. If they're busy → you wait.

Event-driven way: You subscribe to your friend's Instagram. When they post something → you get notified. You're not waiting. They publish, you consume when ready.

In software:
- **Traditional (Synchronous):** Service A calls Service B directly and waits. B must be running.
- **Event-Driven:** Service A publishes an event ("order.placed"). Any number of services can listen and react in their own time.

When a user places an order on Amazon:
1. Order service emits: `order.placed` event
2. Payment service listens → charges the card
3. Inventory service listens → reserves the items
4. Email service listens → sends confirmation
5. Analytics service listens → records the sale
6. Recommendation service listens → updates "bought together" data

None of these services call each other. They all just react to the same event!

---

## 🏗️ Basic Design (Naive — Synchronous Chain)

```javascript
// ❌ Tightly coupled synchronous chain
async function placeOrder(orderData) {
  const order = await orderService.create(orderData);       // 50ms
  await paymentService.charge(order.id);                    // 500ms
  await inventoryService.reserve(order.items);              // 100ms
  await emailService.sendConfirmation(order.userId);        // 300ms
  await analyticsService.track(order);                      // 200ms
  return order; // User waits 1150ms total!
}

// Problems:
// - If emailService is down → entire order fails!
// - Adding new step = modifying this function
// - Hard to scale individual parts
// - Very slow for the user
```

---

## ⚡ Optimized Design (Event-Driven)

```
User places order
      ↓
Order Service → Creates order in DB
      ↓
Emits event: "order.placed" to Event Bus (SNS/Kafka/Redis Pub/Sub)
      ↓ (Order Service's job is DONE! Returns to user.)

Event Bus delivers to all subscribers:
  → Payment Service:     charges the card
  → Inventory Service:   reserves items
  → Email Service:       sends confirmation
  → Analytics Service:   records data
  → Recommendation Svc:  updates models

Each service processes independently, at their own pace.
If one fails → only that step fails, order is still saved.
```

---

## 🔍 Key Components

### Event vs Message Queue

```
Message Queue (Point-to-Point):
Producer → [Queue] → ONE Consumer
→ Only one consumer gets the message
→ Good for: work distribution (one worker processes one job)

Event/Topic (Pub/Sub):
Publisher → [Topic] → ALL Subscribers
→ All subscribers receive the event
→ Good for: notifications, fan-out (everyone needs to know)

In AWS:
SQS = Message Queue
SNS = Pub/Sub (can fan-out to multiple SQS queues)
EventBridge = More advanced event bus with routing rules
```

### Redis Pub/Sub (Simplest for Node.js)

```javascript
const redis = require('ioredis');
const publisher = new redis(process.env.REDIS_URL);
const subscriber = new redis(process.env.REDIS_URL);

// Publisher (Order Service)
async function placeOrder(orderData) {
  const order = await db.createOrder(orderData);
  
  // Publish event
  await publisher.publish('order.placed', JSON.stringify({
    orderId: order.id,
    userId: order.userId,
    items: order.items,
    total: order.total,
    timestamp: new Date().toISOString()
  }));
  
  return order;
}

// Subscriber (Email Service)
subscriber.subscribe('order.placed', (err) => {
  if (err) console.error('Subscribe error:', err);
});

subscriber.on('message', async (channel, message) => {
  if (channel === 'order.placed') {
    const event = JSON.parse(message);
    await emailService.sendOrderConfirmation(event.userId, event.orderId);
  }
});

// ⚠️ Redis Pub/Sub Limitation:
// If subscriber is offline when event is published → event is LOST!
// For guaranteed delivery → use SQS or Bull queues
```

### AWS EventBridge (Production-grade Event Bus)

```javascript
const AWS = require('aws-sdk');
const eventBridge = new AWS.EventBridge({ region: 'us-east-1' });

// Publish event to EventBridge
async function publishOrderEvent(eventType, orderData) {
  await eventBridge.putEvents({
    Entries: [{
      Source: 'order-service',
      DetailType: eventType,            // e.g., 'order.placed', 'order.shipped'
      Detail: JSON.stringify(orderData),
      EventBusName: 'ecommerce-events',
      Time: new Date()
    }]
  }).promise();
}

// In EventBridge console, create RULES to route events:
// Rule: "source = order-service AND detail-type = order.placed"
//   Target 1: SQS queue "payment-queue"     → Payment Service Lambda
//   Target 2: SQS queue "email-queue"       → Email Service Lambda
//   Target 3: SQS queue "inventory-queue"   → Inventory Service Lambda

// Each Lambda processes its own SQS queue independently!
```

### Event-Driven with Socket.IO for Real-time

```javascript
// Server-side: Emit events via Socket.IO for real-time UI updates
const { createAdapter } = require('@socket.io/redis-adapter');

io.adapter(createAdapter(pubClient, subClient));

// Payment service → Emits UI event when payment is confirmed
async function onPaymentSuccess(orderId, userId) {
  // Update DB
  await db.updateOrderStatus(orderId, 'paid');
  
  // Emit real-time event to user's browser
  io.to(`user:${userId}`).emit('order.paid', {
    orderId,
    message: 'Your payment was successful!'
  });
}

// React client
useEffect(() => {
  socket.on('order.paid', (data) => {
    toast.success(data.message);
    navigate(`/orders/${data.orderId}`);
  });
  
  return () => socket.off('order.paid');
}, []);
```

---

### Event Sourcing Pattern

Instead of storing current state, store ALL events that led to the state:

```javascript
// Traditional: Store current account balance
// accounts table: { id: '123', balance: 500 }

// Event Sourcing: Store every event
// account_events table: 
// { id: 1, accountId: '123', type: 'deposit', amount: 1000 }
// { id: 2, accountId: '123', type: 'withdraw', amount: 500 }
// Current balance = 1000 - 500 = 500

// Benefits:
// - Full audit trail (know HOW we got to current state)
// - Can replay events to reconstruct any past state
// - Time travel: "What was balance on Jan 15?"

class AccountEventStore {
  async append(event) {
    await db.query(
      'INSERT INTO account_events (account_id, type, amount, metadata, created_at) VALUES ($1, $2, $3, $4, NOW())',
      [event.accountId, event.type, event.amount, JSON.stringify(event.metadata)]
    );
  }
  
  async getBalance(accountId) {
    const events = await db.query(
      'SELECT * FROM account_events WHERE account_id = $1 ORDER BY created_at ASC',
      [accountId]
    );
    
    return events.rows.reduce((balance, event) => {
      if (event.type === 'deposit') return balance + event.amount;
      if (event.type === 'withdraw') return balance - event.amount;
      return balance;
    }, 0);
  }
  
  // Replay to get state at a specific point in time
  async getBalanceAtTime(accountId, timestamp) {
    const events = await db.query(
      'SELECT * FROM account_events WHERE account_id = $1 AND created_at <= $2',
      [accountId, timestamp]
    );
    return events.rows.reduce((bal, ev) => bal + (ev.type === 'deposit' ? ev.amount : -ev.amount), 0);
  }
}
```

---

## ⚖️ Trade-offs

| Event-Driven | Request-Response |
|-------------|-----------------|
| Loose coupling | Tight coupling |
| Easy to add new consumers | Must modify producer to add consumers |
| Async (fast) | Sync (slower) |
| Hard to trace (async) | Easy to trace (sync) |
| Eventual consistency | Immediate consistency |
| More complex debugging | Simpler debugging |

---

## 📊 Scalability Discussion

### CQRS Pattern (Command Query Responsibility Segregation)

```
COMMAND side (writes): 
  User writes → Command Handler → Write DB (PostgreSQL)
                              → Emits events

QUERY side (reads):
  Events → Read Model Builder → Read DB (MongoDB/Redis)
  User reads → Query Handler → Read DB (optimized for reads)

Why?
- Write side optimized for consistency (ACID)
- Read side optimized for performance (denormalized, pre-computed)

Example: Twitter
- Command: "tweet posted" → Write to write DB
- Event triggers: Build timeline for all followers in Redis
- Query: "show me my timeline" → Read from Redis (super fast!)
```

---

## 💼 Interview Questions (WITH SOLUTIONS)

### Q1: What is Event-Driven Architecture and when should you use it?

**Solution:**
EDA is an architectural pattern where services communicate by producing and consuming events asynchronously, rather than calling each other directly.

**Use when:**
1. Multiple services need to react to the same event (fan-out)
2. You want loose coupling between services
3. You need async processing (don't want user to wait)
4. Services evolve independently (new services can subscribe without changing others)

**Don't use when:**
1. You need an immediate response to know if something succeeded (use sync call)
2. Strong consistency is required (EDA is eventually consistent)
3. Simple request-response is sufficient (YAGNI — don't add complexity you don't need)

---

### Q2: What is the difference between Event-Driven and Microservices?

**Solution:**
These are separate concepts that work well together:
- **Microservices** = architectural style where you split your monolith into small, independent services
- **Event-Driven** = communication style where services talk via events (asynchronously)

You can have:
- Monolith with event-driven (internal events within one service)
- Microservices without EDA (microservices calling each other via REST)
- Microservices + EDA (most scalable combination)

Most large systems use **microservices + event-driven communication** for loose coupling and scalability.

---

### Q3: How do you handle the "dual write problem" in event-driven systems?

**Solution:**
**Problem:** You write to DB and then publish an event. What if the publish fails? DB has the data but no event was sent!

```javascript
// ❌ Dual write problem
async function placeOrder(data) {
  await db.save(order);          // Step 1: DB write succeeds
  await eventBus.publish(event); // Step 2: What if this fails?!
  // Order is in DB but no event → inventory not reserved, no email sent!
}
```

**Solutions:**

1. **Transactional Outbox Pattern (Best):**
```javascript
// Write event to DB in same transaction as the data!
async function placeOrder(data) {
  const client = await pool.connect();
  await client.query('BEGIN');
  try {
    const order = await client.query('INSERT INTO orders...', [...]);
    
    // Write event to outbox table (same transaction!)
    await client.query(
      'INSERT INTO outbox (event_type, payload, status) VALUES ($1, $2, $3)',
      ['order.placed', JSON.stringify({ orderId: order.id }), 'pending']
    );
    
    await client.query('COMMIT');
  } catch (e) {
    await client.query('ROLLBACK');
    throw e;
  }
  
  // Separate process reads outbox and publishes to event bus
  // If publish fails → retry from outbox → never lose events!
}

// Outbox reader (runs every second)
setInterval(async () => {
  const pending = await db.query(
    "SELECT * FROM outbox WHERE status = 'pending' ORDER BY created_at LIMIT 10"
  );
  for (const event of pending.rows) {
    await eventBus.publish(event.payload);
    await db.query("UPDATE outbox SET status = 'published' WHERE id = $1", [event.id]);
  }
}, 1000);
```

2. **Saga Pattern:** For distributed transactions across multiple services.

---

### Q4: What is the Saga pattern in event-driven systems?

**Solution:**
A Saga is a sequence of local transactions, each publishing events to trigger the next step. If one step fails, compensating transactions undo previous steps.

```
Order Saga:
1. Order Service: Create order (status: pending)
   ↓ event: order.created
2. Payment Service: Charge payment
   ↓ success: event: payment.succeeded
   ↓ failure: event: payment.failed → ORDER: compensate → cancel order
3. Inventory Service: Reserve items
   ↓ success: event: inventory.reserved
   ↓ failure: event: inventory.failed → PAYMENT: compensate → refund → ORDER: cancel
4. Shipping Service: Create shipment
   → Final success!

Each step either succeeds (triggers next) or fails (triggers compensations)
```

```javascript
// Saga orchestrator (one approach)
class OrderSaga {
  async start(orderId) {
    await this.step1_createOrder(orderId);
  }
  
  async step1_createOrder(orderId) {
    try {
      await orderService.confirm(orderId);
      await this.step2_chargePayment(orderId);
    } catch (error) {
      await orderService.cancel(orderId); // Compensate
    }
  }
  
  async step2_chargePayment(orderId) {
    try {
      await paymentService.charge(orderId);
      await this.step3_reserveInventory(orderId);
    } catch (error) {
      await paymentService.refund(orderId); // Compensate
      await orderService.cancel(orderId);    // Compensate step 1
    }
  }
}
```

---

### Q5: How do you ensure event ordering in an event-driven system?

**Solution:**
Strict ordering is expensive and limits scalability. Common approaches:

1. **Partition by key (Kafka):** All events for the same entity (same orderId) go to the same partition → guaranteed ordering for that entity.

2. **Sequence numbers:** Attach sequence number to events. Consumers process in order.

3. **Timestamps + idempotency:** Don't rely on ordering. Make operations idempotent. Last-write-wins based on timestamp.

4. **State machine:** Use a state machine that only accepts valid state transitions.
```javascript
const validTransitions = {
  'pending': ['confirmed', 'cancelled'],
  'confirmed': ['shipped', 'cancelled'],
  'shipped': ['delivered'],
  'delivered': [],
  'cancelled': []
};

async function updateOrderStatus(orderId, newStatus) {
  const order = await db.getOrder(orderId);
  
  if (!validTransitions[order.status].includes(newStatus)) {
    throw new Error(`Invalid transition: ${order.status} → ${newStatus}`);
  }
  
  await db.updateStatus(orderId, newStatus);
}
// Even if events arrive out of order, invalid transitions are rejected!
```

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem 1: Design a notification system using Event-Driven Architecture

**Solution:**
```javascript
// Event types:
// post.liked, comment.added, user.followed, mention.created, order.shipped

// Notification Service subscribes to ALL events
const notificationQueue = new Bull('notifications', redisConfig);

// When any event occurs, it's routed here
notificationQueue.process(20, async (job) => {
  const event = job.data;
  
  // Determine who to notify
  const recipients = await getRecipients(event);
  
  for (const recipient of recipients) {
    const prefs = await getUserNotificationPrefs(recipient.userId);
    
    // Send via appropriate channels based on user preferences
    const sends = [];
    if (prefs.push) sends.push(sendPushNotification(recipient, event));
    if (prefs.email && event.type !== 'post.liked') sends.push(sendEmail(recipient, event));
    if (prefs.inApp) sends.push(saveInAppNotification(recipient, event));
    
    await Promise.allSettled(sends); // Don't fail if one channel fails
  }
});

// Real-time in-app notifications via Socket.IO
async function saveInAppNotification(recipient, event) {
  const notification = await db.createNotification({ recipientId: recipient.userId, event });
  
  // Push to client if they're online
  io.to(`user:${recipient.userId}`).emit('notification', notification);
}

// User's React app:
// useEffect → socket.on('notification', (data) => { 
//   setNotifications(prev => [data, ...prev]);
//   showToast(data.message);
// })
```

---

### Problem 2: An event was published but one consumer failed. How do you recover?

**Solution:**
```
Design for failure from the start:

1. Use message queues instead of direct pub/sub:
   Event → SNS → SQS (per consumer) → Worker
   SQS retains message if consumer fails.

2. Idempotent consumers:
   - Use event ID + status tracking to prevent double-processing
   - Check "already processed?" before doing work

3. Dead Letter Queue:
   - SQS automatically moves failed messages to DLQ after N retries
   - Monitor DLQ size (CloudWatch alarm)
   - Manual review + replay from DLQ

4. Retry policy in Bull:
   - attempts: 5, backoff: exponential
   - Automatically retries with increasing delays

5. Alerting:
   - Alert when DLQ has messages
   - Alert when consumer error rate > 1%
   - On-call engineer investigates

6. Event replay capability:
   - Store all events in an event store (S3 or PostgreSQL)
   - If consumer has a bug and processes incorrectly:
     - Fix the bug
     - Replay events from store for the affected time window
   
   // Replay events from store
   const failedPeriod = { from: '2024-01-15T10:00:00Z', to: '2024-01-15T11:00:00Z' };
   const events = await eventStore.getRange(failedPeriod);
   for (const event of events) {
     await emailQueue.add(event, { priority: 1 });
   }
```

---

### Navigation
**Prev:** [14_Message_Queues.md](14_Message_Queues.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [16_Microservices.md](16_Microservices.md)
