# Validation

Accepting client inputs without validation exposes your application to SQL injection, NoSQL injection, resource exhaustion attacks (like sending a huge payload), and database structure corruption. Input validation acts as the front gate of your application, filtering out invalid or malicious data before it can reach your database or trigger business logic.

### Request Boundary Validation
Input validation should happen as early as possible in the request lifecycle, right at the HTTP routing boundary. It checks that incoming payloads have the correct structure, field types, and size.

There are two main approaches to validation:
1. **Manual Validation**: Writing long lists of `if/else` statements inside controller functions. This makes controllers bloated and leads to repetitive code.
2. **Schema-based Validation**: Defining a declarative data schema that describes the expected fields and types. The request is validated against this schema using reusable middleware, keeping controllers focused on business logic.

### Schema Validation Libraries
* **Joi**: A mature schema validation library popular in the Node.js ecosystem.
* **Zod**: A modern, TypeScript-first validation library that supports static type inference, making it popular in modern JS/TS backends.

## Deep Dive

### Request Target Areas
A robust validation middleware must validate three distinct input channels in Express:
1. **`req.body`**: JSON payload parameters sent in request bodies (e.g. validating email formats during signup).
2. **`req.query`**: Query string parameters (e.g. validating sorting fields and paging indices).
3. **`req.params`**: Route parameters (e.g. validating that resource IDs match uuid or digit formats).

If any of these fields fail validation, the middleware should halt the request and return a `400 Bad Request` status code immediately, preventing the request from executing controller logic.

## Visual Explanation

### Request Validation Middleware Pipeline
```text
Client Request ──> [ Express Router ]
                         │
                         ▼
        [ Validation Middleware: Zod Schema ]
                         │
                         ├── (Validation fails?)
                         │     ├── YES ──> Send 400 Bad Request Response (End)
                         │     │             (Contains array of field-level error messages)
                         │     └── NO  ──> Mutate req.body with sanitized data ──> next()
                         ▼
               [ Route Controller ] ──> Process database changes safely
```

## Real-World Example
Consider a user registration endpoint `/register`. Instead of manual validation, you define a registration schema: a username between 3 and 20 characters, a valid email format, and a password containing special characters. You bind this schema to validation middleware. If the client submits invalid inputs, the middleware catches the errors and returns a formatted JSON list of issues, keeping the controller clean.

## Code Examples

### Zod Schema Definition and Express Validation Middleware

```javascript
// middleware/validate.js
const { z } = require('zod');

// 1. Reusable Validation Middleware
// Accepts schemas for body, query, and params optionally
const validate = (schemas) => (req, res, next) => {
  try {
    // Validate request parameters if schema is provided
    if (schemas.params) {
      req.params = schemas.params.parse(req.params);
    }
    
    // Validate request query strings if schema is provided
    if (schemas.query) {
      req.query = schemas.query.parse(req.query);
    }
    
    // Validate request JSON body if schema is provided
    if (schemas.body) {
      // parse() normalizes values (e.g. stripping unknown keys)
      req.body = schemas.body.parse(req.body);
    }
    
    next(); // Pass control to the controller if validation passes
  } catch (err) {
    if (err instanceof z.ZodError) {
      // Map Zod errors to a client-friendly format
      const formattedErrors = err.issues.map(issue => ({
        field: issue.path.join('.'),
        message: issue.message
      }));
      
      return res.status(400).json({
        error: 'Bad Request: Input Validation Failed',
        details: formattedErrors
      });
    }
    
    next(err);
  }
};

// 2. Define Validation Schemas
const schemas = {
  // Body schema for user registration
  registerUser: {
    body: z.object({
      username: z.string().min(3, 'Username must be at least 3 characters long').max(20),
      email: z.string().email('Invalid email address format'),
      password: z.string().min(8, 'Password must be at least 8 characters long'),
      role: z.enum(['user', 'manager']).default('user')
    })
  },
  
  // Params schema to validate UUID resource IDs
  fetchUser: {
    params: z.object({
      id: z.string().regex(/^\d+$/, 'ID parameter must be a valid numeric index')
    })
  }
};

module.exports = { validate, schemas };
```

```javascript
// app.js
const express = require('express');
const { validate, schemas } = require('./middleware/validate');

const app = express();
app.use(express.json());

// Bind validation middleware to routes before controllers
app.post('/api/users', validate(schemas.registerUser), (req, res) => {
  // At this point, req.body is guaranteed to be valid and clean
  res.status(201).json({ message: 'User registered', data: req.body });
});

app.get('/api/users/:id', validate(schemas.fetchUser), (req, res) => {
  res.json({ message: 'Fetching user', id: req.params.id });
});

app.listen(3000, () => console.log('Validation server running on port 3000'));
```

## Best Practices
* **Strip Unknown Properties**: Configure your validation library to strip out fields not defined in the schema to prevent clients from executing Parameter Injection attacks (e.g., adding a `"role": "admin"` property during user registration).
* **Sanitize Inputs**: Use validation schemas to trim spaces and normalize data formats (like lowercasing emails) before writing to databases.
* **Validate Every Input Channel**: Always validate all input sources (request body, path parameters, and query strings) rather than focusing only on request bodies.

## Interview Questions

**Q:** Why should you validate user input in a backend application?

> **Answer:**
> Input validation prevents security vulnerabilities (like database injection attacks), blocks invalid data formats that could crash the application, and keeps the database structure clean.

**Q:** What is the difference between Joi and Zod validation libraries?

> **Answer:**
> Joi is a schema-validation library that uses chained helper methods to validate runtime data. Zod is a newer schema-validation library that supports TypeScript type inference out of the box, allowing you to infer TS types directly from your schemas without manual type definitions.

**Q:** Explain how validation middleware helps keep your code clean, and how to configure it to prevent parameter injection attacks.

> **Answer:**
> Validation middleware checks incoming request structures before they reach controller handlers, keeping controllers focused on business logic.
> To prevent parameter injection attacks (where clients send extra properties to modify values like roles or billing status), configure your schemas to strip unknown keys. In Zod, the `.parse()` method strips out undefined properties by default. In Joi, you can configure the validation options to set `stripUnknown: true`, ensuring only defined fields reach the database operations.

**Q:** How would you build an extensible, schema-driven validation framework in an Express API that integrates with database models to perform asynchronous, cross-field integrity checks (e.g., validating that an email is unique in the database before routing)?

> **Answer:**
> To build a validation framework with asynchronous database checks:
> 1. Define a base schema validation middleware using a library like Zod.
> 2. Leverage Zod's `.refine()` method, which supports asynchronous callbacks, to check database state:
> ```javascript
> const emailSchema = z.string().email().refine(async (email) => {
> const userExists = await db.findUserByEmail(email);
> return !userExists; // Valid if user does not exist
> }, {
> message: 'Email address is already registered'
> });
> ```
> 3. Keep database queries inside validation refines fast by using indexing on the target columns (e.g., email), preventing database query latency from blocking requests at the API boundary.

---
Previous : [28_Environment_Variables.md](28_Environment_Variables.md) | Index : [00_index.md](00_index.md) | Next : [30_Error_Handling.md](30_Error_Handling.md)
