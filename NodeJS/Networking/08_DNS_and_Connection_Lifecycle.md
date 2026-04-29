# 📌 08 — DNS and Connection Lifecycle: Resolvers and Handshakes

## 🧠 Concept Explanation

### Basic → Intermediate
DNS (Domain Name System) is the phonebook of the internet. It translates a human-readable name (google.com) into an IP address (142.250.190.46).

### Advanced → Expert
At a systems level, DNS resolution in Node.js is a frequent source of hidden latency. Node.js provides two different ways to resolve DNS:
1. **`dns.lookup()`**: Uses the OS's `getaddrinfo(3)` syscall. This is **synchronous** at the OS level, so Node.js must offload it to the **libuv thread pool**. This is the method used by `http.get()` and `net.connect()` by default.
2. **`dns.resolve()`**: Uses the **c-ares** library. It performs its own network requests to DNS servers and is truly asynchronous (doesn't use the thread pool). However, it doesn't use the `/etc/hosts` file or local OS cache.

---

## 🏗️ Common Mental Model
"DNS resolution is instant."
**Correction**: DNS resolution can take anywhere from 1ms (cache hit) to 500ms+ (cache miss, multiple recursive queries). In a microservices architecture, this can be the single largest contributor to latency.

---

## ⚡ Actual Behavior: Thread Pool Starvation
Because `dns.lookup` (used by `http`) uses the libuv thread pool, if you have a massive number of DNS resolutions happening simultaneously, you can exhaust the 4 threads in the pool, causing all other tasks (like file I/O) to hang.

---

## 🔬 Internal Mechanics (libuv + c-ares + syscalls)

### getaddrinfo(3)
This is the standard C library function for DNS. It reads `/etc/nsswitch.conf`, `/etc/hosts`, and then queries the nameservers in `/etc/resolv.conf`. Because it blocks the thread, libuv must manage it.

### The Connection Lifecycle
1. **DNS Lookup**: Find the IP.
2. **TCP Handshake**: SYN ──▶ SYN-ACK ──▶ ACK.
3. **TLS Handshake**: (If HTTPS) Exchange certificates and keys.
4. **HTTP Request**: Send the headers and body.

---

## 📐 ASCII Diagrams

### DNS Resolution Path (lookup)
```text
  NODE.JS (JS)
     │
     ▼ [ libuv Thread Pool ]
     │
  getaddrinfo() syscall
     │
     ▼ [ OS Resolver ]
     │
  Check /etc/hosts ──▶ Check Local Cache ──▶ Query DNS Server (UDP 53)
```

---

## 🔍 Code Example: Comparing Resolvers
```javascript
const dns = require('dns');

const domain = 'google.com';

// Method 1: lookup (standard, uses thread pool, uses /etc/hosts)
console.time('lookup');
dns.lookup(domain, (err, address) => {
  console.log('Lookup Address:', address);
  console.timeEnd('lookup');
});

// Method 2: resolve (network-only, non-blocking, ignores /etc/hosts)
console.time('resolve');
dns.resolve4(domain, (err, addresses) => {
  console.log('Resolve Address:', addresses[0]);
  console.timeEnd('resolve');
});
```

---

## 💥 Production Failures & Debugging

### Scenario: The "First Request" Latency Spike
**Problem**: The first request to a service is slow (500ms), but subsequent requests are fast (10ms).
**Reason**: The service name isn't in the local DNS cache. The OS has to perform a full recursive lookup.
**Fix**: Use a **DNS Cache** at the application level (e.g. `dnscache` package) or use a local caching resolver like **dnsmasq** on your server.

### Scenario: Thread Pool Exhaustion via DNS
**Problem**: During a spike in traffic, `fs.readFile` becomes incredibly slow.
**Reason**: You are making hundreds of outgoing HTTP requests. Each one triggers a `dns.lookup`, which fills the 4-thread libuv pool. The file read is stuck waiting for a thread.
**Fix**: Increase `UV_THREADPOOL_SIZE` or use an IP address directly instead of a hostname for high-frequency internal calls.

---

## 🧪 Real-time Production Q&A

**Q: "Should I hardcode IP addresses in my config to avoid DNS?"**
**A**: **No.** IPs can change (especially in Cloud/K8s). Use **DNS Caching** instead. It gives you the performance of hardcoded IPs with the flexibility of hostnames.

---

## 🧪 Debugging Toolchain
- **`dig @8.8.8.8 google.com`**: Query a specific DNS server to test resolution.
- **`host -v google.com`**: Detailed breakdown of the DNS response.

---

## 🏢 Industry Best Practices
- **Implement Application-Level DNS Caching**: Node.js does **not** cache DNS results by default. 
- **Use `keep-alive`**: Reusing a connection means you skip the DNS lookup and the TCP/TLS handshakes entirely for subsequent requests.

---

## 💼 Interview Questions
**Q: What is the difference between `dns.lookup` and `dns.resolve` in Node.js?**
**A**: `lookup` uses the OS's synchronous resolver via libuv threads and respects `/etc/hosts`. `resolve` uses the `c-ares` library for true async network-level resolution but ignores local OS configurations.

---

## 🧩 Practice Problems
1. Write a script that performs 1000 `dns.lookup` calls in a loop and measures how many threads are active in libuv (using `process.env.UV_THREADPOOL_SIZE`).
2. Build a simple DNS caching wrapper around `dns.lookup`.

---

**Prev:** [07_HTTP2_and_HTTP3.md](./07_HTTP2_and_HTTP3.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [09_Connection_Pooling.md](./09_Connection_Pooling.md)
