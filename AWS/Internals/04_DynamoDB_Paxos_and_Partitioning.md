# 🔬 DynamoDB Paxos and Partitioning

## 📌 Topic Name
DynamoDB Internals: Consensus, Replication, and the 10GB Partition Limit

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: DynamoDB scales by splitting your data into small pieces and replicating them for safety.
*   **Expert**: DynamoDB is a **Leader-based Partitioned System**. It uses a consensus algorithm (a variant of **Multi-Paxos**) to maintain consistency across replicas and **Consistent Hashing** to distribute data across partitions. Every partition is a 3-node replication group. Writes go to the "Leader" of the partition, which then propagates them to the "Followers."

## 🏗️ Mental Model
Think of DynamoDB as a **Network of 3-Person Committees**.
- **The Table**: A large company with many departments (Partitions).
- **The Department (Partition)**: A committee of 3 people. One is the Chairperson (Leader).
- **A Write**: You tell the Chairperson "Update this record." The Chairperson tells the other 2 people. As soon as ONE other person agrees (Quorum of 2), the update is official.
- **Failover**: If the Chairperson quits, the other 2 people instantly vote for a new leader and keep working.

## ⚡ Actual Behavior
- **Quorum**: A write is successful when 2 out of 3 replicas acknowledge it.
- **Strong Consistency**: If you ask for a "Strongly Consistent Read," DynamoDB always routes your request to the current Leader.
- **Eventual Consistency**: If you don't care about freshness, DynamoDB might route your request to a Follower, which might be a few milliseconds behind.

## 🔬 Internal Mechanics
1.  **Multi-Paxos**: This ensures that all 3 replicas agree on the *order* of operations. This is what makes DynamoDB reliable even during network partitions or hardware failures.
2.  **The 10GB / 3000 RCU / 1000 WCU Rule**: This is the physical limit of a single DynamoDB partition. When you exceed any of these, DynamoDB **splits** the partition into two, creating new "Committees" and redistributing the hash ranges.
3.  **Log-Structured Storage**: Internally, DynamoDB writes data to an append-only log (similar to LSM trees), which is why writes are so fast and predictable.

## 🔁 Execution Flow (The Write Path)
1.  **Request**: Client sends `PutItem` to Request Router.
2.  **Hashing**: Router hashes the Partition Key to find the target Partition.
3.  **Leader**: Router sends the request to the Leader of that Partition's replication group.
4.  **Proposal**: Leader sends a Paxos proposal to the 2 Followers.
5.  **Quorum**: Once one Follower ACKs, the Leader commits the write to its local log.
6.  **Response**: Leader returns "Success" to the Client.
7.  **Propagation**: The second Follower eventually receives and commits the write.

## 🧠 Resource Behavior
- **Heat Management**: DynamoDB monitors the load on physical storage nodes. If one node is getting too much traffic (even if it's multiple different partitions), it will move some partitions to a "colder" node.
- **Burst Capacity**: Every partition has a small "bucket" of unused capacity it can use for short-term spikes.

## 📐 ASCII Diagrams
```text
[ REQUEST ROUTER ] --(Hash PK)--> [ PARTITION 3 LEADER ]
                                         |
                   +---------------------+---------------------+
                   | (Paxos Proposal)                          |
          [ FOLLOWER A ]                                [ FOLLOWER B ]
          (ACK) <---------------------------------------(Eventually ACK)
```

## 🔍 Code / Insights (Checking Partitions)
```bash
# You can't see partitions directly, but you can infer them.
# A table with 40,000 RCU will have at least 14 partitions (40,000 / 3,000).
aws dynamodb describe-table --table-name MyTable
```

## 💥 Production Failures
1.  **Leader Election Latency**: If a Leader fails, there is a sub-second gap where the partition is unavailable while a new Leader is elected. If you have thousands of partitions, this can happen occasionally.
2.  **Split Brain**: Paxos is designed to prevent this, but an extremely severe network partition can cause a "Quorum Failure" where the partition becomes read-only because it can't find a majority.
3.  **Slow Follower**: If one Follower is slow, it doesn't impact write latency (because 2/3 is enough). But if TWO nodes are slow or down, the whole partition hangs.

## 🧪 Real-time Q&A
*   **Q**: Does DynamoDB use Raft or Paxos?
*   **A**: AWS has stated that DynamoDB uses a variant of Multi-Paxos for its replication groups.
*   **Q**: What happens during a partition split?
*   **A**: DynamoDB creates two new partitions. It copies the data from the old one to the new ones in the background. Once finished, it updates the Request Router's map. This is transparent to the user.

## ⚠️ Edge Cases
*   **Transaction Coordinator**: For multi-item transactions, a separate service coordinates Paxos across multiple different partitions.
*   **Global Tables**: Uses a "Last Writer Wins" (LWW) conflict resolution strategy between regions, built on top of the per-region Paxos logs.

## 🏢 Best Practices
1.  **High-Cardinality PKs**: Ensure your data is spread across as many partitions as possible to avoid "Hot Partitions."
2.  **Understand RCU/WCU limits**: Remember that even if your table has 1 million RCU, a single Partition Key can never exceed 3,000 RCU.
3.  **Use On-Demand** if you don't want to worry about partition management or capacity planning.

## ⚖️ Trade-offs
*   **DynamoDB Paxos**: Guarantees consistency and availability during single-node failure, but limits the write throughput of a single partition to the speed of the hardware node.

## 💼 Interview Q&A
*   **Q**: How does DynamoDB maintain high availability during a node failure?
*   **A**: Every partition in DynamoDB is replicated 3 times across different Availability Zones using a Multi-Paxos consensus group. If the Leader node fails, the two remaining Followers detect the failure and immediately elect a new Leader from among themselves. Because a quorum only requires 2 out of 3 nodes, the system can continue to process writes and reads without interruption.

## 🧩 Practice Problems
1.  Research the "Dynamo" paper (2007) and see how it differs from the current DynamoDB implementation (hint: the original used eventual consistency and "Sloppy Quorum").
2.  Calculate how many partitions a 100GB table with 5,000 WCU will have.

---
Prev: [03_S3_Bit_Rot_and_Durability.md](../Internals/03_S3_Bit_Rot_and_Durability.md) | Index: [Docker/00_Index.md](../00_Index.md) | Next: [05_Eventual_Consistency.md](../Internals/05_Eventual_Consistency.md)
---
