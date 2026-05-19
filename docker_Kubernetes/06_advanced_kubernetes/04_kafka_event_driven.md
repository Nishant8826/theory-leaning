# Kafka Event Driven

## Why This Exists
In traditional microservices, Service A calls Service B directly via HTTP. If Service B is offline, Service A crashes. This tight coupling makes scaling hard. Event-Driven Architecture uses a message broker (Apache Kafka) so services can simply announce events ("User Signed Up") without caring who is listening or if they are currently online.

## Real World Analogy
Think of a **Notice Board in a Town Square**. 
Traditional HTTP is like calling someone on the phone. If they don't answer, communication fails.
Kafka is like pinning a message to the town's Notice Board. You pin it and walk away immediately. Later, the Bakery, the Bank, and the Post Office can walk by the board, read the message, and take action whenever they are ready. If the Bakery is closed today, they will just read the board tomorrow.

## Core Concepts
*   **Producer:** The app that creates events (pins messages to the board).
*   **Consumer:** The app that reads events.
*   **Topic:** A specific category/folder for events (e.g., `orders`, `user-logins`).
*   **Partition:** Splitting a topic into multiple pieces so many consumers can read simultaneously.
*   **Offset:** A bookmark. The consumer remembers exactly which message it read last.

## Architecture / Flow
1. User clicks "Buy" on the website.
2. The **Order Service (Producer)** creates an `OrderCreated` JSON event and sends it to the Kafka `orders` topic.
3. The Order Service immediately replies "Success" to the user.
4. The **Payment Service (Consumer)** reads the event from Kafka and charges the credit card.
5. The **Inventory Service (Consumer)** also reads the same event and deducts the item from stock.

## Practical Commands
*   *(Usually run via scripts inside the Kafka container)*
*   `kafka-topics.sh --create --topic orders --bootstrap-server localhost:9092`
*   `kafka-console-producer.sh --topic orders --bootstrap-server localhost:9092`
*   `kafka-console-consumer.sh --topic orders --from-beginning --bootstrap-server localhost:9092`

## Hands-On Exercise
Run Kafka and Zookeeper using Docker Compose. Create a topic called `greetings`. Open two terminal windows. In terminal 1, run the console producer and type messages. In terminal 2, run the console consumer and watch the messages appear instantly.

## Mini Project
**"The Decoupled Database"**
Build two simple Node.js microservices. Service A (Producer) exposes an API that accepts user registrations and pushes them to Kafka. Service B (Consumer) connects to Kafka, reads the registrations, and saves them to MongoDB. Take Service B offline, register 5 users in Service A, then turn Service B back on. Watch it process the backlog!

## Real Production Usage
Kafka handles massive data pipelines. Uber uses it to track millions of driver locations per second. Netflix uses it to track every time you pause or click a video. Banks use it to process thousands of transactions per second asynchronously.

## Common Mistakes
*   **Treating Kafka like a Database:** Kafka is a streaming log; data is meant to be in motion. It's not designed for complex SQL queries to find "that one order from last year".
*   **Consumer Group Mess-ups:** If you spin up 5 replicas of your Payment Service, you must put them in the same "Consumer Group". Otherwise, all 5 replicas will process the *exact same order* and charge the customer's credit card 5 times!

## Debugging Guide
*   **Consumer not getting messages?** Check the "Offset". The consumer might be looking at the very end of the log waiting for *new* messages, while the producer already sent the messages an hour ago. Use the `--from-beginning` flag to test.

## Best Practices
*   **Schema Registry:** Always use tools like Avro or Protobuf for message schemas. If Service A suddenly changes the JSON structure of a message, it will crash Service B. A Schema Registry prevents breaking changes from being published.

## Interview Questions
*   **Q: How does Kafka achieve such high throughput compared to traditional message queues like RabbitMQ?**
    *   *A: Kafka uses sequential disk I/O, appending messages to a log file rather than managing complex routing trees in memory. It also uses Partitions to allow massive parallel processing across multiple servers.*

## Summary
Kafka decouples microservices in both time and space, shifting architectures from synchronous "Request/Response" to asynchronous "Event-Driven", enabling systems to handle planetary-scale data loads without crashing.

---
Prev: [03_gitops.md](./03_gitops.md) | Index: [Index](../00_index.md) | Next: [05_multi_cluster.md](./05_multi_cluster.md)
