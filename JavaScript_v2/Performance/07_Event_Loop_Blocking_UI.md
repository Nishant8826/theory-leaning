# 📌 07 — Event Loop Blocking UI

## 🧠 Concept Explanation

Long tasks on the main thread block everything: user input, rendering, and network callbacks. Any task exceeding ~50ms is measurable as "Long Task" (Lighthouse/CrUX). Tasks over 100ms cause visible jank. Tasks over 300ms cause users to perceive the app as unresponsive.

## 🔍 Code Examples

### Long Task Detection

```javascript
// PerformanceObserver for Long Tasks
const observer = new PerformanceObserver((list) => {
  list.getEntries().forEach(entry => {
    console.warn(`Long task: ${entry.duration.toFixed(1)}ms`, {
      startTime: entry.startTime,
      attribution: entry.attribution
    })
    
    // Send to RUM (Real User Monitoring)
    sendMetric('long_task', {
      duration: entry.duration,
      startTime: entry.startTime
    })
  })
})
observer.observe({ entryTypes: ['longtask'] })
```

### Yielding to Main Thread (Time-Sliced Processing)

```javascript
// Modern: scheduler.yield() (Chrome 115+)
async function processLargeArray(items) {
  const CHUNK_SIZE = 100
  const results = []
  
  for (let i = 0; i < items.length; i++) {
    results.push(processItem(items[i]))
    
    if (i % CHUNK_SIZE === 0) {
      // Yield to allow browser to handle frames, input, etc.
      await scheduler.yield()  // Chrome 115+
      // Fallback:
      // await new Promise(resolve => setTimeout(resolve, 0))
    }
  }
  
  return results
}

// Measure if yielding helps:
// Before: 500ms long task (one chunk)
// After: 5 × 100ms tasks with yielding = lower jank, same total
```

### Main Thread Work Budget

```javascript
class WorkBudget {
  constructor(budgetMs = 10) {
    this.budgetMs = budgetMs
    this.startTime = performance.now()
  }
  
  exceeded() {
    return (performance.now() - this.startTime) >= this.budgetMs
  }
  
  reset() {
    this.startTime = performance.now()
  }
  
  static async withBudget(fn, budgetMs = 10) {
    const budget = new WorkBudget(budgetMs)
    
    while (true) {
      const done = fn(budget)
      if (done) break
      if (budget.exceeded()) {
        await scheduler.yield?.() ?? new Promise(r => setTimeout(r))
        budget.reset()
      }
    }
  }
}
```

## 💥 Production Failure — JSON.parse Blocking

```javascript
// Common: large API response parsed synchronously
app.get('/large-export', async (req, res) => {
  const data = await db.query('SELECT * FROM events LIMIT 100000')
  
  // JSON.stringify of 100k rows = 200-500ms BLOCK
  const json = JSON.stringify(data)
  res.end(json)
  // During stringify: zero other requests handled
})

// Fix: Stream response
app.get('/large-export', async (req, res) => {
  res.setHeader('Content-Type', 'application/json')
  const stream = db.queryStream('SELECT * FROM events LIMIT 100000')
  stream.pipe(new JSONStreamStringifier()).pipe(res)
})
```

## 🏢 Industry Best Practices

1. **Long Task API in production** — Every task >50ms should be tracked and alerted.
2. **Time-slice CPU work** — Use `scheduler.yield()` every 50-100ms of compute.
3. **Move heavy work to Worker Threads** — Image processing, PDF generation, ML inference.
4. **Use requestIdleCallback** — For non-critical background work.
5. **Measure INP** — Interaction to Next Paint is Google's real responsiveness metric.

## 🔗 Navigation

**Prev:** [06_Deoptimization_and_ICs.md](06_Deoptimization_and_ICs.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [08_GC_Performance_Tuning.md](08_GC_Performance_Tuning.md)
