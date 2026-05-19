# Cloudwatch

## Why This Exists
Servers and applications in the cloud don't have physical screens attached to them. When a server crashes at 3 AM, how do you know? How do you read the error message? CloudWatch is AWS's native, centralized monitoring and logging service that acts as your eyes and ears.

## Real World Analogy
Think of the **Security Cameras and Alarm System** of a bank. 
*   **CloudWatch Logs** are the security tapes (recording every text output and event).
*   **CloudWatch Metrics** are the thermometers and motion sensors (measuring numbers).
*   **CloudWatch Alarms** are the loud sirens that wake up the manager if the temperature gets too hot or a sensor is tripped.

## Core Concepts
*   **Metrics:** Data points measured over time (e.g., CPU Utilization, Network In/Out).
*   **Logs:** Text-based records of events. Organized into Log Groups (the folder) and Log Streams (the specific file).
*   **Alarms:** Triggers that perform an action (like sending an email or scaling servers) if a metric goes above a threshold.
*   **Dashboards:** Customizable screens combining graphs of metrics and logs.

## Architecture / Flow
1. An EC2 instance is suddenly under heavy load.
2. The hypervisor reports to **CloudWatch Metrics** that CPU is at 95%.
3. A **CloudWatch Alarm** sees the CPU > 90% threshold has been crossed.
4. The Alarm triggers and sends a message to an SNS (Simple Notification Service) Topic.
5. SNS sends an email to the on-call engineer's phone: "Server CPU Critical!".

## Practical Commands
*   `aws cloudwatch put-metric-alarm ...` - Create an alarm via CLI.
*   `aws logs get-log-events --log-group-name my-logs --log-stream-name stream1` - Fetch logs (though mostly done via Console).

## Hands-On Exercise
Create a Billing Alarm. Go to the CloudWatch Console, select Alarms -> Billing. Create an alarm that sends an email to your personal address if your Estimated AWS Charges exceed $5.00 for the month. This will save you from accidental bankruptcy!

## Mini Project
**"Centralized Logs"**
Launch an EC2 instance. Attach an IAM Role to it that grants `CloudWatchAgentServerPolicy`. SSH in and install the CloudWatch Agent. Configure it to push the system log file (`/var/log/syslog` or `/var/log/messages`) up to CloudWatch Logs. View the live logs in the AWS Console.

## Real Production Usage
Auto Scaling Groups rely entirely on CloudWatch Alarms to know when to spin up more EC2 instances. Serverless functions (AWS Lambda) automatically push all their `console.log()` statements to CloudWatch Logs, making it the primary way to debug serverless code.

## Common Mistakes
*   **Assuming CloudWatch monitors *everything*:** By default, CloudWatch only monitors hypervisor-level metrics (CPU, Network Traffic, Disk Read/Write). It CANNOT see how much RAM you are using or how full your hard drive is! To monitor RAM/Disk Space, you MUST install the custom CloudWatch Agent.
*   **Infinite Log Retention:** By default, CloudWatch stores logs forever. Log storage costs money. Always set a Retention Policy (e.g., "Delete logs after 30 days") on your Log Groups.

## Debugging Guide
*   **Logs not appearing?** 
    1. Did you install the CloudWatch Agent?
    2. Does the EC2 instance have an IAM Role attached that permits `logs:PutLogEvents`? If not, the server is blocked from uploading the logs.

## Best Practices
*   **Set up Billing Alarms immediately:** On every new AWS account, the very first thing you should do is set a $10 billing alarm.
*   **Use CloudWatch Insights:** A powerful querying language built into the console that lets you search through gigabytes of logs in seconds using SQL-like syntax.

## Interview Questions
*   **Q: How does an Auto Scaling Group know when to add more EC2 instances?**
    *   *A: It relies on CloudWatch Alarms. You set an alarm to trigger when the Average CPU metric of the instances exceeds a certain threshold (e.g., 70%), which then tells the Auto Scaling Group to execute a scale-out policy.*

## Summary
CloudWatch provides deep visibility into your dark cloud infrastructure, alerting you to problems and storing the forensic log evidence needed to fix them before your customers even notice.

---
Prev: [07_iam_basics.md](./07_iam_basics.md) | Index: [Index](../00_index.md) | Next: [09_cicd_pipelines.md](./09_cicd_pipelines.md)
