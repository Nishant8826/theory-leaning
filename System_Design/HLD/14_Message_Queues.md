# 📌 Message Queues

## 🧠 Concept Explanation (Story Format)

You placed an order on Amazon at 2 AM. The warehouse workers don't process orders at 2 AM — they start at 6 AM. But Amazon confirms your order immediately. How?

Your order goes into a **queue**. Warehouse workers pick orders from the queue when they're ready. Amazon's system (the producer) puts work in, the warehouse (consumer) takes it out at its own pace.

This is a **Message Queue**: a buffer between services that produce work and services that consume (process) it.

In your Node.js app:
- User uploads a video (producer) → Queue → Video encoding service (consumer)
- User registers (producer) → Queue → Email service (consumer)
- Payment received (producer) → Queue → Invoice service (consumer)

Without queues: If the email service is slow, your API is slow.
With queues: API responds immediately, email sends asynchronously.

---

## 🏗️ Basic Design (Naive)

```javascript
// ❌ Synchronous processing — user waits for everything!
app.post('/register', async (req, res) => {
  const user = await db.createUser(req.body);       // 50ms
  await emailService.sendWelcome(user.email);        // 500ms! (external service)
  await analyticsService.trackSignup(user);          // 200ms
  await slackNotify('New user: ' + user.email);      // 300ms
  
  res.json({ user }); // User waits 1050ms for a simple registration!
});
// If email service is down → entire registration fails!
```

---

## ⚡ Optimized Design

```
Producer: Node.js API
Consumer: Separate Worker Processes

User registers
    ↓
API creates user in DB (50ms)
    ↓
API puts jobs in Queue (5ms):
  - { type: 'sendWelcomeEmail', userId: '123' }
  - { type: 'trackSignup', userId: '123' }
  - { type: 'slackNotify', userId: '123' }
    ↓
API returns response to user (55ms total!)
    
Meanwhile, workers process queue:
Worker 1 → sends welcome email
Worker 2 → tracks analytics
Worker 3 → sends Slack notification
```

---

## 🔍 Key Components

### AWS SQS (Simple Queue Service)

AWS SQS is a fully managed message queue — no servers to manage.

```javascript
const AWS = require('aws-sdk');
const sqs = new AWS.SQS({ region: 'us-east-1' });

// Producer: Send message to queue
async function sendToQueue(queueUrl, data) {
  const params = {
    QueueUrl: queueUrl,
    MessageBody: JSON.stringify(data),
    MessageGroupId: data.userId,  // For FIFO queues — same user's messages stay ordered
    DelaySeconds: 0  // Process immediately (or delay up to 15 min)
  };
  
  const result = await sqs.sendMessage(params).promise();
  console.log(`Message sent: ${result.MessageId}`);
  return result;
}

// Usage in API route
app.post('/register', async (req, res) => {
  const user = await userService.create(req.body);
  
  // Fire and forget! Don't await the queue operations.
  Promise.all([
    sendToQueue(process.env.EMAIL_QUEUE_URL, { type: 'welcomeEmail', userId: user.id }),
    sendToQueue(process.env.ANALYTICS_QUEUE_URL, { type: 'signup', userId: user.id })
  ]).catch(err => console.error('Queue error:', err)); // Handle queue errors separately
  
  res.status(201).json({ user }); // Return IMMEDIATELY!
});

// Consumer: Worker process (runs separately)
async function processEmailQueue() {
  while (true) {
    const response = await sqs.receiveMessage({
      QueueUrl: process.env.EMAIL_QUEUE_URL,
      MaxNumberOfMessages: 10,      // Batch process up to 10
      WaitTimeSeconds: 20,          // Long polling — wait up to 20s for messages
      VisibilityTimeout: 300        // Hide message for 5 min while processing
    }).promise();
    
    if (!response.Messages) continue; // No messages, loop again
    
    for (const message of response.Messages) {
      try {
        const data = JSON.parse(message.Body);
        await emailService.sendWelcome(data.userId);
        
        // Success: Delete message from queue
        await sqs.deleteMessage({
          QueueUrl: process.env.EMAIL_QUEUE_URL,
          ReceiptHandle: message.ReceiptHandle  // Unique handle for this message
        }).promise();
      } catch (error) {
        console.error('Failed to process message:', error);
        // Don't delete → message becomes visible again after VisibilityTimeout
        // SQS automatically retries!
      }
    }
  }
}

processEmailQueue(); // Start worker
```

---

### Bull Queue (Redis-based, Node.js native)

Bull is easier to use for Node.js-to-Node.js queuing:

```javascript
const Bull = require('bull');

// Create queues
const emailQueue = new Bull('email-queue', { redis: { url: process.env.REDIS_URL } });
const imageQueue = new Bull('image-processing', { redis: { url: process.env.REDIS_URL } });

// Producer: Add jobs
app.post('/upload', async (req, res) => {
  const imageKey = await uploadToS3(req.file);
  
  // Add job with options
  await imageQueue.add(
    { imageKey, userId: req.user.id },
    {
      attempts: 3,          // Retry up to 3 times on failure
      backoff: {
        type: 'exponential',
        delay: 2000          // 2s, 4s, 8s between retries
      },
      removeOnComplete: 100, // Keep last 100 completed jobs
      removeOnFail: 500      // Keep last 500 failed jobs
    }
  );
  
  res.status(202).json({ message: 'Upload queued', imageKey });
});

// Consumer: Process jobs
imageQueue.process(5, async (job) => {  // Process 5 concurrent jobs
  const { imageKey, userId } = job.data;
  
  // Update progress
  await job.progress(10);
  
  const thumbnails = await generateThumbnails(imageKey);
  await job.progress(70);
  
  await db.updateImage(imageKey, { thumbnails, status: 'processed' });
  await job.progress(90);
  
  await notifyUser(userId, 'Image processed!');
  await job.progress(100);
  
  return { thumbnails };
});

// Monitor job events
imageQueue.on('completed', (job, result) => {
  console.log(`Job ${job.id} completed:`, result);
});

imageQueue.on('failed', (job, error) => {
  console.error(`Job ${job.id} failed:`, error.message);
  // Alert if too many failures: notify via Slack, PagerDuty
});

// Get queue stats (for monitoring dashboard)
const waiting = await imageQueue.getWaitingCount();
const active = await imageQueue.getActiveCount();
const failed = await imageQueue.getFailedCount();
```

---

### Queue Patterns

**Dead Letter Queue (DLQ):**
```javascript
// Messages that fail repeatedly go to DLQ for manual inspection
const sqs = new AWS.SQS();

// Main queue configuration
const queueParams = {
  QueueName: 'email-queue',
  Attributes: {
    RedrivePolicy: JSON.stringify({
      deadLetterTargetArn: 'arn:aws:sqs:us-east-1:123:email-dlq',
      maxReceiveCount: '5'  // Move to DLQ after 5 failed attempts
    })
  }
};

// Monitor DLQ: Alert when messages appear here
// Schedule: Retry DLQ messages periodically
```

**Fan-Out Pattern (SNS + SQS):**
```javascript
// One event → multiple queues → multiple consumers
// AWS SNS (Simple Notification Service) publishes to multiple SQS queues

const sns = new AWS.SNS();

// Publish ONE event
await sns.publish({
  TopicArn: process.env.USER_SIGNUP_TOPIC,
  Message: JSON.stringify({ userId: '123', email: 'alice@example.com' })
}).promise();

// SNS automatically delivers to all subscribed SQS queues:
// → email-queue (sends welcome email)
// → analytics-queue (tracks signup)
// → notifications-queue (sends push notification)
// → crm-queue (adds to CRM system)
// Each queue has its own consumer service!
```

---

## ⚖️ Trade-offs

| With Message Queue | Without Message Queue |
|-------------------|----------------------|
| Async (fast API responses) | Synchronous (slow API) |
| Services decoupled | Services tightly coupled |
| Consumer can scale independently | Everything scales together |
| Failed jobs can be retried | Failed = user sees error |
| Complex to debug | Simple request-response |
| Additional infrastructure | Simple but fragile |

---

## 📊 Scalability Discussion

### SQS vs Bull vs Kafka

| Feature | AWS SQS | Bull (Redis) | Apache Kafka |
|---------|---------|--------------|--------------|
| Setup | Managed (zero setup) | Need Redis | Complex setup |
| Throughput | High (standard) | Medium | Very high (millions/sec) |
| Message replay | No (deleted after consume) | Limited | Yes (retain for days/weeks) |
| Ordering | FIFO queues only | Yes | Per partition |
| Use case | Decoupling services | Node.js jobs | Event streaming |
| Cost | Pay per message | Redis cost | Infrastructure cost |

**Our stack recommendation:**
- **Bull + Redis:** Background jobs (email, image processing, notifications)
- **AWS SQS:** Cross-service communication, reliable delivery
- **Kafka:** If you need event streaming or replay (rare for most apps)

---

## 💼 Interview Questions (WITH SOLUTIONS)

### Q1: What is a message queue and what problem does it solve?

**Solution:**
A message queue is a communication mechanism where a producer sends messages to a queue, and consumers process them independently. It solves:

1. **Decoupling:** Services don't need to know about each other. Email service doesn't need to call payment service directly.
2. **Asynchronous processing:** API responds immediately, heavy work done in background.
3. **Load leveling:** Queue absorbs traffic spikes. Consumer processes at its own pace.
4. **Retry logic:** Failed messages stay in queue and are retried automatically.
5. **Fault tolerance:** If consumer crashes, messages wait in queue (not lost).

Without queue: If your email service is slow, every API call is slow.
With queue: Email service slowness doesn't affect API latency.

---

### Q2: How do you ensure a message is processed exactly once?

**Solution:**
**"Exactly once" is very hard.** Most systems aim for "at least once" with idempotency checks.

**At-least-once delivery (SQS default):**
- Message may be delivered multiple times (network issues, consumer crash mid-processing)
- Solution: Make your consumer **idempotent** (processing twice = same result)

```javascript
// Idempotent consumer
async function processPayment(message) {
  const { orderId, amount } = JSON.parse(message.Body);
  
  // Check if already processed (idempotency key)
  const alreadyProcessed = await db.query(
    'SELECT id FROM payments WHERE order_id = $1', [orderId]
  );
  
  if (alreadyProcessed.rows.length > 0) {
    console.log(`Order ${orderId} already processed, skipping`);
    await deleteFromQueue(message); // Delete so it's not processed again
    return;
  }
  
  // Process payment (idempotent at the database level via UNIQUE constraint)
  await db.query(
    'INSERT INTO payments (order_id, amount) VALUES ($1, $2) ON CONFLICT DO NOTHING',
    [orderId, amount]
  );
  
  await deleteFromQueue(message);
}
```

**SQS FIFO queues** support "exactly-once" with MessageDeduplicationId. Duplicate messages with same ID within 5 minutes are ignored.

---

### Q3: What is the difference between a message queue and a pub/sub system?

**Solution:**
| Feature | Message Queue | Pub/Sub |
|---------|--------------|---------|
| Consumers | One consumer per message | All subscribers receive message |
| Pattern | Point-to-point | Broadcast |
| Example | "Process this order" (one service) | "User signed up" (many services need to know) |
| AWS service | SQS | SNS |
| Use case | Work distribution | Event notification |

```
Queue: Producer → [Q] → Consumer1 OR Consumer2 (load balanced, one gets it)

Pub/Sub: Publisher → Topic → Subscriber1
                           → Subscriber2
                           → Subscriber3 (ALL get it)
```

In practice, combine them: SNS (pub/sub) → multiple SQS queues (one per consumer group).

---

### Q4: How do you handle message ordering in a distributed system?

**Solution:**
Ordering is hard because multiple consumers process in parallel.

**AWS SQS FIFO Queue:**
```javascript
// FIFO queue: messages in same group are ordered
await sqs.sendMessage({
  QueueUrl: process.env.FIFO_QUEUE_URL + '.fifo',
  MessageBody: JSON.stringify({ action: 'updateBalance', amount: 100 }),
  MessageGroupId: `account:${accountId}`,  // All messages for this account are ordered
  MessageDeduplicationId: `${accountId}-${Date.now()}` // Unique per message
}).promise();
```

**Manual ordering with sequence numbers:**
```javascript
// Attach sequence number to messages
const message = {
  sequenceNumber: await redis.incr(`seq:${conversationId}`),
  content: 'Hello!',
  conversationId
};

// Consumer: Buffer out-of-order messages
const buffer = {};
async function processWithOrder(msg) {
  const expected = await redis.get(`expected_seq:${msg.conversationId}`) || 1;
  
  if (msg.sequenceNumber === expected) {
    await processMessage(msg);
    await redis.incr(`expected_seq:${msg.conversationId}`);
    // Process any buffered next messages
    while (buffer[expected + 1]) {
      await processMessage(buffer[expected + 1]);
      delete buffer[expected + 1];
      expected++;
    }
  } else {
    buffer[msg.sequenceNumber] = msg; // Buffer for later
  }
}
```

---

### Q5: How does Bull handle job failures and retries?

**Solution:**
```javascript
// Configure retry behavior per job
await emailQueue.add(
  { to: 'user@example.com', template: 'welcome' },
  {
    attempts: 5,           // Retry up to 5 times
    backoff: {
      type: 'exponential', // Exponential backoff
      delay: 1000          // 1s, 2s, 4s, 8s, 16s between retries
    }
  }
);

// Handle failures
emailQueue.on('failed', async (job, error) => {
  if (job.attemptsMade >= job.opts.attempts) {
    // Max retries exceeded — alert!
    await alertingService.notify({
      severity: 'high',
      message: `Email job ${job.id} failed permanently: ${error.message}`,
      data: job.data
    });
    
    // Move to custom DLQ table for manual review
    await db.query(
      'INSERT INTO failed_jobs (queue, data, error, failed_at) VALUES ($1, $2, $3, NOW())',
      ['email', JSON.stringify(job.data), error.message]
    );
  }
});

// Manual retry for DLQ
app.post('/admin/retry-failed-job/:id', async (req, res) => {
  const job = await emailQueue.getJob(req.params.id);
  await job.retry();
  res.json({ message: 'Job retried' });
});
```

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem 1: Design an order processing system with message queues for an e-commerce app

**Solution:**
```javascript
// Complete order flow with queues

// When order is placed:
app.post('/orders', async (req, res) => {
  const order = await db.createOrder(req.body);
  
  // Publish to SNS topic — fan out to multiple queues
  await sns.publish({
    TopicArn: process.env.ORDER_PLACED_TOPIC,
    Message: JSON.stringify({ orderId: order.id, userId: order.userId, items: order.items })
  }).promise();
  
  res.status(201).json({ order, message: 'Order placed successfully' });
});

// SNS delivers to multiple SQS queues:

// 1. Payment Queue → payment worker
paymentQueue.process(async (job) => {
  const { orderId } = job.data;
  const order = await db.getOrder(orderId);
  const charge = await stripe.charges.create({ amount: order.total });
  await db.updateOrder(orderId, { status: 'paid', chargeId: charge.id });
  
  // Put next event in queue
  await sns.publish({ TopicArn: PAYMENT_SUCCESS_TOPIC, Message: JSON.stringify({ orderId }) });
});

// 2. Inventory Queue → inventory worker
inventoryQueue.process(async (job) => {
  const { items } = job.data;
  for (const item of items) {
    await db.decrementInventory(item.productId, item.quantity);
  }
});

// 3. Email Queue → email worker
emailQueue.process(async (job) => {
  const { orderId, userId } = job.data;
  const user = await db.getUser(userId);
  await emailService.sendOrderConfirmation(user.email, orderId);
});

// 4. Analytics Queue → analytics worker
analyticsQueue.process(async (job) => {
  await analytics.trackPurchase(job.data);
});
```

---

### Problem 2: Your message queue has 1 million unprocessed messages (queue backup). What do you do?

**Solution:**
```
Immediate actions:
1. Scale up consumers:
   - Increase Bull concurrency: queue.process(50, handler) instead of process(5, handler)
   - Add more consumer instances (horizontal scaling)
   - AWS SQS: Launch more EC2 workers via Auto Scaling

2. Identify bottleneck:
   - Is each job slow? → Optimize the processing logic
   - Is external service slow? → Add circuit breaker, queue to that service

3. Prioritization:
   - Add priority levels to queue: critical > high > normal
   - Process payment jobs before analytics jobs

4. Triage:
   - Are some jobs stale? (1M backlog — were these from 3 days ago?)
   - Purge old messages if they're no longer relevant
   
5. Alert and monitor:
   - Set CloudWatch alarm when queue depth > 1000
   - Dashboard showing queue depth, processing rate, DLQ count
   
6. Post-incident:
   - Determine why backlog grew (consumer crash? traffic spike?)
   - Set up auto-scaling for consumers based on queue depth
   - Add circuit breaker to prevent cascade failures

Auto-scaling consumers based on SQS queue depth:
CloudWatch Metric: ApproximateNumberOfMessagesVisible
Scale out when: > 1000 messages
Scale in when: < 100 messages
```

---

### Navigation
**Prev:** [13_Rate_Limiting.md](13_Rate_Limiting.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [15_Event_Driven_Architecture.md](15_Event_Driven_Architecture.md)
