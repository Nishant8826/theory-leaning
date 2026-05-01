# 📌 Topic: Load Balancing (AWS ALB)

## 🧠 Concept Explanation
Load Balancing is the process of distributing incoming network traffic across a group of backend servers. An AWS Application Load Balancer (ALB) is a "Layer 7" (Application Layer) device that is smart enough to look inside your HTTP requests and make routing decisions based on what it sees.

**The Traffic Cop Analogy (Deep Dive):**
Imagine a massively popular stadium event (Your Node.js App).
*   **The Cars (Requests):** 50,000 people are trying to enter the stadium at 7 PM.
*   **The Turnstiles (The Servers):** If you only have one turnstile, people will wait for hours (High Latency).
*   **The Load Balancer (The Traffic Cop):** The cop stands at the entrance.
    *   **Distribution:** As each car arrives, he points them to Turnstile 1, then 2, then 3. This is **Round Robin**.
    *   **Health Check:** If the person at Turnstile 4 falls asleep (Server Crash), the cop sees this and stops sending people there until he wakes up.
    *   **Routing:** The cop looks at the tickets. "VIP tickets (Path: `/api/premium`) go to the Luxury Lounge. Regular tickets (Path: `/static`) go to the General Bleachers." This is **Path-based Routing**.
    *   **Security:** The cop checks if the car has a valid permit (SSL/TLS). He handles the paperwork so the turnstiles don't have to. This is **SSL Termination**.

---

## 🏗️ Mental Model
Think of a Load Balancer as a **Reverse Proxy on Steroids**.
1.  **Frontend (The Public Face):** The single IP address or Domain Name that users talk to. It has your SSL certificates.
2.  **Rules (The Brain):** A set of "If-Then" statements. (e.g., "If the host is `api.example.com`, send to Target Group A").
3.  **Target Groups (The Workers):** Clusters of servers that are identical. The ALB doesn't care about "Server A"; it only cares about the "Group."
4.  **Health Checks (The Pulse):** The ALB is constantly "Heartbeating" your servers. If a server stops beating, it's effectively dead to the ALB.

---

## ⚡ Actual Behavior
When an ALB is in place:
1.  **Request Reception:** The client's browser performs a TLS handshake with the ALB. The ALB uses high-performance hardware (AWS Nitro) to decrypt the traffic.
2.  **Header Injection:** The ALB adds important headers like `X-Forwarded-For` (The original user's IP) and `X-Forwarded-Proto` (Was the original request HTTP or HTTPS?). Node.js needs these to know who the user is.
3.  **Connection Management:** The ALB manages "Keep-Alive" connections with the browser. It keeps thousands of sockets open even if the backend servers are busy.
4.  **Target Selection:** The ALB picks a healthy target. It then opens a *new* connection (or reuses a pooled one) to your Node.js instance on its private IP (e.g., `10.0.1.45`).

---

## 🔬 Internal Mechanics (V8 + libuv + OS)
*   **Layer 7 vs. Layer 4:** 
    *   **Layer 4 (NLB):** Only looks at IP and Port. It's fast but "dumb." 
    *   **Layer 7 (ALB):** Understands HTTP. It can look at cookies, headers, and paths. This requires more CPU but allows for much smarter routing.
*   **SSL Termination and V8:** Decrypting TLS is a CPU-intensive operation involving heavy math (Modular Exponentiation). By doing this at the ALB, your Node.js process doesn't have to use its single-threaded Event Loop to handle encryption, freeing up V8 for business logic.
*   **Socket Pooling:** To save time, the ALB doesn't close the connection to your Node.js server after every request. It keeps a "Pool" of open TCP connections. When a new request arrives from a user, the ALB just "grabs" an existing socket and sends the data, skipping the 3-way TCP handshake.
*   **The "Idle Timeout":** Every ALB has a timeout (default 60s). If your Node.js code is doing a heavy calculation and doesn't send a single byte back to the ALB for 61 seconds, the ALB will unilaterally close the connection and send a "504 Gateway Timeout" to the user, even if the Node.js code is still running in the background.
*   **Proxy Protocol:** In some advanced setups, the ALB can use the "Proxy Protocol" to pass the entire TCP connection state to the backend, allowing Node.js to see the raw connection details if needed.

---

## 🔁 Execution Flow
1.  Client makes a request to `api.myapp.com`.
2.  DNS points to the **Application Load Balancer (ALB)**.
3.  ALB terminates the SSL and reads the HTTP headers.
4.  ALB checks its **Rules** (e.g., If path starts with `/api`).
5.  ALB picks a "Healthy" server from the **Target Group**.
6.  ALB forwards the request to that server's IP on port 3000.
7.  Server responds to ALB -> ALB responds to Client.

---

## 🧠 Resource Behavior
*   **Bandwidth:** ALBs can handle millions of requests per second and scale automatically.
*   **Latency:** Adds a tiny overhead (~1-2ms) but significantly improves reliability and scalability.

---

## 📐 ASCII Diagrams
```text
      [ INTERNET ]
           |
   [ APPLICATION LOAD BALANCER ]
      /    |    \
 [Target] [Target] [Target]
 (Node A) (Node B) (Node C)
    |        |        |
    +---[ DATABASE ]--+
```

---

## 🔍 Code Example (Latest Node.js - Health Check Endpoint)
```javascript
import express from 'express';
const app = express();

// A simple health check for the ALB
app.get('/health', (req, res) => {
    // You can also check DB connectivity here
    const isDbHealthy = checkDb(); 
    
    if (isDbHealthy) {
        res.status(200).send('Healthy');
    } else {
        res.status(503).send('Unhealthy');
    }
});

app.listen(3000);
```

---

## 💥 Production Failures
*   **Unhealthy Targets:** All servers failing health checks at once, causing a total blackout. (Solution: Increase the "Health Check Interval" or "Unhealthy Threshold" to avoid premature removal).
*   **Security Group Misconfiguration:** The Load Balancer can't talk to the servers because the server's firewall (Security Group) only allows traffic from "Your IP," not the "ALB's Security Group."

---

## 🧪 Real-time Scenarios
*   **Zero-Downtime Deployment:** Adding a new version of the app to the Target Group, waiting for it to pass health checks, and then removing the old version.
*   **DDoS Protection:** Using AWS WAF (Web Application Firewall) on top of the ALB to block malicious traffic before it reaches your Node.js servers.

---

## ⚠️ Edge Cases
*   **WebSockets:** Standard ALBs support WebSockets, but you must enable "Sticky Sessions" or use a shared state (Redis) to ensure the client stays connected correctly.
*   **Long-running Requests:** If your ALB timeout is 60s and your report generation takes 90s, the connection will be cut off.

---

## 🏢 Best Practices
1.  **Trust Proxy:** Set `app.set('trust proxy', true)` in Express so that `req.ip` shows the user's IP, not the ALB's IP.
2.  **Use Target Group Port 80:** Since SSL is terminated at the ALB, your internal traffic can be plain HTTP to save CPU.
3.  **Cross-Zone Load Balancing:** Ensure the ALB distributes traffic across multiple AWS Availability Zones for maximum reliability.

---

## ⚖️ Trade-offs
*   **ALB (Layer 7):** Smart, understands HTTP/HTTPS, can do path routing. Great for web apps.
*   **NLB (Network Load Balancer - Layer 4):** Faster, handles raw TCP/UDP, millions of RPS. Great for WebSockets and gaming.

---

## 💼 Interview Q&A
*   **Q:** What is "SSL Termination" and why do we do it at the Load Balancer?
*   **A:** It's the process of decrypting SSL/TLS traffic at the load balancer. We do it to reduce the CPU load on our backend servers and to centralize certificate management.

---

## 🧩 Practice Problems
1.  Draw a diagram showing how an ALB routes traffic to different target groups based on the URL path.
2.  Research the difference between "Application," "Network," and "Classic" Load Balancers in AWS.

---
Prev: [03_Containerized_NodeJS.md](./03_Containerized_NodeJS.md) | Index: [NodeJS/00_Index.md](../00_Index.md) | Next: [05_Scaling_on_AWS.md](./05_Scaling_on_AWS.md)
