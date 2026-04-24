# 📌 Microservices

## 🧠 Concept Explanation (Story Format)

Netflix in 2008 was a DVD-shipping monolith. One big Rails app for everything. Then one database outage took down ALL Netflix — including the unrelated movie recommendation feature.

They spent 7 years breaking it into microservices. Now:
- An outage in the "Search" service doesn't break "Play Video"
- The "Recommendation" team can deploy without coordinating with the "Billing" team
- "Streaming" can be written in Java while "Search" uses Python

Microservices = splitting your app into small, independent, single-purpose services that communicate via APIs or events.

Your Node.js + React stack is perfect for microservices. Each service is a separate Node.js app.

---

## 🏗️ Basic Design (Monolith First)

```
Single Node.js Application:
├── routes/auth.js
├── routes/users.js
├── routes/posts.js
├── routes/comments.js
├── routes/notifications.js
├── routes/payments.js
└── Single MongoDB + PostgreSQL

All in one process. Simple. Easy to develop.
But as team grows → harder to deploy without breaking things.
```

---

## ⚡ Optimized Design (Microservices)

```
React/Next.js Frontend
         ↓
[AWS API Gateway] ← Single entry point
         ↓ routes to:
┌─────────────────────────────────────────┐
│                                         │
[Auth Service]    [User Service]     [Post Service]
Port 3001         Port 3002          Port 3003
MongoDB(users)    PostgreSQL          MongoDB(posts)
                                         │
[Comment Service] [Notification Svc] [Payment Service]
Port 3004         Port 3005          Port 3006
MongoDB           Redis + FCM        PostgreSQL + Stripe
                                         │
[Search Service]  [Media Service]    [Feed Service]
Port 3007         Port 3008          Port 3009
Elasticsearch     S3 + Lambda        Redis + MongoDB

All services communicate via:
- REST APIs (synchronous)
- Events via SNS/SQS (asynchronous)
```

---

## 🔍 Key Components

### Service Communication Patterns

**Synchronous (REST/gRPC):**
```javascript
// User Service calling Auth Service to validate token
// This is synchronous — waits for response

const axios = require('axios');

async function validateToken(token) {
  try {
    const response = await axios.get(`${process.env.AUTH_SERVICE_URL}/validate`, {
      headers: { Authorization: `Bearer ${token}` },
      timeout: 2000  // Don't wait more than 2 seconds!
    });
    return response.data.user;
  } catch (error) {
    if (error.code === 'ECONNABORTED') {
      throw new Error('Auth service timeout');
    }
    throw error;
  }
}
```

**Asynchronous (Events):**
```javascript
// Post Service emitting event (doesn't wait for consumers)
const sns = new AWS.SNS();

async function createPost(userId, content) {
  const post = await db.insertPost({ userId, content });
  
  // Emit event — don't wait for who handles it
  await sns.publish({
    TopicArn: process.env.POST_CREATED_TOPIC,
    Message: JSON.stringify({ postId: post.id, userId, timestamp: new Date() })
  }).promise();
  
  return post;
}

// Feed Service handles the event (separate microservice)
// Notification Service handles the event (separate microservice)
// Analytics Service handles the event (separate microservice)
```

### API Gateway Pattern

```javascript
// AWS API Gateway routes to different services
// Routes configured in AWS console or terraform:

// /auth/*    → Auth Service Lambda or EC2
// /users/*   → User Service
// /posts/*   → Post Service
// /search/*  → Search Service
// /payments/*→ Payment Service

// In Node.js, your service doesn't know about the gateway
// It just handles requests:

// auth-service/index.js
const express = require('express');
const app = express();

app.post('/register', registerHandler);
app.post('/login', loginHandler);
app.get('/validate', validateTokenHandler);

app.listen(3001);
```

### Service Discovery

```javascript
// How does Post Service know where User Service is?

// Option 1: Environment variables (simple, works in Docker/ECS)
// POST_SERVICE_URL=http://post-service:3003
// USER_SERVICE_URL=http://user-service:3002

// Option 2: AWS Service Discovery
// Each service registers with AWS Cloud Map
// Other services query Cloud Map to find it

// Option 3: API Gateway as proxy
// Frontend always calls API Gateway
// API Gateway knows where each service is
```

### Circuit Breaker Pattern

```javascript
// Prevent cascade failures when a service is down
const CircuitBreaker = require('opossum');

// Wrap service calls in circuit breaker
const authServiceCall = async (token) => {
  return axios.get(`${AUTH_SERVICE_URL}/validate`, {
    headers: { Authorization: `Bearer ${token}` }
  });
};

const breaker = new CircuitBreaker(authServiceCall, {
  timeout: 3000,         // 3 second timeout
  errorThresholdPercentage: 50,  // Open if 50% of calls fail
  resetTimeout: 30000    // Try again after 30 seconds
});

breaker.on('open', () => {
  console.error('Auth service circuit OPEN — too many failures!');
  // Alert your on-call team
});

breaker.on('halfOpen', () => {
  console.log('Auth service circuit HALF-OPEN — testing...');
});

breaker.on('close', () => {
  console.log('Auth service circuit CLOSED — back to normal');
});

// Use in your middleware
app.use(async (req, res, next) => {
  try {
    req.user = await breaker.fire(req.headers.authorization);
    next();
  } catch (error) {
    if (breaker.opened) {
      // Fallback: maybe use cached user data from Redis
      req.user = await getCachedUser(req.headers.authorization);
      if (req.user) return next();
    }
    res.status(503).json({ error: 'Authentication service unavailable' });
  }
});
```

### Health Checks and Service Mesh

```javascript
// Every microservice MUST have health checks
app.get('/health', async (req, res) => {
  const health = {
    status: 'healthy',
    service: 'post-service',
    version: process.env.SERVICE_VERSION,
    uptime: process.uptime(),
    dependencies: {}
  };
  
  // Check dependencies
  try {
    await db.query('SELECT 1');
    health.dependencies.database = 'healthy';
  } catch (e) {
    health.dependencies.database = 'unhealthy';
    health.status = 'degraded';
  }
  
  try {
    await redis.ping();
    health.dependencies.redis = 'healthy';
  } catch (e) {
    health.dependencies.redis = 'unhealthy';
  }
  
  const statusCode = health.status === 'healthy' ? 200 : 503;
  res.status(statusCode).json(health);
});
```

---

## ⚖️ Trade-offs

| Microservices | Monolith |
|--------------|---------|
| Independent scaling | Scale entire app |
| Independent deployment | Deploy all at once |
| Technology flexibility | One stack |
| Team autonomy | Easier cross-team coord |
| Network latency between services | In-process calls (fast) |
| Complex debugging (distributed) | Simple debugging |
| Complex testing | Simple testing |
| More infrastructure | Less infrastructure |

---

## 📊 Scalability Discussion

### Deployment with Docker + AWS ECS

```dockerfile
# Each microservice has its own Dockerfile
# post-service/Dockerfile

FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
EXPOSE 3003
CMD ["node", "index.js"]
```

```yaml
# AWS ECS Task Definition (each service is a task)
# post-service-task.json

{
  "family": "post-service",
  "containerDefinitions": [{
    "name": "post-service",
    "image": "123456789.dkr.ecr.us-east-1.amazonaws.com/post-service:latest",
    "cpu": 256,
    "memory": 512,
    "portMappings": [{ "containerPort": 3003, "hostPort": 0 }],
    "environment": [
      { "name": "NODE_ENV", "value": "production" },
      { "name": "DB_URL", "value": "..." }
    ],
    "healthCheck": {
      "command": ["CMD-SHELL", "curl -f http://localhost:3003/health || exit 1"]
    }
  }]
}
```

### Microservices Communication Summary

```
Sync (REST):  
→ User Service → (GET) → Auth Service
→ Use when: You need the response to continue (validate token before serving request)

Async (Events/Queue):
→ Order Service → (Event) → Payment, Email, Analytics
→ Use when: Response not immediately needed, or fan-out to many services

Service Mesh (Advanced):
→ AWS App Mesh or Istio
→ Handles: Service discovery, load balancing, circuit breaking, observability
→ Added complexity, only worth it at large scale (100+ services)
```

---

## 💼 Interview Questions (WITH SOLUTIONS)

### Q1: What are microservices and how do they differ from a monolith?

**Solution:**
- **Monolith:** Single deployable unit containing all application code. One codebase, one deployment, one database.
- **Microservices:** Multiple small, independently deployable services, each owning its own data, communicating via APIs or events.

Key differences:
| | Monolith | Microservices |
|-|----------|---------------|
| Deployment | All or nothing | Each service independently |
| Scaling | Scale entire app | Scale only bottleneck service |
| Failure | One failure can crash all | Failures isolated per service |
| Team size | Works well for small teams | Enables large team autonomy |
| Data | Shared database | Each service owns its data |

---

### Q2: How do microservices communicate? When to use sync vs async?

**Solution:**
**Synchronous (REST/gRPC):** Service A calls Service B and waits for response.
- Use when: "I need the answer to continue" (e.g., validate auth token before serving)
- Risk: If B is slow or down, A is slow or down (tight coupling at runtime)

**Asynchronous (Events/Queue):** Service A publishes event, B processes when ready.
- Use when: "I don't need to wait" (e.g., send email after signup, update analytics)
- Benefit: A continues without waiting for B. B can be down temporarily.
- Risk: Eventual consistency, harder to debug

**Rule of thumb:**
- For "read" operations: sync REST (need data now)
- For "write" side effects: async events (don't need to wait for email to send)

---

### Q3: What is the API Gateway pattern in microservices?

**Solution:**
API Gateway is a single entry point for all client requests. It sits in front of all microservices and handles:

1. **Routing:** `/users/*` → User Service, `/posts/*` → Post Service
2. **Authentication:** Validates JWT once at gateway, microservices trust the request
3. **Rate Limiting:** Apply rate limits at gateway level
4. **Load Balancing:** Distributes requests across service instances
5. **Request/Response transformation:** Change request format before forwarding
6. **SSL termination:** Handle HTTPS at gateway, internal services use HTTP
7. **Logging:** Centralize access logs

**Without Gateway:**
- Client must know the URL of every microservice
- Auth must be implemented in every service
- CORS, rate limiting in every service

**With Gateway (AWS API Gateway):**
- Client has one URL
- Auth checked once
- Other concerns handled centrally

---

### Q4: How do you handle distributed transactions across microservices?

**Solution:**
Unlike a monolith with one DB (ACID transactions), microservices have separate DBs. You can't do a traditional transaction across them.

**Options:**

1. **Saga Pattern:** Series of local transactions. Each step publishes an event. If any step fails, compensating transactions undo previous steps.

2. **Two-Phase Commit (2PC):** "Can everyone commit?" → "OK, all commit". Very slow and ties services together. Avoid.

3. **Eventual Consistency:** Accept that the system will be consistent eventually. Use idempotency to handle retries.

```javascript
// Order Saga Example:
// 1. Create order → 2. Reserve inventory → 3. Process payment → 4. Confirm order
// If payment fails: Release inventory reservation → Cancel order

class OrderSaga {
  steps = [
    { execute: 'createOrder', compensate: 'cancelOrder' },
    { execute: 'reserveInventory', compensate: 'releaseInventory' },
    { execute: 'processPayment', compensate: 'refundPayment' },
    { execute: 'confirmOrder', compensate: null }
  ];

  async run(orderData) {
    const completedSteps = [];
    
    for (const step of this.steps) {
      try {
        await this[step.execute](orderData);
        completedSteps.push(step);
      } catch (error) {
        // Compensate in reverse order
        for (const completedStep of completedSteps.reverse()) {
          if (completedStep.compensate) {
            await this[completedStep.compensate](orderData);
          }
        }
        throw error;
      }
    }
  }
}
```

---

### Q5: How do you monitor microservices? What tools do you use?

**Solution:**
Monitoring distributed systems requires more than just server logs.

**Distributed Tracing:** Track a request across multiple services
- Tool: AWS X-Ray, Jaeger, Zipkin
- Each request gets a trace ID, passed via headers
- See the full request path: API Gateway → Auth Service → Post Service → DB

```javascript
const AWSXRay = require('aws-xray-sdk');
const http = AWSXRay.captureHTTPs(require('http'));

app.use(AWSXRay.express.openSegment('post-service'));

app.get('/posts/:id', async (req, res) => {
  // X-Ray automatically traces this DB call
  const post = await db.getPost(req.params.id);
  res.json(post);
});

app.use(AWSXRay.express.closeSegment());
```

**Centralized Logging:** All services log to one place
- Tool: AWS CloudWatch Logs, ELK Stack (Elasticsearch + Logstash + Kibana)
- Include traceId, serviceId, requestId in every log

**Metrics Dashboard:** Monitor health of all services
- Tool: AWS CloudWatch, Grafana + Prometheus
- Metrics per service: RPS, error rate, p99 latency, queue depth

**Alerting:** Get notified of problems
- CloudWatch Alarms → SNS → Slack/PagerDuty

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem 1: Design the microservices architecture for WhatsApp

**Solution:**
```
Services:
┌──────────────────────────────────────┐
│ Auth Service                         │
│ - Register, login, JWT               │
│ - DB: PostgreSQL (users, tokens)     │
│ - Port: 3001                         │
└──────────────────────────────────────┘
┌──────────────────────────────────────┐
│ User Service                         │
│ - Profile CRUD, contacts             │
│ - DB: PostgreSQL (user profiles)     │
│ - Cache: Redis (frequent profiles)   │
└──────────────────────────────────────┘
┌──────────────────────────────────────┐
│ Messaging Service                    │
│ - Send/receive messages              │
│ - WebSocket connections (Socket.IO)  │
│ - DB: MongoDB (messages)             │
│ - Queue: SQS (message delivery)      │
└──────────────────────────────────────┘
┌──────────────────────────────────────┐
│ Notification Service                 │
│ - Push notifications (FCM/APNs)      │
│ - Offline message storage            │
│ - Queue: SQS (notifications)         │
└──────────────────────────────────────┘
┌──────────────────────────────────────┐
│ Media Service                        │
│ - Upload photos, videos, documents   │
│ - S3 for storage                     │
│ - Lambda for thumbnail generation    │
│ - CDN (CloudFront) for delivery      │
└──────────────────────────────────────┘
┌──────────────────────────────────────┐
│ Presence Service                     │
│ - Online/offline/last seen           │
│ - DB: Redis (expiring keys)          │
│ - WebSocket connections              │
└──────────────────────────────────────┘

Communication:
- Message send: REST (Messaging Service)
- Message delivered/read: WebSocket (real-time)
- Offline delivery: SQS queue
- New group member: SNS event → all services update

Deployment: Each service on AWS ECS with 2-10 instances
API Gateway routes by path
Health checks on all services
```

---

### Problem 2: How do you deploy a new version of a microservice without downtime?

**Solution:**
```
Rolling Deployment (AWS ECS default):
1. New task definition created with new image version
2. ECS launches new container with new version
3. Health check passes: new container added to target group
4. ECS drains old container (stops sending new requests)
5. Old container completes in-flight requests
6. Old container terminated
7. Repeat for next instance

Blue-Green Deployment (zero risk):
1. Create new "green" environment with new version
2. Test green environment (run smoke tests)
3. Switch API Gateway/ALB traffic from "blue" to "green"
4. Monitor for 15 minutes
5. Success: Terminate blue
   Failure: Switch back to blue (instant rollback!)

Canary Deployment (gradual, safest for critical services):
1. Deploy new version to 5% of servers
2. Monitor error rates and latency for 1 hour
3. If healthy: increase to 25%, then 50%, then 100%
4. If issues: immediately reduce back to 0%

AWS ECS with CodeDeploy supports all three automatically.
```

---

### Navigation
**Prev:** [15_Event_Driven_Architecture.md](15_Event_Driven_Architecture.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [17_Monolith_vs_Microservices.md](17_Monolith_vs_Microservices.md)
