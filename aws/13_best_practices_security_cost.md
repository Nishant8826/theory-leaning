# Best Practices: Security & Cost Optimization

---

### 2. What
This file covers mandatory architectural practices you must follow to prevent severe data breaches and disastrous billing accidents when operating in AWS. AWS gives you complete freedom; if you misconfigure a server and owe money, AWS holds you liable.

---

### 3. Why
Hackers utilize automated bots that scrape public GitHub repositories 24/7 searching for AWS Access Keys. If they find your key, they will provision large fleets of massive GPU servers to mine cryptocurrency on your account. Applying the "Well-Architected Framework" policies keeps you absolutely secure.

---

### 4. How
- **Security:** Implement IAM Roles, AWS Secrets Manager, and proper VPC routing.
- **Cost:** Utilize AWS Budgets, Rightsizing, and S3 Lifecycle Rules.

---

### 5. Implementation

**A. Using AWS Budgets (CLI)**

```bash
# 1. Create a budget alarm that emails administrator@mycompany.com 
# if the monthly AWS bill touches $10.00!
aws budgets create-budget \
    --account-id 123456789012 \
    --budget file://budget.json
    
# NOTE: The budget.json file explicitly contains the $10 limit threshold.
```

**B. Securing Passwords**

Instead of putting a Database password into a `.env` file, use **AWS Secrets Manager**.

```javascript
// Example in Node.js
const { SecretsManagerClient, GetSecretValueCommand } = require("@aws-sdk/client-secrets-manager");
const client = new SecretsManagerClient({ region: "us-east-1" });

async function getDBPassword() {
  const response = await client.send(new GetSecretValueCommand({ SecretId: "PROD_DB_PASS" }));
  return response.SecretString; 
}
```

---

### 6. Steps
1. Close Port 22 (SSH) to the global internet. Only open it specifically to your personal IP address.
2. Place the RDS database entirely inside a Private Subnet in your VPC.
3. Turn on Amazon GuardDuty to monitor logs for malicious network activity.

---

### 7. Integration

🧠 **Think Like This:**
* Treat your AWS IAM user Access Keys like passwords to your bank account.
* If a Node server needs to upload files to an S3 bucket, NEVER give the Node code an IAM access key. Build an IAM Role with exact S3 permissions, and attach that Role onto the EC2 instance natively.

---

### 8. Impact
📌 **Real-World Scenario:** A startup's S3 costs ballooned to $5,000 a month because users were uploading millions of log files. An engineer implemented **S3 Lifecycle Rules**, which automatically deletes any file older than 30 days. The next month, the AWS bill dropped to twenty dollars.

---

### 9. Interview Questions

Q1. What is the fundamental principle of the AWS Shared Responsibility Model?
Answer: AWS handles security of the cloud hardware, while the customer is responsible for security in the cloud data and software.

Q2. How do you ensure your AWS root account is secure?
Answer: You enable Multi-Factor Authentication on the root account and delete all root API access keys.

Q3. What is an AWS IAM Role?
Answer: An IAM Role is a temporary identity given to services like EC2 servers, preventing developers from hardcoding passwords into source code.

Q4. What is the Principle of Least Privilege?
Answer: A security standard stating that a user or server must only have the minimum permissions required to perform its task.

Q5. How do you optimize S3 storage costs for old unused files?
Answer: You configure S3 Lifecycle Rules to transition older objects automatically into cheaper storage tiers like Amazon S3 Glacier.

Q6. What happens if you commit an AWS Access Key to a public GitHub repository?
Answer: Automated hacker bots will scrape and exploit the key immediately, while AWS automated bots will detect the leak and email you a security notice.

---

### 10. Summary
* Never expose your IAM Access Keys.
* Rely on IAM Roles for instances.
* Keep databases in Private VPC subnets.
* Always define billing budgets using the CLI.

---
Prev : [12_scaling_load_balancing_monitoring.md](./12_scaling_load_balancing_monitoring.md) | Next : [14_aws_interview_preparation.md](./14_aws_interview_preparation.md)
