# Load Balancer

## Why This Exists
If you run an app on a single server, a crash takes your whole business offline. The solution is to run the app on 3 servers. But how do users know which IP address to visit? What happens if Server #2 crashes? An Elastic Load Balancer (ELB) acts as a single, highly-available front door that evenly distributes incoming traffic to healthy backend servers.

## Real World Analogy
Think of a **Bank Teller Line**. 
In a bad bank, there are 3 separate lines for 3 tellers. If the person at the front of your line is depositing 10,000 pennies, you are stuck, while the other lines move fast.
A Load Balancer is the **Manager** standing at the front of one single mega-line. When a customer walks in, the Manager looks at the tellers, sees who is free and healthy, and directs the customer to that specific teller.

## Core Concepts
*   **ALB (Application Load Balancer):** Smart. Operates at Layer 7 (HTTP/HTTPS). It can look at the URL (`/api` vs `/images`) and route traffic to different servers based on the path.
*   **NLB (Network Load Balancer):** Fast. Operates at Layer 4 (TCP/UDP). It doesn't care about HTTP; it just blasts packets to servers at millions of requests per second. Useful for gaming servers or databases.
*   **Target Group:** The logical grouping of your backend servers (EC2 instances or EKS Pods).
*   **Health Checks:** The ELB constantly pings the servers (e.g., hitting `/health`). If a server fails the check, the ELB stops sending it traffic.

## Architecture / Flow
1. User types `myapp.com` and hits the **Load Balancer**.
2. The Load Balancer checks its **Listeners** (e.g., "If traffic is on Port 80...").
3. The Listener rules say "Forward to the Web **Target Group**".
4. The Target Group contains 3 EC2 instances. The ELB picks one (using a Round Robin algorithm) and sends the request.
5. The EC2 instance replies to the ELB, which replies to the User.

## Practical Commands
*   *(ELBs are almost exclusively managed via the AWS Web Console or Infrastructure as Code like Terraform. CLI commands are too verbose to be practical).*
*   If using EKS: applying an `Ingress` YAML automatically provisions an ALB!

## Hands-On Exercise
Spin up two EC2 instances. SSH in and put a simple `index.html` on each (one saying "Server A", the other "Server B"). Create a Target Group with both instances. Create an Application Load Balancer pointing to that Target Group. Copy the ALB's DNS name into your browser and refresh repeatedly. Watch the text bounce between A and B!

## Mini Project
**"Path-Based Routing"**
Create two Target Groups: `TG-Web` and `TG-API`. Configure an ALB with a Listener Rule: If the URL path starts with `/api/*`, forward to `TG-API`. Otherwise, forward to `TG-Web`.

## Real Production Usage
Load Balancers are the unsung heroes of the internet. They allow companies to perform "Zero Downtime Deployments". You add new Version 2 servers to the Target Group, wait for them to pass Health Checks, and then slowly remove the Version 1 servers. The user never notices a blip.

## Common Mistakes
*   **Security Group Misconfiguration:** The EC2 instances should *never* accept HTTP traffic from the open internet (0.0.0.0/0). Their Security Groups should only allow HTTP traffic coming *from* the Load Balancer's Security Group.
*   **Failing Health Checks:** If your app takes 2 minutes to boot up, but your ELB health check requires a response in 10 seconds, the ELB will assume the server is dead and constantly reboot it.

## Debugging Guide
*   **Getting a "502 Bad Gateway"?** This means the Load Balancer received the user's request, but when it tried to talk to the backend EC2 server, the server either didn't respond or threw an error. Check your EC2 app logs.
*   **Instances "Unhealthy"?** Check the path the ELB is pinging (e.g., `/`). Ensure your web server actually returns an HTTP 200 OK status code for that path.

## Best Practices
*   **SSL Termination:** Do not install SSL certificates on your EC2 instances. Install the certificate on the ALB. Let the ALB handle the heavy math of encrypting/decrypting HTTPS traffic, and send unencrypted HTTP to the backend EC2s within the safe AWS network.

## Interview Questions
*   **Q: When would you choose an NLB over an ALB?**
    *   *A: When I need extreme performance (millions of requests/sec) with ultra-low latency, or when my application uses non-HTTP protocols like raw TCP (e.g., a multiplayer game server).*

## Summary
Elastic Load Balancers decouple the incoming traffic from your backend servers, providing the high availability, security, and flexibility required for any production-grade architecture.

---
Prev: [03_eks.md](./03_eks.md) | Index: [Index](../00_index.md) | Next: [05_route53.md](./05_route53.md)
