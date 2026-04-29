# 🚀 Blue-Green and Canary Deployments

## 📌 Topic Name
Advanced Deployment Strategies: Minimizing Risk and Downtime

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Blue-Green swaps all traffic at once; Canary swaps it slowly.
*   **Expert**: These are **Safe Deployment Patterns** designed to reduce the "Blast Radius" of a bad release. **Blue-Green** involves running two identical environments (Blue is old, Green is new) and swapping traffic at the Load Balancer or DNS level. **Canary** involves shifting a small percentage (e.g., 5%) of traffic to the new version, monitoring for errors, and then gradually increasing the percentage. A Staff engineer chooses the strategy based on the application's statefulness, database schema complexity, and rollback requirements.

## 🏗️ Mental Model
- **Blue-Green**: A **Train Track Switch**. You have two parallel tracks. You flip a switch, and the train (Traffic) moves from the old track to the new one. If the new track is broken, you flip the switch back.
- **Canary**: A **Coal Mine Bird**. You send one small bird (5% of users) into the mine first. If the bird stays healthy, you send the rest of the miners (Users) in.

## ⚡ Actual Behavior
- **Blue-Green (ECS/Lambda)**: AWS creates a whole new set of tasks/instances. Once they are healthy, it updates the Load Balancer to point to the new Target Group and drains connections from the old one.
- **Canary (App Mesh/CloudFront)**: Uses weighted routing to split traffic at the edge or at the service mesh layer.

## 🔬 Internal Mechanics
1.  **CodeDeploy Lifecycle Hooks**: 
    - `BeforeAllowTraffic`: Run tests (e.g., DB migration check) before users see the code.
    - `AfterAllowTraffic`: Run smoke tests while users are on the new version.
2.  **Health-Based Rollback**: CodeDeploy can monitor CloudWatch Alarms. If errors spike during the canary phase, it automatically rolls back to the previous version.
3.  **Sticky Sessions**: A challenge for Canary. If a user is "stuck" to a server, they might see a mix of old and new versions if the load balancer isn't careful.

## 🔁 Execution Flow (Blue-Green with ALB)
1.  **Provision**: CodeDeploy launches "Green" instances.
2.  **Health Check**: Wait for Green instances to pass ELB health checks.
3.  **Test**: Run optional "Pre-traffic" tests.
4.  **Shift**: ALB reroutes 100% of traffic to the Green Target Group.
5.  **Draining**: ALB keeps Blue connections open for a "Draining Period" (e.g., 300s) to allow existing requests to finish.
6.  **Cleanup**: Blue instances are terminated after a successful deployment.

## 🧠 Resource Behavior
- **DNS CNAME Swap**: Another way to do Blue-Green. Faster for some architectures but can be delayed by client-side DNS caching.
- **Linear vs. All-at-Once**: CodeDeploy can do "Linear10PercentEvery1Minute" (Canary) or "AllAtOnce" (Blue-Green).

## 📐 ASCII Diagrams
```text
[ BLUE-GREEN ]
[ TRAFFIC ] ----> [ ALB ]
                    |
           +--------+--------+
           | (Current)       | (New)
        [ BLUE ]         [ GREEN ]
       (Version 1)      (Version 2)


[ CANARY ]
[ TRAFFIC ] ----> [ WEIGHTED ROUTER ]
                    | (95%)       | (5%)
                 [ V1 ]        [ V2 (Canary) ]
```

## 🔍 Code / IaC (AppSpec for Lambda Canary)
```yaml
version: 0.0
Resources:
  - myLambdaFunction:
      Type: AWS::Lambda::Function
      Properties:
        Name: "my-function"
        Alias: "live"
        CurrentVersion: "1"
        TargetVersion: "2"
Hooks:
  - PreTraffic: "BeforeAllowTrafficLambda"
  - PostTraffic: "AfterAllowTrafficLambda"
```

## 💥 Production Failures
1.  **Database Incompatibility**: You deploy Code V2 (Blue-Green), which expects a new DB column. You rollback to V1, but V1 doesn't know about the new column and crashes. **Solution**: Use **Expand/Contract (Parallel Change)** database migrations.
2.  **Shared State Corruption**: New code writes a different format to a shared Redis cache. When you rollback, the old code can't read the new format and crashes.
3.  **Canary Too Small**: 1% of traffic isn't enough to trigger an error alarm. You scale to 100%, and *then* the system crashes under full load.

## 🧪 Real-time Q&A
*   **Q**: When should I use Canary over Blue-Green?
*   **A**: Use Canary for high-risk changes or when you want to test performance under real load. Use Blue-Green for simple, fast updates where you want a clean swap.
*   **Q**: Does Blue-Green cost more?
*   **A**: Yes, temporarily. During the deployment, you are running double the amount of compute (both Blue and Green environments).

## ⚠️ Edge Cases
- **Hard-to-Rollback changes**: Like a one-way data migration. These require "Forward-only" fixes instead of traditional rollbacks.
- **WebSocket/Long-lived connections**: These are difficult to "drain" and might require forcing a disconnect.

## 🏢 Best Practices
1.  **Automated Rollbacks**: Never wait for a human to see a problem. Use CloudWatch Alarms to trigger rollbacks automatically.
2.  **Monitor p99 Latency**: During a canary, look for latency spikes in the new version.
3.  **Feature Flags**: Use feature flags (like AWS AppConfig) to decouple "Deployment" from "Release."

## ⚖️ Trade-offs
*   **Blue-Green**: Fast, easy rollback, but expensive (double capacity) and risky for database changes.
*   **Canary**: Very safe, low cost (no double capacity), but complex to set up and slow to complete.

## 💼 Interview Q&A
*   **Q**: How do you handle a database schema change during a Blue-Green deployment?
*   **A**: I use the **Expand/Contract** pattern. First, I deploy a change that *adds* the new column (but the app doesn't use it yet). Then, I deploy the new code (Green) that writes to both columns. Once I'm sure it's working, I deploy a third change that only uses the new column. Finally, I "contract" the database by removing the old column. This ensures that the old code (Blue) can always run if a rollback is needed.

## 🧩 Practice Problems
1.  Configure a Lambda function with "Provisioned Concurrency" and a Canary deployment strategy.
2.  Perform a Blue-Green swap of two S3-hosted websites using Route 53 weighted records.
