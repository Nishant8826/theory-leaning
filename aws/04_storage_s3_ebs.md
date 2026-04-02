# Storage: S3 and EBS

---

### 2. What
Data comes in different structures. AWS provides specific storage services depending on exactly how your application needs to read that data.
- **S3 (Simple Storage Service):** An "Object Store". You upload raw files (PDFs, Images, Videos) into "Buckets". S3 is infinitely scalable, meaning you can store 1 file or 1 billion files without ever running out of space.
- **EBS (Elastic Block Store):** A traditional hard drive. It is a physical block volume that you explicitly plug into a single EC2 Virtual Machine. If you install Ubuntu on an EC2 instance, the OS is installed on an EBS volume.

✅ **Simple Analogy:**
- **S3:** A massive global Dropbox account. You access files over the internet using URLs.
- **EBS:** A physical USB Hard Drive. You literally have to plug it into your computer (EC2 instance) to format and read it.

---

### 3. Why
If you build a social media app where users upload 10,000 photos an hour, you cannot store them on the EC2's internal EBS hard drive. The hard drive will fill up and crash your server! Furthermore, EC2 servers are ephemeral (temporary). If the server gets deleted, the attached EBS drive is usually deleted with it. **All user-uploaded files must go to S3.** 

---

### 4. How
When building full-stack applications locally, you interact with S3 via the official AWS SDK in Node.js, and interact with EBS primarily through the AWS CLI when provisioning servers.

---

### 5. Implementation

**A. S3 Bucket Basics via CLI**

```bash
# 1. Create a brand new globally unique S3 bucket 
aws s3 mb s3://my-cool-social-media-bucket-999

# 2. Upload a local image file directly to the bucket
aws s3 cp ./local-avatar.png s3://my-cool-social-media-bucket-999/avatars/user1.png

# 3. List all files currently sitting inside the bucket
aws s3 ls s3://my-cool-social-media-bucket-999/avatars/
```

**B. EBS Rules!**
You rarely touch EBS through code. Just remember: When you ran the `aws ec2 run-instances` command in the previous lesson, AWS automatically created a new 8GB EBS block drive and attached it to your new Ubuntu instance behind the scenes!

---

### 6. Steps (Handling User Uploads)
1. User selects a Profile Picture in React.
2. React uploads the file (via signed URLs) to your designated S3 Bucket.
3. S3 returns a permanent file URL.
4. React sends that URL to your Node.js backend.
5. Your backend saves just the String URL (`https://s3.amazonaws.com/...`) into the database, NOT the raw image!

---

### 7. Integration

🧠 **Think Like This:**
* **Frontend Hosting:** Are you hosting a static React application? Because it's just raw HTML/JS *files*, you can actually upload your entire React app purely into an S3 bucket and configure it to act as a web server! It costs pennies securely!

---

### 8. Impact
📌 **Real-World Scenario:** Twitter cannot store petabytes of profile pictures on active EC2 servers. They use massive Object Storage systems like S3 safely. S3 automatically replicates those images across 3 different Availability Zones quietly, ensuring that even if an entire data center catches fire, no images are ever lost.

---

### 9. Interview Questions

Q1. What is the fundamental difference between S3 and EBS?
Answer: S3 is a highly scalable Object Storage system accessed globally via HTTP REST APIs. EBS is Block Storage that acts as a physical hard drive directly attached to a single EC2 instance utilizing local file paths.

Q2. Can multiple EC2 instances attach to the exact same EBS volume simultaneously?
Answer: Generally no. A standard EBS volume can only be mounted to a single EC2 instance at a time, similarly to how a physical internal hard drive can only be plugged into one motherboard.

Q3. What is an S3 Bucket?
Answer: A logical container in Amazon S3 for grouping and storing objects (files). Bucket names must be absolutely globally unique across all AWS accounts worldwide.

Q4. If your EC2 instance crashes and is terminated by AWS, what happens to the attached default root EBS volume?
Answer: By default, the root EBS volume is permanently deleted alongside the terminated EC2 instance to prevent accumulating orphan storage charges, unless the "DeleteOnTermination" flag was manually altered.

Q5. How does S3 ensure durability so you do not lose uploaded files?
Answer: S3 inherently provides "99.999999999% (11 9's) of durability" by transparently replicating every uploaded object across multiple completely isolated Availability Zones independently.

Q6. Why is S3 frequently used to host Client-Side React applications?
Answer: Because React generates static frontend files (`index.html`, `js`, `css`). S3 has a built-in feature to serve static web pages directly, eliminating the need and cost to manage an active EC2 web server entirely.

---

### 10. Summary
* Store raw code and OS Kernels on attached EBS drives.
* Store massive user files, images, and backups in vast S3 Buckets.
* S3 is Object Storage (cheap, infinite scale).
* EBS is Block Storage (fast, single server attachment).

---
Prev : [03_compute_ec2_ubuntu_lambda.md](./03_compute_ec2_ubuntu_lambda.md) | Next : [05_databases_rds_dynamodb.md](./05_databases_rds_dynamodb.md)
