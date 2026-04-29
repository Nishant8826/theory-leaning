# ƛ Lambda Internals

## 📌 Topic Name
AWS Lambda: The Event-Driven MicroVM Architecture

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Run code without managing servers. You pay only for execution time.
*   **Expert**: Lambda is a **High-Density Serverless Execution Environment** powered by **Firecracker microVMs**. It abstracts the entire stack from the hardware up to the runtime. It is designed for short-lived, stateless, and event-driven workloads. Understanding Lambda requires understanding the **Worker** fleet, the **Placement Service**, and the **Synchronous vs Asynchronous** invocation models.

## 🏗️ Mental Model
Think of Lambda as a **Racing Pit Stop**.
- **Cold Start**: The car (Code) is in the garage. We have to wheel it out, fuel it, and start the engine. (Slow).
- **Warm Start**: The car is already on the track with the engine running. Just hop in and go. (Fast).
- **Concurrency**: How many cars can be on the track at the same time.

## ⚡ Actual Behavior
When an event (S3 upload, API call) triggers a Lambda:
1.  The **Frontend Worker** receives the request.
2.  The **Placement Service** checks for a "warm" execution environment.
3.  If none exists (**Cold Start**), it spins up a new **Firecracker microVM**, downloads your code/layer, and initializes the runtime.
4.  If one exists (**Warm Start**), it routes the request to the existing environment.

## 🔬 Internal Mechanics
1.  **Firecracker microVM**: A specialized VMM (Virtual Machine Monitor) written in Rust that launches in <100ms. It uses KVM but provides much faster startup than traditional EC2.
2.  **The Worker Fleet**: A massive pool of bare-metal EC2 instances that host thousands of microVMs.
3.  **The Runtime API**: How your code talks to the Lambda management plane to get the next event and send the response.
4.  **Ephemeral Storage (`/tmp`)**: Local disk space (512MB to 10GB) that persists *between* warm invocations but is wiped when the environment is destroyed.

## 🔁 Execution Flow (Synchronous)
1.  **Request**: API Gateway calls Lambda.
2.  **Auth**: IAM checks permissions.
3.  **Environment Selection**: Warm found? Yes -> Run handler. No -> Cold Start.
4.  **Handler Execution**: Code runs, returns result.
5.  **Response**: Returned to API Gateway.

## 🧠 Resource Behavior
- **Memory vs CPU**: In Lambda, you only configure Memory (128MB to 10GB). CPU is scaled linearly with memory. At 1,769MB, you get exactly 1 vCPU.
- **Concurrency Limits**: Regional limit (default 1000). If you hit this, Lambda returns `TooManyRequestsException` (429).

## 📐 ASCII Diagrams
```text
[ Trigger ] --> [ Frontend ] --> [ Placement Service ]
                                       |
                   +-------------------+-------------------+
                   |                                       |
          [ Warm Environment ]                    [ Cold Start ]
          | - Reuse MicroVM  |                    | - Launch Firecracker |
          | - Run Handler    |                    | - Download Code      |
          |                  |                    | - Init Runtime       |
          +------------------+                    +----------------------+
```

## 🔍 Code / IaC (Terraform)
```hcl
resource "aws_lambda_function" "processor" {
  function_name = "data-processor"
  role          = aws_iam_role.lambda_role.arn
  handler       = "index.handler"
  runtime       = "nodejs18.x"
  memory_size   = 1024 # MB
  timeout       = 30   # Seconds

  filename      = "lambda_function.zip"
  
  # Provisioned Concurrency to avoid cold starts
  # Note: This has a cost!
}
```

## 💥 Production Failures
1.  **The VPC Cold Start**: (Older issue, mostly fixed by AWS Hyperplane) Lambda needed to attach an ENI to join a VPC, adding 10+ seconds to cold starts. Now it uses pre-created ENIs, but still has more overhead than non-VPC Lambdas.
2.  **Recursive Invocations**: Lambda A triggers S3, which triggers Lambda A. This creates a loop that consumes all concurrency and costs thousands of dollars in minutes.
3.  **Timeout Cascades**: Lambda calls a slow downstream API. Lambda waits (and pays), eventually timing out. If the upstream (API Gateway) times out first, the client gets an error but the Lambda keeps running.

## 🧪 Real-time Q&A
*   **Q**: How do I stop cold starts?
*   **A**: Use **Provisioned Concurrency** (expensive) or optimize your code (reduce dependencies, use smaller runtimes like Go/Rust/Node instead of Java/DotNet).
*   **Q**: Can I run a background task in Lambda?
*   **A**: No. Once the handler returns, the execution environment is "frozen." Background threads will stop until the next invocation.

## ⚠️ Edge Cases
*   **Maximum Execution Time**: 15 minutes. Hard limit.
*   **Payload Size**: 6MB for synchronous, 256KB for asynchronous. Use S3 for larger data.

## 🏢 Best Practices
1.  **Statelessness**: Never assume `/tmp` will be there.
2.  **Lazy Initialization**: Initialize DB connections *outside* the handler so they are reused in warm starts.
3.  **Right-Sizing**: Use tools like "AWS Lambda Power Tuning" to find the memory setting with the best price/performance.

## ⚖️ Trade-offs
*   **Lambda vs EC2**: Zero management and infinite scale vs. potential cold starts and a 15-minute time limit.

## 💼 Interview Q&A
*   **Q**: Explain "Provisioned Concurrency."
*   **A**: It is a feature that keeps a specific number of execution environments warm and ready to respond immediately. It eliminates cold start latency but incurs a cost even if no requests are made.

## 🧩 Practice Problems
1.  Calculate the cost of 1 million invocations of a 512MB Lambda running for 100ms.
2.  Design a system that handles 10,000 concurrent requests using Lambda, considering regional quotas and account limits.
