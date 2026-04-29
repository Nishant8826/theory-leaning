# 🛡️ Fault Tolerance Patterns

## 📌 Topic Name
Distributed Systems Resilience: Retries, Circuit Breakers, and Idempotency

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: If a request fails, try again.
*   **Expert**: Fault tolerance is the **Ability of a System to Continue Operating** despite the failure of one or more components. It involves software patterns that prevent a single failure from cascading into a total system collapse. A Staff engineer implements **Retries with Exponential Backoff**, **Circuit Breakers** to stop hitting a dead service, and **Idempotency Tokens** to ensure that retried requests don't cause duplicate data.

## 🏗️ Mental Model
- **Retries**: A **Persistent Salesman**. If you don't answer the door, he knocks again later.
- **Exponential Backoff**: The salesman waits 1 minute, then 2, then 4, then 8, so he doesn't annoy you or waste his energy.
- **Circuit Breaker**: A **Household Fuse**. If too much power (Errors) flows through the wire, the fuse "pops" and stops all flow to protect the house (Service) from burning down.
- **Idempotency**: A **Light Switch**. No matter how many times you flip it "On," the light stays "On." It doesn't get "double-on."

## ⚡ Actual Behavior
- **AWS SDKs**: Automatically include retry logic for most services.
- **Step Functions**: Provides native support for retries and error handling in workflows.
- **Lambda**: Automatically retries asynchronous invocations (e.g., from S3) twice before sending to a Dead Letter Queue (DLQ).

## 🔬 Internal Mechanics
1.  **Exponential Backoff + Jitter**: `wait = (2^retry_count) + random_jitter`. Adding "Jitter" ensures that 1,000 clients who all fail at the same time don't all retry at the exact same millisecond (preventing a "Thundering Herd").
2.  **Circuit Breaker States**:
    - **Closed**: Everything is normal. Traffic flows.
    - **Open**: Error threshold reached. Traffic is blocked immediately (returns "Service Unavailable").
    - **Half-Open**: After a timeout, allow a few requests through. If they succeed, move to "Closed." If they fail, go back to "Open."
3.  **Idempotency Token**: A unique ID (e.g., `client-request-id`) sent with a request. If the server receives two requests with the same ID, it returns the same response for the second one without processing it again.

## 🔁 Execution Flow (Circuit Breaker)
1.  **Request**: App A calls App B.
2.  **Error**: App B returns `500 Internal Server Error`.
3.  **Counter**: Circuit Breaker increments error count.
4.  **Threshold**: 5th error in 10 seconds.
5.  **Trip**: Circuit Breaker moves to **OPEN**.
6.  **Protection**: For the next 30 seconds, all calls from A to B are rejected immediately by the breaker. App B has time to recover.
7.  **Reset**: After 30s, breaker allows one request. If it works, it closes.

## 🧠 Resource Behavior
- **Dead Letter Queues (DLQ)**: A secondary SQS queue where "failed" messages are sent after a certain number of retries, allowing for manual inspection.
- **TTL (Time to Live)**: Used in caches to ensure that "bad" data doesn't stay in the system forever during a fault.

## 📐 ASCII Diagrams
```text
[ CLIENT ] --(Request)--> [ CIRCUIT BREAKER ] --(Call)--> [ SERVICE B ]
                                  |
                   +--------------+--------------+
                   | (Success)    | (Failure)    |
              [ STATUS: CLOSED ]  [ STATUS: OPEN ]
                                         |
                                  [ WAIT / RETRY ]
```

## 🔍 Code / IaC (Step Functions Retry)
```hcl
resource "aws_sfn_state_machine" "my_workflow" {
  definition = jsonencode({
    StartAt = "ProcessData"
    States = {
      ProcessData = {
        Type = "Task"
        Resource = aws_lambda_function.processor.arn
        Retry = [
          {
            ErrorEquals = ["Lambda.TooManyRequestsException", "InternalServerError"]
            IntervalSeconds = 2
            MaxAttempts = 3
            BackoffRate = 2.0 # Exponential backoff
          }
        ]
        End = true
      }
    }
  })
}
```

## 💥 Production Failures
1.  **The "Retry Storm"**: A database is slow. 1,000 app servers detect the slowness and all start retrying their queries. The increased load makes the database even slower, causing more retries, and finally, a total crash. **Solution**: Use **Jitter** and **Circuit Breakers**.
2.  **Double Charging**: A user clicks "Buy" on an e-commerce site. The network fails. The user clicks "Buy" again. Without an **Idempotency Token**, the user is charged twice.
3.  **Infinite Loop**: Service A calls B, B calls C, and C calls A. One error in the chain propagates and amplifies, bringing down all three services.

## 🧪 Real-time Q&A
*   **Q**: When should I NOT retry?
*   **A**: Don't retry `4xx` errors (Client errors like "Unauthorized" or "Bad Request"). Retries won't fix those. Only retry `5xx` (Server errors) or network timeouts.
*   **Q**: What is "Fail-Fast"?
*   **A**: It’s the philosophy that if a system is broken, it should stop immediately and report the error, rather than trying to continue in a "limping" or corrupted state.

## ⚠️ Edge Cases
*   **Non-Idempotent Operations**: Like `POST /messages` (which adds a new message). These MUST have a unique ID to be safe for retries. `PUT /user/123` is naturally idempotent because updating the same data twice doesn't change the outcome.
*   **Clock Skew**: In distributed systems, if the clocks on different servers are out of sync, "Time-based" circuit breakers or TTLs can behave unpredictably.

## 🏢 Best Practices
1.  **Use Exponential Backoff + Jitter** for all retries.
2.  **Implement Circuit Breakers** for all downstream dependencies.
3.  **Make API calls Idempotent** whenever possible.
4.  **Use a Service Mesh** (like App Mesh or Istio) to handle these patterns at the infrastructure layer instead of in code.

## ⚖️ Trade-offs
*   **Retries**: Improve success rates but increase latency and load on the system.
*   **Circuit Breakers**: Protect system stability but result in "Fail-Fast" errors for users.

## 💼 Interview Q&A
*   **Q**: How would you handle a transient network error between a Lambda and a DynamoDB table?
*   **A**: 1. I would rely on the **AWS SDK**, which has built-in retries and exponential backoff for DynamoDB. 2. If the error persists, I would implement a **Circuit Breaker** in the Lambda code (or via a library) to stop hitting the table and return a cached or default response. 3. I would ensure the write operation is **Idempotent** so that if the network failed *after* the write but *before* the ACK, the retry wouldn't create a duplicate item.

## 🧩 Practice Problems
1.  Write a Python decorator that implements "Retry with Exponential Backoff" for a function call.
2.  Configure a "Dead Letter Queue" for an SQS queue and simulate a failure to see the message move to the DLQ.
