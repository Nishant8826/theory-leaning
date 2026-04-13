# Deployment & Production Infrastructure

> 📌 **File:** 25_Deployment_And_Production_Infrastructure.md | **Level:** Full-Stack Dev → Networking Expert

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
│  │   Distribution  │  ┌─ /static/* → S3 (React build)               │
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
│                                                                        │
│  External: MongoDB Atlas (VPC Peering or PrivateLink)                 │
│  CI/CD: GitHub Actions → ECR → CodeDeploy / ECS                      │
│  Monitoring: CloudWatch, X-Ray, Prometheus                            │
└────────────────────────────────────────────────────────────────────────┘
```

---

## Deployment Pipeline

```
Developer: git push → GitHub Actions

┌──────────────────────────────────────────────────────────────────┐
│  CI/CD Pipeline                                                  │
│                                                                  │
│  1. Test (GitHub Actions)                                       │
│     npm test → eslint → type check                              │
│                                                                  │
│  2. Build (GitHub Actions)                                      │
│     docker build → tag with git SHA                             │
│     docker push → ECR (123456789.dkr.ecr.us-east-1/api:abc123) │
│                                                                  │
│  3. Deploy (CodeDeploy / ECS)                                   │
│     Rolling update: one instance at a time                      │
│     ALB health check gates each step                            │
│                                                                  │
│  4. Verify (automated)                                          │
│     Smoke tests against production                              │
│     Check error rate in CloudWatch                              │
│     Auto-rollback if error rate > 5%                             │
│                                                                  │
│  Timeline: git push → production: ~5 minutes                    │
└──────────────────────────────────────────────────────────────────┘
```

### GitHub Actions Workflow

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: npm ci
      - run: npm test
      - run: npm run lint

  build-and-deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789:role/github-actions
          aws-region: us-east-1
      
      - name: Login to ECR
        id: ecr
        uses: aws-actions/amazon-ecr-login@v2
      
      - name: Build and push Docker image
        env:
          ECR_REGISTRY: ${{ steps.ecr.outputs.registry }}
          IMAGE_TAG: ${{ github.sha }}
        run: |
          docker build -t $ECR_REGISTRY/api:$IMAGE_TAG .
          docker push $ECR_REGISTRY/api:$IMAGE_TAG
      
      - name: Deploy to ECS
        run: |
          aws ecs update-service \
            --cluster production \
            --service api-service \
            --force-new-deployment
      
      - name: Wait for deployment
        run: |
          aws ecs wait services-stable \
            --cluster production \
            --services api-service
```

---

## Auto Scaling

```
┌──────────────────────────────────────────────────────────────────┐
│  Auto Scaling Group Configuration                                │
│                                                                  │
│  Min: 2 instances (always running — one per AZ)                 │
│  Desired: 3 instances (normal load)                             │
│  Max: 10 instances (peak load)                                  │
│                                                                  │
│  Scale OUT when:                                                 │
│    CPU > 70% for 3 minutes                                      │
│    Request count > 1000/min per target                          │
│    ALB response time > 2 seconds                                │
│                                                                  │
│  Scale IN when:                                                  │
│    CPU < 30% for 10 minutes                                     │
│    Cooldown: 5 minutes (prevent flapping)                       │
│                                                                  │
│  Load pattern:                                                   │
│    Night: 2 instances                                            │
│    Day: 3-5 instances                                            │
│    Flash sale: 5-10 instances (auto-scales)                     │
│    After peak: scales back down (saves money)                   │
└──────────────────────────────────────────────────────────────────┘
```

---

## Zero-Downtime Deployment Checklist

```javascript
// ──── 1. Health Check Endpoint ────
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

// ──── 2. Graceful Shutdown ────
let isShuttingDown = false;

process.on('SIGTERM', async () => {
  console.log('SIGTERM — starting graceful shutdown');
  isShuttingDown = true;
  
  // 1. Stop accepting new connections
  server.close(async () => {
    // 2. Wait for in-flight requests (ALB connection draining handles this)
    console.log('Server closed — cleaning up');
    
    // 3. Close database connections
    await mongoose.connection.close();
    await redis.quit();
    
    // 4. Exit
    console.log('Cleanup complete — exiting');
    process.exit(0);
  });
  
  // Force exit after 30s
  setTimeout(() => process.exit(1), 30000);
});

// ──── 3. Keep-Alive Alignment ────
server.keepAliveTimeout = 65000;  // > ALB idle timeout (60s)
server.headersTimeout = 66000;

// ──── 4. Trust Proxy (behind ALB) ────
app.set('trust proxy', true);

// ──── 5. Backward-Compatible API Changes ────
// During rolling deploy, v1 and v2 run simultaneously!
// New fields: add (old clients ignore new fields) ✅
// Remove fields: deprecate first, remove later ✅
// Rename fields: add new name, keep old, remove old later ✅
// Change types: NEVER during rolling deploy ❌
```

---

## Cost Optimization

```
┌──────────────────────────────────────────────────────────────────┐
│  Cost Breakdown (typical full-stack app)                        │
├───────────────────────┬────────────────┬────────────────────────┤
│  Resource             │ Monthly Cost   │ Optimization           │
├───────────────────────┼────────────────┼────────────────────────┤
│  EC2 (3× t3.medium)  │ ~$90           │ Reserved Instances -40%│
│  ALB                  │ ~$25           │ Cannot reduce          │
│  RDS (db.t3.medium)  │ ~$65           │ Reserved Instance -40% │
│  ElastiCache (t3.micro)│ ~$15         │ Right-size             │
│  NAT Gateway          │ ~$35+data     │ VPC endpoints for S3   │
│  CloudFront           │ ~$10          │ Efficient caching      │
│  Route 53             │ ~$2           │ Minimal                │
│  S3                   │ ~$5           │ Lifecycle policies     │
│  CloudWatch           │ ~$10          │ Log retention policies │
│  Data Transfer         │ ~$10-50      │ CDN, compression       │
├───────────────────────┼────────────────┼────────────────────────┤
│  Total                │ ~$270-380     │ ~$180-250 optimized    │
├───────────────────────┴────────────────┴────────────────────────┤
│                                                                  │
│  Quick wins:                                                     │
│  1. S3 VPC endpoint: Save $0.045/GB on S3 traffic (free!)      │
│  2. Reserved Instances: 40% savings on EC2 + RDS               │
│  3. Right-size: t3.micro instead of t3.medium where possible   │
│  4. Auto-scale down at night: 3→2 instances                    │
│  5. CDN caching: Reduce origin requests by 80%+               │
│  6. Compression: Reduce data transfer by 60-80%               │
│  7. CloudWatch log retention: 30 days instead of forever       │
└──────────────────────────────────────────────────────────────────┘
```

---

## Disaster Recovery

```
┌──────────────────────────────────────────────────────────────────┐
│  DR Strategy         │ RPO/RTO        │ Cost                    │
├──────────────────────┼────────────────┼─────────────────────────┤
│  Backup & Restore    │ Hours/Hours    │ $ (cheapest)            │
│  (S3 backups, AMIs)  │                │ Only backup costs       │
│                      │                │                         │
│  Pilot Light         │ Minutes/Hours  │ $$ (small standby)     │
│  (DB replica running │                │ DB + minimal infra     │
│   minimal infra)     │                │                         │
│                      │                │                         │
│  Warm Standby        │ Seconds/Minutes│ $$$ (reduced capacity) │
│  (Everything running │                │ Full stack, scaled down │
│   at reduced scale)  │                │                         │
│                      │                │                         │
│  Multi-Region Active │ Zero/Seconds   │ $$$$ (2× everything)   │
│  (Full stack in 2    │                │ Highest availability    │
│   regions, Route 53  │                │                         │
│   failover routing)  │                │                         │
├──────────────────────┴────────────────┴─────────────────────────┤
│  For most apps: Pilot Light (DB read replica in second region) │
│  RPO: time since last replication                               │
│  RTO: time to promote replica + deploy app in new region        │
└──────────────────────────────────────────────────────────────────┘
```

---

## Final Networking Checklist

```
┌──────────────────────────────────────────────────────────────────┐
│  ✅ Production Readiness Checklist                               │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  DNS & Domain:                                                   │
│  □ Custom domain with Route 53                                  │
│  □ HTTPS everywhere (ACM certificates)                          │
│  □ HTTP → HTTPS redirect                                        │
│  □ HSTS header (Strict-Transport-Security)                     │
│                                                                  │
│  Infrastructure:                                                 │
│  □ Multi-AZ deployment (minimum 2 AZs)                         │
│  □ VPC with public/private/data subnets                        │
│  □ Security groups referencing by SG ID                        │
│  □ VPC endpoints for S3 and DynamoDB                           │
│  □ NAT Gateway for private subnets                             │
│                                                                  │
│  Application:                                                    │
│  □ Health check endpoint (/health)                              │
│  □ Graceful shutdown (SIGTERM handler)                          │
│  □ Keep-alive timeout > ALB timeout (65s > 60s)               │
│  □ Trust proxy configured (app.set('trust proxy'))             │
│  □ Compression enabled (gzip/brotli)                           │
│  □ Connection pooling for all databases                        │
│  □ TCP keep-alive < NAT timeout (120s < 350s)                 │
│  □ Timeouts on all outbound requests                           │
│  □ Structured JSON logging                                      │
│  □ Error handling (no unhandled rejections crash)              │
│                                                                  │
│  Performance:                                                    │
│  □ CloudFront CDN for static assets                            │
│  □ Redis caching for hot data                                   │
│  □ Cache-Control headers on all responses                      │
│  □ HTTP/2 enabled (Nginx/ALB)                                  │
│  □ Database indexes on query patterns                          │
│                                                                  │
│  Security:                                                       │
│  □ Databases in private subnets                                │
│  □ No SSH 0.0.0.0/0 (use bastion or SSM)                      │
│  □ Helmet security headers                                      │
│  □ Rate limiting on API and auth endpoints                     │
│  □ CORS configured with specific origins                       │
│  □ Input validation and sanitization                           │
│  □ Secrets in Secrets Manager (not env files)                  │
│                                                                  │
│  Monitoring:                                                     │
│  □ CloudWatch alarms for critical metrics                      │
│  □ VPC Flow Logs enabled                                       │
│  □ Application metrics (Prometheus/CloudWatch)                 │
│  □ Distributed tracing (X-Request-ID)                          │
│  □ Error tracking and alerting                                 │
│                                                                  │
│  Deployment:                                                     │
│  □ CI/CD pipeline (GitHub Actions → ECR → ECS/CodeDeploy)     │
│  □ Rolling/blue-green deployment                               │
│  □ Auto-rollback on error rate spike                           │
│  □ Auto-scaling configured                                     │
│  □ Database backups automated                                  │
│  □ DR strategy documented and tested                           │
└──────────────────────────────────────────────────────────────────┘
```

---

## Interview Q&A

**Q1: Walk me through how you'd deploy a full-stack app on AWS.**
> Route 53 for DNS → CloudFront CDN (TLS, caching) → ALB in public subnets → EC2/ECS in private subnets → RDS Multi-AZ + ElastiCache in data subnets. CI/CD: GitHub Actions → Docker build → ECR → Rolling deploy to ECS. Monitoring: CloudWatch alarms, structured logging, health checks. Security: private subnets for data, security groups by reference, ACM certificates, WAF.

**Q2: How do you achieve zero-downtime deployments?**
> Rolling deployment: update one instance at a time. ALB health checks detect unhealthy instances and stop routing traffic. Connection draining waits for in-flight requests. Graceful shutdown in Node.js handles SIGTERM, completes pending work, closes DB connections. Backward-compatible API changes ensure v1 and v2 coexist during rollout.

**Q3: How do you handle auto-scaling for a Node.js application?**
> Auto Scaling Group with target tracking: CPU > 70%, scale out. Minimum 2 instances (one per AZ). Stateless servers (sessions in Redis, files in S3). Health checks confirm instances are ready before receiving traffic. Cooldown periods prevent thrashing. Scale-in slowly (10 minutes grace).

**Q4: What's your approach to cost optimization on AWS?**
> Reserved Instances for predictable workloads (40% savings). VPC endpoints for S3/DynamoDB (free, saves NAT costs). Right-size instances (CloudWatch metrics guide sizing). Auto-scale down at night. CDN caching (reduce origin load). Compression (reduce transfer costs). CloudWatch log retention policies. Spot Instances for non-critical workloads.

**Q5: How do you design for high availability?**
> Multi-AZ: EC2 ASG across 2+ AZs, RDS Multi-AZ, ElastiCache Multi-AZ. Multi-region for global apps: Route 53 latency-based routing, read replicas in secondary region, CloudFront global edge. No single points of failure: every component has redundancy. Auto-scaling handles load spikes. Health checks detect and route around failures automatically.


Prev : [24 Network Monitoring And Observability](./24_Network_Monitoring_And_Observability.md) | Index: [0 Index](./0_Index.md) | Next : N/A
