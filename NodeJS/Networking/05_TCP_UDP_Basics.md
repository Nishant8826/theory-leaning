# 📌 05 — TCP and UDP Basics: The Transport Layer Internals

## 🧠 Concept Explanation

### Basic → Intermediate
TCP (Transmission Control Protocol) is a connection-oriented protocol that guarantees delivery and order. UDP (User Datagram Protocol) is connectionless and "best-effort," prioritize speed over reliability.

### Advanced → Expert
At a staff level, we must understand the **Kernel/User-space boundary** in transport networking.
1. **TCP (Reliability)**: Involves the **3-way handshake** (SYN, SYN-ACK, ACK). It implements **Flow Control** (using the Window Size) and **Congestion Control** (e.g. TCP BBR, Cubic). 
2. **UDP (Throughput)**: Low overhead. No handshakes, no order guarantees. Ideal for VOIP, gaming, and HTTP/3 (QUIC).

Node.js `net` module (TCP) and `dgram` module (UDP) are thin wrappers around the `socket` and `bind` syscalls.

---

## 🏗️ Common Mental Model
"TCP is slow, UDP is fast."
**Correction**: TCP is slower for the *initial* connection due to handshakes. However, modern TCP implementations (like BBR) are incredibly efficient. UDP is only "fast" because it avoids the overhead of ensuring reliability; if your app needs reliability, implementing it on top of UDP can be slower than using TCP.

---

## ⚡ Actual Behavior: Backpressure and Buffers
TCP has a **Send Buffer** and a **Receive Buffer** in the kernel. If your Node.js app writes faster than the network can handle, the kernel buffer fills up. Node's `socket.write()` will return `false`, signaling **Backpressure**.

---

## 🔬 Internal Mechanics (libuv + syscalls)

### The Socket Lifecycle
1. `socket(AF_INET, SOCK_STREAM, 0)`: Creates a socket.
2. `bind()`: Assigns an IP/Port.
3. `listen()`: Puts the socket in a state to accept connections.
4. `accept()`: Blocks (or notifies epoll) when a new client connects.

### Nagle's Algorithm (`setNoDelay`)
By default, TCP buffers small packets to send one large one (Nagle's). This increases latency for real-time apps. Node.js enables `socket.setNoDelay(true)` by default to disable Nagle's for lower latency.

---

## 📐 ASCII Diagrams

### TCP 3-Way Handshake
```text
  CLIENT                                 SERVER
    │                                       │
    │ 1. [SYN] Seq=0                        │
    ├──────────────────────────────────────▶│
    │                                       │
    │ 2. [SYN, ACK] Seq=0 Ack=1             │
    │◀──────────────────────────────────────┤
    │                                       │
    │ 3. [ACK] Seq=1 Ack=1                  │
    ├──────────────────────────────────────▶│
    │                                       │
    │ (Connection Established)              │
```

---

## 🔍 Code Example: Raw TCP Server vs UDP
```javascript
const net = require('net');
const dgram = require('dgram');

// TCP Server: Guaranteed Delivery
const tcpServer = net.createServer((socket) => {
  socket.on('data', (data) => {
    socket.write('TCP ACK');
  });
}).listen(8080);

// UDP Server: Low Latency
const udpServer = dgram.createSocket('udp4');
udpServer.on('message', (msg, rinfo) => {
  console.log(`UDP from ${rinfo.address}:${rinfo.port}`);
  // No 'ACK' unless you implement it manually
});
udpServer.bind(8081);
```

---

## 💥 Production Failures & Debugging

### Scenario: The "TCP Meltdown"
**Problem**: A microservice communication starts timing out. `netstat` shows thousands of connections in `TIME_WAIT` state.
**Reason**: You are creating a new TCP connection for every small request instead of using **Connection Pooling**. The OS runs out of ephemeral ports.
**Fix**: Use `keep-alive` to reuse connections.

### Scenario: UDP Packet Loss
**Problem**: In a real-time game, players "teleport" or actions are lost.
**Reason**: Network congestion caused UDP packets to be dropped. Since UDP doesn't retransmit, the app state becomes inconsistent.
**Fix**: Implement **Forward Error Correction (FEC)** or sequence numbers in your application logic.

---

## 🧪 Real-time Production Q&A

**Q: "When should I use UDP in a backend system?"**
**A**: Use it for **Metrics collection** (StatsD), **Service Discovery** (mDNS), or **Media Streaming**. If a packet of metrics is lost, it doesn't break the system, and it's better than blocking your app's main thread waiting for a TCP ACK.

---

## 🧪 Debugging Toolchain
- **`netstat -ant`**: View the state of all TCP connections.
- **`ss -tap`**: A faster, modern alternative to netstat.
- **`nmap`**: Check if a port is open and reachable.

---

## 🏢 Industry Best Practices
- **Use keep-alive**: To avoid the 3-way handshake cost for every request.
- **Understand MSS/MTU**: Avoid sending packets larger than 1500 bytes to prevent fragmentation in the network path.

---

## 💼 Interview Questions
**Q: What is the TIME_WAIT state in TCP?**
**A**: It is a state where the socket remains closed but "reserved" by the kernel for a period (usually 2 minutes) after the connection is terminated. This ensures that any delayed packets still in the network don't interfere with a new connection using the same port.

---

## 🧩 Practice Problems
1. Write a script that counts the number of TCP connections in each state (`ESTABLISHED`, `TIME_WAIT`, etc.) by parsing `/proc/net/tcp`.
2. Implement a simple "Reliable UDP" protocol that uses sequence numbers and manual ACKs.

---

**Prev:** [04_WebSockets_SocketIO.md](./04_WebSockets_SocketIO.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [06_TLS_SSL_Deep_Dive.md](./06_TLS_SSL_Deep_Dive.md)
