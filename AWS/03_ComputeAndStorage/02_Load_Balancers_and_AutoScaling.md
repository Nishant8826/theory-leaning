# Load Balancers and Auto Scaling

## What Is This Service?
- **Elastic Load Balancer (ELB)**: Specifically the Application Load Balancer (ALB). It automatically distributes incoming HTTP/HTTPS traffic across multiple targets (like EC2 instances or ECS containers).
- **Auto Scaling Groups (ASG)**: Automatically increases or decreases the number of compute instances based on traffic or CPU demand.

## Why This Service Exists
A single Express server will eventually crash under heavy traffic. If it crashes, your MERN app goes offline. The ALB ensures traffic is only sent to healthy servers, while the ASG ensures that if traffic spikes, new servers are dynamically launched to handle the load.

## Real World Analogy
- **Load Balancer**: A **Traffic Cop** or **Host at a Restaurant**. They see a crowd of customers walking in and direct them to the tables (servers) with the shortest wait times.
- **Auto Scaling**: The **Restaurant Manager**. When they see a massive line forming outside, they instantly call in off-duty chefs (new EC2 instances) to help. When the lunch rush is over, they send the extra chefs home to save money.

## How It Works
1. **ALB**: Sits in a Public Subnet. It receives HTTPS traffic, terminates the SSL certificate, and uses a Round-Robin algorithm to forward the HTTP request to a Target Group (a list of your EC2 instances located in Private Subnets).
2. **ASG**: Continuously monitors the average CPU utilization of your EC2 instances. If average CPU > 70%, it launches a new instance, installs your Node app, and registers it with the ALB.
3. **Health Checks**: The ALB pings `/api/health` every 10 seconds. If an instance doesn't reply 3 times in a row, the ALB stops sending traffic to it.

## Core Concepts
- **Target Group**: The logical grouping of servers the Load Balancer forwards traffic to.
- **Listeners**: Rules on the ALB (e.g., "If port 443, forward to Target Group A").
- **Launch Template**: A blueprint for Auto Scaling that defines what AMI, instance type, and IAM Role the new dynamically launched servers should use.

## MERN Stack Integration
Load Balancers are crucial for horizontal scaling in Node.js. Because Node is single-threaded, scaling up means running multiple Node processes across multiple machines. The ALB acts as the unified entry point. Your frontend (React/Next.js) makes API calls to `api.yourdomain.com`, which points to the ALB. The ALB seamlessly balances the requests across 5 different Express servers.

## Production Impact
- **High Availability**: By placing EC2 instances in different Availability Zones and balancing traffic between them, an entire AWS data center can burn down, and your React app won't even drop a request.
- **Zero-Downtime Deployments**: You can update your Express app one server at a time, keeping the application online during updates.

## Real Production Use Cases
- A food delivery app experiences massive traffic spikes at 12:00 PM and 6:00 PM. The ASG scales the backend from 2 servers to 20 servers during these windows, and scales back down to 2 servers at 2:00 AM, optimizing costs perfectly.

## Production Best Practices
- **Stateless Authentication**: Because User A's first request might hit Server 1, and their second request might hit Server 2, your Express app MUST be stateless. Use JWTs (JSON Web Tokens) or store session data in ElastiCache (Redis). If you use local server memory for sessions, users will constantly be logged out.

## Security Best Practices
- **SSL Termination**: Install your SSL/TLS certificates on the ALB using AWS Certificate Manager (ACM). The ALB decrypts the traffic and passes plain HTTP to your private EC2 instances, offloading the CPU-heavy decryption work from your Node servers.
- **Security Group Chaining**: Ensure your EC2 Security Group ONLY accepts inbound traffic from the ALB's Security Group.

## Cost Optimization Tips
- ALBs cost around $16/month base, plus data processing fees. Don't use them for tiny hobby projects, but they are mandatory for production.
- Use Target Tracking Scaling Policies (e.g., keep average CPU at 50%) rather than step scaling.

## Common Mistakes
- **Unhealthy Targets**: Forgetting to create a `GET /health` route in Express that returns `200 OK`. If the ALB's health check fails, it will unregister the server and your app will go offline, even if the code works perfectly.

## Debugging & Troubleshooting
- **502 Bad Gateway**: This means the ALB received the request, but the Express server in the Target Group actively rejected it or crashed while processing it. Check PM2 logs.
- **504 Gateway Timeout**: The Express server took too long to respond (usually a MongoDB connection timeout or a heavy query).

---
Prev : [./01_EC2_Deep_Dive.md](./01_EC2_Deep_Dive.md) | Index : [../00_Index.md](../00_Index.md) | Next : [./03_S3_Deep_Dive.md](./03_S3_Deep_Dive.md)
---
