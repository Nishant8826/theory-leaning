# 🌐 API Gateway Internals

## 📌 Topic Name
Amazon API Gateway: The Front Door to Microservices

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Create a URL that triggers a Lambda function or connects to an existing API.
*   **Expert**: API Gateway is a **Fully Managed Proxy and Orchestration Layer**. It handles the "undifferentiated heavy lifting" of API management: Authentication/Authorization, Request Validation, Throttling, Caching, and Transformation. It supports multiple protocols including **REST (Standard)**, **HTTP (Fast/Low-cost)**, and **WebSockets (Real-time)**.

## 🏗️ Mental Model
Think of API Gateway as a **Nightclub Bouncer**.
- **The ID Check**: Authentication (API Keys, Lambda Authorizers, Cognito).
- **The VIP List**: Authorization (IAM Policies).
- **The Capacity Limit**: Throttling (How many people enter per second).
- **The Translator**: Transformation (Mapping VTL templates from JSON to XML).

## ⚡ Actual Behavior
- **Regional vs. Edge-Optimized**: 
    - **Edge-Optimized**: Uses CloudFront internally to reduce latency for global users.
    - **Regional**: For users in the same region or for use with your own CloudFront distribution.
- **Throttling**: Default limit is 10,000 requests per second (RPS) per account. You can set per-method and per-client (Usage Plan) limits.

## 🔬 Internal Mechanics
1.  **Integrations**: 
    - **Lambda Proxy**: Passes the raw request to Lambda. (Most common).
    - **HTTP Proxy**: Forwards the request to an ALB or on-premise server.
    - **AWS Service Proxy**: Talk directly to Kinesis/S3/DynamoDB without any Lambda code!
2.  **VTL (Velocity Template Language)**: A mapping engine that allows you to transform the body of a request or response.
3.  **Stages**: Allows you to have `/dev`, `/staging`, and `/prod` deployments of the same API.

## 🔁 Execution Flow (Request Lifecycle)
1.  **Request**: Client sends `POST /users`.
2.  **Auth**: API Gateway runs the Lambda Authorizer or checks the API Key.
3.  **Validation**: Checks if the JSON body matches the required schema.
4.  **Integration Request**: Maps the data to the format the backend (e.g., Lambda) expects.
5.  **Execution**: Backend processes the request.
6.  **Integration Response**: Maps the backend result back to the API response format.
7.  **Response**: Returns `201 Created` to the client.

## 🧠 Resource Behavior
- **Caching**: You can enable caching at the stage level to reduce load on your backend and improve response time.
- **WebSockets**: API Gateway maintains the persistent connection for you and only triggers your Lambda when a message is sent.

## 📐 ASCII Diagrams
```text
[ CLIENT ] --(HTTPS)--> [ API GATEWAY ]
                            |
           +----------------+----------------+
           | (Auth / Throttle / Validate)    |
           |                                 |
 [ LAMBDA PROXY ]        [ HTTP PROXY ]    [ AWS SERVICE ]
 (Node/Python)           (ALB / EC2)       (S3 / DynamoDB)
```

## 🔍 Code / IaC (Terraform)
```hcl
resource "aws_apigatewayv2_api" "http_api" {
  name          = "my-http-api"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "lambda_integration" {
  api_id           = aws_apigatewayv2_api.http_api.id
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.my_lambda.invoke_arn
}

resource "aws_apigatewayv2_route" "default_route" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "ANY /"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}
```

## 💥 Production Failures
1.  **The "Lambda Cold Start" Timeout**: Integration timeout is 29 seconds. If your Lambda takes 30 seconds to start (Cold start + DB init), API Gateway returns a 504 Gateway Timeout.
2.  **API Key Leak**: An API key is leaked, and someone consumes your entire account-level quota, causing an outage for all your other APIs. **Solution**: Use Usage Plans with strict limits.
3.  **Invalid VTL Mapping**: A change in the backend response format causes the VTL mapping to fail, resulting in a 500 Internal Server Error even though the backend was successful.

## 🧪 Real-time Q&A
*   **Q**: What is the difference between REST and HTTP APIs?
*   **A**: HTTP APIs are newer, 70% cheaper, and have lower latency, but they lack some advanced features like VTL mapping, request validation, and API keys.
*   **Q**: How do I secure my API?
*   **A**: 1. Mutual TLS (mTLS). 2. Lambda Authorizers. 3. Cognito User Pools. 4. IAM Permissions.

## ⚠️ Edge Cases
*   **Binary Support**: API Gateway can handle binary data (images/PDFs), but you must configure the "Binary Media Types."
*   **Private APIs**: Using VPC Endpoints to make an API only accessible from within your VPC.

## 🏢 Best Practices
1.  **Use HTTP APIs** for simple Lambda-backed microservices to save money.
2.  **Request Validation**: Validate input at the gateway so you don't waste Lambda execution time on bad requests.
3.  **CloudWatch Logs**: Enable "Full Request/Response Logging" during development, but disable it in prod for high-traffic APIs to save on logging costs.

## ⚖️ Trade-offs
*   **API Gateway**: Managed, scalable, feature-rich, but costs $3.50 per million requests.
*   **ALB as API**: Cheaper for high-volume simple APIs but lacks API management features (keys, usage plans, throttling).

## 💼 Interview Q&A
*   **Q**: How do you handle a request that takes longer than 29 seconds in API Gateway?
*   **A**: I would use an **Asynchronous Pattern**. API Gateway accepts the request, drops it into an SQS queue, and immediately returns a `202 Accepted`. A background worker processes the task, and the client either polls for the result or receives a webhook.

## 🧩 Practice Problems
1.  Build an API Gateway that talks directly to DynamoDB (no Lambda) to `GetItem` from a table.
2.  Implement a Lambda Authorizer that checks a JWT token and allows access based on a specific claim.

---
Prev: [03_CDN_CloudFront.md](../Networking/03_CDN_CloudFront.md) | Index: [Docker/00_Index.md](../00_Index.md) | Next: [05_VPC_Peering_and_PrivateLink.md](../Networking/05_VPC_Peering_and_PrivateLink.md)
---
