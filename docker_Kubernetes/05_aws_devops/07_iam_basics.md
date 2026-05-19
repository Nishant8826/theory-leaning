# Iam Basics

## Why This Exists
If a junior engineer accidentally deletes the production database, or a hacker steals a key that has full access to your AWS account, your company is dead. IAM (Identity and Access Management) is the security gatekeeper. It controls exactly *who* (Authentication) can do *what* (Authorization) inside your AWS account.

## Real World Analogy
Think of a **Highly Secure Corporate Office Building**. 
*   **IAM User:** The Employee with a permanent ID badge.
*   **IAM Group:** The Department (e.g., "Engineering Team").
*   **IAM Policy:** The rulebook assigned to the badge (e.g., "Allowed to open the Server Room door, Denied from the Vault").
*   **IAM Role:** A temporary visitor badge. Instead of giving a robot permanent credentials, you give it a "Role" it can assume while it works, which expires automatically.

## Core Concepts
*   **Users:** Long-term credentials (username/password or Access Keys) for humans or service accounts.
*   **Groups:** A collection of Users. (Attach policies to groups, not users!).
*   **Roles:** Temporary credentials assumed by AWS services (like EC2) or federated users.
*   **Policies:** JSON documents defining permissions (Allow/Deny, Actions, Resources).

## Architecture / Flow
1. Admin creates a JSON **Policy**: "Allow creating S3 buckets".
2. Admin creates a **Group** called "Developers".
3. Admin attaches the Policy to the Group.
4. Admin creates an **IAM User** for "Alice" and puts her in the "Developers" group.
5. Alice logs in and can create S3 buckets, but is denied from launching EC2 instances.

## Practical Commands
*   `aws iam create-user --user-name Alice`
*   `aws sts get-caller-identity` - The AWS version of `whoami`. Tells you exactly what user/role your terminal is currently using.
*   `aws iam list-users`

## Hands-On Exercise
Create an IAM User in the console with *only* `AmazonS3ReadOnlyAccess`. Generate access keys for this user. Configure your local AWS CLI with these keys. Try to run `aws s3 ls` (it should work). Then try to run `aws ec2 describe-instances` (it should throw an Access Denied error).

## Mini Project
**"The Passwordless Server"**
Create an IAM Role that allows full access to S3. Launch an EC2 instance and attach this Role to it. SSH into the instance and run `aws s3 ls`. It works magically without you ever typing in an access key or secret key, because the EC2 instance assumed the Role!

## Real Production Usage
This is the security foundation of AWS. Every single API call made to AWS (clicking a button in the console, running a CLI command) is authenticated and authorized by IAM. Massive enterprises use IAM Roles federated with Okta or Active Directory so employees use their corporate logins for AWS.

## Common Mistakes
*   **Using the Root Account:** The email you signed up with is the Root account. It has infinite power and cannot be restricted. NEVER use it for daily tasks. Create an Admin IAM User, enable MFA, and lock away the Root account.
*   **Hardcoding Keys:** Pasting AWS Access Keys into your source code and pushing to GitHub. Bots scan GitHub 24/7 and will steal your keys and mine Bitcoin on your account in minutes.

## Debugging Guide
*   **Keep getting "Access Denied"?** In IAM, an explicit `Deny` *always* trumps an `Allow`. Use the "IAM Policy Simulator" tool in the AWS console to test why a specific user is failing to perform an action.

## Best Practices
*   **Principle of Least Privilege:** If a developer only needs to read from one specific S3 bucket (`arn:aws:s3:::my-bucket`), do NOT give them `AmazonS3FullAccess`. Give them exactly what they need and nothing more.

## Interview Questions
*   **Q: What is the difference between an IAM User and an IAM Role?**
    *   *A: A User has permanent credentials (passwords/keys) usually tied to a specific person. A Role provides temporary credentials and is meant to be assumed by trusted entities (like an EC2 instance or a Lambda function).*

## Summary
IAM is arguably the most critical service to master in AWS. Without strict IAM policies, a tiny code bug or a leaked key can result in catastrophic data loss and massive financial bills.

---
Prev: [06_ssl_setup.md](./06_ssl_setup.md) | Index: [Index](../00_index.md) | Next: [08_cloudwatch.md](./08_cloudwatch.md)
