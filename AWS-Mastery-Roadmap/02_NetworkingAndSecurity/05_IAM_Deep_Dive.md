# IAM Deep Dive

## What Is This Service?
AWS Identity and Access Management (IAM) enables you to manage access to AWS services and resources securely. It defines *who* (authentication) can do *what* (authorization) inside your AWS account.

## Why This Service Exists
When you create an AWS account, you get a "Root User" that has infinite power—it can delete databases, spin up $10,000 servers, and close the account. Using this user for daily development or in your MERN application code is incredibly dangerous. IAM exists so you can create granular, restricted permissions for developers, CI/CD pipelines, and application servers.

## Real World Analogy
IAM is the **Keycard Access System** of a high-security corporate building.
- **IAM User**: A person receiving a keycard.
- **IAM Policy**: The permissions programmed into the keycard (e.g., "Can open Door A, but not Door B").
- **IAM Role**: A temporary visitor badge or a specific hat (like "Maintenance Worker") that grants temporary permissions to whoever puts it on (e.g., a Node.js server).

## How It Works
IAM operates globally (not tied to a specific Region). You create identities (Users or Roles) and attach JSON documents called Policies to them. Every time an API request is made to AWS (via Console, CLI, or SDK), IAM evaluates the request against the attached Policies to implicitly deny or explicitly allow the action.

## Core Concepts
- **Users**: Long-term credentials (password for console, Access Keys for CLI) for human developers.
- **Groups**: A collection of Users. You attach a policy to the Group, and all Users inherit it.
- **Policies**: JSON documents defining exact permissions (`Effect`, `Action`, `Resource`).
- **Roles**: Temporary credentials intended to be assumed by AWS services (like an EC2 instance or Lambda function) or federated users.

## MERN Stack Integration
If your Next.js API route needs to upload a user avatar to S3:
**The Wrong Way**: Creating an IAM User, generating Access Keys, and hardcoding them in `.env`.
**The Right Way**: Creating an **IAM Role** with `s3:PutObject` permissions and attaching that Role directly to the EC2 instance or ECS container running your Node.js app. The AWS SDK automatically retrieves temporary keys.

## Production Impact
- **Security**: Eliminating hardcoded long-term Access Keys from your Node.js code drastically reduces the risk of credential leakage via GitHub or NPM vulnerabilities.
- **Auditing**: Combined with CloudTrail, IAM allows you to see exactly which developer or which server executed specific commands.

## Real Production Use Cases
- A CI/CD pipeline (GitHub Actions) needs to deploy a React app to S3. Instead of using access keys, GitHub Actions assumes an IAM Role via OIDC (OpenID Connect), getting a temporary 1-hour token to perform the deployment safely.

## Production Best Practices
- **Principle of Least Privilege**: Never grant `AdministratorAccess` to applications or developers. Give them exactly what they need and nothing more.
- **Require MFA**: Enforce Multi-Factor Authentication for all human Users accessing the console.

## Security Best Practices
- Never share IAM Users. Every human must have their own User account to maintain accountability.
- Rotate Access Keys every 90 days if you absolutely must use them.
- Use IAM Roles for EC2/ECS/Lambda. Never store AWS credentials on the server's disk.

## Cost Optimization Tips
- IAM is 100% free. There is no excuse for cutting corners on access management.

## Common Mistakes
- **The Wildcard Policy**: Writing policies like `"Action": "s3:*"` when the app only needs `"Action": "s3:PutObject"`. If the app is hacked, the hacker can delete the entire bucket instead of just writing to it.
- Committing AWS Access Keys to source control.

## Debugging & Troubleshooting
- **Access Denied (403)**: If your Node API throws an `AccessDenied` exception when calling AWS, use the IAM Policy Simulator. It allows you to test why a specific action on a specific resource is failing for a specific Role.

---
Prev : [./04_Security_Groups_and_NACL.md](./04_Security_Groups_and_NACL.md) | Index : [../00_Index.md](../00_Index.md) | Next : None
---
