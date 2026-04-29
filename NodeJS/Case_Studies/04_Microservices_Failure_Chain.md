# 📌 Case Study 04 — The Microservices Failure Chain

## 🛠️ The Scenario
A system consists of 3 services: **Gateway**, **Order Service**, and **Payment Service**.
The Payment Service is slow due to a vendor issue.

**Impact**:
- The Gateway is slow.
- The Order Service is slow.
- Users cannot even *view* their orders, even though that doesn't require the Payment Service.

---

## 🔍 Step 1: Trace the Failure
We use **Distributed Tracing** (Jaeger) to see why the `GetOrder` call is taking 30 seconds.

**The Trace**:
1. `GET /order/123` hits Gateway.
2. Gateway calls `OrderService.get(123)`.
3. `OrderService` calls `PaymentService.getStatus(123)` to see if it's paid.
4. `PaymentService` is slow and takes 30 seconds to timeout.

The `OrderService` is "waiting" on the `PaymentService` for every single request. This exhausts the `OrderService`'s request queue, so it can't handle any other requests.

---

## 🧪 Step 2: The Cascading Failure
Because the `OrderService` is slow, the `Gateway`'s connections are all busy waiting for the `OrderService`. Now the whole Gateway is blocked. This is a **Cascading Failure**.

---

## 💡 Step 3: Optimization - Timeouts
First, we reduce the timeout. It's better to fail in 2 seconds than in 30 seconds.

```javascript
// ✅ SHORT TIMEOUT
const res = await axios.get('http://payment-service/status', { timeout: 2000 });
```
This helps, but the `OrderService` is still wasting 2 seconds on every request for a service we *know* is down.

---

## 🔬 Step 4: The Solution - The Circuit Breaker
We implement a **Circuit Breaker** (Opossum) in the `OrderService`.

```javascript
const breaker = new CircuitBreaker(getPaymentStatus, {
  errorThresholdPercentage: 50,
  resetTimeout: 30000
});

breaker.fallback(() => {
  // Return "Status Unknown" instead of failing
  return { status: 'PENDING_VERIFICATION' };
});
```

**How it works**:
1. After 50% of calls fail, the circuit "Trips" (Opens).
2. For the next 30 seconds, all calls to `getPaymentStatus` immediately execute the `fallback` function.
3. The `OrderService` no longer waits for the `PaymentService`. It responds instantly.

---

## ✅ Step 5: Verification
With the Circuit Breaker:
- The `OrderService` is fast again.
- The `Gateway` is fast again.
- Users can view their orders (with a "Pending" status).
- The `PaymentService` is given "room to breathe" and eventually recovers.

---

## 🏢 Lessons Learned
1. **Never wait forever**: Always set aggressive timeouts for internal microservice calls.
2. **Fail Gracefully**: Use fallbacks to provide a partial experience rather than a total outage.
3. **Isolate Failures**: Use circuit breakers to prevent a slow downstream service from taking down the entire system.

---

**Next:** [05_Zero_Downtime_Migration.md](./05_Zero_Downtime_Migration.md)
