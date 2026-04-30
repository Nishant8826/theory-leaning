# 📌 06 — Async JavaScript Interview Mastery

## 🌟 Introduction

**Async questions dominate JavaScript interviews.** Companies like Google, Amazon, and Flipkart heavily test your understanding of Promises, async/await, and the Event Loop. This file covers advanced async patterns and real interview problems.

---

## 🏗️ 1. Promise Chaining — Order of Execution

### Problem: What is the output?

```javascript
console.log('start');

const p1 = new Promise((resolve) => {
  console.log('promise constructor');
  resolve('resolved');
});

p1.then((val) => {
  console.log(val);
}).then(() => {
  console.log('then 2');
});

console.log('end');
```

**Output:**
```
start
promise constructor     ← Promise constructor runs synchronously!
end
resolved               ← Microtask 1
then 2                 ← Microtask 2
```

**Key Insight:** The Promise constructor callback runs **synchronously**. Only `.then()` callbacks are microtasks.

---

## 🏗️ 2. Nested Promises & Microtask Interleaving

### Problem: What is the output?

```javascript
Promise.resolve().then(() => {
  console.log('A');
  Promise.resolve().then(() => console.log('B'));
}).then(() => console.log('C'));

Promise.resolve().then(() => console.log('D'));
```

**Output:** `A, D, B, C`

**Why?**
1. Two `.then()` callbacks are queued: `[printA, printD]`
2. `printA` runs → logs "A", queues `printB`; the chained `.then(C)` is also queued
3. `printD` runs → logs "D"
4. `printB` runs → logs "B"
5. `printC` runs → logs "C"

---

## 🏗️ 3. async/await Execution Order

### Problem: What is the output?

```javascript
async function foo() {
  console.log('foo start');
  const result = await bar();
  console.log('foo end:', result);
}

async function bar() {
  console.log('bar');
  return 'bar result';
}

console.log('script start');
foo();
console.log('script end');
```

**Output:**
```
script start
foo start
bar
script end
foo end: bar result
```

**Key Insight:** `await` pauses the async function and puts the rest into a microtask. Everything after `await` runs after the current synchronous code completes.

---

## 🏗️ 4. Error Handling in Promise Chains

### Problem: What is the output?

```javascript
Promise.resolve(1)
  .then(val => {
    console.log(val);        // 1
    throw new Error('Oops');
  })
  .then(val => {
    console.log('skip');     // Skipped!
  })
  .catch(err => {
    console.log(err.message); // "Oops"
    return 'recovered';
  })
  .then(val => {
    console.log(val);         // "recovered"
  });
```

**Key Insight:** `.catch()` returns a resolved promise, so the chain continues after catch.

---

## 🏗️ 5. Implement `Promise.allSettled` from scratch

```javascript
function myAllSettled(promises) {
  return Promise.all(
    promises.map(p =>
      Promise.resolve(p)
        .then(value => ({ status: 'fulfilled', value }))
        .catch(reason => ({ status: 'rejected', reason }))
    )
  );
}

// Usage
const results = await myAllSettled([
  Promise.resolve(1),
  Promise.reject('fail'),
  Promise.resolve(3),
]);
// [
//   { status: 'fulfilled', value: 1 },
//   { status: 'rejected', reason: 'fail' },
//   { status: 'fulfilled', value: 3 }
// ]
```

---

## 🏗️ 6. Implement `Promise.race` from scratch

```javascript
function myRace(promises) {
  return new Promise((resolve, reject) => {
    promises.forEach(p => {
      Promise.resolve(p).then(resolve).catch(reject);
    });
  });
}
```

---

## 🏗️ 7. Implement `Promise.any` from scratch

```javascript
function myAny(promises) {
  return new Promise((resolve, reject) => {
    const errors = [];
    let count = 0;

    promises.forEach((p, i) => {
      Promise.resolve(p)
        .then(resolve)  // First resolved wins
        .catch(err => {
          errors[i] = err;
          count++;
          if (count === promises.length) {
            reject(new AggregateError(errors, 'All promises rejected'));
          }
        });
    });
  });
}
```

---

## 🏗️ 8. Retry with Exponential Backoff

**Real Interview Problem:** Implement a function that retries a failed async operation with exponential backoff.

```javascript
async function retry(fn, maxRetries = 3, baseDelay = 1000) {
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (err) {
      if (attempt === maxRetries) throw err;

      const delay = baseDelay * Math.pow(2, attempt);
      const jitter = Math.random() * delay * 0.1; // 10% jitter
      console.log(`Retry ${attempt + 1} in ${delay + jitter}ms`);
      await new Promise(r => setTimeout(r, delay + jitter));
    }
  }
}

// Usage
const data = await retry(() => fetch('https://api.example.com/data'), 3, 500);
```

---

## 🏗️ 9. Sequential vs Parallel vs Batched Execution

```javascript
const urls = ['url1', 'url2', 'url3', 'url4', 'url5'];

// ❌ Sequential — SLOW (one at a time)
async function sequential(urls) {
  const results = [];
  for (const url of urls) {
    results.push(await fetch(url));
  }
  return results;
}

// ✅ Parallel — FAST (all at once)
async function parallel(urls) {
  return Promise.all(urls.map(url => fetch(url)));
}

// ✅ Batched — CONTROLLED (N at a time)
async function batched(urls, batchSize = 2) {
  const results = [];
  for (let i = 0; i < urls.length; i += batchSize) {
    const batch = urls.slice(i, i + batchSize);
    const batchResults = await Promise.all(batch.map(url => fetch(url)));
    results.push(...batchResults);
  }
  return results;
}
```

---

## 🏗️ 10. Implement `sleep()` / `delay()`

```javascript
const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

// Usage
async function demo() {
  console.log('Start');
  await sleep(2000);
  console.log('After 2 seconds');
}
```

---

## 🏗️ 11. Cancel an Async Operation with AbortController

```javascript
const controller = new AbortController();
const { signal } = controller;

// Cancel after 5 seconds
setTimeout(() => controller.abort(), 5000);

try {
  const res = await fetch('https://api.example.com/large-data', { signal });
  const data = await res.json();
} catch (err) {
  if (err.name === 'AbortError') {
    console.log('Request was cancelled');
  } else {
    throw err;
  }
}
```

---

## 🏗️ 12. Timeout wrapper for Promises

```javascript
function withTimeout(promise, ms) {
  const timeout = new Promise((_, reject) =>
    setTimeout(() => reject(new Error(`Timed out after ${ms}ms`)), ms)
  );
  return Promise.race([promise, timeout]);
}

// Usage
try {
  const data = await withTimeout(fetch('/api/slow'), 3000);
} catch (err) {
  console.log(err.message); // "Timed out after 3000ms"
}
```

---

## 🏗️ 13. The `for await...of` Pattern

```javascript
// Async iteration over paginated API
async function* fetchPages(baseUrl) {
  let page = 1;
  let hasMore = true;

  while (hasMore) {
    const res = await fetch(`${baseUrl}?page=${page}`);
    const data = await res.json();
    yield data.items;
    hasMore = data.hasNextPage;
    page++;
  }
}

// Usage
for await (const items of fetchPages('/api/products')) {
  items.forEach(item => console.log(item.name));
}
```

---

## 🏗️ 14. Common Async Mistakes

### Mistake 1: Forgetting to await

```javascript
// ❌ Bug: returns Promise, not the value
async function getUser() {
  const res = fetch('/api/user'); // Missing await!
  return res.json(); // ❌ res is a Promise, not a Response
}

// ✅ Fix
async function getUser() {
  const res = await fetch('/api/user');
  return res.json();
}
```

### Mistake 2: Using forEach with async

```javascript
// ❌ Bug: forEach doesn't wait for async callbacks
[1, 2, 3].forEach(async (n) => {
  await someAsyncOp(n);
});
console.log('Done'); // Prints BEFORE operations complete!

// ✅ Fix: Use for...of
for (const n of [1, 2, 3]) {
  await someAsyncOp(n);
}
console.log('Done'); // Prints AFTER all operations
```

### Mistake 3: Unhandled Promise rejections

```javascript
// ❌ Dangerous: no catch
async function risky() {
  const data = await fetch('/api/fail');
  return data.json();
}
risky(); // If it fails, unhandled rejection!

// ✅ Always handle errors
risky().catch(err => console.error(err));
```

---

## 📐 Async Decision Matrix

| Scenario | Pattern | Why |
| :--- | :--- | :--- |
| Fetch multiple independent resources | `Promise.all` | Parallel = fastest |
| Fetch with some allowed failures | `Promise.allSettled` | Don't fail-fast |
| First response wins (CDN fallback) | `Promise.race` | Fastest server wins |
| First SUCCESS wins | `Promise.any` | Ignore rejections |
| Process items in order | `for...of` + `await` | Sequential guarantee |
| Limited concurrency | Batched or Task Queue | Don't overwhelm server |
| Cancellable request | `AbortController` | User navigates away |
| Auto-retry on failure | Exponential backoff | Network flakiness |

---

## 🔗 Navigation

**Prev:** [05_Most_Asked_50_Questions.md](05_Most_Asked_50_Questions.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [07_Realtime_Scenario_Problems.md](07_Realtime_Scenario_Problems.md)
