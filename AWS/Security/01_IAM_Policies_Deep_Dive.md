# 🔐 IAM Policies Deep Dive

## 📌 Topic Name
IAM Policy Evaluation: Logic, Variables, and Boundaries

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: You write JSON to allow or deny actions.
*   **Expert**: IAM Policies are a **Logic-Based Domain Specific Language (DSL)**. Evaluation is a deterministic process that consolidates multiple policy types. A Staff engineer doesn't just write `Allow`, they use **Condition Keys**, **Policy Variables**, and **Permissions Boundaries** to create scalable, self-service security models.

## 🏗️ Mental Model
Think of IAM Policy Evaluation as a **Judge in a Courtroom**.
1.  **Is there a Law against this?** (Explicit Deny in any policy? Yes -> Guilty/Deny).
2.  **Does the Organization allow it?** (SCP check).
3.  **Is it within the Employee's scope?** (Permissions Boundary).
4.  **Is there a specific Law allowing this?** (Explicit Allow in Identity or Resource policy).
5.  **Default**: If no one said it's allowed, it's Denied (Implicit Deny).

## ⚡ Actual Behavior
- **Evaluation Order**: Explicit Deny > SCP > Permissions Boundary > Session Policy > Identity/Resource Policy.
- **Variables**: You can use `${aws:username}` or `${aws:PrincipalTag/Department}` to write one policy that works for thousands of users.
- **NotAction**: Be careful! `Allow` with `NotAction: "s3:DeleteObject"` means you allow EVERYTHING ELSE in AWS (EC2, RDS, IAM) EXCEPT S3 Delete.

## 🔬 Internal Mechanics
1.  **The "Request Context"**: When an API call is made, AWS generates a context containing the `Action`, `Resource`, `Principal`, `SourceIp`, `Time`, and any `Tags`.
2.  **Boolean Logic**: Policies are evaluated as a massive boolean expression. `Condition` blocks use operators like `StringEquals`, `NumericLessThan`, and `IpAddress`.
3.  **Cross-Account**: For cross-account access (e.g., Account A accessing S3 in Account B), BOTH the Identity Policy in A AND the Resource Policy in B must explicitly `Allow`.

## 🔁 Execution Flow (Evaluation Logic)
1.  **Start**: Default = Deny.
2.  **SCP**: Does the Org allow `s3:PutObject`? Yes.
3.  **Identity Policy**: Does the user have `Allow` for `s3:PutObject`? Yes.
4.  **Resource Policy**: Does the S3 bucket have a `Deny` for this user? No.
5.  **Permissions Boundary**: Does the boundary allow `s3:PutObject`? Yes.
6.  **Final**: Access ALLOWED.

## 🧠 Resource Behavior
- **Confused Deputy**: Using `Condition: { "StringEquals": { "aws:SourceArn": "..." } }` in a trust policy to ensure only a specific resource can assume a role.
- **PassRole**: The permission `iam:PassRole` is what allows a user to "give" a role to a service (like EC2 or Lambda). Without this, you can't launch an instance with a role.

## 📐 ASCII Diagrams
```text
[ REQUEST ]
    |
[ EXPLICIT DENY? ] --(YES)--> [ DENY ]
    |
[ SCP ALLOW? ] ------(NO)---> [ DENY ]
    |
[ BOUNDARY ALLOW? ] --(NO)--> [ DENY ]
    |
[ IDENTITY/RESOURCE ALLOW? ] --(YES)--> [ ALLOW ]
    |
[ IMPLICIT DENY ]
```

## 🔍 Code / IaC (Advanced Policy)
```hcl
# Policy using Variables for Home Directories in S3
resource "aws_iam_policy" "user_home" {
  name = "UserS3Home"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["s3:ListBucket"]
        Resource = ["arn:aws:s3:::my-company-data"]
        Condition = {
          "StringLike" = { "s3:prefix": ["home/${aws:username}/*"] }
        }
      },
      {
        Effect   = "Allow"
        Action   = ["s3:GetObject", "s3:PutObject"]
        Resource = ["arn:aws:s3:::my-company-data/home/${aws:username}/*"]
      }
    ]
  })
}
```

## 💥 Production Failures
1.  **SCP Lockout**: An administrator applies an SCP that denies `iam:*` to everyone in the account, including themselves. Now no one can fix the permissions (Must be fixed from the Management account).
2.  **Resource-Based Deny**: A bucket policy has a `Deny` for all traffic NOT coming from a specific VPC. An admin tries to fix it from the console (public internet) and locks themselves out.
3.  **Policy Length Limit**: Reaching the character limit of a policy (6KB for roles, 10KB for users). You must refactor into multiple managed policies.

## 🧪 Real-time Q&A
*   **Q**: What is a Permissions Boundary?
*   **A**: It's a "Maximum Permission" set. If a user has `AdministratorAccess` but a boundary that only allows `S3`, they can only use S3.
*   **Q**: Can I use IAM to restrict access to specific rows in a DynamoDB table?
*   **A**: Yes, using `dynamodb:LeadingKeys` condition to match the Partition Key with the user's ID.

## ⚠️ Edge Cases
*   **Trust Relationships**: The "AssumeRolePolicyDocument" is a special type of resource policy that defines who can become the role.
*   **Service-Linked Roles**: Roles managed by AWS services (like Auto Scaling) that you cannot delete or modify.

## 🏢 Best Practices
1.  **No Wildcards**: Never use `Action: "*"`.
2.  **Use Groups/Roles**: Avoid attaching policies directly to users.
3.  **Tags for ABAC**: Use `aws:PrincipalTag` to grant access based on department/project tags.

## ⚖️ Trade-offs
*   **Identity-Based**: Easier to manage for users/groups.
*   **Resource-Based**: Essential for cross-account access and providing access to anonymous or federated users.

## 💼 Interview Q&A
*   **Q**: A user has an IAM policy allowing `s3:*` but still can't access a bucket. Why?
*   **A**: 1. There is an explicit `Deny` in the Bucket Policy. 2. There is an SCP denying access. 3. A Permissions Boundary is restricting them. 4. The bucket is encrypted with a KMS key they don't have access to.

## 🧩 Practice Problems
1.  Write a policy that allows a developer to launch EC2 instances ONLY if they attach a specific IAM Role to the instance.
2.  Debug a cross-account S3 access issue where the user can see the objects but cannot download them.

---
Prev: [08_Connection_Lifecycle.md](../Networking/08_Connection_Lifecycle.md) | Index: [Docker/00_Index.md](../00_Index.md) | Next: [02_KMS_Internals.md](../Security/02_KMS_Internals.md)
---
