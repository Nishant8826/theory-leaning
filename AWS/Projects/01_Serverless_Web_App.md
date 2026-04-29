# 🛠️ Project: Serverless Web App

## 📌 Topic Name
Project: Building a Globally Distributed, Serverless E-commerce API

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Use Lambda and DynamoDB to build a website that doesn't need servers.
*   **Expert**: This project implements a **Fully Managed, Event-Driven Architecture**. It leverages **CloudFront** for edge delivery, **API Gateway** for request orchestration, **Lambda** for business logic, and **DynamoDB** for single-digit millisecond data persistence. The entire stack is defined as **Infrastructure as Code (Terraform)** and includes **Observability (X-Ray)** and **Security (OIDC)** as first-class citizens.

## 🏗️ Architecture Overview
- **Frontend**: Static React/Next.js files hosted on **S3** and served via **CloudFront**.
- **Auth**: User sign-up and login handled by **Amazon Cognito**.
- **API**: **API Gateway (HTTP API)** protected by a Cognito JWT Authorizer.
- **Compute**: **AWS Lambda** functions (Node.js/Python).
- **Storage**: **DynamoDB** using a "Single Table Design" for efficiency.
- **Messaging**: **SQS** and **SNS** for asynchronous task processing (e.g., sending emails).

## 📐 Architecture Diagram
```text
[ USER ] ----(HTTPS)----> [ CLOUDFRONT ] ----> [ S3 (Static UI) ]
      |                         |
      |                 [ API GATEWAY ]
      |                         |
[ COGNITO ] <---(Auth)---+      |
      |                 [ LAMBDA (Logic) ]
      |                         |
      +----------------> [ DYNAMODB (Data) ]
                                |
                        [ SQS / SNS (Events) ]
```

## 🔍 Implementation Steps (Terraform)
1.  **Storage**: Create a DynamoDB table with `PK` and `SK`.
2.  **Compute**: Write a Lambda function that performs a `PutItem` (Create Order).
3.  **API**: Set up an HTTP API in API Gateway and connect it to the Lambda via an Integration.
4.  **Security**: Create a Cognito User Pool and attach it as an Authorizer to the API Route.
5.  **Edge**: Create a CloudFront distribution pointing to the S3 bucket and the API Gateway.

## 🔍 Code Snippet (Lambda Logic)
```javascript
const AWS = require('aws-sdk');
const db = new AWS.DynamoDB.DocumentClient();

exports.handler = async (event) => {
    const body = JSON.parse(event.body);
    const order = {
        PK: `USER#${event.requestContext.authorizer.claims.sub}`,
        SK: `ORDER#${Date.now()}`,
        Status: "PENDING",
        Total: body.total
    };

    await db.put({ TableName: 'OrdersTable', Item: order }).promise();

    return {
        statusCode: 201,
        body: JSON.stringify({ message: "Order Created", id: order.SK })
    };
};
```

## 💥 Production Considerations
1.  **Cold Starts**: Use "Provisioned Concurrency" for the `CreateOrder` Lambda to ensure fast checkout.
2.  **Concurrency Limits**: Ensure your account limit for Lambda (default 1000) is high enough for expected peak traffic.
3.  **Idempotency**: Use a `ClientToken` from the frontend to ensure a user doesn't get double-charged if they click "Buy" twice.

## 💼 Interview Walkthrough
- **Q**: How would you scale this app to 1 million users?
- **A**: The beauty of this architecture is that every component is serverless. **CloudFront** and **S3** handle static traffic globally. **API Gateway** scales automatically to 10k+ RPS. **Lambda** scales out to thousands of concurrent executions. **DynamoDB** handles any volume of data. To scale further, I would focus on **Caching** (using DAX for DynamoDB) and **Asynchronous processing** for non-critical tasks (using SQS).

## 🧩 Practice Problems
1.  Implement a "Dead Letter Queue" for the order processing Lambda.
2.  Add a Global Secondary Index (GSI) to the DynamoDB table to allow searching for orders by `Status`.
