# MVC Architecture

## What You Will Learn
* The first-principles structure of Model-View-Controller (MVC) architecture.
* Decoupling route definitions from controller logic.
* The roles and boundaries of Models, Views, and Controllers.
* Codebase folder structure layout for large production-grade projects.

## Why This Matters
When starting out, it is easy to write all routing, database queries, and response formatting inside a single file. However, as the application grows, this creates a "spaghetti codebase" that is difficult to understand, impossible to unit test, and prone to conflicts among developers. MVC provides a standard structure that separates concerns, keeping code clean and maintainable.

## Theory

### The MVC Structural Pattern
MVC separates application concerns into three distinct layers:
1. **Model (Data Layer)**: Handles data structures, database schemas, validation rules, and direct database queries. The Model does not know about routing, HTTP protocols, or how the data is presented to the client.
2. **View (Presentation Layer)**: Formats and presents the data to the client. In a REST API, the View is the serialization layer that formats JavaScript objects into JSON responses. In a server-rendered app, the View is a template engine (like EJS or Pug) that outputs HTML.
3. **Controller (Orchestration Layer)**: The glue that binds the Model and the View. The Controller parses incoming HTTP requests, validates input parameters, calls the appropriate Model methods to query or update data, and passes the output to the View to send back to the client.

### Decoupling Routes from Controllers
A key best practice in MVC is separating route declarations from request handling logic:
* **Router Files**: Define *only* the endpoint paths, HTTP verbs, and security middleware. They do not handle requests or write responses.
* **Controller Files**: Define the actual request handlers. They receive `req` and `res`, process the inputs, and return responses, keeping routing files clean and readable.

## Deep Dive

### Folder Structure Layout
Here is a standard, production-ready directory structure for an MVC-based Node.js API:

```text
src/
├── config/             # Environment variables and DB client setups
├── models/             # Mongoose/Sequelize schemas and DB query logic
│   └── User.js
├── controllers/        # Request handlers and orchestration logic
│   └── userController.js
├── routes/             # Route configurations and middleware mounts
│   └── userRoutes.js
├── views/              # Optional template engines or JSON serializers
├── middlewares/        # Custom global or route-specific middlewares
└── app.js              # Express app bootstrap entrypoint
```

## Visual Explanation

### MVC Request Lifecycle
```text
  [ Client Request ] ────> [ Router ] ────> Passes execution ────> [ Controller ]
                                                                        │
                                                                        ├─ Queries ─> [ Model ]
                                                                        │                 │
                                                                        │                 ▼
                                                                        │         [ Database Store ]
                                                                        │                 │
                                                                        │   Return Data   │
                                                                        ├<────────────────┘
                                                                        │
                                                                        ▼
                                                              [ View / Serializer ]
                                                                        │
  [ Client Browser ] <── Send JSON (200 OK) ────────────────────────────┘
```

## Real-World Example
Suppose a user requests their profile details. The router maps the request `GET /users/42` to the user controller. The controller extracts the ID parameter, calls the User Model to fetch the data from the database, and passes the database record to the JSON view serializer. This ensures that database changes do not break routing, and route changes do not modify database schemas.

## Code Examples

### Decoupled MVC Implementation

```javascript
// models/User.js (Model Layer)
// Mock database array representing a data store
const usersDatabase = [
  { id: 1, name: 'Alice', email: 'alice@db.com' }
];

class UserModel {
  static async findById(id) {
    // Simulates an asynchronous database query
    return usersDatabase.find(user => user.id === id) || null;
  }

  static async create(data) {
    const newUser = { id: usersDatabase.length + 1, ...data };
    usersDatabase.push(newUser);
    return newUser;
  }
}
module.exports = UserModel;
```

```javascript
// controllers/userController.js (Controller Layer)
const UserModel = require('../models/User');

exports.getUserProfile = async (req, res, next) => {
  try {
    const userId = parseInt(req.params.id, 10);
    const user = await UserModel.findById(userId);
    
    if (!user) {
      return res.status(404).json({ error: 'User profile not found' });
    }
    
    // View/Presentation logic is handled by res.json() serialization
    res.status(200).json(user);
  } catch (err) {
    next(err); // Forward server errors to the global error handler
  }
};
```

```javascript
// routes/userRoutes.js (Routing Layer)
const express = require('express');
const router = express.Router();
const userController = require('../controllers/userController');

// Routes only define paths and link them to controllers
router.get('/users/:id', userController.getUserProfile);

module.exports = router;
```

## Best Practices
* **Keep Controllers Thin**: Controllers should only handle input validation, call models, and return responses. Keep business logic and complex calculations inside your models or dedicated service modules.
* **Keep Models Protocol-Agnostic**: Models should never references Express objects like `req` or `res`. They should only receive parameters and return raw data.
* **Enforce Strict Boundaries**: Ensure layers communicate only in one direction: Routing calls Controllers, Controllers call Models, and Models interact with the Database.

## Interview Questions

### Beginner
* **What does MVC stand for, and what is the primary role of each component?**
  *Answer*: MVC stands for Model-View-Controller.
  * **Model**: Manages data structures, validation schemas, and database queries.
  * **View**: Formats and presents the output data (e.g. templates or JSON responses) to the client.
  * **Controller**: Orchestrates the process: receives client input, calls the model, and passes the output to the view.

### Intermediate
* **Why should Models be kept protocol-agnostic (never referencing `req` or `res`)?**
  *Answer*: Models handle data access and business rules, which should be independent of the delivery mechanism. If a Model references `req` or `res`, it becomes tightly coupled to Express. Keeping it protocol-agnostic allows you to reuse the Model class in CLI tools, background workers, or unit tests without importing Express.

### Advanced
* **What are the architectural benefits of decoupling route definitions from controller functions, and how does this improve unit testing?**
  *Answer*: Decoupling route definitions from controllers isolates routing configurations from business logic. This separation allows you to test controller functions independently by mocking the `req`, `res`, and `next` parameters, without needing to spin up an HTTP server or route requests through the entire Express stack, simplifying unit testing.

### Senior Architect
* **In a highly scaled enterprise codebase, why can standard MVC patterns lead to fat controllers and bloated models? How do you refactor MVC into a Clean Architecture or Service-Repository pattern?**
  *Answer*: In large enterprise systems, business logic often overlaps multiple data queries, leading to bloated controllers that handle transaction orchestration and data formatting, and models that house complex business validation rules.
  
  To solve this, we introduce the **Service-Repository** pattern to decouple the MVC layers further:
  1. **Repository Layer**: Acts as an abstraction over the ORM or database queries, exposing simple methods (like `userRepository.findById(id)`).
  2. **Service Layer**: Houses the actual business logic. It coordinates transactions, updates multiple models, and sends notifications (e.g., `registrationService.registerUser(data)`).
  3. **Controller Layer**: Becomes a lightweight interface that simply parses request inputs, calls the appropriate Service, and formats the output, keeping the codebase clean and modular.

---
Previous : [26_Routing.md] | Index : [00_index.md] | Next : [28_Environment_Variables.md]
