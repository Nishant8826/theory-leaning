# 📌 Topic: Blue-Green and Canary Deploys (Strategy)

## 🧠 Concept Explanation (Basic → Expert)
**Basic**: Blue-Green deployment means having two identical environments. One is "Live" (Blue), and one is "New" (Green). You test the new one, and then flip a switch to make it live. Canary deployment is like the "Canary in a coal mine"—you send a tiny bit of traffic to the new version first to see if it "dies" (crashes) before sending everyone there.
**Expert**: These are **Progressive Delivery Strategies** designed to minimize **Blast Radius** and ensure **Zero-Downtime**. Blue-Green is a binary switch (All-or-nothing), while Canary is an incremental rollout (1% -> 10% -> 50% -> 100%). Staff-level engineering requires mastering the **Network Cutover** (using DNS or Load Balancers), managing **Database Schema Compatibility** (ensuring the DB works with both old and new code simultaneously), and implementing **Automated Rollbacks** triggered by real-time health metrics.

## 🏗️ Mental Model
- **Blue-Green**: A stage with two identical sets. You perform on Set A while you build Set B behind the curtain. When ready, you close the curtain for 1 second and open it on Set B.
- **Canary**: A new recipe at a restaurant. You don't give it to all 100 customers at once. You give it to 2 tables first. If they like it and don't get sick, you give it to the whole restaurant.

## ⚡ Actual Behavior
- **Blue-Green**: Requires 2x the infrastructure. You run 10 containers for Blue and 10 for Green.
- **Canary**: Uses existing infrastructure. You replace 1 container out of 10 with the new version.

## 🔬 Internal Mechanics (The Traffic Split)
1. **Load Balancer (ALB/Nginx)**: The "Brain." It has two "Target Groups."
2. **The Switch**: To flip from Blue to Green, you update the Listener rule in the Load Balancer to point to the new Target Group.
3. **Weighting**: For Canary, you tell the Load Balancer: "Send 90% of traffic to Target Group A and 10% to Target Group B."

## 🔁 Execution Flow (Canary)
1. CI builds `app:v2`.
2. CD deploys 1 replica of `v2` alongside 9 replicas of `v1`.
3. Monitoring (Prometheus) watches for 5xx errors on `v2`.
4. If errors < 0.1%, CD deploys 3 more replicas of `v2`.
5. If still healthy, CD replaces all remaining `v1` replicas.
6. If errors spike, CD instantly deletes the `v2` replica and reverts the traffic.

## 🧠 Resource Behavior
- **Blue-Green Cost**: High. You are paying for double the servers during the cutover.
- **Risk**: Blue-Green is safer for "Breaking Changes." Canary is better for "Performance Verification."

## 📐 ASCII Diagrams (REQUIRED)

```text
       BLUE-GREEN vs CANARY
       
    [ BLUE-GREEN ]               [ CANARY ]
       (Switch)                  (Weight)
          |                         |
   +------+------+           +------+------+
   |             |           |             |
[ v1 ]  -->  [ v2 ]       [ v1 ] (90%)  [ v2 ] (10%)
(Idle)      (Live)        (Live)        (Testing)
```

## 🔍 Code (Nginx Weighted Canary)
```nginx
# Simple Nginx split based on a cookie or random weight
http {
    upstream v1 { server app-v1:3000; }
    upstream v2 { server app-v2:3000; }

    split_clients "${remote_addr}AAA" $variant {
        10%     v2;
        *       v1;
    }

    server {
        listen 80;
        location / {
            proxy_pass http://$variant;
        }
    }
}
```

## 💥 Production Failures
- **The "Stateful Session" Break**: A user is on a Blue container. You flip the switch to Green. The user's session data was stored in Blue's local RAM. The user is suddenly logged out.
  *Fix*: Use a shared Redis session store.
- **The "DB Version Conflict"**: App v2 adds a `last_login` column to the DB. You roll out a Canary. App v1 (the 90%) doesn't know about this column and crashes when it tries to read the record.
  *Fix*: Use "Two-Phase Migrations" (Add the column first, then deploy the code).

## 🧪 Real-time Q&A
**Q: Which one should I choose?**
**A**: Use **Blue-Green** for major infrastructure changes or when you can afford the extra cost. Use **Canary** for frequent, small code updates where you want to detect subtle performance regressions or bugs under real load.

## ⚠️ Edge Cases
- **Sticky Sessions**: If a user is assigned to the "Canary" version, they should stay there. You don't want them flipping between v1 and v2 on every click. Use a cookie-based affinity.

## 🏢 Best Practices
- **Automate the Rollback**: Never rely on a human to "Click the button" if a canary fails.
- **Monitoring is Mandatory**: You cannot do canary deployments without deep observability (Metrics/Logs).
- **Small Steps**: Start with 1% traffic. Many bugs only appear at scale.

## ⚖️ Trade-offs
| Strategy | Infrastructure Cost | Safety | Rollback Speed |
| :--- | :--- | :--- | :--- |
| **Recreate** | **Lowest** | Low | Slow |
| **Blue-Green** | Highest | **Highest**| **Instant** |
| **Canary** | Low | High | Fast |

## 💼 Interview Q&A
**Q: How do you handle database schema changes during a Blue-Green deployment?**
**A**: I follow the **Expand and Contract** pattern. First, I apply a "Forward-Compatible" migration to the database (e.g., adding a new column but keeping the old one). This ensures that both the current Blue version and the upcoming Green version can work with the database. Then, I perform the Blue-Green switch. Once Green is confirmed stable, I perform a second migration to "Contract" the database by removing the now-obsolete old columns. This ensures that the database is never a bottleneck or a source of failure during the environment switch.

## 🧩 Practice Problems
1. Set up two Nginx services in Docker Compose (`blue` and `green`). Manually update an `lb` service to point to one or the other.
2. Use the `split_clients` directive in Nginx to implement a 50/50 traffic split.
3. Research "Argo Rollouts" to see how Kubernetes automates these complex strategies.

---
Prev: [03_Caching_Build_Layers_in_CI.md](./03_Caching_Build_Layers_in_CI.md) | Index: [00_Index.md](../00_Index.md) | Next: [05_Artifact_Management.md](./05_Artifact_Management.md)
---
