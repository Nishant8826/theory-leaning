# 📌 02 — Integration Testing: Validating Component Synergy

## 🧠 Concept Explanation

### Basic → Intermediate
Integration Testing verifies that different parts of your application work together correctly (e.g. "Does my Express route correctly save to the real Postgres database?").

### Advanced → Expert
At a staff level, integration testing is about **Environmental Parity**. 
1. **Real Dependencies**: Use real databases and message brokers (usually via Docker) instead of mocks.
2. **State Management**: Each test must start with a "Clean Slate." This involves wiping the database or using transactions that roll back after each test.
3. **API Level Testing**: Using tools like **Supertest** to make actual HTTP requests to your app and verify the status codes and JSON response.

---

## 🏗️ Common Mental Model
"Integration tests are slow, so I'll only run them once a day."
**Correction**: With modern tools like **Testcontainers**, you can spin up a fresh Redis or Postgres in seconds. Integration tests should be part of your local development cycle and your CI/CD pipeline.

---

## ⚡ Actual Behavior: The "Network Partition" Simulation
Integration tests are the perfect place to test how your app handles dependency failures. You can use a proxy like **Toxiproxy** to simulate slow database connections or broken network pipes during a test.

---

## 🔬 Internal Mechanics (Docker + Node.js)

### Testcontainers
A library that allows you to manage Docker containers directly from your Node.js code.
```javascript
const { GenericContainer } = require("testcontainers");

const redisContainer = await new GenericContainer("redis")
  .withExposedPorts(6379)
  .start();
```

---

## 📐 ASCII Diagrams

### Integration Testing Scope
```text
  ┌─────────────────────────────────────────────────────────────┐
  │                   INTEGRATION TEST SCOPE                    │
  │                                                             │
  │  ┌───────────────┐        ┌───────────────┐        ┌─────┐  │
  │  │   API ROUTE   │ ──▶ ── │   SERVICE     │ ──▶ ── │ DB  │  │
  │  └───────────────┘        └───────────────┘        └─────┘  │
  │                                                            │
  └─────────────────────────────────────────────────────────────┘
```

---

## 🔍 Code Example: API Testing with Supertest and Postgres
```javascript
const request = require('supertest');
const app = require('../app');
const db = require('../db');

describe('POST /users', () => {
  // Before each test, wipe the users table
  beforeEach(async () => {
    await db('users').truncate();
  });

  it('should create a user in the database', async () => {
    const res = await request(app)
      .post('/users')
      .send({ username: 'antigravity', email: 'ai@google.com' });

    expect(res.status).toBe(201);
    
    // VERIFY with a real DB query
    const user = await db('users').where({ username: 'antigravity' }).first();
    expect(user).toBeDefined();
    expect(user.email).toBe('ai@google.com');
  });
});
```

---

## 💥 Production Failures & Debugging

### Scenario: The "Dirty DB" Bug
**Problem**: Test A fails only if Test B runs before it.
**Reason**: Test B added data to the database that Test A didn't expect.
**Fix**: Use `beforeEach` to clean the database or run each test inside a **DB Transaction** and roll it back at the end.

### Scenario: The Port Conflict
**Problem**: You cannot run tests in parallel because they all try to listen on port 3000.
**Reason**: Hardcoded ports in the test environment.
**Fix**: Use port `0` in your server listen call. This tells the OS to assign a random available port.

---

## 🧪 Real-time Production Q&A

**Q: "Should I test external APIs (like Stripe) in my integration tests?"**
**A**: **No.** That makes your tests dependent on the internet and Stripe's uptime. Use a **Mock Server** (like `msw` or `nock`) that returns a real HTTP response but doesn't actually hit the external network.

---

## 🏢 Industry Best Practices
- **Test the "Happy Path" and "Edge Cases"**: Integration tests should cover valid input, invalid input, and database errors.
- **Run in Parallel**: Use a test runner that supports parallel execution to keep your feedback loop fast.

---

## 💼 Interview Questions
**Q: What is the difference between a "Sanity Test" and an "Integration Test"?**
**A**: A **Sanity Test** is a quick check to see if the main functionality works after a change (e.g. "Can I still log in?"). An **Integration Test** is a detailed verification of the interaction between specific components.

---

## 🧩 Practice Problems
1. Set up a test suite using `supertest` that validates a CRUD API. Use a local SQLite database for the tests.
2. Use `nock` to simulate a 500 error from an external Weather API and verify that your app handles it gracefully.

---

**Prev:** [01_Unit_Testing_Patterns.md](./01_Unit_Testing_Patterns.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [03_Load_and_Stress_Testing.md](./03_Load_and_Stress_Testing.md)
