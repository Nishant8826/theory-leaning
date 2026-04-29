# 🛡️ Compliance and Auditing

## 📌 Topic Name
AWS Compliance: Proving Security through CloudTrail, Config, and Audit Manager

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: AWS has certificates (SOC2, ISO) and you can see logs of what happened.
*   **Expert**: Compliance is the **Continuous Verification of Governance**. It involves **Logging (CloudTrail)**, **Monitoring Configuration Drift (AWS Config)**, and **Aggregating Proof (Audit Manager)**. A Staff engineer doesn't just "pass an audit"; they build **Automated Remediation** systems that ensure the environment remains compliant in real-time, even as thousands of changes occur daily.

## 🏗️ Mental Model
Think of Compliance as a **Security Camera and Alarm System**.
- **CloudTrail**: The **Security Camera**. It records every person who enters the building and what they did.
- **AWS Config**: The **Inventory Inspector**. It checks if the doors are locked every hour and sounds an alarm if one is open.
- **Audit Manager**: The **Auditor's Binder**. It automatically gathers the camera footage and inspector reports to prove everything was done correctly.

## ⚡ Actual Behavior
- **CloudTrail**: Enabled by default for 90 days. Records "Who, What, When, Where." Essential for forensic analysis after a security incident.
- **AWS Config**: A resource inventory service. It records a history of your resource configurations (e.g., "What did this SG look like on Tuesday?").
- **AWS Artifact**: A portal where you can download AWS's own compliance reports (SOC, PCI, HIPAA).

## 🔬 Internal Mechanics
1.  **CloudTrail S3 Delivery**: To keep logs longer than 90 days, you must create a "Trail" that delivers logs to an S3 bucket. These should be encrypted and protected by MFA Delete.
2.  **Config Rules**: AWS provides managed rules (e.g., `s3-bucket-public-read-prohibited`). You can also write custom rules in Lambda.
3.  **Remediation**: AWS Config can trigger a **Systems Manager Automation** document to fix a non-compliant resource automatically (e.g., "If an S3 bucket is public, make it private immediately").

## 🔁 Execution Flow (Continuous Compliance)
1.  **Event**: Developer changes a Security Group to allow `0.0.0.0/0`.
2.  **CloudTrail**: Records the `AuthorizeSecurityGroupIngress` event.
3.  **AWS Config**: Detects the change and evaluates it against the `restricted-common-ports` rule.
4.  **Violation**: Config marks the SG as "Non-compliant."
5.  **Remediation**: EventBridge triggers an SSM document that deletes the `0.0.0.0/0` rule.
6.  **Resolution**: The SG is back to compliant in <1 minute.

## 🧠 Resource Behavior
- **Management Events**: API calls that modify resources (e.g., `RunInstances`).
- **Data Events**: High-volume API calls within resources (e.g., `s3:GetObject`, `lambda:Invoke`). These are NOT enabled by default because they are expensive.

## 📐 ASCII Diagrams
```text
[ RESOURCE CHANGE ]
        |
+-------V-------+       +-------V-------+
|  CLOUDTRAIL   |       |  AWS CONFIG   |
| (Action Log)  |       | (State Check) |
+-------|-------+       +-------|-------+
        |                       |
[ EVENTBRIDGE ] <---------------(If Non-Compliant)
        |
[ SSM REMEDIATION ] ----> [ FIX RESOURCE ]
```

## 🔍 Code / IaC (Config Rule)
```hcl
# AWS Config Rule to ensure S3 buckets have versioning
resource "aws_config_config_rule" "s3_versioning" {
  name = "s3-bucket-versioning-enabled"

  source {
    owner             = "AWS"
    source_identifier = "S3_BUCKET_VERSIONING_ENABLED"
  }
}

# Remediation configuration
resource "aws_config_remediation_configuration" "s3_versioning_fix" {
  config_rule_name = aws_config_config_rule.s3_versioning.name
  target_type      = "SSM_DOCUMENT"
  target_id        = "AWS-ConfigureS3BucketVersioning"

  parameter {
    name         = "BucketName"
    resource_id_parameter_value = true
  }
}
```

## 💥 Production Failures
1.  **CloudTrail Logs Deleted**: An attacker compromises an account and immediately deletes the CloudTrail logs to hide their tracks. **Solution**: Use **Organizational Trails** and deliver logs to a separate, locked-down security account.
2.  **Config Cost Explosion**: Enabling AWS Config in an account with millions of short-lived resources (like EMR or Batch). Every resource creation/deletion counts as a "Configuration Item" and costs money.
3.  **Remediation Loop**: An automated remediation script fixes a resource, but an IaC tool (like Terraform) immediately "corrects" it back to the non-compliant state during its next run.

## 🧪 Real-time Q&A
*   **Q**: Does AWS Config stop the change from happening?
*   **A**: No. It is "Detective," not "Preventative." To prevent changes, use **IAM Policies** or **Service Control Policies (SCPs)**.
*   **Q**: What is the difference between CloudTrail and CloudWatch Logs?
*   **A**: CloudTrail is for **API Actions** (Who did what). CloudWatch Logs is for **Application/OS Logs** (What is the app doing).

## ⚠️ Edge Cases
*   **Global Services**: Some services (like IAM and CloudFront) log to `us-east-1` CloudTrail even if used globally.
*   **Insights**: CloudTrail Insights can detect "unusual activity" (e.g., a sudden spike in `TerminateInstances` calls) and alert you.

## 🏢 Best Practices
1.  **Centralize Logs**: Send all CloudTrail logs to a dedicated security account.
2.  **Use Organizational Trails**: Ensure CloudTrail is enabled in every sub-account automatically.
3.  **Automate Remediation**: Don't wait for a human to read an email; fix high-risk violations (like public S3 buckets) automatically.

## ⚖️ Trade-offs
*   **Detailed Logging**: High security and auditability, but high cost in S3 storage and API fees.

## 💼 Interview Q&A
*   **Q**: How would you prove to an auditor that your EBS volumes have been encrypted for the last 6 months?
*   **A**: I would use **AWS Config**. I would show the history of the `encrypted-volumes` rule for that time period. AWS Config maintains a timeline for every resource, allowing me to show exactly when an EBS volume was created and that its "Encrypted" flag was always set to `true`.

## 🧩 Practice Problems
1.  Use Athena to query your CloudTrail logs and find all `ConsoleLogin` events from the last 7 days.
2.  Create a custom AWS Config rule that checks if an EC2 instance has a specific mandatory tag.
