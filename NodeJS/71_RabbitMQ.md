# RabbitMQ

## What You Will Learn
* The Advanced Message Queuing Protocol (AMQP) core architecture.
* The roles of Producers, Exchanges, Bindings, Queues, and Consumers.
* Configuring Exchange Types: Direct, Fanout, Topic, and Headers.
* Connecting to RabbitMQ in Node.js using the `amqplib` library.
* Message Acknowledgments (`ack`, `nack`, `reject`) to prevent data loss.
* Implementing Dead Letter Exchanges (DLX) for failed messages.

## Why This Matters
For high-throughput applications, you need a message broker that supports complex message routing rules and guarantees delivery. RabbitMQ is an enterprise-grade AMQP message broker. If you do not configure message acknowledgments correctly, network drops or crashed consumer processes can cause lost or duplicated messages, resulting in data corruption.

## Theory

### AMQP Architecture Components
RabbitMQ is built on the **AMQP** protocol. It separates message publishers from message queues using **Exchanges**:

```text
  [ Producer ] ── publishes ──> [ Exchange ]
                                     │
                                     ├── (Binding Rules: Routing Key)
                                     ▼
                              [ Queue Space ] ── delivers ──> [ Consumer ]
```

* **Producer**: The application service that publishes messages.
* **Exchange**: Receives messages from producers and routes them to queues based on binding rules.
* **Binding**: The link configuration between an exchange and a queue.
* **Queue**: A buffer that stores messages in memory or disk until consumed.
* **Consumer**: The application service that processes messages.

### Exchange Types
1. **Direct**: Routes messages to queues based on an exact match of the **Routing Key** (e.g. routing key `logs.error` matches queue `error-logs`).
2. **Fanout**: Ignores routing keys. It duplicates and broadcasts the message to **all** queues bound to it. (Ideal for Pub/Sub).
3. **Topic**: Routes messages to queues based on wildcard matches of routing keys. Wildcards use:
   * `*` (star) to match exactly one word (e.g. `logs.*` matches `logs.info` but not `logs.info.db`).
   * `#` (hash) to match zero or more words (e.g. `logs.#` matches `logs.info` and `logs.info.db`).

## Deep Dive

### Message Acknowledgments (Ack/Nack)
To prevent data loss, RabbitMQ does not delete a message from a queue as soon as it is sent to a consumer. It waits for confirmation:
* **`channel.ack(message)`**: The consumer has processed the message successfully. RabbitMQ can delete the message.
* **`channel.nack(message, allUpTo, requeue)`**: The consumer failed to process the message. If `requeue` is true, RabbitMQ puts the message back in the queue. If false, it deletes it or routes it to a DLX.
* **`channel.reject(message, requeue)`**: Rejects a single message (similar to `nack`).

### Dead Letter Exchanges (DLX)
If a message fails to process after multiple attempts, or is rejected with `requeue = false`, you do not want it to be lost. Configure a **Dead Letter Exchange (DLX)**:
* RabbitMQ automatically routes failed or rejected messages to the DLX.
* The DLX routes the message to a Dead Letter Queue (DLQ) for manual audit or debugging, preventing data loss.

## Visual Explanation

### Topic Exchange Routing Pattern
```text
Exchange: topic_logs
Queue A (Bound to: *.error)     <-- Receives: app1.error, db.error
Queue B (Bound to: db.#)        <-- Receives: db.error, db.info, db.info.replica

Incoming Message: Routing Key = db.error
  - Result: Matches Queue A (*.error) and Queue B (db.#). Both queues receive a copy of the message!

Incoming Message: Routing Key = app1.info
  - Result: No match. The message is discarded.
```

## Real-World Example
Consider an invoice generation service. When a client requests a PDF invoice, the order service publishes the invoice data to a direct exchange with routing key `invoice.generate`. The invoice queue receives the message. The PDF worker consumes the message, generates the PDF, and calls `ack()`. If the worker crashes mid-generation, RabbitMQ detects the connection drop and requeues the task, ensuring the PDF is eventually generated.

## Code Examples

### Connecting, Publishing, and Consuming with `amqplib`

```javascript
// db/rabbitConnection.js
// Dependency required: npm install amqplib
const amqplib = require('amqplib');

const RABBIT_URL = process.env.RABBIT_URL || 'amqp://localhost:5672';

let connectionInstance = null;

async function getRabbitConnection() {
  if (connectionInstance) return connectionInstance;

  try {
    connectionInstance = await amqplib.connect(RABBIT_URL);
    console.log('Successfully established connection to RabbitMQ server.');
    return connectionInstance;
  } catch (err) {
    console.error('RabbitMQ connection error:', err.message);
    process.exit(1);
  }
}

module.exports = { getRabbitConnection };
```

```javascript
// worker-consumer.js
const { getRabbitConnection } = require('./db/rabbitConnection');

async function startConsumer() {
  const conn = await getRabbitConnection();
  const channel = await conn.createChannel();

  const EXCHANGE_NAME = 'order_exchange';
  const QUEUE_NAME = 'process_payment_queue';
  const DLX_NAME = 'dead_letter_exchange';
  const DLQ_NAME = 'failed_payments_dlq';

  // 1. Declare Dead Letter Exchange and Queue
  await channel.assertExchange(DLX_NAME, 'direct', { durable: true });
  await channel.assertQueue(DLQ_NAME, { durable: true });
  await channel.bindQueue(DLQ_NAME, DLX_NAME, 'payment_failed');

  // 2. Declare Main Exchange and Queue with DLX configuration
  await channel.assertExchange(EXCHANGE_NAME, 'direct', { durable: true });
  await channel.assertQueue(QUEUE_NAME, {
    durable: true,
    arguments: {
      'x-dead-letter-exchange': DLX_NAME,
      'x-dead-letter-routing-key': 'payment_failed'
    }
  });
  
  await channel.bindQueue(QUEUE_NAME, EXCHANGE_NAME, 'payment_route');

  // 3. Consume messages with manual acknowledgment (noAck: false)
  channel.consume(QUEUE_NAME, async (msg) => {
    if (!msg) return;

    try {
      const payload = JSON.parse(msg.content.toString());
      console.log(`[CONSUMER] Received payment task for order ID: ${payload.orderId}`);

      if (payload.amount <= 0) {
        throw new Error('Invalid payment amount. Processing failed.');
      }

      // Simulate success
      console.log(`[CONSUMER] Payment processed successfully for: ${payload.amount}`);
      channel.ack(msg); // Acknowledge successful processing

    } catch (err) {
      console.error(`[CONSUMER ERROR] Processing failed: ${err.message}`);
      
      // Reject message and send it to the Dead Letter Queue (requeue = false)
      channel.nack(msg, false, false);
      console.log('[CONSUMER] Message rejected and routed to Dead Letter Queue.');
    }
  }, { noAck: false });

  console.log(`Worker listening for messages in: ${QUEUE_NAME}`);
}
startConsumer();
```

## Best Practices
* **Always set `noAck: false`**: Never configure auto-acknowledgments (`noAck: true`) for critical tasks. If the consumer crashes before completing the task, the message is lost. Use manual acknowledgments instead.
* **Pre-fetch Messages Limits**: Set pre-fetch limits using `channel.prefetch(n)` (e.g. `n = 10`). This tells RabbitMQ to send at most `n` messages to a worker at a time, preventing a single worker from being overloaded while others sit idle.
* **Use Dead Letter Exchanges (DLX)**: Configure a DLX on all queues to capture and debug failed messages without blocking the queue.

## Interview Questions

### Beginner
* **What is RabbitMQ and what protocol does it use?**
  *Answer*: RabbitMQ is an open-source message broker that routes and queues messages. It is built on the **AMQP** (Advanced Message Queuing Protocol) standard.

### Intermediate
* **What is the difference between Direct and Topic exchanges in RabbitMQ?**
  *Answer*: A **Direct** exchange routes messages to queues based on an exact match of the routing key. A **Topic** exchange routes messages using wildcard patterns: `*` matches exactly one word, and `#` matches zero or more words, supporting complex routing.

### Advanced
* **What are message acknowledgments in RabbitMQ, and what is the difference between `ack`, `nack`, and `reject`?**
  *Answer*: Acknowledgments are confirmations sent by consumers to RabbitMQ:
  * **`ack`**: Confirms success; RabbitMQ deletes the message.
  * **`nack`**: Signals failure; can reject multiple messages and optionally requeue them.
  * **`reject`**: Signals failure for a single message, optionally requeuing it or routing it to a Dead Letter Queue (DLQ).

### Senior Architect
* **How would you architecture a high-availability RabbitMQ cluster that guarantees message persistence and prevents data loss during broker failovers?**
  *Answer*: To ensure high availability and durability:
  1. **Quorum Queues**: Configure queues as **Quorum Queues** instead of classic queues. Quorum queues replicate data across multiple cluster nodes using the Raft consensus algorithm, protecting data if a broker crashes.
  2. **Configure Publisher Confirms**: Enable publisher confirms on the channel (`channel.confirmSelect()`). This ensures the broker sends an acknowledgment to the producer once the message is written to disk, preventing data loss in transit.
  3. **Persist Messages**: Set `persistent: true` in publishing options, and set `durable: true` when declaring exchanges and queues to ensure they survive broker restarts.
  4. **Connection Heartbeats**: Configure connection heartbeats to detect network drops and automatically reconnect.

---
Previous : [70_Event_Driven_Architecture.md] | Index : [00_index.md] | Next : [72_Kafka.md]
