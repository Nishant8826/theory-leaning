# Microservices Networking

> 📌 **File:** 17_Microservices_Networking.md | **Level:** Full-Stack Dev → Networking Expert

---

## What is it?

Microservices architecture splits your monolith into independent services that communicate over the network. Instead of one Express app doing everything, you have separate services for users, orders, products, notifications — each with its own database. The networking between these services is the critical challenge.

---

## Map it to MY STACK (CRITICAL)

```
Monolith (what you probably have now):
┌─────────────────────────────────────┐
│  Express App (:3000)                │
│  ├── /api/users     → User logic   │
│  ├── /api/orders    → Order logic  │
│  ├── /api/products  → Product logic│
│  ├── /api/payments  → Payment logic│
│  └── All share ONE MongoDB         │
└─────────────────────────────────────┘

Microservices:
┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ User Service │  │ Order Service│  │Product Service│  │Payment Service│
│ :3001        │  │ :3002        │  │ :3003        │  │ :3004        │
│ PostgreSQL   │  │ MongoDB      │  │ MongoDB      │  │ PostgreSQL   │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                 │                 │
       └────── Internal Network (HTTP/gRPC/Message Queue) ──┘
```

### Communication Patterns

```
┌──────────────────────────────────────────────────────────────────────┐
│  Pattern           │ Protocol    │ When to Use                     │
├────────────────────┼─────────────┼─────────────────────────────────┤
│  Synchronous REST  │ HTTP/JSON   │ Simple service-to-service calls │
│                    │             │ CRUD operations, data fetching  │
│                    │             │                                 │
│  Synchronous gRPC  │ HTTP/2 +    │ High-performance internal calls │
│                    │ Protobuf    │ Low latency, streaming          │
│                    │             │                                 │
│  Async Messages    │ SQS/SNS/   │ Fire-and-forget operations      │
│  (Queue)           │ RabbitMQ    │ Order processing, email sending │
│                    │             │                                 │
│  Async Events      │ SNS/Kafka/ │ Event-driven architecture       │
│  (Pub/Sub)         │ EventBridge│ "Order created" → notify, update│
│                    │             │ inventory, send email            │
└────────────────────┴─────────────┴─────────────────────────────────┘
```

---

## Synchronous Communication (HTTP)

```javascript
// ──── Order Service calling User Service ────
const axios = require('axios');

// Service discovery: How does Order Service find User Service?

// Option 1: Hardcoded URL (simplest, for dev)
const USER_SERVICE = 'http://localhost:3001';

// Option 2: Environment variable (for EC2/containers)
const USER_SERVICE = process.env.USER_SERVICE_URL; // http://user-service:3001

// Option 3: AWS Cloud Map (service discovery)
const USER_SERVICE = 'http://user-service.myapp.local'; // Private DNS

// Option 4: ALB with path routing (all services behind one ALB)
const API_BASE = 'http://internal-alb.us-east-1.elb.amazonaws.com';

// ──── Service-to-service call with retry ────
async function getUserById(userId) {
  const maxRetries = 3;
  
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      const response = await axios.get(`${USER_SERVICE}/users/${userId}`, {
        timeout: 5000,  // 5 second timeout
        headers: {
          'X-Request-ID': req.headers['x-request-id'],  // Propagate trace ID
          'X-Caller-Service': 'order-service'
        }
      });
      return response.data;
    } catch (err) {
      if (attempt === maxRetries) throw err;
      if (err.response?.status >= 500) {
        // Retry on 5xx (server error)
        await new Promise(r => setTimeout(r, 1000 * attempt)); // Backoff
        continue;
      }
      throw err; // Don't retry on 4xx (client error)
    }
  }
}

// ──── Order creation with cross-service calls ────
app.post('/orders', async (req, res) => {
  const { userId, productIds, shippingAddress } = req.body;
  
  try {
    // Call User Service (synchronous — need user data now)
    const user = await getUserById(userId);
    
    // Call Product Service (synchronous — need prices now)  
    const products = await axios.post(`${PRODUCT_SERVICE}/products/batch`, {
      ids: productIds
    }, { timeout: 5000 });
    
    // Create order locally
    const order = await Order.create({
      userId, user: { name: user.name, email: user.email },
      items: products.data, shippingAddress,
      status: 'pending'
    });
    
    // Publish event (asynchronous — don't need to wait)
    await publishEvent('order.created', {
      orderId: order._id, userId, total: order.total
    });
    
    res.status(201).json(order);
  } catch (err) {
    if (err.response?.status === 404) {
      return res.status(400).json({ error: 'User or product not found' });
    }
    res.status(500).json({ error: 'Failed to create order' });
  }
});
```

---

## Asynchronous Communication (Message Queues)

```javascript
// ──── SQS: Send message to queue ────
const { SQSClient, SendMessageCommand } = require('@aws-sdk/client-sqs');
const sqs = new SQSClient({ region: 'us-east-1' });

async function publishEvent(eventType, data) {
  await sqs.send(new SendMessageCommand({
    QueueUrl: process.env.EVENTS_QUEUE_URL,
    MessageBody: JSON.stringify({
      eventType,
      data,
      timestamp: new Date().toISOString(),
      source: 'order-service'
    }),
    MessageGroupId: data.orderId  // FIFO: ensures order of messages per order
  }));
}

// Order Service publishes:
await publishEvent('order.created', { orderId: '123', userId: 'abc', total: 99.99 });

// ──── SQS: Consume messages (separate services) ────

// Notification Service: Listens for order events → sends email
async function processNotificationQueue() {
  while (true) {
    const { Messages } = await sqs.send(new ReceiveMessageCommand({
      QueueUrl: process.env.NOTIFICATION_QUEUE_URL,
      MaxNumberOfMessages: 10,
      WaitTimeSeconds: 20  // Long polling (cost-efficient)
    }));
    
    for (const msg of (Messages || [])) {
      const event = JSON.parse(msg.Body);
      
      if (event.eventType === 'order.created') {
        await sendOrderConfirmationEmail(event.data.userId, event.data.orderId);
      }
      
      // Delete message after processing
      await sqs.send(new DeleteMessageCommand({
        QueueUrl: process.env.NOTIFICATION_QUEUE_URL,
        ReceiptHandle: msg.ReceiptHandle
      }));
    }
  }
}

// Inventory Service: Listens for order events → decrements stock
// Payment Service: Listens for order events → charges customer
// Analytics Service: Listens for order events → updates dashboard
```

---

## Visual Diagram — Event-Driven Microservices

```
                     ┌──────────────┐
    User Request ───►│ API Gateway  │
                     └──────┬───────┘
                            │
                     ┌──────▼───────┐
                     │ Order Service│ ← Creates order
                     └──────┬───────┘
                            │
                     ┌──────▼───────┐
                     │  SNS Topic   │ ← Publishes "order.created"
                     │ order-events │
                     └──┬───┬───┬──┘
                        │   │   │
           ┌────────────┘   │   └────────────┐
           │                │                │
    ┌──────▼──────┐  ┌─────▼──────┐  ┌──────▼───────┐
    │ SQS:        │  │ SQS:       │  │ SQS:         │
    │ notification│  │ inventory  │  │ analytics    │
    └──────┬──────┘  └─────┬──────┘  └──────┬───────┘
           │               │                │
    ┌──────▼──────┐  ┌─────▼──────┐  ┌──────▼───────┐
    │ Notification│  │ Inventory  │  │ Analytics    │
    │ Service     │  │ Service    │  │ Service      │
    │ (sends email)│ │ (- stock) │  │ (dashboard)  │
    └─────────────┘  └────────────┘  └──────────────┘

Benefits:
  ✅ Services are decoupled (Order doesn't know about Notifications)
  ✅ Add new consumers without changing Order Service
  ✅ If Notification Service is down, messages queue up (no data loss)
  ✅ Each service scales independently
```

---

## The Network Challenges

### Service Discovery

```
Problem: How does Service A find Service B's IP/port?

┌──────────────────────────────────────────────────────────────────┐
│  Method              │ How it Works          │ AWS Service       │
├──────────────────────┼───────────────────────┼───────────────────┤
│  Hardcoded URLs      │ Config files / env    │ Environment vars  │
│  DNS-based           │ DNS resolves service  │ Cloud Map, Route 53│
│  Load balancer       │ All services behind LB│ ALB path routing  │
│  Service mesh        │ Sidecar proxy handles │ App Mesh          │
│  Container platform  │ Built-in DNS          │ ECS Service Disc. │
└──────────────────────┴───────────────────────┴───────────────────┘

Simplest for your stack:
  Option A: ALB with path routing (all services behind one ALB)
  Option B: One ALB per service (more isolation, more cost)
  Option C: ECS service discovery (if using containers)
```

### Circuit Breaker Pattern

```javascript
// Prevent cascade failures when a downstream service is down
class CircuitBreaker {
  constructor(options = {}) {
    this.failureThreshold = options.failureThreshold || 5;
    this.resetTimeout = options.resetTimeout || 30000;
    this.state = 'CLOSED';    // CLOSED = normal, OPEN = blocked, HALF_OPEN = testing
    this.failureCount = 0;
    this.lastFailureTime = null;
  }
  
  async call(fn) {
    if (this.state === 'OPEN') {
      if (Date.now() - this.lastFailureTime > this.resetTimeout) {
        this.state = 'HALF_OPEN'; // Allow one test request
      } else {
        throw new Error('Circuit breaker is OPEN — service unavailable');
      }
    }
    
    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (err) {
      this.onFailure();
      throw err;
    }
  }
  
  onSuccess() {
    this.failureCount = 0;
    this.state = 'CLOSED';
  }
  
  onFailure() {
    this.failureCount++;
    this.lastFailureTime = Date.now();
    if (this.failureCount >= this.failureThreshold) {
      this.state = 'OPEN';
      console.warn(`Circuit breaker OPEN after ${this.failureCount} failures`);
    }
  }
}

// Usage
const userServiceBreaker = new CircuitBreaker({ failureThreshold: 5, resetTimeout: 30000 });

async function getUserSafely(userId) {
  return userServiceBreaker.call(() => 
    axios.get(`${USER_SERVICE}/users/${userId}`, { timeout: 5000 })
  );
}
```

### Distributed Tracing

```javascript
// Track a request across multiple services
const crypto = require('crypto');

// Middleware: Generate or propagate trace ID
app.use((req, res, next) => {
  req.traceId = req.headers['x-request-id'] || crypto.randomUUID();
  req.spanId = crypto.randomUUID();
  
  res.set('X-Request-ID', req.traceId);
  
  console.log(JSON.stringify({
    traceId: req.traceId,
    spanId: req.spanId,
    service: 'order-service',
    method: req.method,
    path: req.path,
    timestamp: new Date().toISOString()
  }));
  
  next();
});

// When calling other services, propagate the trace ID
async function callService(url, traceId) {
  return axios.get(url, {
    headers: { 'X-Request-ID': traceId }
  });
}
```

---

## Monolith vs Microservices — Decision

```
┌──────────────────────────────────────────────────────────────────┐
│  Start with a monolith. Extract microservices when needed.      │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Keep monolith when:                                            │
│  ✅ Small team (< 10 developers)                                │
│  ✅ Simple domain                                                │
│  ✅ Tight deadlines                                              │
│  ✅ Single deployment target                                     │
│                                                                  │
│  Consider microservices when:                                    │
│  ✅ Large team (independent feature teams)                      │
│  ✅ Different scaling needs (API heavy vs compute heavy)        │
│  ✅ Different tech stacks needed (Python ML + Node.js API)     │
│  ✅ Independent deployment cycles                                │
│                                                                  │
│  The networking overhead of microservices is SIGNIFICANT:       │
│  - Every function call becomes a network call (+latency)        │
│  - Need service discovery, retries, circuit breakers            │
│  - Distributed tracing, centralized logging                      │
│  - Data consistency across services (no shared DB)              │
│  - More infrastructure to manage                                 │
│                                                                  │
│  "You must be THIS tall to use microservices"                    │
│  — most teams are better off with a well-structured monolith    │
└──────────────────────────────────────────────────────────────────┘
```

---

## Common Mistakes

### ❌ Synchronous Chain of Calls

```
User → API → Order Service → Product Service → User Service → Payment Service
Each call: 50ms network + 50ms processing = 100ms
Total: 400ms just for network overhead!

✅ Parallel calls where possible
✅ Async events for non-blocking operations
✅ Embed needed data to avoid cross-service calls
```

### ❌ Shared Database Across Services

```
❌ Order Service and Product Service both write to the same MongoDB
   → Tight coupling (can't change schema independently)
   → Scaling one affects the other

✅ Each service owns its database
   Order Service → orders_db (MongoDB)
   Product Service → products_db (MongoDB)
   Need product data in order? Call Product Service API or cache locally.
```

---

## Interview Q&A

**Q1: How do microservices communicate?**
> Synchronous: REST (HTTP/JSON) for simple calls, gRPC (HTTP/2 + Protobuf) for high-performance. Asynchronous: message queues (SQS, RabbitMQ) for fire-and-forget, event buses (SNS, Kafka) for pub/sub. Use sync for queries needing immediate response; async for background processing.

**Q2: What is the circuit breaker pattern?**
> Wraps service calls with failure detection. After N consecutive failures, the circuit "opens" — subsequent calls fail fast without attempting the network call. After a timeout, one test request is allowed (half-open). If it succeeds, circuit closes. Prevents cascade failures across services.

**Q3: How do you handle data consistency across microservices?**
> Eventual consistency with events: Service A publishes event, Service B reacts and updates its own database. Saga pattern: a sequence of local transactions coordinated by events. Avoid distributed transactions (2PC) — they're slow and fragile. Embrace eventual consistency.

**Q4: What is service discovery and why is it needed?**
> Services need to find each other's network addresses. Static config breaks when services scale/restart. Solutions: DNS-based (AWS Cloud Map), load balancer (ALB routing), container platform DNS (ECS/K8s), or service mesh (sidecar proxy handles routing).

**Q5: When should you NOT use microservices?**
> Small teams (< 10 people), simple domains, early-stage startups, tight deadlines. The networking overhead (latency, retries, tracing, discovery) and operational complexity (more deployments, more monitoring, more failure modes) outweigh benefits for small projects.
