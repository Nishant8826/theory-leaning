# Elastic Container Registry (ECR)

## What Is This Service?
Amazon Elastic Container Registry (ECR) is a fully managed container registry that makes it easy to store, manage, share, and deploy your container images and artifacts.

## Why This Service Exists
Once you build a Docker image for your Next.js or Express app, you need a secure, private place to store it so your production servers (ECS/EKS) can download it. While Docker Hub is popular, using ECR keeps your private company code inside the AWS network, offering vastly superior security, speed, and IAM integration.

## Real World Analogy
ECR is the **Private Warehouse** for your shipping containers.
You build your shipping container (Docker Image) at the factory (your laptop/CI pipeline). You drive it to the secure ECR Warehouse to store it. Later, the delivery trucks (ECS/EKS) pull up to the warehouse to pick up the container and take it to the store (Production).

## How It Works
ECR provides Docker CLI-compatible endpoints. You authenticate your local Docker CLI with AWS using an IAM token, then use standard `docker push` commands to upload your image. ECS and EKS have native integration to perform `docker pull` securely from ECR using IAM Roles.

## Core Concepts
- **Repository**: A collection of related images (e.g., one repository for `mern-backend`, one for `nextjs-frontend`).
- **Image Tags**: Labels to identify specific versions of an image (e.g., `v1.0.0`, `latest`, or a Git commit hash `a1b2c3d`).
- **Image Scanning**: ECR can automatically scan your Node.js container images for known vulnerabilities (CVEs) as soon as they are pushed.

## MERN Stack Integration
When deploying a full-stack containerized MERN app, you will typically create two ECR repositories:
1. `my-app/nextjs-frontend`
2. `my-app/express-backend`
Your CI/CD pipeline builds both images, tags them with the GitHub commit hash, and pushes them to their respective ECR repositories.

## Production Impact
- **Deployment Reliability**: ECR is highly available. If Docker Hub goes down, you can't deploy. ECR ensures your deployment pipeline always has access to your images.
- **Speed**: Pulling an image from ECR to an EC2 instance in the same AWS Region takes seconds because the traffic never leaves the high-speed AWS backbone network.

## Real Production Use Cases
- A GitHub Actions CI/CD pipeline automatically triggers when code is merged to `main`. It builds the Next.js Docker image, logs into ECR using temporary OIDC credentials, and pushes the image. ECS then pulls this new image to update the live website.

## Production Best Practices
- **Never use the `latest` tag**: Always tag your images with a unique identifier like the Git commit SHA (e.g., `api:9f8a7b6`). If you just use `latest`, rolling back to a previous version is incredibly difficult because you don't know which code is inside the `latest` image.
- **Lifecycle Policies**: Container images are large. Set an ECR Lifecycle Policy to automatically delete untagged images or images older than 90 days to save storage costs.

## Security Best Practices
- **Vulnerability Scanning**: Enable "Scan on Push". If ECR detects that your `node:18` base image has a critical OpenSSL vulnerability, it will alert you immediately so you can patch it before deployment.
- **Cross-Account Access**: If you use a central AWS account for CI/CD and a separate account for Production, use ECR Resource Policies to securely grant the Prod account `ecr:BatchGetImage` permissions.

## Cost Optimization Tips
- ECR charges $0.10 per GB per month for storage. Without a lifecycle policy, your CI/CD pipeline pushing a 500MB image 10 times a day will quickly bloat your AWS bill with terabytes of obsolete images.

## Common Mistakes
- Trying to pull an ECR image from an EC2 instance that doesn't have an IAM Role with `AmazonEC2ContainerRegistryReadOnly` permissions. The pull will fail with an authentication error.

## Debugging & Troubleshooting
- **Docker Login Fails**: The AWS CLI login command requires valid AWS credentials. Ensure your CLI profile is configured correctly and your IAM user has `ecr:GetAuthorizationToken` permissions.
- **Cannot Pull Image**: Ensure the ECS Task Execution Role has the correct ECR permissions to pull the image.

---
Prev : [./01_Docker_on_AWS.md](./01_Docker_on_AWS.md) | Index : [../00_Index.md](../00_Index.md) | Next : [./03_ECS_Deep_Dive.md](./03_ECS_Deep_Dive.md)
---
