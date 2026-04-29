# 🔄 Data Lifecycle Policies

## 📌 Topic Name
S3 Lifecycle Management: Automating the Data Journey

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Set rules to delete old files or move them to cheaper storage.
*   **Expert**: Lifecycle Policies are a **Declarative State Machine** for object storage. They allow you to define a set of transitions and expirations based on object age, prefix, or tags. A Staff engineer uses lifecycle policies to optimize for the **TCO (Total Cost of Ownership)** of data, ensuring that the cost of storing a byte decreases as its value (access frequency) decreases over time.

## 🏗️ Mental Model
Think of Lifecycle Policies as a **Conveyor Belt**.
1.  **S3 Standard**: The fresh produce (Hot data).
2.  **S3 Standard-IA**: The pantry (Warm data).
3.  **S3 Glacier**: The freezer (Cold data).
4.  **Trash**: The compost bin (Expired data).
The conveyor belt moves the boxes automatically based on the date on the box.

## ⚡ Actual Behavior
- **Daily Execution**: S3 evaluates lifecycle rules once a day. Changes might not be visible immediately.
- **Price Optimization**: It’s not just about storage cost; lifecycle rules also help avoid "Object Management" fees by cleaning up non-current versions.
- **Filtering**: Rules can apply to the whole bucket, specific prefixes (e.g., `logs/`), or objects with specific tags.

## 🔬 Internal Mechanics
1.  **Transition vs Expiration**:
    *   **Transition**: Changes the `StorageClass` of an object.
    *   **Expiration**: Deletes the object (or creates a delete marker if versioning is on).
2.  **Non-current Version Actions**: If versioning is on, you can have separate rules for the "Live" version and "Old" versions. (e.g., "Keep the live version forever, but delete old versions after 30 days").
3.  **Intelligent Tiering**: A special storage class that automatically moves data between frequent and infrequent access tiers based on actual usage patterns, without you needing to write lifecycle rules.

## 🔁 Execution Flow
1.  **Rule Definition**: "Move `logs/` to Glacier after 30 days."
2.  **S3 Engine Scan**: The background lifecycle engine scans the bucket index.
3.  **Matching**: Identifies objects with key `logs/...` older than 30 days.
4.  **Action**: Marks objects for transition.
5.  **Completion**: S3 moves the bytes to the target storage class.

## 🧠 Resource Behavior
- **Waterfall Effect**: You must transition in order of "temperature" (Standard -> IA -> Glacier -> Deep Archive). You cannot transition "up" the chain (e.g., Glacier -> Standard) via lifecycle rules.
- **Versioning**: When a lifecycle rule expires a versioned object, it adds a "Delete Marker." You can have a rule to clean up "Expired Object Delete Markers" to save on index overhead.

## 📐 ASCII Diagrams
```text
[ TIME ] ---------------------------------------------------------->
[ DATA ] [ S3 STANDARD ] -> [ S3 IA ] -> [ GLACIER ] -> [ DELETE ]
           (Day 0-30)       (Day 30-90)  (Day 90-365)   (Day 366+)
               |               |              |             |
           ($0.023/GB)     ($0.0125/GB)   ($0.004/GB)     ($0)
```

## 🔍 Code / IaC (Terraform)
```hcl
resource "aws_s3_bucket_lifecycle_configuration" "complex_policy" {
  bucket = aws_s3_bucket.my_data.id

  # Rule for Log files
  rule {
    id     = "log-management"
    status = "Enabled"
    filter {
      prefix = "logs/"
    }

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    expiration {
      days = 90
    }
  }

  # Rule for non-current versions (clean up history)
  rule {
    id     = "version-cleanup"
    status = "Enabled"

    noncurrent_version_expiration {
      noncurrent_days = 30
    }
  }
}
```

## 💥 Production Failures
1.  **The "IA" Cost Trap**: Standard-IA has a minimum storage duration of 30 days. If you move a file to IA and then delete it 2 days later, you pay for 30 days. If your data is very short-lived, lifecycle rules can *increase* your cost.
2.  **Small Object Overhead**: Standard-IA and Glacier have minimum object sizes (128KB and 40KB). Moving millions of 1KB files to IA will cost significantly MORE than keeping them in Standard.
3.  **Conflicting Rules**: Two rules with overlapping filters but different actions. S3 generally picks the "least cost" or "most restrictive" path, but it can lead to unexpected deletions.

## 🧪 Real-time Q&A
*   **Q**: Can I use tags to exclude some files from being deleted?
*   **A**: Yes. You can add a rule filter with a tag (e.g., `Retention=Forever`) and ensure that rule has no expiration action.
*   **Q**: What is "Intelligent Tiering"?
*   **A**: It's a "managed" lifecycle. You pay a small monthly monitoring fee per object, and AWS handles the transitions for you based on actual access patterns.

## ⚠️ Edge Cases
*   **Aborting Incomplete Multipart Uploads**: This is a CRITICAL lifecycle rule. If a large upload fails, the parts stay in S3 and you are billed for them. Always add a rule to delete these after 7 days.
*   **Expired Delete Markers**: If you delete many objects in a versioned bucket, you end up with millions of delete markers that slow down `LIST` operations. Use a lifecycle rule to clean them up.

## 🏢 Best Practices
1.  **Always use Intelligent Tiering** for data with unpredictable access patterns.
2.  **Abort Incomplete Multipart Uploads** in every bucket.
3.  **Archive, don't Delete**: If storage is cheap (Deep Archive), consider archiving instead of permanent deletion for compliance/auditing.

## ⚖️ Trade-offs
*   **Lifecycle Rules (Manual)**: Granular control, zero monitoring fee, but requires maintenance and knowledge of access patterns.
*   **Intelligent Tiering (Managed)**: Set and forget, but has a monitoring fee (not ideal for billions of tiny objects).

## 💼 Interview Q&A
*   **Q**: How would you reduce the cost of an S3 bucket that contains 1PB of data where 90% hasn't been accessed in 6 months?
*   **A**: I would implement a Lifecycle Policy to transition objects older than 30 days to S3 Standard-IA and objects older than 90 days to S3 Glacier Deep Archive. I would also check for non-current versions and incomplete multipart uploads to clean up unnecessary storage.

## 🧩 Practice Problems
1.  Create a lifecycle rule that only applies to objects with the tag `Type=Temporary` and deletes them after 24 hours.
2.  Analyze an S3 storage lens report to identify buckets that would benefit from lifecycle policies.
