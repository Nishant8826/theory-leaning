# 🌐 ELB / ALB / NLB Internals

## 📌 Topic Name
Elastic Load Balancing: ALB vs. NLB Architecture

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: A load balancer distributes incoming traffic across multiple servers.
*   **Expert**: AWS Elastic Load Balancing is a **Scalable, Managed Proxy Service**. It consists of **Application Load Balancers (ALB)** which operate at Layer 7 (HTTP/S) and **Network Load Balancers (NLB)** which operate at Layer 4 (TCP/UDP/TLS). ELB is a distributed system that lives in multiple AZs and automatically scales its capacity based on traffic patterns.

## 🏗️ Mental Model
- **ALB (L7)**: A **Smart Concierge**. It reads the guest's ticket (URL/Header) and directs them to the specific room (Target Group) they need (e.g., `/images` goes to the Image Service).
- **NLB (L4)**: A **High-Speed Tunnel**. It doesn't look at the data; it just shoves packets through as fast as possible based on the IP address and Port.

## ⚡ Actual Behavior
- **DNS-based**: Load Balancers provide a DNS name, not a single IP address (except for NLB which can have Static IPs). The DNS resolves to multiple IP addresses (one per AZ).
- **Scaling**: As traffic increases, AWS adds more load balancer nodes behind that DNS name.
- **Cross-Zone Load Balancing**: Allows a load balancer node in AZ-1 to send traffic to an instance in AZ-2.

## 🔬 Internal Mechanics
1.  **ALB Nodes**: These are essentially managed fleets of Nginx or similar proxies. They perform TLS termination and header processing.
2.  **NLB (Hyperplane)**: NLB is built on the **AWS Hyperplane**—a massive, horizontally scaled state management system that handles millions of connections with ultra-low latency. It uses one Static IP per AZ.
3.  **Connection Tracking**: NLB is "flow-based." It remembers which backend instance a TCP flow belongs to. ALB is "request-based."

## 🔁 Execution Flow (ALB HTTP Request)
1.  **DNS**: Client resolves `lb-123.us-east-1.elb.amazonaws.com`.
2.  **TCP/TLS**: Client establishes connection to one of the ALB's IP addresses.
3.  **Request**: Client sends `GET /api/users`.
4.  **Routing**: ALB evaluates Listener Rules (e.g., Path `/api/*` -> TargetGroup `api-tg`).
5.  **Forwarding**: ALB selects an instance in `api-tg` using **Least Outstanding Requests** or **Round Robin**.
6.  **Response**: Instance responds to ALB; ALB responds to Client.

## 🧠 Resource Behavior
- **Target Groups**: Logical groups of EC2s, Lambdas, or IP addresses.
- **Health Checks**: ELB periodically pings targets. If a target fails, it is removed from the rotation.

## 📐 ASCII Diagrams
```text
[ CLIENT ] --(DNS: lb.com)--> [ Route 53 ]
      |
      V
[ ALB NODE (AZ-1) ] <----(Cross-Zone)----> [ TARGET 2 (AZ-2) ]
      |                                           ^
      +-------------------------------------------+
      |
[ TARGET 1 (AZ-1) ]
```

## 🔍 Code / IaC (Terraform)
```hcl
# Application Load Balancer
resource "aws_lb" "web_alb" {
  name               = "web-alb"
  internal           = false
  load_balancer_type = "application"
  subnets            = [aws_subnet.public_a.id, aws_subnet.public_b.id]
}

# Listener with Path-based Routing
resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.web_alb.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.default.arn
  }
}

resource "aws_lb_listener_rule" "api" {
  listener_arn = aws_lb_listener.http.arn
  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.api.arn
  }
  condition {
    path_pattern {
      values = ["/api/*"]
    }
  }
}
```

## 💥 Production Failures
1.  **ALB 504 Gateway Timeout**: The backend instance took too long to respond. Often caused by slow DB queries or thread pool exhaustion in the app.
2.  **NLB Port Exhaustion**: An NLB talking to a single backend instance can run out of ephemeral ports if there are millions of simultaneous connections.
3.  **Nodes Out of Sync**: ALB scales out by adding new IPs. If a client's DNS resolver caches an old IP for too long (ignoring the 60s TTL), they will try to connect to a deleted ALB node and get a timeout.

## 🧪 Real-time Q&A
*   **Q**: When should I use NLB over ALB?
*   **A**: Use NLB for ultra-low latency, non-HTTP protocols, or when you need a **Static/Elastic IP** for whitelisting. Use ALB for everything else (WAF integration, Path routing, OIDC).
*   **Q**: Does ELB support WebSockets?
*   **A**: Yes, both ALB and NLB support WebSockets.

## ⚠️ Edge Cases
*   **Pre-warming**: If you expect a massive traffic spike (e.g., a flash sale), you must contact AWS to "pre-warm" your ALB so it can handle the load from second one.
*   **Sticky Sessions**: Allows an ALB to bind a user's session to a specific backend instance using cookies. Use with caution as it can cause uneven load.

## 🏢 Best Practices
1.  **Use Target Group Health Checks**: Ensure they are testing a valid "health" endpoint, not just `/`.
2.  **Enable Access Logs**: Crucial for debugging performance issues and identifying malicious traffic.
3.  **Security Groups**: The LB's SG should allow inbound traffic from the internet, and the Instance's SG should ONLY allow inbound traffic from the LB's SG.

## ⚖️ Trade-offs
*   **ALB**: Rich feature set (WAF, SSL, Routing) but higher latency (~ms).
*   **NLB**: Extreme performance (millions of RPS) and low latency (~μs) but limited routing features.

## 💼 Interview Q&A
*   **Q**: How does an ALB handle a failing instance?
*   **A**: It uses health checks (e.g., an HTTP GET to `/health`). If the instance fails X consecutive checks, the ALB marks it as "unhealthy" and stops sending traffic to it. It continues to probe, and if the instance passes Y consecutive checks, it is added back to the pool.

## 🧩 Practice Problems
1.  Configure an ALB to perform a "Fixed Response" (e.g., 503 Maintenance) for a specific header.
2.  Set up an NLB with an Elastic IP and verify that the IP stays consistent even after a mock failure.

---
Prev: [06_Read_Replicas_and_Failover.md](../Databases/06_Read_Replicas_and_Failover.md) | Index: [Docker/00_Index.md](../00_Index.md) | Next: [02_DNS_Route53.md](../Networking/02_DNS_Route53.md)
---
