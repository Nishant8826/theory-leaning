# Async/Await

## What You Will Learn
* How `async/await` acts as syntactic sugar over Promises.
* How the V8 engine suspends and resumes execution of `async` functions.
* Handling errors cleanly using `try/catch` blocks.
* Identifying and fixing the sequential execution bottleneck.
* Tracing the execution order of `async/await` functions.

## Why This Matters
`async/await` allows you to write asynchronous code that reads like synchronous code, making it easier to read and maintain. However, misusing `await` can introduce performance bottlenecks, such as running independent tasks sequentially rather than in parallel, which slows down your application.

## Theory

### Syntactic Sugar over Promises
The `async` and `await` keywords do not introduce a new execution model. Under the hood, they compile to standard Promises and generator functions:
* Declaring a function as `async` guarantees that it always returns a **Promise**. If you return a primitive value, Node automatically wraps it in a resolved Promise.
* Using `await` suspends the execution of the `async` function, freeing up the main thread to run other JavaScript code. Once the awaited Promise settles, V8 resumes the function's execution with the resolved value.

### Try/Catch Error Handling
In a standard Promise chain, you handle errors using `.catch()`. With `async/await`, you write error-handling logic using standard `try/catch` blocks, which makes catching errors from synchronous and asynchronous code uniform:

```javascript
try {
  const data = await fs.promises.readFile('file.txt');
  console.log(data);
} catch (err) {
  // Catches filesystem errors or parsing errors
  console.error(err);
}
```

## Deep Dive

### The Sequential Execution Bottleneck
A common performance mistake is executing independent operations sequentially when they could run in parallel:

```javascript
// AVOID THIS ANTI-PATTERN (Sequential execution)
const user = await fetchUser();       // Takes 100ms
const orders = await fetchOrders();   // Takes 100ms (Independent! Total: 200ms)
```

Since fetching orders does not depend on the user details, these requests should be initiated in parallel:

```javascript
// PREFERRED APPROACH (Parallel execution)
const [user, orders] = await Promise.all([fetchUser(), fetchOrders()]); // Total: 100ms
```

## Visual Explanation

### Execution Flow: Sequential vs. Parallel Await
```text
Sequential Execution (200ms total):
[ Main Thread ] ── Fetch User (100ms) ──> [ Suspended ] ── Fetch Orders (100ms) ──> [ Resumed ]
Total Latency: |============================================================| (200ms)

Parallel Execution (100ms total):
[ Main Thread ] ── Initiates both requests concurrently (Promise.all)
                ├── Fetch User (100ms) ────┐
                └── Fetch Orders (100ms) ──┴──> [ Resumed when both resolve ]
Total Latency: |==============================| (100ms)
```

## Real-World Example
Consider an API endpoint that compiles a dashboard for a user. It needs to fetch profile data from a database and check their subscription status. Fetching the profile and checking the subscription are independent tasks. Using `Promise.all` with `await` fetches both resources concurrently, cutting the API's response latency in half.

## Code Examples

### Async/Await Ordering and Parallel Execution Optimization

```javascript
// async-await-demo.js
const { promisify } = require('util');
const sleep = promisify(setTimeout);

const getProfile = async () => {
  await sleep(100); // Simulate database read
  return { name: 'Bob' };
};

const getSubscription = async () => {
  await sleep(100); // Simulate billing API check
  return { plan: 'pro' };
};

// 1. Sequential execution (Slow)
async function runSequential() {
  const start = Date.now();
  
  const profile = await getProfile();
  const sub = await getSubscription();
  
  const end = Date.now();
  console.log(`Sequential: Fetch finished in ${end - start}ms.`); // ~200ms
}

// 2. Parallel execution (Fast)
async function runParallel() {
  const start = Date.now();
  
  // Start both promises concurrently and wait for both to settle
  const [profile, sub] = await Promise.all([getProfile(), getSubscription()]);
  
  const end = Date.now();
  console.log(`Parallel: Fetch finished in ${end - start}ms.`); // ~100ms
}

// 3. Tracing Execution Order
async function traceExecution() {
  console.log('Trace: 1 (Start)');
  
  // The expression is evaluated synchronously
  const resultPromise = getProfile(); 
  
  // Code after await is executed as a microtask callback
  const data = await resultPromise;
  console.log('Trace: 3 (Resumed with data:', data.name, ')');
}

async function runAll() {
  await runSequential();
  await runParallel();
  console.log();
  traceExecution();
  console.log('Trace: 2 (Main execution thread clear)');
}
runAll();
```

## Best Practices
* **Run Independent Tasks in Parallel**: Use `Promise.all` or `Promise.allSettled` to execute independent asynchronous operations concurrently instead of using sequential `await` statements.
* **Return Awaited Values in try/catch**: If you want a `try/catch` block to handle errors from a returned Promise, you must `await` the Promise before returning it:
  ```javascript
  // CORRECT: errors are caught in the catch block
  try {
    return await asyncTask(); 
  } catch (err) {
    handle(err);
  }
  ```
* **Avoid wrapping everything in async**: If a function returns a Promise directly and does not need to use `await`, you don't need to declare it as `async`. Returning the Promise directly saves memory overhead.

## Interview Questions

### Beginner
* **What is the relation between Promises and `async/await`?**
  *Answer*: `async/await` is syntactic sugar built on top of Promises. A function marked with the `async` keyword always returns a Promise, and the `await` keyword pauses the execution of that function until the awaited Promise resolves, returning the result.

### Intermediate
* **How do you handle errors when using `async/await`?**
  *Answer*: You handle errors by wrapping the `await` statement inside standard `try/catch` blocks. If the awaited Promise rejects, the rejection reason is thrown as an error that can be caught in the `catch` block.

### Advanced
* **What is the sequential execution bottleneck in `async/await`, and how do you resolve it? Provide code examples.**
  *Answer*: The sequential execution bottleneck occurs when multiple independent asynchronous operations are executed one after the other using separate `await` statements, compounding their latency. 
  You resolve this by starting all independent operations concurrently and waiting for them to settle using `Promise.all` or `Promise.allSettled`:
  ```javascript
  // Slow (Sequential)
  const data1 = await callAPI1();
  const data2 = await callAPI2();

  // Fast (Parallel)
  const [data1, data2] = await Promise.all([callAPI1(), callAPI2()]);
  ```

### Senior Architect
* **Explain how V8 executes `async/await` under the hood. Specifically, trace how the execution context is suspended, how it yields control to the event loop, and how it resumes.**
  *Answer*: When V8 compiles an `async` function, it converts the function into a generator that yields Promises. When execution reaches an `await <Promise>` statement:
  1. The engine evaluates the expression next to `await` and wraps it in a Promise if it is a primitive value.
  2. It saves the function's execution context (including local variables and the instruction pointer) on the heap.
  3. It registers a microtask callback that resumes the function's execution when the Promise settles.
  4. Control is returned back to the caller of the `async` function (or the main event loop if called at the root level).
  5. When the Promise resolves, its callback is pushed to the Promise microtask queue. When the Call Stack clears, V8 drains this queue, restores the saved execution context, and resumes execution from the saved instruction pointer, writing the resolved value to the target variable.

---
Previous : [19_Promises.md] | Index : [00_index.md] | Next : [21_HTTP_Module.md]
