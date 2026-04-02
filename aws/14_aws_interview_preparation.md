# Interview Preparation: AWS DevOps & Cloud Engineering

---

### 2. What
AWS is the industry leader in Cloud Computing. Most mid-to-senior Full Stack and DevOps engineering interviews heavily feature scenario-based AWS questions testing your logic regarding Compute scaling, VPC networking, and Data Storage architecture.

---

### 3. Why
Memorizing vocabulary is not enough. Interviewers want to see how you piece services together. If they ask you to host a React app, responding with "EC2" is a technical fail. You must understand the cost patterns and architectural benefits of combining S3 + CloudFront + Route53.

---

### 4. How
Focus on the trifecta: **Compute** (EC2, Lambda, ECS), **Storage/Databases** (S3, RDS, DynamoDB), and **Networking** (VPC, ASG, Load Balancers).

---

### 5. Implementation
No actual code. Prepare mentally for these architectural flows.

---

### 6. Steps (Approaching Scenario Questions)
1. Identify if the application is static or server-based.
2. Determine if the database requires rigid relationships (RDS) or extreme scale (DynamoDB).
3. Always mention separating the architecture across multiple Availability Zones for fault tolerance.

---

### 7. Integration

🧠 **Think Like This:**
When building an architecture block diagram in a whiteboard interview:
* Place **CloudFront** and the **Load Balancer** on the public edge.
* Place **EC2/Node.js** servers in a private network scaling group.
* Place the **RDS Database** in the deepest, securest isolated database subnet.

---

### 8. Impact
📌 **Real-World Scenario:** By explaining that an EC2 instance operates ephemerally, you show the interviewer that you understand that servers randomly crash. Demonstrating that you would store uploaded user files in S3 rather than the local EBS drive proves you know how to build a resilient, scalable, production-grade cloud structure.

---

### 9. Interview Questions

Q1. Elaborate on the structural difference between AWS EC2 and AWS Lambda.
Answer: EC2 provides virtual machine servers that require manual operating system patching and scaling, billing you by the hour. Lambda is a Serverless function orchestrator that executes code purely on-demand, billing by the millisecond with zero server maintenance.

Q2. Compare S3, EBS, and EFS.
Answer: S3 is an object storage service accessed via HTTP URLs over the internet. EBS is a block storage virtual hard drive attached to a single EC2 instance. EFS is an elastic file system designed to be mounted concurrently across multiple EC2 instances similar to a massive NAS drive.

Q3. Scenario: You are building an enterprise e-commerce platform. A cluster of EC2 instances runs the frontend API. How do you ensure the API survives if an entire AWS Data Center loses power?
Answer: Deploy the EC2 instances inside an Auto Scaling Group that provisions spanning servers across at least three distinct Availability Zones within the region, placing a unified Application Load Balancer in front of them to route traffic evenly around the dead zone.

Q4. Scenario: A developer accidentally pushes an AWS Root Access Key to a public GitHub repository. What steps must you immediately perform to triage?
Answer: First, log into the AWS Console and permanently delete or deactivate the compromised Access Key ID. Second, inspect AWS CloudTrail logs to identify exactly what malicious API calls the attacker performed while the key was active.

Q5. Why decouple a single-page React Application from its Node.js backend entirely when deploying to AWS?
Answer: Decoupling allows the static React frontend to be hosted Serverlessly and infinitely cheaply using S3 and CloudFront, reducing the compute load strictly to API logic handled separately on EC2 or Lambda.

Q6. Explain the purpose and benefit of Amazon CloudFront in a global application.
Answer: CloudFront is a Content Delivery Network that pulls your primary data from its origin server and caches it at localized Edge locations worldwide, ensuring a user in Japan downloads the site instantly from Tokyo instead of waiting for a packet roundtrip to Virginia.

---

### 10. Summary
* Study the "Serverless" architecture specifically (S3, CloudFront, Lambda, DynamoDB).
* Understand VPC network boundaries and isolated subnets.
* Always prioritize high availability using Multi-AZ deployments.
* Rely on CloudWatch and Auto Scaling Groups for intelligent infrastructure response.

---
Prev : [13_best_practices_security_cost.md](./13_best_practices_security_cost.md) | Next : None (End of Guide)
