# TLS/SSL Handshake

> 📌 **File:** 09_TLS_SSL_Handshake.md | **Level:** Full-Stack Dev → Networking Expert

---

## What is it?

TLS (Transport Layer Security) encrypts the TCP connection between client and server. Every `https://` URL, every MongoDB Atlas connection, every Stripe API call uses TLS. Without TLS, anyone on the network (WiFi, ISP, routers) can read your users' passwords, credit cards, and API tokens in plain text.

**SSL is the old name. TLS is the current standard. When people say "SSL certificate," they mean TLS.**

### Why Does This Matter — The Real Threat

Imagine you're at a coffee shop, connected to the public WiFi. Without TLS, every HTTP request you make is sent as plain text over the air. Anyone else on the same network running a packet sniffer (like Wireshark — a free, legal tool) can read every byte you send. Your login form submits `username=john&password=mySecret123` and it literally travels across the room readable by anyone.

TLS solves this by encrypting the payload before it ever leaves your device. Even if someone captures every single packet, all they see is random-looking encrypted bytes — completely useless without the session key that only your browser and the server computed together.

There are three distinct problems TLS solves simultaneously:
- **Confidentiality** — No one in the middle can read what you send or receive.
- **Integrity** — No one in the middle can silently modify the data (e.g., change a bank transfer amount). Any tampering is detected and the connection is dropped.
- **Authentication** — You are actually talking to the real `api.myapp.com`, not an impostor server. This is what the certificate is for.

All three must hold simultaneously. Encryption without authentication is still dangerous — you might be securely encrypting all your data directly to an attacker.

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

### Why "ALB terminates TLS" Is Usually Fine

The VPC (Virtual Private Cloud) is a private, isolated network segment inside AWS. Traffic between your ALB and your EC2 instance never travels over the public internet — it goes over AWS's internal backbone network, which is physically separate from other customers' traffic and inaccessible from outside. This is fundamentally different from a public coffee shop WiFi.

That said, "encrypted inside VPC" is a real compliance requirement for industries like healthcare (HIPAA), finance (PCI-DSS), and government. In those cases, Option 2 is mandatory regardless of complexity.

---

## How does it actually work?

### Before TLS: The Public-Key Cryptography Problem

To understand TLS, you need to understand one fundamental problem: **how do two strangers securely share a secret over an insecure channel?**

If Alice wants to send Bob an encrypted message, she needs a key. But how does she securely tell Bob what key to use? She can't send it in the open — an attacker (Eve) could intercept the key and then decrypt everything.

The solution is **asymmetric (public-key) cryptography**. Every participant has two mathematically linked keys:
- **Public key** — can be shared with anyone. Used to *encrypt* data or *verify* a signature.
- **Private key** — kept secret forever. Used to *decrypt* data or *create* a signature.

Data encrypted with the public key can *only* be decrypted with the private key. So Alice can grab Bob's public key (even if Eve sees it), encrypt a message, and only Bob can decrypt it. Eve watching the channel sees only encrypted gibberish.

TLS uses this idea, but cleverly — because asymmetric encryption is **computationally expensive**. So TLS only uses asymmetric crypto for the handshake (to securely agree on a shared secret), then switches to **symmetric encryption** (same key on both sides) for the actual data transfer, which is ~1000x faster.

---

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

### Step-by-Step Breakdown (What Each Field Actually Does)

#### Step 1 — ClientHello (Browser speaks first)

The browser fires the opening message. It contains:

- **TLS version** — "I support TLS 1.3." The server will pick the best version both sides understand.
- **Cipher suites** — A list of algorithm combinations the browser knows. Each suite is a combination like `TLS_AES_256_GCM_SHA384`. The name encodes three things: the symmetric cipher (`AES_256_GCM`), and the hash function for integrity (`SHA384`). In TLS 1.3, all remaining cipher suites are strong — the weak ones were eliminated entirely.
- **Client random** — 32 bytes of random data. This is mixed into the final key derivation. Its purpose: even if the same session keys were somehow reused, a different random makes each session's keys unique. Prevents replay attacks.
- **Key share (DH public key)** — The browser's half of the Diffie-Hellman exchange (explained below). In TLS 1.3, the browser guesses which key agreement algorithm the server will choose and pre-sends a key share for it. This is how TLS 1.3 achieves 1 RTT — it doesn't wait for the server to announce its choice first.

#### Step 2 — ServerHello + Finished (Server responds with everything at once)

This is the big message. In TLS 1.3, the server sends everything it needs to in one shot:

- **Chosen cipher suite** — The server picks one from the client's list (the best one it also supports).
- **Server random** — Another 32 bytes of random data from the server side.
- **Key share (DH public key)** — The server's half of the Diffie-Hellman exchange.
- **Certificate** — The server's identity proof. Contains the server's public key and is signed by a Certificate Authority. The browser doesn't "trust" the server directly — it trusts the chain leading back to a Root CA pre-installed in the browser.
- **Certificate Verify** — A digital signature over the entire handshake transcript so far, created with the server's private key. This proves the server actually *owns* the private key that matches the certificate's public key. Without this step, an attacker could steal someone else's certificate and present it — the Certificate Verify makes that impossible because they don't have the matching private key.
- **Finished** — An HMAC (keyed hash) over the entire handshake, computed with the derived session key. Proves that the handshake messages weren't tampered with in transit.

> **Key insight:** Notice that by the time the server sends its key share, both sides have *all the pieces needed to independently compute the same session key*. Neither side ever transmits the actual session key — they each compute it locally from the same inputs.

#### Step 3 — Client Finished

The browser:
1. Verifies the certificate chain (detailed below).
2. Verifies the Certificate Verify signature using the server's public key from the certificate.
3. Computes the same session key the server computed (Diffie-Hellman magic).
4. Sends its own `Finished` HMAC to confirm to the server that it received and verified everything.

After this, both sides have the session key and all communication is encrypted.

---

### Diffie-Hellman Key Exchange — The Core Magic

This is the mathematical trick that makes TLS possible. Two parties can agree on a shared secret *in public* without ever transmitting the secret.

The simplified analogy (using colors instead of math):

```
Public information: Base color = Yellow (everyone knows this)

Alice picks a secret: Red
Alice mixes: Yellow + Red = Orange → sends Orange to Bob
                                       (Red stays secret, Orange is sent publicly)

Bob picks a secret: Blue
Bob mixes: Yellow + Blue = Green → sends Green to Alice
                                    (Blue stays secret, Green is sent publicly)

Alice: Green + Red = Brown
Bob:   Orange + Blue = Brown

Both get the same Brown! (The shared secret)
Eve watched everything but only has: Yellow, Orange, Green.
She cannot compute Brown without either Red or Blue.
```

In practice, TLS uses **Elliptic Curve Diffie-Hellman (ECDH)** where "mixing colors" is replaced by elliptic curve point multiplication — a mathematical operation that's easy to do forward but computationally infeasible to reverse (the "discrete log problem").

The session key is derived from:
- Client DH key share + Server DH key share → Pre-master secret
- Pre-master secret + Client random + Server random → Master secret
- Master secret → Derived into multiple keys (one for client→server encryption, one for server→client encryption, one for each MAC)

**Why are there multiple derived keys?** Using different keys in each direction means if an attacker somehow breaks one direction of encryption, the other direction remains secure. Defense in depth.

---

### What About Forward Secrecy?

**Forward secrecy** (also called Perfect Forward Secrecy, PFS) means: even if the server's private key is compromised in the future, past recorded sessions cannot be decrypted.

In older TLS (pre-1.3 with RSA key exchange), the client encrypted the pre-master secret with the server's public key. If an attacker recorded all traffic and later stole the server's private key, they could decrypt all historical sessions.

TLS 1.3 **mandates** Diffie-Hellman for key exchange. The DH keys are **ephemeral** — generated fresh for every connection and discarded afterward. The server's certificate private key is only used for the Certificate Verify signature, not for key derivation. So even if the private key leaks years later, the attacker cannot derive the session keys for past sessions — those ephemeral DH keys are gone forever.

Forward secrecy is one of the reasons TLS 1.3 removed RSA key exchange entirely.

---

#### Diagram Explanation (The Secret Handshake — Spy Analogy)
Think of the TLS handshake like two spies meeting in public to exchange a secret code:
- **ClientHello (The Greeting):** The browser says "Hi! I speak these 3 secret languages (cipher suites). Here is a random string of text and my half of a color puzzle (key share)."
- **ServerHello (The Verification):** The server replies "Great, let's speak language #2. Here is my random string, my half of the color puzzle, and... my ID card (certificate) proving I am officially who I say I am."
- **Finished:** Because both spies now have both halves of the color puzzle and the random strings, they independently mix them together to mathematically compute the exact same secret color (the symmetric encryption key). From that moment on, all data is locked in a box painted with that exact color!

---

### TLS 1.2 vs TLS 1.3 — The Detailed Differences

```
┌────────────────────────────────────────────────────────────────────┐
│              TLS 1.2                    TLS 1.3                   │
├─────────────────────────────────────────────────────────────────── │
│  Handshake RTT:    2 RTT                1 RTT                     │
│  Resumption RTT:   1 RTT                0 RTT                     │
│  Key Exchange:     RSA or DH            ECDH only (mandatory PFS) │
│  Cipher suites:    ~37 (many weak)      5 (all strong)            │
│  RSA key exchange: ✅ allowed           ❌ removed                 │
│  CBC mode:         ✅ allowed           ❌ removed                 │
│  SHA-1:            ✅ allowed           ❌ removed                 │
│  Handshake encrypt:❌ certificate sent  ✅ certificate encrypted   │
│                    in plain text        (after ServerHello)        │
│  Forward secrecy:  Optional             Mandatory                  │
└────────────────────────────────────────────────────────────────────┘
```

**Why 2 RTT in TLS 1.2?**

In TLS 1.2:
- RTT 1: ClientHello → ServerHello (server announces chosen cipher). **At this point the browser doesn't know the cipher yet, so it couldn't pre-send a key share.**
- RTT 2: Client sends key exchange → Server sends Finished.

TLS 1.3 pre-sends the key share in the *first* message (making a good guess about what cipher the server will pick). If the server picks a different algorithm (a "HelloRetryRequest"), it falls back to 2 RTT — but this is rare since browsers guess correctly almost always.

**Why is TLS 1.3's certificate encrypted but TLS 1.2's isn't?**

In TLS 1.2, by the time the server sends its certificate, the encryption keys haven't been established yet — they're derived later. So the certificate travels in plaintext. In TLS 1.3, session keys are derived immediately after the ServerHello key share exchange (before the certificate is sent), so everything from the Certificate message onward is encrypted.

This means in TLS 1.3, an eavesdropper cannot see which certificate the server presented — a modest privacy improvement.

---

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

### Why IP Addresses Can't Be Encrypted

TLS operates at Layer 5-6 (Session/Presentation) of the OSI model. IP operates at Layer 3. The IP header containing source and destination IP addresses must be *readable by every router along the path* — that's literally how packets get from your computer to the server. Routers don't understand TLS. They only know Layer 3. Encrypting IP headers would make routing impossible.

This is also why VPNs work differently — they encapsulate the entire packet (including IP header) inside another encrypted packet. The outer IP header is for the VPN server, the inner (encrypted) IP header is your real destination.

### SNI — The Privacy Gap in Plain Sight

**Server Name Indication (SNI)** is an extension added in ClientHello. It tells the server *which hostname* the client is trying to reach. This exists because many servers (especially cloud providers) host thousands of domains on the same IP address — the server needs to know which certificate to present *before* the TLS session is established.

The problem: SNI is sent before encryption begins. Your ISP, your employer's firewall, any network observer sees the exact hostname in every HTTPS request you make — `api.myapp.com`, `mail.google.com`, etc.

**ECH (Encrypted Client Hello)** solves this by encrypting the real SNI using a public key the server publishes in its DNS record. A fake "outer" ClientHello with a generic SNI is used for routing, while the real hostname is inside the encrypted inner ClientHello. This is in deployment but not yet widespread as of 2024.

---

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

### What's Actually Inside a Certificate

A TLS certificate is a structured file in X.509 format. It contains:

```
Certificate:
  Version: 3
  Serial Number: 03:45:a1:... (unique ID issued by the CA)
  Signature Algorithm: sha256WithRSAEncryption
  Issuer: C=US, O=Let's Encrypt, CN=R3
  Validity:
    Not Before: Jan  1 00:00:00 2024 GMT
    Not After : Mar 31 23:59:59 2024 GMT
  Subject: CN=api.myapp.com
  Subject Public Key Info:
    Public Key Algorithm: id-ecPublicKey
    Public-Key: (256 bit)  ← This is the server's public key
  X509v3 extensions:
    Subject Alternative Name:
      DNS:api.myapp.com, DNS:www.myapp.com  ← All valid domains
    Key Usage: Digital Signature, Key Encipherment
    Extended Key Usage: TLS Web Server Authentication
    Authority Key Identifier: ... (links to the issuing CA)
    CRL Distribution Points: http://crl.example.com/r3.crl
    Authority Information Access:
      OCSP: http://ocsp.example.com
      CA Issuers: http://cert.example.com/r3.crt
  Signature: (signed by Let's Encrypt R3's private key)
```

**The critical field is the Signature.** Let's Encrypt R3 took a hash of all the certificate fields above and signed it with their own private key. Your browser can verify this signature using Let's Encrypt R3's public key (which it knows because it's in the trust store or obtained from the intermediate cert). If the signature verifies, the browser knows: "Let's Encrypt R3 vouch for this certificate."

**SAN (Subject Alternative Name)** is how one certificate can cover multiple domains. `www.myapp.com` and `api.myapp.com` can both be in one cert. The old `CN` (Common Name) field is deprecated for domain matching — modern browsers only check SAN.

**Wildcard certificates** use `*.myapp.com` in the SAN. This covers `api.myapp.com`, `www.myapp.com`, `mail.myapp.com` — but NOT `sub.api.myapp.com` (wildcards only cover one level deep) and NOT `myapp.com` itself.

---

### How Certificate Revocation Works (OCSP and CRL)

What if a certificate's private key is stolen? The certificate is still valid until its expiry date. Revocation exists to handle this:

**CRL (Certificate Revocation List):** The CA publishes a list of revoked certificate serial numbers. Browsers can download this list. Problem: CRLs are large and cached — there's a delay between revocation and browsers knowing about it.

**OCSP (Online Certificate Status Protocol):** The browser asks the CA's OCSP server in real-time: "Is serial number 03:45:a1 still valid?" Gets a signed yes/no response. Problem: Extra round trip + privacy issue (the CA now knows every site you're visiting).

**OCSP Stapling:** The *server* periodically fetches its own OCSP response from the CA and "staples" it to the TLS handshake. Browser gets the signed freshness proof without needing to contact the CA directly. No extra RTT, no privacy leak. This is the recommended approach.

**Chrome's CRLSets:** Chrome doesn't actually do OCSP for regular sites — it maintains its own compressed revocation list (CRLSets) pushed via automatic updates. Full OCSP is only done for Extended Validation (EV) certificates.

---

#### Diagram Explanation (The Chain of Trust — Passport Analogy)
Why does your computer blindly trust a random server you've never visited? Because of the Chain of Trust, which works exactly like getting a passport:
- **Your Certificate:** Your server shows its "ID Card" (Certificate). It says "I am api.myapp.com." But anyone can print a fake ID card...
- **The Intermediate CA:** What makes the ID Card valid is the notary stamp from the post office (Intermediate CA) that proves "We officially verified this person."
- **The Root CA:** But why do we trust the post office? Because the Federal Government (Root CA) explicitly authorized the post office! Your browser literally comes pre-installed with a list of "Federal Governments" (`ISRG Root X1`, `DigiCert`, etc.) it universally trusts. If the chain breaks or expires at any point, the browser violently rejects the connection.

### Why Intermediate CAs Exist

Root CAs are extraordinarily valuable and their private keys are kept in **Hardware Security Modules (HSMs)** in physically secured bunkers, never connected to the internet. Signing millions of certificates daily with the root key would require it to be online — an unacceptable risk.

Instead, Root CAs sign a small number of Intermediate CA certificates. The Intermediate CA's private key is used for day-to-day signing. If an Intermediate CA is compromised, the Root CA can revoke just that intermediate, and only the certificates that intermediate issued are affected. The Root CA itself remains untouched.

This is why your server's TLS certificate is never signed directly by a Root CA — there's always at least one intermediate in between.

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

### How ACM Validates Domain Ownership

Before ACM issues a certificate, it must verify you actually own/control the domain. There are two validation methods:

**DNS Validation (Recommended):**
ACM gives you a specific CNAME record to add to your domain's DNS. For example:
```
_acme-challenge.api.myapp.com  CNAME  _abc123.acm-validations.aws.
```
ACM periodically checks that this record exists. Because only the domain owner can add DNS records, this proves ownership. Once validated, ACM can auto-renew silently (it keeps checking the CNAME is still there). **This is the recommended method** — set it up once, forget about renewals forever.

**Email Validation:**
ACM sends a verification email to admin@yourdomain.com and similar addresses. Simpler to set up but requires manual action on renewal. Not suitable for automated pipelines.

### Why ACM Certificates Can't Be Used on EC2 Directly

ACM certificates are stored and managed entirely within AWS's infrastructure. AWS never lets the private key leave their systems. This is intentional — it means a compromised EC2 instance cannot exfiltrate the private key. The downside: you can only attach ACM certs to AWS managed services (ALB, CloudFront, API Gateway) that know how to use ACM's internal key access mechanism. EC2 instances running Nginx or Node.js directly need the private key on disk — which ACM won't give you. Hence: Let's Encrypt for EC2.

---

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

### What Certbot Actually Does (Behind the Scenes)

When you run `certbot --nginx -d api.myapp.com`, here's what happens:

1. **ACME Challenge:** Certbot contacts Let's Encrypt's servers and requests a certificate for `api.myapp.com`. Let's Encrypt responds: "Prove you control this domain. Place this token at `/.well-known/acme-challenge/<random-token>`."
2. **Local Server:** Certbot temporarily starts a local web server (or configures Nginx) to serve that token at the specified URL.
3. **Verification:** Let's Encrypt's servers make an HTTP request to `http://api.myapp.com/.well-known/acme-challenge/<random-token>`. If they get the correct token back, you own the domain.
4. **Certificate Issued:** Let's Encrypt signs and returns a certificate. Certbot saves it to `/etc/letsencrypt/live/`.
5. **Nginx Config:** Certbot modifies your Nginx config to enable HTTPS, pointing to the new certificate files.

The ACME protocol (RFC 8555) automates everything. Certbot sets up a systemd timer to re-run `certbot renew` twice daily. If the cert is within 30 days of expiry, it renews automatically. Let's Encrypt certs last 90 days (intentionally short to encourage automation).

**DNS challenge instead of HTTP challenge:**
```bash
# Use DNS challenge (needed if port 80 is blocked, or for wildcard certs)
sudo certbot certonly --manual --preferred-challenges dns -d "*.myapp.com"
# You must manually add a TXT DNS record: _acme-challenge.myapp.com = <token>
```

Wildcard certs (`*.myapp.com`) require DNS challenge because Let's Encrypt can't HTTP-verify a wildcard — it doesn't know which specific subdomains to check.

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

### Understanding the Node.js TLS Options in Detail

**`minVersion: 'TLSv1.2'`**

This rejects any client trying to connect with TLS 1.0 or 1.1. These older versions have known vulnerabilities (POODLE, BEAST, CRIME) and modern browsers no longer support them anyway. Forcing TLS 1.2+ is a security best practice and also a PCI-DSS requirement for payment processing.

**`ciphers`**

A cipher suite specifies the exact algorithms used. Each name encodes several components:
- `TLS_AES_256_GCM_SHA384` → Symmetric cipher: AES-256-GCM, MAC: SHA-384
- `TLS_CHACHA20_POLY1305_SHA256` → Symmetric cipher: ChaCha20-Poly1305, MAC: SHA-256

**AES-GCM** is fast on hardware that supports AES-NI instructions (all modern Intel/AMD CPUs). **ChaCha20-Poly1305** is faster on devices without AES hardware acceleration (older mobile CPUs, IoT devices). Supporting both lets the server pick the fastest option for each client.

All three listed ciphers use **AEAD (Authenticated Encryption with Associated Data)** — they encrypt and authenticate in one pass, preventing padding oracle attacks that plagued older CBC-mode ciphers.

**`fullchain.pem` vs `cert.pem`**

Always use `fullchain.pem` for the `cert` option in Node.js (and Nginx). This file contains your certificate *plus* the intermediate CA certificate(s). Without the intermediate, some clients (particularly mobile apps and older systems) may fail certificate chain verification because they don't have the intermediate cached. The browser may have cached Let's Encrypt R3 from a previous connection, but you shouldn't rely on that.

**`rejectUnauthorized: true`** (when making outbound TLS connections)

This is Node.js's way of saying "verify the server's certificate, reject if invalid." It's the default (true) for `https.request()`, but explicitly setting it for database connections makes intent clear. Setting it to `false` means "accept any certificate, including self-signed, expired, or from unknown CAs" — this completely defeats TLS authentication.

---

### Self-Signed Certificates for Development

In development, you often want HTTPS locally without buying a certificate. Self-signed certificates are the solution — but they'll cause browser warnings because no trusted CA signed them.

```bash
# Generate a self-signed certificate for localhost development
openssl req -x509 -newkey rsa:2048 -nodes \
  -keyout localhost.key \
  -out localhost.crt \
  -days 365 \
  -subj '/CN=localhost' \
  -addext "subjectAltName=DNS:localhost,IP:127.0.0.1"

# Use in Node.js
const server = https.createServer({
  key: fs.readFileSync('./localhost.key'),
  cert: fs.readFileSync('./localhost.crt'),
}, app);
```

**Better alternative: `mkcert`** — a tool that creates a local CA, installs it in your system's trust store, then issues certificates signed by that local CA. No browser warnings, and it works with any domain you want for local dev:

```bash
# Install mkcert
brew install mkcert        # macOS
mkcert -install            # Installs local CA into system trust store

# Create cert for local dev
mkcert localhost 127.0.0.1 api.localdev.me

# Now browsers trust *.pem — no security warnings!
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

### Reading `openssl s_client` Output

When you run `openssl s_client -connect google.com:443`, the output can be overwhelming. Here's what to look for:

```
CONNECTED(00000003)
depth=2 C = US, O = Google Trust Services LLC, CN = GTS Root R1
verify return:1
depth=1 C = US, O = Google Trust Services LLC, CN = GTS CA 1C3
verify return:1
depth=0 CN = *.google.com
verify return:1
---
Certificate chain
 0 s:CN = *.google.com                         ← Your cert (depth 0)
   i:C = US, O = Google Trust Services LLC, CN = GTS CA 1C3  ← Signed by
 1 s:C = US, O = Google Trust Services LLC, CN = GTS CA 1C3  ← Intermediate
   i:C = US, O = Google Trust Services LLC, CN = GTS Root R1  ← Signed by
---
Server certificate
-----BEGIN CERTIFICATE-----
... (base64 encoded cert data)
-----END CERTIFICATE-----
---
No client certificate CA names sent
---
SSL handshake has read 4915 bytes and written 317 bytes
Verification: OK                       ← Chain verified successfully
---
New, TLSv1.3, Cipher is TLS_AES_256_GCM_SHA384   ← TLS version and cipher
Server public key is 256 bit           ← EC key (256 bit = strong, small)
Secure Renegotiation IS NOT supported  ← (not needed for TLS 1.3)
Compression: NONE
Expansion: NONE
No ALPN negotiated
Early data was not sent                ← 0-RTT not used this connection
Verify return code: 0 (ok)             ← 0 = no error
```

Key things to check:
- `Verification: OK` — Certificate chain valid
- `TLSv1.3` — Modern protocol in use
- `Verify return code: 0 (ok)` — No errors

If you see `Verify return code: 19 (self signed certificate in certificate chain)` — the certificate is self-signed or the chain is broken.

### Monitoring Certificate Expiry Proactively

Don't wait for user complaints. Set up automated monitoring:

```bash
# Check days until expiry
echo | openssl s_client -connect api.myapp.com:443 2>/dev/null | \
  openssl x509 -noout -enddate | \
  awk -F= '{print $2}' | \
  xargs -I{} date -d "{}" +%s | \
  xargs -I{} bash -c 'echo $(( ({} - $(date +%s)) / 86400 )) days remaining'

# Nagios/monitoring-style check
# Many monitoring tools (Datadog, Uptime Robot, Prometheus blackbox_exporter)
# have built-in TLS certificate expiry checks.

# Prometheus blackbox_exporter scrapes TLS info and exposes:
# probe_ssl_earliest_cert_expiry (Unix timestamp of cert expiry)
# Alert rule: (probe_ssl_earliest_cert_expiry - time()) / 86400 < 30
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

### Breaking Down the RTT Math

A **round trip time (RTT)** of 200ms means it takes 200ms for a packet to go from the client to the server and back. This is typical for a US ↔ Europe connection.

**A full TCP + TLS 1.2 connection to first byte:**
```
TCP SYN                     +0ms
TCP SYN-ACK                 +200ms  (1 TCP RTT)
TCP ACK + TLS ClientHello   +200ms  (sent immediately)
TLS ServerHello             +400ms  (1 TLS RTT)
TLS Finished (client)       +400ms  (sent immediately)
TLS Finished (server)       +600ms  (2nd TLS RTT)
First HTTP request          +600ms  (sent immediately)
First HTTP response         +800ms  (1 HTTP RTT)
Total: ~800ms to first byte
```

**TCP + TLS 1.3:**
```
TCP SYN                     +0ms
TCP SYN-ACK                 +200ms  (1 TCP RTT)
TCP ACK + TLS ClientHello   +200ms  (key share included!)
TLS ServerHello+Finished    +400ms  (1 TLS RTT — keys derived!)
First HTTP request          +400ms  (sent immediately after TLS done)
First HTTP response         +600ms  (1 HTTP RTT)
Total: ~600ms to first byte (200ms saved!)
```

**TLS 1.3 + 0-RTT + HTTP/2 multiplexing:**

With session resumption and HTTP/2, a returning visitor's browser can send the HTTP request *in the same packet* as the TLS ClientHello. The response arrives after just 1 RTT (TCP + TLS + HTTP all in one exchange).

### 0-RTT: The Security Trade-off

TLS 1.3 0-RTT (also called "Early Data") lets a returning client send encrypted application data in the very first ClientHello packet, before the handshake is complete. This is achieved using a **session ticket** — a token the server gave the client in a previous session that encodes a resumption secret.

**The risk: Replay attacks.** A network attacker could capture the 0-RTT data and replay it — sending it again to the server. The server receives what looks like a valid encrypted request.

For GET requests and idempotent reads: replay is harmless (same data fetched twice).
For POST requests that transfer money or submit forms: replay is catastrophic.

**Mitigation:** Never use 0-RTT for state-changing operations. CDNs and ALBs that implement 0-RTT typically only forward early data for idempotent HTTP methods (GET, HEAD) and reject it for POST/PUT/DELETE.

### EC Keys vs RSA Keys

Elliptic Curve (EC) keys at 256-bit provide equivalent security to RSA at 3072-bit. This means:
- **Smaller certificates** — faster to transmit, less overhead in the handshake
- **Faster signing/verification** — EC operations are cheaper than RSA for equivalent security
- **Better forward secrecy performance** — ECDH is faster than DHE at equivalent security levels

The standard EC curve for TLS is **P-256** (secp256r1) or **X25519**. X25519 is slightly faster and has better security properties (designed to avoid potential backdoors in NIST curves). TLS 1.3 supports both.

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

#### Why `NODE_TLS_REJECT_UNAUTHORIZED = '0'` Is So Dangerous

Setting this environment variable makes Node.js accept *any* certificate — expired, self-signed, for the wrong domain, signed by a random unknown CA. This means if an attacker is in a position to intercept traffic (man-in-the-middle), they can present any certificate and Node.js will happily proceed, encrypting all data for the attacker.

The typical situation where developers reach for this "fix" is when connecting to a service with a self-signed certificate or an internal CA. The *correct* fix is to specify the CA file:

```javascript
// ✅ When your service uses a self-signed cert or private CA
const https = require('https');
const fs = require('fs');

const agent = new https.Agent({
  ca: fs.readFileSync('./internal-ca.pem'),   // Your internal CA's certificate
  rejectUnauthorized: true                    // Still verify, just against your CA
});

// All requests through this agent verify against your internal CA
fetch('https://internal-service.company.com/api', { agent });
```

Another common scenario is development against localhost. Use `mkcert` (described above) instead of disabling verification entirely.

#### The MITM Attack in Detail

Here's what a man-in-the-middle attack looks like when certificate verification is disabled:

```
                                   Eve (attacker)
                                   ┌─────────────┐
                                   │             │
Browser ──── TLS ──────────────► Eve ──── TLS ──►  Real Server
             (uses Eve's cert)         (uses real cert)

Browser thinks it's talking to api.myapp.com
Eve sees ALL decrypted data before re-encrypting to real server
```

With proper certificate verification, the browser would see that Eve's certificate isn't signed by a trusted CA for `api.myapp.com` and abort the connection.

---

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

#### Why `x-forwarded-proto` and Not `req.secure`?

When TLS terminates at the ALB (Option 1 from above), Node.js receives plain HTTP. `req.secure` will always be `false` because Node.js only sees HTTP. The ALB adds the `X-Forwarded-Proto: https` header to tell the backend what protocol the *client* used. Your redirect logic must check this header, not `req.secure`.

#### HSTS — Strict Transport Security Explained

Even with an HTTP → HTTPS redirect, there's a vulnerability window: the very first HTTP request (before the redirect) travels in plain text. An attacker could intercept that first request, modify it, and prevent the redirect from happening (SSL stripping attack).

**HSTS (HTTP Strict Transport Security)** tells the browser: "Once you've seen this header, never make plain HTTP requests to this domain for the next `max-age` seconds. Always use HTTPS, even before making a request."

```
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```

- `max-age=31536000` — Remember this rule for 1 year (in seconds)
- `includeSubDomains` — Also applies to all subdomains (`api.`, `www.`, etc.)
- `preload` — Request inclusion in the browser's hardcoded HSTS preload list (your site ships pre-loaded in Chrome/Firefox). Even the very first request is HTTPS.

**HSTS Preload list** (`https://hstspreload.org/`): Sites on this list are hardcoded into Chrome, Firefox, Safari, and Edge. Browsers *never* make HTTP requests to these domains, even on the very first visit, even after clearing browser data. This is the ultimate protection — but requires `includeSubDomains` and `max-age` ≥ 31536000, and is very hard to undo (takes months to remove from the list).

---

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

### ❌ Mixing HTTP and HTTPS Resources (Mixed Content)

A subtle but common mistake: your page loads over HTTPS, but it references a resource (image, script, API) over HTTP.

```html
<!-- ❌ Mixed content — browser blocks this on HTTPS pages -->
<script src="http://cdn.example.com/jquery.js"></script>
<img src="http://images.example.com/photo.jpg" />

<!-- ✅ Protocol-relative URLs (picks the right scheme) -->
<script src="//cdn.example.com/jquery.js"></script>

<!-- ✅ Explicit HTTPS -->
<script src="https://cdn.example.com/jquery.js"></script>
```

Modern browsers block **active mixed content** (scripts, iframes, XHR) outright — the resource won't load at all and the browser shows a console error. **Passive mixed content** (images, audio, video) may show a warning but still load (behavior varies by browser version).

The `Content-Security-Policy: upgrade-insecure-requests` header tells the browser to automatically upgrade all HTTP subresource requests to HTTPS before making them — a good safety net.

---

## Practice Exercises

### Exercise 1: Inspect TLS
Use `openssl s_client` to connect to `google.com:443`. Identify: TLS version, cipher suite, certificate issuer, and expiry date.

**Extended challenge:** Compare the outputs from `google.com`, `cloudflare.com`, and a bank site you use. Do all use TLS 1.3? Do they use EC or RSA keys? What cipher suite did each negotiate?

### Exercise 2: Certificate Comparison
Compare the TLS setup of `github.com`, `google.com`, and `amazon.com`. Which uses TLS 1.3? What cipher suites?

**Extended challenge:** Look at the SAN field on each cert. How many domains does each certificate cover? What's the key size? Does each server send OCSP stapling? (Look for "OCSP Response" in the `openssl s_client` output.)

### Exercise 3: HTTPS Node.js Server
Create a self-signed certificate and set up an HTTPS Express server. Test with `curl -k` (skip verification) and without.

**Extended challenge:** Use `mkcert` to create a locally-trusted certificate. Verify you can open it in your browser with no warnings. Then add HSTS headers and the HTTP → HTTPS redirect. Use `curl -I http://localhost` and verify it returns a 301 redirect.

### Exercise 4: Certificate Chain Inspection
Run the following and interpret every line of output:
```bash
openssl s_client -connect github.com:443 -showcerts
```
How many certificates are in the chain? Which is the leaf? Which is the intermediate? Find the `Not After` date for each.

### Exercise 5: Simulate MITM (Educational)
In a controlled local environment, use `mitmproxy` to intercept HTTPS traffic. Observe what happens when certificate verification is enabled vs disabled in the client. This demonstrates exactly why `rejectUnauthorized: false` is dangerous.

---

## Interview Q&A

**Q1: How does the TLS handshake work?**
> Client sends ClientHello (supported ciphers, random, DH key share). Server chooses cipher, sends certificate, its own DH key share, Certificate Verify signature, and Finished. Client verifies certificate chain, verifies the signature, computes shared secret using Diffie-Hellman. Both derive session keys. TLS 1.3 does this in 1 RTT (vs 2 RTT in TLS 1.2) because the client speculatively sends a DH key share upfront.

**Q2: What is the difference between TLS 1.2 and TLS 1.3?**
> TLS 1.3: 1 RTT handshake (vs 2), 0-RTT resumption, removed insecure ciphers (RSA key exchange, CBC mode, SHA-1), forward secrecy mandatory, simplified to 5 strong cipher suites, certificate encrypted during handshake. Result: faster, simpler, and more secure. RSA key exchange removal is the biggest security improvement — it makes forward secrecy mandatory so past sessions can't be decrypted even if the private key is later compromised.

**Q3: What is TLS termination and where should it happen?**
> TLS termination = where encryption ends and plain HTTP begins. At ALB: offloads CPU, ACM manages certs, simple. At Node.js: encrypted end-to-end within VPC, compliance requirements. Most apps terminate at ALB — VPC is already a trusted, isolated network. For PCI-DSS/HIPAA, end-to-end encryption may be required even inside the VPC.

**Q4: What is certificate pinning and when should you use it?**
> Pinning hard-codes the expected certificate or public key in your app, preventing even trusted CAs from impersonating your server. Used in mobile apps for banking/security — an app pins the exact certificate (or public key hash) it expects to see. Not for web apps (certificates rotate every 90 days and you can't force-update browsers). React Native: can implement via SSL pinning libraries like `react-native-ssl-pinning`. Risk: if you pin a certificate and it rotates without updating the app, all users are locked out until they update.

**Q5: What happens if your TLS certificate expires?**
> All HTTPS connections fail. Browsers show "Your connection is not private" warnings with no easy way for users to proceed. API clients get `CERTIFICATE_HAS_EXPIRED` errors. SEO ranking drops (HTTPS is a ranking factor). Revenue impact is immediate. Prevention: ACM auto-renewal (best), Let's Encrypt certbot systemd timer, monitoring with certificate expiry alerts 30+ days in advance via Prometheus blackbox_exporter or a managed service.

**Q6: Explain Forward Secrecy. Why does it matter?**
> Forward secrecy means past sessions remain secure even if the server's private key is compromised in the future. In TLS 1.2 with RSA key exchange, the client encrypted the pre-master secret with the server's public key. An attacker who recorded all traffic could later use a stolen private key to decrypt everything. TLS 1.3 mandates ephemeral Diffie-Hellman (ECDHE) — the session key is derived from temporary DH keys that are discarded after the connection. The server's certificate key is only used for signing, never for key derivation. Stealing the private key years later gives the attacker nothing — the ephemeral keys are gone.

**Q7: What is OCSP stapling?**
> Without stapling, the browser contacts the CA's OCSP server to verify a certificate hasn't been revoked — an extra network round trip that adds latency and leaks your browsing to the CA. With OCSP stapling, the *server* periodically fetches its own signed OCSP response from the CA (valid for ~24 hours) and includes it in the TLS handshake. The browser gets the freshness proof without a separate CA request — faster handshake, no privacy leak. Enable in Nginx with `ssl_stapling on; ssl_stapling_verify on;`.

---

Prev : [08 UDP And When To Use It](./08_UDP_And_When_To_Use_It.md) | Index: [0 Index](./0_Index.md) | Next : [10 Routing And NAT](./10_Routing_And_NAT.md)