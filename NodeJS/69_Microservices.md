# Microservices

As applications grow, maintaining a single, massive codebase (a Monolith) becomes difficult. Microservices partition applications into small, independent services organized around business capabilities. However, microservices introduce network complexity, latency, and data consistency challenges. Understanding microservices architecture allows you to design scalable, distributed systems.

### Monolith vs. Microservices
* **Monolith**: A single, unified application containing all business modules. It shares a single database, runs in a single process space, and is easy to develop and deploy initially. However, it scales poorly as teams grow, and a single crash takes the entire system offline.
* **Microservices**: A network of small, independent services. Each service manages its own database, deploys independently, and communicates with other services over network protocols. This enables team autonomy and allows services to scale independently, but increases network complexity.

### Service Communication Protocols
1. **Synchronous (Request-Response)**:
   * **HTTP/REST**: Simple, stateless communication. However, it creates tight coupling and increases latency when chaining calls across services.
   * **gRPC**: A high-performance RPC framework built on HTTP/2. It uses **Protocol Buffers** (binary serialization) instead of text JSON, reducing payload sizes and latency.
2. **Asynchronous (Message-Driven)**:
   * **Message Brokers (e.g. RabbitMQ, Kafka)**: Services communicate by publishing and consuming events. This decouples services, preventing slow downstream services from blocking upstream request handlers.

## Deep Dive

### Distributed Transactions: The Saga Pattern
In a monolithic application, you ensure data consistency using database transactions (`BEGIN` / `COMMIT`). In microservices, each service has its own database, meaning you cannot run single database transactions across service boundaries.
* **Two-Phase Commit (2PC)**: A protocol where a central coordinator asks all databases to prepare to write, and then commits only if all databases agree.
  * *Drawback*: It blocks database resources during the process, reducing performance and scaling poorly.
* **The Saga Pattern**: A design pattern that manages distributed transactions as a sequence of local database transactions:
  * Each service executes its own local transaction and publishes an event.
  * The next service listens to the event and executes its local transaction.
  * If any step fails, the system executes **Compensating Transactions** (rollback actions) in reverse order to undo the changes and maintain consistency.

## Visual Explanation

### The Saga Pattern: Distributed Rollback Lifecycle
```text
Successful Order Flow:
[ Order Service ] ── Creates Order (Pending) ──> [ Payment Service ] ── Debits Balance ──> [ Completed ]

Failed Payment Rollback Flow:
[ Order Service ] ── Creates Order (Pending) ──> [ Payment Service ] (Fails: Insufficient Funds!)
                                                        │
                                                        ▼ (Publishes failure event)
[ Order Service ] <── Run Compensating: Cancel Order <──┘
  - Reverts order status to 'Cancelled', restoring database consistency without blocking locks.
```

## Real-World Example
Consider an e-commerce platform. When a user buys a product, the request hits the **API Gateway**. The gateway validates the JWT token, maps the request, routes it to the Order Service to create a pending order, and publishes a `create-order` event. The Payment Service consumes the event to charge the card, and the Inventory Service updates stock levels asynchronously, keeping the checkout fast.

## Code Examples

### Implementing a Basic Saga Coordinator Router

```javascript
// saga-coordinator.js
const express = require('express');
const axios = require('axios');
const app = express();
app.use(express.json());

// Mock Service Host URLs
const ORDER_SERVICE = 'http://localhost:3001';
const PAYMENT_SERVICE = 'http://localhost:3002';

// 1. Saga Coordinator Route Handler
app.post('/api/checkout', async (req, res, next) => {
  const { userId, items, amount } = req.body;
  
  let createdOrderId = null;

  try {
    // Step 1: Execute Local Transaction on Order Service
    console.log('[SAGA] Creating pending order...');
    const orderResponse = await axios.post(`${ORDER_SERVICE}/orders`, { userId, items });
    createdOrderId = orderResponse.data.id;

    // Step 2: Execute Local Transaction on Payment Service
    console.log('[SAGA] Executing payment charge...');
    await axios.post(`${PAYMENT_SERVICE}/payments`, { orderId: createdOrderId, amount });

    // Step 3: Success, confirm order status
    console.log('[SAGA] Transaction succeeded. Confirming order...');
    await axios.put(`${ORDER_SERVICE}/orders/${createdOrderId}`, { status: 'confirmed' });

    res.status(200).json({ status: 'success', orderId: createdOrderId });

  } catch (err) {
    console.error('[SAGA ERROR] Step failed. Executing compensating rollback transactions...');
    
    // Compensating Transaction: Roll back the created order if it exists
    if (createdOrderId) {
      try {
        await axios.put(`${ORDER_SERVICE}/orders/${createdOrderId}`, { status: 'cancelled' });
        console.log(`[SAGA ROLLBACK] Order ${createdOrderId} successfully cancelled.`);
      } catch (rollbackErr) {
        console.error('[CRITICAL] Compensating transaction failed:', rollbackErr.message);
        // Alert operations team for manual reconciliation
      }
    }

    res.status(500).json({
      error: 'Checkout transaction failed. Changes rolled back.',
      reason: err.message
    });
  }
});

app.listen(3000, () => console.log('Saga Gateway Coordinator running on port 3000'));
```

## Best Practices
* **Use API Gateways**: Implement an API Gateway (like Kong or Nginx) to handle routing, authentication, and rate-limiting at the cluster boundary, keeping microservices lightweight.
* **Design Idempotent Event Handlers**: Ensure all message consumers are idempotent. If network issues trigger duplicate event delivery, consumers must handle the duplicate event without creating duplicate records.
* **Enforce Database per Service**: Never allow services to query each other's databases directly. Services must communicate strictly over APIs or message queues to preserve service autonomy.

## Interview Questions

**Q:** What is the difference between a monolithic and a microservices architecture?

> **Answer:**
> A monolith is a single application where all modules run in a single process and share a database. Microservices partition the application into small, independent services, where each service runs in its own process, manages its own database, and communicates over network protocols.

**Q:** What is the role of an API Gateway in a microservices architecture?

> **Answer:**
> An API Gateway acts as the entry point for all client requests. It handles routing to downstream microservices, aggregates responses, terminates SSL, and enforces cross-cutting concerns like authentication, rate-limiting, and CORS, protecting internal services.

**Q:** What is the Saga Pattern, and how does it manage data consistency in microservices compared to a Two-Phase Commit (2PC)?

> **Answer:**
> The Saga Pattern manages distributed transactions as a sequence of local transactions. Each service executes its local transaction and publishes an event to trigger the next service. If a step fails, the system executes compensating transactions (rollbacks) in reverse order to restore consistency.
> It differs from 2PC (which uses a coordinator to lock all databases before committing) because it does not lock database rows, improving performance and scalability.

**Q:** How would you handle a failure in a compensating rollback transaction during a Saga execution? Discuss monitoring, dead-letter queues, and manual reconciliation workflows.

> **Answer:**
> 

**Q:** Failure Analysis

> **Answer:**
> 

**Q:** Architecture Strategy

> **Answer:**
> 1. **Retry Mechanism**: Configure the saga coordinator or message queue (e.g. BullMQ) to retry the compensating transaction using exponential backoff.
> 2. **Dead Letter Queue (DLQ)**: If the compensating transaction fails after maximum retries (e.g. 5 attempts), route the failed transaction context payload to a Dead Letter Queue (DLQ).
> 3. **Monitoring and Alerts**: Configure alerts (e.g., in Prometheus or PagerDuty) to notify the operations team immediately when a job enters the DLQ.
> 4. **Manual Reconciliation Dashboard**: Build an administrative tool that displays failed transactions in the DLQ, allowing operators to audit records, manually fix database consistency, and clear the queue safely.

---
Previous : [68_Swagger_OpenAPI.md](68_Swagger_OpenAPI.md) | Index : [00_index.md](00_index.md) | Next : [70_Event_Driven_Architecture.md](70_Event_Driven_Architecture.md)
