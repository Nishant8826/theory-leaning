# 🚀 Interview Preparation - AWS

> **Domain:** Cloud Infrastructure / System Architecture  
> **Level:** Beginner to Expert  
> **Target Role:** Software Engineer / Senior Engineer / DevOps Engineer / Cloud Architect

---

## 🟢 Beginner Level

### ❓ Q1. **What is AWS and what is Cloud Computing?**

<details>
<summary><b>👀 Show Answer</b></summary>

* **Cloud Computing:** The on-demand delivery of IT resources (compute, database, storage, networking) over the internet with pay-as-you-go pricing, replacing physical on-premise servers.
* **AWS (Amazon Web Services):** The world's leading cloud platform, offering over 200 fully featured services from data centers globally. It allows scaling resources up or down dynamically, reducing upfront capital expenditure (CapEx) to operational expenditure (OpEx).

> 💡 **Interviewer Focus:** Pay-as-you-go cost model, elastic resource allocation, and transitioning from physical server operations to virtual cloud infrastructure.

</details>

<hr/>

### ❓ Q2. **What is the difference between Regions and Availability Zones (AZs)?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **AWS Region:** A physical geographical location in the world where AWS clusters data centers (e.g., `us-east-1` in N. Virginia, `ap-south-1` in Mumbai). Each region is completely isolated from other regions to ensure fault tolerance.
- **Availability Zone (AZ):** One or more discrete data centers within an AWS Region. Each AZ is isolated regarding power, cooling, and network, but connected to other AZs in the same region via low-latency, redundant private fiber optic links.

> 💡 **Interviewer Focus:** Designing high availability by deploying resources (like EC2 instances or RDS databases) across multiple AZs to prevent local data center outages.

</details>

<hr/>

### ❓ Q3. **What is IAM and what is the principle of least privilege?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **IAM (Identity and Access Management):** A web service that helps you securely control access to AWS resources. It manages who is authenticated (signed in) and authorized (has permissions) to use resources.
- **Principle of Least Privilege:** A core security best practice where users, groups, or roles are granted *only* the minimum necessary permissions required to perform their specific tasks, and nothing more.

> 💡 **Interviewer Focus:** Avoiding using the AWS Root User account for daily operations, and using IAM policies to enforce narrow permission boundaries.

</details>

<hr/>

### ❓ Q4. **What is Amazon EC2?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **EC2 (Elastic Compute Cloud):** Provides secure, resizable virtual servers (compute capacity) in the cloud.
- **Key Concepts:**
  - **AMI (Amazon Machine Image):** Pre-configured templates containing the OS and software needed to launch instances.
  - **Instance Types:** Optimized configurations of CPU, memory, storage, and networking (e.g., General Purpose `t` or `m`, Compute Optimized `c`, Memory Optimized `r`).
  - **Key Pairs:** Secure login credentials using public/private key cryptography.

> 💡 **Interviewer Focus:** Dynamic scaling capabilities and selecting instance types based on application workload profiles (e.g., memory vs compute intensive).

</details>

<hr/>

### ❓ Q5. **What is Amazon S3 and what are its storage classes?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **S3 (Simple Storage Service):** An object storage service offering industry-leading scalability, data availability, security, and performance. Stores files as "objects" inside "buckets".
- **Storage Classes:**
  - **S3 Standard:** High durability, availability, and performance object storage for frequently accessed data.
  - **S3 Intelligent-Tiering:** Automatically moves data to the most cost-effective tier based on access patterns.
  - **S3 Standard-IA (Infrequent Access):** For data accessed less frequently but requiring rapid access when needed (lower storage price, retrieval fee).
  - **S3 Glacier Flexible/Deep Archive:** Ultra low-cost archive storage for data archiving (retrieval times range from minutes to 12 hours).

> 💡 **Interviewer Focus:** Designing lifecycle rules to automatically move logs or backups to Glacier to optimize storage costs.

</details>

<hr/>

### ❓ Q6. **What is a VPC and what are public vs private subnets?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **VPC (Virtual Private Cloud):** A logically isolated virtual network dedicated to your AWS account. You control IP address ranges, subnets, route tables, and network gateways.
- **Public Subnet:** A subnet linked to an **Internet Gateway (IGW)**, allowing resources inside it (like load balancers) to send and receive traffic directly to/from the public internet.
- **Private Subnet:** A subnet with no direct route to the Internet Gateway. Resources inside it (like databases or app servers) cannot be reached from the internet, but can access the internet outbound via a **NAT Gateway** placed in a public subnet.

> 💡 **Interviewer Focus:** Keeping databases and backend application servers inside private subnets for security.

</details>

<hr/>

### ❓ Q7. **What is Amazon RDS?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **RDS (Relational Database Service):** A managed service that makes it easy to set up, operate, and scale relational databases in the cloud.
- **Supported Engines:** MySQL, PostgreSQL, MariaDB, Oracle, MS SQL Server, and Amazon Aurora.
- **Managed Features:** Automatic patching, automated backups, hardware scaling, and Multi-AZ replication for high availability.

> 💡 **Interviewer Focus:** Managed benefits of RDS compared to hosting a database manually on a self-managed EC2 instance (saving administrative operational overhead).

</details>

<hr/>

### ❓ Q8. **What is AWS Lambda and what is Serverless?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **AWS Lambda:** A serverless event-driven compute service that lets you run code without provisioning or managing servers. You pay only for the compute time you consume (per millisecond).
- **Serverless:** A cloud execution model where the cloud provider manages server provisioning, scaling, patching, and infrastructure management automatically, letting developers focus purely on application code.

> 💡 **Interviewer Focus:** Point out that serverless does not mean there are no servers; it means server management is abstracted away from the developer.

</details>

<hr/>

### ❓ Q9. **What is the difference between Security Groups and NACLs?**

<details>
<summary><b>👀 Show Answer</b></summary>

Both act as firewalls but operate at different network layers:
- **Security Groups (Instance Level):**
  - **Stateful:** If you allow inbound traffic, outbound return traffic is automatically allowed.
  - Supports only `ALLOW` rules.
  - Evaluates all rules before deciding to permit traffic.
- **NACLs - Network Access Control Lists (Subnet Level):**
  - **Stateless:** Outbound return traffic must be explicitly allowed.
  - Supports both `ALLOW` and `DENY` rules (useful for blocking specific IP blocks).
  - Rules are processed sequentially in numerical order.

> 💡 **Interviewer Focus:** Explaining how to secure an architecture by combining security groups at the EC2 instance layer with NACLs at the subnet boundary.

</details>

<hr/>

### ❓ Q10. **What is Amazon Route 53?**

<details>
<summary><b>👀 Show Answer</b></summary>

Route 53 is a highly available and scalable Domain Name System (DNS) web service.
- **Role:** Translates human-friendly domain names (e.g., `www.example.com`) into numeric IP addresses (e.g., `192.0.2.1`).
- **Routing Policies:** Supports Latency-based, Geo DNS, Failover (for disaster recovery), Weighted, and Simple routing.

> 💡 **Interviewer Focus:** Implementing global high availability using Route 53 active-passive failover routes.

</details>

<hr/>

### ❓ Q11. **Explain the AWS Shared Responsibility Model.**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Security OF the Cloud (AWS Responsibility):** AWS is responsible for protecting the physical infrastructure (hardware, software, networking, facilities) that runs all of the services offered.
- **Security IN the Cloud (Customer Responsibility):** The customer is responsible for configuring guest operating systems, firewalls (security groups), network routes, identity access permissions (IAM), data encryption, and application code dependencies.

> 💡 **Interviewer Focus:** Differentiating physical security responsibilities from cloud configuration responsibilities.

</details>

<hr/>

### ❓ Q12. **What is an Elastic IP address?**

<details>
<summary><b>👀 Show Answer</b></summary>

An Elastic IP address is a static, public IPv4 address allocated to your AWS account. You can mask the failure of an instance or software by rapidly remapping the Elastic IP address to another active instance in your VPC.

> 💡 **Interviewer Focus:** Point out that while static IPs are useful, deploying load balancers (ALBs) or DNS CNAMEs is preferred for high availability routing instead of mapping static IPs to individual EC2 instances.

</details>

<hr/>

### ❓ Q13. **What is the difference between EBS and S3?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **EBS (Elastic Block Store):** High-performance block storage volume designed for use with a single EC2 instance (similar to a local physical hard drive). Ideal for databases or file systems.
- **S3 (Simple Storage Service):** Object storage accessible from anywhere via HTTP. Highly scalable, durable, and designed for static assets (images, backups, HTML files).

> 💡 **Interviewer Focus:** EBS volume network coupling limits vs S3 global availability.

</details>

<hr/>

### ❓ Q14. **What is AWS CloudTrail used for?**

<details>
<summary><b>👀 Show Answer</b></summary>

AWS CloudTrail records all API activity across your AWS account. It tracks *who* made an API request, *what* resource was modified, *when* the request occurred, and from *which* IP address. Essential for security audits, compliance, and troubleshooting resource modifications.

> 💡 **Interviewer Focus:** Audit logs management and security incident post-mortems.

</details>

<hr/>

### ❓ Q15. **What is the role of an Internet Gateway (IGW)?**

<details>
<summary><b>👀 Show Answer</b></summary>

An Internet Gateway is a horizontally scaled, redundant VPC component that enables communication between resources in a public subnet and the public internet. It performs Network Address Translation (NAT) for instances with public IP addresses.

> 💡 **Interviewer Focus:** Internet gateways are required for resources that must be publicly accessible (like load balancers).

</details>

<hr/>

### ❓ Q16. **Explain what an Auto Scaling Group (ASG) does.**

<details>
<summary><b>👀 Show Answer</b></summary>

An ASG monitors your EC2 instances and automatically adjusts the instance count (scaling out by adding instances, or scaling in by terminating instances) to maintain target CPU thresholds or request capacities. It also performs health checks to automatically replace unhealthy instances.

> 💡 **Interviewer Focus:** Dynamic capacity scaling matching application demand patterns.

</details>

<hr/>

### ❓ Q17. **What is an AWS IAM Policy?**

<details>
<summary><b>👀 Show Answer</b></summary>

An IAM Policy is a JSON document that explicitly defines permissions. It specifies:
- **Effect:** Allow or Deny.
- **Action:** List of API operations allowed (e.g. `s3:GetObject`).
- **Resource:** Target AWS resources (e.g. bucket ARN).
- **Condition:** Under what variables the policy applies.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::my-bucket/*"
    }
  ]
}
```

> 💡 **Interviewer Focus:** JSON policy syntax components.

</details>

<hr/>

### ❓ Q18. **What is Amazon CloudWatch?**

<details>
<summary><b>👀 Show Answer</b></summary>

CloudWatch is a monitoring and observability service. It collects metric data (CPU utilization, disk write metrics), aggregates logs from EC2/Lambda, and allows users to configure Alarms to trigger actions (like auto-scaling or sending emails) when metrics cross limits.

> 💡 **Interviewer Focus:** Metric alarms triggers.

</details>

<hr/>

### ❓ Q19. **What are the differences between scale-up and scale-out?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Scale-Up (Vertical Scaling):** Increasing the capacity of an existing resource (e.g. changing an EC2 instance from a `t3.medium` to a `t3.xlarge` with more RAM/CPU).
- **Scale-Out (Horizontal Scaling):** Adding more resource units in parallel (e.g. adding more `t3.medium` instances to an Auto Scaling Group). Preferred for cloud designs.

> 💡 **Interviewer Focus:** Horizontal scaling is preferred because it avoids single-point-of-failure limits and supports cost elasticity.

</details>

<hr/>

### ❓ Q20. **What is a NAT Gateway and why is it placed in a public subnet?**

<details>
<summary><b>👀 Show Answer</b></summary>

A NAT (Network Address Translation) Gateway allows EC2 instances in private subnets to connect outbound to the internet (e.g., for system updates), but prevents the public internet from initiating connections with those private instances.
- **Why in public subnet:** It needs a route to the Internet Gateway to forward outgoing private traffic and receive the response.

> 💡 **Interviewer Focus:** Securing database updates routing.

</details>

<hr/>

### ❓ Q21. **What is AWS IAM Root User?**

<details>
<summary><b>👀 Show Answer</b></summary>

The Root User is the initial identity created when the AWS account is set up. It has absolute, unrestricted access to all resources and billing metrics.
- **Best Practice:** Enable MFA immediately, lock away root credentials, and perform daily tasks using delegated IAM users with limited permissions.

> 💡 **Interviewer Focus:** Core security configurations.

</details>

<hr/>

### ❓ Q22. **What is the purpose of S3 Bucket Policies?**

<details>
<summary><b>👀 Show Answer</b></summary>

S3 Bucket Policies are resource-based policies attached directly to S3 buckets. They manage access permissions for users inside and outside your AWS account, enforcing constraints like requiring HTTPS or blocking unencrypted uploads.

> 💡 **Interviewer Focus:** Restricting bucket access boundaries.

</details>

<hr/>

### ❓ Q23. **What is the default limit of VPCs per region?**

<details>
<summary><b>👀 Show Answer</b></summary>

The default soft limit of VPCs per region is **`5`**. This limit can be increased by submitting a service quota request to AWS.

> 💡 **Interviewer Focus:** AWS Service Quotas familiarity.

</details>

<hr/>

### ❓ Q24. **How do you SSH into an EC2 instance in a private subnet?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Option A: Bastion Host (Jump Box):** Deploy a tiny EC2 instance in a public subnet, SSH into the Bastion, and then SSH from the Bastion to the private instance.
- **Option B (Modern Preferred): AWS Systems Manager Session Manager:** Bypasses SSH keys and internet access entirely. It executes commands via the SSM Agent using secure IAM policies.

> 💡 **Interviewer Focus:** Security: avoiding exposing port 22 directly to the internet.

</details>

<hr/>

### ❓ Q25. **What does the keyword 'Serverless' mean for databases?**

<details>
<summary><b>👀 Show Answer</b></summary>

Serverless databases (like DynamoDB or Aurora Serverless) automate database instance scaling, resource allocation, and storage management. You pay based on actual database operations (reads/writes per second) rather than paying for idle database server CPU time.

> 💡 **Interviewer Focus:** Database scaling models.

</details>

<hr/>

## 🟡 Intermediate Level

### ❓ Q26. **Explain AWS IAM Role vs. IAM User vs. IAM Group.**

<details>
<summary><b>👀 Show Answer</b></summary>

- **IAM User:** An identity representing a specific person or application that interacts with AWS. Has permanent credentials (password or access keys).
- **IAM Group:** A collection of IAM Users. Used to apply matching permission policies to multiple users at once.
- **IAM Role:** An identity with permission policies that determine what the identity can and cannot do in AWS, but is **not associated with a specific user**.
  - Roles do not have permanent credentials.
  - Temporarily assumed by users, applications, or AWS services (like an EC2 instance assuming a role to read from S3) using STS (Security Token Service) to obtain short-lived credentials.

> 💡 **Interviewer Focus:** Never hardcode access keys on EC2 instances; always attach an IAM Instance Profile (Role) to the EC2 instance to fetch credentials securely.

</details>

<hr/>

### ❓ Q27. **How does an Amazon S3 Presigned URL work and when do you use it?**

<details>
<summary><b>👀 Show Answer</b></summary>

A Presigned URL gives temporary access to a private object in S3 using the credentials of the IAM user who generated the URL.
- **How it works:**
  - The URL contains cryptographic signature parameters verifying permission.
  - It remains valid only for a defined time window (e.g., 15 minutes).
- **Use Case:** Allowing users to download private files (like paid PDF reports, invoices) or upload files directly to S3 (bypassing the application server to save bandwidth) without making the S3 bucket public.

> 💡 **Interviewer Focus:** Bypassing application compute constraints by letting clients communicate directly with S3.

</details>

<hr/>

### ❓ Q28. **What is an AWS Lambda cold start and how do you optimize it?**

<details>
<summary><b>👀 Show Answer</b></summary>

A **Cold Start** is the latency latency latency that occurs when a Lambda function is invoked for the first time or after a period of inactivity. AWS must spin up a new container container environment, instantiate runtime engines, and load function bundle code.
- **Optimization Strategies:**
  - **Provisioned Concurrency:** Keeps a specified number of environments warm and ready to respond instantly (adds cost).
  - **Minimize package size:** Exclude unnecessary dependencies and bundle imports.
  - **Reuse resources outside handler:** Initialize database connection pools and SDK clients outside the Lambda handler function so they persist across invocations.
  - Choose runtimes with faster startup speeds (Node.js/Python are faster than Java/C#).

> 💡 **Interviewer Focus:** Knowing how to read execution metrics to distinguish initialization time (cold start) from handler execution time.

</details>

<hr/>

### ❓ Q29. **What is Amazon DynamoDB and how does it handle scaling?**

<details>
<summary><b>👀 Show Answer</b></summary>

DynamoDB is a fully managed NoSQL key-value and document database offering single-digit millisecond latency at any scale.
- **Scaling Mechanisms:**
  - Data is horizontally partitioned across multiple physical storage nodes based on the **Partition Key**.
  - **Capacity Modes:**
    - **Provisioned:** You define read capacity units (RCUs) and write capacity units (WCUs). Auto-scaling adjusts these based on CPU usage.
    - **On-Demand:** Scales up or down instantly based on request volume. Best for unpredictable workloads.

> 💡 **Interviewer Focus:** Importance of partition key design to prevent hot partition issues.

</details>

<hr/>

### ❓ Q30. **What is AWS Elastic Load Balancing? Compare ALB vs. NLB.**

<details>
<summary><b>👀 Show Answer</b></summary>

Elastic Load Balancing (ELB) automatically distributes incoming traffic across multiple targets (EC2 instances, containers, or IP addresses) to ensure high availability.
- **Application Load Balancer (ALB):**
  - Operates at Layer 7 (Application Layer).
  - Inspects HTTP/HTTPS headers, allowing routing based on URL paths (`/api` vs `/static`) or host headers.
  - Best for standard web application traffic.
- **Network Load Balancer (NLB):**
  - Operates at Layer 4 (Transport Layer).
  - Handles millions of requests per second with ultra-low latency.
  - Routes TCP/UDP traffic and provides static IP addresses per AZ.
  - Best for high-performance streaming, game servers, or IoT ingestion.

> 💡 **Interviewer Focus:** Knowing when to choose Layer 7 routing (ALB) vs high-throughput TCP optimization (NLB).

</details>

<hr/>

### ❓ Q31. **What is Amazon CloudFront and what is CDN caching?**

<details>
<summary><b>👀 Show Answer</b></summary>

CloudFront is a fast content delivery network (CDN) service that securely delivers data, videos, applications, and APIs to customers globally with low latency.
- **How it works:**
  - Caches static content (HTML, JS, images) at globally distributed **Edge Locations**.
  - When a user requests content, Route 53 routes them to the nearest Edge Location. If cached, the content is returned immediately (Cache Hit), bypassing the origin server (S3 or ALB).
  - If not cached, it fetches it from the origin, caches it for future users, and returns it (Cache Miss).

> 💡 **Interviewer Focus:** Caching headers (Cache-Control, TTL) and handling cache invalidation strategies during deployments.

</details>

<hr/>

### ❓ Q32. **Explain AWS SQS vs. SNS and when to use which.**

<details>
<summary><b>👀 Show Answer</b></summary>

- **SQS (Simple Queue Service):**
  - A message queuing service based on the **Pull** model.
  - Messages are stored in a queue until a worker retrieves and processes them.
  - Direct 1-to-1 decoupling: One message is consumed by one worker.
  - Best for decoupling microservices or batch processing tasks.
- **SNS (Simple Notification Service):**
  - A pub/sub messaging service based on the **Push** model.
  - Messages published to an SNS Topic are pushed instantly to all subscribers (HTTP, Lambda, SQS, Email).
  - Fan-out pattern: One event triggers notifications to multiple consumers simultaneously.

> 💡 **Interviewer Focus:** Combining SNS with SQS (fan-out pattern where SNS pushes messages to multiple SQS queues for parallel processing by different worker pools).

</details>

<hr/>

### ❓ Q33. **What is AWS API Gateway and what are its key features?**

<details>
<summary><b>👀 Show Answer</b></summary>

AWS API Gateway is a fully managed service that makes it easy for developers to create, publish, maintain, monitor, and secure APIs at any scale.
- **Key Features:**
  - Acts as the entry point (front door) for backend Lambda functions or VPC servers.
  - Handles CORS, API key management, request throttling, and payload validations.
  - Supports HTTP, REST, and WebSocket APIs.

> 💡 **Interviewer Focus:** Implementing auth guards at the gateway level using Cognito or Custom Lambda Authorizers.

</details>

<hr/>

### ❓ Q34. **What is the difference between AWS Secrets Manager and SSM Parameter Store?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **SSM Parameter Store:** Managed key-value configuration store. Free for standard parameters. Best for basic application settings, URLs, or non-sensitive properties.
- **AWS Secrets Manager:** Specifically designed for confidential credentials. Costs more, but supports **automatic password rotation** (for RDS databases), random secret generation, and cross-account access controls.

> 💡 **Interviewer Focus:** Credentials rotation security capabilities.

</details>

<hr/>

### ❓ Q35. **What is the role of the VPC NAT Gateway?**

<details>
<summary><b>👀 Show Answer</b></summary>

A NAT Gateway routes outbound traffic from private subnet instances to the internet, translating private IPs to its own public Elastic IP, and forwards responses back, preventing direct external incoming connections.

> 💡 **Interviewer Focus:** Secure internet access for internal VPC app servers.

</details>

<hr/>

### ❓ Q36. **Explain the difference between S3 Standard-IA and S3 One Zone-IA.**

<details>
<summary><b>👀 Show Answer</b></summary>

- **S3 Standard-IA (Infrequent Access):** Stores data redundantly across a minimum of **3 Availability Zones**. High availability ($99.9\%$).
- **S3 One Zone-IA:** Stores data in a **single Availability Zone**. Costs 20% less, but data will be lost if that specific AZ suffers a disaster. Recommended only for reproducible backups.

> 💡 **Interviewer Focus:** Cost optimization vs data durability.

</details>

<hr/>

### ❓ Q37. **How does Route 53 health checking work?**

<details>
<summary><b>👀 Show Answer</b></summary>

Route 53 monitors endpoints (IPs or domain names) using periodic ping requests. If an endpoint fails checks for a specified consecutive limit:
- Route 53 flags it as unhealthy.
- It removes the resource record from DNS queries and redirects users to a healthy standby endpoint.

> 💡 **Interviewer Focus:** Implementing DNS failovers for disaster recovery.

</details>

<hr/>

### ❓ Q38. **What is AWS Elastic Beanstalk?**

<details>
<summary><b>👀 Show Answer</b></summary>

Elastic Beanstalk is a Platform as a Service (PaaS) tool. Developers upload application code (Node.js, Docker, Java), and Beanstalk automatically provisions the load balancer, auto-scaling groups, EC2 instances, and databases while preserving full control of the underlying infrastructure.

> 💡 **Interviewer Focus:** Developers deployment velocity options.

</details>

<hr/>

### ❓ Q39. **Explain the concept of RDS Multi-AZ vs Read Replicas.**

<details>
<summary><b>👀 Show Answer</b></summary>

- **RDS Multi-AZ (High Availability):**
  - Replicates data **synchronously** to a standby instance in a different AZ.
  - Standby cannot accept traffic (active-passive).
  - Automatically handles automatic failovers if primary goes down.
- **Read Replicas (Scalability):**
  - Replicates data **asynchronously** to one or more active nodes.
  - Replicas accept read queries (active-active for reads).
  - Used to offload read-heavy workloads from the primary database.

> 💡 **Interviewer Focus:** Synchronous HA replication vs asynchronous read scaling.

</details>

<hr/>

### ❓ Q40. **What is AWS KMS and how does key rotation work?**

<details>
<summary><b>👀 Show Answer</b></summary>

KMS is a managed encryption key service. Key rotation automatically generates a new cryptographic key version once a year for AWS-managed keys.
- Historical data encrypted with older key versions can still be decrypted because KMS retains older versions to resolve decrypt operations automatically.

> 💡 **Interviewer Focus:** Cryptographic compliance configurations.

</details>

<hr/>

### ❓ Q41. **Explain the difference between EBS General Purpose SSD (gp2/gp3) and Provisioned IOPS SSD (io2).**

<details>
<summary><b>👀 Show Answer</b></summary>

- **gp2/gp3 (General Purpose):** Costs less. Balances price and performance. Baseline IOPS is 3,000 for gp3, scaling up to 16,000 IOPS based on capacity size.
- **io2 (Provisioned IOPS):** Designed for extreme I/O workloads (large SQL databases). Allows provisioning specific throughput and IOPS (up to 256,000 IOPS) independently of disk size, guaranteeing performance SLA.

> 💡 **Interviewer Focus:** Database storage tuning.

</details>

<hr/>

### ❓ Q42. **What is the role of an IAM Policy evaluation logic?**

<details>
<summary><b>👀 Show Answer</b></summary>

AWS evaluates policies using standard priority rules:
1. By default, all requests are denied.
2. An **explicit deny** in any policy overrides any allow permissions.
3. An **explicit allow** grants access only if no deny exists.
4. If no explicit allow exists, access is denied (implicit deny).

> 💡 **Interviewer Focus:** Explicit deny priority overrides.

</details>

<hr/>

### ❓ Q43. **What is AWS Lambda concurrency?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Reserved Concurrency:** Restricts the maximum number of concurrent instances allocated to a specific function. Useful to prevent Lambda from exhausting the regional pool, or to limit database connections.
- **Provisioned Concurrency:** Pre-warms instances to eliminate cold start latency.

> 💡 **Interviewer Focus:** Concurrency limit management.

</details>

<hr/>

### ❓ Q44. **What is the difference between Amazon EKS and Amazon ECS?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **ECS (Elastic Container Service):** AWS-native container orchestrator. Easy to integrate with other AWS services, has low complexity, and is ideal for standard Docker configurations.
- **EKS (Elastic Kubernetes Service):** Managed Kubernetes platform. Has higher complexity, but conforms to standard CNCF Kubernetes configurations, enabling multi-cloud deployments.

> 💡 **Interviewer Focus:** Cloud lock-in trade-offs vs open-standard container configurations.

</details>

<hr/>

### ❓ Q45. **What is a VPC peering connection?**

<details>
<summary><b>👀 Show Answer</b></summary>

A VPC peering connection is a 1-to-1 private network link between two VPCs. It allows instances in either VPC to communicate using private IP addresses as if they were on the same network. It is non-transitive.

> 💡 **Interviewer Focus:** VPC communication designs.

</details>

<hr/>

### ❓ Q46. **What is the function of the AWS EventBridge (CloudWatch Events)?**

<details>
<summary><b>👀 Show Answer</b></summary>

EventBridge is a serverless event bus service. It intercepts events from AWS services, custom SaaS applications, or cron schedules and routes them to target targets (Lambda, SQS) based on pattern matching rules.

> 💡 **Interviewer Focus:** Event-driven microservices decoupling.

</details>

<hr/>

### ❓ Q47. **How do you encrypt S3 buckets by default?**

<details>
<summary><b>👀 Show Answer</b></summary>

By enabling default bucket encryption. All incoming objects are automatically encrypted using Server-Side Encryption:
- **SSE-S3**: Keys managed by S3 (AES-256).
- **SSE-KMS**: Keys managed by KMS, allowing audit log tracking.

> 💡 **Interviewer Focus:** Data at rest compliance.

</details>

<hr/>

### ❓ Q48. **What is Amazon Cognito User Pools vs Identity Pools?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **User Pools:** Managed user directories handling authentication (sign-up, sign-in, MFA, token validation).
- **Identity Pools (Federated Identities):** Handles authorization. Authorizes users authenticated by User Pools or third-party providers (Google, Apple) to obtain temporary, limited AWS credentials to access resources directly (like S3 uploads).

> 💡 **Interviewer Focus:** AuthN (User Pools) vs AuthR (Identity Pools).

</details>

<hr/>

### ❓ Q49. **What does the TTL parameter do in DynamoDB?**

<details>
<summary><b>👀 Show Answer</b></summary>

The TTL (Time-To-Live) parameter automatically deletes items from a DynamoDB table after a defined Unix timestamp is reached. It runs as a background task at no extra charge, saving storage costs for temporary data.

> 💡 **Interviewer Focus:** Automating data pruning.

</details>

<hr/>

### ❓ Q50. **What is the difference between VPC Endpoint Interface vs Gateway?**

<details>
<summary><b>👀 Show Answer</b></summary>

Both route traffic privately inside AWS instead of exiting to the public internet:
- **Gateway Endpoints:** Free of charge. Modifies route tables. Supports *only* **S3** and **DynamoDB**.
- **Interface Endpoints (PrivateLink):** Charges per hour/GB. Allocates an Elastic Network Interface (ENI) with a private IP. Supports most other AWS services (ECR, KMS, SSM).

> 💡 **Interviewer Focus:** Eliminating NAT Gateway traffic costs.

</details>

<hr/>

## 🔴 Advanced Level

### ❓ Q51. **How do you design a highly available, fault-tolerant 3-Tier Web Architecture on AWS?**

<details>
<summary><b>👀 Show Answer</b></summary>

A 3-tier architecture splits the application into Web, Application, and Database layers across multiple AZs:
1. **Network Layer (VPC):** 
   - Deploy across 2 or 3 Availability Zones (AZs).
   - Create public subnets, private app subnets, and private database subnets in each AZ.
2. **Web/Presentation Tier:**
   - Deploy an **Application Load Balancer (ALB)** in the public subnets.
   - Configure Route 53 to route public traffic to the ALB.
   - Optional: CloudFront CDN in front of the ALB to cache static assets.
3. **Application Tier:**
   - Place EC2 instances (or ECS containers) in the private subnets for security.
   - Configure an **Auto Scaling Group (ASG)** to automatically scale instances based on CPU or request count.
   - Security: Restrict security groups to accept traffic *only* from the ALB.
4. **Database Tier:**
   - Deploy **Amazon RDS (Multi-AZ)** in the private database subnets. The primary database writes in AZ-1, and RDS replicates synchronously to a standby database in AZ-2.
   - Security: Database security group accepts traffic *only* from the Application Tier security group.

```
[Internet] ──> [Route 53] ──> [CloudFront]
                                  │
                           [Public Subnet]
                      [ALB (Multi-AZ Load Balancer)]
                                  │
                           [Private Subnet]
                    [ASG (EC2 App Servers in AZ-1 & AZ-2)]
                                  │
                      [Private Database Subnet]
                [RDS Primary (AZ-1)] <──(Sync)──> [RDS Standby (AZ-2)]
```

> 💡 **Interviewer Focus:** Restricting access using security group chaining (only allowing traffic from the immediate parent layer) and avoiding single points of failure.

</details>

<hr/>

### ❓ Q52. **What is Infrastructure as Code (IaC) and how does it compare to manual provisioning?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Infrastructure as Code (IaC):** The practice of provisioning and managing cloud infrastructure using configuration files (code) rather than manually click-configuring servers in the AWS Console.
- **Core Benefits:**
  - **Consistency:** Eliminates configuration drift (differences between dev, staging, and prod environments).
  - **Speed & Automation:** Infrastructure can be spun up or deleted automatically inside CI/CD pipelines.
  - **Version Control:** Infrastructure code can be reviewed, merged, and rolled back using Git.
- **Tools:**
  - **AWS CloudFormation:** AWS-native declarative JSON/YAML templates.
  - **Terraform:** Multi-provider, declarative HashiCorp Configuration Language (HCL) that maintains state files.
  - **AWS CDK (Cloud Development Kit):** Allows writing infrastructure using standard programming languages (TypeScript, Python, Go).

> 💡 **Interviewer Focus:** Managing state files in Terraform and resolving configuration drifts.

</details>

<hr/>

### ❓ Q53. **How do you secure data at rest and data in transit in AWS?**

<details>
<summary><b>👀 Show Answer</b></summary>

Security must be implemented at both layers:
- **Data in Transit:**
  - Encrypt all HTTP traffic using SSL/TLS.
  - Deploy SSL/TLS certificates on the Application Load Balancer (managed via **AWS Certificate Manager - ACM**).
  - Use VPNs or AWS Direct Connect for secure corporate-to-VPC traffic.
- **Data at Rest:**
  - Encrypt block storage (EBS) and databases (RDS, DynamoDB) at creation time using **AWS KMS** keys.
  - Encrypt S3 buckets using Default Server-Side Encryption (SSE-S3 or SSE-KMS).
  - Enable encryption in application code before writing sensitive data to storage.

> 💡 **Interviewer Focus:** Enforcing encryption standards using AWS Config rules and S3 Bucket Policies (denying requests without the `x-amz-server-side-encryption` header).

</details>

<hr/>

### ❓ Q54. **What is VPC Peering vs. AWS Transit Gateway?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **VPC Peering:**
  - A 1-to-1 private network connection between two VPCs.
  - Traffic travels over the private AWS network, not the public internet.
  - **Drawback:** Non-transitive. If VPC-A is peered with VPC-B, and VPC-B with VPC-C, VPC-A cannot talk to VPC-C without a direct peer link. Scaling this to dozens of VPCs results in a complex mesh network of links.
- **AWS Transit Gateway:**
  - Acts as a cloud router, connecting multiple VPCs and on-premise networks via a central hub.
  - Simpler hub-and-spoke architecture.
  - Fully transitive, scaling easily to thousands of VPC connections.

> 💡 **Interviewer Focus:** Scalability trade-offs. VPC Peering is cost-effective for small connections, while Transit Gateway is preferred for enterprise networks.

</details>

<hr/>

### ❓ Q55. **What is AWS KMS Envelope Encryption and how does it work?**

<details>
<summary><b>👀 Show Answer</b></summary>

Envelope encryption is the practice of encrypting plaintext data with a **Data Key**, and then encrypting the data key with a **Master Key** (Customer Master Key - CMK) managed in KMS.
- **Why it is used:** Encrypting large files directly with KMS API calls has network performance overhead and payload limits (max 4KB for KMS operations). Envelope encryption bypasses this.
- **Workflow:**
  1. The application requests a Data Key from KMS using the Master Key ID.
  2. KMS returns a plaintext Data Key and an encrypted Data Key.
  3. The application encrypts the file locally with the plaintext Data Key, then deletes the plaintext key from memory.
  4. The application stores the encrypted file along with the encrypted Data Key.
  5. **Decryption:** The application sends the encrypted Data Key back to KMS. KMS decrypts it using the Master Key and returns the plaintext Data Key, which the application uses to decrypt the file.

> 💡 **Interviewer Focus:** The security benefit of keeping master keys strictly within the HSM boundary of KMS.

</details>

<hr/>

### ❓ Q56. **Explain RDS Failover in Multi-AZ deployments.**

<details>
<summary><b>👀 Show Answer</b></summary>

In an RDS Multi-AZ deployment, RDS automatically provisions and maintains a synchronous standby replica in a different Availability Zone.
- **Failover Trigger:** If the primary database instance suffers an outage (hardware failure, AZ loss, network disruption), RDS initiates failover.
- **Under the hood:**
  - The standby replica is promoted to primary.
  - RDS updates the DNS record (CNAME) of the database endpoint to point to the new primary instance.
  - This DNS flip typically completes in 60-120 seconds.
  - Application connection pools must handle these transient drops and reconnect to the same database endpoint.

> 💡 **Interviewer Focus:** Understanding that failover is handled via DNS changes, which is why applications must use the database endpoint string rather than caching static IPs.

</details>

<hr/>

### ❓ Q57. **What is a Dead Letter Queue (DLQ) in AWS SQS/Lambda?**

<details>
<summary><b>👀 Show Answer</b></summary>

A DLQ is an SQS queue (or SNS topic) where message processing engines (like Lambda or SQS consumer threads) drop messages that fail processing after a set number of retries (e.g. 3 attempts).
- **Purpose:** Prevents blocking the main queue (poison pill messages) and allows developers to inspect failed payloads for debugging later.

> 💡 **Interviewer Focus:** Decoupled error handling and queue retry parameters tuning.

</details>

<hr/>

### ❓ Q58. **Compare S3 Object Lock vs S3 Versioning.**

<details>
<summary><b>👀 Show Answer</b></summary>

- **S3 Versioning:** Keeps historical versions of objects in the bucket, allowing recovery if objects are deleted or modified.
- **S3 Object Lock:** Implements WORM (Write Once, Read Many) compliance. It blocks deleting or overwriting objects for a defined retention period. Cannot be overridden even by root user credentials in Compliance Mode.

> 💡 **Interviewer Focus:** Regulatory compliance storage patterns.

</details>

<hr/>

### ❓ Q59. **Explain how Amazon ECS Fargate compares to standard EC2 launch types.**

<details>
<summary><b>👀 Show Answer</b></summary>

- **EC2 Launch Type:** You provision, patch, and manage the underlying EC2 instances running the container cluster. You control instance sizing and scaling.
- **Fargate Launch Type:** Serverless container execution. You define CPU and memory at the task level, and AWS dynamically allocates and manages the underlying host compute. No EC2 instances to manage.

> 💡 **Interviewer Focus:** Serverless container operations trade-offs (reduced administrative overhead vs slightly higher baseline compute costs).

</details>

<hr/>

### ❓ Q60. **What is AWS Global Accelerator?**

<details>
<summary><b>👀 Show Answer</b></summary>

Global Accelerator routes user traffic over AWS's private global fiber network instead of the public internet.
- **How it works:** Provides two static Anycast IP addresses globally. Traffic enters the nearest AWS Edge location and travels over the private network to the destination load balancer.
- **Benefit:** Reduces packet loss, lowers latency by up to 60%, and supports fast failover.

> 💡 **Interviewer Focus:** Optimizing global application routing.

</details>

<hr/>

### ❓ Q61. **Explain the difference between AWS WAF and AWS Shield.**

<details>
<summary><b>👀 Show Answer</b></summary>

- **AWS WAF (Web Application Firewall):** Operates at Layer 7 (Application). Inspects HTTP/HTTPS payloads to block SQL injection, cross-site scripting (XSS), or malicious bots using custom rules.
- **AWS Shield:** Operates at Layer 3/4 (Network). Protects AWS resources against volumetric DDoS attacks (Shield Standard is free; Shield Advanced provides dedicated support and cost protection).

> 💡 **Interviewer Focus:** Differentiating application filters from DDoS mitigation.

</details>

<hr/>

### ❓ Q62. **How does Amazon Aurora's storage architecture differ from standard RDS MySQL?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **RDS MySQL:** Uses standard EBS block storage. Replicates synchronously to one standby node in a different AZ (Multi-AZ).
- **Amazon Aurora:** Uses a shared log-structured storage virtualization layer. Aurora automatically replicates data across **3 Availability Zones** (writing 6 copies total). It separates compute and storage, allowing extremely fast failovers and up to 15 read replicas sharing the same storage layer.

> 💡 **Interviewer Focus:** Aurora storage virtualization benefits.

</details>

<hr/>

### ❓ Q63. **What is a NAT Instance vs a NAT Gateway?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **NAT Instance:** A standard EC2 instance configured to route traffic. Managed by the customer (software updates, instance scaling are your responsibility).
- **NAT Gateway:** A fully managed AWS service. Highly available, auto-scalable, and handles up to 45 Gbps of traffic without administration.

> 💡 **Interviewer Focus:** Managed services vs manual infrastructure administration.

</details>

<hr/>

### ❓ Q64. **Explain IAM Policy Evaluation Variables and Conditions.**

<details>
<summary><b>👀 Show Answer</b></summary>

IAM policies support `Condition` blocks to restrict access based on runtime variables (e.g., checking the requester's IP address, requiring Multi-Factor Authentication, or restricting access to specific time windows).

```json
"Condition": {
  "IpAddress": { "aws:SourceIp": "203.0.113.0/24" }
}
```

> 💡 **Interviewer Focus:** Fine-grained resource protection configurations.

</details>

<hr/>

### ❓ Q65. **What is AWS Organizations and Service Control Policies (SCPs)?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **AWS Organizations:** Allows consolidating and managing multiple AWS accounts under a single organization.
- **Service Control Policies (SCPs):** Guardrails that enforce maximum permission boundaries across accounts. Even if an account administrator has root access, an SCP can block them from performing specific API operations (e.g. deleting CloudTrail logs or creating resources outside specific regions).

> 💡 **Interviewer Focus:** Multi-account security compliance rules.

</details>

<hr/>

### ❓ Q66. **What is AWS EventBridge Schema Registry?**

<details>
<summary><b>👀 Show Answer</b></summary>

EventBridge Schema Registry stores structural event payloads schemas. It generates code bindings for Java, Python, or TypeScript, allowing developers to import event schemas directly into application code to enforce data types.

> 💡 **Interviewer Focus:** Managing event schemas in decoupled microservices.

</details>

<hr/>

### ❓ Q67. **How do you secure Amazon S3 buckets against accidental public exposure?**

<details>
<summary><b>👀 Show Answer</b></summary>

1. Enable **S3 Block Public Access (BPA)** at the bucket or account level.
2. Avoid using wildcard (`*`) Principals in bucket access policies.
3. Audit bucket policies regularly using **IAM Access Analyzer**.

> 💡 **Interviewer Focus:** S3 security best practices.

</details>

<hr/>

### ❓ Q68. **Explain the role of the VPC Flow Logs.**

<details>
<summary><b>👀 Show Answer</b></summary>

VPC Flow Logs capture network traffic statistics going to/from network interfaces (ENIs) inside your VPC. They record source/destination IPs, ports, protocols, and whether the packets were accepted or rejected by Security Groups/NACLs.

> 💡 **Interviewer Focus:** Diagnosing network routing and security block issues.

</details>

<hr/>

### ❓ Q69. **What is DynamoDB DAX (DynamoDB Accelerator)?**

<details>
<summary><b>👀 Show Answer</b></summary>

DAX is a fully managed, in-memory write-through cache for DynamoDB. It reduces read latency from single-digit milliseconds to microseconds for high-throughput, read-heavy tables.

> 💡 **Interviewer Focus:** Microsecond caching layers for NoSQL.

</details>

<hr/>

### ❓ Q70. **What are the differences between Spot, On-Demand, and Reserved instances?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **On-Demand:** Pay-per-second, flexible. No long-term commitments. Best for short-term, unpredictable workloads.
- **Spot:** Purchase unused EC2 capacity at up to 90% discount. AWS can terminate instances with a 2-minute warning if capacity is needed elsewhere. Best for stateless, batch processing.
- **Reserved Instances / Savings Plans:** Commit to a consistent usage limit for 1 or 3 years. Offers up to 72% discount. Best for steady-state workloads.

> 💡 **Interviewer Focus:** Cost optimization pricing models.

</details>

<hr/>

### ❓ Q71. **What is AWS Lambda Layers?**

<details>
<summary><b>👀 Show Answer</b></summary>

Lambda Layers package library dependencies, custom runtimes, or configurations separately from the main function deployment ZIP. Multiple Lambda functions can reference the same layer, reducing code package sizes.

> 💡 **Interviewer Focus:** Shared dependency management in serverless.

</details>

<hr/>

### ❓ Q72. **Explain how VPC endpoints save money compared to NAT Gateways.**

<details>
<summary><b>👀 Show Answer</b></summary>

NAT Gateways charge an hourly fee plus data processing rates per GB.
- If private instances access S3 or DynamoDB (transferring TBs of data), routing this traffic through the NAT Gateway incurs high data processing charges.
- Configuring a free **VPC Gateway Endpoint** routes all S3/DynamoDB traffic privately over the AWS internal network, bypassing the NAT Gateway and eliminating data processing charges.

> 💡 **Interviewer Focus:** NAT Gateway cost optimization under high traffic volumes.

</details>

<hr/>

### ❓ Q73. **What is a placement group in EC2?**

<details>
<summary><b>👀 Show Answer</b></summary>

Placement groups dictate physical EC2 instance distribution on hardware:
- **Cluster:** Places instances close together within a single AZ. Best for low-latency network performance (high-performance computing).
- **Spread:** Places instances on distinct physical hardware racks. Best for high availability (critical instances).
- **Partition:** Divides instances across logical partitions on distinct racks. Best for distributed workloads (Hadoop, Cassandra).

> 💡 **Interviewer Focus:** Custom hardware allocation.

</details>

<hr/>

### ❓ Q74. **What is AWS Snowball and Snowmobile?**

<details>
<summary><b>👀 Show Answer</b></summary>

Physical storage transfer devices used to migrate large volumes of data (TBs to PBs) to AWS, bypassing slow internet networks.
- **Snowball Edge:** A ruggedized suitcase-sized device (up to 80TB storage).
- **Snowmobile:** A shipping container pulled by a semi-trailer truck (up to 100PB storage).

> 💡 **Interviewer Focus:** Physical migration strategies for legacy datacenters.

</details>

<hr/>

### ❓ Q75. **Explain the purpose of the Amazon EBS CSI driver in Kubernetes.**

<details>
<summary><b>👀 Show Answer</b></summary>

The EBS Container Storage Interface (CSI) driver allows Kubernetes clusters running on Amazon EKS to manage the lifecycle of Amazon EBS volumes as persistent volumes for Kubernetes pods. It automatically attaches, mounts, and detaches EBS volumes dynamically based on Pod requirements.

> 💡 **Interviewer Focus:** Stateful workloads storage management in EKS.

</details>

<hr/>

## 🟣 Expert Level

### ❓ Q76. **Explain the AWS Well-Architected Framework and its 6 pillars.**

<details>
<summary><b>👀 Show Answer</b></summary>

The Well-Architected Framework provides architectural best practices for designing and operating reliable, secure, efficient, and cost-effective systems in the cloud.
- **The Six Pillars:**
  1. **Operational Excellence:** Running and monitoring systems to deliver business value, and continually improving processes (automation, game days).
  2. **Security:** Protecting information and systems (data encryption, least privilege, threat detection).
  3. **Reliability:** Ensuring workloads perform their intended functions correctly and consistently (fault tolerance, automated recovery, horizontal scaling).
  4. **Performance Efficiency:** Using IT and computing resources efficiently (selecting correct resource types based on workload demand).
  5. **Cost Optimization:** Avoiding unnecessary costs (understanding spending, selecting pricing models, sizing resources).
  6. **Sustainability:** Minimizing the environmental impacts of running cloud workloads (improving utilization, reducing waste).

> 💡 **Interviewer Focus:** Expecting the candidate to relate real-world architectural design decisions to these six pillars.

</details>

<hr/>

### ❓ Q77. **How do you design a Serverless, Event-Driven microservices architecture using API Gateway, Lambda, DynamoDB, SQS, and EventBridge?**

<details>
<summary><b>👀 Show Answer</b></summary>

An event-driven architecture handles transactions asynchronously using events:
1. **Request Ingestion:** The client calls an HTTPS endpoint on **API Gateway**.
2. **Synchronous Validation:** API Gateway triggers a **Lambda Authorizer** to authenticate the request, then forwards it to an ingestion **Lambda function**.
3. **Queueing (Decoupling):** The ingestion Lambda runs quick validation and drops the payload into an **SQS Queue**, immediately returning a `202 Accepted` response to the client. This handles huge traffic spikes without dropping requests.
4. **Asynchronous Processing:** SQS triggers a worker **Lambda function** in batches. The worker processes the business logic and saves the state in **DynamoDB**.
5. **Event Dispatching:** DynamoDB Streams captures the database write and triggers a stream Lambda, which publishes a domain event (e.g., `OrderPlaced`) to **Amazon EventBridge** (central event bus).
6. **Downstream Consumption:** EventBridge rules route the event to other microservices (like the Notification Service SQS queue or the Shipping Service) for decoupled parallel execution.

```
[Client] ──> [API Gateway] ──> [Ingestion Lambda]
                                    │
                               [SQS Queue]
                                    │
                               [Worker Lambda] ──> [DynamoDB]
                                                        │ (Streams)
                                                  [EventBridge]
                                             (Route to other services)
```

> 💡 **Interviewer Focus:** Asynchronous messaging benefits, error handling (DLQs), and avoiding synchronous API-to-API calls that cause cascading failures.

</details>

<hr/>

### ❓ Q78. **How do you optimize AWS costs for an enterprise infrastructure spending $100k+/month?**

<details>
<summary><b>👀 Show Answer</b></summary>

Cost optimization requires a multi-faceted approach:
1. **Analyze Usage:** Implement tag enforcement (allocation tags) and analyze spending using **AWS Cost Explorer** and **AWS Compute Optimizer**.
2. **Right-sizing compute:** Identify over-provisioned EC2 instances, RDS databases, or ECS tasks and scale them down to match actual CPU/Memory usage.
3. **Commitment Discounts:** Buy **Savings Plans** or **Reserved Instances** for stable, predictable workloads (up to 72% savings compared to On-Demand).
4. **Lifecycle Policies on S3:** Move raw data, audit logs, and older database backups from S3 Standard to Standard-IA and Glacier Deep Archive using S3 lifecycle rules.
5. **Manage NAT Gateways:** NAT Gateways charge per GB processed. Route internal AWS service traffic (like S3 or DynamoDB calls) through free **VPC Gateway Endpoints** instead of routing it through the NAT Gateway.
6. **Orphaned Resources:** Clean up detached EBS volumes, unused Elastic IPs, and old EBS snapshots.
7. **Spot Instances:** Run stateless, interruptible background workers or CI/CD agents on Spot Instances (up to 90% savings).

> 💡 **Interviewer Focus:** Practical familiarity with AWS Compute Optimizer recommendations, and S3 lifecycle storage calculations.

</details>

<hr/>

### ❓ Q79. **How does DynamoDB Partitioning and primary key design prevent hot partitions?**

<details>
<summary><b>👀 Show Answer</b></summary>

DynamoDB stores data in physical partitions. Each partition has limits: max 10GB size, 3,000 Read Capacity Units (RCUs), and 1,000 Write Capacity Units (WCUs).
- **The Hot Partition Problem:**
  - If your primary key design causes a high percentage of requests to target the same partition key value (e.g., querying an active tenant in a multi-tenant DB), that single partition will exceed its WCU/RCU limits, throwing `ProvisionedThroughputExceededException` (throttling), even if the overall table capacity is not exhausted.
- **Prevention Strategies:**
  - **Add a synthetic suffix (Write Sharding):** Append a random number suffix to the partition key (e.g., `tenant_123_0`, `tenant_123_1`) during writes to distribute the data across multiple partitions. Query them in parallel.
  - **Ensure High Cardinality:** Use composite keys like `userId` or `deviceId` rather than low-cardinality status flags.
  - **DynamoDB Adaptive Capacity:** DynamoDB automatically adjusts partitions and moves throughput allocations to busy partitions, but this takes time to adapt and should not replace solid schema design.

> 💡 **Interviewer Focus:** Architectural limits of DynamoDB partitions, and designing keys that scale throughput linearly.

</details>

<hr/>

### ❓ Q80. **Explain how global databases in Amazon Aurora and DynamoDB (Global Tables) handle latency and active-active writes.**

<details>
<summary><b>👀 Show Answer</b></summary>

- **DynamoDB Global Tables (Active-Active Multi-Region):**
  - Replicates data fully across multiple AWS Regions.
  - Applications can write to *any* regional replica with local latency.
  - Changes are replicated asynchronously to other regions (usually in under 1 second).
  - **Conflict Resolution:** Uses a "Last-Writer-Wins" policy based on timestamps. If two writes occur at the same millisecond in different regions, the last one wins. This can lead to silent updates and requires application-level care.
- **Amazon Aurora Global Databases (Active-Passive Multi-Region):**
  - Replicates data across regions with latency under 1 second using dedicated storage-level replication.
  - Only *one* region (the Primary Region) accepts writes. All other regions act as read replicas.
  - If the primary region fails, Route 53 failover can promote a secondary region to primary in under 1 minute.
  - Write forwarding allows secondary regions to accept write requests from local clients and automatically forward them to the primary region, though this adds network latency.

> 💡 **Interviewer Focus:** CAP Theorem trade-offs. The latency vs consistency dilemma of multi-region replication.

</details>

<hr/>

### ❓ Q81. **How do you implement zero-downtime blue-green deployments on AWS ECS (Fargate) using AWS CodeDeploy?**

<details>
<summary><b>👀 Show Answer</b></summary>

1. **Duplicate Tasks:** CodeDeploy spins up the new task version (Green tasks) alongside active stable tasks (Blue tasks) on ECS.
2. **Health Checking:** Green tasks register with a target group and run health checks.
3. **Route Traffic:** Once healthy, CodeDeploy modifies Application Load Balancer rules to route traffic to the Green target group.
4. **Evaluation:** Traffic is routed to Green. The deployment monitors CloudWatch Alarms for errors. If an alarm triggers, CodeDeploy rolls back instantly by shifting traffic back to the Blue target group.
5. **Dismantle:** If no alarms trigger after a defined termination window (e.g. 5 minutes), the old Blue tasks are terminated.

> 💡 **Interviewer Focus:** Automated rollbacks based on CloudWatch metrics alarms.

</details>

<hr/>

### ❓ Q82. **How do you implement disaster recovery strategies on AWS?**

<details>
<summary><b>👀 Show Answer</b></summary>

AWS supports four disaster recovery (DR) patterns balancing cost against Recovery Time Objective (RTO) and Recovery Point Objective (RPO):
- **Backup & Restore:** Regular data backups are stored (e.g. S3/snapshots). Low cost, but slow recovery time (high RTO).
- **Pilot Light:** Critical core services (like databases Multi-Region) are kept active and replicating, while compute resources (EC2/ASG) are scaled down to 0, ready to be scaled up on disaster.
- **Warm Standby:** A scaled-down but functional copy of the infrastructure runs in the secondary region, ready to scale to full capacity instantly.
- **Multi-Site Active-Active:** Full infrastructure runs in parallel in multiple regions, routing traffic globally. Zero RTO, but highest cost.

> 💡 **Interviewer Focus:** RTO/RPO trade-off calculations and cost analyses.

</details>

<hr/>

### ❓ Q83. **How do you secure VPC workloads against advanced data exfiltration using VPC Endpoints?**

<details>
<summary><b>👀 Show Answer</b></summary>

Workloads inside private subnets can exfiltrate data by writing to unauthorized public S3 buckets.
- **Prevention:**
  - Block access to the public internet via NAT Gateways.
  - Deploy a **VPC Endpoint** for S3.
  - Configure a **VPC Endpoint Policy** that denies access to all S3 buckets except those explicitly owned by the organization. This blocks data transfer to external personal accounts.

> 💡 **Interviewer Focus:** Designing endpoint policies to enforce strict data governance.

</details>

<hr/>

### ❓ Q84. **How does AWS Shield Advanced protect against DDoS attacks compared to Standard?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Shield Standard (Free):** Automatically protects all AWS customers against common Layer 3/4 DDoS attacks (SYN floods, UDP reflection).
- **Shield Advanced (Subscription):** Provides custom detection, real-time metrics dashboards, access to the DDoS Response Team (DRT) to write custom WAF rules during attacks, and **cost protection** to refund charges incurred from resource scaling spikes caused by DDoS traffic.

> 💡 **Interviewer Focus:** Enterprise-level DDoS mitigations.

</details>

<hr/>

### ❓ Q85. **Explain AWS Direct Connect vs Site-to-Site VPN.**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Site-to-Site VPN:** Connects corporate network to VPC over the public internet using IPsec. Fast setup, low cost, but bandwidth depends on public internet routing.
- **AWS Direct Connect:** Bypasses the internet entirely. Establishes a dedicated, physical fiber connection from corporate networks directly to AWS network routers. Guarantees extremely high bandwidth (1G to 100G) and stable network latency.

> 💡 **Interviewer Focus:** Private enterprise network topologies.

</details>

<hr/>

### ❓ Q86. **Explain the AWS Transit Gateway route table configuration at scale.**

<details>
<summary><b>👀 Show Answer</b></summary>

At scale, Transit Gateway utilizes separate route tables to enforce network isolation (e.g., placing Production, Staging, and Shared Services VPCs in separate tables).
- **Association:** A VPC attachment is associated with one Transit Gateway route table, determining where outbound traffic from that VPC can go.
- **Propagation:** Routes from VPC subnets are dynamically propagated into specific Transit Gateway route tables. This enables hub-and-spoke configurations with strict domain-isolation policies (e.g. blocking Staging from routing to Production, but allowing both to route to Shared Services).

> 💡 **Interviewer Focus:** Designing multi-tenant isolation patterns using routing domains.

</details>

<hr/>

### ❓ Q87. **What is VPC CIDR block optimization?**

<details>
<summary><b>👀 Show Answer</b></summary>

CIDR block optimization is the practice of carefully allocating IP address spaces (e.g. `/16` for VPC, split into `/24` or `/20` for subnets) to prevent IP exhaustion while avoiding overlapping CIDR blocks with on-premise networks or peered VPCs. Overlapping ranges prevent establishing VPC Peering or VPN connections.

> 💡 **Interviewer Focus:** Calculating subnet capacities and planning network topologies.

</details>

<hr/>

### ❓ Q88. **Explain the implementation of S3 Object Replication (CRR vs SRR).**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Cross-Region Replication (CRR):** Automatically, asynchronously copies S3 objects across buckets in different AWS Regions (for disaster recovery/compliance).
- **Same-Region Replication (SRR):** Replicates objects between buckets within the same AWS Region (useful for sharing data between dev/test accounts or logs consolidation).
- **Prerequisite:** S3 Versioning must be enabled on both source and destination buckets.

> 💡 **Interviewer Focus:** Versioning dependencies and replication status monitoring.

</details>

<hr/>

### ❓ Q89. **How do you diagnose EC2 CPU steal time metrics?**

<details>
<summary><b>👀 Show Answer</b></summary>

CPU Steal Time is the percentage of time a virtual machine (EC2 instance) wants CPU cycles, but the physical hypervisor host cannot allocate them because other co-located virtual machines on the same hardware are consuming the CPU resources.
- **Diagnosis:** Monitor `CPUSteal` metrics in CloudWatch. If high, it indicates a "noisy neighbor" issue on the shared physical host.
- **Resolution:** Restart the EC2 instance (which forces the hypervisor to launch it on a different physical host) or upgrade to dedicated instances.

> 💡 **Interviewer Focus:** Shared hypervisor virtualization resource constraints.

</details>

<hr/>

### ❓ Q90. **Explain how S3 Select and Glacier Select save application compute cost.**

<details>
<summary><b>👀 Show Answer</b></summary>

Standard S3 queries require downloading the entire object (e.g., a 10GB CSV file) to the application server before parsing and filtering it.
- **S3/Glacier Select:** Allows executing simple SQL queries (e.g., `SELECT * FROM S3Object WHERE age > 30`) directly at the S3 storage layer. S3 runs the query on the object and returns *only* the filtered rows, reducing network transit costs and application RAM overhead.

> 💡 **Interviewer Focus:** Offloading file parsing compute costs to S3.

</details>

<hr/>

### ❓ Q91. **What is AWS Outposts?**

<details>
<summary><b>👀 Show Answer</b></summary>

AWS Outposts is a fully managed service that delivers AWS physical hardware racks, APIs, and services directly to a customer's local on-premise data center. It allows running workloads locally for low latency or data residency requirements while managing them through the standard AWS Console.

> 💡 **Interviewer Focus:** Hybrid cloud infrastructure layouts.

</details>

<hr/>

### ❓ Q92. **How does Route 53 Geoproximity routing differ from Geolocation routing?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Geolocation Routing:** Routes traffic based on the geographic location of users (e.g., all users from Europe route to the Europe server).
- **Geoproximity Routing:** Routes traffic based on the physical distance of users to the nearest AWS resources. It supports **bias parameters** to expand or shrink the geographic reach of a specific regional server endpoint dynamically.

> 💡 **Interviewer Focus:** Geographic routing mechanisms.

</details>

<hr/>

### ❓ Q93. **What is DynamoDB transactional write limits?**

<details>
<summary><b>👀 Show Answer</b></summary>

DynamoDB `TransactWriteItems` operations can process up to **100** coordinated write actions (or up to 4MB of data total) in a single transaction. If any write in the transaction fails, the entire transaction is rolled back.

> 💡 **Interviewer Focus:** Transaction sizing limits in NoSQL databases.

</details>

<hr/>

### ❓ Q94. **Explain how Amazon RDS database encryption can be enabled on an existing unencrypted database.**

<details>
<summary><b>👀 Show Answer</b></summary>

You cannot enable encryption directly on an unencrypted RDS instance. The migration path is:
1. Take a snapshot of the unencrypted RDS instance.
2. Copy the snapshot, selecting the **Enable Encryption** option and choosing a KMS key.
3. Restore a new RDS instance from the encrypted snapshot copy.
4. Update the application connection strings to point to the new encrypted database instance.

> 💡 **Interviewer Focus:** Database encryption migration constraints.

</details>

<hr/>

### ❓ Q95. **What is AWS KMS Key Policies vs IAM Policies?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **KMS Key Policies:** Resource-based policies attached directly to a KMS key. Unlike other AWS resources, if a KMS key policy does not explicitly delegate access to the root account (`"Principal": { "AWS": "arn:aws:iam::account-id:root" }`), standard IAM policies in the account *cannot* grant access to the key.
- **IAM Policies:** Standard user/role policies. They only grant access to KMS keys if the key policy explicitly allows delegation to IAM.

> 💡 **Interviewer Focus:** KMS explicit key-policy delegation requirements.

</details>

<hr/>

### ❓ Q96. **How do you configure S3 Event Notifications to trigger Lambda functions asynchronously?**

<details>
<summary><b>👀 Show Answer</b></summary>

1. In the S3 Bucket configuration, add an **Event Notification** selecting the trigger event (e.g. `s3:ObjectCreated:*`).
2. Set the destination target to the target Lambda function.
3. **Important:** Add a permission policy on the Lambda function permitting the S3 service principal (`s3.amazonaws.com`) to invoke the function (`lambda:InvokeFunction`). Otherwise, S3 cannot trigger the Lambda.

> 💡 **Interviewer Focus:** Asymmetric service invocation permissions.

</details>

<hr/>

### ❓ Q97. **Explain how Aurora Serverless v2 scales CPU and RAM.**

<details>
<summary><b>👀 Show Answer</b></summary>

Aurora Serverless v2 scales compute capacity in fractions of seconds using **Aurora Capacity Units (ACUs)** (1 ACU represents 2GB of RAM and corresponding CPU).
- It monitors CPU, memory, and connection metrics in real-time, dynamically scaling the active capacity up or down (even mid-query) without dropping active connections.

> 💡 **Interviewer Focus:** Serverless database scaling latency.

</details>

<hr/>

### ❓ Q98. **What is the function of the AWS PrivateLink?**

<details>
<summary><b>👀 Show Answer</b></summary>

PrivateLink exposes application endpoints (SaaS services or VPC target groups) privately to external consumer VPCs without routing traffic over the public internet or requiring VPC peering.
- It maps the target service to an Elastic Network Interface (ENI) with a private IP inside the consumer subnet.

> 💡 **Interviewer Focus:** Exposing services privately across enterprise accounts.

</details>

<hr/>

### ❓ Q99. **How do you debug EBS volume I/O credit exhaustion?**

<details>
<summary><b>👀 Show Answer</b></summary>

EBS gp2 volumes rely on an I/O credit burst bucket model. If a database executes prolonged high writes, it depletes these credits.
- **Diagnosis:** Monitor `BurstBalance` metrics in CloudWatch. If it drops to `0%`, disk throughput drops to baseline speed, causing application database queries to lock.
- **Resolution:** Upgrade the volume to gp3 (which provides baseline 3,000 IOPS independently of size) or io2.

> 💡 **Interviewer Focus:** EBS burst mechanics.

</details>

<hr/>

### ❓ Q100. **Explain the concept of AWS Lambda runtime API under the hood.**

<details>
<summary><b>👀 Show Answer</b></summary>

When a Lambda container runs:
1. The bootstrap process calls the **Runtime API** HTTP endpoint (`/runtime/invocation/next`) hosted by the Lambda system.
2. The loop blocks until an event is returned.
3. The bootstrap processes the event payload and passes it to the handler function.
4. The handler returns the result, and the bootstrap calls `/runtime/invocation/response` (or `/error`) to submit the response before blocking again.

> 💡 **Interviewer Focus:** Low-level execution API loops in custom runtimes.

</details>

<hr/>

### 🧭 Navigation

| ⬅️ Previous | 🏠 Index | ➡️ Next |
| :--- | :---: | ---: |
| [⬅️ MongoDB](./09_MongoDB.md) | [Home](./00_Index.md) | [➡️ DevOps](./11_DevOps.md) |
