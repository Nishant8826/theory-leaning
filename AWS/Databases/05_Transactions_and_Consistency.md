# 🤝 Transactions and Consistency

## 📌 Topic Name
Distributed Transactions: ACID and Base in the AWS Cloud

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Transactions ensure that either all operations succeed or none do. Consistency ensures data is correct.
*   **Expert**: In distributed systems, consistency is a spectrum defined by the **CAP Theorem** (Consistency, Availability, Partition Tolerance). AWS offers **ACID (Atomicity, Consistency, Isolation, Durability)** for relational databases (RDS/Aurora) and **Base (Basically Available, Soft state, Eventual consistency)** for many NoSQL services. However, modern services like DynamoDB and S3 now offer **Strong Consistency** and **Multi-Item Transactions**, bridging the gap between SQL and NoSQL reliability.

## 🏗️ Mental Model
Think of a Transaction as a **Bank Transfer**.
- **Operation A**: Subtract $100 from Account 1.
- **Operation B**: Add $100 to Account 2.
A transaction ensures that if Operation B fails (e.g., the power goes out), Operation A is **rolled back**, and the $100 isn't lost in the ether.

## ⚡ Actual Behavior
- **RDS/Aurora**: Standard SQL transactions (`BEGIN`, `COMMIT`, `ROLLBACK`). Full ACID compliance within a single cluster.
- **DynamoDB Transactions**: `TransactWriteItems` and `TransactGetItems`. Allows up to 100 items or 4MB of data to be updated atomically across one or more tables in the same account/region.
- **S3 Consistency**: Strong Read-After-Write consistency for all operations.

## 🔬 Internal Mechanics
1.  **Two-Phase Commit (2PC)**: Used internally by DynamoDB for transactions.
    - **Prepare Phase**: All partitions involved "lock" the items and verify they can perform the update.
    - **Commit Phase**: If all partitions are ready, the change is committed. If any fail, all are rolled back.
2.  **Isolation Levels**:
    *   RDS: Supports `Read Committed`, `Repeatable Read`, and `Serializable`.
    *   DynamoDB: Transactions are `Serializable`. Non-transactional writes are `Eventual` or `Strong`.
3.  **MvCC (Multi-Version Concurrency Control)**: Aurora and Postgres use MvCC to allow readers to see a consistent snapshot of the data without blocking writers.

## 🔁 Execution Flow (DynamoDB TransactWrite)
1.  **Request**: `TransactWriteItems [ Put(A), Update(B) ]`.
2.  **Coordinator**: A background service receives the request and identifies the partitions for A and B.
3.  **Prepare**: Sends "Can you do this?" to Partition A and Partition B.
4.  **Promise**: Nodes respond "Yes, locked."
5.  **Commit**: Coordinator sends "Do it."
6.  **Response**: Returns success to the client.

## 🧠 Resource Behavior
- **Transaction Conflict**: If two transactions try to update the same item, one will fail with a `TransactionCanceledException`.
- **Cost**: DynamoDB Transactions cost **2x** the standard RCU/WCU because they require two passes over the data.

## 📐 ASCII Diagrams
```text
[ CLIENT ] --(TransactWrite)--> [ TRANSACTION COORDINATOR ]
                                       |
                   +-------------------+-------------------+
                   | (Phase 1: Prepare)                    |
          [ Partition A ]                         [ Partition B ]
          (Locked?) -> YES                        (Locked?) -> YES
                   |                                       |
                   +-------------------+-------------------+
                   | (Phase 2: Commit)                     |
          [ SUCCESS: v2 ]                         [ SUCCESS: v2 ]
```

## 🔍 Code / IaC (Python SDK)
```python
import boto3

dynamodb = boto3.client('dynamodb')

try:
    response = dynamodb.transact_write_items(
        TransactItems=[
            {
                'Update': {
                    'TableName': 'Accounts',
                    'Key': {'AccountID': {'S': 'Acc1'}},
                    'UpdateExpression': 'SET Balance = Balance - :amt',
                    'ConditionExpression': 'Balance >= :amt',
                    'ExpressionAttributeValues': {':amt': {'N': '100'}}
                }
            },
            {
                'Update': {
                    'TableName': 'Accounts',
                    'Key': {'AccountID': {'S': 'Acc2'}},
                    'UpdateExpression': 'SET Balance = Balance + :amt',
                    'ExpressionAttributeValues': {':amt': {'N': '100'}}
                }
            }
        ]
    )
    print("Transfer successful")
except Exception as e:
    print(f"Transfer failed: {e}")
```

## 💥 Production Failures
1.  **The "Long Transaction" Lockup**: In RDS, a developer starts a transaction and then waits for a slow API call. This keeps locks open, blocking all other updates and eventually crashing the DB connections. **Staff Rule**: Never put network calls inside a DB transaction.
2.  **Idempotency Failure**: A transaction succeeds, but the network fails on the way back. The client retries, and if not handled, the money is transferred twice. **Solution**: Use `ClientRequestToken` for idempotency in DynamoDB.
3.  **Deadlocks**: Transaction 1 locks A then B. Transaction 2 locks B then A. They wait for each other forever until the DB kills one of them.

## 🧪 Real-time Q&A
*   **Q**: Can a DynamoDB transaction span regions?
*   **A**: No. Transactions are limited to a single region.
*   **Q**: Is S3 Strong Consistency a transaction?
*   **A**: No. It guarantees that once a write is finished, it is visible. It does not guarantee atomicity across multiple objects.

## ⚠️ Edge Cases
*   **GSI Consistency**: Global Secondary Indexes in DynamoDB are ALWAYS eventually consistent, even if the main table update was part of a transaction.
*   **Read-after-Write in Aurora**: If you write to the Primary and immediately read from a Replica, you might get old data due to "Replica Lag."

## 🏢 Best Practices
1.  **Keep Transactions Short**: Only include the bare minimum operations.
2.  **Use Idempotency Tokens**: Always provide a unique token for transactional writes to prevent double-processing.
3.  **ACID for Money**: Use RDS or DynamoDB Transactions for financial or inventory state. Use Eventual Consistency for "Likes," "Comments," or "Analytics."

## ⚖️ Trade-offs
*   **Strong Consistency**: Guaranteed correctness but higher latency and lower throughput.
*   **Eventual Consistency**: Maximum performance and availability but "stale" data for a few milliseconds.

## 💼 Interview Q&A
*   **Q**: Explain the CAP Theorem and how AWS DynamoDB fits into it.
*   **A**: CAP states you can only have 2 of 3 (Consistency, Availability, Partition Tolerance). In a distributed cloud like AWS, Partition Tolerance is a given. DynamoDB is typically an **AP** system (Available and Partition Tolerant) by default, using eventual consistency. However, by using Strongly Consistent reads or Transactions, it can behave as a **CP** system (Consistent and Partition Tolerant) at the cost of some availability during network splits.

## 🧩 Practice Problems
1.  Implement a "Retry with Jitter" logic for a DynamoDB transaction that fails due to a `TransactionConflict`.
2.  Compare the latency of a standard `PutItem` vs a `TransactWriteItem` in a test environment.

---
Prev: [04_Partitioning_and_Hot_Keys.md](../Databases/04_Partitioning_and_Hot_Keys.md) | Index: [Docker/00_Index.md](../00_Index.md) | Next: [06_Read_Replicas_and_Failover.md](../Databases/06_Read_Replicas_and_Failover.md)
---
