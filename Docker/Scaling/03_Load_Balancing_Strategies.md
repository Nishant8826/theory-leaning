# 📌 Topic: Load Balancing Strategies (L4 vs L7)

## 🧠 Concept Explanation (Basic → Expert)
**Basic**: A Load Balancer is a traffic cop. It stands in front of your containers and tells each incoming request which container to go to. This ensures no single container is overwhelmed.
**Expert**: Load Balancing exists at different layers of the OSI model. **L4 (Transport)** balancing works with IP addresses and TCP ports; it's fast but "blind" to the application data. **L7 (Application)** balancing works with HTTP headers, cookies, and URLs; it's slower but "intelligent." Staff-level engineering requires choosing the right layer based on the protocol (gRPC vs HTTP) and the need for features like **SSL Termination**, **Path-based Routing**, and **Header Manipulation**.

## 🏗️ Mental Model
- **L4 (The Mail Sorter)**: Reads the address on the envelope (IP/Port) and puts it in the correct bin. They don't open the envelope.
- **L7 (The Secretary)**: Opens the envelope, reads the letter (HTTP Request), and decides who should see it based on what the letter says (e.g., "If it's a bill, send to Accounting; if it's a resume, send to HR").

## ⚡ Actual Behavior
- **L4 (TCP)**: Once a connection is established, all data in that connection goes to the same container. This is extremely high-performance.
- **L7 (HTTP)**: The balancer can send different requests from the SAME user to DIFFERENT containers based on the URL (e.g., `/api` goes to one group, `/static` goes to another).

## 🔬 Internal Mechanics (The Hops)
1. **L4 Balancing (IPVS/NLB)**:
   - Uses DNAT to change the packet's destination.
   - Operates at the kernel level.
   - Supports any TCP/UDP protocol.
2. **L7 Balancing (Nginx/ALB)**:
   - Terminates the TCP connection from the client.
   - Opens a NEW TCP connection to the container.
   - Can inspect and modify HTTP headers (e.g., adding `X-Forwarded-For`).

## 🔁 Execution Flow (L7 Path Routing)
1. Request: `GET /v1/orders`.
2. L7 Balancer: Parses the path `/v1/orders`.
3. Rule Check: "Path /v1/* goes to the 'Orders-Service' group."
4. Selection: Picks a healthy container from the 'Orders-Service'.
5. Forward: Sends the request and waits for the response.

## 🧠 Resource Behavior
- **CPU**: L7 balancing is CPU-intensive due to TLS decryption and string parsing.
- **Latency**: L4 adds microseconds; L7 adds milliseconds (due to the double TCP handshake).

## 📐 ASCII Diagrams (REQUIRED)

```text
       L4 vs L7 LOAD BALANCING
       
   [ CLIENT ]              [ CLIENT ]
       |                       |
 ( TCP Handshake )       ( HTTP GET /api )
       |                       |
 [ L4 BALANCER ]         [ L7 BALANCER ]
 ( Packet Level )        ( Request Level )
       |                       |
+------+------+         +------+------+
|             |         |             |
[ APP A ]  [ APP B ]   [ API ]    [ AUTH ]
 (Same App)             (Split by Path)
```

## 🔍 Code (Nginx L7 Path-based Routing)
```nginx
http {
    upstream orders_api {
        server orders-container:3000;
    }
    upstream users_api {
        server users-container:3001;
    }

    server {
        listen 80;

        location /orders {
            proxy_pass http://orders_api;
        }

        location /users {
            proxy_pass http://users_api;
        }
    }
}
```

## 💥 Production Failures
- **The "Zombie Connection" (L4)**: A client opens a long-lived TCP connection to an L4 balancer. Even if you add 10 new containers, the L4 balancer keeps sending all traffic from that specific client to the original container.
  *Fix*: Use L7 balancing for long-lived protocols or implement client-side load balancing.
- **The "Header Size" Error**: A client sends a very large cookie or header. The L7 balancer has a limit (e.g., 4KB) and rejects the request before it even reaches your container.
  *Fix*: Increase `large_client_header_buffers` in Nginx.

## 🧪 Real-time Q&A
**Q: Which one should I use for my Docker cluster?**
**A**: Use **L7** (ALB/Nginx/Traefik) for your web applications so you can handle SSL, redirects, and path routing. Use **L4** (NLB) in front of your L7 balancers or for high-performance non-HTTP services (like a database or a game server).

## ⚠️ Edge Cases
- **gRPC Load Balancing**: gRPC uses HTTP/2, which multiplexes many requests over one TCP connection. A standard L4 balancer will send ALL gRPC traffic to one container. You **MUST** use an L7 balancer that understands gRPC (like Envoy or Nginx 1.13+) to balance it properly.

## 🏢 Best Practices
- **Health Checks**: Always configure active health checks (e.g., a `/health` endpoint).
- **SSL Offloading**: Terminate SSL at the Load Balancer to save container CPU.
- **Sticky Sessions**: Only use them if absolutely necessary; they make horizontal scaling much harder.

## ⚖️ Trade-offs
| Feature | L4 (Transport) | L7 (Application) |
| :--- | :--- | :--- |
| **Speed** | **Fastest** | Slower |
| **Intelligence** | Low | **High** |
| **Protocol Support**| Any TCP/UDP | HTTP / gRPC / WebSocket |
| **SSL Handling** | Pass-through | **Termination** |

## 💼 Interview Q&A
**Q: Why is L7 load balancing necessary for a Microservices architecture?**
**A**: L7 balancing is essential because it allows for **Service Decomposition**. In a microservices environment, different parts of the application (e.g., `/orders`, `/users`, `/payments`) are handled by different sets of containers. An L4 balancer only sees IP addresses and ports and cannot distinguish between these different URLs. An L7 balancer can inspect the HTTP path and route the request to the correct microservice, providing a unified "Gateway" for the entire system while allowing the underlying services to scale and evolve independently.

## 🧩 Practice Problems
1. Set up an Nginx container that balances traffic between two "Hello World" containers.
2. Use `curl -v` to see the `X-Forwarded-For` header added by the balancer.
3. Compare the behavior of a Round Robin vs a Least Connections algorithm using a load testing tool like `wrk`.

---
Prev: [02_Auto_scaling_Mechanisms.md](./02_Auto_scaling_Mechanisms.md) | Index: [00_Index.md](../00_Index.md) | Next: [04_Global_Traffic_Management.md](./04_Global_Traffic_Management.md)
---
