# 23 – AWS Lambda & Serverless Architecture

> **Topic:** AWS Lambda Serverless Architecture – Image Resizing Project  
> **Level:** Beginner-friendly with interview prep  

---

## Table of Contents

1. [What is Serverless Computing?](#1-what-is-serverless-computing)
2. [AWS Lambda – Deep Dive](#2-aws-lambda--deep-dive)
3. [Project Architecture – Image Resizing](#3-project-architecture--image-resizing)
4. [Key AWS Services Involved](#4-key-aws-services-involved)
5. [Practical Implementation with Terraform](#5-practical-implementation-with-terraform)
6. [How Lambda Triggering Works](#6-how-lambda-triggering-works)
7. [Visual Diagrams](#7-visual-diagrams)
8. [Scenario-Based Q&A](#8-scenario-based-qa)
9. [Interview Q&A](#9-interview-qa)

---

## 1. What is Serverless Computing?

### What
Serverless computing is a cloud model where **you write code and the cloud provider manages everything else** – servers, OS, scaling, patching, availability. You never "see" or manage a server.

> 🧠 "Serverless" doesn't mean *no* servers. It means *you* don't manage them. AWS does.

### Why
Traditional approach: You rent a virtual machine (EC2), install software, manage uptime, pay 24/7.  
Serverless approach: You deploy a function, it runs *only when triggered*, and you pay *only for that run time*.

| Traditional Server (EC2) | Serverless (Lambda) |
|--------------------------|---------------------|
| Pay 24/7 even if idle    | Pay only when code runs |
| You manage scaling       | Auto-scales instantly |
| You patch/maintain OS    | AWS manages everything |
| Always running           | Wakes up on demand |

### How
1. You upload your code (called a **function**) to the cloud.
2. You define a **trigger** (an event that runs your code).
3. When the trigger fires, the cloud provider allocates compute, runs your code, and shuts it down.
4. You're billed only for the milliseconds your code ran.

### Impact
- **With serverless:** Low cost, zero server management, infinite scalability.
- **Without serverless:** You'd need a running server 24/7, manual scaling, higher ops overhead.

---

## 2. AWS Lambda – Deep Dive

### What
AWS Lambda is Amazon's serverless compute service. It runs your code in response to **events** (triggers), automatically manages compute infrastructure, and charges per millisecond of execution.

**Launched:** 2014 – the first major serverless compute platform.

### Key Facts at a Glance

| Feature | Detail |
|---------|--------|
| Billing | Per millisecond of execution |
| Free tier | 1 million requests/month free |
| Languages | 20+ (Python, Node.js, Java, Go, Ruby, .NET, etc.) |
| Integrations | 200+ AWS services |
| Default concurrency | Up to 1,000 concurrent executions |
| Max execution time | 15 minutes per invocation |
| Cold start | First invocation may be slightly slower |

### Why Lambda Exists
Before Lambda, running a small task (like resizing an image) required a full server running 24/7. Lambda lets you run that same task for a fraction of a cent, only when needed.

### How Lambda Works (Step-by-Step)

```
1. Event occurs (e.g., file uploaded to S3)
        ↓
2. AWS detects the trigger
        ↓
3. Lambda spins up a compute container
        ↓
4. Your code runs inside it
        ↓
5. Output is produced (file saved, notification sent, etc.)
        ↓
6. Container is shut down
        ↓
7. You are billed for only the time your code ran
```

### Impact

- ✅ **Used:** No servers to manage, automatic scaling, cost-efficient.
- ❌ **Not used:** You'd need to run EC2 instances round the clock for event-driven tasks — wasteful and expensive.

---

## 3. Project Architecture – Image Resizing

### What
A real-world project that:
1. Accepts image uploads into an S3 bucket
2. Automatically triggers a Lambda function
3. Lambda resizes the image
4. Saves the resized image to another S3 bucket
5. Sends an email notification (success or failure)
6. Logs everything in CloudWatch

### Components

| Component | Role |
|-----------|------|
| S3 Bucket (Source) | Where original images are uploaded |
| S3 Bucket (Destination) | Where resized images are saved |
| AWS Lambda | Runs the image-resizing Python code |
| Python (`create-thumbnail.py`) | 36-line script that performs the resize |
| CloudWatch | Logs execution output and errors |
| SNS | Sends email alerts on success or failure |
| Terraform | Infrastructure-as-Code tool to set up everything |

### How It Works (End-to-End Flow)

```
User uploads image (1.4MB)
        ↓
S3 Source Bucket receives file
        ↓
S3 Event Notification fires
        ↓
Lambda is triggered automatically
        ↓
Python code resizes image (1.4MB → 95KB)
        ↓
Resized image saved to S3 Destination Bucket
        ↓
SNS sends success email notification
        ↓
CloudWatch logs the entire execution
```

### What Happens With Unsupported Files

```
User uploads PDF (8.9MB)
        ↓
Lambda triggered
        ↓
Python code cannot resize a PDF
        ↓
Lambda throws an error
        ↓
SNS sends failure email
        ↓
CloudWatch logs the detailed error message
```

---

## 4. Key AWS Services Involved

### S3 (Simple Storage Service)

**What:** Object storage service to store any file (images, videos, PDFs, etc.).  
**Why used here:** Acts as both input (source) and output (destination) for images.  
**How it triggers Lambda:** S3 has built-in **Event Notifications** – when a file is uploaded, it can automatically call a Lambda function.

---

### SNS (Simple Notification Service)

**What:** A messaging service that sends notifications (email, SMS, push, etc.).  
**Why used here:** To alert the team when an image is processed successfully or when it fails.  
**How:** Lambda publishes a message to an SNS topic → SNS delivers it to subscribed emails.

---

### CloudWatch

**What:** AWS monitoring and logging service.  
**Why used here:** To see what happened inside Lambda – what ran, what failed, how long it took.  
**How:** Lambda automatically sends logs to CloudWatch. You can view execution logs, errors, duration, memory usage.

---

### Terraform

**What:** An Infrastructure-as-Code (IaC) tool that creates and manages cloud resources using configuration files.  
**Why used here:** Instead of clicking through the AWS Console to create S3, Lambda, SNS, IAM roles manually – Terraform does it all automatically with code.  
**How:**
```
terraform init   → Downloads required plugins
terraform plan   → Shows what will be created (preview)
terraform apply  → Creates the actual infrastructure
terraform destroy → Deletes everything (cleanup)
```

---

## 5. Practical Implementation with Terraform

### Prerequisites

1. **AWS Account** – with an IAM user (e.g., "Terraform user") with admin permissions
2. **Access Key & Secret Key** – generated from IAM for programmatic access
3. **Terraform** – binary downloaded and placed in a `bin/` folder
4. **AWS CLI/SDK** – installed (MSI for Windows, PKG for Mac)
5. **Git** – to clone the project code

### Step-by-Step Execution

```bash
# Step 1: Clone the project
git clone <repository-url>
cd <project-folder>

# Step 2: Create terraform.tfvars with your settings
# Contents of terraform.tfvars:
# email        = "your@email.com"
# access_key   = "AKIA..."
# secret_key   = "abc123..."
# source_bucket = "cloud-devops-hub-source"
# dest_bucket   = "cloud-devops-hub-destination"

# Step 3: Initialize Terraform
terraform init

# Step 4: Preview the infrastructure plan
terraform plan
# Output: "9 resources to be added"

# Step 5: Create all infrastructure
terraform apply

# Step 6: Test by uploading an image to S3 source bucket

# Step 7: Cleanup when done
terraform destroy
```

### What Terraform Created (9 Resources)

1. S3 Source Bucket
2. S3 Destination Bucket
3. S3 Event Notification (trigger)
4. Lambda Function
5. Lambda IAM Role
6. Lambda IAM Policy
7. SNS Topic
8. SNS Email Subscription
9. CloudWatch Log Group

---

## 6. How Lambda Triggering Works

### Event-Driven Model

Lambda does **not run continuously**. It only runs when something triggers it. This is called **event-driven architecture**.

```
Event Source          Trigger             Lambda Action
──────────────────────────────────────────────────────
S3 file upload   →   S3 Event        →   Resize image
API Gateway req  →   HTTP Request    →   Return response
DynamoDB change  →   Stream Event    →   Process record
CloudWatch rule  →   Scheduled Cron  →   Run daily task
SNS message      →   Topic publish   →   Handle alert
```

### Concurrency

Lambda can handle **many requests simultaneously** – up to 1,000 concurrent executions by default. If 500 images are uploaded at once, Lambda spins up 500 parallel instances automatically.

---

## 7. Visual Diagrams

### 7.1 – Overall Project Architecture

```
┌─────────────┐     Upload      ┌──────────────────┐
│    User     │ ──────────────► │  S3 Source Bucket│
└─────────────┘                 └────────┬─────────┘
                                         │
                                  S3 Event Trigger
                                         │
                                         ▼
                                ┌─────────────────┐
                                │   AWS Lambda    │
                                │  (Python code)  │
                                │  Resize Image   │
                                └────┬────────┬───┘
                                     │        │
                          Success ───┘        └─── Failure
                              │                      │
                ┌─────────────▼──────┐    ┌──────────▼─────────┐
                │  S3 Dest Bucket    │    │   CloudWatch Logs  │
                │  (Resized image)   │    │   (Error details)  │
                └────────────────────┘    └────────────────────┘
                              │
                    ┌─────────▼─────────┐
                    │       SNS         │
                    │  Email Alert      │
                    │ success/failure   │
                    └───────────────────┘
```

---

### 7.2 – Lambda Execution Lifecycle

```
  Trigger Fires
       │
       ▼
  ┌─────────────────────────────────┐
  │  Cold Start (first invocation)  │  ← Slightly slower
  │  - Container created            │
  │  - Runtime initialized          │
  │  - Code loaded                  │
  └────────────┬────────────────────┘
               │
               ▼
  ┌─────────────────────────────────┐
  │        Handler Executes         │  ← Your code runs here
  │  - Event object received        │
  │  - Business logic runs          │
  │  - Response returned            │
  └────────────┬────────────────────┘
               │
               ▼
  ┌─────────────────────────────────┐
  │    Warm Container (reused)      │  ← Faster for next call
  │    or Shutdown after idle       │
  └─────────────────────────────────┘
```

---

### 7.3 – Terraform Workflow

```
terraform.tfvars (your config)
         │
         ▼
  terraform init ──► Downloads providers & plugins
         │
         ▼
  terraform plan ──► Previews what will change (dry run)
         │
         ▼
  terraform apply ──► Creates real AWS infrastructure
         │
         ▼
  [Test your project]
         │
         ▼
  terraform destroy ──► Removes all created resources
```

---

### 7.4 – Serverless vs Traditional Comparison

```
TRADITIONAL (EC2-based):
────────────────────────────────────────────────────────
[Server Running 24/7] ──► Always consuming cost & resources
        │
        ├── 0 requests at 3 AM?   Still paying. Still running.
        └── 1000 requests at noon? Must manually scale.


SERVERLESS (Lambda-based):
────────────────────────────────────────────────────────
[0 requests] → No cost, nothing running
        │
        ├── Request arrives → Lambda spins up → Runs → Shuts down
        └── 1000 requests → 1000 parallel Lambdas auto-created
```

---

## 8. Scenario-Based Q&A

---

🔍 **Scenario 1:** Your company has an e-commerce site. Users upload product photos. The site needs thumbnails for listings and full-size for detail pages. Running a server just for this seems wasteful.

✅ **Answer:** Use AWS Lambda with S3 triggers. When a product photo is uploaded to the source bucket, Lambda automatically resizes it into multiple sizes (thumbnail, medium, full) and stores them in a destination bucket. You pay only when images are uploaded, not 24/7.

---

🔍 **Scenario 2:** A Lambda function fails when processing a file. Your team needs to know what went wrong and why.

✅ **Answer:** Lambda automatically sends all logs (print statements, errors, stack traces) to **CloudWatch Logs**. You can view the log group for that Lambda function, filter by error, and see the exact line of code that failed and the error message.

---

🔍 **Scenario 3:** A non-image file (like a PDF or `.txt`) accidentally gets uploaded to the image processing bucket. What happens?

✅ **Answer:** Lambda is still triggered (it doesn't know the file type before running). Your Python code attempts to open it as an image and fails. Lambda logs the error to **CloudWatch**, and **SNS** sends a failure email notification. The bad file is not copied to the destination bucket.

---

🔍 **Scenario 4:** You need to set up the entire image-resizing infrastructure for 5 different environments (dev, staging, QA, prod, demo). Doing it manually via the console is error-prone.

✅ **Answer:** Use **Terraform**. Write the infrastructure once as code (`main.tf`, `terraform.tfvars`). For each environment, just change the variable values and run `terraform apply`. All 9 resources are created consistently and repeatably.

---

🔍 **Scenario 5:** During a flash sale, 10,000 product images are uploaded simultaneously. Will Lambda handle it?

✅ **Answer:** Yes. Lambda automatically scales concurrently. Each image upload triggers a separate Lambda invocation. AWS will run up to 1,000 concurrent executions by default (this limit can be increased). All 10,000 images will be processed rapidly in parallel.

---

## 9. Interview Q&A

---

**Q1. What is AWS Lambda and how is it different from EC2?**

> **A:** AWS Lambda is a serverless compute service where you upload code (a function) and AWS runs it in response to events — without you provisioning or managing any server. EC2 is a virtual machine you rent and manage yourself. Lambda charges per millisecond of execution; EC2 charges per hour even when idle. Lambda auto-scales; EC2 requires manual or auto-scaling setup.

---

**Q2. What does "serverless" actually mean?**

> **A:** Serverless doesn't mean no servers — it means the *developer* doesn't manage servers. The cloud provider (AWS) handles all server provisioning, OS management, patching, scaling, and availability. You just write code.

---

**Q3. How does Lambda get triggered? Give examples.**

> **A:** Lambda uses an event-driven model. Triggers include:
> - **S3** – file uploaded/deleted
> - **API Gateway** – HTTP request received
> - **DynamoDB Streams** – database record changed
> - **CloudWatch Events** – scheduled time (cron-like)
> - **SNS/SQS** – message published to a queue or topic
> - **Cognito** – user sign-up event

---

**Q4. What is a cold start in Lambda?**

> **A:** When Lambda hasn't been invoked recently, AWS needs to spin up a new container, load the runtime, and initialize your code — this first-time setup is called a **cold start** and adds latency (typically 100ms–1s). Subsequent invocations reuse the same "warm" container and are faster. You can minimize cold starts by using provisioned concurrency or keeping Lambda warm with scheduled pings.

---

**Q5. What is the maximum execution time for a Lambda function?**

> **A:** 15 minutes (900 seconds) per invocation. Lambda is designed for short-lived tasks. For long-running workloads, use EC2, ECS, or Step Functions.

---

**Q6. How does Terraform help in this project?**

> **A:** Terraform is an Infrastructure-as-Code tool. Instead of manually clicking through the AWS Console to create S3 buckets, Lambda functions, IAM roles, SNS topics, etc., Terraform automates all of it from configuration files. Key commands:
> - `terraform init` – set up
> - `terraform plan` – preview
> - `terraform apply` – create
> - `terraform destroy` – delete
> This makes infrastructure repeatable, version-controllable, and consistent across environments.

---

**Q7. What is the role of CloudWatch in a Lambda-based system?**

> **A:** CloudWatch is AWS's monitoring and logging service. Lambda automatically sends all stdout/stderr output and execution metadata to CloudWatch Logs. You can use it to debug errors, monitor function duration, track invocation count, set alarms on error rates, and trace performance issues.

---

**Q8. What is SNS and why is it used in this project?**

> **A:** SNS (Simple Notification Service) is a publish-subscribe messaging service. In this project, after Lambda finishes processing an image, it publishes a message to an SNS topic. Anyone subscribed to that topic (like an email address) receives the notification. This provides real-time alerts for both successful processing and failures.

---

**Q9. What happens if 500 images are uploaded to S3 at the same time?**

> **A:** Lambda auto-scales. Each S3 upload event triggers a separate Lambda invocation. AWS will spin up up to 1,000 concurrent Lambda instances (default limit, can be raised). All 500 images will be processed in parallel without any manual intervention.

---

**Q10. What are the Lambda free tier limits?**

> **A:** AWS Lambda's free tier (permanent, not just first year) includes:
> - **1 million requests** per month
> - **400,000 GB-seconds** of compute time per month
> This is typically more than enough for small projects and learning.

---

## Quick Reference Summary

```
┌──────────────────────────────────────────────────────────┐
│                    AWS LAMBDA CHEAT SHEET                │
├──────────────────┬───────────────────────────────────────┤
│ Type             │ Serverless Compute                    │
│ Billing          │ Per millisecond                       │
│ Free Tier        │ 1M requests/month                     │
│ Max Runtime      │ 15 minutes                            │
│ Concurrency      │ 1,000+ simultaneous executions        │
│ Languages        │ Python, Node, Java, Go, Ruby, .NET... │
│ Trigger Types    │ S3, API GW, DynamoDB, SNS, SQS, CW   │
│ Monitoring       │ CloudWatch Logs & Metrics             │
│ Notifications    │ SNS (email, SMS, push)                │
│ IaC Tool Used    │ Terraform                             │
└──────────────────┴───────────────────────────────────────┘
```

---

*Notes generated from class session on AWS Lambda Serverless Architecture – Image Resizing Project.*

> ← Previous: [`22_aws_cloudwatch_monitoring_and_billing`](22_aws_cloudwatch_monitoring_and_billing.md) | Next: [`24_Git_&_GitHub_Fundamentals.md`](24_Git_&_GitHub_Fundamentals.md) →