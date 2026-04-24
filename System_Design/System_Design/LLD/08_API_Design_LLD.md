# 📌 API Design (LLD)

## 🧠 Concept Explanation (Story Format)

A badly designed API is like a badly designed door handle. You never know if you should push or pull, it's inconsistent in different rooms, and sometimes it breaks when you use it.

A well-designed API is so intuitive that developers can guess how it works without reading documentation. They're predictable, consistent, and easy to use.

This module focuses on the LOW-LEVEL details of API design — how to structure routes, validate inputs, handle errors, and structure responses.

---

## 🔍 Key API Design Principles

### 1. RESTful Route Design

```javascript
// ✅ RESTful conventions

// Resources = nouns, HTTP methods = verbs
GET    /api/users           → List users
GET    /api/users/:id       → Get specific user
POST   /api/users           → Create user
PUT    /api/users/:id       → Replace user completely
PATCH  /api/users/:id       → Update user partially
DELETE /api/users/:id       → Delete user

// Nested resources
GET    /api/users/:id/posts          → Get user's posts
POST   /api/users/:id/posts          → Create post for user
GET    /api/users/:id/posts/:postId  → Get specific post

// Actions that don't fit CRUD (use verbs in route)
POST   /api/auth/login
POST   /api/auth/logout
POST   /api/auth/refresh
POST   /api/orders/:id/cancel        → Action on resource
POST   /api/posts/:id/like
DELETE /api/posts/:id/like           → Unlike

// ❌ Bad REST design
GET  /api/getUser          → Verb in noun route (bad!)
GET  /api/user             → Inconsistent singular (should be plural)
POST /api/createUser       → Verb in route (bad!)
GET  /api/searchProducts   → Should be GET /api/products?q=...
```

### 2. Request Validation with Zod

```javascript
const { z } = require('zod');

// Define schema
const createUserSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters').max(100),
  email: z.string().email('Invalid email format'),
  password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/, 'Password must have uppercase, lowercase, and number'),
  role: z.enum(['user', 'admin']).default('user'),
  dateOfBirth: z.string().datetime().optional()
});

const createPostSchema = z.object({
  title: z.string().min(5).max(200),
  content: z.string().min(10).max(50000),
  tags: z.array(z.string().max(30)).max(10).optional().default([]),
  isPublished: z.boolean().default(false),
  scheduledAt: z.string().datetime().optional()
});

// Validation middleware factory
function validate(schema) {
  return (req, res, next) => {
    const result = schema.safeParse(req.body);
    
    if (!result.success) {
      return res.status(400).json({
        success: false,
        error: {
          code: 'VALIDATION_ERROR',
          message: 'Invalid request data',
          details: result.error.errors.map(e => ({
            field: e.path.join('.'),
            message: e.message,
            code: e.code
          }))
        }
      });
    }
    
    req.validated = result.data; // Use validated/sanitized data!
    next();
  };
}

// Usage
app.post('/api/users', validate(createUserSchema), async (req, res) => {
  const { name, email, password, role } = req.validated; // Always use validated data!
  const user = await userService.create({ name, email, password, role });
  res.status(201).json({ success: true, data: user });
});
```

### 3. Consistent Response Structure

```javascript
// ALWAYS use consistent response format!

// ✅ Success response structure
{
  "success": true,
  "data": { ... },         // The actual data
  "meta": {                // Pagination, counts, etc.
    "page": 1,
    "limit": 20,
    "total": 1543,
    "pages": 78
  },
  "timestamp": "2024-01-15T10:30:45Z"
}

// ✅ Error response structure
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",   // Machine-readable error code
    "message": "Invalid input",   // Human-readable message
    "details": [                  // Optional: field-level errors
      { "field": "email", "message": "Invalid email format" }
    ]
  },
  "timestamp": "2024-01-15T10:30:45Z",
  "requestId": "req_abc123"       // For tracing
}

// ✅ List response
{
  "success": true,
  "data": [
    { "id": "1", "name": "Alice" },
    { "id": "2", "name": "Bob" }
  ],
  "meta": { "total": 100, "page": 1, "limit": 20, "pages": 5 }
}
```

```javascript
// Response helper class
class APIResponse {
  static success(res, data, statusCode = 200, meta = null) {
    const response = {
      success: true,
      data,
      timestamp: new Date().toISOString()
    };
    if (meta) response.meta = meta;
    return res.status(statusCode).json(response);
  }
  
  static created(res, data) {
    return this.success(res, data, 201);
  }
  
  static noContent(res) {
    return res.status(204).send();
  }
  
  static error(res, statusCode, code, message, details = null) {
    const response = {
      success: false,
      error: { code, message },
      timestamp: new Date().toISOString(),
      requestId: res.locals.requestId
    };
    if (details) response.error.details = details;
    return res.status(statusCode).json(response);
  }
  
  static paginated(res, data, { page, limit, total }) {
    return this.success(res, data, 200, {
      page: parseInt(page),
      limit: parseInt(limit),
      total,
      pages: Math.ceil(total / limit),
      hasNext: page * limit < total,
      hasPrev: page > 1
    });
  }
}

// Usage in controllers
app.get('/api/posts', async (req, res) => {
  const { page = 1, limit = 20, sort = 'createdAt' } = req.query;
  const { posts, total } = await postService.list({ page, limit, sort });
  return APIResponse.paginated(res, posts, { page, limit, total });
});

app.post('/api/posts', validate(createPostSchema), async (req, res) => {
  const post = await postService.create(req.validated);
  return APIResponse.created(res, post);
});
```

### 4. Centralized Error Handling

```javascript
// Error types
class AppError extends Error {
  constructor(message, statusCode = 500, code = 'INTERNAL_ERROR', details = null) {
    super(message);
    this.statusCode = statusCode;
    this.code = code;
    this.details = details;
    this.isOperational = true; // We expected this error
  }
}

class ValidationError extends AppError {
  constructor(message, details) {
    super(message, 400, 'VALIDATION_ERROR', details);
  }
}

class NotFoundError extends AppError {
  constructor(resource = 'Resource') {
    super(`${resource} not found`, 404, 'NOT_FOUND');
  }
}

class UnauthorizedError extends AppError {
  constructor(message = 'Authentication required') {
    super(message, 401, 'UNAUTHORIZED');
  }
}

class ForbiddenError extends AppError {
  constructor(message = 'Access denied') {
    super(message, 403, 'FORBIDDEN');
  }
}

class ConflictError extends AppError {
  constructor(message) {
    super(message, 409, 'CONFLICT');
  }
}

// Controllers throw errors, handler catches all
app.get('/api/users/:id', authenticate, async (req, res, next) => {
  try {
    const user = await userService.findById(req.params.id);
    if (!user) throw new NotFoundError('User');
    return APIResponse.success(res, user);
  } catch (error) {
    next(error); // Pass to global error handler!
  }
});

// Global error handler (LAST middleware in Express)
app.use((error, req, res, next) => {
  // Operational errors (we created them intentionally)
  if (error.isOperational) {
    return res.status(error.statusCode).json({
      success: false,
      error: {
        code: error.code,
        message: error.message,
        ...(error.details && { details: error.details })
      },
      requestId: req.requestId
    });
  }
  
  // Programming errors (bugs!) — log full details
  logger.error('Unexpected error', {
    error: error.message,
    stack: error.stack,
    requestId: req.requestId,
    url: req.url,
    method: req.method,
    userId: req.user?.id
  });
  
  // Don't leak error details in production
  return res.status(500).json({
    success: false,
    error: {
      code: 'INTERNAL_SERVER_ERROR',
      message: 'Something went wrong. Please try again later.'
    },
    requestId: req.requestId
  });
});

// Async error wrapper (avoids try-catch in every route)
const asyncHandler = (fn) => (req, res, next) => {
  Promise.resolve(fn(req, res, next)).catch(next);
};

// Clean route handler!
app.get('/api/users/:id', authenticate, asyncHandler(async (req, res) => {
  const user = await userService.findById(req.params.id);
  if (!user) throw new NotFoundError('User');
  return APIResponse.success(res, user);
}));
```

### 5. Pagination Design

```javascript
// Cursor-based pagination (better for large datasets)
app.get('/api/posts', asyncHandler(async (req, res) => {
  const { cursor, limit = 20, sort = 'desc' } = req.query;
  
  const limitNum = Math.min(parseInt(limit), 100); // Max 100
  
  let query = db.collection('posts').find({ isPublished: true });
  
  if (cursor) {
    const cursorDate = new Date(Buffer.from(cursor, 'base64').toString('ascii'));
    query = query.find({
      createdAt: sort === 'desc' ? { $lt: cursorDate } : { $gt: cursorDate }
    });
  }
  
  const posts = await query
    .sort({ createdAt: sort === 'desc' ? -1 : 1 })
    .limit(limitNum + 1) // Fetch one extra to check if there's a next page
    .toArray();
  
  const hasMore = posts.length > limitNum;
  const results = posts.slice(0, limitNum);
  
  const nextCursor = hasMore 
    ? Buffer.from(results[results.length - 1].createdAt.toISOString()).toString('base64')
    : null;
  
  return res.json({
    success: true,
    data: results,
    meta: { cursor: nextCursor, hasMore, limit: limitNum }
  });
}));

// Offset-based pagination (simpler, good for small datasets)
app.get('/api/products', asyncHandler(async (req, res) => {
  const page = Math.max(1, parseInt(req.query.page) || 1);
  const limit = Math.min(100, parseInt(req.query.limit) || 20);
  const skip = (page - 1) * limit;
  
  const [products, total] = await Promise.all([
    db.query('SELECT * FROM products ORDER BY created_at DESC LIMIT $1 OFFSET $2', [limit, skip]),
    db.query('SELECT COUNT(*) FROM products')
  ]);
  
  return APIResponse.paginated(res, products.rows, { page, limit, total: parseInt(total.rows[0].count) });
}));
```

### 6. API Versioning

```javascript
// URL-based versioning (most common)
app.use('/api/v1', v1Router);
app.use('/api/v2', v2Router);

// v1 routes
const v1Router = express.Router();
v1Router.get('/users/:id', async (req, res) => {
  const user = await db.getUser(req.params.id);
  // v1 response format
  res.json({ id: user.id, name: user.name, email: user.email });
});

// v2 routes (updated format)
const v2Router = express.Router();
v2Router.get('/users/:id', async (req, res) => {
  const user = await db.getUser(req.params.id);
  // v2 response format (improved structure)
  res.json({
    success: true,
    data: {
      id: user.id, name: user.name, email: user.email,
      profile: { avatar: user.avatarUrl, bio: user.bio }
    }
  });
});

// Deprecation headers — warn v1 clients to upgrade
v1Router.use((req, res, next) => {
  res.set('Deprecation', 'true');
  res.set('Sunset', 'Sat, 1 Jan 2026 00:00:00 GMT');
  res.set('Link', '<https://api.myapp.com/v2>; rel="successor-version"');
  next();
});
```

---

## 💼 Interview Questions (WITH SOLUTIONS)

### Q1: What are the HTTP status codes you should know?

**Solution:**
```
2xx Success:
  200 OK          — GET success, PUT/PATCH success
  201 Created     — POST success (created new resource)
  202 Accepted    — Request accepted but processing async
  204 No Content  — DELETE success (no body to return)

3xx Redirection:
  301 Moved Permanently — Resource URL changed (update bookmarks)
  302 Found             — Temporary redirect
  304 Not Modified      — Cached version is still valid

4xx Client Errors (client's fault):
  400 Bad Request      — Invalid request (missing/invalid fields)
  401 Unauthorized     — Not authenticated (no/invalid token)
  403 Forbidden        — Authenticated but not authorized (wrong role)
  404 Not Found        — Resource doesn't exist
  409 Conflict         — Duplicate resource (email already exists)
  422 Unprocessable    — Validation error (data invalid)
  429 Too Many Requests— Rate limit exceeded

5xx Server Errors (server's fault):
  500 Internal Server Error — Unhandled exception, bug
  502 Bad Gateway           — Upstream service failed
  503 Service Unavailable   — Overloaded or down for maintenance
  504 Gateway Timeout       — Upstream service timed out
```

### Q2: How do you design a pagination API?

**Solution:**
Two approaches:
1. **Offset pagination:** `?page=2&limit=20` → easy but slow for large offsets (DB must skip N rows)
2. **Cursor pagination:** `?cursor=eyJj...&limit=20` → fast at any depth (cursor = encoded last item)

Use offset for: Small datasets, admin interfaces where you need to jump to page 50.
Use cursor for: Infinite scroll, large datasets (Twitter feed, Slack messages).

Return in response: `{ data, meta: { nextCursor, hasMore, limit } }` for cursor pagination.

### Q3: How do you handle API versioning?

**Solution:**
Three approaches:
1. **URL versioning:** `/api/v1/users` vs `/api/v2/users` — most common, clear in URLs
2. **Header versioning:** `Accept: application/vnd.myapp.v2+json` — cleaner URLs but less discoverable
3. **Query param:** `/api/users?version=2` — simple but pollutes query params

Best practice:
- Start with v1 from day 1 (even if you never bump to v2)
- Add `Deprecation` header when deprecating old versions
- Give 6-12 months notice before removing old versions
- Document breaking changes clearly in changelogs

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem: Design a complete REST API for a blog platform

```javascript
// Complete blog API with proper design

const router = express.Router();

// Posts
router.get('/posts', asyncHandler(async (req, res) => {
  const { page = 1, limit = 20, tag, author, search, sort = 'recent' } = req.query;
  const { posts, total } = await postService.list({ page, limit, tag, author, search, sort });
  return APIResponse.paginated(res, posts, { page, limit, total });
}));

router.get('/posts/:slug', asyncHandler(async (req, res) => {
  const post = await postService.findBySlug(req.params.slug);
  if (!post) throw new NotFoundError('Post');
  return APIResponse.success(res, post);
}));

router.post('/posts', authenticate, validate(createPostSchema), asyncHandler(async (req, res) => {
  const post = await postService.create({ ...req.validated, authorId: req.user.id });
  return APIResponse.created(res, post);
}));

router.patch('/posts/:id', authenticate, validate(updatePostSchema), asyncHandler(async (req, res) => {
  const post = await postService.findById(req.params.id);
  if (!post) throw new NotFoundError('Post');
  if (post.authorId !== req.user.id && req.user.role !== 'admin') throw new ForbiddenError();
  const updated = await postService.update(req.params.id, req.validated);
  return APIResponse.success(res, updated);
}));

router.delete('/posts/:id', authenticate, asyncHandler(async (req, res) => {
  const post = await postService.findById(req.params.id);
  if (!post) throw new NotFoundError('Post');
  if (post.authorId !== req.user.id && req.user.role !== 'admin') throw new ForbiddenError();
  await postService.delete(req.params.id);
  return APIResponse.noContent(res);
}));

// Post actions
router.post('/posts/:id/like', authenticate, asyncHandler(async (req, res) => {
  const result = await postService.like(req.params.id, req.user.id);
  return APIResponse.success(res, result);
}));

router.delete('/posts/:id/like', authenticate, asyncHandler(async (req, res) => {
  await postService.unlike(req.params.id, req.user.id);
  return APIResponse.noContent(res);
}));

// Comments (nested resource)
router.get('/posts/:id/comments', asyncHandler(async (req, res) => {
  const { cursor, limit = 20 } = req.query;
  const { comments, nextCursor, hasMore } = await commentService.list(req.params.id, { cursor, limit });
  return res.json({ success: true, data: comments, meta: { cursor: nextCursor, hasMore } });
}));

router.post('/posts/:id/comments', authenticate, validate(createCommentSchema), asyncHandler(async (req, res) => {
  const comment = await commentService.create({ ...req.validated, postId: req.params.id, userId: req.user.id });
  return APIResponse.created(res, comment);
}));
```

---

### Navigation
**Prev:** [07_Database_Design.md](07_Database_Design.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [09_Caching_Strategy.md](09_Caching_Strategy.md)
