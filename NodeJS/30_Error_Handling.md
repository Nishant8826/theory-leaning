# Error Handling

Unhandled errors crash servers and expose sensitive internal details (like database queries, file paths, and dependency stacks) to clients. Standardizing error handling secures your application, prevents crashes, and ensures that clients receive consistent error payloads that are easy to debug.

### Operational vs. Programmer Errors
In backend architecture, errors are divided into two main categories:
1. **Operational Errors**: Predictable failures that occur in correct programs (e.g. invalid user input, database timeouts, missing resource IDs, network failures). These should be handled gracefully by returning the correct HTTP status code without crashing the server.
2. **Programmer Errors**: Unanticipated bugs that result from incorrect code (e.g. calling `undefined` functions, syntax errors, pointer dereferences, passing incorrect argument types). These indicate an unstable application state; the server should print the error stack trace and restart immediately.

### Custom Exception Class: `AppError`
To manage operational errors consistently, create a custom exception class `AppError` that inherits from JavaScript's native `Error` class. This class attaches properties like `statusCode`, `isOperational`, and `errorCode` directly to the error object.

## Deep Dive

### Global Error Handling Middleware
In Express, whenever you pass an argument to `next(err)`, the framework stops running the current middleware chain and routes the error down the stack until it reaches the first middleware declared with exactly four arguments: `(err, req, res, next)`.

This global handler processes the error in a single location:
* **Logging**: Logs error details (like stack traces) to your internal logging pipeline.
* **Client Response**: Sanitizes error messages for the client.
* **State Check**: Checks if the error is a Programmer Error. If so, it triggers a graceful shutdown to restart the process.

## Visual Explanation

### Express Error Propagation Pipeline
```text
  [ Route Handler / Middleware ] ── Exception occurred! ──> Call: next(err)
                                                                │
                                                                ▼ (Routes down the stack)
+-------------------------------------------------------------------------------+
| [ Global Error Handling Middleware (err, req, res, next) ]                    |
|   1. Log details to system stdout/files                                       |
|   2. Check error type:                                                        |
|      ├── Operational Error?                                                   |
|      │     └── Send sanitized JSON (statusCode, message)                      |
|      └── Programmer Error?                                                    |
|            ├── Dev Mode  ──> Return full Stack Trace                          |
|            └── Prod Mode ──> Return generic 500 error ──> Graceful Shutdown   |
+-------------------------------------------------------------------------------+
```

## Real-World Example
Consider an endpoint that fetches a user profile. If the database query fails due to an invalid user ID, the controller catches the error, wraps it in an `AppError` with status `404 Not Found`, and calls `next(err)`. The global handler logs the error details, strips out internal stack traces, and returns a clean JSON error response, keeping the controller codebase clean.

## Code Examples

### Custom AppError Class and Global Error Handler Middleware

```javascript
// utils/AppError.js
class AppError extends Error {
  constructor(message, statusCode, errorCode = 'INTERNAL_ERROR') {
    super(message);
    
    this.statusCode = statusCode;
    this.errorCode = errorCode;
    this.isOperational = true; // Identifies operational errors

    // Captures the stack trace, excluding this constructor call
    Error.captureStackTrace(this, this.constructor);
  }
}
module.exports = AppError;
```

```javascript
// app.js
const express = require('express');
const AppError = require('./utils/AppError');

const app = express();
app.use(express.json());

// Helper wrapper for async functions to catch rejections automatically
const asyncHandler = (fn) => (req, res, next) => {
  Promise.resolve(fn(req, res, next)).catch(next);
};

// Route throwing an Operational Error
app.get('/api/users/:id', asyncHandler(async (req, res, next) => {
  const userId = req.params.id;
  
  if (userId === '0') {
    // Throws a custom, validated operational error
    throw new AppError('User profile does not exist.', 404, 'USER_NOT_FOUND');
  }
  
  res.json({ id: userId, username: 'Alice' });
}));

// Route throwing a Programmer Error (calling undefined function)
app.get('/api/buggy', asyncHandler(async (req, res) => {
  nonExistentFunction(); // Throws ReferenceError (Programmer Error)
  res.send('Done');
}));

// Global Error Handling Middleware
app.use((err, req, res, next) => {
  err.statusCode = err.statusCode || 500;
  err.errorCode = err.errorCode || 'INTERNAL_SERVER_ERROR';

  // Log the full stack trace for internal monitoring
  console.error(`[ERROR LOG] ${err.errorCode}:`, err.stack);

  // Development vs. Production Output Formatting
  if (process.env.NODE_ENV === 'development') {
    res.status(err.statusCode).json({
      status: 'error',
      errorCode: err.errorCode,
      message: err.message,
      stack: err.stack, // Include stack trace in development
      error: err
    });
  } else {
    // Production Mode (Sanitize responses)
    if (err.isOperational) {
      // Send validated operational errors directly to the client
      res.status(err.statusCode).json({
        status: 'error',
        errorCode: err.errorCode,
        message: err.message
      });
    } else {
      // Hide stack trace and internal details for programmer errors
      res.status(500).json({
        status: 'error',
        errorCode: 'INTERNAL_SERVER_ERROR',
        message: 'Something went wrong on the server.'
      });
    }
  }
});

app.listen(3000, () => console.log('Error handling server running on port 3000'));
```

## Best Practices
* **Use AppError for Known Failures**: Use custom `AppError` objects to represent operational failures (like validation errors or missing resources), specifying correct status codes and error keys.
* **Sanitize Production Errors**: Never send internal stack traces or database errors (like SQL strings or mongo queries) to clients in production to prevent security leaks.
* **Wrap Async Handlers**: Use an asynchronous wrapper function (like `asyncHandler`) or database wrapper blocks to catch async errors and pass them to `next(err)` automatically.
* **Restart on Programmer Errors**: If a programmer error occurs (such as an uncaught exception), log the details, shut down gracefully, and let your container orchestrator (e.g. Kubernetes) restart the container.

## Interview Questions

**Q:** What is the difference between an operational error and a programmer error?

> **Answer:**
> Operational errors are predictable failures that can occur in correct programs (e.g., database timeouts, missing IDs, or validation errors). They should be handled gracefully. Programmer errors are unexpected bugs caused by incorrect code (e.g., syntax errors, reference errors, or undefined functions). They require logging and restarting the process.

**Q:** How do you define a global error handler in Express?

> **Answer:**
> You define global error handler middleware by declaring a function that takes exactly four arguments: `(err, req, res, next)`. You then register this middleware at the very end of your middleware chain, after all route definitions.

**Q:** Why do try/catch blocks fail to catch errors thrown in asynchronous callbacks or nested timer loops in Express, and how do you resolve this?

> **Answer:**
> Try/catch blocks only catch errors thrown in the same execution context and call stack. If an error is thrown inside an asynchronous callback (such as inside a `setTimeout` loop or database client event handler) after the main call stack has cleared, the try/catch block will miss it.
> To resolve this, ensure all asynchronous execution paths use Promises or `async/await` and pass caught errors to `next(err)` explicitly.

**Q:** How would you architecture a zero-crash, self-healing process recovery system inside a Node.js cluster when encountering uncaught programmer errors?

> **Answer:**
> To build a self-healing process recovery system:
> 1. Register process-level event listeners for `uncaughtException` and `unhandledRejection`:
> ```javascript
> process.on('uncaughtException', (err) => {
> logger.error('CRITICAL UNCAUGHT EXCEPTION:', err);
> gracefulShutdown(1); // Exit with failure code
> });
> ```
> 2. Implement a `gracefulShutdown` function that:
> - Instructs load balancers to stop routing traffic to this instance.
> - Sets a timeout (e.g. 10-20 seconds) to force-exit the process.
> - Attempts to close active database pools and server connections.
> - Exits the process with code `1`.
> 3. Deploy the application inside a container orchestrator (like Kubernetes) or use process managers (like PM2) configured to automatically launch a fresh, healthy container instance when a container exits, ensuring zero downtime.

---
Previous : [29_Validation.md](29_Validation.md) | Index : [00_index.md](00_index.md) | Next : [31_Logging.md](31_Logging.md)
