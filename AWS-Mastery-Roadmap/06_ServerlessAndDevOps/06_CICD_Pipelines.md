# CI/CD Pipelines

## What Is This Service?
CI/CD (Continuous Integration / Continuous Deployment) is the practice of automating the integration of code changes and the deployment of applications to infrastructure (like AWS). Common tools include GitHub Actions, AWS CodePipeline, and GitLab CI.

## Why This Service Exists
Manually building a React app (`npm run build`), logging into the AWS Console, and dragging/dropping the files into an S3 bucket is tedious and error-prone. CI/CD exists to completely automate this. You push code to GitHub; the pipeline automatically tests it, builds it, and deploys it to AWS without any human intervention.

## Real World Analogy
CI/CD is the **Automated Assembly Line** in a car factory.
Instead of a mechanic building a car by hand and driving it to the dealership (manual deployment), the assembly line automatically welds the parts, tests the engine, paints the car, and puts it on a delivery truck the moment the raw materials arrive.

## How It Works (GitHub Actions to AWS)
1. You create a `.yml` workflow file in `.github/workflows/`.
2. When you `git push` to the `main` branch, GitHub provisions a temporary Linux server (runner).
3. The runner checks out your code and installs Node.js.
4. **CI (Continuous Integration)**: The runner runs `npm test` and `npm run lint` to ensure the code isn't broken.
5. **CD (Continuous Deployment)**: The runner authenticates with AWS, builds the Docker image, pushes it to ECR, and tells ECS to update the service.

## Core Concepts
- **Continuous Integration**: The process of automatically merging code and running automated tests.
- **Continuous Deployment**: The process of automatically releasing the tested code to production.
- **OIDC (OpenID Connect)**: A secure protocol allowing GitHub Actions to authenticate with AWS without using hardcoded, long-lived Access Keys.

## Hands-On Setup (React to S3 via GitHub Actions)
1. Create `.github/workflows/deploy.yml` in your React repo.
```yaml
name: Deploy React to S3
on:
  push:
    branches: [ "main" ]
jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm install && npm run build
      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-region: us-east-1
          role-to-assume: arn:aws:iam::123456789012:role/GitHubActionsS3Role
      - run: aws s3 sync build/ s3://my-react-bucket --delete
```
2. Push to GitHub and watch it deploy.

## MERN Stack Integration
- **Frontend**: CI/CD runs `npm run build`, syncs the output to S3, and creates a CloudFront Invalidation so users see the new site immediately.
- **Backend**: CI/CD runs Jest tests against the Express routes, builds a new Docker image, pushes to ECR, and updates the ECS Fargate service.

## Production Impact
- **Velocity**: Developers can deploy changes to production 10 times a day safely, drastically speeding up feature releases.
- **Reliability**: Because the pipeline runs automated tests *before* deploying, broken code never makes it to the production servers.

## Real Production Use Cases
- A developer accidentally pushes a syntax error in an Express route to GitHub. The CI pipeline runs `npm test`, the tests fail, and the pipeline halts. AWS is never updated, preventing the production API from crashing.

## Production Best Practices
- **Never use Long-Lived AWS Credentials**: Storing `AWS_ACCESS_KEY_ID` in GitHub Secrets is a major security risk. Use AWS OIDC integration so GitHub Actions can dynamically assume an IAM Role and get temporary 1-hour credentials.
- **Environment Separation**: Configure pipelines to deploy the `develop` branch to a Staging AWS environment, and require a manual approval step before deploying the `main` branch to Production.

## Security Best Practices
- Only grant the CI/CD IAM Role the absolute minimum permissions needed. If it deploys to S3, it only needs `s3:PutObject`. It should not have full EC2 access.

## Cost Optimization Tips
- Running heavy Docker builds in CI pipelines consumes minutes. If you are using GitHub Actions, cache your `node_modules` and Docker layers to speed up the build time and save on CI compute costs.

## Common Mistakes
- **No Rollback Strategy**: Assuming every deployment will succeed. Always ensure your Terraform state or ECS Task Definitions are versioned so you can click "Revert" in GitHub and instantly redeploy the previous working version if a bug sneaks through.

## Debugging & Troubleshooting
- **Pipeline Fails on Deployment**: If the AWS CLI step fails with `AccessDenied`, the IAM Role attached to the GitHub Action via OIDC is missing the required permissions to perform that specific AWS action.

---
Prev : [./05_Terraform_Basics.md](./05_Terraform_Basics.md) | Index : [../00_Index.md](../00_Index.md) | Next : None
---
