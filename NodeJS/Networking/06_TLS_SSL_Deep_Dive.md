# 📌 06 — TLS/SSL Deep Dive: Encryption at the Socket Level

## 🧠 Concept Explanation

### Basic → Intermediate
TLS (Transport Layer Security) is the successor to SSL. It provides encryption, authentication, and integrity for network communication (HTTPS).

### Advanced → Expert
In Node.js, TLS is implemented using the **OpenSSL** library via the `tls` module. 
A TLS connection involves a **Heavy Handshake** on top of the TCP handshake:
1. **Client Hello**: Negotiate ciphers and protocols.
2. **Server Hello**: Server sends its Certificate.
3. **Key Exchange**: Client and Server agree on a **Symmetric Key** using Diffie-Hellman or RSA.
4. **Finished**: Encrypted communication begins.

This adds **Round Trip Time (RTT)** and CPU overhead for the initial asymmetric encryption (RSA/ECDSA).

---

## 🏗️ Common Mental Model
"TLS encrypts everything."
**Correction**: TLS encrypts the **Payload** and most of the **Headers**. However, the IP addresses, Ports, and the **SNI (Server Name Indication)** are visible in plain text during the handshake.

---

## ⚡ Actual Behavior: Session Resumption
To avoid the heavy cost of the full handshake for repeat clients, TLS supports:
1. **Session IDs**: The server stores the session state and gives the client an ID.
2. **Session Tickets**: The server sends an encrypted state "ticket" to the client.
These allow for an **Abbreviated Handshake** (0-RTT or 1-RTT).

---

## 🔬 Internal Mechanics (OpenSSL + libuv)

### The JS ↔ OpenSSL Boundary
Encryption is a CPU-bound task. Node.js offloads the actual encryption/decryption logic to OpenSSL (C code). However, data must be moved between V8 Buffers and OpenSSL memory spaces, which has a cost.

### ALPN (Application-Layer Protocol Negotiation)
TLS is used to negotiate which protocol to use next (HTTP/1.1 vs HTTP/2) without requiring extra round trips.

---

## 📐 ASCII Diagrams

### TLS 1.2 Handshake (Simplifed)
```text
  CLIENT                                 SERVER
    │                                       │
    │ 1. [Client Hello] (Ciphers, Random)   │
    ├──────────────────────────────────────▶│
    │                                       │
    │ 2. [Server Hello] (Cert, ServerRandom)│
    │◀──────────────────────────────────────┤
    │                                       │
    │ 3. [Key Exchange] (Encrypted Premaster)│
    ├──────────────────────────────────────▶│
    │                                       │
    │ 4. [Change Cipher Spec]               │
    │◀─────────────────────────────────────▶│
    │                                       │
    │ (Encrypted Data Begins)               │
```

---

## 🔍 Code Example: Secure TLS Server
```javascript
const tls = require('tls');
const fs = require('fs');

const options = {
  key: fs.readFileSync('server-key.pem'),
  cert: fs.readFileSync('server-cert.pem'),
  // Force secure protocols and ciphers
  minVersion: 'TLSv1.2',
  ciphers: 'ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256'
};

const server = tls.createServer(options, (socket) => {
  console.log('Client connected:', 
    socket.authorized ? 'Authorized' : 'Unauthorized');
  
  socket.write('Welcome to the Secure Layer\n');
  socket.pipe(socket);
});

server.listen(8000);
```

---

## 💥 Production Failures & Debugging

### Scenario: The Certificate Expiry Outage
**Problem**: Suddenly, all mobile app users see "SSL Error" and cannot connect.
**Reason**: The Leaf or Intermediate certificate expired.
**Debug**: `openssl s_client -connect myapi.com:443 -showcerts`
**Fix**: Use automated tools like **Certbot** or AWS ACM with auto-renewal.

### Scenario: High CPU during "Handshake Storm"
**Problem**: CPU spikes to 100% and stays there during a traffic burst.
**Reason**: Each new TLS connection requires a CPU-intensive RSA/ECDSA key exchange.
**Fix**: Enable **TLS Session Resumption** or use a hardware-accelerated SSL terminator (like an F5 or AWS ALB).

---

## 🧪 Real-time Production Q&A

**Q: "Is TLS 1.3 much faster than TLS 1.2?"**
**A**: **Yes.** TLS 1.3 reduces the handshake to **one round trip** (1-RTT) and supports 0-RTT for repeat connections. It also removes legacy, insecure ciphers, making the negotiation faster.

---

## 🧪 Debugging Toolchain
- **`openssl s_client`**: The "Swiss Army Knife" for debugging TLS connections.
- **`sslyze`**: Scans a server to see supported ciphers and vulnerabilities.

---

## 🏢 Industry Best Practices
- **Prefer TLS 1.3**: Whenever possible.
- **OCSP Stapling**: The server "staples" a fresh proof of certificate validity from the CA, so the client doesn't have to make an extra request to check for revocation.

---

## 💼 Interview Questions
**Q: What is SNI (Server Name Indication)?**
**A**: SNI allows a single IP address to host multiple SSL certificates for different domains. The client sends the hostname it wants to connect to in the initial "Client Hello" so the server knows which certificate to provide.

---

## 🧩 Practice Problems
1. Generate a self-signed certificate and key using OpenSSL and build a HTTPS server.
2. Use `curl --trace-ascii` to observe the TLS handshake steps of a production website.

---

**Prev:** [05_TCP_UDP_Basics.md](./05_TCP_UDP_Basics.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [07_HTTP2_and_HTTP3.md](./07_HTTP2_and_HTTP3.md)
