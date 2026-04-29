# 📌 06 — Middleware Design

## 🧠 Concept Explanation

Middleware is a function that sits in a processing pipeline, receiving context, executing logic, and passing control to the next function. It's the backbone of HTTP framework design (Express, Koa, Fastify) and enables cross-cutting concerns (logging, auth, rate limiting) to be composed without repeating code.

## 🔬 Internal Mechanics

### Express Middleware Stack

Express maintains an ordered list of middleware functions. `next()` moves to the next function. The stack is traversed as a linked list; `next()` is essentially `stack[index++](req, res, next)`.

### Koa's Onion Model

Koa uses `async/await` + generator-based (now async function) middleware:

```
Request:
  ─► Middleware 1 starts
       ─► Middleware 2 starts
            ─► Middleware 3 starts
            ◄── Middleware 3 ends (await next())
       ◄── Middleware 2 ends (await next())
  ◄── Middleware 1 ends (await next())
Response sent
```

Koa's compose function:

```javascript
function compose(middleware) {
  return function(ctx, next) {
    let index = -1
    
    function dispatch(i) {
      if (i <= index) return Promise.reject(new Error('next() called multiple times'))
      index = i
      const fn = middleware[i] || next
      if (!fn) return Promise.resolve()
      return Promise.resolve(fn(ctx, () => dispatch(i + 1)))
    }
    
    return dispatch(0)
  }
}
```

## 🔍 Code Examples

### Example 1 — Express Middleware Patterns

```javascript
// Logging middleware
function requestLogger(req, res, next) {
  const start = Date.now()
  const { method, url } = req
  
  res.on('finish', () => {
    console.log(`${method} ${url} ${res.statusCode} ${Date.now() - start}ms`)
  })
  
  next()
}

// Async middleware with error handling
function asyncMiddleware(fn) {
  return (req, res, next) => {
    Promise.resolve(fn(req, res, next)).catch(next)
  }
}

app.use(asyncMiddleware(async (req, res, next) => {
  req.user = await verifyJWT(req.headers.authorization)
  next()
}))

// Error middleware (4 parameters!)
app.use((err, req, res, next) => {
  console.error(err.stack)
  res.status(err.status || 500).json({
    error: err.message,
    ...(process.env.NODE_ENV === 'development' && { stack: err.stack })
  })
})
```

### Example 2 — Rate Limiting Middleware

```javascript
class RateLimiter {
  constructor({ windowMs = 60000, max = 100, keyGenerator = (req) => req.ip }) {
    this.windowMs = windowMs
    this.max = max
    this.keyGenerator = keyGenerator
    this.store = new Map()
    
    // Cleanup old entries every minute
    setInterval(() => {
      const now = Date.now()
      for (const [key, data] of this.store.entries()) {
        if (now > data.resetTime) this.store.delete(key)
      }
    }, 60000)
  }
  
  middleware() {
    return (req, res, next) => {
      const key = this.keyGenerator(req)
      const now = Date.now()
      
      let data = this.store.get(key)
      if (!data || now > data.resetTime) {
        data = { count: 0, resetTime: now + this.windowMs }
        this.store.set(key, data)
      }
      
      data.count++
      
      res.setHeader('X-RateLimit-Limit', this.max)
      res.setHeader('X-RateLimit-Remaining', Math.max(0, this.max - data.count))
      res.setHeader('X-RateLimit-Reset', Math.ceil(data.resetTime / 1000))
      
      if (data.count > this.max) {
        return res.status(429).json({ error: 'Too many requests' })
      }
      
      next()
    }
  }
}
```

### Example 3 — Middleware Composition Pattern

```javascript
// Generic compose utility
const compose = (...middlewares) => (ctx) => {
  const execute = (index) => {
    if (index >= middlewares.length) return Promise.resolve()
    const middleware = middlewares[index]
    return Promise.resolve(middleware(ctx, () => execute(index + 1)))
  }
  return execute(0)
}

// Domain-specific middleware stack
const processOrder = compose(
  validateOrderMiddleware,
  checkInventoryMiddleware,
  calculatePricingMiddleware,
  applyDiscountsMiddleware,
  chargePaymentMiddleware,
  sendConfirmationMiddleware
)

await processOrder({ order: orderData })
```

## 💥 Production Failure — Unhandled Async Errors

```javascript
// BUG: Async middleware error not caught
app.use(async (req, res, next) => {
  const user = await db.findUser(req.userId)  // Throws if DB is down
  req.user = user
  // NO try/catch, NO .catch() → unhandledRejection → process may crash
  next()
})

// Fix: Wrap async middleware
app.use(async (req, res, next) => {
  try {
    req.user = await db.findUser(req.userId)
    next()
  } catch(err) {
    next(err)  // Pass to error middleware
  }
})

// Or use express-async-errors package:
require('express-async-errors')
// Now async errors in middleware are automatically passed to next(err)
```

## 🏢 Industry Best Practices

1. **Keep middleware single-responsibility** — Each middleware does ONE thing.
2. **Always call next() or send response** — Hanging requests = resource leak.
3. **Use express-async-errors or wrap async middleware** — Prevent unhandled rejections.
4. **Order matters** — Auth before routes, error handler last.
5. **Test middleware in isolation** — Mock req/res/next to unit test middleware logic.

## 💼 Interview Questions

**Q1: What is the difference between Express's middleware model and Koa's?**
> Express: linear stack, callbacks with next(). Middleware cannot modify the response after next() is called (well, it can, but it's not idiomatic). Error middleware needs 4 parameters. Koa: async/await onion model. Middleware wraps the next middleware — code before await next() runs on the way in, code after runs on the way out. This makes post-processing (e.g., logging response time, adding response headers after route handler runs) natural and clean.

## 🔗 Navigation

**Prev:** [05_Worker_Threads.md](05_Worker_Threads.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [07_Event_Loop_Node_vs_Browser.md](07_Event_Loop_Node_vs_Browser.md)
