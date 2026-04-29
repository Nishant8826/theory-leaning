# 📌 04 — Message Queues: Task Management and Background Processing

## 🧠 Concept Explanation

### Basic → Intermediate
A Message Queue (MQ) is a buffer that stores "tasks" or "messages" that need to be processed later. It allows you to move heavy work (like image resizing or data crunching) out of the main request-response path.

### Advanced → Expert
At a staff level, MQs are about **Load Smoothing** and **Resource Management**. 
1. **Producer**: The web server creates a job and adds it to the queue.
2. **Broker**: (Redis, RabbitMQ, SQS) stores the job reliably.
3. **Worker**: A separate pool of Node.js processes that pull jobs from the queue and execute them.

This ensures that even if you get 10,000 image uploads in 1 second, your web server stays fast. The workers will just work through the queue as fast as they can (Backpressure management).

---

## 🏗️ Common Mental Model
"Queues are just for async tasks."
**Correction**: Queues are for **guaranteed execution**. Unlike a simple `setTimeout` or a Promise, if the server crashes, the job remains in the persistent queue (Redis/Disk) and will be picked up by another worker.

---

## ⚡ Actual Behavior: Visibility Timeout
When a worker picks up a job, the job isn't deleted immediately. It is "hidden" from other workers for a specific time (Visibility Timeout). If the worker doesn't acknowledge (ACK) completion within that time, the job becomes visible again for another worker to try. This is how MQs handle worker crashes.

---

## 🔬 Internal Mechanics (Redis + BullMQ)

### BullMQ Internals
BullMQ uses **Redis Lua scripts** to ensure atomicity. 
1. Jobs are stored in a Redis **Hash**.
2. Queue state is managed in **Sorted Sets** (ZSETs) keyed by priority and timestamp.
3. This ensures that even with hundreds of concurrent workers, no job is processed twice simultaneously.

---

## 📐 ASCII Diagrams

### Task Queue Lifecycle
```text
  ┌───────────────┐           ┌────────────────┐           ┌───────────────┐
  │   PRODUCER    │ ──Job───▶ │     QUEUE      │ ──Pull──▶ │    WORKER     │
  │ (Web Server)  │           │    (Redis)     │           │ (Background)  │
  └───────────────┘           └────────────────┘           └───────┬───────┘
                                     ▲                             │
                                     └────────── ACK/Done ─────────┘
```

---

## 🔍 Code Example: BullMQ with Redis
```javascript
const { Queue, Worker } = require('bullmq');

// 1. Setup the Queue (Producer)
const imageQueue = new Queue('image-processing', { connection: { host: 'localhost', port: 6379 } });

async function addJob() {
  await imageQueue.add('resize', { imageUrl: 's3://bucket/img.jpg' }, {
    attempts: 3, // Retry 3 times on failure
    backoff: { type: 'exponential', delay: 1000 }
  });
}

// 2. Setup the Worker (Consumer)
const worker = new Worker('image-processing', async (job) => {
  console.log(`Processing job ${job.id}: ${job.data.imageUrl}`);
  // Perform heavy image resizing here
  return { success: true };
}, { connection: { host: 'localhost', port: 6379 } });

worker.on('completed', job => console.log(`Job ${job.id} done!`));
```

---

## 💥 Production Failures & Debugging

### Scenario: The "Stuck" Job
**Problem**: The queue size is growing, but workers seem to be idle.
**Reason**: A job is taking longer than the **Visibility Timeout**. The broker thinks the worker died and makes the job visible again. Another worker picks it up, it takes too long again... loop.
**Fix**: Increase the timeout or ensure the worker "heartbeats" the broker to say it's still alive.

### Scenario: Redis OOM (Out of Memory)
**Problem**: Redis crashes or starts evicting keys.
**Reason**: You are adding millions of jobs but not deleting the "completed" ones. BullMQ stores job history by default.
**Fix**: Configure job retention: `{ removeOnComplete: true, removeOnFail: 100 }`.

---

## 🧪 Real-time Production Q&A

**Q: "Should I use BullMQ (Redis) or SQS?"**
**A**: Use **BullMQ** if you need high performance (thousands of jobs per second), complex features (delayed jobs, priorities, parent/child jobs), and already have Redis. Use **SQS** if you want a managed AWS service that scales to infinity with zero maintenance.

---

## 🏢 Industry Best Practices
- **Separate Workers**: Run your workers on separate infrastructure from your API servers to ensure CPU-intensive jobs don't slow down HTTP responses.
- **Monitoring**: Always monitor **Queue Depth** (total pending jobs) and **Job Latency**.

---

## 💼 Interview Questions
**Q: What is a "Delayed Job" and how is it implemented?**
**A**: A delayed job is a task that shouldn't run until a future time (e.g. "Send reminder email in 24 hours"). In Redis-based queues, these are stored in a **Sorted Set** where the "score" is the timestamp. A background process periodically checks the set for scores `<=` current time and moves them to the active queue.

---

## 🧩 Practice Problems
1. Implement a "Rate Limited Worker" that only processes 10 jobs per minute across all instances.
2. Build a "Priority Queue" where "Gold Users" have their jobs processed before "Free Users."

---

**Prev:** [03_Event_Driven_Architecture.md](./03_Event_Driven_Architecture.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [05_Backend_For_Frontend.md](./05_Backend_For_Frontend.md)
