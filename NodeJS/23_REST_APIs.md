# REST APIs

## What You Will Learn
* The architectural constraints of REST (Representational State Transfer).
* Mapping HTTP methods (GET, POST, PUT, DELETE, PATCH) to CRUD operations.
* Correct utilization of HTTP Status Code categories.
* Designing semantic, resource-oriented URIs.
* Implementing query parameters for filtering, sorting, and pagination.
* Content negotiation using request headers.

## Why This Matters
Building an API is not just about routing requests to functions. Poorly structured endpoints (like `POST /delete-user?id=1` or returning `200 OK` with an error message in the body) break integration standards, make client integration difficult, and bypass caching proxies. Understanding REST standards ensures your APIs are secure, scalable, and easy to consume.

## Theory

### REST Architectural Constraints
REST is an architectural style defined by several constraints:
1. **Statelessness**: Every request from a client must contain all the information needed to understand and process it. The server does not store client session context in its memory.
2. **Client-Server Separation**: The client and server are decoupled; they can evolve independently as long as the interface agreement remains intact.
3. **Cacheability**: Responses must declare whether they are cacheable to optimize network utilization.
4. **Uniform Interface**: Resources are identified in requests using uniform resource identifiers (URIs) and manipulated using standard HTTP methods.

### HTTP Verbs and CRUD Mapping
| Method | CRUD Action | Idempotent? | Safe? | Description |
| :--- | :--- | :--- | :--- | :--- |
| **GET** | Read | Yes | Yes | Fetches a resource. Does not modify state. |
| **POST** | Create | No | No | Creates a new resource. |
| **PUT** | Update (Replace) | Yes | No | Replaces an entire resource. |
| **PATCH** | Update (Partial) | No | No | Partially updates a resource. |
| **DELETE** | Delete | Yes | No | Removes a resource. |

*Note on Idempotence*: An operation is **idempotent** if running it multiple times yields the same state. For instance, sending a `DELETE` request twice has the same effect as sending it once.

## Deep Dive

### HTTP Status Code Selection
Using the correct status codes allows clients to handle responses programmatically:
* **2xx (Success)**:
  * `200 OK`: Standard success response.
  * `201 Created`: Resource successfully created (common response to `POST`).
  * `204 No Content`: Request succeeded, but returns no body (common response to `DELETE`).
* **3xx (Redirection)**:
  * `304 Not Modified`: The resource has not changed; the client should load it from cache.
* **4xx (Client Error)**:
  * `400 Bad Request`: Invalid input or payload errors.
  * `401 Unauthorized`: Client is not authenticated.
  * `403 Forbidden`: Client is authenticated but lacks access rights to the resource.
  * `404 Not Found`: Target resource does not exist.
  * `429 Too Many Requests`: Client has exceeded rate limits.
* **5xx (Server Error)**:
  * `500 Internal Server Error`: Generic unhandled server error.
  * `502 Bad Gateway`: Upstream proxy or server failed to communicate.
  * `503 Service Unavailable`: Server is overloaded or down for maintenance.

## Visual Explanation

### REST Request-Response Cycle and Headers
```text
Client Request:
GET /api/v1/orders?status=shipped&limit=5 HTTP/1.1
Host: api.store.com
Accept: application/json
Authorization: Bearer <Token>

               │
               ▼ (Server Processes REST Routing)
               
Server Response:
HTTP/1.1 200 OK
Content-Type: application/json
Cache-Control: public, max-age=3600

[
  { "id": 101, "item": "Laptop", "status": "shipped" },
  ...
]
```

## Real-World Example
Suppose you design an order management endpoint. The URI should use plural nouns rather than verbs:
* Use `GET /api/v1/orders` to fetch orders (with query parameters like `?status=pending` for filtering).
* Use `POST /api/v1/orders` to create a new order.
* Use `DELETE /api/v1/orders/123` to remove order 123.
* Do not use paths like `/api/v1/getOrders` or `/api/v1/deleteOrder?id=123`.

## Code Examples

### Constructing a Native REST Route Handler

```javascript
// rest-api-router.js
const http = require('http');

// In-memory mock database
const usersDb = [
  { id: 1, name: 'Alice', role: 'admin' },
  { id: 2, name: 'Bob', role: 'user' }
];

const server = http.createServer((req, res) => {
  const method = req.method.toUpperCase();
  const reqUrl = new URL(req.url, `http://${req.headers.host}`);
  const path = reqUrl.pathname;

  // 1. Content Negotiation Check
  const acceptHeader = req.headers['accept'] || '';
  if (acceptHeader && !acceptHeader.includes('application/json') && !acceptHeader.includes('*/*')) {
    res.writeHead(406, { 'Content-Type': 'text/plain' });
    res.end('Not Acceptable (Only JSON is supported)');
    return;
  }

  // Helper to send JSON responses
  const sendJson = (status, payload) => {
    res.writeHead(status, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(payload));
  };

  // 2. Resource Routes
  // Route: GET /users
  if (path === '/users' && method === 'GET') {
    // Implement filtering via query parameters
    const roleFilter = reqUrl.searchParams.get('role');
    let results = usersDb;
    
    if (roleFilter) {
      results = usersDb.filter(u => u.role === roleFilter);
    }
    
    sendJson(200, results);
    return;
  }

  // Route: GET /users/:id
  const matchUserRoute = path.match(/^\/users\/(\d+)$/);
  if (matchUserRoute && method === 'GET') {
    const userId = parseInt(matchUserRoute[1], 10);
    const user = usersDb.find(u => u.id === userId);
    
    if (!user) {
      sendJson(404, { error: 'User not found' });
    } else {
      sendJson(200, user);
    }
    return;
  }

  // Route: POST /users
  if (path === '/users' && method === 'POST') {
    let body = '';
    req.on('data', chunk => body += chunk.toString());
    req.on('end', () => {
      try {
        const payload = JSON.parse(body);
        if (!payload.name || !payload.role) {
          sendJson(400, { error: 'Name and role are required' });
          return;
        }
        const newUser = {
          id: usersDb.length + 1,
          name: payload.name,
          role: payload.role
        };
        usersDb.push(newUser);
        sendJson(201, newUser);
      } catch (err) {
        sendJson(400, { error: 'Invalid JSON format' });
      }
    });
    return;
  }

  // Route not matched
  sendJson(404, { error: 'Route endpoint not found' });
});

server.listen(3000, () => console.log('REST API Server running on port 3000'));
```

## Best Practices
* **Use Plural Nouns for URIs**: Design resource paths using plural nouns (e.g. `/api/v1/products`) rather than actions (e.g. `/api/v1/getProducts`).
* **Handle Errors Consistently**: Always return errors in a standardized JSON payload structure (e.g. `{ "error": "Reason", "code": 404 }`) along with the correct HTTP status code.
* **Support Content Negotiation**: Verify client content preferences using the `Accept` request header and reject requests if you cannot return the requested format.
* **Keep APIs Stateless**: Avoid storing authentication or session context in the server's memory. Pass authorization tokens in request headers instead.

## Interview Questions

### Beginner
* **What is a REST API?**
  *Answer*: A REST API is a web service architecture style built on top of the HTTP protocol. It identifies resources using URIs and manipulates them using standard HTTP methods (GET, POST, PUT, DELETE), returning data in formats like JSON.

### Intermediate
* **What is the difference between PUT and PATCH methods?**
  *Answer*: The `PUT` method replaces the entire representation of a target resource with the new request payload. It is idempotent. The `PATCH` method applies partial modifications to the resource (updating only specific fields). It is not guaranteed to be idempotent.

### Advanced
* **What does "idempotence" mean in the context of HTTP methods, and why are POST operations not idempotent?**
  *Answer*: An HTTP method is idempotent if executing the same request multiple times yields the exact same resource state on the server. `GET`, `PUT`, and `DELETE` are idempotent. `POST` is not idempotent because repeating a `POST` request (e.g. submitting a payment form twice) creates duplicate resources (e.g. two separate transactions or orders) on the server.

### Senior Architect
* **Discuss the API design trade-offs of using JSON API standards versus GraphQL in a microservices ecosystem. When would you veto a migration to GraphQL?**
  *Answer*: 
  * **REST (JSON API)**:
    * *Pros*: Simple to cache using standard CDNs (via HTTP headers like `Cache-Control`), has a small learning curve, and is easy to load-balance.
    * *Cons*: Can suffer from over-fetching or under-fetching data, requiring clients to make multiple round-trip requests.
  * **GraphQL**:
    * *Pros*: Clients can fetch exactly the fields they need in a single request, which is ideal for complex frontend views.
    * *Cons*: Difficult to cache at the network layer because requests use `POST` payloads, and clients can write complex queries that overload the database.
  * *Veto Criteria*: I would veto a migration to GraphQL if:
    1. The application relies heavily on network caching and CDN performance.
    2. The services are lightweight and do not have deeply nested relational queries.
    3. The team lacks database query-depth analysis and cost-limiting middleware to prevent clients from executing resource-heavy nested queries.

---
Previous : [22_Creating_Web_Servers.md] | Index : [00_index.md] | Next : [24_ExpressJS.md]
