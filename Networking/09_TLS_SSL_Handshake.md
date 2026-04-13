# TLS/SSL Handshake

> 📌 **File:** 09_TLS_SSL_Handshake.md | **Level:** Full-Stack Dev → Networking Expert

---

## What is it?

TLS (Transport Layer Security) encrypts the TCP connection between client and server. Every `https://` URL, every MongoDB Atlas connection, every Stripe API call uses TLS. Without TLS, anyone on the network (WiFi, ISP, routers) can read your users' passwords, credit cards, and API tokens in plain text.

**SSL is the old name. TLS is the current standard. When people say "SSL certificate," they mean TLS.**

---

## Map it to MY STACK (CRITICAL)

```
┌──────────────────────────────────────────────────────────────────────┐
│  Where TLS is Used in Your Stack                                    │
├──────────────────────────────────┬───────────────────────────────────┤
│  Browser → CloudFront            │ TLS 1.3 (HTTPS)                  │
│  Browser → ALB                   │ TLS 1.2/1.3 (HTTPS)              │
│  ALB → Node.js (EC2)             │ Optional (usually plain HTTP)    │
│  Node.js → MongoDB Atlas         │ TLS 1.2+ (required by Atlas)    │
│  Node.js → RDS PostgreSQL        │ TLS (ssl: { rejectUnauthorized })│
│  Node.js → ElastiCache Redis     │ TLS (in-transit encryption)      │
│  Node.js → Stripe API            │ TLS 1.2+ (HTTPS)                │
│  Node.js → S3                    │ TLS (HTTPS SDK calls)            │
│  GitHub webhook → your server    │ TLS (HTTPS endpoint)             │
├──────────────────────────────────┴───────────────────────────────────┤
│                                                                      │
│  TLS Termination: WHERE encryption ends                             │
│                                                                      │
│  Option 1: ALB terminates TLS                                       │
│    Browser ──HTTPS──► ALB ──HTTP──► EC2 (Node.js)                  │
│    ALB handles certificates. Node.js sees plain HTTP.               │
│    Pros: Simple, ACM manages certs, offloads CPU                    │
│    Cons: Traffic unencrypted inside VPC                              │
│                                                                      │
│  Option 2: End-to-end TLS                                           │
│    Browser ──HTTPS──► ALB ──HTTPS──► EC2 (Node.js with TLS)       │
│    Both ALB and Node.js have certificates.                          │
│    Pros: Encrypted everywhere. Compliance requirements.             │
│    Cons: More complex, CPU overhead on Node.js                      │
│                                                                      │
│  Most apps use Option 1. Your VPC is a private network.             │
└──────────────────────────────────────────────────────────────────────┘
```

---

## How does it actually work?

### TLS 1.3 Handshake (Current Standard)

```
Client (Browser)                    Server (ALB/Nginx)
  │                                        │
  │  ClientHello                           │
  │  - TLS version: 1.3                    │
  │  - Cipher suites supported             │
  │  - Client random (32 bytes)            │
  │  - Key share (DH public key)           │
  │ ──────────────────────────────────►    │
  │                                        │
  │  ServerHello + Finished               │
  │  - Chosen cipher suite                 │
  │  - Server random (32 bytes)            │
  │  - Key share (DH public key)           │
  │  - Certificate (proves identity)       │
  │  - Certificate Verify (signature)      │
  │  - Finished (handshake MAC)            │
  │ ◄──────────────────────────────────    │
  │                                        │
  │  Finished                              │
  │  - Handshake MAC                       │
  │ ──────────────────────────────────►    │
  │                                        │
  │  ═══ ENCRYPTED DATA FLOW ═══         │
  │                                        │
  TLS 1.3: 1 RTT handshake (vs 2 RTT in TLS 1.2)
  With 0-RTT resumption: 0 RTT on reconnect!
```

### What TLS Protects

```
┌──────────────────────────────────────────────────────────────────┐
│  Protected (encrypted)         │ NOT protected (visible)        │
├────────────────────────────────┼────────────────────────────────┤
│  HTTP headers                  │ IP addresses (src/dst)         │
│  HTTP body (JSON, HTML)        │ TCP ports (src/dst)            │
│  URL path (/api/users)         │ DNS queries (domain name)      │
│  Cookies                       │ Packet sizes (approximate)     │
│  Authorization tokens          │ Timing of requests             │
│  Request/response data         │ TLS certificate (server name)  │
├────────────────────────────────┴────────────────────────────────┤
│  SNI (Server Name Indication): The domain name IS visible       │
│  during TLS handshake. ISPs/firewalls can see WHICH site        │
│  you're visiting, but NOT what you're doing on it.              │
│                                                                  │
│  Solution: ECH (Encrypted Client Hello) — encrypts SNI too.    │
│  Not widely deployed yet.                                        │
└──────────────────────────────────────────────────────────────────┘
```

### Certificate Chain

```
Browser verifies:
  Your certificate (api.myapp.com)
    ├── Signed by: Intermediate CA (Let's Encrypt R3)
    │     └── Signed by: Root CA (ISRG Root X1)
    │           └── Pre-installed in browser's trust store ✅
    │
    └── Is the domain correct?
        └── api.myapp.com matches the certificate's CN/SAN ✅

    └── Is it expired?
        └── Not Before: 2024-01-01, Not After: 2024-03-31 ✅

If ANY check fails → browser shows 🔒❌ "Not Secure" warning
```

---

## AWS Certificate Manager (ACM)

```
ACM provides FREE TLS certificates for AWS services:

┌──────────────────────────────────────────────────────────────┐
│  Service       │ ACM Support │ How                           │
├────────────────┼─────────────┼───────────────────────────────┤
│  ALB           │ ✅          │ Attach cert to HTTPS listener │
│  CloudFront    │ ✅          │ Custom SSL certificate        │
│  API Gateway   │ ✅          │ Custom domain setup           │
│  EC2 directly  │ ❌          │ Use Let's Encrypt + Nginx    │
│  Elastic BStalk│ ✅          │ Through ALB                   │
├────────────────┴─────────────┴───────────────────────────────┤
│  ACM certs auto-renew. Let's Encrypt certs renew every 90d. │
│  ACM is simpler. Use Let's Encrypt only for EC2 direct.     │
└──────────────────────────────────────────────────────────────┘
```

### Let's Encrypt on EC2 (Nginx)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d api.myapp.com

# Auto-renewal (certbot adds a cron/systemd timer automatically)
sudo certbot renew --dry-run

# Certificate location
ls /etc/letsencrypt/live/api.myapp.com/
# fullchain.pem — certificate + intermediate
# privkey.pem — private key
# cert.pem — just your certificate
# chain.pem — intermediate CA
```

---

## Node.js Implementation

```javascript
// ──── HTTPS server with Node.js (for EC2 without ALB) ────
const https = require('https');
const fs = require('fs');
const express = require('express');

const app = express();

const server = https.createServer({
  key: fs.readFileSync('/etc/letsencrypt/live/api.myapp.com/privkey.pem'),
  cert: fs.readFileSync('/etc/letsencrypt/live/api.myapp.com/fullchain.pem'),
  
  // Security options
  minVersion: 'TLSv1.2',          // Reject TLS 1.0/1.1
  ciphers: [                       // Strong ciphers only
    'TLS_AES_256_GCM_SHA384',
    'TLS_CHACHA20_POLY1305_SHA256',
    'TLS_AES_128_GCM_SHA256'
  ].join(':')
}, app);

server.listen(443);

// ──── HTTP → HTTPS redirect ────
const http = require('http');
http.createServer((req, res) => {
  res.writeHead(301, { Location: `https://${req.headers.host}${req.url}` });
  res.end();
}).listen(80);

// ──── HTTPS client with certificate verification ────
const https2 = require('https');

// Connecting to MongoDB Atlas (TLS required)
const mongoose = require('mongoose');
mongoose.connect('mongodb+srv://user:pass@cluster0.xxxxx.mongodb.net/mydb', {
  tls: true,
  tlsCAFile: '/path/to/ca-certificate.crt',  // Custom CA (if needed)
  // Atlas uses well-known CAs — usually not needed
});

// Connecting to PostgreSQL with TLS
const { Pool } = require('pg');
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: {
    rejectUnauthorized: true,   // ✅ Verify server certificate
    // ca: fs.readFileSync('/path/to/rds-combined-ca-bundle.pem')
  }
});

// ──── Inspect TLS connection details ────
const tls = require('tls');

function inspectTLS(hostname, port = 443) {
  const socket = tls.connect({ host: hostname, port, servername: hostname }, () => {
    const cert = socket.getPeerCertificate();
    console.log(`\nTLS Connection to ${hostname}:`);
    console.log(`  Protocol: ${socket.getProtocol()}`);
    console.log(`  Cipher: ${socket.getCipher().name}`);
    console.log(`  Subject: ${cert.subject.CN}`);
    console.log(`  Issuer: ${cert.issuer.O}`);
    console.log(`  Valid from: ${cert.valid_from}`);
    console.log(`  Valid to: ${cert.valid_to}`);
    console.log(`  Fingerprint: ${cert.fingerprint}`);
    console.log(`  SAN: ${cert.subjectaltname}`);
    socket.end();
  });
  
  socket.on('error', (err) => console.error(`TLS error: ${err.message}`));
}

inspectTLS('google.com');
inspectTLS('api.github.com');
```

---

## Commands & Debugging Tools

```bash
# Test TLS connection
openssl s_client -connect api.myapp.com:443 -servername api.myapp.com
# Shows: certificate chain, cipher, protocol version

# Check certificate details
openssl s_client -connect api.myapp.com:443 </dev/null 2>/dev/null | \
  openssl x509 -text -noout
# Shows: subject, issuer, validity dates, SAN

# Check certificate expiry
echo | openssl s_client -connect api.myapp.com:443 2>/dev/null | \
  openssl x509 -noout -dates
# notBefore=Jan  1 00:00:00 2024 GMT
# notAfter=Mar 31 23:59:59 2024 GMT

# Test TLS version
curl --tls13 -I https://api.myapp.com        # Force TLS 1.3
curl --tlsv1.2 -I https://api.myapp.com      # Force TLS 1.2

# curl verbose TLS info
curl -v https://api.myapp.com 2>&1 | grep -E "SSL|TLS|cipher|certificate"

# Check if Let's Encrypt cert will auto-renew
sudo certbot renew --dry-run

# SSL Labs test (most thorough)
# https://www.ssllabs.com/ssltest/analyze.html?d=api.myapp.com
```

---

## Performance Insight

```
┌──────────────────────────────────────────────────────────────────┐
│  TLS Performance Impact                                          │
├──────────────────┬───────────────────────────────────────────────┤
│  TLS 1.2 new     │ 2 RTT (TCP + TLS handshake)                  │
│  TLS 1.3 new     │ 1 RTT (combined key exchange)                │
│  TLS 1.3 0-RTT   │ 0 RTT (session resumption — instant!)       │
│  TLS CPU overhead │ ~5-10% on modern hardware (AES-NI)          │
├──────────────────┴───────────────────────────────────────────────┤
│                                                                  │
│  Optimization:                                                   │
│  1. Use TLS 1.3 (1 RTT vs 2 RTT) — major latency saving       │
│  2. TLS session resumption (0 RTT on reconnect)                 │
│  3. OCSP stapling (avoid extra round trip for cert validation)  │
│  4. Terminate TLS at ALB/CloudFront (offload CPU from Node.js) │
│  5. Use HTTP/2 (one TLS handshake, many requests)              │
│  6. Use small certificates (EC keys: 256-bit vs RSA: 2048-bit) │
│                                                                  │
│  Real impact (cross-continent, 200ms RTT):                      │
│  TLS 1.2: +400ms for new connection                              │
│  TLS 1.3: +200ms for new connection                              │
│  TLS 1.3 0-RTT: +0ms for returning visitor                     │
│  Keep-alive: +0ms (connection already established)               │
└──────────────────────────────────────────────────────────────────┘
```

---

## Common Mistakes

### ❌ Disabling Certificate Verification

```javascript
// ❌ NEVER do this in production
process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';
// Disables ALL certificate checking
// Vulnerable to man-in-the-middle attacks

// ❌ Also bad
const pool = new Pool({
  ssl: { rejectUnauthorized: false }  // Accepts any certificate
});

// ✅ Proper way — specify the CA
const pool = new Pool({
  ssl: {
    rejectUnauthorized: true,
    ca: fs.readFileSync('./rds-combined-ca-bundle.pem')
  }
});
```

### ❌ Not Redirecting HTTP to HTTPS

```javascript
// ❌ HTTP and HTTPS both serving content
// Users on HTTP → passwords sent in plain text!

// ✅ Redirect all HTTP to HTTPS
app.use((req, res, next) => {
  if (req.headers['x-forwarded-proto'] !== 'https') {
    return res.redirect(301, `https://${req.hostname}${req.url}`);
  }
  next();
});

// ✅ Set HSTS header (tell browser to ALWAYS use HTTPS)
app.use((req, res, next) => {
  res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');
  next();
});
```

### ❌ Expired Certificates

```
Certificate expired → EVERY user sees "Not Secure" warning
→ Users leave → Revenue drops → SEO penalty

Prevention:
  - ACM: Auto-renews (problem solved)
  - Let's Encrypt: certbot auto-renew via cron
  - Monitor: Set up certificate expiry alerts
    curl -v https://api.myapp.com 2>&1 | grep "expire"
```

---

## Practice Exercises

### Exercise 1: Inspect TLS
Use `openssl s_client` to connect to `google.com:443`. Identify: TLS version, cipher suite, certificate issuer, and expiry date.

### Exercise 2: Certificate Comparison
Compare the TLS setup of `github.com`, `google.com`, and `amazon.com`. Which uses TLS 1.3? What cipher suites?

### Exercise 3: HTTPS Node.js Server
Create a self-signed certificate and set up an HTTPS Express server. Test with `curl -k` (skip verification) and without.

---

## Interview Q&A

**Q1: How does the TLS handshake work?**
> Client sends ClientHello (supported ciphers, random). Server chooses cipher, sends certificate and key share. Client verifies certificate chain, computes shared secret. Both derive session keys. TLS 1.3 does this in 1 RTT (vs 2 RTT in TLS 1.2).

**Q2: What is the difference between TLS 1.2 and TLS 1.3?**
> TLS 1.3: 1 RTT handshake (vs 2), 0-RTT resumption, removed insecure ciphers (RSA key exchange, CBC mode, SHA-1), forward secrecy mandatory, simplified cipher suites. Result: faster and more secure.

**Q3: What is TLS termination and where should it happen?**
> TLS termination = where encryption ends and plain HTTP begins. At ALB: offloads CPU, ACM manages certs, simple. At Node.js: encrypted end-to-end within VPC, compliance requirements. Most apps terminate at ALB — VPC is already a trusted network.

**Q4: What is certificate pinning and when should you use it?**
> Pinning hard-codes the expected certificate or public key in your app, preventing even trusted CAs from impersonating your server. Used in mobile apps for banking/security. Not for web apps (certificates rotate). React Native: can implement via SSL pinning libraries.

**Q5: What happens if your TLS certificate expires?**
> All HTTPS connections fail. Browsers show security warnings. Users can't reach your site. API clients get certificate errors. SEO ranking drops. Prevention: ACM auto-renewal, Let's Encrypt certbot timer, monitoring with certificate expiry alerts.
