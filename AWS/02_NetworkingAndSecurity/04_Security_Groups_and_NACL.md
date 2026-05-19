# Security Groups and NACL

## What Is This Service?
- **Security Groups (SGs)**: Stateful virtual firewalls operating at the **instance/resource level** (e.g., attached to an EC2 instance or RDS database).
- **Network Access Control Lists (NACLs)**: Stateless virtual firewalls operating at the **subnet level**.

## Why This Service Exists
Even if you place your servers in a VPC, you need strict rules defining exactly what traffic is allowed to enter or leave your servers. Security Groups and NACLs provide defense-in-depth, ensuring that only expected traffic (like HTTP/HTTPS or MongoDB connections) can flow through your application architecture.

## Real World Analogy
- **NACL (Subnet Level)**: The **security guard at the front gate** of the apartment complex. They check IDs when you enter AND when you leave (Stateless).
- **Security Group (Instance Level)**: The **deadbolt on your specific apartment door**. Once you let a friend inside, they are automatically allowed to walk back out without unlocking the door again (Stateful).

## How It Works
When a request from a user hits your VPC:
1. It first encounters the **NACL** associated with the subnet. The NACL evaluates its numbered rules (from lowest to highest). If allowed, traffic enters the subnet.
2. It then encounters the **Security Group** attached to the specific EC2 instance or Load Balancer. If the SG has an Inbound rule allowing the port, the traffic reaches the server.
3. **Statefulness**: Because SGs are stateful, if an incoming request is allowed, the outbound response is automatically allowed, regardless of Outbound rules. NACLs are stateless, so you must explicitly allow both inbound and outbound traffic.

## Core Concepts
- **Default Deny**: SGs implicitly deny all inbound traffic by default.
- **SG Chaining**: Instead of whitelisting IP addresses, you can configure an SG to allow traffic *only* from another SG (e.g., Database SG only allows traffic from Node.js SG).
- **Ephemeral Ports**: When dealing with NACLs, returning outbound traffic uses random high-number ports (1024-65535) which must be explicitly opened.

## MERN Stack Integration
The ultimate security configuration for MERN:
1. **Load Balancer SG**: Allow Inbound HTTP (80) & HTTPS (443) from `0.0.0.0/0` (the world).
2. **Next.js/Express App SG**: Allow Inbound Custom TCP (e.g., port 3000 or 5000) ONLY from the `Load Balancer SG`.
3. **MongoDB SG**: Allow Inbound Custom TCP (27017) ONLY from the `Express App SG`.

## Production Impact
- **Absolute Isolation**: By using SG chaining, even if a hacker breaches your VPC, they cannot query your database because the Database SG instantly drops any connection that doesn't originate from the exact Node.js Security Group.

## Real Production Use Cases
- A DDoS attack attempts to flood an Express server on SSH port 22. The Security Group drops the packets at the hypervisor level before they ever consume CPU cycles on the Node.js server.

## Production Best Practices
- **Never use `0.0.0.0/0` for databases or backend servers.**
- **Group by Function**: Create distinct SGs for `Web-Tier`, `App-Tier`, and `Data-Tier`.
- **Rely on SGs, ignore NACLs**: For 95% of MERN applications, the default NACL (Allow All) is fine. Manage all your security logic purely through Security Groups.

## Security Best Practices
- Remove SSH (Port 22) access from your Security Groups. In modern AWS, use AWS Systems Manager Session Manager to access servers securely without opening inbound ports.
- Regularly audit SGs for overly permissive rules using AWS Config or Security Hub.

## Cost Optimization Tips
- Security Groups and NACLs are completely free to create and use. There is no limit to the amount of security you can apply.

## Common Mistakes
- **The "It's Not Working" Hack**: A developer gets frustrated that their Node app cannot connect to MongoDB, so they change the Database SG Inbound rule to `0.0.0.0/0` (Allow from anywhere). **This is how companies end up in the news for data breaches.**
- Trying to whitelist dynamic IP addresses instead of using SG chaining.

## Debugging & Troubleshooting
- **Connection Timed Out**: If a request hangs indefinitely and eventually times out, it is almost 100% a Security Group issue (traffic was dropped silently).
- **Connection Refused**: If a request fails instantly, the Security Group allowed the traffic, but the application (e.g., Express or MongoDB) is either not running or listening on the wrong port.

---
Prev : [./03_Internet_and_NAT_Gateway.md](./03_Internet_and_NAT_Gateway.md) | Index : [../00_Index.md](../00_Index.md) | Next : [./05_IAM_Deep_Dive.md](./05_IAM_Deep_Dive.md)
---
