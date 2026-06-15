# Security Fundamentals

## What You Will Learn
* Implementing the Principle of Least Privilege in process execution.
* Scanning for vulnerabilities in third-party dependencies.
* Defending against Denial of Service (DoS) attacks.
* Proper sanitization and data escaping rules.
* Secure secrets management and rotation.

## Why This Matters
Security is not an afterthought; it must be built into your application's design. A single compromised dependency, a hardcoded API key committed to a repository, or a process running with root permissions can allow attackers to steal user data or gain control of your servers. Implementing security fundamentals protects your application from vulnerabilities.

## Theory

### Principle of Least Privilege
The **Principle of Least Privilege** states that a process must only have access to the resources and permissions it needs to perform its task, and no more.
* **Never Run Node as Root**: If your Node.js application runs with root permissions and is compromised (e.g. through a Remote Code Execution vulnerability), the attacker gains full control of the entire server. Always create a dedicated, non-root system user (e.g. `node`) to run your process.

### Dependency Security Auditing
Supply chain attacks (malicious updates to third-party npm packages) are a major risk. Use auditing tools to scan your dependency tree for vulnerabilities:
* **`npm audit`**: Scans your `package-lock.json` against the GitHub Advisory Database.
* **Snyk**: A security platform that integrates into your CI/CD pipelines to scan code, containers, and dependencies for vulnerabilities.

## Deep Dive

### Defending Against Denial of Service (DoS)
Attackers can exhaust server resources by sending large payloads or slow requests:
1. **Payload Size Limits**: Set maximum limits on incoming request bodies (e.g. 10KB for JSON payloads) to prevent attackers from sending huge payloads that exhaust server memory.
2. **Timeout Thresholds**: Set connection timeouts on your server sockets to close slow or idle connections quickly, preventing **Slowloris** attacks from consuming all available file descriptors.

## Visual Explanation

### Principle of Least Privilege Isolation
```text
Insecure Execution:
[ Node.js Process (Running as root) ] ── Exploit RCE ──> Gained Full OS root access!
                                                               │
                                                               ▼
                                                      Can read/delete any file

Secure Execution:
[ Docker Container ] ──> [ Node.js Process (Running as user 'node') ] ── Exploit RCE ──> Trapped in sandbox!
                                                                                           │
                                                                                           ▼
                                                                                   Access denied to root!
```

## Real-World Example
Consider storing a database password. If you write it directly in your code, any developer with repository access can see it. Instead, you store it in a secure cloud vaults manager (like AWS Secrets Manager or HashiCorp Vault) and inject it into the application's environment variables at runtime, ensuring secrets are isolated from the codebase.

## Code Examples

### Setting Body Limits, Timeouts, and Sanitizing Input Data

```javascript
// secure-server.js
// Dependencies required: npm install express xss
const express = require('express');
const xss = require('xss');
const AppError = require('./utils/AppError');

const app = express();

// 1. Defend against DoS: Limit payload size limits
app.use(express.json({ limit: '10kb' })); // Reject JSON bodies larger than 10KB
app.use(express.urlencoded({ extended: true, limit: '10kb' }));

// 2. Data Sanitization Middleware
// Prevents Cross-Site Scripting (XSS) by escaping HTML characters
const sanitizeInput = (req, res, next) => {
  if (req.body) {
    for (const key in req.body) {
      if (typeof req.body[key] === 'string') {
        req.body[key] = xss(req.body[key]); // Clean inputs
      }
    }
  }
  next();
};
app.use(sanitizeInput);

app.post('/api/feedback', (req, res) => {
  // If user sent: <script>alert('xss')</script>
  // Output is sanitized to: &lt;script&gt;alert('xss')&lt;/script&gt;
  res.json({
    message: 'Feedback received',
    sanitizedContent: req.body.content
  });
});

const server = http.createServer(app);

// 3. Defend against Slowloris: Configure socket timeouts
server.headersTimeout = 5000;      // Time limit for parsing HTTP headers (5 seconds)
server.requestTimeout = 10000;     // Time limit for parsing entire request (10 seconds)
server.keepAliveTimeout = 5000;    // Time limit to keep idle socket open (5 seconds)

server.listen(3000, () => console.log('Secure server running on port 3000'));
```

## Best Practices
* **Never Run as Root**: Create and use a non-root user (e.g. `node`) inside your Dockerfiles and deployment environments.
* **Enforce Size Limits**: Set strict body limits (e.g., 10KB for JSON) on all incoming request parser configurations.
* **Integrate Audits in CI/CD**: Run `npm audit --audit-level=high` or Snyk scans inside your pull request checks to prevent deploying vulnerable packages.
* **Inject Secrets Dynamically**: Use environment variables or secret vaults manager to inject credentials at runtime. Never commit keys to git repositories.

## Interview Questions

### Beginner
* **What is the Principle of Least Privilege in security?**
  *Answer*: The Principle of Least Privilege states that a user, process, or program should only have the minimum permissions necessary to perform its task. In Node.js, this means never running the application process as the system root user.

### Intermediate
* **Why should you set payload size limits on your JSON body parsers in an Express API?**
  *Answer*: Exposing endpoints without payload size limits allows attackers to send massive JSON payloads (e.g., 100MB). Parsing these payloads consumes significant CPU and RAM, which can exhaust server resources and crash the application, creating a Denial of Service (DoS).

### Advanced
* **What is a Slowloris attack, and how do you configure socket timeouts in Node.js to defend against it?**
  *Answer*: A Slowloris attack is a type of Denial of Service (DoS) attack where an attacker opens multiple connections to a server and sends request headers very slowly. This keeps the connections open, exhausting the server's maximum file descriptor or socket limit and blocking genuine users. 
  To defend against this, configure socket timeouts on the HTTP server instance: `server.headersTimeout` (timeout for reading headers) and `server.requestTimeout` (timeout for processing the entire request) to close slow, idle connections quickly.

### Senior Architect
* **How would you build a secure CI/CD pipeline that enforces dependency vulnerability checks, prevents credentials from leaking, and handles automatic secret rotations?**
  *Answer*: To build a secure pipeline:
  1. **Enforce Audits**: Add a step in the pipeline that runs `npm audit` or Snyk. If high-severity vulnerabilities are found, fail the build and block the pull request.
  2. **Scan for Secrets**: Integrate scanner tools (like GitGuardian or Trufflehog) into the pre-commit or CI pipeline to detect if any developer has accidentally committed API keys or passwords.
  3. **Inject Secrets at Runtime**: Retrieve configuration settings and credentials dynamically from a secret vault (like HashiCorp Vault or AWS Secrets Manager) using secure environment variables.
  4. **Implement Rotation**: Configure your application to reload database connection credentials dynamically from the vault periodically without restarting the process, supporting zero-downtime secret rotations.

---
Previous : [54_NodeJS_Internals.md] | Index : [00_index.md] | Next : [56_OWASP_Top_Risks.md]
