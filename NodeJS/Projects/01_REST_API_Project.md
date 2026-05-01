# 📌 Project: Production-Grade REST API

## 🧠 Concept Explanation
A production API is more than just routes; it's a **Layered Architecture**.
**Analogy:** 
- **Controller (The Waiter):** Takes the request, validates the order, and passes it to the kitchen.
- **Service (The Chef):** Handles the business logic (cooking the food).
- **Repository (The Pantry):** Interacts with the database (getting the ingredients).
By separating these, you can change the "Ingredients" (The DB) without teaching the "Chef" a new recipe.

---

## 🏗️ Mental Model
- **Framework:** Fastify (Faster than Express) or Express.
- **ORM:** Prisma or TypeORM.
- **Validation:** Zod.
- **Documentation:** Swagger (OpenAPI).
- **Structure:** `src/controllers`, `src/services`, `src/repositories`, `src/middlewares`.

---

## ⚡ Actual Behavior
*   **Request Lifecycle:** Auth Middleware -> Validation Middleware -> Controller -> Service -> Repository -> Database.
*   **Unified Error Handling:** All errors are caught and transformed into a standard JSON format.
*   **Dependency Injection:** Services are passed into controllers to make them easy to test.

---

## 🔬 Internal Mechanics (V8 + libuv + OS)
*   **Middleware Stack:** We use a high-performance middleware stack to minimize the overhead per request.
*   **Asynchronous Flow:** Every layer is `async/await` to ensure non-blocking I/O throughout the entire stack.

---

## 🔁 Execution Flow
1.  **Incoming:** `POST /api/v1/users`.
2.  **Middleware:** JWT verified; rate limit checked.
3.  **Validation:** Zod ensures `email` and `password` are valid.
4.  **Controller:** Extracts data from `req.body` and calls `userService.createUser()`.
5.  **Service:** Hashes the password and calls `userRepository.save()`.
6.  **Repository:** Prisma executes the SQL `INSERT`.
7.  **Response:** Controller returns `201 Created` with the new user ID.

---

## 🧠 Resource Behavior
*   **CPU:** Peak during password hashing (Bcrypt) and JSON serialization.
*   **Memory:** Stable, managed by V8.

---

## 📐 ASCII Diagrams
```text
[ CLIENT ] --(HTTP)--> [ CONTROLLER ]
                           |
                     [ SERVICE LAYER ] (Business Logic)
                           |
                     [ REPOSITORY ] (Data Access)
                           |
                     [ DATABASE ]
```

---

## 🔍 Code Example (Latest Node.js - Project Skeleton)
```javascript
// src/services/userService.js
export class UserService {
  constructor(userRepository) {
    this.userRepository = userRepository;
  }

  async registerUser(userData) {
    const hashedPassword = await argon2.hash(userData.password);
    return this.userRepository.create({ ...userData, password: hashedPassword });
  }
}

// src/controllers/userController.js
export const register = async (req, res, next) => {
  try {
    const service = new UserService(new UserRepository());
    const user = await service.registerUser(req.body);
    res.status(201).json(user);
  } catch (err) {
    next(err); // Centralized error handling
  }
};
```

---

## 💥 Production Failures
*   **Circular Dependencies:** Service A needs B, and B needs A, causing Node.js to fail at startup.
*   **Fat Controllers:** Putting 500 lines of logic inside a single route handler, making it impossible to test or reuse.
*   **Uncaught Rejections:** Forgetting `try/catch` in an async controller, crashing the process on the first error.

---

## 🧪 Real-time Scenarios
*   **User Registration:** The classic flow including validation, hashing, and DB storage.
*   **Product Search:** Implementing pagination and filtering in the Repository layer.

---

## ⚠️ Edge Cases
*   **Transaction Management:** Ensuring that if the DB save fails, the profile picture uploaded to S3 is deleted (Atomic operations).
*   **Request Timeouts:** Setting a global timeout to ensure a slow DB query doesn't hang the request forever.

---

## 🏢 Best Practices
1.  **Use TypeScript:** For type safety in large codebases.
2.  **Write Integration Tests:** Use Supertest to test the whole flow from Controller to DB.
3.  **Implement Logging:** Use Pino to log every request and error.
4.  **Graceful Shutdown:** Handle `SIGTERM` to close DB connections cleanly.

---

## ⚖️ Trade-offs
*   **Layered Architecture:** More files and boilerplate, but much easier to maintain and scale as the project grows.
*   **Flat Structure:** Fast to build, but becomes a "spaghetti" mess after 6 months.

---

## 💼 Interview Q&A
*   **Q:** Why use a Service layer?
*   **A:** To separate business logic from the transport layer (HTTP). This allows you to call the same logic from a CLI tool, a WebSocket, or an HTTP route without duplicating code.

---

## 🧩 Practice Problems
1.  Build a simple "Task Manager" API using this layered structure.
2.  Add a "Logger Middleware" that prints the execution time of every service method.

---
Prev: [../Cloud/05_Scaling_on_AWS.md](../Cloud/05_Scaling_on_AWS.md) | Index: [NodeJS/00_Index.md](../00_Index.md) | Next: [02_RealTime_Chat_App.md](./02_RealTime_Chat_App.md)
