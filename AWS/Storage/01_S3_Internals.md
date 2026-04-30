# 📦 S3 Internals

## 📌 Topic Name
Amazon S3: The Infinite Object Store

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Put files in buckets and access them via a URL.
*   **Expert**: S3 is a **Distributed Object Storage System** designed for 99.999999999% (11 nines) of durability. It is a key-value store where the "key" is the file path and the "value" is the data. Unlike a file system, S3 is flat; "folders" are just prefixes in the key name. It uses a **Ring-based Distributed Hash Table (DHT)** to distribute data across hundreds of thousands of physical disks and dozens of data centers.

## 🏗️ Mental Model
Think of S3 as a **Colossal Digital Warehouse**.
- **Bucket**: A specialized floor in the warehouse (Global namespace but Regional data).
- **Object**: A box with a unique ID (Key) and contents (Data).
- **Metadata**: The manifest on the outside of the box (Custom tags, content-type).
- **Prefix**: A sorting system that looks like folders but is really just a naming convention.

## ⚡ Actual Behavior
- **Namespace**: Bucket names must be globally unique across all AWS accounts.
- **Data Location**: When you upload an object, S3 synchronously replicates it across at least 3 AZs before returning a `200 OK`.
- **Scaling**: S3 scales automatically to handle thousands of requests per second. If you exceed 3,500 PUT/COPY/POST or 5,500 GET/HEAD requests per second per prefix, S3 might return a 503 Throttling error.

## 🔬 Internal Mechanics
1.  **Shard and Partitioning**: S3 uses the prefix of the key to determine which internal "shard" of the index to use. 
2.  **Erasure Coding**: To achieve 11 nines of durability, S3 doesn't just make 3 copies. It uses erasure coding to split data into fragments and store them across many disks. Even if multiple disks or an entire data center fails, the data can be reconstructed.
3.  **The Index Plane**: S3 has a separate control plane for the index (where keys live) and the data plane (where bytes live). The index is a massive distributed database.

## 🔁 Execution Flow (PUT Request)
1.  **Client**: Sends `PUT /my-bucket/image.jpg`.
2.  **Load Balancer**: Directs traffic to an S3 Frontend server.
3.  **Auth**: IAM checks bucket policy and ACLs.
4.  **Write Phase**: Data is streamed to the S3 internal storage cluster.
5.  **Replication**: S3 ensures data is written to 3 AZs.
6.  **Index Update**: The index database is updated with the new key.
7.  **Response**: `200 OK` sent to client.

## 🧠 Resource Behavior
- **Immutability**: Objects cannot be "edited." If you change one byte, you must re-upload the entire object.
- **Versioning**: If enabled, S3 stores every version of an object, protecting against accidental deletes or overwrites.

## 📐 ASCII Diagrams
```text
[ CLIENT ] --(PUT)--> [ S3 FRONTEND ]
                         |
      +------------------+------------------+
      |                  |                  |
   [ AZ-A ]           [ AZ-B ]           [ AZ-C ]
   - Data Shard 1     - Data Shard 2     - Data Shard 3
   - Erasure Code A   - Erasure Code B   - Erasure Code C
      |                  |                  |
      +------------------+------------------+
                         |
                 [ SYNC REPLICATION ] --> 200 OK
```

## 🔍 Code / IaC (Terraform)
```hcl
resource "aws_s3_bucket" "data" {
  bucket = "my-staff-level-bucket-2023"
}

resource "aws_s3_bucket_versioning" "data_versioning" {
  bucket = aws_s3_bucket.data.id
  versioning_configuration {
    status = "Enabled"
  }
}

# S3 Bucket Policy (JSON)
resource "aws_s3_bucket_policy" "allow_public_read" {
  bucket = aws_s3_bucket.data.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Principal = "*"
      Action    = "s3:GetObject"
      Effect    = "Allow"
      Resource  = "${aws_s3_bucket.data.arn}/*"
    }]
  })
}
```

## 💥 Production Failures
1.  **Prefix Throttling**: A logging app writes 10,000 files/sec to `s3://my-bucket/logs/2023-01-01/...`. Because they all share the same prefix (`/logs/`), S3 throttles them. **Solution**: Add a random hash prefix: `s3://my-bucket/A1Z2/logs/...`.
2.  **The Public Bucket Leak**: Misconfiguring a bucket policy to `Principal: "*"` and `Action: "s3:*"` allows the whole world to delete your data.
3.  **Incomplete Multipart Uploads**: A large upload starts but fails. S3 keeps the parts that *did* upload. You pay for this storage, but the object isn't visible. **Solution**: Use Lifecycle rules to abort incomplete multipart uploads.

## 🧪 Real-time Q&A
*   **Q**: Is S3 a file system?
*   **A**: No. It is an object store. You cannot "append" to a file or "rename" a folder.
*   **Q**: What is the maximum object size?
*   **A**: 5 TB. However, a single `PUT` operation is limited to 5 GB. Larger objects must use **Multipart Upload**.

## ⚠️ Edge Cases
*   **Consistent Hashing**: S3 used to require randomized prefixes for performance, but as of 2018, AWS redesigned the backend to handle most workloads without manual randomization. However, for extreme scale (>5000 requests/sec), randomization is still a best practice.
*   **S3 Select**: Allows you to run SQL queries against objects (CSV, JSON, Parquet) directly in S3, reducing data transfer by only pulling the rows/columns you need.

## 🏢 Best Practices
1.  **Block Public Access**: Always enable the "S3 Block Public Access" feature at the account level.
2.  **KMS Encryption**: Always enable server-side encryption (SSE-KMS).
3.  **VPC Endpoints**: Use Gateway VPC Endpoints to avoid NAT Gateway costs for S3 traffic.

## ⚖️ Trade-offs
*   **S3 vs. EBS**: Infinite scale and 11 nines durability vs. ultra-low latency and POSIX compliance.

## 💼 Interview Q&A
*   **Q**: How does S3 achieve 11 nines of durability?
*   **A**: Through massive scale, erasure coding, and synchronous replication across at least 3 geographically separate availability zones. It also performs regular checksums on data at rest and automatically repairs corrupted fragments.

## 🧩 Practice Problems
1.  Set up a lifecycle policy that moves objects to Glacier after 30 days and deletes them after 365 days.
2.  Simulate S3 Throttling by launching 100 threads that all attempt to write to the same prefix simultaneously.

---
Prev: [08_Spot_Instances.md](../Compute/08_Spot_Instances.md) | Index: [Docker/00_Index.md](../00_Index.md) | Next: [02_S3_Consistency_Model.md](../Storage/02_S3_Consistency_Model.md)
---
