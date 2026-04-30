# 📌 Topic: Session Affinity and Persistence (Sticky Sessions)

## 🧠 Concept Explanation (Basic → Expert)
**Basic**: Sticky Sessions (Session Affinity) make sure a user stays connected to the same container during their entire visit. This is important if your app "remembers" things about the user in its memory.
**Expert**: Session Affinity is a **Stateful Load Balancing** pattern. While modern architecture prefers "Stateless" containers (where any container can handle any request), legacy apps or specialized real-time systems (WebSockets/Gaming) require a user to have a **Persistent Connection** to a specific container. Staff-level engineering requires managing the **Imbalance Problem** (where one container gets all the "heavy" users) and implementing **Session Externalization** as the long-term solution to eliminate the need for stickiness.

## 🏗️ Mental Model
- **Standard LB**: A busy doctor's office where you see whichever doctor is free. You have to explain your symptoms from scratch every time.
- **Sticky Session**: You always see the same doctor. They remember you, but if that doctor goes on vacation (Container crashes), you are in trouble.

## ⚡ Actual Behavior
- **Cookie-based**: The Load Balancer (Nginx/ALB) inserts a special cookie (e.g., `AWSALB`) into the user's browser. On the next request, the LB reads this cookie and knows exactly which container to send the user to.
- **IP-based (L4)**: The LB hashes the user's IP address. This is less reliable because many users (like in an office) share the same public IP.

## 🔬 Internal Mechanics (Nginx Sticky)
1. **The First Request**: User hits Nginx. Nginx picks a container (Round Robin).
2. **The Signature**: Nginx generates a hash of the container's IP/Port.
3. **The Set-Cookie**: Nginx sends `Set-Cookie: route=abcdef...` to the user.
4. **Subsequent Requests**: User sends the cookie back. Nginx decodes the hash and routes directly to that container, bypassing the load balancing algorithm.

## 🔁 Execution Flow
1. User logs into Container A.
2. Container A stores `user_id: 123` in its local RAM.
3. LB marks User as "Sticky" to Container A.
4. User clicks "View Profile."
5. LB sees stickiness, sends request to Container A.
6. Container A finds user in RAM, returns profile instantly.
7. **Failure**: Container A crashes. LB sends user to Container B.
8. Container B says "Who are you?" -> User is logged out.

## 🧠 Resource Behavior
- **Memory**: Sticky sessions lead to **Memory Pressure**. If you have 1 million users, and they are all "stuck" to specific containers, you can't easily redistribute them if one container's RAM gets full.
- **Imbalance**: If 10 "heavy" users (performing 1000 requests/sec) all get stuck to the same container, that container will burn out while others are idle.

## 📐 ASCII Diagrams (REQUIRED)

```text
       SESSION AFFINITY (STICKY SESSIONS)
       
[ User A ] --( Cookie:ID=1 )--> [ Load Balancer ]
                                     |
          +--------------------------+--------------------------+
          | (Route to ID=1)                                     | (Route to ID=2)
          v                                                     v
   [ CONTAINER 1 ]                                       [ CONTAINER 2 ]
   ( Local Session )                                     ( Local Session )
```

## 🔍 Code (Nginx Sticky Sessions)
```nginx
upstream myapp {
    # Use the 'ip_hash' directive for simple IP-based stickiness
    ip_hash; 
    server srv1.example.com;
    server srv2.example.com;
}

# OR: Using Cookies (Nginx Plus or custom modules)
# sticky cookie srv_id expires=1h domain=.example.com path=/;
```

## 💥 Production Failures
- **The "Rolling Update" Logout**: You update your app. One by one, containers are killed and replaced. Every time a container dies, all users "stuck" to it are logged out.
  *Fix*: Use **Redis** for session storage so it doesn't matter which container a user hits.
- **The "Corporate NAT" Problem**: An entire company (1,000 employees) visits your site. They all share one public IP. Your `ip_hash` balancer sends all 1,000 people to the SAME container, crashing it immediately.

## 🧪 Real-time Q&A
**Q: Should I use Sticky Sessions?**
**A**: **Avoid them if possible.** They make your system fragile and harder to scale. Only use them as a "Stop-gap" for old legacy apps that you can't rewrite, or for specialized real-time apps where the "Handshake" is very expensive.

## ⚠️ Edge Cases
- **Drain Mode**: When you want to take a container offline, you put it in "Drain" mode. The LB stops sending *new* users to it, but continues sending *existing* sticky users until their sessions expire.

## 🏢 Best Practices
- **Externalize State**: Use Redis or Memcached. This is the "Staff" way.
- **Short TTL**: If you must use stickiness, keep the cookie expiration short (e.g., 30 minutes).
- **Monitor Distribution**: Use metrics to ensure your Load Balancer isn't becoming imbalanced.

## ⚖️ Trade-offs
| Feature | No Stickiness (Stateless) | Sticky Sessions (Stateful) |
| :--- | :--- | :--- |
| **Scalability** | **Highest** | Low |
| **Fault Tolerance**| **Highest** | Low (User logs out) |
| **Dev Effort** | Medium (Setup Redis) | **Lowest** |

## 💼 Interview Q&A
**Q: What are the downsides of relying on Sticky Sessions for horizontal scaling?**
**A**: Sticky sessions introduce three major problems: 1. **Imbalance**: Traffic distribution can become skewed if several high-activity users are "stuck" to the same container. 2. **Fragility**: If a container fails or is restarted during an update, all users stuck to it lose their session data, leading to a poor user experience. 3. **Scaling Constraints**: It becomes difficult to "Scale Down" or perform maintenance because you have to wait for all sticky sessions to expire before you can safely remove a container, making the infrastructure less elastic.

## 🧩 Practice Problems
1. Set up a 2-replica app in Compose. Use `curl` to hit it and notice the traffic alternates.
2. Enable `ip_hash` in Nginx and notice how `curl` from your machine now always hits the same container.
3. Replace the local session with a Redis-backed session and disable `ip_hash`. Verify you stay logged in even if you manually stop one of the containers.

---
Prev: [04_Global_Traffic_Management.md](./04_Global_Traffic_Management.md) | Index: [00_Index.md](../00_Index.md) | Next: [01_CPU_and_Memory_Profiling.md](../Performance/01_CPU_and_Memory_Profiling.md)
---
