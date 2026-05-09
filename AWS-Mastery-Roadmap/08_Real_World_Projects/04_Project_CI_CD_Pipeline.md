# Project 4: CI/CD Pipeline for MERN Stack

## What Is This Project?
This project automates the deployment of your MERN application. We will use GitHub Actions to create a CI/CD pipeline that automatically builds the React frontend, syncs it to S3, builds the Node.js Docker image, pushes it to ECR, and updates the ECS Fargate cluster—all triggered simply by pushing code to the `main` branch.

## Why Do This Project?
Manual deployments are slow, error-prone, and unscalable. A robust CI/CD pipeline guarantees that every code change is tested, compiled, and safely delivered to production users in minutes, empowering development teams to ship features faster.

## How to Build It (Step-by-Step)

### Step 1: Configure AWS OIDC (Security First)
*Do NOT generate static IAM Access Keys.*
1. In the AWS Console, go to **IAM** > **Identity providers** > **Add provider**.
2. Select **OpenID Connect**.
   - Provider URL: `https://token.actions.githubusercontent.com`
   - Audience: `sts.amazonaws.com`
3. Click **Get thumbprint** and Add.
4. Go to **IAM Roles** > Create Role > Web identity.
5. Select the GitHub OIDC provider.
6. Create an inline policy allowing `s3:PutObject` (for the frontend bucket), `ecr:CompleteLayerUpload` (for ECR), and `ecs:UpdateService` (for ECS).
7. Name the role `GitHubActions-MERN-Deploy-Role` and copy its ARN.

### Step 2: Create the GitHub Actions Workflow File
In your MERN repository, create a directory `.github/workflows/` and add a file named `deploy.yml`.

### Step 3: Write the Frontend Deployment Job
Inside `deploy.yml`, define the pipeline trigger and the frontend deployment logic:

```yaml
name: Production Deployment

on:
  push:
    branches:
      - main

permissions:
  id-token: write # Required for AWS OIDC
  contents: read

jobs:
  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install and Build React
        working-directory: ./frontend
        run: |
          npm install
          npm run build

      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          role-to-assume: arn:aws:iam::123456789012:role/GitHubActions-MERN-Deploy-Role
          aws-region: us-east-1

      - name: Sync to S3
        working-directory: ./frontend
        run: aws s3 sync build/ s3://my-mern-frontend --delete
```

### Step 4: Write the Backend Deployment Job
Append the backend deployment logic to the same `deploy.yml` file under the `jobs` section:

```yaml
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v3

      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          role-to-assume: arn:aws:iam::123456789012:role/GitHubActions-MERN-Deploy-Role
          aws-region: us-east-1

      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v1

      - name: Build, tag, and push image to Amazon ECR
        working-directory: ./backend
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          ECR_REPOSITORY: mern-api
          IMAGE_TAG: ${{ github.sha }}
        run: |
          docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG

      - name: Force ECS Update
        run: |
          aws ecs update-service --cluster Mern-Cluster --service mern-api-service --force-new-deployment
```

### Step 5: Test the Pipeline
1. Commit the `.github/workflows/deploy.yml` file.
2. Run `git push origin main`.
3. Go to your GitHub repository > **Actions** tab.
4. Watch the pipeline authenticate securely with AWS, build the React app, sync to S3, build the Docker image, and restart the ECS service automatically.

## Production Impact
- **Security Auditing**: Because we used OIDC, AWS CloudTrail logs will show that the temporary token was generated explicitly by the GitHub Actions runner for a specific repository and commit hash.
- **Rollbacks**: The backend image is tagged with `${{ github.sha }}` (the unique commit hash) instead of `latest`. If a bug is deployed, you can instantly revert to the previous commit hash in ECS without needing to rebuild the image.

## Knowledge Transfer (KT)
- **Why `--force-new-deployment`?** In this simple pipeline, we didn't update the ECS Task Definition JSON with the new image tag. By using `--force-new-deployment`, ECS pulls the `latest` tag from ECR. In a true enterprise environment, the CI pipeline generates a new Task Definition Revision pointing to the exact `IMAGE_TAG` and registers it with ECS for absolute immutability.
- **CloudFront Invalidation**: For the frontend, syncing to S3 isn't enough because CloudFront caches the old files. In a real pipeline, you would add a step: `aws cloudfront create-invalidation --distribution-id XXXX --paths "/*"` to clear the cache instantly.

---
Prev : [./03_Project_MERN_on_EKS.md](./03_Project_MERN_on_EKS.md) | Index : [../00_Index.md](../00_Index.md) | Next : [./05_Project_Custom_VPC_Networking.md](./05_Project_Custom_VPC_Networking.md)
---
