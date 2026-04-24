# 📌 Security Basics

## 🧠 Concept Explanation (Story Format)

In 2022, a hacker found a simple SQL injection vulnerability in a company's login page. They extracted 5 million user passwords. The company paid $150 million in fines and settlements.

You've built APIs, React apps, and Node.js backends. But have you thought about:
- What happens if someone sends malicious SQL in your search field?
- Can someone access another user's data by guessing their user ID?
- Are your user passwords stored safely?
- Is your S3 bucket accidentally public?

Security is NOT optional. It's a fundamental requirement. And most security issues are NOT exotic — they're the same basic mistakes repeated over and over.

---

## 🏗️ Top Security Vulnerabilities (OWASP Top 10)

### 1. Injection (SQL, NoSQL, Command)

```javascript
// ❌ DANGEROUS: SQL Injection
app.get('/users', async (req, res) => {
  const name = req.query.name;
  // Attacker sends: name = "' OR '1'='1' --"
  const query = `SELECT * FROM users WHERE name = '${name}'`;
  // Becomes: SELECT * FROM users WHERE name = '' OR '1'='1' --'
  // Returns ALL users! Data breach!
  const users = await db.query(query);
  res.json(users);
});

// ✅ SAFE: Parameterized queries (ALWAYS use this!)
app.get('/users', async (req, res) => {
  const name = req.query.name;
  // Parameters are NEVER interpreted as SQL
  const users = await db.query('SELECT * FROM users WHERE name = $1', [name]);
  res.json(users);
});

// ✅ SAFE: NoSQL Injection prevention
// ❌ MongoDB injection risk
const user = await User.findOne({ email: req.body.email });
// Attacker sends: { "email": { "$gt": "" } } → returns ALL users!

// ✅ Use validation to ensure email is a string
const email = String(req.body.email); // Force string type
const user = await User.findOne({ email: email });

// Even better: Use Joi/Zod validation before touching DB
const schema = Joi.object({ email: Joi.string().email().required() });
const { error, value } = schema.validate(req.body);
if (error) return res.status(400).json({ error: 'Invalid input' });
```

### 2. Broken Authentication

```javascript
// ❌ Storing plain text passwords
await db.query('INSERT INTO users (email, password) VALUES ($1, $2)', 
               [email, password]); // NEVER!

// ✅ Hash passwords with bcrypt
const bcrypt = require('bcrypt');
const SALT_ROUNDS = 12; // Higher = slower to crack (but also slower for legit users)

async function hashPassword(password) {
  return bcrypt.hash(password, SALT_ROUNDS);
}

async function verifyPassword(password, hash) {
  return bcrypt.compare(password, hash);
}

// Registration
const hashedPassword = await hashPassword(req.body.password);
await db.query('INSERT INTO users (email, password_hash) VALUES ($1, $2)', 
               [email, hashedPassword]);

// Login
const user = await db.query('SELECT * FROM users WHERE email = $1', [email]);
const isValid = await verifyPassword(req.body.password, user.rows[0].password_hash);
if (!isValid) return res.status(401).json({ error: 'Invalid credentials' });
```

### 3. Sensitive Data Exposure

```javascript
// ❌ Returning sensitive fields
app.get('/users/:id', async (req, res) => {
  const user = await db.query('SELECT * FROM users WHERE id = $1', [req.params.id]);
  res.json(user.rows[0]); // Returns: password_hash, SSN, credit_card_number!
});

// ✅ Always whitelist fields you return
app.get('/users/:id', async (req, res) => {
  const user = await db.query(
    'SELECT id, name, email, avatar_url, bio, created_at FROM users WHERE id = $1',
    [req.params.id]
    // NEVER select password_hash, reset_token, ssn, etc.
  );
  res.json(user.rows[0]);
});

// ✅ Encrypt sensitive data at rest
const crypto = require('crypto');

function encryptField(plaintext) {
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv('aes-256-gcm', Buffer.from(process.env.ENCRYPTION_KEY, 'hex'), iv);
  const encrypted = Buffer.concat([cipher.update(plaintext, 'utf8'), cipher.final()]);
  const authTag = cipher.getAuthTag();
  return `${iv.toString('hex')}:${authTag.toString('hex')}:${encrypted.toString('hex')}`;
}

function decryptField(ciphertext) {
  const [ivHex, authTagHex, encryptedHex] = ciphertext.split(':');
  const decipher = crypto.createDecipheriv('aes-256-gcm', Buffer.from(process.env.ENCRYPTION_KEY, 'hex'), Buffer.from(ivHex, 'hex'));
  decipher.setAuthTag(Buffer.from(authTagHex, 'hex'));
  return decipher.update(Buffer.from(encryptedHex, 'hex')) + decipher.final('utf8');
}

// Store SSN encrypted
const encryptedSSN = encryptField(req.body.ssn);
await db.query('INSERT INTO users (ssn_encrypted) VALUES ($1)', [encryptedSSN]);
```

### 4. Broken Access Control

```javascript
// ❌ Missing authorization check — anyone can update any post!
app.put('/posts/:id', authenticate, async (req, res) => {
  await db.query('UPDATE posts SET content = $1 WHERE id = $2', 
                 [req.body.content, req.params.id]);
  // Attacker can update ANYONE's post by guessing the post ID!
});

// ✅ Always check ownership!
app.put('/posts/:id', authenticate, async (req, res) => {
  const post = await db.query('SELECT * FROM posts WHERE id = $1', [req.params.id]);
  
  if (!post.rows[0]) return res.status(404).json({ error: 'Post not found' });
  
  // CRITICAL: Verify the logged-in user owns this post!
  if (post.rows[0].user_id !== req.user.id) {
    return res.status(403).json({ error: 'Forbidden: You do not own this post' });
  }
  
  await db.query('UPDATE posts SET content = $1 WHERE id = $2 AND user_id = $3', 
                 [req.body.content, req.params.id, req.user.id]);
  // The WHERE user_id = $3 is a safety net even if the check above fails
  
  res.json({ message: 'Updated' });
});

// ✅ Use UUIDs instead of sequential IDs to prevent enumeration
// Sequential: user_id=1, user_id=2, user_id=3 — easy to guess!
// UUID: user_id="7c9e6679-7425-40de-944b-e07fc1f90ae7" — impossible to guess
```

### 5. Security Misconfiguration

```javascript
// ❌ Common misconfigurations
app.get('/debug', (req, res) => res.json({ env: process.env })); // NEVER expose env vars!
// Stack traces in production error responses
// Default admin passwords not changed
// CORS: allowing all origins
app.use(cors()); // Allows ANY domain! Open CORS.

// ✅ Secure configuration
const cors = require('cors');
app.use(cors({
  origin: ['https://myapp.com', 'https://www.myapp.com'], // Whitelist only your frontend
  methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: true
}));

// Security headers with Helmet.js
const helmet = require('helmet');
app.use(helmet()); // Sets many security headers automatically:
// X-Frame-Options: DENY (prevent clickjacking)
// X-XSS-Protection: 1; mode=block
// X-Content-Type-Options: nosniff
// Content-Security-Policy: ...
// Strict-Transport-Security: max-age=31536000 (HTTPS only)

// Error responses: never expose internal details
app.use((err, req, res, next) => {
  if (process.env.NODE_ENV === 'production') {
    // Generic message to user
    res.status(500).json({ error: 'Internal server error', requestId: req.requestId });
    // Full details only in logs
    logger.error('Unhandled error', { error: err.message, stack: err.stack });
  } else {
    // Development: show full details
    res.status(500).json({ error: err.message, stack: err.stack });
  }
});
```

### 6. XSS (Cross-Site Scripting) Prevention

```javascript
// ❌ Dangerous: Rendering user input as HTML without sanitization
// In React, this is safe because React escapes by default:
function Comment({ content }) {
  return <p>{content}</p>; // Safe — React escapes HTML automatically
}

// ❌ DANGEROUS in React: Never use dangerouslySetInnerHTML with user data!
function Comment({ content }) {
  return <p dangerouslySetInnerHTML={{ __html: content }} />; // XSS risk!
}

// ✅ If you must render HTML (e.g., rich text editor): sanitize first
const DOMPurify = require('dompurify');
const { JSDOM } = require('jsdom');
const window = new JSDOM('').window;
const purify = DOMPurify(window);

function sanitizeHtml(dirty) {
  return purify.sanitize(dirty, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a'],
    ALLOWED_ATTR: ['href']
  });
}

// In Node.js API: Sanitize input before storing
const sanitizedContent = sanitizeHtml(req.body.content);
await db.query('INSERT INTO posts (content) VALUES ($1)', [sanitizedContent]);
```

### 7. AWS Security Best Practices

```javascript
// ❌ Hardcoded AWS credentials
const s3 = new AWS.S3({
  accessKeyId: 'AKIA...',     // NEVER hardcode!
  secretAccessKey: 'abc123...' // NEVER hardcode!
});

// ✅ Use IAM roles (for EC2/Lambda) or environment variables
// On EC2/ECS: IAM role automatically provides credentials
const s3 = new AWS.S3({ region: 'us-east-1' });
// AWS SDK automatically uses instance role credentials!

// ✅ Principle of Least Privilege — only give minimum permissions
// S3 policy for your API: Only allow GetObject from specific bucket
// NOT: s3:* (all S3 actions!) 

// ✅ Environment variables for secrets (not .env files in git!)
// Use AWS Secrets Manager or AWS Parameter Store
const secretsManager = new AWS.SecretsManager();
async function getSecret(secretId) {
  const response = await secretsManager.getSecretValue({ SecretId: secretId }).promise();
  return JSON.parse(response.SecretString);
}

const dbCreds = await getSecret('prod/postgres/credentials');
// Secrets Manager auto-rotates passwords, no hardcoding needed!

// ✅ S3 bucket should NOT be public by default
// In AWS console: Block all public access = TRUE
// Only specific files (public avatars) get public-read ACL explicitly
```

---

## ⚖️ Trade-offs

| Security Measure | Benefit | Cost |
|-----------------|---------|------|
| bcrypt(12) | Brute-force resistant | 200ms to hash password |
| Input validation | Prevent injection | Extra code, request overhead |
| HTTPS everywhere | Encrypted in transit | Certificate management |
| Rate limiting | Prevent brute force | Slightly more complex |
| Encryption at rest | Data breach protection | Small performance overhead |

---

## 📊 Scalability Discussion

### Security Checklist for Production

```
Authentication:
  ✅ Passwords hashed with bcrypt/argon2 (not MD5/SHA1!)
  ✅ JWT tokens expire (don't use infinite tokens)
  ✅ Rate limit login attempts (5/15min per IP + per email)
  ✅ HTTPS only (HTTP → redirect to HTTPS)

Authorization:
  ✅ Every API endpoint requires authentication (unless explicitly public)
  ✅ Check user owns resource before modifying
  ✅ Role-based access control (admin vs user)
  ✅ UUID for IDs (not sequential integers)

Input Validation:
  ✅ Validate and sanitize ALL input (use Joi/Zod)
  ✅ Parameterized queries everywhere (no string interpolation in SQL)
  ✅ File upload validation (type, size, virus scan)
  ✅ JSON size limits (bodyParser limit: '10kb')

Infrastructure:
  ✅ No secrets in code or git (use env vars + Secrets Manager)
  ✅ S3 buckets not public (unless intentionally serving public files)
  ✅ Security groups: only required ports open
  ✅ Database not publicly accessible (only from app servers)
  ✅ Helmet.js for security headers
  ✅ CORS configured for specific origins
```

---

## 💼 Interview Questions (WITH SOLUTIONS)

### Q1: What is SQL injection and how do you prevent it?

**Solution:**
SQL injection is when an attacker inserts malicious SQL code into user input that gets executed as part of a database query.

```javascript
// Attack: User inputs: username = "'; DROP TABLE users; --"
// Bad query becomes: SELECT * FROM users WHERE username = ''; DROP TABLE users; --'
// This deletes your entire users table!

// Prevention: ALWAYS use parameterized queries
// ✅ PostgreSQL (pg library)
await db.query('SELECT * FROM users WHERE username = $1', [username]);

// ✅ MongoDB — validate that input is a string, not an object
const username = String(req.body.username); // Prevents NoSQL injection

// ✅ Mongoose — schema validation prevents type confusion
const User = mongoose.model('User', new mongoose.Schema({ username: String }));
await User.findOne({ username: req.body.username }); // Mongoose coerces to string
```

---

### Q2: How do you store passwords securely?

**Solution:**
Never store plain text or reversible encryption. Use adaptive hashing algorithms.

**Why not MD5/SHA1?**
- These are fast hash functions — can hash billions/second
- Brute force possible: try all common passwords until you find a match
- Rainbow table attacks: pre-computed hash → password lookup tables

**Use bcrypt or Argon2 (intentionally slow):**
```javascript
const bcrypt = require('bcrypt');

// REGISTRATION
async function registerUser(email, password) {
  // Validate password strength first
  if (password.length < 8) throw new Error('Password too short');
  
  // Cost factor 12: ~250ms to hash (too slow for brute force attacks)
  const hash = await bcrypt.hash(password, 12);
  
  await db.query(
    'INSERT INTO users (email, password_hash) VALUES ($1, $2)',
    [email, hash]
  );
}

// LOGIN
async function loginUser(email, password) {
  const user = await db.query('SELECT * FROM users WHERE email = $1', [email]);
  if (!user.rows[0]) return null; // Don't say "user not found" — gives info to attacker!
  
  const isValid = await bcrypt.compare(password, user.rows[0].password_hash);
  if (!isValid) return null; // Don't say "wrong password" — gives info to attacker!
  
  return user.rows[0];
}
```

Additional rules:
- Never log passwords (even "password attempt: xxx")
- Enforce minimum password length (8+)
- Check against common passwords list
- Use HTTPS so password isn't intercepted in transit

---

### Q3: What is CORS and how do you configure it properly?

**Solution:**
CORS (Cross-Origin Resource Sharing) is a browser security mechanism that restricts web pages from making requests to a different domain than the one that served the web page.

Without CORS: A malicious site (evil.com) could make requests to your API (myapp.com) using a logged-in user's cookies → steal data!

```javascript
const cors = require('cors');

// ❌ Allow all origins (dangerous!)
app.use(cors()); // Allows any website to call your API!

// ✅ Whitelist specific origins
const corsOptions = {
  origin: (origin, callback) => {
    const allowedOrigins = [
      'https://myapp.com',
      'https://www.myapp.com',
      process.env.NODE_ENV === 'development' ? 'http://localhost:3000' : null
    ].filter(Boolean);
    
    if (!origin || allowedOrigins.includes(origin)) {
      callback(null, true); // Allow
    } else {
      callback(new Error(`CORS: Origin ${origin} not allowed`));
    }
  },
  methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: true,  // Allow cookies
  maxAge: 86400  // Cache preflight for 24 hours
};

app.use(cors(corsOptions));
```

---

### Q4: What is HTTPS and why is it mandatory?

**Solution:**
HTTPS = HTTP over TLS (Transport Layer Security). All data is encrypted between client and server.

**Without HTTPS:**
- Anyone on the same WiFi can see all your API requests (man-in-the-middle)
- Login credentials, tokens, private data visible in plain text
- Attackers can modify requests/responses
- Browsers show "Not Secure" warning → users leave

**With HTTPS:**
- All data encrypted (JWT tokens, passwords, user data)
- Server authenticated with certificate (prevents impersonation)
- Integrity guaranteed (data can't be modified in transit)

**Implementation:**
```javascript
// On AWS: SSL terminated at ALB (Load Balancer)
// ALB has HTTPS certificate, communicates HTTP internally with Node.js
// Much simpler than managing certs in Node.js

// Force HTTPS redirect in Node.js
app.use((req, res, next) => {
  if (req.headers['x-forwarded-proto'] !== 'https' && process.env.NODE_ENV === 'production') {
    return res.redirect(301, `https://${req.headers.host}${req.url}`);
  }
  next();
});

// HSTS header (tells browsers to ALWAYS use HTTPS for this domain)
app.use(helmet.hsts({
  maxAge: 31536000,  // 1 year
  includeSubDomains: true,
  preload: true
}));
```

---

### Q5: How do you prevent a data breach if your database is compromised?

**Solution:**
Defense in depth — multiple layers so a breach is not catastrophic:

1. **Hashed passwords:** Even if DB is dumped, passwords are hashed (bcrypt) — attacker can't log in as users
2. **Encrypted sensitive fields:** SSN, credit cards encrypted with AES-256 — attacker gets ciphertext only
3. **Principle of least privilege:** App only has SELECT, INSERT, UPDATE on its tables — can't DROP TABLE
4. **No database public access:** Database only accessible from app servers (VPC private subnet)
5. **Audit logs:** Track who accessed what data, when — detect breach early
6. **PII minimization:** Don't store data you don't need
7. **Tokenization:** Replace real card numbers with tokens (use Stripe — they store card numbers, not you!)
8. **Breach notification plan:** Know what to do when it happens (legal requirements to notify users within 72 hours in EU)

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem 1: Design a secure file upload system

**Solution:**
```javascript
const multer = require('multer');
const { promisify } = require('util');

// Validate file uploads
const upload = multer({
  storage: multer.memoryStorage(),
  limits: {
    fileSize: 10 * 1024 * 1024,  // 10MB max
    files: 1  // Only 1 file at a time
  },
  fileFilter: (req, file, cb) => {
    // Whitelist allowed MIME types
    const allowedTypes = ['image/jpeg', 'image/png', 'image/webp', 'application/pdf'];
    if (!allowedTypes.includes(file.mimetype)) {
      return cb(new Error('Invalid file type'), false);
    }
    cb(null, true);
  }
});

const fileTypeLib = require('file-type');

app.post('/upload', authenticate, upload.single('file'), async (req, res) => {
  // 1. Validate file type (don't trust the client!)
  const fileType = await fileTypeLib.fromBuffer(req.file.buffer);
  const allowedMimes = ['image/jpeg', 'image/png', 'image/webp'];
  if (!fileType || !allowedMimes.includes(fileType.mime)) {
    return res.status(400).json({ error: 'Invalid file type' });
  }
  
  // 2. Generate a random, non-guessable filename
  const randomName = `${req.user.id}/${crypto.randomBytes(32).toString('hex')}.${fileType.ext}`;
  
  // 3. Upload to S3 with private ACL (NOT public!)
  await s3.putObject({
    Bucket: process.env.S3_BUCKET,
    Key: randomName,
    Body: req.file.buffer,
    ContentType: fileType.mime,
    ServerSideEncryption: 'AES256', // Encrypt at rest!
    // ACL: 'private' — DON'T make files public unless necessary
  }).promise();
  
  // 4. Store reference in DB (not the file itself)
  await db.query('INSERT INTO files (user_id, s3_key, size, mime_type) VALUES ($1, $2, $3, $4)',
    [req.user.id, randomName, req.file.size, fileType.mime]);
  
  // 5. Return signed URL (expires in 1 hour) — not a permanent public URL!
  const url = s3.getSignedUrl('getObject', {
    Bucket: process.env.S3_BUCKET,
    Key: randomName,
    Expires: 3600
  });
  
  res.json({ url });
});
```

---

### Problem 2: Perform a security audit on an existing Node.js API — what do you look for?

**Solution:**
```
Security Audit Checklist:

Authentication & Session:
□ Are passwords hashed with bcrypt/argon2? NOT MD5/SHA1/plain!
□ Are JWT tokens signed with strong secret (256-bit key)?
□ Do JWT tokens expire? (exp claim)
□ Are refresh tokens stored securely (httpOnly cookies)?
□ Is there rate limiting on login/register?

Authorization:
□ Does every protected route have authentication middleware?
□ For every update/delete: is ownership verified?
□ Are admin routes protected with role check?
□ Are sequential IDs used? (Switch to UUID!)

Input Validation:
□ Are all inputs validated with Joi/Zod?
□ Are SQL queries parameterized? No string concatenation!
□ Is file upload type validated server-side?
□ Is JSON request size limited? (bodyParser limit)

Data Security:
□ Does any API response return passwords/tokens/sensitive fields?
□ Are sensitive fields encrypted at rest? (SSN, credit cards)
□ Are secrets/API keys in environment variables (not git)?

Infrastructure:
□ Is CORS restricted to specific origins?
□ Is Helmet.js used for security headers?
□ Is DB only accessible from app servers? (not public)
□ Are S3 buckets blocked from public access by default?
□ Is HTTPS enforced (HTTP redirects to HTTPS)?
□ Is there error handling that doesn't expose stack traces in production?

Logging:
□ Are passwords ever logged? (Search: logger.*password / console.log.*password)
□ Are sensitive fields logged? (Search: logger.*ssn / credit)

Dependency Security:
□ Run: npm audit → fix HIGH and CRITICAL vulnerabilities
□ Are outdated packages with known CVEs in use?
```

---

### Navigation
**Prev:** [21_Logging_and_Monitoring.md](21_Logging_and_Monitoring.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [23_Authentication_and_Authorization.md](23_Authentication_and_Authorization.md)
