# ☁️ AWS S3: Complete Guide and Static Website Hosting

> **File:** `16_aws-s3-static-website-hosting.md`
> **Topic:** S3 Fundamentals, Buckets, Objects, Versioning, Static Website Hosting
> **Level:** 🟢 Beginner Friendly
> **Prerequisites:** [14_AWS_EC2_AMI_EBS_LoadBalancer.md](./14_AWS_EC2_AMI_EBS_LoadBalancer.md)

---

## 📚 Table of Contents

1. [Introduction to AWS S3](#1-introduction-to-aws-s3)
2. [Key Concepts: Buckets and Objects](#2-key-concepts-buckets-and-objects)
3. [Understanding Data Sizes](#3-understanding-data-sizes-kb-mb-gb-tb)
4. [Object Storage vs Traditional Storage](#4-object-storage-vs-traditional-storage)
5. [Durability and Availability](#5-durability-and-availability)
6. [Pricing and Management](#6-pricing-and-management)
7. [Advanced Features](#7-advanced-features)
8. [Hands-on: Static Website Hosting](#8-hands-on-static-website-hosting)
9. [Real-World Examples](#9-real-world-examples)
10. [Practical Scenarios / Tasks](#10-practical-scenarios--tasks)
11. [Common Mistakes](#11-common-mistakes-beginners-make)
12. [DevOps Best Practices](#12-devops-best-practices)
13. [Interview Questions](#13-interview-questions)

---

AWS **S3 (Simple Storage Service)** is one of the most fundamental services in the AWS cloud. It is an object storage service that offers industry-leading scalability, data availability, security, and performance.

---

## 1. Introduction to AWS S3

### What (Definition)
AWS S3 is "Object Storage" in the cloud. Think of it as an **infinite Google Drive or Dropbox** for your code, images, videos, and backups.

### Why (Purpose / Need)
Traditional hard drives have size limits. If you need to store millions of profile pictures, you can't just keep adding hard drives to your server. S3 allows you to store and retrieve any amount of data from anywhere on the web.

### How (Step-by-step Working)
1. You create a container called a **Bucket**.
2. You upload files called **Objects** into that bucket.
3. You access them via a unique URL.

### Impact (Real-world Importance)
Almost every modern app (Netflix, Airbnb, Pinterest) uses S3 to store its static assets (images, videos, logs). Without S3, scaling storage would be a nightmare.

---

## 2. Key Concepts: Buckets and Objects

### Buckets
- A **Bucket** is like a root folder.
- **Global Uniqueness**: S3 bucket names must be globally unique because each bucket name becomes part of a public URL ``` https://my-portfolio.s3.amazonaws.com ```, and just like domain names(DNS) on the internet, only one unique name can exist worldwide to avoid conflicts, ensure correct data routing, and maintain security and proper access across all AWS users.

### Objects
- **An Object** is the file (and any metadata).
- **Total Size Limit**: A single object can be up to **5 TB**.
- **Single Upload Limit**: You can upload a maximum of **5 GB** in a single `PUT` operation (e.g., via the AWS Console). For files larger than 5 GB, you must use **Multipart Upload** (available via CLI or SDKs).

### ASCII Diagram: How S3 Stores Data
```text
[ AWS CLOUD ]
      |
      +---- [ Bucket: "my-app-data" (Unique Name) ]
               |
               +--- [ Object: "logo.png" ]
               |--- [ Object: "video.mp4" ]
               |--- [ Object: "v2/script.js" ] (Folders are fake; they are part of the "key")
```

---

## 3. Understanding Data Sizes (KB, MB, GB, TB)

To understand S3 limits (like the 5 TB single-object limit), you need to know how data is measured in the digital world.

| Unit | Full Name | Equivalent | Real-world Example |
| :--- | :--- | :--- | :--- |
| **KB** | Kilobyte | 1,024 Bytes | A small text file or a low-resolution icon. |
| **MB** | Megabyte | 1,024 KB | A high-quality photo or a 1-minute song. |
| **GB** | Gigabyte | 1,024 MB | A 2-hour HD movie or a large game installer. |
| **TB** | Terabyte | 1,024 GB | Roughly 250,000 photos or 500 HD movies. |
| **PB** | Petabyte | 1,024 TB | Massive data centers or backup archives. |
| **EB** | Exabyte | 1,024 PB | Approximately 50,000 years of HD video! |

### Why 1,024 instead of 1,000?
Computers operate on a **binary system** (0s and 1s). $2^{10} = 1,024$, which is the closest power of two to 1,000. In DevOps and Cloud, we use this 1,024-based calculation for precision.

---

## 4. Object Storage vs Traditional Storage

| Feature | Object Storage (S3) | Traditional Block Storage (EBS/Hard Drive) |
| :--- | :--- | :--- |
| **Structure** | Flat (Bucket -> Object) | Hierarchical (Folders -> Subfolders) |
| **Accessibility** | Accessible via URL (HTTP/HTTPS) | Must be attached to a server (EC2) |
| **Scaling** | Unlimited scaling automatically | Manual resizing needed |
| **Best For** | Static files, images, backups | OS files, databases, apps |

---

## 5. Durability and Availability

### S3 Durability (11 9’s)
AWS provides **99.999999999% (11 9's)** durability. 
- **What it means**: If you store 10,000,000 objects in S3, you might lose one object every 10,000 years. It is designed to never lose your data.

### S3 Availability
This refers to how "up" and accessible the service is. Usually **99.9%** to **99.99%** depending on the storage class.

### Data Replication across Availability Zones (AZs)
When you upload a file to S3, AWS automatically replicates that file across at least **3 different physical data centers (Availability Zones)** within a Region.

### ASCII Diagram: Data Replication
```text
[ Region: us-east-1 ]
      |
      +---- [ AZ-1 ] ----> [ File Copy A ]
      |
      +---- [ AZ-2 ] ----> [ File Copy B ]
      |
      +---- [ AZ-3 ] ----> [ File Copy C ]
(If one data center burns down, your data is still safe in the other two!)
```

---

## 6. Pricing and Management

### Pricing Model
- **Pay-as-you-go**: You only pay for:
  1. The amount of storage used (GBs per month).
  2. The number of requests (PUT, GET, LIST).
  3. Data Transfer OUT (sending data out of AWS).
- **Free Tier**: AWS offers 5GB of S3 storage for the first 12 months.

### Access Control
1. **IAM Policies**: Control which user in your company can access the bucket.
2. **Bucket Policies**: JSON-based rules attached to the bucket (e.g., "Allow everyone to read files").
3. **ACLs (Access Control Lists)**: Older way to manage access at an individual file level.
4. **Default Privacy**: By default, **everything in S3 is PRIVATE**. You must explicitly "Turn off Block Public Access" to make it public.

---

## 7. Advanced Features

### Versioning
- **What**: Keeps multiple versions of an object in the same bucket.
- **Why**: Protects against accidental deletion or overwrites. You can "roll back" to an older version.

### Data Migration
- **S3 Transfer Acceleration**: Uses Amazon CloudFront’s globally distributed edge locations to speed up long-distance uploads.
- **AWS Snowball**: A physical "suitcase" full of hard drives sent to your office. You load your data (Petabytes) and mail it back to AWS because uploading over the internet would take years.

### Region Limitations
- **Bucket Immovability**: Once a bucket is created in a specific Region (e.g., Mumbai), it stays there. You cannot "move" it; you have to copy the data to a new bucket in another region.

### Deleting Large Data (Scaling Issue)
- **UI Problem**: If a bucket contains a massive amount of data (e.g., **100,000+ objects**), the AWS Console (UI) will often fail, timeout, or refuse to delete/empty the bucket.
- **CLI Solution**: The AWS Command Line Interface is designed for this scale.

**How to delete a heavy bucket via CLI:**
1. **Empty and Delete All-in-One**:
   ```bash
   aws s3 rb s3://your-bucket-name --force
   ```
   *The `--force` flag tells S3 to delete all objects inside first, then delete the bucket itself.*

2. **Just Emptying (Keeping the bucket)**:
   ```bash
   aws s3 rm s3://your-bucket-name --recursive
   ```

---

## 8. Hands-on: Static Website Hosting

You can host a website (HTML, CSS, JS) on S3 without any server (like Nginx or Apache).

### Step-by-step Process

| Step | Action | Why is it needed? |
| :--- | :--- | :--- |
| **1** | **Create Bucket** | To have a container for your website files. |
| **2** | **Upload Files** | To put your `index.html`, `styles.css` into the cloud. |
| **3** | **Disable "Block Public Access"** | By default, S3 is private; the world needs to see your site. |
| **4** | **Add Bucket Policy** | To grant "Read" permission to anonymous users. |
| **5** | **Enable Static Hosting** | Tells S3 to treat the bucket like a web server. |
| **6** | **Set Index Document** | Tells S3 which file to show first (usually `index.html`). |

### ASCII Diagram: Accessing S3 Website
```text
[ User Browser ] ----(Requests: my-site.s3-website.com)----> [ S3 Bucket ]
                                                                 |
[ User ] <----(Serves: index.html)------------------------------+
```

### Example Structure
```text
my-portfolio-bucket/
├── index.html
├── styles.css
├── scripts.js
└── assets/
    ├── me.jpg
    └── logo.svg
```

---

## 9. Real-World Examples

1. **Portfolio Website**: Host your resume and projects for $0.50/month.
2. **App Assets**: Your React app fetches product images from S3.
3. **Log Storage**: EC2 servers push daily logs to S3 for long-term storage.
4. **Backup Systems**: Database backups (MySQL dumps) stored safely in S3.

---

## 10. Practical Scenarios / Tasks

### Scenario 1: Host a Portfolio
- Create a bucket named `yourname-portfolio-2024`.
- Upload an `index.html` file.
- Enable Static Website Hosting.
- **Goal**: Access it via the S3 endpoint URL.

### Scenario 2: Secure a Private Bucket
- Create a bucket `company-tax-returns`.
- Ensure "Block Public Access" is **ON**.
- Create an IAM user with only `s3:GetObject` permission.

### Scenario 3: Versioning & Rollback
- Enable versioning on a bucket.
- Upload `v1.txt`.
- Upload `v1.txt` again (with different content).
- Delete the file.
- **Goal**: Restore the deleted file using the "Show Versions" toggle.

---

## 11. Common Mistakes Beginners Make

- **Keeping Buckets Public**: Accidentally leaving sensitive data (customer info) open to the world.
- **Not Enabling Versioning**: Deleting a critical file and realizing there is no "Undo" button.
- **Ignoring Data Transfer Costs**: Thinking storage is the only cost (forgetting about the cost of users downloading files).

---

## 12. DevOps Best Practices

- **Use Infrastructure as Code (IaC)**: Use Terraform or AWS CDK to create buckets instead of clicking in the console.
- **Enable Encryption**: Always enable SSE-S3 (Server-Side Encryption) for security.
- **Lifecycle Policies**: Automatically move old files to "S3 Glacier" (cheaper storage) after 30 days.
- **Least Privilege**: Grant users only the minimum access they need.

---

## 13. Interview Questions

### Beginner Level
**Q: Can you have two buckets with the same name?**
*A: No. Bucket names are globally unique across all AWS accounts and regions.*

**Q: What is the maximum size of a single file in S3?**
*A: 5 Terabytes (TB).*

### Scenario-based
**Q: Your client deleted a critical configuration file and wants it back. How can you help?**
*A: If "Versioning" was enabled, I can go to the bucket, toggle "Show Versions", and restore the previous version or remove the "Delete Marker".*

**Q: Your website is loading slowly for users in London, but your bucket is in Virginia. What do you do?**
*A: I would use **Amazon CloudFront** (a CDN) to cache the S3 content in Edge Locations closer to London.*

### Tricky Questions
**Q: If you upload a file to S3 and immediately try to read it, will you see the change?**
*A: Yes. S3 provides **Strong Read-after-Write Consistency** for both new objects and updates. (Note: This changed in 2020; previously it was eventual consistency for updates).*

**Q: Can you host a dynamic PHP or Python website on S3?**
*A: No. S3 only hosts **Static** content (HTML, CSS, JS). For PHP/Python, you need a server like EC2 or a service like Lambda.*

---

← Previous: [15_Linux_Practical_Session.md](15_Linux_Practical_Session.md) | Next: [17_S3_Storage_Classes_Lifecycle_RDS.md](17_S3_Storage_Classes_Lifecycle_RDS.md) →
