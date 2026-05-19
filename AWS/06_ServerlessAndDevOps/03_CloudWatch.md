# CloudWatch

## What Is This Service?
Amazon CloudWatch is a monitoring and observability service that collects logs, metrics, and events from your AWS resources and applications in real-time.

## Why This Service Exists
When you run a MERN app locally, you look at your terminal to see `console.log()` statements. When you deploy to AWS across 10 EC2 instances, 5 ECS containers, and 20 Lambda functions, you no longer have a single terminal. CloudWatch exists to centralize all logs, track CPU/Memory metrics, and trigger automated alarms so you can see exactly what is happening across your entire infrastructure.

## Real World Analogy
CloudWatch is the **Dashboard and Black Box** of an airplane.
The pilot (you) can't see the engines or the landing gear while flying. You rely on the dashboard dials (CloudWatch Metrics) to ensure the engines are running smoothly. If the plane crashes, investigators look at the Black Box (CloudWatch Logs) to reconstruct exactly what went wrong.

## How It Works
1. AWS services (like EC2, ECS, Lambda) automatically send **Metrics** (e.g., CPU utilization, Network I/O) to CloudWatch every 1-5 minutes.
2. Applications can stream **Logs** directly into CloudWatch Log Groups.
3. You create **Alarms** based on those metrics (e.g., "If CPU > 80% for 5 minutes, send an email").
4. **Events/EventBridge** listens for state changes and can trigger actions (e.g., "Every day at midnight, trigger this Lambda").

## Core Concepts
- **Metrics**: Time-ordered data points (CPU%, 5xx Error rates).
- **Log Groups & Log Streams**: A Log Group represents an application (e.g., `Mern-Backend`), while a Log Stream represents an individual instance/container running that application.
- **Alarms**: Triggers that watch a single metric and perform actions (like sending an SNS notification or triggering Auto Scaling).

## MERN Stack Integration
- **Node.js Logging**: Instead of writing logs to a local `app.log` file on an EC2 instance, you configure your process manager (PM2) or Docker container (awslogs driver) to pipe `stdout` and `stderr` directly into CloudWatch Logs.
- **Custom Metrics**: Using the AWS SDK, your Node.js application can push custom business metrics to CloudWatch, such as `UserSignups` or `OrdersProcessed`.

## Production Impact
- **Observability**: Without CloudWatch, debugging a crashed ECS container in a private subnet is impossible. With CloudWatch, you simply search the logs for the exact stack trace.
- **Proactive Scaling**: CloudWatch Alarms are the core engine behind EC2 Auto Scaling.

## Real Production Use Cases
- A React application is throwing a generic "Internal Server Error". The developer opens CloudWatch Logs Insights, runs a query to filter for all `ERROR` severity logs in the `/ecs/mern-api` Log Group from the last 15 minutes, and instantly finds the MongoDB connection timeout stack trace.

## Production Best Practices
- **Log Retention**: By default, CloudWatch Log Groups keep logs *forever*. This gets extremely expensive. Always set a Retention Period (e.g., 14 days or 30 days) on your Log Groups to automatically delete old, useless logs.
- **Structured Logging**: Always log in JSON format from your Node.js app (`console.log(JSON.stringify({ user, error }))`). CloudWatch Logs Insights can easily parse, filter, and graph JSON fields.

## Security Best Practices
- **Metric Filters**: Create Metric Filters that scan your CloudWatch Logs for specific keywords (like "UnauthorizedAccess" or "FailedLogin"). If the keyword appears 10 times in a minute, trigger an alarm to alert the security team.

## Cost Optimization Tips
- CloudWatch Logs ingestion costs $0.50 per GB. If your Node.js app logs massive payload dumps for every single HTTP request, you will face a shocking AWS bill. Only log critical information and errors in production environments.

## Common Mistakes
- Creating an alarm but forgetting to confirm the SNS Topic email subscription, meaning critical production down alerts are silently dropped.
- Logging sensitive PII (Personally Identifiable Information) or passwords into CloudWatch.

## Debugging & Troubleshooting
- **Logs Insights**: Learn the CloudWatch Logs Insights query language. It is incredibly powerful. Example query to find the most common errors:
  ```text
  fields @timestamp, @message
  | filter @message like /Error/
  | sort @timestamp desc
  | limit 20
  ```

---
Prev : [./02_API_Gateway.md](./02_API_Gateway.md) | Index : [../00_Index.md](../00_Index.md) | Next : [./04_CloudTrail.md](./04_CloudTrail.md)
---
