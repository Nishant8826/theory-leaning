# 📌 Case Study 01 — Debugging a Real-World Memory Leak

## 🛠️ The Scenario
A high-traffic e-commerce API is crashing with `OOM (Out of Memory)` every 6 hours. The team has doubled the RAM, but the crash still happens, just every 12 hours instead. 

**Symptoms**:
- Memory RSS grows steadily.
- CPU usage increases over time (due to GC working harder).
- Latency spikes before the crash.

---

## 🔍 Step 1: Baseline and Hypothesize
First, we look at the monitoring dashboard. We see a "Sawtooth" pattern, but the bottom of the teeth is rising. This confirms a leak.

**Hypothesis**: Something is capturing request data and never releasing it.

---

## 🧪 Step 2: Collection (The Heap Snapshot)
We cannot wait 6 hours for the crash. We use `clinic doctor` to confirm the leak and then generate heap snapshots.

```bash
# Capture a snapshot at start
node --inspect app.js
# (In Chrome DevTools, Take Snapshot 1)

# Generate load to trigger the leak
autocannon -c 100 -d 30 http://localhost:3000/api/product/123

# Capture a snapshot after load
# (In Chrome DevTools, Take Snapshot 2)
```

---

## 🔬 Step 3: Analysis (Comparison View)
In Chrome DevTools, we select **Snapshot 2** and change the view to **Comparison** (compared to Snapshot 1).

We look for objects with a high `# New` and a low `# Deleted`.
We see:
- `(string)`: +50,000
- `(closure)`: +50,000
- `Object`: +50,000

We expand one of the `Object` entries and look at the **Retainers** (the objects holding onto this memory).

---

## 💡 Step 4: The "Aha!" Moment
The retainer path looks like this:
`Object` ──▶ `context` ──▶ `listener` ──▶ `EventEmitter` ──▶ `DatabaseConnection`

We look at the code:
```javascript
// product.controller.js
const db = require('./db-connection');

app.get('/api/product/:id', (req, res) => {
  const logData = { id: req.params.id, time: Date.now() };
  
  // ❌ THE LEAK: Adding a listener to a GLOBAL object inside a request
  db.on('query', () => {
    console.log('Query executed for product:', logData.id);
  });

  const product = await db.findProduct(req.params.id);
  res.json(product);
});
```
Every request adds a **new** listener to the global `db` object. That listener closure captures `logData` and the entire request context. The listeners are never removed, so they stay in memory forever.

---

## ✅ Step 5: The Fix
We change `.on()` to `.once()`, or better yet, we move the logging logic outside of the request handler or use a dedicated logging service.

```javascript
// ✅ FIXED
db.once('query', () => {
  console.log('Query executed');
});
```

---

## 📈 Step 6: Verification
We run the same `autocannon` load test and take a third snapshot. The number of listeners and strings is now stable. The memory RSS is no longer growing.

---

## 🏢 Lessons Learned
1. **Never subscribe to a long-lived emitter inside a short-lived request.**
2. **Use `once()`** if you only need the next event.
3. **Always use Comparison View** in heap snapshots to filter out the "noise" of normal allocations.

---

**Next:** [02_Optimizing_API_Latency.md](./02_Optimizing_API_Latency.md)
