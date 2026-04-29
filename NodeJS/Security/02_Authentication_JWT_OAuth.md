# 📌 02 — Authentication: JWT and OAuth2 Implementation

## 🧠 Concept Explanation

### Basic → Intermediate
Authentication is verifying *who* a user is. JWT (JSON Web Tokens) are a stateless way to transmit identity between a client and a server. OAuth2 is a framework for delegated authorization (e.g. "Login with Google").

### Advanced → Expert
At a staff level, we must distinguish between **Authentication** (Who) and **Authorization** (What).
1. **JWT (Stateless)**: The server signs a payload and gives it to the client. The client sends it back on every request. The server verifies the signature without checking a database.
2. **OAuth2 (Delegated)**: A client obtains an Access Token from an Authorization Server to access resources on behalf of a user. 

The biggest risk with JWTs is **Token Invalidation**. Since they are stateless, you cannot easily "log out" a user until the token expires.

---

## 🏗️ Common Mental Model
"JWTs are encrypted."
**Correction**: JWTs are usually **Signed**, not encrypted. Anyone can decode the payload (it's just Base64). **Never put sensitive data (like passwords or PII) in a standard JWT.**

---

## ⚡ Actual Behavior: Refresh Tokens
To balance security and UX, we use:
- **Access Token**: Short life (15 min), kept in memory.
- **Refresh Token**: Long life (7 days), kept in a `httpOnly` cookie.
When the Access Token expires, the client uses the Refresh Token to get a new one. This allows for **sliding sessions** and the ability to revoke access by deleting the Refresh Token from the database.

---

## 🔬 Internal Mechanics (Crypto + JWT)

### The Signature (HMAC vs RSA)
- **HS256 (Symmetric)**: Uses a shared secret. Both the auth server and the resource server must know the same password.
- **RS256 (Asymmetric)**: Uses a Public/Private key pair. The auth server signs with the private key, and anyone can verify with the public key. This is much more secure for microservices.

---

## 📐 ASCII Diagrams

### OAuth2 Authorization Code Flow
```text
  1. USER ──▶ [ CLIENT APP ] ──▶ [ AUTH SERVER ]
                                      │
  2. AUTH SERVER ──▶ [ LOGIN PAGE ] ◀─┘
                        │
  3. [ AUTH CODE ] ◀────┘ ──▶ [ CLIENT APP ]
                                   │
  4. [ CLIENT APP ] ──[ AUTH CODE + SECRET ]──▶ [ AUTH SERVER ]
                                                      │
  5. [ ACCESS TOKEN ] ◀───────────────────────────────┘
```

---

## 🔍 Code Example: Secure JWT Signing (RS256)
```javascript
const jwt = require('jsonwebtoken');
const fs = require('fs');

const privateKey = fs.readFileSync('./private.pem');
const publicKey = fs.readFileSync('./public.pem');

// 1. Sign (Authorization Server)
const token = jwt.sign({ userId: 123, role: 'admin' }, privateKey, { 
  algorithm: 'RS256',
  expiresIn: '15m' 
});

// 2. Verify (Resource Server)
try {
  const decoded = jwt.verify(token, publicKey, { algorithms: ['RS256'] });
  console.log('Valid User:', decoded.userId);
} catch (err) {
  console.error('Invalid Token');
}
```

---

## 💥 Production Failures & Debugging

### Scenario: The "None" Algorithm Attack
**Problem**: An attacker modifies the JWT header to `{ "alg": "none" }` and removes the signature. Some older libraries will accept this as a valid token.
**Fix**: Always specify the allowed algorithms in your `verify()` call: `{ algorithms: ['RS256'] }`.

### Scenario: LocalStorage XSS Leak
**Problem**: You store the JWT in `localStorage`. An attacker injects a script (XSS) that reads `localStorage` and steals all user tokens.
**Fix**: Store tokens in **Cookies** with the `httpOnly` and `Secure` flags. JS cannot read `httpOnly` cookies.

---

## 🧪 Real-time Production Q&A

**Q: "Should I use Passport.js or build my own?"**
**A**: **Use Passport.js or a specialized library.** Authentication is easy to get wrong. Passport provides battle-tested "Strategies" for hundreds of providers (Google, GitHub, JWT, Local).

---

## 🏢 Industry Best Practices
- **Use RS256**: For asymmetric security across services.
- **Rotate Keys**: Change your signing keys periodically to limit the impact of a key leak.

---

## 💼 Interview Questions
**Q: What is OIDC (OpenID Connect)?**
**A**: OIDC is an identity layer built on top of the OAuth 2.0 protocol. While OAuth 2.0 is about *authorization* (access tokens), OIDC is about *authentication* (ID tokens). It provides a standard way to get a user's profile information (name, email).

---

## 🧩 Practice Problems
1. Implement a "Token Blacklist" in Redis to handle immediate logouts of stateless JWTs.
2. Build a simple OAuth2 flow using the `passport-google-oauth20` strategy.

---

**Prev:** [01_OWASP_Top_10_in_NodeJS.md](./01_OWASP_Top_10_in_NodeJS.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [03_Input_Validation_Sanitization.md](./03_Input_Validation_Sanitization.md)
