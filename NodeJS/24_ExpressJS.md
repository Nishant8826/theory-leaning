# Express.js

## What You Will Learn
* The structural components of an Express.js application.
* Creating routes and using route parameters (`req.params`, `req.query`).
* Grouping routes logically using `express.Router()`.
* Mounting static file directories and mounting sub-applications.
* Under-the-hood routing optimizations.

## Why This Matters
Express is the most popular framework in the Node.js ecosystem. While it simplifies building APIs, a poor understanding of its routing mechanics can lead to duplicate route definitions, slow route lookups as the app grows, and unhandled errors that crash the server. Knowing how to structure Express routers keeps your codebase clean and fast.

## Theory

### The Core Express Architecture
Express is a minimalist, unopinionated routing and middleware web framework. Its architecture is built around three core concepts:
1. **The Application Instance (`app`)**: The main controller object that binds settings, routes, and starts the HTTP listener.
2. **The Middleware Pipeline**: An array of callback functions executed sequentially during the request-response cycle.
3. **The Router**: A routing isolation system. You can define routes in sub-routers and mount them onto the main application, organizing your code modularly.

### Request & Response Wrappers
Express wraps Node's native `IncomingMessage` and `ServerResponse` objects, extending them with helper properties:
* **`req.params`**: Key-value parameters parsed from the URL path (e.g. `/users/:id` yields `{ id: "123" }`).
* **`req.query`**: Key-value query parameters parsed from the URL search string (e.g. `?status=active` yields `{ status: "active" }`).
* **`res.json(data)`**: Serializes the data to JSON, sets the correct `Content-Type: application/json` header, and ends the response write stream.

## Deep Dive

### Express Routing Engine Internals
When you register a route (e.g., `app.get('/users', callback)`), Express instantiates a new `Route` object and pushes it to an internal stack array (`app._router.stack`).
* **Regex Compilation**: Express compiles each route string into a Regular Expression using the `path-to-regexp` library.
* **Lookup Overhead**: When a request arrives, Express iterates sequentially through its stack, checking if the request path matches the compiled regular expression of each route. If you define thousands of routes directly on the main application, this search loop can degrade request routing performance.

Using `express.Router()` groups related routes into sub-stacks, reducing the search path depth and improving routing speed.

## Visual Explanation

### Express Routing Resolution Stack
```text
Request Path: GET /api/v1/users/5

Main Router Stack Loop:
[ Stack Item 1: express.static ] ── Check path '/api/v1/users/5' ──> No match, skip.
[ Stack Item 2: body-parser ]     ── Runs middleware, modifies req.body.
[ Stack Item 3: API Router ]      ── Matches path prefix '/api/v1/' ──> ENTER Sub-Router stack.
                                          │
                                          ▼
                               [ Sub-Router Stack Loop ]
                               ├── [ Route: GET /health ] ──> No match, skip.
                               └── [ Route: GET /users/:id ] ──> MATCH! Execute controller callback.
```

## Real-World Example
Consider an application that has admin panels, user settings, and billing systems. Instead of writing all routes in a single large `server.js` file, you can create separate routers (`adminRouter.js`, `billingRouter.js`) and mount them on the main app using `app.use('/admin', adminRouter)`. This isolates routing logic and simplifies maintenance.

## Code Examples

### Structuring Route Parameters, Routers, and Static Files

```javascript
// express-app.js
const express = require('express');
const path = require('path');

const app = express();

// 1. Mount standard body parsing middleware
app.use(express.json()); // Parses application/json payloads

// 2. Serve static assets from public directory
app.use('/static', express.static(path.join(__dirname, 'public')));

// 3. Create a Sub-Router (modular routes)
const apiRouter = express.Router();

// Define route with parameters (e.g. GET /api/v1/products/42)
apiRouter.get('/products/:id', (req, res) => {
  const productId = req.params.id;
  const showDetails = req.query.details === 'true'; // Access query params

  res.status(200).json({
    id: productId,
    name: `Product ${productId}`,
    detailed: showDetails
  });
});

apiRouter.post('/products', (req, res) => {
  const payload = req.body; // Accessed thanks to express.json() middleware
  res.status(201).json({
    message: 'Product created',
    data: payload
  });
});

// 4. Mount the Sub-Router onto the Main Application
app.use('/api/v1', apiRouter);

// 5. Global Catch-all for undefined routes
app.use('*', (req, res) => {
  res.status(404).json({ error: 'Endpoint resource not found' });
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Express Server running on port ${PORT}`);
});
```

## Best Practices
* **Use express.Router()**: Divide your application routes into logical sub-routers to keep your codebase clean and optimize route lookup speeds.
* **Mount body parsers early**: Place body parsing middleware (`express.json()`, `express.urlencoded()`) at the top of your middleware chain to ensure payloads are parsed before reaching your route handlers.
* **Do Not serve heavy files via Express**: Use reverse proxies like Nginx or cloud storage CDNs to serve static files in production. Express is not optimized for heavy static file I/O.

## Interview Questions

### Beginner
* **What is the purpose of `express.Router()`?**
  *Answer*: `express.Router()` creates modular, isolated route handlers. You can define routes on a sub-router and mount it on a path prefix in the main application, helping to organize the codebase.

### Intermediate
* **How do you access path variables and query string parameters in Express?**
  *Answer*: Path variables (e.g. `/users/:id`) are accessed via `req.params.id`. Query string parameters (e.g. `?status=active`) are accessed via `req.query.status`.

### Advanced
* **Explain how Express processes routing lookups under the hood, and how defining too many flat routes can degrade performance.**
  *Answer*: Express maintains an internal stack array (`app._router.stack`) of route and middleware entries. Each route is compiled into a regular expression using the `path-to-regexp` library. 
  When a request arrives, Express loops through this stack sequentially and runs matches against the path. If you define thousands of flat routes directly on the main application, Express must perform hundreds of regular expression evaluations for every request, which blocks the event loop and degrades routing performance. Using nested sub-routers limits search paths and reduces this overhead.

### Senior Architect
* **How would you architecture a dynamic sub-app mounting pattern in a multi-tenant Node.js application, where separate tenants load isolated routing configurations dynamically at runtime?**
  *Answer*: To mount sub-apps dynamically:
  1. Define each tenant's API as an isolated Express application class or module.
  2. Implement a master Express gateway application.
  3. Create a tenant-resolution middleware that identifies the tenant based on the request domain or headers (e.g., `tenant-a.domain.com` or `X-Tenant-ID`).
  4. Cache the initialized tenant sub-applications in a map in memory.
  5. Route traffic dynamically using a custom routing handler that delegates request execution to the resolved sub-app using:
     ```javascript
     app.use((req, res, next) => {
       const tenantApp = getTenantSubApp(req.tenantId);
       tenantApp(req, res, next); // Delegates execution
     });
     ```
  This architecture isolates routes, middleware configurations, and databases for each tenant while sharing a single parent process listener.

---
Previous : [23_REST_APIs.md] | Index : [00_index.md] | Next : [25_Middleware.md]
