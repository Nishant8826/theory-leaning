# 🔐 Secrets Manager vs. SSM Parameter Store

## 📌 Topic Name
Secrets Management: Amazon Secrets Manager vs. AWS Systems Manager (SSM) Parameter Store

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Both store strings and passwords. Secrets Manager is for sensitive stuff like DB passwords; SSM is for config like API URLs.
*   **Expert**: The choice is between **Advanced Credential Lifecycle Management (Secrets Manager)** and **Unified Configuration Management (SSM)**. Secrets Manager provides native integration for automatic password rotation (for RDS, Redshift, DocumentDB) and higher API limits. SSM Parameter Store is a more versatile, tiered storage service that handles both plaintext and encrypted (SecureString) data, often at zero cost.

## 🏗️ Mental Model
- **Secrets Manager**: A **High-Security Safe** with an automated locksmith. It doesn't just hold the key; it changes the locks every 30 days and tells the bank.
- **SSM Parameter Store**: A **Digital Filing Cabinet**. It has folders for "Public" (plaintext) and "Locked" (SecureString) files. It’s simple, organized, and reliable.

## ⚡ Actual Behavior
- **Cost**:
    - Secrets Manager: $0.40 per secret per month + $0.05 per 10k requests.
    - SSM (Standard): **FREE** (up to 10k parameters) + $0.05 per 10k requests.
- **Rotation**: Secrets Manager has built-in Lambda templates for rotating RDS/Aurora passwords without application downtime. SSM has no native rotation (requires custom Lambda).

## 🔬 Internal Mechanics
1.  **Storage Substrate**: Both services use KMS for encryption. When you request a "SecureString" from SSM or a "Secret" from Secrets Manager, the service calls KMS to decrypt the value before sending it to you (or sends the ciphertext if requested).
2.  **Versioning**: Both support versioning. Secrets Manager uses "Staging Labels" (e.g., `AWSCURRENT`, `AWSPREVIOUS`) to facilitate safe rotation.
3.  **Cross-Account**: Secrets Manager supports resource-based policies, making it easier to share secrets across AWS accounts than SSM (which requires IAM role assumption).

## 🔁 Execution Flow (Secrets Manager Rotation)
1.  **Trigger**: Time-based or manual trigger.
2.  **Lambda**: Secrets Manager invokes a "Rotation Lambda."
3.  **Create**: Lambda creates a new password in the DB.
4.  **Set**: Lambda updates the secret in Secrets Manager with the new password (labeled `AWSPENDING`).
5.  **Test**: Lambda verifies the new password works.
6.  **Finish**: Lambda promotes `AWSPENDING` to `AWSCURRENT`.

## 🧠 Resource Behavior
- **Parameter Hierarchies**: SSM supports paths like `/prod/web/db_url`. You can fetch all parameters under a path with one API call (`GetParametersByPath`).
- **Secret Values**: Secrets Manager stores values as JSON, allowing you to store a whole set of credentials (username, password, port, host) in one secret.

## 📐 ASCII Diagrams
```text
[ APPLICATION ]
      |
      +----(API Request)----> [ SECRETS MANAGER ] ----> [ KMS ]
      |                           | (Rotate?)
      |                           V
      |                   [ ROTATION LAMBDA ] ----> [ RDS DB ]
      |
      +----(API Request)----> [ SSM PARAMETER STORE ] ----> [ KMS ]
```

## 🔍 Code / IaC (Terraform)
```hcl
# SSM Parameter (Config)
resource "aws_ssm_parameter" "db_url" {
  name  = "/prod/api/url"
  type  = "String"
  value = "https://api.myapp.com"
}

# Secrets Manager (Sensitive)
resource "aws_secretsmanager_secret" "db_pass" {
  name = "prod/db/password"
}

resource "aws_secretsmanager_secret_version" "pass_val" {
  secret_id     = aws_secretsmanager_secret.db_pass.id
  secret_string = jsonencode({
    username = "admin"
    password = "supersecretpassword"
  })
}
```

## 💥 Production Failures
1.  **Throttling**: Using SSM/Secrets Manager inside a high-frequency loop (e.g., every Lambda invocation). At scale, you will hit API limits. **Solution**: Use the **AWS SDK Cache** or a local cache variable.
2.  **Rotation "Race Condition"**: The Lambda rotates the DB password, but the Application hasn't refreshed its cache. The App keeps using the old password and gets "Access Denied." **Solution**: App should catch 401 errors and force a secret refresh.
3.  **Permission Gap**: The IAM role has permission to read the secret but NOT permission to use the KMS key that encrypts it.

## 🧪 Real-time Q&A
*   **Q**: When should I use Secrets Manager over SSM?
*   **A**: When you need **Automatic Rotation** or **Cross-Account Sharing**. For everything else, SSM is usually better and cheaper.
*   **Q**: Does SSM support secret rotation?
*   **A**: Not natively. You have to write a custom Lambda and trigger it with EventBridge.

## ⚠️ Edge Cases
*   **Standard vs. Advanced Parameters**: SSM Advanced parameters allow for larger values (8KB) and parameter policies (like TTL), but they cost money ($0.05/month).
*   **Drift**: Hardcoding secret values in Terraform. This is a security risk. Use `lifecycle { ignore_changes = [secret_string] }` to allow rotation to happen outside of IaC.

## 🏢 Best Practices
1.  **Use Paths** in SSM for organizational clarity.
2.  **Cache Secrets**: Never call the API for every request.
3.  **Environment Variables**: Avoid putting secrets in environment variables (visible in console/logs). Pull them at runtime from the API.

## ⚖️ Trade-offs
*   **Secrets Manager**: High cost, high feature set (Rotation, Sharing).
*   **SSM**: Low cost, simple, integrates with other Systems Manager features.

## 💼 Interview Q&A
*   **Q**: How do you handle password rotation for a production database with zero downtime?
*   **A**: I would use **Amazon Secrets Manager**. I would configure a Rotation Lambda that creates a new user/password in the database, tests it, and then updates the secret. The application code would be designed to catch authentication failures and re-fetch the latest secret from the API, ensuring a smooth transition between old and new credentials.

## 🧩 Practice Problems
1.  Set up an SSM Parameter with the path `/dev/app/config` and retrieve it using the AWS CLI.
2.  Write a simple Lambda function that rotates a simulated password stored in Secrets Manager.

---
Prev: [02_KMS_Internals.md](../Security/02_KMS_Internals.md) | Index: [Docker/00_Index.md](../00_Index.md) | Next: [04_Network_Security.md](../Security/04_Network_Security.md)
---
