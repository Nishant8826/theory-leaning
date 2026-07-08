# TLS/SSL Handshake

> 📌 **File:** 10_TLS_SSL_Handshake.md | **Level:** Full-Stack Dev → Networking Expert

---

## What is it?

TLS (Transport Layer Security) encrypts the TCP connection between client and server. Every `https://` URL, every MongoDB Atlas connection, every Stripe API call uses TLS. Without TLS, anyone on the network (WiFi, ISP, routers) can read your users' passwords, credit cards, and API tokens in plain text.

**SSL is the old name. TLS is the current standard. When people say "SSL certificate," they mean TLS.**

### Why Does This Matter — The Real Threat

Imagine you're at a coffee shop, connected to the public WiFi. Without TLS, every HTTP request you make is sent as plain text over the air. Anyone else on the same network running a packet sniffer (like Wireshark — a free, legal tool) can read every byte you send. Your login form submits `username=john&password=mySecret123` and it literally travels across the room readable by anyone.

TLS solves this by encrypting the payload before it ever leaves your device. Even if someone captures every single packet, all they see is random-looking encrypted bytes — completely useless without the session key that only your browser and the server computed together.

There are three distinct problems TLS solves simultaneously:
- **Confidentiality** — No one in the middle can read what you send or receive.
- **Integrity** — No one in the middle can silently modify the data (e.g., change a bank transfer amount). Any tampering is detected.
- **Authenticity** — You are guaranteed to be talking to the real server (e.g., `google.com`), not an impostor router pretending to be it.

---

## Map it to MY STACK (CRITICAL)

There are two primary ways to set up TLS for your applications:

### Option 1: TLS Termination at the Load Balancer (Most Common)

```
Browser ──── HTTPS (TLS encrypted) ────► ALB (Virginia) ──── HTTP (Plain text) ────► EC2 (Virginia)
                                        (Decrypts here)
```

- **How it works:** Your domain certificate is uploaded to AWS Certificate Manager (ACM) and attached to your Application Load Balancer (ALB). The ALB decrypts incoming HTTPS traffic and forwards plain HTTP to your Node.js application.
- **Pros:** Extremely simple. Node.js doesn't need to manage certificates, cipher configurations, or waste CPU on decryption. ACM automatically renews certificates for free.
- **Cons:** Traffic between the ALB and EC2 is plain text. Inside AWS, this is generally secure (VPC traffic is isolated), but for strict compliance (HIPAA, PCI-DSS), you may need end-to-end encryption.

### Option 2: End-to-End TLS (Terminated at Node.js)

```
Browser ── HTTPS ──► NLB (Layer 4 TCP pass-through) ── HTTPS ──► EC2 (Node.js decrypts)
```

- **How it works:** You use a Network Load Balancer (NLB) or direct DNS routing to pass raw encrypted TCP packets straight to your EC2 instance. Your Node.js code loads the certificate files and handles decryption.
- **Pros:** Traffic is encrypted the entire way to your process.
- **Cons:** Node.js has to spend CPU cycles decrypting packets. You must write scripts to rotate certificates (e.g., Certbot/Let's Encrypt systemd timers) and restart your process.

---

## The Diffie-Hellman Key Exchange (Color Analogy)

How do a browser and a server agree on a secret key if a hacker is sniffing all packets from the start? They use the **Diffie-Hellman (DH)** mathematical algorithm.

```
Common Color (e.g., Yellow) — Known to Everyone (Sent on the wire)
  │
  ├─► Client picks Secret Color (e.g., Red)    ──► Mixes: Orange ──► Sends Orange (on wire)
  │                                                                     │
  ├─► Server picks Secret Color (e.g., Blue)   ──► Mixes: Green  ──► Sends Green (on wire)
  │
  └─► Client receives Green ──► Adds its Secret Red  ──► Shared Secret: Brown
      Server receives Orange ──► Adds its Secret Blue ──► Shared Secret: Brown
```

Even though the hacker saw Yellow, Orange, and Green on the wire, they cannot mix them to get Brown because they don't know the secret colors (Red or Blue). Elliptic Curve point multiplication does this mathematically.

The session key is derived from:
- Client DH key share + Server DH key share → Pre-master secret
- Pre-master secret + Client random + Server random → Master secret
- Master secret → Derived into multiple keys (one for client→server, one for server→client, one for MACs)

---

## TLS 1.2 vs TLS 1.3 — The Detailed Differences

```
┌────────────────────────────────────────────────────────────────────┐
│              TLS 1.2                    TLS 1.3                   │
├────────────────────────────────────────────────────────────────────┤
│  Handshake RTT:    2 RTT                1 RTT                     │
│  Resumption:       1-2 RTT              0-RTT (Early Data)        │
│  Ciphers:          37 cipher suites     5 strong cipher suites    │
│  Security:         Vulnerable ciphers   Secure by design          │
│                    (RSA, CBC, SHA-1)    (removed old ciphers)     │
└────────────────────────────────────────────────────────────────────┘
```

TLS 1.3 is faster because it combined the TCP ACK and the TLS Key Share in the first round trip. In TLS 1.2, it took 2 full RTTs (4 packets back and forth) just to establish the secure channel before any HTTP data could be sent.

---

## Self-Signed Certificates for Development

In development, you often want HTTPS locally without buying a certificate. Self-signed certificates are the solution — but they'll cause browser warnings because no trusted CA signed them.

```bash
# Generate a self-signed certificate for localhost development
openssl req -x509 -newkey rsa:2048 -nodes \
  -keyout localhost.key \
  -out localhost.crt \
  -days 365 \
  -subj '/CN=localhost' \
  -addext "subjectAltName=DNS:localhost,IP:127.0.0.1"
```

Use it in Node.js:
```javascript
const https = require('https');
const fs = require('fs');
const express = require('express');
const app = express();

const options = {
  key: fs.readFileSync('./localhost.key'),
  cert: fs.readFileSync('./localhost.crt')
};

https.createServer(options, app).listen(443);
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

# Test TLS version
curl --tls13 -I https://api.myapp.com        # Force TLS 1.3
curl --tlsv1.2 -I https://api.myapp.com      # Force TLS 1.2
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
└──────────────────────────────────────────────────────────────────┘
```

---

## Common Mistakes

### ❌ Disabling Certificate Verification

```javascript
// ❌ NEVER do this in production
process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0'; // Vulnerable to MITM

// ✅ Proper way — specify the CA file
const pool = new Pool({
  ssl: {
    rejectUnauthorized: true,
    ca: fs.readFileSync('./rds-combined-ca-bundle.pem')
  }
});
```

### ❌ Not Redirecting HTTP to HTTPS

```javascript
// ✅ Redirect all HTTP to HTTPS
app.use((req, res, next) => {
  if (req.headers['x-forwarded-proto'] !== 'https') {
    return res.redirect(301, `https://${req.hostname}${req.url}`);
  }
  next();
});
```

---

## Practice Exercises

### Exercise 1: Inspect TLS
Use `openssl s_client` to connect to `google.com:443`. Identify the TLS version, cipher suite, certificate issuer, and expiry date.

### Exercise 2: HTTPS Node.js Server
Create a self-signed certificate and set up an HTTPS Express server. Test with `curl -k` (skip verification) and without.

---

## Interview Q&A

**Q1: How does the TLS handshake work?**
> Client sends ClientHello (supported ciphers, random, DH key share). Server chooses cipher, sends certificate, its own DH key share, Certificate Verify signature, and Finished. Client verifies certificate chain, verifies the signature, computes shared secret using Diffie-Hellman. Both derive session keys. TLS 1.3 does this in 1 RTT (vs 2 RTT in TLS 1.2) because the client speculatively sends a DH key share upfront.

**Q2: What is the difference between TLS 1.2 and TLS 1.3?**
> TLS 1.3: 1 RTT handshake (vs 2), 0-RTT resumption, removed insecure ciphers (RSA key exchange, CBC mode, SHA-1), forward secrecy mandatory, simplified to 5 strong cipher suites, certificate encrypted during handshake. Result: faster, simpler, and more secure.

**Q3: What is TLS termination and where should it happen?**
> TLS termination = where encryption ends and plain HTTP begins. At ALB: offloads CPU, ACM manages certs, simple. At Node.js: encrypted end-to-end within VPC, compliance requirements. Most apps terminate at ALB — VPC is already a trusted, isolated network.

**Q4: What is certificate pinning and when should you use it?**
> Pinning hard-codes the expected certificate or public key in your app, preventing even trusted CAs from impersonating your server. Used in mobile apps for banking/security — an app pins the exact certificate (or public key hash) it expects to see. Not for web apps.

**Q5: What happens if your TLS certificate expires?**
> All HTTPS connections fail. Browsers show "Your connection is not private" warnings with no easy way for users to proceed. API clients get `CERTIFICATE_HAS_EXPIRED` errors. SEO ranking drops (HTTPS is a ranking factor). Revenue impact is immediate.

---

Prev : [09 UDP And When To Use It](./09_UDP_And_When_To_Use_It.md) | Index: [00 Index](./00_Index.md) | Next : [11 IP Addressing And Subnetting](./11_IP_Addressing_And_Subnetting.md)
