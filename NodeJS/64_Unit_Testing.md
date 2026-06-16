# Unit Testing

Unit tests are the foundation of your testing suite. Because they execute in memory and mock all external resources (like databases and API servers), they run in milliseconds, giving you instant feedback during development. Writing effective unit tests keeps your code modular and makes refactoring safe and fast.

### Unit Testing Isolation
A **Unit Test** verifies the behavior of a single unit of source code (such as a function, method, or class) in isolation.
* **The Rule**: The unit under test must not communicate with external systems (like databases, filesystems, or networks).
* **The Solution**: All dependencies must be mocked. For example, if a function reads a file and queries a database, the filesystem module (`fs`) and the database client are replaced with mock objects during the test.

### Mocking in Jest
Jest is a comprehensive testing framework that provides built-in tools to create mocks and spies:
* **`jest.fn()`**: Creates a mock function that records calls, arguments, and return values, allowing you to simulate callbacks or mock dependencies.
* **`jest.mock('module-name')`**: Replaces an entire module (like `axios` or `fs`) with a mock version, preventing it from making actual network or disk calls.
* **`jest.spyOn(object, 'method')`**: Spies on an existing object method, recording call details while preserving the original implementation (or allowing you to mock it temporarily).

## Deep Dive

### Testing Asynchronous Code
Asynchronous code (Promises and `async/await`) must be tested carefully to prevent test runners from ending the test before the asynchronous operation completes:
* **Async/Await**: Declare the test callback as `async` and use the `await` keyword on the function under test.
* **Reject Assertions**: Use Jest's `.rejects.toThrow()` matcher to verify that a function throws the correct error when a Promise rejects.

## Visual Explanation

### Mocking Module Boundaries
```text
Production Environment:
[ controller.js ] ── imports ──> [ axios (Makes physical HTTP request to api.com) ]

Unit Test Environment:
[ controller.test.js ] ──> mock('axios') ──> Replaces Axios with Jest Mock Object
                                                   │
                                                   ▼ (Returns predefined mock data in RAM)
[ controller.js ] ── imports ──> [ Axios Mock Object ] (Fast, zero network dependency)
```

## Real-World Example
Consider an authentication helper function `generateVerificationToken`. It reads user details and generates a token containing a timestamp. In a unit test, you mock the system clock (using `jest.useFakeTimers()`) to freeze the timestamp, ensuring the generated token is deterministic and easy to assert.

## Code Examples

### Unit Testing Async functions and Mocking Dependencies with Jest

```javascript
// services/userService.js
const axios = require('axios');

class UserService {
  constructor(dbConnection) {
    this.db = dbConnection;
  }

  async fetchAndSaveExternalUser(userId) {
    // 1. Fetch user data from external API (HTTP dependency)
    const response = await axios.get(`https://api.users.com/v1/${userId}`);
    const externalUser = response.data;

    if (!externalUser || !externalUser.email) {
      throw new Error('Invalid user payload returned from API');
    }

    // 2. Write record to local database (DB dependency)
    const savedUser = await this.db.save({
      email: externalUser.email,
      name: externalUser.name,
      status: 'active'
    });

    return savedUser;
  }
}
module.exports = UserService;
```

```javascript
// tests/userService.test.js
// Run this file using Jest: npm install jest && npx jest tests/userService.test.js

const axios = require('axios');
const UserService = require('../services/userService');

// Mock the entire 'axios' module to prevent actual network calls
jest.mock('axios');

describe('UserService Unit Tests', () => {
  let mockDb;
  let userService;

  beforeEach(() => {
    // Reinitialize mock database client before each test
    mockDb = {
      save: jest.fn().mockResolvedValue({ id: 1, email: 'test@db.com', status: 'active' })
    };
    userService = new UserService(mockDb);
  });

  afterEach(() => {
    jest.clearAllMocks(); // Clear mock execution statistics
  });

  test('Should successfully fetch and save external user profile data', async () => {
    // Configure axios mock response
    axios.get.mockResolvedValue({
      data: { name: 'Bob', email: 'test@db.com' }
    });

    const result = await userService.fetchAndSaveExternalUser(42);

    // 1. Assertions on the return value
    expect(result).toEqual({ id: 1, email: 'test@db.com', status: 'active' });

    // 2. Assertions on mock dependencies (Behavior Verification)
    expect(axios.get).toHaveBeenCalledWith('https://api.users.com/v1/42');
    expect(mockDb.save).toHaveBeenCalledTimes(1);
    expect(mockDb.save).toHaveBeenCalledWith({
      email: 'test@db.com',
      name: 'Bob',
      status: 'active'
    });
  });

  test('Should throw an error if the external API returns an invalid payload', async () => {
    // Configure axios mock to return data missing the email field
    axios.get.mockResolvedValue({
      data: { name: 'Bob' } // Missing email
    });

    // Verify that the async function throws the correct error
    await expect(userService.fetchAndSaveExternalUser(42)).rejects.toThrow(
      'Invalid user payload returned from API'
    );

    // Verify that the database was not called (Rollback check)
    expect(mockDb.save).not.toHaveBeenCalled();
  });
});
```

## Best Practices
* **Mock Every Dependency**: Ensure your unit tests do not make actual database connections, filesystem calls, or network requests. Mock these dependencies to keep tests fast and reliable.
* **Isolate Test States**: Clear mock history (`jest.clearAllMocks()`) or reset mocks (`jest.resetAllMocks()`) in `afterEach` hooks to prevent test cases from interfering with each other's assertions.
* **One Behavior per Test**: Focus each test case on a single logical behavior or code branch to make identifying failures easy.

## Interview Questions

**Q:** What is a unit test, and what is its primary rule?

> **Answer:**
> A unit test is a test that verifies the behavior of a single, isolated function or class. The primary rule of unit testing is isolation: the code under test must not interact with external systems (like databases, networks, or filesystems), and all dependencies must be mocked.

**Q:** What is the difference between `jest.mock()` and `jest.spyOn()`?

> **Answer:**
> `jest.mock('module-name')` replaces an entire module with a mock version, preventing its real implementation from running. `jest.spyOn(object, 'method')` wraps an existing object method in a spy, recording execution statistics (like call counts and arguments) while preserving the original implementation (unless you explicitly mock the return value).

**Q:** How do you test that an asynchronous function throws an error (rejects) when using Jest? Provide a code example.

> **Answer:**
> You can test that an asynchronous function rejects by using `await` with Jest's `.rejects.toThrow()` matcher:
> ```javascript
> test('Should throw error on rejection', async () => {
> const failingFunction = async () => { throw new Error('Failed'); };
> await expect(failingFunction()).rejects.toThrow('Failed');
> });
> ```
> This ensures that the test runner awaits the Promise resolution and asserts the thrown error correctly.

**Q:** How would you configure Jest to handle module resolution aliases (e.g. importing files using `@/services/user` paths) and isolate module mocks dynamically across isolated test files?

> **Answer:**
> To configure Jest for module aliases and dynamic mocks:
> 1. Configure `moduleNameMapper` in your `jest.config.js` to map alias paths to physical directories:
> ```javascript
> module.exports = {
> moduleNameMapper: {
> '^@/(.*)$': '<rootDir>/src/$1'
> }
> };
> ```
> 2. To isolate mocks dynamically across files, ensure Jest is configured to run tests in parallel processes (the default behavior). Each test file executes in its own isolated OS process with its own V8 context, preventing mocks declared in one file from bleeding into other test files.
> 3. Use `jest.doMock()` inside test cases if you need to define dynamic, context-specific module mocks at runtime inside the same file, bypassing the standard hoisted `jest.mock()` configuration.

---
Previous : [63_Testing_Fundamentals.md](63_Testing_Fundamentals.md) | Index : [00_index.md](00_index.md) | Next : [65_Integration_Testing.md](65_Integration_Testing.md)
