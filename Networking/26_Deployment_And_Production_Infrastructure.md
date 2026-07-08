# Deployment & Production Infrastructure

> 📌 **File:** 26_Deployment_And_Production_Infrastructure.md | **Level:** Full-Stack Dev → Networking Expert

---

## What is it?

This is the capstone — putting everything together for a production deployment. We'll design the complete networking architecture for deploying your full-stack app (React + Node.js + MongoDB + Redis) on AWS with zero-downtime, high availability, and proper security.

---

## The Complete Production Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│                          PRODUCTION ARCHITECTURE                       │
│                                                                        │
│  Users worldwide                                                       │
│       │                                                                │
│  ┌────▼────┐                                                          │
│  │Route 53 │  DNS: myapp.com → CloudFront                            │
│  │         │  DNS: api.myapp.com → CloudFront                        │
│  └────┬────┘                                                          │
│       │                                                                │
│  ┌────▼────────────┐                                                  │
│  │   CloudFront    │  CDN: TLS termination, caching, HTTP/3          │
│  │   Distribution  │  ├─ /static/* → S3 (React build)               │
│  │                 │  └─ /api/* → ALB origin                         │
│  └────┬────────────┘                                                  │
│       │                                                                │
│  ┌────▼────────────────────────── VPC: 10.0.0.0/16 ───────────────┐  │
│  │                                                                 │  │
│  │  ┌──── Public Subnet (10.0.1.0/24, 10.0.2.0/24) ────────────┐ │  │
│  │  │  ┌─────────┐                    ┌─────────────┐          │ │  │
│  │  │  │   ALB   │  HTTPS listener    │ NAT Gateway │          │ │  │
│  │  │  │         │  Health checks     │ (per AZ)    │          │ │  │
│  │  │  └────┬────┘                    └─────────────┘          │ │  │
│  │  └───────┼──────────────────────────────────────────────────┘ │  │
│  │          │                                                     │  │
│  │  ┌───── Private App Subnet (10.0.10.0/24, 10.0.11.0/24) ──┐ │  │
│  │  │  ┌─────────┐  ┌─────────┐  ┌─────────┐                │ │  │
│  │  │  │  EC2    │  │  EC2    │  │  EC2    │  (Auto Scaling │ │  │
│  │  │  │ Node.js │  │ Node.js │  │ Node.js │   Group)       │ │  │
│  │  │  │ PM2     │  │ PM2     │  │ PM2     │                │ │  │
│  │  │  │ :3000   │  │ :3000   │  │ :3000   │                │ │  │
│  │  │  └─────────┘  └─────────┘  └─────────┘                │ │  │
│  │  └────────────────────────────────────────────────────────┘ │  │
│  │          │                                                     │  │
│  │  ┌───── Private Data Subnet (10.0.20.0/24, 10.0.21.0/24) ─┐ │  │
│  │  │  ┌─────────┐  ┌─────────┐                              │ │  │
│  │  │  │  RDS    │  │  Redis  │  (ElastiCache)              │ │  │
│  │  │  │Multi-AZ │  │Multi-AZ │                              │ │  │
│  │  │  │ :5432   │  │ :6379   │                              │ │  │
│  │  │  └─────────┘  └─────────┘                              │ │  │
│  │  └────────────────────────────────────────────────────────┘ │  │
│  │                                                               │  │
│  │  VPC Endpoints: S3 (Gateway), ECR (Interface)               │  │
│  └───────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────┘
```

#### Diagram Explanation (The Corporate Headquarters)
This is the final view of your entire infrastructure:
- **The Global Mailroom (CloudFront):** Sitting at the edge of the internet, intercepting requests. Static files (`/static`) are served from edge without bothering the corporate office.
- **The Front Desk (ALB):** Deep inside the perimeter (VPC), routes incoming custom requests (`/api`) to an available EC2 worker.
- **The Workforce (EC2 Node.js):** EC2 instances in private subnets executing request handlers.
- **The Vault (RDS/Redis):** The strictly protected room holding your databases, completely isolated from the internet.

---

## Deployment Pipeline

```
Developer: git push → GitHub Actions
  1. Test: Run linting and unit tests
  2. Build: Build Docker image, tag, and push to AWS ECR
  3. Deploy: Trigger CodeDeploy / ECS rolling update
  4. Verify: Smoke tests and CloudWatch logs verification
```

### Zero-Downtime Deployment Code Checklist

```javascript
// 1. Health check endpoint supporting shutdown checks
app.get('/health', async (req, res) => {
  if (isShuttingDown) return res.status(503).json({ status: 'shutting_down' });
  try {
    await mongoose.connection.db.admin().ping();
    await redis.ping();
    res.status(200).json({ status: 'healthy' });
  } catch {
    res.status(503).json({ status: 'unhealthy' });
  }
});

// 2. Graceful SIGTERM shutdown handler
let isShuttingDown = false;
process.on('SIGTERM', async () => {
  console.log('SIGTERM — starting graceful shutdown');
  isShuttingDown = true;
  
  server.close(async () => {
    console.log('Server closed — cleaning up');
    await mongoose.connection.close();
    await redis.quit();
    process.exit(0);
  });
  
  setTimeout(() => process.exit(1), 30000);
});

// 3. Keep-alive alignment
server.keepAliveTimeout = 65000; // > ALB idle timeout (60s)
server.headersTimeout = 66000;
```

---

## Disaster Recovery Strategies

- **Backup & Restore:** Daily S3 backups and server AMIs. Cheap, RPO/RTO in hours.
- **Pilot Light:** DB read replica running in secondary region. Low RPO (seconds), RTO in minutes.
- **Warm Standby:** All stack components running at reduced scale in second region.
- **Active-Active:** Fully scaled multi-region replication. Zero RPO, seconds RTO. Expensive.

---

## Practice Exercises

### Exercise 1: Graceful Shutdown Implementation
Add a SIGTERM graceful shutdown handler to your Express API. Run it locally and test killing the process with `kill -15` (SIGTERM). Verify pending requests complete before exit.

### Exercise 2: Pipeline Blueprint
Create a GitHub Actions workflow YAML file that builds a docker image and outlines AWS ECR deployment steps.

---

## Interview Q&A

**Q1: Walk me through how you'd deploy a full-stack app on AWS.**
> Route 53 for DNS → CloudFront CDN (TLS, caching) → ALB in public subnets → EC2/ECS in private subnets → RDS Multi-AZ + ElastiCache in data subnets. CI/CD: GitHub Actions → Docker build → ECR → Rolling deploy to ECS. Monitoring: CloudWatch alarms, structured logging, health checks. Security: private subnets for data, security groups by reference, ACM certificates, WAF.

**Q2: How do you achieve zero-downtime deployments?**
> Rolling deployment: update one instance at a time. ALB health checks detect unhealthy instances and stop routing traffic. Connection draining waits for in-flight requests. Graceful shutdown in Node.js handles SIGTERM, completes pending work, closes DB connections. Backward-compatible API changes ensure v1 and v2 coexist during rollout.

**Q3: How do you handle auto-scaling for a Node.js application?**
> Auto Scaling Group with target tracking: CPU > 70%, scale out. Minimum 2 instances (one per AZ). Stateless servers (sessions in Redis, files in S3). Health checks confirm instances are ready before receiving traffic.

**Q4: What's your approach to cost optimization on AWS?**
> Reserved Instances for predictable workloads (40% savings). VPC endpoints for S3/DynamoDB (free, saves NAT costs). Right-size instances (CloudWatch metrics guide sizing). Auto-scale down at night. CDN caching (reduce origin load). Compression (reduce transfer costs).

**Q5: How do you design for high availability?**
> Multi-AZ: EC2 ASG across 2+ AZs, RDS Multi-AZ, ElastiCache Multi-AZ. Multi-region for global apps: Route 53 latency-based routing, read replicas in secondary region, CloudFront global edge. No single points of failure: every component has redundancy.

---

Prev : [25 Network Monitoring And Observability](./25_Network_Monitoring_And_Observability.md) | Index: [00 Index](./00_Index.md) | Next : N/A
