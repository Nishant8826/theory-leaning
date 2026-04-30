# 🚀 CI/CD Pipelines

## 📌 Topic Name
Continuous Integration and Deployment: CodePipeline, CodeBuild, and CodeDeploy

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Automate the process of testing and deploying your code.
*   **Expert**: CI/CD is a **Software Supply Chain** that transforms source code into a running application with zero human intervention. It involves **Source Control (CodeCommit/GitHub)**, **Build & Test (CodeBuild)**, and **Deployment (CodeDeploy/CodePipeline)**. A Staff engineer designs pipelines that are **Idempotent**, **Versioned (Pipeline-as-Code)**, and include **Automated Rollbacks** and **Security Scanning**.

## 🏗️ Mental Model
Think of CI/CD as an **Automated Car Assembly Line**.
- **Source**: The raw materials (Steel, Glass, Code).
- **Build**: Stamping the steel into parts and testing them (Compiling, Unit Tests).
- **Staging**: Assembling the car and test-driving it on a private track (Integration Tests).
- **Production**: Delivering the car to the customer's driveway (Deployment).
If any step fails, the assembly line stops immediately.

## ⚡ Actual Behavior
- **CodePipeline**: The orchestrator. It listens for changes and moves data through "Stages."
- **CodeBuild**: A serverless build service. It spins up a temporary Docker container, runs your `buildspec.yml`, and then disappears.
- **CodeDeploy**: Handles the actual deployment to EC2, Lambda, or ECS. It supports advanced patterns like Blue-Green and Canary.

## 🔬 Internal Mechanics
1.  **Artifact S3 Bucket**: CodePipeline stores the output of each stage (the "Artifact") in an encrypted S3 bucket. Each subsequent stage pulls the artifact from this bucket.
2.  **Buildspec.yml**: The core configuration for CodeBuild. It defines phases (Install, Pre-build, Build, Post-build) and the commands to run.
3.  **Appspec.yml**: The configuration for CodeDeploy. It defines where files go and which "Lifecycle Hooks" (e.g., `AfterInstall`, `ValidateService`) to run.

## 🔁 Execution Flow (Pipeline Run)
1.  **Source**: Developer pushes to GitHub. GitHub sends a Webhook to CodePipeline.
2.  **Build**: CodePipeline triggers CodeBuild. CodeBuild pulls the source, runs `npm install`, `npm test`, and `npm run build`. It uploads the zip to S3.
3.  **Approval**: (Optional) A manual approval step sends a notification to an admin.
4.  **Deploy**: CodeDeploy pulls the zip and performs a rolling update on an ECS cluster.

## 🧠 Resource Behavior
- **Serverless Build**: CodeBuild is billed by the minute. You don't manage any build servers.
- **VPC Support**: Both CodeBuild and CodeDeploy can run inside your VPC if they need to access private resources (like a DB for integration tests).

## 📐 ASCII Diagrams
```text
[ SOURCE ] ----(Zip)----> [ BUILD ] ----(Artifact)----> [ DEPLOY ]
(GitHub)                 (CodeBuild)                   (CodeDeploy)
                             |                              |
                      [ UNIT TESTS ]                 [ HEALTH CHECK ]
                      [ LINTING ]                    [ ROLLBACK IF FAIL ]
```

## 🔍 Code / IaC (CodeBuild buildspec.yml)
```yaml
version: 0.2

phases:
  install:
    runtime-versions:
      nodejs: 18
    commands:
      - npm install
  pre_build:
    commands:
      - npm test
  build:
    commands:
      - npm run build
artifacts:
  files:
    - '**/*'
  base-directory: build
```

## 💥 Production Failures
1.  **The "Stuck Pipeline"**: A build fails, but the pipeline doesn't stop. Or a manual approval is forgotten, and production is stuck on an old version for days.
2.  **Inconsistent Environments**: Dev build uses Node 18, but Production server has Node 16. The app crashes on startup. **Solution**: Use the same Docker image for both Build and Production.
3.  **Secret Leakage in Logs**: Printing an API key during the build process (`echo $API_KEY`). The key is now permanently stored in the CodeBuild logs.

## 🧪 Real-time Q&A
*   **Q**: Can I use Jenkins with CodePipeline?
*   **A**: Yes. CodePipeline has a native integration for Jenkins as a Build or Test provider.
*   **Q**: How do I handle multi-account deployments?
*   **A**: You can have a central "DevOps" account with the pipeline and use IAM roles to deploy into "Dev," "Staging," and "Prod" accounts.

## ⚠️ Edge Cases
*   **CodeDeploy Agent**: For EC2 deployments, you must install the CodeDeploy Agent on the instance, or the deployment will hang at "Pending."
*   **Parallel Actions**: CodePipeline can run multiple actions (like testing in 3 different environments) at the same time.

## 🏢 Best Practices
1.  **Pipeline-as-Code**: Define your pipelines in Terraform or CloudFormation.
2.  **Fast Feedback**: Put linting and unit tests as early as possible in the pipeline.
3.  **Small Commits**: Deploy often. Small changes are easier to debug and rollback.

## ⚖️ Trade-offs
*   **CodePipeline**: Deeply integrated with AWS, zero management, but less flexible than Jenkins or GitHub Actions.

## 💼 Interview Q&A
*   **Q**: How would you ensure a zero-downtime deployment for a critical web service?
*   **A**: I would use **CodeDeploy with a Blue-Green deployment strategy**. I would spin up a new set of instances (Green), wait for them to pass health checks, and then shift traffic from the old instances (Blue) to the new ones using the Load Balancer. If anything fails, I would immediately shift traffic back to the Blue instances.

## 🧩 Practice Problems
1.  Create a CodePipeline that triggers on every push to a GitHub repository and runs a simple build in CodeBuild.
2.  Write an `appspec.yml` file for an EC2 deployment that runs a "Smoke Test" script after the deployment is finished.

---
Prev: [04_Alerting_and_SLOs.md](../Observability/04_Alerting_and_SLOs.md) | Index: [Docker/00_Index.md](../00_Index.md) | Next: [02_CloudFormation_vs_Terraform.md](../DevOps/02_CloudFormation_vs_Terraform.md)
---
