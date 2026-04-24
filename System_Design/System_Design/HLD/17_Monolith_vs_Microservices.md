# 📌 Monolith vs Microservices

## 🧠 Concept Explanation (Story Format)

**Monolith:** You live in a house. Kitchen, bedroom, bathroom — all in one building. Easy to manage. Need more space? You add a room. But if the kitchen catches fire, the whole house is in danger.

**Microservices:** You own a city block of apartments. Each apartment has its own kitchen, bathroom, utility meters. Kitchen fire in one apartment doesn't affect others. But managing 50 apartments is far more complex than one house.

Neither is "better" — they're right for different situations.

Shopify ran as a monolith for years. Amazon started as a monolith and broke it apart. WhatsApp served 900M users with 50 engineers — mostly a monolith! Startups that jump to microservices on Day 1 often regret it.

---

## 🏗️ Monolith Architecture

```
┌────────────────────────────────────┐
│         Single Node.js App         │
│                                    │
│  ┌──────────┐    ┌──────────────┐  │
│  │  Auth    │    │   Posts      │  │
│  │  Routes  │    │   Routes     │  │
│  └──────────┘    └──────────────┘  │
│  ┌──────────┐    ┌──────────────┐  │
│  │  Users   │    │  Payments    │  │
│  │  Routes  │    │  Routes      │  │
│  └──────────┘    └──────────────┘  │
│                                    │
│  Shared: DB Connection, Redis,     │
│          Middleware, Config         │
└────────────────────────────────────┘
          ↓ One deployment
   [AWS EC2 / Heroku / Railway]
          ↓
   [Single PostgreSQL + MongoDB]
```

---

## ⚡ Microservices Architecture

```
┌──────────┐ ┌──────────┐ ┌──────────┐
│  Auth    │ │  Users   │ │  Posts   │
│ Service  │ │ Service  │ │ Service  │
│ Node.js  │ │ Node.js  │ │ Node.js  │
│ Port3001 │ │ Port3002 │ │ Port3003 │
│ Postgres │ │ Postgres │ │ MongoDB  │
└──────────┘ └──────────┘ └──────────┘
      ↑               ↑           ↑
[AWS API Gateway — Routes all requests]
      ↑
[React / Next.js Frontend]
```

---

## 🔍 Key Components

### When to Choose Monolith

✅ **Use Monolith when:**

1. **You're a startup / small team (< 10 engineers)**
   - Fast to build and iterate
   - Don't need separate deployments
   - Simpler debugging

2. **You don't know your domain yet**
   - Domain boundaries unclear → wrong microservice split = worse than monolith
   - Build monolith first, learn the domain, then extract services

3. **Traffic is manageable**
   - < 100K users? A well-tuned monolith with Redis + read replicas handles it
   - Uber started running millions of rides as a mostly monolith

4. **Budget constraints**
   - Microservices need more DevOps, monitoring, infrastructure

```javascript
// Well-organized monolith (Modular Monolith)
// Single app, but code is organized as if it were microservices

project/
├── modules/
│   ├── auth/
│   │   ├── auth.router.js
│   │   ├── auth.service.js
│   │   └── auth.test.js
│   ├── users/
│   │   ├── users.router.js
│   │   ├── users.service.js
│   │   └── users.test.js
│   └── posts/
│       ├── posts.router.js
│       └── posts.service.js
├── shared/
│   ├── database.js
│   ├── redis.js
│   └── logger.js
└── app.js
```

### When to Choose Microservices

✅ **Use Microservices when:**

1. **Different parts need different scaling**
   ```
   - Video encoding: 1000 Lambda instances during peak
   - Auth: Just 2 small EC2 instances
   - Can't scale these independently in a monolith
   ```

2. **Large team, team autonomy matters**
   - 10 teams of 5 engineers each
   - Each team owns a service, deploys independently
   - No "deployment freeze" coordination needed

3. **Different tech requirements**
   - Video processing → Python (OpenCV)
   - Real-time notifications → Node.js + Socket.IO
   - ML recommendations → Python + TensorFlow
   - Not possible in one language monolith

4. **High availability requirements per component**
   - Payment service needs 99.999% uptime
   - Profile service can tolerate brief downtime
   - Separate deployments = separate SLAs

---

### The "Strangler Fig" Pattern (Gradual Migration)

Don't rewrite everything at once! Extract services one by one:

```
Phase 1: Monolith
┌────────────────────────────┐
│ Auth | Users | Posts | Pay │
└────────────────────────────┘

Phase 2: Extract Payment Service (highest priority)
┌──────────────────┐  ┌─────────┐
│ Auth | Users | P │  │ Payment │
│  (monolith)      │  │ Service │
└──────────────────┘  └─────────┘
API Gateway routes /payment/* to Payment Service
Everything else still to monolith

Phase 3: Extract Auth Service
┌─────────────┐  ┌────────┐  ┌─────────┐
│ Users | P   │  │  Auth  │  │ Payment │
│ (monolith)  │  │ Service│  │ Service │
└─────────────┘  └────────┘  └─────────┘

Phase N: Full Microservices (when needed)
```

```javascript
// API Gateway configuration evolves gradually
// Monolith handles everything initially:
app.use('/api', monolithRouter);

// Later, extract specific routes:
// In API Gateway (AWS Console):
// /api/payments/* → payment-service-url
// /api/auth/* → auth-service-url
// /api/* → monolith-url (catch-all)
```

---

## ⚖️ Trade-offs Comparison

| Factor | Monolith | Microservices |
|--------|----------|---------------|
| **Development Speed** | Faster initially | Slower initially |
| **Deployment** | Simple | Complex (CI/CD pipeline per service) |
| **Debugging** | Simple (one log stream) | Hard (distributed tracing needed) |
| **Testing** | Easy (unit + integration) | Complex (contract testing, integration) |
| **Scaling** | Whole app scales | Per-service scaling |
| **Fault Isolation** | One crash = everything down | Failures isolated |
| **Database** | Shared (easy joins) | Separate (no joins across services) |
| **Network** | In-process calls (0ms) | HTTP calls (1-20ms latency) |
| **Infrastructure** | One deployment | Many deployments, load balancers |
| **Team Size** | < 15 engineers | 15+ engineers |
| **Operational Cost** | Low | High |

---

## 📊 Scalability Discussion

### Real Company Examples

**Shopify (Mostly Monolith):**
- One massive Ruby on Rails monolith
- Serves millions of merchants + buyers
- Uses: Sharding, Read replicas, Redis heavily
- Only extracted very specific services over time
- Lesson: A well-optimized monolith can scale far

**Airbnb (Started Monolith, Moved to Services):**
- Started as a Ruby monolith
- As they scaled, extracted services for Search, Payments, Messaging
- Still not "pure microservices" — big services with sub-services

**Amazon (True Microservices):**
- 100,000+ services!
- Each team is a "2-pizza team" (max 10 people)
- Team owns service end-to-end (design, code, deploy, monitor)
- Enabled by strong platform (AWS itself)

### Decision Framework

```
START HERE:
Is your team < 10 people?
  YES → Build monolith. Period.
  NO → Continue...

Is your system well-understood (not a new domain)?
  NO → Build monolith first. Learn the domain.
  YES → Continue...

Do different parts need drastically different scaling?
  YES → Consider microservices for those specific parts.
  NO → Stick with modular monolith.

Do you have DevOps expertise?
  NO → Microservices will kill you. Build monolith.
  YES → You can consider microservices.
```

---

## 💼 Interview Questions (WITH SOLUTIONS)

### Q1: What are the main differences between a monolith and microservices?

**Solution:**
| | Monolith | Microservices |
|-|----------|---------------|
| Codebase | One repository | Many repositories |
| Deployment | Deploy once | Deploy each service independently |
| Database | Shared DB | Each service has its own DB |
| Communication | In-process function calls | HTTP APIs or message queues |
| Team structure | All teams work in same codebase | Each team owns a service |
| Scaling | Scale all together | Scale each independently |
| Failure | Single failure can cascade | Isolated failures |

---

### Q2: Why would you NOT start with microservices for a new product?

**Solution:**
1. **Premature complexity:** You don't know your domain boundaries yet. Wrong split = massive refactoring later.
2. **Slower development:** Setting up 10 services, CI/CD pipelines, API contracts takes weeks vs hours for monolith.
3. **Distributed system problems:** Network failures, latency, distributed transactions — all new challenges.
4. **Operational overhead:** Need Kubernetes/ECS, centralized logging, distributed tracing, service discovery.
5. **Cost:** Running 10 services on ECS costs 10x more than one EC2 instance.

> "The microservices premium is not worth it unless you have scale or team problems a monolith can't solve." — Martin Fowler

Start with a well-organized **modular monolith**. Extract services when you have a specific, justified reason.

---

### Q3: What is a "modular monolith" and why is it better than a poorly organized monolith?

**Solution:**
A modular monolith is a single deployable app where code is organized into independent modules with clear boundaries — as if they were microservices, but in one codebase.

```javascript
// ❌ Spaghetti Monolith
// routes/users.js calls posts.service.js directly
// posts.service.js accesses auth.model.js directly
// Everything knows about everything

// ✅ Modular Monolith
// modules/users/ only exposes its service via a public interface
// modules/posts/ calls users via the public interface only
// No direct DB access across module boundaries

// users/index.js (public interface)
module.exports = {
  getUser: userService.getUser,
  getUserProfile: userService.getProfile
  // ONLY these functions are exposed to other modules
};

// posts/posts.service.js
const usersModule = require('../users'); // Via public interface only
const user = await usersModule.getUser(userId); // NOT: require('../users/users.model.js')
```

Benefits:
- Can extract modules to microservices later without rewriting
- Clear ownership
- Easier testing
- Forces good design

---

### Q4: What is the "two-pizza rule" and how does it relate to microservices?

**Solution:**
Amazon's Jeff Bezos said: "If a team needs more than two pizzas to be fed, it's too large."

Two-pizza team = 6-10 people.

This rule applies to microservices: **Each microservice should be owned by a team small enough for two pizzas.**

Why it matters:
- Small teams communicate efficiently
- Team owns service end-to-end (design, build, deploy, monitor, on-call)
- No need to coordinate deployments with 50 other developers
- Team can make technical decisions without committee approval

If your service needs 20 people to maintain → it's too big → split it.
If you don't have enough people to own a service → microservices too granular → merge services.

---

### Q5: How do you decide where to draw service boundaries in microservices?

**Solution:**
Use **Domain-Driven Design (DDD)** concepts:

1. **Bounded Contexts:** Each service should map to a business domain boundary.
   - User Management (auth, profiles)
   - Order Processing (checkout, order history)
   - Payment (billing, refunds)
   - Catalog (products, inventory)
   - Shipping (delivery, tracking)

2. **High Cohesion, Low Coupling:**
   - Functions that change together → stay together (high cohesion)
   - Functions that need to communicate a lot → same service (low coupling)

3. **Data ownership:**
   - Service owns its data. If Service A needs Service B's data all the time → maybe they should be one service.

4. **Team boundaries:**
   - Services align with team structure (Conway's Law: systems mirror communication structure)

5. **Service size sanity check:**
   - Too small: "User password hashing service" → over-engineering
   - Too big: "Everything except payments" → just a monolith with extra steps
   - Right size: Can be understood completely by 2-6 people in an afternoon

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem 1: You have a monolith that's getting slow. What's your approach?

**Solution:**
Before jumping to microservices, try these first:

**Step 1: Profile and identify the bottleneck**
- Use APM (Application Performance Monitoring): New Relic, Datadog
- Find the slow queries, slow routes
- Often: 20% of code causes 80% of performance issues

**Step 2: Add caching**
- Redis for hot data
- Often 10x improvement without architectural changes

**Step 3: Add database read replicas**
- Most monoliths are read-heavy
- Route reads to replicas → dramatic improvement

**Step 4: Optimize the worst queries**
- Add indexes
- Fix N+1 queries
- Add connection pooling

**Step 5: Scale the monolith horizontally**
- Multiple EC2 instances behind ALB
- Make app stateless (sessions in Redis)
- Works for most traffic levels

**Only if all above is insufficient:**
**Step 6: Extract the specific service that's the bottleneck**
- If only the video encoding is slow → extract VideoProcessingService
- Don't rewrite the whole thing

---

### Problem 2: Design the microservices split for an Uber-like app

**Solution:**
```
Services & Boundaries:

1. Auth Service
   - Login, register, JWT validation
   - DB: PostgreSQL (users_auth table)
   - Owned by: Identity team

2. User Service
   - Rider profiles, driver profiles
   - Ratings, reviews
   - DB: PostgreSQL
   - Owned by: User team

3. Location Service (Highest scale!)
   - Real-time driver positions (updates every 3 seconds!)
   - Find nearby drivers (geospatial queries)
   - DB: Redis (sorted set with geospatial data)
   - WebSocket connections for real-time
   - Owned by: Maps team

4. Ride Matching Service
   - Match rider with nearby driver
   - Pricing calculation (surge)
   - DB: PostgreSQL (rides), Redis (active rides)
   - Owned by: Dispatch team

5. Trip Service
   - Ongoing trip state, tracking
   - DB: MongoDB (flexible trip data)
   - WebSocket for real-time updates
   - Owned by: Trips team

6. Payment Service
   - Charge rider, pay driver
   - DB: PostgreSQL (ACID transactions!)
   - Owned by: Payments team (PCI compliance)

7. Notification Service
   - Push notifications, SMS, email
   - Queue: SQS
   - Owned by: Comm team

Communication:
- Sync REST: Auth validation, location queries
- Async Events: Ride completed → Payment, Rating request, Notification
- WebSocket: Driver tracking, ride status updates

The Location Service would be a microservice even for a small Uber clone
because it has 100x the traffic of other services.
```

---

### Navigation
**Prev:** [16_Microservices.md](16_Microservices.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [18_Storage_Systems.md](18_Storage_Systems.md)
