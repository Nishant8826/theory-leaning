# CloudTrail

## What Is This Service?
AWS CloudTrail is a web service that records all API activity in your AWS account. It logs exactly who made an API call, when it was made, from what IP address, and what resources were affected.

## Why This Service Exists
CloudWatch tells you *what* happened to your application (e.g., the server crashed). CloudTrail tells you *who* broke the infrastructure (e.g., Bob from DevOps deleted the database). It exists for auditing, security monitoring, and operational troubleshooting.

## Real World Analogy
CloudTrail is the **Security Camera System and Visitor Log** of your AWS account.
Every time someone unlocks a door, modifies a thermostat, or unplugs a server, the system records their name, the exact timestamp, and a video of the action. You cannot delete or tamper with this tape.

## How It Works
Every action in AWS (clicking a button in the console, running a CLI command, or your Node.js app using the SDK) is ultimately an API call. CloudTrail sits at the foundational layer of AWS and records every single one of these API calls as a JSON event. It then saves these logs securely to an S3 bucket.

## Core Concepts
- **Management Events**: Operations performed on resources (e.g., `RunInstances`, `DeleteBucket`, `CreateUser`). These are logged by default for 90 days for free.
- **Data Events**: Operations performed *on data* within a resource (e.g., `s3:GetObject` or `s3:PutObject`). These are high-volume and cost extra to log.
- **Trails**: A configuration that delivers CloudTrail events continuously to an S3 bucket for long-term storage and compliance.

## MERN Stack Integration
While your MERN code doesn't interact with CloudTrail directly, your infrastructure does.
If your Express.js backend is configured with an IAM Role to upload files to S3, every single `PutObject` call can be tracked in CloudTrail (if Data Events are enabled), providing a perfect audit log of backend activity.

## Production Impact
- **Compliance**: SOC 2, HIPAA, and PCI-DSS all require strict audit logging of infrastructure changes. Enabling a CloudTrail Trail instantly satisfies this requirement.
- **Troubleshooting**: If a production React app suddenly goes offline because an S3 bucket was emptied, CloudTrail is the ONLY way to figure out which developer (or compromised IAM key) did it.

## Real Production Use Cases
- A company notices their AWS bill spiked by $5,000 due to 100 massive EC2 instances being launched overnight in a random region (e.g., Tokyo). They open CloudTrail, search for the `RunInstances` event, and discover that a developer's access key was compromised and used to mine cryptocurrency.

## Production Best Practices
- **Enable a Trail Immediately**: The 90-day free event history is great, but creating a permanent Trail to S3 is mandatory for production.
- **Lock Down the S3 Bucket**: The S3 bucket storing your CloudTrail logs should have strict IAM policies preventing *anyone* (even admins) from deleting the logs.

## Security Best Practices
- **CloudWatch Integration**: You can configure CloudTrail to send specific events to CloudWatch. For example, if someone calls the `DeleteVpc` API, CloudTrail sees it, sends it to CloudWatch, and CloudWatch immediately triggers an Alarm to page the security team.

## Cost Optimization Tips
- **Be careful with Data Events**: Logging every single S3 `GetObject` or Lambda `Invoke` (Data Events) can generate billions of logs a month, resulting in massive CloudTrail bills. Only log Management Events unless you have strict compliance needs.

## Common Mistakes
- **Ignoring Multi-Region**: Hackers know that developers usually only look at their default region (e.g., `us-east-1`). They will spin up malicious resources in `ap-northeast-1`. Always ensure your CloudTrail is configured as a **Multi-Region Trail** to catch global activity.

## Debugging & Troubleshooting
- **"Who deleted my server?"**: Go to CloudTrail > Event History. Filter by `Event name` = `TerminateInstances`. You will instantly see the IAM User or Role responsible.

---
Prev : [./03_CloudWatch.md](./03_CloudWatch.md) | Index : [../00_Index.md](../00_Index.md) | Next : [./05_Terraform_Basics.md](./05_Terraform_Basics.md)
---
