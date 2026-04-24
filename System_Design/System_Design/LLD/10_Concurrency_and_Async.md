# 📌 Concurrency and Async Patterns

## 🧠 Concept Explanation (Story Format)

You're at a restaurant. A bad waiter takes one order, goes to the kitchen, waits for the food, brings it, then takes the next order. This is synchronous — slow, inefficient.

A good waiter takes all orders, submits them to the kitchen, then brings food to each table as it's ready. This is asynchronous — handles multiple tasks concurrently.

Node.js is built on this async model. Understanding how to handle async operations correctly determines whether your app handles 100 users or 100,000 users.

---

## 🔍 JavaScript Async Patterns

### 1. Promise Fundamentals

```javascript
// Promise states: pending → fulfilled | rejected

// ❌ Callback hell (avoid)
db.getUser(userId, (err, user) => {
  if (err) return callback(err);
  db.getPosts(user.id, (err, posts) => {
    if (err) return callback(err);
    emailService.send(user.email, (err, result) => {
      if (err) return callback(err);
      callback(null, result);
    });
  });
});

// ✅ Promise chain
db.getUser(userId)
  .then(user => db.getPosts(user.id))
  .then(posts => emailService.send(posts[0].userId))
  .catch(err => console.error(err));

// ✅ Async/await (most readable)
async function processUser(userId) {
  const user = await db.getUser(userId);    // Waits for user
  const posts = await db.getPosts(user.id); // Then waits for posts
  await emailService.send(user.email, posts);
  return { user, posts };
}
```

### 2. Parallel vs Sequential Execution

```javascript
// ❌ Sequential when parallel is possible (slow!)
async function getUserDashboard(userId) {
  const user = await db.getUser(userId);            // 50ms
  const posts = await db.getUserPosts(userId);       // 100ms  
  const followers = await db.getFollowers(userId);  // 80ms
  const notifications = await db.getNotifications(userId); // 60ms
  // Total: 290ms
  
  return { user, posts, followers, notifications };
}

// ✅ Parallel execution (much faster!)
async function getUserDashboard(userId) {
  const [user, posts, followers, notifications] = await Promise.all([
    db.getUser(userId),
    db.getUserPosts(userId),
    db.getFollowers(userId),
    db.getNotifications(userId)
  ]);
  // Total: 100ms (slowest individual operation)!
  
  return { user, posts, followers, notifications };
}

// ✅ Promise.allSettled — run all, don't fail if one fails
async function getOptionalData(userId) {
  const results = await Promise.allSettled([
    db.getUser(userId),            // Required
    db.getRecommendations(userId), // Optional
    analytics.getUserScore(userId) // Optional (external service)
  ]);
  
  const [userResult, recResult, scoreResult] = results;
  
  return {
    user: userResult.status === 'fulfilled' ? userResult.value : null,
    recommendations: recResult.status === 'fulfilled' ? recResult.value : [],
    score: scoreResult.status === 'fulfilled' ? scoreResult.value : 0
  };
}

// ✅ Promise.race — return fastest result
async function getWithTimeout(fetchFn, timeoutMs = 3000) {
  return Promise.race([
    fetchFn(),
    new Promise((_, reject) => setTimeout(() => reject(new Error('Timeout')), timeoutMs))
  ]);
}

// ✅ Promise.any — first success (any of them succeeds)
async function fetchFromAnyReplica(data) {
  return Promise.any([
    primaryDB.query(data),    // Try primary
    replica1.query(data),     // Try replica 1
    replica2.query(data)      // Try replica 2
  ]);
  // Returns whichever responds first, ignores failures
}
```

### 3. Concurrency Control

```javascript
// Problem: Processing 10,000 items — don't overwhelm external API!
const pLimit = require('p-limit');

// Limit: max 5 concurrent operations
async function processItemsWithLimit(items, concurrency = 5) {
  const limit = pLimit(concurrency);
  
  const results = await Promise.all(
    items.map(item => limit(() => processItem(item)))
  );
  
  return results;
}

// Without p-limit — would fire all 10,000 simultaneously!
// Kills your DB / external API

// Batch processing with concurrency
async function batchProcess(items, batchSize = 100, concurrency = 5) {
  const limit = pLimit(concurrency);
  const results = [];
  
  // Process in batches
  for (let i = 0; i < items.length; i += batchSize) {
    const batch = items.slice(i, i + batchSize);
    
    const batchResults = await Promise.all(
      batch.map(item => limit(() => processItem(item)))
    );
    
    results.push(...batchResults);
    
    // Optional: Progress reporting
    console.log(`Processed ${Math.min(i + batchSize, items.length)}/${items.length}`);
  }
  
  return results;
}

// Manual queue
class AsyncQueue {
  #queue = [];
  #running = 0;
  #concurrency;
  
  constructor(concurrency = 5) {
    this.#concurrency = concurrency;
  }
  
  async add(fn) {
    return new Promise((resolve, reject) => {
      this.#queue.push({ fn, resolve, reject });
      this.#run();
    });
  }
  
  #run() {
    while (this.#running < this.#concurrency && this.#queue.length) {
      const { fn, resolve, reject } = this.#queue.shift();
      this.#running++;
      Promise.resolve(fn())
        .then(resolve, reject)
        .finally(() => {
          this.#running--;
          this.#run(); // Process next item
        });
    }
  }
}

const queue = new AsyncQueue(3); // Max 3 concurrent
await Promise.all(images.map(img => queue.add(() => processImage(img))));
```

### 4. Event Loop and Blocking

```javascript
// ❌ Blocking the event loop — TERRIBLE in Node.js!
app.get('/compute', (req, res) => {
  // CPU-intensive operation blocks ALL other requests!
  let result = 0;
  for (let i = 0; i < 10_000_000_000; i++) {
    result += i;
  }
  res.json({ result }); // During this: zero other requests processed!
});

// ✅ Move heavy computation to worker thread
const { Worker, isMainThread, parentPort } = require('worker_threads');
const path = require('path');

// Worker file (compute.worker.js)
if (!isMainThread) {
  parentPort.on('message', (data) => {
    let result = 0;
    for (let i = 0; i < data.n; i++) result += i;
    parentPort.postMessage({ result });
  });
}

// Main file
function computeInWorker(n) {
  return new Promise((resolve, reject) => {
    const worker = new Worker(path.join(__dirname, 'compute.worker.js'));
    worker.postMessage({ n });
    worker.on('message', resolve);
    worker.on('error', reject);
  });
}

app.get('/compute', async (req, res) => {
  const result = await computeInWorker(10_000_000_000);
  res.json(result); // Event loop free during computation!
});

// ✅ Use setImmediate to yield control in tight loops
async function processLargeArray(items) {
  const results = [];
  for (const item of items) {
    results.push(await processItem(item));
    
    // Yield control to event loop every 100 items
    if (results.length % 100 === 0) {
      await new Promise(resolve => setImmediate(resolve));
    }
  }
  return results;
}
```

### 5. Async Error Handling

```javascript
// ✅ Always handle Promise rejections!

// Unhandled rejection = process crash in newer Node.js versions!
process.on('unhandledRejection', (reason, promise) => {
  logger.error('Unhandled Promise Rejection:', { reason, promise });
  // Don't exit — log and continue (or exit if critical)
});

// Async middleware wrapper
const asyncHandler = fn => (req, res, next) => {
  Promise.resolve(fn(req, res, next)).catch(next);
};

// Error-safe parallel execution
async function safeParallel(promises) {
  const results = await Promise.allSettled(promises);
  
  const errors = results
    .filter(r => r.status === 'rejected')
    .map(r => r.reason);
  
  if (errors.length > 0) {
    logger.warn('Some parallel operations failed', { errors: errors.map(e => e.message) });
  }
  
  return results
    .filter(r => r.status === 'fulfilled')
    .map(r => r.value);
}

// Retry with exponential backoff
async function withRetry(fn, options = {}) {
  const { maxRetries = 3, baseDelay = 1000, maxDelay = 30000, retryCondition = () => true } = options;
  
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (attempt === maxRetries || !retryCondition(error)) {
        throw error; // Max retries or not retryable — give up
      }
      
      // Exponential backoff with jitter
      const delay = Math.min(baseDelay * Math.pow(2, attempt - 1) + Math.random() * 1000, maxDelay);
      logger.warn(`Attempt ${attempt} failed, retrying in ${delay}ms...`, { error: error.message });
      await new Promise(r => setTimeout(r, delay));
    }
  }
}

// Usage
const data = await withRetry(
  () => externalApiService.fetchData(params),
  {
    maxRetries: 3,
    baseDelay: 500,
    retryCondition: (err) => err.status === 503 || err.code === 'ECONNRESET' // Only retry transient errors
  }
);
```

### 6. Async Generators for Streaming

```javascript
// Process large datasets without loading all into memory
async function* streamUsers(batchSize = 100) {
  let offset = 0;
  
  while (true) {
    const batch = await db.query(
      'SELECT * FROM users ORDER BY id LIMIT $1 OFFSET $2',
      [batchSize, offset]
    );
    
    if (batch.rows.length === 0) break; // No more data
    
    for (const user of batch.rows) {
      yield user; // Process one at a time
    }
    
    offset += batchSize;
  }
}

// Use the generator
async function processAllUsers() {
  let count = 0;
  
  for await (const user of streamUsers(100)) {
    await sendEmailToUser(user); // Process one user at a time!
    count++;
    if (count % 1000 === 0) console.log(`Processed ${count} users`);
  }
}

// Streaming HTTP response (large CSV export)
app.get('/export/users.csv', authenticate, async (req, res) => {
  res.setHeader('Content-Type', 'text/csv');
  res.setHeader('Content-Disposition', 'attachment; filename="users.csv"');
  
  res.write('id,name,email,created_at\n'); // Header
  
  for await (const user of streamUsers(500)) {
    res.write(`${user.id},"${user.name}",${user.email},${user.created_at}\n`);
  }
  
  res.end();
  // Memory-efficient: Never loads all users into memory!
});
```

---

## ⚖️ Trade-offs

| Pattern | Use When | Avoid When |
|---------|---------|-----------|
| Parallel (Promise.all) | Independent operations | Operations have dependencies |
| Sequential (await in loop) | Order matters, dependent | All could run in parallel |
| p-limit | High volume, concurrency limit | Few items |
| Worker threads | CPU-intensive tasks | I/O-bound tasks |
| Streams/Generators | Large data | Small data |

---

## 💼 Interview Questions (WITH SOLUTIONS)

### Q1: What is the Node.js event loop?

**Solution:**
Node.js is single-threaded but non-blocking. The event loop is the mechanism that allows it to handle many concurrent operations.

```
Call Stack → runs synchronous code
Event Loop → when call stack empty, picks up callbacks from:
  - Microtask queue (Promises, queueMicrotask) — checked FIRST
  - Timers (setTimeout, setInterval)
  - I/O callbacks
  - setImmediate
  - Close callbacks
```

Because I/O (network, disk) is handled by libuv (C++ library) asynchronously, Node.js can start an I/O operation and move on to handle other requests while waiting for the response. This is why Node.js can handle thousands of concurrent connections despite being single-threaded.

### Q2: What is the difference between Promise.all, Promise.allSettled, Promise.race, and Promise.any?

**Solution:**
| Method | Resolves | Rejects |
|--------|---------|---------|
| `Promise.all` | When ALL succeed | When ANY fail |
| `Promise.allSettled` | When ALL complete (success or fail) | Never rejects |
| `Promise.race` | When FIRST completes (success or fail) | When first rejects |
| `Promise.any` | When FIRST succeeds | When ALL fail |

Use cases:
- `all`: Load all required data (any failure = can't proceed)
- `allSettled`: Load optional data (some can fail gracefully)
- `race`: Timeout implementation, try fastest of N sources
- `any`: Try multiple sources, need any one to succeed

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem: Process 1 million user records with max 10 concurrent DB operations

```javascript
const pLimit = require('p-limit');

async function processOneMillionUsers() {
  const limit = pLimit(10); // Max 10 concurrent
  let processedCount = 0;
  
  for await (const user of streamUsers(1000)) { // Stream in batches of 1000
    await limit(async () => {
      await processUser(user); // Process with concurrency limit
      processedCount++;
      if (processedCount % 10000 === 0) {
        console.log(`Progress: ${processedCount} processed`);
      }
    });
  }
  
  console.log(`Complete! Processed ${processedCount} users`);
}

// Alternatively, with worker threads for CPU-intensive processing
const { Worker } = require('worker_threads');
const os = require('os');

const CPU_COUNT = os.cpus().length;

async function processWithWorkers(items) {
  const chunkSize = Math.ceil(items.length / CPU_COUNT);
  const chunks = Array.from({ length: CPU_COUNT }, (_, i) =>
    items.slice(i * chunkSize, (i + 1) * chunkSize)
  );
  
  const results = await Promise.all(
    chunks.map(chunk => new Promise((resolve, reject) => {
      const worker = new Worker('./process.worker.js', { workerData: { chunk } });
      worker.on('message', resolve);
      worker.on('error', reject);
    }))
  );
  
  return results.flat();
}
```

---

### Navigation
**Prev:** [09_Caching_Strategy.md](09_Caching_Strategy.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** None (End of LLD) → Continue to Case Studies
