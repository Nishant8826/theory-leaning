# TLS/SSL Handshake

> 📌 **File:** 10_TLS_SSL_Handshake.md | **Level:** Full-Stack Dev → Networking Expert

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
│                                                                      │
│  Option 2: End-to-end TLS                                           │
│    Browser ──HTTPS──► ALB ──HTTPS──► EC2 (Node.js with TLS)       │
│    Both ALB and Node.js have certificates.                          │
└──────────────────────────────────────────────────────────────────────┘
```

---

## How does it actually work?

### Before TLS: Public-Key Cryptography

To understand TLS, you need to understand one fundamental problem: **how do two strangers securely share a secret over an insecure channel?**

The solution is **asymmetric (public-key) cryptography**. Every participant has two mathematically linked keys:
- **Public key** — can be shared with anyone. Used to *encrypt* data or *verify* a signature.
- **Private key** — kept secret forever. Used to *decrypt* data or *create* a signature.

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
```

---

### Diffie-Hellman Key Exchange — The Core Magic

This is the mathematical trick that makes TLS possible. Two parties can agree on a shared secret *in public* without ever transmitting the secret.

The color analogy:
```
Public information: Base color = Yellow

Alice secret: Red
Alice mix: Yellow + Red = Orange → sends Orange to Bob

Bob secret: Blue
Bob mix: Yellow + Blue = Green → sends Green to Alice

Alice: Green + Red = Brown
Bob:   Orange + Blue = Brown (Shared Secret!)
```

---

### What TLS Protects

```
┌──────────────────────────────────────────────────────────────────┐
│  Protected (encrypted)         │ NOT protected (visible)        │
├────────────────────────────────┼────────────────────────────────┤
│  HTTP headers                  │ IP addresses (src/dst)         │
│  HTTP body (JSON, HTML)        │ TCP ports (src/dst)            │
│  URL path (/api/users)         │ DNS queries (domain name)      │
│  Cookies                       │ Packet sizes                   │
│  Authorization tokens          │ SNI (Server Name Indication)   │
└────────────────────────────────┴────────────────────────────────┘
```

---

### Certificate Chain

```
Browser verifies:
  Your certificate (api.myapp.com)
    ├── Signed by: Intermediate CA (Let's Encrypt R3)
    │     └── Signed by: Root CA (ISRG Root X1)
    │           └── Pre-installed in browser's trust store ✅
```

---

## AWS Certificate Manager (ACM)

ACM provides FREE TLS certificates for AWS managed services (ALB, CloudFront, API Gateway). It handles validation (DNS or Email) and auto-renews certificates automatically. Note that ACM certificates cannot be used on EC2 directly.

---

### Let's Encrypt on EC2 (Nginx)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d api.myapp.com

# Auto-renewal verification
sudo certbot renew --dry-run
```

---

## Node.js Implementation

```javascript
const https = require('https');
const fs = require('fs');
const express = require('express');

const app = express();

const server = https.createServer({
  key: fs.readFileSync('/etc/letsencrypt/live/api.myapp.com/privkey.pem'),
  cert: fs.readFileSync('/etc/letsencrypt/live/api.myapp.com/fullchain.pem'),
  minVersion: 'TLSv1.2',
  ciphers: [
    'TLS_AES_256_GCM_SHA384',
    'TLS_CHACHA20_POLY1305_SHA256',
    'TLS_AES_128_GCM_SHA256'
  ].join(':')
}, app);

server.listen(443);

// HTTP → HTTPS redirect
const http = require('http');
http.createServer((req, res) => {
  res.writeHead(301, { Location: `https://${req.headers.host}${req.url}` });
  res.end();
}).listen(80);
```

---

## Practice Exercises

### Exercise 1: Test TLS Connection
Use `openssl s_client -connect google.com:443 -servername google.com` to check the TLS version and cipher suite of Google.

### Exercise 2: HTTPS Node.js Server
Create a self-signed certificate and set up an HTTPS Express server locally. Verify you can access it via browser.

---

## Interview Q&A

**Q1: How does the TLS handshake work?**
> Client sends ClientHello (supported ciphers, random, DH key share). Server chooses cipher, sends certificate, its own DH key share, Certificate Verify signature, and Finished. Client verifies certificate chain, verifies the signature, computes shared secret using Diffie-Hellman. Both derive session keys. TLS 1.3 does this in 1 RTT (vs 2 RTT in TLS 1.2) because the client speculatively sends a DH key share upfront.

**Q2: What is the difference between TLS 1.2 and TLS 1.3?**
> TLS 1.3: 1 RTT handshake (vs 2), 0-RTT resumption, removed insecure ciphers (RSA key exchange, CBC mode, SHA-1), forward secrecy mandatory, simplified to 5 strong cipher suites, certificate encrypted during handshake.

**Q3: What is TLS termination and where should it happen?**
> TLS termination = where encryption ends and plain HTTP begins. At ALB: offloads CPU, ACM manages certs, simple. At Node.js: encrypted end-to-end within VPC, compliance requirements. Most apps terminate at ALB — VPC is already a trusted, isolated network.

**Q4: Explain Forward Secrecy. Why does it matter?**
> Forward secrecy means past sessions remain secure even if the server's private key is compromised in the future. In TLS 1.2 with RSA key exchange, the client encrypted the pre-master secret with the server's public key. An attacker who recorded all traffic could later use a stolen private key to decrypt everything. TLS 1.3 mandates ephemeral Diffie-Hellman (ECDHE) — the session key is derived from temporary DH keys that are discarded after the connection.

---

Prev : [09 UDP And When To Use It](./09_UDP_And_When_To_Use_It.md) | Index: [00 Index](./00_Index.md) | Next : [11 IP Addressing And Subnetting](./11_IP_Addressing_And_Subnetting.md)
