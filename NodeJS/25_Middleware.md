# Middleware

## What You Will Learn
* The design and purpose of the Middleware pattern.
* The five main categories of middleware in Express.
* Why the registration order of middleware is critical.
* Implementing custom middleware and handling errors using `next(err)`.

## Why This Matters
Middleware is the backbone of Express. Authentication, input validation, logging, and rate limiting are all written as middleware. If you do not understand how the middleware execution chain works, you will encounter bugs where requests hang indefinitely, authentication checks are bypassed, or errors fail to trigger proper response handlers.

## Theory

### What is Middleware?
**Middleware** functions are code blocks that run sequentially during the request-response cycle. They have access to the request object (`req`), the response object (`res`), and the next middleware function in the execution chain (`next`).

A middleware function can:
* Execute any code.
* Make changes to the request and response objects (e.g. adding user data to `req.user`).
* End the request-response cycle (e.g. sending a `403 Forbidden` response).
* Call the next middleware in the queue by calling `next()`.

If a middleware does not end the request-response cycle or call `next()`, the request hangs and the client eventually receives a gateway timeout error.

### The Five Categories of Middleware
1. **Application-level**: Bound to the app instance using `app.use()` or `app.METHOD()`.
2. **Router-level**: Bound to an instance of `express.Router()` using `router.use()`.
3. **Built-in**: Bundled with Express (e.g. `express.json()`, `express.static()`).
4. **Error-handling**: Declared with four arguments: `(err, req, res, next)`.
5. **Third-party**: Installed from npm (e.g., `cookie-parser`, `morgan`, `cors`).

## Deep Dive

### The Order of Execution
Express runs middleware in the exact order they are registered in your code.
* **Pre-processing**: Middleware like body parsers and loggers must be registered at the top of your file to ensure they parse payloads and log metadata before requests reach your routes.
* **Authentication**: Authentication middleware must run before route controllers to prevent unauthorized clients from accessing sensitive handlers.
* **Error Handlers**: Error-handling middleware must be registered at the very end of your file, after all route definitions, so it can catch exceptions passed down the chain.

## Visual Explanation

### The Middleware Pipeline
```text
Client Request ──> [ Middleware 1: Logger ] ── next() ──> [ Middleware 2: Auth Check ]
                                                                   │
                                                                   ├── (Auth fails?)
                                                                   │     ├── YES ──> Send 401 Response (End)
                                                                   │     └── NO  ──> next()
                                                                   ▼
                                                          [ Route Controller ] ──> res.json() (End)
                                                                   │
                                                           (Exception thrown)
                                                                   ▼
                                                      [ Error Handler Middleware ] ──> Send 500 Response (End)
```

## Real-World Example
Consider building an API that logs request paths and verifies authentication. You write a global logger middleware at the top of the file to trace every request. Then, you write an authentication middleware and apply it only to `/api/secure/*` paths, ensuring public routes (like `/home`) remain accessible while protected routes are secured.

## Code Examples

### Writing Custom and Error-Handling Middleware

```javascript
// middleware-pipeline.js
const express = require('express');
const app = express();

app.use(express.json());

// 1. Custom Application-Level Middleware: Request Logger
const requestLogger = (req, res, next) => {
  const timestamp = new Date().toISOString();
  console.log(`[${timestamp}] ${req.method} ${req.url}`);
  
  // Custom request mutation (add request start time)
  req.startTime = Date.now();
  
  next(); // Pass control to the next middleware in the stack
};
app.use(requestLogger);

// 2. Custom Router-Level Middleware: Simple Authentication Check
const authenticate = (req, res, next) => {
  const apiKey = req.headers['x-api-key'];
  
  if (apiKey === 'secure-key-123') {
    req.user = { id: 101, username: 'admin' }; // Attach data to request
    next();
  } else {
    // End the request-response cycle immediately
    res.status(401).json({ error: 'Unauthorized: Invalid API Key' });
  }
};

// Apply 'authenticate' middleware only to this route
app.get('/api/dashboard', authenticate, (req, res) => {
  const latency = Date.now() - req.startTime; // Read parameter added by Logger
  res.json({
    message: `Welcome ${req.user.username}`,
    latency: `${latency}ms`
  });
});

// 3. Simulating exceptions for Error-Handling
app.get('/api/broken', (req, res, next) => {
  try {
    throw new Error('Database connection failed.');
  } catch (err) {
    // Pass the error down the pipeline to the error handler
    next(err); 
  }
});

// 4. Global Error-Handling Middleware
// MUST have 4 arguments: (err, req, res, next)
const globalErrorHandler = (err, req, res, next) => {
  console.error('[GLOBAL-ERROR-HANDLER]:', err.message);
  
  res.status(500).json({
    error: 'Internal Server Error',
    message: process.env.NODE_ENV === 'development' ? err.message : 'Something went wrong.'
  });
};
app.use(globalErrorHandler); // Registered at the very end

app.listen(3000, () => console.log('Middleware server running on port 3000'));
```

## Best Practices
* **Always Call `next()` or Send Response**: Ensure every middleware execution path either calls `next()`, calls `next(err)` to forward an error, or ends the request by sending a response.
* **Keep Error Handlers at the End**: Always register your error-handling middleware after all routing definitions.
* **Use next(err) for Exceptions**: When an exception occurs in an asynchronous block, pass the error to `next(err)` to ensure Express routes it to the error handler.

## Interview Questions

### Beginner
* **What is middleware in Express.js?**
  *Answer*: Middleware functions are functions that execute sequentially during the request-response cycle of an Express application. They have access to the request object (`req`), response object (`res`), and the `next` middleware function in the execution chain.

### Intermediate
* **Why must error-handling middleware be registered last in the Express app definition?**
  *Answer*: Express executes middleware and routes sequentially in the order they are defined. If you register error-handling middleware before routing definitions, it will not catch exceptions thrown in those routes because they sit further down the execution stack.

### Advanced
* **How does Express distinguish standard middleware from error-handling middleware?**
  *Answer*: Express checks the function signature (specifically the number of arguments) using JavaScript's `Function.prototype.length` property. Standard middleware functions take 2 or 3 arguments (`(req, res, next)`), while error-handling middleware must declare exactly 4 arguments (`(err, req, res, next)`). If you declare fewer than 4 arguments, Express treats the function as standard middleware, and it will not receive thrown errors.

### Senior Architect
* **Discuss how asynchronous error handling changes between Express 4 and Express 5 under the hood. How do you implement a robust global async-error-catcher wrapper in Express 4?**
  *Answer*: 
  * **Express 4**: Does not catch unhandled rejections or errors thrown in asynchronous code paths (such as `await` or callbacks) automatically. If an error is thrown inside an asynchronous block, it bypasses the Express router stack and triggers an `unhandledRejection` event. To handle errors, you must wrap async code in `try/catch` and pass the error to `next(err)` manually.
  * **Express 5**: Automatically catches rejected Promises and forwards them to the error-handling middleware.
  
  To handle this cleanly in Express 4, you can write an asynchronous wrapper helper function (often called `asyncHandler`):
  ```javascript
  const asyncHandler = (fn) => (req, res, next) => {
    Promise.resolve(fn(req, res, next)).catch(next);
  };

  // Usage in routes
  app.get('/api/users', asyncHandler(async (req, res) => {
    const users = await db.fetchUsers();
    res.json(users); // If fetchUsers rejects, catch(next) forwards the error automatically
  }));
  ```
  This wrapper ensures all asynchronous rejections are forwarded to your error-handling middleware without cluttering controllers with duplicate `try/catch` blocks.

---
Previous : [24_ExpressJS.md] | Index : [00_index.md] | Next : [26_Routing.md]
