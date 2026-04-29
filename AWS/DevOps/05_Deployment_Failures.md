# 🚀 Deployment Failures

## 📌 Topic Name
Troubleshooting Deployment Failures: Rollbacks, Stalls, and "Zombie" States

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: If a deployment fails, it stops and tries to go back to the previous version.
*   **Expert**: Deployment failure is a **State Machine Interrupt**. It can manifest as a **Hard Failure** (e.g., code crash), a **Soft Failure** (e.g., performance degradation), or a **Stall** (e.g., waiting for a health check that never passes). A Staff engineer knows how to identify which layer of the stack (IAM, VPC, App, or Orchestrator) is causing the failure and how to perform a **Safe Rollback** that doesn't cause data corruption.

## 🏗️ Mental Model
Think of a Deployment Failure as a **Surgery**.
1.  **The Incision (Deploy)**: Starting the change.
2.  **Complication (Failure)**: Something goes wrong (Heart rate drops).
3.  **The Decision**: Do we finish the surgery (Fix forward) or sew them up and try another day (Rollback)?
4.  **The Recovery**: Ensuring the patient (The App) is stable after the failed attempt.

## ⚡ Actual Behavior
- **CodeDeploy**: Automatically rolls back to the last successful deployment if a CloudWatch Alarm is triggered.
- **CloudFormation**: If any resource fails to create/update, it attempts to roll back all resources in the stack to their previous state (`ROLLBACK_IN_PROGRESS`).
- **ECS**: If a new task fails to pass health checks, ECS will keep trying to launch it (and terminating the failing ones) until the deployment is manually stopped or a timeout is hit.

## 🔬 Internal Mechanics
1.  **Health Check Grace Period**: The time the orchestrator waits for an app to start before marking it as "unhealthy." If this is too short, deployments will always fail.
2.  **Rollback S3 Bucket**: For Lambda/CodeDeploy, the system keeps the previous zip in S3 so it can quickly re-deploy it.
3.  **Circuit Breaker (ECS)**: A feature that automatically stops a deployment and rolls back if tasks fail to start a certain number of times.

## 🔁 Execution Flow (Failed Deployment)
1.  **Trigger**: `aws deploy create-deployment ...`
2.  **Status**: New instances launch.
3.  **Monitor**: CodeDeploy monitors the "Post-Traffic" CloudWatch Alarm.
4.  **Breach**: Alarm fires because 5xx errors > 1%.
5.  **Stop**: CodeDeploy immediately stops shifting traffic to the new version.
6.  **Revert**: Traffic is shifted back 100% to the old version.
7.  **Cleanup**: The new, failing instances are terminated.

## 🧠 Resource Behavior
- **Stalled Deployments**: Often caused by a load balancer not being able to reach the new instances (SG/NACL issue).
- **UpdateRollbackFailed**: The most dreaded CloudFormation state. It means the "revert" action also failed (e.g., a resource was manually deleted).

## 📐 ASCII Diagrams
```text
[ VERSION 1 (OK) ] <-----+
                         |
[ VERSION 2 (DEPLOY) ] --+--(CRASH!)
                         |
[ MONITORING ALARM ] ----+--(TRIGGER ROLLBACK)
                         |
[ VERSION 1 (RE-ACTIVATE) ]
```

## 🔍 Code / IaC (ECS Deployment Circuit Breaker)
```hcl
resource "aws_ecs_service" "app" {
  name            = "my-app"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count   = 3

  deployment_circuit_breaker {
    enable   = true
    rollback = true # Automatically rollback on failure
  }

  deployment_controller {
    type = "ECS" # Default rolling update
  }
}
```

## 💥 Production Failures
1.  **The "Zombie" Deployment**: An app crashes after 5 minutes of running. The initial health check passed, so the old version was deleted. Now the whole service is down, and there is no old version to roll back to. **Solution**: Use longer "Bake Times" for canary deployments.
2.  **Rollback Loop**: Version 2 has a bug. Version 1 (the rollback target) also has a bug because of a shared DB change. The system keeps trying to rollback, but both versions are dead.
3.  **IAM Permission Gap**: The deployment script has permission to *create* a resource but not to *delete* or *rollback* it. The rollback fails, leaving the stack in a broken state.

## 🧪 Real-time Q&A
*   **Q**: What is "Fix Forward"?
*   **A**: Instead of rolling back to the old version, you quickly commit a new fix to resolve the issue in the new version. Only recommended for small, easy fixes.
*   **Q**: Why did my ECS deployment take 20 minutes to fail?
*   **A**: Likely due to the **Load Balancer Health Check** settings (e.g., 10 checks every 30 seconds) plus the **Deployment Timeout** settings.

## ⚠️ Edge Cases
*   **External Dependencies**: A deployment fails because a 3rd party API (like Stripe or Twilio) is down during the smoke test.
*   **Schema Lock**: A database migration is running and holding a lock, preventing the new app instances from starting.

## 🏢 Best Practices
1.  **Always enable Automated Rollbacks**.
2.  **Use Smoke Tests**: A script that verifies the core functionality (e.g., "Can I log in?") before completing the deployment.
3.  **Monitor "Deployment Success Rate"**: If more than 5% of deployments fail, your pipeline or testing strategy is flawed.

## ⚖️ Trade-offs
*   **Aggressive Rollback**: High availability but can mask underlying issues that need fixing.
*   **Manual Rollback**: High control but slow and prone to human error during an incident.

## 💼 Interview Q&A
*   **Q**: How do you troubleshoot a CloudFormation stack that is stuck in `DELETE_FAILED`?
*   **A**: I would check the **Events** tab to see which resource failed to delete. Often it's because a bucket is not empty or a security group is still in use. I would manually fix the resource (e.g., empty the bucket) and then try the deletion again. If that fails, I can choose to **Retain** the failing resource during the next delete attempt to allow the rest of the stack to be cleaned up.

## 🧩 Practice Problems
1.  Purposely break a Lambda function (syntax error) and observe how CodeDeploy handles the failed deployment and rollback.
2.  Debug an ECS service that is "stuck" in a cycle of launching and terminating tasks.
