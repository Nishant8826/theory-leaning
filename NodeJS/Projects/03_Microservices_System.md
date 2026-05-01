# 📌 Project: Distributed Microservices System

## What
### 🧠 Concept Explanation
A microservices system is like **A Professional Orchestra**.
**Analogy:** 
- **The Conductor (The API Gateway):** Tells each musician when to start and stop.
- **The Musicians (The Services):** One plays the violin (Order Service), one plays the drums (Payment Service). They don't need to know how to play each other's instruments, but they must play the same song (The Business Logic).
- **The Sheet Music (gRPC/Proto):** The common language that ensures they stay in sync.
- **The Stage (Kubernetes):** The environment that provides the chairs and microphones.

---

### 🏗️ Mental Model
- **Services:** Auth, Order, Payment, Inventory.
- **Communication:** gRPC for internal sync calls; RabbitMQ for async events.
- **Observability:** Prometheus (Metrics) + Jaeger (Tracing).
- **Deployment:** Docker + Kubernetes.

---

## Why
### 🏢 Best Practices
1.  **One DB per Service:** Never share a database.
2.  **Use a Service Mesh:** Like Istio or Linkerd to handle retries, timeouts, and tracing automatically.
3.  **Contract Testing:** Use Pact to ensure that changes in one service don't break others.
4.  **Graceful Degredation:** If the "Recommendation Service" is down, the app should still work, just without recommendations.

---

### ⚖️ Trade-offs
*   **Microservices:** Incredible scale and team autonomy, but massive architectural complexity and network overhead.
*   **Monolith:** Simple and fast, but becomes a "ball of mud" that is impossible to change.

---

## How
### ⚡ Actual Behavior
*   **Decoupled State:** Each service has its own database (Postgres for Orders, Mongo for Inventory).
*   **Event-Driven:** When an order is created, an event is emitted. The Payment service sees it and reacts.
*   **API Gateway:** Routes external traffic and handles Auth.

---

### 🔬 Internal Mechanics (V8 + libuv + OS)
*   **Networking Latency:** Every "hop" between services adds ~5-10ms. We minimize this by using gRPC (HTTP/2).
*   **Isolation:** If the Payment service uses 100% CPU, it doesn't slow down the Order service (Resource isolation).

---

### 🔁 Execution Flow
1.  **Request:** User hits the Gateway to "Place Order."
2.  **Auth:** Gateway calls Auth service via gRPC to verify token.
3.  **Order:** Gateway forwards request to Order service.
4.  **Sync Check:** Order service calls Inventory service via gRPC to reserve stock.
5.  **Event:** Order service saves "Pending" order and publishes `order.created` to RabbitMQ.
6.  **Async Logic:** Payment service consumes the event and processes the credit card.
7.  **Completion:** Payment service publishes `payment.success`. Order service updates status to "Completed."

---

### 🔍 Code Example (Latest Node.js - gRPC Client Implementation)
```javascript
import * as grpc from '@grpc/grpc-js';
import * as protoLoader from '@grpc/proto-loader';

// Load the shared contract
const packageDefinition = protoLoader.loadSync('inventory.proto');
const inventoryProto = grpc.loadPackageDefinition(packageDefinition).inventory;

// Create a client for the Inventory Service
const client = new inventoryProto.InventoryService(
    'inventory-service:50051', 
    grpc.credentials.createInsecure()
);

export const checkStock = (productId) => {
    return new Promise((resolve, reject) => {
        client.GetStock({ productId }, (err, response) => {
            if (err) reject(err);
            else resolve(response.inStock);
        });
    });
};
```

---

## Impact
### 💥 Production Failures
*   **The "Distributed Monolith":** Making every service depend on every other service via sync gRPC calls. If one service dies, they all die. (Solution: Use async events for non-critical paths).
*   **Data Inconsistency:** An order is created but the payment fails, and the inventory isn't returned to the shelf. (Solution: Use the **Saga Pattern** for distributed transactions).

---

### 🧪 Real-time Scenarios
*   **E-commerce Checkout:** A complex dance between 5 different services.
*   **Scaling specific parts:** Scaling *only* the "Search Service" during a marketing campaign, while leaving the rest of the system as-is.

---

### ⚠️ Edge Cases
*   **Idempotency:** A message is delivered to the Payment service twice. The user must not be charged twice! (Solution: Use unique idempotency keys in the DB).
*   **Version Mismatch:** Service A is updated to a new gRPC version, but Service B is still using the old one. (Solution: Use backward-compatible `.proto` changes).

---

---

Prev: [02_RealTime_Chat_App.md](./02_RealTime_Chat_App.md) | Index: [NodeJS/00_Index.md](../00_Index.md) | Next: [04_Fullstack_App_Node_React.md](./04_Fullstack_App_Node_React.md)
