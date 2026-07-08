# Microservices Networking

> 📌 **File:** 18_Microservices_Networking.md | **Level:** Full-Stack Dev → Networking Expert

---

## What is it?

Microservices architecture splits your monolith into independent services that communicate over the network. Instead of one Express app doing everything, you have separate services for users, orders, products, notifications — each with its own database. The networking between these services is the critical challenge.

---

## Map it to MY STACK (CRITICAL)

```
Monolith:
  Express App (:3000)
  ├── /api/users     → User logic
  ├── /api/orders    → Order logic
  └── All share ONE MongoDB

Microservices:
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ User Service │  │ Order Service│  │Product Service│
│ :3001        │  │ :3002        │  │ :3003        │
│ PostgreSQL   │  │ MongoDB      │  │ MongoDB      │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                 │
       └────── Internal Network (HTTP/gRPC/Message Queue) ──┘
```

### Communication Patterns

```
┌──────────────────────────────────────────────────────────────────────┐
│  Pattern           │ Protocol    │ When to Use                     │
├────────────────────┼─────────────┼─────────────────────────────────┤
│  Synchronous REST  │ HTTP/JSON   │ Simple service-to-service calls │
│  Synchronous gRPC  │ HTTP/2 +    │ High-performance internal calls │
│                    │ Protobuf    │                                 │
│  Async Messages    │ SQS/SNS/    │ Fire-and-forget operations      │
│  (Queue)           │ RabbitMQ    │                                 │
│  Async Events      │ SNS/Kafka/  │ Event-driven architecture       │
│  (Pub/Sub)         │ EventBridge │                                 │
└────────────────────┴─────────────┴─────────────────────────────────┘
```

---

## Synchronous Communication (HTTP)

```javascript
// Order Service calling User Service
const axios = require('axios');

const USER_SERVICE = process.env.USER_SERVICE_URL; // http://user-service:3001

async function getUserById(userId, traceId) {
  try {
    const response = await axios.get(`${USER_SERVICE}/users/${userId}`, {
      timeout: 5000,
      headers: {
        'X-Request-ID': traceId,
        'X-Caller-Service': 'order-service'
      }
    });
    return response.data;
  } catch (err) {
    throw err;
  }
}
```

---

## Asynchronous Communication (Message Queues)

```javascript
// SQS: Send message to queue
const { SQSClient, SendMessageCommand } = require('@aws-sdk/client-sqs');
const sqs = new SQSClient({ region: 'us-east-1' });

async function publishEvent(eventType, data) {
  await sqs.send(new SendMessageCommand({
    QueueUrl: process.env.EVENTS_QUEUE_URL,
    MessageBody: JSON.stringify({
      eventType,
      data,
      timestamp: new Date().toISOString()
    })
  }));
}
```

---

## Visual Diagram — Event-Driven Microservices

```
User Request ───► API Gateway ───► Order Service
                                     │
                                 SNS Topic (order-events)
                                 ├──► SQS (notification) ──► Notification Svc
                                 ├──► SQS (inventory) ──► Inventory Svc
                                 └──► SQS (analytics) ──► Analytics Svc
```

#### Diagram Explanation (The Restaurant Kitchen)
Think of an Event-Driven Microservice architecture exactly like a high-end restaurant kitchen:
- **The Waiter (Order Service):** Takes your order, writes it on a ticket, and stabs the ticket onto the spinning metal wheel above the kitchen counter (`SNS Topic`). The waiter then immediately walks away to help other tables.
- **The Chefs (Subscribers):** Down the line, the Grill Chef (`Inventory Service`), the Fry Chef (`Payment Service`), and the Expediter (`Analytics Service`) all see that a new ticket was placed on the wheel. They all grab a copy of the order ticket into their personal workflow stack (`SQS`) and start working simultaneously and independently.

---

## The Network Challenges

### Service Discovery
- **DNS-based:** AWS Cloud Map private DNS resolves service names to IPs.
- **Container platform:** ECS / Kubernetes handles discovery internally.

### Circuit Breaker Pattern

```javascript
class CircuitBreaker {
  constructor(action, failureThreshold = 5, resetTimeout = 30000) {
    this.action = action;
    this.failureThreshold = failureThreshold;
    this.resetTimeout = resetTimeout;
    this.state = 'CLOSED'; // CLOSED, OPEN, HALF_OPEN
    this.failures = 0;
    this.lastFailureTime = null;
  }
  
  async execute(...args) {
    if (this.state === 'OPEN') {
      if (Date.now() - this.lastFailureTime > this.resetTimeout) {
        this.state = 'HALF_OPEN';
      } else {
        throw new Error('Circuit open');
      }
    }
    
    try {
      const result = await this.action(...args);
      this.failures = 0;
      this.state = 'CLOSED';
      return result;
    } catch (err) {
      this.failures++;
      this.lastFailureTime = Date.now();
      if (this.failures >= this.failureThreshold) this.state = 'OPEN';
      throw err;
    }
  }
}
```

---

## Practice Exercises

### Exercise 1: Custom Gateway with Express
Build a custom API gateway with Express that proxies to 2 microservices with shared authentication and request logging.

### Exercise 2: Event-Driven Simulation
Write two simple Node processes. Process A writes messages to a local Redis Pub/Sub channel. Process B listens and processes them. Simulate network failures by killing Process B and checking how messages accumulate.

---

## Interview Q&A

**Q1: How do microservices communicate?**
> Synchronous: REST (HTTP/JSON) for simple calls, gRPC (HTTP/2 + Protobuf) for high-performance. Asynchronous: message queues (SQS, RabbitMQ) for fire-and-forget, event buses (SNS, Kafka) for pub/sub. Use sync for queries needing immediate response; async for background processing.

**Q2: What is the circuit breaker pattern?**
> Wraps service calls with failure detection. After N consecutive failures, the circuit "opens" — subsequent calls fail fast without attempting the network call. After a timeout, one test request is allowed (half-open). If it succeeds, circuit closes. Prevents cascade failures across services.

**Q3: How do you handle data consistency across microservices?**
> Eventual consistency with events: Service A publishes event, Service B reacts and updates its own database. Saga pattern: a sequence of local transactions coordinated by events. Avoid distributed transactions (2PC).

**Q4: What is service discovery and why is it needed?**
> Services need to find each other's network addresses. Static config breaks when services scale/restart. Solutions: DNS-based (AWS Cloud Map), load balancer (ALB routing), container platform DNS (ECS/K8s), or service mesh (sidecar proxy handles routing).

**Q5: When should you NOT use microservices?**
> Small teams (< 10 people), simple domains, early-stage startups, tight deadlines. The networking overhead (latency, retries, tracing, discovery) and operational complexity (more deployments, more monitoring, more failure modes) outweigh benefits for small projects.

---

Prev : [17 API Gateways](./17_API_Gateways.md) | Index: [00 Index](./00_Index.md) | Next : [19 Containers And Networking](./19_Containers_And_Networking.md)
