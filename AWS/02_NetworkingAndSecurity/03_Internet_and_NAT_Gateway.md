# Internet and NAT Gateway

## What Is This Service?
- **Internet Gateway (IGW)**: A highly available AWS component that allows communication between your VPC and the internet.
- **NAT Gateway (Network Address Translation)**: A service that allows instances in a *Private Subnet* to connect to the internet (e.g., to download updates or NPM packages) but prevents the internet from initiating a connection with those instances.

## Why This Service Exists
A VPC is completely isolated by default. If your Load Balancer needs to receive user traffic, it needs an IGW.
However, your private Node.js servers need to download libraries (`npm install`) or communicate with external APIs (like Stripe or SendGrid). If they are in a Private Subnet, they have no public IP and no IGW access. A NAT Gateway solves this by acting as a one-way secure middleman.

## Real World Analogy
- **Internet Gateway**: The **Main Front Door** of a building. People can walk in from the street, and employees can walk out.
- **NAT Gateway**: A **Secure Mailroom**. Employees inside the secure bunker (Private Subnet) hand their outgoing letters (API requests) to the mail clerk (NAT Gateway). The mail clerk goes outside, sends the letter, receives the reply, and brings it back down to the bunker. No one from the outside is ever allowed to walk into the bunker.

## How It Works
1. You attach an **IGW** to your VPC. You update the Public Route Table to send `0.0.0.0/0` traffic to the IGW.
2. You place a **NAT Gateway** inside a *Public Subnet* (it needs an Elastic IP address to reach the internet).
3. You update the Private Route Table to send `0.0.0.0/0` traffic to the NAT Gateway.
4. When a private Node.js server makes an API call, the traffic goes to the NAT Gateway, which swaps the private IP for its public IP, hits the internet, and returns the response.

## Core Concepts
- **Elastic IP (EIP)**: A static, public IPv4 address. NAT Gateways require an EIP to function.
- **One-Way Traffic**: NAT Gateways only allow outbound-initiated traffic. Inbound-initiated traffic from the internet is instantly dropped.

## MERN Stack Integration
- Your React/Next.js users hit the Load Balancer (via the IGW).
- The Load Balancer forwards requests to the Express.js server in the Private Subnet.
- The Express.js server needs to charge a credit card via the Stripe API. It sends the request to the NAT Gateway, which securely routes it to Stripe and returns the success payload to Express.

## Production Impact
- **Security**: The NAT Gateway ensures your Node servers are completely invisible to the internet while still retaining the ability to consume third-party SaaS APIs.
- **Maintenance**: Node.js servers can fetch security patches (`apt-get update`) without being exposed to incoming SSH brute-force attacks.

## Real Production Use Cases
- A backend job running on an ECS container in a private subnet fetches the latest exchange rates from a public financial API every hour. The NAT Gateway facilitates this secure outbound request.

## Production Best Practices
- **Multi-AZ NAT Gateways**: For production, deploy one NAT Gateway in *every* Availability Zone. If AZ-A goes down and you only had one NAT Gateway there, the servers in AZ-B will suddenly lose internet access.

## Security Best Practices
- Only route `0.0.0.0/0` to the NAT Gateway in Private Subnets. 
- Ensure your databases (like MongoDB) do not have a route to the NAT Gateway unless they explicitly need to download updates, further reducing exfiltration risks.

## Cost Optimization Tips
- **NAT Gateways are expensive**. They cost an hourly rate (~$0.045/hr = $32/month per NAT) plus data processing fees.
- For non-production/hobby MERN apps, use public subnets (to avoid NAT fees) or run a cheap `t2.micro` EC2 instance configured as a "NAT Instance" instead of using the managed NAT Gateway.

## Common Mistakes
- Putting a NAT Gateway in a Private Subnet. It will not work. A NAT Gateway *must* live in a Public Subnet so it can reach the IGW.
- Forgetting to assign an Elastic IP to the NAT Gateway.

## Debugging & Troubleshooting
- **NPM Install Hanging**: If your CI/CD pipeline or Docker build hangs indefinitely on `npm install` inside a private subnet, 99% of the time your NAT Gateway is misconfigured or missing from the Route Table.

---
Prev : [./02_Subnets_and_Route_Tables.md](./02_Subnets_and_Route_Tables.md) | Index : [../00_Index.md](../00_Index.md) | Next : [./04_Security_Groups_and_NACL.md](./04_Security_Groups_and_NACL.md)
---
