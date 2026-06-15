# Authentication

## What You Will Learn
* The difference between Authentication and Authorization.
* Why storing plain-text passwords is a critical security vulnerability.
* The fundamentals of secure password hashing: Salt, Pepper, and Work Factors.
* Comparing password hashing algorithms (bcrypt vs. Argon2id).
* Implementing secure password hashing and verification.

## Why This Matters
If you store plain-text passwords in your database and your server is compromised, attackers will steal your users' credentials. Because users frequently reuse passwords across multiple sites, a data breach at your company exposes their accounts on other platforms. Implementing secure hashing algorithms protects user credentials even if your database is compromised.

## Theory

### Authentication vs. Authorization
* **Authentication (AuthN)**: Verifying **who** a user is (e.g. validating login credentials, verifying OTP tokens).
* **Authorization (AuthZ)**: Verifying **what** resources a verified user is allowed to access (e.g. checking if a user has admin permissions to delete a resource).

### Secure Password Hashing
You should never store passwords directly in a database. Instead, you store a **cryptographic hash** of the password. A hash function is a one-way mathematical function that converts a password into a fixed-length string of characters that cannot be reversed.

To protect hashes from cracking attempts (like rainbow tables or brute-force attacks):
* **Salt**: A random string of characters generated for each user and appended to the password before hashing. This ensures that two users with the same password will have completely different hashes, rendering pre-computed dictionary tables useless.
* **Pepper**: A secret key stored outside the database (e.g., in environment variables). It is appended to passwords before hashing, defending hashes if the database is stolen but the server environment remains secure.
* **Work Factor (Cost)**: A setting that determines how CPU or memory-intensive the hashing computation is, slowing down brute-force attacks.

## Deep Dive

### Hashing Algorithms: bcrypt vs. Argon2id
* **bcrypt (De Facto Standard)**: A CPU-hard algorithm that has been the industry standard for years. It uses a configurable cost factor to determine computation time.
* **Argon2id (Modern Recommendation)**: The winner of the Password Hashing Competition. It is a **memory-hard** algorithm designed to resist GPU-based and ASIC-based hardware cracking attacks by requiring a configurable amount of memory to run, making it the modern standard for password security.

## Visual Explanation

### Password Hashing and Verification Flow
```text
User Signup:
[ Plain-text Password ] ──> Appends unique Salt ──> [ Argon2id Hash Function ] ──> [ Store Hash in DB ]

User Login:
[ Login Password Input ] ────┐
                             ▼
[ Fetch Salt from DB ] ──> Combine ──> [ Argon2id Hash Function ] ──> [ Computed Hash ]
                                                                             │
                                                                             ├── Matches DB Hash?
                                                                             │     ├── YES ──> Login Successful
                                                                             │     └── NO  ──> return 401 Error
                                                                             ▼
```

## Real-World Example
Consider a user setting their password to `123456`. An attacker with a list of common hashes can instantly match `123456` in a database. When you use Argon2id, the library generates a unique salt (e.g. `x82j!`) for the user, combines it, and computes a long hash. If another user sets the same password, a different salt generates a completely different hash, securing both records.

## Code Examples

### Secure Password Hashing using Argon2

```javascript
// utils/auth.js
// Dependency required: npm install argon2
const argon2 = require('argon2');

// 1. Hash Password during User Registration
async function hashPassword(plainTextPassword) {
  try {
    // Configure Argon2id options
    // Argon2id is selected by default by the argon2 package
    const hash = await argon2.hash(plainTextPassword, {
      type: argon2.argon2id,
      memoryCost: 2 ** 16, // 64 MB of RAM usage
      timeCost: 3,         // 3 processing passes
      parallelism: 1       // Number of threads
    });
    return hash;
  } catch (err) {
    throw new Error('Password hashing failed.');
  }
}

// 2. Verify Password during User Login
async function verifyPassword(storedHash, loginAttemptPassword) {
  try {
    // argon2.verify reads the salt and settings directly from the hash string
    const isMatch = await argon2.verify(storedHash, loginAttemptPassword);
    return isMatch;
  } catch (err) {
    throw new Error('Password verification failed.');
  }
}

module.exports = { hashPassword, verifyPassword };
```

```javascript
// registration-controller.js
const { hashPassword, verifyPassword } = require('./utils/auth');

async function simulateAuthenticationFlow() {
  const userPassword = 'my-super-secret-password-123';
  
  console.log('1. Hashing password during registration...');
  const dbHash = await hashPassword(userPassword);
  console.log('Saved Hash String Format:', dbHash);
  // Format includes: $argon2id$v=19$m=65536,t=3,p=1$salt$hash

  console.log('\n2. Verifying correct login attempt...');
  const successResult = await verifyPassword(dbHash, 'my-super-secret-password-123');
  console.log('Login result (correct password):', successResult); // true

  console.log('\n3. Verifying incorrect login attempt...');
  const failResult = await verifyPassword(dbHash, 'wrong-password');
  console.log('Login result (incorrect password):', failResult); // false
}
simulateAuthenticationFlow();
```

## Best Practices
* **Use Argon2id or bcrypt**: Never use fast hash functions (like MD5, SHA-1, or SHA-256) for password hashing. These are designed for data integrity and are fast, which makes them vulnerable to GPU cracking attacks.
* **Configure Work Factors Safely**: Set Argon2id memory and time cost limits to be slow enough to resist brute-force attempts (~100-300ms execution time) but fast enough to prevent resource bottlenecks on your servers.
* **Return Generic Error Messages**: When a login fails, return a generic error message like `"Invalid email or password"` instead of `"User not found"` or `"Incorrect password"`, preventing attackers from mapping active accounts.

## Interview Questions

### Beginner
* **What is the difference between authentication and authorization?**
  *Answer*: Authentication verifies the identity of a user (who they are). Authorization verifies what resources or actions the authenticated user is allowed to perform (what they can access).

### Intermediate
* **Why should you salt passwords before hashing them?**
  *Answer*: A salt is a random string generated for each user and appended to their password before hashing. Salting ensures that identical passwords yield different hashes, preventing attackers from using pre-computed dictionary tables (rainbow tables) to crack passwords.

### Advanced
* **Why are SHA-256 and MD5 inappropriate for password hashing? What makes bcrypt or Argon2 better?**
  *Answer*: SHA-256 and MD5 are cryptographic checksum algorithms designed to compile binary blocks quickly. Because they are fast, an attacker can compute billions of guesses per second using custom GPU hardware. 
  Bcrypt and Argon2 are slow hashing algorithms. They include configurable computational costs (CPU and memory requirements) that slow down the hashing process (~100-200ms per pass). This delay makes brute-force attacks computationally expensive and slow.

### Senior Architect
* **How would you defend your backend authentication endpoints against high-volume credential stuffing attacks without impacting genuine user latency?**
  *Answer*: To defend against credential stuffing:
  1. Implement **Rate Limiting** at the API gateway boundary, limiting request volume by IP and target account email keys.
  2. Implement a **Captcha** system (like Cloudflare Turnstile or reCAPTCHA) for login attempts that exhibit suspicious request profiles.
  3. Deploy **Web Application Firewalls (WAF)** to identify and block automated bots based on user-agent signatures and request behaviors.
  4. Use connection pools and set limits on database query timeouts to prevent credential stuffing spikes from consuming all available database connections, protecting the rest of the application.

---
Previous : [31_Logging.md] | Index : [00_index.md] | Next : [33_Authorization.md]
