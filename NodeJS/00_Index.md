# 🚀 The Ultimate Node.js Knowledge System

Welcome to the definitive guide to mastering Node.js, from internal architecture to large-scale distributed systems. This system is designed for practitioners who want to go beyond tutorials and understand the "why" and "how" of high-performance backend engineering.

---

## 📂 Curriculum Overview

### 🟢 Phase 1: Basics (Foundation)
*   [01. What is Node.js Runtime?](./Basics/01_What_is_NodeJS_Runtime.md) - V8 + libuv + C++ Bindings.
*   [02. JavaScript Execution Model](./Basics/02_JavaScript_Execution_Model.md) - Single-threaded nature and the Call Stack.
*   [03. Event Loop Basics](./Basics/03_Event_Loop_Basics.md) - Introduction to non-blocking I/O.
*   [04. Modules: CommonJS vs ESM](./Basics/04_Modules_CommonJS_ESM.md) - Resolution algorithms and caching.
*   [05. Basic HTTP Server](./Basics/05_Basic_HTTP_Server.md) - Low-level `http` module internals.

### 🟡 Phase 2: Intermediate (Practical Mastery)
*   [01. Event Loop Deep Dive](./Intermediate/01_Event_Loop_Deep_Dive.md) - Microtasks vs Macrotasks.
*   [02. Async Patterns](./Intermediate/02_Async_Patterns_Promises_AsyncAwait.md) - Promises, Async/Await internals.
*   [03. Express Internals](./Intermediate/03_Express_Internals.md) - Routing and the Request/Response cycle.
*   [04. Middleware Architecture](./Intermediate/04_Middleware_Architecture.md) - The Onion model and composability.
*   [05. Error Handling Strategies](./Intermediate/05_Error_Handling_Strategies.md) - Operational vs Programmer errors.
*   [06. Configuration Management](./Intermediate/06_Configuration_Management.md) - Twelve-Factor App principles.

### 🟠 Phase 3: Advanced (System-Level)
*   [01. Streams and Backpressure](./Advanced/01_Streams_and_Backpressure.md) - Efficient data processing.
*   [02. Buffer and Binary Data](./Advanced/02_Buffer_and_Binary_Data.md) - Memory outside the V8 heap.
*   [03. Clustering and Child Processes](./Advanced/03_Clustering_and_Child_Processes.md) - Vertical scaling.
*   [04. Worker Threads](./Advanced/04_Worker_Threads.md) - Parallelism for CPU-bound tasks.
*   [05. TCP/HTTP/TLS Internals](./Advanced/05_TCP_HTTP_TLS_Internals.md) - Networking from the ground up.
*   [06. WebSockets & Socket.IO](./Advanced/06_WebSockets_SocketIO.md) - Real-time bidirectional communication.
*   [07. Database Integration](./Advanced/07_Database_Integration.md) - Connection pooling and query optimization.

### 🔴 Phase 4: Expert (Internals & Performance)
*   [01. V8 Engine Internals](./Expert/01_V8_Engine_Internals.md) - JIT compilation, Hidden Classes, Inline Caching.
*   [02. Libuv and Threadpool](./Expert/02_Libuv_and_Threadpool.md) - The heart of asynchronous I/O.
*   [03. Garbage Collection](./Expert/03_Garbage_Collection.md) - Orinoco, Scavenge, and Mark-Sweep-Compact.
*   [04. Event Loop Phases](./Expert/04_Event_Loop_Phases.md) - Timers, I/O, Poll, Check, Close.
*   [05. Memory Leaks Debugging](./Expert/05_Memory_Leaks_Debugging.md) - Heap snapshots and allocation profiling.
*   [06. Performance Profiling](./Expert/06_Performance_Profiling.md) - Flame graphs and Clinic.js.
*   [07. Low-Level Debugging](./Expert/07_Low_Level_Debugging.md) - `strace`, `gdb`, and core dumps.

### 🏗️ Phase 5: Architecture
*   [01. REST API Design](./Architecture/01_REST_API_Design.md) - Maturity levels and constraints.
*   [02. GraphQL Architecture](./Architecture/02_GraphQL_Architecture.md) - Schema design and the N+1 problem.
*   [03. Microservices with Node.js](./Architecture/03_Microservices_NodeJS.md) - Domain-Driven Design (DDD).
*   [04. Service Communication](./Architecture/04_Service_Communication.md) - gRPC, Message Queues vs HTTP.
*   [05. Message Queues](./Architecture/05_Message_Queues.md) - RabbitMQ and Kafka integration.
*   [06. API Gateway](./Architecture/06_API_Gateway.md) - Rate limiting, Auth, and Routing.

### 🛡️ Phase 6: Security
*   [01. Authentication (JWT/OAuth)](./Security/01_Authentication_JWT_OAuth.md) - Secure identity management.
*   [02. Authorization](./Security/02_Authorization.md) - RBAC vs ABAC models.
*   [03. Common Vulnerabilities](./Security/03_Common_Vulnerabilities.md) - OWASP Top 10 for Node.js.
*   [04. Input Validation](./Security/04_Input_Validation.md) - XSS and SQL Injection prevention.
*   [05. Encryption and TLS](./Security/05_Encryption_and_TLS.md) - Crypto module and secure transport.
*   [06. Rate Limiting](./Security/06_Rate_Limiting.md) - Protecting against DoS/DDoS.

### ⚡ Phase 7: Performance
*   [01. Event Loop Latency](./Performance/01_Event_Loop_Latency.md) - Measuring and reducing lag.
*   [02. CPU and Memory Optimization](./Performance/02_CPU_and_Memory_Optimization.md) - Identifying bottlenecks.
*   [03. Caching Strategies](./Performance/03_Caching_Strategies.md) - Redis, CDN, and in-memory.
*   [04. Load Testing](./Performance/04_Load_Testing.md) - Autocannon and k6.
*   [05. Scaling Node.js](./Performance/05_Scaling_NodeJS.md) - Horizontal vs Vertical scaling.

### 👁️ Phase 8: Observability
*   [01. Logging Strategies](./Observability/01_Logging_Strategies.md) - Structured logging with Pino.
*   [02. Metrics and Monitoring](./Observability/02_Metrics_and_Monitoring.md) - Prometheus and Grafana.
*   [03. Distributed Tracing](./Observability/03_Distributed_Tracing.md) - OpenTelemetry and Jaeger.
*   [04. Debugging Production](./Observability/04_Debugging_Production.md) - Post-mortem analysis.

### 🚀 Phase 9: CI/CD
*   [01. Node.js in Jenkins](./CI_CD/01_NodeJS_in_Jenkins.md) - Groovy pipelines for Node.
*   [02. Build Pipelines](./CI_CD/02_Build_Pipelines.md) - Automated testing and artifact creation.
*   [03. Test Automation](./CI_CD/03_Test_Automation.md) - Jest, Supertest, and Cypress.
*   [04. Deployment Strategies](./CI_CD/04_Deployment_Strategies.md) - Blue-Green vs Canary.

### ☁️ Phase 10: Cloud (AWS)
*   [01. Deploy to AWS EC2](./Cloud/01_Deploy_to_AWS_EC2.md) - Manual vs PM2.
*   [02. Serverless Lambda](./Cloud/02_Serverless_Lambda.md) - Cold starts and event-driven architecture.
*   [03. Containerized Node.js](./Cloud/03_Containerized_NodeJS.md) - Docker and ECR.
*   [04. Load Balancing (ALB)](./Cloud/04_Load_Balancing_ALB.md) - Distributing traffic.
*   [05. Scaling on AWS](./Cloud/05_Scaling_on_AWS.md) - ASG and ECS/EKS.

### 🛠️ Phase 11: Projects
*   [01. Production-Ready REST API](./Projects/01_REST_API_Project.md)
*   [02. Real-Time Chat System](./Projects/02_RealTime_Chat_App.md)
*   [03. Distributed Microservices](./Projects/03_Microservices_System.md)
*   [04. Fullstack App (Node + React)](./Projects/04_Fullstack_App_Node_React.md)
*   [05. Enterprise CI/CD Pipeline](./Projects/05_CI_CD_Pipeline.md)

---
*Created with ❤️ by the Principal Engineering Team.*
