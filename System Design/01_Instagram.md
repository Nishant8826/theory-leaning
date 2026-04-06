# 🎯 System Design: Instagram (Like Photo & Video Sharing Platform)
> **Level:** Beginner-Friendly | **Format:** What → Why → How → Impact
> **Stack:** Next.js + Node.js + MySQL + MongoDB (Polyglot) + Redis + CDN

---

## 1. 📋 REQUIREMENTS

### 🧠 Think of it like this
> Imagine you're building a digital photo album that 500 million people share. You need to list what features the album MUST have (Functional) and how well it should PERFORM (Non-Functional).

---

### ✅ Functional Requirements (FR)

| # | Requirement | What | Why | How | Impact if Missing |
|:--|:-----------|:-----|:----|:----|:-----------------|
| FR1 | **User Authentication** | Signup, Login, Logout | Users need a unique identity to own posts & follow others | JWT tokens + bcrypt password hashing | Anyone could impersonate anyone else |
| FR2 | **Upload Photos/Videos** | Post images/videos with captions | Core purpose — visual content sharing | Multipart upload → Backend → S3 storage | No content = no app |
| FR3 | **News Feed** | Personalized timeline of posts from followed users | Users want to see content from people they care about | Hybrid Push/Pull model with Redis | Users see nothing when they open the app |
| FR4 | **Like & Comment** | React to and discuss posts | Social engagement is the core loop | MongoDB documents + Redis counters | No interaction = no engagement = users leave |
| FR5 | **Follow/Unfollow** | Connect with other users | Build a social graph for feed personalization | MySQL relational table (follower ↔ following) | No social graph = no personalized feed |
| FR6 | **Search** | Find users, hashtags, locations | Discovery of new content and people | Elasticsearch with prefix matching | Users can't find friends or trending content |
| FR7 | **User Profile** | View bio, posts, follower/following counts | Public identity and content showcase | MySQL (profile data) + MongoDB (posts grid) | No way to view someone's content collection |

### ⚙️ Non-Functional Requirements (NFR)

| # | Requirement | What | Why | Real-World Example | Impact if Missing |
|:--|:-----------|:-----|:----|:-------------------|:-----------------|
| NFR1 | **Scalability** | Handle 500M+ active users | User base grows exponentially | Instagram went from 0 → 1B users in 8 years | App crashes under load, users leave |
| NFR2 | **High Availability (99.99%)** | System never goes "down" | Users are global, every timezone is peak somewhere | If down for 1 hour = millions of posts lost | Users switch to competitors |
| NFR3 | **Low Latency (<200ms)** | Feed loads instantly | Users abandon apps that take >3 seconds | Feed should feel instant on scroll | Slow app = user frustration = uninstalls |
| NFR4 | **Reliability** | Uploaded photos are NEVER lost | Photos are irreplaceable memories | S3 provides 99.999999999% durability (11 nines) | Losing user photos = trust destroyed forever |
| NFR5 | **Eventual Consistency** | Likes/comments can take 1-2s to sync globally | Strict consistency at scale is extremely expensive | A like showing up 2s late is acceptable | Over-engineering consistency wastes resources |

---

## 2. 📊 SCALE & CONSTRAINTS

### 🧠 Think of it like this
> Imagine a restaurant. Day 1, you serve 10 customers. Month 6, you serve 10,000. Year 3, you serve 10 million. The kitchen, tables, and staff must grow — but HOW you grow matters.

---

### Traffic Estimation

| Metric | Calculation | Result |
|:-------|:-----------|:-------|
| **Daily Active Users (DAU)** | 500M × 60% active | **300M** |
| **Posts per day** | 300M × 2% post daily | **6M posts/day** |
| **Feed reads per day** | 300M × 10 opens/day | **3B reads/day** |
| **Likes per day** | 300M × 5 likes/day avg | **1.5B likes/day** |
| **Reads RPS (normal)** | 3B ÷ 86,400 | **~35,000 RPS** |
| **Reads RPS (peak, 3x)** | 35K × 3 | **~100,000 RPS** |
| **Writes RPS (normal)** | 6M ÷ 86,400 | **~70 RPS** |

### Storage Estimation

| Data Type | Size per Unit | Daily Volume | Annual Storage |
|:----------|:-------------|:-------------|:---------------|
| **Photos (3 sizes)** | ~2MB avg (thumb+std+orig) | 6M × 2MB = 12TB/day | **~4.4 PB/year** |
| **Videos** | ~50MB avg | 500K × 50MB = 25TB/day | **~9 PB/year** |
| **Post metadata** | ~1KB | 6M × 1KB = 6GB/day | **~2 TB/year** |
| **User data** | ~2KB | Grows slowly | **~1 GB total** |

### Scaling Journey

| Stage | Users | Infra Needed |
|:------|:------|:-------------|
| **MVP** | 0 – 10K | 1 server, 1 DB, local file storage |
| **Growth** | 10K – 1M | Load balancer, read replicas, S3 + CDN |
| **Scale** | 1M – 50M | Microservices, Redis caching, DB sharding |
| **Massive** | 50M – 500M | Multi-region, Kubernetes, advanced sharding, dedicated feed service |

---

## 3. 💰 BUDGET & COSTING

### 🧠 Think of it like this
> Running a small chai stall costs ₹500/day. Running a restaurant chain costs ₹5 lakhs/day. The architecture must match the budget AND the user count.

---

| Component | Startup (10K users) | Mid Scale (5M users) | Large Scale (500M users) |
|:----------|:-------------------|:---------------------|:------------------------|
| **Compute (EC2/EKS)** | 1 server (~$20/mo) | 10-20 instances (~$500/mo) | 1000+ containers on Kubernetes (~$50K/mo) |
| **MySQL DB** | Single instance (~$15/mo) | Master + 3 replicas (~$300/mo) | Sharded cluster + replicas (~$10K/mo) |
| **MongoDB** | Atlas free tier ($0) | Dedicated cluster (~$200/mo) | Sharded multi-region (~$8K/mo) |
| **Redis Cache** | Micro instance (~$15/mo) | Cluster (~$200/mo) | Multi-AZ cluster (~$5K/mo) |
| **S3 Storage** | Pay-as-you-go (~$5/mo) | ~$500/mo | ~$50K/mo (petabytes) |
| **CDN (CloudFront)** | Minimal (~$5/mo) | ~$300/mo | ~$30K/mo (global edge) |
| **Load Balancer** | Not needed | ALB (~$50/mo) | Multi-region ALBs (~$2K/mo) |
| **Total** | **~$60/mo** | **~$2,000/mo** | **~$150K+/mo** |

**💡 Key Reasoning:**
- **Startup:** Use managed services (RDS, Atlas) to avoid hiring a DBA. Save money, not time.
- **Mid Scale:** Add caching (Redis) before scaling DB — caching is 10x cheaper than more DB servers.
- **Large Scale:** CDN cost dominates because serving 4+ PB of images/year is the most expensive operation.

---

## 4. 🏗️ HIGH LEVEL DESIGN (HLD)

### 🧠 Think of it like this
> Imagine a giant post office. The user (sender) drops a letter (post). The post office (backend) stamps it, stores a copy in a file cabinet (DB), puts the actual photo in a warehouse (S3), and delivers copies to every subscriber's mailbox (feed via Redis).

---

### Why Next.js?

| Rendering Mode | What | When to Use in Instagram | Benefit |
|:---------------|:-----|:------------------------|:--------|
| **SSR (Server-Side Rendering)** | HTML generated on server per request | User profile pages (dynamic, unique per user) | SEO-friendly + fast first paint |
| **SSG (Static Site Generation)** | HTML generated at build time | Landing page, About, Help pages | Fastest possible load, cached at CDN |
| **CSR (Client-Side Rendering)** | JavaScript renders in browser | Feed scrolling, real-time interactions | Rich interactivity after initial load |

**Why Not Pure React (CRA)?** → Instagram profiles need to appear in Google Search. CSR-only apps are invisible to search engines. Next.js gives SSR for SEO + CSR for interactivity.

---

### Polyglot Persistence — Which Database for Which Service?

| Service | Database | Why This Choice |
|:--------|:---------|:---------------|
| **User Service** | MySQL | ACID compliance, relational data (users ↔ followers), strong consistency |
| **Follow Service** | MySQL | Follow is a relationship — exactly what SQL is built for, JOINs for mutual followers |
| **Post Service** | MongoDB | Flexible schema (carousel posts, reels, stories all differ), horizontal scaling |
| **Comment Service** | MongoDB | Nested replies, variable-length threads, 16MB doc limit per post is fine |
| **Like Service** | MongoDB + Redis | MongoDB stores individual likes, Redis stores fast counters |
| **Feed Service** | Redis | Pre-built feeds stored as sorted sets, sub-millisecond reads |
| **Search Service** | Elasticsearch | Full-text search, autocomplete, ranking by relevance |
| **Media Storage** | AWS S3 | Object storage designed for binary files, unlimited capacity |

---

### Service-Level Architecture Diagram

```text
                        ┌──────────────────────────┐
                        │   User's Phone / Browser  │
                        │       (Next.js App)        │
                        └────────────┬───────────────┘
                                     │
                                     ▼
                        ┌────────────────────────┐
                        │   CDN (CloudFront)      │ ← Static assets + cached images
                        └────────────┬───────────┘
                                     │
                                     ▼
                        ┌────────────────────────┐
                        │   Load Balancer (Nginx) │ ← Distributes traffic
                        └────────────┬───────────┘
                                     │
                                     ▼
                        ┌────────────────────────┐
                        │   API Gateway           │ ← Auth, Rate Limit, Routing
                        └────────────┬───────────┘
                                     │
              ┌──────────┬───────────┼───────────┬──────────┐
              ▼          ▼           ▼           ▼          ▼
        ┌──────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
        │  Auth    │ │  User  │ │  Post  │ │  Feed  │ │ Search │
        │ Service  │ │Service │ │Service │ │Service │ │Service │
        └────┬─────┘ └───┬────┘ └───┬────┘ └───┬────┘ └───┬────┘
             │           │         │           │          │
             ▼           ▼         ▼           ▼          ▼
        ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌──────┐ ┌────────────┐
        │  Redis  │ │  MySQL  │ │ MongoDB │ │Redis │ │Elasticsearch│
        │(Session)│ │(Users,  │ │(Posts,  │ │(Feed)│ │(Index)      │
        │         │ │Follows) │ │Comments)│ │      │ │             │
        └─────────┘ └─────────┘ └────┬────┘ └──────┘ └────────────┘
                                     │
                                     ▼
                              ┌────────────┐
                              │  AWS S3     │ ← Images & Videos
                              └────────────┘
```

---

### Step-by-Step Flow: User Uploads a Photo

```text
1. User taps "Share" on phone (Next.js frontend)
2. Request hits Load Balancer → routed to available backend server
3. API Gateway validates JWT token (is user authenticated?)
4. Post Service receives photo file + caption
5. Multer middleware handles multipart file stream
6. Sharp library resizes → creates thumb (150px), standard (1080px), original
7. All 3 versions uploaded to AWS S3 → S3 returns URLs
8. Post metadata saved to MongoDB (URLs, caption, userId, timestamp)
9. Fan-out Worker triggered:
   → Queries MySQL for all followers
   → Pushes post ID into each follower's Redis feed list (LPUSH)
   → Trims list to latest 500 posts (LTRIM)
10. CDN caches images at edge locations worldwide
11. Followers open app → feed from Redis → images from CDN
12. Post appears on screen in <200ms ✅
```

---

## 5. 🔧 LOW LEVEL DESIGN (LLD)

### 🧠 Think of it like this
> HLD is the blueprint of a house (rooms, floors). LLD is the wiring diagram — exact placement of every switch, pipe, and wire.

---

### MySQL Tables (CREATE TABLE with indexes)

```sql
-- ========== USERS TABLE ==========
CREATE TABLE users (
    user_id       INT AUTO_INCREMENT PRIMARY KEY,
    username      VARCHAR(30) UNIQUE NOT NULL,
    email         VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    display_name  VARCHAR(50),
    bio           TEXT,
    profile_pic   VARCHAR(500),              -- S3 URL
    followers_count   INT DEFAULT 0,
    following_count   INT DEFAULT 0,
    is_verified   BOOLEAN DEFAULT FALSE,
    is_private    BOOLEAN DEFAULT FALSE,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Indexes for fast lookups
CREATE INDEX idx_users_email ON users(email);        -- Login lookup
CREATE INDEX idx_users_username ON users(username);  -- Profile/search lookup
```

```sql
-- ========== FOLLOWERS TABLE ==========
CREATE TABLE followers (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    follower_id   INT NOT NULL,                      -- The person who follows
    following_id  INT NOT NULL,                      -- The person being followed
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(follower_id, following_id),               -- Prevent duplicate follows
    FOREIGN KEY (follower_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (following_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Indexes for fast "who do I follow?" and "who follows me?" queries
CREATE INDEX idx_followers_follower ON followers(follower_id);
CREATE INDEX idx_followers_following ON followers(following_id);
```

**💡 What are Indexes?** Think of an index like the Table of Contents in a book. Without it, MySQL reads ALL rows to find your data (Full Table Scan — slow). With it, it jumps directly to the right row (fast). We index `email` because every login searches by email.

---

### MongoDB Collections (Example JSON Documents)

**Posts Collection:**
```json
{
  "_id": ObjectId("..."),
  "post_id": "p999",
  "user_id": 101,
  "media": [
    {
      "type": "image",
      "url_thumb": "https://cdn.instagram.com/thumb_p999.webp",
      "url_standard": "https://cdn.instagram.com/std_p999.webp",
      "url_original": "https://s3.aws.com/orig_p999.jpg"
    }
  ],
  "caption": "Living my best life! #dev",
  "hashtags": ["dev", "coding"],
  "likes_count": 1400,
  "comments_count": 85,
  "is_archived": false,
  "created_at": "2024-06-15T10:00:00Z"
}
```

**Comments Collection (Separate for scalability):**
```json
{
  "_id": ObjectId("..."),
  "comment_id": "cm_001",
  "post_id": "p999",
  "user_id": 205,
  "text": "Amazing shot! 🔥",
  "likes_count": 12,
  "parent_comment_id": null,
  "created_at": "2024-06-15T11:00:00Z"
}
```

**Likes Collection:**
```json
{
  "_id": ObjectId("..."),
  "post_id": "p999",
  "user_id": 101,
  "created_at": "2024-06-15T10:30:00Z"
}
```

**💡 Why separate Comments from Posts?** A post with 50,000 comments would hit MongoDB's 16MB document limit if embedded. Separate collections allow pagination (load 20 at a time).

---

### API Design (RESTful Endpoints)

| Method | Path | Description | Auth Required |
|:-------|:-----|:-----------|:-------------|
| `POST` | `/api/v1/auth/signup` | Create new account | ❌ |
| `POST` | `/api/v1/auth/login` | Authenticate user | ❌ |
| `POST` | `/api/v1/posts` | Upload photo/video with caption | ✅ |
| `GET` | `/api/v1/feed?cursor=<id>&limit=20` | Get personalized feed | ✅ |
| `POST` | `/api/v1/posts/:postId/like` | Like a post | ✅ |
| `DELETE` | `/api/v1/posts/:postId/like` | Unlike a post | ✅ |
| `POST` | `/api/v1/posts/:postId/comments` | Add a comment | ✅ |
| `POST` | `/api/v1/users/:userId/follow` | Follow a user | ✅ |
| `DELETE` | `/api/v1/users/:userId/follow` | Unfollow a user | ✅ |
| `GET` | `/api/v1/users/:userId/profile` | Get user profile | ✅ |
| `GET` | `/api/v1/search?q=<query>` | Search users/hashtags | ✅ |

---

### Core Algorithm: Hybrid Feed Generation

```text
┌─────────────────────────────────────────────────────┐
│                  FEED SERVICE                        │
├─────────────────────────────────────────────────────┤
│                                                      │
│  Step 1: GET /feed request arrives                   │
│          ↓                                           │
│  Step 2: Read pre-built feed from Redis (Push)       │
│          → LRANGE feed:{userId} 0 19                 │
│          ↓                                           │
│  Step 3: Identify celebrity follows (MySQL query)    │
│          ↓                                           │
│  Step 4: Pull celebrity latest posts (MongoDB)       │
│          ↓                                           │
│  Step 5: Merge Push + Pull results                   │
│          ↓                                           │
│  Step 6: Apply Ranking Algorithm                     │
│          Score = (Recency × 0.3)                     │
│                + (Relationship × 0.3)                │
│                + (Engagement × 0.2)                  │
│                + (ContentType × 0.2)                 │
│          ↓                                           │
│  Step 7: Filter already-seen posts                   │
│          ↓                                           │
│  Step 8: Return top 20 posts (cursor pagination)     │
│                                                      │
└─────────────────────────────────────────────────────┘
```

**The Celebrity Problem Explained:**
- **Push Model (Fan-out on Write):** When a user posts → push post ID into every follower's Redis list. ✅ Great for normal users (<10K followers). ❌ Ronaldo has 600M followers — pushing to 600M lists would crash the system.
- **Pull Model (Fan-out on Read):** When user opens app → query DB for posts from followed users. ✅ Great for celebrities. ❌ Slow for users following 500+ people.
- **Hybrid:** Push for normal users + Pull for celebrities on read = best of both worlds.

```javascript
// Hybrid Feed — Express.js Implementation
const getHybridFeed = async (req, res) => {
    const userId = req.user.id;

    // STEP A: Get pre-built feed from Redis (Push Model results)
    const pushedPostIds = await redis.lrange(`feed:${userId}`, 0, 19);

    // STEP B: Find which celebrities the user follows
    const celebrities = await db.query(
        `SELECT following_id FROM followers
         WHERE follower_id = ? AND following_id IN (SELECT user_id FROM users WHERE followers_count > 100000)`,
        [userId]
    );

    // STEP C: Pull latest posts from those celebrities (MongoDB)
    const celebPosts = await Post.find({
        user_id: { $in: celebrities.map(c => c.following_id) }
    }).sort({ created_at: -1 }).limit(10);

    // STEP D: Merge and sort by ranking score
    const allPosts = [...pushedPostIds, ...celebPosts];
    const rankedFeed = applyRankingAlgorithm(allPosts);

    res.json({ posts: rankedFeed, nextCursor: rankedFeed[rankedFeed.length - 1]?.post_id });
};
```

---

## 6. 📈 SCALABILITY DESIGN

### 🧠 Think of it like this
> A single chef can cook for 10 people. For 10,000 people, you don't buy a bigger stove (vertical) — you hire 100 chefs and add 50 kitchens (horizontal).

---

### Horizontal Scaling

```text
Vertical Scaling:              Horizontal Scaling:
┌──────────────────┐          ┌────────┐ ┌────────┐ ┌────────┐
│   1 BIG Server   │          │ Small  │ │ Small  │ │ Small  │
│   ($10,000/mo)   │   vs     │ Server │ │ Server │ │ Server │
│   (Has a limit!) │          │ ($500) │ │ ($500) │ │ ($500) │
└──────────────────┘          └────────┘ └────────┘ └────────┘
                               (Add more as needed — no limit!)
```

### Caching Strategy (Redis)

| Data | Cache Duration (TTL) | Why |
|:-----|:--------------------|:----|
| User feed | 5 minutes | Feed doesn't change every second |
| User profile | 1 hour | Name/bio rarely changes |
| Post likes count | 30 seconds | Counts change often but don't need to be exact |
| Session/JWT data | 24 hours | Avoids hitting DB on every API call |

**Cache-Aside Pattern Flow:**
```text
User asks for Feed
    ↓
Is feed in Redis? ── YES → Return from Redis (0.1ms) ✅
    ↓ NO (Cache Miss)
Query MongoDB for feed (50ms)
    ↓
Save result in Redis with TTL
    ↓
Return to user
```

### CDN Usage with Next.js

```text
Without CDN:                     With CDN (CloudFront):
User (India) ──15,000km──→      User (India) ──100km──→ CDN Edge (Mumbai)
    USA Server                        ↓ (If not cached)
    (Slow! 500ms)                    USA Server (Origin)
                                     (Fast! 20ms from edge)
```

- Next.js static assets (JS bundles, CSS) are served from CDN edge
- SSG pages are cached at CDN — zero server load for those pages
- User-uploaded images cached at nearest edge location

### Database Scaling

| Strategy | MySQL | MongoDB |
|:---------|:------|:--------|
| **Replication** | Master (writes) + Read Replicas (reads) | Primary + Secondary Replica Sets |
| **Partitioning** | Range/Hash partition on `user_id` | Built-in sharding via shard key |
| **When** | When reads > 10K RPS on single server | When data > 1TB per collection |

### Scaling Comparison Table (0 → 500M Users)

| Users | Backend | MySQL | MongoDB | Redis | CDN | Special |
|:------|:--------|:------|:--------|:------|:----|:--------|
| **1K** | 1 server | 1 instance | 1 instance | 1 instance | ❌ | Nothing special |
| **100K** | 3 servers + LB | 1 master + 1 replica | 1 replica set | 1 instance | ✅ Basic | Add caching |
| **10M** | 20 servers (auto-scale) | 1 master + 5 replicas | 3-shard cluster | Cluster (3 nodes) | ✅ Multi-region | Microservices split |
| **100M** | 200+ containers (K8s) | Sharded (4 shards) | 10-shard cluster | Cluster (6 nodes) | ✅ Global | Dedicated feed service |
| **500M** | 1000+ containers | Sharded + partitioned | 50+ shards | Multi-AZ cluster | ✅ 400+ edges | Multi-region everything |

---

## 7. 🛡️ RELIABILITY & FAULT TOLERANCE

### 🧠 Think of it like this
> A hospital can't say "Sorry, the cardiac ward is down today." Critical systems must keep running — even when parts break.

---

### What Happens If...

| Failure Scenario | Impact | Solution |
|:-----------------|:-------|:---------|
| **A backend server crashes** | Requests to that server fail | Load Balancer detects via health checks → routes traffic to healthy servers |
| **Redis cache goes down** | Feed loads become slow (fallback to DB) | Redis Sentinel auto-promotes a replica to master; app falls back to DB reads |
| **MySQL master crashes** | All writes fail | Automated failover: promote a read replica to master (RDS Multi-AZ) |
| **MongoDB shard fails** | Data on that shard is unavailable | Replica set: secondary gets auto-promoted, data stays available |
| **S3 outage** | Images won't load for new requests | S3 Cross-Region Replication — CDN serves cached copies from edge |
| **CDN edge fails** | Users in that region get slow loads | CDN automatically routes to next nearest edge location |

### Retry & Fallback Strategies

```text
User Request → Service
    ↓ Fails?
    → Retry (up to 3 times with exponential backoff: 100ms, 400ms, 1600ms)
    ↓ Still fails?
    → Fallback (serve stale cached data from Redis)
    ↓ No cache?
    → Graceful degradation (show "Unable to load feed, try again")
```

### Idempotency

| Operation | Problem Without Idempotency | Solution |
|:----------|:---------------------------|:---------|
| **Like** | Network retry → user likes twice | Check if like already exists before inserting (unique index on `post_id + user_id`) |
| **Follow** | Retry → duplicate follow entry | UNIQUE constraint on `(follower_id, following_id)` |
| **Post Upload** | Retry → duplicate post created | Client sends idempotency key; server checks if key already processed |

### Circuit Breaker Pattern

```text
CLOSED (Normal)           OPEN (Trip!)              HALF-OPEN (Testing)
    │                         │                          │
All requests pass        All requests fail-fast      Let 1 request through
    │                    (don't hit broken service)       │
    ↓                         ↓                          ↓
If failures > threshold  After timeout period        If success → CLOSED
    → OPEN               → HALF-OPEN                If fail → OPEN
```

**Example:** If the Post Service fails 5 times in 10 seconds, the Circuit Breaker "opens" — subsequent requests immediately return an error instead of waiting and timing out. After 30 seconds, it sends one test request. If it succeeds, normal traffic resumes.

---

## 8. 🔌 FLEXIBILITY & EXTENSIBILITY

### 🧠 Think of it like this
> A well-designed house has extra electrical outlets and plumbing connections — you don't break walls to add a new appliance. Similarly, good architecture lets you plug in new features easily.

---

### Adding Notifications (Async, Event-Driven)

```text
User Likes a Post
    ↓
Post Service emits event → Message Queue (RabbitMQ/SQS)
    ↓
Notification Worker picks up event
    ↓
    ├── Saves notification to MongoDB
    ├── Sends push notification (Firebase Cloud Messaging)
    └── Updates unread count in Redis
```

**Why async?** If we sent notifications synchronously inside the Like API, every like would take 500ms+ instead of 50ms. The user shouldn't wait for someone else's notification.

### Multi-Language (i18n)

- Store translations in JSON files per language: `en.json`, `hi.json`, `es.json`
- Next.js has built-in i18n routing: `/en/profile`, `/hi/profile`
- User preference stored in MySQL `users.preferred_language`

### SEO Improvements with Next.js

- **Dynamic `<meta>` tags** per profile page using `getServerSideProps`
- **Open Graph tags** for rich link previews when sharing on WhatsApp/Twitter
- **Sitemap generation** for Explore/public profiles
- **Structured data (JSON-LD)** for Google rich snippets

### Domain-Specific Extensions

| Feature | Architecture Approach |
|:--------|:---------------------|
| **Stories (24h expiry)** | MongoDB TTL Index: `db.stories.createIndex({ created_at: 1 }, { expireAfterSeconds: 86400 })` |
| **Reels (Short Videos)** | Separate Video Processing Service with FFmpeg, HLS streaming |
| **Direct Messages** | WebSocket (Socket.io) for real-time + MongoDB for persistence + Redis Pub/Sub |
| **Explore Page** | Recommendation engine with collaborative filtering, pre-computed in Redis |

---

## 9. 🛠️ DEV-FRIENDLY PRACTICES

### 🧠 Think of it like this
> Even the best recipe is useless if the kitchen is messy. Clean project structure, automated deployments, and monitoring make development sustainable.

---

### Project Structure

```text
instagram/
├── frontend/                    (Next.js App)
│   ├── pages/
│   │   ├── index.js             (Home Feed — SSR)
│   │   ├── profile/[id].js      (User Profile — SSR for SEO)
│   │   ├── explore.js           (Explore Page — SSR)
│   │   └── login.js             (Auth — CSR)
│   ├── components/
│   │   ├── PostCard.js
│   │   ├── FeedList.js
│   │   └── NavBar.js
│   ├── styles/
│   ├── utils/
│   └── next.config.js
│
├── backend/                     (Node.js + Express)
│   ├── routes/
│   │   ├── authRoutes.js
│   │   ├── postRoutes.js
│   │   ├── feedRoutes.js
│   │   └── userRoutes.js
│   ├── controllers/
│   ├── services/
│   ├── middleware/
│   │   ├── authMiddleware.js     (JWT verification)
│   │   └── rateLimiter.js
│   ├── models/
│   │   ├── mysql/                (Sequelize models)
│   │   └── mongo/                (Mongoose models)
│   ├── config/
│   │   ├── db.js
│   │   └── redis.js
│   └── server.js
│
├── workers/                     (Background Jobs)
│   ├── feedFanoutWorker.js
│   ├── imageProcessorWorker.js
│   └── notificationWorker.js
│
├── docker-compose.yml
└── README.md
```

### CI/CD Pipeline

```text
Developer pushes code
        ↓
┌─────────────────────────┐
│   GitHub Actions CI     │
├─────────────────────────┤
│ 1. Lint (ESLint)        │
│ 2. Unit Tests (Jest)    │
│ 3. Integration Tests    │
│ 4. Build Next.js        │
│ 5. Build Docker Image   │
│ 6. Push to ECR          │
└───────────┬─────────────┘
            ↓
┌─────────────────────────┐
│   CD (Deploy)           │
├─────────────────────────┤
│ Staging → Auto Deploy   │
│ Production → Manual     │
│ Approval + Rolling      │
│ Update (zero downtime)  │
└─────────────────────────┘
```

### Logging & Monitoring

| Tool | Purpose | What It Monitors |
|:-----|:--------|:----------------|
| **Winston** (Node.js) | Structured JSON logs | API errors, request duration, user actions |
| **Prometheus** | Metrics collection | RPS, latency percentiles (p50, p95, p99), error rates |
| **Grafana** | Dashboard visualization | Real-time graphs of all Prometheus metrics |
| **ELK Stack** | Log aggregation & search | Search across millions of log lines for debugging |
| **PagerDuty** | Alerting | Notifies on-call engineers when error rate > threshold |

---

## 10. 📝 FINAL NOTES (BEGINNER FRIENDLY)

### Summary Table

| Section | Key Lesson |
|:--------|:-----------|
| **Requirements** | Always separate WHAT the system does (FR) from HOW WELL it does it (NFR) |
| **Scale & Constraints** | Do the math first — know your RPS, storage, and peak before coding |
| **Budget** | Cache is cheaper than more DB servers; CDN is cheaper than more backend servers |
| **HLD** | Use the right DB for the right job (Polyglot Persistence) |
| **LLD** | Design APIs, tables, and documents before writing code |
| **Scalability** | Horizontal > Vertical. Cache > DB. CDN > Origin. |
| **Reliability** | Assume everything will fail. Plan for retries, fallbacks, and circuit breakers |
| **Extensibility** | Event-driven (async) architecture makes adding features easy |
| **Dev Practices** | Clean structure + CI/CD + monitoring = maintainable system |

### Key Takeaways

1. **Polyglot Persistence:** Use MySQL for relationships (users, follows) and MongoDB for content (posts, comments). Don't force one DB to do everything.
2. **Hybrid Feed:** Push for normal users, Pull for celebrities. This is the #1 interview topic for social media design.
3. **Cache Everything Hot:** Redis sits between your app and DB. 80% of reads should hit cache, not DB.
4. **CDN is Non-Negotiable:** For an image-heavy app, CDN reduces latency from 500ms → 20ms.
5. **Design for Failure:** Every component will fail eventually. Health checks, replicas, and circuit breakers keep the system alive.
6. **Start Simple, Scale Gradually:** Don't build for 500M users on day 1. Start with a monolith, split into microservices when needed.

### Common Mistakes Beginners Make

| ❌ Mistake | Why It's Wrong | ✅ Correct Approach |
|:-----------|:--------------|:-------------------|
| Storing images in the database | DB becomes huge and slow; not designed for binary blobs | Store in S3, save URL in DB |
| Using only SQL for everything | Posts/comments have flexible schemas that SQL handles poorly | Polyglot: SQL for relations, NoSQL for content |
| No caching layer | Every request hits DB; DB becomes bottleneck at 10K users | Add Redis cache between app and DB |
| Offset-based pagination | `OFFSET 10000` scans 10,000 rows before returning results | Cursor-based pagination using `last_seen_id` |
| Synchronous notifications | Like API takes 500ms because it sends push notifications inline | Async via message queue (RabbitMQ/SQS) |
| No rate limiting | Bots spam APIs; DB overwhelmed; system crashes | Rate limit at API Gateway (100 req/min per user) |
| Plain text passwords | One DB breach exposes all passwords | Always hash with bcrypt (salt rounds = 10+) |
| Single database server | One server = single point of failure | Master + Read Replicas + automated failover |

---

## 11. 🎤 SCENARIO-BASED Q&A

### Q1: How would you design the Instagram feed for 500M users?
**Answer:** Use a **Hybrid Push/Pull Model**. For normal users (<10K followers), use Push (fan-out on write) — when they post, push the post ID into every follower's Redis feed list. For celebrities (>100K followers), use Pull (fan-out on read) — when a user opens the app, pull celebrity posts from MongoDB on-demand. Merge both sets, apply a ranking algorithm (recency × 0.3 + relationship × 0.3 + engagement × 0.2 + content type × 0.2), and return paginated results. This avoids the "Thundering Herd" problem where a celebrity post would write to 600M Redis lists simultaneously.

### Q2: A user uploads a post, but it doesn't appear in their followers' feed. How do you debug this?
**Answer:** Trace the request through each layer: (1) Check if the post was saved to MongoDB — `db.posts.findOne({post_id: "..."})`. (2) Check if the fan-out worker received the job — inspect the message queue. (3) Check if the post ID was pushed to Redis — `LRANGE feed:{followerId} 0 -1`. (4) Check if the Feed Service read from Redis correctly. Use distributed tracing (Jaeger/Zipkin) to see where the request dropped. Common causes: worker crashed mid-fan-out, Redis connection timeout, or the follower's feed list exceeded the LTRIM limit.

### Q3: Redis goes down during peak hours. What happens and how do you recover?
**Answer:** Immediate impact: feed reads fall back to querying MongoDB directly (50ms instead of 0.1ms), causing latency spikes. Recovery: (1) Redis Sentinel automatically promotes a replica to master within seconds. (2) The app has a fallback path — if Redis read fails, it queries MongoDB and still returns a feed (just slower). (3) Once Redis is back, feeds are lazily rebuilt as users make new posts. Key lesson: **Never make Redis the only source of truth** — it's a cache, not a primary store.

### Q4: How do you ensure SEO for Instagram user profiles using Next.js?
**Answer:** Use `getServerSideProps` in Next.js for profile pages (`/profile/[id].js`). On each request, the server fetches user data and renders HTML with proper `<title>`, `<meta description>`, and Open Graph tags before sending to the browser. Google's crawler receives fully-rendered HTML (not a blank page with JavaScript). For public pages like Explore, use `getStaticProps` with `revalidate` (ISR — Incremental Static Regeneration) to pre-build pages at build time and refresh periodically. This gives the speed of static pages with the freshness of dynamic content.

### Q5: How would you handle a viral post that gets 10 million likes in 1 hour?
**Answer:** The like counter is the bottleneck — 10M writes to MongoDB in 1 hour (~2,800 writes/sec to one document). Solution: **Buffer in Redis first.** Every like increments a Redis counter (`INCR post:p999:likes`). A background worker syncs the Redis counter to MongoDB every 5 seconds in batch. This turns 2,800 writes/sec into 1 write every 5 seconds. The UI reads from Redis for the "live" count. Individual like records are still written to MongoDB (for "unlike" support) but the counter update is decoupled.

### Q6: How would you add a "Stories" feature that auto-deletes content after 24 hours?
**Answer:** Store stories in MongoDB with a `created_at` field. Use MongoDB's **TTL Index**: `db.stories.createIndex({ created_at: 1 }, { expireAfterSeconds: 86400 })`. MongoDB automatically deletes expired documents. For fast reads, cache active stories in Redis (user's story list). When a user opens stories, read from Redis first, fall back to MongoDB. Use a CDN for story media (images/short videos). This approach requires zero cron jobs — the database handles expiration natively.

### Q7: You need to migrate from a monolith to microservices. How would you approach this?
**Answer:** Use the **Strangler Fig Pattern** — don't rewrite everything at once. (1) Identify the highest-traffic, most independent feature (e.g., Feed Service). (2) Build it as a separate Node.js microservice with its own Redis/MongoDB. (3) Route `/feed` requests to the new service via API Gateway while everything else stays in the monolith. (4) Repeat for Post Service, Auth Service, etc. (5) Eventually, the monolith has nothing left — it's been "strangled." Key: each microservice owns its own data store (no shared databases). Services communicate via REST APIs or message queues, never by reading each other's DB directly.

### Q8: How do you prevent a DDoS attack from taking down Instagram's API?
**Answer:** Defense in layers: (1) **CDN Level:** CloudFront absorbs volumetric attacks by distributing traffic across 400+ edge locations. (2) **API Gateway Level:** Rate limiting per API key (100 req/min per user, 10 req/min for unauthenticated). Use Token Bucket algorithm. (3) **WAF (Web Application Firewall):** Block known malicious IPs and patterns. (4) **Auto-scaling:** If legitimate traffic spikes, Kubernetes horizontally scales backend pods. (5) **Circuit Breaker:** If a downstream service is overwhelmed, fail fast instead of cascading the failure. The key is: attackers hit the CDN and API Gateway first — they never reach the backend directly.

---

> **🎓 Study Tip:** Don't memorize diagrams. Understand **WHY** each piece exists (Redis = speed, S3 = files, MySQL = relationships, MongoDB = content). Interviewers want to see you **reason** about trade-offs, not recite answers!
