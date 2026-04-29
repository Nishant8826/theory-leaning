# 📌 04 — Cryptography and Hashing: Securing Data at Rest

## 🧠 Concept Explanation

### Basic → Intermediate
- **Hashing**: A one-way transformation of data into a fixed-length string (e.g. Passwords). You cannot get the original data back.
- **Encryption**: A two-way transformation using a key. You can decrypt the data if you have the key (e.g. PIi like SSNs).

### Advanced → Expert
At a staff level, we must understand the **Computational Cost** of cryptography.
1. **Password Hashing**: Use slow, work-factor based algorithms like **Argon2id** (modern winner) or **bcrypt**. These are designed to be slow to prevent "Brute Force" attacks.
2. **Encryption (AES-256-GCM)**: Use Authenticated Encryption. GCM provides not only secrecy but also **Integrity**—if the ciphertext is tampered with, decryption will fail.
3. **Randomness**: Always use `crypto.randomBytes()` or `crypto.randomUUID()`. Never use `Math.random()`, as it is not cryptographically secure.

---

## 🏗️ Common Mental Model
"I'll use SHA-256 for passwords."
**Correction**: SHA-256 is too **fast**. An attacker can calculate billions of SHA-256 hashes per second. You must use algorithms with a "Salt" and a "Cost Factor" (like bcrypt) that force the CPU to work hard for every check.

---

## ⚡ Actual Behavior: The IV (Initialization Vector)
In symmetric encryption (AES), you must never use the same **IV** twice with the same key. If you do, an attacker can perform a "Crib" attack to recover the original data. The IV should be unique and random for every single encryption.

---

## 🔬 Internal Mechanics (OpenSSL + libuv)

### The Crypto Thread Pool
Cryptography is CPU intensive. In Node.js, the `crypto` module methods (like `pbkdf2` or `scrypt`) are executed in the **libuv thread pool** to avoid blocking the event loop.

### Constant Time Comparison
When comparing a hashed password, you must use `crypto.timingSafeEqual()`. A regular `===` comparison returns as soon as it finds a difference, allowing an attacker to guess the hash byte-by-byte by measuring the time it takes for the server to respond (**Timing Attack**).

---

## 📐 ASCII Diagrams

### Password Hashing Flow
```text
  PASSWORD + SALT (Random)
     │
     ▼ [ Argon2id / bcrypt ]
     │ (Iterated 1000s of times)
     ▼
  SECURE HASH (Stored in DB)
```

---

## 🔍 Code Example: Secure Password Hashing
```javascript
const bcrypt = require('bcrypt');

async function hashPassword(password) {
  // Salt is generated and embedded in the final string
  const saltRounds = 12; // High cost factor
  return await bcrypt.hash(password, saltRounds);
}

async function verifyPassword(password, hash) {
  // Safe comparison against timing attacks
  return await bcrypt.compare(password, hash);
}
```

---

## 💥 Production Failures & Debugging

### Scenario: The "Bcrypt" Event Loop Lock
**Problem**: The server response time spikes to 2 seconds for all users whenever one user logs in.
**Reason**: You are using `bcrypt.hashSync()`. This runs on the main thread and blocks the event loop for the duration of the hash calculation.
**Fix**: Use the asynchronous `bcrypt.hash()`, which offloads the work to the libuv thread pool.

### Scenario: The Leaked Encryption Key
**Problem**: Your database is stolen, but the data is encrypted. However, the attacker finds the encryption key in your `config.json`.
**Fix**: Use a **KMS (Key Management Service)** like AWS KMS or HashiCorp Vault. The app never "sees" the master key; it sends data to the KMS for encryption/decryption.

---

## 🧪 Real-time Production Q&A

**Q: "Is it safe to store secrets in environment variables?"**
**A**: **Moderately.** They are better than code, but they can be leaked via `process.env` logs or `/proc` inspection. For highly sensitive secrets (DB passwords), use a secrets manager that injects them into the process at runtime.

---

## 🏢 Industry Best Practices
- **Use Argon2id**: If possible, as it is resistant to GPU-based cracking.
- **Never roll your own crypto**: Always use the built-in `crypto` module or established libraries.

---

## 💼 Interview Questions
**Q: What is a Salt and why is it used?**
**A**: A Salt is a random string added to a password before hashing. It ensures that two users with the same password have different hashes in the database. This prevents **Rainbow Table** attacks (pre-calculated hashes).

---

## 🧩 Practice Problems
1. Implement a function that encrypts and decrypts a string using `aes-256-gcm`. Ensure the IV is stored along with the ciphertext.
2. Build a script that measures the time difference between `===` and `crypto.timingSafeEqual` for a long string.

---

**Prev:** [03_Input_Validation_Sanitization.md](./03_Input_Validation_Sanitization.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [05_Security_Headers_Helmet.md](./05_Security_Headers_Helmet.md)
