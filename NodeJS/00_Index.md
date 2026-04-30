# 🚀 Node.js Systems Engineering & Runtime Internals

## 🛰️ Course Roadmap: From Intermediate to Staff Engineer

This curriculum is designed for senior engineers with 10+ years of experience who want to master the **Node.js Runtime**, **V8 Engine**, and **Low-Level Systems Engineering**. We bypass beginner analogies and "hello world" examples, focusing instead on memory layouts, kernel syscalls, event loop phases, and production-grade debugging.

---

## 🗺️ Learning Path

### 🏗️ Section 1: Core Architecture
Understanding the bridge between JavaScript and C++.
- [01_Node_Architecture.md](./Core/01_Node_Architecture.md) - The V8 / libuv / Node.js relationship.
- [02_Event_Loop_Deep_Dive.md](./Core/02_Event_Loop_Deep_Dive.md) - Beyond the "circle" diagram; phases and starvation.
- [03_Non_Blocking_IO.md](./Core/03_Non_Blocking_IO.md) - Epoll, Kqueue, and IOCP internals.
- [04_Callbacks_Promises_Async.md](./Core/04_Callbacks_Promises_Async.md) - Microtask queue mechanics and execution order.
- [05_Error_Handling.md](./Core/05_Error_Handling.md) - Boundary crossing, crash safety, and uncaught exceptions.
- [06_Environment_and_Config.md](./Core/06_Environment_and_Config.md) - Secure and scalable configuration management.
- [07_Event_Emitter_Deep_Dive.md](./Core/07_Event_Emitter_Deep_Dive.md) - Observer pattern at scale and memory leak prevention.
- [08_Timers_Internals.md](./Core/08_Timers_Internals.md) - Timer drift, binary heaps, and precision limitations.
- [09_Async_Hooks_and_Context.md](./Core/09_Async_Hooks_and_Context.md) - Managing async state across the lifecycle.

### ⚙️ Section 2: Runtime & V8 Execution
The engine room of execution and resource management.
- [01_V8_Integration.md](./Runtime/01_V8_Integration.md) - Ignition, TurboFan, and the JIT optimization pipeline.
- [02_Memory_Management.md](./Runtime/02_Memory_Management.md) - Heap, Stack, and Off-heap memory layout.
- [03_Garbage_Collection.md](./Runtime/03_Garbage_Collection.md) - Scavenge vs Mark-Compact vs Parallel GC mechanics.
- [04_Worker_Threads.md](./Runtime/04_Worker_Threads.md) - SharedArrayBuffer, Atomics, and multi-core Node.
- [05_Cluster_Module.md](./Runtime/05_Cluster_Module.md) - Round-robin vs OS-level load balancing.
- [06_Process_Model.md](./Runtime/06_Process_Model.md) - Forking, IPC, and master-worker lifecycle.
- [07_Native_Addons_NAPI.md](./Runtime/07_Native_Addons_NAPI.md) - Bridging JS with C/C++ via N-API.
- [08_Diagnostics_Channel.md](./Runtime/08_Diagnostics_Channel.md) - Unified observability and tracing channel.
- [09_Process_Signals_and_Lifecycle.md](./Runtime/09_Process_Signals_and_Lifecycle.md) - Handling SIGTERM, SIGKILL, and graceful exits.

### 🔬 Section 3: Low-Level Internals
Deep dive into the underlying systems that power Node.js.
- [01_V8_Ignition_TurboFan.md](./Internals/01_V8_Ignition_TurboFan.md) - Bytecode generation and machine code optimization.
- [02_libuv_Thread_Pool_Customization.md](./Internals/02_libuv_Thread_Pool_Customization.md) - UV_THREADPOOL_SIZE and I/O bottlenecks.
- [03_Memory_Layout_Smi_Doubles_Elements.md](./Internals/03_Memory_Layout_Smi_Doubles_Elements.md) - How V8 stores integers, doubles, and objects.
- [04_Garbage_Collection_Orinoco_Deep_Dive.md](./Internals/04_Garbage_Collection_Orinoco_Deep_Dive.md) - Advanced GC strategies like Orinoco.
- [05_The_C_Boundary_NAPI_Internals.md](./Internals/05_The_C_Boundary_NAPI_Internals.md) - Marshalling data between JS and C++.

### 🌐 Section 4: Networking & Protocols
Building high-throughput, secure communication stacks.
- [01_HTTP_Server_Internals.md](./Networking/01_HTTP_Server_Internals.md) - Node's http_parser and llhttp mechanics.
- [02_Express_Internals.md](./Networking/02_Express_Internals.md) - The middleware stack and routing engine internals.
- [03_Middleware_Deep_Dive.md](./Networking/03_Middleware_Deep_Dive.md) - Performance impact of sequential middleware.
- [04_WebSockets_SocketIO.md](./Networking/04_WebSockets_SocketIO.md) - Persistent connections and real-time scaling.
- [05_TCP_UDP_Basics.md](./Networking/05_TCP_UDP_Basics.md) - Raw socket programming and transmission trade-offs.
- [06_TLS_SSL_Deep_Dive.md](./Networking/06_TLS_SSL_Deep_Dive.md) - OpenSSL integration and handshake overhead.
- [07_HTTP2_and_HTTP3.md](./Networking/07_HTTP2_and_HTTP3.md) - Multiplexing, Server Push, and QUIC.
- [08_DNS_and_Connection_Lifecycle.md](./Networking/08_DNS_and_Connection_Lifecycle.md) - DNS resolution and TCP handshake costs.
- [09_Connection_Pooling.md](./Networking/09_Connection_Pooling.md) - Reusing connections to reduce latency.

### 🗄️ Section 5: Data Persistence & Caching
Optimizing the data layer for high-performance applications.
- [01_Database_Connections.md](./Data/01_Database_Connections.md) - Connection pool management and saturation.
- [02_ORM_vs_Query_Builder.md](./Data/02_ORM_vs_Query_Builder.md) - Performance trade-offs in data abstraction.
- [03_Caching_Strategies_Redis.md](./Data/03_Caching_Strategies_Redis.md) - Distributed caching and eviction policies.
- [04_Consistency_vs_Availability.md](./Data/04_Consistency_vs_Availability.md) - CAP theorem in modern data stacks.
- [05_Migrations_and_Evolution.md](./Data/05_Migrations_and_Evolution.md) - Schema evolution without downtime.

### 🏛️ Section 6: Distributed Systems Architecture
Designing resilient and scalable system structures.
- [01_Monolith_vs_Microservices.md](./Architecture/01_Monolith_vs_Microservices.md) - Distributed complexity vs local coupling.
- [02_API_Gateway_Pattern.md](./Architecture/02_API_Gateway_Pattern.md) - Routing, authentication, and rate limiting at the edge.
- [03_Event_Driven_Architecture.md](./Architecture/03_Event_Driven_Architecture.md) - Pub/Sub and event-sourced systems.
- [04_Message_Queues.md](./Architecture/04_Message_Queues.md) - Decoupling services with RabbitMQ or Kafka.
- [05_Backend_For_Frontend.md](./Architecture/05_Backend_For_Frontend.md) - Optimizing APIs for specific client needs.
- [06_Stateful_vs_Stateless.md](./Architecture/06_Stateful_vs_Stateless.md) - Managing state in distributed environments.
- [07_Backpressure_in_Distributed_Systems.md](./Architecture/07_Backpressure_in_Distributed_Systems.md) - Preventing system overload via flow control.

### 📉 Section 7: Performance & Observability
Hardening systems through profiling and monitoring.
- [01_Profiling_and_Analysis.md](./Performance/01_Profiling_and_Analysis.md) - Flamegraphs and CPU profiling.
- [02_Memory_Leaks_Detection.md](./Performance/02_Memory_Leaks_Detection.md) - Finding and fixing heap leaks.
- [03_Event_Loop_Lag_Monitoring.md](./Performance/03_Event_Loop_Lag_Monitoring.md) - Identifying blocking code in production.
- [04_I_O_Optimization_Techniques.md](./Performance/04_I_O_Optimization_Techniques.md) - Minimizing syscalls and disk I/O.
- [05_Benchmarking_NodeJS.md](./Performance/05_Benchmarking_NodeJS.md) - Statistical significance in performance tests.

### 📈 Section 8: Scaling & Infrastructure
Managing growth and traffic spikes.
- [01_Vertical_vs_Horizontal.md](./Scaling/01_Vertical_vs_Horizontal.md) - Scaling up vs scaling out.
- [02_Load_Balancing_Strategies.md](./Scaling/02_Load_Balancing_Strategies.md) - L4 vs L7 load balancing.
- [03_Caching_at_the_Edge_CDN.md](./Scaling/03_Caching_at_the_Edge_CDN.md) - Reducing latency through edge delivery.
- [04_Database_Sharding_and_Partitioning.md](./Scaling/04_Database_Sharding_and_Partitioning.md) - Horizontal data scaling.
- [05_Auto_Scaling_Groups.md](./Scaling/05_Auto_Scaling_Groups.md) - Dynamic infrastructure management.

### 🛡️ Section 9: Production Security
Implementing defense-in-depth for Node.js apps.
- [01_OWASP_Top_10_in_NodeJS.md](./Security/01_OWASP_Top_10_in_NodeJS.md) - Mitigating common web vulnerabilities.
- [02_Authentication_JWT_OAuth.md](./Security/02_Authentication_JWT_OAuth.md) - Secure identity management.
- [03_Input_Validation_Sanitization.md](./Security/03_Input_Validation_Sanitization.md) - Preventing XSS and SQL injection.
- [04_Cryptography_and_Hashing.md](./Security/04_Cryptography_and_Hashing.md) - Protecting sensitive data at rest and in transit.
- [05_Security_Headers_Helmet.md](./Security/05_Security_Headers_Helmet.md) - Hardening HTTP responses.

### 🧪 Section 10: Testing & Quality Assurance
Ensuring reliability at scale.
- [01_Unit_Testing_Patterns.md](./Testing/01_Unit_Testing_Patterns.md) - Isolating logic with mocks and stubs.
- [02_Integration_Testing_Strategies.md](./Testing/02_Integration_Testing_Strategies.md) - Testing boundaries and external deps.
- [03_Load_and_Stress_Testing.md](./Testing/03_Load_and_Stress_Testing.md) - Breaking the system to find its limits.
- [04_Contract_Testing.md](./Testing/04_Contract_Testing.md) - Ensuring API compatibility between services.
- [05_TDD_and_BDD.md](./Testing/05_TDD_and_BDD.md) - Behavior-driven development workflows.

### 💼 Section 11: Real-World Case Studies
Lessons from the trenches of large-scale production.
- [01_Debugging_Memory_Leaks.md](./Case_Studies/01_Debugging_Memory_Leaks.md) - A step-by-step resolution of a production leak.
- [02_Optimizing_API_Latency.md](./Case_Studies/02_Optimizing_API_Latency.md) - Reducing p99 latency by 80%.
- [03_Handling_a_Traffic_Spike.md](./Case_Studies/03_Handling_a_Traffic_Spike.md) - Survival during a 100x traffic surge.
- [04_Microservices_Failure_Chain.md](./Case_Studies/04_Microservices_Failure_Chain.md) - Resolving cascading failures in a mesh.
- [05_Zero_Downtime_Migration.md](./Case_Studies/05_Zero_Downtime_Migration.md) - Migrating core databases with zero impact.

---

## 🎯 Suggested Progression
1. **Internals First**: Start with `Internals/` to build a mental model of libuv and syscalls.
2. **Runtime Mastery**: Move to `Runtime/` to understand how V8 consumes your code.
3. **Systems Design**: Apply that knowledge to `Architecture/` and `Scaling/`.
4. **Hardening**: Dive into `Security/` and `Performance/` for production readiness.

---

## 🛠️ Prerequisites
- Deep familiarity with ES2022+ syntax.
- Basic understanding of C++ (for native addon context).
- Familiarity with Linux/Unix terminal and system signals.

**Next:** [01_Node_Architecture.md](./Core/01_Node_Architecture.md)
