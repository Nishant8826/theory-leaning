# TCP/IP Model

> 📌 **File:** 07_TCP_IP_Model.md | **Level:** Full-Stack Dev → Networking Expert

---

## What is it?

The TCP/IP model is the practical, 4-layer model that built the internet. Unlike the conceptual 7-layer OSI model, the TCP/IP model corresponds directly to the protocols in actual use today (IP, TCP, UDP, HTTP).

---

## Map it to MY STACK (CRITICAL)

```
┌──────────────────────────────────────────────────────────────────┐
│  TCP/IP Layer       │ Real Protocols in Your Stack               │
├─────────────────────┼────────────────────────────────────────────┤
│  Application        │ HTTP, HTTPS, WebSocket, DNS, SSH           │
│  (OSI 5, 6, 7)      │ Express routers, JWTs, JSON payloads       │
│                     │                                            │
│  Transport          │ TCP (reliable APIs, DB connections)        │
│  (OSI 4)            │ UDP (fast metrics/StatsD, HTTP/3)          │
│                     │                                            │
│  Internet           │ IP (Routing, subnets, NAT, VPC CIDR)       │
│  (OSI 3)            │                                            │
│                     │                                            │
│  Network Access     │ Ethernet, Wi-Fi, MAC addresses             │
│  (OSI 1, 2)         │ AWS hypervisor networking                  │
└─────────────────────┴────────────────────────────────────────────┘
```

---

## The Four Layers Explained

```
1. Application Layer: The level your code lives.
   - You build an Express server that responds to GET /api/users.
   - The data is formatted as JSON text.

2. Transport Layer: Manages host-to-host communication.
   - The OS wraps your JSON data in a TCP segment.
   - It adds the source port (3000) and destination port (e.g., 51234).
   - Guarantees reliability: if a segment is lost, it retransmits.

3. Internet Layer: Addresses and routes packets across networks.
   - The OS wraps the TCP segment in an IP packet.
   - It adds your server's IP (54.23.189.12) and client's IP.
   - Routers read this layer to move the packet across the web.

4. Network Access Layer: Converts bits to physical signals.
   - Converts the packet to binary frames (0s and 1s).
   - Sends it over the wire (fiber optics, ethernet, radio waves).
```

#### Diagram Explanation (The Delivery Order)
Think of the TCP/IP model visually exactly like ordering food:
- **Application (The Chef):** Prepares the food and puts it on a plate (your raw JSON data).
- **Transport (The Box):** Places the plate in a standard secure delivery box. The box has a label showing the restaurant kitchen port (`:3000`) and the customer's table.
- **Internet (The Driver):** The delivery driver puts the box in their truck. The truck has GPS tracking showing the restaurant's public address (IP) and the customer's home address (IP).
- **Network Access (The Roads):** The actual tires rolling on the physical pavement (Ethernet cables / optical fibers).

---

## Encapsulation (How Data is Built)

```
Each layer wraps the layer above it with its own header:

  [JSON Data]                                                (Application)
  [TCP Header][JSON Data]                                    (Transport - Segment)
  [IP Header][TCP Header][JSON Data]                         (Internet - Packet)
  [Frame Header][IP Header][TCP Header][JSON Data][Trailer]  (Access - Frame)

When the client receives the frame, it performs DE-ENCAPSULATION:
  Peels off Frame header → Peels off IP → Peels off TCP → Hands JSON to React app.
```

---

## Commands & Diagnostics

```bash
# Capture raw network packets (Warning: very verbose!)
# tcpdump operates at Layer 2-4
sudo tcpdump -i any port 3000

# View network statistics
netstat -s
```

---

## Common Mistakes

### ❌ Port Conflicts

```
❌ Error: listen EADDRINUSE: address already in use :::3000
   This is a Transport Layer conflict. Only ONE process can bind to a 
   TCP port on a single IP address at a time.
   
Fix: Kill the zombie Node process (killall -9 node) or change port to 3001.
```

### ❌ Attempting to route by MAC address

```
❌ Try to connect to a server using its MAC address over the internet.
   MAC addresses are Network Access Layer (local link only). Routers strip
   MAC headers at the boundary. You must use IP addresses to route.
```

---

## Practice Exercises

### Exercise 1: tcpdump Packet Analysis
Run a simple Express server. Start `tcpdump` on a separate terminal. Send an HTTP request and capture the headers. Document the TCP flags visible.

### Exercise 2: Port Binding Test
Write a script that attempts to start two independent HTTP servers on port 3000 simultaneously. Capture and print the exact error object returned.

### Exercise 3: Decapsulation Diagram
Draw a step-by-step diagram showing how a standard GET request changes from a raw string in your browser to a frame on the physical network cable.

---

## Interview Q&A

**Q1: What is the difference between the OSI model and the TCP/IP model?**
> The OSI model is a 7-layer conceptual model used for teaching. The TCP/IP model is a 4-layer practical model that corresponds to the actual protocols that run the internet today.

**Q2: What is Encapsulation in networking?**
> The process of wrapping data from an upper layer with headers (and trailers) from a lower layer. As data moves down the stack, each layer adds its own protocol control info.

**Q3: Which layer does a Router operate at?**
> The Internet Layer (IP). Routers inspect the destination IP address of incoming packets to determine the next hop on the path.

**Q4: Which layer does an Express application operate at?**
> The Application Layer. It receives decoded HTTP payloads from the OS kernel and returns application data (JSON, HTML).

**Q5: What is a port and which layer does it belong to?**
> A port is a logical identifier (0-65535) that allows multiple applications to share a single IP address. It belongs to the Transport Layer (TCP/UDP).

---

Prev : [06 OSI Model Vs Real World](./06_OSI_Model_Vs_Real_World.md) | Index: [00 Index](./00_Index.md) | Next : [08 TCP Deep Dive](./08_TCP_Deep_Dive.md)
