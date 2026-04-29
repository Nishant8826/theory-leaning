# 🔥 Partitioning and Hot Keys

## 📌 Topic Name
Data Distribution: Mastering Partitions and Avoiding Throttling

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: AWS splits your database into chunks (partitions) to handle scale. Don't put all your data in one chunk.
*   **Expert**: Partitioning is the **Scalability Engine** for both DynamoDB and Kinesis. In DynamoDB, a partition is a 10GB / 3000 RCU / 1000 WCU unit of storage. A "Hot Key" occurs when the access pattern is disproportionately skewed toward a single **Partition Key**, exhausting the throughput of that specific physical node while the rest of the cluster sits idle. A Staff engineer designs for **High Cardinality** to ensure uniform distribution.

## 🏗️ Mental Model
Think of Partitioning as a **Post Office**.
- **The Partitions**: Mail trucks. Each truck can only carry 1000 letters.
- **The Hot Key**: Everyone in the city sends a letter to the *same* house. One truck is overwhelmed, while the other 99 trucks are empty.
- **Cardinality**: The number of unique "houses." If there are 1 million houses, mail is distributed evenly across all trucks.

## ⚡ Actual Behavior
- **Throughput Dilution**: (Historical) If you had 10,000 WCU and 10 partitions, each partition got 1,000 WCU. If you hit one partition harder, you were throttled.
- **Adaptive Capacity**: (Modern) DynamoDB can now "boost" a hot partition's capacity by borrowing from idle partitions in the same table. However, this has limits and cannot exceed the physical 1,000 WCU / 3,000 RCU limit of a single node.

## 🔬 Internal Mechanics
1.  **Consistent Hashing**: The Partition Key is run through a hash function (e.g., MD5). The result determines which "Locker" (Partition) the data goes into.
2.  **Splitting**: When a partition exceeds 10GB or its throughput limit is exceeded, DynamoDB splits it into two new partitions, redistributing the hash ranges.
3.  **The "Isolation" Problem**: Even with Adaptive Capacity, if multiple "celebrity" keys happen to hash to the same physical node, they will still compete for the same underlying hardware resources (NIC, CPU).

## 🔁 Execution Flow (Partition Lookup)
1.  **Input**: `PartitionKey = "USER#100"`.
2.  **Hash**: `hash("USER#100") -> 0x7F2A`.
3.  **Range Map**: `0x7F2A` falls into the range `0x4000 - 0x7FFF`.
4.  **Routing**: Request is sent to **Partition Node 3**.
5.  **Execution**: Node 3 processes the I/O.

## 🧠 Resource Behavior
- **Cardinality**: A "High Cardinality" key (like `UUID` or `Email`) is good. A "Low Cardinality" key (like `Status="Active"` or `Year=2023`) is bad because it leads to "Mega-Partitions" that cannot be distributed.

## 📐 ASCII Diagrams
```text
[ HASH SPACE: 0000 - FFFF ]
      |
+-----V-----+-----V-----+-----V-----+
| Part 1    | Part 2    | Part 3    |
| (0-5000)  | (5001-A)  | (A001-F)  |
+-----------+-----------+-----------+
      |           |           |
 [ KEY A ]   [ KEY B ]   [ KEY C ]  <--- Even Distribution (Good)
      |           |           |
 [ HOT KEY ] [ HOT KEY ] [ HOT KEY ] <--- All hit Part 1 (THROTTLED)
```

## 🔍 Code / IaC (Terraform)
```hcl
# Designing for high cardinality
resource "aws_dynamodb_table" "proper_partitioning" {
  name     = "Events"
  hash_key = "EventID" # GOOD: High cardinality (UUID)
  # range_key = "Timestamp" 

  attribute {
    name = "EventID"
    type = "S"
  }
}

# ANTI-PATTERN: Low cardinality hash key
# hash_key = "Status" # BAD: Only "Active" or "Inactive"
```

## 💥 Production Failures
1.  **The "Date" Partition Key**: Using `YYYY-MM-DD` as a Partition Key for a high-volume logging app. On any given day, **all** traffic hits the *same* partition (the one for today), leading to massive throttling.
2.  **Sharding Failure**: A developer adds a random suffix (0-9) to a hot key to distribute it. Traffic grows 100x, and even with 10 shards, each shard is now "Hot."
3.  **Burst Exhaustion**: Relying on "Burst Capacity" for a sustained traffic spike. Once the burst bucket is empty, the app suddenly drops from 3000 req/s to 1000 req/s, causing a partial outage.

## 🧪 Real-time Q&A
*   **Q**: How do I find my hot keys?
*   **A**: Use **DynamoDB Contributor Insights**. It provides a real-time graph of the most accessed keys in your table.
*   **Q**: Can I change a Partition Key after the table is created?
*   **A**: No. You must create a new table and migrate the data.

## ⚠️ Edge Cases
*   **Write Sharding**: If you MUST query by a low-cardinality attribute (like `Status`), you can append a random number to the PK (`Active_1`, `Active_2`) and query all shards in parallel.
*   **Kinesis Shard Splitting**: Similar to DynamoDB, if a Kinesis Shard is hot, you must manually "split" it to add more throughput.

## 🏢 Best Practices
1.  **Randomize Keys**: If possible, use UUIDs or hashes for Partition Keys.
2.  **Avoid Time-Series PKs**: Never use the current date/time as a lone PK.
3.  **Cache the Hotest**: Use DAX or ElastiCache to protect your database from "Celebrity" keys that hit the 3000 RCU limit.

## ⚖️ Trade-offs
*   **Read-Efficiency vs. Write-Distribution**: A high-cardinality key is great for writes but can make "range queries" or "group by" operations harder.

## 💼 Interview Q&A
*   **Q**: You have a DynamoDB table for a social media app. Most users are fine, but one user with 10 million followers causes throttling every time they post. How do you solve this?
*   **A**: This is a classic "Hot Key" problem. I would: 1. Use **Write Sharding** (appending a random suffix to the "FollowerID" partition). 2. Implement **Read Caching** using DAX so that followers don't hit the database for every profile view. 3. Ensure the `PostID` is the PK for the actual content, which is naturally high-cardinality.

## 🧩 Practice Problems
1.  Write a script to generate 10,000 requests to a single PK and observe the "ProvisionedThroughputExceededException."
2.  Design a sharding strategy for a leaderboard system where millions of players update their scores.
