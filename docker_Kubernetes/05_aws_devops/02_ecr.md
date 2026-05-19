# Ecr

## Why This Exists
Once you build a Docker image, you need a safe place to store it so your servers can download (pull) and run it. Docker Hub is great, but it's public. If your image contains proprietary company code, you need a private vault. ECR (Elastic Container Registry) is a highly secure, private Docker registry built directly into AWS.

## Real World Analogy
Think of a **Secure Parking Garage for Food Trucks**. 
You build your custom food truck (Docker Image) in your driveway. You can't just leave it parked on a public street (Docker Hub) where anyone could look inside or steal it. You drive it into a highly secure, private parking garage (ECR). Only authorized company drivers (your EC2 or EKS servers) are given the badge to enter the garage, take the truck out, and start serving food.

## Core Concepts
*   **Registry:** Your AWS account's main container storage area.
*   **Repository:** A specific folder inside the registry for one application (e.g., `my-frontend-app`).
*   **Image Tags:** Versions of your image (e.g., `v1.0`, `latest`, `commit-8f3a2b`).
*   **IAM Integration:** Access to ECR is strictly controlled by AWS IAM (Identity and Access Management).

## Architecture / Flow
1. Developer finishes writing code and runs `docker build -t my-app .` on their laptop.
2. Developer authenticates their local Docker client with AWS ECR.
3. Developer tags the image with the ECR URL.
4. Developer runs `docker push`. The image uploads to the AWS vault.
5. In production, an Amazon EKS cluster connects to ECR, pulls that exact image, and runs it.

## Practical Commands
*   `aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.us-east-1.amazonaws.com` - Logs you in.
*   `aws ecr create-repository --repository-name my-app` - Creates a new repo.
*   `docker push <aws_account_id>.dkr.ecr.us-east-1.amazonaws.com/my-app:v1`

## Hands-On Exercise
Create a repository in ECR using the AWS Console. On your local machine, pull a tiny public image like `alpine`. Tag it with your ECR repository URL, log in using the AWS CLI, and push the image to your private ECR.

## Mini Project
**"Automated Build Script"**
Write a simple bash script called `deploy.sh`. The script should take a version number as an argument, build a Dockerfile in the current directory, tag it with that version number, log into ECR, and push the image.

## Real Production Usage
ECR is the central nervous system of any AWS container deployment. CI/CD pipelines (like GitHub Actions) are configured to automatically build and push every new code commit to ECR. If a new deployment crashes the site, engineers can instantly tell K8s to pull the previous image from ECR to roll back.

## Common Mistakes
*   **Paying for Junk:** Docker images are large. If your CI/CD pipeline pushes a 1GB image 10 times a day, you will quickly rack up huge storage costs. You MUST configure "Lifecycle Policies" to automatically delete images older than 30 days.
*   **Hardcoding Credentials:** Never hardcode AWS access keys in a CI/CD pipeline just to push to ECR. Use secure methods like OIDC (OpenID Connect).

## Debugging Guide
*   **`no basic auth credentials` error during push?** Your local Docker daemon is not authenticated. You must run the `aws ecr get-login-password` command first. Remember, this login token expires every 12 hours!
*   **EKS pod says `ImagePullBackOff`?** The Kubernetes cluster's worker nodes probably don't have the IAM permission `AmazonEC2ContainerRegistryReadOnly` attached to them.

## Best Practices
*   **Enable Image Scanning:** ECR has a feature to scan your images for known security vulnerabilities (CVEs) every time you push. Turn this on!
*   **Immutable Tags:** Turn on "Tag Immutability" so someone can't accidentally overwrite `v1.0` with a completely different image, which could break production without changing the version number.

## Interview Questions
*   **Q: How do you secure images stored in ECR?**
    *   *A: Through IAM policies governing who can push/pull, enabling encryption at rest using KMS keys, and utilizing automated image scanning for vulnerabilities.*

## Summary
ECR removes the headache of hosting your own private Docker registry. It seamlessly bridges the gap between your local development/build process and your secure AWS production environments.

---
Prev: [01_ec2.md](./01_ec2.md) | Index: [Index](../00_index.md) | Next: [03_eks.md](./03_eks.md)
