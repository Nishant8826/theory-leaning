# 🧊 Glacier and Archival

## 📌 Topic Name
Amazon S3 Glacier: Cold Storage Architecture for Long-term Preservation

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Low-cost storage for data you rarely need. It takes a long time to get it back.
*   **Expert**: Glacier is a **High-Durability, Offline Storage Tier** optimized for data that is infrequently accessed and has a long retrieval time (minutes to hours). It consists of three tiers: **S3 Glacier Instant Retrieval** (millisecond access), **S3 Glacier Flexible Retrieval** (minutes to hours), and **S3 Glacier Deep Archive** (12+ hours). It is designed to replace tape libraries.

## 🏗️ Mental Model
Think of S3 Storage Tiers as a **Library**.
- **S3 Standard**: The "New Releases" shelf. Right in front of you.
- **S3 Glacier Flexible**: The "Storage Basement." You have to ask the librarian to get it, and it takes an hour.
- **S3 Glacier Deep Archive**: The "Off-site Salt Mine." It's very safe and very cheap, but it takes a day to bring the book back to the library.

## ⚡ Actual Behavior
- **Durability**: Still 11 nines. Your data is safe.
- **Retrieval Cost**: You pay a very low price for storage ($0.00099/GB for Deep Archive) but a significant price to *retrieve* the data.
- **Minimum Storage Duration**: If you delete a file from Deep Archive before 180 days, you still pay for the full 180 days.

## 🔬 Internal Mechanics
1.  **Cold Media**: AWS uses custom-designed hardware for Glacier. While they don't explicitly say "Tape," it is widely believed to be a mix of high-density specialized hard drives that stay powered down or optical/tape-like media.
2.  **Restore Process**: When you request a restore, S3 "rehydrates" the object into the S3 Standard tier (temporarily). You can then access it like any other object.
3.  **Glacier Select**: Just like S3 Select, you can run queries against Glacier data without restoring the entire object, which can save time and money.

## 🔁 Execution Flow (Restoring from Deep Archive)
1.  **Request**: `RestoreObject` API call.
2.  **Tier Selection**: Bulk (12-48 hours) or Standard (12 hours).
3.  **Wait**: AWS internal systems locate the data and copy it to the S3 Standard storage area.
4.  **Completion**: The object's "Restoration Status" changes to "Restored."
5.  **Access**: You download the file.
6.  **Expiry**: After the "Days" period you specified, the restored copy is deleted (the Glacier copy remains).

## 🧠 Resource Behavior
- **Vault Lock**: A feature for compliance. Once a policy is locked, NO ONE (not even the root user) can delete the data until the retention period expires.
- **Inventory**: Glacier vaults can have an inventory of their contents, but it is only updated once a day.

## 📐 ASCII Diagrams
```text
[ ACTIVE DATA ] --(Lifecycle Rule)--> [ GLACIER FLEXIBLE ]
                                            |
                                  [ ARCHIVAL STORAGE ]
                                  (Dormant/Powered Down)
                                            |
                                  (Restore Request)
                                            |
[ RESTORED DATA ] <---(12-48 Hours)--- [ REHYDRATION ]
(Temporary in S3 Std)
```

## 🔍 Code / IaC (Terraform)
```hcl
# Lifecycle rule to move data to Deep Archive
resource "aws_s3_bucket_lifecycle_configuration" "archive_rule" {
  bucket = aws_s3_bucket.my_data.id

  rule {
    id     = "archive-old-logs"
    status = "Enabled"

    transition {
      days          = 90
      storage_class = "GLACIER_IR" # Instant Retrieval
    }

    transition {
      days          = 180
      storage_class = "DEEP_ARCHIVE"
    }
  }
}
```

## 💥 Production Failures
1.  **Retrieval Bill Shock**: Restoring 100TB from Deep Archive using "Standard" retrieval. The retrieval fees can be higher than the storage costs for the last year.
2.  **Minimum Object Size**: Glacier has a 40KB minimum for storage billing. If you store millions of 1KB files, you are paying for 40KB for each, essentially paying 40x more than expected. **Solution**: Zip small files before archiving.
3.  **Premature Deletion**: Moving data to Glacier and deleting it 10 days later, incurring 80 days of "Early Deletion" penalty.

## 🧪 Real-time Q&A
*   **Q**: When should I use Glacier Instant Retrieval?
*   **A**: For data you access once or twice a quarter but need immediately when you do (e.g., medical records, old user photos).
*   **Q**: Can I see my files in the AWS Console if they are in Glacier?
*   **A**: Yes, the metadata (keys) is always visible in the S3 bucket listing.

## ⚠️ Edge Cases
*   **Glacier Direct vs S3 Glacier**: You can use the "Glacier" service directly (Vaults), but AWS recommends using S3 with the Glacier storage classes for a better developer experience and unified API.
*   **Expedited Retrieval**: Not available for Deep Archive. Only available for Flexible Retrieval (1-5 minutes).

## 🏢 Best Practices
1.  **Batch Small Files**: Aggregate logs into larger files before archiving.
2.  **Use Lifecycle Policies**: Don't manually move files to Glacier; let S3 do it based on age.
3.  **Vault Lock for Compliance**: Use it for SEC or HIPAA requirements where data must be immutable for X years.

## ⚖️ Trade-offs
*   **Deep Archive**: Lowest cost ($1/TB/month) but highest latency and highest retrieval effort.
*   **Standard**: Highest cost ($23/TB/month) but lowest latency.

## 💼 Interview Q&A
*   **Q**: How do you handle a request to restore a specific file from Deep Archive as quickly as possible?
*   **A**: I would check if it's in Deep Archive or Flexible Retrieval. If it's in Deep Archive, the "quickest" is ~12 hours. I would initiate a "Standard" retrieval. If it were in Flexible Retrieval, I could use "Expedited" retrieval to get it in 1-5 minutes.

## 🧩 Practice Problems
1.  Calculate the cost of storing 1PB of data in Deep Archive for 5 years vs. S3 Standard.
2.  Initiate a restore of a test file from Glacier and monitor its status via the AWS CLI.

---
Prev: [03_EBS_vs_EFS.md](../Storage/03_EBS_vs_EFS.md) | Index: [Docker/00_Index.md](../00_Index.md) | Next: [05_Data_Lifecycle_Policies.md](../Storage/05_Data_Lifecycle_Policies.md)
---
