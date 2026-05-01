# 📌 Topic: Authentication (JWT & OAuth)

## What
### 🧠 Concept Explanation
Authentication is the process of verifying that a user is who they claim to be. In high-performance Node.js systems, we prioritize "Stateless Authentication" using JSON Web Tokens (JWT) to ensure our API can scale to millions of users without being bogged down by session database lookups.

**The Airport Security Analogy (Deep Dive):**
Imagine you are traveling through an international airport (Your Application).
*   **The Check-in Counter (The Login):** You show your physical passport (Username/Password). The airline verifies your identity in their database.
*   **The Boarding Pass (The JWT):** Instead of making you carry your passport to every gate, they give you a Boarding Pass. 
    *   **The Payload:** The pass says you are "John Doe," sitting in "Seat 12A," flying to "London." Anyone can read this; it is not a secret.
    *   **The Signature:** Most importantly, the pass has a complex digital watermark (The Barcode). Only the airline's special printer can create this watermark.
*   **The Security Gate (The Middleware):** When you reach the gate, the guard doesn't call the check-in desk. They just scan the watermark.
    *   **Verification:** If the watermark is valid, they know you are John Doe and you are allowed on the plane.
    *   **Statelessness:** The guard doesn't need a list of every passenger. The "Proof" of your identity is baked into the pass itself.
*   **The Expired Pass:** If you try to use a pass from last year, the guard sees the date and rejects it, even if the watermark is still "Authentic."

---

### 🏗️ Mental Model
Think of Authentication as **Cryptographic Trust**.
1.  **Identity is Expensive:** Checking a database for a password involves disk I/O and expensive hashing (Bcrypt). We only want to do this *once*.
2.  **Tokens are Cheap:** Verifying a digital signature involves pure math. It happens in memory and is thousands of times faster than a database query.
3.  **Trust but Verify:** The server doesn't trust the *user*; it trusts the *signature* that the server itself created in the past.
4.  **Ownership vs. Access:** Authentication says "I am Alice." Authorization (the next step) says "Alice is allowed to delete this file."

---

## Why
### 🏢 Best Practices
1.  **Never put secrets in Payload:** Anyone can decode a JWT; it is not encrypted, only signed.
2.  **Short Expiration:** Set access tokens to 15-60 minutes.
3.  **Use Refresh Tokens:** Store them in a database so you can revoke them if needed.
4.  **Rotate Secrets:** Regularly change your `JWT_SECRET`.

---

### ⚖️ Trade-offs
*   **JWT:** Stateless (scales easily), but hard to revoke and can become large if you put too much data in it.
*   **Sessions:** Full control (easy to logout), but requires a database/Redis lookup for every single request.

---

## How
### ⚡ Actual Behavior
In a Node.js production environment:
1.  **The Handshake:** The user sends credentials over HTTPS. HTTPS is critical; without it, the JWT can be "sniffed" from the air.
2.  **Hashing:** Node.js uses `bcrypt` or `argon2` to check the password. These are deliberately slow (e.g., 100ms per check) to prevent brute-force attacks.
3.  **The Minting:** Once verified, Node.js "Mints" a JWT. It takes the user's ID, encodes it in Base64, and uses a Secret Key (Symmetric) or Private Key (Asymmetric) to create the signature.
4.  **The Delivery:** The JWT is sent back, ideally in an `HttpOnly` and `Secure` cookie. This prevents malicious JavaScript from stealing the token.
5.  **The Validation Loop:** For every future request, the Node.js middleware extracts the token, performs a "Constant Time Comparison" on the signature, and populates `req.user` if valid.

---

### 🔬 Internal Mechanics (V8 + libuv + OS)
*   **OpenSSL Integration:** Token signing (HMAC, RSA, ECDSA) is not done in JavaScript. It is offloaded to the C++ OpenSSL library via Node.js bindings. This ensures the CPU-heavy math doesn't block the Event Loop.
*   **Symmetric (HS256) vs. Asymmetric (RS256):**
    *   **HS256:** Uses one secret key for both signing and verifying. Fast, but if the secret leaks, the whole system is compromised.
    *   **RS256:** Uses a **Private Key** to sign and a **Public Key** to verify. This is the gold standard for microservices—the Auth Service keeps the Private Key secret, while the 100 other Microservices only need the Public Key to verify tokens.
*   **Memory Management:** JWTs are small strings. Node.js handles millions of them in the V8 heap easily. However, decoding thousands of JWTs per second can create "String Thrashing" in the Young Generation of the Garbage Collector.
*   **The Crypto Module and Buffers:** Node.js uses the `crypto` module to perform the SHA-256 hashing. It uses `Buffer` objects to store the raw bytes of the secret and the payload, avoiding the overhead of converting to/from UTF-8 strings during the math phase.
*   **Entropy:** Signing requires a source of "Randomness." On Linux, Node.js pulls entropy from `/dev/urandom`. If the OS runs out of entropy (rare on modern systems), the `crypto` module can block, causing a sudden spike in Event Loop Latency.
*   **Base64URL Encoding:** This is a modified version of Base64 that replaces `+` and `/` characters so the token can safely be used in URLs and HTTP headers without being "escaped." Node.js `Buffer.from(data, 'base64url')` is a highly optimized native function for this.

---

### 🔁 Execution Flow (JWT)
1.  User sends `POST /login` with credentials.
2.  Server verifies credentials against the DB.
3.  Server creates a payload: `{ uid: 123, role: 'admin', exp: 1714545600 }`.
4.  Server signs the payload with a **PRIVATE_KEY** to create the JWT.
5.  Server sends JWT back to the client.
6.  For next request, client sends `Authorization: Bearer <token>`.
7.  Server verifies the signature. If valid, `req.user = payload`.

---

### 🔍 Code Example (Latest Node.js - signing a JWT)
```javascript
import jwt from 'jsonwebtoken';

const SECRET = process.env.JWT_SECRET;

// 1. Create Token
const token = jwt.sign(
    { userId: 123, role: 'admin' }, 
    SECRET, 
    { expiresIn: '1h' }
);

// 2. Verify Token (Middleware)
const authMiddleware = (req, res, next) => {
    const authHeader = req.headers.authorization;
    if (!authHeader) return res.status(401).send('No token');

    const token = authHeader.split(' ')[1];
    try {
        const decoded = jwt.verify(token, SECRET);
        req.user = decoded;
        next();
    } catch (err) {
        res.status(403).send('Invalid or expired token');
    }
};
```

---

## Impact
### 💥 Production Failures
*   **Storing JWTs in LocalStorage:** This makes them vulnerable to XSS. If a malicious script runs on your page, it can steal the token. (Solution: Use `HttpOnly` cookies).
*   **No Revocation Strategy:** If a user is fired, their JWT is still valid until it expires. (Solution: Use a "Blacklist" in Redis or short-lived Access Tokens with long-lived Refresh Tokens).
*   **Secret Leak:** If your `JWT_SECRET` is leaked, anyone can create an "Admin" token for your site.

---

### 🧪 Real-time Scenarios
*   **Microservices:** The API Gateway validates the JWT once and passes the user ID to internal services, avoiding 10 different DB lookups for the same user.
*   **SSO (Single Sign-On):** One token that works across multiple subdomains (e.g., `mail.google.com` and `drive.google.com`).

---

### ⚠️ Edge Cases
*   **Clock Skew:** If the server's clock is 5 minutes behind the client's, the token might look "not yet valid." (Solution: Use `iat` and a small grace period).
*   **Algorithm "none" Attack:** Some old libraries allowed a header with `"alg": "none"`, causing them to skip signature verification entirely. Always use a library that enforces an algorithm.

---

---

Prev: [../Architecture/06_API_Gateway.md](../Architecture/06_API_Gateway.md) | Index: [NodeJS/00_Index.md](../00_Index.md) | Next: [02_Authorization.md](./02_Authorization.md)
