# TCP Deep Dive

> 📌 **File:** 08_TCP_Deep_Dive.md | **Level:** Full-Stack Dev → Networking Expert

---

## What is it?

TCP (Transmission Control Protocol) is the reliable transport protocol at Layer 4. Every HTTP request, database connection, and API call runs over a TCP connection. TCP guarantees three things: packets arrive, they arrive in order, and they aren't damaged. It does this through connection states, handshakes, sequence numbers, and window sizing.

---

## Map it to MY STACK (CRITICAL)

```
Your Node.js API:
  const app = require('express')();
  app.listen(3000);  // Creates a TCP socket listening on port 3000

When a browser connects:
  1. Browser OS initiates TCP Handshake with Server OS.
  2. Handshake completes in OS kernel (Node.js doesn't see this yet).
  3. Server OS puts connection in "Accept Queue".
  4. Node.js event loop calls "accept()" -> grabs connection.
  5. Your Express routes can now receive HTTP data over this TCP pipe.

If Node.js event loop is blocked:
  - OS still completes TCP handshakes (up to "backlog" limit).
  - But Node.js doesn't call accept(). Accept queue fills up.
  - New clients get "connection refused" or timeouts, even though
    the server process is running!
```

---

## TCP Connection Lifecycle

```
┌──────────────────────────────────────────────────────────────────┐
│  TCP Three-Way Handshake (Establishing connection)               │
│                                                                  │
│  Client (Browser)                      Server (Node.js)          │
│    │                                          │                  │
│    │  SYN (Synchronize)                       │                  │
│    │  Seq=X                                   │                  │
│    │ ───────────────────────────────────────► │                  │
│    │                                          │                  │
│    │  SYN-ACK (Sync-Acknowledge)              │                  │
│    │  Seq=Y, Ack=X+1                          │                  │
│    │ ◄─────────────────────────────────────── │                  │
│    │                                          │                  │
│    │  ACK (Acknowledge)                       │                  │
│    │  Seq=X+1, Ack=Y+1                        │                  │
│    │ ───────────────────────────────────────► │                  │
│    │                                          │                  │
│    ═══ Connection ESTABLISHED (Data can flow) ═══                │
└──────────────────────────────────────────────────────────────────┘
```

#### Diagram Explanation (The Phone Call)
Think of the 3-way handshake exactly like starting a phone call:
- **SYN (Client):** "Hello? Can you hear me?" (Sends initial Sequence number X).
- **SYN-ACK (Server):** "Yes, I hear you! Can you hear me?" (Acknowledges client, sends own Sequence Y).
- **ACK (Client):** "Yep, I can hear you clearly! Let's talk." (Connection established).

```
┌──────────────────────────────────────────────────────────────────┐
│  TCP Four-Way Teardown (Closing connection)                      │
│                                                                  │
│  Client                                Server                    │
│    │                                          │                  │
│    │  FIN (Finished)                          │                  │
│    │ ───────────────────────────────────────► │                  │
│    │                                          │                  │
│    │  ACK                                     │                  │
│    │ ◄─────────────────────────────────────── │                  │
│    │                                          │ (Server finishes │
│    │                                          │  sending data)   │
│    │  FIN                                     │                  │
│    │ ◄─────────────────────────────────────── │                  │
│    │                                          │                  │
│    │  ACK                                     │                  │
│    │ ───────────────────────────────────────► │                  │
│    │                                          │                  │
│    │  (Client enters TIME_WAIT: 2MSL)         │                  │
│    ═══ Socket closed (Resources freed) ══════                 │
└──────────────────────────────────────────────────────────────────┘
```

#### Diagram Explanation (Saying Goodbye)
Closing a TCP connection is like two polite people saying goodbye:
- **FIN (Client):** "I'm done speaking, I have nothing more to say."
- **ACK (Server):** "Got it. Let me finish my sentence..." (Server keeps sending trailing data).
- **FIN (Server):** "Okay, I'm also done speaking now. Goodbye."
- **ACK (Client):** "Goodbye!" (Client enters `TIME_WAIT` state to catch any late packets).

---

## Important TCP States to Monitor

```
┌──────────────────────────────────────────────────────────────────┐
│  State       │ What it Means              │ Production Impact    │
├──────────────┼────────────────────────────┼──────────────────────┤
│  LISTEN      │ Server is waiting for      │ Normal state for     │
│              │ connections on port X      │ Node.js/DB           │
│              │                            │                      │
│  ESTABLISHED │ Active connection, data    │ Normal active        │
│              │ flowing                    │ traffic              │
│              │                            │                      │
│  TIME_WAIT   │ Connection closed by client│ Normal, socket held  │
│              │ Waiting for late packets   │ for 60-120 seconds   │
│              │                            │                      │
│  CLOSE_WAIT  │ Connection closed by server│ DANGER! Server forgot│
│              │ Client waiting for server  │ to call socket.close()│
│              │ to close its end           │ Memory/socket leak   │
└──────────────┴────────────────────────────┴──────────────────────┘

DANGER: Too many TIME_WAIT connections can exhaust server ports!
Each port is a resource. If you have 65,000 connections in TIME_WAIT,
new connections fail with "cannot assign requested address".
Fix: Enable TCP keep-alive, reuse connections.
```

---

## Node.js Implementation

```javascript
const net = require('net');

// ──── Low-Level TCP Server ────
const server = net.createServer((socket) => {
  console.log(`Client connected: ${socket.remoteAddress}:${socket.remotePort}`);
  
  // Keep connection alive
  socket.setKeepAlive(true, 60000); // 60s idle timeout
  
  socket.on('data', (data) => {
    console.log(`Received: ${data.length} bytes`);
    
    // Echo back (Simple protocol)
    socket.write(`Echo: ${data}`);
  });
  
  socket.on('close', () => {
    console.log('Client disconnected');
  });
  
  socket.on('error', (err) => {
    console.error('Socket error:', err);
  });
});

// Listen on TCP port 3000
server.listen(3000, '0.0.0.0', () => {
  console.log('TCP server listening on port 3000');
});

// ──── Low-Level TCP Client ────
const client = new net.Socket();

client.connect(3000, 'localhost', () => {
  console.log('Connected to server');
  client.write('Hello, Server!');
});

client.on('data', (data) => {
  console.log(`Server says: ${data}`);
  client.destroy(); // Kill connection
});
```

---

## Commands & Diagnostics

```bash
# View all listening and established TCP connections
ss -t -a                       # Modern Linux (fast)
netstat -tna                   # Legacy (works on Mac)
netstat -ano                   # Windows PowerShell

# Count connections by state
ss -t -a | awk '{print $1}' | sort | uniq -c

# Check what process is listening on port 3000
lsof -i :3000                  # Mac/Linux
ss -tlpn | grep :3000          # Linux only (requires root)
netstat -ano | findstr 3000    # Windows

# Connect to raw TCP port to test connection (replaces curl for raw ports)
nc -zv api.myapp.com 3000      # Netcat test: check if port is open
telnet localhost 3000          # Telnet test (exit with Ctrl+])
```

---

## Common Mistakes

### ❌ Node.js Event Loop Blocked

```
Node.js runs on a single thread.
If you run a heavy CPU task (like parsing 50MB JSON):
  - Event loop blocks.
  - OS queue fills up with completed TCP handshakes.
  - Clients get connection timeouts.
  - To the user: server looks completely dead.
  
Fix: Never block the event loop. Move heavy computation to worker threads.
```

### ❌ CLOSE_WAIT accumulation (Socket leak)

```
Your code receives a connection, but fails to close it on error.
The database socket stays open forever.
Over time: CLOSE_WAIT count rises. Server runs out of file descriptors.
Then: "EMFILE: too many open files" error -> server crashes.

Fix: Always close sockets in try...finally or use auto-closing pools.
```

---

## Practice Exercises

### Exercise 1: Port Scanner
Write a Node.js script that attempts to open a TCP connection to ports 80, 443, 3000, and 27017 on `localhost`. Print which are open and closed.

### Exercise 2: State Tracking
Start your Node app. Run `ss -t -a` and identify the state of the socket listening on port 3000. Connect via browser and run the command again. Locate the active client connection.

### Exercise 3: Netcat Server
Run `nc -l 3000` (starts a simple TCP listener in terminal). Send a message from a second terminal using `nc localhost 3000`. Observe the output.

---

## Interview Q&A

**Q1: Walk me through the TCP 3-way handshake.**
> Client sends SYN (sync) packet. Server responds with SYN-ACK (sync-ack). Client responds with ACK (ack). Connection is now established.

**Q2: What is the TIME_WAIT state and why is it necessary?**
> The state a socket enters after closing a connection. It lasts 1-2 minutes. It prevents late, delayed packets from a previous connection from being confused with data on a new connection using the same port.

**Q3: How do you identify a socket leak on a production server?**
> Run `ss -t -a` and check the count of sockets in `CLOSE_WAIT` state. If this count is continuously rising and never drops, you have a socket leak (app is not closing sockets).

**Q4: What happens if the Node.js accept queue is full?**
> The OS kernel continues to complete TCP handshakes up to the backlog limit. Once the limit is reached, the OS starts dropping new SYN packets, causing clients to experience connection timeouts.

**Q5: What is TCP Keep-Alive and why is it important for cloud databases?**
> A mechanism that sends periodic empty packets to verify the connection is still alive. Necessary because cloud firewalls (like AWS NAT Gateways) silently drop idle TCP connections after 350 seconds. Keep-Alive prevents this by keeping the channel active.

---

Prev : [07 HTTP HTTPS Internals](./07_HTTP_HTTPS_Internals.md) | Index: [00 Index](./00_Index.md) | Next : [09 UDP And When To Use It](./09_UDP_And_When_To_Use_It.md)
