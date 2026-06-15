# OWASP Top Risks

## What You Will Learn
* Overview of the OWASP Top 10 Web Application Security Risks in Node.js.
* Identifying and defending against Injection vulnerabilities.
* Securing applications against Broken Access Control and privilege escalation.
* Preventing Cryptographic Failures and Security Misconfigurations.
* Integrating security scanners into development workflows.

## Why This Matters
The Open Web Application Security Project (OWASP) compiles a list of the ten most critical security risks for web applications. Attackers actively scan applications for these vulnerabilities. Understanding how these risks manifest in Node.js code allows you to implement defensive programming practices and prevent security breaches.

## Theory

### Key OWASP Risks in Node.js Applications

#### 1. A01:2021-Broken Access Control
* **The Risk**: Users can access resources outside their intended permissions (e.g. standard users hitting admin endpoints or accessing other users' records - IDOR).
* **Mitigation**: Implement strict authentication and authorization checks at the API boundary, and verify resource ownership in controllers.

#### 2. A02:2021-Cryptographic Failures
* **The Risk**: Storing sensitive data in plain-text, using weak hashing algorithms (like MD5), or failing to encrypt data in transit.
* **Mitigation**: Use strong hashing algorithms (like Argon2id) for passwords, encrypt sensitive database columns using AES-256-GCM, and force HTTPS.

#### 3. A03:2021-Injection (SQL, NoSQL, and OS Command)
* **The Risk**: Parsing untrusted user inputs directly into query engines or shell commands, allowing attackers to execute arbitrary code or queries.
* **Mitigation**: Use parameterized queries, sanitize inputs, and avoid using shell execution functions.

#### 4. A05:2021-Security Misconfiguration
* **The Risk**: Running applications with default settings, exposing debug endpoints in production, or sending detailed stack traces in error messages.
* **Mitigation**: Disable debugging headers, sanitize error messages in production, and change all default database settings.

#### 5. A06:2021-Vulnerable and Outdated Components
* **The Risk**: Using third-party npm packages containing known security vulnerabilities.
* **Mitigation**: Integrate dependency scanners (like `npm audit` or Snyk) into your build pipelines.

## Deep Dive

### Securing Error Handlers against Misconfigurations
A common security misconfiguration is returning database connection strings or execution stack traces in HTTP responses when a database query fails.
* **The Attack**: An attacker sends invalid inputs to trigger database exceptions, revealing database usernames, table structures, and internal code paths.
* **The Fix**: Implement environment-based error handling middleware. In production, log detailed stack traces internally and return a generic error message (like `"Internal Server Error"`) to the client, preventing data leaks.

## Visual Explanation

### OWASP Injection Attack Vector and Mitigation
```text
Insecure Execution (NoSQL Injection):
Query: User.findOne({ username: req.body.username, password: req.body.password })
Input: { "username": "admin", "password": { "$ne": "" } }  (Password not-equal to empty string operator)
Compiled Query: SELECT admin WHERE password != ""
Result: Attacker bypasses authentication and logs in as admin!

Secure Execution (Sanitized Input):
Query: User.findOne({ username: String(req.body.username), password: String(req.body.password) })
Input: { "username": "admin", "password": { "$ne": "" } }
Compiled Query: Lookup password literally as the string: '{"$ne": ""}'
Result: Authentication fails safely!
```

## Real-World Example
Consider an application that allows users to download invoices by sending an ID: `GET /invoices/download?id=101`. An attacker can alter the query parameters (`?id=102`) to download other users' invoices (Broken Access Control - IDOR). You prevent this by verifying that the invoice's owner ID matches the authenticated user ID (`req.user.id`) in the database query.

## Code Examples

### Defending Against NoSQL Injection and Information Leakage

```javascript
// secure-routes.js
const express = require('express');
const AppError = require('./utils/AppError');

const app = express();
app.use(express.json());

// Mock database
const users = [{ username: 'admin', passwordHash: 'secure_hash' }];

// 1. DANGEROUS: Vulnerable to NoSQL operator injection
app.post('/api/login-vulnerable', (req, res) => {
  // If attacker sends: { "username": "admin", "password": { "$ne": "" } }
  // MongoDB query: { username: "admin", password: { "$ne": "" } } resolves to true
  const query = {
    username: req.body.username,
    password: req.body.password
  };

  console.log('Executing query:', query);
  res.json({ message: 'Vulnerable query accepted' });
});

// 2. SECURE: Enforcing input validation and types
app.post('/api/login-secure', (req, res, next) => {
  const usernameInput = req.body.username;
  const passwordInput = req.body.password;

  // Enforce types explicitly (cast to string to prevent object injection)
  if (typeof usernameInput !== 'string' || typeof passwordInput !== 'string') {
    return next(new AppError('Bad Request: Invalid parameter types.', 400));
  }

  // Query is safe because parameters are guaranteed to be strings
  const query = {
    username: usernameInput,
    password: passwordInput
  };

  console.log('Executing secure query:', query);
  res.json({ message: 'Query parsed safely' });
});

// 3. SECURE: Preventing Information Exposure in Error Handlers
app.use((err, req, res, next) => {
  // Log the full stack trace internally
  console.error('[INTERNAL ERROR LOG]:', err.stack);

  const statusCode = err.statusCode || 500;
  
  if (process.env.NODE_ENV === 'production') {
    // Hide internal details in production
    res.status(statusCode).json({
      error: 'Server Error',
      message: 'An unexpected error occurred. Please try again later.'
    });
  } else {
    // Show full stack trace in development
    res.status(statusCode).json({
      error: err.message,
      stack: err.stack
    });
  }
});

app.listen(3000, () => console.log('OWASP Demo Server running on port 3000'));
```

## Best Practices
* **Enforce Parameter Types**: Always validate and cast incoming request parameters to strings or numbers before passing them to database queries to prevent NoSQL injection.
* **Implement Least Privilege Access**: Default all endpoints to be private, and require explicit authentication and authorization tokens to access resources.
* **Sanitize Error Payloads**: Never expose database structures, query parameters, or execution stack traces to clients in production errors.
* **Audit regularly**: Run dependency audits (`npm audit`) and static analysis security scans (like Snyk) regularly to identify and resolve vulnerabilities.

## Interview Questions

### Beginner
* **What is OWASP and why is it important for backend security?**
  *Answer*: OWASP stands for the Open Web Application Security Project. It is a non-profit foundation that compiles the "OWASP Top 10", a list of the ten most critical security vulnerabilities in web applications, helping developers understand and prevent common security risks.

### Intermediate
* **What is a NoSQL Injection attack, and how do you prevent it in a MongoDB/Mongoose application?**
  *Answer*: A NoSQL Injection attack occurs when an attacker passes a query operator object (like `{ "$ne": "" }` - "not equal to empty string") instead of a string value inside request parameters. MongoDB evaluates the operator, bypassing checks like password validation. 
  To prevent NoSQL injection, validate request parameters using schema libraries (like Zod) or cast inputs to strings explicitly (e.g. `String(req.body.password)`) before querying the database, ensuring the engine treats them literally.

### Advanced
* **Explain the risk of Insecure Direct Object Reference (IDOR) and outline a multi-layered defense strategy to secure user resources.**
  *Answer*: IDOR is an access control vulnerability where an application uses database identifiers directly in URLs (e.g. `/api/invoices/:id`) and returns resources without verifying if the user has permission to access that record.
  * **Defense Strategy**:
    1. **Authentication**: Verify the client's identity and roles using JWT or Session checks.
    2. **Authorization Middleware**: Restrict route access to roles allowed to query that resource class.
    3. **Resource Ownership Verification**: In the database query, verify that the resource's owner ID matches the authenticated user ID (`req.user.id`), or query the resource filter directly (e.g., `Invoice.findOne({ _id: invoiceId, userId: req.user.id })`), preventing access leaks.

### Senior Architect
* **How would you secure a Node.js microservices cluster against OWASP Top Risks, considering network boundaries, service-to-service communication, and secret management?**
  *Answer*: To secure a microservices cluster:
  1. **API Gateway Boundary**: Enforce rate-limiting, SSL termination, and initial CORS validation at the API Gateway layer before traffic enters the cluster network.
  2. **Zero-Trust Communication**: Secure service-to-service calls using mutual TLS (mTLS) with validation tokens (like SPIFFE/SPIRE).
  3. **Least Privilege Processes**: Run all containers as non-root users (like the `node` user) with read-only filesystems.
  4. **Dynamic Secrets**: Retrieve and rotate credentials dynamically using a secure vault manager (like HashiCorp Vault), preventing credentials from leaking in code repositories.
  5. **Static Analysis**: Integrate security scans into CI/CD pipelines to block builds with high-severity vulnerabilities.

---
Previous : [55_Security_Fundamentals.md] | Index : [00_index.md] | Next : [57_Helmet.md]
