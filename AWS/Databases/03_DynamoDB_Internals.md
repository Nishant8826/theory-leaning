# ⚡ DynamoDB Internals

## 📌 Topic Name
Amazon DynamoDB: The Serverless Key-Value Database

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: A NoSQL database that scales to any amount of data and traffic.
*   **Expert**: DynamoDB is a **Distributed, Multi-Tenant, Partitioned Key-Value Store**. It is built on the principles of the original Dynamo paper (Amazon) and BigTable (Google). It provides single-digit millisecond latency at any scale by automatically partitioning data across thousands of storage nodes using **Consistent Hashing**. It abstracts the "Server" entirely, providing a purely API-based interaction model.

## 🏗️ Mental Model
Think of DynamoDB as a **Infinite Row of Lockers**.
- **Partition Key (PK)**: The locker number.
- **Sort Key (SK)**: The folder inside the locker.
- **Hashing**: A robot that takes your "AccountID" and instantly knows which locker it belongs to.

## ⚡ Actual Behavior
- **Latency**: Consistent performance (e.g., 5ms) whether you have 100 items or 100 billion items.
- **Scaling**: As your data grows or your RCU/WCU (Read/Write Capacity Units) increase, DynamoDB adds more **Partitions** (10GB chunks) behind the scenes.
- **TTL**: Automatically deletes items after a certain timestamp without consuming WCU.

## 🔬 Internal Mechanics
1.  **Partitioning**: DynamoDB uses the **Partition Key** to run a hash function. The result determines the physical partition where the data lives.
2.  **The Request Router**: A stateless fleet of servers that receives your API call, hashes the PK, and forwards the request to the correct Storage Node.
3.  **Storage Nodes**: These run in a 3-node replication group (Paxos-like). A write is only successful when 2 out of 3 nodes acknowledge it.
4.  **Adaptive Capacity**: If one partition is "hot," DynamoDB can temporarily borrow capacity from other partitions to prevent throttling.

## 🔁 Execution Flow (GetItem)
1.  **Request**: `GET Item { PK: 'USER#123' }`.
2.  **Router**: Hashes `'USER#123'` -> Result `A1B2`.
3.  **Metadata**: Looks up which partition handles range `A000-BFFF`.
4.  **Storage Node**: Router sends request to the leader of that partition.
5.  **Response**: Storage node returns the data to the router, then to the client.

## 🧠 Resource Behavior
- **RCU/WCU**:
    - 1 WCU = 1 write per second for 1KB.
    - 1 RCU = 2 eventually consistent reads per second for 4KB.
- **On-Demand vs. Provisioned**: On-demand is pay-per-request (great for spiky traffic); provisioned is cheaper for steady-state workloads.

## 📐 ASCII Diagrams
```text
[ CLIENT ] --(API)--> [ REQUEST ROUTER ]
                            |
           +----------------+----------------+
           | (Hash PK)      |                |
    [ Partition 1 ]  [ Partition 2 ]  [ Partition 3 ]
    (Range: 0-33)    (Range: 34-66)   (Range: 67-100)
           |
    [ Node A (Leader) ] <---(Paxos)---> [ Node B ] [ Node C ]
```

## 🔍 Code / IaC (Terraform)
```hcl
resource "aws_dynamodb_table" "users" {
  name           = "UsersTable"
  billing_mode   = "PAY_PER_REQUEST" # On-Demand
  hash_key       = "UserID"          # Partition Key
  range_key      = "CreatedAt"       # Sort Key

  attribute {
    name = "UserID"
    type = "S"
  }

  attribute {
    name = "CreatedAt"
    type = "N"
  }

  # Global Secondary Index
  global_secondary_index {
    name               = "EmailIndex"
    hash_key           = "Email"
    projection_type    = "ALL"
  }

  attribute {
    name = "Email"
    type = "S"
  }
}
```

## 💥 Production Failures
1.  **Hot Key Throttling**: 90% of your traffic hits a single Partition Key (e.g., a "Celebrity" user). Even if you have 10,000 WCU, that single partition is limited to 1,000 WCU, and you get throttled.
2.  **GSI Bottleneck**: A Global Secondary Index (GSI) has its own throughput. If you write to the main table faster than the GSI can keep up, it can cause backpressure and throttle writes on the *main* table.
3.  **Large Item Size**: An item grows larger than 400KB. DynamoDB rejects the write. **Solution**: Move large attributes to S3 and store the URL in DynamoDB.

## 🧪 Real-time Q&A
*   **Q**: What is the difference between GSI and LSI?
*   **A**: LSI (Local Secondary Index) shares the PK with the table but has a different SK; it must be created when the table is created. GSI has a different PK and SK and can be added later. GSIs are almost always preferred.
*   **Q**: Is DynamoDB eventually consistent?
*   **A**: By default, yes. You can request "Strongly Consistent" reads at the cost of 2x RCU.

## ⚠️ Edge Cases
*   **Scan vs Query**: `Query` uses the PK to find a specific partition. `Scan` reads EVERY item in the table. Never use `Scan` in production.
*   **Optimistic Locking**: Using `ConditionExpression` (e.g., `SET version = version + 1 WHERE version = current_version`) to prevent lost updates in concurrent environments.

## 🏢 Best Practices
1.  **One-Table Design**: Store multiple entity types in the same table to reduce the number of round trips (advanced pattern).
2.  **Short Attribute Names**: Attribute names (like "FirstName") count towards storage and throughput. Use short codes (like "fn") for huge tables.
3.  **DAX**: Use DynamoDB Accelerator (DAX) for microsecond latency for read-heavy workloads.

## ⚖️ Trade-offs
*   **DynamoDB**: Infinite scale, zero management, but requires strict schema design and NoSQL knowledge.
*   **RDS**: Flexible queries (SQL), join support, but limited horizontal scaling.

## 💼 Interview Q&A
*   **Q**: How do you handle a "Hot Partition" in DynamoDB?
*   **A**: 1. Add a "random suffix" to the PK to distribute the load across more partitions. 2. Use a cache like Redis or DAX to offload reads. 3. Re-evaluate the data model to choose a more high-cardinality Partition Key.

## 🧩 Practice Problems
1.  Design a DynamoDB schema for a "Twitter-like" feed where users can follow others and see their tweets in chronological order.
2.  Calculate the cost of writing 10,000 items per second (each 2KB) using On-Demand pricing.

---
Prev: [02_Aurora_Architecture.md](../Databases/02_Aurora_Architecture.md) | Index: [Docker/00_Index.md](../00_Index.md) | Next: [04_Partitioning_and_Hot_Keys.md](../Databases/04_Partitioning_and_Hot_Keys.md)
---
