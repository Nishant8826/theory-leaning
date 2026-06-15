# Callbacks

## What You Will Learn
* The fundamental concept of asynchronous callbacks.
* The design and rules of the **Error-First Callback** pattern.
* What causes "Callback Hell" (Pyramid of Doom).
* Designing clean, modular asynchronous control flows.
* Converting callback-based APIs into Promises (Promisification).

## Why This Matters
Before Promises and Async/Await, callbacks were the only way to write asynchronous code in Node.js. Although modern codebases use newer patterns, thousands of npm packages and core Node APIs still rely on callbacks under the hood. Understanding callbacks is essential for maintaining older codebases and working with legacy libraries.

## Theory

### Asynchronous Callbacks
In JavaScript, functions are first-class citizens: they can be passed as arguments to other functions. An **asynchronous callback** is a function passed to an I/O operation. When the I/O operation completes in the background (via Libuv), the callback is pushed to the event queue to be executed on the main thread.

### The Error-First Callback Pattern
Node.js standardizes callbacks using the **Error-First Callback** pattern. Every asynchronous callback function must follow two rules:
1. The **first argument** is reserved for an error object (`err`). If the operation succeeds, this argument is set to `null` or `undefined`.
2. The **second argument** (and any subsequent arguments) is reserved for the returned data or result.

```javascript
fs.readFile('file.txt', (err, data) => {
  if (err) {
    // Handle error first
    return console.error(err);
  }
  // Process data if no error occurred
  console.log(data);
});
```

## Deep Dive

### Callback Hell (Pyramid of Doom)
When you have multiple asynchronous operations that depend on each other, nesting callbacks inside callbacks creates highly indented code:

```javascript
fetchUser(userId, (err, user) => {
  if (err) return handle(err);
  fetchOrders(user.id, (err, orders) => {
    if (err) return handle(err);
    fetchOrderDetails(orders[0].id, (err, details) => {
      if (err) return handle(err);
      // Process details...
    });
  });
});
```

This nested structure makes code hard to read, difficult to test, and prone to error-handling bugs (such as forgetting to return or catch an error at one of the nesting levels).

### Promisification
**Promisification** is the process of wrapping a callback-based asynchronous function in a function that returns a Promise. This allows you to use clean Promise chains or `async/await` syntax instead of nesting callbacks.

## Visual Explanation

### Execution Flow: Callback Nested Indentation
```text
Synchronous Flow:
[ Start ] ── Line 1 ──> Line 2 ──> Line 3 ──> [ End ]

Asynchronous Nested Callbacks:
[ Line 1: fetchUser() ] ── Registers callback ──> (Offloaded)
                              │
                              ▼ (When resolved)
                      [ Line 2: fetchOrders() ] ── Registers callback ──> (Offloaded)
                                                    │
                                                    ▼ (When resolved)
                                            [ Line 3: fetchDetails() ] ──> Executes ...
```

## Real-World Example
Suppose you run a server that reads a user record, queries their orders, and returns the data as JSON. Using nested callbacks, you write deeply indented code. If you promisify these database calls, you can write flat, readable code that is easier to maintain and debug.

## Code Examples

### Error-First Callbacks, Callback Hell, and Promisification

```javascript
// callback-demo.js
const fs = require('fs');
const { promisify } = require('util');

const filePath = 'example.txt';

// 1. Core Error-First Callback usage
fs.writeFile(filePath, 'Callback Data Payload', (err) => {
  if (err) {
    console.error('Error writing file:', err.message);
    return; // Stop execution
  }
  
  console.log('File written successfully. Commencing read...');
  
  // Nested callback (Pyramid of Doom starts here)
  fs.readFile(filePath, 'utf8', (err, data) => {
    if (err) {
      console.error('Error reading file:', err.message);
      return;
    }
    
    console.log('Read File Data:', data);
    
    // Nested callback level 3
    fs.unlink(filePath, (err) => {
      if (err) {
        console.error('Error deleting file:', err.message);
        return;
      }
      console.log('File deleted cleanly.');
    });
  });
});

// 2. Promisifying Callback Functions manually
function readFilePromise(path, encoding) {
  return new Promise((resolve, reject) => {
    fs.readFile(path, encoding, (err, data) => {
      if (err) {
        reject(err); // Triggers .catch()
      } else {
        resolve(data); // Triggers .then()
      }
    });
  });
}

// 3. Using Node's native util.promisify helper
// This utility converts any standard error-first callback function into a promise-returning function.
const unlinkPromise = promisify(fs.unlink);
```

## Best Practices
* **Always Check for Errors First**: In every callback, handle the `err` object immediately and return early to prevent the rest of the function from executing on invalid data.
* **Avoid Deep Nesting**: Extract nested callbacks into independent, named functions to improve readability and make unit testing easier.
* **Use Promisify**: Convert legacy callback APIs to Promises using Node's native `util.promisify` utility to write cleaner code.

## Interview Questions

### Beginner
* **What is an error-first callback in Node.js?**
  *Answer*: An error-first callback is a standard convention in Node.js where the first argument of the callback function is reserved for an error object (`err`), and subsequent arguments contain the success data. If no error occurs, the first argument is set to `null` or `undefined`.

### Intermediate
* **What is Callback Hell and how do you resolve it?**
  *Answer*: Callback Hell refers to heavily nested and indented callback functions that result from chaining multiple asynchronous operations. It makes code difficult to read and maintain. You can resolve it by modularizing code into separate named functions, wrapping functions in Promises, or using `async/await` syntax.

### Advanced
* **Write a custom function that converts a standard callback-based function into a Promise-based one (implement a basic version of `util.promisify`).**
  *Answer*: 
  ```javascript
  function customPromisify(fn) {
    return function (...args) {
      return new Promise((resolve, reject) => {
        // Append custom error-first callback to arguments
        fn(...args, (err, result) => {
          if (err) {
            reject(err);
          } else {
            resolve(result);
          }
        });
      });
    };
  }
  ```

### Senior Architect
* **Discuss the execution order difference between standard callbacks and Promise callbacks. How do they interact with the event loop's task queues?**
  *Answer*: Standard callbacks (like those passed to `fs.readFile` or network operations) are **macrotasks**. When their underlying I/O operations complete, their callbacks are queued in the Event Loop's I/O queue and execute in a future loop iteration.
  
  Promise callbacks (like those registered in `.then()`) are **microtasks**. When a Promise resolves, its callback is queued in the Promise microtask queue. The microtask queue is checked and drained *immediately* after the currently executing script or task completes, before the Event Loop moves to the next phase. 
  Consequently, Promise callbacks run much earlier than standard I/O callbacks, which is critical to keep in mind when coordinating complex asynchronous sequences.

---
Previous : [17_Streams_Basics.md] | Index : [00_index.md] | Next : [19_Promises.md]
