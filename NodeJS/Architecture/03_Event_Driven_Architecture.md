# 📌 03 — Event-Driven Architecture: Pub/Sub and Message Brokers

## 🧠 Concept Explanation

### Basic → Intermediate
Event-Driven Architecture (EDA) is a pattern where services communicate by producing and consuming events rather than making direct synchronous requests. An "Event" is a notification that "something has happened" (e.g. `OrderPlaced`).

### Advanced → Expert
At a staff level, EDA is about **Temporal Decoupling**. 
1. **Producer**: Emits an event to a **Message Broker** (Kafka, RabbitMQ, SNS/SQS).
2. **Broker**: Persists and routes the message.
3. **Consumer**: Subscribes to the event and processes it at its own pace.

This solves the problem of **Cascading Failures**. If the Email Service is down, the Order Service can still place orders; the Email Service will just process the "Send Email" events once it comes back online.

---

## 🏗️ Common Mental Model
"Events are just async function calls."
**Correction**: Events are **Immutable State Transitions**. Once an event is published, it cannot be changed. Multiple consumers can react to the same event in different ways without the producer knowing about them.

---

## ⚡ Actual Behavior: Delivery Guarantees
Brokers offer different levels of reliability:
- **At most once**: Fast, but messages can be lost.
- **At least once**: No message loss, but duplicates are possible.
- **Exactly once**: Very hard to achieve; requires transactional coordination.

Most Node.js systems aim for **At least once** and ensure consumers are **Idempotent**.

---

## 🔬 Internal Mechanics (Networking + Brokers)

### Push vs Pull
- **RabbitMQ (Push)**: The broker pushes messages to consumers as they arrive.
- **Kafka (Pull)**: Consumers pull batches of messages from the broker at their own speed. This allows for better **Backpressure** management.

### Fan-out
A single producer emits one event, and the broker "fans it out" to multiple queues (e.g. one for Shipping, one for Analytics, one for Email).

---

## 📐 ASCII Diagrams

### Event-Driven Flow
```text
  ┌───────────────┐          ┌────────────────┐          ┌───────────────┐
  │ ORDER SERVICE │ ──EVENT─▶│ MESSAGE BROKER │ ──FANout▶│ EMAIL SERVICE │
  │ (Producer)    │          │ (Kafka/Rabbit) │          └───────────────┘
  └───────────────┘          └──────┬─────────┘          ┌───────────────┐
                                    │                    │ SHIP SERVICE  │
                                    └───────────────────▶└───────────────┘
```

---

## 🔍 Code Example: RabbitMQ Producer/Consumer
```javascript
const amqp = require('amqplib');

// PRODUCER
async function publishEvent(event) {
  const conn = await amqp.connect('amqp://localhost');
  const channel = await conn.createChannel();
  const exchange = 'events_exchange';
  
  await channel.assertExchange(exchange, 'fanout', { durable: true });
  channel.publish(exchange, '', Buffer.from(JSON.stringify(event)));
  console.log(" [x] Sent Event");
}

// CONSUMER
async function startConsumer() {
  const conn = await amqp.connect('amqp://localhost');
  const channel = await conn.createChannel();
  const queue = 'email_queue';
  
  await channel.assertQueue(queue, { durable: true });
  channel.consume(queue, (msg) => {
    const event = JSON.parse(msg.content.toString());
    processEmail(event); // Business logic
    channel.ack(msg); // Acknowledge completion
  });
}
```

---

## 💥 Production Failures & Debugging

### Scenario: The Poison Pill Message
**Problem**: A malformed message enters the queue. The consumer tries to process it, crashes, restarts, and tries again—forever. The queue stops moving.
**Reason**: No error handling for invalid payloads.
**Fix**: Use a **Dead Letter Queue (DLQ)**. If a message fails X times, move it to a separate queue for manual inspection.

### Scenario: Race Conditions in Consumers
**Problem**: Two consumers process `OrderUpdated` events for the same order. Consumer A gets version 2, then Consumer B gets version 1 because of network jitter.
**Reason**: Out-of-order delivery.
**Fix**: Use **Optimistic Locking** or ensure the broker maintains order for specific keys (e.g. Kafka Partitions keyed by OrderId).

---

## 🧪 Real-time Production Q&A

**Q: "When should I use SNS/SQS vs Kafka?"**
**A**: Use **SNS/SQS** for simple, low-maintenance task queues and notifications. Use **Kafka** if you need high-throughput event streaming, message replayability, or "Log-structured" storage where you can re-process history.

---

## 🏢 Industry Best Practices
- **Schema Registry**: Use Protobuf or Avro to ensure producers and consumers agree on the event structure.
- **Keep Events Small**: Don't send a massive database record in an event. Send the ID and the specific change.

---

## 💼 Interview Questions
**Q: What is Idempotency and why is it vital in EDA?**
**A**: Idempotency means that performing the same operation multiple times has the same result as performing it once. In EDA, messages can be delivered twice (At-least-once). Your consumer must check if it has already processed that specific `EventId` before taking action.

---

## 🧩 Practice Problems
1. Implement a "Retry with Delay" mechanism using RabbitMQ's TTL and Dead Letter Exchanges.
2. Design a system where a single "UserSignup" event triggers 3 different actions in 3 different services.

---

**Prev:** [02_API_Gateway_Pattern.md](./02_API_Gateway_Pattern.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [04_Message_Queues.md](./04_Message_Queues.md)
