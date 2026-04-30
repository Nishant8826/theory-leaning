# 📨 SQS and SNS Deep Dive

## 📌 Topic Name
Amazon SQS and SNS: The Asynchronous Backbone of AWS

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: SQS is a queue for messages; SNS is a notification service to send messages to many subscribers.
*   **Expert**: SQS is a **Distributed, Highly Available Message Queuing Service** that enables decoupling of microservices via asynchronous processing. It supports **Standard (At-least-once delivery, best-effort ordering)** and **FIFO (Exactly-once processing, strict ordering)**. SNS is a **Fully Managed Pub/Sub Service** that provides high-throughput, many-to-many messaging. A Staff engineer understands the nuances of **Message Deduplication**, **Visibility Timeouts**, **Dead Letter Queues (DLQ)**, and **Fan-out Patterns** to build resilient, eventual-consistent systems.

## 🏗️ Mental Model
- **SQS**: A **Post Office Box**. One person puts a letter in; one person (the worker) takes it out and processes it. If the worker fails, the letter goes back into the box.
- **SNS**: A **Radio Broadcast**. One station speaks, and anyone with a radio (Subscriber) tuned to that frequency hears the message simultaneously.

## ⚡ Actual Behavior
- **SQS Standard**: Near-infinite throughput. Messages can occasionally be delivered more than once or out of order.
- **SQS FIFO**: Limited to 3,000 messages per second (with batching). Guarantees exactly-once delivery and first-in-first-out order.
- **SNS Fan-out**: One SNS topic can push messages to multiple SQS queues, allowing multiple services to process the same event differently.

## 🔬 Internal Mechanics
1.  **Visibility Timeout**: The period during which SQS prevents other consumers from receiving and processing a message that has already been picked up. If the consumer doesn't delete the message before the timeout, it becomes "Visible" again.
2.  **Long Polling**: Reducing cost and CPU by keeping a connection open for up to 20 seconds (`WaitTimeSeconds`), waiting for a message to arrive instead of repeatedly pinging an empty queue.
3.  **SNS Filtering**: Allows subscribers to only receive a subset of messages based on message attributes (e.g., "Only send me orders with `status: 'shipped'`).

## 🔁 Execution Flow (Fan-out Pattern)
1.  **Publisher**: Sends `OrderPlaced` event to SNS Topic.
2.  **SNS**: Receives event and replicates it to all 3 subscribed SQS queues (Inventory, Billing, Email).
3.  **Inventory Worker**: Pulls from `InventoryQueue`, checks stock, deletes message.
4.  **Billing Worker**: Pulls from `BillingQueue`, charges card, deletes message.
5.  **Email Worker**: Pulls from `EmailQueue`, sends confirmation, deletes message.

## 🧠 Resource Behavior
- **Dead Letter Queues (DLQ)**: If a message fails processing $X$ times (MaxReceiveCount), it is moved to a DLQ for manual inspection.
- **Exactly-once (FIFO)**: Uses a `MessageDeduplicationId` to ignore duplicate sends within a 5-minute window.

## 📐 ASCII Diagrams
```text
[ PRODUCER ] ----> [ SNS TOPIC ]
                         |
           +-------------+-------------+
           |             |             |
     [ SQS QUEUE A ] [ SQS QUEUE B ] [ SQS QUEUE C ]
           |             |             |
     [ WORKER A ]    [ WORKER B ]    [ WORKER C ]
```

## 🔍 Code / IaC (Terraform)
```hcl
# SQS Queue with DLQ
resource "aws_sqs_queue" "main_queue" {
  name                      = "order-processing-queue"
  delay_seconds             = 0
  max_message_size          = 262144
  message_retention_seconds = 345600 # 4 days
  receive_wait_time_seconds = 20     # Long Polling

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.dlq.arn
    maxReceiveCount     = 5
  })
}

resource "aws_sqs_queue" "dlq" {
  name = "order-processing-dlq"
}

# SNS Topic
resource "aws_sns_topic" "order_updates" {
  name = "order-updates-topic"
}

# Subscription
resource "aws_sns_topic_subscription" "queue_sub" {
  topic_arn = aws_sns_topic.order_updates.arn
  protocol  = "sqs"
  endpoint  = aws_sqs_queue.main_queue.arn
}
```

## 💥 Production Failures
1.  **The "Visibility Timeout" Race**: A worker takes 40 seconds to process a message, but the Visibility Timeout is 30 seconds. The message becomes visible again, a second worker picks it up, and the job is processed twice. **Solution**: Increase timeout or use `ChangeMessageVisibility` to heartbeat.
2.  **SNS to SQS Permission Gap**: You subscribe a queue to a topic, but the SQS queue policy doesn't explicitly allow the SNS service principal to `sqs:SendMessage`. Messages are silently dropped.
3.  **Poison Pill**: A message contains data that causes the worker to crash (e.g., a divide-by-zero). It retries, crashes again, and cycles until it hits the DLQ limit.

## 🧪 Real-time Q&A
*   **Q**: What is the max message size?
*   **A**: 256KB. For larger payloads, use the **S3 Extended Client Library** to store the payload in S3 and send the reference in SQS.
*   **Q**: Does SNS guarantee delivery?
*   **A**: It provides durable storage for retries (especially for SQS/Lambda), but it is generally a "push and forget" service.

## ⚠️ Edge Cases
*   **Delayed Queues**: You can configure a queue to hide new messages for up to 15 minutes, useful for building "retry with delay" logic.
*   **Message Grouping (FIFO)**: Allows multiple "streams" of ordered messages within a single queue (e.g., all messages for `User-A` are in order, but `User-B` can be processed in parallel).

## 🏢 Best Practices
1.  **Use Long Polling** to reduce costs and latency.
2.  **Always use DLQs** to handle failed messages.
3.  **Keep messages small**: Use S3 for large payloads.
4.  **Idempotent Consumers**: Ensure that if a message is delivered twice, it doesn't break your system.

## ⚖️ Trade-offs
*   **Standard**: High scale, low cost, but complex app logic (must handle out-of-order/duplicates).
*   **FIFO**: Simple app logic, but limited throughput and slightly higher cost.

## 💼 Interview Q&A
*   **Q**: How would you handle a spike of 1 million orders per minute in an e-commerce system?
*   **A**: I would use **SQS Standard** as a buffer. The web tier drops the order message into SQS and returns a 202 to the user. A fleet of workers in an ASG then pulls from SQS at its own pace. If the queue grows too large, the ASG scales out based on the `ApproximateNumberOfMessagesVisible` metric. This protects the database from being overwhelmed by the traffic spike.

## 🧩 Practice Problems
1.  Set up an SNS Topic that fans out to an SQS Queue and an Email address simultaneously.
2.  Write a script that sends a message to SQS and then attempts to receive it twice, observing the effect of the Visibility Timeout.

---
Prev: [04_Caching_Strategies.md](../Scaling/04_Caching_Strategies.md) | Index: [Docker/00_Index.md](../00_Index.md) | Next: [06_Event_Driven_Architecture.md](../Scaling/06_Event_Driven_Architecture.md)
---
