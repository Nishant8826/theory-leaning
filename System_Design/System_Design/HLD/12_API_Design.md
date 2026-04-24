# 📌 API Design

## 🧠 Concept Explanation (Story Format)

APIs are the language your services speak to each other. You've used Postman to test APIs. You've built REST APIs with Express.js. But have you thought about what makes an API GREAT?

A poorly designed API:
- Confuses developers (who has to use it?)
- Breaks existing clients when you make changes
- Leaks internal system details
- Has no consistent error handling
- Gets overwhelmed by heavy users (no rate limiting)

A well-designed API is like a well-designed TV remote — intuitive, consistent, doesn't expose the TV's internal circuitry, and works reliably every time.

---

## 🏗️ Basic Design (Naive)

```javascript
// Typical beginner Node.js API — BAD design patterns

app.get('/getData', ...);         // Vague name
app.post('/doSomething', ...);    // Not RESTful
app.get('/getAllUsersEvenDeleted', ...); // Leaks implementation
// No versioning → breaking changes break clients
// No consistent error format
// Different response shapes for different endpoints
```

---

## ⚡ Optimized Design

```
API Design Principles:
1. RESTful resource naming
2. Versioning (/v1/, /v2/)
3. Consistent response format
4. Proper HTTP status codes
5. Pagination for collections
6. Clear error messages
7. Input validation
8. Rate limiting
9. Authentication on every endpoint
10. API documentation (OpenAPI/Swagger)
```

---

## 🔍 Key Components

### REST API Design

**Resource Naming Rules:**
```
Nouns, not verbs:
✅ GET    /users              → List all users
✅ POST   /users              → Create a user
✅ GET    /users/123          → Get user 123
✅ PUT    /users/123          → Replace user 123 completely
✅ PATCH  /users/123          → Update part of user 123
✅ DELETE /users/123          → Delete user 123

Nested resources:
✅ GET    /users/123/posts    → Posts belonging to user 123
✅ POST   /users/123/posts    → Create post for user 123
✅ GET    /posts/456/comments → Comments on post 456

❌ GET /getUser?id=123      ← Verb in URL
❌ POST /deleteUser/123     ← Wrong HTTP method
❌ GET /user_posts/123      ← Inconsistent naming
```

**HTTP Status Codes:**
```
2xx - Success
  200 OK              → Successful GET, PUT, PATCH
  201 Created         → Successful POST (resource created)
  202 Accepted        → Request accepted but processing async
  204 No Content      → Successful DELETE (no body returned)

4xx - Client Errors (YOUR fault)
  400 Bad Request     → Invalid input
  401 Unauthorized    → Not logged in
  403 Forbidden       → Logged in but no permission
  404 Not Found       → Resource doesn't exist
  409 Conflict        → Duplicate entry (email already taken)
  422 Unprocessable   → Validation errors
  429 Too Many Reqs   → Rate limit exceeded

5xx - Server Errors (SERVER fault)
  500 Internal Error  → Unhandled exception
  502 Bad Gateway     → Upstream service failed
  503 Service Unavail → Server is down
  504 Gateway Timeout → Upstream service timed out
```

---

### Consistent Response Format

```javascript
// ✅ Standard response format for ALL endpoints

// Success response
{
  "success": true,
  "data": {
    "id": "123",
    "name": "Alice",
    "email": "alice@example.com"
  },
  "meta": {
    "requestId": "req_abc123",
    "timestamp": "2024-01-15T10:30:00Z"
  }
}

// Error response
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Email is already taken",
    "details": [
      { "field": "email", "message": "Must be unique" }
    ]
  },
  "meta": {
    "requestId": "req_abc123",
    "timestamp": "2024-01-15T10:30:00Z"
  }
}

// Paginated list response
{
  "success": true,
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 500,
    "hasNext": true,
    "nextCursor": "cursor_xyz"  // For cursor-based pagination
  }
}
```

**Node.js Response Helper:**
```javascript
// helpers/response.js
const sendSuccess = (res, data, statusCode = 200, meta = {}) => {
  res.status(statusCode).json({
    success: true,
    data,
    meta: { requestId: res.locals.requestId, timestamp: new Date().toISOString(), ...meta }
  });
};

const sendError = (res, code, message, statusCode = 400, details = []) => {
  res.status(statusCode).json({
    success: false,
    error: { code, message, details },
    meta: { requestId: res.locals.requestId, timestamp: new Date().toISOString() }
  });
};

// Usage in routes:
app.get('/users/:id', async (req, res) => {
  const user = await userService.getUser(req.params.id);
  if (!user) return sendError(res, 'NOT_FOUND', 'User not found', 404);
  sendSuccess(res, user);
});
```

---

### API Versioning

```javascript
// ✅ URL-based versioning (most common)
app.use('/api/v1', v1Router);
app.use('/api/v2', v2Router);

// v1: /api/v1/users returns { name: "Alice" }
// v2: /api/v2/users returns { firstName: "Alice", lastName: "Smith" }
// Both work simultaneously! Old clients use v1, new clients use v2.

// Route setup:
const v1Router = express.Router();
v1Router.get('/users/:id', userControllerV1.getUser);

const v2Router = express.Router();
v2Router.get('/users/:id', userControllerV2.getUser);
```

---

### Pagination

```javascript
// ❌ Offset-based pagination (problematic for large datasets)
// GET /posts?page=5&limit=20
app.get('/posts', async (req, res) => {
  const page = parseInt(req.query.page) || 1;
  const limit = parseInt(req.query.limit) || 20;
  const offset = (page - 1) * limit;
  
  // Problem: If new posts are added, page 2 may repeat posts from page 1!
  // Problem: "OFFSET 10000000" is SLOW — DB must skip 10M rows!
  const posts = await db.query('SELECT * FROM posts LIMIT $1 OFFSET $2', [limit, offset]);
  sendSuccess(res, posts.rows, 200, { page, limit });
});

// ✅ Cursor-based pagination (scalable and consistent)
// GET /posts?limit=20&cursor=post_id_abc123
app.get('/posts', async (req, res) => {
  const limit = parseInt(req.query.limit) || 20;
  const cursor = req.query.cursor; // ID of last item seen
  
  let query, params;
  if (cursor) {
    query = 'SELECT * FROM posts WHERE id < $1 ORDER BY id DESC LIMIT $2';
    params = [cursor, limit + 1]; // Fetch 1 extra to know if there's next page
  } else {
    query = 'SELECT * FROM posts ORDER BY id DESC LIMIT $1';
    params = [limit + 1];
  }
  
  const posts = await db.query(query, params);
  const hasNext = posts.rows.length > limit;
  const items = posts.rows.slice(0, limit);
  
  sendSuccess(res, items, 200, {
    hasNext,
    nextCursor: hasNext ? items[items.length - 1].id : null
  });
});
```

---

### Input Validation

```javascript
const Joi = require('joi');

const createUserSchema = Joi.object({
  name: Joi.string().min(2).max(100).required(),
  email: Joi.string().email().required(),
  password: Joi.string().min(8).pattern(/^(?=.*[A-Z])(?=.*[0-9])/).required(),
  age: Joi.number().integer().min(13).max(120).optional()
});

app.post('/users', async (req, res) => {
  const { error, value } = createUserSchema.validate(req.body, { abortEarly: false });
  
  if (error) {
    return sendError(res, 'VALIDATION_ERROR', 'Invalid input', 422,
      error.details.map(d => ({ field: d.path[0], message: d.message }))
    );
  }
  
  const user = await userService.create(value);
  sendSuccess(res, user, 201);
});
```

---

## ⚖️ Trade-offs

| REST | GraphQL | gRPC |
|------|---------|------|
| Simple, universal | Flexible queries | High performance |
| Multiple endpoints | Single endpoint | Binary protocol |
| Over/under-fetching | Exact data needed | Strong typing |
| Easy to cache | Complex caching | Not browser-native |
| Great for public APIs | Great for complex UIs | Great for microservices |

**Our stack recommendation:**
- **REST:** Public APIs, React/Next.js to Node.js
- **GraphQL:** Complex frontend data requirements (consider Apollo)
- **gRPC:** Internal microservice-to-microservice communication

---

## 📊 Scalability Discussion

### API Gateway Pattern

```
React/Next.js
      ↓
AWS API Gateway   ← Single entry point
      ↓ routes to:
  /auth/*   → Auth Service (Node.js)
  /users/*  → User Service (Node.js)
  /posts/*  → Post Service (Node.js)
  /payment/*→ Payment Service (Node.js)

AWS API Gateway provides:
- Rate limiting per API key
- Authentication (JWT validation)
- Request/response transformation
- Logging to CloudWatch
- Caching responses (TTL-based)
- CORS handling
```

---

## 💼 Interview Questions (WITH SOLUTIONS)

### Q1: What are the principles of RESTful API design?

**Solution:**
REST (Representational State Transfer) has 6 constraints:
1. **Client-Server:** UI and data storage are separate. React doesn't know how data is stored.
2. **Stateless:** Each request contains all info needed (JWT token in header). Server doesn't store session.
3. **Cacheable:** Responses can be cached. Use `Cache-Control` headers properly.
4. **Uniform Interface:** Resources identified by URLs. Standard HTTP methods. Consistent format.
5. **Layered System:** Client doesn't know if it's talking to server or load balancer.
6. **Code-on-Demand (optional):** Server can send executable code (rarely used).

Practical REST design rules:
- Use nouns for resources (not verbs)
- Use plural nouns (`/users` not `/user`)
- Use HTTP methods correctly (GET=read, POST=create, PUT=replace, PATCH=update, DELETE=remove)
- Consistent response format
- Proper HTTP status codes

---

### Q2: What is the difference between PUT and PATCH?

**Solution:**
- **PUT:** Replace the ENTIRE resource with the provided data. Missing fields are set to null/default.
- **PATCH:** Update only the provided fields. Other fields remain unchanged.

```javascript
// User: { name: "Alice", email: "alice@ex.com", bio: "Developer" }

// PUT /users/123 with { name: "Alice Smith" }
// Result: { name: "Alice Smith", email: null, bio: null }  ← email and bio WIPED!

// PATCH /users/123 with { name: "Alice Smith" }
// Result: { name: "Alice Smith", email: "alice@ex.com", bio: "Developer" }  ← Only name changed

// In Node.js:
app.patch('/users/:id', async (req, res) => {
  const allowedFields = ['name', 'bio', 'avatar'];
  const updates = Object.fromEntries(
    Object.entries(req.body).filter(([key]) => allowedFields.includes(key))
  );
  // Only update provided fields, leave others alone
  await db.query(
    'UPDATE users SET ' + Object.keys(updates).map((k, i) => `${k} = $${i+1}`).join(', ') + 
    ' WHERE id = $' + (Object.keys(updates).length + 1),
    [...Object.values(updates), req.params.id]
  );
});
```

---

### Q3: How do you design an API that won't break existing clients when you add features?

**Solution:**
**Backward compatibility rules:**
1. **Never remove fields** from responses — clients may depend on them
2. **Never rename fields** — same as removing + adding
3. **Never change field types** — string → number breaks parsing
4. **Always add new optional fields** — clients that don't know about them just ignore them
5. **Use versioning** for breaking changes: `/v1/users` → `/v2/users`

```javascript
// ✅ Safe: Adding new optional field
// v1 response: { id: "123", name: "Alice" }
// v2 response: { id: "123", name: "Alice", firstName: "Alice", lastName: "Smith" }
// Old clients ignore firstName, lastName. New clients use them.

// ❌ Breaking: Renaming field
// v1 response: { id: "123", name: "Alice" }
// v2 response: { id: "123", fullName: "Alice" }  ← Breaks old clients expecting "name"!

// Version deprecation strategy:
// v1: Keep working for 12 months after v2 launch
// Add deprecation header to v1 responses:
res.setHeader('Deprecation', 'true');
res.setHeader('Sunset', 'Sat, 31 Dec 2025 23:59:59 GMT');
```

---

### Q4: What is idempotency and why does it matter for APIs?

**Solution:**
An operation is **idempotent** if calling it multiple times produces the same result as calling it once.

```
GET    → Always idempotent (reading doesn't change state)
PUT    → Idempotent (replacing resource with same data = same result)
DELETE → Idempotent (deleting deleted resource = still deleted)
PATCH  → Usually idempotent (depends on implementation)
POST   → NOT idempotent (calling twice creates two resources!)
```

Why it matters: Network retries! If a request fails, clients retry. If the operation is not idempotent, you might create duplicate orders, charge users twice, etc.

```javascript
// Making POST idempotent with Idempotency Keys:
app.post('/payments', async (req, res) => {
  const idempotencyKey = req.headers['idempotency-key']; // UUID from client
  
  if (!idempotencyKey) return sendError(res, 'MISSING_KEY', 'Idempotency-Key required', 400);
  
  // Check if we've seen this key before
  const existing = await redis.get(`idem:${idempotencyKey}`);
  if (existing) {
    // Return cached response — don't process again!
    return res.json(JSON.parse(existing));
  }
  
  // Process the payment
  const payment = await processPayment(req.body);
  
  // Cache the response for 24 hours
  await redis.setex(`idem:${idempotencyKey}`, 86400, JSON.stringify(payment));
  
  sendSuccess(res, payment, 201);
});
```

---

### Q5: When would you choose GraphQL over REST?

**Solution:**
Choose GraphQL when:
1. **Frontend needs flexible queries:** Mobile app needs `{ name, avatar }`, web needs `{ name, email, bio, posts { title } }` — with REST you either over-fetch or need multiple endpoints.
2. **Complex data relationships:** Social graph, nested data that would require multiple REST calls.
3. **Multiple clients with different data needs:** GraphQL lets each client specify exactly what it needs.
4. **Rapid iteration:** Add new fields without creating new endpoints or versions.

Choose REST when:
1. **Public API:** REST is universally understood, easier for third-party developers.
2. **Simple CRUD operations:** No complex data relationships.
3. **Caching is critical:** REST responses are easily cached by CDNs (GraphQL POST requests are not).
4. **Streaming or file uploads:** REST handles these natively.

For our Instagram-like app: REST for public API + GraphQL for complex internal frontend needs.

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem 1: Design the API for a Twitter-like app

**Solution:**
```
Base URL: https://api.twitter-clone.com/v1

Authentication:
  POST /auth/register    → { email, password, username }
  POST /auth/login       → { email, password } → { token }
  POST /auth/refresh     → Refresh JWT token
  DELETE /auth/logout    → Invalidate token

Tweets:
  GET    /tweets              → Get public timeline (paginated, cursor-based)
  POST   /tweets              → Create tweet { content, mediaUrls? }
  GET    /tweets/:id          → Get single tweet
  DELETE /tweets/:id          → Delete tweet (owner only)
  GET    /tweets/:id/replies  → Get replies (paginated)

Users:
  GET    /users/:username        → Get user profile
  PATCH  /users/me              → Update my profile
  GET    /users/:username/tweets → Get user's tweets
  GET    /users/me/feed          → Get personalized feed (cursor-based)

Social:
  POST   /users/:username/follow   → Follow user
  DELETE /users/:username/follow   → Unfollow user
  GET    /users/:username/followers → List followers
  GET    /users/:username/following → List following

Interactions:
  POST   /tweets/:id/like    → Like a tweet
  DELETE /tweets/:id/like    → Unlike a tweet
  POST   /tweets/:id/retweet → Retweet

Search:
  GET /search?q=react&type=tweets,users&cursor=xxx
```

---

### Problem 2: Your API has inconsistent error responses. Different endpoints return different error formats. How do you fix it?

**Solution:**
```javascript
// 1. Create centralized error classes
class AppError extends Error {
  constructor(code, message, statusCode = 400, details = []) {
    super(message);
    this.code = code;
    this.statusCode = statusCode;
    this.details = details;
    this.isOperational = true; // Known, expected errors
  }
}

class NotFoundError extends AppError {
  constructor(resource) {
    super('NOT_FOUND', `${resource} not found`, 404);
  }
}

class ValidationError extends AppError {
  constructor(details) {
    super('VALIDATION_ERROR', 'Validation failed', 422, details);
  }
}

// 2. Global error handler middleware
app.use((err, req, res, next) => {
  if (err.isOperational) {
    // Known error: send formatted response
    res.status(err.statusCode).json({
      success: false,
      error: { code: err.code, message: err.message, details: err.details }
    });
  } else {
    // Unknown error: log it, send generic message
    console.error('UNEXPECTED ERROR:', err);
    res.status(500).json({
      success: false,
      error: { code: 'INTERNAL_ERROR', message: 'An unexpected error occurred' }
    });
  }
});

// 3. Use in routes
app.get('/users/:id', async (req, res, next) => {
  try {
    const user = await userService.getUser(req.params.id);
    if (!user) throw new NotFoundError('User');
    sendSuccess(res, user);
  } catch (err) {
    next(err); // Pass to global error handler
  }
});
```

---

### Navigation
**Prev:** [11_Consistency_Models.md](11_Consistency_Models.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [13_Rate_Limiting.md](13_Rate_Limiting.md)
