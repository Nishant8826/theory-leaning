# API Gateway

## What Is This Service?
Amazon API Gateway is a fully managed service that makes it easy to create, publish, maintain, monitor, and secure APIs at any scale. It acts as the "front door" for your backend services.

## Why This Service Exists
AWS Lambda functions don't have public URLs by default. If you want a React frontend to trigger a Lambda function via an HTTP `GET` or `POST` request, you need a highly scalable HTTP server to receive the request, validate it, and pass it to Lambda. API Gateway does this, completely removing the need to manage your own Express.js server for routing.

## Real World Analogy
API Gateway is the **Receptionist at a busy corporate office**.
Customers (React apps) walk in and ask to see an employee (a Lambda function or EC2 server). The receptionist checks their ID (Authentication), checks the company directory to see where the employee sits (Routing), limits how many people can go back at once (Rate Limiting), and escorts the customer back.

## How It Works
1. You create an API (REST, HTTP, or WebSocket).
2. You define Routes/Resources (e.g., `/users`, `/products`).
3. You define Methods (GET, POST).
4. You configure Integrations (e.g., wire the `GET /users` route to a specific Lambda function).
5. You deploy the API to a Stage (e.g., `dev`, `prod`), which gives you a public URL.

## Core Concepts
- **REST API vs HTTP API**: HTTP APIs are the newer, faster, and 71% cheaper version of API Gateway designed specifically for Lambda proxying. REST APIs are the older, feature-rich version with complex request validation and mapping templates.
- **Throttling**: Preventing abuse by limiting users to X requests per second.
- **Usage Plans & API Keys**: Issuing specific keys to specific clients to track usage and monetize your API.

## MERN Stack Integration
A "Serverless MERN" stack is often called a **MERNless** or **Serverless** stack. 
Instead of hosting a single Express.js monolith on ECS, you break your Express routes apart:
- React makes an API call to API Gateway.
- API Gateway routes `/auth` to an Auth Lambda, and `/products` to a Products Lambda.
- The Lambdas query MongoDB and return the data. 

## Production Impact
- **Maintenance**: You no longer have to manage NGINX, PM2, or Load Balancers. API Gateway handles hundreds of thousands of concurrent requests effortlessly.
- **Security Validation**: You can configure API Gateway to validate JSON payload schemas *before* it invokes your Lambda function, saving compute costs on malformed requests.

## Real Production Use Cases
- A SaaS company wants to offer a public API to its developers. They use API Gateway to issue unique API Keys to each developer, apply a strict rate limit of 10 requests per second, and attach a Lambda Custom Authorizer to validate JWT tokens.

## Production Best Practices
- **Use HTTP APIs over REST APIs**: Unless you specifically need WebSocket support, WAF integration, or complex request transformation, always choose HTTP APIs. They are vastly cheaper and have lower latency.
- **CORS Configuration**: If your React app is on `domain.com` and API Gateway is on `api-xyz.com`, you MUST configure Cross-Origin Resource Sharing (CORS) directly in API Gateway to allow browser requests.

## Security Best Practices
- **Custom Authorizers**: Don't validate JWTs inside every single Lambda function. Create a dedicated "Authorizer Lambda" and attach it to API Gateway. API Gateway will run the Authorizer first, and only invoke your backend Lambda if the token is valid.
- **WAF**: Attach AWS Web Application Firewall to REST APIs to block SQL injections and malicious IPs at the edge.

## Cost Optimization Tips
- API Gateway REST APIs are notoriously expensive at high scale ($3.50 per million requests). If you are processing billions of requests, moving to Application Load Balancers directly proxying to EC2/ECS is often much cheaper.

## Common Mistakes
- Forgetting to **Deploy** the API. After making changes to routes or integrations in the console, you must explicitly click "Deploy API" to a Stage, otherwise the public URL will still serve the old configuration.

## Debugging & Troubleshooting
- **502 Bad Gateway**: Usually means the Lambda function crashed, or it returned a response payload that API Gateway couldn't understand (e.g., forgetting to return `{ statusCode: 200, body: "..." }`).
- Enable API Gateway Execution Logs in CloudWatch to see the exact raw HTTP requests and routing decisions being made.

---
Prev : [./01_Lambda_Deep_Dive.md](./01_Lambda_Deep_Dive.md) | Index : [../00_Index.md](../00_Index.md) | Next : [./03_CloudWatch.md](./03_CloudWatch.md)
---
