# 📌 Topic: Cloud Registries (ECR and GCR)

## 🧠 Concept Explanation (Basic → Expert)
**Basic**: Cloud Registries are image stores provided by AWS (ECR) and Google (GCR/Artifact Registry). They are better than Docker Hub for companies because they are more secure and closer to your servers.
**Expert**: Cloud Registries are **Managed OCI-Compliant Storage** services deeply integrated with the cloud's **Identity and Access Management (IAM)** system. Unlike Docker Hub, which uses simple usernames/passwords, ECR and GCR use temporary tokens generated from IAM roles. Staff-level engineering requires mastering **Cross-Account Access**, **Immutable Tag Enforcement**, and **Vulnerability Scanning Integration**. These registries also provide "Geo-replication," ensuring that your images are physically located in the same region as your compute (EC2/GKE) to minimize pull latency and cross-region data costs.

## 🏗️ Mental Model
- **Docker Hub**: A public library in the city center. Anyone can walk in, but it's far away.
- **ECR/GCR**: A private, high-security library inside your own office building. Only employees with the right badge (IAM Role) can enter, and it's right next to your desk.

## ⚡ Actual Behavior
- **Zero-Config Auth**: If you run a container on AWS ECS, you don't need to `docker login`. The ECS agent automatically uses the EC2's IAM role to pull from ECR.
- **Lifecycle Policies**: You can set a rule like "Keep only the 10 most recent images" to avoid paying for thousands of old, useless builds.

## 🔬 Internal Mechanics (IAM Integration)
1. **The Token**: The CLI runs `aws ecr get-login-password`. This calls the AWS API and returns a JWT token valid for 12 hours.
2. **The Pull**: When `docker pull` runs, it sends this token in the `Authorization` header.
3. **The Verification**: The Registry service verifies the token against the IAM policy.
4. **The Policy**: You can grant "Read-only" access to your Production servers and "Full" access to your Jenkins server.

## 🔁 Execution Flow (The AWS ECR Push)
1. `aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <id>.dkr.ecr.us-east-1.amazonaws.com`.
2. `docker tag my-app:latest <id>.dkr.ecr.us-east-1.amazonaws.com/my-repo:v1`.
3. `docker push <id>.dkr.ecr.us-east-1.amazonaws.com/my-repo:v1`.
4. ECR receives the layers, stores them in S3, and triggers a vulnerability scan.

## 🧠 Resource Behavior
- **Cost**: You pay for **Storage** (GB/month) and **Data Transfer** (only when pulling *outside* the cloud region). Pulling within the same region is usually free.
- **Performance**: Near-instant pulls (100MB/s+) because the image is traveling over the cloud's internal high-speed backbone.

## 📐 ASCII Diagrams (REQUIRED)

```text
       CLOUD REGISTRY SECURITY MODEL
       
[ Jenkins / CI ]         [ AWS ECR ]         [ EC2 / ECS ]
       |                      |                    |
 (1) Get Token <----------( IAM ) ----------> (3) Auth Pull
       |                      |                    |
 (2) Push Image ------------> | <------------------+
                              |
                     [ Scanning / Policy ]
```

## 🔍 Code (ECR Lifecycle Policy)
```json
// Example: Keep only 30 images, delete untagged ones after 1 day
{
  "rules": [
    {
      "rulePriority": 1,
      "description": "Expire untagged images",
      "selection": {
        "tagStatus": "untagged",
        "countType": "sinceImagePushed",
        "countUnit": "days",
        "countNumber": 1
      },
      "action": { "type": "expire" }
    },
    {
      "rulePriority": 2,
      "description": "Keep last 30 tagged images",
      "selection": {
        "tagStatus": "tagged",
        "tagPrefixList": ["v"],
        "countType": "imageCountMoreThan",
        "countNumber": 30
      },
      "action": { "type": "expire" }
    }
  ]
}
```

## 💥 Production Failures
- **The "Token Expired" Build**: A long-running Jenkins job performs a `docker login` at the start. 13 hours later, it tries to push a large image. The push fails because the ECR token expired (12-hour limit).
  *Fix*: Always refresh the login token immediately before the push command.
- **Cross-Account Denied**: Your ECR is in the "Security" account, but your ECS is in the "Prod" account. The pull fails because the ECR **Repository Policy** (separate from IAM) doesn't explicitly allow the Prod account ID.

## 🧪 Real-time Q&A
**Q: Is GCR different from Artifact Registry?**
**A**: Yes. **GCR (Google Container Registry)** is the older version based on Google Cloud Storage. **Artifact Registry** is the newer, more powerful version that supports not just Docker images, but also NPM, Python, and Java packages in one place. You should use Artifact Registry for all new projects.

## ⚠️ Edge Cases
- **VPC Endpoints**: If your EC2 instances are in a "Private Subnet" with no internet access, they cannot reach ECR unless you create an **Interface VPC Endpoint**.

## 🏢 Best Practices
- **Enable Scan on Push**: It's free or very cheap and catches security holes early.
- **Use Immutable Tags**: Prevents a developer from "fixing" `v1.0` by pushing a new image to the same tag. Use `v1.0.1` instead.
- **Repository Policies**: Use them to restrict access to specific IP ranges or VPCs for maximum security.

## ⚖️ Trade-offs
| Feature | Docker Hub | AWS ECR |
| :--- | :--- | :--- |
| **Auth** | User/Pass | **IAM Roles** |
| **Latency** | Medium | **Very Low** |
| **Integration** | Low | **High (ECS/EKS)** |
| **Scanning** | Basic | **Advanced (Clair/Amazon)**|

## 💼 Interview Q&A
**Q: Why would a company prefer AWS ECR over Docker Hub?**
**A**: 1. **Security**: ECR integrates with AWS IAM, allowing for granular permissions based on roles rather than shared credentials. 2. **Performance**: Pulling images within the same AWS region is significantly faster and doesn't incur data egress charges. 3. **Compliance**: ECR offers built-in vulnerability scanning and immutable tags, which are essential for meeting security standards. 4. **Reliability**: Using a managed service within your own cloud ecosystem reduces the number of external dependencies that can fail during a deployment.

## 🧩 Practice Problems
1. Create an ECR repository and push an image manually using the AWS CLI.
2. Set an "Immutable Tag" policy and try to push a different image to the same tag. Observe the error.
3. Configure a "Lifecycle Policy" to automatically delete images that don't start with the prefix `release-`.

---
Prev: [03_Pull_Through_Caching.md](./03_Pull_Through_Caching.md) | Index: [00_Index.md](../00_Index.md) | Next: [05_Content_Trust_and_Signing.md](./05_Content_Trust_and_Signing.md)
---
