# Kafka

## What You Will Learn
* The architecture of Apache Kafka as a distributed commit log.
* Core components: Producers, Topics, Partitions, Consumer Groups, and Offsets.
* Key differences between Kafka and RabbitMQ.
* Connecting to Kafka in Node.js using the `kafkajs` library.
* Managing partition scaling and consumer rebalancing.

## Why This Matters
For high-volume, real-time data streaming (like tracking user clickstreams, processing financial transactions, or gathering system metrics), traditional message queues like RabbitMQ can struggle. Kafka is a distributed event streaming platform designed for high throughput. It stores events in a partitionable commit log, allowing multiple consumers to read and replay events independently at scale.

## Theory

### Kafka Architecture: Distributed Commit Log
Kafka does not use exchanges and queues. Instead, it stores events in a **Topic**, which is structured as a partitioned commit log:

```text
[ Topic: user-events ]
  ├── Partition 0: [ Event 0 ] [ Event 1 ] [ Event 2 ]  <-- Offset (0, 1, 2)
  ├── Partition 1: [ Event 0 ] [ Event 1 ]              <-- Offset (0, 1)
  └── Partition 2: [ Event 0 ] [ Event 1 ] [ Event 2 ]  <-- Offset (0, 1, 2)
```

* **Partition**: Topics are divided into multiple **Partitions** distributed across cluster nodes. This allows Kafka to scale write and read operations horizontally.
* **Offset**: A unique sequential integer assigned to each event within a partition. Consumers track their progress by committing their current offset value.
* **Consumer Group**: A group of consumers that cooperate to read events from a topic. Kafka assigns each partition in the topic to exactly one consumer in the group, preventing duplicate processing.

### Kafka vs. RabbitMQ
| Feature | Apache Kafka | RabbitMQ |
| :--- | :--- | :--- |
| **Model** | Distributed Commit Log (Pull model) | Message Broker (Push model) |
| **Persistence** | Permanent (Retained based on retention policies) | Temporary (Deleted once acknowledged) |
| **Event Replay** | Yes (Move offset pointer back to reprocess) | No (Message is deleted) |
| **Routing** | Simple key-based partition routing | Complex routing rules (Topic/Headers exchanges) |

## Deep Dive

### Consumer Group Scaling and Rebalancing
To scale consumption, you add more consumer instances to a **Consumer Group**:
* **Even Distribution**: If a topic has 4 partitions, and your group has 2 consumers, Kafka assigns 2 partitions to each consumer.
* **Max Limit**: If you add more consumers than partitions (e.g. 5 consumers for 4 partitions), the extra consumer sits idle. The maximum scaling limit of a consumer group is defined by the number of partitions.
* **Rebalancing**: If a consumer crashes, Kafka triggers a **Rebalance**, reassigning its partitions to the remaining active consumers to keep data processing online.

## Visual Explanation

### Consumer Group Partition Allocation
```text
Topic Partitions:
[ Partition 0 ]     [ Partition 1 ]     [ Partition 2 ]     [ Partition 3 ]
       │                   │                   │                   │
       ▼                   ▼                   ▼                   ▼
[ Consumer 1 ]      [ Consumer 1 ]      [ Consumer 2 ]      [ Consumer 2 ]
  (Allocated)         (Allocated)         (Allocated)         (Allocated)

*Note*: Active Consumer Group contains 2 instances. Each instance handles 2 partitions.
If Consumer 1 crashes, Kafka rebalances and assigns all 4 partitions to Consumer 2.
```

## Real-World Example
Consider an activity log pipeline that tracks page views. The website publishes view events to Kafka. You configure a topic with 12 partitions. You run a cluster of 6 Node.js consumer instances inside a consumer group. Each instance processes events from 2 partitions in parallel. If traffic spikes, you can scale the consumer cluster up to 12 instances to handle the load, optimizing throughput.

## Code Examples

### Producing and Consuming Messages using Kafkajs

```javascript
// db/kafkaClient.js
// Dependency required: npm install kafkajs
const { Kafka } = require('kafkajs');

// 1. Initialize Kafka Client
const kafka = new Kafka({
  clientId: 'mastery-app',
  brokers: [process.env.KAFKA_BROKER || 'localhost:9092']
});

module.exports = kafka;
```

```javascript
// producer.js (Event Publisher)
const kafka = require('./db/kafkaClient');

async function runProducer() {
  const producer = kafka.producer();
  await producer.connect();
  console.log('Kafka Producer connected.');

  try {
    // Publish message to 'user-signups' topic
    const record = await producer.send({
      topic: 'user-signups',
      messages: [
        {
          key: 'user-101', // Partition routing key (guarantees same user goes to same partition)
          value: JSON.stringify({ userId: 101, email: 'bob@db.com', timestamp: Date.now() })
        }
      ]
    });
    console.log('[PRODUCER] Message successfully sent to partition:', record[0].partition);

  } catch (err) {
    console.error('Failed to publish event:', err.message);
  } finally {
    await producer.disconnect();
  }
}
runProducer();
```

```javascript
// consumer.js (Event Subscriber)
const kafka = require('./db/kafkaClient');

async function runConsumer() {
  // 1. Initialize Consumer and join a Consumer Group
  const consumer = kafka.consumer({ groupId: 'analytics-group' });
  
  await consumer.connect();
  console.log('Kafka Consumer connected.');

  // 2. Subscribe to the target topic
  await consumer.subscribe({ topic: 'user-signups', fromBeginning: true });

  // 3. Start processing events
  await consumer.run({
    eachMessage: async ({ topic, partition, message }) => {
      const payload = JSON.parse(message.value.toString());
      console.log(`[CONSUMER] Received event from Partition ${partition} | Offset: ${message.offset}`);
      console.log('User Signup Event Payload:', payload);
      
      // Kafkajs automatically commits offsets after this callback returns successfully
    }
  });
}
runConsumer().catch(console.error);
```

## Best Practices
* **Use Keys for Ordered Events**: When publishing events that require strict ordered processing (like user banking transactions), always specify a partition **Key** (e.g. `userId`). Kafka hashes the key to ensure that all events with the same key are written to the same partition, guaranteeing they are processed in order.
* **Commit Offsets Safely**: Ensure your consumer handles errors correctly. If a consumer fails to process a message but commits the offset anyway, that message is skipped and lost.
* **Match Partitions to Consumer Count**: Avoid running more consumer instances in a group than there are partitions in the topic, as the extra consumers will sit idle.

## Interview Questions

### Beginner
* **What is a Topic and a Partition in Apache Kafka?**
  *Answer*: A topic is a named category or feed to which events are published. A partition is a physical, ordered log segment within a topic. Topics are divided into multiple partitions distributed across cluster nodes to support parallel processing.

### Intermediate
* **What is a Consumer Group in Kafka, and how does it scale data processing?**
  *Answer*: A consumer group is a collection of consumers that collaborate to read events from a topic. Kafka ensures that each partition in the topic is assigned to exactly one consumer in the group, allowing multiple instances to process events in parallel without duplicating messages.

### Advanced
* **Compare Kafka and RabbitMQ. In what scenario would you choose Kafka over RabbitMQ?**
  *Answer*: 
  * **RabbitMQ**: A message broker that routes messages using complex rules and deletes them once acknowledged (push model). Ideal for task queues and simple transactional notifications.
  * **Kafka**: A distributed commit log that stores events permanently in partitions, allowing consumers to pull and replay events (pull model).
  * *Selection Criteria*: Choose **Kafka** for high-volume, real-time data streaming (like activity logs, clickstreams, or telemetry metrics) where you need high write throughput, event replay capabilities, or want to distribute data to multiple systems independently.

### Senior Architect
* **How would you handle a "poison pill" message (a malformed event that crashes the consumer during JSON parsing) in a Kafka consumer loop, ensuring the pipeline continues processing subsequent events?**
  *Answer*: A poison pill message will cause the consumer callback to throw an exception repeatedly. Because Kafkajs will not commit the offset until the callback completes, the consumer gets stuck retrying the same malformed message, blocking the entire partition.
  To resolve this:
  1. Implement a try/catch block around the JSON parsing and message processing logic.
  2. If an exception occurs:
     - Log the error details and message payload immediately.
     - Publish the malformed message payload to a separate **Dead Letter Topic** (DLT) in Kafka.
     - Call the commit offset method manually or return successfully from the callback to allow the consumer to advance to the next message, preventing the pipeline from hanging.

---
Previous : [71_RabbitMQ.md] | Index : [00_index.md] | Next : [73_Distributed_Systems.md]
