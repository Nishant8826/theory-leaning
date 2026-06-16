# Authorization

Authentication only verifies *who* the user is. If your application lacks secure authorization checks, any authenticated user can guess another user's ID and query their private data (an IDOR attack) or access admin endpoints (privilege escalation). Secure authorization enforces access policies at the API boundary, protecting resources from unauthorized access.

### Access Control Models
1. **Role-Based Access Control (RBAC)**:
   * *Concept*: Permissions are grouped into static roles (e.g. `admin`, `manager`, `user`), and roles are assigned to users.
   * *Use Case*: Simple authorization structures (e.g. "Only users with the `admin` role can access this route").
2. **Attribute-Based Access Control (ABAC)**:
   * *Concept*: Access decisions are evaluated dynamically based on attributes of the user, the resource, and the context (e.g., "A manager can edit a project only if they own the project, the project status is `active`, and they are accessing it from the company network").
   * *Use Case*: Complex, dynamic access control policies.

### Insecure Direct Object Reference (IDOR)
An **IDOR** vulnerability occurs when an application exposes a direct reference to a database record (like `/api/orders/42`) in its API routes, and relies on the client's inputs without verifying if the requesting user actually owns or has permission to access that record. An attacker can change the ID in the request to access other users' data.

## Deep Dive

### Implementing Multi-Layered Authorization
Secure applications use a two-layered authorization model:
1. **Role Boundary Layer**: Middleware checks if the user's role is permitted to hit the route (e.g. checking if `req.user.role === 'admin'`).
2. **Resource Ownership Layer**: The controller checks if the database record belongs to the requesting user (e.g. verifying `resource.ownerId === req.user.id`) before returning the resource or applying changes.

## Visual Explanation

### Role-Based Route Gate vs. Resource-Level Ownership Gate
```text
Request: GET /api/v1/projects/505
User: { id: 99, role: 'user' }

Step 1: Role Gate (Middleware)
[ Path: /api/v1/projects/:id ] ── Check permissions for 'user' role ──> Match! Pass to next()
                                                                              │
                                                                              ▼
Step 2: Ownership Gate (Controller)
[ Query Project 505 ] ── returns ──> Project: { id: 505, ownerId: 101 }
                                                      │
                                                      ├── Does project.ownerId === req.user.id?
                                                      │     ├── YES ──> Return Project Details
                                                      │     └── NO  ──> return 403 Forbidden (Prevent IDOR!)
                                                      ▼
```

## Real-World Example
Consider a document sharing platform. You define roles like `guest` and `author`. Guests can only view documents, while authors can write them. Additionally, authors can only edit documents they created. You apply role validation middleware to secure `/documents` routes, and check ownership in controllers to prevent authors from editing each other's documents.

## Code Examples

### Express RBAC Middleware and Ownership Verification

```javascript
// middleware/authorize.js
const AppError = require('../utils/AppError');

// 1. Role-Based Access Control (RBAC) Middleware
// Restricts route access to specific roles
const authorizeRoles = (...allowedRoles) => {
  return (req, res, next) => {
    // Authenticate middleware must run first to attach req.user
    if (!req.user) {
      return next(new AppError('Authentication context missing.', 401));
    }

    if (!allowedRoles.includes(req.user.role)) {
      return next(new AppError('Forbidden: You lack permissions to access this resource.', 403));
    }

    next();
  };
};

module.exports = { authorizeRoles };
```

```javascript
// controllers/projectController.js
const AppError = require('../utils/AppError');

// Mock Database resource
const projectsDb = [
  { id: 505, name: 'Secret Strategy Document', ownerId: 101 },
  { id: 909, name: 'Public Marketing Board', ownerId: 202 }
];

// 2. Resource-Level Ownership Verification Controller
exports.getProjectDetails = async (req, res, next) => {
  try {
    const projectId = parseInt(req.params.id, 10);
    const project = projectsDb.find(p => p.id === projectId);

    if (!project) {
      return next(new AppError('Project not found.', 404));
    }

    // Dynamic Attribute check: Allow access only if user is the Owner OR has Admin role
    const isOwner = project.ownerId === req.user.id;
    const isAdmin = req.user.role === 'admin';

    if (!isOwner && !isAdmin) {
      // Return 403 Forbidden to prevent Insecure Direct Object Reference (IDOR) leaks
      return next(new AppError('Forbidden: Access denied to this project resource.', 403));
    }

    res.status(200).json(project);
  } catch (err) {
    next(err);
  }
};
```

```javascript
// routes/projectRoutes.js
const express = require('express');
const router = express.Router();
const { authorizeRoles } = require('../middleware/authorize');
const projectController = require('../controllers/projectController');

// Mock authentication middleware (simulating token validation)
const mockAuthenticate = (req, res, next) => {
  req.user = { id: 101, role: 'user' }; // Set user context
  next();
};

// Apply gates: user must be authenticated, and only specific roles can route
router.get(
  '/projects/:id',
  mockAuthenticate,
  authorizeRoles('user', 'admin'), // Role-based Gate
  projectController.getProjectDetails // Ownership-based Gate
);

module.exports = router;
```

## Best Practices
* **Use the Principle of Least Privilege**: Default all routes to be private and require explicit authorization.
* **Always Validate Ownership**: Never assume that verifying a user's role is enough. Always check resource ownership in the controller when querying, updating, or deleting records.
* **Secure Route Parameters**: Validate that resource IDs in path parameters match expected formats (like numbers or UUIDs) before using them in database queries.

## Interview Questions

**Q:** What is the difference between role-based access control (RBAC) and attribute-based access control (ABAC)?

> **Answer:**
> RBAC grants access based on predefined static user roles (e.g. admin or editor). ABAC grants access dynamically by evaluating attributes of the user, the resource, and the current request context (e.g., owner ID, creation date, or IP address).

**Q:** What is an Insecure Direct Object Reference (IDOR) vulnerability, and how do you prevent it in a Node.js API?

> **Answer:**
> An IDOR vulnerability occurs when an API endpoint exposes database keys directly (e.g. `/api/orders/:id`), and executes queries without validating if the requesting user has permission to access that specific record.
> To prevent IDOR, always verify in your database query or controller logic that the resource's owner ID matches the authenticated user ID (`req.user.id`) before returning or modifying the data.

**Q:** Explain how authorization middleware interacts with the Express request context pipeline, and why authentication middleware must always execute first.

> **Answer:**
> Authorization checks permissions based on the user's identity and roles. The user context (like `req.user`) is resolved and attached to the request object by the authentication middleware.
> If authorization middleware executes first, `req.user` will be `undefined`, causing the authorization check to fail or crash. Therefore, authentication must always run first to populate the request context.

**Q:** How would you design a scalable, low-latency authorization system in a distributed microservices architecture, ensuring that changes to user permissions propagate instantly without overloading the central database?

> **Answer:**
> To design a distributed authorization system:
> 1. **Decouple Policy Check**: Embed the user's roles and permissions as claims inside a signed, cryptographically secure JWT token. This allows each microservice to validate permissions locally without querying a central database.
> 2. **Cache Permission Scopes**: If permissions are too large to fit in a JWT, store the user's permissions cache in a shared in-memory database like Redis. Microservices can query Redis with low latency.
> 3. **Event-Driven Revocation**: When a user's roles or permissions change, publish a revocation event to a message broker (like RabbitMQ or Redis Pub/Sub). Microservices consume this event to invalidate local tokens or update their cache instantly, ensuring changes propagate without database overhead.

---
Previous : [32_Authentication.md](32_Authentication.md) | Index : [00_index.md](00_index.md) | Next : [34_JWT.md](34_JWT.md)
