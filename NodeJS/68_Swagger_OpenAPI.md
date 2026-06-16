# Swagger/OpenAPI

Exposing APIs without clear documentation makes integration difficult for frontend developers and external clients. Instead of writing and maintaining static document files that quickly become outdated, you can use OpenAPI standards to generate interactive documentation directly from your code. This ensures your documentation updates automatically when you change routes and models, and provides clients with an interactive testing dashboard.

### Swagger vs. OpenAPI
* **OpenAPI**: The official specification standard (a schema definition format) used to describe RESTful APIs in YAML or JSON.
* **Swagger**: The suite of open-source tools (like Swagger Editor, Swagger UI, and Swagger Codegen) built by SmartBear to write, render, and consume OpenAPI specifications.

### API Contract Design
An OpenAPI specification defines an **API Contract**:
* **Paths**: The list of endpoints (e.g. `/users`) and supported HTTP methods (GET, POST).
* **Parameters**: The parameters accepted in the query string, headers, or route paths.
* **Request Body**: The expected data structure and MIME types for payload writes.
* **Responses**: The possible status codes and response schemas.
* **Components (Schemas)**: Reusable object definitions (like a `User` schema) that can be referenced across multiple routes to prevent duplication.

## Deep Dive

### Dynamic Generation using `swagger-jsdoc`
Writing large YAML or JSON configuration files manually can be tedious. A popular pattern in Node.js is writing OpenAPI specs directly inside your router files using JSDoc code comments:
* **`swagger-jsdoc`**: Parses these comments at runtime to generate a complete OpenAPI JSON object.
* **`swagger-ui-express`**: Serves this JSON object on an interactive web page (like `/api-docs`), allowing developers to test API endpoints directly from their browser.

## Visual Explanation

### Dynamic Swagger Generation Pipeline
```text
  [ Router JS Code + JSDoc Comments ]
                 │
                 ▼ (Parse on startup)
          [ swagger-jsdoc ] ── compiles ──> [ OpenAPI JSON Schema ]
                                                    │
                                                    ▼ (Mount middleware)
                                           [ swagger-ui-express ]
                                                    │
  [ Client Browser ] <── Interactive Swagger Web UI ┘  (Accessible at /api-docs)
```

## Real-World Example
Consider an API that manages users. You define a reusable `User` component schema detailing required fields like `id`, `name`, and `email`. Inside the route controllers, you write JSDoc comments referencing this schema. When developers visit `/api-docs` in their browser, they see the schema models, request requirements, and can click "Try it out" to send actual requests, streamlining frontend-backend integration.

## Code Examples

### Swagger Configuration and Dynamic JSDoc Documentation in Express

```javascript
// app.js
// Dependencies required: npm install express swagger-ui-express swagger-jsdoc
const express = require('express');
const swaggerUi = require('swagger-ui-express');
const swaggerJsdoc = require('swagger-jsdoc');

const app = express();
app.use(express.json());

// 1. Define Swagger Definition options
const swaggerOptions = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'Node.js Mastery API Documentation',
      version: '1.0.0',
      description: 'Production-ready Express API documented with OpenAPI specs'
    },
    servers: [
      {
        url: 'http://localhost:3000',
        description: 'Development server'
      }
    ],
    // Reusable schemas (Components)
    components: {
      schemas: {
        User: {
          type: 'object',
          required: ['id', 'username', 'email'],
          properties: {
            id: { type: 'integer', example: 101 },
            username: { type: 'string', example: 'alice_db' },
            email: { type: 'string', format: 'email', example: 'alice@db.com' }
          }
        }
      }
    }
  },
  // Paths to files containing JSDoc comments to parse
  apis: [__filename] 
};

// Compile OpenAPI specification
const swaggerDocs = swaggerJsdoc(swaggerOptions);

// 2. Mount interactive UI middleware
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDocs));

/**
 * @openapi
 * /api/users:
 *   get:
 *     summary: Retrieve a list of users
 *     description: Returns an array of users registered on the platform.
 *     responses:
 *       200:
 *         description: Success
 *         content:
 *           application/json:
 *             schema:
 *               type: array Jah
 *               items:
 *                 $ref: '#/components/schemas/User'
 *       500:
 *         description: Internal Server Error
 */
app.get('/api/users', (req, res) => {
  res.json([
    { id: 101, username: 'alice_db', email: 'alice@db.com' }
  ]);
});

/**
 * @openapi
 * /api/users:
 *   post:
 *     summary: Create a new user
 *     description: Adds a new user profile to the database.
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - username
 *               - email
 *             properties:
 *               username:
 *                 type: string
 *                 example: bob_smith
 *               email:
 *                 type: string
 *                 example: bob@db.com
 *     responses:
 *       201:
 *         description: User successfully created
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/User'
 *       400:
 *         description: Invalid input parameters
 */
app.post('/api/users', (req, res) => {
  const { username, email } = req.body;
  res.status(201).json({
    id: 102,
    username,
    email
  });
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
  console.log('Swagger documentation page available at: http://localhost:3000/api-docs');
});
```

## Best Practices
* **Document Security Schemes**: Document authorization headers (such as JWT Bearer tokens) inside Swagger components under `securitySchemes`, allowing clients to authenticate requests directly inside the Swagger UI.
* **Keep Schemas Updated**: Ensure your OpenAPI component schemas match your actual database models or Zod validation schemas. Outdated documentation is worse than no documentation.
* **Restrict Access in Production**: Secure the `/api-docs` endpoint in production using basic authentication or disable the route entirely in production environments to protect API metadata from public scanning.

## Interview Questions

**Q:** What is the difference between OpenAPI and Swagger?

> **Answer:**
> OpenAPI is the official specification standard (the schema definition format) used to describe RESTful APIs. Swagger refers to the suite of open-source tools (like Swagger UI and Swagger Editor) built to write, render, and consume these OpenAPI specifications.

**Q:** What are Components in an OpenAPI specification, and why are they used?

> **Answer:**
> Components are reusable object definitions (such as request/response payloads or error schemas) defined at the root of the OpenAPI specification. They are used to prevent code duplication, allowing multiple routes to reference the same object schema (e.g. `#/components/schemas/User`) instead of defining the structure repeatedly.

**Q:** How do you document secure endpoints that require JWT Authorization headers inside an OpenAPI specification? Provide the configuration layout.

> **Answer:**
> You define the security scheme under `components.securitySchemes` in your Swagger options, and then apply it globally or to specific routes under the `security` property:
> ```yaml
> # Definition under components
> components:
> securitySchemes:
> BearerAuth:
> type: http
> scheme: bearer
> bearerFormat: JWT
> 
> # Applied to routes
> security:
> - BearerAuth: []
> ```
> This configuration enables a lock icon next to secure routes in the Swagger UI, allowing developers to enter their JWT tokens and send authenticated requests.

**Q:** How would you implement a "Design-First" API development workflow, and how does it compare to a "Code-First" workflow in terms of team collaboration and contract testing?

> **Answer:**
> 

**Q:** Design-First Workflow

> **Answer:**
> 

**Q:** Code-First Workflow

> **Answer:**
> 

**Q:** Comparison

> **Answer:**
> - *Collaboration*: Design-First is superior for team alignment because frontend and backend teams agree on the interface contract before coding starts, preventing API structure mismatches during integration.
> - *Testing*: Design-First enables **Contract Testing** (using tools like Prism or Dredd) to verify that both the backend implementation and frontend requests comply with the defined OpenAPI specification automatically, ensuring API compatibility. Code-First is easier to start with but makes contract enforcement harder.

---
Previous : [67_Supertest.md](67_Supertest.md) | Index : [00_index.md](00_index.md) | Next : [69_Microservices.md](69_Microservices.md)
