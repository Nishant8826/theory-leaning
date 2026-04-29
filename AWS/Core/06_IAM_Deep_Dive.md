# 🔐 IAM Deep Dive

## 📌 Topic Name
Identity and Access Management (IAM): The Global Security Backbone

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Users get permissions to do things in AWS.
*   **Expert**: IAM is a **Distributed Policy Evaluation Engine**. It is a global service (though it has regional endpoints for speed). It handles Authentication (Who are you?) and Authorization (What can you do?). Authorization is determined by a complex evaluation logic that merges multiple policy types: Identity-based, Resource-based, Permissions Boundaries, and Service Control Policies (SCPs).

## 🏗️ Mental Model
Think of IAM as a **Security Guard at a High-Security Facility**.
- **User**: A permanent employee with a badge.
- **Group**: A department (Engineering, Finance).
- **Role**: A "Hat" or "Keycard" that anyone (or a machine) can put on if they are allowed.
- **Policy**: The rulebook the guard uses to decide if you can enter a room.

## ⚡ Actual Behavior
When you make an AWS API call (e.g., `s3:ListBucket`), the request includes a signature (SigV4). AWS IAM receives the request, identifies the principal, and starts the **Evaluation Logic**. It looks for an explicit **DENY** first. If any policy denies the action, the request is rejected immediately. If no Deny exists, it looks for at least one explicit **ALLOW**. If neither exists, the default is an implicit Deny.

## 🔬 Internal Mechanics
1.  **Policy Evaluation Order**:
    *   Explicit Deny (Highest priority)
    *   SCP (Organizations level)
    *   Resource-based Policy (e.g., S3 Bucket Policy)
    *   Permissions Boundary
    *   Session Policy
    *   Identity-based Policy (User/Role)
2.  **IAM Roles and STS**: When an EC2 instance or Lambda uses a role, it calls the **Security Token Service (STS)** to get temporary credentials (Access Key, Secret Key, Session Token). These rotate automatically.
3.  **Global Replication**: IAM is global. When you update a policy, it replicates across all AWS regions in seconds, but "eventual consistency" can occasionally cause a 1-2 second delay where the old policy still applies.

## 🔁 Execution Flow (API Call)
1.  **Client**: Signs request with credentials.
2.  **AWS Endpoint**: Authenticates the signature.
3.  **IAM Engine**: Gathers all applicable policies.
4.  **Logic Logic**: Resolves `Allow` vs `Deny`.
5.  **Service**: Executes the action if authorized.

## 🧠 Resource Behavior
- **Roles vs Users**: Users have long-term credentials. Roles have temporary credentials. **Staff Rule**: Never use IAM Users for applications; always use Roles.
- **Trust Relationship**: A role has a "Trust Policy" that defines *who* can assume it (e.g., "The EC2 service can assume this role").

## 📐 ASCII Diagrams
```text
[ Principal ] --(API Request + SigV4)--> [ IAM Evaluation ]
                                              |
      +---------------------------------------+---------------------------------------+
      |                                       |                                       |
 [ SCP (Org) ]                    [ Permissions Boundary ]               [ Identity Policy ]
      |                                       |                                       |
      V                                       V                                       V
   DENY? ------------------------------> ALLOW? -----------------------------> FINAL DECISION
```

## 🔍 Code / IaC (Terraform)
```hcl
# IAM Role for EC2
resource "aws_iam_role" "app_role" {
  name = "AppExecutionRole"

  # Trust Policy: Allows EC2 to assume this role
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = { Service = "ec2.amazonaws.com" }
    }]
  })
}

# Identity-based Policy
resource "aws_iam_role_policy" "s3_access" {
  name = "S3Access"
  role = aws_iam_role.app_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action   = ["s3:GetObject"]
      Effect   = "Allow"
      Resource = ["arn:aws:s3:::my-bucket/*"]
    }]
  })
}
```

## 💥 Production Failures
1.  **Circular Dependency**: Role A needs to assume Role B, but Role B's trust policy doesn't allow Role A.
2.  **Confused Deputy**: A service (like a 3rd party SaaS) uses your IAM role to access your account but doesn't check an `ExternalID`, allowing other customers of that SaaS to potentially access your resources.
3.  **Policy Size Limit**: IAM policies have a character limit (e.g., 6144 characters for roles). Large, complex policies can hit this, requiring them to be split.

## 🧪 Real-time Q&A
*   **Q**: What happens if an S3 Bucket Policy allows access but an IAM Policy denies it?
*   **A**: Access is **Denied**. Explicit Deny always wins.
*   **Q**: Can I use IAM to control access to my Linux OS users?
*   **A**: No. IAM controls AWS API access. For OS users, use AWS Systems Manager Instance Connect or traditional SSH keys.

## ⚠️ Edge Cases
- **NotAction / NotResource**: Be careful! `Allow` with `NotAction: s3:DeleteObject` means you allow *everything else* in AWS, not just S3.
- **Cross-Account Access**: Requires both the source account (IAM policy) and the destination account (Resource policy) to allow the access.

## 🏢 Best Practices
1.  **Least Privilege**: Never use `Action: "*"`.
2.  **Condition Keys**: Use `aws:SourceIp` or `aws:PrincipalOrgID` for extra security.
3.  **IAM Access Analyzer**: Use it to find resources shared with external entities.

## ⚖️ Trade-offs
*   **Managed Policies vs. Inline Policies**: Managed policies are reusable and versioned; inline policies are strictly bound to one principal but are easier for one-off permissions.

## 💼 Interview Q&A
*   **Q**: Difference between a Role and a User?
*   **A**: A User represents a permanent identity; a Role is a temporary identity with no long-term credentials, assumed by principals (Users, Services, or AWS Accounts).

## 🧩 Practice Problems
1.  Write a policy that allows a user to manage their own MFA device but nothing else.
2.  Debug why an EC2 instance with an S3-full-access role cannot upload a file to a bucket that has an explicit "Deny" for that instance's IP address.
