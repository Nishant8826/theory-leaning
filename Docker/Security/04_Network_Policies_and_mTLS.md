# 📌 Topic: Network Policies and mTLS (Zero Trust)

## 🧠 Concept Explanation (Basic → Expert)
**Basic**: Network Policies are like a firewall for your containers. You can say "The Frontend can talk to the API, but it cannot talk to the Database." mTLS (Mutual TLS) makes sure that every container proves its identity before talking to another.
**Expert**: This is the implementation of the **Zero Trust Architecture** in a containerized environment. By default, Docker networks are "Open"—any container on a bridge can talk to any other. Staff-level engineering requires implementing **Micro-segmentation**. You must assume the network is compromised. Every connection must be **Authenticated** (who are you?), **Authorized** (are you allowed to talk to me?), and **Encrypted** (no one can eavesdrop). This is typically achieved using a **Service Mesh** (like Istio or Linkerd) or **CNI Policies** (like Calico).

## 🏗️ Mental Model
- **Open Network**: An open office where everyone can walk into any room and talk to anyone.
- **Zero Trust**: A high-security facility where every door is locked. To walk from one room to another, you must show your badge (Certificate) to a guard who checks a list (Policy) to see if you are allowed in that specific room.

## ⚡ Actual Behavior
- **Docker Bridge (Default)**: If you run `docker run --network my-net`, any other container on `my-net` can hit your open ports.
- **Zero Trust (mTLS)**: Even if a container hits your port, the connection is rejected at the TCP level because the caller doesn't have a valid SSL certificate signed by the internal CA.

## 🔬 Internal Mechanics (The Sidecar Proxy)
1. **The Proxy**: A small container (Envoy) is placed next to your app.
2. **The Interception**: All incoming and outgoing traffic is forced through this proxy.
3. **Handshake**: When App A talks to App B, the two proxies perform a **Mutual TLS Handshake**. They exchange certificates.
4. **Identity**: The certificates contain the **SPIFFE ID** (a universal identity for the service).
5. **Policy**: The proxy checks a central policy (e.g., "Is 'frontend' allowed to call 'payments'?") before allowing the data to flow to the actual app.

## 🔁 Execution Flow
1. Frontend sends request to `payments:8080`.
2. Frontend Sidecar intercepts request.
3. Sidecar initiates TLS with Payments Sidecar.
4. Payments Sidecar verifies Frontend's certificate.
5. Payments Sidecar checks: "Is Frontend allowed to POST to /pay?"
6. If YES, request is passed to the Payments App.
7. Traffic is encrypted with AES-256 in transit.

## 🧠 Resource Behavior
- **CPU**: Encryption/Decryption and certificate verification consume CPU. A Service Mesh typically adds 1-5ms of latency.
- **RAM**: Each sidecar proxy uses 50-100MB of RAM. In a 1,000-container cluster, this adds up to 100GB of "Security Tax."

## 📐 ASCII Diagrams (REQUIRED)

```text
       ZERO TRUST (mTLS) FLOW
       
[ App A ] <--( Localhost )--> [ Proxy A ] 
                                  |
                        ( Encrypted Tunnel )
                        ( Auth + Policy Check )
                                  |
[ App B ] <--( Localhost )--> [ Proxy B ]
```

## 🔍 Code (Nginx as a simple mTLS Proxy)
```nginx
# Server Block for App B
server {
    listen 443 ssl;
    ssl_certificate /etc/certs/server.crt;
    ssl_key         /etc/certs/server.key;
    
    # Enable Mutual TLS
    ssl_client_certificate /etc/certs/ca.crt;
    ssl_verify_client on;

    location / {
        proxy_pass http://localhost:8080;
    }
}
```

## 💥 Production Failures
- **The "Certificate Expiry" Outage**: An internal CA certificate expires. Suddenly, every container in the cluster stops talking to every other container. The entire system goes dark.
  *Fix*: Use an automated system (Cert-Manager or Istio) that rotates certificates every 24 hours.
- **Circular Block**: You set a policy that "Service A needs Service B" and "Service B needs Service A," but forget to allow the "Health Check" from the Load Balancer. Both services are marked as "Dead" and are killed.

## 🧪 Real-time Q&A
**Q: Do I need mTLS if I am on a private VPC?**
**A**: According to Zero Trust principles, **YES**. A VPC only protects the "Perimeter." If one container is compromised (e.g., via a library vulnerability), the attacker can "sniff" all traffic on that network. mTLS ensures that even an attacker inside your network can't see your data or talk to your services.

## ⚠️ Edge Cases
- **Non-TCP Protocols**: Standard mTLS works for TCP (HTTP/gRPC). For UDP (DNS/Video), you need different strategies like DTLS or IPsec.

## 🏢 Best Practices
- **Default Deny**: Start with a policy that blocks all traffic, then explicitly allow what is needed.
- **Automated Rotation**: Never manage internal certificates manually.
- **Visibility**: Use tools like Kiali or Jaeger to visualize the network traffic and identify unauthorized connection attempts.

## ⚖️ Trade-offs
| Network Security | Performance | Security | Complexity |
| :--- | :--- | :--- | :--- |
| **Open Bridge** | **Highest** | Low | **Lowest** |
| **Basic Firewall**| High | Medium | Medium |
| **Service Mesh (mTLS)**| Medium | **Highest** | High |

## 💼 Interview Q&A
**Q: What is "Micro-segmentation" in a containerized environment?**
**A**: Micro-segmentation is the process of dividing a container network into small, isolated security zones. Instead of one large network where everything can talk to everything, you define granular policies that only allow specific "Service-to-Service" communication paths. For example, the "Reporting" service might be allowed to READ from the "Orders" database, but it is strictly blocked from talking to the "Users" service. This limits the "Blast Radius" of a security breach—if one container is hacked, the attacker cannot move laterally through the rest of the system.

## 🧩 Practice Problems
1. Create two Docker networks. Put a container in each. Try to ping between them.
2. Research "Calico Network Policies" and see how they use IPTables to block traffic between containers on the same host.
3. Set up a simple mTLS handshake between two `curl` commands using self-signed certificates.

---
Prev: [03_Scanning_Images_Trivy.md](./03_Scanning_Images_Trivy.md) | Index: [00_Index.md](../00_Index.md) | Next: [05_Runtime_Security_Falco.md](./05_Runtime_Security_Falco.md)
---
