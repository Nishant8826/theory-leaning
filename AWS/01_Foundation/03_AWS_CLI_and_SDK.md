# AWS CLI and SDK

## What Is This Service?
The AWS Command Line Interface (CLI) is a unified tool to manage your AWS services from your terminal. The AWS Software Development Kit (SDK) allows your application code (like a Node.js backend) to interact programmatically with AWS services. 

## Why This Service Exists
Clicking through the AWS Web Console is acceptable for learning, but it is slow, error-prone, and impossible to automate. Production environments require automation. The CLI allows you to write scripts that manage infrastructure, while the SDK allows your Node.js application to directly utilize AWS services (like uploading files to S3 or triggering Lambda functions).

## Real World Analogy
- **AWS Console**: Ordering food at a restaurant by talking to a waiter, reading the menu, and answering questions.
- **AWS CLI/SDK**: Using the restaurant's API to instantly send a JSON payload with your exact order, bypassing the waiter entirely.

## How It Works
Both the CLI and the SDK act as wrappers around the core AWS REST APIs. When you run a CLI command or execute a Node.js SDK function, it signs an HTTP request using your AWS credentials (Access Key ID and Secret Access Key) and sends it over HTTPS to the respective AWS service endpoint.

## Core Concepts
- **Access Keys**: Programmatic credentials consisting of an ID and a Secret Key. They are used to cryptographically sign requests.
- **Profiles**: The CLI allows you to configure multiple environments (e.g., `default` for development, `production` for prod) using the `aws configure` command.
- **Pagination**: AWS APIs limit the number of items returned. Both CLI and SDK handle pagination (using `NextToken`) to fetch large sets of data.

## MERN Stack Integration
The AWS SDK is heavily used in the Express.js backend. 
A classic requirement in MERN apps is image uploads (e.g., user avatars, product images). Instead of saving images in your MongoDB database (which is an anti-pattern) or local server disk (which breaks when scaling to multiple servers), you use the AWS SDK in Node.js to upload the file directly to an S3 bucket.

## Production Impact
- **Automation**: CI/CD pipelines use the CLI to automatically copy React builds to S3 (`aws s3 sync build/ s3://my-bucket`).
- **Feature Enablement**: The SDK allows your app to send emails (via SES), queue background jobs (via SQS), or store files (via S3) without managing servers.

## Real Production Use Cases
- **Image Processing**: A user uploads a profile picture via a React/Next.js frontend. The Express backend (or Next.js API route) receives the file, uses the AWS SDK to upload it to S3, and saves the resulting S3 URL in the MongoDB user document.
- **Infrastructure Management**: A DevOps engineer writes a bash script using the AWS CLI to snapshot the database and back it up every night at 3 AM.

## Production Best Practices
- **Use SDK v3**: Always use AWS SDK for JavaScript v3, not v2. v3 is modular. Instead of importing the massive `aws-sdk` package, you only import the clients you need (e.g., `@aws-sdk/client-s3`), which drastically reduces your Docker image size and Lambda cold starts.
- **Environment Variables**: Never hardcode credentials in your Node code. The SDK automatically looks for `process.env.AWS_ACCESS_KEY_ID` and `process.env.AWS_SECRET_ACCESS_KEY`. 

## Security Best Practices
- **Least Privilege**: When creating Access Keys for the CLI or SDK, ensure the IAM Policy attached to the user only allows exactly what is needed. If your Node app only needs to write to an S3 bucket, do not give it `AdministratorAccess`.
- **IAM Roles over Keys**: In production, your Node.js app running on EC2 or ECS should **NOT** use hardcoded Access Keys. Instead, attach an IAM Role to the server/container. The SDK will automatically fetch temporary, rotating credentials from the metadata service. This prevents leaked keys.

## Cost Optimization Tips
- API calls made via the CLI and SDK cost money (though usually fractions of a cent). Be cautious of infinite loops in your Node.js code making thousands of SDK requests per second to services like S3 or DynamoDB.

## Common Mistakes
- **Pushing `.env` to GitHub**: Developers put their AWS Access Keys in a `.env` file for the SDK and accidentally commit it. AWS often detects this and aggressively quarantines the account, but not before attackers spin up expensive resources.
- **Using SDK v2 syntax in v3**: v3 uses a Command pattern. E.g., `client.send(new PutObjectCommand(params))` instead of the old v2 `s3.putObject(params).promise()`.

## Debugging & Troubleshooting
- **CLI Debugging**: Add `--debug` to any CLI command to see the raw HTTP requests and responses. Very useful for resolving authentication or permission errors.
  ```bash
  aws s3 ls --debug
  ```
- **SDK Debugging**: Set the environment variable `AWS_DEBUG=true` or examine the HTTP error codes returned in the catch block of your SDK promises.

## Summary
The AWS Console is for exploring; the CLI is for automating; the SDK is for building. Mastering programmatic access to AWS is the dividing line between manual sysadmins and modern cloud developers.

---
Prev : [./02_Global_Infrastructure.md](./02_Global_Infrastructure.md) | Index : [../00_Index.md](../00_Index.md) | Next : None
---
