# Jest

## What You Will Learn
* Configuring Jest for Node.js backends (`jest.config.js`).
* Utilizing standard matchers (`toBe`, `toEqual`, `toThrow`, `toHaveBeenCalledWith`).
* Managing test lifecycle hooks (`beforeAll`, `afterAll`, `beforeEach`, `afterEach`).
* Implementing Snapshot Testing.
* Enforcing Code Coverage thresholds in project configurations.

## Why This Matters
Jest is the most popular testing framework in the JavaScript ecosystem. It provides a test runner, assertion library, code coverage engine, and mock framework in a single package. Understanding how to configure Jest, use the correct matchers, and set up coverage thresholds ensures your test suite is fast, reliable, and maintains high standards.

## Theory

### Core Matchers
Jest uses "matchers" to let you assert values in different ways:
* **`toBe()`**: Checks for strict equality using `Object.is` (ideal for primitive types like strings, numbers, or booleans).
* **`toEqual()`**: Performs a deep comparison of object properties and array elements (ideal for comparing objects or arrays).
* **`toThrow()`**: Verifies that a function throws an exception when invoked.
* **`toHaveBeenCalledWith()`**: Asserts that a spy or mock function was called with specific arguments.

### Test Lifecycle Hooks
Jest executes hooks in a predictable sequence to manage setup and teardown:
* **`beforeAll`**: Runs once before any tests in the file start (ideal for establishing database pools).
* **`beforeEach`**: Runs before each individual test case (ideal for seeding test data or resetting mocks).
* **`afterEach`**: Runs after each individual test case (ideal for cleaning up test data).
* **`afterAll`**: Runs once after all tests in the file complete (ideal for closing database connections).

## Deep Dive

### Snapshot Testing
**Snapshot Testing** is a feature where Jest saves the rendered output of a data structure to a reference file (a snapshot, e.g. `__snapshots__/user.test.js.snap`).
* On subsequent test runs, Jest compares the new output with the stored snapshot. If they do not match, the test fails, alerting you that the output structure has changed.
* You can update snapshots by running the test runner with the `-u` flag: `jest -u`.
* *Use Case*: Testing complex static outputs, API response schemas, or configuration objects. Avoid using snapshots for highly dynamic data (like timestamps or UUIDs) as they will cause tests to fail constantly.

## Visual Explanation

### Jest Lifecycle Execution Flow
```text
[ File Execution Starts ]
           │
           ▼
     [ beforeAll ] (Runs once)
           │
     ┌─────┴─────────────────────────────────────┐
     ▼                                           ▼
[ Test Case 1 ]                             [ Test Case 2 ]
  ├── beforeEach                              ├── beforeEach
  ├── run test logic                          ├── run test logic
  └── afterEach                               └── afterEach
     ▲                                           ▲
     └─────────────────────┬─────────────────────┘
                           │
                           ▼
                      [ afterAll ] (Runs once)
                           │
                           ▼
                [ File Execution Ends ]
```

## Real-World Example
Consider an API endpoint `/settings` that returns a complex configuration JSON object. Instead of writing dozens of assertions to check every single property nested in the object, you write a snapshot test: `expect(config).toMatchSnapshot()`. Jest saves the configuration structure, and alerts you if any properties are accidentally modified or deleted during future updates.

## Code Examples

### Jest Configurations and Assertions

```javascript
// jest.config.js
module.exports = {
  // Enforce the Node.js execution environment (disables browser globals like window)
  testEnvironment: 'node',
  
  // Show detailed test execution results in the console
  verbose: true,

  // Automatically clear mock history between tests
  clearMocks: true,

  // Collect test coverage statistics
  collectCoverage: true,
  coverageDirectory: 'coverage',
  collectCoverageFrom: ['src/**/*.js', '!src/**/*.test.js'],

  // Enforce minimum test coverage thresholds (build fails if coverage drops below limits)
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: -10 // Allow at most 10 uncovered statements
    }
  }
};
```

```javascript
// tests/jest-demo.test.js
// Run tests using: npx jest tests/jest-demo.test.js

const generateUserProfile = (id, username) => {
  if (!id || !username) {
    throw new Error('Invalid input details');
  }
  return {
    id,
    username,
    role: 'user',
    preferences: { theme: 'dark' }
  };
};

describe('Jest Assertions and Lifecycle Demo', () => {
  let dbConnectionMock;

  beforeAll(() => {
    // Simulating database pool connection
    dbConnectionMock = { connected: true };
  });

  afterAll(() => {
    // Clean up connection
    dbConnectionMock = null;
  });

  // 1. Testing Primitive Equality (toBe)
  test('Should return correct database connection status flag', () => {
    expect(dbConnectionMock.connected).toBe(true);
  });

  // 2. Testing Deep Object Equality (toEqual)
  test('Should return correctly structured user profile payload', () => {
    const profile = generateUserProfile(101, 'Alice');
    
    // expect(profile).toBe(...) would fail here because they are separate objects in memory
    expect(profile).toEqual({
      id: 101,
      username: 'Alice',
      role: 'user',
      preferences: { theme: 'dark' }
    });
  });

  // 3. Testing Exception Throws (toThrow)
  test('Should throw an error if input details are invalid', () => {
    // Wrapped in a callback so Jest can catch the error during execution
    expect(() => {
      generateUserProfile(null, 'Alice');
    }).toThrow('Invalid input details');
  });

  // 4. Snapshot Testing (toMatchSnapshot)
  test('Should match the stored user profile schema snapshot', () => {
    const profile = generateUserProfile(42, 'Bob');
    // Saves a copy of the return object in tests/__snapshots__/jest-demo.test.js.snap
    expect(profile).toMatchSnapshot();
  });
});
```

## Best Practices
* **Use Node Test Environment**: Always configure `testEnvironment: 'node'` in your Jest settings for backend services.
* **Enforce Coverage Thresholds**: Configure coverage thresholds in your CI/CD pipelines to prevent developers from adding code without tests.
* **Do Not Snapshot Dynamic Values**: Strip or mock dynamic values (like UUIDs, timestamps, or random hashes) before running snapshot assertions to prevent false test failures.

## Interview Questions

### Beginner
* **What is the difference between `toBe()` and `toEqual()` in Jest?**
  *Answer*: `toBe()` checks for strict equality using `Object.is`, which is suitable for primitive types (numbers, strings, booleans). `toEqual()` performs a deep comparison of properties in objects and elements in arrays, which is suitable for comparing reference types.

### Intermediate
* **What are Jest lifecycle hooks and when would you use `beforeAll` vs `beforeEach`?**
  *Answer*: Jest lifecycle hooks run setup and teardown tasks around tests. You use `beforeAll` once before any tests in the file execute, making it ideal for starting databases or server connections. You use `beforeEach` before each individual test case runs, making it ideal for resetting mocks or seeding clean table states.

### Advanced
* **What is Snapshot Testing in Jest? When should you use it, and what are its main limitations?**
  *Answer*: Snapshot Testing compares a rendered data structure or component output against a stored reference snapshot file. It is useful for verifying complex JSON payloads or configurations. 
  The main limitation is that snapshots fail when they encounter dynamic data (like timestamps, auto-incrementing IDs, or random hashes). Additionally, snapshots can easily be updated blindly without review, missing regression bugs.

### Senior Architect
* **How would you configure Jest to run integration tests sequentially (in a single process) while running unit tests concurrently in multiple worker threads, explaining the rationale behind this configuration?**
  *Answer*: To run unit and integration tests under different execution rules:
  1. **Configure Projects**: Use Jest's `projects` configuration to split tests into separate workspace runs:
     ```javascript
     // jest.config.js
     module.exports = {
       projects: [
         {
           displayName: 'unit',
           testMatch: ['<rootDir>/tests/unit/**/*.test.js'],
           testEnvironment: 'node'
           // Runs concurrently in parallel threads
         },
         {
           displayName: 'integration',
           testMatch: ['<rootDir>/tests/integration/**/*.test.js'],
           testEnvironment: 'node',
           runInBand: true // Forces sequential execution
         }
       ]
     };
     ```
  2. **Rationale**: Unit tests are stateless and run in memory, so they can run concurrently in parallel threads to speed up the test runner. Integration tests share a single database, so running them concurrently can cause write conflicts and data pollution. Running integration tests sequentially (`runInBand: true`) prevents collisions and keeps the database state clean.

---
Previous : [65_Integration_Testing.md] | Index : [00_index.md] | Next : [67_Supertest.md]
