# 📌 01 — Unit Testing Patterns: Isolation and Determinism

## 🧠 Concept Explanation

### Basic → Intermediate
Unit Testing is testing the smallest "unit" of code (usually a function or a class) in isolation. We use frameworks like **Jest** or **Mocha** to define test cases and assertions.

### Advanced → Expert
At a staff level, unit testing is about **Controllable Isolation**. 
1. **Determinism**: A test must give the same result every time. This means mocking "side effects" like Time (`Date.now`), Randomness, and Network calls.
2. **Mocking vs Spying**: 
   - **Mock**: Replaces a dependency (e.g. Database) with a fake implementation.
   - **Spy**: Wraps a real dependency to observe its behavior (e.g. "Was this function called?").
3. **Pure Functions**: The easiest code to test is code that has no side effects and returns a value based solely on its inputs.

---

## 🏗️ Common Mental Model
"I'll test my function by calling the database and checking the result."
**Correction**: That is an **Integration Test**. A **Unit Test** should not touch the network or disk. If your database is slow, your unit tests become slow, and developers will stop running them.

---

## ⚡ Actual Behavior: The "Mocking Trap"
If you mock everything, you might end up testing your **mocks** instead of your **code**. If the real database API changes but your mock stays the same, your tests will pass while your production code fails. 

---

## 🔬 Internal Mechanics (V8 + Testing)

### Dependency Injection (DI)
To make code testable, you should pass dependencies as arguments (or via a constructor) rather than `require`-ing them directly inside the function. This allows the test to "inject" a mock easily.

---

## 📐 ASCII Diagrams

### Unit Testing Isolation
```text
  ┌───────────────────────────┐
  │      TEST RUNNER          │
  └─────────────┬─────────────┘
                ▼
  ┌───────────────────────────┐      ┌───────────────────────────┐
  │   UNIT UNDER TEST (UUT)   │ ◀─── │      MOCK OBJECT          │
  │   (Your Function)         │      │ (Fake DB / Fake API)      │
  └───────────────────────────┘      └───────────────────────────┘
```

---

## 🔍 Code Example: Mocking with Jest
```javascript
// user.service.js
class UserService {
  constructor(db) { this.db = db; } // Dependency Injection

  async getStatus(userId) {
    const user = await this.db.findById(userId);
    return user.isActive ? 'Active' : 'Inactive';
  }
}

// user.service.test.js
test('should return Active for active user', async () => {
  // 1. Create a MOCK dependency
  const mockDb = {
    findById: jest.fn().mockResolvedValue({ isActive: true })
  };

  const service = new UserService(mockDb);
  
  // 2. Execute
  const status = await service.getStatus(123);
  
  // 3. Assert
  expect(status).toBe('Active');
  expect(mockDb.findById).toHaveBeenCalledWith(123);
});
```

---

## 💥 Production Failures & Debugging

### Scenario: The "Flaky" Test
**Problem**: A test passes locally but fails randomly in CI/CD.
**Reason**: The test depends on the current time (`new Date()`) or an external API that is sometimes slow.
**Fix**: Mock the system clock using `jest.useFakeTimers()` or a library like `timekeeper`.

### Scenario: The "Brittle" Test
**Problem**: Every time you refactor a small internal variable name, 50 tests break.
**Reason**: Your tests are "too close" to the implementation. They are checking internal private variables instead of the public output.
**Fix**: Test **Behavior**, not **Implementation**. Only assert on the inputs and outputs of the function.

---

## 🧪 Real-time Production Q&A

**Q: "Should I aim for 100% Code Coverage?"**
**A**: **No.** 100% coverage often leads to low-quality tests that just satisfy the tool. Aim for **80-90%**, focusing on critical business logic and edge cases. High coverage on simple getters/setters is a waste of time.

---

## 🏢 Industry Best Practices
- **Arrange-Act-Assert (AAA)**: Structure your tests clearly: Set up the data, run the function, check the result.
- **Independent Tests**: One test should not depend on the result of another test.

---

## 💼 Interview Questions
**Q: What is the difference between a Stub and a Mock?**
**A**: A **Stub** provides a predefined response to a call (it's passive). A **Mock** also verifies that a specific call was made with specific arguments (it's active and assertive).

---

## 🧩 Practice Problems
1. Take a function that uses `axios` to fetch data and refactor it to use Dependency Injection. Write a unit test that mocks the axios call.
2. Use `jest.useFakeTimers()` to test a function that has a 30-second `setTimeout`.

---

**Prev:** [../Security/05_Security_Headers_Helmet.md](../Security/05_Security_Headers_Helmet.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [02_Integration_Testing_Strategies.md](./02_Integration_Testing_Strategies.md)
