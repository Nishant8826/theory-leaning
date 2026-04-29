# 📌 Case Study 02 — Optimizing API Latency: From 2s to 200ms

## 🛠️ The Scenario
A "User Dashboard" API endpoint is consistently slow. Users are complaining that it takes several seconds to load their data.

**Metrics**:
- Average Latency: 2.1 seconds.
- Throughput: 5 RPS.
- Server CPU: 10%.

---

## 🔍 Step 1: Identify the Bottleneck
Since CPU is low, the issue is likely **I/O Wait** or **Serial Execution**, not heavy math. We use `clinic flame` to visualize where the time is spent.

```bash
npx clinic flame -- autocannon -c 10 -d 20 http://localhost:3000/api/dashboard
```

The flamegraph shows many small bars with lots of gaps between them. This confirms the app is waiting for external dependencies.

---

## 🧪 Step 2: Analyze the Code
We look at the dashboard controller:

```javascript
// dashboard.controller.js
app.get('/api/dashboard', async (req, res) => {
  const user = await db.users.findById(req.user.id); // 200ms
  const posts = await db.posts.findAll({ userId: user.id }); // 500ms
  const followers = await db.followers.count({ userId: user.id }); // 400ms
  const analytics = await analyticsSvc.get(user.id); // 1000ms
  
  res.json({ user, posts, followers, analytics });
});
```
The logic is a **Waterfall**. Each request waits for the previous one to finish. Total time = $200 + 500 + 400 + 1000 = 2100ms$.

---

## 💡 Step 3: Optimization - Parallelization
Since the `posts`, `followers`, and `analytics` queries don't depend on each other (they only need the `user.id`), we can run them in parallel.

```javascript
// ✅ OPTIMIZED
app.get('/api/dashboard', async (req, res) => {
  const user = await db.users.findById(req.user.id);
  
  // Fire the rest in parallel
  const [posts, followers, analytics] = await Promise.all([
    db.posts.findAll({ userId: user.id }),
    db.followers.count({ userId: user.id }),
    analyticsSvc.get(user.id)
  ]);
  
  res.json({ user, posts, followers, analytics });
});
```
New total time = $200ms (User) + \max(500, 400, 1000) = 1200ms$. Still a bit slow.

---

## 🔬 Step 4: Further Optimization - Caching
The `analytics` call takes 1 second and the data only updates once an hour. We add a Redis cache.

```javascript
// ✅ CACHED
const cachedAnalytics = await redis.get(`analytics:${user.id}`);
let analytics;

if (cachedAnalytics) {
  analytics = JSON.parse(cachedAnalytics);
} else {
  analytics = await analyticsSvc.get(user.id);
  await redis.set(`analytics:${user.id}`, JSON.stringify(analytics), 'EX', 3600);
}
```
Now, with a cache hit, the total time is $200ms + \max(500, 400, 5) = 700ms$.

---

## ⚡ Step 5: Final Optimization - Database Tuning
We look at the `db.posts.findAll` query. It doesn't have an index on `userId`. We add a B-Tree index.

```sql
CREATE INDEX idx_posts_user_id ON posts(user_id);
```
The query time drops from 500ms to 50ms.

---

## 📈 Step 6: Final Results
Final total time (with cache and index): $200ms + \max(50, 40, 5) = 250ms$.

**Improvement**: $2100ms$ ──▶ $250ms$ ($8.4x$ faster).

---

## 🏢 Lessons Learned
1. **Parallelize Independent I/O**: Don't use `await` in a loop or waterfall if tasks aren't dependent.
2. **Profile before you guess**: The flamegraph clearly showed the "waiting" gaps.
3. **Check your Indexes**: Database performance is often the root cause of high latency in Node.js.

---

**Next:** [03_Handling_a_Traffic_Spike.md](./03_Handling_a_Traffic_Spike.md)
